from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
from test_models import extract_data
import evaluate
import sklearn
from pprint import pprint
import pandas as pd
from joblib import dump, load

model_name = "ElKulako/cryptobert"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3)
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding = 'max_length')

data = extract_data()
num_correct = 0

# Dataset Labels include:
# Negative, Bearish
# Neutral, Neutral
# Positive, Bullish

# Cryptobert labels data as:
# Bearish, Neutral, Bullish

# Encode the data into ints so it can be evaluated more easily.
def get_rating(ratings):
    if "bullish" in ratings:
        return 1
    elif "neutral" in ratings:
        return 0
    else:
        return -1

references = []
predictions = []
for post_data in data:
    text = post_data[0]
    ratings = post_data[1]
    preds = pipe(text)
    prediction = preds[0]['label'].lower()
    predictions.append(get_rating(prediction))
    references.append(get_rating(ratings))

data_tuples = list(zip(predictions, references))
df = pd.DataFrame(data_tuples, columns=['Predict Label','Ground Label'])
dump(df, "cryptobert_comparison.joblib")


