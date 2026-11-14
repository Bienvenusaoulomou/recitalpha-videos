import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep46")
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
from kit4 import *
import chars as CH

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0
def name_chip(c, x, y, label, a, rgb=CREAM, size=36):
    if a <= 0: return
    f = F(BEBAS, size); w = f.measureText(label) + 30
    c.drawRoundRect(skia.Rect(x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.35), 10, 10, P(C((20, 18, 14), a * 0.85)))
    text(c, label, x, y, BEBAS, size, rgb, a, spacing=1)

PIPE = (150, 140, 120)
def pipeline(c, y, a, t, flow=1.0, x0=40, x1=1040):
    if a <= 0: return
    c.drawRect(skia.Rect(x0, y - 40, x1, y + 40), P(C(PIPE, a)))
    c.drawRect(skia.Rect(x0, y - 40, x1, y + 40), P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(x0, y - 30, x1, y - 18), P(C((200, 190, 170), a * 0.6)))
    for i in range(int((x1 - x0) / 160) + 1):
        xx = x0 + 60 + i * 160
        c.drawRect(skia.Rect(xx - 14, y - 50, xx + 14, y + 50), P(C((110, 100, 86), a)))
        c.drawRect(skia.Rect(xx - 14, y - 50, xx + 14, y + 50), P(C(INK, a), stroke=4))
    if flow > 0:
        for i in range(12):
            f = (t * 0.5 * flow + i / 12) % 1.0
            c.drawCircle(lerp(x0, x1, f), y, 9, P(C(GOLD2, a * 0.8 * flow)))

def pump(c, x, y, s, a, empty=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-80, -300, 80, 0), 14, 14, P(C((190, 50, 46), a))); c.drawRoundRect(skia.Rect(-80, -300, 80, 0), 14, 14, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-55, -270, 55, -190), P(C((20, 24, 22), a)))
    text(c, "EMPTY" if empty > 0.5 else "GAS", 0, -215, BEBAS, 40, RED if empty > 0.5 else (90, 255, 160), a)
    c.drawLine(80, -200, 120, -200, P(C(INK, a), stroke=10)); c.drawLine(120, -200, 120, -60, P(C(INK, a), stroke=10))
    c.drawRect(skia.Rect(-100, -10, 100, 14), P(C((70, 66, 60), a)))
    c.restore()

def wallet(c, x, y, s, a, rgb=(90, 64, 40)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-170, -110, 170, 110), 22, 22, P(C(rgb, a))); c.drawRoundRect(skia.Rect(-170, -110, 170, 110), 22, 22, P(C(INK, a), stroke=6))
    c.drawRoundRect(skia.Rect(60, -40, 190, 40), 14, 14, P(C((120, 88, 56), a))); c.drawRoundRect(skia.Rect(60, -40, 190, 40), 14, 14, P(C(INK, a), stroke=5))
    c.drawCircle(110, 0, 12, P(C(GOLD2, a)))
    c.restore()

