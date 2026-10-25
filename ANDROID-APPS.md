# TNGOD — Tamil Nadu Government Android Apps

Companion to the [website directory](./TAMILNADU.md): the **official Android apps** of Tamil
Nadu government departments, SPVs and schemes. **27 apps verified on Google Play on
25 October 2026.** Machine-readable copy: [`android-apps.csv`](./android-apps.csv).

> Note: there is no iOS mirror inventory here; several apps (e.g. Kaaval Uthavi) also ship on
> the App Store, but Play is the primary distribution channel for the state.

## Methodology

1. **Seed** — the state's own app registry: https://www.tn.gov.in/mobileappform.php (10 apps, each with a Play link, department and description).
2. **Supplement** — Play Store searches for departments/SPVs known from the website inventory (police, CMRL/CUMTA, GCC, corporations, NHM, TNeGA, TNPSC…). An app is included only when the Play developer is the government entity itself (e.g. "Tamil Nadu Police, Chennai", "Greater Chennai Corporation", "Chennai Metro Rail Limited", `in.gov.tn.*` / `org.tnega.*` packages) — third-party wrappers and private land-record apps are excluded.
3. **Verify** — every listing fetched from `play.google.com` at 25 Oct 2026; installs/updated/rating captured at that time. Package id is the stable identifier in the CSV.

The official portal's list also includes **eSevai TPA** (`org.tnega.esevai.tpa`, an internal
TNeGA auditing app) which **no longer resolves on Play** — listed as delisted below.

## Methodology (Tier 3 — app backends)

The 26 obtainable APKs (1 of the 27, TN CMSWFS `com.xts.dma`, is unavailable on the public
mirror) were statically analyzed with `tools/extract_app_urls.py`: every URL string embedded
in dex bytecodes, binary XML, `resources.arsc`, assets and native libs was extracted (UTF-8
+ UTF-16LE decoding), hosts deduped per app, and classified:

- **first-party** — government-owned or named scheme-vendor backends (`*.gov.in`, `*.nic.in`,
  `*.tnega.org`, `tnstc.in`, `tangedco.org`, `chennaimetrorail.org`, `moving.tech` (CUMTA's
  ticketing vendor), `tn-nhis.com` (CMCHIS vendor), …) → promoted to **Tier 3** rows in
  [`tamilnadu-sites.csv`](./tamilnadu-sites.csv) (group *App API Backends (Tier 3)*, 30 rows)
- **sdk** — payments/analytics/maps/crash SDKs (Juspay, Google/Firebase, Razorpay, Mappls, …) — excluded
- **other** — framework/vendor noise (react.dev, wikipedia, font hosts, …) — excluded

Central-government integrations surfaced by the apps (ABDM/ABHA for TNPHR, Parivahan
e-Challan and cybercrime.gov.in for Kaaval Uthavi) are noted here but not Tier-3 rows,
as they are national infrastructure. See [SECURITY-NOTES.md](./SECURITY-NOTES.md) for
hygiene observations.

