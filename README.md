# Eurostat Market Intelligence — PSA & Labels Industry

Automated monthly data extraction from Eurostat for the European pressure-sensitive adhesive (PSA) materials, labels, release liners, films, and converting industry — covering both **supply-side** (raw materials, converting) and **demand-side** (end-market sectors that consume labels).

**Frequency**: Monthly (all series)
**Time range**: 2023-01 to 2026-12
**Sources**: Eurostat Comext (DS-045409) and Short-Term Statistics (STS)

---

## Output Structure

```
output/
├── quality_report.md          # Quality assessment for all series
├── comext/                    # Trade data (CSV + PNG per CN code)
│   ├── CN_39191080.csv
│   ├── CN_39191080.png
│   └── ...
└── sts/                       # Industry indices (CSV + PNG per dataset x NACE)
    ├── sts_inpr_m_C2229.csv
    ├── sts_inpr_m_C2229.png
    ├── sts_trtu_m_G47_FOOD.csv
    ├── sts_trtu_m_G47_FOOD.png
    └── ...
```

---

## Usage

```bash
source .venv/bin/activate

# Run extraction + visualization (~15-20 minutes)
python test_eurostat_extraction.py

# Or generate charts only (from existing CSVs)
python visualize.py
```

---

## Supply-Side: Comext Trade Series (41 CN codes)

**Dataset**: DS-045409
**Granularity**: Monthly, by EU27 member state as reporter
**Partner**: WORLD aggregate (no individual partner country breakdown)
**Indicators**: VALUE_IN_EUROS, QUANTITY_IN_100KG

> The Comext API supports partner-country breakdowns (e.g. by CN, US, JP) but the current extraction uses WORLD aggregate only. To add bilateral trade data, modify the `WORLD` parameter in `test_eurostat_extraction.py`.

### B1: Self-Adhesive Plastics (HS 3919)

| CN Code | Description |
|---|---|
| 39191080 | SA plastic strips in rolls <= 20cm wide, other |
| 39199020 | SA plastic sheets/films (excl. rolls <= 20cm), addition polymerisation — PE, PP, PVC-based labelstock |
| 39199080 | SA plastic sheets/films (excl. rolls <= 20cm), other — catch-all for PSA labelstock |

### B2: Self-Adhesive Paper & Paperboard (HS 4811)

| CN Code | Description |
|---|---|
| 48114100 | Self-adhesive paper and paperboard — paper PSA labelstock (face + adhesive + liner) |
| 48114900 | Gummed/adhesive paper & paperboard (excl. self-adhesive) — competing wet-gummed technology |

### B3: Labels of Paper & Paperboard (HS 4821)

| CN Code | Description |
|---|---|
| 48211010 | Self-adhesive printed labels of paper/paperboard — finished converted PSA labels |
| 48211090 | Other printed labels of paper/paperboard (excl. SA) — wet-glue, shrink sleeve labels |
| 48219010 | Self-adhesive labels, paper/paperboard (unprinted) — blank thermal/shipping labels |
| 48219090 | Other labels, paper/paperboard (unprinted, excl. SA) — blank non-PSA labels |

### B4.1: PE Films (HS 3920.10)

| CN Code | Description |
|---|---|
| 39201023 | PE film, SG < 0.94, thickness <= 0.025mm — thin LDPE/LLDPE films |
| 39201024 | PE film, SG < 0.94, thickness 0.025-0.05mm — medium LDPE films |
| 39201025 | PE film, SG < 0.94, thickness > 0.05mm — thicker LDPE films, label face stock gauge |
| 39201028 | Other PE film, SG < 0.94 — other LDPE/LLDPE films |
| 39201040 | PE film, SG >= 0.94, thickness < 0.021mm — thin HDPE films |
| 39201081 | PE film, SG >= 0.94, thickness 0.021-0.160mm — standard HDPE films |
| 39201089 | Other PE film, SG >= 0.94 — other HDPE films |

### B4.2: PP Films (HS 3920.20)

| CN Code | Description |
|---|---|
| 39202021 | BOPP film, thickness <= 0.10mm — the #1 filmic label face stock material |
| 39202029 | Other PP film (cast/OPP), thickness <= 0.10mm — cast PP for wrap-around labels |
| 39202080 | PP film, thickness > 0.10mm — thicker PP films for heavy-duty applications |

### B4.3: PVC Films (HS 3920.43/49)

| CN Code | Description |
|---|---|
| 39204310 | Flexible PVC film (>= 6% plasticiser), not supported — conformable label/graphic film |
| 39204390 | Other flexible PVC film |
| 39204910 | Rigid PVC film, thickness > 1mm — thick rigid PVC for blister packaging |
| 39204990 | Other rigid PVC film — thin rigid PVC |

### B4.4: PET Films (HS 3920.62)

| CN Code | Description |
|---|---|
| 39206219 | PET film, thickness 0.025-0.35mm — standard PET for label face stocks and release liners |
| 39206290 | PET film, thickness > 0.35mm — heavy PET sheets for industrial labels |

