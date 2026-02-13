#!/usr/bin/env python3
"""
Eurostat Data Quality Testing Script
=====================================
Extracts the 10 most critical series for Avery Dennison market intelligence
and produces a quality assessment report.

Series tested:
  1. PRODCOM — Self-adhesive plastic film (wide rolls) [22292240]
  2. PRODCOM — Self-adhesive paper and paperboard [17127733]
  3. PRODCOM — Self-adhesive printed labels [17291120]
  4. PRODCOM — PET film <= 0.35mm [22213065]
  5. PRODCOM — BOPP film <= 0.10mm [22213021]
  6. Comext  — Self-adhesive plastic trade [39199080]
  7. Comext  — Self-adhesive paper trade [481141]
  8. STS     — Industrial production index, C2229 [sts_inpr_m]
  9. STS     — Producer price index, C2052 [sts_inpp_m]
 10. SBS     — Structural business stats, C2229 [sbs_na_ind_r2]

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
    print("ERROR: 'eurostat' package not installed. Run: pip install eurostat")
    sys.exit(1)

from utils import assess_quality, ensure_output_dir, write_quality_report


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

START_YEAR = 2015
END_YEAR = 2024

# EU-27 ISO codes — used by BOTH DS-datasets and standard datasets
EU27_ISO = sorted([
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES",
    "FI", "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK",
])
EU27_ISO_PLUS = EU27_ISO + ["EU27_2020"]

# PRODCOM indicator codes
PRODCOM_INDICATORS = ["PRODVAL", "PRODQNT"]

# Comext indicator/flow codes
COMEXT_FLOW_IMPORT = "1"
COMEXT_FLOW_EXPORT = "2"
COMEXT_INDICATORS = ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"]


# ---------------------------------------------------------------------------
# Series definitions
# ---------------------------------------------------------------------------

SERIES = [
    {
        "id": 1,
        "name": "Self-Adhesive Plastic Film (wide rolls)",
        "type": "prodcom",
        "dataset": "DS-059358",
        "code": "22292240",
        "filename": "01_prodcom_sa_plastic_film.csv",
    },
    {
        "id": 2,
        "name": "Self-Adhesive Paper & Paperboard",
        "type": "prodcom",
        "dataset": "DS-059358",
        "code": "17127733",
        "filename": "02_prodcom_sa_paper.csv",
    },
    {
        "id": 3,
        "name": "Self-Adhesive Printed Labels",
        "type": "prodcom",
        "dataset": "DS-059358",
        "code": "17291120",
        "filename": "03_prodcom_sa_labels.csv",
    },
    {
        "id": 4,
        "name": "PET Film <= 0.35mm",
        "type": "prodcom",
        "dataset": "DS-059358",
        "code": "22213065",
        "filename": "04_prodcom_pet_film.csv",
    },
    {
        "id": 5,
        "name": "BOPP Film <= 0.10mm",
        "type": "prodcom",
        "dataset": "DS-059358",
        "code": "22213021",
        "filename": "05_prodcom_bopp_film.csv",
    },
    {
        "id": 6,
        "name": "Self-Adhesive Plastic Trade (CN 39199080)",
        "type": "comext",
        "dataset": "DS-045409",
        "code": "39199080",
        "filename": "06_trade_sa_plastic.csv",
    },
    {
        "id": 7,
        "name": "Self-Adhesive Paper Trade (HS6 481141)",
        "type": "comext",
        "dataset": "DS-045409",
        "code": "481141",
        "filename": "07_trade_sa_paper.csv",
    },
    {
        "id": 8,
        "name": "Industrial Production Index (C2229)",
        "type": "sts",
        "dataset": "sts_inpr_m",
        "nace": "C2229",
        "filename": "08_sts_production_index.csv",
    },
    {
        "id": 9,
        "name": "Producer Price Index (C2052)",
        "type": "sts",
        "dataset": "sts_inpp_m",
        "nace": "C2052",
        "filename": "09_sts_price_index.csv",
    },
    {
        "id": 10,
        "name": "Structural Business Stats (C2229)",
        "type": "sbs",
        "dataset": "sbs_na_ind_r2",
        "nace": "C2229",
        "filename": "10_sbs_structure.csv",
    },
]


# ---------------------------------------------------------------------------
# Extraction functions
# ---------------------------------------------------------------------------

def extract_prodcom(series_def):
    """
    Extract PRODCOM data from DS-059358.
    DSD dimension order: freq.reporter.product.indicators
    Reporter uses ISO country codes. Product uses 8-digit PRODCOM codes.
    """
    dataset = series_def["dataset"]
    product_code = series_def["code"]

    # Attempt 1: Direct SDMX REST API (most reliable for DS-datasets)
    print(f"  Trying direct SDMX REST API for {dataset}, product={product_code}...")
    df = _prodcom_direct_api(product_code)
    if df is not None and not df.empty:
        return df

    # Attempt 2: eurostat package with correct lowercase dimension names
    print(f"  Trying eurostat.get_sdmx_data_df with lowercase keys...")
    try:
        filter_pars = {
            "freq": ["A"],
            "product": [product_code],
            "indicators": PRODCOM_INDICATORS,
        }
        df = eurostat.get_sdmx_data_df(
            dataset,
            StartPeriod=START_YEAR,
            EndPeriod=END_YEAR,
            filter_pars=filter_pars,
            flags=True,
            verbose=False,
        )
        if df is not None and not df.empty:
            print(f"  -> Success via eurostat package: {len(df)} rows")
            return df
        print("  -> Empty result from eurostat package.")
    except Exception as e:
        print(f"  -> eurostat package failed: {e}")

    return pd.DataFrame()


def _prodcom_direct_api(product_code):
    """
    Direct REST API call to Eurostat SDMX 2.1 endpoint for PRODCOM.
    DSD key: freq.reporter.product.indicators
    """
    base_url = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1"
    indicators = "+".join(PRODCOM_INDICATORS)
    reporters = "+".join(EU27_ISO_PLUS)

    # Try with all EU27 countries + aggregate
    url = (
        f"{base_url}/data/DS-059358/"
        f"A.{reporters}.{product_code}.{indicators}"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )

    try:
        resp = requests.get(url, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success via direct API: {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}, "
                  f"length {len(resp.content)}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Direct API failed: {e}")

    # Fallback: omit reporter to get all countries
    print("  Trying without country filter...")
    url_open = (
        f"{base_url}/data/DS-059358/"
        f"A..{product_code}.{indicators}"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )
    try:
        resp = requests.get(url_open, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success (all countries): {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}, length {len(resp.content)}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Failed: {e}")

    # Fallback: try just PRODVAL indicator with fewer countries
    print("  Trying minimal query (5 countries, PRODVAL only)...")
    top5 = "+".join(["DE", "FR", "IT", "ES", "NL"])
    url_min = (
        f"{base_url}/data/DS-059358/"
        f"A.{top5}.{product_code}.PRODVAL"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )
    try:
        resp = requests.get(url_min, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success (minimal): {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}, length {len(resp.content)}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Failed: {e}")

    return pd.DataFrame()


def extract_comext(series_def):
    """
    Extract Comext trade data from DS-045409.
    DSD dimension order: freq.reporter.partner.product.flow.indicators
    Reporter uses ISO codes. Partner "WORLD" for total trade.
    """
    dataset = series_def["dataset"]
    cn_code = series_def["code"]

    # Attempt 1: Direct SDMX REST API
    print(f"  Trying direct SDMX REST API for {dataset}, product={cn_code}...")
    df = _comext_direct_api(cn_code)
    if df is not None and not df.empty:
        return df

    # Attempt 2: eurostat package with correct lowercase dimension names
    print(f"  Trying eurostat.get_sdmx_data_df with lowercase keys...")
    try:
        filter_pars = {
            "freq": ["A"],
            "reporter": EU27_ISO,
            "partner": ["WORLD"],
            "product": [cn_code],
            "flow": [COMEXT_FLOW_IMPORT, COMEXT_FLOW_EXPORT],
            "indicators": COMEXT_INDICATORS,
        }
        df = eurostat.get_sdmx_data_df(
            dataset,
            StartPeriod=START_YEAR,
            EndPeriod=END_YEAR,
            filter_pars=filter_pars,
            flags=True,
            verbose=False,
        )
        if df is not None and not df.empty:
            print(f"  -> Success via eurostat package: {len(df)} rows")
            return df
        print("  -> Empty result from eurostat package.")
    except Exception as e:
        print(f"  -> eurostat package failed: {e}")

    return pd.DataFrame()


def _comext_direct_api(cn_code):
    """
    Direct REST API call for Comext trade data.
    DSD key: freq.reporter.partner.product.flow.indicators
    """
    base_url = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1"
    reporters = "+".join(EU27_ISO)
    indicators = "+".join(COMEXT_INDICATORS)
    flows = f"{COMEXT_FLOW_IMPORT}+{COMEXT_FLOW_EXPORT}"

    url = (
        f"{base_url}/data/DS-045409/"
        f"A.{reporters}.WORLD.{cn_code}.{flows}.{indicators}"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )

    try:
        resp = requests.get(url, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success via direct API: {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}, "
                  f"length {len(resp.content)}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Direct API failed: {e}")

    # Fallback: fewer countries
    print("  Trying with top 10 countries only...")
    top10 = "+".join(["DE", "FR", "IT", "ES", "NL", "BE", "PL", "AT", "CZ", "SE"])
    url_small = (
        f"{base_url}/data/DS-045409/"
        f"A.{top10}.WORLD.{cn_code}.{flows}.{indicators}"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )
    try:
        resp = requests.get(url_small, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success (top 10): {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}, length {len(resp.content)}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Failed: {e}")

    # Last resort: single country test
    print("  Trying single country (DE) as connectivity test...")
    url_de = (
        f"{base_url}/data/DS-045409/"
        f"A.DE.WORLD.{cn_code}.{flows}.VALUE_IN_EUROS"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )
    try:
        resp = requests.get(url_de, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success (DE only): {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}, length {len(resp.content)}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Failed: {e}")

    return pd.DataFrame()


def extract_sts(series_def):
    """
    Extract Short-Term Statistics (monthly indices) using eurostat.get_data_df.
    These are standard Eurostat datasets with ISO geo codes.
    """
    dataset = series_def["dataset"]
    nace = series_def["nace"]

    print(f"  Trying eurostat.get_data_df for {dataset}, nace_r2={nace}...")

    # Attempt 1: eurostat package — seasonally adjusted, index 2015=100
    try:
        filter_pars = {
            "startPeriod": START_YEAR,
            "endPeriod": END_YEAR,
            "nace_r2": [nace],
            "s_adj": ["SCA"],
            "unit": ["I15"],
        }
        df = eurostat.get_data_df(
            dataset,
            filter_pars=filter_pars,
            flags=True,
        )
        if df is not None and not df.empty:
            print(f"  -> Success: {len(df)} rows, {len(df.columns)} columns")
            return df
        print("  -> Empty result.")
    except Exception as e:
        print(f"  -> Failed with SCA/I15: {e}")

    # Attempt 2: Try with broader filters
    print("  Retrying with broader filters...")
    try:
        filter_pars = {
            "startPeriod": START_YEAR,
            "endPeriod": END_YEAR,
            "nace_r2": [nace],
        }
        df = eurostat.get_data_df(
            dataset,
            filter_pars=filter_pars,
            flags=True,
        )
        if df is not None and not df.empty:
            print(f"  -> Success with broad filters: {len(df)} rows")
            return df
        print("  -> Still empty.")
    except Exception as e:
        print(f"  -> Broad filter also failed: {e}")

    # Attempt 3: Direct SDMX-CSV API
    print("  Falling back to direct SDMX-CSV API...")
    return _sts_direct_api(dataset, nace)


def _sts_direct_api(dataset, nace):
    """Direct API call for STS datasets using SDMX-CSV format."""
    # STS dimension order: freq.indic_bt.nace_r2.s_adj.unit.geo
    geos = "+".join(["EU27_2020", "DE", "FR", "IT", "ES", "NL", "PL", "BE", "AT", "SE", "CZ"])
    url = (
        f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/"
        f"data/{dataset}/M.PROD.{nace}.SCA.I15.{geos}"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )
    try:
        resp = requests.get(url, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success via direct API: {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Direct API failed: {e}")

    # Try without indic_bt
    url2 = (
        f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/"
        f"data/{dataset}/.PROD.{nace}.SCA.I15.{geos}"
        f"?startPeriod={START_YEAR}&endPeriod={END_YEAR}"
        f"&format=SDMX-CSV"
    )
    try:
        resp = requests.get(url2, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Success via direct API (alt): {len(df)} rows")
            return df
        else:
            print(f"  -> Status {resp.status_code}")
            if resp.status_code >= 400:
                print(f"     Error: {resp.text[:300]}")
    except Exception as e:
        print(f"  -> Failed: {e}")

    return pd.DataFrame()


def extract_sbs(series_def):
    """
    Extract Structural Business Statistics (annual) using eurostat.get_data_df.
    """
    dataset = series_def["dataset"]
    nace = series_def["nace"]

    print(f"  Trying eurostat.get_data_df for {dataset}, nace_r2={nace}...")

    # Attempt 1: eurostat package — key indicators
    try:
        filter_pars = {
            "startPeriod": START_YEAR,
            "endPeriod": END_YEAR,
            "nace_r2": [nace],
            "indic_sb": [
                "V12110",  # Turnover
                "V16110",  # Persons employed
                "V12150",  # Value added at factor cost
                "V11110",  # Number of enterprises
                "V15110",  # Gross investment in tangible goods
            ],
        }
        df = eurostat.get_data_df(
            dataset,
            filter_pars=filter_pars,
            flags=True,
        )
        if df is not None and not df.empty:
            print(f"  -> Success: {len(df)} rows")
            return df
        print("  -> Empty result.")
    except Exception as e:
        print(f"  -> Failed: {e}")

    # Attempt 2: Broader filter
    print("  Retrying with just NACE filter...")
    try:
        filter_pars = {
            "startPeriod": START_YEAR,
            "endPeriod": END_YEAR,
            "nace_r2": [nace],
        }
        df = eurostat.get_data_df(
            dataset,
            filter_pars=filter_pars,
            flags=True,
        )
        if df is not None and not df.empty:
            print(f"  -> Success with broad filter: {len(df)} rows")
            return df
        print("  -> Still empty.")
    except Exception as e:
        print(f"  -> Broad filter also failed: {e}")

    return pd.DataFrame()


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_extraction(series_list=None):
    """
    Run the full extraction and quality assessment pipeline.

    Parameters
    ----------
    series_list : list or None
        If provided, only extract these series (by id). If None, extract all 10.
    """
    output_dir = ensure_output_dir()
    all_metrics = []
    all_code_infos = []
    results = []

    target_series = SERIES
    if series_list:
        target_series = [s for s in SERIES if s["id"] in series_list]

    total = len(target_series)
    success_count = 0

    print("=" * 70)
    print("EUROSTAT DATA QUALITY TESTING")
    print(f"Extracting {total} priority series ({START_YEAR}-{END_YEAR})")
    print("=" * 70)

    for i, sdef in enumerate(target_series, 1):
        sid = sdef["id"]
        sname = sdef["name"]
        stype = sdef["type"]
        filename = sdef["filename"]

        print(f"\n[{i}/{total}] Series #{sid}: {sname}")
        print("-" * 50)

        t0 = time.time()
        df = pd.DataFrame()

        try:
            if stype == "prodcom":
                df = extract_prodcom(sdef)
            elif stype == "comext":
                df = extract_comext(sdef)
            elif stype == "sts":
                df = extract_sts(sdef)
            elif stype == "sbs":
                df = extract_sbs(sdef)
            else:
                print(f"  Unknown type: {stype}")
        except Exception as e:
            print(f"  UNEXPECTED ERROR: {e}")
            traceback.print_exc()

        elapsed = time.time() - t0

        # Save CSV
        csv_path = os.path.join(output_dir, filename)
        if df is not None and not df.empty:
            df.to_csv(csv_path, index=False)
            print(f"  Saved: {csv_path} ({len(df)} rows)")
            success_count += 1
        else:
            # Write empty CSV with a note
            with open(csv_path, "w") as f:
                f.write("# No data returned for this series\n")
            print(f"  WARNING: No data returned. Empty placeholder saved.")
            df = pd.DataFrame()

        # Quality assessment
        code_info = sdef.get("code", sdef.get("nace", "")) + f" ({sdef['dataset']})"
        metrics = assess_quality(df, sname)
        metrics["notes"].append(f"Extraction time: {elapsed:.1f}s")
        if df.empty:
            metrics["notes"].append(
                "FAILED — no data extracted. Check API availability or filter parameters."
            )

        all_metrics.append(metrics)
        all_code_infos.append(code_info)

        results.append({
            "id": sid,
            "name": sname,
            "success": not df.empty,
            "rows": len(df),
            "elapsed": elapsed,
        })

        # Be polite to the API
        if i < total:
            time.sleep(2)

    # Write quality report
    print("\n" + "=" * 70)
    write_quality_report(all_metrics, all_code_infos)

    # Summary
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    for r in results:
        status = "OK" if r["success"] else "FAILED"
        print(f"  [{status:6s}] #{r['id']:2d} {r['name']:45s} "
              f"{r['rows']:6d} rows  ({r['elapsed']:.1f}s)")

    print(f"\nResult: {success_count}/{total} series extracted successfully.")
    if success_count >= 8:
        print("PASS — Sufficient data coverage for market intelligence.")
    elif success_count >= 5:
        print("PARTIAL — Some series failed. Review quality report for details.")
    else:
        print("WARN — Multiple series failed. Check API availability and filters.")

    print(f"\nOutput files in: {output_dir}/")
    return results


if __name__ == "__main__":
    run_extraction()

    # Generate visualizations
    from visualize import generate_all_charts
    generate_all_charts()
