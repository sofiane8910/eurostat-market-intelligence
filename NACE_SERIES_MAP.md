# NACE Series Mapping — Label Materials Market Dashboard

Complete mapping of macro-categories to NACE Rev. 2 codes and their available Eurostat STS series.

**STS Datasets Legend:**

| Abbrev | Dataset ID | Metric |
|:---|:---|:---|
| PROD | sts_inpr_m | Production in industry (monthly index) |
| TV | sts_intv_m | Turnover in industry — total |
| TVD | sts_intvd_m | Turnover in industry — domestic |
| TVND | sts_intvnd_m | Turnover in industry — non-domestic |
| PP | sts_inpp_m | Producer prices — total |
| PPD | sts_inppd_m | Producer prices — domestic |
| PPND | sts_inppnd_m | Producer prices — non-domestic |
| IMP | sts_inpi_m | Import prices in industry |
| LAB | sts_inlb_m | Labour input in industry |
| CONF | ei_bssi_m_r2 | Industry confidence indicator |
| RTT | sts_trtu_m | Retail trade turnover |
| SPI | sts_sepr_m | Services production index |
| RTC | ei_bsrt_m_r2 | Retail trade confidence |
| SC | ei_bsse_m_r2 | Services confidence |

**Coverage rules:**
- **2-digit codes** (C10, C11, ...): All 10 industry datasets (PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF)
- **3/4-digit codes** (C204, C262, ...): 6 datasets (PROD, PP, PPD, PPND, IMP, CONF) — NO turnover/labour
- **Retail (G47)**: RTT + RTC
- **Services (H)**: SPI + SC

---

## SUPPLY SIDE

### Paper & Board

| NACE | Description | Available Series |
|:---|:---|:---|
| **C17** | Paper and paper products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| C171 | Pulp, paper and paperboard | PROD, PP, PPD, PPND, IMP, CONF |
| C1712 | Paper and paperboard | PROD, PP, PPD, PPND, IMP, CONF |
| C172 | Articles of paper and paperboard | PROD, PP, PPD, PPND, IMP, CONF |
| C1729 | Other articles of paper and paperboard | PROD, PP, PPD, PPND, IMP, CONF |

### Labels

| NACE | Description | Available Series |
|:---|:---|:---|
| **C18** | Printing and reproduction | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Films & Plastics

| NACE | Description | Available Series |
|:---|:---|:---|
| **C22** | Rubber and plastic products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| C222 | Plastics products | PROD, PP, PPD, PPND, IMP, CONF |
| C2221 | Plastic plates, sheets, tubes, profiles | PROD, PP, PPD, PPND, IMP, CONF |
| C2229 | Other plastic products | PROD, PP, PPD, PPND, IMP, CONF |

### Adhesives & Chemicals

| NACE | Description | Available Series |
|:---|:---|:---|
| **C20** | Chemicals and chemical products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| C203 | Paints, varnishes, printing ink, mastics | PROD, PP, PPD, PPND, IMP, CONF |
| C2052 | Manufacture of glues | PROD, PP, PPD, PPND, IMP, CONF |

### Inks & Foils

| NACE | Description | Available Series |
|:---|:---|:---|
| C203 | Paints, varnishes, printing ink, mastics | *(shared with Adhesives & Chemicals)* |

### RFID & Smart Cards

| NACE | Description | Available Series |
|:---|:---|:---|
| C2829 | Other general-purpose machinery n.e.c. | PROD, PP, PPD, PPND, IMP, CONF |

---

## DEMAND SIDE — Consumer FMCG

### Food

| NACE | Description | Available Series |
|:---|:---|:---|
| **C10** | Manufacture of food products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| G47_FOOD | Retail sale of food, beverages and tobacco | RTT |
| G4711 | Non-specialised stores (food predominating) | RTT |
| G47_FOOD | *(retail confidence)* | RTC |

### Beverage

| NACE | Description | Available Series |
|:---|:---|:---|
| **C11** | Manufacture of beverages | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Tobacco

| NACE | Description | Available Series |
|:---|:---|:---|
| **C12** | Manufacture of tobacco products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Health & Personal Care

| NACE | Description | Available Series |
|:---|:---|:---|
| **C204** | Soap, detergents, cleaning, cosmetics (aggregate) | PROD, PP, PPD, PPND, IMP, CONF |
| **C2042** | Perfumes and toilet preparations | PROD, PP, PPD, PPND, IMP, CONF |
| G47_NF_HLTH | Dispensing chemist, medical goods, cosmetics | RTT |

### Household Chemicals

