#!/usr/bin/env python3
"""Merge TLS certificate status into tamilnadu-sites.csv.

Reads the eMudraImpacts chain-scan output (openssl s_client chains for every
inventory host) and adds two columns:

  cert_expires — leaf notAfter as YYYY-MM-DD (empty when TLS was not observed)
  emudhra      — `g1-watch`        chain contains an emSign G1-family cert
                                  (watch-list: emSign Root CA - G1, Chrome
                                  "evaluating" removal; G3 roots removed
                                  2026-10-27)
                 `g3-compromised`  chain matches a revoked eMudhra G3 intermediate
                 `unaffected`      TLS fine, other CA
                 ""                no TLS observed (timeout / no site)

Usage:
  EMUDRA_SCAN=../eMudraImpacts/results/tn-inventory/scan-all.csv \
    python3 tools/cert_status.py
"""
import csv
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_PATH = os.path.join(ROOT, "tamilnadu-sites.csv")
SCAN = os.environ.get(
    "EMUDRA_SCAN",
    os.path.join(os.path.dirname(ROOT), "eMudraImpacts", "results",
                 "tn-inventory", "scan-all.csv"))


def url_host(u):
    h = re.sub(r"^https?://(www\.)?", "", u).split("/")[0].split(":")[0].lower()
    return h


def iso_notafter(s):
    """'Dec 27 05:12:58 2026 GMT' -> '2026-12-27'."""
    try:
        t = time.strptime(s.strip(), "%b %d %H:%M:%S %Y %Z")
        return time.strftime("%Y-%m-%d", t)
    except (ValueError, KeyError):
        return ""


def main():
    scan = {}
    for r in csv.DictReader(open(SCAN, newline="", encoding="utf-8")):
        scan[r["host"].lower()] = r

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())
    for extra in ("cert_expires", "emudhra"):
        if extra not in fields:
            fields.append(extra)

    stats = {"g1-watch": 0, "g3-compromised": 0, "unaffected": 0,
             "no-tls": 0, "no-site": 0, "expired": 0}
    for r in rows:
        r["cert_expires"] = ""
        r["emudhra"] = ""
        u = r["url"] or ""
        if not u.startswith("http"):
            stats["no-site"] += 1
            continue
        s = scan.get(url_host(u))
        if not s or s["tls"].startswith("no-tls") or not s.get("notAfter"):
            stats["no-tls"] += 1
            continue
        r["cert_expires"] = iso_notafter(s["notAfter"])
        if r["cert_expires"] and r["cert_expires"] < time.strftime("%Y-%m-%d"):
            stats["expired"] += 1
        imp = s["impacted"]
        if imp == "CONFIRMED-COMPROMISED-INT":
            r["emudhra"] = "g3-compromised"
            stats["g3-compromised"] += 1
        elif imp == "EMSIGN-FAMILY":
            r["emudhra"] = "g1-watch"
            stats["g1-watch"] += 1
        else:
            r["emudhra"] = "unaffected"
            stats["unaffected"] += 1

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print("merged", len(rows), "rows; stats:", stats)


if __name__ == "__main__":
    main()
