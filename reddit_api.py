import os
import praw
from dotenv import load_dotenv
import logging


load_dotenv()

USER_AGENT = os.getenv("REDDIT_USER_AGENT")

WORKER_ZERO = 0
WORKER_ONE = 1
WORKER_TWO = 2
WORKER_THREE = 3

class RedditAPI():


    def __init__(self) -> None:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
            print(f"Logger: {logger_name}")
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

    def connect_to_reddit(self, worker):

        if worker == WORKER_ZERO:
            print("worker0")
            reddit = praw.Reddit(client_id=os.getenv("REDDIT_WORKER_ONE_CLIENT_ID"),
                        client_secret=os.getenv("REDDIT_WORKER_ONE_CLIENT_SECRET"),
                        user_agent=USER_AGENT,
                        ratelimit_seconds=600
                        )
        if worker == WORKER_ONE:
            print("worker1")
            reddit = praw.Reddit(client_id=os.getenv("REDDIT_WORKER_TWO_CLIENT_ID"),
                        client_secret=os.getenv("REDDIT_WORKER_TWO_CLIENT_SECRET"),
                        user_agent=USER_AGENT,
                        ratelimit_seconds=600
                        )
        if worker == WORKER_TWO:
            print("worker2")
            reddit = praw.Reddit(client_id=os.getenv("REDDIT_WORKER_THREE_CLIENT_ID"),
                        client_secret=os.getenv("REDDIT_WORKER_THREE_CLIENT_SECRET"),
                        user_agent=USER_AGENT,
                        ratelimit_seconds=600
                        )
        if worker == WORKER_THREE:
            print("worker3")
            reddit = praw.Reddit(client_id=os.getenv("REDDIT_WORKER_FOUR_CLIENT_ID"),
                        client_secret=os.getenv("REDDIT_WORKER_FOUR_CLIENT_SECRET"),
                        user_agent=USER_AGENT,
                        ratelimit_seconds=600
                        )
        
        
        

        return reddit

# 

