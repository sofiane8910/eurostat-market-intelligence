"""
Data loading and normalization for the Eurostat Labels Market Dashboard.
Loads flat CSVs from output2/ (comext.csv, sts.csv), normalizes formats,
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

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output2")


def _normalize_geo(code: str) -> str:
    """Normalize country codes (EL -> GR)."""
    return GEO_NORMALIZE.get(code, code)


def _load_comext_all() -> dict:
    """Load output2/comext.csv and return {cn_code: DataFrame}."""
    path = os.path.join(DATA_DIR, "comext.csv")
    if not os.path.isfile(path):
        return {}
    df = pd.read_csv(path)
    if df.empty:
        return {}
    df = df.rename(columns={"reporter": "country"})
    df["country"] = df["country"].map(_normalize_geo)
    df["partner"] = df["partner"].map(_normalize_geo)
    df["flow"] = df["flow"].astype(str)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    result = {}
    for cn_code, grp in df.groupby("cn_code"):
        result[str(cn_code)] = grp[["country", "partner", "flow", "indicator", "date", "value"]].copy()
    return result


def _load_sts_all() -> dict:
    """Load output2/sts.csv and return {dataset_nace: DataFrame}."""
    path = os.path.join(DATA_DIR, "sts.csv")
    if not os.path.isfile(path):
        return {}
    df = pd.read_csv(path)
    if df.empty:
        return {}
    # Prefer SCA adjustment, then keep first per (dataset, nace, country, date)
    adj_order = {"SCA": 0}
    df["_adj_rank"] = df["s_adj"].map(adj_order).fillna(1)
    df = df.sort_values("_adj_rank")
    df = df.drop_duplicates(subset=["dataset", "nace", "country", "date"], keep="first")
    df = df.drop(columns=["_adj_rank"])
    df["country"] = df["country"].map(_normalize_geo)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    result = {}
    for (dataset, nace), grp in df.groupby(["dataset", "nace"]):
        result[f"{dataset}_{nace}"] = grp[["country", "date", "value"]].copy()
    return result


def compute_freshness(df: pd.DataFrame, dataset_name: str = "") -> dict:
    """Compute data freshness for a series."""
    if df.empty or "date" not in df.columns:
        return {"latest_date": None, "tier": 2, "lag_days": None}

    latest = df["date"].max()
    today = pd.Timestamp(date.today())
    lag_days = (today - latest).days

    # Determine tier — dataset_name is already the clean dataset ID
    # e.g. "sts_inpr_m", "ei_bssi_m_r2", "comext"
    tier = 1 if dataset_name in TIER1_DATASETS else 2

    return {
        "latest_date": latest,
        "tier": tier,
        "lag_days": lag_days,
    }


@st.cache_data(ttl=3600)
def load_all_data():
    """
    Load flat CSVs from output2/.
    Returns dict with:
        comext: {cn_code: DataFrame}
        sts: {"dataset_nace": DataFrame}
        freshness: {key: {latest_date, tier, lag_days}}
        meta: {
            comext_codes: [(cn_code, description, side), ...],
            sts_series: [(dataset, nace, ds_desc, nace_desc, side), ...],
        }
    """
    freshness = {}
    comext_codes = []
    sts_series = []

    # Load Comext
    comext_data = _load_comext_all()
    for cn_code, df in sorted(comext_data.items()):
        side = "supply" if cn_code in SUPPLY_CN_CODES else "demand"
        desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
        comext_codes.append((cn_code, desc, side))
        freshness[f"comext_{cn_code}"] = compute_freshness(df, "comext")

    # Load STS
    sts_data = _load_sts_all()
    for key, df in sorted(sts_data.items()):
        # key is "dataset_nace" e.g. "sts_inpr_m_C17"
        # Split on last underscore that precedes the NACE code
        m = re.match(r"(.+)_((?:C|G|H)\w*)$", key)
        if m:
            dataset, nace = m.group(1), m.group(2)
        else:
            continue
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
