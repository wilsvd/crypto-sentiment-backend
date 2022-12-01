from data_collector import DataCollector
import json

data = DataCollector()

def runner():
    print("JOB START")
    overall_sentiment = data.find_coin_sentiments()
    with open("./sentiment/sentiment_data1.json", "w") as outfile:
                json.dump(overall_sentiment, outfile)
    print("JOB DONE")

runner()