### B4.5: Other Films

| CN Code | Description |
|---|---|
| 39206100 | Polycarbonate film — durable label substrates for harsh environments |
| 39206900 | Other polyester film (PEN, PBT, etc.) — specialty high-performance label substrates |
| 39209928 | Polyimide film — high-temperature labels for electronics and automotive |
| 39209959 | Other plastic film, n.e.c. — catch-all including bio-based and TPU films |

### B5: Adhesives (HS 3506)

| CN Code | Description |
|---|---|
| 35061000 | Adhesives, retail sale, net weight <= 1kg — small-format retail adhesives |
| 35069110 | Water-based adhesives from synthetic polymers — water-based PSA emulsions, PVAc |
| 35069190 | Other adhesives based on synthetic polymers or rubber — solvent-based PSA, hot-melt, UV-curable |
| 35069900 | Other prepared glues/adhesives, n.e.c. — other industrial adhesives |

### B6: Silicones (HS 3910)

| CN Code | Description |
|---|---|
| 39100000 | Silicones in primary forms — release coating silicones for liner substrates |

### B7: Glassine & Release Liner Papers (HS 4806)

| CN Code | Description |
|---|---|
| 48064010 | Glassine papers in rolls or sheets — primary release liner base paper |
| 48064090 | Other glazed transparent/translucent papers — specialty transparent liner papers |

### B8: Printing Inks (HS 3215)

| CN Code | Description |
|---|---|
| 32151100 | Black printing ink — black inks for flexo, offset, digital label printing |
| 32151900 | Other printing ink — all colour inks for label printing |

### B9: RFID / Smart Labels (HS 8523)

| CN Code | Description |
|---|---|
| 85235910 | RFID tags, inlays, proximity cards — RFID smart label inlays |
| 85235990 | Other semiconductor media — other smart label components |

### B10: Stamping Foils (HS 3212)

| CN Code | Description |
|---|---|
| 32121000 | Stamping foils — hot stamping foils for premium label embellishment |

---

## Demand-Side: Comext Trade Series (15 CN codes)

These CN codes track **finished goods trade** in sectors that consume labels.

### Beverages (HS 20-22)

| CN Code | Description |
|---|---|
| 2009 | Fruit juices (incl. grape must) |
| 2201 | Mineral and aerated waters |
| 2202 | Non-alcoholic beverages (excl. water/juices) |
| 2203 | Beer made from malt |
| 2204 | Wine of fresh grapes |
| 2208 | Spirits, liqueurs and other spirituous beverages |

### HPC / Cleaning (HS 33-34)

| CN Code | Description |
|---|---|
| 3304 | Beauty, make-up and skin care preparations |
| 3305 | Hair preparations |
| 3307 | Shaving, deodorant, bath preparations |
| 3402 | Washing and cleaning preparations |

### Pharmaceuticals (HS 30)

| CN Code | Description |
|---|---|
| 3004 | Medicaments in measured doses |

### Processed Food (HS 16-21)

| CN Code | Description |
|---|---|
| 1602 | Prepared or preserved meat |
| 1604 | Prepared or preserved fish |
| 2005 | Prepared or preserved vegetables |
| 2106 | Food preparations n.e.c. |

---

## STS Monthly Index Series (158 series)

**Granularity**: Monthly
**Scope**: EU27 aggregate + individual EU member states
**Unit**: Index (2021=100), seasonally and calendar adjusted where available

### Industrial Datasets (10 datasets)

| Dataset | Name | Link |
|---|---|---|
| sts_inpr_m | Production in industry | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inpr_m/default/table) |
| sts_intv_m | Turnover in industry — total | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_intv_m/default/table) |
| sts_intvd_m | Turnover — domestic market | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_intvd_m/default/table) |
| sts_intvnd_m | Turnover — non-domestic market | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_intvnd_m/default/table) |
| sts_inpp_m | Producer prices — total | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inpp_m/default/table) |
| sts_inppd_m | Producer prices — domestic | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inppd_m/default/table) |
| sts_inppnd_m | Producer prices — non-domestic | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inppnd_m/default/table) |
| sts_inpi_m | Import prices | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inpi_m/default/table) |
| sts_inlb_m | Labour input | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inlb_m/default/table) |
| ei_bssi_m_r2 | Industry confidence | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/ei_bssi_m_r2/default/table) |

### Retail, Logistics & Confidence Datasets (4 datasets)

| Dataset | Name | NACE Codes | Link |
|---|---|---|---|
| sts_trtu_m | Retail trade turnover | G47, G47_FOOD, G47_NF_HLTH, G47_NFOOD_X_G473, G4711 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_trtu_m/default/table) |
| sts_sepr_m | Services production index | H, H49, H52, H53 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_sepr_m/default/table) |
| ei_bsrt_m_r2 | Retail trade confidence indicator | G47_FOOD, G47_NFOOD | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/ei_bsrt_m_r2/default/table) |
| ei_bsse_m_r2 | Services confidence indicator | H | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/ei_bsse_m_r2/default/table) |

