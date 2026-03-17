"""
Country Deep Dive — All application categories for one selected country.
Shows tabs per category with production, retail, and logistics indicators.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dashboard"))

from constants2 import (
    APP_CATEGORIES, CATEGORY_NAMES,
    NACE_DISPLAY_NAMES, NACE_DESCRIPTIONS,
    DATASET_DISPLAY_NAMES, STS_DATASET_DESCRIPTIONS,
    AGGREGATE_CODES, COUNTRY_NAMES,
    DATASET_DEFINITIONS,
    freshness_footnote,
)
from charts import line_chart, freshness_badge

st.title("Country Deep Dive")
st.caption("All application categories and STS indicators for a single EU country")

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# Country selector in sidebar
with st.sidebar:
    st.divider()
    st.subheader("Filters")
    from constants2 import EU27_CODES
    country_options = list(EU27_CODES)
    default_idx = country_options.index("DE") if "DE" in country_options else 0
    selected_country = st.selectbox(
        "Country", country_options, index=default_idx,
        format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
        key="country_dd_single",
    )

country_name = COUNTRY_NAMES.get(selected_country, selected_country)
st.subheader(f"{country_name} ({selected_country})")

with st.expander("Guide to indicators on this page", expanded=False):
    st.markdown(
        "**Production indicators** (STS):\n"
        "- *Production Volume* = physical output of factories (price effects removed)\n"
        "- *Producer Prices* = average selling prices at the factory gate\n"
        "- *Industry Confidence* = survey of manufacturing managers (positive = optimistic)\n\n"
        "**Retail indicators**: retail turnover (consumer spending in shops, deflated) "
        "and retail confidence (manager survey).\n\n"
        "**Logistics indicators**: transport, warehousing, and postal services output volume "
        "and services confidence.\n\n"
        "All indices use base year 2021 = 100. Confidence is measured in percentage points (pp)."
    )

# Tabs per category
tab_labels = [cat for cat in CATEGORY_NAMES]
tabs = st.tabs(tab_labels)

for i, cat_name in enumerate(CATEGORY_NAMES):
    with tabs[i]:
        info = APP_CATEGORIES[cat_name]
        st.markdown(f"**{cat_name}** \u2014 _{info['description']}_")

        has_data = False

        # ---- Production indicators ----
        if info["production_nace"]:
            prod_found = False
            for nace in info["production_nace"]:
                for ds in ["sts_inpr_m", "sts_inpp_m", "ei_bssi_m_r2"]:
                    key = f"{ds}_{nace}"
                    if key not in data["sts"]:
                        continue
                    sdf = data["sts"][key]
                    country_data = sdf[sdf["country"] == selected_country]
                    if country_data.empty:
                        continue

                    if not prod_found:
                        st.markdown("**Production Indicators**")
                        prod_found = True
                    has_data = True

                    ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                    nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                    label = f"{ds_name} \u2014 {nace_name}"

                    is_confidence = "confidence" in ds_name.lower()
                    y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"

                    date_range = (f"{country_data['date'].min().strftime('%b %Y')} \u2013 "
                                  f"{country_data['date'].max().strftime('%b %Y')}")
                    st.plotly_chart(
                        line_chart(
                            country_data.assign(country=selected_country),
                            [selected_country],
                            f"{label} \u2014 {country_name}, {date_range}",
                            y_label=y_label,
                        ),
                        use_container_width=True,
                    )
                    fr = data["freshness"].get(key, {})
                    st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

        # ---- Retail indicators ----
        if info["retail_nace"]:
            retail_found = False
            for nace in info["retail_nace"]:
                for ds in ["sts_trtu_m", "ei_bsrt_m_r2"]:
                    key = f"{ds}_{nace}"
                    if key not in data["sts"]:
                        continue
                    sdf = data["sts"][key]
                    country_data = sdf[sdf["country"] == selected_country]
                    if country_data.empty:
                        continue

                    if not retail_found:
                        st.markdown("**Retail Indicators**")
                        retail_found = True
                    has_data = True

                    ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                    nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                    label = f"{ds_name} \u2014 {nace_name}"

                    is_confidence = "confidence" in label.lower()
                    y_label = "Confidence Balance (pp)" if is_confidence else "Turnover Index (2021 = 100)"

                    date_range = (f"{country_data['date'].min().strftime('%b %Y')} \u2013 "
                                  f"{country_data['date'].max().strftime('%b %Y')}")
                    st.plotly_chart(
                        line_chart(
                            country_data.assign(country=selected_country),
                            [selected_country],
                            f"{label} \u2014 {country_name}, {date_range}",
                            y_label=y_label,
                        ),
                        use_container_width=True,
                    )

        # ---- Logistics indicators ----
        if info["logistics_nace"]:
            log_found = False
            for nace in info["logistics_nace"]:
                for ds in ["sts_sepr_m", "ei_bsse_m_r2"]:
                    key = f"{ds}_{nace}"
                    if key not in data["sts"]:
                        continue
                    sdf = data["sts"][key]
                    country_data = sdf[sdf["country"] == selected_country]
                    if country_data.empty:
                        continue

                    if not log_found:
                        st.markdown("**Logistics & Transport**")
                        log_found = True
                    has_data = True

                    ds_name = DATASET_DISPLAY_NAMES.get(ds, ds)
                    nace_name = NACE_DISPLAY_NAMES.get(nace, nace)
                    label = f"{ds_name} \u2014 {nace_name}"

                    is_confidence = "confidence" in label.lower()
                    y_label = "Confidence Balance (pp)" if is_confidence else "Production Index (2021 = 100)"

                    date_range = (f"{country_data['date'].min().strftime('%b %Y')} \u2013 "
                                  f"{country_data['date'].max().strftime('%b %Y')}")
                    st.plotly_chart(
                        line_chart(
                            country_data.assign(country=selected_country),
                            [selected_country],
                            f"{label} \u2014 {country_name}, {date_range}",
                            y_label=y_label,
                        ),
                        use_container_width=True,
                    )

        if not has_data:
            st.info(f"No data available for {cat_name} in {country_name}.")
