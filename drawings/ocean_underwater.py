"""ocean-underwater drawings. Run: python drawings/ocean_underwater.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, eye, fish, shade, tint  # noqa: E402
from draw_lib import C, INK, arc_pt, run, star_pts  # noqa: E402

D = {}
GOLD, GOLDD, SAND, ROCK, ROCKD = C["gold"], C["darkgold"], "#E8D8A8", "#8C8A8A", "#5E5C5C"
WATER = ["#BFE6FA", "#7FC4EE", "#3D8BC9", "#1E4F86", "#10294A", "#08162A"]


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def tile(s, color=WATER[1]):
    s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill=color)


def bands(s, highlight=None):
    s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill=WATER[0])
    for i, c in enumerate(WATER[:5]):
        y = 24 + i * 92.8
        s.F("rect", outline=False, x=24, y=f"{y:.0f}", width=464, height=93, fill=c if highlight is None or highlight == i else shade(c, 0.55))
    s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill="none")


def small_fish(s, x, y, sc, body, flip=False):
    s.open(transform=f"translate({x} {y}) scale({-sc if flip else sc} {sc}) translate(-240 -256)")
    fish(s, body=body, tail="fork", length=0.9)
    s.close()


def jelly(s, x, y, sc, color="#E0B8F0", glow=False):
    s.open(transform=f"translate({x} {y}) scale({sc})")
    if glow:
        s.F("circle", outline=False, cx=0, cy=0, r=90, fill=color, fill_opacity="0.3")
    for dx in (-30, -10, 10, 30):
        s.T(f"M{dx} 10 C{dx - 10} 50 {dx + 10} 80 {dx} 120", color, 6)
    s.F("path", d="M-60 20 C-60 -60 60 -60 60 20Z", fill=color)
    s.close()


def seafloor(s, y=420, color=SAND):
    s.F("path", outline=False, d=f"M24 {y} C120 {y - 20} 220 {y + 10} 320 {y - 10} C400 {y - 24} 450 {y} 488 {y - 6} V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill=color)


def weed(s, x, y, h=120, color="#4CB963"):
    s.T(f"M{x} {y} C{x - 20} {y - h * 0.3} {x + 20} {y - h * 0.6} {x} {y - h}", color, 14)


# ---------------------------------------------------------------- zones and features
@reg("ocean-layers")
def _(s):
    bands(s)
    s.F("circle", cx=420, cy=60, r=26, fill=C["yellow"])
    small_fish(s, 150, 70, 0.2, C["orange"])
    jelly(s, 330, 160, 0.4)
    s.F("circle", outline=False, cx=200, cy=260, r=10, fill="#FFE38A")
    seafloor(s, 470, "#3A3A44")


for _i, _id in enumerate(("sunlight-zone", "twilight-zone", "midnight-zone", "abyssal-zone", "hadal-zone")):
    def _zone(s, i=_i):
        bands(s, highlight=i)
        y = 24 + i * 92.8 + 46
        if i == 0:
            s.F("circle", cx=420, cy=60, r=26, fill=C["yellow"])
            small_fish(s, 200, y, 0.22, C["orange"])
        elif i == 1:
            jelly(s, 256, y - 20, 0.45)
        elif i == 2:
            s.F("circle", outline=False, cx=256, cy=y, r=22, fill="#FFE38A")
        elif i == 3:
            s.F("circle", outline=False, cx=200, cy=y, r=8, fill="#8FD0FF")
            s.F("circle", outline=False, cx=320, cy=y + 10, r=6, fill="#8FD0FF")
        else:
            s.F("polygon", points=f"200,{y - 40} 256,{y + 40} 312,{y - 40}", fill="#05101E")
    D[_id] = _zone


@reg("mariana-trench")
def _(s):
    tile(s, WATER[3])
    s.F("path", d="M24 200 H190 L240 470 H272 L322 200 H488 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill="#3A3A44")
    s.F("polygon", outline=False, points="190,200 240,470 272,470 322,200", fill="#05101E")


D["challenger-deep"] = lambda s: (D["mariana-trench"](s), s.F("polygon", points=star_pts(256, 440, 22, 9, 5), fill=C["red"]))


@reg("continental-shelf")
def _(s):
    tile(s, WATER[2])
    s.F("path", outline=False, d="M24 24 H488 V120 H24Z", fill=C["sky"])
    s.F("path", d="M24 150 H260 C300 160 330 300 380 420 H488 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill=SAND)


D["seafloor"] = lambda s: (tile(s, WATER[3]), seafloor(s, 330, "#C9B88A"), [s.F("ellipse", cx=x, cy=y, rx=30, ry=18, fill=ROCK) for x, y in ((120, 380), (300, 410), (400, 360))],
                           weed(s, 200, 380), weed(s, 360, 400, 90))
D["mid-ocean-ridge"] = lambda s: (tile(s, WATER[3]), s.F("path", d="M24 400 L150 300 L220 330 L256 230 L292 330 L362 300 L488 400 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill="#5E5C5C"),
                                  s.F("polygon", outline=False, points="244,240 256,230 268,240 262,300 250,300", fill=C["orange"]))
D["abyssal-plain"] = lambda s: (tile(s, WATER[4]), seafloor(s, 360, "#3A3A44"), s.F("circle", outline=False, cx=120, cy=150, r=6, fill="#8FD0FF"), s.F("circle", outline=False, cx=380, cy=200, r=5, fill="#8FD0FF"))


@reg("hydrothermal-vent")
def _(s):
    tile(s, WATER[4])
    seafloor(s, 440, "#3A3A44")
    for x, h in ((180, 220), (300, 280)):
        s.F("polygon", points=f"{x - 50},450 {x - 20},{450 - h} {x + 20},{450 - h} {x + 50},450", fill="#5E5C5C")
        for k in range(4):
            s.F("circle", cx=x + (k % 2) * 16 - 8, cy=440 - h - 30 - k * 40, r=24 + k * 8, fill="#2E2A3B")


D["cold-seep"] = lambda s: (tile(s, WATER[4]), seafloor(s, 420, "#4A4A55"), [s.F("circle", cx=x, cy=y, r=r, fill="#9AA3AF") for x, y, r in ((240, 380, 10), (250, 340, 14), (236, 290, 18), (260, 230, 12))],
                            [s.F("ellipse", cx=x, cy=420, rx=24, ry=14, fill=WHITE) for x in (150, 330, 380)])
D["underwater-volcano"] = lambda s: (tile(s, WATER[3]), s.F("polygon", points="60,470 210,220 300,220 452,470", fill="#5E5C5C"),
                                     s.F("path", outline=False, d="M210 220 C230 180 280 180 300 220Z", fill=C["orange"]), [s.F("circle", cx=x, cy=y, r=r, fill="#3A3A44") for x, y, r in ((240, 160, 30), (280, 110, 40), (250, 60, 30))])
D["underwater-cave"] = lambda s: (tile(s, WATER[2]), s.F("path", d="M24 24 H488 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill="#5E5C5C"),
                                  s.F("path", d="M100 488 C100 260 200 180 256 180 C312 180 412 260 412 488Z", fill=WATER[3]), small_fish(s, 256, 360, 0.25, C["yellow"]))
D["kelp-forest"] = lambda s: (tile(s, WATER[1]), seafloor(s, 450), [s.T(f"M{x} 470 C{x - 30} 360 {x + 30} 240 {x} 60", "#6E7A2A", 18) for x in (100, 190, 300, 400)],
                              [s.F("ellipse", cx=x + 18, cy=y, rx=26, ry=10, fill="#8C9A3A", transform=f"rotate(-30 {x + 18} {y})") for x in (100, 190, 300, 400) for y in (380, 260, 150)])
D["seagrass-meadow"] = lambda s: (tile(s, WATER[1]), seafloor(s, 430), [s.T(f"M{x} 460 C{x - 10} 400 {x + 10} 350 {x} 300", "#4CB963", 8) for x in range(60, 470, 22)])


@reg("coral-reef")
def _(s):
    tile(s, WATER[1])
    seafloor(s, 430)
    s.T("M120 440 V320 M120 360 C90 330 80 290 90 250 M120 340 C150 310 170 280 170 240", "#F5806A", 26)
    s.T("M360 440 V340 M360 380 C330 360 320 330 330 300 M360 360 C390 340 410 320 410 290", "#B880E8", 24)
    s.F("circle", cx=250, cy=410, r=46, fill=C["yellow"])
    small_fish(s, 270, 180, 0.3, C["orange"])
    small_fish(s, 160, 120, 0.2, C["blue"], True)


D["coral-bleaching"] = lambda s: (tile(s, WATER[1]), seafloor(s, 430), s.T("M200 440 V300 M200 350 C160 320 150 280 160 240 M200 330 C240 300 260 270 260 230", "#F4F1EA", 28),
                                  s.T("M340 440 V340 M340 380 C320 360 310 330 320 300", "#F7D0C8", 24))

# ---------------------------------------------------------------- tides, waves, currents
D["ocean-wave"] = lambda s: (s.F("path", d="M40 400 C80 240 220 140 340 160 C440 180 470 260 420 300 C380 330 330 290 350 250 C300 260 280 330 300 400Z", fill="#3D8BFD"),
                             s.F("path", outline=False, d="M340 160 C440 180 470 260 420 300 C460 240 430 200 340 190Z", fill="#BFE6FA"), s.F("rect", x=30, y=400, width=452, height=60, rx=20, fill="#2C6BD6"))
D["big-wave"] = lambda s: (s.F("path", d="M30 460 C40 220 200 60 360 80 C470 100 490 220 430 260 C380 290 330 240 360 200 C280 200 240 300 260 460Z", fill="#2C6BD6"),
                           s.F("path", outline=False, d="M360 80 C470 100 490 220 430 260 C470 190 440 130 360 110Z", fill="#BFE6FA"))
D["high-tide"] = lambda s: (tile(s, C["sky"]), s.F("rect", outline=False, x=24, y=200, width=464, height=288, fill="#3D8BC9"), s.F("polygon", outline=False, points="300,488 488,330 488,488", fill=SAND),
                            s.M("M110 120 V180 M90 160 L110 180 L130 160", C["blue"], 10))
D["low-tide"] = lambda s: (tile(s, C["sky"]), s.F("rect", outline=False, x=24, y=360, width=464, height=128, fill="#3D8BC9"), s.F("polygon", outline=False, points="24,300 488,300 488,360 24,360", fill=SAND),
                           s.M("M110 180 V120 M90 140 L110 120 L130 140", C["blue"], 10))
D["tide-pool"] = lambda s: (tile(s, "#8C8A8A"), s.F("ellipse", cx=256, cy=290, rx=180, ry=120, fill=WATER[1]), s.F("polygon", points=star_pts(200, 300, 40, 16, 5), fill=C["orange"]),
                            s.F("circle", cx=320, cy=260, r=26, fill="#7A3A7A"))
D["ocean-current"] = lambda s: (tile(s, WATER[2]), [s.M(f"M60 {y} C160 {y - 40} 300 {y + 40} 420 {y} l-30 -20 m30 20 l-30 20", WHITE, 10) for y in (160, 256, 352)])
D["gulf-stream"] = lambda s: (tile(s, WATER[2]), s.T("M60 420 C160 360 220 220 300 160 C360 110 420 100 460 80", "#E8782B", 30), s.M("M440 70 l26 8 l-14 24", "#E8782B", 10))
D["whirlpool"] = lambda s: (tile(s, WATER[2]), s.M("M256 256 " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in (arc_pt(256, 256, 8 + t * 1.3, t * 7) for t in range(1, 150))), WHITE, 10))
D["rip-current"] = lambda s: (tile(s, WATER[1]), s.F("polygon", outline=False, points="24,400 488,400 488,488 24,488", fill=SAND), s.M("M256 400 V120 M230 150 L256 120 L282 150", C["red"], 14),
                              s.M("M120 330 C160 360 200 380 240 390 M392 330 C352 360 312 380 272 390", WHITE, 8))
D["sea-foam"] = lambda s: (tile(s, WATER[1]), [s.F("circle", cx=x, cy=y, r=r, fill=WHITE) for x, y, r in ((150, 300, 60), (230, 270, 70), (320, 300, 60), (390, 320, 44), (100, 330, 40))])

# ---------------------------------------------------------------- light
D["bioluminescence"] = lambda s: (tile(s, WATER[5]), [s.F("circle", outline=False, cx=x, cy=y, r=r, fill="#6EF0FF") for x, y, r in ((120, 140, 6), (200, 220, 8), (300, 160, 5), (380, 260, 9), (160, 360, 7), (320, 380, 6), (420, 400, 5))],
                                  jelly(s, 256, 260, 0.8, "#6EF0FF", glow=True))
D["glowing-plankton"] = lambda s: (tile(s, WATER[5]), [s.F("circle", outline=False, cx=x, cy=y, r=r, fill="#6EF0FF") for x, y, r in ((100, 300, 8), (150, 340, 6), (200, 300, 10), (260, 340, 7), (320, 300, 9), (380, 330, 6), (420, 290, 8))],
                                   s.M("M60 320 C150 290 300 350 460 310", "#6EF0FF", 4))
D["glowing-jellyfish"] = lambda s: (tile(s, WATER[5]), jelly(s, 256, 220, 1.6, "#B8F0FF", glow=True))
D["plankton"] = lambda s: (tile(s, WATER[1]), [s.F("ellipse", cx=x, cy=y, rx=24, ry=14, fill=c, transform=f"rotate({x % 60} {x} {y})") for x, y, c in
                                               ((150, 180, "#4CB963"), (300, 160, "#9BD7A8"), (220, 280, "#4CB963"), (360, 300, "#C8E8A8"), (160, 380, "#9BD7A8"), (330, 400, "#4CB963"))])
D["phytoplankton"] = lambda s: (tile(s, WATER[1]), [s.F("circle", cx=x, cy=y, r=r, fill="#5EB85A") for x, y, r in ((180, 200, 40), (300, 260, 50), (220, 340, 30), (360, 160, 26))],
                                [s.F("circle", outline=False, cx=x, cy=y, r=10, fill="#C8E8A8") for x, y in ((170, 190), (290, 250), (215, 335))])

# ---------------------------------------------------------------- wrecks and treasure
def wreck(s, tilt=-12):
    s.open(transform=f"rotate({tilt} 256 330)")
    s.F("path", d="M70 280 H440 L400 380 H110Z", fill="#6E4A2A")
    s.M("M90 310 H420 M100 340 H410", "#4A3020", 6)
    s.T("M220 280 V120 M320 280 V160", "#4A3020", 14)
    s.F("path", d="M226 140 C280 150 290 200 280 240 L226 250Z", fill="#C9B79A")
    s.close()


D["shipwreck"] = lambda s: (tile(s, WATER[2]), seafloor(s, 420), wreck(s), weed(s, 420, 450, 80))
D["sunken-ship"] = lambda s: (tile(s, WATER[3]), seafloor(s, 430, "#C9B88A"), wreck(s, 15))


def chest(s, x=256, y=330, sc=1.0, open_=True):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -330)")
    s.F("rect", x=130, y=290, width=252, height=140, rx=10, fill="#8C5A2A")
    s.M("M130 330 H382", GOLD, 12)
    if open_:
        s.F("path", d="M140 290 L170 200 H400 L382 290Z", fill="#6E4422")
        for cx_, cy_ in ((190, 290), (230, 280), (270, 286), (310, 278), (350, 290)):
            s.F("circle", cx=cx_, cy=cy_, r=22, fill=GOLD)
    else:
        s.F("path", d="M130 290 C130 230 382 230 382 290Z", fill="#6E4422")
    s.F("rect", x=236, y=320, width=40, height=40, rx=6, fill=GOLD)
    s.close()


D["sunken-treasure"] = lambda s: (tile(s, WATER[2]), seafloor(s, 420), chest(s, 256, 330, 0.9), small_fish(s, 380, 140, 0.2, C["yellow"]))
D["treasure-chest-underwater"] = lambda s: (tile(s, WATER[2]), seafloor(s, 430), chest(s, 256, 330, 1.0, open_=False), [s.F("circle", cx=x, cy=y, r=r, fill=WHITE) for x, y, r in ((300, 200, 8), (310, 160, 12), (296, 110, 9))])
D["gold-coins-underwater"] = lambda s: (tile(s, WATER[2]), seafloor(s, 420), [(s.F("ellipse", cx=x, cy=y, rx=40, ry=16, fill=GOLD), s.F("ellipse", outline=False, cx=x, cy=y - 4, rx=26, ry=8, fill="#F7D57A"))
                                                                            for x, y in ((180, 420), (250, 400), (320, 424), (220, 380), (290, 370))])


@reg("anchor")
def _(s):
    s.T("M256 140 V420 M170 200 H342 M110 330 C130 420 200 440 256 440 C312 440 382 420 402 330", "#5A6270", 30)
    s.F("polygon", points="96,340 120,300 140,346", fill="#5A6270")
    s.F("polygon", points="416,340 392,300 372,346", fill="#5A6270")
    s.T("M256 100 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0", "#5A6270", 22)


@reg("ships-wheel-underwater")
def _(s):
    tile(s, WATER[2])
    for a in range(0, 360, 45):
        x1, y1 = arc_pt(256, 256, 60, a); x2, y2 = arc_pt(256, 256, 200, a)
        s.T(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", "#8C5A2A", 18)
    s.T("M256 106 A150 150 0 1 1 255.9 106", "#8C5A2A", 30)
    s.F("circle", cx=256, cy=256, r=50, fill="#6E4422")


D["message-in-a-bottle"] = lambda s: (s.F("rect", outline=False, x=24, y=330, width=464, height=158, rx=30, fill=WATER[1]),
                                      s.F("path", d="M120 300 C110 260 160 220 220 230 L380 260 C400 264 410 300 390 310 L230 340 C170 350 130 330 120 300Z", fill="#9BD7A8", fill_opacity="0.9"),
                                      s.F("rect", x=380, y=262, width=60, height=36, rx=8, fill="#8C5A2A", transform="rotate(10 410 280)"),
                                      s.F("rect", x=190, y=258, width=120, height=50, rx=10, fill="#F7E3C4", transform="rotate(10 250 283)"))
D["sunken-plane"] = lambda s: (tile(s, WATER[3]), seafloor(s, 430, "#C9B88A"), s.F("path", d="M80 380 L380 330 C420 324 440 340 430 360 L120 410Z", fill="#9AA3AF"),
                               s.F("polygon", points="220,360 300,260 330,262 290,360", fill="#8C96A3"), s.F("polygon", points="110,390 90,330 120,330 140,386", fill="#8C96A3"), weed(s, 330, 440, 60))
D["sunken-city-ruins"] = lambda s: (tile(s, WATER[3]), seafloor(s, 440, "#C9B88A"), [s.F("rect", x=x, y=250, width=40, height=190, fill="#D9CBB0") for x in (100, 200, 300)],
                                    s.F("rect", x=80, y=230, width=280, height=30, fill="#D9CBB0"), s.F("rect", x=380, y=360, width=60, height=80, fill="#D9CBB0", transform="rotate(20 410 400)"), weed(s, 170, 440, 80))

# ---------------------------------------------------------------- diving gear
SKIN, SUIT = C["skin"], "#2E3A4A"


@reg("scuba-diver")
def _(s):
    tile(s, WATER[1])
    s.F("rect", x=200, y=170, width=150, height=46, rx=22, fill=C["yellow"])
    s.T("M120 300 L60 260 M120 312 L60 330", SUIT, 30)
    s.F("polygon", points="60,240 10,210 20,280", fill=C["orange"])
    s.F("polygon", points="60,320 10,330 30,380", fill=C["orange"])
    s.T("M120 290 L330 250", SUIT, 74)
    s.T("M300 270 L380 320 L420 300", SUIT, 24)
    s.F("circle", cx=380, cy=230, r=44, fill=SKIN)
    s.F("path", d="M336 222 C336 180 424 180 424 222Z", fill=SUIT)
    s.F("rect", x=382, y=204, width=50, height=40, rx=12, fill=C["sky"])
    s.T("M360 250 C350 290 320 300 300 280", "#3A3A44", 8)
    for k in range(3):
        s.F("circle", cx=440 + k * 10, cy=190 - k * 40, r=8 + k * 3, fill=WHITE)


D["scuba-tank"] = lambda s: (s.F("rect", x=236, y=70, width=40, height=50, rx=6, fill="#9AA3AF"), s.T("M276 90 C330 90 340 140 330 180", "#3A3A44", 10),
                             s.F("rect", x=196, y=110, width=120, height=330, rx=56, fill=C["yellow"]), s.M("M206 200 H306", "#E8B030", 10))
D["diving-mask"] = lambda s: (s.T("M90 250 C40 250 40 330 110 320 M422 250 C472 250 472 330 402 320", "#3A3A44", 20), s.F("rect", x=100, y=180, width=312, height=160, rx=60, fill="#2E3A4A"),
                              s.F("rect", outline=False, x=126, y=204, width=120, height=112, rx=40, fill=C["sky"]), s.F("rect", outline=False, x=266, y=204, width=120, height=112, rx=40, fill=C["sky"]),
                              s.F("polygon", points="226,340 286,340 256,390", fill="#2E3A4A"))
D["snorkel"] = lambda s: (s.T("M300 60 V340 C300 410 240 430 200 400", C["orange"], 40), s.F("rect", x=170, y=370, width=60, height=50, rx=14, fill="#3A3A44"))
D["swim-fins"] = lambda s: [s.F("path", d=f"M{x - 50} 100 H{x + 50} V200 L{x + 90} 440 H{x - 90} L{x - 50} 200Z", fill=c) for x, c in ((160, C["orange"]), (352, C["yellow"]))]
D["wetsuit"] = lambda s: s.F("path", d="M190 70 H322 L400 150 L370 200 L330 160 V300 L350 460 H272 L256 330 L240 460 H162 L182 300 V160 L142 200 L112 150Z", fill="#2E3A4A")
D["diving-helmet"] = lambda s: (s.F("circle", cx=256, cy=230, r=170, fill="#C98A3E"), s.F("circle", cx=256, cy=240, r=80, fill="#8FD0FF"), s.M("M256 160 V320 M176 240 H336", "#8C5A2A", 10),
                                s.F("rect", x=100, y=380, width=312, height=70, rx=20, fill="#C98A3E"), [s.F("circle", cx=x, cy=230, r=34, fill="#8FD0FF") for x in (120, 392)])
D["regulator"] = lambda s: (s.F("circle", cx=256, cy=256, r=90, fill="#3A3A44"), s.F("rect", x=226, y=330, width=60, height=60, rx=14, fill="#5A5A66"), s.T("M300 200 C380 160 420 120 440 70", "#3A3A44", 22))
D["dive-computer"] = lambda s: (s.T("M100 256 H412", "#3A3A44", 50), s.F("rect", x=156, y=156, width=200, height=200, rx=40, fill="#3A3A44"), s.F("rect", outline=False, x=184, y=184, width=144, height=144, rx=20, fill="#8FE0C8"))
D["underwater-camera"] = lambda s: (s.F("rect", x=100, y=160, width=312, height=220, rx=40, fill=C["yellow"]), s.F("circle", cx=256, cy=270, r=80, fill="#3A3A44"), s.F("circle", cx=256, cy=270, r=46, fill=C["sky"]),
                                    s.F("rect", x=140, y=120, width=70, height=50, rx=10, fill="#3A3A44"))
D["depth-gauge"] = lambda s: (s.F("circle", cx=256, cy=256, r=190, fill="#3A3A44"), s.F("circle", cx=256, cy=256, r=150, fill=WHITE),
                              [s.M(f"M{arc_pt(256, 256, 130, a)[0]:.0f} {arc_pt(256, 256, 130, a)[1]:.0f} L{arc_pt(256, 256, 110, a)[0]:.0f} {arc_pt(256, 256, 110, a)[1]:.0f}", "#3A3A44", 8) for a in range(150, 391, 30)],
                              s.T("M256 256 L340 180", C["red"], 12), s.F("circle", cx=256, cy=256, r=16, fill="#3A3A44"))
D["diving-flag"] = lambda s: (s.T("M150 470 V70", "#5A6270", 14), s.F("rect", x=158, y=90, width=260, height=180, fill=C["red"]), s.F("polygon", outline=False, points="158,90 190,90 418,250 418,270 386,270 158,110", fill=WHITE))

# ---------------------------------------------------------------- exploration
def sub(s, body=C["yellow"], x=256, y=256, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -256)")
    s.F("path", d="M100 260 L60 220 L60 300Z", fill=shade(body, 0.8))
    s.F("rect", x=80, y=200, width=340, height=130, rx=65, fill=body)
    s.F("rect", x=220, y=140, width=110, height=70, rx=20, fill=body)
    s.T("M290 140 V90 H320", "#5A5A66", 10)
    for cx_ in (200, 290, 370):
        s.F("circle", cx=cx_, cy=265, r=24, fill=C["sky"])
    s.close()


D["submarine"] = lambda s: (tile(s, WATER[2]), sub(s))
D["submersible"] = lambda s: (tile(s, WATER[3]), s.F("rect", x=140, y=150, width=232, height=200, rx=60, fill=WHITE), s.F("circle", cx=330, cy=250, r=60, fill=C["sky"]),
                              s.F("rect", x=160, y=350, width=192, height=30, rx=10, fill=C["orange"]), s.T("M372 300 L430 340", "#5A5A66", 12))
D["bathyscaphe"] = lambda s: (tile(s, WATER[4]), s.F("rect", x=100, y=130, width=312, height=130, rx=60, fill="#E8D06E"), s.F("circle", cx=256, cy=330, r=80, fill="#9AA3AF"), s.F("circle", cx=256, cy=330, r=30, fill=C["sky"]))
D["remotely-operated-vehicle"] = lambda s: (tile(s, WATER[3]), s.F("rect", x=130, y=180, width=252, height=160, rx=20, fill=C["yellow"]), s.F("rect", x=150, y=200, width=212, height=40, fill="#3A3A44"),
                                            s.F("circle", cx=200, cy=300, r=24, fill=C["sky"]), s.F("circle", cx=312, cy=300, r=24, fill=C["sky"]), s.T("M256 180 C256 120 300 80 340 40", "#3A3A44", 8),
                                            s.T("M382 300 L440 340 L470 320", "#5A5A66", 12))
D["research-vessel"] = lambda s: (tile(s, C["sky"]), s.F("rect", outline=False, x=24, y=330, width=464, height=158, fill=WATER[2]), s.F("path", d="M60 280 H452 L420 360 H100Z", fill=WHITE),
                                  s.M("M80 320 H430", C["red"], 12), s.F("rect", x=200, y=200, width=160, height=80, rx=8, fill=WHITE), s.T("M380 280 L440 160 L440 300", "#5A5A66", 8))
D["sonar"] = lambda s: (tile(s, WATER[3]), sub(s, C["yellow"], 140, 256, 0.4), [s.M(f"M{220 + k * 40} {200 - k * 10} C{250 + k * 40} {230} {250 + k * 40} {282} {220 + k * 40} {312 + k * 10}", WHITE, 6) for k in range(4)])
D["ocean-buoy"] = lambda s: (tile(s, C["sky"]), s.F("rect", outline=False, x=24, y=330, width=464, height=158, fill=WATER[2]), s.F("path", d="M190 340 L210 200 H302 L322 340Z", fill=C["red"]),
                             s.M("M200 260 H312", WHITE, 14), s.F("rect", x=240, y=150, width=32, height=50, fill="#5A5A66"), s.F("circle", cx=256, cy=140, r=16, fill=C["yellow"]))
D["underwater-drone"] = lambda s: (tile(s, WATER[2]), s.F("rect", x=140, y=220, width=232, height=90, rx=45, fill=WHITE), [s.F("circle", cx=x, cy=210, r=30, fill="#5A5A66") for x in (160, 352)],
                                   s.F("circle", cx=372, cy=265, r=24, fill=C["sky"]))
D["underwater-habitat"] = lambda s: (tile(s, WATER[3]), seafloor(s, 430), s.F("rect", x=100, y=260, width=312, height=140, rx=70, fill="#C9CED6"), [s.F("circle", cx=x, cy=330, r=26, fill="#FFE38A") for x in (170, 256, 342)],
                                     [s.T(f"M{x} 400 V440", "#5A5A66", 14) for x in (150, 362)])
D["diving-bell"] = lambda s: (tile(s, WATER[2]), s.T("M256 24 V100", "#5A5A66", 10), s.F("path", d="M150 380 C150 180 200 100 256 100 C312 100 362 180 362 380Z", fill="#C98A3E"),
                              s.F("circle", cx=256, cy=230, r=40, fill=C["sky"]), s.F("rect", x=130, y=370, width=252, height=30, rx=8, fill="#8C5A2A"))

# ---------------------------------------------------------------- shells and shore finds
D["seashell"] = lambda s: (s.F("path", d="M256 420 L90 220 C120 100 392 100 422 220Z", fill="#F7C4B0"), [s.M(f"M256 420 L{x:.0f} {y:.0f}", "#E89A80", 8) for x, y in (arc_pt(256, 420, 260, a) for a in range(-150, -29, 15))])
D["conch-shell"] = lambda s: (s.F("path", d="M90 330 C70 250 140 170 240 150 C330 132 400 160 430 200 L476 206 L444 244 C440 300 380 350 300 370 C220 390 110 380 90 330Z", fill="#F4E0C8"),
                              s.F("path", d="M150 340 C200 300 300 290 380 300 C350 330 290 350 230 356 C190 360 160 352 150 340Z", fill="#F7A1B5"),
                              s.M("M170 200 C190 230 190 260 170 290 M230 170 C250 210 250 250 236 290 M300 160 C320 200 320 240 306 280", "#C9A27A", 9))
D["spiral-shell"] = lambda s: (s.F("circle", cx=256, cy=270, r=170, fill="#E8C39E"), s.M("M256 270 C256 230 300 230 300 270 C300 320 210 320 210 270 C210 190 340 190 340 270 C340 360 170 360 170 270", "#B08A60", 12))
D["sand-dollar"] = lambda s: (s.F("circle", cx=256, cy=256, r=180, fill="#F2E3C4"), [s.F("ellipse", outline=False, cx=f"{arc_pt(256, 256, 70, a)[0]:.0f}", cy=f"{arc_pt(256, 256, 70, a)[1]:.0f}", rx=12, ry=34, fill="#D9C39A",
                                                                                               transform=f"rotate({a + 90} {arc_pt(256, 256, 70, a)[0]:.0f} {arc_pt(256, 256, 70, a)[1]:.0f})") for a in range(-90, 270, 72)])
D["pearl"] = lambda s: (s.F("circle", cx=256, cy=256, r=150, fill="#F4F1EA"), s.F("circle", outline=False, cx=210, cy=200, r=40, fill=WHITE))
D["pearl-in-oyster"] = lambda s: (s.F("path", d="M90 300 C80 380 160 420 260 420 C380 420 440 370 430 300Z", fill="#9AA3AF"),
                                  s.F("path", outline=False, d="M120 310 C130 370 200 395 260 395 C350 395 400 360 400 310Z", fill="#E5E7EB"),
                                  s.F("path", d="M90 300 C70 200 200 120 300 140 C390 160 440 230 430 300 C380 270 160 270 90 300Z", fill="#8C96A3"),
                                  s.F("circle", cx=262, cy=340, r=40, fill=WHITE), s.F("circle", outline=False, cx=250, cy=328, r=12, fill="#E8F0FF"))
D["driftwood"] = lambda s: (s.F("path", d="M50 300 C120 260 300 250 440 280 L470 260 L460 300 C400 330 200 340 60 330Z", fill="#B8A890"), s.M("M100 300 C200 290 320 290 420 300", "#8C7A60", 6))
D["seaweed"] = lambda s: [s.T(f"M{x} 470 C{x - 40} 380 {x + 40} 260 {x} 120", c, 24) for x, c in ((180, "#4CB963"), (256, "#2F8A4A"), (332, "#6EB84A"))]
D["kelp"] = lambda s: (s.T("M256 470 C220 360 290 240 256 60", "#6E7A2A", 22), [s.F("ellipse", cx=270 + (k % 2) * -30, cy=y, rx=40, ry=14, fill="#8C9A3A", transform=f"rotate({-30 if k % 2 == 0 else 30} {270 + (k % 2) * -30} {y})") for k, y in enumerate((400, 320, 240, 160, 90))])
D["sea-glass"] = lambda s: [s.F("path", d=f"M{x - 40} {y} L{x - 20} {y - 40} L{x + 30} {y - 30} L{x + 40} {y + 10} L{x} {y + 40}Z", fill=c, fill_opacity="0.85") for x, y, c in ((170, 220, "#7FD4B0"), (320, 200, "#8FD0FF"), (250, 340, "#C8E8A8"))]


if __name__ == "__main__":
    run("ocean-underwater", D, sys.argv[1:] or None)
