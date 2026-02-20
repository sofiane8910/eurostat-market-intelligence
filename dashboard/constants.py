"""
Constants, descriptions, and mappings for the Eurostat Labels Market Dashboard.
"""

# ---------------------------------------------------------------------------
# Country mappings
# ---------------------------------------------------------------------------

# Normalize EL (Eurostat STS convention) -> GR (ISO / Comext convention)
GEO_NORMALIZE = {"EL": "GR"}

EU27_CODES = sorted([
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES",
    "FI", "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK",
])

COUNTRY_NAMES = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "CY": "Cyprus",
    "CZ": "Czechia", "DE": "Germany", "DK": "Denmark", "EE": "Estonia",
    "ES": "Spain", "FI": "Finland", "FR": "France", "GR": "Greece",
    "HR": "Croatia", "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "MT": "Malta",
    "NL": "Netherlands", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
    "SE": "Sweden", "SI": "Slovenia", "SK": "Slovakia", "CN": "China",
}

# Aggregate geo codes (not individual countries)
AGGREGATE_CODES = {"EU27_2020", "EA19", "EA20", "EA21"}

# ---------------------------------------------------------------------------
# CN code descriptions — supply side
# ---------------------------------------------------------------------------

SUPPLY_CN_CODES = {
    "39191010": "SA plastic, rolls \u2264 20cm, width \u2264 20cm",
    "39191080": "SA plastic, rolls \u2264 20cm, other",
    "39199010": "SA plastic (excl. rolls \u2264 20cm), condensation polymerisation",
    "39199020": "SA plastic (excl. rolls \u2264 20cm), addition polymerisation",
    "39199080": "SA plastic (excl. rolls \u2264 20cm), other",
    "48114100": "Self-adhesive paper and paperboard",
    "48114900": "Gummed/adhesive paper & paperboard (excl. self-adhesive)",
    "48211010": "Self-adhesive printed labels, paper/paperboard",
    "48211090": "Other printed labels, paper/paperboard (excl. SA)",
    "48219010": "Self-adhesive labels, paper/paperboard (unprinted)",
    "48219090": "Other labels, paper/paperboard (unprinted, excl. SA)",
    "39201023": "PE film, low SG, thickness \u2264 0.025mm",
    "39201024": "PE film, low SG, thickness 0.025-0.05mm",
    "39201025": "PE film, low SG, thickness over 0.05mm",
    "39201028": "Other PE film, low SG",
    "39201040": "PE film, high SG, thickness under 0.021mm",
    "39201081": "PE film, high SG, thickness 0.021-0.160mm",
    "39201089": "Other PE film, high SG",
    "39202021": "BOPP film, thickness \u2264 0.10mm",
    "39202029": "Other PP film (cast/OPP), thickness \u2264 0.10mm",
    "39202080": "PP film, thickness over 0.10mm",
    "39204310": "Flexible PVC film (\u2265 6% plasticiser), not supported",
    "39204390": "Other flexible PVC film",
    "39204910": "Rigid PVC film, thickness over 1mm",
    "39204990": "Other rigid PVC film",
    "39206210": "PET film, thickness \u2264 0.025mm",
    "39206219": "PET film, thickness 0.025-0.35mm",
    "39206290": "PET film, thickness over 0.35mm",
    "39206100": "Polycarbonate film",
    "39206900": "Other polyester film (PEN, PBT, etc.)",
    "39209928": "Polyimide film",
    "39209959": "Other plastic film, n.e.c.",
    "35061000": "Adhesives, retail sale, \u2264 1kg",
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
}

# ---------------------------------------------------------------------------
# CN code descriptions — demand side
# ---------------------------------------------------------------------------

