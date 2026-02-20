# Eurostat Labels Market Dashboard — Implementation Plan

## Overview

Build an interactive Streamlit dashboard to showcase 214+ Eurostat series covering the European labels market (supply + demand side). Includes bilateral EU trade + China competition analysis and data freshness tracking.

**4 Milestones** — execute sequentially.

---

## Milestone 1: Comext Bilateral Extraction Rework

### Goal
Change Comext extraction from `partner=WORLD` (aggregate only) to `partner=WORLD+EU27+CN` (bilateral trade with every EU country + China).

### File: `test_eurostat_extraction.py`

**Change 1** — Add partner configuration (after line ~51):
```python
COMEXT_PARTNERS = "+".join(["WORLD"] + EU27_ISO + ["CN"])
# Result: "WORLD+AT+BE+BG+CY+CZ+DE+DK+EE+ES+FI+FR+GR+HR+HU+IE+IT+LT+LU+LV+MT+NL+PL+PT+RO+SE+SI+SK+CN"
```

**Change 2** — Update `extract_comext_monthly()` URL (line ~283):
```python
# FROM:
f"M.{reporters}.WORLD.{cn_code}.{flows}.{indicators}"
# TO:
f"M.{reporters}.{COMEXT_PARTNERS}.{cn_code}.{flows}.{indicators}"
```
Same change for HS6 fallback URL (line ~301).

**Change 3** — Update totals print (line ~471) to mention bilateral partners.

### Data Impact
- Still 56 API calls (one per CN code), same CN codes
- Each CSV now contains ~29x more rows (27 EU partners + WORLD + CN)
- `partner` column: `WORLD, AT, BE, BG, ..., SK, CN`
- Estimated file sizes: ~5-10MB per CSV (~300-500MB total vs ~48MB currently)

### Verification
```bash
cd ~/Desktop/Work/eurostat && source .venv/bin/activate && python test_eurostat_extraction.py
# Then check:
python3 -c "
import pandas as pd
df = pd.read_csv('output/comext/CN_3920.csv')
print('Partners:', df['partner'].unique())
print('CN rows:', len(df[df['partner']=='CN']))
"
```

---

## Milestone 2: Dashboard Foundation

### Goal
Install dependencies and create the data layer + chart utilities.

### Step 1: Install dependencies
```bash
cd ~/Desktop/Work/eurostat && source .venv/bin/activate
pip install streamlit plotly
```

### Step 2: Create `dashboard/constants.py`

All reference data in one place:

| Constant | Purpose |
|----------|---------|
| `COUNTRY_MAP` | EL->GR normalization + ISO->full names (AT->"Austria") |
| `EU27_CODES` | 27 member state ISO codes |
| `AGGREGATE_CODES` | `["EU27_2020", "EA19", "EA20", "EA21"]` |
| `SUPPLY_CN_CODES` | Supply-side CN codes with descriptions |
| `DEMAND_CN_CODES` | Demand-side CN codes with descriptions |
| `SUPPLY_NACE` | Supply NACE codes: C17, C171, C1712, C172, C1729, C2013, etc. |
| `DEMAND_NACE` | Demand NACE codes: C10, C11, C12, C204, C21 |
| `STS_DATASET_DESCRIPTIONS` | Dataset code -> human name |
| `NACE_DESCRIPTIONS` | NACE code -> human name |
| `CN_DESCRIPTIONS` | CN code -> human name |
| `SECTOR_GROUPS` | Sector -> {cn_codes, nace_codes} mapping (see below) |
| `FRESHNESS_TIERS` | Series categorization by data lag |

**Sector Groups:**
- "Paper & Board" -> CN 4811/4821 + NACE C17/C171/C172
- "Films & Plastics" -> CN 3919/3920/3921 + NACE C222/C2222/C2229
- "Adhesives & Chemicals" -> CN 3506/3100 + NACE C2013/C2016/C2041/C2059
- "Inks & Foils" -> CN 3208/3215/3212 + NACE C2030
- "Printing & Packaging Machinery" -> CN 8443/8523 + NACE C2821
- "Food & Beverages" -> CN 1602/1604/2005/2106/2009/2201-2208 + NACE C10/C11/G47_FOOD
- "HPC & Cosmetics" -> CN 3304/3305/3307/3402 + NACE C204/G47_NF_HLTH
- "Pharma" -> CN 3004 + NACE C21
- "Logistics" -> NACE H/H49/H52/H53

