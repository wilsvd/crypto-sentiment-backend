import os
import praw
from dotenv import load_dotenv
import logging

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

class RedditAPI():

    def connect_to_reddit(self):
        reddit = praw.Reddit(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        user_agent=USER_AGENT,
                        ratelimit_seconds=600
                        )
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

        return reddit

# 

