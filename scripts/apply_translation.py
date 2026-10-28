# -*- coding: utf-8 -*-
"""Apply the English translation to the Japanese source data.

Generates data/pose-en.json, data/meta-en.json and data/translations.csv.

Usage (from the repo root): python3 scripts/apply_translation.py
"""
import csv
import json
import os
import sys
from collections import Counter

import i18n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

with open(os.path.join(DATA, "pose.json"), encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(DATA, "meta.json"), encoding="utf-8") as f:
    meta = json.load(f)

maps = {
    "系統": i18n.SYSTEM,
    "分類": i18n.CATEGORY,
    "アングル": i18n.ANGLE,
    "ポーズ名": i18n.POSE,
}

missing = {k: sorted({x.get(k) for x in data} - set(m)) for k, m in maps.items()}
bad = {k: v for k, v in missing.items() if v}
if bad:
    print("!! Missing translations:")
    for k, v in bad.items():
        for s in v:
            print(f"  [{k}] {s}")
    sys.exit(1)

# English-keyed records consumed by the front end
out = []
for x in data:
    system = i18n.SYSTEM[x["系統"]]
    category = i18n.CATEGORY[x["分類"]]
    name = i18n.POSE[x["ポーズ名"]]
    angle = i18n.ANGLE[x["アングル"]]
    out.append({
        "id": x["id"],
        "system": system,
        "poseNo": x["ポーズ番号"],
        "category": category,
        "name": name,
        "angle": angle,
        "thumb": x["サムネ"],
        "image": x["原寸"],
        "search": f'{x["id"]} {system} {category} {name} {angle}'.lower(),
    })
with open(os.path.join(DATA, "pose-en.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

with open(os.path.join(DATA, "meta-en.json"), "w", encoding="utf-8") as f:
    json.dump({"systems": [i18n.SYSTEM[s] for s in meta["lines"]]}, f, ensure_ascii=False, indent=2)

# Bilingual reference table (Japanese source -> English) for proofreading
with open(os.path.join(DATA, "translations.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["field", "japanese", "english", "count"])
    for field, label in [("系統", "system"), ("分類", "category"), ("アングル", "angle"), ("ポーズ名", "pose")]:
        cnt = Counter(x[field] for x in data)
        for jp in sorted(maps[field]):
            w.writerow([label, jp, maps[field][jp], cnt[jp]])

print("OK records:", len(out))
print("Unique terms:", sum(len(m) for m in maps.values()))
