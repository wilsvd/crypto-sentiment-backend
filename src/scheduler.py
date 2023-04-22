from post_collector import SentimentCollector
from coin_collector import CoinCollector
import time

"""
A script to collect sentiment data from cryptocurrency subreddits.

Modules:
    post_collector: A module that collects posts from Reddit subreddits.
    coin_collector: A module that finds cryptocurrency subreddits on Reddit.

Usage:
    This script can be run directly, in which case it will collect sentiment data from cryptocurrency subreddits and output the time taken to complete the task.

Functions:
    __main__():
        Instantiates the CoinCollector and SentimentCollector objects, finds the cryptocurrency subreddits using the CoinCollector, and calculates the sentiment of each subreddit using the SentimentCollector. Outputs the time taken to complete the task.

Returns:
    None
"""

if __name__ == "__main__":
    coins = CoinCollector()
    data = SentimentCollector()

    start = time.time()
    subreddits = coins.get_coin_subreddits()
    overall_sentiment = data.find_crypto_sentiments(subreddits)
    end = time.time()
    print(f"Time taken: {end - start}")
