#!/usr/bin/env python3
"""
Eurostat Monthly Data Visualization
=====================================
Reads extracted monthly CSVs from output/comext/ and output/sts/
and generates individual PNG charts.

- Comext: single-panel line chart with imports (red) and exports (blue)
- STS: single-panel line chart with EU27 (bold blue) + top countries

Run standalone:
    python visualize.py

Or called from test_eurostat_extraction.py after extraction completes.
"""

import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# Color palette
COLORS = {
    "blue": "#2563EB",
    "red": "#DC2626",
    "green": "#059669",
    "amber": "#D97706",
    "grey": "#6B7280",
}

COUNTRY_COLORS = [
    "#2563EB", "#DC2626", "#059669", "#D97706", "#7C3AED",
    "#DB2777", "#0891B2", "#65A30D", "#EA580C", "#4F46E5",
]

EU27_AGGREGATES = {"EU27_2020", "EU28", "EA19", "EA20", "EA21"}


# ---------------------------------------------------------------------------
# Description mappings (for chart footnotes)
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
# Helpers
# ---------------------------------------------------------------------------

def _fmt_eur(val, _pos=None):
    """Format EUR values: 1,234,567,890 -> 1.2B"""
    if abs(val) >= 1e9:
        return f"{val / 1e9:.1f}B"
    if abs(val) >= 1e6:
        return f"{val / 1e6:.0f}M"
    if abs(val) >= 1e3:
        return f"{val / 1e3:.0f}K"
    return f"{val:.0f}"


def _style_ax(ax, title, ylabel):
    """Apply consistent styling to an axis."""
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)


def _parse_time_period(tp):
    """Parse a TIME_PERIOD string like '2023-01' or '2023M01' to datetime."""
    s = str(tp).strip()
    s = s.replace("M", "-")
    try:
        return pd.Timestamp(s + "-01")
    except Exception:
        return pd.NaT


# =========================================================================
# Comext Chart (per CN code)
# =========================================================================