def badge(c, x, y, s, a, label="FBI"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    for k in range(10):
        r = 120 if k % 2 == 0 else 80; ang = -math.pi / 2 + k * math.pi / 5
        (p.moveTo if k == 0 else p.lineTo)(r * math.cos(ang), r * math.sin(ang))
    p.close(); c.drawPath(p, P(C(GOLD2, a))); c.drawPath(p, P(C(INK, a), stroke=6))
    text(c, label, 0, 20, ANTON, 54, INK, a)
    c.restore()

def price_chart(c, x0, y0, w, h, k, a):
    """falling bitcoin price line"""
    pts = [(0, 0.15), (0.15, 0.1), (0.3, 0.3), (0.45, 0.25), (0.6, 0.5), (0.75, 0.6), (0.9, 0.75), (1.0, 0.8)]
    c.drawRect(skia.Rect(x0, y0, x0 + w, y0 + h), P(C((14, 18, 26), a)))
    path = skia.Path(); n = max(2, int(len(pts) * k))
    for i, (px, py) in enumerate(pts[:n]):
        (path.moveTo if i == 0 else path.lineTo)(x0 + px * w, y0 + py * h)
    c.drawPath(path, P(C(RED, a), stroke=10))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    pop_text(c, "RANSOM PAID", CX, 430, ANTON, 100, CREAM, 1.0)
    counter(c, 4400000, CX, 570, 130, GOLD2, 1.0, prefix="$", glow=22)
    for i in range(5): crypto_coin(c, 180 + i * 180, 680, 60, 1.0, t + i)
    CH.HACKER.draw(c, 230, 1240, 0.85, 1, a=1.0, arm_f=(-60 + 8 * math.sin(t * 9), -60))
    if t > b1 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        badge(c, 800, 1060, 0.9 * lerp(1.6, 1, p), p)
        ps = prog(t, W_("hook", "back") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 900, "TAKEN BACK", RED, 100, -6, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_shutdown(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("shutdown", 1)
    calendar(c, 200, 520, 0.6, a, "7", "MAY 2021")
    pop_text(c, "COLONIAL PIPELINE", CX + 120, 470, ANTON, 90, CREAM, prog(t, 0.1, 0.25))
    off = W_("shutdown", "shut")
    pipeline(c, 860, a, t, flow=1.0 - clamp((t - off) / 0.6))
    ps = prog(t, off, 0.22)
    if ps > 0: stamp(c, CX + 60, 715, "SHUT DOWN", RED, 100, -5, ps, sc=lerp(2.2, 1, eo(ps)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        laptop(c, 300, 1220, 0.6, p, t, label="LOCKED", rgb=RED)
        CH.HACKER.draw(c, 760, 1250, 0.8, -1, a=p, arm_f=(-50, -60))
        name_chip(c, 300, 1030, "DARKSIDE", p, rgb=RED, size=44)

def sc_fuel(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("fuel", 1)
    pop_text(c, "AMERICA'S EAST COAST", CX, 430, ANTON, 90, CREAM, prog(t, 0, 0.25))
    stopped = t > b1 - 0.2
    pipeline(c, 620, a, t, flow=0.0 if stopped else 1.0)
    for i in range(4):
        pump(c, 200 + i * 230, 1180, 0.8, a, empty=1.0 if stopped and t > b1 + i * 0.25 else 0.0)
    if stopped:
        ps = prog(t, b1 - 0.2, 0.22)
        stamp(c, CX, 820, "STOPPED", RED, 110, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_paid(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("paid", 1)
    n = int(75 * eo(prog(t, 0.2, 1.2)))
    for i in range(min(n, 75)):
        x = 130 + (i % 15) * 59; y = 520 + (i // 15) * 70
        crypto_coin(c, x, y, 26, a, t + i * 0.1)
    text(c, "%d BITCOINS" % n, CX, 960, ANTON, 120, GOLD2, a, glow=20, glow_rgb=GOLD)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1150, 820, 140, p, "THEN WORTH ~$4.4 MILLION", rgb=(40, 46, 60), size=72)

def sc_wallet(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("wallet", 1)
    pop_text(c, "FOLLOW THE BITCOIN", CX, 430, ANTON, 96, CREAM, prog(t, 0, 0.25))
    pts = [(150, 620), (420, 780), (250, 960), (620, 900), (820, 1080)]
    k = eo(prog(t, 0.2, 2.2))
    for i in range(len(pts) - 1):
        kk = clamp(k * (len(pts) - 1) - i)
        if kk > 0:
            arrow(c, pts[i][0], pts[i][1], lerp(pts[i][0], pts[i + 1][0], kk), lerp(pts[i][1], pts[i + 1][1], kk), 1.0, a)
    for i, (x, y) in enumerate(pts[:-1]):
        if k * (len(pts) - 1) >= i: crypto_coin(c, x, y, 46, a, t + i)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        wallet(c, 820, 1080, 0.8 * lerp(1.5, 1, p), p)
        name_chip(c, 820, 1230, "THE HACKERS' WALLET", p, rgb=GOLD2, size=44)
    badge(c, 180, 1200, 0.6, a)

def sc_seized(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("seized", 1); b2 = B("seized", 2)
    pop_text(c, "SEIZED · JUNE 2021", CX, 430, ANTON, 90, CREAM, prog(t, 0, 0.25))
    text(c, "63.7", CX, 620, ANTON, 170, GOLD2, a, glow=22, glow_rgb=GOLD)
    text(c, "BITCOINS", CX, 700, BEBAS, 64, CREAM, a, spacing=6)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.6))
        c.drawRect(skia.Rect(140, 780, 940, 850), P(C((50, 52, 60), a)))
        c.drawRect(skia.Rect(140, 780, 140 + 800 * 0.85 * p, 850), P(C(GOLD2, a)))
        text(c, "~85% OF THE RANSOM", CX, 905, ANTON, 56, CREAM, a * p)
    if t > b2 - 0.3:
        p = eo(prog(t, b2 - 0.3, 0.3))
        CH.OFFICIAL.draw(c, 230, 1260, 0.75, 1, a=p, blink=bl(t), arm_f=(-40, -50))
        box(c, 640, 1060, 660, 170, p, "\"TODAY WE TURNED THE TABLES ON DARKSIDE\"", rgb=(40, 46, 60), size=40)
        name_chip(c, 640, 1200, "DEPUTY AG LISA MONACO (STYLISED)", p, size=32)

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("twist", 1)
    pop_text(c, "BITCOIN'S PRICE FELL", CX, 430, ANTON, 96, RED, prog(t, 0, 0.25), glow=14, glow_rgb=RED)
    price_chart(c, 140, 500, 800, 380, eo(prog(t, 0.2, 1.4)), a)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "$4.4M", 300, 1060, ANTON, 110, (140, 140, 140), p)
        c.drawLine(190, 1030, 410, 1030, P(C(RED, p), stroke=10))
        arrow(c, 440, 1030, 600, 1030, 1.0, p)
        counter(c, int(2.3e6 * eo(prog(t, b1, 0.8))), 790, 1070, 110, GOLD2, p, prefix="$", glow=18)
        text(c, "RECOVERED VALUE", 790, 1150, BEBAS, 46, CREAM, p, spacing=3)

def sc_quote(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("quote", 1)
    if t < b1 - 0.2:
        CH.OFFICIAL.draw(c, 250, 1250, 0.9, 1, a=a, blink=bl(t), arm_f=(-40, -50))
        name_chip(c, 640, 860, "FEDERAL PROSECUTOR, VIA AP (STYLISED)", a, rgb=GOLD2, size=30)
        for i, ln in enumerate(["\"THE EXTORTIONISTS", "WILL NEVER SEE", "THIS MONEY.\""]):
            text(c, ln, 640, 560 + i * 100, ANTON, 84, GOLD2 if i == 2 else CREAM, eo(prog(t, 0.4 + i * 0.4, 0.3)))
        wallet(c, 700, 1050, 0.7, a)
        ps = prog(t, W_("quote", "never") - 0.1, 0.22)
        if ps > 0: stamp(c, 700, 1050, "LOCKED", RED, 80, -6, ps, sc=lerp(2.2, 1, eo(ps)))
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        badge(c, CX, 960, 1.0, p)
        for i, ln in enumerate(["\"CUTTING OFF ACCESS", "TO REVENUE IS ONE OF", "THE MOST IMPACTFUL", "CONSEQUENCES WE CAN IMPOSE\""]):
            text(c, ln, CX, 470 + i * 84, ANTON, 70, GOLD2 if i == 3 else CREAM, eo(prog(t, b1 + i * 0.4, 0.3)))
        name_chip(c, CX, 1140, "FBI DEPUTY DIRECTOR PAUL ABBATE, VIA AP", p, rgb=GOLD2, size=34)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pipeline(c, 960, a, t, flow=1.0)
    for i in range(5): crypto_coin(c, 220 + i * 160, 830 + 16 * math.sin(t * 2 + i), 52, a, t + i)
    text(c, "?", CX, 1150, ANTON, 170, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "SHOULD PAYING RANSOMS", CX, 430, ANTON, 88, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "BE ALLOWED?", CX, 545, ANTON, 110, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 690)

E.DRAW = dict(hook=sc_hook, shutdown=sc_shutdown, fuel=sc_fuel, paid=sc_paid, wallet=sc_wallet, seized=sc_seized,
              twist=sc_twist, quote=sc_quote, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"shutdown"}
_IMP = [("hook", "back", -0.2, 0.45), ("shutdown", "shut", -0.1, 0.4), ("fuel", "stopped", -0.2, 0.4), ("rehook", "wallet", -0.2, 0.4),
        ("seized", "63.7", -0.2, 0.4), ("twist", "fallen", -0.2, 0.4), ("quote", "never", -0.1, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$4.4", 0.0), ("paid", "75", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
