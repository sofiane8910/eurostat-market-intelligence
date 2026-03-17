"""
Dashboard 2 — Application Categories Deep Dive
================================================
STS production indices organized by 10 application categories,
with country-level data. Production / Demand (retail+logistics) split.

Run: streamlit run dashboard2/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Application Categories Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from data_loader2 import load_all_data
from constants2 import APP_CATEGORIES, CATEGORY_NAMES

# Load data once
if "data2" not in st.session_state:
    with st.spinner("Loading Dashboard 2 data..."):
        st.session_state["data2"] = load_all_data()

data = st.session_state["data2"]

# Sidebar info
with st.sidebar:
    st.title("Application Categories")

    n_sts = len(data["sts"])
    st.metric("Total STS Series", n_sts)

    n_yf = data["yf_prices"]["ticker"].nunique() if not data["yf_prices"].empty else 0
    if n_yf:
        st.metric("yfinance Tickers", n_yf)

    # Freshness summary
    st.divider()
    st.subheader("Data Freshness")
    t1 = [v for v in data["freshness"].values() if v["tier"] == 1 and v["latest_date"] is not None]
    t2 = [v for v in data["freshness"].values() if v["tier"] == 2 and v["latest_date"] is not None]
    if t1:
        latest_t1 = max(v["latest_date"] for v in t1)
        st.success(f"Tier 1 (fast): {len(t1)} series, latest {latest_t1.strftime('%b %Y')}")
    if t2:
        latest_t2 = max(v["latest_date"] for v in t2)
        st.warning(f"Tier 2 (lagged): {len(t2)} series, latest {latest_t2.strftime('%b %Y')}")

    st.divider()
    st.caption("Data: Eurostat STS APIs")
    st.caption("Coverage: 2023-01 to present")

# Main landing page
st.title("Application Categories Deep Dive")
st.markdown("""
This dashboard provides market intelligence organized by **10 application
categories** — the end-markets where labelled products are consumed. Each category
maps to specific Eurostat STS industrial indicators (NACE codes).

The dashboard separates data into:
- **Production Side**: Industrial output, turnover, prices, labour, and confidence
- **Demand Side**: Retail turnover and logistics indices
- **Market Proxy**: Stock prices, quarterly financials, and news for major listed end-users per category
""")

# Category overview cards
st.subheader("Categories at a Glance")

row1_cats = CATEGORY_NAMES[:6]
row2_cats = CATEGORY_NAMES[6:]

cols = st.columns(len(row1_cats))
for i, cat in enumerate(row1_cats):
    info = APP_CATEGORIES[cat]
    n_prod = len(info["production_nace"])
    n_retail = len(info["retail_nace"])
    n_log = len(info["logistics_nace"])
    with cols[i]:
        st.markdown(f"**{cat}**")
        st.caption(info["description"])
        parts = []
        if n_prod:
            parts.append(f"{n_prod} production")
        if n_retail:
            parts.append(f"{n_retail} retail")
        if n_log:
            parts.append(f"{n_log} logistics")
        st.markdown(f"_{', '.join(parts)}_" if parts else "_No direct series_")

if row2_cats:
    cols2 = st.columns(len(row2_cats))
    for i, cat in enumerate(row2_cats):
        info = APP_CATEGORIES[cat]
        n_prod = len(info["production_nace"])
        n_retail = len(info["retail_nace"])
        n_log = len(info["logistics_nace"])
        with cols2[i]:
            st.markdown(f"**{cat}**")
            st.caption(info["description"])
            parts = []
            if n_prod:
                parts.append(f"{n_prod} production")
            if n_retail:
                parts.append(f"{n_retail} retail")
            if n_log:
                parts.append(f"{n_log} logistics")
            st.markdown(f"_{', '.join(parts)}_" if parts else "_No direct series_")

# Quick stats
st.divider()
st.subheader("Data Coverage")

c1, c2, c3 = st.columns(3)
sts_prod = [s for s in data["meta"]["sts_series"] if s[5] == "production"]
sts_demand = [s for s in data["meta"]["sts_series"] if s[5] == "demand"]

c1.metric("Production Indices", len(sts_prod))
c2.metric("Demand Indices (Retail + Logistics)", len(sts_demand))
c3.metric("Total STS Series", len(data["meta"]["sts_series"]))
