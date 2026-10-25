#!/usr/bin/env python3
"""Verify a list of hosts: DNS (DoH 1.1.1.1) + HTTP(S) liveness + <title>.

Usage: python3 tools/verify_hosts.py hosts.txt out.json
Reads one host per line; writes JSON lines:
  {"host":..., "dns": "ok|nxdomain|timeout|error", "ip":..., "code":...,
   "final_url":..., "title":..., "err":...}

Public information only: anonymous GET requests, no credentials.
"""
import concurrent.futures as cf
import json
import re
import sys

import requests
import urllib3
urllib3.disable_warnings()

DNS = "https://1.1.1.1/dns-query?name={h}&type=A"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def doh(host, sess):
    try:
        r = sess.get(DNS.format(h=host), headers={"accept": "application/dns-json"},
                     timeout=6, verify=True)
        j = r.json()
        st = j.get("Status", -1)
        if st == 3:
            return "nxdomain", ""
        if st == 0 and j.get("Answer"):
            for a in j["Answer"]:
                if a.get("type") == 1:
                    return "ok", a["data"]
            return "no-a", ""
        return "no-a", ""
    except Exception as e:
        return "doh-" + type(e).__name__, ""


def http(host, sess):
    out = {"code": 0, "final_url": "", "title": "", "err": ""}
    for scheme in ("https", "http"):
        url = f"{scheme}://{host}/"
        try:
            r = sess.get(url, timeout=(8, 15), allow_redirects=True, verify=False,
                         headers={"User-Agent": UA})
            out["code"] = r.status_code
            out["final_url"] = r.url
            m = TITLE.search(r.text[:300_000])
            if m:
                out["title"] = re.sub(r"\s+", " ", m.group(1)).strip()[:120]
            if scheme == "https" and r.history:
                out["redirect"] = r.history[0].status_code
            return out
        except Exception as e:
            out["err"] = type(e).__name__
    return out


def one(host):
    s = requests.Session()
    dns, ip = doh(host, s)
    rec = {"host": host, "dns": dns, "ip": ip}
    if dns == "nxdomain":
        rec.update({"code": 0, "final_url": "", "title": "", "err": "nxdomain"})
    else:
        rec.update(http(host, s))
    return rec


def main():
    hosts = [h.strip().lower() for h in open(sys.argv[1]) if h.strip()]
    out = open(sys.argv[2], "w")
    with cf.ThreadPoolExecutor(max_workers=16) as pool:
        futs = {pool.submit(one, h): h for h in hosts}
        for f in cf.as_completed(futs):
            rec = f.result()
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            print(f"{rec['host']:45s} dns={rec['dns']:9s} code={rec.get('code',0):3d} "
                  f"{rec.get('title','')[:60]}", flush=True)


if __name__ == "__main__":
    main()
