from joblib import load
import pandas as pd
import sklearn # Need import as part of evaluate.
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt

class ScoreManager():

    def __init__(self) -> None:
        pass
    
    def plot_confusion_matrix(self, name, actual_data, predicted_data):

        ConfusionMatrixDisplay.from_predictions(actual_data, predicted_data, display_labels=np.unique(actual_data))
        plt.title(name)
        plt.show()

    def cryptobert_score(self):
        df : pd.DataFrame
        df = load("cryptobert_comparison.joblib")
        predictions = df['Predict Label'].to_list()
        references = df['Ground Label'].to_list()

        matrix = classification_report(references, predictions, labels=np.unique(references))
        print(matrix)
        self.plot_confusion_matrix("cryptobert", references, predictions)
        
    def autotrain_NLU_crypto_score(self):
        df : pd.DataFrame
        df = load("autotrain_nlu_crypto_comparison.joblib")
        predictions = df['Predict Label'].to_list()
        references = df['Ground Label'].to_list()

        matrix = classification_report(references, predictions, labels=np.unique(references))
        print(matrix)
        self.plot_confusion_matrix("autotrain_nlu_crypto", references, predictions)

    def twitter_roberta_base_latest_score(self):
        df : pd.DataFrame
        df = load("twitter_roberta_comparison.joblib")
        predictions = df['Predict Label'].to_list()
        references = df['Ground Label'].to_list()

        matrix = classification_report(references, predictions, labels=np.unique(references))
        print(matrix)
        self.plot_confusion_matrix("twitter_roberta", references, predictions)

scores = ScoreManager()
print("cryptobert_score")
scores.cryptobert_score()
print("autotrain_NLU_crypto_score")
scores.autotrain_NLU_crypto_score()
print("twitter_roberta_base_latest_score")
scores.twitter_roberta_base_latest_score()
