"""
Demand Side — End-market trade, retail, logistics, confidence.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    DEMAND_CN_CODES, DEMAND_NACE, EU27_CODES, AGGREGATE_CODES,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS, COUNTRY_NAMES,
    FLOW_LABELS, INDICATOR_LABELS, freshness_footnote,
)
from data_loader import get_eu27_aggregate
from charts import line_chart, bar_chart_latest, heatmap_yoy, trade_balance_chart, freshness_badge
from sidebar_filters import render_global_filters

st.title("Demand Side — End-Market Sectors")
st.caption(
    "Trade flows and economic indicators for sectors that consume labels: "
    "food, beverages, HPC & cosmetics, pharmaceuticals, retail, and logistics"
)

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# --- Sidebar filters ---
filters = render_global_filters(show_sector=True, country_mode="multi")
_sector_cn = filters["sector_cn_codes"]
_sector_nace = filters["sector_nace_codes"]

tab_trade, tab_retail, tab_logistics = st.tabs([
    "End-Market International Trade (Comext)",
    "Retail Trade & Confidence",
    "Logistics & Services",
])

# ---- TRADE TAB ----
with tab_trade:
    st.subheader("EU27 International Trade — End-Market Products")
    st.caption("Source: Eurostat Comext DS-045409 | Monthly bilateral trade data for finished goods")

    _ALL_DEMAND_GROUPS = {
        "Processed Food (meat, fish, vegetables, preparations)": ["1602", "1604", "2005", "2106"],
        "Beverages (juices, water, soft drinks, beer, wine, spirits)": ["2009", "2201", "2202", "2203", "2204", "2208"],
        "HPC & Cosmetics (beauty, hair, cleaning products)": ["3304", "3305", "3307", "3402"],
        "Pharmaceuticals (medicaments in dosage form)": ["3004"],
    }

    # Filter groups by sector CN codes when a sector is selected
    if _sector_cn is not None:
        DEMAND_GROUPS = {k: [c for c in v if c in _sector_cn]
                         for k, v in _ALL_DEMAND_GROUPS.items()}
        DEMAND_GROUPS = {k: v for k, v in DEMAND_GROUPS.items() if v}
    else:
        DEMAND_GROUPS = _ALL_DEMAND_GROUPS

    if not DEMAND_GROUPS:
        st.info("No demand trade data matches the selected sector.")
    else:
        sector = st.selectbox("Select end-market sector", list(DEMAND_GROUPS.keys()), key="demand_sector")
        cn_codes_in_sector = [c for c in DEMAND_GROUPS[sector] if c in data["comext"]]

        if not cn_codes_in_sector:
            st.warning(f"No trade data for {sector}")
        else:
            cn_options = {f"CN {code} \u2014 {DEMAND_CN_CODES.get(code, code)}": code for code in cn_codes_in_sector}
            selected_cn_label = st.selectbox("Select product", list(cn_options.keys()), key="demand_cn")
            cn_code = cn_options[selected_cn_label]
            cdf = data["comext"][cn_code]
            product_name = DEMAND_CN_CODES.get(cn_code, cn_code)

            fr = data["freshness"].get(f"comext_{cn_code}", {})
            if fr.get("latest_date"):
                st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            indicator = col1.radio("Measure", ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"],
                                    format_func=lambda x: INDICATOR_LABELS.get(x, x), key="demand_ind",
                                    horizontal=True)
            flow = col2.radio("Direction", ["1", "2"], format_func=lambda x: FLOW_LABELS.get(x, x),
                               key="demand_flow", horizontal=True)

            flow_name = FLOW_LABELS[flow]
            indicator_name = INDICATOR_LABELS.get(indicator, indicator)

            eu_agg = get_eu27_aggregate(cdf, partner="WORLD", flow=flow, indicator=indicator)
            if not eu_agg.empty:
                date_range = f"{eu_agg['date'].min().strftime('%b %Y')} \u2013 {eu_agg['date'].max().strftime('%b %Y')}"
                st.plotly_chart(
                    line_chart(
                        eu_agg.assign(country="EU27 Total"), ["EU27 Total"],
                        f"{product_name} (CN {cn_code}) \u2014 EU27 {flow_name}, {date_range}",
                        y_label=indicator_name,
                    ),
                    use_container_width=True,
                )
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

            country_latest = cdf[
                (cdf["partner"] == "WORLD") & (cdf["flow"] == flow) &
                (cdf["indicator"] == indicator) & (~cdf["country"].isin(AGGREGATE_CODES))
            ]
            if not country_latest.empty:
                latest_date = country_latest["date"].max()
                latest = country_latest[country_latest["date"] == latest_date].nlargest(15, "value")
                st.plotly_chart(
                    bar_chart_latest(
                        latest, latest["country"].tolist(),
                        f"{product_name} (CN {cn_code}) \u2014 Top EU Countries by {flow_name}",
                        y_label=indicator_name,
                    ),
                    use_container_width=True,
                )
                st.caption(f"Reference period: {latest_date.strftime('%B %Y')} | {freshness_footnote(fr.get('tier', 2), fr.get('latest_date'))}")

            st.plotly_chart(
                trade_balance_chart(cdf, partner="WORLD", indicator=indicator,
                                     title=f"{product_name} (CN {cn_code}) \u2014 EU27 Imports vs Exports"),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- RETAIL TAB ----
with tab_retail:
    st.subheader("Retail Trade Turnover & Consumer Confidence")
    st.caption(
        "Source: Eurostat STS (sts_trtu_m) and Business Surveys (ei_bsrt) | "
        "Monthly indices, base year 2021 = 100 (turnover) or balance in pp (confidence)"
    )

    _all_retail_series = {
        "sts_trtu_m_G47": "Retail trade turnover \u2014 total excl. motor vehicles (G47)",
        "sts_trtu_m_G47_FOOD": "Food, beverages & tobacco retail turnover (G47_FOOD)",
        "sts_trtu_m_G47_NF_HLTH": "Health, cosmetics & toiletries retail turnover (G47_NF_HLTH)",
        "sts_trtu_m_G47_NFOOD_X_G473": "Non-food retail turnover excl. fuel (G47_NFOOD_X_G473)",
        "sts_trtu_m_G4711": "Non-specialised stores, food predominating (G4711)",
        "ei_bsrt_m_r2_G47_FOOD": "Food retail confidence indicator (G47_FOOD)",
        "ei_bsrt_m_r2_G47_NFOOD": "Non-food retail confidence indicator (G47_NFOOD)",
    }

    # Filter by sector NACE codes if selected
    if _sector_nace is not None:
        retail_series = {}
        for k, v in _all_retail_series.items():
            # Extract NACE from key: check if any sector NACE code appears in the key
            matched = any(k.endswith(f"_{nace}") or f"_{nace}_" in k for nace in _sector_nace)
            if matched:
                retail_series[k] = v
    else:
        retail_series = _all_retail_series

    available_retail = {k: v for k, v in retail_series.items() if k in data["sts"]}
    if not available_retail:
        st.warning("No retail data available.")
    else:
        selected_label = st.selectbox("Select indicator", list(available_retail.values()), key="retail_series")
        selected_key = [k for k, v in available_retail.items() if v == selected_label][0]
        df = data["sts"][selected_key]

        fr = data["freshness"].get(selected_key, {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

        is_confidence = "confidence" in selected_label.lower()
        y_label = "Confidence Balance (pp)" if is_confidence else "Turnover Index (2021 = 100)"

        available_countries = sorted(set(df["country"]) - AGGREGATE_CODES)
        selected_countries = [c for c in filters["countries"] if c in available_countries]

        if selected_countries:
            date_range = f"{df['date'].min().strftime('%b %Y')} \u2013 {df['date'].max().strftime('%b %Y')}"
            st.plotly_chart(
                line_chart(df, selected_countries,
                           f"{selected_label}, {date_range}",
                           y_label=y_label),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

            with st.expander(f"Year-on-Year % Change Heatmap"):
                st.plotly_chart(
                    heatmap_yoy(df, selected_countries,
                                f"{selected_label} — Year-on-Year Change (%)"),
                    use_container_width=True,
                )

# ---- LOGISTICS TAB ----
with tab_logistics:
    st.subheader("Logistics, Transport & Services")
    st.caption(
        "Source: Eurostat STS (sts_sepr_m) and Business Surveys (ei_bsse) | "
        "Monthly services production index (2021 = 100) or confidence balance (pp)"
    )

    _all_logistics_series = {
        "sts_sepr_m_H": "Transportation & storage \u2014 total production index (H)",
        "sts_sepr_m_H49": "Land transport & pipelines \u2014 production index (H49)",
        "sts_sepr_m_H52": "Warehousing & transport support \u2014 production index (H52)",
        "sts_sepr_m_H53": "Postal & courier services \u2014 production index (H53)",
        "ei_bsse_m_r2_H": "Services sector confidence indicator (H)",
    }

    # Filter by sector NACE codes if selected
    if _sector_nace is not None:
        logistics_series = {}
        for k, v in _all_logistics_series.items():
            matched = any(k.endswith(f"_{nace}") or f"_{nace}_" in k for nace in _sector_nace)
            if matched:
                logistics_series[k] = v
    else:
        logistics_series = _all_logistics_series

    available_log = {k: v for k, v in logistics_series.items() if k in data["sts"]}
    if not available_log:
        st.warning("No logistics data available.")
    else:
        selected_label = st.selectbox("Select indicator", list(available_log.values()), key="log_series")
        selected_key = [k for k, v in available_log.items() if v == selected_label][0]
        df = data["sts"][selected_key]

        fr = data["freshness"].get(selected_key, {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

        is_confidence = "confidence" in selected_label.lower()
        y_label = "Confidence Balance (pp)" if is_confidence else "Production Index (2021 = 100)"

        available_countries = sorted(set(df["country"]) - AGGREGATE_CODES)
        selected_countries = [c for c in filters["countries"] if c in available_countries]

        if selected_countries:
            date_range = f"{df['date'].min().strftime('%b %Y')} \u2013 {df['date'].max().strftime('%b %Y')}"
            st.plotly_chart(
                line_chart(df, selected_countries,
                           f"{selected_label}, {date_range}",
                           y_label=y_label),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))
