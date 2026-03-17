"""
Production Side — STS industrial indicators by application category.
3 tabs: Output/Turnover, Prices, Labour/Confidence.
"""

import streamlit as st
import pandas as pd
import re

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dashboard"))

from constants2 import (
    APP_CATEGORIES, PRODUCTION_NACE,
    DATASET_DISPLAY_NAMES, NACE_DISPLAY_NAMES, NACE_DESCRIPTIONS,
    STS_DATASET_DESCRIPTIONS, AGGREGATE_CODES,
    PRODUCTION_TAB_OUTPUT, PRODUCTION_TAB_PRICES, PRODUCTION_TAB_LABOUR,
    DATASET_DEFINITIONS, TAB_DEFINITIONS,
    freshness_footnote,
)
from charts import line_chart, bar_chart_latest, heatmap_yoy, freshness_badge
from sidebar_filters2 import render_category_filters

st.title("Production Side")
st.caption(
    "Industrial production, turnover, prices, labour and confidence indicators "
    "by application category. All data from Eurostat STS monthly indices."
)

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# --- Sidebar filters ---
filters = render_category_filters(show_category=True, country_mode="multi")
cat_prod_nace = filters["category_production_nace"]
selected_countries = filters["countries"]

# Determine which NACE codes to show
if cat_prod_nace:
    active_nace = cat_prod_nace
else:
    active_nace = PRODUCTION_NACE

# --- Tabs ---
tab_output, tab_prices, tab_labour = st.tabs([
    "Output & Turnover",
    "Prices",
    "Labour & Confidence",
])


def _render_sts_section(datasets, nace_list, countries):
    """Render STS charts for a list of datasets x NACE codes."""
    # Build available series
    available = {}
    for ds in datasets:
        for nace in nace_list:
            key = f"{ds}_{nace}"
            if key in data["sts"]:
                ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                label = f"{ds_name} \u2014 {nace_name}"
                available[label] = key

    if not available:
        st.info("No data available for the selected category and indicator combination.")
        return

    selected_label = st.selectbox(
        "Select indicator", list(available.keys()),
        key=f"prod_{datasets[0]}",
    )
    selected_key = available[selected_label]
    df = data["sts"][selected_key]

    # Extract dataset and nace from key
    m = re.match(r"(.+)_((?:C|G|H)\w*)$", selected_key)
    if m:
        dataset_id, nace_id = m.group(1), m.group(2)
    else:
        dataset_id, nace_id = selected_key, ""

    # Show definition for the selected indicator
    defn = DATASET_DEFINITIONS.get(dataset_id)
    if defn:
        with st.expander("What does this indicator measure?", expanded=False):
            st.markdown(defn)

    fr = data["freshness"].get(selected_key, {})
    if fr.get("latest_date"):
        st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

    is_confidence = "confidence" in selected_label.lower()
    y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"

    available_countries = sorted(set(df["country"]) - AGGREGATE_CODES)
    plot_countries = [c for c in countries if c in available_countries]

    if not plot_countries:
        st.warning("No data for selected countries. Try selecting different countries.")
        return

    date_range = f"{df['date'].min().strftime('%b %Y')} \u2013 {df['date'].max().strftime('%b %Y')}"
    st.plotly_chart(
        line_chart(df, plot_countries,
                   f"{selected_label}, {date_range}",
                   y_label=y_label),
        use_container_width=True,
    )
    st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))
    st.caption(f"_{STS_DATASET_DESCRIPTIONS.get(dataset_id, dataset_id)} | "
               f"NACE: {nace_id} ({NACE_DESCRIPTIONS.get(nace_id, nace_id)})_")

    # Bar chart of latest values
    latest_date = df["date"].max()
    latest = df[(df["date"] == latest_date) & (df["country"].isin(plot_countries))]
    if not latest.empty:
        st.plotly_chart(
            bar_chart_latest(latest, plot_countries,
                             f"{selected_label} \u2014 Latest Values",
                             y_label=y_label),
            use_container_width=True,
        )

    # YoY heatmap in expander
    with st.expander("Year-on-Year % Change Heatmap"):
        st.plotly_chart(
            heatmap_yoy(df, plot_countries,
                        f"{selected_label} \u2014 Year-on-Year Change (%)"),
            use_container_width=True,
        )


# ---- OUTPUT & TURNOVER TAB ----
with tab_output:
    st.subheader("Industrial Output & Turnover")
    with st.expander("How to read this tab", expanded=False):
        st.markdown(TAB_DEFINITIONS["output_turnover"])
    _render_sts_section(PRODUCTION_TAB_OUTPUT, active_nace, selected_countries)

# ---- PRICES TAB ----
with tab_prices:
    st.subheader("Producer & Import Prices")
    with st.expander("How to read this tab", expanded=False):
        st.markdown(TAB_DEFINITIONS["prices"])
    _render_sts_section(PRODUCTION_TAB_PRICES, active_nace, selected_countries)

# ---- LABOUR & CONFIDENCE TAB ----
with tab_labour:
    st.subheader("Labour Input & Industry Confidence")
    with st.expander("How to read this tab", expanded=False):
        st.markdown(TAB_DEFINITIONS["labour_confidence"])
    _render_sts_section(PRODUCTION_TAB_LABOUR, active_nace, selected_countries)
