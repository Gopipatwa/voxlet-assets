"""brain-teasers-logic drawings. Run: python drawings/brain_teasers_logic.py [ids...]"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import *  # noqa: E402,F401,F403
from _parts import place as P  # noqa: E402
from _parts2 import *  # noqa: E402,F401,F403
from draw_lib import C, arc_pt, head, run, star_pts, stroke_text  # noqa: E402

D = {}


def scene(*steps):
    def fn(s):
        for st in steps:
            if callable(st):
                st(s)
            else:
                part, x, y, sc, *rest = st
                P(s, part, x, y, sc, **(rest[0] if rest else {}))
    return fn


def txt(t, x, y, h, color=DARK, w=None):
    return lambda s: stroke_text(s, t, x, y, h, color, w or max(6, h / 7))


def card(s, x=56, y=56, w=400, h=400, fill=LIGHT):
    s.F("rect", x=x, y=y, width=w, height=h, rx=30, fill=fill)


def grid(s, n, x0=96, y0=96, size=320, color=DARK, w=6, bold=None):
    c = size / n
    for i in range(n + 1):
        ww = w * 2 if bold and i % bold == 0 else w
        s.M(f"M{x0 + i * c:.1f} {y0} V{y0 + size} M{x0} {y0 + i * c:.1f} H{x0 + size}", color, ww, cap="square")


def nums(s, cells, n, x0=96, y0=96, size=320, color=DARK, scale=0.55):
    c = size / n
    for (r, col), v in cells.items():
        stroke_text(s, str(v), x0 + (col + 0.5) * c, y0 + (r + 0.5) * c, c * scale, color, max(5, c * scale / 7))


# ---------------------------------------------------------------- mazes (themed)
def square_maze(s, n=8, seed=3, x0=96, size=320, path=False, wall=A1):
    random.seed(seed)
    c = size / n
    seen = {(0, 0)}
    stack = [(0, 0)]
    open_ = set()
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in seen]
        if nb:
            nx, ny = random.choice(nb)
            open_.add(frozenset(((x, y), (nx, ny))))
            seen.add((nx, ny)); stack.append((nx, ny))
        else:
            stack.pop()
    s.F("rect", x=x0 - 24, y=x0 - 24, width=size + 48, height=size + 48, rx=26, fill=LIGHT)
    d = []
    for x in range(n):
        for y in range(n):
            if x + 1 < n and frozenset(((x, y), (x + 1, y))) not in open_:
                d.append(f"M{x0 + (x + 1) * c:.0f} {x0 + y * c:.0f} V{x0 + (y + 1) * c:.0f}")
            if y + 1 < n and frozenset(((x, y), (x, y + 1))) not in open_:
                d.append(f"M{x0 + x * c:.0f} {x0 + (y + 1) * c:.0f} H{x0 + (x + 1) * c:.0f}")
    d.append(f"M{x0 + c:.0f} {x0} H{x0 + size} V{x0 + size} M{x0 + size - c:.0f} {x0 + size} H{x0} V{x0}")
    s.M(" ".join(d), wall, 12, cap="square")
    if path:
        # BFS from (0,0) to (n-1,n-1)
        prev = {(0, 0): None}
        q = [(0, 0)]
        while q:
            cur = q.pop(0)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx_, ny_ = cur[0] + dx, cur[1] + dy
                if (nx_, ny_) not in prev and frozenset((cur, (nx_, ny_))) in open_:
                    prev[(nx_, ny_)] = cur; q.append((nx_, ny_))
        node, pts = (n - 1, n - 1), []
        while node:
            pts.append(node); node = prev[node]
        s.M("M" + " L".join(f"{x0 + (a + 0.5) * c:.0f} {x0 + (b + 0.5) * c:.0f}" for a, b in reversed(pts)), A2, 10)
    return c


def ring_maze(s, sides=0, rings=4, seed=5):
    random.seed(seed)
    s.F("circle" if not sides else "polygon", **({"cx": 256, "cy": 256, "r": 220} if not sides else
        {"points": " ".join(f"{x:.0f},{y:.0f}" for x, y in (arc_pt(256, 256, 226, i * 60 - 90) for i in range(6)))}), fill=LIGHT)
    for k in range(1, rings + 1):
        r = 40 * k + 20
        gap = random.uniform(0, 360)
        a0, a1 = gap + 25, gap + 335
        if sides:
            pts = [arc_pt(256, 256, r * 1.05, a) for a in range(int(a0), int(a1), 5)]
        else:
            pts = [arc_pt(256, 256, r, a) for a in range(int(a0), int(a1), 4)]
        s.M("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts), A1, 12)
        if k < rings:
            a = random.uniform(0, 360)
            x1, y1 = arc_pt(256, 256, r, a); x2, y2 = arc_pt(256, 256, r + 40, a)
            s.M(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", A1, 12)
    s.F("circle", cx=256, cy=256, r=14, fill=A2)


D["maze"] = lambda s: square_maze(s)
D["square-maze"] = lambda s: square_maze(s, 10, 7)
D["circular-maze"] = lambda s: ring_maze(s)
D["hexagon-maze"] = lambda s: ring_maze(s, sides=6, seed=9)
D["maze-solution"] = lambda s: square_maze(s, 8, 11, path=True)


@lambda f: D.__setitem__("maze-with-start-and-finish", f)
def _(s):
    c = square_maze(s, 8, 4)
    s.F("circle", cx=96 + c / 2, cy=96 + c / 2, r=14, fill="#4CB963")
    s.F("polygon", points=star_pts(416 - c / 2, 416 - c / 2, 20, 9, 5), fill=A2)


def hedge(s):
    s.F("rect", outline=False, x=0, y=0, width=512, height=512, fill="none")
    random.seed(2)
    s.F("rect", x=60, y=60, width=392, height=392, rx=20, fill="#9BD7A8")
    for d in ("M60 60 H452 V452 H60 Z", "M120 120 H392 V392 H180", "M180 180 H332 V332 H240", "M120 120 V300", "M392 200 V300"):
        s.T(d, "#4CB963", 26)


D["hedge-maze"] = hedge


@lambda f: D.__setitem__("classical-labyrinth", f)
def _(s):
    s.F("circle", cx=256, cy=256, r=220, fill=LIGHT)
    for r in range(40, 220, 28):
        s.M(f"M{256 - r} 256 A{r} {r} 0 1 1 {256 + r} 256" + (f" V{256 + 30}" if r % 56 else ""), A1, 12)
    s.M("M256 476 V300", LIGHT, 30)


@lambda f: D.__setitem__("heart-maze", f)
def _(s):
    P(s, heart, 256, 256, 1.0, color=A2L)
    s.M("M150 200 C170 150 230 150 240 200 M300 160 C350 150 380 200 360 240 M160 260 H260 V320 M300 260 H360 M220 360 H300 M256 230 V260", A2, 12)


@lambda f: D.__setitem__("brain-maze", f)
def _(s):
    P(s, brain, 256, 256, 1.0, color=A1L, fold=A1L)
    s.M("M150 200 H220 V260 H180 M270 150 V220 H340 M300 260 V320 H230 M150 300 H200 M350 200 V280", A1, 12)


# ---------------------------------------------------------------- grid puzzles (tiles)
def tile(fn):
    def draw_(s):
        card(s)
        fn(s)
    return draw_


D["logic-grid"] = tile(lambda s: (grid(s, 6, bold=3), [s.M(f"M{96 + (c + 0.3) * 53.3:.0f} {96 + (r + 0.5) * 53.3:.0f} l10 10 l18 -20", "#4CB963", 8) for r, c in ((0, 1), (1, 4), (3, 0), (4, 5))],
                              [s.M(f"M{96 + (c + 0.3) * 53.3:.0f} {96 + (r + 0.3) * 53.3:.0f} l22 22 m0 -22 l-22 22", A2, 7) for r, c in ((0, 0), (2, 2), (5, 3))]))
D["zebra-puzzle"] = tile(lambda s: (grid(s, 5), [s.F("rect", outline=False, x=96 + c * 64 + 10, y=96 + 10, width=44, height=44, rx=8, fill=col)
                                                 for c, col in enumerate((A1, A2, "#4CB963", A1L, MID))], P(s, qmark, 256, 320, 0.3)))
D["sudoku-grid"] = tile(lambda s: (grid(s, 9, bold=3, w=4), nums(s, {(0, 0): 5, (0, 4): 7, (1, 2): 3, (2, 7): 9, (3, 3): 1, (4, 4): 8, (5, 8): 2, (6, 1): 6, (7, 5): 4, (8, 8): 7}, 9)))
D["mini-sudoku"] = tile(lambda s: (grid(s, 4, bold=2), nums(s, {(0, 0): 1, (1, 2): 3, (2, 1): 4, (3, 3): 2}, 4)))
D["kakuro-grid"] = tile(lambda s: (grid(s, 5), [s.F("rect", outline=False, x=96 + c * 64, y=96 + r * 64, width=64, height=64, fill=DARK) for r, c in ((0, 0), (0, 3), (2, 0), (4, 4))],
                                   nums(s, {(1, 1): 7, (3, 2): 4}, 5)))
D["calcudoku-grid"] = tile(lambda s: (grid(s, 4, w=4), s.M("M96 176 H256 M256 96 V256 H416 M176 256 V416 M336 256 V416", A1, 12), nums(s, {(0, 0): 6, (1, 2): 3, (3, 1): 8}, 4, scale=0.4)))
D["futoshiki-grid"] = tile(lambda s: (grid(s, 4), nums(s, {(0, 0): 2, (2, 3): 4}, 4), s.M("M170 210 l14 10 l-14 10 M330 290 l-14 10 l14 10", A2, 6)))
D["binary-puzzle-grid"] = tile(lambda s: (grid(s, 6), nums(s, {(0, 1): 1, (0, 4): 0, (1, 2): 0, (2, 0): 1, (3, 5): 1, (4, 3): 0, (5, 1): 0}, 6)))


@lambda f: D.__setitem__("nonogram", f)
def _(s):
    card(s)
    grid(s, 5, x0=176, y0=176, size=240)
    for r, row in enumerate(("01110", "11011", "11111", "01110", "00100")):
        for c, v in enumerate(row):
            if v == "1":
                s.F("rect", outline=False, x=176 + c * 48, y=176 + r * 48, width=48, height=48, fill=A1)
    nums(s, {(0, 0): 3}, 1, 76, 176, 48, scale=0.6); nums(s, {(0, 0): 5}, 1, 76, 272, 48, scale=0.6)
    nums(s, {(0, 0): 2}, 1, 176, 76, 48, scale=0.6); nums(s, {(0, 0): 4}, 1, 272, 76, 48, scale=0.6)


@lambda f: D.__setitem__("crossword-grid", f)
def _(s):
    card(s)
    black = {(0, 3), (1, 1), (2, 4), (3, 0), (3, 2), (4, 3)}
    for r in range(5):
        for c in range(5):
            s.F("rect", x=96 + c * 64, y=96 + r * 64, width=64, height=64, fill=DARK if (r, c) in black else LIGHT)
    nums(s, {(0, 0): "C", (0, 1): "A", (0, 2): "B"}, 5)


D["word-search-grid"] = tile(lambda s: (nums(s, {(r, c): "ABCDEX"[(r * 7 + c * 3) % 6] for r in range(6) for c in range(6)}, 6, scale=0.45),
                                        s.T("M122 149 H390", A2L, 40), nums(s, {(1, c): "ABCDEX"[(7 + c * 3) % 6] for c in range(6)}, 6, scale=0.45)))
D["tic-tac-toe-grid"] = lambda s: (card(s), s.M("M203 110 V402 M309 110 V402 M110 203 H402 M110 309 H402", DARK, 14),
                                   s.M("M126 126 l60 60 m0 -60 l-60 60 M232 232 l48 48 m0 -48 l-48 48", A1, 16),
                                   s.raw(f'<circle cx="356" cy="156" r="32" fill="none" stroke="{A2}" stroke-width="16"/>'),
                                   s.raw(f'<circle cx="156" cy="356" r="32" fill="none" stroke="{A2}" stroke-width="16"/>'))
D["dots-and-boxes"] = tile(lambda s: (s.M("M136 136 H256 V256 H136 Z M256 136 H376 M256 256 V376", A1, 10),
                                      s.F("rect", outline=False, x=146, y=146, width=100, height=100, fill=A1L),
                                      [s.F("circle", outline=False, cx=136 + c * 120, cy=136 + r * 120, r=14, fill=DARK) for r in range(3) for c in range(3)]))
D["connect-the-dots"] = tile(lambda s: (s.M("M120 360 L180 200 L256 130 L332 200 L392 360", A1, 8, dash="16 14"),
                                        [(s.F("circle", outline=False, cx=x, cy=y, r=14, fill=DARK), stroke_text(s, str(i + 1), x + 26, y - 26, 30, DARK, 5))
                                         for i, (x, y) in enumerate(((120, 360), (180, 200), (256, 130), (332, 200), (392, 360)))]))
D["truth-table"] = tile(lambda s: (grid(s, 4, x0=136, y0=96, size=240), s.F("rect", outline=False, x=136, y=96, width=240, height=60, fill=A1L),
                                   nums(s, {(1, 0): 0, (1, 1): 0, (1, 2): 0, (2, 0): 1, (2, 1): 0, (2, 2): 1, (3, 0): 1, (3, 1): 1, (3, 2): 1}, 4, 136, 96, 240)))


@lambda f: D.__setitem__("eight-queens-puzzle", f)
def _(s):
    card(s)
    for r in range(8):
        for c in range(8):
            s.F("rect", outline=False, x=96 + c * 40, y=96 + r * 40, width=40, height=40, fill=A1L if (r + c) % 2 else LIGHT)
    for r, c in enumerate((0, 4, 7, 5, 2, 6, 1, 3)):
        P(s, crown, 116 + c * 40, 116 + r * 40, 0.075)
    s.F("rect", x=96, y=96, width=320, height=320, fill="none")


@lambda f: D.__setitem__("knights-tour", f)
def _(s):
    card(s)
    for r in range(5):
        for c in range(5):
            s.F("rect", outline=False, x=96 + c * 64, y=96 + r * 64, width=64, height=64, fill=A1L if (r + c) % 2 else LIGHT)
    pts = ((0, 0), (1, 2), (0, 4), (2, 3), (4, 4), (3, 2), (4, 0), (2, 1))
    s.M("M" + " L".join(f"{128 + c * 64} {128 + r * 64}" for r, c in pts), A2, 8)
    P(s, knight, 128, 128, 0.14)
    s.F("rect", x=96, y=96, width=320, height=320, fill="none")


# ---------------------------------------------------------------- sequences and patterns (tiles)
def row_shapes(s, shapes, y=256, q_last=True):
    n = len(shapes) + (1 if q_last else 0)
    step = 360 / n
    for i, sh in enumerate(shapes):
        x = 76 + step * (i + 0.5)
        sh(s, x, y)
    if q_last:
        s.F("rect", x=76 + step * (n - 0.5) - 34, y=y - 34, width=68, height=68, rx=12, fill=A1L)
        stroke_text(s, "?", 76 + step * (n - 0.5), y, 46, DARK, 8)


def circ(c=A1, r=30):
    return lambda s, x, y: s.F("circle", cx=f"{x:.0f}", cy=y, r=r, fill=c)


def sq(c=A2, r=30):
    return lambda s, x, y: s.F("rect", x=f"{x - r:.0f}", y=y - r, width=2 * r, height=2 * r, rx=6, fill=c)


def tri(c="#4CB963", r=34):
    return lambda s, x, y: s.F("polygon", points=f"{x:.0f},{y - r} {x + r:.0f},{y + r * 0.8:.0f} {x - r:.0f},{y + r * 0.8:.0f}", fill=c)


D["number-sequence"] = tile(lambda s: (txt("2 4 8 16", 256, 220, 60)(s), txt("?", 256, 340, 80, A2)(s)))
D["shape-sequence"] = tile(lambda s: row_shapes(s, [circ(), sq(), tri(), circ()]))
D["colour-pattern"] = tile(lambda s: row_shapes(s, [circ(A1), circ(A2), circ(A1), circ(A2)]))
D["missing-number"] = tile(lambda s: (txt("3 6 ? 12", 256, 256, 70)(s), s.T("M206 310 H266", A2, 10)))
D["repeating-pattern"] = tile(lambda s: row_shapes(s, [sq(), circ(), sq(), circ(), sq()], q_last=False))
D["growing-pattern"] = tile(lambda s: [s.F("rect", x=110 + i * 90, y=330 - (i + 1) * 50, width=60, height=(i + 1) * 50, rx=6, fill=A1) for i in range(4)])


@lambda f: D.__setitem__("next-shape-question", f)
def _(s):
    card(s)
    for i, n in enumerate((3, 4, 5)):
        x = 120 + i * 100
        s.F("polygon", points=" ".join(f"{a:.0f},{b:.0f}" for a, b in (arc_pt(x, 220, 36, k * 360 / n - 90) for k in range(n))), fill=A1)
    s.F("rect", x=376 - 34, y=186, width=68, height=68, rx=12, fill=A1L)
    stroke_text(s, "?", 376, 220, 46, DARK, 8)
    s.M("M110 330 H402", MID, 8)


@lambda f: D.__setitem__("matrix-reasoning-puzzle", f)
def _(s):
    card(s)
    grid(s, 3, x0=106, y0=106, size=300)
    shapes = [circ, sq, tri]
    for r in range(3):
        for c in range(3):
            if r == 2 and c == 2:
                stroke_text(s, "?", 356, 356, 60, A2, 10)
            else:
                shapes[(r + c) % 3](A1 if r == 0 else A2 if r == 1 else "#4CB963", 26)(s, 156 + c * 100, 156 + r * 100)


D["analogy-puzzle"] = tile(lambda s: (circ(A1)(s, 130, 180), txt("=", 210, 180, 50)(s), circ(A1, 46)(s, 300, 180),
                                      sq(A2)(s, 130, 330), txt("=", 210, 330, 50)(s), txt("?", 300, 330, 70, A2)(s)))


@lambda f: D.__setitem__("number-pyramid", f)
def _(s):
    card(s)
    vals = [[None], [5, 7], [2, 3, 4]]
    for r, row in enumerate(vals):
        for i, v in enumerate(row):
            x = 256 - (len(row) - 1) * 50 + i * 100
            y = 150 + r * 100
            s.F("rect", x=x - 46, y=y - 40, width=92, height=80, rx=10, fill=A1L if v else A2L)
            stroke_text(s, str(v) if v else "?", x, y, 50, DARK, 8)


@lambda f: D.__setitem__("number-wheel-puzzle", f)
def _(s):
    s.F("circle", cx=256, cy=256, r=200, fill=LIGHT)
    for i, v in enumerate((2, 4, 6, 8, 10, "?")):
        a = i * 60 - 90
        x1, y1 = arc_pt(256, 256, 200, a + 30)
        s.M(f"M256 256 L{x1:.0f} {y1:.0f}", MID, 6)
        x, y = arc_pt(256, 256, 130, a)
        stroke_text(s, str(v), x, y, 50, A2 if v == "?" else DARK, 8)
    s.F("circle", cx=256, cy=256, r=40, fill=A1)


def domino_tile(s, x, y, a, b):
    s.F("rect", x=x - 40, y=y - 80, width=80, height=160, rx=12, fill=LIGHT)
    s.M(f"M{x - 30} {y} H{x + 30}", DARK, 6)
    for v, cy in ((a, y - 40), (b, y + 40)):
        spots = {1: [(0, 0)], 2: [(-14, -14), (14, 14)], 3: [(-16, -16), (0, 0), (16, 16)], 4: [(-14, -14), (14, -14), (-14, 14), (14, 14)]}.get(v, [])
        for dx, dy in spots:
            s.F("circle", outline=False, cx=x + dx, cy=cy + dy, r=7, fill=DARK)


D["domino-sequence"] = lambda s: (domino_tile(s, 110, 256, 1, 2), domino_tile(s, 210, 256, 2, 3), domino_tile(s, 310, 256, 3, 4),
                                  s.F("rect", x=370, y=176, width=80, height=160, rx=12, fill=A1L), stroke_text(s, "?", 410, 256, 60, DARK, 9))


@lambda f: D.__setitem__("clock-sequence-puzzle", f)
def _(s):
    for i, h in enumerate((30, 90, 150)):
        P(s, clock, 100 + i * 110, 256, 0.26, h=h, m=0)
    s.F("circle", cx=430, cy=256, r=50, fill=A1L)
    stroke_text(s, "?", 430, 256, 50, DARK, 8)


D["letter-sequence"] = tile(lambda s: txt("A C E ?", 256, 256, 80)(s))

# ---------------------------------------------------------------- matchsticks (keep)
WOOD, HEADC = C["tan"], C["red"]


def stick(s, x1, y1, x2, y2):
    s.T(f"M{x1} {y1} L{x2} {y2}", WOOD, 16, cap="round")
    s.F("circle", cx=x2, cy=y2, r=13, fill=HEADC)


def sticks(segs):
    def fn(s):
        for seg in segs:
            stick(s, *seg)
    return fn


D["puzzle-matchstick"] = sticks([(120, 400, 380, 120)])
D["matchstick-equation"] = sticks([(80, 180, 80, 330), (110, 255, 190, 255), (150, 215, 150, 295), (230, 180, 230, 330), (270, 230, 340, 230), (270, 280, 340, 280),
                                   (380, 180, 440, 180), (440, 180, 440, 255), (380, 255, 440, 255), (380, 255, 380, 330), (380, 330, 440, 330)])
D["matchstick-squares-puzzle"] = sticks([(100, 140, 230, 140), (230, 140, 230, 270), (230, 270, 100, 270), (100, 270, 100, 140), (230, 140, 360, 140),
                                         (360, 140, 360, 270), (360, 270, 230, 270), (100, 270, 100, 400), (100, 400, 230, 400), (230, 400, 230, 270)])
D["matchstick-triangles-puzzle"] = sticks([(110, 380, 256, 120), (256, 120, 400, 380), (400, 380, 110, 380), (183, 250, 330, 250), (183, 250, 256, 380), (330, 250, 256, 380)])
D["matchstick-fish-puzzle"] = sticks([(110, 180, 230, 256), (110, 330, 230, 256), (110, 180, 110, 330), (230, 256, 330, 170), (330, 170, 420, 256), (420, 256, 330, 340), (330, 340, 230, 256)])
D["matchstick-glass-puzzle"] = lambda s: (sticks([(150, 120, 230, 300), (360, 120, 280, 300), (230, 300, 280, 300), (256, 300, 256, 420)])(s),
                                          s.F("circle", cx=256, cy=220, r=26, fill=HEADC))
D["matchstick-digits"] = sticks([(90, 140, 190, 140), (190, 140, 190, 256), (190, 256, 190, 370), (90, 370, 190, 370), (90, 256, 190, 256), (90, 140, 90, 256),
                                 (320, 140, 420, 140), (420, 140, 420, 256), (320, 256, 420, 256), (320, 256, 320, 370), (320, 370, 420, 370)])
D["matchstick-house-puzzle"] = sticks([(120, 230, 256, 110), (256, 110, 390, 230), (120, 230, 390, 230), (120, 230, 120, 400), (390, 230, 390, 400), (120, 400, 390, 400)])

# ---------------------------------------------------------------- number puzzles (tiles)
D["magic-square"] = tile(lambda s: (grid(s, 3), nums(s, {(0, 0): 2, (0, 1): 7, (0, 2): 6, (1, 0): 9, (1, 1): 5, (1, 2): 1, (2, 0): 4, (2, 1): 3, (2, 2): 8}, 3, scale=0.45)))
D["lo-shu-square"] = tile(lambda s: (grid(s, 3, color=A2), [s.F("circle", outline=False, cx=96 + (c + 0.5) * 106.7 + dx, cy=96 + (r + 0.5) * 106.7 + dy, r=9, fill=DARK if v % 2 == 0 else LIGHT)
                                                            for (r, c), v in {(0, 0): 4, (0, 1): 9, (0, 2): 2, (1, 0): 3, (1, 1): 5, (1, 2): 7, (2, 0): 8, (2, 1): 1, (2, 2): 6}.items()
                                                            for dx, dy in [((i % 3 - 1) * 22, (i // 3 - 1) * 22) for i in range(v)]],
                                     [s.raw(f'<circle cx="{96 + (c + 0.5) * 106.7 + (i % 3 - 1) * 22:.0f}" cy="{96 + (r + 0.5) * 106.7 + (i // 3 - 1) * 22:.0f}" r="9" fill="none" stroke="{DARK}" stroke-width="4"/>')
                                      for (r, c), v in {(0, 1): 9, (1, 0): 3, (1, 1): 5, (1, 2): 7, (2, 1): 1}.items() for i in range(v)]))


@lambda f: D.__setitem__("magic-triangle", f)
def _(s):
    s.F("polygon", points="256,70 452,420 60,420", fill=LIGHT)
    for (x, y), v in zip(((256, 120), (180, 250), (332, 250), (110, 380), (256, 380), (402, 380)), (1, 6, 5, 4, 2, 3)):
        s.F("circle", cx=x, cy=y, r=38, fill=A1L)
        stroke_text(s, str(v), x, y, 40, DARK, 7)


@lambda f: D.__setitem__("magic-star-puzzle", f)
def _(s):
    s.F("polygon", points=star_pts(256, 266, 220, 92, 5), fill=A2L)
    for i, v in enumerate((1, 2, 3, 4, 5, 6, 7, 8, 9, "?")):
        r = 220 if i % 2 == 0 else 92
        x, y = arc_pt(256, 266, r, -90 + i * 36)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=24, fill=LIGHT)
        stroke_text(s, str(v), x, y, 24, DARK, 5)


D["make-24-card"] = lambda s: (card(s, fill=A2L), [(s.F("circle", cx=x, cy=y, r=54, fill=LIGHT), stroke_text(s, str(v), x, y, 54, DARK, 9))
                                                    for (x, y), v in zip(((256, 140), (140, 256), (372, 256), (256, 372)), (8, 3, 8, 3))])
D["number-chain-puzzle"] = lambda s: [(s.F("circle", cx=x, cy=256, r=44, fill=A1L if v != "?" else A2L), stroke_text(s, str(v), x, 256, 44, DARK, 8),
                                       s.M(f"M{x + 44} 256 H{x + 66}", DARK, 8) if x < 420 else None) for x, v in zip((70, 180, 290, 420), (3, 9, 27, "?"))]


@lambda f: D.__setitem__("fruit-equation-puzzle", f)
def _(s):
    card(s)
    for row, y in ((("A", "A", "6"), 170), (("A", "B", "8"), 256), (("B", "?", ""), 342)):
        for i, v in enumerate(row[:2]):
            x = 130 + i * 110
            if v == "A":
                s.F("circle", cx=x, cy=y, r=32, fill=C["red"]); s.T(f"M{x} {y - 30} V{y - 46}", C["darkbrown"], 6)
            elif v == "B":
                s.F("path", d=f"M{x - 34} {y - 10} C{x - 20} {y + 30} {x + 30} {y + 30} {x + 36} {y - 20} C{x + 10} {y} {x - 10} {y} {x - 34} {y - 10}Z", fill=C["yellow"])
        stroke_text(s, "+", 185, y, 30, DARK, 6)
        stroke_text(s, "=", 300, y, 30, DARK, 6)
        stroke_text(s, row[2] or "?", 370, y, 46, A2 if not row[2] else DARK, 8)


D["emoji-equation"] = tile(lambda s: ([P(s, heart, x, 200, 0.14) for x in (130, 240)], txt("+", 185, 200, 34)(s), txt("= 10", 340, 200, 50)(s),
                                      P(s, star, 130, 320, 0.14), txt("+", 185, 320, 34)(s), P(s, heart, 240, 320, 0.14), txt("= ?", 340, 320, 50, A2)(s)))
D["age-riddle-card"] = tile(lambda s: (P(s, person, 160, 260, 0.45), P(s, person, 300, 300, 0.3, shirt=A2), txt("?", 400, 180, 80, A2)(s)))
D["cryptarithm"] = tile(lambda s: (txt("ABC", 300, 150, 60)(s), txt("+ABC", 270, 240, 60)(s), s.M("M130 290 H400", DARK, 8), txt("DEC", 300, 350, 60, A1)(s)))

# ---------------------------------------------------------------- tangrams and shape puzzles (themed)
TANGRAM = {  # 7 pieces of a 300-px square at (106, 106)
    "big1": "106,106 406,106 256,256", "big2": "106,106 256,256 106,406", "med": "406,256 406,406 256,406",
    "small1": "256,256 331,181 331,331", "small2": "106,406 181,331 256,406", "square": "256,256 331,331 256,406 181,331",
    "para": "331,181 406,106 406,256 331,331",
}
TCOL = {"big1": A1, "big2": A2, "med": A1L, "small1": "#4CB963", "small2": A1D, "square": A2L, "para": "#8B5CF6"}


def tangram_shape(placements):
    """placements: list of (piece, transform)."""
    def fn(s):
        for piece, tf in placements:
            s.F("polygon", points=TANGRAM[piece], fill=TCOL[piece], transform=tf)
    return fn


D["tangram"] = tangram_shape([(p, "") for p in TANGRAM])
def tfig(polys):
    def fn(s):
        for pts, col in polys:
            s.F("polygon", points=pts, fill=col)
    return fn


PU = "#8B5CF6"
D["tangram-cat"] = tfig([("160,180 230,110 300,180 230,250", A2L), ("170,150 180,96 214,128", "#4CB963"), ("246,128 280,96 290,150", A1D),
                         ("150,260 350,460 150,460", A1), ("230,260 350,260 350,380", A1L), ("350,460 410,400 450,400 390,460", PU)])
D["tangram-bird"] = tfig([("110,320 330,320 220,210", A1), ("220,210 330,320 330,210", A2), ("330,170 380,120 430,170 380,220", A2L),
                          ("430,170 480,170 430,200", "#4CB963"), ("110,320 60,270 60,370", PU), ("220,320 280,390 200,390", A1D), ("280,390 320,430 240,430", A1L)])
D["tangram-house"] = tfig([("96,240 256,80 416,240", A1), ("126,240 386,240 386,440 126,440", A2L), ("200,320 260,320 260,440 200,440", A2),
                           ("300,290 350,290 350,340 300,340", A1L), ("330,96 370,96 370,180 330,140", A1D)])
D["tangram-runner"] = tfig([("220,60 270,110 220,160 170,110", A2L), ("190,170 300,170 260,300 150,300", A1), ("150,300 260,300 110,430", A2),
                            ("230,300 330,410 260,430", A1L), ("300,170 380,140 400,190", "#4CB963"), ("190,170 110,240 150,250", A1D)])
D["tangram-boat"] = tfig([("256,70 256,320 100,320", A1), ("270,110 270,320 400,320", A2L), ("80,340 432,340 380,420 132,420", A2), ("256,40 300,60 256,80", PU)])
D["tangram-rabbit"] = tfig([("200,60 230,60 260,170 230,170", PU), ("260,60 290,60 290,170 260,170", A1D), ("210,170 300,170 300,250 210,250", A2L),
                            ("200,250 400,450 200,450", A1), ("200,330 120,450 200,450", A2), ("400,450 440,410 460,450", "#4CB963")])
D["tangram-fish"] = tfig([("80,256 250,90 420,256", A1), ("80,256 420,256 250,420", A2), ("420,256 480,180 480,330", A1L), ("150,220 180,190 210,220 180,250", LIGHT)])


def blocks(cells, size=56, x0=None, y0=None, color=A1):
    def fn(s):
        xs = [c for _, c in cells]; ys = [r for r, _ in cells]
        ox = x0 if x0 is not None else 256 - (max(xs) + 1) * size / 2
        oy = y0 if y0 is not None else 256 - (max(ys) + 1) * size / 2
        for r, c in cells:
            s.F("rect", x=f"{ox + c * size:.0f}", y=f"{oy + r * size:.0f}", width=size, height=size, rx=6, fill=color)
    return fn


D["pentomino-set"] = lambda s: [blocks(cells, 36, x, y, col)(s) for cells, x, y, col in (
    ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], 70, 80, A1), ([(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)], 130, 80, A2),
    ([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], 260, 80, "#4CB963"), ([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 130, 260, A1L),
    ([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 280, 270, A1D), ([(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)], 390, 220, A2L))]
D["tetromino-set"] = lambda s: [blocks(cells, 44, x, y, col)(s) for cells, x, y, col in (
    ([(0, 0), (0, 1), (0, 2), (0, 3)], 90, 90, A1), ([(0, 0), (0, 1), (1, 0), (1, 1)], 330, 80, A2), ([(0, 1), (1, 0), (1, 1), (1, 2)], 90, 200, "#4CB963"),
    ([(0, 0), (1, 0), (2, 0), (2, 1)], 300, 200, A1L), ([(0, 1), (0, 2), (1, 0), (1, 1)], 120, 340, A1D), ([(0, 0), (0, 1), (1, 1), (1, 2)], 290, 360, A2L))]
D["jigsaw-puzzle-piece"] = scene((puzzle, 256, 256, 1.0))
D["jigsaw-puzzle"] = scene((puzzle, 170, 170, 0.5), (puzzle, 340, 170, 0.5, {"color": A2}), (puzzle, 170, 340, 0.5, {"color": A2}), (puzzle, 340, 340, 0.5))
D["missing-puzzle-piece"] = scene((puzzle, 170, 170, 0.5), (puzzle, 340, 170, 0.5, {"color": A2}), (puzzle, 170, 340, 0.5, {"color": A2}),
                                  (puzzle, 360, 360, 0.42, {"color": LIGHT}))


@lambda f: D.__setitem__("puzzle-cube", f)
def _(s):
    cols = (C["red"], C["yellow"], C["blue"], C["green"], C["orange"], LIGHT)
    for face, (o, u, v) in enumerate((((256, 90), (60, 34), (-60, 34)), ((136, 158), (60, 34), (0, 70)), ((256, 226), (60, -34), (0, 70)))):
        for i in range(3):
            for j in range(3):
                x = o[0] + u[0] * i + v[0] * j
                y = o[1] + u[1] * i + v[1] * j
                pts = f"{x},{y} {x + u[0]},{y + u[1]} {x + u[0] + v[0]},{y + u[1] + v[1]} {x + v[0]},{y + v[1]}"
                s.F("polygon", points=pts, fill=cols[(face * 2 + i + j) % 6])


@lambda f: D.__setitem__("sliding-puzzle", f)
def _(s):
    card(s, 76, 76, 360, 360, A1D)
    for k in range(15):
        r, c = divmod(k, 4)
        s.F("rect", x=92 + c * 84, y=92 + r * 84, width=76, height=76, rx=10, fill=A1L)
        stroke_text(s, str(k + 1), 130 + c * 84, 130 + r * 84, 34, DARK, 6)


@lambda f: D.__setitem__("tower-of-hanoi", f)
def _(s):
    s.F("rect", x=50, y=400, width=412, height=40, rx=10, fill=A2)
    for x in (130, 256, 382):
        s.T(f"M{x} 400 V160", DARK, 14)
    for i, (w, c) in enumerate(((180, A1), (140, A1L), (100, A2L), (60, A1D))):
        s.F("rect", x=130 - w / 2, y=360 - i * 44, width=w, height=40, rx=16, fill=c)


D["soma-cube"] = lambda s: [P(s, blocks([(0, 0)], 1, 0, 0), 0, 0, 1)] and [
    s.F("polygon", points=f"{x},{y} {x + 60},{y - 34} {x + 120},{y} {x + 60},{y + 34}", fill=col) or
    s.F("polygon", points=f"{x},{y} {x + 60},{y + 34} {x + 60},{y + 104} {x},{y + 70}", fill=A1D) or
    s.F("polygon", points=f"{x + 60},{y + 34} {x + 120},{y} {x + 120},{y + 70} {x + 60},{y + 104}", fill=A1)
    for x, y, col in ((140, 200, A1L), (200, 234, A2L), (260, 200, A1L), (200, 164, A2L), (200, 130, A1L))]


@lambda f: D.__setitem__("burr-puzzle", f)
def _(s):
    s.F("rect", x=96, y=220, width=320, height=72, rx=8, fill=C["tan"])
    s.F("rect", x=220, y=96, width=72, height=320, rx=8, fill=C["brown"])
    s.F("rect", x=210, y=210, width=92, height=92, rx=8, fill=C["darkbrown"])


@lambda f: D.__setitem__("ring-puzzle", f)
def _(s):
    s.T("M150 200 C150 120 290 120 290 200 C290 280 150 280 150 200Z", MID, 26)
    s.T("M230 300 C230 220 370 220 370 300 C370 380 230 380 230 300Z", A2, 26)


@lambda f: D.__setitem__("cube-net", f)
def _(s):
    blocks([(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1)], 80, 96, 136, A1L)(s)
    s.M("M176 216 H256 V296 H176", A1, 8, dash="12 10")


D["mental-rotation"] = lambda s: (blocks([(0, 0), (1, 0), (2, 0), (2, 1)], 50, 90, 160, A1)(s),
                                  s.M("M220 256 C250 210 290 210 310 240 " + head(312, 244, 60, 30), DARK, 10),
                                  blocks([(0, 0), (0, 1), (0, 2), (1, 0)], 50, 320, 210, A2)(s))
D["mirror-image-puzzle"] = lambda s: (s.M("M256 60 V452", A1, 8, dash="16 12"), P(s, knight, 150, 256, 0.45), P(s, knight, 362, 256, 0.45, flip=True, color=A2))
D["paper-folding-puzzle"] = lambda s: (s.F("polygon", points="96,96 416,96 416,416", fill=LIGHT), s.F("polygon", points="96,96 96,416 416,416", fill=A1L),
                                       s.M("M96 96 L416 416", DARK, 8, dash="16 12"), s.F("circle", cx=330, cy=180, r=24, fill=DARK))
D["count-the-triangles"] = lambda s: (s.F("polygon", points="256,70 452,420 60,420", fill=LIGHT),
                                      s.M("M256 70 L256 420 M158 245 L354 245 M158 245 L256 420 L354 245", A1, 10), P(s, qmark, 420, 110, 0.2))
D["count-the-squares"] = lambda s: (s.F("rect", x=96, y=96, width=320, height=320, fill=LIGHT), grid(s, 3, color=A1, w=10), P(s, qmark, 440, 90, 0.18))
D["shape-fitting-puzzle"] = lambda s: (s.F("rect", x=70, y=70, width=372, height=200, rx=20, fill=A1L),
                                       s.F("polygon", outline=False, points="140,120 220,120 220,170 260,170 260,220 140,220", fill=DARK),
                                       [s.F("polygon", points=p, fill=c) for p, c in (("110,320 190,320 190,370 230,370 230,420 110,420", A2),
                                                                                      ("290,320 400,320 400,420 290,420", A1))])

# ---------------------------------------------------------------- optical illusions (themed)
D["impossible-triangle"] = lambda s: [s.F("polygon", points=p, fill=c) for p, c in (
    ("256,60 300,60 470,356 446,398 296,138 136,416 90,416", A1),
    ("446,398 470,356 136,356 112,398 90,416 136,416", A1L),
    ("90,416 42,416 256,60 300,60 136,356 256,356 280,398 112,398", A1D))]


@lambda f: D.__setitem__("endless-stairs", f)
def _(s):
    for i in range(12):
        a = i * 30
        x, y = arc_pt(256, 256, 150, a)
        s.F("polygon", points=f"{x - 40:.0f},{y - 20:.0f} {x + 40:.0f},{y - 20:.0f} {x + 40:.0f},{y + 10:.0f} {x - 40:.0f},{y + 10:.0f}",
            fill=A1 if i % 2 else A1L, transform=f"rotate({a + 90:.0f} {x:.0f} {y:.0f})")


D["impossible-fork"] = lambda s: (s.M("M80 160 H340 M80 256 H340 M80 352 H340", DARK, 14), s.M("M340 160 C400 160 420 208 420 208 M340 256 C400 256 420 208 420 208 "
                                                                                              "M340 256 C400 256 420 304 420 304 M340 352 C400 352 420 304 420 304", DARK, 14),
                                  s.raw(f'<ellipse cx="80" cy="160" rx="16" ry="30" fill="none" stroke="{DARK}" stroke-width="10"/>'),
                                  s.raw(f'<ellipse cx="80" cy="256" rx="16" ry="30" fill="none" stroke="{DARK}" stroke-width="10"/>'),
                                  s.raw(f'<ellipse cx="80" cy="352" rx="16" ry="30" fill="none" stroke="{DARK}" stroke-width="10"/>'))
D["impossible-cube"] = lambda s: (s.M("M120 190 H330 V400 H120 Z M200 110 H410 V320 H200 Z M120 190 L200 110 M330 190 L410 110 M330 400 L410 320 M120 400 L200 320", A1, 26),
                                  s.M("M200 320 V250 M330 190 V230", LIGHT, 34))
D["necker-cube"] = lambda s: s.M("M120 190 H330 V400 H120 Z M200 110 H410 V320 H200 Z M120 190 L200 110 M330 190 L410 110 M330 400 L410 320 M120 400 L200 320", DARK, 12)
D["rubin-vase"] = lambda s: (s.F("rect", x=60, y=60, width=392, height=392, rx=20, fill=DARK),
                             s.F("path", d="M150 60 H362 C362 110 330 130 320 160 C350 180 360 210 330 230 C360 260 350 300 320 320 C330 360 360 380 362 452 H150 "
                                           "C152 380 182 360 192 320 C162 300 152 260 182 230 C152 210 162 180 192 160 C182 130 150 110 150 60Z", fill=LIGHT))
D["duck-or-rabbit"] = lambda s: (s.F("path", d="M130 220 C130 140 250 120 320 170 C380 210 380 320 300 350 C240 370 160 340 140 290 Z", fill=LIGHT),
                                 s.F("path", d="M140 230 L40 200 L60 250 L140 260 Z", fill=A2L), s.F("circle", outline=False, cx=180, cy=220, r=12, fill=DARK),
                                 s.M("M320 180 C360 160 380 170 390 190", DARK, 8))
D["young-woman-old-woman-illusion"] = lambda s: (s.F("path", d="M200 120 C120 140 110 260 160 330 C200 380 230 420 210 460 H360 C340 400 300 360 300 300 C320 240 300 150 200 120Z", fill=DARK),
                                                 s.F("path", d="M210 160 C180 200 190 260 230 300 C250 320 260 300 250 270 C270 240 260 190 210 160Z", fill=LIGHT))
D["muller-lyer-illusion"] = lambda s: (s.M("M136 170 H376 M136 170 l40 -40 M136 170 l40 40 M376 170 l-40 -40 M376 170 l-40 40", A1, 14),
                                       s.M("M136 342 H376 M136 342 l-40 -40 M136 342 l-40 40 M376 342 l40 -40 M376 342 l40 40", A2, 14))


@lambda f: D.__setitem__("ebbinghaus-illusion", f)
def _(s):
    for cx, small, big in ((140, 18, 0), (372, 0, 1)):
        s.F("circle", cx=cx, cy=256, r=40, fill=A2)
        for a in range(0, 360, 60 if small else 72):
            x, y = arc_pt(cx, 256, 70 if small else 120, a)
            s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=18 if small else 56 * 0.6, fill=A1)


D["ponzo-illusion"] = lambda s: (s.M("M180 460 L240 60 M332 460 L272 60", DARK, 12), s.M("M220 160 H292 M220 380 H292", A2, 16))


@lambda f: D.__setitem__("cafe-wall-illusion", f)
def _(s):
    for r in range(6):
        off = (0, 20, 40, 20)[r % 4]
        for c in range(-1, 7):
            if c % 2 == 0:
                s.raw(f'<rect x="{60 + c * 64 + off}" y="{80 + r * 60}" width="64" height="56" fill="{DARK}"/>')
        s.raw(f'<path d="M60 {136 + r * 60} H452" stroke="{MID}" stroke-width="4"/>')
    s.raw(f'<rect x="60" y="80" width="392" height="356" fill="none" stroke="{LIGHT}" stroke-width="0"/>')


D["hermann-grid"] = lambda s: (s.F("rect", x=60, y=60, width=392, height=392, fill=LIGHT),
                               [s.raw(f'<rect x="{70 + c * 96}" y="{70 + r * 96}" width="80" height="80" fill="{DARK}"/>') for r in range(4) for c in range(4)])


@lambda f: D.__setitem__("rotating-snakes-illusion", f)
def _(s):
    for ring, r in enumerate((190, 140, 90)):
        for k in range(18 - ring * 4):
            a = k * 360 / (18 - ring * 4)
            x, y = arc_pt(256, 256, r, a)
            col = (A1, LIGHT, A2, DARK)[k % 4]
            s.F("ellipse", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", rx=24 - ring * 4, ry=14 - ring * 2, fill=col, transform=f"rotate({a + 90:.0f} {x:.0f} {y:.0f})")


D["zollner-illusion"] = lambda s: (s.M(" ".join(f"M{x} 70 L{x + 60} 442" for x in (80, 180, 280, 380)), DARK, 8),
                                   s.M(" ".join(f"M{x + 6 * (y - 70) / 37 - 20 + (25 if i % 2 else -25):.0f} {y - 20} l{(-40 if i % 2 else 40)} 40" for i, x in enumerate((80, 180, 280, 380)) for y in range(110, 440, 40)), A2, 5))
D["hering-illusion"] = lambda s: (s.M(" ".join(f"M256 256 L{x:.0f} {y:.0f}" for x, y in (arc_pt(256, 256, 260, a) for a in range(0, 360, 12))), MID, 3),
                                  s.M("M190 60 V452 M322 60 V452", A2, 12))
D["kanizsa-triangle"] = lambda s: ([s.F("circle", outline=False, cx=x, cy=y, r=60, fill=DARK) for x, y in ((256, 100), (110, 380), (402, 380))],
                                   s.F("polygon", outline=False, points="256,100 402,380 110,380", fill=LIGHT))


@lambda f: D.__setitem__("checker-shadow-illusion", f)
def _(s):
    for r in range(5):
        for c in range(5):
            s.raw(f'<rect x="{96 + c * 64}" y="{96 + r * 64}" width="64" height="64" fill="{"#9AA3AF" if (r + c) % 2 else "#D6DAE0"}"/>')
    s.raw('<ellipse cx="300" cy="310" rx="130" ry="90" fill="#000" fill-opacity="0.35"/>')
    s.F("circle", cx=380, cy=170, r=70, fill="#4CB963")


D["hypnotic-spiral"] = lambda s: s.M("M256 256 " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in (arc_pt(256, 256, 6 + t * 1.4, t * 6) for t in range(1, 150))), A1, 18)
D["ames-room"] = lambda s: (s.F("polygon", points="60,80 452,140 452,380 60,440", fill=A1L), s.M("M60 80 L180 200 V330 L60 440 M452 140 L330 210 V320 L452 380 M180 200 H330 M180 330 H330", DARK, 6),
                            P(s, person, 205, 300, 0.33), P(s, person, 310, 290, 0.16, shirt=A2))
D["wavy-lines-illusion"] = lambda s: [s.M(f"M60 {y} H452", DARK, 6) for y in range(100, 430, 40)] + [
    s.F("rect", outline=False, x=60 + ((y // 40) % 2) * 20 + k * 56, y=y - 16, width=28, height=32, fill=A1) for y in range(100, 430, 40) for k in range(7)]
D["spinning-dancer-illusion"] = scene((person, 256, 300, 0.9, {"pose": "cheer", "shirt": DARK, "skin": DARK, "hair": DARK}))
D["hidden-face-illusion"] = lambda s: (P(s, mountain, 256, 280, 1.0), s.F("circle", outline=False, cx=200, cy=310, r=16, fill=DARK),
                                       s.F("circle", outline=False, cx=310, cy=310, r=16, fill=DARK), s.M("M220 380 Q256 410 290 380", DARK, 10))

# ---------------------------------------------------------------- spot and find (scenes, keep)
def mini_scene(s, x0, variant=0):
    s.F("rect", x=x0, y=110, width=200, height=292, rx=16, fill=C["sky"])
    s.F("rect", outline=False, x=x0, y=330, width=200, height=72, fill=C["green"])
    s.F("circle", cx=x0 + 150, cy=170, r=30, fill=C["yellow"] if variant == 0 else C["orange"])
    s.F("polygon", points=f"{x0 + 40},{330} {x0 + 90},{260} {x0 + 140},{330}", fill=C["red"])
    if variant == 0:
        s.F("circle", cx=x0 + 50, cy=170, r=18, fill=LIGHT)


D["spot-the-difference"] = lambda s: (mini_scene(s, 40, 0), mini_scene(s, 272, 1))
D["hidden-object-puzzle"] = lambda s: (s.F("rect", x=50, y=70, width=412, height=372, rx=20, fill=C["green"]),
                                       [P(s, sprout, x, y, 0.25, pot=False) for x, y in ((120, 160), (260, 140), (390, 180), (150, 330), (300, 300), (400, 360))],
                                       P(s, key, 230, 400, 0.18), P(s, magnifier, 380, 120, 0.25))
D["odd-emoji-out"] = lambda s: [(s.F("circle", cx=120 + c * 136, cy=120 + r * 136, r=50, fill=C["yellow"]),
                                 s.M(f"M{100 + c * 136} {110 + r * 136} V{116 + r * 136} M{140 + c * 136} {110 + r * 136} V{116 + r * 136}", DARK, 8),
                                 s.M(f"M{100 + c * 136} {140 + r * 136} Q{120 + c * 136} {(160 if (r, c) != (1, 2) else 124) + r * 136} {140 + c * 136} {140 + r * 136}", DARK, 7))
                                for r in range(3) for c in range(3)]
D["find-the-mistake"] = lambda s: (P(s, clock, 256, 256, 0.85), stroke_text(s, "13", 256, 152, 40, C["red"], 7))
D["hidden-number"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=C["orange"]),
                                [s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=r, fill=C["green"] if 190 < x < 320 and 140 < y < 380 and (abs(x - 256) < 30 or y < 180 or abs(y - 256) < 26 or y > 340) else C["orange"])
                                 for x, y, r in ((256 + (i * 37) % 360 - 180, 256 + (i * 53) % 360 - 180, 10 + i % 8) for i in range(160)) if (x - 256) ** 2 + (y - 256) ** 2 < 190 ** 2])
D["hidden-letter"] = lambda s: (s.F("rect", x=60, y=60, width=392, height=392, rx=20, fill=C["cream"]), stroke_text(s, "E", 256, 256, 250, C["tan"], 40),
                                [s.F("circle", outline=False, cx=90 + (i * 61) % 340, cy=90 + (i * 97) % 340, r=8, fill=C["brown"]) for i in range(40)])
D["hidden-animal"] = lambda s: (s.F("rect", x=50, y=70, width=412, height=372, rx=20, fill=C["green"]),
                                [s.F("ellipse", cx=x, cy=y, rx=50, ry=26, fill=C["darkgreen"], transform=f"rotate({x % 60 - 30} {x} {y})") for x, y in ((120, 140), (300, 120), (400, 260), (130, 360), (260, 380), (380, 400))],
                                s.F("circle", cx=250, cy=250, r=36, fill=C["green"]), s.F("circle", outline=False, cx=238, cy=244, r=7, fill=DARK), s.F("circle", outline=False, cx=262, cy=244, r=7, fill=DARK))
D["shadow-match"] = lambda s: (P(s, star, 130, 256, 0.4), [P(s, star, 370, y, 0.22, color=DARK) for y in (110, 256, 400)],
                               P(s, heart, 370, 110, 0.2, color=DARK), s.M("M210 256 H300", A2, 10, dash="14 10"))
D["find-the-twins"] = lambda s: [P(s, heart if k in (1, 5) else star, 120 + (k % 3) * 136, 160 + (k // 3) * 190, 0.3, color=c)
                                 for k, c in enumerate((C["red"], C["orange"], C["yellow"], C["blue"], C["green"], C["orange"]))]

# ---------------------------------------------------------------- classic puzzles (scenes, themed)
D["river-crossing-puzzle"] = lambda s: (s.F("rect", outline=False, x=0, y=200, width=512, height=140, fill=A1L), s.F("rect", outline=False, x=0, y=340, width=512, height=172, fill="#9BD7A8"),
                                        s.F("path", d="M190 250 H330 L300 300 H220 Z", fill=C["brown"]), P(s, person, 260, 190, 0.18),
                                        P(s, sprout, 120, 400, 0.2, pot=False), s.F("ellipse", cx=250, cy=420, rx=40, ry=24, fill=LIGHT),
                                        s.F("ellipse", cx=380, cy=420, rx=44, ry=24, fill=MID))
D["two-doors-riddle"] = scene((door, 150, 256, 0.55, {"open_": False}), (door, 362, 256, 0.55, {"open_": False}), (qmark, 256, 90, 0.2))
D["three-switches-puzzle"] = lambda s: ([(s.F("rect", x=70 + i * 90, y=200, width=60, height=110, rx=10, fill=LIGHT), s.F("rect", x=82 + i * 90, y=220 + (0 if i == 1 else 40), width=36, height=40, rx=8, fill=A1))
                                         for i in range(3)], P(s, bulb, 400, 250, 0.4, glow=False, lit=False))
D["water-jug-puzzle"] = lambda s: [(s.F("path", d=f"M{x - w} 160 H{x + w} V400 C{x + w} 420 {x + w - 20} 430 {x + w - 40} 430 H{x - w + 40} C{x - w + 20} 430 {x - w} 420 {x - w} 400 Z", fill=LIGHT),
                                    s.F("rect", outline=False, x=x - w + 8, y=430 - lvl, width=2 * w - 16, height=lvl - 10, fill=A1L), stroke_text(s, str(v), x, 120, 40, DARK, 7))
                                   for x, w, lvl, v in ((160, 80, 120, 5), (360, 56, 200, 3))]
D["monty-hall-problem"] = lambda s: [(P(s, door, 100 + i * 156, 256, 0.45, open_=(i == 2)), stroke_text(s, str(i + 1), 100 + i * 156, 70, 40, DARK, 7)) for i in range(3)]
D["balance-scale-puzzle"] = lambda s: (P(s, scales, 256, 256, 1.0), [s.F("circle", cx=x, cy=270, r=18, fill=A2) for x in (90, 120, 150)],
                                       [s.F("circle", cx=x, cy=270, r=18, fill=A2) for x in (362, 392, 422)], P(s, qmark, 256, 380, 0.12))
D["coin-puzzle"] = lambda s: [(s.F("circle", cx=x, cy=y, r=40, fill=A2), s.F("circle", outline=False, cx=x, cy=y, r=26, fill=A2L)) for x, y in
                              ((256, 120), (206, 200), (306, 200), (156, 280), (256, 280), (356, 280), (106, 360), (206, 360), (306, 360), (406, 360))]
D["bridge-and-torch-puzzle"] = lambda s: (s.F("rect", outline=False, x=0, y=330, width=512, height=182, fill=A1L), s.F("rect", x=60, y=300, width=392, height=30, rx=6, fill=C["brown"]),
                                          [P(s, person, x, 220, 0.25, shirt=c) for x, c in ((130, A1), (200, A2), (300, A1D))], P(s, candle, 380, 220, 0.3))
D["prisoners-and-hats-puzzle"] = lambda s: [(P(s, person, 110 + i * 146, 300, 0.42, shirt=MID), s.F("path", d=f"M{80 + i * 146} 160 H{140 + i * 146} L{125 + i * 146} 100 H{95 + i * 146} Z",
                                                                                                        fill=(A1, A2, A1, A2)[i]))
                                            for i in range(3)]
D["egg-drop-puzzle"] = lambda s: (s.F("rect", x=200, y=60, width=200, height=400, rx=10, fill=A1L),
                                  [s.F("rect", outline=False, x=225 + c * 60, y=90 + r * 70, width=40, height=40, rx=4, fill=LIGHT) for r in range(5) for c in range(3)],
                                  s.F("ellipse", cx=120, cy=200, rx=36, ry=46, fill=LIGHT), s.M("M120 260 V330", DARK, 8, dash="12 10"))
D["clock-angle-puzzle"] = lambda s: (P(s, clock, 256, 256, 1.0, h=90 + 15, m=15),
                                     s.raw(f'<path d="M256 256 L256 186 A70 70 0 0 1 326 256 Z" fill="{A2}" fill-opacity="0.5"/>'))
D["chicken-or-egg"] = lambda s: (s.F("ellipse", cx=150, cy=280, rx=80, ry=104, fill=LIGHT), s.F("ellipse", cx=370, cy=300, rx=90, ry=80, fill=LIGHT),
                                 s.F("circle", cx=410, cy=200, r=44, fill=LIGHT), s.F("polygon", points="450,196 480,206 450,216", fill=A2),
                                 s.F("path", d="M400 150 C410 130 430 130 430 150 Z", fill=C["red"]), P(s, qmark, 256, 110, 0.2))
D["seven-bridges-of-konigsberg"] = lambda s: (s.F("rect", outline=False, x=0, y=180, width=512, height=60, fill=A1L), s.F("rect", outline=False, x=0, y=300, width=512, height=60, fill=A1L),
                                              s.F("ellipse", cx=200, cy=270, rx=90, ry=40, fill="#9BD7A8"),
                                              [s.F("rect", x=x, y=y, width=24, height=70, rx=4, fill=C["brown"]) for x, y in ((140, 175), (230, 175), (140, 295), (230, 295), (330, 175), (330, 295))],
                                              s.F("rect", x=290, y=258, width=90, height=24, rx=4, fill=C["brown"]))
D["wheat-and-chessboard"] = lambda s: ([s.F("rect", outline=False, x=96 + c * 40, y=96 + r * 40, width=40, height=40, fill=A1L if (r + c) % 2 else LIGHT) for r in range(8) for c in range(8)],
                                       [s.F("circle", outline=False, cx=116 + c * 40 + (k % 3 - 1) * 9, cy=116 + 7 * 40 + (k // 3 - 1) * 9, r=4, fill=A2) for c in range(4) for k in range(min(9, 2 ** c))],
                                       s.F("rect", x=96, y=96, width=320, height=320, fill="none"))
D["burning-rope-puzzle"] = lambda s: (s.M("M80 200 C160 160 300 240 430 190", C["tan"], 16), s.M("M80 320 C160 360 300 280 430 330", C["tan"], 16),
                                      P(s, candle, 80, 160, 0.2), P(s, candle, 430, 290, 0.2))
D["three-boxes-puzzle"] = lambda s: [(P(s, gift, 100 + i * 156, 290, 0.4, color=(A1, A2, A1L)[i]), stroke_text(s, "ABC"[i], 100 + i * 156, 110, 50, DARK, 8)) for i in range(3)]
D["handshake-puzzle"] = lambda s: (P(s, handshake, 256, 340, 0.5), [P(s, person, x, 200, 0.25, shirt=c) for x, c in ((90, A1), (200, A2), (312, A1D), (422, A1L))], P(s, qmark, 256, 60, 0.12))


if __name__ == "__main__":
    run("brain-teasers-logic", D, sys.argv[1:] or None)
