"""
View: AI Market Intelligence
============================
AI-powered market analysis, suggestions, educational insights
"""

import streamlit as st
from services.factory import get_market_provider, get_news_provider, get_ai_provider
import config


def render():
    st.title("🤖 AI Market Intelligence")
    st.warning("""
    ⚠️ **Educational Only** — All AI analysis here is for learning purposes.
    IMMOTA is NOT SEBI registered. Nothing here is financial advice.
    Always consult a qualified financial advisor before investing.
    """)

    market = get_market_provider()
    news_provider = get_news_provider()
    ai = get_ai_provider()

    tab1, tab2, tab3 = st.tabs(["📊 Market Analysis", "🎓 Investor Education", "🔮 Trend Insights"])

    # ---- TAB 1: FULL MARKET ANALYSIS ----
    with tab1:
        st.subheader("Full Market Analysis")
        st.caption("AI reads latest news + market data and generates an educational summary")

        if st.button("Generate Market Analysis Now", type="primary", key="market_analysis"):
            with st.spinner("AI is analyzing all markets... (takes 10-15 seconds)"):
                market_data = market.get_market_overview()
                news = news_provider.get_market_news("Indian stock market Nifty Sensex", limit=8)
                analysis = ai.analyze_market(market_data, news)
            st.markdown(analysis)
            st.divider()
            st.subheader("📰 News Used for Analysis")
            for article in news[:5]:
                with st.container(border=True):
                    st.write(f"**{article['title']}**")
                    st.caption(f"{article['source']} | {article.get('published_at', '')[:10]}")

    # ---- TAB 2: INVESTOR EDUCATION ----
    with tab2:
        st.subheader("Investor Education")
        st.caption("Ask anything about investing — AI explains in simple language")

        col1, col2 = st.columns(2)
        with col1:
            experience = st.selectbox(
                "Your Experience Level",
                ["Complete Beginner", "Some Knowledge", "Intermediate", "Advanced"],
            )
        with col2:
            topic = st.selectbox(
                "Topic",
                [
                    "How to start investing in India",
                    "What is Nifty 50 and how it works",
                    "Difference between stocks, mutual funds, ETFs",
                    "How to read a company's financial report",
                    "What is P/E ratio and why it matters",
                    "FII vs DII — what does their movement mean",
                    "How to analyze a stock before buying",
                    "Risk management basics",
                    "What is market capitalization",
                    "How does the RBI affect stock markets",
                    "Custom question (type below)",
                ],
            )

        custom_q = ""
        if topic == "Custom question (type below)":
            custom_q = st.text_area("Your question:", placeholder="e.g. What does a 52-week high mean?")

        if st.button("Explain This To Me", type="primary", key="education"):
            question = custom_q if custom_q else topic
            with st.spinner("AI is preparing your educational content..."):
                market_data = market.get_market_overview()
                response = ai.get_investment_suggestion(market_data, experience.lower())
                # Also ask the specific question
                custom_response = ai._call(
                    f"""
                    A {experience} investor wants to understand: "{question}"
                    
                    Explain this clearly:
                    1. Simple definition (no jargon)
                    2. Why it matters for investors
                    3. A real-world Indian market example
                    4. What a beginner should remember
                    
                    Keep it under 300 words. Use simple English.
                    End with: "This is educational content only — not investment advice."
                    """
                ) if hasattr(ai, '_call') else ai.analyze_market({}, [])
            
            st.subheader(f"📚 {question}")
            st.markdown(custom_response)

        st.divider()

        st.subheader("📖 Key Concepts Quick Reference")
        concepts = {
            "P/E Ratio": "Price to Earnings — how much you pay per ₹1 of company profit. Lower can mean cheaper.",
            "Market Cap": "Total value of all shares. Large-cap > ₹20,000Cr, Mid-cap ₹5,000-20,000Cr, Small-cap < ₹5,000Cr",
            "FII": "Foreign Institutional Investors — foreign funds investing in India. Heavy FII buying = bullish signal.",
            "DII": "Domestic Institutional Investors — Indian mutual funds, insurance companies. Stabilize market.",
            "Bull Market": "Prices rising 20%+ from recent lows. Positive sentiment, investors optimistic.",
            "Bear Market": "Prices falling 20%+ from recent highs. Negative sentiment, investors cautious.",
            "Nifty 50": "Index of top 50 companies on NSE. Represents ~65% of free-float market cap.",
            "Circuit Breaker": "NSE/BSE halts trading if market falls 10%, 15%, 20% in a single day.",
        }
        cols = st.columns(2)
        for i, (term, definition) in enumerate(concepts.items()):
            with cols[i % 2]:
                with st.expander(f"📌 {term}"):
                    st.write(definition)

    # ---- TAB 3: TREND INSIGHTS ----
    with tab3:
        st.subheader("Trend Insights")
        st.caption("AI identifies patterns in stock movements — for educational understanding only")

        stocks_to_analyze = st.multiselect(
            "Select stocks to analyze trends",
            config.DEFAULT_STOCKS,
            default=config.DEFAULT_STOCKS[:3],
        )

        if st.button("Analyze Trends", type="primary", key="trends"):
            results = []
            market_provider = get_market_provider()
            progress = st.progress(0)
            for i, sym in enumerate(stocks_to_analyze):
                with st.spinner(f"Analyzing {sym}..."):
                    history = market_provider.get_stock_history(sym, "1mo")
                    if not history.empty:
                        trend = ai.predict_trend(history.to_dict())
                        price_data = market_provider.get_stock_price(sym)
                        results.append({
                            "symbol": sym,
                            "trend": trend,
                            "price": price_data.get("price", 0),
                            "change": price_data.get("change_pct", 0),
                        })
                    progress.progress((i + 1) / len(stocks_to_analyze))

            st.divider()
            st.subheader("Trend Summary (Educational)")
            for r in results:
                direction = r["trend"]["direction"]
                emoji = "📈" if "Up" in direction else "📉" if "Down" in direction else "➡️"
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"**{r['symbol']}**")
                    with col2:
                        st.markdown(f"{emoji} **{direction}**")
                    with col3:
                        st.markdown(f"Confidence: **{r['trend']['confidence']:.0f}%**")
                    with col4:
                        change = r["change"]
                        color = "🟢" if change >= 0 else "🔴"
                        st.markdown(f"{color} **{change:+.2f}%** today")
                    st.caption(r["trend"]["reasoning"])

            st.warning("⚠️ Trend directions above are mathematical patterns for education only — not buy/sell signals.")
