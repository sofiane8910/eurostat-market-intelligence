# NACE Series Mapping — Label Materials Market Dashboard

Simple mapping of each demand-side segment to its Eurostat STS series keys.

**Series key format:** `{dataset}_{nace_code}` — e.g. `sts_inpr_m_C10` = Food production index.

**Datasets:**
- `sts_inpr_m` = Production | `sts_intv_m` = Turnover (total) | `sts_intvd_m` = Turnover (domestic) | `sts_intvnd_m` = Turnover (non-domestic)
- `sts_inpp_m` = Producer prices (total) | `sts_inppd_m` = Prices (domestic) | `sts_inppnd_m` = Prices (non-domestic)
- `sts_inpi_m` = Import prices | `sts_inlb_m` = Labour input | `ei_bssi_m_r2` = Industry confidence
- `sts_trtu_m` = Retail turnover | `ei_bsrt_m_r2` = Retail confidence | `sts_sepr_m` = Services production | `ei_bsse_m_r2` = Services confidence

---

| Category | Series |
|:---|:---|
| **CONSUMER FMCG** | |
| Food | `sts_inpr_m_C10`, `sts_intv_m_C10`, `sts_intvd_m_C10`, `sts_intvnd_m_C10`, `sts_inpp_m_C10`, `sts_inppd_m_C10`, `sts_inppnd_m_C10`, `sts_inpi_m_C10`, `sts_inlb_m_C10`, `ei_bssi_m_r2_C10`, `sts_trtu_m_G47_FOOD`, `sts_trtu_m_G4711`, `ei_bsrt_m_r2_G47_FOOD` |
| Beverage | `sts_inpr_m_C11`, `sts_intv_m_C11`, `sts_intvd_m_C11`, `sts_intvnd_m_C11`, `sts_inpp_m_C11`, `sts_inppd_m_C11`, `sts_inppnd_m_C11`, `sts_inpi_m_C11`, `sts_inlb_m_C11`, `ei_bssi_m_r2_C11` |
| Tobacco | `sts_inpr_m_C12`, `sts_intv_m_C12`, `sts_intvd_m_C12`, `sts_intvnd_m_C12`, `sts_inpp_m_C12`, `sts_inppd_m_C12`, `sts_inppnd_m_C12`, `sts_inpi_m_C12`, `sts_inlb_m_C12`, `ei_bssi_m_r2_C12` |
| Health & Personal Care | `sts_inpr_m_C2042`, `sts_inpp_m_C2042`, `sts_inppd_m_C2042`, `sts_inppnd_m_C2042`, `sts_inpi_m_C2042`, `ei_bssi_m_r2_C2042`, `sts_inpr_m_C204`, `sts_inpp_m_C204`, `sts_inppd_m_C204`, `sts_inppnd_m_C204`, `sts_inpi_m_C204`, `ei_bssi_m_r2_C204`, `sts_trtu_m_G47_NF_HLTH` |
| Household Chemicals | `sts_inpr_m_C2041`, `sts_inpp_m_C2041`, `sts_inppd_m_C2041`, `sts_inppnd_m_C2041`, `sts_inpi_m_C2041`, `ei_bssi_m_r2_C2041` |
| Textiles & Apparel | `sts_inpr_m_C13`, `sts_intv_m_C13`, `sts_intvd_m_C13`, `sts_intvnd_m_C13`, `sts_inpp_m_C13`, `sts_inppd_m_C13`, `sts_inppnd_m_C13`, `sts_inpi_m_C13`, `sts_inlb_m_C13`, `ei_bssi_m_r2_C13`, `sts_inpr_m_C14`, `sts_intv_m_C14`, `sts_intvd_m_C14`, `sts_intvnd_m_C14`, `sts_inpp_m_C14`, `sts_inppd_m_C14`, `sts_inppnd_m_C14`, `sts_inpi_m_C14`, `sts_inlb_m_C14`, `ei_bssi_m_r2_C14` |
| Footwear & Leather | `sts_inpr_m_C15`, `sts_intv_m_C15`, `sts_intvd_m_C15`, `sts_intvnd_m_C15`, `sts_inpp_m_C15`, `sts_inppd_m_C15`, `sts_inppnd_m_C15`, `sts_inpi_m_C15`, `sts_inlb_m_C15`, `ei_bssi_m_r2_C15` |
| **REGULATED & INDUSTRIAL** | |
| Pharmaceuticals | `sts_inpr_m_C21`, `sts_intv_m_C21`, `sts_intvd_m_C21`, `sts_intvnd_m_C21`, `sts_inpp_m_C21`, `sts_inppd_m_C21`, `sts_inppnd_m_C21`, `sts_inpi_m_C21`, `sts_inlb_m_C21`, `ei_bssi_m_r2_C21` |
| Industrial Chemicals | `sts_inpr_m_C20`, `sts_intv_m_C20`, `sts_intvd_m_C20`, `sts_intvnd_m_C20`, `sts_inpp_m_C20`, `sts_inppd_m_C20`, `sts_inppnd_m_C20`, `sts_inpi_m_C20`, `sts_inlb_m_C20`, `ei_bssi_m_r2_C20` |
| Automotive | `sts_inpr_m_C29`, `sts_intv_m_C29`, `sts_intvd_m_C29`, `sts_intvnd_m_C29`, `sts_inpp_m_C29`, `sts_inppd_m_C29`, `sts_inppnd_m_C29`, `sts_inpi_m_C29`, `sts_inlb_m_C29`, `ei_bssi_m_r2_C29` |
| Consumer Durables | `sts_inpr_m_C26`, `sts_intv_m_C26`, `sts_intvd_m_C26`, `sts_intvnd_m_C26`, `sts_inpp_m_C26`, `sts_inppd_m_C26`, `sts_inppnd_m_C26`, `sts_inpi_m_C26`, `sts_inlb_m_C26`, `ei_bssi_m_r2_C26`, `sts_inpr_m_C262`, `sts_inpp_m_C262`, `sts_inppd_m_C262`, `sts_inppnd_m_C262`, `sts_inpi_m_C262`, `ei_bssi_m_r2_C262`, `sts_inpr_m_C263`, `sts_inpp_m_C263`, `sts_inppd_m_C263`, `sts_inppnd_m_C263`, `sts_inpi_m_C263`, `ei_bssi_m_r2_C263`, `sts_inpr_m_C264`, `sts_inpp_m_C264`, `sts_inppd_m_C264`, `sts_inppnd_m_C264`, `sts_inpi_m_C264`, `ei_bssi_m_r2_C264`, `sts_inpr_m_C27`, `sts_intv_m_C27`, `sts_intvd_m_C27`, `sts_intvnd_m_C27`, `sts_inpp_m_C27`, `sts_inppd_m_C27`, `sts_inppnd_m_C27`, `sts_inpi_m_C27`, `sts_inlb_m_C27`, `ei_bssi_m_r2_C27`, `sts_inpr_m_C2751`, `sts_inpp_m_C2751`, `sts_inppd_m_C2751`, `sts_inppnd_m_C2751`, `sts_inpi_m_C2751`, `ei_bssi_m_r2_C2751` |
| Machinery & Equipment | `sts_inpr_m_C28`, `sts_intv_m_C28`, `sts_intvd_m_C28`, `sts_intvnd_m_C28`, `sts_inpp_m_C28`, `sts_inppd_m_C28`, `sts_inppnd_m_C28`, `sts_inpi_m_C28`, `sts_inlb_m_C28`, `ei_bssi_m_r2_C28` |
| Fabricated Metals | `sts_inpr_m_C25`, `sts_intv_m_C25`, `sts_intvd_m_C25`, `sts_intvnd_m_C25`, `sts_inpp_m_C25`, `sts_inppd_m_C25`, `sts_inppnd_m_C25`, `sts_inpi_m_C25`, `sts_inlb_m_C25`, `ei_bssi_m_r2_C25` |
| Furniture | `sts_inpr_m_C31`, `sts_intv_m_C31`, `sts_intvd_m_C31`, `sts_intvnd_m_C31`, `sts_inpp_m_C31`, `sts_inppd_m_C31`, `sts_inppnd_m_C31`, `sts_inpi_m_C31`, `sts_inlb_m_C31`, `ei_bssi_m_r2_C31` |
| Other Manufacturing | `sts_inpr_m_C32`, `sts_intv_m_C32`, `sts_intvd_m_C32`, `sts_intvnd_m_C32`, `sts_inpp_m_C32`, `sts_inppd_m_C32`, `sts_inppnd_m_C32`, `sts_inpi_m_C32`, `sts_inlb_m_C32`, `ei_bssi_m_r2_C32`, `sts_inpr_m_C3299`, `sts_inpp_m_C3299`, `sts_inppd_m_C3299`, `sts_inppnd_m_C3299`, `sts_inpi_m_C3299`, `ei_bssi_m_r2_C3299` |
| **SERVICES & LOGISTICS** | |
| Transportation & Logistics | `sts_sepr_m_H`, `ei_bsse_m_r2_H`, `sts_sepr_m_H49`, `sts_sepr_m_H52`, `sts_sepr_m_H53` |
| Retail | `sts_trtu_m_G47`, `sts_trtu_m_G47_FOOD`, `sts_trtu_m_G47_NFOOD_X_G473`, `sts_trtu_m_G47_NF_HLTH`, `sts_trtu_m_G4711`, `ei_bsrt_m_r2_G47_FOOD`, `ei_bsrt_m_r2_G47_NFOOD` |
| **MISCELLANEOUS** | |
| Office Products | `sts_inpr_m_C1723`, `sts_inpp_m_C1723`, `sts_inppd_m_C1723`, `sts_inppnd_m_C1723`, `sts_inpi_m_C1723`, `ei_bssi_m_r2_C1723`, `sts_inpr_m_C3299`, `sts_inpp_m_C3299`, `sts_inppd_m_C3299`, `sts_inppnd_m_C3299`, `sts_inpi_m_C3299`, `ei_bssi_m_r2_C3299` |
| Glass & Ceramics | `sts_inpr_m_C23`, `sts_intv_m_C23`, `sts_intvd_m_C23`, `sts_intvnd_m_C23`, `sts_inpp_m_C23`, `sts_inppd_m_C23`, `sts_inppnd_m_C23`, `sts_inpi_m_C23`, `sts_inlb_m_C23`, `ei_bssi_m_r2_C23` |
| Wood & Building Materials | `sts_inpr_m_C16`, `sts_intv_m_C16`, `sts_intvd_m_C16`, `sts_intvnd_m_C16`, `sts_inpp_m_C16`, `sts_inppd_m_C16`, `sts_inppnd_m_C16`, `sts_inpi_m_C16`, `sts_inlb_m_C16`, `ei_bssi_m_r2_C16` |
