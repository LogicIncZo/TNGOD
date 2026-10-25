#!/usr/bin/env python3
"""Link sweep for the TNGOD inventory.

Fetches every inventory homepage, its robots.txt and sitemaps, extracts every
outbound host, and reports hosts that are not yet in tamilnadu-sites.csv.

Public-information only: this reads public web pages, no authentication,
no crawling beyond homepage + robots.txt + declared sitemaps.

Usage:
  python3 tools/sweep_links.py                # full sweep
  python3 tools/sweep_links.py --limit 20     # smoke test
  python3 tools/sweep_links.py --workers 16
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.parse as up
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from requests.adapters import HTTPAdapter
except ImportError:  # pragma: no cover
    sys.exit("pip install requests")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "sweep-findings.csv")
RAW = os.path.join(HERE, "sweep-run.jsonl")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 TNGOD-sweep/1.0")

# Hosts that are never Tamil Nadu government infrastructure: social platforms,
# CDNs, analytics, fonts, marketplaces, standards bodies, generic SaaS.
NOISE = re.compile(
    r"(^|\.)("
    r"google\.[a-z.]+|googleapis\.com|gstatic\.com|googletagmanager\.com|"
    r"google-analytics\.com|doubleclick\.net|youtube\.com|youtu\.be|ytimg\.com|"
    r"facebook\.com|fb\.com|fbcdn\.net|instagram\.com|twitter\.com|x\.com|t\.co|"
    r"linkedin\.com|whatsapp\.com|wa\.me|telegram\.me|t\.me|pinterest\.[a-z.]+|"
    r"threads\.net|mastodon\.[a-z]+|"
    r"play\.google\.com|apps\.apple\.com|apple\.com|microsoft\.com|office\.com|"
    r"live\.com|outlook\.com|skype\.com|zoom\.us|"
    r"w3\.org|schema\.org|xmlns\.com|creativecommons\.org|archive\.org|"
    r"cloudflare\.com|cloudflareinsights\.com|jsdelivr\.net|cdnjs\.cloudflare\.com|"
    r"unpkg\.com|bootstrapcdn\.com|jquery\.com|fontawesome\.com|fonts\.googleapis\.com|"
    r"fonts\.gstatic\.com|use\.typekit\.net|adobe\.com|"
    r"hotjar\.com|clarity\.ms|bing\.com|yahoo\.com|duckduckgo\.com|"
    r"tawk\.to|elfsight\.com|userway\.org|unsplash\.com|maxcdn\.com|"
    r"drupal\.org|wikipedia\.org|wikimedia\.org|wordpress\.org|wordpress\.com|"
    r"blogspot\.com|gmail\.com|mail\.google\.com|"
    r"amazonaws\.com|akamaihd\.net|azureedge\.net|herokuapp\.com|web\.app|"
    r"firebase(app)?\.com|vercel\.app|netlify\.app|github\.io|github\.com|"
    r"bit\.ly|tinyurl\.com|change\.org|paypal\.com|razorpay\.com|"
    r"weatherwidget\.io|forecast7\.com|accuweather\.com|"
    r"fontawesome|bootstrap|cdn|static|assets|imgur\.com|flickr\.com|"
    r"vimeo\.com|dailymotion\.com|soundcloud\.com|spotify\.com|"
    r"datatables\.net|s3waas\.gov\.in|ccavenue\.com|demositeslive\.com|"
    r"w\.org|wix\.com|wixsite\.com|godaddy\.com|bigrock\.in|hostinger\.[a-z]+|"
    r"namecheap\.com|zoho\.com|zohocdn\.com|sendgrid\.net|mailchimp\.com|"
    r"sharethis\.com|addthis\.com|disqus\.com|gravatar\.com|recaptcha\.net|"
    r"gstatic\.com|payumoney\.com|instamojo\.com|billdesk\.com"
    r")$", re.I)

BARE_TLDS = {"gov.in", "nic.in", "in", "ac.in", "res.in", "org.in"}

# Central (GoI) infrastructure that TN pages commonly link to. Excluded from
# discovery because they are national, not Tamil Nadu digital infrastructure.
CENTRAL = re.compile(
    r"(^|\.)("
    r"india\.gov\.in|mygov\.in|goidirectory\.nic\.in|pgportal\.gov\.in|"
    r"digitalindia\.gov\.in|pmindia\.gov\.in|meity\.gov\.in|"
    r"dac\.gov\.in|agricoop\.nic\.in|agriinfra\.dac\.gov\.in|icar\.org\.in|"
    r"dahd\.gov\.in|fci\.gov\.in|moef\.gov\.in|cpcb\.gov\.in|"
    r"ugc\.ac\.in|deb\.ugc\.ac\.in|aicte-india\.org|aishe\.gov\.in|"
    r"swayam\.gov\.in|nptel\.ac\.in|nta\.ac\.in|"
    r"eshram\.gov\.in|labour\.gov\.in|epfindia\.gov\.in|"
    r"cybercrime\.gov\.in|nhrc\.nic\.in|pencil\.gov\.in|"
    r"amritmahotsav\.nic\.in|data\.gov\.in|indiapost\.gov\.in|"
    r"passportindia\.gov\.in|uidai\.gov\.in|incometax\.gov\.in|gst\.gov\.in|"
    r"mca\.gov\.in|rbi\.org\.in|sebi\.gov\.in|nseindia\.com|bseindia\.com"
    r")$", re.I)

# Infrastructure subdomains: not separate inventory entries.
INFRA_PREFIX = {
    "cdn", "static", "assets", "img", "images", "api", "ajax", "forms",
    "formbuilder", "mail", "webmail", "smtp", "ftp", "ns1", "ns2", "dns",
    "vpn", "proxy", "demo", "demosites", "staging", "test", "dev", "beta",
    "download", "downloads", "upload", "files", "status", "monitor",
    "analytics", "tracking", "ads", "pixel", "autodiscover", "cpanel",
}

# Parents whose subdomains are distinct services worth listing individually.
SERVICE_PARENTS = {"tn.gov.in", "tnega.org", "tn.nic.in", "tnrd.tn.gov.in"}

IPRE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
HOSTRE = re.compile(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)+$")
URL_IN_TEXT = re.compile(r"https?://[^\s\"'<>\)\]\}]+", re.I)


def load_inventory():
    rows = []
    with open(os.path.join(ROOT, "tamilnadu-sites.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            u = (r.get("url") or "").strip()
            if u.startswith("http"):
                rows.append((r.get("name", ""), u, r.get("status", "")))
    return rows


def norm_host(url_or_host):
    s = url_or_host.strip()
    if "//" in s:
        s = up.urlsplit(s).netloc
    s = s.split("@")[-1].split(":")[0].strip().lower().strip(".")
    if s.startswith("www."):
        s = s[4:]
    return s


def inventory_hosts(rows):
    hosts = set()
    for _, u, _ in rows:
        h = norm_host(u)
        if h:
            hosts.add(h)
    return hosts


def session():
    s = requests.Session()
    s.verify = False
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
    ad = HTTPAdapter(pool_connections=64, pool_maxsize=64, max_retries=0)
    s.mount("https://", ad)
    s.mount("http://", ad)
    return s


def fetch(sess, url, timeout=(8, 15), max_bytes=3_000_000):
    try:
        r = sess.get(url, timeout=timeout, allow_redirects=True, stream=True)
        chunks, size = [], 0
        for c in r.iter_content(65536):
            chunks.append(c)
            size += len(c)
            if size >= max_bytes:
                break
        body = b"".join(chunks)
        ctype = r.headers.get("content-type", "")
        text = ""
        if any(k in ctype for k in ("text", "html", "xml", "json")) or not ctype:
            text = body.decode(r.encoding or "utf-8", errors="replace")
        return {"url": url, "final_url": r.url, "code": r.status_code,
                "ctype": ctype, "text": text, "bytes": size}
    except Exception as e:
        return {"url": url, "code": 0, "error": type(e).__name__, "text": ""}


def extract_hosts(page, base_url):
    """Return {host: [contexts]} found in HTML/text."""
    out = {}
    if not page.get("text"):
        return out
    text = page["text"][:2_000_000]
    base = page.get("final_url") or base_url

    # href/src/action/data-* attributes
    for m in re.finditer(r'(?:href|src|action|data-href|data-url|content)\s*=\s*["\']([^"\']{2,500})["\']', text, re.I):
        raw = html.unescape(m.group(1)).strip()
        if not raw or raw.startswith(("#", "javascript:", "mailto:", "tel:", "data:")):
            continue
        try:
            u = up.urljoin(base, raw)
        except ValueError:
            continue
        if not u.lower().startswith(("http://", "https://")):
            continue
        h = norm_host(u)
        if h and len(h) < 100:
            out.setdefault(h, []).append(u[:200])

    # absolute URLs appearing in scripts/JSON
    for m in URL_IN_TEXT.finditer(text):
        u = html.unescape(m.group(0)).rstrip(".,;")
        h = norm_host(u)
        if h and len(h) < 100:
            out.setdefault(h, []).append(u[:200])
    return out


def sitemap_hosts(sess, base_url):
    """robots.txt -> Sitemap: entries -> <loc> hosts (max 3 sitemaps)."""
    hosts = {}
    root = "{0.scheme}://{0.netloc}".format(up.urlsplit(base_url))
    if not root.startswith("http"):
        return hosts
    robots = fetch(sess, root + "/robots.txt", max_bytes=200_000)
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots.get("text") or "")
    if not maps:
        maps = [root + "/sitemap.xml"]
    for sm in maps[:3]:
        page = fetch(sess, html.unescape(sm.strip()), max_bytes=2_000_000)
        if page.get("code") != 200 or not page.get("text"):
            continue
        for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", page["text"], re.I):
            h = norm_host(html.unescape(loc))
            if h and len(h) < 100:
                hosts.setdefault(h, []).append(html.unescape(loc)[:200])
    return hosts


def is_candidate(host, known):
    if not host or host in known or IPRE.match(host) or not HOSTRE.match(host):
        return False
    if host in BARE_TLDS or NOISE.search(host) or CENTRAL.search(host):
        return False
    if host.endswith((".jpg", ".png", ".gif", ".svg", ".css", ".js", ".pdf", ".zip")):
        return False
    if host.split(".")[0] in INFRA_PREFIX:
        return False
    # A subdomain of a known institution is the same site, not a new entry —
    # except under generic service parents where each subdomain is a portal.
    for k in known:
        if host.endswith("." + k) and k not in SERVICE_PARENTS:
            return False
    return True


def likely_tn(host):
    labels = host.split(".")
    tld = ".".join(labels[-2:])
    if tld in ("gov.in", "nic.in", "ac.in", "res.in", "org.in", "co.in", "net.in", "edu.in", "mil.in"):
        if host.endswith(("tn.gov.in", "tn.nic.in")):
            return "high"
        if any(l in ("tn", "tamilnadu", "tamil", "chennai", "madras") for l in labels):
            return "high"
        if tld == "nic.in":
            return "medium"  # could be central; needs review
        return "medium"
    if host.endswith((".in", ".com", ".org", ".net", ".co.in")):
        if any(k in host for k in ("tamil", "tn", "chennai", "madras", "madurai", "coimbatore",
                                   "tiruchi", "trichy", "salem", "tirunelveli", "vellore",
                                   "erode", "thanjavur", "kanyakumari", "nilgiri", "ooty")):
            return "medium"
        return "low"
    return "low"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--only-live", action="store_true", default=True)
    args = ap.parse_args()

    rows = load_inventory()
    if args.limit:
        rows = rows[: args.limit]
    known = inventory_hosts(load_inventory())

    sess = session()
    found = {}          # host -> {"sources": set, "contexts": list, "n": int}
    stats = {"targets": len(rows), "ok": 0, "fail": 0, "hosts_seen": 0}

    def work(item):
        name, url, status = item
        p = fetch(sess, url)
        res = {"name": name, "url": url, "status": status,
               "code": p.get("code"), "final_url": p.get("final_url", ""),
               "error": p.get("error", ""), "hosts": {}}
        if p.get("code"):
            res["hosts"] = extract_hosts(p, url)
            if p.get("code") == 200:
                try:
                    for h, ctx in sitemap_hosts(sess, p.get("final_url") or url).items():
                        res["hosts"].setdefault(h, []).extend(ctx)
                except Exception:
                    pass
        return res

    t0 = time.time()
    raw_f = open(RAW, "w", encoding="utf-8")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(work, it): it for it in rows}
        done = 0
        for fut in as_completed(futs):
            res = fut.result()
            done += 1
            if res["code"]:
                stats["ok"] += 1
            else:
                stats["fail"] += 1
            for h, ctx in res["hosts"].items():
                stats["hosts_seen"] += 1
                if not is_candidate(h, known):
                    continue
                rec = found.setdefault(h, {"sources": set(), "contexts": [], "n": 0})
                rec["sources"].add(res["name"] or res["url"])
                rec["n"] += len(ctx)
                for c in ctx:
                    if len(rec["contexts"]) < 3 and c not in rec["contexts"]:
                        rec["contexts"].append(c)
            if done % 25 == 0:
                print(f"  {done}/{len(rows)} fetched, {len(found)} candidate hosts", flush=True)
            raw_f.write(json.dumps({
                "url": res["url"], "code": res["code"],
                "final_url": res.get("final_url", ""),
                "error": res.get("error", ""),
                "hosts_found": len(res["hosts"])}) + "\n")
    raw_f.close()

    elapsed = time.time() - t0

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["host", "likely_tn", "sources_count", "sources", "sample_links"])
        for h, rec in sorted(found.items(), key=lambda kv: (-len(kv[1]["sources"]), kv[0])):
            w.writerow([h, likely_tn(h), len(rec["sources"]),
                        "; ".join(sorted(rec["sources"])[:6]),
                        " | ".join(rec["contexts"])])

    print(json.dumps({"elapsed_s": round(elapsed, 1), **stats,
                      "candidate_hosts": len(found)}, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
