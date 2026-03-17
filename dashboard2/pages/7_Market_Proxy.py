"""
Market Proxy — yfinance company data for major European listed end-users.

Shows stock prices, quarterly financials, and latest news per application category.
"""

import streamlit as st
import pandas as pd

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dashboard"))

from constants2 import (
    MARKET_PROXY_TICKERS, CATEGORY_NAMES,
    PROXY_FINANCIAL_METRICS, PROXY_METRIC_DISPLAY,
)
from charts import sparkline

st.title("Market Proxy")
st.caption("Stock prices, quarterly financials, and news for major European listed end-users")

data = st.session_state.get("data2")
if data is None:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

yf_fin = data.get("yf_financials", pd.DataFrame())
yf_prices = data.get("yf_prices", pd.DataFrame())
yf_news = data.get("yf_news", pd.DataFrame())

if yf_prices.empty:
    st.warning(
        "No yfinance data found. Run `python extract_yfinance_db2.py` to fetch data into `data2/`."
    )
    st.stop()

# Category selector in sidebar
with st.sidebar:
    st.divider()
    st.subheader("Market Proxy")
    proxy_categories = list(MARKET_PROXY_TICKERS.keys())
    # Include all categories so we can show info messages for those without companies
    all_cats_with_proxy_status = []
    for cat in CATEGORY_NAMES:
        if cat in MARKET_PROXY_TICKERS:
            all_cats_with_proxy_status.append(f"{cat} ({len(MARKET_PROXY_TICKERS[cat])} companies)")
        else:
            all_cats_with_proxy_status.append(f"{cat} (no companies)")
    selected_label = st.selectbox(
        "Application Category",
        all_cats_with_proxy_status,
        key="market_proxy_cat",
    )
    cat_name = selected_label.split(" (")[0]

st.subheader(cat_name)

# Handle categories with no companies
if cat_name not in MARKET_PROXY_TICKERS:
    st.info(
        f"No listed company proxies available for **{cat_name}**. "
        "This category is covered by Eurostat STS indices only."
    )
    st.stop()

companies = MARKET_PROXY_TICKERS[cat_name]

# ---------------------------------------------------------------------------
# Render one column per company
# ---------------------------------------------------------------------------
cols = st.columns(len(companies))

for i, comp in enumerate(companies):
    ticker = comp["ticker"]
    with cols[i]:
        # --- Header ---
        st.markdown(f"**{comp['company']}**")
        st.caption(f"{ticker} | {comp['country']}")

        # --- Stock price metric + sparkline ---
        tk_prices = yf_prices[yf_prices["ticker"] == ticker].sort_values("date") if not yf_prices.empty else pd.DataFrame()

        if not tk_prices.empty and "close" in tk_prices.columns:
            latest_close = tk_prices["close"].iloc[-1]

            # 30-day % change
            days_30 = tk_prices.tail(22)  # ~22 trading days
            if len(days_30) >= 2:
                pct_30d = ((days_30["close"].iloc[-1] / days_30["close"].iloc[0]) - 1) * 100
                st.metric(
                    "Latest Close",
                    f"{latest_close:,.2f}",
                    delta=f"{pct_30d:+.1f}% (30d)",
                )
            else:
                st.metric("Latest Close", f"{latest_close:,.2f}")

            # 90-day sparkline
            close_vals = tk_prices["close"].dropna().tolist()
            if len(close_vals) >= 2:
                color = "#00cc96" if close_vals[-1] >= close_vals[0] else "#ef553b"
                st.plotly_chart(sparkline(close_vals, color=color), use_container_width=True)
        else:
            st.info("No price data")

        # --- Quarterly financials table ---
        if not yf_fin.empty:
            tk_fin = yf_fin[yf_fin["ticker"] == ticker]
            tk_fin = tk_fin[tk_fin["metric"].isin(PROXY_FINANCIAL_METRICS)]
        else:
            tk_fin = pd.DataFrame()

        if not tk_fin.empty:
            # Get currency
            currency = tk_fin["currency"].iloc[0] if "currency" in tk_fin.columns else ""

            # Pivot: rows=metric, cols=period
            pivot = tk_fin.pivot_table(
                index="metric", columns="quarter", values="value", aggfunc="first"
            )
            # Sort columns chronologically, keep last 5
            sorted_cols = sorted(pivot.columns)[-5:]
            pivot = pivot.reindex(columns=sorted_cols)

            # Reorder rows
            row_order = [m for m in PROXY_FINANCIAL_METRICS if m in pivot.index]
            pivot = pivot.reindex(row_order)

            # Compute YoY % change per metric
            pct_change = pivot.pct_change(axis=1) * 100

            # Build display with value + % change
            display_name = {m: PROXY_METRIC_DISPLAY.get(m, m) for m in pivot.index}

            def _fmt_cell(val, chg):
                if pd.isna(val):
                    return "—"
                s = f"{val/1e6:,.0f}M"
                if pd.notna(chg):
                    sign = "+" if chg >= 0 else ""
                    s += f" ({sign}{chg:.0f}%)"
                return s

            formatted = pivot.copy()
            for col in pivot.columns:
                for row in pivot.index:
                    formatted.loc[row, col] = _fmt_cell(
                        pivot.loc[row, col], pct_change.loc[row, col]
                    )
            formatted.index = [display_name[m] for m in formatted.index]

            period_type = tk_fin["period_type"].iloc[0] if "period_type" in tk_fin.columns else "annual"
            label = "Quarterly" if period_type == "quarterly" else "Annual"
            if currency:
                st.caption(f"{label} financials ({currency} millions)")
            else:
                st.caption(f"{label} financials (millions)")
            st.dataframe(formatted, use_container_width=True)
        else:
            st.caption("_No quarterly financials available_")

        # --- Latest 3 news headlines ---
        if not yf_news.empty:
            tk_news = yf_news[yf_news["ticker"] == ticker].head(3)
        else:
            tk_news = pd.DataFrame()

        if not tk_news.empty:
            st.caption("Latest news")
            for _, article in tk_news.iterrows():
                title = article.get("title", "")
                link = article.get("link", "")
                publisher = article.get("publisher", "")
                if title:
                    if link:
                        st.markdown(f"- [{title}]({link})")
                    else:
                        st.markdown(f"- {title}")
                    if publisher:
                        st.caption(f"  _{publisher}_")
        else:
            st.caption("_No recent news_")

        st.divider()
