"""
View: News Hub
==============
Real-time financial news from all markets
"""

import streamlit as st
from services.factory import get_news_provider


NEWS_CATEGORIES = {
    "🇮🇳 Indian Markets": "Indian stock market NSE BSE Nifty Sensex",
    "🏦 Banking & Finance": "RBI banking India interest rates NBFC",
    "💹 Economy": "India economy GDP inflation rupee",
    "🌍 Global Markets": "global stock market US Fed interest rates",
    "₿ Crypto": "cryptocurrency bitcoin ethereum blockchain",
    "🏭 Sectors": "IT pharma auto FMCG India sector",
    "📊 IPO": "IPO India listing new share offer",
    "🏢 Company Results": "quarterly results profit earnings India company",
}


def render():
    st.title("📰 News Hub")
    st.caption("Real-time financial and market news — updated every refresh")

    news_provider = get_news_provider()

    # ---- SEARCH ----
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Search News",
            placeholder="e.g. Reliance results, RBI rate cut, Bitcoin rally",
        )
    with col2:
        num_articles = st.selectbox("Articles", [5, 10, 15, 20], index=1)

    if search_query:
        with st.spinner(f"Searching news for '{search_query}'..."):
            articles = news_provider.get_market_news(search_query, limit=num_articles)
        st.subheader(f"Results for: {search_query}")
        _render_news_grid(articles)
        return

    # ---- CATEGORY TABS ----
    tab_names = list(NEWS_CATEGORIES.keys())
    tabs = st.tabs(tab_names)

    for tab, (category, query) in zip(tabs, NEWS_CATEGORIES.items()):
        with tab:
            with st.spinner(f"Loading {category} news..."):
                articles = news_provider.get_market_news(query=query, limit=num_articles)
            _render_news_grid(articles)


def _render_news_grid(articles: list):
    if not articles:
        st.info("No news available. Try adding NEWS_API_KEY in .env for full news access.")
        st.caption("Without API key, news comes from Economic Times RSS feed.")
        return

    for i in range(0, len(articles), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(articles):
                article = articles[i + j]
                with col:
                    with st.container(border=True):
                        title = article.get("title", "No title")
                        st.markdown(f"**{title[:120]}**")

                        meta_parts = []
                        if article.get("source"):
                            meta_parts.append(f"🗞 {article['source']}")
                        if article.get("published_at"):
                            date_str = article["published_at"][:10]
                            meta_parts.append(f"📅 {date_str}")
                        if meta_parts:
                            st.caption(" | ".join(meta_parts))

                        desc = article.get("description", "")
                        if desc and len(desc) > 10:
                            st.caption(desc[:150] + "..." if len(desc) > 150 else desc)

                        if article.get("url"):
                            st.link_button("Read Full Article →", article["url"])
