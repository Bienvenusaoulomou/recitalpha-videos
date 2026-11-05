import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep31")
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
import chars as CH

GREEN = (90, 255, 160)

def laptop(c, x, y, s, a, t=0, label=None, glow=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-170, -230, 170, 0), 14, 14, P(C((40, 42, 48), a)))
    c.drawRect(skia.Rect(-152, -212, 152, -18), P(C((8, 14, 12), a)))
    rng = random.Random(3)
    for i in range(9):
        w = rng.uniform(60, 260); off = (t * 40 + i * 21) % 190
        c.drawRect(skia.Rect(-140, -200 + off, -140 + w, -194 + off), P(C(GREEN, a * 0.6 * glow)))
    if label: text(c, label, 0, -100, ANTON, 44, GREEN, a * glow)
    c.drawRoundRect(skia.Rect(-210, 0, 210, 26), 10, 10, P(C((70, 72, 80), a)))
    c.restore()

def missile(c, x, y, s, a, rgb=(200, 200, 196)):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(0, -300); body.cubicTo(40, -240, 44, -180, 44, -120); body.lineTo(44, 200); body.lineTo(-44, 200); body.lineTo(-44, -120); body.cubicTo(-44, -180, -40, -240, 0, -300); body.close()
    c.drawPath(body, P(C(rgb, a))); c.drawPath(body, P(C(INK, a), stroke=6))
    for sx in (-1, 1):
        fin = skia.Path(); fin.moveTo(sx * 44, 90); fin.lineTo(sx * 110, 200); fin.lineTo(sx * 44, 200); fin.close()
        c.drawPath(fin, P(C(RED, a))); c.drawPath(fin, P(C(INK, a), stroke=5))
    c.drawRect(skia.Rect(-44, -60, 44, -30), P(C(RED, a)))
    c.restore()

def pie(c, x, y, r, frac, a, rgb=RED):
    c.drawCircle(x, y, r, P(C((60, 56, 48), a)))
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, 360 * frac, False); p.close()
    c.drawPath(p, P(C(rgb, a))); c.drawCircle(x, y, r, P(C(CREAM, a), stroke=5))

