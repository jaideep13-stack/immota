"""
View: Stock Analysis
====================
Deep dive into individual stocks with AI analysis
"""

import streamlit as st
import pandas as pd
from services.factory import get_market_provider, get_news_provider, get_ai_provider
from utils.helpers import (
    format_number, format_change, make_candlestick_chart,
    make_line_chart, format_large_usd
)
import config


POPULAR_STOCKS = {
    "🇮🇳 Indian Stocks": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
        "WIPRO.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "BAJFINANCE.NS",
        "TATAMOTORS.NS", "ADANIENT.NS", "MARUTI.NS", "ITC.NS",
        "SUNPHARMA.NS", "SBIN.NS", "AXISBANK.NS", "LT.NS",
    ],
    "🌍 US Stocks": [
        "AAPL", "GOOGL", "MSFT", "AMZN", "NVDA",
        "META", "TSLA", "JPM", "V", "JNJ",
    ],
}


def render():
    st.title("🔍 Stock Analysis")
    st.caption("Deep dive into any stock — price history, financials, AI insights")

    market = get_market_provider()
    news_provider = get_news_provider()
    ai = get_ai_provider()

    # ---- STOCK SELECTOR ----
    col1, col2 = st.columns([2, 1])
    with col1:
        symbol_input = st.text_input(
            "Enter Stock Symbol",
            placeholder="e.g. RELIANCE.NS, TCS.NS, AAPL",
            help="Add .NS for NSE stocks, .BO for BSE stocks",
        )
    with col2:
        category = st.selectbox("Quick Pick", list(POPULAR_STOCKS.keys()))

    selected_from_list = st.selectbox(
        f"Select from {category}",
        POPULAR_STOCKS[category],
        index=0,
    )

    symbol = symbol_input.upper() if symbol_input else selected_from_list
    period = st.select_slider(
        "History Period",
        options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        value="3mo",
    )

    if not symbol:
        st.info("Enter a stock symbol above to begin analysis")
        return

    # ---- LOAD DATA ----
    with st.spinner(f"Loading {symbol}..."):
        price_data = market.get_stock_price(symbol)
        stock_info = market.get_stock_info(symbol)
        history = market.get_stock_history(symbol, period)
        stock_news = news_provider.get_stock_news(symbol, limit=5)

    if "error" in price_data:
        st.error(f"Could not load {symbol}. Check the symbol and try again.")
        return

    # ---- HEADER METRICS ----
    st.divider()
    name = stock_info.get("name") or price_data.get("name", symbol)
    st.subheader(f"{name} ({symbol})")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        currency = "₹" if ".NS" in symbol or ".BO" in symbol else "$"
        st.metric("Current Price", f"{currency}{price_data.get('price', 0):,.2f}")
    with col2:
        change = price_data.get("change_pct", 0)
        st.metric("Day Change", f"{change:+.2f}%", delta=f"{change:+.2f}%")
    with col3:
        vol = price_data.get("volume", 0)
        st.metric("Volume", f"{vol:,.0f}" if vol else "N/A")
    with col4:
        mc = price_data.get("market_cap", 0)
        st.metric("Market Cap", format_large_usd(mc) if mc else "N/A")

    # ---- CHART ----
    st.subheader("📈 Price Chart")
    if not history.empty:
        chart = make_candlestick_chart(history, title=f"{symbol} — {period}")
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.warning("Chart data unavailable for this period.")

    # ---- FUNDAMENTALS ----
    st.subheader("📋 Fundamentals")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("P/E Ratio", stock_info.get("pe_ratio", "N/A"))
        st.metric("EPS", stock_info.get("eps", "N/A"))
        st.metric("Beta", stock_info.get("beta", "N/A"))
    with col2:
        st.metric("52W High", f"{currency}{stock_info.get('52w_high', 'N/A')}")
        st.metric("52W Low", f"{currency}{stock_info.get('52w_low', 'N/A')}")
        st.metric("Dividend Yield", stock_info.get("dividend_yield", "N/A"))
    with col3:
        st.metric("Sector", stock_info.get("sector", "N/A"))
        st.metric("Employees", f"{stock_info.get('employees', 'N/A'):,}" if isinstance(stock_info.get("employees"), int) else "N/A")
        margin = stock_info.get("profit_margin")
        st.metric("Profit Margin", f"{float(margin)*100:.1f}%" if margin and margin != "N/A" else "N/A")

    # ---- ABOUT ----
    description = stock_info.get("description", "")
    if description:
        with st.expander("📖 About the Company"):
            st.write(description[:800] + "..." if len(description) > 800 else description)
            if stock_info.get("website"):
                st.link_button("Visit Website", stock_info["website"])

    st.divider()

    # ---- AI ANALYSIS ----
    st.subheader("🤖 AI Analysis (Educational Only)")
    st.warning("⚠️ AI-generated analysis — NOT investment advice. For educational purposes only.")

    if st.button("Generate AI Analysis", type="primary"):
        with st.spinner("AI is analyzing this stock..."):
            combined_data = {**price_data, **stock_info}
            analysis = ai.analyze_stock(combined_data, stock_news)
        st.markdown(analysis)

        # Trend prediction
        if not history.empty:
            st.subheader("📉 Trend Direction (Educational)")
            trend = ai.predict_trend(history.to_dict())
            tcol1, tcol2 = st.columns(2)
            with tcol1:
                direction = trend.get("direction", "Unknown")
                emoji = "📈" if "Up" in direction else "📉" if "Down" in direction else "➡️"
                st.metric("Trend", f"{emoji} {direction}")
            with tcol2:
                st.metric("Confidence", f"{trend.get('confidence', 0):.0f}%")
            st.caption(trend.get("reasoning", ""))
            st.caption("⚠️ " + trend.get("disclaimer", "Educational only"))

    # ---- RECENT NEWS ----
    st.divider()
    st.subheader(f"📰 News for {name}")
    if stock_news:
        for article in stock_news:
            with st.container(border=True):
                st.markdown(f"**{article['title']}**")
                st.caption(f"🗞 {article['source']} | {article.get('published_at', '')[:10]}")
                if article.get("url"):
                    st.link_button("Read →", article["url"])
    else:
        st.info("No recent news found for this stock.")
