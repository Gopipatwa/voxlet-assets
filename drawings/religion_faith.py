"""religion-faith drawings. Run: python drawings/religion_faith.py [ids...]

Never drawn: God, prophets, companions, angels or any sacred figure. People only as faceless
silhouettes (salah positions, crowds). Text and calligraphy tiles come from the text-tile tool.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import *  # noqa: E402,F401,F403
from _parts import place as P  # noqa: E402
from _parts2 import *  # noqa: E402,F401,F403
from draw_lib import C, arc_pt, head, run, star_pts  # noqa: E402

D = {}
K = C  # natural palette
GOLD, GOLDD, BLACKK, WHITEK, GREY = K["gold"], K["darkgold"], K["black"], K["white"], K["grey"]
SAND, SANDD, SKY, GREEN, GREEND = "#EBCB94", K["tan"], K["sky"], K["green"], K["darkgreen"]
STONE, STONED, MARBLE = "#BFA58A", "#8C7560", "#EEF0F3"


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


# ---------------------------------------------------------------- building blocks
def kaaba(s):
    s.F("polygon", points="70,420 268,462 444,420 444,440 268,482 70,440", fill=MARBLE)
    s.F("polygon", points="96,164 268,194 268,444 96,412", fill=BLACKK)
    s.F("polygon", points="268,194 420,162 420,410 268,444", fill="#34343D")
    s.F("polygon", points="96,164 248,138 420,162 268,194", fill="#45454F")
    s.F("polygon", points="96,226 268,256 268,282 96,252", fill=GOLD)
    s.F("polygon", points="268,256 420,224 420,250 268,282", fill=GOLDD)
    s.F("polygon", points="326,308 384,296 384,392 326,404", fill=GOLD)
    s.M("M120 239 L150 244 M180 249 L210 254 M240 254 L255 257", GOLDD, 5)
    s.M("M290 266 L310 262 M340 256 L360 252 M390 245 L405 242", "#8A5C0E", 5)


def dome(s, cx, base, r, color=GREY, finial=True, onion=False):
    if onion:
        s.F("path", d=f"M{cx - r} {base} C{cx - r} {base - r * 0.9} {cx - r * 0.3} {base - r * 1.1} {cx} {base - r * 1.6} "
                      f"C{cx + r * 0.3} {base - r * 1.1} {cx + r} {base - r * 0.9} {cx + r} {base}Z", fill=color)
    else:
        s.F("path", d=f"M{cx - r} {base} A{r} {r} 0 0 1 {cx + r} {base}Z", fill=color)
    if finial:
        top = base - (r * 1.6 if onion else r)
        s.T(f"M{cx} {top} V{top - r * 0.35}", GOLD, max(4, r * 0.08))
        s.F("circle", cx=cx, cy=top - r * 0.42, r=max(4, r * 0.1), fill=GOLD)


def minaret(s, x, base, h, w=26, color=MARBLE, cap=GREY):
    s.F("rect", x=x - w / 2, y=base - h, width=w, height=h, fill=color)
    s.F("rect", x=x - w * 0.8, y=base - h * 0.62, width=w * 1.6, height=w * 0.45, rx=3, fill=color)
    s.F("rect", x=x - w * 0.7, y=base - h - w * 0.4, width=w * 1.4, height=w * 0.45, rx=3, fill=color)
    s.F("polygon", points=f"{x - w * 0.55},{base - h - w * 0.4} {x + w * 0.55},{base - h - w * 0.4} {x},{base - h - w * 2.2}", fill=cap)
    s.F("circle", cx=x, cy=base - h - w * 2.35, r=w * 0.18, fill=GOLD)


def arches(s, x0, x1, y, h, n, color=MARBLE, inner="#8FA6C9"):
    s.F("rect", x=x0, y=y - h, width=x1 - x0, height=h, fill=color)
    w = (x1 - x0) / n
    for i in range(n):
        ax = x0 + i * w + w * 0.18
        aw = w * 0.64
        s.F("path", outline=False, d=f"M{ax:.0f} {y} V{y - h * 0.5:.0f} C{ax:.0f} {y - h * 0.8:.0f} {ax + aw / 2:.0f} {y - h * 0.86:.0f} {ax + aw / 2:.0f} {y - h * 0.9:.0f} "
                                     f"C{ax + aw / 2:.0f} {y - h * 0.86:.0f} {ax + aw:.0f} {y - h * 0.8:.0f} {ax + aw:.0f} {y - h * 0.5:.0f} V{y}Z", fill=inner)


def mosque(s, body=MARBLE, dome_c=GREY, main=110, side=True, minarets=2, onion=False):
    s.F("rect", outline=False, x=30, y=440, width=452, height=20, fill="none")
    if minarets >= 2:
        minaret(s, 70, 440, 260); minaret(s, 442, 440, 260)
    if minarets in (1, 4):
        minaret(s, 442, 440, 260)
    s.F("rect", x=110, y=300, width=292, height=140, fill=body)
    if side:
        dome(s, 150, 300, 40, dome_c); dome(s, 362, 300, 40, dome_c)
    dome(s, 256, 300, main, dome_c, onion=onion)
    s.F("path", d="M226 440 V380 C226 350 286 350 286 380 V440Z", fill="#8FA6C9")
    for x in (150, 362):
        s.F("path", d=f"M{x - 18} 400 V370 C{x - 18} 350 {x + 18} 350 {x + 18} 370 V400Z", fill="#8FA6C9")


def crescent(s, cx, cy, r, color=GOLD, bg=None):
    outer = [arc_pt(cx, cy, r, a) for a in range(60, 301, 10)]
    ic, ir = cx + r * 0.42, r * 0.78
    inner = [arc_pt(ic, cy, ir, a) for a in range(290, 69, -10)]
    pts = outer + inner
    s.F("polygon", points=" ".join(f"{x:.1f},{y:.1f}" for x, y in pts), fill=color)


def hills(s, color=STONE, dark=STONED, peaks=((60, 300), (180, 170), (300, 230), (440, 300))):
    pts = "30,460 " + " ".join(f"{x},{y}" for x, y in peaks) + " 482,460"
    s.F("polygon", points=pts, fill=color)
    s.F("polygon", outline=False, points=f"{peaks[1][0]},{peaks[1][1]} {peaks[1][0] - 40},{peaks[1][1] + 120} {peaks[1][0] + 20},{peaks[1][1] + 60}", fill=dark)


def ground(s, color=SAND, y=400):
    s.F("rect", x=20, y=y, width=472, height=470 - y, rx=20, fill=color)


def sky_bg(s, color=SKY):
    s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill=color)


# faceless silhouette figures for prayer positions (one colour, no face)
SIL = "#3D6FB6"


def sil(s, pose, x=256, y=470, sc=1.0, color=SIL, white=False):
    """Faceless figure. Coordinates of a 300-tall figure with feet at (0, 0)."""
    c = WHITEK if white else color
    J = {
        "stand": dict(head=(0, -270), body=[(0, -235), (0, -110)], legs=[(0, -110, -14, 0), (0, -110, 14, 0)], arms=[(0, -215, -10, -150, 0, -150), (0, -215, 10, -150, 0, -150)]),
        "takbir": dict(head=(0, -270), body=[(0, -235), (0, -110)], legs=[(0, -110, -14, 0), (0, -110, 14, 0)], arms=[(0, -215, -40, -230, -34, -275), (0, -215, 40, -230, 34, -275)]),
        "arms-down": dict(head=(0, -270), body=[(0, -235), (0, -110)], legs=[(0, -110, -14, 0), (0, -110, 14, 0)], arms=[(0, -215, -24, -160, -26, -110), (0, -215, 24, -160, 26, -110)]),
        "ruku": dict(head=(110, -200), body=[(80, -190), (-20, -180)], legs=[(-20, -180, -26, 0), (-20, -180, -6, 0)], arms=[(60, -188, 70, -120, 66, -96), (60, -188, 50, -120, 46, -96)]),
        "sujood": dict(head=(120, -24), body=[(90, -50), (-40, -120)], legs=[(-40, -120, -70, -40, -150, -20), (-40, -120, -60, -40, -140, -14)], arms=[(70, -60, 100, -30, 110, -4), (70, -60, 80, -30, 90, -4)]),
        "sit": dict(head=(10, -170), body=[(10, -135), (0, -40)], legs=[(0, -40, 70, -20, 80, 0), (0, -40, -60, -10, -110, 0)], arms=[(10, -120, 40, -70, 70, -50), (10, -120, 30, -70, 60, -46)]),
        "tashahhud": dict(head=(10, -170), body=[(10, -135), (0, -40)], legs=[(0, -40, 70, -20, 80, 0), (0, -40, -60, -10, -110, 0)], arms=[(10, -120, 40, -70, 70, -50), (10, -120, 40, -80, 76, -84)]),
        "taslim": dict(head=(22, -168), body=[(10, -135), (0, -40)], legs=[(0, -40, 70, -20, 80, 0), (0, -40, -60, -10, -110, 0)], arms=[(10, -120, 40, -70, 70, -50), (10, -120, 30, -70, 60, -46)]),
    }[pose]
    s.open(transform=f"translate({x} {y}) scale({sc})")
    for leg in J["legs"]:
        if len(leg) == 4:
            s.M(f"M{leg[0]} {leg[1]} L{leg[2]} {leg[3]}", c, 34)
        else:
            s.M(f"M{leg[0]} {leg[1]} L{leg[2]} {leg[3]} L{leg[4]} {leg[5]}", c, 32)
    (bx1, by1), (bx2, by2) = J["body"]
    s.M(f"M{bx1} {by1} L{bx2} {by2}", c, 62)
    for a in J["arms"]:
        s.M(f"M{a[0]} {a[1]} L{a[2]} {a[3]} L{a[4]} {a[5]}", c, 22)
    hx, hy = J["head"]
    s.raw(f'<circle cx="{hx}" cy="{hy}" r="30" fill="{c}"/>')
    if white:
        s.raw(f'<circle cx="{hx}" cy="{hy}" r="30" fill="none" stroke="{SIL}" stroke-width="6"/>')
    s.close()


def mat(s, x, y, w=220, h=60, color=K["red"]):
    s.F("rect", x=x - w / 2, y=y, width=w, height=h, rx=8, fill=color)
    s.M(f"M{x - w / 2 + 14} {y + h / 2} H{x + w / 2 - 14}", GOLD, 4)


def drops(s, pts, color=K["sky"]):
    for x, y in pts:
        s.F("path", d=f"M{x} {y} C{x} {y} {x - 12} {y + 18} {x - 12} {y + 26} C{x - 12} {y + 38} {x + 12} {y + 38} {x + 12} {y + 26} C{x + 12} {y + 18} {x} {y} {x} {y}Z", fill=color)


def tap(s, x=256, y=120):
    s.F("path", d=f"M{x - 120} {y} H{x + 20} C{x + 60} {y} {x + 70} {y + 30} {x + 70} {y + 60} V{y + 80} H{x + 30} V{y + 60} C{x + 30} {y + 44} {x + 24} {y + 40} {x + 14} {y + 40} H{x - 120}Z", fill=GREY)
    s.F("rect", x=x - 60, y=y - 30, width=30, height=34, rx=6, fill=GREY)


def hand(s, x, y, sc=1.0, flip=False, color=SKIN):
    s.open(transform=f"translate({x} {y}) scale({-sc if flip else sc} {sc})")
    s.F("path", d="M-40 80 C-60 40 -66 0 -60 -30 C-56 -46 -36 -44 -36 -26 V-70 C-36 -84 -16 -84 -16 -70 V-86 C-16 -100 4 -100 4 -86 V-78 "
                  "C4 -92 24 -92 24 -78 V-60 C24 -72 44 -72 44 -60 V10 C44 40 30 70 20 80 Z", fill=color)
    s.close()


def face_blank(s, x=256, y=220, r=110, hair=True):
    s.F("circle", cx=x, cy=y, r=r, fill=SKIN)
    if hair:
        s.F("path", d=f"M{x - r} {y - 10} C{x - r} {y - r * 1.2} {x + r} {y - r * 1.2} {x + r} {y - 10} C{x + r * 0.6} {y - r * 0.6} {x - r * 0.6} {y - r * 0.6} {x - r} {y - 10}Z", fill="#4A3B32")


def camel(s, color=K["tan"]):
    s.F("path", d="M100 300 C100 220 150 180 190 220 C220 150 290 160 310 230 C330 250 340 270 330 300 Z", fill=color)
    for x in (130, 170, 280, 310):
        s.T(f"M{x} 296 V430", color, 22)
    s.T("M320 270 C350 240 360 190 370 150", color, 30)
    s.F("ellipse", cx=390, cy=146, rx=34, ry=20, fill=color)
    s.F("circle", outline=False, cx=396, cy=140, r=5, fill=DARK)


def sheep(s, color=WHITEK):
    for cx, cy in ((180, 260), (240, 240), (300, 250), (330, 290), (260, 300), (190, 300)):
        s.F("circle", cx=cx, cy=cy, r=48, fill=color)
    s.F("ellipse", cx=370, cy=230, rx=40, ry=30, fill=K["darkgrey"])
    for x in (190, 230, 280, 320):
        s.T(f"M{x} 330 V420", K["darkgrey"], 16)
    s.T("M360 210 C380 180 410 190 400 220", K["tan"], 12)


def flames(s, cx=256, base=420, w=300, h=260):
    for dx, sc, col in ((-0.3, 0.7, K["orange"]), (0.3, 0.7, K["orange"]), (0, 1.0, K["red"]), (0, 0.6, K["yellow"])):
        hw = w / 2 * sc
        x = cx + dx * w
        s.F("path", d=f"M{x} {base} C{x - hw} {base} {x - hw} {base - h * sc * 0.4} {x - hw * 0.5} {base - h * sc * 0.7} C{x - hw * 0.2} {base - h * sc * 0.5} "
                      f"{x - hw * 0.1} {base - h * sc * 0.8} {x} {base - h * sc} C{x + hw * 0.4} {base - h * sc * 0.6} {x + hw} {base - h * sc * 0.4} {x + hw} {base - h * sc * 0.15} "
                      f"C{x + hw} {base} {x + hw * 0.5} {base} {x} {base}Z", fill=col)


def book_closed(s, color=GREEND, x=256, y=256, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -256)")
    s.F("rect", x=130, y=90, width=252, height=332, rx=14, fill=color)
    s.F("rect", outline=False, x=360, y=100, width=16, height=312, fill=K["cream"])
    s.F("rect", x=160, y=130, width=180, height=252, rx=10, fill="none", stroke_=None)
    s.raw(f'<rect x="162" y="130" width="176" height="252" rx="10" fill="none" stroke="{GOLD}" stroke-width="8"/>')
    s.F("polygon", outline=False, points=star_pts(250, 256, 50, 36, 8, -90), fill=GOLD)
    s.F("polygon", outline=False, points=star_pts(250, 256, 30, 22, 8, -90), fill=color)
    s.close()


def book_open_q(s, x=256, y=256, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -256)")
    s.F("path", d="M256 150 C210 120 130 114 60 130 V390 C130 374 210 380 256 410 Z", fill=K["cream"])
    s.F("path", d="M256 150 C302 120 382 114 452 130 V390 C382 374 302 380 256 410 Z", fill=K["cream"])
    for yy in (190, 230, 270, 310, 350):
        s.M(f"M96 {yy} C140 {yy - 10} 190 {yy - 6} 230 {yy + 6} M282 {yy + 6} C322 {yy - 6} 372 {yy - 10} 416 {yy}", K["darkgreen"], 6)
    s.raw(f'<rect x="80" y="140" width="0" height="0"/>')
    s.close()


def rehal(s, x=256, y=300, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -300)")
    s.T("M120 200 L380 430 M392 200 L132 430", K["brown"], 34)
    s.F("circle", cx=256, cy=318, r=16, fill=K["darkbrown"])
    s.close()


# ---------------------------------------------------------------- islamic holy places (keep)
D["kaaba"] = kaaba


@reg("masjid-al-haram")
def _(s):
    sky_bg(s)
    s.F("ellipse", cx=256, cy=420, rx=230, ry=50, fill=MARBLE)
    arches(s, 40, 472, 330, 110, 9)
    for x, h in ((60, 250), (140, 280), (372, 280), (452, 250)):
        minaret(s, x, 330, h, 20)
    P(s, kaaba, 256, 360, 0.42)


@reg("masjid-an-nabawi")
def _(s):
    sky_bg(s)
    arches(s, 40, 472, 440, 130, 8)
    minaret(s, 70, 310, 200, 24); minaret(s, 442, 310, 200, 24)
    s.F("rect", x=190, y=230, width=132, height=80, fill=MARBLE)
    dome(s, 256, 230, 70, K["green"])
    dome(s, 360, 310, 34, GREY); dome(s, 150, 310, 34, GREY)


D["green-dome"] = lambda s: (s.F("rect", x=126, y=320, width=260, height=120, fill=MARBLE), dome(s, 256, 320, 130, K["green"]),
                             s.F("path", outline=False, d="M170 300 C180 250 210 220 240 210 C220 240 210 270 206 310Z", fill="#7FD493"))


@reg("al-aqsa-mosque")
def _(s):
    sky_bg(s)
    s.F("rect", x=60, y=280, width=392, height=160, fill="#D9CBB0")
    arches(s, 60, 452, 440, 90, 7, "#D9CBB0", "#7A6A55")
    s.F("rect", x=200, y=230, width=112, height=50, fill="#D9CBB0")
    dome(s, 256, 230, 66, "#8D98A6")
    minaret(s, 420, 280, 160, 22, "#D9CBB0", "#8D98A6")


@reg("dome-of-the-rock")
def _(s):
    sky_bg(s)
    s.F("polygon", points="80,440 80,320 150,290 362,290 432,320 432,440", fill="#2D5FA8")
    s.F("rect", outline=False, x=80, y=360, width=352, height=24, fill=LIGHT)
    for x in range(110, 420, 50):
        s.F("path", outline=False, d=f"M{x} 440 V410 C{x} 396 {x + 26} 396 {x + 26} 410 V440Z", fill="#1B3F78")
    s.F("rect", x=176, y=230, width=160, height=60, fill="#2D5FA8")
    dome(s, 256, 230, 104, GOLD)
    s.F("path", outline=False, d="M180 210 C190 170 210 150 240 140 C220 170 210 190 206 220Z", fill="#F7D57A")


D["quba-mosque"] = lambda s: (sky_bg(s), mosque(s, minarets=4, main=80), dome(s, 200, 300, 34, MARBLE), dome(s, 312, 300, 34, MARBLE))


def cave_mountain(s, color=STONE, mouth=(256, 300)):
    sky_bg(s)
    s.F("polygon", points="30,460 150,180 230,120 330,170 420,260 482,460", fill=color)
    s.F("polygon", outline=False, points="230,120 180,250 260,200", fill=STONED)
    x, y = mouth
    s.F("path", d=f"M{x - 60} {y + 60} C{x - 60} {y - 20} {x + 60} {y - 20} {x + 60} {y + 60}Z", fill="#3A2E28")


D["cave-hira"] = lambda s: (cave_mountain(s, mouth=(240, 170)), s.F("circle", cx=400, cy=110, r=26, fill=K["yellow"]))
D["cave-thawr"] = lambda s: cave_mountain(s, "#A58B70", (300, 300))
D["mount-uhud"] = lambda s: (sky_bg(s), hills(s, "#B8735A", "#8E5440", ((40, 320), (140, 200), (220, 240), (310, 170), (400, 230), (470, 320))), ground(s, SAND, 420))


@reg("mount-arafat")
def _(s):
    sky_bg(s)
    s.F("polygon", points="60,460 256,230 452,460", fill=STONE)
    s.F("rect", x=244, y=120, width=24, height=120, fill=MARBLE)
    ground(s, SAND, 430)
    for x in range(60, 460, 26):
        s.F("circle", outline=False, cx=x, cy=440 + (x % 3) * 6, r=8, fill=WHITEK)


D["mount-nur"] = lambda s: (sky_bg(s), s.F("polygon", points="40,460 200,260 256,100 312,250 472,460", fill="#9C7B60"),
                            s.F("polygon", outline=False, points="256,100 220,260 280,200", fill=STONED))


@reg("mina-tents")
def _(s):
    sky_bg(s)
    hills(s, STONE, STONED, ((40, 260), (140, 200), (260, 230), (380, 190), (470, 260)))
    for r in range(3):
        for c in range(7):
            x, y = 60 + c * 64 + (r % 2) * 32, 330 + r * 48
            s.F("polygon", points=f"{x - 28},{y + 30} {x},{y - 10} {x + 28},{y + 30}", fill=WHITEK)


D["muzdalifah"] = lambda s: (sky_bg(s, "#1E2A4A"), [s.F("circle", outline=False, cx=x, cy=y, r=4, fill=WHITEK) for x, y in ((90, 90), (200, 70), (330, 110), (420, 80), (150, 150), (380, 170))],
                             crescent(s, 380, 120, 34), ground(s, SAND, 340), [s.F("circle", outline=False, cx=90 + (i * 47) % 340, cy=380 + (i * 31) % 70, r=7, fill=STONED) for i in range(30)])


@reg("jamarat")
def _(s):
    sky_bg(s)
    for y in (360, 260, 160):
        s.F("rect", x=40, y=y, width=432, height=30, fill=MARBLE)
        for x in (60, 200, 340, 450):
            s.F("rect", outline=False, x=x, y=y + 30, width=14, height=70, fill=GREY)
    s.F("rect", x=226, y=110, width=60, height=330, rx=8, fill="#8C7560")


@reg("safa-and-marwa")
def _(s):
    arches(s, 40, 472, 400, 180, 7)
    s.F("path", d="M40 400 C60 340 110 330 140 400Z", fill=STONE)
    s.F("path", d="M372 400 C400 340 450 330 472 400Z", fill=STONE)
    s.M("M160 430 H350 " + head(350, 430, 0, 30) + " M352 452 H162 " + head(162, 452, 180, 30), "#4CB963", 8)


D["badr-battlefield"] = lambda s: (sky_bg(s), hills(s, "#C89B6A", "#A57A4E", ((40, 300), (130, 230), (220, 270), (330, 220), (470, 300))), ground(s, SAND, 360),
                                   s.F("rect", x=360, y=320, width=60, height=30, rx=4, fill=MARBLE))


@reg("jannat-al-baqi")
def _(s):
    sky_bg(s)
    ground(s, SAND, 300)
    s.F("rect", x=40, y=270, width=432, height=40, fill="#D9CBB0")
    for r in range(3):
        for c in range(7):
            s.F("rect", x=70 + c * 58 + (r % 2) * 20, y=340 + r * 40, width=14, height=24, rx=4, fill=STONED)


D["masjid-al-qiblatayn"] = lambda s: (sky_bg(s), mosque(s, main=70, side=False), dome(s, 330, 300, 60, GREY), dome(s, 190, 300, 60, GREY))


@reg("zamzam-well")
def _(s):
    s.F("ellipse", cx=256, cy=200, rx=170, ry=50, fill=STONED)
    s.F("path", d="M86 200 V380 C86 420 426 420 426 380 V200 C426 250 86 250 86 200Z", fill=STONE)
    s.F("ellipse", outline=False, cx=256, cy=200, rx=140, ry=36, fill="#3D8BFD")
    for x in range(110, 420, 50):
        s.M(f"M{x} 260 V380", STONED, 4)
    drops(s, ((256, 120), (210, 140), (300, 140)), "#8FD0FF")


@reg("black-stone")
def _(s):
    s.F("ellipse", cx=256, cy=256, rx=170, ry=200, fill=K["grey"])
    s.F("ellipse", cx=256, cy=256, rx=120, ry=150, fill="#D0D4DA")
    s.F("ellipse", cx=256, cy=256, rx=80, ry=100, fill=BLACKK)
    for x, y in ((236, 230), (270, 270), (250, 300)):
        s.F("circle", outline=False, cx=x, cy=y, r=12, fill="#3A3A44")


@reg("maqam-ibrahim")
def _(s):
    s.F("rect", x=150, y=400, width=212, height=40, rx=8, fill=MARBLE)
    s.F("path", d="M180 400 V250 C180 170 332 170 332 250 V400Z", fill="#D8E6F2")
    s.M("M206 400 V230 M236 400 V200 M276 400 V200 M306 400 V230 M180 300 H332", GOLD, 8)
    s.F("path", d="M190 210 C210 150 302 150 322 210 Z", fill=GOLD)
    s.F("circle", cx=256, cy=146, r=12, fill=GOLD)


@reg("kiswah")
def _(s):
    s.F("path", d="M100 80 H412 V420 C360 440 300 430 256 440 C212 430 152 440 100 420Z", fill=BLACKK)
    s.F("rect", x=100, y=150, width=312, height=50, fill=GOLD)
    for x in range(120, 400, 46):
        s.F("polygon", outline=False, points=star_pts(x + 10, 175, 16, 10, 8), fill=GOLDD)
    s.M("M140 280 C180 260 220 300 256 280 C292 260 332 300 372 280", "#3A3A44", 6)


# ---------------------------------------------------------------- mosque parts
D["mosque"] = lambda s: mosque(s)
D["mosque-silhouette"] = lambda s: (mosque(s, body=DARK, dome_c=DARK), crescent(s, 400, 110, 30))
D["minaret"] = lambda s: minaret(s, 256, 460, 300, 60)
D["mosque-dome"] = lambda s: (s.F("rect", x=96, y=320, width=320, height=120, fill=MARBLE), dome(s, 256, 320, 150, K["blue"]), crescent(s, 270, 96, 22))


@reg("mihrab")
def _(s):
    s.F("rect", x=96, y=60, width=320, height=400, rx=10, fill="#D9CBB0")
    s.F("path", d="M150 460 V220 C150 140 256 100 256 100 C256 100 362 140 362 220 V460Z", fill=GOLD)
    s.F("path", d="M180 460 V230 C180 170 256 136 256 136 C256 136 332 170 332 230 V460Z", fill=K["darkblue"])
    for y in (260, 320, 380):
        s.F("polygon", outline=False, points=star_pts(256, y, 20, 12, 8), fill=GOLD)


@reg("minbar")
def _(s):
    s.F("polygon", points="100,450 100,380 160,380 160,320 220,320 220,260 280,260 280,450", fill=K["brown"])
    s.F("rect", x=280, y=180, width=100, height=270, fill=K["darkbrown"])
    s.F("path", d="M280 180 C280 120 380 120 380 180Z", fill=GOLD)
    s.M("M100 380 L280 200", K["darkbrown"], 12)


D["mosque-courtyard"] = lambda s: (sky_bg(s), arches(s, 40, 472, 300, 150, 6), s.F("rect", outline=False, x=20, y=300, width=472, height=170, fill=MARBLE),
                                   s.F("ellipse", cx=256, cy=380, rx=80, ry=30, fill="#8FD0FF"), s.F("rect", x=244, y=320, width=24, height=60, fill=GREY))


@reg("wudu-area")
def _(s):
    s.F("rect", x=40, y=120, width=432, height=200, rx=10, fill=MARBLE)
    for x in (110, 210, 310, 410):
        tap_small = f"M{x - 20} 150 H{x + 10} V200"
        s.T(tap_small, GREY, 14)
        drops(s, ((x + 10, 215),))
    s.F("rect", x=40, y=320, width=432, height=40, rx=8, fill=STONE)
    s.F("rect", x=60, y=400, width=392, height=30, rx=8, fill=K["brown"])


D["prayer-hall"] = lambda s: (arches(s, 30, 482, 300, 220, 5, MARBLE, "#B9C8DC"), s.F("rect", outline=False, x=30, y=300, width=452, height=170, fill=K["darkred"]),
                              [s.M(f"M30 {y} H482", GOLD, 4) for y in (340, 380, 420, 460)])


@reg("mosque-lamp")
def _(s):
    s.T("M256 30 V110", GOLDD, 6)
    s.F("path", d="M196 110 H316 L346 190 C346 300 296 360 256 380 C216 360 166 300 166 190Z", fill=GOLD)
    s.F("path", outline=False, d="M206 190 H306 C306 280 280 320 256 336 C232 320 206 280 206 190Z", fill="#FFE38A")
    s.F("polygon", outline=False, points=star_pts(256, 250, 30, 18, 8), fill=GOLD)
    s.F("circle", cx=256, cy=400, r=14, fill=GOLD)


D["mosque-door"] = lambda s: (s.F("path", d="M120 460 V220 C120 120 256 70 256 70 C256 70 392 120 392 220 V460Z", fill=GOLD),
                              s.F("path", d="M150 460 V230 C150 150 256 110 256 110 C256 110 362 150 362 230 V460Z", fill=K["brown"]),
                              s.M("M256 120 V460", K["darkbrown"], 8), s.F("circle", cx=236, cy=320, r=10, fill=GOLD), s.F("circle", cx=276, cy=320, r=10, fill=GOLD))
D["islamic-arch"] = lambda s: (s.F("path", d="M80 460 V230 C80 130 256 60 256 60 C256 60 432 130 432 230 V460 H370 V240 C370 170 256 120 256 120 C256 120 142 170 142 240 V460Z", fill=K["blue"]),
                               [s.F("polygon", outline=False, points=star_pts(x, y, 12, 7, 8), fill=GOLD) for x, y in ((110, 300), (110, 380), (400, 300), (400, 380), (256, 90))])

# ---------------------------------------------------------------- islamic objects
D["quran"] = lambda s: book_closed(s)
D["open-quran"] = lambda s: book_open_q(s)
D["quran-on-rehal"] = lambda s: (rehal(s, 256, 300, 1.0), book_open_q(s, 256, 230, 0.8))
D["rehal"] = lambda s: rehal(s)


@reg("prayer-mat")
def _(s):
    s.F("rect", x=130, y=50, width=252, height=412, rx=14, fill=K["darkred"])
    s.F("rect", outline=False, x=150, y=70, width=212, height=372, rx=8, fill=K["red"])
    s.F("path", d="M190 400 V200 C190 140 256 110 256 110 C256 110 322 140 322 200 V400Z", fill=K["darkred"])
    s.F("polygon", outline=False, points=star_pts(256, 260, 30, 18, 8), fill=GOLD)
    s.M("M150 430 H362", GOLD, 6)
    for x in range(140, 380, 20):
        s.M(f"M{x} 462 V480 M{x} 50 V32", GOLD, 4)


@reg("tasbih")
def _(s):
    for i in range(33):
        a = i * 360 / 36 + 90
        x, y = arc_pt(256, 220, 150, a)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=17, fill=K["darkred"] if i % 11 else GOLD)
    s.T("M256 370 V420", GOLD, 10)
    s.F("path", d="M240 420 H272 L266 470 H246Z", fill=GOLD)


D["crescent-and-star"] = lambda s: (crescent(s, 220, 256, 170, K["darkgreen"]), s.F("polygon", points=star_pts(350, 230, 60, 24, 5), fill=GOLD))


@reg("qibla-compass")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=GOLD)
    s.F("circle", cx=256, cy=256, r=150, fill=MARBLE)
    s.open("part-needle", "256 256")
    s.F("polygon", points="256,256 236,250 300,130 276,262", fill=K["red"])
    s.F("polygon", points="256,256 276,262 212,382 236,250", fill=GREY)
    s.close()
    P(s, kaaba, 300, 130, 0.13)
    s.F("circle", cx=256, cy=256, r=14, fill=GOLDD)


D["prayer-times-clock"] = lambda s: (s.F("rect", x=60, y=90, width=392, height=330, rx=24, fill=K["darkbrown"]), s.F("rect", x=86, y=116, width=340, height=150, rx=12, fill=GOLD),
                                     P(s, clock, 256, 190, 0.32), [s.F("rect", x=96 + i * 56, y=300, width=46, height=90, rx=8, fill="#1F1F24") for i in range(6)],
                                     [s.M(f"M{106 + i * 56} 330 H{132 + i * 56} M{106 + i * 56} 360 H{132 + i * 56}", "#FF6A3D", 6) for i in range(6)])
D["miswak"] = lambda s: (s.T("M120 400 L392 128", K["tan"], 40), s.M("M380 116 L420 96 M392 128 L432 120 M370 104 L388 72", K["cream"], 8))
D["attar"] = lambda s: (s.F("path", d="M196 200 C150 230 140 300 160 360 C176 410 336 410 352 360 C372 300 362 230 316 200Z", fill="#E6B84A"),
                        s.F("rect", x=226, y=150, width=60, height=60, rx=6, fill=GOLD), s.F("path", d="M240 150 C230 90 282 90 272 150Z", fill=GOLD),
                        s.F("path", outline=False, d="M190 260 C186 300 196 340 210 360 C200 320 198 290 206 250Z", fill="#F7D57A"))
D["sadaqah-box"] = lambda s: (s.F("rect", x=110, y=200, width=292, height=230, rx=20, fill=K["darkgreen"]), s.F("rect", x=90, y=180, width=332, height=40, rx=12, fill=GREEN),
                              s.F("rect", outline=False, x=206, y=190, width=100, height=16, rx=6, fill=DARK),
                              s.F("circle", cx=256, cy=120, r=44, fill=GOLD), s.F("circle", outline=False, cx=256, cy=120, r=28, fill="#F7D57A"),
                              P(s, heart, 256, 320, 0.25, color=K["red"]))
D["zakat"] = lambda s: (hand(s, 256, 380, 1.5), [(s.F("circle", cx=x, cy=y, r=40, fill=GOLD), s.F("circle", outline=False, cx=x, cy=y, r=26, fill="#F7D57A"))
                                                  for x, y in ((210, 200), (300, 180), (256, 120))])
D["zamzam-water"] = lambda s: (s.F("path", d="M190 110 H322 V160 C360 180 370 220 370 260 V430 C370 446 358 456 342 456 H170 C154 456 142 446 142 430 V260 C142 220 152 180 190 160Z", fill="#D9EEFB"),
                               s.F("rect", outline=False, x=150, y=300, width=212, height=150, fill="#8FD0FF"), s.F("rect", x=200, y=80, width=112, height=40, rx=8, fill=K["blue"]),
                               s.F("rect", x=170, y=220, width=172, height=60, rx=8, fill=K["darkgreen"]))


@reg("islamic-geometric-pattern")
def _(s):
    s.F("rect", x=56, y=56, width=400, height=400, rx=20, fill=K["darkblue"])
    for r in range(4):
        for c in range(4):
            x, y = 106 + c * 100, 106 + r * 100
            s.F("polygon", outline=False, points=star_pts(x, y, 46, 30, 8, -90 + 22.5), fill=GOLD)
            s.F("polygon", outline=False, points=star_pts(x, y, 24, 16, 8, -90 + 22.5), fill=K["blue"])


D["rub-el-hizb"] = lambda s: (s.F("rect", x=126, y=126, width=260, height=260, fill=K["darkgreen"]), s.F("rect", x=126, y=126, width=260, height=260, fill=K["darkgreen"], transform="rotate(45 256 256)"),
                              s.F("circle", cx=256, cy=256, r=70, fill=GOLD))

# ---------------------------------------------------------------- wudu steps (faceless)
D["wudu"] = lambda s: (tap(s, 256, 110), drops(s, ((300, 210), (290, 260))), hand(s, 210, 380, 1.1), hand(s, 330, 380, 1.1, flip=True))
D["wudu-intention"] = lambda s: (face_blank(s, 256, 200, 100), s.F("path", d="M140 460 C140 360 190 330 256 330 C322 330 372 360 372 460Z", fill=K["blue"]),
                                 P(s, heart, 256, 400, 0.2, color=K["red"]))
D["wudu-washing-hands"] = lambda s: (tap(s, 256, 100), drops(s, ((300, 200), (290, 250))), hand(s, 230, 370, 1.1, False), hand(s, 300, 370, 1.1, True))
D["wudu-rinsing-mouth"] = lambda s: (face_blank(s, 256, 230, 110), s.F("ellipse", cx=256, cy=270, rx=26, ry=14, fill=K["darkred"]), hand(s, 330, 360, 0.9, True), drops(s, ((330, 280),)))
D["wudu-rinsing-nose"] = lambda s: (face_blank(s, 256, 230, 110), s.F("path", d="M256 200 L240 260 H272Z", fill="#E0A878"), hand(s, 320, 330, 0.9, True), drops(s, ((300, 250),)))
D["wudu-washing-face"] = lambda s: (face_blank(s, 256, 220, 110), hand(s, 150, 300, 1.0), hand(s, 362, 300, 1.0, True), drops(s, ((210, 140), (300, 130), (256, 340))))
D["wudu-washing-arms"] = lambda s: (s.T("M100 360 L380 220", SKIN, 70), hand(s, 400, 200, 0.9, True), drops(s, ((180, 260), (260, 220), (330, 190))))
D["wudu-wiping-head"] = lambda s: (face_blank(s, 256, 280, 120), hand(s, 256, 130, 1.0), drops(s, ((180, 150),)))
D["wudu-wiping-ears"] = lambda s: (face_blank(s, 256, 256, 110, hair=True), s.F("ellipse", cx=146, cy=262, rx=22, ry=34, fill=SKIN), s.F("ellipse", cx=366, cy=262, rx=22, ry=34, fill=SKIN),
                                   hand(s, 120, 300, 0.7), hand(s, 392, 300, 0.7, True))
D["wudu-washing-feet"] = lambda s: (s.F("path", d="M140 300 C140 260 200 250 230 280 L330 380 C350 400 340 430 310 430 H150 C130 430 120 410 130 380Z", fill=SKIN),
                                    tap(s, 300, 110), drops(s, ((344, 210), (330, 260), (240, 300))))


@reg("wudu-steps-chart")
def _(s):
    s.F("rect", x=40, y=40, width=432, height=432, rx=30, fill=LIGHT)
    steps = [D["wudu-washing-hands"], D["wudu-rinsing-mouth"], D["wudu-rinsing-nose"], D["wudu-washing-face"], D["wudu-washing-arms"],
             D["wudu-wiping-head"], D["wudu-wiping-ears"], D["wudu-washing-feet"], D["wudu-intention"]]
    for i, fn in enumerate(steps):
        x, y = 110 + (i % 3) * 146, 110 + (i // 3) * 146
        s.open(transform=f"translate({x} {y}) scale(0.24) translate(-256 -256)")
        fn(s)
        s.close()

# ---------------------------------------------------------------- salah positions (faceless figures, side view)
THOBE, CAP = "#F4F1EA", WHITEK


def _head(s, x, y, cap_side="top", r=40):
    s.F("circle", cx=x, cy=y, r=r, fill=SKIN)
    if cap_side == "top":
        s.F("path", d=f"M{x - r} {y - 6} C{x - r} {y - r * 1.25} {x + r} {y - r * 1.25} {x + r} {y - 6}Z", fill=CAP)
    elif cap_side == "front":   # head pointing right (bowing)
        s.F("path", d=f"M{x + 6} {y - r} C{x + r * 1.25} {y - r} {x + r * 1.25} {y + r} {x + 6} {y + r}Z", fill=CAP)
    elif cap_side == "down":    # head on the ground, top of head pointing right/down
        s.F("path", d=f"M{x - 4} {y - r} C{x + r * 1.2} {y - r * 0.9} {x + r * 1.15} {y + r * 0.6} {x + r * 0.5} {y + r * 0.9}Z", fill=CAP)


def worshipper(s, pose="qiyam"):
    """Faceless side-view figure in a white thobe and cap, facing right, feet on y=440."""
    if pose in ("qiyam", "takbir", "qawmah"):
        s.F("ellipse", cx=270, cy=434, rx=42, ry=12, fill=SKIN)
        s.F("path", d="M226 168 C210 178 206 210 206 250 L198 432 H306 L300 250 C300 210 296 178 282 168 Z", fill=THOBE)
        _head(s, 256, 122)
        if pose == "qiyam":
            s.T("M262 188 L258 262 L300 240", THOBE, 32)
            s.F("circle", cx=306, cy=238, r=16, fill=SKIN)
        elif pose == "takbir":
            s.T("M262 188 L304 214 L304 150", THOBE, 32)
            s.F("ellipse", cx=304, cy=130, rx=15, ry=22, fill=SKIN)
        else:
            s.T("M262 188 L266 300", THOBE, 32)
            s.F("circle", cx=266, cy=314, r=15, fill=SKIN)
    elif pose == "ruku":
        s.F("ellipse", cx=248, cy=434, rx=42, ry=12, fill=SKIN)
        s.F("path", d="M196 226 C200 214 268 214 276 236 L266 432 H206 Z", fill=THOBE)
        s.T("M236 246 L350 250", THOBE, 74)
        _head(s, 392, 256, "front", 38)
        s.T("M340 266 L272 336", THOBE, 30)
        s.F("circle", cx=264, cy=344, r=16, fill=SKIN)
    elif pose == "sujood":
        s.F("ellipse", cx=112, cy=420, rx=13, ry=22, fill=SKIN)
        s.T("M130 422 L228 424", THOBE, 44)
        s.T("M226 418 L236 322", THOBE, 58)
        s.T("M236 318 L346 382", THOBE, 72)
        _head(s, 384, 402, "down", 36)
        s.T("M326 384 L344 432 L372 436", THOBE, 28)
        s.F("ellipse", cx=380, cy=436, rx=20, ry=9, fill=SKIN)
    else:  # jalsa, tashahhud, taslim: sitting on the heels
        s.F("ellipse", cx=180, cy=418, rx=15, ry=20, fill=SKIN)
        s.T("M328 424 L186 426", THOBE, 44)
        s.T("M202 398 L320 410", THOBE, 60)
        s.T("M204 386 L216 236", THOBE, 78)
        if pose == "taslim":
            _head(s, 222, 180)
            s.M("M282 150 C300 166 300 194 282 210", INK, 8)
        else:
            _head(s, 222, 180)
        s.T("M222 252 L246 330 L300 382", THOBE, 28)
        s.F("circle", cx=306, cy=386, r=16, fill=SKIN)
        if pose == "tashahhud":
            s.T("M308 374 L318 344", SKIN, 9)


POSE_ALIAS = {"stand": "qiyam", "arms-down": "qawmah", "sit": "jalsa"}


def sil(s, pose, x=256, y=470, sc=1.0, color=None, white=False):
    """Place a worshipper with feet at (x, y). sc=1 is about 330 px tall."""
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -440)")
    worshipper(s, POSE_ALIAS.get(pose, pose))
    s.close()


for _id, pose in (("qiyam", "qiyam"), ("takbir-position", "takbir"), ("ruku", "ruku"), ("qawmah", "qawmah"), ("sujood", "sujood"),
                  ("jalsa", "jalsa"), ("tashahhud", "tashahhud"), ("taslim", "taslim")):
    D[_id] = (lambda p: lambda s: (mat(s, 256, 440, 400, 36), sil(s, p, 256, 440, 1.0)))(pose)


@reg("salah")
def _(s):
    mat(s, 256, 440, 440, 40)
    for x, p in ((110, "stand"), (250, "ruku"), (380, "sujood")):
        sil(s, p, x, 440, 0.62)


@reg("congregational-prayer")
def _(s):
    for row, y in enumerate((300, 440)):
        mat(s, 256, y, 470, 30, K["darkred"] if row else K["red"])
        for x in range(70, 470, 74):
            sil(s, "stand", x, y, 0.4 + row * 0.06)


D["adhan"] = lambda s: (minaret(s, 200, 470, 260, 60), s.M("M300 140 C330 170 330 210 300 240 M340 110 C390 160 390 220 340 270 M380 80 C450 150 450 230 380 300", K["blue"], 14))
D["iqamah"] = lambda s: (mat(s, 256, 440, 440, 34), [sil(s, "stand", x, 440, 0.7) for x in (110, 256, 400)],
                         s.M("M60 120 C80 140 80 170 60 190 M30 100 C70 140 70 180 30 220", K["blue"], 10))
D["friday-prayer"] = lambda s: (P(s, mosque, 256, 180, 0.6), [(mat(s, 256, y, 460, 24, K["red"]), [sil(s, "stand", x, y, 0.3) for x in range(60, 470, 50)]) for y in (380, 460)])
D["eid-prayer"] = lambda s: (sky_bg(s), crescent(s, 380, 110, 40), ground(s, "#9BD7A8", 300), [[sil(s, "stand", x, y, 0.28) for x in range(70, 460, 48)] for y in (370, 450)])
D["taraweeh-prayer"] = lambda s: (sky_bg(s, "#1E2A4A"), crescent(s, 400, 100, 30), [s.F("circle", outline=False, cx=x, cy=y, r=4, fill=WHITEK) for x, y in ((90, 90), (200, 70), (300, 120))],
                                  P(s, mosque, 256, 220, 0.5), [sil(s, "stand", x, 460, 0.36, white=True) for x in range(70, 460, 56)])

# ---------------------------------------------------------------- hajj and umrah
def circle_arrows(s, cx, cy, r, color=K["green"]):
    for a in (-60, 60, 180):
        x0, y0 = arc_pt(cx, cy, r, a); x1, y1 = arc_pt(cx, cy, r, a + 80)
        s.M(f"M{x0:.0f} {y0:.0f} A{r} {r * 0.4} 0 0 0 {x1:.0f} {y1:.0f}", color, 12)


@reg("tawaf")
def _(s):
    s.F("ellipse", cx=256, cy=380, rx=230, ry=90, fill=MARBLE)
    for k in range(40):
        a = k * 9
        x, y = 256 + 200 * math.cos(math.radians(a)), 380 + 74 * math.sin(math.radians(a))
        s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=8, fill=WHITEK if k % 3 else K["grey"])
    P(s, kaaba, 256, 300, 0.5)
    s.M("M120 440 C80 410 80 360 120 330 " + head(120, 330, -60, 26), K["green"], 8)


D["umrah"] = lambda s: (D["tawaf"](s))
@reg("ihram")
def _(s):
    s.F("ellipse", cx=270, cy=434, rx=42, ry=12, fill=SKIN)
    s.T("M236 300 V430 M276 300 V430", SKIN, 30)
    s.F("path", d="M206 170 C200 200 204 250 210 290 H300 C306 250 306 200 296 170 Z", fill=SKIN)
    s.F("path", d="M196 270 H312 L306 400 H202 Z", fill=WHITEK)
    s.F("path", d="M206 168 C220 160 250 160 262 166 L304 290 H212 C204 240 200 200 206 168Z", fill=WHITEK)
    s.T("M290 186 L300 300", SKIN, 30)
    s.F("circle", cx=300, cy=312, r=15, fill=SKIN)
    s.F("circle", cx=256, cy=122, r=40, fill=SKIN)


D["miqat"] = lambda s: (sky_bg(s), ground(s, SAND, 380), P(s, mosque, 330, 260, 0.5), s.T("M120 440 V250", DARK, 12),
                        s.F("rect", x=60, y=220, width=140, height=60, rx=8, fill=K["darkgreen"]))
D["talbiyah-tile"] = None
D["sai"] = lambda s: (D["safa-and-marwa"](s), [sil(s, "stand", x, 400, 0.3, white=True) for x in (200, 260, 320)])
D["day-of-arafah"] = lambda s: (D["mount-arafat"](s), s.F("circle", cx=400, cy=100, r=40, fill=K["yellow"]))
D["night-at-muzdalifah"] = lambda s: D["muzdalifah"](s)


@reg("stoning-the-jamarat")
def _(s):
    s.F("rect", x=40, y=380, width=432, height=60, fill=MARBLE)
    s.F("rect", x=200, y=120, width=112, height=280, rx=10, fill="#8C7560")
    for x, y in ((120, 200), (150, 160), (380, 180), (360, 230)):
        s.F("circle", cx=x, cy=y, r=10, fill=STONED)
    s.M("M90 300 C120 230 160 200 200 200 M430 300 C400 240 360 220 312 230", MID, 6, dash="10 10")


D["qurbani"] = lambda s: sheep(s)
D["halq"] = lambda s: (s.F("rect", x=120, y=200, width=200, height=80, rx=20, fill=GREY), s.F("rect", x=300, y=220, width=110, height=40, rx=10, fill=K["darkgrey"]),
                       s.M("M140 280 V300 M170 280 V300 M200 280 V300 M230 280 V300 M260 280 V300 M290 280 V300", K["darkgrey"], 8))


@reg("hajj-stages-chart")
def _(s):
    s.F("rect", x=40, y=40, width=432, height=432, rx=30, fill=K["cream"])
    pts = ((110, 400), (200, 300), (130, 190), (260, 140), (380, 220), (400, 360), (280, 400))
    s.M("M" + " L".join(f"{x} {y}" for x, y in pts), K["brown"], 8, dash="16 12")
    for i, (x, y) in enumerate(pts):
        s.F("circle", cx=x, cy=y, r=26, fill=(K["green"], K["blue"], K["orange"], K["red"])[i % 4])
    P(s, kaaba, 110, 400, 0.12)


D["tawaf-al-wida"] = lambda s: (D["tawaf"](s), s.M("M420 120 H480 " + head(480, 120, 0, 24), K["green"], 10))

# ---------------------------------------------------------------- ramadan
def lantern(s, x=256, y=256, sc=1.0, glass=K["yellow"]):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -256)")
    s.T("M256 40 V90", GOLDD, 8)
    s.F("path", d="M206 90 H306 L326 130 H186Z", fill=GOLD)
    s.F("path", d="M190 130 H322 L340 330 H172Z", fill=glass)
    s.M("M210 130 L200 330 M256 130 V330 M302 130 L312 330", GOLDD, 8)
    s.F("path", d="M172 330 H340 L300 380 H212Z", fill=GOLD)
    s.F("circle", cx=256, cy=400, r=14, fill=GOLD)
    s.close()


def dates_bowl(s, x=256, y=330, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -330)")
    for dx, dy, r in ((-60, -20, 0), (-10, -34, 20), (40, -24, -14), (80, -10, 30), (-90, 0, -30)):
        s.F("ellipse", cx=256 + dx, cy=300 + dy, rx=34, ry=18, fill=K["darkbrown"], transform=f"rotate({r} {256 + dx} {300 + dy})")
    s.F("path", d="M110 300 H402 C402 380 340 420 256 420 C172 420 110 380 110 300Z", fill=K["brown"])
    s.close()


def glass_water(s, x, y, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc})")
    s.F("path", d="M-40 -80 H40 L30 80 H-30Z", fill="#D9EEFB")
    s.F("path", outline=False, d="M-35 -20 H35 L30 76 H-30Z", fill="#8FD0FF")
    s.close()


D["ramadan"] = lambda s: (sky_bg(s, "#1E2A4A"), crescent(s, 170, 170, 90), lantern(s, 350, 260, 0.7))
D["suhoor"] = lambda s: (sky_bg(s, "#1E2A4A"), crescent(s, 400, 110, 34), s.F("rect", x=40, y=360, width=432, height=40, rx=8, fill=K["brown"]),
                         dates_bowl(s, 180, 330, 0.5), glass_water(s, 330, 300, 0.7))
D["iftar"] = lambda s: (sky_bg(s, "#F5913E"), s.F("circle", cx=256, cy=300, r=90, fill=K["yellow"]), s.F("rect", x=40, y=340, width=432, height=60, rx=8, fill=K["brown"]),
                        dates_bowl(s, 160, 310, 0.45), glass_water(s, 300, 290, 0.6), P(s, cup, 400, 300, 0.25))
D["breaking-fast-with-dates"] = lambda s: (dates_bowl(s, 200, 330, 0.9), glass_water(s, 400, 300, 1.1))
D["laylat-al-qadr"] = lambda s: (sky_bg(s, "#14203A"), [s.F("polygon", outline=False, points=star_pts(x, y, r, r * 0.4, 4), fill="#FFE38A") for x, y, r in
                                                         ((100, 110, 20), (220, 80, 14), (360, 120, 24), (430, 220, 14), (150, 230, 12), (300, 200, 16))],
                                 P(s, mosque, 256, 340, 0.5, body="#3A4A6A", dome_c="#3A4A6A"))
D["itikaf"] = lambda s: (arches(s, 40, 472, 420, 300, 3, MARBLE, "#B9C8DC"), mat(s, 256, 420, 300, 40), book_closed(s, K["darkgreen"], 256, 340, 0.3))
D["quran-recitation"] = lambda s: (s.F("circle", outline=False, cx=256, cy=220, r=190, fill="#FFF1C2"), rehal(s, 256, 330, 0.9), book_open_q(s, 256, 260, 0.75))
D["zakat-al-fitr"] = lambda s: (s.F("path", d="M150 200 C150 160 362 160 362 200 L392 420 C392 450 120 450 120 420Z", fill=K["tan"]),
                                 s.T("M180 190 C220 140 292 140 332 190", K["brown"], 12), [s.F("ellipse", outline=False, cx=x, cy=180, rx=10, ry=6, fill=K["cream"]) for x in range(200, 320, 22)],
                                 hand(s, 420, 380, 0.7, True))

# ---------------------------------------------------------------- prophets' stories through objects
def waves(s, y=380, color="#3D8BFD"):
    s.F("path", d=f"M20 {y} C80 {y - 30} 140 {y + 30} 200 {y} C260 {y - 30} 320 {y + 30} 380 {y} C430 {y - 24} 470 {y + 10} 492 {y} V472 H20Z", fill=color)


D["ark-of-nuh"] = lambda s: (sky_bg(s, "#8FA6C9"), s.F("path", d="M60 300 H452 L400 400 H112Z", fill=K["brown"]), s.F("rect", x=150, y=220, width=212, height=80, rx=6, fill=K["tan"]),
                             s.F("polygon", points="140,220 256,160 372,220", fill=K["darkbrown"]), waves(s, 390))
D["whale-of-yunus"] = lambda s: (waves(s, 300, "#2C5FC9"), s.F("path", d="M80 300 C100 200 300 180 380 260 L460 210 L440 300 L460 380 L380 330 C300 400 100 380 80 300Z", fill="#3A5A8C"),
                                 s.F("circle", outline=False, cx=150, cy=270, r=10, fill=LIGHT), s.M("M200 200 C190 160 210 140 200 110 M220 200 C240 160 220 140 240 110", "#8FD0FF", 8))
D["fire-of-ibrahim"] = lambda s: (flames(s), [s.F("circle", cx=x, cy=y, r=16, fill="#4CB963") for x, y in ((150, 430), (360, 430), (256, 440))],
                                  [P(s, sprout, x, 430, 0.18, pot=False) for x in (110, 400)])
D["staff-of-musa"] = lambda s: (s.T("M200 460 L310 80", K["brown"], 28), s.T("M310 80 C330 50 370 60 360 100", K["brown"], 22))
D["parting-of-the-sea"] = lambda s: (s.F("path", d="M20 100 C80 80 140 120 190 100 L220 470 H20Z", fill="#2C5FC9"), s.F("path", d="M492 100 C432 80 372 120 322 100 L292 470 H492Z", fill="#2C5FC9"),
                                     s.F("polygon", outline=False, points="220,470 292,470 270,100 242,100", fill=SAND), s.M("M200 140 C150 180 120 160 60 200 M312 140 C362 180 392 160 452 200", "#8FD0FF", 8))


@reg("valley-of-the-ants")
def _(s):
    sky_bg(s)
    hills(s, STONE, STONED, ((40, 280), (150, 220), (300, 250), (470, 200)))
    for i in range(9):
        x, y = 60 + i * 46, 380 + (i % 2) * 20
        for dx in (-12, 0, 12):
            s.F("circle", outline=False, cx=x + dx, cy=y, r=7 if dx else 6, fill=DARK)
        s.M(f"M{x - 6} {y} l-6 14 M{x + 6} {y} l6 14 M{x} {y} v14", DARK, 3)


D["well-of-yusuf"] = lambda s: (sky_bg(s), ground(s, SAND, 330), s.F("ellipse", cx=256, cy=320, rx=130, ry=36, fill=STONED),
                                s.F("path", d="M126 320 V410 C126 440 386 440 386 410 V320 C386 350 126 350 126 320Z", fill=STONE), s.F("ellipse", outline=False, cx=256, cy=320, rx=104, ry=24, fill="#1F1F24"),
                                s.T("M160 320 V200 H352 V320", K["brown"], 14), s.T("M256 200 V280", K["tan"], 6))
D["shirt-of-yusuf"] = lambda s: s.F("path", d="M170 90 L120 120 L60 200 L120 240 L150 210 V440 H362 V210 L392 240 L452 200 L392 120 L342 90 C320 130 192 130 170 90Z", fill=K["cream"])
D["she-camel-of-salih"] = lambda s: (sky_bg(s), ground(s, SAND, 400), camel(s))
D["cave-of-the-sleepers"] = lambda s: cave_mountain(s, "#A58B70", (256, 330))
D["spider-web-and-dove-at-the-cave"] = lambda s: (cave_mountain(s, "#A58B70", (256, 320)),
                                                  s.M("M206 380 L306 280 M206 280 L306 380 M256 270 V390 M196 330 H316", LIGHT, 3),
                                                  P(s, dove, 380, 380, 0.3), s.F("circle", cx=140, cy=400, r=20, fill=K["darkbrown"]))
D["ram-of-sacrifice"] = lambda s: (sheep(s, K["cream"]), s.T("M360 200 C330 160 390 140 400 180 C410 220 370 220 370 200", K["tan"], 14))
D["tablets-of-stone"] = lambda s: [s.F("path", d=f"M{x} 440 V170 C{x} 110 {x + 150} 110 {x + 150} 170 V440Z", fill="#C7C2B8") for x in (90, 272)] + [
    s.M(f"M{x + 30} {y} H{x + 120}", "#8C877E", 8) for x in (90, 272) for y in (220, 270, 320, 370)]
D["iron-armour-of-dawud"] = lambda s: (s.F("path", d="M170 90 L110 130 L80 240 L130 260 L160 200 V440 H352 V200 L382 260 L432 240 L402 130 L342 90 C320 130 192 130 170 90Z", fill="#9AA3AF"),
                                       [s.raw(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="#6B7280" stroke-width="3"/>') for x in range(180, 340, 18) for y in range(160, 430, 18)])

# ---------------------------------------------------------------- christianity
def church(s, body="#E8DCC8", roof=K["darkred"]):
    s.F("rect", x=150, y=250, width=212, height=200, fill=body)
    s.F("polygon", points="130,260 256,150 382,260", fill=roof)
    s.F("rect", x=226, y=90, width=60, height=160, fill=body)
    s.F("polygon", points="216,100 256,40 296,100", fill=roof)
    s.T("M256 40 V10 M244 22 H268", GOLD, 8)
    s.F("path", d="M226 450 V390 C226 360 286 360 286 390 V450Z", fill=K["brown"])
    s.F("circle", cx=256, cy=300, r=26, fill=K["sky"])


def cross(s, color=K["brown"]):
    s.F("path", d="M226 60 H286 V170 H376 V230 H286 V452 H226 V230 H136 V170 H226Z", fill=color)


D["church"] = church
D["cross"] = cross
D["bible"] = lambda s: (s.F("rect", x=130, y=90, width=252, height=332, rx=14, fill=K["darkbrown"]), s.F("rect", outline=False, x=360, y=100, width=16, height=312, fill=K["cream"]),
                        P(s, cross, 250, 256, 0.35, color=GOLD))
D["rosary"] = lambda s: ([s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=12, fill=K["brown"]) for x, y in (arc_pt(256, 200, 130, a) for a in range(100, 441, 14))],
                         s.T("M256 330 V380", K["brown"], 8), P(s, cross, 256, 420, 0.22, color=GOLD))
D["church-candle"] = lambda s: (P(s, candle, 256, 256, 1.0), s.F("rect", x=170, y=430, width=172, height=24, rx=8, fill=GOLD))
D["church-bell"] = lambda s: (s.T("M256 60 V100", K["brown"], 16), s.F("path", d="M256 100 C190 100 170 170 170 250 C170 320 140 350 120 370 H392 C372 350 342 320 342 250 C342 170 322 100 256 100Z", fill=GOLD),
                              s.F("circle", cx=256, cy=390, r=24, fill=GOLDD))
D["stained-glass-window"] = lambda s: (s.F("path", d="M120 460 V200 C120 110 256 60 256 60 C256 60 392 110 392 200 V460Z", fill=DARK),
                                       [s.F("polygon", outline=False, points=p, fill=c) for p, c in (("140,440 140,210 256,200 256,440", K["blue"]), ("256,200 372,210 372,440 256,440", K["red"]),
                                                                                                    ("140,210 256,84 256,200", K["yellow"]), ("256,84 372,210 256,200", K["green"]))],
                                       s.M("M256 84 V440 M140 320 H372 M140 210 L372 210", DARK, 10))
@reg("chapel")
def _(s):
    s.F("rect", x=130, y=230, width=252, height=220, fill=WHITEK)
    s.F("polygon", points="110,240 256,120 402,240", fill=K["blue"])
    s.F("path", d="M226 120 V80 H286 V120", fill=WHITEK)
    s.F("circle", cx=256, cy=100, r=12, fill=GOLD)
    s.T("M256 70 V40 M244 52 H268", GOLD, 8)
    s.F("path", d="M220 450 V370 C220 330 292 330 292 370 V450Z", fill=K["brown"])
    for x in (165, 347):
        s.F("path", d=f"M{x - 18} 330 V290 C{x - 18} 270 {x + 18} 270 {x + 18} 290 V330Z", fill=K["sky"])
D["dove-of-peace"] = lambda s: (P(s, dove, 256, 256, 1.0))
D["ichthys"] = lambda s: s.M("M100 300 C180 160 330 160 410 300 M100 220 C180 360 330 360 410 220", K["blue"], 22)
D["chalice"] = lambda s: (s.F("path", d="M150 100 H362 C362 220 310 260 256 260 C202 260 150 220 150 100Z", fill=GOLD), s.F("rect", x=240, y=258, width=32, height=120, fill=GOLD),
                          s.F("path", d="M170 420 C170 380 342 380 342 420Z", fill=GOLD))
D["church-organ"] = lambda s: (s.F("rect", x=80, y=330, width=352, height=120, rx=8, fill=K["brown"]),
                               [s.F("rect", x=96 + i * 40, y=330 - h, width=30, height=h, rx=14, fill=GREY) for i, h in enumerate((120, 170, 220, 260, 220, 170, 120, 90))])
D["baptism-font"] = lambda s: (s.F("path", d="M110 180 H402 C402 260 340 300 256 300 C172 300 110 260 110 180Z", fill=MARBLE), s.F("ellipse", outline=False, cx=256, cy=182, rx=140, ry=24, fill=K["sky"]),
                               s.F("rect", x=226, y=298, width=60, height=110, fill=MARBLE), s.F("rect", x=170, y=400, width=172, height=40, rx=8, fill=MARBLE))
D["advent-candles"] = lambda s: (s.F("ellipse", cx=256, cy=400, rx=200, ry=50, fill=K["darkgreen"]),
                                 [P(s, candle, x, 300, 0.5) for x in (130, 210, 300, 380)])

# ---------------------------------------------------------------- judaism
def star_david(s, color=K["blue"]):
    s.T("M256 70 L416 346 H96 Z", color, 30)
    s.T("M256 442 L96 166 H416 Z", color, 30)


D["synagogue"] = lambda s: (sky_bg(s), s.F("rect", x=100, y=220, width=312, height=230, fill="#E8DCC8"), s.F("path", d="M100 220 C100 120 412 120 412 220Z", fill=K["blue"]),
                            arches(s, 120, 392, 450, 120, 4, "#E8DCC8", "#8FA6C9"), P(s, star_david, 256, 170, 0.2, color=GOLD))
D["star-of-david"] = star_david


@reg("menorah")
def _(s):
    for k in range(3):
        r = 60 + k * 50
        s.T(f"M{256 - r} 160 C{256 - r} {300 + k * 10} {256 + r} {300 + k * 10} {256 + r} 160", GOLD, 16)
    s.T("M256 160 V420", GOLD, 18)
    s.F("path", d="M190 440 C190 400 322 400 322 440Z", fill=GOLD)
    for x in (106, 156, 206, 256, 306, 356, 406):
        s.F("path", d=f"M{x} 120 C{x + 14} 136 {x + 12} 150 {x} 156 C{x - 12} 150 {x - 14} 136 {x} 120Z", fill=K["orange"])


D["torah-scroll"] = lambda s: (s.F("rect", x=150, y=130, width=212, height=260, fill=K["cream"]), [s.M(f"M180 {y} H332", MID, 8) for y in range(170, 370, 36)],
                               [s.F("rect", x=x, y=90, width=40, height=340, rx=18, fill=K["brown"]) for x in (110, 362)])
D["kippah"] = lambda s: (s.F("path", d="M96 330 C96 170 416 170 416 330Z", fill=K["darkblue"]), s.M("M120 300 H392", GOLD, 10))
D["shofar"] = lambda s: s.T("M90 380 C200 380 300 320 360 180 C370 150 400 130 420 140", K["tan"], 50)
D["mezuzah"] = lambda s: (s.F("rect", x=210, y=90, width=92, height=330, rx=20, fill=K["blue"]), s.F("polygon", outline=False, points=star_pts(256, 200, 30, 16, 6), fill=GOLD))
D["tallit"] = lambda s: (s.F("rect", x=80, y=150, width=352, height=220, rx=10, fill=WHITEK), [s.M(f"M80 {y} H432", K["blue"], 12) for y in (190, 330)],
                         [s.M(f"M{x} 370 V420", MID, 4) for x in range(96, 430, 16)])
@reg("challah-bread")
def _(s):
    s.F("path", d="M70 300 C70 230 150 210 256 210 C362 210 442 230 442 300 C442 360 362 380 256 380 C150 380 70 360 70 300Z", fill=K["tan"])
    for x in (130, 200, 270, 340):
        s.F("ellipse", cx=x + 20, cy=290, rx=48, ry=62, fill="#D9A066", transform=f"rotate(35 {x + 20} 290)")
    s.F("ellipse", outline=False, cx=170, cy=250, rx=30, ry=10, fill="#F2CC8F")


D["seder-plate"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=MARBLE), [s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=44, fill=c) for (x, y), c in
                                                                                  zip((arc_pt(256, 256, 120, a) for a in range(-90, 270, 60)), (K["green"], K["tan"], K["red"], WHITEK, K["brown"], K["yellow"]))])
@reg("hanukkiah")
def _(s):
    for k in range(4):
        r = 50 + k * 45
        s.T(f"M{256 - r} 170 C{256 - r} {290 + k * 12} {256 + r} {290 + k * 12} {256 + r} 170", GOLD, 14)
    s.T("M256 120 V420", GOLD, 18)
    s.F("path", d="M190 440 C190 400 322 400 322 440Z", fill=GOLD)
    for x in (61, 106, 151, 196, 316, 361, 406, 451):
        s.F("path", d=f"M{x} 132 C{x + 12} 146 {x + 10} 160 {x} 166 C{x - 10} 160 {x - 12} 146 {x} 132Z", fill=K["orange"])
    s.F("path", d="M256 80 C270 96 268 110 256 116 C244 110 242 96 256 80Z", fill=K["orange"])


# ---------------------------------------------------------------- hinduism
def hindu_temple(s, body=K["orange"], dark=K["darkred"]):
    s.F("rect", x=120, y=330, width=272, height=120, fill=body)
    s.F("path", d="M170 330 C170 230 210 130 256 80 C302 130 342 230 342 330Z", fill=body)
    for y in (200, 250, 300):
        s.M(f"M{180 + (300 - y) // 3} {y} H{332 - (300 - y) // 3}", dark, 8)
    s.T("M256 80 V40", GOLD, 8)
    s.F("polygon", points="256,10 290,30 256,40", fill=K["red"])
    s.F("path", d="M226 450 V390 C226 360 286 360 286 390 V450Z", fill=dark)


def om(s, color=K["orange"]):
    s.M("M120 200 C200 160 250 220 200 260 C260 240 290 300 230 350 C190 380 130 360 120 320 M210 260 C240 260 260 230 280 220 C320 200 350 240 330 290 "
        "C310 340 300 360 340 380 M300 130 C330 150 370 150 390 130", color, 22)
    s.F("circle", cx=360, cy=90, r=14, fill=color)


D["hindu-temple"] = lambda s: (sky_bg(s), hindu_temple(s))


@reg("diya")
def _(s):
    s.F("path", d="M100 300 C140 400 372 400 412 300 C380 320 132 320 100 300Z", fill=K["orange"])
    s.F("path", d="M100 300 C130 280 382 280 412 300 C380 320 132 320 100 300Z", fill=K["darkred"])
    s.open("part-flame", "256 280")
    s.F("path", d="M256 140 C296 190 300 250 256 280 C212 250 216 190 256 140Z", fill=K["yellow"])
    s.F("path", outline=False, d="M256 200 C272 220 272 250 256 266 C240 250 240 220 256 200Z", fill=K["orange"])
    s.close()


D["kalash"] = lambda s: (s.F("path", d="M190 200 C110 230 100 370 170 420 H342 C412 370 402 230 322 200Z", fill=GOLD), s.F("rect", x=200, y=170, width=112, height=40, rx=10, fill=GOLD),
                         [s.F("ellipse", cx=x, cy=150, rx=24, ry=60, fill=K["green"], transform=f"rotate({(x - 256) // 2} {x} 170)") for x in (200, 236, 276, 312)],
                         s.F("circle", cx=256, cy=120, r=40, fill=K["brown"]), s.M("M180 300 H332", K["red"], 10))
@reg("shankh")
def _(s):
    s.F("path", d="M90 330 C70 250 140 170 240 150 C330 132 400 160 430 200 L476 206 L444 244 C440 300 380 350 300 370 C220 390 110 380 90 330Z", fill=K["cream"])
    s.F("path", d="M150 340 C200 300 300 290 380 300 C350 330 290 350 230 356 C190 360 160 352 150 340Z", fill=K["pink"])
    s.M("M170 200 C190 230 190 260 170 290 M230 170 C250 210 250 250 236 290 M300 160 C320 200 320 240 306 280", K["tan"], 9)


D["aarti-plate"] = lambda s: (s.F("ellipse", cx=256, cy=330, rx=210, ry=80, fill=GOLD), s.F("ellipse", outline=False, cx=256, cy=320, rx=170, ry=56, fill="#F7D57A"),
                              P(s, D["diya"], 256, 260, 0.45), [s.F("circle", cx=x, cy=330, r=20, fill=c) for x, c in ((130, K["red"]), (380, K["orange"]))])
D["temple-bell"] = lambda s: (s.T("M256 40 V110", GOLDD, 10), s.F("path", d="M256 110 C200 110 180 170 180 240 C180 300 160 330 140 350 H372 C352 330 332 300 332 240 C332 170 312 110 256 110Z", fill=GOLD),
                              s.F("circle", cx=256, cy=380, r=22, fill=GOLDD))
D["tilak"] = lambda s: (face_blank(s, 256, 260, 150), s.F("path", d="M240 150 H272 L262 250 H250Z", fill=K["red"]), s.F("circle", cx=256, cy=260, r=10, fill=K["orange"]))
D["incense-sticks"] = lambda s: (s.F("path", d="M170 400 C170 360 342 360 342 400 V430 H170Z", fill=K["brown"]),
                                 [(s.T(f"M{x} 380 L{x + d} 160", K["darkbrown"], 8), s.M(f"M{x + d} 150 C{x + d - 20} 120 {x + d + 20} 100 {x + d} 70", MID, 6)) for x, d in ((220, -30), (256, 0), (292, 30))])
D["rudraksha-beads"] = lambda s: [s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=20, fill=K["darkbrown"]) for x, y in (arc_pt(256, 256, 160, a) for a in range(0, 360, 15))]
D["trishul"] = lambda s: (s.T("M256 460 V150", GREY, 18), s.T("M160 120 C160 220 352 220 352 120 M256 220 V80", GREY, 18),
                          [s.F("polygon", points=f"{x - 16},{120 if x != 256 else 80} {x},{70 if x != 256 else 30} {x + 16},{120 if x != 256 else 80}", fill=GREY) for x in (160, 256, 352)])
D["damru"] = lambda s: (s.F("polygon", points="160,120 352,120 280,256 352,392 160,392 232,256", fill=K["brown"]), s.F("ellipse", cx=256, cy=120, rx=96, ry=20, fill=K["cream"]),
                        s.F("ellipse", cx=256, cy=392, rx=96, ry=20, fill=K["cream"]), s.M("M232 256 H280", K["red"], 10))
D["havan-kund"] = lambda s: (s.F("polygon", points="110,330 402,330 360,440 152,440", fill=K["darkred"]), flames(s, 256, 330, 220, 180))
D["coconut-offering"] = lambda s: (s.F("ellipse", cx=256, cy=380, rx=180, ry=40, fill=GOLD), s.F("circle", cx=256, cy=290, r=100, fill=K["brown"]),
                                   [s.F("ellipse", cx=x, cy=160, rx=20, ry=56, fill=K["green"], transform=f"rotate({(x - 256) // 2} {x} 200)") for x in (220, 256, 292)])
D["kumkum"] = lambda s: (s.F("ellipse", cx=256, cy=330, rx=160, ry=60, fill=K["brown"]), s.F("ellipse", outline=False, cx=256, cy=316, rx=130, ry=40, fill=K["red"]),
                         s.F("path", outline=False, d="M180 316 C220 260 300 260 340 316Z", fill="#D63A3F"))
D["temple-gopuram"] = lambda s: (sky_bg(s), s.F("polygon", points="130,450 170,110 342,110 382,450", fill="#E0A458"),
                                 [s.M(f"M{140 + (450 - y) // 9} {y} H{372 - (450 - y) // 9}", K["darkred"], 8) for y in range(150, 440, 40)],
                                 s.F("rect", x=200, y=80, width=112, height=34, rx=10, fill=GOLD), s.F("path", d="M226 450 V390 C226 360 286 360 286 390 V450Z", fill=K["darkbrown"]))
D["lotus-offering"] = lambda s: (s.F("ellipse", cx=256, cy=400, rx=180, ry=36, fill=GOLD), [s.F("ellipse", cx=256, cy=290, rx=44, ry=110, fill=K["pink"], transform=f"rotate({a} 256 380)") for a in (-60, -30, 30, 60, 0)])
D["tulsi-plant-pot"] = lambda s: (s.F("rect", x=170, y=300, width=172, height=150, rx=10, fill=K["orange"]), s.F("rect", x=150, y=280, width=212, height=34, rx=8, fill=K["darkred"]),
                                  s.T("M256 290 V130", K["darkgreen"], 10), [s.F("ellipse", cx=256 + dx, cy=y, rx=30, ry=16, fill=K["green"], transform=f"rotate({dx // 2} {256 + dx} {y})")
                                                                             for dx, y in ((-40, 160), (40, 180), (-40, 220), (40, 240), (0, 130))])
D["ganga-ghat"] = lambda s: (sky_bg(s, "#F9B57A"), [s.F("rect", outline=False, x=40, y=260 + i * 30, width=432, height=30, fill="#C9A87C" if i % 2 else "#B8936A") for i in range(4)],
                             s.F("rect", outline=False, x=20, y=380, width=472, height=90, fill=K["blue"]), P(s, hindu_temple, 140, 180, 0.35), P(s, hindu_temple, 380, 170, 0.4),
                             [P(s, D["diya"], x, 410, 0.15) for x in (120, 220, 330, 420)])

# ---------------------------------------------------------------- sikhism
def khanda(s, color=K["blue"]):
    s.T("M256 60 V420", color, 22)
    s.F("polygon", points="256,40 276,90 236,90", fill=color)
    s.T("M256 230 m-90 0 a90 90 0 1 0 180 0 a90 90 0 1 0 -180 0", color, 22)
    s.T("M150 140 C80 220 120 360 210 380 M362 140 C432 220 392 360 302 380", color, 18)


D["khanda"] = khanda
D["gurdwara"] = lambda s: (sky_bg(s), s.F("rect", x=110, y=280, width=292, height=170, fill=WHITEK), dome(s, 256, 280, 90, WHITEK, onion=True),
                           dome(s, 140, 280, 30, WHITEK, onion=True), dome(s, 372, 280, 30, WHITEK, onion=True), arches(s, 130, 382, 450, 100, 4, WHITEK, "#8FA6C9"),
                           s.T("M440 450 V120", GREY, 8), s.F("polygon", points="440,120 490,140 440,160", fill=K["orange"]))
D["golden-temple"] = lambda s: (sky_bg(s), s.F("rect", outline=False, x=20, y=330, width=472, height=140, fill="#3D8BFD"),
                                s.F("rect", x=150, y=220, width=212, height=120, fill=GOLD), dome(s, 256, 220, 80, GOLD, onion=True),
                                [dome(s, x, 220, 18, GOLD, onion=True) for x in (170, 342)], arches(s, 160, 352, 340, 60, 4, GOLD, GOLDD),
                                s.F("rect", outline=False, x=150, y=340, width=212, height=60, fill="#F7D57A", fill_opacity="0.5"))
D["kesh"] = lambda s: (face_blank(s, 256, 280, 130, hair=False), s.F("path", d="M126 260 C120 120 392 120 386 260 C360 200 152 200 126 260Z", fill="#2E2A3B"),
                       s.F("circle", cx=256, cy=130, r=50, fill="#2E2A3B"))
D["kangha"] = lambda s: (s.F("path", d="M110 200 H402 V250 H110Z", fill=K["tan"]), [s.M(f"M{x} 250 V330", K["tan"], 10) for x in range(126, 400, 18)])
D["kara"] = lambda s: s.T("M256 100 A156 156 0 1 1 255.9 100", GREY, 40)
D["kachera"] = lambda s: s.F("path", d="M120 140 H392 L400 380 H290 L256 260 L222 380 H112Z", fill=WHITEK)
D["kirpan"] = lambda s: (s.F("path", d="M150 420 C220 380 330 250 380 120 C320 220 220 330 140 400Z", fill=GREY), s.T("M130 400 L190 450", GOLD, 24), s.T("M110 430 L80 460", K["brown"], 22))
D["five-ks"] = lambda s: [P(s, D[k], x, y, 0.36) for k, x, y in (("kesh", 130, 130), ("kangha", 382, 130), ("kara", 256, 256), ("kachera", 130, 382), ("kirpan", 382, 382))]
D["langar"] = lambda s: ([(mat(s, 256, y, 460, 30, K["orange"])) for y in (330, 430)], [sil(s, "jalsa", x, y, 0.3) for y in (330, 430) for x in (100, 200, 300, 400)])
D["nishan-sahib"] = lambda s: (s.T("M256 470 V60", GREY, 14), s.F("polygon", points="262,70 440,120 262,170", fill=K["orange"]), P(s, khanda, 330, 120, 0.15))
@reg("chauri")
def _(s):
    for k in range(-4, 5):
        s.T(f"M256 230 C{256 + k * 14} 180 {256 + k * 30} 120 {256 + k * 40} 60", WHITEK, 16)
    s.F("rect", x=232, y=220, width=48, height=40, rx=10, fill=GOLD)
    s.T("M256 260 V460", GREY, 22)


D["sacred-scripture-on-palki"] = lambda s: (s.F("rect", x=100, y=320, width=312, height=120, rx=10, fill=GOLD), s.F("path", d="M100 320 C100 150 412 150 412 320Z", fill=GOLD),
                                            s.F("path", outline=False, d="M130 320 C130 190 382 190 382 320Z", fill=K["darkred"]),
                                            s.F("rect", x=170, y=270, width=172, height=60, rx=10, fill=K["orange"]))

# ---------------------------------------------------------------- buddhism and other faiths
def stupa(s, color=WHITEK):
    s.F("rect", x=90, y=400, width=332, height=50, fill=color)
    s.F("path", d="M110 400 C110 230 402 230 402 400Z", fill=color)
    s.F("rect", x=226, y=200, width=60, height=50, fill=GOLD)
    s.F("polygon", points="236,200 256,60 276,200", fill=GOLD)


def dharma(s, color=GOLD):
    s.T("M256 76 A180 180 0 1 1 255.9 76", color, 26)
    for a in range(0, 360, 45):
        x, y = arc_pt(256, 256, 180, a)
        s.M(f"M256 256 L{x:.0f} {y:.0f}", color, 16)
    s.F("circle", cx=256, cy=256, r=40, fill=color)


D["buddhist-stupa"] = lambda s: (sky_bg(s), stupa(s))
D["dharma-wheel"] = dharma
D["prayer-wheel"] = lambda s: (s.T("M256 470 V380", K["brown"], 20), s.F("rect", x=170, y=160, width=172, height=220, rx=16, fill=GOLD),
                               [s.M(f"M170 {y} H342", K["darkred"], 8) for y in (210, 270, 330)], s.F("rect", x=240, y=110, width=32, height=50, fill=K["brown"]))
D["prayer-flags"] = lambda s: (s.M("M40 140 C200 260 312 260 472 140", DARK, 6), [s.F("rect", x=60 + i * 80, y=170 + int(40 * math.sin(i / 4 * math.pi)), width=60, height=80, fill=c)
                                                                                for i, c in enumerate((K["blue"], WHITEK, K["red"], K["green"], K["yellow"]))])
D["buddhist-monastery"] = lambda s: (sky_bg(s), s.F("rect", x=100, y=280, width=312, height=170, fill=WHITEK), s.F("polygon", points="80,290 256,190 432,290", fill=K["darkred"]),
                                     s.F("rect", x=170, y=150, width=172, height=60, fill=WHITEK), s.F("polygon", points="150,160 256,100 362,160", fill=K["darkred"]),
                                     [s.F("rect", x=x, y=320, width=40, height=60, fill=K["darkbrown"]) for x in (140, 236, 332)])
D["lotus-symbol"] = lambda s: [s.F("ellipse", cx=256, cy=250, rx=50, ry=140, fill=c, transform=f"rotate({a} 256 380)") for a, c in
                               ((-70, K["pink"]), (70, K["pink"]), (-35, "#F48AA6"), (35, "#F48AA6"), (0, K["pink"]))]
D["bodhi-tree"] = lambda s: (s.T("M256 460 V300", K["brown"], 50), s.F("circle", cx=256, cy=220, r=170, fill=K["green"]),
                             [s.F("path", outline=False, d=f"M{x} {y} C{x - 26} {y - 30} {x} {y - 50} {x} {y - 50} C{x} {y - 50} {x + 26} {y - 30} {x} {y}Z", fill=K["darkgreen"])
                              for x, y in ((180, 200), (256, 160), (330, 210), (220, 280), (300, 290))])
D["singing-bowl"] = lambda s: (s.F("path", d="M110 240 H402 C402 360 340 410 256 410 C172 410 110 360 110 240Z", fill=GOLD), s.F("ellipse", cx=256, cy=240, rx=146, ry=30, fill=GOLDD),
                               s.T("M330 160 L420 100", K["brown"], 22), s.M("M120 160 C100 130 110 100 130 80 M392 200 C420 170 430 140 420 110", MID, 6))
D["mandala"] = lambda s: ([s.F("ellipse", cx=256, cy=120, rx=40, ry=90, fill=K["orange"], transform=f"rotate({a} 256 256)") for a in range(0, 360, 45)],
                          [s.F("ellipse", cx=256, cy=170, rx=26, ry=60, fill=K["blue"], transform=f"rotate({a + 22} 256 256)") for a in range(0, 360, 45)],
                          s.F("circle", cx=256, cy=256, r=60, fill=K["yellow"]), s.F("circle", cx=256, cy=256, r=24, fill=K["red"]))
D["begging-bowl"] = lambda s: (s.F("path", d="M100 230 H412 C412 360 350 420 256 420 C162 420 100 360 100 230Z", fill=K["darkbrown"]), s.F("ellipse", cx=256, cy=230, rx=156, ry=34, fill=K["brown"]))
D["jain-temple"] = lambda s: (sky_bg(s), P(s, hindu_temple, 256, 256, 1.0, body=WHITEK, dark=K["red"]))
D["jain-symbol"] = lambda s: (s.F("path", d="M150 430 V200 C150 160 190 160 190 200 V120 C190 90 226 90 226 120 V110 C226 80 262 80 262 110 V120 C262 90 298 90 298 120 V200 "
                                            "C298 160 340 170 340 210 V320 C340 400 300 440 250 440Z", fill=K["orange"]),
                              s.raw(f'<circle cx="250" cy="320" r="44" fill="none" stroke="{WHITEK}" stroke-width="12"/>'))
D["fire-temple"] = lambda s: (sky_bg(s), s.F("rect", x=110, y=240, width=292, height=210, fill="#E8DCC8"), arches(s, 130, 382, 450, 120, 4, "#E8DCC8", "#7A6A55"),
                              s.F("rect", x=90, y=220, width=332, height=30, fill="#C9B79A"), flames(s, 256, 220, 120, 100))
D["sacred-fire"] = lambda s: (s.F("path", d="M140 330 H372 L340 450 H172Z", fill=GOLD), flames(s, 256, 330, 220, 220))
D["torii-gate"] = lambda s: (s.T("M150 460 V140 M362 460 V140", K["red"], 40), s.F("path", d="M60 110 C160 140 352 140 452 110 L440 150 C352 170 160 170 72 150Z", fill=K["red"]),
                             s.F("rect", x=100, y=200, width=312, height=30, fill=K["red"]), s.F("rect", x=60, y=100, width=392, height=18, rx=6, fill=DARK))
D["shinto-shrine"] = lambda s: (sky_bg(s), s.F("rect", x=140, y=260, width=232, height=190, fill=K["cream"]), s.F("path", d="M80 270 C180 230 332 230 432 270 L400 200 C320 180 192 180 112 200Z", fill=K["darkbrown"]),
                                [s.T(f"M{x} 450 V270", K["red"], 18) for x in (160, 352)])
D["yin-yang"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=DARK), s.F("path", d="M256 56 A100 100 0 0 1 256 256 A100 100 0 0 0 256 456 A200 200 0 0 1 256 56Z", fill=WHITEK),
                           s.F("circle", outline=False, cx=256, cy=156, r=30, fill=DARK), s.F("circle", outline=False, cx=256, cy=356, r=30, fill=WHITEK))
D["taoist-temple"] = lambda s: (sky_bg(s), s.F("rect", x=140, y=270, width=232, height=180, fill=K["red"]), s.F("path", d="M60 290 C160 250 352 250 452 290 L410 220 C320 200 192 200 102 220Z", fill=K["darkgreen"]),
                                s.F("rect", x=190, y=170, width=132, height=60, fill=K["red"]), s.F("path", d="M140 180 C200 150 312 150 372 180 L340 130 C290 120 222 120 172 130Z", fill=K["darkgreen"]))
D["siddhachakra"] = lambda s: ([s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=50, fill=K["orange"]) for x, y in (arc_pt(256, 256, 150, a) for a in range(0, 360, 45))],
                               s.F("circle", cx=256, cy=256, r=80, fill=GOLD))
D["fire-altar"] = lambda s: (s.F("path", d="M170 260 H342 V300 H310 V420 H360 V450 H152 V420 H202 V300 H170Z", fill=GREY), flames(s, 256, 260, 160, 170))
D["bahai-nine-pointed-star"] = lambda s: s.F("polygon", points=star_pts(256, 256, 210, 140, 9), fill=K["blue"])

# ---------------------------------------------------------------- places of worship worldwide
def site(*steps):
    return lambda s: (sky_bg(s), [st(s) for st in steps])


D["sheikh-zayed-grand-mosque"] = site(lambda s: (minaret(s, 60, 440, 280, 22), minaret(s, 452, 440, 280, 22), s.F("rect", x=90, y=320, width=332, height=120, fill=WHITEK),
                                                 [dome(s, x, 320, 34, WHITEK) for x in (130, 190, 322, 382)], dome(s, 256, 320, 90, WHITEK), arches(s, 90, 422, 440, 70, 6)))
D["blue-mosque"] = site(lambda s: ([minaret(s, x, 440, 300, 16, GREY, "#6E7E99") for x in (40, 100, 412, 472)], s.F("rect", x=120, y=330, width=272, height=110, fill="#C9CED6"),
                                   [dome(s, x, 330, 40, "#8FA6C9") for x in (160, 352)], dome(s, 256, 330, 100, "#8FA6C9")))
D["hagia-sophia"] = site(lambda s: ([minaret(s, x, 440, 260, 16, "#E8C9A8", GREY) for x in (50, 462)], s.F("rect", x=100, y=320, width=312, height=120, fill="#E8B48A"),
                                    dome(s, 256, 320, 110, "#8D98A6"), [dome(s, x, 320, 40, "#8D98A6") for x in (140, 372)]))
D["faisal-mosque"] = site(lambda s: ([minaret(s, x, 440, 300, 16, WHITEK, GREY) for x in (60, 452)], s.F("polygon", points="110,440 256,140 402,440", fill=WHITEK),
                                     s.F("polygon", outline=False, points="256,140 210,440 300,440", fill=MARBLE)))
D["jama-masjid-delhi"] = site(lambda s: ([minaret(s, x, 440, 260, 26, K["darkred"], WHITEK) for x in (60, 452)], s.F("rect", x=100, y=300, width=312, height=140, fill=K["darkred"]),
                                         [dome(s, x, 300, 50, WHITEK, onion=True) for x in (150, 362)], dome(s, 256, 300, 80, WHITEK, onion=True), arches(s, 120, 392, 440, 80, 5, K["darkred"], "#3A2E28")))
D["badshahi-mosque"] = site(lambda s: ([minaret(s, x, 440, 280, 24, K["darkred"], WHITEK) for x in (50, 462)], s.F("rect", x=90, y=300, width=332, height=140, fill=K["darkred"]),
                                       [dome(s, x, 300, 50, WHITEK, onion=True) for x in (150, 362)], dome(s, 256, 300, 76, WHITEK, onion=True)))
D["umayyad-mosque"] = site(lambda s: (arches(s, 40, 472, 440, 140, 8, "#D9CBB0", "#7A6A55"), minaret(s, 420, 300, 200, 30, "#D9CBB0", GREY), s.F("rect", x=200, y=230, width=112, height=70, fill="#D9CBB0"),
                                      dome(s, 256, 230, 56, "#8D98A6")))
D["mosque-of-cordoba"] = lambda s: (s.F("rect", x=40, y=60, width=432, height=400, fill="#E8DCC8"),
                                    [s.F("path", d=f"M{x} 420 V220 C{x} 150 {x + 120} 150 {x + 120} 220 V420", fill="none") or
                                     [s.F("rect", outline=False, x=x + k * 30, y=180 + (k % 2) * 0, width=30, height=24, fill=K["red"] if k % 2 == 0 else WHITEK) for k in range(4)]
                                     for x in (60, 196, 332)], [s.T(f"M{x} 460 V230", "#C9B79A", 18) for x in (60, 180, 196, 316, 332, 452)],
                                    [s.T(f"M{x} 230 C{x} 150 {x + 120} 150 {x + 120} 230", K["red"], 22) for x in (60, 196, 332)])
D["great-mosque-of-samarra"] = site(lambda s: (ground(s, SAND, 400), s.F("polygon", points="150,420 362,420 306,100 206,100", fill="#C89B6A"),
                                               s.M("M160 380 L352 340 M180 300 L332 260 M196 220 L316 180 M206 150 L306 120", "#A57A4E", 10)))
D["al-azhar-mosque"] = site(lambda s: (minaret(s, 110, 440, 280, 30, "#D9CBB0", "#D9CBB0"), minaret(s, 400, 440, 240, 30, "#D9CBB0", "#D9CBB0"),
                                       arches(s, 60, 452, 440, 120, 6, "#D9CBB0", "#7A6A55")))
D["hassan-ii-mosque"] = site(lambda s: (s.F("rect", x=320, y=60, width=80, height=380, fill="#E8DCC8"), s.F("rect", outline=False, x=332, y=90, width=56, height=330, fill=K["green"], fill_opacity="0.4"),
                                        s.F("rect", x=60, y=320, width=260, height=120, fill="#E8DCC8"), s.F("polygon", points="60,320 190,270 320,320", fill=K["green"]),
                                        s.F("rect", outline=False, x=20, y=440, width=472, height=30, fill=K["blue"])))
D["great-mosque-of-djenne"] = site(lambda s: (ground(s, SAND, 420), s.F("rect", x=70, y=220, width=372, height=210, fill="#C68A5C"),
                                              [s.F("path", d=f"M{x} 220 V140 C{x} 120 {x + 50} 120 {x + 50} 140 V220", fill="#C68A5C") for x in (90, 230, 370)],
                                              [s.M(f"M{x} {y} h20", "#8E5A3A", 6) for x in range(90, 430, 50) for y in (260, 320, 380)]))
D["haji-ali-dargah"] = site(lambda s: (s.F("rect", outline=False, x=20, y=330, width=472, height=140, fill=K["blue"]), s.F("rect", x=60, y=370, width=200, height=16, fill=GREY),
                                       s.F("rect", x=250, y=240, width=180, height=100, fill=WHITEK), dome(s, 340, 240, 50, WHITEK, onion=True), minaret(s, 420, 340, 160, 16)))
D["ajmer-sharif-dargah"] = site(lambda s: (s.F("rect", x=130, y=280, width=252, height=170, fill=WHITEK), dome(s, 256, 280, 90, WHITEK, onion=True),
                                           s.F("path", d="M226 450 V390 C226 360 286 360 286 390 V450Z", fill=GOLD), minaret(s, 150, 280, 80, 14), minaret(s, 362, 280, 80, 14)))
D["nizamuddin-dargah"] = site(lambda s: (s.F("rect", x=130, y=280, width=252, height=170, fill=MARBLE), dome(s, 256, 280, 80, "#E8DCC8", onion=True),
                                         arches(s, 130, 382, 450, 110, 3, MARBLE, K["darkgreen"])))
D["kashi-vishwanath-temple"] = site(lambda s: P(s, hindu_temple, 256, 256, 1.0, body=GOLD, dark=GOLDD))
D["meenakshi-temple"] = site(lambda s: (P(s, D["temple-gopuram"], 256, 256, 1.0),))
D["tirupati-temple"] = site(lambda s: (s.F("rect", x=120, y=320, width=272, height=130, fill=GOLD), s.F("polygon", points="170,320 210,180 302,180 342,320", fill=GOLD),
                                       s.F("rect", x=226, y=140, width=60, height=40, fill=GOLD), s.F("circle", cx=256, cy=130, r=20, fill=GOLDD)))
D["somnath-temple"] = site(lambda s: (s.F("rect", outline=False, x=20, y=400, width=472, height=70, fill=K["blue"]), P(s, hindu_temple, 256, 230, 0.9, body="#E8C9A8", dark="#B88B5A")))
D["konark-sun-temple"] = site(lambda s: (s.F("polygon", points="80,420 130,200 382,200 432,420", fill="#B88B5A"), s.F("polygon", points="140,200 256,90 372,200", fill="#A57A4E"),
                                         P(s, dharma, 170, 380, 0.3, color="#6E4A2A"), P(s, dharma, 342, 380, 0.3, color="#6E4A2A")))
D["akshardham-temple"] = site(lambda s: (s.F("rect", x=90, y=320, width=332, height=130, fill="#E8B48A"), dome(s, 256, 320, 100, "#E8B48A", onion=True),
                                         [dome(s, x, 320, 40, "#E8B48A", onion=True) for x in (140, 372)], arches(s, 90, 422, 450, 80, 7, "#E8B48A", "#B88B5A")))
D["kedarnath-temple"] = site(lambda s: (s.F("polygon", points="20,360 120,120 220,300 320,100 492,360", fill=WHITEK), P(s, hindu_temple, 256, 320, 0.6, body="#9AA3AF", dark="#6B7280")))
D["ajanta-caves"] = site(lambda s: (s.F("path", d="M20 470 V160 C200 120 312 120 492 160 V470Z", fill="#B8936A"),
                                    [s.F("path", d=f"M{x} 380 V300 C{x} 260 {x + 60} 260 {x + 60} 300 V380Z", fill="#3A2E28") for x in (60, 170, 280, 390)]))
D["ellora-caves"] = site(lambda s: (s.F("path", d="M20 470 V120 H492 V470Z", fill="#A58B70"), P(s, hindu_temple, 256, 300, 0.7, body="#C9A87C", dark="#8C7560")))
D["lotus-temple"] = site(lambda s: (ground(s, "#9BD7A8", 400), [s.F("path", d=f"M{256 + dx} 400 C{256 + dx - 70} 300 {256 + dx - 30} 180 {256 + dx} 140 C{256 + dx + 30} 180 {256 + dx + 70} 300 {256 + dx} 400Z",
                                                                     fill=WHITEK) for dx in (-120, 120, -60, 60, 0)]))
D["sanchi-stupa"] = site(lambda s: (stupa(s, "#C9A87C"), s.T("M80 460 V300 M150 460 V300", "#8C7560", 16), s.F("rect", x=60, y=280, width=110, height=24, fill="#8C7560")))
D["mahabodhi-temple"] = site(lambda s: (s.F("polygon", points="196,450 230,90 282,90 316,450", fill="#C9A87C"), [s.F("polygon", points=f"{x - 30},450 {x - 12},280 {x + 12},280 {x + 30},450", fill="#C9A87C") for x in (130, 382)],
                                        s.F("circle", cx=256, cy=80, r=16, fill=GOLD)))
D["angkor-wat"] = site(lambda s: (s.F("rect", outline=False, x=20, y=400, width=472, height=70, fill=K["blue"]), s.F("rect", x=60, y=320, width=392, height=80, fill="#8C7560"),
                                  [s.F("path", d=f"M{x - w} 320 C{x - w} 200 {x} {h} {x} {h} C{x} {h} {x + w} 200 {x + w} 320Z", fill="#A58B70") for x, w, h in ((110, 40, 190), (402, 40, 190), (190, 46, 160), (322, 46, 160), (256, 60, 90))]))
D["borobudur"] = site(lambda s: ([s.F("rect", x=60 + i * 40, y=400 - i * 50, width=392 - i * 80, height=50, fill="#8C877E") for i in range(5)], (s.F("path", d="M226 150 C226 110 286 110 286 150Z", fill="#8C877E"), s.F("polygon", points="250,110 256,60 262,110", fill="#8C877E"))))
D["shwedagon-pagoda"] = site(lambda s: (s.F("path", d="M110 450 C150 380 200 300 230 160 L256 50 L282 160 C312 300 362 380 402 450Z", fill=GOLD),
                                        s.M("M200 330 H312 M220 250 H292", GOLDD, 8)))
D["chureito-pagoda"] = site(lambda s: (s.F("polygon", points="100,460 256,240 412,460", fill="#8FA6C9"),
                                       [s.F("path", d=f"M{256 - w} {y} C{256 - w + 20} {y - 10} {256 + w - 20} {y - 10} {256 + w} {y} L{256 + w - 30} {y - 30} H{256 - w + 30}Z", fill=K["red"])
                                        for w, y in ((120, 380), (100, 310), (80, 240), (64, 180), (50, 130))], s.T("M256 130 V60", DARK, 8)))
D["karnak-temple"] = site(lambda s: (ground(s, SAND, 400), [s.F("rect", x=x, y=160, width=56, height=250, fill="#D9B98A") for x in (60, 160, 260, 360)],
                                     [s.F("rect", x=x - 10, y=140, width=76, height=30, fill="#C9A87C") for x in (60, 160, 260, 360)]))
D["western-wall"] = lambda s: (s.F("rect", x=40, y=60, width=432, height=400, fill="#D9CBB0"),
                               [s.F("rect", outline=False, x=40 + ((r % 2) * 40) + c * 80, y=60 + r * 50, width=76, height=46, rx=4, fill="#C9B79A") for r in range(8) for c in range(-1, 6) if 40 <= 40 + ((r % 2) * 40) + c * 80 <= 420],
                               [P(s, sprout, x, y, 0.12, pot=False) for x, y in ((120, 120), (360, 180))])
D["church-of-the-holy-sepulchre"] = site(lambda s: (s.F("rect", x=90, y=260, width=332, height=190, fill="#D9CBB0"), dome(s, 330, 260, 70, "#8D98A6"),
                                                    arches(s, 110, 260, 450, 120, 2, "#D9CBB0", "#7A6A55"), s.F("rect", x=120, y=190, width=60, height=70, fill="#D9CBB0")))
D["st-peters-basilica"] = site(lambda s: (s.F("rect", x=70, y=300, width=372, height=150, fill="#E8DCC8"), [s.T(f"M{x} 450 V310", "#C9B79A", 18) for x in range(100, 430, 46)],
                                          s.F("rect", x=170, y=220, width=172, height=80, fill="#E8DCC8"), dome(s, 256, 220, 90, "#8FA6C9")))
D["notre-dame-cathedral"] = site(lambda s: (s.F("rect", x=110, y=160, width=100, height=290, fill="#D9CBB0"), s.F("rect", x=302, y=160, width=100, height=290, fill="#D9CBB0"),
                                            s.F("rect", x=200, y=230, width=112, height=220, fill="#D9CBB0"), s.F("circle", cx=256, cy=290, r=40, fill=K["blue"]),
                                            [s.F("path", d=f"M{x} 450 V400 C{x} 370 {x + 50} 370 {x + 50} 400 V450Z", fill="#7A6A55") for x in (135, 231, 327)]))
D["sagrada-familia"] = site(lambda s: [s.F("path", d=f"M{x - w} 450 C{x - w} 300 {x - 10} {h + 60} {x} {h} C{x + 10} {h + 60} {x + w} 300 {x + w} 450Z", fill="#C9A87C")
                                       for x, w, h in ((90, 30, 140), (160, 36, 90), (256, 46, 50), (352, 36, 90), (422, 30, 140))])
D["saint-basils-cathedral"] = site(lambda s: (s.F("rect", x=100, y=300, width=312, height=150, fill=K["darkred"]),
                                              [(s.F("rect", x=x - 22, y=300 - h, width=44, height=h, fill=c2), dome(s, x, 300 - h, 40, c1, onion=True, finial=True))
                                               for x, h, c1, c2 in ((150, 60, K["green"], K["red"]), (256, 140, GOLD, K["red"]), (362, 60, K["blue"], K["red"]), (200, 30, K["orange"], WHITEK), (312, 30, "#8B5CF6", WHITEK))]))
D["vaishno-devi-shrine"] = site(lambda s: (s.F("polygon", points="20,460 160,160 256,240 360,120 492,460", fill="#9C7B60"),
                                           s.F("path", d="M220 400 C220 340 292 340 292 400Z", fill="#3A2E28"), s.F("rect", x=200, y=400, width=112, height=20, fill=K["red"])))
D["jagannath-temple"] = site(lambda s: (P(s, hindu_temple, 256, 256, 1.0, body=WHITEK, dark=K["red"])))
D["brihadeeswara-temple"] = site(lambda s: (s.F("polygon", points="140,450 196,110 316,110 372,450", fill="#C9A87C"), [s.M(f"M{150 + (450 - y) // 6} {y} H{362 - (450 - y) // 6}", "#8C7560", 8) for y in range(150, 440, 40)],
                                            s.F("circle", cx=256, cy=100, r=40, fill="#C9A87C")))
D["mount-sinai"] = site(lambda s: (s.F("polygon", points="20,460 180,240 256,120 340,230 492,460", fill="#C68A5C"), s.F("polygon", outline=False, points="256,120 210,260 290,200", fill="#A0694A")))
D["cologne-cathedral"] = site(lambda s: ([s.F("polygon", points=f"{x - 40},450 {x - 40},200 {x},40 {x + 40},200 {x + 40},450", fill="#6B7280") for x in (170, 342)],
                                         s.F("rect", x=200, y=260, width=112, height=190, fill="#6B7280"), s.F("circle", cx=256, cy=320, r=30, fill=K["blue"])))
D["fushimi-inari-shrine"] = lambda s: (s.F("rect", x=20, y=40, width=472, height=432, rx=30, fill="#9BD7A8"),
                                       [P(s, D["torii-gate"], 256, 256 + k * 10, 1.0 - k * 0.18) for k in range(4)])

# text tiles handled by the text-tile tool
for _k in [k for k, v in D.items() if v is None]:
    del D[_k]


if __name__ == "__main__":
    run("religion-faith", D, sys.argv[1:] or None)
