"""
Category Deep Dive — All data for one selected application category.
Shows production indicators, retail, and logistics in tabs.
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
    PRODUCTION_DATASETS, AGGREGATE_CODES,
    DATASET_DEFINITIONS, TAB_DEFINITIONS,
    freshness_footnote,
)
from charts import line_chart, bar_chart_latest, heatmap_yoy, freshness_badge

st.title("Category Deep Dive")
st.caption("Explore all available STS indicators for a single application category")

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# Category selector in sidebar
with st.sidebar:
    st.divider()
    st.subheader("Filters")
    cat_options = {
        f"{name} \u2014 {APP_CATEGORIES[name]['description']}": name
        for name in CATEGORY_NAMES
    }
    selected_label = st.selectbox(
        "Application Category", list(cat_options.keys()), key="deep_dive_cat"
    )
    cat_name = cat_options[selected_label]
    info = APP_CATEGORIES[cat_name]

    from constants2 import EU27_CODES, COUNTRY_NAMES
    default_countries = [c for c in ["DE", "FR", "IT", "ES", "PL"] if c in EU27_CODES]
    selected_countries = st.multiselect(
        "Countries", EU27_CODES,
        default=default_countries[:5],
        format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
        key="deep_dive_countries",
    )

st.subheader(f"{cat_name}")
st.markdown(f"_{info['description']}_")

# Summary of available data
parts = []
if info["production_nace"]:
    parts.append(f"**{len(info['production_nace'])}** production NACE")
if info["retail_nace"]:
    parts.append(f"**{len(info['retail_nace'])}** retail NACE")
if info["logistics_nace"]:
    parts.append(f"**{len(info['logistics_nace'])}** logistics NACE")
if parts:
    st.markdown("Coverage: " + " | ".join(parts))

# Build tab list dynamically
tab_names = []
if info["production_nace"]:
    tab_names.append("Production Indicators")
if info["retail_nace"]:
    tab_names.append("Retail")
if info["logistics_nace"]:
    tab_names.append("Logistics")

if not tab_names:
    st.info("This category has no direct data series. Check Production Side or Demand Side pages.")
    st.stop()

tabs = st.tabs(tab_names)
tab_idx = 0

# ---- PRODUCTION TAB ----
if info["production_nace"]:
    with tabs[tab_idx]:
        st.subheader(f"{cat_name} \u2014 Production Indicators")
        with st.expander("How to read this tab", expanded=False):
            st.markdown(TAB_DEFINITIONS["output_turnover"])

        available_prod = {}
        for ds in PRODUCTION_DATASETS:
            for nace in info["production_nace"]:
                key = f"{ds}_{nace}"
                if key in data["sts"]:
                    ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                    nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                    label = f"{ds_name} \u2014 {nace_name}"
                    available_prod[label] = key

        if not available_prod:
            st.info("No production data available for this category.")
        else:
            selected_label = st.selectbox(
                "Select indicator", list(available_prod.keys()), key="cat_dd_prod"
            )
            selected_key = available_prod[selected_label]
            df = data["sts"][selected_key]

            # Show definition for the selected indicator
            m_ds = re.match(r"(.+)_((?:C|G|H)\w*)$", selected_key)
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
            y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"

            available_countries = sorted(set(df["country"]) - AGGREGATE_CODES)
            plot_countries = [c for c in selected_countries if c in available_countries]

            if plot_countries:
                date_range = (f"{df['date'].min().strftime('%b %Y')} \u2013 "
                              f"{df['date'].max().strftime('%b %Y')}")
                st.plotly_chart(
                    line_chart(df, plot_countries,
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
                        heatmap_yoy(df, plot_countries,
                                    f"{selected_label} \u2014 YoY Change (%)"),
                        use_container_width=True,
                    )
            else:
                st.warning("No data for selected countries.")
    tab_idx += 1

# ---- RETAIL TAB ----
if info["retail_nace"]:
    with tabs[tab_idx]:
        st.subheader(f"{cat_name} \u2014 Retail Indicators")
        with st.expander("How to read this tab", expanded=False):
            st.markdown(TAB_DEFINITIONS["retail"])

        available_retail = {}
        for nace in info["retail_nace"]:
            for ds in ["sts_trtu_m", "ei_bsrt_m_r2"]:
                key = f"{ds}_{nace}"
                if key in data["sts"]:
                    ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                    nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                    available_retail[f"{ds_name} \u2014 {nace_name}"] = key

        if not available_retail:
            st.info("No retail data available for this category.")
        else:
            selected_label = st.selectbox(
                "Select indicator", list(available_retail.keys()), key="cat_dd_retail"
            )
            selected_key = available_retail[selected_label]
            df = data["sts"][selected_key]

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
            plot_countries = [c for c in selected_countries if c in available_countries]

            if plot_countries:
                date_range = (f"{df['date'].min().strftime('%b %Y')} \u2013 "
                              f"{df['date'].max().strftime('%b %Y')}")
                st.plotly_chart(
                    line_chart(df, plot_countries,
                               f"{selected_label}, {date_range}",
                               y_label=y_label),
                    use_container_width=True,
                )
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))
    tab_idx += 1

# ---- LOGISTICS TAB ----
if info["logistics_nace"]:
    with tabs[tab_idx]:
        st.subheader(f"{cat_name} \u2014 Logistics & Transport")
        with st.expander("How to read this tab", expanded=False):
            st.markdown(TAB_DEFINITIONS["logistics"])

        available_log = {}
        for nace in info["logistics_nace"]:
            for ds in ["sts_sepr_m", "ei_bsse_m_r2"]:
                key = f"{ds}_{nace}"
                if key in data["sts"]:
                    ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                    nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                    available_log[f"{ds_name} \u2014 {nace_name}"] = key

        if not available_log:
            st.info("No logistics data available for this category.")
        else:
            selected_label = st.selectbox(
                "Select indicator", list(available_log.keys()), key="cat_dd_log"
            )
            selected_key = available_log[selected_label]
            df = data["sts"][selected_key]

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
            plot_countries = [c for c in selected_countries if c in available_countries]

            if plot_countries:
                date_range = (f"{df['date'].min().strftime('%b %Y')} \u2013 "
                              f"{df['date'].max().strftime('%b %Y')}")
                st.plotly_chart(
                    line_chart(df, plot_countries,
                               f"{selected_label}, {date_range}",
                               y_label=y_label),
                    use_container_width=True,
                )
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))
    tab_idx += 1
