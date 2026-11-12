import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep43")
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

HOSP = (90, 170, 220)

def med_cross(c, x, y, s, a, rgb=(220, 60, 60)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-90, -90, 90, 90), 20, 20, P(C(CREAM, a))); c.drawRoundRect(skia.Rect(-90, -90, 90, 90), 20, 20, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-22, -62, 22, 62), P(C(rgb, a))); c.drawRect(skia.Rect(-62, -22, 62, 22), P(C(rgb, a)))
    c.restore()

def pct_icon(c, x, y, s, a, rgb=RED):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 90, P(C(rgb, a))); c.drawCircle(0, 0, 90, P(C(INK, a), stroke=6))
    text(c, "%", 0, 36, ANTON, 110, CREAM, a)
    c.restore()

def bar_pair(c, t, a, v1, v2, lab1, lab2, y0=1180, h=520, k=1.0, k2=1.0):
    mx = max(v1, v2)
    for i, (v, lab, rgb, kk) in enumerate([(v1, lab1, RED, k), (v2, lab2, HOSP, k2)]):
        x = 330 + i * 420; hh = h * v / mx * eo(kk)
        if kk <= 0: continue
        c.drawRect(skia.Rect(x - 110, y0 - hh, x + 110, y0), P(C(rgb, a)))
        c.drawRect(skia.Rect(x - 110, y0 - hh, x + 110, y0), P(C(INK, a), stroke=6))
        text(c, "$%d" % v, x, y0 - hh - 24, ANTON, 96, GOLD2, a * clamp(kk * 2))
        text(c, lab, x, y0 + 60, BEBAS, 54, CREAM, a * clamp(kk * 2), spacing=4)

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    africa(c, CX, 820, 330, 0.25, rgb=(60, 54, 42), ol=(120, 100, 60))
    pop_text(c, "INTEREST vs HEALTH", CX, 450, ANTON, 96, CREAM, 1.0)
    k2 = clamp((t - W_("hook", "$42") + 0.4) / 0.4) if t > 0.1 else 0
    bar_pair(c, t, 1.0, 66, 42, "INTEREST", "HEALTH", y0=1150, h=400, k=1.0, k2=max(0.0, k2))
    if t > b1 - 0.1:
        p = eo(prog(t, b1 - 0.1, 0.3))
        name_chip(c, CX, 560, "PER PERSON · PER YEAR · UNCTAD", p, rgb=GOLD2)

def sc_world(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("world", 1)
    globe(c, CX, 860, 210, a * 0.9, t)
    text(c, "WORLD PUBLIC DEBT · 2025", CX, 440, BEBAS, 62, CREAM, a, spacing=5)
    counter(c, int(111e12 * eo(prog(t, 0.1, 1.4))), CX, 560, 96, GOLD2, a, prefix="~$", glow=20)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1170, 760, 130, p, "~$1 TRILLION IN INTEREST", rgb=(70, 34, 30), size=64)
        text(c, "PAID BY DEVELOPING COUNTRIES IN ONE YEAR", CX, 1085, BEBAS, 44, CREAM, p, spacing=2)

