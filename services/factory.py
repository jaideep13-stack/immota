"""
Provider Factory
================
Single place that creates the right adapter based on config.py settings.
No other file should import adapters directly.
"""

import config


def get_market_provider():
    if config.MARKET_PROVIDER == "yahoo":
        from services.market_data.yahoo_adapter import YahooFinanceAdapter
        return YahooFinanceAdapter()
    # elif config.MARKET_PROVIDER == "polygon":
    #     from services.market_data.polygon_adapter import PolygonAdapter
    #     return PolygonAdapter()
    # elif config.MARKET_PROVIDER == "bloomberg":
    #     from services.market_data.bloomberg_adapter import BloombergAdapter
    #     return BloombergAdapter()
    else:
        raise ValueError(f"Unknown market provider: {config.MARKET_PROVIDER}")


def get_crypto_provider():
    if config.CRYPTO_PROVIDER == "coingecko":
        from services.crypto.coingecko_adapter import CoinGeckoAdapter
        return CoinGeckoAdapter()
    # elif config.CRYPTO_PROVIDER == "coinmarketcap":
    #     from services.crypto.coinmarketcap_adapter import CoinMarketCapAdapter
    #     return CoinMarketCapAdapter()
    else:
        raise ValueError(f"Unknown crypto provider: {config.CRYPTO_PROVIDER}")


def get_forex_provider():
    if config.FOREX_PROVIDER == "exchangerate":
        from services.forex.exchangerate_adapter import ExchangeRateAdapter
        return ExchangeRateAdapter()
    # elif config.FOREX_PROVIDER == "oanda":
    #     from services.forex.oanda_adapter import OANDAAdapter
    #     return OANDAAdapter()
    else:
        raise ValueError(f"Unknown forex provider: {config.FOREX_PROVIDER}")


def get_news_provider():
    if config.NEWS_PROVIDER == "newsapi":
        from services.news.newsapi_adapter import NewsAPIAdapter
        return NewsAPIAdapter()
    # elif config.NEWS_PROVIDER == "refinitiv":
    #     from services.news.refinitiv_adapter import RefinitivAdapter
    #     return RefinitivAdapter()
    else:
        raise ValueError(f"Unknown news provider: {config.NEWS_PROVIDER}")


def get_ai_provider():
    if config.AI_PROVIDER == "groq":
        from services.ai_analysis.groq_adapter import GroqAdapter
        return GroqAdapter()
    # elif config.AI_PROVIDER == "openai":
    #     from services.ai_analysis.openai_adapter import OpenAIAdapter
    #     return OpenAIAdapter()
    # elif config.AI_PROVIDER == "anthropic":
    #     from services.ai_analysis.anthropic_adapter import AnthropicAdapter
    #     return AnthropicAdapter()
    else:
        raise ValueError(f"Unknown AI provider: {config.AI_PROVIDER}")
