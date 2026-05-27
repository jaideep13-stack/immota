"""
View: Crypto Markets
====================
Top coins, charts, global crypto market summary
"""

import streamlit as st
import pandas as pd
from services.factory import get_crypto_provider, get_news_provider, get_ai_provider
from utils.helpers import format_large_usd, make_line_chart
import config


def render():
    st.title("₿ Crypto Markets")
    st.caption("Top cryptocurrencies, market trends, AI insights")

    crypto = get_crypto_provider()
    news_provider = get_news_provider()
    ai = get_ai_provider()

    # ---- GLOBAL SUMMARY ----
    st.subheader("🌍 Global Crypto Market")
    with st.spinner("Loading global market data..."):
        summary = crypto.get_market_summary()

    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Market Cap", format_large_usd(summary.get("total_market_cap", 0)))
        with col2:
            st.metric("24h Volume", format_large_usd(summary.get("total_volume", 0)))
        with col3:
            btc_dom = summary.get("btc_dominance", 0)
            st.metric("BTC Dominance", f"{btc_dom:.1f}%")
        with col4:
            change = summary.get("market_cap_change_24h", 0)
            st.metric("24h Market Change", f"{change:+.2f}%")
    else:
        st.warning("Global market summary unavailable.")

    st.divider()

    # ---- TOP COINS TABLE ----
    st.subheader("🏆 Top 20 Cryptocurrencies")
    with st.spinner("Loading top coins..."):
        top_coins = crypto.get_top_coins(limit=20)

    if top_coins:
        rows = []
        for coin in top_coins:
            rows.append({
                "Rank": coin.get("market_cap_rank", ""),
                "Coin": coin.get("name", ""),
                "Symbol": coin.get("symbol", "").upper(),
                "Price (USD)": f"${coin.get('current_price', 0):,.4f}",
                "24h Change": f"{coin.get('price_change_percentage_24h', 0):+.2f}%",
                "7d Change": f"{coin.get('price_change_percentage_7d_in_currency', 0):+.2f}%",
                "Market Cap": format_large_usd(coin.get("market_cap", 0)),
                "Volume (24h)": format_large_usd(coin.get("total_volume", 0)),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error("Could not load top coins. CoinGecko rate limit may be hit. Try again in a minute.")

    st.divider()

    # ---- COIN DEEP DIVE ----
    st.subheader("🔍 Coin Deep Dive")

    coin_options = {
        "Bitcoin": "bitcoin",
        "Ethereum": "ethereum",
        "Solana": "solana",
        "Ripple (XRP)": "ripple",
        "Cardano": "cardano",
        "Dogecoin": "dogecoin",
        "Polygon": "matic-network",
        "Avalanche": "avalanche-2",
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_coin_name = st.selectbox("Select Coin", list(coin_options.keys()))
        selected_coin_id = coin_options[selected_coin_name]
    with col2:
        history_days = st.selectbox("History", [7, 14, 30, 90, 180, 365], index=2)

    with st.spinner(f"Loading {selected_coin_name}..."):
        coin_data = crypto.get_crypto_price(selected_coin_id)
        coin_history = crypto.get_crypto_history(selected_coin_id, history_days)

    if "error" not in coin_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Price (USD)", f"${coin_data.get('price', 0):,.4f}")
        with col2:
            change_24h = coin_data.get("change_24h", 0)
            st.metric("24h Change", f"{change_24h:+.2f}%", delta=f"{change_24h:+.2f}%")
        with col3:
            change_7d = coin_data.get("change_7d", 0)
            st.metric("7d Change", f"{change_7d:+.2f}%")
        with col4:
            st.metric("Market Cap", format_large_usd(coin_data.get("market_cap", 0)))

        # Price in INR
        if coin_data.get("price_inr"):
            st.info(f"💰 Price in INR: ₹{coin_data['price_inr']:,.2f}")

        if not coin_history.empty:
            chart = make_line_chart(coin_history, y_col="price", title=f"{selected_coin_name} — {history_days}d")
            st.plotly_chart(chart, use_container_width=True)
    else:
        st.error(f"Error: {coin_data.get('error', 'Unknown error')}")

    st.divider()

    # ---- AI CRYPTO ANALYSIS ----
    st.subheader("🤖 AI Crypto Analysis (Educational)")
    st.warning("⚠️ AI analysis is for learning only. Crypto is highly volatile. Not financial advice.")

    if st.button("Generate Crypto Market Analysis", type="primary"):
        with st.spinner("AI analyzing crypto market..."):
            crypto_news = news_provider.get_market_news("cryptocurrency bitcoin ethereum", limit=5)
            market_context = {
                "summary": summary,
                "top_coin": coin_data,
            }
            analysis = ai.analyze_market(market_context, crypto_news)
        st.markdown(analysis)
