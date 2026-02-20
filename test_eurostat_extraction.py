#!/usr/bin/env python3
"""
Eurostat Monthly Data Extraction Script
========================================
Extracts monthly data for all Comext trade CN codes and STS industry indices
relevant to the European PSA materials, labels, and converting industry.

Series:
  - 61 Comext CN trade codes (DS-045409, monthly) — supply + demand side
  - 11 STS datasets x 19 NACE codes (monthly indices) — supply + demand side
  - 4 demand-side STS datasets (retail, logistics, confidence) x 12 NACE codes

Time range: 2023-01 through 2025-12

Usage:
    python test_eurostat_extraction.py
"""

import os
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

from utils import assess_quality, ensure_output_dir, write_quality_report


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

# Partners: WORLD aggregate + all 27 EU bilateral + China
COMEXT_PARTNERS = "+".join(["WORLD"] + EU27_ISO + ["CN"])

# ---------------------------------------------------------------------------
# CN codes — 46 total
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
    "2009",    # Fruit juices
    "2201",    # Mineral/aerated waters
    "2202",    # Non-alcoholic beverages
    "2203",    # Beer
    "2204",    # Wine
    "2208",    # Spirits
    # Demand-side: HPC / Cleaning
    "3304",    # Beauty/skin care preparations
    "3305",    # Hair preparations
    "3307",    # Shaving, deodorant, bath preparations
    "3402",    # Washing/cleaning preparations
    # Demand-side: Pharma
    "3004",    # Medicaments in dosage form
    # Demand-side: Food (processed)
    "1602",    # Prepared/preserved meat
    "1604",    # Prepared/preserved fish
    "2005",    # Prepared/preserved vegetables
    "2106",    # Food preparations n.e.c.
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
    "C10",   # Food products
    "C11",   # Beverages
    "C12",   # Tobacco
    "C204",  # Soap, detergents, cosmetics, toiletries (HPC)
    "C21",   # Pharmaceuticals
]

