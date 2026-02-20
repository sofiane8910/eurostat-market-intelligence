"""
Trade Balance & China — Bilateral trade analysis, China competition.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    CN_DESCRIPTIONS, SUPPLY_CN_CODES, DEMAND_CN_CODES,
    EU27_CODES, AGGREGATE_CODES, COUNTRY_NAMES, SECTOR_GROUPS,
    freshness_footnote,
)
from charts import line_chart, dual_axis_chart, freshness_badge

st.title("Trade Balance & China Competition")
st.caption(
    "Analysis of EU27 bilateral trade with China across all tracked product categories. "
    "Source: Eurostat Comext DS-045409 — monthly trade in value (EUR) and volume (100 kg)"
)

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

all_cn_codes = list(data["comext"].keys())

# Get a representative freshness date for trade data
_sample_fr = next((v for k, v in data["freshness"].items() if k.startswith("comext_") and v.get("latest_date")), {})
_trade_footnote = freshness_footnote(_sample_fr.get("tier", 2), _sample_fr.get("latest_date"))

# --- Section 1: EU27 vs China Overview ---
st.subheader("EU27 Total Imports: World vs China — Monthly Trend")


@st.cache_data
def _compute_eu_china_totals(_comext_data, cn_codes):
    """Compute monthly EU27 import totals from WORLD and from China."""
    world_totals = {}
    china_totals = {}

    for cn_code in cn_codes:
        df = _comext_data.get(cn_code)
        if df is None:
            continue
        imp = df[(df["flow"] == "1") & (df["indicator"] == "VALUE_IN_EUROS") &
                 (~df["country"].isin(AGGREGATE_CODES))]

        for _, row in imp.iterrows():
            d = row["date"]
            v = row["value"]
            if pd.isna(v):
                continue
            if row["partner"] == "WORLD":
                world_totals[d] = world_totals.get(d, 0) + v
            elif row["partner"] == "CN":
                china_totals[d] = china_totals.get(d, 0) + v

    world_df = pd.DataFrame(list(world_totals.items()), columns=["date", "value"]).sort_values("date")
    china_df = pd.DataFrame(list(china_totals.items()), columns=["date", "value"]).sort_values("date")
    return world_df, china_df


scope = st.radio("Product scope", ["All Tracked Products", "Supply Materials Only", "Demand Products Only"],
                  horizontal=True, key="china_scope")
if scope == "Supply Materials Only":
    cn_subset = [c for c in all_cn_codes if c in SUPPLY_CN_CODES]
elif scope == "Demand Products Only":
    cn_subset = [c for c in all_cn_codes if c in DEMAND_CN_CODES]
else:
    cn_subset = all_cn_codes

world_totals, china_totals = _compute_eu_china_totals(data["comext"], cn_subset)

if not world_totals.empty and not china_totals.empty:
    both = pd.concat([world_totals, china_totals])
    date_range = f"{both['date'].min().strftime('%b %Y')} – {both['date'].max().strftime('%b %Y')}"
    st.plotly_chart(
        dual_axis_chart(world_totals, china_totals,
                        f"EU27 Monthly Import Value — {scope}, {date_range}",
                        y_label="Trade Value (EUR)",
                        world_label="Imports from World (total)",
                        china_label="Imports from China"),
        use_container_width=True,
    )
    st.caption(_trade_footnote)

    # China share over time
    merged = world_totals.merge(china_totals, on="date", suffixes=("_world", "_china"))
    merged["share"] = merged["value_china"] / merged["value_world"] * 100
    share_df = merged[["date", "share"]].assign(country="China's Share of EU27 Imports")
    st.plotly_chart(
        line_chart(share_df.rename(columns={"share": "value"}),
                   ["China's Share of EU27 Imports"],
                   f"China's Share of EU27 Imports Over Time — {scope}, {date_range}",
                   y_label="Share (%)"),
        use_container_width=True,
    )
    st.caption(_trade_footnote)

st.divider()

# --- Section 2: China Import Share by Product ---
st.subheader("China Import Share by Product — Cumulative over Full Period")
st.caption(
    "Percentage of total EU27 import value coming from China, "
    "summed across all available months. "
    "Red = >50% from China | Orange = 25-50% | Green = <25%"
)

shares = []
for cn_code in cn_subset:
    df = data["comext"].get(cn_code)
    if df is None:
        continue
    imp = df[(df["flow"] == "1") & (df["indicator"] == "VALUE_IN_EUROS") &
             (~df["country"].isin(AGGREGATE_CODES))]
    world_total = imp[imp["partner"] == "WORLD"]["value"].sum()
    china_total = imp[imp["partner"] == "CN"]["value"].sum()
    share = (china_total / world_total * 100) if world_total > 0 else 0
    desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
    shares.append({
        "cn_code": cn_code,
        "description": f"{desc} (CN {cn_code})",
        "share": share,
        "china_eur": china_total,
        "world_eur": world_total,
    })

shares_df = pd.DataFrame(shares).sort_values("share", ascending=False)

if not shares_df.empty:
    sdf = shares_df.sort_values("share", ascending=True)
    colors = ["#ef553b" if s > 50 else "#ffa15a" if s > 25 else "#00cc96" for s in sdf["share"]]

    fig = go.Figure(go.Bar(
        x=sdf["share"], y=sdf["description"],
        orientation="h", marker_color=colors,
        text=sdf["share"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="%{y}<br>China share: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title=f"China's Share of EU27 Imports by Product — {scope}",
        xaxis_title="China Share of Total EU27 Imports (%)", yaxis_title="",
        margin=dict(l=350, r=50, t=40, b=40),
        height=max(400, len(sdf) * 25),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(_trade_footnote)

    top3 = shares_df.nlargest(3, "share")
    st.markdown("**Key findings — products with highest China import dependence:**")
    for _, row in top3.iterrows():
        st.markdown(
            f"- **{row['description']}**: China accounts for **{row['share']:.1f}%** "
            f"of EU imports ({row['china_eur']/1e6:,.0f}M EUR cumulative)"
        )

st.divider()

# --- Section 3: Country Exposure to China ---
st.subheader("EU Country Exposure to Chinese Imports — by Product")
st.caption("For the selected product, how much of each EU country's imports come from China vs the rest of the world?")

cn_options = {f"{CN_DESCRIPTIONS.get(c, c)} (CN {c})": c for c in cn_subset if c in data["comext"]}
selected_cn = st.selectbox("Select product", list(cn_options.keys()), key="china_cn_code")
cn_code = cn_options[selected_cn]
cdf = data["comext"][cn_code]
product_name = CN_DESCRIPTIONS.get(cn_code, cn_code)

country_exposure = []
for country in EU27_CODES:
    imp = cdf[(cdf["country"] == country) & (cdf["flow"] == "1") & (cdf["indicator"] == "VALUE_IN_EUROS")]
    world = imp[imp["partner"] == "WORLD"]["value"].sum()
    china = imp[imp["partner"] == "CN"]["value"].sum()
    rest = world - china
    country_exposure.append({
        "country": country,
        "country_name": COUNTRY_NAMES.get(country, country),
        "china": china,
        "rest_of_world": rest,
        "total": world,
        "china_pct": (china / world * 100) if world > 0 else 0,
    })

exp_df = pd.DataFrame(country_exposure).sort_values("total", ascending=True)
exp_df = exp_df[exp_df["total"] > 0]

if not exp_df.empty:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=exp_df["country_name"], x=exp_df["china"],
        name="Imports from China", orientation="h", marker_color="#ef553b",
        hovertemplate="%{y}: %{x:,.0f} EUR from China<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=exp_df["country_name"], x=exp_df["rest_of_world"],
        name="Imports from rest of world", orientation="h", marker_color="#636efa",
        hovertemplate="%{y}: %{x:,.0f} EUR from others<extra></extra>",
    ))
    fig.update_layout(
        barmode="stack",
        title=f"Import Sources by EU Country — {product_name} (CN {cn_code})",
        xaxis_title="Cumulative Import Value (EUR)", yaxis_title="",
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=120, r=20, t=40, b=40),
        height=max(400, len(exp_df) * 22),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(_trade_footnote)

    top_dep = exp_df.nlargest(5, "china_pct")
    if not top_dep.empty:
        st.markdown(f"**Most China-dependent EU countries for {product_name} (CN {cn_code}):**")
        for _, row in top_dep.iterrows():
            st.markdown(
                f"- **{row['country_name']}**: {row['china_pct']:.1f}% of imports from China "
                f"({row['china']/1e6:,.1f}M EUR cumulative)"
            )

st.divider()

# --- Section 4: Intra-EU Trade ---
st.subheader(f"Intra-EU vs China Imports — {product_name} (CN {cn_code})")
st.caption("Comparison of trade within the EU single market vs imports from China")

intra_eu = 0
china_imp = 0
world_imp = 0
for country in EU27_CODES:
    imp = cdf[(cdf["country"] == country) & (cdf["flow"] == "1") & (cdf["indicator"] == "VALUE_IN_EUROS")]
    eu_partners = imp[imp["partner"].isin(EU27_CODES)]["value"].sum()
    cn_partner = imp[imp["partner"] == "CN"]["value"].sum()
    wd_partner = imp[imp["partner"] == "WORLD"]["value"].sum()
    intra_eu += eu_partners
    china_imp += cn_partner
    world_imp += wd_partner

col1, col2, col3 = st.columns(3)
col1.metric("Intra-EU Imports (cumulative)", f"{intra_eu/1e6:,.0f}M EUR")
col2.metric("Imports from China (cumulative)", f"{china_imp/1e6:,.0f}M EUR")
col3.metric("Total World Imports (cumulative)", f"{world_imp/1e6:,.0f}M EUR")

if world_imp > 0:
    intra_pct = intra_eu / world_imp * 100
    china_pct = china_imp / world_imp * 100
    st.info(
        f"**{product_name} (CN {cn_code})**: "
        f"Intra-EU trade represents **{intra_pct:.1f}%** of total imports | "
        f"China represents **{china_pct:.1f}%** of total imports"
    )
st.caption(_trade_footnote)

st.divider()

# --- Section 5: Trade Balance by Country ---
st.subheader(f"Net Trade Balance by EU Country — {product_name} (CN {cn_code})")
st.caption("Positive = net exporter (green) | Negative = net importer (red). Based on trade with all world partners.")

balance_data = []
for country in EU27_CODES:
    world_data = cdf[(cdf["country"] == country) & (cdf["partner"] == "WORLD") &
                      (cdf["indicator"] == "VALUE_IN_EUROS")]
    imp_total = world_data[world_data["flow"] == "1"]["value"].sum()
    exp_total = world_data[world_data["flow"] == "2"]["value"].sum()
    balance_data.append({
        "country": country,
        "country_name": COUNTRY_NAMES.get(country, country),
        "imports": imp_total,
        "exports": exp_total,
        "balance": exp_total - imp_total,
    })

bal_df = pd.DataFrame(balance_data).sort_values("balance")
bal_df = bal_df[bal_df["imports"] + bal_df["exports"] > 0]

if not bal_df.empty:
    colors = ["#00cc96" if b >= 0 else "#ef553b" for b in bal_df["balance"]]
    fig = go.Figure(go.Bar(
        x=bal_df["balance"], y=bal_df["country_name"],
        orientation="h", marker_color=colors,
        text=bal_df["balance"].apply(lambda v: f"{v/1e6:+,.0f}M"),
        textposition="outside",
        hovertemplate="%{y}: Net balance %{x:,.0f} EUR<extra></extra>",
    ))
    fig.update_layout(
        title=f"Net Trade Balance by Country — {product_name} (CN {cn_code})",
        xaxis_title="Net Trade Balance (EUR) — Exports minus Imports", yaxis_title="",
        margin=dict(l=120, r=70, t=40, b=40),
        height=max(400, len(bal_df) * 22),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(_trade_footnote)
