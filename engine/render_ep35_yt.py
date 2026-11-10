import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep35")
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

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    building(c, 770, 1180, 0.55, 1.0, "CRYPTO EXCHANGE", cols=4)
    for i in range(7):
        f = ((t * 0.8 + i / 7) % 1.0)
        crypto_coin(c, lerp(760, 300, f), lerp(980, 900, f) - 130 * math.sin(f * math.pi), 30, 1.0 - f * 0.3, t + i)
    CH.HACKER.draw(c, 220, 1230, 0.9, 1, look=(1, 0), arm_f=(-70 + 10 * math.sin(t * 9), -60), arm_b=(-40, -50))
    laptop(c, 340, 1155, 0.55, 1.0, t)
    counter(c, 6300000000, CX, 470, 112 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="~$", glow=24)
    text(c, "TAKEN FROM ONE EXCHANGE", CX, 560, BEBAS, 62, CREAM, 1.0, spacing=5)
    po = prog(t, b1 - 0.05, 0.22)
    if po > 0:
        stamp(c, CX, 690, "IN ~20 MINUTES", RED, 110, -5, po, sc=lerp(2.2, 1, eo(po)))
        clock(c, 900, 820, 70, po, t_h=(t * 3) % 12)

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("who", 1)
    pop_text(c, "BINANCE", CX, 450, ANTON, 150, GOLD2, prog(t, W_("who", "Binance.") - 0.3, 0.25), glow=22, glow_rgb=GOLD)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pill(c, "BIGGEST CRYPTO HEIST EVER", 580, p, CREAM, 56, 760)
        kb = eo(prog(t, W_("who", "Bybit") - 0.3, 0.6)); kn = eo(prog(t, b1, 0.9))
        for i, (lab, v, x, rgb, k) in enumerate([("BYBIT 2025", 1.5, 330, (120, 110, 96), kb), ("BINANCE 2026", 6.3, 750, RED, kn)]):
            h = 420 * v / 6.3 * k
            c.drawRect(skia.Rect(x - 110, 1170 - h, x + 110, 1170), P(C(rgb, p)))
            c.drawRect(skia.Rect(x - 110, 1170 - h, x + 110, 1170), P(C(CREAM, p), stroke=5))
            text(c, "$%.1fB" % v, x, 1170 - h - 25, ANTON, 72, GOLD2, p * clamp(k * 3))
            text(c, lab, x, 1225, BEBAS, 46, CREAM, p, spacing=3)
    else:
        building(c, CX, 1180, 0.6, a, "BINANCE", cols=5)

def sc_blame(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "BLOCKCHAIN ANALYSTS", CX, 430, ANTON, 90, CREAM, prog(t, 0, 0.25))
    for i, (w, lab, x) in enumerate([("TRM", "TRM LABS", 300), ("Chainalysis,", "CHAINALYSIS", 780)]):
        p = eo(prog(t, W_("blame", w) - 0.3, 0.3))
        laptop(c, x, 900, 0.75, p, t + i, label=None)
        pill(c, lab, 960, p, GOLD2, 52, 360) if False else text(c, lab, x, 990, BEBAS, 56, GOLD2, p, spacing=3)
    pk = prog(t, W_("blame", "Korea.") - 0.4, 0.22)
    if pk > 0:
        stamp(c, CX, 600, "LINKED TO NORTH KOREA", RED, 92, -5, pk, sc=lerp(2.2, 1, eo(pk)))
        CH.HACKER.draw(c, CX, 1260, 0.75, 1, a=eo(pk), arm_f=(10, -20))

