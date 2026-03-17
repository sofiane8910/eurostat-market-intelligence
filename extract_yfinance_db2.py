"""
yfinance extraction for Dashboard 2 — 28 end-market tickers.

Lighter subset of extract_yfinance_db.py, organized by application category.
Extracts quarterly financials (3 key metrics), daily prices, and news.

Output (in data2/):
  - yfinance_financials.csv  — Total Revenue, EBITDA, Net Income (long format)
  - yfinance_prices.csv      — daily stock prices from 90 days ago
  - yfinance_news.csv        — latest news articles per ticker
"""

import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Ticker registry — 28 tickers across 7 categories
# ---------------------------------------------------------------------------
TICKERS = {
    # Food (4)
    "NESN.SW":     {"company": "Nestlé",              "app_category": "Food",                    "country": "Switzerland"},
    "BN.PA":       {"company": "Danone",              "app_category": "Food",                    "country": "France"},
    "ABF.L":       {"company": "Assoc British Foods", "app_category": "Food",                    "country": "UK"},
    "ORK.OL":      {"company": "Orkla",               "app_category": "Food",                    "country": "Norway"},
    # Beverage (4)
    "ABI.BR":      {"company": "AB InBev",            "app_category": "Beverage",                "country": "Belgium"},
    "HEIA.AS":     {"company": "Heineken",            "app_category": "Beverage",                "country": "Netherlands"},
    "DGE.L":       {"company": "Diageo",              "app_category": "Beverage",                "country": "UK"},
    "CCH.L":       {"company": "Coca-Cola HBC",       "app_category": "Beverage",                "country": "UK"},
    # Tobacco (2)
    "BATS.L":      {"company": "BAT",                 "app_category": "Tobacco",                 "country": "UK"},
    "IMB.L":       {"company": "Imperial Brands",     "app_category": "Tobacco",                 "country": "UK"},
    # Home & Personal Care (4)
    "ULVR.L":      {"company": "Unilever",            "app_category": "Home & Personal Care",    "country": "UK"},
    "OR.PA":        {"company": "L'Oréal",            "app_category": "Home & Personal Care",    "country": "France"},
    "HEN3.DE":     {"company": "Henkel",              "app_category": "Home & Personal Care",    "country": "Germany"},
    "BEI.DE":      {"company": "Beiersdorf",          "app_category": "Home & Personal Care",    "country": "Germany"},
    # Pharmaceuticals (4)
    "NOVN.SW":     {"company": "Novartis",            "app_category": "Pharmaceuticals",         "country": "Switzerland"},
    "ROG.SW":      {"company": "Roche",               "app_category": "Pharmaceuticals",         "country": "Switzerland"},
    "SAN.PA":      {"company": "Sanofi",              "app_category": "Pharmaceuticals",         "country": "France"},
    "NOVO-B.CO":   {"company": "Novo Nordisk",        "app_category": "Pharmaceuticals",         "country": "Denmark"},
    # Retail (4)
    "TSCO.L":      {"company": "Tesco",               "app_category": "Retail",                  "country": "UK"},
    "CA.PA":        {"company": "Carrefour",          "app_category": "Retail",                  "country": "France"},
    "AD.AS":       {"company": "Ahold Delhaize",      "app_category": "Retail",                  "country": "Netherlands"},
    "JMT.LS":      {"company": "Jerónimo Martins",   "app_category": "Retail",                  "country": "Portugal"},
    # Transport & Logistics (4)
    "DHL.DE":      {"company": "DHL Group",           "app_category": "Transport & Logistics",   "country": "Germany"},
    "DSV.CO":      {"company": "DSV",                 "app_category": "Transport & Logistics",   "country": "Denmark"},
    "MAERSK-B.CO": {"company": "Maersk",             "app_category": "Transport & Logistics",   "country": "Denmark"},
    "KNIN.SW":     {"company": "Kuehne+Nagel",       "app_category": "Transport & Logistics",   "country": "Switzerland"},
}

# Only extract these 3 financial metrics
TARGET_METRICS = {"Total Revenue", "EBITDA", "Net Income"}

OUT_DIR = Path(__file__).parent / "data2"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def quarter_label(dt) -> str:
    """Convert a datetime-like to 'YYYY-QN' string."""
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"


def fetch_financials(ticker: str, meta: dict) -> list[dict]:
    """Fetch quarterly financials filtered to 3 key metrics.

    Falls back to annual income statement when quarterly is unavailable
    (common for European-listed companies).
    """
    stock = yf.Ticker(ticker)
    income_stmt = stock.quarterly_financials
    period = "quarterly"

    if income_stmt is None or income_stmt.empty:
        # Fallback: annual financials (most EU companies report annually)
        income_stmt = stock.financials
        period = "annual"

    if income_stmt is None or income_stmt.empty:
        return []

    try:
        currency = stock.info.get("currency", "")
    except Exception:
        currency = ""

    rows = []
    for metric_name, metric_row in income_stmt.iterrows():
        if str(metric_name) not in TARGET_METRICS:
            continue
        for period_date, value in metric_row.items():
            if pd.isna(value):
                continue
            if period == "quarterly":
                label = quarter_label(period_date)
            else:
                label = f"FY {period_date.year}"
            rows.append({
                "ticker": ticker,
                "company": meta["company"],
                "app_category": meta["app_category"],
                "country": meta["country"],
                "quarter": label,
                "quarter_end": period_date.strftime("%Y-%m-%d"),
                "metric": str(metric_name),
                "value": float(value),
                "currency": currency,
                "period_type": period,
            })
    return rows


