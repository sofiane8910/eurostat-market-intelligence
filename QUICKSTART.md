# Quickstart

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Data Extraction

```bash
source .venv/bin/activate
python extract_db.py
python extract_yfinance_db.py
```

## Run Dashboard

```bash
source .venv/bin/activate
streamlit run dashboard/app.py
```

Opens at http://localhost:8501
