"""history drawings B: Islamic golden age, medieval, Mughal/Ottoman, exploration, renaissance and industry, wars,
independence, weapons, archaeology. Run: python drawings/history_b.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hist import (INK, A1, A1D, A1L, A2, A2L, BLACK, BLUE, BROWN, CREAM, DARK, DBROWN, DGOLD, DGREEN, DGREY, DRED, DSAND, DSTONE, GLASS, GOLD, GREEN, GREY, HAIR, IRON, LIGHT, MID, NAVY, ORANGE, PINK, PURPLE, RED, SAND, SKIN, SKIN_D, SKY, STONE, TAN, WHITE, YEL, arc_pt, column, dot, flame, ground, lines, person, pyramid, registry, ring, run, scroll, star_pts, sun_disc, txt)  # noqa: E402

D, reg = registry()


def dome(s, cx, cy, r, color=SKY, fin=GOLD):
    s.F("path", d=f"M{cx - r} {cy} C{cx - r} {cy - r * 1.4} {cx + r} {cy - r * 1.4} {cx + r} {cy}Z", fill=color)
    s.T(f"M{cx} {cy - r * 1.05} V{cy - r * 1.4}", fin, 8)
    s.F("circle", cx=cx, cy=cy - r * 1.5, r=8, fill=fin)


def gear(s, cx, cy, r, color=IRON, teeth=10):
    pts = []
    for i in range(teeth * 2):
        rr = r if i % 2 == 0 else r * 0.78
        a0 = math.radians(i * 180 / teeth - 90 / teeth)
        a1 = math.radians((i + 1) * 180 / teeth - 90 / teeth)
        pts.append((cx + rr * math.cos(a0), cy + rr * math.sin(a0)))
        pts.append((cx + rr * math.cos(a1), cy + rr * math.sin(a1)))
    s.F("polygon", points=" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill=color)
    s.F("circle", outline=False, cx=cx, cy=cy, r=r * 0.3, fill=CREAM)


# ================================================================ islamic-golden-age
@reg("islamic-golden-age")
def _(s):
    s.F("rect", x=60, y=260, width=392, height=190, fill=CREAM)
    dome(s, 256, 260, 100, SKY, GOLD)
    for x in (60, 452):
        s.F("rect", x=x - 24, y=130, width=48, height=320, fill=CREAM)
        s.F("path", d=f"M{x - 30} 130 L{x} 70 L{x + 30} 130Z", fill=SKY)
        s.F("rect", outline=False, x=x - 6, y=200, width=12, height=30, rx=6, fill=BROWN)
    s.F("path", d="M220 450 V370 C220 330 292 330 292 370 V450Z", fill=BROWN)


@reg("house-of-wisdom")
def _(s):
    s.F("rect", x=40, y=330, width=432, height=120, fill=CREAM)
    s.F("rect", x=40, y=420, width=432, height=30, fill=SAND)
    for c in range(5):
        x = 62 + c * 84
        s.F("rect", x=x, y=60, width=70, height=250, fill=BROWN)
        for y in (80, 130, 180, 230, 280):
            s.F("rect", outline=False, x=x + 6, y=y, width=58, height=30, rx=4, fill=(RED, BLUE, GREEN, GOLD, PURPLE)[(y // 50 + c) % 5])
    s.F("path", d="M200 450 V390 C200 360 312 360 312 390 V450Z", fill=DBROWN)


@reg("astrolabe")
def _(s):
    s.F("path", d="M226 30 H286 V70 H226Z", fill=GOLD)
    s.F("circle", cx=256, cy=280, r=190, fill=GOLD)
    s.F("circle", cx=256, cy=280, r=150, fill=CREAM)
    for a in range(0, 360, 15):
        x1, y1 = arc_pt(256, 280, 150, a)
        x2, y2 = arc_pt(256, 280, 170, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DBROWN, 5)
    s.raw(f'<circle cx="256" cy="280" r="90" fill="none" stroke="{DGOLD}" stroke-width="8"/>')
    s.raw(f'<ellipse cx="256" cy="320" rx="80" ry="40" fill="none" stroke="{DGOLD}" stroke-width="8"/>')
    s.M("M256 130 V430 M106 280 H406", DGOLD, 6)
    s.open(transform="rotate(35 256 280)")
    s.F("path", d="M256 280 L90 258 L90 302Z", fill=DGOLD)
    s.F("path", d="M256 280 L422 258 L422 302Z", fill=DGOLD)
    s.close()
    s.F("circle", cx=256, cy=280, r=14, fill=RED)


@reg("islamic-manuscript")
def _(s):
    s.F("path", d="M60 90 H256 V440 H60Z", fill=CREAM)
    s.F("path", d="M256 90 H452 V440 H256Z", fill=SAND)
    s.F("rect", outline=False, x=80, y=110, width=156, height=310, rx=6, fill=CREAM)
    s.raw(f'<rect x="84" y="114" width="148" height="302" fill="none" stroke="{GOLD}" stroke-width="8"/>')
    s.raw(f'<rect x="280" y="114" width="148" height="302" fill="none" stroke="{GOLD}" stroke-width="8"/>')
    for y in range(150, 400, 36):
        s.M(f"M104 {y} h108 M300 {y} h108", DBROWN, 7)
    s.F("circle", cx=358, cy=250, r=34, fill=BLUE)
    s.F("polygon", points=star_pts(358, 250, 28, 12, 8), fill=GOLD)
    s.T("M256 90 V440", BROWN, 8)


@reg("arabic-numerals-history")
def _(s):
    for i, (n, c) in enumerate((("1", RED), ("2", BLUE), ("3", GREEN), ("4", ORANGE), ("5", PURPLE), ("0", DGOLD))):
        x = 50 + (i % 3) * 140
        y = 90 + (i // 3) * 170
        s.F("rect", x=x, y=y, width=124, height=150, rx=28, fill=c)
        txt(s, n, x + 62, y + 75, 56, 90, WHITE)
    s.T("M70 450 H442", DBROWN, 8)


@reg("algebra-book")
def _(s):
    s.F("path", d="M100 70 H390 C410 70 420 80 420 100 V420 C420 440 410 450 390 450 H100Z", fill=BLUE)
    s.F("rect", outline=False, x=140, y=70, width=14, height=380, fill=NAVY)
    s.F("rect", x=190, y=130, width=190, height=90, rx=14, fill=CREAM)
    txt(s, "x + 2", 285, 175, 150, 50, DBROWN)
    s.F("circle", cx=285, cy=330, r=50, fill=GOLD)
    s.F("polygon", points=star_pts(285, 330, 44, 20, 8), fill=DGOLD)


@reg("early-surgical-tools")
def _(s):
    s.T("M100 400 L250 150", IRON, 14)
    s.F("path", d="M250 150 C280 90 340 80 350 100 C340 140 290 160 250 150Z", fill=IRON)
    s.T("M160 420 L330 270", DGREY, 12)
    s.F("path", d="M330 270 L400 190 C420 190 420 220 400 250 L350 300Z", fill=IRON)
    s.T("M360 440 L420 330", BROWN, 22)
    s.F("path", d="M420 330 L440 270 L400 300Z", fill=IRON)
    s.F("rect", x=60, y=380, width=100, height=40, rx=12, fill=BROWN)


@reg("camera-obscura")
def _(s):
    s.F("rect", x=60, y=130, width=270, height=250, rx=14, fill=BROWN)
    s.F("circle", cx=60, cy=250, r=14, fill=DBROWN)
    s.F("rect", x=40, y=236, width=30, height=28, rx=6, fill=BLACK)
    s.F("polygon", points="50,250 250,180 250,330", fill=YEL)
    s.F("polygon", outline=False, points="50,250 250,180 250,330", fill=YEL, fill_opacity="0.4")
    s.F("rect", x=250, y=170, width=80, height=170, fill=CREAM)
    s.F("path", d="M290 230 L310 270 L270 270Z", fill=RED)
    s.F("rect", x=350, y=130, width=110, height=250, rx=10, fill=GLASS)
    s.F("path", outline=False, d="M390 340 V300 H420 V340Z", fill=BROWN)
    s.F("path", outline=False, d="M380 300 L405 250 L430 300Z", fill=GREEN)
    s.T("M90 380 V450 M300 380 V450", DBROWN, 14)


@reg("water-raising-machine")
def _(s):
    s.F("rect", x=20, y=400, width=472, height=60, fill=SKY)
    s.F("rect", outline=False, x=20, y=400, width=472, height=14, fill=WHITE, fill_opacity="0.5")
    s.open("part-wheel", "256 280")
    s.F("circle", cx=256, cy=280, r=170, fill=TAN)
    for a in range(0, 360, 30):
        x, y = arc_pt(256, 280, 170, a)
        s.T(f"M256 280 L{x:.0f} {y:.0f}", DBROWN, 8)
        s.F("rect", x=x - 20, y=y - 14, width=40, height=28, rx=8, fill=BROWN, transform=f"rotate({a + 90} {x:.0f} {y:.0f})")
    s.raw(f'<circle cx="256" cy="280" r="170" fill="none" stroke="{BROWN}" stroke-width="12"/>')
    s.F("circle", cx=256, cy=280, r=20, fill=DBROWN)
    s.close()
    s.T("M256 280 V460", DBROWN, 10)
    s.F("path", d="M380 60 H470 V110 H380Z", fill=SKY)


@reg("islamic-observatory")
def _(s):
    s.F("rect", x=90, y=180, width=332, height=280, fill=CREAM)
    s.F("path", d="M90 180 C90 60 422 60 422 180Z", fill=SKY)
    s.F("path", outline=False, d="M230 60 C245 30 267 30 282 60 L282 150 L230 150Z", fill=NAVY)
    s.T("M256 190 L330 60", IRON, 20)
    s.F("rect", x=330, y=36, width=70, height=36, rx=10, fill=IRON, transform="rotate(-30 365 54)")
    for x in (140, 372):
        s.F("path", d=f"M{x - 28} 460 V370 C{x - 28} 330 {x + 28} 330 {x + 28} 370 V460Z", fill=BROWN)
    s.F("polygon", points=star_pts(80, 70, 24, 10, 5), fill=YEL)
    s.F("polygon", points=star_pts(440, 110, 18, 8, 5), fill=YEL)


@reg("islamic-medicine-book")
def _(s):
    s.F("path", d="M100 70 H390 C410 70 420 80 420 100 V420 C420 440 410 450 390 450 H100Z", fill=GREEN)
    s.F("rect", outline=False, x=140, y=70, width=14, height=380, fill=DGREEN)
    s.F("rect", x=190, y=140, width=190, height=190, rx=20, fill=CREAM)
    s.F("path", outline=False, d="M262 190 H306 V232 H348 V276 H306 V318 H262 V276 H220 V232 H262Z", fill=RED)
    s.M("M200 390 H370", GOLD, 10)


@reg("quranic-manuscript")
def _(s):
    s.F("rect", x=70, y=60, width=372, height=392, rx=16, fill=CREAM)
    s.raw(f'<rect x="96" y="86" width="320" height="340" rx="8" fill="none" stroke="{GOLD}" stroke-width="12"/>')
    s.raw(f'<rect x="116" y="106" width="280" height="300" rx="4" fill="none" stroke="{BLUE}" stroke-width="6"/>')
    s.F("circle", cx=256, cy=256, r=96, fill=BLUE)
    s.F("polygon", points=star_pts(256, 256, 84, 44, 8), fill=GOLD)
    s.F("circle", cx=256, cy=256, r=34, fill=GREEN)
    for a in range(0, 360, 90):
        x, y = arc_pt(256, 256, 130, a)
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=10, fill=GOLD)


@reg("islamic-coins")
def _(s):
    for x, y, r in ((170, 190, 100), (330, 270, 90), (210, 380, 70)):
        s.F("circle", cx=x, cy=y, r=r, fill=GOLD)
        s.raw(f'<circle cx="{x}" cy="{y}" r="{r * 0.76:.0f}" fill="none" stroke="{DGOLD}" stroke-width="6"/>')
        s.F("polygon", points=star_pts(x, y, r * 0.5, r * 0.26, 8), fill=DGOLD)
        s.F("circle", outline=False, cx=x - r * 0.55, cy=y - r * 0.5, r=r * 0.11, fill=WHITE, fill_opacity="0.6")


# ================================================================ medieval
@reg("medieval-times")
def _(s):
    s.F("rect", x=40, y=210, width=130, height=230, fill=STONE)
    s.F("rect", x=342, y=210, width=130, height=230, fill=STONE)
    s.F("rect", x=170, y=280, width=172, height=160, fill=DSTONE)
    for x in (40, 342):
        for k in range(4):
            s.F("rect", x=x + k * 36, y=180, width=26, height=36, fill=STONE)
    s.F("path", d="M210 440 V350 C210 300 302 300 302 350 V440Z", fill=DBROWN)
    s.F("rect", x=225, y=60, width=6, height=100, fill=DBROWN)
    s.F("path", d="M231 60 H300 L280 90 L300 120 H231Z", fill=RED)
    s.F("rect", outline=False, x=96, y=250, width=20, height=44, rx=10, fill=BLACK)
    s.F("rect", outline=False, x=396, y=250, width=20, height=44, rx=10, fill=BLACK)


@reg("knight")
def _(s):
    person(s, 230, 470, 1.0, shirt=IRON, pants=DGREY, skin=SKIN, hair=None, hat="helmet", face=False)
    s.F("rect", outline=False, x=226, y=96, width=60, height=20, rx=8, fill=BLACK)
    s.F("path", d="M260 70 C240 20 290 10 330 30 C310 50 290 60 260 70Z", fill=RED)
    s.F("path", d="M330 220 H420 V310 C420 350 380 380 375 380 C370 380 330 350 330 310Z", fill=BLUE)
    s.M("M375 230 V370 M340 280 H410", WHITE, 10)
    s.T("M110 160 L90 420", BROWN, 10)
    s.F("polygon", points="110,170 90,100 130,100", fill=IRON)


@reg("knights-armour")
def _(s):
    s.F("path", d="M190 80 C190 40 322 40 322 80 V140 C322 160 300 170 256 170 C212 170 190 160 190 140Z", fill=IRON)
    s.F("rect", outline=False, x=220, y=100, width=72, height=14, rx=7, fill=BLACK)
    s.F("path", d="M140 190 H372 L350 400 H162Z", fill=IRON)
    s.F("path", outline=False, d="M180 200 L170 390 H220 L230 200Z", fill=WHITE, fill_opacity="0.35")
    s.F("circle", cx=140, cy=200, r=48, fill=IRON)
    s.F("circle", cx=372, cy=200, r=48, fill=IRON)
    s.F("rect", x=120, y=240, width=50, height=140, rx=20, fill=IRON)
    s.F("rect", x=342, y=240, width=50, height=140, rx=20, fill=IRON)
    s.F("rect", x=190, y=400, width=52, height=70, rx=14, fill=IRON)
    s.F("rect", x=270, y=400, width=52, height=70, rx=14, fill=IRON)
    s.M("M256 190 V400", DGREY, 8)


@reg("castle")
def _(s):
    ground(s, GREEN, 440)
    s.F("rect", x=80, y=220, width=352, height=220, fill=STONE)
    for x in (60, 410):
        s.F("rect", x=x, y=130, width=62, height=310, fill=DSTONE)
        for k in range(3):
            s.F("rect", x=x + k * 22 - 4, y=104, width=18, height=32, fill=DSTONE)
        s.F("rect", outline=False, x=x + 20, y=190, width=22, height=44, rx=10, fill=BLACK)
    s.F("rect", x=190, y=140, width=132, height=300, fill=STONE)
    for k in range(4):
        s.F("rect", x=190 + k * 36 - 2, y=112, width=24, height=34, fill=STONE)
    s.F("path", d="M226 440 V350 C226 300 286 300 286 350 V440Z", fill=DBROWN)
    s.T("M256 112 V60", DBROWN, 8)
    s.F("path", d="M256 60 H316 L296 82 L316 104 H256Z", fill=RED)


@reg("castle-tower")
def _(s):
    s.F("rect", x=170, y=110, width=172, height=350, fill=STONE)
    for k in range(4):
        s.F("rect", x=168 + k * 46, y=60, width=34, height=56, fill=STONE)
    for y in (180, 280, 380):
        s.M(f"M170 {y} H342", DSTONE, 6)
    s.F("rect", outline=False, x=240, y=150, width=32, height=70, rx=16, fill=BLACK)
    s.F("rect", outline=False, x=240, y=260, width=32, height=70, rx=16, fill=BLACK)
    s.F("path", d="M230 460 V400 C230 370 282 370 282 400 V460Z", fill=DBROWN)
    s.F("rect", x=140, y=450, width=232, height=28, rx=8, fill=DSTONE)


@reg("drawbridge")
def _(s):
    s.F("rect", x=40, y=60, width=432, height=260, fill=STONE)
    s.F("path", d="M170 320 V180 C170 110 342 110 342 180 V320Z", fill=BLACK)
    s.F("path", d="M190 320 V190 C190 135 322 135 322 190 V320Z", fill=DBROWN)
    for x in range(200, 320, 20):
        s.M(f"M{x} 150 V320", IRON, 5)
    s.F("polygon", points="170,320 342,320 380,450 130,450", fill=BROWN)
    for x in range(160, 360, 40):
        s.M(f"M{x} 320 L{130 + (x - 170) * 1.2:.0f} 450", DBROWN, 5)
    s.T("M170 200 L130 440 M342 200 L382 440", DGREY, 8)
    s.F("rect", x=0, y=450, width=512, height=40, fill=SKY)


@reg("moat")
def _(s):
    ground(s, GREEN, 300)
    s.F("rect", x=130, y=100, width=252, height=190, fill=STONE)
    for k in range(5):
        s.F("rect", x=130 + k * 52, y=76, width=36, height=30, fill=STONE)
    s.F("path", d="M226 290 V200 C226 160 286 160 286 200 V290Z", fill=DBROWN)
    s.F("path", d="M0 340 C100 320 160 370 256 350 C350 330 420 370 512 340 V460 C420 480 350 440 256 460 C160 480 100 440 0 460Z", fill=SKY)
    s.M("M60 400 C100 390 130 410 170 400 M300 420 C340 410 380 430 430 415", WHITE, 8)


@reg("village-medieval")
def _(s):
    ground(s, GREEN, 380)
    for x, w, h, c in ((40, 140, 110, CREAM), (200, 130, 140, TAN), (340, 130, 100, CREAM)):
        s.F("rect", x=x, y=420 - h, width=w, height=h, fill=c)
        s.F("polygon", points=f"{x - 14},{420 - h} {x + w / 2},{420 - h - 80} {x + w + 14},{420 - h}", fill=BROWN)
        s.M(f"M{x + 20} {420 - h + 10} L{x + 50} {420 - h + 50} M{x + w - 20} {420 - h + 10} L{x + w - 50} {420 - h + 50}", DBROWN, 7)
        s.F("rect", outline=False, x=x + w / 2 - 14, y=420 - 56, width=28, height=56, fill=DBROWN)
    s.F("circle", cx=440, cy=70, r=30, fill=YEL)


@reg("peasant")
def _(s):
    person(s, 230, 470, 1.0, shirt=TAN, pants=BROWN, skin=SKIN, hair=HAIR)
    s.F("path", d="M180 78 C196 36 316 36 332 78Z", fill=DBROWN)
    s.F("rect", x=170, y=70, width=170, height=14, rx=7, fill=DBROWN)
    s.T("M400 80 V440", BROWN, 12)
    s.F("path", d="M380 100 L430 90 L420 130Z", fill=IRON)
    s.T("M360 100 C380 70 420 70 440 100", IRON, 10)


@reg("kings-throne")
def _(s):
    s.F("path", d="M140 440 V130 C140 50 372 50 372 130 V440Z", fill=GOLD)
    s.F("path", outline=False, d="M170 420 V140 C170 90 220 80 256 80", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.4")
    s.F("rect", x=170, y=130, width=172, height=130, rx=24, fill=RED)
    s.F("rect", x=110, y=250, width=292, height=60, rx=18, fill=RED)
    s.F("rect", x=100, y=290, width=312, height=40, rx=12, fill=GOLD)
    s.F("rect", x=130, y=330, width=40, height=120, rx=10, fill=DGOLD)
    s.F("rect", x=342, y=330, width=40, height=120, rx=10, fill=DGOLD)
    s.F("circle", cx=256, cy=60, r=22, fill=RED)
    s.F("circle", outline=False, cx=256, cy=190, r=22, fill=GOLD)


@reg("crown-and-sceptre")
def _(s):
    s.F("path", d="M60 280 L80 130 L160 200 L256 100 L352 200 L432 130 L452 280Z", fill=GOLD)
    s.F("rect", x=60, y=280, width=392, height=60, rx=14, fill=DGOLD)
    for x, c in ((130, RED), (256, BLUE), (382, GREEN)):
        s.F("circle", cx=x, cy=310, r=20, fill=c)
    for x, y in ((80, 130), (256, 100), (432, 130)):
        s.F("circle", cx=x, cy=y, r=16, fill=WHITE)
    s.T("M80 470 L430 360", GOLD, 18)
    s.F("circle", cx=440, cy=355, r=30, fill=RED)


@reg("royal-seal")
def _(s):
    s.F("path", d="M256 70 C340 60 440 110 430 230 C450 300 400 440 256 440 C130 450 70 340 90 250 C60 160 140 70 256 70Z", fill=RED)
    s.raw(f'<circle cx="256" cy="250" r="130" fill="none" stroke="{DRED}" stroke-width="12"/>')
    s.F("path", d="M256 150 L280 220 L350 220 L292 262 L316 330 L256 290 L196 330 L220 262 L162 220 L232 220Z", fill=DRED)
    s.F("path", outline=False, d="M130 180 C150 130 200 100 250 96", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.4")


@reg("scroll-with-wax-seal")
def _(s):
    scroll(s, 100, 90, 312, 260, CREAM, BROWN)
    lines(s, 140, 150, 232, 4, 44, DBROWN, 9)
    s.F("circle", cx=256, cy=400, r=50, fill=RED)
    s.F("polygon", points=star_pts(256, 400, 34, 16, 6), fill=DRED)
    s.T("M222 440 L200 480 M290 440 L312 480", RED, 14)


@reg("quill-and-ink")
def _(s):
    s.F("path", d="M150 440 C150 390 190 380 256 380 C322 380 362 390 362 440 V450 H150Z", fill=NAVY)
    s.F("ellipse", cx=256, cy=380, rx=60, ry=14, fill=BLACK)
    s.F("path", d="M240 370 C250 300 330 180 440 60 C440 130 400 250 296 340Z", fill=WHITE)
    s.F("path", outline=False, d="M300 320 C340 240 390 150 430 80", fill="none", stroke=GREY, stroke_width="8", stroke_linecap="round")
    s.T("M246 372 L236 396", DBROWN, 8)


@reg("plague-doctor-mask")
def _(s):
    s.F("path", d="M170 130 C170 70 342 70 342 130 L350 210 C350 260 310 290 256 290 C202 290 162 260 162 210Z", fill=BLACK)
    s.F("path", d="M256 190 C256 190 340 250 330 350 C300 330 270 290 256 290Z", fill=DGREY)
    for x in (214, 298):
        s.F("circle", cx=x, cy=190, r=30, fill=CREAM)
        s.F("circle", outline=False, cx=x, cy=190, r=12, fill=BLACK)
    s.F("path", d="M130 90 H382 L350 120 H162Z", fill=DBROWN)
    s.F("rect", x=200, y=40, width=112, height=60, rx=16, fill=DBROWN)


# ================================================================ mughal-ottoman
@reg("mughal-empire")
def _(s):
    s.F("rect", x=90, y=250, width=332, height=190, fill=CREAM)
    s.F("path", d="M150 250 C150 120 362 120 362 250Z", fill=CREAM)
    s.F("path", d="M190 250 C190 160 322 160 322 250Z", fill=SAND)
    s.T("M256 118 V70", GOLD, 8)
    s.F("circle", cx=256, cy=62, r=12, fill=GOLD)
    for x in (70, 442):
        s.F("rect", x=x - 20, y=170, width=40, height=270, fill=CREAM)
        s.F("path", d=f"M{x - 26} 170 C{x - 26} 110 {x + 26} 110 {x + 26} 170Z", fill=RED)
    s.F("path", d="M220 440 V350 C220 300 292 300 292 350 V440Z", fill=RED)
    s.F("rect", x=60, y=440, width=392, height=26, rx=8, fill=SAND)


@reg("mughal-court")
def _(s):
    s.F("path", d="M110 90 C110 40 402 40 402 90 V140 H110Z", fill=RED)
    for x in range(120, 400, 40):
        s.F("path", outline=False, d=f"M{x} 140 q10 22 20 0", fill=GOLD)
    s.T("M120 140 V430 M392 140 V430", GOLD, 14)
    s.F("rect", x=170, y=300, width=172, height=100, rx=16, fill=GOLD)
    s.F("rect", x=150, y=380, width=212, height=60, rx=14, fill=DRED)
    s.F("rect", x=200, y=200, width=112, height=110, rx=24, fill=RED)
    s.F("circle", cx=256, cy=180, r=34, fill=SKIN)
    s.F("path", d="M220 170 C220 120 292 120 292 170Z", fill=GOLD)
    s.F("path", d="M256 112 C240 90 262 70 276 86", fill="none", stroke=RED, stroke_width="10", stroke_linecap="round")


@reg("mughal-miniature-painting")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=14, fill=GOLD)
    s.F("rect", x=84, y=84, width=344, height=344, rx=6, fill=CREAM)
    s.F("rect", outline=False, x=100, y=100, width=312, height=140, fill=SKY)
    s.F("rect", outline=False, x=100, y=240, width=312, height=172, fill=GREEN)
    s.F("path", d="M190 240 C190 150 322 150 322 240Z", fill=CREAM)
    s.F("circle", cx=256, cy=124, r=16, fill=YEL)
    s.F("path", d="M230 400 C230 330 282 330 282 400Z", fill=RED)
    s.F("circle", cx=256, cy=318, r=16, fill=SKIN)
    s.F("circle", cx=150, cy=360, r=24, fill=PINK)
    s.F("circle", cx=370, cy=350, r=24, fill=ORANGE)


@reg("mughal-garden")
def _(s):
    s.F("rect", x=40, y=40, width=432, height=432, fill=GREEN)
    s.F("rect", outline=False, x=240, y=40, width=32, height=432, fill=SKY)
    s.F("rect", outline=False, x=40, y=240, width=432, height=32, fill=SKY)
    s.F("circle", cx=256, cy=256, r=50, fill=SKY)
    s.F("circle", outline=False, cx=256, cy=256, r=26, fill=WHITE)
    for x, y in ((120, 120), (392, 120), (120, 392), (392, 392)):
        s.F("rect", x=x - 60, y=y - 60, width=120, height=120, fill=DGREEN)
        for dx, dy in ((-25, -25), (25, -25), (-25, 25), (25, 25)):
            s.F("circle", cx=x + dx, cy=y + dy, r=14, fill=(PINK, YEL, RED, PINK)[(dx > 0) + 2 * (dy > 0)])
    s.F("rect", x=40, y=40, width=432, height=432, fill="none")


@reg("mughal-arch")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=400, fill=CREAM)
    s.F("path", d="M130 460 V260 C130 160 200 130 256 70 C312 130 382 160 382 260 V460Z", fill=SAND)
    s.F("path", d="M170 460 V270 C170 200 220 180 256 130 C292 180 342 200 342 270 V460Z", fill=BLACK)
    s.F("path", d="M190 460 V280 C190 220 230 200 256 160 C282 200 322 220 322 280 V460Z", fill=DBROWN)
    s.raw(f'<path d="M130 260 C130 160 200 130 256 70 C312 130 382 160 382 260" fill="none" stroke="{GOLD}" stroke-width="8" stroke-dasharray="14 10"/>')
    for x in (96, 416):
        s.F("polygon", points=star_pts(x, 120, 20, 8, 8), fill=GOLD)


@reg("ottoman-empire")
def _(s):
    s.F("rect", x=130, y=250, width=252, height=190, fill=CREAM)
    s.F("path", d="M130 250 C130 100 382 100 382 250Z", fill=SKY)
    s.F("path", d="M60 360 C60 280 130 280 130 360Z M382 360 C382 280 452 280 452 360Z", fill=SKY)
    s.F("rect", x=60, y=360, width=70, height=80, fill=CREAM)
    s.F("rect", x=382, y=360, width=70, height=80, fill=CREAM)
    for x in (110, 402):
        s.F("rect", x=x - 12, y=120, width=24, height=140, fill=CREAM)
        s.F("polygon", points=f"{x - 18},120 {x},70 {x + 18},120", fill=SKY)
    s.T("M256 140 V90", GOLD, 8)
    s.F("path", d="M256 70 C240 80 240 100 256 110 C248 100 248 80 256 70Z", fill=GOLD)
    s.F("path", d="M220 440 V370 C220 330 292 330 292 370 V440Z", fill=BROWN)


@reg("ottoman-sultans-turban")
def _(s):
    s.F("path", d="M110 330 C80 220 140 130 256 130 C372 130 432 220 402 330 C380 400 130 400 110 330Z", fill=WHITE)
    for a in range(0, 5):
        s.M(f"M{130 + a * 8} {250 + a * 24} C{200} {200 + a * 20} {320} {200 + a * 20} {382 - a * 8} {250 + a * 24}", GREY, 10)
    s.F("circle", cx=256, cy=270, r=34, fill=GOLD)
    s.F("circle", outline=False, cx=256, cy=270, r=16, fill=RED)
    s.F("path", d="M256 236 C246 160 250 110 270 70 C282 110 280 160 276 236Z", fill=GREEN)
    s.F("path", outline=False, d="M262 130 C264 110 268 92 270 84", fill="none", stroke=WHITE, stroke_width="8", stroke_linecap="round")


@reg("janissary")
def _(s):
    person(s, 230, 470, 1.0, shirt=BLUE, pants=RED, skin=SKIN, hair=HAIR)
    s.F("path", d="M190 90 C190 40 320 40 320 90Z", fill=WHITE)
    s.F("path", d="M300 70 C340 80 360 140 340 200 C320 140 310 100 300 70Z", fill=WHITE)
    s.T("M400 110 L380 440", DBROWN, 12)
    s.F("rect", x=388, y=100, width=26, height=100, rx=10, fill=BROWN, transform="rotate(8 400 150)")
    s.M("M176 300 H336", GOLD, 12)


@reg("ottoman-cannon")
def _(s):
    s.open(transform="rotate(-14 256 256)")
    s.F("path", d="M60 220 H410 L450 200 V312 L410 292 H60 C40 292 40 220 60 220Z", fill=DGOLD)
    s.F("rect", x=130, y=210, width=36, height=92, rx=6, fill=GOLD)
    s.F("rect", x=250, y=210, width=36, height=92, rx=6, fill=GOLD)
    s.F("ellipse", cx=452, cy=256, rx=18, ry=58, fill=BLACK)
    s.close()
    s.F("circle", cx=190, cy=400, r=70, fill=TAN)
    s.raw(f'<circle cx="190" cy="400" r="58" fill="none" stroke="{DBROWN}" stroke-width="12"/>')
    for a in range(0, 360, 45):
        x, y = arc_pt(190, 400, 58, a)
        s.M(f"M190 400 L{x:.0f} {y:.0f}", DBROWN, 8)
    s.F("circle", cx=190, cy=400, r=14, fill=DBROWN)


@reg("tughra")
def _(s):
    s.raw(f'<path d="M110 400 C70 300 90 180 200 140 C300 100 400 150 410 250 C420 320 380 380 330 390" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M110 400 C70 300 90 180 200 140 C300 100 400 150 410 250 C420 320 380 380 330 390" fill="none" stroke="{GOLD}" stroke-width="20" stroke-linecap="round"/>')
    s.raw(f'<path d="M180 400 C150 320 160 220 230 190 C300 170 350 220 350 280" fill="none" stroke="{INK}" stroke-width="36" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M180 400 C150 320 160 220 230 190 C300 170 350 220 350 280" fill="none" stroke="{BLUE}" stroke-width="16" stroke-linecap="round"/>')
    s.T("M150 440 H400", GOLD, 18)
    for x in (200, 260, 320):
        s.T(f"M{x} 440 V200", GOLD, 12)


# ================================================================ age-of-exploration
@reg("age-of-exploration")
def _(s):
    s.F("rect", x=0, y=340, width=512, height=172, fill=SKY)
    s.M("M20 400 C80 380 120 420 180 400 C240 380 300 420 360 400 C420 380 460 420 500 400", WHITE, 10)
    s.F("path", d="M110 330 H400 L370 410 H140Z", fill=BROWN)
    s.T("M256 330 V70", DBROWN, 14)
    s.F("path", d="M256 90 C340 110 370 200 360 290 H256Z", fill=CREAM)
    s.F("path", d="M256 110 C190 130 160 210 168 290 H256Z", fill=WHITE)
    s.F("polygon", points="256,70 320,86 256,100", fill=RED)
    s.M("M290 150 v90 M270 190 h40", RED, 14)
    sun_disc(s, 440, 80, 34, YEL)


@reg("old-world-map")
def _(s):
    s.F("path", d="M60 80 L100 70 L160 90 L230 70 L300 92 L380 72 L440 90 L450 160 L436 250 L452 340 L430 440 L360 424 L290 446 L220 424 L150 440 L90 420 L70 330 L84 240 L62 160Z", fill=CREAM)
    s.F("path", outline=False, d="M120 150 C150 120 200 130 220 160 C230 200 190 230 160 220 C130 210 100 180 120 150Z", fill=SAND)
    s.F("path", outline=False, d="M270 130 C310 110 380 130 380 180 C370 230 300 240 280 200Z", fill=SAND)
    s.F("path", outline=False, d="M200 280 C240 260 300 280 300 330 C290 380 220 390 200 340Z", fill=SAND)
    s.M("M110 380 C150 340 220 410 280 370 C330 340 380 390 410 360", BLUE, 7, dash="12 12")
    s.F("polygon", points=star_pts(400, 130, 30, 12, 8), fill=RED)
    s.F("path", outline=False, d="M340 300 l22 -40 l22 40", fill="none", stroke=RED, stroke_width="0")


@reg("spyglass")
def _(s):
    s.open(transform="rotate(-30 256 256)")
    s.F("rect", x=40, y=220, width=110, height=72, rx=10, fill=BROWN)
    s.F("rect", x=140, y=210, width=130, height=92, rx=10, fill=GOLD)
    s.F("rect", x=260, y=196, width=130, height=120, rx=10, fill=BROWN)
    s.F("rect", x=380, y=184, width=100, height=144, rx=12, fill=GOLD)
    s.F("ellipse", cx=480, cy=256, rx=12, ry=64, fill=SKY)
    s.M("M60 230 V282 M80 230 V282", DBROWN, 5)
    s.close()


@reg("spice-trade")
def _(s):
    for x, y, c, lab in ((140, 330, RED, ""), (256, 350, ORANGE, ""), (372, 330, YEL, "")):
        s.F("path", d=f"M{x - 80} {y - 70} H{x + 80} L{x + 100} {y + 80} C{x + 100} {y + 130} {x - 100} {y + 130} {x - 100} {y + 80}Z", fill=BROWN)
        s.F("path", d=f"M{x - 80} {y - 70} C{x - 60} {y - 130} {x + 60} {y - 130} {x + 80} {y - 70}Z", fill=c)
    s.F("path", d="M60 180 C60 130 130 130 130 180Z", fill=GREEN)
    s.F("polygon", points=star_pts(400, 150, 32, 14, 8), fill=PURPLE)
    s.T("M230 140 L290 100", DBROWN, 14)
    s.T("M300 150 L340 110", DBROWN, 14)


@reg("navigators-astrolabe")
def _(s):
    s.F("circle", cx=256, cy=290, r=170, fill=GOLD)
    s.F("circle", cx=256, cy=290, r=130, fill=CREAM)
    for a in range(0, 360, 10):
        x1, y1 = arc_pt(256, 290, 130, a)
        x2, y2 = arc_pt(256, 290, 150, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DBROWN, 4)
    s.M("M256 290 L130 150", DGOLD, 8)
    s.open(transform="rotate(-55 256 290)")
    s.F("path", d="M256 290 L110 272 L110 308Z", fill=DGOLD)
    s.F("path", d="M256 290 L402 272 L402 308Z", fill=DGOLD)
    s.close()
    s.F("circle", cx=256, cy=290, r=14, fill=RED)
    s.raw(f'<circle cx="256" cy="60" r="34" fill="none" stroke="{INK}" stroke-width="36" data-outline="under"/>')
    s.raw(f'<circle cx="256" cy="60" r="34" fill="none" stroke="{GOLD}" stroke-width="16"/>')


# ================================================================ renaissance-industry
@reg("renaissance")
def _(s):
    s.F("rect", x=60, y=230, width=392, height=210, fill=CREAM)
    s.F("path", d="M120 230 C120 100 392 100 392 230Z", fill=RED)
    s.T("M256 118 V70", GOLD, 8)
    s.F("circle", cx=256, cy=64, r=12, fill=GOLD)
    for x in range(100, 420, 70):
        s.F("path", d=f"M{x - 26} 440 V320 C{x - 26} 280 {x + 26} 280 {x + 26} 320 V440Z", fill=DBROWN)
    s.F("rect", x=40, y=230, width=432, height=26, rx=8, fill=SAND)


@reg("renaissance-painting-easel")
def _(s):
    s.T("M130 460 L220 120 M390 460 L300 120 M170 330 H350", DBROWN, 18)
    s.F("rect", x=130, y=150, width=252, height=190, fill=CREAM)
    s.F("rect", outline=False, x=148, y=168, width=216, height=154, fill=SKY)
    s.F("path", outline=False, d="M148 322 L220 250 L270 290 L330 230 L364 262 V322Z", fill=GREEN)
    s.F("circle", outline=False, cx=320, cy=206, r=18, fill=YEL)
    s.F("path", d="M390 400 L470 290 L486 300 L406 410Z", fill=BROWN)
    s.F("path", d="M386 410 L408 412 L400 440 C390 440 380 430 386 410Z", fill=RED)


@reg("printing-workshop")
def _(s):
    s.F("rect", x=60, y=100, width=40, height=340, rx=8, fill=BROWN)
    s.F("rect", x=250, y=100, width=40, height=340, rx=8, fill=BROWN)
    s.F("rect", x=50, y=70, width=250, height=44, rx=12, fill=DBROWN)
    s.T("M175 110 V220", IRON, 26)
    s.F("rect", x=110, y=230, width=130, height=30, rx=8, fill=IRON)
    s.F("rect", x=80, y=380, width=210, height=60, rx=12, fill=BROWN)
    s.F("rect", x=330, y=240, width=130, height=170, rx=10, fill=CREAM)
    s.M("M350 280 h90 M350 310 h70 M350 340 h90 M350 370 h60", BLACK, 8)
    s.T("M330 440 H460", DBROWN, 10)


@reg("industrial-revolution")
def _(s):
    s.F("rect", x=40, y=300, width=432, height=150, fill="#A0522D")
    s.F("rect", x=60, y=200, width=60, height=100, fill="#A0522D")
    for x in (370, 430):
        s.F("rect", x=x - 20, y=60, width=40, height=240, fill="#A0522D")
        s.F("rect", x=x - 24, y=50, width=48, height=20, fill=DBROWN)
        s.F("circle", cx=x - 10, cy=20, r=26, fill=GREY)
    s.F("path", d="M40 300 L130 230 L130 300 L220 230 L220 300 L310 230 L310 300Z", fill=DSTONE)
    for x in (80, 190, 300):
        s.F("rect", outline=False, x=x, y=340, width=50, height=44, fill=YEL)
    s.F("rect", x=20, y=450, width=472, height=24, rx=8, fill=DGREY)


@reg("steam-factory")
def _(s):
    s.F("rect", x=60, y=240, width=300, height=200, fill="#A0522D")
    s.F("polygon", points="60,240 135,170 135,240", fill="#A0522D")
    s.F("polygon", points="135,240 210,170 210,240", fill="#A0522D")
    s.F("polygon", points="210,240 285,170 285,240", fill="#A0522D")
    s.F("rect", x=380, y=100, width=60, height=340, fill="#A0522D")
    s.F("rect", x=372, y=90, width=76, height=24, fill=DBROWN)
    for x, y, r in ((400, 60, 30), (440, 30, 24), (390, 20, 18)):
        s.F("circle", cx=x, cy=y, r=r, fill=GREY)
    for x in (100, 190, 280):
        s.F("rect", outline=False, x=x, y=300, width=56, height=56, rx=6, fill=YEL)
    s.F("rect", x=20, y=440, width=472, height=24, rx=8, fill=DGREY)


@reg("textile-mill")
def _(s):
    s.F("rect", x=40, y=230, width=432, height=220, fill="#A0522D")
    for k in range(6):
        s.F("rect", outline=False, x=66 + k * 68, y=270, width=44, height=64, rx=8, fill=YEL)
        s.F("rect", outline=False, x=66 + k * 68, y=360, width=44, height=64, rx=8, fill=YEL)
    s.F("polygon", points="40,230 256,120 472,230", fill=DBROWN)
    s.F("circle", cx=256, cy=190, r=30, fill=CREAM)
    s.M("M256 190 V168 M256 190 L272 200", BLACK, 6)
    s.F("rect", x=420, y=60, width=36, height=130, fill="#A0522D")
    s.F("circle", cx=438, cy=40, r=22, fill=GREY)


@reg("coal-mine")
def _(s):
    s.F("path", d="M0 280 C60 220 100 280 160 250 C240 200 300 260 360 230 C420 200 470 240 512 220 V512 H0Z", fill=DBROWN)
    s.F("path", d="M100 460 V330 C100 280 160 250 256 250 C352 250 412 280 412 330 V460Z", fill=BLACK)
    s.T("M120 330 V460 M392 330 V460 M110 340 H402", BROWN, 22)
    s.F("path", d="M170 460 L210 400 H320 L360 460Z", fill=DGREY)
    s.F("circle", cx=200, cy=460, r=20, fill=BLACK)
    s.F("circle", cx=330, cy=460, r=20, fill=BLACK)
    for x, y in ((230, 420), (270, 410), (300, 424), (250, 400)):
        s.F("circle", outline=False, cx=x, cy=y, r=14, fill=BLACK)
    s.F("rect", x=380, y=60, width=60, height=100, fill=BROWN)
    s.F("polygon", points="370,60 410,20 450,60", fill=DBROWN)


@reg("child-labour-history")
def _(s):
    s.F("rect", x=20, y=400, width=472, height=60, rx=14, fill=DGREY)
    s.F("path", d="M240 400 L270 320 H450 L470 400Z", fill=DGREY)
    for x, y in ((290, 300), (340, 290), (400, 300), (440, 310)):
        s.F("circle", cx=x, cy=y, r=24, fill=BLACK)
    s.F("circle", cx=290, cy=420, r=22, fill=BLACK)
    s.F("circle", cx=440, cy=420, r=22, fill=BLACK)
    person(s, 130, 460, 0.55, shirt=DGREY, pants=DBROWN, skin=SKIN, hair=HAIR)
    s.T("M170 330 L250 340", BROWN, 8)


# ================================================================ wars
@reg("world-war")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=SKY)
    s.F("path", outline=False, d="M120 200 C150 150 210 160 230 200 C240 240 200 270 160 260 C120 250 100 230 120 200Z", fill=GREEN)
    s.F("path", outline=False, d="M290 150 C340 130 400 160 390 210 C380 260 320 280 290 240Z", fill=GREEN)
    s.F("path", outline=False, d="M230 310 C270 290 330 320 310 380 C280 420 230 400 230 350Z", fill=GREEN)
    s.F("polygon", points=star_pts(256, 256, 160, 80, 12), fill=ORANGE)
    s.F("polygon", points=star_pts(256, 256, 100, 52, 12), fill=YEL)
    s.F("circle", outline=False, cx=256, cy=256, r=30, fill=WHITE)


@reg("trench")
def _(s):
    s.F("rect", x=0, y=200, width=512, height=312, fill=DBROWN)
    s.F("path", d="M0 280 H512 V430 H0Z", fill=BROWN)
    s.F("path", outline=False, d="M0 280 H512 V300 H0Z", fill=TAN)
    for x in range(10, 500, 70):
        s.F("rect", x=x, y=300, width=40, height=130, fill=DBROWN)
    s.T("M30 210 C100 190 140 230 220 205 C320 180 400 230 480 200", GREY, 10)
    for x in range(40, 480, 60):
        s.M(f"M{x} 205 l12 -18 m-6 6 l14 14", GREY, 6)
    s.F("circle", cx=420, cy=100, r=34, fill=GREY)


@reg("war-helmet")
def _(s):
    s.F("path", d="M70 330 C70 180 150 100 256 100 C362 100 442 180 442 330 C442 350 420 360 400 360 H112 C92 360 70 350 70 330Z", fill="#5C6B4E")
    s.F("path", d="M50 340 H462 C470 340 470 372 462 372 H50 C42 372 42 340 50 340Z", fill="#4A5A3E")
    s.F("path", outline=False, d="M110 300 C110 200 170 140 240 128", fill="none", stroke=WHITE, stroke_width="16", stroke_linecap="round", stroke_opacity="0.4")
    s.T("M170 372 L170 430 M342 372 V430", DBROWN, 10)


@reg("war-medal")
def _(s):
    s.F("path", d="M170 40 H260 L300 190 H210Z", fill=RED)
    s.F("path", d="M340 40 H250 L212 190 H302Z", fill=BLUE)
    s.F("circle", cx=256, cy=300, r=120, fill=GOLD)
    s.raw(f'<circle cx="256" cy="300" r="90" fill="none" stroke="{DGOLD}" stroke-width="8"/>')
    s.F("polygon", points=star_pts(256, 300, 70, 30, 5), fill=DGOLD)
    s.F("circle", outline=False, cx=200, cy=240, r=14, fill=WHITE, fill_opacity="0.5")


@reg("peace-treaty")
def _(s):
    scroll(s, 90, 90, 332, 290, CREAM, BROWN)
    lines(s, 130, 150, 250, 3, 40, DBROWN, 9)
    s.M("M130 290 C170 270 190 310 230 290", BLUE, 8)
    s.F("path", d="M330 340 C330 300 400 300 400 340 C400 380 340 390 330 340Z", fill=WHITE)
    s.F("circle", cx=395, cy=384, r=34, fill=RED)
    s.F("path", d="M372 420 C400 400 430 420 430 440 C410 460 380 450 372 420Z", fill=GREEN)


@reg("war-memorial")
def _(s):
    s.F("rect", x=140, y=390, width=232, height=50, rx=8, fill=STONE)
    s.F("rect", x=170, y=340, width=172, height=52, rx=8, fill=DSTONE)
    s.F("polygon", points="256,50 300,120 312,340 200,340 212,120", fill=STONE)
    s.F("polygon", outline=False, points="256,50 300,120 312,340 262,340 262,100", fill=DSTONE)
    s.F("polygon", points="256,50 300,120 212,120", fill=STONE)
    s.F("rect", outline=False, x=236, y=180, width=40, height=90, rx=6, fill=DSTONE)
    s.M("M256 190 V260 M240 215 H272", STONE, 8)
    s.F("circle", cx=380, cy=440, r=18, fill=RED)
    s.F("circle", cx=140, cy=440, r=18, fill=RED)


# ================================================================ independence (themed)
@reg("independence-movement")
def _(s):
    s.T("M120 50 V450", DARK, 16)
    s.F("path", d="M136 60 H400 L370 140 L400 220 H136Z", fill=A2)
    s.F("polygon", points=star_pts(240, 140, 44, 19, 5), fill=LIGHT)
    for x in (200, 280, 360):
        s.F("path", d=f"M{x - 28} 460 C{x - 28} 380 {x + 28} 380 {x + 28} 460Z", fill=DARK)
        s.F("circle", cx=x, cy=360, r=22, fill=DARK)


@reg("freedom-march")
def _(s):
    s.F("rect", x=0, y=440, width=512, height=30, rx=10, fill=MID)
    for i, x in enumerate((90, 180, 270, 360, 450)):
        h = 330 + (i % 2) * 14
        s.F("circle", cx=x, cy=h - 70, r=24, fill=DARK)
        s.F("path", d=f"M{x - 28} 440 C{x - 28} {h} {x + 28} {h} {x + 28} 440Z", fill=DARK)
    s.T("M270 360 V120", DARK, 10)
    s.F("path", d="M280 124 H380 V210 H280Z", fill=A1)
    s.F("rect", outline=False, x=280, y=150, width=100, height=28, fill=LIGHT)
    s.F("circle", outline=False, cx=330, cy=164, r=10, fill=A2)


@reg("spinning-wheel")
def _(s):
    s.F("rect", x=70, y=360, width=370, height=50, rx=14, fill=A2)
    s.open("part-wheel", "200 240")
    s.raw(f'<circle cx="200" cy="240" r="130" fill="none" stroke="{INK}" stroke-width="36" data-outline="under"/>')
    s.raw(f'<circle cx="200" cy="240" r="130" fill="none" stroke="{A2}" stroke-width="16"/>')
    for a in range(0, 360, 30):
        x, y = arc_pt(200, 240, 124, a)
        s.T(f"M200 240 L{x:.0f} {y:.0f}", A2L, 7)
    s.close()
    s.F("circle", cx=200, cy=240, r=18, fill=DARK)
    s.T("M200 240 V360 M340 360 V250", A2, 18)
    s.F("rect", x=320, y=210, width=130, height=44, rx=16, fill=LIGHT)
    s.M("M200 240 L335 232", MID, 5)


@reg("salt-march")
def _(s):
    s.F("rect", x=0, y=440, width=512, height=30, rx=10, fill=MID)
    s.F("circle", cx=200, cy=130, r=36, fill=DARK)
    s.F("path", d="M150 440 C150 280 250 280 250 440Z", fill=DARK)
    s.T("M270 120 L300 440", DARK, 12)
    s.F("polygon", points="320,440 430,440 470,400 430,350 350,350", fill=LIGHT)
    for x, y in ((350, 380), (390, 370), (420, 400)):
        s.F("polygon", outline=False, points=f"{x},{y - 14} {x + 14},{y} {x},{y + 14} {x - 14},{y}", fill=A1L)
    s.F("circle", cx=440, cy=90, r=30, fill=A2)


@reg("protest-placards")
def _(s):
    for x, c, rot in ((130, A1, -10), (256, A2, 4), (382, A1D, 12)):
        s.T(f"M{x} 460 V250", DARK, 12)
        s.F("rect", x=x - 80, y=110, width=160, height=140, rx=12, fill=c, transform=f"rotate({rot} {x} 180)")
        s.M(f"M{x - 50} 160 h100 M{x - 50} 200 h80", LIGHT, 12)
    for x in (130, 256, 382):
        s.F("path", d=f"M{x - 34} 470 C{x - 34} 410 {x + 34} 410 {x + 34} 470Z", fill=DARK)


@reg("freedom-fighters-silhouette")
def _(s):
    s.F("path", d="M0 440 C100 400 200 450 300 420 C400 390 460 430 512 410 V512 H0Z", fill=MID)
    for x, k in ((130, 1.0), (260, 0.9), (380, 1.0)):
        s.open(transform=f"translate({x} 440) scale({k}) translate(-256 -440)")
        s.F("circle", cx=256, cy=200, r=34, fill=DARK)
        s.F("path", d="M210 440 C210 280 302 280 302 440Z", fill=DARK)
        s.T("M290 300 L330 200", DARK, 14)
        s.close()
    s.T("M388 330 V140", DARK, 8)
    s.F("path", d="M394 140 H470 V200 H394Z", fill=A1)
    s.F("circle", outline=False, cx=432, cy=170, r=12, fill=A2)


@reg("partition-train")
def _(s):
    s.F("rect", x=20, y=440, width=472, height=18, rx=6, fill=DARK)
    s.F("rect", x=40, y=200, width=130, height=230, rx=12, fill=A1)
    s.F("rect", x=180, y=200, width=130, height=230, rx=12, fill=A2)
    s.F("rect", x=320, y=240, width=160, height=190, rx=16, fill=A1D)
    s.F("rect", x=390, y=190, width=80, height=60, rx=10, fill=A1D)
    for x in (60, 100, 200, 240):
        s.F("rect", outline=False, x=x, y=240, width=30, height=40, rx=8, fill=LIGHT)
        s.F("circle", outline=False, cx=x + 15, cy=252, r=11, fill=DARK)
    for x in (80, 200, 340, 430):
        s.F("circle", cx=x + 20, cy=440, r=22, fill=DARK)
    s.F("rect", outline=False, x=410, y=270, width=50, height=50, rx=8, fill=A1L)
    s.F("circle", cx=440, cy=150, r=22, fill=MID)
    s.F("circle", cx=464, cy=110, r=16, fill=MID)


@reg("new-national-flag")
def _(s):
    s.T("M120 470 V60", DARK, 18)
    s.F("circle", cx=120, cy=50, r=22, fill=A2)
    s.F("path", d="M138 80 C200 60 260 110 340 90 C390 80 420 90 440 100 V300 C420 290 390 280 340 290 C260 310 200 260 138 280Z", fill=A2)
    s.F("path", outline=False, d="M138 80 C200 60 260 110 340 90 C390 80 420 90 440 100 L138 280Z", fill=A1)
    s.F("polygon", points=star_pts(300, 190, 40, 17, 5), fill=LIGHT)


# ================================================================ weapons-armour
@reg("sword")
def _(s):
    s.open(transform="rotate(-45 256 256)")
    s.F("path", d="M246 40 H266 L274 340 H238Z", fill=GREY)
    s.F("polygon", points="246,40 266,40 256,12", fill=GREY)
    s.M("M256 60 V330", WHITE, 6)
    s.F("rect", x=170, y=336, width=172, height=26, rx=13, fill=GOLD)
    s.F("rect", x=240, y=362, width=32, height=78, rx=10, fill=BROWN)
    s.F("circle", cx=256, cy=452, r=22, fill=GOLD)
    s.close()


@reg("scimitar")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    s.F("path", d="M130 90 C260 60 400 150 380 300 C360 220 250 150 130 160Z", fill=GREY)
    s.F("path", outline=False, d="M150 108 C260 90 370 160 372 250", fill="none", stroke=WHITE, stroke_width="7")
    s.F("rect", x=60, y=100, width=26, height=100, rx=8, fill=GOLD)
    s.F("rect", x=82, y=96, width=40, height=78, rx=8, fill=BROWN)
    s.close()


@reg("katana")
def _(s):
    s.open(transform="rotate(-38 256 256)")
    s.F("path", d="M60 244 H380 C410 244 440 250 470 256 C440 262 410 268 380 268 H60Z", fill=GREY)
    s.M("M90 250 H360", WHITE, 4)
    s.F("ellipse", cx=56, cy=256, rx=10, ry=30, fill=BLACK)
    s.F("rect", x=-20, y=240, width=76, height=32, rx=12, fill=NAVY)
    s.M("M-4 240 l12 32 M18 240 l12 32 M40 240 l12 32", RED, 5)
    s.close()


@reg("dagger")
def _(s):
    s.open(transform="rotate(-40 256 256)")
    s.F("path", d="M246 60 H266 L292 300 H220Z", fill=GREY)
    s.F("polygon", outline=False, points="256,60 266,60 276,300 256,300", fill=WHITE, fill_opacity="0.4")
    s.F("rect", x=190, y=298, width=132, height=24, rx=12, fill=GOLD)
    s.F("rect", x=240, y=320, width=32, height=70, rx=10, fill=RED)
    s.F("circle", cx=256, cy=400, r=18, fill=GOLD)
    s.close()


@reg("spear")
def _(s):
    s.T("M70 450 L370 130", BROWN, 18)
    s.F("path", d="M360 150 L400 30 L460 120 L420 190Z", fill=GREY)
    s.F("polygon", outline=False, points="400,50 440,120 420,150", fill=WHITE, fill_opacity="0.4")
    s.F("rect", x=340, y=170, width=100, height=20, rx=8, fill=GOLD, transform="rotate(48 390 180)")
    s.T("M110 410 L90 440", RED, 16)


@reg("bow-and-arrow")
def _(s):
    s.raw(f'<path d="M150 60 C60 160 60 360 150 460" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M150 60 C60 160 60 360 150 460" fill="none" stroke="{BROWN}" stroke-width="20" stroke-linecap="round"/>')
    s.M("M150 60 L100 260 L150 460", TAN, 5)
    s.T("M100 260 H450", DBROWN, 10)
    s.F("polygon", points="454,260 416,236 416,284", fill=GREY)
    s.F("path", d="M100 260 L76 232 L88 260 L76 288Z", fill=RED)


@reg("crossbow")
def _(s):
    s.F("rect", x=240, y=100, width=32, height=360, rx=12, fill=BROWN)
    s.raw(f'<path d="M80 160 C160 90 352 90 432 160" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M80 160 C160 90 352 90 432 160" fill="none" stroke="{DBROWN}" stroke-width="20" stroke-linecap="round"/>')
    s.M("M80 160 L256 220 L432 160", TAN, 5)
    s.T("M256 220 V90", GREY, 10)
    s.F("polygon", points="256,60 238,100 274,100", fill=GREY)
    s.F("rect", x=226, y=320, width=60, height=30, rx=8, fill=DBROWN)


@reg("mace")
def _(s):
    s.T("M120 440 L330 230", BROWN, 24)
    s.F("circle", cx=370, cy=190, r=80, fill=IRON)
    for a in range(0, 360, 45):
        x, y = arc_pt(370, 190, 80, a)
        x2, y2 = arc_pt(370, 190, 118, a)
        s.F("polygon", points=f"{x - 12 * math.sin(math.radians(a)):.0f},{y + 12 * math.cos(math.radians(a)):.0f} {x2:.0f},{y2:.0f} {x + 12 * math.sin(math.radians(a)):.0f},{y - 12 * math.cos(math.radians(a)):.0f}", fill=DGREY)
    s.F("circle", outline=False, cx=348, cy=168, r=16, fill=WHITE, fill_opacity="0.5")
    s.F("rect", x=100, y=410, width=40, height=40, rx=10, fill=GOLD, transform="rotate(-45 120 430)")


@reg("battle-axe")
def _(s):
    s.T("M110 450 L340 120", BROWN, 22)
    s.F("path", d="M330 70 C430 60 470 130 440 210 C410 160 360 150 320 170Z", fill=GREY)
    s.F("path", d="M330 70 C290 100 280 170 320 170 L350 150Z", fill=IRON)
    s.F("path", outline=False, d="M360 90 C420 90 440 130 430 170", fill="none", stroke=WHITE, stroke_width="8", stroke_opacity="0.6")
    s.T("M130 410 L160 440", RED, 14)


@reg("shield")
def _(s):
    s.F("path", d="M256 50 L440 110 V260 C440 360 360 430 256 470 C152 430 72 360 72 260 V110Z", fill=BLUE)
    s.F("path", outline=False, d="M256 80 L416 130 V260 C416 340 350 400 256 440Z", fill=NAVY, fill_opacity="0.5")
    s.M("M256 90 V440 M100 220 H412", GOLD, 18)
    s.F("circle", cx=256, cy=220, r=34, fill=GOLD)
    s.F("circle", outline=False, cx=256, cy=220, r=14, fill=RED)


@reg("chainmail")
def _(s):
    s.F("path", d="M190 60 L110 100 L60 300 L130 320 L150 230 V440 H362 V230 L382 320 L452 300 L402 100 L322 60 C310 110 202 110 190 60Z", fill=IRON)
    for r in range(11):
        for c in range(10):
            x, y = 100 + c * 32 + (r % 2) * 16, 100 + r * 32
            if 150 < x < 372 or (y < 330 and 60 < x < 452):
                s.raw(f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{DGREY}" stroke-width="3"/>')
    s.F("path", outline=False, d="M190 60 C202 110 310 110 322 60 C300 130 212 130 190 60Z", fill=DGREY)


@reg("helmet-with-plume")
def _(s):
    s.F("path", d="M110 300 C100 160 170 100 256 100 C342 100 412 160 402 300 V400 H350 V320 C350 290 330 280 256 280 C182 280 162 290 162 320 V400 H110Z", fill=IRON)
    s.F("rect", outline=False, x=190, y=190, width=132, height=16, rx=8, fill=BLACK)
    s.M("M256 190 V280", BLACK, 12)
    s.F("path", d="M256 100 C190 50 150 20 120 60 C150 70 170 90 190 130 C220 120 240 110 256 100Z", fill=RED)
    s.F("path", d="M256 100 C300 50 350 40 400 70 C370 80 340 100 322 130 C300 120 280 110 256 100Z", fill=DRED)
    s.F("path", outline=False, d="M130 270 C130 180 180 130 240 118", fill="none", stroke=WHITE, stroke_width="14", stroke_linecap="round", stroke_opacity="0.5")


@reg("catapult")
def _(s):
    s.F("rect", x=60, y=410, width=392, height=40, rx=12, fill=BROWN)
    s.T("M120 410 L200 240 M340 410 L260 240", DBROWN, 20)
    s.T("M200 240 H260", DBROWN, 20)
    s.T("M230 240 L110 100", BROWN, 18)
    s.F("path", d="M60 70 H140 L130 130 H70Z", fill=DBROWN)
    s.F("circle", cx=100, cy=64, r=30, fill=DGREY)
    s.F("circle", cx=140, cy=450, r=34, fill=TAN)
    s.F("circle", cx=380, cy=450, r=34, fill=TAN)
    s.raw(f'<circle cx="140" cy="450" r="26" fill="none" stroke="{DBROWN}" stroke-width="8"/>')
    s.raw(f'<circle cx="380" cy="450" r="26" fill="none" stroke="{DBROWN}" stroke-width="8"/>')


@reg("trebuchet")
def _(s):
    s.F("rect", x=60, y=420, width=392, height=36, rx=12, fill=BROWN)
    s.T("M130 420 L210 170 M330 420 L250 170 M170 300 H290", DBROWN, 20)
    s.T("M230 170 L420 90", BROWN, 16)
    s.T("M230 170 L130 280", BROWN, 16)
    s.F("rect", x=96, y=270, width=70, height=90, rx=10, fill=DGREY)
    s.T("M430 90 C460 130 450 180 430 190", TAN, 6)
    s.F("circle", cx=430, cy=210, r=26, fill=DGREY)


@reg("cannon")
def _(s):
    s.open(transform="rotate(-18 256 250)")
    s.F("path", d="M60 210 H400 L450 190 V320 L400 300 H60 C40 300 40 210 60 210Z", fill=DGREY)
    s.F("rect", x=100, y=200, width=34, height=108, rx=6, fill=IRON)
    s.F("rect", x=240, y=200, width=34, height=108, rx=6, fill=IRON)
    s.F("ellipse", cx=452, cy=255, rx=16, ry=64, fill=BLACK)
    s.close()
    s.F("circle", cx=190, cy=400, r=70, fill=TAN)
    s.raw(f'<circle cx="190" cy="400" r="58" fill="none" stroke="{DBROWN}" stroke-width="12"/>')
    for a in range(0, 360, 45):
        x, y = arc_pt(190, 400, 58, a)
        s.M(f"M190 400 L{x:.0f} {y:.0f}", DBROWN, 8)
    s.F("circle", cx=190, cy=400, r=14, fill=DBROWN)
    s.F("circle", cx=440, cy=420, r=30, fill=BLACK)


@reg("musket")
def _(s):
    s.open(transform="rotate(-25 256 256)")
    s.F("rect", x=60, y=240, width=380, height=24, rx=10, fill=IRON)
    s.F("path", d="M40 230 H190 L220 280 L200 310 H60 C40 310 30 250 40 230Z", fill=BROWN)
    s.F("rect", x=190, y=230, width=70, height=40, rx=8, fill=GOLD)
    s.F("path", d="M250 262 C240 290 270 300 280 280", fill="none", stroke=DGREY, stroke_width="8", stroke_linecap="round")
    s.F("rect", x=400, y=232, width=40, height=40, rx=10, fill=GOLD)
    s.close()


@reg("siege-tower")
def _(s):
    s.F("rect", x=120, y=60, width=240, height=370, fill=BROWN)
    for y in (60, 160, 260, 360):
        s.M(f"M120 {y} H360", DBROWN, 8)
    s.M("M120 60 L360 160 M360 60 L120 160 M120 260 L360 360 M360 260 L120 360", DBROWN, 6)
    s.F("rect", x=100, y=40, width=280, height=40, rx=8, fill=DBROWN)
    for k in range(5):
        s.F("rect", x=100 + k * 62, y=14, width=36, height=36, fill=DBROWN)
    s.F("rect", outline=False, x=200, y=180, width=80, height=60, rx=8, fill=BLACK)
    s.F("polygon", points="360,100 470,150 470,210 360,200", fill=BROWN)
    for x in (160, 330):
        s.F("circle", cx=x, cy=440, r=34, fill=TAN)
        s.raw(f'<circle cx="{x}" cy="440" r="26" fill="none" stroke="{DBROWN}" stroke-width="8"/>')


# ================================================================ archaeology
@reg("archaeology")
def _(s):
    s.F("rect", x=0, y=300, width=512, height=212, fill=DBROWN)
    s.F("path", d="M0 300 C100 260 200 320 300 280 C400 250 460 290 512 270 V310 H0Z", fill=SAND)
    s.F("path", d="M120 300 C120 230 170 230 190 270 C200 300 190 340 190 380 H120Z", fill=CREAM)
    s.F("ellipse", cx=310, cy=360, rx=70, ry=34, fill=CREAM)
    s.T("M360 100 L290 200", BROWN, 14)
    s.F("path", d="M360 100 L420 60 L430 110Z", fill=IRON)


@reg("excavation-site")
def _(s):
    s.F("rect", x=0, y=230, width=512, height=282, fill=DBROWN)
    s.F("path", d="M60 230 H452 V430 H60Z", fill=BROWN)
    s.F("path", outline=False, d="M60 230 H452 V260 H60Z", fill=TAN)
    for y in (310, 370):
        s.M(f"M60 {y} H452", DBROWN, 6)
    s.T("M120 150 V230 M392 150 V230", DBROWN, 12)
    s.M("M120 160 H392", DBROWN, 6, dash="10 10")
    s.F("ellipse", cx=250, cy=400, rx=60, ry=22, fill=CREAM)
    s.F("path", d="M300 330 C310 290 350 290 360 330 L370 400 H290Z", fill="#C2622E")


@reg("archaeologists-brush")
def _(s):
    s.T("M130 440 L300 270", BROWN, 36)
    s.F("rect", x=290, y=220, width=50, height=60, rx=8, fill=GOLD, transform="rotate(-45 315 250)")
    s.F("path", d="M330 200 L430 100 L470 140 L370 240Z", fill=TAN)
    for k in range(5):
        s.M(f"M{350 + k * 18} {220 - k * 18} L{410 + k * 16} {170 - k * 14}", DBROWN, 6)
    s.F("ellipse", cx=150, cy=420, rx=80, ry=28, fill=DBROWN)
    s.F("path", d="M110 420 C110 380 190 380 190 420Z", fill=CREAM)


@reg("ancient-pottery-shards")
def _(s):
    s.F("path", d="M90 200 L200 120 L260 200 L230 300 L110 290Z", fill="#C2622E")
    s.M("M110 230 L230 200 M120 260 L240 240", CREAM, 8)
    s.F("path", d="M280 180 L400 140 L440 240 L350 310 L290 270Z", fill="#A0522D")
    s.M("M300 210 L410 180", CREAM, 8)
    s.F("path", d="M150 330 L270 340 L290 420 L180 450 L130 400Z", fill="#C2622E")
    s.M("M160 370 L270 380", CREAM, 8)
    s.F("path", d="M330 340 L430 330 L440 420 L350 440Z", fill="#8A3E1B")


@reg("ruins")
def _(s):
    ground(s, GREEN, 430)
    s.F("rect", x=60, y=170, width=50, height=270, fill=STONE)
    s.F("rect", x=180, y=270, width=50, height=170, fill=STONE)
    s.F("polygon", points="260,440 260,200 310,160 310,440", fill=STONE)
    s.F("rect", x=360, y=330, width=100, height=110, fill=DSTONE)
    s.F("rect", x=40, y=140, width=100, height=34, rx=8, fill=DSTONE)
    s.F("rect", x=40, y=440, width=432, height=24, rx=8, fill=DSTONE)
    s.F("circle", cx=330, cy=400, r=24, fill=STONE)
    s.F("path", d="M120 440 C110 400 130 380 150 400 C160 420 150 440 150 440Z", fill=DGREEN)


@reg("ancient-coins-hoard")
def _(s):
    s.F("path", d="M110 230 H402 C420 340 400 440 256 440 C112 440 92 340 110 230Z", fill=BROWN)
    s.F("ellipse", cx=256, cy=230, rx=146, ry=36, fill=DBROWN)
    for x, y, r in ((180, 200, 40), (256, 180, 44), (330, 200, 40), (216, 150, 38), (300, 150, 38), (256, 110, 36)):
        s.F("circle", cx=x, cy=y, r=r, fill=GOLD)
        s.F("circle", outline=False, cx=x, cy=y, r=r * 0.55, fill=DGOLD)
    s.F("circle", cx=110, cy=420, r=32, fill=GOLD)
    s.F("circle", cx=410, cy=430, r=28, fill=GOLD)


@reg("time-capsule")
def _(s):
    s.F("path", d="M150 110 C150 50 362 50 362 110 V380 C362 440 150 440 150 380Z", fill=IRON)
    s.F("path", outline=False, d="M180 100 V380", fill="none", stroke=WHITE, stroke_width="18", stroke_linecap="round", stroke_opacity="0.4")
    s.F("rect", x=140, y=180, width=232, height=24, rx=10, fill=DGREY)
    s.F("rect", x=140, y=290, width=232, height=24, rx=10, fill=DGREY)
    s.F("rect", x=200, y=210, width=112, height=76, rx=10, fill=GLASS)
    s.M("M220 235 H290 M220 258 H270", BLUE, 8)
    s.F("ellipse", cx=256, cy=460, rx=120, ry=20, fill=DBROWN)


@reg("museum-artefact")
def _(s):
    s.F("rect", x=130, y=330, width=252, height=130, rx=10, fill=STONE)
    s.F("rect", x=110, y=450, width=292, height=26, rx=8, fill=DSTONE)
    s.F("rect", x=140, y=70, width=232, height=270, rx=14, fill=GLASS, fill_opacity="0.6")
    s.F("path", d="M210 300 C200 250 220 210 256 190 C292 210 312 250 302 300Z", fill="#C2622E")
    s.F("ellipse", cx=256, cy=190, rx=40, ry=12, fill="#8A3E1B")
    s.M("M210 250 H300", CREAM, 7)
    s.M("M160 90 L190 120", WHITE, 8)


if __name__ == "__main__":
    run("history", D, sys.argv[1:] or None)
