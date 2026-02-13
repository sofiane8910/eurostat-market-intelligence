#!/usr/bin/env python3
"""
Eurostat Data Visualization
============================
Reads extracted CSVs from output/ and generates PNG charts for analysis.

Run standalone:
    python visualize.py

Or called from test_eurostat_extraction.py after extraction completes.
"""

import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# Consistent color palette
COLORS = {
    "primary": "#2563EB",
    "secondary": "#DC2626",
    "tertiary": "#059669",
    "quaternary": "#D97706",
    "grey": "#6B7280",
    "light_blue": "#93C5FD",
    "light_red": "#FCA5A5",
    "covid": "#F87171",
}

COUNTRY_COLORS = [
    "#2563EB", "#DC2626", "#059669", "#D97706", "#7C3AED",
    "#DB2777", "#0891B2", "#65A30D", "#EA580C", "#4F46E5",
]

EU27_AGGREGATES = {"EU27_2020", "EU28", "EA19", "EA20", "EA21"}


def _fmt_eur(val, _pos=None):
    """Format EUR values: 1,234,567,890 -> 1.2B"""
    if abs(val) >= 1e9:
        return f"{val / 1e9:.1f}B"
    if abs(val) >= 1e6:
        return f"{val / 1e6:.0f}M"
    if abs(val) >= 1e3:
        return f"{val / 1e3:.0f}K"
    return f"{val:.0f}"


def _add_covid_band(ax, ymin, ymax):
    """Add subtle COVID-19 shading."""
    ax.axvspan(2019.8, 2020.5, alpha=0.08, color=COLORS["covid"], zorder=0)
    ax.text(2020.15, ymax * 0.97, "COVID", fontsize=7, color=COLORS["covid"],
            alpha=0.6, ha="center", va="top")


def _style_ax(ax, title, ylabel, xlabel="Year"):
    """Apply consistent styling to an axis."""
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)


