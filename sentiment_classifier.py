from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import pandas as pd
from joblib import dump, load


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"

class SentimentClassifier():

    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.config = AutoConfig.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    def _get_encoding(self, ratings):
        if "positive" in ratings:
            return 1
        elif "neutral" in ratings:
            return 0
        else:
            return -1

    # Preprocess text (username and link placeholders)
    def _preprocess(self, text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def predict_sentiment(self, text):
        text = self._preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        prediction = self.config.id2label[ranking[0]].lower()
        encoded_prediction = self._get_encoding(prediction)

        return encoded_prediction
    
