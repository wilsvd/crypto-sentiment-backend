import os
import praw

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
    """
    A wrapper class for the PRAW Reddit API.

    Attributes:
        None

    Methods:
        __init__(self):
            Initializes the logging configuration for the PRAW library.

        multi_acc_multi_instance(self):
            Creates and returns multiple authenticated PRAW Reddit instances for different Reddit accounts.

        _setup_instance(self, client_id: str, client_secret: str, refresh_token: str) -> praw.Reddit:
            Sets up an authenticated PRAW Reddit instance using the provided client_id, client_secret and refresh_token.

    """

    def __init__(self) -> None:
        """
        Initializes the logging configuration for the PRAW library.

        Parameters:
            None

        Returns:
            None
        """
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
            print(
                f"Logger: {logger_name}"
            )  # Prints logs so that output gets directed to cronitors log file
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

    def multi_acc_multi_instance(self) -> list[praw.Reddit]:
        """
        Creates and returns multiple authenticated PRAW Reddit instances for different Reddit clients.

        Parameters:
            None

        Returns:
            list: A list of authenticated PRAW Reddit instances.

        Raises:
            None
        """
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

    def _setup_instance(self, client_id, client_secret, refresh_token) -> praw.Reddit:
        """
        Initializes and returns a Reddit instance with the provided credentials.

        Parameters:
            client_id (str): The client ID of the Reddit app.
            client_secret (str): The client secret of the Reddit app.
            refresh_token (str): The refresh token of the Reddit app.

        Returns:
            praw.Reddit: A Reddit instance authenticated with the provided credentials.

        Raises:
            praw.exceptions.PRAWException: If there was an issue creating the Reddit instance.
        """
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            redirect_uri="http://localhost:8080",
            user_agent=USER_AGENT,
        )
        return reddit


#
