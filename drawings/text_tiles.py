"""Text tiles for symbols-signs, concepts-ideas, brain-teasers-logic, celebrations-holidays and
religion-faith: lettering drawn as paths with tools/text_tile.py (no font needed in the SVG).

Arabic is written without short-vowel marks (tashkeel). It was typed by hand: have someone who
reads Arabic check the surah names, the 99 Names and the phrases before publishing.
Run: python drawings/text_tiles.py [ids...]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from _parts import A1, A1D, A1L, A2, A2L, DARK, LIGHT, MID, bulb, check_badge, hourglass, key, magnifier, place, qmark, star, stairs  # noqa: E402
from draw_lib import C, INK, arc_pt, run, star_pts  # noqa: E402
from check_catalog import slug  # noqa: E402
from text_tile import text_path  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GOLD, GREEN_D, GREEN = "#D9A520", "#0E5E3A", "#1F8A55"


def txt(s, text, font="black", cx=256, cy=256, w=400, h=100, color=LIGHT):
    d, _ = text_path(text, font, cx, cy, w, h)
    if d:
        s.F("path", outline=False, d=d, fill=color)


def lines(s, rows, cy=256, w=380, h=86, gap=18, color=LIGHT, font="black"):
    total = len(rows) * h + (len(rows) - 1) * gap
    y = cy - total / 2 + h / 2
    for r in rows:
        txt(s, r, font, 256, y, w, h, color)
        y += h + gap


def card(s, color=A1, y0=70, y1=442):
    s.F("rect", x=40, y=y0, width=432, height=y1 - y0, rx=44, fill=color)


# ---------------------------------------------------------------- symbols-signs: label tiles
SYM = {}


def burst(text, color):
    def fn(s):
        s.F("polygon", points=star_pts(256, 256, 220, 180, 22), fill=color)
        txt(s, text, cx=256, cy=256, w=290, h=110)
    return fn


def pill(text, color, dot=False, flame=False):
    def fn(s):
        s.F("rect", x=40, y=166, width=432, height=180, rx=90, fill=color)
        x0 = 256
        if dot:
            s.F("circle", cx=104, cy=256, r=28, fill=LIGHT)
            x0 = 300
        if flame:
            s.F("path", d="M118 316 C76 300 74 250 104 216 C104 246 120 252 126 236 C132 210 120 196 136 176 C170 210 180 300 118 316 Z", fill=A2L)
            x0 = 300
        txt(s, text, cx=x0, cy=256, w=250 if (dot or flame) else 360, h=100)
    return fn


def tag(text, color):
    def fn(s):
        s.F("path", d="M150 136 H446 C460 136 472 148 472 162 V350 C472 364 460 376 446 376 H150 L40 256 Z", fill=color)
        s.F("circle", cx=128, cy=256, r=20, fill=LIGHT)
        txt(s, text, cx=300, cy=256, w=260, h=110)
    return fn


def ribbon(text, color):
    def fn(s):
        for x0, sgn in ((60, 1), (452, -1)):
            s.F("polygon", points=f"{x0},{206} {x0 + sgn * 90},{206} {x0 + sgn * 90},{330} {x0},{330} {x0 + sgn * 34},{268}", fill=A1D if color == A1 else A2L)
        s.F("rect", x=100, y=180, width=312, height=130, rx=14, fill=color)
        txt(s, text, cx=256, cy=245, w=270, h=84)
    return fn


def hanging(text, color, text_c=LIGHT):
    def fn(s):
        s.M("M150 200 L256 90 L362 200", DARK, 10)
        s.F("circle", cx=256, cy=90, r=16, fill=MID)
        s.F("rect", x=50, y=196, width=412, height=200, rx=30, fill=color)
        txt(s, text, cx=256, cy=296, w=340, h=110, color=text_c)
    return fn


def stamp(rows, color, tick=False):
    def fn(s):
        s.open(transform="rotate(-12 256 256)")
        s.raw(f'<rect x="46" y="126" width="420" height="260" rx="34" fill="none" stroke="{color}" stroke-width="18"/>')
        s.raw(f'<rect x="72" y="152" width="368" height="208" rx="20" fill="none" stroke="{color}" stroke-width="7"/>')
        if tick:
            s.M("M120 262 L160 302 L222 222", color, 22)
            txt(s, rows[0], cx=310, cy=256, w=180, h=110, color=color)
        else:
            total = len(rows)
            for i, r in enumerate(rows):
                txt(s, r, cx=256, cy=256 + (i - (total - 1) / 2) * 92, w=320, h=78 if total > 1 else 110, color=color)
        s.close()
    return fn


SYM.update({
    "new-label": burst("NEW", A2), "sale-label": tag("SALE", A2), "free-label": ribbon("FREE", A1), "hot-label": pill("HOT", A2, flame=True),
    "limited-label": ribbon("LIMITED", A2), "bonus-label": burst("BONUS", A1), "live-label": pill("LIVE", A2, dot=True),
    "open-sign": hanging("OPEN", A1), "closed-sign": hanging("CLOSED", DARK),
    "approved-stamp": stamp(["APPROVED"], A1), "rejected-stamp": stamp(["REJECTED"], A2), "top-secret-stamp": stamp(["TOP", "SECRET"], A2),
    "sold-out-stamp": stamp(["SOLD", "OUT"], A2), "urgent-stamp": stamp(["URGENT"], A2), "done-stamp": stamp(["DONE"], A1, tick=True),
})


# ---------------------------------------------------------------- explainer and riddle cards
def x_badge(s):
    s.F("circle", cx=256, cy=256, r=190, fill=A2)
    s.M("M176 176 L336 336 M336 176 L176 336", LIGHT, 44)


def brain_icon(s):
    from _parts import brain
    brain(s)


def smile_icon(s):
    s.F("circle", cx=256, cy=256, r=190, fill=C["yellow"])
    for x in (196, 316):
        s.F("ellipse", outline=False, cx=x, cy=220, rx=18, ry=28, fill=INK)
    s.M("M170 300 C210 360 302 360 342 300", INK, 18)


def bubble_icon(s):
    s.F("path", d="M80 120 H432 C452 120 466 134 466 154 V320 C466 340 452 354 432 354 H220 L130 430 L150 354 H80 C60 354 46 340 46 320 V154 C46 134 60 120 80 120 Z", fill=LIGHT)
    for x in (176, 256, 336):
        s.F("circle", outline=False, cx=x, cy=237, r=24, fill=A1)


def arrow_icon(s):
    s.F("circle", cx=256, cy=256, r=190, fill=A2)
    s.M("M150 256 H350 M280 176 L360 256 L280 336", LIGHT, 40)


ICONS = {"bulb": bulb, "q": qmark, "check": check_badge, "x": x_badge, "star": star, "key": key, "mag": magnifier,
         "stairs": stairs, "hourglass": hourglass, "brain": brain_icon, "smile": smile_icon, "bubble": bubble_icon, "arrow": arrow_icon}


def ecard(rows, color=A1, icon=None, text_c=LIGHT):
    def fn(s):
        card(s, color)
        if icon:
            place(s, ICONS[icon], 256, 160, 0.3)
            lines(s, rows, cy=320, h=70 if len(rows) > 1 else 92, gap=14, color=text_c, w=360)
        else:
            lines(s, rows, cy=256, h=96 if len(rows) > 1 else 130, gap=20, color=text_c, w=370)
    return fn


def split(left, right, mid=None):
    def fn(s):
        s.F("path", d="M84 70 H256 V442 H84 C60 442 40 422 40 398 V114 C40 90 60 70 84 70 Z", fill=A2)
        s.F("path", d="M256 70 H428 C452 70 472 90 472 114 V398 C472 422 452 442 428 442 H256 Z", fill=A1)
        txt(s, left, cx=140, cy=256, w=140 if mid else 170, h=70)
        txt(s, right, cx=372, cy=256, w=140 if mid else 170, h=70)
        if mid:
            s.F("circle", cx=256, cy=256, r=50, fill=LIGHT)
            txt(s, mid, cx=256, cy=256, w=64, h=44, color=DARK)
    return fn


def level(name, n):
    def fn(s):
        card(s, A1)
        txt(s, name, cy=170, w=340, h=90)
        for i in range(4):
            h = 50 + i * 34
            s.F("rect", x=126 + i * 72, y=400 - h, width=52, height=h, rx=10, fill=A2 if i < n else A1L)
    return fn


def countdown(s):
    card(s, A1)
    for i, (x, t) in enumerate(((136, "3"), (256, "2"), (376, "1"))):
        s.F("circle", cx=x, cy=256, r=78, fill=A2 if i == 2 else A1L)
        txt(s, t, cx=x, cy=256, w=80, h=86, color=LIGHT if i == 2 else DARK)


CON = {
    "did-you-know": ecard(["DID YOU", "KNOW?"], icon="bulb"), "myth-vs-fact": split("MYTH", "FACT", "VS"),
    "myth": ecard(["MYTH"], A2, "x"), "fact": ecard(["FACT"], A1, "check"), "true-or-false": split("TRUE", "FALSE", "OR"),
    "true-card": ecard(["TRUE"], A1, "check"), "false-card": ecard(["FALSE"], A2, "x"), "fact-check": ecard(["FACT", "CHECK"], icon="mag"),
    "quiz-time": ecard(["QUIZ", "TIME!"], A2, "q"), "question-card": ecard(["QUESTION"], A1, "q"), "answer-card": ecard(["ANSWER"], A1, "bulb"),
    "correct-answer": ecard(["CORRECT!"], A1, "check"), "wrong-answer": ecard(["WRONG!"], A2, "x"), "answer-reveal": ecard(["ANSWER", "REVEAL"], A2, "star"),
    "hint": ecard(["HINT"], A1, "bulb"), "pro-tip": ecard(["PRO TIP"], A2, "star"), "key-takeaway": ecard(["KEY", "TAKEAWAY"], A1, "key"),
    "summary": ecard(["SUMMARY"], A1, "bubble"), "step-by-step": ecard(["STEP BY", "STEP"], A1, "stairs"), "before-and-after": split("BEFORE", "AFTER"),
    "pros-and-cons": split("CONS", "PROS"), "versus": ecard(["VS"], A2), "comparison": split("THIS", "THAT", "VS"),
    "top-10": ecard(["TOP", "10"], A2), "ranking": ecard(["RANKING"], A1, "star"), "spoiler-alert": ecard(["SPOILER", "ALERT!"], A2),
    "easy-level": level("EASY", 1), "medium-level": level("MEDIUM", 2), "hard-level": level("HARD", 3), "expert-level": level("EXPERT", 4),
    "bonus-question": ecard(["BONUS", "QUESTION"], A2, "star"), "final-question": ecard(["FINAL", "QUESTION"], A1, "q"),
    "times-up": ecard(["TIME'S", "UP!"], A2, "hourglass"), "score": ecard(["SCORE"], A1, "star"), "fifty-fifty-lifeline": ecard(["50:50"], A2),
    "think-about-it": ecard(["THINK", "ABOUT IT"], A1, "brain"), "guess-the-answer": ecard(["GUESS THE", "ANSWER"], A2, "q"),
    "comment-your-answer": ecard(["COMMENT", "YOUR ANSWER"], A1, "bubble"), "next-question": ecard(["NEXT", "QUESTION"], A1, "arrow"),
    "countdown-3-2-1": countdown,
}

BRAIN = {
    "brain-teaser-card": ecard(["BRAIN", "TEASER"], A1, "brain"), "riddle-card": ecard(["RIDDLE"], A2, "q"),
    "riddle-answer-card": ecard(["RIDDLE", "ANSWER"], A1, "bulb"), "emoji-puzzle": ecard(["EMOJI", "PUZZLE"], A2, "smile"),
    "rebus-puzzle": ecard(["REBUS", "PUZZLE"], A1, "q"), "trick-question": ecard(["TRICK", "QUESTION"], A2, "q"),
    "lateral-thinking-puzzle": ecard(["LATERAL", "THINKING"], A1, "brain"), "who-am-i-card": ecard(["WHO", "AM I?"], A2, "q"),
    "what-comes-next": ecard(["WHAT COMES", "NEXT?"], A1, "arrow"), "odd-one-out": ecard(["ODD ONE", "OUT"], A2, "mag"),
    "logic-puzzle-card": ecard(["LOGIC", "PUZZLE"], A1, "brain"), "puzzle-solved-card": ecard(["SOLVED!"], A1, "check"),
    "only-geniuses-can-solve": ecard(["ONLY GENIUSES", "CAN SOLVE"], A2, "brain"),
}


# ---------------------------------------------------------------- celebrations
def crescent_star(s, x, y, r, color):
    s.F("path", d=f"M{x + r * 0.2:.0f} {y - r:.0f} A{r} {r} 0 1 0 {x + r * 0.2:.0f} {y + r:.0f} A{r * 0.8:.0f} {r * 0.8:.0f} 0 1 1 {x + r * 0.2:.0f} {y - r:.0f} Z", fill=color)
    s.F("polygon", points=star_pts(x + r * 0.55, y - r * 0.15, r * 0.32, r * 0.13, 5), fill=color)


def greeting(arabic, rows):
    def fn(s):
        card(s, A1)
        crescent_star(s, 256, 128, 40, A2L)
        txt(s, arabic, "arabic", 256, 236, 360, 110)
        lines(s, rows, cy=362, h=46, gap=10, w=340, color=A2L)
    return fn


def festive(rows):
    def fn(s):
        card(s, A2)
        for x, y, r in ((96, 120, 18), (420, 110, 22), (110, 400, 16), (410, 400, 20), (256, 104, 14)):
            s.F("polygon", points=star_pts(x, y, r, r * 0.4, 4), fill=LIGHT)
        lines(s, rows, cy=266, h=96, gap=20, w=370)
    return fn


CEL = {
    "eid-mubarak-tile": greeting("عيد مبارك", ["EID MUBARAK"]),
    "ramadan-kareem-tile": greeting("رمضان كريم", ["RAMADAN KAREEM"]),
    "ramadan-mubarak-tile": greeting("رمضان مبارك", ["RAMADAN MUBARAK"]),
    "happy-new-year-tile": festive(["HAPPY", "NEW YEAR"]),
    "happy-birthday-tile": festive(["HAPPY", "BIRTHDAY"]),
}


# ---------------------------------------------------------------- religion-faith
SURAHS = ("الفاتحة البقرة آل_عمران النساء المائدة الأنعام الأعراف الأنفال التوبة يونس هود يوسف الرعد إبراهيم الحجر النحل الإسراء الكهف مريم طه "
          "الأنبياء الحج المؤمنون النور الفرقان الشعراء النمل القصص العنكبوت الروم لقمان السجدة الأحزاب سبأ فاطر يس الصافات ص الزمر غافر "
          "فصلت الشورى الزخرف الدخان الجاثية الأحقاف محمد الفتح الحجرات ق الذاريات الطور النجم القمر الرحمن الواقعة الحديد المجادلة الحشر "
          "الممتحنة الصف الجمعة المنافقون التغابن الطلاق التحريم الملك القلم الحاقة المعارج نوح الجن المزمل المدثر القيامة الإنسان المرسلات "
          "النبأ النازعات عبس التكوير الانفطار المطففين الانشقاق البروج الطارق الأعلى الغاشية الفجر البلد الشمس الليل الضحى الشرح التين "
          "العلق القدر البينة الزلزلة العاديات القارعة التكاثر العصر الهمزة الفيل قريش الماعون الكوثر الكافرون النصر المسد الإخلاص الفلق الناس")
SURAH_AR = [w.replace("_", " ") for w in SURAHS.split()]
assert len(SURAH_AR) == 114, len(SURAH_AR)

NAMES_AR = """الرحمن الرحيم الملك القدوس السلام المؤمن المهيمن العزيز الجبار المتكبر الخالق البارئ المصور الغفار القهار الوهاب الرزاق الفتاح
العليم القابض الباسط الخافض الرافع المعز المذل السميع البصير الحكم العدل اللطيف الخبير الحليم العظيم الغفور الشكور العلي الكبير
الحفيظ المقيت الحسيب الجليل الكريم الرقيب المجيب الواسع الحكيم الودود المجيد الباعث الشهيد الحق الوكيل القوي المتين الولي الحميد
المحصي المبدئ المعيد المحيي المميت الحي القيوم الواجد الماجد الواحد الأحد الصمد القادر المقتدر المقدم المؤخر الأول الآخر الظاهر
الباطن الوالي المتعالي البر التواب المنتقم العفو الرءوف مالك_الملك ذو_الجلال_والإكرام المقسط الجامع الغني المغني المانع الضار النافع النور
الهادي البديع الباقي الوارث الرشيد الصبور""".split()
NAMES_AR = [n.replace("_", " ") for n in NAMES_AR]
assert len(NAMES_AR) == 99, len(NAMES_AR)

MONTHS_AR = ["محرم", "صفر", "ربيع الأول", "ربيع الآخر", "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان", "رمضان", "شوال", "ذو القعدة", "ذو الحجة"]


def latin(name):
    return " ".join(w[:1].upper() + w[1:] if not w.startswith(("al-", "ar-", "as-", "an-", "at-", "ad-", "az-", "ash-")) else w[:w.index("-") + 1] + w[w.index("-") + 1:].capitalize()
                    for w in name.split(" "))


def surah_tile(num, arabic, name):
    def fn(s):
        card(s, A1, 50, 462)
        s.F("path", d="M96 440 V200 C96 120 180 84 256 84 C332 84 416 120 416 200 V440 Z", fill=LIGHT)
        s.F("circle", cx=256, cy=50, r=36, fill=A2)
        txt(s, str(num), "black", 256, 50, 46, 34)
        txt(s, arabic, "arabic", 256, 236, 280, 130, DARK)
        txt(s, latin(name).upper(), "black", 256, 390, 280, 40, A1)
    return fn


def name_tile(num, arabic, name):
    def fn(s):
        sq = " ".join(f"{x:.0f},{y:.0f}" for x, y in (arc_pt(256, 236, 210, a) for a in (-90, 0, 90, 180)))
        for outline in (True, False):     # two squares make the eight-pointed star; outline only around both
            for rot in (0, 45):
                s.F("polygon", outline=outline, points=sq, fill=A1, transform=f"rotate({rot} 256 236)")
        s.F("circle", cx=256, cy=236, r=160, fill=LIGHT)
        txt(s, arabic, "arabic", 256, 230, 250, 120, DARK)
        s.F("rect", x=86, y=410, width=340, height=70, rx=35, fill=A2)
        txt(s, latin(name), "black", 256, 445, 300, 40)
        txt(s, str(num), "black", 256, 120, 40, 26, A1)
    return fn


def month_tile(num, arabic, name):
    def fn(s):
        s.F("rect", x=56, y=70, width=400, height=380, rx=40, fill=LIGHT)
        s.F("path", d="M56 150 V110 C56 88 74 70 96 70 H416 C438 70 456 88 456 110 V150 Z", fill=A1)
        for x in (150, 362):
            s.T(f"M{x} 46 V96", DARK, 16)
        txt(s, str(num), "black", 256, 112, 60, 50)
        txt(s, arabic, "arabic", 256, 270, 320, 120, DARK)
        txt(s, latin(name).upper(), "black", 256, 400, 330, 46, A1)
    return fn


def calligraphy(rows, panel=GREEN_D, ink=GOLD, arch=True):
    def fn(s):
        if arch:
            s.F("path", d="M60 470 V210 C60 110 160 46 256 46 C352 46 452 110 452 210 V470 Z", fill=panel)
            s.raw(f'<path d="M86 452 V214 C86 128 172 72 256 72 C340 72 426 128 426 214 V452 Z" fill="none" stroke="{ink}" stroke-width="6"/>')
        else:
            s.F("rect", x=40, y=90, width=432, height=332, rx=30, fill=panel)
            s.raw(f'<rect x="62" y="112" width="388" height="288" rx="18" fill="none" stroke="{ink}" stroke-width="6"/>')
        n = len(rows)
        top, bot = (150, 420) if arch else (140, 372)
        h = (bot - top) / n
        for i, r in enumerate(rows):
            txt(s, r, "arabic", 256, top + h * (i + 0.5), 300, h * 0.8, ink)
    return fn


def pillar_word(arabic, label):
    def fn(s):
        card(s, A1)
        txt(s, arabic, "arabic", 256, 220, 330, 140)
        s.F("rect", x=106, y=340, width=300, height=64, rx=32, fill=A2)
        txt(s, label, "black", 256, 372, 250, 38)
    return fn


def five_pillars(s):
    card(s, A1)
    s.F("polygon", points="96,190 256,110 416,190", fill=A2)
    for i in range(5):
        s.F("rect", x=112 + i * 62, y=200, width=40, height=150, rx=6, fill=LIGHT)
    s.F("rect", x=88, y=350, width=336, height=26, rx=6, fill=A2)
    txt(s, "5 PILLARS", "black", 256, 412, 300, 36)


def belief(arabic, rows):
    def fn(s):
        card(s, A1)
        txt(s, arabic, "arabic", 256, 180, 340, 110)
        s.M("M120 266 H392", A1L, 6)
        lines(s, rows, cy=350, h=50, gap=12, w=340, color=A2L)
    return fn


def six_articles(s):
    card(s, A1)
    for i in range(6):
        x, y = arc_pt(256, 220, 96, -90 + i * 60)
        s.F("circle", cx=f"{x:.0f}", cy=f"{y:.0f}", r=40, fill=LIGHT)
        txt(s, str(i + 1), "black", x, y, 34, 40, A1)
    txt(s, "6 ARTICLES OF FAITH", "black", 256, 392, 360, 40, A2L)


def om(s):
    s.F("circle", cx=256, cy=256, r=210, fill="#F28C28")
    s.F("circle", cx=256, cy=256, r=180, fill="#FFF3DF")
    txt(s, "ॐ", "devanagari", 256, 262, 260, 260, "#C2410C")


def ik_onkar(s):
    s.F("circle", cx=256, cy=256, r=210, fill="#1E3A8A")
    s.F("circle", cx=256, cy=256, r=180, fill="#FFF3DF")
    txt(s, "ੴ", "gurmukhi", 256, 262, 270, 250, "#1E3A8A")


def hijri_new_year(s):
    s.F("rect", x=40, y=70, width=432, height=372, rx=44, fill=GREEN_D)
    crescent_star(s, 256, 150, 50, GOLD)
    txt(s, "١ محرم", "arabic", 256, 270, 260, 90, GOLD)
    lines(s, ["HAPPY HIJRI", "NEW YEAR"], cy=370, h=40, gap=10, w=320, color="#FFF3DF")


def talbiyah(s):
    s.F("rect", x=40, y=90, width=432, height=332, rx=30, fill="#FFFFFF")
    s.raw('<rect x="62" y="112" width="388" height="288" rx="18" fill="none" stroke="#1F1F24" stroke-width="5"/>')
    s.F("rect", x=206, y=136, width=100, height=96, rx=4, fill="#1F1F24")
    s.F("rect", outline=False, x=206, y=160, width=100, height=12, fill=GOLD)
    txt(s, "لبيك اللهم لبيك", "arabic", 256, 318, 340, 110, "#1F1F24")


def religion():
    out = {}
    cat = json.loads((ROOT / "catalog" / "religion-faith.json").read_text(encoding="utf-8"))
    groups = {g["id"]: g for g in cat["groups"]}
    for i, it in enumerate(groups["surahs"]["items"]):
        nm = it["name"].replace("surah ", "", 1).replace("'", "")
        out[it["id"]] = surah_tile(i + 1, SURAH_AR[i], nm)
    for i, it in enumerate(groups["names-99"]["items"]):
        nm = it["name"].replace(" name tile", "")
        n = int(re.search(r"name (\d+)", " ".join(it.get("aka", []))).group(1))
        out[it["id"]] = name_tile(n, NAMES_AR[n - 1], nm)
    for i, it in enumerate(groups["islamic-months"]["items"]):
        nm = it if isinstance(it, str) else it[0] if isinstance(it, list) else it["name"]
        iid = it["id"] if isinstance(it, dict) else slug(nm)
        out[iid] = month_tile(i + 1, MONTHS_AR[i], nm.replace("ramadan month", "ramadan"))
    out.update({
        "islamic-calligraphy": calligraphy(["الحمد لله"]),
        "bismillah-calligraphy": calligraphy(["بسم الله", "الرحمن الرحيم"]),
        "shahada-calligraphy": calligraphy(["لا إله إلا الله", "محمد رسول الله"]),
        "allah-calligraphy-tile": calligraphy(["الله"], arch=False),
        "takbir-tile": calligraphy(["الله أكبر"], arch=False),
        "hijri-new-year-tile": hijri_new_year,
        "five-pillars-of-islam": five_pillars,
        "shahada": pillar_word("الشهادة", "SHAHADA"), "sawm": pillar_word("الصوم", "SAWM"), "hajj": pillar_word("الحج", "HAJJ"),
        "six-articles-of-faith": six_articles,
        "belief-in-allah": belief("الإيمان بالله", ["BELIEF IN", "ALLAH"]),
        "belief-in-the-angels-tile": belief("الإيمان بالملائكة", ["BELIEF IN", "THE ANGELS"]),
        "belief-in-the-holy-books": belief("الإيمان بالكتب", ["BELIEF IN", "THE HOLY BOOKS"]),
        "belief-in-the-prophets-tile": belief("الإيمان بالرسل", ["BELIEF IN", "THE PROPHETS"]),
        "belief-in-the-day-of-judgement": belief("الإيمان باليوم الآخر", ["BELIEF IN THE", "DAY OF JUDGEMENT"]),
        "belief-in-divine-decree": belief("الإيمان بالقدر", ["BELIEF IN", "DIVINE DECREE"]),
        "talbiyah-tile": talbiyah, "om-symbol": om, "ik-onkar": ik_onkar,
    })
    return out


if __name__ == "__main__":
    only = sys.argv[1:] or None
    for category, table in (("symbols-signs", SYM), ("concepts-ideas", CON), ("brain-teasers-logic", BRAIN),
                            ("celebrations-holidays", CEL), ("religion-faith", religion())):
        mine = [i for i in (only or []) if i in table]
        if only and not mine:
            continue
        run(category, table, mine or None)
