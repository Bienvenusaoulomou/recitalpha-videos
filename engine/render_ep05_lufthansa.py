import os, sys, math, random
os.environ["REC_ROOT"] = "/home/claude/ep05"
sys.path.insert(0, "/home/claude/ep05")
import skia
import engine as E
from props import *

NAVY = (34, 40, 64)

def mask(c, x, y, r, a, rgb=(30, 30, 34)):
    c.drawCircle(x, y, r, P(C(rgb, a)))
    c.drawRoundRect(skia.Rect(x - r * 0.75, y - r * 0.32, x + r * 0.75, y + r * 0.02), r * 0.15, r * 0.15, P(C(CREAM, a * 0.9)))
    c.drawOval(skia.Rect(x - r * 0.55, y - r * 0.25, x - r * 0.15, y - r * 0.05), P(C(INK, a)))
    c.drawOval(skia.Rect(x + r * 0.15, y - r * 0.25, x + r * 0.55, y - r * 0.05), P(C(INK, a)))

def robber(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-70, 10, 70, 200), 40, 40, P(C(NAVY, a)))
    mask(c, 0, -40, 52, a)
    c.restore()

def van(c, x, y, s, a, lights=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(-260, 0); body.lineTo(-260, -200); body.lineTo(120, -200); body.lineTo(200, -110)
    body.lineTo(260, -100); body.lineTo(260, 0); body.close()
    c.drawPath(body, P(C((22, 22, 26), a))); c.drawPath(body, P(C(GOLD, a * 0.6), stroke=4))
    c.drawRect(skia.Rect(130, -185, 190, -115), P(C((70, 80, 96), a)))
    for wx in (-160, 160):
        c.drawCircle(wx, 0, 52, P(C((10, 10, 10), a))); c.drawCircle(wx, 0, 22, P(C(MUTED, a)))
    if lights > 0:
        g = P(C(GOLD2, a * lights)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
        c.drawCircle(262, -70, 26, g)
    c.restore()

def plane(c, x, y, s, a, rot=-6):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    pl = skia.Path(); pl.moveTo(-240, 0); pl.lineTo(200, -10); pl.cubicTo(250, -10, 260, 10, 200, 14); pl.lineTo(-240, 14); pl.close()
    c.drawPath(pl, P(C(CREAM, a)))
    w = skia.Path(); w.moveTo(-20, 0); w.lineTo(-120, 120); w.lineTo(-60, 120); w.lineTo(60, 4); w.close(); c.drawPath(w, P(C(CREAM, a)))
    tl = skia.Path(); tl.moveTo(-220, 0); tl.lineTo(-260, -80); tl.lineTo(-210, -80); tl.lineTo(-170, 0); tl.close(); c.drawPath(tl, P(C(GOLD, a)))
    c.restore()

def hangar(c, x, y, s, a, lit=0.6):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-380, -300, 380, 0), P(C((48, 44, 40), a)))
    c.drawRect(skia.Rect(-380, -300, 380, 0), P(C(GOLD, a * 0.6), stroke=4))
    for k in range(6):
        c.drawRect(skia.Rect(-340 + k * 116, -250, -260 + k * 116, -200), P(C(GOLD2 if k % 2 == 0 else (30, 26, 20), a * (0.3 + 0.7 * lit))))
    c.drawRect(skia.Rect(-120, -150, 120, 0), P(C((22, 20, 18), a)))
    text(c, "CARGO 261", 0, -322, ANTON, 52, GOLD2, a)
    c.restore()

def box(c, x, y, s, a, label="$"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-60, -50, 60, 50), P(C((150, 118, 74), a)))
    c.drawRect(skia.Rect(-60, -50, 60, 50), P(C((90, 68, 40), a), stroke=4))
    c.drawRect(skia.Rect(-8, -50, 8, 50), P(C((200, 170, 110), a)))
    text(c, label, 0, 22, ANTON, 54, (70, 50, 26), a)
    c.restore()

