"""Build a CSV catalog of all monthly time series in the Eurostat project."""

import pandas as pd

# ── Descriptions & use-cases for the 14 STS datasets ────────────────────────

STS_META = {
    "sts_inpr_m": {
        "description": (
            "Production in industry – monthly data. This index measures the volume of industrial "
            "output (deflated turnover or physical quantities) for a given NACE sector and country. "
            "The base year is 2021 = 100. It covers manufacturing sub-sectors relevant to the "
            "pressure-sensitive materials value chain (paper, chemicals, plastics, printing) as well "
            "as downstream demand sectors (food, beverages, pharma, HPC). Available with seasonal "
            "adjustment variants (NSA, SA, SCA)."
        ),
        "use_case": (
            "Use this series to monitor the pace of manufacturing activity month-over-month. "
            "It serves as a coincident indicator of industrial health: rising production signals "
            "expanding demand for raw materials and labels. Compare across countries to identify "
            "regional divergences, or across NACE sectors to spot shifts in the supply-demand balance "
            "of the label industry. Particularly useful for benchmarking capacity utilisation and "
            "detecting turning points in the industrial cycle."
        ),
    },
    "sts_inpp_m": {
        "description": (
            "Producer prices in industry – total (domestic + non-domestic). This index tracks "
            "the evolution of ex-factory gate selling prices for industrial products, covering both "
            "domestic and export markets. Base year 2021 = 100. It captures price movements in the "
            "materials supply chain (paper, plastics, chemicals, adhesives) and in downstream consumer "
            "goods sectors."
        ),
        "use_case": (
            "Use this series to track input-cost inflation or deflation along the label value chain. "
            "Rising producer prices in paper (C17), chemicals (C20), or plastics (C22) signal margin "
            "pressure for label converters. Comparing total prices with domestic-only and non-domestic-only "
            "variants reveals whether pricing power differs between home and export markets. Essential for "
            "cost-pass-through analysis, pricing strategy, and margin forecasting."
        ),
    },
    "sts_inppd_m": {
        "description": (
            "Producer prices in industry – domestic market only. Same methodology as sts_inpp_m but "
            "restricted to goods sold within the reporting country. Base year 2021 = 100. Covers the "
            "same NACE sectors relevant to the label materials supply chain."
        ),
        "use_case": (
            "Use this series to isolate domestic pricing dynamics from export prices. It helps "
            "identify whether domestic buyers face different cost trajectories than export customers. "
            "When compared with the total and non-domestic variants, it reveals pricing segmentation "
            "and potential arbitrage between markets. Useful for domestic-focused label converters "
            "assessing their cost base."
        ),
    },
    "sts_inppnd_m": {
        "description": (
            "Producer prices in industry – non-domestic (export) market only. This index measures "
            "ex-factory prices for goods sold outside the reporting country. Base year 2021 = 100. "
            "Available for the same NACE sectors as the domestic variant."
        ),
        "use_case": (
            "Use this series to understand export pricing trends in the materials and downstream "
            "sectors. It captures the combined effect of competitive pressure, FX pass-through, and "
            "transport costs on export prices. Comparing with the domestic variant helps assess whether "
            "producers absorb or pass on cost increases differently across markets, which is critical "
            "for multinational label material suppliers."
        ),
    },
    "sts_inpi_m": {
        "description": (
            "Import prices in industry – monthly data. This index measures the price of goods "
            "imported by a country's industrial sector, classified by NACE activity of the buyer. "
            "Base year 2021 = 100. It is the largest dataset in the STS file, reflecting the breadth "
            "of import-dependent supply chains in Europe, especially for raw materials (plastics, "
            "chemicals, paper pulp) that feed label and packaging production."
        ),
        "use_case": (
            "Use this series to monitor the cost of imported raw materials and intermediates. "
            "Import prices capture FX effects, global commodity price swings, and trade-policy impacts "
            "(tariffs, quotas). For the label industry, rising import prices in plastics (C22) or "
            "chemicals (C20) are an early warning of margin compression. Cross-country comparison "
            "reveals which markets are more exposed to import-cost shocks. Combine with producer "
            "prices to compute implied margins."
        ),
    },
    "sts_intv_m": {
        "description": (
            "Turnover in industry – total (domestic + non-domestic). This index measures the "
            "evolution of total revenue (in current prices) for industrial enterprises, by NACE "
            "sector and country. Base year 2021 = 100. Unlike production indices, turnover reflects "
            "both volume and price effects."
        ),
        "use_case": (
            "Use this series to gauge the revenue trajectory of material suppliers and downstream "
            "manufacturers. Rising turnover indicates expanding demand in nominal terms. Combining "
            "turnover with production indices reveals whether growth is volume-driven or price-driven — "
            "a crucial distinction for strategic planning. Track domestic vs non-domestic splits to "
            "understand geographic demand allocation."
        ),
    },
    "sts_intvd_m": {
        "description": (
            "Turnover in industry – domestic market only. Measures revenue from goods sold within "
            "the reporting country. Base year 2021 = 100. Same NACE coverage as total turnover."
        ),
        "use_case": (
            "Use this series to assess the strength of domestic demand for industrial products. "
            "For label converters selling primarily in their home market, this is the most direct "
            "revenue proxy. Compare with non-domestic turnover to understand the export dependency "
            "of each sector and country."
        ),
    },
    "sts_intvnd_m": {
        "description": (
            "Turnover in industry – non-domestic (export) market only. Measures revenue from goods "
            "sold outside the reporting country. Base year 2021 = 100."
        ),
        "use_case": (
            "Use this series to track export revenue trends in the label materials and downstream "
            "sectors. It captures the combined effect of volume, pricing, and FX on export performance. "
            "Useful for assessing the international competitiveness of European producers and identifying "
            "which countries are gaining or losing export share."
        ),
    },
    "sts_inlb_m": {
        "description": (
            "Labour input in industry – monthly data. This index measures the total number of hours "
            "worked (or number of employees) in industrial enterprises, by NACE sector and country. "
            "Base year 2021 = 100. It is a direct indicator of capacity utilisation and employment "
            "conditions in the manufacturing sector."
        ),
        "use_case": (
            "Use this series to track the labour intensity of production and assess capacity "
            "constraints. Rising labour input alongside flat production may signal declining "
            "productivity, while falling labour input with stable production suggests efficiency gains "
            "or automation. Useful for workforce planning, cost analysis, and understanding the "
            "operating leverage of label material producers."
        ),
    },
    "sts_trtu_m": {
        "description": (
            "Retail trade turnover – monthly data. This index measures the volume (deflated) or "
            "value of retail sales, covering food retail, non-food retail, health/beauty retail, and "
            "total retail trade. Base year 2021 = 100. It tracks consumer-facing demand that ultimately "
            "drives label consumption (every product on a shelf needs a label)."
        ),
        "use_case": (
            "Use this series as a demand-pull indicator for the label industry. Retail turnover is "
            "the closest available proxy for the volume of labelled consumer goods moving through the "
            "supply chain. Track food vs non-food splits to understand which end-markets are driving "
            "label demand. Combine with production indices to assess the lag between manufacturing "
            "and retail sales."
        ),
    },
    "sts_sepr_m": {
        "description": (
            "Services production index – monthly data. This index measures the output volume of "
            "services sectors, including transportation (H49), warehousing (H52), and postal/courier "
            "services (H53). Base year 2021 = 100. These logistics sectors are essential for the "
            "physical distribution of labelled products."
        ),
        "use_case": (
            "Use this series to monitor the logistics and distribution infrastructure that underpins "
            "the label value chain. Rising services production in transport and warehousing indicates "
            "increasing throughput of goods — and therefore more labelling. It also serves as a "
            "cross-check on industrial production: if goods are being produced but logistics are "
            "contracting, inventory build-ups may be occurring."
        ),
    },
    "ei_bssi_m_r2": {
        "description": (
            "Industry confidence indicator – monthly survey data. This is a composite balance "
            "indicator derived from the European Commission's Business and Consumer Surveys, "
            "specifically the industry module. It combines assessments of order books, production "
            "expectations, and stocks of finished goods. Values above zero indicate optimism, below "
            "zero pessimism."
        ),
        "use_case": (
            "Use this series as a leading indicator of industrial activity — it typically leads "
            "hard data (production, turnover) by 1-3 months. Rising confidence signals upcoming "
            "production increases and demand for materials. Compare across countries to identify "
            "where the manufacturing cycle is turning. Particularly useful for short-term demand "
            "forecasting and early warning of downturns."
        ),
    },
    "ei_bsrt_m_r2": {
        "description": (
            "Retail trade confidence indicator – monthly survey data. A composite balance indicator "
            "from the European Commission's Business and Consumer Surveys, retail trade module. "
            "It combines assessments of recent business activity, stock levels, and business expectations. "
            "Values above zero indicate optimism."
        ),
        "use_case": (
            "Use this series as a leading indicator of retail sales trends. Retail confidence "
            "precedes actual retail turnover data and provides early signals of consumer demand "
            "shifts. For the label industry, declining retail confidence suggests downstream customers "
            "may reduce orders. Useful for demand planning and inventory management."
        ),
    },
    "ei_bsse_m_r2": {
        "description": (
            "Services confidence indicator – monthly survey data. A composite balance indicator "
            "from the European Commission's Business and Consumer Surveys, services module. "
            "It combines assessments of business climate, recent demand, and demand expectations. "
            "Values above zero indicate optimism."
        ),
        "use_case": (
            "Use this series as a leading indicator of services sector activity, especially "
            "logistics and distribution. Services confidence helps anticipate changes in transport "
            "volumes, warehousing demand, and overall supply chain throughput. Combine with the "
            "industry confidence indicator for a complete picture of the business cycle."
        ),
    },
}


