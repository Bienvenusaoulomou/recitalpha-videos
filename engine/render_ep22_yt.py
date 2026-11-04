import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep22")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
from kit3 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999
def B(sid, i):
    try: return beat(sid, i)
    except Exception: return 999

PH = dict(tw=load_photo("twain_01.jpg"), pg=load_photo("paige_01.jpg"))
CR_T = "PHOTO: A.F. BRADLEY, 1907 · LIBRARY OF CONGRESS · PUBLIC DOMAIN"
CR_P = "SCIENTIFIC AMERICAN, 1901 · PUBLIC DOMAIN"

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    photo_card(c, PH["tw"], CX, 790, 540, 700, t / D, 1.0, 1.0, 1.14, focus=(0.5, 0.3), rot=-1.5, credit=CR_T, dim=0.35 * eo(prog(t, b1 - 0.2, 0.3)))
    pop_text(c, "MARK TWAIN", CX, 390, ANTON, 120, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pe = prog(t, W_("hook", "everything") - 0.2, 0.22)
    if pe > 0: stamp(c, CX, 700, "LOST ALMOST EVERYTHING", RED, 74, -5, pe * (1 - eo(prog(t, b1 - 0.2, 0.3))), sc=lerp(2.2, 1, eo(pe)))
    pr = prog(t, W_("hook", "rich.") - 0.25, 0.25)
    if pr > 0: stamp(c, CX, 860, "\"IT'LL MAKE ME RICH\"", GOLD2, 84, 4, pr, sc=lerp(2.2, 1, eo(pr)))

def sc_machine(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["pg"], CX, 790, 760, 680, t / D, a, 1.0, 1.1, focus=(0.5, 0.5), credit=CR_P)
    pop_text(c, "THE PAIGE COMPOSITOR", CX, 390, ANTON, 96, GOLD2, prog(t, W_("machine", "Paige") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    pill(c, "SETS TYPE ALL BY ITSELF", 1205, eo(prog(t, W_("machine", "itself.") - 0.5, 0.3)), CREAM, 58, 760)

def sc_money(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("money", 1)
    pop_text(c, "TWAIN INVESTED", CX, 420, BEBAS, 90, CREAM, prog(t, 0.0, 0.25), s0=1.3)
    k = eo(prog(t, W_("money", "$300,000") - 0.3, 1.1))
    counter(c, 300000 * k, CX, 720, 190, GOLD2, a, prefix="$", glow=26)
    bills(c, CX - 260, 980, a * k, n=int(1 + 5 * k), rot=-8); bills(c, CX + 260, 980, a * k, n=int(1 + 5 * k), rot=8)
    pill(c, "MILLIONS IN TODAY'S MONEY", 1200, eo(prog(t, b1 - 0.1, 0.3)), GOLD2, 60, 820)

def sc_rival(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["pg"], 300, 700, 420, 380, t / D, a, 1.0, 1.05, credit=None, dim=0.55, rot=-3)
    pb = prog(t, 0.1, 0.22)
    if pb > 0: stamp(c, 300, 720, "BROKEN", RED, 90, -8, pb, sc=lerp(2, 1, eo(pb)))
    pl = eo(prog(t, W_("rival", "Linotype,") - 0.3, 0.35))
    press(c, 790, 820, 0.85 * lerp(0.6, 1, back(pl)), pl, t)
    pop_text(c, "LINOTYPE", 790, 520, ANTON, 104, GOLD2, prog(t, W_("rival", "Linotype,") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    pill(c, "TOOK OVER THE MARKET", 1180, eo(prog(t, W_("rival", "took") - 0.2, 0.3)), CREAM, 62, 780)

def sc_bankrupt(c, t, D):
    a = eo(prog(t, 0, 0.3))
    calendar(c, CX, 620, 0.9, a, "1894", "")
    pb = prog(t, W_("bankrupt", "bankruptcy.") - 0.3, 0.22)
    if pb > 0: stamp(c, CX, 1000, "BANKRUPT", RED, 170, -7, pb, sc=lerp(2.3, 1, eo(pb)))

def sc_tour(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("tour", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    globe(c, CX, 790, 300 * lerp(1, 0.75, out), a, t)
    pts = [(CX - 220, 700), (CX - 60, 640), (CX + 120, 760), (CX + 230, 860), (CX + 40, 930)]
    route(c, [(x, lerp(y, 790 + (y - 790) * 0.75, out)) for x, y in pts], clamp((t - 0.6) / 2.2), a)
    pop_text(c, "A WORLD LECTURE TOUR", CX, 390, ANTON, 96, CREAM, prog(t, W_("tour", "lecture") - 0.2, 0.25))
    pill(c, "AT ALMOST 60", 1180, eo(prog(t, W_("tour", "sixty,") - 0.3, 0.3)) * (1 - out), GOLD2, 64, 520)
    pf = prog(t, W_("tour", "full.") - 0.3, 0.22)
    if pf > 0: stamp(c, CX, 1140, "PAID BACK IN FULL", GOLD2, 104, -5, pf, sc=lerp(2.2, 1, eo(pf)))

def sc_loopend(c, t, D):
    photo_card(c, PH["tw"], CX, 790, 540, 700, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.3), rot=-1.5, credit=CR_T, dim=0.3)
    pop_text(c, "WHICH IS HOW...", CX, 390, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, machine=sc_machine, money=sc_money, rival=sc_rival, bankrupt=sc_bankrupt, tour=sc_tour,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"bankrupt"}
_IMP = [("hook", "everything", -0.2, 0.4), ("machine", "Paige", -0.2, 0.3), ("money", "$300,000", -0.2, 0.35),
        ("rehook", "breaking", -0.2, 0.3), ("rival", "Linotype,", -0.2, 0.3), ("bankrupt", "bankruptcy.", -0.3, 0.45),
        ("tour", "full.", -0.3, 0.4), ("loopend", "Which", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("money", "$300,000", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
