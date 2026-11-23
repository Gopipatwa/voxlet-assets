"""animals drawings. Run: python drawings/animals.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, bat, bird, bug, butterfly_wings, cetacean, eye, fish, kangaroo, lizard, primate, quad, round_critter, seal, shade, snake, tint, turtle  # noqa: E402
from draw_lib import C, arc_pt, run, star_pts  # noqa: E402

D = {}
BROWN, DBROWN, TAN, CREAM, GREY, DGREY = C["brown"], C["darkbrown"], C["tan"], C["cream"], C["grey"], C["darkgrey"]
PINK, ORANGE, YEL, GREEN, DGREEN, RED = C["pink"], C["orange"], C["yellow"], C["green"], C["darkgreen"], C["red"]


def Q(**p):
    return lambda s: quad(s, **p)


def B(**p):
    return lambda s: bird(s, **p)


def F(**p):
    return lambda s: fish(s, **p)


# ---------------------------------------------------------------- samples across templates
D["cow"] = Q(body=WHITE, pattern="patches", pat_c="#3A3A44", snout="flat", snout_c=PINK, ears="side", horns="cow", tail="tuft", hoof=DGREY, nose=shade(PINK, 0.6), seed=4)
D["horse"] = Q(body=BROWN, neck=0.55, head_r=48, snout="long", snout_c=TAN, ears="pointy", tail="horse", mane=DBROWN, hoof=DGREY, leg=1.25, bw=1.0)
D["lion"] = Q(body="#E0A458", mane="lion", snout="round", snout_c=CREAM, ears="round", tail="tuft", head_r=60, whiskers=True)
D["tiger"] = Q(body=ORANGE, belly=CREAM, pattern="stripes", pat_c="#2E2A3B", snout="round", snout_c=CREAM, ears="round", ear_in=CREAM, tail="long", whiskers=True, chin=CREAM)
D["elephant"] = Q(body="#9AA3AF", bw=1.15, bh=1.25, leg_w=50, head_r=80, snout="none", ears="elephant", ear_in="#B7BEC8", trunk=True, tusks=True, tail="thin", leg=0.9)
D["giraffe"] = Q(body="#F2C14E", pattern="giraffe", pat_c="#B0712E", neck=1.25, head_r=40, snout="long", snout_c="#F7D98A", ears="pointy", horns="small", leg=1.5, bw=0.85, tail="tuft", hoof=DBROWN, mane="#B0712E")
D["zebra"] = Q(body=WHITE, pattern="stripes", pat_c="#2E2A3B", neck=0.45, head_r=46, snout="long", snout_c="#5A5A66", ears="pointy", tail="tuft", mane="#2E2A3B", hoof=DGREY, leg=1.2)
D["dog"] = Q(body=TAN, belly=CREAM, ears="floppy", snout="normal", snout_c=CREAM, tail="thin", head_r=56, bw=0.9, tongue=True)
D["cat"] = Q(body="#9AA3AF", pattern="stripes", pat_c="#6B7280", ears="pointy", ear_in=PINK, snout="round", snout_c=WHITE, nose=PINK, tail="long", whiskers=True, bw=0.85, head_r=54)
D["rabbit"] = Q(body="#C9CED6", belly=WHITE, ears="long", ear_in=PINK, snout="round", snout_c=WHITE, nose=PINK, tail="short", tail_c=WHITE, bw=0.8, leg=0.5, head_r=56)
D["pig"] = Q(body=PINK, snout="pig", snout_c="#F48AA6", ears="pointy", ear_c="#F48AA6", tail="curl", leg=0.6, bw=1.0, head_r=60, nose=None)
D["goat"] = Q(body=WHITE, snout="long", snout_c=CREAM, ears="side", horns="goat", horn_c=GREY, tail="short", hoof=DGREY, head_r=46, neck=0.25, leg=1.1)
D["camel"] = Q(body=TAN, hump=1, neck=0.6, head_r=40, snout="long", ears="round", tail="tuft", leg=1.45, leg_w=24, hoof=DBROWN)
D["deer"] = Q(body=BROWN, belly=CREAM, pattern="spots", pat_c=CREAM, neck=0.4, head_r=44, snout="long", snout_c=TAN, ears="pointy", horns="antlers", horn_c=DBROWN, tail="short", tail_c=WHITE, leg=1.3, hoof=DBROWN)
D["bear"] = Q(body=DBROWN, snout="round", snout_c=TAN, ears="round", tail="short", bw=1.05, bh=1.15, leg_w=40, leg=0.7, head_r=62)
D["fox"] = Q(body=ORANGE, belly=WHITE, ears="pointy", ear_in=DBROWN, snout="long", snout_c=WHITE, tail="bushy", tail_c=ORANGE, bw=0.85, head_r=50, chin=WHITE)
D["parrot"] = B(body=GREEN, wing=C["blue"], head_c=GREEN, belly=YEL, beak="hook", beak_c=DGREY, tail="long", tail_c=C["blue"], cheek=YEL, legs_c=DGREY)
D["eagle"] = B(body=DBROWN, head_c=WHITE, beak="hook", beak_c=YEL, tail="fan", tail_c=WHITE, legs_c=YEL, size=1.1)
D["duck"] = B(body=WHITE, head_c=WHITE, beak="duck", beak_c=ORANGE, tail="up", tail_c=WHITE, swim=True, wing="#E5E7EB")
D["flamingo"] = B(body="#F7A1B5", wing="#F48AA6", beak="bent", beak_c=BLACK, neck=0.9, leg=2.2, legs_c="#F48AA6", size=0.85, tail="short")
D["hen"] = B(body=BROWN, wing=DBROWN, beak="short", beak_c=YEL, comb=RED, wattle=RED, tail="up", tail_c=DBROWN, legs_c=YEL, size=1.05)
D["goldfish"] = F(body=ORANGE, belly="#FFC83D", tail="fan", dorsal="small", length=0.9)
D["clownfish"] = F(body=ORANGE, stripes=3, stripe_c=WHITE, tail="round", dorsal="small", length=0.95)
D["shark"] = F(body="#7A8CA3", belly=WHITE, tail="crescent", dorsal="shark", length=1.25, height=0.75, teeth=True)
D["bee"] = lambda s: bug(s, body=YEL, head_c="#3A3A44", wings="clear", stripes="#3A3A44", stinger=True)
D["ladybird"] = lambda s: bug(s, body="#3A3A44", wings="beetle", wing_c=RED, spots="#2E2A3B")
D["butterfly"] = lambda s: butterfly_wings(s, ORANGE, YEL)
D["snake"] = lambda s: snake(s, body=GREEN, pattern=DGREEN)
D["cobra"] = lambda s: snake(s, body="#B88B5A", belly=CREAM, hood=True)
D["turtle"] = lambda s: turtle(s)
D["lizard"] = lambda s: lizard(s, body="#7DBB4A", belly=CREAM)

# ---------------------------------------------------------------- farm mammals
COW = dict(body=WHITE, pattern="patches", pat_c="#3A3A44", snout="flat", snout_c=PINK, ears="side", horns="cow", tail="tuft", hoof=DGREY, nose=shade(PINK, 0.6), seed=4)
D["bull"] = Q(**{**COW, "body": DBROWN, "pattern": None, "snout_c": TAN, "bw": 1.15, "bh": 1.15, "horns": "cow", "horn_c": CREAM, "head_r": 62})
D["ox"] = Q(**{**COW, "body": BROWN, "pattern": None, "snout_c": TAN, "bw": 1.15, "horn_c": CREAM})
D["calf"] = Q(**{**COW, "horns": None, "bw": 0.8, "bh": 0.85, "head_r": 62, "leg": 0.9, "seed": 7})
D["buffalo"] = Q(body="#3A3A44", snout="flat", snout_c="#5A5A66", ears="side", horns="ram", horn_c="#6B7280", tail="tuft", hoof=BLACK, bw=1.15, bh=1.1, head_r=60, nose=BLACK)
SHEEP = dict(body="#3A3A44", wool="#F4F1EA", head_c="#3A3A44", leg_c="#3A3A44", snout="round", snout_c="#5A5A66", ears="side", ear_c="#3A3A44", tail="short", tail_c="#F4F1EA", head_r=46, leg=0.8, nose=BLACK)
D["sheep"] = Q(**SHEEP)
D["lamb"] = Q(**{**SHEEP, "wool": WHITE, "head_c": CREAM, "leg_c": CREAM, "ear_c": CREAM, "snout_c": tint(CREAM, 0.3), "bw": 0.75, "bh": 0.8, "head_r": 52})
D["ram"] = Q(**{**SHEEP, "horns": "ram", "horn_c": TAN, "head_r": 50})
D["kid-goat"] = Q(body=WHITE, snout="long", snout_c=CREAM, ears="side", tail="short", hoof=DGREY, head_r=50, neck=0.2, leg=0.95, bw=0.75, bh=0.8)
D["piglet"] = Q(body=PINK, snout="pig", snout_c="#F48AA6", ears="pointy", ear_c="#F48AA6", tail="curl", leg=0.55, bw=0.75, bh=0.85, head_r=60, nose=None)
HORSE = dict(body=BROWN, neck=0.55, head_r=48, snout="long", snout_c=TAN, ears="pointy", tail="horse", mane=DBROWN, hoof=DGREY, leg=1.25)
D["foal"] = Q(**{**HORSE, "body": TAN, "mane": BROWN, "bw": 0.75, "leg": 1.35, "head_r": 46})
D["pony"] = Q(**{**HORSE, "body": "#C9CED6", "mane": WHITE, "leg": 0.9, "bw": 0.9, "head_r": 50})
D["donkey"] = Q(**{**HORSE, "body": "#9AA3AF", "mane": "#6B7280", "ears": "long", "ear_in": "#6B7280", "snout_c": "#E5E7EB", "tail": "tuft", "leg": 1.05, "neck": 0.4})
D["mule"] = Q(**{**HORSE, "body": "#8C6A50", "ears": "long", "ear_in": DBROWN, "tail": "tuft", "leg": 1.15})
CAMEL = dict(body=TAN, hump=1, neck=0.6, head_r=40, snout="long", ears="round", tail="tuft", leg=1.45, leg_w=24, hoof=DBROWN)
D["dromedary-camel"] = Q(**CAMEL)
D["bactrian-camel"] = Q(**{**CAMEL, "hump": 2, "body": "#B08A5A"})
D["llama"] = Q(body="#F4F1EA", wool="#F4F1EA", neck=0.9, head_r=36, snout="long", snout_c=CREAM, ears="long", tail="short", leg=1.2, leg_w=22, bw=0.85, hoof=DBROWN)
D["alpaca"] = Q(body="#C68A5C", wool="#E8B878", head_c="#E8B878", neck=0.7, head_r=40, snout="round", snout_c=CREAM, ears="pointy", tail="short", tail_c="#E8B878", leg=0.95, leg_w=24, bw=0.8)
D["yak"] = Q(body="#3A3A44", wool="#4A4A55", snout="flat", snout_c="#5A5A66", ears="side", horns="cow", horn_c=CREAM, tail="tuft", leg=0.85, bw=1.15, bh=1.15, head_r=56, nose=BLACK)

# ---------------------------------------------------------------- pets
DOG = dict(body=TAN, belly=CREAM, ears="floppy", snout="normal", snout_c=CREAM, tail="thin", head_r=56, bw=0.9, tongue=True)
D["puppy"] = Q(**{**DOG, "body": "#E8B878", "bw": 0.7, "bh": 0.8, "head_r": 64, "leg": 0.75})
CAT = dict(body="#9AA3AF", pattern="stripes", pat_c="#6B7280", ears="pointy", ear_in=PINK, snout="round", snout_c=WHITE, nose=PINK, tail="long", whiskers=True, bw=0.85, head_r=54)
D["kitten"] = Q(**{**CAT, "body": ORANGE, "pat_c": "#D9772B", "bw": 0.65, "bh": 0.8, "head_r": 62, "leg": 0.75})
D["hamster"] = lambda s: round_critter(s, body="#E8A066", belly="#FFF3DF")
D["guinea-pig"] = lambda s: round_critter(s, body="#B07A4A", belly=WHITE, ears="round", whiskers=False)
D["gerbil"] = lambda s: round_critter(s, body="#D9A66E", belly="#FFF3DF", tail="thin")
D["ferret"] = Q(body="#E8D8BF", bw=1.2, bh=0.6, leg=0.45, leg_w=20, head_r=40, ears="round", snout="round", snout_c=WHITE, mask="#6E5A4A", tail="long", tail_c="#6E5A4A", leg_c="#6E5A4A")

# ---------------------------------------------------------------- wild mammals
ELE = dict(body="#9AA3AF", bw=1.15, bh=1.25, leg_w=50, head_r=80, snout="none", ears="elephant", ear_in="#B7BEC8", trunk=True, tusks=True, tail="thin", leg=0.9)
D["african-elephant"] = Q(**{**ELE, "head_r": 84})
D["asian-elephant"] = Q(**{**ELE, "body": "#8C95A1", "head_r": 72, "ear_in": "#A6AEB9", "tusks": False})
D["baby-elephant"] = Q(**{**ELE, "bw": 0.8, "bh": 0.95, "head_r": 84, "tusks": False, "leg": 0.75})
D["rhinoceros"] = Q(body="#8C95A1", bw=1.2, bh=1.1, leg_w=44, leg=0.75, head_r=58, snout="long", snout_c="#A6AEB9", ears="pointy", horns="rhino", horn_c="#E5E7EB", tail="thin")
D["hippopotamus"] = Q(body="#8E7B9E", bw=1.25, bh=1.2, leg_w=46, leg=0.55, head_r=62, snout="flat", snout_c="#B9A8C7", ears="round", tail="short", nose="#5A4A6A")
BEAR = dict(body=DBROWN, snout="round", snout_c=TAN, ears="round", tail="short", bw=1.05, bh=1.15, leg_w=40, leg=0.7, head_r=62)
D["brown-bear"] = Q(**BEAR)
D["polar-bear"] = Q(**{**BEAR, "body": "#F4F1EA", "snout_c": WHITE})
D["black-bear"] = Q(**{**BEAR, "body": "#2E2A3B", "snout_c": TAN})
D["grizzly-bear"] = Q(**{**BEAR, "body": "#8C6239", "hump": 1, "snout_c": "#C9A27A"})
D["panda"] = Q(**{**BEAR, "body": WHITE, "leg_c": "#2E2A3B", "ear_c": "#2E2A3B", "snout_c": WHITE, "mask": "#2E2A3B", "pattern": None})
D["red-panda"] = Q(body="#C1442E", head_c="#D9653E", leg_c="#3A2E28", ears="pointy", ear_in=WHITE, snout="round", snout_c=WHITE, tail="bushy", tail_c="#D9653E", bw=0.85, leg=0.6, head_r=54, chin=WHITE)
D["koala"] = lambda s: primate(s, body="#9AA3AF", face="#B7BEC8", belly="#E5E7EB", big_nose="#3A3A44")
D["kangaroo"] = lambda s: kangaroo(s)
D["wallaby"] = lambda s: kangaroo(s, body="#9A8A7A", belly="#D9CBB0")
D["wombat"] = Q(body="#8C7560", bw=1.0, bh=1.0, leg=0.4, leg_w=34, head_r=56, ears="round", snout="round", snout_c="#A58B70", tail="short")
D["platypus"] = lambda s: (quad(s, body="#7A5A3E", bw=1.1, bh=0.75, leg=0.35, leg_w=24, head_r=44, ears="none", snout="none", tail="none"),
                           s.F("path", d="M130 380 C40 380 40 330 140 330Z", fill="#7A5A3E"))
D["echidna"] = lambda s: round_critter(s, body="#6E5A4A", belly="#8C7560", quills="#E8DCC8", ears=None, whiskers=False)
DEER = dict(body=BROWN, belly=CREAM, neck=0.4, head_r=44, snout="long", snout_c=TAN, ears="pointy", horns="antlers", horn_c=DBROWN, tail="short", tail_c=WHITE, leg=1.3, hoof=DBROWN)
D["reindeer"] = Q(**{**DEER, "body": "#8C6A50", "belly": "#E8DCC8", "chin": "#E8DCC8"})
D["moose"] = Q(**{**DEER, "body": "#4A3B32", "belly": None, "head_r": 52, "snout_c": "#5E4A3E", "horn_c": "#C9A27A", "hump": 1, "neck": 0.2})
D["elk"] = Q(**{**DEER, "body": "#A0703E", "belly": None, "head_r": 46, "neck": 0.45})
ANT = dict(body="#C68A5C", belly=WHITE, neck=0.35, head_r=40, snout="long", snout_c=CREAM, ears="pointy", horns="long-curved", horn_c=DBROWN, tail="short", leg=1.35, leg_w=20, hoof=DBROWN, bw=0.9)
D["antelope"] = Q(**ANT)
D["gazelle"] = Q(**{**ANT, "body": "#D9A066", "horns": "goat"})
D["impala"] = Q(**{**ANT, "body": "#C67A4A", "horns": "long-curved"})
D["wildebeest"] = Q(body="#5A5A66", hump=1, neck=0.2, head_r=50, snout="long", snout_c="#3A3A44", ears="side", horns="cow", horn_c="#3A3A44", tail="tuft", mane="#2E2A3B", leg=1.1, hoof=BLACK)
D["bison"] = Q(body="#4A3B32", hump=1, wool="#5E4A3E", head_c="#3A2E28", snout="flat", snout_c="#3A2E28", ears="side", horns="cow", horn_c="#2E2A3B", tail="tuft", leg=0.85, bw=1.2, bh=1.1, head_r=58, nose=BLACK)
D["oryx"] = Q(**{**ANT, "body": "#E8DCC8", "belly": WHITE, "mask": "#3A3A44", "horn_c": "#3A3A44", "horns": "long-curved"})
D["ibex"] = Q(body="#A58B70", neck=0.2, head_r=44, snout="long", snout_c="#C9B79A", ears="side", horns="long-curved", horn_c="#6E5A4A", tail="short", leg=1.0, hoof=DGREY)
D["mountain-goat"] = Q(body=WHITE, wool="#F4F1EA", neck=0.2, head_r=44, snout="long", snout_c=WHITE, ears="pointy", horns="small", horn_c=BLACK, tail="short", leg=1.0, hoof=BLACK)
D["wild-boar"] = Q(body="#5E4A3E", snout="pig", snout_c="#7A6250", ears="pointy", tail="thin", leg=0.6, bw=1.0, head_r=56, tusks=True, mane="#3A2E28", nose=None)
D["warthog"] = Q(body="#8C7560", snout="pig", snout_c="#A58B70", ears="pointy", tail="thin", leg=0.65, bw=1.0, head_r=58, tusks=True, nose=None)
FOX = dict(body=ORANGE, belly=WHITE, ears="pointy", ear_in=DBROWN, snout="long", snout_c=WHITE, tail="bushy", tail_c=ORANGE, bw=0.85, head_r=50, chin=WHITE)
D["arctic-fox"] = Q(**{**FOX, "body": "#F4F1EA", "tail_c": "#F4F1EA", "ear_in": "#C9CED6"})
D["fennec-fox"] = Q(**{**FOX, "body": "#EBCB94", "tail_c": "#EBCB94", "ears": "long", "ear_in": PINK, "head_r": 46})
WOLF = dict(body="#7A8290", belly="#D9DEE5", ears="pointy", ear_in="#D9DEE5", snout="long", snout_c="#D9DEE5", tail="bushy", tail_c="#7A8290", bw=1.0, head_r=50, chin="#D9DEE5", leg=1.05)
D["wolf"] = Q(**WOLF)
D["coyote"] = Q(**{**WOLF, "body": "#B08A60", "tail_c": "#B08A60", "belly": "#E8DCC8", "snout_c": "#E8DCC8", "chin": "#E8DCC8"})
D["jackal"] = Q(**{**WOLF, "body": "#C68A5C", "tail_c": "#6E5A4A", "bw": 0.85})
D["hyena"] = Q(body="#C9A27A", pattern="spots", pat_c="#6E5A4A", ears="round", snout="long", snout_c="#6E5A4A", tail="tuft", mane="#6E5A4A", back_slope=-8, head_r=52, leg=1.0)
D["raccoon"] = Q(body="#8C96A3", belly="#C9CED6", ears="pointy", ear_in=WHITE, snout="round", snout_c=WHITE, mask="#2E2A3B", tail="long", tail_c="#5A5A66", bw=0.85, head_r=52, leg=0.6)
D["badger"] = Q(body="#8C96A3", head_c=WHITE, leg_c="#2E2A3B", ears="round", snout="long", snout_c=WHITE, mask="#2E2A3B", tail="short", leg=0.45, bw=1.0, head_r=48)
D["skunk"] = Q(body="#2E2A3B", ears="round", snout="round", snout_c="#2E2A3B", tail="bushy", tail_c="#2E2A3B", bw=0.85, leg=0.5, head_r=50, chin=WHITE, pattern="stripes", pat_c=WHITE)
D["otter"] = Q(body="#7A5A3E", belly="#C9A27A", ears="round", snout="round", snout_c="#C9A27A", tail="long", whiskers=True, bw=1.15, bh=0.7, leg=0.4, head_r=46)
D["beaver"] = lambda s: (quad(s, body="#7A5A3E", ears="round", snout="round", snout_c="#9A7A5E", tail="none", bw=1.0, leg=0.45, head_r=54),
                         s.F("ellipse", cx=60, cy=400, rx=60, ry=22, fill="#4A3B32", transform="rotate(-15 60 400)"))
D["squirrel"] = lambda s: round_critter(s, body="#C1662E", belly="#F2D3B0", ears="round", tail="bushy")
D["chipmunk"] = lambda s: round_critter(s, body="#B07A4A", belly="#F2D3B0", ears="round", tail="bushy")
D["porcupine"] = lambda s: round_critter(s, body="#6E5A4A", belly="#8C7560", quills="#3A2E28", ears=None)
D["hedgehog"] = lambda s: round_critter(s, body="#E8C39E", belly="#F7E3C4", quills="#8C6A50", ears=None)
D["mouse-animal"] = lambda s: round_critter(s, body="#B7BEC8", belly="#E5E7EB", ears="big", tail="thin")
D["rat"] = lambda s: round_critter(s, body="#7A8290", belly="#B7BEC8", ears="round", tail="thin")
D["mole"] = lambda s: round_critter(s, body="#3A3A44", belly="#5A5A66", ears=None, nose=PINK)
D["shrew"] = lambda s: round_critter(s, body="#6E5A4A", belly="#A58B70", ears=None, tail="thin")
D["bat-animal"] = lambda s: bat(s)
D["sloth"] = lambda s: (s.T("M40 120 H472", "#6E5A4A", 26), primate(s, body="#A58B70", face="#E8DCC8", arms_long=True))
D["anteater"] = Q(body="#8C7560", snout="long", snout_c="#8C7560", head_r=36, ears="round", tail="bushy", tail_c="#6E5A4A", bw=1.15, leg=0.8, pattern="stripes", pat_c="#3A3A44")
D["armadillo"] = Q(body="#A6AEB9", pattern="stripes", pat_c="#7A8290", head_r=36, snout="long", snout_c="#C9CED6", ears="pointy", tail="thin", leg=0.35, bw=1.0, bh=0.9)
D["pangolin"] = Q(body="#8C6A50", pattern="rosettes", pat_c="#5E4A3E", head_r=34, snout="long", snout_c="#A58B70", ears="none", tail="long", leg=0.35, bw=1.1, bh=0.9)
@lambda f: D.__setitem__("meerkat", f)
def _(s):
    s.T("M220 420 C180 440 150 446 120 446", "#B08A60", 18)
    s.T("M236 400 V446 M276 400 V446", "#B08A60", 22)
    s.F("ellipse", cx=256, cy=300, rx=62, ry=130, fill="#D9A66E")
    s.F("ellipse", outline=False, cx=262, cy=320, rx=34, ry=96, fill="#F2D3B0")
    s.T("M240 240 C260 270 280 270 296 256 M272 240 C290 266 306 268 318 256", "#B08A60", 14)
    s.F("circle", cx=226, cy=126, r=14, fill="#3A2E28")
    s.F("ellipse", cx=262, cy=140, rx=52, ry=44, fill="#D9A66E")
    s.F("ellipse", cx=302, cy=152, rx=26, ry=18, fill="#E8C39E")
    s.F("ellipse", outline=False, cx=262, cy=134, rx=16, ry=12, fill="#3A2E28")
    eye(s, 264, 134, 7)
    s.F("ellipse", outline=False, cx=326, cy=148, rx=7, ry=5, fill=BLACK)


@lambda f: D.__setitem__("platypus", f)
def _(s):
    s.F("path", d="M150 330 C90 320 40 340 30 370 C60 390 110 384 160 370Z", fill="#5E4A3E")
    for x in (190, 320):
        s.F("ellipse", cx=x, cy=400, rx=34, ry=14, fill="#5E4A3E")
    s.F("ellipse", cx=250, cy=340, rx=120, ry=62, fill="#7A5A3E")
    s.F("ellipse", cx=360, cy=318, rx=50, ry=42, fill="#7A5A3E")
    s.F("path", d="M394 300 C440 296 486 304 486 326 C486 346 440 350 394 342Z", fill="#3A3A44")
    eye(s, 372, 304, 7)
D["mongoose"] = Q(body="#9A8A7A", ears="round", snout="long", snout_c="#B7A898", tail="long", tail_c="#7A6A5A", bw=1.1, bh=0.65, leg=0.5, head_r=40)
D["aardvark"] = Q(body="#C9A27A", ears="long", ear_in=PINK, snout="long", snout_c="#B08A60", tail="long", leg=0.7, bw=1.0, head_r=42)
D["tapir"] = Q(body="#3A3A44", belly=None, ears="round", snout="long", snout_c="#3A3A44", trunk=False, tail="short", leg=0.8, bw=1.1, head_r=50, chin=WHITE)
D["capybara"] = Q(body="#A0703E", ears="round", snout="flat", snout_c="#8C6239", tail="none", leg=0.55, bw=1.05, bh=0.95, head_r=58)
D["opossum"] = lambda s: round_critter(s, body="#C9CED6", belly=WHITE, ears="round", tail="thin", nose=PINK)
D["weasel"] = Q(body="#A0703E", belly="#F2D3B0", ears="round", snout="round", snout_c="#F2D3B0", tail="long", bw=1.25, bh=0.55, leg=0.45, head_r=38)
D["mink"] = Q(body="#4A3B32", ears="round", snout="round", snout_c="#5E4A3E", tail="long", bw=1.2, bh=0.55, leg=0.45, head_r=38)
D["lemming"] = lambda s: round_critter(s, body="#C68A5C", belly="#3A2E28", ears=None)
D["hare"] = Q(body="#B08A60", belly=CREAM, ears="long", ear_in="#E8C39E", snout="round", snout_c=CREAM, nose=PINK, tail="short", tail_c=WHITE, bw=0.85, leg=0.8, head_r=52)
D["honey-badger"] = Q(body="#2E2A3B", head_c="#C9CED6", ears="round", snout="long", snout_c="#2E2A3B", tail="short", leg=0.5, bw=1.0, head_r=48, mane="#C9CED6")
D["okapi"] = Q(body="#4A3B32", leg_c="#F4F1EA", pattern=None, neck=0.5, head_r=44, snout="long", snout_c="#E8DCC8", ears="long", tail="tuft", leg=1.25, hoof=BLACK)

# ---------------------------------------------------------------- primates
D["monkey"] = lambda s: primate(s, tail="curl")
D["gorilla"] = lambda s: primate(s, body="#3A3A44", face="#5A5A66", arms_long=True, crest="#3A3A44")
D["chimpanzee"] = lambda s: primate(s, body="#2E2A3B", face="#D9B38C", arms_long=True)
D["orangutan"] = lambda s: primate(s, body="#C1662E", face="#8C6A50", arms_long=True)
D["gibbon"] = lambda s: primate(s, body="#6E5A4A", face="#3A3A44", arms_long=True)
D["baboon"] = lambda s: primate(s, body="#9A8A6A", face="#E8C39E", tail="long", big_nose="#C9A27A")
D["mandrill"] = lambda s: primate(s, body="#5A5A3A", face="#E8DCC8", big_nose=C["red"])
D["lemur"] = lambda s: primate(s, body="#9AA3AF", face=WHITE, tail="ringed", tail_c="#2E2A3B", nose="#2E2A3B")
D["macaque"] = lambda s: primate(s, body="#A58B70", face="#F2A6A0", tail="long")
D["langur"] = lambda s: primate(s, body="#C9CED6", face="#2E2A3B", tail="long", nose="#5A5A66")
D["capuchin-monkey"] = lambda s: primate(s, body="#3A2E28", face="#F2D3B0", tail="curl")
D["howler-monkey"] = lambda s: primate(s, body="#5E2E1E", face="#3A2E28", tail="curl")
D["proboscis-monkey"] = lambda s: primate(s, body="#C1662E", face="#F2C29B", tail="long", big_nose="#F2A6A0")

# ---------------------------------------------------------------- big cats
LION = dict(body="#E0A458", mane="lion", snout="round", snout_c=CREAM, ears="round", tail="tuft", head_r=60, whiskers=True)
D["lioness"] = Q(**{**LION, "mane": None, "head_r": 52, "chin": CREAM})
D["lion-cub"] = Q(**{**LION, "mane": None, "head_r": 64, "bw": 0.7, "bh": 0.8, "leg": 0.75, "pattern": "spots", "pat_c": "#C98A3E"})
TIGER = dict(body=ORANGE, belly=CREAM, pattern="stripes", pat_c="#2E2A3B", snout="round", snout_c=CREAM, ears="round", ear_in=CREAM, tail="long", whiskers=True, chin=CREAM)
D["bengal-tiger"] = Q(**{**TIGER, "body": "#E8782B"})
D["white-tiger"] = Q(**{**TIGER, "body": "#F4F1EA", "pat_c": "#3A3A44"})
SPOT = dict(body="#E8B04A", belly=CREAM, pattern="rosettes", pat_c="#3A2E28", snout="round", snout_c=CREAM, ears="round", tail="long", whiskers=True, chin=CREAM, head_r=50)
D["leopard"] = Q(**SPOT)
D["snow-leopard"] = Q(**{**SPOT, "body": "#D9DEE5", "pat_c": "#5A5A66", "tail": "bushy", "tail_c": "#D9DEE5"})
D["jaguar"] = Q(**{**SPOT, "body": "#D9963A", "bw": 1.1})
D["cheetah"] = Q(**{**SPOT, "pattern": "spots", "leg": 1.25, "bw": 1.05, "bh": 0.8, "head_r": 44})
D["cougar"] = Q(**{**SPOT, "pattern": None, "body": "#C9A27A"})
D["lynx"] = Q(**{**SPOT, "pattern": "spots", "body": "#C9B79A", "ears": "pointy", "tail": "short", "pat_c": "#8C7560"})
D["bobcat"] = Q(**{**SPOT, "pattern": "spots", "body": "#B08A60", "ears": "pointy", "tail": "short", "pat_c": "#6E5A4A"})
D["caracal"] = Q(**{**SPOT, "pattern": None, "body": "#D9A066", "ears": "long", "ear_in": "#3A3A44"})
D["black-panther"] = Q(**{**SPOT, "pattern": None, "body": "#2E2A3B", "belly": None, "snout_c": "#3A3A44", "chin": None})

# ---------------------------------------------------------------- marine mammals
D["whale"] = lambda s: cetacean(s, spout=True)
D["blue-whale"] = lambda s: cetacean(s, body="#4C78A8", belly="#9DB7D5", length=1.05, height=0.8, spout=True)
D["humpback-whale"] = lambda s: cetacean(s, body="#3A4A5E", belly="#D9E2EC", flipper_long=True, height=1.0)
D["sperm-whale"] = lambda s: cetacean(s, body="#5A5A66", belly="#8C96A3", height=1.1, dorsal=False)
D["killer-whale"] = lambda s: cetacean(s, body="#2E2A3B", belly=WHITE, height=0.9)
D["beluga-whale"] = lambda s: cetacean(s, body="#F4F1EA", belly=WHITE, dorsal=False, height=0.95)
D["narwhal"] = lambda s: cetacean(s, body="#8C96A3", belly="#D9DEE5", tusk=True, dorsal=False, length=0.85)
D["dolphin"] = lambda s: cetacean(s, body="#7A9CC6", belly="#E5EEF8", beak=True, length=0.95, height=0.75)
D["porpoise"] = lambda s: cetacean(s, body="#6B7A8C", belly="#D9DEE5", length=0.8, height=0.75)
D["seal"] = lambda s: seal(s)
D["sea-lion"] = lambda s: seal(s, body="#8C6A50", sea_lion=True)
D["walrus"] = lambda s: seal(s, body="#B08A6A", tusks=True)
D["manatee"] = lambda s: cetacean(s, body="#8C96A3", belly="#A6AEB9", dorsal=False, length=0.85, height=1.1)
D["dugong"] = lambda s: cetacean(s, body="#9A8A7A", belly="#B7A898", dorsal=False, length=0.85, height=1.0)
D["sea-otter"] = Q(body="#6E5A4A", head_c="#C9B79A", ears="round", snout="round", snout_c="#E8DCC8", tail="long", whiskers=True, bw=1.1, bh=0.7, leg=0.35, head_r=48)


# ---------------------------------------------------------------- birds
BLUE, DBLUE, SKY, PURPLE = C["blue"], C["darkblue"], C["sky"], C["purple"]


def penguin(s, body="#2E2A3B", front=WHITE, beak=ORANGE, patch=None, size=1.0):
    s.open(transform=f"translate(256 446) scale({size}) translate(-256 -446)")
    for x in (220, 292):
        s.F("ellipse", cx=x, cy=436, rx=34, ry=12, fill=ORANGE)
    s.F("ellipse", cx=256, cy=290, rx=120, ry=160, fill=body)
    s.F("ellipse", outline=False, cx=256, cy=320, rx=84, ry=124, fill=front)
    for sgn in (1, -1):
        s.F("ellipse", cx=256 + sgn * 120, cy=300, rx=26, ry=80, fill=body, transform=f"rotate({sgn * -15} {256 + sgn * 120} 300)")
    if patch:
        for sgn in (1, -1):
            s.F("ellipse", outline=False, cx=256 + sgn * 70, cy=200, rx=24, ry=34, fill=patch)
    eye(s, 226, 180, 10, "left")
    eye(s, 286, 180, 10, "right")
    s.F("polygon", points="240,200 272,200 256,232", fill=beak)
    s.close()


def owl(s, body="#8C6A50", face="#E8DCC8", belly="#C9A27A", tufts=True):
    for x in (226, 286):
        s.F("ellipse", cx=x, cy=440, rx=22, ry=10, fill=C["yellow"])
    if tufts:
        s.F("polygon", points="150,130 176,60 210,120", fill=body)
        s.F("polygon", points="362,130 336,60 302,120", fill=body)
    s.F("ellipse", cx=256, cy=280, rx=140, ry=170, fill=body)
    s.F("ellipse", outline=False, cx=256, cy=330, rx=90, ry=110, fill=belly)
    for sgn in (1, -1):
        s.F("ellipse", cx=256 + sgn * 130, cy=300, rx=30, ry=90, fill=shade(body, 0.85), transform=f"rotate({sgn * -10} {256 + sgn * 130} 300)")
    s.F("path", d="M136 200 C136 130 236 120 256 170 C276 120 376 130 376 200 C376 260 296 260 256 240 C216 260 136 260 136 200Z", fill=face)
    for x, side in ((204, "left"), (308, "right")):
        s.F("circle", cx=x, cy=196, r=40, fill=WHITE)
        s.F("circle", outline=False, cx=x, cy=196, r=26, fill=C["orange"])
        eye(s, x, 196, 15, side)
    s.F("polygon", points="242,220 270,220 256,250", fill=C["darkgold"])


def peacock(s, female=False):
    if not female:
        s.F("path", d="M240 360 C60 380 20 160 140 70 C220 40 320 40 400 90 C440 140 420 260 300 340Z", fill="#2F8A4A")
        for k in range(11):
            a = 200 + k * 13
            x, y = 240 + 170 * math.cos(math.radians(a)), 330 + 230 * math.sin(math.radians(a))
            s.F("ellipse", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", rx=20, ry=26, fill=C["gold"])
            s.F("ellipse", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", rx=12, ry=16, fill=BLUE)
            s.F("ellipse", outline=False, cx=f"{x:.0f}", cy=f"{y + 3:.0f}", rx=6, ry=8, fill="#1E3A8A")
    for x in (236, 276):
        s.T(f"M{x} 390 V440", C["darkgrey"], 8)
    s.F("ellipse", cx=256, cy=350, rx=56, ry=60, fill="#1E5FB4" if not female else "#8C7560")
    s.T("M270 310 C280 260 270 220 270 190", "#1E5FB4" if not female else "#8C7560", 30)
    s.F("circle", cx=272, cy=180, r=26, fill="#1E5FB4" if not female else "#8C7560")
    s.M("M266 154 L258 120 M272 154 L272 118 M278 154 L286 120", "#1E5FB4" if not female else "#8C7560", 4)
    s.F("polygon", points="296,178 318,184 296,192", fill=C["darkgrey"])
    eye(s, 280, 176, 5)


D["bird"] = B(body=SKY, wing=BLUE, belly=WHITE, beak="short", beak_c=ORANGE, tail="fan")
D["sparrow"] = B(body="#A0703E", wing="#6E4A2A", belly="#E8DCC8", head_c="#8C6239", cheek="#E8DCC8", beak="short", beak_c=DGREY, tail="short")
D["crow"] = B(body="#2E2A3B", beak="short", beak_c="#2E2A3B", legs_c="#2E2A3B", tail="fan")
D["raven"] = B(body="#1F1F24", wing="#2E2A3B", beak="hook", beak_c="#1F1F24", legs_c="#1F1F24", tail="fan", size=1.1)
D["pigeon"] = B(body="#9AA3AF", wing="#7A8290", head_c="#6B7A8C", beak="short", beak_c=DGREY, legs_c=PINK, tail="fan", cheek="#7FB8A0")
D["dove"] = B(body="#F4F1EA", wing="#E5E7EB", beak="short", beak_c=PINK, legs_c=PINK, tail="fan")
D["macaw"] = B(body=RED, wing=BLUE, head_c=RED, beak="hook", beak_c="#F4F1EA", tail="long", tail_c=BLUE, cheek=WHITE, legs_c=DGREY)
D["cockatoo"] = B(body=WHITE, wing="#F4F1EA", crest=YEL, beak="hook", beak_c=DGREY, tail="fan", legs_c=DGREY)
D["budgie"] = B(body="#7DD36B", wing="#3A7A3A", head_c=YEL, beak="hook", beak_c="#E8B878", tail="long", tail_c=BLUE, legs_c=PINK, size=0.85)
D["peacock"] = lambda s: peacock(s)
D["peahen"] = lambda s: (s.open(transform="translate(256 446) scale(1.7) translate(-256 -446)"), peacock(s, female=True), s.close())
D["robin"] = B(body="#8C6A50", wing="#6E5A4A", belly="#E8782B", beak="short", beak_c=DGREY, tail="short")
D["blue-jay"] = B(body=BLUE, wing="#2C5FC9", belly=WHITE, crest=BLUE, beak="short", beak_c=BLACK, tail="long", legs_c=DGREY)
D["cardinal-bird"] = B(body=RED, wing="#B5323A", crest=RED, beak="short", beak_c=ORANGE, tail="long", legs_c=DGREY)
D["hummingbird"] = B(body="#2F8A4A", wing="#4CB963", belly="#C1442E", beak="long", beak_c=BLACK, tail="short", size=0.8, leg=0.5)
D["kingfisher"] = B(body=BLUE, wing="#1E5FB4", belly=ORANGE, beak="long", beak_c=BLACK, tail="short", legs_c=RED)
D["woodpecker"] = B(body="#2E2A3B", wing=WHITE, crest=RED, beak="long", beak_c=DGREY, tail="fan", belly=WHITE)
D["toucan"] = B(body="#1F1F24", wing="#2E2A3B", cheek=YEL, beak="big", beak_c=ORANGE, tail="fan", legs_c=BLUE)
D["hornbill"] = B(body="#2E2A3B", belly=WHITE, beak="big", beak_c=YEL, tail="long", tail_c=WHITE, legs_c=DGREY)
D["myna"] = B(body="#5E4A3E", head_c="#1F1F24", eye_ring=YEL, beak="short", beak_c=YEL, legs_c=YEL, tail="fan")
D["bulbul"] = B(body="#8C7560", head_c="#1F1F24", crest="#1F1F24", cheek=WHITE, beak="short", beak_c=BLACK, tail="long", legs_c=DGREY)
D["cuckoo"] = B(body="#7A8290", wing="#5A6270", belly="#E5E7EB", beak="short", beak_c=YEL, tail="long", legs_c=YEL)
D["koel"] = B(body="#1F1F24", beak="short", beak_c="#9AB84A", eye_ring=RED, tail="long", legs_c=DGREY)
D["nightingale"] = B(body="#A0703E", wing="#8C6239", belly="#E8DCC8", beak="short", beak_c=DGREY, tail="fan", size=0.9)
D["canary"] = B(body=YEL, wing="#E8B030", beak="short", beak_c=PINK, tail="fan", legs_c=PINK, size=0.85)
D["finch"] = B(body="#E8782B", wing="#5E4A3E", head_c=RED, belly="#F2D3B0", beak="short", beak_c=DGREY, tail="short", size=0.85)
D["swallow"] = B(body="#1E3A8A", wing="#1E3A8A", belly=WHITE, cheek="#C1442E", beak="short", beak_c=BLACK, tail="long", legs_c=BLACK, size=0.9)
D["starling"] = B(body="#2E3A3A", wing="#2F5A5A", beak="long", beak_c=YEL, tail="short", legs_c=PINK)
D["magpie"] = B(body="#1F1F24", wing=WHITE, belly=WHITE, beak="short", beak_c=BLACK, tail="long", tail_c="#1F3A5A", legs_c=BLACK)
D["lark"] = B(body="#B08A60", wing="#8C6A50", belly="#E8DCC8", crest="#8C6A50", beak="short", beak_c=DGREY, tail="fan")
D["wren"] = B(body="#8C6239", wing="#6E4A2A", beak="short", beak_c=DGREY, tail="up", size=0.8)
D["weaver-bird"] = lambda s: (s.F("path", d="M300 60 C380 60 420 160 380 260 C350 320 260 320 240 260 C220 200 240 80 300 60Z", fill="#C9A27A"),
                              s.M("M260 120 C300 140 340 110 380 130 M250 180 C300 200 350 170 390 190 M260 240 C300 260 340 230 370 250", "#8C7560", 6),
                              s.F("circle", outline=False, cx=320, cy=260, r=26, fill="#3A2E28"),
                              s.open(transform="translate(130 360) scale(0.4) translate(-256 -256)"),
                              bird(s, body=YEL, wing="#C9A22A", head_c="#3A3A44", beak="short", beak_c=DGREY, tail="short"), s.close())
D["lyrebird"] = B(body="#8C7560", wing="#6E5A4A", beak="short", beak_c=DGREY, tail="up", tail_c="#A58B70", size=1.0)
D["bird-of-paradise"] = B(body="#5E2E1E", head_c="#E8B030", cheek="#2F8A4A", beak="short", beak_c=SKY, tail="long", tail_c=YEL, legs_c=DGREY)
D["kiwi-bird"] = B(body="#8C6A50", wing="#8C6A50", beak="long", beak_c="#E8C39E", tail="short", leg=0.5, legs_c="#E8C39E", size=1.1)
D["ostrich"] = B(body="#2E2A3B", wing=WHITE, tail="fan", tail_c=WHITE, head_c="#E8C39E", beak="short", beak_c="#E8C39E", neck=1.0, leg=2.2, legs_c="#E8C39E", size=0.9)
D["emu"] = B(body="#6E5A4A", wing="#5E4A3E", head_c="#3A5A7A", beak="short", beak_c=DGREY, neck=0.9, leg=2.0, legs_c="#5A5A66", size=0.9, tail="short")
D["cassowary"] = B(body="#1F1F24", head_c=BLUE, crest="#C9A27A", wattle=RED, beak="short", beak_c=DGREY, neck=0.7, leg=1.8, legs_c="#5A5A66", size=0.95, tail="short")
D["rhea"] = B(body="#9AA3AF", wing="#7A8290", beak="short", beak_c=DGREY, neck=0.9, leg=1.9, legs_c="#C9A27A", size=0.85, tail="short")
D["dodo-bird"] = B(body="#9AA3AF", wing="#7A8290", beak="hook", beak_c="#E8D06E", tail="up", tail_c=WHITE, leg=0.6, legs_c="#E8D06E", size=1.2)
D["turkey"] = B(body="#6E4A2A", wing="#5E3E22", head_c="#8FA6C9", wattle=RED, beak="short", beak_c="#E8B878", tail="up", tail_c="#8C6239", legs_c="#E8B878", size=1.15)
D["rooster"] = B(body="#C1662E", wing="#8E3E1E", head_c="#E8782B", beak="short", beak_c=YEL, comb=RED, wattle=RED, tail="up", tail_c="#1F3A2A", legs_c=YEL, size=1.05)
D["chick"] = B(body=YEL, wing="#F2B930", beak="short", beak_c=ORANGE, tail="short", legs_c=ORANGE, size=0.9, leg=0.6)
D["quail"] = B(body="#A0703E", wing="#8C6239", belly="#E8DCC8", beak="short", beak_c=DGREY, crest="#3A2E28", tail="short", leg=0.5)
D["pheasant"] = B(body="#C1662E", wing="#8E3E1E", head_c="#2F8A4A", cheek=RED, beak="short", beak_c="#E8D06E", tail="long", tail_c="#8C6239")
D["guinea-fowl"] = B(body="#3A3A44", wing="#3A3A44", head_c=BLUE, wattle=RED, beak="short", beak_c="#E8B878", tail="short", leg=0.8)
D["partridge"] = B(body="#9A8A7A", wing="#8C7560", head_c="#C67A4A", beak="short", beak_c=RED, tail="short", legs_c=RED, leg=0.6)
D["roadrunner"] = B(body="#8C7560", wing="#6E5A4A", crest="#3A3A44", beak="long", beak_c=DGREY, tail="long", leg=1.3, legs_c=DGREY)
D["crane-bird"] = B(body="#E5E7EB", wing="#9AA3AF", head_c=WHITE, crest=None, cheek=RED, beak="long", beak_c=DGREY, neck=0.9, leg=2.0, legs_c=DGREY, size=0.85, tail="fan", tail_c="#3A3A44")
EAGLE = dict(body=DBROWN, head_c=WHITE, beak="hook", beak_c=YEL, tail="fan", tail_c=WHITE, legs_c=YEL, size=1.1)
D["bald-eagle"] = B(**EAGLE)
D["golden-eagle"] = B(**{**EAGLE, "head_c": "#C9963A", "tail_c": DBROWN})
D["hawk"] = B(**{**EAGLE, "body": "#8C6239", "head_c": "#A0703E", "belly": "#F2D3B0", "tail_c": "#C1662E", "size": 1.0})
D["falcon"] = B(**{**EAGLE, "body": "#5A6270", "head_c": "#3A3A44", "belly": "#E8DCC8", "tail_c": "#5A6270", "size": 0.95})
D["peregrine-falcon"] = B(**{**EAGLE, "body": "#4A5260", "head_c": "#2E2A3B", "cheek": WHITE, "belly": "#F4F1EA", "tail_c": "#4A5260", "size": 0.95})
D["kite-bird"] = B(**{**EAGLE, "body": "#A0582E", "head_c": "#E8DCC8", "tail": "long", "tail_c": "#A0582E"})
D["vulture"] = B(body="#3A2E28", wing="#2E2A3B", head_c=PINK, beak="hook", beak_c="#E8DCC8", tail="fan", legs_c=DGREY, neck=0.3, size=1.1, belly="#6E5A4A")
D["condor"] = B(body="#1F1F24", head_c="#C1442E", beak="hook", beak_c="#E8DCC8", tail="fan", legs_c=DGREY, neck=0.3, size=1.15)
D["osprey"] = B(**{**EAGLE, "body": "#4A3B32", "belly": WHITE, "head_c": WHITE, "tail_c": "#4A3B32"})
D["secretary-bird"] = B(body="#C9CED6", wing="#2E2A3B", crest="#2E2A3B", cheek=ORANGE, beak="hook", beak_c=DGREY, neck=0.5, leg=2.2, legs_c="#E8B878", tail="long", tail_c="#2E2A3B", size=0.85)
D["owl"] = lambda s: owl(s)
D["barn-owl"] = lambda s: owl(s, body="#D9A066", face=WHITE, belly="#F7E3C4", tufts=False)
D["snowy-owl"] = lambda s: owl(s, body="#F4F1EA", face=WHITE, belly=WHITE, tufts=False)
D["duckling"] = B(body=YEL, wing="#F2B930", beak="duck", beak_c=ORANGE, tail="short", swim=True, size=0.85)
D["goose"] = B(body="#F4F1EA", wing="#E5E7EB", beak="short", beak_c=ORANGE, legs_c=ORANGE, neck=0.5, tail="short")
D["swan"] = B(body=WHITE, wing="#F4F1EA", beak="short", beak_c=ORANGE, neck=0.8, swim=True, tail="up", tail_c=WHITE)
D["penguin"] = lambda s: penguin(s)
D["emperor-penguin"] = lambda s: penguin(s, patch=YEL)
D["pelican"] = B(body=WHITE, wing="#E5E7EB", beak="pouch", beak_c="#E8B030", tail="short", legs_c=ORANGE, size=1.05, neck=0.3)
D["stork"] = B(body=WHITE, wing="#2E2A3B", beak="long", beak_c=RED, neck=0.6, leg=2.0, legs_c=RED, size=0.85, tail="short")
D["heron"] = B(body="#9AA3AF", wing="#7A8290", head_c=WHITE, crest="#2E2A3B", beak="long", beak_c=YEL, neck=0.9, leg=1.9, legs_c=YEL, size=0.85, tail="short")
D["egret"] = B(body=WHITE, wing="#F4F1EA", beak="long", beak_c=YEL, neck=0.9, leg=1.9, legs_c=BLACK, size=0.8, tail="short")
D["seagull"] = B(body=WHITE, wing="#9AA3AF", beak="short", beak_c=YEL, legs_c=PINK, tail="short")
D["albatross"] = B(body=WHITE, wing="#3A3A44", beak="hook", beak_c=PINK, legs_c=PINK, tail="short", size=1.1)
D["puffin"] = B(body="#1F1F24", belly=WHITE, cheek=WHITE, beak="big", beak_c=ORANGE, legs_c=ORANGE, tail="short", size=0.9, leg=0.6)
D["cormorant"] = B(body="#1F1F24", wing="#2E3A3A", beak="hook", beak_c=YEL, neck=0.5, legs_c=BLACK, tail="fan")
D["ibis"] = B(body=RED, wing="#B5323A", beak="long", beak_c="#3A3A44", neck=0.6, leg=1.6, legs_c=RED, size=0.85, tail="short")
D["spoonbill"] = B(body="#F7A1B5", wing="#F48AA6", beak="long", beak_c="#9AA3AF", neck=0.6, leg=1.6, legs_c="#C1442E", size=0.85, tail="short")

# ---------------------------------------------------------------- fish
D["fish"] = F(body=BLUE, belly=SKY, tail="fork")
D["angelfish"] = F(body="#E8D06E", stripes=3, stripe_c="#2E2A3B", dorsal="tall", tail="fork", length=0.6, height=1.2)
D["betta-fish"] = F(body=RED, tail="fan", dorsal="tall", fin="#8E2128", length=0.75)
D["guppy"] = F(body="#9AA3AF", tail="fan", fin=ORANGE, length=0.6, height=0.7)
D["salmon"] = F(body="#E88A6A", belly="#F7C4B0", spots="#6E4A3A", tail="fork", length=1.15, height=0.8)
D["trout"] = F(body="#8CA36B", belly="#F2D3B0", spots="#3A3A44", stripes=None, tail="fork", length=1.1, height=0.75)
D["tuna"] = F(body="#2C4A7A", belly="#D9E2EC", tail="crescent", dorsal="small", length=1.15, height=0.9)
D["cod"] = F(body="#9A8A6A", belly="#E8DCC8", spots="#6E5A4A", tail="fork", length=1.05, whisk=True)
D["carp"] = F(body="#C9963A", belly="#F2D3B0", tail="fork", length=1.0, whisk=True)
D["koi"] = F(body=WHITE, spots=ORANGE, tail="fan", fin="#F7D0B0", length=1.0, whisk=True)
D["catfish"] = F(body="#6B6B5A", belly="#B7B7A0", tail="round", length=1.15, height=0.75, whisk=True)
D["piranha"] = F(body="#7A8290", belly=RED, tail="fork", length=0.8, height=1.15, teeth=True)
D["swordfish"] = F(body="#3A5A8C", belly="#D9E2EC", tail="crescent", dorsal="shark", length=0.95, height=0.75, sword=True)
D["marlin"] = F(body="#2C4A7A", belly="#D9E2EC", tail="crescent", dorsal="tall", length=0.95, height=0.75, sword=True)
D["sailfish"] = F(body="#2C5FC9", belly="#D9E2EC", tail="crescent", dorsal="tall", fin="#3A7AD9", length=0.95, height=0.7, sword=True)
D["barracuda"] = F(body="#9AA3AF", belly=WHITE, tail="fork", length=1.3, height=0.55, teeth=True)
D["pufferfish"] = lambda s: (fish(s, body="#E8D06E", belly="#FFF3C0", tail="round", length=0.75, height=1.6, spots="#8C7A3A"),
                             [s.M(f"M{x:.0f} {y:.0f} l{dx} {dy}", "#8C7A3A", 5) for x, y, dx, dy in ((200, 110, -6, -20), (260, 102, 0, -20), (320, 112, 8, -18), (200, 400, -6, 20), (260, 410, 0, 20), (320, 400, 8, 18))])
D["lionfish"] = F(body="#E8DCC8", stripes=5, stripe_c="#C1442E", dorsal="spiky", fin="#C1442E", tail="fan", length=0.85)
D["anglerfish"] = lambda s: (fish(s, body="#4A3B32", belly="#6E5A4A", tail="round", length=0.8, height=1.2, teeth=True),
                             s.T("M360 170 C380 90 440 80 460 120", "#4A3B32", 8), s.F("circle", cx=462, cy=130, r=18, fill="#FFE38A"))
D["seahorse"] = lambda s: (s.T("M270 400 C200 420 190 470 240 470 C270 470 270 440 250 440", "#E8B030", 22),
                           s.F("path", d="M240 150 C300 150 330 210 310 280 C300 330 260 360 270 400 C230 400 200 360 210 300 C215 260 200 220 210 190Z", fill="#E8B030"),
                           s.F("ellipse", cx=260, cy=140, rx=50, ry=36, fill="#E8B030"), s.F("rect", x=296, y=132, width=70, height=22, rx=10, fill="#E8B030"),
                           s.F("path", d="M200 250 C170 240 160 290 196 300Z", fill="#F2C94C"), [s.M(f"M{x} {y} l18 0", "#B88A20", 5) for x, y in ((250, 200), (260, 250), (250, 300), (240, 350))],
                           eye(s, 268, 132, 8))
D["eel"] = lambda s: (s.T("M60 300 C120 200 200 380 280 280 C340 210 390 250 430 240", "#5A6A3A", 50), eye(s, 420, 230, 7))
D["moray-eel"] = lambda s: (s.T("M60 360 C120 260 200 420 280 320 C340 250 390 290 430 270", "#5A7A3A", 56), s.M("M80 340 C140 260 210 400 280 310", "#8CA35A", 10, dash="16 18"), eye(s, 420, 258, 8))
D["electric-eel"] = lambda s: (s.T("M60 360 C120 260 200 420 280 320 C340 250 390 290 430 270", "#3A3A44", 50),
                               s.M("M150 200 L170 160 L160 160 L180 120 M330 180 L350 140 L340 140 L360 100", YEL, 8), eye(s, 420, 258, 7))
D["flying-fish"] = lambda s: (fish(s, body="#3A7AD9", belly="#D9E2EC", tail="fork", length=0.9, height=0.7),
                              s.F("path", d="M260 230 C200 120 120 100 80 110 C140 160 190 220 240 250Z", fill="#8FB8F0"))
D["mudskipper"] = F(body="#8C7A5A", belly="#C9B79A", spots="#5E4A3E", tail="round", length=0.95, height=0.6, eye_r=14)
D["sardine"] = F(body="#7A9CC6", belly="#E5EEF8", tail="fork", length=1.1, height=0.5)
D["mackerel"] = F(body="#2F6A6A", belly="#E5EEF8", stripes=6, stripe_c="#1F3A3A", tail="fork", length=1.1, height=0.6)
D["herring"] = F(body="#6B8CB0", belly="#E5EEF8", tail="fork", length=1.1, height=0.55)
D["hilsa"] = F(body="#B7C3D1", belly="#F4F6F9", tail="fork", length=1.0, height=0.85)
D["rohu"] = F(body="#8C9AA8", belly="#E8D9C8", tail="fork", length=1.05, height=0.85)
D["pomfret"] = F(body="#C9CED6", belly="#F4F6F9", tail="fork", length=0.7, height=1.3, dorsal="small")
D["surgeonfish"] = F(body="#1E5FB4", belly="#2C6BD6", stripes=None, tail="fork", fin=YEL, length=0.8, height=1.05)
D["parrotfish"] = F(body="#2FB8A0", belly="#9BE0D0", spots=PINK, tail="fan", length=0.95, height=0.95)
D["grouper"] = F(body="#8C6A50", belly="#C9A27A", spots="#5E4A3E", tail="round", length=1.1, height=1.0)
D["sunfish"] = lambda s: (s.F("path", d="M230 150 C240 80 270 40 290 40 C300 90 300 130 290 160Z", fill="#7A8290"),
                          s.F("path", d="M230 360 C240 430 270 470 290 470 C300 420 300 380 290 350Z", fill="#7A8290"),
                          s.F("path", d="M120 220 C100 250 100 270 120 300 C130 290 140 270 140 256 C140 240 130 230 120 220Z", fill="#7A8290"),
                          s.F("ellipse", cx=270, cy=256, rx=150, ry=130, fill="#9AA3AF"), s.F("ellipse", outline=False, cx=280, cy=300, rx=110, ry=70, fill="#C9CED6"),
                          s.M("M400 270 q-14 6 -24 0", BLACK, 6), eye(s, 360, 230, 12))

# ---------------------------------------------------------------- sharks and rays
SHARK = dict(body="#7A8CA3", belly=WHITE, tail="crescent", dorsal="shark", length=1.25, height=0.75, teeth=True)
D["great-white-shark"] = F(**SHARK)
D["hammerhead-shark"] = lambda s: (fish(s, **{**SHARK, "body": "#8C9AA8"}), s.F("rect", x=420, y=200, width=40, height=110, rx=14, fill="#8C9AA8"))
D["whale-shark"] = F(**{**SHARK, "body": "#3A5A7A", "spots": WHITE, "teeth": False, "length": 1.3, "height": 0.9})
D["tiger-shark"] = F(**{**SHARK, "body": "#7A8290", "stripes": 5, "stripe_c": "#5A6270"})
D["bull-shark"] = F(**{**SHARK, "body": "#6B7280", "height": 0.9})
D["megamouth-shark"] = F(**{**SHARK, "body": "#5A5A66", "height": 0.95, "teeth": True})


def ray(s, body="#8C96A3", belly=None, tail_c=None, horns=False, spots=None):
    s.T("M256 320 C260 380 250 430 230 480", tail_c or body, 10)
    s.F("path", d="M256 120 C300 140 360 200 470 240 C380 280 320 300 256 330 C192 300 132 280 42 240 C152 200 212 140 256 120Z", fill=body)
    if horns:
        s.F("path", d="M230 130 C220 100 230 80 240 76 L250 124Z", fill=body)
        s.F("path", d="M282 130 C292 100 282 80 272 76 L262 124Z", fill=body)
    if spots:
        for x, y in ((200, 220), (310, 220), (256, 260), (180, 260), (330, 260)):
            s.F("circle", outline=False, cx=x, cy=y, r=10, fill=spots)
    eye(s, 236, 170, 7, "left")
    eye(s, 276, 170, 7, "right")


D["stingray"] = lambda s: ray(s, body="#A08A6A", spots="#6E5A4A")
D["manta-ray"] = lambda s: ray(s, body="#2E3A4A", horns=True)
D["sawfish"] = lambda s: (fish(s, body="#8C8A6A", belly="#D9D6C0", tail="fork", dorsal="shark", length=1.2, height=0.55),
                          s.F("rect", x=440, y=244, width=60, height=22, rx=6, fill="#8C8A6A"), [s.M(f"M{x} 240 v-10 M{x} 270 v10", WHITE, 4) for x in range(446, 500, 10)])

# ---------------------------------------------------------------- sea invertebrates
D["jellyfish"] = lambda s: ([s.T(f"M{x} 250 C{x - 20} 320 {x + 20} 380 {x} 460", "#C9A6E8", 8) for x in (180, 220, 256, 292, 332)],
                            s.F("path", d="M110 260 C110 120 402 120 402 260 C360 280 330 250 300 270 C270 250 240 280 210 260 C180 280 150 250 110 260Z", fill="#E0B8F0"),
                            s.F("path", outline=False, d="M170 200 C180 160 220 140 250 140 C220 170 200 190 190 220Z", fill="#F2DCF8"), eye(s, 220, 210, 8, "left"), eye(s, 290, 210, 8, "right"))
D["octopus"] = lambda s: ([s.T(f"M{x0} 300 C{x0 + dx} 360 {x0 + dx * 2} 400 {x0 + dx * 3} 440", "#E8782B", 30) for x0, dx in ((170, -30), (210, -12), (256, 0), (300, 12), (340, 30))],
                          s.F("ellipse", cx=256, cy=210, rx=130, ry=120, fill="#F5913E"), s.F("ellipse", outline=False, cx=210, cy=160, rx=30, ry=40, fill="#F9B57A"),
                          eye(s, 216, 230, 14, "left"), eye(s, 296, 230, 14, "right"))
D["squid"] = lambda s: (s.F("path", d="M256 40 L340 120 C330 200 320 260 300 300 H212 C192 260 182 200 172 120Z", fill="#F2A6A0"),
                        [s.T(f"M{x} 300 C{x} 360 {x + (x - 256) // 3} 420 {x + (x - 256) // 2} 470", "#E88A80", 14) for x in (220, 240, 256, 272, 292)],
                        eye(s, 230, 260, 12, "left"), eye(s, 282, 260, 12, "right"))
D["giant-squid"] = lambda s: (D["squid"](s), s.T("M220 300 C150 380 120 440 60 470 M292 300 C362 380 392 440 452 470", "#E88A80", 18))
D["cuttlefish"] = lambda s: (s.F("ellipse", cx=230, cy=256, rx=180, ry=90, fill="#C9A27A"), s.M("M80 220 C160 200 300 200 400 220", "#8C6A50", 8, dash="18 12"),
                             [s.T(f"M400 {y} C440 {y} 460 {y + (y - 256) // 2} 490 {y + (y - 256)}", "#B08A60", 12) for y in (230, 256, 282)], eye(s, 360, 240, 14))
D["nautilus"] = lambda s: (s.F("circle", cx=250, cy=256, r=170, fill="#F4E8D8"), [s.M(f"M250 256 L{x:.0f} {y:.0f}", "#C1662E", 14) for x, y in (arc_pt(250, 256, 170, a) for a in range(-160, 60, 30))],
                           s.M("M250 256 C250 200 320 200 320 256 C320 330 200 330 200 256 C200 160 350 160 350 256", "#C9A27A", 8),
                           [s.T(f"M380 {y} L460 {y + (y - 300) // 3}", "#E8C39E", 10) for y in (270, 300, 330)], eye(s, 380, 290, 9))
D["starfish"] = lambda s: (s.F("polygon", points=star_pts(256, 266, 210, 80, 5), fill=ORANGE), [s.F("circle", outline=False, cx=f"{x:.0f}", cy=f"{y:.0f}", r=8, fill="#F9C98A") for x, y in (arc_pt(256, 266, 120, a) for a in range(-90, 270, 72))])
D["sea-urchin"] = lambda s: ([s.M(f"M256 290 L{x:.0f} {y:.0f}", "#5A2E5A", 8) for x, y in (arc_pt(256, 290, 190, a) for a in range(0, 360, 12))], s.F("circle", cx=256, cy=290, r=110, fill="#7A3A7A"))
D["sea-cucumber"] = lambda s: (s.F("path", d="M60 320 C80 220 420 200 460 300 C440 360 80 380 60 320Z", fill="#8C5A3A"), [s.F("circle", outline=False, cx=x, cy=y, r=9, fill="#B07A50") for x, y in ((120, 290), (180, 270), (250, 260), (320, 265), (390, 280))],
                               [s.M(f"M60 320 l-20 {d}", "#E8C39E", 6) for d in (-30, 0, 30)])
D["sea-anemone"] = lambda s: ([s.T(f"M256 330 C{256 + dx} 260 {256 + dx * 1.3} 200 {256 + dx * 1.2} 140", "#F48AA6", 16) for dx in (-140, -90, -40, 0, 40, 90, 140)],
                              s.F("path", d="M140 440 C140 340 372 340 372 440Z", fill="#E05A7A"))
D["coral"] = lambda s: (s.T("M256 460 V300 M256 360 C200 330 160 260 170 180 M256 330 C320 300 350 240 340 160 M200 270 C160 250 130 220 120 180 M330 230 C370 210 400 180 400 140", "#F5806A", 34),
                        s.F("rect", x=170, y=440, width=172, height=30, rx=10, fill="#C9A27A"))
D["crab-animal"] = lambda s: ([s.T(f"M{256 + sgn * 70} {y} L{256 + sgn * 160} {y + 20} L{256 + sgn * 190} {y + 70}", "#D9472B", 14) for sgn in (1, -1) for y in (300, 330, 360)],
                              [s.T(f"M{256 + sgn * 90} 260 L{256 + sgn * 150} 190", "#D9472B", 20) for sgn in (1, -1)],
                              [s.F("path", d=f"M{256 + sgn * 150} 190 C{256 + sgn * 120} 130 {256 + sgn * 190} 100 {256 + sgn * 210} 150 L{256 + sgn * 170} 160 L{256 + sgn * 200} 190 C{256 + sgn * 190} 210 {256 + sgn * 160} 210 {256 + sgn * 150} 190Z", fill="#E8583B") for sgn in (1, -1)],
                              s.F("ellipse", cx=256, cy=320, rx=130, ry=80, fill="#E8583B"), s.T("M226 250 V210 M286 250 V210", "#D9472B", 8), eye(s, 226, 200, 12, "left"), eye(s, 286, 200, 12, "right"))
D["hermit-crab"] = lambda s: (s.F("path", d="M140 360 C100 260 180 150 290 170 C380 190 400 300 330 360Z", fill="#E8C39E"), s.M("M200 300 C200 240 260 220 290 250 C320 280 290 320 260 300", "#B08A60", 10),
                              s.F("ellipse", cx=360, cy=360, rx=60, ry=40, fill="#E8583B"), s.T("M380 330 V290 M400 334 V300", "#D9472B", 8), eye(s, 380, 284, 9, "left"), eye(s, 400, 296, 9, "right"),
                              s.T("M400 370 L460 360 L470 400", "#D9472B", 16))
D["lobster"] = lambda s: (s.F("path", d="M100 260 L60 220 L40 280 L60 330 L100 290Z", fill="#C1442E"), [s.F("ellipse", cx=x, cy=270, rx=34, ry=50, fill="#D9472B") for x in (120, 170, 220)],
                          s.F("ellipse", cx=300, cy=270, rx=90, ry=60, fill="#E8583B"), [s.T(f"M330 {y} C380 {y - 40} 410 {y - 60} 430 {y - 60}", "#D9472B", 16) for y in (240, 300)],
                          s.F("ellipse", cx=440, cy=180, rx=44, ry=26, fill="#E8583B"), s.F("ellipse", cx=440, cy=360, rx=44, ry=26, fill="#E8583B"),
                          s.M("M380 250 C440 210 470 150 500 120 M380 290 C440 330 470 380 500 410", "#D9472B", 5), eye(s, 380, 250, 8))
D["shrimp"] = lambda s: (s.T("M140 320 C140 200 260 150 360 200", "#F7A1B5", 70), s.F("polygon", points="130,330 80,390 160,380", fill="#F48AA6"),
                         [s.M(f"M{x} {y} l16 26", "#E88A9A", 6) for x, y in ((180, 230), (230, 200), (280, 190))], s.M("M370 190 C420 150 460 160 490 130 M370 200 C430 200 470 210 500 190", "#E88A9A", 4), eye(s, 360, 186, 9))
D["krill"] = lambda s: (D["shrimp"](s))
D["prawn"] = lambda s: (s.T("M140 320 C140 200 260 150 360 200", "#F08A5A", 70), s.F("polygon", points="130,330 80,390 160,380", fill="#E8783B"),
                        s.M("M370 190 C420 150 460 160 490 130", "#E8783B", 4), eye(s, 360, 186, 9))
D["barnacle"] = lambda s: (s.F("rect", outline=False, x=40, y=400, width=432, height=60, fill="#8C7560"), [s.F("polygon", points=f"{x - 50},{400} {x - 26},{300} {x + 26},{300} {x + 50},{400}", fill="#E8DCC8") for x in (140, 260, 380)],
                           [s.F("ellipse", outline=False, cx=x, cy=302, rx=24, ry=8, fill="#6E5A4A") for x in (140, 260, 380)])
D["sea-sponge"] = lambda s: (s.F("path", d="M140 460 C120 340 150 200 200 120 H312 C362 200 392 340 372 460Z", fill="#E8C74A"), [s.F("ellipse", outline=False, cx=x, cy=y, rx=14, ry=18, fill="#C9A22A") for x, y in ((200, 200), (290, 220), (230, 300), (320, 330), (210, 400), (300, 410))])
D["oyster"] = lambda s: (s.F("path", d="M90 300 C80 380 160 420 260 420 C380 420 440 370 430 300Z", fill="#9AA3AF"),
                         s.F("path", outline=False, d="M120 310 C130 370 200 395 260 395 C350 395 400 360 400 310Z", fill="#E5E7EB"),
                         s.F("path", d="M90 300 C70 200 200 120 300 140 C390 160 440 230 430 300 C380 270 160 270 90 300Z", fill="#8C96A3"),
                         s.M("M130 260 C200 200 320 190 400 250 M150 230 C220 180 320 170 380 210", "#6B7280", 8),
                         s.F("circle", cx=262, cy=340, r=34, fill=WHITE), s.F("circle", outline=False, cx=252, cy=330, r=10, fill="#E8F0FF"))
D["clam"] = lambda s: (s.F("path", d="M80 300 C100 160 412 160 432 300Z", fill="#E8C39E"), [s.M(f"M256 300 L{x:.0f} {y:.0f}", "#C9A27A", 6) for x, y in (arc_pt(256, 300, 170, a) for a in range(200, 341, 20))],
                       s.F("path", d="M80 300 C120 360 392 360 432 300Z", fill="#D9B38C"))
D["mussel"] = lambda s: (s.F("path", d="M120 380 C80 300 180 120 300 110 C380 110 400 200 340 280 C290 340 200 420 120 380Z", fill="#2E2A4A"), s.M("M150 360 C220 300 290 220 320 150", "#4A4A6A", 8))
D["scallop"] = lambda s: (s.F("path", d="M256 400 L90 220 C120 100 392 100 422 220Z", fill="#F2A07A"), [s.M(f"M256 400 L{x:.0f} {y:.0f}", "#D9785A", 8) for x, y in (arc_pt(256, 400, 260, a) for a in range(-150, -29, 15))],
                          s.F("rect", x=210, y=380, width=92, height=40, rx=8, fill="#F2A07A"))
D["sea-slug"] = lambda s: (s.F("path", d="M60 340 C100 260 380 240 450 300 C460 350 100 380 60 340Z", fill="#8B5CF6"), s.M("M100 330 C200 300 330 300 430 310", ORANGE, 12),
                           [s.T(f"M{x} 280 L{x - 10} 230", ORANGE, 12) for x in (180, 230, 280)], s.T("M430 290 L460 250 M440 296 L480 270", "#8B5CF6", 10))
D["horseshoe-crab"] = lambda s: (s.T("M256 380 L256 480", "#6E5A3E", 12), s.F("path", d="M256 400 C140 400 80 300 100 200 C150 120 362 120 412 200 C432 300 372 400 256 400Z", fill="#8C7A5A"),
                                 s.M("M150 250 C200 230 312 230 362 250", "#6E5A3E", 8), eye(s, 200, 210, 8, "left"), eye(s, 312, 210, 8, "right"))


if __name__ == "__main__":
    run("animals", D, sys.argv[1:] or None)
