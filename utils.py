"""
Shared utility functions for Eurostat data quality assessment.
"""

import os
import pandas as pd
from datetime import datetime


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def ensure_output_dir():
    """Create output/ directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return OUTPUT_DIR


def assess_quality(df, series_name, time_col_pattern=None):
    """
    Assess data quality for an extracted Eurostat DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The extracted data.
    series_name : str
        Human-readable series name for the report.
    time_col_pattern : str or None
        If provided, regex pattern to identify time/period columns.
        If None, auto-detects columns matching year patterns or 'time' columns.

    Returns
    -------
    dict with quality metrics:
        - series_name, rows, cols, countries, country_list,
          year_min, year_max, completeness_pct, confidential_count,
          flag_distribution, latest_period, notes
    """
    metrics = {
        "series_name": series_name,
        "rows": len(df),
        "cols": len(df.columns),
        "countries": 0,
        "country_list": [],
        "missing_countries": [],
        "year_min": None,
        "year_max": None,
        "completeness_pct": 0.0,
        "confidential_count": 0,
        "flag_distribution": {},
        "latest_period": None,
        "notes": [],
    }

    if df.empty:
        metrics["notes"].append("DataFrame is empty — no data returned.")
        return metrics

    # Detect geo/country column
    geo_col = _find_geo_column(df)
    if geo_col:
        unique_geos = df[geo_col].dropna().unique()
        metrics["countries"] = len(unique_geos)
        metrics["country_list"] = sorted(unique_geos.tolist())

        # EU-27: accept both EL and GR for Greece
        eu27_el = {
            "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
            "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
            "NL", "PL", "PT", "RO", "SE", "SI", "SK",
        }
        geo_set = set(str(g) for g in unique_geos)
        if all(len(str(g)) <= 3 for g in list(unique_geos)[:5]):
            # Treat GR and EL as equivalent
            if "GR" in geo_set:
                geo_set.add("EL")
            missing = [c for c in sorted(eu27_el) if c not in geo_set]
            metrics["missing_countries"] = missing

    # Detect time columns and range
    time_cols = _find_time_columns(df)
    if time_cols:
        periods = []
        for col in time_cols:
            try:
                year = int(str(col)[:4])
                periods.append(year)
            except (ValueError, TypeError):
                pass
        if periods:
            metrics["year_min"] = min(periods)
            metrics["year_max"] = max(periods)
            metrics["latest_period"] = str(max(periods))
    else:
        # Check for a 'time' or 'TIME_PERIOD' column (long format)
        time_col = _find_time_period_column(df)
        if time_col:
            try:
                years = df[time_col].dropna().apply(lambda x: int(str(x)[:4]))
                metrics["year_min"] = years.min()
                metrics["year_max"] = years.max()
                metrics["latest_period"] = str(years.max())
            except (ValueError, TypeError):
                pass

    # Completeness: % of non-null, non-empty, non-':' values in data columns
    data_cols = _find_data_columns(df, time_cols)
    if data_cols:
        total_cells = len(df) * len(data_cols)
        if total_cells > 0:
            null_count = 0
            conf_count = 0
            flag_dist = {}
            for col in data_cols:
                for val in df[col]:
                    sval = str(val).strip()
                    if pd.isna(val) or sval in ("", ":", "nan", "None"):
                        null_count += 1
                    elif sval.startswith(":"):
                        null_count += 1
                        # Check for flag after colon
                        flag = sval[1:].strip()
                        if flag:
                            if flag == "c":
                                conf_count += 1
                            flag_dist[flag] = flag_dist.get(flag, 0) + 1
            metrics["completeness_pct"] = round(
                100 * (1 - null_count / total_cells), 1
            )
            metrics["confidential_count"] = conf_count
            metrics["flag_distribution"] = flag_dist
    else:
        # Long format: check the 'value' or 'OBS_VALUE' column
        val_col = None
        for candidate in ["value", "OBS_VALUE", "values", "Value"]:
            if candidate in df.columns:
                val_col = candidate
                break
        if val_col:
            total_cells = len(df)
            null_count = df[val_col].isna().sum()
            metrics["completeness_pct"] = round(
                100 * (1 - null_count / total_cells), 1
            ) if total_cells > 0 else 0.0

    return metrics


def format_quality_row(idx, metrics, code_info):
    """
    Format a quality metrics dict as a markdown table row.

    Parameters
    ----------
    idx : int
        Row number (1-based).
    metrics : dict
        Output from assess_quality().
    code_info : str
        Dataset/code identifier string.

    Returns
    -------
    str : markdown table row
    """
    return (
        f"| {idx} | {metrics['series_name']} | {code_info} | "
        f"{metrics['rows']} | {metrics['countries']}/27 | "
        f"{metrics['year_min'] or 'N/A'}-{metrics['year_max'] or 'N/A'} | "
        f"{metrics['completeness_pct']}% | "
        f"{metrics['confidential_count']} | "
        f"{metrics['latest_period'] or 'N/A'} |"
    )


def format_detailed_section(idx, metrics, code_info):
    """
    Format detailed notes for a single series in the quality report.
    """
    lines = [
        f"### {idx}. {metrics['series_name']} ({code_info})",
        "",
    ]
    if metrics["country_list"]:
        lines.append(
            f"- **Countries with data**: {', '.join(metrics['country_list'][:30])}"
        )
        if len(metrics["country_list"]) > 30:
            lines.append(f"  (and {len(metrics['country_list']) - 30} more)")
    if metrics["missing_countries"]:
        lines.append(
            f"- **Countries missing (EU-27)**: {', '.join(metrics['missing_countries'])}"
        )
    if metrics["confidential_count"] > 0:
        lines.append(
            f"- **Confidential values**: {metrics['confidential_count']} suppressed"
        )
    if metrics["flag_distribution"]:
        flags_str = ", ".join(
            f"'{k}': {v}" for k, v in sorted(metrics["flag_distribution"].items())
        )
        lines.append(f"- **Flag distribution**: {{{flags_str}}}")
    for note in metrics.get("notes", []):
        lines.append(f"- **Note**: {note}")
    lines.append("")
    return "\n".join(lines)


def write_quality_report(all_metrics, all_code_infos):
    """
    Write the full quality report to output/quality_report.md.

    Parameters
    ----------
    all_metrics : list of dict
        List of metrics dicts from assess_quality().
    all_code_infos : list of str
        Corresponding code identifiers.
    """
    ensure_output_dir()
    report_path = os.path.join(OUTPUT_DIR, "quality_report.md")

    lines = [
        "# Eurostat Data Quality Assessment Report",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Summary Table",
        "",
        "| # | Series | Dataset | Rows | Countries | Years | Completeness | Confidential | Latest |",
        "|---|--------|---------|------|-----------|-------|-------------|-------------|--------|",
    ]

    for i, (m, c) in enumerate(zip(all_metrics, all_code_infos), 1):
        lines.append(format_quality_row(i, m, c))

    lines.append("")
    lines.append("## Detailed Notes per Series")
    lines.append("")

    for i, (m, c) in enumerate(zip(all_metrics, all_code_infos), 1):
        lines.append(format_detailed_section(i, m, c))

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nQuality report written to: {report_path}")
    return report_path


# --- Internal helpers ---

def _find_geo_column(df):
    """Find the geography/country column."""
    candidates = ["geo", "geo\\TIME_PERIOD", "DECL", "REPORTER", "reporter",
                   "geo\\time", "GEO"]
    for c in candidates:
        if c in df.columns:
            return c
    # Check for columns containing 'geo' or 'decl'
    for c in df.columns:
        cl = c.lower()
        if "geo" in cl or "decl" in cl or "reporter" in cl:
            return c
    return None


def _find_time_columns(df):
    """Find columns that look like time periods (wide format).
    Handles: 2015, 2015-01, 2015M01, 2015-01_value, 2015-01_flag, etc.
    Returns only _value columns (or bare year columns) for quality assessment.
    """
    import re
    time_cols = []
    for c in df.columns:
        sc = str(c).strip()
        # Bare year: 2015, 2015-01, 2015M01
        if re.match(r"^\d{4}(-\d{2})?$", sc) or re.match(r"^\d{4}[MQ]\d{1,2}$", sc):
            time_cols.append(c)
        # Year_value columns: 2015-01_value, 2023_value
        elif re.match(r"^\d{4}(-\d{2})?_value$", sc):
            time_cols.append(c)
    return time_cols


def _find_time_period_column(df):
    """Find a time period column in long format."""
    candidates = ["TIME_PERIOD", "time", "Time", "time_period", "PERIOD"]
    for c in candidates:
        if c in df.columns:
            return c
    for c in df.columns:
        if "time" in c.lower() or "period" in c.lower():
            return c
    return None


def _find_data_columns(df, time_cols):
    """
    Find data columns (typically the time period columns in wide format).
    Returns time_cols if they exist, otherwise empty list.
    """
    if time_cols:
        return time_cols
    return []
