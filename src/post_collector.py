from reddit_api import RedditAPI
from process_text import TextProcessor
from classifier import SentimentClassifier
from prawcore.exceptions import NotFound
from firestore import FirestoreDatabase

from datetime import datetime

import numpy as np

# from threading import Thread
from concurrent.futures import ThreadPoolExecutor


# TODO: Use the post limit specified
POST_LIMIT = 100


class SentimentCollector:
    m_ids = []

    def __init__(self) -> None:
        self.r_api = RedditAPI()
        self.classifier = SentimentClassifier()
        self.database = FirestoreDatabase()
        self.tp = TextProcessor()

    # TODO: Optimise _get_submission function.
    def _get_submission(self, reddit_helper, subreddit):
        # NOTE: PRAW is fetching 100 submissions in one request.

        # historical_data = {"datetime": now_datetime, "total_sentiment": sentiment}
        # post_data = {
        #     "datetime": now_datetime,
        #     "title": f"Some text with number: {i}",
        #     "sentiment": sentiment,
        # }

        try:
            seen_posts = {}
            new_posts = {}
            posts = reddit_helper.subreddit(subreddit).hot()
            now_datetime = datetime.now()

            # Check if a post already exists

            for post in posts:
                data = self.database.post_data_exists(subreddit, post.id)
                if data.exists:
                    seen_posts[post.id] = data.to_dict()["sentiment"]
                    continue

                if not post.stickied and self.tp.is_question(post.title):
                    new_posts[post.id] = post.title

            print(reddit_helper.auth.limits)

            new_sent_preds = {}
            if len(new_posts) > 0:
                new_sent_preds = self.classifier.predict_sentiment(new_posts)

            # Combine titles and sentiments into one
            # NOTE: posts and new_sent_preds share the same keys since the keys are the submission ids.

            for post_id in new_posts.keys():
                title = new_posts[post_id]
                sentiment = new_sent_preds[post_id]

                post_data = {
                    "datetime": now_datetime,
                    "title": title,
                    "sentiment": sentiment,
                }
                self.database.add_post_data(subreddit, post_id, post_data)
            total_sentiment = self.database.get_total_sentiment(subreddit)
            total_posts = self.database.get_count(subreddit)
            self.database.add_historical_data(
                subreddit,
                {
                    "datetime": now_datetime,
                    "sub_sentiment": round(total_sentiment / total_posts, 2),
                },
            )
            # Get the new total sentiment data for the subreddit

        except NotFound:
            print("Subreddit does not exist")
            return None

    def find_partition_sentiment(self, partition, reddit_helper):

        for subreddit in partition:
            self._get_submission(reddit_helper, subreddit)

    def find_crypto_sentiments(self, total_subreddits: list):

        # Partition total_subreddits as evenly as possible
        partitions = np.array_split(total_subreddits, 4)

        reddit_helpers = self.r_api.multi_acc_multi_instance()

        with ThreadPoolExecutor(max_workers=4) as executor:
            for worker, partition in enumerate(partitions):
                reddit_helper = reddit_helpers[worker]
                executor.submit(
                    self.find_partition_sentiment,
                    partition,
                    reddit_helper,
                )


# Template:
# historical_data = {"time": now_time, "sentiment": sentiment}
# post_data = {
#     "date_added": now_time,
#     "title": f"Some text with number: {i}",
#     "sentiment": sentiment,
# }

# submission_id = f"submission{i}"
# firedb.add_historical_data("ethereum", historical_data)
# firedb.add_post_data("ethereum", submission_id, post_data)
