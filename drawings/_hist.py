"""Shared helpers for history, fantasy-mythology and mysteries drawings (natural colours)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID  # noqa: E402,F401
from draw_lib import C, INK, arc_pt, head, run, star_pts  # noqa: E402,F401
from text_tile import text_path  # noqa: E402

WHITE, GREY, DGREY, BLACK = C["white"], C["grey"], C["darkgrey"], C["black"]
RED, DRED, ORANGE, YEL, GOLD, DGOLD = C["red"], C["darkred"], C["orange"], C["yellow"], C["gold"], C["darkgold"]
GREEN, DGREEN, SKY, BLUE, DBLUE, NAVY, PURPLE, PINK = C["green"], C["darkgreen"], C["sky"], C["blue"], C["darkblue"], C["navy"], C["purple"], C["pink"]
TAN, CREAM, SKIN, BROWN, DBROWN = C["tan"], C["cream"], C["skin"], C["brown"], C["darkbrown"]
SKIN_D = "#E0A878"
HAIR = "#4A3B32"
STONE, DSTONE = "#B8B2A7", "#8F897E"
SAND, DSAND = "#E8CFA0", "#C9A86A"
IRON = "#8A8F9B"
GLASS = "#E3F3FC"
OW = 10


def registry():
    D = {}

    def reg(name):
        def r(fn):
            D[name] = fn
            return fn
        return r
    return D, reg


def txt(s, text, cx, cy, w, h, color=WHITE, font="black"):
    d, _ = text_path(text, font, cx, cy, w, h)
    if d:
        s.F("path", outline=False, d=d, fill=color)


def ring(s, cx, cy, r, color, w):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w + 2 * OW}" data-outline="under"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>')


def dot(s, x, y, r, color=BLACK):
    s.F("circle", outline=False, cx=x, cy=y, r=r, fill=color)


def flame(s, x, y, k=1.0):
    s.open(transform=f"translate({x} {y}) scale({k})")
    s.F("path", d="M0 -90 C30 -40 56 -20 50 20 C46 46 26 56 0 56 C-26 56 -46 46 -50 20 C-56 -20 -30 -40 0 -90Z", fill=ORANGE)
    s.F("path", outline=False, d="M0 -30 C16 0 28 10 24 30 C20 46 10 50 0 50 C-10 50 -20 46 -24 30 C-28 10 -16 0 0 -30Z", fill=YEL)
    s.close()


def person(s, cx=256, base=470, k=1.0, shirt=BLUE, pants=BROWN, skin=SKIN, hair=HAIR, hat=None, arms="down", face=True):
    """Generic standing figure; base is the y of the feet. Origin point (cx, base)."""
    s.open(transform=f"translate({cx} {base}) scale({k}) translate(-256 -470)")
    s.F("rect", x=206, y=340, width=46, height=124, rx=18, fill=pants)
    s.F("rect", x=260, y=340, width=46, height=124, rx=18, fill=pants)
    s.F("rect", x=198, y=448, width=62, height=22, rx=10, fill=DBROWN)
    s.F("rect", x=252, y=448, width=62, height=22, rx=10, fill=DBROWN)
    if arms == "down":
        s.F("rect", x=150, y=200, width=44, height=130, rx=20, fill=shirt)
        s.F("rect", x=318, y=200, width=44, height=130, rx=20, fill=shirt)
        s.F("circle", cx=172, cy=338, r=20, fill=skin)
        s.F("circle", cx=340, cy=338, r=20, fill=skin)
    elif arms == "up":
        s.F("rect", x=140, y=110, width=44, height=130, rx=20, fill=shirt, transform="rotate(-18 162 240)")
        s.F("rect", x=328, y=110, width=44, height=130, rx=20, fill=shirt, transform="rotate(18 350 240)")
        s.F("circle", cx=140, cy=112, r=20, fill=skin)
        s.F("circle", cx=372, cy=112, r=20, fill=skin)
    s.F("rect", x=176, y=190, width=160, height=170, rx=40, fill=shirt)
    s.F("circle", cx=256, cy=130, r=62, fill=skin)
    if hair:
        s.F("path", d="M194 130 C190 70 240 52 256 56 C290 52 324 76 318 130 C290 112 230 104 194 130Z", fill=hair)
    if face:
        dot(s, 234, 138, 7)
        dot(s, 278, 138, 7)
    if hat == "helmet":
        s.F("path", d="M190 130 C190 60 322 60 322 130Z", fill=IRON)
    s.close()


def pyramid(s, cx=256, base=420, w=380, h=300, color=SAND, dark=DSAND):
    s.F("polygon", points=f"{cx - w / 2},{base} {cx},{base - h} {cx + w / 2},{base}", fill=color)
    s.F("polygon", outline=False, points=f"{cx},{base - h} {cx + w / 2},{base} {cx + 20},{base}", fill=dark)


def column(s, x, y, h, w=70, color=STONE):
    s.F("rect", x=x - w / 2, y=y, width=w, height=h, fill=color)
    for dx in (-w * 0.25, 0, w * 0.25):
        s.M(f"M{x + dx} {y + 20} V{y + h - 20}", DSTONE, 5)
    s.F("rect", x=x - w * 0.62, y=y - 22, width=w * 1.24, height=26, rx=6, fill=color)
    s.F("rect", x=x - w * 0.62, y=y + h - 4, width=w * 1.24, height=26, rx=6, fill=color)


def sun_disc(s, x, y, r, color=YEL):
    s.F("circle", cx=x, cy=y, r=r, fill=color)
    for a in range(0, 360, 45):
        x1, y1 = arc_pt(x, y, r * 1.2, a)
        x2, y2 = arc_pt(x, y, r * 1.6, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", color, 10)


def ground(s, color=GREEN, y=400):
    s.F("path", d=f"M0 {y} C100 {y - 30} 200 {y + 20} 300 {y - 10} C400 {y - 30} 460 {y} 512 {y - 20} V512 H0Z", fill=color)


def scroll(s, x=96, y=110, w=320, h=290, color=CREAM, rod=BROWN):
    s.F("rect", x=x, y=y, width=w, height=h, rx=10, fill=color)
    s.F("rect", x=x - 20, y=y - 18, width=w + 40, height=36, rx=18, fill=rod)
    s.F("rect", x=x - 20, y=y + h - 18, width=w + 40, height=36, rx=18, fill=rod)


def lines(s, x, y, w, n=4, gap=40, color=TAN, sw=10):
    for i in range(n):
        s.M(f"M{x} {y + i * gap} h{w - (i % 2) * 40}", color, sw)
