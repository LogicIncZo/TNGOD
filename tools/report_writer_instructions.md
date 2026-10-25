# Report-writer instructions (shared by all subagents)

You write one passive security-posture report per website, in Markdown, from
pre-collected data. You do NOT access the network under any circumstances.
No curl, no dig, no requests, no WebFetch — every fact must come from the
JSON files you are given. If a fact is absent from the JSON, write
"not observed".

## Source of truth

Each input file `results/posture/data/NNN-<host>.json` is one site. Key
fields:

- `idx`, `host`, `url`, `name`, `group`, `tier` — inventory identity
- `csv_status` (live/dead), `csv_detail`, `csv_cert_expires`, `csv_emudhra`
  (unaffected | g1-watch | g3-compromised) — from the project's earlier sweep
- `tls` — from the eMudraImpacts chain scan: `leaf_cn`, `leaf_issuer`,
  `notBefore`, `notAfter`, `chain_roots`, `chain_issuers`, `verify_code`,
  `http_status`, `tls` ("ok"/failed), `expired` ("YES"/"no"/"")
  (may be empty if TLS was never observed)
- `dns` — `a`, `aaaa`, `mx`, `txt`, `spf`, `dmarc`, `dnssec`, `error`
- `http.https` / `http.http` — `status`, `final_url`, `redirects`,
  `headers`, `title`, `generator`, `content_type`, `body_bytes`, `cookies`,
  `error`
- `posture` — precomputed `grade` (A–F or "n/a (site not live)"), `score`,
  and `findings` (list of [severity, text])

## Output

For each input `NNN-<host>.json` write `reports/NNN-<host>.md` — same path
with .md. Use this exact skeleton:

```markdown
# <name> (<host>)

**Posture grade: <grade> (<score>/100)** · Group: <group> · Tier: <tier> ·
Inventory status: <csv_status>

> Passive observation only (DNS lookups + two HTTP GETs + the earlier TLS
> chain scan). No exploitation was attempted. Data as of 2026-10-25.

## Availability

- HTTPS root: <status, final_url, redirect chain or error>
- HTTP root: <status, whether it redirects to https, or error>
- Landing page title: <title or "not observed">

## TLS / certificate

- Leaf: <leaf_cn>, issued by <leaf_issuer>, valid <notBefore> → <notAfter>
- Verification: <verify_code>; <expired YES/NO>
- Chain roots: <chain_roots>
- CA family: <csv_emudhra with one-line meaning, or "no TLS observed">

## HTTP security headers (HTTPS response)

| Header | Present |
|---|---|
| Strict-Transport-Security | ✅ value / ❌ absent |
| Content-Security-Policy | … |
| X-Frame-Options | … |
| X-Content-Type-Options | … |
| Referrer-Policy | … |
| Permissions-Policy | … |

## Fingerprinting exposure

- Server: <value or "not disclosed">
- X-Powered-By: <value or "not disclosed">
- Meta generator: <value or "not disclosed">
- Cookies: <total N; flag counts if any unflagged>

## DNS / email hygiene

- A: <addresses> · AAAA: <addresses or none>
- MX: <count or none>
- SPF: <record or "absent">
- DMARC: <policy line or "absent">
- DNSSEC: <signed (RRSIG/AD) or "not signed">

## Findings

1. **[<severity>]** <finding text>
(continue for every finding in posture.findings, in order)

## Recommendations

- <one actionable bullet per High/Critical/Medium finding, e.g. "Publish a
  DMARC policy and an SPF record", "Add HSTS", "Renew the certificate">
- <one line for Low/Info clusters, e.g. "Add CSP, X-Frame-Options and
  Referrer-Policy headers">
```

## Rules

1. Reproduce `posture.grade`, `posture.score` and every `posture.findings`
   entry verbatim (you may lightly polish wording, never change meaning or
   severity). Do not invent findings the JSON does not contain.
2. If the site is not live (no DNS, no TLS, non-200 HTTPS, or
   `csv_status != live`), compress Availability/TLS/headers/DNS into a short
   **Postmortem** section explaining the failure mode from the data (e.g.
   NXDOMAIN, TLS handshake refused, HTTP 404/502), keep the findings list,
   and drop Recommendations down to 1–3 bullets. Title line gets
   "*(site down at scan time)*" after the host.
3. When `csv_emudhra` is `g3-compromised`, state plainly that the chain
   matched a REVOKED eMudhra G3 intermediate (emSign G3 roots removed
   2026-10-27) and the site needs a replacement certificate urgently.
   When `g1-watch`, state the chain uses emSign Root CA - G1 which is on the
   Chrome "evaluating" watch list.
4. Keep reports 35–80 lines. Use the JSON's `redirects` list to describe the
   redirect chain compactly (http→https→www etc.).
5. Never run network tools. Never modify anything outside `reports/`.
6. Report file count at the end of your final message: "wrote N/N reports".