def clock(c, x, y, r, a, minutes):
    c.drawCircle(x, y, r, P(C((236, 226, 204), a)))
    c.drawCircle(x, y, r, P(C(GOLD, a), stroke=8))
    ang = math.radians(minutes / 60 * 360 - 90)
    c.drawLine(x, y, x + r * 0.8 * math.cos(ang), y + r * 0.8 * math.sin(ang), P(C(RED, a), stroke=8))
    ang2 = math.radians(minutes / 720 * 360 - 90 + 90)
    c.drawLine(x, y, x + r * 0.5 * math.cos(ang2), y + r * 0.5 * math.sin(ang2), P(C(INK, a), stroke=10))
    c.drawCircle(x, y, 10, P(C(INK, a)))

def dice(c, x, y, s, rot, a, n=5):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-60, -60, 60, 60), 14, 14, P(C(CREAM, a)))
    pts = {5: [(-30, -30), (30, -30), (0, 0), (-30, 30), (30, 30)], 3: [(-30, -30), (0, 0), (30, 30)]}[n]
    for px, py in pts: c.drawCircle(px, py, 10, P(C(INK, a)))
    c.restore()

# ---------------- scenes ----------------
def sc_hook(c, t, D):
    # frame 1: hook text already big on screen
    text(c, "6 MASKED MEN", CX, 440, ANTON, 120, CREAM, 1.0)
    shadowed(c, lambda: text(c, "$5,000,000", CX, 640, ANTON, 170, GOLD2, 1.0, glow=26, glow_rgb=GOLD))
    text(c, "IN CASH", CX, 740, BEBAS, 80, MUTED, 1.0, spacing=8)
    for i in range(6):
        robber(c, 165 + i * 150, 930, 0.62, 1.0)
    pn = prog(t, wt("hook", "Not") - 0.15, 0.25)
    if pn > 0:
        c.drawRect(skia.Rect(0, 820, W, 1230), P(C(BG, 0.8 * eo(pn))))
        stamp(c, CX, 1050, "NEVER FOUND", RED, 120, -6, pn, sc=lerp(2, 1, eo(pn)))

def sc_place(c, t, D):
    a = eo(prog(t, 0, 0.4))
    for i in range(60):
        R = random.Random(i); c.drawCircle(R.uniform(0, W), R.uniform(300, 700), R.uniform(1.5, 3.5), P(C(CREAM, 0.5 * a * (0.5 + 0.5 * math.sin(t * 2 + i)))))
    plane(c, lerp(-300, W + 300, prog(t, 0.3, D)), 560, 0.8, a, rot=-10)
    hangar(c, CX, 1060, 1.0, a, lit=0.5 + 0.5 * math.sin(t * 2.5))
    calendar(c, 870, 470, 0.55, eo(prog(t, wt("place", "11,") - 0.3, 0.3)), "11", "DEC 1978")
    pill(c, "JFK AIRPORT · LUFTHANSA CARGO", 1170, eo(prog(t, wt("place", "Lufthansa") - 0.2, 0.3)), GOLD2, 60, 920)

def sc_cash(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "WEST GERMANY", 250, 470, BEBAS, 64, CREAM, a, spacing=4)
    text(c, "NEW YORK", 830, 470, BEBAS, 64, CREAM, a, spacing=4)
    pp = eio(prog(t, 0.2, 2.2))
    arc = skia.Path(); arc.moveTo(250, 520); arc.quadTo(CX, 380, 830, 520)
    c.drawPath(arc, P(C(GOLD, a * 0.5), stroke=4))
    px = lerp(250, 830, pp); py = 520 - 4 * (380 - 520) * -pp * (1 - pp) * 0.5 - 0
    py = (1 - pp) ** 2 * 520 + 2 * (1 - pp) * pp * 380 + pp * pp * 520
    plane(c, px, py, 0.35, a, rot=-20 + 40 * pp)
    safe(c, CX, 860, 0.9, a, open_=prog(t, 1.0, 1.0))
    b1 = beat("cash", 1)
    pu = eo(prog(t, b1 - 0.2, 0.3))
    pill(c, "USED BILLS", 1110, pu, CREAM, 64, 600)
    ps = prog(t, wt("cash", "impossible") - 0.2, 0.25)
    if ps > 0: stamp(c, CX, 600, "UNTRACEABLE", RED, 90, -8, ps, sc=lerp(2, 1, eo(ps)))

