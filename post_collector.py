from reddit_api import RedditAPI
from process_text import TextProcessor
from classifier import SentimentClassifier
from firebase import FirebaseDatabase

import numpy as np

# from threading import Thread
from concurrent.futures import ThreadPoolExecutor


# TODO: Use the post limit specified
POST_LIMIT = 50


class SentimentCollector:
    m_ids = []

    def __init__(self) -> None:
        self.r_api = RedditAPI()
        self.classifier = SentimentClassifier()

    # TODO: Optimise _get_submission function.
    def _get_submission(self, reddit_helper, subreddit, sub_info):
        # NOTE: PRAW is fetching 100 submissions in one request.

        seen_submissions = {}
        if sub_info and "posts" in sub_info:
            seen_submissions = sub_info["posts"]

        try:
            total_sentiments = {}
            posts = {}
            submissions = reddit_helper.subreddit(subreddit).hot()
            for submission in submissions:
                if submission.id in seen_submissions:
                    continue

                if submission.stickied == False and TextProcessor().is_question(
                    submission.title
                ):
                    posts[submission.id] = submission.title

            print(reddit_helper.auth.limits)
            # Account for a division by 0 error by just returning None (Effectively ignoring the subreddit)

            new_sentiment_predictions = {}
            if len(posts) > 0:
                new_sentiment_predictions = self.classifier.predict_sentiment(posts)

            if new_sentiment_predictions and len(new_sentiment_predictions) > 0:
                for key, value in new_sentiment_predictions.items():
                    total_sentiments[key] = value
            if seen_submissions and len(seen_submissions) > 0:
                for key, value in seen_submissions.items():
                    total_sentiments[key] = value

            sentiment = round(
                sum(list(total_sentiments.values())) / len(total_sentiments), 2
            )
            return {
                "posts": total_sentiments,
                "sentiment": sentiment,
            }
        except:
            print("Subreddit does not exist")
            return None

    def find_partition_sentiment(self, partition, reddit_helper, existing_post_data):
        partition_sentiment = {}

        for subreddit in partition:

            if (
                existing_post_data
                and "data" in existing_post_data
                and subreddit in existing_post_data["data"]
            ):
                sub_info = existing_post_data["data"][subreddit]
                result = self._get_submission(reddit_helper, subreddit, sub_info)
                if result:
                    partition_sentiment[subreddit] = result
            else:
                result = self._get_submission(reddit_helper, subreddit, {})
                if result:
                    partition_sentiment[subreddit] = result

        return partition_sentiment

    def find_crypto_sentiments(
        self, total_subreddits: list, database: FirebaseDatabase
    ):
        overall_feeling = {}

        # Partition total_subreddits as evenly as possible
        partitions = np.array_split(total_subreddits, 4)

        reddit_helpers = self.r_api.multi_acc_multi_instance()

        existing_post_data = database.ref.get()
        threadFutures = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for worker, partition in enumerate(partitions):
                reddit_helper = reddit_helpers[worker]
                future = executor.submit(
                    self.find_partition_sentiment,
                    partition,
                    reddit_helper,
                    existing_post_data,
                )
                threadFutures.append(future)

        for future in threadFutures:
            partition_dict: dict = future.result()
            for key, value in partition_dict.items():
                overall_feeling[key] = value
        return overall_feeling
