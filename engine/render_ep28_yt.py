import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep28")
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

PH = dict(lh=load_photo("leona_01.jpg"))
CR_L = "U.S. MARSHALS SERVICE PHOTO, 1988 · PUBLIC DOMAIN"

def crown(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-120, 60); p.lineTo(-130, -40); p.lineTo(-65, 10); p.lineTo(0, -70); p.lineTo(65, 10); p.lineTo(130, -40); p.lineTo(120, 60); p.close()
    c.drawPath(p, P(C(GOLD2, a))); c.drawPath(p, P(C(INK, a), stroke=6))
    for px in (-130, 0, 130): c.drawCircle(px, (-40, -70, -40)[(px + 130) // 130], 14, P(C(RED, a)))
    c.restore()

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        dog(c, CX - 40, 900, 1.6, 1 - out, t)
        counter(c, 12000000, CX, 560, 150 * lerp(1.15, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1 - out, prefix="$", glow=24)
        pop_text(c, "LEFT TO HER DOG", CX, 1200, ANTON, 104, CREAM, prog(t, W_("hook", "dog.") - 0.3, 0.25) * (1 - out))
    if out > 0:
        photo_card(c, PH["lh"], CX, 780, 500, 660, (t - b1) / max(1, D - b1), out, 1.0, 1.1, focus=(0.5, 0.35), rot=-1.5, credit=CR_L)
        pop_text(c, "LEONA HELMSLEY", CX, 390, ANTON, 112, CREAM, prog(t, W_("hook", "Leona") - 0.15, 0.25))

def sc_queen(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i, lab in enumerate(["HOTEL", "HOTEL", "HOTEL"]):
        building(c, 230 + i * 310, 1150, 0.42, eo(prog(t, 0.1 + i * 0.2, 0.3)), lab, cols=3)
    pop_text(c, "A NEW YORK HOTEL EMPIRE", CX, 400, ANTON, 92, CREAM, prog(t, 0.0, 0.25))
    pc = eo(prog(t, W_("queen", "Queen") - 0.3, 0.35))
    crown(c, CX, 600, lerp(0.6, 1.0, back(pc)), pc)
    pq = prog(t, W_("queen", "Mean.") - 0.3, 0.22)
    if pq > 0: stamp(c, CX, 790, "\"QUEEN OF MEAN\"", RED, 120, -5, pq, sc=lerp(2.2, 1, eo(pq)))

def sc_taxes(c, t, D):
    a = eo(prog(t, 0, 0.3))
    calendar(c, CX, 560, 0.7, a, "1989", "CONVICTED")
    k = eo(prog(t, W_("taxes", "$1.2") - 0.3, 0.9))
    if k > 0: counter(c, 1200000 * k, CX, 900, 150, RED, a, prefix="~$", glow=18)
    pop_text(c, "IN FEDERAL TAXES, EVADED", CX, 1020, BEBAS, 70, CREAM, eo(prog(t, W_("taxes", "federal") - 0.2, 0.3)))

def sc_quote(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("quote", 1)
    for i in range(5): person(c, 200 + i * 170, 560, 46, MUTED, a * 0.7)
    pop_text(c, "HER FORMER HOUSEKEEPER:", CX, 400, BEBAS, 80, CREAM, prog(t, 0.0, 0.25))
    pq = prog(t, b1 - 0.05, 0.3)
    if pq > 0:
        pop_text(c, "\"ONLY THE LITTLE PEOPLE", CX, 780, ANTON, 92, GOLD2, pq, glow=18, glow_rgb=GOLD)
        pop_text(c, "PAY TAXES.\"", CX, 900, ANTON, 120, GOLD2, prog(t, W_("quote", "taxes.\"") - 0.3, 0.3), glow=18, glow_rgb=GOLD)
    pd = prog(t, W_("quote", "denied") - 0.2, 0.22)
    if pd > 0: stamp(c, CX, 1130, "SHE DENIED IT", CREAM, 96, -5, pd, sc=lerp(2.2, 1, eo(pd)))

def sc_prison(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["lh"], CX, 780, 480, 640, t / D, a, 1.0, 1.08, focus=(0.5, 0.35), credit=CR_L, dim=0.3)
    bars(c, eo(prog(t, 0.2, 0.4)), y0=330, y1=1240)
    pp = prog(t, W_("prison", "prison.") - 0.3, 0.22)
    if pp > 0: stamp(c, CX, 1150, "FEDERAL PRISON", RED, 96, -5, pp, sc=lerp(2.2, 1, eo(pp)))

def sc_dog(c, t, D):
    a = eo(prog(t, 0, 0.3))
    paper_doc(c, CX - 200, 760, 0.8, -8, a * 0.9, "LAST WILL", "", "TESTAMENT", lines=7)
    pd = eo(prog(t, W_("dog", "Maltese,") - 0.4, 0.35))
    dog(c, CX + 170, 940, 1.2 * lerp(0.6, 1, back(pd)), pd, t)
    k = eo(prog(t, W_("dog", "$12") - 0.3, 0.9))
    if k > 0: counter(c, 12000000 * k, CX, 470, 150, GOLD2, a, prefix="$", glow=24)
    pop_text(c, "\"TROUBLE\"", CX + 170, 1210, ANTON, 104, CREAM, prog(t, W_("dog", "Trouble.") - 0.2, 0.25))
    pill(c, "2007", 590, eo(prog(t, W_("dog", "2007,") - 0.2, 0.3)), CREAM, 54, 200)

def sc_judge(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("judge", 1)
    out = eo(prog(t, b1 + 0.1, 0.3))
    k = eo(prog(t, 0.15, 0.8))
    if out < 1:
        dog(c, CX, 1000, 1.0, a * (1 - out), t)
        counter(c, 12000000 - 10000000 * k, CX, 600, 160, GOLD2 if k < 0.5 else CREAM, a * (1 - out), prefix="$", glow=20)
        pc = prog(t, W_("judge", "$2") - 0.3, 0.22)
        if pc > 0: stamp(c, CX, 760, "CUT BY A JUDGE", RED, 96, -5, pc * (1 - out), sc=lerp(2.2, 1, eo(pc)))
    if out > 0:
        building(c, CX, 1160, 0.7, out, "FOUNDATION", cols=5)
        counter(c, 10000000, CX, 560, 160, GOLD2, out, prefix="$", glow=20)
        pop_text(c, "TO HER CHARITABLE FOUNDATION", CX, 690, BEBAS, 64, CREAM, prog(t, W_("judge", "charitable") - 0.2, 0.3))

def sc_loopend(c, t, D):
    dog(c, CX - 40, 900, 1.6, 1.0, t)
    pop_text(c, "YES,", CX, 450, ANTON, 150, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, queen=sc_queen, taxes=sc_taxes, quote=sc_quote, prison=sc_prison, dog=sc_dog, judge=sc_judge,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"prison"}
_IMP = [("hook", "dog.", -0.3, 0.4), ("queen", "Mean.", -0.3, 0.35), ("taxes", "convicted", -0.2, 0.35),
        ("quote", "taxes.\"", -0.3, 0.4), ("prison", "prison.", -0.3, 0.4), ("rehook", "stranger.", -0.2, 0.35),
        ("dog", "Trouble.", -0.2, 0.35), ("judge", "$2", -0.3, 0.35), ("loopend", "Yes,", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$12", 0.0), ("dog", "$12", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
