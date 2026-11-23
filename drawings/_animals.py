"""Animal templates (style B, natural colours). Side view facing right, ground at y = 440.

quad(s, **p)   four-legged mammals (farm, wild, pets, big cats...)
bird(s, **p)   birds, standing or swimming
fish(s, **p)   fish and fish-like animals
bug(s, **p)    insects and spiders
Plus smaller helpers. Every template has eyes in part-eye-* groups so the engine can blink them.
"""
import hashlib
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from draw_lib import C, INK, arc_pt, star_pts  # noqa: E402

WHITE, BLACK = C["white"], C["black"]
GROUND = 440


def shade(hex_color, k=0.8):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, int(v * k))) for v in (r, g, b)))


def tint(hex_color, k=0.35):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#{:02X}{:02X}{:02X}".format(*(int(v + (255 - v) * k) for v in (r, g, b)))


def eye(s, x, y, r, side="right", color=BLACK):
    s.open(f"part-eye-{side}", f"{x:.0f} {y:.0f}")
    s.F("circle", outline=False, cx=f"{x:.1f}", cy=f"{y:.1f}", r=f"{r:.1f}", fill=color)
    s.F("circle", outline=False, cx=f"{x + r * 0.35:.1f}", cy=f"{y - r * 0.35:.1f}", r=f"{r * 0.35:.1f}", fill=WHITE)
    s.close()


# ---------------------------------------------------------------- four-legged mammals
class _Sil:
    """Shapes that together make one silhouette: drawn once with the outline, then again without,
    so the outline only shows around the whole animal, never at the joins between parts."""

    def __init__(self):
        self.items = []

    def add(self, tag, **a):
        self.items.append((tag, a))

    def draw(self, s):
        for tag, a in self.items:
            s.F(tag, **a)
        for tag, a in self.items:
            s.F(tag, outline=False, **a)


