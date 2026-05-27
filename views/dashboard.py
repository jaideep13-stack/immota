"""
View: Market Dashboard
"""

import streamlit as st
import pandas as pd
from services.factory import get_market_provider, get_news_provider
from utils.helpers import format_large_usd, get_change_color
import config


def render():
    st.title("📊 Market Dashboard")
    st.caption("Live market overview — Indian & Global indices")

    market = get_market_provider()
    news = get_news_provider()

    with st.spinner("Loading market data..."):
        overview = market.get_market_overview()

    if overview:
        st.subheader("🇮🇳 Indian Markets")
        indian_symbols = {"^NSEI": "Nifty 50", "^BSESN": "Sensex", "NIFTYBANK.NS": "Bank Nifty"}
        cols = st.columns(len(indian_symbols))
        for i, (sym, name) in enumerate(indian_symbols.items()):
            data = overview.get(sym, {})
            with cols[i]:
                price = data.get("price", 0)
                change = data.get("change_pct", 0)
                st.metric(label=name, value=f"₹{price:,.2f}" if price else "N/A", delta=f"{change:+.2f}%" if change else None)

        st.subheader("🌍 Global Markets")
        global_symbols = {"^GSPC": "S&P 500", "^DJI": "Dow Jones", "^IXIC": "NASDAQ", "^FTSE": "FTSE 100", "^N225": "Nikkei 225"}
        cols = st.columns(len(global_symbols))
        for i, (sym, name) in enumerate(global_symbols.items()):
            data = overview.get(sym, {})
            with cols[i]:
                price = data.get("price", 0)
                change = data.get("change_pct", 0)
                st.metric(label=name, value=f"${price:,.2f}" if price else "N/A", delta=f"{change:+.2f}%" if change else None)
    else:
        st.error("Market data unavailable. Check your internet connection.")

    st.divider()

    st.subheader("⭐ Your Watchlist")
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = config.DEFAULT_STOCKS[:4]

    col1, col2 = st.columns([3, 1])
    with col2:
        new_stock = st.text_input("Add stock (e.g. INFY.NS)", key="add_watch")
        if st.button("Add") and new_stock:
            if new_stock not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_stock.upper())
                st.rerun()

    watchlist_data = []
    with st.spinner("Loading watchlist..."):
        for sym in st.session_state.watchlist:
            data = market.get_stock_price(sym)
            if "error" not in data:
                watchlist_data.append(data)

    if watchlist_data:
        df = pd.DataFrame(watchlist_data)
        df = df[["symbol", "name", "price", "change", "change_pct", "volume"]].copy()
        df.columns = ["Symbol", "Name", "Price (₹)", "Change", "Change %", "Volume"]
        df["Change %"] = df["Change %"].apply(lambda x: f"{x:+.2f}%")
        df["Volume"] = df["Volume"].apply(lambda x: f"{x:,.0f}" if x else "N/A")
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("🏦 FII / DII Activity")
    fii_data = {}
    with st.spinner("Fetching FII/DII data from NSE..."):
        fii_data = market.get_fii_dii_data()

    if isinstance(fii_data, list) and len(fii_data) > 0:
        df_fii = pd.DataFrame(fii_data[:10])
        if not df_fii.empty:
            st.dataframe(df_fii, use_container_width=True, hide_index=True)
        st.caption("Source: NSE India — FII = Foreign Institutional Investors, DII = Domestic Institutional Investors")
    elif isinstance(fii_data, dict) and fii_data.get("data"):
        df_fii = pd.DataFrame(fii_data["data"][:10])
        st.dataframe(df_fii, use_container_width=True, hide_index=True)
    else:
        st.info("FII/DII data temporarily unavailable. NSE sometimes restricts access.")
        st.caption("Tip: Check nseindia.com directly for latest FII/DII data.")

    st.divider()

    st.subheader("📰 Market News")
    with st.spinner("Loading news..."):
        articles = news.get_market_news(query="Indian stock market NSE BSE", limit=6)

    if articles:
        for i in range(0, len(articles), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(articles):
                    article = articles[i + j]
                    with col:
                        with st.container(border=True):
                            st.markdown(f"**{article['title'][:100]}**")
                            st.caption(f"🗞 {article['source']} | {article['published_at'][:10] if article.get('published_at') else ''}")
                            if article.get("description"):
                                st.caption(article["description"][:120] + "...")
                            if article.get("url"):
                                st.link_button("Read More →", article["url"])
    else:
        st.info("News unavailable. Add NEWS_API_KEY in .env for full news access.")