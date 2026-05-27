"""
IMMOTA Configuration
====================
All provider switching happens in THIS file only.
To upgrade from free to paid: change the import line.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# API KEYS
# ============================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# ============================================
# PROVIDER SELECTION — CHANGE HERE TO UPGRADE
# ============================================

# --- MARKET DATA ---
MARKET_PROVIDER = "yahoo"          # FREE
# MARKET_PROVIDER = "polygon"      # PAID ~$29/month
# MARKET_PROVIDER = "bloomberg"    # PAID ~$2000/month

# --- CRYPTO DATA ---
CRYPTO_PROVIDER = "coingecko"      # FREE
# CRYPTO_PROVIDER = "coinmarketcap" # PAID ~$79/month

# --- FOREX DATA ---
FOREX_PROVIDER = "exchangerate"    # FREE
# FOREX_PROVIDER = "oanda"         # PAID ~$50/month

# --- NEWS ---
NEWS_PROVIDER = "newsapi"          # FREE (100 req/day)
# NEWS_PROVIDER = "refinitiv"      # PAID ~$500/month

# --- AI ANALYSIS ---
AI_PROVIDER = "groq"               # FREE
# AI_PROVIDER = "openai"           # PAID ~$0.01/1k tokens
# AI_PROVIDER = "anthropic"        # PAID ~$0.015/1k tokens

# ============================================
# APP SETTINGS
# ============================================
APP_NAME = "IMMOTA"
APP_TAGLINE = "Intelligent Market Intelligence Platform"
REFRESH_INTERVAL = 300  # seconds (5 min)

# Indian market indices
NIFTY_SYMBOLS = ["^NSEI", "^BSESN", "NIFTYBANK.NS"]
GLOBAL_INDICES = ["^GSPC", "^DJI", "^IXIC", "^FTSE", "^N225"]

# Default watchlist
DEFAULT_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
    "WIPRO.NS", "TATAMOTORS.NS", "ADANIENT.NS", "BAJFINANCE.NS"
]

DEFAULT_CRYPTO = ["bitcoin", "ethereum", "solana", "ripple", "cardano"]

FOREX_PAIRS = ["USD/INR", "EUR/INR", "GBP/INR", "JPY/INR", "USD/EUR"]
