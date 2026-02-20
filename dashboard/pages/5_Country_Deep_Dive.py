"""
Country Deep Dive — All indicators for a selected country.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    EU27_CODES, AGGREGATE_CODES, COUNTRY_NAMES,
    CN_DESCRIPTIONS, SUPPLY_CN_CODES, DEMAND_CN_CODES,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS, SUPPLY_NACE, DEMAND_NACE,
    FLOW_LABELS, INDICATOR_LABELS, freshness_footnote,
)
from charts import line_chart, trade_balance_chart, bilateral_flow_chart, freshness_badge

st.title("Country Deep Dive")
st.caption("Select an EU member state to view all available trade and industrial indicators")

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

country = st.selectbox(
    "Select country", EU27_CODES,
    format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
    index=EU27_CODES.index("DE") if "DE" in EU27_CODES else 0,
)

country_name = COUNTRY_NAMES.get(country, country)
st.markdown(f"## {country_name} ({country})")

tab_supply_trade, tab_demand_trade, tab_supply_idx, tab_demand_idx, tab_partners = st.tabs([
    "Supply Material Trade",
    "End-Market Product Trade",
    "Supply Industrial Indices",
    "Demand Sector Indices",
    "Trade Partners Overview",
])

# ---- SUPPLY TRADE ----
with tab_supply_trade:
    st.subheader(f"Supply Material Trade — {country_name}")
    st.caption("International trade in label materials: World total, China breakdown. Source: Eurostat Comext DS-045409")

    indicator = st.radio("Measure", ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"],
                          format_func=lambda x: INDICATOR_LABELS.get(x, x),
                          key="cd_supply_ind", horizontal=True)
    indicator_name = INDICATOR_LABELS.get(indicator, indicator)

    for cn_code, desc in SUPPLY_CN_CODES.items():
        cdf = data["comext"].get(cn_code)
        if cdf is None:
            continue
        country_data = cdf[(cdf["country"] == country) & (cdf["indicator"] == indicator)]
        if country_data.empty:
            continue

        with st.expander(f"{desc} (CN {cn_code})"):
            world_imp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "1")]
            world_exp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "2")]
            china_imp = country_data[(country_data["partner"] == "CN") & (country_data["flow"] == "1")]

            plot_data = []
            if not world_imp.empty:
                plot_data.append(world_imp[["date", "value"]].assign(country="Imports from World"))
            if not world_exp.empty:
                plot_data.append(world_exp[["date", "value"]].assign(country="Exports to World"))
            if not china_imp.empty:
                plot_data.append(china_imp[["date", "value"]].assign(country="Imports from China"))

            if plot_data:
                combined = pd.concat(plot_data)
                date_range = f"{combined['date'].min().strftime('%b %Y')} – {combined['date'].max().strftime('%b %Y')}"
                st.plotly_chart(
                    line_chart(combined, combined["country"].unique().tolist(),
                               f"{desc} (CN {cn_code}) — {country_name}, {date_range}",
                               y_label=indicator_name),
                    use_container_width=True,
                )
                fr = data["freshness"].get(f"comext_{cn_code}", {})
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- DEMAND TRADE ----
with tab_demand_trade:
    st.subheader(f"End-Market Product Trade — {country_name}")
    st.caption("International trade in finished goods (food, beverages, HPC, pharma). Source: Eurostat Comext DS-045409")

    indicator = st.radio("Measure", ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"],
                          format_func=lambda x: INDICATOR_LABELS.get(x, x),
                          key="cd_demand_ind", horizontal=True)
    indicator_name = INDICATOR_LABELS.get(indicator, indicator)

    for cn_code, desc in DEMAND_CN_CODES.items():
        cdf = data["comext"].get(cn_code)
        if cdf is None:
            continue
        country_data = cdf[(cdf["country"] == country) & (cdf["indicator"] == indicator)]
        if country_data.empty:
            continue

        with st.expander(f"{desc} (CN {cn_code})"):
            world_imp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "1")]
            world_exp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "2")]
            china_imp = country_data[(country_data["partner"] == "CN") & (country_data["flow"] == "1")]

            plot_data = []
            if not world_imp.empty:
                plot_data.append(world_imp[["date", "value"]].assign(country="Imports from World"))
            if not world_exp.empty:
                plot_data.append(world_exp[["date", "value"]].assign(country="Exports to World"))
            if not china_imp.empty:
                plot_data.append(china_imp[["date", "value"]].assign(country="Imports from China"))

            if plot_data:
                combined = pd.concat(plot_data)
                date_range = f"{combined['date'].min().strftime('%b %Y')} – {combined['date'].max().strftime('%b %Y')}"
                st.plotly_chart(
                    line_chart(combined, combined["country"].unique().tolist(),
                               f"{desc} (CN {cn_code}) — {country_name}, {date_range}",
                               y_label=indicator_name),
                    use_container_width=True,
                )
                fr = data["freshness"].get(f"comext_{cn_code}", {})
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- SUPPLY INDICES ----
with tab_supply_idx:
    st.subheader(f"Supply Industrial Indices — {country_name}")
    st.caption("Production, prices, turnover, and confidence indices for label material sectors. Source: Eurostat STS")

    for nace, nace_desc in SUPPLY_NACE.items():
        datasets_with_data = []
        for ds in ["sts_inpr_m", "sts_inpp_m", "sts_intv_m", "ei_bssi_m_r2"]:
            key = f"{ds}_{nace}"
            df = data["sts"].get(key)
            if df is not None:
                cdata = df[df["country"] == country]
                if not cdata.empty:
                    ds_desc = STS_DATASET_DESCRIPTIONS.get(ds, ds)
                    datasets_with_data.append((key, ds, ds_desc, cdata))

        if datasets_with_data:
            with st.expander(f"{nace_desc} ({nace}) — {len(datasets_with_data)} indicators"):
                for key, ds, ds_desc, cdata in datasets_with_data:
                    fr = data["freshness"].get(key, {})
                    badge = freshness_badge(fr.get("tier", 2), fr.get("latest_date"))
                    is_confidence = "confidence" in ds_desc.lower()
                    y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"
                    st.markdown(f"**{ds_desc}** ({ds}) {badge}", unsafe_allow_html=True)
                    date_range = f"{cdata['date'].min().strftime('%b %Y')} – {cdata['date'].max().strftime('%b %Y')}"
                    plot_df = cdata.assign(country=country_name)
                    st.plotly_chart(
                        line_chart(plot_df, [country_name],
                                   f"{ds_desc} — {nace_desc} ({nace}), {country_name}, {date_range}",
                                   y_label=y_label),
                        use_container_width=True,
                    )
                    st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- DEMAND INDICES ----
with tab_demand_idx:
    st.subheader(f"Demand Sector Indices — {country_name}")
    st.caption("Production, retail turnover, logistics, and confidence for end-market sectors. Source: Eurostat STS")

    for nace, nace_desc in DEMAND_NACE.items():
        datasets_with_data = []
        all_datasets = ["sts_inpr_m", "sts_inpp_m", "sts_intv_m", "ei_bssi_m_r2",
                         "sts_trtu_m", "sts_sepr_m", "ei_bsrt_m_r2", "ei_bsse_m_r2"]
        for ds in all_datasets:
            key = f"{ds}_{nace}"
            df = data["sts"].get(key)
            if df is not None:
                cdata = df[df["country"] == country]
                if not cdata.empty:
                    ds_desc = STS_DATASET_DESCRIPTIONS.get(ds, ds)
                    datasets_with_data.append((key, ds, ds_desc, cdata))

        if datasets_with_data:
            with st.expander(f"{nace_desc} ({nace}) — {len(datasets_with_data)} indicators"):
                for key, ds, ds_desc, cdata in datasets_with_data:
                    fr = data["freshness"].get(key, {})
                    badge = freshness_badge(fr.get("tier", 2), fr.get("latest_date"))
                    is_confidence = "confidence" in ds_desc.lower()
                    y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"
                    st.markdown(f"**{ds_desc}** ({ds}) {badge}", unsafe_allow_html=True)
                    date_range = f"{cdata['date'].min().strftime('%b %Y')} – {cdata['date'].max().strftime('%b %Y')}"
                    plot_df = cdata.assign(country=country_name)
                    st.plotly_chart(
                        line_chart(plot_df, [country_name],
                                   f"{ds_desc} — {nace_desc} ({nace}), {country_name}, {date_range}",
                                   y_label=y_label),
                        use_container_width=True,
                    )
                    st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- TRADE PARTNERS ----
with tab_partners:
    st.subheader(f"Top Import Partners — {country_name}")
    st.caption(
        "Aggregated across all tracked product categories. "
        "Shows which countries supply the most imports to this country. "
        "China highlighted in red. Source: Eurostat Comext DS-045409"
    )

    partner_totals = {}
    for cn_code, cdf in data["comext"].items():
        imp = cdf[(cdf["country"] == country) & (cdf["flow"] == "1") &
                   (cdf["indicator"] == "VALUE_IN_EUROS") & (cdf["partner"] != "WORLD")]
        for _, row in imp.iterrows():
            p = row["partner"]
            partner_totals[p] = partner_totals.get(p, 0) + (row["value"] if not pd.isna(row["value"]) else 0)

    if partner_totals:
        pt_df = pd.DataFrame(list(partner_totals.items()), columns=["partner", "value"])
        pt_df = pt_df.sort_values("value", ascending=True).tail(15)
        pt_df["label"] = pt_df["partner"].map(lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})")

        import plotly.graph_objects as go
        fig = go.Figure(go.Bar(
            x=pt_df["value"], y=pt_df["label"],
            orientation="h",
            text=pt_df["value"].apply(lambda v: f"{v/1e6:,.0f}M EUR"),
            textposition="outside",
            marker_color=["#ef553b" if p == "CN" else "#636efa" for p in pt_df["partner"]],
            hovertemplate="%{y}: %{x:,.0f} EUR<extra></extra>",
        ))
        fig.update_layout(
            title=f"Top 15 Import Partners — {country_name} ({country}), All Tracked Products",
            xaxis_title="Cumulative Import Value (EUR)", yaxis_title="",
            margin=dict(l=180, r=80, t=40, b=40), height=450,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Source: Eurostat Comext DS-045409 | China highlighted in red | ~6-8 week publication lag")
    else:
        st.info(f"No bilateral partner data available for {country_name}.")
