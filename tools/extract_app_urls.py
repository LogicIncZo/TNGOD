#!/usr/bin/env python3
"""Static URL extraction from the apks/ directory (no execution).

Reads every .apk/.xapk (recursing into .xapk bundles), extracts http(s) URLs
from dex bytecodes, binary XML, resources.arsc (UTF-16LE), assets and native
libs, then classifies each host as first-party / sdk / other.

Outputs:
  tools/app-urls.jsonl   {"pkg", "host", "count", "sample"} per (pkg, host)
  tools/app-backends.jsonl same rows + "cls" classification

This reads public APK bytes only — no emulator, no dynamic analysis.
"""
import json
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APKS = os.path.join(ROOT, "apks")

URL_RE = re.compile(rb"https?://[\x21-\x7e]{4,300}")
HOST_OK = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")

# SDK / vendor noise: analytics, payments, maps, crash reporting, ads, push.
SDK_RE = re.compile(
    r"(^|\.)(google|googleapis|gstatic|googleusercontent|google-analytics|"
    r"app-measurement|googlesyndication|googleadservices|googlesource|"
    r"crashlytics|firebaseio|firebaseapp|firebase|fcm|recaptcha|goo\.gl|goo\.gle|"
    r"android\.com|play\.google|issuetracker|crbug|"
    r"appsflyer|clevertap|moengage|mixpanel|segment\.com|branch\.io|"
    r"amplitude|onesignal|airship|pushwoosh|sentry|bugsnag|instabug|"
    r"userexperior|uxcam|smartlook|hotjar|webengage|netcore|"
    r"facebook|fb\.com|instagram|twitter|x\.com|whatsapp|telegram|wikipedia|"
    r"razorpay|paytm|phonepe|cashfree|payu|zaakpay|juspay|billdesk|ccavenue|"
    r"atomtech|ebixcash|freecharge|mobikwik|"
    r"mapmyindia|mappls|here\.com|mapbox|openstreetmap|tomtom|esri|arcgis|"
    r"cloudflare|akamai|amazonaws|azureedge|heroku|vercel|netlify|cloudfront|"
    r"doubleclick|admob|applovin|unity3d|"
    r"w3\.org|apache\.org|json\.org|schema\.org|xmlpull\.org|slf4j\.org|"
    r"purl\.org|adobe\.com|xmlsoap|unicode\.org|mozilla|"
    r"jetbrains|github|gitlab|bitbucket|jsdelivr|npmjs|maven|gradle|"
    r"bit\.ly|tinyurl|t\.co|is\.gd|"
    r"youtube|vimeo|dailymotion|"
    r"typography\.com|typekit|fonts\.|"
    r"example\.com|localhost|inventcare|"
    r"apple\.com|microsoft|outlook|skype|zoom\.us|"
    r"ietf\.org|csswg|fxtf\.org|reactnavigation|react\.dev|swmansion|dottoro|"
    r"momentjs|dashif|chromium\.org|webrtc|whatwg|khronos|sqlite\.org|"
    r"openssl\.org|gnu\.org|json-schema|swagger|ecma|tc39|openjsf|"
    r"twilio|msg91|exotel|knowlarity|gupshup|"
    r"credgenics|perfios|karza|signzy|digio|idfy|hyperverge|"
    r"zomato|uber|ola|rapido|redbus|irctc|swiggy|"
    r"freshdesk|freshchat|zendesk|intercom|kapture|"
    r"salesforce|hubspot|zoho|momentjs|dottoro|swmansion|"
    r"reactnavigation|react\.dev|csswg|fxtf|dashif|chromium|ietf|"
    r"whatwg|khronos|sqlite|openssl|gnu\.org|ecma|tc39|openjsf)", re.I)

FIRST_PARTY_EXTRA = re.compile(
    r"(^|\.)(tn\.gov\.in|gov\.in|nic\.in|tnega\.org|tnpolice\.gov\.in|cmrl|"
    r"tneb|tangedco|tnpdcl|tnmsc|tnrtp|tnrise|cscl\.co\.in|tnscbank|tnreginet|"
    r"tamilnilam|tnhmis|tnmrbd|tnurbaneseva|cmhelpline|kaaval|kavalan|"
    r"chennaicorporation|ccmc|gcc|coimbatore|madurai|trichy|tiruppur|salem|"
    r"tnepass|tnsta|tnagrisnet|tnagri|tneoffice|tnhealth|tnmrhs|"
    r"tamilnadu|makkalsevai|nilam|erss\.in|dial100|kavaluthavi|112\.gov\.in|"
    r"spmcrdial100\.in|dial112\.in|"
    r"tngis|tnswp|tnscb|tantea|tnfdc|tnpl|aavin|tasmac|elcot|tnhighways|"
    r"tnkisan|tnphr|nhm\.gov|nhm\.gov|mdm\.tn|tnservices|esevai|tnvelugu|"
    r"tnpubliclibraries|tnpfc|tnsurvey|tnemandi|tnnambikkai|"
    r"chennaimetrorail\.org|moving\.tech|tnstc|tn-nhis|thiranmigutiruppur|tnstc\.in)(\.|$)", re.I)

