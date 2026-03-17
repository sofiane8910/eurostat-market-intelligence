"""
Constants, descriptions, and mappings for Dashboard 2 — Application Categories Deep Dive.

Imports shared geo constants from dashboard/constants.py and defines
the 10 application categories with business-friendly display names.
Production-side STS indices only (no Comext trade data).
"""

import sys
import os

# Import shared constants from dashboard/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard"))
from constants import (
    EU27_CODES,
    COUNTRY_NAMES,
    GEO_NORMALIZE,
    AGGREGATE_CODES,
    TIER1_DATASETS,
    freshness_footnote,
)

# ---------------------------------------------------------------------------
# Application categories — 10 end-market categories (NACE codes only)
# ---------------------------------------------------------------------------

APP_CATEGORIES = {
    "Food": {
        "production_nace": ["C10"],
        "retail_nace": ["G47_FOOD", "G4711"],
        "logistics_nace": [],
        "description": "Food product manufacturing and food retail",
    },
    "Beverage": {
        "production_nace": ["C11"],
        "retail_nace": ["G47_FOOD"],
        "logistics_nace": [],
        "description": "Beverage manufacturing and food/drink retail",
    },
    "Tobacco": {
        "production_nace": ["C12"],
        "retail_nace": [],
        "logistics_nace": [],
        "description": "Tobacco product manufacturing",
    },
    "Home & Personal Care": {
        "production_nace": ["C204"],
        "retail_nace": ["G47_NF_HLTH"],
        "logistics_nace": [],
        "description": "Soap, cosmetics, cleaning products manufacturing and retail",
    },
    "Pharmaceuticals": {
        "production_nace": ["C21"],
        "retail_nace": ["G47_NF_HLTH"],
        "logistics_nace": [],
        "description": "Pharmaceutical manufacturing and health retail",
    },
    "Retail": {
        "production_nace": [],
        "retail_nace": ["G47", "G47_FOOD", "G47_NF_HLTH", "G47_NFOOD_X_G473", "G4711"],
        "logistics_nace": [],
        "description": "Retail trade turnover across all channels",
    },
    "Transport & Logistics": {
        "production_nace": [],
        "retail_nace": [],
        "logistics_nace": ["H", "H49", "H52", "H53"],
        "description": "Transport, warehousing, postal & courier services",
    },
    "Industrial Chemicals": {
        "production_nace": ["C20"],
        "retail_nace": [],
        "logistics_nace": [],
        "description": "Chemicals and chemical products manufacturing",
    },
    "Office Products": {
        "production_nace": ["C17"],
        "retail_nace": [],
        "logistics_nace": [],
        "description": "Paper products manufacturing (proxy for office labelling)",
    },
    "Consumer Durables": {
        "production_nace": ["C27"],
        "retail_nace": [],
        "logistics_nace": [],
        "description": "Electrical equipment manufacturing (proxy for appliance labels)",
    },
    "Automotive": {
        "production_nace": ["C29"],
        "retail_nace": [],
        "logistics_nace": [],
        "description": "Motor vehicle manufacturing (proxy for automotive labels)",
    },
}

# Category names as ordered list
CATEGORY_NAMES = list(APP_CATEGORIES.keys())

# ---------------------------------------------------------------------------
# Business-friendly display names
# ---------------------------------------------------------------------------

# STS dataset display names (no technical codes in UI)
DATASET_DISPLAY_NAMES = {
    "sts_inpr_m": "Production Volume",
    "sts_intv_m": "Total Turnover",
    "sts_intvd_m": "Domestic Turnover",
    "sts_intvnd_m": "Export Turnover",
    "sts_inpp_m": "Producer Prices",
    "sts_inppd_m": "Domestic Prices",
    "sts_inppnd_m": "Export Prices",
    "sts_inpi_m": "Import Prices",
    "sts_inlb_m": "Labour Input",
    "ei_bssi_m_r2": "Industry Confidence",
    "sts_trtu_m": "Retail Turnover",
    "sts_sepr_m": "Services Production",
    "ei_bsrt_m_r2": "Retail Confidence",
    "ei_bsse_m_r2": "Services Confidence",
}

# STS full descriptions (for captions/footnotes)
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

