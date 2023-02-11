from sentiment_collector import SentimentCollector
from coin_collectors import CoinCollector

import json

import os

dir_path = os.path.dirname(os.path.abspath(__file__))

print(dir_path)
sentiment_path = os.path.join(dir_path, "sentiment/sentiment_data.json")
print(sentiment_path)

data = SentimentCollector()
coins = CoinCollector()

subreddits = coins._get_coin_subreddits()

import time


def runner():
    start = time.time()
    print("JOB START")
    overall_sentiment = data.find_crypto_sentiments(subreddits)
    with open(sentiment_path, "w") as outfile:
        json.dump(overall_sentiment, outfile)
    print("JOB DONE")
    end = time.time()
    print(f"Time taken: {end-start}")


runner()
