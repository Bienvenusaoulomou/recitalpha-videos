import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep38")
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



AGENT = CH.Char("office", dict(skin=(224, 186, 152), body=(32, 36, 48), sleeve=(30, 34, 46), legs=(26, 30, 40), shoe=(18, 16, 14),
                               hat=(0, 0, 0), hair=(70, 50, 34), accent=(40, 70, 140), accent2=(0, 0, 0)))
PROS = CH.OFFICIAL

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0

def badge(c, x, y, s, a, label="FBI"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, -150); p.lineTo(120, -100); p.lineTo(110, 40); p.cubicTo(90, 110, 40, 140, 0, 160)
    p.cubicTo(-40, 140, -90, 110, -110, 40); p.lineTo(-120, -100); p.close()
    c.drawPath(p, P(C(GOLD, a))); c.drawPath(p, P(C(INK, a), stroke=8))
    c.drawCircle(0, 0, 70, P(C((40, 52, 90), a))); c.drawCircle(0, 0, 70, P(C(GOLD2, a), stroke=6))
    text(c, label, 0, 22, ANTON, 62, CREAM, a)
    c.restore()

def keyicon2(c, x, y, s, a, rot=0, rgb=GOLD2):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawCircle(-60, 0, 38, P(C(rgb, a), stroke=16))
    c.drawRect(skia.Rect(-24, -9, 90, 9), P(C(rgb, a)))
    c.drawRect(skia.Rect(55, 0, 68, 34), P(C(rgb, a))); c.drawRect(skia.Rect(78, 0, 90, 26), P(C(rgb, a)))
    c.restore()

