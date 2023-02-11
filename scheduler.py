from sentiment_collector import SentimentCollector
from coin_collectors import CoinCollector

import json
import time

import os

dir_path = os.path.dirname(os.path.abspath(__file__))

print(dir_path)
sentiment_path = os.path.join(dir_path, "sentiment/sentiment_data.json")
print(sentiment_path)

data = SentimentCollector()
coins = CoinCollector()

subreddits = coins.get_coin_subreddits()

# SUBREDDITS = [
#     "bitcoin",
#     "ethereum",
#     "bnbchainofficial",
#     "ripple",
#     "cardano",
#     "0xPolygon",
#     "dogecoin",
#     "solana",
#     "dot",
#     "SHIBArmy",
#     "litecoin",
#     "Tronix",
#     "Avax",
#     "Uniswap",
#     "cosmosnetwork",
#     "chainlink",
#     "bitfinex",
#     "EthereumClassic",
#     "monero",
#     "Bitcoincash",
#     "okx",
#     "stellar",
#     "hedera",
#     "lidofinance",
#     "Crypto_com",
#     "AlgorandOfficial",
#     "vechain",
#     "QuantNetwork",
#     "dfinity",
#     "thegraph",
#     "decentraland",
#     "FantomFoundation",
#     "EOS",
#     "Aave_Official",
#     "theta_network",
#     "AxieInfinity",
#     "tezos",
#     "terraluna",
#     "HuobiGlobal",
#     "kucoin",
#     "ImmutableX/",
#     "zec",
#     "pancakeswap/",
#     "MakerDAO",
#     "CurveDAO",
#     "MinaProtocol",
#     "BittorrentToken",
#     "ecash",
#     "dashpay",
#     "Iota",
#     "NEO",
#     "synthetix_io",
#     "Gemini",
#     "klaytn",
#     "trustwallet",
#     "thorchain",
#     "rocketpool",
#     "SingularityNet",
#     "loopringorg",
#     "EnjinCoin",
#     "zilliqa",
#     "1inch",
#     "nexo",
#     "CasperCSPR",
#     "BATProject",
#     "dydxprotocol",
#     "stacks",
#     "terraluna",
#     "xinfin",
#     "WOO_X",
#     "holochain",
#     "decred",
#     "Ravencoin",
#     "CeloHQ",
#     "oasisnetwork/",
#     "Arweave",
#     "FetchAI_Community",
#     "kava_platform/",
#     "HeliumNetwork",
#     "thresholdnetwork",
#     "theta_network",
#     "harmony_one/",
#     "GoGalaGames/",
#     "Qtum",
#     "BitcoinGoldHQ",
#     "gnosisPM",
#     "Ankrofficial/",
#     "SushiSwap",
#     "SSVnetwork/",
#     "IoTex",
#     "oceanprotocol",
#     "Wavesplatform",
#     "chia",
#     "StepN",
#     "moonbeam",
#     "SHIBArmy",
#     "GolemProject",
#     "livepeer",
#     "MaskNetwork",
#     "kadena/",
# ]


def runner():
    print("JOB START")
    start = time.time()
    data.find_crypto_sentiments(subreddits)
    end = time.time()
    print("JOB DONE")
    print(f"Time taken: {end-start}")


runner()
