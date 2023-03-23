from transformers import pipeline

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"


class SentimentClassifier:
    def __init__(self) -> None:
        self.sentiment_task = pipeline(
            "sentiment-analysis", model=MODEL, tokenizer=MODEL
        )

    def _get_encoding(self, ratings):
        if "positive" in ratings:
            return 1
        elif "neutral" in ratings:
            return 0
        else:
            return -1

    def predict_sentiment(self, post_ids: list, post_titles: list):
        post_sentiments = {}
        predictions = self.sentiment_task(post_titles, batch_size=16)
        for i in range(len(post_ids)):
            encoding = self._get_encoding(predictions[i]["label"])
            post_sentiments[post_ids[i]] = encoding

        return post_sentiments
