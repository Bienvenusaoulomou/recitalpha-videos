import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep32")
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
    building(c, 760, 1180, 0.55, 1.0, "FRENCH BANK", cols=4)
    for i in range(6):
        f = ((t * 0.6 + i / 6) % 1.0)
        euro_note(c, lerp(740, 330, f), lerp(990, 900, f) - 140 * math.sin(f * math.pi), 0.45, 1.0 - f * 0.3, rot=f * 200 - 100)
    CH.HACKER.draw(c, 220, 1230, 0.85, 1, look=(1, 0), arm_f=(-70 + 10 * math.sin(t * 9), -60), arm_b=(-40, -50))
    laptop(c, 340, 1150, 0.55, 1.0, t)
    counter(c, 100000000, CX, 470, 140 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="~€", glow=24)
    text(c, "STOLEN BY HACKERS", CX, 560, BEBAS, 64, CREAM, 1.0, spacing=6)
    po = prog(t, b1 - 0.05, 0.22)
    if po > 0: stamp(c, CX, 680, "CUSTOMERS LOST: €0", (90, 220, 140), 84, -5, po, sc=lerp(2.2, 1, eo(po)))

def sc_reveal(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pill(c, "NOVEMBER 2026", 420, a, CREAM, 64, 420)
    building(c, CX, 1150, 0.62, a, "CRÉDIT MUTUEL ARKÉA", cols=5)
    k = eo(prog(t, W_("reveal", "6") - 0.3, 0.8))
    if k > 0:
        counter(c, 5800000 * k, CX, 590, 110, GOLD2, a, prefix="~", glow=18)
        text(c, "CUSTOMERS", CX, 660, BEBAS, 56, CREAM, a * k, spacing=6)
    pc = prog(t, W_("reveal", "cyberattack.") - 0.4, 0.22)
    if pc > 0: stamp(c, CX, 820, "CYBERATTACK", RED, 120, -5, pc, sc=lerp(2.2, 1, eo(pc)))

def sc_how(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("how", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        CH.CLERK.draw(c, 300, 1220, 0.95, 1, a=a * o1, blink=bl(t))
        CH.LADY.draw(c, 760, 1220, 0.95, -1, a=a * o1, blink=bl(t, 2.7))
        shield(c, CX, 720, 0.8, a * o1, "CUSTOMER ACCOUNTS")
        pop_text(c, "NOT TOUCHED", CX, 430, ANTON, 110, (90, 220, 140), prog(t, W_("how", "touch") - 0.2, 0.25) * o1)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 470, 640, 120, p, "THE BANK'S OWN ACCOUNT", rgb=(90, 30, 30), size=60)
        kp = eo(prog(t, W_("how", "outside") - 0.3, 0.4))
        arrow(c, CX, 540, CX, 640, kp, p)
        box(c, CX, 720, 560, 110, max(kp, 0.35 * p), "OUTSIDE SERVICE PROVIDER", size=52)
        ko = eo(prog(t, W_("how", "other") - 0.3, 0.5))
        for i, xx in enumerate((220, CX, 860)):
            arrow(c, CX, 790, xx, 900, ko, p, RED)
            building(c, xx, 1180, 0.32, ko, "BANK", cols=3)
        if ko > 0:
            for i in range(5):
                f = (t * 0.8 + i / 5) % 1.0; xx = (220, CX, 860)[i % 3]
                euro_note(c, lerp(CX, xx, f), lerp(790, 980, f), 0.3, ko * (1 - f * 0.5), rot=f * 90)

def sc_crypto(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "EUROS", 260, 440, ANTON, 96, CREAM, prog(t, 0, 0.25))
    arrow(c, 420, 420, 620, 420, eo(prog(t, 0.3, 0.4)), a)
    pop_text(c, "CRYPTO", 820, 440, ANTON, 96, GOLD2, prog(t, W_("crypto", "converted") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    ks = eo(prog(t, W_("crypto", "spread") - 0.3, 0.8))
    xs = (180, 420, 660, 900)
    for i, xx in enumerate(xs):
        box(c, xx, 1030, 210, 110, ks, "EXCHANGE", size=40)
    for i in range(10):
        f = clamp(ks * 1.2 - i * 0.02); tx = xs[i % 4]
        x0, y0 = CX, 680
        crypto_coin(c, lerp(x0, tx, f), lerp(y0, 960, f) - 120 * math.sin(f * math.pi), 34, a, t + i)
    crypto_coin(c, CX, 680, 90 * (1 - ks * 0.5), a * (1 - ks * 0.6), t)
    ph = prog(t, W_("crypto", "harder") - 0.3, 0.22)
    if ph > 0: stamp(c, CX, 1185, "HARD TO FOLLOW", RED, 70, -4, ph, sc=lerp(2, 1, eo(ph)))

def sc_alarm(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("alarm", 1)
    CH.EMPLOYEE.draw(c, 260, 1230, 1.0, 1, a=a, blink=bl(t), arm_f=(-70 + 6 * math.sin(t * 9), -60), arm_b=(-40, -50))
    laptop(c, 420, 1160, 0.6, a, t, label="ON-CHAIN")
    pop_text(c, "FIRST ALARM:", CX, 420, BEBAS, 96, CREAM, prog(t, 0, 0.25))
    pz = prog(t, W_("alarm", "ZachXBT.") - 0.4, 0.22)
    if pz > 0:
        stamp(c, 680, 570, "ZachXBT", GOLD2, 110, -4, pz, sc=lerp(2.2, 1, eo(pz)))
        text(c, "ONLINE BLOCKCHAIN INVESTIGATOR", 680, 680, BEBAS, 44, CREAM, pz, spacing=2)
    if t > b1 - 0.3:
        p1 = eo(prog(t, b1 - 0.3, 0.3)); p2 = eo(prog(t, W_("alarm", "bank", 0) - 0.2, 0.3))
        calendar(c, 720, 800, 0.5, p1, "2", "NOV")
        text(c, "ALARM", 720, 930, BEBAS, 44, CREAM, p1, spacing=4)
        calendar(c, 900, 800, 0.5, p2, "4", "NOV")
        text(c, "BANK", 900, 930, BEBAS, 44, CREAM, p2, spacing=4)
        pd = prog(t, W_("alarm", "confirmed") - 0.2, 0.22)
        if pd > 0: stamp(c, 810, 1040, "+2 DAYS", RED, 70, -6, pd, sc=lerp(2, 1, eo(pd)))

def sc_estimate(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("estimate", 1)
    pop_text(c, "HIS ESTIMATE", CX, 430, ANTON, 100, CREAM, prog(t, 0, 0.25))
    k = eo(prog(t, W_("estimate", "climbed") - 0.2, 1.4))
    v = lerp(106000000, 133000000, k)
    counter(c, v, CX, 640, 140, RED, a, prefix="~$", glow=18)
    bh = lerp(200, 330, k)
    c.drawRect(skia.Rect(CX - 90, 1250 - bh, CX + 90, 1250), P(C(RED, a * 0.85)))
    c.drawRect(skia.Rect(CX - 90, 1250 - bh, CX + 90, 1250), P(C(CREAM, a), stroke=5))
    pn = prog(t, W_("estimate", "never") - 0.2, 0.22)
    if pn > 0: stamp(c, CX, 790, "BANK: NO EXACT NUMBER", CREAM, 70, -5, pn, sc=lerp(2, 1, eo(pn)))

def sc_frozen(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("frozen", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        for i in range(4):
            crypto_coin(c, 330 + i * 140, 760 + 30 * math.sin(i), 50, a * o1, 0.2 + i * 0.3)
        kf = eo(prog(t, W_("frozen", "frozen.") - 0.4, 0.4))
        ice_block(c, CX, 770, 680, 240, kf * o1)
        snowflake(c, 260, 560, 70, kf * o1, rot=t * 0.5); snowflake(c, 830, 600, 50, kf * o1, rot=-t * 0.6)
        pf = prog(t, W_("frozen", "frozen.") - 0.3, 0.22)
        if pf > 0: stamp(c, CX, 470, "PART FROZEN", (170, 220, 255), 110, -5, pf * o1, sc=lerp(2.2, 1, eo(pf)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pill(c, "PARIS PROSECUTORS", 440, p, GOLD2, 70, 640)
        pop_text(c, "INVESTIGATION OPEN", CX, 590, ANTON, 86, CREAM, prog(t, W_("frozen", "investigation") - 0.2, 0.25))
        CH.CLERK.draw(c, 300, 1230, 0.95, 1, a=p, blink=bl(t), arm_f=(-40, -40))
        kr = eo(prog(t, W_("frozen", "rest") - 0.4, 0.8))
        for i in range(3):
            crypto_coin(c, lerp(900, 480, kr) + i * 40, 900 - i * 40, 40, p * kr, t + i)
        pop_text(c, "THE REST?", 760, 1150, ANTON, 80, GOLD2, prog(t, W_("frozen", "rest") - 0.2, 0.25))

def sc_safe(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pill(c, "CUSTOMER MONEY", 540, a, GOLD2, 66, 520)
    shield(c, CX, 790, 0.85, a, "SAFE")
    CH.CLERK.draw(c, 150, 1240, 0.75, 1, a=a, blink=bl(t))
    CH.LADY.draw(c, 930, 1240, 0.75, -1, a=a, blink=bl(t, 2.6))
    pop_text(c, "THE BANK SAYS:", CX, 420, BEBAS, 90, CREAM, prog(t, 0, 0.25))
    pg = prog(t, W_("safe", "threaten") - 0.3, 0.22)
    if pg > 0: stamp(c, CX, 1170, "GROUP NOT THREATENED", GOLD2, 64, -4, pg, sc=lerp(2, 1, eo(pg)))

def sc_war(c, t, D):
    a = eo(prog(t, 0, 0.3))
    CH.HACKER.draw(c, 250, 1230, 0.95, 1, a=a, arm_f=(-70 + 8 * math.sin(t * 10), -60), arm_b=(-40, -50))
    laptop(c, 390, 1160, 0.55, a, t)
    pop_text(c, "THE NEW BANK ROBBERY", CX, 420, ANTON, 96, GOLD2, prog(t, 0.0, 0.25), glow=20, glow_rgb=GOLD)
    for i, (w, lab) in enumerate([("masks.", "NO MASKS."), ("vault.", "NO VAULT.")]):
        pop_text(c, lab, 680, 600 + i * 120, ANTON, 90, RED, prog(t, W_("war", w) - 0.3, 0.25))
    pm = prog(t, W_("war", "account.") - 0.4, 0.22)
    if pm > 0: stamp(c, 680, 880, "ONE ACCOUNT", GREEN, 86, -5, pm, sc=lerp(2.2, 1, eo(pm)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    building(c, 300, 1060, 0.42, a, "BANK", cols=3)
    for k in range(3):
        rr = 60 + ((t * 120 + k * 60) % 180)
        c.drawCircle(780, 860, rr, P(C(RED, a * (1 - rr / 240)), stroke=6))
    text(c, "!", 780, 900, ANTON, 140, RED, a)
    pop_text(c, "WARN THE PUBLIC", CX, 430, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "THE MOMENT THEY'RE HACKED?", CX, 550, ANTON, 76, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, reveal=sc_reveal, how=sc_how, crypto=sc_crypto, alarm=sc_alarm, estimate=sc_estimate,
              frozen=sc_frozen, safe=sc_safe, war=sc_war, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"estimate"}
_IMP = [("hook", "cent.", -0.2, 0.45), ("reveal", "cyberattack.", -0.4, 0.45), ("how", "own", -0.3, 0.35),
        ("rehook", "crypto.", -0.2, 0.35), ("crypto", "harder", -0.3, 0.35), ("alarm", "ZachXBT.", -0.4, 0.4),
        ("estimate", "never", -0.2, 0.35), ("frozen", "frozen.", -0.3, 0.4), ("war", "account.", -0.4, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("estimate", "$133", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
