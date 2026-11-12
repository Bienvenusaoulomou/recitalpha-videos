import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep41")
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

BLUE_M = (66, 168, 206)
CONT = [(66, 168, 206), (206, 62, 44), (214, 168, 75), (90, 150, 110), (150, 160, 176)]

def ship(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y + 6 * math.sin(t * 1.6)); c.scale(s, s); c.rotate(1.2 * math.sin(t * 1.3))
    for r in range(3):
        for i in range(9):
            col = CONT[(i * 3 + r * 2) % len(CONT)]
            rr = skia.Rect(-300 + i * 62, -70 - r * 46, -244 + i * 62, -28 - r * 46)
            c.drawRect(rr, P(C(col, a))); c.drawRect(rr, P(C(INK, a), stroke=4))
    c.drawRect(skia.Rect(270, -230, 330, -28), P(C(CREAM, a))); c.drawRect(skia.Rect(270, -230, 330, -28), P(C(INK, a), stroke=5))
    for k in range(3): c.drawRect(skia.Rect(280, -215 + k * 40, 320, -195 + k * 40), P(C((40, 60, 80), a)))
    h = skia.Path(); h.moveTo(-380, -30); h.lineTo(400, -30); h.lineTo(350, 70); h.lineTo(-340, 70); h.close()
    c.drawPath(h, P(C(BLUE_M, a))); c.drawPath(h, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-340, 40, 350, 70), P(C((40, 50, 70), a)))
    c.restore()

def waves(c, y, a, t):
    for k in range(3):
        p = skia.Path(); yy = y + k * 40
        p.moveTo(0, yy)
        for xx in range(0, 1100, 20): p.lineTo(xx, yy + 10 * math.sin(xx / 60 + t * 2 + k))
        p.lineTo(1080, 1300); p.lineTo(0, 1300); p.close()
        c.drawPath(p, P(C((30 + k * 6, 60 + k * 8, 90 + k * 10), a * 0.9)))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    waves(c, 1110, 1.0, t)
    ship(c, 620, 1090, 0.95, 1.0, t)
    counter(c, 5000000, CX, 470, 140 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="$", glow=24)
    text(c, "RANSOM DEMAND", CX, 560, BEBAS, 64, CREAM, 1.0, spacing=8)
    CH.HACKER.draw(c, 170, 1230, 0.8, 1, blink=0, look=(1, 0), arm_f=(-70 + 10 * math.sin(t * 9), -60), arm_b=(-40, -50))
    laptop(c, 290, 1170, 0.45, 1.0, t)
    po = prog(t, b1 - 0.05, 0.22)
    if po > 0: stamp(c, CX, 720, "NOT THE FIRST TIME", RED, 96, -6, po, sc=lerp(2.2, 1, eo(po)))