# NACE display names (business-friendly)
NACE_DISPLAY_NAMES = {
    "C10": "Food Manufacturing",
    "C11": "Beverage Manufacturing",
    "C12": "Tobacco Manufacturing",
    "C17": "Paper Products",
    "C20": "Chemicals",
    "C204": "Soap & Cosmetics",
    "C21": "Pharmaceuticals",
    "C27": "Electrical Equipment",
    "C29": "Motor Vehicles",
    # Retail
    "G47": "Total Retail",
    "G47_FOOD": "Food & Beverage Retail",
    "G47_NF_HLTH": "Health & Cosmetics Retail",
    "G47_NFOOD_X_G473": "Non-Food Retail",
    "G4711": "Supermarkets",
    "G47_NFOOD": "Non-Food Retail Products",
    # Logistics
    "H": "Transport & Storage (total)",
    "H49": "Land Transport",
    "H52": "Warehousing",
    "H53": "Postal & Courier",
}

# NACE full descriptions (for captions)
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

# ---------------------------------------------------------------------------
# Series definitions — plain-language explanations for every indicator
# ---------------------------------------------------------------------------

DATASET_DEFINITIONS = {
    "sts_inpr_m": (
        "**Production Volume** measures the physical output of a manufacturing sector, "
        "stripped of price effects. It tracks how many goods factories actually produce "
        "each month, indexed to a base year (2021 = 100). A value of 105 means output "
        "is 5% higher than the 2021 monthly average."
    ),
    "sts_intv_m": (
        "**Total Turnover** is the total revenue (sales) earned by businesses in a sector, "
        "including both domestic sales and exports. It reflects both volume and price changes. "
        "Unlike Production Volume, turnover rises when prices increase even if output stays flat. "
        "Indexed to 2021 = 100."
    ),
    "sts_intvd_m": (
        "**Domestic Turnover** is the share of total revenue from sales within the home country. "
        "Comparing domestic vs. export turnover reveals whether growth is driven by local demand "
        "or foreign buyers. Indexed to 2021 = 100."
    ),
    "sts_intvnd_m": (
        "**Export Turnover** is the share of total revenue from sales to foreign markets. "
        "A rising export turnover with flat domestic turnover signals growing international "
        "competitiveness. Indexed to 2021 = 100."
    ),
    "sts_inpp_m": (
        "**Producer Prices** (total) track the average selling prices received by manufacturers "
        "at the factory gate, covering both domestic and export sales. This is an early inflation "
        "signal \u2014 rising producer prices often feed through to consumer prices. Indexed to 2021 = 100."
    ),
    "sts_inppd_m": (
        "**Domestic Prices** track factory-gate selling prices for goods sold within the home "
        "country only. Comparing domestic vs. export prices reveals pricing strategies \u2014 "
        "e.g., whether manufacturers charge more abroad. Indexed to 2021 = 100."
    ),
    "sts_inppnd_m": (
        "**Export Prices** track factory-gate selling prices for goods sold to foreign markets. "
        "These can diverge from domestic prices due to exchange rates, tariffs, or competitive "
        "pressure in export markets. Indexed to 2021 = 100."
    ),
    "sts_inpi_m": (
        "**Import Prices** track the cost of goods imported into the country for industrial use. "
        "Rising import prices signal supply-chain cost pressure \u2014 especially relevant for sectors "
        "reliant on imported raw materials or components. Indexed to 2021 = 100."
    ),
    "sts_inlb_m": (
        "**Labour Input** measures the total hours worked by employees in a sector. "
        "It reflects hiring, overtime, and working-time changes. A drop in labour input "
        "alongside stable production suggests productivity gains; a drop with falling "
        "production signals contraction. Indexed to 2021 = 100."
    ),
    "ei_bssi_m_r2": (
        "**Industry Confidence** is a survey-based indicator where manufacturing managers "
        "report their expectations for production, order books, and finished-goods stocks. "
        "The balance is in percentage points (pp): positive = more optimistic than pessimistic "
        "managers, negative = more pessimistic. It is a leading indicator \u2014 confidence drops "
        "typically precede output declines by 1\u20132 months."
    ),
    "sts_trtu_m": (
        "**Retail Turnover** measures the total sales value of retail businesses. "
        "It captures consumer spending patterns in shops and online stores. "
        "The index is deflated (volume-adjusted) and set to 2021 = 100, "
        "so changes reflect real spending changes, not just price inflation."
    ),
    "sts_sepr_m": (
        "**Services Production** measures the output volume of service-sector industries "
        "(transport, warehousing, postal). It tracks the physical activity of the logistics "
        "chain \u2014 how many goods are shipped, stored, and delivered. Indexed to 2021 = 100."
    ),
    "ei_bsrt_m_r2": (
        "**Retail Confidence** is a survey of retail managers on their recent business situation, "
        "stock levels, and expected orders. The balance is in percentage points (pp): "
        "positive = more optimistic, negative = more pessimistic. "
        "It is a leading indicator for consumer spending trends."
    ),
    "ei_bsse_m_r2": (
        "**Services Confidence** is a survey of services-sector managers covering business "
        "climate, demand expectations, and employment plans. The balance is in percentage "
        "points (pp). Positive values signal expanding services activity; negative values "
        "signal contraction. Closely watched for logistics and transport outlook."
    ),
}

