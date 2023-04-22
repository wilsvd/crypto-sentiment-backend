from transformers import pipeline

# Huggingface model for sentiment analysis
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"


class SentimentClassifier:
    """
    A sentiment analysis model that uses the Huggingface library to predict the sentiment of a given text.

    Attributes:
        sentiment_task: A Huggingface pipeline object that performs sentiment analysis on text.

    Methods:
        __init__():
            Initializes the sentiment analysis pipeline using the Huggingface model.

        _get_encoding(label: str) -> int:
            Maps sentiment labels returned by the Huggingface model to integers.

        predict_sentiment(post_ids: list, post_titles: list) -> dict:
            Predicts the sentiment of a list of post titles using the Huggingface model.

    """

    def __init__(self) -> None:
        """
        Initializes the sentiment analysis pipeline using the Huggingface model.

        Parameters:
            None

        Returns:
            None
        """
        self.sentiment_task = pipeline(
            "sentiment-analysis", model=MODEL, tokenizer=MODEL
        )

    def _get_encoding(self, label: str) -> int:
        """
        Maps sentiment labels returned by the Huggingface model to integers.

        Parameters:
            label (str): A sentiment label string.

        Returns:
            int: The corresponding sentiment encoding (1 for positive, 0 for neutral, -1 for negative).
        """
        if "positive" == label:
            return 1
        elif "neutral" == label:
            return 0
        else:
            return -1

    def predict_sentiment(self, post_ids: list, post_titles: list) -> dict:
        """
        Predicts the sentiment of a list of post titles using the Huggingface model.

        Parameters:
            post_ids (list): A list of post IDs.
            post_titles (list): A list of post titles.

        Returns:
            dict: A dictionary mapping each post ID to its corresponding sentiment encoding.
        """
        post_sentiments = {}
        predictions = self.sentiment_task(post_titles, batch_size=16)
        for i in range(len(post_ids)):
            encoding = self._get_encoding(predictions[i]["label"])
            post_sentiments[post_ids[i]] = encoding

        return post_sentiments
