"""symbols-signs drawings. Run: python drawings/symbols_signs.py [ids...]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from draw_lib import C, INK, THEME, Svg, ang, arc_pt, head, run  # noqa: E402

D = {}


def draw(item_id):
    def reg(fn):
        D[item_id] = fn
        return fn
    return reg


A1, A2, LIGHT = THEME["accent"], THEME["accent-2"], THEME["light"]


# ---------------------------------------------------------------- arrows (mono)
def straight(s, x1, y1, x2, y2, both=False):
    s.M(f"M{x1} {y1} L{x2} {y2} " + head(x2, y2, ang(x1, y1, x2, y2)) +
        (" " + head(x1, y1, ang(x2, y2, x1, y1)) if both else ""))


for _id, (x1, y1, x2, y2) in {
    "arrow-right": (96, 256, 416, 256), "arrow-left": (416, 256, 96, 256),
    "arrow-up": (256, 416, 256, 96), "arrow-down": (256, 96, 256, 416),
    "arrow-up-right": (128, 384, 384, 128), "arrow-up-left": (384, 384, 128, 128),
    "arrow-down-right": (128, 128, 384, 384), "arrow-down-left": (384, 128, 128, 384),
}.items():
    D[_id] = (lambda a: lambda s: straight(s, *a))((x1, y1, x2, y2))

D["double-arrow-left-right"] = lambda s: straight(s, 80, 256, 432, 256, both=True)
D["double-arrow-up-down"] = lambda s: straight(s, 256, 80, 256, 432, both=True)


@draw("curved-arrow-right")
def _(s):
    s.M("M104 400 C104 230 220 150 400 150 " + head(400, 150, 0))


@draw("curved-arrow-left")
def _(s):
    s.M("M408 400 C408 230 292 150 112 150 " + head(112, 150, 180))


@draw("u-turn-arrow")
def _(s):
    s.M("M150 430 V230 C150 110 362 110 362 230 V350 " + head(362, 350, 90))


def arc_arrow(s, cx, cy, r, a0, a1, w=None, sweep=1, both=False):
    """Arc from angle a0 to a1 (degrees, clockwise when sweep=1) with a head at a1."""
    x0, y0 = arc_pt(cx, cy, r, a0)
    x1, y1 = arc_pt(cx, cy, r, a1)
    span = (a1 - a0) % 360 if sweep else (a0 - a1) % 360
    large = 1 if span > 180 else 0
    tangent = a1 + (90 if sweep else -90)
    d = f"M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f} " + head(x1, y1, tangent, 76)
    if both:
        d += " " + head(x0, y0, a0 + (-90 if sweep else 90), 76)
    s.M(d) if w is None else s.M(d, w=w)


D["circular-arrow"] = lambda s: arc_arrow(s, 256, 256, 160, -60, 250)
D["clockwise-arrow"] = lambda s: arc_arrow(s, 256, 256, 160, 180, 90)
D["counterclockwise-arrow"] = lambda s: arc_arrow(s, 256, 256, 160, 0, 90, sweep=0)


@draw("zigzag-arrow")
def _(s):
    s.M("M90 360 L200 230 L290 320 L410 170 " + head(410, 170, ang(290, 320, 410, 170)))


@draw("wavy-arrow")
def _(s):
    s.M("M80 256 C140 150 200 362 260 256 C300 186 350 256 420 256 " + head(420, 256, 0))


@draw("spiral-arrow")
def _(s):
    s.M("M256 256 A40 40 0 0 1 336 256 A80 80 0 0 1 176 256 A120 120 0 0 1 416 256 A160 160 0 0 1 96 256 "
        + head(96, 256, -90, 76))


@draw("trend-up-arrow")
def _(s):
    s.M("M80 400 L200 280 L270 340 L420 170 " + head(420, 170, ang(270, 340, 420, 170)))


@draw("trend-down-arrow")
def _(s):
    s.M("M80 112 L200 232 L270 172 L420 342 " + head(420, 342, ang(270, 172, 420, 342)))


for _id, d in {
    "chevron-right": "M196 112 L340 256 L196 400", "chevron-left": "M316 112 L172 256 L316 400",
    "chevron-up": "M112 316 L256 172 L400 316", "chevron-down": "M112 196 L256 340 L400 196",
    "double-chevron-right": "M128 120 L264 256 L128 392 M256 120 L392 256 L256 392",
    "double-chevron-left": "M384 120 L248 256 L384 392 M256 120 L120 256 L256 392",
}.items():
    D[_id] = (lambda d: lambda s: s.M(d))(d)


@draw("hand-drawn-arrow")
def _(s):
    s.M("M84 330 C150 300 196 334 256 290 C306 254 350 236 410 196 "
        "M318 176 C352 186 384 190 412 194 C404 226 396 256 392 290")


@draw("dashed-arrow")
def _(s):
    s.M("M96 256 H330", dash="40 36")
    s.M(head(416, 256, 0) + " M340 256 H416")


@draw("split-arrow")
def _(s):
    s.M("M90 256 H220 C280 256 300 150 410 150 " + head(410, 150, 0) +
        " M220 256 C280 256 300 362 410 362 " + head(410, 362, 0))


@draw("merge-arrows")
def _(s):
    s.M("M90 150 C200 150 220 256 290 256 M90 362 C200 362 220 256 290 256 H420 " + head(420, 256, 0))


@draw("expand-arrows")
def _(s):
    d = []
    for (x1, y1, x2, y2) in ((216, 216, 100, 100), (296, 216, 412, 100), (216, 296, 100, 412), (296, 296, 412, 412)):
        d.append(f"M{x1} {y1} L{x2} {y2} " + head(x2, y2, ang(x1, y1, x2, y2), 70))
    s.M(" ".join(d))


@draw("collapse-arrows")
def _(s):
    d = []
    for (x1, y1, x2, y2) in ((96, 96, 210, 210), (416, 96, 302, 210), (96, 416, 210, 302), (416, 416, 302, 302)):
        d.append(f"M{x1} {y1} L{x2} {y2} " + head(x2, y2, ang(x1, y1, x2, y2), 70))
    s.M(" ".join(d))


@draw("swap-arrows")
def _(s):
    s.M("M100 186 H410 " + head(410, 186, 0, 70) + " M412 326 H102 " + head(102, 326, 180, 70))


@draw("block-arrow-right")
def _(s):
    s.raw(f'<polygon points="88,196 280,196 280,112 432,256 280,400 280,316 88,316" fill="{INK}" '
          f'stroke="{INK}" stroke-width="24" stroke-linejoin="round"/>')


@draw("bent-arrow-down-right")
def _(s):
    s.M("M140 100 V300 C140 346 166 370 212 370 H412 " + head(412, 370, 0))


@draw("arrow-in-circle-right")
def _(s):
    s.raw(f'<circle cx="256" cy="256" r="196" fill="none" stroke="{INK}" stroke-width="24"/>')
    s.M("M156 256 H350 " + head(350, 256, 0, 76))


@draw("four-way-arrows")
def _(s):
    s.M("M256 70 V442 M70 256 H442 " + head(256, 70, -90, 66) + " " + head(256, 442, 90, 66) + " "
        + head(70, 256, 180, 66) + " " + head(442, 256, 0, 66))


@draw("cycle-arrows")
def _(s):
    for a in (-80, 40, 160):
        arc_arrow(s, 256, 256, 160, a, a + 92)


@draw("arrow-hitting-target")
def _(s):
    for r in (180, 120, 60):
        s.raw(f'<circle cx="236" cy="276" r="{r}" fill="none" stroke="{INK}" stroke-width="24"/>')
    s.raw(f'<circle cx="236" cy="276" r="14" fill="{INK}"/>')
    s.M("M248 264 L430 82 M430 82 L430 140 M430 82 L372 82 M400 112 L400 160 M400 112 L352 112")


# ---------------------------------------------------------------- check and cross marks (mono)
CHECK = "M124 268 L214 358 L392 160"
CROSS = "M150 150 L362 362 M362 150 L150 362"
BOX = f'<rect x="76" y="76" width="360" height="360" rx="56" fill="none" stroke="{INK}" stroke-width="24"/>'
RING = f'<circle cx="256" cy="256" r="196" fill="none" stroke="{INK}" stroke-width="24"/>'

D["check-mark"] = lambda s: s.M("M96 270 L208 382 L420 136")
D["cross-mark"] = lambda s: s.M("M120 120 L392 392 M392 120 L120 392")


@draw("check-in-circle")
def _(s):
    s.raw(RING); s.M("M156 264 L228 336 L362 186")


@draw("cross-in-circle")
def _(s):
    s.raw(RING); s.M("M176 176 L336 336 M336 176 L176 336")


@draw("checked-box")
def _(s):
    s.raw(BOX); s.M("M156 264 L228 336 L362 186")


D["empty-check-box"] = lambda s: s.raw(BOX)


@draw("crossed-box")
def _(s):
    s.raw(BOX); s.M("M176 176 L336 336 M336 176 L176 336")


@draw("radio-button-selected")
def _(s):
    s.raw(f'<circle cx="256" cy="256" r="160" fill="none" stroke="{INK}" stroke-width="24"/>')
    s.raw(f'<circle cx="256" cy="256" r="86" fill="{INK}"/>')


D["radio-button-empty"] = lambda s: s.raw(f'<circle cx="256" cy="256" r="160" fill="none" stroke="{INK}" stroke-width="24"/>')


@draw("double-check-mark")
def _(s):
    s.M("M60 270 L150 360 L330 160 M210 330 L240 360 L452 160")


@draw("check-mark-in-shield")
def _(s):
    s.M("M256 64 L416 124 V250 C416 352 344 418 256 452 C168 418 96 352 96 250 V124 Z")
    s.M("M178 260 L236 318 L340 202")


# ---------------------------------------------------------------- question and exclamation marks (themed)
Q_PATH = "M166 186 C166 116 214 82 262 82 C318 82 352 120 352 170 C352 222 304 240 278 264 C264 278 256 294 256 318"


def qmark(s, color=A1, w=60):
    s.T(Q_PATH, color, w)
    s.F("circle", cx=256, cy=410, r=w * 0.62, fill=color)


def emark(s, color=A1, w=64):
    s.T("M256 96 V306", color, w)
    s.F("circle", cx=256, cy=406, r=w * 0.6, fill=color)


D["question-mark"] = lambda s: qmark(s)
D["exclamation-mark"] = lambda s: emark(s)


@draw("question-mark-in-circle")
def _(s):
    s.F("circle", cx=256, cy=256, r=210, fill=A1)
    s.open(transform="translate(256 262) scale(0.62) translate(-256 -256)")
    qmark(s, LIGHT, 60)
    s.close()


@draw("exclamation-mark-in-circle")
def _(s):
    s.F("circle", cx=256, cy=256, r=210, fill=A2)
    s.open(transform="translate(256 262) scale(0.62) translate(-256 -256)")
    emark(s, LIGHT, 64)
    s.close()


@draw("double-question-mark")
def _(s):
    for x in (150, 362):
        s.open(transform=f"translate({x} 256) scale(0.72) translate(-256 -256)")
        qmark(s)
        s.close()


@draw("double-exclamation-mark")
def _(s):
    for x in (176, 336):
        s.open(transform=f"translate({x} 256) scale(0.9) translate(-256 -256)")
        emark(s, A2)
        s.close()


@draw("interrobang")
def _(s):
    s.T(Q_PATH, A1, 58)
    s.T("M236 118 V318", A1, 46)
    s.F("circle", cx=256, cy=410, r=36, fill=A1)


@draw("upside-down-question-mark")
def _(s):
    s.open(transform="rotate(180 256 256)"); qmark(s); s.close()


@draw("inverted-exclamation-mark")
def _(s):
    s.open(transform="rotate(180 256 256)"); emark(s, A2); s.close()


@draw("question-marks-cloud")
def _(s):
    for x, y, sc, rot, col in ((256, 250, 0.62, 0, A1), (118, 170, 0.36, -18, A2), (400, 160, 0.4, 16, A2),
                               (110, 380, 0.3, -10, A1), (410, 380, 0.34, 12, A1)):
        s.open(transform=f"translate({x} {y}) rotate({rot}) scale({sc}) translate(-256 -256)")
        qmark(s, col)
        s.close()


@draw("question-mark-box")
def _(s):
    s.F("polygon", points="96,176 256,120 416,176 256,232", fill="#7DB2FF")
    s.F("polygon", points="96,176 256,232 256,440 96,384", fill=A1)
    s.F("polygon", points="256,232 416,176 416,384 256,440", fill="#2C6BD6")
    s.open(transform="matrix(0.5 0.175 0 0.56 48 140)")
    qmark(s, LIGHT, 56)
    s.close()


# ---------------------------------------------------------------- punctuation (mono)
import math  # noqa: E402

from draw_lib import star_pts  # noqa: E402

A1L, A2L = "#7DB2FF", "#F9B57A"  # highlight tints of the two accents


def dot(s, x, y, r=40, color=INK):
    s.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')


def comma_at(s, x, y, flip=False, scale=1.0):
    tf = f"translate({x} {y}) scale({scale})" + (" rotate(180)" if flip else "")
    s.open(transform=tf)
    dot(s, 0, 0, 40)
    s.M("M30 10 C34 70 6 112 -34 130", w=30)
    s.close()


D["full-stop"] = lambda s: dot(s, 256, 256, 56)
D["comma"] = lambda s: comma_at(s, 250, 210, scale=1.3)


@draw("colon-punctuation")
def _(s):
    dot(s, 256, 166, 48); dot(s, 256, 346, 48)


@draw("semicolon")
def _(s):
    dot(s, 250, 140, 46); comma_at(s, 250, 310, scale=1.1)


D["apostrophe"] = lambda s: comma_at(s, 250, 190, scale=1.3)


@draw("quotation-marks")
def _(s):
    for x in (186, 326):
        comma_at(s, x, 300, flip=True, scale=1.2)


@draw("single-quotation-marks")
def _(s):
    comma_at(s, 166, 300, flip=True, scale=1.2); comma_at(s, 346, 210, scale=1.2)


D["hyphen"] = lambda s: s.M("M176 256 H336", w=40)
D["em-dash"] = lambda s: s.M("M72 256 H440", w=40)


@draw("ellipsis")
def _(s):
    for x in (126, 256, 386):
        dot(s, x, 256, 40)


D["parentheses"] = lambda s: s.M("M206 80 Q100 256 206 432 M306 80 Q412 256 306 432", w=32)
D["square-brackets"] = lambda s: s.M("M212 88 H140 V424 H212 M300 88 H372 V424 H300", w=32)


@draw("curly-braces")
def _(s):
    left = "M216 88 C164 88 170 130 170 182 C170 228 160 256 112 256 C160 256 170 284 170 330 C170 382 164 424 216 424"
    s.M(left, w=30)
    s.open(transform="translate(512 0) scale(-1 1)"); s.M(left, w=30); s.close()


D["angle-brackets"] = lambda s: s.M("M216 120 L104 256 L216 392 M296 120 L408 256 L296 392", w=32)
D["forward-slash"] = lambda s: s.M("M340 80 L172 432", w=32)
D["backslash"] = lambda s: s.M("M172 80 L340 432", w=32)
D["ampersand"] = lambda s: s.M("M392 420 L196 206 C152 158 166 92 226 92 C286 92 296 164 246 196 L174 244 "
                               "C108 288 120 412 226 412 C290 412 340 370 380 300", w=34)


@draw("at-sign")
def _(s):
    s.M("M320 200 V300 C320 350 390 350 404 280 C430 160 340 90 256 90 C160 90 90 166 90 256 "
        "C90 346 160 422 256 422 C304 422 340 410 372 388", w=30)
    s.raw(f'<circle cx="256" cy="256" r="66" fill="none" stroke="{INK}" stroke-width="30"/>')


D["hash-sign"] = lambda s: s.M("M216 100 L186 412 M336 100 L306 412 M124 200 H408 M104 312 H388", w=32)


@draw("asterisk")
def _(s):
    d = []
    for a in (90, 30, 150):
        x1, y1 = arc_pt(256, 256, 150, a); x2, y2 = arc_pt(256, 256, 150, a + 180)
        d.append(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}")
    s.M(" ".join(d), w=36)


D["underscore"] = lambda s: s.M("M104 410 H408", w=32)
D["vertical-bar"] = lambda s: s.M("M256 72 V440", w=32)
D["tilde"] = lambda s: s.M("M96 290 C140 200 206 214 256 256 C306 298 372 312 416 222", w=34)
D["caret"] = lambda s: s.M("M140 310 L256 170 L372 310", w=34)
D["section-sign"] = lambda s: s.M(
    "M326 132 C312 92 200 86 192 148 C184 206 330 220 330 290 C330 350 200 352 190 296 "
    "M186 380 C200 420 312 426 320 364 C328 306 182 292 182 222 C182 162 312 160 322 216", w=28)


@draw("pilcrow")
def _(s):
    s.raw(f'<path d="M300 96 H226 C166 96 132 138 132 184 C132 230 166 272 226 272 H300 Z" fill="{INK}"/>')
    s.M("M300 96 V420 M372 96 V420 M300 96 H404", w=32)


@draw("bullet-point")
def _(s):
    dot(s, 140, 256, 48); s.M("M232 256 H420", w=28)


D["guillemets"] = lambda s: s.M(
    "M196 150 L96 256 L196 362 M276 150 L176 256 L276 362 M236 150 L336 256 L236 362 M316 150 L416 256 L316 362", w=28)
D["arabic-comma"] = lambda s: comma_at(s, 262, 300, flip=True, scale=1.3)


@draw("arabic-question-mark")
def _(s):
    s.open(transform="translate(512 0) scale(-1 1)")
    s.M(Q_PATH, w=44)
    dot(s, 256, 410, 34)
    s.close()


@draw("arabic-semicolon")
def _(s):
    comma_at(s, 262, 200, flip=True, scale=1.1); dot(s, 256, 370, 46)


# ---------------------------------------------------------------- hearts and stars (themed)
HEART = ("M256 432 C140 352 68 282 68 190 C68 128 114 84 172 84 C210 84 240 104 256 134 "
         "C272 104 302 84 340 84 C398 84 444 128 444 190 C444 282 372 352 256 432Z")
HEART_L = "M256 134 C240 104 210 84 172 84 C114 84 68 128 68 190 C68 282 140 352 256 432 L236 340 L278 270 L226 208 Z"
HEART_R = "M256 134 C272 104 302 84 340 84 C398 84 444 128 444 190 C444 282 372 352 256 432 L236 340 L278 270 L226 208 Z"


def heart(s, x=256, y=256, sc=1.0, color=A2, hi=A2L, rot=0):
    s.open(transform=f"translate({x} {y}) rotate({rot}) scale({sc}) translate(-256 -256)")
    s.F("path", d=HEART, fill=color)
    s.F("ellipse", outline=False, cx=150, cy=172, rx=38, ry=24, fill=hi, transform="rotate(-40 150 172)")
    s.close()


def sparkle(s, x, y, r, color=A1):
    s.F("polygon", points=star_pts(x, y, r, r * 0.32, 4), fill=color)


def star(s, x=256, y=266, r=196, color=A2, hi=A2L):
    s.F("polygon", points=star_pts(x, y, r, r * 0.44, 5), fill=color)
    s.F("polygon", outline=False, points=star_pts(x - r * 0.18, y - r * 0.12, r * 0.22, r * 0.1, 5), fill=hi)


D["heart"] = lambda s: s.open("part-heart", "256 256") or (heart(s), s.close())


@draw("broken-heart")
def _(s):
    s.F("path", d=HEART_L, fill=A2, transform="translate(-16 8) rotate(-6 256 432)")
    s.F("path", d=HEART_R, fill=A2, transform="translate(16 8) rotate(6 256 432)")


@draw("two-hearts")
def _(s):
    heart(s, 200, 290, 0.62, rot=-12)
    heart(s, 330, 210, 0.5, A1, A1L, rot=14)


@draw("heart-with-arrow")
def _(s):
    s.T("M96 400 L250 268", THEME["dark"], 16)
    heart(s, 256, 256, 0.82)
    s.T("M262 258 L392 146", THEME["dark"], 16)
    s.F("polygon", points="430,112 360,132 410,182", fill=A1)
    s.F("polygon", points="96,400 60,396 76,374 110,388", fill=A1)
    s.F("polygon", points="96,400 100,436 122,420 108,388", fill=A1)


D["heart-outline"] = lambda s: s.T(HEART, A2, 34)


@draw("sparkling-heart")
def _(s):
    heart(s, 240, 270, 0.82)
    sparkle(s, 410, 120, 48); sparkle(s, 104, 110, 30); sparkle(s, 420, 380, 30)


@draw("heart-burst")
def _(s):
    heart(s, 256, 280, 0.66)
    for x, y, sc, r in ((110, 130, 0.22, -20), (390, 110, 0.26, 18), (440, 260, 0.18, 24), (80, 300, 0.18, -24), (250, 70, 0.16, 0)):
        heart(s, x, y, sc, A1, A1L, r)


D["star-symbol"] = lambda s: star(s)


@draw("star-outline")
def _(s):
    s.T("M" + " L".join(star_pts(256, 270, 190, 84, 5).split()) + " Z", A2, 30)


@draw("half-star")
def _(s):
    pts = star_pts(256, 266, 196, 86, 5).split()
    s.F("polygon", outline=False, points=" ".join(pts), fill=THEME["mid"])
    s.F("polygon", outline=False, points=" ".join(pts[i] for i in (0, 9, 8, 7, 6, 5)), fill=A2)
    s.F("polygon", points=" ".join(pts), fill="none")


@draw("five-star-rating")
def _(s):
    for i in range(5):
        star(s, 72 + i * 92, 262, 50)


@draw("sparkle")
def _(s):
    s.open("part-glow", "240 270")
    sparkle(s, 230, 280, 170, A2)
    sparkle(s, 400, 120, 70)
    sparkle(s, 400, 400, 40)
    s.close()


D["four-point-star"] = lambda s: sparkle(s, 256, 256, 200, A2)


@draw("peace-symbol")
def _(s):
    s.T("M256 76 A180 180 0 1 1 255.9 76 M256 76 V436 M256 256 L130 384 M256 256 L382 384", A1, 36)


# ---------------------------------------------------------------- badges (themed)
def scallop(s, r=200, color=A1, n=24):
    s.F("polygon", points=star_pts(256, 256, r, r * 0.9, n), fill=color)


@draw("badge")
def _(s):
    scallop(s)
    s.F("circle", cx=256, cy=256, r=136, fill=A1L)
    star(s, 256, 262, 96)


@draw("ribbon-badge")
def _(s):
    s.F("polygon", points="176,300 130,470 186,440 214,490 250,320", fill=A2)
    s.F("polygon", points="336,300 382,470 326,440 298,490 262,320", fill=A2)
    s.open(transform="translate(256 196) scale(0.74) translate(-256 -256)")
    scallop(s); s.F("circle", cx=256, cy=256, r=130, fill=A1L)
    s.close()


SHIELD = "M256 56 L424 118 V246 C424 352 352 426 256 460 C160 426 88 352 88 246 V118 Z"


@draw("shield-badge")
def _(s):
    s.F("path", d=SHIELD, fill=A1)
    s.F("path", d="M256 110 L370 152 V246 C370 322 322 376 256 404 Z", fill=A1L, outline=False)
    star(s, 256, 252, 92, A2)


@draw("verified-badge")
def _(s):
    scallop(s, 208, A1, 16)
    s.T("M170 262 L232 322 L350 196", LIGHT, 40)


D["starburst-badge"] = lambda s: s.F("polygon", points=star_pts(256, 256, 214, 172, 18), fill=A2)


@draw("banner-ribbon")
def _(s):
    s.F("polygon", points="30,220 120,220 120,330 30,330 66,275", fill="#2C6BD6")
    s.F("polygon", points="482,220 392,220 392,330 482,330 446,275", fill="#2C6BD6")
    s.F("polygon", points="96,330 120,330 120,300", fill=THEME["dark"])
    s.F("polygon", points="416,330 392,330 392,300", fill=THEME["dark"])
    s.F("rect", x=96, y=184, width=320, height=118, rx=8, fill=A1)


@draw("corner-ribbon")
def _(s):
    s.F("rect", x=70, y=70, width=372, height=372, rx=36, fill=LIGHT)
    s.F("polygon", points="250,70 330,70 442,182 442,262", fill=A2)


@draw("pin-badge")
def _(s):
    s.F("circle", cx=256, cy=256, r=190, fill=A1)
    s.F("circle", cx=256, cy=256, r=140, fill=A2)
    star(s, 256, 262, 80, LIGHT, A2L)
    s.F("ellipse", outline=False, cx=170, cy=150, rx=40, ry=22, fill=A1L, transform="rotate(-40 170 150)")


@draw("laurel-wreath")
def _(s):
    for side in (1, -1):
        s.open(transform="translate(512 0) scale(-1 1)" if side < 0 else None)
        p0, p1, p2 = (236, 444), (70, 390), (134, 110)
        s.T(f"M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}", A2, 12)
        for k in range(7):
            t = 0.14 + k * 0.13
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
            dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
            a = math.degrees(math.atan2(dy, dx))
            for sgn in (1, -1):
                lx = x + 30 * math.cos(math.radians(a + sgn * 50))
                ly = y + 30 * math.sin(math.radians(a + sgn * 50))
                s.F("ellipse", cx=f"{lx:.0f}", cy=f"{ly:.0f}", rx=32, ry=14, fill=A2,
                    transform=f"rotate({a + sgn * 50:.0f} {lx:.0f} {ly:.0f})")
        s.close()


@draw("number-one-badge")
def _(s):
    scallop(s, 208, A2, 18)
    s.F("circle", cx=256, cy=256, r=140, fill=A1)
    s.T("M226 196 L272 160 V350 M222 352 H318", LIGHT, 34)


@draw("level-badge")
def _(s):
    s.F("path", d=SHIELD, fill=A1)
    for y in (150, 230, 310):
        s.T(f"M166 {y} L256 {y + 56} L346 {y}", LIGHT, 34)


# ---------------------------------------------------------------- common symbols (mono)
RING196 = f'<circle cx="256" cy="256" r="196" fill="none" stroke="{INK}" stroke-width="24"/>'


@draw("copyright-symbol")
def _(s):
    s.raw(RING196); s.M("M326 196 A96 96 0 1 0 326 316", w=30)


@draw("trademark-symbol")
def _(s):
    s.M("M70 170 H240 M155 170 V352 M286 352 V170 L352 280 L418 170 V352", w=30)


@draw("registered-symbol")
def _(s):
    s.raw(RING196); s.M("M206 356 V156 H274 C338 156 338 256 274 256 H206 M268 256 L326 356", w=30)


@draw("male-symbol")
def _(s):
    s.raw(f'<circle cx="214" cy="298" r="114" fill="none" stroke="{INK}" stroke-width="28"/>')
    s.M("M296 216 L420 92 M326 92 H420 V186", w=28)


@draw("female-symbol")
def _(s):
    s.raw(f'<circle cx="256" cy="196" r="120" fill="none" stroke="{INK}" stroke-width="28"/>')
    s.M("M256 316 V456 M190 392 H322", w=28)


D["lightning-bolt-symbol"] = lambda s: s.raw(
    f'<polygon points="292,56 128,292 242,292 208,456 384,204 270,204" fill="{INK}" stroke="{INK}" stroke-width="24" stroke-linejoin="round"/>')
D["flame-symbol"] = lambda s: s.raw(
    f'<path d="M256 460 C158 460 108 392 108 320 C108 236 182 200 190 112 C242 154 254 200 248 244 '
    f'C282 214 294 170 288 112 C364 164 404 248 404 320 C404 400 350 460 256 460Z" fill="{INK}"/>')


@draw("crosshair")
def _(s):
    s.raw(f'<circle cx="256" cy="256" r="150" fill="none" stroke="{INK}" stroke-width="24"/>')
    s.M("M256 60 V180 M256 332 V452 M60 256 H180 M332 256 H452")
    dot(s, 256, 256, 18)


@draw("sos-signal")
def _(s):
    def S(cx):
        return (f"M{cx + 46} 190 C{cx + 26} 160 {cx - 52} 162 {cx - 48} 214 C{cx - 44} 260 {cx + 48} 252 {cx + 48} 306 "
                f"C{cx + 48} 360 {cx - 30} 368 {cx - 54} 330")
    s.M(S(110) + " " + S(402), w=30)
    s.raw(f'<ellipse cx="256" cy="260" rx="62" ry="92" fill="none" stroke="{INK}" stroke-width="30"/>')


def clip_rect(poly, x0, y0, x1, y1):
    def clip(pts, inside, inter):
        out = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            if inside(p):
                if not inside(q):
                    out.append(inter(q, p))
                out.append(p)
            elif inside(q):
                out.append(inter(q, p))
        return out

    def ix(xv):
        return lambda a, b: (xv, a[1] + (b[1] - a[1]) * (xv - a[0]) / (b[0] - a[0]))
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1))):
        poly = clip(poly, inside, inter)
        if not poly:
            break
    return poly


@draw("prohibited-zone-stripes")
def _(s):
    x0, y0, x1, y1 = 56, 176, 456, 336
    for x in range(x0 - 160, x1 + 160, 100):
        poly = clip_rect([(x, y0), (x + 50, y0), (x + 50 + 160, y1), (x + 160, y1)], x0, y0, x1, y1)
        if len(poly) >= 3:
            s.raw(f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in poly)}" fill="{INK}"/>')
    s.raw(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="12" fill="none" stroke="{INK}" stroke-width="24"/>')


# ---------------------------------------------------------------- UI symbols, part 1 (mono)
def fill(s, tag, **a):
    s.raw(f"<{tag} " + " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
          + f' fill="{INK}" stroke="{INK}" stroke-width="24" stroke-linejoin="round"/>')


D["play-button"] = lambda s: fill(s, "polygon", points="176,112 400,256 176,400")


@draw("pause-button")
def _(s):
    fill(s, "rect", x=150, y=116, width=64, height=280); fill(s, "rect", x=298, y=116, width=64, height=280)


D["stop-button"] = lambda s: fill(s, "rect", x=132, y=132, width=248, height=248, rx=20)
D["record-button"] = lambda s: s.raw(f'<circle cx="256" cy="256" r="150" fill="{INK}"/>')


@draw("fast-forward-button")
def _(s):
    fill(s, "polygon", points="80,140 250,256 80,372"); fill(s, "polygon", points="262,140 432,256 262,372")


@draw("rewind-button")
def _(s):
    fill(s, "polygon", points="432,140 262,256 432,372"); fill(s, "polygon", points="250,140 80,256 250,372")


@draw("next-track-button")
def _(s):
    fill(s, "polygon", points="120,130 320,256 120,382"); fill(s, "rect", x=352, y=130, width=40, height=252)


@draw("previous-track-button")
def _(s):
    fill(s, "polygon", points="392,130 192,256 392,382"); fill(s, "rect", x=120, y=130, width=40, height=252)


@draw("shuffle-symbol")
def _(s):
    s.M("M80 160 H160 C260 160 252 352 352 352 H420 " + head(420, 352, 0, 64) +
        " M80 352 H160 C200 352 220 320 236 290 M276 222 C292 192 312 160 352 160 H420 " + head(420, 160, 0, 64))


@draw("repeat-symbol")
def _(s):
    s.M("M110 280 V230 C110 186 146 160 190 160 H400 " + head(400, 160, 0, 64) +
        " M402 232 V282 C402 326 366 352 322 352 H112 " + head(112, 352, 180, 64))


SPEAKER = "M100 206 H170 L262 120 V392 L170 306 H100 Z"


@draw("volume-symbol")
def _(s):
    s.M(SPEAKER); s.M("M322 196 C352 226 352 286 322 316 M370 150 C426 206 426 306 370 362")


@draw("mute-symbol")
def _(s):
    s.M(SPEAKER); s.M("M324 196 L428 316 M428 196 L324 316")


@draw("power-symbol")
def _(s):
    s.M("M176 144 A160 160 0 1 0 336 144 M256 70 V250", w=30)


D["home-symbol"] = lambda s: s.M("M80 250 L256 92 L432 250 M128 210 V420 H212 V310 H300 V420 H384 V210")
D["menu-symbol"] = lambda s: s.M("M96 140 H416 M96 256 H416 M96 372 H416", w=32)


@draw("three-dots-menu")
def _(s):
    for y in (136, 256, 376):
        dot(s, 256, y, 38)


@draw("search-symbol")
def _(s):
    s.raw(f'<circle cx="220" cy="220" r="130" fill="none" stroke="{INK}" stroke-width="30"/>')
    s.M("M316 316 L426 426", w=40)


@draw("settings-gear")
def _(s):
    pts = []
    for i in range(8):
        base = i * 45
        for da, r in ((-14, 150), (-9, 196), (9, 196), (14, 150)):
            x, y = arc_pt(256, 256, r, base + da)
            pts.append(f"{x:.1f},{y:.1f}")
    s.raw(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="26" stroke-linejoin="round"/>')
    s.raw(f'<circle cx="256" cy="256" r="58" fill="none" stroke="{INK}" stroke-width="26"/>')


@draw("notification-bell")
def _(s):
    s.open("part-bell", "256 80")
    s.M("M120 360 C150 330 152 300 152 240 C152 170 196 116 256 116 C316 116 360 170 360 240 C360 300 362 330 392 360 Z M256 80 V116")
    s.M("M216 410 C226 440 286 440 296 410")
    s.close()


@draw("add-button")
def _(s):
    s.raw(RING196); s.M("M256 160 V352 M160 256 H352")


@draw("close-button")
def _(s):
    s.raw(RING196); s.M("M186 186 L326 326 M326 186 L186 326")


@draw("download-symbol")
def _(s):
    s.M("M256 80 V300 " + head(256, 300, 90, 100) + " M90 320 V420 H422 V320")


@draw("upload-symbol")
def _(s):
    s.M("M256 300 V80 " + head(256, 80, -90, 100) + " M90 320 V420 H422 V320")


@draw("share-symbol")
def _(s):
    s.M("M170 256 L340 150 M170 256 L340 362")
    for x, y in ((150, 256), (362, 136), (362, 376)):
        s.raw(f'<circle cx="{x}" cy="{y}" r="60" fill="#FFFFFF" stroke="{INK}" stroke-width="24"/>')


# ---------------------------------------------------------------- UI symbols, part 2 (mono)
def ring(s, cx, cy, r, w=24):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w}"/>')


@draw("link-symbol")
def _(s):
    s.M("M236 300 L300 236 M226 214 L262 178 C302 138 362 138 384 168 C410 196 400 248 366 278 L330 314 "
        "M286 298 L250 334 C210 374 150 374 128 344 C102 316 112 264 146 234 L182 198", w=30)


@draw("external-link-symbol")
def _(s):
    s.M("M220 120 H140 C116 120 104 132 104 156 V372 C104 396 116 408 140 408 H356 C380 408 392 396 392 372 V292 "
        "M260 252 L408 104 M300 104 H408 V212")


@draw("attachment-symbol")
def _(s):
    s.M("M330 190 L200 320 C176 344 204 372 228 348 L370 206 C420 156 356 92 306 142 L160 288 C110 338 180 408 230 358 L356 232")


LOCK_BODY = '<rect x="120" y="230" width="272" height="210" rx="34" fill="none" stroke="' + INK + '" stroke-width="24"/>'


@draw("lock-symbol")
def _(s):
    s.raw(LOCK_BODY); s.M("M176 230 V170 C176 66 336 66 336 170 V230 M256 310 V360")


@draw("unlock-symbol")
def _(s):
    s.raw(LOCK_BODY); s.M("M176 230 V170 C176 66 330 66 336 150 M256 310 V360")


EYE = "M56 256 C110 156 186 120 256 120 C326 120 402 156 456 256 C402 356 326 392 256 392 C186 392 110 356 56 256Z"


@draw("eye-symbol")
def _(s):
    s.M(EYE); ring(s, 256, 256, 70)


@draw("hidden-symbol")
def _(s):
    s.M(EYE); ring(s, 256, 256, 70); s.M("M96 96 L416 416", w=30)


@draw("user-symbol")
def _(s):
    ring(s, 256, 176, 86); s.M("M100 430 C100 340 170 300 256 300 C342 300 412 340 412 430")


@draw("group-symbol")
def _(s):
    ring(s, 256, 180, 70); s.M("M136 420 C136 340 190 304 256 304 C322 304 376 340 376 420")
    ring(s, 120, 220, 48, 20); ring(s, 392, 220, 48, 20)
    s.M("M40 380 C40 330 74 300 116 300 M472 380 C472 330 438 300 396 300", w=20)


@draw("location-pin")
def _(s):
    s.M("M256 460 C200 380 120 300 120 210 C120 130 182 72 256 72 C330 72 392 130 392 210 C392 300 312 380 256 460Z")
    ring(s, 256, 210, 56)


@draw("wifi-symbol")
def _(s):
    s.M("M70 210 C176 104 336 104 442 210 M130 276 C200 206 312 206 382 276 M190 340 C226 304 286 304 322 340", w=30)
    dot(s, 256, 400, 30)


@draw("signal-bars")
def _(s):
    for i, h in enumerate((80, 150, 220, 300)):
        fill(s, "rect", x=92 + i * 90, y=420 - h, width=48, height=h, rx=6)


def battery(s, level, charging=False):
    s.raw(f'<rect x="70" y="160" width="340" height="192" rx="30" fill="none" stroke="{INK}" stroke-width="24"/>')
    fill(s, "rect", x=424, y=220, width=20, height=72, rx=6)
    if level:
        fill(s, "rect", x=112, y=202, width=int(256 * level), height=108, rx=10)
    if charging:
        s.raw('<polygon points="270,170 190,268 250,268 230,342 318,236 258,236" fill="#FFFFFF" stroke="'
              + INK + '" stroke-width="12" stroke-linejoin="round"/>')


D["battery-full-symbol"] = lambda s: battery(s, 1.0)
D["battery-low-symbol"] = lambda s: battery(s, 0.2)
D["battery-charging-symbol"] = lambda s: battery(s, 0.6, True)


@draw("loading-spinner")
def _(s):
    s.open("part-spinner", "256 256")
    for i in range(8):
        a = i * 45
        x1, y1 = arc_pt(256, 256, 110, a); x2, y2 = arc_pt(256, 256, 180, a)
        op = 0.25 + 0.75 * i / 7
        s.raw(f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{INK}" stroke-opacity="{op:.2f}" stroke-width="34" stroke-linecap="round"/>')
    s.close()


@draw("progress-bar")
def _(s):
    s.raw(f'<rect x="56" y="216" width="400" height="80" rx="40" fill="none" stroke="{INK}" stroke-width="24"/>')
    fill(s, "rect", x=92, y=244, width=200, height=24, rx=12)


@draw("toggle-switch-on")
def _(s):
    fill(s, "rect", x=72, y=156, width=368, height=200, rx=100)
    s.raw('<circle cx="340" cy="256" r="72" fill="#FFFFFF"/>')


@draw("toggle-switch-off")
def _(s):
    s.raw(f'<rect x="72" y="156" width="368" height="200" rx="100" fill="none" stroke="{INK}" stroke-width="24"/>')
    fill(s, "circle", cx=172, cy=256, r=56)


@draw("slider-control")
def _(s):
    s.M("M70 256 H442", w=24)
    s.raw(f'<circle cx="220" cy="256" r="54" fill="#FFFFFF" stroke="{INK}" stroke-width="24"/>')


D["mouse-pointer"] = lambda s: fill(s, "polygon", points="150,80 150,400 236,320 290,440 340,418 288,300 400,300")


@draw("hand-cursor")
def _(s):
    s.M("M196 300 V110 C196 76 244 76 244 110 V250 M244 230 C244 196 292 196 292 230 V262 M292 240 C292 208 340 208 340 240 V270 "
        "M340 252 C340 222 388 222 388 252 V340 C388 410 340 450 280 450 H250 C210 450 186 430 166 400 L112 318 C96 292 128 266 152 286 L196 330")


@draw("trash-symbol")
def _(s):
    s.M("M90 140 H422 M200 140 V100 H312 V140 M130 140 L152 430 H360 L382 140 M216 210 V370 M296 210 V370")


@draw("edit-symbol")
def _(s):
    s.M("M330 96 L416 182 L196 402 L96 416 L110 316 Z M290 136 L376 222")


@draw("copy-symbol")
def _(s):
    s.raw(f'<rect x="176" y="176" width="248" height="268" rx="30" fill="none" stroke="{INK}" stroke-width="24"/>')
    s.M("M120 360 H110 C96 360 88 352 88 338 V100 C88 86 96 78 110 78 H310 C324 78 332 86 332 100 V120")


@draw("save-symbol")
def _(s):
    s.M("M96 96 H350 L416 162 V416 H96 Z M170 96 V200 H330 V96 M150 416 V290 H362 V416")


D["filter-symbol"] = lambda s: s.M("M76 104 H436 L292 280 V420 L220 380 V280 Z")


@draw("sort-symbol")
def _(s):
    s.M("M176 420 V100 " + head(176, 100, -90, 70) + " M336 92 V412 " + head(336, 412, 90, 70))


@draw("grid-view-symbol")
def _(s):
    for x in (96, 280):
        for y in (96, 280):
            s.raw(f'<rect x="{x}" y="{y}" width="136" height="136" rx="22" fill="none" stroke="{INK}" stroke-width="24"/>')


@draw("list-view-symbol")
def _(s):
    for y in (136, 256, 376):
        dot(s, 108, y, 26)
    s.M("M184 136 H420 M184 256 H420 M184 376 H420")


@draw("info-symbol")
def _(s):
    s.raw(RING196); dot(s, 256, 166, 24); s.M("M256 230 V362", w=32)


D["bookmark-symbol"] = lambda s: s.M("M140 80 H372 V440 L256 340 L140 440 Z")
D["flag-symbol"] = lambda s: s.M("M130 460 V70 M130 90 C210 50 250 140 390 100 V280 C250 320 210 230 130 270")


@draw("zoom-in-symbol")
def _(s):
    ring(s, 220, 220, 130, 30); s.M("M316 316 L426 426", w=40); s.M("M220 160 V280 M160 220 H280")


@draw("zoom-out-symbol")
def _(s):
    ring(s, 220, 220, 130, 30); s.M("M316 316 L426 426", w=40); s.M("M160 220 H280")


@draw("camera-symbol")
def _(s):
    s.M("M70 180 C70 158 86 146 106 146 H170 L200 104 H312 L342 146 H406 C426 146 442 158 442 180 V384 C442 404 426 416 406 416 H106 C86 416 70 404 70 384 Z")
    ring(s, 256, 280, 82)


@draw("image-symbol")
def _(s):
    s.raw(f'<rect x="70" y="96" width="372" height="320" rx="36" fill="none" stroke="{INK}" stroke-width="24"/>')
    s.M("M96 380 L210 260 L290 340 L340 290 L420 370"); dot(s, 330, 180, 34)


D["chat-symbol"] = lambda s: s.M(
    "M90 120 C90 100 104 88 124 88 H388 C408 88 422 100 422 120 V310 C422 330 408 342 388 342 H200 L120 420 V342 H124 "
    "C104 342 90 330 90 310 Z")
D["send-symbol"] = lambda s: s.M("M70 256 L440 90 L360 440 L250 300 Z M250 300 L440 90")
D["refresh-button"] = lambda s: arc_arrow(s, 256, 256, 160, -100, 200)


@draw("login-symbol")
def _(s):
    s.M("M290 90 H390 C410 90 422 102 422 122 V390 C422 410 410 422 390 422 H290 M90 256 H300 " + head(300, 256, 0, 76))


@draw("logout-symbol")
def _(s):
    s.M("M222 90 H122 C102 90 90 102 90 122 V390 C90 410 102 422 122 422 H222 M200 256 H430 " + head(430, 256, 0, 76))


# ---------------------------------------------------------------- road signs (keep)
from draw_lib import stroke_text  # noqa: E402

RED, WHITE, BLUE, BLACK = C["red"], C["white"], C["darkblue"], C["black"]


def picto(s, fn, x=256, y=280, sc=1.0, color=BLACK):
    s.open(transform=f"translate({x} {y}) scale({sc})")
    fn(s, color)
    s.close()


def warn(s, fn, sc=0.95):
    s.F("path", d="M256 58 C270 58 280 66 288 80 L462 384 C476 410 462 430 434 430 H78 C50 430 36 410 50 384 L224 80 C232 66 242 58 256 58Z", fill=RED)
    s.F("polygon", outline=False, points="256,132 410,396 102,396", fill=WHITE)
    picto(s, fn, 256, 304, sc * 1.02)


def prohib(s, fn=None, slash=True, inner=WHITE, sc=1.0):
    s.F("circle", cx=256, cy=256, r=204, fill=RED)
    s.F("circle", outline=False, cx=256, cy=256, r=158, fill=inner)
    if fn:
        picto(s, fn, 256, 256, sc)
    if slash:
        s.raw(f'<path d="M146 146 L366 366" stroke="{RED}" stroke-width="38"/>')


def mandatory(s, fn, sc=1.0):
    s.F("circle", cx=256, cy=256, r=204, fill=BLUE)
    picto(s, fn, 256, 256, sc, WHITE)


def info(s, fn, sc=1.0, bg=BLUE):
    s.F("rect", x=60, y=60, width=392, height=392, rx=44, fill=bg)
    picto(s, fn, 256, 256, sc, WHITE)


def st(s, d, color, w=18):
    s.raw(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def fl(s, tag, color, **a):
    s.raw(f"<{tag} " + " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items()) + f' fill="{color}"/>')


# pictograms in a -100..100 box
def p_walker(s, c):
    fl(s, "circle", c, cx=12, cy=-80, r=18)
    st(s, "M6 -54 L-6 16 M-32 -18 L4 -44 L36 -8 M-6 16 L-38 80 M-6 16 L26 42 L30 84", c, 18)


def p_children(s, c):
    s.open(transform="translate(-38 14) scale(0.72)"); p_walker(s, c); s.close()
    s.open(transform="translate(40 26) scale(0.6)"); p_walker(s, c); s.close()


def p_car(s, c, body=None):
    fl(s, "path", body or c, d="M-86 34 V2 L-58 -32 H44 L76 2 H88 V34 Z")
    fl(s, "path", WHITE, d="M-50 -22 H-8 V0 H-66 Z M4 -22 H40 L58 0 H4 Z")
    for x in (-50, 52):
        fl(s, "circle", c, cx=x, cy=38, r=18); fl(s, "circle", WHITE, cx=x, cy=38, r=7)


def p_bus(s, c):
    fl(s, "rect", c, x=-88, y=-56, width=176, height=100, rx=14)
    for x in (-74, -30, 14):
        fl(s, "rect", WHITE if c != WHITE else BLUE, x=x, y=-42, width=36, height=34, rx=5)
    fl(s, "rect", WHITE if c != WHITE else BLUE, x=56, y=-42, width=20, height=70, rx=4)
    for x in (-52, 52):
        fl(s, "circle", c, cx=x, cy=50, r=18)


def p_bike(s, c):
    for x in (-50, 50):
        s.raw(f'<circle cx="{x}" cy="30" r="34" fill="none" stroke="{c}" stroke-width="12"/>')
    st(s, "M-50 30 L-12 -24 H34 L50 30 M-12 -24 L4 30 L34 -24 M-22 -40 H0 M34 -24 L28 -48 H48", c, 12)


def p_deer(s, c):
    fl(s, "ellipse", c, cx=-8, cy=0, rx=56, ry=24)
    st(s, "M-46 14 L-52 78 M-30 16 L-26 78 M24 14 L20 78 M38 10 L46 78", c, 11)
    st(s, "M38 -8 L60 -52", c, 16)
    fl(s, "ellipse", c, cx=70, cy=-58, rx=20, ry=11)
    st(s, "M60 -64 L52 -96 M56 -80 L42 -92 M68 -66 L80 -96 M74 -82 L90 -90", c, 7)


def p_camel(s, c):
    fl(s, "path", c, d="M-74 14 C-74 -26 -46 -48 -22 -24 C-2 -56 34 -48 44 -12 C54 2 50 16 40 16 Z")
    st(s, "M-58 12 L-62 80 M-40 14 L-38 80 M18 14 L16 80 M34 14 L38 80", c, 11)
    st(s, "M40 0 C60 -10 70 -40 76 -62", c, 14)
    fl(s, "ellipse", c, cx=84, cy=-64, rx=17, ry=9)


def p_cow(s, c):
    fl(s, "rect", c, x=-70, y=-30, width=112, height=56, rx=16)
    st(s, "M-56 20 V80 M-36 20 V80 M16 20 V80 M32 20 V80", c, 12)
    fl(s, "ellipse", c, cx=62, cy=-26, rx=24, ry=18)
    st(s, "M50 -42 L42 -60 M74 -42 L82 -60 M-70 -20 C-86 -10 -86 20 -82 40", c, 7)


def p_elephant(s, c):
    fl(s, "ellipse", c, cx=-14, cy=-6, rx=62, ry=44)
    fl(s, "circle", c, cx=46, cy=-22, r=34)
    st(s, "M72 -10 C88 22 80 52 70 74", c, 15)
    for x in (-54, -30, 6, 26):
        fl(s, "rect", c, x=x, y=20, width=20, height=58, rx=6)
    fl(s, "ellipse", WHITE, cx=36, cy=-22, rx=12, ry=20)


def p_kangaroo(s, c):
    st(s, "M-26 44 C-60 70 -80 84 -100 88", c, 18)
    fl(s, "ellipse", c, cx=-6, cy=-4, rx=32, ry=58, transform="rotate(22 -6 -4)")
    fl(s, "ellipse", c, cx=2, cy=44, rx=34, ry=24)
    fl(s, "ellipse", c, cx=30, cy=-66, rx=24, ry=14, transform="rotate(14 30 -66)")
    st(s, "M16 -76 L8 -100 M26 -78 L24 -102 M18 -26 L40 -6 M-4 64 L56 86", c, 10)


def p_train(s, c):
    fl(s, "rect", c, x=-56, y=-86, width=112, height=146, rx=24)
    fl(s, "rect", WHITE, x=-38, y=-66, width=76, height=50, rx=8)
    for x in (-30, 30):
        fl(s, "circle", WHITE, cx=x, cy=26, r=10)
    st(s, "M-40 64 L-62 90 M40 64 L62 90", c, 12)


def p_lights(s, c):
    fl(s, "rect", BLACK, x=-34, y=-96, width=68, height=192, rx=20)
    for y, col in ((-56, RED), (0, C["yellow"]), (56, C["green"])):
        fl(s, "circle", col, cx=0, cy=y, r=22)


def p_horn(s, c):
    fl(s, "path", c, d="M-80 -24 H-30 L56 -66 V66 L-30 24 H-80 Z")
    st(s, "M76 -40 C96 -20 96 20 76 40", c, 12)


def p_pump(s, c):
    fl(s, "rect", c, x=-56, y=-76, width=80, height=150, rx=10)
    fl(s, "rect", BLUE if c == WHITE else WHITE, x=-42, y=-60, width=52, height=40, rx=6)
    st(s, "M24 -48 H50 V40 C50 58 72 58 72 40 V-30 L56 -50", c, 11)


def bent_arrow(s, c, flip=False):
    s.open(transform="scale(-1 1)" if flip else None)
    st(s, "M-30 86 V0 C-30 -40 -4 -56 36 -56", c, 26)
    fl(s, "polygon", c, points="30,-94 92,-56 30,-18")
    s.close()


@draw("stop-sign")
def _(s):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (arc_pt(256, 256, 210, 22.5 + i * 45) for i in range(8)))
    s.F("polygon", points=pts, fill=RED)
    ipts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (arc_pt(256, 256, 186, 22.5 + i * 45) for i in range(8)))
    s.raw(f'<polygon points="{ipts}" fill="none" stroke="{WHITE}" stroke-width="10" stroke-linejoin="round"/>')
    stroke_text(s, "STOP", 256, 256, 104, WHITE, 24)


@draw("give-way-sign")
def _(s):
    s.F("path", d="M256 454 C270 454 280 446 288 432 L462 128 C476 102 462 82 434 82 H78 C50 82 36 102 50 128 L224 432 C232 446 242 454 256 454Z", fill=RED)
    s.F("polygon", outline=False, points="256,380 410,116 102,116", fill=WHITE)


@draw("no-entry-sign")
def _(s):
    s.F("circle", cx=256, cy=256, r=204, fill=RED)
    s.F("rect", outline=False, x=120, y=222, width=272, height=68, rx=12, fill=WHITE)


@draw("one-way-sign")
def _(s):
    s.F("rect", x=50, y=166, width=412, height=180, rx=26, fill=BLUE)
    fl(s, "polygon", WHITE, points="98,226 322,226 322,190 414,256 322,322 322,286 98,286")


@draw("speed-limit-sign")
def _(s):
    prohib(s, slash=False); stroke_text(s, "50", 256, 256, 150, BLACK, 26)


@draw("parking-sign")
def _(s):
    info(s, lambda s, c: None); stroke_text(s, "P", 256, 256, 230, WHITE, 40)


@draw("no-parking-sign")
def _(s):
    prohib(s, inner=BLUE)


@draw("no-stopping-sign")
def _(s):
    prohib(s, inner=BLUE, slash=False)
    s.raw(f'<path d="M146 146 L366 366 M366 146 L146 366" stroke="{RED}" stroke-width="38"/>')


def p_uturn(s, c):
    st(s, "M-40 80 V-10 C-40 -80 50 -80 50 -10 V20", c, 26)
    fl(s, "polygon", c, points="12,10 50,70 88,10")


D["no-u-turn-sign"] = lambda s: prohib(s, p_uturn)
D["no-left-turn-sign"] = lambda s: prohib(s, lambda s, c: bent_arrow(s, c, True))
D["no-right-turn-sign"] = lambda s: prohib(s, bent_arrow)


@draw("no-overtaking-sign")
def _(s):
    prohib(s, slash=False)
    picto(s, lambda s, c: p_car(s, c, RED), 196, 256, 0.62)
    picto(s, p_car, 316, 256, 0.62)


D["no-horn-sign"] = lambda s: prohib(s, p_horn, sc=0.9)


@draw("roundabout-sign")
def _(s):
    s.F("circle", cx=256, cy=256, r=204, fill=BLUE)
    for a in (-90, 30, 150):
        x0, y0 = arc_pt(256, 256, 100, a); x1, y1 = arc_pt(256, 256, 100, a + 80)
        st(s, f"M{x0:.0f} {y0:.0f} A100 100 0 0 1 {x1:.0f} {y1:.0f}", WHITE, 26)
        tip = arc_pt(256, 256, 100, a + 104)
        b1 = arc_pt(256, 256, 64, a + 78); b2 = arc_pt(256, 256, 136, a + 78)
        fl(s, "polygon", WHITE, points=f"{tip[0]:.0f},{tip[1]:.0f} {b1[0]:.0f},{b1[1]:.0f} {b2[0]:.0f},{b2[1]:.0f}")


D["traffic-lights-ahead-sign"] = lambda s: warn(s, p_lights, 0.85)


@draw("pedestrian-crossing-sign")
def _(s):
    warn(s, lambda s, c: (p_walker(s, c), [fl(s, "rect", c, x=-90 + i * 40, y=88, width=22, height=12) for i in range(5)]))


D["school-zone-sign"] = lambda s: warn(s, p_children)


def p_works(s, c):
    fl(s, "circle", c, cx=-22, cy=-74, r=16)
    st(s, "M-26 -52 L-10 14 M-40 -20 L10 -40 L40 10 M-10 14 L-46 80 M-10 14 L16 44 L14 84", c, 16)
    st(s, "M40 10 L62 72", c, 8)
    fl(s, "polygon", c, points="30,86 96,86 70,50")


D["road-works-sign"] = lambda s: warn(s, p_works)


@draw("slippery-road-sign")
def _(s):
    warn(s, lambda s, c: (picto(s, p_car, 0, -26, 0.7), st(s, "M-50 40 C-70 60 -30 70 -50 92 M30 40 C10 60 50 70 30 92", c, 9)))


D["sharp-bend-sign"] = lambda s: warn(s, bent_arrow)
D["steep-hill-sign"] = lambda s: warn(s, lambda s, c: fl(s, "polygon", c, points="-92,80 92,80 92,-30"))


@draw("falling-rocks-sign")
def _(s):
    warn(s, lambda s, c: (fl(s, "polygon", c, points="96,86 96,-90 36,-90 58,86"),
                          [fl(s, "circle", c, cx=x, cy=y, r=r) for x, y, r in ((8, -46, 14), (-18, 6, 18), (-46, 62, 22), (14, 54, 12))],
                          st(s, "M-96 86 H96", c, 10)))


D["road-narrows-sign"] = lambda s: warn(s, lambda s, c: st(s, "M-50 -80 V-14 L-22 26 V86 M50 -80 V-14 L22 26 V86", c, 16))
D["speed-bump-sign"] = lambda s: warn(s, lambda s, c: fl(s, "path", c, d="M-92 70 H-50 C-30 -10 30 -10 50 70 H92 V82 H-92 Z"))


@draw("two-way-traffic-sign")
def _(s):
    def arrows(s, c):
        st(s, "M-34 86 V-50", c, 18); fl(s, "polygon", c, points="-62,-40 -34,-92 -6,-40")
        st(s, "M34 -86 V50", c, 18); fl(s, "polygon", c, points="6,40 34,92 62,40")
    warn(s, arrows)


D["level-crossing-sign"] = lambda s: warn(s, p_train, 0.9)
D["animal-crossing-sign"] = lambda s: warn(s, p_deer)
D["camel-crossing-sign"] = lambda s: warn(s, p_camel)
D["cattle-crossing-sign"] = lambda s: warn(s, p_cow)
D["elephant-crossing-sign"] = lambda s: warn(s, p_elephant)


@draw("kangaroo-crossing-sign")
def _(s):
    s.F("polygon", points="256,40 472,256 256,472 40,256", fill=C["yellow"])
    picto(s, p_kangaroo, 256, 266, 1.25)


@draw("dead-end-sign")
def _(s):
    info(s, lambda s, c: (fl(s, "rect", WHITE, x=-26, y=-60, width=52, height=160), fl(s, "rect", RED, x=-90, y=-100, width=180, height=46)))


@draw("detour-sign")
def _(s):
    s.F("rect", x=50, y=110, width=412, height=292, rx=30, fill=C["orange"])
    picto(s, lambda s, c: (st(s, "M-120 60 H-40 C0 60 0 -40 40 -40 H90", c, 26), fl(s, "polygon", c, points="80,-80 140,-40 80,0")), 256, 256, 1.0)


D["keep-left-sign"] = lambda s: mandatory(s, lambda s, c: (st(s, "M70 -70 L-40 40", c, 30), fl(s, "polygon", c, points="-80,80 -70,-6 6,70")))
D["turn-left-only-sign"] = lambda s: mandatory(s, lambda s, c: bent_arrow(s, c, True))
D["cycle-lane-sign"] = lambda s: mandatory(s, p_bike, 1.3)
D["bus-stop-sign"] = lambda s: info(s, p_bus, 1.25)
D["fuel-station-sign"] = lambda s: info(s, p_pump, 1.35)


@draw("height-limit-sign")
def _(s):
    prohib(s, slash=False)
    fl(s, "polygon", BLACK, points="216,110 296,110 256,150"); fl(s, "polygon", BLACK, points="216,402 296,402 256,362")
    stroke_text(s, "4m", 256, 256, 110, BLACK, 22)


@draw("weight-limit-sign")
def _(s):
    prohib(s, slash=False); stroke_text(s, "10t", 256, 256, 120, BLACK, 22)


@draw("direction-sign")
def _(s):
    s.F("rect", x=40, y=100, width=432, height=312, rx=30, fill=C["darkgreen"])
    s.raw(f'<rect x="62" y="122" width="388" height="268" rx="18" fill="none" stroke="{WHITE}" stroke-width="8"/>')
    st(s, "M256 370 V170", WHITE, 26); fl(s, "polygon", WHITE, points="216,180 256,136 296,180")
    st(s, "M256 300 H140", WHITE, 22); fl(s, "polygon", WHITE, points="150,270 106,300 150,330")
    st(s, "M256 240 H372", WHITE, 22); fl(s, "polygon", WHITE, points="362,210 406,240 362,270")


# ---------------------------------------------------------------- safety signs (ISO 7010 style, keep)
YEL, GREEN = C["yellow"], C["darkgreen"]


def hz(s, fn, sc=1.0):
    s.F("path", d="M256 50 C272 50 282 58 290 72 L468 380 C482 406 468 430 438 430 H74 C44 430 30 406 44 380 L222 72 C230 58 240 50 256 50Z", fill=BLACK)
    s.F("path", outline=False, d="M256 110 L420 396 H92 Z", fill=YEL)
    picto(s, fn, 256, 306, sc)


def no(s, fn, sc=1.0):
    prohib(s, fn, sc=sc)


def must(s, fn, sc=1.0):
    mandatory(s, fn, sc)


def safe(s, fn, sc=1.0):
    info(s, fn, sc, GREEN)


def firesign(s, fn, sc=1.0):
    info(s, fn, sc, RED)


def person(s, c, arms=True):
    fl(s, "circle", c, cx=0, cy=-74, r=20)
    fl(s, "rect", c, x=-24, y=-48, width=48, height=74, rx=14)
    fl(s, "rect", c, x=-22, y=14, width=19, height=74, rx=8)
    fl(s, "rect", c, x=3, y=14, width=19, height=74, rx=8)
    if arms:
        fl(s, "rect", c, x=-40, y=-46, width=15, height=66, rx=7)
        fl(s, "rect", c, x=25, y=-46, width=15, height=66, rx=7)


def woman(s, c):
    fl(s, "circle", c, cx=0, cy=-74, r=20)
    fl(s, "path", c, d="M-20 -48 H20 L44 34 H-44 Z")
    fl(s, "rect", c, x=-18, y=30, width=15, height=58, rx=7)
    fl(s, "rect", c, x=3, y=30, width=15, height=58, rx=7)
    fl(s, "rect", c, x=-40, y=-44, width=14, height=56, rx=7, transform="rotate(14 -33 -16)")
    fl(s, "rect", c, x=26, y=-44, width=14, height=56, rx=7, transform="rotate(-14 33 -16)")


def runner(s, c):
    fl(s, "circle", c, cx=24, cy=-76, r=18)
    st(s, "M14 -50 L-8 14 M-40 -30 L-4 -46 L30 -16 L56 -24 M-8 14 L-48 34 L-70 78 M-8 14 L30 48 L18 90", c, 20)


def skull(s, c):
    fl(s, "path", c, d="M0 -84 C-50 -84 -64 -46 -60 -10 C-58 12 -44 20 -40 34 H40 C44 20 58 12 60 -10 C64 -46 50 -84 0 -84Z")
    fl(s, "rect", c, x=-30, y=30, width=60, height=26, rx=6)
    bg = YEL if c == BLACK else WHITE
    for x in (-24, 24):
        fl(s, "circle", bg, cx=x, cy=-16, r=15)
    fl(s, "polygon", bg, points="0,8 -9,22 9,22")


def flame(s, c):
    fl(s, "path", c, d="M0 88 C-52 88 -74 54 -74 18 C-74 -26 -34 -44 -30 -92 C0 -66 8 -40 4 -16 C24 -32 30 -54 26 -84 C64 -56 76 -14 76 18 C76 58 50 88 0 88Z")


def hand(s, c):
    fl(s, "path", c, d="M-46 90 C-60 60 -70 30 -70 0 C-70 -14 -50 -16 -46 0 L-40 20 V-60 C-40 -76 -18 -76 -18 -60 V-10 V-80 "
                       "C-18 -96 6 -96 6 -80 V-10 V-72 C6 -88 30 -88 30 -72 V-6 V-52 C30 -66 52 -66 52 -52 V30 C52 60 40 80 30 90 Z")


def dog(s, c):
    fl(s, "path", c, d="M-70 -10 C-70 -30 40 -30 50 -10 L78 -40 C88 -48 100 -40 96 -28 L70 0 C66 20 50 24 40 22 V80 H24 V30 H-40 V80 "
                       "H-56 V20 C-70 14 -74 4 -70 -10Z M-70 -10 L-96 -34")
    st(s, "M-70 -10 L-96 -36", c, 10)


hazards = {
    "warning-sign": lambda s, c: (st(s, "M0 -66 V30", c, 30), fl(s, "circle", c, cx=0, cy=72, r=18)),
    "danger-sign": skull,
    "high-voltage-sign": lambda s, c: fl(s, "polygon", c, points="16,-96 -50,10 -2,10 -26,96 50,-14 2,-14 30,-96"),
    "toxic-sign": lambda s, c: (st(s, "M-70 20 L70 90 M70 20 L-70 90", c, 18), picto(s, skull, 0, -20, 0.8, c)),
    "flammable-sign": flame,
    "explosive-sign": lambda s, c: (fl(s, "polygon", c, points=star_pts(0, 10, 86, 40, 9)),
                                    [fl(s, "circle", c, cx=x, cy=y, r=11) for x, y in ((-86, -60), (82, -66), (-90, 70), (90, 60))]),
    "corrosive-sign": lambda s, c: (fl(s, "rect", c, x=-74, y=-90, width=26, height=60, rx=6, transform="rotate(-30 -60 -60)"),
                                    fl(s, "rect", c, x=40, y=-90, width=26, height=60, rx=6, transform="rotate(30 52 -60)"),
                                    [fl(s, "circle", c, cx=x, cy=y, r=8) for x, y in ((-34, -6), (-26, 20), (28, -6), (20, 22))],
                                    fl(s, "rect", c, x=-90, y=50, width=70, height=34, rx=6),
                                    fl(s, "path", c, d="M10 84 C10 50 40 44 60 50 C80 56 90 70 90 84 Z")),
    "oxidiser-sign": lambda s, c: (picto(s, flame, 0, -26, 0.7, c),
                                   s.raw(f'<circle cx="0" cy="56" r="34" fill="none" stroke="{c}" stroke-width="14"/>')),
    "compressed-gas-sign": lambda s, c: (fl(s, "rect", c, x=-34, y=-62, width=68, height=150, rx=30),
                                         fl(s, "rect", c, x=-12, y=-90, width=24, height=30, rx=4)),
    "health-hazard-sign": lambda s, c: (person(s, c), fl(s, "polygon", YEL, points=star_pts(0, -12, 26, 10, 6))),
    "environmental-hazard-sign": lambda s, c: (st(s, "M-50 60 V-60 M-50 -20 L-80 -50 M-50 -40 L-20 -76 M-50 0 L-24 -20", c, 12),
                                               fl(s, "path", c, d="M10 60 C30 30 80 30 96 60 C80 90 30 90 10 60 Z M10 60 L-6 40 V80 Z"),
                                               st(s, "M-96 90 H96", c, 10)),
    "laser-hazard-sign": lambda s, c: (fl(s, "polygon", c, points=star_pts(-20, 0, 70, 22, 12)), st(s, "M-20 0 H96", c, 12)),
    "magnetic-field-sign": lambda s, c: (st(s, "M-50 -70 V10 C-50 70 50 70 50 10 V-70", c, 30),
                                         fl(s, "rect", WHITE, x=-65, y=-80, width=30, height=24), fl(s, "rect", WHITE, x=35, y=-80, width=30, height=24)),
    "wet-floor-sign": lambda s, c: (fl(s, "circle", c, cx=-30, cy=-70, r=18),
                                    st(s, "M-24 -46 L10 20 M-60 -50 L-20 -30 L30 -60 M10 20 L60 40 M10 20 L-40 60", c, 18),
                                    st(s, "M-90 86 H90", c, 10), [fl(s, "circle", c, cx=x, cy=76, r=7) for x in (-50, 0, 50)]),
    "falling-objects-sign": lambda s, c: (picto(s, person, 10, 30, 0.7, c), fl(s, "rect", c, x=-40, y=-96, width=50, height=40, rx=4,
                                                                                transform="rotate(20 -15 -76)")),
    "hot-surface-sign": lambda s, c: (st(s, "M-60 -70 C-40 -50 -80 -30 -60 -10 M0 -70 C20 -50 -20 -30 0 -10 M60 -70 C80 -50 40 -30 60 -10", c, 12),
                                      fl(s, "rect", c, x=-90, y=20, width=180, height=30, rx=6), picto(s, hand, 30, 64, 0.35, c)),
    "trip-hazard-sign": lambda s, c: (picto(s, runner, 0, -10, 0.8, c), fl(s, "rect", c, x=-90, y=66, width=60, height=26)),
    "deep-water-sign": lambda s, c: (fl(s, "circle", c, cx=0, cy=-30, r=22), st(s, "M-30 -60 L-10 -30 M30 -60 L10 -30", c, 12),
                                     st(s, "M-90 10 C-60 -10 -30 30 0 10 C30 -10 60 30 90 10 M-90 50 C-60 30 -30 70 0 50 C30 30 60 70 90 50", c, 12)),
    "tsunami-hazard-sign": lambda s, c: (fl(s, "path", c, d="M-96 86 C-96 0 -40 -86 40 -80 C80 -78 96 -50 80 -30 C60 -50 20 -40 10 -10 C0 30 40 60 96 60 V86 Z"),
                                         fl(s, "rect", c, x=50, y=10, width=40, height=34)),
    "landslide-warning-sign": lambda s, c: (fl(s, "polygon", c, points="-96,86 96,86 -96,-60"),
                                            [fl(s, "circle", c, cx=x, cy=y, r=r) for x, y, r in ((10, -10, 16), (40, 30, 12), (64, 60, 10))]),
}
for _id, fn in hazards.items():
    D[_id] = (lambda f: lambda s: hz(s, f))(fn)


def trefoil(s, c, holes=False):
    for a in (-90, 30, 150):
        x1, y1 = arc_pt(0, 0, 90, a - 30); x2, y2 = arc_pt(0, 0, 90, a + 30)
        x3, y3 = arc_pt(0, 0, 26, a + 30); x4, y4 = arc_pt(0, 0, 26, a - 30)
        fl(s, "path", c, d=f"M{x4:.0f} {y4:.0f} L{x1:.0f} {y1:.0f} A90 90 0 0 1 {x2:.0f} {y2:.0f} L{x3:.0f} {y3:.0f} A26 26 0 0 0 {x4:.0f} {y4:.0f}Z")
    fl(s, "circle", c, cx=0, cy=0, r=16)


D["radiation-sign"] = lambda s: hz(s, trefoil)


@draw("biohazard-sign")
def _(s):
    def bio(s, c):
        for a in (-90, 30, 150):
            x, y = arc_pt(0, 0, 40, a); xi, yi = arc_pt(0, 0, 54, a)
            s.raw(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="42" fill="none" stroke="{c}" stroke-width="16"/>')
            fl(s, "circle", YEL, cx=f"{xi:.0f}", cy=f"{yi:.0f}", r=22)
        s.raw(f'<circle cx="0" cy="0" r="50" fill="none" stroke="{c}" stroke-width="10"/>')
    hz(s, bio)


# prohibition signs
def cigarette(s, c):
    fl(s, "rect", c, x=-90, y=10, width=150, height=28, rx=4)
    fl(s, "rect", c, x=66, y=10, width=22, height=28, rx=4)
    st(s, "M74 0 C64 -24 90 -40 80 -70", c, 10)


def phone(s, c):
    fl(s, "rect", c, x=-40, y=-80, width=80, height=160, rx=16)
    fl(s, "rect", WHITE, x=-28, y=-60, width=56, height=104, rx=4)


def cam(s, c):
    fl(s, "path", c, d="M-80 -30 H-40 L-24 -54 H24 L40 -30 H80 V60 H-80 Z")
    fl(s, "circle", WHITE, cx=0, cy=14, r=32)
    fl(s, "circle", c, cx=0, cy=14, r=18)


def cup(s, c):
    fl(s, "path", c, d="M-50 -50 H40 L30 70 H-40 Z")
    st(s, "M40 -20 C76 -20 76 30 34 30", c, 14)


def cutlery(s, c):
    st(s, "M-34 -80 V80 M-54 -80 V-30 C-54 -10 -14 -10 -14 -30 V-80", c, 12)
    fl(s, "path", c, d="M34 80 V-80 C70 -60 64 0 40 10 Z")


def swimmer(s, c):
    fl(s, "circle", c, cx=-40, cy=-30, r=18)
    st(s, "M-20 -10 L40 -40 L70 -20 M-60 10 C-30 -6 0 26 30 10 C50 0 70 20 90 10", c, 14)
    st(s, "M-90 50 C-60 34 -30 66 0 50 C30 34 60 66 90 50", c, 12)


def diver(s, c):
    fl(s, "circle", c, cx=30, cy=-30, r=16)
    st(s, "M-60 -86 L20 -8 M10 -30 L60 -70 M-20 -30 L-50 -60", c, 16)
    st(s, "M-90 60 C-60 44 -30 76 0 60 C30 44 60 76 90 60", c, 12)


def fishing(s, c):
    st(s, "M-80 80 L40 -80 M40 -80 V20", c, 10)
    fl(s, "path", c, d="M10 40 C30 20 70 20 84 40 C70 60 30 60 10 40Z M10 40 L-6 26 V54 Z")


def shoe(s, c):
    fl(s, "path", c, d="M-90 40 V-20 C-60 -20 -40 -30 -30 -50 L10 -40 C10 -10 60 0 90 10 V40 Z")
    fl(s, "rect", c, x=-90, y=44, width=180, height=14, rx=4)


def match(s, c):
    st(s, "M-40 80 L20 -10", c, 14)
    picto(s, flame, 30, -50, 0.5, c)


def tent(s, c):
    fl(s, "polygon", c, points="-90,70 0,-80 90,70")
    fl(s, "polygon", WHITE, points="-20,70 0,10 20,70")


def bag(s, c):
    fl(s, "path", c, d="M-56 -30 H56 L66 80 H-66 Z")
    st(s, "M-30 -30 V-56 C-30 -80 30 -80 30 -56 V-30", c, 12)


def bubble(s, c):
    fl(s, "path", c, d="M-80 -60 H80 C90 -60 96 -54 96 -44 V20 C96 30 90 36 80 36 H-20 L-60 76 V36 H-80 C-90 36 -96 30 -96 20 V-44 C-96 -54 -90 -60 -80 -60Z")


def litter(s, c):
    picto(s, person, -30, 0, 0.8, c)
    fl(s, "rect", c, x=40, y=40, width=24, height=40, rx=5, transform="rotate(30 52 60)")


nos = {
    "no-smoking-sign": cigarette, "no-phones-sign": phone, "no-photography-sign": cam, "no-food-sign": cutlery,
    "no-drinks-sign": cup, "no-pets-sign": dog, "no-littering-sign": litter, "no-swimming-sign": swimmer,
    "no-diving-sign": diver, "no-fishing-sign": fishing, "no-shoes-sign": shoe, "no-open-flames-sign": match,
    "no-touching-sign": hand, "no-running-sign": runner, "no-cycling-sign": p_bike, "no-talking-sign": bubble,
    "no-plastic-sign": bag, "no-camping-sign": tent, "no-access-sign": person, "no-entry-for-pedestrians-sign": p_walker,
}
for _id, fn in nos.items():
    D[_id] = (lambda f: lambda s: no(s, f, 0.92))(fn)
D["prohibited-symbol"] = lambda s: prohib(s)


# public signs
def wheelchair(s, c):
    fl(s, "circle", c, cx=-10, cy=-80, r=18)
    st(s, "M-14 -56 V0 H40 L60 60 M-14 -30 H30", c, 18)
    s.raw(f'<path d="M-40 -10 A56 56 0 1 0 30 50" fill="none" stroke="{c}" stroke-width="14"/>')


def plane(s, c):
    fl(s, "path", c, d="M0 -96 C10 -96 14 -80 14 -66 V-20 L90 20 V40 L14 20 V60 L36 76 V90 L0 80 L-36 90 V76 L-14 60 V20 L-90 40 V20 L-14 -20 V-66 C-14 -80 -10 -96 0 -96Z")


def recycle(s, c):
    for a in (-90, 30, 150):
        x0, y0 = arc_pt(0, 0, 70, a); x1, y1 = arc_pt(0, 0, 70, a + 80)
        st(s, f"M{x0:.0f} {y0:.0f} A70 70 0 0 1 {x1:.0f} {y1:.0f}", c, 22)
        tip = arc_pt(0, 0, 70, a + 104); b1 = arc_pt(0, 0, 40, a + 78); b2 = arc_pt(0, 0, 100, a + 78)
        fl(s, "polygon", c, points=f"{tip[0]:.0f},{tip[1]:.0f} {b1[0]:.0f},{b1[1]:.0f} {b2[0]:.0f},{b2[1]:.0f}")


def tap(s, c):
    fl(s, "path", c, d="M-80 -60 H20 C50 -60 60 -40 60 -10 V10 H30 V-10 C30 -24 24 -30 14 -30 H-80 Z")
    fl(s, "rect", c, x=-40, y=-86, width=24, height=30, rx=4)
    fl(s, "path", c, d="M45 30 C45 30 20 60 20 76 C20 92 70 92 70 76 C70 60 45 30 45 30Z")


def exit_run(s, c):
    picto(s, runner, -26, 0, 0.8, c)
    fl(s, "rect", c, x=40, y=-90, width=52, height=180, rx=4)
    fl(s, "rect", GREEN, x=52, y=-78, width=28, height=156)


def extinguisher(s, c):
    fl(s, "rect", c, x=-34, y=-50, width=68, height=140, rx=26)
    fl(s, "rect", c, x=-12, y=-80, width=24, height=34)
    st(s, "M12 -70 H50 L70 -40", c, 12)


def lift(s, c):
    s.raw(f'<rect x="-70" y="-90" width="140" height="180" rx="10" fill="none" stroke="{c}" stroke-width="12"/>')
    fl(s, "polygon", c, points="-30,-20 0,-60 30,-20"); fl(s, "polygon", c, points="-30,20 0,60 30,20")


def stairs(s, c):
    fl(s, "path", c, d="M-90 90 V50 H-46 V10 H-2 V-30 H42 V-70 H90 V90 Z")


def escalator(s, c):
    st(s, "M-90 70 H-40 L40 -40 H90", c, 26)
    picto(s, person, 0, -30, 0.5, c)


def mosque_room(s, c):
    fl(s, "path", c, d="M-76 90 V10 C-76 -40 -36 -54 0 -70 C36 -54 76 -40 76 10 V90 Z")
    fl(s, "rect", c, x=-4, y=-96, width=8, height=30)
    fl(s, "circle", c, cx=0, cy=-104, r=14)
    fl(s, "circle", BLUE, cx=6, cy=-108, r=11)
    fl(s, "path", BLUE, d="M-26 90 V40 C-26 14 26 14 26 40 V90 Z")


def wudu(s, c):
    picto(s, tap, 0, -30, 0.8, c)
    for x in (-20, 20, 60):
        fl(s, "path", c, d=f"M{x} 50 C{x} 50 {x - 14} 70 {x - 14} 80 C{x - 14} 96 {x + 14} 96 {x + 14} 80 C{x + 14} 70 {x} 50 {x} 50Z")


def lostfound(s, c):
    picto(s, bag, -20, 20, 0.8, c)
    st(s, "M30 -70 C30 -96 80 -96 80 -70 C80 -50 56 -46 56 -30", c, 14)
    fl(s, "circle", c, cx=56, cy=-10, r=8)


def taxi(s, c):
    picto(s, p_car, 0, 20, 1.0, c)
    fl(s, "rect", c, x=-24, y=-50, width=48, height=20, rx=4)


def head_icon(s, c, extra=None):
    fl(s, "circle", c, cx=0, cy=-10, r=56)
    fl(s, "path", c, d="M-70 96 C-70 50 -40 40 0 40 C40 40 70 50 70 96Z")
    if extra:
        extra(s)


def gear_helmet(s):
    fl(s, "path", YEL, d="M-70 -20 C-70 -70 70 -70 70 -20 H86 V-6 H-86 V-20Z")


def gear_mask(s):
    fl(s, "path", C["sky"], d="M-54 -4 H54 V26 C54 54 -54 54 -54 26Z")
    st(s, "M-50 0 L-60 -10 M50 0 L60 -10", C["sky"], 6)


def gear_goggles(s):
    fl(s, "rect", BLACK, x=-60, y=-34, width=120, height=38, rx=17)
    fl(s, "rect", C["sky"], x=-46, y=-26, width=38, height=22, rx=9); fl(s, "rect", C["sky"], x=8, y=-26, width=38, height=22, rx=9)


def glove(s, c):
    fl(s, "path", c, d="M-40 90 V60 C-60 40 -70 10 -70 -10 C-70 -24 -50 -24 -46 -10 L-40 6 V-60 C-40 -76 -18 -76 -18 -60 V-80 "
                       "C-18 -96 6 -96 6 -80 V-72 C6 -88 30 -88 30 -72 V-52 C30 -66 52 -66 52 -52 V30 C52 50 40 60 40 60 V90 Z")


def wash(s, c):
    picto(s, hand, -10, 30, 0.6, c)
    for x, y in ((-50, -70), (0, -86), (50, -70)):
        fl(s, "path", c, d=f"M{x} {y} C{x} {y} {x - 14} {y + 20} {x - 14} {y + 30} C{x - 14} {y + 46} {x + 14} {y + 46} {x + 14} {y + 30} C{x + 14} {y + 20} {x} {y} {x} {y}Z")


def seatbelt(s, c):
    person(s, c, arms=False)
    st(s, "M-30 -50 L30 20", BLUE, 12)


def distance(s, c):
    picto(s, person, -60, 0, 0.7, c); picto(s, person, 60, 0, 0.7, c)
    st(s, "M-26 -80 H26", c, 8)
    fl(s, "polygon", c, points="-34,-80 -20,-90 -20,-70"); fl(s, "polygon", c, points="34,-80 20,-90 20,-70")


def bin_use(s, c):
    picto(s, person, -40, 0, 0.8, c)
    fl(s, "path", c, d="M30 10 H90 L82 90 H38 Z")
    fl(s, "rect", c, x=26, y=-4, width=68, height=10, rx=3)


def cctv(s, c):
    fl(s, "rect", c, x=-60, y=-60, width=110, height=50, rx=10, transform="rotate(16 -5 -35)")
    st(s, "M30 -10 L50 40 H80 M80 0 V80", c, 12)


def charger(s, c):
    fl(s, "rect", c, x=-60, y=-80, width=90, height=170, rx=12)
    fl(s, "polygon", BLUE, points="-10,-60 -40,0 -16,0 -26,50 10,-14 -14,-14")
    st(s, "M30 -20 H60 V60 C60 80 80 80 80 60", c, 10)


def toilets(s, c):
    picto(s, person, -46, 0, 0.9, c); picto(s, woman, 46, 0, 0.9, c)
    fl(s, "rect", c, x=-3, y=-90, width=6, height=180)


def baby(s, c):
    fl(s, "rect", c, x=-90, y=30, width=180, height=16, rx=4)
    fl(s, "circle", c, cx=-50, cy=4, r=20)
    fl(s, "rect", c, x=-30, y=-8, width=90, height=34, rx=14)
    picto(s, person, 40, -50, 0.45, c)


def assembly(s, c):
    for x, y in ((-50, -50), (50, -50), (-50, 50), (50, 50)):
        picto(s, person, x, y, 0.38, c)
    for a in (45, 135, 225, 315):
        x, y = arc_pt(0, 0, 30, a)
        fl(s, "circle", c, cx=f"{x:.0f}", cy=f"{y:.0f}", r=6)


publics = {
    "toilet-sign": (toilets, "info", 1.0), "men-toilet-sign": (person, "info", 1.0), "women-toilet-sign": (woman, "info", 1.0),
    "accessibility-symbol": (wheelchair, "info", 1.1), "baby-changing-sign": (baby, "info", 1.0),
    "emergency-exit-sign": (exit_run, "safe", 1.1), "fire-extinguisher-sign": (extinguisher, "fire", 1.2),
    "first-aid-sign": (lambda s, c: (fl(s, "rect", c, x=-26, y=-90, width=52, height=180), fl(s, "rect", c, x=-90, y=-26, width=180, height=52)), "safe", 1.0),
    "assembly-point-sign": (assembly, "safe", 1.3),
    "information-desk-sign": (lambda s, c: (fl(s, "circle", c, cx=0, cy=-70, r=22), fl(s, "rect", c, x=-20, y=-30, width=40, height=120, rx=6)), "info", 1.0),
    "lift-sign": (lift, "info", 1.0), "stairs-sign": (stairs, "info", 1.1), "escalator-sign": (escalator, "info", 1.1),
    "drinking-water-sign": (tap, "info", 1.2), "prayer-room-sign": (mosque_room, "info", 1.1), "wudu-area-sign": (wudu, "info", 1.1),
    "lost-and-found-sign": (lostfound, "info", 1.1), "taxi-stand-sign": (taxi, "info", 1.2), "airport-sign": (plane, "info", 1.2),
    "pharmacy-sign": (lambda s, c: (fl(s, "rect", c, x=-26, y=-80, width=52, height=160, rx=6), fl(s, "rect", c, x=-80, y=-26, width=160, height=52, rx=6)), "safe", 1.1),
    "recycling-point-sign": (recycle, "safe", 1.2), "charging-point-sign": (charger, "info", 1.1),
    "wear-helmet-sign": (lambda s, c: head_icon(s, c, gear_helmet), "must", 1.2),
    "wear-mask-sign": (lambda s, c: head_icon(s, c, gear_mask), "must", 1.2),
    "wash-hands-sign": (wash, "must", 1.2), "wear-seatbelt-sign": (seatbelt, "must", 1.2),
    "wear-safety-goggles-sign": (lambda s, c: head_icon(s, c, gear_goggles), "must", 1.2),
    "wear-gloves-sign": (glove, "must", 1.2), "keep-distance-sign": (distance, "must", 1.3),
    "use-the-bin-sign": (bin_use, "must", 1.2), "cctv-sign": (cctv, "info", 1.4),
}
FRAMES = {"info": info, "safe": safe, "fire": firesign, "must": must}
for _id, (fn, frame, sc) in publics.items():
    D[_id] = (lambda f, fr, k: lambda s: FRAMES[fr](s, f, k))(fn, frame, sc)


@draw("hospital-sign")
def _(s):
    info(s, lambda s, c: None); stroke_text(s, "H", 256, 256, 220, WHITE, 44)


if __name__ == "__main__":
    run("symbols-signs", D, sys.argv[1:] or None)
