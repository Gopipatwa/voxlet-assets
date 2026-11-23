"""Shared helpers for the technology, future-tech and inventions drawings (themed colours only)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID  # noqa: E402,F401
from draw_lib import C, INK, arc_pt, head, run, star_pts  # noqa: E402,F401
from text_tile import text_path  # noqa: E402

WHITE = LIGHT
SKIN, HAIR = C["skin"], "#4A3B32"
OW = 10


def registry():
    D = {}

    def reg(name):
        def r(fn):
            D[name] = fn
            return fn
        return r
    return D, reg


def txt(s, text, cx, cy, w, h, color=WHITE, font="black"):
    d, _ = text_path(text, font, cx, cy, w, h)
    if d:
        s.F("path", outline=False, d=d, fill=color)


def ring(s, cx, cy, r, color, w):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w + 2 * OW}" data-outline="under"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>')


def dot(s, x, y, r, color=DARK):
    s.F("circle", outline=False, cx=x, cy=y, r=r, fill=color)


def screen(s, x, y, w, h, body=DARK, glass=A1L, rx=20, pad=16):
    s.F("rect", x=x, y=y, width=w, height=h, rx=rx, fill=body)
    s.F("rect", outline=False, x=x + pad, y=y + pad, width=w - 2 * pad, height=h - 2 * pad, rx=max(rx - 10, 4), fill=glass)


def shine(s, x, y, w, h=18, op="0.4"):
    s.F("rect", outline=False, x=x, y=y, width=w, height=h, rx=h / 2, fill=WHITE, fill_opacity=op)


def wifi(s, cx, cy, r=120, color=A1, w=22, n=3):
    for i in range(n):
        rr = r * (i + 1) / n
        x0, y0 = arc_pt(cx, cy, rr, -135)
        x1, y1 = arc_pt(cx, cy, rr, -45)
        s.raw(f'<path d="M{x0:.0f} {y0:.0f} A{rr:.0f} {rr:.0f} 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
    s.F("circle", cx=cx, cy=cy, r=w * 0.7, fill=color)


def waves(s, cx, cy, r=120, color=A1, w=16, n=3, a0=-50, a1=50):
    for i in range(n):
        rr = r * (i + 1) / n
        x0, y0 = arc_pt(cx, cy, rr, a0)
        x1, y1 = arc_pt(cx, cy, rr, a1)
        s.raw(f'<path d="M{x0:.0f} {y0:.0f} A{rr:.0f} {rr:.0f} 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')


def bolt(s, cx=256, cy=256, k=1.0, color=A2):
    pts = [(30, -150), (-70, 20), (-6, 20), (-34, 150), (76, -40), (6, -40), (60, -150)]
    s.F("polygon", points=" ".join(f"{cx + x * k:.0f},{cy + y * k:.0f}" for x, y in pts), fill=color)


def cloud(s, cx=256, cy=256, k=1.0, color=LIGHT):
    s.open(transform=f"translate({cx} {cy}) scale({k}) translate(-256 -256)")
    s.F("path", d="M150 380 C80 380 60 300 120 280 C110 210 190 170 240 210 C280 140 400 160 400 250 C470 250 480 380 400 380Z", fill=color)
    s.close()


def arrow(s, x1, y1, x2, y2, color=A2, w=22, hl=56):
    s.T(f"M{x1} {y1} L{x2} {y2}", color, w)
    a = math.atan2(y2 - y1, x2 - x1)
    tip = (x2 + 14 * math.cos(a), y2 + 14 * math.sin(a))
    p1 = (x2 + hl * math.cos(a + math.radians(150)), y2 + hl * math.sin(a + math.radians(150)))
    p2 = (x2 + hl * math.cos(a - math.radians(150)), y2 + hl * math.sin(a - math.radians(150)))
    s.F("polygon", points=f"{tip[0]:.0f},{tip[1]:.0f} {p1[0]:.0f},{p1[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}", fill=color)


def lock(s, cx=256, cy=300, k=1.0, color=A2, open_=False):
    s.open(transform=f"translate({cx} {cy}) scale({k}) translate(-256 -300)")
    if open_:
        s.T("M196 240 V190 C196 120 316 120 316 190", MID, 24)
    else:
        s.T("M196 250 V200 C196 120 316 120 316 200 V250", MID, 24)
    s.F("rect", x=156, y=240, width=200, height=170, rx=28, fill=color)
    s.F("circle", outline=False, cx=256, cy=312, r=20, fill=DARK)
    s.F("rect", outline=False, x=246, y=316, width=20, height=52, rx=8, fill=DARK)
    s.close()


def person_hood(s, cx=256, cy=256, k=1.0):
    """Faceless hooded figure (hacker)."""
    s.open(transform=f"translate({cx} {cy}) scale({k}) translate(-256 -256)")
    s.F("path", d="M110 470 C110 360 170 310 256 310 C342 310 402 360 402 470Z", fill=A1)
    s.F("path", d="M256 50 C340 50 380 130 370 210 C362 270 330 310 256 310 C182 310 150 270 142 210 C132 130 172 50 256 50Z", fill=A1D)
    s.F("ellipse", cx=256, cy=200, rx=82, ry=90, fill=DARK)
    s.F("circle", outline=False, cx=226, cy=196, r=10, fill=A2L)
    s.F("circle", outline=False, cx=286, cy=196, r=10, fill=A2L)
    s.close()
