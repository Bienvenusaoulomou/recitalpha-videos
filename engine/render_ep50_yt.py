import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep50")
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


def badge(c, x, y, s, a, label="FBI"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    for k in range(10):
        r = 130 if k % 2 == 0 else 90; ang = -math.pi / 2 + k * math.pi / 5
        (p.moveTo if k == 0 else p.lineTo)(r * math.cos(ang), r * math.sin(ang))
    p.close(); c.drawPath(p, P(C(GOLD2, a))); c.drawPath(p, P(C(INK, a), stroke=6))
    text(c, label, 0, 16, ANTON, 54 if len(label) <= 3 else 36, INK, a)
    c.restore()

def smartphone(c, x, y, s, a, t=0, caller="IT SUPPORT", ring=0.0, rgb=(28, 30, 36), sub="INCOMING CALL"):
    if a <= 0: return
    c.save(); c.translate(x + ring * 5 * math.sin(t * 55), y); c.rotate(ring * 3 * math.sin(t * 40)); c.scale(s, s)
    sh = P(C((0, 0, 0), 0.5 * a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawRoundRect(skia.Rect(-150, -280, 150, 280), 40, 40, sh)
    c.drawRoundRect(skia.Rect(-150, -280, 150, 280), 40, 40, P(C(rgb, a)))
    c.drawRoundRect(skia.Rect(-150, -280, 150, 280), 40, 40, P(C(GOLD, a * 0.7), stroke=5))
    c.drawRoundRect(skia.Rect(-130, -250, 130, 250), 26, 26, P(C((16, 22, 34), a)))
    text(c, sub, 0, -170, BEBAS, 34, (170, 180, 200), a, spacing=2)
    c.drawCircle(0, -70, 58, P(C((60, 120, 200), a)))
    text(c, "IT", 0, -52, ANTON, 50, CREAM, a)
    text(c, caller, 0, 40, ANTON, 44, CREAM, a)
    c.drawCircle(-70, 170, 40, P(C((210, 60, 60), a))); c.drawCircle(70, 170, 40, P(C((60, 190, 100), a)))
    if ring > 0:
        for k in range(3):
            rr = 180 + k * 40 + (t * 120) % 40
            arc = skia.Path(); arc.addArc(skia.Rect(-rr, -rr - 60, rr, rr - 60), -60, 120)
            c.drawPath(arc, P(C(GOLD2, a * ring * (1 - k / 3) * 0.7), stroke=6))
            arc = skia.Path(); arc.addArc(skia.Rect(-rr, -rr - 60, rr, rr - 60), 120, 120)
            c.drawPath(arc, P(C(GOLD2, a * ring * (1 - k / 3) * 0.7), stroke=6))
    c.restore()

def wave(c, x0, x1, y, a, t, amp=60, rgb=GREEN):
    if a <= 0: return
    n = 38
    for i in range(n):
        xx = lerp(x0, x1, i / (n - 1))
        h = amp * (0.25 + 0.75 * abs(math.sin(t * 7 + i * 0.7) * math.sin(i * 0.33 + t * 2)))
        c.drawRoundRect(skia.Rect(xx - 7, y - h, xx + 7, y + h), 7, 7, P(C(rgb, a)))

def dossier(c, x, y, s, a, rot, title, rows, k=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-220, -280, 220, 280), 12, 12, P(C((214, 196, 150), a)))
    c.drawRoundRect(skia.Rect(-220, -280, 220, 280), 12, 12, P(C(INK, a), stroke=5))
    text(c, title, 0, -210, ANTON, 52, INK, a)
    for i, r in enumerate(rows):
        aa = a * clamp(k * len(rows) - i)
        text(c, r, -180, -110 + i * 90, BEBAS, 54, INK, aa, align="l", spacing=2)
        c.drawLine(-180, -95 + i * 90, 180, -95 + i * 90, P(C(INK, aa * 0.3), stroke=2))
    c.restore()

def cash_stack(c, x, y, s, a, n=5):
    for i in range(n): bills(c, x + (i % 2) * 14 * s, y - i * 26 * s, a, n=1, rot=(-4 if i % 2 else 3))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    pop_text(c, "\"HI, IT SUPPORT HERE\"", CX, 430, ANTON, 92, CREAM, 1.0)
    smartphone(c, 760, 900, 0.95, 1.0, t, ring=1.0 if t < b1 else 0.3)
    CH.HACKER.draw(c, 260, 1250, 0.9, 1, a=1.0, arm_f=(-150 + 6 * math.sin(t * 5), 30))
    if t > b1 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        c.drawRect(skia.Rect(0, 500, W, 640), P(C((10, 10, 12), 0.75 * p)))
        counter(c, int(40e6 * eo(prog(t, b1, 1.0))), CX, 610, 120, GOLD2, p, prefix="$", glow=22)

def sc_police(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("police", 1)
    pop_text(c, "UKRAINE + FBI", CX, 430, ANTON, 110, CREAM, prog(t, 0, 0.25))
    badge(c, 300, 690, 0.95, a, "POLICE")
    badge(c, 780, 690, 0.95, a, "FBI")
    text(c, "+", CX, 720, ANTON, 120, GOLD2, a)
    k = eo(prog(t, 1.0, 2.5))
    box(c, CX, 880, 700, 110, a * k * (1 - eo(prog(t, b1 - 0.4, 0.3))), "2-YEAR INVESTIGATION", rgb=(40, 46, 60), size=56)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        for i in range(4):
            CH.HACKER.draw(c, 190 + i * 235, 1260, 0.62, 1 if i < 2 else -1, a=p, blink=bl(t + i), arm_f=(-20, -30))
        ps = prog(t, W_("police", "arrested") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 1060, "4 ARRESTED", RED, 100, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_study(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("study", 1)
    pop_text(c, "STEP 1: STUDY THE TARGET", CX, 430, ANTON, 80, CREAM, prog(t, 0, 0.25))
    building(c, 240, 1150, 0.7, a, label="COMPANY")
    dossier(c, 690, 800, 0.8, a, 4, "TARGET FILE", ["MONEY", "STAFF", "WEAK SPOTS"], k=eo(prog(t, b1 - 0.2, 1.8)))
    CH.HACKER.draw(c, 930, 1260, 0.55, -1, a=a, arm_f=(-70, -40))

def sc_call(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("call", 1)
    if t < b1 - 0.2:
        pop_text(c, "STEP 2: THE CALL", CX, 430, ANTON, 100, CREAM, prog(t, 0, 0.25))
        CH.EMPLOYEE.draw(c, 300, 1250, 0.95, 1, a=a, blink=bl(t), brow=0.3, arm_f=(-140, 40))
        smartphone(c, 760, 860, 0.85, a, t, ring=1.0)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        pop_text(c, "AI-GENERATED VOICES", CX, 430, ANTON, 92, GREEN, prog(t, b1 - 0.2, 0.25), glow=14, glow_rgb=GREEN)
        laptop(c, CX, 900, 0.95, p, t, label="VOICE PLATFORM")
        wave(c, 140, 740, 1130, p, t, amp=50)
        CH.HACKER.draw(c, 900, 1270, 0.55, -1, a=p, arm_f=(-60, -60))

def sc_access(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("access", 1)
    pop_text(c, "STEP 3: GET INSIDE", CX, 430, ANTON, 96, CREAM, prog(t, 0, 0.25))
    if t < b1 - 0.2:
        CH.EMPLOYEE.draw(c, 260, 1250, 0.9, 1, a=a, blink=bl(t), arm_f=(-60, -40))
        laptop(c, 700, 1050, 0.8, a, t, label="PASSWORD: ****")
        ps = prog(t, W_("access", "remote") - 0.1, 0.3)
        if ps > 0: box(c, 700, 760, 600, 110, eo(ps), "REMOTE ACCESS: ON", rgb=(120, 40, 40), size=52)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        CH.HACKER.draw(c, 220, 1250, 0.8, 1, a=p, arm_f=(-150, 30))
        smartphone(c, 230, 760, 0.5, p, t, sub="ON THE LINE", caller="TALKING...")
        CH.HACKER.draw(c, 820, 1250, 0.8, -1, a=p, arm_f=(-60, -60))
        laptop(c, 680, 1080, 0.6, p, t, label="IN", rgb=RED)
        ps = prog(t, W_("access", "broke") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 860, "BROKE IN", RED, 100, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_ransom(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("ransom", 1); b2 = B("ransom", 2)
    if t < b1 - 0.2:
        pop_text(c, "DATA STOLEN · FILES LOCKED", CX, 430, ANTON, 76, RED, prog(t, 0, 0.25), glow=12, glow_rgb=RED)
        laptop(c, CX, 900, 1.0, a, t, label="LOCKED", rgb=RED)
        for i in range(5): crypto_coin(c, 180 + i * 180, 1180 + 14 * math.sin(t * 3 + i), 50, a, t + i)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        pop_text(c, "ONE U.S. COMPANY", CX, 430, ANTON, 100, CREAM, prog(t, b1 - 0.2, 0.25))
        text(c, "ASKED", 300, 600, BEBAS, 64, CREAM, p, spacing=4)
        text(c, "$10M", 300, 760, ANTON, 150, (150, 150, 150) if t > b2 else GOLD2, p, glow=0 if t > b2 else 18, glow_rgb=GOLD)
        if t > b2 - 0.2:
            q = eo(prog(t, b2 - 0.2, 0.3))
            c.drawLine(160, 710, 440, 710, P(C(RED, q), stroke=12))
            arrow(c, 470, 710, 600, 710, 1.0, q)
            text(c, "PAID", 800, 600, BEBAS, 64, CREAM, q, spacing=4)
            text(c, "$5M", 800, 760, ANTON, 150, GOLD2, q, glow=18, glow_rgb=GOLD)
        building(c, CX, 1230, 0.7, p, label="COMPANY")

def sc_total(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("total", 1)
    pop_text(c, "AT LEAST 28 COMPANIES", CX, 430, ANTON, 90, CREAM, prog(t, 0, 0.25))
    n = int(28 * eo(prog(t, 0.2, 1.6)))
    for i in range(n):
        x = 150 + (i % 7) * 130; y = 540 + (i // 7) * 90
        c.drawRect(skia.Rect(x - 40, y - 34, x + 40, y + 34), P(C((70, 76, 90), a)))
        c.drawRect(skia.Rect(x - 40, y - 34, x + 40, y + 34), P(C(INK, a), stroke=4))
        for q in range(3): c.drawRect(skia.Rect(x - 28 + q * 22, y - 20, x - 16 + q * 22, y - 4), P(C(GOLD2, a * 0.8)))
    counter(c, int(40.5e6 * eo(prog(t, 0.6, 2.4))), CX, 1000, 130, GOLD2, a, prefix="$", glow=22)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1160, 900, 120, p, "\"ALREADY BEEN PAID\" (POLICE)", rgb=(40, 46, 60), size=54)

def sc_raids(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("raids", 1)
    pop_text(c, "66 SEARCHES", CX, 430, ANTON, 120, CREAM, prog(t, 0, 0.25))
    if t < b1 - 0.2:
        smartphone(c, 230, 800, 0.45, a, t, sub="SEIZED", caller="PHONE")
        laptop(c, 520, 860, 0.55, a, t, label="SEIZED", rgb=RED)
        cash_stack(c, 820, 900, a, 6)
        k = eo(prog(t, W_("raids", "cash") - 0.6, 1.0))
        counter(c, int(370000 * k), CX, 1150, 120, GOLD2, a * clamp(k * 3), prefix="$", glow=20)
        text(c, "IN CASH", CX, 1230, BEBAS, 54, CREAM, a * clamp(k * 3), spacing=4)
    else:
        p = eo(prog(t, b1 - 0.2, 0.3))
        bars(c, p, y0=520, y1=1260)
        text(c, "UP TO", CX, 760, BEBAS, 80, CREAM, p, spacing=6)
        text(c, "15 YEARS", CX, 920, ANTON, 170, RED, p, glow=18, glow_rgb=RED)
        text(c, "IN PRISON", CX, 1020, BEBAS, 70, CREAM, p, spacing=6)

def sc_network(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("network", 1)
    pop_text(c, "60+ PEOPLE · 8 JURISDICTIONS", CX, 430, ANTON, 72, CREAM, prog(t, 0, 0.25))
    globe(c, CX, 820, 300, a, t)
    rng = random.Random(4)
    pts = [(CX + rng.uniform(-240, 240), 820 + rng.uniform(-220, 220)) for _ in range(8)]
    for i, (x, y) in enumerate(pts):
        pa = a * clamp((t - 0.4 - i * 0.25) / 0.3)
        if pa > 0:
            c.drawCircle(x, y, 18 + 4 * math.sin(t * 6 + i), P(C(RED, pa)))
            if i: c.drawLine(pts[i - 1][0], pts[i - 1][1], x, y, P(C(RED, pa * 0.6), stroke=4))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1230, 760, 120, p, "THE HUNT IS NOT OVER", rgb=(120, 40, 40), size=60)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    smartphone(c, CX, 1000, 0.7, a, t, ring=1.0, caller="IT SUPPORT?")
    pop_text(c, "WOULD YOU KNOW", CX, 430, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "IT WAS FAKE?", CX, 550, ANTON, 120, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 690)

E.DRAW = dict(hook=sc_hook, police=sc_police, study=sc_study, call=sc_call, access=sc_access, ransom=sc_ransom,
              total=sc_total, raids=sc_raids, network=sc_network, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"ransom"}
_IMP = [("police", "arrested", -0.1, 0.4), ("access", "broke", -0.1, 0.4), ("rehook", "bill", -0.2, 0.4),
        ("ransom", "negotiations", -0.2, 0.4), ("raids", "15", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$40", 0.0), ("total", "$405", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