def _savefig(fig, filename):
    """Save figure to output/ directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {filename}")
    return path


# =========================================================================
# PRODCOM Charts (Series 1-5)
# =========================================================================

def plot_prodcom(csv_path, png_name, title, top_n=7):
    """
    Generate a 3-panel chart for a PRODCOM series:
      - Top-left: EU27 production value time series
      - Top-right: EU27 production volume time series
      - Bottom: Top N country breakdown (latest year, stacked bars over time)
    """
    df = pd.read_csv(csv_path)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.98)

    # --- Panel 1: EU27 Production Value ---
    ax1 = axes[0, 0]
    eu_val = df[(df["reporter"] == "EU27_2020") & (df["indicators"] == "PRODVAL")]
    eu_val = eu_val.sort_values("TIME_PERIOD")
    if not eu_val.empty:
        ax1.bar(eu_val["TIME_PERIOD"], eu_val["OBS_VALUE"],
                color=COLORS["primary"], alpha=0.85, width=0.7)
        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
        ymax = eu_val["OBS_VALUE"].max() * 1.15
        _add_covid_band(ax1, 0, ymax)
        ax1.set_ylim(0, ymax)
    _style_ax(ax1, "EU27 Sold Production Value", "EUR")

    # --- Panel 2: EU27 Production Volume ---
    ax2 = axes[0, 1]
    eu_vol = df[(df["reporter"] == "EU27_2020") & (df["indicators"] == "PRODQNT")]
    eu_vol = eu_vol.sort_values("TIME_PERIOD")
    if not eu_vol.empty:
        ax2.bar(eu_vol["TIME_PERIOD"], eu_vol["OBS_VALUE"],
                color=COLORS["tertiary"], alpha=0.85, width=0.7)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
        ymax = eu_vol["OBS_VALUE"].max() * 1.15
        _add_covid_band(ax2, 0, ymax)
        ax2.set_ylim(0, ymax)
    _style_ax(ax2, "EU27 Sold Production Volume", "Units / kg")

    # --- Panel 3: Top countries by value (latest year) ---
    ax3 = axes[1, 0]
    countries = df[
        (df["indicators"] == "PRODVAL") &
        (~df["reporter"].isin(EU27_AGGREGATES))
    ]
    latest_yr = countries["TIME_PERIOD"].max()
    top = countries[countries["TIME_PERIOD"] == latest_yr].nlargest(top_n, "OBS_VALUE")
    top_codes = top["reporter"].tolist()

    if top_codes:
        for i, cc in enumerate(top_codes):
            cc_data = countries[countries["reporter"] == cc].sort_values("TIME_PERIOD")
            ax3.plot(cc_data["TIME_PERIOD"], cc_data["OBS_VALUE"],
                     marker="o", markersize=4, linewidth=1.5,
                     color=COUNTRY_COLORS[i % len(COUNTRY_COLORS)], label=cc)
        ax3.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
        ax3.legend(fontsize=7, ncol=2, loc="upper left")
        ymax = countries[countries["reporter"].isin(top_codes)]["OBS_VALUE"].max() * 1.15
        _add_covid_band(ax3, 0, ymax)
    _style_ax(ax3, f"Top {top_n} Countries — Production Value", "EUR")

    # --- Panel 4: Implied unit value (EUR/unit) ---
    ax4 = axes[1, 1]
    eu_merged = pd.merge(
        eu_val[["TIME_PERIOD", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "value"}),
        eu_vol[["TIME_PERIOD", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "volume"}),
        on="TIME_PERIOD", how="inner"
    )
    if not eu_merged.empty and (eu_merged["volume"] > 0).all():
        eu_merged["unit_value"] = eu_merged["value"] / eu_merged["volume"]
        ax4.plot(eu_merged["TIME_PERIOD"], eu_merged["unit_value"],
                 marker="s", markersize=5, linewidth=2, color=COLORS["quaternary"])
        ax4.fill_between(eu_merged["TIME_PERIOD"], eu_merged["unit_value"],
                         alpha=0.1, color=COLORS["quaternary"])
        ymin = eu_merged["unit_value"].min() * 0.85
        ymax = eu_merged["unit_value"].max() * 1.15
        _add_covid_band(ax4, ymin, ymax)
    _style_ax(ax4, "EU27 Implied Unit Value", "EUR / unit")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _savefig(fig, png_name)


# =========================================================================
# Trade Charts (Series 6-7)
# =========================================================================

def plot_trade(csv_path, png_name, title):
    """
    Generate a 2x2 chart for trade data:
      - Top-left: Import vs Export value time series
      - Top-right: Trade balance
      - Bottom-left: Top importers
      - Bottom-right: Top exporters
    """
    df = pd.read_csv(csv_path)
    val = df[df["indicators"] == "VALUE_IN_EUROS"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.98)

    # --- Imports vs Exports (total EU27) ---
    ax1 = axes[0, 0]
    imports = val[val["flow"].astype(str) == "1"].groupby("TIME_PERIOD")["OBS_VALUE"].sum().reset_index()
    exports = val[val["flow"].astype(str) == "2"].groupby("TIME_PERIOD")["OBS_VALUE"].sum().reset_index()
    imports = imports.sort_values("TIME_PERIOD")
    exports = exports.sort_values("TIME_PERIOD")

    w = 0.35
    if not imports.empty:
        ax1.bar(imports["TIME_PERIOD"] - w / 2, imports["OBS_VALUE"],
                width=w, color=COLORS["secondary"], alpha=0.8, label="Imports")
    if not exports.empty:
        ax1.bar(exports["TIME_PERIOD"] + w / 2, exports["OBS_VALUE"],
                width=w, color=COLORS["primary"], alpha=0.8, label="Exports")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
    ax1.legend(fontsize=8)
    ymax = max(
        imports["OBS_VALUE"].max() if not imports.empty else 0,
        exports["OBS_VALUE"].max() if not exports.empty else 0,
    ) * 1.15
    _add_covid_band(ax1, 0, ymax)
    _style_ax(ax1, "EU27 Total Imports vs Exports (sum of all reporters)", "EUR")

    # --- Trade Balance ---
    ax2 = axes[0, 1]
    if not imports.empty and not exports.empty:
        merged = pd.merge(imports, exports, on="TIME_PERIOD", suffixes=("_imp", "_exp"))
        merged["balance"] = merged["OBS_VALUE_exp"] - merged["OBS_VALUE_imp"]
        colors_bar = [COLORS["tertiary"] if b >= 0 else COLORS["secondary"]
                      for b in merged["balance"]]
        ax2.bar(merged["TIME_PERIOD"], merged["balance"], color=colors_bar, alpha=0.85, width=0.7)
        ax2.axhline(y=0, color="black", linewidth=0.5)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
        yabs = max(abs(merged["balance"].min()), abs(merged["balance"].max())) * 1.3
        _add_covid_band(ax2, -yabs, yabs)
    _style_ax(ax2, "Trade Balance (Exports - Imports)", "EUR")
    ax2.text(0.02, 0.02, "Note: sums individual country reports;\nincludes intra-EU double counting",
             transform=ax2.transAxes, fontsize=7, color=COLORS["grey"], style="italic")

    # --- Top importers (latest year) ---
    ax3 = axes[1, 0]
    imp_data = val[val["flow"].astype(str) == "1"]
    latest_yr = imp_data["TIME_PERIOD"].max()
    top_imp = imp_data[imp_data["TIME_PERIOD"] == latest_yr].nlargest(10, "OBS_VALUE")
    if not top_imp.empty:
        ax3.barh(top_imp["reporter"][::-1], top_imp["OBS_VALUE"][::-1],
                 color=COLORS["secondary"], alpha=0.8)
        ax3.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
    _style_ax(ax3, f"Top 10 Importers ({latest_yr:.0f})", "", "EUR")

    # --- Top exporters (latest year) ---
    ax4 = axes[1, 1]
    exp_data = val[val["flow"].astype(str) == "2"]
    top_exp = exp_data[exp_data["TIME_PERIOD"] == latest_yr].nlargest(10, "OBS_VALUE")
    if not top_exp.empty:
        ax4.barh(top_exp["reporter"][::-1], top_exp["OBS_VALUE"][::-1],
                 color=COLORS["primary"], alpha=0.8)
        ax4.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
    _style_ax(ax4, f"Top 10 Exporters ({latest_yr:.0f})", "", "EUR")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _savefig(fig, png_name)


# =========================================================================
# STS Index Charts (Series 8-9)
# =========================================================================

def plot_sts_index(csv_path, png_name, title, index_label="Index (2015=100)"):
    """
    Generate a 2-panel chart for STS monthly index:
      - Left: Multi-country monthly time series
      - Right: Annual averages comparison
    """
    df = pd.read_csv(csv_path)
    geo_col = "geo\\TIME_PERIOD"

    val_cols = [c for c in df.columns if c.endswith("_value")]
    if not val_cols:
        print(f"  SKIP {png_name}: no _value columns found")
        return None

    # Parse into long format for easier plotting
    records = []
    for _, row in df.iterrows():
        geo = row[geo_col]
        for c in val_cols:
            m = re.match(r"(\d{4})-(\d{2})_value", c)
            if m:
                v = row[c]
                if pd.notna(v):
                    try:
                        records.append({
                            "geo": geo,
                            "year": int(m.group(1)),
                            "month": int(m.group(2)),
                            "value": float(v),
                            "date": float(m.group(1)) + (float(m.group(2)) - 0.5) / 12,
                        })
                    except (ValueError, TypeError):
                        pass

    if not records:
        print(f"  SKIP {png_name}: no valid data points")
        return None

    long = pd.DataFrame(records)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)

    # --- Left: Monthly time series by country ---
    ax1 = axes[0]
    # Prioritize EU27, then large countries
    priority = ["EU27_2020", "DE", "FR", "IT", "ES", "NL", "IE", "EL"]
    available = [g for g in priority if g in long["geo"].unique()]
    others = [g for g in long["geo"].unique() if g not in available and g not in EU27_AGGREGATES]
    plot_geos = available[:8]

    for i, geo in enumerate(plot_geos):
        gdata = long[long["geo"] == geo].sort_values("date")
        lw = 2.5 if geo == "EU27_2020" else 1.0
        alpha = 1.0 if geo == "EU27_2020" else 0.7
        ax1.plot(gdata["date"], gdata["value"],
                 linewidth=lw, alpha=alpha,
                 color=COUNTRY_COLORS[i % len(COUNTRY_COLORS)],
                 label=geo)

    ax1.axhline(y=100, color="black", linewidth=0.5, linestyle="--", alpha=0.3)
    ax1.legend(fontsize=7, loc="best")
    ymin = long["value"].min() * 0.9
    ymax = long["value"].max() * 1.1
    _add_covid_band(ax1, ymin, ymax)
    _style_ax(ax1, "Monthly Index by Country", index_label, "")

    # --- Right: Annual average for EU27 ---
    ax2 = axes[1]
    eu_data = long[long["geo"] == "EU27_2020"]
    if eu_data.empty:
        # Fall back to EA20
        for fallback in ["EA20", "EA21", "EA19"]:
            eu_data = long[long["geo"] == fallback]
            if not eu_data.empty:
                break

    if not eu_data.empty:
        annual = eu_data.groupby("year")["value"].mean().reset_index()
        colors_bar = [COLORS["tertiary"] if v >= 100 else COLORS["secondary"]
                      for v in annual["value"]]
        ax2.bar(annual["year"], annual["value"], color=colors_bar, alpha=0.85, width=0.7)
        ax2.axhline(y=100, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
        for _, r in annual.iterrows():
            ax2.text(r["year"], r["value"] + 0.5, f"{r['value']:.1f}",
                     ha="center", va="bottom", fontsize=7)
        ymin = annual["value"].min() * 0.9
        ymax = annual["value"].max() * 1.1
        _add_covid_band(ax2, ymin, ymax)
        geo_label = "EU27" if "EU27_2020" in eu_data["geo"].values else eu_data["geo"].iloc[0]
        _style_ax(ax2, f"{geo_label} Annual Average", index_label)
    else:
        _style_ax(ax2, "Annual Average (no EU27 data)", index_label)

    fig.tight_layout()
    return _savefig(fig, png_name)


# =========================================================================
# SBS Chart (Series 10)
# =========================================================================

def plot_sbs(csv_path, png_name, title):
    """
    Generate a 2x2 chart for SBS structural data:
      - Turnover, Value Added, Employment, Number of enterprises
    """
    df = pd.read_csv(csv_path)
    geo_col = "geo\\TIME_PERIOD"
    eu = df[df[geo_col] == "EU27_2020"]

    val_cols = sorted([c for c in df.columns if re.match(r"\d{4}", c)])

    indicator_config = [
        ("V12110", "Turnover", "EUR million", COLORS["primary"]),
        ("V12150", "Value Added at Factor Cost", "EUR million", COLORS["tertiary"]),
        ("V16110", "Persons Employed", "Persons", COLORS["quaternary"]),
        ("V11110", "Number of Enterprises", "Count", COLORS["secondary"]),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.98)

    for idx, (indic, label, unit, color) in enumerate(indicator_config):
        ax = axes[idx // 2, idx % 2]
        row = eu[eu["indic_sb"] == indic]
        if row.empty:
            _style_ax(ax, f"{label} — No Data", unit)
            continue

        years = []
        values = []
        for c in val_cols:
            m = re.match(r"(\d{4})", c)
            if m:
                v = row[c].values[0]
                if pd.notna(v):
                    try:
                        values.append(float(v))
                        years.append(int(m.group(1)))
                    except (ValueError, TypeError):
                        pass

        if years:
            ax.bar(years, values, color=color, alpha=0.85, width=0.7)
            for y, v in zip(years, values):
                ax.text(y, v * 1.02, f"{v:,.0f}", ha="center", va="bottom", fontsize=7)
            ymax = max(values) * 1.2
            _add_covid_band(ax, 0, ymax)
            ax.set_ylim(0, ymax)
        _style_ax(ax, f"EU27 — {label}", unit)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _savefig(fig, png_name)


# =========================================================================
# Summary Overview Charts
# =========================================================================

def plot_summary_market_size():
    """Generate a combined market size overview chart."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle("EU27 PSA Market Overview — PRODCOM Production Values",
                 fontsize=13, fontweight="bold", y=1.02)

    series_info = [
        ("01_prodcom_sa_plastic_film.csv", "SA Plastic Film\n(22292240)", COLORS["primary"]),
        ("02_prodcom_sa_paper.csv", "SA Paper\n(17127733)", COLORS["secondary"]),
        ("03_prodcom_sa_labels.csv", "SA Printed Labels\n(17291120)", COLORS["tertiary"]),
        ("04_prodcom_pet_film.csv", "PET Film\n(22213065)", COLORS["quaternary"]),
        ("05_prodcom_bopp_film.csv", "BOPP Film\n(22213021)", "#7C3AED"),
    ]

    # --- Left: Stacked area chart over time ---
    ax1 = axes[0]
    all_years = set()
    series_data = {}
    for filename, label, color in series_info:
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        eu_val = df[(df["reporter"] == "EU27_2020") & (df["indicators"] == "PRODVAL")]
        eu_val = eu_val.sort_values("TIME_PERIOD")
        if not eu_val.empty:
            series_data[label] = eu_val.set_index("TIME_PERIOD")["OBS_VALUE"]
            all_years.update(eu_val["TIME_PERIOD"].values)

    if series_data:
        combined = pd.DataFrame(series_data)
        combined = combined.sort_index()
        combined = combined.fillna(0)
        cumulative = combined.cumsum(axis=1)
        prev = None
        for (label, _color), col_name in zip(
            [(l, c) for _, l, c in series_info if l in combined.columns],
            [l for _, l, _ in series_info if l in combined.columns]
        ):
            current = cumulative[col_name]
            if prev is None:
                ax1.fill_between(combined.index, 0, current, alpha=0.7,
                                 color=_color, label=col_name)
            else:
                ax1.fill_between(combined.index, prev, current, alpha=0.7,
                                 color=_color, label=col_name)
            prev = current

        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_eur))
        ax1.legend(fontsize=7, loc="upper left")
        _add_covid_band(ax1, 0, prev.max() * 1.1)
    _style_ax(ax1, "EU27 Production Value — Stacked", "EUR")

    # --- Right: Latest year breakdown ---
    ax2 = axes[1]
    latest_vals = []
    labels = []
    colors = []
    for filename, label, color in series_info:
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        eu_val = df[(df["reporter"] == "EU27_2020") & (df["indicators"] == "PRODVAL")]
        if not eu_val.empty:
            latest = eu_val.sort_values("TIME_PERIOD").iloc[-1]["OBS_VALUE"]
            latest_vals.append(latest)
            labels.append(label)
            colors.append(color)

    if latest_vals:
        wedges, texts, autotexts = ax2.pie(
            latest_vals, labels=labels, colors=colors, autopct="%1.0f%%",
            startangle=90, textprops={"fontsize": 8},
        )
        for at in autotexts:
            at.set_fontsize(8)
            at.set_fontweight("bold")
        total = sum(latest_vals)
        ax2.set_title(f"Share of EU27 Production (Latest Year)\nTotal: EUR {_fmt_eur(total)}",
                      fontsize=11, fontweight="bold")

    fig.tight_layout()
    return _savefig(fig, "summary_market_sizing.png")


