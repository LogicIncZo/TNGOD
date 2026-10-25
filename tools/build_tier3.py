#!/usr/bin/env python3
"""Build the Tier-3 (app backend) layer from tools/app-backends.jsonl.

- aggregates first-party hosts across apps
- names them (curated map + inventory reverse lookup)
- writes: tier-3 rows into tamilnadu-sites.csv, `backends` column into
  android-apps.csv, and a host list for tools/verify_hosts.py

Liveness: run tools/verify_hosts.py <hosts.txt> out.jsonl first and pass the
result via BACKEND_VERIFY env var; rows without verification data are marked
unverified.
"""
import csv
import json
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

APP_NAME = {r["pkg"]: r["name"] for r in
            csv.DictReader(open(os.path.join(ROOT, "android-apps.csv"),
                                newline="", encoding="utf-8"))}
INV = {re.sub(r"^https?://(www\.)?", "", (r["url"] or "")).split("/")[0].lower():
       r["name"] for r in
       csv.DictReader(open(os.path.join(ROOT, "tamilnadu-sites.csv"),
                           newline="", encoding="utf-8")) if r["url"]}

# Central (GoI) portals and non-TN environments referenced by the apps:
# documented but not promoted to Tier-3 rows.
EXCLUDE = {
    "cybercrime.gov.in", "echallan.parivahan.gov.in",          # GoI portals
    "healthidsbx.abdm.gov.in", "abhasbx.abdm.gov.in", "dev.abdm.gov.in",  # ABDM
    "hhsuat.tnega.org",                                        # UAT, NXDOMAIN
    "sandbox.assets.moving.tech", "plasma.moving.tech",        # vendor infra
    "appmonitor.moving.tech", "assets.moving.tech", "config.moving.tech",
}

# curated names/notes for backend hosts discovered in the APKs
NAMED = {
    "tn.erss.in": ("ERSS 112 — TN Emergency Response Support System",
                   "national emergency-number backend used by Kaaval Uthavi"),
    "appkvl.spmcrdial100.in": ("ERSS 112 backend (SPMCR)",
                               "112-India platform endpoint; unreachable at check"),
    "api.moving.tech": ("Chennai One API (Moving Tech — CUMTA vendor)",
                        "primary ticketing backend of the official CUMTA app; vendor-operated; assets/config/appmonitor.moving.tech also live"),
    "commuters-data.chennaimetrorail.org": ("CMRL commuter-data API",
                                            "official CMRL app backend"),
    "chennaimetrorail.org": ("Chennai Metro Rail Limited website",
                             "official CMRL site + app content host"),
    "chennaicorporation.gov.in": ("Greater Chennai Corporation (app portal)",
                                  "GCC app portal (Tomcat)"),
    "erp.chennaicorporation.gov.in": ("GCC ERP backend",
                                      "Greater Chennai Corporation ERP (property tax etc.)"),
    "gisgcc.chennaicorporation.gov.in": ("GCC GIS backend",
                                         "Greater Chennai Corporation GIS (Tomcat)"),
    "gccservices.chennaicorporation.gov.in": ("GCC services backend",
                                              "GCC civic services API"),
    "gccapp.chennaicorporation.gov.in": ("GCC app API",
                                         "GCC mobile-app API host"),
    "portal.chennaicorporation.gov.in": ("GCC portal services", ""),
    "ccmc.appifeedback.in": ("CCMC citizen-feedback backend (AppiFeedback)",
                             "vendor-operated feedback tool used by Coimbatore corporation"),
    "thiranmigutiruppur.com": ("Tiruppur Smart City backend (TSC)",
                               "vendor-operated portal of Tiruppur Smart City"),
    "tnurbanepay.tn.gov.in": ("TN Urban Pay (urban utility payments)",
                              "payment gateway used by CMA/urban-body apps"),
    "urbantamilnilam.tn.gov.in": ("Urban TamilNilam",
                                  "urban land-records e-services"),
    "tamilnilam.tn.gov.in": ("TamilNilam citizen portal", "land-records e-services"),
    "collabland-tn.gov.in": ("Collabland TN (CollabWeb)", "land-records collaboration platform"),
    "mobileapi.phr.tn.gov.in": ("TNPHR mobile API",
                                "TN Personal Health Record API; unreachable at check (NIC)"),
    "tn-nhis.com": ("TN-NHIS (CM Comprehensive Health Insurance Scheme backend)",
                    "scheme backend of the CMCHIS app; vendor-operated domain"),
    "tnstc.in": ("TNSTC app backend", "bus-ticketing API of the TNSTC app"),
    "ccms.tangedco.org": ("TANGEDCO app backend (CCMS)",
                          "consumer-care/billing API of the TANGEDCO app"),
    "app1.tangedco.org": ("TANGEDCO app backend (app1)", "secondary app API host"),
    "eservices.tnpolice.gov.in": ("TN Police e-Services",
                                  "police citizen-services backend (Kaaval Uthavi)"),
    "tnpscems.tn.gov.in": ("TNPSC EMS portal",
                           "exam-management portal behind the TNPSC app"),
    "tnagrisnet.tn.gov.in": ("Uzhavan web services (Agriculture Dept)",
                             "farmer-services backend of the UZHAVAR app"),
    "ekyc.tnega.org": ("TNeGA generic eKYC", "shared eKYC gateway (Makkal Sevai)"),
    "cmhelpline.tnega.org": ("TN CM Helpline 1100", "grievance platform backend"),
    "kmut.tnega.org": ("Kalaignar Magalir Urimai Thittam portal", "scheme portal"),
    "mut.secureapp.tnega.org": ("KMUT verification API", "entitlement-verification API host"),
    "cropsurveyapi.tnega.org": ("Crop Survey API", "field crop-survey data collection API"),
    "tngis.tnega.org": ("TNeGA GIS service", "no DNS at check time (referenced by app)"),
    "cumta.tn.gov.in": ("CUMTA — Chennai Unified Metropolitan Transport Authority",
                        "transport authority portal"),
    "tnesevai.tn.gov.in": ("TNeGA eSevai gateway", "eSevai services host"),
    "skilldevelopment.tn.gov.in": ("Naan Mudhalvan skill portal", "backend of the skill app"),
    "tnreginet.gov.in": ("TNREGINET (Registration Dept)", "registration e-services"),
    "tnlandsurvey.tn.gov.in": ("Commissionerate of Survey & Settlement", ""),
    "tnurbantree.tn.gov.in": ("TN Urban Tree Authority portal", ""),
    "tnhealth.tn.gov.in": ("Health & Family Welfare Dept", ""),
}


