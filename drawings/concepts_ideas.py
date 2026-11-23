"""concepts-ideas drawings. Run: python drawings/concepts_ideas.py [ids...]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import *  # noqa: E402,F401,F403
from _parts import place as P  # noqa: E402
from draw_lib import head, run  # noqa: E402

D = {}


def draw(item_id):
    def reg(fn):
        D[item_id] = fn
        return fn
    return reg


def scene(*steps):
    """Build a drawing from (part, x, y, scale, kwargs) steps."""
    def fn(s):
        for st in steps:
            if callable(st):
                st(s)
            else:
                part, x, y, sc, *rest = st
                P(s, part, x, y, sc, **(rest[0] if rest else {}))
    return fn


# ---------------------------------------------------------------- ideas and thinking
D["idea"] = scene((bulb, 256, 256, 1.0))
D["brainstorm"] = scene((thought, 256, 220, 1.0), (bulb, 180, 220, 0.3, {"glow": False}), (bulb, 260, 190, 0.34, {"glow": False}),
                        (bulb, 340, 230, 0.3, {"glow": False}), (person, 120, 380, 0.42, {"pose": "think"}))
D["creativity"] = scene((brain, 256, 270, 0.9), lambda s: [sparkle(s, x, y, r, c) for x, y, r, c in
                                                          ((110, 110, 40, A2), (400, 100, 50, A1), (420, 390, 34, A2), (90, 380, 28, A1))])
D["imagination"] = scene((thought, 256, 210, 1.05), (rocket, 200, 220, 0.3, ), (star, 300, 200, 0.22), (person, 120, 390, 0.4, {"pose": "think"}))
D["curiosity"] = scene((magnifier, 230, 240, 0.9), (qmark, 236, 236, 0.4))
D["inspiration"] = scene((person, 220, 280, 0.75, {"pose": "cheer"}), lambda s: [sparkle(s, x, y, r) for x, y, r in ((400, 120, 50), (420, 260, 30), (90, 140, 34))],
                         (bulb, 380, 160, 0.3, {"glow": False}))
D["insight"] = scene((brain, 256, 300, 0.75), (bulb, 256, 110, 0.4))
D["thinking"] = scene((person, 220, 280, 0.8, {"pose": "think"}), (thought, 400, 120, 0.45), (qmark, 404, 110, 0.18))
D["overthinking"] = scene((person, 256, 300, 0.7, {"pose": "sad"}), lambda s: s.M(
    "M120 120 C160 60 220 140 260 80 C300 30 360 120 400 70 M100 170 C140 130 200 200 250 150 C300 100 360 190 420 140", DARK, 10))
D["decision"] = scene((signpost, 300, 256, 0.9), (person, 130, 300, 0.6, {"pose": "think"}))
D["crossroads"] = scene(lambda s: (s.F("polygon", points="200,0 312,0 312,200 512,200 512,312 312,312 312,512 200,512 200,312 0,312 0,200 200,200", fill=MID),
                                   s.M("M256 20 V180 M256 330 V500 M20 256 H180 M330 256 H500", LIGHT, 12)), (signpost, 380, 140, 0.4))
D["plan"] = scene(lambda s: (s.F("rect", x=90, y=70, width=332, height=390, rx=20, fill=LIGHT), s.F("rect", x=190, y=50, width=132, height=50, rx=14, fill=A1),
                             [s.F("circle", cx=140, cy=y, r=16, fill=A2) for y in (160, 240, 320, 400)],
                             s.M("M180 160 H380 M180 240 H350 M180 320 H370 M180 400 H320", MID, 18)))
D["strategy"] = scene((knight, 300, 280, 0.8), lambda s: s.M("M80 420 C120 320 100 220 180 160 " + head(180, 160, -40, 50), A2, 14))
D["analysis"] = scene((bars, 230, 280, 0.8, {"arrow": False}), (magnifier, 350, 210, 0.45))
D["research"] = scene((book, 220, 300, 0.75), (magnifier, 350, 200, 0.5))
D["knowledge"] = scene(lambda s: [P(s, book, 256, y, 0.7, color=c) for y, c in ((380, A1), (300, A2), (220, A1D))], (bulb, 256, 110, 0.3, {"glow": False}))
D["wisdom"] = scene((book, 256, 340, 0.8, {"color": A1D}), lambda s: [sparkle(s, 256, 120, 60), sparkle(s, 160, 160, 26, A1), sparkle(s, 356, 160, 26, A1)])
D["learning"] = scene((book, 256, 360, 0.65), (person, 256, 210, 0.5))
D["innovation"] = scene((gear, 200, 300, 0.6), (gear, 330, 210, 0.45, {"color": A2}), (bulb, 350, 360, 0.35, {"glow": False}))
D["mind-map"] = scene(lambda s: ([s.M(f"M256 256 L{x} {y}", DARK, 10) for x, y in ((100, 110), (420, 120), (90, 400), (420, 400), (256, 70))],
                                 [s.F("circle", cx=x, cy=y, r=46, fill=c) for x, y, c in ((100, 110, A2), (420, 120, A1L), (90, 400, A1L), (420, 400, A2), (256, 70, A1L))],
                                 s.F("circle", cx=256, cy=256, r=86, fill=A1)))
D["problem"] = scene((puzzle, 256, 260, 0.8, {"color": A2}), (qmark, 256, 250, 0.35, {"color": LIGHT}))
D["solution"] = scene((puzzle, 230, 260, 0.75), (key, 330, 360, 0.4))
D["problem-and-solution"] = scene((puzzle, 170, 256, 0.55, {"color": A2}), (puzzle, 360, 256, 0.55),
                                  lambda s: s.M("M230 256 H290 " + head(300, 256, 0, 36), DARK, 14))
D["connecting-the-dots"] = scene(lambda s: (s.M("M90 380 L170 160 L270 300 L360 110 L430 330", A1, 14),
                                            [s.F("circle", cx=x, cy=y, r=30, fill=A2) for x, y in ((90, 380), (170, 160), (270, 300), (360, 110), (430, 330))]))
D["focus"] = scene((target, 256, 256, 0.95))
D["distraction"] = scene((person, 256, 300, 0.7, {"pose": "think"}), lambda s: [P(s, p, x, y, 0.2, **k) for p, x, y, k in
                         ((qmark, 100, 120, {}), (heart, 400, 110, {}), (clock, 420, 300, {}), (star, 100, 300, {}))])
D["simplicity"] = scene(lambda s: (s.F("circle", cx=256, cy=256, r=150, fill=A1), s.F("circle", outline=False, cx=210, cy=200, r=40, fill=A1L)))
D["complexity"] = scene((maze, 256, 256, 1.0))
D["perspective"] = scene(lambda s: (s.F("rect", x=60, y=120, width=392, height=270, rx=30, fill=A1L),
                                    s.F("circle", cx=200, cy=256, r=60, fill=LIGHT), s.F("circle", cx=320, cy=256, r=60, fill=LIGHT),
                                    s.F("circle", outline=False, cx=210, cy=256, r=26, fill=DARK), s.F("circle", outline=False, cx=330, cy=256, r=26, fill=DARK)))
D["open-mind"] = scene((brain, 256, 300, 0.7), lambda s: [sparkle(s, x, y, 30, A2) for x, y in ((140, 110), (256, 70), (372, 110))])
D["common-sense"] = scene((brain, 256, 230, 0.7), (check_badge, 370, 380, 0.3))
D["critical-thinking"] = scene((brain, 220, 240, 0.7), (magnifier, 360, 330, 0.45))

# ---------------------------------------------------------------- success, failure and progress
D["success"] = scene((trophy, 256, 256, 1.0))
D["failure"] = scene((person, 256, 280, 0.8, {"pose": "sad", "shirt": MID}), (check_badge, 400, 120, 0.25, {"ok": False}))
D["achievement"] = scene((medal, 256, 256, 1.0))
D["victory"] = scene((person, 256, 270, 0.85, {"pose": "cheer"}), lambda s: [sparkle(s, x, y, r) for x, y, r in ((90, 120, 36), (420, 120, 40), (440, 300, 24))])
D["defeat"] = scene((person, 256, 280, 0.85, {"pose": "sad", "shirt": MID}))
D["progress"] = scene((bars, 256, 256, 1.0))
D["milestone"] = scene((road, 256, 256, 1.0), (flag, 300, 180, 0.4))
D["goal"] = scene((target, 256, 256, 1.0))
D["ambition"] = scene((mountain, 256, 300, 0.9), (flag, 270, 120, 0.3), (person, 110, 400, 0.35, {"pose": "point"}))
D["vision"] = scene((person, 150, 300, 0.7, {"pose": "point"}), (star, 400, 120, 0.35))
D["mission"] = scene((rocket, 256, 256, 0.95))
D["reaching-the-top"] = scene((mountain, 256, 300, 0.95), (person, 236, 120, 0.25, {"pose": "cheer"}), (flag, 290, 110, 0.22))
D["ladder-of-success"] = scene((ladder, 256, 260, 0.95), (star, 256, 50, 0.22))
D["steps-to-success"] = scene((stairs, 256, 280, 1.0), (flag, 400, 120, 0.35))
D["first-step"] = scene((stairs, 300, 300, 0.85, {"n": 4}), (person, 110, 300, 0.55, {"pose": "walk"}))
D["level-up"] = scene((arrow_up, 256, 256, 0.85), (star, 400, 110, 0.2), (star, 110, 140, 0.15))
D["breakthrough"] = scene((wall, 256, 260, 1.0, {"broken": True}), (rocket, 260, 250, 0.45))
D["comeback"] = scene(lambda s: s.M("M80 140 C160 420 260 420 300 300 C330 210 360 160 430 120 " + head(430, 120, -30, 60), A1, 26),
                      (star, 430, 120, 0.15))
D["setback"] = scene(lambda s: s.M("M80 380 L200 240 L280 300 L320 220 L430 400 " + head(430, 400, 58, 60), A2, 26))
D["mistake"] = scene((check_badge, 256, 256, 0.9, {"ok": False}))
D["trial-and-error"] = scene((check_badge, 160, 180, 0.4, {"ok": False}), (check_badge, 352, 180, 0.4, {"ok": False}), (check_badge, 256, 360, 0.45))
D["learning-from-mistakes"] = scene((check_badge, 150, 256, 0.35, {"ok": False}), lambda s: s.M("M220 256 H290 " + head(300, 256, 0, 36), DARK, 14),
                                    (bulb, 380, 256, 0.42, {"glow": False}))
D["second-chance"] = scene(lambda s: s.M("M370 120 A150 150 0 1 1 210 108 " + head(210, 108, 200, 56), A1, 30), (heart, 256, 270, 0.4))
D["risk"] = scene((dice, 256, 256, 0.9))
D["opportunity"] = scene((door, 256, 256, 1.0))
D["luck"] = scene(lambda s: [P(s, heart, 256 + dx, 256 + dy, 0.38, rot=r, color="#4CB963") for dx, dy, r in ((0, -84, 0), (84, 0, 90), (0, 84, 180), (-84, 0, -90))],
                  lambda s: s.T("M256 300 C270 380 300 420 330 450", "#2F8A4A", 16))
D["hard-work"] = scene((person, 256, 280, 0.8, {"pose": "carry"}), lambda s: [s.F("path", outline=False, d=f"M{x} {y} C{x} {y} {x - 10} {y + 16} {x - 10} {y + 24} C{x - 10} {y + 36} {x + 10} {y + 36} {x + 10} {y + 24} C{x + 10} {y + 16} {x} {y} {x} {y}Z", fill=A1L) for x, y in ((160, 100), (360, 90))])
D["perseverance"] = scene((mountain, 300, 300, 0.85), (person, 150, 330, 0.5, {"pose": "walk"}))
D["consistency"] = scene(lambda s: [s.F("rect", x=70 + i * 76, y=200, width=60, height=60, rx=12, fill=A1) for i in range(5)],
                         lambda s: [s.T(f"M{86 + i * 76} 230 L{98 + i * 76} 244 L{116 + i * 76} 218", LIGHT, 10) for i in range(5)])
D["discipline"] = scene((clock, 180, 220, 0.5), (dumbbell, 330, 360, 0.55))
D["self-improvement"] = scene((stairs, 256, 300, 0.9), (person, 330, 130, 0.35, {"pose": "walk"}))
D["growth"] = scene((sprout, 256, 256, 1.0))
D["decline"] = scene((arrow_down, 256, 256, 0.85))
D["potential"] = scene(lambda s: (s.F("path", d="M150 330 H362 L338 450 H174 Z", fill=A2), s.F("rect", x=134, y=310, width=244, height=40, rx=10, fill=A2)),
                       lambda s: s.F("ellipse", cx=256, cy=300, rx=40, ry=26, fill=A1), lambda s: sparkle(s, 256, 170, 60))
D["talent"] = scene((star, 256, 256, 0.95))
D["skill"] = scene((gear, 256, 256, 0.85), (check_badge, 256, 256, 0.3))
D["practice"] = scene((dumbbell, 256, 256, 1.0))
D["excellence"] = scene((star, 256, 230, 0.6), (medal, 256, 340, 0.45))
D["quality"] = scene((check_badge, 256, 256, 0.6), lambda s: s.F("polygon", points=__import__("draw_lib").star_pts(256, 256, 210, 190, 20), fill="none"))
D["competition"] = scene((person, 160, 290, 0.6, {"pose": "walk"}), (person, 352, 290, 0.6, {"pose": "walk", "shirt": A2}))
D["rivalry"] = scene((knight, 160, 280, 0.6), (knight, 352, 280, 0.6, {"color": A2}), lambda s: s.M("M220 140 L292 210 M292 140 L220 210", DARK, 14))
D["challenge"] = scene((mountain, 256, 280, 1.0))
D["obstacle"] = scene((wall, 300, 270, 0.75), (person, 110, 310, 0.5, {"pose": "think"}))
D["overcoming-obstacles"] = scene((wall, 256, 330, 0.6), (person, 256, 160, 0.45, {"pose": "cheer"}))
D["shortcut"] = scene(lambda s: (s.M("M90 420 C90 120 420 420 420 110", MID, 34), s.M("M90 420 L420 110 " + head(420, 110, -43, 60), A2, 20)))
D["journey"] = scene((road, 256, 256, 1.0), (mountain, 256, 90, 0.3))
D["turning-point"] = scene(lambda s: s.M("M100 420 V260 C100 180 160 140 240 140 H420 " + head(420, 140, 0, 60), A1, 30))
D["rock-bottom"] = scene(lambda s: (s.F("rect", x=60, y=400, width=392, height=60, rx=10, fill=MID)), (person, 256, 270, 0.65, {"pose": "sad"}))
D["progress-plateau"] = scene(lambda s: s.M("M80 400 L200 220 H340 V220 L360 220 H430", A1, 28))
D["finish-line"] = scene((finish_banner, 256, 256, 1.0))
D["new-beginning"] = scene(lambda s: (s.F("path", d="M40 400 H472 V460 H40Z", fill=A1L), s.F("circle", cx=256, cy=400, r=120, fill=A2)),
                           lambda s: s.F("rect", outline=False, x=40, y=404, width=432, height=60, fill=A1L), (sprout, 256, 300, 0.5, {"pot": False}))


# ---------------------------------------------------------------- values and virtues
from _parts2 import *  # noqa: E402,F401,F403
from draw_lib import star_pts  # noqa: E402


def arrow_line(d, x, y, a, color=DARK, w=14, L=40):
    return lambda s: s.M(d + " " + head(x, y, a, L), color, w)


D["patience"] = scene((hourglass, 256, 256, 0.95))
D["gratitude"] = scene((hands_heart, 256, 256, 1.0))
D["honesty"] = scene((person, 256, 280, 0.8, {"pose": "stand"}), (check_badge, 400, 120, 0.25))
D["truth"] = scene((magnifier, 256, 256, 0.9), (check_badge, 230, 230, 0.33))
D["kindness"] = scene((person, 170, 290, 0.65), (person, 340, 300, 0.55, {"shirt": A2, "pose": "carry"}), (heart, 256, 110, 0.25))
D["generosity"] = scene((gift, 256, 300, 0.8), (heart, 256, 90, 0.22))
D["respect"] = scene((person, 160, 290, 0.65), (person, 352, 290, 0.65, {"shirt": A2}), (heart, 256, 120, 0.18, {"color": A1}))
D["responsibility"] = scene((person, 256, 300, 0.75, {"pose": "carry"}), (globe, 256, 110, 0.3))
D["trust"] = scene((handshake, 256, 256, 1.0))
D["loyalty"] = scene((shield, 256, 256, 0.95), (heart, 256, 250, 0.4))
D["courage"] = scene((shield, 256, 256, 0.9), lambda s: s.F("polygon", points="290,120 200,270 250,270 220,400 320,240 268,240", fill=A2))
D["humility"] = scene((person, 256, 300, 0.8, {"pose": "sad", "shirt": A1}), (sprout, 400, 380, 0.3, {"pot": False}))
D["forgiveness"] = scene((handshake, 256, 300, 0.8), (heart, 256, 110, 0.25))
D["compassion"] = scene((hands_heart, 256, 256, 1.0, {"color": A1}))
D["fairness"] = scene((scales, 256, 256, 1.0))
D["integrity"] = scene((shield, 256, 256, 0.95, {"check": True}))
D["sincerity"] = scene((heart, 256, 256, 0.85), (check_badge, 256, 250, 0.25))
D["modesty"] = scene((person, 256, 290, 0.8, {"shirt": MID}))
D["contentment"] = scene((person, 256, 300, 0.75, {"pose": "sit"}), (sun, 410, 100, 0.3))
D["hope"] = scene((candle, 256, 256, 1.0))
D["friendship"] = scene((person, 170, 290, 0.65, {"pose": "cheer"}), (person, 342, 290, 0.65, {"pose": "cheer", "shirt": A2}), (heart, 256, 100, 0.2))
D["unity"] = scene((chain, 256, 256, 1.0))
D["peace"] = scene((dove, 256, 256, 1.0))
D["equality"] = scene((seesaw, 256, 256, 1.0, {"left": (person, 0.35), "right": (person, 0.35, {"shirt": A2})}))
D["freedom"] = scene(lambda s: [P(s, dove, x, y, sc) for x, y, sc in ((300, 200, 0.7), (130, 330, 0.4), (420, 380, 0.3))])
D["diversity"] = scene((group, 256, 256, 1.0, {"shirts": (A1, A2, "#4CB963")}))
D["inclusion"] = scene((group, 256, 256, 1.0), lambda s: s.T("M100 460 C180 500 332 500 412 460", A2, 16))
D["sharing"] = scene((person, 160, 290, 0.6), (person, 352, 290, 0.6, {"shirt": A2}), (gift, 256, 330, 0.3))
D["helping-others"] = scene((hands_heart, 256, 300, 0.7), (person, 256, 110, 0.3))
D["volunteering"] = scene((person, 256, 290, 0.8, {"shirt": A2}), (heart, 256, 250, 0.15, {"color": LIGHT}))
D["self-control"] = scene((brain, 256, 230, 0.7), (padlock, 256, 400, 0.3))
D["punctuality"] = scene((clock, 256, 256, 1.0, {"h": 270, "m": 0}))
D["cleanliness"] = scene(lambda s: [sparkle(s, x, y, r, c) for x, y, r, c in ((256, 256, 140, A1L), (380, 120, 50, A2), (120, 380, 40, A2))])
D["moderation"] = scene((scales, 256, 256, 0.95))
D["balance"] = scene((seesaw, 256, 256, 1.0, {"left": (star, 0.3), "right": (heart, 0.3)}))
D["good-manners"] = scene((person, 256, 290, 0.8), lambda s: sparkle(s, 400, 120, 40))
D["keeping-promises"] = scene((handshake, 256, 280, 0.8), (check_badge, 256, 100, 0.22))
D["role-model"] = scene((person, 256, 300, 0.75, {"pose": "cheer"}), (star, 256, 70, 0.18))

# ---------------------------------------------------------------- teamwork
D["teamwork"] = scene((puzzle, 180, 200, 0.4), (puzzle, 330, 200, 0.4, {"color": A2}), (group, 256, 330, 0.7))
D["collaboration"] = scene((gear, 190, 256, 0.55), (gear, 330, 256, 0.45, {"color": A2}))
D["leadership"] = scene((person, 256, 270, 0.7, {"pose": "point"}), (person, 110, 360, 0.4, {"shirt": MID}), (person, 400, 360, 0.4, {"shirt": MID}), (flag, 430, 120, 0.3))
D["partnership"] = scene((handshake, 256, 256, 1.0, {"c2": A1D}))
D["community"] = scene((group, 256, 290, 0.9), (heart, 256, 90, 0.2))
D["support"] = scene((person, 256, 220, 0.5, {"pose": "cheer"}), (hands_heart, 256, 380, 0.6, {"color": A1}))
D["mentorship"] = scene((person, 190, 280, 0.8, {"pose": "point"}), (person, 380, 330, 0.5, {"shirt": A2}))
D["networking"] = scene(lambda s: ([s.M(f"M{a} {b} L{c} {d}", DARK, 8) for a, b, c, d in ((256, 256, 100, 120), (256, 256, 412, 120), (256, 256, 100, 392), (256, 256, 412, 392), (100, 120, 412, 120))],
                                    [P(s, person, x, y, 0.22, shirt=c) for x, y, c in ((100, 150, A2), (412, 150, A2), (100, 420, A1D), (412, 420, A1D), (256, 290, A1))]))
D["conflict"] = scene((person, 150, 290, 0.6), (person, 362, 290, 0.6, {"shirt": A2}), lambda s: s.F("polygon", points=star_pts(256, 120, 70, 30, 8), fill=A2))
D["agreement"] = scene((handshake, 256, 300, 0.85), (check_badge, 256, 100, 0.2))
D["disagreement"] = scene((person, 150, 290, 0.6), (person, 362, 290, 0.6, {"shirt": A2}), (check_badge, 150, 80, 0.15), (check_badge, 362, 80, 0.15, {"ok": False}))
D["compromise"] = scene((puzzle, 200, 256, 0.5), (puzzle, 330, 256, 0.5, {"color": A2}), arrow_line("M140 400 H230", 240, 400, 0), arrow_line("M372 400 H282", 272, 400, 180))
D["negotiation"] = scene((person, 130, 300, 0.55), (person, 382, 300, 0.55, {"shirt": A2}), (scales, 256, 220, 0.45))
D["feedback"] = scene(lambda s: (P(s, thought, 180, 200, 0.6), P(s, thought, 340, 300, 0.55, color=A1L)), (star, 180, 190, 0.18), (check_badge, 340, 290, 0.15))
D["influence"] = scene((megaphone, 256, 256, 0.95))
D["power"] = scene((crown, 256, 256, 0.95))
D["delegation"] = scene((person, 150, 290, 0.6, {"pose": "point"}), (checklist, 380, 260, 0.45))
D["listening"] = scene((ear, 256, 256, 0.95))
D["peer-pressure"] = scene((person, 256, 330, 0.55, {"pose": "sad", "shirt": A2}), (person, 110, 240, 0.4, {"pose": "point", "shirt": MID}),
                           (person, 402, 240, 0.4, {"pose": "point", "shirt": MID}, ), (person, 256, 130, 0.35, {"shirt": MID}))
D["standing-out"] = scene((person, 120, 300, 0.45, {"shirt": MID}), (person, 392, 300, 0.45, {"shirt": MID}), (person, 256, 270, 0.65, {"shirt": A2, "pose": "cheer"}))
D["fitting-in"] = scene(lambda s: [P(s, person, x, 300, 0.45, shirt=A1) for x in (110, 256, 402)])

# ---------------------------------------------------------------- time, habits and productivity
D["time-management"] = scene((clock, 200, 220, 0.6), (checklist, 360, 330, 0.45))
D["productivity"] = scene((gear, 220, 280, 0.6), (bars, 350, 260, 0.4, {"arrow": False}), (check_badge, 400, 110, 0.18))
D["deadline"] = scene((calendar, 230, 280, 0.75), (clock, 400, 140, 0.3))
D["procrastination"] = scene((person, 256, 320, 0.6, {"pose": "sit"}), (clock, 400, 120, 0.3), (checklist, 110, 140, 0.25, {"done": 0}))
D["multitasking"] = scene((person, 256, 300, 0.7, {"pose": "cheer"}), (clock, 110, 110, 0.18), (book, 400, 110, 0.2), (cup, 410, 290, 0.18), (checklist, 100, 300, 0.18))
D["taking-a-break"] = scene((cup, 256, 256, 0.9))
D["work-life-balance"] = scene((seesaw, 256, 256, 1.0, {"left": (checklist, 0.3), "right": (heart, 0.3)}))
D["daily-routine"] = scene((sun, 140, 150, 0.4), (moon, 380, 150, 0.4), (clock, 256, 340, 0.45))
D["priorities"] = scene(lambda s: [s.F("rect", x=120, y=y, width=272, height=80, rx=16, fill=c) for y, c in ((100, A2), (210, A1), (320, A1L))],
                        lambda s: [s.F("circle", cx=160, cy=140 + i * 110, r=22, fill=LIGHT) for i in range(3)])
D["to-do-list"] = scene((checklist, 256, 256, 1.0))
D["efficiency"] = scene((gear, 256, 256, 0.8), lambda s: s.F("polygon", points="280,170 210,270 250,270 230,350 300,250 262,250", fill=A2))
D["slow-and-steady"] = scene((road, 256, 256, 1.0), lambda s: s.F("ellipse", cx=256, cy=380, rx=70, ry=50, fill="#4CB963"))
D["early-bird"] = scene((sun, 256, 330, 0.7), lambda s: s.F("rect", outline=False, x=0, y=360, width=512, height=152, fill=A1L), (dove, 300, 150, 0.4))
D["night-owl"] = scene((owl, 256, 290, 0.8), (moon, 410, 100, 0.3))
D["wasting-time"] = scene((hourglass, 256, 256, 0.7), lambda s: s.M("M100 120 C160 140 200 100 240 130 M300 400 C340 420 380 390 420 410", MID, 12))
D["saving-time"] = scene((clock, 256, 256, 0.85), (check_badge, 390, 390, 0.22))
D["good-habit"] = scene((checklist, 256, 256, 0.9, {"done": 3}))
D["bad-habit"] = scene((checklist, 256, 256, 0.85, {"done": 0}), (check_badge, 380, 390, 0.25, {"ok": False}))
D["habit-streak"] = scene((calendar, 256, 256, 0.95, {"mark": False}), lambda s: [s.M(f"M{x - 10} {y} L{x} {y + 12} L{x + 18} {y - 12}", A2, 10)
                                                                                   for x, y in ((142, 252), (204, 252), (266, 252), (328, 252), (390, 252))])
D["small-steps"] = scene((stairs, 256, 300, 0.9, {"n": 8}))
D["the-past"] = scene((clock, 256, 256, 0.85), arrow_line("M150 440 A190 190 0 0 1 100 200", 100, 200, -100, A2, 18))
D["the-present"] = scene((gift, 256, 256, 0.95))
D["the-future"] = scene((rocket, 256, 256, 0.9), (star, 420, 100, 0.15), (star, 100, 140, 0.1))
D["change"] = scene(arrow_line("M380 160 A150 150 0 0 0 140 220", 140, 220, 120, A1, 28, 60), arrow_line("M132 352 A150 150 0 0 0 372 292", 372, 292, -60, A2, 28, 60))
D["transformation"] = scene((butterfly, 256, 256, 1.0))

# ---------------------------------------------------------------- mindsets and abstract states
D["growth-mindset"] = scene((brain, 256, 300, 0.75), (sprout, 256, 110, 0.35, {"pot": False}))
D["fixed-mindset"] = scene((brain, 256, 256, 0.8), (padlock, 256, 300, 0.3))
D["positive-thinking"] = scene((sun, 256, 256, 0.9))
D["negative-thinking"] = scene((cloud, 256, 200, 0.9, {"color": MID}), lambda s: s.M("M180 360 V420 M250 360 V440 M320 360 V420", A1, 14))
D["comfort-zone"] = scene(lambda s: s.F("circle", cx=256, cy=256, r=200, fill=A1L), (person, 256, 300, 0.55, {"pose": "sit"}), (star, 440, 80, 0.12))
D["pressure"] = scene((person, 256, 340, 0.55, {"pose": "sad"}), arrow_line("M256 40 V150", 256, 160, 90, A2, 22, 50), arrow_line("M40 300 H130", 140, 300, 0, A2, 22, 50),
                      arrow_line("M472 300 H382", 372, 300, 180, A2, 22, 50))
D["confidence"] = scene((person, 256, 280, 0.85, {"pose": "cheer", "shirt": A2}))
D["self-doubt"] = scene((person, 256, 300, 0.7, {"pose": "think"}), (qmark, 400, 120, 0.3))
D["chaos"] = scene(lambda s: s.M("M100 300 C80 160 300 100 340 200 C380 300 160 380 200 260 C230 170 420 180 420 320 C420 420 220 440 140 380", A2, 18))
D["order"] = scene(lambda s: [s.F("rect", x=100 + c * 110, y=100 + r * 110, width=90, height=90, rx=16, fill=A1 if (r + c) % 2 == 0 else A1L) for r in range(3) for c in range(3)])
D["harmony"] = scene(lambda s: (s.F("circle", cx=256, cy=256, r=190, fill=A1),
                                s.F("path", d="M256 66 A95 95 0 0 1 256 256 A95 95 0 0 0 256 446 A190 190 0 0 1 256 66Z", fill=LIGHT),
                                s.F("circle", outline=False, cx=256, cy=161, r=28, fill=A1), s.F("circle", outline=False, cx=256, cy=351, r=28, fill=LIGHT)))
D["opposites"] = scene((sun, 160, 256, 0.55), (moon, 360, 256, 0.55))
D["security"] = scene((shield, 256, 256, 0.95, {"check": True}))
D["privacy"] = scene((eye, 256, 200, 0.6), (padlock, 256, 380, 0.4))
D["secret"] = scene((padlock, 256, 256, 0.9))
D["uncertainty"] = scene((signpost, 256, 256, 0.9), (qmark, 400, 110, 0.25))
D["possibility"] = scene((door, 256, 256, 1.0), lambda s: sparkle(s, 256, 300, 40))
D["impossible"] = scene((mountain, 256, 280, 1.0), (check_badge, 400, 100, 0.2, {"ok": False}))
D["limits"] = scene(lambda s: (s.M("M60 150 H452", A2, 18, dash="40 26"), s.F("rect", outline=False, x=60, y=420, width=392, height=40, fill=MID)), (person, 256, 300, 0.55, {"pose": "cheer"}))
D["minimalism"] = scene(lambda s: (s.F("rect", x=60, y=60, width=392, height=392, rx=30, fill=LIGHT), s.F("circle", cx=256, cy=256, r=50, fill=A1)))
D["the-big-picture"] = scene((globe, 256, 256, 0.75), (magnifier, 400, 400, 0.3))
D["hidden-truth"] = scene((iceberg, 256, 256, 1.0))

# ---------------------------------------------------------------- cause and effect
D["cause-and-effect"] = scene((domino, 140, 256, 0.6, {"rot": -30}), arrow_line("M230 256 H300", 310, 256, 0, DARK, 16), (star, 400, 256, 0.3))
D["domino-effect"] = scene(lambda s: [P(s, domino, x, 256, 0.6, rot=r, color=c) for x, r, c in ((100, -60, A1L), (200, -40, LIGHT), (300, -18, A1L), (400, 0, LIGHT))])
D["snowball-effect"] = scene(lambda s: s.F("polygon", outline=False, points="0,512 512,512 512,300", fill=A1L), (snowball, 120, 220, 0.25), (snowball, 250, 280, 0.45), (snowball, 390, 330, 0.65))
D["ripple-effect"] = scene((ripple, 256, 256, 1.0))
D["butterfly-effect"] = scene((butterfly, 180, 180, 0.5), arrow_line("M260 280 C300 330 330 340 360 340", 370, 340, 0, DARK, 12), (cloud, 400, 360, 0.35, {"color": MID}))
D["tipping-point"] = scene((seesaw, 256, 256, 1.0, {"tilt": -14, "right": (star, 0.3)}))
D["vicious-cycle"] = scene(lambda s: [arrow_line(f"M{a[0]:.0f} {a[1]:.0f} A150 150 0 0 1 {b[0]:.0f} {b[1]:.0f}", b[0], b[1], ang + 120, A2, 24, 50)(s)
                                      for ang in (-90, 30, 150) for a, b in [(arc_pt(256, 256, 150, ang), arc_pt(256, 256, 150, ang + 90))]],
                           (check_badge, 256, 256, 0.25, {"ok": False}))
D["virtuous-cycle"] = scene(lambda s: [arrow_line(f"M{a[0]:.0f} {a[1]:.0f} A150 150 0 0 1 {b[0]:.0f} {b[1]:.0f}", b[0], b[1], ang + 120, A1, 24, 50)(s)
                                       for ang in (-90, 30, 150) for a, b in [(arc_pt(256, 256, 150, ang), arc_pt(256, 256, 150, ang + 90))]],
                            (check_badge, 256, 256, 0.25))
D["bottleneck"] = scene((bottle, 256, 256, 0.95))
D["feedback-loop"] = scene(lambda s: (arrow_line("M120 200 C120 80 392 80 392 200", 392, 210, 90, A1, 24, 50)(s), arrow_line("M392 312 C392 432 120 432 120 312", 120, 302, -90, A2, 24, 50)(s)))
D["side-effect"] = scene(arrow_line("M80 256 H400", 410, 256, 0, A1, 26, 60), arrow_line("M240 256 C260 330 300 380 380 400", 390, 402, 10, A2, 16, 40))
D["trade-off"] = scene((scales, 256, 256, 1.0), (heart, 136, 290, 0.16), (star, 376, 290, 0.16))
D["input-and-output"] = scene(arrow_line("M40 256 H150", 160, 256, 0, A2, 22, 44), (gear, 256, 256, 0.5), arrow_line("M360 256 H460", 470, 256, 0, A1, 22, 44))


if __name__ == "__main__":
    run("concepts-ideas", D, sys.argv[1:] or None)