def plot_comext(csv_path, cn_code, output_dir):
    """
    Single-panel chart for Comext trade data:
    Two lines — total EU27 monthly imports (red) and exports (blue) in EUR.
    """
    df = pd.read_csv(csv_path)
    desc = CN_DESCRIPTIONS.get(cn_code, cn_code)

    # Filter for value indicator
    if "indicators" not in df.columns:
        print(f"  SKIP CN_{cn_code}.png: no 'indicators' column")
        return None

    val = df[df["indicators"] == "VALUE_IN_EUROS"].copy()
    if val.empty:
        print(f"  SKIP CN_{cn_code}.png: no VALUE_IN_EUROS data")
        return None

    # Parse TIME_PERIOD to datetime
    val["date"] = val["TIME_PERIOD"].apply(_parse_time_period)
    val = val.dropna(subset=["date"])
    if val.empty:
        print(f"  SKIP CN_{cn_code}.png: no valid dates")
        return None

    # Sum across all reporters by month and flow
    imports = (val[val["flow"].astype(str) == "1"]
               .groupby("date")["OBS_VALUE"].sum()
               .reset_index().sort_values("date"))
    exports = (val[val["flow"].astype(str) == "2"]
               .groupby("date")["OBS_VALUE"].sum()
               .reset_index().sort_values("date"))

    fig, ax = plt.subplots(figsize=(12, 5))

    if not imports.empty:
        ax.plot(imports["date"], imports["OBS_VALUE"],
                color=COLORS["red"], linewidth=1.5, label="Imports")
    if not exports.empty:
        ax.plot(exports["date"], exports["OBS_VALUE"],
                color=COLORS["blue"], linewidth=1.5, label="Exports")

    _style_ax(ax, f"Trade: CN {cn_code}", "EUR")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    fig.text(0.5, -0.02,
             f"{desc}. Source: Eurostat Comext DS-045409, monthly",
             ha="center", fontsize=7, color=COLORS["grey"], style="italic")

    fig.tight_layout()
    png_path = os.path.join(output_dir, f"CN_{cn_code}.png")
    fig.savefig(png_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: CN_{cn_code}.png")
    return png_path


# =========================================================================
# STS Chart (per dataset x NACE)
# =========================================================================

def plot_sts(csv_path, dataset, nace, output_dir):
    """
    Single-panel chart for STS index data:
    EU27 line (bold blue) + top 3 country lines (thinner, colored).
    """
    df = pd.read_csv(csv_path)

    # Find geo column
    geo_col = None
    for candidate in ["geo\\TIME_PERIOD", "geo\\time", "geo"]:
        if candidate in df.columns:
            geo_col = candidate
            break
    if geo_col is None:
        print(f"  SKIP {dataset}_{nace}.png: no geo column found")
        return None

    # Filter to single series per geo if needed (handles old unclean CSVs)
    rows_per_geo = df.groupby(geo_col).size()
    if rows_per_geo.max() > 1:
        if "s_adj" in df.columns and df["s_adj"].nunique() > 1:
            for pref in ["SCA", "SA", "NSA"]:
                subset = df[df["s_adj"] == pref]
                if not subset.empty:
                    df = subset
                    break
        if "unit" in df.columns and df["unit"].nunique() > 1:
            for pref in ["I21", "I15"]:
                subset = df[df["unit"] == pref]
                if not subset.empty:
                    df = subset
                    break
        rows_per_geo = df.groupby(geo_col).size()
        if rows_per_geo.max() > 1:
            for col in ["indic_bt", "indic"]:
                if col in df.columns and df[col].nunique() > 1:
                    df = df[df[col] == df[col].iloc[0]]
                    break

    # Find date columns: "2023-01_value" or bare "2023-01"
    val_cols = [c for c in df.columns if re.match(r"\d{4}-\d{2}_value$", c)]
    bare_cols = [c for c in df.columns if re.match(r"\d{4}-\d{2}$", c)]
    date_cols = val_cols or bare_cols
    is_value_suffix = bool(val_cols)

    if not date_cols:
        print(f"  SKIP {dataset}_{nace}.png: no date columns")
        return None

    # Parse to long format
    records = []
    for _, row in df.iterrows():
        geo = row[geo_col]
        for c in date_cols:
            if is_value_suffix:
                m = re.match(r"(\d{4})-(\d{2})_value$", c)
            else:
                m = re.match(r"(\d{4})-(\d{2})$", c)
            if m:
                v = row[c]
                if pd.notna(v):
                    try:
                        records.append({
                            "geo": geo,
                            "date": pd.Timestamp(
                                year=int(m.group(1)),
                                month=int(m.group(2)),
                                day=1,
                            ),
                            "value": float(v),
                        })
                    except (ValueError, TypeError):
                        pass

    if not records:
        print(f"  SKIP {dataset}_{nace}.png: no valid data points")
        return None

    long = pd.DataFrame(records)

    fig, ax = plt.subplots(figsize=(12, 5))

    # EU27 line (bold blue)
    eu = long[long["geo"] == "EU27_2020"].sort_values("date")
    eu_label = "EU27"
    if eu.empty:
        for fb in ["EA20", "EA21", "EA19"]:
            eu = long[long["geo"] == fb].sort_values("date")
            if not eu.empty:
                eu_label = fb
                break

    if not eu.empty:
        ax.plot(eu["date"], eu["value"],
                color=COLORS["blue"], linewidth=2.5, label=eu_label, zorder=5)

    # Top 3 countries (excluding aggregates)
    countries = long[~long["geo"].isin(EU27_AGGREGATES)]
    if not countries.empty:
        avg_by_geo = countries.groupby("geo")["value"].mean().nlargest(3)
        for i, (geo, _) in enumerate(avg_by_geo.items()):
            gdata = countries[countries["geo"] == geo].sort_values("date")
            ax.plot(gdata["date"], gdata["value"],
                    linewidth=1, alpha=0.7,
                    color=COUNTRY_COLORS[(i + 1) % len(COUNTRY_COLORS)],
                    label=geo)

    _style_ax(ax, f"{dataset} x {nace}", "Index value")
    ax.legend(fontsize=8, loc="best")
    ax.axhline(y=100, color="black", linewidth=0.5, linestyle="--", alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    ds_desc = STS_DATASET_DESCRIPTIONS.get(dataset, dataset)
    nace_desc = NACE_DESCRIPTIONS.get(nace, nace)
    fig.text(0.5, -0.02,
             f"{ds_desc} -- {nace_desc}. Index (2021=100). Source: Eurostat STS",
             ha="center", fontsize=7, color=COLORS["grey"], style="italic")

    fig.tight_layout()
    png_path = os.path.join(output_dir, f"{dataset}_{nace}.png")
    fig.savefig(png_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {dataset}_{nace}.png")
    return png_path


# =========================================================================
# Main
# =========================================================================

def generate_all_charts():
    """Generate all visualization PNGs from extracted CSVs."""
    comext_dir = os.path.join(OUTPUT_DIR, "comext")
    sts_dir = os.path.join(OUTPUT_DIR, "sts")

    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)

    comext_count = 0
    sts_count = 0

    # --- Comext charts ---
    if os.path.isdir(comext_dir):
        csv_files = sorted(f for f in os.listdir(comext_dir) if f.endswith(".csv"))
        print(f"\nComext: {len(csv_files)} CSVs found")
        for csv_name in csv_files:
            m = re.match(r"CN_(\w+)\.csv$", csv_name)
            if not m:
                continue
            cn_code = m.group(1)
            csv_path = os.path.join(comext_dir, csv_name)
            result = plot_comext(csv_path, cn_code, comext_dir)
            if result:
                comext_count += 1
    else:
        print("\nNo output/comext/ directory found.")

    # --- STS charts ---
    if os.path.isdir(sts_dir):
        csv_files = sorted(f for f in os.listdir(sts_dir) if f.endswith(".csv"))
        print(f"\nSTS: {len(csv_files)} CSVs found")
        for csv_name in csv_files:
            m = re.match(r"(.+)_((?:C|G|H)\w*)\.csv$", csv_name)
            if not m:
                continue
            dataset = m.group(1)
            nace = m.group(2)
            csv_path = os.path.join(sts_dir, csv_name)
            result = plot_sts(csv_path, dataset, nace, sts_dir)
            if result:
                sts_count += 1
    else:
        print("\nNo output/sts/ directory found.")

    print(f"\nCharts generated: {comext_count} Comext + {sts_count} STS "
          f"= {comext_count + sts_count} total")
    print(f"Output in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    generate_all_charts()
