from post_collector import SentimentCollector
from coin_collector import CoinCollector
from firebase import FirebaseDatabase


if __name__ == "__main__":
    data = SentimentCollector()
    coins = CoinCollector()
    database = FirebaseDatabase()

    subreddits = coins.get_coin_subreddits()
    overall_sentiment = data.find_crypto_sentiments(subreddits, database)
    database.set_data(overall_sentiment)
