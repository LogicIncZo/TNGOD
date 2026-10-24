# TNGOD — Tamil Nadu Government Online Directory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Searchable web directory](https://img.shields.io/badge/search-web%20directory-2ea44f)](https://logicinczo.github.io/TNGOD/)
[![Data source: IGOD](https://img.shields.io/badge/source-IGOD%20%C2%B7%20india.gov.in-0969da)](https://www.india.gov.in/directory/web-directory)
[![URL-verified](https://img.shields.io/badge/URL_verified-24_Oct_2026-orange)](./TAMILNADU.md)

A comprehensive, URL-verified directory of Tamil Nadu government websites, built from the official **IGOD** (Integrated Government Online Directory) listing and cross-checked against the Tamil Nadu state portal.

> IGOD lives at [igod.gov.in](https://igod.gov.in) and is now served by the National Portal's
> [Web Directory](https://www.india.gov.in/directory/web-directory) (State/UTs → Tamil Nadu).
> The India Portal is maintained by NIC under the Digital India programme.

## 🔎 Searchable web directory

Browse and filter the directory at **https://logicinczo.github.io/TNGOD/** — a dependency-free client-side search over the dataset (by name, URL, group, and verification status), served by GitHub Pages from [`docs/`](./docs/index.html) with no tracking.

## Files

| File | Contents |
|---|---|
| [TAMILNADU.md](./TAMILNADU.md) | The main directory — 339 organizations grouped by sector (departments, directorates, boards/PSUs, universities, 38 districts, corporations, e-governance portals), each with a verification status. |
| [tamilnadu-sites.csv](./tamilnadu-sites.csv) | Machine-readable copy: `name, url, group, igod_type, status, detail`. |
| [docs/index.html](./docs/index.html) | Searchable GitHub Pages site (vanilla JS, loads the CSV at render time). |

## Snapshot (24 Oct 2026)

- **339 entries** · **265 unique URLs** reachable or DNS-confirmed
- 251 live (HTTP 200 / redirect / bot-403) · 18 DNS-live but network-unreachable at check time · 33 defunct/no-DNS · 37 have no dedicated website (served by the TN portal)
- IGOD org-type codes used for grouping: `SPORT` state portal · `E003` departments · `E004` directorates · `E013` commissions · `E051` statutory/autonomous bodies · `E011` boards/undertakings · `E059` PSUs/JVs · `E009` academies/institutions · `E042` districts · `SPMA` schemes/portals · `OTHR` others

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
- This is a public-information index only, compiled entirely from official sources.

## License

[MIT](./LICENSE) © 2026 LogicIncZo
