"""More reusable themed parts (values, teamwork, time, mindsets, cause and effect). See _parts.py."""
from _parts import *  # noqa: F401,F403
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, SKIN, arc_pt, heart, person, place  # noqa: F401


def handshake(s, c1=A1, c2=A2):
    s.T("M40 300 L170 250", c1, 70, cap="butt"); s.T("M472 300 L342 250", c2, 70, cap="butt")
    s.F("path", d="M342 210 C310 196 280 204 262 220 L220 250 C240 260 260 254 280 244 L360 300 Z", fill=SKIN)
    s.F("path", d="M170 210 C210 190 250 200 280 220 L330 260 C350 276 336 304 312 292 L280 276 C300 300 290 320 266 312 "
                  "C276 336 254 350 232 336 C236 356 214 366 196 350 L150 300 Z", fill=SKIN)


def hands_heart(s, color=A2):
    place(s, heart, 256, 200, 0.5, color=color)
    s.F("path", d="M60 330 C120 300 180 330 220 380 C240 400 250 420 256 440 H60 Z", fill=SKIN)
    s.F("path", d="M452 330 C392 300 332 330 292 380 C272 400 262 420 256 440 H452 Z", fill=SKIN)


def shield(s, color=A1, check=False):
    s.F("path", d="M256 56 L424 118 V246 C424 352 352 426 256 460 C160 426 88 352 88 246 V118 Z", fill=color)
    s.F("path", outline=False, d="M256 104 L376 150 V246 C376 320 330 380 256 410 Z", fill=A1L)
    if check:
        s.T("M180 262 L236 316 L340 206", LIGHT, 36)


def padlock(s, color=A2, open_=False):
    s.T("M176 230 V170 C176 66 336 66 336 170" + (" V180" if open_ else " V230"), MID, 34)
    s.F("rect", x=120, y=230, width=272, height=220, rx=34, fill=color)
    s.F("circle", cx=256, cy=320, r=26, fill=DARK)
    s.F("rect", x=244, y=330, width=24, height=60, rx=8, fill=DARK)


def eye(s, color=A1):
    s.F("path", d="M40 256 C110 140 190 110 256 110 C322 110 402 140 472 256 C402 372 322 402 256 402 C190 402 110 372 40 256Z", fill=LIGHT)
    s.F("circle", cx=256, cy=256, r=96, fill=color)
    s.F("circle", cx=256, cy=256, r=46, fill=DARK)
    s.F("circle", outline=False, cx=226, cy=226, r=18, fill=LIGHT)


def globe(s):
    s.F("circle", cx=256, cy=256, r=200, fill=A1)
    for d in ("M150 120 C190 96 236 104 246 140 C254 172 220 182 214 214 C208 250 172 256 150 232 C126 206 102 160 150 120Z",
              "M210 268 C246 256 276 282 270 322 C264 362 246 396 226 420 C206 400 200 360 192 332 C184 300 186 276 210 268Z",
              "M300 120 C346 112 396 140 410 186 C420 224 396 236 372 226 C352 218 344 244 324 252 C298 262 284 236 290 210 C296 180 270 140 300 120Z"):
        s.F("path", d=d, fill=A2L)


def chain(s, color=A1):
    s.T("M50 256 C50 196 190 196 190 256 C190 316 50 316 50 256Z", color, 28)
    s.T("M256 186 C316 186 316 326 256 326 C196 326 196 186 256 186Z", color, 28)
    s.T("M322 256 C322 196 462 196 462 256 C462 316 322 316 322 256Z", color, 28)


def domino(s, color=LIGHT, rot=0):
    s.open(transform=f"rotate({rot} 256 416)")
    s.F("rect", x=196, y=96, width=120, height=320, rx=18, fill=color)
    s.M("M206 256 H306", DARK, 8)
    s.close()


def ripple(s):
    for r, c in ((200, A1L), (140, A1), (80, A1L)):
        s.F("ellipse", cx=256, cy=300, rx=r, ry=r * 0.4, fill=c)
    s.F("circle", cx=256, cy=180, r=30, fill=A1)


