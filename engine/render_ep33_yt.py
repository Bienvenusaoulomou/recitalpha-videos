import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep33")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
from kit3 import *
from kit4 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999
def B(sid, i):
    try: return beat(sid, i)
    except Exception: return 999
import chars as CH

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0

def car(c, x, y, s, a, rgb=(160, 30, 40)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(-200, -30); body.lineTo(-180, -80); body.lineTo(-80, -90); body.lineTo(-30, -140)
    body.lineTo(90, -140); body.lineTo(150, -85); body.lineTo(200, -70); body.lineTo(205, -30); body.close()
    c.drawPath(body, P(C(rgb, a))); c.drawPath(body, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-20, -128, 80, -92), P(C((150, 190, 220), a * 0.8)))
    for wx in (-120, 120):
        c.drawCircle(wx, -28, 38, P(C(INK, a))); c.drawCircle(wx, -28, 18, P(C((180, 180, 186), a)))
    c.restore()

def crowd(c, x0, x1, y, a, n=9, seed=4, r=26):
    rng = random.Random(seed)
    for i in range(n):
        xx = lerp(x0, x1, i / max(1, n - 1)) + rng.uniform(-10, 10)
        person(c, xx, y + rng.uniform(-10, 10), r, (rng.randint(90, 200), rng.randint(80, 160), rng.randint(70, 140)), a)

