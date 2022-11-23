from transformers import AutoModelForSequenceClassification, AutoTokenizer
from test_models import extract_data
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from pprint import pprint

MODEL =  "zainalq7/autotrain-NLU_crypto_sentiment_analysis-754123133"
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)

data = extract_data()
num_correct = 0

for post_data in data:
    text = post_data[0]
    ratings = post_data[1]
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    scores = outputs[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    result = config.id2label[ranking[0]]
    if result.lower() in ratings:
        num_correct += 1

print(num_correct)