# Tab-level definitions (shown as intro notes on each tab)
TAB_DEFINITIONS = {
    "output_turnover": (
        "**What are Output & Turnover?**\n\n"
        "- **Production Volume** = physical output (how much is made), price effects removed\n"
        "- **Total Turnover** = total sales revenue (volume x price)\n"
        "- **Domestic Turnover** = revenue from home-market sales only\n"
        "- **Export Turnover** = revenue from sales to foreign markets\n\n"
        "All are monthly indices with base year 2021 = 100. "
        "A value of 110 means the indicator is 10% above its 2021 average."
    ),
    "prices": (
        "**What are Price Indices?**\n\n"
        "- **Producer Prices** = average factory-gate selling prices (what manufacturers charge)\n"
        "- **Domestic Prices** = selling prices for goods sold within the country\n"
        "- **Export Prices** = selling prices for goods sold abroad\n"
        "- **Import Prices** = cost of imported goods used in production\n\n"
        "All are monthly indices with base year 2021 = 100. "
        "Rising producer prices are an early signal of inflation passing through the supply chain."
    ),
    "labour_confidence": (
        "**What are Labour Input & Confidence?**\n\n"
        "- **Labour Input** = total hours worked by employees in the sector (index, 2021 = 100)\n"
        "- **Industry Confidence** = survey of manufacturing managers on production expectations, "
        "order books, and stock levels (balance in percentage points)\n\n"
        "Confidence is a *leading* indicator: drops typically precede production declines "
        "by 1\u20132 months. Labour input is a *coincident* indicator that moves with the cycle."
    ),
    "retail": (
        "**What are Retail indicators?**\n\n"
        "- **Retail Turnover** = total sales value of retail businesses, deflated to remove "
        "price effects (volume index, 2021 = 100)\n"
        "- **Retail Confidence** = survey of retail managers (balance in percentage points: "
        "positive = optimistic, negative = pessimistic)\n\n"
        "These indicators show how much consumers are buying in shops and online. "
        "Different NACE breakdowns (Food, Health, Non-Food) reveal which product categories drive spending."
    ),
    "logistics": (
        "**What are Logistics & Services indicators?**\n\n"
        "- **Services Production** = output volume of transport, warehousing, and postal services "
        "(index, 2021 = 100)\n"
        "- **Services Confidence** = survey of services managers on business outlook "
        "(balance in percentage points)\n\n"
        "Logistics indices track the physical movement of goods through the supply chain. "
        "A decline in transport/warehousing activity often signals weakening manufacturing demand."
    ),
}

# ---------------------------------------------------------------------------
# Production vs Demand dataset groups
# ---------------------------------------------------------------------------

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

DEMAND_STS_DATASETS = {
    "sts_trtu_m": ["G47", "G47_FOOD", "G47_NF_HLTH", "G47_NFOOD_X_G473", "G4711"],
    "sts_sepr_m": ["H", "H49", "H52", "H53"],
    "ei_bsrt_m_r2": ["G47_FOOD", "G47_NFOOD"],
    "ei_bsse_m_r2": ["H"],
}