def plot_summary_trade_balance():
    """Generate trade balance summary comparing plastic vs paper PSA."""
    fig, ax = plt.subplots(figsize=(12, 6))

    trade_series = [
        ("06_trade_sa_plastic.csv", "SA Plastic (CN 39199080)", COLORS["primary"], COLORS["light_blue"]),
        ("07_trade_sa_paper.csv", "SA Paper (HS6 481141)", COLORS["secondary"], COLORS["light_red"]),
    ]

    for filename, label, exp_color, imp_color in trade_series:
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        val = df[df["indicators"] == "VALUE_IN_EUROS"]
        imports = val[val["flow"].astype(str) == "1"].groupby("TIME_PERIOD")["OBS_VALUE"].sum()
        exports = val[val["flow"].astype(str) == "2"].groupby("TIME_PERIOD")["OBS_VALUE"].sum()
        merged = pd.DataFrame({"imports": imports, "exports": exports}).dropna()
        merged["balance"] = merged["exports"] - merged["imports"]
        ax.plot(merged.index, merged["balance"] / 1e9, marker="o", markersize=5,
                linewidth=2, color=exp_color, label=f"{label} balance")
        ax.fill_between(merged.index, merged["balance"] / 1e9, alpha=0.15, color=exp_color)

    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.legend(fontsize=9)
    _style_ax(ax, "EU27 Trade Balance (Exports - Imports)\n(Sum of all member state reports — includes intra-EU)",
              "EUR Billion")
    ax.text(0.02, 0.02,
            "Note: Positive = net exporter. Values include intra-EU trade double counting.",
            transform=ax.transAxes, fontsize=7, color=COLORS["grey"], style="italic")

    fig.tight_layout()
    return _savefig(fig, "summary_trade_balance.png")


