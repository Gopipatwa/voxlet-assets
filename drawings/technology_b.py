"""technology drawings, part B: internet, cybersecurity, ai-robots, programming, smart-home, telecom.
Run: python drawings/technology_b.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tech import (A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, INK, SKIN, WHITE, arc_pt, arrow, bolt, cloud, dot, lock, person_hood, registry, ring, run, screen, shine, star_pts, txt, waves, wifi)  # noqa: E402

D, reg = registry()


def globe(s, cx=256, cy=256, r=170, color=A1, land=A1L):
    s.F("circle", cx=cx, cy=cy, r=r, fill=color)
    s.F("path", outline=False, d=f"M{cx - r * 0.55} {cy - r * 0.5} C{cx - r * 0.2} {cy - r * 0.8} {cx + r * 0.1} {cy - r * 0.5} {cx} {cy - r * 0.2} C{cx - r * 0.1} {cy} {cx - r * 0.5} {cy + r * 0.1} {cx - r * 0.6} {cy - r * 0.2}Z", fill=land)
    s.F("path", outline=False, d=f"M{cx + r * 0.2} {cy + r * 0.1} C{cx + r * 0.6} {cy} {cx + r * 0.7} {cy + r * 0.4} {cx + r * 0.3} {cy + r * 0.7} C{cx + r * 0.1} {cy + r * 0.5} {cx + r * 0.1} {cy + r * 0.3} {cx + r * 0.2} {cy + r * 0.1}Z", fill=land)


# ================================================================ internet-networks
@reg("internet")
def _(s):
    globe(s, 256, 256, 130)
    pts = [(80, 120), (432, 120), (70, 390), (440, 380), (256, 60), (256, 460)]
    for x, y in pts:
        s.T(f"M256 256 L{x} {y}", MID, 8)
    for x, y in pts:
        s.F("circle", cx=x, cy=y, r=24, fill=A2)


@reg("world-wide-web-globe")
def _(s):
    globe(s, 256, 256, 190)
    s.F("rect", x=120, y=190, width=272, height=130, rx=40, fill=LIGHT)
    txt(s, "www", 256, 255, 220, 70, A1D)


@reg("wi-fi-router")
def _(s):
    s.T("M140 330 L100 140 M372 330 L412 140", DARK, 14)
    s.F("rect", x=50, y=330, width=412, height=110, rx=36, fill=A1)
    s.F("rect", outline=False, x=70, y=346, width=372, height=22, rx=11, fill=A1L, fill_opacity="0.6")
    for i in range(4):
        dot(s, 120 + i * 40, 400, 10, A2L)
    wifi(s, 256, 250, 150, A2, 20)


@reg("modem")
def _(s):
    s.F("rect", x=70, y=190, width=372, height=200, rx=40, fill=DARK)
    s.F("rect", outline=False, x=90, y=206, width=332, height=34, rx=16, fill=A1, fill_opacity="0.5")
    for i, c in enumerate((A2, A1L, A1L, MID)):
        dot(s, 130 + i * 50, 310, 14, c)
    s.F("rect", x=330, y=290, width=70, height=50, rx=8, fill=MID)
    s.T("M256 190 V90", MID, 14)
    s.F("circle", cx=256, cy=76, r=26, fill=A2)
    waves(s, 256, 76, 80, A2L, 12, 2, -150, -30)


@reg("network")
def _(s):
    s.T("M256 256 L90 120 M256 256 L422 120 M256 256 L90 400 M256 256 L422 400 M90 120 L422 120 M90 400 L422 400", MID, 10)
    s.F("circle", cx=256, cy=256, r=62, fill=A1)
    for x, y in ((90, 120), (422, 120), (90, 400), (422, 400)):
        s.F("circle", cx=x, cy=y, r=40, fill=A2)
    dot(s, 256, 256, 20, A1L)


@reg("ethernet-cable")
def _(s):
    s.T("M120 256 C200 120 312 392 392 256", A1D, 26)
    for x, f in ((30, 1), (382, 1)):
        s.F("rect", x=x, y=196, width=100, height=120, rx=14, fill=LIGHT)
        for i in range(6):
            s.F("rect", outline=False, x=x + 12 + i * 13, y=282, width=8, height=22, rx=3, fill=A2)
        s.F("rect", outline=False, x=x + 12, y=210, width=76, height=18, rx=8, fill=A1L, fill_opacity="0.6")


@reg("fibre-optic-cable")
def _(s):
    s.T("M60 390 C190 390 190 130 322 130 H400", DARK, 56)
    for i, c in enumerate((A2, A1L, A2L, A1)):
        o = i * 12 - 18
        s.M(f"M60 {390 + o} C190 {390 + o} 190 {130 + o} 322 {130 + o} H400", c, 7)
    s.F("rect", x=396, y=94, width=60, height=72, rx=12, fill=MID)
    s.M("M470 130 L500 100 M470 130 L506 130 M470 130 L500 160", A2, 10)


@reg("undersea-cable")
def _(s):
    s.F("rect", x=40, y=120, width=432, height=340, rx=30, fill=A1L)
    s.F("path", outline=False, d="M60 140 C120 110 180 170 240 140 C300 110 360 170 452 130 V150 H60Z", fill=A1)
    s.F("path", d="M40 400 C120 380 180 430 260 400 C340 370 400 420 472 390 V430 C472 448 458 460 440 460 H72 C54 460 40 448 40 430Z", fill=DARK)
    s.T("M70 410 C150 390 200 440 270 410 C340 380 400 430 450 400", A2, 12)
    s.F("rect", x=40, y=84, width=90, height=70, rx=10, fill=MID)
    s.F("rect", x=382, y=84, width=90, height=70, rx=10, fill=MID)
    s.T("M85 154 V330 C85 380 120 390 150 395 M427 154 V330 C427 380 400 390 370 395", DARK, 10)
    s.F("path", d="M170 260 C200 230 250 240 270 260 C250 290 200 290 170 260Z", fill=A2)
    s.F("path", outline=False, d="M270 260 L300 240 V280Z", fill=A2)
    dot(s, 190, 256, 6, DARK)


@reg("5g-tower")
def _(s):
    s.T("M256 140 L170 450 M256 140 L342 450 M205 330 H307 M222 250 H290", DARK, 16)
    s.F("rect", x=216, y=100, width=80, height=56, rx=12, fill=A1)
    s.F("circle", cx=256, cy=100, r=20, fill=A2)
    waves(s, 256, 100, 90, A2, 14, 2, -140, -40)
    s.F("rect", x=330, y=40, width=130, height=70, rx=26, fill=A1)
    txt(s, "5G", 395, 75, 90, 40, LIGHT)


@reg("server")
def _(s):
    for i, y in enumerate((70, 200, 330)):
        s.F("rect", x=90, y=y, width=332, height=110, rx=28, fill=A1 if i != 1 else A1D)
        s.F("rect", outline=False, x=112, y=y + 22, width=160, height=18, rx=9, fill=A1L, fill_opacity="0.7")
        s.F("rect", outline=False, x=112, y=y + 58, width=110, height=18, rx=9, fill=A1L, fill_opacity="0.4")
        dot(s, 360, y + 55, 14, A2)
        dot(s, 394, y + 55, 14, A2L)


@reg("server-rack")
def _(s):
    s.F("rect", x=100, y=40, width=312, height=432, rx=24, fill=DARK)
    for i in range(6):
        y = 64 + i * 66
        s.F("rect", x=122, y=y, width=268, height=52, rx=10, fill=A1 if i % 2 == 0 else A1D)
        s.F("rect", outline=False, x=136, y=y + 14, width=110, height=10, rx=5, fill=A1L)
        dot(s, 340, y + 26, 8, A2)
        dot(s, 366, y + 26, 8, A2L)


@reg("data-centre")
def _(s):
    s.F("rect", x=30, y=150, width=452, height=300, rx=26, fill=A1D)
    s.F("rect", outline=False, x=30, y=150, width=452, height=50, rx=24, fill=A1)
    for i in range(4):
        x = 60 + i * 106
        s.F("rect", x=x, y=224, width=84, height=200, rx=12, fill=DARK)
        for j in range(5):
            s.F("rect", outline=False, x=x + 10, y=238 + j * 36, width=64, height=24, rx=6, fill=A1L if j % 2 else MID)
            dot(s, x + 62, 250 + j * 36, 5, A2)
    s.T("M256 150 V90", DARK, 12)
    cloud(s, 256, 76, 0.28, LIGHT)


@reg("cloud-computing")
def _(s):
    cloud(s, 256, 230, 1.0, A1L)
    s.F("rect", outline=False, x=130, y=330, width=252, height=14, rx=7, fill=WHITE, fill_opacity="0.4")
    s.T("M170 400 V440 M256 400 V440 M342 400 V440", MID, 10)
    for x in (170, 256, 342):
        s.F("rect", x=x - 28, y=430, width=56, height=44, rx=10, fill=A1)
    txt(s, "{ }", 256, 245, 130, 70, A1D)


@reg("download-progress")
def _(s):
    s.F("rect", x=40, y=380, width=432, height=70, rx=35, fill=LIGHT)
    s.F("rect", x=40, y=380, width=300, height=70, rx=35, fill=A1)
    arrow(s, 256, 60, 256, 270, A2, 40, 90)
    s.F("rect", outline=False, x=70, y=396, width=200, height=14, rx=7, fill=A1L, fill_opacity="0.6")


@reg("upload-to-cloud")
def _(s):
    cloud(s, 256, 220, 0.95, A1L)
    arrow(s, 256, 440, 256, 230, A2, 36, 80)


@reg("bandwidth")
def _(s):
    s.F("rect", x=40, y=190, width=432, height=132, rx=66, fill=A1)
    s.F("rect", outline=False, x=60, y=208, width=392, height=40, rx=20, fill=A1L, fill_opacity="0.5")
    for i, x in enumerate((100, 190, 280, 370)):
        s.F("rect", x=x, y=240, width=60, height=40, rx=20, fill=A2 if i % 2 == 0 else A2L)
    arrow(s, 60, 120, 450, 120, A2, 14, 36)
    arrow(s, 450, 392, 60, 392, A1D, 14, 36)


# ================================================================ cybersecurity
@reg("cybersecurity")
def _(s):
    s.F("path", d="M256 40 L440 110 V250 C440 360 360 430 256 474 C152 430 72 360 72 250 V110Z", fill=A1)
    s.F("path", outline=False, d="M256 70 L416 130 V250 C416 340 350 405 256 444Z", fill=A1D, fill_opacity="0.4")
    lock(s, 256, 290, 0.55, A2)


@reg("password")
def _(s):
    s.F("rect", x=40, y=170, width=432, height=172, rx=44, fill=LIGHT)
    for i in range(6):
        dot(s, 100 + i * 62, 256, 20, DARK)
    s.F("rect", outline=False, x=40, y=180, width=432, height=40, rx=20, fill=A1L, fill_opacity="0.4")


@reg("strong-password")
def _(s):
    s.F("rect", x=40, y=120, width=432, height=172, rx=44, fill=LIGHT)
    for i in range(6):
        dot(s, 100 + i * 62, 206, 20, DARK)
    for i in range(4):
        s.F("rect", x=60 + i * 104, y=340, width=92, height=34, rx=17, fill=A1 if i < 3 else MID)
    s.F("circle", cx=420, cy=410, r=38, fill=A2)
    s.M("M402 410 L416 424 L440 394", LIGHT, 12)


@reg("hacker")
def _(s):
    person_hood(s, 256, 220, 0.9)
    s.F("rect", x=130, y=370, width=252, height=100, rx=14, fill=MID)
    s.F("rect", outline=False, x=146, y=384, width=220, height=60, rx=8, fill=DARK)
    s.M("M170 410 H230 M170 430 H290", A2L, 8)
    s.F("path", d="M110 470 H402 L420 490 H92Z", fill=MID)


@reg("computer-virus")
def _(s):
    screen(s, 50, 90, 412, 300, DARK, A1L, 28, 20)
    s.F("path", d="M226 390 H286 L300 440 H212Z", fill=MID)
    for a in range(0, 360, 45):
        x1, y1 = arc_pt(256, 240, 60, a)
        x2, y2 = arc_pt(256, 240, 90, a)
        s.T(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DARK, 8)
        s.F("circle", outline=False, cx=f"{x2:.0f}", cy=f"{y2:.0f}", r=12, fill=A2)
    s.F("circle", cx=256, cy=240, r=64, fill=A2)
    dot(s, 236, 228, 9, DARK)
    dot(s, 276, 228, 9, DARK)
    s.M("M236 264 C250 250 262 250 276 264", DARK, 8)


@reg("phishing")
def _(s):
    s.F("rect", x=40, y=250, width=320, height=210, rx=24, fill=LIGHT)
    s.F("path", outline=False, d="M54 268 L200 380 L346 268", fill="none", stroke=A1, stroke_width="14", stroke_linecap="round", stroke_linejoin="round")
    s.T("M400 30 V250 C400 330 320 330 330 260", DARK, 16)
    s.F("polygon", points="330,260 306,282 342,288", fill=DARK)
    s.F("circle", cx=400, cy=30, r=16, fill=A2)
    s.F("circle", cx=440, cy=360, r=40, fill=A2)
    txt(s, "!", 440, 360, 24, 50, DARK)


@reg("firewall")
def _(s):
    s.F("rect", x=60, y=200, width=392, height=240, rx=14, fill=A1D)
    for r in range(3):
        for c in range(4):
            x = 60 + c * 100 - (50 if r % 2 else 0)
            x0, x1 = max(x, 60), min(x + 94, 452)
            if x1 - x0 > 8:
                s.F("rect", outline=False, x=x0, y=212 + r * 76, width=x1 - x0, height=64, rx=8, fill=A1 if (r + c) % 2 else A1L)
    s.F("path", d="M256 40 C300 100 360 130 340 210 C330 250 300 260 256 260 C212 260 182 250 172 210 C152 130 212 100 256 40Z", fill=A2)
    s.F("path", outline=False, d="M256 120 C276 150 300 170 292 210 C286 232 266 238 256 238 C246 238 226 232 220 210 C212 170 236 150 256 120Z", fill=A2L)


@reg("encryption")
def _(s):
    lock(s, 200, 280, 0.9, A2)
    for i, b in enumerate("1010"):
        s.F("rect", x=340, y=90 + i * 90, width=100, height=70, rx=18, fill=A1)
        txt(s, b, 390, 125 + i * 90, 36, 44, LIGHT)
    s.M("M312 330 H340", MID, 10)


@reg("two-factor-authentication")
def _(s):
    s.F("rect", x=60, y=60, width=190, height=360, rx=36, fill=DARK)
    s.F("rect", outline=False, x=76, y=96, width=158, height=290, rx=16, fill=A1L)
    txt(s, "482", 155, 190, 120, 50, A1D)
    s.F("rect", outline=False, x=96, y=260, width=118, height=14, rx=7, fill=A1)
    s.F("rect", outline=False, x=96, y=300, width=80, height=14, rx=7, fill=A1, fill_opacity="0.6")
    s.F("path", d="M360 150 L460 190 V290 C460 350 410 390 360 410 C310 390 260 350 260 290 V190Z", fill=A1)
    s.M("M312 292 L350 330 L412 250", LIGHT, 20)


@reg("data-privacy")
def _(s):
    s.F("rect", x=80, y=50, width=250, height=330, rx=24, fill=LIGHT)
    for y in (110, 160, 210, 260):
        s.M(f"M120 {y} H290", MID, 12)
    s.F("path", d="M190 330 C250 270 400 270 460 330 C400 390 250 390 190 330Z", fill=A1)
    s.F("circle", cx=325, cy=330, r=40, fill=DARK)
    dot(s, 325, 330, 16, A2L)
    s.M("M190 420 L460 250", A2, 22)


@reg("scam-alert")
def _(s):
    s.F("path", d="M256 50 C268 50 278 56 284 66 L470 390 C482 412 470 440 442 440 H70 C42 440 30 412 42 390 L228 66 C234 56 244 50 256 50Z", fill=A2)
    s.F("rect", outline=False, x=240, y=170, width=32, height=140, rx=16, fill=DARK)
    dot(s, 256, 366, 22, DARK)


# ================================================================ ai-robots
@reg("artificial-intelligence")
def _(s):
    s.F("path", d="M256 70 C150 60 90 150 110 240 C100 290 130 330 170 340 V400 H340 V340 C400 320 430 250 410 190 C400 110 340 60 256 70Z", fill=A1L)
    s.M("M256 120 V330 M256 190 H330 M256 250 H190 M256 300 H320", A1D, 10)
    for x, y in ((330, 190), (190, 250), (320, 300), (256, 120)):
        s.F("circle", cx=x, cy=y, r=20, fill=A2)
    s.F("rect", x=180, y=400, width=152, height=60, rx=16, fill=A1)
    txt(s, "AI", 256, 430, 80, 36, LIGHT)


@reg("ai-chip")
def _(s):
    s.F("rect", x=110, y=110, width=292, height=292, rx=36, fill=A1)
    for i in range(5):
        s.F("rect", x=136 + i * 56, y=60, width=24, height=48, rx=8, fill=MID)
        s.F("rect", x=136 + i * 56, y=404, width=24, height=48, rx=8, fill=MID)
        s.F("rect", x=60, y=136 + i * 56, width=48, height=24, rx=8, fill=MID)
        s.F("rect", x=404, y=136 + i * 56, width=48, height=24, rx=8, fill=MID)
    s.F("rect", outline=False, x=160, y=160, width=192, height=192, rx=24, fill=DARK)
    txt(s, "AI", 256, 256, 120, 90, A2L)


@reg("chatbot")
def _(s):
    s.F("path", d="M80 90 H432 C456 90 472 106 472 130 V320 C472 344 456 360 432 360 H260 L170 440 V360 H80 C56 360 40 344 40 320 V130 C40 106 56 90 80 90Z", fill=A1)
    s.F("rect", outline=False, x=150, y=160, width=212, height=140, rx=40, fill=LIGHT)
    s.open("part-eye-left", "206 230")
    s.F("circle", outline=False, cx=206, cy=230, r=20, fill=DARK)
    s.close()
    s.open("part-eye-right", "306 230")
    s.F("circle", outline=False, cx=306, cy=230, r=20, fill=DARK)
    s.close()
    s.T("M256 160 V130", DARK, 8)
    s.F("circle", cx=256, cy=118, r=14, fill=A2)
    s.M("M226 274 H286", A1D, 8)


@reg("machine-learning")
def _(s):
    s.F("rect", x=40, y=70, width=250, height=190, rx=20, fill=LIGHT)
    s.M("M70 220 L120 170 L170 200 L220 130 L262 100", A1, 12)
    for x, y in ((70, 220), (170, 200), (262, 100)):
        s.F("circle", cx=x, cy=y, r=14, fill=A2)
    gx, gy = 340, 330
    s.F("circle", cx=gx, cy=gy, r=112, fill=A1)
    for a in range(0, 360, 45):
        x, y = arc_pt(gx, gy, 112, a)
        s.F("rect", outline=False, x=x - 18, y=y - 18, width=36, height=36, rx=8, fill=A1, transform=f"rotate({a} {x:.0f} {y:.0f})")
    s.F("circle", outline=False, cx=gx, cy=gy, r=60, fill=A1L)
    s.F("circle", cx=gx, cy=gy, r=24, fill=A2)
    arrow(s, 150, 340, 230, 340, A2, 14, 36)


@reg("neural-network")
def _(s):
    layers = [[130, 256, 382], [90, 190, 322, 422], [190, 322], ]
    xs = [90, 230, 370]
    cols = [A1, A2, A1D]
    layers = [[140, 256, 372], [90, 190, 322, 422], [200, 312]]
    for li in range(2):
        for y1 in layers[li]:
            for y2 in layers[li + 1]:
                s.M(f"M{xs[li] + 14} {y1} L{xs[li + 1] - 14} {y2}", MID, 5)
    for li, ys in enumerate(layers):
        for y in ys:
            s.F("circle", cx=xs[li], cy=y, r=34, fill=cols[li])
    s.M("M404 200 H460 M404 312 H460", MID, 5)


@reg("robot")
def _(s):
    s.T("M256 100 V60", DARK, 12)
    s.F("circle", cx=256, cy=50, r=22, fill=A2)
    s.F("rect", x=110, y=100, width=292, height=210, rx=60, fill=A1)
    s.F("rect", outline=False, x=140, y=140, width=232, height=110, rx=44, fill=DARK)
    s.open("part-eye-left", "206 195")
    s.F("circle", outline=False, cx=206, cy=195, r=24, fill=A1L)
    s.close()
    s.open("part-eye-right", "306 195")
    s.F("circle", outline=False, cx=306, cy=195, r=24, fill=A1L)
    s.close()
    s.M("M226 270 H286", A2L, 8)
    s.F("rect", x=70, y=360, width=372, height=100, rx=40, fill=A1D)
    s.F("circle", cx=256, cy=410, r=26, fill=A2)
    s.F("rect", x=70, y=190, width=34, height=60, rx=14, fill=MID)
    s.F("rect", x=408, y=190, width=34, height=60, rx=14, fill=MID)
    s.F("rect", x=200, y=308, width=112, height=54, rx=14, fill=MID)


@reg("robot-arm")
def _(s):
    s.F("rect", x=50, y=410, width=250, height=50, rx=16, fill=DARK)
    s.F("rect", x=100, y=330, width=100, height=90, rx=16, fill=A1D)
    s.T("M150 340 L230 160 L350 120", A1, 44)
    s.F("circle", cx=150, cy=340, r=36, fill=A2)
    s.F("circle", cx=230, cy=160, r=34, fill=A2)
    s.F("rect", x=340, y=90, width=60, height=70, rx=14, fill=A1D, transform="rotate(20 370 125)")
    s.T("M392 170 L420 220 M372 178 L384 232", DARK, 12)
    s.F("rect", x=380, y=390, width=90, height=70, rx=10, fill=A2L)


@reg("robot-vacuum")
def _(s):
    s.F("ellipse", cx=256, cy=350, rx=210, ry=56, fill=DARK, fill_opacity="0.15")
    s.F("path", d="M60 280 C60 190 160 150 256 150 C352 150 452 190 452 280 V320 C452 360 400 380 256 380 C112 380 60 360 60 320Z", fill=A1)
    s.F("ellipse", cx=256, cy=250, rx=130, ry=58, fill=A1L)
    s.F("circle", cx=256, cy=250, r=38, fill=DARK)
    dot(s, 256, 250, 12, A2)
    s.M("M120 196 C160 170 210 160 256 160", WHITE, 8)
    for x in (90, 422):
        s.T(f"M{x} 340 l{-10 if x < 256 else 10} 30", DARK, 12)


@reg("voice-assistant")
def _(s):
    s.F("rect", x=190, y=40, width=132, height=230, rx=66, fill=A1)
    s.F("rect", outline=False, x=214, y=64, width=30, height=150, rx=15, fill=A1L, fill_opacity="0.6")
    s.raw(f'<path d="M120 240 C120 340 392 340 392 240" fill="none" stroke="{INK}" stroke-width="42" stroke-linecap="round" data-outline="under"/>')
    s.raw(f'<path d="M120 240 C120 340 392 340 392 240" fill="none" stroke="{DARK}" stroke-width="22" stroke-linecap="round"/>')
    s.T("M256 316 V400 M190 420 H322", DARK, 20)
    s.M("M70 130 V190 M30 150 V170 M442 130 V190 M482 150 V170", A2, 14)


@reg("face-recognition")
def _(s):
    s.M("M60 150 V70 H140 M372 70 H452 V150 M452 362 V442 H372 M140 442 H60 V362", A1, 22)
    s.F("path", d="M256 110 C190 110 160 170 166 240 C170 310 210 370 256 370 C302 370 342 310 346 240 C352 170 322 110 256 110Z", fill=SKIN)
    s.F("path", outline=False, d="M170 200 C170 140 220 110 256 110 C300 110 346 140 342 200 C300 190 230 170 190 150Z", fill="#4A3B32")
    dot(s, 224, 240, 9, DARK)
    dot(s, 288, 240, 9, DARK)
    s.M("M232 310 C250 322 268 322 284 310", DARK, 8)
    s.M("M70 256 H442", A2, 10)


# ================================================================ programming
@reg("code")
def _(s):
    s.T("M170 140 L60 256 L170 372", A1, 40)
    s.T("M342 140 L452 256 L342 372", A1, 40)
    s.T("M290 100 L222 412", A2, 36)


@reg("code-screen")
def _(s):
    screen(s, 40, 70, 432, 340, DARK, DARK, 28, 0)
    s.F("rect", outline=False, x=40, y=70, width=432, height=50, rx=28, fill=MID)
    s.F("rect", outline=False, x=40, y=96, width=432, height=24, fill=MID)
    for x, c in ((80, A2), (116, A1L), (152, LIGHT)):
        dot(s, x, 95, 10, c)
    for y, w, x, c in ((160, 120, 70, A2), (200, 180, 100, A1L), (240, 100, 100, LIGHT), (280, 220, 100, A1L), (320, 90, 70, A2), (360, 160, 70, LIGHT)):
        s.F("rect", outline=False, x=x, y=y, width=w, height=18, rx=9, fill=c)


@reg("software-bug")
def _(s):
    s.T("M170 200 L80 150 M170 260 L60 270 M175 330 L90 400 M342 200 L432 150 M342 260 L452 270 M337 330 L422 400", DARK, 14)
    s.F("ellipse", cx=256, cy=290, rx=108, ry=140, fill=A2)
    s.F("circle", cx=256, cy=140, r=62, fill=DARK)
    s.T("M226 90 L190 40 M286 90 L322 40", DARK, 10)
    s.M("M256 160 V430", DARK, 10)
    for x, y in ((210, 260), (302, 260), (206, 340), (306, 340)):
        s.F("circle", outline=False, cx=x, cy=y, r=16, fill=DARK)
    dot(s, 236, 132, 8, A2L)
    dot(s, 276, 132, 8, A2L)


@reg("algorithm")
def _(s):
    s.F("rect", x=170, y=40, width=172, height=70, rx=35, fill=A1)
    s.T("M256 110 V150 M256 250 V290 M170 200 H90 V320 M342 200 H422 V320", DARK, 10)
    s.F("polygon", points="256,150 350,200 256,250 162,200", fill=A2)
    s.F("rect", x=170, y=290, width=172, height=70, rx=14, fill=A1L)
    s.F("rect", x=30, y=320, width=120, height=70, rx=14, fill=A1L)
    s.F("rect", x=362, y=320, width=120, height=70, rx=14, fill=A1L)
    s.T("M256 360 V400 M90 390 V420 H422 V390", DARK, 10)
    s.F("rect", x=170, y=400, width=172, height=60, rx=30, fill=A1)


@reg("binary-code")
def _(s):
    rows = ("1010", "0110", "1101", "0011")
    for r, row in enumerate(rows):
        for c, b in enumerate(row):
            x = 60 + c * 100
            y = 70 + r * 98
            s.F("rect", x=x, y=y, width=84, height=80, rx=22, fill=A1 if b == "1" else A1D if (r + c) % 2 else DARK)
            txt(s, b, x + 42, y + 40, 34, 46, A2L if b == "1" else MID)


@reg("html-tags")
def _(s):
    s.F("rect", x=40, y=130, width=432, height=252, rx=44, fill=A1)
    txt(s, "<html>", 256, 256, 360, 90, LIGHT)
    s.F("rect", outline=False, x=60, y=150, width=392, height=30, rx=15, fill=A1L, fill_opacity="0.4")


@reg("terminal-window")
def _(s):
    s.F("rect", x=40, y=70, width=432, height=372, rx=30, fill=DARK)
    s.F("path", d="M40 100 C40 82 56 70 70 70 H442 C456 70 472 82 472 100 V130 H40Z", fill=MID)
    for x, c in ((80, A2), (116, A1L), (152, LIGHT)):
        dot(s, x, 100, 10, c)
    s.M("M100 210 L170 260 L100 310", A2L, 22)
    s.M("M210 320 H340", LIGHT, 22)


@reg("app")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=96, fill=A1)
    s.F("rect", outline=False, x=84, y=84, width=344, height=130, rx=60, fill=A1L, fill_opacity="0.4")
    for r in range(2):
        for c in range(2):
            s.F("rect", outline=False, x=130 + c * 130, y=130 + r * 130, width=110, height=110, rx=30, fill=A2 if (r + c) % 2 == 0 else LIGHT)


@reg("mobile-app")
def _(s):
    s.F("rect", x=90, y=40, width=190, height=330, rx=40, fill=DARK)
    s.F("rect", outline=False, x=106, y=74, width=158, height=262, rx=16, fill=A1L)
    for r in range(3):
        s.F("rect", outline=False, x=124, y=94 + r * 76, width=56, height=56, rx=16, fill=A2 if r == 1 else WHITE)
        s.F("rect", outline=False, x=194, y=94 + r * 76, width=56, height=56, rx=16, fill=A1)
    s.F("rect", x=250, y=250, width=190, height=190, rx=54, fill=A1)
    s.F("rect", outline=False, x=270, y=270, width=70, height=70, rx=20, fill=A2)
    s.F("rect", outline=False, x=350, y=270, width=70, height=70, rx=20, fill=LIGHT)
    s.F("rect", outline=False, x=270, y=350, width=150, height=70, rx=20, fill=A1L)


@reg("website")
def _(s):
    s.F("rect", x=40, y=70, width=432, height=372, rx=30, fill=LIGHT)
    s.F("path", d="M40 100 C40 82 56 70 70 70 H442 C456 70 472 82 472 100 V130 H40Z", fill=A1)
    for x, c in ((80, A2), (116, A1L), (152, LIGHT)):
        dot(s, x, 100, 10, c)
    s.F("rect", outline=False, x=70, y=160, width=372, height=110, rx=14, fill=A1L)
    s.F("circle", outline=False, cx=360, cy=200, r=22, fill=A2)
    s.F("path", outline=False, d="M70 270 L170 200 L250 250 L320 220 L442 270Z", fill=A1)
    for i in range(3):
        s.F("rect", outline=False, x=70 + i * 128, y=300, width=116, height=110, rx=14, fill=A1L if i != 1 else A2L)


@reg("web-browser")
def _(s):
    s.F("rect", x=40, y=70, width=432, height=372, rx=30, fill=LIGHT)
    s.F("path", d="M40 100 C40 82 56 70 70 70 H442 C456 70 472 82 472 100 V150 H40Z", fill=A1D)
    s.F("rect", outline=False, x=140, y=96, width=290, height=34, rx=17, fill=LIGHT)
    s.M("M70 112 L90 100 M70 112 L90 124 M120 112 H112", LIGHT, 8)
    globe(s, 256, 300, 100, A1, A1L)


@reg("database")
def _(s):
    for y, c in ((330, A1D), (210, A1), (90, A1L)):
        s.F("path", d=f"M96 {y} V{y + 70} C96 {y + 130} 416 {y + 130} 416 {y + 70} V{y}Z", fill=c)
    for y in (90, 210, 330):
        s.F("ellipse", cx=256, cy=y, rx=160, ry=56, fill=A1L if y == 90 else A1)
    s.F("ellipse", outline=False, cx=256, cy=90, rx=110, ry=26, fill=WHITE, fill_opacity="0.5")
    for y in (160, 280, 400):
        dot(s, 140, y + 20, 8, A2L)
        dot(s, 170, y + 26, 8, LIGHT)


@reg("api")
def _(s):
    s.F("rect", x=40, y=170, width=170, height=172, rx=30, fill=A1)
    s.F("circle", cx=230, cy=256, r=34, fill=A1)
    s.F("rect", x=302, y=170, width=170, height=172, rx=30, fill=A2)
    s.F("circle", cx=282, cy=256, r=34, fill=DARK)
    s.F("circle", outline=False, cx=282, cy=256, r=14, fill=A2L)
    txt(s, "API", 125, 256, 100, 44, LIGHT)
    s.M("M350 220 H430 M350 256 H430 M350 292 H400", LIGHT, 10)


@reg("debugging")
def _(s):
    s.F("ellipse", cx=210, cy=260, rx=70, ry=90, fill=A2)
    s.F("circle", cx=210, cy=160, r=42, fill=DARK)
    s.T("M150 230 L80 200 M150 290 L70 300 M160 330 L100 380 M270 230 L330 205", DARK, 10)
    s.T("M330 330 L440 440", DARK, 30)
    s.F("circle", cx=300, cy=300, r=90, fill="#E3F3FC", fill_opacity="0.8")
    ring(s, 300, 300, 90, A1, 22)


@reg("open-source")
def _(s):
    lock(s, 256, 300, 1.15, A1, True)
    txt(s, "</>", 256, 330, 120, 56, LIGHT)


# ================================================================ smart-home
@reg("smart-home")
def _(s):
    s.F("path", d="M256 70 L450 230 V440 C450 452 442 460 430 460 H82 C70 460 62 452 62 440 V230Z", fill=A1)
    s.F("path", d="M256 40 L480 230 H32Z", fill=A2)
    s.F("rect", x=200, y=330, width=112, height=130, rx=14, fill=A1D)
    wifi(s, 256, 300, 100, LIGHT, 16)


@reg("smart-bulb")
def _(s):
    s.F("path", d="M256 50 C150 50 110 140 140 220 C158 266 196 290 196 330 H316 C316 290 354 266 372 220 C402 140 362 50 256 50Z", fill=A2L)
    s.F("path", outline=False, d="M190 120 C210 90 240 82 262 84", fill="none", stroke="#FFFFFF", stroke_width="16", stroke_linecap="round", stroke_opacity="0.8")
    s.F("rect", x=190, y=330, width=132, height=40, rx=10, fill=MID)
    s.F("rect", x=200, y=370, width=112, height=40, rx=10, fill=MID)
    s.F("rect", x=216, y=410, width=80, height=40, rx=16, fill=DARK)


@reg("smart-thermostat")
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=LIGHT)
    s.raw(f'<circle cx="256" cy="256" r="200" fill="none" stroke="{MID}" stroke-width="22"/>')
    s.F("circle", cx=256, cy=256, r=140, fill=DARK)
    txt(s, "22°", 256, 256, 150, 90, A2L)
    s.F("rect", outline=False, x=160, y=330, width=192, height=12, rx=6, fill=A1L)
    s.raw(f'<path d="M80 330 A200 200 0 0 0 432 330" fill="none" stroke="{A2}" stroke-width="22" stroke-linecap="round"/>')


@reg("smart-lock")
def _(s):
    s.F("rect", x=130, y=40, width=252, height=432, rx=44, fill=DARK)
    s.F("circle", cx=256, cy=170, r=72, fill=A1)
    s.F("circle", outline=False, cx=256, cy=170, r=30, fill=A1L)
    s.F("rect", outline=False, x=246, y=150, width=20, height=44, rx=8, fill=DARK)
    for r in range(3):
        for c in range(3):
            s.F("circle", outline=False, cx=196 + c * 60, cy=290 + r * 50, r=15, fill=MID)
    s.F("rect", outline=False, x=160, y=60, width=40, height=14, rx=7, fill=A2)


@reg("smart-plug")
def _(s):
    s.F("rect", x=130, y=110, width=252, height=252, rx=60, fill=LIGHT)
    s.F("rect", outline=False, x=160, y=140, width=192, height=40, rx=20, fill=A1L, fill_opacity="0.4")
    s.F("rect", outline=False, x=196, y=210, width=20, height=60, rx=8, fill=DARK)
    s.F("rect", outline=False, x=296, y=210, width=20, height=60, rx=8, fill=DARK)
    dot(s, 256, 310, 20, A2)
    s.F("rect", x=196, y=362, width=20, height=68, rx=6, fill=MID)
    s.F("rect", x=296, y=362, width=20, height=68, rx=6, fill=MID)


@reg("cctv-camera")
def _(s):
    s.F("rect", x=40, y=70, width=60, height=200, rx=14, fill=MID)
    s.T("M100 140 H160", DARK, 24)
    s.open(transform="rotate(18 270 220)")
    s.F("rect", x=130, y=140, width=300, height=130, rx=44, fill=A1)
    s.F("rect", outline=False, x=150, y=156, width=180, height=18, rx=9, fill=A1L, fill_opacity="0.6")
    s.F("circle", cx=420, cy=205, r=56, fill=DARK)
    s.F("circle", cx=420, cy=205, r=32, fill=A1L)
    dot(s, 420, 205, 12, A2)
    s.close()


@reg("video-doorbell")
def _(s):
    s.F("rect", x=170, y=50, width=172, height=412, rx=60, fill=A1D)
    s.F("circle", cx=256, cy=150, r=58, fill=DARK)
    s.F("circle", cx=256, cy=150, r=34, fill=A1L)
    dot(s, 256, 150, 12, A2)
    s.F("circle", cx=256, cy=350, r=48, fill=LIGHT)
    s.F("circle", outline=False, cx=256, cy=350, r=24, fill=A2)
    s.M("M390 250 C410 270 410 310 390 330 M420 230 C455 270 455 310 420 350", A2, 12)


@reg("smart-tv")
def _(s):
    screen(s, 30, 80, 452, 290, DARK, A1L, 28, 18)
    s.F("path", outline=False, d="M60 130 L220 130 L60 300Z", fill=WHITE, fill_opacity="0.35")
    s.F("path", d="M226 370 H286 L300 410 H212Z", fill=MID)
    s.F("rect", x=140, y=406, width=232, height=30, rx=14, fill=MID)
    wifi(s, 256, 280, 70, A1D, 12)


# ================================================================ telecom
@reg("mobile-tower")
def _(s):
    s.T("M256 160 L170 460 M256 160 L342 460 M200 330 H312 M220 250 H292 M184 400 H328", DARK, 16)
    s.F("circle", cx=256, cy=130, r=34, fill=A2)
    waves(s, 256, 130, 130, A1, 16, 3, -140, -40)
    waves(s, 256, 130, 130, A1, 16, 3, 40, 140)


@reg("sim-card")
def _(s):
    s.F("path", d="M150 50 H320 L400 130 V440 C400 456 388 464 374 464 H138 C122 464 112 456 112 440 V70 C112 58 124 50 150 50Z", fill=A1)
    s.F("rect", x=170, y=170, width=172, height=150, rx=20, fill=A2L)
    s.M("M170 218 H342 M170 268 H342 M226 170 V320 M286 170 V320", A2, 8)


@reg("satellite-phone")
def _(s):
    s.F("rect", x=150, y=150, width=190, height=312, rx=40, fill=DARK)
    s.F("rect", outline=False, x=170, y=180, width=150, height=90, rx=12, fill=A1L)
    for r in range(3):
        for c in range(3):
            s.F("circle", outline=False, cx=196 + c * 50, cy=312 + r * 44, r=14, fill=MID)
    s.T("M330 170 L430 70", DARK, 20)
    s.F("circle", cx=440, cy=60, r=22, fill=A2)
    s.M("M110 90 C90 130 90 170 110 210", A1, 14)


@reg("telephone-exchange")
def _(s):
    s.F("rect", x=50, y=100, width=412, height=300, rx=30, fill=A1D)
    for r in range(3):
        for c in range(6):
            s.F("circle", cx=100 + c * 62, cy=160 + r * 60, r=18, fill=DARK)
            dot(s, 100 + c * 62, 160 + r * 60, 8, MID)
    s.T("M100 160 C130 230 200 200 224 280 M286 220 C330 300 380 250 410 340", A2, 12)
    s.F("rect", x=70, y=340, width=372, height=40, rx=14, fill=DARK)


@reg("qr-code")
def _(s):
    s.F("rect", x=60, y=60, width=392, height=392, rx=36, fill=LIGHT)
    for x, y in ((90, 90), (320, 90), (90, 320)):
        s.F("rect", outline=False, x=x, y=y, width=102, height=102, rx=14, fill=DARK)
        s.F("rect", outline=False, x=x + 20, y=y + 20, width=62, height=62, rx=8, fill=LIGHT)
        s.F("rect", outline=False, x=x + 34, y=y + 34, width=34, height=34, rx=6, fill=DARK)
    import random
    rnd = random.Random(7)
    for r in range(8):
        for c in range(8):
            x, y = 214 + c * 26, 214 + r * 26
            if x > 440 or y > 440:
                continue
            if rnd.random() < 0.5:
                s.F("rect", outline=False, x=x, y=y, width=22, height=22, rx=4, fill=DARK if rnd.random() < 0.7 else A1)
    for r in range(3):
        for c in range(3):
            if rnd.random() < 0.6:
                s.F("rect", outline=False, x=214 + c * 26, y=90 + r * 26, width=22, height=22, rx=4, fill=DARK)


@reg("contactless-symbol")
def _(s):
    s.F("rect", x=40, y=110, width=432, height=292, rx=50, fill=A1)
    s.F("rect", outline=False, x=60, y=130, width=392, height=50, rx=24, fill=A1L, fill_opacity="0.4")
    for i, r in enumerate((60, 110, 160)):
        x0, y0 = arc_pt(150, 256, r, -50)
        x1, y1 = arc_pt(150, 256, r, 50)
        s.raw(f'<path d="M{x0 + 90:.0f} {y0:.0f} A{r} {r} 0 0 1 {x1 + 90:.0f} {y1:.0f}" fill="none" stroke="{LIGHT}" stroke-width="22" stroke-linecap="round"/>')
    s.F("rect", outline=False, x=60, y=330, width=90, height=14, rx=7, fill=A2)


if __name__ == "__main__":
    run("technology", D, sys.argv[1:] or None)
