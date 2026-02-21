"""
Sector Explorer — Cross-indicator sector view with country comparisons.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    SECTOR_GROUPS, EU27_CODES, AGGREGATE_CODES, COUNTRY_NAMES,
    CN_DESCRIPTIONS, STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS,
    INDICATOR_LABELS, FLOW_LABELS, freshness_footnote,
)
from charts import line_chart, bar_chart_latest, heatmap_yoy, freshness_badge

st.title("Sector Explorer")
st.caption(
    "Select a sector to view all related trade flows and industrial indicators together. "
    "Each sector groups related product codes (CN) and industry classifications (NACE)."
)

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

sector_name = st.selectbox("Select sector", list(SECTOR_GROUPS.keys()))
sector = SECTOR_GROUPS[sector_name]

st.markdown(f"### {sector_name}")
st.markdown(f"_{sector['description']}_")

# Show which codes belong to this sector
with st.expander("Sector coverage — product codes and industry classifications"):
    if sector["cn_codes"]:
        st.markdown("**Trade product codes (Comext CN):**")
        for cn in sector["cn_codes"]:
            desc = CN_DESCRIPTIONS.get(cn, cn)
            st.markdown(f"- {desc} (CN {cn})")
    if sector["nace_codes"]:
        st.markdown("**Industry classifications (NACE):**")
        for nace in sector["nace_codes"]:
            desc = NACE_DESCRIPTIONS.get(nace, nace)
            st.markdown(f"- {desc} ({nace})")

tab_trade, tab_indices, tab_compare = st.tabs([
    "International Trade",
    "Industrial Indices",
    "Country Comparison",
])

# ---- TRADE TAB ----
with tab_trade:
    cn_codes = [c for c in sector["cn_codes"] if c in data["comext"]]
    if not cn_codes:
        st.info(f"No trade data available for the {sector_name} sector.")
    else:
        st.subheader(f"EU27 Trade — {sector_name}")
        st.caption("Source: Eurostat Comext DS-045409 | Monthly imports and exports with all world partners")

        indicator = st.radio("Measure", ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"],
                              format_func=lambda x: INDICATOR_LABELS.get(x, x),
                              key="sector_trade_ind", horizontal=True)
        indicator_name = INDICATOR_LABELS.get(indicator, indicator)

        for cn_code in cn_codes:
            cdf = data["comext"][cn_code]
            desc = CN_DESCRIPTIONS.get(cn_code, cn_code)

            with st.expander(f"{desc} (CN {cn_code})", expanded=len(cn_codes) <= 3):
                imp = cdf[(cdf["flow"] == "1") & (cdf["partner"] == "WORLD") &
                          (cdf["indicator"] == indicator) & (~cdf["country"].isin(AGGREGATE_CODES))]
                exp = cdf[(cdf["flow"] == "2") & (cdf["partner"] == "WORLD") &
                          (cdf["indicator"] == indicator) & (~cdf["country"].isin(AGGREGATE_CODES))]

                imp_agg = imp.groupby("date")["value"].sum().reset_index().assign(country="EU27 Imports")
                exp_agg = exp.groupby("date")["value"].sum().reset_index().assign(country="EU27 Exports")
                combined = pd.concat([imp_agg, exp_agg])

                if not combined.empty:
                    date_range = f"{combined['date'].min().strftime('%b %Y')} – {combined['date'].max().strftime('%b %Y')}"
                    st.plotly_chart(
                        line_chart(combined, ["EU27 Imports", "EU27 Exports"],
                                   f"{desc} (CN {cn_code}) — EU27 Trade, {date_range}",
                                   y_label=indicator_name),
                        use_container_width=True,
                    )

                # China share
                china_imp = cdf[(cdf["flow"] == "1") & (cdf["partner"] == "CN") &
                                (cdf["indicator"] == "VALUE_IN_EUROS") &
                                (~cdf["country"].isin(AGGREGATE_CODES))]
                world_imp_eur = cdf[(cdf["flow"] == "1") & (cdf["partner"] == "WORLD") &
                                    (cdf["indicator"] == "VALUE_IN_EUROS") &
                                    (~cdf["country"].isin(AGGREGATE_CODES))]
                world_total = world_imp_eur["value"].sum()
                china_total = china_imp["value"].sum()
                if world_total > 0:
                    st.caption(
                        f"China import share: {china_total/world_total*100:.1f}% of EU27 imports "
                        f"({china_total/1e6:,.0f}M EUR from China out of {world_total/1e6:,.0f}M EUR total)"
                    )

                fr = data["freshness"].get(f"comext_{cn_code}", {})
                st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- INDICES TAB ----
with tab_indices:
    nace_codes = sector["nace_codes"]
    if not nace_codes:
        st.info(f"No industrial indices available for the {sector_name} sector.")
    else:
        st.subheader(f"Industrial Indices — {sector_name}")
        st.caption("Source: Eurostat Short-Term Statistics (STS) | Monthly indices")

        all_countries = set()
        for nace in nace_codes:
            for ds in STS_DATASET_DESCRIPTIONS:
                key = f"{ds}_{nace}"
                df = data["sts"].get(key)
                if df is not None:
                    all_countries.update(set(df["country"]) - AGGREGATE_CODES)

        available = sorted(all_countries & set(EU27_CODES))
        default_c = [c for c in ["DE", "FR", "IT", "ES", "PL"] if c in available]
        selected = st.multiselect(
            "Select countries", available, default=default_c[:5],
            format_func=lambda x: COUNTRY_NAMES.get(x, x),
            key="sector_idx_countries",
        )

        for nace in nace_codes:
            nace_desc = NACE_DESCRIPTIONS.get(nace, nace)
            available_ds = []
            for ds in ["sts_inpr_m", "sts_inpp_m", "sts_intv_m", "sts_trtu_m", "sts_sepr_m",
                        "ei_bssi_m_r2", "ei_bsrt_m_r2", "ei_bsse_m_r2"]:
                key = f"{ds}_{nace}"
                if key in data["sts"]:
                    available_ds.append((ds, key))

            if available_ds:
                with st.expander(f"{nace_desc} ({nace}) — {len(available_ds)} datasets"):
                    for ds, key in available_ds:
                        ds_desc = STS_DATASET_DESCRIPTIONS.get(ds, ds)
                        df = data["sts"][key]

                        fr = data["freshness"].get(key, {})
                        badge = freshness_badge(fr.get("tier", 2), fr.get("latest_date"))
                        is_confidence = "confidence" in ds_desc.lower()
                        y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"
                        st.markdown(f"**{ds_desc}** ({ds}) {badge}", unsafe_allow_html=True)

                        if selected:
                            date_range = f"{df['date'].min().strftime('%b %Y')} – {df['date'].max().strftime('%b %Y')}"
                            st.plotly_chart(
                                line_chart(df, selected,
                                           f"{ds_desc} — {nace_desc} ({nace}), {date_range}",
                                           y_label=y_label),
                                use_container_width=True,
                            )
                            st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

# ---- COUNTRY COMPARISON TAB ----
with tab_compare:
    st.subheader(f"Country Comparison — {sector_name}")
    st.caption("Ranking of EU27 countries by latest available values for this sector")

    nace_codes = sector["nace_codes"]
    if nace_codes:
        rep_key = None
        rep_ds = None
        rep_nace = None
        for nace in nace_codes:
            for ds in ["sts_inpr_m", "sts_trtu_m", "sts_sepr_m", "sts_inpp_m"]:
                key = f"{ds}_{nace}"
                if key in data["sts"]:
                    rep_key = key
                    rep_ds = ds
                    rep_nace = nace
                    break
            if rep_key:
                break

        if rep_key:
            df = data["sts"][rep_key]
            ds_desc = STS_DATASET_DESCRIPTIONS.get(rep_ds, rep_ds)
            nace_desc = NACE_DESCRIPTIONS.get(rep_nace, rep_nace)

            st.caption(f"Using: {ds_desc} ({rep_ds}) for {nace_desc} ({rep_nace})")

            eu_data = df[df["country"].isin(EU27_CODES)]
            if not eu_data.empty:
                latest_date = eu_data["date"].max()
                latest = eu_data[eu_data["date"] == latest_date].sort_values("value", ascending=True)

                if not latest.empty:
                    is_confidence = "confidence" in ds_desc.lower()
                    y_label = "Confidence Balance (pp)" if is_confidence else "Index (2021 = 100)"
                    st.plotly_chart(
                        bar_chart_latest(latest, latest["country"].tolist(),
                                          f"{ds_desc} — {nace_desc} ({rep_nace}), All EU27 Countries",
                                          y_label=y_label),
                        use_container_width=True,
                    )
                    fr = data["freshness"].get(rep_key, {})
                    st.caption(freshness_footnote(fr.get("tier", 2), fr.get("latest_date")))

                top_countries = latest.nlargest(10, "value")["country"].tolist()
                if top_countries:
                    st.plotly_chart(
                        heatmap_yoy(df, top_countries,
                                     f"Year-on-Year Change (%) — {nace_desc} ({rep_nace}), Top 10 Countries"),
                        use_container_width=True,
                    )
        else:
            st.info(f"No STS data available for country comparison in the {sector_name} sector.")

    cn_codes = [c for c in sector.get("cn_codes", []) if c in data["comext"]]
    if cn_codes:
        st.markdown(f"**Import Volume by Country — {sector_name} (latest available month)**")
        st.caption("Sum of all product codes in this sector")

        country_totals = {}
        for cn_code in cn_codes:
            cdf = data["comext"][cn_code]
            imp = cdf[(cdf["flow"] == "1") & (cdf["partner"] == "WORLD") &
                      (cdf["indicator"] == "VALUE_IN_EUROS") &
                      (cdf["country"].isin(EU27_CODES))]
            if not imp.empty:
                latest_date = imp["date"].max()
                latest_imp = imp[imp["date"] == latest_date]
                for _, row in latest_imp.iterrows():
                    c = row["country"]
                    country_totals[c] = country_totals.get(c, 0) + (row["value"] if not pd.isna(row["value"]) else 0)

        if country_totals:
            ct_df = pd.DataFrame(list(country_totals.items()), columns=["country", "value"])
            ct_df = ct_df.sort_values("value", ascending=True)
            st.plotly_chart(
                bar_chart_latest(ct_df, ct_df["country"].tolist(),
                                  f"Total Imports by Country — {sector_name}",
                                  y_label="Trade Value (EUR)"),
                use_container_width=True,
            )
            st.caption("Source: Eurostat Comext DS-045409 | ~6-8 week publication lag")
