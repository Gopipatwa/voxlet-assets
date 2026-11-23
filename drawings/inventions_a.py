"""inventions-discoveries, part A: ancient, middle-age and modern inventions (natural colours).
Run: python drawings/inventions_a.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tech import (INK, arc_pt, head, registry, run, star_pts, txt)  # noqa: E402
from draw_lib import C  # noqa: E402

D, reg = registry()
WHITE, GREY, DGREY, BLACK = C["white"], C["grey"], C["darkgrey"], C["black"]
RED, DRED, ORANGE, YEL, GOLD, DGOLD = C["red"], C["darkred"], C["orange"], C["yellow"], C["gold"], C["darkgold"]
GREEN, DGREEN, SKY, BLUE, DBLUE, NAVY, PURPLE, PINK = C["green"], C["darkgreen"], C["sky"], C["blue"], C["darkblue"], C["navy"], C["purple"], C["pink"]
TAN, CREAM, SKIN, BROWN, DBROWN = C["tan"], C["cream"], C["skin"], C["brown"], C["darkbrown"]
GLASS = "#E3F3FC"
IRON = "#8A8F9B"
BRASS = "#D9A520"


def spokes(s, cx, cy, r, n=8, color=DBROWN, w=14):
    for i in range(n):
        x, y = arc_pt(cx, cy, r, i * 360 / n)
        s.T(f"M{cx} {cy} L{x:.0f} {y:.0f}", color, w)


def wheel(s, cx, cy, r, rim=BROWN, hub=DBROWN, n=6):
    s.F("circle", cx=cx, cy=cy, r=r, fill=TAN)
    spokes(s, cx, cy, r - 10, n, rim, 14)
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r - 8}" fill="none" stroke="{rim}" stroke-width="20"/>')
    s.F("circle", cx=cx, cy=cy, r=r * 0.18, fill=hub)


def flame(s, x, y, k=1.0):
    s.open(transform=f"translate({x} {y}) scale({k})")
    s.F("path", d="M0 -90 C30 -40 56 -20 50 20 C46 46 26 56 0 56 C-26 56 -46 46 -50 20 C-56 -20 -30 -40 0 -90Z", fill=ORANGE)
    s.F("path", outline=False, d="M0 -30 C16 0 28 10 24 30 C20 46 10 50 0 50 C-10 50 -20 46 -24 30 C-28 10 -16 0 0 -30Z", fill=YEL)
    s.close()


def bolt(s, cx, cy, k=1.0, color=YEL):
    pts = [(30, -150), (-70, 20), (-6, 20), (-34, 150), (76, -40), (6, -40), (60, -150)]
    s.F("polygon", points=" ".join(f"{cx + x * k:.0f},{cy + y * k:.0f}" for x, y in pts), fill=color)


def glass_lens(s, cx, cy, r, ring=BRASS):
    s.F("circle", cx=cx, cy=cy, r=r, fill="#CFEBFB")
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ring}" stroke-width="16"/>')


# ================================================================ ancient-inventions
@reg("invention-of-the-wheel")
def _(s):
    s.open("part-wheel", "256 256")
    wheel(s, 256, 256, 190)
    s.close()


@reg("invention-of-writing")
def _(s):
    s.F("path", d="M110 90 H400 C420 90 430 100 430 120 V380 C430 410 410 430 380 430 H130 C100 430 82 410 82 380 V120 C82 100 92 90 110 90Z", fill=C["tan"])
    for r in range(5):
        for c in range(6):
            x, y = 130 + c * 46, 140 + r * 56
            s.M(f"M{x} {y} l16 -12 M{x} {y} l16 12 M{x + 10} {y} h24" if (r + c) % 2 else f"M{x} {y - 12} v24 M{x + 16} {y - 12} l14 12 l-14 12", DBROWN, 8)
    s.T("M400 440 L470 340", BROWN, 16)
    s.F("polygon", points="470,340 486,316 454,326", fill=DBROWN)


@reg("invention-of-paper")
def _(s):
    s.F("path", d="M110 150 C90 150 80 170 90 190 L130 400 C134 420 148 430 166 430 H370 C390 430 402 416 400 396 L380 170 C378 156 366 150 350 150Z", fill=CREAM)
    s.M("M150 230 H340 M156 280 H330 M162 330 H320", TAN, 10)
    s.F("path", d="M330 150 C330 110 420 100 450 130 C470 150 440 190 400 190 C370 190 330 190 330 150Z", fill=WHITE)
    s.F("path", d="M70 440 C90 410 130 400 190 410", fill="none", stroke=GREEN, stroke_width="14", stroke_linecap="round")
    s.F("path", d="M60 440 C60 400 100 390 120 400", fill="none", stroke=DGREEN, stroke_width="12", stroke_linecap="round")


@reg("invention-of-the-plough")
def _(s):
    s.F("rect", x=20, y=420, width=472, height=40, rx=14, fill=BROWN)
    s.T("M60 420 C140 410 200 420 290 410", DBROWN, 8)
    s.T("M90 120 L200 330 L330 330", DBROWN, 24)
    s.T("M330 330 L440 190", DBROWN, 24)
    s.T("M120 150 L90 110", DBROWN, 24)
    s.F("path", d="M190 330 L330 330 L360 410 L180 410Z", fill=IRON)
    s.T("M440 190 L470 160", DBROWN, 18)
    s.F("path", d="M60 440 C100 420 150 430 190 420", fill="none")


@reg("pottery-wheel")
def _(s):
    s.F("path", d="M130 330 H382 L350 440 H162Z", fill=BROWN)
    s.open("part-wheel", "256 330")
    s.F("ellipse", cx=256, cy=330, rx=150, ry=34, fill=TAN)
    s.close()
    s.F("path", d="M200 330 C170 280 190 230 220 210 C190 180 200 140 256 140 C312 140 322 180 292 210 C322 230 342 280 312 330 C290 345 222 345 200 330Z", fill=C["orange"])
    s.F("path", outline=False, d="M210 300 C200 270 212 240 228 222", fill="none", stroke="#F9B57A", stroke_width="14", stroke_linecap="round")
    s.F("ellipse", cx=256, cy=146, rx=44, ry=12, fill=DBROWN)


@reg("sundial-invention")
def _(s):
    s.F("ellipse", cx=256, cy=330, rx=200, ry=90, fill=GREY)
    s.F("ellipse", outline=False, cx=256, cy=330, rx=160, ry=66, fill=WHITE)
    for a in range(0, 360, 30):
        x, y = arc_pt(256, 330, 150, a)
        s.M(f"M{x * 0.95 + 256 * 0.05:.0f} {330 + (y - 330) * 0.7:.0f} l0 0", DGREY, 6)
    for a in range(20, 360, 40):
        x, y = arc_pt(256, 330, 140, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{330 + (y - 330) * 0.45:.0f}", r=7, fill=DGREY)
    s.F("polygon", points="256,330 256,330 330,290 330,150", fill=GOLD)
    s.F("polygon", points="256,330 330,290 300,340", fill=DGOLD)
    s.F("ellipse", outline=False, cx=370, cy=360, rx=90, ry=16, fill=DGREY, fill_opacity="0.35")


@reg("abacus-invention")
def _(s):
    s.F("rect", x=50, y=70, width=412, height=372, rx=26, fill=BROWN)
    s.F("rect", outline=False, x=76, y=96, width=360, height=320, rx=12, fill=CREAM)
    for i, y in enumerate((140, 210, 280, 350)):
        s.T(f"M86 {y} H426", DBROWN, 8)
        for j in range(5):
            s.F("circle", cx=120 + j * 44 + (i % 2) * 100, cy=y, r=24, fill=(RED, BLUE, GREEN, ORANGE)[i])


@reg("irrigation-canals-invention")
def _(s):
    s.F("rect", x=30, y=90, width=452, height=340, rx=26, fill=GREEN)
    s.F("path", d="M30 250 C120 220 170 290 250 260 S400 230 482 260 V310 C400 290 340 330 250 320 S120 270 30 300Z", fill=SKY)
    s.T("M250 90 V260", SKY, 36)
    s.T("M120 270 V430 M390 250 V430", SKY, 36)
    for x in (110, 170, 330, 440):
        s.F("path", d=f"M{x} 150 C{x - 20} 120 {x - 4} 118 {x} 134 C{x + 4} 118 {x + 20} 120 {x} 150Z", fill=DGREEN)


@reg("glass-making")
def _(s):
    s.F("path", d="M60 440 V220 C60 160 130 130 180 130 H230 V440Z", fill=IRON)
    s.F("rect", outline=False, x=96, y=290, width=90, height=90, rx=14, fill=DGREY)
    flame(s, 140, 350, 0.5)
    s.F("path", d="M300 440 V300 C300 260 330 230 360 230 C390 230 420 260 420 300 V440Z", fill=GLASS)
    s.F("rect", x=336, y=140, width=48, height=100, rx=10, fill=GLASS)
    s.F("rect", x=330, y=120, width=60, height=26, rx=8, fill=GLASS)
    s.F("path", outline=False, d="M310 320 H410 V430 H310Z", fill=SKY, fill_opacity="0.5")
    s.T("M240 190 L290 160", DBROWN, 10)


@reg("iron-smelting")
def _(s):
    s.F("path", d="M110 450 L150 140 H362 L402 450Z", fill=BROWN)
    s.F("ellipse", cx=256, cy=140, rx=106, ry=26, fill=DBROWN)
    s.F("ellipse", outline=False, cx=256, cy=142, rx=76, ry=14, fill=ORANGE)
    s.F("path", d="M210 450 V360 C210 320 302 320 302 360 V450Z", fill=ORANGE)
    s.F("path", outline=False, d="M230 450 V380 C230 356 282 356 282 380 V450Z", fill=YEL)
    s.F("path", d="M190 100 C180 70 230 60 220 20 C260 50 270 90 250 120Z", fill=GREY, fill_opacity="0.9")
    s.F("rect", x=360, y=360, width=110, height=40, rx=10, fill=IRON)


@reg("coins-invention")
def _(s):
    for x, y, r in ((160, 340, 90), (330, 330, 80), (250, 190, 100)):
        s.F("circle", cx=x, cy=y, r=r, fill=GOLD)
        s.raw(f'<circle cx="{x}" cy="{y}" r="{r * 0.72:.0f}" fill="none" stroke="{DGOLD}" stroke-width="8"/>')
        s.F("polygon", points=star_pts(x, y, r * 0.4, r * 0.17, 5), fill=DGOLD)
        s.F("circle", outline=False, cx=x - r * 0.45, cy=y - r * 0.45, r=r * 0.14, fill=WHITE, fill_opacity="0.6")


@reg("water-mill")
def _(s):
    s.F("rect", x=40, y=420, width=432, height=40, rx=14, fill=SKY)
    s.F("path", d="M60 400 V230 L180 140 L300 230 V400Z", fill=CREAM)
    s.F("path", d="M40 235 L180 120 L320 235Z", fill=RED)
    s.F("rect", x=140, y=290, width=70, height=110, rx=10, fill=BROWN)
    s.open("part-wheel", "380 330")
    s.F("circle", cx=380, cy=330, r=100, fill=TAN)
    spokes(s, 380, 330, 92, 8, DBROWN, 12)
    s.raw(f'<circle cx="380" cy="330" r="92" fill="none" stroke="{BROWN}" stroke-width="14"/>')
    for a in range(0, 360, 45):
        x, y = arc_pt(380, 330, 100, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=12, fill=DBROWN)
    s.F("circle", cx=380, cy=330, r=18, fill=DBROWN)
    s.close()
    s.F("path", d="M320 150 C390 160 430 190 440 220 C400 220 340 200 320 150Z", fill=SKY)


@reg("gunpowder")
def _(s):
    s.F("path", d="M130 150 H382 V420 H130Z", fill=DBROWN)
    s.F("rect", x=120, y=150, width=272, height=30, rx=10, fill=BROWN)
    s.F("rect", x=120, y=390, width=272, height=30, rx=10, fill=BROWN)
    s.F("circle", cx=256, cy=285, r=44, fill=BLACK)
    s.F("polygon", points=star_pts(256, 285, 36, 16, 6), fill=ORANGE)
    s.T("M256 150 C256 100 320 90 340 50", TAN, 8)
    s.F("polygon", points=star_pts(344, 40, 22, 9, 6), fill=YEL)
    s.F("ellipse", cx=420, cy=450, rx=60, ry=18, fill=BLACK)


@reg("fireworks-invention")
def _(s):
    for x, y, r, c in ((256, 190, 120, RED), (110, 130, 56, GOLD), (410, 120, 60, BLUE), (390, 280, 44, GREEN)):
        for a in range(0, 360, 30):
            x1, y1 = arc_pt(x, y, r * 0.35, a)
            x2, y2 = arc_pt(x, y, r, a)
            s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", c, 10)
            s.F("circle", outline=False, cx=f"{x2:.0f}", cy=f"{y2:.0f}", r=9, fill=YEL)
    s.F("rect", x=232, y=400, width=48, height=80, rx=8, fill=BROWN)
    s.M("M256 400 V340", TAN, 8, dash="6 12")


@reg("magnetic-compass-invention")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=BRASS)
    s.F("circle", cx=256, cy=256, r=156, fill=CREAM)
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(256, 256, 130, a)
        x2, y2 = arc_pt(256, 256, 150, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DBROWN, 6)
    s.open("part-needle", "256 256")
    s.open(transform="rotate(40 256 256)")
    s.F("polygon", points="256,100 284,256 228,256", fill=RED)
    s.F("polygon", points="256,412 284,256 228,256", fill=WHITE)
    s.close()
    s.close()
    s.F("circle", cx=256, cy=256, r=16, fill=DGOLD)
    txt(s, "N", 256, 90, 30, 34, DBROWN)


@reg("woodblock-printing")
def _(s):
    s.F("rect", x=50, y=150, width=190, height=250, rx=14, fill=BROWN)
    s.F("rect", outline=False, x=70, y=170, width=150, height=210, rx=8, fill=TAN)
    s.M("M90 210 H200 M90 250 H180 M90 290 H200 M90 330 H160", DBROWN, 14)
    s.F("rect", x=290, y=150, width=170, height=250, rx=8, fill=CREAM)
    s.M("M310 210 H440 M310 250 H420 M310 290 H440 M310 330 H400", BLACK, 14)
    s.F("path", d="M110 120 H190 L200 150 H100Z", fill=DBROWN)
    s.T("M250 270 H278", DGREY, 10)


# ================================================================ middle-inventions
@reg("printing-press")
def _(s):
    s.F("rect", x=90, y=110, width=40, height=340, rx=10, fill=BROWN)
    s.F("rect", x=382, y=110, width=40, height=340, rx=10, fill=BROWN)
    s.F("rect", x=70, y=80, width=372, height=50, rx=14, fill=DBROWN)
    s.T("M256 130 V250", IRON, 34)
    s.T("M170 150 H342", DBROWN, 18)
    s.F("rect", x=180, y=250, width=152, height=36, rx=8, fill=IRON)
    s.F("rect", x=110, y=380, width=292, height=70, rx=14, fill=BROWN)
    s.F("rect", outline=False, x=170, y=350, width=172, height=30, rx=6, fill=CREAM)
    s.M("M190 365 H320", BLACK, 6)


@reg("mechanical-clock")
def _(s):
    s.F("rect", x=140, y=40, width=232, height=420, rx=20, fill=BROWN)
    s.F("path", d="M140 80 L256 20 L372 80Z", fill=DBROWN)
    s.F("circle", cx=256, cy=190, r=94, fill=CREAM)
    s.raw(f'<circle cx="256" cy="190" r="94" fill="none" stroke="{BRASS}" stroke-width="14"/>')
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(256, 190, 70, a)
        x2, y2 = arc_pt(256, 190, 82, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", BLACK, 6)
    s.open("part-hand-minute", "256 190")
    s.M("M256 190 V126", BLACK, 8)
    s.close()
    s.open("part-hand-hour", "256 190")
    s.M("M256 190 L300 214", BLACK, 8)
    s.close()
    s.F("circle", cx=256, cy=190, r=10, fill=RED)
    s.F("rect", outline=False, x=190, y=320, width=132, height=100, rx=12, fill=DBROWN)
    s.F("circle", cx=256, cy=370, r=34, fill=BRASS)


@reg("eyeglasses-invention")
def _(s):
    s.raw(f'<circle cx="160" cy="280" r="90" fill="#CFEBFB" stroke="{BRASS}" stroke-width="20"/>')
    s.raw(f'<circle cx="352" cy="280" r="90" fill="#CFEBFB" stroke="{BRASS}" stroke-width="20"/>')
    s.T("M250 260 C256 230 256 230 262 260", BRASS, 16)
    s.M("M120 240 C150 220 170 220 190 232", WHITE, 10)


@reg("first-telescope")
def _(s):
    s.T("M120 160 L400 250", BROWN, 54)
    s.F("rect", x=60, y=110, width=100, height=96, rx=10, fill=BRASS, transform="rotate(18 110 158)")
    s.F("rect", x=360, y=216, width=76, height=80, rx=10, fill=BRASS, transform="rotate(18 398 256)")
    s.T("M250 250 L190 440 M250 250 L330 440 M250 250 L256 450", DBROWN, 16)


@reg("first-microscope")
def _(s):
    s.F("path", d="M110 450 H390 V410 H320 C380 390 400 320 380 250 C360 190 310 170 280 180 L292 220 C320 220 340 260 330 310 C320 370 280 390 240 390 H110Z", fill=BRASS)
    s.open(transform="rotate(-20 220 180)")
    s.F("rect", x=170, y=50, width=100, height=150, rx=14, fill=DBROWN)
    s.F("rect", x=190, y=200, width=60, height=60, rx=8, fill=BRASS)
    s.close()
    s.F("rect", x=130, y=330, width=170, height=30, rx=10, fill=BROWN)


@reg("pendulum-clock-invention")
def _(s):
    s.F("rect", x=170, y=40, width=172, height=430, rx=22, fill=BROWN)
    s.F("path", d="M160 80 L256 20 L352 80Z", fill=DBROWN)
    s.F("circle", cx=256, cy=140, r=60, fill=CREAM)
    s.raw(f'<circle cx="256" cy="140" r="60" fill="none" stroke="{BRASS}" stroke-width="10"/>')
    s.M("M256 140 V100 M256 140 L284 154", BLACK, 7)
    s.F("rect", outline=False, x=198, y=230, width=116, height=200, rx=12, fill=DBROWN)
    s.open("part-pendulum", "256 240")
    s.M("M256 240 V380", GOLD, 8)
    s.F("circle", cx=256, cy=390, r=30, fill=BRASS)
    s.close()


@reg("barometer-invention")
def _(s):
    s.F("circle", cx=256, cy=256, r=196, fill=BRASS)
    s.F("circle", cx=256, cy=256, r=156, fill=CREAM)
    for a in range(135, 406, 30):
        x1, y1 = arc_pt(256, 256, 120, a)
        x2, y2 = arc_pt(256, 256, 144, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", BLACK, 6)
    s.M("M256 256 L330 190", RED, 12)
    s.F("circle", cx=256, cy=256, r=16, fill=DBROWN)
    txt(s, "Hg", 256, 340, 70, 40, DBROWN)


@reg("thermometer-invention")
def _(s):
    s.F("rect", x=214, y=40, width=84, height=330, rx=42, fill=GLASS)
    s.F("circle", cx=256, cy=420, r=62, fill=RED)
    s.F("rect", outline=False, x=240, y=130, width=32, height=300, rx=16, fill=RED)
    for i, y in enumerate(range(80, 340, 26)):
        s.M(f"M320 {y} h{34 if i % 2 == 0 else 22}", DGREY, 8)
    s.F("rect", outline=False, x=226, y=60, width=14, height=60, rx=7, fill=WHITE, fill_opacity="0.7")


@reg("steam-engine")
def _(s):
    s.F("rect", x=60, y=260, width=250, height=140, rx=70, fill=IRON)
    s.F("rect", outline=False, x=84, y=278, width=140, height=18, rx=9, fill=WHITE, fill_opacity="0.4")
    s.F("rect", x=130, y=170, width=44, height=100, rx=12, fill=DGREY)
    s.F("path", d="M130 170 H174 L184 150 H120Z", fill=DGREY)
    s.F("path", d="M140 120 C110 90 170 70 150 30 C200 60 200 100 164 140Z", fill=GREY)
    s.F("rect", x=300, y=300, width=70, height=60, rx=10, fill=DGREY)
    s.open("part-wheel", "400 340")
    s.F("circle", cx=400, cy=340, r=80, fill=TAN)
    spokes(s, 400, 340, 74, 8, DGREY, 10)
    s.raw(f'<circle cx="400" cy="340" r="74" fill="none" stroke="{DGREY}" stroke-width="12"/>')
    s.close()
    s.F("circle", cx=400, cy=340, r=14, fill=BLACK)
    s.F("rect", x=40, y=400, width=290, height=40, rx=12, fill=DGREY)


@reg("spinning-jenny")
def _(s):
    s.F("rect", x=60, y=330, width=392, height=40, rx=12, fill=BROWN)
    s.T("M110 370 V450 M400 370 V450", DBROWN, 22)
    for i in range(6):
        x = 100 + i * 50
        s.T(f"M{x} 330 V160", CREAM, 8)
        s.F("rect", x=x - 16, y=150, width=32, height=70, rx=8, fill=WHITE)
    s.open("part-wheel", "400 250")
    s.F("circle", cx=400, cy=250, r=60, fill=TAN)
    spokes(s, 400, 250, 54, 8, DBROWN, 8)
    s.close()
    s.T("M100 140 H350", DBROWN, 16)


@reg("hot-air-balloon-first-flight")
def _(s):
    s.F("path", d="M256 40 C130 40 80 150 120 240 C150 300 210 330 220 350 H292 C302 330 362 300 392 240 C432 150 382 40 256 40Z", fill=RED)
    s.F("path", outline=False, d="M256 40 C200 100 190 260 220 350 H292 C322 260 312 100 256 40Z", fill=YEL)
    s.F("path", outline=False, d="M150 100 C170 70 210 56 240 56", fill="none", stroke=WHITE, stroke_width="16", stroke_linecap="round", stroke_opacity="0.7")
    s.T("M226 352 L210 408 M286 352 L302 408", DBROWN, 8)
    s.F("rect", x=190, y=408, width=132, height=70, rx=12, fill=BROWN)
    s.F("rect", outline=False, x=200, y=420, width=112, height=14, rx=6, fill=TAN)


@reg("lightning-rod")
def _(s):
    s.F("rect", x=130, y=320, width=250, height=140, rx=10, fill=CREAM)
    s.F("path", d="M110 320 L256 210 L402 320Z", fill=RED)
    s.F("rect", x=234, y=370, width=44, height=90, rx=8, fill=BROWN)
    s.F("rect", x=170, y=350, width=40, height=40, rx=8, fill=SKY)
    s.T("M256 210 V80", IRON, 14)
    s.F("polygon", points="256,40 270,86 242,86", fill=IRON)
    bolt(s, 380, 130, 0.5, YEL)
    s.T("M256 210 V300", IRON, 6)
    s.F("path", d="M60 120 C30 120 20 170 60 180 H150 C190 180 190 130 150 120 C140 80 100 80 80 110Z", fill=GREY)


@reg("smallpox-vaccine")
def _(s):
    s.open(transform="rotate(-40 256 256)")
    s.F("rect", x=130, y=210, width=230, height=92, rx=12, fill=GLASS)
    s.F("rect", outline=False, x=140, y=220, width=130, height=72, fill=SKY)
    s.F("rect", x=360, y=236, width=40, height=40, fill=GREY)
    s.T("M400 256 H490", GREY, 6)
    s.F("rect", x=70, y=196, width=60, height=120, rx=8, fill=GREY)
    s.T("M30 256 H70", GREY, 16)
    s.close()
    s.F("path", d="M370 330 C400 330 430 350 430 380 V450 H350 V380 C350 350 340 330 370 330Z", fill=GLASS)
    s.F("rect", x=360, y=312, width=60, height=28, rx=8, fill=RED)
    s.F("rect", outline=False, x=360, y=390, width=60, height=50, fill=SKY)


# ================================================================ modern-inventions
@reg("battery-invention")
def _(s):
    for i in range(5):
        y = 410 - i * 66
        s.F("ellipse", cx=256, cy=y, rx=120, ry=30, fill=GOLD if i % 2 == 0 else IRON)
        s.F("rect", outline=False, x=136, y=y - 8, width=240, height=30, fill=GOLD if i % 2 == 0 else IRON)
        s.F("ellipse", outline=False, cx=256, cy=y - 8, rx=120, ry=28, fill=GOLD if i % 2 == 0 else IRON)
    s.T("M256 100 V50 M256 50 H400 V400 H380", DBROWN, 10)
    bolt(s, 420, 140, 0.3, YEL)


@reg("electric-motor-invention")
def _(s):
    s.F("rect", x=100, y=160, width=300, height=220, rx=60, fill=BLUE)
    s.F("rect", outline=False, x=124, y=180, width=160, height=26, rx=12, fill=WHITE, fill_opacity="0.4")
    s.F("rect", x=400, y=240, width=70, height=60, rx=8, fill=IRON)
    s.open("part-wheel", "250 270")
    s.F("circle", cx=250, cy=270, r=70, fill=GOLD)
    for a in (0, 90, 180, 270):
        x, y = arc_pt(250, 270, 38, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=12, fill=DGOLD)
    s.close()
    s.F("circle", cx=250, cy=270, r=16, fill=BLACK)
    s.F("rect", x=120, y=380, width=260, height=36, rx=10, fill=DGREY)
    bolt(s, 120, 110, 0.3, YEL)


@reg("invention-of-photography")
def _(s):
    s.F("rect", x=100, y=150, width=312, height=250, rx=14, fill=BROWN)
    s.F("path", d="M170 150 L200 90 H312 L342 150Z", fill=DBROWN)
    s.F("circle", cx=256, cy=270, r=84, fill=DGOLD)
    s.F("circle", cx=256, cy=270, r=60, fill=BLACK)
    s.F("circle", cx=256, cy=270, r=40, fill=BLUE)
    s.F("circle", outline=False, cx=240, cy=252, r=12, fill=WHITE, fill_opacity="0.7")
    s.F("rect", x=100, y=400, width=312, height=40, rx=10, fill=DBROWN)
    s.T("M120 440 L90 480 M392 440 L422 480", DBROWN, 14)


@reg("light-bulb")
def _(s):
    s.F("path", d="M256 40 C150 40 110 130 140 210 C158 258 196 280 196 320 H316 C316 280 354 258 372 210 C402 130 362 40 256 40Z", fill="#FFF3B0")
    s.F("path", outline=False, d="M180 120 C200 84 236 74 262 76", fill="none", stroke=WHITE, stroke_width="18", stroke_linecap="round", stroke_opacity="0.9")
    s.M("M226 320 V250 L256 220 L286 250 V320", ORANGE, 8)
    s.F("rect", x=190, y=320, width=132, height=36, rx=10, fill=GREY)
    s.F("rect", x=198, y=356, width=116, height=36, rx=10, fill=GREY)
    s.F("rect", x=214, y=392, width=84, height=50, rx=18, fill=DGREY)
    for a in (-60, -30, 0, 30, 60):
        x1, y1 = arc_pt(256, 160, 140, -90 + a)
        x2, y2 = arc_pt(256, 160, 180, -90 + a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", YEL, 10)


@reg("telephone-invention")
def _(s):
    s.F("ellipse", cx=256, cy=450, rx=130, ry=30, fill=BLACK)
    s.T("M256 450 V150", BLACK, 34)
    s.F("path", d="M170 60 L342 60 L296 150 L216 150Z", fill=BLACK)
    s.F("ellipse", outline=False, cx=256, cy=62, rx=82, ry=14, fill=DGREY)
    s.T("M296 250 C380 250 410 300 400 330", DGREY, 8)
    s.F("rect", x=372, y=290, width=56, height=140, rx=24, fill=BLACK)
    s.F("circle", cx=400, cy=290, r=34, fill=BLACK)
    s.F("circle", cx=400, cy=438, r=34, fill=BLACK)
    s.F("circle", cx=256, cy=250, r=26, fill=BRASS)
    s.F("circle", outline=False, cx=256, cy=250, r=10, fill=DGOLD)


@reg("telegraph")
def _(s):
    s.F("rect", x=60, y=330, width=392, height=100, rx=20, fill=BROWN)
    s.T("M130 330 V290 M382 330 V290", BRASS, 14)
    s.T("M120 290 H300", BRASS, 18)
    s.F("circle", cx=330, cy=290, r=26, fill=BLACK)
    s.F("rect", x=190, y=380, width=130, height=14, rx=6, fill=DBROWN)
    s.M("M140 262 L140 230", BRASS, 10)
    s.F("circle", cx=380, cy=380, r=14, fill=BRASS)
    s.F("circle", cx=110, cy=380, r=14, fill=BRASS)


@reg("gramophone")
def _(s):
    s.F("rect", x=70, y=330, width=300, height=110, rx=14, fill=BROWN)
    s.F("ellipse", cx=220, cy=330, rx=130, ry=30, fill=BLACK)
    s.open("part-wheel", "220 330")
    s.F("ellipse", cx=220, cy=330, rx=90, ry=20, fill=DBROWN)
    s.F("ellipse", outline=False, cx=220, cy=330, rx=26, ry=7, fill=RED)
    s.close()
    s.T("M330 330 L380 220 C390 170 440 120 480 100", BRASS, 22)
    s.F("path", d="M410 80 C470 30 510 50 500 130 C480 170 430 150 410 80Z", fill=BRASS)
    s.F("path", outline=False, d="M430 80 C470 60 490 80 486 120 C460 130 440 110 430 80Z", fill=DGOLD)
    s.T("M250 300 L300 250", IRON, 10)


@reg("motor-car-invention")
def _(s):
    s.F("rect", x=100, y=250, width=300, height=90, rx=20, fill=BLACK)
    s.F("rect", x=130, y=190, width=160, height=70, rx=10, fill=BROWN)
    s.F("path", d="M290 250 V200 H370 V250Z", fill=RED)
    s.F("rect", x=120, y=170, width=190, height=20, rx=8, fill=DBROWN)
    s.open("part-wheel", "150 390")
    s.F("circle", cx=150, cy=390, r=64, fill=TAN)
    spokes(s, 150, 390, 56, 8, DBROWN, 6)
    s.raw(f'<circle cx="150" cy="390" r="58" fill="none" stroke="{BLACK}" stroke-width="12"/>')
    s.close()
    s.open("part-wheel", "360 390")
    s.F("circle", cx=360, cy=390, r=64, fill=TAN)
    spokes(s, 360, 390, 56, 8, DBROWN, 6)
    s.raw(f'<circle cx="360" cy="390" r="58" fill="none" stroke="{BLACK}" stroke-width="12"/>')
    s.close()
    s.F("circle", cx=410, cy=270, r=14, fill=YEL)


@reg("bicycle-invention")
def _(s):
    s.open("part-wheel", "330 330")
    s.raw(f'<circle cx="330" cy="330" r="86" fill="none" stroke="{INK}" stroke-width="26" data-outline="under"/>')
    s.raw(f'<circle cx="330" cy="330" r="86" fill="none" stroke="{BLACK}" stroke-width="12"/>')
    spokes(s, 330, 330, 80, 10, GREY, 4)
    s.close()
    s.open("part-wheel", "150 380")
    s.raw(f'<circle cx="150" cy="380" r="40" fill="none" stroke="{INK}" stroke-width="26" data-outline="under"/>')
    s.raw(f'<circle cx="150" cy="380" r="40" fill="none" stroke="{BLACK}" stroke-width="12"/>')
    s.close()
    s.T("M150 380 L220 150 L320 150 M330 330 L300 150 M200 150 H300", RED, 18)
    s.T("M300 150 L280 100 H320 M170 100 H250", BLACK, 14)
    s.F("circle", cx=330, cy=330, r=14, fill=GOLD)


@reg("aeroplane-invention")
def _(s):
    s.F("path", d="M110 240 H400 C430 240 430 290 400 290 H110Z", fill=RED)
    s.F("rect", x=70, y=170, width=372, height=30, rx=14, fill=TAN)
    s.F("rect", x=60, y=320, width=392, height=30, rx=14, fill=TAN)
    s.T("M150 200 V320 M360 200 V320", DBROWN, 10)
    s.F("circle", cx=440, cy=265, r=26, fill=DBROWN)
    s.M("M440 215 V315", GREY, 10)
    s.F("path", d="M80 260 L40 200 V270Z", fill=RED)
    s.F("circle", cx=200, cy=380, r=22, fill=BLACK)
    s.T("M200 290 V360", DBROWN, 10)


@reg("radio-invention")
def _(s):
    s.F("rect", x=60, y=130, width=392, height=290, rx=36, fill=BROWN)
    s.F("rect", outline=False, x=84, y=154, width=190, height=242, rx=18, fill=CREAM)
    for i in range(5):
        s.M(f"M100 {190 + i * 40} H258", TAN, 10)
    s.F("circle", cx=360, cy=210, r=56, fill=BRASS)
    s.F("circle", cx=360, cy=210, r=30, fill=DBROWN)
    s.M("M360 210 L376 186", WHITE, 8)
    s.F("circle", cx=360, cy=350, r=34, fill=BRASS)
    s.T("M200 130 L160 40", IRON, 10)


@reg("television-invention")
def _(s):
    s.F("rect", x=50, y=100, width=412, height=320, rx=40, fill=BROWN)
    s.F("rect", x=80, y=130, width=290, height=260, rx=44, fill=DGREY)
    s.F("rect", outline=False, x=96, y=146, width=258, height=228, rx=34, fill="#BFD8C8")
    s.F("path", outline=False, d="M120 180 C140 160 200 156 230 160", fill="none", stroke=WHITE, stroke_width="16", stroke_linecap="round", stroke_opacity="0.8")
    s.F("circle", cx=416, cy=210, r=22, fill=BLACK)
    s.F("circle", cx=416, cy=290, r=22, fill=BLACK)
    s.T("M230 100 L150 40 M280 100 L360 40", IRON, 8)


@reg("refrigerator-invention")
def _(s):
    s.F("rect", x=130, y=40, width=252, height=430, rx=30, fill=WHITE)
    s.F("rect", outline=False, x=146, y=56, width=40, height=400, rx=14, fill=SKY, fill_opacity="0.4")
    s.M("M130 190 H382", GREY, 10)
    s.F("rect", x=340, y=90, width=14, height=70, rx=7, fill=DGREY)
    s.F("rect", x=340, y=230, width=14, height=120, rx=7, fill=DGREY)
    s.M("M190 110 l24 24 m-24 0 l24 -24", SKY, 10)


@reg("sewing-machine")
def _(s):
    s.F("path", d="M60 400 H452 V340 H380 V190 C380 130 320 110 270 110 H150 C110 110 90 140 90 180 V250 H130 V340 H60Z", fill=BLACK)
    s.F("path", outline=False, d="M110 190 C110 160 130 140 160 140 H260 C300 140 340 150 350 190Z", fill=DGREY)
    s.F("circle", cx=330, cy=240, r=42, fill=GOLD)
    s.F("circle", outline=False, cx=330, cy=240, r=18, fill=DGOLD)
    s.T("M130 250 V320", IRON, 14)
    s.F("polygon", points="120,320 140,320 130,350", fill=IRON)
    s.F("rect", x=60, y=400, width=392, height=40, rx=12, fill=DGREY)
    s.F("rect", x=170, y=340, width=130, height=60, rx=6, fill=CREAM)


@reg("typewriter")
def _(s):
    s.F("rect", x=100, y=320, width=312, height=110, rx=20, fill=BLACK)
    for r in range(3):
        for c in range(8):
            s.F("circle", cx=130 + c * 36 + (r % 2) * 14, cy=340 + r * 26, r=11, fill=WHITE)
    s.F("rect", x=90, y=200, width=332, height=124, rx=18, fill=DGREY)
    s.F("rect", x=140, y=70, width=232, height=140, rx=6, fill=CREAM)
    s.M("M160 110 H350 M160 140 H330 M160 170 H300", DGREY, 8)
    s.T("M70 190 H442", DGOLD, 14)
    s.F("circle", cx=60, cy=190, r=20, fill=BRASS)
    s.F("circle", cx=452, cy=190, r=20, fill=BRASS)


@reg("cinema-projector")
def _(s):
    s.F("rect", x=210, y=240, width=130, height=100, rx=14, fill=DGREY)
    s.F("circle", cx=250, cy=170, r=70, fill=IRON)
    s.F("circle", cx=380, cy=170, r=60, fill=IRON)
    for x, y, r in ((250, 170, 70), (380, 170, 60)):
        s.F("circle", outline=False, cx=x, cy=y, r=r * 0.55, fill=DGREY)
    s.open("part-wheel", "250 170")
    s.M("M250 130 V210 M210 170 H290", BLACK, 8)
    s.close()
    s.F("rect", x=90, y=250, width=130, height=70, rx=10, fill=BLACK)
    s.F("circle", cx=90, cy=285, r=26, fill=BRASS)
    s.F("polygon", outline=False, points="70,270 20,200 20,370 70,300", fill=YEL, fill_opacity="0.6")
    s.T("M250 340 L210 450 M300 340 L340 450", DBROWN, 16)


@reg("x-ray-machine-invention")
def _(s):
    s.F("rect", x=60, y=80, width=170, height=150, rx=16, fill=DGREY)
    s.F("rect", outline=False, x=84, y=104, width=122, height=60, rx=10, fill=SKY)
    s.T("M145 230 L180 330", IRON, 18)
    s.F("polygon", points="100,330 260,330 230,230 130,230", fill=YEL, fill_opacity="0.55")
    s.F("rect", x=60, y=380, width=392, height=50, rx=14, fill=BLUE)
    s.F("rect", x=250, y=290, width=200, height=170, rx=18, fill=NAVY)
    for i in range(4):
        s.M(f"M{290 + i * 36} 330 V410", WHITE, 12)
    s.M("M290 370 H410", WHITE, 12)


@reg("air-conditioner-invention")
def _(s):
    s.F("rect", x=40, y=110, width=432, height=190, rx=40, fill=WHITE)
    s.F("rect", outline=False, x=60, y=130, width=392, height=34, rx=16, fill=SKY, fill_opacity="0.5")
    s.F("rect", x=60, y=230, width=392, height=40, rx=16, fill=GREY)
    for x in range(90, 440, 60):
        s.M(f"M{x} 240 V262", DGREY, 8)
    s.F("circle", outline=False, cx=420, cy=182, r=10, fill=GREEN)
    for x in (110, 220, 330, 440):
        s.M(f"M{x} 330 v50 M{x - 14} 360 l14 24 l14 -24", SKY, 12)


@reg("zip-fastener")
def _(s):
    s.F("path", d="M90 70 H215 L230 440 H110Z", fill=BLUE)
    s.F("path", d="M422 70 H297 L282 440 H402Z", fill=BLUE)
    for i in range(11):
        y = 100 + i * 32
        s.F("rect", x=200, y=y, width=40, height=22, rx=6, fill=GREY)
        s.F("rect", x=272, y=y + 16, width=40, height=22, rx=6, fill=IRON)
    s.F("path", d="M210 70 H302 L330 140 H182Z", fill=GOLD)
    s.F("rect", x=232, y=140, width=48, height=70, rx=10, fill=GOLD)
    s.F("rect", x=240, y=210, width=32, height=60, rx=14, fill=DGOLD)


@reg("jet-engine")
def _(s):
    s.F("path", d="M50 190 C50 160 100 150 140 150 H400 C450 150 470 190 470 256 C470 322 450 362 400 362 H140 C100 362 50 352 50 322Z", fill=GREY)
    s.F("ellipse", cx=90, cy=256, rx=50, ry=96, fill=DGREY)
    s.open("part-wheel", "92 256")
    for a in range(0, 360, 45):
        s.F("path", outline=False, d=f"M92 256 L{92 + 40 * math.cos(math.radians(a)):.0f} {256 + 88 * math.sin(math.radians(a)):.0f}", fill="none", stroke=IRON, stroke_width="12", stroke_linecap="round")
    s.close()
    s.F("circle", cx=92, cy=256, r=14, fill=BLACK)
    s.F("path", d="M470 190 L500 230 V282 L470 322Z", fill=DGREY)
    s.F("rect", outline=False, x=160, y=170, width=230, height=22, rx=11, fill=WHITE, fill_opacity="0.5")
    s.F("polygon", points=star_pts(500, 256, 30, 12, 8), fill=ORANGE)


@reg("first-computer")
def _(s):
    for x in (40, 190, 340):
        s.F("rect", x=x, y=90, width=130, height=340, rx=12, fill=DGREY)
        for y in range(120, 400, 56):
            s.F("rect", outline=False, x=x + 14, y=y, width=102, height=38, rx=6, fill=BLACK)
            for k in range(4):
                s.F("circle", outline=False, cx=x + 32 + k * 24, cy=y + 19, r=7, fill=(YEL, RED, GREEN, BLUE)[k])
    s.F("circle", cx=105, cy=60, r=36, fill=IRON)
    s.F("circle", outline=False, cx=105, cy=60, r=12, fill=BLACK)
    s.F("circle", cx=255, cy=60, r=36, fill=IRON)
    s.F("circle", outline=False, cx=255, cy=60, r=12, fill=BLACK)
    s.F("rect", x=30, y=430, width=452, height=26, rx=10, fill=BLACK)


if __name__ == "__main__":
    run("inventions-discoveries", D, sys.argv[1:] or None)
