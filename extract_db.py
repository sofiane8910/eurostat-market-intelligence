#!/usr/bin/env python3
"""
Database-ready Eurostat extraction pipeline
============================================
Produces two flat CSVs in output2/:
  - comext.csv  — all trade data stacked (one row per observation)
  - sts.csv     — all STS index data stacked (one row per observation)

Excludes 68 series that return no data from Eurostat.

Usage:
    python extract_db.py
"""

import os
import re
import sys
import time
import traceback
from io import StringIO

import pandas as pd
import requests

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

COMEXT_FLOW_IMPORT = "1"
COMEXT_FLOW_EXPORT = "2"
COMEXT_INDICATORS = ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"]

COMEXT_PARTNERS = "+".join(["WORLD"] + EU27_ISO + ["CN"])

# ---------------------------------------------------------------------------
# CN codes — 61 total (before exclusions)
# ---------------------------------------------------------------------------

COMEXT_CN_CODES = [
    # B1: SA Plastics
    "39191010", "39191080", "39199010", "39199020", "39199080",
    # B2: SA Paper
    "48114100", "48114900",
    # B3: Labels
    "48211010", "48211090", "48219010", "48219090",
    # B4.1: PE Films
    "39201023", "39201024", "39201025", "39201028",
    "39201040", "39201081", "39201089",
    # B4.2: PP Films
    "39202021", "39202029", "39202080",
    # B4.3: PVC Films
    "39204310", "39204390", "39204910", "39204990",
    # B4.4: PET Films
    "39206210", "39206219", "39206290",
    # B4.5: Other Films
    "39206100", "39206900", "39209928", "39209959",
    # B5: Adhesives
    "35061000", "35069110", "35069190", "35069900",
    # B6: Silicones
    "39100000",
    # B7: Glassine
    "48064010", "48064090",
    # B8: Printing Inks
    "32151100", "32151900", "32159000",
    # B9: RFID
    "85235210", "85235910", "85235990",
    # B10: Stamping Foils
    "32121000",
    # Demand-side: Beverages
    "2009", "2201", "2202", "2203", "2204", "2208",
    # Demand-side: HPC / Cleaning
    "3304", "3305", "3307", "3402",
    # Demand-side: Pharma
    "3004",
    # Demand-side: Food (processed)
    "1602", "1604", "2005", "2106",
]

# ---------------------------------------------------------------------------
# STS datasets and NACE codes
# ---------------------------------------------------------------------------

STS_DATASETS = [
    "sts_inpr_m",
    "sts_intv_m",
    "sts_intvd_m",
    "sts_intvnd_m",
    "sts_inpp_m",
    "sts_inppd_m",
    "sts_inppnd_m",
    "sts_inpi_m",
    "sts_ordi_m",
    "sts_inlb_m",
    "ei_bssi_m_r2",
]

NACE_CODES = [
    "C17", "C171", "C1712", "C172", "C1729",
    "C18", "C20", "C203", "C2052",
    "C22", "C222", "C2221", "C2229", "C2829",
    # Demand-side end-market sectors
    "C10", "C11", "C12", "C204", "C21",
]

DEMAND_STS_SERIES = {
    "sts_trtu_m": ["G47", "G47_FOOD", "G47_NF_HLTH", "G47_NFOOD_X_G473", "G4711"],
    "sts_sepr_m": ["H", "H49", "H52", "H53"],
    "ei_bsrt_m_r2": ["G47_FOOD", "G47_NFOOD"],
    "ei_bsse_m_r2": ["H"],
}

# ---------------------------------------------------------------------------
# Description mappings
# ---------------------------------------------------------------------------