# Production tab groupings
PRODUCTION_TAB_OUTPUT = ["sts_inpr_m", "sts_intv_m", "sts_intvd_m", "sts_intvnd_m"]
PRODUCTION_TAB_PRICES = ["sts_inpp_m", "sts_inppd_m", "sts_inppnd_m", "sts_inpi_m"]
PRODUCTION_TAB_LABOUR = ["sts_inlb_m", "ei_bssi_m_r2"]

# All production NACE codes
PRODUCTION_NACE = ["C10", "C11", "C12", "C204", "C21", "C20", "C17", "C27", "C29"]

# ---------------------------------------------------------------------------
# Utility lookups
# ---------------------------------------------------------------------------

def get_category_for_nace(nace: str) -> str:
    """Return the application category for a NACE code."""
    for cat, info in APP_CATEGORIES.items():
        if nace in info["production_nace"] + info["retail_nace"] + info["logistics_nace"]:
            return cat
    return ""


def get_all_nace_for_category(cat_name: str) -> list:
    """Return all NACE codes (production + retail + logistics) for a category."""
    info = APP_CATEGORIES.get(cat_name, {})
    return info.get("production_nace", []) + info.get("retail_nace", []) + info.get("logistics_nace", [])


# ---------------------------------------------------------------------------
# Market Proxy — yfinance company registry (28 tickers)
# ---------------------------------------------------------------------------

MARKET_PROXY_TICKERS = {
    "Food": [
        {"ticker": "NESN.SW", "company": "Nestlé", "country": "Switzerland"},
        {"ticker": "BN.PA", "company": "Danone", "country": "France"},
        {"ticker": "ABF.L", "company": "Assoc British Foods", "country": "UK"},
        {"ticker": "ORK.OL", "company": "Orkla", "country": "Norway"},
    ],
    "Beverage": [
        {"ticker": "ABI.BR", "company": "AB InBev", "country": "Belgium"},
        {"ticker": "HEIA.AS", "company": "Heineken", "country": "Netherlands"},
        {"ticker": "DGE.L", "company": "Diageo", "country": "UK"},
        {"ticker": "CCH.L", "company": "Coca-Cola HBC", "country": "UK"},
    ],
    "Tobacco": [
        {"ticker": "BATS.L", "company": "BAT", "country": "UK"},
        {"ticker": "IMB.L", "company": "Imperial Brands", "country": "UK"},
    ],
    "Home & Personal Care": [
        {"ticker": "ULVR.L", "company": "Unilever", "country": "UK"},
        {"ticker": "OR.PA", "company": "L'Oréal", "country": "France"},
        {"ticker": "HEN3.DE", "company": "Henkel", "country": "Germany"},
        {"ticker": "BEI.DE", "company": "Beiersdorf", "country": "Germany"},
    ],
    "Pharmaceuticals": [
        {"ticker": "NOVN.SW", "company": "Novartis", "country": "Switzerland"},
        {"ticker": "ROG.SW", "company": "Roche", "country": "Switzerland"},
        {"ticker": "SAN.PA", "company": "Sanofi", "country": "France"},
        {"ticker": "NOVO-B.CO", "company": "Novo Nordisk", "country": "Denmark"},
    ],
    "Retail": [
        {"ticker": "TSCO.L", "company": "Tesco", "country": "UK"},
        {"ticker": "CA.PA", "company": "Carrefour", "country": "France"},
        {"ticker": "AD.AS", "company": "Ahold Delhaize", "country": "Netherlands"},
        {"ticker": "JMT.LS", "company": "Jerónimo Martins", "country": "Portugal"},
    ],
    "Transport & Logistics": [
        {"ticker": "DHL.DE", "company": "DHL Group", "country": "Germany"},
        {"ticker": "DSV.CO", "company": "DSV", "country": "Denmark"},
        {"ticker": "MAERSK-B.CO", "company": "Maersk", "country": "Denmark"},
        {"ticker": "KNIN.SW", "company": "Kuehne+Nagel", "country": "Switzerland"},
    ],
}

# Financial metrics to extract and display
PROXY_FINANCIAL_METRICS = ["Total Revenue", "EBITDA", "Net Income"]

PROXY_METRIC_DISPLAY = {
    "Total Revenue": "Revenue",
    "EBITDA": "EBITDA",
    "Net Income": "Net Income",
}
