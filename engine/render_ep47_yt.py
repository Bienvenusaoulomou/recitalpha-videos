import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep47")
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

AGR = CH.CFO      # stylised Angelo Agrizzi
CEO = CH.RECRUITER

def cash_stack(c, x, y, a, n=5, rot=0):
    for i in range(n): bills(c, x, y - i * 14, a, 1, rot=rot)

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    text(c, "SOUTH AFRICA · COURT ORDER", CX, 420, BEBAS, 64, GOLD, 1.0, spacing=4)
    counter(c, 1660000000, CX, 560, 140 * lerp(1.1, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, prefix="R", glow=24)
    text(c, "TO PAY BACK", CX, 640, BEBAS, 60, CREAM, 1.0, spacing=6)
    scales(c, 260, 1060, 0.9, 1.0, tilt=0.4 * math.sin(t * 1.5))
    AGR.draw(c, 780, 1250, 0.95, -1, a=1.0, blink=bl(t), brow=-0.4, arm_f=(-20, -30))
    if t > b1 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        for i in range(6):
            yy = 700 + ((t - b1) * 380 + i * 90) % 500
            bills(c, 120 + i * 160, yy, p * 0.9, 1, rot=(t * 60 + i * 40) % 360)
        ps = prog(t, b1 + 0.3, 0.22)
        if ps > 0: stamp(c, 300, 760, "BRIBES", RED, 90, -8, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("who", 1)
    AGR.draw(c, 270, 1250, 1.0, 1, a=a, blink=bl(t), mouth=0.0, arm_f=(-30, -40))
    name_chip(c, 290, 600, "ANGELO AGRIZZI (STYLISED)", a, rgb=GOLD2, size=36)
    pop_text(c, "THE NAME", CX + 160, 470, ANTON, 80, CREAM, prog(t, 0.1, 0.25))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "FORMER COO", 760, 860, ANTON, 90, GOLD2, p, glow=16, glow_rgb=GOLD)
        building(c, 760, 1220, 0.55 * lerp(1.3, 1, p), p, "BOSASA", cols=4)
        pd = eo(prog(t, W_("who", "government") - 0.2, 0.3))
        if pd > 0:
            for i in range(3):
                paper_doc(c, 560 + i * 120, 600 + i * 10, 0.28, -10 + i * 10, pd, "REPUBLIC", "TENDER", "CONTRACT", lines=4)

def sc_vault(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("vault", 1); b2 = B("vault", 2)
    if t < b1 - 0.2:
        calendar(c, 230, 560, 0.6, a, "19", "JAN 2019")
        pop_text(c, "PUBLIC INQUIRY", CX + 150, 470, ANTON, 84, CREAM, prog(t, 0.1, 0.25))
        text(c, "INTO CORRUPTION", CX + 150, 560, BEBAS, 60, GOLD, a, spacing=4)
        AGR.draw(c, 300, 1250, 0.9, 1, a=a, blink=bl(t), mouth=talk(t), arm_f=(-80, -40))
        pv = eo(prog(t, W_("vault", "secret") - 0.2, 0.3))
        if pv > 0:
            inner = screen(c, 720, 930, 520, 360, pv, "SECRET VIDEO")
            c.drawCircle(inner.left() + 34, inner.top() + 34, 12, P(C(RED, pv * (0.5 + 0.5 * math.sin(t * 8)))))
            safe(c, 720, 960, 0.45, pv, open_=0.0)
    else:
        inner = screen(c, CX, 900, 900, 640, 1.0, "INSIDE THE VAULT · SECRET VIDEO")
        c.save(); c.clipRect(inner)
        safe(c, 300, 820, 0.8, 1.0, open_=1.0)
        CEO.draw(c, 700, 1150, 0.85, -1, a=1.0, blink=bl(t), look=(0, 1), arm_f=(-20 + 15 * math.sin(t * 8), -70), arm_b=(-30, -60))
        for i in range(4): cash_stack(c, 560 + i * 90, 1060, 1.0, n=3 + i % 2)
        c.drawCircle(inner.left() + 34, inner.top() + 34, 12, P(C(RED, 0.5 + 0.5 * math.sin(t * 8))))
        c.restore()
        name_chip(c, CX, 1268, "BOSASA'S CEO (STYLISED)", 1.0, size=34)
        if t > b2 - 0.3:
            p = eo(prog(t, b2 - 0.3, 0.3))
            counter(c, int(1e6 * eo(prog(t, b2 - 0.2, 0.9))), CX, 520, 120, GOLD2, p, prefix="~R", glow=22)
            ps = prog(t, W_("vault", "bribes") - 0.1, 0.22)
            if ps > 0: tag(c, 760, 700, "FOR BRIBES, HE SAID", ps, rot=-5)

def sc_guilty(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("guilty", 1)
    text(c, "NOVEMBER 2025", 420, 600, BEBAS, 60, GOLD, a, spacing=4)
    AGR.draw(c, 760, 1250, 0.95, -1, a=a, blink=bl(t), brow=-0.6, tilt=-4, arm_f=(10, -10))
    ps = prog(t, W_("guilty", "guilty") - 0.1, 0.22)
    if ps > 0: stamp(c, 440, 470, "PLEADED GUILTY", RED, 84, -5, ps, sc=lerp(2.2, 1, eo(ps)))
    pc = eo(prog(t, W_("guilty", "corruption") - 0.1, 0.3))
    text(c, "CORRUPTION", 330, 830, ANTON, 76, CREAM, pc)
    pm = eo(prog(t, W_("guilty", "laundering") - 0.3, 0.3))
    text(c, "+ MONEY LAUNDERING", 330, 920, ANTON, 60, CREAM, pm)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, 330, 1060, 560, 120, p, "10-YEAR SENTENCE", rgb=(40, 46, 60), size=60)
        text(c, "(REPORTEDLY SUSPENDED)", 330, 1170, BEBAS, 44, GOLD, eo(prog(t, W_("guilty", "suspended") - 0.2, 0.3)), spacing=2)

def sc_order(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("order", 1)
    pop_text(c, "LATE OCTOBER 2026", CX, 430, ANTON, 84, CREAM, prog(t, 0, 0.25))
    building(c, CX, 1230, 0.9, a * (1 - eo(prog(t, b1 - 0.3, 0.3))), "HIGH COURT · PRETORIA", cols=5)
    scales(c, CX, 840, 0.7, a * (1 - eo(prog(t, b1 - 0.3, 0.3))), tilt=0.3 * math.sin(t * 1.4))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        paper_doc(c, CX, 900, 0.62 * lerp(1.3, 1, p), -3, p, "HIGH COURT", "CONFISCATION ORDER", "TO PAY:", lines=3)
        text(c, "R1.66 BILLION", CX, 905, ANTON, 76, RED, p * eo(prog(t, b1, 0.3)))
        pi = eo(prog(t, W_("order", "interest") - 0.2, 0.3))
        text(c, "+ INTEREST", CX, 1010, ANTON, 80, INK, pi)

def sc_hid(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("hid", 1)
    q = 1 - eo(prog(t, b1 - 0.3, 0.3))
    scales(c, 200, 900, 0.6, a * q, tilt=-0.4)
    pop_text(c, "NOT FULLY DISCLOSED", CX + 80, 470, ANTON, 80, CREAM, prog(t, 0.1, 0.25))
    paper_doc(c, 680, 870, 0.5, 4, a * q, "ASSETS", "DECLARATION", "INCOMPLETE", lines=5)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        house(c, 280, 1180, 0.9, p)
        globe(c, 760, 900, 170, p, t)
        house(c, 760, 1220, 0.6, p, rgb=(190, 170, 140), roof=(60, 70, 110))
        text(c, "SOUTH AFRICA", 280, 1240, BEBAS, 50, CREAM, p, spacing=3)
        text(c, "ABROAD", 760, 1260, BEBAS, 50, CREAM, p, spacing=3)
        ps = prog(t, W_("hid", "hidden") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 680, "HIDDEN PROPERTIES", RED, 80, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("twist", 1); b2 = B("twist", 2)
    pop_text(c, "THE CATCH", CX, 450, ANTON, 120, GOLD2, prog(t, 0, 0.25), glow=20, glow_rgb=GOLD)
    if t < b2 - 0.2:
        safe(c, CX, 940, 0.9, a, open_=eo(prog(t, b1, 0.6)) * 0.29)
        if t > b1 - 0.3:
            p = eo(prog(t, b1 - 0.3, 0.3))
            text(c, "AN ORDER IS NOT", CX, 600, ANTON, 80, CREAM, p)
            text(c, "MONEY IN THE BANK", CX, 690, ANTON, 80, CREAM, p)
            ps = prog(t, W_("twist", "recovered") - 0.1, 0.22)
            if ps > 0: stamp(c, CX, 940, "NOT RECOVERED", RED, 90, -6, ps, sc=lerp(2.2, 1, eo(ps)))
    else:
        p = eo(prog(t, b2 - 0.2, 0.3))
        globe(c, CX, 900, 260, p, t)
        house(c, 330, 1230, 0.6, p); house(c, 760, 1230, 0.6, p, rgb=(190, 170, 140), roof=(60, 70, 110))
        # magnifier
        mx = CX + 220 * math.sin(t * 1.3); my = 880 + 90 * math.cos(t * 1.7)
        c.drawCircle(mx, my, 90, P(C(GOLD2, p), stroke=16)); c.drawLine(mx + 64, my + 64, mx + 150, my + 150, P(C(GOLD2, p), stroke=26))
        text(c, "NOW: FIND IT", CX, 620, ANTON, 96, GOLD2, p, glow=16, glow_rgb=GOLD)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i in range(7):
        bills(c, 120 + i * 140, 860 + 20 * math.sin(t * 2 + i), a, 2, rot=(i - 3) * 8)
    text(c, "?", CX, 1150, ANTON, 170, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "SHOULD BRIBE-PAYERS", CX, 430, ANTON, 92, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "PAY IT ALL BACK?", CX, 545, ANTON, 110, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 690)

E.DRAW = dict(hook=sc_hook, who=sc_who, vault=sc_vault, guilty=sc_guilty, order=sc_order, hid=sc_hid,
              twist=sc_twist, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"guilty"}
_IMP = [("hook", "bribes", -0.1, 0.4), ("guilty", "guilty", -0.1, 0.4), ("hid", "hidden", -0.1, 0.4),
        ("twist", "recovered", -0.1, 0.4), ("rehook", "him", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "R1.66", 0.0), ("order", "R1.66", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
