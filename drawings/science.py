"""science drawings by hand (the 118 element tiles are in science_elements.py).
Run: python drawings/science.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE  # noqa: E402
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, bulb, check_badge, magnifier, qmark  # noqa: E402
from _parts import place as P  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run, star_pts  # noqa: E402

D = {}
RED, DRED, GREEN, YEL, ORANGE, PINK, SKY, GREY, DGREY = C["red"], C["darkred"], C["green"], C["yellow"], C["orange"], C["pink"], C["sky"], C["grey"], C["darkgrey"]
BLUE, PURPLE, BROWN, DBROWN, TAN, GOLD = C["blue"], C["purple"], C["brown"], C["darkbrown"], C["tan"], C["gold"]
GLASS, GLASS_D = "#E3F3FC", "#BFE0F2"


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def marks(s, x, y0, y1, n, w=22, color=DGREY, sw=5):
    for i in range(n):
        y = y0 + (y1 - y0) * i / max(n - 1, 1)
        s.M(f"M{x} {y:.0f} h{w}", color, sw)


def bubbles(s, pts, color=WHITE):
    for x, y, r in pts:
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=color, fill_opacity="0.8")


def ring(s, cx, cy, r, color, w):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w + 20}" data-outline="under"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>')


# ================================================================ lab-equipment
@reg("beaker")
def _(s):
    s.F("path", d="M120 70 H392 L376 440 C374 458 360 466 344 466 H168 C152 466 138 458 136 440Z", fill=GLASS)
    s.F("path", outline=False, d="M130 250 H382 L376 440 C374 454 360 458 344 458 H168 C152 458 138 454 136 440Z", fill=A1L)
    s.F("rect", outline=False, x=146, y=90, width=14, height=320, rx=7, fill=WHITE, fill_opacity="0.7")
    marks(s, 330, 150, 400, 6, 36)


@reg("test-tube")
def _(s):
    s.open(transform="rotate(25 256 256)")
    s.F("path", d="M206 50 H306 V380 C306 440 206 440 206 380Z", fill=GLASS)
    s.F("path", outline=False, d="M212 230 H300 V380 C300 430 212 430 212 380Z", fill=A2L)
    s.F("rect", outline=False, x=220, y=70, width=12, height=140, rx=6, fill=WHITE, fill_opacity="0.7")
    s.F("rect", x=196, y=38, width=120, height=26, rx=12, fill=GLASS_D)
    s.close()


def tube(s, x, top, color, h=300, w=64):
    s.F("path", d=f"M{x - w / 2} {top} H{x + w / 2} V{top + h - w / 2} C{x + w / 2} {top + h + w / 2} {x - w / 2} {top + h + w / 2} {x - w / 2} {top + h - w / 2}Z", fill=GLASS)
    if color:
        s.F("path", outline=False, d=f"M{x - w / 2 + 5} {top + 120} H{x + w / 2 - 5} V{top + h - w / 2} C{x + w / 2 - 5} {top + h + w / 2 - 8} {x - w / 2 + 5} {top + h + w / 2 - 8} {x - w / 2 + 5} {top + h - w / 2}Z", fill=color)


@reg("test-tube-rack")
def _(s):
    s.F("rect", x=84, y=230, width=26, height=210, rx=8, fill=BROWN)
    s.F("rect", x=402, y=230, width=26, height=210, rx=8, fill=BROWN)
    for x, c in ((150, A1L), (256, A2L), (362, "#9BE0A8")):
        tube(s, x, 90, c, 260)
    s.F("rect", x=70, y=230, width=372, height=34, rx=10, fill=TAN)
    s.F("rect", x=70, y=330, width=372, height=34, rx=10, fill=TAN)
    s.F("rect", x=70, y=420, width=372, height=34, rx=10, fill=BROWN)


@reg("conical-flask")
def _(s):
    s.F("path", d="M210 60 H302 V190 L420 410 C432 440 420 466 388 466 H124 C92 466 80 440 92 410 L210 190Z", fill=GLASS)
    s.F("path", outline=False, d="M170 300 H342 L412 420 C420 444 410 458 386 458 H126 C102 458 92 444 100 420Z", fill=A2L)
    s.F("rect", outline=False, x=224, y=80, width=12, height=100, rx=6, fill=WHITE, fill_opacity="0.7")
    s.F("rect", x=198, y=46, width=116, height=26, rx=12, fill=GLASS_D)
    bubbles(s, [(240, 380, 12), (290, 350, 8), (320, 410, 10)])


@reg("round-bottom-flask")
def _(s):
    s.F("path", d="M214 60 H298 V170 C400 200 440 290 420 370 C400 450 330 466 256 466 C182 466 112 450 92 370 C72 290 112 200 214 170Z", fill=GLASS)
    s.F("path", outline=False, d="M104 330 C170 310 340 350 410 320 C416 340 414 360 408 380 C390 440 330 458 256 458 C182 458 122 440 104 380Z", fill=PINK)
    s.F("rect", outline=False, x=226, y=76, width=12, height=80, rx=6, fill=WHITE, fill_opacity="0.7")
    s.F("rect", x=202, y=46, width=108, height=26, rx=12, fill=GLASS_D)


@reg("volumetric-flask")
def _(s):
    s.F("path", d="M226 40 H286 V240 C400 270 440 330 420 396 C400 462 330 470 256 470 C182 470 112 462 92 396 C72 330 112 270 226 240Z", fill=GLASS)
    s.F("path", outline=False, d="M100 360 H412 C416 376 414 392 410 404 C392 456 330 460 256 460 C182 460 120 456 102 404Z", fill=A1L)
    s.M("M226 130 H286", A2, 8)
    s.F("rect", x=214, y=26, width=84, height=24, rx=10, fill=A2)


@reg("measuring-cylinder")
def _(s):
    s.F("path", d="M170 50 H342 V80 H320 V430 H400 V470 H112 V430 H192 V80 H170Z", fill=GLASS)
    s.F("path", outline=False, d="M196 230 H316 V430 H196Z", fill=A1L)
    s.F("path", outline=False, d="M196 232 C230 220 286 244 316 230 V240 H196Z", fill=A1)
    marks(s, 270, 110, 400, 9, 46)


@reg("pipette")
def _(s):
    s.open(transform="rotate(30 256 256)")
    s.F("path", d="M226 90 C226 30 286 30 286 90 V120 H226Z", fill=RED)
    s.F("path", d="M232 120 H280 V360 L256 460 L232 360Z", fill=GLASS)
    s.F("path", outline=False, d="M238 290 H274 V360 L256 440 L238 360Z", fill=A2L)
    marks(s, 250, 160, 260, 4, 22)
    s.close()
    s.F("circle", cx=140, cy=450, r=14, fill=A2L)


@reg("burette")
def _(s):
    s.T("M256 50 V380", GLASS, 44)
    s.F("rect", outline=False, x=240, y=160, width=32, height=220, fill=A1L)
    marks(s, 288, 70, 360, 9, 32)
    s.F("rect", x=226, y=380, width=60, height=36, rx=8, fill=GREY)
    s.F("rect", x=170, y=392, width=172, height=16, rx=8, fill=RED)
    s.F("path", d="M240 416 H272 L256 462Z", fill=GLASS)
    s.F("path", outline=False, d="M256 476 c-8 12 -8 22 0 24 c8 -2 8 -12 0 -24z", fill=A1L)


@reg("petri-dish")
def _(s):
    s.F("ellipse", cx=256, cy=320, rx=200, ry=70, fill=GLASS)
    s.F("ellipse", outline=False, cx=256, cy=316, rx=176, ry=50, fill="#F2D488")
    s.F("path", d="M56 320 V260 C56 200 456 200 456 260 V320 C456 380 56 380 56 320Z", fill=GLASS, fill_opacity="0.55")
    s.F("ellipse", cx=256, cy=260, rx=200, ry=56, fill=GLASS, fill_opacity="0.7")
    for x, y, r in ((200, 258, 16), (270, 250, 22), (330, 266, 14), (240, 280, 10)):
        s.F("circle", outline=False, cx=x, cy=y, r=r, fill=A1)


@reg("microscope")
def _(s):
    s.F("path", d="M110 450 H390 V400 H330 C400 380 420 300 390 220 C370 170 320 150 290 160 L300 200 C330 200 350 250 340 300 C330 360 290 380 250 380 H110Z", fill=A1)
    s.open(transform="rotate(-20 220 180)")
    s.F("rect", x=170, y=40, width=100, height=160, rx=14, fill=DGREY)
    s.F("rect", x=190, y=200, width=60, height=70, rx=8, fill=GREY)
    s.F("rect", x=176, y=20, width=88, height=34, rx=10, fill=GREY)
    s.close()
    s.F("rect", x=140, y=320, width=170, height=30, rx=10, fill=A1L)
    s.F("circle", cx=370, cy=300, r=26, fill=A2)


@reg("magnifying-glass")
def _(s):
    s.T("M330 330 L440 440", DBROWN, 40)
    s.F("circle", cx=230, cy=230, r=150, fill="#CFEBFB")
    ring(s, 230, 230, 150, GOLD, 26)
    s.M("M130 200 C150 140 210 110 262 118", WHITE, 16)


@reg("bunsen-burner")
def _(s):
    s.F("path", d="M256 40 C300 100 330 140 320 190 C312 220 290 230 256 230 C222 230 200 220 192 190 C182 140 212 100 256 40Z", fill=A2)
    s.F("path", outline=False, d="M256 110 C280 150 290 170 280 195 C272 212 240 212 232 195 C222 170 236 150 256 110Z", fill=A2L)
    s.F("rect", x=226, y=220, width=60, height=180, rx=10, fill=GREY)
    s.F("rect", x=216, y=290, width=80, height=24, rx=8, fill=DGREY)
    s.F("path", d="M120 460 C120 420 160 400 256 400 C352 400 392 420 392 460Z", fill=DGREY)


@reg("tripod-stand")
def _(s):
    s.T("M256 150 L120 440 M256 150 L392 440 M256 150 L256 330", DGREY, 22)
    s.T("M170 300 H342", DGREY, 14)
    s.F("ellipse", cx=256, cy=130, rx=140, ry=34, fill=GREY)
    s.F("ellipse", outline=False, cx=256, cy=130, rx=96, ry=16, fill=DGREY)


@reg("wire-gauze")
def _(s):
    s.F("path", d="M60 280 L170 190 H450 L340 280Z", fill=GREY)
    s.F("path", d="M60 280 H340 V312 H60Z", fill=DGREY)
    s.F("path", outline=False, d="M236 240 C236 214 330 214 330 240 C330 262 236 262 236 240Z", fill=A2L)
    for i in range(1, 6):
        s.M(f"M{60 + i * 56} 280 L{170 + i * 56} 190", DGREY, 5)
    for i in range(1, 3):
        s.M(f"M{60 + i * 33} {280 - i * 30} H{340 + i * 37}", DGREY, 5)


@reg("spirit-lamp")
def _(s):
    s.F("path", d="M256 50 C290 90 300 120 284 150 C276 164 262 170 256 170 C250 170 236 164 228 150 C212 120 222 90 256 50Z", fill=A2)
    s.F("rect", x=240, y=166, width=32, height=40, rx=6, fill=GREY)
    s.F("path", d="M210 200 H302 L350 300 C400 340 400 430 310 450 H202 C112 430 112 340 162 300Z", fill=GLASS)
    s.F("path", outline=False, d="M130 360 C180 340 340 380 382 350 C390 400 360 440 306 446 H206 C152 440 124 410 130 360Z", fill=A1L)
    s.F("rect", outline=False, x=170, y=310, width=12, height=40, rx=6, fill=WHITE, fill_opacity="0.7")


@reg("retort-stand")
def _(s):
    s.F("rect", x=60, y=420, width=300, height=36, rx=12, fill=DGREY)
    s.F("rect", x=112, y=60, width=30, height=370, rx=8, fill=GREY)
    s.T("M142 130 H300", DGREY, 16)
    s.T("M142 260 H290", DGREY, 16)
    ring(s, 340, 260, 48, DGREY, 16)
    s.F("rect", x=124, y=242, width=36, height=36, rx=8, fill=RED)
    s.F("rect", x=124, y=112, width=36, height=36, rx=8, fill=RED)


@reg("funnel")
def _(s):
    s.F("path", d="M80 90 H432 L300 270 V420 H212 V270Z", fill=GLASS)
    s.F("path", outline=False, d="M130 140 H382 L290 262 H222Z", fill=A1L)
    s.F("rect", outline=False, x=110, y=106, width=14, height=36, rx=7, fill=WHITE, fill_opacity="0.7")
    s.F("path", d="M212 420 H300 L262 468 H250Z", fill=GLASS)


@reg("filter-paper")
def _(s):
    s.F("path", d="M70 160 C70 130 440 130 440 160 L270 440 C260 456 252 456 242 440Z", fill="#F7F1E4")
    s.F("path", outline=False, d="M256 150 L256 440 L242 440 L110 200Z", fill="#E7DEC8")
    s.M("M120 175 C200 200 310 200 390 175", MID, 6)


@reg("mortar-and-pestle")
def _(s):
    s.T("M170 90 L290 230", GREY, 40)
    s.F("circle", cx=160, cy=82, r=34, fill=GREY)
    s.F("path", d="M70 240 H442 C442 380 360 440 256 440 C152 440 70 380 70 240Z", fill=DGREY)
    s.F("path", outline=False, d="M92 252 H230 C210 330 170 390 130 398 C104 360 92 300 92 252Z", fill=GREY, fill_opacity="0.45")
    s.F("rect", x=190, y=440, width=132, height=34, rx=12, fill=DGREY)


@reg("watch-glass")
def _(s):
    s.F("path", d="M60 220 H452 C452 330 360 380 256 380 C152 380 60 330 60 220Z", fill=GLASS)
    s.F("path", outline=False, d="M130 240 H390 C380 290 330 330 256 330 C182 330 140 290 130 240Z", fill=A1L)
    s.F("ellipse", cx=256, cy=220, rx=196, ry=28, fill=GLASS)
    s.F("ellipse", outline=False, cx=256, cy=222, rx=120, ry=12, fill=WHITE, fill_opacity="0.6")
    s.F("rect", x=190, y=392, width=132, height=26, rx=10, fill=DGREY)


@reg("crucible")
def _(s):
    s.F("path", d="M110 170 H402 L352 400 C348 430 320 440 290 440 H222 C192 440 164 430 160 400Z", fill=C["cream"])
    s.F("path", outline=False, d="M130 180 H290 L236 428 H222 C192 428 168 420 164 396Z", fill="#EAD2A8", fill_opacity="0.7")
    s.F("ellipse", cx=256, cy=170, rx=146, ry=32, fill="#8A7C6A")
    s.F("ellipse", outline=False, cx=256, cy=172, rx=110, ry=18, fill="#4A3F34")
    s.F("path", d="M196 130 C190 90 250 90 256 50 C272 90 330 90 316 130 C300 150 220 150 196 130Z", fill=A2)


@reg("tongs")
def _(s):
    s.F("path", d="M170 70 H342 L322 140 H190Z", fill=C["cream"])
    s.F("ellipse", outline=False, cx=256, cy=76, rx=70, ry=10, fill="#4A3F34")
    s.T("M200 150 L226 230 L120 460 M312 150 L286 230 L392 460", DGREY, 22)
    s.T("M226 230 L286 330 M286 230 L226 330", DGREY, 22)
    s.F("circle", cx=256, cy=280, r=20, fill=GREY)
    s.F("rect", outline=False, x=96, y=420, width=48, height=20, rx=8, fill=RED, transform="rotate(-62 120 430)")
    s.F("rect", outline=False, x=370, y=420, width=48, height=20, rx=8, fill=RED, transform="rotate(62 392 430)")


@reg("test-tube-holder")
def _(s):
    s.T("M80 440 L250 270", DGREY, 22)
    s.T("M110 460 L270 300", DGREY, 22)
    s.T("M250 270 C240 190 300 160 340 180 C380 200 380 270 340 290", DGREY, 22)
    s.F("rect", x=318, y=60, width=60, height=120, rx=14, fill=GLASS)


@reg("lab-thermometer")
def _(s):
    s.F("rect", x=226, y=40, width=60, height=360, rx=30, fill=GLASS)
    s.F("circle", cx=256, cy=420, r=54, fill=RED)
    s.F("rect", outline=False, x=244, y=140, width=24, height=270, rx=12, fill=RED)
    marks(s, 296, 80, 340, 12, 26)
    s.F("circle", outline=False, cx=240, cy=406, r=14, fill=WHITE, fill_opacity="0.7")


@reg("spatula")
def _(s):
    s.T("M110 430 L300 250", DGREY, 22)
    s.F("path", d="M290 250 L350 190 C390 150 440 150 450 180 C456 220 400 250 340 300Z", fill=GREY)
    s.F("rect", x=70, y=380, width=80, height=34, rx=12, fill=A1, transform="rotate(-44 110 397)")


@reg("wash-bottle")
def _(s):
    s.F("path", d="M190 160 H322 C350 180 380 230 380 290 V430 C380 456 360 470 336 470 H176 C152 470 132 456 132 430 V290 C132 230 162 180 190 160Z", fill="#F3F6FA")
    s.F("path", outline=False, d="M150 290 H362 V430 C362 450 344 456 330 456 H182 C168 456 150 450 150 430Z", fill=A1L)
    s.F("rect", x=228, y=110, width=56, height=60, rx=10, fill=A1)
    s.T("M256 120 C256 70 300 50 380 60 L420 90", A1, 18)
    s.F("rect", outline=False, x=150, y=230, width=14, height=40, rx=7, fill=WHITE, fill_opacity="0.8")


@reg("safety-goggles")
def _(s):
    s.T("M70 250 C40 250 40 300 70 300 M442 250 C472 250 472 300 442 300", DGREY, 22)
    s.F("path", d="M70 200 C70 170 200 160 256 190 C312 160 442 170 442 200 V300 C442 350 350 360 320 330 C290 300 270 300 256 310 C242 300 222 300 192 330 C162 360 70 350 70 300Z", fill=A1)
    s.F("path", outline=False, d="M100 215 C130 195 190 190 226 205 V300 C226 330 170 335 130 320 C104 310 100 290 100 270Z", fill="#CFEBFB")
    s.F("path", outline=False, d="M412 215 C382 195 322 190 286 205 V300 C286 330 342 335 382 320 C408 310 412 290 412 270Z", fill="#CFEBFB")


@reg("lab-coat")
def _(s):
    s.F("path", d="M190 60 L110 90 L60 300 L130 320 L150 230 V460 H362 V230 L382 320 L452 300 L402 90 L322 60 L256 220Z", fill=WHITE)
    s.F("path", outline=False, d="M190 60 L256 220 L322 60 L296 54 L256 100 L216 54Z", fill=A1L)
    s.F("rect", x=300, y=300, width=44, height=56, rx=6, fill=WHITE)
    s.M("M256 220 V450", MID, 8)
    s.F("circle", outline=False, cx=256, cy=300, r=7, fill=MID)
    s.F("circle", outline=False, cx=256, cy=370, r=7, fill=MID)
    s.F("rect", outline=False, x=312, y=306, width=6, height=32, fill=A1)


def glove(s, x, f, color):
    s.F("path", d=f"M{x - 66 * f} 460 V310 C{x - 90 * f} 270 {x - 94 * f} 240 {x - 84 * f} 220 C{x - 76 * f} 204 {x - 58 * f} 208 {x - 56 * f} 228 V150 C{x - 56 * f} 128 {x - 30 * f} 128 {x - 30 * f} 150 V120 C{x - 30 * f} 98 {x - 4 * f} 98 {x - 4 * f} 120 V132 C{x - 4 * f} 112 {x + 22 * f} 112 {x + 22 * f} 134 V155 C{x + 22 * f} 140 {x + 46 * f} 140 {x + 46 * f} 158 V330 C{x + 46 * f} 380 {x + 36 * f} 420 {x + 36 * f} 460Z", fill=color)


@reg("lab-gloves")
def _(s):
    glove(s, 190, 1, "#8FE0C0")
    glove(s, 330, -1, "#9ED8F0")


@reg("fume-hood")
def _(s):
    s.F("rect", x=70, y=60, width=372, height=400, rx=20, fill=GREY)
    s.F("rect", x=100, y=100, width=312, height=220, rx=12, fill=GLASS)
    s.F("rect", outline=False, x=116, y=116, width=40, height=190, rx=8, fill=WHITE, fill_opacity="0.55")
    s.F("rect", x=100, y=320, width=312, height=24, rx=8, fill=DGREY)
    s.F("path", d="M200 320 V260 C200 240 230 240 230 260 V320Z", fill=A2L)
    s.F("circle", outline=False, cx=300, cy=290, r=26, fill=A1L)
    s.F("rect", x=100, y=364, width=312, height=66, rx=10, fill=DGREY)
    s.M("M180 397 H332", GREY, 10)


@reg("centrifuge")
def _(s):
    s.F("path", d="M70 440 V200 C70 130 130 110 256 110 C382 110 442 130 442 200 V440Z", fill=GREY)
    s.F("ellipse", cx=256, cy=200, rx=150, ry=58, fill=DGREY)
    s.F("ellipse", outline=False, cx=256, cy=200, rx=104, ry=30, fill="#3B4252")
    for x in (190, 256, 322):
        s.F("rect", outline=False, x=x - 8, y=186, width=16, height=24, rx=5, fill=A1L)
    s.F("circle", cx=256, cy=350, r=36, fill=A2)
    s.F("circle", outline=False, cx=256, cy=350, r=14, fill=A2L)


@reg("electronic-balance")
def _(s):
    s.F("path", d="M60 360 L100 250 H412 L452 360 V420 C452 440 440 450 420 450 H92 C72 450 60 440 60 420Z", fill=GREY)
    s.F("rect", x=170, y=130, width=172, height=110, rx=12, fill="#1F2A35")
    s.F("rect", outline=False, x=190, y=150, width=132, height=36, rx=6, fill="#9BE0A8")
    s.F("ellipse", cx=256, cy=112, rx=100, ry=22, fill=DGREY)
    s.F("rect", outline=False, x=120, y=330, width=80, height=40, rx=10, fill=A1)
    s.F("circle", outline=False, cx=400, cy=350, r=14, fill=A2)


@reg("spring-balance")
def _(s):
    ring(s, 256, 62, 26, DGREY, 12)
    s.F("rect", x=206, y=92, width=100, height=250, rx=22, fill=WHITE)
    s.F("rect", outline=False, x=236, y=116, width=40, height=190, rx=6, fill=GLASS_D)
    marks(s, 276, 124, 300, 8, 18)
    s.F("rect", outline=False, x=240, y=190, width=32, height=14, rx=5, fill=RED)
    s.T("M256 342 V400", DGREY, 10)
    ring(s, 256, 424, 24, DGREY, 12)
    s.F("rect", x=226, y=454, width=60, height=34, rx=10, fill=A2)


@reg("ph-meter")
def _(s):
    s.F("rect", x=60, y=100, width=280, height=330, rx=26, fill=A1)
    s.F("rect", outline=False, x=88, y=130, width=224, height=110, rx=12, fill="#9BE0A8")
    s.M("M118 205 H180 M206 172 h28 v36 h-28z M254 172 l22 36", "#1F2A35", 8)
    for i in range(3):
        s.F("circle", outline=False, cx=120 + i * 70, cy=300, r=22, fill=A1L)
    s.F("rect", outline=False, x=96, y=350, width=208, height=40, rx=14, fill=A1D)
    s.T("M340 330 C390 330 400 380 392 410", DGREY, 10)
    s.F("rect", x=372, y=340, width=40, height=130, rx=16, fill=GLASS)
    s.F("rect", outline=False, x=386, y=360, width=12, height=100, rx=6, fill=A2)


@reg("litmus-paper")
def _(s):
    for x, c in ((100, RED), (206, BLUE), (312, PURPLE)):
        s.F("rect", x=x, y=70, width=100, height=330, rx=10, fill="#F7F1E4")
        s.F("rect", outline=False, x=x, y=240, width=100, height=160, rx=10, fill=c)
        s.F("circle", outline=False, cx=x + 50, cy=135, r=12, fill=c)


@reg("ph-scale")
def _(s):
    cols = ["#E5484D", "#EE6A48", "#F5913E", "#F7AA36", "#FFC83D", "#E4D843", "#B8D84A", "#4CB963", "#35B58A", "#2FB5A8", "#3D8BFD", "#4F6FE0", "#6D5DE8", "#8B5CF6"]
    w = 384 / 14
    for i, c in enumerate(cols):
        s.F("rect", outline=False, x=f"{64 + i * w:.1f}", y=170, width=f"{w + 0.6:.1f}", height=140, fill=c)
    s.raw(f'<rect x="64" y="170" width="384" height="140" rx="28" fill="none" stroke="{INK}" stroke-width="10" data-outline="stroke"/>')
    s.F("path", d="M256 150 L224 100 H288Z", fill=DARK)
    s.F("circle", cx=110, cy=385, r=24, fill=RED)
    s.F("circle", cx=256, cy=385, r=24, fill=GREEN)
    s.F("circle", cx=402, cy=385, r=24, fill=PURPLE)


@reg("periodic-table")
def _(s):
    s.F("rect", x=36, y=96, width=440, height=250, rx=22, fill=WHITE)
    for r in range(4):
        for c in range(18):
            if r == 0 and 1 <= c <= 16:
                continue
            if r in (1, 2) and 2 <= c <= 11:
                continue
            col = RED if c == 0 else ORANGE if c == 1 else PURPLE if c == 17 else (A1 if 2 <= c <= 11 else GREEN if c < 14 else YEL)
            s.F("rect", outline=False, x=50 + c * 23.4, y=110 + r * 34, width=20, height=30, rx=4, fill=col)
    for c in range(15):
        s.F("rect", outline=False, x=96 + c * 23.4, y=262, width=20, height=18, rx=4, fill=PINK)
        s.F("rect", outline=False, x=96 + c * 23.4, y=286, width=20, height=18, rx=4, fill=A2L)
    s.F("rect", x=36, y=96, width=440, height=250, rx=22, fill="none")
    s.F("rect", outline=False, x=150, y=370, width=212, height=22, rx=11, fill=MID)


@reg("molecular-model-kit")
def _(s):
    s.T("M170 170 L256 270 L350 190 M256 270 L220 380 M256 270 L350 340", GREY, 14)
    for x, y, r, c in ((170, 170, 44, RED), (256, 270, 54, DGREY), (350, 190, 44, A1), (220, 380, 44, WHITE), (350, 340, 40, GREEN)):
        s.F("circle", cx=x, cy=y, r=r, fill=c)
        s.F("circle", outline=False, cx=x - r * 0.3, cy=y - r * 0.3, r=r * 0.26, fill=WHITE, fill_opacity="0.6")


@reg("dissection-tray")
def _(s):
    s.F("path", d="M50 200 H462 L430 400 C428 420 414 430 394 430 H118 C98 430 84 420 82 400Z", fill=GREY)
    s.F("path", outline=False, d="M92 220 H420 L398 390 H114Z", fill=DGREY)
    s.F("path", d="M150 290 C170 250 260 240 300 270 C340 290 330 350 290 360 C240 372 170 350 150 290Z", fill=PINK)
    s.M("M180 285 C220 268 270 272 292 292", WHITE, 8)
    s.T("M340 340 L420 260", GREY, 14)
    s.F("path", d="M410 250 L440 220 L436 262Z", fill=WHITE)


@reg("specimen-jar")
def _(s):
    s.F("rect", x=130, y=60, width=252, height=60, rx=16, fill=A1)
    s.F("path", d="M146 120 H366 V420 C366 450 346 462 320 462 H192 C166 462 146 450 146 420Z", fill=GLASS)
    s.F("path", outline=False, d="M154 170 H358 V420 C358 442 342 454 320 454 H192 C170 454 154 442 154 420Z", fill="#D9F0E0")
    s.F("path", d="M200 330 C210 280 290 270 330 320 C340 330 340 345 330 355 C300 390 210 390 200 330Z", fill=PINK)
    s.F("circle", outline=False, cx=310, cy=316, r=7, fill=INK)
    s.F("rect", outline=False, x=162, y=140, width=16, height=200, rx=8, fill=WHITE, fill_opacity="0.7")


@reg("prism")
def _(s):
    s.F("polygon", points="256,80 420,380 92,380", fill=GLASS)
    s.F("polygon", outline=False, points="256,112 276,150 150,360 130,360", fill=WHITE, fill_opacity="0.55")
    s.T("M40 300 L190 250", WHITE, 14)
    for i, c in enumerate((RED, ORANGE, YEL, GREEN, BLUE, PURPLE)):
        s.M(f"M330 {290 + i * 14} L470 {260 + i * 34}", c, 12)


@reg("convex-lens")
def _(s):
    s.F("path", d="M256 50 C400 160 400 352 256 462 C112 352 112 160 256 50Z", fill=GLASS)
    s.M("M236 100 C176 180 166 280 200 380", WHITE, 14)


@reg("concave-lens")
def _(s):
    s.F("path", d="M110 60 H402 C340 180 340 332 402 452 H110 C172 332 172 180 110 60Z", fill=GLASS)
    s.M("M146 110 C196 180 196 330 146 400", WHITE, 12)


@reg("mirror")
def _(s):
    s.F("rect", x=100, y=50, width=312, height=380, rx=40, fill=GOLD)
    s.F("rect", x=130, y=80, width=252, height=320, rx=22, fill="#CFEBFB")
    s.F("path", outline=False, d="M150 220 L300 90 H340 L150 280Z", fill=WHITE, fill_opacity="0.7")
    s.F("path", outline=False, d="M150 330 L360 110 H382 V150 L190 390 H150Z", fill=WHITE, fill_opacity="0.35")
    s.F("rect", x=210, y=430, width=92, height=40, rx=10, fill=DBROWN)


# ================================================================ scientific-method
@reg("scientific-method")
def _(s):
    cx, cy, r = 256, 256, 150
    ring(s, cx, cy, r, MID, 44)
    for i, c in enumerate([A1, A2, GREEN, PURPLE]):
        a0 = -90 + i * 90 + 8
        x1, y1 = arc_pt(cx, cy, r, a0)
        x2, y2 = arc_pt(cx, cy, r, a0 + 74)
        s.raw(f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{c}" stroke-width="44" stroke-linecap="round"/>')
    P(s, bulb, 256, 256, 0.38)


@reg("hypothesis")
def _(s):
    P(s, qmark, 190, 250, 0.8)
    P(s, bulb, 360, 190, 0.5)
    s.M("M290 340 H430", DGREY, 12)
    s.M("M290 390 H400", DGREY, 12)


@reg("experiment")
def _(s):
    s.F("path", d="M210 50 H302 V190 L410 400 C424 436 404 466 368 466 H144 C108 466 88 436 102 400 L210 190Z", fill=GLASS)
    s.F("path", outline=False, d="M156 320 H356 L402 410 C410 436 396 456 366 456 H146 C116 456 102 436 110 410Z", fill=GREEN)
    bubbles(s, [(220, 380, 14), (290, 350, 10), (330, 410, 12), (250, 320, 8)])
    s.F("circle", cx=300, cy=60, r=26, fill=A2L)
    s.F("circle", cx=346, cy=30, r=16, fill=A2L)


@reg("observation")
def _(s):
    s.F("path", d="M40 256 C110 130 402 130 472 256 C402 382 110 382 40 256Z", fill=WHITE)
    s.F("circle", cx=256, cy=256, r=88, fill=A1)
    s.F("circle", cx=256, cy=256, r=44, fill=DARK)
    s.F("circle", outline=False, cx=232, cy=232, r=16, fill=WHITE)


@reg("data-collection")
def _(s):
    s.F("rect", x=90, y=60, width=252, height=370, rx=22, fill=WHITE)
    s.F("rect", x=160, y=40, width=112, height=44, rx=14, fill=A1)
    for i in range(5):
        y = 130 + i * 56
        s.M(f"M120 {y} h40", A2, 12)
        s.M(f"M180 {y} h130", MID, 12)
    s.T("M350 460 L410 280", GOLD, 26)
    s.F("path", d="M410 280 L428 236 L392 262Z", fill=TAN)


@reg("conclusion")
def _(s):
    s.F("rect", x=90, y=60, width=300, height=380, rx=22, fill=WHITE)
    for y in (130, 180, 230):
        s.M(f"M130 {y} H350", MID, 12)
    P(s, check_badge, 330, 350, 0.42)


@reg("lab-notebook")
def _(s):
    s.F("path", d="M110 60 H400 C416 60 420 70 420 86 V430 C420 446 410 452 394 452 H110Z", fill=A1)
    s.F("rect", outline=False, x=150, y=60, width=14, height=392, fill=A1D)
    s.F("rect", x=190, y=110, width=170, height=120, rx=14, fill=WHITE)
    s.M("M206 200 C230 170 250 180 266 160 C290 130 320 150 344 130", A2, 12)
    s.F("circle", outline=False, cx=330, cy=330, r=36, fill=A1L)
    s.F("circle", outline=False, cx=250, cy=330, r=18, fill=A2L)
    s.F("rect", x=90, y=100, width=26, height=44, rx=8, fill=GREY)
    s.F("rect", x=90, y=250, width=26, height=44, rx=8, fill=GREY)


@reg("variables")
def _(s):
    s.T("M70 440 V90 M70 440 H450", DGREY, 16)
    s.T("M70 380 C170 360 250 260 420 120", A1, 22)
    for x, y in ((130, 330), (210, 300), (290, 230), (370, 160)):
        s.F("circle", cx=x, cy=y, r=20, fill=A2)
    s.F("path", d="M440 100 L392 112 L426 150Z", fill=A1)


@reg("graph-of-results")
def _(s):
    s.F("rect", x=60, y=70, width=392, height=370, rx=24, fill=WHITE)
    for i, (h, c) in enumerate(((120, A1), (190, A2), (150, A1L), (250, A1))):
        s.F("rect", outline=False, x=100 + i * 82, y=400 - h, width=54, height=h, rx=8, fill=c)
    s.M("M100 420 H420", DGREY, 8)
    s.M("M110 330 L190 270 L270 300 L350 200 L420 130", RED, 10)
    s.F("circle", cx=420, cy=130, r=14, fill=RED)


if __name__ == "__main__":
    run("science", D, sys.argv[1:] or None)
