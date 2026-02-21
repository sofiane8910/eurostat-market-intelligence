"""
Country Deep Dive — All indicators for a selected country.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    EU27_CODES, AGGREGATE_CODES, COUNTRY_NAMES,
    CN_DESCRIPTIONS, SUPPLY_CN_CODES, DEMAND_CN_CODES,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS, SUPPLY_NACE, DEMAND_NACE,
    FLOW_LABELS, INDICATOR_LABELS, freshness_footnote,
)
from charts import line_chart, dual_axis_chart, trade_balance_chart, bilateral_flow_chart, freshness_badge
from sidebar_filters import render_global_filters

st.title("Country Deep Dive")
st.caption("Select an EU member state to view all available trade and industrial indicators")

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# --- Sidebar filters ---
filters = render_global_filters(show_sector=True, country_mode="single_country")
country = filters["scope_code"]
country_name = filters["scope_name"]
_sector_cn = filters["sector_cn_codes"]
_sector_nace = filters["sector_nace_codes"]
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

    _supply_cn_items = {code: desc for code, desc in SUPPLY_CN_CODES.items()
                        if _sector_cn is None or code in _sector_cn}
    if not _supply_cn_items:
        st.info("No supply trade data matches the selected sector.")
    for cn_code, desc in _supply_cn_items.items():
        cdf = data["comext"].get(cn_code)
        if cdf is None:
            continue
        country_data = cdf[(cdf["country"] == country) & (cdf["indicator"] == indicator)]
        if country_data.empty:
            continue

        with st.expander(f"CN {cn_code} \u2014 {desc}"):
            world_imp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "1")]
            world_exp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "2")]
            china_imp = country_data[(country_data["partner"] == "CN") & (country_data["flow"] == "1")]

            # World imports & exports on left axis, China on right axis
            has_world = not world_imp.empty or not world_exp.empty
            has_china = not china_imp.empty

            if has_world or has_china:
                all_dates = pd.concat([
                    d[["date"]] for d in [world_imp, world_exp, china_imp] if not d.empty
                ])
                date_range = f"{all_dates['date'].min().strftime('%b %Y')} \u2013 {all_dates['date'].max().strftime('%b %Y')}"

                if has_china and has_world:
                    from plotly.subplots import make_subplots
                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    if not world_imp.empty:
                        fig.add_trace(go.Scatter(
                            x=world_imp["date"], y=world_imp["value"],
                            mode="lines+markers", name="Imports from World",
                            line=dict(width=2.5, color="#1f77b4"), marker=dict(size=4),
                            hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>World Imports</extra>",
                        ), secondary_y=False)
                    if not world_exp.empty:
                        fig.add_trace(go.Scatter(
                            x=world_exp["date"], y=world_exp["value"],
                            mode="lines+markers", name="Exports to World",
                            line=dict(width=2.5, color="#00cc96"), marker=dict(size=4),
                            hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>World Exports</extra>",
                        ), secondary_y=False)
                    fig.add_trace(go.Scatter(
                        x=china_imp["date"], y=china_imp["value"],
                        mode="lines+markers", name="Imports from China",
                        line=dict(width=2.5, color="#ef553b"), marker=dict(size=4),
                        hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>China Imports</extra>",
                    ), secondary_y=True)
                    fig.update_layout(
                        title=f"{desc} (CN {cn_code}) \u2014 {country_name}, {date_range}",
                        xaxis_title="", hovermode="x unified",
                        legend=dict(orientation="h", y=-0.15),
                        margin=dict(l=60, r=60, t=40, b=40), height=400,
                    )
                    fig.update_yaxes(title_text=f"{indicator_name} \u2014 World",
                                      title_font=dict(color="#1f77b4"),
                                      tickfont=dict(color="#1f77b4"), secondary_y=False)
                    fig.update_yaxes(title_text=f"{indicator_name} \u2014 China",
                                      title_font=dict(color="#ef553b"),
                                      tickfont=dict(color="#ef553b"), secondary_y=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    plot_data = []
                    if not world_imp.empty:
                        plot_data.append(world_imp[["date", "value"]].assign(country="Imports from World"))
                    if not world_exp.empty:
                        plot_data.append(world_exp[["date", "value"]].assign(country="Exports to World"))
                    if not china_imp.empty:
                        plot_data.append(china_imp[["date", "value"]].assign(country="Imports from China"))
                    combined = pd.concat(plot_data)
                    st.plotly_chart(
                        line_chart(combined, combined["country"].unique().tolist(),
                                   f"{desc} (CN {cn_code}) \u2014 {country_name}, {date_range}",
                                   y_label=indicator_name),
                        use_container_width=True,
                    )

                fr = data["freshness"].get(f"comext_{cn_code}", {})
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- DEMAND TRADE ----
with tab_demand_trade:
    st.subheader(f"End-Market Product Trade \u2014 {country_name}")
    st.caption("International trade in finished goods (food, beverages, HPC, pharma). Source: Eurostat Comext DS-045409")

    indicator = st.radio("Measure", ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"],
                          format_func=lambda x: INDICATOR_LABELS.get(x, x),
                          key="cd_demand_ind", horizontal=True)
    indicator_name = INDICATOR_LABELS.get(indicator, indicator)

    _demand_cn_items = {code: desc for code, desc in DEMAND_CN_CODES.items()
                        if _sector_cn is None or code in _sector_cn}
    if not _demand_cn_items:
        st.info("No demand trade data matches the selected sector.")
    for cn_code, desc in _demand_cn_items.items():
        cdf = data["comext"].get(cn_code)
        if cdf is None:
            continue
        country_data = cdf[(cdf["country"] == country) & (cdf["indicator"] == indicator)]
        if country_data.empty:
            continue

        with st.expander(f"CN {cn_code} \u2014 {desc}"):
            world_imp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "1")]
            world_exp = country_data[(country_data["partner"] == "WORLD") & (country_data["flow"] == "2")]
            china_imp = country_data[(country_data["partner"] == "CN") & (country_data["flow"] == "1")]

            has_world = not world_imp.empty or not world_exp.empty
            has_china = not china_imp.empty

            if has_world or has_china:
                all_dates = pd.concat([
                    d[["date"]] for d in [world_imp, world_exp, china_imp] if not d.empty
                ])
                date_range = f"{all_dates['date'].min().strftime('%b %Y')} \u2013 {all_dates['date'].max().strftime('%b %Y')}"

                if has_china and has_world:
                    from plotly.subplots import make_subplots
                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    if not world_imp.empty:
                        fig.add_trace(go.Scatter(
                            x=world_imp["date"], y=world_imp["value"],
                            mode="lines+markers", name="Imports from World",
                            line=dict(width=2.5, color="#1f77b4"), marker=dict(size=4),
                            hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>World Imports</extra>",
                        ), secondary_y=False)
                    if not world_exp.empty:
                        fig.add_trace(go.Scatter(
                            x=world_exp["date"], y=world_exp["value"],
                            mode="lines+markers", name="Exports to World",
                            line=dict(width=2.5, color="#00cc96"), marker=dict(size=4),
                            hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>World Exports</extra>",
                        ), secondary_y=False)
                    fig.add_trace(go.Scatter(
                        x=china_imp["date"], y=china_imp["value"],
                        mode="lines+markers", name="Imports from China",
                        line=dict(width=2.5, color="#ef553b"), marker=dict(size=4),
                        hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>China Imports</extra>",
                    ), secondary_y=True)
                    fig.update_layout(
                        title=f"{desc} (CN {cn_code}) \u2014 {country_name}, {date_range}",
                        xaxis_title="", hovermode="x unified",
                        legend=dict(orientation="h", y=-0.15),
                        margin=dict(l=60, r=60, t=40, b=40), height=400,
                    )
                    fig.update_yaxes(title_text=f"{indicator_name} \u2014 World",
                                      title_font=dict(color="#1f77b4"),
                                      tickfont=dict(color="#1f77b4"), secondary_y=False)
                    fig.update_yaxes(title_text=f"{indicator_name} \u2014 China",
                                      title_font=dict(color="#ef553b"),
                                      tickfont=dict(color="#ef553b"), secondary_y=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    plot_data = []
                    if not world_imp.empty:
                        plot_data.append(world_imp[["date", "value"]].assign(country="Imports from World"))
                    if not world_exp.empty:
                        plot_data.append(world_exp[["date", "value"]].assign(country="Exports to World"))
                    if not china_imp.empty:
                        plot_data.append(china_imp[["date", "value"]].assign(country="Imports from China"))
                    combined = pd.concat(plot_data)
                    st.plotly_chart(
                        line_chart(combined, combined["country"].unique().tolist(),
                                   f"{desc} (CN {cn_code}) \u2014 {country_name}, {date_range}",
                                   y_label=indicator_name),
                        use_container_width=True,
                    )

                fr = data["freshness"].get(f"comext_{cn_code}", {})
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- SUPPLY INDICES ----
with tab_supply_idx:
    st.subheader(f"Supply Industrial Indices — {country_name}")
    st.caption("Production, prices, turnover, and confidence indices for label material sectors. Source: Eurostat STS")

    _supply_nace_items = {code: desc for code, desc in SUPPLY_NACE.items()
                          if _sector_nace is None or code in _sector_nace}
    if not _supply_nace_items:
        st.info("No supply indices match the selected sector.")
    for nace, nace_desc in _supply_nace_items.items():
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
            with st.expander(f"{nace} \u2014 {nace_desc} \u2014 {len(datasets_with_data)} indicators"):
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

    _demand_nace_items = {code: desc for code, desc in DEMAND_NACE.items()
                          if _sector_nace is None or code in _sector_nace}
    if not _demand_nace_items:
        st.info("No demand indices match the selected sector.")
    for nace, nace_desc in _demand_nace_items.items():
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
            with st.expander(f"{nace} \u2014 {nace_desc} \u2014 {len(datasets_with_data)} indicators"):
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
    _partner_cn_codes = {k: v for k, v in data["comext"].items()
                         if _sector_cn is None or k in _sector_cn}
    for cn_code, cdf in _partner_cn_codes.items():
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
