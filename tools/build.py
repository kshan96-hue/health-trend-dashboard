#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Injects manifest + latest daily report into template.html and writes index.html.

Usage: python3 tools/build.py   (from the repository root)
"""
import glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TPL = os.path.join(ROOT, "tools", "template.html")
OUT = os.path.join(ROOT, "index.html")

with open(TPL, encoding="utf-8") as f:
    tpl = f.read()

with open(os.path.join(ROOT, "data", "manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)

reports = {}
latest = None
if manifest.get("daily"):
    latest = sorted(manifest["daily"])[-1]
    if latest:
        with open(os.path.join(ROOT, "data", "daily", latest + ".json"), encoding="utf-8") as f:
            reports[latest] = json.load(f)

payload = {"manifest": manifest, "reports": reports, "embeddedAt": latest}
blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
if "</script" in blob.lower():
    sys.exit("embedded JSON contains </script>")

if "__EMBEDDED__" not in tpl:
    sys.exit("template has no __EMBEDDED__ placeholder")
html = tpl.replace("__EMBEDDED__", blob)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("built", OUT, len(html), "bytes; embedded daily:", latest or "none")
