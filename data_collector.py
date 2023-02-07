from cmc_api import CoinMarketCapAPI
from reddit_api import RedditAPI
from process_text import TextProcessor

# from pprint import pprint
from praw.models.reddit.submission import Submission
from sentiment_classifier import SentimentClassifier

import time

import json

CRYPTO_LIMIT = 100

# TODO: Use the post limit specified

POST_LIMIT = 50

class DataCollector():
        
    m_ids = []

    def __init__(self) -> None:    
        self.cmc = CoinMarketCapAPI()
        r_api = RedditAPI()
        self.reddit = r_api.connect_to_reddit()
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
            result = ""
            if coin_data[id]['subreddit'] != '':
                result = (coin_data[id]['subreddit'])
            elif coin_data[id]['name'] != '':
                result = (coin_data[id]['name'])
            elif coin_data[id]['symbol'] != '':
                result = (coin_data[id]['symbol'])
            subreddits.append(result)
        return subreddits

    # TODO: Optimise _get_submission function.
    def _get_submission(self, subreddit):

        total_sentiment = 0
        post_count = 0
        for submission in self.reddit.subreddit(subreddit).hot():
            if (submission.stickied == False and TextProcessor().is_question(submission.title)):
                sentiment = self.classifier.predict_sentiment(submission.title)
                post_count += 1
                total_sentiment += sentiment
        # Account for a division by 0 error by just returning None
        if post_count == 0:
            return None
        
        result = {"sentiment": round(total_sentiment/post_count, 2)}              
        return result
      
    def _get_valid_subreddit(self, subreddits_info):
            options = self.reddit.subreddits.search_by_name(subreddits_info) # Searches for the subreddit.
            if len(options) > 0:
                return str(options[0])

    def find_coin_sentiments(self):
        subreddits = self._get_coin_subreddits()
        overall_feeling = {}

        valid_subreddits = []
        for subreddits_info in subreddits:
            subreddit = self._get_valid_subreddit(subreddits_info)
            valid_subreddits.append(subreddit)
        
        print(valid_subreddits)
        for subreddit in valid_subreddits:
            result = self._get_submission(subreddit)
            if result:
                overall_feeling[subreddit] = result
        
        return overall_feeling

# Top 10
import time

start = time.time()
data = DataCollector()
overall_sentiment = data.find_coin_sentiments()
end = time.time()

print(f"Time taken: {end-start}")