def sc_how(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("how", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        pop_text(c, "STEP 1?", CX, 430, ANTON, 110, CREAM, prog(t, 0, 0.25) * o1)
        CH.EMPLOYEE.draw(c, 260, 1230, 1.0, 1, a=a * o1, blink=bl(t), arm_f=(-70 + 6 * math.sin(t * 9), -60), arm_b=(-40, -50))
        laptop(c, 430, 1160, 0.6, a * o1, t, label="ENGINEER")
        ph = prog(t, W_("how", "hacked") - 0.3, 0.22)
        if ph > 0:
            stamp(c, 720, 700, "HACKED LAPTOP", RED, 84, -5, ph * o1, sc=lerp(2.2, 1, eo(ph)))
            text(c, "BINANCE'S FIRST ACCOUNT", 720, 800, BEBAS, 44, CREAM, ph * o1, spacing=2)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pop_text(c, "MORE COMPLEX", CX, 430, ANTON, 110, GOLD2, p, glow=18, glow_rgb=GOLD)
        laptop(c, CX, 820, 0.7, p, t, label="ENGINEER")
        ko = eo(prog(t, W_("how", "other") - 0.3, 0.6))
        for i, (xx, yy) in enumerate([(220, 1060), (860, 1060), (CX, 1220)]):
            arrow(c, xx, yy - 40, CX, 860, ko, p, RED)
            box(c, xx, yy, 300, 90, ko * p, "POINT OF BREACH", rgb=(90, 30, 30), size=40)

def sc_freeze(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("freeze", 1)
    pop_text(c, "THE RACE", CX, 430, ANTON, 120, CREAM, prog(t, 0, 0.25))
    for i, (w, lab, x) in enumerate([("Tether", "TETHER", 300), ("Circle", "CIRCLE", 780)]):
        p = eo(prog(t, W_("freeze", w) - 0.3, 0.3))
        box(c, x, 600, 330, 110, p, lab, size=60)
    for i in range(6):
        crypto_coin(c, 220 + i * 128, 880 + 30 * math.sin(i * 1.7), 48, a, 0.3 + i * 0.4)
    kf = eo(prog(t, W_("freeze", "froze") - 0.3, 0.4))
    ice_block(c, CX, 880, 860, 230, kf)
    snowflake(c, 160, 740, 50, kf, rot=t * 0.5); snowflake(c, 930, 760, 40, kf, rot=-t * 0.6)
    if t > b1 - 0.3:
        k = eo(prog(t, b1 - 0.2, 1.0))
        counter(c, 3000000000 * k, CX, 1150, 120, (170, 220, 255), eo(prog(t, b1 - 0.3, 0.3)), prefix="~$", glow=18)
        text(c, "FROZEN", CX, 1230, BEBAS, 60, CREAM, eo(prog(t, b1, 0.3)), spacing=8)

def sc_missing(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "STILL OUT THERE", CX, 430, ANTON, 104, CREAM, prog(t, 0, 0.25))
    counter(c, 3000000000, CX, 640, 118, RED, a, prefix="~$", glow=20)
    for i in range(8):
        f = (t * 0.35 + i / 8) % 1.0
        crypto_coin(c, 200 + (i * 137) % 700, lerp(1250, 760, f), 36, a * (1 - f), t + i)
    text(c, "?", CX, 1100, ANTON, 260, GOLD2, a * (0.6 + 0.4 * math.sin(t * 4)))

def sc_pay(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("pay", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        pw = prog(t, W_("pay", "withdrawals,") - 0.4, 0.22)
        if pw > 0: stamp(c, CX, 440, "WITHDRAWALS PAUSED", RED, 90, -4, pw * o1, sc=lerp(2.2, 1, eo(pw)))
        shield(c, CX, 800, 0.8, eo(prog(t, W_("pay", "cover") - 0.3, 0.3)) * o1, "USERS COVERED")
        CH.CLERK.draw(c, 220, 1240, 0.85, 1, a=a * o1, blink=bl(t))
        CH.LADY.draw(c, 860, 1240, 0.85, -1, a=a * o1, blink=bl(t, 2.7))
        text(c, "BINANCE'S PROMISE", CX, 1060, BEBAS, 50, CREAM, eo(prog(t, W_("pay", "cover") - 0.3, 0.3)) * o1, spacing=4)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3)); k = eo(prog(t, b1, 1.2))
        crypto_coin(c, CX, 560, 110, p, t)
        pts = [(140, 760), (300, 820), (460, 790), (620, 950), (780, 1010), (940, 1160)]
        route(c, [(x, y - 60) for x, y in pts], k, p, RED)
        pop_text(c, "6-WEEK LOW", CX, 1200, ANTON, 96, RED, prog(t, W_("pay", "low.") - 0.4, 0.25))

def sc_why(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "WHY IT MATTERS", CX, 430, ANTON, 104, GOLD2, prog(t, 0.0, 0.22), glow=20, glow_rgb=GOLD)
    pill(c, "A UN PANEL:", 580, eo(prog(t, W_("why", "UN") - 0.2, 0.3)), CREAM, 60, 400)
    for i in range(4): crypto_coin(c, 200 + (i % 2) * 120, 740 + i * 80, 34, a, t + i)
    pm = eo(prog(t, W_("why", "nuclear") - 0.5, 0.5))
    missile(c, CX + 300, 1000 - 60 * pm, 0.7, pm)
    pf = prog(t, W_("why", "fund") - 0.2, 0.22)
    if pf > 0: stamp(c, CX - 60, 1150, "FUNDS NUCLEAR PROGRAM", RED, 70, -4, pf, sc=lerp(2, 1, eo(pf)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    CH.CLERK.draw(c, 200, 1110, 0.7, 1, a=a, blink=bl(t))
    building(c, CX, 1040, 0.42, a, "EXCHANGE", cols=3)
    CH.EMPLOYEE.draw(c, 880, 1110, 0.7, -1, a=a, blink=bl(t, 2.6))
    text(c, "?", CX, 780, ANTON, 200, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "ROBBED EXCHANGE:", CX, 430, ANTON, 96, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "WHO SHOULD PAY?", CX, 550, ANTON, 110, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

def missile(c, x, y, s, a, rgb=(200, 200, 196)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(0, -300); body.cubicTo(40, -240, 44, -180, 44, -120); body.lineTo(44, 200); body.lineTo(-44, 200); body.lineTo(-44, -120); body.cubicTo(-44, -180, -40, -240, 0, -300); body.close()
    c.drawPath(body, P(C(rgb, a))); c.drawPath(body, P(C(INK, a), stroke=6))
    for sx in (-1, 1):
        fin = skia.Path(); fin.moveTo(sx * 44, 90); fin.lineTo(sx * 110, 200); fin.lineTo(sx * 44, 200); fin.close()
        c.drawPath(fin, P(C(RED, a))); c.drawPath(fin, P(C(INK, a), stroke=5))
    c.drawRect(skia.Rect(-44, -60, 44, -30), P(C(RED, a)))
    c.restore()

E.DRAW = dict(hook=sc_hook, who=sc_who, blame=sc_blame, how=sc_how, freeze=sc_freeze, missing=sc_missing, pay=sc_pay,
              why=sc_why, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"missing"}
_IMP = [("hook", "minutes.", -0.3, 0.45), ("who", "$1.5", -0.3, 0.35), ("blame", "Korea.", -0.4, 0.45),
        ("rehook", "laptop.", -0.2, 0.4), ("how", "hacked", -0.3, 0.35), ("freeze", "froze", -0.3, 0.35),
        ("missing", "$3", -0.3, 0.35), ("pay", "low.", -0.4, 0.35), ("why", "nuclear", -0.3, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("freeze", "$3", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