def sc_claim(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("claim", 1)
    calendar(c, 190, 520, 0.6, a, "NOV", "7 · 2026")
    pop_text(c, "LEAK SITE", CX + 120, 480, ANTON, 96, CREAM, prog(t, 0.1, 0.25))
    screen(c, CX, 790, 760, 330, a, "WHITEARMOR")
    pm = eo(prog(t, W_("claim", "Maersk") - 0.3, 0.3))
    text(c, "VICTIM: MAERSK", CX, 790, ANTON, 76, RED, pm)
    text(c, "GANG CLAIM · UNVERIFIED", CX, 860, BEBAS, 40, CREAM, pm * 0.85, spacing=3)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        server(c, 250, 1240, 0.8, p, t, busy=1.0)
        data_stream(c, 330, 1060, 820, 1060, t, p)
        text(c, "~100 GB", 820, 1150, ANTON, 90, GOLD2, p, glow=14)
        pp = eo(prog(t, W_("claim", "passwords.") - 0.3, 0.3))
        text(c, "+ THOUSANDS OF PASSWORDS", 700, 1220, BEBAS, 46, CREAM, pp, spacing=2)

def sc_ransom(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("ransom", 1)
    counter(c, 5000000, CX, 500, 130, GOLD2, a, prefix="$", glow=22)
    text(c, "IN BITCOIN", CX, 590, BEBAS, 60, CREAM, a, spacing=8)
    for i in range(5):
        crypto_coin(c, 200 + i * 170, 760 + 20 * math.sin(t * 3 + i), 54, a, t + i)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        clock(c, CX, 1030, 130, p, t_h=12 - (t - b1) * 0.8, label=None)
        ps = prog(t, W_("ransom", "30") - 0.2, 0.22)
        if ps > 0: stamp(c, CX, 1215, "30-DAY DEADLINE", RED, 88, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_confirm(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("confirm", 1)
    calendar(c, 190, 520, 0.6, a, "NOV", "11 · 2026")
    pop_text(c, "MAERSK CONFIRMS", CX + 110, 480, ANTON, 84, CREAM, prog(t, 0.1, 0.25))
    pd_ = eo(prog(t, W_("confirm", "old") - 0.3, 0.3))
    box(c, CX, 700, 760, 130, pd_, "OLD LOCAL SYSTEM", rgb=(60, 46, 40), size=62)
    text(c, "FROM A COMPANY IT HAD BOUGHT", CX, 820, BEBAS, 46, CREAM, pd_, spacing=3)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        waves(c, 1150, p, t)
        ship(c, CX + 60 * math.sin(t * 0.3), 1130, 0.75, p, t)
        text(c, "\"NO SENSITIVE DATA\" SEEMS OUT", CX, 930, BEBAS, 52, GOLD2, p, spacing=2)
        text(c, "· ACCORDING TO MAERSK ·", CX, 985, BEBAS, 36, CREAM, p * 0.8, spacing=3)

def sc_notpetya(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("notpetya", 1)
    calendar(c, 190, 520, 0.6, a, "JUN", "27 · 2017")
    pop_text(c, "NOTPETYA", CX + 120, 490, ANTON, 120, RED, prog(t, 0.1, 0.25), glow=18, glow_rgb=RED)
    if t < b1 - 0.2:
        for i in range(5):
            gl = 1.0 if math.sin(t * 17 + i * 3) > 0.2 else 0.4
            laptop(c, 160 + i * 190, 900, 0.36, a, t, label="ERROR" if gl > 0.5 else None, rgb=RED)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        text(c, "REBUILT IN 10 DAYS", CX, 740, ANTON, 84, GOLD2, p, glow=14)
        p1 = eo(prog(t, W_("notpetya", "4,000") - 0.3, 0.3))
        for i in range(4): server(c, 140 + i * 110, 1000, 0.6, p1, t, busy=1.0)
        counter(c, int(4000 * eo(prog(t, W_("notpetya", "4,000") - 0.3, 0.8))), 300, 1090, 80, CREAM, p1, prefix="")
        text(c, "SERVERS", 300, 1150, BEBAS, 48, CREAM, p1, spacing=4)
        p2 = eo(prog(t, W_("notpetya", "45,000") - 0.3, 0.3))
        laptop(c, 780, 950, 0.55, p2, t)
        counter(c, int(45000 * eo(prog(t, W_("notpetya", "45,000") - 0.3, 0.8))), 780, 1090, 80, CREAM, p2, prefix="")
        text(c, "PCs", 780, 1150, BEBAS, 48, CREAM, p2, spacing=4)

def sc_ghana(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("ghana", 1)
    africa(c, 330, 800, 300, a)
    pin(c, 230, 790, 1.0, a, rgb=GOLD2, label=None)
    pop_text(c, "GHANA", CX, 440, ANTON, 130, GOLD2, prog(t, 0, 0.25), glow=20, glow_rgb=GOLD)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        dark = 1.0 if (t - b1) % 1.6 < 1.0 else 0.6
        server(c, 790, 1100, 1.0, p, t, busy=0.0)
        text(c, "POWER CUT", 790, 760, ANTON, 80, RED, p * dark)
        ps = prog(t, W_("ghana", "never") - 0.3, 0.22)
        if ps > 0: stamp(c, 790, 1200, "IT SURVIVED", (90, 255, 160), 76, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_bill(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("bill", 1)
    text(c, "UP TO", CX, 430, BEBAS, 70, CREAM, a, spacing=8)
    counter(c, int(300000000 * eo(prog(t, 0.1, 1.2))), CX, 560, 128, GOLD2, a, prefix="$", glow=22)
    text(c, "THE COST OF NOTPETYA FOR MAERSK", CX, 640, BEBAS, 46, CREAM, a, spacing=2)
    for i in range(5): bills(c, 200 + i * 170, 830 + 30 * math.sin(t * 2 + i), a, n=3, rot=8 * math.sin(t * 2 + i))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        name_chip(c, CX, 1000, "US + UK GOVERNMENTS, FEB 2018", p, rgb=GOLD2)
        ps = prog(t, W_("bill", "Russian") - 0.3, 0.22)
        if ps > 0: stamp(c, CX, 1160, "BLAMED: RUSSIAN MILITARY", RED, 76, -4, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    waves(c, 1170, a, t); ship(c, 640, 1160, 0.6, a, t)
    CH.HACKER.draw(c, 170, 1230, 0.75, 1, a=a, blink=0, look=(1, 0))
    text(c, "?", CX, 830, ANTON, 180, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "SHOULD A COMPANY", CX, 430, ANTON, 96, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "EVER PAY A RANSOM?", CX, 545, ANTON, 100, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 990)

E.DRAW = dict(hook=sc_hook, claim=sc_claim, ransom=sc_ransom, confirm=sc_confirm, notpetya=sc_notpetya, ghana=sc_ghana,
              bill=sc_bill, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"notpetya"}
_IMP = [("hook", "not", -0.1, 0.4), ("claim", "Maersk", -0.3, 0.3), ("ransom", "30", -0.2, 0.4), ("rehook", "2017...", -0.2, 0.4),
        ("notpetya", "NotPetya", -0.3, 0.45), ("ghana", "never", -0.3, 0.4), ("bill", "Russian", -0.3, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$5", 0.0), ("bill", "$300", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
