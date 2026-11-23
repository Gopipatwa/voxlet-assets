"""fantasy-mythology A: classic creatures. Run: python drawings/fantasy_a.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _animals import quad  # noqa: E402
from _hist import (INK, BLACK, BLUE, BROWN, CREAM, DARK, DBROWN, DGOLD, DGREEN, DGREY, DRED, GLASS, GOLD, GREEN, GREY, HAIR, IRON, LIGHT, MID, NAVY, ORANGE, PINK, PURPLE, RED, SAND, SKIN, SKY, STONE, TAN, WHITE, YEL, arc_pt, dot, flame, registry, ring, run, star_pts, txt)  # noqa: E402

D, reg = registry()
DB = "#2C5FC9"
TEAL, DTEAL = "#2FB5A8", "#1F8A80"
LGREEN = "#8FDCA0"
FUR, DFUR = "#B9A892", "#8F7E68"


def eye(s, x, y, r=9, c=BLACK, w=WHITE):
    s.F("circle", outline=False, cx=x, cy=y, r=r * 1.5, fill=w)
    s.F("circle", outline=False, cx=x + 1, cy=y + 1, r=r, fill=c)
    s.F("circle", outline=False, cx=x - 2, cy=y - 2, r=r * 0.32, fill=WHITE)


def wing_bat(s, x, y, w=200, h=170, color=PURPLE, flip=1, bone=None):
    bone = bone or color
    pts = f"M{x} {y} C{x + flip * w * 0.2} {y - h} {x + flip * w * 0.8} {y - h * 1.1} {x + flip * w} {y - h * 0.7} C{x + flip * w * 0.85} {y - h * 0.35} {x + flip * w * 0.9} {y - h * 0.15} {x + flip * w * 0.7} {y} C{x + flip * w * 0.6} {y - h * 0.15} {x + flip * w * 0.5} {y - h * 0.15} {x + flip * w * 0.4} {y} C{x + flip * w * 0.3} {y - h * 0.1} {x + flip * w * 0.15} {y - h * 0.1} {x} {y}Z"
    s.F("path", d=pts, fill=color)
    s.M(f"M{x} {y} L{x + flip * w * 0.97} {y - h * 0.68}", INK, 5)


def feather_wing(s, x, y, w=180, h=150, color=WHITE, flip=1):
    s.F("path", d=f"M{x} {y} C{x + flip * w * 0.2} {y - h} {x + flip * w * 0.7} {y - h * 1.1} {x + flip * w} {y - h * 0.55} C{x + flip * w * 0.9} {y - h * 0.4} {x + flip * w * 0.95} {y - h * 0.25} {x + flip * w * 0.8} {y - h * 0.1} C{x + flip * w * 0.7} {y} {x + flip * w * 0.6} {y + 4} {x + flip * w * 0.5} {y + 10} C{x + flip * w * 0.3} {y + 4} {x + flip * w * 0.15} {y + 4} {x} {y}Z", fill=color)
    for t in (0.35, 0.55, 0.75):
        s.M(f"M{x + flip * w * t} {y - h * 0.15} L{x + flip * w * (t + 0.15)} {y - h * 0.5 * (1.2 - t)}", MID, 5)


def horn(s, x, y, a, l=80, c=CREAM, w=22):
    ex, ey = x + l * math.cos(math.radians(a)), y + l * math.sin(math.radians(a))
    nx, ny = -math.sin(math.radians(a)) * w / 2, math.cos(math.radians(a)) * w / 2
    s.F("polygon", points=f"{x + nx:.0f},{y + ny:.0f} {ex:.0f},{ey:.0f} {x - nx:.0f},{y - ny:.0f}", fill=c)


def scales(s, cx, cy, rx, ry, color, n=3):
    for i in range(n):
        for j in range(3):
            x = cx - rx * 0.6 + j * rx * 0.55
            y = cy - ry * 0.3 + i * ry * 0.4
            s.raw(f'<path d="M{x - 14:.0f} {y:.0f} q14 18 28 0" fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round"/>')


# ================================================================ dragons
def dragon(s, body=GREEN, dark=DGREEN, belly=TAN, wing=PURPLE, fire=True):
    wing_bat(s, 230, 230, 230, 190, wing, 1)
    s.F("path", d="M60 330 C20 310 20 270 60 270 C90 270 110 300 140 330 C190 380 300 400 360 340 C390 310 370 260 400 240 C420 225 450 225 470 245 C490 260 480 290 450 295 C430 300 410 300 400 320 C390 380 330 430 220 430 C130 430 90 380 60 330Z", fill=body)
    s.F("path", outline=False, d="M150 360 C200 410 300 420 350 370 C320 400 200 400 150 360Z", fill=belly)
    s.F("path", d="M390 230 C390 190 430 170 470 180 L505 200 C500 230 480 245 450 245 C420 250 400 245 390 230Z", fill=body)
    s.F("path", d="M410 200 L420 160 L436 196Z", fill=belly)
    s.F("path", d="M440 192 L455 156 L468 190Z", fill=belly)
    s.F("circle", outline=False, cx=444, cy=214, r=8, fill=BLACK)
    s.F("circle", outline=False, cx=494, cy=212, r=3.5, fill=BLACK)
    for x in (110, 150, 190, 240, 290, 340):
        s.F("path", outline=False, d=f"M{x} {336 - (x % 13)} l10 -22 l10 22Z", fill=dark)
    s.F("rect", x=220, y=392, width=40, height=60, rx=14, fill=body)
    s.F("rect", x=320, y=380, width=40, height=70, rx=14, fill=body)
    for x in (220, 320):
        s.F("path", outline=False, d=f"M{x} 450 l8 14 l8 -14 l8 14 l8 -14Z", fill=belly)


@reg("dragon")
def _(s):
    dragon(s)


@reg("chinese-dragon")
def _(s):
    s.raw(f'<path d="M70 400 C20 300 130 260 180 320 C230 380 300 360 300 280 C300 200 220 170 260 120 C300 70 420 90 440 150" fill="none" stroke="{INK}" stroke-width="78" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M70 400 C20 300 130 260 180 320 C230 380 300 360 300 280 C300 200 220 170 260 120 C300 70 420 90 440 150" fill="none" stroke="{RED}" stroke-width="58" stroke-linecap="round"/>')
    s.raw(f'<path d="M70 400 C20 300 130 260 180 320 C230 380 300 360 300 280 C300 200 220 170 260 120 C300 70 420 90 440 150" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-dasharray="4 26"/>')
    s.F("path", d="M410 110 C410 70 470 70 490 110 C505 140 490 180 450 185 C420 185 400 150 410 110Z", fill=RED)
    s.F("path", d="M430 70 C420 40 400 30 380 36 C400 50 410 60 420 80Z", fill=GOLD)
    s.F("path", d="M470 80 C480 50 500 40 510 40 C500 60 495 70 488 92Z", fill=GOLD)
    eye(s, 455, 118, 7)
    s.T("M440 180 C420 220 400 230 380 222", GOLD, 6)
    s.T("M485 160 C510 175 520 160 505 150", GOLD, 6)
    s.F("circle", cx=110, cy=130, r=36, fill=GOLD)
    s.F("circle", outline=False, cx=100, cy=120, r=10, fill=WHITE, fill_opacity="0.7")
    s.F("path", d="M64 420 L44 470 L90 440Z", fill=GOLD)


@reg("baby-dragon")
def _(s):
    wing_bat(s, 190, 270, 100, 100, PINK, -1)
    wing_bat(s, 320, 270, 100, 100, PINK, 1)
    s.F("ellipse", cx=256, cy=350, rx=110, ry=100, fill=GREEN)
    s.F("ellipse", outline=False, cx=256, cy=380, rx=70, ry=60, fill=TAN)
    s.F("circle", cx=256, cy=200, r=100, fill=GREEN)
    s.F("path", d="M200 120 L180 60 L228 100Z", fill=TAN)
    s.F("path", d="M312 120 L332 60 L284 100Z", fill=TAN)
    eye(s, 220, 200, 14)
    eye(s, 292, 200, 14)
    s.F("ellipse", outline=False, cx=236, cy=244, rx=6, ry=4, fill=DGREEN)
    s.F("ellipse", outline=False, cx=276, cy=244, rx=6, ry=4, fill=DGREEN)
    s.M("M226 264 C246 278 266 278 286 264", DGREEN, 8)
    s.T("M360 410 C430 420 450 360 420 340", GREEN, 28)
    s.F("circle", cx=190, cy=440, r=26, fill=GREEN)
    s.F("circle", cx=322, cy=440, r=26, fill=GREEN)
    for x, y in ((256, 120), (240, 126), (272, 126)):
        s.F("circle", outline=False, cx=x, cy=y, r=7, fill=TAN)


@reg("dragon-egg")
def _(s):
    s.F("path", d="M256 40 C160 40 90 170 100 290 C110 400 170 470 256 470 C342 470 402 400 412 290 C422 170 352 40 256 40Z", fill=PURPLE)
    for x, y, r in ((190, 160, 26), (320, 130, 20), (350, 250, 30), (180, 300, 24), (260, 380, 28), (330, 380, 18)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=GOLD, fill_opacity="0.9")
    s.M("M256 90 L236 150 L270 190 L240 240", INK, 8)
    s.F("path", outline=False, d="M150 190 C170 120 210 80 250 66", fill="none", stroke=WHITE, stroke_width="18", stroke_linecap="round", stroke_opacity="0.45")


# ================================================================ horse-likes
HORSE = dict(neck=0.55, head_r=48, snout="long", snout_c=CREAM, ears="pointy", tail="horse", hoof=GREY, leg=1.25)


@reg("unicorn")
def _(s):
    quad(s, body=WHITE, mane=PINK, **HORSE)
    s.F("polygon", points="402,106 412,26 428,100", fill=GOLD)
    s.M("M404 90 L418 62 M408 76 L420 52", DGOLD, 4)
    for x, y in ((100, 120), (440, 380), (60, 380)):
        s.F("polygon", points=star_pts(x, y, 22, 8, 4), fill=GOLD)


@reg("pegasus")
def _(s):
    quad(s, body=WHITE, mane=SKY, **HORSE)
    feather_wing(s, 220, 250, 170, 190, SKY, -1)
    feather_wing(s, 250, 250, 190, 200, WHITE, 1)


@reg("centaur")
def _(s):
    quad(s, body=BROWN, mane=DBROWN, tail_c=DBROWN, neck=0.0, head_r=1, snout="none", ears="none", tail="horse", hoof=DGREY, leg=1.1, cx=200)
    s.F("rect", x=300, y=150, width=96, height=170, rx=40, fill=SKIN)
    s.F("rect", x=272, y=186, width=36, height=110, rx=18, fill=SKIN, transform="rotate(20 290 240)")
    s.F("rect", x=390, y=186, width=36, height=110, rx=18, fill=SKIN, transform="rotate(-15 408 240)")
    s.F("circle", cx=350, cy=116, r=48, fill=SKIN)
    s.F("path", d="M304 110 C300 54 400 50 398 110 C380 96 330 90 304 110Z", fill=HAIR)
    eye(s, 336, 122, 5)
    eye(s, 366, 122, 5)
    s.T("M440 230 L470 90", DBROWN, 8)
    s.F("polygon", points="470,90 456,60 482,70", fill=IRON)


@reg("mermaid")
def _(s):
    s.F("path", d="M230 250 C190 320 190 400 230 440 C260 470 300 450 300 420 C330 470 400 460 440 420 C400 410 380 380 340 340 C320 310 310 270 300 250Z", fill=TEAL)
    s.F("path", d="M300 420 C330 470 400 460 440 420 C400 410 380 400 360 380Z", fill=DTEAL)
    s.F("rect", x=214, y=170, width=96, height=110, rx=36, fill=SKIN)
    s.F("circle", cx=262, cy=130, r=48, fill=SKIN)
    s.F("path", d="M210 130 C190 60 340 40 320 140 C320 200 330 260 310 300 C290 240 300 160 290 120 C260 110 230 110 210 130Z", fill=RED)
    eye(s, 246, 130, 5)
    eye(s, 280, 130, 5)
    s.M("M250 152 C258 160 270 160 276 152", DRED, 5)
    s.F("path", d="M222 200 C226 220 296 220 302 200 C300 190 224 190 222 200Z", fill=PINK)
    for x, y in ((240, 330), (270, 300), (270, 380), (235, 400)):
        s.raw(f'<path d="M{x - 12} {y} q12 16 24 0" fill="none" stroke="{DTEAL}" stroke-width="5" stroke-linecap="round"/>')


@reg("merman")
def _(s):
    s.F("path", d="M230 250 C190 320 190 400 230 440 C260 470 300 450 300 420 C330 470 400 460 440 420 C400 410 380 380 340 340 C320 310 310 270 300 250Z", fill=SKY)
    s.F("path", d="M300 420 C330 470 400 460 440 420 C400 410 380 400 360 380Z", fill=DB)
    s.F("rect", x=210, y=160, width=104, height=130, rx=36, fill=SKIN)
    s.F("circle", cx=262, cy=118, r=48, fill=SKIN)
    s.F("path", d="M212 112 C214 56 310 54 312 112 C290 96 240 94 212 112Z", fill=HAIR)
    s.F("path", d="M232 150 C240 190 284 190 294 150 C284 160 244 160 232 150Z", fill=HAIR)
    eye(s, 246, 124, 5)
    eye(s, 280, 124, 5)
    s.T("M330 190 L380 60", GOLD, 8)
    s.F("path", d="M380 60 L362 26 M380 60 L380 20 M380 60 L398 26", fill="none", stroke=GOLD, stroke_width="8", stroke_linecap="round")


@reg("sea-serpent")
def _(s):
    s.F("rect", x=0, y=300, width=512, height=212, fill=SKY)
    s.raw(f'<path d="M20 400 C80 280 130 280 170 380 C210 280 260 270 300 370 C340 280 390 250 430 190" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M20 400 C80 280 130 280 170 380 C210 280 260 270 300 370 C340 280 390 250 430 190" fill="none" stroke="{TEAL}" stroke-width="44" stroke-linecap="round"/>')
    s.F("path", d="M410 130 C410 90 470 90 490 130 C500 160 490 200 450 205 C420 205 400 170 410 130Z", fill=TEAL)
    s.F("path", d="M430 92 L440 50 L458 90Z", fill=DTEAL)
    eye(s, 455, 135, 8)
    s.M("M90 330 l12 -18 l12 18 M220 330 l12 -18 l12 18 M350 300 l12 -18 l12 18", DTEAL, 8)
    s.F("rect", outline=False, x=0, y=330, width=512, height=182, fill=SKY, fill_opacity="0.55")
    s.M("M30 470 C80 455 120 485 170 470 M300 470 C350 455 390 485 440 470", WHITE, 8)


@reg("kraken")
def _(s):
    s.F("path", d="M110 230 C110 70 400 70 400 230 C400 280 360 310 340 310 H170 C150 310 110 280 110 230Z", fill=PURPLE)
    s.F("path", outline=False, d="M150 190 C160 120 220 96 270 98", fill="none", stroke=WHITE, stroke_width="16", stroke_linecap="round", stroke_opacity="0.4")
    eye(s, 205, 215, 16, BLACK, YEL)
    eye(s, 305, 215, 16, BLACK, YEL)
    for i, x in enumerate((70, 140, 210, 280, 350, 420)):
        s.raw(f'<path d="M{x + 30} 300 C{x - 30} 380 {x + 60} 400 {x} 470" fill="none" stroke="{INK}" stroke-width="36" stroke-linecap="round" data-outline="under"/>')
        s.raw(f'<path d="M{x + 30} 300 C{x - 30} 380 {x + 60} 400 {x} 470" fill="none" stroke="{PURPLE}" stroke-width="20" stroke-linecap="round"/>')
        s.F("circle", outline=False, cx=x + 10, cy=395, r=6, fill=PINK)


@reg("hydra")
def _(s):
    s.F("path", d="M120 460 C100 360 160 320 256 320 C352 320 412 360 392 460Z", fill=GREEN)
    for x, y, a in ((140, 130, -20), (256, 90, 0), (372, 130, 20)):
        s.raw(f'<path d="M256 340 C{256 + (x - 256) * 0.2} 260 {x} 250 {x} {y + 60}" fill="none" stroke="{INK}" stroke-width="48" stroke-linecap="round" data-outline="under"/>')
        s.raw(f'<path d="M256 340 C{256 + (x - 256) * 0.2} 260 {x} 250 {x} {y + 60}" fill="none" stroke="{GREEN}" stroke-width="28" stroke-linecap="round"/>')
        s.open(transform=f"rotate({a} {x} {y})")
        s.F("ellipse", cx=x, cy=y, rx=44, ry=34, fill=GREEN)
        s.F("path", d=f"M{x - 28} {y + 10} h56 v18 h-56Z", fill=LGREEN)
        eye(s, x - 14, y - 6, 6, BLACK, YEL)
        eye(s, x + 14, y - 6, 6, BLACK, YEL)
        s.F("path", d=f"M{x - 12} {y - 34} L{x - 18} {y - 56} L{x} {y - 36}Z", fill=TAN)
        s.close()


@reg("cerberus")
def _(s):
    s.F("rect", x=130, y=290, width=252, height=130, rx=56, fill="#3B3B44")
    s.F("rect", x=140, y=400, width=40, height=60, rx=14, fill="#3B3B44")
    s.F("rect", x=332, y=400, width=40, height=60, rx=14, fill="#3B3B44")
    for x, y, c in ((150, 190, 0.9), (256, 150, 1.1), (362, 190, 0.9)):
        s.open(transform=f"translate({x} {y}) scale({c}) translate(-256 -150)")
        s.F("ellipse", cx=256, cy=150, rx=60, ry=56, fill="#3B3B44")
        s.F("path", d="M210 110 L196 70 L236 96Z", fill="#3B3B44")
        s.F("path", d="M302 110 L316 70 L276 96Z", fill="#3B3B44")
        s.F("ellipse", cx=256, cy=185, rx=34, ry=24, fill="#5A5A64")
        s.F("circle", outline=False, cx=256, cy=176, r=9, fill=BLACK)
        eye(s, 232, 140, 6, BLACK, ORANGE)
        eye(s, 280, 140, 6, BLACK, ORANGE)
        s.F("path", outline=False, d="M246 200 C250 226 262 226 266 200Z", fill=RED)
        s.close()
    s.T("M382 330 C440 320 450 260 420 240", "#3B3B44", 18)
    flame(s, 420, 230, 0.4)


@reg("minotaur")
def _(s):
    s.F("rect", x=170, y=240, width=172, height=200, rx=60, fill=BROWN)
    s.F("rect", x=130, y=250, width=50, height=140, rx=22, fill=BROWN)
    s.F("rect", x=332, y=250, width=50, height=140, rx=22, fill=BROWN)
    s.F("rect", x=180, y=400, width=56, height=70, rx=18, fill=DBROWN)
    s.F("rect", x=276, y=400, width=56, height=70, rx=18, fill=DBROWN)
    s.F("ellipse", cx=256, cy=150, rx=80, ry=76, fill=BROWN)
    s.F("ellipse", cx=256, cy=190, rx=44, ry=34, fill=TAN)
    s.F("path", d="M190 110 C150 90 110 60 110 20 C150 40 190 60 210 90Z", fill=CREAM)
    s.F("path", d="M322 110 C362 90 402 60 402 20 C362 40 322 60 302 90Z", fill=CREAM)
    eye(s, 224, 140, 8)
    eye(s, 288, 140, 8)
    s.F("circle", outline=False, cx=244, cy=190, r=7, fill=BLACK)
    s.F("circle", outline=False, cx=268, cy=190, r=7, fill=BLACK)
    s.raw(f'<path d="M240 222 C244 240 268 240 272 222" fill="none" stroke="{GOLD}" stroke-width="8"/>')


@reg("chimera")
def _(s):
    s.F("rect", x=120, y=250, width=280, height=120, rx=56, fill=TAN)
    for x in (140, 210, 310, 370):
        s.F("rect", x=x, y=350, width=36, height=100, rx=14, fill=TAN)
    s.F("ellipse", cx=420, cy=210, rx=70, ry=62, fill="#E0A458")
    for a in range(0, 360, 30):
        x, y = arc_pt(420, 210, 74, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=18, fill=BROWN)
    s.F("circle", cx=420, cy=210, r=48, fill="#E0A458")
    eye(s, 405, 202, 5)
    eye(s, 436, 202, 5)
    s.F("path", outline=False, d="M405 224 h30 v10 h-30Z", fill=BROWN)
    wing_bat(s, 220, 250, 150, 130, DBROWN, 1)
    s.F("path", d="M110 290 C60 280 50 220 70 190 C80 250 100 260 120 270Z", fill=TAN)
    s.T("M110 300 C60 320 50 380 40 410", GREEN, 22)
    s.F("ellipse", cx=34, cy=420, rx=28, ry=20, fill=GREEN)
    eye(s, 28, 416, 5, BLACK, YEL)
    s.F("ellipse", cx=250, cy=130, rx=40, ry=34, fill=GREY)
    s.F("path", d="M230 112 L220 76 L252 100Z", fill=BROWN)
    s.F("path", d="M270 112 L282 78 L260 100Z", fill=BROWN)
    eye(s, 240, 128, 5)


@reg("basilisk")
def _(s):
    s.raw(f'<path d="M60 420 C100 330 180 340 240 400 C300 450 380 420 400 340 C415 290 370 260 345 280" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M60 420 C100 330 180 340 240 400 C300 450 380 420 400 340 C415 290 370 260 345 280" fill="none" stroke="{GREEN}" stroke-width="44" stroke-linecap="round"/>')
    s.F("path", d="M320 240 C320 180 400 160 430 210 C450 250 420 290 380 290 C340 290 320 270 320 240Z", fill=GREEN)
    s.F("path", d="M330 190 L340 140 L370 180 L390 140 L400 190Z", fill=YEL)
    eye(s, 392, 228, 9, BLACK, YEL)
    s.T("M425 255 C450 260 470 280 480 300", RED, 6)
    for x, y in ((150, 380), (230, 420), (330, 410)):
        s.F("polygon", outline=False, points=f"{x},{y - 16} {x + 12},{y} {x},{y + 16} {x - 12},{y}", fill=DGREEN)


@reg("cyclops")
def _(s):
    s.F("rect", x=150, y=270, width=212, height=190, rx=70, fill=GREEN)
    s.F("rect", x=90, y=280, width=64, height=140, rx=28, fill=GREEN)
    s.F("rect", x=358, y=280, width=64, height=140, rx=28, fill=GREEN)
    s.F("circle", cx=256, cy=170, r=110, fill=GREEN)
    s.F("circle", cx=256, cy=160, r=50, fill=WHITE)
    s.F("circle", cx=256, cy=164, r=26, fill="#3D8BFD")
    s.F("circle", outline=False, cx=256, cy=164, r=11, fill=BLACK)
    s.F("path", d="M190 120 C210 95 300 95 322 120", fill="none", stroke=DGREEN, stroke_width="14", stroke_linecap="round")
    s.F("path", d="M210 230 C240 270 280 270 310 230 C290 240 230 240 210 230Z", fill=WHITE)
    s.M("M215 232 C240 250 280 250 306 232", DGREEN, 6)
    s.T("M120 400 L60 460", BROWN, 22)
    s.F("circle", cx=48, cy=470, r=28, fill=BROWN)


@reg("medusas-head")
def _(s):
    for a in range(-170, 10, 22):
        x, y = arc_pt(256, 250, 130, a)
        x2, y2 = arc_pt(256, 250, 220, a + 14)
        s.raw(f'<path d="M{x:.0f} {y:.0f} C{x2:.0f} {y2 - 40:.0f} {x2 + 40:.0f} {y2:.0f} {x2:.0f} {y2 + 40:.0f}" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round" data-outline="under"/>')
        s.raw(f'<path d="M{x:.0f} {y:.0f} C{x2:.0f} {y2 - 40:.0f} {x2 + 40:.0f} {y2:.0f} {x2:.0f} {y2 + 40:.0f}" fill="none" stroke="{GREEN}" stroke-width="18" stroke-linecap="round"/>')
        s.F("circle", cx=f"{x2:.0f}", cy=f"{y2 + 40:.0f}", r=12, fill=DGREEN)
    s.F("circle", cx=256, cy=270, r=130, fill=LGREEN)
    eye(s, 214, 260, 11, BLACK, YEL)
    eye(s, 298, 260, 11, BLACK, YEL)
    s.M("M190 226 C205 216 225 216 238 226 M274 226 C287 216 307 216 322 226", DGREEN, 8)
    s.M("M222 340 C246 356 270 356 294 340", DRED, 9)


@reg("harpy")
def _(s):
    feather_wing(s, 220, 280, 190, 190, DBROWN, -1)
    feather_wing(s, 300, 280, 190, 190, DBROWN, 1)
    s.F("rect", x=210, y=180, width=92, height=160, rx=40, fill=SKIN)
    s.F("path", d="M200 330 C180 400 200 440 230 440 C250 410 260 380 256 340Z M312 330 C332 400 312 440 282 440 C262 410 252 380 256 340Z", fill=BROWN)
    s.F("circle", cx=256, cy=140, r=52, fill=SKIN)
    s.F("path", d="M200 140 C196 70 316 66 312 140 C300 110 214 110 200 140Z", fill=RED)
    eye(s, 238, 148, 6)
    eye(s, 274, 148, 6)
    s.M("M240 176 C250 184 264 184 272 176", DRED, 5)
    s.F("path", d="M226 440 l-12 36 M246 440 l-4 36 M278 440 l4 36 M296 440 l14 36", fill="none", stroke=DGOLD, stroke_width="10", stroke_linecap="round")


@reg("sphinx-creature")
def _(s):
    s.F("path", d="M40 440 V330 C40 290 90 270 150 270 H430 C470 270 480 320 470 370 V440Z", fill=SAND)
    s.F("rect", x=70, y=370, width=140, height=90, rx=24, fill=SAND)
    s.F("rect", x=70, y=440, width=360, height=26, rx=10, fill="#C9A86A")
    s.F("path", d="M110 280 C100 190 130 110 200 100 C270 110 300 190 290 280Z", fill=GOLD)
    s.F("path", d="M140 280 C140 200 160 150 200 140 C240 150 260 200 260 280Z", fill=SKIN)
    for y in (170, 200, 230):
        s.M(f"M110 {y} H150 M250 {y} H290", BLUE, 8)
    eye(s, 178, 192, 5)
    eye(s, 224, 192, 5)
    s.M("M185 228 C196 236 210 236 218 228", DRED, 5)
    s.T("M470 340 C500 340 505 300 480 290", SAND, 20)


@reg("manticore")
def _(s):
    s.F("rect", x=130, y=260, width=250, height=110, rx=52, fill=ORANGE)
    for x in (140, 200, 310, 350):
        s.F("rect", x=x, y=350, width=38, height=100, rx=14, fill=ORANGE)
    wing_bat(s, 230, 270, 160, 140, DRED, 1)
    s.F("circle", cx=412, cy=220, r=58, fill=SKIN)
    for a in range(0, 360, 30):
        x, y = arc_pt(412, 220, 62, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=18, fill=DRED)
    s.F("circle", cx=412, cy=220, r=44, fill=SKIN)
    eye(s, 398, 214, 5)
    eye(s, 428, 214, 5)
    s.M("M398 242 C408 252 420 252 430 242", DRED, 5)
    s.T("M130 290 C70 280 60 180 100 120", ORANGE, 24)
    s.F("polygon", points="100,120 80,80 120,90", fill=IRON)
    for x, y in ((70, 190), (66, 150), (84, 112)):
        s.F("polygon", outline=False, points=f"{x},{y} {x - 22},{y - 6} {x - 4},{y + 14}", fill=DRED)


@reg("roc")
def _(s):
    feather_wing(s, 250, 270, 240, 230, BROWN, -1)
    feather_wing(s, 270, 270, 240, 230, DBROWN, 1)
    s.F("ellipse", cx=260, cy=300, rx=70, ry=90, fill=BROWN)
    s.F("circle", cx=260, cy=190, r=44, fill=WHITE)
    s.F("path", d="M290 190 L340 206 L296 222Z", fill=YEL)
    eye(s, 274, 184, 6, BLACK, YEL)
    s.F("path", d="M240 390 l-20 50 M280 390 l20 50", fill="none", stroke=YEL, stroke_width="12", stroke_linecap="round")
    s.F("path", d="M232 380 L260 460 L288 380Z", fill=DBROWN)


@reg("thunderbird")
def _(s):
    feather_wing(s, 250, 260, 240, 200, BLUE, -1)
    feather_wing(s, 270, 260, 240, 200, "#2C5FC9", 1)
    s.F("ellipse", cx=260, cy=300, rx=64, ry=96, fill=NAVY)
    s.F("circle", cx=260, cy=190, r=44, fill=NAVY)
    s.F("path", d="M290 190 L340 206 L296 222Z", fill=ORANGE)
    eye(s, 274, 184, 6, BLACK, YEL)
    s.F("polygon", points="400,80 360,170 394,170 362,260 440,150 400,150 430,80", fill=YEL)
    s.F("polygon", points="110,100 80,170 106,170 84,230 140,150 112,150 134,100", fill=YEL)
    s.F("path", d="M230 390 l-14 50 M290 390 l14 50", fill="none", stroke=YEL, stroke_width="12", stroke_linecap="round")


@reg("phoenix")
def _(s):
    s.F("path", d="M256 340 C150 330 50 250 60 140 C100 220 160 250 220 260 C190 190 200 120 260 70 C320 120 330 190 300 260 C360 250 420 220 460 140 C470 250 370 330 256 340Z", fill=ORANGE)
    s.F("path", outline=False, d="M256 320 C190 300 140 250 130 190 C170 240 210 260 240 262 C230 220 236 170 256 130 C276 170 282 220 272 262 C302 260 342 240 382 190 C372 250 322 300 256 320Z", fill=YEL)
    s.F("ellipse", cx=256, cy=270, rx=44, ry=60, fill=RED)
    s.F("circle", cx=256, cy=200, r=36, fill=RED)
    s.F("path", d="M232 160 C232 100 256 80 256 60 C256 80 280 100 280 160Z", fill=ORANGE)
    s.F("path", d="M285 200 L322 214 L288 226Z", fill=YEL)
    eye(s, 268, 196, 5)
    s.F("path", d="M230 330 C200 400 140 440 100 470 C170 460 220 440 256 390 C292 440 342 460 412 470 C372 440 312 400 282 330Z", fill=ORANGE)
    s.F("path", outline=False, d="M256 390 C256 420 240 450 220 470 C250 460 270 430 256 390Z", fill=YEL)


@reg("griffin")
def _(s):
    s.F("rect", x=130, y=270, width=250, height=110, rx=52, fill="#E0A458")
    for x in (150, 214, 304, 360):
        s.F("rect", x=x, y=360, width=36, height=90, rx=14, fill="#E0A458")
    for x in (150, 214, 304, 360):
        s.F("path", d=f"M{x - 4} 448 h44 l-8 20 h-28Z", fill=GOLD)
    feather_wing(s, 230, 270, 190, 200, WHITE, 1)
    s.F("path", d="M110 300 C60 300 50 240 70 200 C80 260 100 270 120 280Z", fill="#E0A458")
    s.F("circle", cx=400, cy=210, r=56, fill=WHITE)
    s.F("path", d="M440 196 L490 220 L446 250Z", fill=GOLD)
    eye(s, 410, 196, 6, BLACK, YEL)
    s.F("path", d="M380 170 L372 120 L410 160Z", fill=WHITE)
    s.F("path", d="M400 160 L410 110 L430 160Z", fill=WHITE)


# ================================================================ other creatures
@reg("yeti")
def _(s):
    s.F("rect", x=140, y=250, width=232, height=200, rx=80, fill=WHITE)
    s.F("rect", x=70, y=250, width=80, height=190, rx=36, fill=WHITE)
    s.F("rect", x=362, y=250, width=80, height=190, rx=36, fill=WHITE)
    s.F("circle", cx=256, cy=170, r=110, fill=WHITE)
    s.F("ellipse", cx=256, cy=190, rx=64, ry=62, fill="#8FD0FF")
    eye(s, 230, 175, 8)
    eye(s, 282, 175, 8)
    s.F("ellipse", outline=False, cx=256, cy=212, rx=22, ry=14, fill=DB)
    s.M("M230 232 C246 244 266 244 282 232", INK, 6)
    s.F("rect", x=170, y=440, width=70, height=40, rx=16, fill=SKY)
    s.F("rect", x=272, y=440, width=70, height=40, rx=16, fill=SKY)
    s.F("polygon", points=star_pts(80, 90, 24, 9, 6), fill=SKY)


@reg("werewolf")
def _(s):
    s.F("circle", cx=380, cy=90, r=62, fill=YEL)
    s.F("circle", outline=False, cx=366, cy=76, r=18, fill="#F5C14A")
    s.F("rect", x=150, y=250, width=212, height=200, rx=70, fill="#6B5F55")
    s.F("rect", x=90, y=250, width=70, height=170, rx=30, fill="#6B5F55")
    s.F("rect", x=352, y=250, width=70, height=170, rx=30, fill="#6B5F55")
    s.F("path", d="M170 180 C150 100 190 70 256 70 C322 70 362 100 342 180 C330 230 290 250 256 250 C222 250 182 230 170 180Z", fill="#6B5F55")
    s.F("path", d="M180 100 L170 40 L226 80Z", fill="#6B5F55")
    s.F("path", d="M332 100 L342 40 L286 80Z", fill="#6B5F55")
    s.F("path", d="M226 180 H286 V236 C286 250 226 250 226 236Z", fill=CREAM)
    s.F("circle", outline=False, cx=256, cy=190, r=9, fill=BLACK)
    eye(s, 224, 150, 7, BLACK, YEL)
    eye(s, 288, 150, 7, BLACK, YEL)
    s.M("M236 230 l6 14 l6 -14 M262 230 l6 14 l6 -14", WHITE, 5)


@reg("vampire-bat-myth")
def _(s):
    wing_bat(s, 240, 280, 220, 190, "#3B3B44", -1)
    wing_bat(s, 272, 280, 220, 190, "#3B3B44", 1)
    s.F("ellipse", cx=256, cy=300, rx=58, ry=80, fill="#5A5A64")
    s.F("circle", cx=256, cy=210, r=50, fill="#5A5A64")
    s.F("path", d="M216 180 L202 120 L244 160Z", fill="#5A5A64")
    s.F("path", d="M296 180 L310 120 L268 160Z", fill="#5A5A64")
    eye(s, 238, 210, 7, BLACK, RED)
    eye(s, 274, 210, 7, BLACK, RED)
    s.F("polygon", outline=False, points="244,236 252,254 260,236", fill=WHITE)
    s.F("polygon", outline=False, points="256,236 264,254 272,236", fill=WHITE)


@reg("ghost")
def _(s):
    s.F("path", d="M110 450 V230 C110 100 400 100 400 230 V450 C380 420 360 480 330 440 C310 410 290 480 256 440 C222 480 200 410 180 440 C150 480 130 420 110 450Z", fill=WHITE)
    s.F("path", outline=False, d="M140 220 C150 160 200 130 250 130", fill="none", stroke=SKY, stroke_width="16", stroke_linecap="round", stroke_opacity="0.7")
    s.F("ellipse", cx=210, cy=230, rx=22, ry=30, fill=BLACK)
    s.F("ellipse", cx=302, cy=230, rx=22, ry=30, fill=BLACK)
    s.F("ellipse", cx=256, cy=320, rx=30, ry=40, fill=BLACK)
    s.F("path", d="M110 300 C60 290 40 250 60 240 C80 270 110 270 130 280Z", fill=WHITE)


@reg("zombie")
def _(s):
    s.F("rect", x=200, y=370, width=46, height=100, rx=16, fill=DGREY)
    s.F("rect", x=266, y=370, width=46, height=100, rx=16, fill=DGREY)
    s.F("rect", x=190, y=230, width=140, height=160, rx=40, fill=DB)
    s.F("rect", x=330, y=240, width=40, height=130, rx=18, fill=LGREEN, transform="rotate(-80 350 250)")
    s.F("rect", x=140, y=240, width=40, height=130, rx=18, fill=LGREEN, transform="rotate(-100 160 250)")
    s.F("circle", cx=256, cy=170, r=62, fill=LGREEN)
    s.F("path", d="M196 150 C196 100 316 100 316 150 C290 130 220 130 196 150Z", fill=HAIR)
    s.F("circle", cx=232, cy=170, r=14, fill=WHITE)
    s.F("circle", cx=284, cy=166, r=10, fill=WHITE)
    dot(s, 234, 172, 5)
    dot(s, 282, 168, 4)
    s.M("M232 206 H284 M244 200 v12 M258 200 v12 M272 200 v12", DGREEN, 5)
    s.M("M210 280 l18 14 M300 320 l16 -10", DGREEN, 5)


@reg("mummy-monster")
def _(s):
    s.F("path", d="M256 50 C190 50 170 100 176 160 C140 170 130 250 150 320 L156 450 H356 L362 320 C382 250 372 170 336 160 C342 100 322 50 256 50Z", fill=CREAM)
    for y in range(90, 450, 32):
        s.M(f"M{160 + (y % 3) * 4} {y} L{352 - (y % 4) * 3} {y + 14}", TAN, 10)
    s.F("rect", outline=False, x=190, y=110, width=132, height=40, rx=12, fill=BLACK)
    dot(s, 226, 130, 10, YEL)
    dot(s, 290, 130, 10, YEL)
    s.T("M360 220 C420 210 460 230 470 260", CREAM, 26)
    s.T("M150 300 C110 340 100 380 70 400", CREAM, 20)


@reg("troll")
def _(s):
    s.F("rect", x=140, y=250, width=232, height=200, rx=70, fill="#7A8B6A")
    s.F("rect", x=70, y=260, width=80, height=180, rx=34, fill="#7A8B6A")
    s.F("rect", x=362, y=260, width=80, height=180, rx=34, fill="#7A8B6A")
    s.F("circle", cx=256, cy=170, r=100, fill="#7A8B6A")
    s.F("path", d="M176 110 L120 80 L170 150Z M336 110 L392 80 L342 150Z", fill="#7A8B6A")
    s.F("ellipse", cx=256, cy=190, rx=30, ry=24, fill="#6A7B5A")
    eye(s, 216, 150, 9, BLACK, YEL)
    eye(s, 296, 150, 9, BLACK, YEL)
    s.M("M206 124 L238 136 M306 124 L274 136", INK, 7)
    s.M("M210 240 C240 262 272 262 302 240", INK, 7)
    s.F("polygon", outline=False, points="224,244 232,222 240,248", fill=WHITE)
    s.F("polygon", outline=False, points="276,248 284,222 292,244", fill=WHITE)
    s.T("M440 430 L470 220", BROWN, 22)
    s.F("circle", cx=470, cy=200, r=44, fill=DBROWN)


@reg("ogre")
def _(s):
    s.F("rect", x=130, y=240, width=252, height=210, rx=80, fill="#8CB369")
    s.F("rect", x=60, y=250, width=84, height=180, rx=36, fill="#8CB369")
    s.F("rect", x=368, y=250, width=84, height=180, rx=36, fill="#8CB369")
    s.F("rect", x=140, y=300, width=232, height=90, rx=30, fill=BROWN)
    s.F("circle", cx=256, cy=170, r=104, fill="#8CB369")
    s.F("path", d="M176 112 L150 70 L196 100Z M336 112 L362 70 L316 100Z", fill="#8CB369")
    eye(s, 218, 150, 10)
    eye(s, 294, 150, 10)
    s.M("M196 122 L236 134 M316 122 L276 134", INK, 8)
    s.F("ellipse", cx=256, cy=190, rx=22, ry=16, fill="#6F9250")
    s.F("path", d="M200 230 C230 270 282 270 312 230Z", fill=DBROWN)
    s.F("polygon", outline=False, points="224,236 232,258 240,238", fill=WHITE)
    s.F("polygon", outline=False, points="272,238 280,258 288,236", fill=WHITE)


@reg("goblin")
def _(s):
    s.F("rect", x=190, y=290, width=132, height=150, rx=44, fill=BROWN)
    s.F("rect", x=200, y=420, width=40, height=50, rx=14, fill=DBROWN)
    s.F("rect", x=272, y=420, width=40, height=50, rx=14, fill=DBROWN)
    s.F("rect", x=140, y=300, width=60, height=26, rx=12, fill="#8CB369")
    s.F("rect", x=312, y=300, width=60, height=26, rx=12, fill="#8CB369")
    s.F("circle", cx=256, cy=210, r=84, fill="#8CB369")
    s.F("path", d="M180 190 L90 150 L182 240Z", fill="#8CB369")
    s.F("path", d="M332 190 L422 150 L330 240Z", fill="#8CB369")
    eye(s, 224, 200, 11, BLACK, YEL)
    eye(s, 288, 200, 11, BLACK, YEL)
    s.F("path", d="M246 214 L256 250 L266 214Z", fill="#6F9250")
    s.M("M214 262 C240 280 272 280 298 262", INK, 7)
    s.F("polygon", outline=False, points="228,268 236,286 244,270", fill=WHITE)
    s.F("polygon", outline=False, points="268,270 276,286 284,268", fill=WHITE)


@reg("gnome")
def _(s):
    s.F("rect", x=190, y=300, width=132, height=130, rx=44, fill=DB)
    s.F("rect", x=196, y=420, width=44, height=44, rx=14, fill=DBROWN)
    s.F("rect", x=272, y=420, width=44, height=44, rx=14, fill=DBROWN)
    s.F("circle", cx=256, cy=240, r=62, fill=SKIN)
    s.F("path", d="M190 260 C180 350 250 390 256 390 C262 390 332 350 322 260 C300 300 212 300 190 260Z", fill=WHITE)
    s.F("path", d="M180 210 C190 100 256 40 280 20 C290 80 330 130 332 210Z", fill=RED)
    s.F("ellipse", cx=256, cy=252, rx=18, ry=14, fill="#E0A878")
    eye(s, 232, 232, 5)
    eye(s, 280, 232, 5)


@reg("dwarf-miner")
def _(s):
    s.F("rect", x=170, y=290, width=172, height=150, rx=44, fill=RED)
    s.F("rect", x=180, y=420, width=60, height=50, rx=14, fill=DBROWN)
    s.F("rect", x=272, y=420, width=60, height=50, rx=14, fill=DBROWN)
    s.F("circle", cx=256, cy=220, r=66, fill=SKIN)
    s.F("path", d="M186 250 C180 350 250 410 256 410 C262 410 332 350 326 250 C310 310 202 310 186 250Z", fill=DBROWN)
    s.F("path", d="M186 200 C186 130 326 130 326 200Z", fill=YEL)
    s.F("circle", cx=256, cy=150, r=18, fill=WHITE)
    s.F("circle", outline=False, cx=256, cy=150, r=10, fill=YEL)
    eye(s, 232, 224, 5)
    eye(s, 280, 224, 5)
    s.F("ellipse", cx=256, cy=250, rx=16, ry=12, fill="#E0A878")
    s.T("M380 440 L420 280", BROWN, 14)
    s.F("path", d="M380 280 C400 250 450 250 470 280 C440 270 410 275 400 295Z", fill=IRON)


@reg("elf")
def _(s):
    s.F("rect", x=190, y=290, width=132, height=160, rx=44, fill=DGREEN)
    s.F("rect", x=196, y=430, width=44, height=44, rx=14, fill=DBROWN)
    s.F("rect", x=272, y=430, width=44, height=44, rx=14, fill=DBROWN)
    s.F("circle", cx=256, cy=200, r=70, fill=SKIN)
    s.F("path", d="M190 210 L120 170 L196 250Z", fill=SKIN)
    s.F("path", d="M322 210 L392 170 L316 250Z", fill=SKIN)
    s.F("path", d="M184 190 C180 100 330 90 330 190 C310 150 230 130 184 190Z", fill="#F7E3A0")
    s.F("path", d="M184 190 C170 260 180 330 200 360 C190 300 200 240 210 200Z", fill="#F7E3A0")
    s.F("path", d="M328 190 C342 260 332 330 312 360 C322 300 312 240 302 200Z", fill="#F7E3A0")
    eye(s, 234, 204, 5, BLACK, SKY)
    eye(s, 280, 204, 5, BLACK, SKY)
    s.M("M240 236 C250 244 264 244 272 236", DRED, 5)
    s.T("M380 440 C440 380 440 200 390 150", BROWN, 12)
    s.M("M390 150 L380 440", TAN, 3)


@reg("giant")
def _(s):
    s.F("rect", x=130, y=230, width=252, height=240, rx=80, fill=SKIN)
    s.F("rect", x=130, y=300, width=252, height=110, rx=30, fill=BROWN)
    s.F("rect", x=60, y=240, width=84, height=200, rx=38, fill=SKIN)
    s.F("rect", x=368, y=240, width=84, height=200, rx=38, fill=SKIN)
    s.F("circle", cx=256, cy=150, r=84, fill=SKIN)
    s.F("path", d="M172 130 C172 60 340 60 340 130 C310 100 210 100 172 130Z", fill=DBROWN)
    eye(s, 226, 154, 8)
    eye(s, 286, 154, 8)
    s.F("ellipse", cx=256, cy=186, rx=16, ry=12, fill="#E0A878")
    s.M("M232 214 C246 224 266 224 280 214", DRED, 6)
    s.T("M70 160 L90 470", DBROWN, 24)
    s.F("circle", cx=66, cy=134, r=36, fill=DBROWN)
    for x in (60, 96):
        s.F("polygon", outline=False, points=f"{x},120 {x + 10},136 {x - 6},136", fill=GREY)


@reg("fairy")
def _(s):
    wing_bat(s, 256, 260, 140, 170, SKY, 1)
    wing_bat(s, 256, 260, 140, 170, PINK, -1)
    s.F("path", d="M210 250 H302 L330 380 H182Z", fill=PINK)
    s.F("circle", cx=256, cy=190, r=46, fill=SKIN)
    s.F("path", d="M208 190 C200 120 312 120 304 190 C290 150 224 150 208 190Z", fill=YEL)
    eye(s, 240, 194, 5)
    eye(s, 272, 194, 5)
    s.M("M244 214 C252 222 262 222 268 214", DRED, 5)
    s.F("rect", x=226, y=380, width=26, height=70, rx=10, fill=SKIN)
    s.F("rect", x=262, y=380, width=26, height=70, rx=10, fill=SKIN)
    s.T("M330 280 L420 200", GOLD, 8)
    s.F("polygon", points=star_pts(430, 190, 28, 12, 5), fill=YEL)
    for x, y in ((90, 120), (410, 380), (120, 400)):
        s.F("polygon", points=star_pts(x, y, 14, 6, 4), fill=YEL)


@reg("pixie")
def _(s):
    wing_bat(s, 256, 280, 110, 130, SKY, 1)
    wing_bat(s, 256, 280, 110, 130, "#B9A0FA", -1)
    s.F("path", d="M222 260 H290 L304 350 H208Z", fill=LGREEN)
    s.F("circle", cx=256, cy=210, r=42, fill=SKIN)
    s.F("path", d="M214 212 C200 150 242 130 256 150 C270 130 312 150 298 212 C288 170 224 170 214 212Z", fill=PURPLE)
    s.F("path", d="M214 200 L184 176 L220 224Z", fill=SKIN)
    s.F("path", d="M298 200 L328 176 L292 224Z", fill=SKIN)
    eye(s, 240, 214, 5)
    eye(s, 272, 214, 5)
    s.F("rect", x=232, y=350, width=20, height=60, rx=8, fill=SKIN)
    s.F("rect", x=262, y=350, width=20, height=60, rx=8, fill=SKIN)
    s.F("path", d="M232 404 h22 l4 12 h-30Z M262 404 h22 l4 12 h-30Z", fill=DGREEN)


@reg("genie")
def _(s):
    s.F("path", d="M256 310 C310 360 200 380 250 430 C290 470 340 460 320 500 C260 470 190 470 200 420 C210 380 310 360 256 310Z", fill=SKY)
    s.F("rect", x=170, y=200, width=172, height=130, rx=60, fill=SKY)
    s.F("rect", x=100, y=210, width=80, height=40, rx=18, fill=SKY, transform="rotate(30 140 230)")
    s.F("rect", x=332, y=210, width=80, height=40, rx=18, fill=SKY, transform="rotate(-30 372 230)")
    s.F("circle", cx=256, cy=150, r=54, fill=SKY)
    s.F("path", d="M210 120 C220 60 300 60 306 120 C280 100 240 100 210 120Z", fill=NAVY)
    s.F("circle", cx=256, cy=54, r=26, fill=NAVY)
    eye(s, 238, 150, 6)
    eye(s, 274, 150, 6)
    s.M("M240 176 C250 184 264 184 272 176", NAVY, 5)
    s.F("rect", x=206, y=250, width=100, height=26, rx=10, fill=GOLD)
    s.F("path", d="M100 440 C100 400 200 390 256 400 C300 390 360 400 380 430 C380 470 330 480 256 470 C180 480 100 470 100 440Z", fill=GOLD)
    s.F("path", outline=False, d="M130 430 C150 410 190 404 226 404", fill="none", stroke=WHITE, stroke_width="10", stroke_linecap="round", stroke_opacity="0.5")


@reg("golem")
def _(s):
    s.F("rect", x=130, y=240, width=252, height=190, rx=20, fill=STONE)
    s.F("rect", x=60, y=250, width=84, height=170, rx=20, fill="#9A948A")
    s.F("rect", x=368, y=250, width=84, height=170, rx=20, fill="#9A948A")
    s.F("rect", x=170, y=420, width=70, height=60, rx=14, fill="#9A948A")
    s.F("rect", x=272, y=420, width=70, height=60, rx=14, fill="#9A948A")
    s.F("rect", x=170, y=100, width=172, height=140, rx=20, fill=STONE)
    s.F("rect", outline=False, x=198, y=150, width=40, height=26, rx=6, fill=BLACK)
    s.F("rect", outline=False, x=274, y=150, width=40, height=26, rx=6, fill=BLACK)
    s.F("rect", outline=False, x=212, y=156, width=12, height=14, fill=ORANGE)
    s.F("rect", outline=False, x=288, y=156, width=12, height=14, fill=ORANGE)
    s.M("M210 210 H300", INK, 8)
    s.M("M150 300 L190 340 M330 280 L370 330 M270 380 L300 420", DGREY, 6)
    s.F("polygon", outline=False, points="256,270 280,296 256,322 232,296", fill=GREEN)


if __name__ == "__main__":
    run("fantasy-mythology", D, sys.argv[1:] or None)
