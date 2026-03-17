"""
Data Freshness — Monitor data recency for all Dashboard 2 series.
"""

import streamlit as st
import pandas as pd
import re

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dashboard"))

from constants2 import (
    NACE_DISPLAY_NAMES, DATASET_DISPLAY_NAMES, STS_DATASET_DESCRIPTIONS,
    freshness_footnote,
)
from charts import freshness_badge

st.title("Data Freshness Monitor")
st.caption("Overview of data recency across all STS series in Dashboard 2")

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

freshness = data["freshness"]

if not freshness:
    st.warning("No freshness data available.")
    st.stop()

# Build freshness table
rows = []
for key, fr in sorted(freshness.items()):
    m = re.match(r"(.+)_((?:C|G|H)\w*)$", key)
    if m:
        dataset, nace = m.group(1), m.group(2)
    else:
        continue
    ds_display = DATASET_DISPLAY_NAMES.get(dataset, dataset)
    nace_display = NACE_DISPLAY_NAMES.get(nace, nace)
    display_name = f"{ds_display} \u2014 {nace_display}"
    technical = f"{dataset} x {nace}"

    latest = fr.get("latest_date")
    rows.append({
        "Series": display_name,
        "Tier": fr.get("tier", 2),
        "Latest Data": latest.strftime("%b %Y") if latest else "N/A",
        "Lag (days)": fr.get("lag_days", "N/A"),
        "Technical ID": technical,
    })

df = pd.DataFrame(rows)

# Summary metrics
col1, col2, col3 = st.columns(3)
t1_count = len(df[df["Tier"] == 1])
t2_count = len(df[df["Tier"] == 2])
total = len(df)
col1.metric("Total Series", total)
col2.metric("Tier 1 (fast, ~3 week lag)", t1_count)
col3.metric("Tier 2 (lagged, ~6-8 weeks)", t2_count)

# Tier 1 and Tier 2 tables
st.subheader("Tier 1 Series (Survey / Prices)")
st.caption("These series are typically published within ~3 weeks of the reference month")
t1_df = df[df["Tier"] == 1].drop(columns=["Tier"]).reset_index(drop=True)
if not t1_df.empty:
    st.dataframe(t1_df, use_container_width=True, hide_index=True)
else:
    st.info("No Tier 1 series found.")

st.subheader("Tier 2 Series (Hard Economic Data)")
st.caption("These series are typically published with a ~6-8 week lag")
t2_df = df[df["Tier"] == 2].drop(columns=["Tier"]).reset_index(drop=True)
if not t2_df.empty:
    st.dataframe(t2_df, use_container_width=True, hide_index=True)
else:
    st.info("No Tier 2 series found.")

st.divider()
st.caption(
    "Tier 1 = confidence indicators, price indices (fast release). "
    "Tier 2 = production, turnover, labour data (slower release)."
)
