from cmc_api import CoinMarketCapAPI

from pprint import pprint

# NOTE: 965 Is the upper limit. If I go higher than I get an Error
# TODO: Adapt the CMC API Setup to able to retrieve more than 965 cryptocurrencies.
CRYPTO_LIMIT = "100"


class CoinCollector:

    m_ids = []

    def __init__(self) -> None:
        self.cmc = CoinMarketCapAPI()
        self._set_coin_ids()

        # First in - First out.

    def _get_coin_ids(self):
        return self.m_ids

    def _set_coin_ids(self):
        map_info = self.cmc.get_Cryptocurrency_Map_Info(limit=CRYPTO_LIMIT)
        ids = []
        for item in map_info["data"]:
            ids.append(str(item["id"]))
        self.m_ids = ids

    def get_coin_subreddits(self):
        coin_ids = self._get_coin_ids()
        ids = ",".join(coin_ids)
        cmc_meta = self.cmc.get_Cryptocurrency_Meta_Info(ids)
        subreddits = self._clean_coin_data(ids=coin_ids, coin_data=cmc_meta["data"])
        return subreddits

    def _clean_coin_data(self, ids, coin_data):
        subreddits = []
        for id in ids:
            subredditName = coin_data[id]["subreddit"]
            if subredditName != "":
                subreddits.append(subredditName)

        return subreddits
