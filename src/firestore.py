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

TOTAL_POSTS = 100
DESCENDING = firestore.Query.DESCENDING


class FirestoreDatabase:
    def __init__(self) -> None:
        cred = credentials.Certificate(SERVICE_ACCOUNT)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        print("SETup")

    def add_historical_data(self, crypto: str, data: dict):
        col_ref = (
            self.db.collection("sentiments").document(crypto).collection("history")
        )
        col_ref.add(data)

    def get_post_data(self, crypto: str):
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        collection = col_ref.get()
        return collection

    def post_data_exists(self, crypto: str, post_id: str):
        doc_ref = (
            self.db.collection("sentiments")
            .document(crypto)
            .collection("posts")
            .document(post_id)
        )
        doc = doc_ref.get()

        return doc

    def add_post_data(self, crypto: str, submission_id: str, data: dict):
        # Store only 100 posts for a cryptocurrency
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        count = self.get_count(crypto)
        if count > TOTAL_POSTS:
            self.del_old_post_submission(crypto)
        else:
            col_ref.document(submission_id).set(data)

    def del_old_n_posts(self, batch, crypto: str):
        existing_post_counts = self.get_count(crypto)
        print(existing_post_counts)
        if existing_post_counts > TOTAL_POSTS:
            n_posts_to_remove = existing_post_counts - TOTAL_POSTS
            submissions = self.get_n_oldest_posts(crypto, n_posts_to_remove)

            for submission in submissions:
                document_id = submission.id
                self.batch_delete(batch, crypto, document_id)
            print("Write")
            batch.commit()
        else:
            print("Hey you don't have enough")

    def get_n_oldest_posts(self, crypto: str, n: int):
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        res = col_ref.order_by("datetime").limit(n)

        return res.get()

    def del_old_post_submission(self, crypto: str):
        submission_id = self.get_oldest_post_id(crypto)
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")

        col_ref.document(submission_id).delete()

    def get_oldest_post_id(self, crypto: str):
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        res = col_ref.order_by("datetime").limit(1)
        return res.get()[0].id

    def get_count(self, crypto: str):
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        query = col_ref.count()
        count = getattr(query.get()[0][0], "value")
        return count

    def get_total_sentiment(self, crypto: str):
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        posQuery = col_ref.where("sentiment", "==", 1).count().get()
        negQuery = col_ref.where("sentiment", "==", -1).count().get()
        posNum = getattr(posQuery[0][0], "value")
        negNum = getattr(negQuery[0][0], "value")

        return posNum - negNum

    def batch_delete(self, batch, crypto: str, submission_id: int):
        sub_ref = (
            self.db.collection("sentiments")
            .document(crypto)
            .collection("posts")
            .document(submission_id)
        )
        batch.delete(sub_ref)

    def batch_write(self, batch, crypto: str, submission_id, data):
        # print("Entering")
        sub_ref = (
            self.db.collection("sentiments")
            .document(crypto)
            .collection("posts")
            .document(submission_id)
        )
        # print("Hi")
        (batch.set(sub_ref, data))


firedb = FirestoreDatabase()
now_datetime = datetime.now()
print(now_datetime)


firedb.get_count("Crypto_com")
# batch = firedb.db.batch()
# print("Starting")

# for i in range(100):
#     post_data = {
#         "datetime": now_datetime,
#         "title": "good stuff",
#         "sentiment": 0.7,
#     }
#     firedb.batch_write(batch, "Crypto_com", f"submission{i}", post_data)
# batch.commit()
# print("Deleting old posts")
# firedb.del_old_n_posts(batch, "Crypto_com")
# batch.commit()
# firedb.get_count("Crypto_com")
# print("Ending")
