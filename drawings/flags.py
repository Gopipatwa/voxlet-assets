"""earth-geography flags, drawn from a spec table (no downloaded artwork).

Flags are drawn in flag units (300 x 200 for 3:2) and placed on the 512 canvas with a rounded frame.
Emblems and coats of arms are simplified to read at icon size. Arabic script on flags (Saudi Arabia,
Afghanistan, Iraq, Iran) is drawn as outlines with tools/text_tile.py (fonts: see README).
Run: python drawings/flags.py [ids...]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from draw_lib import run, star_pts  # noqa: E402
from text_tile import text_path  # noqa: E402

D = {}
W_, Y_, K_ = "#FFFFFF", "#FCD116", "#000000"


class Flag:
    def __init__(self, s, name, w=300, h=200):
        self.s, self.name, self.w, self.h = s, name, w, h

    # shapes in flag units
    def r(self, x, y, w, h, c):
        self.s.F("rect", outline=False, x=f"{x:g}", y=f"{y:g}", width=f"{w:g}", height=f"{h:g}", fill=c)

    def hs(self, cols, wts=None):
        wts = wts or [1] * len(cols)
        tot, y = sum(wts), 0.0
        for c, wt in zip(cols, wts):
            hh = self.h * wt / tot
            self.r(0, y, self.w, hh + 0.5, c)
            y += hh

    def vs(self, cols, wts=None):
        wts = wts or [1] * len(cols)
        tot, x = sum(wts), 0.0
        for c, wt in zip(cols, wts):
            ww = self.w * wt / tot
            self.r(x, 0, ww + 0.5, self.h, c)
            x += ww

    def p(self, pts, c):
        self.s.F("polygon", outline=False, points=" ".join(f"{x:.1f},{y:.1f}" for x, y in pts), fill=c)

    def d(self, d, c):
        self.s.F("path", outline=False, d=d, fill=c)

    def c(self, cx, cy, r, c):
        self.s.F("circle", outline=False, cx=f"{cx:g}", cy=f"{cy:g}", r=f"{r:g}", fill=c)

    def ring(self, cx, cy, r, c, w):
        self.s.raw(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="none" stroke="{c}" stroke-width="{w:g}"/>')

    def line(self, d, c, w, cap="butt"):
        self.s.raw(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w:g}" stroke-linecap="{cap}" stroke-linejoin="round"/>')

    def star(self, cx, cy, r, c, n=5, inner=0.382, rot=-90):
        self.s.F("polygon", outline=False, points=star_pts(cx, cy, r, r * inner, n, rot), fill=c)

    def cres(self, cx, cy, r, c, bg, dx=0.28, dy=0.0, k=0.82):
        self.c(cx, cy, r, c)
        self.c(cx + dx * r, cy + dy * r, r * k, bg)

    def stars_ring(self, cx, cy, R, n, r, c, a0=-90):
        for i in range(n):
            a = math.radians(a0 + i * 360 / n)
            self.star(cx + R * math.cos(a), cy + R * math.sin(a), r, c)

    def sun(self, cx, cy, r, c, rays=12, rl=1.7, rw=0.22, a0=0):
        for i in range(rays):
            a = math.radians(a0 + i * 360 / rays)
            b1, b2 = a - rw, a + rw
            self.p([(cx + r * 0.9 * math.cos(b1), cy + r * 0.9 * math.sin(b1)), (cx + r * rl * math.cos(a), cy + r * rl * math.sin(a)),
                    (cx + r * 0.9 * math.cos(b2), cy + r * 0.9 * math.sin(b2))], c)
        self.c(cx, cy, r, c)

    def nordic(self, bg, cc, ic=None, x=105, t=40, ti=20):
        self.r(0, 0, self.w, self.h, bg)
        self.r(x - t / 2, 0, t, self.h, cc)
        self.r(0, self.h / 2 - t / 2, self.w, t, cc)
        if ic:
            self.r(x - ti / 2, 0, ti, self.h, ic)
            self.r(0, self.h / 2 - ti / 2, self.w, ti, ic)

    def uj(self, x=0, y=0, w=None, h=None):
        w = w or self.w
        h = h or self.h
        cid = f"uj-{self.name}"
        self.s.raw(f'<defs><clipPath id="{cid}"><rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"/></clipPath></defs>')
        self.s.raw(f'<g clip-path="url(#{cid})"><g transform="translate({x:g} {y:g}) scale({w / 60:.4f} {h / 30:.4f})">')
        self.r(0, 0, 60, 30, "#012169")
        self.line("M0 0 L60 30 M60 0 L0 30", W_, 6)
        self.line("M0 0 L60 30 M60 0 L0 30", "#C8102E", 2)
        self.line("M30 0 V30 M0 15 H60", W_, 10)
        self.line("M30 0 V30 M0 15 H60", "#C8102E", 6)
        self.s.raw("</g></g>")

    def diag(self, c1, c2, band=None, edge=None, bw=60, ew=12, up=True):
        """Diagonal split (lower-left to upper-right when up): c1 top-left, c2 bottom-right."""
        W, H = self.w, self.h
        self.p([(0, 0), (W, 0), (0, H)] if up else [(0, 0), (W, 0), (W, H)], c1)
        self.p([(W, 0), (W, H), (0, H)] if up else [(0, 0), (0, H), (W, H)], c2)
        d = f"M0 {H} L{W} 0" if up else f"M0 0 L{W} {H}"
        if edge:
            self.line(d, edge, bw + 2 * ew)
        if band:
            self.line(d, band, bw)

    def hoist_tri(self, c, depth=0.4):
        self.p([(0, 0), (self.w * depth, self.h / 2), (0, self.h)], c)


def flag(name, w=300, h=200, frame=True):
    def deco(fn):
        def draw(s):
            if not frame:
                k = 320 / h
                s.open(transform=f"translate({256 - w * k / 2:.1f} {256 - h * k / 2:.1f}) scale({k:.4f})")
                fn(Flag(s, name, w, h))
                s.close()
                return
            k = 440 / w if w / h >= 1.4 else 320 / h
            fw, fh = w * k, h * k
            x0, y0 = 256 - fw / 2, 256 - fh / 2
            cid = f"fc-{name}"
            rr = 12
            s.raw(f'<defs><clipPath id="{cid}"><rect width="{w}" height="{h}" rx="{rr}"/></clipPath></defs>')
            s.open(transform=f"translate({x0:.1f} {y0:.1f}) scale({k:.4f})")
            s.raw(f'<g clip-path="url(#{cid})">')
            fn(Flag(s, name, w, h))
            s.raw("</g>")
            s.close()
            s.F("rect", x=f"{x0:.1f}", y=f"{y0:.1f}", width=f"{fw:.1f}", height=f"{fh:.1f}", rx=f"{rr * k:.1f}", fill="none")
        D["flag-" + name] = draw
        return fn
    return deco


def simple(name, kind, cols, wts=None):
    flag(name)(lambda f: f.hs(cols, wts) if kind == "h" else f.vs(cols, wts))


# ---------------------------------------------------------------- plain tricolours and stripes
for _n, _k, _c, _w in (
    ("armenia", "h", ["#D90012", "#0033A0", "#F2A800"], None), ("austria", "h", ["#C8102E", W_, "#C8102E"], None),
    ("belgium", "v", [K_, "#FDDA24", "#EF3340"], None), ("bolivia", "h", ["#D52B1E", "#F9E300", "#007934"], None),
    ("bulgaria", "h", [W_, "#00966E", "#D62612"], None), ("chad", "v", ["#002664", "#FECB00", "#C60C30"], None),
    ("cote-divoire", "v", ["#F77F00", W_, "#009E60"], None), ("estonia", "h", ["#0072CE", K_, W_], None),
    ("france", "v", ["#002395", W_, "#ED2939"], None), ("gabon", "h", ["#009E60", "#FCD116", "#3A75C4"], None),
    ("germany", "h", [K_, "#DD0000", "#FFCE00"], None), ("guinea", "v", ["#CE1126", "#FCD116", "#009460"], None),
    ("hungary", "h", ["#CE2939", W_, "#477050"], None), ("indonesia", "h", ["#CE1126", W_], None),
    ("ireland", "v", ["#169B62", W_, "#FF883E"], None), ("italy", "v", ["#009246", W_, "#CE2B37"], None),
    ("latvia", "h", ["#9E3039", W_, "#9E3039"], [2, 1, 2]), ("lithuania", "h", ["#FDB913", "#006A44", "#C1272D"], None),
    ("luxembourg", "h", ["#EF3340", W_, "#00A3E0"], None), ("mali", "v", ["#14B53A", "#FCD116", "#CE1126"], None),
    ("mauritius", "h", ["#EA2839", "#1A206D", "#FFD500", "#00A551"], None), ("monaco", "h", ["#CE1126", W_], None),
    ("netherlands", "h", ["#AE1C28", W_, "#21468B"], None), ("nigeria", "v", ["#008751", W_, "#008751"], None),
    ("peru", "v", ["#D91023", W_, "#D91023"], None), ("poland", "h", [W_, "#DC143C"], None),
    ("romania", "v", ["#002B7F", "#FCD116", "#CE1126"], None), ("russia", "h", [W_, "#0039A6", "#D52B1E"], None),
    ("sierra-leone", "h", ["#1EB53A", W_, "#0072C6"], None), ("ukraine", "h", ["#0057B7", "#FFD700"], None),
    ("yemen", "h", ["#CE1126", W_, K_], None), ("colombia", "h", ["#FCD116", "#003893", "#CE1126"], [2, 1, 1]),
    ("gambia", "h", ["#CE1126", W_, "#0C1C8C", W_, "#3A7728"], [6, 1, 4, 1, 6]),
    ("thailand", "h", ["#A51931", W_, "#2D2A4A", W_, "#A51931"], [1, 1, 2, 1, 1]),
    ("costa-rica", "h", ["#002B7F", W_, "#CE1126", W_, "#002B7F"], [1, 1, 2, 1, 1]),
):
    simple(_n, _k, _c, _w)


# ---------------------------------------------------------------- Asia
@flag("azerbaijan")
def _(f):
    f.hs(["#00B5E2", "#EF3340", "#509E2F"])
    f.cres(140, 100, 30, W_, "#EF3340", 0.25)
    f.star(178, 100, 14, W_, 8, 0.5)


@flag("bahrain")
def _(f):
    f.r(0, 0, 300, 200, "#CE1126")
    pts = [(0, 0), (75, 0)]
    for i in range(5):
        y0 = i * 40
        pts += [(115, y0 + 20), (75, y0 + 40)]
    pts += [(0, 200)]
    f.p(pts, W_)


@flag("bangladesh")
def _(f):
    f.r(0, 0, 300, 200, "#006A4E")
    f.c(135, 100, 60, "#F42A41")


@flag("bhutan")
def _(f):
    f.p([(0, 0), (300, 0), (0, 200)], "#FFD520")
    f.p([(300, 0), (300, 200), (0, 200)], "#FF4E12")
    f.line("M70 150 C110 110 120 150 150 110 C180 70 200 110 230 60", W_, 22, "round")
    f.c(232, 58, 16, W_)
    for x, y in ((90, 128), (140, 118), (190, 86)):
        f.c(x, y + 18, 8, W_)


@flag("brunei")
def _(f):
    f.r(0, 0, 300, 200, "#F7E017")
    f.p([(0, 30), (300, 130), (300, 160), (0, 60)], W_)
    f.p([(0, 60), (300, 160), (300, 190), (0, 90)], K_)
    f.cres(150, 112, 34, "#CF1126", "#F7E017", 0, -0.35, 0.8)
    f.r(146, 58, 8, 56, "#CF1126")
    f.p([(120, 66), (180, 66), (150, 48)], "#CF1126")


@flag("cambodia")
def _(f):
    f.hs(["#032EA1", "#E00025", "#032EA1"], [1, 2, 1])
    f.r(95, 110, 110, 22, W_)
    for x, h in ((110, 30), (130, 40), (150, 56), (170, 40), (190, 30)):
        f.p([(x - 9, 110), (x - 6, 110 - h + 10), (x, 110 - h), (x + 6, 110 - h + 10), (x + 9, 110)], W_)


@flag("china")
def _(f):
    f.r(0, 0, 300, 200, "#EE1C25")
    f.star(50, 50, 30, "#FFFF00")
    for x, y, a in ((100, 20, -40), (120, 40, -10), (120, 70, 15), (100, 90, 40)):
        f.star(x, y, 10, "#FFFF00", rot=-90 + a)


@flag("cyprus")
def _(f):
    f.r(0, 0, 300, 200, W_)
    f.d("M90 80 C120 60 190 50 230 60 C220 75 200 80 210 95 C180 105 150 100 120 110 C100 108 85 95 90 80 Z", "#D57800")
    f.line("M110 150 C130 140 150 140 150 140 M190 150 C170 140 150 140 150 140", "#4E5B31", 8, "round")


@flag("georgia")
def _(f):
    f.r(0, 0, 300, 200, W_)
    f.r(130, 0, 40, 200, "#FF0000")
    f.r(0, 80, 300, 40, "#FF0000")
    for x, y in ((65, 40), (235, 40), (65, 160), (235, 160)):
        f.r(x - 4, y - 18, 8, 36, "#FF0000")
        f.r(x - 18, y - 4, 36, 8, "#FF0000")


@flag("india")
def _(f):
    f.hs(["#FF9933", W_, "#138808"])
    f.ring(150, 100, 26, "#000080", 5)
    for i in range(24):
        a = math.radians(i * 15)
        f.line(f"M150 100 L{150 + 26 * math.cos(a):.1f} {100 + 26 * math.sin(a):.1f}", "#000080", 2)
    f.c(150, 100, 5, "#000080")


@flag("israel")
def _(f):
    f.r(0, 0, 300, 200, W_)
    f.r(0, 20, 300, 30, "#0038B8")
    f.r(0, 150, 300, 30, "#0038B8")
    for rot in (-90, 90):
        pts = []
        for i in range(3):
            a = math.radians(rot + i * 120)
            pts.append(f"{150 + 36 * math.cos(a):.1f},{100 + 36 * math.sin(a):.1f}")
        f.s.raw(f'<polygon points="{" ".join(pts)}" fill="none" stroke="#0038B8" stroke-width="8" stroke-linejoin="miter"/>')


@flag("japan")
def _(f):
    f.r(0, 0, 300, 200, W_)
    f.c(150, 100, 60, "#BC002D")


@flag("jordan")
def _(f):
    f.hs([K_, W_, "#007A3D"])
    f.hoist_tri("#CE1126", 0.5)
    f.star(55, 100, 16, W_, 7, 0.5)


@flag("kazakhstan")
def _(f):
    f.r(0, 0, 300, 200, "#00AFCA")
    f.sun(160, 80, 26, "#FEC50C", 32, 1.45, 0.06)
    f.d("M100 130 C130 110 150 130 160 120 C170 130 190 110 220 130 C190 140 175 132 160 140 C145 132 130 140 100 130 Z", "#FEC50C")
    for y in range(10, 200, 24):
        f.p([(22, y), (30, y + 10), (22, y + 20), (14, y + 10)], "#FEC50C")


@flag("kuwait")
def _(f):
    f.hs(["#007A3D", W_, "#CE1126"])
    f.p([(0, 0), (75, 67), (75, 133), (0, 200)], K_)


@flag("kyrgyzstan")
def _(f):
    f.r(0, 0, 300, 200, "#E8112D")
    f.sun(150, 100, 40, "#FFEF00", 40, 1.55, 0.05)
    f.c(150, 100, 26, "#E8112D")
    f.ring(150, 100, 22, "#FFEF00", 5)
    f.line("M130 96 C140 86 160 86 170 96 M130 106 C140 116 160 116 170 106 M140 82 V118 M160 82 V118", "#FFEF00", 4)


@flag("laos")
def _(f):
    f.hs(["#CE1126", "#002868", "#CE1126"], [1, 2, 1])
    f.c(150, 100, 40, W_)


@flag("lebanon")
def _(f):
    f.hs(["#ED1C24", W_, "#ED1C24"], [1, 2, 1])
    f.p([(150, 58), (190, 100), (172, 100), (200, 128), (100, 128), (128, 100), (110, 100)], "#00A651")
    f.r(144, 128, 12, 14, "#00A651")


@flag("malaysia")
def _(f):
    f.hs(["#CC0001", W_] * 7)
    f.r(0, 0, 150, 114, "#010066")
    f.cres(58, 57, 36, "#FFCC00", "#010066", 0.26)
    f.star(112, 57, 26, "#FFCC00", 14, 0.45)


@flag("maldives")
def _(f):
    f.r(0, 0, 300, 200, "#D21034")
    f.r(50, 50, 200, 100, "#007E3A")
    f.cres(150, 100, 34, W_, "#007E3A", 0.32)


@flag("mongolia")
def _(f):
    f.vs(["#C4272F", "#015197", "#C4272F"])
    x = 50
    f.p([(x, 26), (x - 8, 40), (x + 8, 40)], "#F9CF02")
    f.c(x, 52, 9, "#F9CF02")
    f.cres(x, 66, 12, "#F9CF02", "#C4272F", 0, -0.45)
    f.r(x - 16, 82, 32, 8, "#F9CF02")
    f.r(x - 16, 140, 32, 8, "#F9CF02")
    f.c(x, 115, 16, "#F9CF02")
    f.r(x - 30, 82, 8, 66, "#F9CF02")
    f.r(x + 22, 82, 8, 66, "#F9CF02")


@flag("myanmar")
def _(f):
    f.hs(["#FECB00", "#34B233", "#EA2839"])
    f.star(150, 112, 70, W_)


@flag("nepal", w=240, h=300, frame=False)
def _(f):
    shape = "M20 10 L210 150 H90 L210 290 H20 Z"
    f.s.raw(f'<path d="{shape}" fill="#DC143C" stroke="#003893" stroke-width="16" stroke-linejoin="miter"/>')
    f.cres(70, 110, 26, W_, "#DC143C", 0, -0.5, 0.85)
    f.sun(70, 232, 18, W_, 12, 1.5, 0.14)


@flag("north-korea")
def _(f):
    f.hs(["#024FA2", W_, "#ED1C27", W_, "#024FA2"], [6, 1, 17, 1, 6])
    f.c(100, 100, 42, W_)
    f.star(100, 100, 40, "#ED1C27")


@flag("oman")
def _(f):
    f.hs([W_, "#DB161B", "#008000"])
    f.r(0, 0, 80, 200, "#DB161B")
    f.line("M22 22 L58 58 M58 22 L22 58 M40 18 V60", W_, 6, "round")


@flag("pakistan")
def _(f):
    f.r(0, 0, 300, 200, "#01411C")
    f.r(0, 0, 75, 200, W_)
    f.cres(190, 100, 50, W_, "#01411C", 0.22, -0.2, 0.82)
    f.star(214, 72, 16, W_, rot=-60)


@flag("palestine")
def _(f):
    f.hs([K_, W_, "#007A3D"])
    f.hoist_tri("#CE1126", 0.5)


@flag("philippines")
def _(f):
    f.hs(["#0038A8", "#CE1126"])
    f.hoist_tri(W_, 0.5)
    f.sun(52, 100, 14, "#FCD116", 8, 2.0, 0.2)
    for x, y in ((14, 18), (14, 182), (128, 100)):
        f.star(x, y, 10, "#FCD116")


@flag("qatar")
def _(f):
    f.r(0, 0, 300, 200, "#8A1538")
    pts = [(0, 0), (80, 0)]
    for i in range(9):
        y0 = i * 200 / 9
        pts += [(120, y0 + 100 / 9), (80, y0 + 200 / 9)]
    pts += [(0, 200)]
    f.p(pts, W_)


@flag("singapore")
def _(f):
    f.hs(["#EF3340", W_])
    f.cres(60, 50, 32, W_, "#EF3340", 0.3)
    f.stars_ring(92, 50, 18, 5, 7, W_)


@flag("south-korea")
def _(f):
    f.r(0, 0, 300, 200, W_)
    f.c(150, 100, 50, "#0047A0")
    f.d("M100 100 A50 50 0 0 1 200 100 A25 25 0 0 1 150 100 A25 25 0 0 0 100 100 Z", "#CD2E3A")
    f.s.raw('<g transform="rotate(33.7 150 100)"><path d="M100 100 A50 50 0 0 1 200 100 A25 25 0 0 1 150 100 A25 25 0 0 0 100 100 Z" fill="#CD2E3A"/>'
            '<path d="M100 100 A50 50 0 0 0 200 100 A25 25 0 0 0 150 100 A25 25 0 0 1 100 100 Z" fill="#0047A0"/></g>')
    for cx, cy, rot in ((60, 42, 56), (240, 42, -56), (60, 158, -56), (240, 158, 56)):
        f.s.raw(f'<g transform="rotate({rot} {cx} {cy})">')
        for i in range(3):
            f.r(cx - 22, cy - 15 + i * 11, 44, 7, K_)
        f.s.raw("</g>")


@flag("sri-lanka")
def _(f):
    f.r(0, 0, 300, 200, "#FFBE29")
    f.r(12, 12, 36, 176, "#00534E")
    f.r(52, 12, 36, 176, "#EB7400")
    f.r(96, 12, 192, 176, "#8D153A")
    f.d("M140 150 C140 120 150 100 180 96 C190 70 210 60 230 70 C246 80 244 100 236 110 C250 120 254 140 250 150 Z", "#FFBE29")
    f.line("M150 150 V170 M240 150 V170 M236 92 L262 56", "#FFBE29", 7, "round")


@flag("syria")
def _(f):
    f.hs(["#007A3D", W_, K_])
    for x in (100, 150, 200):
        f.star(x, 100, 20, "#CE1126")


@flag("taiwan")
def _(f):
    f.r(0, 0, 300, 200, "#FE0000")
    f.r(0, 0, 150, 100, "#000095")
    f.sun(75, 50, 18, W_, 12, 1.8, 0.16)
    f.c(75, 50, 16, "#000095")
    f.c(75, 50, 13, W_)


@flag("tajikistan")
def _(f):
    f.hs(["#CC0000", W_, "#006600"], [2, 3, 2])
    f.d("M132 112 H168 L172 96 L160 104 L150 90 L140 104 L128 96 Z", "#F8C300")
    for i in range(7):
        a = math.radians(-160 + i * 23.3)
        f.star(150 + 42 * math.cos(a), 108 + 34 * math.sin(a), 6, "#F8C300")


@flag("timor-leste")
def _(f):
    f.r(0, 0, 300, 200, "#DC241F")
    f.hoist_tri("#FFC726", 0.5)
    f.hoist_tri(K_, 0.33)
    f.star(34, 100, 20, W_, rot=-60)


@flag("turkiye")
def _(f):
    f.r(0, 0, 300, 200, "#E30A17")
    f.cres(112, 100, 50, W_, "#E30A17", 0.25, 0, 0.8)
    f.star(178, 100, 24, W_, rot=180)


@flag("turkmenistan")
def _(f):
    f.r(0, 0, 300, 200, "#00843D")
    f.r(36, 0, 54, 200, "#D22630")
    for y in range(14, 200, 36):
        f.d(f"M63 {y} L82 {y + 14} L63 {y + 28} L44 {y + 14} Z", "#FFB81C")
        f.c(63, y + 14, 6, "#00843D")
    f.cres(130, 50, 24, W_, "#00843D", 0.3)
    for x, y in ((150, 30), (164, 42), (170, 60), (152, 52), (164, 74)):
        f.star(x, y, 6, W_)


@flag("united-arab-emirates")
def _(f):
    f.hs(["#00732F", W_, K_])
    f.r(0, 0, 75, 200, "#FF0000")


@flag("uzbekistan")
def _(f):
    f.hs(["#0099B5", "#CE1126", W_, "#CE1126", "#1EB53A"], [10, 1, 10, 1, 10])
    f.cres(40, 32, 20, W_, "#0099B5", 0.3)
    for row, n in ((0, 3), (1, 4), (2, 5)):
        for i in range(n):
            f.star(120 - i * 16, 18 + row * 15, 5, W_)


@flag("vietnam")
def _(f):
    f.r(0, 0, 300, 200, "#DA251D")
    f.star(150, 104, 60, "#FFFF00")


# ---------------------------------------------------------------- Africa
@flag("algeria")
def _(f):
    f.vs(["#006233", W_])
    f.cres(155, 100, 50, "#D21034", W_, 0.3, 0, 0.82)
    f.star(178, 100, 22, "#D21034", rot=180)


@flag("angola")
def _(f):
    f.hs(["#CC092F", K_])
    f.s.raw('<path d="M120 130 A50 50 0 1 0 190 80" fill="none" stroke="#FFCB00" stroke-width="12" stroke-dasharray="10 5"/>')
    f.line("M118 136 L170 84", "#FFCB00", 12)
    f.star(150, 92, 14, "#FFCB00")


@flag("benin")
def _(f):
    f.r(0, 0, 300, 100, "#FCD116")
    f.r(0, 100, 300, 100, "#E8112D")
    f.r(0, 0, 120, 200, "#008751")


@flag("botswana")
def _(f):
    f.hs(["#75AADB", W_, K_, W_, "#75AADB"], [9, 1, 4, 1, 9])


@flag("burkina-faso")
def _(f):
    f.hs(["#EF2B2D", "#009E49"])
    f.star(150, 100, 34, "#FCD116")


@flag("burundi")
def _(f):
    f.p([(0, 0), (300, 0), (150, 100)], "#CE1126")
    f.p([(0, 200), (300, 200), (150, 100)], "#CE1126")
    f.p([(0, 0), (0, 200), (150, 100)], "#1EB53A")
    f.p([(300, 0), (300, 200), (150, 100)], "#1EB53A")
    f.line("M0 0 L300 200 M300 0 L0 200", W_, 30)
    f.c(150, 100, 50, W_)
    for x, y in ((150, 78), (130, 114), (170, 114)):
        f.star(x, y, 14, "#CE1126", 6, 0.55)


@flag("cabo-verde")
def _(f):
    f.hs(["#003893", W_, "#CF2027", W_, "#003893"], [6, 1, 1, 1, 3])
    f.stars_ring(110, 125, 46, 10, 8, "#F7D116")


@flag("cameroon")
def _(f):
    f.vs(["#007A5E", "#CE1126", "#FCD116"])
    f.star(150, 100, 26, "#FCD116")


@flag("central-african-republic")
def _(f):
    f.hs(["#003082", W_, "#289728", "#FFCE00"])
    f.r(125, 0, 50, 200, "#D21034")
    f.star(40, 25, 16, "#FFCE00")


@flag("comoros")
def _(f):
    f.hs(["#FFC61E", W_, "#CE1126", "#3A75C4"])
    f.hoist_tri("#3D8E33", 0.5)
    f.cres(46, 100, 32, W_, "#3D8E33", 0.32)
    for y in (76, 92, 108, 124):
        f.star(64, y, 5, W_)


@flag("democratic-republic-of-the-congo")
def _(f):
    f.r(0, 0, 300, 200, "#007FFF")
    f.line("M0 200 L300 0", "#F7D618", 70)
    f.line("M0 200 L300 0", "#CE1021", 48)
    f.star(50, 44, 30, "#F7D618")


@flag("republic-of-the-congo")
def _(f):
    f.diag("#009543", "#DC241F", "#FBDE4A", None, 80, up=True)


@flag("djibouti")
def _(f):
    f.hs(["#6AB2E7", "#12AD2B"])
    f.hoist_tri(W_, 0.5)
    f.star(50, 100, 16, "#D7141A")


@flag("egypt")
def _(f):
    f.hs(["#CE1126", W_, K_])
    f.d("M130 82 C140 74 160 74 170 82 L176 120 L150 130 L124 120 Z", "#C09300")
    f.c(150, 76, 7, "#C09300")


@flag("equatorial-guinea")
def _(f):
    f.hs(["#3E9A00", W_, "#E32118"])
    f.hoist_tri("#0073CE", 0.25)
    f.d("M140 80 H160 V118 L150 126 L140 118 Z", "#C8C8C8")
    f.c(150, 90, 8, "#3E9A00")


@flag("eritrea")
def _(f):
    f.p([(0, 0), (300, 0), (300, 100), (0, 0)], "#12AD2B")
    f.p([(0, 200), (300, 200), (300, 100)], "#4189DD")
    f.p([(0, 0), (300, 100), (0, 200)], "#EA0437")
    f.ring(70, 100, 34, "#FFC726", 8)
    f.line("M70 128 V80", "#FFC726", 6)


@flag("eswatini")
def _(f):
    f.hs(["#3E5EB9", "#FFD900", "#B10C0C", "#FFD900", "#3E5EB9"], [3, 1, 6, 1, 3])
    f.line("M60 100 H240", "#FFD900", 5)
    f.s.raw('<ellipse cx="150" cy="100" rx="58" ry="28" fill="#000000"/>')
    f.d("M150 72 A58 28 0 0 1 150 128 Z", W_)


@flag("ethiopia")
def _(f):
    f.hs(["#078930", "#FCDD09", "#DA121A"])
    f.c(150, 100, 40, "#0F47AF")
    f.s.raw(f'<polygon points="{star_pts(150, 102, 30, 12, 5)}" fill="none" stroke="#FCDD09" stroke-width="5"/>')


@flag("ghana")
def _(f):
    f.hs(["#CE1126", "#FCD116", "#006B3F"])
    f.star(150, 102, 30, K_)


@flag("guinea-bissau")
def _(f):
    f.r(0, 0, 300, 100, "#FCD116")
    f.r(0, 100, 300, 100, "#009E49")
    f.r(0, 0, 100, 200, "#CE1126")
    f.star(50, 100, 28, K_)


@flag("kenya")
def _(f):
    f.hs([K_, W_, "#BB0000", W_, "#006600"], [6, 1, 6, 1, 6])
    f.line("M110 160 L190 40 M190 160 L110 40", W_, 6)
    f.s.raw('<ellipse cx="150" cy="100" rx="26" ry="60" fill="#BB0000"/>')
    f.s.raw('<path d="M150 40 A26 60 0 0 0 150 160 Z" fill="#000000"/>')
    f.s.raw('<ellipse cx="150" cy="100" rx="8" ry="40" fill="#FFFFFF"/>')


@flag("lesotho")
def _(f):
    f.hs(["#00209F", W_, "#009543"], [3, 4, 3])
    f.d("M150 72 L176 120 H124 Z", K_)
    f.r(118, 116, 64, 8, K_)


@flag("liberia")
def _(f):
    f.hs(["#BF0A30", W_] * 5 + ["#BF0A30"])
    f.r(0, 0, 91, 91, "#002868")
    f.star(45, 46, 30, W_)


@flag("libya")
def _(f):
    f.hs(["#E70013", K_, "#239E46"], [1, 2, 1])
    f.cres(144, 100, 26, W_, K_, 0.3)
    f.star(172, 100, 12, W_, rot=180)


@flag("madagascar")
def _(f):
    f.r(0, 0, 300, 100, "#FC3D32")
    f.r(0, 100, 300, 100, "#007E3A")
    f.r(0, 0, 100, 200, W_)


@flag("malawi")
def _(f):
    f.hs([K_, "#CE1126", "#339E35"])
    f.sun(150, 70, 22, "#CE1126", 31, 1.7, 0.07)
    f.r(100, 66.7, 100, 30, "#CE1126")


@flag("mauritania")
def _(f):
    f.hs(["#D01C1F", "#00A95C", "#D01C1F"], [1, 6, 1])
    f.cres(150, 92, 46, "#FFD700", "#00A95C", 0, -0.32, 0.86)
    f.star(150, 76, 16, "#FFD700")


@flag("morocco")
def _(f):
    f.r(0, 0, 300, 200, "#C1272D")
    f.s.raw('<polygon points="' + " ".join(f"{150 + 52 * math.cos(math.radians(-90 + i * 144)):.1f},{104 + 52 * math.sin(math.radians(-90 + i * 144)):.1f}" for i in range(5)) + '" fill="none" stroke="#006233" stroke-width="7"/>')


@flag("mozambique")
def _(f):
    f.hs(["#007168", W_, K_, W_, "#FCE100"], [6, 1, 6, 1, 6])
    f.hoist_tri("#D21034", 0.45)
    f.star(46, 100, 32, "#FCE100")
    f.r(34, 96, 24, 16, W_)
    f.line("M28 118 L64 84 M64 118 L28 84", K_, 4)


@flag("namibia")
def _(f):
    f.diag("#003580", "#009A44", "#D21034", W_, 50, 10, up=True)
    f.sun(60, 50, 16, "#FFCE00", 12, 1.7, 0.16)


@flag("niger")
def _(f):
    f.hs(["#E05206", W_, "#0DB02B"])
    f.c(150, 100, 22, "#E05206")


@flag("rwanda")
def _(f):
    f.hs(["#20603D", "#FAD201", "#00A1DE"][::-1], [1, 1, 2][::-1])
    f.sun(240, 50, 16, "#FAD201", 24, 1.8, 0.09)
    f.c(240, 50, 12, "#00A1DE")
    f.c(240, 50, 10, "#FAD201")


@flag("sao-tome-and-principe")
def _(f):
    f.hs(["#12AD2B", "#FFCE00", "#12AD2B"], [2, 3, 2])
    f.hoist_tri("#D21034", 0.3)
    f.star(160, 100, 20, K_)
    f.star(230, 100, 20, K_)


@flag("senegal")
def _(f):
    f.vs(["#00853F", "#FDEF42", "#E31B23"])
    f.star(150, 102, 26, "#00853F")


@flag("seychelles")
def _(f):
    f.r(0, 0, 300, 200, "#007A3D")
    for pts, c in (([(0, 200), (0, 0), (100, 0)], "#003F87"), ([(0, 200), (100, 0), (200, 0)], "#FCD856"),
                   ([(0, 200), (200, 0), (300, 0), (300, 66)], "#D62828"), ([(0, 200), (300, 66), (300, 133)], W_)):
        f.p(pts, c)


@flag("somalia")
def _(f):
    f.r(0, 0, 300, 200, "#4189DD")
    f.star(150, 104, 46, W_)


@flag("south-africa")
def _(f):
    f.r(0, 0, 300, 100, "#E03C31")
    f.r(0, 100, 300, 100, "#001489")
    f.line("M0 0 L120 100 H300 M0 200 L120 100", W_, 66)
    f.line("M0 0 L120 100 H300 M0 200 L120 100", "#007749", 40)
    f.p([(0, 30), (84, 100), (0, 170)], "#FFB81C")
    f.p([(0, 46), (64, 100), (0, 154)], K_)


@flag("south-sudan")
def _(f):
    f.hs([K_, W_, "#DA121A", W_, "#078930"], [6, 1, 6, 1, 6])
    f.hoist_tri("#0F47AF", 0.4)
    f.star(40, 100, 20, "#FCDD09")


@flag("sudan")
def _(f):
    f.hs(["#D21034", W_, K_])
    f.hoist_tri("#007229", 0.33)


@flag("tanzania")
def _(f):
    f.diag("#1EB53A", "#00A3DD", K_, "#FCD116", 50, 10, up=True)


@flag("togo")
def _(f):
    f.hs(["#006A4E", "#FFCE00"] * 2 + ["#006A4E"])
    f.r(0, 0, 120, 120, "#D21034")
    f.star(60, 60, 34, W_)


@flag("tunisia")
def _(f):
    f.r(0, 0, 300, 200, "#E70013")
    f.c(150, 100, 50, W_)
    f.cres(146, 100, 36, "#E70013", W_, 0.26, 0, 0.8)
    f.star(160, 100, 18, "#E70013", rot=180)


@flag("uganda")
def _(f):
    f.hs([K_, "#FCDC04", "#D90000"] * 2)
    f.c(150, 100, 36, W_)
    f.d("M140 80 C150 70 162 76 160 90 C170 100 170 116 156 120 L150 128 L146 120 C136 116 134 100 140 90 Z", "#9CA69C")
    f.line("M158 76 L166 66", "#D90000", 4, "round")


@flag("zambia")
def _(f):
    f.r(0, 0, 300, 200, "#198A00")
    f.r(195, 90, 35, 110, "#DE2010")
    f.r(230, 90, 35, 110, K_)
    f.r(265, 90, 35, 110, "#EF7D00")
    f.d("M210 60 C230 46 250 56 255 66 C260 56 280 46 300 60 C280 66 270 72 255 80 C240 72 230 66 210 60 Z", "#EF7D00")


@flag("zimbabwe")
def _(f):
    f.hs(["#319208", "#FFD200", "#DE2010", K_, "#DE2010", "#FFD200", "#319208"])
    f.s.raw('<polygon points="0,0 120,100 0,200" fill="#FFFFFF" stroke="#000000" stroke-width="6"/>')
    f.star(44, 100, 26, "#DE2010")
    f.d("M38 86 H52 V112 L46 118 L40 112 Z", "#FFD200")


# ---------------------------------------------------------------- Europe
@flag("albania")
def _(f):
    f.r(0, 0, 300, 200, "#E41E20")
    f.d("M150 60 L160 80 L200 60 L190 100 L210 110 L170 120 L160 150 H140 L130 120 L90 110 L110 100 L100 60 L140 80 Z", K_)


@flag("andorra")
def _(f):
    f.vs(["#10069F", "#FEDD00", "#D50032"], [8, 9, 8])
    f.d("M128 74 H172 V112 C172 128 160 136 150 140 C140 136 128 128 128 112 Z", "#C7B37F")
    f.r(132, 78, 16, 24, "#D50032")
    f.r(152, 78, 16, 24, "#FEDD00")


@flag("belarus")
def _(f):
    f.hs(["#C8313E", "#4AA657"], [2, 1])
    f.r(0, 0, 44, 200, W_)
    for y in range(0, 200, 30):
        f.d(f"M22 {y + 4} L38 {y + 15} L22 {y + 26} L6 {y + 15} Z", "#C8313E")


@flag("bosnia-and-herzegovina")
def _(f):
    f.r(0, 0, 300, 200, "#002395")
    f.p([(70, 0), (230, 0), (230, 200)], "#FECB00")
    for i in range(9):
        tt = (i + 0.5) / 9.5
        f.star(70 + 160 * tt - 26, 200 * tt - 6, 10, W_)


@flag("croatia")
def _(f):
    f.hs(["#FF0000", W_, "#171796"])
    f.d("M122 66 H178 V112 C178 132 160 140 150 144 C140 140 122 132 122 112 Z", W_)
    for i in range(5):
        for j in range(5):
            if (i + j) % 2 == 0:
                f.r(122 + j * 11.2, 66 + i * 11.2, 11.2, 11.2, "#FF0000")
    f.s.raw('<path d="M122 66 H178 V112 C178 132 160 140 150 144 C140 140 122 132 122 112 Z" fill="none" stroke="#171796" stroke-width="3"/>')


@flag("czechia")
def _(f):
    f.hs([W_, "#D7141A"])
    f.hoist_tri("#11457E", 0.5)


@flag("denmark")
def _(f):
    f.nordic("#C8102E", W_, x=110, t=30)


@flag("finland")
def _(f):
    f.nordic(W_, "#002F6C", x=105, t=50)


@flag("greece")
def _(f):
    f.hs(["#0D5EAF", W_] * 4 + ["#0D5EAF"])
    f.r(0, 0, 111, 111, "#0D5EAF")
    f.r(44, 0, 22, 111, W_)
    f.r(0, 44, 111, 22, W_)


@flag("iceland")
def _(f):
    f.nordic("#02529C", W_, "#DC1E35", x=105, t=44, ti=22)


@flag("kosovo")
def _(f):
    f.r(0, 0, 300, 200, "#244AA5")
    f.d("M110 90 L140 80 L170 86 L196 100 L190 140 L160 156 L126 150 L108 124 Z", "#D0A650")
    for i in range(6):
        a = math.radians(-150 + i * 24)
        f.star(150 + 70 * math.cos(a), 112 + 50 * math.sin(a), 9, W_)


@flag("liechtenstein")
def _(f):
    f.hs(["#002B7F", "#CE1126"])
    f.d("M56 30 L60 50 H100 L104 30 L92 40 L80 26 L68 40 Z", "#FFD83D")
    f.r(58, 50, 44, 8, "#FFD83D")


@flag("malta")
def _(f):
    f.vs([W_, "#CF142B"])
    f.r(28, 14, 30, 30, "#A0A0A0")
    f.r(28 + 10, 14, 10, 30, "#C8C8C8")
    f.r(28, 14 + 10, 30, 10, "#C8C8C8")


@flag("moldova")
def _(f):
    f.vs(["#003DA5", "#FFD200", "#CC092F"])
    f.d("M130 70 C140 60 160 60 170 70 L180 110 L150 140 L120 110 Z", "#B07E2B")
    f.d("M136 90 H164 V118 L150 128 L136 118 Z", "#CC092F")


@flag("montenegro")
def _(f):
    f.r(0, 0, 300, 200, "#C40308")
    f.s.raw('<rect x="6" y="6" width="288" height="188" fill="none" stroke="#D3AE3B" stroke-width="12"/>')
    f.d("M150 60 L160 80 L200 64 L190 104 L206 112 L170 120 L160 150 H140 L130 120 L94 112 L110 104 L100 64 L140 80 Z", "#D3AE3B")


@flag("north-macedonia")
def _(f):
    f.r(0, 0, 300, 200, "#D20000")
    for a in range(0, 360, 45):
        r = math.radians(a)
        cx, cy = 150, 100
        w = math.radians(10)
        f.p([(cx, cy), (cx + 260 * math.cos(r - w), cy + 260 * math.sin(r - w)), (cx + 260 * math.cos(r + w), cy + 260 * math.sin(r + w))], "#FFE600")
    f.c(150, 100, 30, "#D20000")
    f.c(150, 100, 24, "#FFE600")


@flag("norway")
def _(f):
    f.nordic("#BA0C2F", W_, "#00205B", x=105, t=44, ti=22)


@flag("portugal")
def _(f):
    f.vs(["#006600", "#FF0000"], [2, 3])
    f.ring(120, 100, 40, "#FFE900", 10)
    f.d("M102 76 H138 V108 C138 124 128 130 120 132 C112 130 102 124 102 108 Z", W_)
    f.d("M108 82 H132 V106 C132 118 126 122 120 124 C114 122 108 118 108 106 Z", "#FF0000")


@flag("san-marino")
def _(f):
    f.hs([W_, "#5EB6E4"])
    f.d("M130 70 H170 V110 C170 128 160 136 150 140 C140 136 130 128 130 110 Z", "#5EB6E4")
    for x in (138, 150, 162):
        f.r(x - 4, 84, 8, 22, W_)
    f.s.raw('<path d="M130 70 H170 V110 C170 128 160 136 150 140 C140 136 130 128 130 110 Z" fill="none" stroke="#D4A73B" stroke-width="4"/>')


@flag("serbia")
def _(f):
    f.hs(["#C6363C", "#0C4076", W_])
    f.d("M80 60 H130 V110 C130 130 116 140 105 144 C94 140 80 130 80 110 Z", "#C6363C")
    f.line("M105 70 V130 M88 100 H122", W_, 8)


@flag("slovakia")
def _(f):
    f.hs([W_, "#0B4EA2", "#EE1C25"])
    f.s.raw('<path d="M70 50 H140 V110 C140 140 118 152 105 158 C92 152 70 140 70 110 Z" fill="#EE1C25" stroke="#FFFFFF" stroke-width="5"/>')
    f.line("M105 62 V132 M86 84 H124 M92 102 H118", W_, 7)
    f.d("M76 130 C86 118 96 118 105 130 C114 118 124 118 134 130 C126 146 116 152 105 156 C94 152 84 146 76 130 Z", "#0B4EA2")


@flag("slovenia")
def _(f):
    f.hs([W_, "#005DA4", "#ED1C24"])
    f.s.raw('<path d="M58 30 H110 V70 C110 90 96 98 84 102 C72 98 58 90 58 70 Z" fill="#005DA4" stroke="#ED1C24" stroke-width="4"/>')
    f.p([(62, 80), (76, 56), (84, 66), (92, 56), (106, 80)], W_)
    f.star(84, 42, 5, "#FFDD00", 6)


@flag("spain")
def _(f):
    f.hs(["#AA151B", "#F1BF00", "#AA151B"], [1, 2, 1])
    f.d("M80 70 H120 V110 C120 124 108 132 100 134 C92 132 80 124 80 110 Z", "#AA151B")
    f.r(80, 70, 20, 32, "#AA151B")
    f.r(100, 70, 20, 32, "#C8B100")
    f.r(70, 70, 8, 60, "#C8B100")
    f.r(122, 70, 8, 60, "#C8B100")


@flag("sweden")
def _(f):
    f.nordic("#006AA7", "#FECC00", x=105, t=40)


@flag("switzerland", w=200, h=200)
def _(f):
    f.r(0, 0, 200, 200, "#DA291C")
    f.r(80, 36, 40, 128, W_)
    f.r(36, 80, 128, 40, W_)


@flag("united-kingdom")
def _(f):
    f.uj()


@flag("vatican-city", w=200, h=200)
def _(f):
    f.vs(["#FFE000", W_])
    f.line("M120 150 L170 90 M170 150 L120 90", "#D4AF37", 8, "round")
    f.d("M132 52 C132 36 158 36 158 52 L162 78 H128 Z", "#D4AF37")


# ---------------------------------------------------------------- North America
@flag("antigua-and-barbuda")
def _(f):
    f.r(0, 0, 300, 200, "#CE1126")

    def band(y0, y1, c):
        f.p([(0.75 * y0, y0), (300 - 0.75 * y0, y0), (300 - 0.75 * y1, y1), (0.75 * y1, y1)], c)
    f.p([(0, 0), (300, 0), (150, 200)], W_)
    band(0, 130, "#0072C6")
    band(0, 90, K_)
    f.sun(150, 90, 26, "#FCD116", 16, 1.75, 0.12)
    band(90, 130, "#0072C6")


@flag("bahamas")
def _(f):
    f.hs(["#00778B", "#FFC72C", "#00778B"])
    f.hoist_tri(K_, 0.45)


@flag("barbados")
def _(f):
    f.vs(["#00267F", "#FFC726", "#00267F"])
    f.line("M150 140 V60 M120 66 V90 C120 104 180 104 180 90 V66", K_, 9)
    f.p([(150, 50), (142, 66), (158, 66)], K_)


@flag("belize")
def _(f):
    f.hs(["#CE1126", "#003F87", "#CE1126"], [1, 8, 1])
    f.c(150, 100, 62, W_)
    f.ring(150, 100, 52, "#2A7A2A", 10)
    f.d("M132 80 H168 V108 C168 120 158 126 150 128 C142 126 132 120 132 108 Z", "#C9A04A")


@flag("canada")
def _(f):
    f.vs(["#D80621", W_, "#D80621"], [1, 2, 1])
    f.d("M150 40 L160 60 L174 54 L168 88 L186 70 L190 80 L206 76 L200 96 L210 100 L180 124 L184 136 L154 132 V160 H146 V132 "
        "L116 136 L120 124 L90 100 L100 96 L94 76 L110 80 L114 70 L132 88 L126 54 L140 60 Z", "#D80621")


@flag("cuba")
def _(f):
    f.hs(["#002A8F", W_] * 2 + ["#002A8F"])
    f.hoist_tri("#CF142B", 0.45)
    f.star(46, 100, 26, W_)


@flag("dominica")
def _(f):
    f.r(0, 0, 300, 200, "#006B3F")
    for c, o in (("#FCD116", -14), (K_, 0), (W_, 14)):
        f.r(120 + o, 0, 14, 200, c)
        f.r(0, 86 + o, 300, 14, c)
    f.c(134, 100, 46, "#D41C30")
    f.stars_ring(134, 100, 36, 10, 6, "#006B3F")
    f.d("M126 86 C140 80 148 96 142 112 L134 118 L128 106 Z", "#9461C9")


@flag("dominican-republic")
def _(f):
    f.r(0, 0, 300, 200, W_)
    f.r(0, 0, 130, 80, "#002D62")
    f.r(170, 0, 130, 80, "#CE1126")
    f.r(0, 120, 130, 80, "#CE1126")
    f.r(170, 120, 130, 80, "#002D62")
    f.d("M138 84 H162 V108 C162 116 156 118 150 120 C144 118 138 116 138 108 Z", "#00843D")


@flag("el-salvador")
def _(f):
    f.hs(["#0F47AF", W_, "#0F47AF"])
    f.ring(150, 100, 28, "#1A7A3A", 6)
    f.p([(150, 80), (170, 112), (130, 112)], "#F7D116")


@flag("grenada")
def _(f):
    f.r(0, 0, 300, 200, "#CE1126")
    f.p([(30, 30), (270, 30), (150, 100)], "#FCD116")
    f.p([(30, 170), (270, 170), (150, 100)], "#FCD116")
    f.p([(30, 30), (30, 170), (150, 100)], "#007A5E")
    f.p([(270, 30), (270, 170), (150, 100)], "#007A5E")
    f.c(150, 100, 22, "#CE1126")
    f.star(150, 100, 16, "#FCD116")
    for x in (80, 150, 220):
        f.star(x, 15, 9, "#FCD116")
        f.star(x, 185, 9, "#FCD116")
    f.c(62, 100, 10, "#E26E2F")


@flag("guatemala")
def _(f):
    f.vs(["#4997D0", W_, "#4997D0"])
    f.ring(150, 100, 30, "#2A7A2A", 7)
    f.line("M128 120 L172 80 M172 120 L128 80", "#8A8A8A", 4)
    f.d("M140 96 C150 86 162 90 160 100 L150 108 Z", "#2A9A4A")


@flag("haiti")
def _(f):
    f.hs(["#00209F", "#D21034"])
    f.r(110, 70, 80, 60, W_)
    f.p([(140, 120), (150, 80), (160, 120)], "#016A16")
    f.r(124, 116, 52, 8, "#016A16")


@flag("honduras")
def _(f):
    f.hs(["#00BCE4", W_, "#00BCE4"])
    for x, y in ((150, 100), (118, 86), (118, 114), (182, 86), (182, 114)):
        f.star(x, y, 9, "#00BCE4")


@flag("jamaica")
def _(f):
    f.p([(0, 0), (300, 0), (150, 100)], "#009B3A")
    f.p([(0, 200), (300, 200), (150, 100)], "#009B3A")
    f.p([(0, 0), (0, 200), (150, 100)], K_)
    f.p([(300, 0), (300, 200), (150, 100)], K_)
    f.line("M0 0 L300 200 M300 0 L0 200", "#FED100", 30)


@flag("mexico")
def _(f):
    f.vs(["#006847", W_, "#CE1126"])
    f.d("M136 80 C146 70 160 72 166 82 L170 104 C164 112 150 114 140 110 Z", "#8C5A2B")
    f.line("M134 118 C144 126 156 126 166 118", "#2A7A2A", 6, "round")
    f.d("M146 106 V92 M154 106 V96", "#3A8A3A")


@flag("nicaragua")
def _(f):
    f.hs(["#0067C6", W_, "#0067C6"])
    f.s.raw('<polygon points="150,80 172,116 128,116" fill="none" stroke="#C8A600" stroke-width="5"/>')
    f.p([(150, 88), (164, 112), (136, 112)], "#4CB8E0")


@flag("panama")
def _(f):
    f.r(0, 0, 150, 100, W_)
    f.r(150, 0, 150, 100, "#DA121A")
    f.r(0, 100, 150, 100, "#072357")
    f.r(150, 100, 150, 100, W_)
    f.star(75, 50, 24, "#072357")
    f.star(225, 150, 24, "#DA121A")


@flag("saint-kitts-and-nevis")
def _(f):
    f.diag("#009E49", "#CE1126", K_, "#FCD116", 60, 12, up=True)
    f.star(110, 120, 16, W_, rot=-60)
    f.star(190, 80, 16, W_, rot=-60)


@flag("saint-lucia")
def _(f):
    f.r(0, 0, 300, 200, "#65CFFF")
    f.p([(150, 30), (200, 170), (100, 170)], W_)
    f.p([(150, 40), (194, 170), (106, 170)], K_)
    f.p([(150, 90), (200, 170), (100, 170)], "#FCD116")


@flag("saint-vincent-and-the-grenadines")
def _(f):
    f.vs(["#002674", "#FCD022", "#009E60"], [1, 2, 1])
    for x, y in ((120, 70), (180, 70), (150, 130)):
        f.p([(x, y - 22), (x + 16, y), (x, y + 22), (x - 16, y)], "#009E60")


@flag("trinidad-and-tobago")
def _(f):
    f.r(0, 0, 300, 200, "#DA1A35")
    f.line("M0 0 L300 200", W_, 70)
    f.line("M0 0 L300 200", K_, 50)


@flag("united-states")
def _(f):
    f.hs(["#B22234", W_] * 6 + ["#B22234"])
    f.r(0, 0, 120, 108, "#3C3B6E")
    for row in range(9):
        n = 6 if row % 2 == 0 else 5
        for i in range(n):
            x = 10 + i * 20 + (10 if row % 2 else 0)
            f.star(x, 8 + row * 11.5, 4.5, W_)


# ---------------------------------------------------------------- South America
@flag("argentina")
def _(f):
    f.hs(["#74ACDF", W_, "#74ACDF"])
    f.sun(150, 100, 14, "#F6B40E", 16, 1.9, 0.14)


@flag("brazil")
def _(f):
    f.r(0, 0, 300, 200, "#009C3B")
    f.p([(150, 20), (280, 100), (150, 180), (20, 100)], "#FFDF00")
    f.c(150, 100, 50, "#002776")
    f.s.raw('<path d="M102 90 C130 82 170 86 198 104" fill="none" stroke="#FFFFFF" stroke-width="10"/>')
    for x, y in ((130, 116), (150, 126), (170, 116), (160, 136), (140, 136)):
        f.c(x, y, 3, W_)


@flag("chile")
def _(f):
    f.hs([W_, "#D52B1E"])
    f.r(0, 0, 100, 100, "#0039A6")
    f.star(50, 50, 22, W_)


@flag("ecuador")
def _(f):
    f.hs(["#FFDD00", "#034EA2", "#ED1C24"], [2, 1, 1])
    f.s.raw('<ellipse cx="150" cy="100" rx="24" ry="32" fill="#57A0D3" stroke="#C8A600" stroke-width="4"/>')
    f.d("M126 64 C140 54 160 54 174 64 L150 72 Z", "#5A3A1A")


@flag("guyana")
def _(f):
    f.r(0, 0, 300, 200, "#009E49")
    f.p([(0, 0), (300, 100), (0, 200)], W_)
    f.p([(0, 8), (284, 100), (0, 192)], "#FCD116")
    f.p([(0, 0), (150, 100), (0, 200)], K_)
    f.p([(0, 10), (136, 100), (0, 190)], "#CE1126")


@flag("paraguay")
def _(f):
    f.hs(["#D52B1E", W_, "#0038A8"])
    f.ring(150, 100, 24, "#1A7A3A", 5)
    f.star(150, 100, 10, "#FCD116")


@flag("suriname")
def _(f):
    f.hs(["#377E3F", W_, "#B40A2D", W_, "#377E3F"], [2, 1, 4, 1, 2])
    f.star(150, 102, 36, "#ECC81D")


@flag("uruguay")
def _(f):
    f.hs([W_, "#0038A8"] * 4 + [W_])
    f.r(0, 0, 110, 111, W_)
    f.sun(55, 55, 16, "#FCD116", 16, 2.2, 0.12)


@flag("venezuela")
def _(f):
    f.hs(["#FFCC00", "#00247D", "#CF142B"])
    for i in range(8):
        a = math.radians(-160 + i * 20)
        f.star(150 + 44 * math.cos(a), 124 + 44 * math.sin(a), 7, W_)


# ---------------------------------------------------------------- Oceania
@flag("australia")
def _(f):
    f.r(0, 0, 300, 200, "#012169")
    f.uj(0, 0, 150, 100)
    f.star(75, 150, 22, W_, 7, 0.45)
    for x, y, r in ((225, 160, 12), (180, 90, 12), (225, 40, 12), (264, 80, 12), (245, 108, 6)):
        f.star(x, y, r, W_, 7 if r > 8 else 5, 0.45)


@flag("fiji")
def _(f):
    f.r(0, 0, 300, 200, "#68BFE5")
    f.uj(0, 0, 150, 100)
    f.d("M190 60 H250 V120 C250 144 230 156 220 160 C210 156 190 144 190 120 Z", W_)
    f.r(190, 60, 60, 20, "#CE1126")
    f.line("M220 80 V158 M190 116 H250", "#CE1126", 6)


@flag("kiribati")
def _(f):
    f.r(0, 0, 300, 120, "#CE1126")
    f.sun(150, 120, 34, "#FCD116", 17, 1.7, 0.1)
    f.d("M100 70 C130 50 150 64 150 70 C150 64 170 50 200 70 C170 74 160 80 150 84 C140 80 130 74 100 70 Z", "#FCD116")
    f.r(0, 120, 300, 80, "#003F87")
    for y in (130, 154, 178):
        f.line(f"M0 {y} q25 -10 50 0 t50 0 t50 0 t50 0 t50 0 t50 0", W_, 8)


@flag("marshall-islands")
def _(f):
    f.r(0, 0, 300, 200, "#003893")
    f.p([(0, 200), (300, 30), (300, 55)], "#DD7500")
    f.p([(0, 200), (300, 55), (300, 80)], W_)
    f.star(70, 60, 34, W_, 24, 0.5)


@flag("micronesia")
def _(f):
    f.r(0, 0, 300, 200, "#75B2DD")
    for x, y in ((150, 50), (100, 100), (200, 100), (150, 150)):
        f.star(x, y, 20, W_)


@flag("nauru")
def _(f):
    f.r(0, 0, 300, 200, "#002B7F")
    f.r(0, 94, 300, 12, "#FFC61E")
    f.star(80, 150, 24, W_, 12, 0.5)


@flag("new-zealand")
def _(f):
    f.r(0, 0, 300, 200, "#012169")
    f.uj(0, 0, 150, 100)
    for x, y, r in ((225, 160, 16), (190, 90, 14), (225, 40, 12), (260, 80, 14)):
        f.star(x, y, r + 4, W_)
        f.star(x, y, r, "#C8102E")


@flag("palau")
def _(f):
    f.r(0, 0, 300, 200, "#4AADD6")
    f.c(130, 100, 60, "#FFDE00")


@flag("papua-new-guinea")
def _(f):
    f.p([(0, 0), (300, 0), (300, 200)], "#CE1126")
    f.p([(0, 0), (0, 200), (300, 200)], K_)
    for x, y, r in ((70, 120, 12), (40, 150, 12), (100, 150, 12), (70, 180, 12), (80, 160, 6)):
        f.star(x, y, r, W_)
    f.d("M180 70 C200 40 240 40 250 60 L270 50 L256 74 C240 80 220 90 200 110 L190 96 Z", "#FCD116")


@flag("samoa")
def _(f):
    f.r(0, 0, 300, 200, "#CE1126")
    f.r(0, 0, 150, 100, "#002B7F")
    for x, y, r in ((75, 20, 10), (50, 50, 10), (100, 46, 10), (75, 80, 12), (88, 62, 5)):
        f.star(x, y, r, W_)


@flag("solomon-islands")
def _(f):
    f.p([(0, 0), (300, 0), (0, 200)], "#0051BA")
    f.p([(300, 0), (300, 200), (0, 200)], "#215B33")
    f.line("M0 200 L300 0", "#FCD116", 20)
    for x, y in ((30, 25), (90, 25), (60, 50), (30, 75), (90, 75)):
        f.star(x, y, 10, W_)


@flag("tonga")
def _(f):
    f.r(0, 0, 300, 200, "#C10000")
    f.r(0, 0, 130, 100, W_)
    f.r(52, 16, 26, 68, "#C10000")
    f.r(31, 37, 68, 26, "#C10000")


@flag("tuvalu")
def _(f):
    f.r(0, 0, 300, 200, "#5B97B1")
    f.uj(0, 0, 150, 100)
    for x, y in ((190, 40), (230, 30), (270, 60), (210, 90), (250, 100), (190, 140), (230, 150), (270, 130), (200, 180)):
        f.star(x, y, 9, "#FFCE00")


@flag("vanuatu")
def _(f):
    f.hs(["#D21034", "#009543"])
    f.line("M0 0 L130 100 H300 M0 200 L130 100", K_, 40)
    f.line("M0 0 L130 100 H300 M0 200 L130 100", "#FDCE12", 20)
    f.line("M0 0 L130 100 H300 M0 200 L130 100", K_, 10)
    f.p([(0, 20), (104, 100), (0, 180)], K_)
    f.ring(40, 100, 20, "#FDCE12", 6)


# ---------------------------------------------------------------- other flags
@flag("united-nations")
def _(f):
    f.r(0, 0, 300, 200, "#5B92E5")
    f.ring(150, 100, 44, W_, 4)
    f.ring(150, 100, 28, W_, 3)
    f.line("M150 56 V144 M106 100 H194", W_, 3)
    for side in (-1, 1):
        f.s.raw(f'<path d="M{150 + side * 58} 60 C{150 + side * 76} 90 {150 + side * 70} 130 150 160" fill="none" stroke="#FFFFFF" stroke-width="7"/>')


@flag("european-union")
def _(f):
    f.r(0, 0, 300, 200, "#003399")
    f.stars_ring(150, 100, 66, 12, 11, "#FFCC00")


@flag("arab-league")
def _(f):
    f.r(0, 0, 300, 200, "#006C35")
    f.ring(150, 100, 52, W_, 5)
    f.cres(150, 100, 36, W_, "#006C35", 0, -0.3, 0.85)
    f.line("M108 130 C130 146 170 146 192 130", W_, 5)


@flag("african-union")
def _(f):
    f.r(0, 0, 300, 200, "#009A44")
    f.stars_ring(150, 100, 76, 24, 5, "#FFD100")
    f.c(150, 100, 58, W_)
    f.d("M128 64 C150 56 176 64 180 86 C186 104 170 116 164 132 C158 146 150 148 146 136 C140 120 134 112 126 102 C116 92 112 76 128 64 Z", "#009A44")


def pole_flag(draw):
    def fn(s):
        s.T("M120 470 V60", "#8A5A33", 18)
        s.F("circle", cx=120, cy=56, r=16, fill="#E8A520")
        draw(s)
    return fn


def _white(s):
    s.F("path", d="M130 80 C200 60 260 110 330 90 C380 76 410 80 430 90 V250 C400 240 370 240 330 254 C260 274 200 224 130 244 Z", fill="#FFFFFF")


def _chequer(s):
    cid = "chk-flag-chequered"
    shape = "M130 80 C200 60 260 110 330 90 C380 76 410 80 430 90 V250 C400 240 370 240 330 254 C260 274 200 224 130 244 Z"
    s.raw(f'<defs><clipPath id="{cid}"><path d="{shape}"/></clipPath></defs>')
    s.F("path", d=shape, fill="#FFFFFF")
    s.raw(f'<g clip-path="url(#{cid})">')
    for i in range(8):
        for j in range(6):
            if (i + j) % 2 == 0:
                x, y = 130 + i * 38, 60 + j * 36 + (8 * math.sin(i * 0.9))
                s.F("rect", outline=False, x=f"{x:.0f}", y=f"{y:.0f}", width=38, height=36, fill="#1F1F24")
    s.raw("</g>")
    s.F("path", d=shape, fill="none")


D["flag-white"] = pole_flag(_white)
D["flag-chequered"] = pole_flag(_chequer)


@flag("pirate")
def _(f):
    f.r(0, 0, 300, 200, "#1F1F24")
    f.line("M100 140 L200 180 M200 140 L100 180", W_, 14, "round")
    f.c(150, 84, 40, W_)
    f.r(130, 110, 40, 24, W_)
    f.c(136, 84, 10, "#1F1F24")
    f.c(164, 84, 10, "#1F1F24")
    f.p([(150, 96), (144, 108), (156, 108)], "#1F1F24")



# ---------------------------------------------------------------- flags with Arabic script
def ar(f, text, cx, cy, w, h, color):
    d, _ = text_path(text, "arabic", cx, cy, w, h)
    f.s.F("path", outline=False, d=d, fill=color)


@flag("saudi-arabia")
def _(f):
    f.r(0, 0, 300, 200, "#006C35")
    ar(f, "لا إله إلا الله محمد رسول الله", 150, 82, 220, 64, W_)
    f.d("M70 136 H222 L232 130 V146 L222 140 H70 L60 138 Z", W_)
    f.r(228, 124, 6, 28, W_)


@flag("iraq")
def _(f):
    f.hs(["#CE1126", W_, K_])
    ar(f, "الله أكبر", 150, 100, 150, 52, "#007A3D")


@flag("iran")
def _(f):
    f.hs(["#239F40", W_, "#DA0000"])
    for y in (62, 138):
        for i in range(11):
            ar(f, "الله اكبر", 14 + i * 27.2, y, 24, 8, W_)
    f.line("M150 76 V124", "#DA0000", 5)
    for sgn in (-1, 1):
        f.s.raw(f'<path d="M{150 + sgn * 8} 78 C{150 + sgn * 34} 86 {150 + sgn * 34} 118 {150 + sgn * 6} 124" fill="none" stroke="#DA0000" stroke-width="5"/>')
        f.s.raw(f'<path d="M{150 + sgn * 14} 72 C{150 + sgn * 48} 84 {150 + sgn * 46} 120 {150 + sgn * 12} 128" fill="none" stroke="#DA0000" stroke-width="4"/>')


@flag("afghanistan")
def _(f):
    f.vs([K_, "#D32011", "#007A36"])
    f.ring(150, 104, 52, W_, 5)
    for sgn in (-1, 1):
        for i in range(5):
            a = math.radians(110 + i * 22) if sgn < 0 else math.radians(70 - i * 22)
            f.s.raw(f'<ellipse cx="{150 + 58 * math.cos(a):.1f}" cy="{104 + 58 * math.sin(a):.1f}" rx="7" ry="3.5" fill="#FFFFFF" '
                    f'transform="rotate({math.degrees(a) + 90:.0f} {150 + 58 * math.cos(a):.1f} {104 + 58 * math.sin(a):.1f})"/>')
    ar(f, "لا إله إلا الله محمد رسول الله", 150, 76, 70, 14, W_)
    f.r(126, 100, 48, 30, W_)
    f.p([(120, 100), (150, 86), (180, 100)], W_)
    f.d("M144 130 V114 A6 6 0 0 1 156 114 V130 Z", "#D32011")
    f.r(118, 136, 64, 6, W_)


if __name__ == "__main__":
    run("earth-geography", D, sys.argv[1:] or None)
