"""
Demand Side — Retail and logistics STS indices by application category.
2 tabs: Retail Trade & Confidence, Logistics & Services.
"""

import streamlit as st
import pandas as pd
import re

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dashboard"))

from constants2 import (
    APP_CATEGORIES, CATEGORY_NAMES,
    NACE_DISPLAY_NAMES, NACE_DESCRIPTIONS,
    DATASET_DISPLAY_NAMES, STS_DATASET_DESCRIPTIONS,
    DEMAND_STS_DATASETS, AGGREGATE_CODES,
    DATASET_DEFINITIONS, TAB_DEFINITIONS,
    freshness_footnote,
)
from charts import line_chart, heatmap_yoy, freshness_badge
from sidebar_filters2 import render_category_filters

st.title("Demand Side")
st.caption(
    "Retail turnover and logistics indices for end-market application categories"
)

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# --- Sidebar filters ---
filters = render_category_filters(show_category=True, country_mode="multi")
cat_retail_nace = filters["category_retail_nace"]
cat_logistics_nace = filters["category_logistics_nace"]

tab_retail, tab_logistics = st.tabs([
    "Retail Trade & Confidence",
    "Logistics & Services",
])

# ---- RETAIL TAB ----
with tab_retail:
    st.subheader("Retail Trade & Consumer Confidence")
    with st.expander("How to read this tab", expanded=False):
        st.markdown(TAB_DEFINITIONS["retail"])

    _all_retail_series = {}
    for ds in ["sts_trtu_m"]:
        for nace in DEMAND_STS_DATASETS.get(ds, []):
            key = f"{ds}_{nace}"
            nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
            _all_retail_series[key] = f"Retail Turnover \u2014 {nace_name}"
    for ds in ["ei_bsrt_m_r2"]:
        for nace in DEMAND_STS_DATASETS.get(ds, []):
            key = f"{ds}_{nace}"
            nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
            _all_retail_series[key] = f"Retail Confidence \u2014 {nace_name}"

    # Filter by category retail NACE
    if cat_retail_nace is not None:
        retail_series = {}
        for k, v in _all_retail_series.items():
            matched = any(k.endswith(f"_{nace}") for nace in cat_retail_nace)
            if matched:
                retail_series[k] = v
    else:
        retail_series = _all_retail_series

    available_retail = {k: v for k, v in retail_series.items() if k in data["sts"]}
    if not available_retail:
        st.info("No retail data available for the selected category.")
    else:
        selected_label = st.selectbox(
            "Select indicator", list(available_retail.values()), key="retail_series"
        )
        selected_key = [k for k, v in available_retail.items() if v == selected_label][0]
        df = data["sts"][selected_key]

        # Show definition for the selected indicator
        m_ds = re.match(r"(.+)_((?:G|H)\w*)$", selected_key)
        if m_ds:
            defn = DATASET_DEFINITIONS.get(m_ds.group(1))
            if defn:
                with st.expander("What does this indicator measure?", expanded=False):
                    st.markdown(defn)

        fr = data["freshness"].get(selected_key, {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]),
                        unsafe_allow_html=True)

        is_confidence = "confidence" in selected_label.lower()
        y_label = "Confidence Balance (pp)" if is_confidence else "Turnover Index (2021 = 100)"

        available_countries = sorted(set(df["country"]) - AGGREGATE_CODES)
        selected_countries = [c for c in filters["countries"] if c in available_countries]

        if selected_countries:
            date_range = (f"{df['date'].min().strftime('%b %Y')} \u2013 "
                          f"{df['date'].max().strftime('%b %Y')}")
            st.plotly_chart(
                line_chart(df, selected_countries,
                           f"{selected_label}, {date_range}",
                           y_label=y_label),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

            if m_ds:
                st.caption(f"_{STS_DATASET_DESCRIPTIONS.get(m_ds.group(1), m_ds.group(1))} | "
                           f"NACE: {m_ds.group(2)} ({NACE_DESCRIPTIONS.get(m_ds.group(2), m_ds.group(2))})_")

            with st.expander("Year-on-Year % Change Heatmap"):
                st.plotly_chart(
                    heatmap_yoy(df, selected_countries,
                                f"{selected_label} \u2014 Year-on-Year Change (%)"),
                    use_container_width=True,
                )

# ---- LOGISTICS TAB ----
with tab_logistics:
    st.subheader("Logistics, Transport & Services")
    with st.expander("How to read this tab", expanded=False):
        st.markdown(TAB_DEFINITIONS["logistics"])

    _all_logistics_series = {}
    for ds in ["sts_sepr_m"]:
        for nace in DEMAND_STS_DATASETS.get(ds, []):
            key = f"{ds}_{nace}"
            nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
            _all_logistics_series[key] = f"Services Production \u2014 {nace_name}"
    for ds in ["ei_bsse_m_r2"]:
        for nace in DEMAND_STS_DATASETS.get(ds, []):
            key = f"{ds}_{nace}"
            nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
            _all_logistics_series[key] = f"Services Confidence \u2014 {nace_name}"

    # Filter by category logistics NACE
    if cat_logistics_nace is not None:
        logistics_series = {}
        for k, v in _all_logistics_series.items():
            matched = any(k.endswith(f"_{nace}") for nace in cat_logistics_nace)
            if matched:
                logistics_series[k] = v
    else:
        logistics_series = _all_logistics_series

    available_log = {k: v for k, v in logistics_series.items() if k in data["sts"]}
    if not available_log:
        st.info("No logistics data available for the selected category.")
    else:
        selected_label = st.selectbox(
            "Select indicator", list(available_log.values()), key="log_series"
        )
        selected_key = [k for k, v in available_log.items() if v == selected_label][0]
        df = data["sts"][selected_key]

        # Show definition for the selected indicator
        m_ds = re.match(r"(.+)_((?:G|H)\w*)$", selected_key)
        if m_ds:
            defn = DATASET_DEFINITIONS.get(m_ds.group(1))
            if defn:
                with st.expander("What does this indicator measure?", expanded=False):
                    st.markdown(defn)

        fr = data["freshness"].get(selected_key, {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]),
                        unsafe_allow_html=True)

        is_confidence = "confidence" in selected_label.lower()
        y_label = "Confidence Balance (pp)" if is_confidence else "Production Index (2021 = 100)"

        available_countries = sorted(set(df["country"]) - AGGREGATE_CODES)
        selected_countries = [c for c in filters["countries"] if c in available_countries]

        if selected_countries:
            date_range = (f"{df['date'].min().strftime('%b %Y')} \u2013 "
                          f"{df['date'].max().strftime('%b %Y')}")
            st.plotly_chart(
                line_chart(df, selected_countries,
                           f"{selected_label}, {date_range}",
                           y_label=y_label),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

            if m_ds:
                st.caption(f"_{STS_DATASET_DESCRIPTIONS.get(m_ds.group(1), m_ds.group(1))} | "
                           f"NACE: {m_ds.group(2)} ({NACE_DESCRIPTIONS.get(m_ds.group(2), m_ds.group(2))})_")
