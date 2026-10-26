import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep12")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999

PH = dict(tino=load_photo("oil_01.png"))
CR = "PHOTO: 1963 · PUBLIC DOMAIN"

def tanks3(c, t, a, xr, y=1000, s=0.74, label="SALAD OIL"):
    for i, x in enumerate((CX - 320, CX, CX + 320)):
        oil_tank(c, x, y, s, a, level=0.92, water=0.94, t=t + i, label=label, xray=xr)

def chart(c, x0, y0, w, h, k, a, crash_at=0.6):
    pts = []
    n = 40
    for i in range(int(n * k) + 1):
        f = i / n
        v = 0.75 + 0.06 * math.sin(i * 1.3) if f < crash_at else 0.75 - (f - crash_at) / (1 - crash_at) * 0.6 + 0.03 * math.sin(i * 2)
        pts.append((x0 + f * w, y0 + h - v * h))
    if len(pts) > 1:
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        c.drawPath(p, P(C(RED if k > crash_at else GOLD2, a), stroke=10))
    c.drawLine(x0, y0 + h, x0 + w, y0 + h, P(C(MUTED, a), stroke=3)); c.drawLine(x0, y0, x0, y0 + h, P(C(MUTED, a), stroke=3))

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    xr = eo(prog(t, W_("hook", "water.") - 0.7, 0.6))
    tanks3(c, t, 1.0, xr)
    counter(c, 150000000, CX, 470, 130, GOLD2, 1.0, suffix="+", glow=22)
    text(c, "BORROWED AGAINST SALAD OIL", CX, 560, BEBAS, 58, CREAM, 1.0, spacing=5)
    pw = prog(t, W_("hook", "water.") - 0.1, 0.22)
    if pw > 0: stamp(c, CX, 1150, "FULL OF WATER", RED, 110, -5, pw, sc=lerp(2.2, 1, eo(pw)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["tino"], CX, 740, 520, 700, t / D, a, 1.0, 1.12, focus=(0.5, 0.25), rot=-1.5, credit=CR)
    pop_text(c, "TINO DE ANGELIS", CX, 340, ANTON, 110, CREAM, prog(t, W_("who", "Tino") - 0.1, 0.25))
    pill(c, "ALLIED CRUDE VEGETABLE OIL", 1170, eo(prog(t, W_("who", "giant") - 0.2, 0.3)), GOLD2, 56, 860)

def sc_receipts(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("receipts", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        tanks3(c, t, a, 0, y=1050)
        person(c, CX + 380, 600, 60, CREAM, eo(prog(t, W_("receipts", "inspectors") - 0.2, 0.3)))
        chip(c, "INSPECTORS", CX + 260, 470, eo(prog(t, W_("receipts", "inspectors") - 0.2, 0.3)))
        pop_text(c, "AMERICAN EXPRESS", CX - 120, 420, ANTON, 80, GOLD2, prog(t, W_("receipts", "American") - 0.1, 0.25))
        c.restore(); c.restore()
    if out > 0:
        ticket(c, CX, 640, 0.95, out, rot=-3, head="WAREHOUSE RECEIPT", title="SALAD OIL · 1,000 TONS", sub="INSPECTED")
        pb = eo(prog(t, W_("receipts", "banks") - 0.2, 0.3))
        building(c, CX, 1230, 0.5, pb, "BANK")
        for i in range(4):
            bills(c, CX - 300 + i * 200, lerp(1150, 980, eo(clamp((t - W_("receipts", "lent") ) * 1.5 - i * 0.2))), pb, 2, rot=(i - 2) * 6)

def sc_trick(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("trick", 1)
    pop_text(c, "OIL FLOATS ON WATER", CX, 380, ANTON, 104, GOLD2, prog(t, 0.05, 0.25), glow=18, glow_rgb=GOLD)
    xr = eo(prog(t, b1 - 0.3, 0.6))
    oil_tank(c, CX - 160, 1150, 1.6, a, level=0.92, water=0.95, t=t, label="SALAD OIL", xray=xr)
    if xr > 0.5:
        text(c, "WATER", CX - 160, 960, ANTON, 90, CREAM, xr)
        text(c, "OIL", CX + 160, 670, ANTON, 64, GOLD2, xr, align="l")
        c.drawLine(CX + 150, 650, CX + 60, 650, P(C(GOLD2, xr), stroke=5))
    ph = eo(prog(t, W_("trick", "hatch,") - 0.3, 0.35))
    if ph > 0:
        # hatch view: top-down circle full of oil
        c.drawCircle(CX + 300, 900, 150, P(C((40, 38, 36), ph)))
        c.drawCircle(CX + 300, 900, 130, P(C((222, 176, 60), ph)))
        c.drawCircle(CX + 300, 900, 150, P(C(GOLD, ph), stroke=8))
        text(c, "WHAT INSPECTORS SAW", CX + 300, 1110, BEBAS, 40, CREAM, ph, spacing=3)

def sc_pipes(c, t, D):
    a = eo(prog(t, 0, 0.3))
    xs = [190, 420, 660, 890]
    for i, x in enumerate(xs):
        oil_tank(c, x, 1000, 0.48, a, level=0.9, water=1.0, t=t + i, label=None, xray=1.0)
    c.drawLine(xs[0], 1020, xs[-1], 1020, P(C((120, 120, 116), a), stroke=22))
    for x in xs: c.drawLine(x, 990, x, 1020, P(C((120, 120, 116), a), stroke=22))
    k = clamp(t / max(1.0, D - 0.4)) * 3.999
    i = int(k); f = k - i
    bx = lerp(xs[i], xs[min(3, i + 1)], eio(f)) if i < 3 else xs[3]
    g = P(C((240, 190, 70), a)); c.drawCircle(bx, 1020, 26, g)
    for j in range(min(4, i + 1)):
        pop_text(c, "COUNTED x%d" % (j + 1), xs[j], 760, BEBAS, 46, GOLD2, prog(t, j * D / 4.2, 0.25))
    pop_text(c, "THE SAME OIL", CX, 420, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    pop_text(c, "AGAIN AND AGAIN", CX, 560, ANTON, 96, RED, prog(t, W_("pipes", "again") - 0.2, 0.25), glow=16, glow_rgb=RED)

def sc_numbers(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("numbers", 1)
    k1 = eo(prog(t, W_("numbers", "about") - 0.2, 1.0))
    k2 = eo(prog(t, b1 + 0.3, 0.8))
    base = 1150
    c.drawRect(skia.Rect(200, base - 640 * k1, 480, base), P(C(GOLD2, a)))
    c.drawRect(skia.Rect(600, base - 640 * 0.061 * k2, 880, base), P(C(RED, eo(prog(t, b1, 0.3)))))
    text(c, "CLAIMED", 340, base + 70, BEBAS, 54, CREAM, a, spacing=4)
    text(c, "REAL", 740, base + 70, BEBAS, 54, CREAM, eo(prog(t, b1, 0.3)), spacing=4)
    counter(c, 900000 * k1, 340, base - 640 * k1 - 30, 70, GOLD2, a, prefix="", suffix=" T")
    counter(c, 55000 * k2, 740, base - 640 * 0.061 * k2 - 30, 70, RED, eo(prog(t, b1, 0.3)), prefix="", suffix=" T")
    pop_text(c, "TONS OF OIL", CX, 380, ANTON, 104, CREAM, prog(t, 0.05, 0.25))

def sc_crash(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("crash", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        news(c, CX, 760, 1.25 * lerp(0.7, 1, back(a)), -3, a * (1 - out), "EXTRA!", "SALAD OIL GIANT GOES BUST", "NOVEMBER 1963")
        pb = prog(t, W_("crash", "bankrupt,") - 0.2, 0.25)
        if pb > 0: stamp(c, CX, 1100, "BANKRUPT", RED, 120, -6, pb * (1 - out), sc=lerp(2, 1, eo(pb)))
    if out > 0:
        tilt = eo(prog(t, W_("crash", "down") - 0.3, 0.8))
        c.save(); c.translate(CX + 300, 1200); c.rotate(-25 * tilt); c.translate(-(CX + 300), -1200)
        building(c, CX, 1200, 0.9, out, "WALL ST. BROKER", cols=6)
        c.restore()
        pop_text(c, "WENT DOWN WITH IT", CX, 400, ANTON, 104, RED, prog(t, W_("crash", "down") - 0.2, 0.25), glow=16, glow_rgb=RED)

def sc_amex(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("amex", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    chart(c, 150, 520, 780, 520, clamp(t / max(0.6, b1 - 0.2)), a * (1 - out * 0.7))
    pop_text(c, "AMERICAN EXPRESS STOCK", CX, 400, ANTON, 84, CREAM, prog(t, 0.05, 0.25) * (1 - out))
    if out > 0:
        pop_text(c, "WARREN BUFFETT", CX, 400, ANTON, 120, GOLD2, prog(t, W_("amex", "Warren") - 0.1, 0.25), glow=20, glow_rgb=GOLD)
        pb = prog(t, W_("amex", "bargain:") - 0.2, 0.25)
        if pb > 0: stamp(c, CX, 780, "BUYS", GOLD2, 150, -8, pb, sc=lerp(2, 1, eo(pb)))
        pill(c, "ONE OF HIS BEST DEALS EVER", 1160, eo(prog(t, W_("amex", "best") - 0.2, 0.3)), CREAM, 58, 860)

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3))
    bars(c, a, y0=330, y1=1240)
    pt = prog(t, W_("verdict", "20") - 0.15, 0.25)
    po = prog(t, W_("verdict", "out") - 0.15, 0.25)
    if pt > 0: stamp(c, CX, 680, "20 YEARS", RED, 150, -6, pt, sc=lerp(2.2, 1, eo(pt)))
    if po > 0: stamp(c, CX, 960, "OUT AFTER 7", GOLD2, 110, 5, po, sc=lerp(2.2, 1, eo(po)))

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    clock(c, CX - 230, 820, 150, a, 9.75 + t * 0.05)
    plane(c, lerp(-200, W + 200, (t / max(1, D)) % 1), 560, 0.6, a)
    pk = prog(t, W_("cta", "memorized") - 0.2, 0.25)
    pop_text(c, "HE MEMORIZED", CX + 200, 760, ANTON, 72, CREAM, pk)
    pop_text(c, "THE SOUNDS", CX + 200, 850, ANTON, 72, GOLD2, pk)
    pm = prog(t, W_("cta", "Machine") - 0.15, 0.25)
    if pm > 0: stamp(c, CX, 1110, "MACHINE GUN KELLY", RED, 90, -4, pm, sc=lerp(2, 1, eo(pm)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    tanks3(c, t, 1.0, 1.0)
    pop_text(c, "TANKS OF WATER", CX, 420, ANTON, 120, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "A FORTUNE ON PAPER", CX, 560, ANTON, 96, GOLD2, prog(t, W_("loopend", "fortune") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    pop_text(c, "BECAUSE...", CX, 1170, ANTON, 110, GOLD2, prog(t, beat("loopend", 1) - 0.1, 0.25), glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, who=sc_who, receipts=sc_receipts, trick=sc_trick, pipes=sc_pipes, numbers=sc_numbers,
              crash=sc_crash, amex=sc_amex, verdict=sc_verdict, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"crash", "verdict"}
_IMP = [("hook", "water.", -0.1, 0.4), ("who", "Tino", -0.1, 0.3), ("receipts", "banks", -0.2, 0.3),
        ("rehook", "wasn't", -0.1, 0.35), ("trick", "hatch,", -0.3, 0.3), ("numbers", "real", -0.1, 0.35),
        ("crash", "bankrupt,", -0.2, 0.4), ("amex", "crashed.", -0.2, 0.35), ("amex", "bargain:", -0.2, 0.3),
        ("verdict", "20", -0.15, 0.4), ("cta", "Machine", -0.15, 0.3), ("loopend", "Tanks", -0.05, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("receipts", "lent", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
