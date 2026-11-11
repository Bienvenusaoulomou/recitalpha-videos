import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep40")
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



LEADER1 = CH.Char("lady", dict(skin=(244, 214, 186), body=(60, 90, 150), sleeve=(244, 214, 186), legs=(236, 200, 170), shoe=(40, 40, 60),
                               hat=(0, 0, 0), hair=(220, 196, 140), accent=(214, 168, 75), accent2=(40, 60, 120)))
LEADER2 = CH.Char("lady", dict(skin=(236, 200, 166), body=(36, 36, 44), sleeve=(236, 200, 166), legs=(226, 190, 160), shoe=(30, 30, 30),
                               hat=(0, 0, 0), hair=(200, 160, 100), accent=(214, 168, 75), accent2=(30, 30, 30)))
LEADER3 = CH.CFO
PRES = CH.Char("office", dict(skin=(214, 172, 136), body=(28, 30, 36), sleeve=(26, 28, 34), legs=(22, 24, 30), shoe=(16, 14, 12),
                              hat=(0, 0, 0), hair=(60, 56, 54), accent=(190, 40, 40), accent2=(0, 0, 0)))
EUBLUE = (30, 60, 150)

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0

def eu_flag(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-150, -100, 150, 100), P(C(EUBLUE, a))); c.drawRect(skia.Rect(-150, -100, 150, 100), P(C(INK, a), stroke=6))
    for i in range(12):
        ang = i / 12 * math.tau
        c.drawCircle(60 * math.cos(ang), 60 * math.sin(ang), 9, P(C((255, 214, 0), a)))
    c.restore()

def tn_flag(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-150, -100, 150, 100), P(C((220, 30, 40), a))); c.drawRect(skia.Rect(-150, -100, 150, 100), P(C(INK, a), stroke=6))
    c.drawCircle(0, 0, 55, P(C((255, 255, 255), a)))
    c.drawCircle(4, 0, 42, P(C((220, 30, 40), a))); c.drawCircle(16, 0, 34, P(C((255, 255, 255), a)))
    st = skia.Path()
    for i in range(10):
        r = 20 if i % 2 == 0 else 8; ang = -math.pi / 2 + i * math.pi / 5
        (st.moveTo if i == 0 else st.lineTo)(10 + r * math.cos(ang), r * math.sin(ang))
    st.close(); c.drawPath(st, P(C((220, 30, 40), a)))
    c.restore()

def name_chip(c, x, y, label, a, rgb=CREAM):
    if a <= 0: return
    f = F(BEBAS, 36); w = f.measureText(label) + 30
    c.drawRoundRect(skia.Rect(x - w / 2, y - 30, x + w / 2, y + 12), 10, 10, P(C((20, 18, 14), a * 0.85)))
    text(c, label, x, y, BEBAS, 36, rgb, a, spacing=1)

def money_flow(c, x0, y0, x1, y1, t, a, n=6, back_=False):
    for i in range(n):
        f = (t * 0.7 + i / n) % 1.0
        if back_: f = 1 - f
        euro_note(c, lerp(x0, x1, f), lerp(y0, y1, f) - 110 * math.sin(f * math.pi), 0.35, a * (0.4 + 0.6 * math.sin(f * math.pi)), rot=8 * math.sin(t * 3 + i), value="")

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    eu_flag(c, 230, 860, 0.8, 1.0); tn_flag(c, 850, 860, 0.8, 1.0)
    counter(c, 60000000, CX, 470, 118 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="€", glow=24)
    text(c, "FROM EUROPE TO TUNISIA", CX, 560, BEBAS, 62, CREAM, 1.0, spacing=5)
    if t < b1 - 0.1:
        money_flow(c, 300, 960, 780, 960, t, 1.0)
    else:
        p = eo(prog(t, b1 - 0.1, 0.3))
        money_flow(c, 300, 960, 780, 960, t, p, back_=True)
        ps = prog(t, W_("hook", "back.") - 0.4, 0.22)
        if ps > 0: stamp(c, CX, 690, "SENT BACK", RED, 110, -5, ps, sc=lerp(2.2, 1, eo(ps)))
    text(c, "EU", 230, 1010, ANTON, 60, CREAM, 1.0); text(c, "TUNISIA", 850, 1010, ANTON, 60, CREAM, 1.0)

