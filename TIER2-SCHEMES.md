# TNGOD Tier 2 — Projects, Schemes & Missions

> **Tier 2** is the project & scheme layer of the Tamil Nadu government web estate: named schemes, missions, programmes, citizen-service platforms, and special-purpose vehicles built for them. These mostly live **outside** the `gov.in` / `nic.in` domain space — on `*.tnega.org` (TNeGA's application ecosystem), smart-city SPV domains, and independent `.com` / `.org` / `.in` registrations.
>
> **Tier 1** (the [main directory](./TAMILNADU.md)) covers permanent institutions — departments, directorates, boards, PSUs, universities, districts. Tier 2 covers the time-bound and theme-specific layer on top.

**Researched & URL-verified:** 24 October 2026. Status icons: ✅ live · 🌐 DNS-live but unreachable from the verification network · ⚠️ server up but erroring · ➖ no dedicated portal found.

## 1. e-Governance platforms (TNeGA ecosystem)

| Portal | Owner | Website | Status |
|---|---|---|---|
| TN Direct Benefit Transfer (DBT) portal | TNeGA / Finance Dept | https://dbt.tn.gov.in | ✅ live |
| UMIS — Unified Monitoring Information System (attendance/beneficiary tracking for Pudhumai Penn & Tamil Pudhalvan) | TNeGA / SW&WE Dept | https://umisdashboard.tnega.org | ✅ live |
| Crop Survey / e-Adangal | TNeGA / Agriculture Dept | https://cropsurvey.tnega.org/dashboard/index.html | ✅ live |
| CM Helpline 1100 | TNeGA / CM Office | https://cmhelpline.tnega.org | ✅ live |
| Pudhumai Penn scheme portal | TNeGA / SW&WE Dept | https://pudhumaipenn.tnega.org | 🌐 DNS-live (AWS); unreachable from verification network |
| TNeGA (alternate domain) | TNeGA | https://tnega.org | ✅ live (redirects to tnega.tn.gov.in) |

## 2. Education & skilling missions

| Scheme | Owner | Website | Status |
|---|---|---|---|
| Illam Thedi Kalvi (Education at the Doorstep) | School Education Dept | https://illamthedikalvi.tnschools.gov.in | ✅ live |
| Naan Mudhalvan | Guidance / Higher Ed | https://naanmudhalvan.tn.gov.in | ✅ live (alias `naanmudhalvan.in` also registered) |

## 3. Health, food & welfare schemes

| Scheme | Owner | Website | Status |
|---|---|---|---|
| CM Comprehensive Health Insurance Scheme (CMCHIS) | Health & Family Welfare | https://cmchistn.com | ✅ live |
| Mudhalvar Marundhagam (budget pharmacies) | Medical & Rural Health Services | https://mudhalvarmarundhagam.tn.gov.in | ✅ live |
| PM POSHAN / Puratchi Thalaivar M.G.R. Nutritious Meal Programme | School Education Dept | https://middaymeal.tn.gov.in | ✅ live |
| TNPDS smart-card PDS | Food & Consumer Protection | https://tnpds.gov.in | ✅ live |

## 4. Urban missions & smart-city SPVs

| SPV / project | Owner | Website | Status |
|---|---|---|---|
| Chennai Smart City Limited (CSCL) | GCC / Govt of TN SPV | https://cscl.co.in | ⚠️ server up, HTTP 500 at check |
| CSCL Open Data Portal | CSCL | https://opendata.cscl.co.in/welcome | ✅ live |
| Coimbatore Smart City ("Idhu Namma Kovai") | CCMC SPV | https://coimbatoresmartcity.org | ✅ live |
| Madurai Smart City | MCMC SPV | https://maduraismartcity.in | ✅ live |
| Salem Smart City | SCC SPV | https://salemsmartcity.org | ✅ live |
| Erode Smart City | ECC SPV | https://erodesmartcity.org | ✅ live |
| Singara Chennai 2.0 | Greater Chennai Corporation | https://singarachennai.com | ✅ live |

## 5. Startups & industry

| Project | Owner | Website | Status |
|---|---|---|---|
| TN-RISE Women Start-Up Council (Tamil Nadu Rural Incubator Startup Enabler) | MSME Dept SPV | https://tnrise.co.in | ✅ live |
| Tamil Nadu Green Climate Company (TNGCC — climate mission vehicle) | Environment & Climate Change Dept | https://www.tngcc.tn.gov.in | ✅ live |

## 6. Environment & eco-tourism

| Portal | Owner | Website | Status |
|---|---|---|---|
| TN Wildscapes (eco-tourism bookings) | TN Forest Development Corp | https://tnwildscapes.com | ✅ live |
| TN Wilderness Experiences Corporation (TNWEC) | Govt of TN eco-tourism SPV | https://tnwec.com | ✅ live |

## 7. Local-governance service portals

| Portal | Owner | Website | Status |
|---|---|---|---|
| Village Panchayat Tax portal | RD&PR Dept | https://vptax.tnrd.tn.gov.in | ✅ live |
| Single-window Planning Permission (Online PPA) | DTCP / CMDA | https://onlineppa.tn.gov.in | ✅ live |

## 8. Corrections & aliases applied to the main directory

- **Coimbatore City Municipal Corporation** — the corporation's real host is **https://ccmc.gov.in** (✅ live); the `coimbatorecorporation.tn.gov.in` variant commonly cited has no DNS. Fixed in the main directory.
- **TN Police alternate portal** — https://police.tn.gov.in (🌐 DNS-live, unreachable from verification network; main site `tnpolice.gov.in` is DNS-live too).
- **Naan Mudhalvan alias** — `naanmudhalvan.in` is registered and redirects into the skill-development portal.
- **Guidance Tamil Nadu** — the live portal is **https://investingintamilnadu.com** (✅); `guidancetn.com` no longer responds (see [SECURITY-NOTES.md](./SECURITY-NOTES.md)).

## 9. Link-sweep additions (25 Oct 2026) — Tier-2 discoveries

New Tier-2 entries found by crawling every inventory homepage, robots.txt and
sitemap (`tools/sweep_links.py`), then verifying each candidate host
(`tools/verify_hosts.py`). Full data in `tamilnadu-sites.csv` (tier=2).

### Forest, wildlife & environment projects

| Project | Website | Status |
|---|---|---|
| Green Tamil Nadu Mission | https://greentnmission.com | ✅ live |
| Project Nilgiri Tahr | https://tnprojectnilgiritahr.com | ✅ live |
| TNFD Yaanai (Thadam) | https://tnfdyaanai.com | ✅ live |
| Thamizh Maram (tree cultivation) | https://thamizhmaram.com | ✅ live |
| TNFWCCB (wildlife conflict mitigation) | https://tnfwccb.com | ✅ live |
| TN Biodiversity Conservation & Greening Project (TGBPCCR) | https://tbgpccr.tn.gov.in | ✅ live |
| Sathyamangalam Tiger Reserve | https://sathytiger.tn.gov.in | ✅ live |
| Kalakkad Mundanthurai Tiger Reserve | https://kmtr.co.in | ✅ live |
| Trek Tamil Nadu (TNWEC) | https://trektamilnadu.com | ✅ live |
| Nilgiris Tree Cutting Permissions | https://nilgiristreecuttingpermissions.org | ⚠️ HTTP 429 |

### Water resources & land

| Project | Website | Status |
|---|---|---|
| TNsand (sand mining portal, WRD) | https://tnsand.in | ✅ live |
| Ground & Surface Water Resources Data Centre (WRD) | https://groundwatertnpwd.org.in | ✅ live |
| IMTI (WRD training institute) | https://tamilnaduimti.org | ⚠️ HTTP 403 |
| TN Fisheries Development Corporation | https://tnfdc.in | ✅ live |
| TN Fisheries Welfare Board | https://tnfwb.tn.gov.in | ✅ live |
| TN Maritime Board | https://tnmaritime.tn.gov.in | ✅ live |
| PUNAL (drinking-water grievances) | https://punal.tn.gov.in | ✅ live |
| TWAD Board e-ODB | https://twadeodb.tn.gov.in | ✅ live |

### Education, employment & welfare service portals

| Portal | Website | Status |
|---|---|---|
| State Scholarship Portal | https://ssp.tn.gov.in | ⚠️ HTTP 503 |
| TN ePass | https://epass.tnega.org | ✅ live |
| Tamil Digital Library | https://tamildigitallibrary.in | ✅ live |
| Kani Tamil (Tamil Virtual Academy) | https://kanitamil.in | ⚠️ HTTP 403 |
| Thiran 360 (capacity building) | https://thiran360.tn.gov.in | ✅ live |
| PM-KUSUM solar pumps (TN) | https://pmkusum.tn.gov.in | ✅ live |
| TN Medical Selection (DME) | https://tnmedicalselection.net | ✅ live |
| TN AYUSH admissions | https://tnayushonline.co.in | ✅ live |
| AD&TW Dept Overseas Scholarship | https://tnadwscholarship.in | ✅ live |
| DipExOnline (DGE) | https://dipexamstndte.in | ✅ live |
| DoTE GTE | https://tndtegteonline.in | ✅ live |
| DoTE Web Apps | https://tndotehub.in | ✅ live |
| DOTE Polytechnic admissions | https://tnpoly.in | ✅ live |
| TN Lateral Entry | https://tnlea.com | ✅ live |
| TN MBA/MCA counselling | https://tn-mbamca.com | ✅ live |
| PTBE-TNEA | https://ptbe-tnea.com | 🌐 unreachable |
| UMS (Univ of Madras IDE) | https://ideunom.ac.in | ✅ live |
| Anna University CeGov | https://auegov.ac.in | ✅ live |
| TNOU student portal | https://tnouportal.in | ✅ live |
| TNAU AgriCart | https://tnauagricart.com | ✅ live |

### Infrastructure, industry & roads

| Portal | Website | Status |
|---|---|---|
| TN Road Sector Project II | https://tnrsp.tn.gov.in | ✅ live |
| CKICP (Highways project portal) | https://ckicp.tn.gov.in | ✅ live |
| Trichy Master Plan (DTCP) | https://trichymasterplan.com | ✅ live |
| TN RERA | https://tnrera.in | 🌐 unreachable |
| TNREAT (real-estate appellate tribunal) | https://tnreat.tn.gov.in | ✅ live |
| TN BizBuddy | https://tnbizbuddy.com | ✅ live |
| TNPL Cements | https://tnplcement.in | ✅ live |
| TN Polymer Park | https://tnpolymerpark.com | ⚠️ HTTP 403 |
| TANTEA | https://tantea.co.in | ⚠️ HTTP 429 |

### Tourism & civic services

| Portal | Website | Status |
|---|---|---|
| TN Tourism Operator Registration System | https://tntourismtors.com | ✅ live |
| TN Tourism Awards | https://tntourismawards.com | ✅ live |
| TN Green Climate Company tracker | https://trackertngcc.tn.gov.in | ✅ live |
| Birth & Death Certificates (crstn.org) | https://crstn.org | ✅ live |
| eAdangal / Emunnetram / OCMMS / PUNAL / Urban eSeva | see `tamilnadu-sites.csv` | ✅ live |

## Appendix — Schemes researched with no dedicated portal (as of 24 Oct 2026)

These flagship schemes had **no standalone website**; official information lives in department pages, G.O.s on `cms.tn.gov.in`, or State Planning Commission write-ups:

| Scheme | Where official info lives |
|---|---|
| Tamil Pudhalvan (₹1,000/month for govt-school boys in higher education) | SW&WE Dept page — https://www.tnsocialwelfare.tn.gov.in/en/specilisationswoman-welfare/tamil-pudhalvan |
| Makkalai Thedi Maruthuvam (doorstep primary care) | SPC evaluation doc — https://spc.tn.gov.in/wp-content/uploads/M_T_M.pdf; Health Dept https://tnhealth.tn.gov.in |
| Innuyir Kappom – Nammai Kaakkum 48 (free 48-hr accident care) | G.O. (Ms) 419/2024 on cms.tn.gov.in; TNSTA https://www.tnsta.gov.in |
| Kudimaramathu (waterbody restoration with community participation) | WRD policy notes — https://www.wrd.tn.gov.in |
| Ungaludan Stalin (outreach camps, launched Jul 2025) | tn.gov.in press releases + district collectorate sites |
| Ennum Ezhuthum (foundational literacy & numeracy mission) | School Ed policy notes; tnschools.gov.in / EMIS |
| Kaaval Uthavi / Kavalan SOS (community policing apps) | App-only — Google Play / App Store; https://tnpolice.gov.in |
| Uzhavan (farmer services app) | App-only — Play Store; Agriculture Dept https://www.tnagrisnet.tn.gov.in |

*Maintained as part of [TNGOD](./README.md). Public-information index only.*
