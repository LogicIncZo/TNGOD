#!/usr/bin/env python3
"""Passive security-posture collection for every site in tamilnadu-sites.csv.

Strictly non-intrusive: DNS lookups (A/AAAA/MX/TXT/DMARC/DNSSEC) plus at most
two ordinary HTTP GETs per host (http:// and https:// of the bare site root),
identical to what a browser visit produces. No fuzzing, no brute force, no
exploitation. Output feeds per-site markdown reports.

Writes:
  results/posture/posture.jsonl      one line per host
  results/posture/data/<slug>.json   merged CSV row + TLS scan row + posture row
"""
import concurrent.futures as cf
import csv
import faulthandler
import json
import os
import re
import socket
import ssl
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import urllib3

import dns.flags
import dns.message
import dns.query
import dns.rdatatype
import dns.resolver

urllib3.disable_warnings()

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "results", "posture")
DATA = os.path.join(OUT, "data")
EMUDRA_SCAN = os.path.join(os.path.dirname(ROOT), "eMudraImpacts", "results",
                           "tn-inventory", "scan-all.csv")

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
SEC_HEADERS = ["strict-transport-security", "content-security-policy",
               "x-frame-options", "x-content-type-options",
               "referrer-policy", "permissions-policy"]

_lock = threading.Lock()
_done = 0


def log(msg):
    with _lock:
        print(msg, file=sys.stderr, flush=True)


def url_host(u):
    return re.sub(r"^https?://", "", u).split("/")[0].split(":")[0].lower().strip()


def clean_host(h):
    return re.sub(r"[^a-z0-9.-]", "_", h)


# ---------------------------------------------------------------- DNS

_res = dns.resolver.Resolver()
_res.timeout = 3
_res.lifetime = 6
_ns = _res.nameservers[0]


def _q(name, rdtype):
    q = dns.message.make_query(name, rdtype)
    resp = dns.query.udp(q, _ns, timeout=3)
    return resp


def dns_probe(host):
    out = {"a": [], "aaaa": [], "mx": [], "txt": [], "dmarc": [], "spf": None,
           "dnssec": None, "error": None}
    try:
        resp = _q(host, "A")
        out["a"] = sorted({rr.address for rr in resp.answer[0]} if resp.answer else [])
    except dns.resolver.NXDOMAIN:
        out["error"] = "NXDOMAIN"
        return out
    except Exception as e:
        out["error"] = type(e).__name__
    for rd, key in (("AAAA", "aaaa"), ("MX", "mx")):
        try:
            resp = _q(host, rd)
            if rd == "MX":
                out[key] = sorted({f"{rr.preference} {rr.exchange}" for rr in resp.answer[0]}
                                  if resp.answer else [])
            else:
                out[key] = sorted({rr.address for rr in resp.answer[0]} if resp.answer else [])
        except Exception:
            pass
    try:
        resp = _q(host, "TXT")
        if resp.answer:
            out["txt"] = [b"".join(s.strings).decode("utf-8", "replace")
                          for s in resp.answer[0]]
    except Exception:
        pass
    apex = host.split(".", 1)[1] if host.startswith("www.") and host.count(".") >= 2 else host
    if apex != host:
        try:
            resp = _q(apex, "TXT")
            if resp.answer:
                out["txt"] += [b"".join(s.strings).decode("utf-8", "replace")
                               for s in resp.answer[0]]
        except Exception:
            pass
    for zone in (host, apex):
        try:
            resp = _q("_dmarc." + zone, "TXT")
            if resp.answer:
                out["dmarc"] = [b"".join(s.strings).decode("utf-8", "replace")
                                for s in resp.answer[0]]
                break
        except Exception:
            pass
    for t in out["txt"]:
        if t.lower().startswith("v=spf1"):
            out["spf"] = t
            break
    # DNSSEC: ask with DO bit; RRSIG in the answer or AD flag means signed path
    try:
        q = dns.message.make_query(host, "A", want_dnssec=True)
        resp = dns.query.udp(q, _ns, timeout=3)
        has_rrsig = any(rr.rdtype == dns.rdatatype.RRSIG for rr in resp.answer)
        ad = bool(resp.flags & dns.flags.AD)
        out["dnssec"] = "RRSIG" if has_rrsig else ("AD" if ad else None)
    except Exception:
        pass
    return out


# ---------------------------------------------------------------- HTTP