def sc_deal(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("deal", 1)
    pop_text(c, "TUNIS · JULY 2023", CX, 440, ANTON, 100, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    figs = [(LEADER1, 150, "Ursula", "VON DER LEYEN", 1), (LEADER2, 340, "Giorgia", "MELONI", 1), (LEADER3, 530, "Mark", "RUTTE", 1)]
    for ch, x, w, lab, f in figs:
        p = eo(prog(t, W_("deal", w) - 0.3, 0.3))
        ch.draw(c, x, 1180, 0.62, f, a=p, blink=bl(t, 2.5 + x / 500))
        name_chip(c, x, 1250, lab, p)
    pk = eo(prog(t, W_("deal", "Kais") - 0.3, 0.3))
    PRES.draw(c, 880, 1180, 0.66, -1, a=pk, blink=bl(t))
    name_chip(c, 880, 1250, "PRES. KAIS SAIED", pk)
    eu_flag(c, 160, 560, 0.4, a); tn_flag(c, 920, 560, 0.4, pk)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        paper_doc(c, CX, 640, 0.42, -4, p, "MEMORANDUM", "EU - TUNISIA", "MIGRATION · MONEY", lines=4)

def sc_money(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "ON THE TABLE", CX, 440, ANTON, 110, CREAM, prog(t, 0, 0.25))
    rows = [("€105", 105, "MIGRATION & BORDERS", (90, 120, 170)), ("€150", 150, "BUDGET SUPPORT", (90, 150, 110)), ("€900", 900, "LOANS (UP TO)", RED)]
    for i, (w, v, lab, rgb) in enumerate(rows):
        p = eo(prog(t, W_("money", w) - 0.3, 0.3)); k = eo(prog(t, W_("money", w) - 0.2, 0.9))
        y = 620 + i * 210
        wbar = 700 * v / 900 * k
        if p <= 0: continue
        c.drawRect(skia.Rect(150, y, 150 + max(8, wbar), y + 90), P(C(rgb, p)))
        c.drawRect(skia.Rect(150, y, 150 + max(8, wbar), y + 90), P(C(CREAM, p), stroke=4))
        text(c, "€%dM" % v, 150 + max(8, wbar) + 20, y + 70, ANTON, 64, GOLD2, p, align="l") if v < 900 else text(c, "€900M", 150 + wbar - 20, y + 70, ANTON, 64, CREAM, p, align="r")
        text(c, lab, 150, y - 14, BEBAS, 44, CREAM, p, align="l", spacing=3)

def sc_payment(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("payment", 1)
    calendar(c, 190, 520, 0.6, a, "OCT", "2023")
    pop_text(c, "FIRST PAYMENT", CX + 110, 480, ANTON, 84, CREAM, prog(t, 0.1, 0.25))
    eu_flag(c, 230, 900, 0.6, a); tn_flag(c, 850, 900, 0.6, a)
    money_flow(c, 300, 960, 780, 960, t, a)
    counter(c, 60000000, CX, 700, 104, GOLD2, a, prefix="€", glow=18)
    text(c, "BUDGET SUPPORT", CX, 780, BEBAS, 52, CREAM, a, spacing=5)
    if t > b1 - 0.3:
        p = prog(t, b1 - 0.2, 0.22)
        stamp(c, CX, 1170, "FROM AN OLDER COVID PROGRAM", GOLD2, 54, -3, p, sc=lerp(2, 1, eo(p)))
        text(c, "ACCORDING TO THE EU COMMISSION", CX, 1090, BEBAS, 40, CREAM, eo(p), spacing=3)

def sc_charity(c, t, D):
    a = eo(prog(t, 0, 0.3))
    PRES.draw(c, 270, 1240, 0.95, 1, a=a, blink=bl(t), brow=-0.4, arm_f=(-60, -70))
    name_chip(c, 270, 600, "PRES. KAIS SAIED", a)
    tn_flag(c, 270, 470, 0.5, a)
    pc = eo(prog(t, W_("charity", "cooperation,") - 0.3, 0.3))
    box(c, 720, 640, 520, 120, pc, "\"COOPERATION\"", rgb=(30, 70, 50), lab_rgb=CREAM, size=60)
    text(c, "YES", 720, 760, ANTON, 70, (90, 255, 160), pc)
    pn = eo(prog(t, W_("charity", "charity.") - 0.3, 0.3))
    box(c, 720, 900, 520, 120, pn, "\"CHARITY\"", rgb=(70, 30, 30), lab_rgb=CREAM, size=60)
    text(c, "NO", 720, 1020, ANTON, 70, RED, pn)
    if pn > 0: c.drawLine(480, 960, 960, 840, P(C(RED, pn), stroke=12))
    text(c, "PRESIDENCY STATEMENT, OCT 2023", 720, 1090, BEBAS, 36, CREAM, pn * 0.8, spacing=2)

def sc_refund(c, t, D):
    a = eo(prog(t, 0, 0.3))
    eu_flag(c, 230, 860, 0.8, a); tn_flag(c, 850, 860, 0.8, a)
    text(c, "BRUSSELS", 230, 1010, ANTON, 60, CREAM, a); text(c, "TUNIS", 850, 1010, ANTON, 60, CREAM, a)
    money_flow(c, 300, 960, 780, 960, t, a, back_=True)
    counter(c, 60000000, CX, 470, 112, GOLD2, a, prefix="€", glow=20)
    pr = prog(t, W_("refund", "back") - 0.4, 0.22)
    if pr > 0: stamp(c, CX, 640, "RETURNED", RED, 120, -5, pr, sc=lerp(2.2, 1, eo(pr)))

def sc_loans(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("loans", 1)
    pop_text(c, "THE BIGGEST PART", CX, 440, ANTON, 104, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    counter(c, 900000000, CX, 620, 100, CREAM, a, prefix="€", glow=10)
    text(c, "IN LOANS", CX, 700, BEBAS, 52, CREAM, a, spacing=6)
    pi = eo(prog(t, W_("loans", "IMF,") - 0.3, 0.3))
    box(c, CX, 880, 640, 130, pi, "IMF DEAL · ~$2 BILLION", rgb=(40, 52, 90), size=58)
    arrow(c, CX, 735, CX, 805, pi, pi, GOLD2)
    if t > b1 - 0.3:
        p = prog(t, b1 - 0.2, 0.22)
        stamp(c, CX, 1130, "STUCK FOR MONTHS", RED, 92, -5, p, sc=lerp(2.2, 1, eo(p)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    eu_flag(c, 230, 900, 0.6, a); tn_flag(c, 850, 900, 0.6, a)
    money_flow(c, 300, 960, 780, 960, t, a * 0.8, back_=True)
    text(c, "?", CX, 840, ANTON, 180, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "WAS TUNISIA RIGHT", CX, 430, ANTON, 96, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "TO SEND IT BACK?", CX, 545, ANTON, 104, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, deal=sc_deal, money=sc_money, payment=sc_payment, charity=sc_charity, refund=sc_refund,
              loans=sc_loans, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"refund"}
_IMP = [("hook", "back.", -0.4, 0.45), ("deal", "Kais", -0.3, 0.3), ("money", "€900", -0.3, 0.4), ("rehook", "backfired.", -0.2, 0.4),
        ("payment", "COVID", -0.3, 0.35), ("charity", "charity.", -0.3, 0.4), ("refund", "back", -0.4, 0.45), ("loans", "stuck", -0.3, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "€60", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
