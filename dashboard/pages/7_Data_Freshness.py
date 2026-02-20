"""
Data Freshness — Full overview of data lag and timeliness for all tracked series.
"""

import streamlit as st
import pandas as pd
from datetime import date

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    CN_DESCRIPTIONS, STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS,
    SUPPLY_CN_CODES, DEMAND_CN_CODES, SUPPLY_NACE, DEMAND_NACE,
    TIER1_DATASETS,
)

st.title("Data Freshness & Publication Lag Monitor")
st.caption(
    "Overview of how current each Eurostat data series is. "
    "Eurostat publishes different indicators at different speeds — "
    "this page helps you understand which data is up-to-date and which may be lagged."
)

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

st.markdown("""
### How Eurostat publication lags work

Different data series are published at different speeds after their reference month:

- **Tier 1 — Fast publication (~3 week lag)**: Business confidence indicators (survey-based: ei_bssi, ei_bsrt, ei_bsse)
  and producer price indices (sts_inpp, sts_inpi). These are published quickly because they rely on
  survey responses and price reporting, not hard transaction data.

- **Tier 2 — Standard publication (~6-8 week lag)**: Production indices (sts_inpr), turnover (sts_intv),
  retail trade turnover (sts_trtu), services production (sts_sepr), labour input (sts_inlb),
  new orders (sts_ordi), and all Comext international trade data (DS-045409).
  These require collection and reconciliation of actual economic transactions across all EU member states.

**Example**: If today is February 20, 2026:
- A Tier 1 series should have data up to **January 2026** (~3 weeks ago)
- A Tier 2 series should have data up to **December 2025** (~7 weeks ago)
""")

today = date.today()

# Build freshness table
rows = []
for key, info in data["freshness"].items():
    if info["latest_date"] is None:
        continue

    if key.startswith("comext_"):
        cn_code = key.replace("comext_", "")
        desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
        category = "Comext Trade (DS-045409)"
        side = "Supply" if cn_code in SUPPLY_CN_CODES else "Demand"
        series_name = f"{desc} (CN {cn_code})"
        dataset_id = f"DS-045409 / CN {cn_code}"
    else:
        # STS series — key format: "sts_inpr_m_C17" or "ei_bssi_m_r2_C20"
        # Need to split on the NACE code part
        parts = key.rsplit("_", 1)
        if len(parts) == 2:
            dataset, nace = parts[0], parts[1]
        else:
            dataset, nace = key, ""
        ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
        nace_desc = NACE_DESCRIPTIONS.get(nace, nace)
        category = "STS Industrial Index"
        side = "Supply" if nace in SUPPLY_NACE else ("Demand" if nace in DEMAND_NACE else "Other")
        series_name = f"{ds_desc} — {nace_desc} ({dataset} x {nace})"
        dataset_id = f"{dataset} / {nace}"

    latest = info["latest_date"]
    lag = info["lag_days"]
    tier = info["tier"]

    # Determine status based on lag
    if lag is not None:
        if tier == 1:
            status = "Current" if lag < 45 else ("Lagged" if lag < 90 else "Stale")
        else:
            status = "Current" if lag < 75 else ("Lagged" if lag < 120 else "Stale")
    else:
        status = "Unknown"

    rows.append({
        "Series": series_name,
        "Dataset ID": dataset_id,
        "Category": category,
        "Value Chain": side,
        "Tier": f"Tier {tier}",
        "Expected Lag": "~3 weeks" if tier == 1 else "~6-8 weeks",
        "Latest Data": latest.strftime("%B %Y") if hasattr(latest, "strftime") else str(latest),
        "Lag (days)": lag if lag is not None else 0,
        "Status": status,
    })

df = pd.DataFrame(rows)

if df.empty:
    st.warning("No freshness data available.")
    st.stop()

# ---- Summary metrics ----
st.divider()
st.subheader("Summary — Data Timeliness as of Today")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Series Tracked", len(df))
col2.metric("Tier 1 (Fast, ~3 wk)", len(df[df["Tier"] == "Tier 1"]))
col3.metric("Tier 2 (Standard, ~6-8 wk)", len(df[df["Tier"] == "Tier 2"]))
current_count = len(df[df["Status"] == "Current"])
col4.metric("Series Current", f"{current_count} / {len(df)}")
avg_lag = df["Lag (days)"].mean()
col5.metric("Average Lag", f"{avg_lag:.0f} days")

# Status breakdown
status_counts = df["Status"].value_counts()
st.markdown(
    f"**Status breakdown**: "
    f"{status_counts.get('Current', 0)} Current | "
    f"{status_counts.get('Lagged', 0)} Lagged | "
    f"{status_counts.get('Stale', 0)} Stale"
)
st.caption(
    f"Reference date: {today.strftime('%B %d, %Y')} | "
    "'Current' = within expected publication window | "
    "'Lagged' = moderately behind schedule | "
    "'Stale' = significantly outdated"
)

st.divider()

