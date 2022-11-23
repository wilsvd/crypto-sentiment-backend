# REQUIRES THAT I FINE TUNE IT ON CRYPTO_CURRENCY DATA
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from test_models import extract_data

MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(MODEL)
model = DistilBertForSequenceClassification.from_pretrained(MODEL)

data = extract_data()
num_correct = 0

for post_data in data:
    text = post_data[0]
    ratings = post_data[1]
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    result = model.config.id2label[predicted_class_id]
    if result.lower() in ratings:
        num_correct += 1

print(num_correct)
