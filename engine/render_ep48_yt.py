import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep48")
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
from kit4 import *
import chars as CH

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0
def name_chip(c, x, y, label, a, rgb=CREAM, size=36):
    if a <= 0: return
    f = F(BEBAS, size); w = f.measureText(label) + 30
    c.drawRoundRect(skia.Rect(x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.35), 10, 10, P(C((20, 18, 14), a * 0.85)))
    text(c, label, x, y, BEBAS, size, rgb, a, spacing=1)
def talk(t, k=1.0): return k * max(0.0, math.sin(t * 13)) * 0.8
def house(c, x, y, s, a, rgb=(150, 120, 90), roof=(120, 50, 40)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-110, -150, 110, 0), P(C(rgb, a))); c.drawRect(skia.Rect(-110, -150, 110, 0), P(C(INK, a), stroke=6))
    p = skia.Path(); p.moveTo(-140, -150); p.lineTo(0, -260); p.lineTo(140, -150); p.close()
    c.drawPath(p, P(C(roof, a))); c.drawPath(p, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-25, -80, 25, 0), P(C(INK, a)))
    for dx in (-70, 70): c.drawRect(skia.Rect(dx - 22, -120, dx + 22, -80), P(C((250, 220, 140), a)))
    c.restore()

GREEN_NG = (0, 135, 81)
JUDGE = CH.CLERK     # stylised Justice Robin Knowles

def flag_ng(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-6, -10, 6, 330), P(C((120, 110, 96), a)))
    wv = 8 * math.sin(t * 3)
    for i, rgb in enumerate((GREEN_NG, (245, 245, 240), GREEN_NG)):
        c.drawRect(skia.Rect(6 + i * 70, 0 + wv * (i / 3), 76 + i * 70, 140 + wv * (i / 3)), P(C(rgb, a)))
    c.drawRect(skia.Rect(6, 0, 216, 140), P(C(INK, a), stroke=5))
    c.restore()

