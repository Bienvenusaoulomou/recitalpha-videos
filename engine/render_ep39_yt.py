import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep39")
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



ENVOY = CH.Char("office", dict(skin=(226, 190, 150), body=(34, 34, 40), sleeve=(32, 32, 38), legs=(28, 28, 34), shoe=(16, 14, 12),
                               hat=(0, 0, 0), hair=(24, 22, 22), accent=(170, 40, 40), accent2=(0, 0, 0)))
ITGUY = CH.OFFICIAL
DIPLO = CH.COLLEAGUE

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0

def hq_tower(c, x, y, s, a, t=0, lit=0.0, label="AU HEADQUARTERS"):
    """modern glass tower + low wing, base center (x, y)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-330, -170, 330, 0), P(C((70, 74, 80), a)))          # low wing
    c.drawRect(skia.Rect(-330, -170, 330, 0), P(C(INK, a), stroke=6))
    for i in range(10): c.drawRect(skia.Rect(-310 + i * 62, -140, -270 + i * 62, -40), P(C((120, 150, 170), a * 0.6)))
    c.drawRect(skia.Rect(-110, -760, 110, -160), P(C((60, 80, 100), a)))      # tower
    c.drawRect(skia.Rect(-110, -760, 110, -160), P(C(INK, a), stroke=6))
    rng = random.Random(7)
    for r in range(18):
        for k in range(4):
            on = lit > 0 and rng.random() < 0.2 + 0.6 * lit and (math.sin(t * 6 + r * 1.3 + k) > -0.2)
            col = (90, 255, 160) if on else (140, 170, 196)
            c.drawRect(skia.Rect(-94 + k * 48, -744 + r * 32, -60 + k * 48, -724 + r * 32), P(C(col, a * (0.9 if on else 0.45))))
    c.drawRect(skia.Rect(-14, -840, 14, -760), P(C((90, 90, 96), a)))
    c.restore()
    if label: text(c, label, x, y + 60 * s, BEBAS, 44, CREAM, a, spacing=4)

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

def mic(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-24, -60, 24, 20), 24, 24, P(C((180, 184, 190), a)))
    c.drawRoundRect(skia.Rect(-24, -60, 24, 20), 24, 24, P(C(INK, a), stroke=5))
    for i in range(3): c.drawLine(-18, -40 + i * 16, 18, -40 + i * 16, P(C(INK, a * 0.5), stroke=3))
    c.drawRect(skia.Rect(-4, 20, 4, 50), P(C(INK, a)))
    for k in range(3):
        rr = 40 + k * 22 + 10 * math.sin(t * 6 - k)
        c.drawArc(skia.Rect(-rr, -20 - rr, rr, -20 + rr), -60, 120, False, P(C(RED, a * (0.8 - k * 0.2)), stroke=5))
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

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    hq_tower(c, 330, 1150, 0.62, 1.0, t, lit=0.3 if t < b1 else 1.0, label="AU HEADQUARTERS")
    counter(c, 200000000, CX, 470, 112 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="$", glow=24)
    text(c, "A GIFT FROM CHINA", CX, 560, BEBAS, 62, CREAM, 1.0, spacing=6)
    pf = prog(t, W_("hook", "free.") - 0.3, 0.22)
    if pf > 0 and t < b1 - 0.2: stamp(c, 790, 760, "FREE", GOLD2, 110, -6, pf, sc=lerp(2.2, 1, eo(pf)))
    if t > b1 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        data_stream(c, 380, 780, 860, 900, t, p)
        pin(c, 860, 940, 1.0, p, label="SHANGHAI")
        ps = prog(t, W_("hook", "night.") - 0.3, 0.22)
        if ps > 0: stamp(c, 760, 700, "EVERY NIGHT", RED, 84, -5, ps, sc=lerp(2.2, 1, eo(ps)))
        text(c, "ACCORDING TO LE MONDE", 760, 1110, BEBAS, 40, CREAM, p * 0.85, spacing=3)

def sc_gift(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("gift", 1)
    pop_text(c, "ADDIS ABABA · 2012", CX, 440, ANTON, 96, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    hq_tower(c, 230 if t > B("gift", 1) - 0.3 else CX, 1170, 0.6, a, t, lit=0.2, label=None)
    if t > b1 - 0.3:
        for i, (w, lab) in enumerate([("built", "BUILT IT"), ("paid", "PAID FOR IT"), ("computer", "SET UP THE NETWORK")]):
            p = eo(prog(t, W_("gift", w) - 0.3, 0.3))
            box(c, 690, 640 + i * 125, 600, 100, p, "CHINA " + lab, rgb=(110, 30, 30), size=50)

def sc_peak(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("peak", 1)
    calendar(c, 170, 520, 0.6, a, "JAN", "2017")
    pop_text(c, "SOMETHING STRANGE", CX + 110, 480, ANTON, 72, CREAM, prog(t, 0.1, 0.25))
    ITGUY.draw(c, 220, 1240, 0.9, 1, a=a, blink=bl(t), brow=0.5, arm_f=(-70, -60))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        clock(c, 760, 680, 100, p, t_h=(0 + 2 * eo(prog(t, b1, 3.0))) % 12)
        text(c, "MIDNIGHT - 2 A.M.", 760, 840, BEBAS, 56, GOLD2, p, spacing=4)
        busy = eo(prog(t, W_("peak", "busy.") - 0.5, 0.3))
        for i in range(3): server(c, 600 + i * 160, 1210, 0.8, p, t + i, busy=busy)
        pb = prog(t, W_("peak", "busy.") - 0.4, 0.22)
        if pb > 0: stamp(c, 760, 980, "DATA PEAK", RED, 70, -5, pb, sc=lerp(2, 1, eo(pb)))

def sc_shanghai(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("shanghai", 1)
    server(c, 230, 900, 1.0, a, t, busy=1.0)
    text(c, "ADDIS ABABA", 230, 960, BEBAS, 48, CREAM, a, spacing=3)
    globe(c, 820, 780, 130, a, t)
    pin(c, 820, 720, 0.9, eo(prog(t, W_("shanghai", "Shanghai.") - 0.3, 0.3)), label="SHANGHAI")
    data_stream(c, 300, 660, 760, 700, t, a, n=12)
    pop_text(c, "TO SHANGHAI", CX, 450, ANTON, 120, RED, prog(t, W_("shanghai", "Shanghai.") - 0.3, 0.25))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3)); k = eo(prog(t, W_("shanghai", "2012") - 0.2, 1.6))
        x0, x1 = 200, 880
        c.drawRect(skia.Rect(x0, 1110, lerp(x0, x1, k), 1140), P(C(GOLD2, p)))
        for i in range(6):
            xx = lerp(x0, x1, i / 5)
            c.drawCircle(xx, 1125, 12, P(C(GOLD2 if k >= i / 5 else (90, 84, 70), p)))
            text(c, str(2012 + i), xx, 1200, BEBAS, 44, CREAM, p)
        text(c, "5 YEARS · REPORTED BY LE MONDE", CX, 1070, BEBAS, 46, GOLD2, p, spacing=3)

def sc_mics(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "HIDDEN MICROPHONES", CX, 440, ANTON, 92, RED, prog(t, W_("mics", "microphones") - 0.3, 0.25))
    text(c, "ACCORDING TO THE REPORT", CX, 540, BEBAS, 48, CREAM, a, spacing=4)
    # desk
    c.drawRect(skia.Rect(180, 980, 620, 1010), P(C((110, 76, 50), a)))
    c.drawRect(skia.Rect(200, 1010, 230, 1200), P(C((90, 62, 40), a))); c.drawRect(skia.Rect(570, 1010, 600, 1200), P(C((90, 62, 40), a)))
    pd = eo(prog(t, W_("mics", "desks") - 0.3, 0.3))
    mic(c, 400, 1080, 0.8, pd, t)
    text(c, "DESKS", 400, 1260, BEBAS, 54, GOLD2, pd, spacing=5)
    # wall
    c.drawRect(skia.Rect(700, 640, 930, 1200), P(C((80, 76, 70), a)))
    for r in range(9):
        for k in range(2):
            c.drawRect(skia.Rect(705 + k * 115 + (r % 2) * 55 - 55 * (r % 2) * k, 645 + r * 61, 815 + k * 115, 700 + r * 61), P(C(INK, a * 0.35), stroke=3))
    pw = eo(prog(t, W_("mics", "walls.") - 0.3, 0.3))
    mic(c, 815, 900, 0.9, pw, t)
    text(c, "WALLS", 815, 1260, BEBAS, 54, GOLD2, pw, spacing=5)

def sc_fix(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("fix", 1)
    pop_text(c, "THE AU'S RESPONSE", CX, 440, ANTON, 96, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    po = eo(prog(t, W_("fix", "own") - 0.3, 0.3))
    for i in range(2): server(c, 230 + i * 170, 960, 0.85, po, t + i, busy=0.3)
    text(c, "ITS OWN SERVERS", 315, 1020, BEBAS, 46, CREAM, po, spacing=3)
    pe = eo(prog(t, W_("fix", "encrypting") - 0.3, 0.3))
    lock(c, 790, 860, 1.0, pe)
    text(c, "ENCRYPTION", 790, 1020, BEBAS, 46, CREAM, pe, spacing=3)
    if t > b1 - 0.3:
        p = prog(t, b1 - 0.2, 0.22)
        stamp(c, CX, 680, "OFFER DECLINED", RED, 84, -5, p, sc=lerp(2.2, 1, eo(p)))
        text(c, "REPORTEDLY", CX, 780, BEBAS, 44, CREAM, eo(p), spacing=6)

def sc_denial(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("denial", 1)
    pd = prog(t, 0, 0.22)
    stamp(c, CX, 470, "CHINA DENIED IT", RED, 100, -4, pd, sc=lerp(2.2, 1, eo(pd)))
    ENVOY.draw(c, 300, 1240, 0.9, 1, a=a, blink=bl(t), brow=-0.3, arm_f=(-40, -60))
    text(c, "CHINA'S AMBASSADOR TO THE AU", CX, 640, BEBAS, 48, CREAM, eo(prog(t, b1 - 0.3, 0.3)), spacing=3)
    ps = eo(prog(t, W_("denial", "sensational,") - 0.3, 0.3))
    box(c, 740, 820, 460, 110, ps, "\"SENSATIONAL\"", rgb=(60, 30, 30), lab_rgb=GOLD2, size=64)
    pa = eo(prog(t, W_("denial", "absurd.") - 0.3, 0.3))
    box(c, 740, 970, 460, 110, pa, "\"ABSURD\"", rgb=(60, 30, 30), lab_rgb=GOLD2, size=64)
    text(c, "QUOTED BY AFP / FRANCE 24", 740, 1090, BEBAS, 36, CREAM, pa * 0.8, spacing=2)

def sc_diplomat(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "ONE AFRICAN DIPLOMAT", CX, 440, ANTON, 92, CREAM, prog(t, 0, 0.25))
    text(c, "TO LE MONDE", CX, 530, BEBAS, 52, GOLD2, a, spacing=6)
    DIPLO.draw(c, 250, 1240, 0.9, 1, a=a, blink=bl(t), arm_f=(-60, -70))
    pq = eo(prog(t, W_("diplomat", "at") - 0.3, 0.3))
    if pq > 0:
        r = skia.RRect.MakeRectXY(skia.Rect(400, 660, 1000, 960), 30, 30)
        c.drawRRect(r, P(C(CREAM, pq))); c.drawRRect(r, P(C(INK, pq), stroke=6))
        tri = skia.Path(); tri.moveTo(440, 930); tri.lineTo(360, 1010); tri.lineTo(500, 950); tri.close()
        c.drawPath(tri, P(C(CREAM, pq)))
        text(c, "\"AT LEAST THEY", 700, 760, ANTON, 72, INK, pq)
        text(c, "NEVER COLONIZED US\"", 700, 860, ANTON, 64, RED, eo(prog(t, W_("diplomat", "colonized") - 0.3, 0.3)))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    hq_tower(c, CX, 1130, 0.5, a, t, lit=0.6, label=None)
    stamp(c, CX + 170, 820, "FREE?", GOLD2, 70, -8, a)
    pop_text(c, "A FREE BUILDING", CX, 430, ANTON, 100, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "FROM A FOREIGN POWER?", CX, 545, ANTON, 92, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1200)

E.DRAW = dict(hook=sc_hook, gift=sc_gift, peak=sc_peak, shanghai=sc_shanghai, mics=sc_mics, fix=sc_fix, denial=sc_denial,
              diplomat=sc_diplomat, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"mics"}
_IMP = [("hook", "night.", -0.3, 0.45), ("gift", "paid", -0.3, 0.3), ("peak", "busy.", -0.4, 0.4), ("shanghai", "Shanghai.", -0.3, 0.4),
        ("rehook", "ears.", -0.2, 0.4), ("mics", "walls.", -0.3, 0.35), ("fix", "turned", -0.3, 0.35), ("denial", "absurd.", -0.3, 0.4),
        ("diplomat", "colonized", -0.3, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = []
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
