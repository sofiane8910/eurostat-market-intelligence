# Eurostat Market Intelligence — PSA & Labels Industry

Automated monthly data extraction from Eurostat for the European pressure-sensitive adhesive (PSA) materials, labels, release liners, films, and converting industry.

**Frequency**: Monthly (all series)
**Time range**: 2023-01 to 2025-12
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
    └── ...
```

---

## Usage

```bash
source .venv/bin/activate

# Run extraction + visualization (~10-15 minutes)
python test_eurostat_extraction.py

# Or generate charts only (from existing CSVs)
python visualize.py
```

---

## Comext Trade Series (41 CN codes)

**Dataset**: DS-045409
**Granularity**: Monthly, by EU27 member state as reporter
**Partner**: WORLD aggregate (no individual partner country breakdown)
**Indicators**: VALUE_IN_EUROS, QUANTITY_IN_100KG

> The Comext API supports partner-country breakdowns (e.g. by CN, US, JP) but the current extraction uses WORLD aggregate only. To add bilateral trade data, modify the `WORLD` parameter in `test_eurostat_extraction.py`.

### B1: Self-Adhesive Plastics (HS 3919)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39191080 | SA plastic strips in rolls <= 20cm wide, other | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39199020 | SA plastic sheets/films (excl. rolls <= 20cm), addition polymerisation — PE, PP, PVC-based labelstock | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39199080 | SA plastic sheets/films (excl. rolls <= 20cm), other — catch-all for PSA labelstock | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B2: Self-Adhesive Paper & Paperboard (HS 4811)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 48114100 | Self-adhesive paper and paperboard — paper PSA labelstock (face + adhesive + liner) | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 48114900 | Gummed/adhesive paper & paperboard (excl. self-adhesive) — competing wet-gummed technology | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B3: Labels of Paper & Paperboard (HS 4821)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 48211010 | Self-adhesive printed labels of paper/paperboard — finished converted PSA labels | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 48211090 | Other printed labels of paper/paperboard (excl. SA) — wet-glue, shrink sleeve labels | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 48219010 | Self-adhesive labels, paper/paperboard (unprinted) — blank thermal/shipping labels | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 48219090 | Other labels, paper/paperboard (unprinted, excl. SA) — blank non-PSA labels | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B4.1: PE Films (HS 3920.10)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39201023 | PE film, SG < 0.94, thickness <= 0.025mm — thin LDPE/LLDPE films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39201024 | PE film, SG < 0.94, thickness 0.025-0.05mm — medium LDPE films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39201025 | PE film, SG < 0.94, thickness > 0.05mm — thicker LDPE films, label face stock gauge | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39201028 | Other PE film, SG < 0.94 — other LDPE/LLDPE films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39201040 | PE film, SG >= 0.94, thickness < 0.021mm — thin HDPE films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39201081 | PE film, SG >= 0.94, thickness 0.021-0.160mm — standard HDPE films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39201089 | Other PE film, SG >= 0.94 — other HDPE films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B4.2: PP Films (HS 3920.20)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39202021 | BOPP film, thickness <= 0.10mm — the #1 filmic label face stock material | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39202029 | Other PP film (cast/OPP), thickness <= 0.10mm — cast PP for wrap-around labels | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39202080 | PP film, thickness > 0.10mm — thicker PP films for heavy-duty applications | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B4.3: PVC Films (HS 3920.43/49)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39204310 | Flexible PVC film (>= 6% plasticiser), not supported — conformable label/graphic film | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39204390 | Other flexible PVC film | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39204910 | Rigid PVC film, thickness > 1mm — thick rigid PVC for blister packaging | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39204990 | Other rigid PVC film — thin rigid PVC | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B4.4: PET Films (HS 3920.62)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39206219 | PET film, thickness 0.025-0.35mm — standard PET for label face stocks and release liners | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39206290 | PET film, thickness > 0.35mm — heavy PET sheets for industrial labels | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B4.5: Other Films

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39206100 | Polycarbonate film — durable label substrates for harsh environments | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39206900 | Other polyester film (PEN, PBT, etc.) — specialty high-performance label substrates | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39209928 | Polyimide film — high-temperature labels for electronics and automotive | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 39209959 | Other plastic film, n.e.c. — catch-all including bio-based and TPU films | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B5: Adhesives (HS 3506)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 35061000 | Adhesives, retail sale, net weight <= 1kg — small-format retail adhesives | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 35069110 | Water-based adhesives from synthetic polymers — water-based PSA emulsions, PVAc | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 35069190 | Other adhesives based on synthetic polymers or rubber — solvent-based PSA, hot-melt, UV-curable | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 35069900 | Other prepared glues/adhesives, n.e.c. — other industrial adhesives | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B6: Silicones (HS 3910)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 39100000 | Silicones in primary forms — release coating silicones for liner substrates | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B7: Glassine & Release Liner Papers (HS 4806)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 48064010 | Glassine papers in rolls or sheets — primary release liner base paper | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 48064090 | Other glazed transparent/translucent papers — specialty transparent liner papers | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B8: Printing Inks (HS 3215)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 32151100 | Black printing ink — black inks for flexo, offset, digital label printing | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 32151900 | Other printing ink — all colour inks for label printing | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B9: RFID / Smart Labels (HS 8523)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 85235910 | RFID tags, inlays, proximity cards — RFID smart label inlays | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |
| 85235990 | Other semiconductor media — other smart label components | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### B10: Stamping Foils (HS 3212)

| CN Code | Description | Freq | Range | Partner Detail | Link |
|---|---|---|---|---|---|
| 32121000 | Stamping foils — hot stamping foils for premium label embellishment | Monthly | 2023-01 to 2025-12 | WORLD only | [Comext](https://ec.europa.eu/eurostat/comext/newxtweb/) |

### Excluded CN Codes (no data returned from Eurostat)

The following CN codes were requested but returned 0 rows — likely discontinued or reclassified:

| CN Code | Description | Reason |
|---|---|---|
| 39191010 | SA plastic strips in rolls <= 20cm, width <= 20cm | No data returned |
| 39199010 | SA plastic sheets/films, condensation polymerisation — PET, PU, PC-based | No data returned |
| 39206210 | PET film, thickness <= 0.025mm | No data returned |
| 32159000 | Other ink (excl. printing) — coding/marking inks | No data returned |
| 85235210 | Smart cards with electronic integrated circuit | No data returned |

---

## STS Monthly Index Series (100 series extracted)

**Granularity**: Monthly
**Scope**: EU27 aggregate + individual EU member states
**Unit**: Index (2021=100), seasonally and calendar adjusted where available
**Partner detail**: N/A (industry indices, not trade data)

### Datasets

| Dataset | Name | Freq | Range | NACE codes with data | Link |
|---|---|---|---|---|---|
| sts_inpr_m | Production in industry | Monthly | 2023-01 to 2025-12 | All 14 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inpr_m/default/table) |
| sts_intv_m | Turnover in industry — total | Monthly | 2023-01 to 2025-12 | C17, C18, C20, C22 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_intv_m/default/table) |
| sts_intvd_m | Turnover — domestic market | Monthly | 2023-01 to 2025-12 | C17, C18, C20, C22 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_intvd_m/default/table) |
| sts_intvnd_m | Turnover — non-domestic market | Monthly | 2023-01 to 2025-12 | C17, C18, C20, C22 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_intvnd_m/default/table) |
| sts_inpp_m | Producer prices — total | Monthly | 2023-01 to 2025-12 | All 14 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inpp_m/default/table) |
| sts_inppd_m | Producer prices — domestic | Monthly | 2023-01 to 2025-12 | All 14 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inppd_m/default/table) |
| sts_inppnd_m | Producer prices — non-domestic | Monthly | 2023-01 to 2025-12 | All 14 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inppnd_m/default/table) |
| sts_inpi_m | Import prices | Monthly | 2023-01 to 2025-12 | All 14 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inpi_m/default/table) |
| sts_inlb_m | Labour input | Monthly | 2023-01 to 2025-12 | C17, C18, C20, C22 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/sts_inlb_m/default/table) |
| ei_bssi_m_r2 | Industry confidence | Monthly | 2023-01 to 2025-12 | All 14 | [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/ei_bssi_m_r2/default/table) |

### NACE Codes

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

### Coverage Matrix (dataset x NACE)

| Dataset | C17 | C171 | C1712 | C172 | C1729 | C18 | C20 | C203 | C2052 | C22 | C222 | C2221 | C2229 | C2829 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sts_inpr_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_intv_m | Y | - | - | - | - | Y | Y | - | - | Y | - | - | - | - |
| sts_intvd_m | Y | - | - | - | - | Y | Y | - | - | Y | - | - | - | - |
| sts_intvnd_m | Y | - | - | - | - | Y | Y | - | - | Y | - | - | - | - |
| sts_inpp_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inppd_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inppnd_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inpi_m | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| sts_inlb_m | Y | - | - | - | - | Y | Y | - | - | Y | - | - | - | - |
| ei_bssi_m_r2 | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

Y = data available, - = no data for this combination

### Excluded STS Dataset

| Dataset | Name | Reason |
|---|---|---|
| sts_ordi_m | New orders in industry | 0 rows for all 14 NACE codes — not available for these sectors |

---

## Series Count Summary

| Category | Extracted | Failed | Total Attempted |
|---|---|---|---|
| Comext trade (CN codes) | 41 | 5 | 46 |
| STS indices (dataset x NACE) | 100 | 54 | 154 |
| **Total** | **141** | **59** | **200** |

---

## Files

| File | Purpose |
|---|---|
| `test_eurostat_extraction.py` | Main extraction script — fetches all monthly series from Eurostat APIs |
| `visualize.py` | Chart generation — single-panel PNG per series with title + footnote |
| `utils.py` | Shared utilities — output directory management, quality assessment |
