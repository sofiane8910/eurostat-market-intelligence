"""
Supply Side — Trade data + STS industrial indices for label materials.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    SUPPLY_CN_CODES, SUPPLY_NACE, EU27_CODES, AGGREGATE_CODES,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS, COUNTRY_NAMES,
    FLOW_LABELS, INDICATOR_LABELS, freshness_footnote,
)
from data_loader import get_eu27_aggregate
from charts import line_chart, bar_chart_latest, heatmap_yoy, trade_balance_chart, freshness_badge
from sidebar_filters import render_global_filters

st.title("Supply Side — Raw Materials & Packaging")
st.caption(
    "Trade flows and industrial indices for label materials: "
    "self-adhesive plastics, paper, films (PE/PP/PVC/PET), adhesives, inks, RFID, and packaging machinery"
)

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# --- Sidebar filters ---
filters = render_global_filters(show_sector=True, country_mode="multi")
_sector_cn = filters["sector_cn_codes"]
_sector_nace = filters["sector_nace_codes"]

tab_trade, tab_indices, tab_confidence = st.tabs([
    "International Trade (Comext)", "Industrial Indices (STS)", "Business Confidence (Surveys)"
])

# ---- TRADE TAB ----
with tab_trade:
    st.subheader("EU27 International Trade — Supply Materials")
    st.caption("Source: Eurostat Comext DS-045409 | Monthly bilateral trade data")

    _supply_cn = {code: desc for code, desc in SUPPLY_CN_CODES.items()
                  if code in data["comext"] and (_sector_cn is None or code in _sector_cn)}
    cn_options = {f"CN {code} \u2014 {desc}": code for code, desc in _supply_cn.items()}
    if not cn_options:
        st.warning("No supply-side trade data loaded.")
    else:
        selected_cn_label = st.selectbox("Select product", list(cn_options.keys()), key="supply_cn")
        cn_code = cn_options[selected_cn_label]
        cdf = data["comext"][cn_code]
        product_name = SUPPLY_CN_CODES.get(cn_code, cn_code)

        fr = data["freshness"].get(f"comext_{cn_code}", {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        indicator = col1.radio("Measure", ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"],
                                format_func=lambda x: INDICATOR_LABELS.get(x, x), key="supply_ind",
                                horizontal=True)
        flow = col2.radio("Direction", ["1", "2"], format_func=lambda x: FLOW_LABELS.get(x, x),
                           key="supply_flow", horizontal=True)

        flow_name = FLOW_LABELS[flow]
        indicator_name = INDICATOR_LABELS.get(indicator, indicator)

        eu_agg = get_eu27_aggregate(cdf, partner="WORLD", flow=flow, indicator=indicator)
        if not eu_agg.empty:
            date_range = f"{eu_agg['date'].min().strftime('%b %Y')} – {eu_agg['date'].max().strftime('%b %Y')}"
            st.plotly_chart(
                line_chart(
                    eu_agg.assign(country="EU27 Total"),
                    ["EU27 Total"],
                    f"{product_name} (CN {cn_code}) — EU27 {flow_name}, {date_range}",
                    y_label=indicator_name,
                ),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

        st.markdown(f"**Top EU countries by {flow_name.lower()} — latest available month**")
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
                    f"{product_name} (CN {cn_code}) — Top {flow_name} by Country",
                    y_label=indicator_name,
                ),
                use_container_width=True,
            )
            st.caption(f"Reference period: {latest_date.strftime('%B %Y')} | {freshness_footnote(fr.get('tier', 2), fr.get('latest_date'))}")

        st.markdown(f"**EU27 Trade Balance — {product_name} (CN {cn_code})**")
        st.plotly_chart(
            trade_balance_chart(cdf, partner="WORLD", indicator=indicator,
                                 title=f"{product_name} (CN {cn_code}) — EU27 Imports vs Exports"),
            use_container_width=True,
        )
        st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- INDICES TAB ----
with tab_indices:
    st.subheader("EU Industrial Indices — Supply Sectors")
    st.caption("Source: Eurostat Short-Term Statistics (STS) | Monthly indices, base year 2021 = 100")

    supply_datasets = ["sts_inpr_m", "sts_intv_m", "sts_intvd_m", "sts_intvnd_m",
                        "sts_inpp_m", "sts_inppd_m", "sts_inppnd_m", "sts_inpi_m",
                        "sts_ordi_m", "sts_inlb_m"]
    ds_options = {STS_DATASET_DESCRIPTIONS.get(d, d): d for d in supply_datasets}
    selected_ds_label = st.selectbox("Select indicator", list(ds_options.keys()), key="supply_ds")
    dataset = ds_options[selected_ds_label]

    _supply_nace = {code: desc for code, desc in SUPPLY_NACE.items()
                    if _sector_nace is None or code in _sector_nace}
    nace_options = {f"{code} \u2014 {desc}": code for code, desc in _supply_nace.items()}
    if not nace_options:
        st.info("No supply NACE codes match the selected sector.")
        st.stop()
    selected_nace_label = st.selectbox("Select sector (NACE)", list(nace_options.keys()), key="supply_nace")
    nace = nace_options[selected_nace_label]
    nace_desc = NACE_DESCRIPTIONS.get(nace, nace)

    key = f"{dataset}_{nace}"
    df = data["sts"].get(key)

    if df is None:
        st.warning(f"No data available for {selected_ds_label} in sector {nace_desc} ({nace})")
    else:
        fr = data["freshness"].get(key, {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

        available = sorted(set(df["country"]) - AGGREGATE_CODES)
        selected_countries = [c for c in filters["countries"] if c in available]

        if selected_countries:
            date_range = f"{df['date'].min().strftime('%b %Y')} – {df['date'].max().strftime('%b %Y')}"
            st.plotly_chart(
                line_chart(df, selected_countries,
                           f"{selected_ds_label} — {nace_desc} ({nace}), {date_range}",
                           y_label="Index (2021 = 100)"),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

            with st.expander(f"Year-on-Year % Change Heatmap — {nace_desc} ({nace})"):
                st.plotly_chart(
                    heatmap_yoy(df, selected_countries,
                                f"{selected_ds_label} — {nace_desc} ({nace}) — Year-on-Year Change (%)"),
                    use_container_width=True,
                )
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- CONFIDENCE TAB ----
with tab_confidence:
    st.subheader("Industry Business Confidence — Survey Indicator (ei_bssi)")
    st.caption(
        "Source: Eurostat Business and Consumer Surveys | "
        "Balance statistic: % of positive responses minus % of negative responses"
    )

    _supply_nace_conf = {code: desc for code, desc in SUPPLY_NACE.items()
                         if _sector_nace is None or code in _sector_nace}
    nace_options_conf = {f"{code} \u2014 {desc}": code for code, desc in _supply_nace_conf.items()}
    if not nace_options_conf:
        st.info("No supply NACE codes match the selected sector.")
        st.stop()
    selected_nace_conf = st.selectbox("Select sector (NACE)", list(nace_options_conf.keys()), key="supply_conf_nace")
    nace_conf = nace_options_conf[selected_nace_conf]
    nace_conf_desc = NACE_DESCRIPTIONS.get(nace_conf, nace_conf)

    key_conf = f"ei_bssi_m_r2_{nace_conf}"
    df_conf = data["sts"].get(key_conf)

    if df_conf is None:
        st.warning(f"No confidence data for {nace_conf_desc} ({nace_conf})")
    else:
        fr = data["freshness"].get(key_conf, {})
        if fr.get("latest_date"):
            st.markdown(freshness_badge(fr["tier"], fr["latest_date"]), unsafe_allow_html=True)

        available_conf = sorted(set(df_conf["country"]) - AGGREGATE_CODES)
        selected_conf = [c for c in filters["countries"] if c in available_conf]

        if selected_conf:
            date_range = f"{df_conf['date'].min().strftime('%b %Y')} – {df_conf['date'].max().strftime('%b %Y')}"
            st.plotly_chart(
                line_chart(df_conf, selected_conf,
                           f"Industry Confidence — {nace_conf_desc} ({nace_conf}), {date_range}",
                           y_label="Confidence Balance (pp)"),
                use_container_width=True,
            )
            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))
