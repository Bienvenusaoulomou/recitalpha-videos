import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep25")
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

PH = dict(bs=load_photo("siegel_01.jpg"))
CR_S = "NYPD MUGSHOT, 1928 · PUBLIC DOMAIN"

def desert(c, a, t):
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 900), (0, 1240)], [C((90, 60, 40), a), C((40, 26, 18), a)]))
    c.drawRect(skia.Rect(40, 900, W - 40, 1240), g)
    for i in range(5):
        x = 140 + i * 210; c.drawLine(x, 1000, x + 4, 920, P(C((70, 100, 60), a), stroke=14))
        c.drawLine(x, 960, x - 26, 940, P(C((70, 100, 60), a), stroke=10)); c.drawLine(x + 2, 950, x + 28, 930, P(C((70, 100, 60), a), stroke=10))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["bs"], CX, 780, 520, 660, t / b1, 1 - out, 1.0, 1.12, focus=(0.5, 0.35), rot=-1.5, credit=CR_S)
        pop_text(c, "BUGSY SIEGEL", CX, 390, ANTON, 120, CREAM, prog(t, 0.0, 0.22) * (1 - out), s0=1.3)
    if out > 0:
        desert(c, out, t)
        casino_sign(c, CX, 640, 1.0, out, t)
        k = eo(prog(t, b1, 1.2))
        counter(c, 6000000 * k, CX, 1120, 150, RED, out, prefix="$", glow=20)
        pop_text(c, "THE BILL", CX, 390, BEBAS, 100, CREAM, out, s0=1.2)

def sc_vegas(c, t, D):
    a = eo(prog(t, 0, 0.3))
    desert(c, a, t)
    pop_text(c, "LAS VEGAS · 1946", CX, 400, ANTON, 112, CREAM, prog(t, 0.0, 0.25))
    pf = eo(prog(t, W_("vegas", "Flamingo.") - 0.4, 0.4))
    casino_sign(c, CX, 680, lerp(0.6, 1.0, back(pf)), pf, t)
    pill(c, "THE MOST LUXURIOUS IN TOWN", 1180, eo(prog(t, W_("vegas", "luxurious") - 0.2, 0.3)), GOLD2, 56, 800)

def sc_costs(c, t, D):
    a = eo(prog(t, 0, 0.3))
    k = eo(prog(t, 0.2, max(0.6, D - 0.8)))
    c.drawLine(160, 1150, 920, 1150, P(C(MUTED, a), stroke=3))
    n = 8
    for i in range(n):
        f = (i + 1) / n
        if f <= k + 0.001:
            h = 60 + 420 * f ** 1.6
            c.drawRect(skia.Rect(170 + i * 94, 1150 - h, 170 + i * 94 + 70, 1150), P(C(RED if f > 0.7 else GOLD2, a)))
    counter(c, 6000000 * k, CX, 440, 150, RED if k > 0.9 else GOLD2, a, prefix="$", glow=20)
    pm = prog(t, W_("costs", "$6") - 0.2, 0.22)
    if pm > 0: stamp(c, CX, 580, "MORE THAN $6 MILLION", RED, 84, -4, pm, sc=lerp(2.2, 1, eo(pm)))

def sc_opening(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("opening", 1)
    desert(c, a, t)
    casino_sign(c, CX, 650, 1.0, a, t)
    pop_text(c, "DEC 26, 1946", CX, 400, ANTON, 112, CREAM, prog(t, 0.0, 0.25))
    pu = prog(t, W_("opening", "finished.") - 0.4, 0.22)
    if pu > 0: stamp(c, CX, 960, "NOT EVEN FINISHED", RED, 100, -5, pu, sc=lerp(2.2, 1, eo(pu)))

def sc_closed(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("closed", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        casino_sign(c, CX, 680, 1.0, a * (1 - out), t, lights=1 - eo(prog(t, W_("closed", "shut") - 0.3, 0.4)))
        ps = prog(t, W_("closed", "down.") - 0.2, 0.22)
        if ps > 0: stamp(c, CX, 980, "CLOSED", RED, 170, -7, ps * (1 - out), sc=lerp(2.2, 1, eo(ps)))
        pop_text(c, "WITHIN WEEKS", CX, 400, ANTON, 112, CREAM, prog(t, 0.0, 0.25) * (1 - out))
    if out > 0:
        for i in range(5): person(c, 200 + i * 170, 560, 54, (110, 100, 90), out)
        pop_text(c, "HIS PARTNERS SUSPECTED...", CX, 400, ANTON, 90, CREAM, out)
        bills(c, CX, 860, out, n=6, rot=-6)
        pk = prog(t, W_("closed", "skimmed") - 0.2, 0.22)
        if pk > 0: stamp(c, CX, 1120, "SKIMMING", RED, 140, -6, pk, sc=lerp(2.2, 1, eo(pk)))

def sc_end(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("end", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["bs"], CX, 770, 480, 600, t / D, a * (1 - out), 1.0, 1.1, focus=(0.5, 0.35), credit=CR_S, dim=0.4)
        pill(c, "JUNE 20, 1947", 1215, eo(prog(t, 0.3, 0.3)) * (1 - out), RED, 60, 520)
        pop_text(c, "6 MONTHS LATER", CX, 390, ANTON, 112, CREAM, prog(t, 0.05, 0.25) * (1 - out))
    if out > 0:
        desert(c, out, t)
        casino_sign(c, CX, 680, 1.0, out, t)
        pop_text(c, "STILL ON THE STRIP TODAY", CX, 400, ANTON, 92, GOLD2, prog(t, W_("end", "still") - 0.2, 0.25), glow=18, glow_rgb=GOLD)

def sc_loopend(c, t, D):
    photo_card(c, PH["bs"], CX, 780, 520, 660, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.35), rot=-1.5, credit=CR_S, dim=0.3)
    pop_text(c, "ALL BECAUSE...", CX, 390, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, vegas=sc_vegas, costs=sc_costs, opening=sc_opening, closed=sc_closed, end=sc_end,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"closed"}
_IMP = [("hook", "$6", -0.2, 0.45), ("vegas", "Flamingo.", -0.3, 0.3), ("costs", "$6", -0.2, 0.4),
        ("opening", "finished.", -0.4, 0.35), ("rehook", "money.", -0.2, 0.35), ("closed", "down.", -0.2, 0.4),
        ("end", "dead.", -0.2, 0.4), ("loopend", "All", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("costs", "$6", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
