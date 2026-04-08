"""
Helper utilities for yfinance company data in the dashboard.
"""

import pandas as pd
import streamlit as st

from constants import SECTOR_TO_YFINANCE


def get_tickers_for_sector(sector_name: str, yf_prices: pd.DataFrame) -> list[str]:
    """Return list of tickers matching a sector, using SECTOR_TO_YFINANCE mapping."""
    if yf_prices.empty or sector_name not in SECTOR_TO_YFINANCE:
        return []
    keys = SECTOR_TO_YFINANCE[sector_name]
    tickers = []
    for group, sector in keys:
        match = yf_prices[(yf_prices["group"] == group) & (yf_prices["sector"] == sector)]
        tickers.extend(match["ticker"].unique().tolist())
    return sorted(set(tickers))


def render_company_news(news_df: pd.DataFrame, tickers: list[str],
                        max_items: int = 10):
    """Render news items as markdown links in Streamlit."""
    if news_df.empty:
        st.info("No news available.")
        return
    filtered = news_df[news_df["ticker"].isin(tickers)].head(max_items)
    if filtered.empty:
        st.info("No news available for selected companies.")
        return
    for _, row in filtered.iterrows():
        title = row.get("title", "")
        link = row.get("link", "")
        publisher = row.get("publisher", "")
        company = row.get("company", "")
        source = f" — {publisher}" if publisher else ""
        prefix = f"**{company}**: " if company else ""
        if link:
            st.markdown(f"- {prefix}[{title}]({link}){source}")
        else:
            st.markdown(f"- {prefix}{title}{source}")


def normalize_prices(df: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """Rebase price series to 100 at first available date for each ticker."""
    parts = []
    for ticker in tickers:
        tdf = df[df["ticker"] == ticker].sort_values("date").copy()
        if tdf.empty or tdf["close"].iloc[0] == 0:
            continue
        tdf["normalized"] = tdf["close"] / tdf["close"].iloc[0] * 100
        parts.append(tdf)
    if parts:
        return pd.concat(parts, ignore_index=True)
    return pd.DataFrame()


def get_ytd_return(df: pd.DataFrame, ticker: str) -> float | None:
    """Compute YTD return % for a ticker."""
    tdf = df[df["ticker"] == ticker].sort_values("date")
    if tdf.empty:
        return None
    current_year = tdf["date"].max().year
    year_start = tdf[tdf["date"].dt.year == current_year]
    if year_start.empty:
        return None
    first_price = year_start["close"].iloc[0]
    last_price = year_start["close"].iloc[-1]
    if first_price == 0:
        return None
    return (last_price / first_price - 1) * 100


def ticker_summary_table(yf_prices: pd.DataFrame, tickers: list[str],
                         labels: dict = None) -> pd.DataFrame:
    """Build a summary table with latest price and YTD return for given tickers."""
    rows = []
    for ticker in tickers:
        tdf = yf_prices[yf_prices["ticker"] == ticker].sort_values("date")
        if tdf.empty:
            continue
        company = tdf["company"].iloc[0]
        sector = tdf["sector"].iloc[0] if "sector" in tdf.columns else ""
        latest_price = tdf["close"].iloc[-1]
        ytd = get_ytd_return(yf_prices, ticker)
        label = labels.get(ticker, sector) if labels else sector
        rows.append({
            "Ticker": ticker,
            "Company": company,
            "Sub-sector": label,
            "Latest Price": f"{latest_price:.2f}",
            "YTD %": f"{ytd:+.1f}%" if ytd is not None else "N/A",
        })
    return pd.DataFrame(rows)
