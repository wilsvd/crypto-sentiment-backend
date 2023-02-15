import os
import praw

from praw import models
from dotenv import load_dotenv
import logging


load_dotenv()

USER_AGENT = os.getenv("REDDIT_USER_AGENT")

ONE_CLIENT_ID = os.getenv("REDDIT_WORKER_ONE_CLIENT_ID")
ONE_CLIENT_SECRET = os.getenv("REDDIT_WORKER_ONE_CLIENT_SECRET")
ONE_CLIENT_REFRESH_TOKEN = os.getenv("REDDIT_WORKER_ONE_CLIENT_REFRESH")

TWO_CLIENT_ID = os.getenv("REDDIT_WORKER_TWO_CLIENT_ID")
TWO_CLIENT_SECRET = os.getenv("REDDIT_WORKER_TWO_CLIENT_SECRET")
TWO_CLIENT_REFRESH_TOKEN = os.getenv("REDDIT_WORKER_TWO_CLIENT_REFRESH")

THREE_CLIENT_ID = os.getenv("REDDIT_WORKER_THREE_CLIENT_ID")
THREE_CLIENT_SECRET = os.getenv("REDDIT_WORKER_THREE_CLIENT_SECRET")
THREE_CLIENT_REFRESH_TOKEN = os.getenv("REDDIT_WORKER_THREE_CLIENT_REFRESH")

FOUR_CLIENT_ID = os.getenv("REDDIT_WORKER_FOUR_CLIENT_ID")
FOUR_CLIENT_SECRET = os.getenv("REDDIT_WORKER_FOUR_CLIENT_SECRET")
FOUR_CLIENT_REFRESH_TOKEN = os.getenv("REDDIT_WORKER_FOUR_CLIENT_REFRESH")


WORKER_ZERO = 0
WORKER_ONE = 1
WORKER_TWO = 2
WORKER_THREE = 3


class RedditAPI:
    def __init__(self) -> None:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
            print(f"Logger: {logger_name}")
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

    def single_instance(self):
        instance1 = self._setup_instance(
            ONE_CLIENT_ID, ONE_CLIENT_SECRET, ONE_CLIENT_REFRESH_TOKEN
        )

        # print(instance1.config._settings)
        return [instance1]

    def multi_acc_multi_instance(self):
        instance1 = self._setup_instance(
            ONE_CLIENT_ID, ONE_CLIENT_SECRET, ONE_CLIENT_REFRESH_TOKEN
        )
        instance2 = self._setup_instance(
            TWO_CLIENT_ID, TWO_CLIENT_SECRET, TWO_CLIENT_REFRESH_TOKEN
        )
        instance3 = self._setup_instance(
            THREE_CLIENT_ID, THREE_CLIENT_SECRET, THREE_CLIENT_REFRESH_TOKEN
        )
        instance4 = self._setup_instance(
            FOUR_CLIENT_ID, FOUR_CLIENT_SECRET, FOUR_CLIENT_REFRESH_TOKEN
        )

        return [instance1, instance2, instance3, instance4]

    def _setup_instance(self, client_id, client_secret, refresh_token):
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            redirect_uri="http://localhost:8080",
            user_agent=USER_AGENT,
        )
        return reddit


#