def butterfly(s, c1=A2, c2=A1):
    s.open("part-wing-left", "256 256")
    s.F("path", d="M250 250 C200 120 80 90 80 180 C80 240 150 260 250 260 Z", fill=c1)
    s.F("path", d="M250 270 C170 270 110 300 130 360 C150 410 230 380 250 290 Z", fill=c2)
    s.close()
    s.open("part-wing-right", "256 256")
    s.F("path", d="M262 250 C312 120 432 90 432 180 C432 240 362 260 262 260 Z", fill=c1)
    s.F("path", d="M262 270 C342 270 402 300 382 360 C362 410 282 380 262 290 Z", fill=c2)
    s.close()
    s.F("rect", x=242, y=170, width=28, height=200, rx=14, fill=DARK)
    s.M("M250 176 C240 140 220 120 200 110 M262 176 C272 140 292 120 312 110", DARK, 6)


def bottle(s, color=A1L):
    s.F("path", d="M216 70 H296 V150 C350 180 370 220 370 280 V430 C370 450 356 460 336 460 H176 C156 460 142 450 142 430 V280 "
                  "C142 220 162 180 216 150 Z", fill=color)
    s.F("rect", x=206, y=50, width=100, height=36, rx=10, fill=A2)


def seesaw(s, tilt=0, left=None, right=None):
    s.F("polygon", points="256,300 200,440 312,440", fill=A2)
    s.open(transform=f"rotate({tilt} 256 290)")
    s.F("rect", x=50, y=270, width=412, height=30, rx=12, fill=A1)
    for item, x in ((left, 130), (right, 382)):
        if item:
            place(s, item[0], x, 200, item[1], **(item[2] if len(item) > 2 else {}))
    s.close()


def calendar(s, mark=True):
    s.F("rect", x=80, y=100, width=352, height=340, rx=30, fill=LIGHT)
    s.F("path", d="M80 130 C80 112 94 100 112 100 H400 C418 100 432 112 432 130 V180 H80 Z", fill=A1)
    for x in (160, 352):
        s.T(f"M{x} 70 V130", DARK, 22)
    for r in range(3):
        for c in range(5):
            s.F("rect", outline=False, x=110 + c * 62, y=210 + r * 70, width=46, height=46, rx=8, fill=MID)
    if mark:
        s.T("M330 302 A36 36 0 1 1 329 302", A2, 12)


def checklist(s, done=2):
    s.F("rect", x=100, y=70, width=312, height=390, rx=24, fill=LIGHT)
    for i, y in enumerate((150, 240, 330)):
        s.F("rect", x=140, y=y - 26, width=52, height=52, rx=10, fill=A1 if i < done else LIGHT)
        if i < done:
            s.M(f"M150 {y} L162 {y + 12} L184 {y - 14}", LIGHT, 10)
        s.M(f"M220 {y} H370", MID, 16)


def cup(s, color=A2):
    s.M("M200 160 C180 120 220 100 200 60 M260 160 C240 120 280 100 260 60", MID, 12)
    s.T("M360 240 C440 240 440 340 352 340", color, 26)
    s.F("path", d="M120 200 H360 V330 C360 400 310 440 240 440 C170 440 120 400 120 330 Z", fill=color)


def sun(s, color=A2):
    s.open("part-glow", "256 256")
    for a in range(0, 360, 30):
        x1, y1 = arc_pt(256, 256, 140, a); x2, y2 = arc_pt(256, 256, 196, a)
        s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", color, 24)
    s.close()
    s.F("circle", cx=256, cy=256, r=110, fill=color)


def moon(s, color=A1L):
    s.F("path", d="M300 70 C190 90 130 180 140 280 C150 380 250 450 350 430 C250 400 200 320 210 240 C220 160 260 100 300 70Z", fill=color)


def owl(s):
    s.F("polygon", points="130,150 170,200 120,210", fill=A1)
    s.F("polygon", points="382,150 342,200 392,210", fill=A1)
    s.F("ellipse", cx=256, cy=290, rx=150, ry=170, fill=A1)
    s.F("ellipse", outline=False, cx=256, cy=330, rx=90, ry=110, fill=A1L)
    for x in (200, 312):
        s.F("circle", cx=x, cy=230, r=52, fill=LIGHT)
        s.F("circle", outline=False, cx=x, cy=234, r=24, fill=DARK)
    s.F("polygon", points="240,270 272,270 256,300", fill=A2)