def gas_plant(c, x, y, s, a, ghost=0.0, t=0):
    """gas processing plant; ghost=1 -> dashed outline only"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    if ghost > 0.5:
        pp = P(C(CREAM, a * 0.6), stroke=6); pp.setPathEffect(skia.DashPathEffect.Make([24, 18], t * 30 % 42))
    for (x0, y0, x1, y1) in ((-380, -260, -200, 0), (-160, -380, -60, 0), (-20, -200, 180, 0), (220, -300, 380, 0)):
        r = skia.Rect(x0, y0, x1, y1)
        if ghost > 0.5: c.drawRect(r, pp)
        else:
            c.drawRect(r, P(C((120, 116, 108), a))); c.drawRect(r, P(C(INK, a), stroke=6))
    if ghost > 0.5: c.drawLine(-400, 0, 400, 0, pp)
    else:
        for k in range(3): c.drawCircle(-110 + k * 10, -420 - k * 60 - (t * 40 % 60), 30 + k * 10, P(C((200, 196, 186), a * 0.4)))
    c.restore()

def growth_bars(c, x0, y0, w, h, k, a):
    n = 8
    for i in range(n):
        v = (1.07 ** (i * 1.3)) / (1.07 ** ((n - 1) * 1.3))
        hh = h * (0.6 + 0.4 * v) * clamp(k * n - i)
        if hh <= 0: continue
        bx = x0 + i * w / n
        c.drawRect(skia.Rect(bx + 8, y0 + h - hh, bx + w / n - 8, y0 + h), P(C(GOLD2 if i == n - 1 else (150, 120, 60), a)))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    text(c, "NIGERIA WAS ORDERED TO PAY", CX, 440, BEBAS, 62, CREAM, 1.0, spacing=3)
    text(c, "$11 BILLION+", CX, 590, ANTON, 150 * lerp(1.1, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, glow=24, glow_rgb=GOLD)
    gas_plant(c, CX, 1180, 1.0, 1.0, ghost=1.0, t=t)
    text(c, "A GAS PLANT", CX, 720, ANTON, 70, CREAM, eo(prog(t, b1 - 0.2, 0.3)))
    ps = prog(t, W_("hook", "never") - 0.1, 0.22)
    if ps > 0: stamp(c, CX, 960, "NEVER BUILT", RED, 110, -6, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_deal(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("deal", 1)
    calendar(c, 200, 560, 0.55, a, "2010", "DEAL")
    pop_text(c, "20-YEAR GAS DEAL", CX + 130, 440, ANTON, 84, CREAM, prog(t, 0.1, 0.25))
    flag_ng(c, 120, 900, 0.6, a, t)
    paper_doc(c, 420, 980, 0.42, -3, a, "GAS SUPPLY", "AND PROCESSING", "AGREEMENT", lines=4)
    pp = eo(prog(t, W_("deal", "P&ID") - 0.2, 0.3))
    box(c, 840, 600, 260, 110, pp, "P&ID", rgb=(60, 46, 34), lab_rgb=GOLD2, size=70)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "BRITISH VIRGIN ISLANDS", 840, 700, BEBAS, 42, GOLD, p, spacing=2)
        CH.CONMAN.draw(c, 700, 1250, 0.7, 1, a=p, blink=bl(t))
        CH.EMPLOYEE.draw(c, 920, 1250, 0.7, -1, a=p, blink=bl(t + 1))
        name_chip(c, 810, 780, "2 IRISH FOUNDERS (STYLISED)", p, size=32)

def sc_award(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("award", 1); b2 = B("award", 2)
    if t < b1 - 0.2:
        gas_plant(c, CX, 1200, 0.8, a, ghost=1.0, t=t)
        ps = prog(t, W_("award", "collapsed") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 520, "DEAL COLLAPSED", RED, 90, -5, ps, sc=lerp(2.2, 1, eo(ps)))
        pl = eo(prog(t, W_("award", "London") - 0.3, 0.3))
        building(c, CX, 960, 0.6 * lerp(1.3, 1, pl), pl, "ARBITRATION · LONDON", cols=4)
    elif t < b2 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        text(c, "2017 AWARD", CX, 450, BEBAS, 72, GOLD, p, spacing=6)
        counter(c, int(6.6e9 * eo(prog(t, b1, 0.9))), CX, 620, 130, GOLD2, p, prefix="$", glow=22)
        text(c, "FOR \"LOST PROFITS\"", CX, 720, ANTON, 70, CREAM, eo(prog(t, W_("award", "profits") - 0.2, 0.3)))
        for i in range(7): bills(c, 140 + i * 135, 950 + 18 * math.sin(t * 2 + i), p, 3, rot=(i - 3) * 6)
    else:
        p = eo(prog(t, b2 - 0.2, 0.3)); k = eo(prog(t, b2, 2.6))
        text(c, "+7% INTEREST / YEAR", CX, 450, ANTON, 80, CREAM, p)
        growth_bars(c, 140, 780, 800, 440, k, p)
        counter(c, int(lerp(6.6e9, 11e9, k)), CX, 640, 120, RED if k > 0.95 else GOLD2, p, prefix="$", glow=18)

def sc_ruling(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("ruling", 1)
    if t < b1 - 0.2:
        text(c, "OCTOBER 2023 · LONDON", CX, 440, BEBAS, 66, GOLD, a, spacing=4)
        JUDGE.draw(c, 270, 1250, 1.0, 1, a=a, blink=bl(t), arm_f=(-60, -40))
        name_chip(c, 270, 640, "JUSTICE ROBIN KNOWLES (STYLISED)", a, rgb=GOLD2, size=32)
        scales(c, 740, 1060, 0.8, a, tilt=lerp(0, -0.8, eo(prog(t, W_("ruling", "Nigeria") - 0.2, 0.6))))
        pf = eo(prog(t, W_("ruling", "Nigeria") - 0.2, 0.3))
        flag_ng(c, 640, 600, 0.5, pf, t)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        pop_text(c, "THE JUDGE FOUND:", CX, 450, ANTON, 84, CREAM, prog(t, b1 - 0.2, 0.25))
        box(c, 250, 880, 300, 100, p, "P&ID", rgb=(60, 46, 34), lab_rgb=GOLD2, size=60)
        CH.OFFICIAL.draw(c, 820, 1250, 0.85, -1, a=p, blink=bl(t), look=(-1, 0), arm_f=(40, -60))
        name_chip(c, 820, 700, "OIL MINISTRY OFFICIAL (STYLISED)", p, size=30)
        for i in range(4):
            f = ((t - b1) * 0.6 + i / 4) % 1.0
            bills(c, lerp(330, 700, f), 900 - 80 * math.sin(f * math.pi), p * (1 - f * 0.3), 1, rot=f * 200)
        ps = prog(t, W_("ruling", "bribes") - 0.1, 0.22)
        if ps > 0: stamp(c, 450, 1130, "BRIBES", RED, 110, -6, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_docs(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("docs", 1)
    if t < b1 - 0.2:
        for i in range(3):
            paper_doc(c, 320 + i * 220, 860 + i * 20, 0.45, -8 + i * 8, a, "FEDERAL REPUBLIC", "LEGAL STRATEGY", "PRIVILEGED", lines=6)
        ps = prog(t, W_("docs", "confidential") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 860, "CONFIDENTIAL", RED, 100, -8, ps, sc=lerp(2.2, 1, eo(ps)))
        pop_text(c, "NIGERIA'S OWN LEGAL PAPERS", CX, 460, ANTON, 72, CREAM, prog(t, 0.1, 0.25))
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        counter(c, 11000000000, CX, 760, 140, (150, 140, 120), p, prefix="$")
        c.drawLine(80, 720, 1000, 720, P(C(RED, p), stroke=14))
        ps = prog(t, W_("docs", "overturned") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 980, "OVERTURNED", RED, 120, -6, ps, sc=lerp(2.2, 1, eo(ps)))
        flag_ng(c, 120, 400, 0.5, p, t)

def sc_quote(c, t, D):
    a = eo(prog(t, 0, 0.3))
    JUDGE.draw(c, 220, 1250, 0.8, 1, a=a, blink=bl(t), arm_f=(-40, -50))
    for i, ln in enumerate(["\"WHAT SOME", "INDIVIDUALS", "WILL DO", "FOR MONEY.\""]):
        text(c, ln, 640, 520 + i * 120, ANTON, 104, GOLD2 if i == 3 else CREAM, eo(prog(t, 0.3 + i * 0.5, 0.3)))
    name_chip(c, 640, 1060, "JUSTICE ROBIN KNOWLES, VIA OCCRP", a, rgb=GOLD2, size=34)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    gas_plant(c, CX, 1180, 0.7, a, ghost=1.0, t=t)
    for i in range(5): bills(c, 220 + i * 160, 860 + 16 * math.sin(t * 2 + i), a, 2, rot=(i - 2) * 9)
    text(c, "?", CX, 1100, ANTON, 170, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "PAY FOR A DEAL", CX, 430, ANTON, 100, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "WON WITH BRIBES?", CX, 545, ANTON, 104, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 690)

E.DRAW = dict(hook=sc_hook, deal=sc_deal, award=sc_award, ruling=sc_ruling, docs=sc_docs, quote=sc_quote,
              question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"docs"}
_IMP = [("hook", "never", -0.1, 0.45), ("award", "collapsed", -0.1, 0.4), ("ruling", "bribes", -0.1, 0.4),
        ("docs", "overturned", -0.1, 0.45), ("rehook", "agreed", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$11", 0.0), ("award", "$6.6", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
