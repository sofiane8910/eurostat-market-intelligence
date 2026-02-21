"""
yfinance → DB-ready CSVs for listed companies financial data.

Extracts quarterly income statement line items, daily stock prices, and latest news
for end-market companies and Avery Dennison competitors.

Output (in output2/):
  - yfinance_financials.csv  — ALL quarterly income statement line items (long format), 2025-2026
  - yfinance_prices.csv      — daily stock prices from 2023-01-01 onwards
  - yfinance_news.csv        — latest news articles per ticker
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Ticker registry — 60 tickers (42 end-market + 18 competitors)
# ---------------------------------------------------------------------------
TICKERS = {
    # === GROUP A: End-market companies (42) ===
    # Beverages (9)
    "ABI.BR":       {"company": "Anheuser-Busch InBev",       "group": "end_market", "sector": "beverages",  "country": "Belgium"},
    "HEIA.AS":      {"company": "Heineken",                    "group": "end_market", "sector": "beverages",  "country": "Netherlands"},
    "CARL-B.CO":    {"company": "Carlsberg",                   "group": "end_market", "sector": "beverages",  "country": "Denmark"},
    "DGE.L":        {"company": "Diageo",                      "group": "end_market", "sector": "beverages",  "country": "UK"},
    "RI.PA":        {"company": "Pernod Ricard",               "group": "end_market", "sector": "beverages",  "country": "France"},
    "RCO.PA":       {"company": "Rémy Cointreau",              "group": "end_market", "sector": "beverages",  "country": "France"},
    "CPR.MI":       {"company": "Campari",                     "group": "end_market", "sector": "beverages",  "country": "Italy"},
    "CCH.L":        {"company": "Coca-Cola HBC",               "group": "end_market", "sector": "beverages",  "country": "UK"},
    "CCEP.AS":      {"company": "Coca-Cola Europacific Partners", "group": "end_market", "sector": "beverages", "country": "Netherlands"},
    # Food (5)
    "NESN.SW":      {"company": "Nestlé",                      "group": "end_market", "sector": "food",       "country": "Switzerland"},
    "BN.PA":        {"company": "Danone",                      "group": "end_market", "sector": "food",       "country": "France"},
    "KYGA.L":       {"company": "Kerry Group",                 "group": "end_market", "sector": "food",       "country": "Ireland"},
    "ABF.L":        {"company": "Associated British Foods",    "group": "end_market", "sector": "food",       "country": "UK"},
    "ORK.OL":       {"company": "Orkla",                       "group": "end_market", "sector": "food",       "country": "Norway"},
    # HPC (6)
    "ULVR.L":       {"company": "Unilever",                    "group": "end_market", "sector": "hpc",        "country": "UK"},
    "OR.PA":        {"company": "L'Oréal",                     "group": "end_market", "sector": "hpc",        "country": "France"},
    "HEN3.DE":      {"company": "Henkel",                      "group": "end_market", "sector": "hpc",        "country": "Germany"},
    "BEI.DE":       {"company": "Beiersdorf",                  "group": "end_market", "sector": "hpc",        "country": "Germany"},
    "RKT.L":        {"company": "Reckitt Benckiser",           "group": "end_market", "sector": "hpc",        "country": "UK"},
    "ESSITY-B.ST":  {"company": "Essity",                      "group": "end_market", "sector": "hpc",        "country": "Sweden"},
    # Pharma (8)
    "NOVN.SW":      {"company": "Novartis",                    "group": "end_market", "sector": "pharma",     "country": "Switzerland"},
    "ROG.SW":       {"company": "Roche",                       "group": "end_market", "sector": "pharma",     "country": "Switzerland"},
    "SAN.PA":       {"company": "Sanofi",                      "group": "end_market", "sector": "pharma",     "country": "France"},
    "AZN.L":        {"company": "AstraZeneca",                 "group": "end_market", "sector": "pharma",     "country": "UK"},
    "NOVO-B.CO":    {"company": "Novo Nordisk",                "group": "end_market", "sector": "pharma",     "country": "Denmark"},
    "BAYN.DE":      {"company": "Bayer",                       "group": "end_market", "sector": "pharma",     "country": "Germany"},
    "GSK.L":        {"company": "GSK",                         "group": "end_market", "sector": "pharma",     "country": "UK"},
    "UCB.BR":       {"company": "UCB",                         "group": "end_market", "sector": "pharma",     "country": "Belgium"},
    # Tobacco (2)
    "BATS.L":       {"company": "BAT",                         "group": "end_market", "sector": "tobacco",    "country": "UK"},
    "IMB.L":        {"company": "Imperial Brands",             "group": "end_market", "sector": "tobacco",    "country": "UK"},
    # Retail (6)
    "TSCO.L":       {"company": "Tesco",                       "group": "end_market", "sector": "retail",     "country": "UK"},
    "SBRY.L":       {"company": "Sainsbury's",                 "group": "end_market", "sector": "retail",     "country": "UK"},
    "MKS.L":        {"company": "M&S",                         "group": "end_market", "sector": "retail",     "country": "UK"},
    "CA.PA":        {"company": "Carrefour",                   "group": "end_market", "sector": "retail",     "country": "France"},
    "AD.AS":        {"company": "Ahold Delhaize",              "group": "end_market", "sector": "retail",     "country": "Netherlands"},
    "JMT.LS":       {"company": "Jerónimo Martins",            "group": "end_market", "sector": "retail",     "country": "Portugal"},
    # Logistics (4)
    "DHL.DE":       {"company": "DHL Group",                   "group": "end_market", "sector": "logistics",  "country": "Germany"},
    "DSV.CO":       {"company": "DSV",                         "group": "end_market", "sector": "logistics",  "country": "Denmark"},
    "MAERSK-B.CO":  {"company": "Maersk",                      "group": "end_market", "sector": "logistics",  "country": "Denmark"},
    "KNIN.SW":      {"company": "Kuehne + Nagel",              "group": "end_market", "sector": "logistics",  "country": "Switzerland"},
    # Extra end-market entries to reach 42: count above = 40
    # (The plan lists 42 but enumerates 40; keeping what's listed)

    # === GROUP B: Avery Dennison competitors (18) ===
    # EMEA-listed (5)
    "UPM.HE":       {"company": "UPM-Kymmene / Raflatac",     "group": "competitor", "sector": "label_materials",  "country": "Finland"},
    "STERV.HE":     {"company": "Stora Enso",                  "group": "competitor", "sector": "label_materials",  "country": "Finland"},
    "HUH1V.HE":     {"company": "Huhtamaki",                   "group": "competitor", "sector": "label_materials",  "country": "Finland"},
    "MNDI.L":       {"company": "Mondi",                       "group": "competitor", "sector": "label_materials",  "country": "UK"},
    "BOL.PA":       {"company": "Bolloré",                     "group": "competitor", "sector": "label_materials",  "country": "France"},
    # Extra-EU with European operations (5)
    "AVY":          {"company": "Avery Dennison",              "group": "competitor", "sector": "label_materials",  "country": "US"},
    "CCL-B.TO":     {"company": "CCL Industries",              "group": "competitor", "sector": "label_materials",  "country": "Canada"},
    "AMCR":         {"company": "Amcor",                       "group": "competitor", "sector": "packaging",        "country": "US"},
    "POLYPLEX.NS":  {"company": "Polyplex Corporation",        "group": "competitor", "sector": "films",            "country": "India"},
    "COSMOFILMS.NS":{"company": "Cosmo Films",                 "group": "competitor", "sector": "films",            "country": "India"},
    # China (8)
    "002191.SZ":    {"company": "Jinjia Group",                "group": "competitor", "sector": "label_materials",  "country": "China"},
    "300106.SZ":    {"company": "Guanhao High-Tech",           "group": "competitor", "sector": "release_films",    "country": "China"},
    "603681.SS":    {"company": "Shanghai Yongguan",           "group": "competitor", "sector": "label_materials",  "country": "China"},
    "000859.SZ":    {"company": "Anhui Guofeng",               "group": "competitor", "sector": "films",            "country": "China"},
    "002263.SZ":    {"company": "Zhejiang Dadongnan",          "group": "competitor", "sector": "films",            "country": "China"},
    "300305.SZ":    {"company": "Jiangsu Yuxing Film",         "group": "competitor", "sector": "films",            "country": "China"},
    "600210.SS":    {"company": "Shanghai Zijiang",            "group": "competitor", "sector": "label_materials",  "country": "China"},
    "600135.SS":    {"company": "Lekai Film",                  "group": "competitor", "sector": "release_films",    "country": "China"},
}

OUT_DIR = Path(__file__).parent / "output2"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def quarter_label(dt) -> str:
    """Convert a datetime-like to 'YYYY-QN' string."""
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"


def fetch_financials(ticker: str, meta: dict) -> list[dict]:
    """Fetch ALL quarterly income statement line items for a ticker (long format)."""
    stock = yf.Ticker(ticker)
    income_stmt = stock.quarterly_financials  # rows=metrics, cols=quarter dates

    if income_stmt is None or income_stmt.empty:
        return []

    # Get currency from info
    try:
        currency = stock.info.get("currency", "")
    except Exception:
        currency = ""

    rows = []
    for metric_name, metric_row in income_stmt.iterrows():
        for quarter_date, value in metric_row.items():
            if pd.isna(value):
                continue
            # Filter to 2025-2026 only
            if hasattr(quarter_date, "year") and quarter_date.year not in (2025, 2026):
                continue
            rows.append({
                "ticker": ticker,
                "company": meta["company"],
                "group": meta["group"],
                "sector": meta["sector"],
                "country": meta["country"],
                "quarter": quarter_label(quarter_date),
                "quarter_end": quarter_date.strftime("%Y-%m-%d"),
                "metric": str(metric_name),
                "value": float(value),
                "currency": currency,
            })
    return rows


def fetch_prices(ticker: str, meta: dict) -> list[dict]:
    """Fetch daily stock prices from 2023-01-01 onwards."""
    stock = yf.Ticker(ticker)
    hist = stock.history(start="2023-01-01")

    if hist is None or hist.empty:
        return []

    hist = hist.reset_index()
    rows = []
    for _, row in hist.iterrows():
        dt = row["Date"]
        if hasattr(dt, "strftime"):
            date_str = dt.strftime("%Y-%m-%d")
        else:
            date_str = str(dt)[:10]
        rows.append({
            "ticker": ticker,
            "company": meta["company"],
            "group": meta["group"],
            "sector": meta["sector"],
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
        # yfinance news format can vary; handle both old and new formats
        title = article.get("title", article.get("content", {}).get("title", ""))
        publisher = article.get("publisher", article.get("content", {}).get("provider", {}).get("displayName", ""))
        link = article.get("link", article.get("content", {}).get("canonicalUrl", {}).get("url", ""))
        pub_time = article.get("providerPublishTime", None)
        article_type = article.get("type", "")

        if pub_time and isinstance(pub_time, (int, float)):
            published_at = datetime.fromtimestamp(pub_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        elif pub_time and isinstance(pub_time, str):
            published_at = pub_time
        else:
            published_at = ""

        rows.append({
            "ticker": ticker,
            "company": meta["company"],
            "group": meta["group"],
            "sector": meta["sector"],
            "title": title,
            "publisher": publisher,
            "link": link,
            "published_at": published_at,
            "type": article_type,
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
            # Financials
            fin_rows = fetch_financials(ticker, meta)
            all_financials.extend(fin_rows)
            fin_count = len(fin_rows)
            if fin_count > 0:
                ok_fin += 1

            # Prices
            price_rows = fetch_prices(ticker, meta)
            all_prices.extend(price_rows)
            price_count = len(price_rows)
            if price_count > 0:
                ok_price += 1

            # News
            news_rows = fetch_news(ticker, meta)
            all_news.extend(news_rows)
            news_count = len(news_rows)
            if news_count > 0:
                ok_news += 1

            print(f"OK (fin={fin_count}, prices={price_count}, news={news_count})")

        except Exception as e:
            print(f"FAILED: {e}")
            failed.append(ticker)

        # Small delay to be polite to Yahoo Finance
        time.sleep(0.5)

    # --- Write CSVs ---
    print("\nWriting CSVs...")

    if all_financials:
        df_fin = pd.DataFrame(all_financials)
        df_fin.to_csv(OUT_DIR / "yfinance_financials.csv", index=False)
        print(f"  yfinance_financials.csv: {len(df_fin)} rows, {df_fin['ticker'].nunique()} tickers, {df_fin['metric'].nunique()} metrics")
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
