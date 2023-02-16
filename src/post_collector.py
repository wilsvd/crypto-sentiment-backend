from reddit_api import RedditAPI
from process_text import TextProcessor
from classifier import SentimentClassifier
from firebase import FirebaseDatabase
from prawcore.exceptions import NotFound

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

                if not submission.stickied and TextProcessor().is_question(
                    submission.title
                ):
                    posts[submission.id] = submission.title

            print(reddit_helper.auth.limits)

            new_sent_preds = {}
            if len(posts) > 0:
                new_sent_preds = self.classifier.predict_sentiment(posts)

            if new_sent_preds and len(new_sent_preds) > 0:
                for key, value in new_sent_preds.items():
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
        except NotFound:
            print("Subreddit does not exist")
            return None

    def find_partition_sentiment(self, partition, reddit_helper, stored_posts):
        partition_sentiment = {}

        for subreddit in partition:

            if (
                stored_posts
                and "data" in stored_posts
                and subreddit in stored_posts["data"]
            ):
                sub_info = stored_posts["data"][subreddit]
                res = self._get_submission(reddit_helper, subreddit, sub_info)
                if res:
                    partition_sentiment[subreddit] = res
            else:
                res = self._get_submission(reddit_helper, subreddit, {})
                if res:
                    partition_sentiment[subreddit] = res

        return partition_sentiment

    def find_crypto_sentiments(
        self, total_subreddits: list, database: FirebaseDatabase
    ):
        overall_feeling = {}

        # Partition total_subreddits as evenly as possible
        partitions = np.array_split(total_subreddits, 4)

        reddit_helpers = self.r_api.multi_acc_multi_instance()

        existing_post_data = {}
        if database:
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
