"""
Eurostat Labels Market Dashboard
================================
Interactive dashboard for European PSA labels market intelligence.
Supply-side (materials) and demand-side (end-markets) with bilateral trade analysis.

Run: streamlit run dashboard/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Eurostat Labels Market",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import after page config
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from data_loader import load_all_data

# Load data once
if "data" not in st.session_state:
    with st.spinner("Loading all Eurostat data..."):
        st.session_state["data"] = load_all_data()

data = st.session_state["data"]

# Sidebar info
with st.sidebar:
    st.title("Eurostat Labels Market")

    n_comext = len(data["comext"])
    n_sts = len(data["sts"])
    st.metric("Total Series", n_comext + n_sts)
    col1, col2 = st.columns(2)
    col1.metric("Comext Trade", n_comext)
    col2.metric("STS Indices", n_sts)

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
    st.caption("Data: Eurostat Comext & STS APIs")
    st.caption("Coverage: 2023-01 to present")

# Main landing page
st.title("European Labels Market Intelligence")
st.markdown("""
This dashboard provides comprehensive market intelligence for the European
pressure-sensitive adhesive (PSA) labels industry, covering both:

- **Supply side**: Raw materials, films, adhesives, inks, and labels trade & production
- **Demand side**: End-market sectors — food, beverages, HPC, pharma, logistics

Navigate using the sidebar to explore:
""")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Analysis Pages**
    - **Executive Summary** — KPIs, trends, freshness
    - **Supply Side** — Materials trade & industrial indices
    - **Demand Side** — End-market trade, retail & logistics
    - **Trade Balance & China** — Bilateral analysis, China competition
    """)
with col2:
    st.markdown("""
    **Deep Dive Pages**
    - **Country Deep Dive** — All indicators for one country
    - **Sector Explorer** — Cross-indicator sector view
    - **Data Freshness** — Full lag/status overview
    """)

# Quick stats
st.divider()
st.subheader("Quick Overview")

c1, c2, c3, c4 = st.columns(4)
supply_comext = [c for c in data["meta"]["comext_codes"] if c[2] == "supply"]
demand_comext = [c for c in data["meta"]["comext_codes"] if c[2] == "demand"]
supply_sts = [s for s in data["meta"]["sts_series"] if s[4] == "supply"]
demand_sts = [s for s in data["meta"]["sts_series"] if s[4] == "demand"]

c1.metric("Supply Trade Series", len(supply_comext))
c2.metric("Supply STS Indices", len(supply_sts))
c3.metric("Demand Trade Series", len(demand_comext))
c4.metric("Demand STS Indices", len(demand_sts))
