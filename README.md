# TNGOD — Tamil Nadu Government Online Directory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Searchable web directory](https://img.shields.io/badge/search-web%20directory-2ea44f)](https://logicinczo.github.io/TNGOD/)
[![Data source: IGOD](https://img.shields.io/badge/source-IGOD%20%C2%B7%20india.gov.in-0969da)](https://www.india.gov.in/directory/web-directory)
[![URL-verified](https://img.shields.io/badge/URL_verified-25_Oct_2026-orange)](./TAMILNADU.md)
[![Link sweep](https://img.shields.io/badge/link_sweep-441%20entries-8250df)](./TAMILNADU.md)

A comprehensive, URL-verified directory of Tamil Nadu government websites, built from the official **IGOD** (Integrated Government Online Directory) listing, cross-checked against the Tamil Nadu state portal, and expanded by an automated **homepage/sitemap link sweep** over the whole inventory.

> IGOD lives at [igod.gov.in](https://igod.gov.in) and is now served by the National Portal's
> [Web Directory](https://www.india.gov.in/directory/web-directory) (State/UTs → Tamil Nadu).
> The India Portal is maintained by NIC under the Digital India programme.

## 🔎 Searchable web directory

Browse and filter the directory at **https://logicinczo.github.io/TNGOD/** — a dependency-free client-side search over the dataset (by name, URL, group, tier and verification status), served by GitHub Pages from [`docs/`](./docs/index.html) with no tracking.

## Tiers

The directory is organized in two layers:

- **Tier 1 — Institutional estate (371 entries):** permanent government institutions — departments, directorates, commissions, boards, PSUs, universities, districts, ULBs — irrespective of domain.
- **Tier 2 — Projects & schemes (70 entries):** named schemes, missions, programmes, citizen-service platforms (the TNeGA ecosystem), smart-city SPVs, service portals (admissions, sand, grievances), and project vehicles — mostly on **non-`gov.in`** domains (`*.tnega.org`, `.com`/`.org`/`.in` SPV registrations). Detailed registry with scheme owners and research notes: **[TIER2-SCHEMES.md](./TIER2-SCHEMES.md)**.

## Files

| File | Contents |
|---|---|
| [TAMILNADU.md](./TAMILNADU.md) | The main Tier-1 directory — institutions grouped by sector (departments, directorates, boards/PSUs, universities, 38 districts, corporations), each with a verification status. |
| [TIER2-SCHEMES.md](./TIER2-SCHEMES.md) | Tier-2 registry — projects, schemes, missions, citizen-service platforms and SPVs, including schemes researched with *no* dedicated portal. |
| [tamilnadu-sites.csv](./tamilnadu-sites.csv) | Machine-readable copy: `name, url, group, igod_type, status, detail, tier, cert_expires, emudhra`. |
| [docs/index.html](./docs/index.html) | Searchable GitHub Pages site (vanilla JS, loads the CSV at render time; tier + TLS/eMudhra filters). |
| [SECURITY-NOTES.md](./SECURITY-NOTES.md) | Hygiene log: hijacked/lapsed/spam-serving government domains, TLS certificate expiry findings, and the eMudhra CA-incident status for TN. |
| [tools/](./tools/) | Reproducible pipeline: `sweep_links.py` (link sweep), `verify_hosts.py` (DoH+HTTP), `cert_status.py` (merge TLS scan into the CSV) and the raw candidate list (`sweep-findings.csv`). |

## Snapshot (25 Oct 2026, after the homepage/sitemap link sweep)

- **441 entries** (Tier 1: 371 · Tier 2: 70) · **404 unique URLs** reachable or DNS-confirmed
- 334 live (HTTP 200 / redirect / bot-403) · 28 DNS-live but network-unreachable at check time · 10 server-error pages (HTTP 4xx/5xx/522) · 32 defunct/no-DNS/errored · 37 have no dedicated website (served by the TN portal)
- The sweep crawled all 316 inventory URLs (homepages + robots.txt + sitemaps), extracted 3,685 outbound hostnames, filtered to 748 new candidates, and added 88 verified TN-relevant hosts
- **TLS certificates scanned for all 389 hosts** (2026-10-25, openssl chain capture): **0 sites on the revoked eMudhra G3 intermediates**, 5 on the eMudhra/emSign **G1 watch-list** (`tamilnadupost.cept.gov.in`, `tnsericulture.tn.gov.in`, `ideunom.ac.in`, `cscl.co.in`, `tantea.nic.in`), 320 on unaffected CAs, and **24 with already-expired leaf certs** — expiry dates are the new `cert_expires` column, chain status the `emudhra` column
- IGOD org-type codes used for grouping: `SPORT` state portal · `E003` departments · `E004` directorates · `E013` commissions · `E051` statutory/autonomous bodies · `E011` boards/undertakings · `E059` PSUs/JVs · `E009` academies/institutions · `E042` districts · `SPMA` schemes/portals · `OTHR` others

## Reproducing the sweep

```bash
pip install requests
python3 tools/sweep_links.py            # crawl inventory homepages + robots/sitemaps
python3 tools/verify_hosts.py hosts.txt out.jsonl   # DoH + HTTP verify any host list
# TLS chain scan (uses eMudraImpacts' scanner), then merge into the CSV:
SCAN_OUT=results/tn-inventory SCAN_NO_WWW=1 python3 ../eMudraImpacts/scripts/scan_tls.py hosts.txt
EMUDRA_SCAN=../eMudraImpacts/results/tn-inventory/scan-all.csv python3 tools/cert_status.py
```

`tools/sweep-findings.csv` holds the last raw candidate list (host, TN-likelihood, discovering sources, sample links). All scripts are anonymous, unauthenticated public-page readers — no credentials, no crawling beyond declared sitemaps.

## Refreshing the IGOD dump

The directory API is a POST-based resolver. To re-dump the current Tamil Nadu listing:

```bash
curl -sk -X POST "https://www.india.gov.in/directory/web-directory/api" \
  -H "Content-Type: application/json" \
  -d '{"dataval":{"clientvalue":"client",
        "mustvalue":[{"fieldName":"category","fieldValue":"sg"},
                     {"fieldName":"state_id","fieldValue":"TN"}],
        "pageno":1,"pageSize":500,"shouldvalue":[],
        "querytype":"WebdirectoryCategorydetalsList"}}'
```

Swap `fieldValue` of `state_id` for any other state code (`AP`, `KA`, `KL`, …) to build the same directory for another state; `organizationtypewithCategory` (with `mustvalue: "sg"`) returns the category legend and per-state counts.

## Verification notes

- Liveness was checked with follow-redirect HTTP GETs; failures were re-tested with DNS-over-HTTPS to separate *defunct domains* from *hosts unreachable from the verification network* (NIC ranges — 164.100/16, 117.239/16, 103.59.64/22 — were heavily throttled during testing, so those entries are marked 🌐 *likely live* instead of dead).
- A strict-TLS pass (no insecure flag) validated 175+ hosts; the remainder mostly serve CCAIndia/eMudhra chains that fail stock CA bundles — a well-known quirk of `gov.in` hosting, not necessarily a site problem.
- The 25 Oct sweep surfaced several **hijacked or lapsed government-adjacent domains** (gambling spam on `maduraismartcity.in`, `tnteu.co.in`, `tnteuijer.com`; counterfeit-goods spam on `tnhrce.org`; injected spam links on the live `tnslurb.tn.gov.in`). See [SECURITY-NOTES.md](./SECURITY-NOTES.md).
- **eMudhra CA incident (revoked / fixed?):** no TN host ever served the revoked eMudhra G3 intermediates, so nothing needed remediation; 5 hosts remain on the still-trusted emSign G1 watch-list and should migrate at renewal. Incident tracking: [LogicIncZo/eMudraImpacts](https://github.com/LogicIncZo/eMudraImpacts).
- This is a public-information index only, compiled entirely from official sources and passive liveness checks — no credentials, no exploitation.

## License

[MIT](./LICENSE) © 2026 LogicIncZo
