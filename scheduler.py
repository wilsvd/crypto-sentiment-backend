from post_collector import SentimentCollector
from coin_collector import CoinCollector
from firebase import FirebaseDatabase

import os

import time

from pprint import pprint

if __name__ == "__main__":
    data = SentimentCollector()
    coins = CoinCollector()
    database = FirebaseDatabase()
    print("JOB START")
    start = time.time()
    subreddits = coins.get_coin_subreddits()
    overall_sentiment = data.find_crypto_sentiments(subreddits, database)
    database.set_data(overall_sentiment)
    end = time.time()
    print("JOB DONE")
    print(f"Time taken: {end-start}")