def plot_summary_price_vs_production():
    """Overlay production index vs price index to show margin squeeze."""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    geo_col = "geo\\TIME_PERIOD"

    # Production index
    path8 = os.path.join(OUTPUT_DIR, "08_sts_production_index.csv")
    path9 = os.path.join(OUTPUT_DIR, "09_sts_price_index.csv")
    if not os.path.exists(path8) or not os.path.exists(path9):
        print("  SKIP summary_price_vs_production.png: missing STS data")
        return None

    def _extract_annual(path, target_geo="EU27_2020"):
        df = pd.read_csv(path)
        row = df[df[geo_col] == target_geo]
        if row.empty:
            for fb in ["EA20", "EA21", "EA19"]:
                row = df[df[geo_col] == fb]
                if not row.empty:
                    break
        if row.empty:
            return pd.Series(dtype=float)
        val_cols = [c for c in df.columns if c.endswith("_value")]
        years = {}
        for c in val_cols:
            m = re.match(r"(\d{4})-(\d{2})_value", c)
            if m:
                v = row[c].values[0]
                if pd.notna(v):
                    try:
                        years.setdefault(int(m.group(1)), []).append(float(v))
                    except (ValueError, TypeError):
                        pass
        return pd.Series({yr: sum(vs) / len(vs) for yr, vs in years.items()}).sort_index()

    prod_idx = _extract_annual(path8)
    price_idx = _extract_annual(path9)

    if not prod_idx.empty:
        ax1.plot(prod_idx.index, prod_idx.values, marker="o", markersize=5,
                 linewidth=2.5, color=COLORS["primary"], label="Production Index (C2229)")
    ax1.set_ylabel("Production Index (2015=100)", color=COLORS["primary"], fontsize=10)
    ax1.tick_params(axis="y", labelcolor=COLORS["primary"])

    ax2 = ax1.twinx()
    if not price_idx.empty:
        ax2.plot(price_idx.index, price_idx.values, marker="s", markersize=5,
                 linewidth=2.5, color=COLORS["secondary"], label="Price Index — Adhesives (C2052)")
    ax2.set_ylabel("Price Index (2015=100)", color=COLORS["secondary"], fontsize=10)
    ax2.tick_params(axis="y", labelcolor=COLORS["secondary"])

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="upper left")

    ax1.axhline(y=100, color=COLORS["grey"], linewidth=0.5, linestyle="--", alpha=0.3)
    ax1.set_title("Production Volume vs Input Prices — Margin Squeeze Indicator",
                  fontsize=12, fontweight="bold", pad=15)
    ax1.set_xlabel("Year", fontsize=10)
    ax1.grid(True, alpha=0.2)
    ax1.spines["top"].set_visible(False)

    # COVID annotation
    ax1.axvspan(2019.8, 2020.5, alpha=0.08, color=COLORS["covid"], zorder=0)

    fig.tight_layout()
    return _savefig(fig, "summary_price_vs_production.png")


