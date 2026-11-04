import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep29")
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

PH = dict(dig=load_photo("giant_01.jpg"), gt=load_photo("giant_02.jpg"), pt=load_photo("barnum_01.jpg"))
CR_D = "EXCAVATION OF THE CARDIFF GIANT, 1869 · PUBLIC DOMAIN"
CR_G = "THE CARDIFF GIANT · BAIN NEWS SERVICE / LOC · PUBLIC DOMAIN"
CR_B = "P.T. BARNUM, c.1860 · MATHEW BRADY STUDIO · PUBLIC DOMAIN"

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    photo_card(c, PH["dig"], CX, 790, 520, 720, t / D, 1.0, 1.0, 1.14, focus=(0.5, 0.6), rot=-1.5, credit=CR_D, dim=0.3 * eo(prog(t, b1, 0.3)))
    pop_text(c, "NEW YORK · 1869", CX, 390, ANTON, 112, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    if t > b1 - 0.2:
        for i in range(5): person(c, 200 + i * 170, 1180, 44, GOLD2 if i % 2 else CREAM, eo(prog(t, b1 + i * 0.08, 0.3)))
    pf = prog(t, W_("hook", "fake.") - 0.25, 0.22)
    if pf > 0: stamp(c, CX, 760, "IT WAS A FAKE", RED, 120, -6, pf, sc=lerp(2.2, 1, eo(pf)))

def sc_dig(c, t, D):
    a = eo(prog(t, 0, 0.3))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 700), (0, 1240)], [C((70, 52, 36), a), C((36, 26, 18), a)]))
    c.drawRect(skia.Rect(40, 700, W - 40, 1240), g)
    k = eo(prog(t, W_("dig", "huge.") - 0.6, 0.8))
    stone_giant(c, CX, lerp(1260, 960, k), 0.95, a * (0.3 + 0.7 * k))
    pop_text(c, "CARDIFF, NEW YORK", CX, 400, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    calendar(c, CX, 560, 0.5, eo(prog(t, W_("dig", "October") - 0.2, 0.3)), "OCT 1869", "")

def sc_hull(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("hull", 1)
    pop_text(c, "THE TRUTH:", CX, 400, ANTON, 112, GOLD2, prog(t, 0.0, 0.25), glow=18, glow_rgb=GOLD)
    id_card(c, CX, 640, 0.85, -3, eo(prog(t, W_("hull", "George") - 0.3, 0.35)), "GEORGE HULL", "THE MAN BEHIND IT", tag_="HOAXER")
    pg = eo(prog(t, W_("hull", "gypsum,") - 0.4, 0.4))
    c.drawRect(skia.Rect(CX - 330, 930, CX + 330, 1060), P(C((214, 206, 190), pg))); c.drawRect(skia.Rect(CX - 330, 930, CX + 330, 1060), P(C(INK, pg), stroke=5))
    text(c, "BLOCK OF GYPSUM", CX, 1012, BEBAS, 60, INK, pg, spacing=4)
    pb = prog(t, W_("hull", "buried") - 0.2, 0.22)
    if pb > 0: stamp(c, CX, 1170, "BURIED A YEAR EARLIER", RED, 80, -4, pb, sc=lerp(2.2, 1, eo(pb)))

def sc_barnum(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("barnum", 1)
    photo_card(c, PH["pt"], CX, 750, 460, 580, t / D, a, 1.0, 1.12, focus=(0.5, 0.3), rot=1.5, credit=CR_B)
    pop_text(c, "P.T. BARNUM", CX, 390, ANTON, 120, CREAM, prog(t, 0.0, 0.25))
    k = eo(prog(t, W_("barnum", "$50,000") - 0.3, 0.8))
    if k > 0: counter(c, 50000 * k, CX, 1210, 130, GOLD2, k, prefix="$", glow=22)
    pn = prog(t, b1 + 0.1, 0.22)
    if pn > 0: stamp(c, CX, 760, "\"NO.\"", RED, 200, -8, pn, sc=lerp(2.2, 1, eo(pn)))

def sc_copy(c, t, D):
    a = eo(prog(t, 0, 0.3))
    k = eo(prog(t, W_("copy", "copy,") - 0.4, 0.6))
    stone_giant(c, CX, 640, 0.95, a)
    stone_giant(c, CX, 1000, 0.95, k, rgb=(206, 196, 176))
    tag(c, CX - 300, 560, "ORIGINAL FAKE", a, -6, MUTED)
    tag(c, CX - 300, 920, "BARNUM'S FAKE", k, -6, RED)
    pr = prog(t, W_("copy", "real") - 0.2, 0.22)
    if pr > 0: stamp(c, CX, 1200, "\"MINE IS THE REAL ONE\"", GOLD2, 90, -4, pr, sc=lerp(2.2, 1, eo(pr)))
    pop_text(c, "HIS OWN COPY", CX, 400, ANTON, 112, CREAM, prog(t, 0.0, 0.25))

def sc_sucker(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("sucker", 1)
    pop_text(c, "DAVID HANNUM, AN OWNER:", CX, 420, BEBAS, 80, CREAM, prog(t, W_("sucker", "Hannum,") - 0.3, 0.25))
    pq = prog(t, W_("sucker", "sucker") - 0.4, 0.3)
    if pq > 0:
        pop_text(c, "\"THERE'S A SUCKER", CX, 700, ANTON, 112, GOLD2, pq, glow=18, glow_rgb=GOLD)
        pop_text(c, "BORN EVERY MINUTE\"", CX, 830, ANTON, 112, GOLD2, prog(t, W_("sucker", "minute.\"") - 0.3, 0.3), glow=18, glow_rgb=GOLD)
    clock(c, CX, 1060, 90, eo(prog(t, 0.2, 0.3)), t_h=t * 2)
    pb = prog(t, W_("sucker", "Barnum.", 0) - 0.3, 0.22) if t > b1 - 0.5 else 0
    if pb > 0: stamp(c, CX, 1200, "CREDITED TO BARNUM", RED, 84, -5, pb, sc=lerp(2.2, 1, eo(pb)))

def sc_court(c, t, D):
    a = eo(prog(t, 0, 0.3))
    calendar(c, CX, 560, 0.6, a, "1870", "COURT")
    pop_text(c, "THE RULING:", CX, 400, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pq = prog(t, W_("court", "sued") - 0.3, 0.3)
    if pq > 0:
        pop_text(c, "YOU CAN'T BE SUED", CX, 860, ANTON, 104, GOLD2, pq, glow=18, glow_rgb=GOLD)
        pop_text(c, "FOR CALLING A FAKE", CX, 980, ANTON, 92, CREAM, prog(t, W_("court", "calling") - 0.2, 0.3))
    pf = prog(t, W_("court", "fake.") - 0.3, 0.22)
    if pf > 0: stamp(c, CX, 1150, "A FAKE", RED, 150, -6, pf, sc=lerp(2.2, 1, eo(pf)))

def sc_loopend(c, t, D):
    photo_card(c, PH["dig"], CX, 790, 520, 720, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.6), rot=-1.5, credit=CR_D, dim=0.3)
    pop_text(c, "AND IT ALL BEGAN...", CX, 390, ANTON, 112, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, dig=sc_dig, hull=sc_hull, barnum=sc_barnum, copy=sc_copy, sucker=sc_sucker, court=sc_court,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = set()
_IMP = [("hook", "fake.", -0.25, 0.45), ("dig", "huge.", -0.3, 0.4), ("hull", "buried", -0.2, 0.3),
        ("barnum", "no.", -0.1, 0.35), ("rehook", "crazier.", -0.2, 0.35), ("copy", "real", -0.2, 0.35),
        ("sucker", "minute.\"", -0.3, 0.35), ("court", "fake.", -0.3, 0.4), ("loopend", "And", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("barnum", "$50,000", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
