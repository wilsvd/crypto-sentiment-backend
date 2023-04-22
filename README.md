[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Sentiment Analysis on Cryptocurrency Reddit Posts

## Project Description

This project is a sentiment analysis tool that collects and analyzes Reddit posts from various cryptocurrency subreddits.

The data collection process involves retrieving the titles of Reddit posts from various cryptocurrency subreddits using the CoinMarketCap API and Python Reddit API Wrapper (PRAW). The post titles are then classified into Positive, Neutral or Negative sentiments using the "twitter-roberta-base-sentiment-latest" model on Hugging Face. These predictions are encoded into a numeric value to calculate the average sentiment of a subreddit. The sentiments and posts from each subreddit are stored on a Firebase Cloud Firestore database. The Cron scheduler is used to update the data every 12 hours.

This system will help users to make more informed decisions regarding their cryptocurrency investments because it will provide valuable insights into how the market and other investors feel about a cryptocurrency.

## Technology Stack

The following technologies were used in this project:

-   Python
-   CoinMarketCap (CMC) API
-   Python Reddit API Wrapper (PRAW)
-   Sentiment Analysis (Hugging Face model ["twitter-roberta-base-sentiment-latest"](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest))
-   Firebase Cloud Firestore
-   Google Compute Engine (GCE) for Deployment
-   Cronitor

## Setup Instructions

To set up this project on a local machine, follow these steps:

1. Clone the repository to your local machine.
2. Install [Poetry](https://python-poetry.org/docs/) to manage dependencies.
3. Run poetry install to install the necessary dependencies.
4. Activate the virtual environment
5. Obtain API keys for [CoinMarketCap](https://coinmarketcap.com/api/) and [Reddit](https://www.reddit.com/prefs/apps).
6. Create a Firebase project
7. Add Cloud Firestore to the project
8. Obtain the necessary Firebase Admin credentials.
9. Create a file named .env in the root directory of the project.
    - 4 PRAW Instances, and 4 Reddit Clients are used but this can be changed to any number.
    - In the .env file, set the necessary environment variables:

```py
CMC_CRYPTO_API_KEY = ""

REDDIT_USER_AGENT = ""

REDDIT_WORKER_ONE_CLIENT_ID = ""
REDDIT_WORKER_ONE_CLIENT_SECRET = ""
REDDIT_WORKER_ONE_CLIENT_REFRESH = ""

REDDIT_WORKER_TWO_CLIENT_ID = ""
REDDIT_WORKER_TWO_CLIENT_SECRET = ""
REDDIT_WORKER_TWO_CLIENT_REFRESH = ""

REDDIT_WORKER_THREE_CLIENT_ID = ""
REDDIT_WORKER_THREE_CLIENT_SECRET = ""
REDDIT_WORKER_THREE_CLIENT_REFRESH = ""

REDDIT_WORKER_FOUR_CLIENT_ID = ""
REDDIT_WORKER_FOUR_CLIENT_SECRET = ""
REDDIT_WORKER_FOUR_CLIENT_REFRESH = ""

FIREBASE_TYPE = ""
FIREBASE_PROJECT_ID = ""
FIREBASE_PRIVATE_KEY_ID = ""
FIREBASE_PRIVATE_KEY = ""
FIREBASE_CLIENT_EMAIL = ""
FIREBASE_CLIENT_ID = ""
FIREBASE_AUTH_URI = ""
FIREBASE_TOKEN_URI = ""
FIREBASE_AUTH_X509_CERT_URL = ""
FIREBASE_CLIENT_X509_CERT_URL = ""

```

## Usage

To use this project and consistenly collect data, follow these steps:

1. Run the script python src/scheduler.py to confirm that it is working.
2. If you want to use your own computer, you can skip steps 3 to 5.
3. Create an account with a cloud provider, such as Google Cloud.
4. Set up a virtual machine on the cloud provider's platform.
5. Install the necessary dependencies and configure the environment variables as specified in the Setup section.
6. Create a cron job to schedule the script to run on a consistent basis.
7. Use a monitoring tool such as Cronitor to monitor the cron job and receive alerts if it fails.

## Dependency Documentation

-   [CoinMarketCap (CMC) API](https://coinmarketcap.com/api/documentation/v1/)
-   [Python Reddit API Wrapper (PRAW)](https://praw.readthedocs.io/en/stable/)
-   [Firebase](https://firebase.google.com/docs/firestore)
-   [HuggingFace](https://huggingface.co/docs)

## License

This project is released under the [MIT License](LICENSE.md). Please see the license file for more information.
