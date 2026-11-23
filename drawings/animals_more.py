"""animals drawings, part 2: reptiles, amphibians, bugs, worms, dinosaurs and extinct animals,
animal homes and body parts. Run: python drawings/animals_more.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, bird, bug, fish, butterfly_wings, eye, lizard, quad, shade, snake, tint, turtle  # noqa: E402
from draw_lib import C, INK, arc_pt, run, star_pts  # noqa: E402

D = {}
BROWN, DBROWN, TAN, CREAM, GREY, DGREY = C["brown"], C["darkbrown"], C["tan"], C["cream"], C["grey"], C["darkgrey"]
PINK, ORANGE, YEL, GREEN, DGREEN, RED, BLUE = C["pink"], C["orange"], C["yellow"], C["green"], C["darkgreen"], C["red"], C["blue"]


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def fitted(scale, fn, cx=256, cy=256):
    def draw(s):
        s.open(transform=f"translate({cx} {cy}) scale({scale}) translate(-256 -256)")
        fn(s)
        s.close()
    return draw


# ---------------------------------------------------------------- reptiles
def croc(s, body="#5E7A3A", belly="#C9C38A", snout="normal"):
    s.T("M200 330 C120 330 70 350 30 380", body, 40)
    for x in (170, 330):
        s.T(f"M{x} 350 L{x - 20} 410 L{x + 20} 414", shade(body, 0.85), 22)
    s.F("ellipse", cx=250, cy=320, rx=140, ry=48, fill=body)
    s.F("ellipse", outline=False, cx=250, cy=345, rx=120, ry=18, fill=belly)
    for x in range(140, 360, 26):
        s.F("polygon", outline=False, points=f"{x - 10},282 {x},264 {x + 10},282", fill=shade(body, 0.75))
    if snout == "thin":
        s.F("rect", x=360, y=300, width=140, height=22, rx=10, fill=body)
        s.F("ellipse", cx=380, cy=304, rx=40, ry=26, fill=body)
    else:
        w = 150 if snout == "normal" else 130
        s.F("path", d=f"M350 296 C380 280 {350 + w} 288 {360 + w} 306 C{350 + w} 330 380 338 350 334Z", fill=body)
        for x in range(380, 350 + w, 16):
            s.F("polygon", outline=False, points=f"{x},322 {x + 6},334 {x + 12},322", fill=WHITE)
    s.F("circle", cx=380, cy=286, r=16, fill=body)
    eye(s, 382, 282, 6)
    for x in (170, 330):
        s.T(f"M{x} 340 L{x + 20} 410 L{x + 50} 414", body, 22)


D["king-cobra"] = lambda s: snake(s, body="#6E6A3A", belly=CREAM, hood=True)
D["python"] = lambda s: snake(s, body="#B08A50", pattern="#5E4A2E")
D["anaconda"] = lambda s: snake(s, body="#5E6A3A", pattern="#2E2A1E")
D["rattlesnake"] = lambda s: (snake(s, body="#C9A27A", pattern="#6E5A4A"), s.F("ellipse", cx=80, cy=404, rx=18, ry=12, fill="#E8DCC8"), s.F("ellipse", cx=62, cy=410, rx=14, ry=10, fill="#E8DCC8"))
D["viper"] = lambda s: snake(s, body="#8C7A5A", pattern="#3A2E28")
D["green-tree-snake"] = lambda s: (s.T("M40 160 H472", BROWN, 28), snake(s, body="#4CB963"))
D["sea-snake"] = lambda s: (s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="#BFE6FA"), snake(s, body="#3A6A9A", pattern=WHITE))
D["crocodile"] = lambda s: croc(s)
D["saltwater-crocodile"] = lambda s: croc(s, body="#6E7A4A", belly="#D9D2A0")
D["alligator"] = lambda s: croc(s, body="#3E5A3A", belly="#B9B88A", snout="short")
D["gharial"] = lambda s: croc(s, body="#6E7A5A", belly="#D9D6B0", snout="thin")
D["gecko"] = lambda s: lizard(s, body="#E8C74A", spots=ORANGE)
D["iguana"] = lambda s: lizard(s, body="#5EA84A", crest=True, belly="#A8D88A")
D["chameleon"] = lambda s: (lizard(s, body="#4CB963", crest=True, belly="#9BD7A8"), s.T("M120 340 C60 360 50 420 90 430 C120 436 120 400 100 400", "#4CB963", 24))
D["komodo-dragon"] = lambda s: lizard(s, body="#7A6A5A", belly="#A09080")
D["monitor-lizard"] = lambda s: lizard(s, body="#5A5A4A", spots="#C9C38A")
D["frilled-lizard"] = lambda s: lizard(s, body="#B08A50", frill="#E8782B")
D["gila-monster"] = lambda s: lizard(s, body="#E8782B", spots="#2E2A3B")
D["sea-turtle"] = lambda s: (s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="#BFE6FA"), turtle(s, shell="#7A8A4A", skin="#A8B87A", sea=True))
D["tortoise"] = lambda s: turtle(s, shell="#8C6A3A", skin="#A89A7A")
D["giant-tortoise"] = lambda s: fitted(1.0, lambda s: turtle(s, shell="#5E4A3A", skin="#8C8A7A"))(s)
D["tuatara"] = lambda s: lizard(s, body="#6E7A5A", crest=True)


# ---------------------------------------------------------------- amphibians
def frog(s, body="#4CB963", belly="#C8E8A8", spots=None, eye_c=BLACK, toad=False):
    for sgn in (1, -1):
        s.F("ellipse", cx=256 + sgn * 120, cy=400, rx=70, ry=36, fill=shade(body, 0.85))
        s.F("ellipse", cx=256 + sgn * 170, cy=436, rx=50, ry=14, fill=shade(body, 0.85))
    s.F("ellipse", cx=256, cy=330, rx=150, ry=110, fill=body)
    s.F("ellipse", outline=False, cx=256, cy=370, rx=100, ry=60, fill=belly)
    if spots:
        for x, y in ((180, 270), (330, 270), (230, 300), (300, 310)):
            s.F("circle", outline=False, cx=x, cy=y, r=16, fill=spots)
    if toad:
        for x, y in ((170, 300), (340, 300), (256, 260), (210, 330), (310, 330)):
            s.F("circle", outline=False, cx=x, cy=y, r=9, fill=shade(body, 0.75))
    for sgn in (1, -1):
        s.T(f"M{256 + sgn * 60} 380 L{256 + sgn * 70} 440", shade(body, 0.85), 22)
    for x, side in ((190, "left"), (322, "right")):
        s.F("circle", cx=x, cy=220, r=44, fill=body)
        s.F("circle", outline=False, cx=x, cy=220, r=28, fill=WHITE)
        eye(s, x, 220, 16, side, eye_c)
    s.M("M190 320 Q256 350 322 320", INK, 6)


D["frog"] = lambda s: frog(s)
D["toad"] = lambda s: frog(s, body="#8C7A4A", belly="#C9B88A", toad=True)
D["tadpole"] = lambda s: (s.T("M120 300 C180 260 200 340 250 280", "#3A3A44", 26), s.F("ellipse", cx=320, cy=270, rx=90, ry=70, fill="#3A3A44"), eye(s, 360, 250, 10))
D["tree-frog"] = lambda s: (s.T("M30 470 C200 440 320 460 482 430", BROWN, 26), frog(s, body="#5EC84A", belly="#E8F0A8", eye_c=RED))
D["poison-dart-frog"] = lambda s: frog(s, body="#2C8FE8", belly="#1E5FB4", spots="#1F1F24")
D["bullfrog"] = lambda s: frog(s, body="#6E8A3A", belly="#E8E0B0", spots="#4A5A2A")
D["salamander"] = lambda s: lizard(s, body="#2E2A3B", spots=YEL)
D["newt"] = lambda s: lizard(s, body="#B07A3A", belly=ORANGE)
D["axolotl"] = lambda s: (lizard(s, body="#F7A1B5", belly="#FCD0DC"), [s.T(f"M400 270 L{x} {y}", "#E8607A", 8) for x, y in ((380, 220), (410, 214), (440, 222))],
                          [s.T(f"M440 300 L{x} {y}", "#E8607A", 8) for x, y in ((470, 260), (480, 290))])
D["caecilian"] = lambda s: (s.T("M60 340 C140 260 220 400 300 320 C360 260 410 300 450 280", "#6E5A6A", 46), s.M("M80 330 C150 270 220 390 300 310", "#5A4A5A", 4, dash="6 12"), eye(s, 440, 274, 5))


# ---------------------------------------------------------------- insects
D["insect"] = lambda s: bug(s, body="#5A6A3A", wings="clear")
D["ant"] = lambda s: bug(s, body="#3A2E28", length=0.9)
D["fire-ant"] = lambda s: bug(s, body="#C1442E", length=0.9)
D["bumblebee"] = lambda s: bug(s, body="#2E2A3B", head_c="#2E2A3B", wings="clear", stripes=YEL, length=1.1)
D["wasp"] = lambda s: bug(s, body=YEL, head_c="#2E2A3B", wings="clear", stripes="#2E2A3B", stinger=True, length=0.85)
D["hornet"] = lambda s: bug(s, body="#E8A030", head_c="#8E3E1E", wings="clear", stripes="#5E2E1E", stinger=True)
D["monarch-butterfly"] = lambda s: butterfly_wings(s, "#E8782B", "#E8782B", spots=WHITE)
D["moth"] = lambda s: butterfly_wings(s, "#B7A898", "#9A8A7A", spots="#6E5A4A", body="#6E5A4A")


@reg("caterpillar")
def _(s):
    for i in range(7):
        x = 110 + i * 46
        y = 330 + (24 if i % 2 else 0)
        s.F("circle", cx=x, cy=y, r=40, fill="#7DC84A" if i % 2 else "#5EB83A")
        s.T(f"M{x} {y + 36} V{y + 56}", "#3A6A2A", 8)
    s.F("circle", cx=420, cy=300, r=52, fill="#5EB83A")
    s.T("M400 254 L390 220 M430 252 L440 218", "#3A3A44", 6)
    eye(s, 436, 292, 9)
    s.M("M420 324 Q440 334 456 322", INK, 5)


D["cocoon"] = lambda s: (s.T("M256 40 V100", BROWN, 10), s.F("path", d="M256 100 C330 120 340 260 300 380 C280 430 232 430 212 380 C172 260 182 120 256 100Z", fill="#B7A878"),
                         s.M("M200 200 C240 210 280 210 320 200 M196 270 C240 280 280 280 318 270 M210 340 C240 350 280 350 304 340", "#8C7A50", 6))
D["beetle"] = lambda s: bug(s, body="#2E2A3B", wings="beetle", wing_c="#3A6A5A")
D["dung-beetle"] = lambda s: (s.F("circle", cx=130, cy=360, r=90, fill="#8C6A3A"), fitted(0.6, lambda s: bug(s, body="#2E2A3B", wings="beetle", wing_c="#3A3A44"), 340, 320)(s))
D["stag-beetle"] = lambda s: (bug(s, body="#4A2E1E", wings="beetle", wing_c="#6E3E22"), s.T("M236 170 C200 120 210 80 236 60 M276 170 C312 120 302 80 276 60", "#4A2E1E", 14))
D["rhinoceros-beetle"] = lambda s: (bug(s, body="#3A2E22", wings="beetle", wing_c="#5E3E22"), s.T("M256 170 C256 110 240 70 220 50", "#3A2E22", 18))
D["firefly"] = lambda s: (s.F("circle", outline=False, cx=256, cy=380, r=90, fill="#FFF3A0"), bug(s, body="#3A3A44", wings="clear", stripes=YEL))
D["dragonfly"] = lambda s: bug(s, body="#2C8FE8", wings="dragonfly", length=1.25)
D["damselfly"] = lambda s: bug(s, body="#5EC8C0", wings="dragonfly", length=1.1)


def side_bug(s, body="#7DC84A", legs_long=False, wings=None, antenna_long=True, length=1.0, raptor=False, stick=False):
    """Side view grasshopper-like insect."""
    if stick:
        s.T("M60 300 H460", body, 18)
        for x in (160, 260, 360):
            s.T(f"M{x} 300 L{x - 40} 380 M{x} 300 L{x + 30} 230", body, 6)
        s.T("M460 300 L500 260", body, 6)
        eye(s, 450, 294, 5)
        return
    if legs_long:
        s.T("M240 300 L180 200 L120 420", shade(body, 0.85), 14)
    s.F("ellipse", cx=250, cy=300, rx=170 * length, ry=44, fill=body)
    if wings:
        s.F("path", d=f"M150 270 C220 250 340 250 380 280 C320 300 220 300 150 290Z", fill=wings)
    s.F("ellipse", cx=420, cy=282, rx=46, ry=40, fill=body)
    if legs_long:
        s.T("M260 310 L200 210 L140 430", body, 16)
    s.T("M360 320 L380 400 M320 320 L320 404", shade(body, 0.85), 8)
    if raptor:
        s.T("M390 300 L410 360 L450 330", body, 12)
    if antenna_long:
        s.M("M430 250 C440 160 470 120 500 100 M440 252 C460 170 490 140 510 130", shade(body, 0.7), 4)
    eye(s, 436, 274, 8)


D["grasshopper"] = lambda s: side_bug(s, legs_long=True, wings="#5EA83A")
D["cricket-insect"] = lambda s: side_bug(s, body="#5E4A2E", legs_long=True, wings="#3A2E1E")
D["locust"] = lambda s: side_bug(s, body="#C9A24A", legs_long=True, wings="#A08030")
D["praying-mantis"] = lambda s: side_bug(s, body="#8CC84A", raptor=True, antenna_long=False, length=1.1)
D["stick-insect"] = lambda s: side_bug(s, body="#8C7A4A", stick=True)
D["leaf-insect"] = lambda s: (s.F("path", d="M80 300 C160 200 360 200 440 300 C360 400 160 400 80 300Z", fill="#6EB84A"), s.M("M80 300 H440 M200 300 L160 250 M280 300 L250 240 M200 300 L170 350 M280 300 L250 360", "#4A8A2A", 6),
                              eye(s, 430, 290, 6))
D["cockroach"] = lambda s: bug(s, body="#6E3E22", wings="beetle", wing_c="#8C5A32")
D["termite"] = lambda s: bug(s, body="#E8DCC8", head_c="#C9A27A", length=0.9)
D["fly"] = lambda s: bug(s, body="#3A3A44", wings="clear", wing_c="#D9EEFB", length=0.85)
D["mosquito"] = lambda s: (bug(s, body="#5A5A66", wings="clear", length=0.7), s.T("M256 140 V60", "#5A5A66", 5))
D["flea"] = lambda s: side_bug(s, body="#6E3E22", legs_long=True, antenna_long=False, length=0.6)
D["louse"] = lambda s: bug(s, body="#C9B79A", length=0.8)
D["bed-bug"] = lambda s: bug(s, body="#8E3E1E", length=0.9)
D["cicada"] = lambda s: bug(s, body="#4A5A3A", wings="clear", wing_c="#D9EEFB", length=1.0)
D["water-strider"] = lambda s: (s.F("rect", outline=False, x=0, y=300, width=512, height=212, fill="#BFE6FA"), s.T("M256 280 L60 320 M256 280 L460 320 M256 280 L120 220 M256 280 L400 220", "#3A3A44", 6),
                                s.F("ellipse", cx=256, cy=280, rx=60, ry=16, fill="#3A3A44"))
D["silkworm"] = lambda s: (D["caterpillar"](s))

# ---------------------------------------------------------------- spiders and other bugs
D["spider"] = lambda s: bug(s, body="#2E2A3B", legs=8, antennae=None)
D["tarantula"] = lambda s: bug(s, body="#5E3E22", legs=8, antennae=None, length=1.15)
D["black-widow-spider"] = lambda s: (bug(s, body="#1F1F24", legs=8, antennae=None), s.F("polygon", points="246,330 266,330 256,350 266,370 246,370 256,350", fill=RED))
D["jumping-spider"] = lambda s: (bug(s, body="#3A3A44", legs=8, antennae=None, length=0.9), s.F("circle", cx=240, cy=190, r=12, fill=BLACK), s.F("circle", cx=272, cy=190, r=12, fill=BLACK))


@reg("spider-web")
def _(s):
    for a in range(0, 360, 30):
        x, y = arc_pt(256, 256, 220, a)
        s.M(f"M256 256 L{x:.0f} {y:.0f}", "#9AA3AF", 4)
    for r in (50, 100, 150, 200):
        pts = [arc_pt(256, 256, r, a) for a in range(0, 361, 30)]
        s.M("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts), "#9AA3AF", 4)
    s.F("circle", cx=330, cy=200, r=18, fill="#2E2A3B")


D["scorpion"] = lambda s: (s.T("M150 320 C80 300 70 200 120 150 C150 120 190 140 170 170", "#8C6A3A", 26), s.F("polygon", points="160,160 190,150 176,190", fill="#5E4A2E"),
                           [s.T(f"M{x} 330 L{x - 20} 390 M{x} 330 L{x + 10} 394", "#6E5A3A", 8) for x in (210, 250, 290, 330)],
                           s.F("ellipse", cx=270, cy=320, rx=110, ry=40, fill="#8C6A3A"), [s.T(f"M370 {y} L430 {y - 20}", "#8C6A3A", 14) for y in (300, 340)],
                           [s.F("path", d=f"M430 {y - 40} C470 {y - 50} 480 {y - 10} 460 {y} L440 {y - 14} Z", fill="#8C6A3A") for y in (300, 340)], eye(s, 370, 304, 6))
D["centipede"] = lambda s: ([s.T(f"M{x} {300 + (i % 2) * 10} l-10 -40 M{x} {300 + (i % 2) * 10} l-10 40", "#8E3E1E", 5) for i, x in enumerate(range(80, 440, 30))],
                            s.T("M70 310 C150 280 230 340 310 300 C370 270 410 300 440 290", "#C1662E", 34), eye(s, 440, 284, 6))
D["millipede"] = lambda s: ([s.T(f"M{x} 330 l0 30", "#3A2E28", 4) for x in range(90, 440, 12)], s.T("M80 320 C160 300 260 330 340 310 C390 300 420 310 440 300", "#4A3B32", 40), eye(s, 440, 294, 6))
D["tick-animal"] = lambda s: bug(s, body="#6E3E22", legs=8, antennae=None, length=0.85)
D["mite"] = lambda s: bug(s, body="#C1442E", legs=8, antennae=None, length=0.7)
D["woodlouse"] = lambda s: (s.F("ellipse", cx=256, cy=300, rx=170, ry=90, fill="#7A8290"), [s.M(f"M{x} 220 V380", "#5A6270", 8) for x in range(150, 380, 32)], eye(s, 410, 280, 7))

# ---------------------------------------------------------------- worms and molluscs
D["earthworm"] = lambda s: (s.T("M80 360 C140 260 220 380 300 300 C360 240 410 280 440 250", "#E89A8A", 40), s.M("M260 330 l14 -14 M280 314 l14 -14", "#C97A6A", 6), eye(s, 436, 244, 5))
D["leech"] = lambda s: (s.T("M100 340 C180 280 300 360 420 290", "#3A3A2E", 44), s.M("M120 330 C180 290 300 350 400 300", "#8C8A5A", 6, dash="12 12"))


@reg("snail")
def _(s):
    s.F("path", d="M60 420 C120 400 200 400 280 400 C340 360 380 330 400 290 C420 260 450 260 460 290 C470 330 440 400 420 430 Z", fill="#C9B79A")
    s.T("M410 290 L400 220 M430 290 L440 222", "#C9B79A", 10)
    s.F("circle", cx=230, cy=300, r=110, fill="#C1662E")
    s.M("M230 300 C230 260 280 260 280 300 C280 350 200 350 200 300 C200 230 310 230 310 300 C310 380 170 380 170 300", "#8E3E1E", 10)
    eye(s, 400, 214, 7, "left")
    eye(s, 442, 216, 7, "right")


D["slug"] = lambda s: (s.F("path", d="M60 420 C140 380 260 360 360 350 C420 340 460 360 460 400 C460 430 360 432 60 432Z", fill="#A88A50"), s.T("M430 350 L420 290 M448 352 L458 292", "#A88A50", 10),
                       eye(s, 420, 284, 7, "left"), eye(s, 460, 286, 7, "right"))
D["tapeworm"] = lambda s: ([s.F("rect", x=60 + i * 38, y=290 + int(30 * math.sin(i / 2)), width=34, height=50, rx=6, fill="#F2E3C4") for i in range(10)], s.F("circle", cx=460, cy=300, r=22, fill="#F2E3C4"))


# ---------------------------------------------------------------- dinosaurs and extinct animals
def theropod(s, body="#5E9A4A", belly="#C9D8A0", arms=True, sail=None, small=False, feathers=None, crest=None):
    s.T("M200 300 C120 300 60 260 20 220", body, 46)
    s.T("M210 320 L190 400 L210 440", shade(body, 0.85), 40)
    s.F("ellipse", cx=250, cy=290, rx=110, ry=70, fill=body, transform="rotate(-15 250 290)")
    if sail:
        s.F("path", d="M150 250 C170 120 300 110 330 220Z", fill=sail)
    s.F("ellipse", outline=False, cx=280, cy=320, rx=70, ry=30, fill=belly, transform="rotate(-15 280 320)")
    if feathers:
        s.F("path", d="M190 250 C220 200 260 220 280 250Z", fill=feathers)
    s.T("M250 330 L270 400 L300 440", body, 44)
    s.T("M320 240 L380 180", body, 60)
    s.F("path", d="M350 140 C380 110 470 120 480 160 C485 190 460 200 430 200 L470 210 C460 230 400 236 360 220 C330 200 330 160 350 140Z", fill=body)
    if crest:
        s.F("path", d="M360 140 C330 90 360 60 380 70 C380 100 380 120 380 140Z", fill=crest)
    for x in range(400, 470, 14):
        s.F("polygon", outline=False, points=f"{x},202 {x + 5},212 {x + 10},202", fill=WHITE)
    if arms:
        s.T("M330 270 L360 300 L376 296", body, 14)
    eye(s, 400, 150, 9)


def sauropod(s, body="#7A9AB0", belly="#C9D8E0"):
    s.T("M150 300 C80 300 40 340 20 380", body, 40)
    for x in (180, 320):
        s.T(f"M{x} 320 V440", shade(body, 0.85), 44)
    s.F("ellipse", cx=250, cy=300, rx=140, ry=80, fill=body)
    s.F("ellipse", outline=False, cx=260, cy=340, rx=110, ry=30, fill=belly)
    for x in (210, 300):
        s.T(f"M{x} 330 V440", body, 46)
    s.T("M360 260 C400 200 410 120 420 70", body, 44)
    s.F("ellipse", cx=440, cy=64, rx=46, ry=28, fill=body)
    eye(s, 450, 56, 7)


def quad_dino(s, body="#B08A50", belly="#E8D8A8", kind="trike", accent="#E8782B"):
    s.T("M150 300 C90 310 50 340 30 370", body, 40)
    if kind == "ankylo":
        s.F("ellipse", cx=34, cy=372, rx=30, ry=24, fill=shade(body, 0.75))
    for x in (180, 320):
        s.T(f"M{x} 320 V440", shade(body, 0.85), 40)
    if kind == "stego":
        for k, x in enumerate(range(140, 360, 40)):
            h = 70 - abs(k - 2.5) * 12
            s.F("polygon", points=f"{x - 22},{250} {x},{250 - h:.0f} {x + 22},{250}", fill=accent)
    s.F("ellipse", cx=250, cy=300, rx=140, ry=74, fill=body)
    if kind == "ankylo":
        for x in range(150, 360, 36):
            s.F("polygon", outline=False, points=f"{x - 12},250 {x},228 {x + 12},250", fill=shade(body, 0.7))
    s.F("ellipse", outline=False, cx=260, cy=340, rx=110, ry=26, fill=belly)
    for x in (210, 300):
        s.T(f"M{x} 330 V440", body, 42)
    if kind == "trike":
        s.F("path", d="M330 170 C390 110 470 150 450 230 L400 250Z", fill=accent)
        s.F("ellipse", cx=420, cy=270, rx=70, ry=48, fill=body)
        s.T("M420 230 L470 170 M440 236 L490 196", "#F4F1EA", 12)
        s.F("polygon", points="480,270 500,250 490,280", fill="#F4F1EA")
        eye(s, 430, 256, 8)
    else:
        s.F("ellipse", cx=410, cy=290, rx=56, ry=38, fill=body)
        eye(s, 420, 278, 8)


D["dinosaur"] = lambda s: sauropod(s, body="#5EB85A", belly="#C8E8A8")
D["tyrannosaurus-rex"] = lambda s: theropod(s, body="#5E7A3A", belly="#C9C38A")
D["triceratops"] = lambda s: quad_dino(s, kind="trike")
D["stegosaurus"] = lambda s: quad_dino(s, body="#6E9A5A", belly="#C8D8A8", kind="stego", accent="#E8782B")
D["brachiosaurus"] = lambda s: sauropod(s)
D["diplodocus"] = lambda s: sauropod(s, body="#9A8A6A", belly="#D9CBB0")
D["velociraptor"] = lambda s: theropod(s, body="#C9A24A", belly="#F2E3B0", feathers="#8E5A2A")
D["spinosaurus"] = lambda s: theropod(s, body="#6E7A8A", belly="#C9D0D8", sail="#C1662E")
D["ankylosaurus"] = lambda s: quad_dino(s, body="#8C7A5A", belly="#C9B88A", kind="ankylo")
D["parasaurolophus"] = lambda s: theropod(s, body="#4C9A8A", belly="#B8E0D8", crest="#E8782B", arms=True)
D["iguanodon"] = lambda s: theropod(s, body="#7A8A4A", belly="#C9D08A")
D["allosaurus"] = lambda s: theropod(s, body="#A86A3A", belly="#E8C9A0")


@reg("pterodactyl")
def _(s):
    s.open("part-wing-left", "256 260")
    s.F("path", d="M240 250 L40 180 L120 300 Z", fill="#A8784A")
    s.close()
    s.open("part-wing-right", "256 260")
    s.F("path", d="M272 250 L472 180 L392 300 Z", fill="#A8784A")
    s.close()
    s.F("ellipse", cx=256, cy=270, rx=40, ry=70, fill="#C1662E")
    s.F("path", d="M256 190 C300 170 380 180 420 200 L270 220 Z", fill="#C1662E")
    s.F("path", d="M250 196 C230 160 200 140 180 136 L250 180 Z", fill="#C1662E")
    eye(s, 276, 196, 6)


D["plesiosaurus"] = lambda s: (s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="#BFE6FA"), s.T("M300 300 C350 220 380 150 420 120", "#4C7A9A", 34),
                               s.F("ellipse", cx=250, cy=320, rx=130, ry=60, fill="#4C7A9A"), [s.F("ellipse", cx=x, cy=380, rx=50, ry=16, fill="#3A6A8A", transform=f"rotate(25 {x} 380)") for x in (180, 320)],
                               s.T("M130 320 L60 340", "#4C7A9A", 20), s.F("ellipse", cx=440, cy=112, rx=40, ry=22, fill="#4C7A9A"), eye(s, 448, 104, 6))
D["mosasaurus"] = lambda s: (s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="#BFE6FA"), croc(s, body="#3A6A7A", belly="#B8D8E0"))
D["ichthyosaurus"] = lambda s: (s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="#BFE6FA"),
                                s.F("path", d="M60 260 L30 180 L110 250 L30 330Z", fill="#5A8AA8"), s.F("ellipse", cx=250, cy=256, rx=170, ry=70, fill="#5A8AA8"),
                                s.F("path", d="M400 240 L500 252 L400 270Z", fill="#5A8AA8"), s.F("polygon", points="230,190 260,140 290,192", fill="#5A8AA8"), eye(s, 390, 240, 10))
D["archaeopteryx"] = lambda s: bird(s, body="#6E8AA8", wing="#3A5A7A", head_c="#6E8AA8", beak="short", beak_c=DGREY, tail="long", tail_c="#3A5A7A", legs_c=DGREY)
D["dinosaur-egg"] = lambda s: (s.F("ellipse", cx=256, cy=270, rx=140, ry=180, fill="#E8DCC8"), [s.F("circle", outline=False, cx=x, cy=y, r=r, fill="#B8A88A") for x, y, r in ((200, 200, 20), (300, 260, 26), (230, 340, 18), (300, 160, 12))],
                               s.M("M150 300 l30 20 l20 -30 l30 30 l20 -20", "#8C7A60", 6))
D["dinosaur-skeleton"] = lambda s: (s.T("M30 230 C100 260 160 280 220 280 C300 280 340 240 380 190", "#F4F1EA", 16),
                                    [s.T(f"M{x} {y} v40", "#F4F1EA", 10) for x, y in ((200, 284), (230, 286), (260, 284), (290, 276), (320, 262))],
                                    s.T("M220 290 L200 380 L220 440 M280 280 L300 380 L330 440", "#F4F1EA", 14),
                                    s.F("path", d="M370 150 C400 120 470 130 480 160 C485 190 460 200 430 200 L470 210 C460 230 400 236 380 220 C350 200 350 170 370 150Z", fill="#F4F1EA"),
                                    s.F("circle", outline=False, cx=410, cy=160, r=12, fill="#9AA3AF"))
D["woolly-mammoth"] = lambda s: quad(s, body="#6E4A2A", wool="#7A5232", head_c="#6E4A2A", bw=1.15, bh=1.25, leg_w=50, head_r=80, snout="none", ears="round", trunk=True, tusks=True, tail="thin", leg=0.9, hump=1)
D["mastodon"] = lambda s: quad(s, body="#8C6A4A", bw=1.15, bh=1.2, leg_w=48, head_r=76, snout="none", ears="round", trunk=True, tusks=True, tail="thin", leg=0.85)
D["sabre-toothed-cat"] = lambda s: quad(s, body="#C9A27A", snout="round", snout_c=CREAM, ears="round", tail="short", head_r=58, whiskers=True, tusks=True, bw=1.05)
D["megalodon"] = lambda s: fish(s, body="#5A6A7A", belly=WHITE, tail="crescent", dorsal="shark", length=1.3, height=0.9, teeth=True)
D["giant-sloth"] = lambda s: quad(s, body="#8C7560", wool="#9A8268", bw=1.1, bh=1.2, leg=0.7, leg_w=44, head_r=50, snout="round", ears="none", tail="bushy", tail_c="#8C7560")
D["thylacine"] = lambda s: quad(s, body="#C9A27A", pattern="stripes", pat_c="#5E4A3E", ears="pointy", snout="long", snout_c=CREAM, tail="long", head_r=48, bw=1.05)
D["great-auk"] = lambda s: bird(s, body="#1F1F24", belly=WHITE, beak="big", beak_c="#1F1F24", tail="short", legs_c=DGREY, size=1.0)
D["passenger-pigeon"] = lambda s: bird(s, body="#7A8CA0", wing="#5A6A80", belly="#C97A5A", beak="short", beak_c=DGREY, tail="long", legs_c=RED)
D["quagga"] = lambda s: quad(s, body="#B08A60", pattern="stripes", pat_c="#5E4A3E", neck=0.45, head_r=46, snout="long", snout_c="#5A5A66", ears="pointy", tail="tuft", mane="#5E4A3E", hoof=DGREY, leg=1.2)
D["trilobite"] = lambda s: (s.F("ellipse", cx=256, cy=270, rx=130, ry=180, fill="#8C7A6A"), s.F("path", d="M126 200 C126 110 386 110 386 200Z", fill="#A8967E"),
                            [s.M(f"M136 {y} H376", "#6E5A4A", 8) for y in range(230, 430, 26)], s.M("M256 200 V440", "#6E5A4A", 10))
D["ammonite"] = lambda s: (s.F("circle", cx=256, cy=256, r=190, fill="#C9A27A"), s.M("M256 256 C256 220 300 220 300 256 C300 310 210 310 210 256 C210 170 350 170 350 256 C350 360 160 360 160 256 C160 120 400 120 400 256", "#8C6A4A", 10),
                           [s.M(f"M256 256 L{x:.0f} {y:.0f}", "#A8825A", 4) for x, y in (arc_pt(256, 256, 190, a) for a in range(0, 360, 20))])

# ---------------------------------------------------------------- animal homes
D["nest"] = lambda s: (s.F("ellipse", cx=256, cy=320, rx=200, ry=90, fill="#A0703E"), s.F("ellipse", outline=False, cx=256, cy=290, rx=150, ry=40, fill="#6E4A2A"),
                       s.M("M70 320 C150 360 360 360 440 320 M90 350 C170 390 340 390 420 350", "#C9A27A", 8))
D["bird-nest-with-eggs"] = lambda s: (D["nest"](s), [s.F("ellipse", cx=x, cy=270, rx=34, ry=44, fill="#9AD0E8") for x in (200, 256, 312)],
                                      s.F("path", d="M60 310 C120 380 392 380 452 310 C400 330 112 330 60 310Z", fill="#A0703E"))
D["burrow"] = lambda s: (s.F("rect", outline=False, x=20, y=200, width=472, height=270, fill="#8C6A3A"), s.F("rect", outline=False, x=20, y=170, width=472, height=40, fill="#5EB85A"),
                         s.F("path", d="M140 210 C140 300 260 300 300 360 C340 410 420 410 440 380", fill="none"), s.T("M150 210 C150 300 260 300 300 360 C340 410 420 410 440 380", "#3A2E22", 60))
D["den"] = lambda s: (s.F("path", d="M30 460 C60 260 200 160 300 180 C420 200 480 320 482 460Z", fill="#8C7A6A"), s.F("path", d="M190 460 C190 340 340 340 340 460Z", fill="#2E2A28"))


@reg("beehive")
def _(s):
    s.T("M256 30 V80", BROWN, 14)
    for i, (w, y) in enumerate(((90, 100), (130, 160), (160, 220), (170, 280), (150, 340), (110, 395))):
        s.F("ellipse", cx=256, cy=y, rx=w, ry=40, fill="#E8B030" if i % 2 else "#F2C94C")
    s.F("ellipse", cx=256, cy=320, rx=26, ry=20, fill="#3A2E28")


D["honeycomb"] = lambda s: [s.F("polygon", points=" ".join(f"{x:.0f},{y:.0f}" for x, y in (arc_pt(cx, cy, 52, a) for a in range(30, 390, 60))), fill="#F2B930")
                            for cx, cy in ((166, 160), (256, 160), (346, 160), (121, 238), (211, 238), (301, 238), (391, 238), (166, 316), (256, 316), (346, 316))]
D["anthill"] = lambda s: (s.F("path", d="M60 440 C140 420 200 220 256 200 C312 220 372 420 452 440Z", fill="#B08A50"), s.F("ellipse", outline=False, cx=256, cy=212, rx=16, ry=8, fill="#3A2E22"),
                          [s.F("circle", outline=False, cx=x, cy=y, r=5, fill="#3A2E22") for x, y in ((200, 330), (300, 360), (240, 280))])
D["termite-mound"] = lambda s: (s.F("path", d="M120 440 C140 300 180 200 200 80 C230 60 250 120 260 150 C280 100 300 120 310 180 C330 300 370 380 392 440Z", fill="#C1662E"), s.M("M200 160 V420 M280 220 V420", "#A04E22", 8))
D["beaver-lodge"] = lambda s: (s.F("rect", outline=False, x=20, y=360, width=472, height=110, fill="#8FD0FF"),
                               s.F("path", d="M60 380 C100 220 200 180 256 180 C312 180 412 220 452 380Z", fill="#8C6A3A"),
                               [s.T(f"M{x1} {y1} L{x2} {y2}", "#6E4A2A", 12) for x1, y1, x2, y2 in ((100, 330, 220, 240), (300, 220, 420, 340), (150, 280, 360, 260), (200, 360, 330, 300))])
D["kennel"] = lambda s: (s.F("rect", x=110, y=230, width=292, height=210, fill="#C1662E"), s.F("polygon", points="80,250 256,110 432,250", fill="#8E3E1E"), s.F("path", d="M196 440 V340 C196 290 316 290 316 340 V440Z", fill="#3A2E28"))
D["cat-bed"] = lambda s: (s.F("ellipse", cx=256, cy=340, rx=200, ry=90, fill="#8B5CF6"), s.F("ellipse", outline=False, cx=256, cy=320, rx=150, ry=50, fill="#C4B5FD"))
D["bird-cage"] = lambda s: (s.F("path", d="M110 440 V220 C110 100 402 100 402 220 V440Z", fill="none"), [s.M(f"M{x} 440 V{200 if 140 < x < 372 else 240}", GREY, 8) for x in range(110, 410, 36)],
                            s.M("M110 220 C110 100 402 100 402 220 M110 440 H402", GREY, 10), s.T("M256 60 V110", GREY, 10), s.T("M150 330 H362", BROWN, 10))
D["birdhouse"] = lambda s: (s.T("M256 460 V360", BROWN, 24), s.F("rect", x=150, y=170, width=212, height=200, fill=C["sky"]), s.F("polygon", points="120,190 256,80 392,190", fill=RED),
                            s.F("circle", cx=256, cy=250, r=36, fill="#2E2A3B"), s.T("M256 310 V330", BROWN, 10))
D["aquarium"] = lambda s: (s.F("rect", x=60, y=130, width=392, height=280, rx=12, fill="#BFE6FA"), s.F("rect", outline=False, x=70, y=360, width=372, height=40, fill="#E8D8A8"),
                           s.T("M120 400 C110 340 130 300 120 250 M380 400 C390 330 370 280 380 220", "#4CB963", 12),
                           s.F("ellipse", cx=250, cy=250, rx=50, ry=30, fill=ORANGE), s.F("polygon", points="200,250 170,226 170,274", fill=ORANGE), s.F("rect", x=50, y=110, width=412, height=26, rx=8, fill=DGREY))
D["stable"] = lambda s: (s.F("rect", x=60, y=200, width=392, height=240, fill="#A0582E"), s.F("polygon", points="40,210 256,90 472,210", fill="#6E3E22"),
                         s.F("rect", x=196, y=290, width=120, height=150, fill="#6E3E22"), s.M("M196 290 L316 440 M316 290 L196 440", "#F4F1EA", 8))
D["cowshed"] = lambda s: (s.F("rect", x=60, y=220, width=392, height=220, fill="#C9A27A"), s.F("polygon", points="40,230 256,120 472,230", fill="#8C6A3A"),
                          s.F("rect", outline=False, x=60, y=380, width=392, height=60, fill="#E8D8A8"), [s.T(f"M{x} 300 V440", "#8C6A3A", 12) for x in (140, 256, 372)])
D["pigsty"] = lambda s: (s.F("ellipse", cx=256, cy=420, rx=230, ry=40, fill="#8C6A3A"), [s.T(f"M{x} 440 V320", "#C9A27A", 14) for x in range(50, 480, 60)], s.T("M40 340 H472 M40 390 H472", "#C9A27A", 12))
D["hen-house"] = lambda s: (s.F("rect", x=120, y=220, width=272, height=170, fill=C["red"]), s.F("polygon", points="100,230 256,130 412,230", fill="#8E2128"),
                            s.F("rect", x=226, y=290, width=60, height=100, fill="#3A2E28"), s.T("M256 390 L320 460", BROWN, 14), [s.T(f"M{x} 390 V450", BROWN, 14) for x in (140, 372)])
D["rabbit-hutch"] = lambda s: (s.F("rect", x=80, y=200, width=352, height=180, fill="#C9A27A"), s.F("polygon", points="60,210 256,130 452,210", fill="#6E4A2A"),
                               s.F("rect", x=100, y=220, width=180, height=140, fill="#FFF8E7"), [s.M(f"M{x} 220 V360", GREY, 6) for x in range(110, 280, 22)], s.F("rect", x=300, y=220, width=112, height=140, fill="#8C6A3A"),
                               [s.T(f"M{x} 380 V450", "#6E4A2A", 14) for x in (100, 412)])
D["cave-den"] = lambda s: D["den"](s)
D["shell-home"] = lambda s: (s.F("circle", cx=256, cy=270, r=170, fill="#E8C39E"), s.M("M256 270 C256 220 320 220 320 270 C320 340 190 340 190 270 C190 160 370 160 370 270", "#B08A60", 12))
D["coral-reef-home"] = lambda s: (s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="#BFE6FA"), s.F("rect", outline=False, x=0, y=420, width=512, height=92, fill="#E8D8A8"),
                                  s.T("M150 440 V320 M150 360 C120 330 110 290 120 250 M150 340 C180 310 200 280 200 240", "#F5806A", 26),
                                  s.T("M350 440 V340 M350 380 C320 360 310 330 320 300 M350 360 C380 340 400 320 400 290", "#B880E8", 24),
                                  s.F("ellipse", cx=260, cy=220, rx=40, ry=24, fill=ORANGE), s.F("polygon", points="220,220 196,204 196,236", fill=ORANGE))

# ---------------------------------------------------------------- animal body parts
D["tail"] = lambda s: s.F("path", d="M80 360 C40 300 80 200 180 180 C300 160 380 240 440 160 C460 260 360 320 260 300 C180 290 140 330 140 380Z", fill="#E8782B")
D["wing"] = lambda s: (s.F("path", d="M60 360 C80 220 220 100 460 80 C420 160 380 220 330 260 C300 300 220 360 60 360Z", fill="#9AA3AF"),
                       s.M("M120 330 C200 260 300 200 420 120 M140 350 L170 300 M200 340 L240 280 M260 320 L310 250", "#6B7280", 6))
D["feather"] = lambda s: (s.F("path", d="M140 440 C120 300 200 120 400 70 C380 220 300 360 160 440Z", fill="#3D8BFD"), s.M("M140 460 C200 340 290 210 390 80", "#1E3A8A", 8))
D["fin"] = lambda s: s.F("path", d="M80 400 C160 380 260 300 300 100 C340 220 400 340 440 400Z", fill="#5A8AA8")
D["beak"] = lambda s: s.F("path", d="M80 200 C200 180 380 200 460 260 C380 300 200 320 80 300Z", fill=ORANGE)
D["horn"] = lambda s: s.F("path", d="M140 440 C120 300 200 140 380 80 C300 180 260 320 260 440Z", fill="#E8DCC8")
D["antlers"] = lambda s: (s.T("M256 460 V300 M256 300 C200 200 140 160 100 80 M256 300 C312 200 372 160 412 80 M180 200 L120 200 M332 200 L392 200 M140 140 L180 80 M372 140 L332 80", "#6E4A2A", 18))
D["tusk"] = lambda s: s.F("path", d="M100 140 C120 320 240 420 420 400 C300 380 200 300 160 140Z", fill="#FFF8E7")
D["trunk"] = lambda s: s.T("M200 60 C200 200 230 300 300 380 C340 420 380 400 380 360", "#9AA3AF", 80)
D["claw"] = lambda s: [s.F("path", d=f"M{x} 160 C{x + 60} 200 {x + 70} 300 {x + 40} 400 C{x + 30} 320 {x + 10} 240 {x - 20} 180Z", fill="#3A3A44") for x in (130, 230, 330)]
D["paw"] = lambda s: (s.F("ellipse", cx=256, cy=330, rx=110, ry=90, fill="#3A3A44"), [s.F("ellipse", cx=x, cy=y, rx=36, ry=46, fill="#3A3A44") for x, y in ((150, 200), (220, 150), (292, 150), (362, 200))])
D["paw-print"] = lambda s: (s.F("ellipse", cx=256, cy=330, rx=100, ry=82, fill="#6E5A4A"), [s.F("ellipse", cx=x, cy=y, rx=32, ry=42, fill="#6E5A4A") for x, y in ((160, 200), (225, 150), (290, 150), (355, 200))])
D["hoof"] = lambda s: (s.F("path", d="M160 140 H352 L380 400 H132Z", fill="#8C6A4A"), s.F("path", d="M132 400 H380 L400 440 H112Z", fill="#3A3A44"), s.M("M256 400 V440", "#8C96A3", 8))
D["mane"] = lambda s: s.F("polygon", points=star_pts(256, 256, 210, 160, 16), fill="#8E5A2A")
D["whiskers"] = lambda s: (s.F("circle", cx=256, cy=256, r=50, fill=PINK), s.M("M210 240 L60 200 M210 256 L50 256 M210 272 L60 312 M302 240 L452 200 M302 256 L462 256 M302 272 L452 312", "#3A3A44", 6))
D["fangs"] = lambda s: (s.F("path", d="M80 200 C200 160 312 160 432 200 V240 H80Z", fill="#C1442E"), [s.F("polygon", points=f"{x - 30},240 {x + 30},240 {x},380", fill=WHITE) for x in (170, 342)])
D["scales"] = lambda s: [s.F("path", d=f"M{x - 50} {y} A50 50 0 0 0 {x + 50} {y}Z", fill="#4CB963" if (r + c) % 2 else "#5EB85A") for r in range(5) for c in range(5) for x, y in [(80 + c * 90 + (r % 2) * 45, 120 + r * 70)]]
D["shell"] = lambda s: (s.F("path", d="M80 380 C80 160 432 160 432 380Z", fill="#8C6A3A"), [s.F("polygon", outline=False, points=" ".join(f"{a:.0f},{b:.0f}" for a, b in (arc_pt(x, y, 40, k * 60) for k in range(6))), fill="#6E4A2A") for x, y in ((180, 320), (256, 270), (332, 320))])
D["gills"] = lambda s: (s.F("ellipse", cx=256, cy=256, rx=200, ry=140, fill="#5A8AA8"), [s.M(f"M{x} 160 C{x + 30} 220 {x + 30} 290 {x} 350", "#C1442E", 10) for x in (230, 270, 310)])
D["tentacle"] = lambda s: (s.T("M120 460 C140 300 280 300 300 180 C310 120 270 80 230 100", "#E8782B", 50), [s.F("circle", outline=False, cx=x, cy=y, r=8, fill="#F9B57A") for x, y in ((150, 420), (190, 350), (250, 300), (290, 230))])
D["quills"] = lambda s: [s.T(f"M256 460 L{x:.0f} {y:.0f}", "#6E5A4A" if a % 2 else "#E8DCC8", 10) for a, (x, y) in enumerate(arc_pt(256, 460, 380, a2) for a2 in range(200, 341, 10))]
D["fur"] = lambda s: (s.F("rect", x=60, y=100, width=392, height=312, rx=40, fill="#C68A5C"), [s.M(f"M{x} {y} q10 -20 20 0", "#8E5A2A", 6) for x in range(90, 420, 40) for y in range(140, 400, 50)])
D["animal-egg"] = lambda s: (s.F("ellipse", cx=256, cy=270, rx=130, ry=170, fill="#F4E8D8"), s.F("ellipse", outline=False, cx=210, cy=200, rx=26, ry=44, fill=WHITE))
D["antennae"] = lambda s: (s.F("circle", cx=256, cy=380, r=80, fill="#3A3A44"), s.T("M230 310 C200 200 150 140 100 100 M282 310 C312 200 362 140 412 100", "#3A3A44", 12),
                           s.F("circle", cx=100, cy=100, r=20, fill="#3A3A44"), s.F("circle", cx=412, cy=100, r=20, fill="#3A3A44"))
D["stinger"] = lambda s: (s.F("ellipse", cx=200, cy=256, rx=150, ry=90, fill=YEL), [s.F("rect", outline=False, x=x, y=170, width=30, height=172, fill="#2E2A3B") for x in (120, 200)], s.F("polygon", points="340,236 470,256 340,276", fill="#2E2A3B"))
D["footprint-animal"] = lambda s: [s.F("polygon", points=f"{x},{y} {x - 26},{y + 50} {x},{y + 34} {x + 26},{y + 50}", fill="#6E5A4A") for x, y in ((150, 380), (250, 290), (330, 190), (410, 90))]


if __name__ == "__main__":
    run("animals", D, sys.argv[1:] or None)
