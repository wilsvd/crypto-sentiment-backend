from fastapi import FastAPI, Response
import json
from fastapi.middleware.cors import CORSMiddleware

SENTIMENTS = "./sentiment/sentiment_data.json"


app = FastAPI()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open(SENTIMENTS) as json_file:
    data : dict = json.load(json_file) 

@app.get("/")
def get_legacy_data():
    return data