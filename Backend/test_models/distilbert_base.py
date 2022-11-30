
# IT IS NOT A FAIR COMPARISON FOR DISTILBERT_BASE. THIS IS BECAUSE DISTILBERT ONLY HAS TWO LABELS POSITIVE AND NEGATIVE.
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from test_models import extract_data
import pandas as pd
from joblib import dump
# Disregard this model because it only takes into accounts two labels.
# I was planning on using this model. However, when going through the dataset there are some statements which simply are impossible
# to give a negative or positive score towards.
# For example, one of the inputs in the dataset is one word: "Bitcoin". There is no way of stating that is a positive or negative statement.

MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(MODEL)
model = DistilBertForSequenceClassification.from_pretrained(MODEL)

data = extract_data()

# Encoding for positive and negative
def get_rating(ratings):
    if "positive" in ratings:
        return 1
    elif "negative" in ratings:
        return -1

references = []
predictions = []
for post_data in data:
    text = post_data[0]
    ratings = post_data[1]
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()

    prediction = model.config.id2label[predicted_class_id].lower()

    predictions.append(get_rating(prediction))
    references.append(get_rating(ratings))

data_tuples = list(zip(predictions, references))
df = pd.DataFrame(data_tuples, columns=['Predict Label','Ground Label'])
dump(df, "./test_models/joblibs/distilbert_comparison.joblib")

print(df.head(10))