**Freshness Tiers:**
- Tier 1 (~3 week lag): ei_bssi, ei_bsrt, ei_bsse, sts_inpp, sts_inpr — have 2026-01 data
- Tier 2 (~6-8 week lag): everything else — latest is Dec 2025 or Nov 2025

### Step 3: Create `dashboard/data_loader.py`

```python
@st.cache_data
def load_all_data():
    """Load all 270+ CSVs, normalize, compute freshness."""
    ...
```

Key functions:
- `load_comext_file(path)` -> DataFrame: `country, partner, flow, indicator, date, value`
  - Multiple partners now (WORLD, EU countries, CN)
  - Normalize country codes via COUNTRY_MAP
- `load_sts_file(path)` -> DataFrame: `country, date, value`
  - Auto-detect meta cols (4/5/6) by finding `geo\TIME_PERIOD` column
  - Take first row per geo (preferred SCA/I21 combo from existing `_clean_sts_df`)
  - Melt wide->long, normalize EL->GR
- `compute_freshness(df)` -> `{latest_date, tier, lag_days}`
- Returns dict: `{comext: {cn_code: df}, sts: {key: df}, freshness: {key: info}}`

### Step 4: Create `dashboard/charts.py`

8 reusable Plotly chart builders:
1. `line_chart(df, countries, title)` — multi-country time series
2. `bar_chart_latest(df, countries, title)` — latest month bar by country
3. `heatmap_yoy(df, countries, title)` — YoY% heatmap (country x month)
4. `sparkline(values)` — inline sparkline for KPI cards
5. `trade_balance_chart(imports_df, exports_df, title)` — stacked import/export + net balance line
6. `china_share_chart(world_df, china_df, countries, title)` — China % of total trade
7. `bilateral_flow_chart(df, reporter, title)` — trade partner breakdown (bar or sankey)
8. `freshness_badge(tier, latest_date)` — colored HTML badge (green/orange/red)

### Step 5: Create `dashboard/app.py`

Entry point:
```python
import streamlit as st
st.set_page_config(page_title="Eurostat Labels Market", layout="wide", page_icon="📊")
```
- Sidebar: data freshness summary, series counts
- Load data once into session_state

### Verification
```bash
cd ~/Desktop/Work/eurostat && source .venv/bin/activate
streamlit run dashboard/app.py
# Should launch with sidebar, no pages yet
```

---

## Milestone 3: Core Dashboard Pages (1-4)

