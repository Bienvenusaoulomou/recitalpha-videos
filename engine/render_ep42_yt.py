import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep42")
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

import chars as CH

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0
def name_chip(c, x, y, label, a, rgb=CREAM):
    if a <= 0: return
    f = F(BEBAS, 36); w = f.measureText(label) + 30
    c.drawRoundRect(skia.Rect(x - w / 2, y - 30, x + w / 2, y + 12), 10, 10, P(C((20, 18, 14), a * 0.85)))
    text(c, label, x, y, BEBAS, 36, rgb, a, spacing=1)

def server(c, x, y, s, a, t=0, busy=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-90, -260, 90, 0), 10, 10, P(C((36, 40, 48), a)))
    c.drawRoundRect(skia.Rect(-90, -260, 90, 0), 10, 10, P(C(INK, a), stroke=6))
    for i in range(6):
        c.drawRect(skia.Rect(-72, -244 + i * 40, 72, -216 + i * 40), P(C((22, 26, 32), a)))
        on = busy > 0 and math.sin(t * 14 + i * 2.1) > 0.3 - busy
        c.drawCircle(52, -230 + i * 40, 7, P(C((90, 255, 160) if on else (60, 70, 66), a)))
    c.restore()

def lock(c, x, y, s, a, rgb=GOLD2):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawArc(skia.Rect(-50, -110, 50, -10), 180, 180, False, P(C(rgb, a), stroke=18))
    c.drawRoundRect(skia.Rect(-70, -60, 70, 60), 14, 14, P(C(rgb, a)))
    c.drawCircle(0, -5, 14, P(C(INK, a))); c.drawRect(skia.Rect(-5, 0, 5, 30), P(C(INK, a)))
    c.restore()

def data_stream(c, x0, y0, x1, y1, t, a, n=10):
    for i in range(n):
        f = (t * 0.6 + i / n) % 1.0
        x = lerp(x0, x1, f); y = lerp(y0, y1, f) - 160 * math.sin(f * math.pi)
        text(c, "01"[(i + int(t * 4)) % 2], x, y, BEBAS, 46, (90, 255, 160), a * (1 - 0.5 * f))

AFR = [(-0.30, -0.95), (0.05, -1.0), (0.30, -0.88), (0.42, -0.62), (0.70, -0.40), (0.95, -0.38), (0.62, 0.05), (0.50, 0.30),
       (0.30, 0.62), (0.12, 0.98), (-0.05, 0.95), (-0.15, 0.55), (-0.22, 0.20), (-0.30, -0.05), (-0.62, -0.10), (-0.92, -0.30),
       (-0.95, -0.55), (-0.70, -0.85)]
def africa(c, x, y, r, a, rgb=(70, 64, 50), ol=GOLD2):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x + AFR[0][0] * r, y + AFR[0][1] * r)
    for px, py in AFR[1:]: p.lineTo(x + px * r, y + py * r)
    p.close(); c.drawPath(p, P(C(rgb, a))); c.drawPath(p, P(C(ol, a), stroke=6))

WAG = (60, 200, 110)

def smartphone(c, x, y, s, a, t=0, infected=0.0, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-80, -160, 80, 160), 26, 26)
    c.drawRRect(r, P(C((30, 32, 38), a))); c.drawRRect(r, P(C(INK, a), stroke=6))
    scr = skia.Rect(-68, -140, 68, 140)
    c.drawRect(scr, P(C((20, 40, 60), a)))
    if infected > 0:
        c.drawRect(scr, P(C((140, 20, 20), a * infected * (0.6 + 0.4 * math.sin(t * 8)))))
        c.drawCircle(0, -20, 34, P(C(CREAM, a * infected), stroke=8))
        c.drawCircle(0, -20, 12, P(C(CREAM, a * infected)))
    c.drawRoundRect(skia.Rect(-24, -152, 24, -144), 4, 4, P(C(INK, a)))
    c.restore()

def gavel(c, x, y, s, a, hit=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-40 + 40 * hit)
    c.drawRoundRect(skia.Rect(-10, -20, 170, 10), 6, 6, P(C((130, 84, 46), a))); c.drawRoundRect(skia.Rect(-10, -20, 170, 10), 6, 6, P(C(INK, a), stroke=5))
    c.drawRoundRect(skia.Rect(-60, -60, 20, 50), 12, 12, P(C((150, 98, 54), a))); c.drawRoundRect(skia.Rect(-60, -60, 20, 50), 12, 12, P(C(INK, a), stroke=5))
    c.restore()
    c.drawRoundRect(skia.Rect(x - 110 * s, y + 70 * s, x + 50 * s, y + 100 * s), 8, 8, P(C((110, 70, 40), a)))

