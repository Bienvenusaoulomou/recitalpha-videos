import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep37")
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

AFR = [(-0.30, -0.95), (0.05, -1.0), (0.30, -0.88), (0.42, -0.62), (0.70, -0.40), (0.95, -0.38), (0.62, 0.05), (0.50, 0.30),
       (0.30, 0.62), (0.12, 0.98), (-0.05, 0.95), (-0.15, 0.55), (-0.22, 0.20), (-0.30, -0.05), (-0.62, -0.10), (-0.92, -0.30),
       (-0.95, -0.55), (-0.70, -0.85)]
def africa(c, x, y, r, a, rgb=(70, 64, 50), ol=GOLD2):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x + AFR[0][0] * r, y + AFR[0][1] * r)
    for px, py in AFR[1:]: p.lineTo(x + px * r, y + py * r)
    p.close(); c.drawPath(p, P(C(rgb, a))); c.drawPath(p, P(C(ol, a), stroke=6))

def leak(c, x, y, r, t, a, n=8, ang0=-40, spread=80):
    for i in range(n):
        f = (t * 0.5 + i / n) % 1.0
        ang = math.radians(ang0 + (i * 37) % spread)
        bx, by = x + math.cos(ang) * (r * 0.5 + f * r * 0.9), y + math.sin(ang) * (r * 0.5 + f * r * 0.9)
        bills(c, bx, by, a * (1 - f), 1, rot=i * 40 + f * 90)

def goldbar(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-90, 40); p.lineTo(90, 40); p.lineTo(65, -30); p.lineTo(-65, -30); p.close()
    c.drawPath(p, P(C(GOLD2, a))); c.drawPath(p, P(C(INK, a), stroke=5))
    c.drawLine(-50, -14, 50, -14, P(C((255, 240, 180), a), stroke=5))
    c.restore()

def suitcase(c, x, y, s, a, cross=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-60, -150, 60, -110), 14, 14, P(C(INK, a), stroke=14))
    c.drawRoundRect(skia.Rect(-170, -120, 170, 110), 20, 20, P(C((110, 70, 40), a)))
    c.drawRoundRect(skia.Rect(-170, -120, 170, 110), 20, 20, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-170, -20, 170, -4), P(C((80, 50, 30), a)))
    c.restore()
    if cross > 0:
        c.drawLine(x - 200 * s, y - 160 * s, x - 200 * s + 400 * s * cross, y - 160 * s + 300 * s * cross, P(C(RED, a), stroke=16))

def island(c, x, y, s, a, label="TAX HAVEN"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-220, -40, 220, 50), P(C((200, 170, 110), a)))
    c.drawLine(-110, 0, -90, -200, P(C((110, 80, 50), a), stroke=16))
    for k in range(5):
        ang = math.radians(-160 + k * 35); c.drawLine(-90, -200, -90 + 110 * math.cos(ang), -200 + 70 * math.sin(ang) + 30, P(C((60, 140, 80), a), stroke=18))
    c.restore()
    building(c, x + 70 * s, y - 10 * s, 0.25 * s, a, "BANK", cols=3)
    text(c, label, x, y + 110 * s, BEBAS, 46, CREAM, a, spacing=3)

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    africa(c, CX, 930, 330, 1.0)
    leak(c, CX + 60, 880, 380, t, 1.0, n=10, ang0=-60, spread=120)
    if o1 > 0:
        counter(c, 88000000000, CX, 470, 108 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, o1, prefix="~$", glow=24)
        text(c, "LEAVES AFRICA ILLEGALLY · EVERY YEAR", CX, 560, BEBAS, 54, CREAM, o1, spacing=3)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        pop_text(c, "≈ AID + INVESTMENT", CX, 470, ANTON, 100, CREAM, p)
        pc = prog(t, W_("hook", "combined.") - 0.4, 0.22)
        if pc > 0: stamp(c, CX, 600, "COMBINED", RED, 110, -5, pc, sc=lerp(2.2, 1, eo(pc)))

