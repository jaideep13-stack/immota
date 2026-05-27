"""
CoinGecko Adapter (FREE)
========================
Active crypto provider. 50 requests/min on free tier.
To upgrade: replace with coinmarketcap_adapter
"""

from pycoingecko import CoinGeckoAPI
from services.base import CryptoDataProvider
import pandas as pd


class CoinGeckoAdapter(CryptoDataProvider):

    def __init__(self):
        self.cg = CoinGeckoAPI()

    def get_crypto_price(self, coin_id: str) -> dict:
        try:
            data = self.cg.get_coin_by_id(
                coin_id,
                localization=False,
                tickers=False,
                market_data=True,
                community_data=False,
                developer_data=False,
            )
            md = data["market_data"]
            return {
                "id": coin_id,
                "name": data["name"],
                "symbol": data["symbol"].upper(),
                "price": md["current_price"]["usd"],
                "price_inr": md["current_price"].get("inr", 0),
                "change_24h": md["price_change_percentage_24h"],
                "change_7d": md["price_change_percentage_7d"],
                "volume": md["total_volume"]["usd"],
                "market_cap": md["market_cap"]["usd"],
                "circulating_supply": md["circulating_supply"],
                "ath": md["ath"]["usd"],
                "image": data["image"]["small"],
            }
        except Exception as e:
            return {"id": coin_id, "error": str(e), "price": 0}

    def get_crypto_history(self, coin_id: str, days: int = 30) -> pd.DataFrame:
        try:
            data = self.cg.get_coin_market_chart_by_id(
                id=coin_id, vs_currency="usd", days=days
            )
            prices = data["prices"]
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("date", inplace=True)
            return df
        except:
            return pd.DataFrame()

    def get_top_coins(self, limit: int = 20) -> list:
        try:
            coins = self.cg.get_coins_markets(
                vs_currency="usd",
                order="market_cap_desc",
                per_page=limit,
                page=1,
                sparkline=False,
                price_change_percentage="24h,7d",
            )
            return coins
        except:
            return []

    def get_market_summary(self) -> dict:
        try:
            global_data = self.cg.get_global()["data"]
            return {
                "total_market_cap": global_data["total_market_cap"]["usd"],
                "total_volume": global_data["total_volume"]["usd"],
                "btc_dominance": global_data["market_cap_percentage"]["btc"],
                "eth_dominance": global_data["market_cap_percentage"].get("eth", 0),
                "market_cap_change_24h": global_data["market_cap_change_percentage_24h_usd"],
                "active_coins": global_data["active_cryptocurrencies"],
            }
        except:
            return {}


# ============================================
# PAID ADAPTER — CoinMarketCap (~$79/month)
# Real-time tick data, better coverage
# ============================================

# import requests, os
# from services.base import CryptoDataProvider
#
# class CoinMarketCapAdapter(CryptoDataProvider):
#
#     BASE_URL = "https://pro-api.coinmarketcap.com/v1"
#
#     def __init__(self):
#         self.api_key = os.getenv("COINMARKETCAP_API_KEY")
#         self.headers = {"X-CMC_PRO_API_KEY": self.api_key}
#
#     def get_crypto_price(self, coin_id: str) -> dict:
#         r = requests.get(
#             f"{self.BASE_URL}/cryptocurrency/quotes/latest",
#             headers=self.headers,
#             params={"slug": coin_id, "convert": "USD,INR"}
#         )
#         # parse and return...