| NACE | Description | Available Series |
|:---|:---|:---|
| **C2041** | Soap, detergents, cleaning and polishing | PROD, PP, PPD, PPND, IMP, CONF |

### Textiles & Apparel

| NACE | Description | Available Series |
|:---|:---|:---|
| **C13** | Manufacture of textiles | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| **C14** | Manufacture of wearing apparel | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| **C15** | Manufacture of leather and related products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

---

## DEMAND SIDE — Regulated & Industrial

### Pharmaceuticals

| NACE | Description | Available Series |
|:---|:---|:---|
| **C21** | Basic pharmaceutical products and preparations | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Industrial Chemicals

| NACE | Description | Available Series |
|:---|:---|:---|
| **C20** | Chemicals and chemical products (excl 20.41/20.42) | *(shared with Supply > Adhesives)* PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Automotive

| NACE | Description | Available Series |
|:---|:---|:---|
| **C29** | Motor vehicles, trailers and semi-trailers | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Consumer Durables

| NACE | Description | Available Series |
|:---|:---|:---|
| **C26** | Computer, electronic and optical products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| C262 | Computers and peripheral equipment | PROD, PP, PPD, PPND, IMP, CONF |
| C263 | Communication equipment | PROD, PP, PPD, PPND, IMP, CONF |
| C264 | Consumer electronics | PROD, PP, PPD, PPND, IMP, CONF |
| **C27** | Electrical equipment | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| C2751 | Electric domestic appliances (white goods) | PROD, PP, PPD, PPND, IMP, CONF |

### Machinery & Metals

| NACE | Description | Available Series |
|:---|:---|:---|
| **C28** | Machinery and equipment n.e.c. | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| **C25** | Fabricated metal products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Furniture & Other Manufacturing

| NACE | Description | Available Series |
|:---|:---|:---|
| **C31** | Manufacture of furniture | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| **C32** | Other manufacturing | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |
| C3299 | Other manufacturing n.e.c. | PROD, PP, PPD, PPND, IMP, CONF |

### Fabricated Metals

*(included under Machinery & Metals above)*

---

## DEMAND SIDE — Services & Logistics

### Transportation & Logistics

| NACE | Description | Available Series |
|:---|:---|:---|
| **H** | Transportation and storage | SPI, SC |
| H49 | Land transport and pipelines | SPI |
| H52 | Warehousing and transport support | SPI |
| H53 | Postal and courier activities | SPI |

### Retail

| NACE | Description | Available Series |
|:---|:---|:---|
| **G47** | Retail trade (excl. motor vehicles) | RTT |
| G47_FOOD | Retail sale of food, beverages and tobacco | RTT, RTC |
| G47_NFOOD | Retail non-food products | RTC |
| G47_NFOOD_X_G473 | Non-food retail (excl. automotive fuel) | RTT |
| G47_NF_HLTH | Dispensing chemist, medical goods, cosmetics | RTT |
| G4711 | Non-specialised stores (food predominating) | RTT |

---

## DEMAND SIDE — Miscellaneous

### Office Products

| NACE | Description | Available Series |
|:---|:---|:---|
| **C1723** | Manufacture of paper stationery | PROD, PP, PPD, PPND, IMP, CONF |
| **C3299** | Other manufacturing n.e.c. | PROD, PP, PPD, PPND, IMP, CONF |

### Glass & Ceramics

| NACE | Description | Available Series |
|:---|:---|:---|
| **C23** | Other non-metallic mineral products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

### Wood & Building Materials

| NACE | Description | Available Series |
|:---|:---|:---|
| **C16** | Manufacture of wood and cork products | PROD, TV, TVD, TVND, PP, PPD, PPND, IMP, LAB, CONF |

---

## Summary

| Side | Macro-Category | Segments | NACE codes | Est. series |
|:---|:---|:---|:---|:---|
| Supply | Labels supply chain | 6 | 14 | ~158 |
| Demand | Consumer FMCG | 7 (Food, Beverage, Tobacco, HPC, Household Chem, Textiles & Apparel, Footwear) | 10 industry + 4 retail | ~120 |
| Demand | Regulated & Industrial | 6 (Pharma, Ind. Chemicals, Auto, Durables, Machinery, Furniture) | 15 | ~130 |
| Demand | Services & Logistics | 2 (Transport, Retail) | 10 | ~12 |
| Demand | Miscellaneous | 3 (Office, Glass, Building Materials) | 4 | ~30 |
| **Total** | | **24 segments** | **~53 NACE codes** | **~450 series** |

All series use Index base 2021=100 (I21), seasonally and calendar adjusted (SCA), monthly frequency, covering EU27 member states.
