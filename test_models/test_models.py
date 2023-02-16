import json
from pprint import pprint

SENTIMENTS = "./sentiment/copy_overall_sentiment.json"


def extract_data():
    with open(SENTIMENTS) as json_file:
        file: dict = json.load(json_file)

        data = []
        for post in file:
            for info in file[post]:
                data.append([info, file[post][info]])
                # print(info)
    return data
