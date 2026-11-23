"""earth-geography: hand-drawn groups (landforms, earth layers, volcanoes, rocks, gems, fossils,
biomes, maps and navigation). Maps of real places are in earth_geography.py; flags in flags.py.
Run: python drawings/earth_geography_hand.py [ids...]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run, star_pts  # noqa: E402

D = {}
_cur = [""]

SKY, SKY2 = "#BFE6FA", "#8FD0FF"
GRASS, GRASS_D, GRASS_L = "#7CC56F", "#4E9E4A", "#A6DB8E"
WATER, WATER_D, WATER_L = "#5BB0F0", "#3D8BC9", "#A8DAF7"
SEA = "#7FC4EE"
ROCK, ROCK_D, ROCK_L = "#A89A8A", "#7D6E60", "#C9BCAE"
RED_R, RED_RD, RED_RL = "#D9774A", "#A8522E", "#EDA27A"
SAND, SAND_D = "#EBD49A", "#D2B46E"
SNOW, ICE, ICE_D = "#FFFFFF", "#DDF1FB", "#A9D8F0"
EARTH, EARTH_D = C["brown"], C["darkbrown"]
TRUNK, LEAF, LEAF_D = "#8A5A33", "#3FA45A", "#2F7F45"
WHITE, BLACK, YELLOW, ORANGE, RED = C["white"], C["black"], C["yellow"], C["orange"], C["red"]


def reg(name):
    def r(fn):
        def wrapped(s):
            _cur[0] = name
            fn(s)
        D[name] = wrapped
        return fn
    return r


# ---------------------------------------------------------------- scene helpers
def tile(s, sky=SKY):
    """Rounded scene tile; everything until end() is clipped to it."""
    cid = "clip-" + _cur[0]
    s.raw(f'<defs><clipPath id="{cid}"><rect x="24" y="24" width="464" height="464" rx="36"/></clipPath></defs>')
    s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill=sky)
    s.raw(f'<g clip-path="url(#{cid})">')


def end(s):
    s.raw("</g>")
    s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill="none")


def peak(s, x, by, w, h, c=ROCK, shade=ROCK_D, snow=0.3):
    s.F("polygon", points=f"{x - w / 2:.0f},{by:.0f} {x:.0f},{by - h:.0f} {x + w / 2:.0f},{by:.0f}", fill=c)
    s.F("polygon", outline=False, points=f"{x:.0f},{by - h + 14:.0f} {x + w / 2 - 12:.0f},{by - 4:.0f} {x + w * 0.08:.0f},{by - 4:.0f}", fill=shade)
    if snow:
        f = snow
        lx, ly = x - w / 2 * f, by - h + h * f
        rx_, ry = x + w / 2 * f, by - h + h * f
        s.F("polygon", points=(f"{x:.0f},{by - h:.0f} {rx_:.0f},{ry:.0f} {x + w * 0.07:.0f},{ry - h * 0.06:.0f} "
                               f"{x:.0f},{ry + h * 0.04:.0f} {x - w * 0.08:.0f},{ly - h * 0.05:.0f} {lx:.0f},{ly:.0f}"), fill=SNOW)


def sun(s, x=400, y=110, r=40):
    s.F("circle", cx=x, cy=y, r=r, fill=YELLOW)


def cloud(s, x, y, k=1.0):
    s.F("path", d=(f"M{x - 60 * k:.0f} {y + 20 * k:.0f} C{x - 80 * k:.0f} {y + 20 * k:.0f} {x - 80 * k:.0f} {y - 10 * k:.0f} {x - 54 * k:.0f} {y - 10 * k:.0f} "
                   f"C{x - 50 * k:.0f} {y - 40 * k:.0f} {x - 6 * k:.0f} {y - 44 * k:.0f} {x + 4 * k:.0f} {y - 20 * k:.0f} "
                   f"C{x + 24 * k:.0f} {y - 36 * k:.0f} {x + 60 * k:.0f} {y - 24 * k:.0f} {x + 56 * k:.0f} {y:.0f} "
                   f"C{x + 80 * k:.0f} {y:.0f} {x + 80 * k:.0f} {y + 20 * k:.0f} {x + 60 * k:.0f} {y + 20 * k:.0f} Z"), fill=WHITE)


def tree(s, x, y, k=1.0, kind="round"):
    s.F("rect", x=f"{x - 7 * k:.0f}", y=f"{y - 40 * k:.0f}", width=f"{14 * k:.0f}", height=f"{40 * k:.0f}", fill=TRUNK)
    if kind == "pine":
        s.F("polygon", points=f"{x:.0f},{y - 120 * k:.0f} {x + 36 * k:.0f},{y - 34 * k:.0f} {x - 36 * k:.0f},{y - 34 * k:.0f}", fill=LEAF_D)
    else:
        s.F("circle", cx=f"{x:.0f}", cy=f"{y - 62 * k:.0f}", r=f"{34 * k:.0f}", fill=LEAF)


def palm(s, x, y, k=1.0, lean=1):
    tx = x + 30 * k * lean
    s.T(f"M{x:.0f} {y:.0f} Q{x + 4 * k * lean:.0f} {y - 80 * k:.0f} {tx:.0f} {y - 150 * k:.0f}", TRUNK, 14 * k)
    ty = y - 150 * k
    for dx, dy in ((-70, 20), (-50, -30), (10, -50), (60, -20), (74, 26)):
        s.F("path", d=(f"M{tx:.0f} {ty:.0f} Q{tx + dx * k * 0.6:.0f} {ty + dy * k - 30 * k:.0f} {tx + dx * k:.0f} {ty + dy * k:.0f} "
                       f"Q{tx + dx * k * 0.5:.0f} {ty + dy * k * 0.4 - 8 * k:.0f} {tx:.0f} {ty:.0f} Z"), fill=LEAF)


def cactus(s, x, y, k=1.0):
    s.F("path", d=(f"M{x - 16 * k:.0f} {y:.0f} V{y - 120 * k:.0f} A16 16 0 0 1 {x + 16 * k:.0f} {y - 120 * k:.0f} V{y:.0f} Z"), fill=GRASS_D)
    s.T(f"M{x - 16 * k:.0f} {y - 60 * k:.0f} H{x - 40 * k:.0f} V{y - 92 * k:.0f}", GRASS_D, 20 * k)
    s.T(f"M{x + 16 * k:.0f} {y - 76 * k:.0f} H{x + 38 * k:.0f} V{y - 104 * k:.0f}", GRASS_D, 20 * k)


def ground(s, y, color=GRASS, wave=0):
    s.F("path", d=f"M0 {y} C140 {y - wave} 340 {y + wave} 512 {y} V512 H0 Z", fill=color)


def wavelines(s, x0, x1, y, color=WHITE, n=3, gap=26):
    for i in range(n):
        yy = y + i * gap
        s.M(f"M{x0 + i * 20} {yy} q15 -10 30 0 t30 0", color, 6)


def tag_arrow(s, x, y, ang_deg, color=RED):
    """Pointer arrow, tip at (x, y), coming from direction ang_deg."""
    a = math.radians(ang_deg)
    x0, y0 = x + 90 * math.cos(a), y + 90 * math.sin(a)
    s.T(f"M{x0:.0f} {y0:.0f} L{x:.0f} {y:.0f}", color, 14)
    s.T(head(x, y, math.degrees(math.atan2(y - y0, x - x0)), 30, 35), color, 14)


# ---------------------------------------------------------------- landforms
@reg("mountain")
def _(s):
    tile(s)
    sun(s, 400, 110)
    cloud(s, 130, 120, 0.8)
    peak(s, 256, 470, 520, 330)
    ground(s, 450, GRASS, 10)
    end(s)


@reg("mountain-range")
def _(s):
    tile(s)
    cloud(s, 380, 100, 0.7)
    peak(s, 120, 440, 280, 230, ROCK_L, ROCK)
    peak(s, 390, 440, 300, 260, ROCK_L, ROCK)
    peak(s, 250, 460, 360, 330)
    ground(s, 440, GRASS, 12)
    end(s)


@reg("snowy-peak")
def _(s):
    tile(s, "#D6EEFB")
    peak(s, 256, 500, 500, 400, ICE_D, "#7FB4D4", snow=0.55)
    for x, y in ((90, 120), (140, 220), (420, 150), (380, 260), (110, 330), (440, 360)):
        s.F("circle", cx=x, cy=y, r=9, fill=WHITE)
    end(s)


@reg("hill")
def _(s):
    tile(s)
    sun(s, 110, 110, 36)
    s.F("path", d="M-10 400 C80 230 260 230 360 400 Z", fill=GRASS_L)
    s.F("path", d="M150 470 C250 250 450 250 530 470 Z", fill=GRASS)
    ground(s, 440, GRASS_D, 8)
    tree(s, 340, 300, 0.7)
    end(s)


@reg("valley")
def _(s):
    tile(s)
    sun(s, 256, 120, 40)
    s.F("path", d="M0 120 C80 140 170 300 230 420 L0 520 Z", fill=GRASS_D)
    s.F("path", d="M512 140 C430 150 340 300 282 420 L512 520 Z", fill=GRASS)
    s.F("path", d="M210 512 C230 440 240 400 256 360 C270 400 290 440 310 512 Z", fill=WATER)
    tree(s, 90, 300, 0.8, "pine")
    tree(s, 430, 320, 0.8, "pine")
    end(s)


@reg("plateau")
def _(s):
    tile(s)
    cloud(s, 120, 110, 0.7)
    s.F("path", d="M60 440 L120 220 H400 L452 440 Z", fill=RED_R)
    s.F("path", outline=False, d="M330 228 H396 L446 432 H360 Z", fill=RED_RD)
    s.F("path", d="M110 222 C200 206 320 206 406 222 L400 236 H116 Z", fill=GRASS)
    for x in (180, 260, 330):
        tree(s, x, 222, 0.45)
    ground(s, 430, SAND, 6)
    end(s)


@reg("plain")
def _(s):
    tile(s)
    sun(s, 390, 120, 38)
    cloud(s, 150, 130, 0.7)
    s.F("rect", x=0, y=300, width=512, height=220, fill=GRASS)
    s.F("path", outline=False, d="M0 360 H512 V380 H0 Z", fill=GRASS_L)
    s.F("path", outline=False, d="M0 430 H512 V450 H0 Z", fill=GRASS_L)
    tree(s, 90, 304, 0.4)
    tree(s, 430, 304, 0.35)
    for x in (140, 230, 320, 400):
        s.M(f"M{x} 470 l8 -24 m4 24 l6 -20", GRASS_D, 6)
    end(s)


@reg("canyon")
def _(s):
    tile(s, SKY2)
    s.F("path", d="M0 150 H210 L190 220 L200 300 L176 380 L190 512 H0 Z", fill=RED_R)
    s.F("path", d="M512 160 H300 L320 230 L306 310 L330 390 L316 512 H512 Z", fill=RED_R)
    for y, c in ((200, RED_RL), (260, RED_RD), (330, RED_RL), (410, RED_RD)):
        s.F("path", outline=False, d=f"M0 {y} H{196 if y < 300 else 182} V{y + 22} H0 Z", fill=c)
        s.F("path", outline=False, d=f"M512 {y + 6} H{312 if y < 300 else 324} V{y + 28} H512 Z", fill=c)
    s.F("path", d="M186 512 C200 450 230 420 250 400 C270 420 300 450 318 512 Z", fill=WATER)
    end(s)


@reg("gorge")
def _(s):
    tile(s, SKY2)
    s.F("path", d="M0 60 H232 L220 160 L236 260 L218 380 L232 512 H0 Z", fill=ROCK)
    s.F("path", d="M512 60 H282 L294 170 L276 270 L294 380 L280 512 H512 Z", fill=ROCK_D)
    for y in (120, 210, 300, 400):
        s.M(f"M40 {y} H180", ROCK_D, 8)
        s.M(f"M330 {y + 30} H470", "#5E5246", 8)
    s.F("path", d="M226 512 C236 470 248 440 256 420 C266 440 276 470 286 512 Z", fill=WATER)
    tree(s, 70, 64, 0.5, "pine")
    tree(s, 440, 64, 0.5, "pine")
    end(s)


@reg("cliff")
def _(s):
    tile(s)
    s.F("rect", x=0, y=360, width=512, height=160, fill=SEA)
    wavelines(s, 330, 470, 400)
    s.F("path", d="M0 150 H300 C310 200 290 260 310 300 C320 340 300 380 316 520 H0 Z", fill=ROCK)
    s.F("path", outline=False, d="M260 160 H296 C306 206 286 262 306 302 C316 342 296 382 310 512 H270 Z", fill=ROCK_D)
    s.F("path", d="M0 150 H300 V172 H0 Z", fill=GRASS)
    tree(s, 90, 152, 0.7)
    s.F("path", d="M290 488 C330 470 380 470 420 488 V520 H290 Z", fill=WHITE)
    end(s)


@reg("cave")
def _(s):
    tile(s)
    ground(s, 430, GRASS, 6)
    s.F("path", d="M30 460 C40 220 160 120 260 120 C380 120 480 230 486 460 Z", fill=ROCK)
    s.F("path", outline=False, d="M360 150 C430 200 478 300 480 456 H400 C400 320 380 220 360 150 Z", fill=ROCK_D)
    s.F("path", d="M160 460 C160 330 200 270 256 270 C312 270 352 330 352 460 Z", fill="#2B2530")
    for x in (200, 236, 276, 312):
        s.F("polygon", outline=False, points=f"{x - 10},{285 if 220 < x < 300 else 310} {x + 10},{285 if 220 < x < 300 else 310} {x},{330 if 220 < x < 300 else 350}", fill=ROCK_L)
    end(s)


@reg("island")
def _(s):
    tile(s, SKY)
    sun(s, 400, 110, 38)
    s.F("rect", x=0, y=330, width=512, height=200, fill=SEA)
    s.F("path", d="M100 360 C140 300 380 300 420 360 Z", fill=SAND)
    palm(s, 240, 340, 1.0)
    wavelines(s, 60, 200, 410)
    wavelines(s, 320, 460, 430)
    end(s)


def topview(s, land, sea=SEA, beach=True):
    """Map seen from above: sea tile, then land shapes with a sandy edge."""
    tile(s, sea)
    for d in land:
        if beach:
            s.F("path", outline=False, d=d, fill=SAND, stroke=SAND, stroke_width=26)
        s.F("path", d=d, fill=GRASS)


@reg("peninsula")
def _(s):
    topview(s, ["M0 512 V380 C60 370 130 400 180 360 C220 330 200 250 230 190 C260 130 320 120 340 170 C360 220 310 290 330 350 C350 400 440 380 512 400 V512 Z"])
    tree(s, 280, 220, 0.5)
    wavelines(s, 60, 200, 120, WHITE, 2)
    end(s)


@reg("cape")
def _(s):
    topview(s, ["M512 512 V60 C440 90 420 160 370 200 C300 250 210 250 120 300 C90 318 100 340 140 340 C220 340 300 360 360 420 C390 450 380 512 380 512 Z"])
    s.F("rect", x=120, y=250, width=26, height=60, fill=WHITE)
    s.F("rect", outline=False, x=120, y=268, width=26, height=14, fill=RED)
    s.F("polygon", points="114,252 133,224 152,252", fill=RED)
    s.M("M160 240 L230 200 M160 260 L236 260", YELLOW, 8)
    end(s)


@reg("isthmus")
def _(s):
    topview(s, ["M0 0 H512 V130 C430 170 330 150 300 200 C284 228 290 280 300 320 C330 370 430 350 512 390 V512 H0 V380 "
                "C80 360 180 380 210 320 C226 284 224 230 210 196 C180 150 80 160 0 120 Z"])
    wavelines(s, 60, 180, 230, WHITE, 2)
    wavelines(s, 340, 460, 250, WHITE, 2)
    end(s)


@reg("delta")
def _(s):
    topview(s, ["M0 0 H512 V140 C470 170 440 260 430 390 C410 450 100 450 82 390 C72 260 40 170 0 140 Z"])
    s.T("M256 0 C240 60 272 120 256 170", WATER, 30)
    for d in ("M256 170 C200 220 140 300 110 410", "M256 170 C230 260 200 350 196 450", "M256 170 C282 260 310 350 316 450",
              "M256 170 C312 220 372 300 402 410", "M216 300 C240 330 280 330 300 300"):
        s.T(d, WATER, 12)
    tree(s, 90, 110, 0.5)
    tree(s, 420, 120, 0.5)
    end(s)


@reg("river")
def _(s):
    tile(s)
    sun(s, 410, 100, 34)
    s.F("rect", x=0, y=170, width=512, height=360, fill=GRASS)
    s.F("path", d="M240 170 C230 200 300 220 290 260 C280 300 150 320 150 380 C150 440 300 450 330 520 H90 C80 440 70 380 120 330 C170 290 250 290 250 260 C250 230 214 210 226 170 Z", fill=WATER)
    tree(s, 400, 300, 0.7)
    tree(s, 100, 240, 0.5)
    tree(s, 440, 430, 0.8, "pine")
    end(s)


@reg("stream")
def _(s):
    tile(s, GRASS)
    s.F("path", d="M300 0 C260 80 340 140 280 220 C230 290 160 300 180 380 C196 440 260 470 240 520 H170 C190 470 120 440 110 380 C96 290 190 270 230 210 C270 150 210 80 250 0 Z", fill=WATER)
    for x, y, r in ((250, 140, 16), (200, 300, 20), (165, 420, 14), (220, 470, 12)):
        s.F("ellipse", cx=x, cy=y, rx=r + 6, ry=r, fill=ROCK_L)
    for x, y in ((90, 120), (400, 300), (360, 450), (80, 470)):
        s.M(f"M{x} {y} l-10 -30 m14 30 l2 -36 m10 36 l12 -28", GRASS_D, 6)
    end(s)


@reg("waterfall")
def _(s):
    tile(s)
    s.F("rect", x=0, y=380, width=512, height=140, fill=WATER)
    s.F("path", d="M0 80 H180 V420 H0 Z", fill=ROCK)
    s.F("path", d="M512 80 H340 V420 H512 Z", fill=ROCK)
    s.F("path", d="M0 80 H180 V100 H0 Z M340 80 H512 V100 H340 Z", fill=GRASS)
    s.F("path", d="M170 90 H350 V400 H170 Z", fill=WATER_L)
    for x in (200, 240, 280, 320):
        s.M(f"M{x} 110 V380", WHITE, 8)
    for x, r in ((170, 40), (230, 50), (300, 50), (350, 38)):
        s.F("circle", cx=x, cy=410, r=r, fill=WHITE)
    end(s)


@reg("lake")
def _(s):
    tile(s)
    peak(s, 140, 260, 260, 170, ROCK_L, ROCK, 0.3)
    peak(s, 360, 260, 300, 200, ROCK_L, ROCK, 0.3)
    s.F("rect", x=0, y=250, width=512, height=270, fill=GRASS)
    s.F("ellipse", cx=256, cy=370, rx=200, ry=80, fill=WATER)
    s.M("M150 360 H230 M280 390 H360", WHITE, 6)
    tree(s, 60, 360, 0.6, "pine")
    tree(s, 460, 380, 0.6, "pine")
    end(s)


@reg("pond")
def _(s):
    tile(s, GRASS)
    s.F("path", d="M90 260 C90 170 220 140 300 160 C400 180 440 260 410 330 C380 400 230 420 160 390 C110 370 90 320 90 260 Z", fill=WATER)
    for x, y in ((190, 240), (300, 320), (330, 220)):
        s.F("path", d=f"M{x} {y} m-30 0 a30 18 0 1 0 60 0 l-30 0 z", fill=GRASS_L)
    s.F("circle", cx=200, cy=232, r=10, fill=C["pink"])
    for x in (80, 110, 430):
        s.T(f"M{x} 470 V340", GRASS_D, 8)
        s.F("rect", x=x - 8, y=330, width=16, height=40, rx=8, fill=EARTH)
    end(s)


@reg("coastline")
def _(s):
    tile(s, SEA)
    s.F("path", outline=False, d="M0 0 H300 C280 70 340 110 310 170 C280 230 360 280 330 350 C310 400 370 450 350 512 H0 Z", fill=SAND, stroke=SAND, stroke_width=40)
    s.F("path", d="M0 0 H270 C250 70 310 110 280 170 C250 230 330 280 300 350 C280 400 340 450 320 512 H0 Z", fill=GRASS)
    for y in (90, 250, 420):
        s.M(f"M{380 + (y % 60)} {y} q15 -10 30 0 t30 0", WHITE, 6)
    tree(s, 120, 200, 0.6)
    tree(s, 170, 380, 0.6)
    end(s)


@reg("sand-dunes")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 380, 120, 46)
    s.F("path", d="M0 300 C100 220 180 220 300 320 C360 270 440 260 512 290 V520 H0 Z", fill=SAND)
    s.F("path", d="M0 400 C120 330 240 340 340 420 C400 380 460 370 512 380 V520 H0 Z", fill=SAND_D)
    s.M("M60 330 C120 300 170 300 230 330", "#C39A50", 6)
    s.M("M120 450 C180 420 240 420 290 450", "#B88C40", 6)
    end(s)


@reg("desert")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 390, 110, 44)
    s.F("path", d="M0 330 C110 280 230 290 300 340 C380 300 450 300 512 320 V520 H0 Z", fill=SAND)
    s.F("path", d="M0 430 C150 400 330 400 512 440 V520 H0 Z", fill=SAND_D)
    cactus(s, 140, 420, 1.1)
    cactus(s, 380, 360, 0.6)
    end(s)


@reg("oasis")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 410, 100, 38)
    s.F("path", d="M0 300 C140 270 360 270 512 300 V520 H0 Z", fill=SAND)
    s.F("ellipse", cx=256, cy=400, rx=150, ry=50, fill=WATER)
    palm(s, 150, 380, 0.9, 1)
    palm(s, 370, 380, 1.0, -1)
    s.M("M200 400 H260 M280 420 H330", WHITE, 6)
    end(s)


@reg("glacier")
def _(s):
    tile(s)
    peak(s, 110, 400, 280, 320, ROCK, ROCK_D, 0.4)
    peak(s, 410, 400, 280, 330, ROCK, ROCK_D, 0.4)
    s.F("path", d="M200 120 C250 110 290 120 320 140 C340 260 380 380 420 512 H100 C150 380 180 260 200 120 Z", fill=ICE)
    for d in ("M230 200 C240 260 220 320 200 380", "M280 200 C290 280 300 340 320 420", "M256 260 V330"):
        s.M(d, ICE_D, 8)
    end(s)


@reg("iceberg")
def _(s):
    tile(s, SKY)
    s.F("rect", x=0, y=250, width=512, height=270, fill=WATER_D)
    s.F("path", d="M110 470 C90 400 120 330 170 290 L340 290 C400 340 430 420 400 480 C330 510 180 510 110 470 Z", fill="#A9D8F0", opacity="0.85")
    s.F("path", d="M150 260 L200 140 L240 180 L280 100 L330 190 L370 260 Z", fill=SNOW)
    s.F("polygon", outline=False, points="280,100 330,190 370,260 300,260 300,160", fill=ICE)
    s.F("rect", x=0, y=250, width=512, height=14, fill=WATER)
    s.M("M60 300 q15 -8 30 0 t30 0 M400 320 q15 -8 30 0 t30 0", WHITE, 6)
    end(s)


@reg("ice-sheet")
def _(s):
    tile(s, SKY)
    s.F("rect", x=0, y=330, width=512, height=200, fill=WATER_D)
    s.F("path", d="M0 160 C120 150 300 150 420 170 L430 360 H0 Z", fill=ICE)
    s.F("path", d="M0 160 C120 150 300 150 420 170 L424 196 C300 180 120 180 0 190 Z", fill=SNOW)
    s.M("M60 240 L100 270 L90 300 M220 220 L260 250 L250 290 M340 240 L360 280", ICE_D, 7)
    s.F("path", d="M440 330 L460 300 L490 300 L500 330 Z", fill=SNOW)
    end(s)


@reg("fjord")
def _(s):
    tile(s, SKY)
    s.F("path", d="M0 90 C80 80 140 140 200 200 C220 260 210 330 230 520 H0 Z", fill=ROCK)
    s.F("path", d="M512 80 C430 80 360 140 310 200 C292 260 300 330 284 520 H512 Z", fill=ROCK_D)
    s.F("path", d="M0 90 C80 80 140 140 160 170 C110 150 60 140 0 150 Z", fill=GRASS)
    s.F("path", d="M512 80 C430 80 380 120 350 160 C400 140 460 136 512 140 Z", fill=GRASS)
    s.F("path", d="M226 520 C228 400 236 300 256 250 C276 300 284 400 290 520 Z", fill=WATER)
    end(s)


@reg("lagoon")
def _(s):
    tile(s, WATER_D)
    s.F("path", d="M80 260 C80 140 180 70 300 80 C420 90 470 200 440 300 C410 400 300 450 200 430 C120 410 80 350 80 260 Z", fill=SAND)
    s.F("path", d="M130 260 C130 170 200 120 290 126 C380 132 410 210 390 280 C370 350 290 390 210 380 C150 370 130 320 130 260 Z", fill="#7FE0D8")
    s.F("path", outline=False, d="M420 330 L470 360 L460 380 L410 350 Z", fill=WATER_D)
    palm(s, 110, 160, 0.4)
    palm(s, 400, 400, 0.4, -1)
    end(s)


@reg("bay")
def _(s):
    topview(s, ["M0 0 H512 V512 H380 C400 420 420 330 380 260 C330 180 200 170 140 250 C100 300 120 420 150 512 H0 Z"])
    s.F("path", d="M220 440 l20 -10 h40 l-10 14 h-50 z", fill=WHITE)
    s.T("M248 430 V400", DARK, 4)
    s.F("polygon", points="250,402 272,424 250,424", fill=WHITE)
    end(s)


@reg("gulf")
def _(s):
    topview(s, ["M0 0 H512 V120 C470 130 460 200 470 260 C480 330 400 420 300 430 C200 440 110 380 90 300 C70 220 120 160 90 120 C70 90 30 90 0 100 Z"])
    wavelines(s, 200, 320, 300, WHITE, 2)
    end(s)


@reg("strait")
def _(s):
    topview(s, ["M0 0 H512 V200 C420 190 330 230 260 220 C190 210 110 180 0 200 Z",
                "M0 512 H512 V300 C420 290 340 320 260 300 C180 280 100 300 0 300 Z"])
    s.F("path", d="M200 250 h80 l-14 20 h-56 z", fill=RED)
    s.F("rect", x=226, y=230, width=30, height=20, fill=WHITE)
    end(s)


@reg("archipelago")
def _(s):
    land = []
    for x, y, r in ((110, 130, 50), (230, 190, 38), (330, 140, 30), (390, 270, 56), (260, 330, 34), (140, 360, 44), (360, 410, 28), (420, 120, 20)):
        land.append(f"M{x - r} {y} C{x - r} {y - r} {x + r * 0.8} {y - r * 1.1} {x + r} {y} C{x + r * 1.1} {y + r * 0.9} {x - r * 0.6} {y + r} {x - r} {y} Z")
    topview(s, land)
    end(s)


@reg("atoll")
def _(s):
    tile(s, WATER_D)
    s.F("circle", cx=256, cy=256, r=180, fill=SAND)
    s.F("circle", cx=256, cy=256, r=130, fill="#7FE0D8")
    s.F("path", outline=False, d="M410 200 L470 180 L476 230 L418 250 Z", fill=WATER_D)
    s.F("path", outline=False, d="M120 330 L60 370 L80 400 L140 360 Z", fill=WATER_D)
    for a in (110, 160, 230, 300, 20):
        x, y = arc_pt(256, 256, 156, a)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=16, fill=LEAF)
    end(s)


@reg("geyser")
def _(s):
    tile(s)
    ground(s, 400, "#C9B48A", 6)
    s.F("path", d="M220 400 C230 300 220 200 236 110 H276 C292 200 282 300 292 400 Z", fill=WATER_L)
    for x, y, r in ((256, 110, 56), (200, 140, 40), (312, 140, 40), (256, 70, 40)):
        s.F("circle", cx=x, cy=y, r=r, fill=WHITE)
    s.F("ellipse", cx=256, cy=410, rx=110, ry=26, fill=WATER)
    s.F("ellipse", cx=256, cy=404, rx=40, ry=10, fill=WHITE)
    end(s)


@reg("hot-spring")
def _(s):
    tile(s, "#D6EEFB")
    ground(s, 300, ROCK_L, 4)
    s.F("ellipse", cx=256, cy=380, rx=190, ry=80, fill="#7FE0D8")
    for x, y, r in ((100, 330, 30), (420, 340, 36), (380, 450, 26), (130, 450, 30)):
        s.F("ellipse", cx=x, cy=y, rx=r + 10, ry=r, fill=ROCK)
    for x in (190, 256, 320):
        s.M(f"M{x} 340 C{x - 30} 300 {x + 30} 260 {x} 220 C{x - 30} 180 {x + 20} 150 {x} 120", WHITE, 12)
    end(s)


@reg("mesa")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 410, 100, 36)
    s.F("path", d="M40 420 L90 200 H420 L470 420 Z", fill=RED_R)
    for y, c in ((250, RED_RL), (320, RED_RD)):
        s.F("path", outline=False, d=f"M{78 - (y - 200) * 0.2:.0f} {y} H{432 + (y - 200) * 0.2:.0f} V{y + 18} H{74 - (y - 200) * 0.2:.0f} Z", fill=c)
    ground(s, 410, SAND, 6)
    cactus(s, 440, 470, 0.5)
    end(s)


@reg("butte")
def _(s):
    tile(s, "#FFE3B0")
    s.F("path", d="M190 420 L210 140 H300 L322 420 Z", fill=RED_R)
    s.F("path", outline=False, d="M270 144 H298 L318 416 H286 Z", fill=RED_RD)
    s.F("path", d="M60 420 L80 320 H130 L150 420 Z", fill=RED_RL)
    s.F("path", d="M380 420 L396 290 H446 L466 420 Z", fill=RED_RL)
    ground(s, 410, SAND, 6)
    end(s)


@reg("sinkhole")
def _(s):
    tile(s, GRASS)
    s.F("ellipse", cx=256, cy=280, rx=180, ry=120, fill=EARTH)
    s.F("ellipse", cx=256, cy=300, rx=140, ry=90, fill="#3A2A22")
    s.F("path", outline=False, d="M116 300 C130 250 190 220 256 220 C322 220 382 250 396 300 C380 270 320 250 256 250 C190 250 130 270 116 300 Z", fill=EARTH_D)
    tree(s, 90, 150, 0.5)
    tree(s, 420, 460, 0.6)
    s.M("M60 430 l20 -10 M430 130 l20 10", GRASS_D, 6)
    end(s)


@reg("swamp")
def _(s):
    tile(s, "#CFE3C0")
    s.F("rect", x=0, y=330, width=512, height=200, fill="#5E8A6A")
    for x, k in ((130, 1.0), (360, 1.2)):
        s.F("path", d=f"M{x - 20 * k:.0f} 360 L{x - 10 * k:.0f} 180 H{x + 10 * k:.0f} L{x + 20 * k:.0f} 360 Z", fill="#6E5A44")
        s.M(f"M{x - 20 * k:.0f} 360 l-20 20 M{x + 20 * k:.0f} 360 l20 20 M{x} 360 v24", "#6E5A44", 10)
        s.F("ellipse", cx=x, cy=170, rx=90 * k, ry=50 * k, fill="#6E9A4A")
        s.M(f"M{x - 50 * k:.0f} 190 v50 M{x + 40 * k:.0f} 196 v60", "#9DBA6A", 6)
    s.M("M60 420 h60 M240 450 h70 M400 430 h50", "#8FB89A", 6)
    s.F("ellipse", cx=250, cy=400, rx=34, ry=12, fill="#4E7A3A")
    s.F("circle", cx=232, cy=392, r=6, fill=YELLOW)
    end(s)


@reg("marsh")
def _(s):
    tile(s)
    s.F("rect", x=0, y=330, width=512, height=190, fill=WATER)
    s.M("M60 400 h50 M300 430 h60 M180 470 h40", WHITE, 6)
    for cx, n, top in ((100, 5, 170), (250, 6, 130), (410, 5, 180)):
        for i in range(n):
            off = (i - (n - 1) / 2) * 16
            tip_x, tip_y = cx + off * 3.2, top + abs(off) * 2.4
            s.T(f"M{cx + off:.0f} 380 Q{cx + off * 1.5:.0f} {(380 + tip_y) / 2:.0f} {tip_x:.0f} {tip_y:.0f}", GRASS_D if i % 2 else GRASS, 8)
        for i in (1, n - 2):
            off = (i - (n - 1) / 2) * 16
            x = cx + off * 1.4
            s.T(f"M{cx + off:.0f} 380 L{x:.0f} {top + 10:.0f}", "#7A8A4A", 5)
            s.F("rect", x=f"{x - 9:.0f}", y=top - 30, width=18, height=48, rx=9, fill=EARTH)
        s.F("ellipse", cx=cx, cy=384, rx=n * 12, ry=12, fill=GRASS_D)
    end(s)


@reg("floodplain")
def _(s):
    tile(s)
    sun(s, 410, 90, 32)
    s.F("rect", x=0, y=160, width=512, height=360, fill=GRASS)
    s.F("path", d="M0 280 C120 250 200 330 300 300 C400 270 450 310 512 300 V400 C450 410 400 370 300 400 C200 430 120 350 0 380 Z", fill=WATER_L)
    s.F("path", d="M0 320 C120 290 200 370 300 340 C400 310 450 350 512 340 V360 C450 370 400 330 300 360 C200 390 120 310 0 340 Z", fill=WATER_D)
    for x in (90, 410):
        s.F("rect", x=x - 30, y=200, width=60, height=40, fill=WHITE)
        s.F("polygon", points=f"{x - 40},{204} {x},{170} {x + 40},{204}", fill=RED)
    end(s)


@reg("meander")
def _(s):
    tile(s, GRASS)
    s.T("M40 0 C40 120 200 100 200 180 C200 260 60 240 60 330 C60 420 260 420 300 340 C340 260 460 300 460 380 C460 450 380 470 400 512", WATER, 34)
    s.T("M370 150 C420 110 480 140 460 200 C440 250 370 230 366 196", WATER, 22)
    tree(s, 330, 470, 0.5)
    tree(s, 120, 120, 0.5)
    end(s)


# ---------------------------------------------------------------- earth layers
CRUST, MANTLE, OUTER, INNER = "#9A6A3A", "#E8743B", "#F5A623", "#FFD84D"
PALE = {CRUST: "#D9C3A8", MANTLE: "#F4C3A6", OUTER: "#F8DCAE", INNER: "#FFF0B8"}


def wedge(s, cx, cy, r, a0, a1, fill, outline=True):
    x0, y0 = arc_pt(cx, cy, r, a0)
    x1, y1 = arc_pt(cx, cy, r, a1)
    big = 1 if (a1 - a0) % 360 > 180 else 0
    s.F("path", outline=outline, d=f"M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {big} 1 {x1:.1f} {y1:.1f} Z", fill=fill)


def earth_cut(s, hi=None):
    """Earth with a quarter cut away to show crust, mantle, outer core and inner core."""
    cx, cy = 246, 266
    s.F("circle", cx=cx, cy=cy, r=200, fill=SEA)
    for d in ("M90 200 C120 140 190 120 220 150 C240 180 200 210 170 230 C140 250 100 250 90 200 Z",
              "M110 330 C150 300 200 320 210 360 C220 400 180 440 140 420 C110 400 90 360 110 330 Z",
              "M250 380 C290 360 340 380 350 420 C320 450 270 450 250 380 Z"):
        s.F("path", d=d, fill=GRASS)
    layers = ((CRUST, 200), (MANTLE, 184), (OUTER, 110), (INNER, 56))
    for c, r in layers:
        fill = c if hi in (None, c) else PALE[c]
        wedge(s, cx, cy, r, -90, 0, fill)
    if hi:
        r = dict(layers)[hi]
        inner = {CRUST: 184, MANTLE: 110, OUTER: 56, INNER: 0}[hi]
        x, y = arc_pt(cx, cy, (r + inner) / 2, -45)
        tag_arrow(s, x, y, -45)


@reg("layers-of-the-earth")
def _(s):
    earth_cut(s)


for _id, _c in (("crust", CRUST), ("mantle", MANTLE), ("outer-core", OUTER), ("inner-core", INNER)):
    D[_id] = (lambda c: lambda s: earth_cut(s, c))(_c)


def blob_path(cx, cy, pts, k=1.0):
    """Smooth closed path through relative points (x, y) around (cx, cy)."""
    p = [(cx + x * k, cy + y * k) for x, y in pts]
    n = len(p)
    d = f"M{(p[0][0] + p[-1][0]) / 2:.0f} {(p[0][1] + p[-1][1]) / 2:.0f}"
    for i in range(n):
        a, b = p[i], p[(i + 1) % n]
        d += f" Q{a[0]:.0f} {a[1]:.0f} {(a[0] + b[0]) / 2:.0f} {(a[1] + b[1]) / 2:.0f}"
    return d + " Z"


CONTS = ([(-130, -90), (-60, -140), (0, -110), (-10, -60), (-60, -30), (-100, -10)],
         [(-60, 30), (0, 40), (10, 100), (-30, 170), (-60, 110)],
         [(40, -140), (130, -130), (175, -70), (130, -20), (60, -10), (30, -70)],
         [(70, 60), (140, 50), (150, 100), (90, 120)])


LANDS = ("M90 120 C120 90 190 80 220 100 C240 120 210 150 190 160 C170 175 175 200 160 215 C145 225 120 210 110 190 C95 170 75 145 90 120 Z",
         "M180 260 C210 250 240 270 238 300 C236 340 210 380 195 420 C180 400 172 360 168 330 C162 300 160 270 180 260 Z",
         "M290 110 C320 96 360 100 370 120 C376 140 350 150 330 150 C310 152 290 140 290 110 Z",
         "M290 180 C330 166 380 180 392 220 C400 260 370 290 350 330 C335 360 320 380 310 380 C300 350 300 320 290 290 C270 260 262 200 290 180 Z",
         "M240 80 C260 70 280 76 276 92 C270 104 250 106 240 80 Z")


def globe2(s, cx=256, cy=256, r=200, ocean=SEA, land=GRASS):
    s.open(transform=f"translate({cx} {cy}) scale({r / 200:.3f}) translate(-256 -256)")
    s.F("circle", cx=256, cy=256, r=200, fill=ocean)
    for d in LANDS:
        s.F("path", d=d, fill=land)
    s.close()


@reg("tectonic-plates")
def _(s):
    globe2(s)
    for d in ("M70 200 L130 220 L170 190 L230 230 L300 200 L360 240 L440 220", "M230 230 L220 300 L250 360 L230 450",
              "M300 200 L320 120 L290 70", "M360 240 L380 330 L430 370"):
        s.M(d, RED, 12)
    for x, y, a in ((180, 300, 180), (290, 300, 0), (330, 150, -90), (420, 290, 90)):
        s.T(head(x, y, a, 30, 40), YELLOW, 10)


@reg("fault-line")
def _(s):
    def block(x, y, w, h, top):
        s.F("path", d=f"M{x} {y} L{x + 90} {y - 60} H{x + 90 + w} L{x + w} {y} Z", fill=top)
        s.F("rect", x=x, y=y, width=w, height=h, fill=EARTH)
        s.F("path", d=f"M{x + w} {y} L{x + w + 90} {y - 60} V{y + h - 60} L{x + w} {y + h} Z", fill=EARTH_D)
        for i, c in enumerate((RED_RL, SAND, RED_RL)):
            yy = y + 30 + i * 50
            s.F("rect", outline=False, x=x + 2, y=yy, width=w - 4, height=18, fill=c)
    block(40, 230, 190, 220, GRASS)
    block(250, 180, 160, 220, GRASS)
    s.M("M236 120 L244 160 L234 200 L246 240 L238 300 L248 400", RED, 10)
    s.T(head(130, 200, -90, 34, 40), RED, 10)
    s.T(head(360, 150, 90, 34, 40), RED, 10)


@reg("continental-drift")
def _(s):
    s.F("circle", cx=140, cy=256, r=110, fill=SEA)
    s.F("path", d=blob_path(140, 256, [(-60, -50), (0, -80), (60, -40), (50, 30), (10, 70), (-50, 40)]), fill=GRASS)
    s.T("M262 256 H300", DARK, 14)
    s.T(head(310, 256, 0, 26, 40), DARK, 14)
    s.F("circle", cx=400, cy=256, r=100, fill=SEA)
    for c in ([(-70, -60), (-30, -70), (-20, -30), (-60, -20)], [(-40, 10), (-10, 20), (-20, 70), (-50, 50)],
              [(10, -70), (70, -50), (60, -10), (20, -20)], [(30, 20), (70, 30), (60, 60)]):
        s.F("path", d=blob_path(400, 256, c), fill=GRASS)


# ---------------------------------------------------------------- volcanoes and quakes
LAVA, LAVA_D, LAVA_L, ASH, ASH_D = "#F0592A", "#C23A1C", "#FFB13B", "#9A9AA4", "#6E6E78"


def cone(s, top=200, snow=False, green=False, crater=True):
    s.F("path", d=f"M0 470 L190 {top} H322 L512 470 Z", fill=GRASS if green else "#8C6A52")
    s.F("path", outline=False, d=f"M300 {top + 6} H318 L500 466 H420 Z", fill=GRASS_D if green else "#6E5240")
    if snow:
        s.F("path", d=f"M190 {top} H322 L350 {top + 50} L320 {top + 40} L290 {top + 60} L256 {top + 40} L220 {top + 60} L190 {top + 40} L162 {top + 50} Z", fill=SNOW)
    if crater:
        s.F("ellipse", cx=256, cy=top, rx=66, ry=14, fill="#3A2A22")


@reg("volcano")
def _(s):
    tile(s)
    cone(s, 220)
    for x, y, r in ((250, 170, 30), (280, 130, 38), (250, 84, 44)):
        s.F("circle", cx=x, cy=y, r=r, fill=ASH)
    ground(s, 460, GRASS, 6)
    end(s)


@reg("erupting-volcano")
def _(s):
    tile(s, "#FFD9C2")
    for x, y, r in ((200, 110, 50), (300, 90, 60), (380, 130, 40), (130, 140, 36)):
        s.F("circle", cx=x, cy=y, r=r, fill=ASH_D)
    s.F("path", d="M210 230 C200 170 230 140 256 120 C282 140 312 170 302 230 Z", fill=LAVA)
    cone(s, 230)
    s.F("path", d="M210 230 C190 300 150 340 160 400 C190 360 220 300 240 236 Z", fill=LAVA)
    s.F("path", d="M290 232 C300 290 330 330 350 420 C370 380 330 300 306 232 Z", fill=LAVA)
    s.F("ellipse", cx=256, cy=230, rx=66, ry=14, fill=LAVA_L)
    for x, y in ((160, 170), (350, 180), (210, 80), (320, 60)):
        s.F("circle", cx=x, cy=y, r=12, fill=LAVA_L)
    ground(s, 460, "#6E5240", 6)
    end(s)


@reg("dormant-volcano")
def _(s):
    tile(s)
    cloud(s, 120, 110, 0.6)
    cone(s, 190, snow=True, green=True, crater=False)
    for x in (90, 150, 400, 440):
        tree(s, x, 470, 0.6, "pine")
    end(s)


@reg("lava")
def _(s):
    tile(s, "#3A2A2A")
    s.F("path", d="M0 120 C120 160 200 100 300 160 C380 200 440 160 512 190 V512 H0 Z", fill=LAVA)
    s.F("path", outline=False, d="M0 220 C140 250 240 200 340 260 C420 300 470 270 512 290 V330 C460 310 400 340 330 300 C240 250 140 290 0 260 Z", fill=LAVA_L)
    for d in ("M40 320 L100 300 L160 340 L220 330", "M260 380 L330 360 L380 400 L460 380", "M80 430 L150 420 L200 450", "M300 460 L360 440 L430 470"):
        s.M(d, "#2E1A14", 14)
    for x, y in ((180, 230), (380, 220), (90, 380), (420, 330)):
        s.F("circle", cx=x, cy=y, r=10, fill=YELLOW)
    end(s)


@reg("magma-chamber")
def _(s):
    tile(s)
    s.F("rect", x=0, y=260, width=512, height=260, fill=EARTH)
    cone(s, 150)
    s.F("rect", outline=False, x=0, y=300, width=512, height=220, fill=EARTH)
    s.M("M0 300 H512", INK, 10)
    for y in (340, 400):
        s.M(f"M0 {y} C120 {y - 10} 380 {y + 10} 512 {y}", EARTH_D, 8)
    s.F("ellipse", cx=256, cy=440, rx=140, ry=50, fill=LAVA)
    s.F("path", d="M236 150 V400 H276 V150 Z", fill=LAVA)
    s.F("ellipse", cx=256, cy=150, rx=60, ry=12, fill=LAVA_L)
    end(s)


@reg("volcanic-ash-cloud")
def _(s):
    tile(s)
    cone(s, 300)
    for x, y, r in ((256, 260, 50), (210, 200, 60), (300, 190, 66), (170, 120, 70), (330, 110, 80), (250, 90, 70), (420, 140, 50), (90, 160, 50)):
        s.F("circle", cx=x, cy=y, r=r, fill=ASH if (x + y) % 3 else ASH_D)
    ground(s, 470, GRASS, 6)
    end(s)


@reg("lava-lamp-volcano-diagram")
def _(s):
    tile(s, SKY)
    s.F("path", d="M20 430 L200 130 H312 L492 430 Z", fill="#8C6A52")
    for i, c in enumerate(("#A47D62", "#7D5C48", "#A47D62")):
        y = 220 + i * 70
        w = (y - 130) * 0.6 + 56
        s.F("path", outline=False, d=f"M{256 - w - 40:.0f} {y} H{256 + w + 40:.0f} L{256 + w + 50:.0f} {y + 30} H{256 - w - 50:.0f} Z", fill=c)
    s.F("rect", x=0, y=430, width=512, height=90, fill=EARTH_D)
    s.F("ellipse", cx=256, cy=460, rx=120, ry=36, fill=LAVA)
    s.F("path", d="M238 130 V440 H274 V130 Z", fill=LAVA)
    s.T("M270 300 L360 260", LAVA, 18)
    for x, y, r in ((256, 90, 34), (226, 60, 26), (290, 56, 28)):
        s.F("circle", cx=x, cy=y, r=r, fill=ASH)
    end(s)


def house(s, x, y, k=1.0, rot=0, wall=WHITE, roof=RED):
    s.open(transform=f"rotate({rot} {x} {y})")
    s.F("rect", x=f"{x - 50 * k:.0f}", y=f"{y - 70 * k:.0f}", width=f"{100 * k:.0f}", height=f"{70 * k:.0f}", fill=wall)
    s.F("polygon", points=f"{x - 64 * k:.0f},{y - 66 * k:.0f} {x:.0f},{y - 120 * k:.0f} {x + 64 * k:.0f},{y - 66 * k:.0f}", fill=roof)
    s.F("rect", x=f"{x - 12 * k:.0f}", y=f"{y - 40 * k:.0f}", width=f"{24 * k:.0f}", height=f"{40 * k:.0f}", fill=A1)
    s.close()


@reg("earthquake")
def _(s):
    tile(s)
    s.F("path", d="M0 360 H240 L260 380 L250 400 L272 430 L260 520 H0 Z", fill=EARTH)
    s.F("path", d="M512 340 H270 L288 370 L276 400 L296 430 L284 520 H512 Z", fill=EARTH)
    s.F("path", d="M0 360 H240 L248 370 H0 Z M512 340 H270 L276 350 H512 Z", fill=GRASS)
    house(s, 140, 358, 1.2, -8)
    house(s, 390, 338, 1.1, 10)
    for x in (60, 452):
        s.M(f"M{x} 160 l-16 20 l16 20 l-16 20", DARK, 8)
    s.M("M200 140 l-14 16 l14 16 M330 120 l14 16 l-14 16", DARK, 8)
    end(s)


@reg("seismograph")
def _(s):
    s.F("rect", x=40, y=330, width=432, height=110, rx=18, fill=MID)
    s.F("rect", x=70, y=180, width=372, height=150, rx=10, fill=WHITE)
    s.M("M80 255 H150 L170 220 L185 300 L200 190 L220 320 L240 210 L255 290 L270 240 L290 262 H430", RED, 7)
    s.T("M300 120 V170", DARK, 12)
    s.T("M300 120 H400", DARK, 12)
    s.F("circle", cx=290, cy=258, r=10, fill=DARK)
    s.T("M290 258 L300 170", DARK, 6)
    for x in (110, 400):
        s.F("circle", cx=x, cy=386, r=24, fill=DARK)


@reg("richter-scale")
def _(s):
    cols = ("#4CB963", "#A6D04A", "#FFC83D", "#F5913E", "#E5484D", "#B5323A")
    for i, c in enumerate(cols):
        wedge(s, 256, 360, 210, 180 + i * 30, 180 + (i + 1) * 30, c)
    s.F("circle", cx=256, cy=360, r=110, fill=WHITE)
    s.F("rect", outline=False, x=30, y=362, width=452, height=60, fill=WHITE)
    s.M("M46 360 H466", INK, 10)
    x, y = arc_pt(256, 360, 180, -40)
    s.T(f"M256 360 L{x:.0f} {y:.0f}", DARK, 14)
    s.F("circle", cx=256, cy=360, r=26, fill=DARK)


@reg("crack-in-the-ground")
def _(s):
    tile(s, GRASS)
    s.F("path", d="M60 40 L150 120 L130 180 L220 250 L200 320 L300 380 L290 440 L380 520 L400 520 L310 430 L330 370 L230 300 L250 240 L170 170 L190 110 L90 40 Z", fill="#3A2A22")
    s.M("M150 120 L100 150 M220 250 L280 230 M300 380 L250 410", "#3A2A22", 8)
    end(s)


@reg("tsunami")
def _(s):
    tile(s)
    ground(s, 430, SAND, 4)
    house(s, 380, 440, 0.8)
    house(s, 470, 440, 0.6)
    s.F("path", d="M-10 520 V300 C0 160 120 70 250 80 C350 90 400 160 370 220 C340 260 280 230 290 190 C300 150 250 140 220 170 C180 210 240 330 300 420 L320 520 Z", fill=WATER_D)
    s.F("path", outline=False, d="M250 96 C340 100 386 160 362 210 C340 240 300 226 300 196 C310 150 270 120 230 130 Z", fill=WHITE)
    s.M("M60 300 C100 250 150 240 190 260 M40 400 C90 360 140 350 180 370", WATER_L, 8)
    end(s)


@reg("landslide")
def _(s):
    tile(s)
    s.F("path", d="M0 100 L300 470 H0 Z", fill=GRASS)
    s.F("path", d="M60 170 C120 250 200 330 300 470 H90 C110 380 60 280 60 170 Z", fill="#8C6A52")
    for x, y, r in ((180, 340, 24), (240, 410, 30), (300, 450, 26), (130, 300, 18), (350, 460, 20)):
        s.F("circle", cx=x, cy=y, r=r, fill=ROCK)
    ground(s, 470, GRASS_D, 0)
    house(s, 420, 470, 0.8)
    for y in (220, 300):
        s.T(head(200, y + 20, 50, 26, 40), DARK, 8)
    end(s)


@reg("ring-of-fire")
def _(s):
    s.F("circle", cx=256, cy=256, r=210, fill=SEA)
    s.F("path", d=blob_path(256, 256, [(-200, -150), (-120, -190), (-110, -100), (-160, -20), (-150, 80), (-200, 120)]), fill=GRASS)
    s.F("path", d=blob_path(256, 256, [(140, -190), (200, -120), (180, 20), (130, 120), (100, 40), (120, -80)]), fill=GRASS)
    s.F("path", d=blob_path(256, 256, [(-60, 120), (40, 110), (60, 170), (-30, 190)]), fill=GRASS)
    for a in range(-160, 180, 22):
        if -20 < a < 20:
            continue
        rr = 150 if abs(a) > 90 else 140
        x, y = arc_pt(256, 256, rr, a + 90)
        s.F("polygon", points=f"{x - 14:.0f},{y + 10:.0f} {x:.0f},{y - 14:.0f} {x + 14:.0f},{y + 10:.0f}", fill=LAVA)


# ---------------------------------------------------------------- rocks and minerals
CHUNK = [(-150, 100), (-170, 10), (-110, -80), (0, -110), (110, -80), (170, 0), (150, 100), (60, 130), (-60, 130)]


def rock(s, c=ROCK, shade=ROCK_D, cx=256, cy=280, k=1.0):
    pts = " ".join(f"{cx + x * k:.0f},{cy + y * k:.0f}" for x, y in CHUNK)
    s.F("polygon", points=pts, fill=c)
    s.F("polygon", outline=False, points=f"{cx + 110 * k:.0f},{cy - 80 * k:.0f} {cx + 170 * k:.0f},{cy:.0f} {cx + 150 * k:.0f},{cy + 100 * k:.0f} {cx + 60 * k:.0f},{cy + 130 * k:.0f} {cx + 40 * k:.0f},{cy + 20 * k:.0f}", fill=shade)
    s.M(f"M{cx - 110 * k:.0f} {cy - 80 * k:.0f} L{cx + 40 * k:.0f} {cy + 20 * k:.0f} L{cx + 110 * k:.0f} {cy - 80 * k:.0f} M{cx + 40 * k:.0f} {cy + 20 * k:.0f} L{cx + 60 * k:.0f} {cy + 130 * k:.0f}", INK, 6)
    return pts


def clip_rock(s, name, c, shade, inner, cx=256, cy=280, k=1.0):
    """Rock with a pattern (inner(s) draws it) clipped to the rock outline."""
    pts = rock(s, c, shade, cx, cy, k)
    cid = f"r-{_cur[0]}-{name}"
    s.raw(f'<defs><clipPath id="{cid}"><polygon points="{pts}"/></clipPath></defs>')
    s.raw(f'<g clip-path="url(#{cid})">')
    inner(s)
    s.raw("</g>")
    s.F("polygon", points=pts, fill="none")


def speckle(s, colors, n=40, seed=3):
    x = seed
    for i in range(n):
        x = (x * 73 + 41) % 997
        y = (x * 31 + 17) % 991
        s.F("circle", outline=False, cx=90 + x % 330, cy=160 + y % 250, r=5 + (x % 7), fill=colors[i % len(colors)])


@reg("rock")
def _(s):
    rock(s)


@reg("igneous-rock")
def _(s):
    clip_rock(s, "a", "#5A5560", "#3F3B45", lambda s: speckle(s, ("#C9C2D0", "#2B2830", "#E8A0A0"), 50))


@reg("sedimentary-rock")
def _(s):
    def bands(s):
        for i, c in enumerate(("#E8C99A", "#C9A26A", "#EAD8B0", "#B8884E", "#E0BE86", "#C9A26A")):
            s.F("rect", outline=False, x=60, y=150 + i * 44, width=400, height=44, fill=c)
            s.M(f"M60 {150 + i * 44} H460", "#8C6A42", 4)
    clip_rock(s, "a", "#E0BE86", "#B8884E", bands)


@reg("metamorphic-rock")
def _(s):
    def folds(s):
        for i in range(8):
            y = 150 + i * 34
            s.M(f"M60 {y} C140 {y - 40} 200 {y + 40} 280 {y} C360 {y - 40} 400 {y + 30} 470 {y}", "#4A4A5A" if i % 2 else "#D8D8E0", 14)
    clip_rock(s, "a", "#8A8A9A", "#6A6A7A", folds)


@reg("rock-cycle")
def _(s):
    for (cx, cy), c, sh in (((256, 120), "#5A5560", "#3F3B45"), ((130, 360), "#E0BE86", "#B8884E"), ((382, 360), "#8A8A9A", "#6A6A7A")):
        rock(s, c, sh, cx, cy, 0.48)
    for d, a, x, y in (("M330 120 C410 140 440 220 420 280", 110, 420, 280), ("M300 400 H212", 180, 212, 400), ("M92 290 C70 220 110 150 180 128", -20, 180, 128)):
        s.T(d, A1, 14)
        s.T(head(x, y, a, 30, 40), A1, 14)


@reg("granite")
def _(s):
    clip_rock(s, "a", "#E8C8C0", "#C9A8A0", lambda s: speckle(s, ("#2B2830", "#FFFFFF", "#9A8A88", "#F2A9A0"), 70))


@reg("marble")
def _(s):
    def veins(s):
        for d in ("M80 200 C160 220 200 300 300 290 C360 280 400 340 460 330", "M120 380 C200 340 260 380 340 360", "M200 150 C220 200 260 220 280 260"):
            s.M(d, "#A8A8B8", 6)
    clip_rock(s, "a", "#F6F6FA", "#DCDCE6", veins)


@reg("limestone")
def _(s):
    def shells(s):
        for x, y in ((150, 230), (260, 200), (340, 300), (200, 340), (300, 380), (120, 320)):
            s.M(f"M{x} {y} a14 14 0 1 1 14 14 a8 8 0 1 1 -8 -8", "#B8A880", 5)
    clip_rock(s, "a", "#EFE6CC", "#D6C9A6", shells)


@reg("sandstone")
def _(s):
    def lines(s):
        for i in range(7):
            y = 160 + i * 38
            s.M(f"M60 {y} C200 {y + 10} 320 {y - 10} 470 {y}", "#C47A4A", 5)
        speckle(s, ("#F4C49A", "#B8683A"), 40, 7)
    clip_rock(s, "a", "#E89A68", "#C47A4A", lines)


@reg("basalt")
def _(s):
    for i, (x, h) in enumerate(((120, 220), (190, 280), (260, 250), (330, 300), (400, 200))):
        top = 440 - h
        s.F("rect", x=x - 34, y=top, width=68, height=h, fill="#4A4752" if i % 2 else "#5A5662")
        s.F("polygon", points=f"{x - 34},{top} {x - 18},{top - 14} {x + 18},{top - 14} {x + 34},{top} {x + 18},{top + 14} {x - 18},{top + 14}", fill="#7A7684")


@reg("obsidian")
def _(s):
    s.F("polygon", points="110,380 150,200 260,120 400,180 420,320 330,420 190,430", fill="#1F1C26")
    s.F("polygon", outline=False, points="260,120 400,180 300,260", fill="#3A3646")
    s.F("polygon", outline=False, points="150,200 260,120 230,200 170,260", fill="#4A4658")
    s.M("M190 230 L240 170 M330 220 L380 200", "#8A86A0", 8)


@reg("pumice")
def _(s):
    def holes(s):
        x = 5
        for i in range(55):
            x = (x * 61 + 29) % 983
            y = (x * 37 + 11) % 977
            s.F("ellipse", outline=False, cx=90 + x % 330, cy=160 + y % 250, rx=6 + x % 9, ry=4 + x % 6, fill="#A8A49C")
    clip_rock(s, "a", "#DEDAD0", "#C6C2B6", holes)


@reg("slate")
def _(s):
    for i, (x, y, c) in enumerate(((120, 360, "#4A5568"), (140, 300, "#5A6578"), (110, 240, "#4A5568"), (150, 180, "#647086"))):
        s.F("polygon", points=f"{x},{y} {x + 260},{y - 10} {x + 290},{y + 40} {x + 20},{y + 52}", fill=c)


def crystal(s, x, y, w, h, c, cl, rot=0):
    s.open(transform=f"rotate({rot} {x} {y})")
    s.F("polygon", points=f"{x - w / 2:.0f},{y:.0f} {x - w / 2:.0f},{y - h:.0f} {x:.0f},{y - h - w * 0.8:.0f} {x + w / 2:.0f},{y - h:.0f} {x + w / 2:.0f},{y:.0f}", fill=c)
    s.F("polygon", outline=False, points=f"{x - w / 2 + 6:.0f},{y - 6:.0f} {x - w / 2 + 6:.0f},{y - h:.0f} {x - 2:.0f},{y - h - w * 0.6:.0f} {x - 2:.0f},{y - 6:.0f}", fill=cl)
    s.close()


def cluster(s, c, cl, base=ROCK):
    s.F("ellipse", cx=256, cy=420, rx=170, ry=40, fill=base)
    for x, w, h, r in ((180, 60, 150, -22), (330, 56, 140, 20), (256, 80, 230, 0), (210, 46, 90, -40), (310, 44, 90, 38)):
        crystal(s, x, 420, w, h, c, cl, r)


@reg("quartz")
def _(s):
    cluster(s, "#EEF4FA", WHITE)


@reg("mica")
def _(s):
    for i in range(6):
        y = 340 - i * 30
        s.F("polygon", points=f"{130 + i * 6},{y} {360 - i * 4},{y - 14} {400 - i * 6},{y + 20} {160 + i * 4},{y + 34}", fill="#D9B96A" if i % 2 else "#C9A458")
    s.F("polygon", outline=False, points="200,200 300,190 320,206 220,214", fill="#F4E2A8")


@reg("gypsum")
def _(s):
    s.F("ellipse", cx=256, cy=420, rx=150, ry=34, fill=SAND)
    for x, h, r in ((190, 220, -24), (256, 280, 0), (320, 230, 22), (230, 160, -48), (290, 170, 46)):
        s.open(transform=f"rotate({r} {x} 420)")
        s.F("polygon", points=f"{x - 22},{420} {x - 14},{420 - h} {x},{420 - h - 20} {x + 14},{420 - h} {x + 22},{420}", fill="#F6F2EA")
        s.close()


@reg("calcite")
def _(s):
    s.F("polygon", points="140,330 220,170 400,150 360,330 180,380", fill="#F7B26A")
    s.F("polygon", outline=False, points="220,170 400,150 360,330 270,240", fill="#E8964A")
    s.M("M220 170 L270 240 L360 330 M270 240 L180 380", INK, 6)
    s.F("polygon", outline=False, points="190,300 230,210 250,230 210,320", fill="#FCD6A6")


@reg("gold-nugget")
def _(s):
    s.F("path", d=blob_path(256, 280, [(-150, 30), (-110, -80), (-20, -110), (60, -70), (150, -60), (160, 40), (80, 110), (-60, 100)]), fill=C["gold"])
    s.F("path", outline=False, d=blob_path(256, 280, [(-110, -10), (-80, -70), (-20, -80), (0, -40), (-60, -10)]), fill=YELLOW)
    s.F("path", outline=False, d=blob_path(256, 280, [(60, 20), (140, 0), (130, 70), (70, 90)]), fill=C["darkgold"])
    for x, y in ((200, 220), (320, 240), (240, 330)):
        s.F("circle", outline=False, cx=x, cy=y, r=8, fill="#FFF3B0")


@reg("silver-ore")
def _(s):
    def veins(s):
        for d in ("M80 250 C160 230 220 300 300 270 C360 250 420 300 470 280", "M140 360 C200 340 280 380 360 350"):
            s.M(d, "#E8ECF2", 20)
            s.M(d, "#B8C0CC", 6)
    clip_rock(s, "a", "#5A5662", "#423E4A", veins)


@reg("iron-ore")
def _(s):
    def spots(s):
        speckle(s, ("#3A3A44", "#8A3A24", "#5A5A66"), 45, 11)
    clip_rock(s, "a", "#A0522D", "#7A3A20", spots)


@reg("copper-ore")
def _(s):
    def spots(s):
        for x, y, r in ((170, 220, 40), (300, 300, 50), (220, 360, 30), (360, 200, 30)):
            s.F("circle", outline=False, cx=x, cy=y, r=r, fill="#2FA67A")
            s.F("circle", outline=False, cx=x + 8, cy=y + 6, r=r * 0.5, fill="#45C8A0")
        for x, y in ((260, 220), (140, 320), (380, 320)):
            s.F("circle", outline=False, cx=x, cy=y, r=16, fill="#C8743A")
    clip_rock(s, "a", "#6A5A50", "#4E4038", spots)


@reg("geode")
def _(s):
    s.F("path", d=blob_path(256, 266, [(-180, 0), (-150, -130), (0, -190), (150, -130), (180, 0), (150, 140), (0, 190), (-150, 140)]), fill="#A89A8A")
    s.F("path", d=blob_path(256, 266, [(-140, 0), (-110, -100), (0, -150), (110, -100), (140, 0), (110, 110), (0, 150), (-110, 110)]), fill=WHITE)
    s.F("path", d=blob_path(256, 266, [(-110, 0), (-84, -76), (0, -116), (84, -76), (110, 0), (84, 84), (0, 116), (-84, 84)]), fill="#8B5CF6")
    for a in range(0, 360, 30):
        x, y = arc_pt(256, 266, 90, a)
        x2, y2 = arc_pt(256, 266, 50, a + 8)
        s.F("polygon", outline=False, points=f"{x:.0f},{y:.0f} {x2:.0f},{y2:.0f} {arc_pt(256, 266, 90, a + 16)[0]:.0f},{arc_pt(256, 266, 90, a + 16)[1]:.0f}", fill="#C4A8FF")
    s.F("circle", cx=256, cy=266, r=34, fill="#5B33C2")


# ---------------------------------------------------------------- gems
def brilliant(s, c, cl, cd, cx=256, cy=256, k=1.0):
    def P(*pts):
        return " ".join(f"{cx + x * k:.0f},{cy + y * k:.0f}" for x, y in pts)
    s.F("polygon", points=P((-70, -90), (70, -90), (150, -30), (0, 170), (-150, -30)), fill=c)
    s.F("polygon", outline=False, points=P((-70, -90), (70, -90), (40, -30), (-40, -30)), fill=cl)
    s.F("polygon", outline=False, points=P((-150, -30), (-40, -30), (0, 170)), fill=cl)
    s.F("polygon", outline=False, points=P((150, -30), (40, -30), (0, 170)), fill=cd)
    s.M(f"M{cx - 150 * k:.0f} {cy - 30 * k:.0f} H{cx + 150 * k:.0f} M{cx - 70 * k:.0f} {cy - 90 * k:.0f} L{cx - 40 * k:.0f} {cy - 30 * k:.0f} L{cx:.0f} {cy + 170 * k:.0f} L{cx + 40 * k:.0f} {cy - 30 * k:.0f} L{cx + 70 * k:.0f} {cy - 90 * k:.0f}", INK, 6)
    s.F("polygon", outline=False, points=P((-50, -80), (-20, -80), (-40, -50)), fill=WHITE)


def oval_cut(s, c, cl, cd, rx=150, ry=190):
    s.F("ellipse", cx=256, cy=256, rx=rx, ry=ry, fill=c)
    s.F("ellipse", outline=False, cx=256, cy=256, rx=rx * 0.5, ry=ry * 0.5, fill=cl)
    for a in range(0, 360, 45):
        x1, y1 = 256 + rx * 0.5 * math.cos(math.radians(a)), 256 + ry * 0.5 * math.sin(math.radians(a))
        x2, y2 = 256 + rx * math.cos(math.radians(a + 22)), 256 + ry * math.sin(math.radians(a + 22))
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", cd, 5)
    s.F("ellipse", cx=256, cy=256, rx=rx * 0.5, ry=ry * 0.5, fill="none")
    s.F("ellipse", outline=False, cx=226, cy=200, rx=20, ry=30, fill=WHITE, opacity="0.8")


def step_cut(s, c, cl, cd, w=280, h=360):
    def octa(w, h, cut):
        x0, y0 = 256 - w / 2, 256 - h / 2
        return (f"{x0 + cut:.0f},{y0:.0f} {x0 + w - cut:.0f},{y0:.0f} {x0 + w:.0f},{y0 + cut:.0f} {x0 + w:.0f},{y0 + h - cut:.0f} "
                f"{x0 + w - cut:.0f},{y0 + h:.0f} {x0 + cut:.0f},{y0 + h:.0f} {x0:.0f},{y0 + h - cut:.0f} {x0:.0f},{y0 + cut:.0f}")
    s.F("polygon", points=octa(w, h, 50), fill=c)
    s.F("polygon", outline=False, points=octa(w - 60, h - 60, 34), fill=cd)
    s.F("polygon", points=octa(w - 120, h - 120, 20), fill=cl)
    s.M(f"M{256 - w / 2 + 50:.0f} {256 - h / 2:.0f} L{256 - w / 2 + 80:.0f} {256 - h / 2 + 60:.0f}", INK, 5)
    s.F("polygon", outline=False, points=f"{256 - w / 2 + 70:.0f},{256 - h / 2 + 70:.0f} {256 - w / 2 + 100:.0f},{256 - h / 2 + 70:.0f} {256 - w / 2 + 70:.0f},{256 - h / 2 + 130:.0f}", fill=WHITE)


@reg("gemstone")
def _(s):
    brilliant(s, "#E5484D", "#F7A1A5", "#B5323A", 170, 300, 0.6)
    brilliant(s, "#3D8BFD", "#9CC4FF", "#2C5FC9", 350, 320, 0.55)
    brilliant(s, "#4CB963", "#A6E0B2", "#2F8A4A", 260, 170, 0.6)


@reg("diamond")
def _(s):
    brilliant(s, "#D8F0FF", WHITE, "#9CCFF0")
    for x, y in ((420, 110), (90, 150), (430, 380)):
        s.F("polygon", points=star_pts(x, y, 26, 8, 4), fill=YELLOW)


@reg("ruby")
def _(s):
    oval_cut(s, "#D8263A", "#F06A78", "#9A1424")


@reg("emerald")
def _(s):
    step_cut(s, "#21A35A", "#7FDCA0", "#137A40")


@reg("sapphire")
def _(s):
    s.F("rect", x=86, y=86, width=340, height=340, rx=90, fill="#2C5FC9")
    s.F("rect", outline=False, x=166, y=166, width=180, height=180, rx=40, fill="#6A9CF0")
    for x1, y1, x2, y2 in ((166, 166, 110, 110), (346, 166, 402, 110), (166, 346, 110, 402), (346, 346, 402, 402), (256, 166, 256, 90), (256, 346, 256, 422), (166, 256, 90, 256), (346, 256, 422, 256)):
        s.M(f"M{x1} {y1} L{x2} {y2}", "#1E3A8A", 5)
    s.F("rect", x=166, y=166, width=180, height=180, rx=40, fill="none")
    s.F("ellipse", outline=False, cx=210, cy=200, rx=16, ry=24, fill=WHITE, opacity="0.8")


@reg("amethyst")
def _(s):
    cluster(s, "#8B5CF6", "#C4A8FF", "#6E6E78")


@reg("topaz")
def _(s):
    brilliant(s, "#F5A623", "#FFD27A", "#C27A10")


@reg("opal")
def _(s):
    s.F("ellipse", cx=256, cy=256, rx=150, ry=190, fill="#E8F4FA")
    for x, y, r, c in ((210, 180, 40, "#7FE0D8"), (300, 220, 34, "#F7A1B5"), (230, 300, 44, "#A6E0B2"), (300, 330, 30, "#C4A8FF"), (250, 240, 26, "#FFD27A"), (200, 380, 24, "#8FD0FF")):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=c, opacity="0.85")
    s.F("ellipse", cx=256, cy=256, rx=150, ry=190, fill="none")
    s.F("ellipse", outline=False, cx=200, cy=150, rx=20, ry=34, fill=WHITE)


@reg("turquoise")
def _(s):
    s.F("path", d=blob_path(256, 256, [(-150, -20), (-90, -140), (40, -150), (150, -60), (140, 80), (40, 150), (-100, 120)]), fill="#3CC8C0")
    for d in ("M140 220 L200 240 L230 200 L300 230", "M180 320 L240 300 L300 340 L360 310", "M230 200 L240 140"):
        s.M(d, "#3A3A3A", 5)
    s.F("ellipse", outline=False, cx=200, cy=170, rx=24, ry=14, fill="#9AEDE6")


@reg("jade")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill="#3FAE6A")
    s.F("circle", cx=256, cy=256, r=70, fill=WHITE)
    s.F("path", outline=False, d="M100 200 C120 140 170 100 230 86 C180 120 150 160 140 210 Z", fill="#7FD6A0")
    s.M("M300 120 C340 140 370 170 380 210", "#2E8A52", 8)


@reg("garnet")
def _(s):
    s.F("circle", cx=256, cy=256, r=180, fill="#8E1B2A")
    s.F("polygon", outline=False, points=star_pts(256, 256, 170, 90, 8), fill="#B42A3C")
    s.F("polygon", points=" ".join(f"{arc_pt(256, 256, 90, a)[0]:.0f},{arc_pt(256, 256, 90, a)[1]:.0f}" for a in range(0, 360, 45)), fill="#D84A5C")
    s.F("ellipse", outline=False, cx=220, cy=210, rx=18, ry=26, fill=WHITE, opacity="0.8")


@reg("aquamarine")
def _(s):
    step_cut(s, "#7FD3EA", "#C8EEF8", "#4AB0D0", 260, 380)


# ---------------------------------------------------------------- fossils
STONE, STONE_D = "#D8CBB4", "#B8A88E"


def slab(s):
    s.F("path", d=blob_path(256, 266, [(-200, -120), (-60, -170), (120, -160), (200, -60), (190, 110), (60, 170), (-120, 160), (-200, 60)]), fill=STONE)
    s.F("path", outline=False, d=blob_path(256, 266, [(120, 40), (180, 40), (170, 110), (80, 150)]), fill=STONE_D)


@reg("fossil")
def _(s):
    slab(s)
    s.M("M256 266 m0 0 a20 20 0 1 1 20 20 a40 40 0 1 1 -40 -40 a60 60 0 1 1 60 60 a90 90 0 1 1 -90 -90", "#8A7458", 16)
    for a in range(0, 330, 30):
        x1, y1 = arc_pt(256, 266, 60, a)
        x2, y2 = arc_pt(256, 266, 110, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", "#A08A6A", 5)


@reg("fossil-leaf")
def _(s):
    slab(s)
    s.F("path", outline=False, d="M150 380 C140 260 230 160 370 150 C380 290 280 380 150 380 Z", fill="#A08A6A")
    s.M("M150 380 L360 160 M210 316 L200 250 M250 274 L250 200 M290 230 L300 180 M210 316 L280 320 M250 274 L320 280 M290 230 L350 240", "#6E5A40", 6)


@reg("fossil-fish")
def _(s):
    slab(s)
    s.M("M120 266 C170 200 300 200 360 266 C300 330 170 330 120 266 Z", "#8A7458", 10)
    s.M("M120 266 H360 M360 266 L410 220 M360 266 L410 310", "#8A7458", 10)
    for x in range(160, 340, 26):
        s.M(f"M{x} 226 L{x + 10} 306", "#8A7458", 6)
    s.F("circle", outline=False, cx=150, cy=256, r=10, fill="#6E5A40")


@reg("fossil-footprint")
def _(s):
    tile(s, STONE)
    for x, y, rot in ((180, 380, -10), (320, 180, 10)):
        s.open(transform=f"rotate({rot} {x} {y})")
        s.F("ellipse", outline=False, cx=x, cy=y, rx=40, ry=46, fill="#8A7458")
        for dx, dy, r in ((-50, -70, -30), (0, -90, 0), (50, -70, 30)):
            s.F("ellipse", outline=False, cx=x + dx, cy=y + dy, rx=16, ry=44, fill="#8A7458", transform=f"rotate({r} {x + dx} {y + dy})")
        s.close()
    end(s)


@reg("amber-with-insect")
def _(s):
    s.F("path", d=blob_path(256, 266, [(-150, -60), (-60, -170), (80, -160), (170, -40), (130, 120), (0, 180), (-140, 110)]), fill="#F5A623", opacity="0.95")
    s.F("ellipse", outline=False, cx=256, cy=266, rx=24, ry=50, fill="#5A3A1A")
    s.F("circle", outline=False, cx=256, cy=206, r=18, fill="#5A3A1A")
    for dx in (-1, 1):
        s.F("ellipse", outline=False, cx=256 + dx * 50, cy=240, rx=44, ry=18, fill="#FFF3D0", opacity="0.85", transform=f"rotate({dx * -20} {256 + dx * 50} 240)")
        for dy in (250, 280, 310):
            s.M(f"M{256 + dx * 20} {dy} l{dx * 30} 14", "#5A3A1A", 5)
    s.F("path", outline=False, d="M150 160 C170 120 210 100 250 100 C210 120 190 140 170 180 Z", fill="#FFE0A0")


@reg("fossil-dig")
def _(s):
    tile(s, "#C9A26A")
    s.F("rect", outline=False, x=0, y=0, width=512, height=100, fill="#E0BE86")
    s.M("M0 100 H512", INK, 8)
    for d in ("M120 260 H320", "M150 230 V290 M190 230 V290 M230 230 V290 M270 230 V290", "M320 260 C350 240 380 250 390 280"):
        s.M(d, "#F7F0E0", 18)
    s.F("circle", cx=110, cy=260, r=22, fill="#F7F0E0")
    s.T("M360 380 L440 300", C["brown"], 14)
    s.F("rect", x=420, y=260, width=40, height=50, rx=8, fill=YELLOW, transform="rotate(45 440 285)")
    end(s)


# ---------------------------------------------------------------- biomes
@reg("biome")
def _(s):
    for a0, c in ((-90, GRASS), (0, SAND), (90, SNOW), (180, SEA)):
        wedge(s, 256, 256, 200, a0, a0 + 90, c)
    tree(s, 330, 200, 0.7, "pine")
    cactus(s, 330, 360, 0.5)
    s.F("polygon", points="150,360 190,300 230,360", fill=ICE)
    s.M("M140 180 q15 -10 30 0 t30 0", WHITE, 6)


@reg("tropical-rainforest-biome")
def _(s):
    tile(s, "#2F7F45")
    for x, y, r, c in ((60, 120, 90, "#3FA45A"), (200, 80, 100, "#4CB963"), (360, 110, 100, "#3FA45A"), (480, 90, 80, "#4CB963")):
        s.F("circle", cx=x, cy=y, r=r, fill=c)
    for x in (110, 300, 420):
        s.F("rect", x=x - 14, y=160, width=28, height=360, fill=TRUNK)
    s.M("M160 120 C170 220 150 300 170 380 M250 140 C260 230 240 280 256 340", "#5A9A3A", 8)
    for x, y, r in ((60, 400, -30), (200, 430, 20), (350, 410, -20), (470, 440, 30)):
        s.F("ellipse", cx=x, cy=y, rx=70, ry=26, fill=LEAF, transform=f"rotate({r} {x} {y})")
    s.F("ellipse", cx=250, cy=280, rx=18, ry=12, fill=RED)
    s.F("polygon", points="266,278 290,270 284,290", fill=YELLOW)
    end(s)


@reg("temperate-forest")
def _(s):
    tile(s)
    ground(s, 420, GRASS, 6)
    for x, y, k, c in ((100, 430, 1.1, ORANGE), (250, 420, 1.3, GRASS_D), (400, 430, 1.1, C["red"]), (180, 450, 0.7, YELLOW), (330, 460, 0.8, ORANGE)):
        s.F("rect", x=f"{x - 8 * k:.0f}", y=f"{y - 70 * k:.0f}", width=f"{16 * k:.0f}", height=f"{70 * k:.0f}", fill=TRUNK)
        s.F("circle", cx=x, cy=f"{y - 110 * k:.0f}", r=f"{50 * k:.0f}", fill=c)
    end(s)


def acacia(s, x, y, k=1.0):
    s.T(f"M{x} {y} L{x} {y - 90 * k:.0f} M{x} {y - 70 * k:.0f} L{x - 40 * k:.0f} {y - 120 * k:.0f} M{x} {y - 80 * k:.0f} L{x + 40 * k:.0f} {y - 124 * k:.0f}", TRUNK, 12 * k)
    s.F("ellipse", cx=x, cy=f"{y - 136 * k:.0f}", rx=f"{110 * k:.0f}", ry=f"{30 * k:.0f}", fill=GRASS_D)


@reg("savanna")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 256, 220, 70)
    s.F("rect", x=0, y=330, width=512, height=200, fill="#E8C060")
    acacia(s, 140, 350, 1.0)
    acacia(s, 400, 340, 0.6)
    for x in range(30, 500, 46):
        s.M(f"M{x} 470 l-8 -30 m10 30 l4 -36 m8 36 l12 -26", "#B8902A", 6)
    end(s)


@reg("grassland-biome")
def _(s):
    tile(s)
    cloud(s, 380, 110, 0.7)
    s.F("path", d="M0 300 C120 260 260 280 512 260 V520 H0 Z", fill=GRASS_L)
    s.F("path", d="M0 380 C160 340 320 360 512 340 V520 H0 Z", fill=GRASS)
    for x in range(20, 500, 36):
        s.M(f"M{x} 480 l-8 -50 m10 50 l4 -60 m8 60 l12 -44", GRASS_D, 6)
    for x, c in ((120, YELLOW), (260, C["pink"]), (400, WHITE)):
        s.F("circle", cx=x, cy=410, r=12, fill=c)
    end(s)


@reg("tundra")
def _(s):
    tile(s, "#D6E2EA")
    peak(s, 140, 300, 260, 140, ROCK_L, ROCK, 0.5)
    peak(s, 380, 300, 300, 170, ROCK_L, ROCK, 0.5)
    s.F("rect", x=0, y=290, width=512, height=230, fill="#9AA86A")
    for x, y, w in ((60, 350, 90), (300, 400, 120), (150, 460, 80)):
        s.F("ellipse", cx=x + w / 2, cy=y, rx=w / 2, ry=16, fill=SNOW)
    for x, y in ((230, 340), (420, 360), (90, 420), (380, 460)):
        s.F("ellipse", cx=x, cy=y, rx=22, ry=12, fill="#6E8A4A")
    end(s)


@reg("taiga")
def _(s):
    tile(s, "#D6E2EA")
    ground(s, 420, SNOW, 4)
    for x, y, k in ((90, 430, 1.2), (200, 400, 0.9), (300, 440, 1.3), (420, 410, 1.0), (150, 470, 0.7)):
        tree(s, x, y, k, "pine")
        s.F("polygon", outline=False, points=f"{x:.0f},{y - 120 * k:.0f} {x + 14 * k:.0f},{y - 90 * k:.0f} {x - 14 * k:.0f},{y - 90 * k:.0f}", fill=SNOW)
    for x, y in ((60, 80), (180, 140), (330, 70), (440, 150), (250, 220)):
        s.F("circle", cx=x, cy=y, r=7, fill=WHITE)
    end(s)


@reg("polar-region")
def _(s):
    tile(s, "#1E3A6A")
    for i, c in enumerate(("#4CE0A0", "#7FE8C0")):
        s.M(f"M20 {120 + i * 40} C140 {60 + i * 40} 300 {180 + i * 40} 500 {100 + i * 40}", c, 18)
    s.F("rect", x=0, y=330, width=512, height=200, fill=WATER_D)
    s.F("path", d="M40 360 L120 260 L200 300 L260 360 Z", fill=SNOW)
    s.F("path", d="M240 400 L330 290 L440 330 L480 410 Z", fill=ICE)
    s.F("ellipse", cx=150, cy=420, rx=80, ry=14, fill=SNOW)
    end(s)


@reg("desert-biome")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 110, 110, 40)
    s.F("path", d="M260 330 L290 190 H400 L430 330 Z", fill=RED_R)
    s.F("path", d="M0 330 C160 300 340 300 512 330 V520 H0 Z", fill=SAND)
    cactus(s, 150, 430, 1.0)
    cactus(s, 400, 450, 0.7)
    s.F("ellipse", cx=280, cy=450, rx=30, ry=14, fill=ROCK)
    end(s)


@reg("mountain-biome")
def _(s):
    tile(s)
    peak(s, 256, 400, 520, 330)
    for x, y in ((80, 440), (140, 420), (380, 420), (440, 440), (200, 460), (320, 460)):
        tree(s, x, y, 0.7, "pine")
    ground(s, 460, GRASS, 6)
    end(s)


@reg("freshwater-biome")
def _(s):
    tile(s)
    s.F("rect", x=0, y=220, width=512, height=300, fill=WATER)
    s.F("rect", outline=False, x=0, y=220, width=512, height=14, fill=WATER_L)
    s.F("path", d="M0 450 C140 430 360 440 512 450 V520 H0 Z", fill=EARTH)
    for x in (60, 90, 440):
        s.T(f"M{x} 460 V120", GRASS_D, 8)
        s.F("rect", x=x - 9, y=110, width=18, height=46, rx=9, fill=EARTH)
    for x, y in ((220, 320), (340, 380)):
        s.F("path", d=f"M{x - 40} {y} C{x - 20} {y - 24} {x + 20} {y - 24} {x + 30} {y} C{x + 20} {y + 24} {x - 20} {y + 24} {x - 40} {y} Z", fill=ORANGE)
        s.F("polygon", points=f"{x + 28},{y} {x + 54},{y - 18} {x + 54},{y + 18}", fill=ORANGE)
    s.F("path", d="M160 230 m-34 0 a34 14 0 1 0 68 0 a34 14 0 1 0 -68 0", fill=GRASS_L)
    end(s)


@reg("marine-biome")
def _(s):
    tile(s, "#3D8BC9")
    s.F("path", d="M0 440 C140 420 360 430 512 440 V520 H0 Z", fill=SAND)
    for x in (70, 120, 430):
        s.M(f"M{x} 450 C{x - 20} 380 {x + 20} 330 {x} 260", GRASS_D, 14)
    for x, c in ((210, "#F7A1B5"), (330, ORANGE)):
        s.T(f"M{x} 450 V380 M{x} 410 L{x - 30} 370 M{x} 400 L{x + 30} 360", c, 16)
    for x, y, c in ((220, 200, YELLOW), (360, 260, ORANGE), (150, 320, A1L)):
        s.F("path", d=f"M{x - 34} {y} C{x - 16} {y - 20} {x + 16} {y - 20} {x + 26} {y} C{x + 16} {y + 20} {x - 16} {y + 20} {x - 34} {y} Z", fill=c)
        s.F("polygon", points=f"{x + 24},{y} {x + 46},{y - 16} {x + 46},{y + 16}", fill=c)
        s.F("circle", outline=False, cx=x - 18, cy=y - 4, r=4, fill=INK)
    for x, y in ((420, 110), (400, 160), (430, 70)):
        s.F("circle", cx=x, cy=y, r=8, fill=WATER_L)
    end(s)


# ---------------------------------------------------------------- maps and navigation (themed)
def tglobe(s, cx=256, cy=256, r=200):
    globe2(s, cx, cy, r, A1, A2L)


@reg("globe")
def _(s):
    s.T("M120 120 A190 190 0 0 0 360 430", DARK, 16)
    tglobe(s, 246, 256, 170)
    s.T("M246 446 V470", DARK, 16)
    s.F("rect", x=170, y=460, width=152, height=28, rx=12, fill=A2)


@reg("map")
def _(s):
    s.F("polygon", points="40,120 180,80 330,120 472,80 472,420 330,460 180,420 40,460", fill=LIGHT)
    s.F("polygon", outline=False, points="180,80 330,120 330,460 180,420", fill=MID)
    s.M("M90 380 C150 300 220 340 260 260 C300 190 360 220 400 160", A2, 10, dash="2 22")
    s.F("path", d="M400 100 C370 100 356 124 356 144 C356 176 400 210 400 210 C400 210 444 176 444 144 C444 124 430 100 400 100 Z", fill=A1)
    s.F("circle", cx=400, cy=144, r=14, fill=LIGHT)


@reg("folding-map")
def _(s):
    for i, x in enumerate((60, 190, 320)):
        y0 = 120 if i % 2 == 0 else 90
        s.F("polygon", points=f"{x},{y0} {x + 130},{210 - y0} {x + 130},{210 - y0 + 300} {x},{y0 + 300}", fill=LIGHT if i % 2 == 0 else MID)
    s.M("M90 340 C150 300 200 250 260 260 C320 270 360 220 420 200", A1, 10)
    s.F("circle", cx=420, cy=200, r=16, fill=A2)


@reg("treasure-map")
def _(s):
    s.F("path", d="M70 90 H440 C420 140 460 180 440 230 C420 290 460 340 440 420 H70 C90 360 50 300 70 240 C90 180 50 140 70 90 Z", fill="#F3DFAE")
    s.F("path", d="M120 260 C140 200 230 190 260 230 C300 280 260 350 200 340 C150 330 110 310 120 260 Z", fill=A1L)
    s.M("M110 380 C180 380 200 300 260 300 C320 300 300 200 360 180", A2, 10, dash="2 22")
    s.M("M340 140 L390 190 M390 140 L340 190", "#E5484D", 16)


@reg("atlas")
def _(s):
    s.F("rect", x=110, y=70, width=300, height=380, rx=18, fill=A1)
    s.F("rect", outline=False, x=110, y=70, width=40, height=380, fill=A1D)
    s.F("rect", x=380, y=90, width=40, height=350, rx=8, fill=LIGHT)
    tglobe(s, 270, 240, 100)
    s.F("rect", x=200, y=370, width=140, height=24, rx=8, fill=A2)


@reg("compass-navigation")
def _(s):
    s.F("circle", cx=256, cy=270, r=190, fill=A1)
    s.F("circle", cx=256, cy=270, r=150, fill=LIGHT)
    s.F("rect", x=232, y=50, width=48, height=40, rx=12, fill=A1)
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(256, 270, 150, a)
        x2, y2 = arc_pt(256, 270, 130 if a % 90 else 118, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DARK, 6)
    s.F("polygon", points="256,140 286,270 226,270", fill="#E5484D")
    s.F("polygon", points="256,400 286,270 226,270", fill=MID)
    s.F("circle", cx=256, cy=270, r=16, fill=DARK)


@reg("compass-rose")
def _(s):
    s.F("circle", cx=256, cy=256, r=150, fill="none")
    s.F("polygon", points=star_pts(256, 256, 150, 40, 4, -45), fill=A1L)
    s.F("polygon", points=star_pts(256, 256, 220, 46, 4, -90), fill=A1)
    for a in (-90, 0, 90, 180):
        x, y = arc_pt(256, 256, 220, a)
        xl, yl = arc_pt(256, 256, 46, a - 45)
        s.F("polygon", outline=False, points=f"256,256 {x:.0f},{y:.0f} {xl:.0f},{yl:.0f}", fill=A1D)
    x, y = arc_pt(256, 256, 220, -90)
    s.F("polygon", points=f"256,256 {x:.0f},{y:.0f} {arc_pt(256, 256, 46, -45)[0]:.0f},{arc_pt(256, 256, 46, -45)[1]:.0f}", fill=A2)
    s.F("circle", cx=256, cy=256, r=22, fill=LIGHT)


def gridglobe(s, hi=None):
    tglobe(s)
    s.raw('<g fill="none" stroke="' + LIGHT + '" stroke-width="5" opacity="0.9">')
    for dy in (-140, -70, 70, 140):
        rx = math.sqrt(200 ** 2 - dy ** 2)
        s.raw(f'<ellipse cx="256" cy="{256 + dy}" rx="{rx:.0f}" ry="{rx * 0.14:.0f}"/>')
    s.raw('<ellipse cx="256" cy="256" rx="200" ry="28"/>')
    for rx in (70, 140):
        s.raw(f'<ellipse cx="256" cy="256" rx="{rx}" ry="200"/>')
    s.raw('<path d="M256 56 V456"/>')
    s.raw("</g>")
    if hi == "equator":
        s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="28" fill="none" stroke="{A2}" stroke-width="14"/>')
    elif hi == "prime":
        s.M("M256 56 V456", A2, 14)
    elif hi in ("cancer", "capricorn"):
        dy = -82 if hi == "cancer" else 82
        rx = math.sqrt(200 ** 2 - dy ** 2)
        s.raw(f'<ellipse cx="256" cy="{256 + dy}" rx="{rx:.0f}" ry="{rx * 0.14:.0f}" fill="none" stroke="{A2}" stroke-width="12" stroke-dasharray="26 16"/>')
        s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="28" fill="none" stroke="{LIGHT}" stroke-width="8"/>')
    s.F("circle", cx=256, cy=256, r=200, fill="none")


@reg("latitude-and-longitude")
def _(s):
    gridglobe(s)


D["equator"] = lambda s: gridglobe(s, "equator")
D["prime-meridian"] = lambda s: gridglobe(s, "prime")
D["tropic-of-cancer"] = lambda s: gridglobe(s, "cancer")
D["tropic-of-capricorn"] = lambda s: gridglobe(s, "capricorn")


def pole(s, north=True):
    tglobe(s, 256, 286 if north else 226, 180)
    y = 106 if north else 406
    s.F("ellipse", cx=256, cy=y + (14 if north else -14), rx=90, ry=24, fill=LIGHT)
    top = y - 110 if north else y - 100
    s.T(f"M256 {y + 4} V{top}", DARK, 10)
    s.F("path", d=f"M262 {top} H340 L320 {top + 24} L340 {top + 48} H262 Z", fill="#E5484D" if north else A2)


D["north-pole"] = lambda s: pole(s, True)
D["south-pole"] = lambda s: pole(s, False)


@reg("hemispheres")
def _(s):
    tglobe(s)
    s.F("path", outline=False, d="M56 256 A200 200 0 0 1 456 256 Z", fill=A2, opacity="0.45")
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="28" fill="none" stroke="{DARK}" stroke-width="10"/>')
    s.F("circle", cx=256, cy=256, r=200, fill="none")


@reg("gps-navigation")
def _(s):
    s.F("rect", x=140, y=50, width=232, height=412, rx=36, fill=DARK)
    s.F("rect", outline=False, x=160, y=90, width=192, height=330, rx=10, fill=LIGHT)
    s.M("M180 380 C220 340 200 280 250 260 C300 240 300 180 330 140", MID, 20)
    s.M("M180 380 C220 340 200 280 250 260 C300 240 300 180 330 140", A1, 10)
    s.F("path", d="M330 90 C306 90 294 110 294 126 C294 150 330 180 330 180 C330 180 366 150 366 126 C366 110 354 90 330 90 Z", fill=A2)
    s.F("circle", cx=330, cy=126, r=10, fill=LIGHT)
    s.F("circle", cx=180, cy=380, r=14, fill=A1)


@reg("route-map")
def _(s):
    s.F("rect", x=40, y=60, width=432, height=392, rx=30, fill=LIGHT)
    s.M("M110 390 C160 300 240 380 280 290 C320 200 380 260 400 150", A1, 12, dash="4 24")
    for x, y, c in ((110, 390, A1), (400, 150, A2)):
        s.F("path", d=f"M{x} {y - 70} C{x - 30} {y - 70} {x - 44} {y - 48} {x - 44} {y - 30} C{x - 44} {y} {x} {y + 10} {x} {y + 10} C{x} {y + 10} {x + 44} {y} {x + 44} {y - 30} C{x + 44} {y - 48} {x + 30} {y - 70} {x} {y - 70} Z", fill=c)
        s.F("circle", cx=x, cy=y - 34, r=12, fill=LIGHT)


@reg("map-legend")
def _(s):
    s.F("rect", x=90, y=60, width=332, height=392, rx=24, fill=LIGHT)
    rows = ((130, "circle"), (210, "tri"), (290, "line"), (370, "dash"))
    for y, kind in rows:
        if kind == "circle":
            s.F("circle", cx=160, cy=y, r=22, fill=A2)
        elif kind == "tri":
            s.F("polygon", points=f"136,{y + 20} 160,{y - 24} 184,{y + 20}", fill=A1)
        elif kind == "line":
            s.M(f"M136 {y} H184", A1, 14)
        else:
            s.M(f"M136 {y} H184", A2, 10, dash="10 10")
        s.M(f"M220 {y} H380", MID, 16)


@reg("scale-bar")
def _(s):
    for i in range(4):
        s.F("rect", x=60 + i * 98, y=226, width=98, height=50, fill=DARK if i % 2 == 0 else LIGHT)
    for i in range(5):
        s.M(f"M{60 + i * 98} 226 V190", DARK, 8)
    s.M("M60 330 H452", MID, 14)


@reg("contour-lines")
def _(s):
    s.F("rect", x=40, y=40, width=432, height=432, rx=30, fill=LIGHT)
    for i, k in enumerate((1.0, 0.78, 0.56, 0.36, 0.18)):
        s.F("path", outline=False, d=blob_path(256, 256, [(-180, -40), (-100, -170), (60, -160), (180, -60), (170, 90), (40, 170), (-140, 140)], k),
            fill="none", stroke=A1 if i % 2 == 0 else A1D, stroke_width=8)
    s.F("polygon", points="256,226 276,262 236,262", fill=A2)


if __name__ == "__main__":
    run("earth-geography", D, sys.argv[1:] or None)
