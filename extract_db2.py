#!/usr/bin/env python3
"""
Dashboard 2 — Eurostat extraction pipeline
============================================
Produces one flat CSV in data2/:
  - sts.csv — STS indices: 10 production datasets x 9 NACE + retail/logistics/confidence

Usage:
    python extract_db2.py
"""

import os
import re
import sys
import time
import traceback

import pandas as pd

try:
    import eurostat
except ImportError:
    eurostat = None


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

START_PERIOD = 2023
END_PERIOD = 2026

EU27_ISO = sorted([
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES",
    "FI", "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK",
])

# Aggregate codes to drop from STS results
AGGREGATE_GEO = {"EU27_2020", "EA19", "EA20", "EA21"}

# ---------------------------------------------------------------------------
# Application category mapping — 10 categories (NACE only, no trade codes)
# ---------------------------------------------------------------------------

APP_CATEGORIES = {
    "Food": {"production_nace": ["C10"], "retail_nace": ["G47_FOOD", "G4711"], "logistics_nace": []},
    "Beverage": {"production_nace": ["C11"], "retail_nace": ["G47_FOOD"], "logistics_nace": []},
    "Tobacco": {"production_nace": ["C12"], "retail_nace": [], "logistics_nace": []},
    "Home & Personal Care": {"production_nace": ["C204"], "retail_nace": ["G47_NF_HLTH"], "logistics_nace": []},
    "Pharmaceuticals": {"production_nace": ["C21"], "retail_nace": ["G47_NF_HLTH"], "logistics_nace": []},
    "Retail": {"production_nace": [], "retail_nace": ["G47", "G47_FOOD", "G47_NF_HLTH", "G47_NFOOD_X_G473", "G4711"], "logistics_nace": []},
    "Transport & Logistics": {"production_nace": [], "retail_nace": [], "logistics_nace": ["H", "H49", "H52", "H53"]},
    "Industrial Chemicals": {"production_nace": ["C20"], "retail_nace": [], "logistics_nace": []},
    "Office Products": {"production_nace": ["C17"], "retail_nace": [], "logistics_nace": []},
    "Consumer Durables": {"production_nace": ["C27"], "retail_nace": [], "logistics_nace": []},
    "Automotive": {"production_nace": ["C29"], "retail_nace": [], "logistics_nace": []},
}

# Production NACE codes
ALL_PRODUCTION_NACE = []
NACE_TO_CATEGORY = {}
for cat, info in APP_CATEGORIES.items():
    for nace in info["production_nace"]:
        if nace not in NACE_TO_CATEGORY:
            ALL_PRODUCTION_NACE.append(nace)
            NACE_TO_CATEGORY[nace] = cat

# Demand STS series (retail + logistics + confidence)
DEMAND_STS_SERIES = {
    "sts_trtu_m": ["G47", "G47_FOOD", "G47_NF_HLTH", "G47_NFOOD_X_G473", "G4711"],
    "sts_sepr_m": ["H", "H49", "H52", "H53"],
    "ei_bsrt_m_r2": ["G47_FOOD", "G47_NFOOD"],
    "ei_bsse_m_r2": ["H"],
}

# Production STS datasets
PRODUCTION_DATASETS = [
    "sts_inpr_m",
    "sts_intv_m",
    "sts_intvd_m",
    "sts_intvnd_m",
    "sts_inpp_m",
    "sts_inppd_m",
    "sts_inppnd_m",
    "sts_inpi_m",
    "sts_inlb_m",
    "ei_bssi_m_r2",
]

# ---------------------------------------------------------------------------
# STS descriptions
# ---------------------------------------------------------------------------

STS_DATASET_DESCRIPTIONS = {
    "sts_inpr_m": "Production in industry - monthly",
    "sts_intv_m": "Turnover in industry - total",
    "sts_intvd_m": "Turnover in industry - domestic market",
    "sts_intvnd_m": "Turnover in industry - non-domestic market",
    "sts_inpp_m": "Producer prices in industry - total",
    "sts_inppd_m": "Producer prices - domestic market",
    "sts_inppnd_m": "Producer prices - non-domestic market",
    "sts_inpi_m": "Import prices in industry",
    "sts_inlb_m": "Labour input in industry",
    "ei_bssi_m_r2": "Industry confidence indicator",
    "sts_trtu_m": "Retail trade turnover",
    "sts_sepr_m": "Services production index",
    "ei_bsrt_m_r2": "Retail trade confidence indicator",
    "ei_bsse_m_r2": "Services confidence indicator",
}

