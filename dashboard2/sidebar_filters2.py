"""
Sidebar filters for Dashboard 2 — Application Categories.
Provides category + country filtering across all pages.
"""

import streamlit as st

from constants2 import (
    APP_CATEGORIES, CATEGORY_NAMES, EU27_CODES, COUNTRY_NAMES,
)


def render_category_filters(show_category: bool = True,
                             country_mode: str = "multi") -> dict:
    """
    Render sidebar filter widgets and return current selections.

    Returns dict with keys:
        category                 - selected category name or None
        category_production_nace - list of production NACE for category, or None
        category_retail_nace     - list of retail NACE for category, or None
        category_logistics_nace  - list of logistics NACE for category, or None
        countries                - list of selected country codes
        scope_code               - single country code or None
        scope_name               - human-readable scope label
    """
    result = {
        "category": None,
        "category_production_nace": None,
        "category_retail_nace": None,
        "category_logistics_nace": None,
        "countries": [],
        "scope_code": None,
        "scope_name": "",
    }

    with st.sidebar:
        st.divider()
        st.subheader("Filters")

        # ---- Category filter ----
        if show_category:
            cat_options = ["All Categories"] + [
                f"{name} \u2014 {APP_CATEGORIES[name]['description']}"
                for name in CATEGORY_NAMES
            ]
            selected_label = st.selectbox(
                "Application Category", cat_options, index=0,
                key="global_category",
                help=(
                    "Select an application category to filter all charts. "
                    "Categories map to specific industrial indicators (NACE codes)."
                ),
            )
            if selected_label != "All Categories":
                cat_name = selected_label.split(" \u2014 ")[0]
                info = APP_CATEGORIES[cat_name]
                result["category"] = cat_name
                result["category_production_nace"] = info["production_nace"] or None
                result["category_retail_nace"] = info["retail_nace"] or None
                result["category_logistics_nace"] = info["logistics_nace"] or None

        # ---- Country filter ----
        if country_mode == "single_country":
            if st.session_state.get("db2_country_single") not in EU27_CODES:
                st.session_state["db2_country_single"] = "DE"
            country_options_list = list(EU27_CODES)
            default_idx = country_options_list.index("DE") if "DE" in country_options_list else 0
            selected_code = st.selectbox(
                "Country", country_options_list, index=default_idx,
                format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
                key="db2_country_single",
            )
            result["scope_code"] = selected_code
            result["scope_name"] = COUNTRY_NAMES.get(selected_code, selected_code)
            result["countries"] = [selected_code]

        elif country_mode == "multi":
            default_countries = [c for c in ["DE", "FR", "IT", "ES", "PL"] if c in EU27_CODES]
            selected = st.multiselect(
                "Countries", EU27_CODES,
                default=default_countries[:5],
                format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
                key="db2_countries",
            )
            result["countries"] = selected
            result["scope_name"] = f"{len(selected)} countries" if selected else "No countries"

    return result
