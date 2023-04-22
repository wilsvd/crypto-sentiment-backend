import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from dotenv import load_dotenv

import os

load_dotenv()

# Details for Firebase admin account
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
    """
    A wrapper class for the Firebase Firestore database.

    Attributes:
        db: A Firebase Firestore database object.

    Methods:
        __init__(self):
            Initializes the Firestore database object with the appropriate credentials.

        add_historical_data(self, crypto: str, subreddit: str, data: dict):
            Adds historical data to the database.

        get_post(self, crypto: str, post_id: str)
            Finds a post document in the database.

        del_old_n_posts(self, batch, crypto: str)
            Deletes the oldest n posts from a specific cryptocurrency's database collection.

        get_n_oldest_posts(self, crypto: str, n: int)
            Gets the n oldest posts from the given cryptocurrency's collection.

        get_count(self, crypto: str) -> int
            Gets the count of posts in the given cryptocurrency's collection.

        get_total_sentiment(self, crypto: str)
            Calculates the total sentiment of a given cryptocurrency's database.

        batch_delete(self, batch, crypto: str, submission_id: int)
            Deletes a post with a given ID from the given cryptocurrency's collection in a batch.

        batch_write(self, batch, crypto: str, submission_id, data)
            Writes a batch of data to a specific cryptocurrency's database collection.

    """

    def __init__(self) -> None:
        """
        Initializes the Firestore database object with the appropriate credentials.

        Parameters:
            None

        Returns:
            None
        """

        cred = credentials.Certificate(SERVICE_ACCOUNT)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_historical_data(self, crypto: str, subreddit: str, data: dict):
        """
        Adds historical data to the database.

        Parameters:
            crypto (str): The cryptocurrency for which to add data.
            subreddit (str): The subreddit for which to add data.
            data (dict): The data to add to the database.

        Returns:
            None
        """

        crypto_doc = self.db.collection("sentiments").document(crypto)

        crypto_doc.set(
            {
                "crypto": crypto,
                "subreddit": subreddit,
                "latest_sentiment": data["sub_sentiment"],
            }
        )

        col_ref = (
            self.db.collection("sentiments").document(crypto).collection("history")
        )

        col_ref.add(data)

    def get_post(self, crypto: str, post_id: str):
        """
        Finds a post document in the database.

        Parameters:
            crypto (str): The cryptocurrency for which to check for the post.
            post_id (str): The post id to check.

        Returns:
            Firestore Document: The post document object.
        """

        doc_ref = (
            self.db.collection("sentiments")
            .document(crypto)
            .collection("posts")
            .document(post_id)
        )
        doc = doc_ref.get()

        return doc

    def del_old_n_posts(self, batch, crypto: str):
        """
        Deletes the oldest n posts from a specific cryptocurrency's database collection.

        Parameters:
            batch: A batch of documents to delete.
            crypto (str): The cryptocurrency whose collection is to be deleted.

        Returns:
            None
        """
        existing_post_counts = self.get_count(crypto)
        if existing_post_counts > TOTAL_POSTS:
            n_posts_to_remove = existing_post_counts - TOTAL_POSTS
            submissions = self.get_n_oldest_posts(crypto, n_posts_to_remove)

            # Iterate through submissions to the deleted adding it to deletion batch
            for submission in submissions:
                document_id = submission.id
                self.batch_delete(batch, crypto, document_id)
            batch.commit()
        else:
            print("Hey you don't have enough")

    def get_n_oldest_posts(self, crypto: str, n: int):
        """
        Gets the n oldest posts from the given cryptocurrency's collection.

        Parameters:
            crypto (str): The cryptocurrency whose collection is to be checked.
            n (int): The number of oldest posts to get.

        Returns:
            A QuerySnapshot object containing the n oldest posts from the given cryptocurrency's collection.
        """
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        res = col_ref.order_by("datetime").limit(n)

        return res.get()

    def get_count(self, crypto: str) -> int:
        """
        Gets the count of posts in the given cryptocurrency's collection.

        Parameters:
            crypto (str): The cryptocurrency whose collection is to be checked.

        Returns:
            The count of posts in the given cryptocurrency's collection.
        """

        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        query = col_ref.count()
        count = getattr(query.get()[0][0], "value")
        return count

    def get_total_sentiment(self, crypto: str):
        """
        Calculates the total sentiment of a given cryptocurrency's database.

        Parameters:
            crypto (str): The cryptocurrency for which to calculate the sentiment.

        Returns:
            int: The total sentiment value.
        """
        col_ref = self.db.collection("sentiments").document(crypto).collection("posts")
        posQuery = col_ref.where("sentiment", "==", 1).count().get()
        negQuery = col_ref.where("sentiment", "==", -1).count().get()
        posNum = getattr(posQuery[0][0], "value")
        negNum = getattr(negQuery[0][0], "value")

        return posNum - negNum

    def batch_delete(self, batch, crypto: str, submission_id: int):
        """
        Deletes a post with a given ID from the given cryptocurrency's collection in a batch.

        Parameters:
            batch: A Firestore batch object.
            crypto (str): The cryptocurrency whose collection is to be deleted.
            submission_id (int): The ID of the post to be deleted.

        Returns:
            None
        """

        sub_ref = (
            self.db.collection("sentiments")
            .document(crypto)
            .collection("posts")
            .document(submission_id)
        )
        batch.delete(sub_ref)

    def batch_write(self, batch, crypto: str, submission_id, data):
        """
        Writes a batch of data to a specific cryptocurrency's database collection.

        Parameters:
            batch: The batch of data to be written to the database.
            crypto (str): The cryptocurrency for which to write the batch of data.
            submission_id: The ID of the submission to be written to the database.
            data: The data to be written to the database.

        Returns:
            None
        """
        sub_ref = (
            self.db.collection("sentiments")
            .document(crypto)
            .collection("posts")
            .document(submission_id)
        )
        (batch.set(sub_ref, data))