CN_DESCRIPTIONS = {
    "39191010": "SA plastic, rolls <= 20cm, width <= 20cm",
    "39191080": "SA plastic, rolls <= 20cm, other",
    "39199010": "SA plastic (excl. rolls <= 20cm), condensation polymerisation",
    "39199020": "SA plastic (excl. rolls <= 20cm), addition polymerisation",
    "39199080": "SA plastic (excl. rolls <= 20cm), other",
    "48114100": "Self-adhesive paper and paperboard",
    "48114900": "Gummed/adhesive paper & paperboard (excl. self-adhesive)",
    "48211010": "Self-adhesive printed labels, paper/paperboard",
    "48211090": "Other printed labels, paper/paperboard (excl. SA)",
    "48219010": "Self-adhesive labels, paper/paperboard (unprinted)",
    "48219090": "Other labels, paper/paperboard (unprinted, excl. SA)",
    "39201023": "PE film, SG < 0.94, thickness <= 0.025mm",
    "39201024": "PE film, SG < 0.94, thickness 0.025-0.05mm",
    "39201025": "PE film, SG < 0.94, thickness > 0.05mm",
    "39201028": "Other PE film, SG < 0.94",
    "39201040": "PE film, SG >= 0.94, thickness < 0.021mm",
    "39201081": "PE film, SG >= 0.94, thickness 0.021-0.160mm",
    "39201089": "Other PE film, SG >= 0.94",
    "39202021": "BOPP film, thickness <= 0.10mm",
    "39202029": "Other PP film (cast/OPP), thickness <= 0.10mm",
    "39202080": "PP film, thickness > 0.10mm",
    "39204310": "Flexible PVC film (>= 6% plasticiser), not supported",
    "39204390": "Other flexible PVC film",
    "39204910": "Rigid PVC film, thickness > 1mm",
    "39204990": "Other rigid PVC film",
    "39206210": "PET film, thickness <= 0.025mm",
    "39206219": "PET film, thickness 0.025-0.35mm",
    "39206290": "PET film, thickness > 0.35mm",
    "39206100": "Polycarbonate film",
    "39206900": "Other polyester film (PEN, PBT, etc.)",
    "39209928": "Polyimide film",
    "39209959": "Other plastic film, n.e.c.",
    "35061000": "Adhesives, retail sale, <= 1kg",
    "35069110": "Water-based adhesives from synthetic polymers",
    "35069190": "Other adhesives (synthetic polymers/rubber)",
    "35069900": "Other prepared glues/adhesives, n.e.c.",
    "39100000": "Silicones in primary forms",
    "48064010": "Glassine papers",
    "48064090": "Other glazed transparent/translucent papers",
    "32151100": "Black printing ink",
    "32151900": "Other printing ink",
    "32159000": "Other ink (excl. printing)",
    "85235210": "Smart cards (electronic IC)",
    "85235910": "RFID tags, inlays, proximity cards",
    "85235990": "Other semiconductor media",
    "32121000": "Stamping foils",
    "2009": "Fruit juices (incl. grape must)",
    "2201": "Mineral and aerated waters",
    "2202": "Non-alcoholic beverages (excl. water/juices)",
    "2203": "Beer made from malt",
    "2204": "Wine of fresh grapes",
    "2208": "Spirits, liqueurs and other spirituous beverages",
    "3304": "Beauty, make-up and skin care preparations",
    "3305": "Hair preparations",
    "3307": "Shaving, deodorant, bath preparations",
    "3402": "Washing and cleaning preparations",
    "3004": "Medicaments in measured doses",
    "1602": "Prepared or preserved meat",
    "1604": "Prepared or preserved fish",
    "2005": "Prepared or preserved vegetables",
    "2106": "Food preparations n.e.c.",
}

STS_DATASET_DESCRIPTIONS = {
    "sts_inpr_m": "Production in industry - monthly",
    "sts_intv_m": "Turnover in industry - total",
    "sts_intvd_m": "Turnover in industry - domestic market",
    "sts_intvnd_m": "Turnover in industry - non-domestic market",
    "sts_inpp_m": "Producer prices in industry - total",
    "sts_inppd_m": "Producer prices - domestic market",
    "sts_inppnd_m": "Producer prices - non-domestic market",
    "sts_inpi_m": "Import prices in industry",
    "sts_ordi_m": "New orders in industry",
    "sts_inlb_m": "Labour input in industry",
    "ei_bssi_m_r2": "Industry confidence indicator",
    "sts_trtu_m": "Retail trade turnover",
    "sts_sepr_m": "Services production index",
    "ei_bsrt_m_r2": "Retail trade confidence indicator",
    "ei_bsse_m_r2": "Services confidence indicator",
}

