"""science drawings, part 2: atoms-molecules, matter-chemistry, forces-motion, simple-machines.
Run: python drawings/science2.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import WHITE  # noqa: E402
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, gear, person  # noqa: E402
from _parts import place as P  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run, star_pts  # noqa: E402

D = {}
RED, GREEN, YEL, ORANGE, PINK, SKY, GREY, DGREY = C["red"], C["green"], C["yellow"], C["orange"], C["pink"], C["sky"], C["grey"], C["darkgrey"]
BLUE, PURPLE, BROWN, DBROWN, TAN, GOLD = C["blue"], C["purple"], C["brown"], C["darkbrown"], C["tan"], C["gold"]
GLASS, GLASS_D = "#E3F3FC", "#BFE0F2"


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def ball(s, x, y, r, color):
    s.F("circle", cx=x, cy=y, r=r, fill=color)
    s.F("circle", outline=False, cx=round(x - r * 0.32, 1), cy=round(y - r * 0.32, 1), r=round(r * 0.26, 1), fill=WHITE, fill_opacity="0.55")


def orbit(s, rx, ry, rot, color=MID, w=7, cx=256, cy=256):
    s.raw(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-width="{w}" transform="rotate({rot} {cx} {cy})"/>')


def ring(s, cx, cy, r, color, w):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w + 20}" data-outline="under"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>')


def arrow(s, x1, y1, x2, y2, color=RED, w=22, hl=60):
    s.T(f"M{x1} {y1} L{x2} {y2}", color, w)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    tip = (x2 + 16 * math.cos(math.radians(a)), y2 + 16 * math.sin(math.radians(a)))
    p1 = (x2 + hl * math.cos(math.radians(a + 150)), y2 + hl * math.sin(math.radians(a + 150)))
    p2 = (x2 + hl * math.cos(math.radians(a - 150)), y2 + hl * math.sin(math.radians(a - 150)))
    s.F("polygon", points=f"{tip[0]:.0f},{tip[1]:.0f} {p1[0]:.0f},{p1[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}", fill=color)


# ================================================================ atoms-molecules
def atom_core(s, n=3, cx=256, cy=256, k=1.0):
    pts = [(0, 0), (22, -16), (-20, -20), (-4, 24), (24, 16), (-26, 12)][:n]
    cols = [RED, BLUE, RED, BLUE, RED, BLUE]
    for i, (dx, dy) in enumerate(pts):
        ball(s, cx + dx * k, cy + dy * k, 22 * k, cols[i])


@reg("atom")
def _(s):
    orbit(s, 190, 66, 0)
    orbit(s, 190, 66, 60)
    orbit(s, 190, 66, 120)
    atom_core(s, 4, k=1.5)
    for x, y in ((446, 256), (126, 144), (126, 368)):
        s.F("circle", cx=x, cy=y, r=20, fill=A2)


@reg("nucleus")
def _(s):
    atom_core(s, 6, k=4.2)


@reg("proton")
def _(s):
    s.F("circle", cx=256, cy=256, r=170, fill=RED)
    s.F("circle", outline=False, cx=196, cy=196, r=44, fill=WHITE, fill_opacity="0.4")
    s.M("M256 190 V322 M190 256 H322", WHITE, 30)


@reg("neutron")
def _(s):
    s.F("circle", cx=256, cy=256, r=170, fill=C["grey"])
    s.F("circle", outline=False, cx=196, cy=196, r=44, fill=WHITE, fill_opacity="0.55")
    s.M("M206 256 H306", DGREY, 30)


@reg("electron")
def _(s):
    s.F("circle", cx=256, cy=256, r=110, fill=A1)
    s.F("circle", outline=False, cx=216, cy=216, r=30, fill=WHITE, fill_opacity="0.45")
    s.M("M206 256 H306", WHITE, 26)
    orbit(s, 200, 70, -30, A1L, 8)


@reg("electron-shells")
def _(s):
    for r in (60, 110, 160, 210):
        s.raw(f'<circle cx="256" cy="256" r="{r}" fill="none" stroke="{MID}" stroke-width="7"/>')
    ball(s, 256, 256, 30, RED)
    for r, ang in ((110, 20), (110, 200), (160, 70), (160, 160), (160, 250), (160, 340), (210, 110), (210, 300)):
        x, y = arc_pt(256, 256, r, ang)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=16, fill=A1)


@reg("molecule")
def _(s):
    s.T("M140 340 L256 190 L380 330", GREY, 16)
    ball(s, 256, 190, 62, RED)
    ball(s, 140, 340, 48, A1)
    ball(s, 380, 330, 48, A1)
    ball(s, 396, 130, 34, A2)
    s.T("M300 160 L380 130", GREY, 14)


@reg("water-molecule")
def _(s):
    s.T("M256 220 L120 360 M256 220 L392 360", GREY, 16)
    ball(s, 256, 220, 90, RED)
    ball(s, 120, 360, 52, WHITE)
    ball(s, 392, 360, 52, WHITE)


@reg("carbon-dioxide-molecule")
def _(s):
    ball(s, 256, 256, 66, DGREY)
    ball(s, 100, 256, 58, RED)
    ball(s, 412, 256, 58, RED)
    s.M("M165 232 H178 M165 280 H178 M334 232 H347 M334 280 H347", WHITE, 6)


@reg("oxygen-molecule")
def _(s):
    ball(s, 176, 256, 96, RED)
    ball(s, 336, 256, 96, RED)


@reg("methane-molecule")
def _(s):
    s.T("M256 256 L256 100 M256 256 L130 350 M256 256 L390 350 M256 256 L300 430", GREY, 14)
    ball(s, 256, 256, 62, DGREY)
    for x, y in ((256, 100), (130, 350), (390, 350), (300, 430)):
        ball(s, x, y, 38, WHITE)


@reg("salt-crystal")
def _(s):
    s.F("polygon", points="256,70 420,160 420,340 256,430 92,340 92,160", fill="#F4F6FA")
    s.F("polygon", outline=False, points="256,70 420,160 256,250 92,160", fill=WHITE)
    s.F("polygon", outline=False, points="256,250 420,160 420,340 256,430", fill="#D9DEE8")
    s.M("M256 250 V430", INK, 6)


@reg("diamond-structure")
def _(s):
    pts = [(256, 90), (130, 190), (382, 190), (256, 290), (130, 380), (382, 380)]
    s.T("M256 90 L130 190 M256 90 L382 190 M130 190 L256 290 M382 190 L256 290 M130 190 L130 380 M382 190 L382 380 M256 290 L130 380 M256 290 L382 380", GREY, 10)
    for x, y in pts:
        ball(s, x, y, 36, A1)


@reg("chemical-bond")
def _(s):
    ball(s, 130, 256, 80, RED)
    ball(s, 382, 256, 80, A1)
    s.T("M190 256 H322", DGREY, 22)
    s.F("circle", cx=256, cy=256, r=20, fill=YEL)


@reg("ion")
def _(s):
    ball(s, 256, 256, 150, A1)
    s.M("M200 256 H312 M256 200 V312", WHITE, 30)
    ring(s, 256, 256, 200, MID, 4)


@reg("isotope")
def _(s):
    ball(s, 150, 256, 100, A1)
    ball(s, 360, 256, 120, A2)
    s.M("M100 256 H200", WHITE, 20)
    s.M("M310 256 H410 M360 206 V306", WHITE, 20)


@reg("radioactive-decay")
def _(s):
    s.F("circle", cx=180, cy=256, r=110, fill=YEL)
    s.F("path", outline=False, d="M180 256 L180 150 A106 106 0 0 1 272 203Z M180 256 L272 309 A106 106 0 0 1 88 309Z M180 256 L88 203 A106 106 0 0 1 180 150Z", fill=DGREY)
    s.F("circle", cx=180, cy=256, r=26, fill=YEL)
    arrow(s, 300, 256, 420, 256, A2, 18, 40)
    ball(s, 440, 170, 28, A1)
    ball(s, 440, 342, 20, A2L)


@reg("nuclear-fission")
def _(s):
    ball(s, 256, 256, 100, A1)
    arrow(s, 40, 256, 140, 256, A2, 16, 36)
    ball(s, 400, 150, 60, A2)
    ball(s, 400, 362, 60, A2)
    s.M("M420 256 L470 256", A2, 12)
    s.M("M350 210 L330 180 M350 300 L330 330", YEL, 12)


@reg("nuclear-fusion")
def _(s):
    ball(s, 100, 180, 56, A1)
    ball(s, 100, 332, 56, A1)
    arrow(s, 170, 256, 250, 256, A2, 16, 36)
    ball(s, 380, 256, 96, A2)
    s.F("polygon", points=star_pts(440, 120, 44, 20, 8), fill=YEL)
    s.F("polygon", points=star_pts(440, 392, 36, 16, 8), fill=YEL)


# ================================================================ matter-chemistry
@reg("states-of-matter")
def _(s):
    for x in (36, 188, 340):
        s.F("rect", x=x, y=130, width=136, height=250, rx=26, fill=GLASS)
    s.F("rect", x=62, y=250, width=84, height=84, rx=14, fill=A1L)
    s.F("rect", outline=False, x=72, y=260, width=26, height=14, rx=6, fill=WHITE, fill_opacity="0.8")
    s.F("path", outline=False, d="M196 290 C216 274 236 304 256 290 C276 274 296 304 316 290 V366 C316 372 312 374 306 374 H206 C200 374 196 372 196 366Z", fill=A1)
    for x, y in ((372, 190), (430, 230), (390, 280), (440, 330), (366, 340)):
        s.F("circle", outline=False, cx=x, cy=y, r=14, fill=A2)
    s.M("M104 110 V90 M256 110 V90 M408 110 V90", MID, 8)


@reg("solid")
def _(s):
    for i in range(3):
        for j in range(3):
            ball(s, 140 + i * 116, 140 + j * 116, 44, A1)
    s.T("M140 140 H372 M140 256 H372 M140 372 H372", A1L, 4)


@reg("liquid")
def _(s):
    s.F("path", d="M256 60 C330 160 400 230 400 320 C400 400 336 456 256 456 C176 456 112 400 112 320 C112 230 182 160 256 60Z", fill=A1)
    s.F("path", outline=False, d="M200 250 C180 290 176 330 200 380", fill="none", stroke=WHITE, stroke_width="20", stroke_linecap="round", stroke_opacity="0.65")


@reg("gas")
def _(s):
    s.F("rect", x=100, y=80, width=312, height=352, rx=34, fill=GLASS)
    for x, y, r, c in ((180, 160, 26, A2L), (300, 150, 22, A1L), (350, 250, 28, A2L), (210, 260, 24, A1L), (290, 340, 26, A2L), (170, 370, 20, A1L), (380, 370, 18, A1L)):
        s.F("circle", cx=x, cy=y, r=r, fill=c)
    s.M("M210 190 L260 230 M300 190 L330 210", MID, 6)


@reg("plasma")
def _(s):
    s.F("circle", cx=256, cy=256, r=110, fill=PURPLE)
    s.F("circle", outline=False, cx=256, cy=256, r=70, fill="#C9B0FF")
    for a in range(0, 360, 45):
        x, y = arc_pt(256, 256, 120, a)
        x2, y2 = arc_pt(256, 256, 210 if a % 90 == 0 else 180, a + 10)
        s.M(f"M{x:.0f} {y:.0f} L{(x + x2) / 2 + 14:.0f} {(y + y2) / 2 - 14:.0f} L{x2:.0f} {y2:.0f}", YEL, 12)


@reg("melting")
def _(s):
    s.F("path", d="M150 420 C110 430 120 468 170 470 H350 C410 468 410 428 360 420 Z", fill=A1)
    s.F("path", d="M150 70 H360 C380 70 392 82 392 102 V230 C392 250 380 262 360 262 H318 C318 300 330 340 306 346 C286 350 288 300 286 262 H226 C226 330 232 380 208 386 C188 390 188 320 190 262 H150 C130 262 118 250 118 230 V102 C118 82 130 70 150 70Z", fill=A1L)
    s.F("rect", outline=False, x=140, y=92, width=60, height=26, rx=12, fill=WHITE, fill_opacity="0.8")
    s.F("circle", outline=False, cx=300, cy=392, r=12, fill=A1)


@reg("freezing")
def _(s):
    s.F("path", d="M256 70 C330 170 380 230 380 310 C380 380 330 430 256 430 C182 430 132 380 132 310 C132 230 182 170 256 70Z", fill=A1L)
    s.M("M256 150 V380 M180 215 L332 345 M332 215 L180 345", WHITE, 14)
    s.F("circle", outline=False, cx=256, cy=262, r=20, fill=WHITE)


@reg("evaporation")
def _(s):
    s.F("path", d="M80 340 C100 320 140 320 160 340 C180 360 230 360 256 340 C282 320 330 320 352 340 C372 360 420 360 432 340 V440 H80Z", fill=A1)
    for x in (150, 256, 362):
        s.M(f"M{x} 270 C{x - 24} 230 {x + 24} 200 {x} 150 C{x - 20} 120 {x + 10} 100 {x} 80", A1L, 16)
    s.F("circle", cx=430, cy=80, r=44, fill=YEL)


@reg("condensation")
def _(s):
    s.F("rect", x=90, y=110, width=332, height=290, rx=30, fill=GLASS)
    for x, y in ((150, 180), (230, 250), (310, 170), (360, 280), (170, 330), (260, 360)):
        s.F("path", d=f"M{x} {y - 30} C{x + 26} {y} {x + 22} {y + 28} {x} {y + 28} C{x - 22} {y + 28} {x - 26} {y} {x} {y - 30}Z", fill=A1)
    s.M("M120 140 C110 200 118 250 130 280", WHITE, 12)


@reg("boiling")
def _(s):
    s.F("rect", x=100, y=210, width=312, height=190, rx=26, fill=DGREY)
    s.F("rect", outline=False, x=112, y=222, width=288, height=100, rx=12, fill=A1)
    for x, y, r in ((170, 300, 14), (230, 270, 18), (300, 300, 12), (350, 260, 16)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=WHITE, fill_opacity="0.8")
    for x in (170, 256, 342):
        s.M(f"M{x} 190 C{x - 24} 150 {x + 24} 120 {x} 70", MID, 14)
    s.F("path", d="M200 400 C190 440 210 450 220 470 C240 450 250 430 256 400Z", fill=A2)
    s.F("path", d="M290 400 C290 440 300 450 310 470 C330 450 340 430 340 400Z", fill=A2L)


@reg("sublimation")
def _(s):
    s.F("polygon", points="110,340 330,340 400,290 180,290", fill=WHITE)
    s.F("polygon", points="110,340 330,340 330,430 110,430", fill=A1L)
    s.F("polygon", points="330,340 400,290 400,380 330,430", fill=A1)
    for cx, cy, r in ((200, 230, 44), (270, 190, 52), (340, 220, 40), (240, 130, 38), (310, 100, 32)):
        s.F("circle", cx=cx, cy=cy, r=r, fill=WHITE, fill_opacity="0.92")
    s.M("M170 380 H280", WHITE, 10)


@reg("mixture")
def _(s):
    s.F("path", d="M110 90 H402 L388 430 C386 452 370 462 352 462 H160 C142 462 126 452 124 430Z", fill=GLASS)
    for x, y, r, c in ((190, 360, 20, RED), (260, 400, 18, YEL), (330, 350, 20, A1), (240, 320, 16, GREEN), (300, 420, 14, ORANGE), (180, 420, 14, PURPLE), (350, 410, 14, RED)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=c)
    s.M("M160 120 H240", WHITE, 12)


@reg("chemical-solution")
def _(s):
    s.F("path", d="M110 180 H402 L388 440 C386 462 370 470 352 470 H160 C142 470 126 462 124 440Z", fill=GLASS)
    s.F("path", outline=False, d="M118 240 H394 L388 440 C386 458 370 462 352 462 H160 C142 462 126 458 124 440Z", fill="#9BE0C8")
    s.F("rect", x=270, y=60, width=26, height=270, rx=10, fill=GREY, transform="rotate(14 280 190)")
    for x, y in ((170, 300), (230, 360), (330, 310)):
        s.F("circle", outline=False, cx=x, cy=y, r=8, fill=WHITE, fill_opacity="0.8")


@reg("chemical-reaction")
def _(s):
    s.F("path", d="M60 230 H150 V420 H60Z", fill=RED)
    ball(s, 105, 190, 24, RED)
    s.F("path", d="M160 230 H250 V420 H160Z", fill=A1)
    arrow(s, 262, 330, 340, 330, DARK, 14, 34)
    s.F("path", d="M360 200 H450 V420 H360Z", fill=PURPLE)
    s.F("circle", outline=False, cx=405, cy=300, r=26, fill=WHITE, fill_opacity="0.7")
    s.F("polygon", points=star_pts(400, 130, 40, 16, 8), fill=YEL)


@reg("combustion")
def _(s):
    s.F("path", d="M256 40 C300 120 400 170 400 290 C400 390 330 460 256 460 C182 460 112 390 112 290 C112 220 160 190 180 130 C200 170 220 180 230 160 C240 130 230 80 256 40Z", fill=A2)
    s.F("path", outline=False, d="M256 190 C290 250 340 280 340 340 C340 400 300 430 256 430 C212 430 172 400 172 340 C172 290 220 260 256 190Z", fill=YEL)
    s.F("path", outline=False, d="M256 300 C276 330 300 350 296 380 C292 410 220 410 216 380 C212 350 240 330 256 300Z", fill=WHITE)


@reg("rusting")
def _(s):
    s.open(transform="rotate(-38 256 256)")
    s.F("rect", x=100, y=236, width=300, height=40, rx=8, fill=GREY)
    s.F("polygon", points="400,236 400,276 470,256", fill=GREY)
    s.F("ellipse", cx=96, cy=256, rx=26, ry=60, fill=DGREY)
    for x, y, r, c in ((190, 256, 34, "#C2622E"), (280, 252, 28, "#9A4A20"), (350, 258, 24, "#C2622E"), (150, 240, 20, "#9A4A20")):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=c)
    s.close()
    for x, y, r in ((130, 400, 14), (190, 440, 10), (330, 420, 12)):
        s.F("rect", outline=False, x=x, y=y, width=r * 1.6, height=r, rx=3, fill="#C2622E", transform=f"rotate(30 {x} {y})")


@reg("acid")
def _(s):
    s.F("path", d="M190 60 H322 V160 L400 420 C410 450 395 468 368 468 H144 C117 468 102 450 112 420 L190 160Z", fill=GLASS)
    s.F("path", outline=False, d="M142 330 H370 L398 420 C404 442 392 458 366 458 H146 C120 458 108 442 114 420Z", fill=RED)
    s.F("circle", cx=256, cy=258, r=44, fill=RED)
    s.M("M228 258 H284", WHITE, 14)


@reg("base")
def _(s):
    s.F("path", d="M190 60 H322 V160 L400 420 C410 450 395 468 368 468 H144 C117 468 102 450 112 420 L190 160Z", fill=GLASS)
    s.F("path", outline=False, d="M142 330 H370 L398 420 C404 442 392 458 366 458 H146 C120 458 108 442 114 420Z", fill=BLUE)
    s.F("circle", cx=256, cy=258, r=44, fill=BLUE)
    s.M("M228 258 H284 M256 230 V286", WHITE, 14)


@reg("neutralisation")
def _(s):
    s.F("path", d="M120 150 H250 L226 440 H144Z", fill=RED)
    s.F("path", d="M262 150 H392 L368 440 H286Z", fill=BLUE)
    s.F("circle", cx=256, cy=100, r=36, fill=GREEN)
    s.M("M236 100 H276", WHITE, 12)


@reg("indicator-colour-change")
def _(s):
    for x, c in ((120, RED), (256, GREEN), (392, PURPLE)):
        s.F("path", d=f"M{x - 38} 100 H{x + 38} V360 C{x + 38} 430 {x - 38} 430 {x - 38} 360Z", fill=GLASS)
        s.F("path", outline=False, d=f"M{x - 32} 220 H{x + 32} V360 C{x + 32} 420 {x - 32} 420 {x - 32} 360Z", fill=c)
    s.M("M170 250 H210 M300 250 H340", DGREY, 12)


@reg("crystals")
def _(s):
    s.F("polygon", points="256,40 310,150 290,400 222,400 202,150", fill=A1L)
    s.F("polygon", outline=False, points="256,40 310,150 256,170", fill=WHITE, fill_opacity="0.6")
    s.F("polygon", points="150,200 190,260 170,420 120,420 100,260", fill=A1)
    s.F("polygon", points="360,220 410,280 400,420 340,420 320,280", fill=A1)
    s.F("rect", x=70, y=410, width=370, height=34, rx=12, fill=DGREY)


@reg("density-tower")
def _(s):
    s.F("path", d="M170 60 H342 V400 C342 440 320 460 256 460 C192 460 170 440 170 400Z", fill=GLASS)
    for y0, y1, c in ((350, 460, "#C98A3C"), (290, 350, "#FFD36B"), (240, 290, "#B7E3B0"), (190, 240, "#9AD0F2"), (140, 190, "#F7A1B5")):
        s.F("rect", outline=False, x=176, y=y0, width=160, height=y1 - y0, fill=c)
    s.raw(f'<path d="M170 60 H342 V400 C342 440 320 460 256 460 C192 460 170 440 170 400Z" fill="none" stroke="{INK}" stroke-width="10" stroke-linejoin="round" data-outline="stroke"/>')


@reg("volcano-experiment")
def _(s):
    s.F("path", d="M80 450 L190 200 H322 L432 450Z", fill=BROWN)
    s.F("path", outline=False, d="M190 200 H322 L336 235 H176Z", fill=DBROWN)
    s.F("path", d="M200 200 C190 150 220 120 220 90 C240 110 250 80 256 50 C270 90 300 110 300 140 C320 130 330 170 316 200Z", fill=RED)
    s.F("path", outline=False, d="M236 200 C236 170 256 150 256 130 C272 150 286 170 280 200Z", fill=ORANGE)
    for x, y in ((140, 110), (390, 120), (370, 60)):
        s.F("circle", outline=False, cx=x, cy=y, r=16, fill=RED)


@reg("elephant-toothpaste-experiment")
def _(s):
    s.F("path", d="M190 200 H322 V440 C322 456 308 462 296 462 H216 C204 462 190 456 190 440Z", fill=GLASS)
    for y in range(40, 240, 40):
        s.F("rect", outline=False, x=214 + 16 * math.sin(y / 20), y=y, width=84, height=60, rx=30, fill=PINK if (y // 40) % 2 else WHITE)
    s.F("path", d="M230 210 C190 120 200 60 256 40 C312 60 322 120 282 210Z", fill=PINK)
    s.M("M230 120 C240 100 250 100 262 70", WHITE, 10)


@reg("catalyst")
def _(s):
    ball(s, 90, 330, 48, A1)
    ball(s, 170, 400, 40, A2)
    arrow(s, 230, 350, 390, 350, DARK, 16, 38)
    s.F("polygon", points=star_pts(310, 190, 70, 34, 6), fill=GREEN)
    s.M("M310 262 V320", GREEN, 12)
    s.F("circle", cx=440, cy=350, r=54, fill=PURPLE)
    s.F("circle", outline=False, cx=424, cy=334, r=14, fill=WHITE, fill_opacity="0.5")


# ================================================================ forces-motion
@reg("force")
def _(s):
    s.F("rect", x=250, y=190, width=140, height=140, rx=18, fill=A1)
    arrow(s, 40, 260, 240, 260, RED, 28, 70)
    s.M("M290 220 H350", WHITE, 12)


@reg("push-and-pull")
def _(s):
    s.F("rect", x=190, y=200, width=132, height=132, rx=16, fill=A2)
    arrow(s, 40, 266, 180, 266, A1, 22, 56)
    arrow(s, 472, 266, 332, 266, RED, 22, 56)


@reg("gravity")
def _(s):
    s.F("circle", cx=256, cy=380, r=130, fill=A1L)
    s.F("path", outline=False, d="M170 330 C200 300 250 310 270 330 C300 350 350 330 380 350 C400 380 380 400 340 410 C290 440 190 420 170 380Z", fill=GREEN)
    s.F("circle", cx=256, cy=100, r=34, fill=A2)
    arrow(s, 256, 150, 256, 238, RED, 18, 44)


@reg("friction")
def _(s):
    s.F("rect", x=60, y=360, width=392, height=70, rx=14, fill=DGREY)
    s.F("rect", x=140, y=220, width=190, height=130, rx=18, fill=A2)
    for x in range(80, 440, 40):
        s.M(f"M{x} 380 l16 -14", GREY, 6)
    arrow(s, 100, 288, 126, 288, A1, 16, 30)
    arrow(s, 420, 340, 340, 340, RED, 18, 40)


@reg("air-resistance")
def _(s):
    s.F("path", d="M110 150 C110 40 400 40 400 150Z", fill=RED)
    s.F("path", outline=False, d="M180 70 C200 60 240 56 256 56 V150 H110 C110 110 140 80 180 70Z", fill=A2L)
    s.T("M120 150 L240 300 M256 150 V300 M390 150 L270 300", DGREY, 8)
    s.F("rect", x=216, y=300, width=80, height=100, rx=24, fill=A1)
    s.M("M60 260 H110 M60 320 H120 M410 260 H460 M400 330 H450", MID, 10)


@reg("buoyancy")
def _(s):
    s.F("rect", x=40, y=210, width=432, height=240, rx=24, fill=A1L)
    s.F("path", outline=False, d="M40 230 C100 200 160 260 220 230 C280 200 340 260 400 230 C430 215 450 225 472 235 V210 H40Z", fill=A1)
    s.F("path", d="M150 200 H370 L340 270 H180Z", fill=RED)
    s.F("rect", x=250, y=80, width=10, height=120, rx=4, fill=DGREY)
    s.F("path", d="M262 80 L340 150 H262Z", fill=WHITE)
    arrow(s, 256, 420, 256, 330, GREEN, 18, 40)


@reg("pressure-gauge")
def _(s):
    s.F("circle", cx=256, cy=250, r=190, fill=WHITE)
    ring(s, 256, 250, 190, GREY, 24)
    for i in range(9):
        a = 150 + i * 30
        x1, y1 = arc_pt(256, 250, 140, a)
        x2, y2 = arc_pt(256, 250, 170, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DGREY, 10)
    s.M("M256 250 L330 160", RED, 14)
    s.F("circle", cx=256, cy=250, r=24, fill=DARK)
    s.F("rect", x=226, y=430, width=60, height=50, rx=8, fill=GOLD)


@reg("newtons-cradle")
def _(s):
    s.T("M70 90 H442", DGREY, 20)
    s.F("rect", x=50, y=60, width=14, height=380, rx=6, fill=DGREY)
    s.F("rect", x=448, y=60, width=14, height=380, rx=6, fill=DGREY)
    for i in range(5):
        x = 156 + i * 50
        if i == 0:
            s.M(f"M{x} 90 L{x - 70} 330", DGREY, 6)
            s.F("circle", cx=x - 70, cy=355, r=26, fill=GREY)
        elif i == 4:
            s.M(f"M{x} 90 L{x + 70} 330", DGREY, 6)
            s.F("circle", cx=x + 70, cy=355, r=26, fill=GREY)
        else:
            s.M(f"M{x} 90 V380", DGREY, 6)
            s.F("circle", cx=x, cy=406, r=26, fill=GREY)
    s.F("rect", x=36, y=436, width=440, height=30, rx=12, fill=BROWN)


@reg("inertia")
def _(s):
    s.F("rect", x=40, y=300, width=432, height=34, rx=10, fill=DGREY)
    s.F("rect", x=150, y=230, width=170, height=76, rx=16, fill=A1)
    s.F("circle", cx=256, cy=150, r=34, fill=A2)
    s.F("rect", x=232, y=185, width=48, height=48, rx=10, fill=A2L)
    s.F("circle", cx=190, cy=350, r=24, fill=DARK)
    s.F("circle", cx=290, cy=350, r=24, fill=DARK)
    arrow(s, 460, 230, 400, 230, RED, 12, 30)


@reg("momentum")
def _(s):
    s.F("circle", cx=300, cy=270, r=110, fill=A2)
    s.F("circle", outline=False, cx=260, cy=230, r=30, fill=WHITE, fill_opacity="0.5")
    arrow(s, 100, 270, 190, 270, RED, 20, 46)
    s.M("M30 220 H100 M20 270 H80 M30 320 H100", MID, 10)


@reg("acceleration")
def _(s):
    s.F("rect", x=40, y=380, width=432, height=34, rx=10, fill=DGREY)
    for i, (x, sc) in enumerate(((60, 0.5), (150, 0.62), (250, 0.8))):
        s.open(transform=f"translate({x} {380 - 90 * sc}) scale({sc})")
        s.F("rect", x=0, y=20, width=170, height=80, rx=24, fill=A1 if i == 2 else A1L)
        s.F("path", d="M30 20 L60 -10 H120 L150 20Z", fill=GLASS)
        s.F("circle", cx=40, cy=100, r=22, fill=DARK)
        s.F("circle", cx=130, cy=100, r=22, fill=DARK)
        s.close()
    arrow(s, 110, 130, 330, 130, RED, 20, 46)


@reg("speed-and-velocity")
def _(s):
    s.F("path", d="M60 360 A196 196 0 0 1 452 360Z", fill=WHITE)
    ring(s, 256, 360, 196, GREY, 16)
    for i in range(8):
        a = 180 + i * 180 / 7
        x1, y1 = arc_pt(256, 360, 150, a)
        x2, y2 = arc_pt(256, 360, 176, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DGREY, 8)
    for c, a0, a1 in ((GREEN, 180, 250), (YEL, 250, 310), (RED, 310, 360)):
        x1, y1 = arc_pt(256, 360, 120, a0)
        x2, y2 = arc_pt(256, 360, 120, a1)
        s.raw(f'<path d="M{x1:.0f} {y1:.0f} A120 120 0 0 1 {x2:.0f} {y2:.0f}" fill="none" stroke="{c}" stroke-width="22"/>')
    s.M("M256 360 L350 230", RED, 14)
    s.F("circle", cx=256, cy=360, r=26, fill=DARK)


@reg("action-and-reaction")
def _(s):
    s.F("rect", x=40, y=410, width=432, height=30, rx=10, fill=GREEN)
    s.open(transform="rotate(-18 230 300)")
    s.F("rect", x=150, y=250, width=190, height=80, rx=30, fill=DGREY)
    s.F("rect", x=320, y=240, width=40, height=100, rx=10, fill=GREY)
    s.close()
    s.F("circle", cx=190, cy=380, r=46, fill=DBROWN)
    s.F("circle", outline=False, cx=190, cy=380, r=14, fill=TAN)
    s.F("circle", cx=446, cy=130, r=34, fill=DARK)
    s.F("polygon", points=star_pts(380, 220, 40, 18, 8), fill=YEL)
    arrow(s, 150, 160, 80, 160, A1, 14, 34)
    arrow(s, 330, 110, 400, 110, RED, 14, 34)


@reg("centripetal-force")
def _(s):
    s.raw(f'<circle cx="256" cy="256" r="150" fill="none" stroke="{MID}" stroke-width="8" stroke-dasharray="16 14"/>')
    s.T("M256 256 L406 256", DGREY, 8)
    ball(s, 406, 256, 40, A2)
    s.F("circle", cx=256, cy=256, r=30, fill=A1)
    arrow(s, 366, 256, 296, 256, RED, 14, 34)
    arrow(s, 406, 200, 406, 120, A1, 12, 30)


@reg("pendulum")
def _(s):
    s.F("rect", x=130, y=50, width=252, height=26, rx=10, fill=DGREY)
    s.raw(f'<line x1="256" y1="76" x2="150" y2="360" stroke="{DGREY}" stroke-width="8" stroke-linecap="round"/>')
    s.raw(f'<path d="M256 330 A260 260 0 0 0 150 360" fill="none" stroke="{MID}" stroke-width="6" stroke-dasharray="10 12"/>')
    s.raw(f'<path d="M256 330 A260 260 0 0 1 362 360" fill="none" stroke="{MID}" stroke-width="6" stroke-dasharray="10 12"/>')
    s.raw(f'<line x1="256" y1="76" x2="256" y2="420" stroke="{MID}" stroke-width="5" stroke-dasharray="8 12"/>')
    ball(s, 150, 390, 50, A2)
    s.F("circle", outline=False, cx=362, cy=370, r=40, fill=A2L, fill_opacity="0.6")


@reg("projectile-motion")
def _(s):
    s.F("rect", x=40, y=420, width=432, height=30, rx=10, fill=GREEN)
    s.raw(f'<path d="M80 400 C160 60 360 60 440 400" fill="none" stroke="{MID}" stroke-width="8" stroke-dasharray="16 14"/>')
    ball(s, 256, 130, 34, A2)
    s.F("circle", cx=80, cy=392, r=26, fill=A1)
    ball(s, 440, 396, 20, A2L)


@reg("tension")
def _(s):
    s.F("rect", x=30, y=180, width=80, height=150, rx=14, fill=DGREY)
    s.F("rect", x=402, y=180, width=80, height=150, rx=14, fill=DGREY)
    s.T("M110 255 H402", TAN, 20)
    for x in range(150, 380, 30):
        s.M(f"M{x} 244 l14 22", BROWN, 5)
    arrow(s, 160, 130, 60, 130, RED, 14, 34)
    arrow(s, 352, 130, 452, 130, RED, 14, 34)


@reg("weight-vs-mass")
def _(s):
    s.F("path", d="M80 400 H200 L210 440 H70Z", fill=GREY)
    s.F("path", d="M312 400 H432 L442 440 H302Z", fill=GREY)
    ball(s, 140, 310, 80, A2)
    ball(s, 372, 310, 80, A2)
    s.F("circle", cx=140, cy=90, r=40, fill=A1L)
    s.F("circle", cx=372, cy=90, r=26, fill=MID)
    arrow(s, 140, 150, 140, 215, RED, 14, 30)
    arrow(s, 372, 140, 372, 190, RED, 10, 22)


@reg("falling-apple")
def _(s):
    s.F("rect", x=40, y=420, width=432, height=34, rx=10, fill=GREEN)
    s.T("M120 420 V230", BROWN, 40)
    s.F("circle", cx=140, cy=170, r=90, fill=C["darkgreen"])
    s.F("circle", outline=False, cx=110, cy=140, r=30, fill=GREEN)
    s.F("circle", cx=330, cy=300, r=44, fill=RED)
    s.F("path", d="M330 260 C330 244 344 236 354 236", fill="none", stroke=BROWN, stroke_width="10", stroke_linecap="round")
    s.F("path", d="M340 250 C350 230 372 232 378 240 C366 252 350 256 340 250Z", fill=GREEN)
    s.M("M290 240 V180 M330 220 V160", MID, 8)
    arrow(s, 330, 330, 330, 400, A1, 14, 32)


# ================================================================ simple-machines
@reg("lever")
def _(s):
    s.F("polygon", points="256,320 196,430 316,430", fill=BROWN)
    s.T("M60 300 L450 210", TAN, 28)
    ball(s, 110, 270, 40, A2)
    arrow(s, 410, 120, 410, 190, RED, 16, 38)


@reg("pulley")
def _(s):
    s.F("rect", x=130, y=40, width=252, height=30, rx=10, fill=DGREY)
    s.T("M256 70 V120", DGREY, 12)
    ring(s, 256, 180, 60, A1, 24)
    s.F("circle", cx=256, cy=180, r=14, fill=DARK)
    s.T("M196 180 V380 M316 180 V270", TAN, 10)
    s.F("rect", x=170, y=370, width=92, height=92, rx=14, fill=A2)
    arrow(s, 316, 290, 316, 380, RED, 14, 34)


@reg("wheel-and-axle")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=A2)
    s.F("circle", outline=False, cx=256, cy=256, r=140, fill=A2L)
    for a in range(0, 180, 45):
        x1, y1 = arc_pt(256, 256, 180, a)
        x2, y2 = arc_pt(256, 256, 180, a + 180)
        s.T(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DBROWN, 12)
    s.F("circle", cx=256, cy=256, r=44, fill=GREY)
    s.F("circle", cx=256, cy=256, r=16, fill=DGREY)


@reg("inclined-plane")
def _(s):
    s.F("polygon", points="50,420 450,420 450,170", fill=TAN)
    s.F("polygon", outline=False, points="130,420 450,420 450,200", fill=C["cream"], fill_opacity="0.6")
    s.open(transform="rotate(-24 230 310)")
    s.F("rect", x=180, y=260, width=100, height=70, rx=12, fill=A1)
    s.close()


@reg("wedge")
def _(s):
    s.F("rect", x=70, y=260, width=372, height=190, rx=26, fill=BROWN)
    s.F("ellipse", cx=256, cy=260, rx=186, ry=44, fill=TAN)
    s.M("M120 260 C160 245 200 275 256 260", DBROWN, 6)
    s.M("M256 260 L256 330", DBROWN, 8)
    s.F("polygon", points="206,250 306,250 256,370", fill=GREY)
    s.F("polygon", outline=False, points="222,254 256,254 256,336", fill=WHITE, fill_opacity="0.55")
    s.F("rect", x=196, y=190, width=120, height=64, rx=14, fill=DGREY)
    s.F("rect", x=232, y=90, width=48, height=110, rx=14, fill=TAN)


@reg("screw")
def _(s):
    s.F("path", d="M150 70 H362 V120 H150Z", fill=GREY)
    s.F("rect", x=214, y=120, width=84, height=270, fill=GREY)
    s.F("polygon", points="214,390 298,390 256,466", fill=GREY)
    for y in range(150, 400, 38):
        s.F("path", outline=False, d=f"M200 {y + 20} L312 {y - 16} V{y + 2} L200 {y + 38}Z", fill=DGREY)
    s.M("M238 150 V384", WHITE, 8)


@reg("gear-machine")
def _(s):
    P(s, gear, 190, 200, 0.85, color=A1)
    P(s, gear, 360, 340, 0.7, color=A2)
    s.F("circle", cx=190, cy=200, r=16, fill=DARK)
    s.F("circle", cx=360, cy=340, r=14, fill=DARK)


@reg("seesaw-lever")
def _(s):
    s.F("polygon", points="256,320 196,430 316,430", fill=A1)
    s.T("M70 260 L440 190", TAN, 26)
    s.F("rect", x=90, y=180, width=70, height=70, rx=12, fill=A2, transform="rotate(-10 125 215)")
    s.F("circle", cx=410, cy=150, r=44, fill=A1L)
    s.F("rect", x=40, y=430, width=432, height=26, rx=10, fill=GREEN)


if __name__ == "__main__":
    run("science", D, sys.argv[1:] or None)