def _get(url, follow, timeout=8):
    """One GET. Returns dict of observed facts. No exploitation, no parsing
    beyond headers/title/meta-generator (static content a browser renders)."""
    hops, resp, err = [], None, None
    cur = url
    for _ in range(6 if follow else 1):
        try:
            req = urllib.request.Request(cur, headers={"User-Agent": UA})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            break
        except urllib.error.HTTPError as e:
            resp = e
            break
        except Exception as e:
            err = f"{type(e).__name__}: {e}"[:200]
            break
    if resp is None:
        return {"error": err, "status": None}
    status = resp.getcode()
    headers = {k.lower(): v for k, v in resp.headers.items()}
    body = b""
    try:
        body = resp.read(200_000)
    except Exception:
        pass
    title = ""
    m = re.search(rb"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    if m:
        title = re.sub(r"\s+", " ", m.group(1).decode("utf-8", "replace")).strip()[:120]
    gen = ""
    m = re.search(rb'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)',
                  body, re.I)
    if m:
        gen = m.group(1).decode("utf-8", "replace")[:80]
    cookies = [c for c in resp.headers.get_all("Set-Cookie") or []]
    return {
        "status": status,
        "url": resp.geturl(),
        "headers": {k: headers[k] for k in headers if k in
                    SEC_HEADERS + ["server", "x-powered-by", "x-aspnet-version",
                                   "x-aspnetmvc-version", "set-cookie", "location",
                                   "via", "x-cache"]},
        "all_header_names": sorted(headers),
        "title": title,
        "generator": gen,
        "content_type": headers.get("content-type", "")[:60],
        "body_bytes": len(body),
        "cookies": {"total": len(cookies),
                    "no_secure": sum("secure" not in c.lower() for c in cookies),
                    "no_httponly": sum("httponly" not in c.lower() for c in cookies),
                    "no_samesite": sum("samesite" not in c.lower() for c in cookies)},
        "error": None,
    }


def http_probe(url, scheme):
    out = {"scheme": scheme, "status": None, "final_url": None, "redirects": [],
           "error": None}
    try:
        cur = url
        for hop in range(5):
            r = _get(cur, follow=False, timeout=8)
            if r.get("error"):
                out["error"] = r["error"]
                break
            out["status"] = r["status"]
            if scheme == "https" and 300 <= (r["status"] or 0) < 400 and \
                    r["headers"].get("location"):
                nxt = urllib.parse.urljoin(cur, r["headers"]["location"])
                out["redirects"].append({"from": cur, "to": nxt,
                                         "status": r["status"]})
                if hop == 4:
                    out["error"] = "redirect loop (5 hops)"
                    break
                cur = nxt
                continue
            out["final_url"] = r["url"]
            out.update({k: r[k] for k in ("headers", "all_header_names", "title",
                                          "generator", "content_type", "body_bytes",
                                          "cookies") if k in r})
            break
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"[:200]
    return out


# ---------------------------------------------------------------- grade

def grade(row):
    """Deterministic posture grade + finding list (severity, text)."""
    f, sc = [], 100
    live = row.get("http", {}).get("https", {}).get("status") == 200 or \
        row.get("http", {}).get("http", {}).get("status") == 200
    tls_ok = row.get("tls", {}).get("tls") == "ok"
    expired = row.get("tls", {}).get("expired", "").upper() == "YES"
    if not row.get("dns", {}).get("a") and not row.get("dns", {}).get("aaaa"):
        f.append(("High", "Domain does not resolve (no A/AAAA record)."))
        sc -= 40
    if expired:
        f.append(("High", "TLS certificate has EXPIRED."))
        sc -= 40
    elif not tls_ok and row.get("dns", {}).get("a"):
        f.append(("High", "HTTPS handshake failed (no usable TLS)."))
        sc -= 30
    if row.get("tls", {}).get("verify_code", "").startswith("10"):
        f.append(("High", "Certificate chain does not verify (expired/mismatch)."))
        sc -= 30
    em = row.get("csv", {}).get("emudhra", "")
    if em == "g3-compromised":
        f.append(("Critical", "Chain contains a REVOKED eMudhra G3 intermediate "
                              "(emSign G3 roots removed 2026-10-27)."))
        sc -= 60
    elif em == "g1-watch":
        f.append(("Medium", "Chain uses emSign Root CA - G1 (Chrome-trust "
                            "watch-list; G3 roots already removed)."))
        sc -= 10
    h = row.get("http", {}).get("https", {})
    hdrs = h.get("headers", {})
    if h.get("status") == 200:
        if "strict-transport-security" in hdrs:
            sc += 0
        else:
            f.append(("Medium", "No HSTS header on the HTTPS response."))
            sc -= 10
        if "content-security-policy" not in hdrs:
            f.append(("Low", "No Content-Security-Policy header."))
            sc -= 8
        if "x-frame-options" not in hdrs and "frame-ancestors" not in \
                hdrs.get("content-security-policy", ""):
            f.append(("Low", "No clickjacking protection (X-Frame-Options / "
                             "CSP frame-ancestors)."))
            sc -= 8
        if "x-content-type-options" not in hdrs:
            f.append(("Info", "No X-Content-Type-Options: nosniff."))
            sc -= 3
        if "referrer-policy" not in hdrs:
            f.append(("Info", "No Referrer-Policy header."))
            sc -= 2
        ck = h.get("cookies", {})
        if ck.get("total") and (ck.get("no_secure") or ck.get("no_httponly")):
            f.append(("Medium", f"Cookies without Secure/HttpOnly flags "
                                f"({ck['no_secure']} without Secure, "
                                f"{ck['no_httponly']} without HttpOnly)."))
            sc -= 10
    elif live and h.get("status"):
        f.append(("Info", f"HTTPS root returns HTTP {h.get('status')} "
                          f"(not a normal 200 landing page)."))
    http_resp = row.get("http", {}).get("http", {})
    if http_resp.get("status") == 200:
        f.append(("Medium", "Plain http:// serves content (no redirect to "
                            "https://)."))
        sc -= 10
    d = row.get("dns", {})
    if d.get("a") or d.get("aaaa"):
        if not d.get("dmarc"):
            f.append(("Low", "No DMARC record (_dmarc TXT)."))
            sc -= 5
        if not d.get("spf"):
            f.append(("Low", "No SPF record on the apex TXT set."))
            sc -= 5
        if d.get("dnssec") is None:
            f.append(("Info", "Zone does not appear to be DNSSEC-signed."))
            sc -= 2
    srv = (h.get("headers", {}).get("server", "") or "")
    if srv and re.search(r"\d+\.\d+", srv):
        f.append(("Info", f"Server header discloses version: {srv!r}."))
        sc -= 2
    if h.get("headers", {}).get("x-powered-by"):
        f.append(("Info", f"X-Powered-By discloses stack: "
                          f"{h['headers']['x-powered-by']!r}."))
        sc -= 2

    sc = max(0, min(100, sc))
    g = "A" if sc >= 90 else "B" if sc >= 75 else "C" if sc >= 60 else \
        "D" if sc >= 40 else "F"
    if not live:
        g = "n/a (site not live)"
    return {"score": sc, "grade": g, "findings": f}


# ---------------------------------------------------------------- main

def load_tls():
    tls = {}
    with open(EMUDRA_SCAN, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            h = (r["host"] or "").lower()
            if h:
                tls[h] = r
    return tls


def scan_site(rec):
    global _done
    idx, row, tls = rec
    host = url_host(row["url"])
    slug = clean_host(host)
    out_path = os.path.join(DATA, f"{idx:03d}-{slug}.json")
    if os.path.exists(out_path):
        with _lock:
            _done += 1
        return None
    base = re.sub(r"^https?://", "", row["url"]).split("/")[0]
    entry = {"idx": idx, "host": host, "url": row["url"], "name": row["name"],
             "group": row["group"], "tier": row["tier"],
             "csv_status": row["status"], "csv_detail": row["detail"],
             "csv_cert_expires": row.get("cert_expires", ""),
             "csv_emudhra": row.get("emudhra", ""),
             "tls": tls or {}, "dns": {}, "http": {}}
    try:
        entry["dns"] = dns_probe(host)
    except Exception as e:
        entry["dns"] = {"error": f"probe-crash {type(e).__name__}"}
    for scheme in ("https", "http"):
        try:
            entry["http"][scheme] = http_probe(f"{scheme}://{base}/", scheme)
        except Exception as e:
            entry["http"][scheme] = {"error": f"probe-crash {type(e).__name__}",
                                     "status": None}
    entry["posture"] = grade(entry)
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(entry, f, indent=1)
    os.rename(tmp, out_path)
    with _lock:
        _done += 1
        if _done % 25 == 0:
            log(f"[{_done}/441] {host} grade={entry['posture']['grade']}")
    return entry


def main():
    os.makedirs(DATA, exist_ok=True)
    socket.setdefaulttimeout(10)
    faulthandler.dump_traceback_later(180, repeat=True, file=sys.stderr)
    tls = load_tls()
    with open(os.path.join(ROOT, "tamilnadu-sites.csv"), newline="",
              encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    jobs = []
    for i, row in enumerate(rows, 1):
        host = url_host(row["url"])
        # scan-all.csv may key on bare host or www variant
        t = tls.get(host) or tls.get(host.replace("www.", "", 1) if
                                     host.startswith("www.") else "www." + host) or {}
        jobs.append((i, row, t))
    results = []
    with cf.ThreadPoolExecutor(20) as ex:
        for res in ex.map(scan_site, jobs):
            if res:
                results.append(res)
    faulthandler.cancel_dump_traceback_later()
    with open(os.path.join(OUT, "posture.jsonl"), "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    grades = {}
    for r in results:
        g = r["posture"]["grade"]
        grades[g] = grades.get(g, 0) + 1
    log(f"DONE {len(results)} new + resume; grades of new: {json.dumps(grades, sort_keys=True)}")


if __name__ == "__main__":
    main()
