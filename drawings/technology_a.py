"""technology drawings, part A: devices and computer parts. Run: python drawings/technology_a.py [ids...]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tech import (A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, INK, WHITE, arc_pt, arrow, bolt, dot, registry, ring, run, screen, shine, txt, wifi)  # noqa: E402

D, reg = registry()


# ================================================================ devices
@reg("smartphone")
def _(s):
    s.F("rect", x=150, y=40, width=212, height=432, rx=44, fill=DARK)
    s.F("rect", outline=False, x=168, y=76, width=176, height=360, rx=20, fill=A1L)
    s.F("rect", outline=False, x=224, y=54, width=64, height=12, rx=6, fill=MID)
    for r in range(3):
        for c in range(3):
            s.F("rect", outline=False, x=186 + c * 52, y=100 + r * 54, width=40, height=40, rx=12, fill=A2 if (r + c) % 3 == 0 else WHITE)
    shine(s, 184, 330, 120, 14, "0.6")
    s.F("rect", outline=False, x=184, y=360, width=144, height=50, rx=18, fill=A1)


@reg("feature-phone")
def _(s):
    s.F("rect", x=160, y=40, width=192, height=432, rx=36, fill=A2)
    s.F("rect", x=184, y=70, width=144, height=110, rx=14, fill=A1L)
    s.F("rect", outline=False, x=198, y=86, width=116, height=24, rx=8, fill=WHITE, fill_opacity="0.6")
    for r in range(4):
        for c in range(3):
            s.F("rect", outline=False, x=188 + c * 50, y=206 + r * 56, width=40, height=42, rx=14, fill=LIGHT)


@reg("tablet")
def _(s):
    screen(s, 50, 90, 412, 332, DARK, A1L, 36, 22)
    shine(s, 90, 130, 150, 16, "0.6")
    s.F("rect", outline=False, x=90, y=170, width=140, height=100, rx=14, fill=A2)
    s.F("rect", outline=False, x=250, y=170, width=130, height=44, rx=12, fill=WHITE)
    s.F("rect", outline=False, x=250, y=226, width=130, height=44, rx=12, fill=A1)
    s.F("rect", outline=False, x=90, y=290, width=290, height=60, rx=14, fill=WHITE)


@reg("laptop")
def _(s):
    s.F("rect", x=100, y=90, width=312, height=220, rx=24, fill=DARK)
    s.F("rect", outline=False, x=120, y=110, width=272, height=180, rx=10, fill=A1L)
    s.F("path", d="M50 330 H462 L482 392 C484 408 474 416 460 416 H52 C38 416 28 408 30 392Z", fill=MID)
    s.F("rect", outline=False, x=200, y=334, width=112, height=16, rx=8, fill=LIGHT)
    s.F("rect", outline=False, x=140, y=130, width=110, height=70, rx=10, fill=A2)
    s.F("rect", outline=False, x=266, y=130, width=106, height=34, rx=8, fill=WHITE)
    s.F("rect", outline=False, x=266, y=176, width=106, height=24, rx=8, fill=A1)


@reg("desktop-computer")
def _(s):
    s.F("rect", x=40, y=70, width=290, height=230, rx=24, fill=DARK)
    s.F("rect", outline=False, x=58, y=88, width=254, height=194, rx=10, fill=A1L)
    s.F("rect", x=156, y=300, width=60, height=50, fill=MID)
    s.F("rect", x=100, y=350, width=170, height=26, rx=12, fill=MID)
    s.F("rect", x=350, y=100, width=122, height=276, rx=20, fill=A1)
    s.F("circle", outline=False, cx=411, cy=150, r=18, fill=LIGHT)
    s.F("rect", outline=False, x=372, y=200, width=78, height=14, rx=7, fill=A1L)
    s.F("rect", outline=False, x=372, y=226, width=78, height=14, rx=7, fill=A1L)
    s.F("rect", x=60, y=414, width=250, height=44, rx=14, fill=LIGHT)


@reg("computer-monitor")
def _(s):
    screen(s, 50, 70, 412, 290, DARK, A1L, 28, 20)
    s.F("path", outline=False, d="M90 110 L260 110 L90 270Z", fill=WHITE, fill_opacity="0.35")
    s.F("path", d="M226 360 H286 L300 420 H212Z", fill=MID)
    s.F("rect", x=160, y=416, width=192, height=34, rx=14, fill=MID)


@reg("keyboard")
def _(s):
    s.F("rect", x=30, y=130, width=452, height=252, rx=36, fill=MID)
    for r, n in enumerate((10, 10, 9)):
        for c in range(n):
            s.F("rect", outline=False, x=58 + c * 40 + r * 14, y=158 + r * 58, width=32, height=44, rx=8, fill=LIGHT)
    s.F("rect", outline=False, x=130, y=332, width=252, height=34, rx=10, fill=LIGHT)
    s.F("rect", outline=False, x=58, y=332, width=60, height=34, rx=10, fill=A1)
    s.F("rect", outline=False, x=394, y=332, width=60, height=34, rx=10, fill=A2)


@reg("computer-mouse")
def _(s):
    s.F("path", d="M256 50 C370 50 400 150 400 280 C400 400 340 462 256 462 C172 462 112 400 112 280 C112 150 142 50 256 50Z", fill=LIGHT)
    s.F("path", d="M256 50 C200 50 150 80 128 180 H256Z", fill=A1)
    s.F("path", d="M256 50 C312 50 362 80 384 180 H256Z", fill=A1L)
    s.F("rect", x=232, y=96, width=48, height=96, rx=24, fill=A2)
    shine(s, 150, 250, 40, 100, "0.5")


@reg("printer")
def _(s):
    s.F("rect", x=130, y=50, width=252, height=140, rx=10, fill=LIGHT)
    s.F("rect", outline=False, x=160, y=80, width=130, height=12, rx=6, fill=MID)
    s.F("rect", outline=False, x=160, y=110, width=190, height=12, rx=6, fill=MID)
    s.F("path", d="M50 190 H462 V380 H50Z", fill=A1)
    s.F("rect", outline=False, x=66, y=200, width=380, height=30, rx=10, fill=A1L, fill_opacity="0.6")
    s.F("circle", cx=410, cy=250, r=16, fill=A2)
    s.F("rect", x=120, y=330, width=272, height=130, rx=10, fill=LIGHT)
    s.F("rect", outline=False, x=150, y=360, width=180, height=12, rx=6, fill=A1L)
    s.F("rect", outline=False, x=150, y=392, width=130, height=12, rx=6, fill=A1L)
    s.F("rect", x=100, y=326, width=312, height=20, rx=10, fill=DARK)


@reg("scanner")
def _(s):
    s.F("polygon", points="112,230 400,230 424,96 88,96", fill=A1D)
    s.F("polygon", outline=False, points="130,208 380,208 394,120 116,120", fill=A1, fill_opacity="0.7")
    s.F("polygon", points="64,320 448,320 400,230 112,230", fill=LIGHT)
    s.F("rect", x=180, y=252, width=150, height=50, rx=6, fill=WHITE, transform="skewX(-20) translate(66 0)")
    s.F("rect", x=50, y=320, width=412, height=90, rx=26, fill=A1)
    s.F("rect", outline=False, x=80, y=346, width=250, height=14, rx=7, fill=A1L)
    s.F("circle", cx=410, cy=366, r=14, fill=A2)


@reg("webcam")
def _(s):
    s.F("rect", x=130, y=340, width=252, height=60, rx=18, fill=DARK)
    s.F("rect", x=226, y=250, width=60, height=100, rx=10, fill=MID)
    s.F("circle", cx=256, cy=170, r=130, fill=DARK)
    s.F("circle", cx=256, cy=170, r=84, fill=MID)
    s.F("circle", cx=256, cy=170, r=52, fill=A1)
    s.F("circle", outline=False, cx=236, cy=150, r=16, fill=WHITE, fill_opacity="0.7")
    dot(s, 256, 60, 10, A2)


@reg("smartwatch")
def _(s):
    s.F("path", d="M190 20 H322 L336 130 H176Z", fill=A1D)
    s.F("path", d="M176 382 H336 L322 492 H190Z", fill=A1D)
    s.F("rect", x=110, y=120, width=292, height=272, rx=70, fill=DARK)
    s.F("rect", outline=False, x=132, y=142, width=248, height=228, rx=52, fill=A1L)
    ring(s, 256, 256, 60, A2, 20)
    s.F("rect", x=402, y=214, width=26, height=80, rx=12, fill=MID)


@reg("fitness-band")
def _(s):
    s.F("path", d="M60 200 H452 V312 H60Z", fill=A1D)
    for x in (110, 150, 362, 402):
        dot(s, x, 256, 8, A1L)
    s.F("rect", x=170, y=170, width=172, height=172, rx=40, fill=DARK)
    s.F("rect", outline=False, x=188, y=188, width=136, height=136, rx=28, fill=A1L)
    s.F("path", outline=False, d="M256 300 C206 266 206 226 232 222 C246 220 254 230 256 238 C258 230 266 220 280 222 C306 226 306 266 256 300Z", fill=A2)


@reg("earbuds")
def _(s):
    s.F("rect", x=130, y=300, width=252, height=150, rx=70, fill=LIGHT)
    s.F("rect", outline=False, x=130, y=300, width=252, height=36, rx=18, fill=MID, fill_opacity="0.5")
    dot(s, 256, 400, 12, A2)
    for x, f in ((150, 1), (362, -1)):
        s.F("path", d=f"M{x} 80 C{x - 60 * f} 60 {x - 70 * f} 180 {x - 20 * f} 200 L{x - 14 * f} 290 H{x + 26 * f} L{x + 24 * f} 190 C{x + 70 * f} 150 {x + 60 * f} 90 {x} 80Z", fill=A1)
        dot(s, x - 14 * f, 130, 12, A1L)


@reg("smart-speaker")
def _(s):
    s.F("path", d="M130 150 C130 90 382 90 382 150 V380 C382 460 130 460 130 380Z", fill=A1D)
    s.F("ellipse", cx=256, cy=150, rx=126, ry=44, fill=A1)
    s.F("ellipse", outline=False, cx=256, cy=150, rx=96, ry=26, fill=DARK)
    s.raw(f'<path d="M140 380 C140 410 372 410 372 380" fill="none" stroke="{A2}" stroke-width="16" stroke-linecap="round"/>')
    for x in range(160, 360, 40):
        s.F("circle", outline=False, cx=x, cy=290, r=6, fill=A1L)
        s.F("circle", outline=False, cx=x + 20, cy=320, r=6, fill=A1L)


@reg("game-controller")
def _(s):
    s.F("path", d="M110 150 H402 C470 150 500 290 460 380 C440 420 390 400 360 340 H152 C122 400 72 420 52 380 C12 290 42 150 110 150Z", fill=A1)
    s.M("M120 230 H190 M155 195 V265", LIGHT, 22)
    for x, y, c in ((380, 200, A2), (420, 240, LIGHT), (340, 240, LIGHT), (380, 280, A2L)):
        s.F("circle", cx=x, cy=y, r=20, fill=c)
    s.F("circle", outline=False, cx=215, cy=290, r=22, fill=DARK)
    s.F("circle", outline=False, cx=297, cy=290, r=22, fill=DARK)
    s.F("rect", outline=False, x=130, y=162, width=250, height=18, rx=9, fill=A1L, fill_opacity="0.5")


@reg("game-console")
def _(s):
    s.F("path", d="M50 190 L120 110 H392 L462 190 V340 C462 370 440 390 410 390 H102 C72 390 50 370 50 340Z", fill=A1D)
    s.F("rect", outline=False, x=100, y=170, width=312, height=34, rx=17, fill=DARK)
    s.F("rect", outline=False, x=100, y=222, width=312, height=12, rx=6, fill=A1L)
    s.F("circle", cx=398, cy=300, r=22, fill=A2)
    s.F("rect", outline=False, x=96, y=290, width=130, height=14, rx=7, fill=MID)
    s.F("rect", outline=False, x=96, y=318, width=90, height=14, rx=7, fill=MID)


@reg("vr-headset")
def _(s):
    s.T("M60 230 C60 130 140 80 256 80 C372 80 452 130 452 230", A1D, 34)
    s.F("path", d="M60 190 H452 C482 190 492 230 490 280 C488 340 450 410 400 410 C350 410 320 340 256 340 C192 340 162 410 112 410 C62 410 24 340 22 280 C20 230 30 190 60 190Z", fill=DARK)
    s.F("path", outline=False, d="M90 220 H422 C440 220 450 250 446 290 C440 340 420 366 400 366 C360 366 330 310 256 310 C182 310 152 366 112 366 C92 366 72 340 66 290 C62 250 72 220 90 220Z", fill=A1L)
    s.F("rect", outline=False, x=224, y=205, width=64, height=14, rx=7, fill=WHITE, fill_opacity="0.7")
    dot(s, 130, 270, 10, A2)
    dot(s, 382, 270, 10, A2)


@reg("camera-drone")
def _(s):
    s.T("M256 230 L90 160 M256 230 L422 160 M256 270 L100 340 M256 270 L412 340", DARK, 20)
    for x, y in ((90, 150), (422, 150), (100, 350), (412, 350)):
        s.F("ellipse", cx=x, cy=y, rx=62, ry=16, fill=A1L)
        s.F("rect", outline=False, x=x - 6, y=y - 16, width=12, height=32, fill=DARK)
    s.F("rect", x=190, y=200, width=132, height=100, rx=36, fill=A1)
    s.F("circle", cx=256, cy=330, r=38, fill=DARK)
    s.F("circle", outline=False, cx=256, cy=330, r=20, fill=A2)


@reg("camera")
def _(s):
    s.F("path", d="M60 160 H170 L196 110 H316 L342 160 H452 C474 160 484 170 484 190 V390 C484 410 474 420 452 420 H60 C38 420 28 410 28 390 V190 C28 170 38 160 60 160Z", fill=DARK)
    s.F("rect", outline=False, x=28, y=200, width=456, height=70, fill=A1D)
    s.F("circle", cx=256, cy=290, r=110, fill=MID)
    s.F("circle", cx=256, cy=290, r=78, fill=DARK)
    s.F("circle", cx=256, cy=290, r=48, fill=A1)
    s.F("circle", outline=False, cx=236, cy=270, r=14, fill=WHITE, fill_opacity="0.7")
    s.F("rect", x=70, y=124, width=60, height=30, rx=8, fill=A2)
    dot(s, 420, 212, 12, A2L)


@reg("action-camera")
def _(s):
    s.F("rect", x=90, y=130, width=332, height=252, rx=46, fill=A1D)
    s.F("circle", cx=256, cy=256, r=96, fill=DARK)
    s.F("circle", cx=256, cy=256, r=62, fill=A1)
    s.F("circle", outline=False, cx=236, cy=236, r=18, fill=WHITE, fill_opacity="0.7")
    s.F("rect", x=130, y=96, width=60, height=34, rx=10, fill=A2)
    s.F("circle", cx=370, cy=170, r=14, fill=A2L)
    s.F("rect", outline=False, x=110, y=316, width=60, height=40, rx=12, fill=A1L, fill_opacity="0.5")


@reg("usb-cable")
def _(s):
    s.T("M120 330 C120 140 392 400 392 190", DARK, 22)
    s.F("rect", x=90, y=330, width=60, height=70, rx=8, fill=MID)
    s.F("rect", x=100, y=400, width=40, height=62, rx=6, fill=A1)
    s.F("rect", outline=False, x=106, y=420, width=10, height=14, rx=3, fill=DARK)
    s.F("rect", outline=False, x=124, y=420, width=10, height=14, rx=3, fill=DARK)
    s.F("rect", x=362, y=130, width=60, height=70, rx=8, fill=MID)
    s.F("rect", x=372, y=60, width=40, height=70, rx=8, fill=A2)


@reg("phone-charger")
def _(s):
    s.F("rect", x=170, y=100, width=172, height=190, rx=34, fill=LIGHT)
    s.F("rect", x=200, y=40, width=16, height=64, rx=6, fill=MID)
    s.F("rect", x=296, y=40, width=16, height=64, rx=6, fill=MID)
    bolt(s, 256, 196, 0.42, A2)
    s.T("M256 290 C256 380 150 380 150 440", DARK, 18)
    s.F("rect", x=122, y=430, width=56, height=44, rx=10, fill=A1)


@reg("power-bank")
def _(s):
    s.F("rect", x=130, y=60, width=252, height=392, rx=44, fill=A1)
    s.F("rect", outline=False, x=150, y=80, width=212, height=60, rx=20, fill=A1L, fill_opacity="0.5")
    for i in range(4):
        s.F("rect", outline=False, x=164 + i * 48, y=180, width=36, height=18, rx=9, fill=A2 if i < 3 else LIGHT)
    bolt(s, 256, 320, 0.34, LIGHT)
    s.F("rect", outline=False, x=210, y=416, width=92, height=14, rx=7, fill=DARK)


@reg("external-hard-drive")
def _(s):
    s.F("rect", x=70, y=120, width=372, height=252, rx=40, fill=A1D)
    s.F("rect", outline=False, x=90, y=140, width=332, height=60, rx=22, fill=A1L, fill_opacity="0.4")
    s.F("circle", cx=256, cy=290, r=52, fill=DARK)
    s.F("circle", outline=False, cx=256, cy=290, r=18, fill=MID)
    dot(s, 392, 160, 10, A2)
    s.T("M256 372 C256 430 150 420 130 470", DARK, 16)


@reg("memory-card")
def _(s):
    s.F("path", d="M130 50 H320 L400 130 V440 C400 456 388 464 374 464 H138 C122 464 112 456 112 440 V70 C112 58 120 50 130 50Z", fill=A1D)
    s.F("path", outline=False, d="M130 66 H316 L384 134 V250 H130Z", fill=A1L, fill_opacity="0.35")
    for i in range(6):
        s.F("rect", outline=False, x=140 + i * 38, y=70, width=24, height=60, rx=6, fill=A2L)
    txt(s, "SD", 256, 340, 120, 70, LIGHT)


@reg("usb-flash-drive")
def _(s):
    s.open(transform="rotate(-35 256 256)")
    s.F("rect", x=60, y=210, width=130, height=92, rx=10, fill=MID)
    s.F("rect", outline=False, x=86, y=236, width=22, height=14, rx=3, fill=DARK)
    s.F("rect", outline=False, x=118, y=236, width=22, height=14, rx=3, fill=DARK)
    s.F("rect", x=190, y=190, width=270, height=132, rx=44, fill=A1)
    s.F("circle", cx=400, cy=256, r=24, fill=A1L)
    s.F("rect", outline=False, x=214, y=206, width=130, height=20, rx=10, fill=A1L, fill_opacity="0.6")
    s.close()


@reg("projector")
def _(s):
    s.F("path", d="M40 150 H380 C420 150 440 180 440 220 V290 C440 330 410 350 380 350 H40Z", fill=A1)
    s.F("circle", cx=320, cy=250, r=78, fill=DARK)
    s.F("circle", cx=320, cy=250, r=50, fill=A1L)
    s.F("circle", outline=False, cx=302, cy=232, r=14, fill=WHITE, fill_opacity="0.7")
    s.F("rect", outline=False, x=60, y=176, width=170, height=14, rx=7, fill=A1L, fill_opacity="0.7")
    dot(s, 80, 300, 12, A2)
    s.F("rect", x=100, y=350, width=40, height=50, rx=8, fill=DARK)
    s.F("rect", x=300, y=350, width=40, height=50, rx=8, fill=DARK)
    s.F("polygon", outline=False, points="410,190 500,120 500,380 410,310", fill=A2L, fill_opacity="0.6")


# ================================================================ computer-parts
def pins(s, x0, y0, n, step, w, h, horizontal=True, color=A2):
    for i in range(n):
        if horizontal:
            s.F("rect", outline=False, x=x0 + i * step, y=y0, width=w, height=h, rx=3, fill=color)
        else:
            s.F("rect", outline=False, x=x0, y=y0 + i * step, width=h, height=w, rx=3, fill=color)


@reg("motherboard")
def _(s):
    s.F("rect", x=50, y=50, width=412, height=412, rx=30, fill=A1D)
    s.F("rect", x=170, y=130, width=110, height=110, rx=10, fill=MID)
    s.F("rect", outline=False, x=190, y=150, width=70, height=70, rx=6, fill=DARK)
    for i in range(4):
        s.F("rect", x=330 + i * 28, y=80, width=18, height=180, rx=6, fill=DARK)
    s.F("rect", x=90, y=320, width=300, height=34, rx=10, fill=DARK)
    s.F("rect", x=90, y=380, width=300, height=34, rx=10, fill=DARK)
    s.F("rect", x=80, y=90, width=60, height=140, rx=10, fill=A2)
    s.M("M290 190 H320 M280 280 H430 M150 280 V310", A1L, 6)
    dot(s, 420, 420, 14, A2L)


@reg("cpu")
def _(s):
    s.F("rect", x=110, y=110, width=292, height=292, rx=36, fill=DARK)
    s.F("rect", x=160, y=160, width=192, height=192, rx=20, fill=MID)
    s.F("rect", outline=False, x=190, y=190, width=132, height=132, rx=12, fill=A1)
    txt(s, "CPU", 256, 256, 100, 44, LIGHT)
    for i in range(5):
        s.F("rect", outline=False, x=142 + i * 52, y=72, width=24, height=36, rx=6, fill=A2)
        s.F("rect", outline=False, x=142 + i * 52, y=404, width=24, height=36, rx=6, fill=A2)
        s.F("rect", outline=False, x=72, y=142 + i * 52, width=36, height=24, rx=6, fill=A2)
        s.F("rect", outline=False, x=404, y=142 + i * 52, width=36, height=24, rx=6, fill=A2)


@reg("ram-stick")
def _(s):
    s.F("rect", x=40, y=150, width=432, height=190, rx=20, fill=A1)
    for i in range(6):
        s.F("rect", x=70 + i * 62, y=186, width=48, height=70, rx=8, fill=DARK)
    for i in range(14):
        s.F("rect", outline=False, x=60 + i * 30, y=340, width=18, height=30, rx=3, fill=A2)
    s.F("rect", outline=False, x=40, y=290, width=432, height=14, fill=A1L, fill_opacity="0.7")
    s.F("path", d="M230 340 V372 H262 V340Z", fill=A1)


@reg("graphics-card")
def _(s):
    s.F("rect", x=40, y=140, width=432, height=210, rx=26, fill=DARK)
    ring(s, 160, 245, 70, A1, 30)
    ring(s, 350, 245, 70, A1, 30)
    for cx in (160, 350):
        s.F("circle", cx=cx, cy=245, r=22, fill=A2)
    s.F("rect", x=60, y=350, width=360, height=40, rx=10, fill=MID)
    for i in range(12):
        s.F("rect", outline=False, x=76 + i * 28, y=360, width=14, height=24, rx=3, fill=A2)
    s.F("rect", x=440, y=170, width=24, height=130, rx=8, fill=A1D)


@reg("circuit-board")
def _(s):
    s.F("rect", x=50, y=50, width=412, height=412, rx=36, fill=A1D)
    s.M("M100 140 H220 L260 180 H400 M100 250 H180 L220 290 H300 V400 M360 250 H420 M130 400 H220", A1L, 9)
    for x, y in ((100, 140), (400, 180), (100, 250), (420, 250), (300, 400), (130, 400)):
        s.F("circle", cx=x, cy=y, r=16, fill=A2)
    s.F("rect", x=210, y=190, width=90, height=70, rx=10, fill=DARK)
    s.F("rect", x=320, y=300, width=80, height=50, rx=10, fill=MID)


@reg("computer-chip")
def _(s):
    s.F("rect", x=110, y=110, width=292, height=292, rx=36, fill=A1)
    s.F("rect", outline=False, x=150, y=150, width=212, height=212, rx=20, fill=A1L, fill_opacity="0.45")
    s.F("circle", cx=256, cy=256, r=44, fill=DARK)
    s.F("circle", outline=False, cx=256, cy=256, r=18, fill=A2)
    for i in range(5):
        s.F("rect", x=136 + i * 56, y=60, width=24, height=48, rx=8, fill=MID)
        s.F("rect", x=136 + i * 56, y=404, width=24, height=48, rx=8, fill=MID)
        s.F("rect", x=60, y=136 + i * 56, width=48, height=24, rx=8, fill=MID)
        s.F("rect", x=404, y=136 + i * 56, width=48, height=24, rx=8, fill=MID)


@reg("cooling-fan")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=60, fill=DARK)
    s.F("circle", outline=False, cx=256, cy=256, r=170, fill=MID)
    s.open("part-wheel", "256 256")
    for a in range(0, 360, 72):
        x1, y1 = arc_pt(256, 256, 40, a)
        x2, y2 = arc_pt(256, 256, 150, a + 30)
        x3, y3 = arc_pt(256, 256, 150, a - 20)
        s.F("path", d=f"M256 256 L{x3:.0f} {y3:.0f} Q{x2:.0f} {y2:.0f} {x2:.0f} {y2:.0f} Q{(x1 + x2) / 2 + 30:.0f} {(y1 + y2) / 2 + 30:.0f} 256 256Z", fill=A1)
    s.close()
    s.F("circle", cx=256, cy=256, r=34, fill=A2)
    for x, y in ((92, 92), (420, 92), (92, 420), (420, 420)):
        dot(s, x, y, 12, A1L)


@reg("hard-disk")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=36, fill=MID)
    s.F("circle", cx=240, cy=256, r=150, fill=LIGHT)
    s.F("circle", cx=240, cy=256, r=60, fill=A1)
    s.F("circle", cx=240, cy=256, r=14, fill=DARK)
    s.F("path", d="M430 90 L330 220 L350 250 L440 120Z", fill=A2)
    dot(s, 420, 420, 14, A1)


@reg("ssd")
def _(s):
    s.F("rect", x=60, y=130, width=392, height=252, rx=30, fill=A1D)
    s.F("rect", outline=False, x=80, y=150, width=352, height=100, rx=20, fill=A1L, fill_opacity="0.4")
    s.F("rect", outline=False, x=96, y=290, width=70, height=60, rx=10, fill=DARK)
    s.F("rect", outline=False, x=180, y=290, width=70, height=60, rx=10, fill=DARK)
    txt(s, "SSD", 340, 206, 150, 56, LIGHT)
    bolt(s, 380, 320, 0.22, A2)


if __name__ == "__main__":
    run("technology", D, sys.argv[1:] or None)