VALID_TLD = {
    "com", "in", "org", "net", "io", "co", "app", "dev", "ai", "gov", "nic",
    "edu", "res", "ac", "us", "uk", "me", "info", "xyz", "online", "site",
    "tech", "digital", "care", "health", "bank", "finance", "capital",
    "energy", "power", "solutions", "systems", "world", "cloud", "live",
    "news", "media", "tv", "store", "shop", "link", "one", "life", "plus",
    "in.net", "co.in", "gov.in", "nic.in", "ac.in", "res.in", "edu.in",
    "org.in", "net.in",
}


def _clean(s):
    # cut at the first char that can't appear in a URL embedded in binaries
    return re.split(r"[\s\"'<>\)\]\\}],;]+", s)[0]


def iter_urls(data: bytes):
    """Yield URL-candidate strings via UTF-8 and UTF-16LE decoding."""
    for m in URL_RE.finditer(data):
        yield _clean(m.group(0).decode("ascii", "replace"))
    try:
        u16 = data.decode("utf-16-le", errors="replace")
    except Exception:
        return
    for m in re.finditer(r"https?://[\x21-\x7e]{4,300}", u16):
        yield _clean(m.group(0))


def host_of(url):
    m = re.match(r"https?://([^/:?#]+)", url, re.I)
    if not m:
        return None
    h = m.group(1).lower().strip(".")
    if h.startswith("www."):
        h = h[4:]
    if len(h) < 4 or len(h) > 100 or not HOST_OK.match(h):
        return None
    labels = h.split(".")
    if len(labels) < 2 or ".".join(labels[-2:]) not in VALID_TLD and labels[-1] not in VALID_TLD:
        return None
    return h


def iter_zip_payloads(zf, depth=0):
    """Yield (name, bytes) for every file, recursing one level into bundles."""
    for info in zf.infolist():
        if info.is_dir():
            continue
        name = info.filename
        try:
            data = zf.read(name)
        except Exception:
            continue
        if name.lower().endswith((".apk", ".xapk", ".apkm")) and depth < 1:
            try:
                yield from iter_zip_payloads(zipfile.ZipFile(
                    __import__("io").BytesIO(data)), depth + 1)
            except Exception:
                pass
            continue
        yield name, data


def extract_pkg(path):
    per_host = {}
    with zipfile.ZipFile(path) as zf:
        for name, data in iter_zip_payloads(zf):
            low = name.lower()
            interesting = (low.endswith((".dex", ".arsc", ".so", ".json",
                                         ".xml", ".html", ".txt", ".properties"))
                           or "assets/" in low or "res/" in low
                           or low.startswith(("classes", "root/")))
            if not interesting:
                continue
            for url in iter_urls(data):
                h = host_of(url)
                if not h:
                    continue
                rec = per_host.setdefault(h, {"count": 0, "sample": url[:160]})
                rec["count"] += 1
    return per_host


def classify(host):
    if SDK_RE.search(host):
        return "sdk"
    if FIRST_PARTY_EXTRA.search(host) or host.endswith(
            (".gov.in", ".nic.in", ".tnega.org", ".tn.gov.in")):
        return "first-party"
    return "other"


def main():
    out1 = open(os.path.join(HERE, "app-urls.jsonl"), "w", encoding="utf-8")
    out2 = open(os.path.join(HERE, "app-backends.jsonl"), "w", encoding="utf-8")
    files = sorted(f for f in os.listdir(APKS)
                   if f.endswith((".apk", ".xapk", ".apkm")))
    for fname in files:
        pkg = fname.rsplit(".", 1)[0]
        try:
            hosts = extract_pkg(os.path.join(APKS, fname))
        except Exception as e:
            print(f"{pkg:44s} ERROR {type(e).__name__}: {e}")
            continue
        fp = sd = ot = 0
        for h, rec in sorted(hosts.items(), key=lambda kv: -kv[1]["count"]):
            cls = classify(h)
            if cls == "first-party":
                fp += 1
            elif cls == "sdk":
                sd += 1
            else:
                ot += 1
            row = {"pkg": pkg, "host": h, "count": rec["count"],
                   "sample": rec["sample"], "cls": cls}
            out2.write(json.dumps(row, ensure_ascii=False) + "\n")
            out1.write(json.dumps({k: row[k] for k in
                                   ("pkg", "host", "count", "sample")},
                                  ensure_ascii=False) + "\n")
        print(f"{pkg:44s} hosts={len(hosts):4d} first-party={fp:3d} sdk={sd:3d} other={ot:3d}",
              flush=True)
    out1.close()
    out2.close()


if __name__ == "__main__":
    main()