NACE_DESCRIPTIONS = {
    "C17": "Paper and paper products",
    "C171": "Pulp, paper and paperboard",
    "C1712": "Paper and paperboard",
    "C172": "Articles of paper and paperboard",
    "C1729": "Other articles of paper and paperboard",
    "C18": "Printing and reproduction",
    "C20": "Chemicals and chemical products",
    "C203": "Paints, varnishes, printing ink, mastics",
    "C2052": "Manufacture of glues",
    "C22": "Rubber and plastic products",
    "C222": "Plastics products",
    "C2221": "Plastic plates, sheets, tubes, profiles",
    "C2229": "Other plastic products",
    "C2829": "Other general-purpose machinery, n.e.c.",
    "C10": "Manufacture of food products",
    "C11": "Manufacture of beverages",
    "C12": "Manufacture of tobacco products",
    "C204": "Soap, detergents, cleaning, cosmetics, toiletries",
    "C21": "Basic pharmaceutical products and preparations",
    "G47": "Retail trade (excl. motor vehicles)",
    "G47_FOOD": "Retail sale of food, beverages and tobacco",
    "G47_NF_HLTH": "Dispensing chemist, medical goods, cosmetics, toiletries",
    "G47_NFOOD_X_G473": "Non-food retail (excl. automotive fuel)",
    "G4711": "Non-specialised stores (food predominating)",
    "H": "Transportation and storage",
    "H49": "Land transport and pipelines",
    "H52": "Warehousing and transport support",
    "H53": "Postal and courier activities",
    "G47_NFOOD": "Retail non-food products",
}


# ---------------------------------------------------------------------------
# Exclusion lists (68 series that return 0 rows from Eurostat)
# ---------------------------------------------------------------------------

EXCLUDED_CN = {"39191010", "39199010", "39206210", "32159000", "85235210"}

EXCLUDED_STS_DATASETS = {"sts_ordi_m"}

_EXCLUDED_NACE_FOR_TURNOVER_LABOUR = [
    "C171", "C1712", "C172", "C1729", "C203", "C2052",
    "C222", "C2221", "C2229", "C2829", "C204",
]
EXCLUDED_STS_COMBOS = {
    (ds, nace)
    for ds in ["sts_intv_m", "sts_intvd_m", "sts_intvnd_m", "sts_inlb_m"]
    for nace in _EXCLUDED_NACE_FOR_TURNOVER_LABOUR
}


# ---------------------------------------------------------------------------
# Side classification
# ---------------------------------------------------------------------------

DEMAND_CN_CODES = {
    "2009", "2201", "2202", "2203", "2204", "2208",
    "3304", "3305", "3307", "3402",
    "3004",
    "1602", "1604", "2005", "2106",
}

SUPPLY_NACE = {
    "C17", "C171", "C1712", "C172", "C1729",
    "C18", "C20", "C203", "C2052",
    "C22", "C222", "C2221", "C2229", "C2829",
}


# ---------------------------------------------------------------------------
# Extraction functions
# ---------------------------------------------------------------------------

