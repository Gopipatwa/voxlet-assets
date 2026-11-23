"""science: the 118 element tiles (atomic number, symbol, name; colour = element family).
Run: python drawings/science_elements.py [ids...]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from draw_lib import C, run  # noqa: E402
from text_tile import text_path  # noqa: E402

SYMS = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "
        "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu "
        "Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr "
        "Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og").split()
NAMES = ("hydrogen helium lithium beryllium boron carbon nitrogen oxygen fluorine neon sodium magnesium aluminium silicon "
         "phosphorus sulfur chlorine argon potassium calcium scandium titanium vanadium chromium manganese iron cobalt nickel "
         "copper zinc gallium germanium arsenic selenium bromine krypton rubidium strontium yttrium zirconium niobium molybdenum "
         "technetium ruthenium rhodium palladium silver cadmium indium tin antimony tellurium iodine xenon caesium barium "
         "lanthanum cerium praseodymium neodymium promethium samarium europium gadolinium terbium dysprosium holmium erbium "
         "thulium ytterbium lutetium hafnium tantalum tungsten rhenium osmium iridium platinum gold mercury thallium lead "
         "bismuth polonium astatine radon francium radium actinium thorium protactinium uranium neptunium plutonium americium "
         "curium berkelium californium einsteinium fermium mendelevium nobelium lawrencium rutherfordium dubnium seaborgium "
         "bohrium hassium meitnerium darmstadtium roentgenium copernicium nihonium flerovium moscovium livermorium tennessine oganesson").split()
assert len(SYMS) == 118 and len(NAMES) == 118

# family colours: (card, light band)
FAM = {
    "nonmetal": ("#4CB963", "#8FDCA0"),
    "noble": ("#8B5CF6", "#B9A0FA"),
    "alkali": ("#E5484D", "#F18A8E"),
    "alkaline": ("#F5913E", "#F9B57A"),
    "metalloid": ("#2FB5A8", "#7FD8CF"),
    "halogen": ("#F2B01E", "#FFD36B"),
    "post": ("#6B8FD6", "#A3BDEB"),
    "transition": ("#3D8BFD", "#7DB2FF"),
    "lanth": ("#E0629A", "#F7A1B5"),
    "actin": ("#B5323A", "#E5787D"),
    "unknown": ("#6B7280", "#A0A6B2"),
}


def family(z):
    if z in (1, 6, 7, 8, 15, 16, 34):
        return "nonmetal"
    if z in (2, 10, 18, 36, 54, 86, 118):
        return "noble"
    if z in (3, 11, 19, 37, 55, 87):
        return "alkali"
    if z in (4, 12, 20, 38, 56, 88):
        return "alkaline"
    if z in (5, 14, 32, 33, 51, 52):
        return "metalloid"
    if z in (9, 17, 35, 53, 85, 117):
        return "halogen"
    if z in (13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116):
        return "post"
    if 57 <= z <= 71:
        return "lanth"
    if 89 <= z <= 103:
        return "actin"
    if z >= 104 and z not in (113, 114, 115, 116, 117, 118):
        return "unknown"
    return "transition"


def tile(z, sym, name):
    def fn(s):
        base, light = FAM[family(z)]
        s.F("rect", x=50, y=50, width=412, height=412, rx=56, fill=base)
        s.F("rect", outline=False, x=66, y=66, width=380, height=88, rx=40, fill=light, fill_opacity="0.55")
        d, _ = text_path(str(z), "black", 256, 112, 150, 56)
        s.F("path", outline=False, d=d, fill="#FFFFFF", fill_opacity="0.9")
        d, _ = text_path(sym, "black", 256, 262, 290, 190)
        s.F("path", outline=False, d=d, fill="#FFFFFF")
        d, _ = text_path(name.capitalize(), "sans", 256, 396, 340 if len(name) > 9 else 300, 46)
        s.F("path", outline=False, d=d, fill="#FFFFFF")
    return fn


D = {f"element-{n}": tile(i + 1, SYMS[i], n) for i, n in enumerate(NAMES)}

if __name__ == "__main__":
    run("science", D, sys.argv[1:] or None)
