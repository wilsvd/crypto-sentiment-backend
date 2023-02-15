from post_collector import SentimentCollector
from coin_collector import CoinCollector
from firebase import FirebaseDatabase

import os

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.abspath(__file__))
    sentiment_path = os.path.join(dir_path, "sentiment/sentiment_data.json")
    data = SentimentCollector()
    coins = CoinCollector()
    database = FirebaseDatabase()
    subreddits = coins.get_coin_subreddits()
    overall_sentiment = data.find_crypto_sentiments(subreddits)
    database.set_data(overall_sentiment)
