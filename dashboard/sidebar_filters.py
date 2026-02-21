"""
Shared sidebar filters for the Eurostat Labels Market Dashboard.
Provides consistent sector + country filtering across all pages.
"""

import streamlit as st

from constants import (
    SECTOR_GROUPS, EU27_CODES, COUNTRY_NAMES, AGGREGATE_CODES,
)


def render_global_filters(show_sector: bool = True,
                          country_mode: str = "multi") -> dict:
    """
    Render sidebar filter widgets and return current selections.

    Parameters
    ----------
    show_sector : bool
        Whether to show the sector filter (False for Page 1).
    country_mode : str
        "multi"          – st.multiselect for multiple countries (Pages 2,3,4,6)
        "single"         – st.selectbox with EU27 Aggregate option (Page 1)
        "single_country" – st.selectbox, single country only, no aggregate (Page 5)
        "none"           – no country filter (Page 7)

    Returns
    -------
    dict with keys:
        sector          – selected sector name or None (when "All Sectors")
        sector_cn_codes – set of CN codes for the sector, or None (no filter)
        sector_nace_codes – set of NACE codes for the sector, or None (no filter)
        countries       – list of selected country codes
        is_aggregate    – True when EU27 Aggregate is selected (single mode)
        scope_code      – single country code or None
        scope_name      – human-readable scope label
    """
    result = {
        "sector": None,
        "sector_cn_codes": None,
        "sector_nace_codes": None,
        "countries": [],
        "is_aggregate": False,
        "scope_code": None,
        "scope_name": "",
    }

    with st.sidebar:
        st.divider()
        st.subheader("Filters")

        # ---- Sector filter ----
        if show_sector:
            sector_options = ["All Sectors"] + [
                f"{name} \u2014 {info['description']}"
                for name, info in SECTOR_GROUPS.items()
            ]
            selected_sector_label = st.selectbox(
                "Sector", sector_options, index=0, key="global_sector",
            )
            if selected_sector_label != "All Sectors":
                sector_name = selected_sector_label.split(" \u2014 ")[0]
                info = SECTOR_GROUPS[sector_name]
                result["sector"] = sector_name
                result["sector_cn_codes"] = set(info["cn_codes"])
                result["sector_nace_codes"] = set(info["nace_codes"])

        # ---- Country filter ----
        if country_mode == "single":
            # EU27 Aggregate + individual countries — use "EU27" sentinel
            country_options = ["EU27"] + list(EU27_CODES)

            def _fmt_single(c):
                if c == "EU27":
                    return "EU27 Aggregate"
                return f"{COUNTRY_NAMES.get(c, c)} ({c})"

            selected_code = st.selectbox(
                "Country", country_options, index=0,
                format_func=_fmt_single,
                key="global_country_single",
            )
            if selected_code == "EU27":
                result["is_aggregate"] = True
                result["scope_name"] = "EU27 Aggregate"
                result["scope_code"] = None
                result["countries"] = list(EU27_CODES)
            else:
                result["is_aggregate"] = False
                result["scope_code"] = selected_code
                result["scope_name"] = COUNTRY_NAMES.get(selected_code, selected_code)
                result["countries"] = [selected_code]

        elif country_mode == "single_country":
            # Single country only, no aggregate — same key, compatible options
            # If session state has "EU27" from a previous page, reset it
            if st.session_state.get("global_country_single") == "EU27":
                st.session_state["global_country_single"] = "DE"
            country_options_list = list(EU27_CODES)
            default_idx = country_options_list.index("DE") if "DE" in country_options_list else 0
            selected_code = st.selectbox(
                "Country", country_options_list, index=default_idx,
                format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
                key="global_country_single",
            )
            result["is_aggregate"] = False
            result["scope_code"] = selected_code
            result["scope_name"] = COUNTRY_NAMES.get(selected_code, selected_code)
            result["countries"] = [selected_code]

        elif country_mode == "multi":
            default_countries = [c for c in ["DE", "FR", "IT", "ES", "PL"] if c in EU27_CODES]
            selected = st.multiselect(
                "Countries", EU27_CODES,
                default=default_countries[:5],
                format_func=lambda x: f"{COUNTRY_NAMES.get(x, x)} ({x})",
                key="global_countries",
            )
            result["countries"] = selected
            result["scope_name"] = f"{len(selected)} countries" if selected else "No countries"

        # country_mode == "none" → no widget, countries stays []

    return result
