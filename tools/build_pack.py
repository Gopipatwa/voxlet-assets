"""Builds the voxlet-own pack zip that the Voxlet app downloads.

    python tools/build_pack.py [--version 2026.11.23]

Writes dist/voxlet-own.zip (and a copy named with the version). Inside:
    index.json   {"pack", "version", "license", "assets": [...]}
    LICENSE
    svg/<category>/<id>.svg   every drawn item of the catalogue
Upload dist/voxlet-own.zip to a GitHub Release of this repo; the app downloads
https://github.com/<owner>/voxlet-assets/releases/latest/download/voxlet-own.zip
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from check_catalog import slug  # noqa: E402

PACK = "voxlet-own"
LICENSE_ID = "LicenseRef-Voxlet-own"


def words(text: str) -> list[str]:
    return [w for w in re.split(r"[^a-z0-9]+", text.lower()) if w]


def item_parts(it):
    if isinstance(it, dict):
        return it.get("id") or slug(it["name"]), it["name"], list(it.get("aka", []))
    if isinstance(it, list):
        return slug(it[0]), it[0], list(it[1:])
    return slug(it), it, []


def build(version: str) -> tuple[Path, int, int]:
    assets, missing = [], 0
    for cat_file in sorted((ROOT / "catalog").glob("*.json")):
        if cat_file.stem == "playlists":
            continue
        cat = json.loads(cat_file.read_text(encoding="utf-8"))
        category = cat_file.stem
        for g in cat["groups"]:
            for it in g["items"]:
                iid, name, aka = item_parts(it)
                svg = ROOT / "svg" / category / f"{iid}.svg"
                if not svg.exists():
                    missing += 1
                    continue
                tags = []
                for t in [name, *aka, g["name"], category.replace("-", " ")]:
                    tags += words(t)
                tags = list(dict.fromkeys(tags))
                assets.append({
                    "id": iid, "name": name, "category": category, "group": g["id"],
                    "kind": "icon" if g.get("kind") == "icon" else "illustration",
                    "recolor": g.get("recolor", "themed"), "motion": g.get("motion", []),
                    "tags": tags, "file": f"svg/{category}/{iid}.svg",
                })
    index = {"pack": PACK, "version": version, "license": LICENSE_ID, "assets": assets}
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"{PACK}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("index.json", json.dumps(index, ensure_ascii=False, separators=(",", ":")))
        z.write(ROOT / "LICENSE", "LICENSE")
        for a in assets:
            z.write(ROOT / a["file"], a["file"])
    (dist / f"{PACK}-{version}.zip").write_bytes(out.read_bytes())
    return out, len(assets), missing


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", default=dt.date.today().isoformat().replace("-", "."))
    a = ap.parse_args()
    path, n, missing = build(a.version)
    print(f"{path.name}: {n} drawings ({missing} catalogue items not drawn yet), {path.stat().st_size / 1e6:.1f} MB")
