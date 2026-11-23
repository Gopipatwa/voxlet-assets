"""health-medicine drawings. Run: python drawings/health_medicine.py [ids...]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _animals import BLACK, WHITE, eye, shade, tint  # noqa: E402
from _parts import A1, A1L, A2, A2L, DARK, LIGHT, MID, person  # noqa: E402
from _parts import place as P  # noqa: E402
from _parts2 import calendar, checklist, heart, shield  # noqa: E402
from draw_lib import C, INK, arc_pt, head, run, star_pts, stroke_text  # noqa: E402

D = {}
SKIN, SKIN_D, HAIR = C["skin"], "#E0A878", "#4A3B32"
RED, DRED, GREEN, YEL, ORANGE, PINK, SKY, GREY, DGREY = C["red"], C["darkred"], C["green"], C["yellow"], C["orange"], C["pink"], C["sky"], C["grey"], C["darkgrey"]


def reg(name):
    def r(fn):
        D[name] = fn
        return fn
    return r


def cross(s, x, y, size=40, color=RED):
    w = size * 0.34
    s.F("path", d=f"M{x - w} {y - size} H{x + w} V{y - w} H{x + size} V{y + w} H{x + w} V{y + size} H{x - w} V{y + w} H{x - size} V{y - w} H{x - w}Z", fill=color)


# ---------------------------------------------------------------- medical equipment
@reg("stethoscope")
def _(s):
    s.T("M170 80 C150 200 170 280 256 300 C342 280 362 200 342 80", DGREY, 16)
    s.T("M256 300 V360 C256 420 330 440 360 400", DGREY, 16)
    s.F("circle", cx=380, cy=380, r=50, fill=GREY)
    s.F("circle", cx=380, cy=380, r=28, fill=A1)
    for x in (170, 342):
        s.F("circle", cx=x, cy=74, r=14, fill=DARK)


D["medical-thermometer"] = lambda s: (s.F("rect", x=226, y=60, width=60, height=330, rx=30, fill=WHITE), s.F("circle", cx=256, cy=400, r=50, fill=RED), s.F("rect", outline=False, x=244, y=200, width=24, height=200, fill=RED),
                                      [s.M(f"M226 {y} h18", MID, 5) for y in range(100, 200, 20)])
D["blood-pressure-monitor"] = lambda s: (s.F("rect", x=110, y=110, width=200, height=240, rx=24, fill=WHITE), s.F("rect", outline=False, x=134, y=134, width=152, height=100, rx=8, fill="#B8E0D0"),
                                         s.F("rect", x=330, y=200, width=110, height=180, rx=40, fill=A1), s.T("M310 300 C330 340 330 360 340 380", DGREY, 10))
D["pulse-oximeter"] = lambda s: (s.F("path", d="M140 300 C140 200 372 200 372 300 V360 H140Z", fill=A1), s.F("rect", outline=False, x=180, y=240, width=152, height=70, rx=10, fill="#1F1F24"),
                                 s.M("M196 276 H226 L240 252 L256 300 L270 276 H316", "#5EE89A", 6), s.F("path", d="M120 360 H392 V400 H120Z", fill=SKIN))
D["syringe"] = lambda s: (s.open(transform="rotate(-40 256 256)"), s.F("rect", x=140, y=210, width=220, height=92, rx=12, fill="#E8F4FF"), s.F("rect", outline=False, x=150, y=220, width=120, height=72, fill=A1L),
                          s.F("rect", x=360, y=236, width=40, height=40, fill=GREY), s.T("M400 256 H480", GREY, 6), s.F("rect", x=80, y=196, width=60, height=120, rx=8, fill=GREY), s.T("M40 256 H80", GREY, 16), s.close())
D["needle"] = lambda s: (s.T("M100 412 L380 132", GREY, 14), s.F("path", d="M380 132 L420 92 L400 152Z", fill=GREY), s.F("rect", x=70, y=402, width=50, height=30, rx=6, fill=A1, transform="rotate(-45 95 417)"))
D["ecg-monitor"] = lambda s: (s.F("rect", x=60, y=100, width=392, height=280, rx=24, fill=DARK), s.F("rect", outline=False, x=84, y=124, width=344, height=200, rx=10, fill="#10202A"),
                              s.M("M100 224 H190 L210 160 L236 300 L256 224 H330 L345 190 L360 224 H410", "#5EE89A", 8), s.T("M256 380 V440 M196 440 H316", DGREY, 16))
D["heartbeat-line"] = lambda s: s.M("M40 256 H170 L200 150 L236 380 L270 200 L290 256 H472", RED, 22)
D["x-ray"] = lambda s: (s.F("rect", x=80, y=50, width=352, height=412, rx=20, fill="#1E2A4A"), s.M("M256 90 V420", "#D9E2F0", 16),
                        [s.M(f"M256 {y} C210 {y - 8} 180 {y + 16} 176 {y + 40} M256 {y} C302 {y - 8} 332 {y + 16} 336 {y + 40}", "#D9E2F0", 10) for y in range(120, 330, 40)])
D["mri-scanner"] = lambda s: (s.F("path", d="M80 400 V220 C80 110 432 110 432 220 V400Z", fill=WHITE), s.F("circle", cx=256, cy=260, r=90, fill="#5A6270"),
                              s.F("rect", x=90, y=320, width=440, height=40, rx=12, fill=A1L), s.F("rect", x=60, y=400, width=392, height=30, rx=8, fill=GREY))
D["ct-scanner"] = lambda s: (s.F("circle", cx=230, cy=250, r=170, fill=WHITE), s.F("circle", cx=230, cy=250, r=80, fill="#5A6270"), s.F("rect", x=160, y=300, width=330, height=36, rx=10, fill=A1L),
                             s.F("rect", x=350, y=336, width=40, height=100, fill=GREY))
D["ultrasound-scanner"] = lambda s: (s.F("rect", x=90, y=90, width=260, height=200, rx=20, fill=DARK), s.F("path", outline=False, d="M150 250 L220 120 L290 250Z", fill="#5A6A80"),
                                     s.F("rect", x=130, y=300, width=180, height=120, rx=14, fill=WHITE), s.T("M350 330 C400 330 420 360 420 400", DGREY, 10), s.F("rect", x=396, y=396, width=48, height=60, rx=14, fill=A1))
D["microscope-slide"] = lambda s: (s.F("rect", x=60, y=200, width=392, height=112, rx=10, fill="#E8F4FF"), s.F("rect", x=200, y=216, width=112, height=80, rx=6, fill=A1L, fill_opacity="0.8"),
                                   s.F("circle", outline=False, cx=256, cy=256, r=20, fill=PINK))
D["blood-test-tube"] = lambda s: (s.F("rect", x=206, y=60, width=100, height=380, rx=50, fill="#E8F4FF"), s.F("rect", outline=False, x=212, y=220, width=88, height=214, rx=42, fill=DRED),
                                  s.F("rect", x=196, y=40, width=120, height=50, rx=10, fill=RED), s.F("rect", x=216, y=120, width=80, height=60, fill=WHITE))
D["glucose-meter"] = lambda s: (s.F("rect", x=130, y=80, width=220, height=340, rx=40, fill=A1), s.F("rect", outline=False, x=160, y=120, width=160, height=120, rx=10, fill="#B8E0D0"),
                                s.F("rect", x=210, y=420, width=60, height=60, fill=WHITE), s.F("circle", cx=240, cy=310, r=30, fill=LIGHT))
D["inhaler"] = lambda s: (s.F("path", d="M190 80 H300 V300 H190Z", fill=A1), s.F("path", d="M170 280 H330 V400 H260 V360 H170Z", fill=A2), s.F("rect", x=200, y=60, width=90, height=30, rx=8, fill=A1L))
D["nebuliser"] = lambda s: (s.F("rect", x=60, y=280, width=240, height=150, rx=20, fill=WHITE), s.T("M300 330 C380 330 380 230 330 200", MID, 12), s.F("path", d="M300 120 C300 80 420 80 420 120 V200 H300Z", fill=A1L),
                            s.M("M330 70 C320 50 340 40 330 20 M380 70 C370 50 390 40 380 20", MID, 8))
D["oxygen-mask"] = lambda s: (s.F("path", d="M170 150 C170 100 342 100 342 150 L370 300 C370 360 142 360 142 300Z", fill="#D9EEFB", fill_opacity="0.9"), s.T("M256 360 C256 420 300 450 360 460", "#9AD0E8", 14),
                              s.T("M150 200 C80 200 60 260 90 300 M362 200 C432 200 452 260 422 300", "#5EB85A", 8))
D["oxygen-cylinder"] = lambda s: (s.F("rect", x=190, y=120, width=132, height=340, rx=60, fill="#5EB85A"), s.F("rect", outline=False, x=190, y=120, width=132, height=90, fill=WHITE), s.F("rect", x=226, y=70, width=60, height=60, rx=8, fill=GREY))
D["iv-drip"] = lambda s: (s.T("M256 40 V470 M190 470 H322", DGREY, 12), s.T("M200 60 H312", DGREY, 10), s.F("path", d="M180 80 H300 V240 C300 270 180 270 180 240Z", fill="#D9EEFB"),
                          s.F("rect", outline=False, x=186, y=160, width=108, height=90, rx=16, fill=SKY), s.T("M240 270 C240 340 320 360 360 420", MID, 8))
D["defibrillator"] = lambda s: (s.F("rect", x=100, y=150, width=312, height=240, rx=30, fill=YEL), P(s, heart, 256, 260, 0.3, color=RED), s.M("M180 260 H215 L232 228 L250 292 L268 260 H330", WHITE, 8))
D["otoscope"] = lambda s: (s.F("rect", x=226, y=200, width=60, height=250, rx=20, fill=DARK), s.F("path", d="M210 200 H302 L280 100 H232Z", fill=GREY), s.F("polygon", points="240,100 272,100 262,40 250,40", fill=WHITE))
D["reflex-hammer"] = lambda s: (s.T("M150 430 L330 160", GREY, 18), s.F("path", d="M260 120 C300 90 420 150 410 200 C400 240 320 200 280 180Z", fill=RED))
D["scalpel"] = lambda s: (s.T("M100 400 L300 200", GREY, 24), s.F("path", d="M300 200 L420 120 C420 160 380 220 320 240Z", fill="#D9E2F0"))
D["surgical-mask"] = lambda s: (s.T("M110 210 C60 200 50 280 100 300 M402 210 C452 200 462 280 412 300", WHITE, 8), s.F("path", d="M110 180 C200 160 312 160 402 180 V320 C312 360 200 360 110 320Z", fill="#9AD0E8"),
                                [s.M(f"M120 {y} C200 {y - 10} 312 {y - 10} 392 {y}", "#7FB8D8", 6) for y in (220, 260, 300)])
D["face-mask"] = lambda s: (s.T("M110 210 C60 200 50 280 100 300 M402 210 C452 200 462 280 412 300", DGREY, 8), s.F("path", d="M110 180 C200 150 312 150 402 180 C410 260 380 340 256 360 C132 340 102 260 110 180Z", fill=A1))
D["medical-gloves"] = lambda s: [s.F("path", d=f"M{x - 60} 460 V300 C{x - 80} 260 {x - 90} 220 {x - 80} 200 C{x - 74} 186 {x - 56} 190 {x - 54} 210 V140 C{x - 54} 120 {x - 30} 120 {x - 30} 140 V120 C{x - 30} 100 {x - 6} 100 {x - 6} 120 V130 "
                                              f"C{x - 6} 112 {x + 18} 112 {x + 18} 132 V150 C{x + 18} 134 {x + 42} 134 {x + 42} 152 V320 C{x + 42} 360 {x + 30} 400 {x + 30} 460Z", fill="#9AD0E8") for x in (180, 352)]

# ---------------------------------------------------------------- hospital items
D["hospital-bed"] = lambda s: (s.F("rect", x=60, y=260, width=392, height=60, rx=12, fill=WHITE), s.F("rect", x=60, y=230, width=110, height=40, rx=16, fill=A1L),
                               s.F("rect", x=170, y=240, width=282, height=30, rx=8, fill=A1), s.T("M70 180 V400 M442 230 V400", DGREY, 14), [s.F("circle", cx=x, cy=410, r=16, fill=DARK) for x in (90, 422)])
D["stretcher"] = lambda s: (s.F("rect", x=60, y=230, width=392, height=50, rx=14, fill=A1), s.T("M100 280 L160 400 M412 280 L352 400 M160 280 L100 400 M352 280 L412 400", DGREY, 10),
                            [s.F("circle", cx=x, cy=410, r=16, fill=DARK) for x in (100, 160, 352, 412)])
D["ambulance-bed"] = lambda s: (D["stretcher"](s), s.F("rect", x=70, y=200, width=100, height=40, rx=16, fill=WHITE), s.T("M452 230 V160", DGREY, 10))
D["operating-table"] = lambda s: (s.F("rect", x=70, y=230, width=372, height=50, rx=12, fill="#5EB8A8"), s.T("M256 280 V400", DGREY, 30), s.F("rect", x=170, y=400, width=172, height=30, rx=8, fill=DGREY))
D["surgical-lights"] = lambda s: (s.T("M256 30 V120 M256 120 L150 200 M256 120 L362 200", DGREY, 12), [(s.F("ellipse", cx=x, cy=240, rx=90, ry=50, fill=GREY), s.F("ellipse", outline=False, cx=x, cy=250, rx=60, ry=26, fill="#FFF3B0"))
                                                                                                     for x in (150, 362)])
D["patient-chart"] = lambda s: (P(s, checklist, 256, 256, 1.0), s.M("M150 380 L200 350 L240 380 L290 330 L340 360", RED, 8))
D["medical-file"] = lambda s: (s.F("path", d="M80 140 H210 L240 170 H432 V420 H80Z", fill=A1), s.F("rect", x=110, y=190, width=292, height=200, rx=8, fill=WHITE), cross(s, 256, 290, 50))
D["prescription"] = lambda s: (s.F("rect", x=110, y=60, width=292, height=392, rx=16, fill=WHITE), s.M("M150 140 V220 H180 C210 220 210 180 180 180 H150 M180 180 L220 230 M200 210 L180 240", A1, 10),
                               s.M("M150 290 H360 M150 330 H330 M150 370 H300", MID, 12))
D["doctors-bag"] = lambda s: (s.T("M190 180 V140 C190 110 322 110 322 140 V180", DARK, 22), s.F("path", d="M80 200 H432 L412 430 H100Z", fill="#6E3E22"), cross(s, 256, 310, 50, WHITE))
D["hospital-gown"] = lambda s: s.F("path", d="M180 70 L120 110 L80 200 L130 220 L160 170 V450 H352 V170 L382 220 L432 200 L392 110 L332 70 C320 100 192 100 180 70Z", fill="#9AD0E8")
D["wheelchair"] = lambda s: (s.raw(f'<circle cx="220" cy="340" r="110" fill="none" stroke="{DARK}" stroke-width="20"/>'), s.T("M180 140 V260 H330 L360 360 H410", DGREY, 18), s.F("rect", x=170, y=220, width=170, height=50, rx=10, fill=A1),
                             s.F("circle", cx=400, cy=420, r=24, fill=DARK))
D["crutches"] = lambda s: [s.T(f"M{x} 60 L{x - 20} 470 M{x - 30} 60 H{x + 30} M{x - 26} 250 H{x + 20}", DGREY, 14) for x in (200, 330)]
D["walking-stick"] = lambda s: s.T("M280 470 V150 C280 90 200 90 200 150", "#8C5A2A", 26)
D["walker-frame"] = lambda s: (s.T("M140 460 V130 H372 V460 M140 280 H372", GREY, 18), [s.F("circle", cx=x, cy=466, r=14, fill=DARK) for x in (140, 372)])
D["prosthetic-leg"] = lambda s: (s.F("path", d="M190 60 H322 L310 220 H202Z", fill=GREY), s.T("M256 220 V420", DGREY, 22), s.F("path", d="M210 420 H330 C360 420 370 450 340 460 H210Z", fill=DARK))
D["prosthetic-arm"] = lambda s: (s.F("path", d="M110 140 H240 V240 H110Z", fill=GREY), s.T("M240 190 H360", DGREY, 30), s.F("path", d="M360 150 H420 L440 170 V230 H360Z", fill=GREY),
                                 s.T("M430 170 L470 150 M430 200 L475 195 M430 225 L470 240", GREY, 10))
D["hearing-aid"] = lambda s: (s.F("path", d="M220 80 C300 60 360 120 340 200 C330 240 300 260 290 300 L230 290 C260 250 290 220 290 180 C290 140 250 120 220 130Z", fill=SKIN),
                              s.T("M260 300 C250 360 280 400 320 410", "#E8D8C8", 10), s.F("ellipse", cx=330, cy=420, rx=24, ry=16, fill="#E8D8C8"))
D["glasses"] = lambda s: (s.raw(f'<circle cx="160" cy="256" r="80" fill="#D9EEFB" stroke="{DARK}" stroke-width="18"/>'), s.raw(f'<circle cx="352" cy="256" r="80" fill="#D9EEFB" stroke="{DARK}" stroke-width="18"/>'),
                          s.M("M240 246 C250 230 262 230 272 246 M80 240 L40 220 M432 240 L472 220", DARK, 14))
D["contact-lens"] = lambda s: (s.T("M256 140 m-140 0 a140 140 0 0 0 280 0", "#9AD0E8", 20), s.F("path", d="M116 140 C116 260 396 260 396 140 C340 200 172 200 116 140Z", fill="#D9EEFB"), s.F("circle", cx=380, cy=360, r=60, fill=SKIN))
D["white-cane"] = lambda s: (s.T("M150 60 L330 460", WHITE, 22), s.T("M300 400 L330 460", RED, 22))
D["braille-watch"] = lambda s: (s.T("M256 60 V452", DARK, 60), s.F("circle", cx=256, cy=256, r=110, fill=GREY), s.F("circle", cx=256, cy=256, r=86, fill=WHITE),
                                [s.F("circle", outline=False, cx=f"{arc_pt(256, 256, 64, a)[0]:.0f}", cy=f"{arc_pt(256, 256, 64, a)[1]:.0f}", r=8, fill=DARK) for a in range(0, 360, 30)])

# ---------------------------------------------------------------- medicines
def pill(s, x=256, y=256, rot=-35, w=220, h=90, c1=A1, c2=LIGHT):
    s.open(transform=f"rotate({rot} {x} {y})")
    s.F("path", d=f"M{x} {y - h / 2} H{x - w / 2 + h / 2} A{h / 2} {h / 2} 0 0 0 {x - w / 2 + h / 2} {y + h / 2} H{x}Z", fill=c1)
    s.F("path", d=f"M{x} {y - h / 2} H{x + w / 2 - h / 2} A{h / 2} {h / 2} 0 0 1 {x + w / 2 - h / 2} {y + h / 2} H{x}Z", fill=c2)
    s.close()


def bottle(s, body=A2, cap=LIGHT, label=LIGHT):
    s.F("rect", x=150, y=150, width=212, height=300, rx=30, fill=body)
    s.F("rect", x=170, y=80, width=172, height=80, rx=14, fill=cap)
    s.F("rect", x=170, y=230, width=172, height=130, rx=10, fill=label)
    cross(s, 256, 296, 36, body)


D["medicine"] = lambda s: (bottle(s), pill(s, 380, 420, -35, 130, 56))
D["pill"] = lambda s: (s.F("circle", cx=256, cy=256, r=150, fill=LIGHT), s.M("M146 256 H366", MID, 14))
D["capsule"] = lambda s: pill(s)
D["pills-bottle"] = lambda s: bottle(s, A2)
D["syrup-bottle"] = lambda s: (s.F("path", d="M200 120 H312 V180 C380 200 380 260 380 300 V440 H132 V300 C132 260 132 200 200 180Z", fill=DRED), s.F("rect", x=190, y=70, width=132, height=60, rx=10, fill=LIGHT),
                               s.F("rect", x=160, y=290, width=192, height=110, rx=10, fill=LIGHT))
D["medicine-spoon"] = lambda s: (s.T("M100 400 L300 200", GREY, 20), s.F("ellipse", cx=340, cy=170, rx=90, ry=60, fill=GREY, transform="rotate(-45 340 170)"),
                                 s.F("ellipse", outline=False, cx=340, cy=170, rx=60, ry=36, fill=DRED, transform="rotate(-45 340 170)"))
D["eye-drops"] = lambda s: (s.F("path", d="M200 200 H312 V420 C312 450 200 450 200 420Z", fill=A1L), s.F("path", d="M220 200 L240 100 H272 L292 200Z", fill=LIGHT),
                            s.F("path", d="M256 30 C256 30 236 60 236 70 C236 86 276 86 276 70 C276 60 256 30 256 30Z", fill=SKY))
D["ointment-tube"] = lambda s: (s.F("path", d="M100 200 L340 160 V350 L100 310Z", fill=LIGHT), s.F("rect", x=340, y=200, width=60, height=110, rx=8, fill=A1), s.F("rect", x=400, y=220, width=40, height=70, rx=6, fill=A2),
                                s.M("M100 210 V300", MID, 10))
D["vaccine"] = lambda s: (D["syringe"](s), s.F("rect", x=60, y=320, width=100, height=140, rx=16, fill=A1L))
D["vaccine-vial"] = lambda s: (s.F("rect", x=180, y=160, width=152, height=280, rx=30, fill="#D9EEFB"), s.F("rect", outline=False, x=190, y=280, width=132, height=150, rx=24, fill=A1L),
                               s.F("rect", x=200, y=90, width=112, height=80, rx=10, fill=A2), s.F("rect", x=190, y=200, width=132, height=60, fill=LIGHT))
D["antibiotics"] = lambda s: (bottle(s, "#5EB8A8"), pill(s, 380, 420, -35, 130, 56, "#5EB8A8"))
D["painkiller"] = lambda s: (s.F("rect", x=80, y=150, width=352, height=220, rx=20, fill="#D9E2F0"), [s.F("circle", cx=140 + c * 80, cy=210 + r * 100, r=32, fill=LIGHT) for r in range(2) for c in range(4)])
D["herbal-medicine"] = lambda s: (s.F("path", d="M120 250 H392 C392 380 330 430 256 430 C182 430 120 380 120 250Z", fill="#8C6A3A"), s.F("ellipse", cx=256, cy=250, rx=136, ry=30, fill="#6E8A3A"),
                                  [s.F("ellipse", cx=x, cy=180, rx=30, ry=60, fill=GREEN, transform=f"rotate({(x - 256) // 3} {x} 220)") for x in (200, 256, 312)])
D["first-aid-ointment"] = lambda s: (D["ointment-tube"](s), cross(s, 220, 250, 34))

# ---------------------------------------------------------------- first aid (keep)
D["first-aid-kit"] = lambda s: (s.T("M200 150 V110 H312 V150", DGREY, 18), s.F("rect", x=80, y=150, width=352, height=270, rx=30, fill=RED), cross(s, 256, 285, 70, WHITE))
D["bandage"] = lambda s: (s.F("rect", x=140, y=100, width=232, height=312, rx=60, fill="#F4EBDD"), [s.M(f"M150 {y} H362", "#E0D2B8", 8) for y in range(150, 400, 40)])
D["plaster"] = lambda s: (s.F("rect", x=60, y=190, width=392, height=132, rx=66, fill="#E8B87A", transform="rotate(-30 256 256)"), s.F("rect", x=196, y=210, width=120, height=92, rx=12, fill="#F4E0C8", transform="rotate(-30 256 256)"))
D["gauze"] = lambda s: (s.F("rect", x=100, y=120, width=312, height=272, rx=12, fill=WHITE), [s.M(f"M100 {y} H412 M{x} 120 V392", "#E5E7EB", 4) for y, x in zip(range(150, 392, 30), range(130, 412, 30))])
D["sling"] = lambda s: (s.F("path", d="M170 80 L340 400 L120 420 Z", fill="#9AD0E8"), s.T("M170 80 C230 60 320 120 340 400", "#7FB8D8", 14), s.T("M140 340 L330 360", SKIN, 50))
D["splint"] = lambda s: (s.T("M140 120 L380 400", SKIN, 70), s.T("M160 90 L400 370 M110 150 L350 430", "#C9A27A", 20), [s.M(f"M{x} {y} l-60 70", WHITE, 14) for x, y in ((240, 180), (330, 290))])
D["ice-pack"] = lambda s: (s.F("rect", x=100, y=150, width=312, height=220, rx=40, fill="#9AD0E8"), [s.F("rect", outline=False, x=x, y=y, width=54, height=54, rx=10, fill=WHITE, transform=f"rotate(15 {x} {y})") for x, y in ((150, 200), (250, 230), (320, 190))])
D["cpr"] = lambda s: (P(s, person, 300, 280, 0.6, pose="carry"), s.F("rect", x=40, y=400, width=432, height=50, rx=10, fill=A1L), s.F("ellipse", cx=160, cy=400, rx=110, ry=30, fill=SKIN), cross(s, 420, 120, 30))
D["recovery-position"] = lambda s: (s.F("rect", x=40, y=420, width=432, height=40, rx=10, fill="#9BD7A8"), s.T("M120 390 H330", A1, 60), s.F("circle", cx=380, cy=380, r=40, fill=SKIN), s.T("M140 400 L120 430 M300 400 L340 430", DARK, 20))
D["burn-care"] = lambda s: (s.T("M80 300 L400 220", SKIN, 90), s.F("ellipse", cx=260, cy=260, rx=60, ry=30, fill="#F07A7E", transform="rotate(-14 260 260)"), s.M("M200 120 C220 80 260 80 280 120", SKY, 10), [s.F("path", d=f"M{x} 140 C{x} 140 {x - 12} 160 {x - 12} 168 C{x - 12} 180 {x + 12} 180 {x + 12} 168 C{x + 12} 160 {x} 140 {x} 140Z", fill=SKY) for x in (220, 260)])
D["cold-compress"] = lambda s: (s.F("ellipse", cx=256, cy=300, rx=150, ry=170, fill=SKIN), s.F("rect", x=150, y=120, width=212, height=90, rx=30, fill="#9AD0E8"))

# ---------------------------------------------------------------- illness and symptoms (patient busts)
def bust(s, mood="sick", shirt=A1, cheeks=None, sweat=False, eyes_closed=False):
    s.F("path", d="M90 470 C100 380 160 340 256 340 C352 340 412 380 422 470Z", fill=shirt)
    s.F("rect", x=226, y=300, width=60, height=50, fill=SKIN)
    s.F("ellipse", cx=256, cy=220, rx=110, ry=120, fill=SKIN)
    s.F("path", d="M146 200 C140 100 372 100 366 200 C340 150 300 140 256 140 C212 140 172 150 146 200Z", fill=HAIR)
    if eyes_closed:
        s.M("M196 220 Q216 232 236 220 M276 220 Q296 232 316 220", INK, 7)
    elif mood == "sick":
        s.M("M196 212 L236 222 M276 222 L316 212", INK, 6)
        eye(s, 216, 236, 9, "left")
        eye(s, 296, 236, 9, "right")
    else:
        eye(s, 216, 226, 10, "left")
        eye(s, 296, 226, 10, "right")
    if mood in ("sick", "sad"):
        s.M("M226 296 Q256 278 286 296", INK, 7)
    elif mood == "pain":
        s.M("M222 290 L238 282 L254 292 L270 282 L290 290", INK, 6)
    else:
        s.M("M226 286 Q256 306 286 286", INK, 7)
    if cheeks:
        for x in (186, 326):
            s.F("ellipse", outline=False, cx=x, cy=268, rx=22, ry=14, fill=cheeks)
    if sweat:
        s.F("path", d="M360 150 C360 150 346 172 346 182 C346 196 374 196 374 182 C374 172 360 150 360 150Z", fill=SKY)


def thermo_in_mouth(s):
    s.T("M286 296 L380 250", WHITE, 14)
    s.F("circle", cx=286, cy=296, r=10, fill=RED)


D["illness"] = lambda s: (bust(s, "sick", cheeks="#F07A7E"), s.F("rect", x=170, y=110, width=172, height=50, rx=20, fill="#9AD0E8"))
D["fever"] = lambda s: (bust(s, "sick", cheeks="#F07A7E", sweat=True), thermo_in_mouth(s))
D["cold-and-flu"] = lambda s: (bust(s, "sick", shirt="#8C96A3", cheeks="#F07A7E"), s.F("path", d="M330 260 C380 240 420 280 400 320 C380 350 330 340 320 310Z", fill=WHITE), s.F("rect", x=80, y=40, width=100, height=40, rx=20, fill="#9AD0E8"))
D["cough"] = lambda s: (bust(s, "pain"), s.M("M320 280 L380 260 M320 296 L390 300 M320 312 L376 336", MID, 8))
D["sneeze-into-elbow"] = lambda s: (bust(s, eyes_closed=True), s.T("M120 420 C160 360 220 300 300 300", A1, 60))
D["headache"] = lambda s: (bust(s, "pain"), s.M("M140 100 L170 130 M372 100 L342 130 M256 60 V96", RED, 10), s.F("polygon", points="360,60 330,110 360,110 340,160", fill=YEL))
D["stomach-ache"] = lambda s: (bust(s, "pain"), s.T("M160 420 C200 390 230 400 256 410", SKIN, 40), s.M("M300 400 L320 380 L340 410 L360 390", RED, 8))
D["toothache"] = lambda s: (bust(s, "pain"), s.F("ellipse", cx=320, cy=270, rx=40, ry=30, fill="#F07A7E"), s.T("M110 380 C150 300 220 260 300 270", A1, 40), s.M("M370 230 L400 210 M374 270 L410 270", RED, 8))
D["sore-throat"] = lambda s: (bust(s, "sick"), s.F("rect", x=210, y=320, width=92, height=40, rx=16, fill="#F07A7E"))
D["runny-nose"] = lambda s: (bust(s, "sick", cheeks="#F07A7E"), s.F("path", d="M262 270 C262 270 252 292 252 300 C252 312 272 312 272 300 C272 292 262 270 262 270Z", fill=SKY))
D["allergy"] = lambda s: (bust(s, "sick"), [s.F("circle", outline=False, cx=x, cy=y, r=9, fill="#F07A7E") for x, y in ((180, 260), (200, 290), (320, 260), (300, 300), (256, 180))],
                          [s.F("circle", cx=x, cy=y, r=12, fill=YEL) for x, y in ((80, 100), (430, 120), (420, 300))])
D["rash"] = lambda s: (s.F("rect", x=80, y=120, width=352, height=272, rx=40, fill=SKIN), [s.F("circle", outline=False, cx=x, cy=y, r=r, fill="#F07A7E") for x, y, r in
                                                                                       ((160, 200, 18), (220, 240, 14), (300, 190, 20), (340, 280, 16), (200, 320, 18), (270, 300, 12))])
D["broken-arm"] = lambda s: (bust(s, "sad"), s.F("path", d="M170 470 L150 340 C200 330 330 330 380 350 L340 470Z", fill="#9AD0E8"), s.T("M170 400 H330", WHITE, 46), s.M("M200 390 L210 410 M260 388 L270 412", MID, 5))
D["broken-leg"] = lambda s: (s.T("M200 60 V250", "#5A6A8A", 60), s.F("rect", x=160, y=240, width=90, height=200, rx=30, fill=WHITE), s.F("path", d="M150 430 H280 C300 430 310 460 290 470 H150Z", fill=WHITE),
                             s.T("M330 470 V120 M290 160 H370", DGREY, 14))
D["sprain"] = lambda s: (s.F("path", d="M150 80 H260 V300 C300 330 420 330 430 380 C440 430 360 440 300 430 H180 C150 430 150 380 150 340Z", fill=SKIN), s.F("ellipse", cx=220, cy=330, rx=60, ry=40, fill="#F07A7E", fill_opacity="0.8"),
                         s.M("M300 200 L330 170 M310 240 L350 240", RED, 8))
D["burn-injury"] = lambda s: D["burn-care"](s)
D["cut-wound"] = lambda s: (s.T("M60 300 L450 220", SKIN, 120), s.M("M200 260 L320 236", DRED, 10), s.F("path", d="M260 260 C260 260 250 280 250 288 C250 300 270 300 270 288 C270 280 260 260 260 260Z", fill=RED))
D["nosebleed"] = lambda s: (bust(s, "sad"), s.F("path", d="M250 280 C250 280 240 300 240 308 C240 320 260 320 260 308 C260 300 250 280 250 280Z", fill=RED))
D["diabetes"] = lambda s: (D["glucose-meter"](s), s.F("path", d="M380 120 C380 120 360 150 360 162 C360 180 400 180 400 162 C400 150 380 120 380 120Z", fill=RED))
D["asthma"] = lambda s: (bust(s, "sad"), s.F("path", d="M330 300 H400 V380 H330Z", fill=A2), s.M("M310 290 C290 280 290 260 310 250", MID, 6))
D["high-blood-pressure"] = lambda s: (D["blood-pressure-monitor"](s), s.M("M140 150 L170 130 L200 170 L230 120 L260 170", RED, 8))
D["heart-attack"] = lambda s: (P(s, heart, 256, 240, 0.8, color=RED), s.M("M180 240 H230 L250 200 L270 290 L290 240 H340", WHITE, 10))
D["stroke"] = lambda s: (s.F("path", d="M110 300 C80 230 120 140 200 120 C240 80 330 90 370 130 C430 150 450 230 420 290 C410 340 360 360 320 350 C300 380 240 390 200 360 C150 370 110 340 110 300Z", fill="#F7B5C0"),
                         s.F("circle", outline=False, cx=300, cy=210, r=40, fill=RED, fill_opacity="0.8"), s.M("M300 160 L320 130 M340 200 L380 190", RED, 8))
D["cancer-ribbon"] = lambda s: (s.T("M256 300 C200 220 180 120 256 100 C332 120 312 220 256 300 L170 440 M256 300 L342 440", "#F48AA6", 40))
D["malaria"] = lambda s: (P(s, lambda s: (s.T("M256 300 V180", DGREY, 6), s.F("ellipse", cx=256, cy=320, rx=26, ry=80, fill="#5A5A66"), [s.F("ellipse", cx=256 + sg * 70, cy=260, rx=70, ry=24, fill="#D9EEFB", fill_opacity="0.8") for sg in (1, -1)],
                                             [s.T(f"M256 300 L{256 + sg * 90} {340 + k * 30}", "#5A5A66", 5) for sg in (1, -1) for k in range(3)]), 256, 230, 1.0), s.F("rect", x=150, y=420, width=212, height=40, rx=16, fill="#F07A7E"))
D["dengue"] = lambda s: (D["malaria"](s), [s.F("circle", outline=False, cx=x, cy=y, r=8, fill=WHITE) for x, y in ((240, 320), (272, 360), (240, 380))])
D["chickenpox"] = lambda s: (bust(s, "sad"), [s.F("circle", cx=x, cy=y, r=10, fill="#F07A7E") for x, y in ((180, 180), (220, 290), (300, 170), (320, 280), (256, 250), (190, 400), (330, 410))])
D["measles"] = lambda s: (bust(s, "sick"), [s.F("circle", outline=False, cx=x, cy=y, r=7, fill=RED) for x in range(170, 360, 26) for y in (190, 300) if (x + y) % 3])
D["food-poisoning"] = lambda s: (bust(s, "pain", cheeks="#9BD7A8"), s.F("circle", cx=400, cy=120, r=50, fill=LIGHT), s.F("ellipse", cx=400, cy=120, rx=30, ry=16, fill="#C1662E"), s.M("M360 80 L440 160 M440 80 L360 160", RED, 8))
D["dehydration"] = lambda s: (bust(s, "sick", sweat=True), s.F("rect", x=380, y=200, width=70, height=180, rx=20, fill="#D9EEFB"), s.F("rect", outline=False, x=386, y=340, width=58, height=34, rx=10, fill=SKY))
D["obesity"] = lambda s: (s.F("ellipse", cx=256, cy=330, rx=170, ry=150, fill=A2), s.F("circle", cx=256, cy=150, r=80, fill=SKIN), eye(s, 230, 140, 8, "left"), eye(s, 282, 140, 8, "right"), s.M("M236 180 Q256 192 276 180", INK, 6))
D["insomnia"] = lambda s: (bust(s, "sad", shirt="#5A6A8A"), s.F("ellipse", outline=False, cx=216, cy=258, rx=26, ry=10, fill="#B8A0C8"), s.F("ellipse", outline=False, cx=296, cy=258, rx=26, ry=10, fill="#B8A0C8"),
                           s.F("path", d="M420 60 C380 70 360 110 370 150 C380 190 420 200 450 190 C420 180 400 160 400 130 C400 100 410 80 420 60Z", fill=YEL))

# ---------------------------------------------------------------- germs (keep)
def germ(s, x=256, y=256, r=120, color="#6EC84A", spikes=12, face=True):
    for k in range(spikes):
        a = k * 360 / spikes
        x1, y1 = arc_pt(x, y, r, a); x2, y2 = arc_pt(x, y, r * 1.35, a)
        s.T(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", color, r * 0.12)
        s.F("circle", cx=f"{x2:.0f}", cy=f"{y2:.0f}", r=f"{r * 0.12:.0f}", fill=shade(color, 0.8))
    s.F("circle", cx=x, cy=y, r=r, fill=color)
    if face:
        eye(s, x - r * 0.3, y - r * 0.1, r * 0.12, "left")
        eye(s, x + r * 0.3, y - r * 0.1, r * 0.12, "right")
        s.M(f"M{x - r * 0.3:.0f} {y + r * 0.35:.0f} Q{x:.0f} {y + r * 0.15:.0f} {x + r * 0.3:.0f} {y + r * 0.35:.0f}", INK, r * 0.06)


D["germs"] = lambda s: (germ(s, 200, 220, 90), germ(s, 350, 320, 70, "#B880E8"), germ(s, 150, 380, 40, "#F5913E"))
D["germ-character"] = lambda s: germ(s)
D["flu-virus"] = lambda s: germ(s, color="#5EA8E8", face=False)
D["coronavirus"] = lambda s: germ(s, color="#E8607A", spikes=16, face=False)
D["pandemic"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=C["blue"]), [germ(s, x, y, 30, "#E8607A", 10, False) for x, y in ((180, 180), (320, 200), (250, 300), (350, 340), (160, 340))])
D["epidemic"] = lambda s: (s.F("rect", x=60, y=80, width=392, height=352, rx=20, fill="#9BD7A8"), [germ(s, x, y, 26, "#E8607A", 10, False) for x, y in ((150, 160), (250, 240), (340, 180), (300, 340))])
D["infection"] = lambda s: (s.F("rect", x=60, y=150, width=392, height=212, rx=40, fill=SKIN), s.F("ellipse", cx=256, cy=256, rx=90, ry=50, fill="#F07A7E"), germ(s, 256, 256, 30, "#6EC84A", 10, False))
D["quarantine"] = lambda s: (s.F("rect", x=100, y=140, width=312, height=300, fill="#D9E2F0"), s.F("polygon", points="80,150 256,60 432,150", fill=A2), P(s, person, 256, 330, 0.4, pose="sit"))
D["spread-of-germs"] = lambda s: (P(s, person, 150, 280, 0.6, pose="stand"), [germ(s, x, y, r, "#6EC84A", 8, False) for x, y, r in ((270, 200, 20), (330, 170, 16), (380, 230, 22), (430, 180, 14))])
D["immune-response"] = lambda s: (germ(s, 340, 300, 60, "#6EC84A", 10, True), [s.T(f"M{x} {y} L{x + 40} {y + 40}", A1, 14) for x, y in ((140, 160), (200, 120), (120, 260))], [s.M(f"M{x + 40} {y + 40} l20 -10 M{x + 40} {y + 40} l-10 20", A1, 10) for x, y in ((140, 160), (200, 120), (120, 260))])

# ---------------------------------------------------------------- dental (keep)
D["toothbrush"] = lambda s: (s.T("M80 430 L360 150", A1, 34), s.F("rect", x=330, y=80, width=120, height=50, rx=10, fill=A1, transform="rotate(-45 390 105)"),
                             [s.T(f"M{x} {y} l-30 -30", WHITE, 12) for x, y in ((380, 120), (400, 100), (420, 80))])
D["toothpaste"] = lambda s: (s.F("path", d="M80 300 L330 230 V350 L80 330Z", fill=WHITE), s.F("rect", x=330, y=250, width=60, height=80, rx=8, fill=A1), s.M("M100 300 L320 250", RED, 12),
                             s.F("path", d="M390 260 C430 250 450 270 440 290 C430 310 400 300 390 300Z", fill="#9AD0E8"))
D["dental-floss"] = lambda s: (s.F("rect", x=140, y=200, width=232, height=200, rx=40, fill="#9AD0E8"), s.T("M256 200 C260 120 340 80 440 60", WHITE, 6))
D["mouthwash"] = lambda s: (s.F("path", d="M190 140 H322 V440 H190Z", fill="#5EC8C0"), s.F("rect", x=200, y=80, width=112, height=70, rx=10, fill=LIGHT), s.F("rect", x=200, y=240, width=112, height=110, rx=10, fill=LIGHT))
D["dentist-chair"] = lambda s: (s.F("path", d="M100 330 H330 L380 160 H420 L380 360 H100Z", fill=A1), s.T("M220 360 V430 M140 430 H300", DGREY, 16), s.T("M380 160 L380 100", DGREY, 10), s.F("ellipse", cx=380, cy=90, rx=40, ry=20, fill="#FFF3B0"))
D["braces"] = lambda s: (s.F("path", d="M60 220 C140 120 372 120 452 220 V300 H60Z", fill="#F48AA6"), [s.F("rect", x=96 + k * 42, y=200, width=38, height=80, rx=12, fill=WHITE) for k in range(8)],
                         s.M("M90 240 H422", GREY, 6), [s.F("rect", x=106 + k * 42, y=230, width=18, height=20, rx=3, fill=GREY) for k in range(8)])
D["tooth-decay"] = lambda s: (s.F("path", d="M150 120 C150 70 230 60 256 90 C282 60 362 70 362 120 C362 200 340 230 330 300 C320 380 300 440 280 440 C260 440 266 340 256 340 C246 340 252 440 232 440 C212 440 192 380 182 300 C172 230 150 200 150 120Z", fill="#F4EBDD"),
                              s.F("circle", outline=False, cx=300, cy=150, r=34, fill="#5E4A3E"), s.F("circle", outline=False, cx=220, cy=200, r=20, fill="#8C6A4A"))
D["clean-tooth"] = lambda s: (s.F("path", d="M150 120 C150 70 230 60 256 90 C282 60 362 70 362 120 C362 200 340 230 330 300 C320 380 300 440 280 440 C260 440 266 340 256 340 C246 340 252 440 232 440 C212 440 192 380 182 300 C172 230 150 200 150 120Z", fill=WHITE),
                              [s.F("polygon", outline=False, points=star_pts(x, y, r, r * 0.3, 4), fill="#8FD0FF") for x, y, r in ((400, 120, 40), (110, 160, 26), (420, 300, 20))])
D["tooth-filling"] = lambda s: (D["clean-tooth"](s), s.F("ellipse", cx=270, cy=150, rx=50, ry=30, fill=GREY))
D["false-teeth"] = lambda s: (s.F("path", d="M80 200 C160 120 352 120 432 200 V260 C352 230 160 230 80 260Z", fill="#F48AA6"), [s.F("rect", x=110 + k * 40, y=220, width=36, height=60, rx=12, fill=WHITE) for k in range(8)],
                              s.F("path", d="M80 300 C160 330 352 330 432 300 V360 C352 410 160 410 80 360Z", fill="#F48AA6"), [s.F("rect", x=116 + k * 38, y=290, width=34, height=50, rx=12, fill=WHITE) for k in range(8)])

# ---------------------------------------------------------------- hygiene (keep)
def drops(s, pts, color=SKY):
    for x, y in pts:
        s.F("path", d=f"M{x} {y} C{x} {y} {x - 12} {y + 18} {x - 12} {y + 26} C{x - 12} {y + 38} {x + 12} {y + 38} {x + 12} {y + 26} C{x + 12} {y + 18} {x} {y} {x} {y}Z", fill=color)


def hands(s):
    for x, f in ((200, 1), (312, -1)):
        s.open(transform=f"translate({x} 330) scale({f} 1)")
        s.F("path", d="M-60 140 C-80 80 -80 20 -70 -20 C-64 -40 -40 -40 -40 -20 V-110 C-40 -130 -10 -130 -10 -110 V-130 C-10 -150 20 -150 20 -130 V-120 C20 -140 50 -140 50 -120 V0 C50 60 30 110 20 140Z", fill=SKIN)
        s.close()


D["handwashing"] = lambda s: (hands(s), [s.F("circle", cx=x, cy=y, r=r, fill=WHITE) for x, y, r in ((240, 240, 26), (280, 270, 20), (260, 320, 16), (300, 220, 14))], drops(s, ((256, 80), (230, 130), (290, 120))))
D["soap"] = lambda s: (s.F("rect", x=110, y=200, width=292, height=170, rx=60, fill=PINK), s.F("rect", outline=False, x=150, y=220, width=200, height=40, rx=20, fill="#FCD0DC"),
                       [s.F("circle", cx=x, cy=y, r=r, fill=WHITE) for x, y, r in ((160, 160, 26), (220, 130, 18), (300, 150, 30))])
D["hand-sanitiser"] = lambda s: (s.F("rect", x=170, y=200, width=172, height=260, rx=30, fill="#D9EEFB"), s.F("rect", outline=False, x=180, y=300, width=152, height=150, rx=24, fill="#8FD0FF"),
                                 s.F("rect", x=220, y=140, width=72, height=70, fill=WHITE), s.T("M256 140 V100 H320", WHITE, 20))
D["liquid-soap"] = lambda s: (s.F("rect", x=170, y=200, width=172, height=260, rx=30, fill=PINK), s.F("rect", x=220, y=140, width=72, height=70, fill=WHITE), s.T("M256 140 V100 H320", WHITE, 20))
D["bath"] = lambda s: (s.F("path", d="M60 250 H452 V320 C452 400 400 430 340 430 H172 C112 430 60 400 60 320Z", fill=WHITE), [s.F("circle", cx=x, cy=240, r=r, fill="#D9EEFB") for x, r in ((140, 40), (220, 50), (300, 46), (380, 36))],
                       s.T("M100 430 L80 470 M412 430 L432 470", DGREY, 14), s.T("M420 250 V120 C420 80 380 80 370 110", GREY, 12))
D["shower"] = lambda s: (s.T("M380 470 V100 C380 60 320 60 300 90", GREY, 16), s.F("path", d="M250 90 H350 L330 130 H270Z", fill=GREY), drops(s, ((270, 170), (300, 200), (330, 170), (280, 260), (320, 260), (300, 330))))
D["towel"] = lambda s: (s.T("M100 120 H412", GREY, 14), s.F("rect", x=140, y=120, width=232, height=300, rx=12, fill=A1L), s.M("M140 380 H372", A1, 14))
D["tissue-box"] = lambda s: (s.F("rect", x=100, y=220, width=312, height=200, rx=20, fill=A1L), s.F("ellipse", cx=256, cy=230, rx=80, ry=14, fill=A1), s.F("path", d="M210 230 C200 160 240 120 256 100 C280 140 320 160 300 230Z", fill=WHITE))
D["nail-clipper"] = lambda s: (s.F("path", d="M80 300 L400 220 L420 260 L100 340Z", fill=GREY), s.F("path", d="M80 300 L400 280 L410 320 L100 340Z", fill="#B7BEC8"), s.F("circle", cx=380, cy=270, r=12, fill=DGREY))
D["comb"] = lambda s: (s.F("rect", x=80, y=180, width=352, height=60, rx=14, fill=A2), [s.M(f"M{x} 240 V330", A2, 10) for x in range(100, 420, 18)])
D["deodorant"] = lambda s: (s.F("rect", x=190, y=150, width=132, height=300, rx=40, fill=A1), s.F("rect", x=200, y=90, width=112, height=70, rx=16, fill=WHITE))
D["cotton-buds"] = lambda s: [(s.T(f"M{x} 420 L{x + 60} 100", WHITE, 12), s.F("ellipse", cx=x, cy=430, rx=18, ry=26, fill=WHITE), s.F("ellipse", cx=x + 60, cy=92, rx=18, ry=26, fill=WHITE)) for x in (160, 256)]

# ---------------------------------------------------------------- healthy habits (scenes)
GR = "#9BD7A8"


def ground(s, color=GR):
    s.F("rect", outline=False, x=24, y=410, width=464, height=60, rx=20, fill=color)


def plate(s, x=256, y=300, r=150):
    s.F("circle", cx=x, cy=y, r=r, fill=WHITE)
    for a0, col in ((0, "#4CB963"), (90, C["orange"]), (180, "#E8C27A"), (270, C["red"])):
        x1, y1 = arc_pt(x, y, r * 0.85, a0); x2, y2 = arc_pt(x, y, r * 0.85, a0 + 90)
        s.F("path", d=f"M{x} {y} L{x1:.0f} {y1:.0f} A{r * 0.85:.0f} {r * 0.85:.0f} 0 0 1 {x2:.0f} {y2:.0f}Z", fill=col)


D["healthy-lifestyle"] = lambda s: (ground(s), P(s, person, 200, 270, 0.75, pose="walk", shirt=A2), P(s, heart, 400, 120, 0.25, color=RED), P(s, plate, 400, 330, 0.35))
D["balanced-diet"] = lambda s: plate(s)
D["drink-water"] = lambda s: (s.F("path", d="M150 120 H362 L330 440 H182Z", fill="#D9EEFB"), s.F("path", outline=False, d="M160 220 H352 L330 430 H182Z", fill=SKY), drops(s, ((256, 40),)))
D["regular-exercise"] = lambda s: (ground(s), P(s, person, 256, 270, 0.85, pose="cheer", shirt=A1), s.T("M130 160 H380", DGREY, 14), [s.F("rect", x=x, y=130, width=30, height=60, rx=6, fill=A2) for x in (110, 372)])
D["good-sleep"] = lambda s: (s.F("rect", x=60, y=280, width=392, height=100, rx=20, fill=A1L), s.F("rect", x=80, y=250, width=120, height=50, rx=20, fill=WHITE), s.F("circle", cx=200, cy=240, r=40, fill=SKIN),
                             s.M("M190 236 Q200 244 210 236", INK, 5), s.F("path", d="M380 60 C340 70 320 110 330 150 C340 190 380 200 410 190 C380 180 360 160 360 130 C360 100 370 80 380 60Z", fill=YEL),
                             s.M("M270 150 H300 L270 180 H300", A1, 8))
D["morning-walk"] = lambda s: (s.F("rect", x=24, y=24, width=464, height=446, rx=30, fill="#FFE8C0"), s.F("circle", cx=400, cy=130, r=60, fill=YEL), ground(s), P(s, person, 200, 270, 0.75, pose="walk"))
D["yoga"] = lambda s: (s.F("rect", x=60, y=420, width=392, height=30, rx=10, fill=A2), P(s, person, 256, 260, 0.8, pose="cheer", shirt=A1))
D["meditation"] = lambda s: (s.F("circle", outline=False, cx=256, cy=260, r=200, fill=A1L, fill_opacity="0.5"), P(s, person, 256, 300, 0.75, pose="sit", shirt=A1))
D["stretching"] = lambda s: (ground(s), P(s, person, 256, 260, 0.8, pose="cheer", shirt=A2))
D["sunlight-vitamin-d"] = lambda s: (s.F("circle", cx=380, cy=130, r=70, fill=YEL), ground(s), P(s, person, 200, 280, 0.7, pose="cheer"), s.M("M320 170 L270 220 M340 210 L300 260", YEL, 8))
D["no-junk-food"] = lambda s: (s.F("circle", cx=256, cy=256, r=200, fill=WHITE), s.F("path", d="M160 220 C160 160 352 160 352 220Z", fill="#E8B87A"), s.F("rect", x=156, y=230, width=200, height=30, fill="#6E3E22"), s.F("path", d="M160 270 H352 C352 300 160 300 160 270Z", fill="#E8B87A"),
                               s.raw(f'<circle cx="256" cy="256" r="200" fill="none" stroke="{RED}" stroke-width="30"/>'), s.M("M115 115 L397 397", RED, 30))
D["screen-time-limit"] = lambda s: (s.F("rect", x=150, y=80, width=212, height=352, rx=30, fill=DARK), s.F("rect", outline=False, x=170, y=110, width=172, height=290, rx=10, fill=A1L), P(s, lambda s: (s.F("circle", cx=256, cy=256, r=190, fill=WHITE), s.M("M256 256 V140 M256 256 L340 300", DARK, 24)), 256, 256, 0.5))

# ---------------------------------------------------------------- mental health
def head_side(s, inner=None, color=A1L):
    s.F("path", d="M150 460 V380 C110 360 90 300 100 240 C110 140 190 70 290 80 C380 90 430 160 420 240 C416 280 440 300 430 320 L410 330 C410 360 400 380 370 380 H330 V460Z", fill=color)
    if inner:
        inner(s)


D["mental-health"] = lambda s: head_side(s, lambda s: P(s, heart, 270, 220, 0.35, color=C["pink"]))
D["stress"] = lambda s: head_side(s, lambda s: s.M("M180 220 C200 180 240 260 270 200 C300 150 330 230 360 190", DARK, 10), "#F9B57A")
D["anxiety"] = lambda s: head_side(s, lambda s: [s.T(f"M{x} {y} q20 -30 40 0", DARK, 8) for x, y in ((190, 200), (250, 170), (300, 220), (220, 260))], "#C9CED6")
D["depression"] = lambda s: head_side(s, lambda s: (s.F("path", d="M190 210 C190 170 330 170 330 210Z", fill="#8C96A3"), drops(s, ((220, 240), (280, 250), (250, 290)), "#8FB8F8")), "#B7BEC8")
D["burnout"] = lambda s: (P(s, lambda s: (s.F("rect", x=70, y=160, width=340, height=192, rx=30, fill=WHITE), s.F("rect", x=410, y=220, width=34, height=72, rx=8, fill=GREY), s.F("rect", outline=False, x=96, y=186, width=50, height=140, rx=10, fill=RED)), 256, 256, 1.0))
D["self-care"] = lambda s: (P(s, heart, 256, 280, 0.8, color=C["pink"]), P(s, lambda s: s.F("path", d="M256 140 C200 140 160 180 160 230 C200 210 230 210 256 230 C282 210 312 210 352 230 C352 180 312 140 256 140Z", fill="#4CB963"), 256, 140, 0.5))
D["talk-therapy-session"] = lambda s: (P(s, person, 150, 300, 0.6, pose="sit"), P(s, person, 362, 300, 0.6, pose="sit", shirt=A2), s.F("path", d="M200 80 H330 C350 80 360 90 360 110 V150 C360 170 350 180 330 180 H260 L230 210 V180 H200 C180 180 170 170 170 150 V110 C170 90 180 80 200 80Z", fill=A1L))
D["support-helpline"] = lambda s: (s.F("path", d="M150 140 C150 120 180 110 200 120 L230 200 L200 230 C220 280 250 310 290 330 L320 300 L400 330 C410 350 400 380 380 380 C240 380 150 290 150 140Z", fill=A1), P(s, heart, 380, 140, 0.25, color=C["pink"]))
D["mindfulness"] = lambda s: (s.F("circle", outline=False, cx=256, cy=256, r=200, fill="#C8E8D8"), P(s, person, 256, 300, 0.75, pose="sit", shirt="#5EB8A8"), [s.F("circle", outline=False, cx=x, cy=y, r=8, fill=WHITE) for x, y in ((120, 140), (390, 160), (100, 300))])
D["calm-breathing"] = lambda s: (head_side(s, None, A1L), s.M("M440 280 C480 260 500 230 500 200 M440 300 C490 300 510 280 512 260", SKY, 10))
D["journaling"] = lambda s: (s.F("rect", x=110, y=80, width=292, height=360, rx=20, fill=A2), s.F("rect", x=140, y=100, width=242, height=320, rx=10, fill=WHITE), s.M("M170 170 H350 M170 220 H330 M170 270 H350 M170 320 H300", MID, 10),
                             s.T("M300 420 L420 300", DARK, 14))

# ---------------------------------------------------------------- health checks
D["health-checkup"] = lambda s: (P(s, person, 160, 290, 0.65, shirt=WHITE), P(s, person, 360, 300, 0.55, shirt=A2), s.T("M140 180 C130 230 150 260 180 260", DGREY, 8))
D["eye-test-chart"] = lambda s: (s.F("rect", x=120, y=50, width=272, height=412, rx=16, fill=WHITE), stroke_text(s, "E", 256, 120, 90, DARK, 16), stroke_text(s, "ED", 256, 220, 60, DARK, 11),
                                 stroke_text(s, "ABC", 256, 300, 44, DARK, 8), stroke_text(s, "DEAB", 256, 370, 30, DARK, 6), stroke_text(s, "BCDEA", 256, 420, 22, DARK, 4))
D["weighing-machine"] = lambda s: (s.F("rect", x=100, y=150, width=312, height=280, rx=60, fill=LIGHT), s.F("rect", outline=False, x=180, y=190, width=152, height=70, rx=10, fill="#B8E0D0"),
                                   s.F("ellipse", outline=False, cx=190, cy=350, rx=40, ry=60, fill=MID), s.F("ellipse", outline=False, cx=322, cy=350, rx=40, ry=60, fill=MID))
D["height-measuring"] = lambda s: (s.F("rect", x=330, y=40, width=80, height=430, fill="#F2D06E"), [s.M(f"M330 {y} h{20 if y % 80 else 40}", "#8C6A20", 6) for y in range(60, 470, 40)],
                                   P(s, person, 220, 270, 0.8, shirt=A1), s.T("M260 70 H330", DARK, 10))
D["blood-donation"] = lambda s: (s.T("M130 380 L360 250", SKIN, 70), s.T("M300 270 C330 200 360 160 400 140", RED, 8), s.F("rect", x=380, y=60, width=90, height=130, rx=16, fill=RED), P(s, heart, 425, 110, 0.12, color=WHITE))
D["organ-donation-card"] = lambda s: (s.F("rect", x=60, y=130, width=392, height=252, rx=24, fill=WHITE), P(s, heart, 160, 250, 0.3, color=RED), s.M("M240 210 H400 M240 250 H380 M240 290 H360", MID, 12))
D["health-insurance-card"] = lambda s: (s.F("rect", x=60, y=130, width=392, height=252, rx=24, fill=A1), P(s, shield, 150, 256, 0.3), s.M("M240 210 H400 M240 250 H380 M240 290 H360", A1L, 12))
D["bmi-chart"] = lambda s: (s.F("rect", x=60, y=100, width=392, height=312, rx=20, fill=WHITE), [s.F("rect", outline=False, x=80 + k * 88, y=320 - k * 50, width=70, height=60 + k * 50, rx=6, fill=c) for k, c in enumerate(("#8FD0FF", "#4CB963", C["yellow"], C["red"]))])


if __name__ == "__main__":
    run("health-medicine", D, sys.argv[1:] or None)
