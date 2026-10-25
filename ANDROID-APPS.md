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
