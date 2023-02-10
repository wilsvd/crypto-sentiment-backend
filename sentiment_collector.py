from reddit_api import RedditAPI

import time

import praw.reddit

# from threading import Thread
from concurrent.futures import ThreadPoolExecutor


# TODO: Use the post limit specified
POST_LIMIT = 50


class SentimentCollector:

    m_ids = []

    def __init__(self) -> None:
        self.r_api = RedditAPI()

    # TODO: Optimise _get_submission function.
    def _get_submission(self, reddit_helper, subreddit):

        try:

            submissions = reddit_helper.subreddit(subreddit).hot(limit=POST_LIMIT)
            # PRAW Uses lazy loading so the fetch only occurs once the data is actually going to be used.
            count = 0
            for submission in submissions:
                count += 1
        except:
            print("Subreddit does not exist")

    def find_crypto_sentiments(self, total_subreddits):

        # NOTE: Partition when using Alternating/Multi-threading
        # partitions = np.array_split(total_subreddits, 4)

        # NOTE: Single Acc/Single PRAW
        # single = self.r_api.single_instance()
        # reddit_helper = single[0]
        # for subreddit in total_subreddits:
        # self._get_submission(reddit_helper, subreddit)

        # single_multi = self.r_api.single_acc_multi_instance()
        # multi_multi = self.r_api.multi_acc_multi_instance()

        # print(multi_multi[0].auth.limits)
        # print(multi_multi[1].auth.limits)
        # print(multi_multi[2].auth.limits)

        # NOTE: Single Acc/Multi PRAW --- Alternating
        # for worker, subreddit in enumerate(total_subreddits):
        #     worker_index = worker % 4
        #     reddit_helper = single_multi[worker_index]
        #     print(reddit_helper.auth.limits)
        #     self._get_submission(reddit_helper, subreddit)

        # NOTE: Multi Acc/Multi PRAW --- Alternating
        # for worker, subreddit in enumerate(total_subreddits):
        #     worker_index = worker % 4
        #     reddit_helper = self.multi_multi[worker_index]
        #     self._get_submission(reddit_helper, subreddit)

        # NOTE: Single Acc/Multi PRAW --- Multi-threading

        # NOTE: Multi Acc/Multi PRAW --- Multi-threading

        # return overall_feeling

    # def find_partition_sentiment(self, partition, reddit_helper):
    #     partition_sentiment = {}
    #     for subreddit in partition:
    #         result = self._get_submission(reddit_helper, subreddit)
    #         if result:
    #             partition_sentiment[subreddit] = result
    #     print(partition_sentiment)
    # return partition_sentiment
