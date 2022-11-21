from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import os
from dotenv import load_dotenv

load_dotenv()

CRYPTO_API_KEY = os.getenv("CMC_CRYPTO_API_KEY")

BASE_URL = 'https://pro-api.coinmarketcap.com'

# Extension urls
MAP_URL = "/v1/cryptocurrency/map"
META_URL = "/v2/cryptocurrency/info"
LISTING_URL = "/v1/cryptocurrency/listings/latest" # Ignore these ones for now
QUOTE_URL = "/v2/cryptocurrency/quotes/latest" # Ignore these ones for now
AIRDROPS = "/v1/cryptocurrency/airdrops" # Ignore these ones for now


class CoinMarketCapAPI():
    
    def __init__(self) -> None:
        headers = {
        'X-CMC_PRO_API_KEY': CRYPTO_API_KEY,
        }
        self.session = Session()
        self.session.headers.update(headers)
    
    def _get_dict(self, url : str, parameters):
            response = self.session.get(url, params=parameters)
            print(response)
            return json.loads(response.text)

    def get_Cryptocurrency_Map_Info(self, status: str ="active", start: str ="1", limit: str ="1000", sort: str = "cmc_rank") -> dict:
        parameters = {
        'listing_status': status,
        'start': start,
        'limit': limit,
        'sort': sort
        }

        try:
            return self._get_dict(BASE_URL + MAP_URL, parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def get_Cryptocurrency_Meta_Info(self, id: str) -> dict:
        parameters = {
        'id': id,
        }
        try:
            return self._get_dict(BASE_URL + META_URL, parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