def extract_comext_monthly(cn_code):
    """
    Extract monthly Comext trade data for a single CN code from DS-045409.
    Falls back to HS6 (first 6 digits) if CN8 returns 400.
    """
    base_url = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1"
    reporters = "+".join(EU27_ISO)
    indicators = "+".join(COMEXT_INDICATORS)
    flows = f"{COMEXT_FLOW_IMPORT}+{COMEXT_FLOW_EXPORT}"

    url = (
        f"{base_url}/data/DS-045409/"
        f"M.{reporters}.{COMEXT_PARTNERS}.{cn_code}.{flows}.{indicators}"
        f"?startPeriod={START_PERIOD}&endPeriod={END_PERIOD}"
        f"&format=SDMX-CSV"
    )

    print(f"  Fetching CN {cn_code} (monthly, bilateral)...")
    try:
        resp = requests.get(url, timeout=300)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> OK: {len(df)} rows")
            return df

        if resp.status_code == 400 and len(cn_code) == 8:
            hs6 = cn_code[:6]
            print(f"  -> CN8 returned 400, trying HS6 ({hs6})...")
            url_hs6 = (
                f"{base_url}/data/DS-045409/"
                f"M.{reporters}.{COMEXT_PARTNERS}.{hs6}.{flows}.{indicators}"
                f"?startPeriod={START_PERIOD}&endPeriod={END_PERIOD}"
                f"&format=SDMX-CSV"
            )
            resp2 = requests.get(url_hs6, timeout=300)
            if resp2.status_code == 200 and len(resp2.content) > 100:
                df = pd.read_csv(StringIO(resp2.text))
                print(f"  -> OK (HS6 fallback): {len(df)} rows")
                return df
            print(f"  -> HS6 also failed: status {resp2.status_code}")
        else:
            print(f"  -> Status {resp.status_code}, length {len(resp.content)}")
    except Exception as e:
        print(f"  -> Failed: {e}")

    return pd.DataFrame()


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
    Extract STS monthly index data for a dataset x NACE combination
    using eurostat.get_data_df(). Returns cleaned DataFrame with one
    row per geo and bare date columns.
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

    # Attempt 3: broader filter — clean aggressively
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


