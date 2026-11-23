"""Shared helpers for hand-drawn Asset Studio SVGs (style B, with a flat style A derived from it).

Every drawing is written once, in style B. Outline pieces are marked so style A ("no border")
is the same file with them stripped:
  - filled shapes carry their outline as stroke attributes plus data-outline="stroke"
  - tubes get an ink under-stroke element with data-outline="under"
flat(svg_text) removes both, giving style A. Mono line icons have no outline marks.

Drawing scripts live in drawings/<category>.py and use:
    s = Svg()                      new 512x512 drawing
    s.F(tag, **attrs)              filled shape with outline (fill="..." etc.)
    s.T(d, color, width)           tube: coloured stroke with an outlined edge
    s.M(d, color, width=24, ...)   mono line, no outline
    s.open(id, pivot, transform)   start a group (animation parts: id="part-<name>")
    s.close()
    save(category, item_id, s)     writes svg/<category>/<id>.svg
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PALETTE = json.loads((ROOT / "style" / "palette.json").read_text(encoding="utf-8"))
C = dict(PALETTE["keep"])
THEME = PALETTE["themed"]
INK = PALETTE["outline"]["color"]
OW = PALETTE["outline"]["width"]
MONO_W = PALETTE["mono"]["width"]


def _attrs(a: dict) -> str:
    return " ".join(f'{k.rstrip("_").replace("_", "-")}="{v}"' for k, v in a.items() if v is not None)


class Svg:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.depth = 0

    def _add(self, s: str) -> None:
        self.parts.append("  " * self.depth + s)

    def F(self, tag: str, outline: bool = True, **a) -> None:
        """Filled shape. outline=False for highlights and small inner details."""
        if outline:
            a = {**a, "stroke": INK, "stroke_width": OW, "stroke_linejoin": "round", "data_outline": "stroke"}
        self._add(f"<{tag} {_attrs(a)}/>")

    def T(self, d: str, color: str, w: float, cap: str = "round") -> None:
        self._add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * OW:g}" '
                  f'stroke-linecap="{cap}" stroke-linejoin="round" data-outline="under"/>')
        self._add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w:g}" '
                  f'stroke-linecap="{cap}" stroke-linejoin="round"/>')

    def M(self, d: str, color: str = INK, w: float = MONO_W, dash: str | None = None, cap: str = "round") -> None:
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self._add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w:g}" '
                  f'stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>')

    def raw(self, s: str) -> None:
        self._add(s)

    def open(self, gid: str | None = None, pivot: str | None = None, transform: str | None = None) -> None:
        self._add(f"<g {_attrs({'id': gid, 'data_pivot': pivot, 'transform': transform})}>".replace("<g >", "<g>"))
        self.depth += 1

    def close(self) -> None:
        self.depth -= 1
        self._add("</g>")

    def text(self) -> str:
        assert self.depth == 0, "unclosed group"
        body = "\n  ".join(self.parts)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">\n  {body}\n</svg>\n'


def save(category: str, item_id: str, s: Svg) -> Path:
    out = ROOT / "svg" / category / f"{item_id}.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s.text(), encoding="utf-8")
    return out


def flat(svg_text: str) -> str:
    """Style A: drop outline under-strokes and the stroke attributes of outlined shapes."""
    svg_text = re.sub(r'\n?[ \t]*<[^<>]*data-outline="under"[^<>]*/>', "", svg_text)

    def strip(m: re.Match) -> str:
        tag = m.group(0)
        for attr in ("stroke", "stroke-width", "stroke-linejoin", "data-outline"):
            tag = re.sub(rf'\s{attr}="[^"]*"', "", tag)
        return tag
    return re.sub(r'<[^<>]*data-outline="stroke"[^<>]*/>', strip, svg_text)


# ---------------------------------------------------------------- geometry helpers
def head(x: float, y: float, angle: float, length: float = 84, spread: float = 40) -> str:
    """Open arrow head path at tip (x, y), pointing along angle (degrees, SVG y-down)."""
    pts = []
    for s in (-spread, spread):
        a = math.radians(angle + 180 + s)
        pts.append((x + length * math.cos(a), y + length * math.sin(a)))
    (x1, y1), (x2, y2) = pts
    return f"M{x1:.1f} {y1:.1f} L{x:.1f} {y:.1f} L{x2:.1f} {y2:.1f}"


def ang(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def star_pts(cx: float, cy: float, r1: float, r2: float, n: int, rot: float = -90) -> str:
    out = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        out.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(out)


def arc_pt(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


# ---------------------------------------------------------------- tiny stroke font (signs, badges)
# Glyphs in a 100 x 160 box. Only for short labels inside pictures (STOP, P, 50, 10t);
# proper text tiles come from the text-tile tool.
GLYPHS = {
    "S": "M90 25 C75 0 10 0 10 40 C10 80 90 75 90 118 C90 165 20 165 8 130",
    "T": "M5 5 H95 M50 5 V155",
    "O": "M50 5 C10 5 5 50 5 80 C5 110 10 155 50 155 C90 155 95 110 95 80 C95 50 90 5 50 5Z",
    "P": "M14 155 V5 H55 C100 5 100 85 55 85 H14",
    "H": "M10 5 V155 M90 5 V155 M10 80 H90",
    "0": "M50 5 C15 5 10 50 10 80 C10 110 15 155 50 155 C85 155 90 110 90 80 C90 50 85 5 50 5Z",
    "1": "M26 34 L60 5 V155",
    "2": "M12 40 C12 0 88 0 88 45 C88 80 12 110 10 155 H92",
    "3": "M12 22 C30 -5 88 0 88 40 C88 70 55 78 40 78 C62 78 92 86 92 118 C92 165 20 165 8 135",
    "4": "M70 155 V5 L5 110 H98",
    "5": "M88 5 H20 L14 72 C42 55 92 60 92 106 C92 160 26 165 8 132",
    "6": "M80 12 C40 0 8 40 8 100 C8 160 92 160 92 108 C92 65 30 60 10 95",
    "7": "M8 5 H92 L40 155",
    "8": "M50 78 C12 78 12 5 50 5 C88 5 88 78 50 78 C6 78 6 155 50 155 C94 155 94 78 50 78Z",
    "9": "M90 62 C70 95 8 92 8 50 C8 0 92 0 92 55 C92 120 60 160 20 150",
    "m": "M8 155 V72 M8 92 C8 60 50 50 50 90 V155 M50 90 C50 50 92 60 92 92 V155",
    "t": "M42 20 V136 C42 158 62 158 82 150 M14 64 H78",
    "A": "M8 155 L50 5 L92 155 M24 100 H76",
    "B": "M14 155 V5 H55 C95 5 95 78 55 78 H14 M55 78 C100 78 100 155 55 155 H14",
    "C": "M90 30 C70 0 10 0 10 80 C10 160 70 160 90 130",
    "D": "M14 5 V155 H45 C100 155 100 5 45 5 Z",
    "E": "M88 5 H14 V155 H88 M14 80 H70",
    "X": "M10 5 L90 155 M90 5 L10 155",
    "?": "M14 40 C14 0 86 0 86 42 C86 80 50 80 50 115 M50 148 V152",
    "+": "M50 30 V130 M0 80 H100",
    "=": "M5 55 H95 M5 105 H95",
    "-": "M10 80 H90",
    "x": "M15 45 L85 135 M85 45 L15 135",
    " ": "",
}


def stroke_text(s: "Svg", txt: str, cx: float, cy: float, h: float, color: str, w: float) -> None:
    k = h / 160
    adv = 100 * k + 26 * k
    x = cx - (adv * len(txt) - 26 * k) / 2
    for ch in txt:
        s.raw(f'<path d="{GLYPHS[ch]}" transform="translate({x:.1f} {cy - h / 2:.1f}) scale({k:.4f})" fill="none" '
              f'stroke="{color}" stroke-width="{w / k:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        x += adv


def run(category: str, drawings: dict, only: list[str] | None = None) -> None:
    """Draw every (or only the given) item of a category drawing module."""
    cat = json.loads((ROOT / "catalog" / f"{category}.json").read_text(encoding="utf-8"))
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from check_catalog import slug
    ids = set()
    for g in cat["groups"]:
        for it in g["items"]:
            ids.add(it["id"] if isinstance(it, dict) and "id" in it else slug(it if isinstance(it, str) else (it[0] if isinstance(it, list) else it["name"])))
    import inspect
    src = Path(inspect.stack()[1].filename).read_text(encoding="utf-8")
    bad = [m for m in ("if False", ":= None") if m in src]
    assert not bad, f"placeholder shortcuts left in the drawing script: {bad}"
    unknown = [k for k in drawings if k not in ids]
    assert not unknown, f"not in catalog/{category}.json: {unknown}"
    n = 0
    for item_id, fn in drawings.items():
        if only and item_id not in only:
            continue
        s = Svg()
        fn(s)
        save(category, item_id, s)
        n += 1
    print(f"{category}: drew {n}")
