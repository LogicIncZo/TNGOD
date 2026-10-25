#!/usr/bin/env python3
"""Download the inventory's Android apps from APKPure for static analysis.

Public APKs from a public mirror, desktop-UA, polite delays. Saved to apks/
(gitignored) — nothing here is executed; downstream tools only read bytes.

Usage: python3 tools/fetch_apks.py [--limit N]
"""
import csv
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "apks")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def curl(url, referer=None, out=None, max_time=180):
    cmd = ["curl", "-sL", "--max-time", str(max_time), "-A", UA,
           "-w", "\n@@%{http_code} %{size_download} %{content_type}"]
    if referer:
        cmd += ["-e", referer]
    if out:
        cmd += ["-o", out]
    cmd.append(url)
    p = subprocess.run(cmd, capture_output=True, timeout=max_time + 10)
    raw = p.stdout
    if out:
        # with -o the w-line is the only stdout content ("\n@@code size type")
        wline = raw.decode("utf-8", "replace").strip()
        if wline.startswith("@@"):
            wline = wline[2:]
        return wline, b""
    marker = raw.rfind(b"\n@@")
    if marker == -1:
        return "", raw
    wline = raw[marker + 3:].decode("utf-8", "replace").strip()
    return wline, raw[:marker]


def get_apk(pkg):
    # canonical page (any slug 301s to the real one)
    head, _ = curl(f"https://apkpure.com/app/{pkg}")
    if not head.startswith("200"):
        return f"page-{head.split()[0] or 'fail'}"
    time.sleep(2)
    head, html = curl(f"https://apkpure.com/app/{pkg}/download",
                      referer=f"https://apkpure.com/app/{pkg}")
    if not head.startswith("200"):
        return f"download-{head.split()[0] or 'fail'}"
    m = re.search(r'https://d\.apkpure\.com/b/(APK|XAPK)/' + re.escape(pkg) +
                  r'\?version=[^"\\\s]+', html.decode("utf-8", "replace"))
    if not m:
        return "no-direct-link"
    kind, url = m.group(1), m.group(0).replace("\\/", "/")
    ext = "apk" if kind == "APK" else "xapk"
    dest = os.path.join(OUT, f"{pkg}.{ext}")
    if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
        return "cached"
    head, _ = curl(url, referer="https://apkpure.com/", out=dest, max_time=600)
    code, size = head.split()[:2]
    if code == "200" and int(size) > 100_000:
        return f"ok {int(size)//1024}KB {ext}"
    return f"dl-{code}"


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(ROOT, "android-apps.csv"),
                                    newline="", encoding="utf-8")))
    if "--limit" in sys.argv:
        rows = rows[: rows.index(next(r for r in rows)) + int(sys.argv[sys.argv.index("--limit") + 1])]
    for r in rows:
        pkg = r["pkg"]
        status = get_apk(pkg)
        print(f"{pkg:42s} {status}", flush=True)
        time.sleep(3)


if __name__ == "__main__":
    main()