def sc_source(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("source", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        pop_text(c, "UNCTAD", CX, 450, ANTON, 150, GOLD2, prog(t, W_("source", "UNCTAD,") - 0.3, 0.25) * o1, glow=22, glow_rgb=GOLD)
        pill(c, "UN TRADE & DEVELOPMENT AGENCY", 590, eo(prog(t, W_("source", "UN's") - 0.3, 0.3)) * o1, CREAM, 54, 820)
        paper_doc(c, CX, 960, 0.6, -3, eo(prog(t, 0.3, 0.4)) * o1, "Economic Development in Africa", "REPORT 2020", "ILLICIT FLOWS", lines=5)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        k = eo(prog(t, b1, 0.8))
        c.drawCircle(CX, 830, 230, P(C((60, 56, 48), p)))
        pth = skia.Path(); pth.moveTo(CX, 830); pth.arcTo(skia.Rect(CX - 230, 600, CX + 230, 1060), -90, 360 * 0.037 * k * 3, False); pth.close()
        c.drawPath(pth, P(C(RED, p))); c.drawCircle(CX, 830, 230, P(C(CREAM, p), stroke=5))
        pop_text(c, "3.7%", CX, 470, ANTON, 150, RED, p, glow=18)
        text(c, "OF AFRICA'S ECONOMY (GDP)", CX, 1150, BEBAS, 56, CREAM, p, spacing=3)
        text(c, "(SLICE ENLARGED 3X)", CX, 1210, BEBAS, 36, MUTED, p, spacing=3)

def sc_compare(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("compare", 1)
    pop_text(c, "PER YEAR", CX, 430, ANTON, 100, CREAM, prog(t, 0, 0.25))
    items = [("Aid:", "AID IN", 48, 230, (90, 170, 120)), ("Foreign", "INVESTMENT IN", 54, 540, (90, 170, 120)), ("$88.6", "LEAVING", 88.6, 850, RED)]
    for w, lab, v, x, rgb in items:
        k = eo(prog(t, W_("compare", w) - 0.2, 0.8))
        if k <= 0: continue
        h = 560 * v / 88.6 * k
        c.drawRect(skia.Rect(x - 110, 1180 - h, x + 110, 1180), P(C(rgb, a)))
        c.drawRect(skia.Rect(x - 110, 1180 - h, x + 110, 1180), P(C(CREAM, a), stroke=5))
        text(c, "$%gB" % v, x, 1180 - h - 22, ANTON, 66, GOLD2, a * clamp(k * 3))
        text(c, lab, x, 1235, BEBAS, 44, CREAM, a * clamp(k * 3), spacing=2)

def sc_how(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "HOW?", CX, 440, ANTON, 140, GOLD2, prog(t, 0, 0.25), glow=20, glow_rgb=GOLD)
    rows = [("Fake", "FAKE PRICES ON SHIPMENTS", 620), ("Tax", "TAX DODGING", 760), ("Corruption,", "CORRUPTION", 900), ("theft", "THEFT", 1040), ("crime.", "CRIME", 1180)]
    for w, lab, y in rows:
        p = eo(prog(t, W_("how", w) - 0.3, 0.3))
        box(c, CX, y, 760, 110, p, lab, rgb=(44, 50, 62), size=58)

def sc_gold(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("gold", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        calendar(c, 170, 470, 0.4, a * o1, "2015", "")
        k = eo(prog(t, W_("gold", "$40") - 0.3, 0.9))
        counter(c, 40000000000 * k, 610, 600, 96, GOLD2, a * o1, prefix="~$", glow=18)
        pill(c, "RAW COMMODITY EXPORTS", 760, eo(prog(t, W_("gold", "raw") - 0.3, 0.3)) * o1, CREAM, 56, 720)
        for i in range(6):
            goldbar(c, 260 + (i % 3) * 280, 960 + (i // 3) * 120, 1.0, eo(prog(t, 0.3 + i * 0.12, 0.3)) * o1)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3)); k = eo(prog(t, b1, 0.9))
        c.drawCircle(CX, 860, 240, P(C((60, 56, 48), p)))
        pth = skia.Path(); pth.moveTo(CX, 860); pth.arcTo(skia.Rect(CX - 240, 620, CX + 240, 1100), -90, 360 * 0.77 * k, False); pth.close()
        c.drawPath(pth, P(C(GOLD2, p))); c.drawCircle(CX, 860, 240, P(C(CREAM, p), stroke=5))
        text(c, "~77%", CX, 890, ANTON, 110, INK, p * clamp(k * 2))
        pop_text(c, "GOLD ALONE", CX, 470, ANTON, 130, GOLD2, p, glow=22, glow_rgb=GOLD)
        text(c, "OF COMMODITY-LINKED FLOWS · 2015", CX, 1170, BEBAS, 48, CREAM, p, spacing=3)

def sc_creditor(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pill(c, "THE UN REPORT:", 440, a, CREAM, 62, 480)
    africa(c, 300, 900, 220, a)
    globe(c, 800, 900, 180, a, t)
    k = eo(prog(t, 0.4, 1.2))
    arrow(c, 430, 900, 610, 900, k, a, GOLD2, 14)
    for i in range(3):
        f = (t * 0.6 + i / 3) % 1.0
        bills(c, lerp(430, 620, f), 840 - 40 * math.sin(f * math.pi), a * k, 1, rot=f * 40)
    pn = prog(t, W_("creditor", "net") - 0.3, 0.22)
    if pn > 0: stamp(c, CX, 620, "NET CREDITOR", GOLD2, 120, -5, pn, sc=lerp(2.2, 1, eo(pn)))
    pw = prog(t, W_("creditor", "world.") - 0.4, 0.25)
    if pw > 0: pop_text(c, "TO THE WORLD", CX, 1200, ANTON, 90, CREAM, pw)

def sc_twoside(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("twoside", 1)
    pop_text(c, "IT TAKES TWO SIDES", CX, 440, ANTON, 96, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    africa(c, 240, 860, 180, a)
    k = eo(prog(t, b1 - 0.2, 1.0))
    arrow(c, 380, 860, 580, 860, k, a, RED, 14)
    pb = eo(prog(t, W_("twoside", "banks") - 0.3, 0.3))
    building(c, 800, 780, 0.38, pb, "BANKS", cols=3)
    island(c, 800, 1060, 0.8, eo(prog(t, W_("twoside", "havens") - 0.3, 0.3)))
    if pb > 0:
        for i in range(3):
            f = (t * 0.6 + i / 3) % 1.0
            bills(c, lerp(380, 700, f), 820 + 40 * math.sin(f * 6), pb * (1 - f * 0.3), 1, rot=f * 50)
    pp = prog(t, W_("twoside", "profit") - 0.3, 0.22)
    if pp > 0: stamp(c, CX, 600, "OUTSIDE AFRICA, TOO", RED, 84, -4, pp, sc=lerp(2.2, 1, eo(pp)))
    text(c, "ACCORDING TO WATCHDOGS", CX, 1235, BEBAS, 44, MUTED, eo(prog(t, W_("twoside", "Watchdogs") - 0.3, 0.3)), spacing=4)

def sc_quote(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pill(c, "MUKHISA KITUYI · UNCTAD CHIEF (2020)", 440, a, CREAM, 52, 860)
    for i, (w, lab) in enumerate([("rob", "“ROB AFRICA"), ("people", "AND ITS PEOPLE"), ("prospects.\"", "OF THEIR PROSPECTS”")]):
        pop_text(c, lab, CX, 640 + i * 125, PLAY, 80, GOLD2, prog(t, W_("quote", w) - 0.3, 0.25))
    africa(c, CX, 1120, 120, a * 0.8)
    pop_text(c, "ILLICIT FLOWS...", CX, 540, ANTON, 80, CREAM, prog(t, W_("quote", "illicit") - 0.3, 0.25))

def sc_gap(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("gap", 1)
    pop_text(c, "THE GAP", CX, 430, ANTON, 120, CREAM, prog(t, 0, 0.25))
    k = eo(prog(t, W_("gap", "$200") - 0.3, 0.9))
    counter(c, 200000000000 * k, CX, 600, 112, GOLD2, a, prefix="~$", glow=18)
    text(c, "MORE NEEDED EVERY YEAR · UN GOALS", CX, 680, BEBAS, 50, CREAM, a, spacing=3)
    x0, x1, y = 120, 960, 900
    c.drawRoundRect(skia.Rect(x0, y - 60, x1, y + 60), 20, 20, P(C((60, 56, 48), a)))
    c.drawRoundRect(skia.Rect(x0, y - 60, x1, y + 60), 20, 20, P(C(CREAM, a), stroke=5))
    if t > b1 - 0.3:
        kk = eo(prog(t, b1, 1.0))
        fx = x0 + (x1 - x0) * (88.6 / 200) * kk
        c.drawRoundRect(skia.Rect(x0, y - 60, fx, y + 60), 20, 20, P(C(RED, a)))
        text(c, "THE LEAK: ~$88.6B", (x0 + x1) / 2, y + 140, ANTON, 72, RED, a * clamp(kk * 2))
        pc = prog(t, W_("gap", "big") - 0.3, 0.22)
        if pc > 0: stamp(c, CX, 1170, "A BIG PART", GOLD2, 100, -5, pc, sc=lerp(2.2, 1, eo(pc)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "WHO SHOULD", CX, 430, ANTON, 110, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "STOP THIS MONEY?", CX, 550, ANTON, 104, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    africa(c, 270, 880, 170, eo(prog(t, W_("question", "African") - 0.3, 0.3)))
    text(c, "AFRICAN GOVERNMENTS", 270, 1100, BEBAS, 46, CREAM, eo(prog(t, W_("question", "African") - 0.3, 0.3)), spacing=2)
    island(c, 810, 930, 0.7, eo(prog(t, W_("question", "lands?") - 0.4, 0.3)), label="WHERE IT LANDS")
    text(c, "OR", CX, 900, ANTON, 80, GOLD2, eo(prog(t, W_("question", "or") - 0.3, 0.3)))
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, source=sc_source, compare=sc_compare, how=sc_how, gold=sc_gold, creditor=sc_creditor,
              twoside=sc_twoside, quote=sc_quote, gap=sc_gap, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"twoside"}
_IMP = [("hook", "combined.", -0.4, 0.45), ("source", "3.7%", -0.3, 0.35), ("compare", "$88.6", -0.2, 0.4),
        ("how", "Corruption,", -0.3, 0.3), ("rehook", "gold.", -0.2, 0.45), ("gold", "77%", -0.3, 0.4),
        ("creditor", "net", -0.3, 0.4), ("twoside", "profit", -0.3, 0.4), ("gap", "big", -0.3, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("gold", "$40", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