# ── Descriptions & use-cases for the 56 COMEXT CN codes ─────────────────────

COMEXT_META = {
    # B1: Self-Adhesive Plastics
    "39191080": {
        "family": "B1 – Self-Adhesive Plastics",
        "description": (
            "Trade of self-adhesive plastic strips and films in rolls of width ≤ 20 cm (excluding "
            "those merely gummed). CN code 39191080. This product category covers the core pressure-"
            "sensitive labelstock material — the plastic face film coated with adhesive, supplied in "
            "narrow rolls for label converting. Monthly trade data includes import and export values "
            "(EUR) and quantities (100 kg) between EU member states and with the rest of the world, "
            "including China."
        ),
        "use_case": (
            "Use this series to track the intra-EU and extra-EU trade flows of narrow-web self-adhesive "
            "plastic films — the primary substrate for filmic labels. Rising imports may indicate "
            "domestic supply shortfalls or competitive pricing from outside the EU. Export trends "
            "reveal European competitiveness in this segment. Volume vs value comparison reveals "
            "price trends per unit weight. Essential for supply-demand balancing and trade flow analysis."
        ),
    },
    "39199020": {
        "family": "B1 – Self-Adhesive Plastics",
        "description": (
            "Trade of self-adhesive plastic sheets and films in rolls of width > 20 cm (CN 39199020). "
            "Covers wider-format self-adhesive plastic materials used in graphic arts, signage, and "
            "wide-web label applications."
        ),
        "use_case": (
            "Use this series to monitor trade in wider-format SA plastics, which complement the "
            "narrow-roll data. These materials serve different end-uses (large-format graphics, "
            "industrial labels) and help complete the picture of total self-adhesive plastic trade."
        ),
    },
    "39199080": {
        "family": "B1 – Self-Adhesive Plastics",
        "description": (
            "Trade of other self-adhesive plastic plates, sheets, film, foil, strip (CN 39199080). "
            "A catch-all category for SA plastic materials not classified elsewhere."
        ),
        "use_case": (
            "Use this series to capture residual self-adhesive plastic trade not covered by the "
            "more specific codes. Important for completeness when estimating total market size."
        ),
    },
    # B2: Self-Adhesive Paper
    "48114100": {
        "family": "B2 – Self-Adhesive Paper",
        "description": (
            "Trade of self-adhesive paper and paperboard (CN 48114100). This covers gummed or "
            "self-adhesive paper in rolls or sheets, the primary substrate for paper-based "
            "pressure-sensitive labels."
        ),
        "use_case": (
            "Use this series to track trade flows of the core paper labelstock material. Paper-based "
            "labels dominate food, beverage, and pharma labelling. Import/export trends reveal "
            "sourcing patterns and competitive dynamics between European paper mills and Asian imports."
        ),
    },
    "48114900": {
        "family": "B2 – Self-Adhesive Paper",
        "description": (
            "Trade of other self-adhesive paper and paperboard, not elsewhere specified (CN 48114900). "
            "Covers specialty SA papers and paperboards beyond the main category."
        ),
        "use_case": (
            "Use this series to capture specialty and niche SA paper trade not covered by 48114100. "
            "Includes coated, coloured, and specialty-finish SA papers used in premium labels."
        ),
    },
    # B3: Paper Labels
    "48211010": {
        "family": "B3 – Paper Labels",
        "description": (
            "Trade of printed paper labels (CN 48211010). Finished printed labels made of paper, "
            "ready for application. This is the direct output of the label converting industry."
        ),
        "use_case": (
            "Use this series to track the trade of finished label products. It directly measures "
            "the output of the label converting industry crossing borders. Rising exports indicate "
            "competitive European label converters; rising imports suggest domestic converters are "
            "losing share or that specialised labels are sourced from abroad."
        ),
    },
    "48211090": {
        "family": "B3 – Paper Labels",
        "description": (
            "Trade of other printed paper or paperboard labels (CN 48211090). Covers printed labels "
            "not classified under 48211010."
        ),
        "use_case": (
            "Use alongside 48211010 for a complete view of printed label trade. Includes specialty "
            "formats, multi-layer labels, and other printed label variants."
        ),
    },
    "48219010": {
        "family": "B3 – Paper Labels",
        "description": (
            "Trade of unprinted self-adhesive paper labels (CN 48219010). Blank SA paper labels "
            "that will be printed by the end-user (e.g., thermal transfer labels for logistics)."
        ),
        "use_case": (
            "Use this series to monitor trade in blank/unprinted SA labels, typically used in "
            "variable-information printing (barcodes, shipping labels, retail price labels). "
            "Growth indicates expanding logistics and retail labelling needs."
        ),
    },
    "48219090": {
        "family": "B3 – Paper Labels",
        "description": (
            "Trade of other unprinted paper labels (CN 48219090). Residual category for unprinted "
            "labels not classified elsewhere."
        ),
        "use_case": (
            "Use for completeness in estimating total unprinted label trade volumes alongside "
            "48219010."
        ),
    },
    # B4: Films – PE
    "39201023": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of polyethylene (PE) film, non-cellular, not reinforced, thickness ≤ 0.125 mm, "
            "of specific gravity < 0.94 (LDPE/LLDPE), biaxially oriented (CN 39201023). These "
            "oriented PE films are used as label face materials and flexible packaging."
        ),
        "use_case": (
            "Use to track biaxially oriented LDPE/LLDPE film trade — a key material for shrink "
            "sleeve labels and flexible packaging. Trade volumes indicate demand from the label "
            "and packaging converting industries."
        ),
    },
    "39201024": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of PE film, thickness ≤ 0.125 mm, specific gravity < 0.94, stretch film "
            "(CN 39201024). Stretch wrap films used in logistics and pallet wrapping."
        ),
        "use_case": (
            "Use to monitor stretch film trade — an indicator of logistics activity and goods "
            "movement. While not directly a label material, stretch film demand correlates with "
            "overall manufacturing and distribution throughput."
        ),
    },
    "39201025": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of PE film, thickness ≤ 0.125 mm, specific gravity < 0.94, other (CN 39201025). "
            "General-purpose LDPE/LLDPE films."
        ),
        "use_case": (
            "Use for overall LDPE film trade tracking. Serves as a proxy for flexible packaging "
            "and industrial film demand."
        ),
    },
    "39201028": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of PE film, thickness ≤ 0.125 mm, specific gravity < 0.94, other not elsewhere "
            "specified (CN 39201028)."
        ),
        "use_case": (
            "Residual PE film category. Use for completeness in total PE film market sizing."
        ),
    },
    "39201040": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of PE film, thickness ≤ 0.125 mm, specific gravity ≥ 0.94 (HDPE) (CN 39201040). "
            "High-density polyethylene films used in packaging and industrial applications."
        ),
        "use_case": (
            "Use to track HDPE film trade. HDPE films are used in stiffer packaging applications "
            "and some label constructions requiring higher rigidity and barrier properties."
        ),
    },
    "39201081": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of PE film, thickness > 0.125 mm, specific gravity < 0.94 (CN 39201081). "
            "Thicker LDPE sheets and films."
        ),
        "use_case": (
            "Use to monitor thicker PE film/sheet trade used in industrial packaging, construction, "
            "and agricultural applications."
        ),
    },
    "39201089": {
        "family": "B4 – Films (PE)",
        "description": (
            "Trade of PE film, thickness > 0.125 mm, specific gravity ≥ 0.94 (CN 39201089). "
            "Thicker HDPE sheets."
        ),
        "use_case": (
            "Use for completeness in PE film market analysis, covering thicker gauge HDPE products."
        ),
    },
    # B4: Films – PP
    "39202021": {
        "family": "B4 – Films (PP)",
        "description": (
            "Trade of biaxially oriented polypropylene (BOPP) film, thickness ≤ 0.10 mm "
            "(CN 39202021). BOPP is the dominant face material for filmic pressure-sensitive "
            "labels, especially in food, beverage, and HPC applications."
        ),
        "use_case": (
            "Use this series to track trade in BOPP films — the single most important filmic label "
            "material. BOPP labels are used on bottles, jars, and containers across all FMCG sectors. "
            "Trade volumes directly indicate label industry demand, while value trends reveal pricing "
            "dynamics in the BOPP film market."
        ),
    },
    "39202029": {
        "family": "B4 – Films (PP)",
        "description": (
            "Trade of other biaxially oriented PP film (CN 39202029). Includes specialty BOPP "
            "variants (metallised, matte, pearlised, cavitated)."
        ),
        "use_case": (
            "Use alongside 39202021 for total BOPP film trade. Specialty variants command premium "
            "prices and indicate demand for higher-value label constructions."
        ),
    },
    "39202080": {
        "family": "B4 – Films (PP)",
        "description": (
            "Trade of other (non-BOPP) polypropylene film and sheet (CN 39202080). Includes cast "
            "PP and other non-oriented PP films used in packaging and labels."
        ),
        "use_case": (
            "Use to complement BOPP data with non-oriented PP film trade. Cast PP is used in "
            "some label and packaging applications where biaxial orientation is not required."
        ),
    },
    # B4: Films – PVC
    "39204310": {
        "family": "B4 – Films (PVC)",
        "description": (
            "Trade of plasticised PVC film, containing ≥ 6% of plasticisers, non-cellular "
            "(CN 39204310). Flexible PVC films used in shrink sleeves and some label applications."
        ),
        "use_case": (
            "Use to track flexible PVC film trade — a material used in shrink sleeve labels and "
            "flexible packaging. PVC shrink sleeves are widely used in beverages and dairy."
        ),
    },
    "39204390": {
        "family": "B4 – Films (PVC)",
        "description": (
            "Trade of other plasticised PVC film (CN 39204390)."
        ),
        "use_case": (
            "Residual plasticised PVC film category. Use for completeness in PVC film market sizing."
        ),
    },
    "39204910": {
        "family": "B4 – Films (PVC)",
        "description": (
            "Trade of rigid (unplasticised) PVC film, thickness ≤ 1 mm (CN 39204910). Rigid "
            "PVC used in blister packs, thermoformed trays, and some label applications."
        ),
        "use_case": (
            "Use to monitor rigid PVC film trade — relevant for pharmaceutical blister packaging "
            "which requires labelling, and for rigid label applications."
        ),
    },
    "39204990": {
        "family": "B4 – Films (PVC)",
        "description": (
            "Trade of other rigid PVC film (CN 39204990)."
        ),
        "use_case": (
            "Residual rigid PVC category. Use for total PVC film market completeness."
        ),
    },
    # B4: Films – PET
    "39206219": {
        "family": "B4 – Films (PET)",
        "description": (
            "Trade of polyethylene terephthalate (PET) film, thickness ≤ 0.025 mm (CN 39206219). "
            "Thin PET films used as label face stock, overlaminates, and release liners."
        ),
        "use_case": (
            "Use to track thin PET film trade — a key material for high-clarity labels, "
            "overlaminates providing scratch/UV resistance, and some release liner constructions. "
            "PET labels are growing in beverage and personal care segments."
        ),
    },
    "39206290": {
        "family": "B4 – Films (PET)",
        "description": (
            "Trade of other PET film and sheet (CN 39206290). Covers thicker PET films and "
            "specialty grades."
        ),
        "use_case": (
            "Use alongside 39206219 for total PET film trade. Thicker PET is used in rigid "
            "packaging, electrical insulation, and industrial label applications."
        ),
    },
    # B4: Films – Other Polyester
    "39206100": {
        "family": "B4 – Films (Other Polyester)",
        "description": (
            "Trade of polycarbonate film and sheet (CN 39206100)."
        ),
        "use_case": (
            "Use for broader polyester/polycarbonate film market analysis. Polycarbonate has niche "
            "uses in durable labels and overlays."
        ),
    },
    "39206900": {
        "family": "B4 – Films (Other Polyester)",
        "description": (
            "Trade of other polyester film and sheet (CN 39206900). Includes PBT, PEN, and "
            "other specialty polyester films."
        ),
        "use_case": (
            "Use for completeness in polyester film market analysis. Specialty polyesters are "
            "used in high-performance label and packaging applications."
        ),
    },
    # B4: Films – Specialty
    "39209928": {
        "family": "B4 – Films (Specialty)",
        "description": (
            "Trade of polyimide film and sheet (CN 39209928). High-temperature-resistant film "
            "used in electronics, aerospace, and specialty industrial labels."
        ),
        "use_case": (
            "Use to track polyimide film trade — a niche but high-value material used for "
            "labels in extreme environments (electronics assembly, automotive, aerospace). "
            "Growth signals expanding high-tech manufacturing."
        ),
    },
    "39209959": {
        "family": "B4 – Films (Specialty)",
        "description": (
            "Trade of other plastic film and sheet, not elsewhere specified (CN 39209959). "
            "Catch-all for specialty films not covered by specific CN codes."
        ),
        "use_case": (
            "Use as a residual category for specialty films. Helps capture emerging materials "
            "and novel film types entering the market."
        ),
    },
    # B5: Adhesives
    "35061000": {
        "family": "B5 – Adhesives",
        "description": (
            "Trade of adhesives based on cyanoacrylates, in retail packages ≤ 1 kg "
            "(CN 35061000). Instant adhesives (superglues) with some niche label applications."
        ),
        "use_case": (
            "Use to track retail adhesive trade. While not a core label material, cyanoacrylate "
            "trade indicates broader adhesive market trends."
        ),
    },
    "35069110": {
        "family": "B5 – Adhesives",
        "description": (
            "Trade of adhesives based on rubber or plastics (including synthetic latex), "
            "in retail packages ≤ 1 kg (CN 35069110). Covers pressure-sensitive adhesive "
            "formulations at retail scale."
        ),
        "use_case": (
            "Use to track rubber/plastic-based adhesive trade in small formats. Includes PSA "
            "formulations used in label construction. Trade patterns indicate supply chain sourcing."
        ),
    },
    "35069190": {
        "family": "B5 – Adhesives",
        "description": (
            "Trade of adhesives based on rubber or plastics, in packages > 1 kg "
            "(CN 35069190). Bulk adhesive trade — the primary industrial format for PSA "
            "used in label manufacturing."
        ),
        "use_case": (
            "Use this series to track bulk PSA (pressure-sensitive adhesive) trade — the core "
            "adhesive input for label manufacturing. This is the most relevant adhesive CN code for "
            "the label industry. Volume trends directly indicate label production activity across Europe."
        ),
    },
    "35069900": {
        "family": "B5 – Adhesives",
        "description": (
            "Trade of other prepared adhesives not elsewhere specified (CN 35069900). Covers "
            "hot-melt, water-based, solvent-based, and UV-curable adhesives."
        ),
        "use_case": (
            "Use to complement rubber/plastic adhesive data. Includes hot-melt adhesives "
            "increasingly used in label converting as an alternative to traditional PSA."
        ),
    },
    # B6: Silicones
    "39100000": {
        "family": "B6 – Silicones",
        "description": (
            "Trade of silicones in primary forms (CN 39100000). Silicone fluids, resins, and "
            "elastomers used to manufacture release coatings for label liners. Release coatings "
            "are what allow the label to peel cleanly from its backing."
        ),
        "use_case": (
            "Use this series to monitor silicone trade — a critical input for release liner "
            "manufacturing. Silicone supply tightness directly impacts label production capacity. "
            "Price and volume trends signal the health of the release liner supply chain, which is "
            "one of the most concentrated segments of the label industry."
        ),
    },
    # B7: Glassine & Release Papers
    "48064010": {
        "family": "B7 – Glassine & Release Papers",
        "description": (
            "Trade of glassine paper (CN 48064010). Glassine is a smooth, glossy, greaseproof "
            "paper used as the primary release liner substrate in pressure-sensitive labelstock. "
            "It is siliconised to create the backing from which labels are dispensed."
        ),
        "use_case": (
            "Use this series to track glassine paper trade — the dominant release liner substrate. "
            "Glassine demand directly correlates with labelstock production volumes. Trade imbalances "
            "reveal sourcing dependencies (e.g., European converters importing from Asian mills). "
            "A key supply chain monitoring indicator."
        ),
    },
    "48064090": {
        "family": "B7 – Glassine & Release Papers",
        "description": (
            "Trade of other greaseproof papers (CN 48064090). Includes kraft-based and specialty "
            "release papers beyond standard glassine."
        ),
        "use_case": (
            "Use alongside glassine data for total release paper market sizing. Specialty release "
            "papers serve niche applications (thick labels, industrial tapes, medical products)."
        ),
    },
    # B8: Printing Inks
    "32151100": {
        "family": "B8 – Printing Inks",
        "description": (
            "Trade of black printing ink (CN 32151100). Covers all types of black ink used in "
            "printing, including flexographic and digital inks used in label printing."
        ),
        "use_case": (
            "Use to monitor black ink trade — an essential consumable in label printing. Trade "
            "volumes correlate with overall printing activity. Price trends reflect raw material "
            "costs (carbon black, resins, solvents)."
        ),
    },
    "32151900": {
        "family": "B8 – Printing Inks",
        "description": (
            "Trade of other (non-black) printing ink (CN 32151900). Covers colour inks "
            "(CMYK process colours, spot colours, metallic inks) used in label printing."
        ),
        "use_case": (
            "Use to track colour ink trade, which represents the majority of ink consumption in "
            "label printing. Growth in colour ink trade indicates rising demand for high-quality, "
            "multi-colour labels."
        ),
    },
    # B9: RFID / Smart Labels
    "85235910": {
        "family": "B9 – RFID / Smart Labels",
        "description": (
            "Trade of unrecorded smart cards (CN 85235910). Includes RFID inlays, NFC tags, "
            "and blank smart label components before encoding."
        ),
        "use_case": (
            "Use to track RFID/NFC inlay trade — the fastest-growing segment of the label "
            "industry. Smart labels enable item-level tracking in retail (RAIN RFID for apparel), "
            "supply chain visibility, and anti-counterfeiting. Rapidly growing trade volumes "
            "confirm the digital transformation of labelling."
        ),
    },
    "85235990": {
        "family": "B9 – RFID / Smart Labels",
        "description": (
            "Trade of other semiconductor media, smart cards, and smart labels (CN 85235990). "
            "Broader smart label and electronic identification category."
        ),
        "use_case": (
            "Use alongside 85235910 for total smart label market sizing. This broader category "
            "captures the full range of electronic identification products traded across borders."
        ),
    },
    # B10: Stamping Foils
    "32121000": {
        "family": "B10 – Stamping Foils",
        "description": (
            "Trade of stamping foils (CN 32121000). Metallic and holographic foils applied to "
            "labels and packaging via hot stamping or cold foil processes for decorative and "
            "security purposes."
        ),
        "use_case": (
            "Use to track stamping foil trade — an indicator of premium and security label demand. "
            "Stamping foils are used on wine labels, spirits, cosmetics, and anti-counterfeiting "
            "features. Growth indicates premiumisation trends in consumer goods."
        ),
    },
    # Demand-side: Beverages
    "2009": {
        "family": "Demand – Beverages (Juices)",
        "description": (
            "Trade of fruit juices and vegetable juices (CN 2009). Major labelled consumer product "
            "category in the beverage sector."
        ),
        "use_case": (
            "Use as a demand proxy for label consumption in the juice segment. Every juice container "
            "requires labelling. Trade volumes indicate cross-border movement of labelled products "
            "and reveal sourcing patterns in the European beverage industry."
        ),
    },
    "2201": {
        "family": "Demand – Beverages (Water)",
        "description": (
            "Trade of mineral and aerated waters (CN 2201). Bottled water is one of the highest-"
            "volume labelled product categories globally."
        ),
        "use_case": (
            "Use as a high-volume demand indicator for label consumption. Bottled water labelling "
            "is highly automated and price-sensitive, making it a bellwether for filmic label demand."
        ),
    },
    "2202": {
        "family": "Demand – Beverages (Soft Drinks)",
        "description": (
            "Trade of sweetened or flavoured waters and non-alcoholic beverages (CN 2202). "
            "Includes soft drinks, energy drinks, and flavoured waters."
        ),
        "use_case": (
            "Use as a demand indicator for label consumption in the soft drinks segment. This "
            "category drives significant shrink sleeve and wrap-around label demand."
        ),
    },
    "2203": {
        "family": "Demand – Beverages (Beer)",
        "description": (
            "Trade of beer made from malt (CN 2203). Beer labelling is one of the most demanding "
            "applications, requiring wet-strength adhesives and premium printing."
        ),
        "use_case": (
            "Use to track beer trade as a proxy for beer label demand. Beer labels are a premium "
            "segment with high decoration standards (embossing, foiling, metallised substrates)."
        ),
    },
    "2204": {
        "family": "Demand – Beverages (Wine)",
        "description": (
            "Trade of wine of fresh grapes (CN 2204). Wine labelling is a high-value segment "
            "with emphasis on premium aesthetics, textured papers, and brand differentiation."
        ),
        "use_case": (
            "Use to track wine trade as a proxy for premium label demand. Wine labels are among "
            "the highest-value per unit labels, driving demand for specialty papers, foils, and "
            "embossing. A key indicator of premiumisation in the label market."
        ),
    },
    "2208": {
        "family": "Demand – Beverages (Spirits)",
        "description": (
            "Trade of spirits (ethyl alcohol < 80%, liqueurs, other) (CN 2208). Premium spirits "
            "labelling demands high-end decoration and anti-counterfeiting features."
        ),
        "use_case": (
            "Use to track spirits trade as a proxy for ultra-premium label demand. Spirits labels "
            "are the most decorated segment, driving demand for foiling, embossing, multi-layer "
            "constructions, and anti-counterfeiting technologies."
        ),
    },
    # Demand-side: HPC / Cleaning
    "3304": {
        "family": "Demand – HPC (Cosmetics)",
        "description": (
            "Trade of beauty/make-up preparations and skincare products (CN 3304). A major end-"
            "market for filmic labels with high aesthetic requirements."
        ),
        "use_case": (
            "Use to track cosmetics trade as a demand proxy for premium filmic labels. The HPC "
            "sector is a key driver of clear-on-clear (no-label look) labels and digital printing "
            "adoption for short runs and personalisation."
        ),
    },
    "3305": {
        "family": "Demand – HPC (Hair Care)",
        "description": (
            "Trade of hair care preparations (shampoos, conditioners, styling) (CN 3305). "
            "High-volume label segment with squeeze-bottle and pump-dispenser applications."
        ),
        "use_case": (
            "Use to monitor hair care trade as a label demand indicator. Squeeze-resistant labels "
            "for hair care bottles drive demand for conformable filmic labels with high ink adhesion."
        ),
    },
    "3307": {
        "family": "Demand – HPC (Perfumery & Toiletries)",
        "description": (
            "Trade of perfumes, deodorants, bath preparations, and room perfuming products "
            "(CN 3307). Premium segment with high aesthetic and regulatory labelling requirements."
        ),
        "use_case": (
            "Use to track toiletries and perfumery trade as a demand proxy. This segment drives "
            "demand for specialised labels that withstand moisture (shower products) and chemical "
            "exposure (perfume alcohol)."
        ),
    },
    "3402": {
        "family": "Demand – HPC (Detergents)",
        "description": (
            "Trade of organic surface-active agents, washing and cleaning preparations "
            "(CN 3402). High-volume commodity segment for labels."
        ),
        "use_case": (
            "Use to monitor detergent and cleaning product trade as a label demand indicator. "
            "This is a volume-driven segment with large-format labels, often using shrink sleeves "
            "for 360° decoration."
        ),
    },
    # Demand-side: Pharmaceuticals
    "3004": {
        "family": "Demand – Pharmaceuticals",
        "description": (
            "Trade of medicaments in dosage form (CN 3004). Pharmaceutical labelling is a highly "
            "regulated segment requiring serialisation, tamper-evidence, multi-language panels, "
            "and Braille."
        ),
        "use_case": (
            "Use to track pharmaceutical product trade as a demand proxy for pharma labels. "
            "Pharma is one of the most stable and regulation-driven label end-markets. Growth in "
            "pharma trade correlates with increasing demand for booklet labels, peel-and-read labels, "
            "and serialised labels for track-and-trace compliance."
        ),
    },
    # Demand-side: Food
    "1602": {
        "family": "Demand – Food (Processed Meat)",
        "description": (
            "Trade of prepared or preserved meat and meat offal (CN 1602). Canned and processed "
            "meats requiring label printing with nutritional and regulatory information."
        ),
        "use_case": (
            "Use to track processed meat trade as a label demand indicator in the food segment. "
            "Labels for these products must comply with EU food contact and allergen regulations."
        ),
    },
    "1604": {
        "family": "Demand – Food (Processed Fish)",
        "description": (
            "Trade of prepared or preserved fish, caviar, and fish-based products (CN 1604). "
            "Canned fish is a high-volume labelling application."
        ),
        "use_case": (
            "Use to monitor canned fish trade as a label demand proxy. Canned fish drives "
            "demand for wrap-around paper labels with high-speed application capability."
        ),
    },
    "2005": {
        "family": "Demand – Food (Prepared Vegetables)",
        "description": (
            "Trade of prepared or preserved vegetables (not frozen, not in vinegar) (CN 2005). "
            "Canned vegetables are among the highest-volume labelled products in food retail."
        ),
        "use_case": (
            "Use to track canned vegetable trade as a high-volume label demand indicator. This "
            "segment is price-sensitive, driving demand for efficient, high-speed labelling "
            "solutions."
        ),
    },
    "2106": {
        "family": "Demand – Food (Food Preparations)",
        "description": (
            "Trade of food preparations not elsewhere specified (CN 2106). Includes supplements, "
            "protein powders, flavourings, and other processed food products."
        ),
        "use_case": (
            "Use to monitor specialty food product trade. This diverse category includes fast-"
            "growing segments like nutraceuticals and health foods, which drive demand for premium "
            "labelling with complex ingredient and health-claim information."
        ),
    },
}


