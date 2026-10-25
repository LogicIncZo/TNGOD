# Security & Hygiene Notes — Tamil Nadu Government Domains

Observed during the 2026-10-25 link sweep (anonymous HTTP checks + DNS-over-HTTPS).
This is a public-interest observation log from passive liveness checks — no
penetration testing, no exploit content. Website owners are encouraged to verify
and remediate. Dates are the check date.

## ⚠ Hijacked / squatted / spam-serving domains

| Domain | Observation (2026-10-25) | Notes |
|---|---|---|
| `maduraismartcity.in` | Whole domain serves "Aviator Game" gambling content | The Madurai Smart City SPV domain has lapsed and been re-registered by a gambling operation. Listed as **dead** in the inventory. |
| `tnhrce.org` | Serves Japanese counterfeit-goods spam (ノースフェイス shop) | The Hindu Religious & Charitable Endowments Dept domain has lapsed/squatted. The department's live site is `hrce.tn.gov.in`. |
| `tnteu.co.in` | Serves "GELORA188" gambling portal | Tamil Nadu Teachers Education University alternate domain hijacked. |
| `tnteuijer.com` | Serves "HK Pools" gambling portal | TNTEU journal/exam-adjacent domain hijacked. |
| `tnslurb.tn.gov.in` | Official site serves **16 injected Turkish gambling spam links** ("canli mac izle") on its homepage | Likely CMS compromise of a live .gov.in host — needs urgent remediation. |
| `tnclimatechangemission.in` | Serves an Indonesian-language default web-server page ("WOE! SSL Jangan Lupa Di-install!") | Site misconfigured or taken over. |

## ⚠ Parked, lapsed or look-alike domains

| Domain | Observation |
|---|---|
| `cmda.tnic.in` | Look-alike of `cmdachennai.gov.in` linked from the official CMDA site; serves a hosting "Domain Default page". Do not trust content on it. |
| `chennaivizha.com` | "is for sale" — lapsed. |
| `msutnset.com` | "Website Disabled" — lapsed (MSU SET exam portal). |
| `ootyflowershow.in` | "Coming Soon" placeholder. |
| `tngts2026.com` | Appwrite default page (broken deployment). |
| `guidancetn.com` | DNS alive but connection failing; the live Guidance Tamil Nadu portal is `investingintamilnadu.com`. |
| `tnarchives.tn.gov.in` | HTTP 404 — site offline. |
| `tnvat.gov.in` | NXDOMAIN — retired commercial-tax portal. |

## Legitimate domains verified during the sweep

`tnrajbhavan.gov.in` (Lok Bhavan / Raj Bhavan — the `rajbhavan.tn.gov.in` guess has no DNS),
`hcmadras.tn.gov.in` (Madras High Court's current portal; `mhc.tn.gov.in` legacy still resolves),
`hrce.tn.gov.in` (HR&CE Dept current site).

## TLS certificate status & the eMudhra CA incident (scanned 2026-10-25)

**Revoked / fixed? — Tamil Nadu is effectively in the clear.**

- **Revoked eMudhra G3 intermediates (the compromised chains, revoked 2026-10-18/19):** **0 TN inventory hosts** present them. There was nothing to fix — no TN site was on the affected chains.
- **eMudhra/emSign G1-family watch-list (root still trusted; Chrome "evaluating" removal):** **5 hosts** currently serve G1-family chains and should migrate at their next renewal:

| Host | Leaf issuer | Chain | Leaf expires |
|---|---|---|---|
| `tamilnadupost.cept.gov.in` | EM DV TLS CA - G2A-1 | G2A-1 → emSign Root TLS CA - G1 (x-sign) → emSign Root CA - G1 | 2026-12-27 |
| `tnsericulture.tn.gov.in` | EM DV TLS CA - G2A-1 | same G1 cross-sign path | 2026-12-09 |
| `ideunom.ac.in` | EM DV TLS CA - G2A-1 | same G1 cross-sign path | **expired 2026-05-10** |
| `cscl.co.in` | emSign SSL CA - G1 | legacy-direct G1 | **expired 2026-10-20** (site also down) |
| `tantea.nic.in` | emSign SSL CA - G1 | legacy-direct G1 | **expired 2026-05-25** |

  Full methodology and incident context: [LogicIncZo/eMudraImpacts](https://github.com/LogicIncZo/eMudraImpacts) (per-host evidence in `results/tn-inventory/`).

## ⚠ Expired leaf certificates observed (2026-10-25)

24 inventory hosts presented an **already-expired** leaf certificate during the TLS scan
(`tools/cert_status.py` flags them red in the web directory). Highlights:

- `tnregipayment.gov.in` — expired **2018-03-12**, still serving HTTP 200 (GlobalSign chain)
- `prisons.tn.gov.in` (expired 2024-05-29), `tahdco.tn.gov.in` (2024-09-16), `tnarchives.tn.gov.in` (2024-09-16)
- `textbookcorp.tn.gov.in` (2025-05-02), `mrb.tn.gov.in` (2026-01-29), `ssp.tn.gov.in` (2026-01-24)
- Plus ~17 more within 2026 — including several that clearly use short-lived Let's Encrypt
  certificates (`YR1`/`YE1`/`R10`-`R13` issuers, ~6-day validity, e.g. `rtionline.tn.gov.in`,
  `tncu.tn.gov.in`, `tnpoly.in`) where an expiry at scan time is routine auto-renewal churn, not neglect.
  The genuine outliers are the fixed-date certs listed above.

The complete machine-readable list is in `tamilnadu-sites.csv` (`cert_expires` column) and
`eMudraImpacts/results/tn-inventory/scan-all.csv` (`expired=YES`).

## Methodology

All observations are from anonymous, unauthenticated HTTP(S) GET requests and
DNS-over-HTTPS lookups (`1.1.1.1`), reproducible with
`tools/sweep_links.py` and `tools/verify_hosts.py` in this repository.
No credentials, no scanning beyond homepage fetches, no exploitation.
