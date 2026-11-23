#!/usr/bin/env python3
"""Check the Asset Studio catalogue and show drawing progress.

Standard library only. Run from anywhere:

    python tools/check_catalog.py                 # check + progress per category
    python tools/check_catalog.py --find lion     # is "lion" already listed?
    python tools/check_catalog.py --todo animals  # items in animals with no SVG yet

The catalogue is catalog/<category>.json (playlists.json is skipped here).
Drawings are svg/<category>/<id>.svg; folders starting with "_" (like
_style-test) are ignored. Exit code 1 when there are errors, so it can gate a commit or CI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

KINDS = {"illustration", "icon", "scene", "tile", "emoji", "character"}
RECOLORS = {"keep", "themed", "mono"}
MOTIONS = {
    "pop", "rise", "slide", "drop", "draw", "morph", "fade", "float", "pulse", "wiggle", "spin",
    "flap", "swim", "walk", "run", "hop", "sway", "blink", "wave", "glow", "twinkle", "flicker",
    "orbit", "bounce", "rotate", "pour", "drip", "grow", "beat", "breathe", "launch", "fly", "roll",
    "tick", "ring", "shake", "splash", "open",
}
CATEGORY_KEYS = {"id", "name", "description", "groups"}
GROUP_KEYS = {"id", "name", "kind", "recolor", "motion", "items", "see"}
ITEM_KEYS = {"id", "name", "aka", "note"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKIP_FILES = {"playlists.json"}


def slug(text: str) -> str:
    """Name to id: "polar bear" -> polar-bear, "Earth's moon" -> earths-moon, "déjà vu" -> deja-vu.

    Must match slug() in viewer.html.
    """
    s = unicodedata.normalize("NFKD", text)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace("&", " and ").replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm_name(text: str) -> str:
    """Key for comparing names and other names (case, accents and punctuation ignored)."""
    return slug(text).replace("-", " ")


@dataclass
class Item:
    id: str
    name: str
    aka: list[str]
    category: str
    group: str
    note: str = ""

    @property
    def names(self) -> list[str]:
        return [self.name, *self.aka]


@dataclass
class Group:
    id: str
    category: str
    see: list[str] = field(default_factory=list)
    item_ids: list[str] = field(default_factory=list)


@dataclass
class Catalogue:
    items: dict[str, Item] = field(default_factory=dict)
    groups: dict[str, Group] = field(default_factory=dict)
    categories: dict[str, list[str]] = field(default_factory=dict)  # category -> item ids, in order
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_item(raw, where: str, cat: Catalogue) -> tuple[str, str, list[str], str] | None:
    """Return (id, name, aka, note) or None after recording an error."""
    if isinstance(raw, str):
        if not raw.strip():
            cat.errors.append(f"{where}: empty item name")
            return None
        return slug(raw), raw, [], ""
    if isinstance(raw, list):
        if not raw or not all(isinstance(x, str) and x.strip() for x in raw):
            cat.errors.append(f"{where}: an item list must be non-empty strings: {raw!r}")
            return None
        return slug(raw[0]), raw[0], list(raw[1:]), ""
    if isinstance(raw, dict):
        extra = set(raw) - ITEM_KEYS
        if extra:
            cat.errors.append(f"{where}: unknown item keys {sorted(extra)}")
        name = raw.get("name")
        if not isinstance(name, str) or not name.strip():
            cat.errors.append(f"{where}: item object needs a \"name\": {raw!r}")
            return None
        aka = raw.get("aka", [])
        if not isinstance(aka, list) or not all(isinstance(x, str) and x.strip() for x in aka):
            cat.errors.append(f"{where}: \"aka\" must be a list of strings for {name!r}")
            aka = []
        note = raw.get("note", "")
        if not isinstance(note, str):
            cat.errors.append(f"{where}: \"note\" must be a string for {name!r}")
            note = ""
        item_id = raw.get("id", slug(name))
        if not isinstance(item_id, str):
            cat.errors.append(f"{where}: \"id\" must be a string for {name!r}")
            return None
        return item_id, name, aka, note
    cat.errors.append(f"{where}: an item must be a string, a list or an object, got {raw!r}")
    return None


def check_group(g, fname: str, cat_id: str, cat: Catalogue) -> None:
    if not isinstance(g, dict):
        cat.errors.append(f"{fname}: a group must be an object, got {g!r}")
        return
    gid = g.get("id")
    where = f"{fname} group {gid!r}"
    if not isinstance(gid, str) or not ID_RE.match(gid):
        cat.errors.append(f"{where}: group id must be lower-case words joined by '-'")
        return
    for key in ("id", "name", "kind", "recolor", "motion", "items"):
        if key not in g:
            cat.errors.append(f"{where}: missing \"{key}\"")
    extra = set(g) - GROUP_KEYS
    if extra:
        cat.errors.append(f"{where}: unknown group keys {sorted(extra)}")
    if "kind" in g and g["kind"] not in KINDS:
        cat.errors.append(f"{where}: unknown kind {g['kind']!r} (use one of {sorted(KINDS)})")
    if "recolor" in g and g["recolor"] not in RECOLORS:
        cat.errors.append(f"{where}: unknown recolor {g['recolor']!r} (use one of {sorted(RECOLORS)})")
    motion = g.get("motion", [])
    if not isinstance(motion, list) or not 1 <= len(motion) <= 3:
        cat.errors.append(f"{where}: motion must be a list of 1 to 3 motions")
    else:
        bad = [m for m in motion if m not in MOTIONS]
        if bad:
            cat.errors.append(f"{where}: unknown motion {bad}")

    group = Group(gid, cat_id)
    if gid in cat.groups:
        other = cat.groups[gid].category
        cat.errors.append(f"{where}: group id already used in {other}.json")
        # Keep checking its items under a private key so one mistake doesn't hide others.
        cat.groups[f"{cat_id}/{gid}#{len(cat.groups)}"] = group
    else:
        cat.groups[gid] = group

    items = g.get("items", [])
    if not isinstance(items, list):
        cat.errors.append(f"{where}: \"items\" must be a list")
        items = []
    for raw in items:
        parsed = parse_item(raw, where, cat)
        if parsed is None:
            continue
        item_id, name, aka, note = parsed
        if not ID_RE.match(item_id):
            cat.errors.append(f"{where}: bad id {item_id!r} for {name!r} (lower-case words joined by '-')")
            continue
        if item_id in cat.items:
            prev = cat.items[item_id]
            cat.errors.append(
                f"{where}: repeated id {item_id!r} (already in {prev.category}.json group {prev.group!r}); "
                f"qualify one of them, e.g. {item_id}-<what>"
            )
            continue
        cat.items[item_id] = Item(item_id, name, aka, cat_id, gid, note)
        group.item_ids.append(item_id)
        cat.categories[cat_id].append(item_id)

    see = g.get("see", [])
    if not isinstance(see, list) or not all(isinstance(s, str) for s in see):
        cat.errors.append(f"{where}: \"see\" must be a list of ids")
    else:
        group.see = see
    if not group.item_ids and not group.see:
        cat.warnings.append(f"{where}: group has no items and no see")


def load(root: Path) -> Catalogue:
    cat = Catalogue()
    folder = root / "catalog"
    files = sorted(p for p in folder.glob("*.json") if p.name not in SKIP_FILES) if folder.is_dir() else []
    for path in files:
        fname = path.name
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
            cat.errors.append(f"{fname}: cannot read: {e}")
            continue
        if not isinstance(data, dict):
            cat.errors.append(f"{fname}: top level must be an object")
            continue
        for key in ("id", "name", "description", "groups"):
            if key not in data:
                cat.errors.append(f"{fname}: missing \"{key}\"")
        extra = set(data) - CATEGORY_KEYS
        if extra:
            cat.errors.append(f"{fname}: unknown keys {sorted(extra)}")
        cat_id = data.get("id", path.stem)
        if cat_id != path.stem:
            cat.errors.append(f"{fname}: id {cat_id!r} must equal the file name {path.stem!r}")
            cat_id = path.stem
        cat.categories.setdefault(cat_id, [])
        groups = data.get("groups", [])
        if not isinstance(groups, list):
            cat.errors.append(f"{fname}: \"groups\" must be a list")
            continue
        for g in groups:
            check_group(g, fname, cat_id, cat)

    # see links: must exist, and should not repeat the group's own items.
    for g in cat.groups.values():
        for target in g.see:
            if target not in cat.items:
                cat.errors.append(f"{g.category}.json group {g.id!r}: see {target!r} is not an item id")
            elif target in g.item_ids:
                cat.warnings.append(f"{g.category}.json group {g.id!r}: see {target!r} is already in this group")

    # The same name or other name on two different items.
    by_name: dict[str, list[str]] = {}
    for item in cat.items.values():
        for key in {norm_name(n) for n in item.names}:
            by_name.setdefault(key, []).append(item.id)
    for key, ids in sorted(by_name.items()):
        if len(ids) > 1:
            where = ", ".join(f"{i} ({cat.items[i].category})" for i in ids)
            cat.warnings.append(f"name {key!r} is used by {len(ids)} items: {where}")
    return cat


def drawn_ids(root: Path) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    svg = root / "svg"
    if not svg.is_dir():
        return out
    for d in svg.iterdir():
        if d.is_dir() and not d.name.startswith("_"):
            out[d.name] = {p.stem for p in d.glob("*.svg")}
    return out


def cmd_check(root: Path, cat: Catalogue, show_warnings: bool) -> int:
    drawn = drawn_ids(root)
    for c, ids in sorted(drawn.items()):
        if c not in cat.categories:
            cat.warnings.append(f"svg/{c}/ has drawings but there is no catalog/{c}.json")
            continue
        listed = set(cat.categories[c])
        for i in sorted(ids - listed):
            owner = cat.items.get(i)
            hint = f" (it belongs to {owner.category})" if owner else ""
            cat.warnings.append(f"svg/{c}/{i}.svg is not in catalog/{c}.json{hint}")

    for e in cat.errors:
        print(f"ERROR   {e}")
    if show_warnings:
        for w in cat.warnings:
            print(f"warning {w}")
    if cat.errors or (show_warnings and cat.warnings):
        print()

    if not cat.categories:
        print(f"No catalogue files yet in {root / 'catalog'}")
    else:
        width = max(len(c) for c in cat.categories)
        total_items = total_drawn = 0
        print(f"{'category':<{width}}  {'groups':>6}  {'items':>6}  {'drawn':>6}  {'done':>5}")
        for c in sorted(cat.categories):
            ids = cat.categories[c]
            done = len(set(ids) & drawn.get(c, set()))
            groups = sum(1 for g in cat.groups.values() if g.category == c)
            pct = f"{100 * done / len(ids):.0f}%" if ids else "-"
            print(f"{c:<{width}}  {groups:>6}  {len(ids):>6}  {done:>6}  {pct:>5}")
            total_items += len(ids)
            total_drawn += done
        pct = f"{100 * total_drawn / total_items:.0f}%" if total_items else "-"
        print(f"{'total':<{width}}  {len(cat.groups):>6}  {total_items:>6}  {total_drawn:>6}  {pct:>5}")

    summary = f"{len(cat.errors)} error(s), {len(cat.warnings)} warning(s)"
    if cat.warnings and not show_warnings:
        summary += " (--warnings to list them)"
    print(f"\n{summary}")
    return 1 if cat.errors else 0


def cmd_find(cat: Catalogue, word: str) -> int:
    q = norm_name(word)
    if not q:
        print("Give a word to look for.")
        return 2
    exact, partial = [], []
    for item in cat.items.values():
        keys = [norm_name(n) for n in item.names] + [item.id.replace("-", " ")]
        if q in keys:
            exact.append(item)
        elif any(q in k for k in keys):
            partial.append(item)
    see_in = {}
    for g in cat.groups.values():
        for t in g.see:
            see_in.setdefault(t, []).append(f"{g.category}/{g.id}")

    def show(item: Item) -> None:
        aka = f"  aka: {', '.join(item.aka)}" if item.aka else ""
        also = f"  (also seen in {', '.join(see_in[item.id])})" if item.id in see_in else ""
        print(f"  {item.category}/{item.group}/{item.id}  \"{item.name}\"{aka}{also}")

    if exact:
        print(f"Already listed as \"{word}\":")
        for i in exact:
            show(i)
    if partial:
        print(f"{'Similar' if exact else 'Not listed exactly; similar'}:")
        for i in sorted(partial, key=lambda i: (len(i.id), i.id))[:30]:
            show(i)
        if len(partial) > 30:
            print(f"  ... and {len(partial) - 30} more")
    if not exact and not partial:
        print(f"\"{word}\" is not in the catalogue. Suggested id: {slug(word)}")
    return 0


def cmd_todo(root: Path, cat: Catalogue, category: str) -> int:
    if category not in cat.categories:
        print(f"No catalog/{category}.json. Categories: {', '.join(sorted(cat.categories)) or 'none yet'}")
        return 2
    have = drawn_ids(root).get(category, set())
    todo_total = 0
    for g in cat.groups.values():
        if g.category != category:
            continue
        todo = [i for i in g.item_ids if i not in have]
        if not todo:
            continue
        todo_total += len(todo)
        print(f"{g.id} ({len(todo)}/{len(g.item_ids)} to draw)")
        for i in todo:
            print(f"  {i}")
    ids = cat.categories[category]
    print(f"\n{category}: {len(ids) - todo_total} of {len(ids)} drawn, {todo_total} to go")
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Check the Asset Studio catalogue and show drawing progress.")
    ap.add_argument("--find", metavar="WORD", help="is this word already in the catalogue?")
    ap.add_argument("--todo", metavar="CATEGORY", help="list items in CATEGORY with no SVG yet")
    ap.add_argument("--warnings", action="store_true", help="list warnings, not only their count")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                    help="asset-studio folder (default: the one this script is in)")
    args = ap.parse_args(argv)

    cat = load(args.root)
    if args.find is not None:
        return cmd_find(cat, args.find)
    if args.todo is not None:
        return cmd_todo(args.root, cat, args.todo)
    return cmd_check(args.root, cat, args.warnings)


if __name__ == "__main__":
    sys.exit(main())