def load_backends():
    per_host = defaultdict(lambda: {"apps": set(), "count": 0, "sample": ""})
    for line in open(os.path.join(HERE, "app-backends.jsonl"), encoding="utf-8"):
        j = json.loads(line)
        if j["cls"] != "first-party":
            continue
        rec = per_host[j["host"]]
        rec["apps"].add(j["pkg"])
        rec["count"] += j["count"]
        if not rec["sample"]:
            rec["sample"] = j["sample"]
    return per_host


def host_display(host):
    if host in NAMED:
        return NAMED[host]
    if host in INV:
        return (INV[host] + " (app backend)", "")
    # gov.in / nic.in / tnega hosts: derive a readable name from labels
    base = re.sub(r"\.(gov\.in|nic\.in|tn\.gov\.in|tnega\.org|nic\.in)$", "", host)
    label = base.split(".")[0].replace("-", " ")
    return (f"{label} (TN gov app backend)", "")


def main():
    per_host = load_backends()
    hosts = sorted(per_host, key=lambda h: (-len(per_host[h]["apps"]), h))

    verify = {}
    vf = os.environ.get("BACKEND_VERIFY")
    if vf and os.path.exists(vf):
        for line in open(vf, encoding="utf-8"):
            j = json.loads(line)
            verify[j["host"]] = j

    # ---- android-apps.csv: add backends column ----
    app_rows = list(csv.DictReader(open(os.path.join(ROOT, "android-apps.csv"),
                                        newline="", encoding="utf-8")))
    fields = list(app_rows[0].keys())
    if "backends" not in fields:
        fields.append("backends")
    for r in app_rows:
        top = sorted((h for h, rec in per_host.items() if r["pkg"] in rec["apps"]),
                     key=lambda h: -per_host[h]["count"])[:3]
        r["backends"] = "; ".join(top)
    with open(os.path.join(ROOT, "android-apps.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(app_rows)

    # ---- tamilnadu-sites.csv: tier-3 rows ----
    site_rows = list(csv.DictReader(open(os.path.join(ROOT, "tamilnadu-sites.csv"),
                                         newline="", encoding="utf-8")))
    fields = list(site_rows[0].keys())
    existing = {re.sub(r"^https?://(www\.)?", "", (r["url"] or "")).split("/")[0].lower()
                for r in site_rows if r["url"]}
    added = 0
    for h in hosts:
        if h in existing or h in EXCLUDE:
            continue
        existing.add(h)
        rec = per_host[h]
        name, note = host_display(h)
        apps = ", ".join(sorted(APP_NAME.get(a, a) for a in rec["apps"]))
        v = verify.get(h, {})
        code = v.get("code", 0) if v else 0
        if v:
            if code == 200:
                status, detail = "live", f"HTTP 200; backend for: {apps}"
            elif code:
                status, detail = "error", f"HTTP {code}; backend for: {apps}"
            elif v.get("dns") == "nxdomain":
                status, detail = "dead", f"no DNS; backend for: {apps}"
            else:
                status, detail = "unreachable", f"DNS live; no HTTP response; backend for: {apps}"
        else:
            status, detail = "unreachable", f"unverified; backend for: {apps}"
        if note:
            detail += f" — {note}"
        site_rows.append({"name": name, "url": f"https://{h}",
                          "group": "App API Backends (Tier 3)", "igod_type": "OTHR",
                          "status": status, "detail": detail, "tier": "3",
                          "cert_expires": "", "emudhra": ""})
        added += 1
    with open(os.path.join(ROOT, "tamilnadu-sites.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(site_rows)

    # ---- host list for verification ----
    with open(os.path.join(HERE, "tier3-hosts.txt"), "w") as f:
        f.write("\n".join(hosts) + "\n")

    print(f"first-party hosts: {len(hosts)}; new tier-3 rows: {added}")
    for h in hosts:
        rec = per_host[h]
        print(f"  {h:46s} apps={len(rec['apps']):2d} refs={rec['count']:4d} {rec['sample'][:60]}")


if __name__ == "__main__":
    main()
