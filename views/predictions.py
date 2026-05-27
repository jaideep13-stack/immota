"""
View: Investor Predictions
===========================
Community section — users post predictions, others rate them
Stored in session state (no database needed for MVP)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os


PREDICTIONS_FILE = "predictions_store.json"


def _load_predictions() -> list:
    if os.path.exists(PREDICTIONS_FILE):
        try:
            with open(PREDICTIONS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return _get_sample_predictions()


def _save_predictions(predictions: list):
    with open(PREDICTIONS_FILE, "w") as f:
        json.dump(predictions, f, indent=2, default=str)


def _get_sample_predictions() -> list:
    return [
        {
            "id": 1,
            "author": "BigBullRohit",
            "symbol": "RELIANCE.NS",
            "direction": "Bullish 📈",
            "target_price": 3200,
            "timeframe": "3 months",
            "reasoning": "Strong Q3 results expected. Jio subscribers growing. Retail business expanding.",
            "votes_up": 24,
            "votes_down": 5,
            "timestamp": "2024-01-15",
            "verified": False,
        },
        {
            "id": 2,
            "author": "TechAnalystPriya",
            "symbol": "TCS.NS",
            "direction": "Neutral ➡️",
            "target_price": 4100,
            "timeframe": "1 month",
            "reasoning": "IT sector facing headwinds from US slowdown. Deal wins are good but margin pressure continues.",
            "votes_up": 18,
            "votes_down": 7,
            "timestamp": "2024-01-14",
            "verified": False,
        },
        {
            "id": 3,
            "author": "CryptoKingArjun",
            "symbol": "BTC/USD",
            "direction": "Bullish 📈",
            "target_price": 65000,
            "timeframe": "6 months",
            "reasoning": "BTC ETF approval in US is massive. Halving event in April 2024. Institutional demand rising.",
            "votes_up": 41,
            "votes_down": 12,
            "timestamp": "2024-01-13",
            "verified": False,
        },
    ]


def render():
    st.title("👥 Investor Predictions")
    st.warning("""
    ⚠️ **Community Content — NOT Financial Advice**
    Predictions are user opinions for educational discussion only.
    IMMOTA does not verify these predictions. Do NOT invest based on them.
    """)

    predictions = _load_predictions()

    tab1, tab2, tab3 = st.tabs(["📋 All Predictions", "➕ Add Prediction", "🏆 Leaderboard"])

    # ---- TAB 1: VIEW PREDICTIONS ----
    with tab1:
        st.subheader("Community Predictions")

        col1, col2, col3 = st.columns(3)
        with col1:
            filter_direction = st.selectbox("Filter by", ["All", "Bullish 📈", "Bearish 📉", "Neutral ➡️"])
        with col2:
            sort_by = st.selectbox("Sort by", ["Most Upvoted", "Latest", "Most Discussed"])
        with col3:
            search_sym = st.text_input("Search symbol", placeholder="e.g. TCS, BTC")

        # Apply filters
        filtered = predictions
        if filter_direction != "All":
            filtered = [p for p in filtered if p["direction"] == filter_direction]
        if search_sym:
            filtered = [p for p in filtered if search_sym.upper() in p["symbol"].upper()]

        if not filtered:
            st.info("No predictions match your filters.")
            return

        for pred in filtered:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"### {pred['symbol']} — {pred['direction']}")
                    st.caption(f"By **{pred['author']}** | Target: ₹{pred['target_price']:,} | Timeframe: {pred['timeframe']}")
                with col2:
                    st.metric("Target", f"₹{pred['target_price']:,}")
                with col3:
                    st.caption(f"📅 {pred['timestamp']}")

                st.write(pred["reasoning"])

                vote_col1, vote_col2, vote_col3 = st.columns([1, 1, 4])
                with vote_col1:
                    if st.button(f"👍 {pred['votes_up']}", key=f"up_{pred['id']}"):
                        pred["votes_up"] += 1
                        _save_predictions(predictions)
                        st.rerun()
                with vote_col2:
                    if st.button(f"👎 {pred['votes_down']}", key=f"down_{pred['id']}"):
                        pred["votes_down"] += 1
                        _save_predictions(predictions)
                        st.rerun()
                with vote_col3:
                    total = pred["votes_up"] + pred["votes_down"]
                    accuracy = (pred["votes_up"] / total * 100) if total > 0 else 50
                    st.caption(f"Community agreement: {accuracy:.0f}%")

    # ---- TAB 2: ADD PREDICTION ----
    with tab2:
        st.subheader("Share Your Prediction")
        st.caption("Share your market view for educational community discussion")

        with st.form("add_prediction"):
            col1, col2 = st.columns(2)
            with col1:
                author_name = st.text_input("Your Name / Handle", placeholder="e.g. BullishTrader99")
                symbol = st.text_input("Stock/Crypto Symbol", placeholder="e.g. RELIANCE.NS, BTC/USD")
            with col2:
                direction = st.selectbox("Your Prediction", ["Bullish 📈", "Bearish 📉", "Neutral ➡️"])
                timeframe = st.selectbox("Timeframe", ["1 week", "2 weeks", "1 month", "3 months", "6 months", "1 year"])

            target_price = st.number_input("Target Price (₹ or $)", min_value=0.0, step=10.0)
            reasoning = st.text_area(
                "Your Reasoning",
                placeholder="Explain why you think this — fundamentals, technicals, news catalyst...",
                max_chars=500,
            )

            agreed_disclaimer = st.checkbox(
                "I understand this is for educational discussion only and not financial advice"
            )

            submitted = st.form_submit_button("Post Prediction", type="primary")
            if submitted:
                if not all([author_name, symbol, reasoning, agreed_disclaimer]):
                    st.error("Fill all fields and accept the disclaimer.")
                else:
                    new_pred = {
                        "id": len(predictions) + 1,
                        "author": author_name,
                        "symbol": symbol.upper(),
                        "direction": direction,
                        "target_price": target_price,
                        "timeframe": timeframe,
                        "reasoning": reasoning,
                        "votes_up": 0,
                        "votes_down": 0,
                        "timestamp": datetime.now().strftime("%Y-%m-%d"),
                        "verified": False,
                    }
                    predictions.append(new_pred)
                    _save_predictions(predictions)
                    st.success("Prediction posted! Go to 'All Predictions' to see it.")

    # ---- TAB 3: LEADERBOARD ----
    with tab3:
        st.subheader("Community Leaderboard")
        st.caption("Based on community upvotes on predictions")

        if not predictions:
            st.info("No predictions yet. Be the first!")
            return

        df = pd.DataFrame(predictions)
        df["Net Score"] = df["votes_up"] - df["votes_down"]
        df["Total Votes"] = df["votes_up"] + df["votes_down"]
        df["Agreement %"] = df.apply(
            lambda r: f"{r['votes_up']/r['Total Votes']*100:.0f}%" if r["Total Votes"] > 0 else "0%",
            axis=1
        )

        leaderboard = df[["author", "symbol", "direction", "Net Score", "Agreement %", "timestamp"]].copy()
        leaderboard.columns = ["Analyst", "Symbol", "Call", "Score", "Agreement", "Date"]
        leaderboard = leaderboard.sort_values("Score", ascending=False)

        st.dataframe(leaderboard, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("📊 Prediction Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Predictions", len(predictions))
        with col2:
            bullish = len([p for p in predictions if "Bullish" in p["direction"]])
            st.metric("Bullish Calls", bullish)
        with col3:
            bearish = len([p for p in predictions if "Bearish" in p["direction"]])
            st.metric("Bearish Calls", bearish)
