"""earth-geography drawings. Run: python drawings/earth_geography.py [ids...]

Countries, continents, the world map and state maps come from Natural Earth outlines (public
domain), via _geo.py. India uses Natural Earth's India point-of-view shape (official borders).
Everything else in this category is hand-drawn below.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _geo import Frame, load, main_rings, ring_area, rings_of, unwrap  # noqa: E402
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID  # noqa: E402
from check_catalog import slug  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
D = {}
LAND, LAND_HI, SEA = A1, A2, A1L


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def centroid(r):
    return sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r)


def filter_far(rings, max_deg=22):
    """Keep the main landmass and pieces near it (drops far-away overseas territories)."""
    if not rings:
        return rings
    main = max(rings, key=ring_area)
    mx, my = centroid(main)
    big = ring_area(main)
    out = []
    for r in rings:
        x, y = centroid(r)
        d = math.hypot((x - mx) * math.cos(math.radians(my)), y - my)
        if d <= max_deg or ring_area(r) > big * 0.3:
            out.append(r)
    return out


def merged(s, d, fill):
    """Outline drawn once underneath, fill on top: shared borders inside a shape stay hidden."""
    s.F("path", d=d, fill=fill)
    s.F("path", outline=False, d=d, fill=fill)


def draw_shape(s, rings, fill=LAND, eps=1.0, merge=False):
    f = Frame(rings)
    areas = [ring_area([f.pt(x, y) for x, y in r]) for r in rings]
    if sum(areas) < 2500:   # scattered atolls: show each island as a visible dot
        for r in rings:
            pts = [f.pt(x, y) for x, y in r]
            cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
            s.F("circle", cx=f"{cx:.0f}", cy=f"{cy:.0f}", r=16, fill=fill)
        return f
    d = f.path(rings, eps=eps, min_area=4.0)
    if merge:
        merged(s, d, fill)
    else:
        s.F("path", d=d, fill=fill, fill_rule="evenodd")
    return f


# ---------------------------------------------------------------- countries
NE = None
NE_IND = None


def countries():
    global NE, NE_IND
    if NE is None:
        NE = load("ne_50m_admin_0_countries")
        NE_IND = load("ne_10m_admin_0_countries_ind")
    return NE


def country_rings(names):
    feats = countries()
    want = {slug(n) for n in names}
    chosen = [f for f in feats if any(slug(str(f["properties"].get(k, ""))) in want for k in ("NAME", "NAME_LONG", "ADMIN", "NAME_EN", "FORMAL_EN"))]
    if not chosen:
        raise KeyError(names)
    # pick the single best match (exact NAME first)
    exact = [f for f in chosen if slug(f["properties"]["NAME"]) in want]
    f = (exact or chosen)[0]
    rings = rings_of(f)
    name = f["properties"]["NAME"]
    extra = {"Somalia": "Somaliland", "Cyprus": "N. Cyprus"}.get(name)
    if extra:
        for g in feats:
            if g["properties"]["NAME"] == extra:
                rings += rings_of(g)
    return rings


def india_rings():
    countries()
    f = next(f for f in NE_IND if f["properties"].get("NAME") == "India" or f["properties"].get("ADMIN") == "India")
    return rings_of(f)


SPECIAL = {"turkiye": ["Turkey"], "india": None}


def country_drawing(item_id, names):
    def fn(s):
        rings = india_rings() if item_id == "india" else country_rings(SPECIAL.get(item_id) or names)
        rings = filter_far(main_rings(rings, 0.004))
        draw_shape(s, rings)
    return fn


CAT = json.loads((ROOT / "catalog" / "earth-geography.json").read_text(encoding="utf-8"))
for g in CAT["groups"]:
    if g["id"].startswith("countries-"):
        for it in g["items"]:
            nm = it["name"] if isinstance(it, dict) else (it if isinstance(it, str) else it[0])
            iid = it["id"] if isinstance(it, dict) else slug(nm)
            alts = [] if isinstance(it, (str, dict)) else it[1:]
            D[iid] = country_drawing(iid, [nm] + alts)


# ---------------------------------------------------------------- continents and world
WINDOWS = {
    "africa": ("Africa", (-20, 55, -36, 38)),
    "asia": ("Asia", (25, 180, -11, 80)),
    "europe": ("Europe", (-25, 60, 34, 72)),
    "north-america": ("North America", (-170, -50, 7, 84)),
    "south-america": ("South America", (-82, -34, -56, 13)),
    "oceania": ("Oceania", (110, 180, -48, 0)),
    "antarctica": ("Antarctica", (-180, 180, -90, -60)),
}


def continent_rings(key):
    cont, (x0, x1, y0, y1) = WINDOWS[key]
    out = []
    for f in countries():
        p = f["properties"]
        rings = rings_of(f)
        if p.get("CONTINENT") == cont or (key == "asia" and p["NAME"] == "Russia"):
            for r in rings:
                cx, cy = centroid(r)
                if x0 <= cx <= x1 and y0 <= cy <= y1:
                    out.append(r)
    if key == "europe":
        out = [r for r in out if centroid(r)[0] < 60]
    return out


def polar_south(s, rings, fill=LAND, eps=1.4):
    """Antarctica seen from above the South Pole (a flat map stretches it into a strip)."""
    from _geo import simplify_ring
    proj = [[(256 + (90 + y) * 7.0 * math.sin(math.radians(x)), 256 - (90 + y) * 7.0 * math.cos(math.radians(x))) for x, y in r] for r in rings]
    xs = [p[0] for r in proj for p in r]
    ys = [p[1] for r in proj for p in r]
    k = min(420 / (max(xs) - min(xs)), 420 / (max(ys) - min(ys)))
    ox, oy = 256 - (max(xs) + min(xs)) / 2 * k, 256 - (max(ys) + min(ys)) / 2 * k
    out = []
    for r in proj:
        pts = simplify_ring([(x * k + ox, y * k + oy) for x, y in r], eps)
        if len(pts) >= 3 and ring_area(pts) >= 6:
            out.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
    merged(s, " ".join(out), fill)


for _k in WINDOWS:
    D[_k] = (lambda k: lambda s: draw_shape(s, continent_rings(k), eps=1.8, merge=True))(_k)
D["antarctica"] = lambda s: polar_south(s, continent_rings("antarctica"), fill="#E9F3FB")

CONT_COLORS = {"africa": "#F5913E", "asia": "#E5484D", "europe": "#3D8BFD", "north-america": "#4CB963", "south-america": "#FFC83D", "oceania": "#8B5CF6", "antarctica": "#C9CED6"}


def world(s, colors=None, box=(30, 110, 482, 402)):
    allr = [r for k in WINDOWS for r in continent_rings(k) if k != "antarctica"]
    f = Frame([[[-180, 75], [180, 75], [180, -58], [-180, -58]]], box, wrap=False)
    for k in WINDOWS:
        if k == "antarctica":
            continue
        rings = continent_rings(k)
        merged(s, f.path(rings, eps=3.0, min_area=16.0), (colors or {}).get(k, LAND))
    return allr


D["seven-continents"] = lambda s: world(s, CONT_COLORS)
D["world-map"] = lambda s: (s.F("rect", x=24, y=96, width=464, height=320, rx=24, fill=SEA), world(s))


# ---------------------------------------------------------------- Indian states and US states
ADM1 = None


def adm1(admin):
    global ADM1
    if ADM1 is None:
        ADM1 = load("ne_50m_admin_1_states_provinces")
    return {f["properties"]["name"]: rings_of(f) for f in ADM1 if f["properties"]["admin"] == admin}


IN_NAMES = {"andaman-and-nicobar-ut": "Andaman and Nicobar", "chandigarh-ut": "Chandigarh", "delhi-ut": "Delhi", "puducherry-ut": "Puducherry",
            "dadra-and-nagar-haveli-and-daman-and-diu": "Dadra and Nagar Haveli and Daman and Diu", "odisha": "Odisha"}


def highlight_map(s, base_rings, parts, hi_name, frame=None, all_states=False):
    f = frame or Frame(base_rings)
    s.F("path", d=f.path(base_rings, eps=1.6, min_area=6.0), fill=LIGHT, fill_rule="evenodd")
    if all_states:
        cols = (A1, A1L, A2L, "#9BD7A8", "#C8B8F0")
        for i, (nm, rings) in enumerate(sorted(parts.items())):
            s.F("path", d=f.path(rings, eps=1.8, min_area=2.0), fill=cols[i % len(cols)])
        return
    for nm, rings in parts.items():
        s.raw(f'<path d="{f.path(rings, eps=2.2, min_area=4.0)}" fill="none" stroke="{MID}" stroke-width="3"/>')
    rings = parts[hi_name]
    d = f.path(rings, eps=0.6, min_area=0.0)
    s.F("path", d=d, fill=LAND_HI)
    pts = [f.pt(x, y) for r in rings for x, y in r]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    if max(xs) - min(xs) < 22 and max(ys) - min(ys) < 22:
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        s.raw(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="20" fill="none" stroke="{INK}" stroke-width="6"/>')


def india_state(name):
    def fn(s):
        base = filter_far(main_rings(india_rings(), 0.0005), 40)
        highlight_map(s, base, adm1("India"), name)
    return fn


def usa_lower48():
    parts = {k: v for k, v in adm1("United States of America").items() if k not in ("Alaska", "Hawaii")}
    return parts


def us_state(name):
    def fn(s):
        if name in ("Alaska", "Hawaii"):
            draw_shape(s, adm1("United States of America")[name], fill=LAND_HI)
            return
        parts = usa_lower48()
        base = [r for v in parts.values() for r in v]
        highlight_map(s, base, parts, name)
    return fn


for g in CAT["groups"]:
    if g["id"] == "indian-states":
        for it in g["items"]:
            nm = it["name"] if isinstance(it, dict) else (it if isinstance(it, str) else it[0])
            iid = it["id"] if isinstance(it, dict) else slug(nm)
            if iid == "india-map-with-states":
                continue
            ne_name = IN_NAMES.get(iid) or next((k for k in adm1("India") if slug(k) == iid), None)
            if ne_name:
                D[iid] = india_state(ne_name)
    if g["id"] == "us-states":
        for it in g["items"]:
            nm = it["name"] if isinstance(it, dict) else (it if isinstance(it, str) else it[0])
            iid = it["id"] if isinstance(it, dict) else slug(nm)
            if iid == "usa-map-with-states":
                continue
            ne_name = {"georgia-us-state": "Georgia", "new-york-state": "New York", "washington-state": "Washington"}.get(iid) or next((k for k in adm1("United States of America") if slug(k) == iid), None)
            if ne_name:
                D[iid] = us_state(ne_name)

# ---------------------------------------------------------------- region maps: rivers, lakes, seas, mountains, deserts, islands
from _geo import Region  # noqa: E402

WATER, WATER_HI, RIVER, LAND_R = "#BFE6FA", "#3D8BFD", "#2C6BD6", "#F4EFE2"


def all_land_rings():
    """All land, with India from the India point-of-view shape drawn last (official borders)."""
    others = [r for f in countries() if f["properties"]["NAME"] not in ("India", "Siachen Glacier") for r in rings_of(f)]
    return others + india_rings()


def region_map(s, lon0, lon1, lat0, lat1, sea_hi=None, water=WATER):
    rg = Region(lon0, lon1, lat0, lat1)
    s.F("rect", x=24, y=24, width=464, height=464, rx=30, fill=water)
    if sea_hi:
        for (a0, a1, b0, b1) in sea_hi:
            s.F("path", outline=False, d=rg.poly([[[a0, b1], [a1, b1], [a1, b0], [a0, b0]]], eps=0.5, min_area=0), fill=WATER_HI)
    d = rg.poly(all_land_rings(), eps=0.9, min_area=4.0)
    s.F("path", d=d, fill=LAND_R)
    s.F("path", outline=False, d=d, fill=LAND_R, stroke=LAND_R, stroke_width=6)
    s.F("rect", x=24, y=24, width=464, height=464, rx=30, fill="none")
    return rg


RIVERS = None
LAKES = None


def river_lines(names):
    global RIVERS
    if RIVERS is None:
        RIVERS = load("ne_50m_rivers_lake_centerlines")
    out = []
    for f in RIVERS:
        if slug(f["properties"].get("name") or "") in {slug(n) for n in names}:
            g = f["geometry"]
            out += [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
    return out


def lake_rings(names):
    global LAKES
    if LAKES is None:
        LAKES = load("ne_50m_lakes")
    return [r for f in LAKES if (f["properties"].get("name") or "") in names for r in rings_of(f)]


def bbox(lines, pad=2.0, square=True):
    xs = [p[0] for l in lines for p in l]
    ys = [p[1] for l in lines for p in l]
    x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    if square:
        k = math.cos(math.radians((y0 + y1) / 2))
        w, h = (x1 - x0) * k, y1 - y0
        if w > h:
            c = (y0 + y1) / 2
            y0, y1 = c - w / 2, c + w / 2
        else:
            c = (x0 + x1) / 2
            x0, x1 = c - h / k / 2, c + h / k / 2
    return x0, x1, y0, y1


RIVER_NAMES = {
    "nile": ["Nile", "Albert Nile", "Victoria Nile", "Bahr el Jebel", "El Bahr el Abyad", "El Bahr el Azraq", "Abay", "Damietta Branch", "Rosetta Branch"],
    "amazon-river": ["Amazonas", "Ucayali", "Marañón", "Marañón"], "yangtze": ["Chang Jiang", "Yangtze", "Jinsha", "Tongtian", "Tuotuo"],
    "yellow-river": ["Huang"], "mississippi-river": ["Mississippi"], "ganges": ["Ganges"], "yamuna": ["Yamuna"], "indus-river": ["Indus"],
    "brahmaputra": ["Brahmaputra", "Yarlung", "Dihang"], "godavari": ["Godāvari", "Godavari"], "krishna-river": ["Krishna"], "narmada": ["Narmada"],
    "tigris": ["Tigris", "Dicle"], "euphrates": ["Euphrates", "Firat", "Al Furat"], "jordan-river": ["Jordan"], "danube": ["Danube", "Donau"],
    "rhine": ["Rhine", "Rhein", "Rhin", "Nederrijn", "Waal"], "thames": ["Thames"], "volga": ["Volga"], "mekong": ["Mekong", "Lancang"],
    "congo-river": ["Congo", "Lualaba"], "niger-river": ["Niger"], "zambezi": ["Zambezi"], "colorado-river": ["Colorado"], "seine": ["Seine"],
}


def river_drawing(names):
    def fn(s):
        lines = river_lines(set(names))
        if not lines:
            raise KeyError(names)
        rg = region_map(s, *bbox(lines, 2.5))
        for l in lines:
            d = rg.line(l)
            if d:
                s.T(d, RIVER, 12)
    return fn


for _id, _names in RIVER_NAMES.items():
    D[_id] = river_drawing(_names)


@reg("kaveri")
def _(s):
    rg = region_map(s, 73.5, 81.5, 8.5, 16.5)
    s.T(rg.line([[75.7, 12.4], [76.2, 12.3], [76.6, 12.2], [77.2, 12.1], [77.8, 11.9], [78.3, 11.5], [78.8, 11.0], [79.4, 10.9], [79.85, 11.1]]), RIVER, 12)


LAKE_NAMES = {"lake-baikal": ["Lake Baikal"], "lake-superior": ["Lake Superior"], "great-lakes": ["Lake Superior", "Lake Michigan", "Lake Huron", "Lake Erie", "Lake Ontario"],
              "lake-victoria": ["Lake Victoria"], "lake-tanganyika": ["Lake Tanganyika"], "lake-titicaca": ["Lago Titicaca"], "dead-sea": ["Dead Sea"]}


def lake_drawing(names):
    def fn(s):
        rings = lake_rings(set(names))
        rg = region_map(s, *bbox(rings, 1.5 if len(rings) < 3 else 2.5))
        s.F("path", d=rg.poly(rings, eps=0.6, min_area=0), fill=WATER_HI)
    return fn


for _id, _names in LAKE_NAMES.items():
    D[_id] = lake_drawing(_names)


def spot(lat, lon, half=3.0, icon="lake", sz=1.0):
    def fn(s):
        k = math.cos(math.radians(lat))
        rg = region_map(s, lon - half / k, lon + half / k, lat - half, lat + half)
        x, y = rg.frame.pt(lon, lat)
        if icon == "lake":
            s.F("ellipse", cx=f"{x:.0f}", cy=f"{y:.0f}", rx=f"{36 * sz:.0f}", ry=f"{22 * sz:.0f}", fill=WATER_HI)
        elif icon == "peak":
            s.F("polygon", points=f"{x - 40 * sz:.0f},{y + 26 * sz:.0f} {x:.0f},{y - 40 * sz:.0f} {x + 40 * sz:.0f},{y + 26 * sz:.0f}", fill="#8C7A6A")
            s.F("polygon", outline=False, points=f"{x - 14 * sz:.0f},{y - 18 * sz:.0f} {x:.0f},{y - 40 * sz:.0f} {x + 14 * sz:.0f},{y - 18 * sz:.0f}", fill=WHITE_)
        elif icon == "desert":
            s.F("ellipse", cx=f"{x:.0f}", cy=f"{y:.0f}", rx=f"{150 * sz:.0f}", ry=f"{90 * sz:.0f}", fill="#F2C94C", fill_opacity="0.75")
            for dx in (-60, 0, 60):
                s.M(f"M{x + dx * sz - 24:.0f} {y + 10:.0f} q24 -24 48 0", "#C9963A", 6)
        elif icon == "island":
            s.raw(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{40 * sz:.0f}" fill="none" stroke="{C["red"]}" stroke-width="8"/>')
    return fn


WHITE_ = C["white"]
D["caspian-sea"] = lambda s: region_map(s, 44, 57, 34.5, 48.5, sea_hi=[(46, 55, 36.5, 47.5)])
D["dal-lake"] = spot(34.11, 74.86, 1.2, "lake")
D["chilika-lake"] = spot(19.7, 85.3, 2.0, "lake")
D["wular-lake"] = spot(34.36, 74.6, 1.2, "lake")

PEAKS = {"mount-everest": (27.99, 86.93, 4), "k2": (35.88, 76.51, 4), "kangchenjunga": (27.70, 88.15, 4), "nanda-devi": (30.38, 79.97, 4), "mount-kilimanjaro": (-3.07, 37.35, 5),
         "mont-blanc": (45.83, 6.86, 4), "mount-fuji": (35.36, 138.73, 4), "denali": (63.07, -151.0, 6), "aconcagua": (-32.65, -70.01, 5), "mount-elbrus": (43.35, 42.44, 5),
         "matterhorn": (45.98, 7.66, 3), "table-mountain": (-33.96, 18.40, 3)}
for _id, (_la, _lo, _h) in PEAKS.items():
    D[_id] = spot(_la, _lo, _h, "peak")

RANGES = {"himalayas": [(35.5, 74.5), (33, 77), (30.5, 80), (28.5, 84), (27.8, 87), (27.8, 90), (28.0, 93.5)],
          "alps": [(44.2, 7.0), (45.9, 7.0), (46.5, 9.0), (46.8, 11.5), (47.3, 13.5), (47.7, 15.5)],
          "andes": [(10, -72), (2, -77), (-8, -77.5), (-16, -71), (-24, -68), (-32, -70), (-42, -71.5), (-52, -73)],
          "rocky-mountains": [(60, -125), (54, -120), (49, -115), (44, -110), (39, -106), (34, -106)],
          "atlas-mountains": [(30, -9), (31.5, -6.5), (33, -4), (34.5, 0), (35.5, 4), (36.3, 8)],
          "ural-mountains": [(68, 65), (64, 60), (60, 59.5), (56, 59), (52, 58)],
          "western-ghats": [(21, 73.6), (18.5, 73.6), (15.5, 74.2), (12.5, 75.5), (10, 77), (8.3, 77.3)],
          "eastern-ghats": [(21.5, 85.5), (19, 83.5), (17, 81.5), (15, 79.5), (13, 79), (11.5, 78)],
          "aravalli-range": [(28.5, 77.0), (27, 76), (25.8, 74.5), (24.5, 73.3)],
          "hindu-kush": [(37.0, 73.5), (36.2, 71.5), (35.5, 70), (34.8, 68)],
          "karakoram": [(37.0, 74.0), (36.0, 76.0), (35.5, 77.5), (34.8, 78.5)]}


def mountain_range(pts):
    def fn(s):
        lines = [[[lo, la] for la, lo in pts]]
        rg = region_map(s, *bbox(lines, 4))
        for la, lo in pts:
            x, y = rg.frame.pt(lo, la)
            s.F("polygon", points=f"{x - 22:.0f},{y + 16:.0f} {x:.0f},{y - 26:.0f} {x + 22:.0f},{y + 16:.0f}", fill="#8C7A6A")
            s.F("polygon", outline=False, points=f"{x - 8:.0f},{y - 12:.0f} {x:.0f},{y - 26:.0f} {x + 8:.0f},{y - 12:.0f}", fill=WHITE_)
    return fn


for _id, _pts in RANGES.items():
    D[_id] = mountain_range(_pts)

DESERTS = {"sahara-desert": (23, 13, 16, 1.3), "arabian-desert": (22, 47, 10, 1.0), "rub-al-khali": (20, 50, 6, 0.8), "thar-desert": (27, 71.5, 6, 0.6),
           "gobi-desert": (43, 105, 10, 0.9), "kalahari-desert": (-23, 22, 8, 0.8), "atacama-desert": (-24, -69.5, 7, 0.45), "namib-desert": (-24, 15, 7, 0.45),
           "mojave-desert": (35, -116, 5, 0.6)}
for _id, (_la, _lo, _h, _sz) in DESERTS.items():
    D[_id] = spot(_la, _lo, _h, "desert", _sz)
D["antarctic-desert"] = lambda s: polar_south(s, continent_rings("antarctica"), fill=WHITE_)

ISLANDS = {"borneo": (0.5, 114.5, 6), "sumatra": (-0.3, 101.5, 6), "java-island": (-7.3, 110.0, 4), "bali": (-8.4, 115.2, 0.8),
           "andaman-and-nicobar-islands": (11.0, 92.8, 4), "galapagos-islands": (-0.6, -90.5, 1.6), "sicily": (37.5, 14.2, 1.6), "zanzibar": (-6.1, 39.3, 0.7),
           "socotra": (12.5, 53.9, 1.0), "tasmania": (-42.0, 146.6, 2.6), "canary-islands": (28.3, -15.6, 2.6), "easter-island": (-27.1, -109.35, 0.5)}


def island(lat, lon, rad):
    def fn(s):
        rings = []
        for f in countries():
            for r in rings_of(f):
                cx, cy = centroid(r)
                if math.hypot((cx - lon) * math.cos(math.radians(lat)), cy - lat) <= rad:
                    rings.append(r)
        if rings:
            draw_shape(s, rings, eps=0.8)
        else:
            spot(lat, lon, 4, "island")(s)
    return fn


for _id, (_la, _lo, _r) in ISLANDS.items():
    D[_id] = island(_la, _lo, _r)
D["greenland"] = country_drawing("greenland", ["Greenland"])
D["sri-lanka-island"] = country_drawing("sri-lanka", ["Sri Lanka"])

OCEANS = {"pacific-ocean": [(120, 180, -50, 66), (-180, -75, -50, 66)], "atlantic-ocean": [(-75, 15, -50, 68)], "indian-ocean": [(35, 118, -50, 25)],
          "arctic-ocean": [(-180, 0, 68, 95), (0, 180, 68, 95)], "southern-ocean": [(-180, 0, -75, -50), (0, 180, -75, -50)]}


OCEAN_BOX = (24, 140, 488, 372)


def world_land():
    """All land except Antarctica (its coast only shows as slivers on a flat world map)."""
    return [r for r in all_land_rings() if max(p[1] for p in r) > -58]


def ocean_map(boxes):
    def fn(s):
        rg = Region(-180, 180, -62, 84, box=OCEAN_BOX)
        s.F("rect", x=24, y=140, width=464, height=232, rx=24, fill=WATER)
        for (a0, a1, b0, b1) in boxes:
            s.F("path", outline=False, d=rg.poly([[[a0, b1], [a1, b1], [a1, b0], [a0, b0]]], eps=0.5, min_area=0), fill=WATER_HI)
        d = rg.poly(world_land(), eps=2.6, min_area=30.0)
        s.F("path", d=d, fill=LAND_R)
        s.F("path", outline=False, d=d, fill=LAND_R, stroke=LAND_R, stroke_width=6)
        s.F("rect", x=24, y=140, width=464, height=232, rx=24, fill="none")
    return fn


for _id, _b in OCEANS.items():
    D[_id] = ocean_map(_b)


@reg("five-oceans")
def _(s):
    rg = Region(-180, 180, -62, 84, box=OCEAN_BOX)
    s.F("rect", x=24, y=140, width=464, height=232, rx=24, fill=WATER)
    for boxes, c in ((OCEANS["pacific-ocean"], "#3D8BFD"), (OCEANS["atlantic-ocean"], "#5EC8C0"), (OCEANS["indian-ocean"], "#8B5CF6"),
                     (OCEANS["arctic-ocean"], "#9AD0E8"), (OCEANS["southern-ocean"], "#2C6BD6")):
        for (a0, a1, b0, b1) in boxes:
            s.F("path", outline=False, d=rg.poly([[[a0, b1], [a1, b1], [a1, b0], [a0, b0]]], eps=0.5, min_area=0), fill=c)
    d = rg.poly(world_land(), eps=2.6, min_area=30.0)
    s.F("path", d=d, fill=LAND_R)
    s.F("path", outline=False, d=d, fill=LAND_R, stroke=LAND_R, stroke_width=6)
    s.F("rect", x=24, y=140, width=464, height=232, rx=24, fill="none")


SEAS = {"mediterranean-sea": ((-8, 37, 29, 47), [(-6, 36, 30, 46)]), "red-sea": ((30, 46, 11, 31), [(32, 44, 12, 30)]), "arabian-sea": ((52, 80, 3, 27), [(55, 74, 5, 22)]),
        "bay-of-bengal": ((77, 98, 4, 24), [(80, 95, 5, 22)]), "persian-gulf": ((45, 59, 22, 32), [(47.5, 56.5, 24, 30.5)]), "gulf-of-oman": ((54, 63, 21, 28), [(56, 61, 22, 26)]),
        "caribbean-sea": ((-90, -58, 6, 25), [(-86, -60, 10, 20)]), "south-china-sea": ((100, 124, 0, 25), [(105, 120, 3, 22)]), "black-sea": ((26, 43, 39, 48), [(27.5, 41.5, 41, 46.5)]),
        "north-sea": ((-6, 12, 49, 62), [(-2, 9, 51, 61)]), "baltic-sea": ((9, 32, 53, 67), [(12, 30, 54, 65)]), "gulf-of-mexico": ((-100, -78, 17, 32), [(-97, -81, 19, 30)]),
        "bering-sea": ((160, 205, 50, 68), [(165, 200, 52, 65)]), "sea-of-japan": ((126, 144, 32, 53), [(128, 141, 34, 51)]), "coral-sea": ((142, 168, -28, -6), [(146, 162, -26, -8)])}
for _id, ((_x0, _x1, _y0, _y1), _hi) in SEAS.items():
    D[_id] = (lambda a, h: lambda s: region_map(s, *a, sea_hi=h))((_x0, _x1, _y0, _y1), _hi)


D["india-map-with-states"] =lambda s: highlight_map(s, filter_far(main_rings(india_rings(), 0.0005), 40), adm1("India"), None, all_states=True)
D["usa-map-with-states"] = lambda s: highlight_map(s, [r for v in usa_lower48().values() for r in v], usa_lower48(), None, all_states=True)


if __name__ == "__main__":
    run("earth-geography", D, sys.argv[1:] or None)
