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

## Methodology

All observations are from anonymous, unauthenticated HTTP(S) GET requests and
DNS-over-HTTPS lookups (`1.1.1.1`), reproducible with
`tools/sweep_links.py` and `tools/verify_hosts.py` in this repository.
No credentials, no scanning beyond homepage fetches, no exploitation.
