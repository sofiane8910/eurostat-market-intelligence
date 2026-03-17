"""
Data loading and normalization for Dashboard 2 — Application Categories.
Loads STS CSV from data2/sts.csv, normalizes formats,
and computes data freshness metrics. No Comext trade data.
"""

import os
import re
from datetime import date

import pandas as pd
import streamlit as st

from constants2 import (
    GEO_NORMALIZE, AGGREGATE_CODES,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS, NACE_DISPLAY_NAMES,
    TIER1_DATASETS,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data2")


def _normalize_geo(code: str) -> str:
    """Normalize country codes (EL -> GR)."""
    return GEO_NORMALIZE.get(code, code)


def _load_sts_all() -> dict:
    """Load data2/sts.csv and return {dataset_nace: DataFrame}."""
    path = os.path.join(DATA_DIR, "sts.csv")
    if not os.path.isfile(path):
        gz_path = path + ".gz"
        if os.path.isfile(gz_path):
            path = gz_path
        else:
            return {}
    df = pd.read_csv(path)
    if df.empty:
        return {}
    # Prefer SCA adjustment
    adj_order = {"SCA": 0}
    df["_adj_rank"] = df["s_adj"].map(adj_order).fillna(1)
    df = df.sort_values("_adj_rank")
    df = df.drop_duplicates(subset=["dataset", "nace", "country", "date"], keep="first")
    df = df.drop(columns=["_adj_rank"])
    df["country"] = df["country"].map(_normalize_geo)
    # Drop aggregate geo codes
    df = df[~df["country"].isin(AGGREGATE_CODES)]
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    result = {}
    for (dataset, nace), grp in df.groupby(["dataset", "nace"]):
        key = f"{dataset}_{nace}"
        result[key] = grp[["country", "date", "value", "app_category"]].copy()
    return result


def compute_freshness(df: pd.DataFrame, dataset_name: str = "") -> dict:
    """Compute data freshness for a series."""
    if df.empty or "date" not in df.columns:
        return {"latest_date": None, "tier": 2, "lag_days": None}

    latest = df["date"].max()
    today = pd.Timestamp(date.today())
    lag_days = (today - latest).days

    tier = 1 if dataset_name in TIER1_DATASETS else 2

    return {
        "latest_date": latest,
        "tier": tier,
        "lag_days": lag_days,
    }


def _load_yfinance_financials() -> pd.DataFrame:
    """Load data2/yfinance_financials.csv."""
    path = os.path.join(DATA_DIR, "yfinance_financials.csv")
    if not os.path.isfile(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def _load_yfinance_prices() -> pd.DataFrame:
    """Load data2/yfinance_prices.csv."""
    path = os.path.join(DATA_DIR, "yfinance_prices.csv")
    if not os.path.isfile(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


def _load_yfinance_news() -> pd.DataFrame:
    """Load data2/yfinance_news.csv."""
    path = os.path.join(DATA_DIR, "yfinance_news.csv")
    if not os.path.isfile(path):
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(ttl=3600)
def load_all_data():
    """
    Load STS CSV and yfinance data from data2/.
    Returns dict with:
        sts: {"dataset_nace": DataFrame}
        freshness: {key: {latest_date, tier, lag_days}}
        meta: {
            sts_series: [(dataset, nace, ds_desc, nace_display, app_category, side), ...],
        }
        yf_financials: DataFrame
        yf_prices: DataFrame
        yf_news: DataFrame
    """
    freshness = {}
    sts_series = []

    # Load STS
    sts_data = _load_sts_all()
    for key, df in sorted(sts_data.items()):
        m = re.match(r"(.+)_((?:C|G|H)\w*)$", key)
        if m:
            dataset, nace = m.group(1), m.group(2)
        else:
            continue
        ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
        nace_display = NACE_DISPLAY_NAMES.get(nace, nace)
        cat = df["app_category"].iloc[0] if "app_category" in df.columns and not df.empty else ""
        side = "production" if dataset.startswith("sts_in") or dataset == "ei_bssi_m_r2" else "demand"
        sts_series.append((dataset, nace, ds_desc, nace_display, cat, side))
        freshness[key] = compute_freshness(df, dataset)

    # Load yfinance data
    yf_fin = _load_yfinance_financials()
    yf_prices = _load_yfinance_prices()
    yf_news = _load_yfinance_news()

    return {
        "sts": sts_data,
        "freshness": freshness,
        "meta": {
            "sts_series": sts_series,
        },
        "yf_financials": yf_fin,
        "yf_prices": yf_prices,
        "yf_news": yf_news,
    }
