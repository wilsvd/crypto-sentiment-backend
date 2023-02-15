from transformers import pipeline


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"


class SentimentClassifier:
    def __init__(self) -> None:
        self.sentiment_task = pipeline(
            "sentiment-analysis", model=MODEL, tokenizer=MODEL, device=0
        )

    def _get_encoding(self, ratings):
        if "positive" in ratings:
            return 1
        elif "neutral" in ratings:
            return 0
        else:
            return -1

    def predict_sentiment(self, posts):

        predictions = self.sentiment_task(posts, batch_size=16)

        total_sentiment = 0
        for prediction in predictions:
            encoded_prediction = self._get_encoding(prediction["label"])
            total_sentiment += encoded_prediction

        return round(total_sentiment / len(posts), 2)
