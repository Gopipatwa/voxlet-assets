"""human-body drawings. Run: python drawings/human_body.py [ids...]

Body parts are shown on one shared front-view figure with the named part highlighted, so the
set is consistent. Organs, bones, cells and teeth are drawn as friendly anatomy icons.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, eye, shade, tint  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run, star_pts  # noqa: E402

D = {}
SKIN, SKIN_D, HAIR = C["skin"], "#E0A878", "#4A3B32"
HI = C["orange"]          # highlight colour for the named part
RED, DRED, PINK, BONE, BONE_D = "#E5484D", "#B5323A", "#F7A1B5", "#F4EBDD", "#D9C9AE"


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


# ---------------------------------------------------------------- shared body figure (front view)
ARM_L = "M192 144 C176 180 168 210 164 238 C160 262 157 284 156 300"
ARM_R = "M320 144 C336 180 344 210 348 238 C352 262 355 284 356 300"
LEG_L = "M224 296 C222 330 219 360 217 388 C215 414 214 436 214 452"
LEG_R = "M288 296 C290 330 293 360 295 388 C297 414 298 436 298 452"
TORSO = "M196 130 H316 C336 132 342 148 338 168 L328 250 C330 266 336 276 336 292 H176 C176 276 182 266 184 250 L174 168 C170 148 176 132 196 130Z"


def figure(s, back=False):
    s.T(ARM_L, SKIN, 30)
    s.T(ARM_R, SKIN, 30)
    s.T(LEG_L, SKIN, 40)
    s.T(LEG_R, SKIN, 40)
    for x in (156, 356):
        s.F("circle", cx=x, cy=314, r=18, fill=SKIN)
    s.F("ellipse", cx=208, cy=464, rx=28, ry=13, fill=SKIN)
    s.F("ellipse", cx=304, cy=464, rx=28, ry=13, fill=SKIN)
    s.F("rect", x=240, y=104, width=32, height=32, fill=SKIN)
    s.F("path", d=TORSO, fill=SKIN)
    s.F("path", d="M176 268 H336 V300 C320 304 300 304 290 300 H222 C212 304 192 304 176 300Z", fill="#6B8CC9")
    s.F("circle", cx=256, cy=70, r=42, fill=SKIN)
    s.F("path", d="M214 66 C212 20 300 20 298 66 C290 44 276 38 256 38 C236 38 222 44 214 66Z", fill=HAIR)
    if back:
        s.F("path", d="M214 70 C212 30 300 30 298 70 C292 104 220 104 214 70Z", fill=HAIR)
        s.M("M256 140 V250", SKIN_D, 6)
    else:
        s.F("circle", outline=False, cx=268, cy=238, r=4, fill=SKIN_D)


def hl_circle(x, y, r):
    return lambda s: s.F("circle", cx=x, cy=y, r=r, fill=HI)


def hl_tube(d, w):
    return lambda s: s.T(d, HI, w)


HILITE = {
    "head": lambda s: s.F("circle", cx=256, cy=70, r=46, fill=HI, fill_opacity="0.85"),
    "neck": lambda s: s.F("rect", x=236, y=102, width=40, height=34, rx=8, fill=HI),
    "shoulder": hl_circle(196, 146, 22),
    "chest": lambda s: s.F("ellipse", cx=256, cy=176, rx=58, ry=28, fill=HI),
    "stomach-area": lambda s: s.F("ellipse", cx=256, cy=228, rx=50, ry=26, fill=HI),
    "waist": lambda s: s.F("rect", x=178, y=246, width=156, height=22, rx=10, fill=HI),
    "hip": hl_circle(188, 290, 22),
    "arm": hl_tube(ARM_L, 32),
    "elbow": hl_circle(164, 236, 20),
    "forearm": hl_tube("M164 238 C160 262 157 284 156 300", 32),
    "wrist": hl_circle(156, 298, 17),
    "hand": hl_circle(156, 314, 22),
    "leg": hl_tube(LEG_L, 42),
    "thigh": hl_tube("M224 296 C222 330 219 360 217 388", 42),
    "knee": hl_circle(217, 388, 23),
    "calf-of-the-leg": hl_tube("M217 388 C215 414 214 436 214 452", 40),
    "ankle": hl_circle(214, 450, 18),
    "foot": lambda s: s.F("ellipse", cx=208, cy=464, rx=30, ry=15, fill=HI),
    "belly-button": lambda s: s.raw(f'<circle cx="268" cy="238" r="14" fill="none" stroke="{HI}" stroke-width="7"/>'),
}

D["human-body"] = lambda s: figure(s)
for _part, _hl in HILITE.items():
    D[_part] = (lambda h: lambda s: (figure(s), h(s)))(_hl)
D["back"] = lambda s: (figure(s, back=True), s.F("path", d="M196 134 H316 L328 250 H184Z", fill=HI, fill_opacity="0.85"))


# hand, foot and finger close-ups
def hand(s, hl=None, nails=False):
    s.F("path", d="M150 470 C120 400 110 330 120 280 C124 256 150 254 156 280 L170 330 V150 C170 120 206 120 206 150 V300 V110 C206 80 242 80 242 110 V300 V120 "
                  "C242 90 278 90 278 120 V300 V160 C278 132 314 132 314 160 V360 C314 420 290 450 270 470Z", fill=SKIN)
    s.M("M206 300 V290 M242 300 V290 M278 300 V290", SKIN_D, 4)
    if nails:
        for x, y in ((188, 140), (224, 100), (260, 110), (296, 150)):
            s.F("rect", x=x - 12, y=y, width=24, height=26, rx=10, fill="#F7D0C0")
    if hl == "palm":
        s.F("ellipse", cx=240, cy=380, rx=60, ry=60, fill=HI, fill_opacity="0.7")
    elif hl == "fingers":
        s.F("rect", x=168, y=110, width=148, height=120, rx=30, fill=HI, fill_opacity="0.55")
    elif hl == "thumb":
        s.F("ellipse", cx=138, cy=300, rx=26, ry=50, fill=HI, fill_opacity="0.7", transform="rotate(-15 138 300)")
    elif hl == "fingernail":
        s.raw(f'<circle cx="224" cy="114" r="28" fill="none" stroke="{HI}" stroke-width="8"/>')


def foot(s, hl=None):
    s.F("path", d="M120 140 C120 100 200 100 210 150 C220 220 230 300 330 330 C400 350 430 380 420 410 C410 440 330 450 260 440 C190 430 120 400 120 300Z", fill=SKIN)
    for x, y, r in ((330, 330, 22), (370, 340, 18), (400, 354, 16), (418, 374, 14), (424, 396, 12)):
        s.F("circle", cx=x, cy=y, r=r, fill=SKIN)
    if hl == "heel":
        s.F("circle", cx=150, cy=380, r=50, fill=HI, fill_opacity="0.7")
    elif hl == "toes":
        s.F("ellipse", cx=380, cy=360, rx=70, ry=40, fill=HI, fill_opacity="0.6")
    elif hl == "toenail":
        s.raw(f'<circle cx="330" cy="330" r="30" fill="none" stroke="{HI}" stroke-width="8"/>')


D["palm"] = lambda s: hand(s, "palm")
D["fingers"] = lambda s: hand(s, "fingers")
D["thumb"] = lambda s: hand(s, "thumb")
D["fingernail"] = lambda s: hand(s, "fingernail", nails=True)
D["heel"] = lambda s: foot(s, "heel")
D["toes"] = lambda s: foot(s, "toes")
D["toenail"] = lambda s: foot(s, "toenail")


# ---------------------------------------------------------------- face
def face(s, hl=None, beard=False, moustache=False):
    for x in (110, 402):
        s.F("ellipse", cx=x, cy=270, rx=34, ry=52, fill=SKIN)
    s.F("ellipse", cx=256, cy=270, rx=150, ry=180, fill=SKIN)
    s.F("path", d="M106 230 C96 80 416 80 406 230 C380 150 330 130 256 130 C182 130 132 150 106 230Z", fill=HAIR)
    if beard:
        s.F("path", d="M120 300 C130 420 200 460 256 460 C312 460 382 420 392 300 C370 360 330 380 256 380 C182 380 142 360 120 300Z", fill=HAIR)
    for x in (200, 312):
        s.M(f"M{x - 34} 218 Q{x} 200 {x + 34} 218", HAIR, 12)
        s.F("ellipse", cx=x, cy=258, rx=26, ry=18, fill=WHITE)
        eye(s, x, 258, 12, "left" if x < 256 else "right")
    s.T("M256 270 L240 330 H268", SKIN_D, 10)
    if moustache:
        s.F("path", d="M200 360 C220 340 250 346 256 356 C262 346 292 340 312 360 C290 366 270 362 256 368 C242 362 222 366 200 360Z", fill=HAIR)
    s.F("path", d="M210 380 Q256 410 302 380 Q256 396 210 380Z", fill=DRED)
    if hl:
        spots = {"eye": (200, 258, 46), "eyebrow": (200, 214, 42), "nose": (254, 300, 40), "mouth": (256, 388, 54), "ear": (110, 270, 50), "cheek": (180, 330, 40),
                 "chin": (256, 430, 40), "forehead": (256, 170, 60), "jaw": (360, 400, 50), "lips": (256, 388, 54)}
        x, y, r = spots[hl]
        s.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{HI}" stroke-width="10"/>')


D["face"] = lambda s: face(s)
for _p in ("eyebrow", "cheek", "chin", "forehead", "jaw"):
    D[_p] = (lambda p: lambda s: face(s, p))(_p)
D["beard"] = lambda s: face(s, beard=True, moustache=True)
D["moustache"] = lambda s: face(s, moustache=True)


def eye_big(s, iris="#6B8E5A", lashes=False, lid=False, hl=None):
    s.F("path", d="M40 256 C120 140 392 140 472 256 C392 372 120 372 40 256Z", fill=WHITE)
    s.F("circle", cx=256, cy=256, r=96, fill=iris)
    s.F("circle", outline=False, cx=256, cy=256, r=44, fill=BLACK)
    s.F("circle", outline=False, cx=230, cy=226, r=18, fill=WHITE)
    if lid:
        s.F("path", d="M40 256 C120 140 392 140 472 256 C392 200 120 200 40 256Z", fill=SKIN)
    if lashes:
        for k in range(7):
            x, y = arc_pt(256, 420, 250, -150 + k * 20)
            x2, y2 = arc_pt(256, 420, 300, -150 + k * 20)
            s.M(f"M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}", INK, 8)
    if hl == "pupil":
        s.raw(f'<circle cx="256" cy="256" r="56" fill="none" stroke="{HI}" stroke-width="10"/>')
    elif hl == "iris":
        s.raw(f'<circle cx="256" cy="256" r="104" fill="none" stroke="{HI}" stroke-width="10"/>')


D["eye"] = lambda s: eye_big(s)
D["eyes"] = lambda s: (s.open(transform="translate(140 256) scale(0.45) translate(-256 -256)"), eye_big(s), s.close(), s.open(transform="translate(372 256) scale(0.45) translate(-256 -256)"), eye_big(s), s.close())
D["eyelashes"] = lambda s: eye_big(s, lashes=True)
D["eyelid"] = lambda s: eye_big(s, lid=True)
D["eye-pupil"] = lambda s: eye_big(s, hl="pupil")
D["iris-eye"] = lambda s: eye_big(s, iris="#3D8BFD", hl="iris")
D["nose"] = lambda s: s.F("path", d="M256 60 C230 140 200 260 160 330 C140 370 170 400 210 390 C230 410 282 410 302 390 C342 400 372 370 352 330 C312 260 282 140 256 60Z", fill=SKIN)
D["nostrils"] = lambda s: (D["nose"](s), s.F("ellipse", outline=False, cx=215, cy=372, rx=18, ry=10, fill=SKIN_D), s.F("ellipse", outline=False, cx=297, cy=372, rx=18, ry=10, fill=SKIN_D))
D["mouth"] = lambda s: (s.F("path", d="M80 240 C160 200 352 200 432 240 C380 360 132 360 80 240Z", fill=DRED), s.F("path", outline=False, d="M120 250 C200 230 312 230 392 250 V270 H120Z", fill=WHITE),
                        s.F("ellipse", outline=False, cx=256, cy=320, rx=70, ry=22, fill=PINK))
D["lips"] = lambda s: s.F("path", d="M60 256 C120 180 200 200 256 220 C312 200 392 180 452 256 C380 360 132 360 60 256Z", fill="#D9576A")
D["tongue"] = lambda s: (s.F("path", d="M140 120 H372 V300 C372 420 140 420 140 300Z", fill=PINK), s.M("M256 140 V320", "#E07A90", 8))
D["ear"] = lambda s: (s.F("path", d="M300 70 C190 60 130 150 140 240 C146 300 190 320 190 370 C190 430 240 460 280 440 C330 420 330 370 360 330 C400 280 420 210 400 160 C380 110 340 74 300 70Z", fill=SKIN),
                      s.M("M290 150 C230 150 210 200 230 240 C250 270 290 260 290 300", SKIN_D, 14))
D["earlobe"] = lambda s: (D["ear"](s), s.raw(f'<circle cx="250" cy="420" r="44" fill="none" stroke="{HI}" stroke-width="10"/>'))

# ---------------------------------------------------------------- organs
D["heart-organ"] = lambda s: (s.T("M196 210 V110", "#3D8BFD", 34), s.T("M236 200 C226 120 266 88 306 92 C346 98 356 132 350 170", DRED, 38),
                              [s.T(f"M{x} 98 V58", DRED, 16) for x in (270, 296, 322)], s.T("M276 212 C296 168 330 170 368 186", "#3D8BFD", 30),
                              s.F("path", d="M250 452 C150 404 108 320 124 250 C138 188 196 168 240 196 C282 160 352 168 380 228 C408 300 360 400 250 452Z", fill=RED),
                              s.F("path", outline=False, d="M170 250 C176 220 200 208 222 214 C200 230 186 252 180 290 Z", fill="#F07A7E"),
                              s.M("M262 214 C250 280 268 340 300 400 M262 260 C300 270 330 300 350 330", DRED, 8))


def brain_side(s):
    s.F("path", d="M110 300 C80 230 120 140 200 120 C240 80 330 90 370 130 C430 150 450 230 420 290 C410 340 360 360 320 350 C300 380 240 390 200 360 C150 370 110 340 110 300Z", fill="#F7B5C0")
    s.M("M160 220 C190 200 220 230 250 210 C280 190 320 220 350 200 M150 280 C190 260 230 300 270 270 C300 250 340 280 380 260 M240 140 C230 170 260 190 240 220",
        "#E07A90", 10)
    s.F("path", d="M300 350 C320 380 330 410 320 440 L290 440 C300 410 290 380 280 360Z", fill="#F2A0AE")


D["brain"] = brain_side
D["lungs"] = lambda s: (s.T("M256 60 V190 M256 190 L210 230 M256 190 L302 230", "#9AA3AF", 24),
                        s.F("path", d="M226 210 C150 180 90 260 90 360 C90 430 150 450 200 430 C230 420 236 380 236 340Z", fill="#F48AA6"),
                        s.F("path", d="M286 210 C362 180 422 260 422 360 C422 430 362 450 312 430 C282 420 276 380 276 340Z", fill="#F48AA6"))
D["liver"] = lambda s: s.F("path", d="M60 220 C120 160 300 150 450 180 C460 220 420 280 340 320 C260 360 180 350 120 320 C80 300 50 260 60 220Z", fill="#A8402E")
D["kidneys"] = lambda s: ([s.F("path", d=f"M{x} 140 C{x - 80 * k} 140 {x - 100 * k} 260 {x - 60 * k} 330 C{x - 30 * k} 380 {x + 30 * k} 360 {x + 20 * k} 300 C{x + 10 * k} 270 {x + 30 * k} 230 {x + 20 * k} 190 C{x + 10 * k} 160 {x} 140 {x} 140Z", fill="#B5323A")
                           for x, k in ((190, 1), (322, -1))], s.T("M200 260 C230 320 240 380 240 460 M312 260 C282 320 272 380 272 460", "#E8D06E", 10))
D["stomach"] = lambda s: s.F("path", d="M190 60 V150 C110 170 90 280 140 360 C190 430 330 440 400 370 C440 330 430 270 380 260 C340 255 320 300 280 290 C240 280 240 220 250 150 V60Z", fill="#F48AA6")
D["small-intestine"] = lambda s: (s.F("rect", x=110, y=130, width=292, height=250, rx=120, fill="#F7B5C0"),
                                  s.M("M160 180 C200 150 240 210 280 180 C320 150 360 200 350 240 C340 280 280 250 240 280 C200 310 160 280 170 330 C180 360 240 340 280 350 C320 360 340 330 350 320", "#E07A90", 12))
D["colon-organ"] = lambda s: s.T("M150 450 V130 H362 V420 C362 450 330 460 300 450 C270 440 260 400 230 410", "#D98A70", 60)
D["intestines"] = lambda s: (D["colon-organ"](s), s.F("rect", x=190, y=180, width=140, height=200, rx=60, fill="#F7B5C0"), s.M("M210 220 C240 200 270 240 300 220 M210 280 C240 260 270 300 300 280 M210 340 C240 320 270 360 300 340", "#E07A90", 10))
D["pancreas"] = lambda s: s.F("path", d="M60 280 C100 220 200 220 260 240 C320 260 380 230 450 220 C460 260 430 300 360 300 C300 300 240 330 160 340 C100 350 60 320 60 280Z", fill="#E8B87A")
D["spleen"] = lambda s: s.F("path", d="M140 200 C200 100 380 110 400 220 C410 300 350 380 260 390 C190 400 130 350 160 300 C180 270 120 250 140 200Z", fill="#8E3E6A")
D["gallbladder"] = lambda s: (s.F("path", d="M256 80 C280 80 300 120 320 200 C350 320 320 420 256 420 C192 420 162 320 192 200 C212 120 232 80 256 80Z", fill="#6EA84A"), s.T("M256 80 V30", "#4A7A30", 14))
D["bladder"] = lambda s: (s.F("path", d="M256 120 C360 120 410 220 380 320 C360 380 300 400 256 400 C212 400 152 380 132 320 C102 220 152 120 256 120Z", fill="#F2C94C"), s.T("M200 130 C170 90 160 60 150 30 M312 130 C342 90 352 60 362 30 M256 400 V470", "#E8D06E", 12))
D["appendix"] = lambda s: (s.T("M100 140 H300 C360 140 380 200 360 260", "#D98A70", 60), s.T("M330 280 C320 340 300 400 260 440", "#F7B5C0", 24))
D["oesophagus"] = lambda s: (s.T("M256 40 C250 160 270 260 256 360", "#F48AA6", 50), s.F("path", d="M210 360 C160 380 150 460 230 470 C320 480 380 420 330 370Z", fill="#F48AA6"))
D["windpipe"] = lambda s: (s.T("M256 40 V330 M256 330 L170 440 M256 330 L342 440", "#C9CED6", 50), [s.M(f"M226 {y} H286", "#9AA3AF", 8) for y in range(70, 320, 30)])
D["thyroid"] = lambda s: (s.T("M256 80 V420", "#C9CED6", 40), s.F("path", d="M256 250 C200 180 120 200 120 290 C120 360 200 360 256 300 C312 360 392 360 392 290 C392 200 312 180 256 250Z", fill="#C1442E"))
D["skin-organ"] = lambda s: (s.F("rect", x=80, y=140, width=352, height=60, fill="#F2C29B"), s.F("rect", x=80, y=200, width=352, height=100, fill="#F7B5C0"), s.F("rect", x=80, y=300, width=352, height=80, fill="#F9E3B0"),
                             [s.T(f"M{x} 140 V100", HAIR, 6) for x in (150, 260, 360)])

# ---------------------------------------------------------------- skeleton
def bone(s, x1, y1, x2, y2, w=26, color=BONE):
    s.T(f"M{x1} {y1} L{x2} {y2}", color, w)
    a = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
    for x, y in ((x1, y1), (x2, y2)):
        for sgn in (1, -1):
            s.F("circle", cx=f"{x + sgn * math.cos(a) * w * 0.45:.0f}", cy=f"{y + sgn * math.sin(a) * w * 0.45:.0f}", r=f"{w * 0.6:.0f}", fill=color)


def skull(s, x=256, y=200, sc=1.0, jaw=True):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -200)")
    s.F("path", d="M256 40 C150 40 100 120 110 210 C116 260 150 280 160 320 H352 C362 280 396 260 402 210 C412 120 362 40 256 40Z", fill=BONE)
    if jaw:
        s.F("path", d="M170 320 H342 L326 380 C300 400 212 400 186 380Z", fill=BONE)
        s.M("M210 340 V376 M240 340 V384 M272 340 V384 M302 340 V376", BONE_D, 5)
    for x in (200, 312):
        s.F("ellipse", outline=False, cx=x, cy=220, rx=36, ry=40, fill="#3A3A44")
    s.F("polygon", outline=False, points="256,260 240,300 272,300", fill="#3A3A44")
    s.close()


@reg("skeleton")
def _(s):
    skull(s, 256, 64, 0.3)
    s.T("M256 112 V280", BONE, 12)
    for k in range(5):
        y = 140 + k * 20
        s.T(f"M256 {y} C222 {y - 4} 206 {y + 10} 204 {y + 24} M256 {y} C290 {y - 4} 306 {y + 10} 308 {y + 24}", BONE, 7)
    s.F("path", d="M208 270 C212 254 300 254 304 270 L292 304 H220Z", fill=BONE)
    for x1, y1, x2, y2 in ((200, 140, 166, 236), (166, 236, 156, 304), (312, 140, 346, 236), (346, 236, 356, 304),
                           (228, 300, 218, 388), (218, 388, 214, 456), (284, 300, 294, 388), (294, 388, 298, 456)):
        bone(s, x1, y1, x2, y2, 11)


D["skull"] = lambda s: skull(s, 256, 230, 1.0)
D["spine"] = lambda s: [s.F("rect", x=216, y=50 + k * 34, width=80, height=26, rx=10, fill=BONE) for k in range(12)] + [s.M(f"M296 {63 + k * 34} l26 6 M216 {63 + k * 34} l-26 6", BONE_D, 8) for k in range(12)]
D["rib-cage"] = lambda s: (s.T("M256 80 V400", BONE, 26), [s.T(f"M256 {y} C190 {y - 10} 140 {y + 20} 140 {y + 60} M256 {y} C322 {y - 10} 372 {y + 20} 372 {y + 60}", BONE, 16) for y in range(110, 360, 48)])
D["pelvis"] = lambda s: (s.F("path", d="M100 200 C120 120 220 130 256 200 C292 130 392 120 412 200 C420 260 360 300 320 330 C300 370 212 370 192 330 C152 300 92 260 100 200Z", fill=BONE),
                         s.F("circle", outline=False, cx=200, cy=300, r=34, fill="#3A3A44"), s.F("circle", outline=False, cx=312, cy=300, r=34, fill="#3A3A44"))
D["femur"] = lambda s: bone(s, 180, 80, 330, 430, 40)
D["humerus"] = lambda s: bone(s, 200, 90, 312, 420, 34)
D["collarbone"] = lambda s: s.T("M80 280 C150 220 220 300 256 260 C292 220 362 300 432 240", BONE, 30)
D["kneecap"] = lambda s: (bone(s, 256, 40, 256, 250, 50), bone(s, 256, 300, 256, 470, 44), s.F("ellipse", cx=256, cy=270, rx=52, ry=44, fill=BONE_D))
D["hand-bones"] = lambda s: [bone(s, x1, y1, x2, y2, 16) for x1, y1, x2, y2 in ((160, 330, 120, 260), (120, 260, 100, 200), (190, 300, 180, 200), (180, 200, 176, 130), (230, 300, 230, 180), (230, 180, 230, 100),
                                                                                (270, 300, 280, 190), (280, 190, 286, 120), (310, 310, 330, 220), (330, 220, 344, 160))] + [s.F("rect", x=170, y=300, width=160, height=120, rx=30, fill=BONE)]
D["foot-bones"] = lambda s: (s.F("path", d="M100 300 C100 240 180 240 220 280 L330 310 H200 C160 330 100 330 100 300Z", fill=BONE), [bone(s, 300, y, 420, y + 10, 14) for y in (280, 300, 320, 340)])
D["jaw-bone"] = lambda s: s.F("path", d="M100 160 C110 300 180 400 256 400 C332 400 402 300 412 160 L370 150 C360 270 310 340 256 340 C202 340 152 270 142 150Z", fill=BONE)
D["bone"] = lambda s: bone(s, 120, 380, 392, 132, 50)
D["bone-marrow"] = lambda s: (bone(s, 120, 380, 392, 132, 80), s.T("M170 340 L342 172", "#E8583B", 30))
D["joint"] = lambda s: (bone(s, 256, 40, 256, 230, 50), bone(s, 256, 290, 256, 470, 50), s.F("ellipse", cx=256, cy=260, rx=70, ry=40, fill="#8FD0FF", fill_opacity="0.6"))
D["cartilage"] = lambda s: (bone(s, 256, 40, 256, 220, 50), bone(s, 256, 300, 256, 470, 50), s.F("ellipse", cx=256, cy=260, rx=60, ry=26, fill="#B8E0F0"))
D["x-ray-of-hand"] = lambda s: (s.F("rect", x=60, y=40, width=392, height=432, rx=24, fill="#1E2A4A"), s.open(transform="translate(256 256) scale(0.9) translate(-256 -256)"), D["hand-bones"](s), s.close())

# ---------------------------------------------------------------- muscles
MUS, MUS_D = "#E8696A", "#B5323A"


def muscle_band(s, d, w=60):
    s.T(d, MUS, w)
    s.M(d, MUS_D, 4)


D["muscles"] = lambda s: (figure(s), s.F("ellipse", cx=224, cy=176, rx=30, ry=22, fill=MUS), s.F("ellipse", cx=288, cy=176, rx=30, ry=22, fill=MUS),
                          [s.F("rect", x=234, y=y, width=44, height=16, rx=7, fill=MUS) for y in (206, 226, 246)], s.T(ARM_L, MUS, 22), s.T(ARM_R, MUS, 22))
D["biceps"] = lambda s: (s.T("M100 400 L200 300 L360 140", SKIN, 70), s.F("ellipse", cx=270, cy=230, rx=90, ry=50, fill=MUS, transform="rotate(-45 270 230)"))
D["triceps"] = lambda s: (s.T("M100 400 L200 300 L360 140", SKIN, 70), s.F("ellipse", cx=250, cy=280, rx=90, ry=40, fill=MUS_D, transform="rotate(-45 250 280)"))
D["abs"] = lambda s: (s.F("rect", x=140, y=80, width=232, height=352, rx=60, fill=SKIN),
                      [s.F("rect", x=x, y=y, width=72, height=70, rx=20, fill=MUS) for x in (178, 262) for y in (120, 210, 300)])
D["heart-muscle"] = lambda s: (D["heart-organ"](s), s.M("M160 300 C200 280 240 320 280 300 M170 360 C210 340 250 380 290 360", MUS_D, 6))
D["tendon"] = lambda s: (s.F("ellipse", cx=200, cy=200, rx=80, ry=140, fill=MUS), s.T("M220 330 C250 380 280 420 320 460", "#F4EBDD", 22))
D["ligament"] = lambda s: (bone(s, 256, 40, 256, 220, 46), bone(s, 256, 300, 256, 470, 46), s.T("M220 210 L230 310 M292 210 L282 310", "#F4EBDD", 18))
D["muscle-fibre"] = lambda s: [s.T(f"M60 {y} C200 {y - 20} 312 {y + 20} 452 {y}", MUS if k % 2 else MUS_D, 34) for k, y in enumerate(range(150, 400, 50))]

# ---------------------------------------------------------------- body systems (figure + system)
def system(fn):
    return lambda s: (figure(s), fn(s))


D["digestive-system"] = system(lambda s: (s.T("M256 108 V170", "#F48AA6", 9), s.F("ellipse", cx=278, cy=182, rx=26, ry=18, fill="#F48AA6"),
                                          s.T("M214 206 H298 V256 H214 Z", "#D98A70", 11), s.M("M232 220 H282 M232 240 H282", "#F7B5C0", 7)))
D["respiratory-system"] = system(lambda s: (s.T("M256 104 V150", "#C9CED6", 9), s.F("ellipse", cx=230, cy=184, rx=22, ry=38, fill="#F48AA6"), s.F("ellipse", cx=282, cy=184, rx=22, ry=38, fill="#F48AA6")))
D["circulatory-system"] = system(lambda s: (s.M("M262 176 C206 190 176 220 164 240 L156 300 M262 176 C318 190 336 220 348 240 L356 300 M262 176 V280 L220 452 M262 280 L294 452 M262 176 V100", RED, 5),
                                            s.M("M250 180 C200 200 172 228 160 250 M270 180 C320 200 340 228 352 250", "#3D8BFD", 4), s.F("circle", cx=264, cy=176, r=13, fill=RED)))
D["nervous-system"] = system(lambda s: (s.F("ellipse", cx=256, cy=60, rx=32, ry=22, fill="#F7B5C0"), s.M("M256 84 V280 M256 150 L170 240 L156 300 M256 150 L342 240 L356 300 M256 280 L217 388 L214 452 M256 280 L295 388 L298 452", "#E8D06E", 5)))
D["skeletal-system"] = lambda s: D["skeleton"](s)
D["muscular-system"] = lambda s: D["muscles"](s)
D["immune-system"] = system(lambda s: (s.F("path", d="M256 146 L316 168 V218 C316 254 288 278 256 290 C224 278 196 254 196 218 V168Z", fill="#3D8BFD"), s.T("M226 218 L250 242 L290 198", WHITE, 12)))
D["endocrine-system"] = system(lambda s: [s.F("circle", cx=x, cy=y, r=r, fill=c) for x, y, r, c in ((256, 60, 10, "#B880E8"), (256, 116, 11, "#C1442E"), (236, 222, 10, "#E8B87A"), (276, 222, 10, "#E8B87A"), (256, 204, 11, "#E8D06E"))])
D["excretory-system"] = system(lambda s: (s.F("ellipse", cx=228, cy=214, rx=13, ry=20, fill="#B5323A"), s.F("ellipse", cx=284, cy=214, rx=13, ry=20, fill="#B5323A"), s.M("M228 234 L250 264 M284 234 L262 264", "#E8D06E", 5),
                                          s.F("ellipse", cx=256, cy=270, rx=17, ry=11, fill="#F2C94C")))
D["lymphatic-system"] = system(lambda s: (s.M("M256 120 V280 M256 150 L176 230 M256 150 L336 230 M256 260 L222 380 M256 260 L290 380", "#5EB85A", 4), [s.F("circle", cx=x, cy=y, r=7, fill="#5EB85A") for x, y in ((256, 124), (212, 190), (300, 190), (240, 290), (272, 290))]))
D["reproductive-system-diagram"] = lambda s: (s.F("path", d="M196 180 C196 300 236 340 256 360 C276 340 316 300 316 180 Z", fill="#F48AA6"), s.T("M200 190 C150 180 120 210 110 250 M312 190 C362 180 392 210 402 250", "#F48AA6", 14),
                                              s.F("ellipse", cx=110, cy=262, rx=26, ry=20, fill="#F7B5C0"), s.F("ellipse", cx=402, cy=262, rx=26, ry=20, fill="#F7B5C0"), s.T("M256 360 V440", "#F48AA6", 22))

# ---------------------------------------------------------------- senses
D["sense-of-sight"] = lambda s: eye_big(s)
D["sense-of-hearing"] = lambda s: (D["ear"](s), s.M("M60 200 C40 240 40 280 60 320 M30 170 C0 230 0 290 30 350", "#3D8BFD", 10))
D["sense-of-smell"] = lambda s: (D["nose"](s), s.M("M120 150 C100 120 140 100 120 70 M390 150 C370 120 410 100 390 70", "#9BD7A8", 10))
D["sense-of-taste"] = lambda s: D["tongue"](s)
D["sense-of-touch"] = lambda s: (hand(s), s.M("M320 200 C340 200 350 220 350 240 M330 170 C370 170 390 200 390 240", "#3D8BFD", 8))
D["five-senses"] = lambda s: [(s.open(transform=f"translate({x} {y}) scale(0.32) translate(-256 -256)"), D[k](s), s.close())
                              for k, x, y in (("eye", 256, 100), ("ear", 110, 220), ("nose", 402, 220), ("tongue", 160, 390), ("sense-of-touch", 352, 390))]
D["taste-buds"] = lambda s: (D["tongue"](s), [s.F("circle", outline=False, cx=x, cy=y, r=10, fill="#E07A90") for x, y in ((200, 180), (300, 180), (220, 250), (290, 250), (256, 320), (200, 300), (310, 300))])
D["eye-anatomy"] = lambda s: (s.F("circle", cx=256, cy=256, r=190, fill=WHITE), s.F("path", d="M400 160 C450 220 450 290 400 350 C420 290 420 220 400 160Z", fill="#8FD0FF"),
                              s.F("ellipse", cx=400, cy=256, rx=20, ry=70, fill="#3A3A44"), s.T("M66 256 H20", "#E8D06E", 30), s.M("M120 160 C180 200 160 300 120 350", RED, 5))
D["ear-anatomy"] = lambda s: (D["ear"](s), s.T("M300 300 C360 300 380 260 400 240", "#E8C39E", 16), s.M("M410 220 C440 210 460 240 440 260 C460 280 430 300 410 280", "#F48AA6", 10))
D["nose-anatomy"] = lambda s: (s.F("path", d="M100 400 C140 300 200 120 260 100 C320 120 380 300 420 400Z", fill=SKIN), s.F("path", outline=False, d="M200 360 C240 300 280 300 320 360Z", fill="#F7B5C0"))

# ---------------------------------------------------------------- teeth
TOOTH = "M150 120 C150 70 230 60 256 90 C282 60 362 70 362 120 C362 200 340 230 330 300 C320 380 300 440 280 440 C260 440 266 340 256 340 C246 340 252 440 232 440 C212 440 192 380 182 300 C172 230 150 200 150 120Z"
D["tooth"] = lambda s: (s.F("path", d=TOOTH, fill=WHITE), s.F("path", outline=False, d="M180 120 C180 100 200 92 216 100 C196 120 192 150 196 180Z", fill="#E8F0FF"))
D["teeth"] = lambda s: (s.F("path", d="M60 220 C140 120 372 120 452 220 V260 H60Z", fill="#F48AA6"), [s.F("rect", x=96 + k * 42, y=200, width=38, height=70, rx=12, fill=WHITE) for k in range(8)],
                        s.F("path", d="M60 300 H452 V320 C372 420 140 420 60 320Z", fill="#F48AA6"), [s.F("rect", x=110 + k * 40, y=290, width=36, height=56, rx=12, fill=WHITE) for k in range(8)])
D["milk-teeth"] = lambda s: (s.F("path", d="M100 260 C160 180 352 180 412 260 V300 H100Z", fill="#F48AA6"), [s.F("rect", x=140 + k * 48, y=250, width=40, height=56, rx=14, fill=WHITE) for k in range(5)])
D["molar"] = lambda s: (s.F("path", d="M130 150 C130 100 200 100 220 130 C240 100 272 100 292 130 C312 100 382 100 382 150 C382 230 360 260 350 330 C340 420 300 440 290 420 C276 380 270 330 256 330 C242 330 236 380 222 420 C212 440 172 420 162 330 C152 260 130 230 130 150Z", fill=WHITE))
D["incisor"] = lambda s: s.F("path", d="M190 80 H322 C330 160 320 240 300 320 C290 390 270 440 256 440 C242 440 222 390 212 320 C192 240 182 160 190 80Z", fill=WHITE)
D["canine-tooth"] = lambda s: s.F("path", d="M256 60 C300 100 330 160 320 220 C310 300 290 400 256 440 C222 400 202 300 192 220 C182 160 212 100 256 60Z", fill=WHITE)
D["wisdom-tooth"] = lambda s: (D["molar"](s), s.raw(f'<circle cx="256" cy="256" r="200" fill="none" stroke="{HI}" stroke-width="10"/>'))
D["tooth-anatomy"] = lambda s: (s.F("path", d=TOOTH, fill=WHITE), s.F("path", outline=False, d="M230 160 C230 140 282 140 282 160 C282 260 270 360 256 380 C242 360 230 260 230 160Z", fill="#F48AA6"),
                                s.F("rect", outline=False, x=150, y=230, width=212, height=20, fill="#F7B5C0", fill_opacity="0.6"))
D["gums"] = lambda s: (s.F("path", d="M50 200 C140 120 372 120 462 200 V300 C372 260 140 260 50 300Z", fill="#E8607A"), [s.F("rect", x=96 + k * 42, y=250, width=38, height=80, rx=12, fill=WHITE) for k in range(8)])

# ---------------------------------------------------------------- blood and cells
def drop(s, x=256, y=80, h=360, color=RED):
    w = h * 0.55
    s.F("path", d=f"M{x} {y} C{x} {y} {x - w} {y + h * 0.55} {x - w} {y + h * 0.72} C{x - w} {y + h * 1.0} {x + w} {y + h * 1.0} {x + w} {y + h * 0.72} C{x + w} {y + h * 0.55} {x} {y} {x} {y}Z", fill=color)
    s.F("ellipse", outline=False, cx=x - w * 0.45, cy=y + h * 0.7, rx=w * 0.14, ry=h * 0.1, fill="#F07A7E")


def rbc(s, x=256, y=256, r=150):
    s.F("circle", cx=x, cy=y, r=r, fill=RED)
    s.F("circle", outline=False, cx=x, cy=y, r=r * 0.5, fill=DRED)


D["blood"] = lambda s: (drop(s, 180, 120, 260), rbc(s, 360, 330, 80))
D["blood-drop"] = lambda s: drop(s)
D["red-blood-cell"] = lambda s: rbc(s)
D["white-blood-cell"] = lambda s: (s.F("path", d="M256 90 C350 80 430 160 420 250 C430 340 350 430 256 420 C160 430 80 350 90 256 C80 160 160 90 256 90Z", fill="#F4F1EA"),
                                   s.F("path", d="M200 220 C220 180 300 180 310 230 C330 250 320 300 280 300 C250 330 200 310 210 270 C180 260 190 230 200 220Z", fill="#B880E8"))
D["platelets"] = lambda s: [s.F("ellipse", cx=x, cy=y, rx=50, ry=30, fill="#E8B04A", transform=f"rotate({r} {x} {y})") for x, y, r in ((170, 200, 20), (320, 180, -30), (250, 300, 10), (360, 340, 40), (150, 350, -20))]
D["blood-vessels"] = lambda s: (s.T("M40 200 C140 180 260 240 470 200", RED, 46), s.T("M40 330 C140 350 260 290 470 330", "#3D8BFD", 46), [rbc(s, x, 200 + (x % 3) * 4, 14) for x in (110, 220, 360)])
D["arteries-and-veins"] = lambda s: (s.T("M256 470 V300 C256 200 150 160 100 60 M256 300 C256 200 362 160 412 60", RED, 30), s.T("M226 470 V310 C226 220 120 200 70 120 M286 470 V310 C286 220 392 200 442 120", "#3D8BFD", 22))
D["capillaries"] = lambda s: (s.T("M40 160 C120 160 160 200 200 200", RED, 34), s.T("M472 350 C392 350 352 310 312 310", "#3D8BFD", 34),
                              s.M("M200 200 C240 200 260 240 312 310 M200 200 C260 180 300 260 312 310 M200 200 C220 260 280 280 312 310", "#B5323A", 8))
D["blood-types"] = lambda s: [(drop(s, x, y, 150), ) for x, y in ((150, 60), (362, 60), (150, 280), (362, 280))]
D["plasma-blood"] = lambda s: (s.F("rect", x=180, y=60, width=152, height=400, rx=70, fill="none"), s.F("rect", outline=False, x=184, y=64, width=144, height=180, rx=60, fill="#F2D06E"),
                               s.F("rect", outline=False, x=184, y=240, width=144, height=216, rx=60, fill=DRED), s.raw('<rect x="180" y="60" width="152" height="400" rx="70" fill="none" stroke="#2E2A3B" stroke-width="10"/>'))
D["nerve-cell"] = lambda s: ([s.T(f"M200 220 L{x} {y}", "#E8B04A", 10) for x, y in ((100, 120), (80, 220), (110, 330), (200, 80))], s.T("M240 240 C300 280 360 300 440 380", "#E8B04A", 14),
                             s.F("circle", cx=200, cy=220, r=60, fill="#F2C94C"), s.F("circle", outline=False, cx=200, cy=220, r=24, fill="#C1662E"), [s.T(f"M440 380 L{x} {y}", "#E8B04A", 8) for x, y in ((470, 350), (480, 410), (430, 440))])
D["stem-cell"] = lambda s: (s.F("circle", cx=256, cy=256, r=170, fill="#9BD7E8"), s.F("circle", outline=False, cx=256, cy=256, r=70, fill="#3A8AB8"), [s.F("circle", outline=False, cx=x, cy=y, r=10, fill="#5AB0D0") for x, y in ((170, 180), (340, 200), (200, 350), (340, 340))])

# ---------------------------------------------------------------- skin and hair
D["skin-layers"] = lambda s: D["skin-organ"](s)
D["hair"] = lambda s: (s.F("ellipse", cx=256, cy=300, rx=150, ry=170, fill=SKIN), s.F("path", d="M96 300 C70 100 442 100 416 300 C400 200 330 170 256 170 C182 170 112 200 96 300Z", fill=HAIR))
D["hair-follicle"] = lambda s: (s.F("rect", x=60, y=200, width=392, height=260, fill="#F7B5C0"), s.F("rect", x=60, y=160, width=392, height=40, fill=SKIN), s.T("M256 60 V380", HAIR, 14),
                                s.F("ellipse", cx=256, cy=390, rx=34, ry=40, fill="#E8B87A"))
D["curly-hair"] = lambda s: (s.F("ellipse", cx=256, cy=320, rx=140, ry=160, fill=SKIN), [s.F("circle", cx=x, cy=y, r=40, fill=HAIR) for x, y in ((140, 220), (200, 160), (256, 140), (312, 160), (372, 220), (110, 290), (402, 290))])
D["straight-hair"] = lambda s: (s.F("path", d="M110 200 C110 90 402 90 402 200 V460 H340 V240 H172 V460 H110Z", fill=HAIR), s.F("ellipse", cx=256, cy=300, rx=110, ry=140, fill=SKIN))
D["bald-head"] = lambda s: (s.F("ellipse", cx=256, cy=280, rx=150, ry=180, fill=SKIN), s.F("ellipse", outline=False, cx=200, cy=160, rx=40, ry=26, fill="#F9DCC0"), s.F("path", d="M106 300 C110 340 130 360 140 370 L150 300Z", fill=HAIR),
                            s.F("path", d="M406 300 C402 340 382 360 372 370 L362 300Z", fill=HAIR))
D["grey-hair"] = lambda s: (s.F("ellipse", cx=256, cy=300, rx=150, ry=170, fill=SKIN), s.F("path", d="M96 300 C70 100 442 100 416 300 C400 200 330 170 256 170 C182 170 112 200 96 300Z", fill="#C9CED6"))
D["fingerprint"] = lambda s: [s.raw(f'<ellipse cx="256" cy="270" rx="{40 + k * 30}" ry="{60 + k * 36}" fill="none" stroke="#3A3A44" stroke-width="10" stroke-dasharray="{200 + k * 30} 40"/>') for k in range(6)]
D["freckles"] = lambda s: (s.F("ellipse", cx=256, cy=280, rx=170, ry=190, fill=SKIN), [s.F("circle", outline=False, cx=x, cy=y, r=7, fill="#C98A5A") for x, y in ((180, 300), (200, 320), (220, 296), (300, 300), (320, 320), (336, 296), (256, 330))])
D["sweat-drop"] = lambda s: drop(s, color="#8FD0FF")
D["goosebumps"] = lambda s: (s.F("rect", x=60, y=120, width=392, height=272, rx=30, fill=SKIN), [s.F("circle", cx=x, cy=y, r=12, fill="#F2B48A") for x in range(100, 420, 50) for y in range(160, 360, 50)])

# ---------------------------------------------------------------- growth stages
def kid(s, x, base, sc, shirt=C["blue"]):
    s.open(transform=f"translate({x} {base}) scale({sc}) translate(-256 -470)")
    figure(s)
    s.F("path", d=TORSO, fill=shirt)
    s.close()


D["growth-stages"] = lambda s: [kid(s, x, 470, sc, c) for x, sc, c in ((70, 0.32, C["yellow"]), (170, 0.5, C["orange"]), (290, 0.72, C["green"]), (410, 0.9, C["blue"]))]
D["embryo"] = lambda s: (s.F("circle", cx=256, cy=256, r=190, fill="#F7D0DC"), s.T("M300 180 C260 140 180 170 190 250 C200 330 300 350 320 290", "#F2A6B8", 50), s.F("circle", cx=300, cy=186, r=40, fill="#F2A6B8"))
D["foetus"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill="#F7D0DC"), s.F("circle", cx=290, cy=180, r=70, fill=SKIN), s.F("path", d="M240 230 C160 260 150 380 240 400 C320 410 360 340 330 260Z", fill=SKIN),
                         s.T("M260 330 C300 360 330 330 340 300", SKIN_D, 8))
D["newborn"] = lambda s: (s.F("path", d="M100 380 C100 280 200 240 300 250 C380 260 420 320 412 380Z", fill="#B8D8F8"), s.F("circle", cx=330, cy=230, r=80, fill=SKIN),
                          s.M("M310 230 Q320 236 330 230 M350 230 Q360 236 370 230", INK, 5), s.F("path", d="M270 180 C270 130 390 130 390 180 C360 160 300 160 270 180Z", fill="#B8D8F8"))
D["growing-up"] = lambda s: (kid(s, 150, 470, 0.55, C["orange"]), kid(s, 330, 470, 0.85, C["blue"]), s.M("M220 140 L280 100 " + head(280, 100, -34, 20), C["green"], 8))
D["puberty"] = lambda s: (kid(s, 256, 470, 0.92, C["purple"]), s.M("M400 400 V120 " + head(400, 120, -90, 24), C["green"], 8))
D["old-age"] = lambda s: (kid(s, 230, 470, 0.92, "#8C7A6A"), s.T("M340 300 V470", C["brown"], 12), s.T("M340 300 C340 270 370 270 370 300", C["brown"], 12))
D["height-chart"] = lambda s: (s.F("rect", x=320, y=40, width=120, height=440, rx=10, fill="#F2D06E"), [s.M(f"M320 {y} h{30 if y % 80 else 60}", "#8C6A20", 6) for y in range(60, 470, 40)],
                               kid(s, 200, 470, 0.85, C["blue"]))


if __name__ == "__main__":
    run("human-body", D, sys.argv[1:] or None)
