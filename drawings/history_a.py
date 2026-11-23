"""history drawings A: human origins, Egypt, Mesopotamia, Indus, China, Greece, Rome, Persia, Americas.
Run: python drawings/history_a.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hist import *  # noqa: E402,F401,F403
from _hist import (A1, A2, BLACK, BLUE, BROWN, CREAM, DBROWN, DGOLD, DGREEN, DGREY, DRED, DSAND, DSTONE, GOLD, GREEN, GREY, HAIR, IRON, ORANGE, PINK, PURPLE, RED, SAND, SKIN, SKIN_D, SKY, STONE, TAN, WHITE, YEL, arc_pt, column, dot, flame, ground, lines, person, pyramid, registry, ring, run, scroll, star_pts, sun_disc, txt)  # noqa: E402

D, reg = registry()


# ================================================================ human-origins
@reg("early-humans")
def _(s):
    person(s, 180, 470, 0.9, shirt=TAN, pants=BROWN, skin=SKIN_D)
    person(s, 360, 470, 0.7, shirt=BROWN, pants=DBROWN, skin=SKIN_D)
    s.T("M130 250 L90 140", DBROWN, 10)
    s.F("polygon", points="90,140 74,176 106,168", fill=STONE)


@reg("human-evolution-chart")
def _(s):
    for i, (x, tilt, k, c) in enumerate(((70, 38, 0.62, "#6E4A2A"), (180, 24, 0.72, "#7A5638"), (290, 10, 0.84, "#8C6A4A"), (400, 0, 1.0, "#A07C58"))):
        s.open(transform=f"translate({x} 430) scale({k}) rotate({tilt} 0 0)")
        s.F("circle", cx=0, cy=-250, r=40, fill=c)
        s.F("rect", x=-36, y=-215, width=72, height=130, rx=34, fill=c)
        s.F("rect", x=-60, y=-205, width=26, height=110, rx=13, fill=c, transform="rotate(8 -47 -150)")
        s.F("rect", x=34, y=-205, width=26, height=110, rx=13, fill=c, transform="rotate(-8 47 -150)")
        s.F("rect", x=-34, y=-100, width=30, height=100, rx=14, fill=c)
        s.F("rect", x=4, y=-100, width=30, height=100, rx=14, fill=c)
        s.close()
    s.T("M40 470 H440", DGREY, 8)
    s.F("polygon", points="480,470 446,448 446,492", fill=DGREY)


@reg("hominin-skull")
def _(s):
    s.F("path", d="M110 230 C100 120 190 60 290 80 C390 100 420 190 400 270 C390 330 340 350 330 380 H250 V340 C190 340 130 310 110 230Z", fill=CREAM)
    s.F("ellipse", cx=210, cy=220, rx=40, ry=34, fill=DGREY)
    s.F("path", d="M250 330 H330 V410 H250Z", fill=CREAM)
    for x in (262, 284, 306):
        s.M(f"M{x} 345 V395", DGREY, 8)
    s.F("path", outline=False, d="M130 140 C150 100 210 80 260 84", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round")
    s.F("path", d="M110 230 C110 260 150 290 210 290", fill="none", stroke=DGREY, stroke_width="8")


@reg("footprints-of-early-humans")
def _(s):
    s.F("rect", x=30, y=90, width=452, height=340, rx=40, fill=SAND)
    for x, y, f in ((170, 150, 1), (310, 260, -1), (190, 360, 1)):
        s.F("ellipse", outline=False, cx=x, cy=y, rx=34, ry=60, fill=DSAND)
        s.F("ellipse", outline=False, cx=x, cy=y + 70, rx=26, ry=22, fill=DSAND)
        for i in range(5):
            s.F("circle", outline=False, cx=x - 28 * f + i * 14 * f, cy=y - 74 - (abs(i - 1) * 4), r=9 - i, fill=DSAND)


@reg("hunter-gatherers")
def _(s):
    ground(s, GREEN, 400)
    person(s, 150, 450, 0.8, shirt=TAN, pants=BROWN, skin=SKIN_D)
    s.T("M210 270 L260 150", DBROWN, 10)
    person(s, 330, 450, 0.8, shirt=BROWN, pants=DBROWN, skin=SKIN_D)
    s.F("path", d="M400 400 C380 340 440 340 440 400Z", fill=RED)
    for x, y in ((395, 400), (425, 405)):
        s.F("circle", cx=x, cy=y, r=16, fill=RED)


@reg("hunting-with-spears")
def _(s):
    ground(s, SAND, 410)
    person(s, 140, 460, 0.85, shirt=BROWN, pants=DBROWN, skin=SKIN_D, arms="up")
    s.T("M70 40 L230 220", DBROWN, 10)
    s.F("polygon", points="230,220 250,196 258,232", fill=STONE)
    s.F("ellipse", cx=380, cy=360, rx=90, ry=50, fill=BROWN)
    s.F("circle", cx=460, cy=330, r=30, fill=BROWN)
    s.T("M330 400 V450 M420 400 V450", DBROWN, 16)
    s.F("polygon", points="470,320 505,300 478,342", fill=CREAM)


@reg("gathering-berries")
def _(s):
    ground(s, GREEN, 400)
    s.F("circle", cx=140, cy=290, r=110, fill=DGREEN)
    for x, y in ((100, 250), (160, 220), (190, 300), (120, 330), (70, 300)):
        s.F("circle", cx=x, cy=y, r=16, fill=RED)
    s.F("path", d="M330 400 C310 330 420 330 400 400Z", fill=TAN)
    s.T("M330 360 C340 320 390 320 400 360", DBROWN, 8)
    for x, y in ((345, 345), (375, 340), (360, 330)):
        s.F("circle", cx=x, cy=y, r=14, fill=PURPLE)


@reg("discovery-of-fire")
def _(s):
    s.F("ellipse", cx=256, cy=420, rx=160, ry=36, fill=DBROWN)
    for a in (-30, 20, 160, 210):
        s.T(f"M{256 + 120 * math.cos(math.radians(a)):.0f} {430 + 20 * math.sin(math.radians(a)):.0f} L256 400", BROWN, 22)
    flame(s, 256, 290, 1.8)
    s.F("ellipse", cx=120, cy=440, rx=44, ry=26, fill=STONE)
    s.F("ellipse", cx=400, cy=440, rx=36, ry=22, fill=STONE)


@reg("cave-shelter")
def _(s):
    s.F("path", d="M0 460 V220 C0 100 120 40 256 40 C392 40 512 100 512 220 V460Z", fill=DSTONE)
    s.F("path", d="M110 460 V290 C110 200 180 160 256 160 C332 160 402 200 402 290 V460Z", fill=DBROWN)
    flame(s, 256, 400, 0.8)
    s.F("ellipse", cx=256, cy=450, rx=70, ry=16, fill=BROWN)
    person(s, 160, 460, 0.5, shirt=TAN, pants=BROWN, skin=SKIN_D)


@reg("cave-painting")
def _(s):
    s.F("path", d="M30 90 H482 V430 H30Z", fill=DSTONE)
    s.F("path", outline=False, d="M30 90 H482 V160 C400 180 300 140 200 170 C140 190 80 160 30 170Z", fill=STONE)
    s.F("ellipse", cx=250, cy=290, rx=100, ry=56, fill=DBROWN)
    s.F("path", d="M330 270 C360 240 390 260 380 300 L350 310Z", fill=DBROWN)
    s.T("M180 330 V400 M230 335 V400 M290 335 V400 M330 320 V390", DBROWN, 14)
    s.T("M190 240 L170 200 M300 240 L320 205", DBROWN, 10)
    s.F("path", d="M110 380 L120 330 L130 380Z", fill=RED)


@reg("hand-stencil-cave-art")
def _(s):
    s.F("rect", x=30, y=60, width=452, height=390, rx=30, fill=DSTONE)
    s.F("path", d="M190 420 C170 360 180 320 170 290 C150 260 110 240 120 220 C130 200 160 230 170 240 C160 190 160 150 180 150 C196 150 196 200 200 230 C200 170 210 130 230 130 C246 130 244 190 246 230 C250 180 266 150 284 156 C300 164 290 210 286 240 C310 210 330 190 346 204 C356 218 330 250 316 280 C330 330 300 380 290 420Z", fill=RED)
    for x, y in ((90, 120), (110, 150), (400, 110), (420, 140), (380, 400), (140, 400)):
        s.F("circle", outline=False, cx=x, cy=y, r=8, fill=RED)


@reg("stone-tools")
def _(s):
    s.F("path", d="M90 330 C60 250 130 120 190 100 C250 140 290 260 250 360 C200 420 130 400 90 330Z", fill=STONE)
    s.M("M190 120 L170 220 L200 300 L170 360", DSTONE, 6)
    s.F("polygon", points="300,420 340,240 380,420", fill=DSTONE)
    s.F("polygon", outline=False, points="326,400 340,290 354,400", fill=WHITE, fill_opacity="0.3")
    s.F("path", d="M360 150 C400 100 470 130 460 200 C450 260 380 270 340 230Z", fill=STONE)
    s.F("ellipse", cx=150, cy=450, rx=60, ry=18, fill=DSTONE)


@reg("hand-axe")
def _(s):
    s.open(transform="rotate(-30 256 256)")
    s.F("path", d="M256 60 C330 130 380 220 340 330 C320 390 290 420 256 420 C222 420 192 390 172 330 C132 220 182 130 256 60Z", fill=STONE)
    s.F("path", outline=False, d="M256 100 C300 160 330 230 310 310 C300 350 280 380 256 380", fill="none", stroke=WHITE, stroke_width="12", stroke_opacity="0.4")
    s.M("M256 140 L230 220 L256 280 L232 340", DSTONE, 6)
    s.close()


@reg("flint-knife")
def _(s):
    s.T("M90 420 L170 340", DBROWN, 40)
    s.F("path", d="M170 340 L420 80 C440 120 420 220 340 320 C300 360 230 380 170 340Z", fill=DSTONE)
    s.F("path", outline=False, d="M200 330 L400 100 C410 150 380 220 330 290", fill="none", stroke=WHITE, stroke_width="14", stroke_opacity="0.4")
    s.T("M130 380 L180 330 M110 400 L160 350", TAN, 8)


@reg("stone-spear")
def _(s):
    s.T("M70 450 L360 130", BROWN, 22)
    s.F("polygon", points="360,130 450,40 440,160 340,200", fill=STONE)
    s.F("polygon", outline=False, points="380,130 440,70 430,140", fill=WHITE, fill_opacity="0.4")
    s.T("M320 230 L370 190 M300 250 L350 205", TAN, 8)


@reg("bow-and-arrow-early")
def _(s):
    s.raw(f'<path d="M150 60 C60 160 60 360 150 460" fill="none" stroke="{INK}" stroke-width="38" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M150 60 C60 160 60 360 150 460" fill="none" stroke="{BROWN}" stroke-width="18" stroke-linecap="round"/>')
    s.M("M150 60 L110 260 L150 460", TAN, 5)
    s.T("M110 260 H440", DBROWN, 10)
    s.F("polygon", points="440,260 410,236 410,284", fill=STONE)
    s.F("path", d="M110 260 L90 236 L96 260 L90 284Z", fill=RED)


@reg("bone-needle")
def _(s):
    s.open(transform="rotate(-40 256 256)")
    s.F("path", d="M60 244 H440 L470 256 L440 268 H60 C40 268 40 244 60 244Z", fill=CREAM)
    s.F("ellipse", cx=96, cy=256, rx=12, ry=7, fill=DBROWN)
    s.close()
    s.T("M120 400 C180 330 140 280 230 270 C330 260 320 360 400 330", TAN, 8)
    s.F("path", d="M320 380 L440 380 L420 450 H340Z", fill=BROWN)


@reg("animal-skin-clothing")
def _(s):
    s.F("path", d="M150 70 H362 L420 190 L380 230 V440 H132 V230 L92 190Z", fill=BROWN)
    s.F("path", outline=False, d="M150 70 L256 150 L362 70 L330 66 L256 110 L182 66Z", fill=TAN)
    for x, y in ((190, 260), (320, 300), (230, 380), (350, 400)):
        s.F("ellipse", outline=False, cx=x, cy=y, rx=22, ry=14, fill=DBROWN)
    for x in range(140, 380, 28):
        s.M(f"M{x} 440 v24", BROWN, 8)


@reg("mammoth-hunt")
def _(s):
    ground(s, "#EAF2F7", 410)
    s.F("path", d="M110 300 C110 190 230 150 330 180 C420 200 450 280 430 340 L420 420 H360 V360 H250 V420 H190 V360 C150 360 110 350 110 300Z", fill=DBROWN)
    s.F("path", d="M110 280 C70 260 40 300 40 350 C40 380 60 400 90 380", fill="none", stroke=CREAM, stroke_width="22", stroke_linecap="round")
    s.F("circle", cx=118, cy=260, r=40, fill=DBROWN)
    s.T("M96 290 C60 330 70 380 110 390", DBROWN, 28)
    dot(s, 108, 250, 6, WHITE)
    s.T("M60 130 L170 240", BROWN, 8)
    s.F("polygon", points="170,240 150,248 164,224", fill=STONE)
    person(s, 380, 460, 0.45, shirt=TAN, pants=BROWN, skin=SKIN_D)


@reg("first-farming")
def _(s):
    ground(s, "#CDB07A", 330)
    for x in (80, 160, 240, 320, 400):
        s.M(f"M{x} 460 V350", DGREEN, 8)
        s.F("path", d=f"M{x} 350 C{x - 30} 320 {x - 10} 290 {x} 270 C{x + 10} 290 {x + 30} 320 {x} 350Z", fill=GREEN)
    s.T("M60 130 L170 250", DBROWN, 14)
    s.F("path", d="M150 250 C170 230 190 250 180 270 C170 290 140 280 150 250Z", fill=STONE)
    person(s, 380, 300, 0.45, shirt=TAN, pants=BROWN, skin=SKIN_D)


@reg("clay-pot-ancient")
def _(s):
    s.F("path", d="M190 90 H322 C340 140 440 200 440 300 C440 400 360 450 256 450 C152 450 72 400 72 300 C72 200 172 140 190 90Z", fill="#C2622E")
    s.F("ellipse", cx=256, cy=92, rx=66, ry=18, fill="#8A3E1B")
    s.M("M90 240 C180 270 330 270 422 240 M82 300 C180 330 330 330 430 300", CREAM, 10)
    for i in range(7):
        s.M(f"M{110 + i * 48} 260 l16 18 l16 -18", DBROWN, 6)
    s.F("path", outline=False, d="M120 250 C130 210 180 180 220 160", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.4")


@reg("megalith")
def _(s):
    ground(s, GREEN, 420)
    s.F("polygon", points="120,430 150,150 230,120 260,430", fill=DSTONE)
    s.F("polygon", points="300,430 320,190 400,170 420,430", fill=STONE)
    s.F("polygon", points="90,160 240,100 440,140 420,200 110,220", fill=DSTONE)
    s.M("M150 200 V400 M340 230 V400", DGREY, 6)
    s.F("polygon", outline=False, points="120,160 230,120 410,150 380,170 140,190", fill=WHITE, fill_opacity="0.25")


# ================================================================ ancient-egypt
@reg("ancient-egypt")
def _(s):
    sun_disc(s, 400, 110, 50, ORANGE)
    s.F("path", d="M0 420 C100 380 220 430 330 400 C420 380 470 410 512 400 V512 H0Z", fill=SAND)
    pyramid(s, 170, 420, 300, 240, SAND, DSAND)
    pyramid(s, 360, 420, 200, 160, SAND, DSAND)
    s.F("ellipse", outline=False, cx=256, cy=450, rx=200, ry=20, fill=DSAND, fill_opacity="0.5")


@reg("pyramid-egyptian")
def _(s):
    pyramid(s, 256, 430, 440, 340, SAND, DSAND)
    for y in (180, 250, 320, 390):
        s.M(f"M{256 - (y - 90) * 0.62:.0f} {y} H{256 + (y - 90) * 0.62:.0f}", DSAND, 6)
    s.F("rect", outline=False, x=236, y=400, width=40, height=30, rx=6, fill=BROWN)
    sun_disc(s, 70, 80, 34, YEL)


@reg("mummy")
def _(s):
    s.F("path", d="M256 40 C200 40 170 90 175 150 C130 160 120 230 140 300 L150 440 H362 L372 300 C392 230 382 160 337 150 C342 90 312 40 256 40Z", fill=CREAM)
    for y in range(110, 440, 34):
        s.M(f"M{150 + abs(y - 280) * 0.05:.0f} {y} L{362 - abs(y - 280) * 0.05:.0f} {y + 12}", TAN, 10)
    s.F("rect", outline=False, x=190, y=120, width=132, height=40, rx=10, fill=BROWN)
    dot(s, 226, 140, 11, WHITE)
    dot(s, 286, 140, 11, WHITE)
    dot(s, 226, 140, 5, BLACK)
    dot(s, 286, 140, 5, BLACK)


@reg("sarcophagus")
def _(s):
    s.F("path", d="M256 30 C190 30 160 80 170 150 C140 180 130 260 140 350 L150 480 H362 L372 350 C382 260 372 180 342 150 C352 80 322 30 256 30Z", fill=GOLD)
    s.F("path", d="M190 160 H322 L336 240 H176Z", fill=BLUE)
    s.F("circle", cx=256, cy=120, r=52, fill=SKIN)
    s.M("M216 112 H236 M276 112 H296", BLACK, 7)
    s.F("path", d="M170 150 L120 200 L190 190Z M342 150 L392 200 L322 190Z", fill=BLUE)
    for y in (280, 330, 380, 430):
        s.M(f"M170 {y} H342", DGOLD, 8)
    s.M("M256 250 V470", DGOLD, 8)


@reg("pharaohs-mask")
def _(s):
    s.F("path", d="M256 30 C150 30 110 130 130 230 L150 330 L110 450 H402 L362 330 L382 230 C402 130 362 30 256 30Z", fill=GOLD)
    for x in (140, 372):
        for i in range(5):
            s.F("rect", outline=False, x=x - 18, y=230 + i * 42, width=36, height=26, rx=8, fill=BLUE if i % 2 else DGOLD)
    s.F("path", d="M188 130 C188 80 324 80 324 130 V300 C324 340 290 360 256 360 C222 360 188 340 188 300Z", fill=GOLD)
    s.M("M206 190 H246 M266 190 H306", BLACK, 12)
    s.M("M206 190 H180 M306 190 H332", BLUE, 10)
    s.M("M256 200 V250", DGOLD, 8)
    s.F("path", d="M230 300 C250 316 262 316 282 300", fill="none", stroke=DGOLD, stroke_width="9", stroke_linecap="round")
    s.F("path", d="M210 70 H302 L290 110 H222Z", fill=BLUE)
    s.F("circle", cx=256, cy=90, r=18, fill=RED)


@reg("hieroglyphs")
def _(s):
    s.F("rect", x=60, y=50, width=392, height=412, rx=16, fill=SAND)
    s.M("M60 150 H452 M60 250 H452 M60 350 H452", DSAND, 6)
    s.M("M110 100 l0 30 m-18 -30 h36 M190 105 c20 -20 40 0 20 20 c-20 20 -40 0 -20 -20 M290 100 l0 30 M270 115 h40 M370 100 c-20 0 -20 30 0 30", DBROWN, 8)
    s.F("circle", outline=False, cx=140, cy=200, r=14, fill=BLUE)
    s.M("M200 190 h60 M200 215 h40 M300 190 l30 20 l30 -20", DBROWN, 8)
    s.M("M100 300 q30 -30 60 0 M190 285 v30 M240 290 q20 -10 20 10 M330 285 h50 M355 285 v40", DBROWN, 8)
    s.M("M120 390 h50 M120 415 h30 M230 380 v40 M260 380 q30 20 0 40 M340 390 c30 -20 30 30 0 20", DBROWN, 8)


@reg("papyrus-scroll")
def _(s):
    scroll(s, 90, 110, 330, 300, CREAM, BROWN)
    s.M("M130 170 h250 M130 220 h210 M130 270 h250 M130 320 h180", DBROWN, 9)
    s.F("circle", outline=False, cx=360, cy=330, r=22, fill=BLUE)
    s.M("M160 360 h60", RED, 8)


@reg("scarab-amulet")
def _(s):
    s.F("ellipse", cx=256, cy=290, rx=130, ry=150, fill=BLUE)
    s.F("circle", cx=256, cy=140, r=62, fill=BLUE)
    s.M("M256 150 V430", "#1E3A8A", 8)
    s.M("M126 280 C170 270 220 270 256 290 C292 270 342 270 386 280", "#1E3A8A", 8)
    s.T("M130 250 L60 220 M130 320 L50 340 M380 250 L452 220 M380 320 L462 340", GOLD, 14)
    s.F("circle", cx=256, cy=60, r=28, fill=GOLD)
    s.F("ellipse", outline=False, cx=200, cy=210, rx=24, ry=60, fill=WHITE, fill_opacity="0.3")


@reg("ankh")
def _(s):
    s.raw(f'<ellipse cx="256" cy="150" rx="86" ry="106" fill="none" stroke="{INK}" stroke-width="60" data-outline="under"/>')
    s.raw(f'<ellipse cx="256" cy="150" rx="86" ry="106" fill="none" stroke="{GOLD}" stroke-width="40"/>')
    s.T("M256 256 V460 M150 310 H362", GOLD, 40)
    s.M("M240 280 V430", WHITE, 8)


@reg("eye-of-horus")
def _(s):
    s.F("path", d="M50 220 C130 130 330 130 410 220 C330 300 130 300 50 220Z", fill=WHITE)
    s.F("circle", cx=230, cy=220, r=54, fill=BLUE)
    s.F("circle", cx=230, cy=220, r=26, fill=BLACK)
    s.T("M60 190 C120 150 300 140 400 190", BLACK, 16)
    s.T("M230 280 L230 330 C230 370 270 380 290 370", BLUE, 14)
    s.T("M270 290 C330 310 400 340 440 300", BLUE, 14)
    s.F("circle", cx=440, cy=300, r=18, fill=BLUE)
    s.M("M60 190 V150", BLACK, 10)


@reg("obelisk")
def _(s):
    s.F("polygon", points="256,40 300,110 320,420 192,420 212,110", fill=SAND)
    s.F("polygon", outline=False, points="256,40 300,110 320,420 262,420 262,100", fill=DSAND)
    s.F("polygon", points="256,40 300,110 212,110", fill=GOLD)
    s.F("rect", x=150, y=420, width=212, height=40, rx=8, fill=STONE)
    s.F("rect", x=120, y=456, width=272, height=30, rx=8, fill=DSTONE)
    for y in (150, 210, 270, 330):
        s.M(f"M238 {y} h12 M262 {y} h12 M240 {y + 20} h34", DBROWN, 6)


@reg("canopic-jars")
def _(s):
    for x, head_, c in ((100, "human", SKIN), (190, "baboon", "#8C6A4A"), (322, "jackal", "#3B3B44"), (412, "falcon", GOLD)):
        pass
    for x, c in ((60, SKIN), (160, "#8C6A4A"), (260, "#3B3B44"), (360, GOLD)):
        s.F("path", d=f"M{x} 190 H{x + 92} L{x + 100} 420 C{x + 100} 450 {x + 80} 460 {x + 46} 460 C{x + 12} 460 {x - 8} 450 {x - 8} 420Z", fill=SAND)
        s.F("path", d=f"M{x + 2} 190 C{x + 2} 130 {x + 90} 130 {x + 90} 190Z", fill=c)
        s.F("rect", outline=False, x=x + 12, y=290, width=68, height=60, rx=8, fill=BLUE)
        dot(s, x + 28, 176, 6, WHITE)
        dot(s, x + 66, 176, 6, WHITE)
        s.F("polygon", points=f"{x + 24},120 {x + 40},150 {x + 8},150", fill=c)


@reg("rosetta-stone")
def _(s):
    s.F("path", d="M110 450 L90 160 C90 80 160 50 230 60 L360 90 C420 100 440 150 430 220 L412 450Z", fill=DSTONE)
    s.F("path", outline=False, d="M110 440 L102 180 C104 110 160 80 220 86 L350 110", fill="none", stroke=STONE, stroke_width="18", stroke_linecap="round")
    s.M("M150 150 h240 M150 190 h240 M150 230 h240", DGREY, 7)
    s.M("M140 290 h260 M140 320 h260 M140 350 h260 M140 380 h200", DGREY, 7)
    s.M("M170 150 l10 20 M210 190 l12 -18 M250 230 l16 14", BLACK, 5)


# ================================================================ mesopotamia
@reg("mesopotamia")
def _(s):
    ground(s, SAND, 430)
    s.F("rect", x=40, y=360, width=432, height=70, fill="#6EC4E8")
    s.F("rect", outline=False, x=40, y=360, width=432, height=14, fill=WHITE, fill_opacity="0.5")
    for k, (w, y) in enumerate(((260, 340), (190, 260), (120, 180))):
        s.F("rect", x=256 - w / 2, y=y, width=w, height=80, fill=SAND)
        s.M(f"M{256 - w / 2} {y + 40} H{256 + w / 2}", DSAND, 6)
    s.F("rect", x=226, y=120, width=60, height=60, fill=BLUE)
    s.F("rect", x=240, y=70, width=32, height=50, fill=GOLD)


@reg("ziggurat")
def _(s):
    for i, (w, y) in enumerate(((400, 360), (310, 290), (220, 220), (130, 150))):
        s.F("rect", x=256 - w / 2, y=y, width=w, height=70, fill=SAND if i % 2 == 0 else DSAND)
    s.F("rect", x=216, y=100, width=80, height=50, fill=BLUE)
    s.F("polygon", points="256,70 290,100 222,100", fill=GOLD)
    s.F("path", d="M240 430 L256 360 L272 430Z", fill=BROWN)
    s.M("M256 360 V430", DBROWN, 6)
    for k in range(5):
        s.M(f"M{200 + k * 28} 430 L{232 + k * 12} 360", DSAND, 6)


@reg("cuneiform-tablet")
def _(s):
    s.F("path", d="M130 90 H382 C400 90 410 100 410 120 V400 C410 430 390 440 360 440 H150 C120 440 102 430 102 400 V120 C102 100 112 90 130 90Z", fill=TAN)
    for r in range(6):
        for c in range(6):
            x, y = 140 + c * 42, 140 + r * 48
            s.M(f"M{x} {y} l18 -10 M{x} {y} l18 10 M{x + 6} {y} h26" if (r * 3 + c) % 3 == 0 else f"M{x} {y - 12} v24 M{x + 12} {y - 12} l14 12 l-14 12" if (r + c) % 2 else f"M{x} {y} h30 M{x + 14} {y - 14} v28", DBROWN, 7)


@reg("clay-tablet")
def _(s):
    s.open(transform="rotate(-8 256 256)")
    s.F("rect", x=110, y=100, width=292, height=320, rx=34, fill=TAN)
    lines(s, 150, 160, 210, 6, 44, DBROWN, 9)
    s.close()
    s.T("M400 440 L460 340", BROWN, 14)
    s.F("polygon", points="460,340 476,314 446,324", fill=DBROWN)


@reg("code-of-hammurabi-stele")
def _(s):
    s.F("path", d="M150 450 V150 C150 60 362 60 362 150 V450Z", fill="#2E2A3B")
    s.F("path", d="M150 450 V150 C150 60 362 60 362 150 V450Z", fill=BLACK)
    s.F("path", outline=False, d="M170 440 V150 C170 90 200 76 240 72", fill="none", stroke=DGREY, stroke_width="12", stroke_linecap="round")
    s.F("rect", outline=False, x=180, y=100, width=152, height=100, rx=10, fill=DGREY)
    s.F("rect", outline=False, x=200, y=120, width=36, height=50, rx=10, fill=SKIN)
    s.F("rect", outline=False, x=270, y=120, width=36, height=50, rx=10, fill=SKIN)
    for y in range(230, 430, 24):
        s.M(f"M180 {y} h152", DGREY, 6)


@reg("hanging-gardens-of-babylon")
def _(s):
    for i, (w, y) in enumerate(((400, 340), (320, 260), (240, 180), (160, 100))):
        s.F("rect", x=256 - w / 2, y=y, width=w, height=80, fill=SAND)
        for x in range(int(256 - w / 2) + 20, int(256 + w / 2) - 10, 60):
            s.F("circle", cx=x, cy=y - 6, r=24, fill=GREEN)
            s.F("circle", cx=x + 20, cy=y + 6, r=16, fill=DGREEN)
        s.T(f"M{256 - w / 2 + 40} {y + 30} V{y + 80}", GREEN, 10)
    s.F("rect", x=60, y=420, width=392, height=40, rx=10, fill="#6EC4E8")


@reg("lamassu")
def _(s):
    s.F("path", d="M120 450 V240 C120 100 330 100 330 240 V450Z", fill=SAND)
    s.F("path", d="M300 240 C340 130 440 130 440 240 V450 H330Z", fill=DSAND)
    s.F("path", d="M150 200 C130 110 200 60 270 80 C330 100 340 180 300 230Z", fill=SKIN)
    s.F("path", d="M140 160 C150 70 330 60 330 150 C300 130 200 120 140 160Z", fill=GOLD)
    dot(s, 230, 170, 10, BLACK)
    s.F("path", d="M170 250 C190 330 250 330 270 250 L260 300 C230 330 200 330 180 300Z", fill=BROWN)
    s.F("path", d="M360 200 C420 170 470 200 480 260 C440 250 400 260 360 280Z", fill=SAND)
    s.T("M140 450 V480 M300 450 V480", DSAND, 22)


# ================================================================ indus-ancient-india
@reg("indus-valley-civilization")
def _(s):
    ground(s, SAND, 420)
    for x, y, w, h in ((60, 300, 130, 130), (200, 260, 130, 170), (340, 310, 120, 120)):
        s.F("rect", x=x, y=y, width=w, height=h, fill="#C2622E")
        s.F("rect", outline=False, x=x + 20, y=y + 30, width=w - 40, height=18, fill=BROWN)
        for k in range(1, 4):
            s.M(f"M{x} {y + k * 36} H{x + w}", "#8A3E1B", 4)
    s.F("rect", x=40, y=428, width=432, height=34, rx=10, fill="#6EC4E8")
    sun_disc(s, 400, 100, 40, YEL)


@reg("mohenjo-daro")
def _(s):
    s.F("rect", x=40, y=380, width=432, height=70, rx=10, fill="#C2622E")
    for x in range(40, 440, 50):
        s.M(f"M{x} 380 V450", "#8A3E1B", 4)
    s.F("rect", x=100, y=260, width=140, height=120, fill="#C2622E")
    s.F("rect", x=280, y=200, width=140, height=180, fill="#C2622E")
    s.F("rect", outline=False, x=124, y=290, width=30, height=50, fill=BROWN)
    s.F("rect", outline=False, x=320, y=240, width=30, height=40, fill=BROWN)
    s.M("M40 380 H472", DBROWN, 8)
    sun_disc(s, 400, 90, 36, YEL)


@reg("harappa")
def _(s):
    s.F("rect", x=60, y=300, width=392, height=140, fill="#C2622E")
    for r in range(4):
        for c in range(8):
            s.M(f"M{60 + c * 49 + (r % 2) * 24} {300 + r * 35} v35", "#8A3E1B", 4)
        s.M(f"M60 {300 + r * 35} H452", "#8A3E1B", 4)
    s.F("rect", x=150, y=200, width=60, height=100, fill="#C2622E")
    s.F("rect", x=300, y=220, width=60, height=80, fill="#C2622E")
    s.F("path", d="M150 200 H210 L200 180 H160Z", fill="#8A3E1B")
    s.F("ellipse", cx=256, cy=450, rx=170, ry=14, fill=DSAND)


@reg("great-bath")
def _(s):
    s.F("rect", x=40, y=160, width=432, height=290, fill="#C2622E")
    s.F("rect", x=90, y=210, width=332, height=190, fill="#6EC4E8")
    s.F("rect", outline=False, x=90, y=210, width=332, height=40, fill=WHITE, fill_opacity="0.4")
    for i in range(5):
        s.M(f"M{110 + i * 62} 250 V400", "#8A3E1B", 5)
    s.F("rect", x=200, y=400, width=110, height=50, fill=DBROWN)
    s.M("M90 330 H422", "#4C9DC2", 6)


@reg("indus-seal")
def _(s):
    s.F("rect", x=80, y=80, width=352, height=352, rx=36, fill=TAN)
    s.F("path", d="M130 300 C130 230 170 220 200 230 L240 210 C300 190 380 200 390 260 V330 H350 V380 H320 V330 H210 V380 H180 V330 H130Z", fill=DBROWN)
    s.T("M200 230 L170 170 M240 215 L270 160", DBROWN, 14)
    s.M("M120 130 l20 20 m0 -20 l-20 20 M190 130 v30 M240 135 c20 -10 30 10 10 20 M310 125 h50 M335 125 v30 M390 130 c-15 0 -15 25 0 25", BROWN, 8)


@reg("dancing-girl-bronze")
def _(s):
    s.F("rect", x=170, y=400, width=172, height=36, rx=10, fill=DGOLD)
    s.F("path", d="M240 400 C230 330 240 280 256 250 C280 230 300 280 290 340 L282 400Z", fill="#A0662C")
    s.F("path", d="M256 250 C220 240 190 280 160 330 C170 340 190 310 230 290Z", fill="#A0662C")
    s.F("path", d="M290 250 C310 270 340 290 360 360 L336 366 C320 320 300 300 280 290Z", fill="#A0662C")
    s.F("circle", cx=268, cy=190, r=40, fill="#A0662C")
    s.F("path", d="M250 160 C260 130 310 140 300 170Z", fill="#6E3E22")
    s.T("M300 330 C320 360 310 400 296 420", "#A0662C", 24)
    for y in (260, 280, 300):
        s.M(f"M164 {y} h30", GOLD, 6)


@reg("ancient-indian-coins")
def _(s):
    for x, y, r in ((170, 220, 100), (340, 290, 90), (220, 380, 70)):
        s.F("circle", cx=x, cy=y, r=r, fill=GOLD)
        s.F("polygon", points=f"{x},{y - r * 0.6} {x + r * 0.55},{y + r * 0.45} {x - r * 0.55},{y + r * 0.45}", fill=DGOLD)
        s.F("circle", outline=False, cx=x, cy=y + 4, r=r * 0.14, fill=GOLD)
        s.F("circle", outline=False, cx=x - r * 0.5, cy=y - r * 0.5, r=r * 0.12, fill=WHITE, fill_opacity="0.6")


@reg("ashoka-pillar")
def _(s):
    s.F("path", d="M190 450 L210 150 H302 L322 450Z", fill=STONE)
    s.F("path", outline=False, d="M210 150 H260 L246 450 H190Z", fill=WHITE, fill_opacity="0.25")
    s.F("path", d="M160 150 C160 110 352 110 352 150Z", fill=DSTONE)
    s.F("rect", x=170, y=120, width=172, height=30, rx=10, fill=STONE)
    s.F("path", d="M200 120 C190 60 240 40 256 60 C272 40 322 60 312 120Z", fill=SAND)
    s.F("rect", x=150, y=450, width=212, height=30, rx=8, fill=DSTONE)


@reg("lion-capital")
def _(s):
    s.F("ellipse", cx=256, cy=420, rx=190, ry=40, fill=STONE)
    s.F("rect", x=70, y=370, width=372, height=50, fill=STONE)
    s.M("M120 395 h40 M236 395 h40 M352 395 h40", DSTONE, 8)
    for x, f in ((130, 1), (382, -1)):
        s.F("path", d=f"M{x} 370 C{x - 40 * f} 300 {x - 20 * f} 220 {x + 10 * f} 200 C{x + 50 * f} 190 {x + 80 * f} 230 {x + 70 * f} 290 L{x + 50 * f} 370Z", fill=SAND)
        s.F("circle", cx=x + 20 * f, cy=195, r=40, fill=SAND)
        dot(s, x + 8 * f, 190, 6, BLACK)
    s.F("path", d="M180 370 C180 280 190 220 256 200 C322 220 332 280 332 370Z", fill=SAND)
    s.F("circle", cx=256, cy=190, r=46, fill=SAND)
    dot(s, 240, 184, 7, BLACK)
    dot(s, 272, 184, 7, BLACK)
    s.F("path", d="M215 140 C220 100 290 100 297 140 C270 130 240 130 215 140Z", fill=DSAND)


@reg("nalanda-university-ruins")
def _(s):
    ground(s, GREEN, 430)
    s.F("rect", x=50, y=300, width=412, height=130, fill="#C2622E")
    for x in range(50, 462, 80):
        s.F("rect", outline=False, x=x + 16, y=330, width=48, height=100, rx=24, fill=BROWN)
    s.F("rect", x=90, y=220, width=100, height=80, fill="#C2622E")
    s.F("rect", x=300, y=250, width=120, height=50, fill="#C2622E")
    s.F("polygon", points="190,220 250,160 250,300 190,300", fill="#A0522D")
    s.M("M50 300 H462", DBROWN, 8)


@reg("vedic-scrolls")
def _(s):
    s.F("rect", x=40, y=140, width=432, height=70, rx=18, fill=TAN)
    s.F("rect", x=40, y=230, width=432, height=70, rx=18, fill=CREAM)
    s.F("rect", x=40, y=320, width=432, height=70, rx=18, fill=TAN)
    for y in (175, 265, 355):
        s.M(f"M90 {y} h120 M230 {y} h60 M310 {y} h110", DBROWN, 7)
    s.T("M110 140 V390 M410 140 V390", BROWN, 6)
    s.T("M256 140 V100 M236 100 H276", RED, 10)


# ================================================================ ancient-china
@reg("ancient-china")
def _(s):
    s.F("path", d="M0 420 C100 400 120 330 200 330 C280 330 300 400 400 380 C450 370 480 380 512 370 V512 H0Z", fill=GREEN)
    s.F("rect", x=130, y=240, width=250, height=90, fill=RED)
    s.F("path", d="M60 250 C130 230 170 200 256 130 C342 200 382 230 452 250 C400 250 360 270 256 270 C152 270 112 250 60 250Z", fill=DBROWN)
    s.F("path", d="M110 330 L130 300 H382 L402 330Z", fill=DBROWN)
    for x in (170, 256, 342):
        s.F("rect", outline=False, x=x - 24, y=270, width=48, height=60, rx=6, fill=DRED)
    sun_disc(s, 410, 90, 34, YEL)


@reg("chinese-dynasty-scroll")
def _(s):
    scroll(s, 90, 100, 332, 300, CREAM, DRED)
    s.M("M150 150 v80 M190 150 v60 M230 150 v90 M270 150 v70 M310 150 v50 M350 150 v80", BLACK, 10)
    s.F("circle", cx=256, cy=320, r=44, fill=RED)
    s.M("M236 320 h40 M256 300 v40", CREAM, 8)


@reg("silk-road")
def _(s):
    s.F("path", d="M0 330 C100 280 160 360 260 320 C360 280 420 330 512 290 V512 H0Z", fill=SAND)
    s.F("path", d="M0 330 C100 280 160 360 260 320 C360 280 420 330 512 290", fill="none", stroke=DSAND, stroke_width="10")
    s.T("M30 470 C140 420 220 470 300 400 C370 340 420 420 490 370", BROWN, 24)
    s.M("M30 470 C140 420 220 470 300 400 C370 340 420 420 490 370", SAND, 8, dash="16 20")
    s.F("rect", x=130, y=100, width=60, height=160, rx=10, fill=RED)
    s.F("rect", outline=False, x=140, y=110, width=40, height=100, fill=GOLD)
    s.F("path", d="M300 130 L340 60 L380 130Z", fill=BLUE)
    s.F("rect", x=310, y=130, width=60, height=90, fill=BLUE)
    sun_disc(s, 430, 80, 34, YEL)


@reg("silk-road-caravan")
def _(s):
    s.F("rect", x=0, y=410, width=512, height=102, fill=SAND)
    for x, k in ((120, 0.8), (320, 0.8)):
        s.open(transform=f"translate({x} 330) scale({k})")
        s.F("path", d="M-110 20 C-120 -60 -50 -90 -20 -110 C-10 -150 40 -160 50 -120 L70 -50 C110 -40 120 -10 110 20 L90 40 H60 V120 H30 V50 H-70 V120 H-100 V50 H-110Z", fill=TAN)
        s.F("circle", outline=False, cx=-5, cy=-80, r=20, fill=BROWN)
        s.F("rect", x=-70, y=-90, width=110, height=70, rx=10, fill=RED)
        s.F("rect", outline=False, x=-60, y=-80, width=90, height=14, fill=GOLD)
        s.close()
    sun_disc(s, 430, 80, 36, ORANGE)


@reg("ancient-chinese-coins")
def _(s):
    for x, y, rot in ((170, 200, 20), (340, 280, -15), (210, 370, 0)):
        s.open(transform=f"rotate({rot} {x} {y})")
        s.raw(f'<path d="M{x} {y - 90} A90 90 0 1 1 {x - 0.1} {y - 90}Z M{x - 26} {y - 26} H{x + 26} V{y + 26} H{x - 26}Z" fill="{GOLD}" fill-rule="evenodd" stroke="{INK}" stroke-width="10" stroke-linejoin="round" data-outline="stroke"/>')
        s.M(f"M{x} {y - 62} v14 M{x} {y + 48} v14 M{x - 62} {y} h14 M{x + 48} {y} h14", DGOLD, 8)
        s.close()


@reg("oracle-bones")
def _(s):
    s.F("path", d="M120 120 C60 200 80 380 180 440 C250 480 380 400 400 280 C420 180 360 70 250 70 C190 70 150 90 120 120Z", fill=CREAM)
    s.M("M170 170 l30 40 l-30 40 M240 150 v140 M240 210 h60 M330 170 v100 M330 220 l40 -30 M200 330 h130 M270 330 v60", DBROWN, 9)
    s.F("circle", outline=False, cx=150, cy=300, r=10, fill=DBROWN)
    s.F("circle", outline=False, cx=370, cy=330, r=10, fill=DBROWN)
    s.M("M120 280 l-20 20 M120 300 l-24 -4", RED, 6)


@reg("jade-disc")
def _(s):
    s.raw(f'<path d="M256 56 A200 200 0 1 1 255.9 56Z M256 176 A80 80 0 1 0 256.1 176Z" fill="#5EC7A0" fill-rule="evenodd" stroke="{INK}" stroke-width="10" stroke-linejoin="round" data-outline="stroke"/>')
    s.raw(f'<circle cx="256" cy="256" r="140" fill="none" stroke="#2F9C78" stroke-width="10" stroke-dasharray="14 12"/>')
    s.F("path", outline=False, d="M110 180 C130 130 190 90 240 84", fill="none", stroke=WHITE, stroke_width="18", stroke_linecap="round", stroke_opacity="0.6")


# ================================================================ ancient-greece
@reg("ancient-greece")
def _(s):
    s.F("polygon", points="60,190 256,70 452,190", fill=STONE)
    s.F("polygon", outline=False, points="120,180 256,100 392,180", fill=WHITE, fill_opacity="0.3")
    s.F("rect", x=60, y=190, width=392, height=30, fill=DSTONE)
    for x in (110, 183, 256, 329, 402):
        s.F("rect", x=x - 24, y=220, width=48, height=190, fill=STONE)
        s.M(f"M{x - 8} 230 V400 M{x + 8} 230 V400", DSTONE, 5)
    s.F("rect", x=40, y=410, width=432, height=26, rx=6, fill=STONE)
    s.F("rect", x=20, y=436, width=472, height=26, rx=6, fill=DSTONE)


@reg("greek-temple")
def _(s):
    s.F("polygon", points="40,190 256,60 472,190", fill=SAND)
    s.F("polygon", points="120,180 256,100 392,180", fill=SKY)
    s.F("rect", x=40, y=190, width=432, height=34, fill=SAND)
    for x in range(80, 460, 60):
        s.F("rect", x=x - 20, y=224, width=40, height=190, fill=CREAM)
        s.M(f"M{x - 6} 230 V400 M{x + 6} 230 V400", DSAND, 4)
    s.F("rect", x=20, y=414, width=472, height=24, rx=6, fill=SAND)
    s.F("rect", x=0, y=438, width=512, height=24, rx=6, fill=DSAND)


@reg("greek-column")
def _(s):
    s.F("rect", x=130, y=70, width=252, height=34, rx=8, fill=STONE)
    s.F("path", d="M150 104 C150 130 190 130 190 150 H322 C322 130 362 130 362 104Z", fill=STONE)
    s.F("rect", x=190, y=150, width=132, height=270, fill=CREAM)
    for x in (214, 238, 262, 286, 310):
        s.M(f"M{x} 160 V410", STONE, 6)
    s.F("rect", x=160, y=420, width=192, height=34, rx=8, fill=STONE)
    s.F("rect", x=140, y=454, width=232, height=28, rx=8, fill=DSTONE)
    s.F("path", outline=False, d="M200 160 V410", fill="none", stroke=WHITE, stroke_width="8", stroke_opacity="0.5")


@reg("amphitheatre")
def _(s):
    s.F("path", d="M30 420 C30 150 482 150 482 420Z", fill=SAND)
    for r in (230, 190, 150, 110):
        s.raw(f'<path d="M{256 - r} 420 C{256 - r} {420 - r * 1.3} {256 + r} {420 - r * 1.3} {256 + r} 420" fill="none" stroke="{DSAND}" stroke-width="10"/>')
    s.F("path", d="M110 420 C110 330 402 330 402 420Z", fill=TAN)
    s.M("M256 345 V420 M180 355 L200 420 M330 355 L310 420", DSAND, 8)
    s.F("rect", x=20, y=420, width=472, height=34, rx=10, fill=DSAND)


@reg("greek-vase")
def _(s):
    s.F("path", d="M190 60 H322 L300 120 C380 160 400 260 360 340 C340 380 330 420 340 450 H172 C182 420 172 380 152 340 C112 260 132 160 212 120Z", fill="#C2622E")
    s.M("M146 250 C200 270 312 270 366 250", BLACK, 14)
    s.F("path", outline=False, d="M190 300 C200 290 220 290 230 300 L230 340 L190 340Z", fill=BLACK)
    s.T("M250 300 l30 -10 l30 10 v40 h-60Z", BLACK, 8)
    s.F("rect", x=190, y=450, width=132, height=22, rx=8, fill="#8A3E1B")
    s.T("M200 110 C130 110 110 200 150 230 M312 110 C382 110 402 200 362 230", "#C2622E", 18)


@reg("greek-helmet")
def _(s):
    s.F("path", d="M110 280 C110 140 190 90 256 90 C322 90 402 140 402 280 V400 C402 420 380 440 360 440 H320 V320 C320 300 300 290 256 290 C212 290 192 300 192 320 V440 H152 C132 440 110 420 110 400Z", fill=GOLD)
    s.F("path", d="M240 90 C230 30 280 10 340 20 C380 30 400 60 380 100 C340 70 290 80 256 90Z", fill=RED)
    s.M("M150 260 H210 M302 260 H362", DGOLD, 10)
    s.F("path", outline=False, d="M140 230 C140 160 190 120 240 112", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.5")


@reg("olympic-torch-ancient")
def _(s):
    s.F("path", d="M200 230 H312 L290 460 H222Z", fill=GOLD)
    s.F("path", d="M180 210 H332 L312 240 H200Z", fill=DGOLD)
    flame(s, 256, 130, 1.2)
    s.M("M236 280 L228 420 M276 280 L284 420", DGOLD, 8)
    s.M("M170 70 L130 40 M342 70 L382 40", ORANGE, 12)


@reg("greek-scroll")
def _(s):
    scroll(s, 90, 110, 332, 280, CREAM, BROWN)
    s.M("M130 160 h250 M130 205 h250 M130 250 h200", DBROWN, 9)
    s.M("M130 330 C160 300 190 300 220 330 C250 360 280 360 310 330 C330 310 350 310 380 330", BLUE, 10)


# ================================================================ ancient-rome
@reg("ancient-rome")
def _(s):
    s.F("path", d="M30 440 V180 C30 120 100 90 256 90 C412 90 482 120 482 180 V440Z", fill=SAND)
    for r, y in enumerate((130, 230, 330)):
        for c in range(7):
            x = 54 + c * 60
            s.F("path", outline=False, d=f"M{x} {y + 90} V{y + 50} C{x} {y + 20} {x + 40} {y + 20} {x + 40} {y + 50} V{y + 90}Z", fill=DBROWN)
        s.M(f"M30 {y + 96} H482", DSAND, 8)
    s.F("rect", x=20, y=440, width=472, height=30, rx=8, fill=DSAND)


@reg("roman-soldier")
def _(s):
    person(s, 220, 470, 1.0, shirt=RED, pants=SKIN, skin=SKIN, hair=None, hat="helmet")
    s.F("rect", x=240, y=30, width=32, height=60, rx=8, fill=RED)
    s.F("rect", x=320, y=230, width=100, height=170, rx=20, fill=RED)
    s.F("rect", outline=False, x=336, y=250, width=68, height=130, rx=12, fill=GOLD)
    s.T("M120 180 L90 420", DBROWN, 10)
    s.F("polygon", points="120,180 104,130 140,150", fill=IRON)


@reg("roman-helmet")
def _(s):
    s.F("path", d="M100 300 C100 150 180 100 256 100 C332 100 412 150 412 300 V400 H360 V320 C360 300 340 290 256 290 C172 290 152 300 152 320 V400 H100Z", fill=IRON)
    s.F("rect", x=224, y=60, width=64, height=44, rx=10, fill=RED)
    s.F("rect", x=190, y=30, width=132, height=36, rx=18, fill=RED)
    s.M("M100 300 H152 M360 300 H412", GOLD, 10)
    s.F("path", outline=False, d="M130 270 C130 180 180 130 240 118", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.5")


@reg("roman-shield")
def _(s):
    s.F("rect", x=140, y=50, width=232, height=410, rx=50, fill=RED)
    s.F("rect", outline=False, x=240, y=70, width=32, height=370, rx=8, fill=GOLD)
    s.F("ellipse", cx=256, cy=250, rx=60, ry=40, fill=GOLD)
    s.F("ellipse", outline=False, cx=256, cy=250, rx=34, ry=20, fill=DGOLD)
    s.M("M160 120 H352 M160 380 H352", GOLD, 12)


@reg("roman-aqueduct")
def _(s):
    s.F("rect", x=20, y=130, width=472, height=60, fill=SAND)
    s.F("rect", outline=False, x=20, y=140, width=472, height=24, fill="#6EC4E8")
    for c in range(6):
        x0 = 20 + c * 80
        s.F("path", d=f"M{x0} 190 H{x0 + 80} V330 H{x0 + 66} V260 C{x0 + 66} 230 {x0 + 14} 230 {x0 + 14} 260 V330 H{x0}Z", fill=SAND)
    for c in range(5):
        x0 = 60 + c * 80
        s.F("path", d=f"M{x0} 330 H{x0 + 80} V460 H{x0 + 66} V390 C{x0 + 66} 360 {x0 + 14} 360 {x0 + 14} 390 V460 H{x0}Z", fill=DSAND)


@reg("roman-road")
def _(s):
    s.F("polygon", points="200,60 312,60 480,470 32,470", fill=STONE)
    for i in range(7):
        y = 80 + i * 60
        k = (y - 60) / 410
        x0, x1 = 200 - 168 * k, 312 + 168 * k
        s.M(f"M{x0:.0f} {y} H{x1:.0f}", DSTONE, 6)
        n = 3 + i
        for j in range(1, n):
            xx = x0 + (x1 - x0) * j / n
            s.M(f"M{xx:.0f} {y} l{(xx - 256) * 0.15:.0f} 60", DSTONE, 5)
    s.M("M256 70 V470", WHITE, 8, dash="28 30")


@reg("roman-coins")
def _(s):
    for x, y, r in ((180, 190, 100), (330, 270, 90), (210, 380, 70)):
        s.F("circle", cx=x, cy=y, r=r, fill=GOLD)
        s.raw(f'<circle cx="{x}" cy="{y}" r="{r * 0.78:.0f}" fill="none" stroke="{DGOLD}" stroke-width="6" stroke-dasharray="6 8"/>')
        s.F("path", d=f"M{x - r * 0.3} {y + r * 0.4} C{x - r * 0.4} {y - r * 0.4} {x} {y - r * 0.5} {x + r * 0.3} {y - r * 0.2} C{x + r * 0.2} {y + r * 0.1} {x + r * 0.1} {y + r * 0.3} {x} {y + r * 0.4}Z", fill=DGOLD)
        s.F("circle", outline=False, cx=x - r * 0.5, cy=y - r * 0.5, r=r * 0.12, fill=WHITE, fill_opacity="0.6")


@reg("chariot-race")
def _(s):
    s.F("rect", x=0, y=400, width=512, height=60, fill=SAND)
    s.F("path", d="M130 320 H260 L290 230 H340 V270 H300 L270 340 H130Z", fill=GOLD)
    s.F("circle", cx=190, cy=380, r=50, fill=TAN)
    s.raw(f'<circle cx="190" cy="380" r="40" fill="none" stroke="{DBROWN}" stroke-width="10"/>')
    for a in range(0, 360, 60):
        x, y = arc_pt(190, 380, 40, a)
        s.M(f"M190 380 L{x:.0f} {y:.0f}", DBROWN, 6)
    s.F("ellipse", cx=390, cy=280, rx=70, ry=40, fill=BROWN)
    s.F("circle", cx=450, cy=240, r=28, fill=BROWN)
    s.T("M360 310 V400 M420 310 V400", DBROWN, 14)
    s.T("M340 250 L270 230", DBROWN, 6)
    s.F("circle", cx=250, cy=200, r=28, fill=SKIN)
    s.F("rect", x=226, y=224, width=48, height=70, rx=16, fill=RED)


@reg("gladiator-helmet")
def _(s):
    s.F("path", d="M110 280 C100 140 180 80 256 80 C332 80 412 140 402 280 V380 C402 420 380 440 340 440 H172 C132 440 110 420 110 380Z", fill=IRON)
    s.F("path", d="M150 250 H362 V330 H150Z", fill=DGREY)
    for x in range(168, 360, 28):
        s.M(f"M{x} 262 V320", IRON, 8)
    s.F("path", d="M230 80 C230 20 282 20 282 80Z", fill=GOLD)
    s.F("path", d="M256 20 C300 0 360 30 340 80 L282 80Z", fill=RED)
    s.F("path", outline=False, d="M140 230 C140 160 190 120 240 108", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.5")


@reg("roman-numerals-clock")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=CREAM)
    s.raw(f'<circle cx="256" cy="256" r="200" fill="none" stroke="{DGOLD}" stroke-width="16"/>')
    for i, n in enumerate(("XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI")):
        x, y = arc_pt(256, 256, 150, -90 + i * 30)
        txt(s, n, x, y, 20 + 14 * len(n), 34, DBROWN)
    s.open("part-hand-minute", "256 256")
    s.M("M256 256 V120", BLACK, 12)
    s.close()
    s.open("part-hand-hour", "256 256")
    s.M("M256 256 L320 290", BLACK, 14)
    s.close()
    s.F("circle", cx=256, cy=256, r=14, fill=RED)


@reg("laurel-crown")
def _(s):
    for f in (1, -1):
        for i in range(8):
            t = i / 7
            x = 256 + f * (150 - 90 * math.sin(t * 1.4))
            y = 410 - 330 * t
            rot = f * (-30 + 70 * t)
            s.F("ellipse", cx=x, cy=y, rx=46, ry=20, fill=GREEN if i % 2 else DGREEN, transform=f"rotate({rot + (90 if f == 1 else 90)} {x:.0f} {y:.0f})")
    s.F("circle", cx=256, cy=440, r=24, fill=RED)


# ================================================================ persia
@reg("ancient-persia")
def _(s):
    s.F("polygon", points="30,470 30,410 100,410 100,350 170,350 170,290 240,290 240,470", fill=STONE)
    for x in (300, 420):
        s.F("rect", x=x - 24, y=170, width=48, height=290, fill=SAND)
        s.M(f"M{x - 8} 180 V450 M{x + 8} 180 V450", DSAND, 4)
        s.F("path", d=f"M{x - 50} 100 C{x - 70} 160 {x - 30} 180 {x - 24} 170 H{x + 24} C{x + 30} 180 {x + 70} 160 {x + 50} 100 C{x + 30} 130 {x + 10} 130 {x} 110 C{x - 10} 130 {x - 30} 130 {x - 50} 100Z", fill=GOLD)
    s.F("rect", x=270, y=80, width=180, height=30, rx=8, fill=SAND)
    s.F("rect", x=270, y=460, width=180, height=26, rx=8, fill=DSAND)


@reg("persian-soldier")
def _(s):
    person(s, 220, 470, 1.0, shirt=BLUE, pants=DBROWN, skin=SKIN, hair=HAIR)
    s.F("path", d="M194 100 C194 60 318 60 318 100 L330 130 H182Z", fill=GOLD)
    s.T("M380 50 L360 440", DBROWN, 10)
    s.F("polygon", points="380,60 366,10 394,18", fill=IRON)
    s.F("circle", cx=340, cy=300, r=50, fill=GOLD)
    s.F("circle", outline=False, cx=340, cy=300, r=26, fill=BLUE)


@reg("persian-rug-ancient")
def _(s):
    s.F("rect", x=60, y=90, width=392, height=332, rx=16, fill=RED)
    s.F("rect", outline=False, x=84, y=114, width=344, height=284, rx=8, fill=DRED)
    s.F("rect", outline=False, x=110, y=140, width=292, height=232, rx=8, fill=CREAM)
    s.F("polygon", points="256,160 360,256 256,352 152,256", fill=BLUE)
    s.F("polygon", points="256,198 322,256 256,314 190,256", fill=GOLD)
    s.F("circle", outline=False, cx=256, cy=256, r=20, fill=RED)
    for x in range(70, 460, 28):
        s.M(f"M{x} 422 v34 M{x} 56 v34", CREAM, 6)


@reg("royal-road")
def _(s):
    s.F("path", d="M0 330 C100 290 160 360 260 330 C360 300 420 340 512 310 V512 H0Z", fill=SAND)
    s.T("M20 460 C150 400 230 440 320 380 C380 340 440 380 500 340", BROWN, 28)
    s.F("rect", x=360, y=130, width=70, height=110, rx=6, fill=GOLD)
    s.F("polygon", points="352,130 395,80 438,130", fill=RED)
    s.F("path", d="M100 230 C100 190 160 190 160 230 L170 290 H90Z", fill=BLUE)
    s.F("circle", cx=130, cy=170, r=24, fill=SKIN)
    s.F("ellipse", cx=240, cy=300, rx=50, ry=26, fill=BROWN)
    s.F("circle", cx=282, cy=268, r=18, fill=BROWN)
    s.T("M210 322 V358 M270 322 V358", DBROWN, 10)


# ================================================================ americas-ancient
@reg("maya-civilization")
def _(s):
    ground(s, DGREEN, 430)
    for i, (w, y) in enumerate(((340, 350), (270, 290), (200, 230), (130, 170))):
        s.F("rect", x=256 - w / 2, y=y, width=w, height=60, fill=STONE if i % 2 == 0 else DSTONE)
    s.F("rect", x=216, y=110, width=80, height=60, fill=STONE)
    s.F("rect", outline=False, x=240, y=130, width=32, height=40, fill=BLACK)
    for x in range(200, 320, 20):
        s.M(f"M{x} 350 V430", DSTONE, 5)
    s.F("circle", cx=70, cy=360, r=60, fill=GREEN)
    s.F("circle", cx=450, cy=370, r=60, fill=DGREEN)


@reg("maya-pyramid")
def _(s):
    ground(s, GREEN, 440)
    for i, (w, y) in enumerate(((400, 390), (340, 330), (280, 270), (220, 210))):
        s.F("rect", x=256 - w / 2, y=y, width=w, height=60, fill=STONE if i % 2 == 0 else DSTONE)
    s.F("rect", x=206, y=120, width=100, height=90, fill=STONE)
    s.F("polygon", points="196,120 256,70 316,120", fill=DSTONE)
    s.F("rect", x=236, y=150, width=40, height=60, fill=BLACK)
    s.F("polygon", outline=False, points="236,450 276,450 270,210 242,210", fill=DSTONE)
    for y in range(220, 450, 30):
        s.M(f"M{242 - (y - 210) * 0.05:.0f} {y} H{270 + (y - 210) * 0.05:.0f}", STONE, 8)


@reg("maya-calendar")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=SAND)
    s.raw(f'<circle cx="256" cy="256" r="150" fill="none" stroke="{DSAND}" stroke-width="12"/>')
    for a in range(0, 360, 30):
        x, y = arc_pt(256, 256, 175, a)
        s.F("rect", outline=False, x=x - 18, y=y - 18, width=36, height=36, rx=8, fill=DBROWN, transform=f"rotate({a} {x:.0f} {y:.0f})")
    s.F("circle", cx=256, cy=256, r=70, fill=DSAND)
    s.F("circle", outline=False, cx=256, cy=256, r=34, fill=BROWN)
    for a in range(0, 360, 45):
        x, y = arc_pt(256, 256, 112, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=9, fill=DBROWN)


@reg("aztec-civilization")
def _(s):
    ground(s, GREEN, 440)
    s.F("rect", x=70, y=350, width=372, height=80, fill=STONE)
    s.F("rect", x=120, y=280, width=272, height=70, fill=DSTONE)
    s.F("rect", x=170, y=210, width=172, height=70, fill=STONE)
    s.F("rect", x=210, y=140, width=92, height=70, fill=RED)
    s.F("rect", x=232, y=160, width=48, height=50, fill=DRED)
    s.F("polygon", points="256,120 290,140 222,140", fill=GOLD)
    for x in range(180, 340, 20):
        s.M(f"M{x} 350 V430", DSTONE, 5)
    s.F("path", d="M60 440 V400 C60 380 100 380 100 400 V440Z", fill=DGREEN)


@reg("aztec-sun-stone")
def _(s):
    s.F("circle", cx=256, cy=256, r=210, fill=STONE)
    s.raw(f'<circle cx="256" cy="256" r="176" fill="none" stroke="{DSTONE}" stroke-width="14"/>')
    for a in range(0, 360, 20):
        x, y = arc_pt(256, 256, 192, a)
        s.F("rect", outline=False, x=x - 12, y=y - 12, width=24, height=24, rx=6, fill=DSTONE, transform=f"rotate({a} {x:.0f} {y:.0f})")
    s.F("circle", cx=256, cy=256, r=110, fill=DSTONE)
    s.F("circle", outline=False, cx=256, cy=256, r=74, fill=STONE)
    s.F("rect", outline=False, x=226, y=226, width=60, height=60, rx=14, fill=DSTONE)
    for x, y in ((226, 226), (286, 226)):
        dot(s, x + 4, y + 8, 7, BLACK)
    for a in range(0, 360, 45):
        x1, y1 = arc_pt(256, 256, 120, a + 22)
        x2, y2 = arc_pt(256, 256, 160, a + 22)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DSTONE, 12)


@reg("inca-civilization")
def _(s):
    s.F("polygon", points="0,440 130,170 220,300 310,120 420,330 512,230 512,512 0,512", fill=DSTONE)
    s.F("polygon", points="310,120 340,170 280,170", fill=WHITE)
    s.F("polygon", points="130,170 150,210 110,210", fill=WHITE)
    s.F("rect", x=80, y=380, width=200, height=60, fill=STONE)
    s.F("rect", x=100, y=330, width=160, height=50, fill=SAND)
    s.F("polygon", points="90,330 180,270 270,330", fill=DBROWN)
    s.F("circle", cx=420, cy=80, r=36, fill=YEL)


@reg("inca-terraces")
def _(s):
    for i, y in enumerate((130, 200, 270, 340, 410)):
        s.F("path", d=f"M{20 + i * 30} {y} H{492 - i * 30} V{y + 70} H{20 + i * 30}Z", fill=GREEN if i % 2 == 0 else DGREEN)
        s.F("rect", outline=False, x=20 + i * 30, y=y + 40, width=472 - i * 60, height=30, fill=STONE)
        for x in range(20 + i * 30, 492 - i * 30, 40):
            s.M(f"M{x} {y + 40} v30", DSTONE, 4)
    s.F("polygon", points="256,40 340,130 172,130", fill=DSTONE)


@reg("quipu")
def _(s):
    s.T("M60 110 H452", BROWN, 22)
    for i, x in enumerate(range(90, 440, 50)):
        c = (RED, YEL, BLUE, GREEN, CREAM, ORANGE, PURPLE)[i % 7]
        s.T(f"M{x} 110 V{300 + (i % 3) * 60}", c, 12)
        for k in range(1 + i % 4):
            s.F("circle", cx=x, cy=170 + k * 34, r=13, fill=c)


if __name__ == "__main__":
    run("history", D, sys.argv[1:] or None)