def build_sts_catalog(sts_path: str) -> pd.DataFrame:
    """Build catalog rows from the STS dataset."""
    print("Reading sts.csv ...")
    df = pd.read_csv(sts_path, dtype=str)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    rows = []
    for ds, grp in df.groupby("dataset"):
        meta = STS_META.get(ds, {})
        desc_text = grp["dataset_description"].iloc[0] if "dataset_description" in grp.columns else ds

        nace_codes = sorted(grp["nace"].dropna().unique())
        nace_descs = sorted(grp["nace_description"].dropna().unique()) if "nace_description" in grp.columns else []
        countries = sorted(grp["country"].dropna().unique())
        s_adjs = sorted(grp["s_adj"].dropna().unique()) if "s_adj" in grp.columns else []
        units = sorted(grp["unit"].dropna().unique()) if "unit" in grp.columns else []
        dates = sorted(grp["date"].dropna().unique())
        sides = sorted(grp["side"].dropna().unique()) if "side" in grp.columns else []

        rows.append({
            "source": "sts (Eurostat Short-Term Statistics)",
            "series_code": ds,
            "series_name": desc_text,
            "side": ", ".join(sides),
            "granularity": "monthly",
            "date_range": f"{dates[0]} to {dates[-1]}" if dates else "",
            "n_observations": len(grp),
            "matrix_dimensions": "dataset × nace_sector × country × seasonal_adjustment × unit",
            "nace_or_cn_codes": ", ".join(nace_codes),
            "nace_or_cn_descriptions": "; ".join(nace_descs),
            "countries": ", ".join(countries),
            "seasonal_adjustments": ", ".join(s_adjs),
            "units": ", ".join(units),
            "product_family": "Industrial statistics",
            "description": meta.get("description", desc_text),
            "use_case": meta.get("use_case", ""),
        })

    return pd.DataFrame(rows)