NACE_DESCRIPTIONS = {
    "C10": "Manufacture of food products",
    "C11": "Manufacture of beverages",
    "C12": "Manufacture of tobacco products",
    "C17": "Paper and paper products",
    "C20": "Chemicals and chemical products",
    "C204": "Soap, detergents, cleaning, cosmetics, toiletries",
    "C21": "Basic pharmaceutical products and preparations",
    "C27": "Manufacture of electrical equipment",
    "C29": "Manufacture of motor vehicles",
    "G47": "Retail trade (excl. motor vehicles)",
    "G47_FOOD": "Retail sale of food, beverages and tobacco",
    "G47_NF_HLTH": "Dispensing chemist, medical goods, cosmetics, toiletries",
    "G47_NFOOD_X_G473": "Non-food retail (excl. automotive fuel)",
    "G4711": "Non-specialised stores (food predominating)",
    "G47_NFOOD": "Retail non-food products",
    "H": "Transportation and storage",
    "H49": "Land transport and pipelines",
    "H52": "Warehousing and transport support",
    "H53": "Postal and courier activities",
}

# Build category lookup for demand NACE too
for cat, info in APP_CATEGORIES.items():
    for nace in info["retail_nace"] + info["logistics_nace"]:
        if nace not in NACE_TO_CATEGORY:
            NACE_TO_CATEGORY[nace] = cat


# ---------------------------------------------------------------------------
# Known STS exclusions (dataset x NACE combos that return no data)
# ---------------------------------------------------------------------------

_EXCLUDED_NACE_FOR_TURNOVER_LABOUR = ["C204"]
EXCLUDED_STS_COMBOS = {
    (ds, nace)
    for ds in ["sts_intv_m", "sts_intvd_m", "sts_intvnd_m", "sts_inlb_m"]
    for nace in _EXCLUDED_NACE_FOR_TURNOVER_LABOUR
}


# ---------------------------------------------------------------------------
# Extraction functions
# ---------------------------------------------------------------------------

def _clean_sts_df(df):
    """
    Clean STS DataFrame: keep one series per geo, drop flag columns,
    rename value columns to bare dates.
    """
    geo_col = None
    for c in ["geo\\TIME_PERIOD", "geo\\time", "geo"]:
        if c in df.columns:
            geo_col = c
            break
    if geo_col is None:
        return df

    flag_cols = [c for c in df.columns if c.endswith("_flag")]
    df = df.drop(columns=flag_cols, errors="ignore")

    rename = {}
    for c in df.columns:
        if c.endswith("_value"):
            rename[c] = c.replace("_value", "")
    df = df.rename(columns=rename)

    rows_per_geo = df.groupby(geo_col).size()
    if rows_per_geo.max() <= 1:
        return df

    if "s_adj" in df.columns and df["s_adj"].nunique() > 1:
        for pref in ["SCA", "SA", "NSA"]:
            subset = df[df["s_adj"] == pref]
            if not subset.empty:
                df = subset
                break

    if "unit" in df.columns and df["unit"].nunique() > 1:
        for pref in ["I21", "I15", "I10", "I05"]:
            subset = df[df["unit"] == pref]
            if not subset.empty:
                df = subset
                break

    rows_per_geo = df.groupby(geo_col).size()
    if rows_per_geo.max() > 1:
        for col in ["indic_bt", "indic"]:
            if col in df.columns and df[col].nunique() > 1:
                first_val = df[col].iloc[0]
                df = df[df[col] == first_val]
                break

    return df.reset_index(drop=True)


