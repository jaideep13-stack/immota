"""
Yahoo Finance Adapter (FREE)
============================
Active provider for market data.
To upgrade: replace with polygon_adapter.py or bloomberg_adapter.py
"""

import yfinance as yf
import pandas as pd
import requests
from services.base import MarketDataProvider
import config


class YahooFinanceAdapter(MarketDataProvider):

    def get_stock_price(self, symbol: str) -> dict:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")

            current = info.get("currentPrice") or info.get("regularMarketPrice", 0)
            prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose", 0)
            change = current - prev_close if current and prev_close else 0
            change_pct = (change / prev_close * 100) if prev_close else 0

            return {
                "symbol": symbol,
                "name": info.get("shortName", symbol),
                "price": round(current, 2),
                "change": round(change, 2),
                "change_pct": round(change_pct, 2),
                "volume": info.get("volume", 0),
                "market_cap": info.get("marketCap", 0),
                "currency": info.get("currency", "INR"),
            }
        except Exception as e:
            return {"symbol": symbol, "error": str(e), "price": 0}

    def get_stock_history(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            return pd.DataFrame()

    def get_stock_info(self, symbol: str) -> dict:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                "name": info.get("longName", ""),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "description": info.get("longBusinessSummary", ""),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "eps": info.get("trailingEps", "N/A"),
                "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "beta": info.get("beta", "N/A"),
                "revenue": info.get("totalRevenue", "N/A"),
                "profit_margin": info.get("profitMargins", "N/A"),
                "website": info.get("website", ""),
                "employees": info.get("fullTimeEmployees", "N/A"),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_market_overview(self) -> dict:
        result = {}
        all_indices = config.NIFTY_SYMBOLS + config.GLOBAL_INDICES
        for symbol in all_indices:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                price = info.get("regularMarketPrice") or info.get("currentPrice", 0)
                prev = info.get("regularMarketPreviousClose", price)
                change_pct = ((price - prev) / prev * 100) if prev else 0
                result[symbol] = {
                    "name": info.get("shortName", symbol),
                    "price": round(price, 2),
                    "change_pct": round(change_pct, 2),
                }
            except:
                pass
        return result

    def get_fii_dii_data(self) -> dict:
        """
        NSE FII/DII data via NSE India public endpoint.
        Best effort — NSE sometimes blocks scrapers.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
                "Referer": "https://www.nseindia.com/",
            }
            session = requests.Session()
            session.get("https://www.nseindia.com", headers=headers, timeout=5)
            url = "https://www.nseindia.com/api/fiidiiTradeReact"
            resp = session.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            return {"error": "NSE data unavailable", "data": []}
        except Exception as e:
            return {"error": str(e), "data": []}


# ============================================
# PAID ADAPTER — Polygon.io (~$29/month)
# Uncomment and replace YahooFinanceAdapter in config.py
# ============================================

# import requests
# from services.base import MarketDataProvider
#
# class PolygonAdapter(MarketDataProvider):
#
#     BASE_URL = "https://api.polygon.io/v2"
#
#     def __init__(self):
#         import os
#         self.api_key = os.getenv("POLYGON_API_KEY")
#
#     def get_stock_price(self, symbol: str) -> dict:
#         url = f"{self.BASE_URL}/aggs/ticker/{symbol}/prev"
#         r = requests.get(url, params={"apiKey": self.api_key})
#         data = r.json()["results"][0]
#         return {
#             "symbol": symbol,
#             "price": data["c"],
#             "change": data["c"] - data["o"],
#             "change_pct": ((data["c"] - data["o"]) / data["o"]) * 100,
#             "volume": data["v"],
#         }
