"""
Base Provider Interfaces
========================
All adapters MUST implement these interfaces.
This ensures swapping free → paid needs zero changes elsewhere.
"""

from abc import ABC, abstractmethod
from typing import Optional


class MarketDataProvider(ABC):

    @abstractmethod
    def get_stock_price(self, symbol: str) -> dict:
        """Returns: {symbol, price, change, change_pct, volume, market_cap}"""
        pass

    @abstractmethod
    def get_stock_history(self, symbol: str, period: str) -> dict:
        """period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y"""
        pass

    @abstractmethod
    def get_stock_info(self, symbol: str) -> dict:
        """Returns: {name, sector, description, pe_ratio, eps, 52w_high, 52w_low}"""
        pass

    @abstractmethod
    def get_market_overview(self) -> dict:
        """Returns all major indices prices"""
        pass

    @abstractmethod
    def get_fii_dii_data(self) -> dict:
        """Returns FII and DII buy/sell data"""
        pass


class CryptoDataProvider(ABC):

    @abstractmethod
    def get_crypto_price(self, coin_id: str) -> dict:
        """Returns: {id, name, price, change_24h, volume, market_cap}"""
        pass

    @abstractmethod
    def get_crypto_history(self, coin_id: str, days: int) -> dict:
        pass

    @abstractmethod
    def get_top_coins(self, limit: int = 20) -> list:
        pass

    @abstractmethod
    def get_market_summary(self) -> dict:
        """Global crypto market cap, dominance, etc."""
        pass


class ForexDataProvider(ABC):

    @abstractmethod
    def get_rate(self, base: str, target: str) -> dict:
        """Returns: {pair, rate, change}"""
        pass

    @abstractmethod
    def get_all_rates(self, base: str = "USD") -> dict:
        pass


class NewsDataProvider(ABC):

    @abstractmethod
    def get_market_news(self, query: str = "stock market India", limit: int = 10) -> list:
        """Returns list of {title, description, url, source, published_at}"""
        pass

    @abstractmethod
    def get_stock_news(self, symbol: str, limit: int = 5) -> list:
        pass


class AIAnalysisProvider(ABC):

    @abstractmethod
    def analyze_market(self, market_data: dict, news: list) -> str:
        """Returns AI-generated market analysis text"""
        pass

    @abstractmethod
    def analyze_stock(self, stock_data: dict, news: list) -> str:
        """Returns AI-generated stock analysis text"""
        pass

    @abstractmethod
    def predict_trend(self, historical_data: dict) -> dict:
        """Returns {direction, confidence, reasoning}"""
        pass
