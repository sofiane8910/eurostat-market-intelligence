"""
Overview — KPI cards for all 10 application categories with sparklines.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dashboard"))

from constants2 import (
    APP_CATEGORIES, CATEGORY_NAMES,
    NACE_DISPLAY_NAMES, DATASET_DISPLAY_NAMES, AGGREGATE_CODES,
)
from charts import sparkline

st.title("Application Categories Overview")
st.caption(
    "Key performance indicators across 10 application categories. "
    "Each card shows the latest production, retail, and logistics data with trend sparklines."
)

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# Build KPI cards for each category
for cat_name in CATEGORY_NAMES:
    info = APP_CATEGORIES[cat_name]
    st.subheader(cat_name)
    st.caption(info["description"])

    cols = st.columns(4)
    col_idx = 0

    # Production KPIs: latest value for main production NACE
    for nace in info["production_nace"]:
        key = f"sts_inpr_m_{nace}"
        if key not in data["sts"]:
            continue
        sdf = data["sts"][key]
        monthly = sdf.groupby("date")["value"].mean().sort_index()
        if monthly.empty:
            continue
        latest_val = monthly.iloc[-1]
        latest_date = monthly.index[-1]
        nace_name = NACE_DISPLAY_NAMES.get(nace, nace)

        with cols[col_idx % 4]:
            st.metric(
                f"{nace_name} Production",
                f"{latest_val:.1f}",
                help=f"Production volume index (EU avg), {nace}",
            )
            if len(monthly) >= 3:
                st.plotly_chart(sparkline(monthly.tail(12).tolist(), color="#1f77b4"),
                                use_container_width=True, key=f"spark_prod_{cat_name}_{nace}")
            st.caption(f"sts_inpr_m x {nace} | {latest_date.strftime('%b %Y')}")
        col_idx += 1

    # Producer prices KPI
    for nace in info["production_nace"]:
        key = f"sts_inpp_m_{nace}"
        if key not in data["sts"]:
            continue
        sdf = data["sts"][key]
        monthly = sdf.groupby("date")["value"].mean().sort_index()
        if monthly.empty:
            continue
        latest_val = monthly.iloc[-1]
        latest_date = monthly.index[-1]
        nace_name = NACE_DISPLAY_NAMES.get(nace, nace)

        with cols[col_idx % 4]:
            st.metric(
                f"{nace_name} Prices",
                f"{latest_val:.1f}",
                help=f"Producer prices index (EU avg), {nace}",
            )
            if len(monthly) >= 3:
                st.plotly_chart(sparkline(monthly.tail(12).tolist(), color="#00cc96"),
                                use_container_width=True, key=f"spark_price_{cat_name}_{nace}")
            st.caption(f"sts_inpp_m x {nace} | {latest_date.strftime('%b %Y')}")
        col_idx += 1

    # Retail KPIs
    for nace in info["retail_nace"][:1]:
        key = f"sts_trtu_m_{nace}"
        if key not in data["sts"]:
            continue
        sdf = data["sts"][key]
        monthly = sdf.groupby("date")["value"].mean().sort_index()
        if monthly.empty:
            continue
        latest_val = monthly.iloc[-1]
        latest_date = monthly.index[-1]
        nace_name = NACE_DISPLAY_NAMES.get(nace, nace)

        with cols[col_idx % 4]:
            st.metric(
                f"{nace_name}",
                f"{latest_val:.1f}",
                help=f"Retail turnover index (EU avg), {nace}",
            )
            if len(monthly) >= 3:
                st.plotly_chart(sparkline(monthly.tail(12).tolist(), color="#ffa15a"),
                                use_container_width=True, key=f"spark_retail_{cat_name}_{nace}")
            st.caption(f"sts_trtu_m x {nace} | {latest_date.strftime('%b %Y')}")
        col_idx += 1

    # Logistics KPIs
    for nace in info["logistics_nace"][:1]:
        key = f"sts_sepr_m_{nace}"
        if key not in data["sts"]:
            continue
        sdf = data["sts"][key]
        monthly = sdf.groupby("date")["value"].mean().sort_index()
        if monthly.empty:
            continue
        latest_val = monthly.iloc[-1]
        latest_date = monthly.index[-1]
        nace_name = NACE_DISPLAY_NAMES.get(nace, nace)

        with cols[col_idx % 4]:
            st.metric(
                f"{nace_name}",
                f"{latest_val:.1f}",
                help=f"Services production index (EU avg), {nace}",
            )
            if len(monthly) >= 3:
                st.plotly_chart(sparkline(monthly.tail(12).tolist(), color="#ab63fa"),
                                use_container_width=True, key=f"spark_log_{cat_name}_{nace}")
            st.caption(f"sts_sepr_m x {nace} | {latest_date.strftime('%b %Y')}")
        col_idx += 1

    if col_idx == 0:
        st.info("No data available for this category yet.")

    st.divider()
