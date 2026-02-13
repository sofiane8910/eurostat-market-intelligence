# EUROSTAT SERIES REFERENCE — AVERY DENNISON MARKET INTELLIGENCE

**Scope**: All Eurostat statistical series relevant to the European pressure-sensitive adhesive (PSA) materials, labels, release liners, films, and converting industry.

**Purpose**: Market sizing, competitive benchmarking, supply chain monitoring, pricing analysis, demand forecasting, and strategic planning.

**Last updated**: February 2025

---

## TABLE OF CONTENTS

1. [PART A — PRODCOM: EU Production Statistics by Product](#part-a--prodcom-eu-production-statistics-by-product)
2. [PART B — COMEXT: International Trade by CN/HS Code](#part-b--comext-international-trade-by-cnhs-code)
3. [PART C — HIGH-LEVEL TIME SERIES: Industry Indices & Structural Data](#part-c--high-level-time-series-industry-indices--structural-data)
4. [PART D — DATA ACCESS, METHODOLOGY & MARKET SIZING](#part-d--data-access-methodology--market-sizing)
5. [PART E — PRIORITY MATRIX & RECOMMENDED WORKFLOW](#part-e--priority-matrix--recommended-workflow)

---

# PART A — PRODCOM: EU PRODUCTION STATISTICS BY PRODUCT

**What is PRODCOM?**
PRODCOM (PRODuction COMmunautaire) is the EU system for collecting and publishing statistics on the production of manufactured goods. Data is reported annually by EU member states at the 8-digit product level. It provides:
- **Sold production value** (in EUR)
- **Sold production volume** (in kg, m2, units, etc.)
- **Total production volume**
- Data available by **individual EU country** and **EU aggregates**

**Primary Dataset**: `DS-059358` — Sold production, exports and imports by PRODCOM list (NACE Rev. 2)

**Eurostat Access**: https://ec.europa.eu/eurostat/databrowser/product/view/ds-059358

**Time coverage**: 1995–present (annual)

**How to query**: Filter by PRCCODE (enter code without dots, e.g. `22292140`)

---

## A1. SELF-ADHESIVE PRODUCTS — THE CORE MARKET

These codes directly capture Avery Dennison's primary product categories: PSA labelstock, tapes, and finished labels.

### A1.1 Self-Adhesive Plastic Products (NACE 22.29)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.29.21.30** | Self-adhesive strips of plastic with a coating consisting of unvulcanised natural or synthetic rubber, in rolls of a width <= 20 cm | kg | Rubber-coated PSA tapes in narrow rolls. Covers masking tapes, duct tapes, electrical tapes with natural or synthetic rubber adhesive. Competitors: tesa (Beiersdorf), 3M, Nitto Denko. |
| **22.29.21.40** | Self-adhesive plates, sheets, film, foil, tape, strip and other flat shapes, of plastics, in rolls <= 20 cm wide (excluding plastic strips coated with unvulcanised natural or synthetic rubber) | kg | **CRITICAL CODE.** Covers all non-rubber PSA tapes and converted label rolls in narrow format: acrylic PSA tapes, hot-melt PSA tapes, narrow die-cut label rolls, printed label rolls, barcode label rolls. This is the most common format for end-user label application. |
| **22.29.22.40** | Self-adhesive plates, sheets, film, foil, tape, strip and other flat shapes, of plastics, whether or not in rolls > 20 cm wide (excluding floor, wall and ceiling coverings of HS 3918) | kg | **CRITICAL CODE.** Covers wide-format self-adhesive plastic films and labelstock in jumbo/master rolls. This is the PRIMARY output of Avery Dennison's Materials Group: master rolls of filmic PSA labelstock (PP, PE, PET, PVC face stocks laminated with adhesive + liner), wide graphic films, wide PSA films for industrial applications. Also covers competitors like UPM Raflatac, Fedrigoni (Ritrama), Lintec, Coveris. |

### A1.2 Self-Adhesive Paper Products (NACE 17.12)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.12.77.33** | Self-adhesive paper and paperboard in rolls or sheets | kg | **CRITICAL CODE.** Covers self-adhesive paper labelstock in jumbo/master rolls and sheets — face paper already laminated with adhesive and release liner, BEFORE converting (die-cutting/printing). This is the paper equivalent of 22.29.22.40 and represents Avery Dennison's core paper labelstock output. Corresponds to CN 4811.41. Major competitors: UPM Raflatac, Fedrigoni, Herma, Lecta. |
| **17.12.77.35** | Gummed paper and paperboard in rolls or sheets (excluding self-adhesives) | kg | Wet-gummed paper (non-PSA). Alternative/competing technology — gummed envelopes, stamps, wet-glue label papers. Declining market but still used in some packaging applications. |

### A1.3 Self-Adhesive Labels — Finished Products (NACE 17.29)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.29.11.20** | Self-adhesive printed labels of paper or paperboard | EUR/kg | **CRITICAL CODE.** Finished converted printed PSA labels — the output of label converters (Avery Dennison's customers). Covers prime labels, variable information labels, barcode/shipping labels, pharmaceutical labels, food labels. Tracks the downstream demand that drives labelstock sales. Major converters: Multi-Color Corp (now Platinum Equity), CCL Industries, Coveris. |
| **17.29.11.40** | Printed labels of paper or paperboard (excluding self-adhesive) | EUR/kg | Non-PSA printed labels: wet-glue labels, shrink sleeves of paper, in-mould labels of paper. These are **competing label technologies**. Tracking this helps understand technology substitution trends (PSA vs. wet-glue vs. shrink). |
| **17.29.11.60** | Self-adhesive labels of paper or paperboard (excluding printed) | EUR/kg | Unprinted/blank PSA label stock — blank die-cut labels, blank thermal labels (before variable data printing at end-user site), blank shipping labels. Important for the thermal label segment (logistics, warehousing, retail). |
| **17.29.11.80** | Labels of paper or paperboard (excluding printed, excluding self-adhesive) | EUR/kg | Blank non-PSA labels. Niche adjacent market. |

---

## A2. ADHESIVES — RAW MATERIAL & COMPETITOR MARKET

These codes cover the adhesive formulations used in PSA labelstock manufacturing and in competing adhesive technologies.

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.52.10.10** | Adhesives based on natural polymers | kg | Natural rubber-based adhesives, starch-based glues, casein adhesives, dextrin-based adhesives. Relevant for natural rubber PSA formulations (used in some tape products) and traditional wet-glue formulations. Natural rubber is still a significant PSA chemistry for tapes. |
| **20.52.10.80** | Prepared glues and other prepared adhesives, n.e.c. (not elsewhere classified) | kg | **CRITICAL CODE.** This is the catch-all for ALL synthetic adhesives including: acrylic PSA (the dominant label adhesive chemistry), hot-melt PSA (SBC-based, EVA, polyolefin), water-based emulsion adhesives, solvent-based adhesives, UV-curable adhesives, silicone PSA, polyurethane adhesives, epoxy adhesives, cyanoacrylates. Unfortunately, Eurostat does NOT break this code down by adhesive technology. For technology-level segmentation, rely on industry reports (AWA, FINAT, TLMI). Competitors: Henkel, H.B. Fuller, Bostik (Arkema), Dow, 3M, Loctite. |

> **LIMITATION**: PRODCOM does not distinguish between PSA types (acrylic vs. rubber vs. hot-melt vs. silicone). The 20.52.10.80 code is a broad catch-all. To segment by adhesive chemistry, supplement with trade data (CN 3506.91.xx) and industry association reports.

---

## A3. PLASTIC FILMS — FACE STOCKS & RELEASE LINER FILMS

These codes cover the plastic films used as face materials for filmic labels and as release liner substrates.

### A3.1 Polyethylene (PE) Films — LDPE, LLDPE, HDPE

**Applications in label industry**: PE face stocks for squeezable container labels (shampoo, ketchup), shrink labels, PE liner films, PE overwrap.

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.21.30.10** | Plates, sheets, film, foil and strip, of polymers of ethylene, not reinforced, laminated, supported or similarly combined with other materials, thickness <= 0.125 mm | kg | **PRIMARY PE FILM CODE.** Covers LDPE, LLDPE, and HDPE films up to 125 microns — the most common thickness range for label face stocks and packaging films. PE films are used for conformable labels on squeezable containers (personal care, food), and increasingly for mono-material recyclable label constructions (PE label on PE bottle). |
| **22.21.30.17** | Plates, sheets, film, foil and strip, of polymers of ethylene, not reinforced, etc., thickness > 0.125 mm | kg | Thicker PE films/sheets. Used for heavier gauge label face stocks, protective films, and industrial applications. Less common in standard labeling but relevant for specialty constructions. |

### A3.2 Polypropylene (PP) Films — BOPP, OPP, Cast PP

**Applications in label industry**: BOPP is the DOMINANT clear filmic label face stock globally. Used for beverage labels, food packaging labels, personal care labels, and increasingly as a release liner substrate ("rapid roll" / linerless constructions).

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.21.30.21** | Plates, sheets, film, foil and strip, of biaxially oriented polymers of propylene (BOPP), not reinforced, etc., thickness <= 0.10 mm | kg | **CRITICAL CODE.** This IS the BOPP film market. BOPP (biaxially oriented polypropylene) is the single most important filmic label face stock material — clear, white, metallized, pearlized BOPP grades dominate the filmic label segment. Also used extensively for flexible packaging, overwrap, and tape backing. Key BOPP film producers: Taghleef Industries, Innovia Films (CCL), Cosmo Films, Jindal Films, Treofan. This code is essential for understanding filmic label face stock supply. |
| **22.21.30.23** | Plates, sheets, film, foil and strip, of polymers of propylene (excl. biaxially oriented), thickness <= 0.10 mm | kg | Cast PP and unoriented PP films. Used as an alternative to BOPP in some label applications (cast PP has better clarity for certain wrap-around labels), and increasingly explored as PP-based release liner films. |
| **22.21.30.26** | Plates, sheets, film, foil and strip, of non-cellular polymers of propylene, not reinforced, etc., thickness > 0.10 mm | kg | Thicker PP films/sheets. Used in heavy-duty label applications, rigid packaging, and thermoformed containers receiving labels. |

### A3.3 PET (Polyethylene Terephthalate) Films

**Applications in label industry**: PET films serve a DUAL role — as (1) durable label face stocks (chemical/thermal resistance for industrial, automotive, electronics labels) AND as (2) release liner films (PET liner — replacing paper liners in automated/high-speed dispensing, "rapid roll" applications). Also used for overlaminates and graphic protection films.

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.21.30.65** | Plates, sheets, film, foil, strip, of polyethylene terephthalate (PET), not reinforced, etc., of a thickness <= 0.35 mm | kg | **CRITICAL CODE.** Covers the vast majority of PET films used in the label industry: 12 micron PET for liner films ("PET liner" — a major growth segment replacing glassine for high-speed/automated labeling and "rapid roll" constructions), 23-50 micron PET for durable label face stocks, and PET overlaminates. The shift from paper liners to PET liners is one of the biggest structural trends in the label industry. Key PET film producers: Mitsubishi Chemical (Hostaphan), DuPont Teijin, Polyplex, Uflex, Toray, SKC. |
| **22.21.30.67** | Plates, sheets, film, foil, strip, of polyethylene terephthalate (PET), not reinforced, etc., of a thickness > 0.35 mm | kg | Heavy-gauge PET sheets. Used for heavy-duty industrial labels, membrane switch overlays, and thermoformed label applications. Smaller volume but higher value. |

### A3.4 PVC (Polyvinyl Chloride) Films

**Applications in label industry**: PVC face stocks for conformable/contour-cut labels (wine bottles, cosmetics), graphic/signage films (vehicle wraps, outdoor advertising), and shrink sleeves.

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.21.30.35** | Plates, sheets, film, foil and strip, of polymers of vinyl chloride, containing >= 6% of plasticisers (flexible PVC), thickness <= 1 mm | kg | **KEY CODE for flexible PVC films.** Covers conformable label face stocks (PVC is still preferred for complex curves — wine bottles, cosmetics), graphic films (cast and calendered vinyl for vehicle wraps, signage), and Avery Dennison's Graphics Solutions division products. PVC is under increasing regulatory and brand-owner pressure due to recyclability concerns, driving substitution to PP and PE. |
| **22.21.30.36** | Flexible PVC film, thickness > 1 mm | kg | Thicker flexible PVC sheets. Niche applications. |
| **22.21.30.37** | Rigid/semi-rigid PVC film (< 6% plasticiser), thickness <= 1 mm | kg | Rigid PVC films used in blister packaging, which receives printed labels. |
| **22.21.30.38** | Rigid PVC film, thickness > 1 mm | kg | Thicker rigid PVC sheets. |

### A3.5 Other Specialty Films

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.21.30.59** | Acrylic polymer films (non-cellular, not reinforced) | kg | Acrylic films for overlaminates, specialty transparent face stocks, and UV-resistant label constructions. |
| **22.21.30.61** | Polycarbonate films (non-cellular) | kg | Polycarbonate films for extremely durable labels in harsh environments (automotive engine compartment, electronics, outdoor). |
| **22.21.30.69** | Other polyester films (excl. PET, polycarbonate, unsaturated polyesters) | kg | PEN (polyethylene naphthalate), PBT films — specialty high-performance label substrates. |
| **22.21.30.82** | Polyamide (nylon) films (non-cellular) | kg | Nylon films used in flexible packaging labels, retort pouch labels, and high-barrier constructions. |
| **22.21.30.90** | Other plates, sheets, film, foil and strip, of non-cellular plastics, n.e.c. | kg | Catch-all for any plastic film not classified elsewhere (includes newer bio-based films, TPU films, etc.). |
| **22.21.41.50** | Plates, sheets, film, foil and strip, of cellular polyurethane | kg | Foam base material for foam tapes and foam-backed labels (mounting tapes, cushioning labels). |
| **22.21.42.30** | Non-cellular plates/sheets of condensation polymerisation products (polyesters), reinforced, laminated, supported | kg | Laminated polyester films — multi-layer label constructions with enhanced barrier/strength. |

---

## A4. RELEASE LINER PAPERS — THE HIDDEN VALUE CHAIN

Release liners are the silicone-coated backing papers/films that protect the adhesive until the label is applied. The release liner is a critical component of the labelstock construction and represents a significant portion of material cost. Understanding liner production helps assess supply chain dynamics.

### A4.1 Glassine & Specialty Transparent Papers

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.12.60.00** | Vegetable parchment, greaseproof papers, tracing papers and glassine and other glazed transparent or translucent papers, in rolls or sheets | kg | **CRITICAL CODE.** This includes **glassine paper**, which is THE dominant release liner base paper in the European label industry. Glassine is a supercalendered, dense, smooth paper ideal for silicone coating. Major glassine producers: Ahlstrom-Munksjo (now Ahlstrom), Delfort, Glatfelter (now Magnera), Sappi, Cham Paper. Also captures supercalendered kraft (SCK) papers used for machine-direction oriented (MDO) liners. The glassine/SCK supply base is concentrated among a few producers — understanding production volumes is essential for supply chain risk management. |

### A4.2 Kraft Papers (Liner Base Substrates)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.12.41.60** | Uncoated kraft paper and paperboard, weight <= 150 g/m2 (excl. kraftliner, sack kraft, graphic purposes) | kg | Kraft base papers used as substrates for clay-coated kraft (CCK) and supercalendered kraft (SCK) release liners. CCK liners are the dominant liner type in North America and growing in Europe. SCK is produced by calendering kraft paper to high smoothness. |
| **17.12.74.00** | Kraft paper (other than for writing/printing/graphic purposes), coated on one or both sides with kaolin or other inorganic substances, in rolls or sheets | kg | **Clay-coated kraft (CCK) release liner base.** CCK liners are coated with a clay (kaolin) layer before silicone application. They offer good dimensional stability and are common in VIP (variable information printing) label applications. CCK is the primary liner type for thermal labels. |
| **17.12.75.00** | Kraft paperboard (other than for writing/printing/graphic purposes), coated with kaolin or other inorganic substances | kg | Heavier-weight CCK grades used for thicker label constructions and specialty applications. |

### A4.3 Poly-Coated & Plastic-Laminated Papers

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.12.77.55** | Bleached paper and paperboard in rolls or sheets, coated, impregnated or covered with plastics, weight > 150 g/m2 (excl. adhesives) | kg | **Poly-coated kraft (PCK) release liner.** PCK liners have a polyethylene (PE) coating applied before silicone treatment. PCK liners are used for high-speed die-cutting, matrix stripping applications, and when higher moisture resistance is needed. Also covers poly-coated release papers for tape and industrial applications. |
| **17.12.77.59** | Paper and paperboard in rolls or sheets, coated, impregnated or covered with plastics (excl. adhesives, bleached > 150 g/m2) | kg | Other plastic-coated papers — includes additional polyolefin-coated release papers and barrier papers. |
| **17.12.77.70** | Paper and paperboard in rolls or sheets, coated, impregnated or covered with wax, paraffin wax, stearin, oil or glycerol | kg | Waxed papers used as alternative release substrates in some tape and industrial applications. Declining technology. |
| **17.12.77.80** | Other paper, paperboard, cellulose wadding and webs of cellulose fibres, coated, impregnated, covered, surface-coloured, surface-decorated or printed, in rolls or sheets, n.e.c. | kg | Catch-all for specialty coated papers. **Silicone-coated release liners (after siliconization)** may be classified here when sold as a standalone product (not as part of an adhesive labelstock construction). Also covers other functional coatings. |

### A4.4 Summary of Liner Types vs. PRODCOM Codes

| Liner Type | Base Paper | PRODCOM Code | Key Characteristics |
|---|---|---|---|
| **Glassine** | Supercalendered woodfree | 17.12.60.00 | Smooth, dense, translucent. Dominant in Europe. Low cost. |
| **SCK** (Supercalendered Kraft) | Calendered kraft | 17.12.60.00 / 17.12.41.60 | Similar to glassine but kraft-based. Good tear strength. |
| **CCK** (Clay-Coated Kraft) | Kaolin-coated kraft | 17.12.74.00 | Clay-coated for smoothness. Dominant in thermal labels. |
| **PCK** (Poly-Coated Kraft) | PE-coated kraft | 17.12.77.55 | PE barrier. For high-speed/moisture-resistant applications. |
| **PET Liner** | PET film | 22.21.30.65 | Film-based liner. For "rapid roll", automated dispensing. Growing fast. |
| **PP Liner** | PP/BOPP film | 22.21.30.21 / 22.21.30.23 | Film-based alternative. Emerging for mono-material recycling. |

---

## A5. LABEL FACE STOCK PAPERS

Papers used as the printable face material of paper-based PSA labels.

### A5.1 Coated Papers (Primary Label Face Stocks)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.12.73.36** | Coated paper for photo-sensitive, heat-sensitive or electro-sensitive purposes, mechanical fibres <= 10%, weight <= 150 g/m2 | kg | **Thermal paper face stocks.** Direct thermal (DT) and thermal transfer (TT) papers for barcode labels, shipping labels, receipt labels, weighing scale labels. A fast-growing segment driven by e-commerce logistics. Major producers: Koehler, Mitsubishi HiTec Paper, Ricoh, Hansol Paper. |
| **17.12.73.60** | Lightweight coated paper for writing, printing or graphic purposes, mechanical fibres > 10% of total fibre weight | kg | Lightweight coated (LWC) papers. Can be used as label face stocks for economy/promotional labels. |
| **17.12.73.75** | Other coated paper for graphic purposes, mechanical fibres > 10%, in rolls | kg | Coated woodfree and mechanical papers in rolls — used as label face stocks for high-quality printed labels. |
| **17.12.73.79** | Other coated paper for graphic purposes, mechanical fibres > 10%, in sheets | kg | Same in sheet format — for sheet-fed label printing. |

### A5.2 Uncoated Papers

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.12.14.35** | Graphic paper, mechanical fibres <= 10%, weight 40-150 g/m2, in rolls | kg | Uncoated woodfree (WF) paper in rolls. Used for thermal transfer labels, matte-finish labels, and standard paper labels. |
| **17.12.14.39** | Graphic paper, mechanical fibres <= 10%, weight 40-150 g/m2, in sheets | kg | Same in sheet format. |
| **17.12.13.00** | Paper and paperboard used as a base for photo-sensitive, heat-sensitive or electro-sensitive paper; carbonising base paper; wallpaper base | kg | Base papers for thermal papers BEFORE coating. Upstream to thermal label face stocks. |
| **17.12.42.40** | Other uncoated paper, <= 150 g/m2 | kg | Various uncoated papers used as face stock bases. |
| **17.12.42.60** | Other uncoated paper, 150-225 g/m2 | kg | Medium-weight face stock papers for thicker labels. |
| **17.12.42.80** | Other uncoated paper, >= 225 g/m2 | kg | Board-weight papers for heavy/rigid label constructions. |

---

## A6. SILICONES — RELEASE COATING CHEMISTRY

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.16.57.00** | Silicones, in primary forms | kg | **CRITICAL UPSTREAM CODE.** Silicone is the release agent coated onto liner substrates to enable clean label release from the liner. The silicone release coating market is an oligopoly: Dow (Dow Silicones), Wacker Chemie, Momentive, Shin-Etsu, Elkem Silicones control the vast majority of supply. Tracking silicone production/trade is essential for supply chain security and cost forecasting. Includes all forms: silicone fluids, silicone emulsions, silicone resins, and crosslinkers. |

---

## A7. POLYMER RESINS — UPSTREAM RAW MATERIALS

These codes track the raw material inputs for films, adhesives, and coatings.

### A7.1 Polyolefin Resins (for PE & PP Films)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.16.10.35** | Linear polyethylene (LLDPE), specific gravity < 0.94, primary forms | kg | LLDPE resin — primary raw material for PE films (label face stocks, stretch films). |
| **20.16.10.39** | Polyethylene (LDPE), specific gravity < 0.94, primary forms (excl. linear) | kg | LDPE resin — raw material for PE films and PE coating of release liners (PCK). |
| **20.16.10.50** | Polyethylene (HDPE), specific gravity >= 0.94, primary forms | kg | HDPE resin — for HDPE films (rigid container labels). |
| **20.16.10.70** | Ethylene-vinyl acetate copolymers (EVA), primary forms | kg | EVA copolymer — KEY raw material for hot-melt adhesive formulations (HMA). EVA-based hot-melts are widely used in packaging, bookbinding, and some PSA applications. |
| **20.16.51.30** | Polypropylene, primary forms | kg | PP resin — raw material for BOPP/OPP/cast PP film production. Price fluctuations directly impact filmic label costs. |

### A7.2 Polyester Resins (for PET Films)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.16.40.62** | Polyethylene terephthalate (PET), viscosity number >= 78 ml/g, primary forms | kg | Film-grade PET resin — raw material for PET film production (label face stocks + PET liners). |
| **20.16.40.64** | Other polyethylene terephthalate (PET), primary forms | kg | Other PET grades (bottle-grade PET, fiber-grade). Provides context on overall PET market. |

### A7.3 Acrylic & Other Adhesive Resins

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.16.53.90** | Acrylic polymers (excl. polymethyl methacrylate), primary forms | kg | **KEY CODE.** Acrylic polymer resins are the BASE for acrylic pressure-sensitive adhesives — the DOMINANT adhesive chemistry in the label industry. Acrylic PSA offers superior UV resistance, aging characteristics, and food-contact compliance vs. rubber PSA. Tracking acrylic resin supply helps forecast PSA raw material availability and costs. |
| **20.16.53.50** | Polymethyl methacrylate (PMMA), primary forms | kg | PMMA resin — used in certain specialty coating and adhesive formulations. |
| **20.16.52.30** | Polymers of vinyl acetate, in aqueous dispersion, primary forms | kg | PVAc dispersions — base for water-based emulsion adhesives used in label lamination and some wet-glue formulations. |
| **20.16.56.50** | Urea resins and thiourea resins, primary forms | kg | Used in certain adhesive crosslinker formulations. |
| **20.16.56.70** | Polyurethanes, primary forms | kg | PU resins — used in polyurethane adhesives, protective coatings, and PU-based PSA (specialty applications). |
| **20.16.40.50** | Alkyd resins, primary forms | kg | Used in certain ink and coating formulations for label printing. |

---

## A8. PRINTING INKS & COATINGS

Inks and coatings applied during the label converting/printing process.

### A8.1 Printing Inks

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.30.24.50** | Black printing inks | kg | Black inks for label printing (flexo, offset, letterpress, gravure, digital). |
| **20.30.24.70** | Printing inks (excluding black) | kg | **PRIMARY INK CODE.** Covers ALL colour printing inks used in label printing: flexographic inks (dominant for labels), offset/lithographic inks, UV-curable inks, water-based inks, energy-curable (EB) inks, digital inkjet inks, gravure inks. The label printing ink market is an indicator of label converting activity. Major ink suppliers: Sun Chemical, Flint Group, Siegwerk, Toyo Ink, hubergroup. |

### A8.2 Coatings, Varnishes & Embellishment

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **20.30.22.30** | Stamping foils | kg | Hot stamping foils for label embellishment — metallic, holographic, pigment foils for premium label finishing (wine, spirits, cosmetics). Major producers: KURZ, API Group. |
| **20.30.11.50** | Paints and varnishes based on acrylic or vinyl polymers, aqueous medium | kg | Water-based overprint varnishes (OPV) for label protection and finish. |
| **20.30.12.50** | Other paints and varnishes based on acrylic or vinyl polymers | kg | UV-curable and other specialty varnishes for label overcoating — high-gloss, matte, soft-touch finishes. |
| **20.30.12.90** | Other paints and varnishes based on synthetic polymers, n.e.c. | kg | Other specialty coatings for label applications (silicone coatings, functional coatings). |
| **20.59.30.00** | Inks (excluding printing ink) | kg | Non-printing inks — marker inks, stamp pad inks, coding inks used in label-adjacent applications. |

---

## A9. PACKAGING END-USE — DOWNSTREAM DEMAND DRIVERS

Labels are applied TO packaging. Tracking packaging production provides leading indicators of label demand.

### A9.1 Plastic Packaging (Primary Label End-Use)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **22.22.14.50** | Plastic bottles and similar articles, capacity <= 2 litres | pcs/kg | **MAJOR label end-use.** Plastic bottles for beverages, personal care, household chemicals are the #1 application for PSA labels. Trends in plastic bottle production directly drive label demand. |
| **22.22.14.70** | Plastic bottles, capacity > 2 litres | pcs/kg | Larger containers — industrial, automotive, cleaning product labels. |
| **22.22.13.00** | Plastic boxes, cases, crates | kg | Rigid plastic containers receiving PSA labels. |
| **22.22.19.25** | Plastic stoppers, lids, caps, capsules | kg | Closures — sometimes receive tamper-evident PSA labels/seals. |
| **22.22.11.00** | Sacks and bags of polymers of ethylene (PE) | kg | PE bags — food packaging receiving PSA labels. |

### A9.2 Paper & Board Packaging

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **17.21.14.00** | Folding cartons, boxes, cases of non-corrugated paper/paperboard | kg | Folding cartons — major end-use for PSA labels (food, pharma, cosmetics). |
| **17.21.13.00** | Corrugated paper/paperboard boxes and cases | kg | Corrugated shipping cases — receive shipping/logistics PSA labels. E-commerce growth drives demand. |
| **17.21.15.30** | Other packaging containers of paper/paperboard, n.e.c. | kg | Other paper packaging requiring labels. |

### A9.3 Glass Packaging

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **23.13.11.30** | Glass bottles for beverages, food products | pcs | Glass bottles for wine, spirits, beer, food — a key end-use for PSA labels (especially wine and spirits). |
| **23.13.11.50** | Jars and pots of glass | pcs | Glass jars for food — receive PSA labels. |

---

## A10. LABELLING & CONVERTING MACHINERY

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **28.29.21.50** | Machinery for filling, closing, sealing, capsuling or labelling bottles, cans, boxes, bags or other containers; machinery for aerating beverages | EUR/pcs | Labelling machinery production — indicates investment in label application capacity. Growth in labelling machine production = growth in label demand. Major producers: Krones, Sidel, HERMA, P.E. Labellers. |
| **28.29.21.80** | Machinery for packing or wrapping (excl. filling/closing/labelling) | EUR/pcs | Packaging machinery — context for overall packaging automation investment. |

### A10.1 Printing Machinery (Label Presses)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **28.99.12.50** | Flexographic printing machinery | EUR/pcs | Flexo presses are the dominant printing technology for PSA labels. Investment in flexo presses indicates label converter capacity expansion. Major press manufacturers: BOBST, Mark Andy, Nilpeter, Gallus (Heidelberg). |
| **28.99.12.70** | Other printing machinery (excl. offset, flexo) | EUR/pcs | Includes digital label presses (HP Indigo, Xeikon, Domino, Durst) and gravure presses. Digital press investment is a key indicator of the shift to short-run label production. |

---

## A11. TEXTILE LABELS & RFID (Adjacent Markets)

| PRODCOM Code | Description | Unit | Why It Matters |
|---|---|---|---|
| **13.96.17.50** | Labels, badges and similar articles in textile materials (excl. embroidered) | EUR/pcs | Woven/printed textile labels — adjacent to paper/film PSA labels. Avery Dennison has a significant RBIS (Retail Branding & Information Solutions) division serving this market. |
| **26.11.40.30** | Electronic integrated circuits — smart cards, RFID chips | EUR/pcs | RFID/NFC chips integrated into smart labels and inlays — a major growth segment for Avery Dennison's Intelligent Labels division. |

---

# PART B — COMEXT: INTERNATIONAL TRADE BY CN/HS CODE

**What is COMEXT?**
COMEXT is Eurostat's reference database for international trade in goods. It provides detailed monthly/annual import and export statistics by product (CN 8-digit code), declaring country, and partner country. Data includes:
- **Trade value** (in EUR)
- **Trade quantity** (in kg, m2, units, etc.)
- **Number of statistical items**

**Primary Dataset**: `DS-045409` (monthly data by CN8 code, partner country)

**Access**: https://ec.europa.eu/eurostat/comext/newxtweb/

**Time coverage**: 1988–present (monthly)

**Why trade data matters**: Combined with PRODCOM production data, trade data enables calculation of **Apparent Consumption** (= Production + Imports - Exports), which is the best proxy for actual market demand in each EU country.

---

## B1. SELF-ADHESIVE PLASTICS (HS Chapter 39, Heading 3919)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3919 10 10** | Self-adhesive plates, sheets, film, foil, tape, strip, of plastics, in rolls of width <= 20 cm, width <= 20 cm | Narrow PSA tape/label rolls (standard label rolls for application) |
| **3919 10 80** | Self-adhesive plates, sheets, film, foil, tape, strip, of plastics, in rolls of width <= 20 cm, other | Other narrow PSA products |
| **3919 90 10** | Self-adhesive plates, sheets, film, foil, strip, of plastics (excl. in rolls <= 20 cm), of condensation or rearrangement polymerisation products | Wide PSA films from polyester, polyurethane, polycarbonate base — covers PET-based labelstock, PET graphic films |
| **3919 90 20** | Self-adhesive plates, sheets, film, foil, strip, of plastics (excl. in rolls <= 20 cm), of addition polymerisation products | Wide PSA films from PE, PP, PVC base — covers BOPP-based labelstock, PE labelstock, PVC graphic films |
| **3919 90 80** | Self-adhesive plates, sheets, film, foil, strip, of plastics (excl. in rolls <= 20 cm), other | Other wide PSA products — **KEY CATCH-ALL** for labelstock exports/imports |

---

## B2. SELF-ADHESIVE PAPER & PAPERBOARD (HS Chapter 48, Heading 4811)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **4811 41 00** | Self-adhesive paper and paperboard | **CRITICAL CODE.** Directly corresponds to paper PSA labelstock (face paper + adhesive + release liner). All imports/exports of paper-based PSA labelstock are captured here. |
| **4811 49 00** | Gummed or adhesive paper and paperboard (excl. self-adhesive) | Wet-gummed paper — competing technology |

---

## B3. LABELS OF PAPER & PAPERBOARD (HS Chapter 48, Heading 4821)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **4821 10 10** | Self-adhesive printed labels of paper or paperboard | Finished printed PSA labels — **TRACKS CONVERTED LABEL TRADE** |
| **4821 10 90** | Other printed labels of paper or paperboard (excl. self-adhesive) | Non-PSA printed labels (wet-glue, shrink) |
| **4821 90 10** | Self-adhesive labels of paper or paperboard (unprinted) | Blank PSA labels — thermal/shipping labels |
| **4821 90 90** | Other labels of paper or paperboard (unprinted, excl. self-adhesive) | Blank non-PSA labels |

---

## B4. PLASTIC FILMS (HS Chapter 39, Heading 3920)

### B4.1 PE Films

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3920 10 23** | PE film, SG < 0.94, thickness <= 0.025 mm, not printed | Thin LDPE/LLDPE films |
| **3920 10 24** | PE film, SG < 0.94, thickness > 0.025 mm but <= 0.05 mm | Medium LDPE films |
| **3920 10 25** | PE film, SG < 0.94, thickness > 0.05 mm | Thicker LDPE films — label face stock gauge range |
| **3920 10 28** | Other PE film, SG < 0.94 | Other LDPE/LLDPE films |
| **3920 10 40** | PE film, SG >= 0.94, thickness < 0.021 mm | Thin HDPE films |
| **3920 10 81** | PE film, SG >= 0.94, thickness >= 0.021 mm but <= 0.160 mm | Standard HDPE films |
| **3920 10 89** | Other PE film, SG >= 0.94 | Other HDPE films |

### B4.2 PP Films (BOPP)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3920 20 21** | Biaxially oriented PP (BOPP) film, thickness <= 0.10 mm | **CRITICAL CODE.** BOPP film trade — directly tracks the supply/demand for the #1 filmic label face stock. |
| **3920 20 29** | Other PP film (cast, OPP), thickness <= 0.10 mm | Cast PP and non-oriented PP films |
| **3920 20 80** | PP film, thickness > 0.10 mm | Thicker PP films |

### B4.3 PVC Films

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3920 43 10** | Flexible PVC film (>= 6% plasticiser), not supported, not printed | Flexible PVC label/graphic film |
| **3920 43 90** | Other flexible PVC film | Other flexible PVC |
| **3920 49 10** | Rigid PVC film, thickness > 1 mm | Thick rigid PVC |
| **3920 49 90** | Other rigid PVC film | Thin rigid PVC |

### B4.4 PET Films

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3920 62 10** | PET film, thickness <= 0.025 mm | Thin PET — ultrathin liner films, capacitor films |
| **3920 62 19** | PET film, thickness > 0.025 mm but <= 0.35 mm | **CRITICAL CODE.** Standard PET films for labels and liners — this is the primary trade code for PET label face stock and PET release liner film. |
| **3920 62 90** | PET film, thickness > 0.35 mm | Heavy PET sheets |

### B4.5 Other Films

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3920 61 00** | Polycarbonate film | Durable label substrates |
| **3920 69 00** | Other polyester film (PEN, PBT, etc.) | Specialty polyester labels |
| **3920 99 28** | Polyimide film | High-temp labels (electronics, automotive) |
| **3920 99 59** | Other plastic film, n.e.c. | Catch-all |

---

## B5. ADHESIVES (HS Chapter 35, Heading 3506)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3506 10 00** | Products for use as glues/adhesives, retail sale, net weight <= 1 kg | Retail adhesives — small format |
| **3506 91 10** | Adhesives based on polymers of headings 3901-3913, in aqueous dispersion | Water-based synthetic adhesives — covers water-based PSA emulsions, PVAc adhesives, water-based laminating adhesives. Important for tracking the shift to water-based PSA technology. |
| **3506 91 90** | Other adhesives based on polymers of headings 3901-3913 or on rubber | **CRITICAL CODE.** Covers ALL other synthetic adhesives: solvent-based PSA, hot-melt adhesives, UV-curable adhesives, solvent-based rubber PSA, acrylic PSA (non-aqueous), structural adhesives. This is the broadest trade code for industrial adhesives. |
| **3506 99 00** | Other prepared glues and other prepared adhesives, n.e.c. | Other adhesives not classified above |

---

## B6. SILICONES (HS Chapter 39, Heading 3910)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3910 00 00** | Silicones in primary forms | **CRITICAL CODE.** All silicone trade — release coating silicones, silicone sealants, silicone fluids, silicone rubber. Track imports from non-EU producers (Shin-Etsu Japan, Dow USA, KCC Korea) and intra-EU trade (Wacker Germany, Elkem Norway). |

---

## B7. GLASSINE & RELEASE LINER PAPERS (HS Chapter 48, Heading 4806)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **4806 40 10** | Glassine papers in rolls or sheets | **CRITICAL CODE.** Trade in glassine paper — the primary release liner base. Track imports from major glassine mills (Finland, Sweden, Germany, Brazil). |
| **4806 40 90** | Other glazed transparent or translucent papers | Other specialty transparent papers for liners |

---

## B8. PRINTING INKS (HS Chapter 32, Heading 3215)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3215 11 00** | Black printing ink | Black inks for labels |
| **3215 19 00** | Other printing ink | Colour inks for labels — all technologies |
| **3215 90 00** | Other ink (excl. printing) | Coding/marking inks |

---

## B9. RFID / SMART LABELS (HS Chapter 85)

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **8523 52 10** | Smart cards (with electronic integrated circuit) | Smart card inlays — related to RFID label technology |
| **8523 59 10** | RFID tags, inlays, proximity cards | **KEY CODE.** RFID smart label inlays — Avery Dennison's Intelligent Labels division is the global leader. Track trade flows in RFID inlays/tags. |
| **8523 59 90** | Other semiconductor media | Other smart label components |

---

## B10. STAMPING FOILS & SPECIALTY MATERIALS

| CN8 Code | Description | Why It Matters |
|---|---|---|
| **3212 10 00** | Stamping foils | Hot stamping foils for label embellishment |
| **3506 91 10** | Water-based adhesives from synthetic polymers | Water-based adhesive systems (see B5) |

---

# PART C — HIGH-LEVEL TIME SERIES: INDUSTRY INDICES & STRUCTURAL DATA

## C1. SHORT-TERM STATISTICS (STS) — MONTHLY/QUARTERLY PRODUCTION & PRICE INDICES

These indices provide **timely, high-frequency** data on industrial activity across relevant NACE sectors. Filter by the following NACE codes:

| NACE Code | Description | Relevance to Avery Dennison |
|---|---|---|
| **C17** | Manufacture of paper and paper products | Paper labelstock, release liner papers, thermal papers |
| **C17.1** | Manufacture of pulp, paper and paperboard | Release liner base papers (glassine, kraft), label face papers |
| **C17.12** | Manufacture of paper and paperboard | Core paper/board production |
| **C17.2** | Manufacture of articles of paper and paperboard | Converted labels, self-adhesive paper products |
| **C17.29** | Manufacture of other articles of paper and paperboard | Finished labels (PSA and non-PSA) |
| **C18** | Printing and reproduction of recorded media | Label printing/converting activity |
| **C20** | Manufacture of chemicals and chemical products | Adhesives, silicones, polymer resins |
| **C20.3** | Manufacture of paints, varnishes, printing ink, mastics | Printing inks, overprint varnishes |
| **C20.52** | Manufacture of glues | Adhesive manufacturing |
| **C22** | Manufacture of rubber and plastic products | PSA tapes, plastic films, converted plastic products |
| **C22.2** | Manufacture of plastics products | Plastic label/film production |
| **C22.21** | Manufacture of plastic plates, sheets, tubes, profiles | Film extrusion (PE, PP, PET, PVC) |
| **C22.29** | Manufacture of other plastic products | PSA tapes and self-adhesive film products |
| **C28.29** | Manufacture of other general-purpose machinery, n.e.c. | Labelling machinery |

### C1.1 Production Volume

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sts_inpr_m** | Production in industry — monthly data | Monthly | Index (2021=100) | Track production volume trends for adhesives (C20.52), films (C22.21), paper (C17.1), labels (C17.29), tapes (C22.29). Seasonally adjusted and calendar adjusted series available. **ESSENTIAL for monitoring industry cycles.** |

### C1.2 Turnover (Revenue)

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sts_intv_m** | Turnover in industry — total | Monthly | Index (2021=100) | Industry revenue trends — domestic + export combined |
| **sts_intvd_m** | Turnover in industry — domestic market | Monthly | Index (2021=100) | Domestic market revenue. Track relative domestic vs. export revenue. |
| **sts_intvnd_m** | Turnover in industry — non-domestic market | Monthly | Index (2021=100) | Export revenue trends. Identifies export-oriented growth vs. domestic stagnation. |

### C1.3 Producer Prices (Selling Prices)

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sts_inpp_m** | Producer prices in industry — total | Monthly | Index (2021=100) | **CRITICAL for pricing analysis.** Output price trends for adhesives, films, paper, labels. Shows pricing power and competitive pressure. |
| **sts_inppd_m** | Producer prices — domestic market | Monthly | Index (2021=100) | Domestic selling prices — tracks local market pricing. |
| **sts_inppnd_m** | Producer prices — non-domestic market | Monthly | Index (2021=100) | Export selling prices — reveals competitive pricing pressure in export markets. |

### C1.4 Import Prices (Input Costs)

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sts_inpi_m** | Import prices in industry | Monthly | Index (2021=100) | **KEY for cost analysis.** Track import price trends for raw materials (polymer resins, silicones, base papers). Rising import prices signal cost pressure on labelstock manufacturing. |

### C1.5 New Orders (Demand Leading Indicator)

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sts_ordi_m** | New orders in industry | Monthly | Index (2021=100) | **Leading demand indicator.** New order intake for paper (C17), chemicals (C20), machinery (C28). Available for domestic and non-domestic orders. Order trends lead production by 1-3 months. |

### C1.6 Employment & Labour Input

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sts_inlb_m** | Labour input in industry | Monthly | Index (2021=100) | Hours worked in manufacturing sectors. Tracks capacity utilization through labour input. A declining labour index may signal automation investment or contraction. |
| **sts_inem_q** | Employment in industry | Quarterly | Index (2021=100) | Number of employees by NACE sector — structural employment trends. |

### C1.7 Business Confidence & Capacity Utilization

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **ei_bsin_q_r2** | Industry confidence / capacity utilization | Quarterly | % capacity utilization, confidence balance | **Capacity utilization rate** by broad industry groups. When capacity utilization > 85%, producers face supply constraints and may raise prices. |
| **ei_bssi_m_r2** | Industry confidence indicator | Monthly | Balance (s.a.) | Business expectations for production, order books, finished product stocks. A forward-looking sentiment indicator. |

---

## C2. STRUCTURAL BUSINESS STATISTICS (SBS) — ANNUAL MARKET STRUCTURE

SBS provides **detailed annual data** on the structure and performance of European industry at the NACE 4-digit level.

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **sbs_na_ind_r2** | Annual detailed enterprise statistics for industry | Annual | Number of enterprises, persons employed, turnover, production value, value added at factor cost, gross operating surplus, personnel costs, gross investment in tangible goods, apparent labour productivity | **ESSENTIAL FOR MARKET SIZING.** Provides the total turnover, number of enterprises, employment, and value added for each NACE 4-digit activity (C20.52 = Adhesives, C22.21 = Plastic films, C22.29 = Other plastic products, C17.12 = Paper/board, C17.29 = Other paper articles). This is the most reliable source for industry-level market sizing. |
| **sbs_sc_ind_r2** | Annual enterprise statistics by size class | Annual | Same variables, broken down by employment size class (0-9, 10-19, 20-49, 50-249, 250+) | **Market concentration analysis.** Shows whether the industry is dominated by large enterprises (like Avery Dennison, UPM Raflatac) or fragmented among SMEs. Reveals the competitive landscape structure. |
| **sbs_r_nuts06_r2** | SBS statistics at regional level (NUTS 2) | Annual | Turnover, employment, number of enterprises by NACE and NUTS 2 region | **Geographic mapping** of manufacturing clusters. Identifies where label/adhesive production is concentrated (e.g., North Rhine-Westphalia, Lombardy, Catalonia). |

---

## C3. FOREIGN AFFILIATES STATISTICS (FATS) — COMPETITIVE LANDSCAPE

FATS data reveals the role of **foreign-owned companies** in EU markets — essential for understanding the competitive position of US, Japanese, and other non-EU multinationals.

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **fats_g1a_08** | Inward FATS — Foreign-controlled enterprises in the EU | Annual | Number of enterprises, turnover, persons employed, value added, by controlling country and NACE | **COMPETITION INTELLIGENCE.** Shows the market share of US-controlled (Avery Dennison, 3M, Brady), Japanese-controlled (Lintec, Nitto Denko), and other foreign-controlled enterprises in EU adhesive/label/film/paper markets. Reveals import penetration via FDI. |
| **fats_out2_r2** | Outward FATS — EU enterprises abroad | Annual | Number of enterprises, turnover, employment abroad by host country and NACE | **Global footprint** of EU competitors (Henkel, UPM Raflatac, Fedrigoni, tesa) outside Europe. Shows their international expansion. |

---

## C4. BUSINESS DEMOGRAPHY — MARKET DYNAMICS

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **bd_9bd_sz_cl_r2** | Business demography by size class and NACE | Annual | Enterprise births, deaths, survival rates (1-5 year), birth rate, death rate | **Market consolidation tracking.** The label industry has undergone significant consolidation (Avery acquiring Mactac, Fedrigoni acquiring Ritrama/Acucote). Business demography data shows whether the rate of enterprise births exceeds deaths (fragmentation) or vice versa (consolidation). |
| **bd_9fh_sz_cl_r2** | High-growth enterprises | Annual | Number of high-growth enterprises (>10% annual employee growth for 3 years) by NACE and size class | **Identifies fast-growing competitors or acquisition targets.** Rapidly growing enterprises in NACE C22.29 or C17.29 may represent emerging competitors or M&A opportunities. |

---

## C5. R&D AND INNOVATION

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **rd_e_berdindr2** | Business enterprise R&D expenditure by NACE | Annual | Intramural R&D expenditure (million EUR), R&D personnel, by NACE 2-digit | **Innovation investment tracking.** R&D spending in C20 (chemicals), C22 (plastics), C17 (paper) indicates the pace of innovation in adhesive formulations, new film technologies, sustainable materials, digital printing. Avery Dennison's R&D spend can be benchmarked against sector averages. |
| **inn_cis_type** | Community Innovation Survey (CIS) by type of innovation | Biennial (~every 2 years) | Share of innovative enterprises, type of innovation (product, process, organizational, marketing), barriers to innovation | Innovation rates and types across relevant manufacturing sectors. Identifies whether the industry is product-innovation driven (new materials) or process-innovation driven (automation, digital printing). |

---

## C6. ENVIRONMENTAL / SUSTAINABILITY / PACKAGING WASTE

Sustainability is a **major strategic driver** in the label industry. The EU Packaging and Packaging Waste Regulation (PPWR) and Extended Producer Responsibility (EPR) schemes directly impact material choices for labels and liners.

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **env_waspac** | Packaging waste by waste management operations | Annual | Generated packaging waste, recycled, recovered, landfilled — by material type (paper/cardboard, plastic, glass, metal, wood) and by country | **REGULATORY DRIVER.** The EU PPWR mandates recycling targets by material type. Tracking packaging waste volumes by material helps forecast demand shifts (e.g., from PVC to PP labels, from paper-liner to PET-liner constructions that are easier to recycle). Also tracks the total volume of packaging entering the market. |
| **env_waspacr** | Recycling rates of packaging waste by material type | Annual | Recycling rate (%) for paper, plastic, glass, metal, wood packaging | **Compliance monitoring.** If recycling rates for plastic packaging are below targets, expect regulatory pressure on non-recyclable label constructions (multi-material constructions, PVC, certain adhesives). Drives demand for wash-off adhesives and recyclable face stocks. |
| **cei_wm020** | Recycling rate of packaging waste by type | Annual | Same as above, formatted for Circular Economy Indicators dashboard | Circular economy lens on the same data. |
| **cei_srm030** | Circular material use rate | Annual | % of material input from recycled materials | Overall circularity indicator — context for recycled content mandates affecting label materials. |
| **env_ac_ainah_r2** | Air emissions by NACE activity | Annual | CO2, N2O, CH4, SOx, NOx emissions by NACE sector | **ESG/Carbon reporting.** Scope 1 & 2 emissions intensity for chemical manufacturing (C20), paper manufacturing (C17), plastics (C22). Useful for Avery Dennison's Scope 3 emissions calculations and sustainability benchmarking. |
| **env_ac_mfa** | Material flow accounts (economy-wide) | Annual | Domestic extraction, imports, exports of biomass, metal ores, minerals, fossil fuels (tonnes) | Macro-level material demand trends. Contextualizes raw material availability for the label industry supply chain. |

---

## C7. ENERGY

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **nrg_bal_s** | Simplified energy balance | Annual | Energy consumption by fuel type and sector | Overall energy consumption for chemical/paper/plastic industries — cost driver and sustainability metric. |
| **nrg_d_indq_n** | Energy consumption in industry by NACE activity | Annual | Final energy consumption (TJ) by NACE 2-digit sector and fuel type | Detailed energy use for C17, C20, C22 — benchmark energy efficiency. Rising energy costs impact film extrusion, paper drying, and coating processes. |

---

## C8. NATIONAL ACCOUNTS & INPUT-OUTPUT TABLES — VALUE CHAIN ANALYSIS

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **nama_10_a64** | Gross value added and income by A*64 industry | Annual | Output, intermediate consumption, GVA, compensation of employees, gross operating surplus by NACE 2-digit | Macro-level industry performance. Compare GVA growth across paper (C17), chemicals (C20), plastics (C22). |
| **naio_10_cp1700** | Symmetric input-output table (product by product) | ~every 5 years | Inter-industry transaction matrix (EUR million) | **VALUE CHAIN MAPPING.** Shows how much output from "adhesives" (C20.52) is consumed by "plastic products" (C22.29) and "paper articles" (C17.29). Quantifies the supply chain linkages between adhesive producers, film producers, and label converters. |
| **naio_10_cp15** | Supply table at basic prices | Annual | Product supply by industry | Which industries produce which products — useful for understanding production overlap. |
| **naio_10_cp16** | Use table at purchasers' prices | Annual | Product use by industry | Which industries consume which products — tracks intermediate demand for adhesives, films, papers. |

---

## C9. LABOUR COSTS

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **lc_lci_r2_q** | Labour cost index by NACE | Quarterly | Labour cost index (wages & salaries, other labour costs) by NACE B-S | Wage inflation in manufacturing — a cost driver for label converting (labour-intensive process). Compare labour cost trends across countries to assess production location competitiveness. |
| **earn_ses_annual** | Structure of Earnings Survey | Annual | Mean/median hourly earnings by NACE and country | Absolute wage levels by sector and country — useful for site selection and benchmarking. |

---

## C10. INTERNATIONAL TRADE AGGREGATES — MACRO CONTEXT

| Dataset Code | Name | Frequency | Variables | Use Case |
|---|---|---|---|---|
| **ext_st_eu27_2020sitc** | EU trade by SITC product group | Monthly | Import/export values at SITC 1-5 digit level | High-level trade balance for chemicals, manufactured goods, machinery. |
| **bop_its6_det** | International trade in services by type | Annual | Trade in services (licensing, R&D, technical services) | Tracks cross-border service flows — relevant for licensing fees, technical assistance in label manufacturing. |

---

# PART D — DATA ACCESS, METHODOLOGY & MARKET SIZING

## D1. DATA ACCESS POINTS

| Resource | URL | Best For |
|---|---|---|
| **Eurostat Data Browser** | https://ec.europa.eu/eurostat/databrowser | STS indices, SBS, environmental, demographic datasets. Search by dataset code or keyword. |
| **Easy Comext** | https://ec.europa.eu/eurostat/comext/newxtweb/ | International trade data at CN8 level. Filter by CN code, country, period. Monthly granularity. |
| **PRODCOM Portal** | https://ec.europa.eu/eurostat/web/prodcom/database | PRODCOM production data. Annual, by EU country, by 8-digit PRODCOM code. |
| **Eurostat API (SDMX REST)** | https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/ | Programmatic access to STS, SBS, environmental datasets. JSON/XML output. |
| **Comext API** | https://ec.europa.eu/eurostat/api/comext/dissemination/ | Programmatic access to trade data (DS-prefixed datasets). |
| **Eurostat Bulk Download** | https://ec.europa.eu/eurostat/databrowser/bulk | Full dataset downloads in TSV/SDMX format. |
| **PRODCOM List (Classification)** | https://op.europa.eu/en/web/eu-vocabularies (search "PRODCOM") | Official PRODCOM product classification list (browse all codes). |
| **TARIC / CN Nomenclature** | https://taxation-customs.ec.europa.eu/customs-4/calculation-customs-duties/customs-tariff/eu-customs-tariff-taric_en | Official CN/HS code classification for trade data. |

---

## D2. MARKET SIZING METHODOLOGY

### D2.1 Apparent Consumption Formula

For any product code, the **European apparent consumption** (a proxy for market demand) is calculated as:

```
Apparent Consumption = Domestic Production (PRODCOM) + Imports (Comext) - Exports (Comext)
```

**Example — Self-Adhesive Paper Labelstock in Germany (2023)**:
- Production of 17.12.77.33 in Germany = X million EUR (from PRODCOM DS-059358)
- German imports of CN 4811.41.00 = Y million EUR (from Comext DS-045409)
- German exports of CN 4811.41.00 = Z million EUR (from Comext DS-045409)
- **Apparent Consumption = X + Y - Z**

### D2.2 PRODCOM ↔ CN Code Concordance

PRODCOM 8-digit codes and CN 8-digit codes are NOT identical but are linked through official concordance tables. For most codes, the mapping is 1:1 or 1:many.

| PRODCOM Code | Corresponding CN Code(s) | Product |
|---|---|---|
| 17.12.77.33 | 4811 41 00 | Self-adhesive paper |
| 22.29.21.40 | 3919 10 10, 3919 10 80 | Self-adhesive plastic strips <= 20 cm |
| 22.29.22.40 | 3919 90 10, 3919 90 20, 3919 90 80 | Self-adhesive plastic sheets > 20 cm |
| 17.29.11.20 | 4821 10 10 | Self-adhesive printed labels |
| 17.29.11.60 | 4821 90 10 | Self-adhesive unprinted labels |
| 22.21.30.21 | 3920 20 21 | BOPP film |
| 22.21.30.65 | 3920 62 10, 3920 62 19 | PET film <= 0.35 mm |
| 20.52.10.80 | 3506 91 10, 3506 91 90, 3506 99 00 | Prepared adhesives |
| 20.16.57.00 | 3910 00 00 | Silicones |
| 17.12.60.00 | 4806 40 10, 4806 40 90 | Glassine / transparent papers |

### D2.3 Geographic Coverage

- **EU-27** aggregate (post-Brexit, excl. UK)
- All **27 individual EU member states**
- EFTA countries (Norway, Switzerland, Iceland, Liechtenstein) partially covered in trade data
- UK data available pre-2021 in PRODCOM; post-2021 treated as non-EU trade partner in Comext

### D2.4 Time Coverage

| Data Source | Start Year | Frequency | Typical Lag |
|---|---|---|---|
| PRODCOM (DS-059358) | 1995 | Annual | ~18 months (e.g., 2023 data available mid-2025) |
| Comext (DS-045409) | 1988 | Monthly | ~2 months |
| STS (sts_inpr_m etc.) | 2000 | Monthly | ~2 months |
| SBS (sbs_na_ind_r2) | 2008 | Annual | ~24 months |

---

## D3. DATA QUALITY NOTES

1. **Confidentiality flags**: Some PRODCOM data is suppressed (flagged `:c`) when fewer than 3 enterprises produce a product in a country, to protect business confidentiality. This is common for specialized products like silicone-coated release papers.

2. **PRODCOM limitations**: PRODCOM reports production by establishments classified to a given NACE activity. If a labelstock manufacturer (NACE 22.29) also produces an adhesive (NACE 20.52), the adhesive production may or may not be reported under the correct PRODCOM code depending on how the establishment is classified.

3. **Trade data quality**: Intra-EU trade is reported via Intrastat surveys (above a reporting threshold that varies by country). Small intra-EU trade flows may be under-reported.

4. **STS indices are NOT absolute values**: They are index numbers (2021=100) showing relative changes over time. To convert to absolute values, combine with SBS annual turnover/production data.

5. **NACE Rev. 2 vs. Rev. 2.1**: A new NACE classification (Rev. 2.1) is being introduced from 2025 reference year. Some NACE codes may change. Monitor Eurostat announcements.

---

# PART E — PRIORITY MATRIX & RECOMMENDED WORKFLOW

## E1. PRIORITY TIERS

### TIER 1 — MUST HAVE (Core Market Monitoring)

**Update frequency: Monthly/Annual | Build first**

| # | Series | Code(s) | What It Answers |
|---|---|---|---|
| 1 | Self-adhesive plastic production (wide) | PRODCOM 22.29.22.40 | How much filmic PSA labelstock does Europe produce? |
| 2 | Self-adhesive plastic production (narrow) | PRODCOM 22.29.21.40 | How much converted PSA tape/label output? |
| 3 | Self-adhesive paper production | PRODCOM 17.12.77.33 | How much paper PSA labelstock? |
| 4 | Self-adhesive label production | PRODCOM 17.29.11.20, .60 | How many finished labels? |
| 5 | PSA plastic trade | CN 3919 (all) | Who imports/exports filmic PSA? From/to where? |
| 6 | PSA paper trade | CN 4811 41 00 | Who imports/exports paper PSA labelstock? |
| 7 | Label trade | CN 4821 10 10, 4821 90 10 | Who imports/exports finished labels? |
| 8 | Production index | sts_inpr_m (C17.2, C22.29) | Is label/tape production growing or declining? |
| 9 | Producer prices | sts_inpp_m (C17, C20, C22) | Are prices rising or falling? |
| 10 | SBS market sizing | sbs_na_ind_r2 (C17.29, C20.52, C22.29) | Total industry turnover, # enterprises, employment |

### TIER 2 — HIGH VALUE (Supply Chain & Cost Dynamics)

**Update frequency: Monthly/Annual | Build second**

| # | Series | Code(s) | What It Answers |
|---|---|---|---|
| 11 | BOPP film production/trade | PRODCOM 22.21.30.21 / CN 3920 20 21 | What is the supply position for BOPP label face stock? |
| 12 | PET film production/trade | PRODCOM 22.21.30.65 / CN 3920 62 19 | PET face stock + PET liner supply — rapid roll market? |
| 13 | PE film production/trade | PRODCOM 22.21.30.10 / CN 3920 10 xx | PE face stock supply? |
| 14 | PVC film production/trade | PRODCOM 22.21.30.35 / CN 3920 43 xx | PVC graphic film supply (declining)? |
| 15 | Glassine production/trade | PRODCOM 17.12.60.00 / CN 4806 40 10 | Release liner base paper supply? |
| 16 | Silicone production/trade | PRODCOM 20.16.57.00 / CN 3910 00 00 | Release coating silicone supply? |
| 17 | Adhesive production/trade | PRODCOM 20.52.10.80 / CN 3506 91 xx | Adhesive raw material supply? |
| 18 | Import prices | sts_inpi_m (C20, C22) | Are input costs rising? |
| 19 | New orders | sts_ordi_m (C17, C20) | Is demand accelerating? (Leading indicator) |
| 20 | Packaging waste/recycling | env_waspac, env_waspacr | Regulatory pressure on materials? |

### TIER 3 — STRATEGIC INTELLIGENCE (Competitive & Macro Context)

**Update frequency: Annual/Multi-year | Build third**

| # | Series | Code(s) | What It Answers |
|---|---|---|---|
| 21 | Foreign affiliates (inward) | fats_g1a_08 | What % of EU market is foreign-controlled? (Avery vs. EU competitors) |
| 22 | Business demography | bd_9bd_sz_cl_r2 | Is the industry consolidating? Birth/death rates? |
| 23 | High-growth enterprises | bd_9fh_sz_cl_r2 | Who are the fast-growing competitors? |
| 24 | R&D expenditure | rd_e_berdindr2 | How much does the industry invest in R&D? |
| 25 | Polymer resin production | PRODCOM 20.16.xx.xx | Upstream raw material supply? |
| 26 | Packaging end-use | PRODCOM 22.22.14.50, 17.21.14.00, 23.13.11.30 | Downstream demand from bottles, cartons, glass? |
| 27 | Labelling machinery | PRODCOM 28.29.21.50 | Investment in label application capacity? |
| 28 | Input-output tables | naio_10_cp1700 | Value chain inter-industry linkages? |
| 29 | Labour costs | lc_lci_r2_q | Wage inflation impact on converting costs? |
| 30 | Energy consumption | nrg_d_indq_n | Energy cost exposure by sector? |

---

## E2. RECOMMENDED WORKFLOW

```
STEP 1: Market Sizing (Annual)
├── Pull PRODCOM data for codes in Tier 1 (by country, by year)
├── Pull Comext trade data for corresponding CN codes (by country, partner, month)
├── Calculate Apparent Consumption = Production + Imports - Exports
└── Build market size estimates by product type and country

STEP 2: Trend Monitoring (Monthly)
├── Set up STS index tracking (production, turnover, prices)
├── Monitor monthly trade flows for early signals
├── Track capacity utilization and business confidence
└── Build rolling dashboards with YoY and MoM comparisons

STEP 3: Supply Chain Analysis (Quarterly)
├── Track upstream raw material production/trade (films, papers, silicones, resins)
├── Monitor import prices for cost pressure signals
├── Assess liner type evolution (glassine vs. CCK vs. PET liner)
└── Map geographic supply concentration risks

STEP 4: Competitive Intelligence (Annual)
├── Analyze FATS data for foreign vs. domestic market share
├── Track business demography for consolidation trends
├── Benchmark R&D spending against sector averages
└── Map value chain flows through input-output tables

STEP 5: Sustainability & Regulatory (Annual)
├── Monitor packaging waste and recycling rate trends
├── Track material-specific recycling compliance gaps
├── Assess energy intensity and carbon footprint by sector
└── Anticipate regulatory shifts (PPWR, EPR, recyclability mandates)
```

---

## E3. TOTAL CODE COUNT SUMMARY

| Category | PRODCOM Codes | CN/HS Codes | STS/SBS/Other Datasets |
|---|---|---|---|
| Self-adhesive products (core) | 8 | 12 | — |
| Adhesives | 2 | 4 | — |
| Plastic films (PE, PP, PET, PVC, other) | 17 | 24 | — |
| Release liner papers | 7 | 2 | — |
| Face stock papers | 10 | — | — |
| Silicones | 1 | 1 | — |
| Polymer resins | 11 | — | — |
| Printing inks & coatings | 7 | 3 | — |
| Packaging end-use | 10 | — | — |
| Labelling & printing machinery | 4 | — | — |
| RFID / Smart labels | 2 | 3 | — |
| Textile labels | 1 | — | — |
| **High-level time series** | — | — | **30+ datasets** |
| **TOTAL** | **~80** | **~49** | **30+** |

**Grand total: ~160 distinct statistical series** covering the full value chain from polymer resins to finished labels and end-use packaging.

---

*Prepared for Avery Dennison WU Headquarters — European Market Intelligence*
*Data sources: Eurostat PRODCOM, Comext, STS, SBS, FATS, Business Demography, Environmental Statistics*
