"""celebrations-holidays drawings. Run: python drawings/celebrations_holidays.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import *  # noqa: E402,F401,F403
from _parts import place as P  # noqa: E402
from _parts2 import *  # noqa: E402,F401,F403
from draw_lib import C, arc_pt, head, run, star_pts, stroke_text  # noqa: E402

D = {}
K = C
GOLD, GOLDD, WHITEK = K["gold"], K["darkgold"], K["white"]
RED, GREEN, BLUE, YEL, ORANGE, PINK, PURPLE = K["red"], K["green"], K["blue"], K["yellow"], K["orange"], K["pink"], K["purple"]


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def scene(*steps):
    def fn(s):
        for st in steps:
            if callable(st):
                st(s)
            else:
                part, x, y, sc, *rest = st
                P(s, part, x, y, sc, **(rest[0] if rest else {}))
    return fn


# ---------------------------------------------------------------- reusable party parts
def balloon(s, color=A2, hi=A2L, x=256, y=200, r=110):
    s.T(f"M{x} {y + r * 1.15} C{x - 20} {y + r * 1.6} {x + 20} {y + r * 2} {x} {y + r * 2.5}", DARK, 4)
    s.F("ellipse", cx=x, cy=y, rx=r * 0.86, ry=r, fill=color)
    s.F("polygon", points=f"{x - 12},{y + r + 14} {x + 12},{y + r + 14} {x},{y + r - 4}", fill=color)
    s.F("ellipse", outline=False, cx=x - r * 0.34, cy=y - r * 0.4, rx=r * 0.16, ry=r * 0.26, fill=hi, transform=f"rotate(-25 {x - r * 0.34} {y - r * 0.4})")


def confetti_bits(s, n=18, seed=1, box=(60, 60, 452, 452)):
    import random
    random.seed(seed)
    cols = (A1, A2, "#4CB963", A1L, A2L, "#F7A1B5")
    for _ in range(n):
        x = random.uniform(box[0], box[2]); y = random.uniform(box[1], box[3])
        c = random.choice(cols)
        if random.random() < 0.5:
            s.F("rect", outline=False, x=f"{x:.0f}", y=f"{y:.0f}", width=14, height=24, rx=3, fill=c, transform=f"rotate({random.randint(0, 180)} {x:.0f} {y:.0f})")
        else:
            s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=8, fill=c)


def firework(s, x, y, r, color=A2, n=12):
    for k in range(n):
        a = k * 360 / n
        x1, y1 = arc_pt(x, y, r * 0.3, a); x2, y2 = arc_pt(x, y, r, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", color, max(6, r * 0.08))
        s.F("circle", outline=False, cx=f"{x2:.0f}", cy=f"{y2:.0f}", r=max(5, r * 0.07), fill=color)


def cake(s, layers=2, color=A2L, icing=LIGHT, candles=3):
    if layers >= 2:
        s.F("rect", x=110, y=320, width=292, height=120, rx=16, fill=color)
        s.F("path", d="M110 340 C130 370 150 340 170 370 C190 340 210 370 230 340 C250 370 270 340 290 370 C310 340 330 370 350 340 C370 370 390 340 402 360 V336 H110Z", fill=icing)
    s.F("rect", x=150, y=220, width=212, height=110, rx=16, fill=A1L)
    s.F("path", d="M150 240 C170 270 190 240 210 270 C230 240 250 270 270 240 C290 270 310 240 330 270 C350 240 362 260 362 260 V236 H150Z", fill=icing)
    for i in range(candles):
        x = 256 + (i - (candles - 1) / 2) * 50
        s.F("rect", x=x - 9, y=150, width=18, height=70, rx=5, fill=A2 if i % 2 else A1)
        s.open("part-flame", f"{x:.0f} 140")
        s.F("path", d=f"M{x:.0f} 104 C{x + 16:.0f} 122 {x + 14:.0f} 140 {x:.0f} 146 C{x - 14:.0f} 140 {x - 16:.0f} 122 {x:.0f} 104Z", fill=K["orange"])
        s.close()


def lantern(s, x=256, y=256, sc=1.0, glass=K["yellow"], body=GOLD):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -256)")
    s.T("M256 40 V90", GOLDD, 8)
    s.F("path", d="M206 90 H306 L326 130 H186Z", fill=body)
    s.F("path", d="M190 130 H322 L340 330 H172Z", fill=glass)
    s.M("M210 130 L200 330 M256 130 V330 M302 130 L312 330", GOLDD, 8)
    s.F("path", d="M172 330 H340 L300 380 H212Z", fill=body)
    s.F("circle", cx=256, cy=400, r=14, fill=body)
    s.close()


def crescent(s, cx, cy, r, color=GOLD):
    outer = [arc_pt(cx, cy, r, a) for a in range(60, 301, 10)]
    inner = [arc_pt(cx + r * 0.42, cy, r * 0.78, a) for a in range(290, 69, -10)]
    s.F("polygon", points=" ".join(f"{x:.1f},{y:.1f}" for x, y in outer + inner), fill=color)


def diya(s, x=256, y=300, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -300)")
    s.F("path", d="M100 300 C140 400 372 400 412 300 C380 320 132 320 100 300Z", fill=ORANGE)
    s.F("path", d="M100 300 C130 280 382 280 412 300 C380 320 132 320 100 300Z", fill=K["darkred"])
    s.open("part-flame", "256 280")
    s.F("path", d="M256 140 C296 190 300 250 256 280 C212 250 216 190 256 140Z", fill=YEL)
    s.close()
    s.close()


def ring(s, x=256, y=300, r=110, stone=None, color=GOLD):
    s.T(f"M{x} {y - r} A{r} {r * 0.9} 0 1 1 {x - 0.1} {y - r}", color, 26)
    if stone:
        s.F("polygon", points=f"{x - 40},{y - r - 10} {x + 40},{y - r - 10} {x + 24},{y - r - 50} {x - 24},{y - r - 50}", fill=stone)
        s.F("polygon", points=f"{x - 40},{y - r - 10} {x + 40},{y - r - 10} {x},{y - r + 30}", fill=stone)


def flag_pole(s, colors_fn, x=150):
    s.T(f"M{x} 470 V70", K["darkgrey"], 14)
    s.F("circle", cx=x, cy=66, r=14, fill=GOLD)
    colors_fn(s, x + 8, 90)


def flag_india(s, x, y, w=260, h=170):
    for i, c in enumerate(("#FF9933", K["white"], "#138808")):
        s.F("rect", x=x, y=y + i * h / 3, width=w, height=h / 3, fill=c, outline=False)
    s.F("rect", x=x, y=y, width=w, height=h, fill="none")
    s.raw(f'<circle cx="{x + w / 2}" cy="{y + h / 2}" r="{h / 8}" fill="none" stroke="#000080" stroke-width="4"/>')


def flag_uae(s, x, y, w=260, h=150):
    s.F("rect", outline=False, x=x, y=y, width=w / 4, height=h, fill=RED)
    for i, c in enumerate(("#00732F", K["white"], "#000000")):
        s.F("rect", outline=False, x=x + w / 4, y=y + i * h / 3, width=w * 3 / 4, height=h / 3, fill=c)
    s.F("rect", x=x, y=y, width=w, height=h, fill="none")


def person_dance(s, shirt=A1, flip=False):
    P(s, person, 256, 256, 1.0, flip=flip, shirt=shirt, pose="cheer")


# ---------------------------------------------------------------- party
D["balloon"] = lambda s: balloon(s, A2, A2L, 256, 190, 140)
D["balloons-bunch"] = lambda s: (balloon(s, A1, A1L, 180, 180, 90), balloon(s, A2, A2L, 330, 170, 95), balloon(s, "#4CB963", "#9BD7A8", 256, 120, 90))
D["party-hat"] = lambda s: (s.F("polygon", points="256,70 380,430 132,430", fill=A1), s.M("M200 260 L290 230 M170 350 L330 300", A2, 18),
                            s.F("circle", cx=256, cy=70, r=30, fill=A2), s.F("ellipse", cx=256, cy=432, rx=130, ry=24, fill=A2))
D["party-popper"] = lambda s: (s.F("polygon", points="110,430 200,230 300,330", fill=A2), s.M("M140 360 L230 280 M160 410 L260 320", A1, 12),
                               s.M("M260 240 C300 180 340 160 380 170 M290 280 C350 260 390 280 430 260 M240 200 C240 150 270 110 300 90", A1, 10), confetti_bits(s, 12, 3, (270, 60, 470, 260)))
D["confetti"] = lambda s: confetti_bits(s, 40, 7)
D["streamers"] = lambda s: [s.M(f"M{x} 60 C{x + 60} 140 {x - 60} 220 {x} 300 C{x + 60} 380 {x - 40} 420 {x} 460", c, 18) for x, c in ((130, A1), (256, A2), (382, "#4CB963"))]
D["bunting"] = lambda s: (s.M("M30 120 C150 220 362 220 482 120", DARK, 6), [s.F("polygon", points=f"{x - 30},{y} {x + 30},{y} {x},{y + 80}", fill=c)
                                                                               for (x, y), c in zip(((80, 150), (160, 186), (256, 200), (352, 186), (432, 150)), (A1, A2, "#4CB963", A2, A1))])
D["gift-box"] = lambda s: P(s, gift, 256, 256, 1.0)
D["gift-bag"] = lambda s: (s.F("path", d="M120 200 H392 L412 450 H100Z", fill=A1), s.T("M190 200 C190 120 322 120 322 200", A1D, 14),
                           s.F("path", d="M210 200 L230 120 L256 170 L282 120 L302 200Z", fill=A2), P(s, star, 256, 330, 0.25))
D["ribbon-bow"] = lambda s: (s.F("path", d="M256 256 C180 160 80 180 100 260 C120 330 200 300 256 256Z", fill=A2), s.F("path", d="M256 256 C332 160 432 180 412 260 C392 330 312 300 256 256Z", fill=A2),
                             s.F("path", d="M240 270 L180 440 L220 420 L240 450 Z", fill=A2), s.F("path", d="M272 270 L332 440 L292 420 L272 450 Z", fill=A2), s.F("circle", cx=256, cy=256, r=34, fill=A1))
D["greeting-card"] = lambda s: (s.F("polygon", points="256,100 420,140 420,430 256,400", fill=LIGHT), s.F("polygon", points="256,100 92,140 92,430 256,400", fill=A1L),
                                P(s, heart, 340, 260, 0.25))
D["invitation-card"] = lambda s: (s.F("rect", x=96, y=120, width=320, height=290, rx=16, fill=LIGHT), s.F("polygon", points="96,120 256,260 416,120", fill=A1L),
                                  s.F("circle", cx=256, cy=250, r=36, fill=A2), s.M("M150 330 H362 M180 370 H332", MID, 12))
D["fireworks"] = lambda s: (firework(s, 180, 180, 120, A2), firework(s, 360, 280, 100, A1), firework(s, 200, 380, 60, "#4CB963", 10))
D["sparkler"] = lambda s: (s.T("M150 460 L300 200", MID, 10), [s.M(f"M300 200 L{x:.0f} {y:.0f}", A2, 6) for x, y in (arc_pt(300, 200, 100, a) for a in range(0, 360, 30))],
                           s.F("circle", cx=300, cy=200, r=24, fill=YEL))
D["firecracker"] = lambda s: (s.F("rect", x=196, y=160, width=120, height=280, rx=16, fill=RED), s.M("M196 240 H316 M196 360 H316", GOLD, 12),
                              s.T("M256 160 C256 120 290 110 300 80", DARK, 6), s.F("polygon", points=star_pts(300, 70, 34, 12, 8), fill=YEL))
D["party-lights"] = lambda s: (s.M("M30 140 C150 260 362 260 482 140", DARK, 6), [(s.F("ellipse", cx=f"{x:.0f}", cy=f"{y + 30:.0f}", rx=18, ry=28, fill=c), s.F("rect", x=f"{x - 10:.0f}", y=f"{y:.0f}", width=20, height=12, fill=MID))
                                                                                    for (x, y), c in zip(((70, 170), (150, 210), (256, 228), (362, 210), (442, 170)), (A2, A1, "#4CB963", A2, A1))])
D["disco-ball"] = lambda s: (s.T("M256 30 V90", DARK, 6), s.F("circle", cx=256, cy=260, r=170, fill=MID),
                             [s.F("rect", outline=False, x=110 + c * 44, y=110 + r * 44, width=38, height=38, rx=4, fill=(LIGHT if (r + c) % 3 == 0 else A1L if (r + c) % 3 == 1 else MID))
                              for r in range(7) for c in range(7) if (110 + c * 44 + 19 - 256) ** 2 + (110 + r * 44 + 19 - 260) ** 2 < 150 ** 2],
                             s.F("circle", cx=256, cy=260, r=170, fill="none"))
D["candles-on-cake"] = lambda s: cake(s, 2, candles=5)
D["pinata"] = lambda s: (s.T("M256 30 V100", DARK, 6), s.F("polygon", points=star_pts(256, 240, 150, 70, 5), fill=A2),
                         s.F("circle", cx=256, cy=246, r=56, fill=A1), [s.T(f"M{x:.0f} {y:.0f} L{x:.0f} {y + 70:.0f}", c, 12)
                         for (x, y), c in zip((arc_pt(256, 240, 150, a) for a in (18, 90, 162)), (A1, "#4CB963", A1))])

# ---------------------------------------------------------------- eid and ramadan
D["eid-al-fitr"] = lambda s: (crescent(s, 200, 220, 140, GOLD), lantern(s, 380, 260, 0.6), P(s, star, 400, 80, 0.15))
D["eid-al-adha"] = lambda s: (P(s, lambda s: (crescent(s, 256, 256, 160, GOLD)), 160, 160, 0.6),
                              [s.F("circle", cx=x, cy=y, r=40, fill=LIGHT) for x, y in ((240, 340), (290, 320), (330, 350), (280, 370))],
                              s.F("ellipse", cx=380, cy=310, rx=30, ry=24, fill=MID), [s.T(f"M{x} 380 V440", MID, 12) for x in (250, 320)])
D["eidi"] = lambda s: (s.F("rect", x=80, y=150, width=352, height=220, rx=16, fill="#4CB963"), s.F("polygon", points="80,150 256,280 432,150", fill="#2F8A4A"),
                       crescent(s, 256, 300, 34, GOLD), s.F("rect", x=140, y=100, width=230, height=90, rx=8, fill="#9BD7A8", transform="rotate(-8 255 145)"))
D["eid-moon-sighting"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#F5913E"), crescent(s, 340, 140, 50, "#FFF1C2"),
                                    s.F("rect", outline=False, x=20, y=330, width=472, height=142, fill="#6E4A2A"), P(s, person, 160, 290, 0.45, pose="point"))
D["eid-gift-box"] = lambda s: (P(s, gift, 256, 290, 0.9, color="#4CB963"), crescent(s, 256, 300, 40, GOLD))
D["eid-decorations"] = lambda s: (s.M("M30 80 C150 160 362 160 482 80", DARK, 6), [lantern(s, x, 210, 0.35) for x in (110, 256, 400)],
                                  [crescent(s, x, 170, 24, GOLD) for x in (180, 330)], [s.F("polygon", points=star_pts(x, 140, 16, 7, 5), fill=GOLD) for x in (60, 452)])
D["eid-greeting-card"] = lambda s: (s.F("rect", x=96, y=80, width=320, height=360, rx=20, fill="#2F8A4A"), crescent(s, 230, 230, 90, GOLD),
                                    s.F("polygon", points=star_pts(330, 190, 30, 12, 5), fill=GOLD), s.M("M150 380 H362", GOLD, 8))
D["sheer-khurma"] = lambda s: (s.F("path", d="M100 230 H412 C412 360 350 420 256 420 C162 420 100 360 100 230Z", fill=LIGHT), s.F("ellipse", cx=256, cy=230, rx=156, ry=40, fill="#F7E3C4"),
                               [s.M(f"M{x} {y} q14 -10 28 0", "#E8B878", 8) for x, y in ((170, 220), (220, 240), (280, 220), (320, 236))],
                               [s.F("ellipse", outline=False, cx=x, cy=y, rx=10, ry=6, fill="#4CB963") for x, y in ((200, 226), (300, 240))])
D["fanous"] = lambda s: lantern(s)
D["crescent-lights"] = lambda s: (crescent(s, 230, 240, 170, "#2C5FC9"), [s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=10, fill=YEL) for x, y in (arc_pt(230, 240, 150, a) for a in range(80, 290, 20))])
D["ramadan-calendar"] = lambda s: (P(s, calendar, 256, 256, 1.0), crescent(s, 256, 140, 22, GOLD))
D["iftar-table"] = lambda s: (s.F("rect", x=40, y=300, width=432, height=40, rx=8, fill=K["brown"]), s.T("M80 340 V440 M432 340 V440", K["darkbrown"], 18),
                              [s.F("circle", cx=x, cy=270, r=40, fill=LIGHT) for x in (120, 256, 392)], [s.F("ellipse", cx=x, cy=262, rx=16, ry=9, fill=K["darkbrown"]) for x in (110, 130)],
                              s.F("rect", x=240, y=200, width=32, height=70, rx=6, fill="#8FD0FF"), s.F("circle", cx=392, cy=262, r=24, fill=ORANGE))
D["ramadan-garland"] = lambda s: (s.M("M30 100 C150 200 362 200 482 100", DARK, 6), [crescent(s, x, y, 30, GOLD) for x, y in ((90, 170), (256, 210), (420, 170))],
                                  [s.F("polygon", points=star_pts(x, y, 24, 10, 5), fill=GOLD) for x, y in ((170, 200), (340, 200))])

# ---------------------------------------------------------------- diwali and holi
D["diwali"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#2B2350"), firework(s, 140, 140, 80, YEL), firework(s, 380, 120, 70, PINK),
                         [diya(s, x, 360, 0.4) for x in (130, 256, 382)])
D["rangoli"] = lambda s: ([s.F("ellipse", cx=256, cy=140, rx=50, ry=110, fill=c, transform=f"rotate({a} 256 256)") for a, c in zip(range(0, 360, 45), (RED, YEL, BLUE, GREEN) * 2)],
                          [s.F("circle", cx=256, cy=256, r=r, fill=c) for r, c in ((90, PINK), (60, ORANGE), (30, YEL))])
D["diwali-lamps-row"] = lambda s: [diya(s, x, 300, 0.32) for x in (70, 160, 256, 352, 442)]
D["lantern-kandil"] = lambda s: (s.T("M256 30 V90", DARK, 6), s.F("polygon", points="256,90 400,220 256,400 112,220", fill=ORANGE), s.F("polygon", points="256,140 340,220 256,330 172,220", fill=YEL),
                                 [s.T(f"M{x} 400 L{x} 470", c, 8) for x, c in ((220, RED), (256, PINK), (292, RED))])
D["diwali-sweets-box"] = lambda s: (s.F("rect", x=80, y=200, width=352, height=220, rx=16, fill=GOLD), s.F("rect", outline=False, x=100, y=220, width=312, height=180, rx=10, fill="#FFF1C2"),
                                    [s.F("circle", cx=140 + c * 78, cy=270 + r * 80, r=30, fill=(ORANGE, YEL, PINK, "#E8B878")[(r + c) % 4]) for r in range(2) for c in range(4)])
D["diwali-fireworks"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#2B2350"), firework(s, 160, 180, 110, YEL), firework(s, 350, 240, 120, PINK), firework(s, 260, 380, 60, GREEN))
D["holi"] = lambda s: ([s.F("circle", cx=x, cy=y, r=r, fill=c) for x, y, r, c in ((160, 180, 100, PINK), (330, 170, 90, YEL), (250, 320, 110, GREEN), (380, 340, 70, BLUE), (130, 360, 60, ORANGE))],
                       confetti_bits(s, 20, 4))
D["gulal"] = lambda s: [(s.F("path", d=f"M{x - 70} {y} H{x + 70} C{x + 70} {y + 60} {x - 70} {y + 60} {x - 70} {y}Z", fill=MID), s.F("ellipse", cx=x, cy=y, rx=70, ry=24, fill=c),
                         s.F("path", outline=False, d=f"M{x - 50} {y} C{x - 30} {y - 50} {x + 30} {y - 50} {x + 50} {y}Z", fill=c))
                        for x, y, c in ((140, 200, PINK), (372, 200, YEL), (140, 380, GREEN), (372, 380, BLUE))]
D["pichkari"] = lambda s: (s.F("rect", x=100, y=210, width=230, height=90, rx=40, fill=YEL), s.F("rect", x=330, y=240, width=90, height=30, rx=10, fill=ORANGE),
                           s.T("M60 255 H100", BLUE, 30), [s.F("circle", cx=x, cy=255 + (x % 3 - 1) * 12, r=12, fill=PINK) for x in (440, 465, 490)])
D["holi-colour-splash"] = lambda s: [s.F("path", d=f"M{x} {y} C{x + 60} {y - 80} {x + 140} {y - 20} {x + 100} {y + 40} C{x + 160} {y + 90} {x + 60} {y + 140} {x + 20} {y + 90} "
                                                    f"C{x - 40} {y + 140} {x - 90} {y + 60} {x - 40} {y + 20} C{x - 100} {y - 30} {x - 30} {y - 80} {x} {y}Z", fill=c)
                                     for x, y, c in ((170, 130, PINK), (320, 220, YEL), (180, 320, GREEN))]
D["gujiya-plate"] = lambda s: (s.F("ellipse", cx=256, cy=330, rx=200, ry=70, fill=GOLD), [s.F("path", d=f"M{x - 70} {y} C{x - 70} {y - 70} {x + 70} {y - 70} {x + 70} {y}Z", fill="#E8B878")
                                                                                       for x, y in ((170, 320), (340, 320), (256, 290))])

# ---------------------------------------------------------------- indian festivals
D["rakhi"] = lambda s: (s.M("M40 256 H472", RED, 10), [s.F("ellipse", cx=256, cy=256, rx=40, ry=100, fill=c, transform=f"rotate({a} 256 256)") for a, c in zip(range(0, 180, 30), (ORANGE, YEL) * 3)],
                        s.F("circle", cx=256, cy=256, r=50, fill=RED), s.F("circle", cx=256, cy=256, r=24, fill=GOLD))
D["raksha-bandhan"] = lambda s: (s.T("M60 300 L330 260", SKIN, 70), s.F("path", d="M330 230 C380 220 420 240 430 270 C420 300 380 310 330 300Z", fill=SKIN),
                                 P(s, D["rakhi"], 220, 278, 0.45))
D["navratri"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#F9B57A"), [diya(s, x, 400, 0.25) for x in (110, 256, 402)],
                           P(s, person, 170, 260, 0.6, pose="cheer", shirt=PINK), P(s, person, 340, 260, 0.6, pose="cheer", shirt=GREEN))
D["dandiya-sticks"] = lambda s: (s.T("M140 420 L360 120", ORANGE, 22), s.T("M372 420 L152 120", PINK, 22), s.M("M180 360 L200 330 M330 360 L310 330", GOLD, 8))
D["garba-dance"] = lambda s: [P(s, person, x, 270, 0.55, pose="cheer", shirt=c) for x, c in ((120, PINK), (256, ORANGE), (392, GREEN))]
D["durga-puja-pandal"] = lambda s: (s.F("rect", x=60, y=200, width=392, height=260, rx=10, fill=RED), s.F("polygon", points="40,210 256,70 472,210", fill=GOLD),
                                    s.F("path", d="M180 460 V300 C180 250 332 250 332 300 V460Z", fill="#FFF1C2"), [diya(s, x, 430, 0.2) for x in (110, 402)])
D["pongal-pot"] = lambda s: (s.F("path", d="M150 200 C80 240 80 400 160 440 H352 C432 400 432 240 362 200Z", fill=K["tan"]), s.F("rect", x=170, y=170, width=172, height=40, rx=10, fill=K["brown"]),
                             s.F("path", d="M170 180 C200 110 312 110 342 180Z", fill=LIGHT), s.M("M150 300 C200 330 312 330 362 300", YEL, 12),
                             [s.F("ellipse", cx=x, cy=420, rx=14, ry=60, fill=GREEN, transform=f"rotate({(x - 256) // 4} {x} 460)") for x in (90, 422)])
D["pongal"] = lambda s: (s.F("circle", cx=256, cy=140, r=80, fill=YEL), P(s, D["pongal-pot"], 256, 340, 0.6))
D["makar-sankranti-kites"] = lambda s: [(s.F("polygon", points=f"{x},{y - 70} {x + 56},{y} {x},{y + 70} {x - 56},{y}", fill=c), s.M(f"M{x} {y - 70} V{y + 70} M{x - 56} {y} H{x + 56}", DARK, 4),
                                         s.M(f"M{x} {y + 70} C{x - 30} {y + 120} {x + 30} {y + 150} {x} {y + 200}", DARK, 3))
                                        for x, y, c in ((150, 140, PINK), (340, 110, YEL), (280, 280, GREEN))]
D["lohri-bonfire"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#2B2350"), [s.T(f"M{a} 440 L{b} 340", K["brown"], 22) for a, b in ((150, 300), (362, 212), (220, 256), (300, 256))],
                                P(s, lambda s: (s.F("path", d="M256 440 C150 440 120 330 180 270 C190 320 220 330 230 300 C210 240 240 180 280 150 C280 220 330 230 340 290 C400 330 360 440 256 440Z", fill=ORANGE),
                                                s.F("path", outline=False, d="M256 430 C200 430 190 370 220 340 C230 370 250 370 256 350 C270 380 300 380 300 400 C300 420 280 430 256 430Z", fill=YEL)), 256, 270, 0.8))
D["pookalam"] = lambda s: ([s.F("circle", cx=256, cy=256, r=r, fill=c) for r, c in ((200, ORANGE), (160, YEL), (120, RED), (80, "#F7E3C4"), (40, GREEN))],
                           [s.F("ellipse", outline=False, cx=256, cy=96, rx=20, ry=34, fill=PINK, transform=f"rotate({a} 256 256)") for a in range(0, 360, 30)])
D["onam"] = lambda s: (P(s, D["pookalam"], 220, 300, 0.75), s.F("path", d="M380 440 H460 L450 420 H390Z", fill=GOLD), s.T("M420 420 V200", GOLD, 14),
                       s.F("path", d="M370 200 H470 C470 230 370 230 370 200Z", fill=GOLD), s.F("path", d="M420 150 C436 170 434 188 420 196 C406 188 404 170 420 150Z", fill=ORANGE))
D["snake-boat-race"] = lambda s: (s.F("rect", outline=False, x=20, y=300, width=472, height=170, fill=BLUE), s.F("path", d="M30 300 C120 340 380 340 470 260 L470 200 C450 260 400 300 380 300 H40Z", fill=K["darkbrown"]),
                                  [P(s, person, x, 270, 0.18, shirt=WHITEK) for x in range(80, 400, 40)])
D["ganesh-chaturthi-decorations"] = lambda s: (s.M("M30 100 C150 180 362 180 482 100", DARK, 6), [s.F("circle", cx=x, cy=y, r=26, fill=c) for (x, y), c in zip(((90, 150), (180, 170), (256, 176), (332, 170), (422, 150)), (ORANGE, YEL) * 3)],
                                               [s.F("ellipse", cx=x, cy=330, rx=40, ry=60, fill=GREEN) for x in (110, 402)], s.F("rect", x=170, y=260, width=172, height=190, rx=10, fill=RED), s.F("path", d="M170 260 C170 200 342 200 342 260Z", fill=GOLD))
D["janmashtami-dahi-handi"] = lambda s: (s.M("M30 80 H482", DARK, 6), s.T("M256 80 V140", DARK, 6), s.F("path", d="M180 150 C120 190 130 300 200 320 H312 C382 300 392 190 332 150Z", fill=K["tan"]),
                                         s.F("rect", x=190, y=130, width=132, height=30, rx=8, fill=K["brown"]), [s.T(f"M{x} 250 V280", RED, 10) for x in (220, 256, 292)],
                                         [P(s, person, x, 400, 0.35, pose="cheer", shirt=c) for x, c in ((180, ORANGE), (256, BLUE), (332, ORANGE))])
D["baisakhi"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#FFE38A"), [s.T(f"M{x} 470 V{300 - (x % 3) * 30}", "#C89B3C", 10) for x in range(60, 460, 30)],
                           [s.F("ellipse", outline=False, cx=x, cy=290 - (x % 3) * 30, rx=10, ry=26, fill=GOLD) for x in range(60, 460, 30)], P(s, person, 256, 260, 0.55, pose="cheer", shirt=ORANGE))
D["chhath-puja"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#F9B57A"), s.F("circle", cx=256, cy=260, r=100, fill=ORANGE), s.F("rect", outline=False, x=20, y=300, width=472, height=172, fill=BLUE),
                              s.F("path", d="M150 380 C150 330 362 330 362 380Z", fill=K["tan"]), [diya(s, x, 360, 0.18) for x in (200, 256, 312)])
D["independence-day-india"] = lambda s: flag_pole(s, lambda s, x, y: flag_india(s, x, y))
D["republic-day-india"] = lambda s: (flag_pole(s, lambda s, x, y: flag_india(s, x, y), 120), [s.F("circle", cx=x, cy=420, r=r, fill=c) for x, r, c in ((350, 30, "#FF9933"), (410, 30, "#138808"), (380, 26, LIGHT))])

# ---------------------------------------------------------------- world festivals
def xmas_tree(s):
    s.F("rect", x=226, y=400, width=60, height=60, fill=K["brown"])
    for (w, y) in ((200, 400), (160, 300), (120, 200)):
        s.F("polygon", points=f"{256 - w},{y} {256 + w},{y} 256,{y - 140}", fill=K["darkgreen"])
    s.F("polygon", points=star_pts(256, 60, 34, 14, 5), fill=GOLD)
    for x, y, c in ((200, 360, RED), (300, 330, BLUE), (230, 260, YEL), (290, 200, RED), (250, 160, BLUE)):
        s.F("circle", cx=x, cy=y, r=12, fill=c)


D["christmas"] = xmas_tree
D["christmas-stockings"] = lambda s: (s.F("path", d="M180 80 H330 V300 C330 340 320 360 300 380 L240 430 C200 460 150 430 170 390 L200 340 C186 320 180 300 180 280Z", fill=RED),
                                      s.F("rect", x=170, y=70, width=170, height=60, rx=16, fill=LIGHT))
D["christmas-wreath"] = lambda s: (s.T("M256 90 A166 166 0 1 1 255.9 90", K["darkgreen"], 70), [s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=12, fill=RED) for x, y in (arc_pt(256, 256, 166, a) for a in range(0, 360, 40))],
                                   P(s, lambda s: (s.F("path", d="M256 256 C200 200 150 220 170 260 C190 300 240 280 256 256Z", fill=RED), s.F("path", d="M256 256 C312 200 362 220 342 260 C322 300 272 280 256 256Z", fill=RED)), 256, 420, 0.6))
D["christmas-bauble"] = lambda s: (s.T("M256 40 V110", DARK, 6), s.F("rect", x=226, y=100, width=60, height=40, rx=6, fill=GOLD), s.F("circle", cx=256, cy=290, r=160, fill=RED),
                                   s.M("M100 270 C180 310 332 310 412 270", GOLD, 12), s.F("ellipse", outline=False, cx=200, cy=220, rx=30, ry=50, fill="#F07A7E", transform="rotate(30 200 220)"))
D["candy-cane"] = lambda s: (s.T("M290 460 V180 C290 80 170 80 170 180", LIGHT, 56), [s.M(f"M266 {y} l48 -30", RED, 14) for y in range(200, 460, 50)], s.M("M180 150 l30 -20 M220 110 l20 30", RED, 14))
D["gingerbread-house"] = lambda s: (s.F("rect", x=120, y=240, width=272, height=210, fill="#C68A5C"), s.F("polygon", points="96,250 256,110 416,250", fill="#8E5A3A"),
                                    s.M("M110 240 C140 260 160 230 190 250 C220 260 240 230 270 250 C300 260 320 230 350 250 C370 260 390 240 402 245", LIGHT, 14),
                                    s.F("path", d="M226 450 V380 C226 350 286 350 286 380 V450Z", fill=RED), [s.F("circle", cx=x, cy=300, r=16, fill=c) for x, c in ((170, GREEN), (342, YEL))])
D["hanukkah"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#1E3A8A"), [s.F("rect", x=70 + i * 45, y=260, width=26, height=150, rx=6, fill=LIGHT) for i in range(9) if i != 4],
                           s.F("rect", x=244, y=220, width=26, height=190, rx=6, fill=LIGHT), [s.F("path", d=f"M{83 + i * 45} 220 C{97 + i * 45} 236 {95 + i * 45} 250 {83 + i * 45} 256 C{71 + i * 45} 250 {69 + i * 45} 236 {83 + i * 45} 220Z", fill=YEL) for i in range(9) if i != 4])
D["dreidel"] = lambda s: (s.T("M256 60 V140", K["brown"], 24), s.F("polygon", points="156,140 356,140 356,300 256,440 156,300", fill=BLUE), s.F("polygon", points="356,140 400,180 400,300 356,300", fill="#2C5FC9"))
D["lunar-new-year"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#B5323A"), [P(s, D["paper-lantern"], x, 220, 0.45) for x in (150, 362)], firework(s, 256, 380, 70, GOLD))


@reg("paper-lantern")
def _(s):
    s.T("M256 30 V80", DARK, 6)
    s.F("rect", x=200, y=70, width=112, height=30, rx=6, fill=GOLD)
    s.F("ellipse", cx=256, cy=250, rx=170, ry=160, fill=RED)
    s.M("M256 92 V408 M170 110 C120 200 120 300 170 390 M342 110 C392 200 392 300 342 390", "#8E2128", 8)
    s.F("rect", x=200, y=400, width=112, height=30, rx=6, fill=GOLD)
    s.M("M240 430 V480 M256 430 V490 M272 430 V480", GOLD, 6)


D["red-envelope"] = lambda s: (s.F("rect", x=140, y=80, width=232, height=352, rx=16, fill=RED), s.F("path", d="M140 96 C140 86 150 80 160 80 H352 C362 80 372 86 372 96 V160 C320 200 192 200 140 160Z", fill="#D63A3F"),
                               s.F("circle", cx=256, cy=200, r=40, fill=GOLD), s.F("rect", outline=False, x=246, y=190, width=20, height=20, fill="#D63A3F"))
D["dragon-dance"] = lambda s: (s.T("M60 300 C120 220 180 360 240 280 C300 200 340 320 380 270", RED, 70), s.M("M60 300 C120 220 180 360 240 280 C300 200 340 320 380 270", GOLD, 10),
                               s.F("path", d="M360 210 C420 180 480 220 476 270 C472 310 420 320 370 300 Z", fill=RED), s.F("circle", cx=440, cy=245, r=14, fill=LIGHT),
                               s.F("circle", outline=False, cx=444, cy=245, r=6, fill=DARK), s.F("polygon", points="400,200 420,150 440,205", fill=GOLD),
                               [s.T(f"M{x} {y + 30} V{y + 120}", DARK, 12) for x, y in ((110, 300), (230, 300), (340, 290))])
D["lion-dance"] = lambda s: (s.F("path", d="M140 200 C140 120 372 120 372 200 V320 C372 360 140 360 140 320Z", fill=RED), s.F("rect", x=170, y=320, width=172, height=60, rx=20, fill=GOLD),
                             [s.F("circle", cx=x, cy=220, r=34, fill=LIGHT) for x in (210, 302)], [s.F("circle", outline=False, cx=x, cy=226, r=14, fill=DARK) for x in (210, 302)],
                             s.T("M150 150 C100 100 120 60 170 90 M362 150 C412 100 392 60 342 90", GOLD, 14))
D["mid-autumn-festival"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#1E2A4A"), s.F("circle", cx=360, cy=140, r=70, fill="#FFE38A"),
                                      s.F("circle", cx=200, cy=330, r=110, fill="#C68A5C"), s.F("circle", cx=200, cy=330, r=76, fill="#E8B878"), [s.M(f"M{200 + dx} 270 V390", "#C68A5C", 6) for dx in (-30, 0, 30)])
D["easter-eggs"] = lambda s: [(s.F("ellipse", cx=x, cy=y, rx=70, ry=92, fill=c), s.M(f"M{x - 66} {y} C{x - 30} {y - 20} {x + 30} {y + 20} {x + 66} {y}", LIGHT, 10))
                              for x, y, c in ((150, 300, PINK), (260, 250, YEL), (370, 310, BLUE))]
D["halloween-pumpkin"] = lambda s: (s.T("M256 120 C256 90 270 70 290 60", "#4CB963", 18), s.F("ellipse", cx=256, cy=290, rx=190, ry=150, fill=ORANGE),
                                    s.M("M180 160 C150 230 150 350 180 430 M332 160 C362 230 362 350 332 430", "#D97A2B", 10),
                                    s.F("polygon", outline=False, points="180,250 230,250 205,210", fill=DARK), s.F("polygon", outline=False, points="282,250 332,250 307,210", fill=DARK),
                                    s.F("path", outline=False, d="M170 320 L200 340 L230 320 L256 340 L282 320 L312 340 L342 320 C320 380 192 380 170 320Z", fill=DARK))
D["thanksgiving"] = lambda s: (s.F("ellipse", cx=256, cy=380, rx=210, ry=50, fill=MID), s.F("ellipse", cx=256, cy=300, rx=160, ry=100, fill="#C68A5C"),
                               [s.T(f"M{x} {y} L{x + d} {y + 50}", "#F7E3C4", 22) for x, y, d in ((120, 230, -40), (392, 230, 40))])
D["day-of-the-dead"] = lambda s: ([s.F("ellipse", cx=256, cy=120 + k * 30, rx=40, ry=90, fill=c, transform=f"rotate({a} 256 256)") for a, c, k in zip(range(0, 360, 45), (ORANGE, PINK) * 4, [0] * 8)],
                                  s.F("circle", cx=256, cy=256, r=90, fill=YEL), s.F("circle", cx=256, cy=256, r=40, fill=ORANGE))
D["carnival-mask"] = lambda s: (s.F("path", d="M60 220 C60 170 140 160 256 200 C372 160 452 170 452 220 C452 300 380 330 300 290 C280 280 270 270 256 270 C242 270 232 280 212 290 C132 330 60 300 60 220Z", fill=PURPLE),
                                s.F("ellipse", outline=False, cx=170, cy=240, rx=50, ry=28, fill=DARK), s.F("ellipse", outline=False, cx=342, cy=240, rx=50, ry=28, fill=DARK),
                                s.T("M420 190 C450 120 430 80 400 60", GOLD, 12), [s.F("polygon", points=star_pts(x, 190, 14, 6, 5), fill=GOLD) for x in (120, 392)])
D["nowruz"] = lambda s: (P(s, sprout, 256, 300, 0.9), [s.F("ellipse", cx=x, cy=420, rx=30, ry=38, fill=c) for x, c in ((110, RED), (402, BLUE))])
D["haft-seen-table"] = lambda s: (s.F("rect", x=40, y=320, width=432, height=40, rx=8, fill=K["brown"]), P(s, sprout, 120, 250, 0.4, pot=False), s.F("circle", cx=120, cy=300, r=30, fill="#4CB963"),
                                  s.F("circle", cx=210, cy=290, r=34, fill=RED), [s.F("ellipse", cx=300, cy=290, rx=22, ry=30, fill=c) for c in (YEL,)], s.F("rect", x=350, y=200, width=90, height=120, rx=8, fill="#D9EEFB"),
                                  s.F("rect", outline=False, x=360, y=260, width=70, height=56, fill="#8FD0FF"), s.F("ellipse", outline=False, cx=395, cy=280, rx=16, ry=8, fill=ORANGE))
D["songkran"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#8FD0FF"), P(s, person, 160, 290, 0.5, pose="cheer", shirt=YEL), P(s, person, 352, 290, 0.5, pose="cheer", shirt=PINK),
                           [s.F("circle", outline=False, cx=x, cy=y, r=8, fill="#3D8BFD") for x, y in ((240, 120), (260, 160), (280, 110), (230, 180), (300, 150))])
D["oktoberfest"] = lambda s: (s.T("M150 300 C90 230 140 130 220 170 C280 200 300 300 256 340 C212 300 232 200 292 170 C372 130 422 230 362 300 C320 350 192 350 150 300Z", "#C68A5C", 42),
                              [s.F("ellipse", outline=False, cx=x, cy=y, rx=6, ry=4, fill=LIGHT) for x, y in ((140, 250), (200, 180), (300, 180), (370, 250), (256, 320), (190, 320), (330, 320))])

# ---------------------------------------------------------------- new year, birthday
D["new-year"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#1E2A4A"), firework(s, 160, 170, 100, A2), firework(s, 360, 230, 110, A1), confetti_bits(s, 16, 9, (40, 330, 470, 460)))
D["new-year-countdown"] = lambda s: (P(s, clock, 256, 256, 1.0, h=0, m=58))
D["midnight-fireworks"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#14203A"), firework(s, 256, 200, 140, A2, 16), firework(s, 120, 330, 60, A1), firework(s, 400, 330, 60, "#4CB963"),
                                     s.F("polygon", outline=False, points="20,472 20,420 80,420 80,380 130,380 130,430 200,430 200,400 260,400 260,440 330,440 330,390 380,390 380,420 492,420 492,472", fill=DARK))
D["new-year-resolutions"] = lambda s: (P(s, checklist, 230, 270, 0.9, done=1), P(s, star, 400, 110, 0.2))
D["birthday"] = lambda s: (cake(s, 2, candles=3), confetti_bits(s, 10, 5, (40, 40, 470, 120)))
D["birthday-candles"] = lambda s: [(s.F("rect", x=x - 18, y=200, width=36, height=230, rx=8, fill=c), s.M(f"M{x - 18} 250 l36 -20 M{x - 18} 320 l36 -20 M{x - 18} 390 l36 -20", LIGHT, 8),
                                    s.F("path", d=f"M{x} 120 C{x + 26} 150 {x + 22} 180 {x} 190 C{x - 22} 180 {x - 26} 150 {x} 120Z", fill=K["orange"])) for x, c in ((150, A1), (256, A2), (362, "#4CB963"))]
D["birthday-party"] = lambda s: (P(s, D["bunting"], 256, 140, 0.9), P(s, cake, 256, 330, 0.6), P(s, person, 90, 330, 0.4, pose="cheer", shirt=A2), P(s, person, 422, 330, 0.4, pose="cheer"))
D["birthday-gift"] = lambda s: (P(s, gift, 256, 300, 0.9), balloon(s, A1, A1L, 400, 110, 60))
D["number-candles"] = lambda s: (stroke_text(s, "1", 180, 280, 220, A1, 40), stroke_text(s, "0", 330, 280, 220, A2, 40),
                                 [s.F("path", d=f"M{x} 90 C{x + 20} 112 {x + 18} 136 {x} 144 C{x - 18} 136 {x - 20} 112 {x} 90Z", fill=K["orange"]) for x in (180, 330)])

# ---------------------------------------------------------------- weddings
def couple(s):
    # faceless bride and groom silhouettes
    s.F("path", d="M120 460 C130 330 160 260 196 240 C232 260 262 330 272 460Z", fill=LIGHT)
    s.F("circle", cx=196, cy=190, r=42, fill=SKIN)
    s.F("path", d="M150 200 C140 120 252 110 244 200 C250 260 230 300 196 300 C170 300 146 260 150 200Z", fill=A2L)
    s.F("circle", cx=196, cy=196, r=38, fill=SKIN)
    s.F("path", d="M268 460 V280 C268 250 290 236 320 236 C350 236 372 250 372 280 V460Z", fill=DARK)
    s.F("polygon", points="306,240 334,240 320,300", fill=LIGHT)
    s.F("circle", cx=320, cy=190, r=40, fill=SKIN)
    s.F("path", d="M280 180 C280 140 360 140 360 180 C340 166 300 166 280 180Z", fill="#4A3B32")


D["bride-and-groom-silhouettes"] = couple
D["wedding"] = lambda s: (couple(s), P(s, heart, 256, 80, 0.2, color=A2))
D["nikah"] = lambda s: (P(s, D["nikah-certificate"], 256, 220, 0.7), ring(s, 180, 400, 50), ring(s, 300, 400, 50, color=MID))
D["nikah-certificate"] = lambda s: (s.F("rect", x=100, y=80, width=312, height=360, rx=16, fill="#FFF8E7"), s.F("rect", x=124, y=104, width=264, height=312, rx=10, fill="none"),
                                    s.raw(f'<rect x="124" y="104" width="264" height="312" rx="10" fill="none" stroke="{GOLD}" stroke-width="8"/>'),
                                    s.M("M160 200 H352 M160 250 H352 M160 300 H300", MID, 12), crescent(s, 256, 150, 22, GOLD), s.F("circle", cx=330, cy=370, r=28, fill=RED))
D["wedding-rings"] = lambda s: (ring(s, 200, 300, 110), ring(s, 320, 300, 110, color=MID))
D["engagement-ring"] = lambda s: ring(s, 256, 320, 130, stone=A1L)
D["wedding-cake"] = lambda s: (s.F("rect", x=96, y=350, width=320, height=100, rx=12, fill=LIGHT), s.F("rect", x=136, y=250, width=240, height=100, rx=12, fill=LIGHT),
                               s.F("rect", x=176, y=160, width=160, height=90, rx=12, fill=LIGHT), [s.M(f"M{x} {y} H{x + w}", A2L, 12) for x, y, w in ((96, 380, 320), (136, 280, 240), (176, 190, 160))],
                               P(s, heart, 256, 120, 0.15, color=A2))
D["wedding-invitation"] = lambda s: (D["invitation-card"](s), ring(s, 256, 250, 24))
D["mehndi"] = lambda s: (P(s, lambda s: s.F("path", d="M-40 80 C-60 40 -66 0 -60 -30 C-56 -46 -36 -44 -36 -26 V-70 C-36 -84 -16 -84 -16 -70 V-86 C-16 -100 4 -100 4 -86 V-78 C4 -92 24 -92 24 -78 V-60 C24 -72 44 -72 44 -60 V10 C44 40 30 70 20 80 Z",
                                                                        fill=SKIN, transform="translate(256 256) scale(2.4)"), 256, 256, 1.0),
                                                     s.M("M230 300 C250 280 270 280 290 300 M240 250 C256 240 272 240 280 260 M256 330 V360 M200 180 C210 170 220 170 230 180 M300 170 C310 160 320 160 330 170", "#9C4A2A", 8),
                                                     s.F("circle", outline=False, cx=262, cy=290, r=14, fill="#9C4A2A"))
D["mehndi-hands"] = lambda s: (P(s, D["mehndi"], 180, 256, 0.75), P(s, D["mehndi"], 332, 256, 0.75, flip=True))
D["wedding-stage"] = lambda s: (s.F("rect", x=40, y=330, width=432, height=80, rx=8, fill=A2), s.F("path", d="M60 330 V140 C60 80 452 80 452 140 V330 H400 V160 C400 120 112 120 112 160 V330Z", fill=A1),
                                [s.F("circle", cx=x, cy=330, r=24, fill=A2L) for x in (80, 432)], s.F("rect", x=170, y=260, width=172, height=70, rx=16, fill=LIGHT))
D["wedding-garland"] = lambda s: [s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=20, fill=(K["red"], K["orange"], WHITEK)[i % 3]) for i, (x, y) in enumerate(arc_pt(256, 160, 190, a) for a in range(10, 171, 8))]
D["wedding-flowers"] = lambda s: ([s.T(f"M256 460 L{x} 240", "#2F8A4A", 8) for x in (180, 256, 332)], [s.F("circle", cx=x, cy=y, r=46, fill=c) for x, y, c in ((180, 220, K["pink"]), (256, 170, WHITEK), (332, 220, K["pink"]))],
                                  s.F("path", d="M196 380 H316 L296 460 H216Z", fill=A1L))

# ---------------------------------------------------------------- national days and occasions
D["national-day"] = lambda s: (flag_pole(s, lambda s, x, y: (s.F("rect", x=x, y=y, width=260, height=160, fill=A1), P(s, star, x + 130, y + 80, 0.25, color=LIGHT))), firework(s, 400, 340, 60, A2))
D["independence-day"] = lambda s: (flag_pole(s, lambda s, x, y: (s.F("rect", x=x, y=y, width=260, height=160, fill=A2), P(s, star, x + 130, y + 80, 0.25, color=LIGHT))), firework(s, 390, 360, 60, A1))
D["flag-hoisting"] = lambda s: (flag_pole(s, lambda s, x, y: s.F("rect", x=x, y=y, width=200, height=130, fill=A1), 300), P(s, person, 160, 300, 0.6, pose="point"))
D["national-anthem"] = lambda s: (P(s, person, 200, 280, 0.75, pose="think"), s.M("M340 150 V250 M340 150 L400 130 V230", A1, 14), s.F("ellipse", cx=325, cy=252, rx=20, ry=14, fill=A1), s.F("ellipse", cx=385, cy=232, rx=20, ry=14, fill=A1))
D["parade"] = lambda s: [P(s, person, x, 300, 0.45, pose="walk", shirt=c) for x, c in ((90, A1), (200, A2), (310, A1), (420, A2))] + [P(s, flag, 200, 120, 0.3)]
D["uae-national-day"] = lambda s: (flag_pole(s, lambda s, x, y: flag_uae(s, x, y)), firework(s, 400, 360, 60, GOLD))


@reg("saudi-national-day")
def _(s):
    s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#006C35")
    s.T("M256 330 C250 260 256 200 262 150", K["brown"], 22)
    for a in (-160, -125, -90, -55, -20):
        x, y = arc_pt(262, 150, 90, a)
        s.F("ellipse", cx=f"{(262 + x) / 2:.0f}", cy=f"{(150 + y) / 2:.0f}", rx=52, ry=16, fill="#4CB963", transform=f"rotate({a} {(262 + x) / 2:.0f} {(150 + y) / 2:.0f})")
    for k in (1, -1):
        s.T(f"M{256 - 140 * k} 420 C{256 - 60 * k} 380 {256 + 40 * k} 350 {256 + 140 * k} 330", K["white"], 16)
        s.F("rect", x=256 - 150 * k - 14, y=408, width=28, height=28, rx=6, fill=GOLD)


D["mothers-day"] = lambda s: (P(s, heart, 256, 240, 0.8, color=K["pink"]), P(s, sprout, 256, 380, 0.35, pot=False))
D["fathers-day"] = lambda s: (s.F("path", d="M150 120 H362 L330 200 L256 160 L182 200Z", fill=LIGHT), s.F("polygon", points="236,170 276,170 296,420 256,460 216,420", fill=A1),
                              s.F("rect", x=232, y=150, width=48, height=40, rx=8, fill=A1D))
D["teachers-day"] = lambda s: (P(s, book, 200, 330, 0.55), P(s, D["ribbon-bow"], 360, 170, 0.35), s.F("rect", x=300, y=260, width=140, height=90, rx=10, fill="#2F8A4A"))
D["childrens-day"] = lambda s: (P(s, person, 170, 300, 0.5, pose="cheer", shirt=A2), P(s, person, 340, 300, 0.5, pose="cheer"), balloon(s, A1, A1L, 256, 110, 60))
D["valentines-day"] = lambda s: (P(s, heart, 230, 270, 0.75, color=K["red"]), P(s, heart, 380, 140, 0.3, color=K["pink"]))
D["womens-day"] = lambda s: (s.T("M256 300 V460 M190 390 H322", K["purple"], 30), s.T("M256 80 A110 110 0 1 1 255.9 80", K["purple"], 30))
D["graduation-day"] = lambda s: (s.F("polygon", points="256,110 470,200 256,290 42,200", fill=DARK), s.F("path", d="M140 250 V330 C140 370 372 370 372 330 V250 L256 300Z", fill=DARK),
                                 s.T("M440 210 V320", A2, 8), s.F("circle", cx=440, cy=330, r=14, fill=A2))
D["anniversary"] = lambda s: (ring(s, 200, 320, 90), ring(s, 312, 320, 90, color=MID), P(s, heart, 256, 110, 0.25, color=A2))


if __name__ == "__main__":
    run("celebrations-holidays", D, sys.argv[1:] or None)
