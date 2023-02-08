from cmc_api import CoinMarketCapAPI
from reddit_api import RedditAPI
from process_text import TextProcessor

import numpy as np

# from pprint import pprint
from praw.models.reddit.submission import Submission
from sentiment_classifier import SentimentClassifier

import time

import json

CRYPTO_LIMIT = 20

# TODO: Use the post limit specified
POST_LIMIT = 50

class DataCollector():
        
    m_ids = []

    def __init__(self) -> None:    
        self.cmc = CoinMarketCapAPI()
        self.r_api = RedditAPI()
        self._set_coin_ids()
        self.classifier = SentimentClassifier()
        
    def _get_coin_ids(self):
        return self.m_ids

    def _set_coin_ids(self):
        map_info = self.cmc.get_Cryptocurrency_Map_Info(limit=CRYPTO_LIMIT)
        ids = []
        for item in map_info['data']:
            ids.append(str(item['id']))
        self.m_ids = ids

    def _get_coin_subreddits(self):
        coin_ids = self._get_coin_ids()
        ids = ",".join(coin_ids)
        cmc_meta = self.cmc.get_Cryptocurrency_Meta_Info(ids)
        subreddits = self._clean_coin_data(ids=coin_ids, coin_data=cmc_meta['data'])
        return subreddits
    
    def _clean_coin_data(self, ids, coin_data):
        subreddits = []
        for id in ids:
            subredditName = coin_data[id]['subreddit']
            if subredditName != '' or subredditName != "":
                subreddits.append(subredditName)
            
        return subreddits

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

    def find_coin_sentiments(self):
        total_subreddits = self._get_coin_subreddits()
        # Partition total_subreddits as evenly as possible
        partitions = np.array_split(total_subreddits, 4)
        overall_feeling = {}

        for worker, partition in enumerate(partitions):
            reddit_helper = self.r_api.connect_to_reddit(worker)
            for subreddit in partition:
                result = self._get_submission(reddit_helper, subreddit)
                if result:
                    overall_feeling[subreddit] = result        
        
        return overall_feeling

# Top 10

