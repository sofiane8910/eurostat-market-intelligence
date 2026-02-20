"""
Executive Summary — KPIs, sparklines, freshness indicators.
Supports filtering by EU27 aggregate or individual country.
Detects incomplete latest periods (late-reporting countries).
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    AGGREGATE_CODES, EU27_CODES, COUNTRY_NAMES, SECTOR_GROUPS,
    SUPPLY_CN_CODES, DEMAND_CN_CODES, freshness_footnote,
)
from data_loader import get_eu27_aggregate
from charts import sparkline, freshness_badge

st.title("Executive Summary — European Labels Market")
st.caption("Key performance indicators across supply and demand sides of the EU27 labels industry")

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# --- Country filter ---
country_options = ["EU27 Aggregate"] + [
    f"{COUNTRY_NAMES.get(c, c)} ({c})" for c in EU27_CODES
]
selected_label = st.selectbox(
    "Select scope", country_options, index=0,
    help="View KPIs for the full EU27 aggregate or drill into an individual country",
    key="exec_country",
)
is_aggregate = selected_label == "EU27 Aggregate"
if is_aggregate:
    scope_name = "EU27 Aggregate"
    scope_code = None
else:
    scope_code = selected_label.split("(")[-1].rstrip(")")
    scope_name = COUNTRY_NAMES.get(scope_code, scope_code)

# --- Freshness banner ---
t1 = [v for v in data["freshness"].values() if v["tier"] == 1 and v["latest_date"] is not None]
t2 = [v for v in data["freshness"].values() if v["tier"] == 2 and v["latest_date"] is not None]

col1, col2 = st.columns(2)
if t1:
    latest_t1 = max(v["latest_date"] for v in t1)
    col1.success(
        f"**Fast-release data** (confidence surveys, price indices): "
        f"{len(t1)} series through **{latest_t1.strftime('%B %Y')}**\n\n"
        f"_~3 week publication lag_"
    )
if t2:
    latest_t2 = max(v["latest_date"] for v in t2)
    col2.warning(
        f"**Standard-release data** (production, trade, turnover, retail): "
        f"{len(t2)} series through **{latest_t2.strftime('%B %Y')}**\n\n"
        f"_~6-8 week publication lag_"
    )

st.divider()


# --- Helper: detect missing countries on latest period ---
def _detect_incomplete_period(df, aggregate_codes=AGGREGATE_CODES):
    """
    Check the latest month in a dataset: which EU27 countries have data,
    which are missing. Returns (latest_date, present, missing).
    """
    if df is None or df.empty:
        return None, [], EU27_CODES.copy()
    non_agg = df[~df["country"].isin(aggregate_codes)]
    if non_agg.empty:
        return None, [], EU27_CODES.copy()
    latest_date = non_agg["date"].max()
    latest_data = non_agg[non_agg["date"] == latest_date]
    present = sorted(set(latest_data["country"]) & set(EU27_CODES))
    missing = sorted(set(EU27_CODES) - set(present))
    return latest_date, present, missing


def _detect_incomplete_comext(cdf, flow="1", indicator="VALUE_IN_EUROS"):
    """Check latest Comext period for missing reporters."""
    if cdf is None or cdf.empty:
        return None, [], EU27_CODES.copy()
    sub = cdf[
        (cdf["partner"] == "WORLD") & (cdf["flow"] == flow) &
        (cdf["indicator"] == indicator) & (~cdf["country"].isin(AGGREGATE_CODES))
    ]
    return _detect_incomplete_period(sub)


# --- Helper: get time series for selected scope ---
def _get_sts_series(key: str):
    """
    Get time series from STS data for the selected scope.
    For EU27: use the EU27_2020 aggregate row.
    For a country: use that country's row.
    Returns (latest_val, mom, yoy, latest_date, series_df).
    """
    df = data["sts"].get(key)
    if df is None:
        return None, None, None, None, None

    if is_aggregate:
        ts = df[df["country"] == "EU27_2020"].sort_values("date")
        if ts.empty:
            ts = df[df["country"] == "EA20"].sort_values("date")
    else:
        ts = df[df["country"] == scope_code].sort_values("date")

    if ts.empty or len(ts) < 2:
        return None, None, None, None, None

    latest_val = ts["value"].iloc[-1]
    latest_date = ts["date"].iloc[-1]
    prev_val = ts["value"].iloc[-2]
    mom = ((latest_val - prev_val) / abs(prev_val) * 100) if prev_val != 0 else 0

    yoy_date = latest_date - pd.DateOffset(years=1)
    yoy_row = ts[ts["date"] == yoy_date]
    yoy = None
    if not yoy_row.empty:
        yoy_val = yoy_row["value"].iloc[0]
        if yoy_val != 0:
            yoy = (latest_val - yoy_val) / abs(yoy_val) * 100

    return latest_val, mom, yoy, latest_date, ts


def _kpi_card(col, label, value, mom, yoy, latest_date, tier_key=""):
    """Render a KPI card in a column with explicit date and lag info."""
    freshness = data["freshness"].get(tier_key, {})
    tier = freshness.get("tier", 2)
    dot = "\U0001f7e2" if tier == 1 else "\U0001f7e0"
    lag_text = "~3 wk lag" if tier == 1 else "~6-8 wk lag"

    if value is not None:
        date_label = latest_date.strftime("%b %Y") if latest_date is not None else ""
        col.metric(
            f"{dot} {label}",
            f"{value:,.1f}",
            delta=f"MoM: {mom:+.1f}%" if mom is not None else None,
        )
        parts = []
        if yoy is not None:
            parts.append(f"YoY: {yoy:+.1f}%")
        parts.append(f"As of {date_label}")
        parts.append(f"({lag_text})")
        col.caption(" | ".join(parts))
    else:
        col.metric(f"{dot} {label}", "N/A")
        col.caption(f"No data for {scope_name} ({lag_text})")


# --- KPI Cards ---
st.subheader(f"Key Indicators — {scope_name}")

# Row 1: Supply-side KPIs
st.markdown("### Supply Side — Raw Materials & Packaging")
c1, c2, c3, c4 = st.columns(4)

val, mom, yoy, dt, _ = _get_sts_series("ei_bssi_m_r2_C17")
_kpi_card(c1, "Paper & Board Confidence (C17)", val, mom, yoy, dt, "ei_bssi_m_r2_C17")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C222")
_kpi_card(c2, "Plastics Production Index (C222)", val, mom, yoy, dt, "sts_inpr_m_C222")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpp_m_C17")
_kpi_card(c3, "Paper Producer Prices (C17)", val, mom, yoy, dt, "sts_inpp_m_C17")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C203")
_kpi_card(c4, "Inks & Varnish Production (C203)", val, mom, yoy, dt, "sts_inpr_m_C203")

# Row 2: Demand-side KPIs
st.markdown("### Demand Side — End-Market Sectors")
c1, c2, c3, c4 = st.columns(4)

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C10")
_kpi_card(c1, "Food Production Index (C10)", val, mom, yoy, dt, "sts_inpr_m_C10")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C11")
_kpi_card(c2, "Beverages Production Index (C11)", val, mom, yoy, dt, "sts_inpr_m_C11")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C21")
_kpi_card(c3, "Pharma Production Index (C21)", val, mom, yoy, dt, "sts_inpr_m_C21")

val, mom, yoy, dt, _ = _get_sts_series("sts_trtu_m_G47_FOOD")
_kpi_card(c4, "Food Retail Turnover (G47_FOOD)", val, mom, yoy, dt, "sts_trtu_m_G47_FOOD")

# Row 3: Trade
st.markdown(f"### Trade Overview — {scope_name} (Comext)")

supply_codes = [c[0] for c in data["meta"]["comext_codes"] if c[2] == "supply"]

total_supply_imp = 0
total_supply_exp = 0
trade_latest_date = None
total_china_imp = 0

for cn_code in supply_codes:
    cdf = data["comext"].get(cn_code)
    if cdf is None:
        continue

    if is_aggregate:
        # Sum all non-aggregate reporters for EU27 total
        world_imp = cdf[
            (cdf["partner"] == "WORLD") & (cdf["flow"] == "1") &
            (cdf["indicator"] == "VALUE_IN_EUROS") & (~cdf["country"].isin(AGGREGATE_CODES))
        ]
        world_exp = cdf[
            (cdf["partner"] == "WORLD") & (cdf["flow"] == "2") &
            (cdf["indicator"] == "VALUE_IN_EUROS") & (~cdf["country"].isin(AGGREGATE_CODES))
        ]
        cn_imp = cdf[
            (cdf["partner"] == "CN") & (cdf["flow"] == "1") &
            (cdf["indicator"] == "VALUE_IN_EUROS") & (~cdf["country"].isin(AGGREGATE_CODES))
        ]
    else:
        world_imp = cdf[
            (cdf["country"] == scope_code) & (cdf["partner"] == "WORLD") &
            (cdf["flow"] == "1") & (cdf["indicator"] == "VALUE_IN_EUROS")
        ]
        world_exp = cdf[
            (cdf["country"] == scope_code) & (cdf["partner"] == "WORLD") &
            (cdf["flow"] == "2") & (cdf["indicator"] == "VALUE_IN_EUROS")
        ]
        cn_imp = cdf[
            (cdf["country"] == scope_code) & (cdf["partner"] == "CN") &
            (cdf["flow"] == "1") & (cdf["indicator"] == "VALUE_IN_EUROS")
        ]

    if not world_imp.empty:
        latest_date = world_imp["date"].max()
        trade_latest_date = latest_date
        total_supply_imp += world_imp[world_imp["date"] == latest_date]["value"].sum()
    if not world_exp.empty:
        latest_date = world_exp["date"].max()
        total_supply_exp += world_exp[world_exp["date"] == latest_date]["value"].sum()
    if not cn_imp.empty:
        latest_date = cn_imp["date"].max()
        total_china_imp += cn_imp[cn_imp["date"] == latest_date]["value"].sum()

trade_date_str = trade_latest_date.strftime("%B %Y") if trade_latest_date else "N/A"
c1, c2, c3 = st.columns(3)
c1.metric(f"Total Supply Imports ({trade_date_str})", f"{total_supply_imp/1e6:,.0f}M EUR")
c2.metric(f"Total Supply Exports ({trade_date_str})", f"{total_supply_exp/1e6:,.0f}M EUR")
c3.metric(f"Net Trade Balance ({trade_date_str})", f"{(total_supply_exp - total_supply_imp)/1e6:+,.0f}M EUR")
st.caption(f"Source: Eurostat Comext (DS-045409) | Data as of {trade_date_str} | ~6-8 week publication lag")

if total_supply_imp > 0:
    china_pct = total_china_imp / total_supply_imp * 100
    st.info(
        f"**China Competition ({trade_date_str})**: China accounts for **{china_pct:.1f}%** "
        f"of {scope_name} supply material imports "
        f"({total_china_imp/1e6:,.0f}M EUR out of {total_supply_imp/1e6:,.0f}M EUR)"
    )

st.divider()

# --- Incomplete Period Detection ---
st.subheader("Data Completeness — Latest Period Reporting Status")
st.caption(
    "Some EU countries report data later than others. "
    "When the latest month has fewer reporters, aggregated values may appear artificially low. "
    "This section flags which countries are missing from the most recent period."
)

# Check a representative STS series
incomplete_alerts = []
representative_sts = [
    ("sts_inpr_m_C17", "Production in industry — Paper (C17)"),
    ("sts_inpr_m_C222", "Production in industry — Plastics (C222)"),
    ("sts_trtu_m_G47_FOOD", "Retail trade turnover — Food (G47_FOOD)"),
]

for sts_key, sts_label in representative_sts:
    df = data["sts"].get(sts_key)
    if df is not None:
        dt, present, missing = _detect_incomplete_period(df)
        if dt and missing:
            incomplete_alerts.append({
                "series": sts_label,
                "dataset_id": sts_key,
                "latest_date": dt,
                "reporters": len(present),
                "missing_count": len(missing),
                "missing_countries": missing,
            })

# Check representative Comext series
representative_comext = [
    ("48114100", "Self-adhesive paper and paperboard (CN 48114100)"),
    ("39191080", "SA plastic, rolls (CN 39191080)"),
]
for cn_code, cn_label in representative_comext:
    cdf = data["comext"].get(cn_code)
    if cdf is not None:
        dt, present, missing = _detect_incomplete_comext(cdf)
        if dt and missing:
            incomplete_alerts.append({
                "series": cn_label,
                "dataset_id": f"comext_{cn_code}",
                "latest_date": dt,
                "reporters": len(present),
                "missing_count": len(missing),
                "missing_countries": missing,
            })

if incomplete_alerts:
    for alert in incomplete_alerts:
        dt_str = alert["latest_date"].strftime("%B %Y")
        missing_names = [f"{COUNTRY_NAMES.get(c, c)} ({c})" for c in alert["missing_countries"]]

        if alert["missing_count"] == 0:
            st.success(f"**{alert['series']}** ({dt_str}): All 27 EU countries reporting")
        elif alert["missing_count"] <= 5:
            st.warning(
                f"**{alert['series']}** ({dt_str}): "
                f"{alert['reporters']}/27 EU countries reporting — "
                f"**{alert['missing_count']} missing**: {', '.join(missing_names)}"
            )
        else:
            with st.expander(
                f"\u26a0\ufe0f {alert['series']} ({dt_str}): "
                f"{alert['reporters']}/27 reporting — {alert['missing_count']} missing",
                expanded=False,
            ):
                st.markdown(f"**Missing countries** ({alert['missing_count']}):")
                for name in missing_names:
                    st.markdown(f"- {name}")
                st.caption(
                    "When many countries are missing from the latest period, "
                    "aggregated totals may appear artificially low. "
                    "Consider using the previous complete month for comparisons."
                )
else:
    st.success("All representative series have complete reporting for the latest period.")

st.divider()

# --- Sector sparklines ---
st.subheader(f"Sector Trends — {scope_name} Production Index (2021 = 100)")
st.caption(
    "Each sparkline shows the monthly production index for the sector's primary NACE code. "
    + ("Source: Eurostat STS — EU27_2020 aggregate" if is_aggregate
       else f"Source: Eurostat STS — {scope_name} ({scope_code})")
)

for sector_name, sector_info in SECTOR_GROUPS.items():
    nace_codes = sector_info["nace_codes"]
    if not nace_codes:
        continue

    for nace in nace_codes:
        key = f"sts_inpr_m_{nace}"
        df = data["sts"].get(key)
        if df is None:
            continue

        if is_aggregate:
            ts = df[df["country"] == "EU27_2020"].sort_values("date")
        else:
            ts = df[df["country"] == scope_code].sort_values("date")

        if not ts.empty and len(ts) > 3:
            col1, col2 = st.columns([1, 3])
            latest_val = ts["value"].iloc[-1]
            latest_dt = ts["date"].iloc[-1].strftime("%b %Y")
            col1.markdown(f"**{sector_name}** ({nace})")
            col1.caption(f"{sector_info['description']}\n\nLatest: {latest_val:.1f} ({latest_dt})")
            fig = sparkline(ts["value"].tolist())
            col2.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            break
