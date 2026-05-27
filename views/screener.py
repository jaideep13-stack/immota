"""
View: Stock Screener & Comparator
===================================
Compare multiple stocks side by side
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from services.factory import get_market_provider
from utils.helpers import format_large_usd, CHART_THEME
import config


def render():
    st.title("⚖️ Stock Comparator")
    st.caption("Compare multiple stocks side by side — performance, fundamentals, charts")

    market = get_market_provider()

    # ---- STOCK SELECTION ----
    st.subheader("Select Stocks to Compare")
    selected_stocks = st.multiselect(
        "Choose 2-5 stocks",
        config.DEFAULT_STOCKS + ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"],
        default=config.DEFAULT_STOCKS[:3],
        max_selections=5,
    )

    custom_stocks = st.text_input(
        "Or add custom symbols (comma-separated)",
        placeholder="HCLTECH.NS, MINDTREE.NS, PERSISTENT.NS",
    )
    if custom_stocks:
        extras = [s.strip().upper() for s in custom_stocks.split(",") if s.strip()]
        selected_stocks = list(set(selected_stocks + extras))[:5]

    period = st.select_slider(
        "Comparison Period",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        value="3mo",
    )

    if len(selected_stocks) < 2:
        st.info("Select at least 2 stocks to compare")
        return

    if st.button("Compare Now", type="primary"):
        _run_comparison(market, selected_stocks, period)


def _run_comparison(market, stocks: list, period: str):
    # ---- LOAD ALL DATA ----
    all_prices = {}
    all_info = {}
    all_history = {}

    progress = st.progress(0)
    for i, sym in enumerate(stocks):
        with st.spinner(f"Loading {sym}..."):
            all_prices[sym] = market.get_stock_price(sym)
            all_info[sym] = market.get_stock_info(sym)
            hist = market.get_stock_history(sym, period)
            if not hist.empty:
                all_history[sym] = hist
        progress.progress((i + 1) / len(stocks))

    # ---- PRICE METRICS COMPARISON ----
    st.divider()
    st.subheader("💰 Current Price Comparison")
    cols = st.columns(len(stocks))
    for i, sym in enumerate(stocks):
        with cols[i]:
            data = all_prices[sym]
            name = data.get("name", sym)[:15]
            price = data.get("price", 0)
            change = data.get("change_pct", 0)
            currency = "₹" if ".NS" in sym or ".BO" in sym else "$"
            st.metric(
                label=f"{name}\n({sym})",
                value=f"{currency}{price:,.2f}",
                delta=f"{change:+.2f}%",
            )

    # ---- NORMALIZED PERFORMANCE CHART ----
    st.subheader(f"📈 Relative Performance ({period})")
    st.caption("All stocks normalized to 100 at start — shows who performed better")

    if all_history:
        fig = go.Figure()
        for sym, hist in all_history.items():
            if "Close" in hist.columns and len(hist) > 1:
                normalized = (hist["Close"] / hist["Close"].iloc[0]) * 100
                fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=normalized,
                    mode="lines",
                    name=sym,
                    line=dict(width=2),
                ))

        fig.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.5)
        fig.update_layout(
            paper_bgcolor=CHART_THEME["bg_color"],
            plot_bgcolor=CHART_THEME["bg_color"],
            font=dict(color=CHART_THEME["text_color"]),
            xaxis=dict(gridcolor=CHART_THEME["grid_color"]),
            yaxis=dict(gridcolor=CHART_THEME["grid_color"], title="Relative Performance (base=100)"),
            height=400,
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---- FUNDAMENTALS COMPARISON TABLE ----
    st.subheader("📋 Fundamentals Comparison")
    rows = {
        "Sector": [],
        "P/E Ratio": [],
        "EPS": [],
        "52W High": [],
        "52W Low": [],
        "Beta": [],
        "Profit Margin": [],
        "Dividend Yield": [],
    }

    for sym in stocks:
        info = all_info[sym]
        rows["Sector"].append(info.get("sector", "N/A"))
        rows["P/E Ratio"].append(info.get("pe_ratio", "N/A"))
        rows["EPS"].append(info.get("eps", "N/A"))
        rows["52W High"].append(info.get("52w_high", "N/A"))
        rows["52W Low"].append(info.get("52w_low", "N/A"))
        rows["Beta"].append(info.get("beta", "N/A"))
        margin = info.get("profit_margin")
        rows["Profit Margin"].append(f"{float(margin)*100:.1f}%" if margin and margin != "N/A" else "N/A")
        rows["Dividend Yield"].append(info.get("dividend_yield", "N/A"))

    df = pd.DataFrame(rows, index=stocks).T
    st.dataframe(df, use_container_width=True)

    # ---- VOLUME COMPARISON ----
    st.subheader("📊 Volume Comparison")
    vol_data = {sym: all_prices[sym].get("volume", 0) for sym in stocks}
    vol_df = pd.DataFrame({"Stock": list(vol_data.keys()), "Volume": list(vol_data.values())})
    vol_df = vol_df.sort_values("Volume", ascending=True)

    fig2 = go.Figure(go.Bar(
        x=vol_df["Volume"],
        y=vol_df["Stock"],
        orientation="h",
        marker_color=CHART_THEME["line_color"],
    ))
    fig2.update_layout(
        paper_bgcolor=CHART_THEME["bg_color"],
        plot_bgcolor=CHART_THEME["bg_color"],
        font=dict(color=CHART_THEME["text_color"]),
        xaxis=dict(gridcolor=CHART_THEME["grid_color"], title="Volume"),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"]),
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig2, use_container_width=True)
