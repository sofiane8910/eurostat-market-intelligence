"""
Data loading and normalization for the Eurostat Labels Market Dashboard.
Loads all CSV files from output/comext/ and output/sts/, normalizes formats,
and computes data freshness metrics.
"""

import os
import re
from datetime import date

import pandas as pd
import streamlit as st

from constants import (
    GEO_NORMALIZE, AGGREGATE_CODES, CN_DESCRIPTIONS,
    STS_DATASET_DESCRIPTIONS, NACE_DESCRIPTIONS,
    SUPPLY_CN_CODES, DEMAND_CN_CODES, SUPPLY_NACE, DEMAND_NACE,
    TIER1_DATASETS,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def _normalize_geo(code: str) -> str:
    """Normalize country codes (EL -> GR)."""
    return GEO_NORMALIZE.get(code, code)


def load_comext_file(path: str) -> pd.DataFrame:
    """
    Load a Comext CSV file and return normalized long-format DataFrame.
    Columns: country, partner, flow, indicator, date, value
    """
    df = pd.read_csv(path)
    if df.empty:
        return pd.DataFrame(columns=["country", "partner", "flow", "indicator", "date", "value"])

    df = df.rename(columns={
        "reporter": "country",
        "partner": "partner",
        "flow": "flow",
        "indicators": "indicator",
        "TIME_PERIOD": "date",
        "OBS_VALUE": "value",
    })
    df = df[["country", "partner", "flow", "indicator", "date", "value"]].copy()
    df["country"] = df["country"].map(_normalize_geo)
    df["partner"] = df["partner"].map(_normalize_geo)
    df["flow"] = df["flow"].astype(str)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def load_sts_file(path: str) -> pd.DataFrame:
    """
    Load an STS CSV file (wide format) and return long-format DataFrame.
    Columns: country, date, value
    Takes only the first row per geo (preferred SCA/I21 combo).
    """
    df = pd.read_csv(path)
    if df.empty:
        return pd.DataFrame(columns=["country", "date", "value"])

    # Find the geo column (contains TIME_PERIOD)
    geo_col = None
    for c in df.columns:
        if "geo" in c.lower():
            geo_col = c
            break
    if geo_col is None:
        return pd.DataFrame(columns=["country", "date", "value"])

    # Identify meta columns (everything before date columns)
    date_cols = [c for c in df.columns if re.match(r"^\d{4}-\d{2}$", c)]
    if not date_cols:
        return pd.DataFrame(columns=["country", "date", "value"])

    # Keep first row per geo (already sorted by preference in extraction)
    df = df.drop_duplicates(subset=[geo_col], keep="first")

    # Melt wide -> long
    melted = df.melt(
        id_vars=[geo_col],
        value_vars=date_cols,
        var_name="date",
        value_name="value",
    )
    melted = melted.rename(columns={geo_col: "country"})
    melted["country"] = melted["country"].map(_normalize_geo)
    melted["date"] = pd.to_datetime(melted["date"], format="%Y-%m")
    melted["value"] = pd.to_numeric(melted["value"], errors="coerce")
    melted = melted.dropna(subset=["value"])

    return melted[["country", "date", "value"]]


def _parse_sts_filename(filename: str):
    """
    Parse STS filename like 'sts_inpr_m_C10.csv' -> ('sts_inpr_m', 'C10')
    or 'ei_bssi_m_r2_C10.csv' -> ('ei_bssi_m_r2', 'C10')
    """
    name = filename.replace(".csv", "")
    # Match NACE codes: C*, G*, H* (including bare H)
    m = re.match(r"(.+)_((?:C|G|H)\w*)$", name)
    if m:
        return m.group(1), m.group(2)
    return None, None


def compute_freshness(df: pd.DataFrame, dataset_key: str = "") -> dict:
    """Compute data freshness for a series."""
    if df.empty or "date" not in df.columns:
        return {"latest_date": None, "tier": 2, "lag_days": None}

    latest = df["date"].max()
    today = pd.Timestamp(date.today())
    lag_days = (today - latest).days

    # Determine tier from dataset key
    ds = dataset_key.split("_")[:-1]  # remove NACE suffix
    ds_name = "_".join(ds) if ds else dataset_key
    tier = 1 if ds_name in TIER1_DATASETS else 2

    return {
        "latest_date": latest,
        "tier": tier,
        "lag_days": lag_days,
    }


@st.cache_data(ttl=3600)
def load_all_data():
    """
    Load all CSVs from output/comext/ and output/sts/.
    Returns dict with:
        comext: {cn_code: DataFrame}
        sts: {"dataset_nace": DataFrame}
        freshness: {key: {latest_date, tier, lag_days}}
        meta: {
            comext_codes: [(cn_code, description, side), ...],
            sts_series: [(dataset, nace, ds_desc, nace_desc, side), ...],
        }
    """
    comext_dir = os.path.join(DATA_DIR, "comext")
    sts_dir = os.path.join(DATA_DIR, "sts")

    comext_data = {}
    sts_data = {}
    freshness = {}
    comext_codes = []
    sts_series = []

    # Load Comext files
    if os.path.isdir(comext_dir):
        for fname in sorted(os.listdir(comext_dir)):
            if not fname.endswith(".csv"):
                continue
            cn_code = fname.replace("CN_", "").replace(".csv", "")
            path = os.path.join(comext_dir, fname)
            df = load_comext_file(path)
            if not df.empty:
                comext_data[cn_code] = df
                side = "supply" if cn_code in SUPPLY_CN_CODES else "demand"
                desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
                comext_codes.append((cn_code, desc, side))
                freshness[f"comext_{cn_code}"] = compute_freshness(df, "comext")

    # Load STS files
    if os.path.isdir(sts_dir):
        for fname in sorted(os.listdir(sts_dir)):
            if not fname.endswith(".csv"):
                continue
            dataset, nace = _parse_sts_filename(fname)
            if dataset is None:
                continue
            path = os.path.join(sts_dir, fname)
            df = load_sts_file(path)
            if not df.empty:
                key = f"{dataset}_{nace}"
                sts_data[key] = df
                ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
                nace_desc = NACE_DESCRIPTIONS.get(nace, nace)
                side = "supply" if nace in SUPPLY_NACE else "demand"
                sts_series.append((dataset, nace, ds_desc, nace_desc, side))
                freshness[key] = compute_freshness(df, dataset)

    return {
        "comext": comext_data,
        "sts": sts_data,
        "freshness": freshness,
        "meta": {
            "comext_codes": comext_codes,
            "sts_series": sts_series,
        },
    }


def get_eu27_aggregate(df: pd.DataFrame, partner: str = "WORLD",
                        flow: str = "1", indicator: str = "VALUE_IN_EUROS") -> pd.DataFrame:
    """
    For a Comext DataFrame, compute EU27 total by summing all reporters
    for the given partner/flow/indicator. Returns DataFrame with date + value.
    """
    mask = (
        (df["partner"] == partner) &
        (df["flow"] == flow) &
        (df["indicator"] == indicator) &
        (~df["country"].isin(AGGREGATE_CODES))
    )
    agg = df[mask].groupby("date")["value"].sum().reset_index()
    return agg.sort_values("date")


def get_country_series(df: pd.DataFrame, country: str,
                        partner: str = "WORLD", flow: str = "1",
                        indicator: str = "VALUE_IN_EUROS") -> pd.DataFrame:
    """
    For a Comext DataFrame, get time series for a specific country/partner/flow/indicator.
    """
    mask = (
        (df["country"] == country) &
        (df["partner"] == partner) &
        (df["flow"] == flow) &
        (df["indicator"] == indicator)
    )
    result = df[mask][["date", "value"]].sort_values("date")
    return result
