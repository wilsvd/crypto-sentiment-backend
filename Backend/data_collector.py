from cmc_api import CoinMarketCapAPI
from reddit_api import RedditAPI
from pprint import pprint
import json

NUM_POSTS = 5
CRYPTO_LIMIT = 5

class DataCollector():
        
    m_ids = []

    def __init__(self) -> None:    
        self.cmc = CoinMarketCapAPI()
        r_api = RedditAPI()
        self.reddit = r_api.connect_to_reddit()
        self._set_coin_ids()
        
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
            if coin_data[id]['subreddit'] != '':
                subreddits.append(coin_data[id]['subreddit'])
        return subreddits

    def _get_submission(self, subreddit:str="Cryptocurrency"):
        ratings = {}
        print(subreddit)
        encoding = 0
        for submission in self.reddit.subreddit(subreddit).hot(limit=NUM_POSTS):
            ratings[submission.title] = encoding
        return ratings
      
    def _find_coin_sentiments(self):
        subreddits = self._get_coin_subreddits()

        overall_feeling = {}
        for subreddit in subreddits:
            options = self.reddit.subreddits.search_by_name(subreddit) # Searches for the subreddit.
            if len(options) > 0:  
                name = str(options[0])
                overall_feeling[subreddit] = data._get_submission(name)
        return overall_feeling

data = DataCollector()
overall_sentiment = data._find_coin_sentiments()


with open("./sentiment/overall_sentiment.json", "w") as outfile:
            json.dump(overall_sentiment, outfile)

