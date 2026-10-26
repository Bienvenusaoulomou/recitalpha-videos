import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep20")
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

PH = dict(mint=load_photo("mint_02.jpg"), buick=load_photo("mint_03.jpg"))
CR_M = "DENVER MINT · DETROIT PUBLISHING CO. · PUBLIC DOMAIN"
CR_B = "A 1924 BUICK TOURER · STATE LIBRARY QLD · PUBLIC DOMAIN"

def truck(c, x, y, s, a, label="FEDERAL RESERVE"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-260, -220, 120, 0), P(C((70, 76, 70), a)))
    c.drawRect(skia.Rect(120, -150, 260, 0), P(C((60, 64, 60), a)))
    c.drawRect(skia.Rect(150, -130, 235, -80), P(C((120, 140, 150), a)))
    text(c, label, -70, -95, BEBAS, 44, CREAM, a, spacing=3)
    for wx in (-170, 180): c.drawCircle(wx, 0, 42, P(C((15, 15, 15), a))); c.drawCircle(wx, 0, 18, P(C((150, 150, 150), a)))
    c.restore()

def sack(c, x, y, s, a, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(-40, -110); p.quadTo(-150, -20, -120, 90); p.quadTo(0, 150, 120, 90); p.quadTo(150, -20, 40, -110); p.close()
    c.drawPath(p, P(C((190, 170, 130), a))); c.drawPath(p, P(C((120, 100, 70), a), stroke=5))
    text(c, "$", 0, 60, ANTON, 120, (60, 110, 60), a)
    c.restore()

def garage(c, x, y, a, open_=0.0):
    c.drawRect(skia.Rect(x - 360, y - 380, x + 360, y), P(C((90, 80, 66), a)))
    r = skia.Path(); r.moveTo(x - 400, y - 380); r.lineTo(x, y - 480); r.lineTo(x + 400, y - 380); r.close(); c.drawPath(r, P(C((60, 52, 44), a)))
    c.drawRect(skia.Rect(x - 280, y - 300, x + 280, y), P(C((20, 18, 16), a)))
    door_h = 300 * (1 - open_)
    c.drawRect(skia.Rect(x - 280, y - 300, x + 280, y - 300 + door_h), P(C((140, 126, 104), a)))
    for k in range(int(door_h // 50)): c.drawLine(x - 280, y - 300 + k * 50, x + 280, y - 300 + k * 50, P(C((100, 90, 74), a), stroke=3))

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    photo_card(c, PH["mint"], CX, 800, 840, 671, t / D, 1.0, 1.0, 1.12, credit=CR_M, dim=0.55 * out)
    text(c, "THE U.S. MINT", CX, 390, ANTON, 120, CREAM, 1.0)
    text(c, "IN BROAD DAYLIGHT", CX, 1210, ANTON, 92, GOLD2, 1.0 - out, glow=18, glow_rgb=GOLD)
    if out > 0:
        k = eo(prog(t, W_("hook", "$200,000") - 0.2, 0.9))
        counter(c, 200000 * k, CX, 800, 170, GOLD2, out, glow=26)
        ps = prog(t, W_("hook", "90") - 0.15, 0.22)
        if ps > 0: stamp(c, CX, 1150, "IN ~90 SECONDS", RED, 110, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_morning(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("morning", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    pop_text(c, "DENVER · DEC. 18, 1922", CX, 380, ANTON, 96, CREAM, prog(t, 0.05, 0.25))
    if out < 1:
        clock(c, CX, 800, 230, a * (1 - out), 10.5, None)
        pop_text(c, "10:30 A.M.", CX, 1150, ANTON, 120, GOLD2, prog(t, W_("morning", "10:30") - 0.2, 0.25) * (1 - out), glow=18, glow_rgb=GOLD)
    if out > 0:
        truck(c, lerp(W + 400, CX, eo(prog(t, b1 - 0.2, 0.7))), 1000, 1.25, out)
        pill(c, "LOADING OUTSIDE THE MINT", 1180, eo(prog(t, W_("morning", "loaded") - 0.2, 0.3)), GOLD2, 58, 820)

def sc_cargo(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i in range(10):
        d = clamp(t * 3 - i * 0.15)
        banknote(c, CX + ((i * 41) % 120 - 60), 940 - i * 18, 0.8, a * d, rot=(i * 7) % 12 - 6, value="5", sub="DOLLARS", rgb=(150, 180, 150))
    k = eo(prog(t, W_("cargo", "$200,000,") - 0.2, 0.9))
    counter(c, 200000 * k, CX, 480, 160, GOLD2, a, glow=24)
    pn = prog(t, W_("cargo", "brand") - 0.15, 0.25)
    pop_text(c, "BRAND NEW $5 BILLS", CX, 1200, ANTON, 92, CREAM, pn)

def sc_attack(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("attack", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["buick"], CX, 740, 920, 617, t / b1, a * (1 - out), 1.0, 1.12, credit=CR_B)
        pop_text(c, "A BLACK BUICK", CX, 360, ANTON, 120, CREAM, prog(t, W_("attack", "black") - 0.15, 0.25))
    if out > 0:
        truck(c, CX + 160, 1050, 1.0, out)
        for i in range(3):
            d = eo(prog(t, W_("attack", "grabbed") - 0.2 + i * 0.2, 0.5))
            sack(c, lerp(CX + 100, CX - 330 + i * 40, d), lerp(900, 700 - i * 30, d), 0.7, out, rot=(i - 1) * 12)
        ps = prog(t, W_("attack", "shotguns") - 0.15, 0.22)
        if ps > 0: stamp(c, CX, 430, "SHOTGUNS", RED, 130, -5, ps, sc=lerp(2.2, 1, eo(ps)))
        pop_text(c, "THEY GRABBED THE BAGS", CX, 1220, ANTON, 84, GOLD2, prog(t, W_("attack", "grabbed") - 0.15, 0.25), glow=16, glow_rgb=GOLD)

def sc_cost(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("cost", 1)
    c.drawRect(skia.Rect(0, 330, W, 1240), P(C((0, 0, 0), 0.35 * a)))
    pop_text(c, "A GUARD LOST HIS LIFE", CX, 560, ANTON, 104, CREAM, prog(t, 0.05, 0.25))
    pn = eo(prog(t, W_("cost", "Charles") - 0.2, 0.3))
    text(c, "CHARLES LINTON", CX, 720, PLAY, 90, GOLD2, pn)
    rule(c, CX - 260, CX + 260, 760, GOLD, pn, 2)
    pw = prog(t, b1 - 0.05, 0.25)
    pill(c, "ONE ROBBER BADLY WOUNDED", 1050, eo(pw), RED, 60, 860)

def sc_garage(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("garage", 1)
    op = eo(prog(t, W_("garage", "found") - 0.2, 1.0))
    garage(c, CX, 1150, a, op)
    if op > 0.3:
        c.save(); c.clipRect(skia.Rect(CX - 280, 850, CX + 280, 1150))
        c.drawRect(skia.Rect(CX - 220, 1020, CX + 220, 1110), P(C((30, 30, 34), a))); c.drawRect(skia.Rect(CX - 120, 960, CX + 120, 1020), P(C((30, 30, 34), a)))
        c.restore()
    pop_text(c, "WEEKS LATER", CX, 400, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    pop_text(c, "THE GETAWAY BUICK", CX, 540, ANTON, 90, GOLD2, prog(t, W_("garage", "Buick") - 0.15, 0.25))
    pl = prog(t, W_("garage", "Left") - 0.15, 0.22)
    if pl > 0: stamp(c, CX, 700, "LEFT BEHIND BY HIS GANG", RED, 80, -4, pl, sc=lerp(2, 1, eo(pl)))

def sc_money(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("money", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    pin(c, CX, 780, 1.3, a * (1 - out * 0.6), RED, "MINNESOTA")
    k = eo(prog(t, W_("money", "$80,000") - 0.2, 0.9))
    counter(c, 80000 * k, CX, 450, 140, GOLD2, a, suffix=" FOUND", glow=20)
    if out > 0:
        c.drawRect(skia.Rect(0, 950, W, 1240), P(C(BG, 0.8 * out)))
        counter(c, 120000, CX, 1110, 130, RED, out, suffix="?", glow=16)
        text(c, "NEVER ACCOUNTED FOR", CX, 1200, BEBAS, 60, CREAM, out, spacing=6)

def sc_closed(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("closed", 1)
    calendar(c, CX, 720, 1.0, a, "1934", "12 YEARS LATER")
    pc = prog(t, W_("closed", "knew") - 0.2, 0.22)
    if pc > 0: stamp(c, CX, 1000, "CASE CLOSED", GOLD2, 120, -5, pc * (1 - eo(prog(t, b1 - 0.2, 0.3)) * 0.6), sc=lerp(2, 1, eo(pc)))
    pd = prog(t, b1 - 0.05, 0.25)
    pop_text(c, "MOST WERE ALREADY DEAD", CX, 1180, ANTON, 84, RED, pd, glow=14, glow_rgb=RED)

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["mint"], CX, 800, 840, 671, t / D, a, 1.0, 1.1, credit=CR_M, dim=0.5)
    pn = prog(t, W_("twist", "No") - 0.1, 0.22)
    if pn > 0: stamp(c, CX, 800, "NO ONE CHARGED", RED, 120, -6, pn, sc=lerp(2.2, 1, eo(pn)))
    pop_text(c, "NOT ONE PERSON", CX, 390, ANTON, 110, CREAM, prog(t, 0.05, 0.25))

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    news(c, CX, 760, 1.05, -3, a, "LONDON, 1814", "NAPOLEON IS DEAD?", "A FAKE MESSENGER")
    pm = prog(t, W_("cta", "market") - 0.2, 0.25)
    if pm > 0:
        pts = [(160 + i * 40, 1180 - (i ** 1.6) * 6) for i in range(20)]
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:int(1 + 19 * eo(pm))]: p.lineTo(*q)
        c.drawPath(p, P(C(GOLD2, eo(pm)), stroke=10))
        text(c, "STOCKS WENT WILD", CX + 120, 1120, ANTON, 70, GOLD2, eo(pm))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    photo_card(c, PH["mint"], CX, 800, 840, 671, t / D, 1.0, 1.0, 1.1, credit=CR_M, dim=0.45)
    pop_text(c, "STILL A MYSTERY", CX, 800, ANTON, 130, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "BECAUSE...", CX, 1210, ANTON, 110, GOLD2, prog(t, W_("loopend", "Because") - 0.1, 0.25), glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, morning=sc_morning, cargo=sc_cargo, attack=sc_attack, cost=sc_cost, garage=sc_garage, money=sc_money,
              closed=sc_closed, twist=sc_twist, cta=sc_cta, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"attack", "cost"}
_IMP = [("hook", "90", -0.15, 0.4), ("morning", "Federal", -0.1, 0.3), ("cargo", "brand", -0.15, 0.3),
        ("attack", "shotguns", -0.15, 0.35), ("rehook", "gone.", -0.2, 0.35), ("garage", "Left", -0.15, 0.35),
        ("money", "rest?", -0.1, 0.35), ("closed", "knew", -0.2, 0.3), ("twist", "No", -0.1, 0.45),
        ("cta", "Napoleon", -0.1, 0.3), ("loopend", "To", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("cargo", "$200,000,", 0.0), ("money", "$80,000", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
