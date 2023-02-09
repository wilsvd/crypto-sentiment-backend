from reddit_api import RedditAPI
from process_text import TextProcessor
from sentiment_classifier import SentimentClassifier

import numpy as np

# from threading import Thread
from concurrent.futures import ThreadPoolExecutor


# TODO: Use the post limit specified
POST_LIMIT = 50

class SentimentCollector():
        
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
                if (submission.stickied == False and TextProcessor().is_question(submission.title)):
                    sentiment = self.classifier.predict_sentiment(submission.title)
                    post_count += 1
                    total_sentiment += sentiment
            # Account for a division by 0 error by just returning None (Effectively ignoring the subreddit)
            if post_count == 0:
                return None
            
            result = {"sentiment": round(total_sentiment/post_count, 2)}              
            return result
        except:
            print("Subreddit does not exist")
            return None        
      
    # def _get_valid_subreddit(self, subreddits_info):
    #         options = self.reddit.subreddits.search_by_name(subreddits_info) # Searches for the subreddit.
    #         if len(options) > 0:
    #             return str(options[0])

    def find_crypto_sentiments(self, total_subreddits):
        # overall_feeling = {}

        # Partition total_subreddits as evenly as possible
        partitions = np.array_split(total_subreddits, 4)

        with ThreadPoolExecutor(max_workers=4) as executor:
            for worker, partition in enumerate(partitions):
                reddit_helper = self.r_api.connect_to_reddit(worker)
                executor.submit(self.find_partition_sentiment, partition, reddit_helper)

        # for worker, partition in enumerate(partitions):
        #     reddit_helper = self.r_api.connect_to_reddit(worker)
        #     t = Thread(target=self.find_partition_sentiment, args=(partition, reddit_helper))
        #     t.start()

        # for worker, subreddit in enumerate(total_subreddits):
        #     worker_index = worker % 4
        #     reddit_helper = self.worker_queue[worker_index]
        #     result = self._get_submission(reddit_helper, subreddit)
        #     if result:
        #         overall_feeling[subreddit] = result        
        
        # return overall_feeling

    def find_partition_sentiment(self, partition, reddit_helper):
        partition_sentiment = {}
        for subreddit in partition:
            result = self._get_submission(reddit_helper, subreddit)
            if result:
                partition_sentiment[subreddit] = result  
        print(partition_sentiment)
        # return partition_sentiment

# Top 10

