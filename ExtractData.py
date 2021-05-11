import requests
from pycoingecko import CoinGeckoAPI


class ExtractData:
    cg = CoinGeckoAPI()

    def getCoinsList(self):
        return self.cg.get_coins_list()

    def getCoinsMarket(self):
        return self.cg.get_coins_markets(vs_currency='usd')