def sc_people(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("people", 1)
    text(c, "3.7", CX, 500, ANTON, 150, GOLD2, a, glow=22, glow_rgb=GOLD)
    text(c, "BILLION PEOPLE", CX, 580, BEBAS, 64, CREAM, a, spacing=6)
    text(c, "INTEREST > HEALTH OR EDUCATION", CX, 650, BEBAS, 50, RED, a, spacing=3)
    rng = random.Random(4)
    for i in range(60):
        x = 120 + (i % 12) * 76; y = 760 + (i // 12) * 70
        ink = (214, 168, 75) if (t > b1 - 0.3 and i < 16) else (120, 110, 90)
        c.drawCircle(x, y - 22, 14, P(C(ink, a))); c.drawRoundRect(skia.Rect(x - 18, y - 6, x + 18, y + 30), 10, 10, P(C(ink, a)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        africa(c, 900, 1180, 70, p)
        text(c, "~970 MILLION IN AFRICA", 470, 1200, ANTON, 64, GOLD2, p)

def sc_rates(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("rates", 1)
    pop_text(c, "THE PRICE OF BORROWING", CX, 440, ANTON, 84, CREAM, prog(t, 0, 0.25))
    rows = [("US", 1, (120, 140, 180), 0.0), ("DEVELOPING COUNTRIES", 4, RED, 0.3)]
    p1 = eo(prog(t, 0.2, 0.6))
    c.drawRect(skia.Rect(150, 600, 150 + 160 * p1, 680), P(C((120, 140, 180), a)))
    text(c, "US RATE", 150, 580, BEBAS, 46, CREAM, a, align="l", spacing=3)
    p2 = eo(prog(t, W_("rates", "2") - 0.3, 1.0))
    c.drawRect(skia.Rect(150, 780, 150 + 640 * p2, 860), P(C(RED, a)))
    text(c, "DEVELOPING COUNTRIES", 150, 760, BEBAS, 46, CREAM, a * clamp(p2 * 3), align="l", spacing=3)
    text(c, "2-4x", 150 + 640 * p2 + 20, 845, ANTON, 76, GOLD2, a * clamp(p2 * 3), align="l") if p2 > 0 else None
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        c.drawRect(skia.Rect(150, 990, 150 + 60 * p, 1050), P(C((200, 200, 200), a)))
        text(c, "GERMANY'S RATE", 150, 970, BEBAS, 46, CREAM, p, align="l", spacing=3)
        ps = prog(t, W_("rates", "12") - 0.2, 0.22)
        if ps > 0: stamp(c, CX + 80, 1160, "UP TO 12x MORE", RED, 96, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_kenya(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("kenya", 1)
    africa(c, 200, 560, 110, a)
    pin(c, 250, 560, 0.5, a, rgb=GOLD2)
    pop_text(c, "KENYA", CX + 120, 480, ANTON, 120, GOLD2, prog(t, 0.1, 0.25), glow=18, glow_rgb=GOLD)
    text(c, "BUDGET PLAN · ~2025/26 · SHILLINGS", CX + 120, 550, BEBAS, 40, CREAM, a, spacing=2)
    pi = eo(prog(t, W_("kenya", "1.1") - 0.3, 0.6))
    hh = 390 * pi
    c.drawRect(skia.Rect(220, 1180 - hh, 440, 1180), P(C(RED, a))); c.drawRect(skia.Rect(220, 1180 - hh, 440, 1180), P(C(INK, a), stroke=6))
    if pi > 0: text(c, "1.1 TRILLION", 330, 1180 - hh - 24, ANTON, 72, GOLD2, a)
    text(c, "INTEREST", 330, 1240, BEBAS, 52, CREAM, a * clamp(pi * 2), spacing=4)
    if t > b1 - 0.3:
        ph = eo(prog(t, b1 - 0.1, 0.6)); h2 = 390 * 139 / 1100 * ph
        c.drawRect(skia.Rect(640, 1180 - h2, 860, 1180), P(C(HOSP, a))); c.drawRect(skia.Rect(640, 1180 - h2, 860, 1180), P(C(INK, a), stroke=6))
        text(c, "139 BILLION", 750, 1180 - h2 - 24, ANTON, 72, GOLD2, a * ph)
        text(c, "NATIONAL HEALTH", 750, 1240, BEBAS, 52, CREAM, a * ph, spacing=4)
        med_cross(c, 750, 860, 0.7, a * ph)

def sc_zambia(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("zambia", 1)
    calendar(c, 190, 520, 0.6, a, "2020", "")
    pop_text(c, "ZAMBIA", CX + 120, 480, ANTON, 120, GOLD2, prog(t, 0.1, 0.25), glow=18, glow_rgb=GOLD)
    ticket(c, CX, 820, 1.0, a, rot=-3, head="BOND PAYMENT", title="$42.5 MILLION", sub="DUE OCT 2020")
    ps = prog(t, W_("zambia", "missed") - 0.2, 0.22)
    if ps > 0: stamp(c, CX + 150, 990, "MISSED", RED, 96, -8, ps, sc=lerp(2.2, 1, eo(ps)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1130, 820, 130, p, "AFRICA'S FIRST DEFAULT OF THE PANDEMIC", rgb=(70, 34, 30), size=52)

def sc_views(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("views", 1)
    pop_text(c, "TWO VIEWS", CX, 440, ANTON, 120, CREAM, prog(t, 0, 0.25))
    CH.CFO.draw(c, 260, 1220, 0.85, 1, a=a, blink=bl(t), arm_f=(-50, -60))
    box(c, 280, 560, 470, 110, a, "GOVTS BORROWED", rgb=(50, 46, 60), size=56)
    text(c, "TOO MUCH", 280, 665, ANTON, 56, CREAM, a)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        CH.OFFICIAL.draw(c, 820, 1220, 0.85, -1, a=p, blink=bl(t, 2.7), arm_f=(-50, -60))
        box(c, 800, 560, 470, 110, p, "LENDERS CHARGE", rgb=(50, 46, 60), size=56)
        text(c, "TOO MUCH", 800, 665, ANTON, 56, CREAM, p)
    scales(c, CX, 1000, 0.55, a, tilt=0.5 * math.sin(t * 1.4))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    africa(c, CX, 1110, 110, a * 0.8)
    for i in range(6): bills(c, 140 + i * 160, 1215 + 15 * math.sin(t * 2 + i), a, n=2, rot=8 * math.sin(t * 2 + i))
    text(c, "?", CX, 790, ANTON, 170, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "WHO SHOULD FIX IT:", CX, 430, ANTON, 96, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "GOVERNMENTS OR LENDERS?", CX, 545, ANTON, 84, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 920)

E.DRAW = dict(hook=sc_hook, world=sc_world, people=sc_people, rates=sc_rates, kenya=sc_kenya, zambia=sc_zambia,
              views=sc_views, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"zambia"}
_IMP = [("hook", "$42", -0.3, 0.4), ("world", "$1", -0.3, 0.35), ("people", "970", -0.3, 0.35), ("rehook", "rate.", -0.2, 0.4),
        ("rates", "12", -0.2, 0.4), ("kenya", "139", -0.3, 0.35), ("zambia", "missed", -0.2, 0.45)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$66", 0.0), ("world", "$111", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