def extract_sts_monthly(dataset, nace):
    """
    Extract STS monthly index data for a dataset x NACE combination.
    Returns cleaned DataFrame with one row per geo and bare date columns.
    """
    if eurostat is None:
        print("  -> eurostat package not available")
        return pd.DataFrame()

    print(f"  Fetching {dataset} x {nace}...")

    # Attempt 1: seasonally adjusted, index 2021=100
    try:
        filter_pars = {
            "startPeriod": START_PERIOD,
            "endPeriod": END_PERIOD,
            "nace_r2": [nace],
            "s_adj": ["SCA"],
            "unit": ["I21"],
        }
        df = eurostat.get_data_df(dataset, filter_pars=filter_pars, flags=True)
        if df is not None and not df.empty:
            df = _clean_sts_df(df)
            print(f"  -> OK: {len(df)} rows")
            return df
    except Exception as e:
        print(f"  -> SCA/I21 failed: {e}")

    # Attempt 2: index 2015=100
    try:
        filter_pars = {
            "startPeriod": START_PERIOD,
            "endPeriod": END_PERIOD,
            "nace_r2": [nace],
            "s_adj": ["SCA"],
            "unit": ["I15"],
        }
        df = eurostat.get_data_df(dataset, filter_pars=filter_pars, flags=True)
        if df is not None and not df.empty:
            df = _clean_sts_df(df)
            print(f"  -> OK (I15): {len(df)} rows")
            return df
    except Exception as e:
        print(f"  -> SCA/I15 failed: {e}")

    # Attempt 3: broader filter
    try:
        filter_pars = {
            "startPeriod": START_PERIOD,
            "endPeriod": END_PERIOD,
            "nace_r2": [nace],
        }
        df = eurostat.get_data_df(dataset, filter_pars=filter_pars, flags=True)
        if df is not None and not df.empty:
            df = _clean_sts_df(df)
            print(f"  -> OK (broad): {len(df)} rows")
            return df
    except Exception as e:
        print(f"  -> Broad filter failed: {e}")

    print(f"  -> No data for {dataset} x {nace}")
    return pd.DataFrame()


