import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
}


class FirebaseDatabase:
    def __init__(self) -> None:
        cred = credentials.Certificate(SERVICE_ACCOUNT)
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")},
        )
        self.ref = db.reference("/")

    def set_data(self, data: list):
        self.ref.set({"data": data})
