"""science drawings, part 3: magnets-electricity, light-sound-heat, biology-basics, famous-experiments.
Run: python drawings/science3.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import WHITE  # noqa: E402
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, bulb, gear, person, sparkle  # noqa: E402
from _parts import place as P  # noqa: E402
from draw_lib import C, INK, arc_pt, run, star_pts  # noqa: E402
from text_tile import text_path  # noqa: E402

D = {}
RED, DRED, GREEN, DGREEN, YEL, ORANGE, PINK, SKY, GREY, DGREY = C["red"], C["darkred"], C["green"], C["darkgreen"], C["yellow"], C["orange"], C["pink"], C["sky"], C["grey"], C["darkgrey"]
BLUE, PURPLE, BROWN, DBROWN, TAN, GOLD, CREAM = C["blue"], C["purple"], C["brown"], C["darkbrown"], C["tan"], C["gold"], C["cream"]
GLASS = "#E3F3FC"


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def ring(s, cx, cy, r, color, w):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w + 20}" data-outline="under"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>')


def ball(s, x, y, r, color):
    s.F("circle", cx=x, cy=y, r=r, fill=color)
    s.F("circle", outline=False, cx=round(x - r * 0.32, 1), cy=round(y - r * 0.32, 1), r=round(r * 0.26, 1), fill=WHITE, fill_opacity="0.55")


def arrow(s, x1, y1, x2, y2, color=RED, w=18, hl=44):
    s.T(f"M{x1} {y1} L{x2} {y2}", color, w)
    a = math.atan2(y2 - y1, x2 - x1)
    tip = (x2 + 14 * math.cos(a), y2 + 14 * math.sin(a))
    p1 = (x2 + hl * math.cos(a + math.radians(150)), y2 + hl * math.sin(a + math.radians(150)))
    p2 = (x2 + hl * math.cos(a - math.radians(150)), y2 + hl * math.sin(a - math.radians(150)))
    s.F("polygon", points=f"{tip[0]:.0f},{tip[1]:.0f} {p1[0]:.0f},{p1[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}", fill=color)


def bolt(s, cx=256, cy=256, k=1.0, color=YEL):
    pts = [(30, -150), (-70, 20), (-6, 20), (-34, 150), (76, -40), (6, -40), (60, -150)]
    s.F("polygon", points=" ".join(f"{cx + x * k:.0f},{cy + y * k:.0f}" for x, y in pts), fill=color)


def horseshoe(s, cx=256, cy=270, r=140, w=70):
    s.raw(f'<path d="M{cx - r} {cy + 100} V{cy} A{r} {r} 0 0 1 {cx + r} {cy} V{cy + 100}" fill="none" stroke="{INK}" stroke-width="{w + 20}" stroke-linecap="butt" data-outline="under"/>')
    s.raw(f'<path d="M{cx - r} {cy + 100} V{cy} A{r} {r} 0 0 1 {cx + r} {cy} V{cy + 100}" fill="none" stroke="{RED}" stroke-width="{w}" stroke-linecap="butt"/>')


def flame(s, x, y, k=1.0):
    s.open(transform=f"translate({x} {y}) scale({k})")
    s.F("path", d="M0 -90 C30 -40 56 -20 50 20 C46 46 26 56 0 56 C-26 56 -46 46 -50 20 C-56 -20 -30 -40 0 -90Z", fill=A2)
    s.F("path", outline=False, d="M0 -30 C16 0 28 10 24 30 C20 46 10 50 0 50 C-10 50 -20 46 -24 30 C-28 10 -16 0 0 -30Z", fill=YEL)
    s.close()


# ================================================================ magnets-electricity
@reg("bar-magnet")
def _(s):
    s.F("rect", x=50, y=190, width=206, height=132, rx=18, fill=RED)
    s.F("rect", x=256, y=190, width=206, height=132, rx=18, fill=A1)
    s.F("rect", outline=False, x=256, y=190, width=30, height=132, fill=A1)
    s.F("rect", outline=False, x=70, y=204, width=170, height=22, rx=10, fill=WHITE, fill_opacity="0.35")
    for ch, cx in (("N", 150), ("S", 362)):
        d, _ = text_path(ch, "black", cx, 256, 90, 80)
        s.F("path", outline=False, d=d, fill=WHITE)


@reg("horseshoe-magnet")
def _(s):
    horseshoe(s)
    s.F("rect", x=116, y=360, width=80, height=70, rx=8, fill=GREY)
    s.F("rect", x=316, y=360, width=80, height=70, rx=8, fill=GREY)


@reg("magnetic-field-lines")
def _(s):
    s.F("rect", x=170, y=200, width=86, height=112, rx=12, fill=RED)
    s.F("rect", x=256, y=200, width=86, height=112, rx=12, fill=A1)
    for k, rr in enumerate((70, 120, 168)):
        s.raw(f'<path d="M170 256 C{170 - 30} {256 - rr * 1.6} {342 + 30} {256 - rr * 1.6} 342 256" fill="none" stroke="{A2}" stroke-width="9" stroke-linecap="round"/>')
        s.raw(f'<path d="M170 256 C{170 - 30} {256 + rr * 1.6} {342 + 30} {256 + rr * 1.6} 342 256" fill="none" stroke="{A2}" stroke-width="9" stroke-linecap="round"/>')


@reg("magnetic-attraction")
def _(s):
    s.F("rect", x=40, y=210, width=110, height=92, rx=14, fill=RED)
    s.F("rect", x=150, y=210, width=0.01, height=92, fill=RED)
    s.F("rect", x=362, y=210, width=110, height=92, rx=14, fill=A1)
    arrow(s, 168, 256, 220, 256, DARK, 14, 34)
    arrow(s, 344, 256, 292, 256, DARK, 14, 34)
    s.M("M205 160 L256 120 L307 160", MID, 10)


@reg("magnetic-repulsion")
def _(s):
    s.F("rect", x=60, y=210, width=140, height=92, rx=14, fill=RED)
    s.F("rect", x=312, y=210, width=140, height=92, rx=14, fill=RED)
    arrow(s, 224, 256, 176, 256, DARK, 14, 34)
    arrow(s, 288, 256, 336, 256, DARK, 14, 34)
    s.F("polygon", points=star_pts(256, 256, 22, 8, 6), fill=YEL)


@reg("electromagnet")
def _(s):
    s.F("rect", x=130, y=190, width=252, height=132, rx=20, fill=GREY)
    for x in range(150, 370, 36):
        s.T(f"M{x} 175 C{x + 20} 220 {x + 20} 290 {x} 338", A2, 14)
    s.T("M130 250 C70 250 70 420 150 420 H362 C440 420 440 250 382 250", DGREY, 10)
    s.F("rect", x=210, y=400, width=92, height=60, rx=10, fill=GREEN)
    s.M("M240 430 H272 M256 414 V446", WHITE, 8)
    for x in (180, 256, 332):
        s.M(f"M{x} 150 V110", MID, 10)


@reg("static-electricity")
def _(s):
    s.F("circle", cx=256, cy=360, r=130, fill=PINK)
    for i, x in enumerate(range(150, 380, 35)):
        s.T(f"M{x} 250 C{x - 20 + i * 8} 200 {x + 30 - i * 10} 150 {x - 10 + i * 6} 90", PINK, 12)
    s.F("circle", outline=False, cx=210, cy=350, r=12, fill=DARK)
    s.F("circle", outline=False, cx=300, cy=350, r=12, fill=DARK)
    s.M("M220 400 C240 420 276 420 296 400", DARK, 10)
    bolt(s, 400, 130, 0.38)
    bolt(s, 110, 120, 0.3)


@reg("electric-circuit")
def _(s):
    s.T("M120 150 H392 V362 H120Z", DGREY, 16)
    s.F("rect", x=60, y=210, width=120, height=100, rx=16, fill=A1)
    s.F("rect", outline=False, x=70, y=240, width=100, height=40, fill=A1L)
    s.M("M110 260 H132 M121 249 V271 M150 260 H162", DARK, 7)
    s.F("circle", cx=392, cy=256, r=62, fill=GLASS)
    s.F("circle", outline=False, cx=392, cy=256, r=34, fill=YEL)
    s.F("rect", x=210, y=124, width=100, height=52, rx=12, fill=GREEN)


@reg("battery-cell")
def _(s):
    s.F("rect", x=220, y=36, width=72, height=50, rx=10, fill=GREY)
    s.F("rect", x=160, y=80, width=192, height=380, rx=30, fill=A2)
    s.F("rect", outline=False, x=160, y=80, width=192, height=110, rx=30, fill=GOLD)
    s.F("rect", outline=False, x=160, y=150, width=192, height=40, fill=GOLD)
    s.M("M256 270 V350 M216 310 H296", WHITE, 20)
    s.F("rect", outline=False, x=178, y=96, width=26, height=340, rx=12, fill=WHITE, fill_opacity="0.22")


@reg("light-bulb-circuit")
def _(s):
    P(s, bulb, 256, 170, 0.85)
    s.T("M222 330 V390 H130 V330 M290 330 V390 H382 V330", DGREY, 14)
    s.F("rect", x=80, y=330, width=100, height=110, rx=14, fill=A1)
    s.M("M110 385 H150 M130 365 V405", WHITE, 12)
    s.F("rect", x=340, y=346, width=84, height=60, rx=12, fill=GREY)


@reg("switch")
def _(s):
    s.T("M60 340 H170 M342 340 H452", DGREY, 16)
    s.F("circle", cx=170, cy=340, r=28, fill=GOLD)
    s.F("circle", cx=342, cy=340, r=28, fill=GOLD)
    s.T("M170 340 L330 190", GREY, 20)
    s.F("circle", cx=330, cy=190, r=26, fill=RED)
    s.M("M390 190 L420 160 M400 240 L440 240", YEL, 10)


@reg("resistor")
def _(s):
    s.T("M30 256 H110 M402 256 H482", DGREY, 16)
    s.F("rect", x=100, y=190, width=312, height=132, rx=56, fill=TAN)
    for x, c in ((170, RED), (220, PURPLE), (270, ORANGE)):
        s.F("rect", outline=False, x=x, y=192, width=26, height=128, fill=c)
    s.F("rect", outline=False, x=340, y=192, width=26, height=128, fill=GOLD)
    s.raw(f'<rect x="100" y="190" width="312" height="132" rx="56" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')


@reg("wire")
def _(s):
    s.T("M60 380 C140 380 140 140 256 140 C372 140 372 380 452 380", A2, 36)
    s.T("M60 380 H30 M452 380 H482", GREY, 20)
    s.M("M70 380 C150 380 150 150 256 150", WHITE, 8)


@reg("electric-current")
def _(s):
    s.T("M70 256 H442", DGREY, 44)
    for x in (120, 220, 320, 420):
        s.F("circle", cx=x, cy=256, r=18, fill=YEL)
    arrow(s, 100, 150, 400, 150, A1, 16, 38)
    bolt(s, 256, 380, 0.3)


@reg("series-circuit")
def _(s):
    s.T("M80 120 H432 V392 H80Z", DGREY, 14)
    s.F("rect", x=40, y=210, width=80, height=90, rx=12, fill=A1)
    for x in (190, 322):
        s.F("circle", cx=x, cy=120, r=44, fill=GLASS)
        s.F("circle", outline=False, cx=x, cy=120, r=22, fill=YEL)
    s.F("circle", cx=256, cy=392, r=38, fill=GLASS)
    s.F("circle", outline=False, cx=256, cy=392, r=18, fill=YEL)


@reg("parallel-circuit")
def _(s):
    s.T("M120 256 V110 H392 V402 H120Z M120 256 H392 M256 110 V402", DGREY, 12)
    s.F("rect", x=70, y=216, width=100, height=80, rx=12, fill=A1)
    for y in (110, 256, 402):
        s.F("circle", cx=320, cy=y, r=40, fill=GLASS)
        s.F("circle", outline=False, cx=320, cy=y, r=18, fill=YEL)


@reg("conductor-and-insulator")
def _(s):
    s.T("M40 140 H220", A2, 36)
    s.T("M40 340 H220", MID, 36)
    s.F("rect", x=250, y=100, width=210, height=80, rx=14, fill=GOLD)
    s.F("rect", x=250, y=300, width=210, height=80, rx=14, fill=A1L)
    s.M("M110 140 H160", YEL, 14)
    s.M("M330 140 H380", YEL, 14)
    s.M("M290 340 L340 340 M360 320 L400 360 M400 320 L360 360", RED, 10)


@reg("voltmeter")
def _(s):
    s.F("circle", cx=256, cy=250, r=190, fill=WHITE)
    ring(s, 256, 250, 190, GREY, 24)
    s.M("M256 250 L330 170", RED, 12)
    for i in range(7):
        x1, y1 = arc_pt(256, 250, 130, 200 + i * 23)
        x2, y2 = arc_pt(256, 250, 158, 200 + i * 23)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DGREY, 8)
    s.F("circle", cx=256, cy=250, r=22, fill=DARK)
    s.M("M226 340 L256 395 L286 340", A1, 16)


@reg("ammeter")
def _(s):
    s.F("circle", cx=256, cy=250, r=190, fill=WHITE)
    ring(s, 256, 250, 190, GREY, 24)
    s.M("M256 250 L190 170", RED, 12)
    for i in range(7):
        x1, y1 = arc_pt(256, 250, 130, 200 + i * 23)
        x2, y2 = arc_pt(256, 250, 158, 200 + i * 23)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DGREY, 8)
    s.F("circle", cx=256, cy=250, r=22, fill=DARK)
    s.M("M226 340 H286 M226 372 H286", A2, 16)


@reg("generator")
def _(s):
    s.F("rect", x=70, y=180, width=240, height=210, rx=34, fill=A1)
    s.F("rect", outline=False, x=88, y=196, width=204, height=36, rx=14, fill=A1L)
    s.F("circle", cx=190, cy=300, r=62, fill=A2)
    s.open("part-wheel", "190 300")
    s.F("rect", x=176, y=262, width=28, height=76, rx=10, fill=WHITE)
    s.F("rect", x=152, y=286, width=76, height=28, rx=10, fill=WHITE)
    s.close()
    s.F("rect", x=310, y=250, width=60, height=34, rx=8, fill=DGREY)
    s.T("M370 267 C420 267 430 340 450 340", DGREY, 12)
    bolt(s, 420, 150, 0.35)
    s.F("rect", x=100, y=390, width=180, height=36, rx=10, fill=DGREY)


@reg("electric-motor")
def _(s):
    s.F("rect", x=100, y=150, width=260, height=220, rx=60, fill=GREY)
    s.F("rect", outline=False, x=122, y=170, width=140, height=26, rx=12, fill=WHITE, fill_opacity="0.5")
    s.F("rect", x=360, y=232, width=70, height=56, rx=8, fill=DGREY)
    s.open("part-wheel", "232 260")
    s.F("circle", cx=232, cy=260, r=70, fill=A2)
    for a in (0, 90, 180, 270):
        x, y = arc_pt(232, 260, 40, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=12, fill=A2L)
    s.close()
    s.F("circle", cx=232, cy=260, r=16, fill=DARK)
    s.F("rect", x=130, y=370, width=200, height=36, rx=10, fill=DGREY)
    s.F("rect", x=100, y=110, width=60, height=50, rx=8, fill=RED)


# ================================================================ light-sound-heat
@reg("light-ray")
def _(s):
    s.F("circle", cx=110, cy=256, r=62, fill=YEL)
    for i, y in enumerate((170, 256, 342)):
        s.M(f"M190 {256 + (y - 256) * 0.3:.0f} L460 {y}", YEL, 16)
    s.F("polygon", points="430,150 480,170 440,205", fill=YEL)
    s.F("polygon", points="440,236 490,256 440,276", fill=YEL)
    s.F("polygon", points="430,362 480,342 440,308", fill=YEL)


@reg("reflection")
def _(s):
    s.T("M60 400 H452", DGREY, 22)
    s.F("rect", outline=False, x=40, y=412, width=432, height=18, fill=A1L)
    s.M("M256 400 V120", MID, 6)
    s.T("M80 130 L256 400", YEL, 16)
    s.T("M256 400 L432 130", YEL, 16)
    s.F("polygon", points=star_pts(256, 400, 28, 12, 8), fill=ORANGE)


@reg("refraction")
def _(s):
    s.F("rect", x=40, y=250, width=432, height=190, rx=18, fill=A1L)
    s.M("M256 80 V440", MID, 6)
    s.T("M110 70 L256 250", YEL, 16)
    s.T("M256 250 L330 430", YEL, 16)
    s.F("circle", cx=256, cy=250, r=14, fill=ORANGE)


@reg("rainbow-spectrum")
def _(s):
    for i, c in enumerate((RED, ORANGE, YEL, GREEN, BLUE, "#4F46C8", PURPLE)):
        r = 200 - i * 24
        s.raw(f'<path d="M{256 - r} 380 A{r} {r} 0 0 1 {256 + r} 380" fill="none" stroke="{c}" stroke-width="26"/>')
    s.raw(f'<path d="M{256 - 212} 380 A212 212 0 0 1 {256 + 212} 380" fill="none" stroke="{INK}" stroke-width="10" data-outline="under"/>')
    s.F("circle", outline=False, cx=70, cy=395, r=36, fill=WHITE)
    s.F("circle", outline=False, cx=442, cy=395, r=36, fill=WHITE)


@reg("prism-splitting-light")
def _(s):
    s.F("polygon", points="256,100 400,360 112,360", fill=GLASS)
    s.F("polygon", outline=False, points="256,128 274,160 160,340 140,340", fill=WHITE, fill_opacity="0.55")
    s.T("M30 290 L190 245", WHITE, 14)
    for i, c in enumerate((RED, ORANGE, YEL, GREEN, BLUE, PURPLE)):
        s.M(f"M326 {270 + i * 12} L480 {235 + i * 36}", c, 12)


@reg("shadow")
def _(s):
    s.F("rect", x=40, y=410, width=432, height=40, rx=14, fill=GREEN)
    s.F("circle", cx=96, cy=110, r=52, fill=YEL)
    s.M("M96 36 V20 M22 110 H6 M170 110 H186 M44 58 L32 46 M148 58 L160 46", YEL, 10)
    s.F("path", outline=False, d="M190 418 L470 424 L340 440 L190 436Z", fill=DGREY, fill_opacity="0.55")
    s.F("ellipse", outline=False, cx=420, cy=428, rx=60, ry=12, fill=DGREY, fill_opacity="0.55")
    s.T("M190 420 V260", BROWN, 36)
    s.F("circle", cx=190, cy=190, r=100, fill=DGREEN)
    s.F("circle", outline=False, cx=150, cy=150, r=30, fill=GREEN)


@reg("light-speed")
def _(s):
    s.F("circle", cx=380, cy=256, r=90, fill=YEL)
    bolt(s, 380, 256, 0.34, "#FFFFFF")
    for y in (150, 210, 270, 330, 390):
        s.M(f"M40 {y} H{160 + (y % 3) * 20}", MID, 12)
    s.M("M70 256 H240", YEL, 16)


@reg("colour-wheel")
def _(s):
    cols = [RED, ORANGE, YEL, "#B8D84A", GREEN, "#2FB5A8", SKY, BLUE, PURPLE, "#C04FB5", PINK, DRED]
    for i, c in enumerate(cols):
        a0 = -90 + i * 30
        x1, y1 = arc_pt(256, 256, 190, a0)
        x2, y2 = arc_pt(256, 256, 190, a0 + 30)
        s.raw(f'<path d="M256 256 L{x1:.0f} {y1:.0f} A190 190 0 0 1 {x2:.0f} {y2:.0f}Z" fill="{c}"/>')
    s.raw(f'<circle cx="256" cy="256" r="190" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    s.F("circle", cx=256, cy=256, r=60, fill=WHITE)


@reg("primary-colours")
def _(s):
    for x, y, c in ((200, 190, RED), (312, 190, YEL), (256, 290, BLUE)):
        s.F("circle", cx=x, cy=y, r=100, fill=c, fill_opacity="0.85")
    s.F("path", outline=False, d="M256 128 C224 150 212 170 212 190 C212 210 228 230 256 244 C284 230 300 210 300 190 C300 170 288 150 256 128Z", fill=ORANGE)


@reg("laser-beam")
def _(s):
    s.F("rect", x=40, y=210, width=140, height=92, rx=20, fill=DGREY)
    s.F("rect", outline=False, x=56, y=224, width=70, height=18, rx=8, fill=GREY)
    s.F("circle", cx=190, cy=256, r=26, fill=RED)
    s.T("M200 256 H472", RED, 18)
    s.M("M200 256 H472", "#FFD0D0", 6)
    s.F("polygon", points=star_pts(440, 256, 30, 12, 8), fill=YEL)


@reg("electromagnetic-spectrum")
def _(s):
    cols = ["#6B4BD8", "#8B5CF6", BLUE, GREEN, YEL, ORANGE, RED]
    for i, c in enumerate(cols):
        s.F("rect", outline=False, x=50 + i * 59, y=260, width=60, height=150, fill=c)
    s.raw(f'<rect x="50" y="260" width="412" height="150" rx="20" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    s.M("M50 170 C80 120 110 220 140 170 C170 120 200 220 230 170 C260 120 290 220 320 170 C350 120 380 220 410 170 C430 140 450 160 462 170", A1, 14)


@reg("sound-wave")
def _(s):
    s.M("M40 256 C70 140 100 140 130 256 C160 372 190 372 220 256 C250 140 280 140 310 256 C340 372 370 372 400 256 C415 195 435 195 472 256", A1, 24)


@reg("vibration")
def _(s):
    s.T("M60 256 H452", GREY, 12)
    s.F("circle", cx=256, cy=256, r=44, fill=A2)
    for dx in (-1, 1):
        for k in (1, 2):
            s.M(f"M{256 + dx * (44 + k * 36)} {256 - 40 + k * 8} V{256 + 40 - k * 8}", A1, 14)
    s.M("M256 130 V160 M256 352 V382", MID, 10)


@reg("echo")
def _(s):
    s.F("rect", x=360, y=90, width=80, height=330, rx=14, fill=DGREY)
    for i, x in enumerate((200, 255, 310)):
        r = 38 + i * 14
        s.raw(f'<path d="M{x} {256 - r} A{r} {r} 0 0 1 {x} {256 + r}" fill="none" stroke="{A1}" stroke-width="16" stroke-linecap="round"/>')
    s.F("rect", x=40, y=210, width=70, height=92, rx=18, fill=A2)


@reg("frequency")
def _(s):
    s.M("M40 160 C60 110 80 110 100 160 C120 210 140 210 160 160 C180 110 200 110 220 160 C240 210 260 210 280 160 C300 110 320 110 340 160", A1, 18)
    s.M("M40 340 C80 290 120 290 160 340 C200 390 240 390 280 340 C320 290 360 290 400 340", A2, 18)
    s.F("rect", x=360, y=120, width=100, height=60, rx=14, fill=DARK)
    s.M("M376 150 H444", "#9BE0A8", 8)


@reg("loudness")
def _(s):
    s.F("path", d="M60 200 H140 L250 110 V402 L140 312 H60Z", fill=A1)
    for r, w in ((60, 22), (110, 22), (160, 22)):
        s.raw(f'<path d="M270 {256 - r} A{r} {r} 0 0 1 270 {256 + r}" fill="none" stroke="{A2}" stroke-width="{w}" stroke-linecap="round"/>')


@reg("tuning-fork")
def _(s):
    s.T("M256 460 V250", GREY, 36)
    s.T("M190 60 V200 C190 260 322 260 322 200 V60", GREY, 30)
    s.M("M150 130 C130 100 130 160 150 190 M362 130 C382 100 382 160 362 190", A2, 12)


@reg("ultrasound")
def _(s):
    s.F("rect", x=60, y=210, width=100, height=92, rx=20, fill=DGREY)
    for i, r in enumerate((70, 120, 170)):
        s.raw(f'<path d="M190 {256 - r * 0.8:.0f} A{r} {r} 0 0 1 190 {256 + r * 0.8:.0f}" fill="none" stroke="{A1}" stroke-width="14" stroke-linecap="round" transform="translate({i * 20} 0)"/>')
    s.F("path", d="M390 170 C450 170 470 250 440 320 C420 370 380 380 360 340 C340 300 350 200 390 170Z", fill=PINK)
    s.F("circle", cx=410, cy=260, r=26, fill=A1L)


@reg("heat-transfer")
def _(s):
    s.F("circle", cx=110, cy=256, r=80, fill=RED)
    s.F("circle", cx=402, cy=256, r=80, fill=A1)
    arrow(s, 210, 256, 290, 256, A2, 20, 46)
    s.M("M110 190 V170 M60 210 L40 190", ORANGE, 10)


@reg("conduction")
def _(s):
    s.T("M150 330 H430", GREY, 56)
    for x, c in ((180, RED), (230, ORANGE), (280, YEL)):
        s.F("rect", outline=False, x=x - 24, y=306, width=52, height=48, fill=c, fill_opacity="0.9")
    flame(s, 100, 360, 0.9)
    for x in (200, 260, 320):
        s.M(f"M{x} 270 C{x - 16} 240 {x + 16} 220 {x} 190", MID, 8)


@reg("convection")
def _(s):
    s.F("rect", x=100, y=70, width=312, height=300, rx=30, fill=GLASS)
    s.F("path", outline=False, d="M110 110 H402 V360 H110Z", fill=A1L, fill_opacity="0.6")
    s.raw(f'<path d="M170 330 V190 C170 120 250 110 256 150 C262 110 342 120 342 190 V330" fill="none" stroke="{RED}" stroke-width="16" stroke-linecap="round"/>')
    s.F("polygon", points="170,300 140,330 200,330", fill=A1)
    s.F("polygon", points="342,230 312,200 372,200", fill=RED)
    s.F("rect", x=70, y=374, width=372, height=36, rx=14, fill=DGREY)
    flame(s, 200, 450, 0.5)
    flame(s, 312, 450, 0.5)


@reg("radiation-heat")
def _(s):
    s.F("circle", cx=110, cy=140, r=70, fill=YEL)
    for i in range(3):
        s.M(f"M{210 + i * 8} {90 + i * 60} C{260} {110 + i * 60} {290} {70 + i * 60} {340} {100 + i * 60} S{400} {140 + i * 60} {430} {120 + i * 60}", ORANGE, 12)
    s.F("circle", cx=380, cy=380, r=60, fill=A2L)


@reg("thermometer-scale")
def _(s):
    s.F("rect", x=190, y=40, width=80, height=330, rx=40, fill=GLASS)
    s.F("circle", cx=230, cy=410, r=60, fill=RED)
    s.F("rect", outline=False, x=216, y=130, width=28, height=290, rx=14, fill=RED)
    for i, y in enumerate(range(80, 340, 26)):
        s.M(f"M290 {y} h{36 if i % 2 == 0 else 24}", DGREY, 8)


@reg("temperature")
def _(s):
    s.F("rect", x=180, y=50, width=76, height=320, rx=38, fill=GLASS)
    s.F("circle", cx=218, cy=410, r=56, fill=RED)
    s.F("rect", outline=False, x=205, y=160, width=26, height=260, rx=13, fill=RED)
    s.M("M300 150 C330 120 330 180 360 150", ORANGE, 14)
    s.M("M300 260 C330 230 330 290 360 260", SKY, 14)
    s.F("circle", cx=420, cy=130, r=40, fill=YEL)
    s.F("circle", cx=420, cy=330, r=40, fill=A1L)


@reg("absolute-zero")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=A1L)
    s.M("M256 90 V422 M112 173 L400 339 M112 339 L400 173", WHITE, 14)
    for a in range(0, 360, 60):
        x, y = arc_pt(256, 256, 150, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=14, fill=WHITE)
    s.F("circle", cx=256, cy=256, r=50, fill=WHITE)
    s.M("M236 256 H276", A1, 14)


# ================================================================ biology-basics
def cell_body(s, color, edge):
    s.F("path", d="M256 56 C380 40 470 140 456 270 C444 380 350 470 240 456 C120 444 50 360 62 240 C74 130 150 70 256 56Z", fill=color)


@reg("cell")
def _(s):
    cell_body(s, A1L, A1)
    s.F("circle", cx=256, cy=250, r=80, fill=A1)
    s.F("circle", outline=False, cx=256, cy=250, r=34, fill=A1D)
    for x, y in ((130, 150), (380, 170), (150, 360), (370, 350)):
        s.F("ellipse", cx=x, cy=y, rx=34, ry=20, fill=A2)


@reg("animal-cell")
def _(s):
    s.F("ellipse", cx=256, cy=256, rx=210, ry=190, fill=PINK)
    s.F("circle", cx=256, cy=240, r=70, fill=PURPLE)
    s.F("circle", outline=False, cx=256, cy=240, r=28, fill="#C9B0FF")
    for x, y, rot in ((130, 170, 30), (380, 190, -20), (150, 350, -30), (380, 340, 20)):
        s.F("ellipse", cx=x, cy=y, rx=38, ry=20, fill=ORANGE, transform=f"rotate({rot} {x} {y})")
    s.F("circle", cx=330, cy=100, r=16, fill=A1)
    s.F("circle", cx=200, cy=420, r=16, fill=A1)


@reg("plant-cell")
def _(s):
    s.F("rect", x=50, y=70, width=412, height=372, rx=60, fill=GREEN)
    s.F("rect", x=78, y=98, width=356, height=316, rx=44, fill="#9BE0A8")
    s.F("ellipse", cx=300, cy=260, rx=100, ry=90, fill=A1L)
    s.F("circle", cx=160, cy=200, r=44, fill=PURPLE)
    for x, y, rot in ((150, 340, 20), (230, 150, -20), (360, 150, 25)):
        s.F("ellipse", cx=x, cy=y, rx=34, ry=18, fill=DGREEN, transform=f"rotate({rot} {x} {y})")


@reg("cell-nucleus")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=PURPLE)
    s.F("circle", cx=256, cy=256, r=70, fill="#C9B0FF")
    s.F("circle", outline=False, cx=256, cy=256, r=26, fill=PURPLE)
    s.T("M130 200 C170 160 200 200 240 170 M290 350 C330 330 340 370 380 340", "#C9B0FF", 14)


@reg("cell-division")
def _(s):
    s.F("path", d="M256 110 C340 70 450 110 450 220 C450 270 430 290 410 300 C430 310 450 330 450 370 C450 450 340 450 256 400 C172 450 62 450 62 370 C62 330 82 310 102 300 C82 290 62 270 62 220 C62 110 172 70 256 110Z", fill=PINK)
    s.F("circle", cx=160, cy=250, r=46, fill=PURPLE)
    s.F("circle", cx=352, cy=250, r=46, fill=PURPLE)


@reg("dna")
def _(s):
    def strand(sign):
        pts = []
        for i in range(0, 101):
            y = 50 + i * 4.1
            x = 256 + sign * 92 * math.sin(i / 100 * 3 * 2 * math.pi)
            pts.append(f"{x:.1f} {y:.1f}")
        return "M" + " L".join(pts)
    for k in range(0, 13):
        y = 50 + k * 34.2
        x = 92 * math.sin((y - 50) / 410 * 3 * 2 * math.pi)
        s.M(f"M{256 - x:.0f} {y:.0f} H{256 + x:.0f}", GREEN if k % 2 else YEL, 10)
    s.T(strand(1), A1, 22)
    s.T(strand(-1), A2, 22)


@reg("chromosome")
def _(s):
    s.F("path", d="M180 60 C230 40 250 100 256 200 C262 100 282 40 332 60 C380 80 350 190 280 256 C350 322 380 432 332 452 C282 472 262 412 256 312 C250 412 230 472 180 452 C132 432 162 322 232 256 C162 190 132 80 180 60Z", fill=PINK)
    s.F("path", outline=False, d="M200 110 C220 100 236 160 240 220 C214 200 190 150 200 110Z", fill=WHITE, fill_opacity="0.5")
    s.F("circle", cx=256, cy=256, r=26, fill=PURPLE)


@reg("gene")
def _(s):
    s.T("M60 150 H452", DGREY, 20)
    s.F("rect", x=200, y=120, width=130, height=60, rx=16, fill=A2)
    s.T("M60 340 C130 280 190 400 256 340 C322 280 382 400 452 340", A1, 22)
    s.M("M256 180 V310", MID, 8)
    arrow_tip = f"{256},{330} 236,300 276,300"
    s.F("polygon", points=arrow_tip, fill=MID)


@reg("genetics")
def _(s):
    s.T("M120 70 C360 150 120 250 360 330", A1, 22)
    s.T("M360 70 C120 150 360 250 120 330", A2, 22)
    s.F("circle", cx=256, cy=420, r=44, fill=GREEN)
    s.F("rect", x=334, y=380, width=100, height=70, rx=14, fill=WHITE)
    s.M("M354 400 H414 M354 426 H394", MID, 8)


@reg("evolution")
def _(s):
    sizes = [(70, 330, 0.5), (170, 300, 0.65), (270, 270, 0.8), (380, 230, 1.0)]
    cols = [TAN, ORANGE, A2, RED]
    for (x, y, k), c in zip(sizes, cols):
        s.open(transform=f"translate({x} {y}) scale({k})")
        s.F("ellipse", cx=40, cy=110, rx=36, ry=46, fill=c)
        s.F("circle", cx=40, cy=40, r=26, fill=c)
        s.close()
    s.T("M60 440 H460", DGREY, 12)
    s.F("polygon", points="470,440 430,418 430,462", fill=DGREY)


@reg("natural-selection")
def _(s):
    s.F("rect", x=40, y=300, width=432, height=40, rx=14, fill=GREEN)
    for i, x in enumerate((90, 160, 230, 300)):
        c = [GREEN, GREEN, ORANGE, GREEN][i]
        s.F("ellipse", cx=x, cy=280, rx=30, ry=18, fill=c)
        s.F("circle", cx=x + 26, cy=266, r=12, fill=c)
    s.F("path", d="M380 120 C430 100 460 140 440 180 L400 230 C390 190 340 190 340 150Z", fill=A1)
    s.F("circle", outline=False, cx=420, cy=140, r=7, fill=INK)


@reg("classification")
def _(s):
    s.T("M256 90 V180 M256 180 H110 V260 M256 180 H402 V260 M110 260 V330 M110 330 H60 M110 330 H170", DGREY, 12)
    s.F("rect", x=196, y=50, width=120, height=64, rx=16, fill=A1)
    s.F("rect", x=60, y=240, width=100, height=56, rx=14, fill=A2)
    s.F("rect", x=352, y=240, width=100, height=56, rx=14, fill=GREEN)
    s.F("rect", x=20, y=350, width=80, height=50, rx=14, fill=A2L)
    s.F("rect", x=130, y=350, width=80, height=50, rx=14, fill=A2L)


@reg("life-cycle")
def _(s):
    for i, (c, a) in enumerate(((TAN, -90), (GREEN, 0), (A2, 90), (A1, 180))):
        x1, y1 = arc_pt(256, 256, 150, a + 12)
        x2, y2 = arc_pt(256, 256, 150, a + 78)
        s.raw(f'<path d="M{x1:.0f} {y1:.0f} A150 150 0 0 1 {x2:.0f} {y2:.0f}" fill="none" stroke="{INK}" stroke-width="50" stroke-linecap="round" data-outline="under"/>')
        s.raw(f'<path d="M{x1:.0f} {y1:.0f} A150 150 0 0 1 {x2:.0f} {y2:.0f}" fill="none" stroke="{c}" stroke-width="30" stroke-linecap="round"/>')
    s.F("ellipse", cx=256, cy=106, rx=26, ry=34, fill=WHITE)
    s.F("ellipse", cx=406, cy=256, rx=34, ry=16, fill=GREEN)
    s.F("ellipse", cx=256, cy=406, rx=30, ry=40, fill=A2)
    s.F("circle", cx=106, cy=256, r=34, fill=A1)


@reg("food-web")
def _(s):
    pts = {"sun": (256, 70), "grass": (110, 250), "rabbit": (256, 250), "mouse": (400, 250), "fox": (180, 420), "owl": (350, 420)}
    for a, b in (("grass", "rabbit"), ("grass", "mouse"), ("rabbit", "fox"), ("rabbit", "owl"), ("mouse", "owl"), ("mouse", "fox")):
        s.T(f"M{pts[a][0]} {pts[a][1]} L{pts[b][0]} {pts[b][1]}", MID, 8)
    s.F("circle", cx=256, cy=70, r=44, fill=YEL)
    s.F("circle", cx=110, cy=250, r=44, fill=GREEN)
    s.F("circle", cx=256, cy=250, r=44, fill=TAN)
    s.F("circle", cx=400, cy=250, r=44, fill=BROWN)
    s.F("circle", cx=180, cy=420, r=44, fill=ORANGE)
    s.F("circle", cx=350, cy=420, r=44, fill=DBROWN)


@reg("habitat")
def _(s):
    s.F("rect", x=40, y=60, width=432, height=380, rx=40, fill="#BFE7FA")
    s.F("path", d="M40 360 C140 310 240 380 340 330 C400 300 440 330 472 320 V400 C472 424 454 440 430 440 H82 C58 440 40 424 40 400Z", fill=GREEN)
    s.T("M150 360 V230", BROWN, 30)
    s.F("circle", cx=150, cy=200, r=70, fill=DGREEN)
    s.F("ellipse", cx=340, cy=300, rx=34, ry=26, fill=TAN)
    s.F("circle", cx=380, cy=270, r=18, fill=TAN)
    s.F("circle", cx=400, cy=110, r=34, fill=YEL)


@reg("adaptation")
def _(s):
    s.F("rect", x=40, y=380, width=432, height=60, rx=14, fill=TAN)
    s.T("M200 380 V200", DGREEN, 44)
    s.T("M200 280 H130 V220 M200 250 H270 V190", DGREEN, 30)
    for x, y in ((200, 160), (130, 200), (270, 170)):
        s.F("circle", outline=False, cx=x, cy=y, r=8, fill=PINK)
    s.F("circle", cx=400, cy=110, r=44, fill=YEL)
    s.F("path", d="M310 380 C310 330 350 310 400 330 C440 350 440 380 440 380Z", fill=ORANGE)


@reg("bacteria")
def _(s):
    s.F("rect", x=120, y=170, width=272, height=170, rx=85, fill=GREEN)
    s.F("rect", outline=False, x=146, y=190, width=100, height=30, rx=14, fill=WHITE, fill_opacity="0.4")
    s.F("ellipse", cx=270, cy=262, rx=50, ry=30, fill=DGREEN)
    s.T("M392 255 C440 220 460 300 480 260", DGREEN, 10)
    for x, y in ((140, 160), (190, 350), (330, 355), (370, 165)):
        s.T(f"M{x} {y} l{-30 if x < 256 else 30} {-30 if y < 256 else 30}", DGREEN, 8)


@reg("virus")
def _(s):
    for a in range(0, 360, 36):
        x1, y1 = arc_pt(256, 256, 110, a)
        x2, y2 = arc_pt(256, 256, 170, a)
        s.T(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DGREY, 8)
        s.F("circle", cx=f"{x2:.0f}", cy=f"{y2:.0f}", r=16, fill=RED)
    s.F("circle", cx=256, cy=256, r=120, fill=PURPLE)
    s.F("circle", outline=False, cx=220, cy=220, r=28, fill=WHITE, fill_opacity="0.4")
    s.F("circle", outline=False, cx=300, cy=300, r=20, fill="#C9B0FF")


@reg("fungus-cell")
def _(s):
    s.F("ellipse", cx=256, cy=270, rx=160, ry=130, fill=C["tan"])
    s.F("circle", cx=256, cy=260, r=60, fill=BROWN)
    s.F("circle", cx=150, cy=300, r=44, fill=CREAM)
    s.F("circle", cx=370, cy=300, r=34, fill=CREAM)
    s.F("circle", cx=380, cy=170, r=44, fill=CREAM)
    s.T("M200 150 C180 100 220 80 250 100", TAN, 14)


@reg("amoeba")
def _(s):
    s.F("path", d="M110 200 C60 160 130 90 190 110 C220 60 300 50 330 100 C400 80 470 150 440 220 C490 270 450 350 390 350 C380 410 300 450 240 410 C190 450 100 420 110 350 C50 330 60 240 110 200Z", fill=A1L)
    s.F("circle", cx=250, cy=240, r=50, fill=A1)
    s.F("circle", outline=False, cx=250, cy=240, r=20, fill=A1D)
    s.F("circle", cx=160, cy=320, r=24, fill=WHITE)
    s.F("circle", cx=350, cy=300, r=18, fill=WHITE)


@reg("paramecium")
def _(s):
    s.F("path", d="M70 330 C60 200 200 130 330 170 C450 210 470 330 360 380 C260 420 90 430 70 330Z", fill=A1L)
    for i in range(8):
        s.M(f"M{110 + i * 42} {350 - abs(i - 3.5) * 8 + 60} l{-8} 22", A1, 7)
    s.F("ellipse", cx=270, cy=280, rx=52, ry=34, fill=A1)
    s.F("circle", cx=170, cy=270, r=26, fill=WHITE)
    s.F("circle", cx=370, cy=270, r=22, fill=WHITE)
    s.M("M120 240 C170 210 220 215 260 235", WHITE, 8)


@reg("microorganisms")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=GLASS)
    s.F("rect", outline=False, x=110, y=130, width=96, height=44, rx=22, fill=GREEN)
    s.F("circle", cx=340, cy=170, r=46, fill=PURPLE)
    s.F("path", d="M170 290 C150 250 220 240 240 270 C270 250 300 290 280 320 C300 360 240 380 220 350 C180 370 140 330 170 290Z", fill=A1L)
    s.F("circle", outline=False, cx=210, cy=312, r=18, fill=A1)
    s.F("circle", cx=370, cy=330, r=30, fill=PINK)
    s.M("M370 300 V280 M400 330 H420 M340 330 H320", PINK, 8)


# ================================================================ famous-experiments
@reg("double-slit-experiment")
def _(s):
    s.F("circle", cx=70, cy=256, r=40, fill=YEL)
    s.F("rect", x=190, y=70, width=36, height=130, rx=6, fill=DGREY)
    s.F("rect", x=190, y=232, width=36, height=48, rx=6, fill=DGREY)
    s.F("rect", x=190, y=312, width=36, height=130, rx=6, fill=DGREY)
    s.M("M110 256 H190", YEL, 10)
    s.F("rect", x=420, y=60, width=40, height=392, rx=10, fill=WHITE)
    for y in (110, 170, 230, 256, 282, 342, 402):
        w = 34 - abs(y - 256) / 8
        s.F("rect", outline=False, x=424, y=y - 14, width=32, height=28, rx=6, fill=A1 if abs(y - 256) < 80 else A1L)
    s.M("M226 244 C300 200 360 120 420 110 M226 268 C300 310 360 400 420 402", A1L, 7)


@reg("pendulum-experiment")
def _(s):
    s.F("rect", x=100, y=50, width=312, height=26, rx=10, fill=DGREY)
    s.M("M256 76 L170 360", DGREY, 6)
    ball(s, 170, 388, 36, A2)
    s.raw(f'<path d="M170 388 A315 315 0 0 0 342 388" fill="none" stroke="{MID}" stroke-width="6" stroke-dasharray="10 12"/>')
    s.F("circle", cx=342, cy=388, r=34, fill=A2L)
    s.F("rect", x=60, y=440, width=392, height=22, rx=8, fill=BROWN)
    s.F("rect", x=360, y=90, width=70, height=70, rx=12, fill=WHITE)
    s.F("circle", outline=False, cx=395, cy=125, r=22, fill=A1L)


@reg("leaning-tower-drop-experiment")
def _(s):
    s.open(transform="rotate(8 256 400)")
    s.F("path", d="M170 440 L190 110 H322 L342 440Z", fill=CREAM)
    for y in (160, 220, 280, 340, 400):
        s.M(f"M{186 + (y - 110) * 0.04:.0f} {y} H{326 - (y - 110) * 0.04:.0f}", TAN, 8)
    s.F("rect", x=180, y=84, width=152, height=36, rx=10, fill=TAN)
    s.F("rect", x=202, y=60, width=108, height=30, rx=10, fill=CREAM)
    s.close()
    ball(s, 410, 160, 34, DGREY)
    ball(s, 460, 270, 20, A2)
    s.M("M410 200 V230 M460 300 V320", MID, 8)
    s.F("rect", x=40, y=440, width=432, height=24, rx=8, fill=GREEN)


@reg("kite-and-key-experiment")
def _(s):
    s.F("polygon", points="256,40 340,150 256,250 172,150", fill=A1)
    s.M("M256 40 V250 M172 150 H340", WHITE, 8)
    s.T("M256 250 C280 330 220 380 250 450", TAN, 6)
    s.raw(f'<circle cx="236" cy="410" r="20" fill="none" stroke="{GOLD}" stroke-width="12"/>')
    s.F("rect", x=224, y=420, width=24, height=60, rx=6, fill=GOLD)
    bolt(s, 400, 150, 0.4)
    s.F("path", d="M90 100 C40 100 30 150 70 160 H160 C200 160 200 110 160 100 C150 60 110 60 90 100Z", fill=MID)


@reg("prism-experiment")
def _(s):
    s.F("rect", x=30, y=40, width=60, height=432, rx=10, fill=DGREY)
    s.F("rect", outline=False, x=52, y=236, width=38, height=40, fill=YEL)
    s.M("M90 256 L190 256", YEL, 14)
    s.F("polygon", points="256,170 330,330 182,330", fill=GLASS)
    for i, c in enumerate((RED, ORANGE, YEL, GREEN, BLUE, PURPLE)):
        s.M(f"M310 {270 + i * 10} L470 {230 + i * 38}", c, 12)


@reg("pea-plant-experiment")
def _(s):
    s.T("M256 460 V150", GREEN, 24)
    s.F("path", d="M256 360 C150 360 100 300 110 240 C190 250 250 290 256 360Z", fill=GREEN)
    s.F("path", d="M256 300 C360 300 410 240 400 180 C320 190 262 230 256 300Z", fill=GREEN)
    s.F("path", d="M256 150 C230 80 280 50 310 80 C340 110 300 150 256 150Z", fill=PINK)
    for x, y, c in ((340, 420, GREEN), (390, 440, YEL), (420, 400, GREEN)):
        s.F("circle", cx=x, cy=y, r=24, fill=c)
    s.F("rect", x=110, y=440, width=100, height=30, rx=10, fill=BROWN)


if __name__ == "__main__":
    run("science", D, sys.argv[1:] or None)
