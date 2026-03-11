"""
Collect availability metadata for all 30 demand-side series.
Scans comext.csv.gz and sts.csv.gz to build per-series availability info.

Outputs:
  - deep dive/availability_detail.csv
  - deep dive/availability_summary.csv
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "dashboard"))
from constants import (
    DEMAND_CN_CODES, DEMAND_NACE, STS_DATASET_DESCRIPTIONS,
    AGGREGATE_CODES, GEO_NORMALIZE, EU27_CODES,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "output2")
OUT_DIR = os.path.dirname(__file__)


def _normalize_geo(code):
    return GEO_NORMALIZE.get(code, code)


def _load_comext():
    for ext in ("comext.csv.gz", "comext.csv"):
        path = os.path.join(DATA_DIR, ext)
        if os.path.isfile(path):
            return pd.read_csv(path)
    return pd.DataFrame()


def _load_sts():
    for ext in ("sts.csv.gz", "sts.csv"):
        path = os.path.join(DATA_DIR, ext)
        if os.path.isfile(path):
            return pd.read_csv(path)
    return pd.DataFrame()


def collect_comext_availability(comext_df):
    """Build availability rows for each demand CN code from comext data."""
    detail_rows = []
    if comext_df.empty:
        return detail_rows

    comext_df = comext_df.copy()
    comext_df["reporter"] = comext_df["reporter"].map(_normalize_geo)
    comext_df["date"] = pd.to_datetime(comext_df["date"], format="%Y-%m")

    for cn_code, desc in DEMAND_CN_CODES.items():
        sub = comext_df[comext_df["cn_code"].astype(str) == str(cn_code)]
        if sub.empty:
            detail_rows.append({
                "series_name": desc,
                "category": _get_category(cn_code),
                "code_type": "CN",
                "code": cn_code,
                "data_source": "comext",
                "indicator_type": "trade",
                "countries": "",
                "country_count": 0,
                "granularity": "monthly",
                "date_min": None,
                "date_max": None,
            })
            continue

        # Exclude aggregate reporters
        countries = sorted(
            set(sub["reporter"].unique()) - AGGREGATE_CODES
        )
        eu27_countries = [c for c in countries if c in EU27_CODES]
        flows = sorted(sub["flow"].astype(str).unique())
        indicators = sorted(sub["indicator"].unique())

        detail_rows.append({
            "series_name": desc,
            "category": _get_category(cn_code),
            "code_type": "CN",
            "code": cn_code,
            "data_source": "comext",
            "indicator_type": "trade",
            "countries": ";".join(eu27_countries),
            "country_count": len(eu27_countries),
            "granularity": "monthly",
            "date_min": sub["date"].min().strftime("%Y-%m"),
            "date_max": sub["date"].max().strftime("%Y-%m"),
        })

    return detail_rows


def collect_sts_availability(sts_df):
    """Build availability rows for each demand NACE code across all STS datasets."""
    detail_rows = []
    if sts_df.empty:
        return detail_rows

    sts_df = sts_df.copy()
    sts_df["country"] = sts_df["country"].map(_normalize_geo)
    sts_df["date"] = pd.to_datetime(sts_df["date"], format="%Y-%m")

    for nace_code, nace_desc in DEMAND_NACE.items():
        nace_sub = sts_df[sts_df["nace"] == nace_code]
        if nace_sub.empty:
            detail_rows.append({
                "series_name": nace_desc,
                "category": _get_category(nace_code),
                "code_type": "NACE",
                "code": nace_code,
                "data_source": "none",
                "indicator_type": "none",
                "countries": "",
                "country_count": 0,
                "granularity": "monthly",
                "date_min": None,
                "date_max": None,
            })
            continue

        for dataset, ds_grp in nace_sub.groupby("dataset"):
            ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
            countries = sorted(
                set(ds_grp["country"].unique()) - AGGREGATE_CODES
            )
            eu27_countries = [c for c in countries if c in EU27_CODES]
            indicator_type = _classify_indicator(dataset)

            detail_rows.append({
                "series_name": nace_desc,
                "category": _get_category(nace_code),
                "code_type": "NACE",
                "code": nace_code,
                "data_source": dataset,
                "indicator_type": indicator_type,
                "countries": ";".join(eu27_countries),
                "country_count": len(eu27_countries),
                "granularity": "monthly",
                "date_min": ds_grp["date"].min().strftime("%Y-%m"),
                "date_max": ds_grp["date"].max().strftime("%Y-%m"),
            })

    return detail_rows


def _classify_indicator(dataset):
    """Classify STS dataset into indicator type."""
    ds = dataset.lower()
    if "inpr" in ds:
        return "production"
    elif "intv" in ds:
        return "turnover"
    elif "inpp" in ds or "inpi" in ds:
        return "prices"
    elif "bssi" in ds or "bsrt" in ds or "bsse" in ds:
        return "confidence"
    elif "trtu" in ds:
        return "turnover"
    elif "sepr" in ds:
        return "production"
    elif "inlb" in ds:
        return "labour"
    elif "ordi" in ds:
        return "orders"
    return "other"


def _get_category(code):
    """Map a CN or NACE code to its demand-side category."""
    # From demand_side_series.csv categories
    cn_categories = {
        "2009": "Production", "2201": "Production", "2202": "Production",
        "2203": "Production", "2204": "Production", "2208": "Production",
        "3304": "Production", "3305": "Production", "3307": "Production",
        "3402": "Production", "3004": "Production",
        "1602": "Production", "1604": "Production", "2005": "Production",
        "2106": "Production",
    }
    nace_categories = {
        "C10": "Manufacturing", "C11": "Manufacturing", "C12": "Manufacturing",
        "C204": "Manufacturing", "C21": "Manufacturing",
        "G47": "Retail", "G47_FOOD": "Retail", "G47_NF_HLTH": "Retail",
        "G47_NFOOD_X_G473": "Retail", "G4711": "Retail", "G47_NFOOD": "Retail",
        "H": "Logistics", "H49": "Logistics", "H52": "Logistics",
        "H53": "Logistics",
    }
    return cn_categories.get(code, nace_categories.get(code, "Other"))


def build_summary(detail_df):
    """Aggregate detail rows into one row per series."""
    rows = []
    for (series_name, code), grp in detail_df.groupby(["series_name", "code"]):
        first = grp.iloc[0]
        all_countries = set()
        for clist in grp["countries"]:
            if pd.notna(clist) and clist:
                all_countries.update(clist.split(";"))

        datasets = grp[grp["data_source"] != "none"]["data_source"].unique()
        indicator_types = set(grp["indicator_type"].unique()) - {"none"}

        date_mins = grp["date_min"].dropna()
        date_maxs = grp["date_max"].dropna()

        rows.append({
            "series_name": series_name,
            "category": first["category"],
            "code_type": first["code_type"],
            "code": code,
            "total_countries": len(all_countries),
            "country_list": ";".join(sorted(all_countries)),
            "granularity": "monthly",
            "date_min": date_mins.min() if len(date_mins) else None,
            "date_max": date_maxs.max() if len(date_maxs) else None,
            "latest_data": date_maxs.max() if len(date_maxs) else None,
            "n_datasets": len(datasets),
            "dataset_list": ";".join(sorted(datasets)),
            "has_production": "production" in indicator_types,
            "has_turnover": "turnover" in indicator_types,
            "has_prices": "prices" in indicator_types,
            "has_trade": "trade" in indicator_types,
            "has_confidence": "confidence" in indicator_types,
        })

    return pd.DataFrame(rows)


def main():
    print("Loading comext data...")
    comext_df = _load_comext()
    print(f"  Comext: {len(comext_df)} rows")

    print("Loading STS data...")
    sts_df = _load_sts()
    print(f"  STS: {len(sts_df)} rows")

    print("Collecting comext availability...")
    comext_rows = collect_comext_availability(comext_df)
    print(f"  {len(comext_rows)} detail rows from comext")

    print("Collecting STS availability...")
    sts_rows = collect_sts_availability(sts_df)
    print(f"  {len(sts_rows)} detail rows from STS")

    detail_df = pd.DataFrame(comext_rows + sts_rows)
    detail_path = os.path.join(OUT_DIR, "availability_detail.csv")
    detail_df.to_csv(detail_path, index=False)
    print(f"Wrote {detail_path} ({len(detail_df)} rows)")

    summary_df = build_summary(detail_df)
    summary_path = os.path.join(OUT_DIR, "availability_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Wrote {summary_path} ({len(summary_df)} rows)")

    # Quick summary
    print("\n--- Summary ---")
    print(f"Total series: {len(summary_df)}")
    print(f"With production data: {summary_df['has_production'].sum()}")
    print(f"With trade data: {summary_df['has_trade'].sum()}")
    print(f"With price data: {summary_df['has_prices'].sum()}")
    print(f"Average country coverage: {summary_df['total_countries'].mean():.1f}")
    print(f"Full EU27 (27 countries): {(summary_df['total_countries'] >= 27).sum()}")


if __name__ == "__main__":
    main()
