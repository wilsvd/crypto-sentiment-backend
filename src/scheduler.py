from post_collector import SentimentCollector
from coin_collector import CoinCollector

import time

if __name__ == "__main__":
    data = SentimentCollector()
    coins = CoinCollector()

    start = time.time()
    subreddits = coins.get_coin_subreddits()

    overall_sentiment = data.find_crypto_sentiments(subreddits)
    end = time.time()
    print(f"Time taken: {end - start}")