def _limb(pts, w0, w1):
    """Tapered limb through pts (top to foot), width w0 at the top and w1 at the foot, round end."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    d = f"M{left[0][0]:.0f} {left[0][1]:.0f}"
    for x, y in left[1:]:
        d += f" L{x:.0f} {y:.0f}"
    ex, ey = pts[-1]
    rx_, ry_ = right[-1]
    d += f" Q{ex:.0f} {ey + w1 * 0.5:.0f} {rx_:.0f} {ry_:.0f}"
    for x, y in reversed(right[:-1]):
        d += f" L{x:.0f} {y:.0f}"
    return d + " Z"


def _capsule(x1, y1, r1, x2, y2, r2):
    """Closed shape around two circles (a skull and a muzzle)."""
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy) or 1
    a = math.atan2(dy, dx)
    off = math.acos(max(-1.0, min(1.0, (r1 - r2) / dist)))
    p = []
    for sgn in (1, -1):
        t = a + sgn * off
        p.append(((x1 + r1 * math.cos(t), y1 + r1 * math.sin(t)), (x2 + r2 * math.cos(t), y2 + r2 * math.sin(t))))
    (a1, b1), (a2, b2) = p
    return (f"M{a1[0]:.1f} {a1[1]:.1f} L{b1[0]:.1f} {b1[1]:.1f} A{r2:.1f} {r2:.1f} 0 0 0 {b2[0]:.1f} {b2[1]:.1f} "
            f"L{a2[0]:.1f} {a2[1]:.1f} A{r1:.1f} {r1:.1f} 0 1 0 {a1[0]:.1f} {a1[1]:.1f} Z")


def quad(s, body="#C68A5C", belly=None, bw=1.0, bh=1.0, leg=1.0, leg_w=28, hoof=None, neck=0.0,
         head_r=58, snout="round", snout_c=None, nose=BLACK, ears="pointy", ear_c=None, ear_in=None,
         horns=None, horn_c="#E8DCC8", tail="thin", tail_c=None, mane=None, hump=0, pattern=None,
         pat_c=BLACK, seed=1, trunk=False, tusks=False, whiskers=False, cx=225, tongue=False, chin=None,
         back_slope=0, wool=None, head_c=None, leg_c=None, mask=None):
    """Four-legged mammal, side view facing right. One silhouette: back line with withers and rump,
    deep chest, tucked belly, haunch, tapered neck, skull + muzzle head, legs with knees and hocks."""
    rx, ry = 132 * bw, 74 * bh
    leg_h = 110 * leg
    cy = GROUND - leg_h - ry * 0.55
    dark = shade(body, 0.82)
    tail_c = tail_c or body
    head_fill = head_c or body
    snout_c = snout_c or tint(head_fill, 0.35)
    ear_c = ear_c or head_fill
    leg_fill = leg_c or body
    heavy = leg_w >= 40          # elephants, bears, hippos: straight pillar legs
    runner = leg >= 0.9 and not heavy

    # head: skull at (hx, hy); muzzle along angle `ma` (degrees, + is down)
    long_face = snout in ("long", "flat", "thin")
    hx = cx + rx * (0.95 if neck <= 0.2 else 0.8) + head_r * (0.45 if neck <= 0.2 else 0.25)
    hy = cy - ry * 0.55 - neck * 170
    skull_r = head_r * (0.82 if long_face else 1.0)
    ma = {"long": 38, "flat": 30, "thin": 30, "round": 12, "pig": 10, "short": 10, "normal": 15}.get(snout, 0)
    ml = {"long": 1.2, "flat": 0.95, "thin": 1.25, "round": 0.72, "pig": 0.85, "short": 0.6, "normal": 0.75}.get(snout, 0) * head_r
    mr = {"long": 0.42, "flat": 0.55, "thin": 0.3, "round": 0.5, "pig": 0.5, "short": 0.45, "normal": 0.45}.get(snout, 0) * head_r
    mx, my = hx + ml * math.cos(math.radians(ma)), hy + ml * math.sin(math.radians(ma))
    has_muzzle = ml > 0

    # fit the whole animal inside the 512 frame
    left = cx - rx * 1.0 - (110 if tail in ("bushy", "long", "horse") else 60)
    right = max(mx + mr, hx + skull_r) + (head_r * 0.8 if trunk or tusks else 10)
    if whiskers:
        right = max(right, mx + mr + 50)
    if horns == "rhino":
        right = max(right, mx + mr + 20)
    top_k = {"long": 1.6, "pointy": 1.4, "round": 1.15, "elephant": 1.2}.get(ears, 1.05)
    top_k = max(top_k, {"antlers": 3.6, "goat": 1.75, "long-curved": 2.3, "cow": 1.5, "small": 1.5, "ram": 1.4}.get(horns, 0))
    if mane == "lion":
        top_k = max(top_k, 1.6)
    top = min(hy - head_r * top_k, cy - ry * (1.5 if hump else 1.0))
    bottom = max(GROUND + 6, hy + head_r * 2.4 if trunk else GROUND + 6)
    k = min(1.0, 452 / (right - left), 430 / (bottom - top))
    s.open(transform=f"translate({256 - k * (left + right) / 2:.1f} {466 - k * bottom:.1f}) scale({k:.3f})")

    # legs: front leg under the withers, hind leg under the haunch
    fx, bx = cx + rx * 0.55, cx - rx * 0.58
    ltop = cy + ry * 0.2
    w0, w1 = leg_w * 1.25, leg_w * (0.95 if heavy else 0.72)

    def front_leg(x):
        if heavy:
            return [(x, ltop), (x + 2, GROUND - 4)]
        kn = ltop + (GROUND - ltop) * 0.55
        return [(x, ltop), (x + 4, kn), (x + 2, GROUND - 4)]

    def hind_leg(x):
        if heavy or not runner:
            return [(x, ltop), (x - 4, (ltop + GROUND) / 2), (x, GROUND - 4)]
        hock = GROUND - (GROUND - ltop) * 0.38
        return [(x + 8, ltop), (x - leg_w * 0.55, hock), (x - leg_w * 0.25, GROUND - 4)]

    def foot(x, y, col):
        if hoof:
            s.F("path", d=f"M{x - w1 / 2 - 3:.0f} {y - 14:.0f} H{x + w1 / 2 + 3:.0f} L{x + w1 / 2 + 6:.0f} {y + 6:.0f} H{x - w1 / 2 - 4:.0f} Z", fill=hoof)
        elif not heavy:
            s.F("ellipse", cx=f"{x + w1 * 0.25:.0f}", cy=f"{y + 1:.0f}", rx=f"{w1 * 0.72:.0f}", ry=f"{w1 * 0.36:.0f}", fill=col)

    far = shade(leg_fill, 0.8)
    for pts in (front_leg(fx - rx * 0.2), hind_leg(bx + rx * 0.22)):
        s.F("path", d=_limb(pts, w0 * 0.9, w1 * 0.9), fill=far)
        foot(pts[-1][0], GROUND - 4, far)

    # tail (behind the body)
    tx, ty = cx - rx * 0.95, cy - ry * 0.45
    if tail == "thin":
        s.T(f"M{tx:.0f} {ty:.0f} C{tx - 40:.0f} {ty + 20:.0f} {tx - 46:.0f} {ty + 80:.0f} {tx - 36:.0f} {ty + 110:.0f}", tail_c, 12)
    elif tail == "tuft":
        s.T(f"M{tx:.0f} {ty:.0f} C{tx - 40:.0f} {ty + 20:.0f} {tx - 46:.0f} {ty + 70:.0f} {tx - 40:.0f} {ty + 100:.0f}", tail_c, 12)
        s.F("ellipse", cx=f"{tx - 40:.0f}", cy=f"{ty + 112:.0f}", rx=16, ry=26, fill=mane or dark)
    elif tail == "bushy":
        s.F("path", d=f"M{tx + 14:.0f} {ty:.0f} C{tx - 70:.0f} {ty - 50:.0f} {tx - 120:.0f} {ty + 60:.0f} {tx - 70:.0f} {ty + 120:.0f} "
                      f"C{tx - 50:.0f} {ty + 60:.0f} {tx - 20:.0f} {ty + 34:.0f} {tx + 14:.0f} {ty + 34:.0f}Z", fill=tail_c)
    elif tail == "curl":
        s.T(f"M{tx:.0f} {ty:.0f} c-30 -10 -40 30 -16 34 c20 4 18 -24 -2 -20", tail_c, 8)
    elif tail == "short":
        s.F("ellipse", cx=f"{tx - 4:.0f}", cy=f"{ty:.0f}", rx=18, ry=14, fill=tail_c)
    elif tail == "long":
        s.T(f"M{tx:.0f} {ty:.0f} C{tx - 60:.0f} {ty + 10:.0f} {tx - 90:.0f} {ty + 60:.0f} {tx - 70:.0f} {ty + 130:.0f}", tail_c, 16)
    elif tail == "horse":
        s.F("path", d=f"M{tx + 8:.0f} {ty - 8:.0f} C{tx - 50:.0f} {ty - 12:.0f} {tx - 64:.0f} {ty + 80:.0f} {tx - 40:.0f} {ty + 160:.0f} "
                      f"C{tx - 20:.0f} {ty + 100:.0f} {tx - 10:.0f} {ty + 40:.0f} {tx + 12:.0f} {ty + 24:.0f}Z", fill=mane or dark)

    # ears and horns behind the head
    ex, ey = hx - head_r * 0.35, hy - head_r * 0.75
    ec = ear_c
    if mane == "lion":
        mc = C["darkbrown"] if body != C["darkbrown"] else C["brown"]
        tufts = [(hx - head_r * 0.15 + head_r * 1.1 * math.cos(math.radians(a)), hy + head_r * 0.15 + head_r * 1.15 * math.sin(math.radians(a))) for a in range(95, 300, 23)]
        for x, y in tufts:
            s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=f"{head_r * 0.5:.0f}", fill=mc)
        for x, y in tufts:
            s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=f"{head_r * 0.5:.0f}", fill=mc)
        s.F("circle", outline=False, cx=f"{hx - head_r * 0.15:.0f}", cy=f"{hy + head_r * 0.15:.0f}", r=f"{head_r * 1.1:.0f}", fill=mc)
    if ears == "pointy":
        s.F("polygon", points=f"{ex - 22:.0f},{ey + 22:.0f} {ex + 2:.0f},{ey - 40:.0f} {ex + 28:.0f},{ey + 16:.0f}", fill=ec)
        if ear_in:
            s.F("polygon", outline=False, points=f"{ex - 10:.0f},{ey + 12:.0f} {ex + 3:.0f},{ey - 22:.0f} {ex + 16:.0f},{ey + 10:.0f}", fill=ear_in)
    elif ears in ("round", "big"):
        er = head_r * (0.42 if ears == "big" else 0.32)
        s.F("circle", cx=f"{ex:.0f}", cy=f"{ey:.0f}", r=f"{er:.0f}", fill=ec)
        if ear_in:
            s.F("circle", outline=False, cx=f"{ex:.0f}", cy=f"{ey:.0f}", r=f"{er * 0.5:.0f}", fill=ear_in)
    elif ears == "long":
        s.F("ellipse", cx=f"{ex:.0f}", cy=f"{ey - head_r * 0.6:.0f}", rx=f"{head_r * 0.22:.0f}", ry=f"{head_r * 0.85:.0f}", fill=ec,
            transform=f"rotate(-14 {ex:.0f} {ey:.0f})")
        if ear_in:
            s.F("ellipse", outline=False, cx=f"{ex:.0f}", cy=f"{ey - head_r * 0.6:.0f}", rx=f"{head_r * 0.1:.0f}", ry=f"{head_r * 0.6:.0f}", fill=ear_in,
                transform=f"rotate(-14 {ex:.0f} {ey:.0f})")
    elif ears == "side":
        s.F("ellipse", cx=f"{hx - head_r * 0.8:.0f}", cy=f"{hy - head_r * 0.4:.0f}", rx=f"{head_r * 0.45:.0f}", ry=f"{head_r * 0.2:.0f}", fill=ec,
            transform=f"rotate(-20 {hx - head_r * 0.8:.0f} {hy - head_r * 0.4:.0f})")
    if horns == "cow":
        s.T(f"M{hx - head_r * 0.2:.0f} {hy - head_r * 0.75:.0f} C{hx - head_r * 0.4:.0f} {hy - head_r * 1.3:.0f} {hx - head_r * 0.1:.0f} {hy - head_r * 1.5:.0f} {hx + head_r * 0.15:.0f} {hy - head_r * 1.45:.0f}", horn_c, 14)
    elif horns == "goat":
        s.T(f"M{hx - head_r * 0.1:.0f} {hy - head_r * 0.75:.0f} C{hx - head_r * 0.4:.0f} {hy - head_r * 1.6:.0f} {hx - head_r * 0.9:.0f} {hy - head_r * 1.6:.0f} {hx - head_r * 1.1:.0f} {hy - head_r * 1.2:.0f}", horn_c, 14)
    elif horns == "ram":
        s.T(f"M{hx - head_r * 0.1:.0f} {hy - head_r * 0.7:.0f} c-50 -40 -110 10 -70 60 c30 30 70 0 40 -20", horn_c, 20)
    elif horns == "antlers":
        ax, ay = hx - head_r * 0.1, hy - head_r * 0.8
        s.T(f"M{ax:.0f} {ay:.0f} L{ax - 20:.0f} {ay - 110:.0f} M{ax - 8:.0f} {ay - 40:.0f} L{ax - 60:.0f} {ay - 70:.0f} M{ax - 15:.0f} {ay - 80:.0f} L{ax + 20:.0f} {ay - 120:.0f} "
            f"M{ax - 18:.0f} {ay - 100:.0f} L{ax - 60:.0f} {ay - 130:.0f}", horn_c, 10)
    elif horns == "small":
        s.T(f"M{hx - head_r * 0.15:.0f} {hy - head_r * 0.8:.0f} L{hx - head_r * 0.2:.0f} {hy - head_r * 1.35:.0f}", horn_c, 12)
        s.F("circle", cx=f"{hx - head_r * 0.2:.0f}", cy=f"{hy - head_r * 1.4:.0f}", r=9, fill=shade(body, 0.7))
    elif horns == "long-curved":
        s.T(f"M{hx - head_r * 0.1:.0f} {hy - head_r * 0.75:.0f} C{hx - head_r * 0.5:.0f} {hy - head_r * 1.8:.0f} {hx - head_r * 1.2:.0f} {hy - head_r * 2.2:.0f} {hx - head_r * 1.8:.0f} {hy - head_r * 2.1:.0f}", horn_c, 12)
    if ears == "elephant":
        s.F("path", d=f"M{hx - head_r * 0.1:.0f} {hy - head_r * 0.85:.0f} C{hx - head_r * 1.5:.0f} {hy - head_r * 1.2:.0f} {hx - head_r * 1.7:.0f} {hy + head_r * 0.9:.0f} "
                      f"{hx - head_r * 0.5:.0f} {hy + head_r * 1.0:.0f} C{hx - head_r * 0.3:.0f} {hy + head_r * 0.4:.0f} {hx - head_r * 0.2:.0f} {hy:.0f} {hx - head_r * 0.1:.0f} {hy - head_r * 0.85:.0f}Z",
            fill=ear_in or tint(body, 0.15))

    # the silhouette: body, hump, haunch, neck, head, near legs
    sil = _Sil()
    top_y = cy - ry * 0.92
    body_d = (f"M{cx - rx * 0.98:.0f} {cy - ry * 0.05:.0f} "
              f"C{cx - rx * 1.02:.0f} {cy - ry * 0.75:.0f} {cx - rx * 0.75:.0f} {top_y:.0f} {cx - rx * 0.45:.0f} {top_y + ry * 0.04:.0f} "
              f"C{cx - rx * 0.1:.0f} {top_y + ry * (0.18 + back_slope * 0.01):.0f} {cx + rx * 0.3:.0f} {top_y - ry * 0.02:.0f} {cx + rx * 0.62:.0f} {top_y - ry * 0.04:.0f} "
              f"C{cx + rx * 0.95:.0f} {top_y + ry * 0.05:.0f} {cx + rx * 1.05:.0f} {cy - ry * 0.2:.0f} {cx + rx * 1.0:.0f} {cy + ry * 0.2:.0f} "
              f"C{cx + rx * 0.98:.0f} {cy + ry * 0.75:.0f} {cx + rx * 0.7:.0f} {cy + ry * 0.95:.0f} {cx + rx * 0.4:.0f} {cy + ry * 0.92:.0f} "
              f"C{cx + rx * 0.1:.0f} {cy + ry * 0.88:.0f} {cx - rx * 0.2:.0f} {cy + ry * 0.7:.0f} {cx - rx * 0.45:.0f} {cy + ry * 0.78:.0f} "
              f"C{cx - rx * 0.85:.0f} {cy + ry * 0.9:.0f} {cx - rx * 0.97:.0f} {cy + ry * 0.5:.0f} {cx - rx * 0.98:.0f} {cy - ry * 0.05:.0f} Z")
    if wool:
        for a in range(0, 360, 24):
            wx, wy = cx + math.cos(math.radians(a)) * rx * 0.9, cy + math.sin(math.radians(a)) * ry * 0.85
            sil.add("circle", cx=f"{wx:.0f}", cy=f"{wy:.0f}", r=f"{ry * 0.42:.0f}", fill=wool)
    if hump:
        for i in range(hump):
            hxp = cx - rx * 0.15 + (i - (hump - 1) / 2) * rx * 0.55
            sil.add("ellipse", cx=f"{hxp:.0f}", cy=f"{cy - ry * 0.75:.0f}", rx=f"{rx * 0.36:.0f}", ry=f"{ry * 0.8:.0f}", fill=wool or body)
    sil.add("path", d=body_d, fill=wool or body)
    sil.add("ellipse", cx=f"{bx + rx * 0.08:.0f}", cy=f"{cy + ry * 0.12:.0f}", rx=f"{rx * 0.34:.0f}", ry=f"{ry * 0.78:.0f}", fill=wool or body)
    # neck: from withers and chest to the back and throat of the skull
    nb = head_r * (0.75 if neck > 0.2 else 0.85)
    sil.add("path", d=(f"M{cx + rx * 0.35:.0f} {top_y + ry * 0.1:.0f} "
                       f"C{cx + rx * 0.6:.0f} {top_y - ry * 0.1:.0f} {hx - nb * 1.0:.0f} {hy - nb * 0.2:.0f} {hx - nb * 0.6:.0f} {hy - nb * 0.6:.0f} "
                       f"L{hx + nb * 0.3:.0f} {hy + nb * 0.4:.0f} "
                       f"C{hx:.0f} {hy + nb * 1.2:.0f} {cx + rx * 1.05:.0f} {cy - ry * 0.3:.0f} {cx + rx * 0.95:.0f} {cy + ry * 0.3:.0f} Z"), fill=body)
    if has_muzzle:
        sil.add("path", d=_capsule(hx, hy, skull_r, mx, my, mr), fill=head_fill)
    else:
        sil.add("circle", cx=f"{hx:.0f}", cy=f"{hy:.0f}", r=f"{skull_r:.0f}", fill=head_fill)
    near_f, near_b = front_leg(fx), hind_leg(bx)
    sil.add("path", d=_limb(near_f, w0, w1), fill=leg_fill)
    sil.add("path", d=_limb(near_b, w0 * 1.1, w1), fill=leg_fill)
    sil.draw(s)
    foot(near_f[-1][0], GROUND - 4, leg_fill)
    foot(near_b[-1][0], GROUND - 4, leg_fill)

    # belly and coat pattern, clipped to the body
    cid = "clip-" + hashlib.md5(body_d.encode()).hexdigest()[:10]
    s.raw(f'<defs><clipPath id="{cid}"><path d="{body_d}"/></clipPath></defs>')
    s.raw(f'<g clip-path="url(#{cid})">')
    if belly:
        s.F("ellipse", outline=False, cx=f"{cx + rx * 0.1:.0f}", cy=f"{cy + ry * 0.85:.0f}", rx=f"{rx * 0.8:.0f}", ry=f"{ry * 0.4:.0f}", fill=belly)
    rnd = random.Random(seed)
    if pattern == "spots":
        for _ in range(int(11 * bw)):
            x, y = cx + rnd.uniform(-0.85, 0.85) * rx, cy + rnd.uniform(-0.75, 0.6) * ry
            s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=f"{rnd.uniform(7, 12):.0f}", fill=pat_c)
    elif pattern == "patches":
        for _ in range(4):
            x, y = cx + rnd.uniform(-0.7, 0.6) * rx, cy + rnd.uniform(-0.7, 0.5) * ry
            s.F("ellipse", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", rx=f"{rnd.uniform(26, 40):.0f}", ry=f"{rnd.uniform(18, 28):.0f}",
                fill=pat_c, transform=f"rotate({rnd.randint(-40, 40)} {x:.0f} {y:.0f})")
    elif pattern == "giraffe":
        for r in range(4):
            for c in range(6):
                x = cx - rx * 0.95 + c * rx * 0.36 + (r % 2) * rx * 0.18
                y = cy - ry * 0.85 + r * ry * 0.48
                s.F("rect", outline=False, x=f"{x - 18:.0f}", y=f"{y - 14:.0f}", width=36, height=28, rx=8, fill=pat_c)
    elif pattern == "stripes":
        for i in range(-4, 5):
            x = cx + i * rx * 0.2
            s.M(f"M{x - 6:.0f} {cy - ry:.0f} C{x + 12:.0f} {cy - ry * 0.3:.0f} {x - 12:.0f} {cy + ry * 0.2:.0f} {x + 4:.0f} {cy + ry * 0.55:.0f}", pat_c, 12)
    elif pattern == "rosettes":
        for _ in range(int(11 * bw)):
            x, y = cx + rnd.uniform(-0.85, 0.85) * rx, cy + rnd.uniform(-0.75, 0.6) * ry
            s.raw(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="none" stroke="{pat_c}" stroke-width="5" stroke-dasharray="12 6"/>')
    s.raw("</g>")
    # a soft line for the haunch and shoulder so the body reads in 3D
    s.M(f"M{bx + rx * 0.3:.0f} {cy - ry * 0.45:.0f} C{bx + rx * 0.4:.0f} {cy + ry * 0.1:.0f} {bx + rx * 0.3:.0f} {cy + ry * 0.5:.0f} {bx + rx * 0.15:.0f} {cy + ry * 0.75:.0f}", shade(body, 0.7), 5)

    if ears == "floppy":   # dogs: soft ear hanging down the side of the head
        fx0, fy0 = hx - skull_r * 0.25, hy - skull_r * 0.85
        s.F("path", d=(f"M{fx0:.0f} {fy0:.0f} C{fx0 - skull_r * 0.7:.0f} {fy0 - skull_r * 0.1:.0f} {fx0 - skull_r * 0.75:.0f} {fy0 + skull_r * 1.2:.0f} "
                       f"{fx0 - skull_r * 0.35:.0f} {fy0 + skull_r * 1.45:.0f} C{fx0 - skull_r * 0.05:.0f} {fy0 + skull_r * 1.55:.0f} {fx0 + skull_r * 0.25:.0f} {fy0 + skull_r * 0.6:.0f} {fx0 + skull_r * 0.3:.0f} {fy0 + skull_r * 0.1:.0f} Z"),
            fill=ear_in or shade(head_fill, 0.75))

    # neck mane (horse, zebra)
    if mane and mane != "lion" and neck > 0:
        s.T(f"M{cx + rx * 0.45:.0f} {top_y + ry * 0.02:.0f} C{cx + rx * 0.7:.0f} {top_y - ry * 0.2:.0f} {hx - nb * 1.1:.0f} {hy - nb * 0.4:.0f} {hx - nb * 0.55:.0f} {hy - nb * 0.75:.0f}", mane, 16)

    # face
    if mask:
        s.F("ellipse", outline=False, cx=f"{hx + head_r * 0.2:.0f}", cy=f"{hy - head_r * 0.15:.0f}", rx=f"{head_r * 0.32:.0f}", ry=f"{head_r * 0.24:.0f}", fill=mask)
    if chin:
        s.F("ellipse", outline=False, cx=f"{(hx + mx) / 2 if has_muzzle else hx:.0f}", cy=f"{hy + head_r * 0.5:.0f}", rx=f"{head_r * 0.6:.0f}", ry=f"{head_r * 0.3:.0f}", fill=chin)
    nx = ny = None
    if has_muzzle and snout != "pig":
        s.F("circle", outline=False, cx=f"{mx:.0f}", cy=f"{my:.0f}", r=f"{mr * 0.95:.0f}", fill=snout_c)
        nx, ny = mx + mr * 0.55, my - mr * 0.35
        s.M(f"M{mx + mr * 0.7:.0f} {my + mr * 0.45:.0f} Q{mx + mr * 0.1:.0f} {my + mr * 0.7:.0f} {mx - mr * 0.5:.0f} {my + mr * 0.45:.0f}", shade(snout_c, 0.55), 4)
    elif snout == "pig":
        s.F("ellipse", cx=f"{mx + mr * 0.5:.0f}", cy=f"{my:.0f}", rx=f"{mr * 0.45:.0f}", ry=f"{mr * 0.7:.0f}", fill=snout_c or tint(body, 0.2))
        for dy in (-0.25, 0.25):
            s.F("ellipse", outline=False, cx=f"{mx + mr * 0.55:.0f}", cy=f"{my + mr * dy:.0f}", rx=4, ry=7, fill=shade(snout_c, 0.6))
    if nx is not None and nose:
        s.F("ellipse", outline=False, cx=f"{nx:.0f}", cy=f"{ny:.0f}", rx=f"{max(6, mr * 0.3):.0f}", ry=f"{max(5, mr * 0.22):.0f}", fill=nose)
    if tongue and has_muzzle:
        s.F("ellipse", cx=f"{mx + mr * 0.1:.0f}", cy=f"{my + mr * 0.95:.0f}", rx=10, ry=14, fill=C["pink"])
    if whiskers and has_muzzle:
        s.M(f"M{mx + mr * 0.3:.0f} {my:.0f} l50 -10 M{mx + mr * 0.3:.0f} {my + 8:.0f} l50 8", INK, 3)
    if horns == "rhino":
        s.F("path", d=f"M{mx - mr * 0.2:.0f} {my - mr * 0.8:.0f} L{mx + mr * 0.5:.0f} {my - mr * 2.4:.0f} L{mx + mr * 0.7:.0f} {my - mr * 0.6:.0f}Z", fill=horn_c)
    if trunk:
        s.T(f"M{hx + skull_r * 0.6:.0f} {hy + skull_r * 0.2:.0f} C{hx + head_r * 1.2:.0f} {hy + head_r * 0.6:.0f} {hx + head_r * 1.1:.0f} {hy + head_r * 1.8:.0f} {hx + head_r * 1.4:.0f} {hy + head_r * 2.2:.0f}",
            head_fill, head_r * 0.42)
    if tusks:
        tbx, tby = (hx + skull_r * 0.6, hy + skull_r * 0.6) if trunk else (mx, my + mr * 0.6)
        s.T(f"M{tbx:.0f} {tby:.0f} C{tbx + head_r * 0.4:.0f} {tby + head_r * 0.4:.0f} {tbx + head_r * 0.7:.0f} {tby + head_r * 0.3:.0f} {tbx + head_r * 0.85:.0f} {tby:.0f}", "#FFF8E7", 12)
    eye(s, hx + skull_r * 0.32, hy - skull_r * 0.18, max(7, head_r * 0.13))
    s.close()
    return hx, hy


# ---------------------------------------------------------------- birds
def bird(s, body="#3D8BFD", belly=None, wing=None, head_c=None, beak="short", beak_c="#F5913E", legs_c="#F5913E",
         tail="fan", tail_c=None, crest=None, neck=0.0, leg=1.0, size=1.0, swim=False, eye_ring=None, cheek=None,
         wattle=None, comb=None, cx=230):
    rx, ry = 112 * size, 78 * size
    leg_h = 0 if swim else 90 * leg
    cy = (360 if swim else GROUND - leg_h - ry * 0.7)
    wing = wing or shade(body, 0.8)
    tail_c = tail_c or wing
    head_c = head_c or body
    hr = 50 * size
    hx = cx + rx * 0.72
    hy = cy - ry * 0.75 - neck * 150

    _bx = hx + hr * 0.9
    left = cx - rx * 0.9 - (150 * size if tail == "long" else 90 * size)
    right = _bx + hr * (2.0 if beak in ("big", "pouch", "long") else 0.9)
    top = hy - hr * (1.8 if crest else 1.3 if comb else 1.05)
    bottom = 470 if swim else GROUND
    k = min(1.0, 452 / (right - left), 430 / (bottom - top))
    s.open(transform=f"translate({256 - k * (left + right) / 2:.1f} {(476 if swim else 466) - k * bottom:.1f}) scale({k:.3f})")
    if swim:
        s.F("path", outline=False, d=f"M40 {cy + ry * 0.35:.0f} C120 {cy + ry * 0.2:.0f} 200 {cy + ry * 0.5:.0f} 280 {cy + ry * 0.35:.0f} C360 {cy + ry * 0.2:.0f} 420 {cy + ry * 0.45:.0f} 480 {cy + ry * 0.35:.0f} V470 H40Z",
            fill="#8FD0FF")
    else:
        for dx in (-0.2, 0.15):
            x = cx + rx * dx
            s.T(f"M{x:.0f} {cy + ry * 0.7:.0f} L{x:.0f} {GROUND - 4}", legs_c, 9)
            s.T(f"M{x - 18:.0f} {GROUND - 2} L{x + 22:.0f} {GROUND - 2} M{x:.0f} {GROUND - 4} L{x + 10:.0f} {GROUND - 14}", legs_c, 7)

    # tail
    tx, ty = cx - rx * 0.9, cy - ry * 0.1
    if tail == "fan":
        s.F("polygon", points=f"{tx + 20:.0f},{ty - 10:.0f} {tx - 70 * size:.0f},{ty - 50 * size:.0f} {tx - 80 * size:.0f},{ty + 30 * size:.0f} {tx + 20:.0f},{ty + 30:.0f}", fill=tail_c)
    elif tail == "long":
        s.F("polygon", points=f"{tx + 20:.0f},{ty:.0f} {tx - 150 * size:.0f},{ty + 50 * size:.0f} {tx - 140 * size:.0f},{ty + 80 * size:.0f} {tx + 20:.0f},{ty + 30:.0f}", fill=tail_c)
    elif tail == "up":
        s.F("polygon", points=f"{tx + 30:.0f},{ty:.0f} {tx - 40 * size:.0f},{ty - 110 * size:.0f} {tx - 70 * size:.0f},{ty - 90 * size:.0f} {tx + 10:.0f},{ty + 30:.0f}", fill=tail_c)
    elif tail == "short":
        s.F("polygon", points=f"{tx + 20:.0f},{ty:.0f} {tx - 40 * size:.0f},{ty + 10 * size:.0f} {tx + 20:.0f},{ty + 30:.0f}", fill=tail_c)

    if neck > 0:
        s.T(f"M{cx + rx * 0.5:.0f} {cy - ry * 0.3:.0f} C{cx + rx * 0.9:.0f} {cy - ry * 0.8:.0f} {hx - hr * 0.6:.0f} {hy + hr * 1.2:.0f} {hx - hr * 0.1:.0f} {hy + hr * 0.3:.0f}", body, hr * 0.9)
    s.F("ellipse", cx=f"{cx:.0f}", cy=f"{cy:.0f}", rx=f"{rx:.0f}", ry=f"{ry:.0f}", fill=body)
    if belly:
        s.F("ellipse", outline=False, cx=f"{cx + rx * 0.2:.0f}", cy=f"{cy + ry * 0.3:.0f}", rx=f"{rx * 0.6:.0f}", ry=f"{ry * 0.55:.0f}", fill=belly)
    s.open("part-wing-left", f"{cx:.0f} {cy - ry * 0.3:.0f}")
    s.F("path", d=f"M{cx + rx * 0.35:.0f} {cy - ry * 0.35:.0f} C{cx - rx * 0.2:.0f} {cy - ry * 0.6:.0f} {cx - rx * 0.9:.0f} {cy - ry * 0.2:.0f} {cx - rx * 0.85:.0f} {cy + ry * 0.35:.0f} "
                  f"C{cx - rx * 0.4:.0f} {cy + ry * 0.45:.0f} {cx + rx * 0.2:.0f} {cy + ry * 0.2:.0f} {cx + rx * 0.35:.0f} {cy - ry * 0.35:.0f}Z", fill=wing)
    s.close()
    if crest:
        s.F("path", d=f"M{hx - hr * 0.3:.0f} {hy - hr * 0.8:.0f} L{hx - hr * 0.6:.0f} {hy - hr * 1.6:.0f} L{hx - hr * 0.1:.0f} {hy - hr * 1.1:.0f} L{hx + hr * 0.1:.0f} {hy - hr * 1.7:.0f} L{hx + hr * 0.3:.0f} {hy - hr * 0.8:.0f}Z", fill=crest)
    if comb:
        for dx in (-0.3, 0.0, 0.3):
            s.F("circle", cx=f"{hx + hr * dx:.0f}", cy=f"{hy - hr * 0.95:.0f}", r=f"{hr * 0.25:.0f}", fill=comb)
    s.F("circle", cx=f"{hx:.0f}", cy=f"{hy:.0f}", r=f"{hr:.0f}", fill=head_c)
    if cheek:
        s.F("circle", outline=False, cx=f"{hx + hr * 0.1:.0f}", cy=f"{hy + hr * 0.25:.0f}", r=f"{hr * 0.35:.0f}", fill=cheek)
    bx, by = hx + hr * 0.9, hy + hr * 0.05
    if beak == "short":
        s.F("polygon", points=f"{bx - 6:.0f},{by - hr * 0.25:.0f} {bx + hr * 0.6:.0f},{by:.0f} {bx - 6:.0f},{by + hr * 0.25:.0f}", fill=beak_c)
    elif beak == "hook":
        s.F("path", d=f"M{bx - 8:.0f} {by - hr * 0.35:.0f} C{bx + hr * 0.6:.0f} {by - hr * 0.4:.0f} {bx + hr * 0.7:.0f} {by + hr * 0.2:.0f} {bx + hr * 0.35:.0f} {by + hr * 0.45:.0f} "
                      f"C{bx + hr * 0.3:.0f} {by + hr * 0.15:.0f} {bx:.0f} {by + hr * 0.25:.0f} {bx - 8:.0f} {by + hr * 0.25:.0f}Z", fill=beak_c)
    elif beak == "long":
        s.F("polygon", points=f"{bx - 6:.0f},{by - hr * 0.18:.0f} {bx + hr * 1.8:.0f},{by + hr * 0.1:.0f} {bx - 6:.0f},{by + hr * 0.2:.0f}", fill=beak_c)
    elif beak == "duck":
        s.F("path", d=f"M{bx - 10:.0f} {by - hr * 0.2:.0f} H{bx + hr * 0.7:.0f} C{bx + hr * 0.95:.0f} {by - hr * 0.2:.0f} {bx + hr * 0.95:.0f} {by + hr * 0.3:.0f} {bx + hr * 0.7:.0f} {by + hr * 0.3:.0f} H{bx - 10:.0f}Z", fill=beak_c)
    elif beak == "big":   # toucan / hornbill
        s.F("path", d=f"M{bx - 10:.0f} {by - hr * 0.5:.0f} C{bx + hr * 1.6:.0f} {by - hr * 0.6:.0f} {bx + hr * 2.0:.0f} {by + hr * 0.2:.0f} {bx + hr * 1.6:.0f} {by + hr * 0.5:.0f} "
                      f"C{bx + hr:.0f} {by + hr * 0.5:.0f} {bx:.0f} {by + hr * 0.4:.0f} {bx - 10:.0f} {by + hr * 0.3:.0f}Z", fill=beak_c)
    elif beak == "pouch":   # pelican
        s.F("path", d=f"M{bx - 10:.0f} {by - hr * 0.15:.0f} H{bx + hr * 1.9:.0f} L{bx + hr * 1.7:.0f} {by + hr * 0.1:.0f} C{bx + hr * 1.2:.0f} {by + hr * 0.9:.0f} {bx + hr * 0.2:.0f} {by + hr * 0.9:.0f} {bx - 10:.0f} {by + hr * 0.3:.0f}Z", fill=beak_c)
    elif beak == "bent":   # flamingo
        s.F("path", d=f"M{bx - 10:.0f} {by - hr * 0.2:.0f} H{bx + hr * 0.6:.0f} L{bx + hr * 0.7:.0f} {by + hr * 0.8:.0f} L{bx + hr * 0.4:.0f} {by + hr * 0.6:.0f} L{bx - 10:.0f} {by + hr * 0.3:.0f}Z", fill=beak_c)
    if wattle:
        s.F("ellipse", cx=f"{bx:.0f}", cy=f"{by + hr * 0.55:.0f}", rx=f"{hr * 0.16:.0f}", ry=f"{hr * 0.3:.0f}", fill=wattle)
    if eye_ring:
        s.F("circle", outline=False, cx=f"{hx + hr * 0.3:.0f}", cy=f"{hy - hr * 0.15:.0f}", r=f"{hr * 0.26:.0f}", fill=eye_ring)
    eye(s, hx + hr * 0.3, hy - hr * 0.15, hr * 0.16)
    s.close()
    return hx, hy


# ---------------------------------------------------------------- fish
def fish(s, body="#F5913E", belly=None, fin=None, length=1.0, height=1.0, tail="fork", stripes=None, stripe_c=WHITE,
         spots=None, dorsal="small", mouth=True, eye_r=None, cx=240, cy=256, teeth=False, sword=False, whisk=False):
    rx, ry = 170 * length, 92 * height
    fin = fin or shade(body, 0.85)
    tx = cx - rx * 0.92
    if tail == "fork":
        s.F("path", d=f"M{tx + 20:.0f} {cy:.0f} L{tx - 80 * length:.0f} {cy - ry * 0.9:.0f} C{tx - 50 * length:.0f} {cy - ry * 0.2:.0f} {tx - 50 * length:.0f} {cy + ry * 0.2:.0f} {tx - 80 * length:.0f} {cy + ry * 0.9:.0f}Z", fill=fin)
    elif tail == "round":
        s.F("ellipse", cx=f"{tx - 30 * length:.0f}", cy=f"{cy:.0f}", rx=f"{55 * length:.0f}", ry=f"{ry * 0.7:.0f}", fill=fin)
    elif tail == "fan":
        s.F("path", d=f"M{tx + 20:.0f} {cy:.0f} L{tx - 80 * length:.0f} {cy - ry * 0.8:.0f} C{tx - 110 * length:.0f} {cy:.0f} {tx - 110 * length:.0f} {cy:.0f} {tx - 80 * length:.0f} {cy + ry * 0.8:.0f}Z", fill=fin)
    elif tail == "crescent":
        s.F("path", d=f"M{tx + 20:.0f} {cy:.0f} C{tx - 20:.0f} {cy - ry * 0.5:.0f} {tx - 60 * length:.0f} {cy - ry * 1.1:.0f} {tx - 90 * length:.0f} {cy - ry * 1.3:.0f} "
                      f"C{tx - 60 * length:.0f} {cy:.0f} {tx - 60 * length:.0f} {cy:.0f} {tx - 90 * length:.0f} {cy + ry * 1.3:.0f} C{tx - 60 * length:.0f} {cy + ry * 1.1:.0f} {tx - 20:.0f} {cy + ry * 0.5:.0f} {tx + 20:.0f} {cy:.0f}Z", fill=fin)
    if dorsal == "small":
        s.F("path", d=f"M{cx - rx * 0.4:.0f} {cy - ry * 0.85:.0f} C{cx - rx * 0.2:.0f} {cy - ry * 1.45:.0f} {cx + rx * 0.15:.0f} {cy - ry * 1.3:.0f} {cx + rx * 0.25:.0f} {cy - ry * 0.85:.0f}Z", fill=fin)
    elif dorsal == "tall":
        s.F("path", d=f"M{cx - rx * 0.5:.0f} {cy - ry * 0.8:.0f} C{cx - rx * 0.3:.0f} {cy - ry * 2.2:.0f} {cx + rx * 0.3:.0f} {cy - ry * 2.0:.0f} {cx + rx * 0.35:.0f} {cy - ry * 0.85:.0f}Z", fill=fin)
    elif dorsal == "shark":
        s.F("polygon", points=f"{cx - rx * 0.25:.0f},{cy - ry * 0.8:.0f} {cx - rx * 0.05:.0f},{cy - ry * 1.9:.0f} {cx + rx * 0.2:.0f},{cy - ry * 0.85:.0f}", fill=fin)
    elif dorsal == "spiky":
        pts = [(cx - rx * 0.6 + k * rx * 0.15, cy - ry * (0.8 if k % 2 == 0 else 1.5)) for k in range(9)]
        s.F("polygon", points=" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill=fin)
    if sword:
        s.F("polygon", points=f"{cx + rx * 0.9:.0f},{cy - 10:.0f} {cx + rx * 0.9 + 170:.0f},{cy:.0f} {cx + rx * 0.9:.0f},{cy + 10:.0f}", fill=shade(body, 0.7))
    s.F("path", d=f"M{cx + rx:.0f} {cy:.0f} C{cx + rx * 0.7:.0f} {cy - ry * 1.15:.0f} {cx - rx * 0.6:.0f} {cy - ry * 1.15:.0f} {cx - rx:.0f} {cy:.0f} "
                  f"C{cx - rx * 0.6:.0f} {cy + ry * 1.15:.0f} {cx + rx * 0.7:.0f} {cy + ry * 1.15:.0f} {cx + rx:.0f} {cy:.0f}Z", fill=body)
    if belly:
        s.F("path", outline=False, d=f"M{cx + rx * 0.85:.0f} {cy + ry * 0.2:.0f} C{cx + rx * 0.5:.0f} {cy + ry * 0.85:.0f} {cx - rx * 0.5:.0f} {cy + ry * 0.85:.0f} {cx - rx * 0.85:.0f} {cy + ry * 0.2:.0f} "
                                     f"C{cx - rx * 0.5:.0f} {cy + ry * 0.45:.0f} {cx + rx * 0.5:.0f} {cy + ry * 0.45:.0f} {cx + rx * 0.85:.0f} {cy + ry * 0.2:.0f}Z", fill=belly)
    if stripes:
        for k in range(stripes):
            x = cx - rx * 0.5 + k * rx * (1.1 / max(1, stripes - 1)) if stripes > 1 else cx
            h = ry * math.sqrt(max(0.0, 1 - ((x - cx) / rx) ** 2)) * 0.95
            s.M(f"M{x:.0f} {cy - h:.0f} C{x + 14:.0f} {cy - h * 0.3:.0f} {x + 14:.0f} {cy + h * 0.3:.0f} {x:.0f} {cy + h:.0f}", stripe_c, 18)
    if spots:
        rnd = random.Random(3)
        for _ in range(12):
            a, d = rnd.uniform(0, 360), rnd.uniform(0, 0.75)
            s.F("circle", outline=False, cx=f"{cx + math.cos(math.radians(a)) * rx * d:.0f}", cy=f"{cy + math.sin(math.radians(a)) * ry * d * 0.8:.0f}", r=8, fill=spots)
    s.F("path", d=f"M{cx + rx * 0.05:.0f} {cy + ry * 0.1:.0f} C{cx - rx * 0.1:.0f} {cy + ry * 0.5:.0f} {cx - rx * 0.2:.0f} {cy + ry * 0.6:.0f} {cx - rx * 0.25:.0f} {cy + ry * 0.55:.0f} "
                  f"C{cx - rx * 0.15:.0f} {cy + ry * 0.3:.0f} {cx - rx * 0.05:.0f} {cy + ry * 0.1:.0f} {cx + rx * 0.05:.0f} {cy + ry * 0.1:.0f}Z", fill=fin)
    s.M(f"M{cx + rx * 0.45:.0f} {cy - ry * 0.7:.0f} C{cx + rx * 0.35:.0f} {cy - ry * 0.2:.0f} {cx + rx * 0.35:.0f} {cy + ry * 0.2:.0f} {cx + rx * 0.45:.0f} {cy + ry * 0.7:.0f}", shade(body, 0.75), 6)
    if mouth:
        s.M(f"M{cx + rx * 0.92:.0f} {cy + ry * 0.12:.0f} q-16 6 -28 -2", INK, 6)
    if teeth:
        s.F("polygon", outline=False, points=f"{cx + rx * 0.7:.0f},{cy + ry * 0.12:.0f} {cx + rx * 0.76:.0f},{cy + ry * 0.3:.0f} {cx + rx * 0.82:.0f},{cy + ry * 0.12:.0f}", fill=WHITE)
    if whisk:
        s.T(f"M{cx + rx * 0.9:.0f} {cy + ry * 0.1:.0f} c40 10 60 40 70 70 M{cx + rx * 0.9:.0f} {cy + ry * 0.2:.0f} c30 20 40 50 40 80", shade(body, 0.6), 6)
    eye(s, cx + rx * 0.66, cy - ry * 0.2, eye_r or ry * 0.16)


# ---------------------------------------------------------------- insects and spiders
def bug(s, body="#3A3A44", head_c=None, wings=None, wing_c="#D9EEFB", legs=6, antennae="thin", spots=None, stripes=None,
        segments=3, length=1.0, cx=256, cy=270, stinger=False, top=True):
    """Top view insect (wings and legs spread). legs=8 for spiders."""
    head_c = head_c or body
    n = legs // 2
    for k in range(n):
        y = cy - 40 + k * (80 / max(1, n - 1))
        for sgn in (1, -1):
            s.T(f"M{cx:.0f} {y:.0f} L{cx + sgn * 90:.0f} {y - 30 + k * 20:.0f} L{cx + sgn * 120:.0f} {y + 30 + k * 10:.0f}", body, 9)
    if wings == "clear":
        for sgn in (1, -1):
            s.F("ellipse", cx=f"{cx + sgn * 70:.0f}", cy=f"{cy - 30:.0f}", rx=90, ry=40, fill=wing_c, fill_opacity="0.85", transform=f"rotate({sgn * -25} {cx + sgn * 70:.0f} {cy - 30:.0f})")
    elif wings == "dragonfly":
        for sgn in (1, -1):
            for dy in (-40, 20):
                s.F("ellipse", cx=f"{cx + sgn * 110:.0f}", cy=f"{cy + dy:.0f}", rx=110, ry=26, fill=wing_c, fill_opacity="0.85")
    if segments >= 3:
        s.F("ellipse", cx=f"{cx:.0f}", cy=f"{cy + 80 * length:.0f}", rx=f"{58 * length:.0f}", ry=f"{90 * length:.0f}", fill=body)
        if stripes:
            for k in range(3):
                yy = cy + 50 * length + k * 36 * length
                s.F("rect", outline=False, x=f"{cx - 52 * length:.0f}", y=f"{yy:.0f}", width=f"{104 * length:.0f}", height=f"{16 * length:.0f}", rx=6, fill=stripes)
        if stinger:
            s.F("polygon", points=f"{cx - 10:.0f},{cy + 165 * length:.0f} {cx + 10:.0f},{cy + 165 * length:.0f} {cx:.0f},{cy + 200 * length:.0f}", fill=C["black"])
    s.F("ellipse", cx=f"{cx:.0f}", cy=f"{cy - 10:.0f}", rx=f"{50 * length:.0f}", ry=f"{55 * length:.0f}", fill=body)
    if wings == "beetle":
        s.F("path", d=f"M{cx:.0f} {cy - 40:.0f} C{cx - 120:.0f} {cy - 30:.0f} {cx - 110:.0f} {cy + 160:.0f} {cx:.0f} {cy + 170:.0f} C{cx + 110:.0f} {cy + 160:.0f} {cx + 120:.0f} {cy - 30:.0f} {cx:.0f} {cy - 40:.0f}Z", fill=wing_c)
        s.M(f"M{cx:.0f} {cy - 40:.0f} V{cy + 170:.0f}", INK, 6)
        if spots:
            for x, y in ((-50, 30), (50, 30), (-40, 100), (40, 100), (0, 60)):
                s.F("circle", outline=False, cx=f"{cx + x:.0f}", cy=f"{cy + y:.0f}", r=18, fill=spots)
    s.F("circle", cx=f"{cx:.0f}", cy=f"{cy - 80 * length:.0f}", r=f"{38 * length:.0f}", fill=head_c)
    if antennae == "thin":
        s.T(f"M{cx - 14:.0f} {cy - 110 * length:.0f} C{cx - 30:.0f} {cy - 160:.0f} {cx - 60:.0f} {cy - 180:.0f} {cx - 80:.0f} {cy - 190:.0f} "
            f"M{cx + 14:.0f} {cy - 110 * length:.0f} C{cx + 30:.0f} {cy - 160:.0f} {cx + 60:.0f} {cy - 180:.0f} {cx + 80:.0f} {cy - 190:.0f}", body, 6)
    for sgn in (1, -1):
        s.F("circle", outline=False, cx=f"{cx + sgn * 18 * length:.0f}", cy=f"{cy - 88 * length:.0f}", r=f"{9 * length:.0f}", fill=WHITE)
        s.F("circle", outline=False, cx=f"{cx + sgn * 18 * length:.0f}", cy=f"{cy - 88 * length:.0f}", r=f"{5 * length:.0f}", fill=BLACK)


def butterfly_wings(s, c1, c2, spots=WHITE, cx=256, cy=256, body=C["black"]):
    s.open("part-wing-left", f"{cx} {cy}")
    s.F("path", d=f"M{cx - 6} {cy - 6} C{cx - 60} {cy - 170} {cx - 200} {cy - 170} {cx - 190} {cy - 60} C{cx - 180} {cy} {cx - 100} {cy + 10} {cx - 6} {cy}Z", fill=c1)
    s.F("path", d=f"M{cx - 6} {cy + 10} C{cx - 110} {cy + 20} {cx - 160} {cy + 70} {cx - 130} {cy + 130} C{cx - 100} {cy + 170} {cx - 30} {cy + 120} {cx - 6} {cy + 20}Z", fill=c2)
    s.close()
    s.open("part-wing-right", f"{cx} {cy}")
    s.F("path", d=f"M{cx + 6} {cy - 6} C{cx + 60} {cy - 170} {cx + 200} {cy - 170} {cx + 190} {cy - 60} C{cx + 180} {cy} {cx + 100} {cy + 10} {cx + 6} {cy}Z", fill=c1)
    s.F("path", d=f"M{cx + 6} {cy + 10} C{cx + 110} {cy + 20} {cx + 160} {cy + 70} {cx + 130} {cy + 130} C{cx + 100} {cy + 170} {cx + 30} {cy + 120} {cx + 6} {cy + 20}Z", fill=c2)
    s.close()
    if spots:
        for x, y, r in ((-130, -80, 16), (130, -80, 16), (-90, 90, 12), (90, 90, 12)):
            s.F("circle", outline=False, cx=cx + x, cy=cy + y, r=r, fill=spots)
    s.F("ellipse", cx=cx, cy=cy + 20, rx=14, ry=110, fill=body)
    s.F("circle", cx=cx, cy=cy - 100, r=20, fill=body)
    s.T(f"M{cx - 8} {cy - 116} C{cx - 30} {cy - 160} {cx - 50} {cy - 170} {cx - 60} {cy - 176} M{cx + 8} {cy - 116} C{cx + 30} {cy - 160} {cx + 50} {cy - 170} {cx + 60} {cy - 176}", body, 6)


# ---------------------------------------------------------------- reptiles
def snake(s, body="#4CB963", belly=None, pattern=None, hood=False, cx=256):
    s.T("M80 400 C160 470 240 380 200 320 C160 260 240 200 320 240 C380 270 400 220 380 170", body, 52)
    if pattern:
        for t in (0.12, 0.3, 0.48, 0.66):
            pass
        s.M("M80 400 C160 470 240 380 200 320 C160 260 240 200 320 240 C380 270 400 220 380 170", pattern, 14, dash="20 24")
    if hood:
        s.F("ellipse", cx=380, cy=150, rx=60, ry=80, fill=body)
        if belly:
            s.F("ellipse", outline=False, cx=380, cy=160, rx=30, ry=50, fill=belly)
    s.F("ellipse", cx=390, cy=140, rx=48, ry=36, fill=body, transform="rotate(-20 390 140)")
    eye(s, 404, 126, 7)
    s.M("M436 150 l24 6 m-24 -6 l22 12", C["red"], 4)


def lizard(s, body="#4CB963", belly=None, crest=False, spots=None, long_tail=True, frill=None):
    s.T("M120 340 C60 360 40 420 80 440", body, 28)
    for x, dy in ((170, 1), (330, 1)):
        s.T(f"M{x} 330 L{x - 30} 400 L{x - 50} 410 M{x} 330 L{x + 30} 400 L{x + 50} 410", shade(body, 0.85), 16)
    s.F("ellipse", cx=250, cy=320, rx=150, ry=50, fill=body)
    if belly:
        s.F("ellipse", outline=False, cx=250, cy=340, rx=120, ry=22, fill=belly)
    if spots:
        for x in (190, 240, 290, 340):
            s.F("circle", outline=False, cx=x, cy=305, r=12, fill=spots)
    if crest:
        s.F("polygon", points=" ".join(f"{x},{280 if k % 2 == 0 else 250}" for k, x in enumerate(range(130, 380, 25))), fill=shade(body, 0.8))
    if frill:
        s.F("circle", cx=400, cy=300, r=70, fill=frill)
    s.F("ellipse", cx=420, cy=300, rx=62, ry=38, fill=body)
    eye(s, 430, 290, 8)


def turtle(s, shell="#6E8B3D", skin="#9BC46B", sea=False):
    for x in (150, 350):
        s.F("ellipse", cx=x, cy=380 if not sea else 330, rx=50 if not sea else 80, ry=26 if not sea else 24, fill=skin, transform=f"rotate({20 if x > 256 else -20} {x} 380)")
    s.F("ellipse", cx=420, cy=320, rx=50, ry=36, fill=skin)
    s.F("path", d="M100 360 C100 200 400 200 400 360Z", fill=shell)
    for x, y in ((180, 300), (250, 270), (320, 300), (250, 330)):
        s.F("polygon", outline=False, points=" ".join(f"{a:.0f},{b:.0f}" for a, b in (arc_pt(x, y, 28, k * 60) for k in range(6))), fill=shade(shell, 0.8))
    s.F("rect", x=96, y=350, width=308, height=26, rx=12, fill=shade(shell, 0.75))
    eye(s, 432, 310, 7)


# ---------------------------------------------------------------- upright and special mammals
def primate(s, body="#8C6239", face="#E8C39E", belly=None, tail=None, tail_c=None, arms_long=False, crest=None, nose=None, big_nose=None):
    """Sitting primate, front view."""
    tail_c = tail_c or body
    if tail == "curl":
        s.T("M330 420 C420 430 450 360 420 320 C400 300 380 320 396 340", tail_c, 18)
    elif tail == "long":
        s.T("M330 420 C430 440 470 380 460 300 C455 260 430 240 410 250", tail_c, 18)
    elif tail == "ringed":
        s.T("M330 420 C430 440 470 380 460 300 C455 260 430 240 410 250", tail_c, 22)
        s.M("M360 432 l8 -20 M400 428 l12 -18 M436 410 l16 -12 M456 370 l20 -4 M462 330 l20 4", WHITE, 8)
    s.F("ellipse", cx=256, cy=360, rx=110, ry=100, fill=body)
    if belly:
        s.F("ellipse", outline=False, cx=256, cy=375, rx=66, ry=70, fill=belly)
    arm_end = 440 if arms_long else 410
    for sgn in (1, -1):
        s.T(f"M{256 + sgn * 90} 300 C{256 + sgn * 120} 350 {256 + sgn * 110} 400 {256 + sgn * 70} {arm_end}", body, 34)
        s.F("ellipse", cx=256 + sgn * 70, cy=arm_end, rx=24, ry=16, fill=face)
        s.F("ellipse", cx=256 + sgn * 60, cy=446, rx=40, ry=18, fill=face)
    if crest:
        s.F("ellipse", cx=256, cy=110, rx=60, ry=40, fill=crest)
    for sgn in (1, -1):
        s.F("circle", cx=256 + sgn * 92, cy=190, r=30, fill=face)
    s.F("circle", cx=256, cy=180, r=96, fill=body)
    s.F("path", d="M186 190 C186 140 236 136 256 156 C276 136 326 140 326 190 C326 250 290 272 256 272 C222 272 186 250 186 190Z", fill=face)
    if big_nose:
        s.F("ellipse", cx=256, cy=235, rx=34, ry=42, fill=big_nose)
    eye(s, 226, 188, 11, "left")
    eye(s, 286, 188, 11, "right")
    s.F("ellipse", outline=False, cx=256, cy=222, rx=14, ry=8, fill=nose or shade(face, 0.6))
    s.M("M236 246 Q256 258 276 246", INK, 5)


def kangaroo(s, body="#C68A5C", belly="#E8C39E", joey=False):
    """Standing kangaroo: big hind leg and foot, thick tail as a prop, upright body, neck, long head."""
    dark = shade(body, 0.8)
    sil = _Sil()
    sil.add("path", d="M190 360 C140 380 90 410 46 438 C80 446 140 430 210 400 Z", fill=body)          # tail
    sil.add("path", d="M180 380 C170 300 190 200 250 170 C290 150 320 170 320 210 C322 260 300 330 290 390 C270 420 200 430 180 380 Z", fill=body)  # body
    sil.add("ellipse", cx=225, cy=380, rx=72, ry=50, fill=body)                                        # haunch
    sil.add("path", d="M250 410 L350 430 C366 434 366 448 350 448 L232 444 Z", fill=body)               # foot
    sil.add("path", d="M262 190 C268 150 284 120 300 104 L332 128 C320 150 312 178 314 210 Z", fill=body)   # neck
    sil.add("path", d=_capsule(318, 112, 34, 372, 132, 17), fill=body)                                  # head
    sil.draw(s)
    s.F("path", outline=False, d="M240 230 C270 220 296 250 296 300 C296 350 280 390 250 396 C228 360 226 280 240 230 Z", fill=belly)
    s.T("M290 230 C310 250 320 270 322 290", body, 18)        # near arm
    s.F("ellipse", cx=300, cy=76, rx=12, ry=34, fill=body, transform="rotate(-14 300 76)")
    s.F("ellipse", cx=322, cy=78, rx=12, ry=34, fill=body, transform="rotate(8 322 78)")
    s.F("ellipse", outline=False, cx=384, cy=126, rx=8, ry=6, fill=BLACK)
    s.M("M226 360 C240 380 260 392 280 396", dark, 5)
    eye(s, 336, 106, 8)
    if joey:
        s.F("circle", cx=272, cy=268, r=24, fill=body)
        s.F("ellipse", cx=262, cy=244, rx=7, ry=16, fill=body)
        eye(s, 280, 264, 5)


def cetacean(s, body="#5A7CA8", belly="#D9E2EC", length=1.0, height=1.0, dorsal=True, spout=False, tusk=False, beak=False, flipper_long=False, cx=250, cy=270):
    rx, ry = 200 * length, 80 * height
    tx = cx - rx
    s.F("path", d=f"M{tx + 30:.0f} {cy - 5:.0f} C{tx - 20:.0f} {cy - 30:.0f} {tx - 50:.0f} {cy - 90:.0f} {tx - 70:.0f} {cy - 110:.0f} C{tx - 20:.0f} {cy - 100:.0f} {tx:.0f} {cy - 60:.0f} {tx + 10:.0f} {cy - 20:.0f} "
                  f"C{tx:.0f} {cy + 20:.0f} {tx - 30:.0f} {cy + 60:.0f} {tx - 70:.0f} {cy + 80:.0f} C{tx - 30:.0f} {cy + 80:.0f} {tx + 10:.0f} {cy + 50:.0f} {tx + 30:.0f} {cy + 10:.0f}Z", fill=body)
    if dorsal:
        s.F("path", d=f"M{cx - rx * 0.1:.0f} {cy - ry * 0.85:.0f} C{cx - rx * 0.05:.0f} {cy - ry * 1.7:.0f} {cx - rx * 0.2:.0f} {cy - ry * 1.6:.0f} {cx - rx * 0.3:.0f} {cy - ry * 0.75:.0f}Z", fill=body)
    nose_x = cx + rx * (1.15 if beak else 1.0)
    s.F("path", d=f"M{tx + 20:.0f} {cy:.0f} C{tx + 60:.0f} {cy - ry * 1.1:.0f} {cx + rx * 0.6:.0f} {cy - ry * 1.3:.0f} {cx + rx * 0.9:.0f} {cy - ry * 0.4:.0f} "
                  f"C{nose_x:.0f} {cy - ry * 0.1:.0f} {nose_x:.0f} {cy + ry * 0.2:.0f} {cx + rx * 0.85:.0f} {cy + ry * 0.4:.0f} C{cx + rx * 0.4:.0f} {cy + ry * 1.0:.0f} {tx + 80:.0f} {cy + ry * 0.6:.0f} {tx + 20:.0f} {cy:.0f}Z", fill=body)
    s.F("path", outline=False, d=f"M{cx + rx * 0.85:.0f} {cy + ry * 0.4:.0f} C{cx + rx * 0.4:.0f} {cy + ry * 0.95:.0f} {tx + 100:.0f} {cy + ry * 0.55:.0f} {tx + 60:.0f} {cy + ry * 0.2:.0f} "
                                 f"C{tx + 150:.0f} {cy + ry * 0.45:.0f} {cx + rx * 0.5:.0f} {cy + ry * 0.4:.0f} {cx + rx * 0.85:.0f} {cy + ry * 0.15:.0f}Z", fill=belly)
    fl = 1.8 if flipper_long else 1.0
    s.F("path", d=f"M{cx + rx * 0.35:.0f} {cy + ry * 0.4:.0f} C{cx + rx * 0.3:.0f} {cy + ry * (0.9 + fl * 0.4):.0f} {cx + rx * 0.15:.0f} {cy + ry * (1.0 + fl * 0.5):.0f} {cx + rx * 0.05:.0f} {cy + ry * (1.0 + fl * 0.5):.0f} "
                  f"C{cx + rx * 0.12:.0f} {cy + ry * 0.8:.0f} {cx + rx * 0.2:.0f} {cy + ry * 0.5:.0f} {cx + rx * 0.35:.0f} {cy + ry * 0.4:.0f}Z", fill=shade(body, 0.85))
    if spout:
        s.M(f"M{cx + rx * 0.55:.0f} {cy - ry * 1.1:.0f} C{cx + rx * 0.5:.0f} {cy - ry * 1.8:.0f} {cx + rx * 0.4:.0f} {cy - ry * 2.1:.0f} {cx + rx * 0.3:.0f} {cy - ry * 2.2:.0f} "
            f"M{cx + rx * 0.55:.0f} {cy - ry * 1.1:.0f} C{cx + rx * 0.6:.0f} {cy - ry * 1.8:.0f} {cx + rx * 0.7:.0f} {cy - ry * 2.1:.0f} {cx + rx * 0.8:.0f} {cy - ry * 2.2:.0f}", "#8FD0FF", 12)
    if tusk:
        s.T(f"M{nose_x:.0f} {cy:.0f} L{nose_x + 110:.0f} {cy - 40:.0f}", "#FFF8E7", 12)
    s.M(f"M{cx + rx * 0.9:.0f} {cy + ry * 0.2:.0f} q-30 10 -60 0", INK, 5)
    eye(s, cx + rx * 0.62, cy - ry * 0.05, 9)


def seal(s, body="#8C96A3", belly=None, tusks=False, whiskers=True, sea_lion=False):
    s.F("path", d="M60 400 C40 380 60 350 90 360 C160 380 200 300 260 270 C300 250 330 200 340 160 C360 120 430 120 440 170 C450 220 420 260 400 300 "
                  "C380 360 340 410 260 420 C200 428 140 420 60 400Z", fill=body)
    if belly:
        s.F("path", outline=False, d="M240 410 C320 400 370 360 390 300 C360 340 320 380 240 410Z", fill=belly)
    s.F("ellipse", cx=330 if sea_lion else 320, cy=400, rx=50, ry=18, fill=shade(body, 0.8), transform="rotate(20 320 400)")
    s.F("ellipse", cx=460, cy=180, rx=24, ry=18, fill=tint(body, 0.2))
    s.F("ellipse", outline=False, cx=474, cy=172, rx=8, ry=6, fill=BLACK)
    if whiskers:
        s.M("M470 186 l30 6 M468 194 l28 14", INK, 3)
    if tusks:
        s.T("M450 196 L440 290 M470 196 L466 290", "#FFF8E7", 12)
    eye(s, 420, 160, 10)


def bat(s, body="#4A3B32", wing="#6E5A4A"):
    s.open("part-wing-left", "256 240")
    s.F("path", d="M240 220 C180 140 100 140 40 180 C60 220 70 260 60 300 C100 280 130 290 150 320 C170 290 200 280 240 280Z", fill=wing)
    s.close()
    s.open("part-wing-right", "256 240")
    s.F("path", d="M272 220 C332 140 412 140 472 180 C452 220 442 260 452 300 C412 280 382 290 362 320 C342 290 312 280 272 280Z", fill=wing)
    s.close()
    s.F("ellipse", cx=256, cy=270, rx=50, ry=70, fill=body)
    s.F("polygon", points="216,190 226,140 246,186", fill=body)
    s.F("polygon", points="296,190 286,140 266,186", fill=body)
    s.F("circle", cx=256, cy=210, r=44, fill=body)
    eye(s, 238, 206, 8, "left")
    eye(s, 274, 206, 8, "right")
    s.F("polygon", outline=False, points="246,232 252,246 258,232", fill=WHITE)
    s.F("polygon", outline=False, points="256,232 262,246 268,232", fill=WHITE)


def round_critter(s, body="#E8B878", belly="#FFF3DF", ears="round", tail=None, quills=None, nose=None, whiskers=True):
    """Small round animal (hamster, mouse, hedgehog...), side view."""
    nose = nose or C["pink"]
    if tail == "thin":
        s.T("M120 380 C70 380 50 330 70 300", C["pink"], 8)
    elif tail == "bushy":
        s.F("path", d="M140 360 C40 360 40 200 120 180 C110 260 150 320 180 340Z", fill=body)
    if quills:
        s.F("polygon", points=" ".join(f"{x:.0f},{y:.0f}" for x, y in (arc_pt(240, 320, 150 if k % 2 == 0 else 110, 180 + k * 9) for k in range(21))), fill=quills)
    s.F("ellipse", cx=250, cy=340, rx=140, ry=100, fill=body if not quills else tint(quills, 0.4))
    s.F("ellipse", outline=False, cx=300, cy=370, rx=80, ry=55, fill=belly)
    if ears == "round":
        s.F("circle", cx=300, cy=240, r=34, fill=body)
        s.F("circle", outline=False, cx=300, cy=240, r=18, fill=C["pink"])
    elif ears == "big":
        s.F("circle", cx=290, cy=220, r=56, fill=body)
        s.F("circle", outline=False, cx=290, cy=220, r=34, fill=C["pink"])
    for x in (200, 300):
        s.F("ellipse", cx=x, cy=438, rx=26, ry=12, fill=C["pink"])
    s.F("circle", outline=False, cx=388, cy=330, r=12, fill=nose)
    if whiskers:
        s.M("M380 336 l50 -8 M380 344 l48 10", INK, 3)
    eye(s, 350, 300, 12)