def chat_bubble(c, x, y, w, h, a, label, rgb=WAG):
    if a <= 0: return
    r = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 30, 30)
    c.drawRRect(r, P(C(rgb, a))); c.drawRRect(r, P(C(INK, a), stroke=5))
    pth = skia.Path(); pth.moveTo(x - w / 2 + 40, y + h / 2 - 2); pth.lineTo(x - w / 2 + 10, y + h / 2 + 40); pth.lineTo(x - w / 2 + 90, y + h / 2 - 2); pth.close()
    c.drawPath(pth, P(C(rgb, a)))
    text(c, label, x, y + 20, ANTON, 58, CREAM, a)

def phone_grid(c, t, a, n_inf, y0=700):
    for i in range(10):
        x = 140 + (i % 5) * 200; y = y0 + (i // 5) * 300
        smartphone(c, x, y, 0.7, a, t, infected=1.0 if i < n_inf else 0.0)

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    counter(c, 650000, CX, 470, 140 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="$", glow=24)
    text(c, "TO SPY ON 10 IPHONES", CX, 560, BEBAS, 64, CREAM, 1.0, spacing=6)
    n = 10 if t > 0.0 else 0
    phone_grid(c, t, 1.0, int(clamp(t / 1.8) * 10) if t < 1.8 else 10, y0=760)
    po = prog(t, b1 - 0.05, 0.22)
    if po > 0: stamp(c, CX, 910, "THE PRICE LIST", RED, 110, -6, po, sc=lerp(2.2, 1, eo(po)))

def sc_pricelist(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("pricelist", 1); b2 = B("pricelist", 2)
    pop_text(c, "PEGASUS · 2016", CX, 440, ANTON, 104, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    text(c, "PRICES REPORTED BY THE NEW YORK TIMES", CX, 510, BEBAS, 42, CREAM, a, spacing=2)
    pn = eo(prog(t, W_("pricelist", "NSO") - 0.3, 0.3))
    name_chip(c, CX, 590, "MADE BY NSO GROUP (ISRAEL)", pn, rgb=CREAM)
    rows = [("$500,000", "INSTALLATION FEE", W_("pricelist", "$500,000")), ("$650,000", "10 IPHONE USERS", W_("pricelist", "$650,000")),
            ("+17%", "OF THE TOTAL, EVERY YEAR", W_("pricelist", "17%"))]
    pr = eo(prog(t, 0.2, 0.3))
    if pr > 0:
        rr = skia.Rect(150, 660, 930, 1210)
        c.drawRoundRect(rr, 20, 20, P(C((236, 226, 204), pr))); c.drawRoundRect(rr, 20, 20, P(C(GOLD, pr), stroke=6))
        text(c, "PRICE LIST", CX, 740, ANTON, 64, INK, pr, spacing=4)
    for i, (v, lab, tw) in enumerate(rows):
        p = eo(prog(t, tw - 0.3, 0.3))
        y = 860 + i * 130
        text(c, v, 200, y, ANTON, 76, RED if i == 1 else INK, p, align="l")
        text(c, lab, 880, y - 6, BEBAS, 42, INK, p, align="r", spacing=2)
        if p > 0: c.drawLine(200, y + 30, 880, y + 30, P(C(MUTED, p), stroke=3))

def sc_attack(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("attack", 1)
    calendar(c, 190, 520, 0.6, a, "2019", "")
    pop_text(c, "WHATSAPP", CX + 120, 480, ANTON, 110, WAG, prog(t, 0.1, 0.25), glow=16, glow_rgb=WAG)
    k = clamp(prog(t, 0.6, 2.5))
    for i in range(24):
        x = 140 + (i % 6) * 160; y = 720 + (i // 6) * 140
        smartphone(c, x, y, 0.38, a, t, infected=1.0 if i < int(k * 24) else 0.0)
    pc = eo(prog(t, W_("attack", "1,400") - 0.3, 0.3))
    if pc > 0:
        c.drawRoundRect(skia.Rect(CX - 320, 1180, CX + 320, 1270), 20, 20, P(C(INK, pc * 0.85)))
        text(c, "~1,400 USERS TARGETED", CX, 1245, ANTON, 64, GOLD2, pc)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        chat_bubble(c, CX, 650, 520, 120, p, "WE'RE SUING NSO")

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("verdict", 1)
    pop_text(c, "JURY VERDICT · MAY 2025", CX, 440, ANTON, 84, CREAM, prog(t, 0, 0.25))
    hit = clamp(math.sin(min(t, 1.2) * 5)) if t < 1.2 else 1.0
    gavel(c, 240, 1030, 1.0, a, hit)
    scales(c, 800, 1060, 0.8, a, tilt=0.4 * math.sin(t * 1.5))
    counter(c, int(167000000 * eo(prog(t, 0.0, 1.4))), CX, 640, 120, GOLD2, a, prefix="$", glow=22)
    text(c, "PUNITIVE DAMAGES", CX, 720, BEBAS, 56, CREAM, a, spacing=6)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "+ ~$444,000", CX, 830, ANTON, 80, CREAM, p)
        text(c, "COMPENSATORY DAMAGES", CX, 890, BEBAS, 44, CREAM, p * 0.85, spacing=4)

def sc_cut(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("cut", 1)
    calendar(c, 190, 520, 0.6, a, "OCT", "2025")
    pop_text(c, "THE JUDGE", CX + 120, 480, ANTON, 110, CREAM, prog(t, 0.1, 0.25))
    pc = prog(t, W_("cut", "cut") - 0.2, 0.5)
    v = int(lerp(167000000, 4000000, eo(prog(t, W_("cut", "$4") - 0.6, 0.9))))
    counter(c, v, CX, 720, 120, GOLD2 if pc < 1 else RED, a, prefix="$", glow=18)
    text(c, "PUNITIVE DAMAGES", CX, 800, BEBAS, 52, CREAM, a, spacing=6)
    if pc > 0: stamp(c, CX, 900, "CUT BY ~97%", RED, 80, -4, pc, sc=lerp(2.2, 1, eo(pc)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        smartphone(c, 300, 1110, 0.6, p, t)
        shield(c, 300, 1110, 0.6, p, label="")
        box(c, 720, 1100, 480, 120, p, "BANNED: TARGETING WHATSAPP", rgb=(40, 70, 50), size=46)

def sc_customers(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("customers", 1)
    pop_text(c, "GOVERNMENTS PAY", CX, 440, ANTON, 104, CREAM, prog(t, 0, 0.25))
    building(c, CX, 820, 0.7, a, "GOVERNMENT", cols=5)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        name_chip(c, CX, 900, "MEXICO · GOVERNMENT FIGURE, 2021", p, rgb=GOLD2)
        pm = eo(prog(t, W_("customers", "$61") - 0.4, 0.3))
        counter(c, max(1000000, int(61000000 * eo(prog(t, W_("customers", "$61") - 0.4, 1.0)))), CX, 1060, 120, GOLD2, pm, prefix="~$", glow=18)
        text(c, "SPENT ON PEGASUS BY PAST ADMINISTRATIONS", CX, 1140, BEBAS, 40, CREAM, pm, spacing=2)

def sc_appeal(c, t, D):
    a = eo(prog(t, 0, 0.3))
    box(c, CX, 560, 820, 140, a, "NSO: \"WE SELL ONLY TO GOVERNMENTS\"", rgb=(50, 46, 60), size=54)
    text(c, "NSO'S POSITION", CX, 670, BEBAS, 40, CREAM, a * 0.8, spacing=4)
    pp = prog(t, W_("appeal", "appealed") - 0.3, 0.25)
    gavel(c, 300, 980, 0.9, a, 0.0); scales(c, 760, 1020, 0.7, a, tilt=0.3 * math.sin(t * 1.5))
    if pp > 0: stamp(c, CX, 1170, "APPEAL PENDING", GOLD2, 96, -5, pp, sc=lerp(2.2, 1, eo(pp)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i in range(5): smartphone(c, 160 + i * 190, 1150, 0.55, a, t, infected=1.0 if (int(t * 2) + i) % 3 == 0 else 0.0)
    text(c, "?", CX, 830, ANTON, 180, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "SHOULD SPYWARE BE SOLD", CX, 430, ANTON, 88, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "TO GOVERNMENTS?", CX, 545, ANTON, 104, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 970)

E.DRAW = dict(hook=sc_hook, pricelist=sc_pricelist, attack=sc_attack, verdict=sc_verdict, cut=sc_cut, customers=sc_customers,
              appeal=sc_appeal, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"attack"}
_IMP = [("hook", "That", -0.1, 0.4), ("pricelist", "$650,000", -0.3, 0.35), ("attack", "1,400", -0.3, 0.35), ("rehook", "huge.", -0.2, 0.4),
        ("verdict", "$167", -0.3, 0.45), ("cut", "cut", -0.2, 0.4), ("customers", "$61", -0.3, 0.35), ("appeal", "appealed", -0.3, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$650,000", 0.0), ("verdict", "$167", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
