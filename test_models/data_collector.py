from cmc_api import CoinMarketCapAPI
from reddit_api import RedditAPI
from process_text import TextProcessor

# from pprint import pprint
from praw.models.reddit.submission import Submission

import json

CRYPTO_LIMIT = 10


class DataCollector:

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
        for item in map_info["data"]:
            ids.append(str(item["id"]))
        self.m_ids = ids

    def _get_coin_subreddits(self):
        coin_ids = self._get_coin_ids()
        ids = ",".join(coin_ids)
        cmc_meta = self.cmc.get_Cryptocurrency_Meta_Info(ids)
        subreddits = self._clean_coin_data(ids=coin_ids, coin_data=cmc_meta["data"])
        return subreddits

    def _clean_coin_data(self, ids, coin_data):
        subreddits = []
        for id in ids:
            names = []
            if coin_data[id]["subreddit"] != "":
                names.append(coin_data[id]["subreddit"])
            if coin_data[id]["name"] != "":
                names.append(coin_data[id]["name"])
            if coin_data[id]["symbol"] != "":
                names.append(coin_data[id]["symbol"])
            subreddits.append(names)
        return subreddits

    def _get_submission(self, subreddit: str = "Cryptocurrency", post_limit=50):
        ratings = {}
        encoding = [
            "negative",
            "neutral",
            "positive",
            "bearish",
            "neutral",
            "bullish",
        ]
        count = 0
        for submission in self.reddit.subreddit(subreddit).hot():
            if count == post_limit:
                break
            if submission.stickied == False and TextProcessor().is_question(
                submission.title
            ):
                ratings[submission.title] = encoding
                count += 1

        return ratings

    def _get_valid_subreddit(self, subreddits_info):
        for subreddit in subreddits_info:
            options = self.reddit.subreddits.search_by_name(
                subreddit
            )  # Searches for the subreddit.
            if len(options) > 0:
                name = str(options[0])
                return name

    def find_coin_sentiments(self):
        subreddits = self._get_coin_subreddits()
        overall_feeling = {}
        for subreddits_info in subreddits:
            subreddit = self._get_valid_subreddit(subreddits_info)
            overall_feeling[subreddit] = data._get_submission(subreddit)

        overall_feeling["Cryptocurrency"] = data._get_submission("Cryptocurrency", 100)
        overall_feeling["CryptoMoonShoots"] = data._get_submission(
            "CryptoMoonShoots", 100
        )
        return overall_feeling


data = DataCollector()
overall_sentiment = data.find_coin_sentiments()

with open("./sentiment/overall_sentiment.json", "w") as outfile:
    json.dump(overall_sentiment, outfile)
