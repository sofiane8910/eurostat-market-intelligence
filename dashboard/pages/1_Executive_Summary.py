"""
Executive Summary — KPIs, sparklines, freshness indicators.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import AGGREGATE_CODES, EU27_CODES, SECTOR_GROUPS, freshness_footnote
from data_loader import get_eu27_aggregate
from charts import sparkline, freshness_badge

st.title("Executive Summary — European Labels Market")
st.caption("Key performance indicators across supply and demand sides of the EU27 labels industry")

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

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

# --- KPI Cards ---
st.subheader("Key Indicators — EU27 Aggregate")


def _get_sts_eu27(key: str):
    """Get EU27 time series from STS data."""
    df = data["sts"].get(key)
    if df is None:
        return None, None, None, None
    eu = df[df["country"] == "EU27_2020"].sort_values("date")
    if eu.empty:
        eu = df[df["country"] == "EA20"].sort_values("date")
    if eu.empty or len(eu) < 2:
        return None, None, None, None
    latest_val = eu["value"].iloc[-1]
    latest_date = eu["date"].iloc[-1]
    prev_val = eu["value"].iloc[-2]
    mom = ((latest_val - prev_val) / abs(prev_val) * 100) if prev_val != 0 else 0
    yoy_date = latest_date - pd.DateOffset(years=1)
    yoy_row = eu[eu["date"] == yoy_date]
    yoy = None
    if not yoy_row.empty:
        yoy_val = yoy_row["value"].iloc[0]
        if yoy_val != 0:
            yoy = (latest_val - yoy_val) / abs(yoy_val) * 100
    return latest_val, mom, yoy, latest_date


def _kpi_card(col, label, value, mom, yoy, latest_date, tier_key=""):
    """Render a KPI card in a column with explicit date and lag info."""
    freshness = data["freshness"].get(tier_key, {})
    tier = freshness.get("tier", 2)
    dot = "🟢" if tier == 1 else "🟠"
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
        col.caption(f"No EU27 data available ({lag_text})")


# Row 1: Supply-side KPIs
st.markdown("### Supply Side — Raw Materials & Packaging")
c1, c2, c3, c4 = st.columns(4)

val, mom, yoy, dt = _get_sts_eu27("ei_bssi_m_r2_C17")
_kpi_card(c1, "Paper & Board Confidence (C17)", val, mom, yoy, dt, "ei_bssi_m_r2_C17")

val, mom, yoy, dt = _get_sts_eu27("sts_inpr_m_C222")
_kpi_card(c2, "Plastics Production Index (C222)", val, mom, yoy, dt, "sts_inpr_m_C222")

val, mom, yoy, dt = _get_sts_eu27("sts_inpp_m_C17")
_kpi_card(c3, "Paper Producer Prices (C17)", val, mom, yoy, dt, "sts_inpp_m_C17")

val, mom, yoy, dt = _get_sts_eu27("sts_inpr_m_C203")
_kpi_card(c4, "Inks & Varnish Production (C203)", val, mom, yoy, dt, "sts_inpr_m_C203")

# Row 2: Demand-side KPIs
st.markdown("### Demand Side — End-Market Sectors")
c1, c2, c3, c4 = st.columns(4)

val, mom, yoy, dt = _get_sts_eu27("sts_inpr_m_C10")
_kpi_card(c1, "Food Production Index (C10)", val, mom, yoy, dt, "sts_inpr_m_C10")

val, mom, yoy, dt = _get_sts_eu27("sts_inpr_m_C11")
_kpi_card(c2, "Beverages Production Index (C11)", val, mom, yoy, dt, "sts_inpr_m_C11")

val, mom, yoy, dt = _get_sts_eu27("sts_inpr_m_C21")
_kpi_card(c3, "Pharma Production Index (C21)", val, mom, yoy, dt, "sts_inpr_m_C21")

val, mom, yoy, dt = _get_sts_eu27("sts_trtu_m_G47_FOOD")
_kpi_card(c4, "Food Retail Turnover (G47_FOOD)", val, mom, yoy, dt, "sts_trtu_m_G47_FOOD")

# Row 3: Trade + China
st.markdown("### Trade Overview — Supply Materials (Comext)")
c1, c2, c3 = st.columns(3)

supply_codes = [c[0] for c in data["meta"]["comext_codes"] if c[2] == "supply"]
total_supply_imp = 0
total_supply_exp = 0
trade_latest_date = None
for cn_code in supply_codes:
    cdf = data["comext"].get(cn_code)
    if cdf is not None:
        world_imp = cdf[(cdf["partner"] == "WORLD") & (cdf["flow"] == "1") & (cdf["indicator"] == "VALUE_IN_EUROS")]
        world_exp = cdf[(cdf["partner"] == "WORLD") & (cdf["flow"] == "2") & (cdf["indicator"] == "VALUE_IN_EUROS")]
        latest_date = world_imp["date"].max() if not world_imp.empty else None
        if latest_date:
            trade_latest_date = latest_date
            total_supply_imp += world_imp[world_imp["date"] == latest_date]["value"].sum()
            total_supply_exp += world_exp[world_exp["date"] == latest_date]["value"].sum()

trade_date_str = trade_latest_date.strftime("%B %Y") if trade_latest_date else "N/A"
c1.metric(f"Total Supply Imports ({trade_date_str})", f"{total_supply_imp/1e6:,.0f}M EUR")
c2.metric(f"Total Supply Exports ({trade_date_str})", f"{total_supply_exp/1e6:,.0f}M EUR")
c3.metric(f"Net Trade Balance ({trade_date_str})", f"{(total_supply_exp - total_supply_imp)/1e6:+,.0f}M EUR")
st.caption(f"Source: Eurostat Comext (DS-045409) | Data as of {trade_date_str} | ~6-8 week publication lag")

# China imports total
total_china_imp = 0
for cn_code in supply_codes:
    cdf = data["comext"].get(cn_code)
    if cdf is not None:
        cn_imp = cdf[(cdf["partner"] == "CN") & (cdf["flow"] == "1") & (cdf["indicator"] == "VALUE_IN_EUROS")]
        if not cn_imp.empty:
            latest_date = cn_imp["date"].max()
            total_china_imp += cn_imp[cn_imp["date"] == latest_date]["value"].sum()

if total_supply_imp > 0:
    china_pct = total_china_imp / total_supply_imp * 100
    st.info(
        f"**China Competition ({trade_date_str})**: China accounts for **{china_pct:.1f}%** "
        f"of total EU supply material imports "
        f"({total_china_imp/1e6:,.0f}M EUR out of {total_supply_imp/1e6:,.0f}M EUR)"
    )

st.divider()

# --- Sector sparklines ---
st.subheader("Sector Trends — EU27 Production Index (2021 = 100)")
st.caption("Each sparkline shows the EU27 monthly production index for the sector's primary NACE code")

for sector_name, sector_info in SECTOR_GROUPS.items():
    nace_codes = sector_info["nace_codes"]
    if not nace_codes:
        continue

    for nace in nace_codes:
        key = f"sts_inpr_m_{nace}"
        df = data["sts"].get(key)
        if df is not None:
            eu = df[df["country"] == "EU27_2020"].sort_values("date")
            if not eu.empty and len(eu) > 3:
                col1, col2 = st.columns([1, 3])
                latest_val = eu["value"].iloc[-1]
                latest_dt = eu["date"].iloc[-1].strftime("%b %Y")
                col1.markdown(f"**{sector_name}** ({nace})")
                col1.caption(f"{sector_info['description']}\n\nLatest: {latest_val:.1f} ({latest_dt})")
                fig = sparkline(eu["value"].tolist())
                col2.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                break