# ---- Filters ----
st.subheader("Detailed Series Table")
st.caption("Filter and sort to find specific series. Color-coded by publication status.")

col1, col2, col3, col4 = st.columns(4)
cat_filter = col1.selectbox("Filter by data source", ["All"] + sorted(df["Category"].unique().tolist()))
tier_filter = col2.selectbox("Filter by tier", ["All", "Tier 1", "Tier 2"])
status_filter = col3.selectbox("Filter by status", ["All", "Current", "Lagged", "Stale"])
side_filter = col4.selectbox("Filter by value chain", ["All", "Supply", "Demand", "Other"])

filtered = df.copy()
if cat_filter != "All":
    filtered = filtered[filtered["Category"] == cat_filter]
if tier_filter != "All":
    filtered = filtered[filtered["Tier"] == tier_filter]
if status_filter != "All":
    filtered = filtered[filtered["Status"] == status_filter]
if side_filter != "All":
    filtered = filtered[filtered["Value Chain"] == side_filter]

# Color-coded table
def _color_status(val):
    if val == "Current":
        return "background-color: #d4edda; color: #155724"
    elif val == "Lagged":
        return "background-color: #fff3cd; color: #856404"
    elif val == "Stale":
        return "background-color: #f8d7da; color: #721c24"
    return ""


def _color_tier(val):
    if val == "Tier 1":
        return "background-color: #d4edda; color: #155724"
    return "background-color: #fff3cd; color: #856404"


styled = filtered.sort_values(["Status", "Lag (days)"], ascending=[True, False])
st.dataframe(
    styled.style.applymap(_color_status, subset=["Status"]).applymap(_color_tier, subset=["Tier"]),
    use_container_width=True,
    height=min(800, len(styled) * 35 + 40),
)
st.caption(f"Showing {len(filtered)} of {len(df)} series | Sorted by status then lag")

st.divider()

# ---- Distribution chart ----
st.subheader("Publication Lag Distribution — All Tracked Series")
st.caption(
    "Histogram showing how many series fall into each lag bucket. "
    "Tier 1 (green) should cluster around 20-30 days. "
    "Tier 2 (orange) should cluster around 45-60 days."
)

import plotly.express as px

fig = px.histogram(
    df, x="Lag (days)", color="Tier",
    nbins=20, barmode="overlay",
    color_discrete_map={"Tier 1": "#00cc96", "Tier 2": "#ffa15a"},
    title="Distribution of Data Lag Across All Tracked Series (days since latest data)",
    labels={"Lag (days)": "Lag from Today (days)", "count": "Number of Series"},
)
fig.update_layout(
    xaxis_title="Lag from Today (days) — lower is better",
    yaxis_title="Number of Series",
    margin=dict(l=60, r=20, t=40, b=40), height=350,
)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    f"As of {today.strftime('%B %d, %Y')} | "
    "Green = Tier 1 (survey/price data, ~3 week lag) | "
    "Orange = Tier 2 (hard economic/trade data, ~6-8 week lag)"
)

st.divider()

# ---- Supply vs Demand freshness comparison ----
st.subheader("Freshness by Value Chain Position — Supply vs Demand")
st.caption("Average data lag for supply-side vs demand-side series")

for side_label in ["Supply", "Demand"]:
    side_df = df[df["Value Chain"] == side_label]
    if side_df.empty:
        continue
    avg = side_df["Lag (days)"].mean()
    current = len(side_df[side_df["Status"] == "Current"])
    total = len(side_df)
    latest_dates = side_df["Latest Data"].unique()
    st.markdown(
        f"**{side_label} side** — {total} series | "
        f"Average lag: **{avg:.0f} days** | "
        f"{current}/{total} series current"
    )

st.divider()

# ---- Tier explanation ----
st.subheader("Reference — Tier 1 Datasets (Fast Publication, ~3 Week Lag)")
st.caption("These datasets are published approximately 3 weeks after the reference month")
for ds in sorted(TIER1_DATASETS):
    desc = STS_DATASET_DESCRIPTIONS.get(ds, ds)
    st.markdown(f"- **{desc}** (`{ds}`)")

st.subheader("Reference — Tier 2 Datasets (Standard Publication, ~6-8 Week Lag)")
st.caption(
    "All other datasets, including Comext international trade (DS-045409) "
    "and remaining STS indices. Published 6-8 weeks after the reference month."
)
tier2_sts = sorted(set(STS_DATASET_DESCRIPTIONS.keys()) - TIER1_DATASETS)
for ds in tier2_sts:
    desc = STS_DATASET_DESCRIPTIONS.get(ds, ds)
    st.markdown(f"- **{desc}** (`{ds}`)")
st.markdown("- **Comext bilateral trade data** (`DS-045409`) — all CN product codes")

st.divider()
st.caption(
    "This page is auto-generated from the loaded data. "
    "Lag is calculated as the difference between today's date and the latest available data point for each series. "
    "Status thresholds: Tier 1 Current < 45 days, Tier 2 Current < 75 days."
)
