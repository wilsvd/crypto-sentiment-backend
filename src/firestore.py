from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
}


DESCENDING = firestore.Query.DESCENDING


class FirestoreDatabase:
    def __init__(self) -> None:
        cred = credentials.Certificate(SERVICE_ACCOUNT)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.sentiment_ref = db.collection("sentiments")

    def add_historical_data(self, crypto: str, data: dict):
        doc_ref = self.sentiment_ref.document(crypto).collection("history")
        doc_ref.add(data)

    def add_post_data(self, crypto: str, submission_id: str, data: dict):
        # Store only 100 posts for a cryptocurrency
        doc_ref = self.sentiment_ref.document(crypto).collection("posts")
        count = self.get_count(crypto)
        if count > 100:
            self.del_old_post_submission(crypto)
        else:
            doc_ref.document(submission_id).set(data)

    def del_old_post_submission(self, crypto: str):
        submission_id = self.get_oldest_post_id(crypto)
        doc_ref = self.sentiment_ref.document(crypto).collection("posts")

        doc_ref.document(submission_id).delete()

    def get_count(self, crypto: str):
        doc_ref = self.sentiment_ref.document(crypto).collection("posts")
        query = doc_ref.count()
        count = getattr(query.get()[0][0], "value")
        return count

    def get_oldest_post_id(self, crypto: str):
        doc_ref = self.sentiment_ref.document(crypto).collection("posts")
        res = doc_ref.order_by("date_added").limit(1)
        return res.get()[0].id

    # def get_latest_date(self, crypto: str):
    #     doc_ref = self.sentiment_ref.document(crypto).collection("history")

    #     res = doc_ref.order_by("time", direction=DESCENDING).limit(1)
    #     for items in res.get():
    #         print(items.to_dict())


firedb = FirestoreDatabase()


for i in range(100):
    now_time = datetime.now()
    sentiment = (i % 2) - 1

    historical_data = {"time": now_time, "sentiment": sentiment}
    post_data = {
        "date_added": now_time,
        "title": f"Some text with number: {i}",
        "sentiment": sentiment,
    }
    submission_id = f"submission{i}"
    firedb.add_historical_data("ethereum", historical_data)
    firedb.add_post_data("ethereum", submission_id, post_data)

    # time.sleep(0.5)
