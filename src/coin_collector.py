from cmc_api import CoinMarketCapAPI

# NOTE: 965 Is the upper limit. If I go higher than I get an Error.
# Cryptocurrency limit is set at 150 due to limitations with GCP.
CRYPTO_LIMIT = "150"


class CoinCollector:
    """
    A class to collect information on available subreddits for each cryptocurrency.

    Attributes:
        m_ids (list): A list of cryptocurrency ids used to retrieve subreddit information.

    Methods:
        __init__(self):
            Initializes a CoinMarketCapAPI object and sets the m_ids attribute by calling the _set_coin_ids method.

        _get_coin_ids(self) -> list:
            Returns the list of cryptocurrency ids.

        _set_coin_ids(self):
            Uses CoinMarketCapAPI object to retrieve a mapping of all cryptocurrencies to unique CoinMarketCap ids.
            Sets the m_ids attribute to a list of cryptocurrency ids.

        _clean_data(self, ids: list, coin_data: dict) -> list:
            Takes in a list of cryptocurrency ids and a dictionary containing metadata for the corresponding cryptocurrencies.
            Returns a cleaned list of cryptocurrency names and subreddit names.

        get_coin_subreddits(self) -> list:
            Uses CoinMarketCapAPI object to retrieve metadata for cryptocurrencies specified by m_ids attribute.
            Cleans and returns a list of cryptocurrency names and corresponding subreddit names.
    """

    m_ids = []

    def __init__(self) -> None:
        """
        Initializes a CoinMarketCapAPI object and sets the m_ids attribute by calling the _set_coin_ids method.

        Parameters:
            None

        Returns:
            None
        """
        self.cmc = CoinMarketCapAPI()
        self._set_coin_ids()

    def _get_coin_ids(self) -> list:
        """
        Returns the list of cryptocurrency ids.

        Parameters:
            None

        Returns:
            list: A list of cryptocurrency ids.
        """
        return self.m_ids

    def _set_coin_ids(self):
        """
        Uses CoinMarketCapAPI object to retrieve a mapping of all cryptocurrencies to unique CoinMarketCap ids.
        Sets the m_ids attribute to a list of cryptocurrency ids.

        Parameters:
            None

        Returns:
            None
        """
        map_info = self.cmc.get_Cryptocurrency_Map_Info(limit=CRYPTO_LIMIT)
        ids = []
        for item in map_info["data"]:
            ids.append(str(item["id"]))
        self.m_ids = ids

    def _clean_data(self, ids: list, coin_data: dict) -> list:
        """
        Takes in a list of cryptocurrency ids and a dictionary containing metadata for the corresponding cryptocurrencies.
        Returns a cleaned list of cryptocurrency names and subreddit names.

        Parameters:
            ids (list): A list of cryptocurrency ids.
            coin_data (dict): A dictionary containing metadata for the corresponding cryptocurrencies.

        Returns:
            list: A list of cryptocurrency names and corresponding subreddit names.
        """
        subreddits = []
        for id in ids:  # Iterate through all the ids
            cryptoName: str = coin_data[id]["name"]
            subredditName: str = coin_data[id]["subreddit"]
            if subredditName != "":  # Check if a subreddit exists
                cleanName = "".join(
                    (
                        filter(  # Clean name of cryptocurrency so Firestore accepts storage
                            lambda i: i not in ["$", "#", "[", "]", "/", "."],
                            subredditName,
                        )
                    )
                )
                subreddits.append([cryptoName, cleanName])

        return subreddits

    def get_coin_subreddits(self) -> list:
        """
        Retrieves a list of subreddits associated with each cryptocurrency in the CoinMarketCap API up to the specified limit.

        Parameters:
            None

        Returns:
            list: A list of subreddits associated with each cryptocurrency. Each element in the list is a list with two elements: the name of the cryptocurrency and the name of its subreddit.

        Raises:
            ConnectionError: If there was an issue connecting to the API.
        """
        coin_ids = self._get_coin_ids()
        ids = ",".join(
            coin_ids
        )  # Convert list into a comma separated string to be accepted by CMC API
        cmc_meta = self.cmc.get_Cryptocurrency_Meta_Info(ids)
        subreddits = self._clean_data(ids=coin_ids, coin_data=cmc_meta["data"])
        return subreddits