def keyicon(c, x, y, s, a, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawCircle(-60, 0, 46, P(C(GOLD2, a), stroke=22))
    c.drawRect(skia.Rect(-16, -11, 120, 11), P(C(GOLD2, a)))
    for k in (70, 100): c.drawRect(skia.Rect(k, 0, k + 14, 34), P(C(GOLD2, a)))
    c.restore()

def crypto_coin(c, x, y, r, a, t=0):
    sq = abs(math.cos(t * 3 + x * 0.01))
    c.save(); c.translate(x, y); c.scale(max(0.15, sq), 1)
    c.drawCircle(0, 0, r, P(C(GOLD2, a))); c.drawCircle(0, 0, r * 0.8, P(C(GOLD, a), stroke=r * 0.12))
    text(c, "B", 0, r * 0.36, ANTON, r * 1.05, INK, a)
    c.restore()

def coin_rain(c, t, a, n=14, seed=2):
    rng = random.Random(seed)
    for i in range(n):
        x = rng.uniform(80, W - 80); sp = rng.uniform(260, 420); y = 330 + ((t * sp + rng.uniform(0, 900)) % 910)
        crypto_coin(c, x, y, rng.uniform(22, 38), a * 0.8, t + i)

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    building(c, 760, 1180, 0.55, 1.0, "CRYPTO EXCHANGE", cols=4)
    for i in range(6):
        f = ((t * 0.7 + i / 6) % 1.0)
        crypto_coin(c, lerp(760, 300, f), lerp(980, 900, f) - 120 * math.sin(f * math.pi), 30, 1.0 - f * 0.3, t + i)
    CH.HACKER.draw(c, 230, 1220, 1.0, 1, blink=0, look=(1, 0), arm_f=(-70 + 10 * math.sin(t * 9), -60), arm_b=(-40, -50))
    laptop(c, 350, 1150, 0.55, 1.0, t)
    counter(c, 1500000000, CX, 470, 140 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="$", glow=24)
    text(c, "STOLEN · FEBRUARY 2025", CX, 560, BEBAS, 60, CREAM, 1.0, spacing=6)
    po = prog(t, b1 - 0.05, 0.22)
    if po > 0: stamp(c, CX, 760, "IN ONE ATTACK", RED, 120, -6, po, sc=lerp(2.2, 1, eo(po)))

def sc_reveal(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("reveal", 1)
    pill(c, "THE FBI:", 420, a, CREAM, 64, 340)
    pg = prog(t, W_("reveal", "gang.") - 0.3, 0.22)
    if pg > 0 and t < b1: stamp(c, CX, 590, "NOT A GANG", CREAM, 120, -5, pg, sc=lerp(2.2, 1, eo(pg)))
    if t > b1 - 0.2:
        pop_text(c, "A COUNTRY:", CX, 510, BEBAS, 100, CREAM, prog(t, b1, 0.25))
        pk = prog(t, W_("reveal", "Korea.") - 0.35, 0.22)
        if pk > 0: stamp(c, CX, 650, "NORTH KOREA", RED, 150, -5, pk, sc=lerp(2.3, 1, eo(pk)))
    CH.HACKER.draw(c, CX, 1250, 0.9, 1, blink=0, arm_f=(10, -20))

def sc_scale(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("scale", 1)
    pop_text(c, "IN 2025 ALONE", CX, 420, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    k = eo(prog(t, W_("scale", "$2") - 0.3, 1.0))
    if k > 0: counter(c, 2000000000 * k, CX, 580, 130, GOLD2, a, prefix="~$", glow=22)
    pk = eo(prog(t, b1 - 0.2, 1.0))
    if t > b1 - 0.3:
        pie(c, CX, 880, 210, 0.6 * pk, eo(prog(t, b1 - 0.3, 0.3)))
        text(c, "~60%", CX, 905, ANTON, 96, CREAM, eo(prog(t, b1 + 0.5, 0.3)))
        pill(c, "OF ALL CRYPTO STOLEN WORLDWIDE", 1190, eo(prog(t, W_("scale", "world.") - 0.5, 0.3)), CREAM, 54, 880)

def sc_why(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "WHY?", CX, 430, ANTON, 140, GOLD2, prog(t, 0.0, 0.22), glow=20, glow_rgb=GOLD)
    pm = eo(prog(t, W_("why", "nuclear") - 0.5, 0.5))
    missile(c, CX + 220, 1180 - 60 * pm, 0.9, pm)
    pill(c, "UN PANEL", 600, eo(prog(t, W_("why", "UN") - 0.2, 0.3)), CREAM, 60, 300)
    for i in range(5): crypto_coin(c, 200 + (i % 2) * 120, 760 + i * 80, 32, a, t + i)
    pf = prog(t, W_("why", "fund") - 0.2, 0.22)
    if pf > 0: stamp(c, CX - 120, 1220, "→ NUCLEAR PROGRAM", RED, 74, -4, pf, sc=lerp(2, 1, eo(pf)))

def sc_method(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("method", 1)
    swap = eo(prog(t, b1 - 0.2, 0.5))
    talk = 0.5 + 0.5 * math.sin(t * 16) if t < b1 - 0.3 else 0
    if swap < 1: CH.RECRUITER.draw(c, 290, 1220, 1.05, 1, a=a * (1 - swap), mouth=talk * 0.7, blink=1.0 if (t % 3.1) < 0.12 else 0, arm_f=(-50 + 15 * math.sin(t * 4), -60))
    if swap > 0: CH.HACKER.draw(c, 290, 1220, 1.05, 1, a=swap, arm_f=(-80, -70))
    CH.EMPLOYEE.draw(c, 800, 1220, 1.05, -1, a=a, blink=1.0 if (t % 2.7) < 0.12 else 0, brow=0.4 * swap, mouth=0.0)
    tag(c, 290, 540, "\"RECRUITER\"" if swap < 0.5 else "HACKER", a, -5, (40, 90, 160) if swap < 0.5 else RED)
    pop_text(c, "REMOTE IT JOB?", 790, 430, ANTON, 80, CREAM, prog(t, W_("method", "remote") - 0.2, 0.25) * (1 - swap))
    if t > b1:
        f = eo(prog(t, W_("method", "keys") - 0.3, 0.8))
        keyicon(c, lerp(760, 360, f), lerp(780, 760, f) - 120 * math.sin(f * math.pi), 0.9, eo(prog(t, b1, 0.3)), rot=-20 + 40 * f)
        pop_text(c, "THE WALLET KEYS", CX, 430, ANTON, 104, GOLD2, prog(t, W_("method", "keys") - 0.2, 0.25), glow=18, glow_rgb=GOLD)

def sc_total(c, t, D):
    a = eo(prog(t, 0, 0.3))
    coin_rain(c, t, a)
    pop_text(c, "SINCE RECORDS BEGAN", CX, 440, ANTON, 96, CREAM, prog(t, 0.0, 0.25))
    k = eo(prog(t, W_("total", "$6.75") - 0.4, 1.0))
    if k > 0: counter(c, 6750000000 * k, CX, 780, 130, GOLD2, a, prefix="~$", glow=26)

def sc_now(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("now", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        calendar(c, CX, 560, 0.6, a * (1 - out), "APR 2026", "")
        pop_text(c, "IT HASN'T STOPPED", CX, 420, ANTON, 100, CREAM, prog(t, 0.0, 0.25) * (1 - out))
        k = eo(prog(t, W_("now", "$300") - 0.3, 0.9))
        if k > 0: counter(c, 300000000 * k, CX, 860, 130, RED, a * (1 - out), prefix="~$", glow=18)
        pill(c, "KELPDAO", 1010, eo(prog(t, W_("now", "KelpDAO.") - 0.4, 0.3)) * (1 - out), GOLD2, 70, 420)
    if out > 0:
        CH.HACKER.draw(c, CX, 1240, 0.95, 1, a=out, arm_f=(-40, -60))
        pop_text(c, "EARLY SIGNS:", CX, 420, BEBAS, 90, CREAM, out)
        pl = prog(t, W_("now", "Lazarus") - 0.3, 0.22)
        if pl > 0: stamp(c, CX, 560, "LAZARUS GROUP", RED, 120, -5, pl, sc=lerp(2.2, 1, eo(pl)))

def sc_war(c, t, D):
    a = eo(prog(t, 0, 0.3))
    CH.HACKER.draw(c, 260, 1230, 0.95, 1, a=a, arm_f=(-70 + 8 * math.sin(t * 10), -60), arm_b=(-40, -50))
    laptop(c, 400, 1160, 0.55, a, t)
    pop_text(c, "THE NEW WAR", CX, 420, ANTON, 120, GOLD2, prog(t, 0.0, 0.25), glow=20, glow_rgb=GOLD)
    for i, (w, lab) in enumerate([("soldiers.", "NO SOLDIERS."), ("borders.", "NO BORDERS."), ("code,", "JUST CODE.")]):
        pop_text(c, lab, 660, 600 + i * 120, ANTON, 84, RED if i < 2 else GREEN, prog(t, W_("war", w) - 0.3, 0.25))
    pm = prog(t, W_("war", "money.") - 0.2, 0.22)
    if pm > 0: stamp(c, 660, 980, "...AND MONEY", GOLD2, 90, -5, pm, sc=lerp(2.2, 1, eo(pm)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    building(c, 280, 1050, 0.45, a, "BANK", cols=3)
    crypto_coin(c, 800, 900, 120, a, t)
    text(c, "VS", CX, 920, ANTON, 110, CREAM, a)
    pop_text(c, "PROTECT CRYPTO", CX, 430, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "LIKE BANKS?", CX, 550, ANTON, 120, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    if "comments." in [x["w"].lower() for x in E.WORDS if x["scene"] == "question"] or True:
        follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, reveal=sc_reveal, scale=sc_scale, why=sc_why, method=sc_method, total=sc_total, now=sc_now,
              war=sc_war, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"why"}
_IMP = [("hook", "attack.", -0.2, 0.45), ("reveal", "Korea.", -0.35, 0.45), ("scale", "$2", -0.3, 0.35),
        ("why", "nuclear", -0.3, 0.4), ("rehook", "interview.", -0.2, 0.35), ("method", "keys", -0.3, 0.35),
        ("total", "$6.75", -0.4, 0.35), ("now", "Lazarus", -0.3, 0.4), ("war", "money.", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("total", "$6.75", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
