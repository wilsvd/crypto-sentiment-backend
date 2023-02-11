from reddit_api import RedditAPI
from process_text import TextProcessor
from sentiment_classifier import SentimentClassifier

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
    def _get_submission(self, reddit_helper, subreddit):

        total_sentiment = 0
        post_count = 0
        # NOTE: PRAW is fetching 100 submissions in one request.

        try:
            submissions = reddit_helper.subreddit(subreddit).hot()
            for submission in submissions:
                if submission.stickied == False and TextProcessor().is_question(
                    submission.title
                ):
                    sentiment = self.classifier.predict_sentiment(submission.title)
                    post_count += 1
                    total_sentiment += sentiment
            print(reddit_helper.auth.limits)
            # Account for a division by 0 error by just returning None (Effectively ignoring the subreddit)
            if post_count == 0:
                return None

            return round(total_sentiment / post_count, 2)
        except:
            print("Subreddit does not exist")
            return None

    def find_crypto_sentiments(self, total_subreddits):
        overall_feeling = []

        # Partition total_subreddits as evenly as possible
        partitions = np.array_split(total_subreddits, 4)

        reddit_helpers = self.r_api.multi_acc_multi_instance()

        threadFutures = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for worker, partition in enumerate(partitions):
                reddit_helper = reddit_helpers[worker]
                future = executor.submit(
                    self.find_partition_sentiment,
                    partition,
                    reddit_helper,
                    overall_feeling,
                )
                threadFutures.append(future)

        for future in threadFutures:
            for items in future.result():
                overall_feeling.append(items)
        return overall_feeling

    def find_partition_sentiment(self, partition, reddit_helper, overall_feeling):
        partition_sentiment = []

        for subreddit in partition:
            crypto_data = {}
            result = self._get_submission(reddit_helper, subreddit)
            if result:
                crypto_data["cryptocurrency"] = subreddit
                crypto_data["sentiment"] = result
                partition_sentiment.append(crypto_data)
        return partition_sentiment