### Supply-Side NACE Codes

| NACE | Description | Relevance |
|---|---|---|
| C17 | Paper and paper products | Paper labelstock, release liner papers, thermal papers |
| C171 | Pulp, paper and paperboard | Release liner base papers (glassine, kraft), label face papers |
| C1712 | Paper and paperboard | Core paper/board production |
| C172 | Articles of paper and paperboard | Converted labels, self-adhesive paper products |
| C1729 | Other articles of paper and paperboard | Finished labels (PSA and non-PSA) |
| C18 | Printing and reproduction | Label printing/converting activity |
| C20 | Chemicals and chemical products | Adhesives, silicones, polymer resins |
| C203 | Paints, varnishes, printing ink, mastics | Printing inks, overprint varnishes for labels |
| C2052 | Manufacture of glues | Adhesive manufacturing — PSA formulations |
| C22 | Rubber and plastic products | PSA tapes, plastic films, converted plastic products |
| C222 | Plastics products | Plastic label/film production |
| C2221 | Plastic plates, sheets, tubes, profiles | Film extrusion (PE, PP, PET, PVC) |
| C2229 | Other plastic products | PSA tapes and self-adhesive film products |
| C2829 | Other general-purpose machinery | Labelling and packaging machinery |

### Demand-Side NACE Codes

| NACE | Description | Relevance |
|---|---|---|
| C10 | Manufacture of food products | Major label end-market — product labelling |
| C11 | Manufacture of beverages | Beverage labelling (wine, beer, spirits, soft drinks) |
| C12 | Manufacture of tobacco products | Tobacco labelling (regulatory + brand) |
| C204 | Soap, detergents, cleaning, cosmetics, toiletries | HPC sector — high-value label segment |
| C21 | Basic pharmaceutical products and preparations | Pharma labelling (regulatory, track & trace) |

### Retail & Logistics NACE Codes

| NACE | Description | Relevance |
|---|---|---|
| G47 | Retail trade (excl. motor vehicles) | Overall retail demand for labelled products |
| G47_FOOD | Retail sale of food, beverages and tobacco | Food & beverage label demand |
| G47_NF_HLTH | Dispensing chemist, medical goods, cosmetics, toiletries | HPC & pharma retail label demand |
| G47_NFOOD_X_G473 | Non-food retail (excl. automotive fuel) | General non-food label demand |
| G4711 | Non-specialised stores (food predominating) | Supermarket/grocery label demand |
| G47_NFOOD | Retail non-food products | Non-food retail label demand |
| H | Transportation and storage | Logistics label demand (shipping, warehousing) |
| H49 | Land transport and pipelines | Road/rail freight — transport labels |
| H52 | Warehousing and transport support | Warehouse labelling demand |
| H53 | Postal and courier activities | Parcel/courier label demand (e-commerce) |

### Coverage Matrix — Industrial Datasets x NACE

Supply-side codes:

| Dataset | C17 | C171 | C1712 | C172 | C1729 | C18 | C20 | C203 | C2052 | C22 | C222 | C2221 | C2229 | C2829 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sts_inpr_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_intv_m | Y | | | | | Y | Y | | | Y | | | | |
| sts_intvd_m | Y | | | | | Y | Y | | | Y | | | | |
| sts_intvnd_m | Y | | | | | Y | Y | | | Y | | | | |
| sts_inpp_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inppd_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inppnd_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inpi_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inlb_m | Y | | | | | Y | Y | | | Y | | | | |
| ei_bssi_m_r2 | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

Demand-side codes:

| Dataset | C10 | C11 | C12 | C204 | C21 |
|---|---|---|---|---|---|
| sts_inpr_m | Y | Y | Y | Y | Y |
| sts_intv_m | Y | Y | Y | | Y |
| sts_intvd_m | Y | Y | Y | | Y |
| sts_intvnd_m | Y | Y | Y | | Y |
| sts_inpp_m | Y | Y | Y | Y | Y |
| sts_inppd_m | Y | Y | Y | Y | Y |
| sts_inppnd_m | Y | Y | Y | Y | Y |
| sts_inpi_m | Y | Y | Y | Y | Y |
| sts_inlb_m | Y | Y | Y | | Y |
| ei_bssi_m_r2 | Y | Y | Y | Y | Y |

Y = data extracted, blank = no data available for this combination

---

## Series Count Summary

| Category | Extracted |
|---|---|
| Comext trade — supply side | 41 |
| Comext trade — demand side | 15 |
| STS industrial indices (10 datasets x 19 NACE) | 146 |
| STS retail, logistics & confidence (4 datasets) | 12 |
| **Total** | **214** |

---

## Files

| File | Purpose |
|---|---|
| `test_eurostat_extraction.py` | Main extraction script — fetches all monthly series from Eurostat APIs |
| `visualize.py` | Chart generation — single-panel PNG per series with title + footnote |
| `utils.py` | Shared utilities — output directory management, quality assessment |
