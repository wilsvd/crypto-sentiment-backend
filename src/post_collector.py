from reddit_api import RedditAPI
from classifier import SentimentClassifier
from prawcore.exceptions import NotFound
from firestore import FirestoreDatabase
from datetime import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# TYPES:
# historical_data = {"time": datetime, "sentiment": float}
# post_data = {
#     "date_added": datimetime,
#     "title": str",
#     "sentiment": float,
# }


class SentimentCollector:
    """
    A class that collects sentiment data for cryptocurrencies from Reddit and stores it in a Firestore database.

    Attributes:
        r_api: A RedditAPI object that provides methods for interfacing with the Reddit API.
        classifier: A SentimentClassifier object that provides methods for classifying the sentiment of text data.
        firedb: A FirestoreDatabase object that provides methods for interfacing with the Firestore database.

    Methods:
        __init__(self):
            Initializes the SentimentCollector object with a RedditAPI object, a SentimentClassifier object, and a FirestoreDatabase object.

        _find_partition_sentiment(self, partition: list, reddit_helper):
            Fetches the submission data for a given partition of cryptocurrency-subreddit pairs and stores the sentiment data in the Firestore database.

        _get_submission(self, reddit_helper, crypto_name: str, subreddit: str):
            Fetches the submission data for a given cryptocurrency-subreddit pair and stores the sentiment data in the Firestore database.

        _store_crypto_data(self, crypto_name: str, subreddit: str, new_posts: dict):
            Stores the sentiment data for a given set of posts in the Firestore database.

        collect_sentiment_data(self, crypto_subreddits: list, num_partitions: int):
            Collects sentiment data for a list of cryptocurrency-subreddit pairs and stores the data in the Firestore database. The data collection is divided into a number of partitions specified by the user.
    """

    m_ids = []

    def __init__(self) -> None:
        """
        Initializes the SentimentCollector object with a RedditAPI object, a SentimentClassifier object, and a FirestoreDatabase object.

        Parameters:
            None

        Returns:
            None
        """
        self.r_api = RedditAPI()
        self.classifier = SentimentClassifier()
        self.firedb = FirestoreDatabase()

    def _find_partition_sentiment(self, partition, reddit_helper):
        """
        Fetches the submission data for a given partition of cryptocurrency-subreddit pairs and stores the sentiment data in the Firestore database.

        Parameters:
            partition (list): A list of cryptocurrency-subreddit pairs.
            reddit_helper: A PRAW Reddit object that is authenticated to access the Reddit API.

        Returns:
            None
        """
        for crypto_info in partition:
            name = crypto_info[0]
            subreddit = crypto_info[1]
            self._get_submission(reddit_helper, name, subreddit)

    # TODO: Optimise _get_submission function.
    def _get_submission(self, reddit_helper, crypto_name: str, subreddit: str):
        """
        Fetches the submission data for a given cryptocurrency-subreddit pair and stores the sentiment data in the Firestore database.

        Parameters:
            reddit_helper: A PRAW Reddit object that is authenticated to access the Reddit API.
            crypto_name (str): The name of the cryptocurrency.
            subreddit (str): The name of the subreddit to fetch data from.

        Returns:
            None
        """
        # NOTE: PRAW is fetching 100 submissions in one request.
        try:
            new_posts = {}
            # Get all the posts from hot
            posts = reddit_helper.subreddit(subreddit).hot()
            for post in posts:
                data = self.firedb.get_post(subreddit, post.id)
                # If posts exists in Firestore then we can ignore fetching it and processing it
                if data.exists:
                    continue

                # If post is not a stickied post then its a valid post
                if not post.stickied:
                    new_posts[post.id] = [
                        post.title,
                        datetime.fromtimestamp(post.created_utc),
                    ]

            print(reddit_helper.auth.limits)

            self._store_crypto_data(crypto_name, subreddit, new_posts)
        except NotFound:
            print("Subreddit does not exist")
            return None
        except ConnectionError:
            print("Could not connect to Reddit")
            return None

    def _store_crypto_data(self, crypto_name: str, subreddit: str, new_posts: dict):
        """
        Store the sentiment data for new crypto posts in Firestore, and update overall sentiment data.

        Parameters:
            crypto_name (str): The name of the cryptocurrency being analyzed.
            subreddit (str): The subreddit being searched for new crypto posts.
            new_posts (dict): A dictionary containing new posts data, with the submission ID as the key, and a list of post title and date as the value.

        Returns:
            None

        Raises:
            None
        """
        try:
            # Calculate new sentiment based on new crypto posts
            new_sent_preds = {}
            if len(new_posts) > 0:
                post_ids = list(new_posts.keys())
                post_data = list(new_posts.values())
                post_titles = [item[0] for item in post_data]
                new_sent_preds = self.classifier.predict_sentiment(
                    post_ids, post_titles
                )
            # Store new posts data in Firestore
            batch = self.firedb.db.batch()
            for post_id in new_posts.keys():
                # NOTE: posts and new_sent_preds share the same keys
                # since the keys are the submission ids.
                title = new_posts[post_id][0]
                date = new_posts[post_id][1]
                sentiment = new_sent_preds[post_id]

                post_data = {
                    "datetime": date,
                    "title": title,
                    "sentiment": sentiment,
                }
                self.firedb.batch_write(batch, crypto_name, post_id, post_data)
            batch.commit()
            # Make sure that only 100 posts are being stored at a time
            self.firedb.del_old_n_posts(batch, crypto_name)

            # Calculate new overall sentiment for crypto
            total_sentiment = self.firedb.get_total_sentiment(crypto_name)
            total_posts = self.firedb.get_count(crypto_name)
            now_datetime = datetime.now()

            # Store historical data in Firestore
            self.firedb.add_historical_data(
                crypto_name,
                subreddit,
                {
                    "datetime": now_datetime,
                    "sub_sentiment": round(total_sentiment / total_posts, 2),
                },
            )
        except:
            print("Some error occurred")
            return None

        # Get the new total sentiment data for the subreddit

    def find_crypto_sentiments(self, total_cryptocurrencies: list):
        """
        Find and store sentiment data for each cryptocurrency subreddit in parallel.

        Parameters:
            total_cryptocurrencies (list): A list of cryptocurrency names to be analyzed.

        Returns:
            None

        Raises:
            None
        """
        # Partition total_cryptocurrencies as evenly as possible
        partitions = np.array_split(total_cryptocurrencies, 4)

        # Connect to the multiple Reddit clients using multiple PRAW accounts
        reddit_helpers = self.r_api.multi_acc_multi_instance()

        # Number of workers must be equivalent to number of partitions
        with ThreadPoolExecutor(max_workers=4) as executor:
            for worker, partition in enumerate(partitions):
                reddit_helper = reddit_helpers[worker]
                executor.submit(
                    self._find_partition_sentiment,
                    partition,
                    reddit_helper,
                )
