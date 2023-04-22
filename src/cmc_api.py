from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import os
from dotenv import load_dotenv

load_dotenv()

CRYPTO_API_KEY = os.getenv("CMC_CRYPTO_API_KEY")

BASE_URL = "https://pro-api.coinmarketcap.com"

# Extension urls
MAP_URL = "/v1/cryptocurrency/map"
META_URL = "/v2/cryptocurrency/info"


class CoinMarketCapAPI:
    """
    A wrapper class for the CoinMarketCap API.

    Attributes:
        session: A requests.Session object used to send requests to the API.

    Methods:
        __init__(self):
            Initializes the session object with the appropriate headers and API key.

        _get_dict(self, url: str, parameters: dict):
            Sends a GET request to the specified URL with the given parameters and returns the response as a dictionary.

        get_Cryptocurrency_Map_Info(self, status: str = "active", start: str = "1", limit: str = "1000", sort: str = "cmc_rank") -> dict:
            Fetches a mapping of all cryptocurrencies to unique CoinMarketCap ids.

        get_Cryptocurrency_Meta_Info(self, id: str) -> dict:
            Fetches all static metadata available for one or more cryptocurrencies. This information includes details like logo, description, official website URL, social links, and links to a cryptocurrency's technical documentation.
    """

    def __init__(self) -> None:
        """
        Initializes the session object with the appropriate headers and API key.

        Parameters:
            None

        Returns:
            None
        """

        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": CRYPTO_API_KEY,
        }
        self.session = Session()
        self.session.headers.update(headers)

    def _get_dict(self, url: str, parameters: dict) -> dict:
        """
        Sends a GET request to the specified URL with the given parameters and returns the response as a dictionary.

        Parameters:
            url (str): The URL to send the request to.
            parameters (dict): The parameters to include in the request.

        Returns:
            dict: The response as a dictionary.

        Raises:
            ConnectionError: If there was an issue connecting to the API.
        """

        response = self.session.get(url, params=parameters)

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError()

    def get_Cryptocurrency_Map_Info(
        self,
        status: str = "active",
        start: str = "1",
        limit: str = "1000",
        sort: str = "cmc_rank",
    ) -> dict:
        """
        Fetches a mapping of all cryptocurrencies to unique CoinMarketCap ids.

        Parameters:
            status (str): Specify whether only active or also inactive cryptocurrencies should be fetched. Default is "active".
            start (str): Offset the start (1-based index) of the paginated list of items to return. Default is "1".
            limit (str): Specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size. Default is "1000".
            sort (str): What field to sort the list of cryptocurrencies by. Default is "cmc_rank".

        Returns:
            dict: A dictionary containing the requested data.

        Raises:
            ConnectionError: If there was an issue connecting to the API.
        """
        parameters = {
            "listing_status": status,
            "start": start,
            "limit": limit,
            "sort": sort,
        }

        try:
            return self._get_dict(BASE_URL + MAP_URL, parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return {}

    def get_Cryptocurrency_Meta_Info(self, id: str) -> dict:
        """
        Fetches all static metadata available for one or more cryptocurrencies. This information includes details like logo,
        description, official website URL, social links, and links to a cryptocurrency's technical documentation.

        Parameters:
            id (str): One or more comma-separated CoinMarketCap cryptocurrency IDs. Example: "1,2".

        Returns:
            dict: A dictionary containing the requested data.

        Raises:
            ConnectionError: If there was an issue connecting to the API.
        """
        parameters = {
            "id": id,
        }
        try:
            return self._get_dict(BASE_URL + META_URL, parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return {}
