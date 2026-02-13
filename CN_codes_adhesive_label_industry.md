# Comprehensive CN/HS Code Reference for the Pressure-Sensitive Adhesive Materials, Labels & Packaging Industry

## Eurostat COMEXT Database Reference for Market Intelligence

---

## TABLE OF CONTENTS

1. [Eurostat COMEXT Database & Dataset Access](#1-eurostat-comext-database--dataset-access)
2. [Self-Adhesive Products (HS 3919)](#2-self-adhesive-products---heading-3919)
3. [Self-Adhesive Paper & Paperboard (HS 4811.41, 4811.49)](#3-self-adhesive-paper--paperboard---heading-4811)
4. [Printed Labels (HS 4821)](#4-paper--paperboard-labels---heading-4821)
5. [Plastic Films - Polyethylene (HS 3920.10)](#5-plastic-films---polyethylene-pe---heading-392010)
6. [Plastic Films - Polypropylene/BOPP (HS 3920.20)](#6-plastic-films---polypropyleneBopp---heading-392020)
7. [Plastic Films - PVC (HS 3920.43, 3920.49)](#7-plastic-films---pvc---heading-392043--392049)
8. [Plastic Films - PET/Polyester (HS 3920.62)](#8-plastic-films---petpolyester---heading-392062)
9. [Other Plastic Films (HS 3920.xx)](#9-other-relevant-plastic-films---heading-3920xx)
10. [Cellular/Reinforced/Laminated Plastics (HS 3921)](#10-cellularreinforcedlaminated-plastic-sheets---heading-3921)
11. [Prepared Glues & Adhesives (HS 3506)](#11-prepared-glues--adhesives---heading-3506)
12. [Silicones for Release Coating (HS 3910)](#12-silicones-in-primary-forms---heading-3910)
13. [Coated Papers & Boards (HS 4810)](#13-coated-paper--paperboard---heading-4810)
14. [Glassine & Release Liner Papers (HS 4806)](#14-glassine--release-liner-papers---heading-4806)
15. [Kraft Papers & Boards (HS 4804, 4805)](#15-kraft-papers--boards---headings-4804--4805)
16. [Printing Inks (HS 3215)](#16-printing-inks---heading-3215)
17. [RFID/Smart Labels (HS 8523)](#17-rfid--smart-labels---heading-8523)

---

## 1. EUROSTAT COMEXT DATABASE & DATASET ACCESS

### Overview
The COMEXT (Commerce Exterieur) database is Eurostat's reference database for detailed statistics on international trade in goods. It provides full access to recent and historical data for the EU, the euro area, individual EU Member States, and many non-EU countries.

### Key Datasets (DS-prefixed)

| Dataset Code | Description | Classification | Granularity |
|-------------|-------------|----------------|-------------|
| **DS-045409** | EU trade since 1988 by HS2-4-6 and CN8 | HS2, HS4, HS6, CN8 | Monthly, by reporter, by partner |
| **DS-016890** | EU trade since 1988 by CN8 | CN8 (8-digit) | Monthly/Annual |
| **DS-016893** | EU trade since 1995 by HS6 | HS6 (6-digit) | Monthly/Annual |
| **DS-018995** | EU trade since 1988 by SITC | SITC | Monthly/Annual |
| **DS-057861** | EU trade by SITC (alternative) | SITC | Monthly/Annual |
| **DS-059268** | EU trade aggregates | Various | Monthly/Annual |

### Recommended Dataset for This Analysis
**DS-045409** is the most comprehensive -- it contains CN8-level data (8-digit Combined Nomenclature), which provides the finest product granularity available in EU trade statistics.

### Access Methods

| Method | URL/Details |
|--------|-------------|
| **Easy Comext (Web UI)** | https://ec.europa.eu/eurostat/comext/newxtweb/ |
| **Eurostat Data Browser** | https://ec.europa.eu/eurostat/databrowser/explore/all/all_themes?lang=en&node_code=ds-045409 |
| **COMEXT API** | Base URI: `https://ec.europa.eu/eurostat/api/comext/dissemination` |
| **Bulk Download** | CSV format, monthly zip files from 1988 onward |
| **Dataset Listing API** | `https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/dataflow/ESTAT/all` |

**Important Note:** The COMEXT API endpoint is different from the standard Eurostat API. Full dataset downloads are disabled due to size; queries must include filtering parameters (reporter, partner, product code, time period).

---

## 2. SELF-ADHESIVE PRODUCTS - Heading 3919

**Description:** Self-adhesive plates, sheets, film, foil, tape, strip and other flat shapes, of plastics, whether or not in rolls.

**Industry Relevance:** This is the CORE heading for pressure-sensitive label materials. Covers self-adhesive labelstock, tapes, protective films, graphic films, and all PSA-coated plastic materials.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39191012** | Self-adhesive plastic strips of PVC or polyethylene, coated with unvulcanised natural or synthetic rubber, in rolls of width <= 20 cm | Narrow-width PSA tapes, electrical tape, packaging tape |
| **39191015** | Self-adhesive plastic strips of polypropylene, coated with unvulcanised natural or synthetic rubber, in rolls of width <= 20 cm | PP-based PSA tapes, packaging tape |
| **39191019** | Self-adhesive plastic strips coated with unvulcanised natural or synthetic rubber, in rolls <= 20 cm wide (excl. PVC, PE, PP) | Other narrow PSA tapes (polyester, etc.) |
| **39191080** | Self-adhesive plates, sheets, film, foil, tape, strip and other flat shapes, of plastics, in rolls <= 20 cm wide (excl. strips coated with unvulcanised rubber) | **KEY CODE**: Narrow label rolls, die-cut labels on rolls, narrow PSA films |
| **39199020** | Self-adhesive circular polishing pads for semiconductor wafer manufacture | Specialty (semiconductor industry) |
| **39199080** | Self-adhesive plates, sheets, film, foil, tape, strip and other flat shapes, of plastics, whether or not in rolls > 20 cm wide | **KEY CODE**: Wide-format PSA labelstock, graphic films, decorative films, master rolls of label material |

---

## 3. SELF-ADHESIVE PAPER & PAPERBOARD - Heading 4811

**Description:** Paper, paperboard, cellulose wadding and webs of cellulose fibres, coated, impregnated, covered, surface-coloured, surface-decorated or printed, in rolls or rectangular sheets, of any size.

**Industry Relevance:** Covers paper-based self-adhesive labelstock, gummed papers, coated papers for label face stocks, and various specialty papers used in label converting.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **48114120** | Self-adhesive paper and paperboard, in strips/rolls <= 10 cm wide, coated with unvulcanised natural or synthetic rubber | Narrow self-adhesive paper tapes |
| **48114190** | Self-adhesive paper and paperboard, other (wider formats, other coatings) | **KEY CODE**: Paper-based self-adhesive labelstock, PSA paper materials in rolls/sheets |
| **48114900** | Gummed or adhesive paper and paperboard (excl. self-adhesive) | Gummed label paper, wet-glue label paper, envelope paper |
| **48111000** | Tarred, bituminised or asphalted paper and paperboard | Specialty industrial papers |
| **48115100** | Paper/paperboard coated with artificial resins or plastics, bleached, weighing > 150 g/m2 | Plastic-coated paper, PE-coated paper for release liners |
| **48115900** | Paper/paperboard coated with artificial resins or plastics (other, <= 150 g/m2) | Plastic-coated papers, PE-coated release liner base papers |
| **48116000** | Paper/paperboard coated with wax, paraffin wax, stearin, oil or glycerol | Wax-coated papers (specialty packaging) |
| **48119000** | Other paper, paperboard, cellulose wadding coated, impregnated or covered, n.e.s. | Thermal papers, specialty coated papers |

---

## 4. PAPER & PAPERBOARD LABELS - Heading 4821

**Description:** Paper or paperboard labels of all kinds, whether or not printed.

**Industry Relevance:** Covers the finished/converted label products -- both self-adhesive and non-self-adhesive paper labels.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **48211010** | Self-adhesive paper or paperboard labels of all kinds, printed | **KEY CODE**: Finished printed PSA labels (product labels, shipping labels, barcode labels) |
| **48211090** | Paper or paperboard labels of all kinds, printed (excl. self-adhesive) | Printed wet-glue labels, hang tags, printed paper labels |
| **48219010** | Self-adhesive paper or paperboard labels of all kinds, non-printed | **KEY CODE**: Blank PSA labels, thermal label blanks, label stock cut to size |
| **48219090** | Paper or paperboard labels of all kinds, non-printed (excl. self-adhesive) | Blank paper labels, unprinted tags |

---

## 5. PLASTIC FILMS - POLYETHYLENE (PE) - Heading 3920.10

**Description:** Non-cellular, non-reinforced plates, sheets, film, foil and strip of polymers of ethylene.

**Industry Relevance:** PE films are widely used as face stocks for labels (especially squeezable container labels), as well as backing/release liner films. The specific gravity threshold of 0.94 differentiates LDPE/LLDPE (< 0.94) from HDPE (>= 0.94).

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39201023** | PE film, 20-40 micrometres, specific gravity < 0.94, for photoresist/semiconductor manufacturing | Specialty PE film (semiconductor) |
| **39201024** | Stretch film of PE, not printed, thickness <= 0.125 mm, specific gravity < 0.94 | LDPE/LLDPE stretch film; potential liner film |
| **39201025** | Other PE film, thickness <= 0.125 mm, specific gravity < 0.94 | **KEY CODE**: LDPE/LLDPE films for label face stocks, overwrap, shrink film |
| **39201028** | PE film, thickness <= 0.125 mm, specific gravity >= 0.94 | **KEY CODE**: HDPE films for label face stocks, stiff packaging films |
| **39201040** | Other PE film/sheet, thickness <= 0.125 mm (special constructions, e.g. barrier films) | Multi-layer barrier PE films |
| **39201081** | Synthetic paper pulp from PE fibrils (thickness > 0.125 mm) | Specialty synthetic paper substitute |
| **39201089** | Other PE film/sheet, thickness > 0.125 mm | Thicker PE films, PE sheets for thermoforming |

---

## 6. PLASTIC FILMS - POLYPROPYLENE/BOPP - Heading 3920.20

**Description:** Non-cellular, non-reinforced plates, sheets, film, foil and strip of polymers of propylene.

**Industry Relevance:** BOPP (Biaxially Oriented Polypropylene) is one of the most widely used face stock materials for pressure-sensitive labels, especially for beverage labels, food packaging labels, and clear/no-look labels. Also used for release liners and overwrap.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39202021** | Biaxially oriented PP film, thickness <= 0.10 mm | **KEY CODE**: BOPP label face stock film, clear label film, metallised BOPP, white BOPP. Major volume code for the label industry. |
| **39202029** | Other (non-biaxially oriented) PP film, thickness <= 0.10 mm | Cast PP film, machine-direction oriented PP film |
| **39202080** | PP film, thickness > 0.10 mm | Thicker PP sheets, thermoformable PP |

---

## 7. PLASTIC FILMS - PVC - Heading 3920.43 & 3920.49

**Description:** Non-cellular, non-reinforced plates, sheets, film, foil and strip of polymers of vinyl chloride.

**Industry Relevance:** PVC films are used extensively for shrink sleeves, wrap-around labels, graphic/sign films, and conformable label face stocks (especially for curved surfaces).

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39204310** | Plasticised PVC film/sheet (>= 6% plasticiser), thickness <= 1 mm | **KEY CODE**: Flexible/conformable PVC label film, graphic film, shrink PVC |
| **39204390** | Plasticised PVC film/sheet (>= 6% plasticiser), thickness > 1 mm | Thicker flexible PVC sheet |
| **39204910** | Unplasticised (rigid) PVC film/sheet (< 6% plasticiser), thickness <= 1 mm | Rigid PVC film for blister packaging, cards |
| **39204990** | Unplasticised (rigid) PVC film/sheet (< 6% plasticiser), thickness > 1 mm | Rigid PVC sheet |

---

## 8. PLASTIC FILMS - PET/POLYESTER - Heading 3920.62

**Description:** Non-cellular, non-reinforced plates, sheets, film, foil and strip of poly(ethylene terephthalate).

**Industry Relevance:** PET (BOPET) films are critical in the label industry as face stocks (durable labels, tamper-evident labels), release liner films (PET liner), and lamination films. Also used for RFID antenna substrates.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39206212** | PET film for manufacture of flexible magnetic disks or photopolymer printing plates, thickness <= 0.35 mm | Specialty PET (printing plates = relevant for flexo plate making) |
| **39206219** | Other PET film, thickness <= 0.35 mm | **KEY CODE**: BOPET label face stock, PET release liner film, lamination film, metallised PET, transparent PET for labels. Major volume code. |
| **39206290** | PET film/sheet, thickness > 0.35 mm | Thicker PET sheets |

---

## 9. OTHER RELEVANT PLASTIC FILMS - Heading 3920.xx

**Description:** Other polymer-specific non-cellular, non-reinforced plastic films.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39203000** | Styrene polymer sheets and films | PS films (some label/packaging use) |
| **39205100** | Poly(methyl methacrylate) (PMMA) products | Acrylic sheets (signage) |
| **39205910** | Copolymer film of acrylic/methacrylic, thickness <= 150 micrometres | Acrylic films for specialty labels |
| **39205990** | Other acrylic polymer films | Acrylic films |
| **39206100** | Polycarbonate sheets and films | PC films (some overlay/laminate use) |
| **39206300** | Unsaturated polyester products | Specialty polyester films |
| **39206900** | Other polyester products | Other polyester-based films |
| **39207100** | Regenerated cellulose products | Cellophane film (classic packaging film) |
| **39207310** | Cellulose acetate film for photographic/sensitised surfaces | Specialty cellulose acetate |
| **39207380** | Other cellulose acetate plates and films | Cellulose acetate films |
| **39209200** | Polyamide (nylon) products | Nylon films (some label/packaging use) |
| **39209921** | Polyimide foil and strip | Polyimide films (electronic/high-temp labels) |
| **39209928** | Other condensation/rearrangement polymer films | Specialty polymer films |
| **39209952** | Poly(vinyl fluoride) and poly(vinyl alcohol) film | PVF films, PVOH films |
| **39209953** | Ion-exchange membranes of fluorinated plastic | Specialty membranes |
| **39209959** | Other addition polymerisation films | Other specialty films |
| **39209990** | Other plastic films/sheets n.e.s. | Catch-all for other plastic films |

---

## 10. CELLULAR/REINFORCED/LAMINATED PLASTIC SHEETS - Heading 3921

**Description:** Other plates, sheets, film, foil and strip of plastics -- cellular, reinforced, laminated, or otherwise combined.

**Industry Relevance:** Covers foam labels, laminated films, reinforced label materials, and cellular plastic sheets used in packaging.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39211100** | Cellular polymers of styrene | Foam PS (packaging inserts) |
| **39211200** | Cellular polymers of vinyl chloride | Foam PVC (sign materials) |
| **39211310** | Flexible cellular polyurethanes | Foam PU (cushioning labels, padding) |
| **39211390** | Other cellular polyurethanes | Rigid PU foam |
| **39211400** | Cellular regenerated cellulose | Cellulose sponge |
| **39211900** | Other cellular plastics | **KEY CODE**: PE foam, PP foam for label/packaging applications |
| **39219010** | Polyester condensation/rearrangement products (reinforced/laminated) | Laminated polyester films |
| **39219030** | Phenolic resin products (reinforced/laminated) | Specialty laminates |
| **39219055** | Other condensation/rearrangement polymer products | Specialty laminates |
| **39219060** | Addition polymerisation products (reinforced/laminated) | **KEY CODE**: Laminated PE, PP, PVC films -- multi-layer label constructions |
| **39219090** | Other (reinforced/laminated plastics) | Other multi-layer/laminated film constructions |

---

## 11. PREPARED GLUES & ADHESIVES - Heading 3506

**Description:** Prepared glues and other prepared adhesives, not elsewhere specified or included.

**Industry Relevance:** This heading covers the adhesive formulations used in pressure-sensitive adhesive (PSA) production, including acrylic PSAs, rubber-based PSAs, hot-melt adhesives, and specialty adhesives used in labelstock manufacturing.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **35061000** | Products suitable for use as glues or adhesives, put up for retail sale (net weight <= 1 kg) | Retail adhesive products |
| **35069110** | Optically clear adhesives for flat panel displays or touch-screen panels | Specialty OCA for electronics |
| **35069190** | Adhesives based on polymers of headings 3901 to 3913 or on rubber (excl. retail and display applications) | **KEY CODE**: All industrial PSA adhesives -- acrylic adhesives, rubber-based adhesives, hot-melt adhesives, water-based adhesives, solvent-based adhesives. This is the primary code for adhesive raw materials. |
| **35069900** | Other prepared glues and adhesives, n.e.s. | **KEY CODE**: Other specialty adhesives including starch-based, casein-based, and other prepared adhesive formulations |

**Note on related headings:**
- HS 3505 (Dextrins, modified starches, glues based on starches) -- relevant for starch-based label adhesives
- HS 3501-3504 (Casein, albumin, gelatin, peptones) -- relevant for protein-based adhesives

---

## 12. SILICONES IN PRIMARY FORMS - Heading 3910

**Description:** Silicones in primary forms.

**Industry Relevance:** Silicones are CRITICAL for the label industry as release coatings applied to release liners (both paper and film liners). Without silicone release coating, pressure-sensitive labels cannot be dispensed from their liner. This covers silicone fluids, emulsions, and resins used in release coating formulations.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **39100000** | Silicones in primary forms | **KEY CODE**: All silicone release coating materials -- polydimethylsiloxane (PDMS), silicone emulsions, platinum-cure silicones, condensation-cure silicones, UV-cure silicones, solvent-based and solventless silicone release systems |

**TARIC subdivisions (10-digit, for import declarations):**
| TARIC Code | Description | Industry Relevance |
|------------|-------------|-------------------|
| 3910000070 | Passivating silicon coating for semiconductor devices | Semiconductor use |
| 3910000080 | Specialty silicones | Specialty formulations |
| 3910000090 | Other silicones in primary forms | **KEY CODE**: General-purpose silicone release coatings |

---

## 13. COATED PAPER & PAPERBOARD - Heading 4810

**Description:** Paper and paperboard, coated on one or both sides with kaolin or other inorganic substances, with or without a binder, with no other coating.

**Industry Relevance:** Coated papers are widely used as face stocks for paper labels (gloss coated, semi-gloss, matte coated), and as base papers for thermal-transfer printing.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **48101300** | Coated paper in rolls, not containing mechanical fibers (or <= 10% by weight) | **KEY CODE**: Coated woodfree paper in rolls -- used as label face stock (gloss, semi-gloss, matte) |
| **48101400** | Coated paper in sheets (one side <= 435 mm, other <= 297 mm), not containing mechanical fibers | Coated paper in sheet form for labels |
| **48101900** | Other coated paper not containing mechanical fibers | Other coated woodfree papers for labels |
| **48102200** | Lightweight coated paper (LWC), mechanical fiber > 10% by weight | Lightweight coated papers (magazine-grade, some label applications) |
| **48102930** | Other coated paper with mechanical fibers, in rolls | Coated mechanical paper in rolls |
| **48102980** | Other coated paper with mechanical fibers, in sheets | Coated mechanical paper in sheets |
| **48103100** | Bleached kraft paper/paperboard coated with kaolin, <= 150 g/m2 | **KEY CODE**: Coated kraft paper -- used as label stock and packaging board |
| **48103210** | Bleached kraft paper coated with kaolin, > 150 g/m2 | Heavy-weight coated kraft board |
| **48103290** | Bleached kraft paper coated with inorganic substances, > 150 g/m2 | Coated kraft board |
| **48103900** | Other kraft paper/paperboard coated with kaolin | Other coated kraft papers |
| **48109210** | Multi-ply paper, all layers bleached, coated with kaolin | Coated multi-ply board for labels |
| **48109230** | Multi-ply paper, one layer bleached, coated with kaolin | Coated folding boxboard |
| **48109290** | Other multi-ply coated paper | Other coated boards |
| **48109910** | Bleached paper coated with kaolin (non-kraft, non-writing/printing) | Other specialty coated papers |
| **48109980** | Paper coated with inorganic substances (non-kaolin) | Specialty mineral-coated papers |

---

## 14. GLASSINE & RELEASE LINER PAPERS - Heading 4806

**Description:** Vegetable parchment, greaseproof papers, tracing papers and glassine and other glazed transparent or translucent papers.

**Industry Relevance:** Glassine is one of the primary base papers used for release liners in the label industry. Super-calendered kraft (SCK) and clay-coated kraft (CCK) are other common release liner substrates, but glassine-based release liners remain significant, especially in food-contact applications.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **48061000** | Vegetable parchment | Specialty paper (food wrapping) |
| **48062000** | Greaseproof papers | Food packaging paper |
| **48063000** | Tracing papers | Technical paper |
| **48064010** | Glassine papers | **KEY CODE**: Glassine release liner base paper -- the primary substrate for silicone-coated release liners in pressure-sensitive label constructions |
| **48064090** | Other glazed transparent or translucent papers (excl. glassine) | Translucent papers, specialty release liner papers |

---

## 15. KRAFT PAPERS & BOARDS - Headings 4804 & 4805

### Heading 4804 -- Uncoated Kraft Paper & Paperboard

**Industry Relevance:** Kraft papers are used as release liner base papers (especially super-calendered kraft / SCK and machine-finished kraft / MFK), as face stocks for industrial labels, and as packaging materials.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **48041111** | Unbleached kraftliner, < 150 g/m2 | Liner board for corrugated (label application surface) |
| **48041115** | Unbleached kraftliner, 150-175 g/m2 | Liner board |
| **48041119** | Unbleached kraftliner, >= 175 g/m2 | Heavy liner board |
| **48041190** | Other unbleached kraftliner | Other kraftliner |
| **48041912** | Mixed-ply kraftliner, < 175 g/m2 | Mixed-ply liner board |
| **48041919** | Mixed-ply kraftliner, >= 175 g/m2 | Heavy mixed-ply liner |
| **48041930** | Bleached/surface-coloured kraftliner | **White-top kraftliner** for label-quality surfaces |
| **48041990** | Other kraftliner | Other kraftliner |
| **48042110** | Unbleached sack kraft paper (coniferous pulp) | Sack kraft (industrial packaging) |
| **48042190** | Unbleached sack kraft paper (other) | Other sack kraft |
| **48042910** | Bleached sack kraft paper | Bleached sack kraft |
| **48042990** | Other sack kraft paper | Other sack kraft |
| **48043151** | Unbleached kraft insulating paper, <= 150 g/m2 | Specialty kraft |
| **48043158** | Unbleached kraft paper (coniferous), <= 150 g/m2 | **KEY CODE**: Base kraft paper suitable for release liner manufacturing (SCK, MFK grades) |
| **48043180** | Other unbleached kraft paper, <= 150 g/m2 | Other kraft papers for liners |
| **48043951** | Bleached kraft paper (coniferous), <= 150 g/m2 | Bleached kraft for release liners |
| **48043958** | Other bleached kraft paper, <= 150 g/m2 | Other bleached kraft |
| **48043980** | Other kraft paper, <= 150 g/m2 | Other kraft papers |
| **48044191** | Unbleached saturating kraft, 150-225 g/m2 | Saturating kraft (specialty) |
| **48044198** | Other unbleached kraft paper, 150-225 g/m2 | Medium-weight kraft |
| **48044200** | Bleached kraft paper, 150-225 g/m2 | Medium-weight bleached kraft |
| **48044900** | Other kraft paper, 150-225 g/m2 | Other medium kraft |
| **48045100** | Unbleached kraft paper, >= 225 g/m2 | Heavy kraft board |
| **48045200** | Bleached kraft paper, >= 225 g/m2 | Bleached kraft board |
| **48045910** | Kraft paper with coniferous pulp, >= 225 g/m2 | Heavy kraft board |
| **48045990** | Other kraft paper, >= 225 g/m2 | Other heavy kraft board |

### Heading 4805 -- Other Uncoated Paper & Paperboard

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **48051100** | Semi-chemical fluting paper | Corrugated medium |
| **48051200** | Straw fluting paper | Corrugated medium |
| **48051910** | Wellenstoff | Corrugated medium |
| **48051990** | Other fluting paper | Corrugated medium |
| **48053000** | Sulphite wrapping paper | Wrapping paper |
| **48054000** | Filter paper and paperboard | Filter papers |
| **48055000** | Felt paper and paperboard | Specialty papers |
| **48052400** | Testliner (recycled liner board), <= 150 g/m2 | Recycled liner board |
| **48052500** | Testliner (recycled liner board), > 150 g/m2 | Heavy recycled liner |
| **48059100** | Uncoated paper/paperboard, <= 150 g/m2 | **Potential release liner base papers, label backing papers** |
| **48059200** | Uncoated paper/paperboard, 150-225 g/m2 | Medium-weight uncoated papers |
| **48059320** | Recovered paper, >= 225 g/m2 | Recycled board |
| **48059380** | Other uncoated paper, >= 225 g/m2 | Heavy uncoated board |

---

## 16. PRINTING INKS - Heading 3215

**Description:** Printing ink, writing or drawing ink and other inks, whether or not concentrated or solid.

**Industry Relevance:** Printing inks are essential for label printing (flexographic, offset, gravure, digital, screen). UV-curable inks, water-based inks, and solvent-based inks are all captured here.

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **32151100** | Black printing ink | **KEY CODE**: Black inks for label printing (flexo, offset, gravure) |
| **32151900** | Other printing ink (excl. black) | **KEY CODE**: Colour inks for label printing -- CMYK process colours, spot colours, UV-curable inks, water-based flexo inks |
| **32159020** | Ink cartridges for printers/copiers (with mechanical/electrical components); solid engineered inks | Digital printing ink cartridges (for digital label presses) |
| **32159070** | Other inks (excl. printing ink, cartridges) | Writing inks, drawing inks, specialty inks, thermal transfer ribbons ink |

---

## 17. RFID & SMART LABELS - Heading 8523

**Description:** Discs, tapes, solid-state non-volatile storage devices, 'smart cards' and other media for the recording of sound or of other phenomena.

**Industry Relevance:** RFID inlays, tags, and smart labels are an increasingly important product category for companies like Avery Dennison. These products combine pressure-sensitive labels with electronic functionality (UHF, HF/NFC, LF RFID).

| CN8 Code | Description | Industry Relevance |
|----------|-------------|-------------------|
| **85235200** | Smart cards incorporating one or more electronic integrated circuits | **KEY CODE**: RFID smart cards, NFC cards |
| **85235110** | Flash memory cards, unrecorded | Flash storage |
| **85235190** | Flash memory cards, recorded | Flash storage |
| **85235910** | Other semiconductor media, unrecorded (excl. flash and smart cards) | **KEY CODE**: RFID inlays and tags (unrecorded/blank) -- passive RFID inlays for label conversion |
| **85235990** | Other semiconductor media, recorded (excl. flash and smart cards) | **KEY CODE**: RFID inlays and tags (programmed/encoded) -- encoded RFID labels |
| **85238010** | Other recording media, unrecorded | Other electronic media |
| **85238090** | Other recording media, recorded | Other electronic media |

**Note:** Classification of RFID labels can be complex. Depending on the product's primary function:
- A simple RFID inlay/tag with IC chip: typically 8523.59
- An RFID smart card: 8523.52
- A paper label with integrated RFID that is primarily a label: could fall under 4821 (paper labels)
- Binding rulings may be required for specific product classifications

---

## SUMMARY: PRIORITY CN8 CODES FOR MARKET INTELLIGENCE

The following is a condensed list of the highest-priority CN8 codes for monitoring the pressure-sensitive adhesive materials, labels, and packaging industry in the EU:

### Tier 1 -- Core Products (Monitor closely)

| CN8 Code | Product |
|----------|---------|
| 39191080 | Self-adhesive plastic films/tapes, rolls <= 20 cm |
| 39199080 | Self-adhesive plastic films/sheets, other (> 20 cm or sheets) |
| 48114190 | Self-adhesive paper and paperboard |
| 48211010 | Printed self-adhesive labels (paper/paperboard) |
| 48219010 | Non-printed self-adhesive labels (paper/paperboard) |
| 35069190 | Adhesives based on polymers/rubber (industrial PSA) |
| 39100000 | Silicones in primary forms (release coatings) |

### Tier 2 -- Key Raw Materials (Films)

| CN8 Code | Product |
|----------|---------|
| 39202021 | BOPP film (biaxially oriented), <= 0.10 mm |
| 39206219 | PET film, <= 0.35 mm |
| 39201025 | PE film (LDPE/LLDPE), <= 0.125 mm, SG < 0.94 |
| 39201028 | PE film (HDPE), <= 0.125 mm, SG >= 0.94 |
| 39204310 | Plasticised PVC film, <= 1 mm |
| 39204910 | Unplasticised PVC film, <= 1 mm |

### Tier 3 -- Papers & Board

| CN8 Code | Product |
|----------|---------|
| 48064010 | Glassine papers (release liner base) |
| 48101300 | Coated woodfree paper in rolls (label face stock) |
| 48043158 | Unbleached kraft paper <= 150 g/m2 (release liner base) |
| 48114120 | Self-adhesive paper strips, <= 10 cm wide |

### Tier 4 -- Inks & Finishing

| CN8 Code | Product |
|----------|---------|
| 32151100 | Black printing ink |
| 32151900 | Colour printing inks |
| 32159020 | Ink cartridges (digital printing) |

### Tier 5 -- RFID/Smart Labels

| CN8 Code | Product |
|----------|---------|
| 85235200 | Smart cards (RFID cards) |
| 85235910 | Semiconductor media, unrecorded (RFID inlays) |
| 85235990 | Semiconductor media, recorded (encoded RFID) |

### Tier 6 -- Other Adhesives & Labels

| CN8 Code | Product |
|----------|---------|
| 35069900 | Other prepared adhesives n.e.s. |
| 48114900 | Gummed/adhesive paper (non-self-adhesive) |
| 48211090 | Printed labels (non-self-adhesive) |
| 48219090 | Non-printed labels (non-self-adhesive) |

---

## NOTES ON USING THESE CODES WITH EUROSTAT COMEXT

1. **Querying DS-045409**: Use the CN8 codes above as the PRODUCT dimension filter. Combine with:
   - REPORTER: Individual EU member states (e.g., DE, FR, IT, NL, FI) or EU27_2020 aggregate
   - PARTNER: All partners, or filter for specific trade partners (CN=China, US, JP, KR, etc.)
   - FLOW: 1=Imports, 2=Exports
   - PERIOD: Monthly (YYYYMM) or Annual (YYYY)
   - INDICATORS: VALUE_IN_EUROS, QUANTITY_IN_100KG, SUPPLEMENTARY_QUANTITY

2. **API Endpoint**: `https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/...`

3. **Easy Comext Interface**: For interactive queries, use https://ec.europa.eu/eurostat/comext/newxtweb/
   - Select "Products" -> enter CN8 codes
   - Select reporting countries and partner countries
   - Choose time period
   - Export in CSV or Excel format

4. **Bulk Download**: For large-scale analysis, download monthly CSV files from the bulk download facility and filter locally.

5. **CN Code Changes**: The Combined Nomenclature is updated annually (usually effective January 1). Always verify that codes are valid for the reporting period being analyzed. Historical data may use different code structures.

---

*Document compiled: February 2026*
*Sources: Eurostat COMEXT, EU Combined Nomenclature 2024, TARIC database, tariffnumber.com, taricsupport.com*
