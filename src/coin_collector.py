from cmc_api import CoinMarketCapAPI

# NOTE: 965 Is the upper limit. If I go higher than I get an Error
# TODO: Adapt the CMC API Setup to able to
# retrieve more than 965 cryptocurrencies.
CRYPTO_LIMIT = "200"


class CoinCollector:

    m_ids = []

    def __init__(self) -> None:
        self.cmc = CoinMarketCapAPI()
        self._set_coin_ids()

    def _get_coin_ids(self):
        return self.m_ids

    def _set_coin_ids(self):
        map_info = self.cmc.get_Cryptocurrency_Map_Info(limit=CRYPTO_LIMIT)
        ids = []
        for item in map_info["data"]:
            ids.append(str(item["id"]))
        self.m_ids = ids

    def _clean_data(self, ids, coin_data):
        subreddits = []
        for id in ids:
            cryptoName: str = coin_data[id]["name"]
            subredditName: str = coin_data[id]["subreddit"]
            if subredditName != "":
                cleanName = "".join(
                    (
                        filter(
                            lambda i: i not in ["$", "#", "[", "]", "/", "."],
                            subredditName,
                        )
                    )
                )
                subreddits.append([cryptoName, cleanName])

        return subreddits

    def get_coin_subreddits(self):
        coin_ids = self._get_coin_ids()
        ids = ",".join(coin_ids)
        cmc_meta = self.cmc.get_Cryptocurrency_Meta_Info(ids)
        subreddits = self._clean_data(ids=coin_ids, coin_data=cmc_meta["data"])
        return subreddits
