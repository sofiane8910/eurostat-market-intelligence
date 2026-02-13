# Eurostat Monthly Data Extraction — PSA & Labels Industry

Automated extraction of Eurostat monthly time series for the European pressure-sensitive adhesive (PSA) materials, labels, release liners, films, and converting industry.

**Time range**: 2023-01 to 2025-12
**Frequency**: Monthly (all series)
**Source**: Eurostat Comext (DS-045409) and Short-Term Statistics (STS)

---

## Output Structure

```
output/
├── quality_report.md          # Quality assessment for all series
├── comext/                    # Trade data (CSV + PNG per CN code)
│   ├── CN_39191010.csv
│   ├── CN_39191010.png
│   └── ...
└── sts/                       # Industry indices (CSV + PNG per dataset×NACE)
    ├── sts_inpr_m_C2229.csv
    ├── sts_inpr_m_C2229.png
    └── ...
```

---

## Comext Trade Series (46 CN codes)

**Dataset**: DS-045409
**Granularity**: Monthly
**Scope**: All 27 EU member states as reporters, WORLD as partner, imports + exports
**Indicators**: VALUE_IN_EUROS, QUANTITY_IN_100KG

### B1: Self-Adhesive Plastics (HS 3919)

| CN Code | Description |
|---|---|
| 39191010 | SA plastic strips in rolls <= 20cm wide, width <= 20cm |
| 39191080 | SA plastic strips in rolls <= 20cm wide, other |
| 39199010 | SA plastic sheets/films (excl. rolls <= 20cm), condensation polymerisation — PET, PU, PC-based labelstock |
| 39199020 | SA plastic sheets/films (excl. rolls <= 20cm), addition polymerisation — PE, PP, PVC-based labelstock |
| 39199080 | SA plastic sheets/films (excl. rolls <= 20cm), other — catch-all for PSA labelstock exports/imports |

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
| 39206210 | PET film, thickness <= 0.025mm — ultrathin PET for liner films, capacitor films |
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
| 32159000 | Other ink (excl. printing) — coding/marking inks |

### B9: RFID / Smart Labels (HS 8523)

| CN Code | Description |
|---|---|
| 85235210 | Smart cards with electronic integrated circuit — smart card inlays |
| 85235910 | RFID tags, inlays, proximity cards — RFID smart label inlays |
| 85235990 | Other semiconductor media — other smart label components |

### B10: Stamping Foils (HS 3212)

| CN Code | Description |
|---|---|
| 32121000 | Stamping foils — hot stamping foils for premium label embellishment |

---

## STS Monthly Index Series (11 datasets x 14 NACE codes)

**Granularity**: Monthly
**Scope**: EU27 aggregate + individual EU member states
**Unit**: Index (2021=100), seasonally and calendar adjusted where available

### Datasets

| Dataset | Name | Description |
|---|---|---|
| sts_inpr_m | Production in industry | Monthly production volume index — tracks output levels |
| sts_intv_m | Turnover in industry — total | Monthly revenue index, domestic + export combined |
| sts_intvd_m | Turnover — domestic market | Domestic market revenue trends |
| sts_intvnd_m | Turnover — non-domestic market | Export revenue trends |
| sts_inpp_m | Producer prices — total | Output selling price trends — pricing power indicator |
| sts_inppd_m | Producer prices — domestic | Domestic market selling prices |
| sts_inppnd_m | Producer prices — non-domestic | Export selling prices — competitive pressure indicator |
| sts_inpi_m | Import prices | Input cost trends for raw materials — cost pressure signal |
| sts_ordi_m | New orders | New order intake — leading demand indicator (1-3 month lead) |
| sts_inlb_m | Labour input | Hours worked — capacity utilization proxy |
| ei_bssi_m_r2 | Industry confidence | Business expectations for production, orders, stocks — sentiment indicator |

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

### Coverage Matrix

Not all dataset x NACE combinations have data. The table below shows availability (based on extraction results):

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
| sts_ordi_m | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| sts_inlb_m | Y | - | - | - | - | Y | Y | - | - | Y | - | - | - | - |
| ei_bssi_m_r2 | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

Y = data available, - = no data for this combination

---

## Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run extraction + visualization (takes ~10-15 minutes)
python test_eurostat_extraction.py

# Or generate charts only (from existing CSVs)
python visualize.py
```

---

## Files

| File | Purpose |
|---|---|
| `test_eurostat_extraction.py` | Main extraction script — fetches all monthly series from Eurostat APIs |
| `visualize.py` | Chart generation — single-panel PNG per series with title + footnote |
| `utils.py` | Shared utilities — output directory management, quality assessment |
| `eurostat_series_reference.md` | Full reference document — all Eurostat series relevant to PSA industry |
| `CN_codes_adhesive_label_industry.md` | CN code reference for adhesive/label trade classification |
