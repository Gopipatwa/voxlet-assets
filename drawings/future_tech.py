"""future-tech drawings (themed colours). Run: python drawings/future_tech.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tech import (A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, INK, SKIN, HAIR, WHITE, arc_pt, arrow, bolt, cloud, dot, lock, registry, ring, run, screen, shine, star_pts, txt, waves, wifi)  # noqa: E402

D, reg = registry()


def head_bot(s, cx, cy, k=1.0, color=A1, eyes=True):
    s.open(transform=f"translate({cx} {cy}) scale({k}) translate(-256 -256)")
    s.T("M256 130 V100", DARK, 10)
    s.F("circle", cx=256, cy=90, r=16, fill=A2)
    s.F("rect", x=146, y=130, width=220, height=170, rx=54, fill=color)
    s.F("rect", outline=False, x=170, y=162, width=172, height=82, rx=34, fill=DARK)
    if eyes:
        s.open("part-eye-left", "216 203")
        s.F("circle", outline=False, cx=216, cy=203, r=18, fill=A1L)
        s.close()
        s.open("part-eye-right", "296 203")
        s.F("circle", outline=False, cx=296, cy=203, r=18, fill=A1L)
        s.close()
    s.close()


def humanoid(s, cx=256, cy=270, k=1.0, color=A1, accent=A2):
    s.open(transform=f"translate({cx} {cy}) scale({k}) translate(-256 -270)")
    s.F("rect", x=170, y=330, width=60, height=130, rx=22, fill=A1D)
    s.F("rect", x=282, y=330, width=60, height=130, rx=22, fill=A1D)
    s.F("rect", x=156, y=440, width=84, height=34, rx=16, fill=DARK)
    s.F("rect", x=272, y=440, width=84, height=34, rx=16, fill=DARK)
    s.F("rect", x=70, y=210, width=50, height=140, rx=24, fill=MID)
    s.F("rect", x=392, y=210, width=50, height=140, rx=24, fill=MID)
    s.F("rect", x=120, y=190, width=272, height=170, rx=54, fill=color)
    s.F("circle", cx=256, cy=270, r=30, fill=accent)
    s.F("circle", outline=False, cx=256, cy=270, r=12, fill=A2L)
    head_bot(s, 256, 110, 0.62, color)
    s.close()


# ================================================================ robots-ai
@reg("humanoid-robot")
def _(s):
    humanoid(s, 256, 270, 1.0)


@reg("robot-assistant")
def _(s):
    head_bot(s, 256, 190, 1.2)
    s.F("rect", x=150, y=350, width=212, height=110, rx=44, fill=A1D)
    s.F("circle", cx=256, cy=405, r=24, fill=A2)
    s.F("rect", x=60, y=360, width=100, height=70, rx=16, fill=LIGHT)
    s.F("rect", outline=False, x=72, y=372, width=76, height=14, rx=7, fill=A1L)
    s.F("rect", outline=False, x=72, y=396, width=50, height=14, rx=7, fill=A1L)


@reg("robot-butler")
def _(s):
    humanoid(s, 200, 280, 0.9)
    s.F("path", d="M226 182 L256 198 L286 182 V214 L256 198 L226 214Z", fill=A2)
    s.F("rect", x=312, y=240, width=170, height=20, rx=10, fill=MID)
    s.F("path", d="M340 236 C340 190 454 190 454 236Z", fill=LIGHT)
    s.F("rect", x=388, y=180, width=16, height=14, rx=6, fill=MID)


@reg("robot-doctor")
def _(s):
    humanoid(s, 256, 270, 1.0, LIGHT, A1)
    s.F("rect", outline=False, x=240, y=236, width=32, height=76, rx=8, fill=A2)
    s.F("rect", outline=False, x=218, y=258, width=76, height=32, rx=8, fill=A2)
    s.F("rect", x=210, y=150, width=92, height=14, rx=7, fill=A2)
    s.T("M200 195 C170 260 230 300 256 300", A1D, 12)


@reg("robot-teacher")
def _(s):
    s.F("rect", x=250, y=60, width=230, height=190, rx=16, fill=A1D)
    s.F("rect", outline=False, x=266, y=76, width=198, height=158, rx=8, fill=A1L)
    s.M("M290 130 H420 M290 170 H380", DARK, 10)
    humanoid(s, 140, 290, 0.78, A1)
    s.T("M240 230 L360 180", A2, 12)


@reg("robot-dog")
def _(s):
    s.F("rect", x=90, y=190, width=270, height=130, rx=50, fill=A1)
    s.F("rect", x=100, y=310, width=44, height=130, rx=16, fill=A1D)
    s.F("rect", x=190, y=310, width=44, height=130, rx=16, fill=A1D)
    s.F("rect", x=250, y=310, width=44, height=130, rx=16, fill=A1D)
    s.F("rect", x=320, y=310, width=44, height=130, rx=16, fill=A1D)
    s.F("rect", x=300, y=100, width=170, height=130, rx=44, fill=A1)
    s.F("rect", outline=False, x=330, y=130, width=110, height=56, rx=24, fill=DARK)
    s.open("part-eye-right", "400 158")
    s.F("circle", outline=False, cx=400, cy=158, r=14, fill=A1L)
    s.close()
    s.F("rect", x=420, y=190, width=60, height=34, rx=14, fill=MID)
    s.F("path", d="M310 108 L300 50 L346 100Z", fill=A2)
    s.T("M90 220 L40 170", A2, 14)


@reg("ai-brain")
def _(s):
    s.F("path", d="M256 80 C170 40 70 100 90 200 C60 250 90 330 160 340 C170 400 330 400 350 340 C420 330 450 250 420 200 C440 100 340 40 256 80Z", fill=A1L)
    s.M("M256 90 V330 M256 180 H180 M256 260 H340 M180 180 V240 M340 260 V200", A1D, 10)
    for x, y in ((180, 240), (340, 200), (256, 90), (180, 180), (340, 260)):
        s.F("circle", cx=x, cy=y, r=20, fill=A2)
    s.F("rect", x=190, y=400, width=132, height=50, rx=14, fill=A1)
    txt(s, "AI", 256, 425, 70, 30, LIGHT)


@reg("android")
def _(s):
    s.F("rect", x=170, y=330, width=60, height=130, rx=22, fill=MID)
    s.F("rect", x=282, y=330, width=60, height=130, rx=22, fill=MID)
    s.F("rect", x=156, y=440, width=84, height=34, rx=16, fill=DARK)
    s.F("rect", x=272, y=440, width=84, height=34, rx=16, fill=DARK)
    s.F("rect", x=70, y=210, width=50, height=140, rx=24, fill=MID)
    s.F("rect", x=392, y=210, width=50, height=140, rx=24, fill=MID)
    s.F("rect", x=120, y=190, width=272, height=170, rx=54, fill=LIGHT)
    s.M("M256 200 V350", MID, 8)
    s.F("path", d="M256 60 C196 60 172 110 176 150 C180 196 216 224 256 224 C296 224 332 196 336 150 C340 110 316 60 256 60Z", fill=SKIN)
    s.F("path", outline=False, d="M176 140 C176 80 220 56 256 60 C300 56 340 80 336 140 C300 130 220 110 176 140Z", fill=HAIR)
    dot(s, 226, 160, 9, DARK)
    dot(s, 286, 160, 9, DARK)
    s.M("M240 192 C250 200 262 200 272 192", DARK, 7)
    s.F("rect", x=232, y=222, width=48, height=26, rx=8, fill=MID)


@reg("cyborg")
def _(s):
    s.F("path", d="M256 70 C190 70 156 120 160 190 C164 260 210 320 256 320 C302 320 348 260 352 190 C356 120 322 70 256 70Z", fill=SKIN)
    s.F("path", d="M256 70 C322 70 356 120 352 190 C348 260 302 320 256 320Z", fill=MID)
    s.F("path", outline=False, d="M170 130 C170 80 220 60 256 70 V120 C220 110 190 120 170 130Z", fill=HAIR)
    dot(s, 218, 190, 10, DARK)
    s.F("circle", cx=300, cy=190, r=26, fill=DARK)
    s.F("circle", outline=False, cx=300, cy=190, r=12, fill=A2)
    s.M("M256 120 V300", A1D, 6)
    s.M("M290 250 H340 M310 120 H350", A1, 8)
    s.F("rect", x=200, y=320, width=112, height=140, rx=26, fill=A1D)
    s.F("rect", outline=False, x=300, y=240, width=40, height=14, rx=7, fill=A2)
    s.M("M226 262 C240 272 252 272 262 262", DARK, 7)


@reg("nanobots")
def _(s):
    for x, y, r, rot in ((140, 150, 48, -20), (330, 120, 36, 25), (250, 280, 56, 8), (110, 360, 32, 30), (390, 340, 44, -25)):
        s.open(transform=f"rotate({rot} {x} {y})")
        for a in (-60, 60, 180, 0):
            x2, y2 = arc_pt(x, y, r * 1.6, a)
            s.T(f"M{x} {y} L{x2:.0f} {y2:.0f}", DARK, 8)
        s.F("circle", cx=x, cy=y, r=r, fill=A1)
        s.F("circle", outline=False, cx=x - r * 0.25, cy=y - r * 0.25, r=r * 0.25, fill=A1L)
        dot(s, x + r * 0.2, y + r * 0.1, r * 0.2, A2)
        s.close()


@reg("swarm-robots")
def _(s):
    pos = [(120, 120, 0.9), (250, 90, 0.7), (370, 140, 0.9), (170, 250, 0.75), (310, 260, 1.0), (90, 380, 0.8), (230, 390, 0.7), (390, 390, 0.9)]
    for i, (x, y, k) in enumerate(pos):
        s.open(transform=f"translate({x} {y}) scale({k})")
        s.F("rect", x=-44, y=-30, width=88, height=60, rx=20, fill=A1 if i % 3 else A2)
        s.F("circle", outline=False, cx=-16, cy=-4, r=9, fill=LIGHT)
        s.F("circle", outline=False, cx=16, cy=-4, r=9, fill=LIGHT)
        s.T("M-30 30 l-10 16 M30 30 l10 16 M0 -30 v-18", DARK, 6)
        s.close()


# ================================================================ future-transport
@reg("flying-car")
def _(s):
    s.F("path", d="M50 300 C50 250 90 230 130 220 L190 160 H340 L400 220 C440 230 470 250 470 300 V340 H50Z", fill=A1)
    s.F("path", outline=False, d="M200 175 H330 L376 220 H160Z", fill=A1L)
    s.F("circle", cx=140, cy=345, r=44, fill=DARK)
    s.F("circle", cx=380, cy=345, r=44, fill=DARK)
    dot(s, 140, 345, 16, MID)
    dot(s, 380, 345, 16, MID)
    s.F("rect", x=130, y=120, width=100, height=14, rx=7, fill=DARK)
    s.F("rect", x=282, y=120, width=100, height=14, rx=7, fill=DARK)
    s.T("M180 134 V160 M332 134 V160", DARK, 8)
    s.M("M60 420 H150 M200 440 H300 M350 420 H450", MID, 12)


@reg("hyperloop")
def _(s):
    s.F("rect", x=30, y=170, width=452, height=170, rx=85, fill=LIGHT)
    s.F("rect", outline=False, x=50, y=186, width=412, height=36, rx=18, fill=A1L, fill_opacity="0.5")
    s.F("rect", x=100, y=215, width=280, height=80, rx=40, fill=A1)
    s.F("rect", outline=False, x=140, y=235, width=40, height=26, rx=10, fill=LIGHT)
    s.F("rect", outline=False, x=200, y=235, width=40, height=26, rx=10, fill=LIGHT)
    s.F("rect", outline=False, x=260, y=235, width=40, height=26, rx=10, fill=LIGHT)
    s.M("M30 400 H482", MID, 10)
    s.F("rect", x=60, y=340, width=24, height=60, fill=MID)
    s.F("rect", x=428, y=340, width=24, height=60, fill=MID)
    s.M("M390 255 H450", A2, 14)


@reg("air-taxi")
def _(s):
    s.F("path", d="M110 290 C110 210 170 180 256 180 C342 180 402 210 402 290 V330 H110Z", fill=A2)
    s.F("path", outline=False, d="M160 200 H350 C380 200 390 240 392 270 H122 C124 240 134 200 160 200Z", fill=A1L)
    for x in (80, 256, 432):
        s.F("rect", x=x - 56, y=130, width=112, height=14, rx=7, fill=DARK)
        s.T(f"M{x} 144 V180", DARK, 8)
    s.T("M170 330 V380 M342 330 V380 M130 384 H210 M302 384 H382", DARK, 12)


@reg("self-driving-car")
def _(s):
    s.F("path", d="M50 330 C50 290 80 260 120 250 L170 190 H340 L392 250 C440 260 464 290 464 330 V370 H50Z", fill=A1)
    s.F("path", outline=False, d="M184 205 H330 L366 250 H146Z", fill=A1L)
    for x in (140, 372):
        s.F("circle", cx=x, cy=375, r=44, fill=DARK)
        dot(s, x, 375, 16, MID)
    s.F("rect", x=220, y=130, width=72, height=44, rx=12, fill=A2)
    waves(s, 256, 152, 120, A2, 10, 2, -150, -30)
    s.M("M70 440 H140 M190 440 H260 M310 440 H380", MID, 10)


@reg("maglev-train-future")
def _(s):
    s.F("path", d="M40 300 C40 200 120 170 260 170 H400 C460 170 480 230 470 300Z", fill=LIGHT)
    s.F("path", outline=False, d="M90 220 H260 C300 220 330 200 340 195 H150 C110 195 95 205 90 220Z", fill=A1L)
    s.F("rect", outline=False, x=300, y=205, width=130, height=40, rx=16, fill=A1)
    s.F("path", outline=False, d="M40 270 H470 V300 H40Z", fill=A2)
    s.F("rect", x=20, y=340, width=472, height=34, rx=10, fill=DARK)
    s.M("M60 322 H450", A1L, 6, dash="14 18")


@reg("personal-jetpack")
def _(s):
    s.F("rect", x=130, y=110, width=100, height=230, rx=40, fill=A1)
    s.F("rect", x=282, y=110, width=100, height=230, rx=40, fill=A1)
    s.F("rect", x=140, y=200, width=232, height=60, rx=14, fill=A1D)
    for x in (180, 332):
        s.F("path", d=f"M{x - 34} 340 H{x + 34} L{x + 20} 440 C{x + 10} 470 {x - 10} 470 {x - 20} 440Z", fill=A2)
        s.F("path", outline=False, d=f"M{x - 16} 350 H{x + 16} L{x + 8} 410 C{x} 424 {x} 424 {x - 8} 410Z", fill=A2L)
    s.F("circle", cx=180, cy=130, r=22, fill=MID)
    s.F("circle", cx=332, cy=130, r=22, fill=MID)


@reg("hoverboard")
def _(s):
    s.F("path", d="M50 280 C50 240 100 230 256 230 C412 230 462 240 462 280 C462 320 412 330 256 330 C100 330 50 320 50 280Z", fill=A1)
    s.F("path", outline=False, d="M90 252 H420", fill="none", stroke=A1L, stroke_width="14", stroke_linecap="round")
    s.F("ellipse", cx=256, cy=410, rx=170, ry=26, fill=A2, fill_opacity="0.6")
    for x in (150, 256, 362):
        s.M(f"M{x} 350 v50", A2, 14)


@reg("passenger-drone")
def _(s):
    s.F("rect", x=170, y=200, width=172, height=130, rx=48, fill=A1)
    s.F("rect", outline=False, x=200, y=224, width=112, height=60, rx=24, fill=A1L)
    s.T("M170 230 L80 170 M342 230 L432 170", DARK, 14)
    for x in (70, 442):
        s.F("ellipse", cx=x, cy=160, rx=62, ry=14, fill=MID)
    s.T("M200 330 L180 390 M312 330 L332 390 M150 392 H220 M292 392 H362", DARK, 12)


@reg("space-plane")
def _(s):
    s.open(transform="rotate(-25 256 256)")
    s.F("path", d="M60 256 C60 200 200 190 340 210 C440 224 470 256 470 256 C470 256 440 288 340 302 C200 322 60 312 60 256Z", fill=LIGHT)
    s.F("path", d="M200 230 L120 120 H190 L300 220Z", fill=A1)
    s.F("path", d="M200 282 L120 392 H190 L300 292Z", fill=A1)
    s.F("path", outline=False, d="M370 222 C410 224 440 240 450 256 C440 272 410 288 370 290Z", fill=A1L)
    s.F("rect", x=40, y=236, width=40, height=40, rx=10, fill=A2)
    s.close()
    s.M("M30 440 H100 M20 400 H70", MID, 10)


# ================================================================ future-space
def ground(s, color=A2L, y=380, extra=A2):
    s.F("path", d=f"M0 {y} C100 {y - 30} 200 {y + 20} 300 {y - 10} C400 {y - 30} 460 {y} 512 {y - 20} V512 H0Z", fill=color)


def dome(s, cx, cy, r, color=A1L):
    s.F("path", d=f"M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}Z", fill=color, fill_opacity="0.9")
    s.F("rect", outline=False, x=cx - r * 0.55, y=cy - r * 0.55, width=r * 0.18, height=r * 0.5, rx=8, fill=WHITE, fill_opacity="0.7")


@reg("mars-base")
def _(s):
    s.F("circle", cx=380, cy=130, r=50, fill=LIGHT)
    ground(s, A2, 360)
    dome(s, 180, 360, 110, A1L)
    s.F("rect", x=250, y=300, width=150, height=70, rx=18, fill=LIGHT)
    s.F("rect", outline=False, x=272, y=320, width=40, height=24, rx=8, fill=A1L)
    s.T("M300 300 V250", DARK, 8)
    s.F("circle", cx=300, cy=240, r=14, fill=A1)
    s.F("circle", outline=False, cx=140, cy=330, r=14, fill=A1)


@reg("moon-base")
def _(s):
    s.F("circle", cx=400, cy=110, r=60, fill=A1L)
    s.F("path", d="M0 400 C100 360 220 410 330 380 C420 360 470 390 512 380 V512 H0Z", fill=MID)
    s.F("ellipse", outline=False, cx=90, cy=440, rx=50, ry=14, fill=DARK, fill_opacity="0.3")
    dome(s, 200, 380, 110, A1L)
    s.F("rect", x=300, y=330, width=120, height=70, rx=18, fill=LIGHT)
    s.F("rect", outline=False, x=322, y=350, width=36, height=22, rx=8, fill=A1L)
    s.T("M420 365 H470", DARK, 10)
    s.F("circle", cx=480, cy=365, r=18, fill=A2)


@reg("space-colony")
def _(s):
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="70" fill="none" stroke="{INK}" stroke-width="86" data-outline="under"/>')
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="70" fill="none" stroke="{A1}" stroke-width="66"/>')
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="70" fill="none" stroke="{A1L}" stroke-width="24" stroke-dasharray="40 30"/>')
    s.F("circle", cx=256, cy=256, r=60, fill=LIGHT)
    s.F("circle", outline=False, cx=256, cy=256, r=28, fill=A2)
    s.T("M256 196 V120 M256 316 V392", MID, 12)
    s.F("circle", cx=256, cy=100, r=22, fill=A2)
    s.F("circle", cx=256, cy=412, r=22, fill=A2)


@reg("space-elevator")
def _(s):
    s.F("path", d="M0 460 C120 430 260 440 380 470 H512 V512 H0Z", fill=A1)
    s.F("circle", cx=256, cy=470, r=60, fill=A1D)
    s.T("M256 460 V120", DARK, 14)
    s.F("rect", x=230, y=290, width=52, height=60, rx=14, fill=A2)
    s.F("rect", outline=False, x=240, y=302, width=32, height=20, rx=6, fill=A2L)
    s.F("rect", x=190, y=60, width=132, height=60, rx=20, fill=LIGHT)
    s.F("rect", outline=False, x=214, y=76, width=84, height=14, rx=7, fill=A1L)
    s.F("circle", cx=420, cy=120, r=26, fill=LIGHT)
    s.F("circle", cx=90, cy=150, r=16, fill=LIGHT)


@reg("space-hotel")
def _(s):
    s.raw(f'<circle cx="256" cy="256" r="150" fill="none" stroke="{INK}" stroke-width="66" data-outline="under"/>')
    s.raw(f'<circle cx="256" cy="256" r="150" fill="none" stroke="{A1}" stroke-width="46"/>')
    s.raw(f'<circle cx="256" cy="256" r="150" fill="none" stroke="{A1L}" stroke-width="14" stroke-dasharray="30 24"/>')
    s.T("M256 256 L256 106 M256 256 L386 331 M256 256 L126 331", DARK, 12)
    s.F("circle", cx=256, cy=256, r=44, fill=A2)
    s.F("polygon", points=star_pts(256, 256, 22, 10, 5), fill=LIGHT)


@reg("asteroid-mining")
def _(s):
    s.F("path", d="M110 300 C80 230 140 170 220 180 C300 150 400 190 410 280 C440 340 360 420 280 410 C200 450 120 400 110 300Z", fill=MID)
    for x, y, r in ((190, 260, 30), (320, 240, 22), (270, 350, 26)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=DARK, fill_opacity="0.3")
    s.F("rect", x=60, y=80, width=130, height=70, rx=18, fill=A1)
    s.F("rect", outline=False, x=80, y=98, width=60, height=20, rx=8, fill=A1L)
    s.T("M190 130 L250 190", DARK, 12)
    s.F("polygon", points="250,190 262,220 232,206", fill=A2)
    s.F("polygon", points="380,180 440,130 420,200", fill=A2L)
    s.F("polygon", points=star_pts(420, 100, 26, 10, 4), fill=A2)


@reg("terraforming-mars")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=A2)
    s.F("path", outline=False, d="M90 230 C130 160 210 190 250 160 C300 130 360 150 380 190 C340 240 300 230 270 270 C220 290 150 300 100 270Z", fill=A1)
    s.F("path", outline=False, d="M180 370 C230 340 310 380 350 340 C380 380 330 430 250 430 C210 430 180 400 180 370Z", fill=A1)
    s.F("circle", outline=False, cx=360, cy=270, r=26, fill=A2L)
    s.F("circle", outline=False, cx=140, cy=330, r=18, fill=A2L)
    s.M("M120 160 C150 130 200 120 240 126", WHITE, 12)


@reg("generation-starship")
def _(s):
    s.F("path", d="M40 256 C120 200 280 190 420 215 L470 256 L420 297 C280 322 120 312 40 256Z", fill=A1)
    s.F("path", outline=False, d="M120 236 C200 215 300 212 400 228", fill="none", stroke=A1L, stroke_width="16", stroke_linecap="round")
    for x in (160, 220, 280, 340):
        s.F("rect", outline=False, x=x, y=250, width=40, height=26, rx=10, fill=A2L)
    s.F("path", d="M40 256 L0 220 V292Z", fill=A2)
    s.M("M470 256 L500 256", A2, 14)


@reg("orbital-solar-power-station")
def _(s):
    for x in (60, 354):
        s.F("rect", x=x, y=150, width=98, height=190, rx=8, fill=A1)
        for i in range(1, 3):
            s.M(f"M{x} {150 + i * 63} H{x + 98}", A1L, 5)
        s.M(f"M{x + 49} 150 V340", A1L, 5)
    s.T("M158 245 H232 M354 245 H280", DARK, 14)
    s.F("rect", x=214, y=190, width=84, height=110, rx=18, fill=LIGHT)
    s.F("circle", cx=256, cy=245, r=22, fill=A2)
    arrow(s, 256, 310, 256, 440, A2, 12, 30)
    s.F("circle", cx=256, cy=470, r=26, fill=A1D)


# ================================================================ human-enhancement
@reg("brain-computer-link")
def _(s):
    s.F("path", d="M256 90 C170 50 80 110 100 200 C70 250 100 320 160 330 C170 380 320 380 340 330 C400 320 430 250 400 200 C420 110 340 50 256 90Z", fill=A1L)
    s.F("rect", x=210, y=130, width=92, height=60, rx=14, fill=DARK)
    s.F("circle", outline=False, cx=256, cy=160, r=14, fill=A2)
    s.T("M256 190 C256 240 200 250 190 290", A2, 8)
    s.T("M300 150 C360 100 420 140 440 100", A2, 8)
    s.F("rect", x=360, y=380, width=120, height=80, rx=16, fill=LIGHT)
    s.F("rect", outline=False, x=376, y=396, width=88, height=14, rx=7, fill=A1L)
    s.F("rect", outline=False, x=376, y=422, width=58, height=14, rx=7, fill=A1L)
    s.T("M300 340 C340 400 330 420 360 420", A2, 8)
    wifi(s, 80, 400, 60, A1, 10)


@reg("exoskeleton")
def _(s):
    s.F("path", d="M256 60 C206 60 190 100 194 140 C198 180 226 200 256 200 C286 200 314 180 318 140 C322 100 306 60 256 60Z", fill=SKIN)
    s.F("path", outline=False, d="M194 130 C194 80 230 58 256 62 C290 58 322 80 318 130 C290 120 230 110 194 130Z", fill=HAIR)
    s.F("rect", x=190, y=210, width=132, height=130, rx=34, fill=LIGHT)
    s.T("M180 230 C130 270 130 320 150 380 M332 230 C382 270 382 320 362 380", A1, 22)
    s.T("M220 340 V400 L200 470 M292 340 V400 L312 470", A1, 22)
    for x, y in ((150, 296), (362, 296), (216, 400), (296, 400)):
        s.F("circle", cx=x, cy=y, r=20, fill=A2)
    s.F("rect", x=170, y=330, width=172, height=30, rx=12, fill=A1D)


@reg("bionic-arm")
def _(s):
    s.F("rect", x=60, y=200, width=110, height=110, rx=30, fill=SKIN)
    s.F("rect", x=160, y=210, width=130, height=90, rx=26, fill=A1)
    s.F("circle", cx=290, cy=256, r=30, fill=A2)
    s.F("rect", x=300, y=210, width=110, height=90, rx=24, fill=MID)
    for i, a in enumerate((-40, -10, 20, 50)):
        s.T(f"M400 256 L{440 + 20 * math.cos(math.radians(a)):.0f} {256 + 70 * math.sin(math.radians(a)):.0f}", A1D, 18)
    s.T("M400 250 L452 220", A1D, 18)
    s.M("M180 240 H270 M180 270 H250", A1L, 7)


@reg("bionic-eye")
def _(s):
    s.F("path", d="M30 256 C110 130 402 130 482 256 C402 382 110 382 30 256Z", fill=LIGHT)
    s.F("circle", cx=256, cy=256, r=100, fill=A1)
    s.raw(f'<circle cx="256" cy="256" r="64" fill="none" stroke="{A1L}" stroke-width="8"/>')
    s.F("circle", cx=256, cy=256, r=44, fill=DARK)
    dot(s, 256, 256, 16, A2)
    for a in range(0, 360, 45):
        x1, y1 = arc_pt(256, 256, 46, a)
        x2, y2 = arc_pt(256, 256, 98, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", A1D, 6)
    s.F("circle", outline=False, cx=222, cy=222, r=12, fill=WHITE, fill_opacity="0.8")


@reg("smart-contact-lens")
def _(s):
    s.F("path", d="M56 220 C56 380 456 380 456 220 C400 130 112 130 56 220Z", fill="#E3F3FC")
    s.F("circle", cx=256, cy=250, r=100, fill=A1L, fill_opacity="0.7")
    ring(s, 256, 250, 62, A1, 14)
    s.F("circle", cx=256, cy=250, r=36, fill=DARK)
    dot(s, 256, 250, 12, A2)
    s.M("M170 330 H340", A1D, 6)
    dot(s, 360, 190, 12, A2)
    s.M("M376 190 H430 M372 170 L420 140", A2, 8)


@reg("gene-editing")
def _(s):
    s.T("M170 60 C400 140 110 240 340 330", A1, 24)
    s.T("M342 60 C112 140 402 240 172 330", A2, 24)
    s.F("path", d="M370 340 L430 440 L400 450 L340 350Z", fill=MID)
    s.F("path", d="M300 350 L400 300 L430 340 L340 400Z", fill=LIGHT)
    s.F("polygon", points=star_pts(440, 110, 36, 14, 4), fill=A2)
    s.M("M180 440 H260", MID, 10)


@reg("designer-genes")
def _(s):
    s.T("M170 60 C400 140 110 240 340 330", A1, 22)
    s.T("M342 60 C112 140 402 240 172 330", A2, 22)
    s.F("rect", x=60, y=350, width=392, height=110, rx=30, fill=A1D)
    for i, c in enumerate((A2, A1L, LIGHT, A2L, A1)):
        s.F("rect", outline=False, x=84 + i * 72, y=374, width=56, height=60, rx=16, fill=c)


@reg("digital-twin")
def _(s):
    s.F("rect", x=60, y=210, width=170, height=200, rx=34, fill=A1)
    s.F("circle", cx=145, cy=150, r=50, fill=A1L)
    s.F("rect", x=282, y=210, width=170, height=200, rx=34, fill=A1L, fill_opacity="0.55")
    s.F("circle", cx=367, cy=150, r=50, fill=A1L, fill_opacity="0.55")
    s.raw(f'<rect x="282" y="210" width="170" height="200" rx="34" fill="none" stroke="{A1}" stroke-width="8" stroke-dasharray="16 12"/>')
    s.raw(f'<circle cx="367" cy="150" r="50" fill="none" stroke="{A1}" stroke-width="8" stroke-dasharray="16 12"/>')
    s.M("M240 260 H272 M240 300 H272", A2, 10)
    s.F("polygon", points="262,244 262,276 286,260", fill=A2)
    s.F("polygon", points="250,284 250,316 226,300", fill=A2)


@reg("mind-upload")
def _(s):
    s.F("path", d="M110 280 C80 220 120 140 200 130 C260 100 330 130 340 200 C380 230 360 290 320 300 C310 340 220 350 200 310 C170 320 130 310 110 280Z", fill=A1L)
    s.M("M210 180 V260 M210 220 H280 M260 190 V250", A1D, 8)
    arrow(s, 256, 360, 256, 440, A2, 14, 34)
    cloud(s, 380, 400, 0.5, LIGHT)
    s.F("circle", cx=300, cy=180, r=18, fill=A2)


@reg("lab-grown-organ")
def _(s):
    s.F("path", d="M256 440 C60 310 50 190 70 150 C100 70 200 60 256 150 C312 60 412 70 442 150 C462 190 452 310 256 440Z", fill=A2, fill_opacity="0.9")
    s.F("path", outline=False, d="M120 150 C140 110 190 106 220 160", fill="none", stroke=A2L, stroke_width="24", stroke_linecap="round")
    s.F("rect", x=170, y=400, width=172, height=70, rx=20, fill="#E3F3FC")
    s.F("path", outline=False, d="M180 430 H332 V450 C332 462 320 466 310 466 H202 C190 466 180 462 180 450Z", fill=A1L)
    s.T("M200 400 V370 M312 400 V370", MID, 10)


# ================================================================ future-devices
@reg("hologram")
def _(s):
    s.F("ellipse", cx=256, cy=420, rx=150, ry=36, fill=DARK)
    s.F("ellipse", outline=False, cx=256, cy=416, rx=100, ry=20, fill=A1)
    s.F("polygon", points="170,410 342,410 380,120 132,120", fill=A1L, fill_opacity="0.45")
    s.F("path", d="M256 150 L330 192 V270 L256 312 L182 270 V192Z", fill=A1)
    s.M("M256 150 V230 M182 192 L256 230 L330 192", LIGHT, 8)


@reg("holographic-call")
def _(s):
    s.F("rect", x=170, y=390, width=172, height=60, rx=18, fill=DARK)
    s.F("polygon", points="196,390 316,390 410,100 102,100", fill=A1L, fill_opacity="0.5")
    s.F("circle", cx=256, cy=190, r=50, fill=SKIN)
    s.F("path", outline=False, d="M206 180 C206 130 256 130 256 130 C300 130 310 170 306 190 C290 176 240 160 206 180Z", fill=HAIR)
    s.F("path", d="M170 330 C170 260 342 260 342 330Z", fill=A1)
    dot(s, 236, 196, 6, DARK)
    dot(s, 276, 196, 6, DARK)
    s.M("M240 218 C252 228 262 228 272 218", DARK, 5)
    s.M("M120 120 H200", WHITE, 6)


@reg("ar-glasses")
def _(s):
    s.T("M60 230 L30 200 M452 230 L482 200", DARK, 18)
    s.F("rect", x=60, y=180, width=190, height=140, rx=50, fill=A1L, fill_opacity="0.7")
    s.F("rect", x=262, y=180, width=190, height=140, rx=50, fill=A1L, fill_opacity="0.7")
    s.M("M250 220 H262", DARK, 16)
    s.F("rect", outline=False, x=90, y=210, width=70, height=18, rx=9, fill=A2)
    s.F("rect", outline=False, x=90, y=240, width=40, height=14, rx=7, fill=LIGHT)
    s.F("circle", outline=False, cx=370, cy=250, r=24, fill=A2)
    s.T("M160 100 V140 M352 100 V140", A2, 8)


@reg("smart-glasses-future")
def _(s):
    s.T("M50 240 L20 210 M462 240 L492 210", DARK, 18)
    s.F("path", d="M60 190 H452 C470 190 478 210 476 240 C470 310 440 330 400 330 C350 330 320 270 290 270 H222 C192 270 162 330 112 330 C72 330 42 310 36 240 C34 210 42 190 60 190Z", fill=DARK)
    s.F("path", outline=False, d="M82 208 H240 C240 280 200 312 128 312 C98 312 76 290 70 250C66 226 70 208 82 208Z", fill=A1L)
    s.F("path", outline=False, d="M430 208 H272 C272 280 312 312 384 312 C414 312 436 290 442 250 C446 226 442 208 430 208Z", fill=A1L)
    s.F("circle", outline=False, cx=440, cy=210, r=10, fill=A2)
    s.F("rect", outline=False, x=110, y=230, width=70, height=12, rx=6, fill=WHITE, fill_opacity="0.8")


@reg("flexible-screen")
def _(s):
    s.F("path", d="M50 170 C150 100 260 240 330 150 C390 80 440 130 462 150 V310 C440 290 390 240 330 320 C260 410 150 270 50 340Z", fill=DARK)
    s.F("path", outline=False, d="M72 190 C160 128 262 262 332 174 C390 110 430 146 446 164 V294 C430 280 394 250 334 330 C262 420 156 286 72 330Z", fill=A1L)
    s.F("path", outline=False, d="M100 220 C140 190 180 230 220 240 C140 260 120 240 100 220Z", fill=A2)
    s.F("path", outline=False, d="M360 190 C390 170 420 190 430 210 C400 220 380 210 360 190Z", fill=LIGHT, fill_opacity="0.8")


@reg("rollable-phone")
def _(s):
    s.F("rect", x=60, y=130, width=392, height=252, rx=36, fill=DARK)
    s.F("rect", outline=False, x=80, y=150, width=290, height=212, rx=18, fill=A1L)
    s.F("rect", outline=False, x=96, y=170, width=100, height=70, rx=12, fill=A2)
    s.F("rect", outline=False, x=210, y=170, width=140, height=34, rx=10, fill=WHITE)
    s.F("rect", outline=False, x=210, y=216, width=140, height=24, rx=10, fill=A1)
    s.F("rect", x=380, y=150, width=50, height=212, rx=24, fill=MID)
    s.M("M392 190 H418 M392 256 H418 M392 322 H418", DARK, 8)


@reg("wearable-display")
def _(s):
    s.F("path", d="M70 180 C70 130 140 130 256 130 C372 130 442 130 442 180 V330 C442 380 372 380 256 380 C140 380 70 380 70 330Z", fill=A1D)
    s.F("path", outline=False, d="M96 190 C96 164 160 160 256 160 C352 160 416 164 416 190 V320 C416 346 352 350 256 350 C160 350 96 346 96 320Z", fill=A1L)
    s.M("M140 240 L190 220 L240 260 L300 200 L370 230", A2, 10)
    for x, y in ((190, 220), (300, 200)):
        s.F("circle", outline=False, cx=x, cy=y, r=10, fill=DARK)
    s.F("path", d="M40 190 H72 V320 H40Z", fill=MID)
    s.F("path", d="M440 190 H472 V320 H440Z", fill=MID)


@reg("invisibility-cloak")
def _(s):
    s.F("path", d="M256 50 C190 50 150 110 150 170 L90 440 C170 470 342 470 422 440 L362 170 C362 110 322 50 256 50Z", fill=A1, fill_opacity="0.55")
    s.raw(f'<path d="M256 50 C190 50 150 110 150 170 L90 440 C170 470 342 470 422 440 L362 170 C362 110 322 50 256 50Z" fill="none" stroke="{INK}" stroke-width="10" stroke-dasharray="22 16" stroke-linejoin="round" data-outline="stroke"/>')
    s.F("path", outline=False, d="M190 120 C210 90 250 84 270 90", fill="none", stroke=WHITE, stroke_width="16", stroke_linecap="round", stroke_opacity="0.7")
    s.F("polygon", points=star_pts(330, 230, 30, 12, 4), fill=A2L, fill_opacity="0.9")
    s.F("polygon", points=star_pts(200, 330, 22, 9, 4), fill=A2L, fill_opacity="0.9")


@reg("translator-earpiece")
def _(s):
    s.F("path", d="M60 60 H270 C290 60 300 74 300 90 V150 C300 166 290 180 270 180 H150 L100 220 V180 H60 C44 180 32 166 32 150 V90 C32 74 44 60 60 60Z", fill=A2)
    txt(s, "Hello", 166, 118, 190, 54, LIGHT)
    s.F("path", d="M450 250 H260 C240 250 230 264 230 280 V340 C230 356 240 370 260 370 H350 L412 410 V370 H450 C466 370 480 356 480 340 V280 C480 264 466 250 450 250Z", fill=A1)
    txt(s, "Hola", 355, 308, 190, 54, LIGHT)
    s.F("rect", x=60, y=360, width=80, height=100, rx=30, fill=LIGHT)
    s.F("circle", cx=100, cy=420, r=16, fill=A1)
    s.M("M170 410 C190 380 210 380 220 400", A2, 8)


# ================================================================ future-cities
def skyline(s, base=440):
    for x, w, h, c in ((40, 70, 180, A1), (120, 80, 270, A1D), (210, 90, 330, A1), (310, 80, 240, A1D), (400, 74, 200, A1)):
        s.F("rect", x=x, y=base - h, width=w, height=h, rx=8, fill=c)
        for yy in range(int(base - h + 20), int(base - 20), 36):
            s.F("rect", outline=False, x=x + 12, y=yy, width=w - 24, height=14, rx=5, fill=A1L, fill_opacity="0.8")


@reg("smart-city")
def _(s):
    skyline(s, 440)
    wifi(s, 256, 110, 90, A2, 14)
    s.F("rect", x=20, y=440, width=472, height=26, rx=10, fill=DARK)
    s.F("rect", x=220, y=388, width=70, height=36, rx=14, fill=A2)


@reg("vertical-farm")
def _(s):
    s.F("rect", x=100, y=50, width=312, height=400, rx=26, fill=A1L)
    s.F("rect", outline=False, x=118, y=66, width=276, height=60, rx=14, fill=WHITE, fill_opacity="0.4")
    for i in range(4):
        y = 130 + i * 80
        s.F("rect", x=120, y=y + 40, width=272, height=22, rx=8, fill=MID)
        for x in (160, 220, 280, 340):
            s.F("path", d=f"M{x} {y + 40} C{x - 22} {y} {x - 4} {y - 4} {x} {y + 16} C{x + 4} {y - 4} {x + 22} {y} {x} {y + 40}Z", fill=A2)
    s.F("rect", x=100, y=450, width=312, height=24, rx=10, fill=DARK)


@reg("vertical-forest-building")
def _(s):
    s.F("rect", x=140, y=50, width=232, height=410, rx=16, fill=LIGHT)
    for i in range(6):
        y = 70 + i * 66
        s.F("rect", outline=False, x=156, y=y + 24, width=200, height=34, rx=8, fill=A1L)
        s.F("rect", x=130 + (i % 2) * 90, y=y + 8, width=170, height=22, rx=10, fill=MID)
        for x in range(150 + (i % 2) * 90, 290 + (i % 2) * 90, 40):
            s.F("circle", cx=x + 10, cy=y - 2, r=22, fill=A1D if i % 2 else A1)
    s.F("rect", x=120, y=456, width=272, height=24, rx=10, fill=DARK)


@reg("floating-city")
def _(s):
    s.F("path", d="M70 330 H442 C430 410 350 440 256 480 C170 440 82 410 70 330Z", fill=MID)
    s.F("rect", x=70, y=310, width=372, height=34, rx=14, fill=A1D)
    for x, w, h, c in ((100, 60, 130, A1), (170, 70, 190, A2), (250, 80, 240, A1), (340, 70, 160, A1D)):
        s.F("rect", x=x, y=310 - h, width=w, height=h, rx=10, fill=c)
        for yy in range(int(310 - h + 16), 300, 32):
            s.F("rect", outline=False, x=x + 10, y=yy, width=w - 20, height=12, rx=5, fill=A1L)
    cloud(s, 90, 110, 0.35, LIGHT)
    cloud(s, 420, 90, 0.3, LIGHT)


@reg("underwater-city")
def _(s):
    s.F("path", d="M60 410 H452 V440 C452 456 440 464 424 464 H88 C72 464 60 456 60 440Z", fill=MID)
    s.F("path", d="M80 410 V330 C80 190 432 190 432 330 V410Z", fill=A1L, fill_opacity="0.75")
    for x, w, h in ((140, 50, 120), (210, 60, 170), (290, 50, 130)):
        s.F("rect", x=x, y=410 - h, width=w, height=h, rx=8, fill=A1 if w == 60 else A1D)
        s.F("rect", outline=False, x=x + 10, y=410 - h + 16, width=w - 20, height=12, rx=5, fill=A1L)
    s.F("circle", cx=380, cy=360, r=24, fill=LIGHT)
    for x, y, r in ((60, 160, 14), (100, 110, 10), (440, 140, 16), (400, 90, 10)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=WHITE, fill_opacity="0.8")


@reg("3d-printed-house")
def _(s):
    s.F("path", d="M80 440 V240 L256 110 L432 240 V440Z", fill=LIGHT)
    for y in range(250, 440, 24):
        s.M(f"M82 {y} H430", MID, 6)
    s.F("rect", x=210, y=320, width=92, height=120, rx=16, fill=A1)
    s.F("rect", x=100, y=280, width=70, height=60, rx=10, fill=A1L)
    s.F("rect", x=340, y=280, width=70, height=60, rx=10, fill=A1L)
    s.T("M40 70 H300 M300 70 V130", DARK, 14)
    s.F("rect", x=280, y=130, width=44, height=40, rx=10, fill=A2)
    s.F("polygon", points="294,170 310,170 302,190", fill=A2L)


@reg("solar-roads")
def _(s):
    s.F("polygon", points="200,60 312,60 500,460 12,460", fill=DARK)
    for i in range(5):
        y = 100 + i * 74
        k = (y - 60) / 400
        x0 = 200 - 188 * k + 18
        x1 = 312 + 188 * k - 18
        s.F("polygon", outline=False, points=f"{x0:.0f},{y} {x1:.0f},{y} {x1 + 8:.0f},{y + 54} {x0 - 8:.0f},{y + 54}", fill=A1, fill_opacity="0.85")
    s.M("M256 70 V460", A2, 8, dash="30 26")
    bolt(s, 256, 220, 0.3, A2)


@reg("smart-home-of-the-future")
def _(s):
    s.F("path", d="M60 440 V260 C60 180 200 120 256 90 C312 120 452 180 452 260 V440Z", fill=LIGHT)
    s.F("path", outline=False, d="M256 90 C312 120 452 180 452 260 V300 C400 220 330 170 256 140Z", fill=A1L)
    s.F("rect", x=100, y=280, width=130, height=100, rx=20, fill=A1L)
    s.F("rect", x=282, y=280, width=130, height=100, rx=20, fill=A1L)
    s.F("rect", x=216, y=360, width=80, height=80, rx=16, fill=A2)
    wifi(s, 256, 210, 70, A1, 12)
    s.F("rect", x=360, y=400, width=110, height=50, rx=14, fill=A1D)
    s.F("circle", outline=False, cx=380, cy=425, r=10, fill=A2L)


@reg("arcology")
def _(s):
    s.F("path", d="M40 450 L130 270 L190 270 L220 120 L292 120 L322 270 L382 270 L472 450Z", fill=A1)
    s.F("path", outline=False, d="M130 270 L190 270 L220 120 L256 120 L180 450 L40 450Z", fill=A1L, fill_opacity="0.5")
    for y in range(160, 440, 40):
        s.M(f"M{210 - (y - 120) * 0.12:.0f} {y} H{302 + (y - 120) * 0.12:.0f}", LIGHT, 8)
    for x, y in ((70, 400), (130, 330), (380, 330), (440, 400)):
        s.F("circle", cx=x, cy=y, r=22, fill=A2)
    s.F("circle", cx=256, cy=90, r=26, fill=A2)


# ================================================================ future-food-energy
@reg("lab-grown-meat")
def _(s):
    s.F("ellipse", cx=256, cy=420, rx=190, ry=50, fill="#E3F3FC")
    s.F("ellipse", cx=256, cy=400, rx=190, ry=50, fill="#E3F3FC")
    s.F("ellipse", outline=False, cx=256, cy=398, rx=150, ry=30, fill=A1L, fill_opacity="0.7")
    s.F("path", d="M110 330 C100 250 170 190 270 200 C370 210 420 280 390 340 C360 390 160 400 110 330Z", fill=A2)
    s.F("path", outline=False, d="M170 270 C200 240 260 230 300 250", fill="none", stroke=A2L, stroke_width="18", stroke_linecap="round")
    s.F("rect", x=300, y=60, width=90, height=50, rx=14, fill=LIGHT)
    s.M("M345 110 V160", MID, 8)


@reg("insect-protein")
def _(s):
    s.F("rect", x=70, y=250, width=372, height=170, rx=40, fill=A1)
    s.F("path", d="M160 250 C160 200 220 180 256 180 C292 180 352 200 352 250Z", fill=A2L)
    s.F("ellipse", cx=256, cy=190, rx=70, ry=34, fill=A2)
    s.F("circle", cx=256, cy=150, r=20, fill=A2)
    s.T("M246 140 L226 100 M266 140 L286 100", DARK, 6)
    for x in (130, 200, 300, 370):
        s.F("rect", outline=False, x=x - 24, y=300, width=48, height=84, rx=16, fill=A1L, fill_opacity="0.6")


@reg("food-printer")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=300, rx=30, fill=LIGHT)
    s.F("rect", outline=False, x=84, y=84, width=344, height=216, rx=16, fill=A1L, fill_opacity="0.6")
    s.F("rect", x=130, y=120, width=252, height=24, rx=8, fill=DARK)
    s.F("rect", x=232, y=130, width=48, height=62, rx=10, fill=A1)
    s.F("polygon", points="244,192 268,192 256,220", fill=A2)
    s.F("ellipse", cx=256, cy=280, rx=90, ry=22, fill=A2L)
    s.F("path", d="M190 280 C190 230 322 230 322 280Z", fill=A2)
    s.F("rect", x=40, y=360, width=432, height=44, rx=16, fill=A1D)


@reg("fusion-reactor")
def _(s):
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="150" fill="none" stroke="{INK}" stroke-width="86" data-outline="under"/>')
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="150" fill="none" stroke="{A1}" stroke-width="66"/>')
    s.raw(f'<ellipse cx="256" cy="256" rx="200" ry="150" fill="none" stroke="{A1L}" stroke-width="14" stroke-dasharray="26 22"/>')
    s.F("circle", cx=256, cy=256, r=70, fill=A2)
    s.F("circle", outline=False, cx=256, cy=256, r=40, fill=A2L)
    s.F("circle", outline=False, cx=256, cy=256, r=16, fill=LIGHT)


@reg("space-based-solar-power")
def _(s):
    s.F("circle", cx=430, cy=100, r=54, fill=A2L)
    s.F("circle", outline=False, cx=430, cy=100, r=30, fill=A2)
    s.F("rect", x=100, y=130, width=140, height=70, rx=8, fill=A1)
    s.F("rect", x=250, y=130, width=140, height=70, rx=8, fill=A1)
    s.F("rect", x=226, y=110, width=60, height=110, rx=14, fill=LIGHT)
    s.F("polygon", points="256,220 190,440 322,440", fill=A2L, fill_opacity="0.5")
    s.F("rect", x=130, y=440, width=252, height=36, rx=12, fill=A1D)


@reg("carbon-capture-machine")
def _(s):
    s.F("rect", x=130, y=140, width=252, height=300, rx=26, fill=A1)
    s.F("rect", outline=False, x=150, y=160, width=212, height=60, rx=16, fill=A1L, fill_opacity="0.5")
    s.F("circle", cx=256, cy=320, r=76, fill=DARK)
    s.open("part-wheel", "256 320")
    for a in range(0, 360, 60):
        x, y = arc_pt(256, 320, 52, a)
        s.F("path", outline=False, d=f"M256 320 L{x:.0f} {y:.0f}", fill="none", stroke=A1L, stroke_width="16", stroke_linecap="round")
    s.close()
    s.F("circle", cx=256, cy=320, r=14, fill=A2)
    s.F("rect", x=206, y=60, width=100, height=90, rx=14, fill=MID)
    arrow(s, 90, 330, 130, 330, A2, 10, 26)
    s.F("circle", cx=90, cy=260, r=30, fill=MID, fill_opacity="0.8")
    s.F("circle", cx=60, cy=300, r=20, fill=MID, fill_opacity="0.8")


@reg("quantum-computer")
def _(s):
    s.F("rect", x=190, y=40, width=132, height=40, rx=16, fill=A1D)
    s.T("M256 80 V150", A2, 14)
    s.F("rect", x=170, y=150, width=172, height=30, rx=12, fill=A1)
    s.T("M256 180 V230", A2, 14)
    s.F("rect", x=150, y=230, width=212, height=30, rx=12, fill=A1)
    s.T("M256 260 V310", A2, 14)
    s.F("rect", x=130, y=310, width=252, height=30, rx=12, fill=A1)
    s.F("circle", cx=256, cy=395, r=50, fill=DARK)
    s.F("circle", outline=False, cx=256, cy=395, r=22, fill=A1L)
    s.M("M160 440 H350", MID, 10)
    for x in (140, 372):
        s.T(f"M{x} 140 C{x} 240 {x} 300 {x} 380", MID, 8)


@reg("quantum-chip")
def _(s):
    s.F("rect", x=110, y=110, width=292, height=292, rx=36, fill=DARK)
    for i in range(5):
        s.F("rect", outline=False, x=136 + i * 56, y=76, width=24, height=36, rx=6, fill=MID)
        s.F("rect", outline=False, x=136 + i * 56, y=402, width=24, height=36, rx=6, fill=MID)
        s.F("rect", outline=False, x=76, y=136 + i * 56, width=36, height=24, rx=6, fill=MID)
        s.F("rect", outline=False, x=402, y=136 + i * 56, width=36, height=24, rx=6, fill=MID)
    s.raw(f'<ellipse cx="256" cy="256" rx="96" ry="34" fill="none" stroke="{A1L}" stroke-width="8"/>')
    s.raw(f'<ellipse cx="256" cy="256" rx="96" ry="34" fill="none" stroke="{A1L}" stroke-width="8" transform="rotate(60 256 256)"/>')
    s.raw(f'<ellipse cx="256" cy="256" rx="96" ry="34" fill="none" stroke="{A1L}" stroke-width="8" transform="rotate(120 256 256)"/>')
    s.F("circle", cx=256, cy=256, r=24, fill=A2)


@reg("delivery-drone")
def _(s):
    s.T("M256 190 L110 120 M256 190 L402 120", DARK, 12)
    for x in (100, 412):
        s.F("ellipse", cx=x, cy=112, rx=64, ry=14, fill=MID)
    s.F("rect", x=190, y=160, width=132, height=70, rx=30, fill=A1)
    s.F("circle", outline=False, cx=256, cy=196, r=12, fill=A2)
    s.T("M226 230 V280 M286 230 V280", DARK, 6)
    s.F("rect", x=180, y=280, width=152, height=130, rx=14, fill=A2)
    s.M("M180 336 H332 M256 280 V410", A2L, 10)
    s.F("rect", outline=False, x=196, y=296, width=26, height=14, rx=6, fill=A2L)


# ================================================================ science-fiction
@reg("time-machine")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=A1)
    s.F("circle", cx=256, cy=256, r=140, fill=LIGHT)
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(256, 256, 112, a)
        x2, y2 = arc_pt(256, 256, 130, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DARK, 8)
    s.open("part-hand-minute", "256 256")
    s.M("M256 256 V150", DARK, 14)
    s.close()
    s.open("part-hand-hour", "256 256")
    s.M("M256 256 L320 290", DARK, 14)
    s.close()
    s.F("circle", cx=256, cy=256, r=16, fill=A2)
    s.raw(f'<path d="M256 36 A220 220 0 0 1 476 256" fill="none" stroke="{A2}" stroke-width="18" stroke-linecap="round"/>')
    s.F("polygon", points="476,256 440,232 500,224", fill=A2)


@reg("teleporter")
def _(s):
    s.F("ellipse", cx=256, cy=420, rx=150, ry=40, fill=A1D)
    s.F("ellipse", outline=False, cx=256, cy=416, rx=110, ry=26, fill=A1L)
    s.F("polygon", points="130,410 382,410 340,80 172,80", fill=A1L, fill_opacity="0.5")
    for x, h in ((190, 200), (240, 260), (290, 220), (330, 160)):
        s.F("rect", outline=False, x=x - 10, y=410 - h, width=20, height=h, rx=10, fill=WHITE, fill_opacity="0.7")
    for x, y in ((180, 120), (330, 150), (250, 90), (300, 70)):
        s.F("polygon", points=star_pts(x, y, 14, 6, 4), fill=A2)
    s.F("ellipse", cx=256, cy=80, rx=84, ry=20, fill=A1D)


@reg("warp-drive")
def _(s):
    s.F("path", d="M240 190 C300 170 380 200 420 256 C380 312 300 342 240 322 L160 322 L110 256 L160 190Z", fill=LIGHT)
    s.F("circle", cx=330, cy=256, r=30, fill=A1L)
    s.F("path", d="M110 256 L40 190 V322Z", fill=A2)
    for i, y in enumerate((100, 150, 360, 410)):
        s.M(f"M{80 - i * 6} {y} H{250 + (i % 2) * 40}", A1, 10)
    for r in (150, 195):
        x0, y0 = arc_pt(440, 256, r, 150)
        x1, y1 = arc_pt(440, 256, r, 210)
        s.raw(f'<path d="M{x0:.0f} {y0:.0f} A{r} {r} 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="{A2}" stroke-width="14" stroke-linecap="round" transform="translate(30 0)"/>')


@reg("force-field")
def _(s):
    s.F("path", d="M60 440 V260 C60 130 150 70 256 70 C362 70 452 130 452 260 V440Z", fill=A1L, fill_opacity="0.55")
    s.raw(f'<path d="M60 440 V260 C60 130 150 70 256 70 C362 70 452 130 452 260 V440" fill="none" stroke="{A1}" stroke-width="14" stroke-linecap="round"/>')
    for x, y in ((256, 130), (150, 190), (362, 190), (256, 250), (110, 300), (402, 300)):
        s.F("polygon", points=f"{x},{y - 28} {x + 24},{y - 14} {x + 24},{y + 14} {x},{y + 28} {x - 24},{y + 14} {x - 24},{y - 14}", fill=A1, fill_opacity="0.6")
    s.F("rect", x=190, y=400, width=132, height=60, rx=20, fill=A1D)
    s.F("circle", cx=256, cy=430, r=14, fill=A2)
    s.F("polygon", points=star_pts(256, 90, 24, 10, 4), fill=A2)


@reg("laser-sword")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    s.F("rect", x=60, y=230, width=170, height=52, rx=20, fill=A1)
    s.F("rect", x=170, y=212, width=24, height=88, rx=8, fill=MID)
    s.F("rect", x=210, y=232, width=30, height=48, rx=8, fill=DARK)
    s.F("rect", x=240, y=236, width=240, height=40, rx=20, fill=A2L)
    s.F("rect", outline=False, x=250, y=246, width=216, height=14, rx=7, fill=WHITE)
    s.close()


@reg("ray-gun")
def _(s):
    s.F("path", d="M80 200 C80 160 200 150 330 160 L420 170 V260 L330 270 C300 280 290 300 280 330 L270 400 H190 L200 300 C160 300 80 290 80 200Z", fill=A1)
    s.F("rect", outline=False, x=110, y=185, width=170, height=18, rx=9, fill=A1L, fill_opacity="0.6")
    s.F("rect", x=420, y=190, width=60, height=60, rx=18, fill=MID)
    s.F("circle", cx=150, cy=230, r=24, fill=A2)
    s.F("polygon", points=star_pts(486, 220, 24, 10, 6), fill=A2L)
    s.M("M284 330 C330 340 340 310 320 292", DARK, 10)


@reg("cryogenic-sleep-pod")
def _(s):
    s.F("path", d="M60 300 C60 200 140 150 256 150 C372 150 452 200 452 300 V390 C452 410 440 420 420 420 H92 C72 420 60 410 60 390Z", fill=A1)
    s.F("path", outline=False, d="M90 300 C90 220 150 180 256 180 C362 180 422 220 422 300 Z", fill=A1L, fill_opacity="0.8")
    s.F("path", d="M150 300 C150 262 190 260 256 260 C322 260 362 262 362 300Z", fill=LIGHT)
    s.F("circle", cx=190, cy=252, r=28, fill=SKIN)
    s.M("M120 210 C150 195 170 195 190 200", WHITE, 8)
    s.F("rect", x=60, y=420, width=392, height=30, rx=12, fill=DARK)
    for x, y in ((380, 120), (420, 170), (110, 130)):
        s.F("polygon", points=star_pts(x, y, 22, 9, 6), fill=A1L)


@reg("shrink-ray")
def _(s):
    s.F("path", d="M60 240 C60 200 130 190 230 200 L330 210 V300 L230 310 C130 320 60 290 60 240Z", fill=A2)
    s.F("circle", cx=330, cy=256, r=46, fill=DARK)
    s.F("circle", outline=False, cx=330, cy=256, r=20, fill=A1L)
    s.F("rect", x=140, y=300, width=60, height=120, rx=16, fill=A1D)
    s.F("polygon", points="390,150 480,256 390,362", fill=A1L, fill_opacity="0.5")
    s.F("rect", x=400, y=226, width=24, height=60, rx=8, fill=A1)
    s.F("rect", x=440, y=240, width=12, height=30, rx=4, fill=A1)


@reg("parallel-universe")
def _(s):
    s.F("circle", cx=190, cy=256, r=150, fill=A1)
    s.F("circle", cx=322, cy=256, r=150, fill=A2, fill_opacity="0.9")
    s.F("path", outline=False, d="M256 128 A150 150 0 0 1 256 384 A150 150 0 0 1 256 128Z", fill=LIGHT, fill_opacity="0.5")
    for x, y in ((130, 200), (250, 300), (380, 180), (350, 330)):
        s.F("polygon", points=star_pts(x, y, 20, 8, 4), fill=LIGHT)
    s.M("M256 130 V382", DARK, 6, dash="10 12")


@reg("alien-contact-future")
def _(s):
    s.F("ellipse", cx=256, cy=190, rx=190, ry=56, fill=MID)
    s.F("path", d="M150 180 C150 100 362 100 362 180Z", fill=A1L)
    for x in (130, 256, 382):
        dot(s, x, 200, 12, A2)
    s.F("polygon", points="170,230 342,230 420,450 92,450", fill=A2L, fill_opacity="0.5")
    s.F("path", d="M256 340 C216 340 200 380 210 410 C220 440 292 440 302 410 C312 380 296 340 256 340Z", fill=A1)
    dot(s, 236, 380, 12, DARK)
    dot(s, 276, 380, 12, DARK)
    s.T("M236 340 L220 308 M276 340 L292 308", A1, 8)


if __name__ == "__main__":
    run("future-tech", D, sys.argv[1:] or None)
