import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep49")
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
def talk(t, k=1.0): return k * max(0.0, math.sin(t * 13)) * 0.8
def house(c, x, y, s, a, rgb=(150, 120, 90), roof=(120, 50, 40)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-110, -150, 110, 0), P(C(rgb, a))); c.drawRect(skia.Rect(-110, -150, 110, 0), P(C(INK, a), stroke=6))
    p = skia.Path(); p.moveTo(-140, -150); p.lineTo(0, -260); p.lineTo(140, -150); p.close()
    c.drawPath(p, P(C(roof, a))); c.drawPath(p, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-25, -80, 25, 0), P(C(INK, a)))
    for dx in (-70, 70): c.drawRect(skia.Rect(dx - 22, -120, dx + 22, -80), P(C((250, 220, 140), a)))
    c.restore()

def person_icon(c, x, y, s, a, rgb=CREAM):
    if a <= 0: return
    c.drawCircle(x, y - 70 * s, 26 * s, P(C(rgb, a)))
    c.drawRoundRect(skia.Rect(x - 36 * s, y - 38 * s, x + 36 * s, y + 40 * s), 24 * s, 24 * s, P(C(rgb, a)))

def server_rack(c, x, y, s, a, t=0, rgb=(36, 40, 50)):
    """rack, base center (x,y)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-110, -520, 110, 0), 10, 10, P(C(rgb, a))); c.drawRoundRect(skia.Rect(-110, -520, 110, 0), 10, 10, P(C(INK, a), stroke=6))
    for k in range(9):
        yy = -490 + k * 54
        c.drawRect(skia.Rect(-90, yy, 90, yy + 40), P(C((22, 26, 34), a)))
        for j in range(3):
            on = (math.sin(t * (5 + j) + k * 1.7 + j + x * 0.01) > 0)
            c.drawCircle(50 + j * 14, yy + 20, 4.5, P(C(GREEN if on else (40, 80, 60), a)))
        c.drawRect(skia.Rect(-80, yy + 16, 10, yy + 24), P(C((60, 66, 80), a)))
    c.restore()

def gpu_chip(c, x, y, s, a, glow=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(5):
        for sx, sy in ((-70, 0), (70, 0)):
            pass
        c.drawRect(skia.Rect(-60 + k * 28, -78, -52 + k * 28, -60), P(C(GOLD, a))); c.drawRect(skia.Rect(-60 + k * 28, 60, -52 + k * 28, 78), P(C(GOLD, a)))
        c.drawRect(skia.Rect(-78, -60 + k * 28, -60, -52 + k * 28), P(C(GOLD, a))); c.drawRect(skia.Rect(60, -60 + k * 28, 78, -52 + k * 28), P(C(GOLD, a)))
    c.drawRoundRect(skia.Rect(-62, -62, 62, 62), 10, 10, P(C((30, 34, 40), a)))
    c.drawRoundRect(skia.Rect(-62, -62, 62, 62), 10, 10, P(C(GOLD2, a), stroke=5))
    text(c, "AI", 0, 18, ANTON, 52, GREEN if glow > 0.5 else GOLD2, a)
    c.restore()

def steam(c, x, y, a, t, n=4):
    for k in range(n):
        f = (t * 0.5 + k / n) % 1.0
        c.drawCircle(x + 20 * math.sin(f * 6 + k), y - f * 260, 24 + f * 50, P(C((220, 220, 214), a * 0.45 * (1 - f))))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    pg = eo(prog(t, b1 - 0.3, 0.3))
    text(c, "ALMOST 1 IN 5 PEOPLE ON EARTH", CX, 430, ANTON, 72, CREAM, 1.0)
    text(c, "LIVES IN AFRICA", CX, 520, BEBAS, 64, GOLD, 1.0, spacing=5)
    for i in range(10):
        x = 120 + i * 93; gold = i < 2
        person_icon(c, x, 760 - (8 * math.sin(t * 4 + i) if gold else 0), 1.0, 1.0 - 0.6 * pg, GOLD2 if gold else (110, 104, 92))
    if pg > 0:
        pie(c, CX - 170, 980, 150, 0.01, pg, rgb=RED)
        text(c, "<1%", CX + 190, 1020, ANTON, 150, RED, pg, glow=14, glow_rgb=RED)
        text(c, "OF THE WORLD'S DATA CENTRE CAPACITY", CX, 1215, BEBAS, 54, CREAM, pg, spacing=2)
    else:
        globe(c, CX, 1040, 180, 1.0, t)

def sc_why(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("why", 1)
    pop_text(c, "A DATA CENTRE", CX, 450, ANTON, 96, CREAM, prog(t, 0, 0.25))
    for i in range(5):
        server_rack(c, 150 + i * 195, 1240, 0.95, eo(prog(t, 0.15 + i * 0.12, 0.3)) * (1 - 0.6 * eo(prog(t, b1 - 0.3, 0.3))), t)
    pa = eo(prog(t, W_("why", "artificial") - 0.2, 0.3)) * (1 - eo(prog(t, b1 - 0.3, 0.3)))
    if pa > 0: box(c, CX, 600, 560, 110, pa, "WHERE AI LIVES", rgb=(40, 46, 60), lab_rgb=GOLD2, size=64)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "NO DATA CENTRES", CX, 640, ANTON, 104, RED, p, glow=12, glow_rgb=RED)
        text(c, "NO AI OF YOUR OWN", CX, 780, ANTON, 104, GOLD2, eo(prog(t, W_("why", "AI") - 0.2, 0.3)), glow=18, glow_rgb=GOLD)

def sc_kenya(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("kenya", 1); b2 = B("kenya", 2)
    if t < b1 - 0.2:
        pop_text(c, "THE MONEY ARRIVES", CX, 450, ANTON, 96, CREAM, prog(t, 0, 0.25))
        for i in range(8):
            f = ((t * 0.5 + i / 8) % 1.0)
            bills(c, lerp(-60, W + 60, f), 750 + 160 * math.sin(i * 1.7) - 60 * math.sin(f * math.pi), a, 2, rot=f * 120 + i * 20)
        globe(c, CX, 1060, 170, a, t)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        calendar(c, 190, 560, 0.5, p, "22", "MAY 2024")
        box(c, 560, 470, 340, 100, p, "MICROSOFT", rgb=(40, 46, 60), size=56)
        text(c, "+", 770, 490, ANTON, 80, GOLD2, p)
        box(c, 900, 470, 200, 100, p, "G42", rgb=(40, 46, 60), size=56)
        pm = eo(prog(t, W_("kenya", "$1") - 0.2, 0.3))
        text(c, "$1 BILLION", 730, 650, ANTON, 120, GOLD2, pm, glow=20, glow_rgb=GOLD)
        pk = eo(prog(t, W_("kenya", "Kenya") - 0.2, 0.3))
        mountains(c, pk, y=1240, t=t)
        pin(c, 300, 1000, 0.9, pk, label="KENYA")
        if t > b2 - 0.3:
            pg = eo(prog(t, b2 - 0.3, 0.3))
            for i in range(3): server_rack(c, 640 + i * 150, 1240, 0.62, pg, t)
            for i in range(3): steam(c, 520 + i * 180, 1180, pg, t + i)
            text(c, "GEOTHERMAL POWER", CX, 800, BEBAS, 62, CREAM, pg, spacing=4)

def sc_gpus(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("gpus", 1)
    pop_text(c, "CASSAVA + NVIDIA", CX, 440, ANTON, 92, CREAM, prog(t, 0, 0.25))
    pm = eo(prog(t, W_("gpus", "$720") - 0.3, 0.3))
    text(c, "UP TO $720 MILLION", CX, 560, ANTON, 90, GOLD2, pm, glow=18, glow_rgb=GOLD)
    gpu_chip(c, CX, 860, 1.6, a * (1 - eo(prog(t, b1 - 0.3, 0.3))), glow=1.0 if int(t * 2) % 2 else 0.0)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3)); k = eo(prog(t, b1, 2.0))
        n = int(24 * k)
        for i in range(24):
            if i < n: gpu_chip(c, 150 + (i % 8) * 112, 700 + (i // 8) * 115, 0.62, p, glow=1.0 if (int(t * 4) + i) % 5 == 0 else 0.0)
        counter(c, int(12000 * k), CX, 1100, 110, GREEN, p, prefix="", suffix=" AI CHIPS")
        text(c, "5 COUNTRIES · 3 TO 4 YEARS", CX, 1200, BEBAS, 56, CREAM, eo(prog(t, W_("gpus", "five") - 0.2, 0.3)), spacing=3)

def sc_slow(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("slow", 1)
    pop_text(c, "BIG ANNOUNCEMENTS", CX, 450, ANTON, 92, CREAM, prog(t, 0, 0.25))
    text(c, "TAKE TIME", CX, 560, ANTON, 92, GOLD2, eo(prog(t, 0.4, 0.3)))
    clock(c, 300, 900, 150, a, t_h=9 + t * 2)
    pin(c, 760, 1000, 0.8, a, label="KENYA")
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "2026", 760, 780, ANTON, 110, CREAM, p)
        ps = prog(t, W_("slow", "negotiated") - 0.2, 0.22)
        if ps > 0: stamp(c, CX, 1170, "STILL BEING NEGOTIATED", RED, 70, -4, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_views(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("views", 1)
    scales(c, CX, 1080, 0.55, a, tilt=0.5 * math.sin(t * 1.2))
    CH.EMPLOYEE.draw(c, 200, 1250, 0.8, 1, a=a, blink=bl(t), mouth=talk(t) if t < b1 else 0, arm_f=(-80, -30))
    text(c, "SUPPORTERS", 290, 430, ANTON, 70, (90, 255, 160), a)
    for i, w in enumerate(["SKILLS", "JOBS", "POWER"]):
        text(c, w, 290, 520 + i * 70, BEBAS, 62, CREAM, eo(prog(t, W_("views", w.lower()) - 0.2, 0.3)), spacing=4)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        CH.RECRUITER.draw(c, 880, 1250, 0.8, -1, a=p, blink=bl(t + 1), brow=-0.5, mouth=talk(t), arm_f=(-80, -30))
        text(c, "CRITICS", 790, 430, ANTON, 70, RED, p)
        for i, w in enumerate(["WHO CONTROLS", "AFRICA'S", "DATA?"]):
            text(c, w, 790, 520 + i * 70, BEBAS, 62, CREAM, eo(prog(t, b1 + 0.4 + i * 0.4, 0.3)), spacing=3)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i in range(4): server_rack(c, 200 + i * 230, 1240, 0.55, a, t)
    text(c, "?", CX, 1000, ANTON, 170, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "BUILD ITS OWN AI", CX, 430, ANTON, 100, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "OR RENT IT?", CX, 545, ANTON, 110, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 690)

def pie(c, x, y, r, frac, a, rgb=RED):
    c.drawCircle(x, y, r, P(C((60, 56, 48), a)))
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, 360 * frac, False); p.close()
    c.drawPath(p, P(C(rgb, a))); c.drawCircle(x, y, r, P(C(CREAM, a), stroke=5))

E.DRAW = dict(hook=sc_hook, why=sc_why, kenya=sc_kenya, gpus=sc_gpus, slow=sc_slow, views=sc_views,
              question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = set()
_IMP = [("hook", "1%", -0.1, 0.45), ("why", "AI", -0.1, 0.4), ("kenya", "$1", -0.1, 0.4),
        ("slow", "negotiated", -0.1, 0.4), ("rehook", "question", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("kenya", "$1", 0.0), ("gpus", "$720", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
