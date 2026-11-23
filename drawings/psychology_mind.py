"""psychology-mind drawings. Run: python drawings/psychology_mind.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, bug, eye, quad, shade, snake  # noqa: E402
from _parts import (A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, SKIN, bars, book, brain, bulb, clock, cloud, door, gear, heart,  # noqa: E402,F401
                    ladder, magnifier, mountain, person, puzzle, qmark, sparkle, sprout, star, stairs, thought, wall)
from _parts import place as P  # noqa: E402
from _parts2 import calendar, checklist, chain, crown, dove, eye as eye_part, gift, group, iceberg, megaphone, moon, padlock, scales, sun  # noqa: E402,F401
from draw_lib import C, INK, arc_pt, head, run, star_pts, stroke_text  # noqa: E402

D = {}


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def scene(*steps):
    def fn(s):
        for st in steps:
            if callable(st):
                st(s)
            else:
                part, x, y, sc, *rest = st
                P(s, part, x, y, sc, **(rest[0] if rest else {}))
    return fn


def head_side(s, inner=None, color=A1L):
    s.F("path", d="M150 460 V380 C110 360 90 300 100 240 C110 140 190 70 290 80 C380 90 430 160 420 240 C416 280 440 300 430 320 L410 330 C410 360 400 380 370 380 H330 V460Z", fill=color)
    if inner:
        inner(s)


def in_head(part, x=260, y=220, sc=0.55, **kw):
    return lambda s: head_side(s, lambda s: P(s, part, x, y, sc, **kw))


def arrow(d, x, y, a, color=DARK, w=12, L=34):
    return lambda s: s.M(d + " " + head(x, y, a, L), color, w)


def bed(s, x=256, y=330, sc=1.0, sleeper=True):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -330)")
    s.F("rect", x=60, y=300, width=392, height=80, rx=16, fill=A1L)
    s.F("rect", x=60, y=230, width=40, height=170, rx=10, fill=A1D)
    if sleeper:
        s.F("rect", x=110, y=270, width=110, height=40, rx=18, fill=LIGHT)
        s.F("circle", cx=170, cy=262, r=34, fill=SKIN)
        s.M("M160 260 Q170 268 180 260", INK, 5)
        s.F("path", d="M200 290 H440 V340 H200Z", fill=A1)
    s.T("M80 380 V420 M432 380 V420", A1D, 14)
    s.close()


# ---------------------------------------------------------------- mind and brain
D["mind"] = in_head(brain, 262, 220, 0.5)
D["brain-with-gears"] = scene((brain, 256, 270, 0.85), (gear, 210, 240, 0.25), (gear, 300, 290, 0.2, {"color": A2}))
D["left-brain-right-brain"] = scene(lambda s: (s.F("path", d="M252 104 C220 78 162 86 150 136 C102 138 76 190 98 232 C66 262 78 322 128 334 C138 384 196 404 238 382 C246 396 252 400 252 400Z", fill=A1L),
                                               s.F("path", d="M260 104 C292 78 350 86 362 136 C410 138 436 190 414 232 C446 262 434 322 384 334 C374 384 316 404 274 382 C266 396 260 400 260 400Z", fill=A2L)),
                                    (gear, 180, 240, 0.2), lambda s: [sparkle(s, x, y, 22) for x, y in ((320, 220), (350, 290))])
D["left-brain"] = scene(lambda s: s.F("path", d="M252 104 C220 78 162 86 150 136 C102 138 76 190 98 232 C66 262 78 322 128 334 C138 384 196 404 238 382 C246 396 252 400 252 400Z", fill=A1L), (gear, 180, 250, 0.25),
                        lambda s: stroke_text(s, "123", 180, 330, 40, A1D, 6))
D["right-brain"] = scene(lambda s: s.F("path", d="M260 104 C292 78 350 86 362 136 C410 138 436 190 414 232 C446 262 434 322 384 334 C374 384 316 404 274 382 C266 396 260 400 260 400Z", fill=A2L),
                         lambda s: [sparkle(s, x, y, r) for x, y, r in ((330, 220, 30), (300, 300, 20), (370, 300, 16))])
D["conscious-mind"] = in_head(bulb, 262, 220, 0.4)
D["subconscious-mind"] = scene((iceberg, 256, 256, 1.0), (brain, 256, 400, 0.25))
D["iceberg-of-the-mind"] = scene((iceberg, 256, 256, 1.0))
D["neurons-firing"] = scene(lambda s: [s.M(f"M{a} {b} L{c} {d}", A1, 8) for a, b, c, d in ((120, 140, 256, 256), (256, 256, 400, 160), (256, 256, 140, 380), (256, 256, 380, 380))],
                            lambda s: [s.F("circle", cx=x, cy=y, r=r, fill=c) for x, y, r, c in ((256, 256, 50, A2), (120, 140, 30, A1L), (400, 160, 30, A1L), (140, 380, 30, A1L), (380, 380, 30, A1L))],
                            lambda s: [sparkle(s, x, y, 18) for x, y in ((190, 200), (330, 210), (200, 320))])
D["brain-waves"] = scene((brain, 256, 170, 0.5), lambda s: [s.M(f"M60 {y} " + " ".join(f"Q{60 + k * 40 + 20} {y + (-30 if k % 2 else 30)} {60 + (k + 1) * 40} {y}" for k in range(10)), c, 8) for y, c in ((340, A1), (410, A2))])
D["neuroplasticity"] = scene((brain, 256, 256, 0.9), lambda s: s.M("M180 240 C220 200 290 300 340 240", A2, 10), lambda s: [s.F("circle", cx=x, cy=y, r=12, fill=A2) for x, y in ((180, 240), (340, 240))])
D["dopamine"] = scene(lambda s: s.M("M120 300 L180 200 L280 200 L340 300 L280 400 L180 400Z M280 200 L360 140 L440 160", A1, 12), lambda s: [s.F("circle", cx=x, cy=y, r=14, fill=A2) for x, y in ((360, 140), (440, 160))],
                      (heart, 400, 400, 0.15))
D["serotonin"] = scene(lambda s: s.M("M100 300 L150 220 L240 220 L290 300 L240 380 L150 380Z M240 220 L300 160 L380 180 M290 300 L380 300", A2, 12), (sun, 410, 380, 0.15))
D["brain-chemicals"] = scene((brain, 256, 300, 0.6), lambda s: [s.F("circle", cx=x, cy=y, r=r, fill=c) for x, y, r, c in ((140, 120, 26, A1), (220, 80, 20, A2), (330, 100, 30, A1L), (400, 160, 18, A2))])

# ---------------------------------------------------------------- memory
D["memory"] = in_head(lambda s: [s.F("rect", x=170 + c * 60, y=170 + r * 60, width=50, height=50, rx=8, fill=A1 if (r + c) % 2 else A2) for r in range(3) for c in range(3)], 262, 200, 0.6)
D["short-term-memory"] = scene((brain, 220, 260, 0.7), (clock, 400, 140, 0.25, {"h": 0, "m": 5}))
D["long-term-memory"] = scene((brain, 220, 260, 0.7), (book, 400, 380, 0.3))
D["memory-palace"] = scene(lambda s: (s.F("rect", x=100, y=240, width=312, height=200, fill=A1L), s.F("polygon", points="80,250 256,120 432,250", fill=A1),
                                      [s.F("rect", x=x, y=300, width=50, height=80, rx=6, fill=LIGHT) for x in (140, 230, 320)]), lambda s: [sparkle(s, x, y, 18) for x, y in ((165, 280), (255, 280), (345, 280))])
D["forgetting-curve"] = scene(lambda s: (s.M("M80 100 V420 H440", DARK, 10), s.M("M90 120 C140 300 260 360 430 390", A2, 12)))
D["forgetting"] = in_head(qmark, 262, 210, 0.4)
D["false-memory"] = scene((thought, 256, 220, 0.9), (puzzle, 256, 210, 0.3, {"color": A2}), lambda s: s.M("M200 160 L320 260 M320 160 L200 260", A2, 10))
D["muscle-memory"] = scene((brain, 160, 180, 0.4), arrow("M230 200 C290 230 320 280 330 320", 334, 330, 70), lambda s: s.T("M260 440 L330 360 L420 300", SKIN, 50))
D["amnesia"] = in_head(lambda s: (s.F("rect", x=180, y=160, width=160, height=120, rx=16, fill=LIGHT), qmark(s)), 262, 220, 0.6)
D["flashbulb-memory"] = scene((brain, 220, 280, 0.6), lambda s: s.F("polygon", points=star_pts(380, 140, 80, 34, 10), fill="#FFE38A"))
D["remembering"] = scene((person, 200, 300, 0.7, {"pose": "think"}), (thought, 390, 120, 0.4), (heart, 392, 112, 0.1))

# ---------------------------------------------------------------- sleep and dreams
D["sleep-cycle"] = scene(lambda s: s.M("M60 150 L120 300 L180 380 L240 300 L300 380 L360 220 L420 300 L460 180", A1, 12), (moon, 420, 90, 0.15))
D["rem-sleep"] = scene(bed, lambda s: s.M("M150 200 Q170 180 190 200", A2, 8), (thought, 380, 140, 0.35))
D["deep-sleep"] = scene(bed, lambda s: (s.M("M270 180 H300 L270 210 H300 M320 120 H360 L320 160 H360", A1, 8)))
D["dream"] = scene(bed, (thought, 360, 140, 0.55), (star, 340, 130, 0.12), (moon, 400, 120, 0.1))
D["nightmare"] = scene(bed, (thought, 360, 140, 0.55, {"color": MID}), lambda s: s.F("polygon", points="330,100 310,150 340,150 320,190 370,130 340,130", fill=DARK))
D["lucid-dream"] = scene(bed, (thought, 360, 140, 0.55, {"color": A2L}), (bulb, 360, 130, 0.12, {"glow": False}))
D["dream-bubble"] = scene((thought, 256, 220, 1.0), (moon, 220, 200, 0.2), (star, 300, 210, 0.12))
D["sleepwalking"] = scene((person, 256, 270, 0.85, {"pose": "walk", "shirt": A1L}), (moon, 420, 90, 0.15), lambda s: s.M("M300 140 H330 L300 170 H330", A1, 8))
D["sleep-paralysis"] = scene(bed, lambda s: s.F("path", d="M330 140 C330 80 410 80 410 140 V230 L390 210 L370 230 L350 210 L330 230Z", fill=MID))
D["power-nap"] = scene((person, 256, 300, 0.75, {"pose": "sit"}), (clock, 410, 110, 0.22, {"h": 30, "m": 20}), lambda s: s.M("M300 160 H330 L300 190 H330", A1, 8))
D["circadian-rhythm"] = scene(lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=A1L), s.F("path", d="M56 256 A200 200 0 0 1 456 256Z", fill="#FFE8C0")), (sun, 256, 150, 0.2), (moon, 256, 360, 0.2),
                              lambda s: s.M("M256 256 L340 200", DARK, 10))
def sheep_small(s, x, y):
    s.open(transform=f"translate({x} {y}) scale(0.32) translate(-256 -256)")
    quad(s, body="#3A3A44", wool=WHITE, head_c="#3A3A44", leg_c="#3A3A44", snout="round", snout_c="#5A5A66", ears="side", tail="short", tail_c=WHITE, head_r=46, leg=0.8)
    s.close()


D["counting-sheep"] = scene(lambda s: [sheep_small(s, x, y) for x, y in ((140, 340), (280, 260), (400, 160))], lambda s: s.M("M80 410 H460", MID, 8))

# ---------------------------------------------------------------- personality
D["personality"] = scene((person, 256, 300, 0.8, {"pose": "cheer"}), lambda s: [sparkle(s, x, y, 22, c) for x, y, c in ((100, 140, A1), (420, 140, A2))])
D["personality-types"] = scene(lambda s: [P(s, person, x, 300, 0.45, shirt=c) for x, c in ((90, A1), (200, A2), (312, "#4CB963"), (422, "#B880E8"))])
D["introvert"] = scene((person, 256, 300, 0.65, {"pose": "sit"}), (book, 256, 360, 0.25), lambda s: s.raw(f'<circle cx="256" cy="290" r="200" fill="none" stroke="{A1L}" stroke-width="10" stroke-dasharray="20 14"/>'))
D["extrovert"] = scene((person, 256, 290, 0.75, {"pose": "cheer", "shirt": A2}), (megaphone, 410, 120, 0.25), lambda s: [sparkle(s, x, y, 18) for x, y in ((90, 140), (110, 330))])
D["ambivert"] = scene((person, 180, 300, 0.55, {"pose": "sit"}), (person, 340, 290, 0.55, {"pose": "cheer", "shirt": A2}), lambda s: s.M("M256 120 V440", MID, 6, dash="16 12"))
D["optimist"] = scene((person, 220, 290, 0.75, {"pose": "cheer"}), (sun, 410, 110, 0.25))
D["pessimist"] = scene((person, 220, 300, 0.75, {"pose": "sad", "shirt": MID}), (cloud, 400, 120, 0.35, {"color": MID}))
D["perfectionist"] = scene((person, 180, 300, 0.65, {"pose": "think"}), (checklist, 380, 260, 0.45, {"done": 3}), (magnifier, 420, 120, 0.2))
D["people-pleaser"] = scene((person, 256, 300, 0.65, {"pose": "carry"}), (heart, 140, 120, 0.15), (heart, 380, 120, 0.15), (gift, 256, 120, 0.2))
D["leader-personality"] = scene((person, 256, 280, 0.75, {"pose": "point"}), (crown, 256, 70, 0.18))
D["type-a-personality"] = scene((person, 200, 290, 0.7, {"pose": "walk", "shirt": A2}), (clock, 400, 120, 0.25), (checklist, 400, 340, 0.3, {"done": 2}))
D["type-b-personality"] = scene((person, 220, 300, 0.7, {"pose": "sit"}), (sun, 410, 110, 0.2), lambda s: s.M("M380 300 C400 280 420 300 440 280", A1, 8))
D["big-five-traits"] = scene(lambda s: [s.F("rect", x=80 + i * 72, y=420 - h, width=56, height=h, rx=8, fill=c) for i, (h, c) in enumerate(((220, A1), (160, A2), (280, "#4CB963"), (120, "#B880E8"), (200, A1L)))])
D["personality-test"] = scene((checklist, 256, 256, 1.0, {"done": 2}), (person, 420, 380, 0.25))

# ---------------------------------------------------------------- emotion science
D["emotion-wheel"] = scene(lambda s: [s.F("path", d=f"M256 256 L{arc_pt(256, 256, 200, a)[0]:.0f} {arc_pt(256, 256, 200, a)[1]:.0f} A200 200 0 0 1 {arc_pt(256, 256, 200, a + 45)[0]:.0f} {arc_pt(256, 256, 200, a + 45)[1]:.0f}Z", fill=c)
                                      for a, c in zip(range(0, 360, 45), ("#FFC83D", "#9BD7A8", "#4CB963", "#5EA8E8", "#3D8BFD", "#B880E8", "#E5484D", "#F5913E"))], lambda s: s.F("circle", cx=256, cy=256, r=60, fill=LIGHT))
D["fight-or-flight"] = scene((person, 150, 290, 0.6, {"pose": "cheer"}), (person, 360, 290, 0.6, {"pose": "walk", "shirt": A2}), lambda s: s.F("polygon", points=star_pts(256, 120, 60, 26, 8), fill=A2))
D["stress-response"] = scene((heart, 180, 240, 0.4, {"color": "#E5484D"}), (brain, 360, 220, 0.35), lambda s: s.M("M80 400 H170 L190 350 L215 450 L240 400 H440", "#E5484D", 10))
D["emotional-intelligence"] = scene((brain, 200, 260, 0.6), (heart, 370, 260, 0.3), lambda s: s.M("M290 260 H320", DARK, 10))
D["mood-swings"] = scene(lambda s: s.M("M60 256 C120 120 180 120 220 256 C260 390 320 390 360 256 C400 120 440 160 460 200", A2, 14), (sun, 160, 110, 0.12), (cloud, 330, 420, 0.2, {"color": MID}))
D["empathy-brain"] = scene((brain, 256, 230, 0.7), (heart, 256, 400, 0.18, {"color": "#F7A1B5"}))
D["mirror-neurons"] = scene((person, 150, 300, 0.6, {"pose": "cheer"}), (person, 362, 300, 0.6, {"pose": "cheer", "shirt": A2}), lambda s: s.M("M256 100 V460", MID, 6, dash="14 12"))
D["laughter-science"] = scene((brain, 256, 300, 0.6), lambda s: (s.M("M190 120 Q210 90 230 120 M280 120 Q300 90 320 120", A2, 10)), lambda s: [sparkle(s, x, y, 20) for x, y in ((120, 160), (400, 170))])

# ---------------------------------------------------------------- phobias
def scared(x=256, y=300, sc=0.7):
    return (person, x, y, sc, {"pose": "sad", "shirt": A1L})


def spider_small(s):
    s.open(transform="translate(380 140) scale(0.35) translate(-256 -270)")
    bug(s, body="#2E2A3B", legs=8, antennae=None)
    s.close()


D["phobia"] = scene(scared(), lambda s: s.F("polygon", points=star_pts(400, 120, 50, 22, 8), fill=A2), (qmark, 120, 120, 0.2))
D["fear-of-heights"] = scene(lambda s: s.F("polygon", points="24,180 240,180 240,488 24,488", fill=MID), (person, 150, 120, 0.25, {"pose": "sad"}), lambda s: s.M("M300 200 V460 M300 460 l-14 -24 M300 460 l14 -24", A2, 8, dash="12 12"))
D["fear-of-spiders"] = scene(scared(200, 300), spider_small)
D["fear-of-the-dark"] = scene(lambda s: s.F("rect", x=24, y=24, width=464, height=464, rx=30, fill="#1E2A4A"), (person, 256, 300, 0.65, {"pose": "sad", "shirt": A1L}),
                              lambda s: [s.F("ellipse", outline=False, cx=x, cy=y, rx=10, ry=6, fill="#FFE38A") for x, y in ((100, 120), (130, 120), (400, 160), (430, 160))])
D["fear-of-small-spaces"] = scene(lambda s: s.F("rect", x=150, y=120, width=212, height=330, fill=MID), (person, 256, 300, 0.5, {"pose": "sad", "shirt": A1L}), lambda s: s.M("M120 140 L150 160 M392 140 L362 160", A2, 8))
D["fear-of-crowds"] = scene((group, 256, 250, 0.9, {"shirts": (MID, MID, MID)}), (person, 256, 340, 0.45, {"pose": "sad", "shirt": A2}))
D["fear-of-public-speaking"] = scene(lambda s: s.F("rect", x=200, y=300, width=112, height=160, rx=10, fill=A1D), (person, 256, 250, 0.55, {"pose": "sad"}),
                                     lambda s: [s.F("ellipse", outline=False, cx=x, cy=470, rx=26, ry=16, fill=MID) for x in (80, 140, 372, 432)])
D["fear-of-water"] = scene(lambda s: s.F("path", outline=False, d="M24 340 C120 300 200 380 300 340 C380 310 430 350 488 330 V488 H24Z", fill="#8FD0FF"), scared(256, 230, 0.55))
D["fear-of-flying"] = scene(lambda s: s.F("path", d="M60 220 L380 180 C440 176 470 200 450 230 L100 270Z", fill=LIGHT), lambda s: s.F("polygon", points="200,210 290,120 320,124 270,210", fill=MID), scared(256, 410, 0.3))
D["fear-of-snakes"] = scene(lambda s: (s.open(transform="translate(360 300) scale(0.5) translate(-256 -256)"), snake(s, body="#4CB963"), s.close()), scared(150, 300, 0.55))
D["fear-of-needles"] = scene(scared(180, 300, 0.6), lambda s: (s.T("M300 300 L440 160", MID, 14), s.F("rect", x=270, y=290, width=60, height=40, rx=6, fill=A1, transform="rotate(-45 300 310)")))
D["fear-of-missing-out"] = scene(lambda s: s.F("rect", x=160, y=80, width=192, height=340, rx=30, fill=DARK), lambda s: s.F("rect", outline=False, x=180, y=110, width=152, height=270, rx=10, fill=A1L),
                                 (group, 256, 250, 0.45), lambda s: [s.F("circle", cx=x, cy=y, r=16, fill="#E5484D") for x, y in ((350, 90), (120, 200))])

# ---------------------------------------------------------------- biases
D["cognitive-bias"] = scene((brain, 220, 260, 0.6), (scales, 400, 300, 0.35))
D["confirmation-bias"] = scene((magnifier, 230, 240, 0.8), (star, 214, 226, 0.2))
D["anchoring-bias"] = scene(lambda s: (s.T("M256 80 V360", MID, 18), s.T("M150 300 C170 420 340 420 362 300", MID, 18), s.F("circle", cx=256, cy=70, r=26, fill="none")), lambda s: stroke_text(s, "100", 256, 210, 60, A2, 9))
D["bandwagon-effect"] = scene(lambda s: [P(s, person, x, 300, 0.42, pose="walk", shirt=c) for x, c in ((110, A1), (220, A1), (330, A1), (440, A2))])
D["dunning-kruger-effect"] = scene(lambda s: (s.M("M70 90 V420 H450", DARK, 10), s.M("M90 400 C120 120 160 100 200 200 C240 330 280 340 320 280 C360 220 400 200 440 190", A2, 12)))
D["halo-effect"] = scene((person, 256, 290, 0.75), lambda s: s.raw(f'<ellipse cx="256" cy="90" rx="70" ry="18" fill="none" stroke="#FFC83D" stroke-width="14"/>'))
D["sunk-cost-fallacy"] = scene(lambda s: s.F("path", outline=False, d="M24 300 C120 280 220 320 300 300 C380 280 430 310 488 300 V488 H24Z", fill="#8FD0FF"), lambda s: [s.F("circle", cx=x, cy=y, r=30, fill="#FFC83D") for x, y in ((180, 360), (260, 400), (330, 350))])
D["placebo-effect"] = scene(lambda s: (s.F("circle", cx=256, cy=256, r=140, fill=LIGHT), s.M("M146 256 H366", MID, 14)), (qmark, 420, 110, 0.18))
D["negativity-bias"] = scene((scales, 256, 256, 1.0), lambda s: (s.F("circle", cx=136, cy=290, r=26, fill="#E5484D"), s.F("circle", cx=376, cy=280, r=14, fill="#4CB963")))
D["hindsight-bias"] = scene((person, 220, 300, 0.7, {"pose": "point"}), arrow("M420 180 C370 120 300 110 250 140", 246, 142, 170, A2))
D["gamblers-fallacy"] = scene(lambda s: (s.F("rect", x=110, y=150, width=170, height=170, rx=30, fill=LIGHT), s.F("rect", x=250, y=210, width=150, height=150, rx=26, fill=LIGHT, transform="rotate(15 325 285)")),
                              lambda s: [s.F("circle", outline=False, cx=x, cy=y, r=12, fill=DARK) for x, y in ((150, 190), (195, 235), (240, 280), (300, 260), (350, 310))], (qmark, 420, 110, 0.15))
D["spotlight-effect"] = scene(lambda s: s.F("polygon", outline=False, points="216,24 296,24 400,460 112,460", fill="#FFF1C2"), (person, 256, 300, 0.7, {"pose": "sad", "shirt": A2}))
D["choice-overload"] = scene((person, 256, 320, 0.55, {"pose": "think"}), lambda s: [P(s, qmark, x, y, 0.12, color=c) for x, y, c in ((100, 100, A1), (180, 70, A2), (260, 60, A1), (340, 70, A2), (420, 100, A1))])

# ---------------------------------------------------------------- perception
D["perception"] = scene((eye_part, 200, 256, 0.55), (brain, 380, 256, 0.35), lambda s: s.M("M300 256 H320", DARK, 10))
D["selective-attention"] = scene((eye_part, 256, 256, 0.7), lambda s: s.raw(f'<circle cx="256" cy="256" r="160" fill="none" stroke="{A2}" stroke-width="12" stroke-dasharray="24 14"/>'))
D["invisible-gorilla-test"] = scene(lambda s: [P(s, person, x, 300, 0.4, pose="cheer", shirt=c) for x, c in ((110, LIGHT), (400, LIGHT))],
                                    lambda s: (s.F("ellipse", cx=256, cy=320, rx=70, ry=90, fill="#3A3A44"), s.F("circle", cx=256, cy=200, r=50, fill="#3A3A44"), s.F("circle", cx=380, cy=140, r=22, fill=A2)))
D["change-blindness"] = scene(lambda s: [(s.F("rect", x=x, y=140, width=200, height=230, rx=16, fill=A1L), s.F("circle", cx=x + 100, cy=230, r=40, fill=c)) for x, c in ((40, A2), (272, "#4CB963"))])
D["pareidolia"] = scene(lambda s: (s.F("rect", x=100, y=160, width=312, height=200, rx=30, fill=A1L), s.F("circle", cx=200, cy=230, r=30, fill=DARK), s.F("circle", cx=312, cy=230, r=30, fill=DARK),
                                   s.M("M200 310 Q256 340 312 310", DARK, 12)))
D["colour-perception"] = scene(lambda s: [s.F("circle", cx=x, cy=y, r=110, fill=c, fill_opacity="0.75") for x, y, c in ((200, 210, "#E5484D"), (312, 210, "#3D8BFD"), (256, 310, "#4CB963"))])
D["inattentional-blindness"] = scene((eye_part, 256, 256, 0.6), lambda s: s.F("rect", x=96, y=230, width=320, height=52, rx=26, fill=DARK))

# ---------------------------------------------------------------- habits and motivation
D["motivation"] = scene((person, 220, 280, 0.75, {"pose": "cheer"}), (star, 410, 110, 0.25), lambda s: s.F("polygon", points="420,250 380,320 410,320 390,380 440,300 410,300", fill=A2))
D["habit-loop"] = scene(lambda s: [arrow(f"M{a[0]:.0f} {a[1]:.0f} A150 150 0 0 1 {b[0]:.0f} {b[1]:.0f}", b[0], b[1], ang + 120, A1, 22, 44)(s) for ang in (-90, 30, 150) for a, b in [(arc_pt(256, 256, 150, ang), arc_pt(256, 256, 150, ang + 90))]],
                        (bulb, 256, 100, 0.15, {"glow": False}), (gear, 400, 340, 0.15), (star, 110, 340, 0.12))
D["habit-formation"] = scene((calendar, 256, 256, 0.95, {"mark": False}), lambda s: [s.M(f"M{x - 10} {y} L{x} {y + 12} L{x + 18} {y - 12}", A2, 10) for x, y in ((142, 252), (204, 252), (266, 252), (328, 252), (142, 322), (204, 322))])
D["reward-system"] = scene((brain, 200, 260, 0.55), (star, 400, 200, 0.3), (gift, 400, 380, 0.25))
D["intrinsic-motivation"] = scene((person, 256, 290, 0.75), (heart, 256, 230, 0.12, {"color": A2}), lambda s: sparkle(s, 380, 120, 30))
D["extrinsic-motivation"] = scene((person, 200, 300, 0.7, {"pose": "walk"}), (crown, 410, 160, 0.2), lambda s: [s.F("circle", cx=x, cy=y, r=22, fill="#FFC83D") for x, y in ((380, 300), (420, 330), (400, 370))])
D["willpower"] = scene((person, 200, 290, 0.7, {"pose": "cheer"}), (padlock, 400, 300, 0.3), (gift, 400, 130, 0.2))
D["delayed-gratification"] = scene(lambda s: (s.F("rect", x=60, y=340, width=392, height=40, rx=10, fill=A2L), s.F("ellipse", cx=256, cy=320, rx=60, ry=40, fill=LIGHT), s.F("ellipse", cx=380, cy=320, rx=60, ry=40, fill=LIGHT)),
                                   (clock, 140, 160, 0.25), (person, 140, 420, 0.25))
D["flow-state"] = scene((person, 220, 300, 0.7, {"pose": "sit"}), lambda s: s.M("M300 140 C360 100 400 180 460 140 M300 200 C360 160 400 240 460 200", A1, 10))
D["procrastination-brain"] = scene((brain, 200, 260, 0.6), (clock, 400, 150, 0.22), lambda s: s.M("M360 330 H400 L360 370 H400", A1, 8))

# ---------------------------------------------------------------- maslow and wellbeing
@reg("maslows-pyramid")
def _(s):
    cols = ("#E5484D", "#F5913E", "#FFC83D", "#4CB963", "#3D8BFD")
    for i, c in enumerate(cols):
        y0, y1 = 440 - i * 76, 440 - (i + 1) * 76
        w0, w1 = 200 - i * 40, 200 - (i + 1) * 40
        s.F("polygon", points=f"{256 - w0},{y0} {256 + w0},{y0} {256 + w1},{y1} {256 - w1},{y1}", fill=c)


D["basic-needs"] = scene(lambda s: (s.F("path", d="M150 120 H362 L330 260 H182Z", fill="#8FD0FF"), s.F("rect", x=150, y=300, width=212, height=140, rx=20, fill="#E8B878")), (heart, 420, 120, 0.12))
D["self-actualisation"] = scene((mountain, 256, 300, 0.9), (person, 236, 120, 0.25, {"pose": "cheer"}), (star, 400, 90, 0.15))
D["happiness-science"] = scene((brain, 220, 280, 0.6), (sun, 410, 130, 0.2), lambda s: s.M("M180 220 Q220 250 260 220", A2, 10))
D["gratitude-journal"] = scene((book, 256, 280, 0.9), (heart, 256, 150, 0.18, {"color": A2}))

# ---------------------------------------------------------------- therapy
def couch(s, x=256, y=330, sc=1.0):
    s.open(transform=f"translate({x} {y}) scale({sc}) translate(-256 -330)")
    s.F("rect", x=60, y=280, width=392, height=100, rx=30, fill=A1)
    s.F("rect", x=60, y=220, width=100, height=160, rx=30, fill=A1D)
    s.T("M90 380 V420 M422 380 V420", DARK, 14)
    s.close()


D["therapy"] = scene((person, 150, 300, 0.6, {"pose": "sit"}), (person, 362, 300, 0.6, {"pose": "sit", "shirt": A2}), (heart, 256, 110, 0.15, {"color": A2}))
D["therapists-couch"] = couch
D["counselling-session"] = scene(couch, (person, 400, 260, 0.5, {"pose": "sit", "shirt": A2}), (thought, 200, 120, 0.3))
D["group-therapy"] = scene(lambda s: [P(s, person, x, y, 0.35, pose="sit", shirt=c) for x, y, c in ((256, 180, A1), (120, 300, A2), (392, 300, A1L), (180, 420, "#4CB963"), (332, 420, A1D))])
D["cognitive-behavioural-therapy"] = scene((brain, 140, 256, 0.35), arrow("M200 256 H230", 240, 256, 0), (heart, 300, 256, 0.15, {"color": A2}), arrow("M340 256 H370", 380, 256, 0), (person, 440, 300, 0.25, {"pose": "cheer"}))
D["art-therapy"] = scene(lambda s: (s.F("rect", x=180, y=100, width=220, height=180, rx=10, fill=LIGHT), s.T("M200 460 L260 280 M380 460 L320 280", A1D, 12),
                                    s.M("M210 220 C240 160 290 260 340 180", A2, 14), s.F("circle", cx=300, cy=150, r=20, fill="#4CB963")), (person, 110, 300, 0.45, {"pose": "point"}))
D["support-group"] = scene((group, 256, 290, 0.95), (heart, 256, 90, 0.18, {"color": A2}))

# ---------------------------------------------------------------- strange experiences
D["deja-vu"] = scene((person, 160, 300, 0.55), (person, 352, 300, 0.55, {"shirt": A1L}), lambda s: s.M("M256 120 C230 140 230 170 256 190 C282 210 282 240 256 260", A2, 10))
D["jamais-vu"] = scene((person, 220, 300, 0.7, {"pose": "think"}), (qmark, 400, 120, 0.25), (door, 400, 330, 0.3))
D["tip-of-the-tongue"] = scene((person, 220, 300, 0.7, {"pose": "think"}), (thought, 400, 120, 0.35), lambda s: s.M("M370 120 H390 M400 120 H410 M420 120 H430", A1, 8))
D["earworm"] = scene(in_head(lambda s: s.M("M220 240 V170 L300 150 V220 M220 240 m-20 0 a20 14 0 1 0 40 0 a20 14 0 1 0 -40 0 M300 220 m-20 0 a20 14 0 1 0 40 0 a20 14 0 1 0 -40 0", A1D, 10), 262, 210, 1.0))
D["brain-freeze"] = scene((brain, 256, 220, 0.6, {"color": "#B8E0F8", "fold": "#7FB8D8"}), lambda s: (s.F("polygon", points="200,320 312,320 256,460", fill="#E8B878"), s.F("circle", cx=256, cy=320, r=56, fill="#F7A1B5")))
D["hypnosis"] = scene(lambda s: s.M("M256 256 " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in (arc_pt(256, 256, 8 + t * 1.4, t * 6) for t in range(1, 140))), A1, 14))
D["daydreaming"] = scene((person, 160, 300, 0.6, {"pose": "sit"}), (thought, 360, 150, 0.55), (sun, 340, 140, 0.1), (star, 390, 150, 0.08))
D["intuition"] = scene((person, 200, 290, 0.7), (heart, 200, 220, 0.1, {"color": A2}), lambda s: sparkle(s, 380, 140, 40))
D["sixth-sense"] = scene((eye_part, 256, 256, 0.7), lambda s: [sparkle(s, x, y, 24, A2) for x, y in ((100, 120), (420, 140), (420, 380), (90, 380))])

# ---------------------------------------------------------------- intelligence and conditioning
D["iq"] = scene((brain, 256, 230, 0.75), lambda s: stroke_text(s, "100", 256, 420, 60, A1D, 9))
D["iq-test"] = scene((checklist, 256, 256, 0.95, {"done": 2}), (brain, 400, 400, 0.22))
D["multiple-intelligences"] = scene((brain, 256, 256, 0.5), lambda s: [P(s, p, x, y, 0.14, **k) for p, x, y, k in ((book, 100, 120, {}), (gear, 412, 120, {}), (heart, 100, 400, {"color": A2}), (star, 412, 400, {}))])
D["classical-conditioning"] = scene(lambda s: (s.F("path", d="M150 120 C150 80 210 80 210 120 V200 H150Z", fill="#FFC83D"), s.F("circle", cx=180, cy=210, r=12, fill="#B97C12")),
                                    lambda s: (s.open(transform="translate(340 330) scale(0.5) translate(-256 -256)"), quad(s, body="#E8B878", ears="side", snout="round", snout_c="#F7E3C4", tail="thin", head_r=56, tongue=True), s.close()))
D["operant-conditioning"] = scene(lambda s: (s.F("rect", x=100, y=160, width=312, height=260, rx=20, fill=A1L), s.F("rect", x=330, y=200, width=50, height=30, rx=6, fill=A2)),
                                  lambda s: (s.F("ellipse", cx=220, cy=360, rx=60, ry=40, fill=LIGHT), s.F("circle", cx=280, cy=330, r=26, fill=LIGHT)))
D["learning-curve"] = scene(lambda s: (s.M("M70 90 V420 H450", DARK, 10), s.M("M90 400 C200 390 240 160 440 130", A1, 12)))
D["growth-of-the-brain"] = scene((brain, 150, 300, 0.3), (brain, 280, 280, 0.45), (brain, 410, 260, 0.55))
D["reaction-time-test"] = scene(lambda s: (s.F("circle", cx=256, cy=280, r=150, fill="#E5484D"), s.F("circle", outline=False, cx=256, cy=270, r=110, fill="#F07A7E")), (clock, 410, 110, 0.18))


if __name__ == "__main__":
    run("psychology-mind", D, sys.argv[1:] or None)
