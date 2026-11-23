"""Text as vector paths for Asset Studio tiles.

Text is shaped with HarfBuzz (so Arabic joins and Devanagari/Gurmukhi conjuncts are right) and
each glyph outline is turned into SVG path data with fontTools. The SVGs then need no font.

Fonts (OFL, not in git): _source-data/fonts/ - see README "Text tiles".
    text_path(text, font="sans", cx=256, cy=256, max_w=400, max_h=120) -> (d, (x0, y0, x1, y1))
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "_source-data" / "fonts"
FONTS = {
    "sans": "NotoSans-Bold.ttf",
    "black": "NotoSans-Black.ttf",
    "arabic": "Amiri-Bold.ttf",
    "devanagari": "NotoSansDevanagari-Bold.ttf",
    "gurmukhi": "NotoSansGurmukhi-Bold.ttf",
}


@lru_cache(maxsize=None)
def _load(key: str):
    path = FONT_DIR / FONTS[key]
    if not path.exists():
        raise FileNotFoundError(f"{path} missing: download the fonts listed in README.md (Text tiles)")
    blob = hb.Blob.from_file_path(str(path))
    face = hb.Face(blob)
    font = hb.Font(face)
    tt = TTFont(str(path))
    return font, tt, tt.getGlyphSet(), tt["head"].unitsPerEm


def _shape(text: str, key: str):
    font, tt, gs, upem = _load(key)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    order = tt.getGlyphOrder()
    x = 0
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((order[info.codepoint], x + pos.x_offset, pos.y_offset))
        x += pos.x_advance
    return out, gs, upem


def _outline(text: str, key: str, scale: float, ox: float, oy: float):
    glyphs, gs, upem = _shape(text, key)
    pen = SVGPathPen(gs, lambda v: f"{v:.1f}")
    bp = BoundsPen(gs)
    for name, gx, gy in glyphs:
        # font units are y-up: flip into SVG space
        tf = (scale, 0, 0, -scale, ox + gx * scale, oy - gy * scale)
        gs[name].draw(TransformPen(pen, tf))
        gs[name].draw(TransformPen(bp, tf))
    return pen.getCommands(), bp.bounds


def text_path(text: str, font: str = "sans", cx: float = 256, cy: float = 256, max_w: float = 400, max_h: float = 120,
              size: float | None = None):
    """Path data for `text`, centred on (cx, cy) and as large as fits max_w x max_h (or at `size` px em)."""
    _, _, _, upem = _load(font)
    _, b = _outline(text, font, 1.0, 0, 0)
    if b is None:
        return "", (cx, cy, cx, cy)
    w, h = b[2] - b[0], b[3] - b[1]
    k = size / upem if size else min(max_w / w, max_h / h)
    k = min(k, max_w / w, max_h / h)
    ox = cx - (b[0] + w / 2) * k
    oy = cy - (b[1] + h / 2) * k
    d, bb = _outline(text, font, k, ox, oy)
    return d, bb
