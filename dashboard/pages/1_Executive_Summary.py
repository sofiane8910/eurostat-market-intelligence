"""
Executive Summary — KPIs, sparklines, freshness indicators.
Supports filtering by EU27 aggregate or individual country.
Detects incomplete latest periods (late-reporting countries).
Click any KPI to pop out the full time series (2023–present).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    AGGREGATE_CODES, EU27_CODES, COUNTRY_NAMES, SECTOR_GROUPS,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS,
    SUPPLY_CN_CODES, DEMAND_CN_CODES, CN_DESCRIPTIONS,
    freshness_footnote,
)
from data_loader import get_eu27_aggregate
from charts import sparkline, freshness_badge, line_chart

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
    if cdf is None or cdf.empty:
        return None, [], EU27_CODES.copy()
    sub = cdf[
        (cdf["partner"] == "WORLD") & (cdf["flow"] == flow) &
        (cdf["indicator"] == indicator) & (~cdf["country"].isin(AGGREGATE_CODES))
    ]
    return _detect_incomplete_period(sub)


# --- Helper: get time series for selected scope ---
def _get_sts_series(key: str):
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


# --- Dialog: full time series chart ---
@st.dialog("Time Series Detail", width="large")
def _show_chart(sts_key: str, label: str):
    """Pop-out dialog showing the full time series from 2023 to present."""
    # Parse dataset and NACE from key
    parts = sts_key.rsplit("_", 1)
    dataset = parts[0] if len(parts) == 2 else sts_key
    nace = parts[1] if len(parts) == 2 else ""
    ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
    nace_desc = NACE_DESCRIPTIONS.get(nace, nace)

    df = data["sts"].get(sts_key)
    if df is None:
        st.warning(f"No data found for {label}")
        return

    # Get the series for current scope
    if is_aggregate:
        ts = df[df["country"] == "EU27_2020"].sort_values("date")
        if ts.empty:
            ts = df[df["country"] == "EA20"].sort_values("date")
    else:
        ts = df[df["country"] == scope_code].sort_values("date")

    if ts.empty:
        st.warning(f"No data for {scope_name}")
        return

    # Metadata
    fr = data["freshness"].get(sts_key, {})
    tier = fr.get("tier", 2)
    lag_text = "~3 week lag (survey/price)" if tier == 1 else "~6-8 week lag (hard data)"

    st.markdown(f"### {label}")
    st.caption(
        f"**Dataset**: {ds_desc} (`{dataset}`) | **Sector**: {nace_desc} (`{nace}`) | "
        f"**Scope**: {scope_name} | **Publication lag**: {lag_text}"
    )

    # Determine y-axis label
    is_confidence = "confidence" in ds_desc.lower() or "ei_bs" in dataset
    if is_confidence:
        y_label = "Confidence Balance (pp)"
    elif "price" in ds_desc.lower() or "inpp" in dataset or "inpi" in dataset:
        y_label = "Price Index (2021 = 100)"
    elif "turnover" in ds_desc.lower() or "trtu" in dataset:
        y_label = "Turnover Index (2021 = 100)"
    else:
        y_label = "Production Index (2021 = 100)"

    date_range = f"{ts['date'].min().strftime('%b %Y')} \u2013 {ts['date'].max().strftime('%b %Y')}"

    # Build detailed chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts["date"], y=ts["value"],
        mode="lines+markers",
        name=scope_name,
        line=dict(width=2.5, color="#1f77b4"),
        marker=dict(size=4),
        hovertemplate="%{x|%b %Y}: %{y:.1f}<extra>" + scope_name + "</extra>",
    ))

    # Add reference line at 100 for indices
    if not is_confidence:
        fig.add_hline(y=100, line_dash="dot", line_color="gray", opacity=0.5,
                       annotation_text="Base = 100 (2021)", annotation_position="bottom right")

    # Add YoY shading
    latest = ts["date"].max()
    one_year_ago = latest - pd.DateOffset(years=1)
    fig.add_vrect(x0=one_year_ago, x1=latest,
                   fillcolor="lightblue", opacity=0.08,
                   annotation_text="Last 12 months", annotation_position="top left")

    fig.update_layout(
        title=f"{label} \u2014 {scope_name}, {date_range}",
        xaxis_title="", yaxis_title=y_label,
        hovermode="x unified",
        margin=dict(l=60, r=20, t=50, b=40), height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Stats table
    st.markdown("#### Summary Statistics")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Latest", f"{ts['value'].iloc[-1]:.1f}")
    c2.metric("Min (period)", f"{ts['value'].min():.1f}")
    c3.metric("Max (period)", f"{ts['value'].max():.1f}")
    c4.metric("Mean (period)", f"{ts['value'].mean():.1f}")
    c5.metric("Observations", f"{len(ts)}")

    # MoM and YoY detail
    if len(ts) >= 2:
        prev = ts["value"].iloc[-2]
        mom_pct = (ts["value"].iloc[-1] - prev) / abs(prev) * 100 if prev != 0 else 0
        st.caption(
            f"Month-on-month: **{mom_pct:+.1f}%** "
            f"({prev:.1f} \u2192 {ts['value'].iloc[-1]:.1f})"
        )

    yoy_date = latest - pd.DateOffset(years=1)
    yoy_row = ts[ts["date"] == yoy_date]
    if not yoy_row.empty:
        yoy_val = yoy_row["value"].iloc[0]
        yoy_pct = (ts["value"].iloc[-1] - yoy_val) / abs(yoy_val) * 100 if yoy_val != 0 else 0
        st.caption(
            f"Year-on-year: **{yoy_pct:+.1f}%** "
            f"({yoy_val:.1f} in {yoy_date.strftime('%b %Y')} \u2192 {ts['value'].iloc[-1]:.1f} in {latest.strftime('%b %Y')})"
        )

    # Incomplete period check
    dt_check, present, missing = _detect_incomplete_period(df)
    if dt_check and missing:
        missing_names = [f"{COUNTRY_NAMES.get(c, c)} ({c})" for c in missing]
        st.warning(
            f"**Latest period ({dt_check.strftime('%b %Y')})**: "
            f"{len(present)}/27 EU countries reporting. "
            f"Missing: {', '.join(missing_names)}"
        )

    st.caption(freshness_footnote(tier, fr.get("latest_date")))


# --- Trade dialog ---
@st.dialog("Trade Time Series Detail", width="large")
def _show_trade_chart(cn_code: str, label: str, flow: str = "1"):
    """Pop-out dialog for Comext trade time series."""
    cdf = data["comext"].get(cn_code)
    if cdf is None:
        st.warning(f"No trade data for {label}")
        return

    desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
    flow_name = "Imports" if flow == "1" else "Exports"

    st.markdown(f"### {desc} (CN {cn_code}) \u2014 {flow_name}")
    st.caption(
        f"**Source**: Eurostat Comext DS-045409 | **Scope**: {scope_name} | "
        f"**Publication lag**: ~6-8 weeks"
    )

    if is_aggregate:
        world = cdf[
            (cdf["partner"] == "WORLD") & (cdf["flow"] == flow) &
            (cdf["indicator"] == "VALUE_IN_EUROS") & (~cdf["country"].isin(AGGREGATE_CODES))
        ].groupby("date")["value"].sum().reset_index().sort_values("date")
        china = cdf[
            (cdf["partner"] == "CN") & (cdf["flow"] == flow) &
            (cdf["indicator"] == "VALUE_IN_EUROS") & (~cdf["country"].isin(AGGREGATE_CODES))
        ].groupby("date")["value"].sum().reset_index().sort_values("date")
    else:
        world = cdf[
            (cdf["country"] == scope_code) & (cdf["partner"] == "WORLD") &
            (cdf["flow"] == flow) & (cdf["indicator"] == "VALUE_IN_EUROS")
        ][["date", "value"]].sort_values("date")
        china = cdf[
            (cdf["country"] == scope_code) & (cdf["partner"] == "CN") &
            (cdf["flow"] == flow) & (cdf["indicator"] == "VALUE_IN_EUROS")
        ][["date", "value"]].sort_values("date")

    if world.empty:
        st.warning(f"No trade data for {scope_name}")
        return

    date_range = f"{world['date'].min().strftime('%b %Y')} \u2013 {world['date'].max().strftime('%b %Y')}"

    if not china.empty:
        from plotly.subplots import make_subplots
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=world["date"], y=world["value"],
            mode="lines+markers", name=f"{flow_name} from World",
            line=dict(width=2.5, color="#1f77b4"), marker=dict(size=4),
            hovertemplate="%{x|%b %Y}: %{y:,.0f} EUR<extra>World</extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=china["date"], y=china["value"],
            mode="lines+markers", name=f"{flow_name} from China",
            line=dict(width=2.5, color="#ef553b"), marker=dict(size=4),
            hovertemplate="%{x|%b %Y}: %{y:,.0f} EUR<extra>China</extra>",
        ), secondary_y=True)
        fig.update_layout(
            title=f"{desc} (CN {cn_code}) \u2014 {scope_name} {flow_name}, {date_range}",
            xaxis_title="", hovermode="x unified",
            legend=dict(orientation="h", y=-0.15),
            margin=dict(l=60, r=60, t=50, b=40), height=500,
        )
        fig.update_yaxes(title_text="Trade Value (EUR) \u2014 World", secondary_y=False,
                          title_font=dict(color="#1f77b4"), tickfont=dict(color="#1f77b4"))
        fig.update_yaxes(title_text="Trade Value (EUR) \u2014 China", secondary_y=True,
                          title_font=dict(color="#ef553b"), tickfont=dict(color="#ef553b"))
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=world["date"], y=world["value"],
            mode="lines+markers", name=f"{flow_name} from World",
            line=dict(width=2.5, color="#1f77b4"), marker=dict(size=4),
            hovertemplate="%{x|%b %Y}: %{y:,.0f} EUR<extra>World</extra>",
        ))
        fig.update_layout(
            title=f"{desc} (CN {cn_code}) \u2014 {scope_name} {flow_name}, {date_range}",
            xaxis_title="", yaxis_title="Trade Value (EUR)",
            hovermode="x unified", legend=dict(orientation="h", y=-0.15),
            margin=dict(l=60, r=20, t=50, b=40), height=500,
        )
    st.plotly_chart(fig, use_container_width=True)

    # Stats
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Latest Month ({world['date'].max().strftime('%b %Y')})",
              f"{world['value'].iloc[-1]/1e6:,.1f}M EUR")
    c2.metric("Period Total", f"{world['value'].sum()/1e6:,.0f}M EUR")
    if not china.empty and world["value"].sum() > 0:
        share = china["value"].sum() / world["value"].sum() * 100
        c3.metric("China Share (cumulative)", f"{share:.1f}%")

    # Incomplete period
    dt_check, present, missing = _detect_incomplete_comext(cdf, flow=flow)
    if dt_check and missing:
        missing_names = [f"{COUNTRY_NAMES.get(c, c)} ({c})" for c in missing]
        st.warning(
            f"**Latest period ({dt_check.strftime('%b %Y')})**: "
            f"{len(present)}/27 EU countries reporting. "
            f"Missing: {', '.join(missing_names)}"
        )

    fr = data["freshness"].get(f"comext_{cn_code}", {})
    st.caption(freshness_footnote(2, fr.get("latest_date")))


# --- KPI card with clickable button ---
def _kpi_card(col, label, value, mom, yoy, latest_date, tier_key="", button_key=""):
    """Render a KPI card with a 'View chart' button that opens the dialog."""
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

    if col.button("View chart", key=button_key, use_container_width=True):
        _show_chart(tier_key, label)


# --- KPI Cards ---
st.subheader(f"Key Indicators — {scope_name}")
st.caption("Click **View chart** on any indicator to see the full time series from 2023 to present")

# Row 1: Supply-side KPIs
st.markdown("### Supply Side — Raw Materials & Packaging")
c1, c2, c3, c4 = st.columns(4)

val, mom, yoy, dt, _ = _get_sts_series("ei_bssi_m_r2_C17")
_kpi_card(c1, "Paper & Board Confidence (C17)", val, mom, yoy, dt,
          "ei_bssi_m_r2_C17", "btn_ei_bssi_C17")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C222")
_kpi_card(c2, "Plastics Production Index (C222)", val, mom, yoy, dt,
          "sts_inpr_m_C222", "btn_inpr_C222")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpp_m_C17")
_kpi_card(c3, "Paper Producer Prices (C17)", val, mom, yoy, dt,
          "sts_inpp_m_C17", "btn_inpp_C17")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C203")
_kpi_card(c4, "Inks & Varnish Production (C203)", val, mom, yoy, dt,
          "sts_inpr_m_C203", "btn_inpr_C203")

# Row 2: Demand-side KPIs
st.markdown("### Demand Side — End-Market Sectors")
c1, c2, c3, c4 = st.columns(4)

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C10")
_kpi_card(c1, "Food Production Index (C10)", val, mom, yoy, dt,
          "sts_inpr_m_C10", "btn_inpr_C10")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C11")
_kpi_card(c2, "Beverages Production Index (C11)", val, mom, yoy, dt,
          "sts_inpr_m_C11", "btn_inpr_C11")

val, mom, yoy, dt, _ = _get_sts_series("sts_inpr_m_C21")
_kpi_card(c3, "Pharma Production Index (C21)", val, mom, yoy, dt,
          "sts_inpr_m_C21", "btn_inpr_C21")

val, mom, yoy, dt, _ = _get_sts_series("sts_trtu_m_G47_FOOD")
_kpi_card(c4, "Food Retail Turnover (G47_FOOD)", val, mom, yoy, dt,
          "sts_trtu_m_G47_FOOD", "btn_trtu_G47")

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

# Trade product drill-down buttons
st.markdown("**Drill into trade by product** (click to see full time series):")
trade_cols = st.columns(4)
top_supply = supply_codes[:8]  # show up to 8 buttons
for i, cn_code in enumerate(top_supply):
    desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
    short = desc[:35] + "..." if len(desc) > 35 else desc
    col = trade_cols[i % 4]
    if col.button(f"{short} (CN {cn_code})", key=f"btn_trade_{cn_code}", use_container_width=True):
        _show_trade_chart(cn_code, desc, flow="1")

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

incomplete_alerts = []
representative_sts = [
    ("sts_inpr_m_C17", "Production in industry \u2014 Paper (C17)"),
    ("sts_inpr_m_C222", "Production in industry \u2014 Plastics (C222)"),
    ("sts_trtu_m_G47_FOOD", "Retail trade turnover \u2014 Food (G47_FOOD)"),
]

for sts_key, sts_label in representative_sts:
    df = data["sts"].get(sts_key)
    if df is not None:
        dt, present, missing = _detect_incomplete_period(df)
        if dt and missing:
            incomplete_alerts.append({
                "series": sts_label,
                "latest_date": dt,
                "reporters": len(present),
                "missing_count": len(missing),
                "missing_countries": missing,
            })

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
                f"{alert['reporters']}/27 EU countries reporting \u2014 "
                f"**{alert['missing_count']} missing**: {', '.join(missing_names)}"
            )
        else:
            with st.expander(
                f"\u26a0\ufe0f {alert['series']} ({dt_str}): "
                f"{alert['reporters']}/27 reporting \u2014 {alert['missing_count']} missing",
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
    + ("Source: Eurostat STS \u2014 EU27_2020 aggregate" if is_aggregate
       else f"Source: Eurostat STS \u2014 {scope_name} ({scope_code})")
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