def dove(s, color=LIGHT):
    s.F("path", d="M110 300 C150 260 220 250 280 270 L360 200 C380 190 400 200 396 216 L340 290 C330 360 260 400 180 380 L100 400 L140 350 Z", fill=color)
    s.F("path", d="M230 280 C210 200 240 120 300 90 C300 160 290 230 260 290 Z", fill=color)
    s.F("circle", outline=False, cx=370, cy=214, r=7, fill=DARK)
    s.F("polygon", points="392,206 430,214 394,226", fill=A2)
    s.T("M400 230 C420 260 440 270 460 266", "#4CB963", 8)


def battery(s, level=1.0, color=A1):
    s.F("rect", x=410, y=220, width=34, height=72, rx=8, fill=MID)
    s.F("rect", x=70, y=160, width=340, height=192, rx=30, fill=LIGHT)
    if level > 0:
        s.F("rect", outline=False, x=96, y=186, width=int(288 * level), height=140, rx=12, fill=color)


def group(s, shirts=(A1, A2, A1D)):
    place(s, person, 150, 290, 0.6, shirt=shirts[1])
    place(s, person, 362, 290, 0.6, shirt=shirts[2])
    place(s, person, 256, 300, 0.7, shirt=shirts[0])


def iceberg(s):
    s.F("rect", outline=False, x=24, y=200, width=464, height=288, rx=30, fill=A1)
    s.F("polygon", points="130,204 382,204 430,300 400,400 300,460 200,440 110,370 96,280", fill="#DCEFFA")
    s.F("polygon", outline=False, points="256,204 382,204 430,300 400,400 300,460 280,300", fill="#BFE0F4")
    s.F("polygon", points="170,204 210,120 240,150 276,80 310,150 342,204", fill=LIGHT)
    s.M("M24 204 H488", A1D, 8)


def crown(s, color=A2):
    s.F("polygon", points="90,380 70,150 170,250 256,120 342,250 442,150 422,380", fill=color)
    s.F("rect", x=90, y=380, width=332, height=50, rx=10, fill=color)
    for x, y in ((70, 150), (256, 120), (442, 150)):
        s.F("circle", cx=x, cy=y, r=22, fill=A1)


def megaphone(s, color=A2):
    s.T("M160 300 L190 410", DARK, 26)
    s.F("path", d="M110 200 L330 100 V400 L110 300 Z", fill=color)
    s.F("rect", x=70, y=196, width=60, height=108, rx=16, fill=A1)
    s.M("M380 200 C410 230 410 280 380 310 M420 160 C470 210 470 300 420 350", A1, 14)


def ear(s):
    s.F("path", d="M300 80 C200 70 140 150 150 230 C156 280 200 300 200 350 C200 410 250 440 290 420 C330 400 330 360 360 320 "
                  "C400 270 420 210 400 160 C380 110 340 84 300 80Z", fill=SKIN)
    s.M("M290 160 C240 160 220 200 240 240 C260 270 300 260 300 300", "#D9A07A", 14)


def gift(s, color=A2):
    s.T("M256 170 C200 90 150 130 200 170 M256 170 C312 90 362 130 312 170", A1, 18)
    s.F("rect", x=100, y=220, width=312, height=230, rx=16, fill=color)
    s.F("rect", x=80, y=170, width=352, height=70, rx=14, fill=color)
    s.F("rect", outline=False, x=232, y=170, width=48, height=280, fill=A1)


def candle(s):
    s.F("rect", x=206, y=220, width=100, height=220, rx=12, fill=A1L)
    s.T("M256 220 V190", DARK, 8)
    s.open("part-flame", "256 190")
    s.F("path", d="M256 90 C290 130 296 170 256 190 C216 170 222 130 256 90Z", fill=A2)
    s.close()


def snowball(s, r=150, color=LIGHT):
    s.F("circle", cx=256, cy=256, r=r, fill=color)
    s.F("circle", outline=False, cx=256 - r * 0.35, cy=256 - r * 0.35, r=r * 0.25, fill=A1L)
