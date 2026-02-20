"""
Reusable Plotly chart builders for the Eurostat Labels Market Dashboard.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from constants import COUNTRY_NAMES


def _country_label(code: str) -> str:
    return COUNTRY_NAMES.get(code, code)


def line_chart(df: pd.DataFrame, countries: list[str], title: str,
               y_label: str = "Value") -> go.Figure:
    """Multi-country time series line chart."""
    fig = go.Figure()
    for country in countries:
        cdf = df[df["country"] == country].sort_values("date")
        if cdf.empty:
            continue
        fig.add_trace(go.Scatter(
            x=cdf["date"], y=cdf["value"],
            mode="lines+markers",
            name=_country_label(country),
            marker=dict(size=4),
            hovertemplate="%{x|%b %Y}: %{y:.1f}<extra>" + _country_label(country) + "</extra>",
        ))
    fig.update_layout(
        title=title, xaxis_title="", yaxis_title=y_label,
        hovermode="x unified", legend=dict(orientation="h", y=-0.15),
        margin=dict(l=60, r=20, t=40, b=40), height=400,
    )
    return fig


def bar_chart_latest(df: pd.DataFrame, countries: list[str], title: str,
                     y_label: str = "Value") -> go.Figure:
    """Bar chart of the latest available value per country."""
    latest_date = df["date"].max()
    latest = df[df["date"] == latest_date].copy()
    latest = latest[latest["country"].isin(countries)]
    latest = latest.sort_values("value", ascending=True)
    latest["label"] = latest["country"].map(_country_label)

    fig = go.Figure(go.Bar(
        x=latest["value"], y=latest["label"],
        orientation="h",
        text=latest["value"].apply(lambda v: f"{v:,.0f}"),
        textposition="outside",
        hovertemplate="%{y}: %{x:,.1f}<extra></extra>",
    ))
    fig.update_layout(
        title=f"{title} ({latest_date.strftime('%b %Y')})",
        xaxis_title=y_label, yaxis_title="",
        margin=dict(l=100, r=20, t=40, b=40),
        height=max(300, len(countries) * 25),
    )
    return fig


def heatmap_yoy(df: pd.DataFrame, countries: list[str], title: str) -> go.Figure:
    """YoY% change heatmap (country rows x month columns)."""
    pivot = df[df["country"].isin(countries)].copy()
    pivot["year"] = pivot["date"].dt.year
    pivot["month"] = pivot["date"].dt.month

    # Compute YoY change
    pivot = pivot.sort_values(["country", "date"])
    pivot["yoy"] = pivot.groupby(["country", "month"])["value"].pct_change() * 100

    # Pivot for heatmap
    pivot["date_str"] = pivot["date"].dt.strftime("%b %Y")
    heat = pivot.pivot_table(index="country", columns="date", values="yoy")
    heat.index = [_country_label(c) for c in heat.index]
    heat.columns = [c.strftime("%b %Y") for c in heat.columns]

    fig = go.Figure(go.Heatmap(
        z=heat.values,
        x=heat.columns,
        y=heat.index,
        colorscale="RdYlGn",
        zmid=0,
        text=heat.values.round(1),
        texttemplate="%{text:.1f}%",
        hovertemplate="Country: %{y}<br>Period: %{x}<br>YoY: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title=title, xaxis_title="", yaxis_title="",
        margin=dict(l=100, r=20, t=40, b=40),
        height=max(300, len(countries) * 22),
    )
    return fig


def sparkline(values: list, color: str = "#1f77b4") -> go.Figure:
    """Small inline sparkline for KPI cards."""
    fig = go.Figure(go.Scatter(
        y=values, mode="lines", line=dict(color=color, width=2),
        hoverinfo="skip",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=50, width=150,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


def trade_balance_chart(df: pd.DataFrame, partner: str = "WORLD",
                         indicator: str = "VALUE_IN_EUROS",
                         title: str = "Trade Balance") -> go.Figure:
    """Stacked import/export with net balance line."""
    imports = df[(df["flow"] == "1") & (df["partner"] == partner) & (df["indicator"] == indicator)]
    exports = df[(df["flow"] == "2") & (df["partner"] == partner) & (df["indicator"] == indicator)]

    imp_agg = imports.groupby("date")["value"].sum().reset_index().sort_values("date")
    exp_agg = exports.groupby("date")["value"].sum().reset_index().sort_values("date")

    merged = imp_agg.merge(exp_agg, on="date", suffixes=("_imp", "_exp"), how="outer").fillna(0)
    merged["balance"] = merged["value_exp"] - merged["value_imp"]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=merged["date"], y=merged["value_imp"], name="Imports",
                         marker_color="#ef553b", opacity=0.7))
    fig.add_trace(go.Bar(x=merged["date"], y=merged["value_exp"], name="Exports",
                         marker_color="#00cc96", opacity=0.7))
    fig.add_trace(go.Scatter(x=merged["date"], y=merged["balance"], name="Net Balance",
                             line=dict(color="black", width=2, dash="dash")))
    fig.update_layout(
        title=title, barmode="group",
        xaxis_title="", yaxis_title="Trade Value (EUR)" if "EUROS" in indicator else "Trade Volume (100 kg)",
        hovermode="x unified", legend=dict(orientation="h", y=-0.15),
        margin=dict(l=60, r=20, t=40, b=40), height=400,
    )
    return fig


def china_share_chart(df: pd.DataFrame, cn_codes: list[str],
                       cn_descriptions: dict, title: str = "China Import Share") -> go.Figure:
    """
    Horizontal bar chart: % of EU imports from China for each CN code.
    df should contain all partners (WORLD + CN).
    """
    shares = []
    for cn_code in cn_codes:
        imp = df[(df["flow"] == "1") & (df["indicator"] == "VALUE_IN_EUROS")]
        world = imp[imp["partner"] == "WORLD"]["value"].sum()
        china = imp[imp["partner"] == "CN"]["value"].sum()
        if world > 0:
            share = (china / world) * 100
        else:
            share = 0
        desc = cn_descriptions.get(cn_code, cn_code)
        shares.append({"cn_code": cn_code, "description": desc, "share": share})

    sdf = pd.DataFrame(shares).sort_values("share", ascending=True)

    colors = ["#ef553b" if s > 50 else "#ffa15a" if s > 25 else "#00cc96" for s in sdf["share"]]

    fig = go.Figure(go.Bar(
        x=sdf["share"], y=sdf["description"],
        orientation="h", marker_color=colors,
        text=sdf["share"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title=title, xaxis_title="China Share (%)", yaxis_title="",
        margin=dict(l=250, r=40, t=40, b=40),
        height=max(300, len(cn_codes) * 28),
    )
    return fig


def bilateral_flow_chart(df: pd.DataFrame, country: str,
                          indicator: str = "VALUE_IN_EUROS",
                          title: str = "") -> go.Figure:
    """Bar chart of trade partners for a specific reporting country."""
    imp = df[(df["country"] == country) & (df["flow"] == "1") &
             (df["indicator"] == indicator) & (df["partner"] != "WORLD")]
    partner_totals = imp.groupby("partner")["value"].sum().sort_values(ascending=True).tail(15)

    labels = [_country_label(p) for p in partner_totals.index]
    fig = go.Figure(go.Bar(
        x=partner_totals.values, y=labels,
        orientation="h",
        text=[f"{v:,.0f}" for v in partner_totals.values],
        textposition="outside",
        hovertemplate="%{y}: %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=title or f"Top Import Partners — {_country_label(country)}",
        xaxis_title="Trade Value (EUR)" if "EUROS" in indicator else "Trade Volume (100 kg)",
        yaxis_title="",
        margin=dict(l=100, r=20, t=40, b=40), height=400,
    )
    return fig


def freshness_badge(tier: int, latest_date, lag_days: int = None) -> str:
    """Return colored HTML badge for data freshness."""
    if latest_date is None:
        return '<span style="color: gray;">No data available</span>'
    date_str = latest_date.strftime("%B %Y") if hasattr(latest_date, "strftime") else str(latest_date)
    if tier == 1:
        return (f'<span style="background-color: #d4edda; color: #155724; padding: 2px 8px; '
                f'border-radius: 4px; font-size: 0.85em;">'
                f'Latest data: {date_str} — ~3 week lag (survey / prices)</span>')
    else:
        return (f'<span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; '
                f'border-radius: 4px; font-size: 0.85em;">'
                f'Latest data: {date_str} — ~6-8 week lag (hard data)</span>')