### Page 1: Executive Summary (`pages/1_Executive_Summary.py`)

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ 🟢 Tier 1 data: Jan 2026 │ 🟠 Tier 2 data: Dec 2025   │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Industry │ Productn │ EU Trade │ Retail   │ China       │
│ Confid.  │ Index    │ Balance  │ Turnover │ Import Δ    │
│ -3.2 🟢  │ 102.4 🟠 │ +€2.1B🟠 │ 108.3 🟠 │ +5.2% 🟠   │
│ ▲ +0.5   │ ▼ -1.2%  │ ▼ -3.4%  │ ▲ +1.1%  │ ▲ +2.1pp   │
├──────────┴──────────┴──────────┴──────────┴─────────────┤
│ Supply Side              │ Demand Side                   │
│ ├─ Paper prod:  ↗ +2.1%  │ ├─ Food prod:   ↗ +1.3%     │
│ ├─ Film prod:   ↘ -0.8%  │ ├─ Bev prod:    → +0.1%     │
│ ├─ Adhesive:    ↗ +1.5%  │ ├─ HPC prod:    ↗ +2.4%     │
│ ├─ Ink prices:  ↘ -1.2%  │ ├─ Pharma:      ↗ +3.1%     │
│ └─ SA Film imp: ↗ +3.4%  │ └─ Retail food: ↗ +0.9%     │
└──────────────────────────┴───────────────────────────────┘
```

### Page 2: Supply Side (`pages/2_Supply_Side.py`)

Three tabs:
- **Trade**: CN code selector (grouped: Plastics, Paper, Labels, Films, Adhesives, Inks, RFID)
  - Line chart: EU27 imports + exports over time (partner=WORLD)
  - Bar chart: top 10 importing countries (latest month)
  - Toggle: value (EUR) vs volume (100KG)
- **Industrial Indices**: Dataset selector (production, turnover, prices, labour cost) + NACE selector
  - Line chart: selected countries over time
  - Heatmap: YoY% change by country x month
- **Confidence**: Industry confidence (ei_bssi) for supply NACE codes
  - Multi-country line chart
- Filters sidebar: country multi-select, date range slider

### Page 3: Demand Side (`pages/3_Demand_Side.py`)

Three tabs:
- **End-Market Trade**: Sector selector (Food, Beverages, HPC, Pharma)
  - Same layout as Supply Trade but for demand CN codes
- **Retail**: sts_trtu_m for G47 codes + ei_bsrt_m_r2 confidence
  - Line chart by country, bar chart of latest values
- **Logistics**: sts_sepr_m for H codes + ei_bsse_m_r2 confidence
  - Same layout

### Page 4: Trade Balance & China (`pages/4_Trade_Balance_China.py`)

**The key page for China competition:**

Sections:
1. **EU27 vs China Overview**
   - Line chart: total EU27 imports from WORLD vs from CN, over time
   - All CN codes combined (sum of VALUE_IN_EUROS where flow=Import)

2. **China Import Share by Product**
   - Horizontal bar chart: % of EU imports from China for each CN code
   - Sorted by share, grouped by sector
   - Color: red if >50%, orange if >25%, green if <10%

3. **Country Exposure to China**
   - Select a CN code -> stacked bar: China imports vs Rest-of-World per EU country
   - Which countries are most dependent on Chinese imports?

4. **Intra-EU vs Extra-EU Trade**
   - For selected CN code: how much is traded within EU vs imported from China?
   - Helps identify where EU self-sufficiency exists

5. **Trade Balance by Country**
   - Select CN code -> net position (exports - imports) per EU country
   - With WORLD partner and with CN partner separately

6. **China Trend**
   - YoY% change in China imports per CN code
   - Is China's share growing or shrinking?

7. **Auto-Generated Storyline**
   - Text callouts: "China accounts for X% of EU [product] imports, [up/down] Y% YoY"
   - Highlight top 3 products where China share is growing fastest

### Verification
```bash
streamlit run dashboard/app.py
# Navigate to each page, verify charts render
# Check China page shows bilateral data
```

---

## Milestone 4: Deep Dive Pages (5-7) + Fixes

### Page 5: Country Deep Dive (`pages/5_Country_Deep_Dive.py`)

- Country selector (27 EU members)
- For selected country, 5 tabs:
  - **Supply Trade**: imports/exports for supply CN codes (WORLD + China breakdown)
  - **Demand Trade**: imports/exports for demand CN codes (WORLD + China breakdown)
  - **Supply Indices**: production, prices, confidence for supply NACE codes
  - **Demand Indices**: food/bev/HPC/pharma production, retail, logistics
  - **Trade Partners**: who does this country trade with most? (intra-EU breakdown)

### Page 6: Sector Explorer (`pages/6_Sector_Explorer.py`)

- Sector selector from SECTOR_GROUPS
- For selected sector:
  - Combined view: trade + production indices side by side
  - Country ranking: bar chart of latest values across 27 countries
  - Cross-indicator: e.g., food production (C10) vs food retail (G47_FOOD)
  - China impact: China import share for the sector's CN codes

### Page 7: Data Freshness (`pages/7_Data_Freshness.py`)

- Full table: series name | latest date | lag (days) | tier | status badge
- Color: green=current month, orange=1 month lag, red=2+ months
- Grouped by: Comext | STS Supply | STS Demand | STS Retail/Logistics
- Explanation of tier logic and why different series have different lags

### Fix: `visualize.py`

Change STS regex from `((?:C|G|H)\w+)` to `((?:C|G|H)\w*)` to match bare "H" in `ei_bsse_m_r2_H.csv` and `sts_sepr_m_H.csv`. Appears twice in the file (line ~400 and ~436).

### Final Verification
```bash
cd ~/Desktop/Work/eurostat && source .venv/bin/activate
streamlit run dashboard/app.py
# Test all 7 pages
# Test country selector (27 countries)
# Test sector selector (9 sectors)
# Test China page with different CN codes
# Verify freshness badges throughout
```
