from cmc_api import CoinMarketCapAPI

CRYPTO_LIMIT = 100

class CoinCollector():
    
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
        for item in map_info['data']:
            ids.append(str(item['id']))
        self.m_ids = ids

    def _get_coin_subreddits(self):
        coin_ids = self._get_coin_ids()
        ids = ",".join(coin_ids)
        cmc_meta = self.cmc.get_Cryptocurrency_Meta_Info(ids)
        subreddits = self._clean_coin_data(ids=coin_ids, coin_data=cmc_meta['data'])
        return subreddits
    
    def _clean_coin_data(self, ids, coin_data):
        subreddits = []
        for id in ids:
            subredditName = coin_data[id]['subreddit']
            if subredditName != '' or subredditName != "":
                subreddits.append(subredditName)
            
        return subreddits

# Top 10