# Retail & logistics datasets with their specific NACE codes
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
    # Demand-side CN descriptions
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
    # Demand-side NACE descriptions
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
    # Find geo column
    geo_col = None
    for c in ["geo\\TIME_PERIOD", "geo\\time", "geo"]:
        if c in df.columns:
            geo_col = c
            break
    if geo_col is None:
        return df

    # Drop flag columns
    flag_cols = [c for c in df.columns if c.endswith("_flag")]
    df = df.drop(columns=flag_cols, errors="ignore")

    # Rename value columns: "2023-01_value" -> "2023-01"
    rename = {}
    for c in df.columns:
        if c.endswith("_value"):
            rename[c] = c.replace("_value", "")
    df = df.rename(columns=rename)

    # If multiple rows per geo, filter to single best series
    rows_per_geo = df.groupby(geo_col).size()
    if rows_per_geo.max() <= 1:
        return df

    # Prefer SCA > SA > NSA
    if "s_adj" in df.columns and df["s_adj"].nunique() > 1:
        for pref in ["SCA", "SA", "NSA"]:
            subset = df[df["s_adj"] == pref]
            if not subset.empty:
                df = subset
                break

    # Prefer I21 > I15 > other index units (skip percentage changes)
    if "unit" in df.columns and df["unit"].nunique() > 1:
        for pref in ["I21", "I15", "I10", "I05"]:
            subset = df[df["unit"] == pref]
            if not subset.empty:
                df = subset
                break

    # If still multiple rows per geo (e.g. multiple indicators), pick first
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


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_extraction():
    """Run the full monthly extraction pipeline."""
    if eurostat is None:
        print("ERROR: 'eurostat' package not installed. Run: pip install eurostat")
        sys.exit(1)

    output_dir = ensure_output_dir()
    comext_dir = os.path.join(output_dir, "comext")
    sts_dir = os.path.join(output_dir, "sts")
    os.makedirs(comext_dir, exist_ok=True)
    os.makedirs(sts_dir, exist_ok=True)

    all_metrics = []
    all_code_infos = []
    results = []

    total_comext = len(COMEXT_CN_CODES)
    total_sts = len(STS_DATASETS) * len(NACE_CODES)
    total_demand_sts = sum(len(v) for v in DEMAND_STS_SERIES.values())
    total = total_comext + total_sts + total_demand_sts
    success_count = 0
    series_idx = 0

    print("=" * 70)
    print("EUROSTAT MONTHLY DATA EXTRACTION")
    print(f"Comext: {total_comext} CN codes (bilateral: WORLD+EU27+CN) | "
          f"STS: {len(STS_DATASETS)} datasets x {len(NACE_CODES)} NACE = {total_sts} | "
          f"Demand STS: {total_demand_sts}")
    print(f"Total: {total} series | Period: {START_PERIOD}-01 to {END_PERIOD}-12")
    print("=" * 70)

    # --- Phase 1: Comext trade data (bilateral) ---
    print(f"\n{'=' * 70}")
    print("PHASE 1: COMEXT TRADE DATA (monthly, bilateral: WORLD+EU27+CN)")
    print(f"{'=' * 70}")

    for i, cn_code in enumerate(COMEXT_CN_CODES, 1):
        series_idx += 1
        desc = CN_DESCRIPTIONS.get(cn_code, cn_code)
        series_name = f"Trade CN {cn_code}: {desc}"

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
            csv_path = os.path.join(comext_dir, f"CN_{cn_code}.csv")
            df.to_csv(csv_path, index=False)
            print(f"  Saved: {csv_path}")
            success_count += 1
        else:
            df = pd.DataFrame()

        code_info = f"CN {cn_code} (DS-045409)"
        metrics = assess_quality(df, series_name)
        metrics["notes"].append(f"Extraction time: {elapsed:.1f}s")
        if df.empty:
            metrics["notes"].append("No data returned.")

        all_metrics.append(metrics)
        all_code_infos.append(code_info)
        results.append({
            "type": "comext",
            "code": cn_code,
            "name": series_name,
            "success": not df.empty,
            "rows": len(df),
            "elapsed": elapsed,
        })

        if series_idx < total:
            time.sleep(1.5)

    # --- Phase 2: STS monthly indices ---
    print(f"\n{'=' * 70}")
    print("PHASE 2: STS MONTHLY INDICES")
    print(f"{'=' * 70}")

    sts_idx = 0
    for dataset in STS_DATASETS:
        for nace in NACE_CODES:
            series_idx += 1
            sts_idx += 1
            ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
            nace_desc = NACE_DESCRIPTIONS.get(nace, nace)
            series_name = f"{ds_desc} x {nace_desc}"

            print(f"\n[{series_idx}/{total}] STS {sts_idx}/{total_sts}: "
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
                csv_path = os.path.join(sts_dir, f"{dataset}_{nace}.csv")
                df.to_csv(csv_path, index=False)
                print(f"  Saved: {csv_path}")
                success_count += 1
            else:
                df = pd.DataFrame()

            code_info = f"{dataset} x {nace}"
            metrics = assess_quality(df, series_name)
            metrics["notes"].append(f"Extraction time: {elapsed:.1f}s")
            if df.empty:
                metrics["notes"].append("No data for this combination.")

            all_metrics.append(metrics)
            all_code_infos.append(code_info)
            results.append({
                "type": "sts",
                "code": f"{dataset}_{nace}",
                "name": series_name,
                "success": not df.empty,
                "rows": len(df),
                "elapsed": elapsed,
            })

            if series_idx < total:
                time.sleep(1)

    # --- Phase 3: Demand-side STS (retail + logistics) ---
    print(f"\n{'=' * 70}")
    print("PHASE 3: DEMAND-SIDE STS (retail, logistics, confidence)")
    print(f"{'=' * 70}")

    demand_idx = 0
    for dataset, nace_list in DEMAND_STS_SERIES.items():
        for nace in nace_list:
            series_idx += 1
            demand_idx += 1
            ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
            nace_desc = NACE_DESCRIPTIONS.get(nace, nace)
            series_name = f"{ds_desc} x {nace_desc}"

            print(f"\n[{series_idx}/{total}] Demand STS {demand_idx}/{total_demand_sts}: "
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
                csv_path = os.path.join(sts_dir, f"{dataset}_{nace}.csv")
                df.to_csv(csv_path, index=False)
                print(f"  Saved: {csv_path}")
                success_count += 1
            else:
                df = pd.DataFrame()

            code_info = f"{dataset} x {nace}"
            metrics = assess_quality(df, series_name)
            metrics["notes"].append(f"Extraction time: {elapsed:.1f}s")
            if df.empty:
                metrics["notes"].append("No data for this combination.")

            all_metrics.append(metrics)
            all_code_infos.append(code_info)
            results.append({
                "type": "sts_demand",
                "code": f"{dataset}_{nace}",
                "name": series_name,
                "success": not df.empty,
                "rows": len(df),
                "elapsed": elapsed,
            })

            if series_idx < total:
                time.sleep(1)

    # --- Quality report ---
    print("\n" + "=" * 70)
    write_quality_report(all_metrics, all_code_infos)

    # --- Summary ---
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)

    comext_ok = sum(1 for r in results if r["type"] == "comext" and r["success"])
    sts_ok = sum(1 for r in results if r["type"] == "sts" and r["success"])
    demand_ok = sum(1 for r in results if r["type"] == "sts_demand" and r["success"])

    print(f"\n  Comext:      {comext_ok}/{total_comext} CN codes extracted")
    print(f"  STS:         {sts_ok}/{total_sts} dataset x NACE combinations extracted")
    print(f"  Demand STS:  {demand_ok}/{total_demand_sts} retail/logistics series extracted")
    print(f"  Total:       {success_count}/{total} series extracted successfully")

    failures = [r for r in results if not r["success"]]
    if failures:
        print(f"\n  Failed series ({len(failures)}):")
        for r in failures[:20]:
            print(f"    - {r['code']}: {r['name'][:60]}")
        if len(failures) > 20:
            print(f"    ... and {len(failures) - 20} more")

    print(f"\nOutput in: {output_dir}/")
    return results


if __name__ == "__main__":
    run_extraction()

    from visualize import generate_all_charts
    generate_all_charts()
