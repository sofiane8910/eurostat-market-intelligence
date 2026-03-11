"""
Interest Review — Deep Dive on Demand-Side Series Availability.
Comprehensive audit of all 30 demand-side series: country coverage,
granularity, and supply-side indicator availability.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import EU27_CODES, COUNTRY_NAMES
from data_loader import load_availability_data

st.title("Interest Review — Demand-Side Series Availability")
st.caption(
    "Comprehensive audit of all 30 demand-side series: country coverage, "
    "available indicators (production, turnover, prices, trade, confidence), "
    "and data freshness."
)

avail = load_availability_data()
summary = avail["summary"]
detail = avail["detail"]

if summary.empty:
    st.error(
        "Availability data not found. Run `python 'deep dive/collect_availability.py'` first."
    )
    st.stop()

# ---- Section 1: Summary KPIs ----
st.divider()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Series", len(summary))
c2.metric("With Production", int(summary["has_production"].sum()))
c3.metric("With Trade", int(summary["has_trade"].sum()))
c4.metric("Avg Country Coverage", f"{summary['total_countries'].mean():.1f}")
c5.metric("Full EU27 Coverage", int((summary["total_countries"] >= 27).sum()))

# ---- Section 2: Category filter ----
st.divider()
categories = ["All"] + sorted(summary["category"].unique().tolist())
cat_filter = st.selectbox("Filter by category", categories)

filtered = summary.copy()
if cat_filter != "All":
    filtered = filtered[filtered["category"] == cat_filter]

# ---- Section 3: Main table ----
st.subheader("Series Overview")

# Build display table
display = filtered[
    ["series_name", "category", "code_type", "code", "total_countries",
     "granularity", "has_production", "has_turnover", "has_prices",
     "has_trade", "has_confidence", "date_min", "date_max", "latest_data"]
].copy()

# Format indicator columns as checkmarks
for col in ["has_production", "has_turnover", "has_prices", "has_trade", "has_confidence"]:
    display[col] = display[col].map({True: "\u2705", False: "\u274c", "True": "\u2705", "False": "\u274c"})

display = display.rename(columns={
    "series_name": "Series Name",
    "category": "Category",
    "code_type": "Code Type",
    "code": "Code",
    "total_countries": "Countries",
    "granularity": "Granularity",
    "has_production": "Production",
    "has_turnover": "Turnover",
    "has_prices": "Prices",
    "has_trade": "Trade",
    "has_confidence": "Confidence",
    "date_min": "Date Min",
    "date_max": "Date Max",
    "latest_data": "Latest Data",
})


def _color_countries(val):
    try:
        v = int(val)
    except (ValueError, TypeError):
        return ""
    if v >= 20:
        return "background-color: #d4edda; color: #155724"
    elif v >= 10:
        return "background-color: #fff3cd; color: #856404"
    return "background-color: #f8d7da; color: #721c24"


styled = display.sort_values("Series Name")
st.dataframe(
    styled.style.applymap(_color_countries, subset=["Countries"]),
    use_container_width=True,
    height=min(900, len(styled) * 35 + 40),
)
st.caption(f"Showing {len(filtered)} of {len(summary)} series")

# ---- Section 4: Country coverage heatmap ----
st.divider()
st.subheader("Country Coverage Heatmap")
st.caption("Binary heatmap: which EU27 countries have data for each series")

# Build matrix from detail data
series_names = sorted(summary["series_name"].unique())
heatmap_data = []
for _, row in summary.iterrows():
    countries = set(str(row["country_list"]).split(";")) if pd.notna(row["country_list"]) and row["country_list"] else set()
    heatmap_data.append({
        "series": row["series_name"],
        **{c: (1 if c in countries else 0) for c in EU27_CODES}
    })

heatmap_df = pd.DataFrame(heatmap_data).set_index("series")
heatmap_df = heatmap_df.loc[sorted(heatmap_df.index)]

# Rename columns to country names
col_labels = [COUNTRY_NAMES.get(c, c) for c in EU27_CODES]

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_df.values,
    x=col_labels,
    y=heatmap_df.index.tolist(),
    colorscale=[[0, "white"], [1, "#2ca02c"]],
    showscale=False,
    hovertemplate="Series: %{y}<br>Country: %{x}<br>Available: %{z}<extra></extra>",
))
fig_heatmap.update_layout(
    height=max(500, len(heatmap_df) * 22),
    margin=dict(l=300, r=20, t=30, b=80),
    xaxis=dict(tickangle=45, side="bottom"),
    yaxis=dict(autorange="reversed"),
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ---- Section 5: Expandable details per series ----
st.divider()
st.subheader("Detailed Series Breakdown")

for _, srow in summary.sort_values("series_name").iterrows():
    name = srow["series_name"]
    code = srow["code"]
    with st.expander(f"{name} ({srow['code_type']} {code})"):
        # Country list
        countries = sorted(str(srow["country_list"]).split(";")) if pd.notna(srow["country_list"]) and srow["country_list"] else []
        country_names = [f"{c} ({COUNTRY_NAMES.get(c, c)})" for c in countries]
        st.markdown(f"**Countries ({len(countries)}):** {', '.join(country_names)}")

        # Datasets
        series_detail = detail[detail["code"] == code]
        if not series_detail.empty:
            st.markdown("**Available datasets:**")
            for _, drow in series_detail.iterrows():
                src = drow["data_source"]
                itype = drow["indicator_type"]
                dmin = drow["date_min"] if pd.notna(drow["date_min"]) else "N/A"
                dmax = drow["date_max"] if pd.notna(drow["date_max"]) else "N/A"
                cnt = drow["country_count"]
                st.markdown(f"- **{src}** ({itype}) — {cnt} countries, {dmin} to {dmax}")

        # Indicator summary
        indicators = []
        if srow["has_production"]: indicators.append("Production")
        if srow["has_turnover"]: indicators.append("Turnover")
        if srow["has_prices"]: indicators.append("Prices")
        if srow["has_trade"]: indicators.append("Trade")
        if srow["has_confidence"]: indicators.append("Confidence")
        st.markdown(f"**Indicator types:** {', '.join(indicators) if indicators else 'None'}")

# ---- Section 6: Supply indicator coverage bar chart ----
st.divider()
st.subheader("Supply Indicator Coverage by Category")
st.caption("How many series in each category have each indicator type")

indicator_cols = ["has_production", "has_turnover", "has_prices", "has_trade", "has_confidence"]
indicator_labels = ["Production", "Turnover", "Prices", "Trade", "Confidence"]

chart_rows = []
for cat in sorted(summary["category"].unique()):
    cat_df = summary[summary["category"] == cat]
    for col, label in zip(indicator_cols, indicator_labels):
        chart_rows.append({
            "Category": cat,
            "Indicator": label,
            "Count": int(cat_df[col].sum()),
        })

chart_df = pd.DataFrame(chart_rows)
fig_bar = px.bar(
    chart_df, x="Category", y="Count", color="Indicator",
    barmode="group",
    color_discrete_map={
        "Production": "#2ca02c", "Turnover": "#1f77b4",
        "Prices": "#ff7f0e", "Trade": "#9467bd", "Confidence": "#d62728",
    },
    title="Indicator Availability per Category",
)
fig_bar.update_layout(
    margin=dict(l=60, r=20, t=40, b=40),
    height=400,
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.caption(
    "Data generated by deep dive/collect_availability.py from Eurostat Comext & STS extracts. "
    "Country coverage reflects EU27 member states only."
)
