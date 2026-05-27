"""
View: Settings
==============
API key setup, watchlist management, app preferences
"""

import streamlit as st
import os
import config


def render():
    st.title("⚙️ Settings")

    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "⭐ Watchlist", "ℹ️ About"])

    # ---- TAB 1: API KEYS ----
    with tab1:
        st.subheader("API Key Setup")
        st.caption("Add your free API keys to unlock full features")

        with st.expander("🤖 Groq API Key (AI Analysis)", expanded=True):
            st.markdown("""
            **Why needed:** Powers all AI market analysis, stock insights, and educational content
            
            **How to get (FREE):**
            1. Go to [console.groq.com](https://console.groq.com)
            2. Sign up for free
            3. Create API key
            4. Add below
            """)
            groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
            if st.button("Save Groq Key"):
                _save_env_key("GROQ_API_KEY", groq_key)
                st.success("Saved! Restart app for changes to take effect.")

        with st.expander("📰 NewsAPI Key (Full News Access)"):
            st.markdown("""
            **Why needed:** Gives 100 fresh news requests/day. Without it, falls back to ET RSS.
            
            **How to get (FREE):**
            1. Go to [newsapi.org](https://newsapi.org)
            2. Register free account
            3. Copy API key
            """)
            news_key = st.text_input("News API Key", type="password", placeholder="abc123...")
            if st.button("Save News Key"):
                _save_env_key("NEWS_API_KEY", news_key)
                st.success("Saved! Restart app for changes to take effect.")

        st.divider()
        st.subheader("🔒 Current Key Status")
        col1, col2 = st.columns(2)
        with col1:
            groq_status = "✅ Set" if config.GROQ_API_KEY else "❌ Missing"
            st.metric("Groq API", groq_status)
        with col2:
            news_status = "✅ Set" if config.NEWS_API_KEY else "❌ Missing (using RSS)"
            st.metric("NewsAPI", news_status)

        st.divider()
        st.subheader("🚀 Paid API Upgrade Path")
        st.markdown("""
        When you're ready to upgrade from free to production-grade data:
        
        | Provider | What You Get | Monthly Cost |
        |----------|-------------|-------------|
        | Polygon.io | Real-time US stocks, 15 min delay for free | ~$29 |
        | CoinMarketCap | 5-min crypto data, better reliability | ~$79 |
        | OANDA | Real-time Forex with spreads | ~$50 |
        | NewsAPI Pro | 500 req/day, full article content | ~$449 |
        | Bloomberg B-PIPE | Institutional real-time data | ~$2,000 |
        
        To upgrade: change ONE line in `config.py` — that's all.
        """)

    # ---- TAB 2: WATCHLIST ----
    with tab2:
        st.subheader("Manage Your Watchlist")

        if "watchlist" not in st.session_state:
            st.session_state.watchlist = config.DEFAULT_STOCKS[:4]

        st.caption("These stocks appear on your dashboard watchlist")

        col1, col2 = st.columns([3, 1])
        with col1:
            new_sym = st.text_input("Add symbol", placeholder="e.g. HCLTECH.NS, TSLA")
        with col2:
            if st.button("Add", type="primary") and new_sym:
                sym = new_sym.upper().strip()
                if sym not in st.session_state.watchlist:
                    st.session_state.watchlist.append(sym)
                    st.success(f"Added {sym}")
                    st.rerun()

        st.write("**Current Watchlist:**")
        for i, sym in enumerate(st.session_state.watchlist):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {sym}")
            with col2:
                if st.button("Remove", key=f"rm_{i}"):
                    st.session_state.watchlist.remove(sym)
                    st.rerun()

        st.caption("Tip: Use .NS suffix for NSE stocks (RELIANCE.NS), .BO for BSE")

    # ---- TAB 3: ABOUT ----
    with tab3:
        st.subheader("About IMMOTA")
        st.markdown(f"""
        ### {config.APP_NAME}
        **{config.APP_TAGLINE}**
        
        ---
        
        **What is IMMOTA?**
        
        IMMOTA is an AI-powered market intelligence platform for educational purposes.
        It aggregates data from Indian and global markets, provides AI-generated insights,
        and helps users understand financial markets better.
        
        **Tech Stack:**
        - Frontend: Streamlit
        - Data: Yahoo Finance, CoinGecko, ExchangeRate-API
        - News: NewsAPI / Economic Times RSS
        - AI Analysis: Groq (LLaMA 3)
        
        **Legal:**
        
        ⚠️ IMMOTA is NOT registered with SEBI or any financial regulatory authority.
        All content is for educational and informational purposes only.
        Nothing on this platform constitutes financial, investment, or trading advice.
        Users are solely responsible for their investment decisions.
        
        **Version:** 1.0.0  
        **Built with:** Python + Streamlit  
        """)

        if st.button("🔄 Reset Disclaimer (Show Again)"):
            st.session_state.sebi_accepted = False
            st.rerun()


def _save_env_key(key: str, value: str):
    """Write key to .env file"""
    env_path = ".env"
    lines = []
    key_found = False

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)

    if not key_found:
        new_lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)
