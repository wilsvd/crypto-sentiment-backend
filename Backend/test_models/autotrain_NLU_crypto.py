from transformers import AutoModelForSequenceClassification, AutoTokenizer
from test_models import extract_data
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from pprint import pprint
from joblib import dump
import pandas as pd

MODEL =  "zainalq7/autotrain-NLU_crypto_sentiment_analysis-754123133"
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)

def get_rating(ratings):
    if "positive" in ratings:
        return 1
    elif "neutral" in ratings:
        return 0
    else:
        return -1

data = extract_data()

references = []
predictions = []
for post_data in data:
    text = post_data[0]
    ratings = post_data[1]
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    scores = outputs[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    prediction = config.id2label[ranking[0]].lower()
    
    if prediction == "neutral":
        print("YES")
        
    predictions.append(get_rating(prediction))
    references.append(get_rating(ratings))
    
data_tuples = list(zip(predictions, references))
df = pd.DataFrame(data_tuples, columns=['Predict Label','Ground Label'])
dump(df, "autotrain_nlu_crypto_comparison.joblib")
