"""
IMMOTA — Intelligent Market Intelligence Platform
==================================================
Main entry point.

Run locally:   streamlit run app.py
Deploy:        Push to GitHub → Deploy on Streamlit Cloud (share.streamlit.io)
"""

import streamlit as st
from utils.helpers import show_sebi_disclaimer

# ============================================
# PAGE CONFIG — Must be first Streamlit call
# ============================================
st.set_page_config(
    page_title="IMMOTA — Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "IMMOTA — AI-Powered Market Intelligence Platform. For educational purposes only.",
        "Report a bug": None,
        "Get Help": None,
    },
)

# ============================================
# GLOBAL STYLES
# ============================================
st.markdown("""
<style>
    /* Dark theme refinements */
    .stApp { background-color: #0E1117; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161B22; }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #21262D;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Positive metric delta */
    [data-testid="stMetricDelta"] svg { display: none; }
    
    /* Containers */
    [data-testid="stVerticalBlock"] > div:has([data-testid="stContainer"]) {
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #161B22; }
    ::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
    
    /* Links */
    a { color: #4FC3F7 !important; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #161B22; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #8B949E; }
    .stTabs [aria-selected="true"] { color: #4FC3F7 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================
# SEBI DISCLAIMER — First visit only
# ============================================
show_sebi_disclaimer()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("## 📊 IMMOTA")
    st.caption("Market Intelligence Platform")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔍 Stock Analysis",
            "₿ Crypto Markets",
            "💱 Forex",
            "🤖 AI Intelligence",
            "📰 News Hub",
            "⚖️ Comparator",
            "👥 Predictions",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    # Quick market status
    st.caption("📡 Data Sources")
    st.caption("• Stocks: Yahoo Finance (Free)")
    st.caption("• Crypto: CoinGecko (Free)")
    st.caption("• Forex: ExchangeRate API (Free)")
    st.caption("• AI: Groq LLaMA 3 (Free)")
    st.caption("• News: NewsAPI / ET RSS (Free)")

    st.divider()
    st.caption("⚠️ Educational use only")
    st.caption("Not SEBI registered")
    st.caption("Not financial advice")

# ============================================
# PAGE ROUTING
# ============================================
if page == "🏠 Dashboard":
    from views.dashboard import render
    render()

elif page == "🔍 Stock Analysis":
    from views.stock_analysis import render
    render()

elif page == "₿ Crypto Markets":
    from views.crypto import render
    render()

elif page == "💱 Forex":
    from views.forex import render
    render()

elif page == "🤖 AI Intelligence":
    from views.ai_intelligence import render
    render()

elif page == "📰 News Hub":
    from views.news import render
    render()

elif page == "⚖️ Comparator":
    from views.screener import render
    render()

elif page == "👥 Predictions":
    from views.predictions import render
    render()

elif page == "⚙️ Settings":
    from views.settings import render
    render()
