"""math drawings, part B: geometry (mono), geometry-tools, graphs-charts, probability, measurement.
Run: python drawings/math_b.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run, star_pts, stroke_text  # noqa: E402
from text_tile import text_path  # noqa: E402

D = {}
WHITE = "#FFFFFF"
GREEN, YEL, RED, SKY, GREY, DGREY, BROWN, TAN, GOLD, PURPLE, PINK, ORANGE = (C[k] for k in ("green", "yellow", "red", "sky", "grey", "darkgrey", "brown", "tan", "gold", "purple", "pink", "orange"))
GLASS = "#E3F3FC"


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def dot(s, x, y, r=18):
    s.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>')


def ring_m(s, cx, cy, r, w=None):
    s.M(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", INK, w or 24)


def txt(s, text, cx, cy, w, h, color=WHITE, font="black"):
    d, _ = text_path(text, font, cx, cy, w, h)
    if d:
        s.F("path", outline=False, d=d, fill=color)


# ================================================================ geometry (mono)
def two_rays(s, a, r=170, ox=110, oy=380, arc=70, mark=None):
    x1, y1 = ox + r * 2.2, oy
    x2, y2 = arc_pt(ox, oy, r * 2.2, -a)
    s.M(f"M{x1:.0f} {y1:.0f} L{ox} {oy} L{x2:.0f} {y2:.0f}")
    ax, ay = arc_pt(ox, oy, arc, -a)
    s.M(f"M{ox + arc} {oy} A{arc} {arc} 0 {1 if a > 180 else 0} 0 {ax:.0f} {ay:.0f}", INK, 14)


D["angle"] = lambda s: two_rays(s, 50)
D["acute-angle"] = lambda s: two_rays(s, 40)
D["obtuse-angle"] = lambda s: two_rays(s, 130, 160, 220, 380)


@reg("right-angle")
def _(s):
    s.M("M90 400 H420 M90 400 V90")
    s.M("M90 320 H170 V400", INK, 14)


@reg("straight-angle")
def _(s):
    s.M("M60 330 H452")
    s.M("M170 330 A86 86 0 0 1 342 330", INK, 14)
    dot(s, 256, 330, 16)


@reg("reflex-angle")
def _(s):
    s.M("M420 256 H256 L380 130")
    ax, ay = arc_pt(256, 256, 84, -45)
    s.raw(f'<path d="M{ax:.0f} {ay:.0f} A84 84 0 1 0 340 256" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>')
    dot(s, 256, 256, 16)


@reg("parallel-lines")
def _(s):
    s.M("M70 180 H442 M70 332 H442")
    s.M("M240 150 L270 180 L240 210", INK, 12)
    s.M("M240 302 L270 332 L240 362", INK, 12)


@reg("perpendicular-lines")
def _(s):
    s.M("M70 400 H442 M200 70 V400")
    s.M("M200 330 H270 V400", INK, 14)


@reg("line-segment")
def _(s):
    s.M("M110 256 H402")
    dot(s, 110, 256, 30)
    dot(s, 402, 256, 30)


@reg("ray")
def _(s):
    s.M("M110 256 H420 " + head(440, 256, 0, 70, 40))
    dot(s, 110, 256, 30)


@reg("radius")
def _(s):
    s.M("M256 56 a200 200 0 1 0 0.1 0Z")
    s.M("M256 256 L400 112")
    dot(s, 256, 256, 24)


@reg("diameter")
def _(s):
    s.M("M256 56 a200 200 0 1 0 0.1 0Z")
    s.M("M70 330 L442 182", INK, 24)
    dot(s, 256, 256, 18)


@reg("circumference")
def _(s):
    s.M("M256 76 a180 180 0 1 0 0.1 0Z", INK, 30)
    s.M("M420 150 L450 180 L400 190", INK, 16)
    dot(s, 256, 256, 14)


@reg("area")
def _(s):
    s.M("M90 90 H422 V422 H90Z")
    s.M("M90 200 H422 M90 311 H422 M200 90 V422 M311 90 V422", INK, 10)


@reg("perimeter")
def _(s):
    s.M("M110 110 H402 V402 H110Z", INK, 24)
    for x, y in ((110, 110), (402, 110), (402, 402), (110, 402)):
        dot(s, x, y, 22)
    s.M("M256 40 H300 M256 40 L282 14 M256 40 L282 66", INK, 12)


@reg("volume")
def _(s):
    s.M("M110 180 L256 100 L402 180 L256 260Z M110 180 V350 L256 430 L402 350 V180 M256 260 V430")
    s.M("M110 265 L256 345 L402 265 M183 222 L329 302", INK, 8)


@reg("symmetry")
def _(s):
    s.M("M256 50 V462", INK, 12, dash="16 20")
    s.M("M256 150 C200 90 90 110 90 200 C90 290 200 300 256 260 C200 310 110 360 130 420 C190 440 240 360 256 340")
    s.M("M256 150 C312 90 422 110 422 200 C422 290 312 300 256 260 C312 310 402 360 382 420 C322 440 272 360 256 340")


@reg("rotational-symmetry")
def _(s):
    s.M("M256 110 L296 210 L402 216 L322 286 L346 392 L256 334 L166 392 L190 286 L110 216 L216 210Z")
    s.M("M256 40 A216 216 0 0 1 462 190 " + head(462, 190, 80, 56, 40))
    dot(s, 256, 256, 14)


@reg("tessellation")
def _(s):
    rr = 70
    for cx, cy in ((256, 256), (256 + rr * 1.732, 256 - rr * 1.5 + rr * 0), (256 + rr * 1.732, 256 + rr * 1.5 + rr * 0), (256 - rr * 1.732, 256 - rr * 1.5), (256 - rr * 1.732, 256 + rr * 1.5), (256, 256 - rr * 3), (256, 256 + rr * 3)):
        s.M("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in (arc_pt(cx, cy, rr * 0.98, 30 + i * 60) for i in range(6))) + "Z", INK, 12)


@reg("coordinates")
def _(s):
    s.M("M80 80 V432 H432", INK, 16)
    for i in range(1, 5):
        s.M(f"M{80 + i * 70} 432 V420 M80 {432 - i * 70} H92", INK, 10)
    s.M("M290 432 V222 H80", INK, 8, dash="12 16")
    dot(s, 290, 222, 24)


@reg("x-and-y-axis")
def _(s):
    s.M("M256 50 V462 M50 256 H462")
    s.M("M256 50 l-24 36 M256 50 l24 36 M462 256 l-36 -24 M462 256 l-36 24", INK, 14)
    for i in (-2, -1, 1, 2):
        s.M(f"M{256 + i * 80} 240 V272 M240 {256 + i * 80} H272", INK, 10)


@reg("pythagoras-theorem")
def _(s):
    s.open(transform="translate(70 0)")
    s.M("M130 290 L280 290 L280 178 Z", INK, 20)
    s.M("M130 290 V440 H280 V290", INK, 14)
    s.M("M280 178 H392 V290 H280", INK, 14)
    s.M("M130 290 L280 178 L168 28 L18 140Z", INK, 14)
    s.M("M280 262 H252 V290", INK, 10)
    s.close()


# ================================================================ geometry-tools (keep)
@reg("ruler")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    s.F("rect", x=20, y=190, width=472, height=132, rx=16, fill=GOLD)
    s.F("rect", outline=False, x=34, y=200, width=444, height=28, rx=10, fill=WHITE, fill_opacity="0.35")
    for i in range(0, 22):
        x = 50 + i * 20.2
        s.M(f"M{x:.0f} 190 v{44 if i % 5 == 0 else 28}", DARK, 6)
    s.close()


@reg("protractor")
def _(s):
    s.F("path", d="M50 400 A206 206 0 0 1 462 400Z", fill=GLASS)
    s.F("path", outline=False, d="M130 400 A126 126 0 0 1 382 400Z", fill=WHITE)
    for i in range(0, 19):
        x1, y1 = arc_pt(256, 400, 206, 180 + i * 10)
        x2, y2 = arc_pt(256, 400, 206 - (34 if i % 3 == 0 else 20), 180 + i * 10)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DARK, 6)
    s.M("M256 400 V250", RED, 8)
    s.F("circle", cx=256, cy=400, r=14, fill=RED)


@reg("geometry-compass")
def _(s):
    s.T("M256 90 L130 440", GREY, 30)
    s.T("M256 90 L382 400", GREY, 30)
    s.F("circle", cx=256, cy=90, r=40, fill=A1)
    s.F("rect", x=226, y=20, width=60, height=40, rx=12, fill=A2)
    s.F("path", d="M382 400 L394 450 L370 450Z", fill=DGREY)
    s.F("path", d="M130 440 L120 480 L142 480Z", fill=DGREY)
    s.T("M200 250 H320", DGREY, 12)


@reg("set-square")
def _(s):
    s.F("polygon", points="60,430 60,90 440,430", fill=GLASS)
    s.F("polygon", outline=False, points="130,360 130,230 280,360", fill=WHITE)
    for i in range(0, 9):
        s.M(f"M60 {430 - i * 38} h{24 if i % 2 == 0 else 14}", DARK, 6)


@reg("geometry-box")
def _(s):
    s.F("rect", x=40, y=140, width=432, height=260, rx=28, fill=GREY)
    s.F("rect", outline=False, x=60, y=160, width=392, height=220, rx=18, fill=DGREY)
    s.F("rect", x=70, y=170, width=150, height=26, rx=8, fill=GOLD)
    s.F("circle", cx=300, cy=290, r=54, fill=A1)
    s.F("polygon", points="90,360 90,230 200,360", fill=GLASS)
    s.F("rect", x=240, y=190, width=190, height=28, rx=10, fill=A2)
    s.F("rect", x=200, y=110, width=112, height=44, rx=14, fill=DGREY)


def calc_body(s, color, w=292, x=110):
    s.F("rect", x=x, y=40, width=w, height=432, rx=40, fill=color)
    s.F("rect", x=x + 24, y=66, width=w - 48, height=100, rx=14, fill="#B8E0D0")


@reg("calculator")
def _(s):
    calc_body(s, DGREY)
    txt(s, "42", 330, 118, 100, 54, "#1F2A35")
    for r in range(4):
        for c in range(3):
            col = A2 if c == 2 else GREY
            s.F("rect", x=140 + c * 80, y=200 + r * 66, width=64, height=52, rx=14, fill=col)


@reg("scientific-calculator")
def _(s):
    calc_body(s, A1D)
    txt(s, "√2", 316, 118, 100, 54, "#1F2A35")
    for r in range(2):
        for c in range(4):
            s.F("rect", x=136 + c * 62, y=190 + r * 48, width=52, height=36, rx=12, fill=A2L)
    for r in range(3):
        for c in range(4):
            s.F("rect", x=136 + c * 62, y=290 + r * 58, width=52, height=44, rx=14, fill=GREY if c < 3 else A2)


@reg("abacus")
def _(s):
    s.F("rect", x=50, y=60, width=412, height=392, rx=30, fill=BROWN)
    s.F("rect", outline=False, x=80, y=90, width=352, height=332, rx=14, fill="#F7E3C4")
    for i, y in enumerate((130, 200, 270, 340, 400)):
        s.T(f"M90 {y} H422", DGREY, 8)
        for j in range(4):
            x = 120 + j * 44 + (i % 2) * 150
            s.F("circle", cx=x, cy=y, r=24, fill=(RED, A1, GREEN, YEL, A2)[i])


@reg("counting-beads")
def _(s):
    for i, y in enumerate((120, 220, 320, 420)):
        s.T(f"M50 {y} H462", DGREY, 8)
        for j in range(8):
            s.F("circle", cx=76 + j * 46, cy=y, r=22, fill=(RED, YEL, A1, GREEN)[i])


@reg("graph-paper")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=16, fill=WHITE)
    for i in range(1, 8):
        s.M(f"M{60 + i * 49} 60 V452 M60 {60 + i * 49} H452", A1L, 4)
    s.F("rect", outline=False, x=60, y=60, width=392, height=0.01, fill=WHITE)
    s.M("M60 256 H452 M256 60 V452", A1, 6)
    s.M("M110 380 L200 300 L290 330 L400 150", RED, 10)


@reg("number-cubes")
def _(s):
    for x, y, rot, c, t in ((60, 190, -10, RED, "1"), (190, 120, 8, A1, "2"), (310, 200, -6, GREEN, "3"), (130, 320, 6, YEL, "4"), (270, 330, -12, A2, "5")):
        s.open(transform=f"rotate({rot} {x + 60} {y + 60})")
        s.F("rect", x=x, y=y, width=120, height=120, rx=22, fill=c)
        txt(s, t, x + 60, y + 60, 50, 70, DARK if c == YEL else WHITE)
        s.close()


# ================================================================ graphs-charts (themed)
@reg("bar-chart")
def _(s):
    s.T("M70 60 V440 H450", DARK, 14)
    for i, (h, c) in enumerate(((120, A1), (210, A2), (160, A1L), (300, A1))):
        s.F("rect", x=110 + i * 82, y=420 - h, width=56, height=h, rx=8, fill=c)


@reg("line-graph")
def _(s):
    s.T("M70 60 V440 H450", DARK, 14)
    s.T("M100 380 L190 280 L270 320 L360 180 L430 110", A1, 20)
    for x, y in ((100, 380), (190, 280), (270, 320), (360, 180), (430, 110)):
        s.F("circle", cx=x, cy=y, r=20, fill=A2)


@reg("pie-chart")
def _(s):
    def w(a0, a1, color):
        x0, y0 = arc_pt(256, 256, 190, a0)
        x1, y1 = arc_pt(256, 256, 190, a1)
        s.F("path", d=f"M256 256 L{x0:.0f} {y0:.0f} A190 190 0 {1 if a1 - a0 > 180 else 0} 1 {x1:.0f} {y1:.0f}Z", fill=color)
    w(-90, 40, A1)
    w(40, 150, A2)
    w(150, 270, A1L)
    s.F("path", d="M256 256 L256 66 A190 190 0 0 1 380 112Z", fill=A2L, transform="translate(14 -14)")


@reg("pictogram")
def _(s):
    for r, n in enumerate((4, 2, 3)):
        for i in range(n):
            s.F("circle", cx=150 + i * 68, cy=120 + r * 130, r=28, fill=(A1, A2, A1L)[r])
        s.M(f"M70 {120 + r * 130} h0.1", DARK, 24)
    s.T("M70 60 V440", DARK, 12)


@reg("histogram")
def _(s):
    s.T("M70 60 V440 H450", DARK, 14)
    for i, h in enumerate((90, 170, 260, 200, 120)):
        s.F("rect", x=84 + i * 72, y=420 - h, width=72, height=h, fill=A1 if i % 2 == 0 else A2)


@reg("scatter-plot")
def _(s):
    s.T("M70 60 V440 H450", DARK, 14)
    for x, y, c in ((130, 360, A1), (170, 300, A2), (220, 320, A1), (250, 240, A2), (290, 260, A1), (330, 180, A2), (380, 200, A1), (410, 120, A2), (190, 380, A2), (340, 270, A1)):
        s.F("circle", cx=x, cy=y, r=20, fill=c)


@reg("venn-diagram")
def _(s):
    s.F("circle", cx=190, cy=256, r=140, fill=A1, fill_opacity="0.85")
    s.F("circle", cx=322, cy=256, r=140, fill=A2, fill_opacity="0.85")
    s.F("path", outline=False, d="M256 140 A140 140 0 0 1 256 372 A140 140 0 0 1 256 140Z", fill=PURPLE, fill_opacity="0.7")


@reg("tally-marks")
def _(s):
    for x in (110, 170, 230, 290):
        s.M(f"M{x} 130 V260", DARK, 22)
    s.M("M80 250 L320 140", A2, 22)
    for x in (110, 170, 230):
        s.M(f"M{x} 330 V440", DARK, 22)
    s.M("M370 130 V260 M430 130 V260", DARK, 22)


@reg("table-chart")
def _(s):
    s.F("rect", x=50, y=80, width=412, height=352, rx=24, fill=WHITE)
    s.F("rect", outline=False, x=50, y=80, width=412, height=76, rx=24, fill=A1)
    s.F("rect", outline=False, x=50, y=120, width=412, height=36, fill=A1)
    s.M("M256 80 V432 M50 232 H462 M50 332 H462", DARK, 8)
    for x, y in ((130, 280), (330, 280), (130, 380), (330, 380)):
        s.M(f"M{x - 40} {y} h80", MID, 12)


@reg("flowchart")
def _(s):
    s.F("rect", x=170, y=40, width=172, height=70, rx=35, fill=A1)
    s.T("M256 110 V150 M256 240 V282 M256 340 H390", DARK, 10)
    s.F("polygon", points="256,150 350,200 256,250 162,200", fill=A2)
    s.F("rect", x=170, y=282, width=172, height=70, rx=14, fill=A1L)
    s.F("rect", x=390, y=310, width=90, height=60, rx=14, fill=A1L)
    s.T("M256 352 V420", DARK, 10)
    s.F("rect", x=170, y=420, width=172, height=60, rx=30, fill=A1)


@reg("tree-diagram")
def _(s):
    s.T("M256 100 V160 M256 160 H130 V240 M256 160 H382 V240 M130 240 V300 M130 300 H70 V380 M130 300 H190 V380", DARK, 10)
    s.F("circle", cx=256, cy=80, r=44, fill=A1)
    s.F("circle", cx=130, cy=250, r=40, fill=A2)
    s.F("circle", cx=382, cy=250, r=40, fill=A2)
    s.F("circle", cx=70, cy=400, r=34, fill=A1L)
    s.F("circle", cx=190, cy=400, r=34, fill=A1L)


@reg("growth-chart")
def _(s):
    s.T("M70 60 V440 H450", DARK, 14)
    for i, h in enumerate((70, 120, 190, 280)):
        s.F("rect", x=110 + i * 82, y=420 - h, width=56, height=h, rx=8, fill=A1)
    s.T("M110 300 C200 290 280 220 410 100", A2, 18)
    s.F("polygon", points="440,80 380,92 420,140", fill=A2)


# ================================================================ probability (keep)
def pips(s, x, y, size, n, color=INK):
    k = size / 4
    pos = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
           5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
    for dx, dy in pos:
        s.raw(f'<circle cx="{x + dx * k:.0f}" cy="{y + dy * k:.0f}" r="{size / 11:.0f}" fill="{color}"/>')


@reg("dice")
def _(s):
    s.F("rect", x=70, y=70, width=372, height=372, rx=64, fill=WHITE)
    s.F("rect", outline=False, x=96, y=96, width=320, height=60, rx=28, fill=GREY, fill_opacity="0.4")
    pips(s, 256, 256, 280, 5)


@reg("pair-of-dice")
def _(s):
    s.open(transform="rotate(-12 150 300)")
    s.F("rect", x=50, y=190, width=200, height=200, rx=40, fill=RED)
    pips(s, 150, 290, 150, 4, WHITE)
    s.close()
    s.open(transform="rotate(14 360 200)")
    s.F("rect", x=270, y=110, width=200, height=200, rx=40, fill=WHITE)
    pips(s, 370, 210, 150, 6)
    s.close()


@reg("coin-toss")
def _(s):
    s.F("circle", cx=256, cy=230, r=150, fill=GOLD)
    s.F("circle", outline=False, cx=256, cy=230, r=112, fill="#F5C14A")
    txt(s, "H", 256, 230, 80, 110, "#B97C12")
    s.M("M60 420 C140 460 380 460 452 420", MID, 10)
    s.F("polygon", points=star_pts(430, 90, 28, 12, 4), fill=YEL)


@reg("spinner")
def _(s):
    cols = [RED, A1, YEL, GREEN, A2, PURPLE]
    for i, c in enumerate(cols):
        x0, y0 = arc_pt(256, 256, 190, -90 + i * 60)
        x1, y1 = arc_pt(256, 256, 190, -30 + i * 60)
        s.raw(f'<path d="M256 256 L{x0:.0f} {y0:.0f} A190 190 0 0 1 {x1:.0f} {y1:.0f}Z" fill="{c}"/>')
    s.raw(f'<circle cx="256" cy="256" r="190" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    s.open("part-wheel", "256 256")
    s.F("path", d="M256 256 L220 150 L256 60 L292 150Z", fill=WHITE)
    s.close()
    s.F("circle", cx=256, cy=256, r=26, fill=DARK)


@reg("playing-cards-odds")
def _(s):
    s.open(transform="rotate(-14 200 270)")
    s.F("rect", x=100, y=100, width=190, height=290, rx=24, fill=WHITE)
    txt(s, "A", 150, 160, 40, 50, RED)
    s.F("path", d="M195 330 C150 290 140 260 160 245 C175 235 190 245 195 255 C200 245 215 235 230 245 C250 260 240 290 195 330Z", fill=RED)
    s.close()
    s.open(transform="rotate(12 330 260)")
    s.F("rect", x=230, y=110, width=190, height=290, rx=24, fill=WHITE)
    txt(s, "K", 280, 170, 40, 50, DARK)
    s.F("path", d="M325 330 L290 290 L325 250 L360 290Z", fill=DARK)
    s.close()


@reg("probability-scale")
def _(s):
    for i, c in enumerate((RED, ORANGE, YEL, "#B8D84A", GREEN)):
        s.F("rect", outline=False, x=50 + i * 82.4, y=200, width=84, height=80, fill=c)
    s.raw(f'<rect x="50" y="200" width="412" height="80" rx="40" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    txt(s, "0", 70, 360, 36, 60, DARK)
    txt(s, "1", 442, 360, 30, 60, DARK)
    txt(s, "½", 256, 360, 50, 60, DARK)
    s.F("polygon", points="256,190 230,150 282,150", fill=DARK)


@reg("random-draw")
def _(s):
    s.F("path", d="M110 200 C60 330 90 450 256 450 C422 450 452 330 402 200 C350 230 160 230 110 200Z", fill=A2)
    s.F("path", d="M110 200 C150 160 360 160 402 200 C350 230 160 230 110 200Z", fill=C["tan"])
    for x, y, c in ((190, 360, RED), (256, 390, A1), (330, 350, GREEN), (250, 320, YEL)):
        s.F("circle", cx=x, cy=y, r=32, fill=c)
    s.F("circle", cx=256, cy=120, r=46, fill=A1)
    s.M("M256 175 V210", DARK, 10)
    txt(s, "?", 256, 120, 40, 60, WHITE)


# ================================================================ measurement (themed)
@reg("measuring-tape")
def _(s):
    s.F("circle", cx=230, cy=256, r=180, fill=A2)
    s.F("circle", outline=False, cx=230, cy=256, r=130, fill="#F9B57A")
    s.F("circle", cx=230, cy=256, r=60, fill=WHITE)
    s.F("rect", x=270, y=320, width=210, height=64, rx=10, fill=YEL)
    for i in range(7):
        s.M(f"M{300 + i * 26} 320 v{30 if i % 2 == 0 else 18}", DARK, 6)
    s.F("rect", x=450, y=320, width=40, height=64, rx=8, fill=DGREY)


@reg("weighing-scale")
def _(s):
    s.F("rect", x=60, y=130, width=392, height=300, rx=48, fill=A1)
    s.F("rect", outline=False, x=84, y=154, width=344, height=70, rx=26, fill=A1L, fill_opacity="0.5")
    s.F("path", d="M150 200 A106 106 0 0 1 362 200Z", fill=WHITE)
    s.M("M256 200 L300 142", RED, 10)
    s.F("circle", cx=256, cy=200, r=14, fill=DARK)
    s.F("rect", x=130, y=300, width=252, height=90, rx=30, fill=A1D)


@reg("kitchen-scale")
def _(s):
    s.F("path", d="M60 360 L100 240 H412 L452 360 V420 C452 440 440 450 420 450 H92 C72 450 60 440 60 420Z", fill=A2)
    s.F("rect", x=170, y=150, width=172, height=70, rx=14, fill="#1F2A35")
    s.M("M190 186 H320", "#9BE0A8", 8)
    s.F("path", d="M110 150 C110 90 400 90 400 150Z", fill=GREY)
    s.F("rect", outline=False, x=130, y=330, width=80, height=40, rx=10, fill="#F9B57A")
    s.F("circle", outline=False, cx=400, cy=350, r=14, fill=WHITE)


@reg("measuring-jug")
def _(s):
    s.F("path", d="M110 90 H350 L330 430 C328 448 316 456 300 456 H160 C144 456 132 448 130 430Z", fill=GLASS)
    s.F("path", outline=False, d="M120 250 H342 L330 430 C328 446 316 450 300 450 H160 C144 450 132 446 130 430Z", fill=A1L)
    s.T("M350 120 C440 110 450 250 340 280", GLASS, 28)
    for i in range(6):
        s.M(f"M262 {130 + i * 54} h{44 if i % 2 == 0 else 30}", DGREY, 6)
    s.F("path", d="M110 90 L70 70 L120 110Z", fill=GLASS)


@reg("thermometer-measure")
def _(s):
    s.F("rect", x=206, y=40, width=76, height=340, rx=38, fill=GLASS)
    s.F("circle", cx=244, cy=420, r=58, fill=RED)
    s.F("rect", outline=False, x=230, y=150, width=28, height=270, rx=14, fill=RED)
    for i, y in enumerate(range(80, 340, 26)):
        s.M(f"M300 {y} h{34 if i % 2 == 0 else 22}", DGREY, 8)
    txt(s, "°C", 400, 100, 100, 60, A1)


@reg("length-units")
def _(s):
    s.F("rect", x=50, y=190, width=412, height=130, rx=20, fill=A2)
    for i in range(0, 15):
        s.M(f"M{76 + i * 26} 190 v{44 if i % 5 == 0 else 28}", DARK, 6)
    txt(s, "cm", 256, 276, 130, 56, WHITE)
    txt(s, "m", 256, 400, 60, 60, A1)


@reg("weight-units")
def _(s):
    s.F("path", d="M90 440 L150 190 H362 L422 440Z", fill=DGREY)
    s.F("path", outline=False, d="M120 420 L162 210 H230 L196 420Z", fill=WHITE, fill_opacity="0.18")
    s.T("M200 190 C190 90 322 90 312 190", DGREY, 26)
    txt(s, "kg", 256, 330, 190, 90, WHITE)


@reg("volume-units")
def _(s):
    s.F("path", d="M200 50 H312 V120 C380 150 410 200 410 270 V420 C410 450 390 466 364 466 H148 C122 466 102 450 102 420 V270 C102 200 132 150 200 120Z", fill=GLASS)
    s.F("path", outline=False, d="M112 270 H400 V420 C400 444 384 458 364 458 H148 C128 458 112 444 112 420Z", fill=A1L)
    s.F("rect", x=190, y=30, width=132, height=40, rx=12, fill=A1)
    txt(s, "L", 256, 360, 90, 110, WHITE)


@reg("metric-system")
def _(s):
    for i, (t, c) in enumerate((("m", A1), ("kg", A2), ("L", A1D))):
        s.F("rect", x=40, y=80 + i * 130, width=432, height=110, rx=36, fill=c)
        txt(s, t, 256, 135 + i * 130, 120 if len(t) > 1 else 50, 70)


@reg("imperial-units")
def _(s):
    for i, (t, c) in enumerate((("ft", A2), ("lb", A1), ("gal", A2))):
        s.F("rect", x=40, y=80 + i * 130, width=432, height=110, rx=36, fill=c)
        txt(s, t, 256, 135 + i * 130, 120 if len(t) > 2 else 90, 70)


if __name__ == "__main__":
    run("math", D, sys.argv[1:] or None)
