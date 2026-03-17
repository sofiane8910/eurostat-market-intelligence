# Dashboard 2 — Quick Start (Windows)

## 1. Open terminal and navigate to the project

```cmd
cd C:\path\to\eurostat-market-intelligence
```

## 2. Create and activate virtual environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

```cmd
pip install streamlit pandas plotly yfinance
```

## 4. Extract data

```cmd
python extract_db2.py
python extract_yfinance_db2.py
```

This creates CSV files in `data2/`:
- `sts.csv` — Eurostat STS production indices
- `yfinance_financials.csv` — Annual/quarterly financials (Revenue, EBITDA, Net Income)
- `yfinance_prices.csv` — 90-day stock prices
- `yfinance_news.csv` — Latest news articles

## 5. Start the dashboard

```cmd
streamlit run dashboard2/app.py
```

Opens at http://localhost:8501

## All-in-one

```cmd
.venv\Scripts\activate && python extract_db2.py && python extract_yfinance_db2.py && streamlit run dashboard2/app.py
```
