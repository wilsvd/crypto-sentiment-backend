from reddit_api import RedditAPI
from process_text import TextProcessor
from classifier import SentimentClassifier
from prawcore.exceptions import NotFound
from firestore import FirestoreDatabase
from datetime import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# TYPES:
# historical_data = {"time": now_time, "sentiment": sentiment}
# post_data = {
#     "date_added": now_time,
#     "title": f"Some text with number: {i}",
#     "sentiment": sentiment,
# }


class SentimentCollector:
    m_ids = []

    def __init__(self) -> None:
        self.r_api = RedditAPI()
        self.classifier = SentimentClassifier()
        self.firedb = FirestoreDatabase()
        self.tp = TextProcessor()

    def _find_partition_sentiment(self, partition, reddit_helper):
        for crypto_info in partition:
            name = crypto_info[0]
            subreddit = crypto_info[1]
            self._get_submission(reddit_helper, name, subreddit)

    # TODO: Optimise _get_submission function.
    def _get_submission(self, reddit_helper, crypto_name, subreddit):
        # NOTE: PRAW is fetching 100 submissions in one request.
        try:
            new_posts = {}
            posts = reddit_helper.subreddit(subreddit).hot()
            for post in posts:
                data = self.firedb.post_data_exists(subreddit, post.id)

                if data.exists:
                    continue

                if not post.stickied and self.tp.is_question(post.title):
                    new_posts[post.id] = [
                        post.title,
                        datetime.fromtimestamp(post.created_utc),
                    ]

            print(reddit_helper.auth.limits)

            self._store_crypto_data(crypto_name, new_posts)
        except NotFound:
            print("Subreddit does not exist")
            return None
        except:
            print("Some error occurred")
            return None

    def _store_crypto_data(self, crypto_name: str, new_posts: dict):
        try:
            # Calculate new sentiment based on new crypto posts
            new_sent_preds = {}
            if len(new_posts) > 0:
                post_ids = list(new_posts.keys())
                post_data = list(new_posts.values())
                post_titles = [item[0] for item in post_data]
                new_sent_preds = self.classifier.predict_sentiment(
                    post_ids, post_titles
                )
            # Store new posts data in Firestore
            batch = self.firedb.db.batch()
            for post_id in new_posts.keys():
                # NOTE: posts and new_sent_preds share the same keys
                # since the keys are the submission ids.
                title = new_posts[post_id][0]
                date = new_posts[post_id][1]
                sentiment = new_sent_preds[post_id]

                post_data = {
                    "datetime": date,
                    "title": title,
                    "sentiment": sentiment,
                }
                self.firedb.batch_write(batch, crypto_name, post_id, post_data)
            batch.commit()
            self.firedb.del_old_n_posts(batch, crypto_name)

            # Calculate new overall sentiment for crypto
            total_sentiment = self.firedb.get_total_sentiment(crypto_name)
            total_posts = self.firedb.get_count(crypto_name)
            now_datetime = datetime.now()

            # Store historical data in Firestore
            self.firedb.add_historical_data(
                crypto_name,
                {
                    "datetime": now_datetime,
                    "sub_sentiment": round(total_sentiment / total_posts, 2),
                },
            )
        except:
            print("Some error occurred")
            return None

        # Get the new total sentiment data for the subreddit

    def find_crypto_sentiments(self, total_cryptocurrencies: list):

        # Partition total_cryptocurrencies as evenly as possible
        partitions = np.array_split(total_cryptocurrencies, 4)

        reddit_helpers = self.r_api.multi_acc_multi_instance()

        with ThreadPoolExecutor(max_workers=4) as executor:
            for worker, partition in enumerate(partitions):
                reddit_helper = reddit_helpers[worker]
                executor.submit(
                    self._find_partition_sentiment,
                    partition,
                    reddit_helper,
                )
