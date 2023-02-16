from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from test_models import extract_data
import pandas as pd
from joblib import dump, load

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

data = extract_data()


def get_rating(ratings):
    if "positive" in ratings:
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
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]

    prediction = config.id2label[ranking[0]].lower()
    predictions.append(get_rating(prediction))
    references.append(get_rating(ratings))

data_tuples = list(zip(predictions, references))
df = pd.DataFrame(data_tuples, columns=["Predict Label", "Ground Label"])
dump(df, "./test_models/joblibs/twitter_roberta_comparison.joblib")
