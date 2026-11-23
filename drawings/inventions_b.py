"""inventions-discoveries, part B: recent inventions, discoveries, invention ideas (themed colours).
Run: python drawings/inventions_b.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tech import (A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, INK, SKIN, HAIR, WHITE, arc_pt, arrow, bolt, cloud, dot, lock, registry, ring, run, screen, shine, star_pts, txt, waves, wifi)  # noqa: E402

D, reg = registry()


def globe(s, cx, cy, r):
    s.F("circle", cx=cx, cy=cy, r=r, fill=A1)
    s.F("path", outline=False, d=f"M{cx - r * 0.55} {cy - r * 0.5} C{cx - r * 0.2} {cy - r * 0.8} {cx + r * 0.1} {cy - r * 0.5} {cx} {cy - r * 0.2} C{cx - r * 0.1} {cy} {cx - r * 0.5} {cy + r * 0.1} {cx - r * 0.6} {cy - r * 0.2}Z", fill=A1L)
    s.F("path", outline=False, d=f"M{cx + r * 0.2} {cy + r * 0.1} C{cx + r * 0.6} {cy} {cx + r * 0.7} {cy + r * 0.4} {cx + r * 0.3} {cy + r * 0.7} C{cx + r * 0.1} {cy + r * 0.5} {cx + r * 0.1} {cy + r * 0.3} {cx + r * 0.2} {cy + r * 0.1}Z", fill=A1L)


def chip_pins(s, x0, y0, x1, y1, n=5):
    for i in range(n):
        t = (i + 0.5) / n
        s.F("rect", x=x0 + (x1 - x0) * t - 12, y=y0 - 46, width=24, height=48, rx=8, fill=MID)
        s.F("rect", x=x0 + (x1 - x0) * t - 12, y=y1 - 2, width=24, height=48, rx=8, fill=MID)
        s.F("rect", x=x0 - 46, y=y0 + (y1 - y0) * t - 12, width=48, height=24, rx=8, fill=MID)
        s.F("rect", x=x1 - 2, y=y0 + (y1 - y0) * t - 12, width=48, height=24, rx=8, fill=MID)


# ================================================================ recent-inventions
@reg("transistor")
def _(s):
    s.F("path", d="M150 70 H362 V260 C362 300 330 320 256 320 C182 320 150 300 150 260Z", fill=DARK)
    s.F("path", outline=False, d="M170 90 H220 V280 C190 276 170 268 170 250Z", fill=MID, fill_opacity="0.45")
    for x in (190, 256, 322):
        s.T(f"M{x} 320 V450", MID, 16)
    s.F("rect", outline=False, x=210, y=130, width=92, height=40, rx=12, fill=A2L)
    txt(s, "NPN", 256, 150, 70, 26, DARK)


@reg("microchip")
def _(s):
    s.F("rect", x=110, y=110, width=292, height=292, rx=36, fill=A1)
    chip_pins(s, 136, 136, 376, 376)
    s.F("rect", outline=False, x=160, y=160, width=192, height=192, rx=24, fill=A1D)
    s.F("circle", outline=False, cx=256, cy=256, r=50, fill=A1L)
    dot(s, 256, 256, 18, A2)


@reg("satellite-invention")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    for x in (40, 350):
        s.F("rect", x=x, y=200, width=122, height=112, rx=8, fill=A1)
        s.M(f"M{x + 40} 200 V312 M{x + 80} 200 V312 M{x} 256 H{x + 122}", A1L, 5)
    s.T("M162 256 H190 M350 256 H322", DARK, 12)
    s.F("rect", x=190, y=206, width=132, height=100, rx=20, fill=LIGHT)
    s.F("rect", outline=False, x=208, y=224, width=96, height=28, rx=10, fill=A1L)
    s.close()
    s.T("M256 160 V100", DARK, 8)
    s.F("circle", cx=256, cy=90, r=20, fill=A2)
    waves(s, 256, 90, 70, A2, 10, 2, 200, 340)


@reg("laser-invention")
def _(s):
    s.F("rect", x=40, y=210, width=140, height=92, rx=20, fill=DARK)
    s.F("rect", outline=False, x=56, y=224, width=70, height=18, rx=8, fill=MID)
    s.F("circle", cx=190, cy=256, r=26, fill=A2)
    s.T("M200 256 H472", A2, 18)
    s.M("M200 256 H472", LIGHT, 6)
    s.F("polygon", points=star_pts(440, 256, 30, 12, 8), fill=A2L)


@reg("personal-computer")
def _(s):
    s.F("rect", x=100, y=50, width=312, height=250, rx=26, fill=LIGHT)
    s.F("rect", outline=False, x=128, y=78, width=256, height=190, rx=14, fill=DARK)
    s.M("M150 110 L190 130 L150 150", A2L, 10)
    s.M("M210 160 H280", LIGHT, 10)
    s.F("rect", x=80, y=300, width=352, height=40, rx=12, fill=MID)
    s.F("rect", x=60, y=360, width=392, height=90, rx=20, fill=LIGHT)
    for r in range(2):
        for c in range(10):
            s.F("rect", outline=False, x=84 + c * 36, y=376 + r * 32, width=28, height=22, rx=6, fill=MID)
    s.F("rect", outline=False, x=360, y=316, width=50, height=10, rx=5, fill=A2)


@reg("mobile-phone-invention")
def _(s):
    s.T("M330 80 L330 30", DARK, 18)
    s.F("rect", x=170, y=70, width=190, height=390, rx=36, fill=DARK)
    s.F("rect", outline=False, x=194, y=100, width=142, height=70, rx=10, fill=A1L)
    for r in range(4):
        for c in range(3):
            s.F("rect", outline=False, x=196 + c * 46, y=196 + r * 56, width=36, height=42, rx=12, fill=MID if (r + c) % 2 else LIGHT)
    s.F("rect", x=280, y=60, width=62, height=20, rx=10, fill=A2)


@reg("internet-invention")
def _(s):
    globe(s, 256, 256, 120)
    pts = [(80, 120), (432, 110), (70, 400), (440, 390), (256, 50), (256, 465)]
    for x, y in pts:
        s.T(f"M256 256 L{x} {y}", MID, 8)
    for x, y in pts:
        s.F("rect", x=x - 34, y=y - 26, width=68, height=52, rx=12, fill=A2)
        s.F("rect", outline=False, x=x - 22, y=y - 15, width=44, height=26, rx=6, fill=A2L)


@reg("email-invention")
def _(s):
    s.F("rect", x=50, y=130, width=412, height=270, rx=34, fill=LIGHT)
    s.M("M70 160 L256 300 L442 160", MID, 14)
    s.F("circle", cx=380, cy=360, r=70, fill=A2)
    txt(s, "@", 380, 360, 80, 80, LIGHT)


@reg("gps-invention")
def _(s):
    s.F("path", d="M256 40 C170 40 110 100 110 180 C110 280 256 420 256 420 C256 420 402 280 402 180 C402 100 342 40 256 40Z", fill=A2)
    s.F("circle", cx=256, cy=180, r=56, fill=LIGHT)
    dot(s, 256, 180, 20, A2)
    s.F("ellipse", outline=False, cx=256, cy=456, rx=100, ry=20, fill=DARK, fill_opacity="0.2")
    s.M("M60 100 L90 70 M60 70 L90 100", A1, 10)
    waves(s, 60, 60, 70, A1, 10, 2, 20, 70)


@reg("smartphone-invention")
def _(s):
    s.F("rect", x=150, y=40, width=212, height=432, rx=44, fill=DARK)
    s.F("rect", outline=False, x=168, y=76, width=176, height=360, rx=20, fill=A1L)
    for r in range(3):
        for c in range(3):
            s.F("rect", outline=False, x=186 + c * 52, y=100 + r * 54, width=40, height=40, rx=12, fill=A2 if (r + c) % 3 == 0 else WHITE)
    s.F("rect", outline=False, x=184, y=360, width=144, height=50, rx=18, fill=A1)
    s.F("rect", outline=False, x=224, y=54, width=64, height=12, rx=6, fill=MID)


@reg("touchscreen")
def _(s):
    screen(s, 40, 70, 360, 290, DARK, A1L, 36, 18)
    s.F("rect", outline=False, x=70, y=100, width=120, height=90, rx=12, fill=A2)
    s.F("rect", outline=False, x=210, y=100, width=160, height=40, rx=10, fill=WHITE)
    s.F("rect", outline=False, x=210, y=150, width=160, height=40, rx=10, fill=A1)
    s.F("path", d="M360 450 C340 400 330 330 330 290 V210 C330 190 360 190 360 210 V290 H380 V240 C380 220 410 220 410 240 V290 H430 V260 C430 240 460 240 460 260 V330 C460 400 440 430 430 450Z", fill=SKIN)
    s.raw(f'<circle cx="345" cy="210" r="40" fill="none" stroke="{A2}" stroke-width="10" stroke-dasharray="14 10"/>')


@reg("3d-printer")
def _(s):
    s.F("rect", x=70, y=40, width=372, height=400, rx=30, fill=LIGHT)
    s.F("rect", outline=False, x=96, y=70, width=320, height=300, rx=14, fill=A1L, fill_opacity="0.5")
    s.F("rect", x=96, y=130, width=320, height=24, rx=8, fill=DARK)
    s.F("rect", x=226, y=140, width=60, height=60, rx=10, fill=A1)
    s.F("polygon", points="242,200 270,200 256,230", fill=A2)
    s.F("path", d="M190 350 L256 250 L322 350Z", fill=A2)
    s.F("path", outline=False, d="M206 340 L256 262 L276 290 L226 340Z", fill=A2L)
    s.F("rect", x=96, y=366, width=320, height=26, rx=8, fill=DARK)


@reg("lithium-ion-battery")
def _(s):
    s.F("rect", x=210, y=30, width=92, height=60, rx=14, fill=MID)
    s.F("rect", x=150, y=80, width=212, height=390, rx=36, fill=A1)
    s.F("rect", outline=False, x=170, y=100, width=30, height=350, rx=14, fill=WHITE, fill_opacity="0.25")
    s.F("rect", outline=False, x=170, y=330, width=172, height=100, rx=14, fill=A1D)
    bolt(s, 270, 230, 0.35, A2)
    txt(s, "Li", 256, 380, 80, 50, A2L)


@reg("solar-cell")
def _(s):
    s.F("polygon", points="110,160 430,160 470,400 70,400", fill=A1D)
    for i in range(1, 4):
        s.M(f"M{110 - i * 10 + (0)} {160 + i * 60} H{430 + i * 10}", A1L, 8)
    for i in range(1, 5):
        s.M(f"M{110 + i * 64 - i * 8} 160 L{70 + i * 80} 400", A1L, 8)
    s.F("circle", cx=400, cy=80, r=48, fill=A2)
    for a in range(0, 360, 45):
        x1, y1 = arc_pt(400, 80, 62, a)
        x2, y2 = arc_pt(400, 80, 86, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", A2, 10)


@reg("artificial-heart")
def _(s):
    s.F("path", d="M256 450 C60 320 50 200 70 160 C100 80 200 70 256 160 C312 70 412 80 442 160 C462 200 452 320 256 450Z", fill=A2)
    s.F("path", outline=False, d="M120 160 C140 120 190 116 220 170", fill="none", stroke=A2L, stroke_width="22", stroke_linecap="round")
    s.F("rect", x=180, y=230, width=152, height=100, rx=20, fill=MID)
    s.M("M200 280 H236 L252 250 L272 310 L290 280 H312", A1, 10)
    s.T("M200 90 V40 M312 90 V40", MID, 18)


@reg("mri-invention")
def _(s):
    s.F("path", d="M60 440 V230 C60 90 452 90 452 230 V440Z", fill=LIGHT)
    s.F("circle", cx=256, cy=270, r=110, fill=A1D)
    s.F("circle", cx=256, cy=270, r=76, fill=DARK)
    s.F("rect", x=70, y=320, width=372, height=44, rx=16, fill=A1L)
    s.F("rect", x=40, y=440, width=432, height=30, rx=10, fill=MID)


@reg("barcode")
def _(s):
    s.F("rect", x=40, y=100, width=432, height=312, rx=30, fill=LIGHT)
    xs = (80, 106, 128, 156, 178, 214, 242, 268, 300, 322, 350, 378, 404)
    ws = (12, 6, 16, 8, 22, 8, 14, 6, 16, 8, 14, 10, 18)
    for x, w in zip(xs, ws):
        s.F("rect", outline=False, x=x, y=140, width=w, height=180, fill=DARK)
    s.M("M70 372 H440", MID, 12)
    s.M("M60 256 H452", A2, 8)


@reg("qr-code-invention")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=36, fill=LIGHT)
    for x, y in ((90, 90), (320, 90), (90, 320)):
        s.F("rect", outline=False, x=x, y=y, width=102, height=102, rx=14, fill=DARK)
        s.F("rect", outline=False, x=x + 20, y=y + 20, width=62, height=62, rx=8, fill=LIGHT)
        s.F("rect", outline=False, x=x + 34, y=y + 34, width=34, height=34, rx=6, fill=DARK)
    import random
    rnd = random.Random(11)
    for r in range(8):
        for c in range(8):
            x, y = 214 + c * 26, 214 + r * 26
            if x + 22 <= 440 and y + 22 <= 440 and rnd.random() < 0.5:
                s.F("rect", outline=False, x=x, y=y, width=22, height=22, rx=4, fill=DARK)
    for r in range(3):
        for c in range(3):
            if rnd.random() < 0.6:
                s.F("rect", outline=False, x=214 + c * 26, y=90 + r * 26, width=22, height=22, rx=4, fill=A1)


@reg("microwave-oven-invention")
def _(s):
    s.F("rect", x=40, y=130, width=432, height=290, rx=36, fill=LIGHT)
    s.F("rect", x=70, y=160, width=270, height=230, rx=20, fill=DARK)
    s.F("rect", outline=False, x=86, y=176, width=238, height=198, rx=12, fill=A1L)
    s.F("ellipse", outline=False, cx=205, cy=330, rx=70, ry=16, fill=A2L)
    s.F("path", outline=False, d="M150 330 C150 290 260 290 260 330Z", fill=A2)
    s.F("circle", cx=406, cy=210, r=30, fill=A1)
    for y in (280, 320, 360):
        s.F("rect", outline=False, x=382, y=y, width=48, height=20, rx=8, fill=MID)


@reg("digital-camera")
def _(s):
    s.F("path", d="M60 170 H170 L196 120 H316 L342 170 H452 C474 170 484 180 484 200 V380 C484 400 474 410 452 410 H60 C38 410 28 400 28 380 V200 C28 180 38 170 60 170Z", fill=A1)
    s.F("circle", cx=256, cy=290, r=100, fill=MID)
    s.F("circle", cx=256, cy=290, r=70, fill=DARK)
    s.F("circle", cx=256, cy=290, r=44, fill=A1L)
    s.F("circle", outline=False, cx=238, cy=272, r=14, fill=WHITE, fill_opacity="0.8")
    s.F("rect", x=70, y=134, width=60, height=30, rx=8, fill=A2)
    s.F("rect", outline=False, x=400, y=200, width=60, height=40, rx=10, fill=A1L)


@reg("usb-drive-invention")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    s.F("rect", x=60, y=210, width=130, height=92, rx=10, fill=MID)
    s.F("rect", outline=False, x=86, y=236, width=22, height=14, rx=3, fill=DARK)
    s.F("rect", outline=False, x=118, y=236, width=22, height=14, rx=3, fill=DARK)
    s.F("rect", x=190, y=190, width=270, height=132, rx=44, fill=A1)
    s.F("circle", cx=400, cy=256, r=24, fill=A1L)
    s.F("rect", outline=False, x=214, y=206, width=130, height=20, rx=10, fill=A1L, fill_opacity="0.6")
    s.close()


@reg("wi-fi-invention")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=A1)
    for r in (70, 120, 170):
        x0, y0 = arc_pt(256, 360, r, -135)
        x1, y1 = arc_pt(256, 360, r, -45)
        s.raw(f'<path d="M{x0:.0f} {y0:.0f} A{r} {r} 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="{LIGHT}" stroke-width="26" stroke-linecap="round"/>')
    s.F("circle", outline=False, cx=256, cy=360, r=20, fill=LIGHT)


# ================================================================ discoveries
@reg("discovery-of-gravity")
def _(s):
    s.F("circle", cx=256, cy=420, r=240, fill=A1L)
    s.F("circle", cx=256, cy=420, r=240, fill=A1L)
    s.F("path", d="M256 190 C200 190 190 130 220 112 C236 104 250 112 256 124 C262 112 276 104 292 112 C322 130 312 190 256 190Z", fill=A2)
    s.T("M256 110 C256 90 262 82 272 78", DARK, 8)
    arrow(s, 256, 214, 256, 330, A2, 16, 38)
    s.M("M170 150 L120 110 M342 150 L392 110", MID, 8)


@reg("discovery-of-electricity")
def _(s):
    bolt(s, 256, 256, 1.2, A2)
    s.M("M90 120 L120 100 M410 420 L440 400 M80 400 L110 420", A1, 12)


@reg("penicillin")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=LIGHT)
    s.F("circle", outline=False, cx=256, cy=256, r=170, fill=A1L, fill_opacity="0.6")
    s.F("circle", outline=False, cx=256, cy=256, r=70, fill=WHITE)
    s.F("circle", cx=256, cy=256, r=40, fill=A2)
    for x, y in ((130, 160), (390, 150), (380, 370), (140, 370), (256, 110), (256, 410)):
        s.F("circle", outline=False, cx=x, cy=y, r=16, fill=A1D)
    for a in range(0, 360, 60):
        x, y = arc_pt(256, 256, 40, a)
        x2, y2 = arc_pt(256, 256, 62, a)
        s.M(f"M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}", A2, 8)


@reg("discovery-of-dna")
def _(s):
    def strand(sign):
        pts = []
        for i in range(0, 101):
            y = 50 + i * 4.1
            x = 256 + sign * 92 * math.sin(i / 100 * 3 * 2 * math.pi)
            pts.append(f"{x:.1f} {y:.1f}")
        return "M" + " L".join(pts)
    for k in range(13):
        y = 50 + k * 34.2
        x = 92 * math.sin((y - 50) / 410 * 3 * 2 * math.pi)
        s.M(f"M{256 - x:.0f} {y:.0f} H{256 + x:.0f}", A2L if k % 2 else LIGHT, 10)
    s.T(strand(1), A1, 22)
    s.T(strand(-1), A2, 22)


@reg("discovery-of-x-rays")
def _(s):
    s.F("rect", x=70, y=50, width=372, height=412, rx=26, fill=DARK)
    for i in range(4):
        s.T(f"M{180 + i * 40} 400 V190", LIGHT, 22)
    s.T("M170 190 C150 130 230 130 250 160 M250 160 C270 120 340 130 320 190", LIGHT, 22)
    s.T("M150 280 C110 250 130 200 160 200", LIGHT, 18)
    s.T("M200 410 H340", LIGHT, 26)
    s.F("polygon", points=star_pts(400, 90, 26, 10, 4), fill=A2L)


@reg("discovery-of-the-atom")
def _(s):
    for rot in (0, 60, 120):
        s.raw(f'<ellipse cx="256" cy="256" rx="190" ry="64" fill="none" stroke="{MID}" stroke-width="8" transform="rotate({rot} 256 256)"/>')
    s.F("circle", cx=256, cy=256, r=52, fill=A2)
    s.F("circle", outline=False, cx=240, cy=240, r=16, fill=A2L)
    for a in (0, 120, 240):
        x, y = arc_pt(256, 256, 190, a)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=20, fill=A1)


@reg("discovery-of-radioactivity")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=A2L)
    for a in (-90, 30, 150):
        x0, y0 = arc_pt(256, 256, 40, a - 30)
        x1, y1 = arc_pt(256, 256, 40, a + 30)
        xa, ya = arc_pt(256, 256, 170, a - 30)
        xb, yb = arc_pt(256, 256, 170, a + 30)
        s.F("path", d=f"M{x0:.0f} {y0:.0f} L{xa:.0f} {ya:.0f} A170 170 0 0 1 {xb:.0f} {yb:.0f} L{x1:.0f} {y1:.0f}Z", fill=DARK)
    s.F("circle", cx=256, cy=256, r=34, fill=DARK)


@reg("discovery-of-oxygen")
def _(s):
    s.F("path", d="M210 50 H302 V190 L410 400 C424 436 404 466 368 466 H144 C108 466 88 436 102 400 L210 190Z", fill="#E3F3FC")
    s.F("path", outline=False, d="M156 320 H356 L402 410 C410 436 396 456 366 456 H146 C116 456 102 436 110 410Z", fill=A1L)
    s.F("circle", cx=256, cy=380, r=54, fill=LIGHT)
    txt(s, "O₂", 256, 382, 70, 44, A1D)
    for x, y, r in ((200, 270, 12), (310, 250, 10), (270, 200, 8)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=A1, fill_opacity="0.8")


@reg("germ-theory")
def _(s):
    s.F("circle", cx=230, cy=240, r=170, fill=A1L)
    s.raw(f'<circle cx="230" cy="240" r="170" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    for x, y, r in ((170, 180, 28), (280, 160, 22), (250, 290, 34), (160, 310, 20), (330, 260, 18)):
        s.F("circle", cx=x, cy=y, r=r, fill=A2)
        for a in range(0, 360, 60):
            x1, y1 = arc_pt(x, y, r, a)
            x2, y2 = arc_pt(x, y, r * 1.5, a)
            s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", A2, 6)
    s.T("M350 360 L450 460", DARK, 36)


@reg("blood-circulation-discovery")
def _(s):
    s.F("path", d="M256 340 C150 270 140 210 154 180 C176 130 236 130 256 190 C276 130 336 130 358 180 C372 210 362 270 256 340Z", fill=A2)
    s.raw(f'<path d="M110 250 C60 400 160 470 256 470 C352 470 452 400 402 250" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M110 250 C60 400 160 470 256 470 C352 470 452 400 402 250" fill="none" stroke="{A1}" stroke-width="20" stroke-linecap="round"/>')
    s.F("polygon", points="402,250 380,290 424,290", fill=A1)
    s.F("polygon", points="110,250 132,210 88,210", fill=A1)
    s.T("M256 190 V80 M256 80 C300 60 380 60 380 110", A2, 16)


@reg("vaccination-discovery")
def _(s):
    s.open(transform="rotate(-40 256 256)")
    s.F("rect", x=130, y=210, width=230, height=92, rx=12, fill="#E3F3FC")
    s.F("rect", outline=False, x=140, y=220, width=130, height=72, fill=A1L)
    s.F("rect", x=360, y=236, width=40, height=40, fill=MID)
    s.T("M400 256 H490", MID, 6)
    s.F("rect", x=70, y=196, width=60, height=120, rx=8, fill=MID)
    s.T("M30 256 H70", MID, 16)
    s.close()
    s.F("path", d="M390 330 C420 330 450 350 450 380 V450 H370 V380 C370 350 360 330 390 330Z", fill="#E3F3FC")
    s.F("rect", x=380, y=312, width=60, height=28, rx=8, fill=A2)
    s.F("circle", cx=110, cy=120, r=44, fill=A2)
    s.M("M90 120 H130 M110 100 V140", LIGHT, 10)


@reg("theory-of-relativity")
def _(s):
    s.F("rect", x=40, y=140, width=432, height=232, rx=44, fill=A1)
    txt(s, "E = mc²", 256, 256, 360, 100, LIGHT)
    s.F("polygon", points=star_pts(430, 120, 26, 10, 4), fill=A2)
    s.F("polygon", points=star_pts(80, 400, 20, 8, 4), fill=A2L)


@reg("heliocentric-model")
def _(s):
    for r in (80, 130, 180):
        s.raw(f'<circle cx="256" cy="256" r="{r}" fill="none" stroke="{MID}" stroke-width="8" stroke-dasharray="12 12"/>')
    s.F("circle", cx=256, cy=256, r=50, fill=A2)
    s.F("circle", outline=False, cx=240, cy=240, r=16, fill=A2L)
    for r, a, c, rr in ((80, 40, A1, 18), (130, 160, A1L, 24), (180, 290, A1D, 20)):
        x, y = arc_pt(256, 256, r, a)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=rr, fill=c)


@reg("round-earth-discovery")
def _(s):
    s.F("circle", cx=256, cy=290, r=190, fill=A1)
    s.F("path", outline=False, d="M150 220 C190 170 250 190 280 230 C300 270 250 300 200 290 C160 280 130 260 150 220Z", fill=A1L)
    s.F("path", outline=False, d="M310 330 C350 300 400 330 380 380 C350 410 310 390 310 330Z", fill=A1L)
    s.F("path", d="M230 100 H330 L316 130 H244Z", fill=A2)
    s.T("M280 60 V100", DARK, 8)
    s.F("path", d="M280 60 L330 90 H280Z", fill=LIGHT)
    s.M("M60 120 C100 110 130 120 160 108", MID, 8)


@reg("discovery-of-zero")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=A2)
    s.raw(f'<ellipse cx="256" cy="256" rx="70" ry="110" fill="{LIGHT}" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    s.F("polygon", points=star_pts(400, 120, 24, 10, 4), fill=A2L)
    s.F("polygon", points=star_pts(110, 390, 18, 8, 4), fill=A2L)


@reg("speed-of-light-measurement")
def _(s):
    s.F("circle", cx=100, cy=256, r=54, fill=A2)
    s.T("M150 256 H360", A2, 22)
    s.F("polygon", points="360,216 440,256 360,296", fill=A2)
    s.F("rect", x=40, y=380, width=432, height=90, rx=30, fill=A1)
    txt(s, "300 000 km/s", 256, 425, 380, 44, LIGHT)
    s.F("rect", x=430, y=80, width=40, height=150, rx=10, fill=MID)


@reg("discovery-of-the-cell")
def _(s):
    for r in range(3):
        for c in range(4):
            s.F("rect", x=60 + c * 98 + (r % 2) * 20, y=80 + r * 98, width=90, height=90, rx=18, fill=A1L if (r + c) % 2 else A1)
            dot(s, 105 + c * 98 + (r % 2) * 20, 125 + r * 98, 14, A2)
    s.T("M360 380 L450 460", DARK, 34)
    s.F("circle", cx=330, cy=350, r=70, fill="#E3F3FC", fill_opacity="0.7")
    ring(s, 330, 350, 70, A2, 14)


@reg("discovery-of-insulin")
def _(s):
    s.F("path", d="M190 190 H322 V420 C322 450 306 462 280 462 H232 C206 462 190 450 190 420Z", fill="#E3F3FC")
    s.F("path", outline=False, d="M198 300 H314 V420 C314 444 300 454 280 454 H232 C212 454 198 444 198 420Z", fill=A1L)
    s.F("rect", x=216, y=150, width=80, height=46, rx=10, fill=A2)
    s.F("rect", x=236, y=110, width=40, height=42, rx=8, fill=MID)
    txt(s, "INS", 256, 380, 80, 40, A1D)
    s.F("circle", cx=410, cy=120, r=44, fill=A2)
    s.F("path", outline=False, d="M410 148 C380 128 380 104 394 100 C402 98 408 104 410 108 C412 104 418 98 426 100 C440 104 440 128 410 148Z", fill=LIGHT)


@reg("discovery-of-antibiotics")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    s.F("path", d="M150 210 H256 V302 H150 C100 302 100 210 150 210Z", fill=A1)
    s.F("path", d="M256 210 H362 C412 210 412 302 362 302 H256Z", fill=LIGHT)
    s.close()
    s.F("rect", x=312, y=330, width=130, height=70, rx=35, fill=A2)
    for x, y in ((90, 120), (150, 90), (60, 190)):
        s.F("circle", cx=x, cy=y, r=26, fill=A2)
    s.M("M70 100 L110 140 M110 100 L70 140", DARK, 12)


@reg("discovery-of-new-planets")
def _(s):
    s.F("circle", cx=300, cy=250, r=100, fill=A2)
    s.F("path", outline=False, d="M215 220 C260 200 330 220 390 210 C395 225 395 240 390 250 C330 260 260 240 210 250Z", fill=A2L)
    s.raw(f'<ellipse cx="300" cy="260" rx="190" ry="48" fill="none" stroke="{INK}" stroke-width="40" transform="rotate(-18 300 260)" data-outline="under"/>')
    s.raw(f'<ellipse cx="300" cy="260" rx="190" ry="48" fill="none" stroke="{A1L}" stroke-width="20" transform="rotate(-18 300 260)"/>')
    s.F("polygon", points=star_pts(90, 100, 28, 11, 4), fill=A1)
    s.F("polygon", points=star_pts(440, 100, 20, 8, 4), fill=A2L)
    s.F("polygon", points=star_pts(110, 420, 16, 6, 4), fill=A1L)


@reg("higgs-boson")
def _(s):
    s.F("circle", cx=256, cy=256, r=60, fill=A2)
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(256, 256, 70, a)
        x2, y2 = arc_pt(256, 256, 190 if (a // 30) % 2 == 0 else 150, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", A1, 10)
        s.F("circle", outline=False, cx=f"{x2:.0f}", cy=f"{y2:.0f}", r=12, fill=A1D)
    s.F("circle", outline=False, cx=256, cy=256, r=26, fill=A2L)


@reg("gravitational-waves")
def _(s):
    s.F("circle", cx=180, cy=256, r=34, fill=DARK)
    s.F("circle", cx=332, cy=256, r=44, fill=DARK)
    for r in (80, 130, 180, 230):
        s.raw(f'<circle cx="256" cy="256" r="{r}" fill="none" stroke="{A1}" stroke-width="10" stroke-opacity="{1 - r / 300:.2f}"/>')
    s.M("M180 256 L332 256", MID, 4, dash="6 10")


# ================================================================ invention-ideas
@reg("invention")
def _(s):
    s.F("path", d="M256 40 C150 40 110 130 140 210 C158 258 196 280 196 320 H316 C316 280 354 258 372 210 C402 130 362 40 256 40Z", fill=A2L)
    s.F("rect", x=190, y=320, width=132, height=40, rx=10, fill=MID)
    s.F("rect", x=214, y=360, width=84, height=40, rx=16, fill=DARK)
    s.F("circle", cx=256, cy=180, r=52, fill=A1)
    for a in range(0, 360, 45):
        x, y = arc_pt(256, 180, 52, a)
        s.F("rect", outline=False, x=x - 11, y=y - 11, width=22, height=22, rx=5, fill=A1, transform=f"rotate({a} {x:.0f} {y:.0f})")
    s.F("circle", outline=False, cx=256, cy=180, r=26, fill=A1L)
    s.F("circle", cx=256, cy=180, r=12, fill=A2)


@reg("inventors-workshop")
def _(s):
    s.F("rect", x=30, y=330, width=452, height=40, rx=12, fill=A1D)
    s.T("M80 370 V460 M432 370 V460", DARK, 22)
    s.F("path", d="M60 120 H452 V320 H60Z", fill=A1L, fill_opacity="0.4")
    s.M("M60 120 H452", DARK, 14)
    for x in (110, 170, 230):
        s.T(f"M{x} 120 V170", DARK, 6)
    s.F("rect", x=96, y=170, width=30, height=70, rx=8, fill=MID)
    s.F("rect", x=156, y=170, width=30, height=50, rx=8, fill=A2)
    s.F("rect", x=216, y=170, width=30, height=60, rx=8, fill=A1)
    s.F("path", d="M330 330 C330 270 370 250 380 200 C400 200 420 220 420 240 C420 270 430 300 430 330Z", fill=A2L)
    s.F("circle", cx=370, cy=170, r=40, fill=A2L)
    s.F("rect", x=240, y=290, width=70, height=40, rx=10, fill=A2)
    s.F("circle", cx=140, cy=300, r=30, fill=A1)
    s.F("circle", outline=False, cx=140, cy=300, r=12, fill=A1L)


@reg("patent")
def _(s):
    s.F("rect", x=80, y=50, width=352, height=412, rx=20, fill=LIGHT)
    s.F("rect", outline=False, x=100, y=70, width=312, height=40, rx=10, fill=A1L)
    s.M("M130 160 H382 M130 200 H340 M130 240 H382", MID, 12)
    s.F("rect", outline=False, x=130, y=280, width=130, height=100, rx=12, fill=A1L, fill_opacity="0.6")
    s.F("circle", cx=370, cy=370, r=54, fill=A2)
    s.F("polygon", points=star_pts(370, 370, 38, 18, 8), fill=A2L)
    s.F("path", d="M340 410 L330 470 L370 450 L410 470 L400 410Z", fill=A1)


@reg("blueprint")
def _(s):
    s.F("rect", x=40, y=80, width=432, height=352, rx=20, fill=A1D)
    for i in range(1, 8):
        s.M(f"M{40 + i * 54} 80 V432", A1, 3)
    for i in range(1, 6):
        s.M(f"M40 {80 + i * 59} H472", A1, 3)
    s.M("M120 360 V220 L256 140 L392 220 V360Z M120 360 H392 M220 360 V280 H292 V360", LIGHT, 8)
    s.M("M120 400 H392 M120 390 V410 M392 390 V410", LIGHT, 6)


@reg("prototype")
def _(s):
    s.raw(f'<rect x="110" y="110" width="250" height="290" rx="40" fill="{A1L}" fill-opacity="0.35" stroke="{INK}" stroke-width="10" stroke-dasharray="22 16"/>')
    s.F("circle", cx=235, cy=210, r=50, fill=A1, fill_opacity="0.75")
    s.M("M170 320 H300 M170 360 H260", MID, 12)
    s.open(transform="rotate(35 400 330)")
    s.F("rect", x=390, y=240, width=26, height=190, rx=10, fill=MID)
    s.F("path", d="M370 250 C370 200 440 200 440 250 C440 270 428 280 416 280 H394 C382 280 370 270 370 250Z", fill=MID)
    s.F("rect", outline=False, x=395, y=210, width=16, height=30, fill=LIGHT)
    s.close()
    s.F("circle", cx=110, cy=110, r=22, fill=A2)


@reg("timeline-of-inventions")
def _(s):
    s.T("M40 256 H472", DARK, 16)
    s.F("polygon", points="496,256 456,230 456,282", fill=DARK)
    for x, y, c in ((100, 150, A1), (210, 360, A2), (320, 150, A1D), (420, 360, A2L)):
        s.T(f"M{x} 256 V{y}", MID, 8)
        s.F("circle", cx=x, cy=y, r=44, fill=c)
        s.F("circle", cx=x, cy=256, r=18, fill=LIGHT)
    bolt(s, 100, 150, 0.2, LIGHT)
    s.F("rect", outline=False, x=190, y=345, width=40, height=30, rx=6, fill=LIGHT)
    s.F("circle", outline=False, cx=320, cy=150, r=16, fill=LIGHT)
    s.F("polygon", points=star_pts(420, 360, 22, 9, 4), fill=A2)


@reg("accidental-discovery")
def _(s):
    s.F("path", d="M200 120 H290 V210 L380 380 C392 410 376 440 342 440 H148 C114 440 98 410 110 380 L200 210Z", fill="#E3F3FC")
    s.F("path", outline=False, d="M150 320 H340 L380 390 C386 410 374 426 346 426 H144 C116 426 104 410 110 390Z", fill=A2L)
    bolt(s, 400, 170, 0.35, A2)
    s.F("circle", cx=110, cy=130, r=44, fill=A1)
    txt(s, "!", 110, 130, 20, 54, LIGHT)
    for x, y, r in ((200, 380, 10), (260, 350, 8), (300, 395, 9)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=WHITE, fill_opacity="0.9")


if __name__ == "__main__":
    run("inventions-discoveries", D, sys.argv[1:] or None)