DEMAND_CN_CODES = {
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

# Combined
CN_DESCRIPTIONS = {**SUPPLY_CN_CODES, **DEMAND_CN_CODES}

# ---------------------------------------------------------------------------
# STS dataset descriptions
# ---------------------------------------------------------------------------

STS_DATASET_DESCRIPTIONS = {
    "sts_inpr_m": "Production in industry",
    "sts_intv_m": "Turnover in industry - total",
    "sts_intvd_m": "Turnover in industry - domestic",
    "sts_intvnd_m": "Turnover in industry - non-domestic",
    "sts_inpp_m": "Producer prices - total",
    "sts_inppd_m": "Producer prices - domestic",
    "sts_inppnd_m": "Producer prices - non-domestic",
    "sts_inpi_m": "Import prices in industry",
    "sts_ordi_m": "New orders in industry",
    "sts_inlb_m": "Labour input in industry",
    "ei_bssi_m_r2": "Industry confidence indicator",
    "sts_trtu_m": "Retail trade turnover",
    "sts_sepr_m": "Services production index",
    "ei_bsrt_m_r2": "Retail trade confidence indicator",
    "ei_bsse_m_r2": "Services confidence indicator",
}

# ---------------------------------------------------------------------------
# NACE descriptions
# ---------------------------------------------------------------------------

SUPPLY_NACE = {
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
}

DEMAND_NACE = {
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
    "G47_NFOOD": "Retail non-food products",
    "H": "Transportation and storage",
    "H49": "Land transport and pipelines",
    "H52": "Warehousing and transport support",
    "H53": "Postal and courier activities",
}

NACE_DESCRIPTIONS = {**SUPPLY_NACE, **DEMAND_NACE}

# ---------------------------------------------------------------------------
# Sector groups — link CN trade codes + NACE indices into coherent sectors
# ---------------------------------------------------------------------------

SECTOR_GROUPS = {
    "Paper & Board": {
        "cn_codes": ["48114100", "48114900", "48064010", "48064090"],
        "nace_codes": ["C17", "C171", "C1712", "C172", "C1729"],
        "description": "Self-adhesive paper, glassine, release liners",
    },
    "Labels": {
        "cn_codes": ["48211010", "48211090", "48219010", "48219090"],
        "nace_codes": ["C18"],
        "description": "Printed and unprinted labels (SA and non-SA)",
    },
    "Films & Plastics": {
        "cn_codes": [
            "39191010", "39191080", "39199010", "39199020", "39199080",
            "39201023", "39201024", "39201025", "39201028",
            "39201040", "39201081", "39201089",
            "39202021", "39202029", "39202080",
            "39204310", "39204390", "39204910", "39204990",
            "39206210", "39206219", "39206290",
            "39206100", "39206900", "39209928", "39209959",
        ],
        "nace_codes": ["C22", "C222", "C2221", "C2229"],
        "description": "PE, PP, PVC, PET, other plastic films and SA plastics",
    },
    "Adhesives & Chemicals": {
        "cn_codes": ["35061000", "35069110", "35069190", "35069900", "39100000"],
        "nace_codes": ["C20", "C203", "C2052"],
        "description": "Adhesives, silicones, chemical inputs",
    },
    "Inks & Foils": {
        "cn_codes": ["32151100", "32151900", "32159000", "32121000"],
        "nace_codes": ["C203"],
        "description": "Printing inks, stamping foils",
    },
    "RFID & Smart Cards": {
        "cn_codes": ["85235210", "85235910", "85235990"],
        "nace_codes": ["C2829"],
        "description": "RFID tags, smart cards, semiconductor media",
    },
    "Food & Beverages": {
        "cn_codes": ["1602", "1604", "2005", "2106", "2009", "2201", "2202", "2203", "2204", "2208"],
        "nace_codes": ["C10", "C11", "C12", "G47_FOOD", "G4711"],
        "description": "Processed food, beverages, food retail",
    },
    "HPC & Cosmetics": {
        "cn_codes": ["3304", "3305", "3307", "3402"],
        "nace_codes": ["C204", "G47_NF_HLTH"],
        "description": "Beauty, hair, cleaning products, cosmetics retail",
    },
    "Pharma": {
        "cn_codes": ["3004"],
        "nace_codes": ["C21"],
        "description": "Pharmaceutical products",
    },
    "Logistics": {
        "cn_codes": [],
        "nace_codes": ["H", "H49", "H52", "H53"],
        "description": "Transport, warehousing, postal services",
    },
}

# ---------------------------------------------------------------------------
# Freshness tiers — which datasets are Tier 1 (fast, ~3 week lag) vs Tier 2
# ---------------------------------------------------------------------------

TIER1_DATASETS = {
    "ei_bssi_m_r2", "ei_bsrt_m_r2", "ei_bsse_m_r2",  # confidence
    "sts_inpp_m", "sts_inppd_m", "sts_inppnd_m", "sts_inpi_m",  # prices
    "sts_inpr_m",  # production (some months)
}

# All other datasets are Tier 2 (~6-8 week lag)

# ---------------------------------------------------------------------------
# Comext flow labels
# ---------------------------------------------------------------------------

FLOW_LABELS = {"1": "Imports", "2": "Exports"}
INDICATOR_LABELS = {
    "VALUE_IN_EUROS": "Trade Value (EUR)",
    "QUANTITY_IN_100KG": "Trade Volume (100 kg)",
}


def freshness_footnote(tier: int, latest_date) -> str:
    """Return a plain-text footnote explaining data freshness."""
    if latest_date is None:
        return "No data available."
    date_str = latest_date.strftime("%B %Y") if hasattr(latest_date, "strftime") else str(latest_date)
    if tier == 1:
        return (f"Source: Eurostat | Data as of {date_str} | "
                "~3 week publication lag (survey-based / price indices)")
    return (f"Source: Eurostat | Data as of {date_str} | "
            "~6-8 week publication lag (hard economic data)")
