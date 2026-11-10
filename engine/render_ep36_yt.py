import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep36")
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

def order(c, x, y, s, a, rot=0, amt="$20,000,000", fake=True, typo=False, tp=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-230, -120, 230, 120), 12, 12)
    c.drawRRect(r, P(C((236, 230, 214), a))); c.drawRRect(r, P(C(INK, a), stroke=5))
    text(c, "PAYMENT ORDER", 0, -70, BEBAS, 44, INK, a, spacing=4)
    text(c, amt, 0, 0, ANTON, 60, (40, 90, 60), a)
    if typo:
        text(c, "TO: SHALIKA FANDATION", 0, 70, BEBAS, 42, INK, a, spacing=2)
        if tp > 0:
            c.drawOval(skia.Rect(5, 28, 215, 92), P(C(RED, a * tp), stroke=7))
    else:
        for i in range(3): c.drawLine(-170, 50 + i * 20, 170 - i * 60, 50 + i * 20, P(C((150, 140, 120), a), stroke=5))
    c.restore()

def printer(c, x, y, s, a, t=0, broken=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-200, -60, 200, 120), 18, 18, P(C((200, 200, 196), a)))
    c.drawRoundRect(skia.Rect(-200, -60, 200, 120), 18, 18, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-140, -160, 140, -60), P(C((236, 230, 214), a))); c.drawRect(skia.Rect(-140, -160, 140, -60), P(C(INK, a), stroke=5))
    k = (t * 0.6) % 1.0 if broken < 0.5 else 0.15
    c.drawRect(skia.Rect(-120, 100, 120, 100 + 160 * k), P(C((244, 240, 230), a)))
    for i in range(int(6 * k)): c.drawLine(-90, 120 + i * 24, 90, 120 + i * 24, P(C((150, 140, 120), a), stroke=4))
    c.drawCircle(150, 20, 16, P(C(RED if broken > 0.5 else (90, 220, 140), a)))
    c.restore()

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    building(c, CX, 1180, 0.6, 1.0, "CENTRAL BANK", cols=5)
    counter(c, 951000000, CX, 470, 120 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="~$", glow=24)
    text(c, "THEY TRIED TO STEAL", CX, 560, BEBAS, 64, CREAM, 1.0, spacing=6)
    CH.HACKER.draw(c, 200, 1240, 0.75, 1, look=(1, 0), arm_f=(-70 + 10 * math.sin(t * 9), -60))
    for i in range(5):
        f = (t * 0.7 + i / 5) % 1.0
        bills(c, lerp(CX, 200, f), lerp(950, 900, f) - 100 * math.sin(f * math.pi), 1.0 - f * 0.4, 1, rot=f * 120)
    po = prog(t, b1 - 0.05, 0.22)
    if po > 0: stamp(c, CX, 700, "GOT AWAY WITH $81M", RED, 92, -5, po, sc=lerp(2.2, 1, eo(po)))

