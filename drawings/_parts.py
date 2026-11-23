"""Reusable themed parts for concept scenes (style B, outline marks via draw_lib).

Every part draws in the normal 512 x 512 space, centred on (256, 256). Put it anywhere with
place(s, part, x, y, scale, **kw). Colours are the themed roles from palette.json, plus skin and
hair for people (the only non-theme colours allowed in themed scenes).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from draw_lib import C, INK, THEME, arc_pt, head, star_pts  # noqa: E402

A1, A2 = THEME["accent"], THEME["accent-2"]
A1L, A2L = THEME["accent-light"], THEME["accent-2-light"]
A1D = "#2C6BD6"
LIGHT, MID, DARK = THEME["light"], THEME["mid"], THEME["dark"]
SKIN, HAIR = C["skin"], "#4A3B32"


def place(s, part, x=256, y=256, sc=1.0, rot=0, flip=False, **kw):
    tf = f"translate({x} {y})" + (f" rotate({rot})" if rot else "") + f" scale({-sc if flip else sc} {sc}) translate(-256 -256)"
    s.open(transform=tf)
    part(s, **kw)
    s.close()


# ---------------------------------------------------------------- objects
def bulb(s, glow=True, color=A2, lit=True):
    if glow:
        s.open("part-glow", "256 210")
        for a in range(-150, 31, 30):
            x1, y1 = arc_pt(256, 210, 150, a); x2, y2 = arc_pt(256, 210, 194, a)
            s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", A2 if lit else MID, 22)
        s.close()
    s.F("path", d="M256 90 C186 90 136 142 136 206 C136 254 162 284 186 308 C204 326 210 344 210 360 L302 360 "
                  "C302 344 308 326 326 308 C350 284 376 254 376 206 C376 142 326 90 256 90Z", fill=color if lit else MID)
    s.F("path", outline=False, d="M180 196 C184 160 206 134 236 126 C210 152 198 178 196 212 Z", fill=A2L if lit else LIGHT)
    s.F("rect", x=206, y=360, width=100, height=30, rx=10, fill=MID)
    s.F("rect", x=212, y=390, width=88, height=28, rx=10, fill=DARK)
    s.F("rect", x=232, y=418, width=48, height=22, rx=10, fill=MID)


def brain(s, color=A2L, fold=A2):
    left = ("M252 104 C220 78 162 86 150 136 C102 138 76 190 98 232 C66 262 78 322 128 334 C138 384 196 404 238 382 "
            "C246 396 252 400 252 400 Z")
    s.F("path", d=left, fill=color)
    s.F("path", d=left, fill=color, transform="translate(512 0) scale(-1 1)")
    s.M("M210 130 C190 170 220 190 200 220 M140 200 C170 210 180 240 160 270 M230 250 C200 270 210 310 180 330 "
        "M302 130 C322 170 292 190 312 220 M372 200 C342 210 332 240 352 270 M282 250 C312 270 302 310 332 330", fold, 10)
    s.T("M236 400 C236 430 250 450 262 470", fold, 22)


def gear(s, color=A1, r=150, teeth=10, hole=LIGHT):
    pts = []
    for i in range(teeth):
        base = i * 360 / teeth
        w = 360 / teeth / 4
        for da, rr in ((-w * 1.3, r * 0.8), (-w * 0.8, r), (w * 0.8, r), (w * 1.3, r * 0.8)):
            x, y = arc_pt(256, 256, rr, base + da)
            pts.append(f"{x:.1f},{y:.1f}")
    s.F("polygon", points=" ".join(pts), fill=color)
    s.F("circle", cx=256, cy=256, r=r * 0.32, fill=hole)


def mountain(s, color=A1, snow=LIGHT, peak=True):
    s.F("polygon", points="40,440 230,120 300,230 340,180 472,440", fill=color)
    if peak:
        s.F("polygon", points="230,120 278,200 252,190 230,214 208,190 186,196", fill=snow)
    s.F("polygon", outline=False, points="230,120 186,196 120,320 210,240", fill=A1L)


def flag(s, color=A2):
    s.T("M200 460 V80", DARK, 14)
    s.F("path", d="M206 90 C260 70 300 120 360 100 V200 C300 220 260 170 206 190 Z", fill=color)


def trophy(s):
    s.T("M150 150 C80 150 84 250 170 262", A2, 22)
    s.T("M362 150 C432 150 428 250 342 262", A2, 22)
    s.F("path", d="M140 110 H372 V170 C372 250 320 300 256 300 C192 300 140 250 140 170 Z", fill=A2)
    s.F("path", outline=False, d="M164 130 H196 V176 C196 220 214 250 236 266 C190 260 164 220 164 176 Z", fill=A2L)
    s.F("rect", x=236, y=298, width=40, height=54, fill=A2)
    s.F("path", d="M190 352 H322 L336 392 H176 Z", fill=A2)
    s.F("rect", x=150, y=392, width=212, height=50, rx=10, fill=A1)
    s.F("polygon", points=star_pts(256, 190, 40, 17, 5), fill=LIGHT)


def target(s, arrow=True):
    for r, c in ((200, A1), (150, LIGHT), (100, A1), (50, A2)):
        s.F("circle", cx=256, cy=256, r=r, fill=c)
    if arrow:
        s.T("M256 256 L420 92", DARK, 14)
        s.F("polygon", points="400,84 452,60 428,112", fill=A2)
        s.F("polygon", points="420,92 450,40 470,60 444,112", fill=A2)


def ladder(s, rungs=6, color=A2):
    s.T("M170 470 L210 50", color, 22); s.T("M342 470 L302 50", color, 22)
    for i in range(rungs):
        y = 430 - i * 66
        k = (470 - y) / 420
        s.T(f"M{170 + 40 * k:.0f} {y} H{342 - 40 * k:.0f}", color, 16)


def stairs(s, n=5, color=A1):
    w, h = 340 / n, 300 / n
    pts = [(86, 440)]
    for i in range(n):
        pts += [(86 + i * w, 440 - (i + 1) * h), (86 + (i + 1) * w, 440 - (i + 1) * h)]
    pts.append((426, 440))
    s.F("polygon", points=" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill=color)


def door(s, open_=True):
    s.F("rect", x=150, y=80, width=212, height=370, rx=8, fill=DARK)
    s.F("rect", x=168, y=98, width=176, height=352, fill=A2L if open_ else A1)
    if open_:
        s.F("polygon", points="168,98 250,128 250,430 168,450", fill=A1)
        s.F("circle", cx=232, cy=280, r=9, fill=LIGHT)
        s.F("polygon", outline=False, points="210,450 344,450 420,500 120,500", fill=A2L)
    else:
        s.F("circle", cx=320, cy=280, r=10, fill=LIGHT)


def clock(s, color=A1, h=60, m=0):
    s.F("circle", cx=256, cy=256, r=190, fill=color)
    s.F("circle", cx=256, cy=256, r=150, fill=LIGHT)
    for i in range(12):
        x1, y1 = arc_pt(256, 256, 134, i * 30); x2, y2 = arc_pt(256, 256, 118, i * 30)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", DARK, 8)
    hx, hy = arc_pt(256, 256, 70, h - 90); mx, my = arc_pt(256, 256, 110, m * 6 - 90)
    s.open("part-hand-hour", "256 256"); s.M(f"M256 256 L{hx:.0f} {hy:.0f}", DARK, 16); s.close()
    s.open("part-hand-minute", "256 256"); s.M(f"M256 256 L{mx:.0f} {my:.0f}", DARK, 10); s.close()
    s.F("circle", cx=256, cy=256, r=12, fill=A2)


PUZZLE = ("M120 160 H210 C200 120 230 96 256 96 C282 96 312 120 302 160 H392 V250 C432 240 456 270 456 296 "
          "C456 322 432 352 392 342 V432 H120 Z")


def puzzle(s, color=A1):
    s.F("path", d=PUZZLE, fill=color)


def magnifier(s, color=A1):
    s.T("M330 330 L440 440", DARK, 44)
    s.F("circle", cx=230, cy=230, r=140, fill=color)
    s.F("circle", cx=230, cy=230, r=104, fill=LIGHT)
    s.F("path", outline=False, d="M170 190 C180 160 206 144 236 142 C208 162 194 180 188 214Z", fill=A1L)


def book(s, color=A1):
    s.F("path", d="M256 140 C210 110 130 104 70 120 V400 C130 384 210 390 256 420 Z", fill=LIGHT)
    s.F("path", d="M256 140 C302 110 382 104 442 120 V400 C382 384 302 390 256 420 Z", fill=LIGHT)
    s.F("path", d="M60 130 V420 C140 400 210 410 256 440 C302 410 372 400 452 420 V130 L442 120 V400 C382 384 302 390 256 420 "
                  "C210 390 130 384 70 400 V120 Z", fill=color)
    for y in (180, 220, 260, 300):
        s.M(f"M110 {y} C160 {y - 8} 200 {y - 2} 230 {y + 10} M282 {y + 10} C312 {y - 2} 352 {y - 8} 402 {y}", MID, 8)


def bars(s, heights=(120, 190, 260, 330), color=A1, arrow=True):
    for i, h in enumerate(heights):
        s.F("rect", x=96 + i * 86, y=440 - h, width=62, height=h, rx=8, fill=color if i < len(heights) - 1 else A2)
    if arrow:
        s.M("M90 330 L200 250 L280 280 L410 130 " + head(410, 130, ang_(280, 280, 410, 130), 64), DARK, 18)


def ang_(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def sprout(s, leaves=2, pot=True, color=A1):
    if pot:
        s.F("path", d="M156 330 H356 L332 450 H180 Z", fill=A2)
        s.F("rect", x=140, y=310, width=232, height=40, rx=10, fill=A2)
    s.T("M256 320 C256 260 250 220 256 160", "#4CB963", 14)
    s.F("path", d="M256 220 C200 230 160 200 150 150 C206 140 246 170 256 220Z", fill="#4CB963")
    if leaves > 1:
        s.F("path", d="M256 180 C300 190 350 160 362 110 C306 100 266 130 256 180Z", fill="#4CB963")


def rocket(s):
    s.open("part-flame", "256 420")
    s.F("path", d="M226 392 Q256 500 286 392 Z", fill=A2)
    s.F("path", outline=False, d="M240 392 Q256 456 272 392 Z", fill=A2L)
    s.close()
    s.F("path", d="M210 330 L160 392 L210 384 Z", fill=A2)
    s.F("path", d="M302 330 L352 392 L302 384 Z", fill=A2)
    s.F("path", d="M256 60 C312 110 316 220 302 390 L210 390 C196 220 200 110 256 60Z", fill=LIGHT)
    s.F("path", d="M256 60 C286 86 300 116 306 146 L206 146 C212 116 226 86 256 60Z", fill=A1)
    s.F("circle", cx=256, cy=230, r=36, fill=MID)
    s.F("circle", cx=256, cy=230, r=24, fill=A1L)


def road(s, color=MID):
    s.F("polygon", points="200,90 312,90 470,480 42,480", fill=color)
    s.M("M256 120 V170 M256 220 V290 M256 350 V460", LIGHT, 14)


def signpost(s):
    s.T("M256 470 V90", DARK, 22)
    s.F("polygon", points="256,120 400,120 440,160 400,200 256,200", fill=A1)
    s.F("polygon", points="256,230 112,230 72,270 112,310 256,310", fill=A2)


def scales(s):
    s.T("M256 440 V120 M120 150 H392", DARK, 16)
    s.F("rect", x=196, y=430, width=120, height=30, rx=8, fill=A1)
    for x in (120, 392):
        s.M(f"M{x} 150 L{x - 60} 300 M{x} 150 L{x + 60} 300", DARK, 6)
        s.F("path", d=f"M{x - 80} 300 H{x + 80} C{x + 70} 350 {x - 70} 350 {x - 80} 300Z", fill=A2)
    s.F("circle", cx=256, cy=120, r=18, fill=A2)


def knight(s, color=A1):
    s.F("path", d="M150 440 H362 V400 H330 C330 330 360 300 350 230 C340 150 280 100 210 110 L200 80 L180 120 C150 140 120 190 110 230 "
                  "C104 250 130 270 150 256 C170 244 190 240 210 240 C180 290 160 340 180 400 H150 Z", fill=color)
    s.F("circle", cx=200, cy=170, r=12, fill=LIGHT)
    s.F("rect", x=130, y=440, width=252, height=30, rx=8, fill=color)


def cloud(s, color=LIGHT):
    for cx, cy, r in ((170, 280, 80), (250, 230, 100), (340, 270, 86), (260, 310, 80)):
        s.F("circle", cx=cx, cy=cy, r=r, fill=color)
    s.F("rect", outline=False, x=120, y=270, width=260, height=90, rx=40, fill=color)


def thought(s, color=LIGHT):
    cloud(s, color)
    s.F("circle", cx=140, cy=400, r=24, fill=color)
    s.F("circle", cx=100, cy=450, r=14, fill=color)


def star(s, color=A2, r=190):
    s.F("polygon", points=star_pts(256, 266, r, r * 0.44, 5), fill=color)
    s.F("polygon", outline=False, points=star_pts(256 - r * 0.18, 266 - r * 0.12, r * 0.22, r * 0.1, 5), fill=A2L)


def check_badge(s, ok=True):
    s.F("circle", cx=256, cy=256, r=190, fill=A1 if ok else A2)
    s.T("M170 262 L232 322 L350 196" if ok else "M180 180 L332 332 M332 180 L180 332", LIGHT, 44)


def qmark(s, color=A1):
    s.T("M166 186 C166 116 214 82 262 82 C318 82 352 120 352 170 C352 222 304 240 278 264 C264 278 256 294 256 318", color, 60)
    s.F("circle", cx=256, cy=410, r=37, fill=color)


def hourglass(s):
    s.F("rect", x=140, y=70, width=232, height=36, rx=10, fill=A1)
    s.F("rect", x=140, y=406, width=232, height=36, rx=10, fill=A1)
    s.F("path", d="M170 106 H342 C342 200 280 230 280 256 C280 282 342 312 342 406 H170 C170 312 232 282 232 256 C232 230 170 200 170 106Z", fill=LIGHT)
    s.F("path", outline=False, d="M200 150 H312 C300 200 262 220 256 250 C250 220 212 200 200 150Z", fill=A2)
    s.F("path", outline=False, d="M190 396 C200 340 240 320 256 300 C272 320 312 340 322 396Z", fill=A2)


def dice(s):
    s.F("rect", x=110, y=110, width=292, height=292, rx=50, fill=LIGHT)
    for x, y in ((180, 180), (256, 256), (332, 332), (332, 180), (180, 332)):
        s.F("circle", outline=False, cx=x, cy=y, r=26, fill=DARK)


def dumbbell(s, color=A1):
    s.T("M140 256 H372", DARK, 24)
    for x in (100, 372):
        s.F("rect", x=x, y=170, width=40, height=172, rx=12, fill=color)
    for x in (60, 412):
        s.F("rect", x=x, y=196, width=40, height=120, rx=12, fill=color)


def medal(s, color=A2):
    s.F("polygon", points="196,60 256,200 316,60 360,60 290,230 222,230 152,60", fill=A1)
    s.F("circle", cx=256, cy=320, r=120, fill=color)
    s.F("circle", cx=256, cy=320, r=84, fill=A2L)
    s.F("polygon", points=star_pts(256, 326, 54, 23, 5), fill=color)


def finish_banner(s):
    s.T("M80 470 V90 M432 470 V90", DARK, 16)
    for r in range(3):
        for c in range(8):
            col = DARK if (r + c) % 2 == 0 else LIGHT
            s.F("rect", outline=False, x=88 + c * 42, y=100 + r * 40, width=42, height=40, fill=col)
    s.F("rect", x=88, y=100, width=336, height=120, fill="none")


def wall(s, color=A2, broken=False):
    for r in range(5):
        off = 0 if r % 2 == 0 else 50
        for c in range(-1, 4):
            x = 90 + c * 100 + off
            if x < 70 or x > 360:
                continue
            if broken and 1 <= r <= 3 and 160 <= x <= 270:
                continue
            s.F("rect", x=x, y=120 + r * 60, width=94, height=54, rx=6, fill=color)


def key(s, color=A2):
    s.F("circle", cx=170, cy=256, r=90, fill=color)
    s.F("circle", cx=150, cy=256, r=34, fill=LIGHT)
    s.F("path", d="M250 236 H440 V276 H420 V320 H384 V276 H360 V310 H326 V276 H250Z", fill=color)


def heart(s, color=A2):
    s.F("path", d="M256 432 C140 352 68 282 68 190 C68 128 114 84 172 84 C210 84 240 104 256 134 C272 104 302 84 340 84 "
                  "C398 84 444 128 444 190 C444 282 372 352 256 432Z", fill=color)


def maze(s, simple=False):
    s.F("rect", x=80, y=80, width=352, height=352, rx=24, fill=LIGHT)
    if simple:
        s.M("M130 256 H382", A1, 22)
    else:
        s.M("M130 130 H300 M380 130 V250 M130 200 V382 H250 M200 200 H320 V320 M250 260 V320 M380 320 V382 H300", A1, 18)
        s.M("M130 160 H190 V230 H280 V290 H350 V350", A2, 10)


# ---------------------------------------------------------------- people
def person(s, shirt=A1, pose="stand", hair=HAIR, skin=SKIN, pants=DARK):
    """A friendly generic person, about 360 px tall, feet at y=470."""
    # legs
    if pose == "walk":
        s.T("M236 360 L200 466", pants, 34); s.T("M276 360 L312 466", pants, 34)
    elif pose == "sit":
        s.T("M220 350 H310 V460", pants, 34); s.T("M240 350 H330 V460", pants, 34)
    else:
        s.T("M236 360 V462", pants, 34); s.T("M276 360 V462", pants, 34)
    # arms behind/in front depending on pose
    arms = {
        "stand": ("M200 230 C180 280 176 320 180 360", "M312 230 C332 280 336 320 332 360"),
        "walk": ("M200 230 C176 270 160 300 150 330", "M312 230 C336 270 352 300 362 330"),
        "cheer": ("M204 230 C170 190 160 140 150 90", "M308 230 C342 190 352 140 362 90"),
        "think": ("M200 230 C180 280 176 320 180 360", "M312 230 C350 260 320 200 280 170"),
        "point": ("M200 230 C180 280 176 320 180 360", "M312 230 C360 220 400 200 440 180"),
        "sad": ("M204 240 C196 290 200 330 210 360", "M308 240 C316 290 312 330 302 360"),
        "sit": ("M200 230 C190 280 210 320 240 330", "M312 230 C322 280 302 320 272 330"),
        "carry": ("M204 230 C180 200 190 160 220 140", "M308 230 C332 200 322 160 292 140"),
    }[pose]
    s.T(arms[0], skin, 26)
    s.F("path", d="M196 220 C196 196 214 184 236 184 H276 C298 184 316 196 316 220 V370 H196 Z", fill=shirt)
    s.T(arms[1], skin, 26)
    # head
    hy = 140 if pose != "sad" else 150
    s.F("rect", outline=False, x=240, y=hy + 20, width=32, height=30, fill=skin)
    s.F("circle", cx=256, cy=hy - 10, r=50, fill=skin)
    s.F("path", d=f"M206 {hy - 14} C200 {hy - 70} 230 {hy - 66} 256 {hy - 64} C290 {hy - 66} 316 {hy - 56} 306 {hy - 14} "
                  f"C296 {hy - 40} 270 {hy - 44} 256 {hy - 40} C236 {hy - 44} 214 {hy - 36} 206 {hy - 14}Z", fill=hair)
    if pose == "sad":
        s.M(f"M236 {hy - 2} V{hy + 2} M276 {hy - 2} V{hy + 2} M240 {hy + 26} Q256 {hy + 16} 272 {hy + 26}", INK, 7)
    else:
        s.open("part-eye-left", f"238 {hy - 6}"); s.M(f"M238 {hy - 8} V{hy - 4}", INK, 9); s.close()
        s.open("part-eye-right", f"274 {hy - 6}"); s.M(f"M274 {hy - 8} V{hy - 4}", INK, 9); s.close()
        s.M(f"M240 {hy + 14} Q256 {hy + 26} 272 {hy + 14}", INK, 7)


def sparkle(s, x, y, r, color=A2):
    s.F("polygon", points=star_pts(x, y, r, r * 0.32, 4), fill=color)


def arrow_up(s, color=A1):
    s.F("polygon", points="256,70 410,230 316,230 316,440 196,440 196,230 102,230", fill=color)


def arrow_down(s, color=A2):
    s.F("polygon", points="256,442 410,282 316,282 316,72 196,72 196,282 102,282", fill=color)