def fetch_prices(ticker: str, meta: dict) -> list[dict]:
    """Fetch daily stock prices for the last 90 days."""
    stock = yf.Ticker(ticker)
    start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    hist = stock.history(start=start)

    if hist is None or hist.empty:
        return []

    hist = hist.reset_index()
    rows = []
    for _, row in hist.iterrows():
        dt = row["Date"]
        date_str = dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)[:10]
        rows.append({
            "ticker": ticker,
            "company": meta["company"],
            "app_category": meta["app_category"],
            "country": meta["country"],
            "date": date_str,
            "open": round(float(row["Open"]), 4) if pd.notna(row["Open"]) else None,
            "high": round(float(row["High"]), 4) if pd.notna(row["High"]) else None,
            "low": round(float(row["Low"]), 4) if pd.notna(row["Low"]) else None,
            "close": round(float(row["Close"]), 4) if pd.notna(row["Close"]) else None,
            "volume": int(row["Volume"]) if pd.notna(row["Volume"]) else None,
        })
    return rows


def fetch_news(ticker: str, meta: dict) -> list[dict]:
    """Fetch latest news articles for a ticker."""
    stock = yf.Ticker(ticker)
    try:
        news = stock.news
    except Exception:
        return []

    if not news:
        return []

    rows = []
    for article in news:
        title = article.get("title", article.get("content", {}).get("title", ""))
        publisher = article.get("publisher", article.get("content", {}).get("provider", {}).get("displayName", ""))
        link = article.get("link", article.get("content", {}).get("canonicalUrl", {}).get("url", ""))
        pub_time = article.get("providerPublishTime", None)

        if pub_time and isinstance(pub_time, (int, float)):
            published_at = datetime.fromtimestamp(pub_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        elif pub_time and isinstance(pub_time, str):
            published_at = pub_time
        else:
            published_at = ""

        rows.append({
            "ticker": ticker,
            "company": meta["company"],
            "app_category": meta["app_category"],
            "country": meta["country"],
            "title": title,
            "publisher": publisher,
            "link": link,
            "published_at": published_at,
        })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    all_financials = []
    all_prices = []
    all_news = []

    total = len(TICKERS)
    ok_fin = 0
    ok_price = 0
    ok_news = 0
    failed = []

    for i, (ticker, meta) in enumerate(TICKERS.items(), 1):
        print(f"[{i}/{total}] {ticker} ({meta['company']})...", end=" ", flush=True)

        try:
            fin_rows = fetch_financials(ticker, meta)
            all_financials.extend(fin_rows)
            if fin_rows:
                ok_fin += 1

            price_rows = fetch_prices(ticker, meta)
            all_prices.extend(price_rows)
            if price_rows:
                ok_price += 1

            news_rows = fetch_news(ticker, meta)
            all_news.extend(news_rows)
            if news_rows:
                ok_news += 1

            print(f"OK (fin={len(fin_rows)}, prices={len(price_rows)}, news={len(news_rows)})")

        except Exception as e:
            print(f"FAILED: {e}")
            failed.append(ticker)

        time.sleep(0.5)

    # --- Write CSVs ---
    print("\nWriting CSVs...")

    if all_financials:
        df_fin = pd.DataFrame(all_financials)
        df_fin.to_csv(OUT_DIR / "yfinance_financials.csv", index=False)
        print(f"  yfinance_financials.csv: {len(df_fin)} rows, {df_fin['ticker'].nunique()} tickers")
    else:
        print("  WARNING: No financial data fetched!")

    if all_prices:
        df_prices = pd.DataFrame(all_prices)
        df_prices.to_csv(OUT_DIR / "yfinance_prices.csv", index=False)
        print(f"  yfinance_prices.csv: {len(df_prices)} rows, {df_prices['ticker'].nunique()} tickers")
    else:
        print("  WARNING: No price data fetched!")

    if all_news:
        df_news = pd.DataFrame(all_news)
        df_news.to_csv(OUT_DIR / "yfinance_news.csv", index=False)
        print(f"  yfinance_news.csv: {len(df_news)} rows, {df_news['ticker'].nunique()} tickers")
    else:
        print("  WARNING: No news data fetched!")

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Total tickers: {total}")
    print(f"  Financials OK: {ok_fin}")
    print(f"  Prices OK:     {ok_price}")
    print(f"  News OK:       {ok_news}")
    if failed:
        print(f"  Failed ({len(failed)}): {', '.join(failed)}")
    print(f"\nOutput: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
