"""landmarks: famous buildings, monuments and natural wonders as small scenes (natural colours).
Run: python drawings/landmarks.py [ids...]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import earth_geography_hand as EH  # noqa: E402
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT  # noqa: E402
from draw_lib import C, INK, arc_pt, run, star_pts  # noqa: E402
from earth_geography_hand import (GRASS, GRASS_D, GRASS_L, ICE, ROCK, ROCK_D, ROCK_L, SAND, SAND_D, SEA, SKY, SKY2,  # noqa: E402
                                  WATER, WATER_D, WATER_L, cloud, end, ground, palm, peak, sun, tile, tree, wavelines)
from text_tile import text_path  # noqa: E402

D = {}
WHITE, BLACK, YELLOW, ORANGE, RED = C["white"], C["black"], C["yellow"], C["orange"], C["red"]
MARBLE, MARBLE_D = "#F4F1EA", "#D8D2C4"
REDSTONE, REDSTONE_D, REDSTONE_L = "#B5523A", "#8E3B28", "#D27A5E"
SANDST, SANDST_D = "#D9B77E", "#B8945A"
STEEL, STEEL_D, GLASS, GLASS_D = "#8C99A8", "#5E6B7A", "#9CC9E8", "#5D93BF"
GOLD, NIGHT, DUSK = "#E8A520", "#1E2A4A", "#FFD9B0"
PINK_ST = "#E58A8A"


def reg(name):
    def r(fn):
        def wrapped(s):
            EH._cur[0] = name
            fn(s)
        D[name] = wrapped
        return fn
    return r


# ---------------------------------------------------------------- building blocks
def R(s, x, y, w, h, c, outline=True, rx=0):
    s.F("rect", outline=outline, x=f"{x:.0f}", y=f"{y:.0f}", width=f"{w:.0f}", height=f"{h:.0f}", rx=rx, fill=c)


def P(s, pts, c, outline=True):
    s.F("polygon", outline=outline, points=" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill=c)


def arch(s, cx, by, w, h, c, outline=True):
    """Rounded-top opening, base at by."""
    r = w / 2
    s.F("path", outline=outline, d=f"M{cx - r:.0f} {by:.0f} V{by - h + r:.0f} A{r:.0f} {r:.0f} 0 0 1 {cx + r:.0f} {by - h + r:.0f} V{by:.0f} Z", fill=c)


def parch(s, cx, by, w, h, c, outline=True):
    """Pointed (Mughal) arch opening."""
    r = w / 2
    s.F("path", outline=outline, d=(f"M{cx - r:.0f} {by:.0f} V{by - h + w * 0.6:.0f} Q{cx - r:.0f} {by - h + w * 0.1:.0f} {cx:.0f} {by - h:.0f} "
                                    f"Q{cx + r:.0f} {by - h + w * 0.1:.0f} {cx + r:.0f} {by - h + w * 0.6:.0f} V{by:.0f} Z"), fill=c)


def dome(s, cx, by, r, c, onion=False, finial=GOLD):
    if onion:
        s.F("path", d=(f"M{cx - r:.0f} {by:.0f} C{cx - r * 1.25:.0f} {by - r * 0.7:.0f} {cx - r * 0.6:.0f} {by - r * 1.2:.0f} {cx:.0f} {by - r * 1.75:.0f} "
                       f"C{cx + r * 0.6:.0f} {by - r * 1.2:.0f} {cx + r * 1.25:.0f} {by - r * 0.7:.0f} {cx + r:.0f} {by:.0f} Z"), fill=c)
        top = by - r * 1.75
    else:
        s.F("path", d=f"M{cx - r:.0f} {by:.0f} A{r:.0f} {r:.0f} 0 0 1 {cx + r:.0f} {by:.0f} Z", fill=c)
        top = by - r
    if finial:
        s.T(f"M{cx:.0f} {top:.0f} V{top - r * 0.35:.0f}", finial, max(4, r * 0.08))


def minaret(s, x, base, h, w, c, cap=MARBLE, rings=3, top="dome"):
    R(s, x - w / 2, base - h, w, h, c)
    for i in range(1, rings + 1):
        y = base - h * i / (rings + 1)
        R(s, x - w * 0.7, y - 5, w * 1.4, 10, c)
    if top == "dome":
        R(s, x - w * 0.6, base - h - 4, w * 1.2, 8, cap)
        dome(s, x, base - h - 4, w * 0.6, cap)
    elif top == "cone":
        P(s, [(x - w * 0.65, base - h), (x, base - h - w * 1.6), (x + w * 0.65, base - h)], cap)


def windows(s, x0, y0, cols, rows, w, h, gx, gy, c, outline=False):
    for i in range(cols):
        for j in range(rows):
            R(s, x0 + i * gx, y0 + j * gy, w, h, c, outline)


def crenels(s, x0, x1, y, size, c):
    x = x0
    while x + size <= x1 + 0.5:
        R(s, x, y - size, size, size, c)
        x += size * 2


def water(s, y, c=WATER, lines=True):
    s.F("rect", x=0, y=y, width=512, height=520 - y, fill=c)
    if lines:
        wavelines(s, 70, 200, y + 30, WHITE, 2)


def night(s):
    tile(s, NIGHT)
    for x, y in ((80, 80), (150, 140), (420, 70), (360, 150), (250, 60), (460, 200), (60, 220)):
        s.F("circle", outline=False, cx=x, cy=y, r=4, fill=WHITE)


def label_tile(s, rows, icon):
    s.F("rect", x=40, y=70, width=432, height=372, rx=44, fill=A1)
    icon(s)
    y = 330
    for r in rows:
        d, _ = text_path(r, "black", 256, y, 360, 52)
        s.F("path", outline=False, d=d, fill=LIGHT)
        y += 62


# ---------------------------------------------------------------- India
@reg("taj-mahal")
def _(s):
    tile(s, "#CDE8F7")
    water(s, 410, WATER_L, False)
    R(s, 40, 384, 432, 28, MARBLE_D)
    for x in (70, 442):
        minaret(s, x, 384, 190, 22, MARBLE, rings=3)
    R(s, 130, 250, 252, 134, MARBLE)
    parch(s, 256, 384, 84, 120, "#C9C1AE")
    for x in (170, 342):
        parch(s, x, 330, 38, 60, "#C9C1AE")
        parch(s, x, 380, 38, 40, "#C9C1AE")
    for x in (160, 352):
        R(s, x - 22, 226, 44, 24, MARBLE)
        dome(s, x, 226, 24, MARBLE)
    R(s, 206, 226, 100, 26, MARBLE)
    dome(s, 256, 228, 74, MARBLE, onion=True)
    s.F("rect", outline=False, x=236, y=420, width=40, height=70, fill=WATER)
    end(s)


@reg("red-fort")
def _(s):
    tile(s)
    ground(s, 430, GRASS, 0)
    R(s, 30, 270, 452, 170, REDSTONE)
    crenels(s, 30, 482, 270, 16, REDSTONE)
    R(s, 186, 210, 140, 230, REDSTONE_L)
    parch(s, 256, 440, 70, 120, REDSTONE_D)
    for x in (180, 332):
        R(s, x - 22, 160, 44, 280, REDSTONE)
        R(s, x - 28, 150, 56, 12, MARBLE)
        dome(s, x, 150, 26, MARBLE)
    for x in (226, 256, 286):
        R(s, x - 10, 190, 20, 20, MARBLE)
        dome(s, x, 190, 11, MARBLE)
    s.T("M256 120 V90", DARK, 5)
    P(s, [(258, 90), (296, 98), (258, 106)], "#FF9933")
    end(s)


@reg("qutub-minar")
def _(s):
    tile(s)
    ground(s, 440, GRASS, 0)
    levels = [(440, 54, 330), (330, 46, 250), (250, 38, 180), (180, 30, 130), (130, 24, 90)]
    for i, (base, w, top) in enumerate(levels):
        P(s, [(256 - w, base), (256 - w * 0.86, top), (256 + w * 0.86, top), (256 + w, base)], REDSTONE if i < 3 else MARBLE)
        for k in range(-2, 3):
            s.M(f"M{256 + k * w * 0.35:.0f} {base - 4} L{256 + k * w * 0.3:.0f} {top + 4}", REDSTONE_D if i < 3 else MARBLE_D, 4)
        R(s, 256 - w * 0.95, top - 8, w * 1.9, 12, SANDST)
    dome(s, 256, 82, 16, MARBLE)
    tree(s, 90, 440, 0.8)
    tree(s, 430, 440, 0.7)
    end(s)


@reg("india-gate")
def _(s):
    tile(s, DUSK)
    ground(s, 440, GRASS, 0)
    R(s, 120, 140, 272, 300, SANDST)
    R(s, 110, 120, 292, 28, SANDST_D)
    R(s, 140, 96, 232, 26, SANDST)
    arch(s, 256, 440, 110, 230, "#8C6A3E")
    s.F("path", d="M200 96 Q256 60 312 96 Z", fill=SANDST_D)
    for x in (150, 362):
        R(s, x - 10, 200, 20, 120, SANDST_D, outline=False)
    end(s)


@reg("gateway-of-india")
def _(s):
    tile(s, SKY)
    water(s, 400, WATER)
    R(s, 110, 170, 292, 232, "#E0C48A")
    arch(s, 256, 402, 100, 190, "#8C6A3E")
    for x in (150, 362):
        parch(s, x, 330, 40, 90, "#B8945A")
    for x in (126, 196, 316, 386):
        R(s, x - 16, 120, 32, 52, "#E0C48A")
        dome(s, x, 120, 16, "#E0C48A")
    R(s, 100, 166, 312, 14, "#C9A86A")
    end(s)


@reg("charminar")
def _(s):
    tile(s)
    ground(s, 440, SANDST_D, 0)
    R(s, 130, 230, 252, 210, "#E8D8B8")
    arch(s, 256, 440, 100, 150, "#8C7A5E")
    R(s, 130, 216, 252, 18, "#D8C8A4")
    windows(s, 160, 250, 6, 1, 20, 30, 34, 0, "#B8A88A")
    for x in (130, 382):
        minaret(s, x, 440, 330, 34, "#E8D8B8", cap="#E8D8B8", rings=3)
    end(s)


@reg("hawa-mahal")
def _(s):
    tile(s)
    ground(s, 450, SANDST_D, 0)
    P(s, [(60, 450), (60, 250), (130, 200), (200, 140), (256, 100), (312, 140), (382, 200), (452, 250), (452, 450)], PINK_ST)
    for row in range(6):
        y = 160 + row * 46
        half = 40 + row * 34
        x = 256 - half
        while x <= 256 + half:
            if 70 < x < 442:
                R(s, x - 12, y, 24, 30, "#F7C9B5", rx=10)
                dome(s, x, y, 12, "#F7C9B5", finial=None)
            x += 34
    end(s)


@reg("amber-fort")
def _(s):
    tile(s)
    water(s, 420, WATER, False)
    P(s, [(0, 420), (60, 300), (150, 260), (380, 250), (470, 300), (512, 420)], "#B8945A")
    R(s, 110, 180, 290, 100, "#F0D48A")
    windows(s, 130, 200, 8, 2, 18, 22, 34, 36, "#C9A24A")
    for x in (110, 220, 310, 400):
        R(s, x - 18, 150, 36, 34, "#F0D48A")
        dome(s, x, 150, 18, "#F0D48A")
    s.M("M0 300 L60 280 L60 250 L120 250 M400 250 L470 250 L470 280 L512 290", "#C9A24A", 10)
    end(s)


@reg("mysore-palace")
def _(s):
    tile(s, NIGHT)
    ground(s, 450, GRASS_D, 0)
    R(s, 60, 260, 392, 190, "#E8E0D0")
    for i in range(7):
        arch(s, 90 + i * 55, 450, 34, 70, "#9C8A6A")
    R(s, 210, 180, 92, 270, "#E8E0D0")
    dome(s, 256, 180, 46, "#D86A6A", onion=True)
    for x in (90, 422):
        R(s, x - 22, 200, 44, 60, "#E8E0D0")
        dome(s, x, 200, 24, "#D86A6A", onion=True)
    for x in range(70, 450, 20):
        s.F("circle", outline=False, cx=x, cy=262, r=4, fill=YELLOW)
    end(s)


@reg("victoria-memorial")
def _(s):
    tile(s)
    water(s, 430, WATER_L, False)
    R(s, 50, 300, 412, 130, MARBLE)
    windows(s, 80, 330, 9, 2, 20, 30, 40, 46, MARBLE_D, True)
    R(s, 186, 230, 140, 200, MARBLE)
    dome(s, 256, 232, 70, MARBLE)
    for x in (70, 442):
        R(s, x - 20, 250, 40, 50, MARBLE)
        dome(s, x, 250, 20, MARBLE)
    end(s)


@reg("humayuns-tomb")
def _(s):
    tile(s)
    ground(s, 440, GRASS, 0)
    R(s, 40, 380, 432, 60, REDSTONE)
    for i in range(7):
        parch(s, 70 + i * 62, 440, 34, 46, REDSTONE_D)
    R(s, 120, 230, 272, 150, REDSTONE)
    parch(s, 256, 380, 80, 130, REDSTONE_D)
    for x in (160, 352):
        parch(s, x, 370, 40, 110, REDSTONE_D)
    s.M("M120 240 H392 M120 300 H392", MARBLE, 6)
    R(s, 206, 204, 100, 28, MARBLE)
    dome(s, 256, 206, 64, MARBLE)
    for x in (140, 372):
        R(s, x - 14, 200, 28, 30, REDSTONE)
        dome(s, x, 200, 16, MARBLE)
    end(s)


@reg("fatehpur-sikri")
def _(s):
    tile(s)
    ground(s, 440, SANDST_D, 0)
    for i, (w, h) in enumerate(((360, 70), (290, 62), (220, 56), (150, 50), (80, 46))):
        y = 440 - sum(x[1] for x in ((360, 70), (290, 62), (220, 56), (150, 50), (80, 46))[:i + 1])
        R(s, 256 - w / 2, y, w, h, REDSTONE)
        n = max(2, w // 40)
        for k in range(n):
            R(s, 256 - w / 2 + 8 + k * (w - 16) / n, y + 10, 8, h - 10, REDSTONE_D, outline=False)
        R(s, 256 - w / 2 - 8, y - 6, w + 16, 10, REDSTONE_L)
    dome(s, 256, 94, 30, REDSTONE_L)
    end(s)


@reg("buland-darwaza")
def _(s):
    tile(s)
    ground(s, 440, SANDST_D, 0)
    P(s, [(120, 440), (140, 400), (372, 400), (392, 440)], REDSTONE_L)
    R(s, 130, 130, 252, 272, REDSTONE)
    parch(s, 256, 400, 120, 220, REDSTONE_D)
    s.M("M140 140 H372", MARBLE, 8)
    for x in (150, 210, 302, 362):
        R(s, x - 14, 98, 28, 32, REDSTONE_L)
        dome(s, x, 98, 15, MARBLE)
    end(s)


@reg("gol-gumbaz")
def _(s):
    tile(s)
    ground(s, 440, GRASS, 0)
    R(s, 110, 260, 292, 180, "#A89A84")
    parch(s, 256, 440, 90, 130, "#6E624E")
    R(s, 110, 246, 292, 18, "#8C7E68")
    dome(s, 256, 248, 132, "#B8AC96")
    for x in (110, 402):
        R(s, x - 22, 200, 44, 240, "#A89A84")
        for y in (240, 290, 340):
            R(s, x - 26, y, 52, 8, "#8C7E68")
        dome(s, x, 200, 24, "#B8AC96")
    end(s)


@reg("hampi")
def _(s):
    tile(s, "#F7E3C4")
    for x, y, r in ((80, 300, 70), (430, 290, 80), (140, 260, 50)):
        s.F("circle", cx=x, cy=y, r=r, fill="#C9A27A")
    ground(s, 430, SANDST_D, 0)
    R(s, 170, 260, 172, 130, "#BFAE94")
    for y in (280, 320, 360):
        s.M(f"M176 {y} H336", "#9C8A70", 6)
    P(s, [(180, 260), (210, 190), (302, 190), (332, 260)], "#BFAE94")
    P(s, [(215, 190), (256, 140), (297, 190)], "#BFAE94")
    for x in (190, 322):
        s.F("circle", cx=x, cy=400, r=40, fill="#9C8A70")
        s.F("circle", cx=x, cy=400, r=12, fill="#BFAE94")
    end(s)


@reg("jantar-mantar")
def _(s):
    tile(s)
    ground(s, 440, SANDST_D, 0)
    P(s, [(160, 440), (330, 100), (360, 100), (360, 440)], "#E8C0A0")
    for i in range(10):
        y = 430 - i * 32
        x = 160 + (440 - y) * 0.5
        s.M(f"M{x:.0f} {y} H{x + 14:.0f}", "#B8806A", 5)
    s.F("path", d="M60 440 A110 110 0 0 1 160 330 V440 Z", fill="#E8C0A0")
    s.F("path", d="M452 440 A110 110 0 0 0 360 330 V440 Z", fill="#E8C0A0")
    end(s)


@reg("mehrangarh-fort")
def _(s):
    tile(s)
    P(s, [(0, 520), (0, 330), (80, 280), (170, 250), (360, 250), (440, 280), (512, 320), (512, 520)], "#9C6A4A")
    R(s, 110, 150, 300, 110, "#B8805A")
    windows(s, 130, 170, 8, 2, 16, 20, 34, 40, "#7A4A30")
    for x in (110, 410):
        R(s, x - 24, 130, 48, 130, "#B8805A")
    crenels(s, 86, 434, 150, 12, "#B8805A")
    for x, y in ((40, 400), (100, 430), (160, 410), (380, 420), (440, 400)):
        R(s, x - 26, y - 30, 52, 40, "#6FA8DC")
    end(s)


@reg("howrah-bridge")
def _(s):
    tile(s, DUSK)
    water(s, 370, "#7A9AAA", False)
    R(s, 0, 330, 512, 26, STEEL_D)
    for x in (120, 392):
        R(s, x - 18, 120, 36, 236, STEEL)
    s.M("M20 330 L120 140 L256 230 L392 140 L492 330", STEEL, 14)
    for x in range(40, 480, 34):
        s.M(f"M{x} 330 L{x + 17} 250", STEEL_D, 6)
    s.M("M0 260 H512", STEEL, 8)
    end(s)


@reg("marine-drive")
def _(s):
    night(s)
    for i, (x, h) in enumerate(((40, 120), (90, 160), (140, 110), (200, 180), (260, 140), (320, 200), (380, 130), (430, 170))):
        R(s, x, 330 - h, 50, h, "#3A4766")
        windows(s, x + 8, 340 - h, 3, h // 30, 8, 10, 13, 28, YELLOW)
    water(s, 380, "#1E3A5A", False)
    s.M("M-10 370 C150 360 300 330 520 270", "#C9CED6", 18)
    for i in range(20):
        t = i / 19
        x = -10 + 530 * t
        y = 370 - 100 * t ** 1.4
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y - 14:.0f}", r=6, fill=YELLOW)
    end(s)


# ---------------------------------------------------------------- Middle East
@reg("burj-khalifa")
def _(s):
    tile(s)
    ground(s, 460, SAND, 0)
    steps = [(460, 70), (400, 58), (340, 48), (280, 38), (220, 28), (160, 18)]
    for i, (y, w) in enumerate(steps):
        top = steps[i + 1][0] if i + 1 < len(steps) else 110
        P(s, [(256 - w, y), (256 - w * 0.8, top), (256 + w * 0.6, top), (256 + w * 0.9, y)], GLASS if i % 2 else "#B8D8EE")
    s.T("M256 112 V40", STEEL, 8)
    for x, h in ((90, 120), (140, 90), (390, 110), (440, 80)):
        R(s, x - 20, 460 - h, 40, h, "#A8B8C8")
    end(s)


@reg("burj-al-arab")
def _(s):
    tile(s)
    water(s, 400, WATER)
    s.F("path", d="M200 400 V90 C320 120 380 260 360 400 Z", fill=WHITE)
    s.F("path", d="M200 90 L180 70 L200 60 Z", fill=STEEL)
    for y in range(130, 400, 30):
        s.M(f"M206 {y} C{260 + (y - 90) * 0.2:.0f} {y + 6} {300 + (y - 90) * 0.15:.0f} {y + 10} {340 + (y - 90) * 0.06:.0f} {y + 20}", MARBLE_D, 3)
    R(s, 170, 90, 30, 310, STEEL)
    s.F("circle", cx=176, cy=210, r=26, fill=STEEL_D)
    R(s, 140, 396, 260, 16, SAND)
    end(s)


@reg("museum-of-the-future")
def _(s):
    tile(s)
    ground(s, 430, GRASS_L, 0)
    R(s, 150, 360, 212, 70, "#C9CED6")
    s.F("path", d="M256 70 C410 70 460 200 420 300 C390 370 320 380 256 380 C190 380 122 370 92 300 C52 200 102 70 256 70 Z M256 150 C330 150 360 210 340 270 C320 310 290 314 256 314 C222 314 192 310 172 270 C152 210 182 150 256 150 Z",
        fill="#DDE3EA", fill_rule="evenodd")
    for a in range(0, 360, 24):
        x1, y1 = 256 + 150 * math.cos(math.radians(a)), 225 + 128 * math.sin(math.radians(a))
        x2, y2 = 256 + 120 * math.cos(math.radians(a + 10)), 225 + 104 * math.sin(math.radians(a + 10))
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", STEEL_D, 5)
    end(s)


@reg("dubai-frame")
def _(s):
    tile(s)
    ground(s, 450, SAND, 0)
    s.F("path", d="M150 450 V80 H362 V450 H310 V140 H202 V450 Z", fill=GOLD)
    for y in range(110, 450, 30):
        s.M(f"M156 {y} H196 M316 {y} H356", "#C9881A", 3)
    R(s, 202, 80, 108, 50, GLASS)
    for x, h in ((240, 200), (275, 260), (60, 120), (450, 140)):
        R(s, x - 16, 450 - h, 32, h, "#B8C8D8", outline=False)
    end(s)


@reg("palm-jumeirah")
def _(s):
    tile(s, WATER)
    s.T("M256 470 V250", SAND, 30)
    for a in range(-80, 81, 20):
        x2, y2 = 256 + 170 * math.sin(math.radians(a)), 250 - 150 * math.cos(math.radians(a))
        s.T(f"M256 260 Q{256 + 80 * math.sin(math.radians(a)):.0f} {250 - 70 * math.cos(math.radians(a)):.0f} {x2:.0f} {y2:.0f}", SAND, 18)
    s.M("M70 220 A200 200 0 0 1 442 220", SAND, 14)
    end(s)


@reg("kingdom-centre")
def _(s):
    tile(s, DUSK)
    ground(s, 460, SAND, 0)
    s.F("path", d="M170 460 L196 160 C210 90 302 90 316 160 L342 460 Z M226 170 C226 130 286 130 286 170 L282 220 H230 Z", fill=GLASS, fill_rule="evenodd")
    s.M("M196 160 C210 70 302 70 316 160", STEEL_D, 10)
    end(s)


@reg("jeddah-tower")
def _(s):
    tile(s)
    water(s, 440, WATER)
    P(s, [(206, 440), (250, 40), (262, 40), (306, 440)], "#C8DCEC")
    P(s, [(256, 440), (256, 60), (306, 440)], "#9CC0DA", outline=False)
    for y in range(100, 440, 40):
        s.M(f"M{256 - (y - 40) * 0.12:.0f} {y} H{256 + (y - 40) * 0.12:.0f}", STEEL_D, 3)
    end(s)


@reg("al-ula")
def _(s):
    tile(s, "#FFE3B0")
    ground(s, 440, SAND, 0)
    s.F("path", d="M110 440 C90 300 120 170 200 140 C280 110 380 140 410 240 C430 320 420 400 400 440 Z", fill="#D9956A")
    R(s, 200, 220, 120, 220, "#E8A87A")
    s.M("M200 220 L220 190 L240 220 L260 190 L280 220 L300 190 L320 220", "#B8724A", 8)
    R(s, 236, 330, 48, 110, "#8E4E30")
    s.M("M200 300 H320", "#B8724A", 8)
    for x in (214, 306):
        R(s, x - 6, 300, 12, 140, "#C98A5E", outline=False)
    end(s)


@reg("masmak-fortress")
def _(s):
    tile(s)
    ground(s, 440, SAND, 0)
    R(s, 120, 230, 272, 210, "#C9A27A")
    for x in (120, 392):
        P(s, [(x - 36, 440), (x - 26, 160), (x + 26, 160), (x + 36, 440)], "#BF9670")
        crenels(s, x - 26, x + 26, 160, 10, "#BF9670")
    crenels(s, 140, 372, 230, 12, "#C9A27A")
    R(s, 226, 330, 60, 110, "#6E4A2A")
    for x in (180, 330):
        P(s, [(x - 8, 280), (x, 268), (x + 8, 280)], "#8E6A4A")
    end(s)


@reg("petra")
def _(s):
    tile(s, "#D98A6A")
    s.F("rect", x=110, y=60, width=292, height=380, fill="#E8A383")
    R(s, 130, 270, 252, 170, "#E8A383")
    for x in (146, 196, 316, 366):
        R(s, x - 10, 290, 20, 150, "#F0B898")
    P(s, [(140, 270), (256, 220), (372, 270)], "#F0B898")
    R(s, 226, 340, 60, 100, "#7A3E2A")
    R(s, 150, 140, 212, 60, "#E8A383")
    for x in (170, 342):
        R(s, x - 10, 120, 20, 80, "#F0B898")
    R(s, 226, 110, 60, 90, "#F0B898")
    P(s, [(226, 110), (256, 80), (286, 110)], "#F0B898")
    ground(s, 450, "#C97A5A", 0)
    end(s)


@reg("pyramids-of-giza")
def _(s):
    tile(s, "#FFE3B0")
    sun(s, 420, 100, 36)
    for cx, w, h, c in ((370, 220, 200, "#E0BE86"), (160, 300, 260, "#E8C88E"), (270, 160, 140, "#D8B47A")):
        P(s, [(cx - w / 2, 430), (cx, 430 - h), (cx + w / 2, 430)], c)
        P(s, [(cx, 430 - h), (cx + w / 2, 430), (cx + w * 0.1, 430)], "#C9A26A", outline=False)
    ground(s, 430, SAND, 0)
    end(s)


@reg("great-sphinx")
def _(s):
    tile(s, "#FFE3B0")
    P(s, [(250, 380), (370, 120), (490, 380)], "#E8C88E")
    ground(s, 420, SAND, 0)
    s.F("path", d="M40 420 V360 C40 330 70 320 110 320 H280 L300 280 C300 220 320 190 350 190 C390 190 410 220 410 270 V420 Z", fill="#D9B77E")
    s.F("path", d="M320 210 L300 300 H330 Z M400 210 L420 300 H390 Z", fill="#C9A26A")
    R(s, 330, 200, 60, 20, "#C9A26A")
    s.F("circle", outline=False, cx=356, cy=240, r=5, fill=INK)
    s.F("circle", outline=False, cx=380, cy=240, r=5, fill=INK)
    R(s, 300, 390, 160, 30, "#D9B77E")
    end(s)


@reg("abu-simbel")
def _(s):
    tile(s, "#FFE3B0")
    R(s, 40, 120, 432, 320, "#D9A86A")
    for x in (95, 195, 317, 417):
        s.F("circle", cx=x, cy=190, r=30, fill="#E8B87A")
        P(s, [(x - 34, 180), (x, 150), (x + 34, 180), (x + 30, 230), (x - 30, 230)], "#E8B87A")
        R(s, x - 38, 230, 76, 120, "#E8B87A", rx=10)
        R(s, x - 42, 340, 30, 100, "#E8B87A")
        R(s, x + 12, 340, 30, 100, "#E8B87A")
    R(s, 236, 330, 40, 110, "#6E4A2A")
    ground(s, 440, SAND, 0)
    end(s)


@reg("cairo-tower")
def _(s):
    tile(s)
    water(s, 430, WATER)
    P(s, [(226, 430), (240, 160), (272, 160), (286, 430)], "#D8C8B0")
    for y in range(180, 430, 24):
        s.M(f"M{240 - (y - 160) * 0.05:.0f} {y} L{272 + (y - 160) * 0.05:.0f} {y + 12}", "#B8A88A", 3)
    P(s, [(206, 160), (196, 110), (316, 110), (306, 160)], "#D8C8B0")
    R(s, 210, 90, 92, 22, GLASS)
    s.T("M256 90 V40", STEEL, 6)
    end(s)


@reg("khalifa-fountain")
def _(s):
    night(s)
    water(s, 380, "#1E3A5A", False)
    P(s, [(236, 380), (250, 60), (262, 60), (276, 380)], "#6E8AAA")
    for x, h in ((80, 160), (140, 230), (200, 280), (312, 280), (372, 230), (432, 160)):
        s.M(f"M{x} 380 C{x - 6} {380 - h * 0.6} {x + 6} {380 - h * 0.9} {x} {380 - h}", "#D8F0FF", 10)
        s.F("circle", outline=False, cx=x, cy=380 - h, r=12, fill="#EAF7FF")
    end(s)


@reg("kuwait-towers")
def _(s):
    tile(s)
    water(s, 430, WATER)
    for x, h, balls in ((180, 330, ((230, 60), (150, 34))), (290, 250, ((220, 46),)), (380, 160, ())):
        P(s, [(x - 6, 430), (x, 430 - h), (x + 6, 430)], "#C9CED6")
        for y, r in balls:
            s.F("circle", cx=x, cy=y, r=r, fill="#3D6FB8")
            for k in range(-2, 3):
                s.F("circle", outline=False, cx=x + k * r * 0.35, cy=y + (k % 2) * 8 - 4, r=4, fill="#2E8A5A")
    end(s)


@reg("museum-of-islamic-art-doha")
def _(s):
    tile(s)
    water(s, 400, WATER)
    R(s, 140, 260, 232, 140, "#EDE6D8")
    R(s, 176, 190, 160, 70, "#E4DCCB")
    R(s, 210, 130, 92, 60, "#DCD2BE")
    P(s, [(210, 130), (256, 100), (302, 130)], "#DCD2BE")
    R(s, 238, 150, 36, 20, "#8C7E68", rx=10)
    R(s, 230, 330, 52, 70, "#8C7E68")
    end(s)


@reg("persepolis")
def _(s):
    tile(s, "#FFE3B0")
    ground(s, 420, SAND_D, 0)
    R(s, 40, 400, 432, 26, "#C9B08A")
    for x, h in ((80, 260), (140, 300), (220, 210), (300, 300), (380, 180), (440, 240)):
        R(s, x - 12, 400 - h, 24, h, "#D8C09A")
        R(s, x - 26, 400 - h - 22, 52, 24, "#C9B08A")
        s.M(f"M{x - 4} {404 - h} V396", "#B8A07A", 3)
    end(s)


@reg("azadi-tower")
def _(s):
    tile(s, DUSK)
    ground(s, 440, "#B8C8A0", 0)
    s.F("path", d="M110 440 C150 360 200 300 220 220 C230 170 230 120 240 80 H272 C282 120 282 170 292 220 C312 300 362 360 402 440 H330 C310 380 290 340 256 330 C222 340 202 380 182 440 Z", fill=MARBLE)
    for y in (120, 160, 200):
        s.M(f"M{236 - (y - 80) * 0.1:.0f} {y} H{276 + (y - 80) * 0.1:.0f}", "#7FB0D8", 6)
    end(s)


@reg("galata-tower")
def _(s):
    tile(s)
    for x, h in ((60, 70), (110, 90), (400, 80), (450, 60)):
        R(s, x - 26, 440 - h, 52, h, "#E8C0A0")
        P(s, [(x - 30, 440 - h), (x, 420 - h), (x + 30, 440 - h)], REDSTONE)
    ground(s, 440, SANDST_D, 0)
    R(s, 200, 150, 112, 290, "#C9B89A")
    for y in range(180, 440, 36):
        s.M(f"M200 {y} H312", "#A89A7E", 4)
    windows(s, 224, 200, 3, 4, 12, 22, 28, 56, "#5A4A3A")
    R(s, 190, 140, 132, 16, "#A89A7E")
    P(s, [(196, 140), (256, 50), (316, 140)], "#6E7A8A")
    end(s)


@reg("babylon-gate")
def _(s):
    tile(s, "#FFE3B0")
    ground(s, 440, SAND, 0)
    R(s, 110, 140, 292, 300, "#2A5FA8")
    for x in (110, 402):
        R(s, x - 40, 110, 80, 330, "#2A5FA8")
        crenels(s, x - 40, x + 40, 110, 14, "#2A5FA8")
    crenels(s, 150, 362, 140, 14, "#2A5FA8")
    arch(s, 256, 440, 90, 180, "#6E4A2A")
    for x, y in ((150, 200), (362, 200), (150, 320), (362, 320), (256, 200)):
        s.F("path", outline=False, d=f"M{x - 22} {y + 10} h44 v-10 l-6 -8 h-26 l-8 -8 v18 z", fill=YELLOW)
    s.M("M70 180 H442", YELLOW, 4)
    end(s)


# ---------------------------------------------------------------- Europe
@reg("eiffel-tower")
def _(s):
    tile(s)
    ground(s, 450, GRASS, 0)
    s.F("path", d="M150 450 C200 330 228 230 244 70 H268 C284 230 312 330 362 450 H310 C296 400 280 380 256 380 C232 380 216 400 202 450 Z", fill="#8C6A4A")
    R(s, 176, 300, 160, 18, "#6E5238")
    R(s, 214, 200, 84, 14, "#6E5238")
    s.T("M256 70 V36", "#6E5238", 6)
    for y in range(110, 300, 30):
        s.M(f"M{250 - (y - 70) * 0.18:.0f} {y} L{262 + (y - 70) * 0.18:.0f} {y + 20}", "#6E5238", 3)
    end(s)


@reg("arc-de-triomphe")
def _(s):
    tile(s)
    ground(s, 440, "#C9CED6", 0)
    R(s, 110, 140, 292, 300, "#E8DDC4")
    R(s, 100, 120, 312, 30, "#D4C6A8")
    arch(s, 256, 440, 100, 210, "#8C7E68")
    for x in (150, 362):
        R(s, x - 26, 270, 52, 70, "#D4C6A8", outline=False)
    s.M("M110 190 H402", "#D4C6A8", 8)
    end(s)


@reg("louvre-pyramid")
def _(s):
    tile(s)
    R(s, 20, 260, 472, 180, "#E0D4B8")
    windows(s, 40, 290, 11, 2, 22, 34, 42, 70, "#9C8A6A")
    ground(s, 440, "#C9CED6", 0)
    P(s, [(130, 440), (256, 230), (382, 440)], GLASS)
    for i in range(1, 6):
        s.M(f"M{130 + i * 21} 440 L256 230 M{382 - i * 21} 440 L256 230", WHITE, 3)
    for i in range(1, 5):
        y = 230 + i * 42
        s.M(f"M{256 - (y - 230) * 0.6:.0f} {y} H{256 + (y - 230) * 0.6:.0f}", WHITE, 3)
    end(s)


@reg("big-ben")
def _(s):
    tile(s)
    ground(s, 450, GRASS, 0)
    R(s, 200, 200, 112, 250, "#C9A86A")
    for y in range(260, 450, 30):
        s.M(f"M206 {y} H306", "#A88A4E", 4)
    R(s, 190, 150, 132, 60, "#C9A86A")
    s.F("circle", cx=256, cy=180, r=40, fill=WHITE)
    s.M("M256 180 V152 M256 180 L276 192", INK, 5)
    R(s, 206, 110, 100, 40, "#C9A86A")
    P(s, [(200, 112), (256, 30), (312, 112)], "#2E4A3A")
    for x in (190, 322):
        P(s, [(x - 8, 150), (x, 120), (x + 8, 150)], "#C9A86A")
    end(s)


@reg("tower-bridge")
def _(s):
    tile(s)
    water(s, 380, "#7A9AAA", False)
    R(s, 0, 300, 512, 24, "#5E7A8A")
    for x in (150, 362):
        R(s, x - 36, 130, 72, 250, "#D8C8A4")
        arch(s, x, 380, 40, 70, "#7A9AAA")
        windows(s, x - 20, 160, 2, 3, 12, 20, 28, 36, "#8C7A5E")
        P(s, [(x - 42, 130), (x, 70), (x + 42, 130)], "#5E7A8A")
        for dx in (-34, 34):
            P(s, [(x + dx - 6, 130), (x + dx, 100), (x + dx + 6, 130)], "#5E7A8A")
    R(s, 186, 160, 140, 20, "#3D6FB8")
    s.M("M0 260 C60 270 100 300 114 300 M512 260 C452 270 412 300 398 300", "#3D6FB8", 10)
    end(s)


@reg("london-eye")
def _(s):
    tile(s)
    water(s, 420, "#7A9AAA", False)
    s.raw('<circle cx="256" cy="230" r="170" fill="none" stroke="#2E2A3B" stroke-width="20"/>')
    s.raw('<circle cx="256" cy="230" r="170" fill="none" stroke="#E8ECF2" stroke-width="10"/>')
    for a in range(0, 360, 20):
        x, y = arc_pt(256, 230, 170, a)
        s.M(f"M256 230 L{x:.0f} {y:.0f}", "#C9CED6", 2)
        s.F("ellipse", cx=f"{x:.0f}", cy=f"{y:.0f}", rx=12, ry=9, fill=GLASS)
    s.F("circle", cx=256, cy=230, r=16, fill=STEEL)
    s.M("M256 230 L190 430 M256 230 L322 430", STEEL_D, 12)
    end(s)


@reg("buckingham-palace")
def _(s):
    tile(s)
    ground(s, 430, GRASS, 0)
    R(s, 40, 220, 432, 210, "#E8E0CC")
    windows(s, 60, 250, 13, 3, 16, 26, 31, 52, "#7A8A9A")
    R(s, 186, 180, 140, 50, "#E8E0CC")
    for x in range(196, 330, 26):
        R(s, x, 190, 12, 40, "#D4C8AE", outline=False)
    P(s, [(186, 180), (256, 150), (326, 180)], "#E8E0CC")
    s.T("M256 150 V100", DARK, 5)
    P(s, [(258, 100), (300, 100), (300, 126), (258, 126)], "#C8102E")
    R(s, 40, 424, 432, 12, "#2E2A3B")
    end(s)


@reg("colosseum")
def _(s):
    tile(s)
    ground(s, 450, "#C9B08A", 0)
    s.F("path", d="M40 450 V200 C40 150 472 150 472 200 V330 L420 300 L400 330 L380 290 V450 Z", fill="#D8B88A")
    for row, y in enumerate((260, 340, 420)):
        for i in range(10):
            x = 64 + i * 40
            if x < 390 or row == 2:
                arch(s, x, y, 24, 56, "#8C6A44")
    s.M("M40 280 H380 M40 360 H400", "#B8986A", 6)
    end(s)


@reg("leaning-tower-of-pisa")
def _(s):
    tile(s)
    ground(s, 450, GRASS, 0)
    s.open(transform="rotate(5 256 450)")
    R(s, 196, 120, 120, 330, "#F2EEE4")
    for y in range(150, 450, 44):
        R(s, 190, y - 6, 132, 10, "#DCD6C6")
        for x in range(206, 312, 22):
            arch(s, x + 8, y + 34, 12, 30, "#C9C1AE", outline=False)
    R(s, 214, 80, 84, 40, "#F2EEE4")
    s.close()
    end(s)


@reg("trevi-fountain")
def _(s):
    tile(s)
    R(s, 40, 100, 432, 260, "#E8E0CC")
    for x in (90, 160, 352, 422):
        R(s, x - 10, 140, 20, 200, "#D4C8AE")
    arch(s, 256, 340, 90, 180, "#C9BFA6")
    R(s, 30, 90, 452, 24, "#D4C8AE")
    P(s, [(120, 360), (180, 320), (260, 330), (330, 310), (392, 360)], "#CFC6B0")
    water(s, 380, "#5EC8D8", False)
    for x in (180, 256, 330):
        s.M(f"M{x} 330 C{x - 10} 350 {x - 6} 370 {x} 384", WHITE, 6)
    end(s)


@reg("acropolis")
def _(s):
    tile(s)
    P(s, [(0, 520), (0, 400), (80, 330), (430, 320), (512, 380), (512, 520)], "#B8A07A")
    R(s, 90, 300, 332, 26, "#EDE4D0")
    for x in range(110, 420, 38):
        R(s, x - 8, 200, 16, 100, "#F2EADA")
    R(s, 90, 186, 332, 18, "#EDE4D0")
    P(s, [(90, 186), (256, 140), (422, 186)], "#EDE4D0")
    end(s)


@reg("brandenburg-gate")
def _(s):
    tile(s)
    ground(s, 440, "#C9CED6", 0)
    R(s, 70, 200, 372, 30, "#E0D2B0")
    for x in (90, 150, 210, 302, 362, 422):
        R(s, x - 12, 230, 24, 210, "#EADCB8")
    R(s, 60, 180, 392, 24, "#D4C6A0")
    R(s, 200, 140, 112, 44, "#D4C6A0")
    P(s, [(226, 140), (236, 110), (276, 110), (286, 140)], "#5E8A6E")
    for x in (240, 256, 272):
        s.T(f"M{x} 110 V96", "#5E8A6E", 6)
    end(s)


@reg("neuschwanstein-castle")
def _(s):
    tile(s)
    P(s, [(0, 520), (0, 380), (120, 320), (400, 330), (512, 360), (512, 520)], GRASS_D)
    for x, w, h in ((150, 70, 200), (260, 90, 240), (360, 60, 170)):
        R(s, x - w / 2, 340 - h, w, h, "#F0ECE4")
        windows(s, x - w / 2 + 10, 360 - h, int(w // 24), 3, 10, 18, 22, 40, "#8C9AAA")
    for x, y, r in ((116, 150, 18), (190, 170, 16), (300, 110, 20), (390, 180, 16), (230, 110, 14)):
        R(s, x - r, y, 2 * r, 340 - y, "#F0ECE4")
        P(s, [(x - r - 4, y), (x, y - r * 3.2), (x + r + 4, y)], "#3D6FB8")
    end(s)


@reg("alhambra")
def _(s):
    tile(s, DUSK)
    P(s, [(0, 520), (0, 360), (512, 340), (512, 520)], GRASS_D)
    R(s, 40, 240, 432, 120, "#D9956A")
    crenels(s, 40, 472, 240, 14, "#D9956A")
    for x, h in ((80, 60), (210, 110), (330, 80), (430, 70)):
        R(s, x - 30, 240 - h, 60, h, "#D9956A")
        crenels(s, x - 30, x + 30, 240 - h, 10, "#D9956A")
    windows(s, 70, 280, 10, 1, 14, 22, 40, 0, "#8E4E30")
    peak(s, 420, 240, 260, 120, ROCK_L, ROCK, 0.5)
    R(s, 40, 240, 432, 120, "#D9956A")
    crenels(s, 40, 472, 240, 14, "#D9956A")
    windows(s, 70, 280, 10, 1, 14, 22, 40, 0, "#8E4E30")
    end(s)


@reg("kremlin")
def _(s):
    tile(s)
    ground(s, 440, "#C9CED6", 0)
    R(s, 20, 330, 472, 110, "#B23A2E")
    for x in range(20, 492, 30):
        P(s, [(x, 330), (x + 6, 314), (x + 18, 314), (x + 24, 330)], "#B23A2E")
    R(s, 210, 200, 92, 240, "#B23A2E")
    R(s, 220, 150, 72, 50, "#B23A2E")
    s.F("circle", cx=256, cy=176, r=20, fill=WHITE)
    s.M("M256 176 V164 M256 176 L266 182", INK, 4)
    P(s, [(214, 150), (256, 60), (298, 150)], "#2E6A4A")
    s.F("polygon", points=star_pts(256, 48, 18, 8, 5), fill=RED)
    arch(s, 256, 440, 40, 70, "#5A2A22")
    end(s)


@reg("atomium")
def _(s):
    tile(s)
    ground(s, 450, GRASS, 0)
    pts = [(256, 90), (156, 170), (356, 170), (156, 310), (356, 310), (256, 250), (256, 390)]
    for a, b in ((0, 1), (0, 2), (1, 3), (2, 4), (3, 6), (4, 6), (0, 5), (5, 6), (1, 5), (2, 5), (3, 5), (4, 5)):
        s.M(f"M{pts[a][0]} {pts[a][1]} L{pts[b][0]} {pts[b][1]}", STEEL, 12)
    s.M("M256 390 V450", STEEL, 14)
    for x, y in pts:
        s.F("circle", cx=x, cy=y, r=36, fill="#D8DEE6")
        s.F("circle", outline=False, cx=x - 12, cy=y - 12, r=10, fill=WHITE)
    end(s)


def windmill(s, x, base, k=1.0):
    P(s, [(x - 40 * k, base), (x - 26 * k, base - 160 * k), (x + 26 * k, base - 160 * k), (x + 40 * k, base)], "#5E4A3A")
    P(s, [(x - 30 * k, base - 160 * k), (x, base - 200 * k), (x + 30 * k, base - 160 * k)], "#3A2E28")
    hx, hy = x, base - 170 * k
    for a in (40, 130, 220, 310):
        x2, y2 = arc_pt(hx, hy, 110 * k, a)
        s.T(f"M{hx:.0f} {hy:.0f} L{x2:.0f} {y2:.0f}", "#E8E0CC", 14 * k)
    s.F("circle", cx=f"{hx:.0f}", cy=f"{hy:.0f}", r=f"{10 * k:.0f}", fill="#3A2E28")


@reg("windmills-of-kinderdijk")
def _(s):
    tile(s)
    ground(s, 380, GRASS, 0)
    water(s, 420, WATER, False)
    windmill(s, 380, 400, 0.8)
    windmill(s, 170, 420, 1.1)
    end(s)


@reg("edinburgh-castle")
def _(s):
    tile(s, "#C8D4DE")
    P(s, [(0, 520), (0, 340), (90, 290), (200, 300), (420, 280), (512, 320), (512, 520)], "#6E6A64")
    R(s, 90, 190, 330, 110, "#9C968A")
    crenels(s, 90, 420, 190, 14, "#9C968A")
    for x, h in ((120, 80), (300, 120), (400, 70)):
        R(s, x - 30, 190 - h, 60, h, "#9C968A")
        crenels(s, x - 30, x + 30, 190 - h, 10, "#9C968A")
    windows(s, 110, 220, 9, 2, 12, 18, 34, 36, "#4A463E")
    end(s)


# ---------------------------------------------------------------- Asia
@reg("great-wall-of-china")
def _(s):
    tile(s)
    P(s, [(0, 520), (0, 300), (120, 220), (240, 280), (360, 180), (512, 260), (512, 520)], GRASS_D)
    s.M("M-10 430 C80 400 100 300 170 300 C240 300 260 360 320 330 C380 300 400 230 520 210", "#A89A84", 40)
    s.M("M-10 410 C80 380 100 280 170 280 C240 280 260 340 320 310 C380 280 400 210 520 190", "#8C7E68", 8, dash="10 12")
    for x, y in ((170, 290), (330, 322), (460, 214)):
        R(s, x - 24, y - 52, 48, 52, "#A89A84")
        crenels(s, x - 24, x + 24, y - 52, 8, "#A89A84")
    end(s)


@reg("forbidden-city")
def _(s):
    tile(s)
    ground(s, 440, "#D8C8A4", 0)
    R(s, 70, 370, 372, 70, "#E8E0CC")
    R(s, 110, 250, 292, 120, "#B23A2E")
    for x in range(130, 400, 32):
        R(s, x, 270, 14, 100, "#8E2A20", outline=False)
    s.F("path", d="M60 260 Q256 230 452 260 L420 230 H92 Z", fill="#E8A520")
    R(s, 140, 200, 232, 34, "#B23A2E")
    s.F("path", d="M100 210 Q256 180 412 210 L380 160 H132 Z", fill="#E8A520")
    end(s)


@reg("terracotta-army")
def _(s):
    tile(s, "#C9A27A")
    for row, (y, k) in enumerate(((220, 0.6), (320, 0.8), (440, 1.0))):
        n = 6 - row
        for i in range(n):
            x = 256 + (i - (n - 1) / 2) * 90 * k
            s.F("circle", cx=f"{x:.0f}", cy=f"{y - 130 * k:.0f}", r=f"{20 * k:.0f}", fill="#B88A5E")
            R(s, x - 22 * k, y - 110 * k, 44 * k, 70 * k, "#A87A4E", rx=8)
            R(s, x - 18 * k, y - 42 * k, 14 * k, 42 * k, "#A87A4E")
            R(s, x + 4 * k, y - 42 * k, 14 * k, 42 * k, "#A87A4E")
            s.M(f"M{x - 18 * k:.0f} {y - 90 * k:.0f} H{x + 18 * k:.0f}", "#8E6038", 4)
    end(s)


@reg("petronas-towers")
def _(s):
    night(s)
    ground(s, 460, "#3A4766", 0)
    for x in (180, 332):
        steps = [(460, 44), (300, 38), (220, 30), (170, 22), (130, 14)]
        for i, (y, w) in enumerate(steps):
            top = steps[i + 1][0] if i + 1 < len(steps) else 100
            R(s, x - w, top, 2 * w, y - top, "#C9D4E0")
        s.T(f"M{x} 100 V40", "#C9D4E0", 6)
        for y in range(320, 460, 20):
            s.M(f"M{x - 40} {y} H{x + 40}", "#8C9AAA", 2)
    R(s, 220, 250, 72, 14, "#C9D4E0")
    end(s)


@reg("marina-bay-sands")
def _(s):
    tile(s, DUSK)
    water(s, 420, "#3D6FA8", False)
    for x in (130, 256, 382):
        P(s, [(x - 40, 420), (x - 30, 170), (x + 30, 170), (x + 40, 420)], "#C9D4E0")
        for y in range(190, 420, 24):
            s.M(f"M{x - 30} {y} H{x + 30}", "#8C9AAA", 2)
    s.F("path", d="M60 170 H470 L480 150 H80 Z", fill="#9CAABA")
    tree(s, 120, 166, 0.25)
    tree(s, 380, 166, 0.25)
    end(s)


@reg("tokyo-tower")
def _(s):
    tile(s)
    ground(s, 450, "#C9CED6", 0)
    s.F("path", d="M156 450 C206 330 234 230 248 70 H264 C278 230 306 330 356 450 H306 C294 410 278 390 256 390 C234 390 218 410 206 450 Z", fill="#E5484D")
    for y, w in ((140, 20), (220, 30), (300, 48), (370, 70)):
        R(s, 256 - w, y, 2 * w, 16, WHITE if y in (220, 370) else "#E5484D")
    R(s, 220, 250, 72, 24, WHITE)
    end(s)


@reg("tokyo-skytree")
def _(s):
    tile(s)
    ground(s, 460, "#C9CED6", 0)
    P(s, [(200, 460), (244, 90), (268, 90), (312, 460)], "#E8ECF2")
    for y in range(120, 460, 20):
        s.M(f"M{244 - (y - 90) * 0.12:.0f} {y} L{268 + (y - 90) * 0.12:.0f} {y + 12}", "#B8C2CE", 2)
    R(s, 222, 260, 68, 26, "#8C9AAA")
    R(s, 230, 180, 52, 18, "#8C9AAA")
    s.T("M256 90 V30", "#B8C2CE", 6)
    end(s)


@reg("taipei-101")
def _(s):
    tile(s)
    ground(s, 460, "#C9CED6", 0)
    R(s, 220, 380, 72, 80, "#6FA89A")
    for i in range(8):
        y = 380 - (i + 1) * 34
        P(s, [(226, y + 34), (216, y), (296, y), (286, y + 34)], "#7FBAAA")
    R(s, 236, 90, 40, 18, "#7FBAAA")
    s.T("M256 90 V30", STEEL, 6)
    end(s)


@reg("merlion")
def _(s):
    tile(s)
    water(s, 400, WATER)
    R(s, 170, 300, 172, 110, "#D8D2C4")
    s.F("path", d="M200 400 C190 330 200 270 230 240 C210 220 210 170 240 150 C270 130 320 140 330 180 C340 210 330 230 310 240 C330 270 330 330 320 400 Z", fill=MARBLE)
    for a in range(200, 340, 22):
        x, y = arc_pt(276, 190, 60, a)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=16, fill=MARBLE)
    s.F("circle", outline=False, cx=300, cy=184, r=6, fill=INK)
    s.M("M330 210 C380 220 410 260 420 330", "#BDE6F7", 14)
    s.M("M330 210 C380 220 410 260 420 330", WHITE, 6)
    end(s)


# ---------------------------------------------------------------- Americas
@reg("statue-of-liberty")
def _(s):
    tile(s)
    water(s, 440, WATER)
    P(s, [(176, 440), (196, 330), (316, 330), (336, 440)], "#C9B08A")
    s.F("path", d="M210 330 C206 260 214 200 230 170 H282 C298 200 306 260 302 330 Z", fill="#7FC4AA")
    s.F("circle", cx=256, cy=150, r=26, fill="#7FC4AA")
    for a in range(200, 345, 24):
        x, y = arc_pt(256, 150, 46, a)
        s.M(f"M{arc_pt(256, 150, 24, a)[0]:.0f} {arc_pt(256, 150, 24, a)[1]:.0f} L{x:.0f} {y:.0f}", "#7FC4AA", 7)
    s.T("M282 180 L322 90", "#7FC4AA", 18)
    s.F("path", d="M322 92 C310 70 330 50 322 30 C344 46 346 76 330 92 Z", fill=ORANGE)
    R(s, 214, 210, 40, 30, "#6AB098", rx=4)
    end(s)


@reg("golden-gate-bridge")
def _(s):
    tile(s)
    water(s, 380, WATER_D, False)
    P(s, [(0, 400), (0, 300), (60, 270), (90, 330)], GRASS_D)
    R(s, -10, 330, 532, 18, "#C0392B")
    for x in (150, 380):
        R(s, x - 14, 110, 28, 290, "#C0392B")
        R(s, x - 20, 160, 40, 10, "#A93226")
        R(s, x - 20, 230, 40, 10, "#A93226")
    s.M("M-10 300 Q80 330 150 112 Q265 330 380 112 Q450 330 520 260", "#C0392B", 8)
    for x in range(10, 512, 22):
        s.M(f"M{x} 330 V{300 if x < 150 else 260}", "#C0392B", 2)
    end(s)


@reg("empire-state-building")
def _(s):
    tile(s)
    ground(s, 460, "#8C9AAA", 0)
    for x, w, top in ((256, 150, 330), (256, 110, 230), (256, 80, 160), (256, 50, 120), (256, 24, 90)):
        R(s, x - w / 2, top, w, 460 - top, "#D8D0C0")
        for k in range(-2, 3):
            s.M(f"M{x + k * w * 0.18:.0f} {top + 6} V458", "#B8B0A0", 3)
    s.T("M256 90 V30", "#B8B0A0", 6)
    for x, h in ((80, 140), (130, 100), (400, 160), (450, 110)):
        R(s, x - 26, 460 - h, 52, h, "#A8B2BE")
    end(s)


@reg("white-house")
def _(s):
    tile(s)
    ground(s, 420, GRASS, 0)
    R(s, 40, 240, 432, 180, WHITE)
    windows(s, 60, 270, 12, 2, 16, 30, 34, 70, "#8C9AAA")
    R(s, 176, 200, 160, 220, WHITE)
    for x in range(186, 336, 30):
        R(s, x, 220, 14, 200, MARBLE_D, outline=False)
    P(s, [(166, 200), (256, 160), (346, 200)], WHITE)
    s.T("M256 160 V110", DARK, 4)
    for i, c in enumerate(("#B22234", WHITE, "#B22234")):
        R(s, 258, 110 + i * 8, 40, 8, c, outline=False)
    R(s, 258, 110, 16, 14, "#3C3B6E", outline=False)
    end(s)


@reg("space-needle")
def _(s):
    tile(s)
    peak(s, 420, 360, 300, 170, ROCK_L, ROCK, 0.5)
    ground(s, 460, GRASS, 0)
    s.M("M210 460 C240 360 246 260 250 170 M302 460 C272 360 266 260 262 170", "#E8ECF2", 16)
    s.M("M226 330 H286", "#E8ECF2", 10)
    s.F("path", d="M150 170 L180 140 H332 L362 170 L332 186 H180 Z", fill="#E8ECF2")
    s.F("path", d="M190 140 L210 116 H302 L322 140 Z", fill="#E8A520")
    s.T("M256 116 V50", "#E8ECF2", 6)
    end(s)


@reg("cn-tower")
def _(s):
    tile(s)
    water(s, 450, WATER)
    P(s, [(222, 450), (246, 120), (266, 120), (290, 450)], "#D8DEE6")
    s.F("ellipse", cx=256, cy=200, rx=50, ry=24, fill="#C9D4E0")
    R(s, 214, 206, 84, 14, "#8C9AAA")
    s.F("ellipse", cx=256, cy=130, rx=16, ry=10, fill="#C9D4E0")
    s.T("M256 120 V30", STEEL, 6)
    end(s)


@reg("machu-picchu")
def _(s):
    tile(s, "#D6E8F0")
    P(s, [(250, 400), (330, 100), (370, 90), (420, 160), (470, 400)], GRASS_D)
    P(s, [(0, 520), (0, 330), (120, 300), (300, 310), (512, 360), (512, 520)], GRASS)
    for i in range(6):
        y = 340 + i * 26
        s.M(f"M{40 + i * 6} {y} H{440 - i * 10}", "#5E8A3E", 5)
    for x, y in ((90, 320), (150, 316), (210, 322), (270, 326)):
        R(s, x - 22, y - 26, 44, 26, ROCK_L)
        P(s, [(x - 24, y - 26), (x, y - 44), (x + 24, y - 26)], ROCK)
    end(s)


@reg("chichen-itza")
def _(s):
    tile(s)
    ground(s, 440, GRASS, 0)
    for i in range(9):
        w = 400 - i * 34
        R(s, 256 - w / 2, 420 - i * 30, w, 30, "#C9B89A" if i % 2 else "#BFAE90")
    R(s, 226, 150, 60, 270, "#B8A888")
    for y in range(170, 420, 14):
        s.M(f"M230 {y} H282", "#9C8C6E", 3)
    R(s, 216, 110, 80, 44, "#C9B89A")
    R(s, 242, 126, 28, 28, "#6E5E48")
    end(s)


@reg("teotihuacan")
def _(s):
    tile(s, "#FFE3B0")
    ground(s, 440, SAND, 0)
    for i in range(5):
        w = 420 - i * 70
        P(s, [(256 - w / 2, 440 - i * 56), (256 - w / 2 + 20, 440 - (i + 1) * 56), (256 + w / 2 - 20, 440 - (i + 1) * 56), (256 + w / 2, 440 - i * 56)], "#B8A07A" if i % 2 else "#A89068")
    R(s, 236, 160, 40, 280, "#C9B08A", outline=False)
    end(s)


@reg("panama-canal")
def _(s):
    tile(s)
    P(s, [(0, 520), (0, 260), (512, 260), (512, 520)], GRASS)
    R(s, 0, 290, 512, 140, "#C9CED6")
    R(s, 0, 300, 250, 120, WATER)
    R(s, 262, 330, 250, 90, WATER_D)
    R(s, 246, 290, 20, 140, "#5E5A50")
    s.F("path", d="M60 320 H220 L200 360 H80 Z", fill=RED)
    R(s, 90, 270, 90, 50, WHITE)
    for x in range(96, 176, 20):
        R(s, x, 280, 10, 10, GLASS_D, outline=False)
    end(s)


# ---------------------------------------------------------------- Africa and Oceania
@reg("sydney-opera-house")
def _(s):
    tile(s)
    water(s, 400, WATER)
    R(s, 40, 360, 432, 40, "#D8C8A4")
    for x, w, h in ((110, 120, 150), (200, 130, 190), (300, 120, 160), (390, 100, 120)):
        s.F("path", d=f"M{x - w / 2:.0f} 360 C{x - w / 3:.0f} {360 - h * 0.7:.0f} {x:.0f} {360 - h:.0f} {x + w / 2:.0f} {360 - h * 1.05:.0f} C{x + w / 3:.0f} {360 - h * 0.5:.0f} {x + w / 2:.0f} 360 {x + w / 2:.0f} 360 Z", fill=WHITE)
        s.M(f"M{x - w / 4:.0f} 358 C{x - w / 8:.0f} {360 - h * 0.5:.0f} {x + w / 6:.0f} {360 - h * 0.8:.0f} {x + w / 2.2:.0f} {360 - h:.0f}", MARBLE_D, 3)
    end(s)


@reg("sydney-harbour-bridge")
def _(s):
    tile(s)
    water(s, 400, WATER)
    for x in (60, 452):
        R(s, x - 36, 220, 72, 180, "#D8C8A4")
    s.M("M96 330 Q256 80 416 330", "#8C99A8", 24)
    s.M("M96 330 Q256 140 416 330", "#8C99A8", 10)
    R(s, 24, 320, 464, 20, "#6E7A88")
    for x in range(110, 410, 24):
        y = 330 - 250 * (1 - ((x - 256) / 160) ** 2) * 0.5
        s.M(f"M{x} 320 V{y:.0f}", "#6E7A88", 3)
    end(s)


@reg("uluru")
def _(s):
    tile(s, DUSK)
    sun(s, 400, 120, 36)
    ground(s, 400, "#C97A4A", 0)
    s.F("path", d="M50 410 C70 330 110 290 180 280 C260 270 340 272 400 290 C450 310 470 360 470 410 Z", fill="#C0582E")
    for x in (150, 220, 300, 380):
        s.M(f"M{x} 290 C{x - 10} 330 {x + 6} 370 {x} 400", "#9A4320", 5)
    for x in (80, 420, 260):
        s.M(f"M{x} 450 l-8 -24 m10 24 l4 -26 m8 26 l10 -20", "#8C9A4A", 5)
    end(s)


@reg("table-mountain-cable-car")
def _(s):
    tile(s)
    water(s, 430, WATER)
    P(s, [(0, 430), (40, 220), (90, 160), (430, 160), (480, 230), (512, 430)], ROCK)
    s.F("path", d="M90 160 H430 V172 H90 Z", fill=WHITE)
    s.M("M60 430 L420 150", DARK, 3)
    R(s, 220, 266, 50, 34, RED, rx=6)
    s.M("M245 266 V258", DARK, 3)
    R(s, 228, 274, 34, 12, GLASS, outline=False)
    end(s)


# ---------------------------------------------------------------- natural wonders
@reg("grand-canyon")
def _(s):
    tile(s, SKY2)
    for i, (y, c) in enumerate(((180, "#D9774A"), (240, "#E8955E"), (300, "#C9653E"), (360, "#E8A070"))):
        s.F("path", d=f"M0 {y} H200 L{220 + i * 10} {y + 60} H{290 - i * 10} L312 {y} H512 V520 H0 Z", fill=c)
    s.F("path", d="M220 520 C240 470 250 450 256 430 C262 450 272 470 292 520 Z", fill=WATER)
    end(s)


def falls(s, x0, x1, top, bottom, water_c=WATER_L):
    R(s, x0, top, x1 - x0, bottom - top, water_c)
    for x in range(int(x0) + 14, int(x1), 22):
        s.M(f"M{x} {top + 8} V{bottom - 10}", WHITE, 5)
    for x in range(int(x0), int(x1) + 1, 40):
        s.F("circle", cx=x, cy=bottom, r=30, fill=WHITE)


@reg("niagara-falls")
def _(s):
    tile(s)
    water(s, 380, WATER_D, False)
    s.F("path", d="M0 200 H512 V250 H0 Z", fill=GRASS_D)
    falls(s, 40, 470, 240, 390)
    s.F("path", d="M300 430 h80 l-12 18 h-56 z", fill="#2C5FC9")
    R(s, 318, 412, 40, 18, "#2C5FC9")
    end(s)


@reg("victoria-falls")
def _(s):
    tile(s)
    s.F("rect", x=0, y=150, width=512, height=90, fill=GRASS_D)
    falls(s, 20, 492, 230, 380)
    R(s, 0, 380, 512, 140, ROCK_D)
    for i, c in enumerate((RED, ORANGE, YELLOW, C["green"], C["blue"])):
        s.raw(f'<path d="M80 380 A180 180 0 0 1 440 380" fill="none" stroke="{c}" stroke-width="10" opacity="0.8" transform="translate(0 {i * 10})"/>')
    end(s)


@reg("angel-falls")
def _(s):
    tile(s)
    s.F("path", d="M60 520 L110 150 C150 130 330 120 400 140 L450 520 Z", fill="#8C6A4E")
    s.F("path", d="M110 150 C150 130 330 120 400 140 L404 168 C320 150 160 156 106 176 Z", fill=GRASS_D)
    for x in (150, 210, 340, 380):
        s.M(f"M{x} 200 L{x - 10} 500", "#6E5038", 5)
    R(s, 250, 150, 22, 300, WATER_L)
    s.M("M261 160 V440", WHITE, 6)
    for x in (226, 261, 296):
        s.F("circle", cx=x, cy=452, r=26, fill=WHITE)
    s.F("rect", x=0, y=470, width=512, height=60, fill=GRASS)
    for x in (60, 450):
        tree(s, x, 500, 0.8)
    end(s)


@reg("iguazu-falls")
def _(s):
    tile(s)
    s.F("rect", x=0, y=140, width=512, height=80, fill=GRASS_D)
    for x0, x1 in ((20, 110), (140, 240), (270, 350), (380, 490)):
        falls(s, x0, x1, 210, 360)
    R(s, 0, 360, 512, 160, WATER)
    for x in (130, 255, 365):
        tree(s, x, 230, 0.6)
    end(s)


@reg("great-barrier-reef")
def _(s):
    tile(s, "#3DB8C9")
    s.F("path", d="M0 420 C140 400 360 410 512 420 V520 H0 Z", fill=SAND)
    for x, c in ((80, "#F7A1B5"), (180, ORANGE), (290, "#8B5CF6"), (400, YELLOW)):
        s.T(f"M{x} 430 V350 M{x} 390 L{x - 30} 340 M{x} 380 L{x + 30} 330", c, 18)
    s.F("ellipse", cx=200, cy=430, rx=40, ry=24, fill="#E5484D")
    for x, y, c in ((150, 200, ORANGE), (320, 260, YELLOW), (420, 170, "#3D8BFD")):
        s.F("path", d=f"M{x - 30} {y} C{x - 14} {y - 18} {x + 14} {y - 18} {x + 22} {y} C{x + 14} {y + 18} {x - 14} {y + 18} {x - 30} {y} Z", fill=c)
        s.F("polygon", points=f"{x + 20},{y} {x + 40},{y - 14} {x + 40},{y + 14}", fill=c)
    end(s)


@reg("amazon-rainforest")
def _(s):
    tile(s, "#2F7F45")
    s.F("path", d="M-10 520 C80 420 220 440 260 360 C300 280 420 300 520 240 V300 C430 340 330 330 300 400 C260 480 120 470 60 520 Z", fill="#8C6A3E")
    for x, y, r in ((60, 160, 90), (200, 110, 100), (360, 140, 110), (480, 200, 80), (120, 300, 60), (420, 380, 70), (60, 420, 60)):
        s.F("circle", cx=x, cy=y, r=r, fill="#3FA45A" if r % 20 else "#4CB963")
    s.F("ellipse", cx=300, cy=230, rx=18, ry=12, fill=RED)
    end(s)


@reg("northern-lights-wonder")
def _(s):
    night(s)
    for i, c in enumerate(("#4CE0A0", "#7FE8C0", "#8B5CF6")):
        s.M(f"M-10 {200 + i * 40} C120 {80 + i * 40} 300 {260 + i * 30} 520 {120 + i * 40}", c, 24 - i * 6)
    s.F("path", d="M0 400 C120 360 300 380 512 350 V520 H0 Z", fill=WHITE)
    tree(s, 100, 420, 0.8, "pine")
    tree(s, 420, 400, 0.9, "pine")
    end(s)


@reg("mount-everest-view")
def _(s):
    tile(s, "#BFDDF2")
    peak(s, 120, 380, 260, 170, ROCK_L, ROCK, 0.5)
    peak(s, 290, 400, 380, 330, ROCK, ROCK_D, 0.45)
    peak(s, 440, 380, 220, 150, ROCK_L, ROCK, 0.5)
    s.M("M290 70 L350 60", WHITE, 8)
    ground(s, 420, WHITE, 6)
    for i, c in enumerate((RED, YELLOW, C["green"], C["blue"], WHITE)):
        P(s, [(60 + i * 30, 450), (90 + i * 30, 450), (75 + i * 30, 470)], c, outline=False)
    s.M("M50 450 H220", DARK, 3)
    end(s)


@reg("ha-long-bay")
def _(s):
    tile(s, "#CFE6EE")
    water(s, 360, "#5EA8B8", False)
    for x, w, h in ((80, 90, 220), (200, 70, 160), (330, 110, 260), (450, 80, 180)):
        s.F("path", d=f"M{x - w / 2} 360 C{x - w / 2} {360 - h * 0.6} {x - w / 3} {360 - h} {x} {360 - h} C{x + w / 3} {360 - h} {x + w / 2} {360 - h * 0.6} {x + w / 2} 360 Z", fill="#6E8A6A")
    s.F("path", d="M180 430 H300 L285 450 H195 Z", fill="#8C5A33")
    s.F("path", d="M230 430 V370 L270 410 L230 410 M240 430 V380 L208 405 L240 405", fill="#E8955E")
    end(s)


@reg("paricutin-volcano")
def _(s):
    tile(s, "#E0D4C8")
    ground(s, 420, GRASS_L, 0)
    s.F("path", d="M100 420 L210 200 H302 L412 420 Z", fill="#5A4A44")
    s.F("ellipse", cx=256, cy=200, rx=46, ry=10, fill="#2E2A28")
    for x, y, r in ((256, 160, 36), (230, 120, 40), (290, 100, 46), (250, 60, 40)):
        s.F("circle", cx=x, cy=y, r=r, fill="#9A9AA4")
    for x in (60, 450):
        tree(s, x, 440, 0.6, "pine")
    end(s)


@reg("harbour-of-rio")
def _(s):
    tile(s)
    water(s, 370, WATER)
    s.F("path", d="M300 370 C300 260 330 160 380 150 C430 150 450 260 450 370 Z", fill="#6E7A5E")
    s.F("path", d="M150 370 C160 320 190 300 220 300 C250 300 260 330 270 370 Z", fill="#6E7A5E")
    s.M("M240 300 L380 152", DARK, 3)
    s.F("path", d="M0 370 C40 300 80 280 120 300 L130 370 Z", fill=GRASS_D)
    for x in range(20, 140, 24):
        R(s, x, 380, 16, 20, WHITE)
    end(s)


@reg("giants-causeway")
def _(s):
    tile(s, "#C8D4DE")
    water(s, 260, WATER_D, False)
    for row in range(6):
        y = 280 + row * 40
        for col in range(9):
            x = 10 + col * 58 + (row % 2) * 29
            h = 30 + ((col * 5 + row * 3) % 4) * 22 + row * 6
            top = y - h
            R(s, x - 26, top, 52, 560 - top, "#4A4A52")
            P(s, [(x - 26, top), (x - 13, top - 12), (x + 13, top - 12), (x + 26, top), (x + 13, top + 12), (x - 13, top + 12)], "#8C8C96")
    end(s)


@reg("cappadocia")
def _(s):
    tile(s, DUSK)
    for x, h in ((90, 200), (180, 260), (300, 220), (410, 180)):
        s.F("path", d=f"M{x - 40} 440 C{x - 34} {440 - h * 0.5} {x - 20} {440 - h * 0.9} {x} {440 - h} C{x + 20} {440 - h * 0.9} {x + 34} {440 - h * 0.5} {x + 40} 440 Z", fill="#E0C49A")
        s.F("ellipse", cx=x, cy=440 - h, rx=26, ry=12, fill="#8C6A4A")
        R(s, x - 8, 400 - h * 0.4, 16, 22, "#6E4A2A", rx=8)
    ground(s, 440, SAND_D, 0)
    for x, y, c in ((140, 100, RED), (370, 80, "#3D8BFD"), (260, 140, YELLOW)):
        s.F("circle", cx=x, cy=y, r=30, fill=c)
        s.M(f"M{x - 16} {y + 24} L{x - 8} {y + 46} M{x + 16} {y + 24} L{x + 8} {y + 46}", DARK, 3)
        R(s, x - 10, y + 44, 20, 14, "#8C5A33")
    end(s)


@reg("pamukkale")
def _(s):
    tile(s, "#BFE6FA")
    s.F("rect", x=0, y=120, width=512, height=400, fill=WHITE)
    for i in range(5):
        y = 160 + i * 70
        for j in range(3):
            x = 20 + j * 170 + (i % 2) * 60
            s.F("path", d=f"M{x} {y} H{x + 150} C{x + 150} {y + 40} {x + 130} {y + 50} {x + 75} {y + 50} C{x + 20} {y + 50} {x} {y + 40} {x} {y} Z", fill="#F4F6F8")
            s.F("ellipse", outline=False, cx=x + 75, cy=y + 8, rx=66, ry=12, fill="#5ED0E0")
    end(s)


@reg("salar-de-uyuni")
def _(s):
    tile(s)
    s.F("rect", x=0, y=260, width=512, height=260, fill="#CFE8F7")
    for x, y in ((140, 140), (380, 110)):
        cloud(s, x, y, 0.8)
        s.open(transform="translate(0 520) scale(1 -1)")
        cloud(s, x, y, 0.8)
        s.close()
    s.M("M0 260 H512", WHITE, 4)
    for x in (230, 270):
        s.F("circle", cx=x, cy=236, r=8, fill=DARK)
        R(s, x - 6, 244, 12, 16, DARK)
        s.F("circle", outline=False, cx=x, cy=284, r=8, fill="#8C9AAA")
    end(s)


@reg("zhangjiajie-pillars")
def _(s):
    tile(s, "#DCE8E4")
    for x, w, h in ((70, 60, 330), (170, 50, 400), (260, 70, 300), (360, 56, 380), (450, 50, 280)):
        R(s, x - w / 2, 520 - h, w, h, "#8C8A80", rx=10)
        s.F("ellipse", cx=x, cy=520 - h, rx=w * 0.7, ry=18, fill=GRASS_D)
        tree(s, x, 520 - h, 0.3, "pine")
    for x, y in ((120, 330), (360, 300), (250, 420), (440, 430)):
        s.F("ellipse", outline=False, cx=x, cy=y, rx=110, ry=22, fill=WHITE, opacity="0.55")
    end(s)


@reg("yellowstone-geyser")
def _(s):
    tile(s)
    peak(s, 120, 330, 260, 120, ROCK_L, ROCK, 0.4)
    ground(s, 400, "#C9B48A", 0)
    s.F("path", d="M226 400 C236 300 226 200 240 110 H272 C286 200 276 300 286 400 Z", fill=WATER_L)
    for x, y, r in ((256, 110, 54), (210, 140, 40), (300, 140, 40), (256, 70, 40)):
        s.F("circle", cx=x, cy=y, r=r, fill=WHITE)
    s.F("ellipse", cx=256, cy=410, rx=110, ry=24, fill="#7FD8E0")
    for x in (420, 470):
        tree(s, x, 410, 0.7, "pine")
    end(s)


@reg("antelope-canyon")
def _(s):
    tile(s, "#8E3B1E")
    for i, c in enumerate(("#E8955E", "#D9774A", "#F0B070", "#C9653E")):
        x = 60 + i * 40
        s.F("path", d=f"M{x} 0 C{x + 80} 120 {x - 40} 260 {x + 40} 520 H{x - 60} C{x - 120} 260 {x} 120 {x - 60} 0 Z", fill=c)
        s.F("path", d=f"M{512 - x} 0 C{432 - x} 120 {552 - x} 260 {472 - x} 520 H{572 - x} C{632 - x} 260 {512 - x} 120 {572 - x} 0 Z", fill=c)
    s.F("polygon", outline=False, points="236,0 276,0 300,520 212,520", fill="#FFF3D0", opacity="0.6")
    end(s)


@reg("plitvice-lakes")
def _(s):
    tile(s)
    s.F("rect", x=0, y=90, width=512, height=430, fill=GRASS_D)
    for y, w in ((150, 300), (270, 380), (400, 470)):
        s.F("ellipse", cx=256, cy=y, rx=w / 2, ry=44, fill="#3DC8C0")
        s.F("ellipse", outline=False, cx=230, cy=y - 10, rx=w / 4, ry=10, fill="#7FE0D8")
    for x, y0, y1 in ((200, 192, 232), (300, 192, 232), (150, 312, 362), (256, 312, 362), (360, 312, 362)):
        R(s, x - 16, y0, 32, y1 - y0, WHITE)
        s.M(f"M{x - 6} {y0 + 4} V{y1 - 4} M{x + 6} {y0 + 4} V{y1 - 4}", "#BFE6FA", 3)
    for x, y in ((40, 120), (470, 120), (60, 250), (450, 250)):
        tree(s, x, y, 0.6, "pine")
    end(s)


@reg("rann-of-kutch")
def _(s):
    tile(s, "#1E2A4A")
    s.F("circle", cx=380, cy=130, r=50, fill="#FFF3D0")
    s.F("rect", x=0, y=280, width=512, height=240, fill="#F4F6F8")
    for i in range(8):
        y = 300 + i * 26
        s.M(f"M0 {y} C140 {y - 8} 360 {y + 8} 512 {y}", "#D8DEE6", 3)
    for x in (80, 140):
        R(s, x - 18, 250, 36, 30, "#E8C88E")
        P(s, [(x - 24, 252), (x, 226), (x + 24, 252)], "#C0392B")
    end(s)


@reg("valley-of-flowers")
def _(s):
    tile(s)
    peak(s, 140, 280, 300, 200, ROCK_L, ROCK, 0.5)
    peak(s, 380, 280, 340, 230, ROCK_L, ROCK, 0.5)
    s.F("rect", x=0, y=260, width=512, height=260, fill=GRASS)
    import random
    rnd = random.Random(7)
    for _ in range(60):
        x, y = rnd.uniform(20, 492), rnd.uniform(290, 500)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=f"{rnd.uniform(5, 10):.0f}", fill=rnd.choice(("#F7A1B5", YELLOW, "#8B5CF6", WHITE, ORANGE)))
    end(s)


# ---------------------------------------------------------------- seven wonders (themed title tiles)
def mini_icons(s, which):
    xs = [256 + (i - (len(which) - 1) / 2) * 70 for i in range(len(which))]
    for x, kind in zip(xs, which):
        y = 220
        if kind == "pyramid":
            P(s, [(x - 30, y), (x, y - 50), (x + 30, y)], A2L)
        elif kind == "tower":
            P(s, [(x - 22, y), (x - 4, y - 60), (x + 4, y - 60), (x + 22, y)], A2L)
        elif kind == "dome":
            R(s, x - 26, y - 24, 52, 24, A2L)
            dome(s, x, y - 24, 22, A2L, finial=None)
        elif kind == "arch":
            arch(s, x, y, 50, 60, A2L)
        elif kind == "peak":
            P(s, [(x - 32, y), (x, y - 56), (x + 32, y)], A2L)
        elif kind == "wave":
            s.M(f"M{x - 30} {y - 20} q15 -16 30 0 t30 0", A2L, 10)


D["seven-wonders-of-the-world"] = lambda s: label_tile(s, ["7 WONDERS", "OF THE WORLD"], lambda s: mini_icons(s, ["dome", "tower", "arch", "pyramid"]))
D["seven-wonders-of-the-ancient-world"] = lambda s: label_tile(s, ["7 ANCIENT", "WONDERS"], lambda s: mini_icons(s, ["pyramid", "tower", "pyramid"]))
D["new-seven-wonders"] = lambda s: label_tile(s, ["NEW 7", "WONDERS"], lambda s: mini_icons(s, ["dome", "arch", "tower"]))
D["seven-natural-wonders"] = lambda s: label_tile(s, ["7 NATURAL", "WONDERS"], lambda s: mini_icons(s, ["peak", "wave", "peak"]))


if __name__ == "__main__":
    run("landmarks", D, sys.argv[1:] or None)
