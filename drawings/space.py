"""space drawings. Run: python drawings/space.py [ids...]"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, eye, shade, tint  # noqa: E402
from _parts import rocket as rocket_part  # noqa: E402
from draw_lib import C, INK, THEME, arc_pt, head, run, star_pts  # noqa: E402

D = {}
NIGHT, NIGHT2 = "#14203A", "#1E2A4A"
SUN, SUN2 = "#FFC83D", "#F5913E"
SUIT, VISOR = "#F4F1EA", "#2C4A7A"


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def sky(s, color=NIGHT, stars=14, seed=2):
    s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill=color)
    rnd = random.Random(seed)
    for _ in range(stars):
        x, y = rnd.uniform(50, 462), rnd.uniform(50, 462)
        s.F("polygon", outline=False, points=star_pts(x, y, rnd.uniform(5, 10), 3, 4), fill="#FFF1C2")


def planet(s, cx=256, cy=256, r=170, base="#C9CED6", bands=None, spots=None, craters=None, hi=True):
    s.F("circle", cx=cx, cy=cy, r=r, fill=base)
    if bands:
        for k, (dy, h, col) in enumerate(bands):
            y = cy + dy * r
            half = math.sqrt(max(0.0, r * r - (dy * r) ** 2)) * 0.97
            s.F("rect", outline=False, x=f"{cx - half:.0f}", y=f"{y - h * r / 2:.0f}", width=f"{2 * half:.0f}", height=f"{h * r:.0f}", rx=f"{h * r / 2:.0f}", fill=col)
    if spots:
        for dx, dy, rr, col in spots:
            s.F("ellipse", outline=False, cx=f"{cx + dx * r:.0f}", cy=f"{cy + dy * r:.0f}", rx=f"{rr * r:.0f}", ry=f"{rr * r * 0.6:.0f}", fill=col)
    if craters:
        for dx, dy, rr in craters:
            s.F("circle", outline=False, cx=f"{cx + dx * r:.0f}", cy=f"{cy + dy * r:.0f}", r=f"{rr * r:.0f}", fill=shade(base, 0.82))
    if hi:
        s.F("path", outline=False, d=f"M{cx - r * 0.75:.0f} {cy - r * 0.1:.0f} A{r * 0.8:.0f} {r * 0.8:.0f} 0 0 1 {cx - r * 0.1:.0f} {cy - r * 0.75:.0f}", fill="none")
    s.F("circle", cx=cx, cy=cy, r=r, fill="none")


def rings(s, cx=256, cy=256, rx=250, ry=60, color="#E8D8A8", front=True):
    if front:
        s.F("path", d=f"M{cx - rx} {cy} A{rx} {ry} 0 0 0 {cx + rx} {cy} L{cx + rx * 0.78} {cy} A{rx * 0.78} {ry * 0.7} 0 0 1 {cx - rx * 0.78} {cy}Z", fill=color)
    else:
        s.F("path", d=f"M{cx - rx} {cy} A{rx} {ry} 0 0 1 {cx + rx} {cy} L{cx + rx * 0.78} {cy} A{rx * 0.78} {ry * 0.7} 0 0 0 {cx - rx * 0.78} {cy}Z", fill=shade(color, 0.85))


def moon_disc(s, cx=256, cy=256, r=170, phase=0.5, lit="#F4F1EA", dark="#4A5570", craters=True):
    """phase: 0 new, 0.25 first quarter, 0.5 full, 0.75 last quarter (northern view, lit from right while waxing)."""
    s.F("circle", cx=cx, cy=cy, r=r, fill=dark)
    k = math.cos(phase * 2 * math.pi)          # 1 new .. -1 full
    if abs(k) < 0.999 or phase in (0.5,):
        waxing = phase < 0.5
        side = 1 if waxing else 0             # which half is lit
        ex = abs(k) * r
        sweep_outer = 1 if waxing else 0
        # lit = half disc on lit side + ellipse bulge (gibbous) or minus (crescent)
        gibbous = k < 0
        sweep_inner = (1 if gibbous else 0) if waxing else (0 if gibbous else 1)
        d = (f"M{cx} {cy - r} A{r} {r} 0 0 {sweep_outer} {cx} {cy + r} "
             f"A{ex:.1f} {r} 0 0 {sweep_inner} {cx} {cy - r}Z")
        if phase == 0.5:
            d = f"M{cx - r} {cy} A{r} {r} 0 1 0 {cx + r} {cy} A{r} {r} 0 1 0 {cx - r} {cy}Z"
        s.F("path", outline=False, d=d, fill=lit)
    if craters:
        for dx, dy, rr in ((-0.3, -0.25, 0.14), (0.25, 0.1, 0.1), (-0.1, 0.35, 0.12), (0.4, -0.35, 0.07)):
            s.F("circle", outline=False, cx=f"{cx + dx * r:.0f}", cy=f"{cy + dy * r:.0f}", r=f"{rr * r:.0f}", fill="#000000", fill_opacity="0.12")
    s.F("circle", cx=cx, cy=cy, r=r, fill="none")


def star_burst(s, cx=256, cy=256, r=150, color=SUN, n=16, glow=None):
    if glow:
        s.F("circle", outline=False, cx=cx, cy=cy, r=r * 1.25, fill=glow, fill_opacity="0.35")
    s.F("polygon", points=star_pts(cx, cy, r, r * 0.55, n), fill=color)
    s.F("circle", outline=False, cx=cx, cy=cy, r=r * 0.45, fill=tint(color, 0.5))


def sun(s, cx=256, cy=256, r=120):
    s.open("part-glow", f"{cx} {cy}")
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(cx, cy, r * 1.2, a); x2, y2 = arc_pt(cx, cy, r * 1.65, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", SUN2, r * 0.18)
    s.close()
    s.F("circle", cx=cx, cy=cy, r=r, fill=SUN)
    s.F("circle", outline=False, cx=cx - r * 0.3, cy=cy - r * 0.3, r=r * 0.25, fill="#FFE38A")


def earth(s, cx=256, cy=256, r=200):
    s.open(transform=f"translate({cx} {cy}) scale({r / 205:.3f}) translate(-256 -256)")
    s.open("part-globe", "256 256")
    s.F("circle", cx=256, cy=256, r=205, fill=C["blue"])
    for d in ("M150 120 C190 96 236 104 246 140 C254 172 220 182 214 214 C208 250 172 256 150 232 C126 206 102 160 150 120Z",
              "M210 268 C246 256 276 282 270 322 C264 362 246 396 226 420 C206 400 200 360 192 332 C184 300 186 276 210 268Z",
              "M300 120 C346 112 396 140 410 186 C420 224 396 236 372 226 C352 218 344 244 324 252 C298 262 284 236 290 210 C296 180 270 140 300 120Z",
              "M350 310 C380 300 410 318 404 348 C398 372 366 380 350 362 C336 346 336 318 350 310Z"):
        s.F("path", d=d, fill=C["green"])
    s.F("path", outline=False, d="M110 300 C130 290 156 300 150 318 C140 336 112 330 110 300Z", fill=WHITE, fill_opacity="0.85")
    s.close()
    s.close()


# ---------------------------------------------------------------- sun and stars
D["sun"] = lambda s: sun(s)
D["star"] = lambda s: (sky(s, stars=10), star_burst(s, r=140, n=8, glow="#FFE38A"))
D["shining-star"] = lambda s: (sky(s, stars=8), star_burst(s, r=150, n=4, glow="#FFF1C2"), [s.F("polygon", outline=False, points=star_pts(x, y, 20, 6, 4), fill="#FFF1C2") for x, y in ((120, 120), (400, 380))])
D["red-giant"] = lambda s: (sky(s, stars=8), s.F("circle", outline=False, cx=256, cy=256, r=210, fill="#E8583B", fill_opacity="0.35"), s.F("circle", cx=256, cy=256, r=180, fill="#E8583B"))
D["red-dwarf"] = lambda s: (sky(s, stars=12), s.F("circle", outline=False, cx=256, cy=256, r=90, fill="#E8583B", fill_opacity="0.35"), s.F("circle", cx=256, cy=256, r=70, fill="#C1442E"))
D["white-dwarf"] = lambda s: (sky(s, stars=12), s.F("circle", outline=False, cx=256, cy=256, r=90, fill="#E8F0FF", fill_opacity="0.4"), s.F("circle", cx=256, cy=256, r=60, fill=WHITE))
D["blue-giant"] = lambda s: (sky(s, stars=8), s.F("circle", outline=False, cx=256, cy=256, r=200, fill="#5EA8FF", fill_opacity="0.35"), s.F("circle", cx=256, cy=256, r=160, fill="#5EA8FF"))
D["neutron-star"] = lambda s: (sky(s, stars=10), s.F("circle", outline=False, cx=256, cy=256, r=110, fill="#B8F0FF", fill_opacity="0.4"), s.F("circle", cx=256, cy=256, r=50, fill="#E8F8FF"))
D["pulsar"] = lambda s: (sky(s, stars=10), s.F("polygon", outline=False, points="256,256 200,30 312,30", fill="#B8F0FF", fill_opacity="0.6"),
                         s.F("polygon", outline=False, points="256,256 200,482 312,482", fill="#B8F0FF", fill_opacity="0.6"), s.F("circle", cx=256, cy=256, r=50, fill="#E8F8FF"))
D["supernova"] = lambda s: (sky(s, stars=6), star_burst(s, r=200, color="#F5913E", n=20, glow="#FFE38A"), s.F("circle", cx=256, cy=256, r=60, fill=WHITE))
D["binary-star"] = lambda s: (sky(s, stars=10), s.M("M100 256 A156 60 0 1 1 412 256 A156 60 0 1 1 100 256", "#5A6A8A", 4, dash="12 10"),
                              star_burst(s, 170, 256, 70, SUN, 10), star_burst(s, 350, 256, 50, "#8FD0FF", 10))
D["north-star"] = lambda s: (sky(s, stars=10), star_burst(s, 256, 200, 90, "#FFF1C2", 8, glow="#FFF1C2"), s.M("M256 330 V420 M226 390 L256 420 L286 390", "#8FD0FF", 10))
D["sirius"] = lambda s: (sky(s, stars=10), star_burst(s, r=110, color="#E8F8FF", n=8, glow="#8FD0FF"))
D["betelgeuse"] = lambda s: (sky(s, stars=10), s.F("circle", outline=False, cx=256, cy=256, r=170, fill="#F5913E", fill_opacity="0.35"), s.F("circle", cx=256, cy=256, r=140, fill="#E8782B"))
D["sunspot"] = lambda s: (sun(s, r=150), [s.F("circle", outline=False, cx=x, cy=y, r=r, fill="#C1662E") for x, y, r in ((220, 230, 20), (300, 280, 14), (250, 310, 10))])
D["solar-flare"] = lambda s: (sky(s, stars=6), s.F("circle", cx=200, cy=330, r=200, fill=SUN), s.T("M260 140 C300 40 420 60 400 160", "#F5913E", 36))
D["solar-wind"] = lambda s: (sky(s, stars=6), s.F("circle", cx=100, cy=256, r=110, fill=SUN), [s.M(f"M230 {y} C300 {y - 20} 380 {y + 20} 470 {y}", "#FFE38A", 8) for y in (170, 220, 270, 320)])

# ---------------------------------------------------------------- planets
D["mercury-planet"] = lambda s: planet(s, base="#9A9490", craters=((-0.3, -0.2, 0.15), (0.3, 0.2, 0.12), (0.0, 0.4, 0.1), (0.35, -0.4, 0.08)))
D["venus-planet"] = lambda s: planet(s, base="#E8C27A", bands=((-0.4, 0.18, "#F2D59A"), (0.1, 0.2, "#D9A85A"), (0.5, 0.15, "#F2D59A")))
D["earth"] = lambda s: earth(s)
D["mars"] = lambda s: planet(s, base="#C9562E", spots=((-0.3, -0.2, 0.25, "#A8401E"), (0.3, 0.3, 0.2, "#A8401E")), craters=((0.1, -0.4, 0.08),))
D["jupiter"] = lambda s: planet(s, base="#E8C9A0", bands=((-0.55, 0.14, "#C98A5A"), (-0.25, 0.18, "#D9A878"), (0.1, 0.16, "#C98A5A"), (0.45, 0.14, "#D9A878")), spots=((0.3, 0.18, 0.16, "#C1562E"),))
D["saturn"] = lambda s: (rings(s, front=False), planet(s, r=130, base="#E8D29A", bands=((-0.3, 0.2, "#D9B878"), (0.2, 0.2, "#D9B878"))), rings(s, front=True))
D["uranus"] = lambda s: (s.F("ellipse", cx=256, cy=256, rx=60, ry=230, fill="none"), s.raw('<ellipse cx="256" cy="256" rx="60" ry="230" fill="none" stroke="#B8E8F0" stroke-width="10"/>'), planet(s, r=150, base="#8FD8E8"))
D["neptune"] = lambda s: planet(s, base="#3A6AD9", bands=((-0.3, 0.16, "#5A88E8"), (0.3, 0.14, "#2C55B8")), spots=((0.2, -0.1, 0.14, "#1E3A8A"),))


@reg("solar-system")
def _(s):
    sky(s, stars=10)
    s.F("circle", cx=24, cy=256, r=110, fill=SUN)
    for x, r, c in ((160, 10, "#9A9490"), (195, 16, "#E8C27A"), (235, 18, C["blue"]), (270, 13, "#C9562E"), (320, 40, "#E8C9A0"), (395, 32, "#E8D29A"), (445, 22, "#8FD8E8"), (476, 20, "#3A6AD9")):
        s.F("circle", cx=x, cy=256, r=r, fill=c)
    s.raw('<ellipse cx="395" cy="256" rx="54" ry="12" fill="none" stroke="#C9B87A" stroke-width="6"/>')


D["planet-orbits"] = lambda s: (sky(s, stars=8), [s.raw(f'<circle cx="256" cy="256" r="{r}" fill="none" stroke="#5A6A8A" stroke-width="4"/>') for r in (70, 120, 170, 210)],
                                s.F("circle", cx=256, cy=256, r=34, fill=SUN), [s.F("circle", cx=f"{arc_pt(256, 256, r, a)[0]:.0f}", cy=f"{arc_pt(256, 256, r, a)[1]:.0f}", r=pr, fill=c)
                                                                                for r, a, pr, c in ((70, 30, 10, "#9A9490"), (120, 200, 14, C["blue"]), (170, 120, 22, "#E8C9A0"), (210, 300, 16, "#3A6AD9"))])
D["exoplanet"] = lambda s: (sky(s, stars=12), star_burst(s, 120, 140, 60, "#FF8A5A", 10), planet(s, 300, 320, 120, "#5EB8A8", bands=((-0.2, 0.2, "#8AD8C8"), (0.3, 0.18, "#3A8A7A"))))

# ---------------------------------------------------------------- dwarf planets
D["pluto"] = lambda s: planet(s, base="#C9A88A", spots=((0.15, 0.2, 0.35, "#F2E3D0"), (-0.4, -0.2, 0.2, "#8C6A50")))
D["ceres"] = lambda s: planet(s, base="#8C8A8A", craters=((-0.2, -0.2, 0.12), (0.3, 0.2, 0.1)), spots=((0.1, -0.05, 0.06, WHITE),))
D["eris"] = lambda s: planet(s, base="#E5E7EB", craters=((-0.2, 0.2, 0.1), (0.3, -0.3, 0.08)))
D["haumea"] = lambda s: (s.F("ellipse", cx=256, cy=256, rx=200, ry=110, fill="#D9DEE5"), s.F("ellipse", outline=False, cx=320, cy=230, rx=40, ry=24, fill="#C1662E"))
D["makemake"] = lambda s: planet(s, base="#C98A6A", spots=((-0.2, 0.1, 0.3, "#E8B89A"),))

# ---------------------------------------------------------------- moons and phases
D["moon"] = lambda s: moon_disc(s, phase=0.5, dark="#F4F1EA")
D["full-moon"] = lambda s: (sky(s, stars=10), moon_disc(s, r=160, phase=0.5, dark="#F4F1EA"))
D["new-moon"] = lambda s: (sky(s, stars=10), moon_disc(s, r=160, phase=0.0, craters=False))
D["crescent-moon"] = lambda s: (sky(s, stars=10), moon_disc(s, r=160, phase=0.12, dark=NIGHT2))
for _id, _ph in (("waxing-crescent", 0.12), ("first-quarter-moon", 0.25), ("waxing-gibbous", 0.37), ("waning-gibbous", 0.63), ("last-quarter-moon", 0.75), ("waning-crescent", 0.88)):
    D[_id] = (lambda ph: lambda s: (sky(s, stars=10), moon_disc(s, r=160, phase=ph, dark=NIGHT2)))(_ph)


@reg("moon-phases")
def _(s):
    sky(s, stars=0)
    for i, ph in enumerate((0.0, 0.12, 0.25, 0.37, 0.5, 0.63, 0.75, 0.88)):
        x, y = arc_pt(256, 256, 165, -90 + i * 45)
        moon_disc(s, x, y, 42, ph, dark="#3A4A6A", craters=False)
    sun(s, 256, 256, 34)


D["blood-moon"] = lambda s: (sky(s, stars=10), moon_disc(s, r=160, phase=0.5, dark="#C1442E", lit="#C1442E"))
D["supermoon"] = lambda s: (sky(s, stars=6), moon_disc(s, r=210, phase=0.5, dark="#FFF1C2", lit="#FFF1C2"))
D["blue-moon"] = lambda s: (sky(s, stars=10), moon_disc(s, r=160, phase=0.5, dark="#B8D8F8", lit="#B8D8F8"))
D["moon-craters"] = lambda s: (moon_disc(s, r=200, phase=0.5, dark="#D9DEE5", lit="#D9DEE5"), [s.F("circle", cx=x, cy=y, r=r, fill="#B7BEC8") for x, y, r in ((190, 200, 40), (320, 300, 32), (260, 360, 24), (330, 170, 20))])
D["io"] = lambda s: planet(s, base="#E8D06E", spots=((-0.3, -0.2, 0.12, "#C1662E"), (0.2, 0.2, 0.1, "#8C3A1E"), (0.3, -0.35, 0.08, WHITE)))
D["europa"] = lambda s: (planet(s, base="#F2E8D8"), s.M("M120 200 C200 260 300 180 400 260 M140 330 C220 290 320 360 390 320", "#C98A5A", 6))
D["ganymede"] = lambda s: planet(s, base="#9A8A7A", spots=((-0.2, -0.1, 0.35, "#C9B89A"), (0.3, 0.3, 0.2, "#6E5E4E")))
D["callisto"] = lambda s: planet(s, base="#6E6258", craters=((-0.3, -0.3, 0.06), (0.2, 0.1, 0.05), (0.0, 0.4, 0.05), (0.4, -0.1, 0.05)), spots=((0.1, -0.2, 0.08, WHITE),))
D["titan"] = lambda s: (s.F("circle", outline=False, cx=256, cy=256, r=185, fill="#F2B95A", fill_opacity="0.4"), planet(s, base="#E8A54A"))
D["enceladus"] = lambda s: (planet(s, base="#F4F8FC"), s.M("M200 380 C220 340 240 360 256 320 M280 400 C290 360 310 370 320 330", "#8FD0FF", 6))
D["triton"] = lambda s: planet(s, base="#E8D8D0", spots=((0.1, 0.25, 0.35, "#F4C9B8"),))
D["phobos"] = lambda s: (s.F("ellipse", cx=256, cy=256, rx=190, ry=140, fill="#8C7A6A", transform="rotate(-15 256 256)"), s.F("circle", outline=False, cx=200, cy=230, r=40, fill="#6E5E4E"))
D["deimos"] = lambda s: (s.F("ellipse", cx=256, cy=256, rx=150, ry=120, fill="#A08E7E", transform="rotate(20 256 256)"), s.F("circle", outline=False, cx=300, cy=270, r=20, fill="#8C7A6A"))
D["charon"] = lambda s: planet(s, base="#A8A49E", spots=((0.0, -0.6, 0.35, "#8C4A3A"),))

# ---------------------------------------------------------------- galaxies and deep space
def galaxy(s, arms=2, color="#B8A8F0", core="#FFF1C2", ell=1.0, rot=0):
    s.open(transform=f"rotate({rot} 256 256) translate(256 256) scale(1 {ell}) translate(-256 -256)")
    for k in range(arms):
        s.M("M256 256 " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in (arc_pt(256, 256, 8 + t * 1.6, t * 3 + k * 360 / arms) for t in range(1, 120))), color, 26)
    s.F("circle", outline=False, cx=256, cy=256, r=60, fill=core)
    s.close()


D["milky-way"] = lambda s: (sky(s, stars=20), galaxy(s, 2, "#B8A8F0", ell=0.55, rot=-20))
D["spiral-galaxy"] = lambda s: (sky(s, stars=12), galaxy(s, 2, "#8FB8F8"))
D["elliptical-galaxy"] = lambda s: (sky(s, stars=12), s.F("ellipse", outline=False, cx=256, cy=256, rx=190, ry=110, fill="#F2D9A8", fill_opacity="0.5"), s.F("ellipse", cx=256, cy=256, rx=120, ry=70, fill="#F9E8C0"))
D["andromeda-galaxy"] = lambda s: (sky(s, stars=14), galaxy(s, 2, "#C8B8F8", ell=0.4, rot=35))
D["nebula"] = lambda s: (sky(s, stars=10), [s.F("ellipse", outline=False, cx=x, cy=y, rx=rx, ry=ry, fill=c, fill_opacity="0.7", transform=f"rotate({r} {x} {y})") for x, y, rx, ry, r, c in
                                             ((220, 220, 160, 90, -20, "#B880E8"), (300, 300, 140, 80, 20, "#F48AA6"), (260, 260, 80, 50, 0, "#8FD0FF"))])
D["star-cluster"] = lambda s: (sky(s, stars=4), [s.F("polygon", outline=False, points=star_pts(256 + dx, 256 + dy, r, r * 0.4, 4), fill="#FFF1C2") for dx, dy, r in
                                                 ((0, 0, 30), (-60, -40, 20), (50, -60, 18), (70, 40, 22), (-40, 70, 16), (-90, 20, 14), (20, 100, 14), (100, -10, 12))])
D["black-hole"] = lambda s: (sky(s, stars=10), s.raw('<ellipse cx="256" cy="256" rx="220" ry="60" fill="none" stroke="#F5913E" stroke-width="30"/>'), s.F("circle", cx=256, cy=256, r=110, fill="#05070D"),
                             s.raw('<path d="M36 256 A220 60 0 0 0 476 256" fill="none" stroke="#FFC83D" stroke-width="18"/>'))
D["wormhole"] = lambda s: (sky(s, stars=10), [s.raw(f'<ellipse cx="256" cy="{256 + k * 8}" rx="{200 - k * 30}" ry="{70 - k * 9}" fill="none" stroke="#8FB8F8" stroke-width="6"/>') for k in range(6)],
                           s.F("ellipse", cx=256, cy=300, rx=20, ry=8, fill="#05070D"))
D["quasar"] = lambda s: (sky(s, stars=8), s.F("polygon", outline=False, points="256,256 226,24 286,24", fill="#B8F0FF"), s.F("polygon", outline=False, points="256,256 226,488 286,488", fill="#B8F0FF"),
                         s.raw('<ellipse cx="256" cy="256" rx="140" ry="40" fill="none" stroke="#F5913E" stroke-width="18"/>'), s.F("circle", cx=256, cy=256, r=40, fill=WHITE))
D["big-bang"] = lambda s: (sky(s, stars=0, color="#05070D"), star_burst(s, r=210, color="#F5913E", n=24, glow="#FFE38A"), s.F("circle", cx=256, cy=256, r=60, fill=WHITE),
                           [s.F("circle", outline=False, cx=f"{arc_pt(256, 256, r, a)[0]:.0f}", cy=f"{arc_pt(256, 256, r, a)[1]:.0f}", r=6, fill="#FFF1C2") for r in (230,) for a in range(0, 360, 30)])
D["expanding-universe"] = lambda s: (sky(s, stars=0), [(s.raw(f'<circle cx="256" cy="256" r="{r}" fill="none" stroke="#5A6A8A" stroke-width="4" stroke-dasharray="10 10"/>')) for r in (80, 150, 210)],
                                     [s.M(f"M{arc_pt(256, 256, 60, a)[0]:.0f} {arc_pt(256, 256, 60, a)[1]:.0f} L{arc_pt(256, 256, 200, a)[0]:.0f} {arc_pt(256, 256, 200, a)[1]:.0f} "
                                          + head(*arc_pt(256, 256, 200, a), a, 24), "#FFC83D", 8) for a in range(0, 360, 45)])
D["dark-matter"] = lambda s: (sky(s, stars=14), [s.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#8B5CF6" fill-opacity="0.25"/>') for x, y, r in ((200, 220, 120), (320, 300, 140), (260, 160, 80))])
D["cosmic-web"] = lambda s: (sky(s, stars=0, color="#05070D"), s.M("M60 120 L200 200 L330 120 L450 220 M200 200 L250 340 L120 420 M250 340 L400 380 L450 220 M330 120 L250 340", "#B880E8", 6),
                             [s.F("circle", outline=False, cx=x, cy=y, r=14, fill="#F48AA6") for x, y in ((60, 120), (200, 200), (330, 120), (450, 220), (250, 340), (120, 420), (400, 380))])

# ---------------------------------------------------------------- small bodies
def rock(s, cx, cy, r, color="#8C7A6A", seed=1):
    rnd = random.Random(seed)
    pts = [arc_pt(cx, cy, r * rnd.uniform(0.8, 1.05), a) for a in range(0, 360, 30)]
    s.F("polygon", points=" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill=color)
    for k in range(3):
        s.F("circle", outline=False, cx=f"{cx + rnd.uniform(-0.4, 0.4) * r:.0f}", cy=f"{cy + rnd.uniform(-0.4, 0.4) * r:.0f}", r=f"{r * rnd.uniform(0.08, 0.16):.0f}", fill=shade(color, 0.8))


def comet(s, head_xy=(360, 160), color="#B8F0FF"):
    x, y = head_xy
    s.F("path", outline=False, d=f"M{x} {y - 30} L60 420 L{x - 30} {y + 20}Z", fill=color, fill_opacity="0.5")
    s.F("path", outline=False, d=f"M{x + 10} {y - 10} L120 460 L{x - 10} {y + 10}Z", fill=WHITE, fill_opacity="0.5")
    s.F("circle", cx=x, cy=y, r=36, fill=WHITE)


D["asteroid"] = lambda s: (sky(s, stars=10), rock(s, 256, 256, 160))
D["asteroid-belt"] = lambda s: (sky(s, stars=6), s.F("circle", cx=256, cy=256, r=40, fill=SUN), [rock(s, *arc_pt(256, 256, 170 + (k % 3) * 18, k * 24), 12 + k % 3 * 4, seed=k) for k in range(15)])
D["comet"] = lambda s: (sky(s, stars=10), comet(s))
D["halleys-comet"] = lambda s: (sky(s, stars=10), comet(s, (380, 140), "#FFF1C2"))
D["meteor"] = lambda s: (sky(s, stars=10), s.F("path", outline=False, d="M360 150 L80 400 L340 170Z", fill="#F5913E", fill_opacity="0.7"), rock(s, 370, 140, 40, "#C1662E"))
D["meteor-shower"] = lambda s: (sky(s, stars=8), [s.M(f"M{x} {y} l-90 90", "#FFF1C2", 6) for x, y in ((420, 90), (330, 160), (460, 240), (260, 80), (380, 300))])
D["meteorite"] = lambda s: rock(s, 256, 256, 190, "#5E5C5C", seed=5)
D["meteor-crater"] = lambda s: (s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill="#D9B88A"), s.F("ellipse", cx=256, cy=300, rx=200, ry=110, fill="#B8936A"), s.F("ellipse", outline=False, cx=256, cy=310, rx=150, ry=70, fill="#8C6A4A"))
D["kuiper-belt"] = lambda s: (sky(s, stars=4), s.F("circle", cx=256, cy=256, r=24, fill=SUN), [s.F("circle", outline=False, cx=f"{arc_pt(256, 256, 190 + (k % 4) * 12, k * 11)[0]:.0f}", cy=f"{arc_pt(256, 256, 190 + (k % 4) * 12, k * 11)[1]:.0f}", r=5, fill="#B8D8F8") for k in range(33)])
D["oort-cloud"] = lambda s: (sky(s, stars=0), s.F("circle", cx=256, cy=256, r=14, fill=SUN), [s.F("circle", outline=False, cx=f"{256 + math.cos(k * 1.7) * (120 + (k * 37) % 100):.0f}", cy=f"{256 + math.sin(k * 1.3) * (120 + (k * 53) % 100):.0f}", r=4, fill="#B8D8F8") for k in range(70)])

# ---------------------------------------------------------------- sky events
D["solar-eclipse"] = lambda s: (sky(s, stars=10), s.F("circle", outline=False, cx=256, cy=256, r=180, fill="#FFE38A", fill_opacity="0.5"), s.F("circle", cx=256, cy=256, r=140, fill="#05070D"))
D["lunar-eclipse"] = lambda s: (sky(s, stars=10), moon_disc(s, r=150, phase=0.5, dark="#B5323A", lit="#B5323A"), s.F("circle", outline=False, cx=180, cy=256, r=150, fill="#000000", fill_opacity="0.35"))
D["total-eclipse"] = lambda s: (sky(s, stars=6, color="#05070D"), [s.M(f"M{arc_pt(256, 256, 150, a)[0]:.0f} {arc_pt(256, 256, 150, a)[1]:.0f} L{arc_pt(256, 256, 220, a)[0]:.0f} {arc_pt(256, 256, 220, a)[1]:.0f}", "#FFF1C2", 6) for a in range(0, 360, 15)],
                                s.F("circle", cx=256, cy=256, r=140, fill="#05070D"))
D["aurora"] = lambda s: (sky(s, stars=10), [s.M(f"M24 {y} C140 {y - 80} 260 {y + 40} 488 {y - 60}", c, 34) for y, c in ((220, "#4CE8A0"), (270, "#5EC8F0"), (310, "#B880E8"))],
                         s.F("path", outline=False, d="M24 420 L120 340 L200 400 L300 320 L400 400 L488 350 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill="#1F2A3A"))
D["southern-lights"] = lambda s: (sky(s, stars=10), [s.M(f"M24 {y} C140 {y - 80} 260 {y + 40} 488 {y - 60}", c, 34) for y, c in ((220, "#F48AA6"), (270, "#B880E8"), (310, "#4CE8A0"))],
                                  s.F("path", outline=False, d="M24 400 H488 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill="#E5E7EB"))
D["planet-alignment"] = lambda s: (sky(s, stars=10), [s.F("circle", cx=x, cy=256, r=r, fill=c) for x, r, c in ((80, 40, SUN), (170, 20, "#E8C27A"), (240, 24, C["blue"]), (320, 46, "#E8C9A0"), (420, 36, "#E8D29A"))])
D["transit-of-venus"] = lambda s: (sun(s, r=150), s.F("circle", cx=300, cy=230, r=26, fill="#1F1F24"))
D["starry-night-sky"] = lambda s: (sky(s, stars=40, seed=7), moon_disc(s, 380, 120, 50, 0.12, dark=NIGHT, craters=False))

# ---------------------------------------------------------------- constellations
def constellation(s, pts, lines):
    sky(s, stars=6)
    s.M(" ".join(f"M{pts[a][0]} {pts[a][1]} L{pts[b][0]} {pts[b][1]}" for a, b in lines), "#8FB8F8", 5)
    for x, y in pts:
        s.F("polygon", outline=False, points=star_pts(x, y, 16, 6, 4), fill="#FFF1C2")


BIG_DIPPER = [(80, 300), (160, 280), (230, 300), (290, 330), (300, 420), (420, 420), (420, 320)]
D["constellation"] = lambda s: constellation(s, BIG_DIPPER, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)])
D["big-dipper"] = D["constellation"]
D["little-dipper"] = lambda s: constellation(s, [(420, 100), (340, 150), (280, 210), (220, 260), (180, 340), (110, 320), (150, 240)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)])
D["orion"] = lambda s: constellation(s, [(170, 90), (340, 110), (220, 250), (256, 260), (292, 270), (160, 420), (350, 420)], [(0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6)])
D["cassiopeia"] = lambda s: constellation(s, [(70, 220), (160, 320), (250, 210), (350, 310), (440, 200)], [(0, 1), (1, 2), (2, 3), (3, 4)])
D["southern-cross"] = lambda s: constellation(s, [(256, 80), (256, 430), (150, 230), (360, 260), (310, 330)], [(0, 1), (2, 3)])
D["scorpius-constellation"] = lambda s: constellation(s, [(380, 80), (360, 140), (320, 200), (300, 270), (260, 330), (200, 380), (140, 380), (100, 330), (120, 280)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)])

# ---------------------------------------------------------------- zodiac signs (classic glyphs on a badge)
ZODIAC = {
    "aries": "M150 380 V240 C150 150 250 140 256 230 C262 140 362 150 362 240 V380 M256 230 V420",
    "taurus": "M256 260 m-90 0 a90 90 0 1 0 180 0 a90 90 0 1 0 -180 0 M110 120 C150 180 210 180 256 170 C302 180 362 180 402 120",
    "gemini": "M130 110 C200 140 312 140 382 110 M130 420 C200 390 312 390 382 420 M200 132 V398 M312 132 V398",
    "cancer-zodiac": "M110 200 C160 120 330 120 390 170 M160 200 m-40 0 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 M402 312 C352 392 182 392 122 342 M352 312 m-40 0 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0",
    "leo": "M190 300 m-50 0 a50 50 0 1 0 100 0 a50 50 0 1 0 -100 0 M230 270 C210 160 330 120 350 200 C370 280 300 320 330 400 C340 430 380 430 400 400",
    "virgo": "M110 380 V170 C110 130 170 130 170 170 V380 M170 170 C170 130 230 130 230 170 V380 M230 170 C230 130 290 130 290 170 V340 C290 400 380 400 380 330 C380 280 330 280 300 330 L260 420",
    "libra": "M100 400 H412 M100 330 H190 C170 230 342 230 322 330 H412",
    "scorpio": "M100 380 V170 C100 130 160 130 160 170 V380 M160 170 C160 130 220 130 220 170 V380 M220 170 C220 130 280 130 280 170 V360 C280 400 330 410 370 370 L400 340 M360 330 H402 V372",
    "sagittarius": "M120 400 L390 130 M260 130 H390 V260 M170 270 L260 360",
    "capricorn": "M100 160 L170 380 L230 160 V320 C230 410 330 410 330 330 C330 270 270 270 260 320 C250 400 330 420 390 380",
    "aquarius": "M90 220 L150 170 L210 220 L270 170 L330 220 L390 170 L430 200 M90 320 L150 270 L210 320 L270 270 L330 320 L390 270 L430 300",
    "pisces": "M140 110 C220 180 220 330 140 400 M372 110 C292 180 292 330 372 400 M130 256 H382",
}
for _id, _d in ZODIAC.items():
    D[_id] = (lambda d: lambda s: (s.F("circle", cx=256, cy=256, r=220, fill=THEME["accent"]),
                                   s.open(transform="translate(256 256) scale(0.8) translate(-256 -256)"), s.T(d, THEME["light"], 26), s.close()))(_d)


@reg("zodiac-wheel")
def _(s):
    s.F("circle", cx=256, cy=256, r=226, fill=THEME["accent"])
    s.F("circle", cx=256, cy=256, r=140, fill=THEME["accent-light"])
    for i, (k, d) in enumerate(ZODIAC.items()):
        x, y = arc_pt(256, 256, 184, -90 + i * 30)
        s.raw(f'<path d="{d}" transform="translate({x:.0f} {y:.0f}) scale(0.11) translate(-256 -256)" fill="none" stroke="{THEME["light"]}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>')
        x1, y1 = arc_pt(256, 256, 140, -75 + i * 30); x2, y2 = arc_pt(256, 256, 226, -75 + i * 30)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", THEME["light"], 4)
    sun(s, 256, 256, 50)


# ---------------------------------------------------------------- rockets and spacecraft
D["rocket"] = lambda s: rocket_part(s)
D["rocket-launch"] = lambda s: (sky(s, color="#8FD0FF", stars=0), s.F("rect", outline=False, x=24, y=410, width=464, height=78, fill="#9AA3AF"),
                                [s.F("circle", cx=x, cy=y, r=r, fill="#E5E7EB") for x, y, r in ((170, 430, 60), (256, 420, 70), (340, 430, 60))],
                                s.open(transform="translate(256 220) scale(0.7) translate(-256 -256)"), rocket_part(s), s.close())


def shuttle(s):
    s.F("path", d="M150 300 L60 420 H200Z", fill="#9AA3AF")
    s.F("path", d="M360 300 L450 420 H310Z", fill="#9AA3AF")
    s.F("rect", x=180, y=120, width=150, height=300, rx=40, fill="#C1662E")
    s.F("path", d="M210 180 C210 100 256 60 256 60 C256 60 300 100 300 180 V420 H210Z", fill=WHITE)
    s.F("polygon", points="256,260 300,340 300,420 210,420 210,340", fill=WHITE)
    s.F("rect", x=230, y=140, width=52, height=30, rx=8, fill=C["sky"])


D["space-shuttle"] = shuttle
D["saturn-v-rocket"] = lambda s: (s.F("path", d="M226 60 L256 20 L286 60 V120 H226Z", fill=WHITE), s.F("rect", x=210, y=120, width=92, height=300, fill=WHITE),
                                  [s.F("rect", outline=False, x=210, y=y, width=92, height=26, fill="#2E2A3B") for y in (170, 260, 360)],
                                  s.F("path", d="M200 420 H312 L330 470 H182Z", fill="#9AA3AF"))
D["reusable-rocket"] = lambda s: (s.F("rect", x=216, y=60, width=80, height=330, rx=36, fill=WHITE), s.F("rect", x=216, y=120, width=80, height=14, fill="#3A3A44"),
                                  s.T("M216 360 L150 450 M296 360 L362 450 M256 390 V460", "#5A5A66", 12), s.F("path", d="M226 390 Q256 440 286 390Z", fill=C["orange"]))
D["space-capsule"] = lambda s: (s.F("path", d="M150 400 L210 160 H302 L362 400Z", fill="#E5E7EB"), s.F("rect", x=226, y=120, width=60, height=40, fill="#9AA3AF"),
                                s.F("circle", cx=256, cy=260, r=34, fill=C["sky"]), s.F("path", d="M140 400 H372 L340 440 H172Z", fill="#8C6A4A"))
D["lunar-module"] = lambda s: (s.F("polygon", points="170,170 342,170 380,250 342,320 170,320 132,250", fill="#C9CED6"), s.F("rect", x=160, y=320, width=192, height=70, fill=C["gold"]),
                               s.T("M170 390 L110 460 M342 390 L402 460", "#9AA3AF", 10), s.F("rect", x=90, y=456, width=40, height=10, fill="#9AA3AF"), s.F("rect", x=382, y=456, width=40, height=10, fill="#9AA3AF"),
                               s.F("polygon", points="230,200 282,200 290,250 222,250", fill="#2C4A7A"))
D["launch-pad"] = lambda s: (s.F("rect", x=60, y=400, width=392, height=60, fill="#5A5A66"), [s.T(f"M{x} 400 V100", C["red"], 16) for x in (110, 170)],
                             [s.M(f"M110 {y} L170 {y + 40}", C["red"], 8) for y in range(110, 400, 50)], s.open(transform="translate(320 250) scale(0.55) translate(-256 -256)"), rocket_part(s), s.close())
D["rocket-stages"] = lambda s: [(s.F("rect", x=196, y=y, width=120, height=h, rx=14, fill=c), s.M(f"M196 {y + h} H316", "#3A3A44", 6)) for y, h, c in ((80, 90, WHITE), (180, 120, "#E5E7EB"), (310, 150, "#C9CED6"))]
D["ion-engine"] = lambda s: (s.F("rect", x=100, y=180, width=200, height=150, rx=30, fill="#C9CED6"), s.F("circle", cx=300, cy=256, r=80, fill="#9AA3AF"),
                             s.F("path", outline=False, d="M320 210 L480 180 V330 L320 300Z", fill="#5EA8FF", fill_opacity="0.6"))
D["solar-sail"] = lambda s: (sky(s, stars=10), s.F("polygon", points="256,60 450,256 256,450 62,256", fill="#E8D8A8"), s.M("M256 60 V450 M62 256 H450", "#C9B87A", 6), s.F("circle", cx=256, cy=256, r=24, fill="#9AA3AF"))

# ---------------------------------------------------------------- satellites, stations, probes, rovers
def solar_panel(s, x, y, w, h):
    s.F("rect", x=x, y=y, width=w, height=h, fill="#2C4A8A")
    for k in range(1, 4):
        s.M(f"M{x + w * k / 4:.0f} {y} V{y + h}", "#5A7AC0", 3)
    s.M(f"M{x} {y + h / 2:.0f} H{x + w}", "#5A7AC0", 3)


def satellite(s):
    solar_panel(s, 40, 216, 150, 80)
    solar_panel(s, 322, 216, 150, 80)
    s.M("M190 256 H322", "#9AA3AF", 8)
    s.F("rect", x=206, y=196, width=100, height=120, rx=10, fill=C["gold"])
    s.T("M256 196 V140", "#9AA3AF", 8)
    s.F("path", d="M216 140 C216 90 296 90 296 140Z", fill=WHITE)


D["satellite"] = satellite
D["communication-satellite"] = lambda s: (satellite(s), s.M("M300 110 C330 90 350 90 370 110 M290 80 C330 50 370 50 400 80", "#5EA8FF", 6))
D["weather-satellite"] = lambda s: (satellite(s), s.F("circle", cx=256, cy=420, r=50, fill="#E5E7EB"))
D["gps-satellite"] = lambda s: (satellite(s), s.F("polygon", outline=False, points="256,316 196,460 316,460", fill="#5EA8FF", fill_opacity="0.4"))
D["sputnik"] = lambda s: (s.F("circle", cx=230, cy=230, r=90, fill="#C9CED6"), [s.T(f"M{x1} {y1} L{x2} {y2}", "#9AA3AF", 6) for x1, y1, x2, y2 in ((290, 290, 460, 460), (300, 260, 470, 380), (260, 300, 380, 470), (280, 280, 430, 470))])


@reg("international-space-station")
def _(s):
    sky(s, stars=10)
    for x in (40, 110, 340, 410):
        solar_panel(s, x, 140, 60, 230)
    s.M("M70 256 H442", "#9AA3AF", 14)
    s.F("rect", x=200, y=226, width=112, height=60, rx=20, fill="#E5E7EB")
    s.F("rect", x=236, y=200, width=40, height=112, rx=14, fill="#E5E7EB")


D["space-station"] = lambda s: (sky(s, stars=10), s.raw('<circle cx="256" cy="256" r="180" fill="none" stroke="#E5E7EB" stroke-width="40"/>'), s.M("M256 76 V436 M76 256 H436", "#C9CED6", 14), s.F("circle", cx=256, cy=256, r=40, fill="#E5E7EB"))
D["space-probe"] = lambda s: (sky(s, stars=10), s.F("path", d="M150 200 C150 120 362 120 362 200Z", fill=WHITE), s.F("rect", x=216, y=200, width=80, height=80, fill=C["gold"]), s.T("M256 280 L256 400 M216 280 L120 400", "#9AA3AF", 6))
D["voyager-probe"] = lambda s: (sky(s, stars=12), s.F("ellipse", cx=256, cy=180, rx=110, ry=40, fill=WHITE), s.F("rect", x=226, y=220, width=60, height=60, fill=C["gold"]),
                                s.T("M256 280 L256 440 M286 250 L440 300 M226 250 L120 380", "#9AA3AF", 6))
D["space-telescope"] = lambda s: (sky(s, stars=10), s.F("rect", x=140, y=196, width=260, height=120, rx=50, fill="#C9CED6"), s.F("ellipse", cx=400, cy=256, rx=30, ry=60, fill="#3A3A44"),
                                  solar_panel(s, 180, 90, 120, 90), solar_panel(s, 180, 330, 120, 90))
D["james-webb-telescope"] = lambda s: (sky(s, stars=10), s.F("polygon", points="90,360 256,420 422,360 256,300", fill="#B8C0D8"), s.F("polygon", points="90,330 256,390 422,330 256,270", fill="#D9DEE5"),
                                       [s.F("polygon", outline=False, points=" ".join(f"{x:.0f},{y:.0f}" for x, y in (arc_pt(cx_, cy_, 34, k * 60 + 30) for k in range(6))), fill=C["gold"])
                                        for cx_, cy_ in ((256, 140), (226, 192), (286, 192), (196, 244), (256, 244), (316, 244))], s.T("M256 270 V120", "#9AA3AF", 4))


def rover(s, body="#E5E7EB", wheels=6, moon=False):
    s.F("rect", outline=False, x=24, y=380, width=464, height=108, rx=30, fill="#C9562E" if not moon else "#B7BEC8")
    s.F("rect", x=120, y=240, width=272, height=90, rx=14, fill=body)
    s.T("M330 240 V140 M310 140 H370", "#9AA3AF", 10)
    s.F("rect", x=340, y=110, width=60, height=40, rx=8, fill="#3A3A44")
    for i in range(3 if wheels == 6 else 2):
        x = 150 + i * (106 if wheels == 6 else 200)
        s.F("circle", cx=x, cy=370, r=34, fill="#5A5A66")
        s.F("circle", outline=False, cx=x, cy=370, r=12, fill="#9AA3AF")
    solar_panel(s, 140, 220, 120, 20)


D["mars-rover"] = lambda s: rover(s)
D["moon-rover"] = lambda s: rover(s, body="#E8D06E", wheels=4, moon=True)
D["lander"] = lambda s: (s.F("rect", outline=False, x=24, y=400, width=464, height=88, rx=30, fill="#C9562E"), s.F("polygon", points="180,180 332,180 360,300 152,300", fill=C["gold"]),
                         s.T("M170 300 L120 400 M342 300 L392 400", "#9AA3AF", 10), s.F("path", d="M216 180 C216 120 296 120 296 180Z", fill=WHITE))

# ---------------------------------------------------------------- astronauts (faceless visor)
def astronaut(s, pose="stand", flag=None):
    if pose == "stand":
        s.T("M226 330 V440 M286 330 V440", SUIT, 52)
        s.F("rect", x=190, y=428, width=60, height=26, rx=10, fill="#9AA3AF")
        s.F("rect", x=262, y=428, width=60, height=26, rx=10, fill="#9AA3AF")
        arms = ("M190 210 C160 260 156 300 166 340", "M322 210 C352 260 356 300 346 340")
    else:  # floating, arms out
        s.T("M226 330 L190 430 M286 330 L340 420", SUIT, 52)
        arms = ("M190 210 C150 200 120 170 100 130", "M322 210 C362 220 392 250 410 290")
    s.F("rect", x=170, y=170, width=172, height=180, rx=40, fill="#C9CED6")
    s.T(arms[0], SUIT, 46)
    s.F("rect", x=186, y=180, width=140, height=170, rx=46, fill=SUIT)
    s.F("rect", x=226, y=230, width=60, height=50, rx=8, fill="#5A7AC0")
    s.T(arms[1], SUIT, 46)
    s.F("circle", cx=256, cy=124, r=78, fill=SUIT)
    s.F("ellipse", cx=262, cy=128, rx=54, ry=44, fill=VISOR)
    s.F("ellipse", outline=False, cx=244, cy=114, rx=16, ry=10, fill="#8FB8F8")
    if flag:
        s.T("M346 340 V100", "#9AA3AF", 8)
        s.F("rect", x=350, y=104, width=110, height=70, fill=flag)


D["astronaut"] = lambda s: astronaut(s)
D["astronaut-floating"] = lambda s: (sky(s, stars=12), s.open(transform="rotate(-20 256 256)"), astronaut(s, "float"), s.close(), s.T("M190 250 C120 300 80 380 60 470", "#E5E7EB", 6))
D["space-suit"] = lambda s: (s.T("M226 330 V440 M286 330 V440", SUIT, 52), s.T("M190 210 C160 260 156 300 166 340 M322 210 C352 260 356 300 346 340", SUIT, 46),
                             s.F("rect", x=186, y=180, width=140, height=170, rx=46, fill=SUIT), s.F("rect", x=226, y=230, width=60, height=50, rx=8, fill="#5A7AC0"),
                             s.F("rect", x=220, y=140, width=72, height=46, rx=14, fill="#9AA3AF"))
D["space-helmet"] = lambda s: (s.F("circle", cx=256, cy=240, r=180, fill=SUIT), s.F("ellipse", cx=266, cy=246, rx=130, ry=104, fill=VISOR), s.F("ellipse", outline=False, cx=220, cy=200, rx=36, ry=22, fill="#8FB8F8"),
                               s.F("rect", x=130, y=380, width=252, height=60, rx=20, fill="#C9CED6"))
D["astronaut-food"] = lambda s: (s.F("path", d="M150 90 H362 V400 L326 440 H186 L150 400Z", fill="#E5E7EB"), s.F("rect", outline=False, x=176, y=170, width=160, height=140, rx=10, fill=C["orange"]),
                                 s.F("rect", x=236, y=60, width=40, height=40, rx=6, fill="#9AA3AF"))
D["moon-footprint"] = lambda s: (s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill="#B7BEC8"), s.F("path", d="M190 110 C150 160 150 360 200 420 H320 C370 360 370 160 330 110Z", fill="#8C96A3"),
                                 [s.M(f"M180 {y} H340", "#6B7280", 12) for y in range(150, 420, 34)])
D["flag-on-the-moon"] = lambda s: (sky(s, stars=10), s.F("path", outline=False, d="M24 380 C140 360 300 390 488 370 V452 C488 472 472 488 452 488 H60 C40 488 24 472 24 452Z", fill="#B7BEC8"),
                                   s.T("M200 390 V120", "#9AA3AF", 10), s.F("rect", x=204, y=124, width=170, height=110, fill=THEME["accent"]), earth(s, 410, 100, 50))
D["zero-gravity"] = lambda s: (s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill="#E5E7EB"), s.open(transform="rotate(25 256 256) translate(256 256) scale(0.8) translate(-256 -256)"), astronaut(s, "float"), s.close(),
                               [s.F("circle", cx=x, cy=y, r=16, fill=c) for x, y, c in ((90, 120, C["orange"]), (420, 140, C["blue"]), (100, 400, C["green"]))])
D["astronaut-training"] = lambda s: (s.F("rect", x=24, y=24, width=464, height=464, rx=36, fill="#8FD0FF"), s.open(transform="translate(256 280) scale(0.75) translate(-256 -256)"), astronaut(s, "float"), s.close(),
                                     [s.F("circle", cx=x, cy=y, r=r, fill=WHITE) for x, y, r in ((380, 120, 12), (400, 90, 8), (120, 140, 10))])

# ---------------------------------------------------------------- observing
def telescope(s, tube="#3D8BFD", refl=False):
    s.T("M256 300 L170 460 M256 300 L342 460 M256 300 V460", "#5A5A66", 12)
    s.open(transform="rotate(-30 256 260)")
    s.F("rect", x=110, y=220, width=300, height=80, rx=20, fill=tube)
    s.F("rect", x=400, y=210, width=40, height=100, rx=10, fill=shade(tube, 0.8))
    s.F("rect", x=80, y=240, width=40, height=40, rx=8, fill="#3A3A44")
    if refl:
        s.F("rect", x=320, y=200, width=30, height=24, rx=6, fill="#3A3A44")
    s.close()


D["telescope"] = lambda s: telescope(s)
D["refracting-telescope"] = lambda s: telescope(s, "#C98A3E")
D["reflecting-telescope"] = lambda s: telescope(s, WHITE, refl=True)
D["radio-telescope"] = lambda s: (s.F("rect", outline=False, x=24, y=420, width=464, height=50, rx=16, fill="#9BD7A8"), s.T("M256 330 L200 440 M256 330 L312 440", "#9AA3AF", 14),
                                  s.F("path", d="M90 180 C120 340 392 340 422 180 C380 240 132 240 90 180Z", fill=WHITE), s.T("M256 260 V130", "#9AA3AF", 8), s.F("circle", cx=256, cy=126, r=12, fill="#9AA3AF"))
D["observatory"] = lambda s: (sky(s, stars=14), s.F("rect", x=130, y=300, width=252, height=150, fill="#E5E7EB"), s.F("path", d="M110 300 C110 150 402 150 402 300Z", fill="#C9CED6"),
                              s.F("polygon", outline=False, points="236,160 276,160 296,300 216,300", fill=NIGHT), s.T("M256 260 L320 160", "#3A3A44", 18))
D["planetarium"] = lambda s: (s.F("path", d="M60 400 C60 140 452 140 452 400Z", fill="#14203A"), [s.F("polygon", outline=False, points=star_pts(x, y, 10, 4, 4), fill="#FFF1C2") for x, y in ((150, 280), (220, 220), (300, 240), (360, 300), (256, 320))],
                              s.F("rect", x=40, y=400, width=432, height=50, rx=10, fill="#9AA3AF"))
D["star-map"] = lambda s: (s.F("rect", x=60, y=80, width=392, height=352, rx=16, fill="#1E2A4A"), s.raw('<circle cx="256" cy="256" r="140" fill="none" stroke="#5A6A8A" stroke-width="4"/>'),
                           s.M("M150 200 L220 260 L300 220 L360 300", "#8FB8F8", 4), [s.F("circle", outline=False, cx=x, cy=y, r=8, fill="#FFF1C2") for x, y in ((150, 200), (220, 260), (300, 220), (360, 300))])
D["binoculars-stargazing"] = lambda s: (sky(s, stars=14), s.F("rect", x=120, y=230, width=110, height=180, rx=40, fill="#3A3A44"), s.F("rect", x=282, y=230, width=110, height=180, rx=40, fill="#3A3A44"),
                                        s.F("rect", x=220, y=280, width=72, height=50, fill="#5A5A66"), s.F("circle", cx=175, cy=250, r=34, fill="#8FD0FF"), s.F("circle", cx=337, cy=250, r=34, fill="#8FD0FF"))

# ---------------------------------------------------------------- UFOs and aliens
def ufo(s, beam=False):
    if beam:
        s.F("polygon", outline=False, points="216,300 296,300 400,480 112,480", fill="#B8F0A8", fill_opacity="0.6")
    s.F("path", d="M190 210 C190 130 322 130 322 210Z", fill="#B8E0F8")
    s.F("ellipse", cx=256, cy=250, rx=200, ry=56, fill="#9AA3AF")
    s.F("ellipse", outline=False, cx=256, cy=236, rx=150, ry=20, fill="#C9CED6")
    for x in (120, 190, 256, 322, 392):
        s.F("circle", cx=x, cy=270, r=12, fill="#FFE38A")


def alien(s, color="#7DD36B", big_eyes=True):
    s.T("M220 330 V440 M292 330 V440", color, 34)
    s.T("M200 280 C160 300 150 340 160 370 M312 280 C352 300 362 340 352 370", color, 26)
    s.F("ellipse", cx=256, cy=300, rx=70, ry=80, fill=color)
    s.T("M220 110 C200 60 180 50 170 40 M292 110 C312 60 332 50 342 40", color, 8)
    s.F("circle", cx=170, cy=40, r=12, fill=color)
    s.F("circle", cx=342, cy=40, r=12, fill=color)
    s.F("ellipse", cx=256, cy=170, rx=100, ry=90, fill=color)
    for x, side in ((220, "left"), (292, "right")):
        s.F("ellipse", outline=False, cx=x, cy=170, rx=26 if big_eyes else 14, ry=34 if big_eyes else 14, fill="#1F1F24")
    s.M("M236 220 Q256 232 276 220", INK, 5)


D["ufo"] = lambda s: (sky(s, stars=12), ufo(s))
D["alien"] = lambda s: alien(s, "#9AD8A8")
D["alien-spaceship"] = lambda s: (sky(s, stars=12), s.open(transform="translate(256 256) scale(1.1) translate(-256 -256)"), ufo(s), s.close())
D["alien-abduction-beam"] = lambda s: (sky(s, stars=10), ufo(s, beam=True), s.F("ellipse", cx=256, cy=440, rx=40, ry=26, fill=WHITE))
D["little-green-alien"] = lambda s: alien(s, "#5EC84A")


if __name__ == "__main__":
    run("space", D, sys.argv[1:] or None)