def sc_where(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("where", 1)
    calendar(c, 300, 760, 0.75, eo(prog(t, 0, 0.3)), "2016", "FEBRUARY")
    building(c, 760, 960, 0.48, eo(prog(t, W_("where", "central") - 0.3, 0.3)), "BANGLADESH BANK", cols=4)
    pop_text(c, "BANGLADESH", CX, 440, ANTON, 120, GOLD2, prog(t, W_("where", "Bangladesh.") - 0.3, 0.25), glow=20, glow_rgb=GOLD)
    pw = prog(t, b1 - 0.1, 0.22)
    if pw > 0: stamp(c, CX, 1130, "OVER A WEEKEND", RED, 90, -4, pw, sc=lerp(2.2, 1, eo(pw)))

def sc_orders(c, t, D):
    a = eo(prog(t, 0, 0.3)); D_ = SCN_D("orders")
    building(c, 830, 1170, 0.42, a, "NEW YORK FED", cols=3)
    building(c, 240, 1170, 0.36, a, "BANGLADESH", cols=3)
    pop_text(c, "~3 DOZEN FAKE ORDERS", CX, 440, ANTON, 92, CREAM, prog(t, W_("orders", "three") - 0.3, 0.25))
    n = int(clamp(prog(t, 0.3, D_ - 1.0)) * 35)
    for i in range(min(n, 12)):
        f = ((t * 0.9 + i / 12) % 1.0)
        order(c, lerp(260, 820, f), 800 - 160 * math.sin(f * math.pi) + (i % 3) * 30, 0.4, a * (1 - abs(f - 0.5) * 0.6), rot=-10 + f * 20, amt="$$$")
    text(c, str(max(1, n)), CX, 1060, ANTON, 120, GOLD2, a * clamp(n), glow=18, glow_rgb=GOLD)

def SCN_D(sid):
    s = [x for x in E.SCENES if x["id"] == sid][0]; return s["end"] - s["start"]

def sc_printer(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("printer", 1)
    br = prog(t, W_("printer", "messed") - 0.2, 0.3)
    pop_text(c, "THE PRINTER", CX, 440, ANTON, 120, CREAM, prog(t, 0, 0.25))
    printer(c, CX, 860, 1.25, a, t, broken=br)
    if br > 0: stamp(c, CX, 600, "MALWARE", RED, 110, -6, br, sc=lerp(2.2, 1, eo(br)))
    pr = prog(t, W_("printer", "transfer") - 0.3, 0.25)
    if pr > 0: pill(c, "TRANSFER RECORDS: HIDDEN", 1200, pr, GOLD2, 56, 760)

def sc_typo(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("typo", 1)
    pill(c, "SRI LANKA", 440, a, CREAM, 64, 380)
    tp = eo(prog(t, W_("typo", "fandation\".") - 0.4, 0.4))
    order(c, CX, 720, 1.4, a, rot=-3, amt="$20,000,000", typo=True, tp=tp)
    if tp > 0:
        pop_text(c, "FOUNDATION?", CX, 1000, ANTON, 96, GOLD2, tp, glow=16, glow_rgb=GOLD)
        text(c, "(REPORTEDLY)", CX, 1060, BEBAS, 46, CREAM, tp, spacing=4)
    ps = prog(t, W_("typo", "stopped.") - 0.4, 0.22)
    if ps > 0: stamp(c, CX, 1190, "STOPPED", RED, 130, -6, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_blocked(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("blocked", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        pop_text(c, "MOST ORDERS:", CX, 440, ANTON, 100, CREAM, prog(t, 0, 0.25) * o1)
        for i in range(6):
            order(c, 260 + (i % 3) * 280, 740 + (i // 3) * 270, 0.5, a * o1, rot=-6 + i * 3, amt="$$$")
        pb = prog(t, W_("blocked", "blocked") - 0.3, 0.22)
        if pb > 0: stamp(c, CX, 870, "BLOCKED", RED, 150, -6, pb * o1, sc=lerp(2.2, 1, eo(pb)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3)); k = eo(prog(t, W_("blocked", "$81") - 0.3, 0.9))
        counter(c, 81000000 * k, CX, 560, 130, GOLD2, p, glow=22)
        pop_text(c, "GOT THROUGH", CX, 650, BEBAS, 70, CREAM, p)
        pl = prog(t, W_("blocked", "Philippines.") - 0.4, 0.25)
        if pl > 0:
            pill(c, "ACCOUNTS IN THE PHILIPPINES", 800, pl, CREAM, 56, 820)
            for i in range(5):
                f = (t * 0.6 + i / 5) % 1.0
                bills(c, lerp(160, 920, f), 1050 - 120 * math.sin(f * math.pi), pl * (1 - f * 0.3), 1, rot=f * 60)

def sc_casino(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("casino", 1)
    casino_sign(c, CX, 600, 1.0, a, t, label="CASINO", lights=1.0)
    for i in range(7):
        f = (t * 0.5 + i / 7) % 1.0
        bills(c, 200 + (i * 113) % 700, lerp(1150, 760, f), a * (1 - f), 1, rot=i * 30 + f * 90)
    pv = prog(t, W_("casino", "vanished") - 0.3, 0.22)
    if pv > 0: stamp(c, CX, 860, "VANISHED", RED, 120, -5, pv * (1 - eo(prog(t, b1 - 0.2, 0.2))), sc=lerp(2.2, 1, eo(pv)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pie_(c, CX, 960, 120, 0.17 * eo(prog(t, b1, 0.8)), p)
        pop_text(c, "RECOVERED: A SMALL PART", CX, 1210, ANTON, 72, CREAM, prog(t, W_("casino", "recovered.") - 0.4, 0.25))

def pie_(c, x, y, r, frac, a, rgb=(90, 220, 140)):
    c.drawCircle(x, y, r, P(C(RED, a)))
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, 360 * frac, False); p.close()
    c.drawPath(p, P(C(rgb, a))); c.drawCircle(x, y, r, P(C(CREAM, a), stroke=5))

def sc_charge(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("charge", 1)
    pill(c, "2018 · US JUSTICE DEPARTMENT", 440, a, CREAM, 56, 760)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        paper_doc(c, CX, 860, 0.8, -3, a * o1, "United States of America", "CRIMINAL COMPLAINT", "PARK JIN HYOK", lines=6)
        pc = prog(t, W_("charge", "charged") - 0.3, 0.22)
        if pc > 0: stamp(c, CX, 1080, "CHARGED", RED, 120, -6, pc * o1, sc=lerp(2.2, 1, eo(pc)))
        text(c, "NORTH KOREAN PROGRAMMER", CX, 1220, BEBAS, 54, GOLD2, eo(prog(t, W_("charge", "North") - 0.3, 0.3)) * o1, spacing=3)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        for i, x in enumerate((240, CX, 840)):
            CH.HACKER.draw(c, x, 1230 - (i == 1) * 20, 0.8, 1 if i < 2 else -1, a=p, arm_f=(10, -20))
        pg = prog(t, W_("charge", "government-backed") - 0.3, 0.25)
        if pg > 0: pop_text(c, "GOVERNMENT-BACKED TEAM", CX, 590, ANTON, 76, CREAM, pg)
        pl = prog(t, W_("charge", "Lazarus") - 0.3, 0.22)
        if pl > 0: stamp(c, CX, 720, "LAZARUS GROUP", RED, 120, -5, pl, sc=lerp(2.2, 1, eo(pl)))

def sc_same(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "THE SAME TEAM?", CX, 440, ANTON, 110, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    text(c, "ACCORDING TO THE US", CX, 520, BEBAS, 50, CREAM, a, spacing=4)
    for i, (w, lab, sub, y) in enumerate([("Sony", "SONY PICTURES HACK", "2014", 700), ("WannaCry", "WANNACRY ATTACK", "2017", 900), ("Bangladesh", "BANGLADESH BANK", "2016", 1100)]):
        p = eo(prog(t, W_("same", w) - 0.3, 0.3)) if i < 2 else eo(prog(t, 0.2, 0.3))
        box(c, CX, y, 700, 130, p, lab + "  ·  " + sub, rgb=(90, 30, 30) if i < 2 else (44, 50, 62), size=62)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "WHO PAYS", CX, 430, ANTON, 120, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "BANGLADESH BACK?", CX, 550, ANTON, 104, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    for i, (w, lab, x) in enumerate([("bank,", "THE BANK", 200), ("Fed,", "NY FED", CX), ("casinos?", "CASINOS", 880)]):
        p = eo(prog(t, W_("question", w) - 0.3, 0.3))
        building(c, x, 980, 0.3, p, lab, cols=3)
        text(c, lab, x, 1050, BEBAS, 54, CREAM, p, spacing=3)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, where=sc_where, orders=sc_orders, printer=sc_printer, typo=sc_typo, blocked=sc_blocked,
              casino=sc_casino, charge=sc_charge, same=sc_same, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"casino"}
_IMP = [("hook", "$81", -0.3, 0.45), ("where", "weekend.", -0.3, 0.35), ("orders", "fake", -0.3, 0.35),
        ("printer", "messed", -0.2, 0.4), ("rehook", "mistake.", -0.2, 0.45), ("typo", "stopped.", -0.4, 0.45),
        ("blocked", "$81", -0.3, 0.35), ("casino", "vanished", -0.3, 0.4), ("charge", "Lazarus", -0.3, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("blocked", "$81", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
