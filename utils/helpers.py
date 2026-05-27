"""
Utility Functions
=================
Shared helpers used across all views.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import functools
import time


# ============================================
# CACHING — reduces API calls significantly
# ============================================

def cache_data(ttl_seconds: int = 300):
    """Simple in-memory cache with TTL"""
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in cache and (now - cache[key]["time"]) < ttl_seconds:
                return cache[key]["value"]
            result = func(*args, **kwargs)
            cache[key] = {"value": result, "time": now}
            return result
        return wrapper
    return decorator


# ============================================
# NUMBER FORMATTERS
# ============================================

def format_number(n) -> str:
    if n is None or n == "N/A":
        return "N/A"
    try:
        n = float(n)
        if n >= 1_00_00_00_000:    # 100 Cr+
            return f"₹{n/1_00_00_00_000:.2f}T"
        elif n >= 1_00_00_000:     # 1 Cr+
            return f"₹{n/1_00_00_000:.2f}Cr"
        elif n >= 1_00_000:        # 1 Lakh+
            return f"₹{n/1_00_000:.2f}L"
        else:
            return f"₹{n:,.2f}"
    except:
        return str(n)


def format_large_usd(n) -> str:
    if n is None:
        return "N/A"
    try:
        n = float(n)
        if n >= 1_000_000_000_000:
            return f"${n/1_000_000_000_000:.2f}T"
        elif n >= 1_000_000_000:
            return f"${n/1_000_000_000:.2f}B"
        elif n >= 1_000_000:
            return f"${n/1_000_000:.2f}M"
        else:
            return f"${n:,.2f}"
    except:
        return str(n)


def format_change(change_pct: float) -> str:
    if change_pct is None:
        return "N/A"
    arrow = "▲" if change_pct >= 0 else "▼"
    color = "🟢" if change_pct >= 0 else "🔴"
    return f"{color} {arrow} {abs(change_pct):.2f}%"


def get_change_color(change_pct: float) -> str:
    return "#00C851" if change_pct >= 0 else "#FF4444"


# ============================================
# PLOTLY CHART BUILDERS
# ============================================

CHART_THEME = {
    "bg_color": "#0E1117",
    "grid_color": "#1E2130",
    "text_color": "#FAFAFA",
    "up_color": "#00C851",
    "down_color": "#FF4444",
    "line_color": "#4FC3F7",
}


def make_candlestick_chart(df: pd.DataFrame, title: str = "") -> go.Figure:
    """Standard OHLC candlestick chart"""
    if df.empty:
        return go.Figure()

    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color=CHART_THEME["up_color"],
            decreasing_line_color=CHART_THEME["down_color"],
            name="Price",
        )
    ])

    if "Volume" in df.columns:
        fig.add_trace(go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume",
            yaxis="y2",
            marker_color="rgba(79, 195, 247, 0.3)",
        ))
        fig.update_layout(yaxis2=dict(
            overlaying="y", side="right", showgrid=False, title="Volume"
        ))

    fig.update_layout(
        title=title,
        paper_bgcolor=CHART_THEME["bg_color"],
        plot_bgcolor=CHART_THEME["bg_color"],
        font=dict(color=CHART_THEME["text_color"]),
        xaxis=dict(gridcolor=CHART_THEME["grid_color"], showgrid=True),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"], showgrid=True),
        xaxis_rangeslider_visible=False,
        height=450,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig


def make_line_chart(df: pd.DataFrame, y_col: str = "price", title: str = "") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index if hasattr(df.index, 'dtype') else df.get("date", df.index),
        y=df[y_col] if y_col in df.columns else df.iloc[:, 0],
        mode="lines",
        line=dict(color=CHART_THEME["line_color"], width=2),
        fill="tozeroy",
        fillcolor="rgba(79, 195, 247, 0.1)",
    ))
    fig.update_layout(
        title=title,
        paper_bgcolor=CHART_THEME["bg_color"],
        plot_bgcolor=CHART_THEME["bg_color"],
        font=dict(color=CHART_THEME["text_color"]),
        xaxis=dict(gridcolor=CHART_THEME["grid_color"]),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"]),
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
    )
    return fig


def make_metric_card(label: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Streamlit metric card wrapper"""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


# ============================================
# SEBI DISCLAIMER
# ============================================

def show_sebi_disclaimer():
    """Shows SEBI disclaimer — call once per session"""
    if "sebi_accepted" not in st.session_state:
        st.session_state.sebi_accepted = False

    if not st.session_state.sebi_accepted:
        with st.container():
            st.warning("""
            ## ⚠️ Important Disclaimer — Please Read

            **IMMOTA is NOT registered with SEBI (Securities and Exchange Board of India).**

            - This platform is for **educational and informational purposes ONLY**
            - Nothing here constitutes financial advice, investment advice, or trading recommendations
            - AI-generated analysis is for learning purposes — it is NOT a buy/sell signal
            - Past performance data shown does not guarantee future results
            - Always consult a SEBI-registered financial advisor before investing
            - You are solely responsible for your investment decisions

            By clicking "I Understand", you acknowledge this is an educational tool only.
            """)
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("✅ I Understand", type="primary", use_container_width=True):
                    st.session_state.sebi_accepted = True
                    st.rerun()
            with col2:
                st.caption("You must accept to use IMMOTA")
        st.stop()