def _melt_sts_df(df, dataset, nace, app_category, side):
    """
    Melt a wide STS DataFrame into long format matching the output schema.
    """
    geo_col = None
    for c in ["geo\\TIME_PERIOD", "geo\\time", "geo"]:
        if c in df.columns:
            geo_col = c
            break
    if geo_col is None:
        return pd.DataFrame()

    s_adj_val = df["s_adj"].iloc[0] if "s_adj" in df.columns and not df["s_adj"].empty else ""
    unit_val = df["unit"].iloc[0] if "unit" in df.columns and not df["unit"].empty else ""

    date_cols = [c for c in df.columns if re.match(r"\d{4}-\d{2}$", c)]
    if not date_cols:
        return pd.DataFrame()

    melted = df.melt(
        id_vars=[geo_col],
        value_vars=date_cols,
        var_name="date",
        value_name="value",
    )
    melted = melted.rename(columns={geo_col: "country"})

    melted["value"] = pd.to_numeric(melted["value"], errors="coerce")
    melted = melted.dropna(subset=["value"])

    if melted.empty:
        return melted

    # Drop aggregate geo codes
    melted = melted[~melted["country"].isin(AGGREGATE_GEO)]

    melted["dataset"] = dataset
    melted["dataset_description"] = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
    melted["nace"] = nace
    melted["nace_description"] = NACE_DESCRIPTIONS.get(nace, nace)
    melted["app_category"] = app_category
    melted["side"] = side
    melted["s_adj"] = s_adj_val
    melted["unit"] = unit_val

    return melted[["dataset", "dataset_description", "nace", "nace_description",
                    "app_category", "side", "s_adj", "unit", "country", "date", "value"]]


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_extraction():
    """Run the Dashboard 2 extraction pipeline."""
    if eurostat is None:
        print("ERROR: 'eurostat' package not installed. Run: pip install eurostat")
        sys.exit(1)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data2")
    os.makedirs(output_dir, exist_ok=True)

    production_pairs = [
        (ds, nace) for ds in PRODUCTION_DATASETS for nace in ALL_PRODUCTION_NACE
        if (ds, nace) not in EXCLUDED_STS_COMBOS
    ]
    total_production = len(production_pairs)

    demand_pairs = [
        (ds, nace) for ds, nace_list in DEMAND_STS_SERIES.items()
        for nace in nace_list
    ]
    total_demand = len(demand_pairs)

    total = total_production + total_demand
    series_idx = 0
    success_count = 0

    print("=" * 70)
    print("DASHBOARD 2 — EUROSTAT EXTRACTION (STS only)")
    print(f"Production STS: {total_production} | Demand STS: {total_demand}")
    print(f"Total: {total} series | Period: {START_PERIOD}-01 to {END_PERIOD}-12")
    print(f"Output: {output_dir}/")
    print("=" * 70)

    # -------------------------------------------------------------------
    # Phase 1: Production STS
    # -------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("PHASE 1: PRODUCTION STS (10 datasets x 9 NACE)")
    print(f"{'=' * 70}")

    sts_frames = []

    for idx, (dataset, nace) in enumerate(production_pairs, 1):
        series_idx += 1
        app_category = NACE_TO_CATEGORY.get(nace, "")

        print(f"\n[{series_idx}/{total}] Production STS {idx}/{total_production}: "
              f"{dataset} x {nace} ({app_category})")
        print("-" * 50)

        t0 = time.time()
        try:
            df = extract_sts_monthly(dataset, nace)
        except Exception as e:
            print(f"  UNEXPECTED ERROR: {e}")
            traceback.print_exc()
            df = pd.DataFrame()

        elapsed = time.time() - t0

        if df is not None and not df.empty:
            melted = _melt_sts_df(df, dataset, nace, app_category, side="production")
            if not melted.empty:
                sts_frames.append(melted)
                success_count += 1
                print(f"  Collected {len(melted)} rows (elapsed {elapsed:.1f}s)")
            else:
                print(f"  Melt produced 0 rows (elapsed {elapsed:.1f}s)")
        else:
            print(f"  No data (elapsed {elapsed:.1f}s)")

        if series_idx < total:
            time.sleep(1)

    # -------------------------------------------------------------------
    # Phase 2: Demand-side STS (retail, logistics, confidence)
    # -------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("PHASE 2: DEMAND-SIDE STS (retail, logistics, confidence)")
    print(f"{'=' * 70}")

    for idx, (dataset, nace) in enumerate(demand_pairs, 1):
        series_idx += 1
        app_category = NACE_TO_CATEGORY.get(nace, "")

        print(f"\n[{series_idx}/{total}] Demand STS {idx}/{total_demand}: "
              f"{dataset} x {nace} ({app_category})")
        print("-" * 50)

        t0 = time.time()
        try:
            df = extract_sts_monthly(dataset, nace)
        except Exception as e:
            print(f"  UNEXPECTED ERROR: {e}")
            traceback.print_exc()
            df = pd.DataFrame()

        elapsed = time.time() - t0

        if df is not None and not df.empty:
            melted = _melt_sts_df(df, dataset, nace, app_category, side="demand")
            if not melted.empty:
                sts_frames.append(melted)
                success_count += 1
                print(f"  Collected {len(melted)} rows (elapsed {elapsed:.1f}s)")
            else:
                print(f"  Melt produced 0 rows (elapsed {elapsed:.1f}s)")
        else:
            print(f"  No data (elapsed {elapsed:.1f}s)")

        if series_idx < total:
            time.sleep(1)

    # Write sts.csv
    if sts_frames:
        sts_all = pd.concat(sts_frames, ignore_index=True)
        sts_path = os.path.join(output_dir, "sts.csv")
        sts_all.to_csv(sts_path, index=False)
        n_combos = sts_all.groupby(["dataset", "nace"]).ngroups
        print(f"\nSaved {sts_path}: {len(sts_all):,} rows, "
              f"{n_combos} dataset x NACE combinations")
    else:
        print("\nNo STS data collected.")

    # -------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"\n  STS:    {len(sts_frames)}/{total} series extracted")
    print(f"  Total:  {success_count}/{total} series extracted successfully")
    print(f"\nOutput in: {output_dir}/")


if __name__ == "__main__":
    run_extraction()
