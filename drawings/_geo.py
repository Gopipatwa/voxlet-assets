"""Map outlines from Natural Earth (public domain) for earth-geography.

Data: _source-data/naturalearth/*.geojson (not in git; see README).
Projection: equirectangular with cos(latitude) correction, fitted to the 512 frame.
Shapes are simplified (Douglas-Peucker) so each SVG stays small.
"""
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "_source-data" / "naturalearth"
_cache = {}


def load(name):
    if name not in _cache:
        _cache[name] = json.loads((DATA / f"{name}.geojson").read_text(encoding="utf-8"))["features"]
    return _cache[name]


def rings_of(feature):
    g = feature["geometry"]
    if g["type"] == "Polygon":
        return [g["coordinates"][0]]
    return [poly[0] for poly in g["coordinates"]]


def ring_area(r):
    return abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2


def unwrap(rings):
    """Shift longitudes so shapes crossing the antimeridian stay together."""
    lons = [p[0] for r in rings for p in r]
    if max(lons) - min(lons) > 180:
        rings = [[[(x + 360) if x < 0 else x, y] for x, y in r] for r in rings]
    return rings


def dp(points, eps):
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-9
    best, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        x0, y0 = points[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > best:
            best, idx = d, i
    if best > eps:
        return dp(points[:idx + 1], eps)[:-1] + dp(points[idx:], eps)
    return [points[0], points[-1]]


def simplify_ring(pts, eps):
    """Douglas-Peucker for a closed ring: split at the point farthest from the start first."""
    if len(pts) < 4:
        return pts
    if tuple(pts[0]) != tuple(pts[-1]):     # clipped rings and boxes come unclosed: close them
        pts = list(pts) + [pts[0]]
    x0, y0 = pts[0]
    far = max(range(len(pts)), key=lambda i: (pts[i][0] - x0) ** 2 + (pts[i][1] - y0) ** 2)
    a = dp(pts[:far + 1], eps)
    b = dp(pts[far:], eps)
    return a[:-1] + b[:-1]


class Frame:
    """Maps lon/lat rings into a box (x0, y0, x1, y1) on the 512 canvas."""

    def __init__(self, rings, box=(40, 40, 472, 472), wrap=True):
        rings = unwrap(rings) if wrap else rings
        lat_mid = sum(p[1] for r in rings for p in r) / max(1, sum(len(r) for r in rings))
        self.k = math.cos(math.radians(max(-70, min(70, lat_mid))))
        xs = [p[0] * self.k for r in rings for p in r]
        ys = [-p[1] for r in rings for p in r]
        self.minx, self.maxx, self.miny, self.maxy = min(xs), max(xs), min(ys), max(ys)
        bw, bh = box[2] - box[0], box[3] - box[1]
        w, h = (self.maxx - self.minx) or 1e-6, (self.maxy - self.miny) or 1e-6
        self.s = min(bw / w, bh / h)
        self.ox = box[0] + (bw - w * self.s) / 2
        self.oy = box[1] + (bh - h * self.s) / 2
        self.wrap = wrap and max(p[0] for r in rings for p in r) > 180

    def pt(self, lon, lat):
        if self.wrap and lon < 0:
            lon += 360
        return ((lon * self.k - self.minx) * self.s + self.ox, (-lat - self.miny) * self.s + self.oy)

    def path(self, rings, eps=1.2, min_area=6.0):
        out = []
        for r in rings:
            pts = [self.pt(x, y) for x, y in r]
            if ring_area(pts) < min_area:
                continue
            simple = simplify_ring(pts, eps)
            if len(simple) >= 3:
                pts = simple
            elif len(pts) > 12:
                pts = pts[:: max(1, len(pts) // 8)]
            if len(pts) < 3:
                continue
            out.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        return " ".join(out)


def clip_poly(pts, x0, y0, x1, y1):
    """Sutherland-Hodgman clip of a polygon to a rectangle (projected coordinates)."""
    def clip(points, inside, inter):
        out = []
        for i, p in enumerate(points):
            q = points[i - 1]
            if inside(p):
                if not inside(q):
                    out.append(inter(q, p))
                out.append(p)
            elif inside(q):
                out.append(inter(q, p))
        return out

    def ix(xv):
        return lambda a, b: (xv, a[1] + (b[1] - a[1]) * (xv - a[0]) / ((b[0] - a[0]) or 1e-9))

    def iy(yv):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yv - a[1]) / ((b[1] - a[1]) or 1e-9), yv)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)),
                          (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        pts = clip(pts, inside, inter)
        if not pts:
            return []
    return pts


class Region:
    """A lon/lat window drawn into a box, with clipping, for region maps."""

    def __init__(self, lon0, lon1, lat0, lat1, box=(24, 24, 488, 488)):
        self.wrap = lon1 > 180
        self.box = box
        self.frame = Frame([[[lon0, lat1], [lon1, lat1], [lon1, lat0], [lon0, lat0]]], box, wrap=False)
        self.frame.wrap = self.wrap

    def poly(self, rings, eps=1.0, min_area=2.0):
        b = self.box
        out = []
        for r in rings:
            lons = [p[0] for p in r]
            if max(lons) - min(lons) > 180:        # ring crosses the date line: make it continuous
                r = [[x + 360 if x < 0 else x, y] for x, y in r]
            pts = [self.frame.pt(x, y) if x <= 180 else self._pt_raw(x, y) for x, y in r]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            if max(xs) < b[0] or min(xs) > b[2] or max(ys) < b[1] or min(ys) > b[3]:
                continue
            pts = clip_poly(pts, b[0], b[1], b[2], b[3])
            if len(pts) < 3 or ring_area(pts) < min_area:
                continue
            s = simplify_ring(pts, eps)
            pts = s if len(s) >= 3 else pts
            out.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        return " ".join(out)

    def _pt_raw(self, lon, lat):
        f = self.frame
        return ((lon * f.k - f.minx) * f.s + f.ox, (-lat - f.miny) * f.s + f.oy)

    def line(self, coords, eps=0.8):
        pts = [self.frame.pt(x, y) for x, y in coords]
        b = self.box
        pts = [p for p in pts if b[0] - 40 <= p[0] <= b[2] + 40 and b[1] - 40 <= p[1] <= b[3] + 40]
        if len(pts) < 2:
            return ""
        pts = dp(pts, eps)
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def find(features, key_names, names):
    want = {n.lower() for n in names}
    return [f for f in features if any(str(f["properties"].get(k, "")).lower() in want for k in key_names)]


def main_rings(rings, keep=0.02):
    """Drop tiny islands far smaller than the main landmass (keeps island nations intact)."""
    areas = [ring_area(r) for r in rings]
    big = max(areas) if areas else 0
    kept = [r for r, a in zip(rings, areas) if a >= big * keep]
    return kept or rings
