# 📊 IMMOTA — Intelligent Market Intelligence Platform

> AI-powered market intelligence for educational purposes | Indian & Global Markets

⚠️ **DISCLAIMER**: IMMOTA is NOT registered with SEBI. This platform is for educational purposes only. Nothing here is financial advice.

---

## Features

- 🏠 **Dashboard** — Live Nifty/Sensex/Global indices + watchlist + FII/DII data
- 🔍 **Stock Analysis** — Deep dive any stock: chart, fundamentals, AI analysis
- ₿ **Crypto Markets** — Top 20 coins, historical charts, global market summary
- 💱 **Forex** — Live INR pairs, currency converter, all major rates
- 🤖 **AI Intelligence** — AI market analysis + investor education (Groq/LLaMA 3)
- 📰 **News Hub** — Real-time financial news across all market categories
- ⚖️ **Comparator** — Compare 2-5 stocks side by side with normalized charts
- 👥 **Predictions** — Community predictions board (upvote/downvote)
- ⚙️ **Settings** — API key setup, watchlist management

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/immota.git
cd immota
pip install -r requirements.txt
```

### 2. Add API Keys (Free)

```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_key   # console.groq.com — FREE
NEWS_API_KEY=your_key   # newsapi.org — FREE
```

**Without keys:** App still works. AI analysis disabled, news falls back to Economic Times RSS.

### 3. Run

```bash
streamlit run app.py
```

Open: http://localhost:8501

---

## Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `app.py`
5. Add secrets in dashboard:
   - `GROQ_API_KEY`
   - `NEWS_API_KEY`
6. Deploy → get public URL

**Done. Free hosting forever on Streamlit Cloud.**

---

## Upgrading from Free to Paid APIs

All providers are in `config.py`. To upgrade:

```python
# config.py — change ONE line
MARKET_PROVIDER = "polygon"    # was "yahoo"
CRYPTO_PROVIDER = "coinmarketcap"  # was "coingecko"
```

Each adapter file has the paid version pre-written and commented out.

---

## Project Structure

```
IMMOTA/
├── app.py                    # Main entry point
├── config.py                 # All settings & provider switching
├── requirements.txt
├── .env.example
├── services/
│   ├── base.py               # Abstract interfaces (never changes)
│   ├── factory.py            # Creates right adapter from config
│   ├── market_data/
│   │   └── yahoo_adapter.py  # FREE active | bloomberg commented
│   ├── crypto/
│   │   └── coingecko_adapter.py  # FREE active | coinmarketcap commented
│   ├── forex/
│   │   └── exchangerate_adapter.py  # FREE active | oanda commented
│   ├── news/
│   │   └── newsapi_adapter.py  # FREE active | refinitiv commented
│   └── ai_analysis/
│       └── groq_adapter.py   # FREE active | openai commented
├── views/
│   ├── dashboard.py
│   ├── stock_analysis.py
│   ├── crypto.py
│   ├── forex.py
│   ├── ai_intelligence.py
│   ├── news.py
│   ├── screener.py
│   ├── predictions.py
│   └── settings.py
└── utils/
    └── helpers.py            # Charts, formatters, SEBI disclaimer
```

---

## Tech Stack

| Layer | Technology | Cost |
|-------|-----------|------|
| Frontend | Streamlit | Free |
| Market Data | Yahoo Finance (yfinance) | Free |
| Crypto | CoinGecko API | Free |
| Forex | ExchangeRate-API | Free |
| News | NewsAPI + ET RSS | Free |
| AI | Groq (LLaMA 3-8b) | Free |
| Hosting | Streamlit Cloud | Free |

**Total monthly cost: ₹0**

---

## Legal

IMMOTA is not registered with SEBI, RBI, or any regulatory authority.
All market data, analysis, and AI-generated content is for educational purposes only.
Users must do their own research and consult SEBI-registered advisors before making investment decisions.