def wallet(c, x, y, s, a, label, rgb=(60, 70, 90), lab_rgb=CREAM):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-130, -80, 130, 80), 18, 18)
    c.drawRRect(r, P(C(rgb, a))); c.drawRRect(r, P(C(INK, a), stroke=6))
    c.drawRoundRect(skia.Rect(60, -30, 150, 30), 12, 12, P(C(GOLD, a)))
    c.drawCircle(100, 0, 10, P(C(INK, a)))
    c.restore()
    text(c, label, x, y + 125 * s, BEBAS, 40, lab_rgb, a, spacing=2)

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    badge(c, 820, 860, 0.9, 1.0)
    AGENT.draw(c, 300, 1240, 0.78, 1, blink=bl(t), look=(1, 0), arm_f=(-80, -40), arm_b=(-20, -30))
    keyicon2(c, 450, 1010 + 10 * math.sin(t * 3), 0.9, 1.0, rot=-0.3)
    text(c, "THE KEYS TO FBI CASE WALLETS", CX, 560, BEBAS, 60, CREAM, 1.0, spacing=4)
    counter(c, 2470000, CX, 470, 120 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="$", glow=24)
    ps = prog(t, W_("hook", "steal") - 0.2, 0.22)
    if ps > 0:
        stamp(c, CX, 665, "STOLEN BY AN AGENT", RED, 80, -5, ps, sc=lerp(2.2, 1, eo(ps)))
        for i in range(6):
            f = ((t * 0.7 + i / 6) % 1.0)
            crypto_coin(c, lerp(760, 340, f), lerp(1020, 1080, f) - 120 * math.sin(f * math.pi), 30, ps * (1 - f * 0.3), t + i)

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("who", 1)
    pop_text(c, "COUNTERINTELLIGENCE", CX, 440, ANTON, 92, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    AGENT.draw(c, 250, 1240, 0.95, 1, a=a, blink=bl(t), arm_f=(-30, -20))
    pb = eo(prog(t, W_("who", "Boston,") - 0.3, 0.3))
    pin(c, 760, 760, 1.0, pb, label="BOSTON")
    pf = prog(t, W_("who", "hostile") - 0.3, 0.25)
    if pf > 0:
        globe(c, 760, 1010, 140, eo(pf), t)
        text(c, "SQUAD: A HOSTILE FOREIGN STATE", CX, 600, BEBAS, 54, CREAM, eo(pf), spacing=3)

def sc_how(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("how", 1)
    inner = screen(c, CX, 760, 760, 440, a, label="FBI SYSTEMS")
    for i in range(4):
        pk = eo(prog(t, 0.3 + i * 0.35, 0.3))
        keyicon2(c, 280 + i * 175, 790, 0.55, a * pk, rot=-0.2 + 0.1 * i)
    text(c, "CRYPTO KEYS FROM FBI CASES", CX, 940, BEBAS, 44, GOLD2, a, spacing=3)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        calendar(c, 230, 520, 0.7, p, "DEC", "2024")
        for i in range(5):
            f = ((t * 0.8 + i / 5) % 1.0)
            crypto_coin(c, lerp(CX, 850, f), lerp(900, 1190, f), 34, p * (1 - f * 0.4), t + i)
        wallet(c, 850, 1170, 0.7, p, "HIS OWN WALLET", rgb=(110, 40, 40))
        AGENT.draw(c, 220, 1250, 0.75, 1, a=p, blink=bl(t), look=(1, 0), arm_f=(-70 + 8 * math.sin(t * 9), -60))

def sc_scale(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("scale", 1)
    k = eo(prog(t, 0.1, 1.3))
    counter(c, 100 * k, CX, 520, 150, GOLD2, a, prefix="~", glow=20)
    text(c, "TRANSFERS", CX, 610, BEBAS, 64, CREAM, a, spacing=8)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        n = int(35 * eo(prog(t, b1 - 0.2, 1.4)))
        for i in range(n):
            col, row = i % 7, i // 7
            paper_doc(c, 190 + col * 117, 720 + row * 92, 0.2, (i % 3 - 1) * 3, p, "FBI", "CASE", "#%d" % (i + 1), lines=3)
        pop_text(c, "35 INVESTIGATIONS", CX, 1255, ANTON, 92, RED, prog(t, W_("scale", "35") - 0.2, 0.25))

def sc_victims(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("victims", 1)
    pop_text(c, "WHOSE WALLETS?", CX, 440, ANTON, 110, CREAM, prog(t, 0, 0.25))
    pw = eo(prog(t, W_("victims", "investigation.") - 0.6, 0.3))
    wallet(c, 280, 690, 0.85, pw, "UNDER INVESTIGATION")
    pf = eo(prog(t, W_("victims", "foreign") - 0.3, 0.3))
    wallet(c, 800, 690, 0.85, pf, "LINKED TO FOREIGN STATES", rgb=(70, 50, 80))
    pi = prog(t, b1 - 0.1, 0.25)
    if pi > 0:
        wallet(c, CX, 1000, 1.0, eo(pi), "CREATED BY THE FBI ITSELF", rgb=(40, 52, 90), lab_rgb=GOLD2)
        badge(c, CX - 30, 1000, 0.32, eo(pi))
        stamp(c, CX, 1190, "AT LEAST ONE", RED, 58, -4, pi, sc=lerp(2, 1, eo(pi)))

def sc_spend(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "WHERE DID IT GO?", CX, 440, ANTON, 104, GOLD2, prog(t, 0, 0.22), glow=18, glow_rgb=GOLD)
    items = [("cards,", "CREDIT CARDS", 560), ("car", "CAR PAYMENTS", 760), ("loans.", "OTHER LOANS", 960)]
    for i, (w, lab, y) in enumerate(items):
        p = eo(prog(t, W_("spend", w) - 0.3, 0.3))
        box(c, CX + 80, y, 560, 130, p, lab, size=64)
        crypto_coin(c, 210, y, 50, p, t + i)
        arrow(c, 270, y, CX - 210, y, p, p, GOLD2)
    text(c, "ACCORDING TO PROSECUTORS", CX, 1150, BEBAS, 48, CREAM, eo(prog(t, W_("spend", "Prosecutors") - 0.2, 0.3)), spacing=4)

def sc_escape(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("escape", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        inner = screen(c, CX, 720, 820, 480, a * o1, label="HIS QUESTION TO CHATGPT")
        q = "IF YOU HAD A BUCKET OF MONEY (AROUND $1 MILLION)..."
        k = eo(prog(t, 0.3, 2.2)); s = q[:int(len(q) * k)]
        l1 = "IF YOU HAD A BUCKET OF"
        text(c, s[:len(l1)], 160, 720, BEBAS, 50, (90, 255, 160), a * o1, align="l")
        text(c, s[len(l1):].strip(), 160, 780, BEBAS, 50, (90, 255, 160), a * o1, align="l")
        text(c, "...LEAVE THE USA FOR AN EU COUNTRY?", 160, 850, BEBAS, 50, (90, 255, 160), a * o1 * eo(prog(t, W_("escape", "leave") - 0.2, 0.3)), align="l")
        text(c, "COURT FILINGS", CX, 1050, BEBAS, 40, CREAM, a * o1 * 0.8, spacing=4)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pop_text(c, "PORTUGAL", CX, 450, ANTON, 140, GOLD2, prog(t, W_("escape", "Portugal") - 0.3, 0.25), glow=20, glow_rgb=GOLD)
        paper_doc(c, 760, 860, 0.8, 4, p, "PROCURAÇÃO", "POWER OF ATTORNEY", "TAX ID", lines=6)
        plane(c, lerp(150, 420, eo(prog(t, b1, 2.0))), 700, 0.8, p, rot=-8)
        AGENT.draw(c, 260, 1240, 0.85, 1, a=p, blink=bl(t))

def sc_confess(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("confess", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        calendar(c, CX, 470, 0.7, a * o1, "JULY", "2026")
        AGENT.draw(c, 300, 1240, 0.95, 1, a=a * o1, blink=bl(t), brow=-0.6, tilt=-6, arm_f=(20, -10))
        CH.CLERK.draw(c, 790, 1240, 0.85, -1, a=a * o1, blink=bl(t, 2.7))
        text(c, "JUSTICE DEPT. EMPLOYEE", 790, 760, BEBAS, 40, CREAM, a * o1, spacing=2)
        pq = eo(prog(t, W_("confess", "very") - 0.3, 0.3))
        if pq > 0:
            box(c, CX, 620, 760, 120, pq * o1, "\"VERY POOR DECISIONS\"", rgb=(60, 30, 30), lab_rgb=GOLD2, size=64)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        bars(c, p)
        AGENT.draw(c, CX, 1240, 0.8, 1, a=p, blink=bl(t), brow=-0.6)
        pa = prog(t, W_("confess", "arrested.") - 0.4, 0.22)
        if pa > 0: stamp(c, CX, 610, "ARRESTED", RED, 110, -6, pa, sc=lerp(2.2, 1, eo(pa)))
        text(c, "2 DAYS LATER", CX, 440, ANTON, 80, CREAM, p)

def sc_plea(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("plea", 1)
    p1 = eo(prog(t, W_("plea", "$1") - 0.3, 0.3)); p2 = eo(prog(t, W_("plea", "November,") - 0.3, 0.6))
    for i, (lab, v, x, rgb, k) in enumerate([("AUGUST", 1.0, 330, (120, 110, 96), p1), ("NOVEMBER", 2.47, 750, RED, p2)]):
        h = 340 * v / 2.47 * k
        if k <= 0: continue
        c.drawRect(skia.Rect(x - 110, 1050 - h, x + 110, 1050), P(C(rgb, a)))
        c.drawRect(skia.Rect(x - 110, 1050 - h, x + 110, 1050), P(C(CREAM, a), stroke=5))
        text(c, "$%.2fM" % v if v < 2 else "$2.47M", x, 1050 - h - 25, ANTON, 70, GOLD2, clamp(k * 3) * a)
        text(c, lab, x, 1105, BEBAS, 46, CREAM, a, spacing=3)
    pop_text(c, "THE TOTAL GREW", CX, 440, ANTON, 104, CREAM, prog(t, 0, 0.25))
    pg = prog(t, W_("plea", "guilty,") - 0.4, 0.22)
    if pg > 0:
        stamp(c, CX, 1215, "PLEADED GUILTY", RED, 76, -4, pg, sc=lerp(2.2, 1, eo(pg)))
    py = eo(prog(t, W_("plea", "20") - 0.2, 0.3))
    text(c, "UP TO 20 YEARS", CX, 560, BEBAS, 62, GOLD2, py, spacing=6)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    AGENT.draw(c, 220, 1110, 0.7, 1, a=a, blink=bl(t))
    keyicon2(c, CX, 900, 1.0, a, rot=-0.2 + 0.1 * math.sin(t * 2))
    PROS.draw(c, 870, 1110, 0.7, -1, a=a, blink=bl(t, 2.6))
    text(c, "?", CX, 790, ANTON, 180, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "WHO SHOULD HOLD", CX, 430, ANTON, 100, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "SEIZED CRYPTO?", CX, 550, ANTON, 110, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, who=sc_who, how=sc_how, scale=sc_scale, victims=sc_victims, spend=sc_spend, escape=sc_escape,
              confess=sc_confess, plea=sc_plea, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"confess"}
_IMP = [("hook", "steal", -0.2, 0.45), ("who", "hostile", -0.3, 0.35), ("how", "himself.", -0.3, 0.35),
        ("scale", "35", -0.2, 0.4), ("rehook", "criminals'.", -0.2, 0.4), ("victims", "itself.", -0.3, 0.4),
        ("spend", "loans.", -0.3, 0.3), ("escape", "Portugal", -0.3, 0.35), ("confess", "arrested.", -0.4, 0.45),
        ("plea", "guilty,", -0.4, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "steal", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