def _melt_sts_df(df, dataset, nace, side):
    """
    Melt a wide STS DataFrame (one row per geo, date columns) into
    long format matching the output schema.
    """
    # Find geo column
    geo_col = None
    for c in ["geo\\TIME_PERIOD", "geo\\time", "geo"]:
        if c in df.columns:
            geo_col = c
            break
    if geo_col is None:
        return pd.DataFrame()

    # Extract s_adj and unit from the DataFrame
    s_adj_val = df["s_adj"].iloc[0] if "s_adj" in df.columns and not df["s_adj"].empty else ""
    unit_val = df["unit"].iloc[0] if "unit" in df.columns and not df["unit"].empty else ""

    # Identify date columns (YYYY-MM pattern)
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

    # Convert to numeric and drop missing
    melted["value"] = pd.to_numeric(melted["value"], errors="coerce")
    melted = melted.dropna(subset=["value"])

    if melted.empty:
        return melted

    # Add identification columns
    melted["dataset"] = dataset
    melted["dataset_description"] = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
    melted["nace"] = nace
    melted["nace_description"] = NACE_DESCRIPTIONS.get(nace, nace)
    melted["side"] = side
    melted["s_adj"] = s_adj_val
    melted["unit"] = unit_val

    # Reorder columns to match schema
    return melted[["dataset", "dataset_description", "nace", "nace_description",
                    "side", "s_adj", "unit", "country", "date", "value"]]


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_extraction():
    """Run the database-ready extraction pipeline."""
    if eurostat is None:
        print("ERROR: 'eurostat' package not installed. Run: pip install eurostat")
        sys.exit(1)

    # Create output directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output2")
    os.makedirs(output_dir, exist_ok=True)

    # Counters
    cn_codes_to_extract = [c for c in COMEXT_CN_CODES if c not in EXCLUDED_CN]
    total_comext = len(cn_codes_to_extract)

    sts_pairs = [
        (ds, nace) for ds in STS_DATASETS for nace in NACE_CODES
        if ds not in EXCLUDED_STS_DATASETS and (ds, nace) not in EXCLUDED_STS_COMBOS
    ]
    total_sts = len(sts_pairs)

    demand_pairs = [
        (ds, nace) for ds, nace_list in DEMAND_STS_SERIES.items() for nace in nace_list
    ]
    total_demand = len(demand_pairs)

    total = total_comext + total_sts + total_demand
    series_idx = 0
    success_count = 0

    print("=" * 70)
    print("EUROSTAT DATABASE-READY EXTRACTION")
    print(f"Comext: {total_comext} CN codes | STS: {total_sts} | Demand STS: {total_demand}")
    print(f"Total: {total} series (68 excluded) | Period: {START_PERIOD}-01 to {END_PERIOD}-12")
    print(f"Output: {output_dir}/")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # Phase 1: Comext trade data → comext.csv
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("PHASE 1: COMEXT TRADE DATA (monthly, bilateral: WORLD+EU27+CN)")
    print(f"{'=' * 70}")

    comext_frames = []

    for i, cn_code in enumerate(cn_codes_to_extract, 1):
        series_idx += 1
        side = "demand" if cn_code in DEMAND_CN_CODES else "supply"

        print(f"\n[{series_idx}/{total}] Comext {i}/{total_comext}: CN {cn_code}")
        print("-" * 50)

        t0 = time.time()
        try:
            df = extract_comext_monthly(cn_code)
        except Exception as e:
            print(f"  UNEXPECTED ERROR: {e}")
            traceback.print_exc()
            df = pd.DataFrame()

        elapsed = time.time() - t0

        if df is not None and not df.empty:
            # Normalise column names to lowercase for consistent access
            df.columns = [c.strip() for c in df.columns]

            # Build the flat row set
            col_map = {}
            for c in df.columns:
                cl = c.lower()
                if cl == "reporter":
                    col_map[c] = "reporter"
                elif cl == "partner":
                    col_map[c] = "partner"
                elif cl == "flow":
                    col_map[c] = "flow"
                elif cl == "indicators":
                    col_map[c] = "indicator"
                elif cl == "time_period":
                    col_map[c] = "date"
                elif cl == "obs_value":
                    col_map[c] = "value"

            df = df.rename(columns=col_map)

            # Keep only the columns we need (some may not exist if API format changes)
            keep = ["reporter", "partner", "flow", "indicator", "date", "value"]
            keep = [c for c in keep if c in df.columns]
            df = df[keep].copy()

            df["cn_code"] = cn_code
            df["cn_description"] = CN_DESCRIPTIONS.get(cn_code, cn_code)
            df["side"] = side

            comext_frames.append(df)
            success_count += 1
            print(f"  Collected {len(df)} rows (elapsed {elapsed:.1f}s)")
        else:
            print(f"  No data (elapsed {elapsed:.1f}s)")

        if series_idx < total:
            time.sleep(1.5)

    # Write comext.csv
    if comext_frames:
        comext_all = pd.concat(comext_frames, ignore_index=True)
        # Final column order
        col_order = ["cn_code", "cn_description", "side", "reporter", "partner",
                      "flow", "indicator", "date", "value"]
        col_order = [c for c in col_order if c in comext_all.columns]
        comext_all = comext_all[col_order]
        comext_path = os.path.join(output_dir, "comext.csv")
        comext_all.to_csv(comext_path, index=False)
        print(f"\nSaved {comext_path}: {len(comext_all):,} rows, "
              f"{comext_all['cn_code'].nunique()} CN codes")
    else:
        print("\nNo Comext data collected.")

    # -----------------------------------------------------------------------
    # Phase 2: STS monthly indices → sts.csv (part 1)
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("PHASE 2: STS MONTHLY INDICES")
    print(f"{'=' * 70}")

    sts_frames = []

    for idx, (dataset, nace) in enumerate(sts_pairs, 1):
        series_idx += 1
        side = "supply" if nace in SUPPLY_NACE else "demand"

        print(f"\n[{series_idx}/{total}] STS {idx}/{total_sts}: {dataset} x {nace}")
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
            melted = _melt_sts_df(df, dataset, nace, side)
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

    # -----------------------------------------------------------------------
    # Phase 3: Demand-side STS → appended to sts_frames
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("PHASE 3: DEMAND-SIDE STS (retail, logistics, confidence)")
    print(f"{'=' * 70}")

    for idx, (dataset, nace) in enumerate(demand_pairs, 1):
        series_idx += 1

        print(f"\n[{series_idx}/{total}] Demand STS {idx}/{total_demand}: "
              f"{dataset} x {nace}")
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
            melted = _melt_sts_df(df, dataset, nace, side="demand")
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

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"\n  Comext:      {len(comext_frames)}/{total_comext} CN codes extracted")
    print(f"  STS+Demand:  {len(sts_frames)}/{total_sts + total_demand} series extracted")
    print(f"  Total:       {success_count}/{total} series extracted successfully")
    print(f"\nOutput in: {output_dir}/")


if __name__ == "__main__":
    run_extraction()