def build_comext_catalog(comext_path: str) -> pd.DataFrame:
    """Build catalog rows from the COMEXT dataset."""
    print("Reading comext.csv ...")
    df = pd.read_csv(comext_path, dtype=str)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    rows = []
    for cn, grp in df.groupby("cn_code"):
        meta = COMEXT_META.get(str(cn), {})
        cn_desc = grp["cn_description"].iloc[0] if "cn_description" in grp.columns else str(cn)

        reporters = sorted(grp["reporter"].dropna().unique())
        partners = sorted(grp["partner"].dropna().unique())
        flows = sorted(grp["flow"].dropna().unique()) if "flow" in grp.columns else []
        indicators = sorted(grp["indicator"].dropna().unique()) if "indicator" in grp.columns else []
        dates = sorted(grp["date"].dropna().unique())
        sides = sorted(grp["side"].dropna().unique()) if "side" in grp.columns else []

        flow_labels = []
        for f in flows:
            if str(f) == "1":
                flow_labels.append("Import")
            elif str(f) == "2":
                flow_labels.append("Export")
            else:
                flow_labels.append(str(f))

        rows.append({
            "source": "comext (Eurostat Trade Data)",
            "series_code": str(cn),
            "series_name": cn_desc,
            "side": ", ".join(sides),
            "granularity": "monthly",
            "date_range": f"{dates[0]} to {dates[-1]}" if dates else "",
            "n_observations": len(grp),
            "matrix_dimensions": "cn_code × reporter_country × partner_country × flow(import/export) × indicator(value/quantity)",
            "nace_or_cn_codes": str(cn),
            "nace_or_cn_descriptions": cn_desc,
            "countries": f"Reporters: {', '.join(reporters)} | Partners: {', '.join(partners)}",
            "seasonal_adjustments": "N/A (raw trade data)",
            "units": ", ".join(indicators),
            "product_family": meta.get("family", ""),
            "description": meta.get("description", cn_desc),
            "use_case": meta.get("use_case", ""),
        })

    return pd.DataFrame(rows)


def main():
    base = "/Users/sofianeelmokaddam/Desktop/Work/eurostat/output2"
    sts_path = f"{base}/sts.csv"
    comext_path = f"{base}/comext.csv"
    output_path = f"{base}/series_catalog.csv"

    sts_catalog = build_sts_catalog(sts_path)
    comext_catalog = build_comext_catalog(comext_path)

    catalog = pd.concat([sts_catalog, comext_catalog], ignore_index=True)
    catalog.to_csv(output_path, index=False)
    print(f"\nCatalog written to {output_path}")
    print(f"Total series: {len(catalog)} ({len(sts_catalog)} STS + {len(comext_catalog)} COMEXT)")


if __name__ == "__main__":
    main()
