"""
Competitive Landscape — Company-level intelligence for PSA label competitors.
Includes global overview, China deep-dive with per-company drill-down,
India competitors, and European & North American players.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from constants import (
    COMPETITOR_COUNTRIES, CHINA_COMPETITOR_DETAIL,
    KEY_FINANCIAL_METRICS, MARGIN_METRICS,
    CHINA_SUBSECTOR_CN_CODES, CN_DESCRIPTIONS,
    AGGREGATE_CODES, EU27_CODES, COUNTRY_NAMES,
)
from charts import (
    stock_price_chart, revenue_bar_chart, margin_trend_chart, line_chart,
)
from yfinance_helpers import (
    render_company_news, ticker_summary_table, get_ytd_return,
)

st.title("Competitive Landscape")
st.caption(
    "Company-level intelligence for PSA labels industry competitors. "
    "Stock prices, quarterly financials, and cross-reference with EU trade data."
)

data = st.session_state.get("data")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

yf_prices = data.get("yf_prices", pd.DataFrame())
yf_fin = data.get("yf_financials", pd.DataFrame())
yf_news = data.get("yf_news", pd.DataFrame())
comext = data.get("comext", {})

if yf_prices.empty:
    st.warning("No company data available. Check that yfinance CSV files exist in output2/.")
    st.stop()

# Filter to competitors only
comp_prices = yf_prices[yf_prices["group"] == "competitor"]
comp_fin = yf_fin[yf_fin["group"] == "competitor"] if not yf_fin.empty else pd.DataFrame()
comp_news = yf_news[yf_news["group"] == "competitor"] if not yf_news.empty else pd.DataFrame()
all_comp_tickers = sorted(comp_prices["ticker"].unique().tolist())

tab_global, tab_china, tab_india, tab_west = st.tabs([
    "Global Overview",
    "China Competitors",
    "India Competitors",
    "European & N. American",
])

# ===========================================================================
# TAB: Global Overview
# ===========================================================================
with tab_global:
    st.subheader("Global Competitor Overview")

    # KPI row for key players
    kpi_tickers = ["AVY", "CCL-B.TO", "UPM.HE"]
    kpi_cols = st.columns(len(kpi_tickers))
    for col, ticker in zip(kpi_cols, kpi_tickers):
        tdf = comp_prices[comp_prices["ticker"] == ticker].sort_values("date")
        if tdf.empty:
            continue
        company = tdf["company"].iloc[0]
        latest = tdf["close"].iloc[-1]
        ytd = get_ytd_return(comp_prices, ticker)
        ytd_str = f"{ytd:+.1f}%" if ytd is not None else "N/A"
        col.metric(company, f"{latest:.2f}", ytd_str)

    # Multiselect for all competitors
    ticker_names = {}
    for t in all_comp_tickers:
        tdf = comp_prices[comp_prices["ticker"] == t]
        if not tdf.empty:
            ticker_names[t] = tdf["company"].iloc[0]

    selected = st.multiselect(
        "Select competitors", all_comp_tickers,
        default=all_comp_tickers,
        format_func=lambda x: ticker_names.get(x, x),
        key="comp_global_tickers",
    )

    if selected:
        st.plotly_chart(
            stock_price_chart(comp_prices, selected,
                              "Competitor Stock Performance (Normalized to 100)",
                              normalize=True),
            use_container_width=True,
        )
        st.caption("Normalized to 100 at start date. Cross-currency comparison via relative returns.")

        # Revenue comparison
        if not comp_fin.empty:
            avail = comp_fin[
                (comp_fin["ticker"].isin(selected)) &
                (comp_fin["metric"] == "Total Revenue")
            ]
            if not avail.empty:
                st.plotly_chart(
                    revenue_bar_chart(comp_fin, selected, "Total Revenue",
                                      "Total Revenue by Quarter — All Competitors"),
                    use_container_width=True,
                )
                st.caption("Values in reporting currency. Use normalized returns for cross-company comparison.")

    st.markdown("**Latest News**")
    render_company_news(comp_news, selected if selected else all_comp_tickers, max_items=15)


# ===========================================================================
# TAB: China Competitors
# ===========================================================================
with tab_china:
    st.subheader("China Competitors — Deep Dive")

    china_tickers = [t[0] for t in COMPETITOR_COUNTRIES.get("China", [])]
    china_names = {t[0]: t[1] for t in COMPETITOR_COUNTRIES.get("China", [])}
    china_subsectors = {t[0]: t[2] for t in COMPETITOR_COUNTRIES.get("China", [])}

    if not china_tickers:
        st.info("No Chinese competitor data available.")
    else:
        # Section A: Overview of all 8
        st.markdown("### A. All Chinese Competitors")
        summary = ticker_summary_table(comp_prices, china_tickers,
                                        labels={t: china_subsectors.get(t, "") for t in china_tickers})
        if not summary.empty:
            st.dataframe(summary, use_container_width=True, hide_index=True)

        st.plotly_chart(
            stock_price_chart(comp_prices, china_tickers,
                              "Chinese Competitors — Stock Performance (Normalized)",
                              normalize=True),
            use_container_width=True,
        )

        # Section B: Breakdown by sub-sector
        st.markdown("### B. Sub-sector Breakdown")
        for subsector, tickers_info in CHINA_COMPETITOR_DETAIL.items():
            sub_tickers = [t[0] for t in tickers_info]
            sub_names = [t[1] for t in tickers_info]
            with st.expander(f"{subsector} ({len(sub_tickers)} companies: {', '.join(sub_names)})"):
                st.plotly_chart(
                    stock_price_chart(comp_prices, sub_tickers,
                                      f"{subsector} — Stock Comparison (Normalized)",
                                      normalize=True),
                    use_container_width=True,
                )

                if not comp_fin.empty:
                    for metric in ["Total Revenue", "EBITDA", "Net Income"]:
                        avail = comp_fin[
                            (comp_fin["ticker"].isin(sub_tickers)) &
                            (comp_fin["metric"] == metric)
                        ]
                        if not avail.empty:
                            st.plotly_chart(
                                revenue_bar_chart(comp_fin, sub_tickers, metric,
                                                  f"{metric} — {subsector}"),
                                use_container_width=True,
                            )

                    # Margin trends
                    for margin_name, (num, den) in MARGIN_METRICS.items():
                        fig = margin_trend_chart(comp_fin, sub_tickers,
                                                 num, den,
                                                 f"{margin_name} — {subsector}")
                        if fig.data:
                            st.plotly_chart(fig, use_container_width=True)

        # Section C: Individual company drill-down
        st.markdown("### C. Individual Company Drill-down")
        selected_china = st.selectbox(
            "Select company", china_tickers,
            format_func=lambda x: china_names.get(x, x),
            key="china_drilldown",
        )
        if selected_china:
            tdf = comp_prices[comp_prices["ticker"] == selected_china].sort_values("date")
            if not tdf.empty:
                company = tdf["company"].iloc[0]
                st.markdown(f"**{company}** ({selected_china}) — {china_subsectors.get(selected_china, '')}")

                # Stock price with volume
                import plotly.graph_objects as go
                from plotly.subplots import make_subplots

                fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                    vertical_spacing=0.03,
                                    row_heights=[0.7, 0.3])
                fig.add_trace(go.Scatter(
                    x=tdf["date"], y=tdf["close"],
                    mode="lines", name="Price",
                    hovertemplate="%{x|%b %d, %Y}: %{y:.2f}<extra>Price</extra>",
                ), row=1, col=1)
                if "volume" in tdf.columns:
                    fig.add_trace(go.Bar(
                        x=tdf["date"], y=tdf["volume"],
                        name="Volume", marker_color="rgba(100,100,200,0.3)",
                        hovertemplate="%{x|%b %d}: %{y:,.0f}<extra>Volume</extra>",
                    ), row=2, col=1)
                fig.update_layout(
                    title=f"{company} — Stock Price & Volume",
                    height=500, showlegend=False,
                    margin=dict(l=60, r=20, t=40, b=40),
                )
                fig.update_yaxes(title_text="Price (CNY)", row=1, col=1)
                fig.update_yaxes(title_text="Volume", row=2, col=1)
                st.plotly_chart(fig, use_container_width=True)

            # Financial metrics pivot table
            if not comp_fin.empty:
                cdf = comp_fin[
                    (comp_fin["ticker"] == selected_china) &
                    (comp_fin["metric"].isin(KEY_FINANCIAL_METRICS))
                ]
                if not cdf.empty:
                    pivot = cdf.pivot_table(index="metric", columns="quarter",
                                            values="value", aggfunc="first")
                    pivot = pivot.reindex(KEY_FINANCIAL_METRICS).dropna(how="all")
                    st.markdown("**Quarterly Financials (CNY)**")
                    st.dataframe(pivot.style.format("{:,.0f}", na_rep="—"),
                                 use_container_width=True)

                # Margin trends
                st.markdown("**Margin Trends**")
                for margin_name, (num, den) in MARGIN_METRICS.items():
                    fig = margin_trend_chart(comp_fin, [selected_china],
                                             num, den, f"{margin_name} — {company}")
                    if fig.data:
                        st.plotly_chart(fig, use_container_width=True)

            # Company news
            st.markdown("**Latest News**")
            render_company_news(comp_news, [selected_china], max_items=10)

        # Section D: Cross-reference with EU trade data
        st.markdown("### D. EU Imports from China — Trade Cross-reference")
        st.caption(
            "Eurostat Comext data showing EU27 member state imports from China "
            "for product codes matching each sub-sector. Each CN code shown individually."
        )

        subsector_sel = st.selectbox(
            "Sub-sector", list(CHINA_SUBSECTOR_CN_CODES.keys()),
            key="china_subsector_trade",
        )
        cn_codes_for_sub = CHINA_SUBSECTOR_CN_CODES.get(subsector_sel, [])
        available_cn = [c for c in cn_codes_for_sub if c in comext]

        if not available_cn:
            st.info(f"No Comext trade data available for {subsector_sel} CN codes.")
        else:
            for cn_code in available_cn:
                cdf = comext[cn_code]
                desc = CN_DESCRIPTIONS.get(cn_code, cn_code)

                # Filter: imports from China, individual EU countries
                china_imp = cdf[
                    (cdf["flow"] == "1") &
                    (cdf["partner"] == "CN") &
                    (cdf["indicator"] == "VALUE_IN_EUROS") &
                    (cdf["country"].isin(EU27_CODES))
                ]

                if china_imp.empty:
                    continue

                with st.expander(f"{desc} (CN {cn_code})", expanded=len(available_cn) <= 3):
                    # Get top importing countries
                    top_countries = (
                        china_imp.groupby("country")["value"].sum()
                        .sort_values(ascending=False).head(10).index.tolist()
                    )

                    if top_countries:
                        st.plotly_chart(
                            line_chart(china_imp, top_countries,
                                       f"EU Imports from China — {desc} (CN {cn_code})",
                                       y_label="Trade Value (EUR)"),
                            use_container_width=True,
                        )
                        st.caption(
                            f"Top {len(top_countries)} EU importing countries shown. "
                            "Source: Eurostat Comext DS-045409."
                        )


# ===========================================================================
# TAB: India Competitors
# ===========================================================================
with tab_india:
    st.subheader("India Competitors")

    india_tickers = [t[0] for t in COMPETITOR_COUNTRIES.get("India", [])]
    india_names = {t[0]: t[1] for t in COMPETITOR_COUNTRIES.get("India", [])}

    if not india_tickers:
        st.info("No Indian competitor data available.")
    else:
        summary = ticker_summary_table(comp_prices, india_tickers)
        if not summary.empty:
            st.dataframe(summary, use_container_width=True, hide_index=True)

        st.plotly_chart(
            stock_price_chart(comp_prices, india_tickers,
                              "Indian Competitors — Stock Performance",
                              normalize=False),
            use_container_width=True,
        )

        if not comp_fin.empty:
            for metric in KEY_FINANCIAL_METRICS:
                avail = comp_fin[
                    (comp_fin["ticker"].isin(india_tickers)) &
                    (comp_fin["metric"] == metric)
                ]
                if not avail.empty:
                    st.plotly_chart(
                        revenue_bar_chart(comp_fin, india_tickers, metric,
                                          f"{metric} — Indian Competitors"),
                        use_container_width=True,
                    )

            for margin_name, (num, den) in MARGIN_METRICS.items():
                fig = margin_trend_chart(comp_fin, india_tickers,
                                         num, den,
                                         f"{margin_name} — Indian Competitors")
                if fig.data:
                    st.plotly_chart(fig, use_container_width=True)

        # Cross-reference: EU film imports from India
        st.markdown("**EU Imports from India — Films**")
        st.caption("Cross-reference with Eurostat trade data for film CN codes.")
        film_cn_codes = CHINA_SUBSECTOR_CN_CODES.get("Films", [])
        avail_cn = [c for c in film_cn_codes if c in comext]
        for cn_code in avail_cn:
            cdf = comext[cn_code]
            desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
            india_imp = cdf[
                (cdf["flow"] == "1") &
                (cdf["partner"] == "IN") &
                (cdf["indicator"] == "VALUE_IN_EUROS") &
                (cdf["country"].isin(EU27_CODES))
            ]
            if india_imp.empty:
                continue
            top_c = (india_imp.groupby("country")["value"].sum()
                     .sort_values(ascending=False).head(8).index.tolist())
            if top_c:
                with st.expander(f"{desc} (CN {cn_code})"):
                    st.plotly_chart(
                        line_chart(india_imp, top_c,
                                   f"EU Imports from India — {desc}",
                                   y_label="Trade Value (EUR)"),
                        use_container_width=True,
                    )

        st.markdown("**Latest News**")
        render_company_news(comp_news, india_tickers, max_items=10)


# ===========================================================================
# TAB: European & N. American
# ===========================================================================
with tab_west:
    st.subheader("European & North American Competitors")

    country_groups = {
        "Finland": COMPETITOR_COUNTRIES.get("Finland", []),
        "France": COMPETITOR_COUNTRIES.get("France", []),
        "UK": COMPETITOR_COUNTRIES.get("UK", []),
        "US": COMPETITOR_COUNTRIES.get("US", []),
        "Canada": COMPETITOR_COUNTRIES.get("Canada", []),
    }

    for country, tickers_info in country_groups.items():
        if not tickers_info:
            continue
        tickers = [t[0] for t in tickers_info]
        names = [t[1] for t in tickers_info]
        available_tickers = [t for t in tickers if t in comp_prices["ticker"].values]
        if not available_tickers:
            continue

        with st.expander(f"{country} ({', '.join(names)})", expanded=True):
            summary = ticker_summary_table(comp_prices, available_tickers)
            if not summary.empty:
                st.dataframe(summary, use_container_width=True, hide_index=True)

            if len(available_tickers) > 1:
                st.plotly_chart(
                    stock_price_chart(comp_prices, available_tickers,
                                      f"{country} Competitors — Stock Performance (Normalized)",
                                      normalize=True),
                    use_container_width=True,
                )
            else:
                st.plotly_chart(
                    stock_price_chart(comp_prices, available_tickers,
                                      f"{names[0]} — Stock Performance"),
                    use_container_width=True,
                )

            if not comp_fin.empty:
                avail = comp_fin[
                    (comp_fin["ticker"].isin(available_tickers)) &
                    (comp_fin["metric"] == "Total Revenue")
                ]
                if not avail.empty:
                    st.plotly_chart(
                        revenue_bar_chart(comp_fin, available_tickers, "Total Revenue",
                                          f"Total Revenue — {country}"),
                        use_container_width=True,
                    )

                for margin_name, (num, den) in MARGIN_METRICS.items():
                    fig = margin_trend_chart(comp_fin, available_tickers,
                                             num, den,
                                             f"{margin_name} — {country}")
                    if fig.data:
                        st.plotly_chart(fig, use_container_width=True)

            render_company_news(comp_news, available_tickers, max_items=5)