## Citizen services & grievance

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| TN CM Helpline Citizen | Mudalvarin Mugavari Dept / TNeGA | 10L+ | 19 Jun 2026 | [org.tnega.cmhelpline.citizen](https://play.google.com/store/apps/details?id=org.tnega.cmhelpline.citizen) |
| Makkal Sevai Generic eKYC | Revenue & DM Dept | 50K+ | 27 Dec 2024 | [gov_in.tn.eKYC](https://play.google.com/store/apps/details?id=gov_in.tn.eKYC) |

## Revenue & land records

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| TamilNilam | Survey & Settlement Dept | 10L+ | 18 Sep 2024 | [com.phonegap.TAMILNILAM](https://play.google.com/store/apps/details?id=com.phonegap.TAMILNILAM) |
| TamilNilam Geo-Info | Survey & Settlement / TNeGA | 10L+ | 2026 | [org.tnega.tamil.nilam](https://play.google.com/store/apps/details?id=org.tnega.tamil.nilam) |
| TNREGINET (TNIGRS) | Registration Dept | 1L+ | 2026 | [com.tnreginet.tnigrs](https://play.google.com/store/apps/details?id=com.tnreginet.tnigrs) |

## Police & safety

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| Kaaval Uthavi | Tamil Nadu Police | 10L+ | 17 Nov 2025 | [com.amtexsystems.kaavaluthavi](https://play.google.com/store/apps/details?id=com.amtexsystems.kaavaluthavi) |

Kavalan SOS (from the [Tier-2 appendix](./TIER2-SCHEMES.md)) no longer has a separate listing — it is folded into Kaaval Uthavi's emergency-alert flow.

## Transport

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| TNSTC Official App | TN State Transport Corp | 50L+ | 14 Oct 2026 | [com.tnstc](https://play.google.com/store/apps/details?id=com.tnstc) |
| Chennai One (bus·metro·train) | CUMTA | 1M+ | 2026 | [in.mobility.cumta](https://play.google.com/store/apps/details?id=in.mobility.cumta) |
| CMRL Metro App | Chennai Metro Rail Ltd | 10L+ | 2026 | [org.chennaimetrorail.appv1](https://play.google.com/store/apps/details?id=org.chennaimetrorail.appv1) |
| CMRL FMS | Chennai Metro Rail Ltd | 5K+ | 2026 | [com.cmrlone.fms](https://play.google.com/store/apps/details?id=com.cmrlone.fms) |

## Energy · Agriculture · Rural

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| TANGEDCO Mobile App | TNPDCL (ex-TANGEDCO) | 10L+ | 22 Oct 2026 | [com.tneb.tangedco](https://play.google.com/store/apps/details?id=com.tneb.tangedco) |
| UZHAVAR | Agriculture & Farmers Welfare | 10L+ | 23 Jun 2026 | [agri.tnagri](https://play.google.com/store/apps/details?id=agri.tnagri) |
| Crop Survey (O) | Agriculture / TNeGA | 1L+ | 2026 | [org.tnega.payiraaivu](https://play.google.com/store/apps/details?id=org.tnega.payiraaivu) |
| Namma Grama Sabhai | RD&PR Dept | 1L+ | 27 Sep 2023 | [com.xts.tnngs](https://play.google.com/store/apps/details?id=com.xts.tnngs) |

## Municipal & urban

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| TN Urban Esevai | Commissionerate of Municipal Administration | 1L+ | 2026 | [com.cma_mobile.beta](https://play.google.com/store/apps/details?id=com.cma_mobile.beta) |
| GCC Official App | Greater Chennai Corporation | 10K+ | 2026 | [chennaicorporation.gov.in.gcc_official_app](https://play.google.com/store/apps/details?id=chennaicorporation.gov.in.gcc_official_app) |
| Namma Chennai | Greater Chennai Corporation | 1L+ | 2026 | [com.ceedeev.grivenancev2](https://play.google.com/store/apps/details?id=com.ceedeev.grivenancev2) |
| Namma Kovai | Coimbatore City Municipal Corporation | 10K+ | 2026 | [com.nammakovai.app](https://play.google.com/store/apps/details?id=com.nammakovai.app) |
| Tiruppur CMC app | Tiruppur City Municipal Corporation | 1K+ | 2026 | [com.tcmiccc.app](https://play.google.com/store/apps/details?id=com.tcmiccc.app) |
| TN CMSWFS | Govt of TN — Corps & Municipalities | 10K+ | 2026 | [com.xts.dma](https://play.google.com/store/apps/details?id=com.xts.dma) |

## Health · Education · Exams

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| TNPHR | NHM Tamil Nadu | 10K+ | 2026 | [com.nhm.tnphr](https://play.google.com/store/apps/details?id=com.nhm.tnphr) |
| CMCHIS | H&FW Dept (TPA: Medi Assist) | 1L+ | 2026 | [com.tnhealthschemev2](https://play.google.com/store/apps/details?id=com.tnhealthschemev2) |
| Naan Mudhalvan | Naan Mudhalvan / TNSDC | 5L+ | 2026 | [in.gov.tn.naanmudhalvan](https://play.google.com/store/apps/details?id=in.gov.tn.naanmudhalvan) |
| TNPSC EMS | TNPSC | 10K+ | 2026 | [com.tnpsc.ems](https://play.google.com/store/apps/details?id=com.tnpsc.ems) |

## Welfare schemes (Tier 2 apps)

| App | Owner | Installs | Updated | Play |
|---|---|---|---|---|
| Kalaignar Magalir Urimai Thittam survey | SPI Dept | 1L+ | 26 Jul 2023 | [com.hhs.android.app](https://play.google.com/store/apps/details?id=com.hhs.android.app) |
| MUT Verification 2026 | SPI Dept / TNeGA | 1L+ | 2026 | [org.tnega.kmut.verification](https://play.google.com/store/apps/details?id=org.tnega.kmut.verification) |
| PKBFS (CM Breakfast Scheme) | SPI Dept | 1L+ | 19 Sep 2026 | [com.xts.cmbfs](https://play.google.com/store/apps/details?id=com.xts.cmbfs) |

## Delisted / retired

- **eSevai TPA** (`org.tnega.esevai.tpa`) — still on the [official state app list](https://www.tn.gov.in/mobileappform.php) but **no longer available on Play** (internal TNeGA audit app; likely withdrawn from the public store).

## Cross-links

- Web-directory counterpart: [TAMILNADU.md](./TAMILNADU.md) · [searchable site](https://logicinczo.github.io/TNGOD/) (apps have their own page: [/apps.html](https://logicinczo.github.io/TNGOD/apps.html))
- Schemes with app-only presence: [TIER2-SCHEMES.md appendix](./TIER2-SCHEMES.md)
- State's official app registry: https://www.tn.gov.in/mobileappform.php

*Maintained as part of [TNGOD](./README.md). Public-information index only; installs/updated/rating snapshot 25 Oct 2026.*

## Tier 3 — domains these apps talk to (app backends)

Static extraction of every URL embedded in the 26 APKs (dex bytecodes, binary XML,
resources, assets, native libs — no execution), filtered to **first-party** backends:
hosts owned by TN government entities (or their named scheme vendors). Central-government
integrations (ABDM, Parivahan e-Challan, cybercrime.gov.in), UAT/sandbox hosts and vendor
dashboards are documented but not listed as rows. Full per-host evidence with reference
counts: [`tools/app-backends.jsonl`](./tools/app-backends.jsonl).

| Backend host | What it is | Apps using it | Status |
|---|---|---|---|
| ⚠️ [`appmonitor.moving.tech`](https://appmonitor.moving.tech) | appmonitor (TN gov app backend) | Chennai One | ⚠️ error |
| ⚠️ [`assets.moving.tech`](https://assets.moving.tech) | assets (TN gov app backend) | Chennai One | ⚠️ error |
| ✅ [`ccmc.appifeedback.in`](https://ccmc.appifeedback.in) | CCMC citizen-feedback backend (AppiFeedback) — vendor-operated feedback tool used by Coimbatore corporation | Namma Kovai | ✅ live |
| ✅ [`chennaimetrorail.org`](https://chennaimetrorail.org) | Chennai Metro Rail Limited website — official CMRL site + app content host | CMRL Metro App | ✅ live |
| ⚠️ [`api.moving.tech`](https://api.moving.tech) | Chennai One API (Moving Tech — CUMTA vendor) — primary ticketing backend of the official CUMTA app; vendor-operated; assets/config/appmonitor.moving.tech also live | Chennai One | ⚠️ error |
| ✅ [`commuters-data.chennaimetrorail.org`](https://commuters-data.chennaimetrorail.org) | CMRL commuter-data API — official CMRL app backend | CMRL Metro App | ✅ live |
| ✅ [`collabland-tn.gov.in`](https://collabland-tn.gov.in) | Collabland TN (CollabWeb) — land-records collaboration platform | TamilNilam | ✅ live |
| ⚠️ [`config.moving.tech`](https://config.moving.tech) | config (TN gov app backend) | Chennai One | ⚠️ error |
| ✅ [`cropsurveyapi.tnega.org`](https://cropsurveyapi.tnega.org) | Crop Survey API — field crop-survey data collection API | Crop Survey (O) | ✅ live |
| ✅ [`cumta.tn.gov.in`](https://cumta.tn.gov.in) | CUMTA — Chennai Unified Metropolitan Transport Authority — transport authority portal | Chennai One | ✅ live |
| 🌐 [`appkvl.spmcrdial100.in`](https://appkvl.spmcrdial100.in) | ERSS 112 backend (SPMCR) — 112-India platform endpoint; unreachable at check | Kaaval Uthavi | 🌐 unreachable |
| ✅ [`tn.erss.in`](https://tn.erss.in) | ERSS 112 — TN Emergency Response Support System — national emergency-number backend used by Kaaval Uthavi | Kaaval Uthavi | ✅ live |
| ✅ [`gccapp.chennaicorporation.gov.in`](https://gccapp.chennaicorporation.gov.in) | GCC app API — GCC mobile-app API host | TN Urban Esevai | ✅ live |
| ✅ [`erp.chennaicorporation.gov.in`](https://erp.chennaicorporation.gov.in) | GCC ERP backend — Greater Chennai Corporation ERP (property tax etc.) | GCC Official App, Namma Chennai | ✅ live |
| ✅ [`gisgcc.chennaicorporation.gov.in`](https://gisgcc.chennaicorporation.gov.in) | GCC GIS backend — Greater Chennai Corporation GIS (Tomcat) | GCC Official App, Namma Chennai | ✅ live |
| ✅ [`portal.chennaicorporation.gov.in`](https://portal.chennaicorporation.gov.in) | GCC portal services | Namma Chennai | ✅ live |
| ✅ [`gccservices.chennaicorporation.gov.in`](https://gccservices.chennaicorporation.gov.in) | GCC services backend — GCC civic services API | Namma Chennai | ✅ live |
| ✅ [`kmut.tnega.org`](https://kmut.tnega.org) | Kalaignar Magalir Urimai Thittam portal — scheme portal | MUT Verification 2026 | ✅ live |
| ⚠️ [`mut.secureapp.tnega.org`](https://mut.secureapp.tnega.org) | KMUT verification API — entitlement-verification API host | MUT Verification 2026 | ⚠️ error |
| ✅ [`tamilnilam.tn.gov.in`](https://tamilnilam.tn.gov.in) | TamilNilam citizen portal — land-records e-services | TamilNilam | ✅ live |
| ⚠️ [`app1.tangedco.org`](https://app1.tangedco.org) | TANGEDCO app backend (app1) — secondary app API host | TANGEDCO Mobile App | ⚠️ error |
| ✅ [`ccms.tangedco.org`](https://ccms.tangedco.org) | TANGEDCO app backend (CCMS) — consumer-care/billing API of the TANGEDCO app | TANGEDCO Mobile App | ✅ live |
| ✅ [`thiranmigutiruppur.com`](https://thiranmigutiruppur.com) | Tiruppur Smart City backend (TSC) — vendor-operated portal of Tiruppur Smart City | Tiruppur City Municipal Corporation app | ✅ live |
| ✅ [`tnurbantree.tn.gov.in`](https://tnurbantree.tn.gov.in) | TN Urban Tree Authority portal | TN Urban Esevai | ✅ live |
| ✅ [`tn-nhis.com`](https://tn-nhis.com) | TN-NHIS (CM Comprehensive Health Insurance Scheme backend) — scheme backend of the CMCHIS app; vendor-operated domain | CMCHIS (CM Health Insurance Scheme) | ✅ live |
| ✅ [`ekyc.tnega.org`](https://ekyc.tnega.org) | TNeGA generic eKYC — shared eKYC gateway (Makkal Sevai) | Makkal Sevai Generic eKYC | ✅ live |
| 🌐 [`tngis.tnega.org`](https://tngis.tnega.org) | TNeGA GIS service — no DNS at check time (referenced by app) | TamilNilam Geo-Info | 🌐 unreachable |
| 🌐 [`mobileapi.phr.tn.gov.in`](https://mobileapi.phr.tn.gov.in) | TNPHR mobile API — TN Personal Health Record API; unreachable at check (NIC) | TNPHR | 🌐 unreachable |
| ✅ [`tnpscems.tn.gov.in`](https://tnpscems.tn.gov.in) | TNPSC EMS portal — exam-management portal behind the TNPSC app | TNPSC EMS | ✅ live |
| ✅ [`urbantamilnilam.tn.gov.in`](https://urbantamilnilam.tn.gov.in) | Urban TamilNilam — urban land-records e-services | TamilNilam | ✅ live |
