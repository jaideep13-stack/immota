"""
View: Forex Markets
===================
Currency exchange rates, INR pairs, global forex
"""

import streamlit as st
import pandas as pd
from services.factory import get_forex_provider, get_ai_provider, get_news_provider
from utils.helpers import make_line_chart


CURRENCY_INFO = {
    "INR": "🇮🇳 Indian Rupee",
    "USD": "🇺🇸 US Dollar",
    "EUR": "🇪🇺 Euro",
    "GBP": "🇬🇧 British Pound",
    "JPY": "🇯🇵 Japanese Yen",
    "AUD": "🇦🇺 Australian Dollar",
    "CAD": "🇨🇦 Canadian Dollar",
    "SGD": "🇸🇬 Singapore Dollar",
    "AED": "🇦🇪 UAE Dirham",
    "CNY": "🇨🇳 Chinese Yuan",
    "CHF": "🇨🇭 Swiss Franc",
}


def render():
    st.title("💱 Forex Markets")
    st.caption("Live currency exchange rates — focus on INR pairs")

    forex = get_forex_provider()
    ai = get_ai_provider()
    news_provider = get_news_provider()

    # ---- INR PAIRS ----
    st.subheader("🇮🇳 INR Exchange Rates")
    st.caption("How much 1 unit of foreign currency = in Indian Rupees")

    with st.spinner("Loading forex rates..."):
        rates_data = forex.get_all_rates(base="USD")

    if "error" not in rates_data:
        inr_rate = rates_data["rates"].get("INR", 83)

        major_currencies = ["EUR", "GBP", "JPY", "AUD", "CAD", "SGD", "AED", "CHF"]
        usd_rates = rates_data["rates"]

        rows = []
        for currency in major_currencies:
            if currency in usd_rates and "INR" in usd_rates:
                usd_to_target = usd_rates.get(currency, 1)
                inr_per_unit = inr_rate / usd_to_target if usd_to_target else 0
                rows.append({
                    "Currency": CURRENCY_INFO.get(currency, currency),
                    "Code": currency,
                    f"1 {currency} = INR": f"₹{inr_per_unit:,.4f}",
                    f"1 INR = {currency}": f"{1/inr_per_unit:.6f}" if inr_per_unit else "N/A",
                })

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

        # USD/INR highlight
        st.info(f"💵 Current USD/INR Rate: **₹{inr_rate:,.2f}**")
    else:
        st.error("Forex data unavailable. Try again later.")

    st.divider()

    # ---- CURRENCY CONVERTER ----
    st.subheader("🔄 Currency Converter")

    col1, col2, col3 = st.columns(3)
    with col1:
        amount = st.number_input("Amount", min_value=0.01, value=100.0, step=10.0)
    with col2:
        from_currency = st.selectbox("From", list(CURRENCY_INFO.keys()), index=1)
    with col3:
        to_currency = st.selectbox("To", list(CURRENCY_INFO.keys()), index=0)

    if st.button("Convert", type="primary"):
        with st.spinner("Fetching rate..."):
            result = forex.get_rate(from_currency, to_currency)
        if result.get("rate"):
            converted = amount * result["rate"]
            st.success(f"**{amount:,.2f} {from_currency} = {converted:,.4f} {to_currency}**")
            st.caption(f"Rate: 1 {from_currency} = {result['rate']} {to_currency}")
        else:
            st.error("Conversion failed. Try again.")

    st.divider()

    # ---- ALL RATES TABLE ----
    st.subheader("📊 USD Base Rates (All Major Currencies)")

    if "error" not in rates_data:
        all_rates = rates_data.get("rates", {})
        display_currencies = list(CURRENCY_INFO.keys())
        rows = []
        for curr in display_currencies:
            if curr in all_rates:
                rows.append({
                    "Currency": CURRENCY_INFO.get(curr, curr),
                    "Code": curr,
                    "Rate vs USD": f"{all_rates[curr]:.4f}",
                })
        if rows:
            df2 = pd.DataFrame(rows)
            st.dataframe(df2, use_container_width=True, hide_index=True)
        st.caption(f"Last updated: {rates_data.get('last_updated', 'N/A')}")

    st.divider()

    # ---- FOREX NEWS ----
    st.subheader("📰 Forex & Economy News")
    with st.spinner("Loading news..."):
        forex_news = news_provider.get_market_news("forex currency exchange rate India RBI", limit=4)

    for article in forex_news:
        with st.container(border=True):
            st.markdown(f"**{article['title']}**")
            st.caption(f"🗞 {article['source']} | {article.get('published_at', '')[:10]}")
            if article.get("url"):
                st.link_button("Read →", article["url"])

    st.divider()

    # ---- AI FOREX ANALYSIS ----
    st.subheader("🤖 AI Forex Insight (Educational)")
    if st.button("Generate Forex Analysis", type="primary"):
        with st.spinner("Analyzing forex market..."):
            forex_context = {"rates": rates_data, "usd_inr": inr_rate if "error" not in rates_data else "N/A"}
            analysis = ai.analyze_market(forex_context, forex_news)
        st.markdown(analysis)