# =========================================================================
# Main
# =========================================================================

def generate_all_charts():
    """Generate all visualization PNGs."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)

    # Individual PRODCOM charts
    prodcom_series = [
        ("01_prodcom_sa_plastic_film.csv", "01_prodcom_sa_plastic_film.png",
         "Self-Adhesive Plastic Film — Wide Rolls (PRODCOM 22292240)"),
        ("02_prodcom_sa_paper.csv", "02_prodcom_sa_paper.png",
         "Self-Adhesive Paper & Paperboard (PRODCOM 17127733)"),
        ("03_prodcom_sa_labels.csv", "03_prodcom_sa_labels.png",
         "Self-Adhesive Printed Labels (PRODCOM 17291120)"),
        ("04_prodcom_pet_film.csv", "04_prodcom_pet_film.png",
         "PET Film <= 0.35mm (PRODCOM 22213065)"),
        ("05_prodcom_bopp_film.csv", "05_prodcom_bopp_film.png",
         "BOPP Film <= 0.10mm (PRODCOM 22213021)"),
    ]

    for csv_name, png_name, title in prodcom_series:
        path = os.path.join(OUTPUT_DIR, csv_name)
        if os.path.exists(path):
            plot_prodcom(path, png_name, title)
        else:
            print(f"  SKIP {png_name}: {csv_name} not found")

    # Trade charts
    trade_series = [
        ("06_trade_sa_plastic.csv", "06_trade_sa_plastic.png",
         "Self-Adhesive Plastic Trade (CN 39199080)"),
        ("07_trade_sa_paper.csv", "07_trade_sa_paper.png",
         "Self-Adhesive Paper Trade (HS6 481141)"),
    ]

    for csv_name, png_name, title in trade_series:
        path = os.path.join(OUTPUT_DIR, csv_name)
        if os.path.exists(path):
            plot_trade(path, png_name, title)
        else:
            print(f"  SKIP {png_name}: {csv_name} not found")

    # STS index charts
    sts_series = [
        ("08_sts_production_index.csv", "08_sts_production_index.png",
         "Industrial Production Index — Other Plastic Products (NACE C2229)"),
        ("09_sts_price_index.csv", "09_sts_price_index.png",
         "Producer Price Index — Adhesives (NACE C2052)"),
    ]

    for csv_name, png_name, title in sts_series:
        path = os.path.join(OUTPUT_DIR, csv_name)
        if os.path.exists(path):
            plot_sts_index(path, png_name, title)
        else:
            print(f"  SKIP {png_name}: {csv_name} not found")

    # SBS chart
    sbs_path = os.path.join(OUTPUT_DIR, "10_sbs_structure.csv")
    if os.path.exists(sbs_path):
        plot_sbs(sbs_path, "10_sbs_structure.png",
                 "Structural Business Statistics — Other Plastic Products (NACE C2229)")

    # Summary charts
    print("\n  --- Summary Charts ---")
    plot_summary_market_size()
    plot_summary_trade_balance()
    plot_summary_price_vs_production()

    print("\nAll charts saved to: " + OUTPUT_DIR)


if __name__ == "__main__":
    generate_all_charts()