def sc_hook(c, t, D):
    b1 = B("hook", 1); q = 1 - eo(prog(t, b1 - 0.3, 0.3))
    mansion(c, CX, 1060, 0.85, 1.0, t)
    if q > 0:
        text(c, "PARIS MANSION", CX, 450, ANTON, 120, GOLD2, q, glow=22, glow_rgb=GOLD)
        stamp(c, CX, 600, "SEIZED BY FRANCE", RED, 90, -4, q, sc=lerp(1.3, 1, eo(prog(t, 0, 0.35))))
    for i, (w, lab, xx, yy) in enumerate([("nightclub,", "NIGHTCLUB", 250, 760), ("cinema", "CINEMA", 830, 760), ("Turkish", "TURKISH BATH", CX, 1140)]):
        p = prog(t, W_("hook", w) - 0.25, 0.25)
        if p * q > 0: tag(c, xx, yy, lab, p * q, -5 + i * 5, (40, 90, 160))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        c.drawRect(skia.Rect(0, 330, W, 1290), P(C(INK, 0.55 * p)))
        CH.OFFICIAL.draw(c, CX, 1240, 1.0, 1, a=p, blink=bl(t), arm_f=(10, -20))
        pop_text(c, "THE OWNER:", CX, 450, BEBAS, 90, CREAM, p)
        pv = prog(t, W_("hook", "president") - 0.3, 0.22)
        if pv > 0: stamp(c, CX, 600, "A VICE PRESIDENT", GOLD2, 96, -4, pv, sc=lerp(2.2, 1, eo(pv)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    id_card(c, CX, 720, 0.95, -3, a, "TEODORO NGUEMA OBIANG MANGUE", "VICE PRESIDENT", tag_="EQUATORIAL GUINEA")
    pop_text(c, "WHO IS HE?", CX, 430, ANTON, 104, CREAM, prog(t, 0, 0.25))
    ps = prog(t, W_("who", "2016.") - 0.4, 0.22)
    if ps > 0: stamp(c, CX, 1060, "SINCE 2016", GOLD2, 100, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("verdict", 1)
    pill(c, "FRENCH COURT · 2017", 430, a, GOLD2, 66, 600)
    scales(c, CX, 960, 1.0, a, tilt=math.sin(t * 1.5) * 0.4 + (1 if t > b1 else 0) * 0.6)
    pc = prog(t, W_("verdict", "convicted") - 0.2, 0.22)
    if pc > 0 and t < b1: stamp(c, CX, 600, "CONVICTED", RED, 120, -5, pc, sc=lerp(2.2, 1, eo(pc)))
    if t < b1:
        pop_text(c, "LAUNDERING EMBEZZLED", CX, 1190, ANTON, 64, CREAM, prog(t, W_("verdict", "laundering") - 0.2, 0.25))
    if t > b1 - 0.2:
        pop_text(c, "3 YEARS IN PRISON", CX, 590, ANTON, 104, CREAM, prog(t, b1 - 0.1, 0.25))
        psu = prog(t, W_("verdict", "Suspended.") - 0.35, 0.22)
        if psu > 0: stamp(c, CX, 740, "SUSPENDED", GOLD2, 110, -6, psu, sc=lerp(2.2, 1, eo(psu)))

def sc_total(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("total", 1)
    pop_text(c, "CONFISCATED", CX, 430, ANTON, 110, CREAM, prog(t, 0, 0.25))
    k = eo(prog(t, W_("total", "150") - 0.3, 1.0))
    if k > 0: counter(c, 150000000 * k, CX, 600, 130, GOLD2, a, prefix="~€", glow=24)
    pm = eo(prog(t, W_("total", "mansion.") - 0.3, 0.3))
    mansion(c, 300, 1150, 0.42, pm, t)
    pc = eo(prog(t, W_("total", "cars.") - 0.4, 0.3))
    for i in range(3): car(c, 800 + (i - 1) * 40, 900 + i * 110, 0.75, pc, [(160, 30, 40), (30, 30, 34), (220, 200, 60)][i])
    pa = prog(t, W_("total", "more.") - 0.3, 0.22)
    if pa > 0: stamp(c, 300, 790, "AND MORE", CREAM, 70, -4, pa, sc=lerp(2, 1, eo(pa)))

def sc_glove(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pill(c, "UK SANCTIONS · 2021", 430, a, CREAM, 66, 600)
    glove(c, 300, 900, 1.05, a, t, rot=-12)
    pa = prog(t, W_("glove", "accusing") - 0.2, 0.22)
    if pa > 0: tag(c, 760, 600, "ACCUSED", pa, -6, RED)
    k = eo(prog(t, W_("glove", "$275,000") - 0.3, 0.9))
    if k > 0: counter(c, 275000 * k, 760, 780, 110, GOLD2, a, glow=20)
    pp = eo(prog(t, W_("glove", "public") - 0.3, 0.3))
    text(c, "MISAPPROPRIATED", 760, 880, BEBAS, 56, CREAM, pp, spacing=3)
    text(c, "PUBLIC MONEY", 760, 940, BEBAS, 56, CREAM, pp, spacing=3)
    pj = prog(t, W_("glove", "Jackson's") - 0.3, 0.22)
    if pj > 0: stamp(c, 760, 1110, "ONE JEWELLED GLOVE", GOLD2, 60, -5, pj, sc=lerp(2, 1, eo(pj)), sub="ONCE MICHAEL JACKSON'S")

def sc_final(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("final", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        scales(c, CX, 1000, 0.9, a * o1, tilt=0.8)
        pop_text(c, "LAST APPEAL", CX, 440, ANTON, 110, CREAM, prog(t, 0, 0.25) * o1)
        pr = prog(t, W_("final", "failed") - 0.2, 0.22)
        if pr > 0: stamp(c, CX, 620, "REJECTED · 2021", RED, 100, -5, pr * o1, sc=lerp(2.2, 1, eo(pr)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pill(c, "NEW FRENCH LAW", 440, p, GOLD2, 70, 520)
        kf = eo(prog(t, W_("final", "back") - 0.4, 0.9))
        for i in range(5):
            euro_note(c, lerp(CX, 200 + i * 170, kf), lerp(640, 960, kf), 0.45, p, rot=(i - 2) * 12)
        crowd(c, 160, 920, 1150, p * kf, n=9)
        pop_text(c, "BACK TO THE PEOPLE", CX, 640, ANTON, 92, CREAM, prog(t, W_("final", "people") - 0.3, 0.25) * (1 - kf * 0) )

def sc_fight(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("fight", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        mansion(c, CX, 1150, 0.6, a * o1, t)
        pop_text(c, "E. GUINEA'S GOVERNMENT:", CX, 440, BEBAS, 84, CREAM, prog(t, 0, 0.25) * o1)
        pb = prog(t, W_("fight", "back.") - 0.4, 0.22)
        if pb > 0: stamp(c, CX, 610, "GIVE IT BACK", GOLD2, 120, -5, pb * o1, sc=lerp(2.2, 1, eo(pb)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        building(c, CX, 1220, 0.42, p, "UN TOP COURT", cols=4)
        pill(c, "ITS REPRESENTATIVE CALLED FRANCE'S APPROACH:", 440, p, CREAM, 46, 980)
        pq = max(prog(t, b1 + 0.2, 0.25), prog(t, W_("fight", "paternalistic") - 0.3, 0.25))
        pop_text(c, "“PATERNALISTIC", CX, 630, PLAY, 84, GOLD2, pq, glow=16, glow_rgb=GOLD)
        pn = prog(t, W_("fight", "neo-colonial.\"") - 0.4, 0.25)
        if pn <= 0: pn = prog(t, W_("fight", "even") - 0.2, 0.25)
        pop_text(c, "AND EVEN NEO-COLONIAL”", CX, 760, PLAY, 62, GOLD2, pn, glow=16, glow_rgb=GOLD)

def sc_icj(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("icj", 1)
    building(c, CX, 1200, 0.5, a, "UN TOP COURT", cols=4)
    pill(c, "2025", 430, a, GOLD2, 70, 260)
    pr = prog(t, W_("icj", "refused") - 0.2, 0.22)
    if pr > 0: stamp(c, CX, 600, "REQUEST REFUSED", RED, 104, -5, pr, sc=lerp(2.2, 1, eo(pr)), sub="NO ORDER TO HAND IT BACK")
    po = prog(t, b1 - 0.1, 0.25)
    pop_text(c, "THE CASE ISN'T OVER", CX, 820, ANTON, 92, CREAM, po)

def sc_poor(c, t, D):
    a = eo(prog(t, 0, 0.3))
    derrick(c, 300, 1150, 0.95, a, t, rgb=(150, 132, 104))
    pop_text(c, "OIL & GAS WEALTH", CX, 430, ANTON, 100, GOLD2, prog(t, W_("poor", "oil") - 0.3, 0.25), glow=18, glow_rgb=GOLD)
    kp = eo(prog(t, W_("poor", "population") - 0.3, 0.4))
    crowd(c, 560, 980, 1170, kp, n=6, r=30)
    pv = prog(t, W_("poor", "poverty.") - 0.4, 0.22)
    if pv > 0:
        stamp(c, 760, 760, "POVERTY", RED, 110, -5, pv, sc=lerp(2.2, 1, eo(pv)))
        text(c, "MUCH OF THE POPULATION", 760, 900, BEBAS, 50, CREAM, pv, spacing=3)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    mansion(c, CX, 1010, 0.55, a, t)
    pop_text(c, "GIVE IT BACK?", CX, 430, ANTON, 110, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "OR SELL IT FOR THE PEOPLE?", CX, 560, ANTON, 80, GOLD2, prog(t, W_("question", "sell") - 0.2, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, who=sc_who, verdict=sc_verdict, total=sc_total, glove=sc_glove, final=sc_final,
              fight=sc_fight, icj=sc_icj, poor=sc_poor, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"verdict"}
_IMP = [("hook", "president", -0.3, 0.45), ("who", "2016.", -0.4, 0.4), ("verdict", "Suspended.", -0.35, 0.45),
        ("total", "150", -0.3, 0.35), ("rehook", "glove.", -0.2, 0.4), ("glove", "Jackson's", -0.3, 0.4),
        ("final", "failed", -0.2, 0.35), ("fight", "paternalistic", -0.3, 0.35), ("icj", "refused", -0.2, 0.4), ("poor", "poverty.", -0.4, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("total", "150", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
