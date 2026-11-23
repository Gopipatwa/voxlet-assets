"""math drawings, part A: math-symbols (mono), numbers-ideas (tiles), fractions, shapes-2d, shapes-3d.
Run: python drawings/math_a.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID  # noqa: E402
from draw_lib import C, INK, arc_pt, run, star_pts, stroke_text  # noqa: E402
from text_tile import text_path  # noqa: E402

D = {}
WHITE = "#FFFFFF"
GREEN, YEL, RED, SKY = C["green"], C["yellow"], C["red"], C["sky"]


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def dot(s, x, y, r=17):
    s.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>')


def ring_m(s, cx, cy, r):
    s.M(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0")


def txt(s, text, cx, cy, w, h, color=WHITE, font="black"):
    d, _ = text_path(text, font, cx, cy, w, h)
    if d:
        s.F("path", outline=False, d=d, fill=color)


# ================================================================ math-symbols (mono)
D["plus-sign"] = lambda s: s.M("M256 110 V402 M110 256 H402")
D["minus-sign"] = lambda s: s.M("M110 256 H402")
D["multiplication-sign"] = lambda s: s.M("M140 140 L372 372 M372 140 L140 372")


@reg("division-sign")
def _(s):
    s.M("M110 256 H402")
    dot(s, 256, 140)
    dot(s, 256, 372)


D["equals-sign"] = lambda s: s.M("M110 190 H402 M110 322 H402")
D["not-equal-sign"] = lambda s: s.M("M110 190 H402 M110 322 H402 M330 100 L182 412")
D["greater-than-sign"] = lambda s: s.M("M150 110 L380 256 L150 402")
D["less-than-sign"] = lambda s: s.M("M362 110 L132 256 L362 402")
D["greater-than-or-equal-sign"] = lambda s: s.M("M150 80 L380 216 L150 352 M150 430 H380")
D["less-than-or-equal-sign"] = lambda s: s.M("M362 80 L132 216 L362 352 M132 430 H362")
D["approximately-equal-sign"] = lambda s: s.M("M100 190 C150 130 200 130 256 190 C312 250 362 250 412 190 M100 322 C150 262 200 262 256 322 C312 382 362 382 412 322")
D["plus-minus-sign"] = lambda s: s.M("M256 80 V270 M161 175 H351 M150 400 H362")
D["infinity-symbol"] = lambda s: s.M("M256 256 C200 140 80 140 80 256 C80 372 200 372 256 256 C312 140 432 140 432 256 C432 372 312 372 256 256")
D["pi-symbol"] = lambda s: s.M("M100 150 H412 M170 150 V400 M340 150 C340 300 330 390 395 395")
D["square-root-symbol"] = lambda s: s.M("M80 290 L130 265 L200 410 L300 100 H440")
D["sigma-symbol"] = lambda s: s.M("M390 100 H130 L290 256 L130 412 H390")
D["integral-symbol"] = lambda s: s.M("M340 100 C290 60 260 100 260 160 V350 C260 420 220 450 170 410")
D["delta-symbol"] = lambda s: s.M("M256 100 L410 400 H102 Z")
D["theta-symbol"] = lambda s: (s.M("M256 90 C150 90 150 420 256 420 C362 420 362 90 256 90Z"), s.M("M190 256 H322"))
D["ratio-sign"] = lambda s: (dot(s, 256, 170, 20), dot(s, 256, 342, 20))
D["decimal-point"] = lambda s: (stroke_text(s, "1", 120, 256, 230, INK, 24), dot(s, 256, 340, 22), stroke_text(s, "5", 392, 256, 230, INK, 24))


@reg("percent-sign")
def _(s):
    ring_m(s, 160, 160, 52)
    ring_m(s, 352, 352, 52)
    s.M("M380 110 L132 402")


@reg("per-mille-sign")
def _(s):
    ring_m(s, 110, 160, 40)
    ring_m(s, 220, 340, 40)
    ring_m(s, 372, 340, 40)
    s.M("M270 110 L60 402")


@reg("degree-sign")
def _(s):
    ring_m(s, 256, 256, 110)


@reg("cube-root-symbol")
def _(s):
    s.M("M130 300 L180 275 L240 410 L320 140 H450")
    stroke_text(s, "3", 120, 190, 80, INK, 16)


@reg("exponent")
def _(s):
    stroke_text(s, "x", 190, 300, 200, INK, 24)
    stroke_text(s, "2", 360, 150, 120, INK, 20)


@reg("factorial-sign")
def _(s):
    s.M("M256 90 V310")
    dot(s, 256, 410, 22)


# ================================================================ numbers-ideas (tiles)
def card(s, color=A1, x=40, y=100, w=432, h=312):
    s.F("rect", x=x, y=y, width=w, height=h, rx=44, fill=color)


@reg("counting")
def _(s):
    for i, c in enumerate((A1, A2, A1L)):
        s.F("rect", x=48 + i * 144, y=150, width=128, height=212, rx=34, fill=c)
        txt(s, str(i + 1), 112 + i * 144, 256, 70, 120, WHITE if i < 2 else DARK)


@reg("odd-and-even-numbers")
def _(s):
    s.F("rect", x=40, y=110, width=206, height=292, rx=40, fill=A1)
    s.F("rect", x=266, y=110, width=206, height=292, rx=40, fill=A2)
    txt(s, "1 3 5", 143, 210, 150, 60)
    txt(s, "2 4 6", 369, 210, 150, 60)
    txt(s, "ODD", 143, 330, 130, 50, A1L)
    txt(s, "EVEN", 369, 330, 150, 50, A2L)


@reg("prime-numbers")
def _(s):
    card(s, A1, 40, 140, 432, 232)
    txt(s, "2 3 5 7", 256, 256, 340, 100)
    for x in (110, 195, 290, 380):
        s.F("circle", outline=False, cx=x, cy=330, r=8, fill=A2L)


@reg("place-value")
def _(s):
    for i, (L, c, dgt) in enumerate((("H", A1, "3"), ("T", A2, "4"), ("O", A1D, "5"))):
        x = 48 + i * 144
        s.F("rect", x=x, y=110, width=128, height=292, rx=34, fill=c)
        s.F("rect", outline=False, x=x + 12, y=124, width=104, height=60, rx=22, fill=WHITE, fill_opacity="0.3")
        txt(s, L, x + 64, 154, 50, 40)
        txt(s, dgt, x + 64, 290, 70, 130)


@reg("times-table")
def _(s):
    card(s, A1, 40, 150, 432, 212)
    txt(s, "3 × 4 = 12", 256, 256, 370, 90)


@reg("number-line")
def _(s):
    s.T("M50 300 H462", DARK, 16)
    for i in range(6):
        x = 80 + i * 70
        s.M(f"M{x} 270 V330", DARK, 10)
        txt(s, str(i), x, 380, 36, 46, DARK)
    s.raw(f'<path d="M80 270 C130 150 220 150 290 270" fill="none" stroke="{A2}" stroke-width="14" stroke-linecap="round"/>')
    s.F("polygon", points="300,282 262,262 296,238", fill=A2)
    s.F("circle", cx=80, cy=300, r=18, fill=A1)


@reg("negative-numbers")
def _(s):
    s.T("M50 256 H462", DARK, 16)
    for i, v in enumerate(("−3", "−2", "−1", "0", "1", "2")):
        x = 70 + i * 74
        s.M(f"M{x} 226 V286", DARK, 10)
        txt(s, v, x, 340, 54 if len(v) > 1 else 30, 46, A2 if i < 3 else A1)
    s.F("circle", cx=70 + 74, cy=256, r=22, fill=A2)


@reg("roman-numerals")
def _(s):
    card(s, A1, 40, 150, 432, 212)
    txt(s, "I V X L", 256, 256, 350, 100)


@reg("binary-numbers")
def _(s):
    for i, b in enumerate("1011"):
        x = 50 + i * 106
        s.F("rect", x=x, y=140, width=92, height=232, rx=28, fill=A1 if b == "1" else A2)
        txt(s, b, x + 46, 256, 50, 120)


@reg("zero")
def _(s):
    s.F("circle", cx=256, cy=256, r=196, fill=A1)
    txt(s, "0", 256, 256, 150, 250)


@reg("googol")
def _(s):
    card(s, A1, 40, 140, 432, 232)
    txt(s, "10", 190, 280, 200, 140)
    txt(s, "100", 362, 190, 140, 90, A2L)


@reg("fibonacci-sequence")
def _(s):
    sq = [(0, 0, 1), (-1, 0, 1), (-1, -2, 2), (-4, -2, 3), (-4, 1, 5)]
    xs = [x for x, y, n in sq] + [x + n for x, y, n in sq]
    ys = [y for x, y, n in sq] + [y + n for x, y, n in sq]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    u = 50
    for (x, y, n), c in zip(sq, (A2, A1, A2L, A1L, A2L)):
        s.F("rect", x=256 + (x - cx) * u, y=256 + (y - cy) * u, width=n * u, height=n * u, fill=c)
        txt(s, str(n), 256 + (x - cx + n / 2) * u, 256 + (y - cy + n / 2) * u, 14 + n * 9, 20 + n * 11, DARK if c in (A2L, A1L) else WHITE)


@reg("golden-ratio")
def _(s):
    s.F("rect", x=50, y=130, width=412, height=254, rx=14, fill=A1L)
    s.F("rect", outline=False, x=50, y=130, width=254, height=254, fill=A2L)
    s.raw(f'<path d="M304 130 V384 M304 258 H462 M404 258 V384" fill="none" stroke="{INK}" stroke-width="8"/>')
    s.raw(f'<path d="M304 384 A254 254 0 0 1 50 130" fill="none" stroke="{DARK}" stroke-width="12" stroke-linecap="round"/>')
    txt(s, "φ", 400, 190, 60, 70, A1D)


@reg("pascals-triangle")
def _(s):
    rows = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
    for r, row in enumerate(rows):
        for i, v in enumerate(row):
            x = 256 + (i - (len(row) - 1) / 2) * 92
            y = 110 + r * 100
            s.F("circle", cx=x, cy=y, r=44, fill=A1 if v == 1 else A2)
            txt(s, str(v), x, y, 30, 46)


@reg("square-numbers")
def _(s):
    k = 58
    for n, x0 in ((1, 30), (2, 110), (3, 250)):
        for i in range(n):
            for j in range(n):
                s.F("rect", x=x0 + i * k, y=420 - (j + 1) * k, width=k - 5, height=k - 5, rx=8, fill=(A2, A1, A1L)[n - 1])


@reg("big-numbers")
def _(s):
    card(s, A1, 40, 150, 432, 212)
    txt(s, "1,000,000", 256, 256, 380, 90)


# ================================================================ fractions
def wedge(cx, cy, r, a0, a1):
    x0, y0 = arc_pt(cx, cy, r, a0)
    x1, y1 = arc_pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}Z"


def pie(s, n, k, cx=256, cy=256, r=190, on=A1, off=LIGHT, start=-90):
    s.F("circle", cx=cx, cy=cy, r=r, fill=off)
    if k >= n:
        s.F("circle", cx=cx, cy=cy, r=r, fill=on)
    elif k > 0:
        s.F("path", d=wedge(cx, cy, r, start, start + 360 * k / n), fill=on)
    for i in range(n):
        x, y = arc_pt(cx, cy, r, start + 360 * i / n)
        s.M(f"M{cx} {cy} L{x:.0f} {y:.0f}", INK, 8)
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')


@reg("fraction")
def _(s):
    txt(s, "1", 256, 130, 70, 130, A1)
    s.T("M130 256 H382", DARK, 22)
    txt(s, "2", 256, 380, 80, 130, A2)


@reg("half")
def _(s):
    pie(s, 2, 1, start=-90)


@reg("third")
def _(s):
    pie(s, 3, 1)


@reg("quarter")
def _(s):
    pie(s, 4, 1)


@reg("three-quarters")
def _(s):
    pie(s, 4, 3)


@reg("fraction-pizza")
def _(s):
    s.F("circle", cx=256, cy=270, r=190, fill=C["tan"])
    s.F("circle", outline=False, cx=256, cy=270, r=160, fill=A2L)
    for a, rr in ((20, 90), (80, 110), (140, 80), (200, 100), (260, 70), (320, 110), (50, 40), (230, 140)):
        x, y = arc_pt(256, 270, rr, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=24, fill=RED)
    for a in (0, 90, 180, 270):
        x, y = arc_pt(256, 270, 190, a)
        s.M(f"M256 270 L{x:.0f} {y:.0f}", INK, 8)
    s.F("path", d="M300 230 L460 100 A190 190 0 0 1 446 346Z", fill=C["tan"], transform="translate(26 -26)")
    s.F("path", outline=False, d="M316 230 L436 138 A150 150 0 0 1 428 300Z", fill=A2L, transform="translate(26 -26)")


@reg("fraction-bar")
def _(s):
    for i in range(4):
        s.F("rect", x=52 + i * 102, y=190, width=102, height=132, fill=A1 if i < 3 else LIGHT)
    s.raw(f'<rect x="52" y="190" width="408" height="132" rx="16" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    txt(s, "3", 256, 120, 50, 70, A1)
    s.M("M216 160 H296", DARK, 6)


@reg("decimal")
def _(s):
    card(s, A1, 40, 150, 432, 212)
    txt(s, "0.5", 256, 256, 330, 120)


@reg("percentage-bar")
def _(s):
    s.F("rect", x=40, y=190, width=432, height=100, rx=50, fill=LIGHT)
    s.F("rect", x=40, y=190, width=324, height=100, rx=50, fill=A1)
    txt(s, "75%", 256, 390, 220, 80, A2)


@reg("ratio-and-proportion")
def _(s):
    for i in range(2):
        s.F("circle", cx=110 + i * 90, cy=150, r=36, fill=A1)
    for i in range(3):
        s.F("circle", cx=110 + i * 90, cy=290, r=36, fill=A2)
    txt(s, "2 : 3", 340, 370, 250, 70, DARK)
    s.F("rect", outline=False, x=40, y=420, width=432, height=14, rx=7, fill=A1L)


# ================================================================ shapes-2d
def poly(n, cx=256, cy=270, r=200, rot=-90):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in (arc_pt(cx, cy, r, rot + i * 360 / n) for i in range(n)))


def regular(s, n, color=A1, light=A1L, r=200, rot=-90, cy=266):
    s.F("polygon", points=poly(n, 256, cy, r, rot), fill=color)
    s.F("polygon", outline=False, points=poly(n, 256 + 0, cy, r * 0.62, rot), fill=light, fill_opacity="0.55")


D["circle"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=A1), s.F("circle", outline=False, cx=256, cy=256, r=124, fill=A1L, fill_opacity="0.55"))
D["semicircle"] = lambda s: (s.F("path", d="M56 330 A200 200 0 0 1 456 330Z", fill=A2), s.F("path", outline=False, d="M110 310 A146 146 0 0 1 402 310Z", fill=A2L, fill_opacity="0.55"))
D["oval"] = lambda s: (s.F("ellipse", cx=256, cy=256, rx=210, ry=140, fill=A2), s.F("ellipse", outline=False, cx=256, cy=256, rx=130, ry=82, fill=A2L, fill_opacity="0.55"))
D["triangle"] = lambda s: (s.F("polygon", points="256,60 460,440 52,440", fill=A1), s.F("polygon", outline=False, points="256,190 350,364 162,364", fill=A1L, fill_opacity="0.55"))
D["equilateral-triangle"] = lambda s: (s.F("polygon", points="256,70 456,416 56,416", fill=A1), s.F("polygon", outline=False, points="256,190 350,352 162,352", fill=A1L, fill_opacity="0.55"),
                                       [s.M(f"M{a} {b} l{dx} {dy}", WHITE, 8) for a, b, dx, dy in ((156, 244, 20, 12), (356, 244, -20, 12), (256, 416, 0, -22))])
D["isosceles-triangle"] = lambda s: (s.F("polygon", points="256,50 400,440 112,440", fill=A2), s.F("polygon", outline=False, points="256,190 330,370 182,370", fill=A2L, fill_opacity="0.55"))
D["scalene-triangle"] = lambda s: (s.F("polygon", points="130,70 460,400 56,440", fill=A1), s.F("polygon", outline=False, points="170,210 330,350 120,370", fill=A1L, fill_opacity="0.55"))
D["square"] = lambda s: (s.F("rect", x=70, y=70, width=372, height=372, rx=20, fill=A1), s.F("rect", outline=False, x=130, y=130, width=252, height=252, rx=14, fill=A1L, fill_opacity="0.55"))
D["rectangle"] = lambda s: (s.F("rect", x=40, y=130, width=432, height=252, rx=20, fill=A2), s.F("rect", outline=False, x=100, y=180, width=312, height=152, rx=12, fill=A2L, fill_opacity="0.55"))
D["rhombus"] = lambda s: (s.F("polygon", points="256,40 440,256 256,472 72,256", fill=A1), s.F("polygon", outline=False, points="256,150 340,256 256,362 172,256", fill=A1L, fill_opacity="0.55"))
D["parallelogram"] = lambda s: (s.F("polygon", points="150,130 460,130 362,382 52,382", fill=A2), s.F("polygon", outline=False, points="190,176 392,176 330,336 128,336", fill=A2L, fill_opacity="0.55"))
D["trapezium"] = lambda s: (s.F("polygon", points="170,130 342,130 462,382 50,382", fill=A1), s.F("polygon", outline=False, points="196,180 316,180 392,334 120,334", fill=A1L, fill_opacity="0.55"))
D["kite-shape"] = lambda s: (s.F("polygon", points="256,40 400,190 256,472 112,190", fill=A2), s.F("polygon", outline=False, points="256,130 332,200 256,340 180,200", fill=A2L, fill_opacity="0.55"),
                             s.M("M256 40 V472 M112 190 H400", WHITE, 6))
D["pentagon"] = lambda s: regular(s, 5, A1, A1L)
D["hexagon"] = lambda s: regular(s, 6, A2, A2L, rot=0, cy=256)
D["heptagon"] = lambda s: regular(s, 7, A1, A1L)
D["octagon"] = lambda s: regular(s, 8, A2, A2L, rot=-67.5, cy=256)
D["nonagon"] = lambda s: regular(s, 9, A1, A1L)
D["decagon"] = lambda s: regular(s, 10, A2, A2L, rot=-90, cy=256)
D["star-shape-polygon"] = lambda s: (s.F("polygon", points=star_pts(256, 270, 210, 90, 5), fill=A2), s.F("polygon", outline=False, points=star_pts(256, 270, 110, 50, 5), fill=A2L, fill_opacity="0.6"))
D["crescent-shape"] = lambda s: s.F("path", d="M330 70 A200 200 0 1 0 330 442 A160 160 0 1 1 330 70Z", fill=A1)
D["heart-shape"] = lambda s: (s.F("path", d="M256 440 C60 310 40 200 60 150 C90 70 200 60 256 150 C312 60 422 70 452 150 C472 200 452 310 256 440Z", fill=A2), s.F("path", outline=False, d="M120 150 C140 110 190 106 220 160", fill="none", stroke=A2L, stroke_width="26", stroke_linecap="round", stroke_opacity="0.8"))
D["arrow-shape"] = lambda s: (s.F("polygon", points="60,190 290,190 290,90 460,256 290,422 290,322 60,322", fill=A1), s.F("polygon", outline=False, points="90,214 300,214 300,150 400,256 300,300 90,300", fill=A1L, fill_opacity="0.4"))
D["cross-shape"] = lambda s: (s.F("polygon", points="190,50 322,50 322,190 462,190 462,322 322,322 322,462 190,462 190,322 50,322 50,190 190,190", fill=A2), s.F("rect", outline=False, x=214, y=214, width=84, height=84, rx=10, fill=A2L, fill_opacity="0.6"))


@reg("right-triangle")
def _(s):
    s.F("polygon", points="80,430 80,80 440,430", fill=A2)
    s.F("polygon", outline=False, points="120,380 120,220 290,380", fill=A2L, fill_opacity="0.55")
    s.M("M80 360 H150 V430", WHITE, 12)


@reg("ring-shape")
def _(s):
    s.raw(f'<path d="M256 56 A200 200 0 1 1 255.9 56Z M256 156 A100 100 0 1 0 256.1 156Z" fill="{A2}" fill-rule="evenodd" stroke="{INK}" stroke-width="10" stroke-linejoin="round" data-outline="stroke"/>')
    s.raw(f'<path d="M110 180 A160 160 0 0 1 220 100" fill="none" stroke="{A2L}" stroke-width="22" stroke-linecap="round"/>')


# ================================================================ shapes-3d
@reg("cube")
def _(s):
    s.F("polygon", points="256,60 436,160 256,260 76,160", fill=A1L)
    s.F("polygon", points="76,160 256,260 256,460 76,360", fill=A1)
    s.F("polygon", points="436,160 256,260 256,460 436,360", fill=A1D)


@reg("cuboid")
def _(s):
    s.F("polygon", points="90,200 230,110 450,150 310,250", fill=A2L)
    s.F("polygon", points="90,200 310,250 310,420 90,360", fill=A2)
    s.F("polygon", points="450,150 310,250 310,420 450,320", fill="#D87420")


@reg("sphere")
def _(s):
    s.F("ellipse", outline=False, cx=256, cy=454, rx=130, ry=20, fill=DARK, fill_opacity="0.18")
    s.F("circle", cx=256, cy=240, r=190, fill=A1)
    s.F("circle", outline=False, cx=200, cy=180, r=70, fill=A1L, fill_opacity="0.75")


@reg("hemisphere")
def _(s):
    s.F("path", d="M60 280 A196 196 0 0 1 452 280Z", fill=A2)
    s.F("ellipse", cx=256, cy=280, rx=196, ry=60, fill="#D87420")
    s.F("path", outline=False, d="M110 250 C130 190 190 150 240 140", fill="none", stroke="#F9B57A", stroke_width="30", stroke_linecap="round")


@reg("cylinder")
def _(s):
    s.F("path", d="M100 130 V380 C100 440 412 440 412 380 V130Z", fill=A1)
    s.F("path", outline=False, d="M130 150 V380 C130 400 150 412 170 416 V150Z", fill=A1L, fill_opacity="0.5")
    s.F("ellipse", cx=256, cy=130, rx=156, ry=60, fill=A1L)


@reg("cone")
def _(s):
    s.F("path", d="M256 50 L420 380 C420 450 92 450 92 380Z", fill=A2)
    s.F("path", outline=False, d="M256 80 L160 340 C140 380 150 400 190 418 Z", fill="#F9B57A", fill_opacity="0.6")


@reg("pyramid")
def _(s):
    s.F("polygon", points="256,50 440,360 256,450 60,350", fill=A2L)
    s.F("polygon", points="256,50 60,350 256,450", fill=A2)
    s.F("polygon", points="256,50 440,360 256,450", fill="#D87420")


@reg("triangular-prism")
def _(s):
    s.F("polygon", points="80,420 330,420 440,340 190,340", fill=A1D)
    s.F("polygon", points="205,170 330,420 440,340 320,100", fill=A1)
    s.F("polygon", points="80,420 205,170 330,420", fill=A1L)


@reg("tetrahedron")
def _(s):
    s.F("polygon", points="256,50 450,400 256,310", fill="#D87420")
    s.F("polygon", points="256,50 60,400 256,310", fill=A2)
    s.F("polygon", points="60,400 450,400 256,310", fill="#F9B57A")


@reg("octahedron")
def _(s):
    s.F("polygon", points="256,40 440,256 256,300 72,256", fill=A1L)
    s.F("polygon", points="256,300 72,256 256,472", fill=A1)
    s.F("polygon", points="256,300 440,256 256,472", fill=A1D)


@reg("dodecahedron")
def _(s):
    s.F("polygon", points=poly(5, 256, 256, 210, -90), fill=A2)
    inner = poly(5, 256, 256, 86, -90)
    s.F("polygon", points=inner, fill=A2L)
    outer = [arc_pt(256, 256, 210, -90 + i * 72) for i in range(5)]
    inn = [arc_pt(256, 256, 86, -90 + i * 72) for i in range(5)]
    for (ox, oy), (ix, iy) in zip(outer, inn):
        s.M(f"M{ox:.0f} {oy:.0f} L{ix:.0f} {iy:.0f}", INK, 10)


@reg("icosahedron")
def _(s):
    s.F("polygon", points=poly(6, 256, 256, 210, 0), fill=A1)
    s.F("polygon", points=poly(3, 256, 256, 130, 90), fill=A1L)
    for i in range(3):
        ax, ay = arc_pt(256, 256, 130, 90 + i * 120)
        bx, by = arc_pt(256, 256, 210, i * 120 + 60)
        cx, cy = arc_pt(256, 256, 210, i * 120 + 120)
        s.M(f"M{ax:.0f} {ay:.0f} L{bx:.0f} {by:.0f} M{ax:.0f} {ay:.0f} L{cx:.0f} {cy:.0f}", INK, 8)


@reg("torus")
def _(s):
    s.raw(f'<path d="M256 120 C400 120 470 200 470 280 C470 380 350 430 256 430 C162 430 42 380 42 280 C42 200 112 120 256 120Z '
          f'M256 220 C190 220 150 250 150 285 C150 320 200 345 256 345 C312 345 362 320 362 285 C362 250 322 220 256 220Z" '
          f'fill="{A2}" fill-rule="evenodd" stroke="{INK}" stroke-width="10" stroke-linejoin="round" data-outline="stroke"/>')
    s.F("path", outline=False, d="M110 250 C130 190 200 150 260 148", fill="none", stroke="#F9B57A", stroke_width="22", stroke_linecap="round")


if __name__ == "__main__":
    run("math", D, sys.argv[1:] or None)