def sc_insider(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("insider", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        hangar(c, CX, 1000, 0.9, a)
        person(c, CX, 850, 60, GOLD2, a)
        text(c, "THE TIP CAME FROM INSIDE", CX, 470, ANTON, 82, CREAM, a)
        c.restore(); c.restore()
    if out > 0:
        person(c, CX, 640, 90, CREAM, out)
        text(c, "LOUIS WERNER", CX, 470, PLAY, 80, CREAM, out)
        text(c, "CARGO SUPERVISOR", CX, 800, BEBAS, 64, MUTED, out, spacing=6)
        dice(c, 200, 620, 0.9, 15 + 30 * math.sin(t * 2), out, 5); dice(c, 880, 620, 0.9, -20 + 30 * math.sin(t * 2 + 1), out, 3)
        pd = prog(t, wt("insider", "$20,000") - 0.2, 0.3)
        pop_text(c, "~$20,000 DEBT", CX, 980, ANTON, 120, RED, pd, glow=20, glow_rgb=RED)
        pill(c, "GAMBLING", 1150, eo(prog(t, wt("insider", "gambling") - 0.2, 0.3)), GOLD2, 64, 520)

def sc_crew(c, t, D):
    a = eo(prog(t, 0, 0.4))
    nodes = [(220, 640, "WERNER", 0.0), (CX, 820, "A BOOKIE", wt("crew", "bookie.") - 0.4), (860, 1000, "MOB CREW", wt("crew", "crew") - 0.4)]
    for i, (x, y, lbl, t0) in enumerate(nodes):
        p = eo(prog(t, t0, 0.35))
        if i > 0:
            x0, y0 = nodes[i - 1][0], nodes[i - 1][1]
            k = eo(prog(t, t0 - 0.2, 0.5))
            c.drawLine(x0, y0, lerp(x0, x, k), lerp(y0, y, k), P(C(GOLD, a * k), stroke=6))
        person(c, x, y - 40, 50, GOLD2 if i == 2 else CREAM, p)
        text(c, lbl, x, y + 70, BEBAS, 58, CREAM, p, spacing=4)
    text(c, "THE SECRET TRAVELS", CX, 470, ANTON, 82, CREAM, a)
    pill(c, "RUN BY JIMMY BURKE", 1170, eo(prog(t, wt("crew", "Jimmy") - 0.2, 0.3)), GOLD2, 64, 760)

def sc_night(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "3:00 AM", CX, 430, ANTON, 120, GOLD2, a, glow=18, glow_rgb=GOLD)
    hangar(c, CX + 260, 1000, 0.75, a)
    vx = lerp(-300, 380, eo(prog(t, 0.1, 1.8)))
    van(c, vx, 1000, 0.85, a, lights=1.0)
    b1 = beat("night", 1)
    for i in range(6):
        p = eo(prog(t, b1 + i * 0.12, 0.3))
        robber(c, 150 + i * 156, 540, 0.55, p)
    seq_rows(c, t, [("SIX MEN", wt("night", "Six") , CREAM), ("MASKS", wt("night", "masks,"), CREAM), ("GUNS", wt("night", "guns."), RED)], 1170, 100)

def sc_vault(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("vault", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        n = int(clamp(t / max(0.1, b1 - 0.3)) * 6) + 1
        for i in range(min(n, 6)):
            person(c, 180 + i * 145, 800, 48, CREAM, a * (1 - out))
        text(c, "THE NIGHT SHIFT", CX, 500, ANTON, 96, CREAM, a * (1 - out))
        pill(c, "ONE WORKER AT A TIME", 1120, eo(prog(t, wt("vault", "one") - 0.2, 0.3)) * (1 - out), GOLD2, 62, 760)
    if out > 0:
        safe(c, CX, 760, 1.15, out, open_=prog(t, b1 + 0.4, 1.0))
        text(c, "THE VAULT", CX, 450, ANTON, 110, GOLD2, out, glow=18, glow_rgb=GOLD)

def sc_loot(c, t, D):
    a = eo(prog(t, 0, 0.3))
    n = int(clamp(t / 2.5) * 18)
    for i in range(n):
        box(c, 170 + (i % 6) * 148, 1110 - (i // 6) * 104, 0.85, 1.0, "$" if i % 4 else "♦" if False else "$")
    p = eio(prog(t, wt("loot", "$5.8") - 0.2, 1.2))
    shadowed(c, lambda: text(c, "${:.1f} MILLION".format(5.8 * p) if p < 1 else "$5.8 MILLION", CX, 560, ANTON, 150,
                             GOLD2 if p >= 1 else CREAM, a, glow=24 if p >= 1 else 0, glow_rgb=GOLD))
    pm = eo(prog(t, wt("loot", "64") - 0.3, 0.3))
    if pm > 0:
        clock(c, 200, 450, 70, pm, 64 * clamp((t - wt("loot", "64")) / 1.0))
        text(c, "IN 64 MINUTES", CX + 60, 680, BEBAS, 80, CREAM, pm, spacing=4)
    b1 = beat("loot", 1)
    pr = prog(t, b1 - 0.1, 0.3)
    if pr > 0:
        c.drawRect(skia.Rect(0, 300, W, 1230), P(C(BG, 0.75 * eo(pr))))
        text(c, "BIGGEST CASH ROBBERY", CX, 700, ANTON, 96, GOLD2, eo(pr))
        text(c, "IN U.S. HISTORY", CX, 810, ANTON, 96, GOLD2, eo(pr))
        text(c, "(AT THE TIME)", CX, 900, BEBAS, 60, MUTED, eo(pr), spacing=6)

def sc_van(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "ONE JOB:", CX, 460, ANTON, 100, CREAM, a)
    text(c, "GET RID OF THE VAN", CX, 580, ANTON, 90, GOLD2, eo(prog(t, wt("van", "rid") - 0.3, 0.3)))
    van(c, CX, 960, 1.1, a)
    b1 = beat("van", 1)
    pd = prog(t, wt("van", "didn't.") - 0.15, 0.25)
    if pd > 0: stamp(c, CX, 860, "HE DIDN'T", RED, 110, -8, pd, sc=lerp(2, 1, eo(pd)))
    pill(c, "POLICE FOUND IT", 1170, eo(prog(t, wt("van", "Police") - 0.2, 0.3)), CREAM, 64, 640)

def sc_fallout(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("fallout", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        for i in range(8):
            x = 150 + (i % 4) * 260; y = 640 + (i // 4) * 300
            fade = 1 - eo(prog(t, 0.6 + i * 0.35, 0.4))
            person(c, x, y, 54, CREAM, a * fade * (1 - out) + 0.0)
            c.drawCircle(x, y, 70, P(C(MUTED, a * 0.25 * (1 - out)), stroke=3))
        text(c, "ONE BY ONE...", CX, 460, ANTON, 100, CREAM, a * (1 - out))
    if out > 0:
        for i in range(10):
            bills(c, CX + (i - 5) * 70, 800 - (t - b1) * 120 * (1 + i % 3) , out * (1 - prog(t, b1, 2.0)), 1, rot=i * 20)
        text(c, "THE MONEY", CX, 650, ANTON, 120, GOLD2, out)
        pop_text(c, "NEVER CAME BACK", CX, 820, ANTON, 110, RED, prog(t, wt("fallout", "never") - 0.15, 0.25))

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("verdict", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        text(c, "CONVICTED:", CX, 460, BEBAS, 90, MUTED, a, spacing=8)
        person(c, CX, 720, 90, CREAM, a)
        for k in range(6): c.drawLine(330 + k * 84, 560, 330 + k * 84, 900, P(C(MUTED, a * 0.8), stroke=10))
        pop_text(c, "ONLY 1 MAN", CX, 1010, ANTON, 120, GOLD2, prog(t, wt("verdict", "one") - 0.1, 0.25))
        pill(c, "THE INSIDE MAN · 15 YEARS", 1160, eo(prog(t, wt("verdict", "15") - 0.3, 0.3)), CREAM, 62, 860)
        c.restore(); c.restore()
    if out > 0:
        # film strip
        for k in range(3):
            x0 = 160 + k * 260
            c.drawRect(skia.Rect(x0, 560, x0 + 240, 860), P(C((24, 22, 20), out)))
            c.drawRect(skia.Rect(x0 + 20, 600, x0 + 220, 820), P(C(GOLD, out * 0.25)))
            for h in range(5):
                c.drawRect(skia.Rect(x0 + 6 + h * 48, 570, x0 + 30 + h * 48, 588), P(C(CREAM, out * 0.6)))
                c.drawRect(skia.Rect(x0 + 6 + h * 48, 832, x0 + 30 + h * 48, 850), P(C(CREAM, out * 0.6)))
        text(c, "12 YEARS LATER...", CX, 470, BEBAS, 84, CREAM, out, spacing=6)
        pop_text(c, "GOODFELLAS", CX, 1010, ANTON, 150, GOLD2, prog(t, wt("verdict", "Goodfellas.") - 0.15, 0.25), glow=26, glow_rgb=GOLD)
        text(c, "(1990)", CX, 1110, BEBAS, 64, MUTED, eo(prog(t, wt("verdict", "Goodfellas."), 0.3)), spacing=6)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "NEXT EPISODE", CX, 450, BEBAS, 70, MUTED, a, spacing=10)
    # map of an island country with question mark
    c.save(); c.translate(CX, 720)
    isl = skia.Path(); isl.moveTo(-260, 20); isl.cubicTo(-200, -140, 60, -160, 180, -80); isl.cubicTo(300, -10, 220, 120, 60, 130)
    isl.cubicTo(-100, 140, -300, 120, -260, 20); isl.close()
    c.drawPath(isl, P(C((60, 80, 50), a))); c.drawPath(isl, P(C(GOLD, a), stroke=5))
    c.restore()
    pq = prog(t, wt("cta", "exist.") - 0.2, 0.25)
    if pq > 0: stamp(c, CX, 720, "DOESN'T EXIST", RED, 84, -8, pq, sc=lerp(2, 1, eo(pq)))
    text(c, "A COUNTRY THAT NEVER WAS", CX, 960, ANTON, 76, CREAM, eo(prog(t, wt("cta", "country") - 0.3, 0.3)))
    for i in range(3):
        p = eo(prog(t, wt("cta", "sailed") - 0.3 + i * 0.15, 0.4))
        x = lerp(-200, 220 + i * 320, p)
        c.save(); c.translate(x, 1080); c.scale(0.5, 0.5)
        hull = skia.Path(); hull.moveTo(-120, 0); hull.lineTo(120, 0); hull.lineTo(90, 40); hull.lineTo(-90, 40); hull.close()
        c.drawPath(hull, P(C(CREAM, p))); c.drawLine(0, 0, 0, -150, P(C(CREAM, p), stroke=6))
        sail = skia.Path(); sail.moveTo(6, -140); sail.lineTo(90, -20); sail.lineTo(6, -20); sail.close(); c.drawPath(sail, P(C(GOLD2, p)))
        c.restore()
    follow_pill(c, wt("cta", "Follow") - 0.1, t, 1170)

E.DRAW = dict(hook=sc_hook, place=sc_place, cash=sc_cash, insider=sc_insider, crew=sc_crew, night=sc_night, vault=sc_vault,
              loot=sc_loot, van=sc_van, fallout=sc_fallout, verdict=sc_verdict, cta=sc_cta)
E.RED_SCENES = {"fallout", "van"}
IMPACTS = [("hook", "Not", -0.15, 0.35), ("cash", "impossible", -0.2, 0.25), ("night", "guns.", -0.1, 0.3),
           ("van", "didn't.", -0.15, 0.35), ("fallout", "never", -0.15, 0.3), ("verdict", "Goodfellas.", -0.15, 0.35),
           ("cta", "exist.", -0.2, 0.3)]
CLINKS = [("loot", "$5.8", 0.0)]
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
