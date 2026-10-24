import os, sys, math, random
os.environ["REC_ROOT"] = "/home/claude/ep04"
sys.path.insert(0, "/home/claude/ep04")
import skia
import engine as E
from props import *

PH = dict(cap=load_photo("brinks_cap.jpg", crop=(200, 0, 1080, 720)))

def mask(c, x, y, r, a, rgb=CREAM):
    c.drawCircle(x, y, r, P(C(rgb, a)))
    c.drawOval(skia.Rect(x - r * 0.55, y - r * 0.3, x - r * 0.15, y + r * 0.05), P(C(INK, a)))
    c.drawOval(skia.Rect(x + r * 0.15, y - r * 0.3, x + r * 0.55, y + r * 0.05), P(C(INK, a)))
    c.drawArc(skia.Rect(x - r * 0.45, y + r * 0.1, x + r * 0.45, y + r * 0.6), 10, 160, False, P(C(INK, a), stroke=max(3, r * 0.09)))

def robber(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-70, 10, 70, 200), 40, 40, P(C((34, 40, 64), a)))
    for k in range(3): c.drawCircle(0, 60 + k * 40, 6, P(C(GOLD, a)))
    mask(c, 0, -40, 52, a)
    c.drawRoundRect(skia.Rect(-60, -110, 60, -78), 10, 10, P(C((30, 30, 36), a)))
    c.drawRoundRect(skia.Rect(-70, -84, 70, -70), 6, 6, P(C((20, 20, 24), a)))
    c.restore()

def building(c, x, y, s, a, lit=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-330, -420, 330, 0), P(C((58, 48, 38), a)))
    c.drawRect(skia.Rect(-330, -420, 330, 0), P(C(GOLD, a * 0.7), stroke=4))
    for r in range(4):
        for k in range(5):
            wx, wy = -280 + k * 118, -380 + r * 88
            on = (r * 5 + k) % 3 == 0
            c.drawRect(skia.Rect(wx, wy, wx + 78, wy + 56), P(C(GOLD2 if on else (30, 26, 20), a * (0.25 + 0.75 * lit if on else 1))))
    c.drawRect(skia.Rect(-70, -110, 70, 0), P(C((24, 20, 16), a)))
    c.drawRect(skia.Rect(-330, -470, 330, -420), P(C((40, 32, 26), a)))
    text(c, "BRINK'S", 0, -432, ANTON, 44, GOLD2, a)
    c.restore()

def key(c, x, y, s, rot, a, rgb=GOLD2):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawCircle(-70, 0, 34, P(C(rgb, a), stroke=14))
    c.drawRect(skia.Rect(-38, -8, 90, 8), P(C(rgb, a)))
    for k in (40, 62, 80): c.drawRect(skia.Rect(k, 8, k + 10, 26), P(C(rgb, a)))
    c.restore()

def bag(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-50, -40); p.cubicTo(-80, 20, -70, 80, 0, 85); p.cubicTo(70, 80, 80, 20, 50, -40); p.close()
    c.drawPath(p, P(C((170, 150, 110), a))); c.drawPath(p, P(C((110, 92, 60), a), stroke=4))
    c.drawRect(skia.Rect(-30, -60, 30, -36), P(C((130, 110, 76), a)))
    text(c, "$", 0, 50, ANTON, 60, (90, 70, 40), a)
    c.restore()

def sc_hook(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "BOSTON · 1950", CX, 420, BEBAS, 90, GOLD, a, spacing=6)
    for i in range(11):
        p = eo(prog(t, 0.15 + i * 0.07, 0.3))
        x = 150 + (i % 6) * 156 + (78 if i >= 6 else 0); y = 600 + (i // 6) * 150
        mask(c, x, y - (1 - p) * 30, 56, p)
    p2 = eio(prog(t, wt("hook", "$2.7") - 0.2, 1.2))
    pop_text(c, "${:.1f} MILLION".format(2.7 * p2) if p2 < 1 else "$2.7 MILLION", CX, 1000, ANTON, 150, GOLD2 if p2 >= 1 else CREAM,
             eo(prog(t, wt("hook", "$2.7") - 0.2, 0.3)), glow=26 if p2 >= 1 else 0, glow_rgb=GOLD, s0=1.2)
    pa = eo(prog(t, wt("hook", "almost") - 0.2, 0.35))
    pill(c, "...AND ALMOST GOT AWAY WITH IT", 1170, pa, CREAM, 62, 900)

def sc_place(c, t, D):
    a = eo(prog(t, 0, 0.5))
    for i in range(70):
        R = random.Random(i); x = (R.uniform(0, W) + t * 30) % W; y = (R.uniform(300, 1200) + t * R.uniform(60, 140)) % 900 + 300
        c.drawCircle(x, y, R.uniform(2, 5), P(C(CREAM, 0.5 * a)))
    building(c, CX, 1000, 1.0, a, lit=0.5 + 0.5 * math.sin(t * 2))
    calendar(c, 850, 470, 0.6, eo(prog(t, wt("place", "17,") - 0.3, 0.3)), "17", "JAN 1950")
    pill(c, "BRINK'S DEPOT · NORTH END", 1170, eo(prog(t, wt("place", "Brink's") - 0.2, 0.3)), GOLD2, 62)

def sc_plan(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("plan", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        building(c, CX + 120, 1000, 0.8, a * (1 - out))
        # binoculars watcher
        c.drawCircle(220, 520, 50, P(C(CREAM, a * (1 - out)), stroke=10)); c.drawCircle(330, 520, 50, P(C(CREAM, a * (1 - out)), stroke=10))
        c.drawRect(skia.Rect(260, 505, 290, 535), P(C(CREAM, a * (1 - out))))
        text(c, "WATCHING FOR MONTHS", CX, 430, BEBAS, 80, CREAM, a * (1 - out), spacing=4)
    if out > 0:
        for i, (lbl, w0) in enumerate([("REMOVE THE LOCKS", "removed"), ("COPY THE KEYS", "copied"), ("PUT THEM BACK", "back.")]):
            p = eo(prog(t, wt("plan", w0) - 0.25, 0.3))
            y = 560 + i * 200
            if p > 0:
                key(c, 230, y - 25, 0.8, -20 + 20 * p, p, GOLD2 if i != 1 else CREAM)
                text(c, lbl, 360, y, ANTON, 84, CREAM, p, align="l")
        pill(c, "NO ONE NOTICED", 1170, eo(prog(t, wt("plan", "back.") + 0.3, 0.3)), GOLD2, 62)

def sc_tries(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i in range(5):
        p = eo(prog(t, 0.2 + i * 0.35, 0.25))
        x = 160 + i * 190
        calendar(c, x, 720, 0.48, p * a, str(i + 1), "TRY")
        if p > 0.5: stamp(c, x, 720, "NO", RED, 70, -14, clamp((p - 0.5) * 2))
    pill(c, "WAITING FOR THE PERFECT NIGHT", 1130, eo(prog(t, wt("tries", "perfect") - 0.3, 0.3)), GOLD2, 62, 900)

def sc_night(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "7:00 PM", CX, 450, ANTON, 120, GOLD2, a, glow=18, glow_rgb=GOLD)
    for i in range(7):
        p = eo(prog(t, wt("night", "seven", 0) - 0.3 + i * 0.12, 0.4))
        robber(c, lerp(-150, 150 + i * 130, p), 830, 0.95, p)
    seq_rows(c, t, [("PEA COATS", wt("night", "Pea") - 0.1, CREAM), ("CHAUFFEUR CAPS", wt("night", "chauffeur") - 0.1, CREAM),
                    ("RUBBER MASKS", wt("night", "rubber") - 0.1, GOLD2)], 1150, 96)

def sc_vault(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("vault", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        for i in range(5):
            p = eo(prog(t, 0.2 + i * 0.15, 0.3)) * (1 - out)
            person(c, 230 + i * 155, 780, 52, CREAM, p)
            c.drawLine(230 + i * 155 - 50, 790, 230 + i * 155 + 50, 790, P(C(RED, p), stroke=8))
        text(c, "5 EMPLOYEES TIED UP", CX, 500, ANTON, 90, CREAM, a * (1 - out))
        pill(c, "NO ONE WAS HURT", 1130, eo(prog(t, wt("vault", "hurt.") - 0.3, 0.3)) * (1 - out), GOLD2, 64)
    if out > 0:
        safe(c, CX, 700, 1.0, out, open_=prog(t, b1, 0.8))
        n = int(clamp((t - b1 - 0.4) / 1.6) * 14)
        for i in range(n): bag(c, 150 + (i % 7) * 130, 1010 + (i // 7) * 100, 0.62, out)
        text(c, "{} BAGS".format(n), CX, 450, ANTON, 110, GOLD2, out)

def sc_loot(c, t, D):
    a = eo(prog(t, 0, 0.3))
    p = eio(prog(t, wt("loot", "$1.2") - 0.2, 1.3))
    shadowed(c, lambda: text(c, "${:,.0f}".format(1_200_000 * p), CX, 560, ANTON, 160, GOLD2 if p >= 1 else CREAM, a,
                             glow=24 if p >= 1 else 0, glow_rgb=GOLD))
    text(c, "IN CASH", CX, 650, BEBAS, 72, MUTED, a, spacing=6)
    pc = eo(prog(t, wt("loot", "checks") - 0.2, 0.3))
    text(c, "+ CHECKS & MONEY ORDERS", CX, 760, BEBAS, 72, CREAM, pc, spacing=3)
    ph = prog(t, beat("loot", 1) - 0.1, 0.3)
    if ph > 0:
        for i in range(14): bag(c, 180 + (i % 7) * 120, 940 + (i // 7) * 110 - (1 - eo(clamp(ph * 2 - i * 0.05))) * 300, 0.6, clamp(ph * 2))
        pop_text(c, "≈ HALF A TON", CX, 1200, ANTON, 90, GOLD2, prog(t, beat("loot", 1) + 0.3, 0.25))

def sc_clues(c, t, D):
    a = eo(prog(t, 0, 0.5))
    photo_card(c, PH["cap"], CX, 610, 760, 600, t / D, a, 1.0, 1.12, rot=-1.5, credit="THE REAL CAP LEFT BEHIND · FBI (PUBLIC DOMAIN)")
    seq_rows(c, t, [("A CAP", wt("clues", "cap,") - 0.2, CREAM), ("SOME TAPE", wt("clues", "tape,") - 0.1, CREAM),
                    ("SOME ROPE", wt("clues", "rope.") - 0.1, CREAM)], 1140, 110)

def sc_pact(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "THE DEAL", CX, 430, BEBAS, 90, MUTED, a, spacing=10)
    c.drawRoundRect(skia.Rect(170, 500, 910, 880), 24, 24, P(C((234, 225, 202), a)))
    text(c, "NOBODY TALKS.", CX, 620, ANTON, 90, INK, eo(prog(t, wt("pact", "Nobody") - 0.2, 0.3)))
    text(c, "NOBODY SPENDS.", CX, 730, ANTON, 90, INK, eo(prog(t, wt("pact", "talks") , 0.3)))
    pr = eo(prog(t, wt("pact", "6") - 0.2, 0.3))
    text(c, "FOR 6 YEARS", CX, 830, BEBAS, 70, RED, pr, spacing=6)
    pl = eo(prog(t, wt("pact", "statute") - 0.3, 0.3))
    pill(c, "UNTIL THE STATUTE OF LIMITATIONS RUNS OUT", 1100, pl, GOLD2, 50, 960)
    if pl > 0:
        k = prog(t, wt("pact", "statute"), D - wt("pact", "statute"))
        text(c, "{}".format(1950 + int(6 * k)), CX, 1210, ANTON, 70, CREAM, pl)

def sc_greed(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("greed", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        robber(c, CX, 760, 1.6, a)
        for k in range(6): c.drawLine(300 + k * 96, 520, 300 + k * 96, 1000, P(C(MUTED, a * 0.8), stroke=10))
        text(c, "SPECS O'KEEFE", CX, 470, PLAY, 80, CREAM, a)
        pill(c, "HE WANTED HIS SHARE", 1150, eo(prog(t, wt("greed", "share.") - 0.4, 0.3)), GOLD2, 64)
        c.restore(); c.restore()
    if out > 0:
        text(c, "THE GANG SENT A HITMAN", CX, 520, ANTON, 84, RED, out)
        ps = eo(prog(t, wt("greed", "survived,") - 0.2, 0.3))
        text(c, "HE SURVIVED...", CX, 720, BEBAS, 100, CREAM, ps, spacing=6)
        pt = prog(t, wt("greed", "talked.") - 0.15, 0.25)
        pop_text(c, "AND HE TALKED.", CX, 920, ANTON, 150, GOLD2, pt, glow=26, glow_rgb=GOLD)

def sc_arrest(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("arrest", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        calendar(c, CX, 680, 1.0, a, "12", "JAN 1956")
        pd = eo(prog(t, wt("arrest", "days") - 0.3, 0.3))
        pill(c, "5 DAYS BEFORE TIME RAN OUT", 1000, pd, GOLD2, 66, 880)
        pa = prog(t, wt("arrest", "arrested") - 0.15, 0.22)
        if pa > 0: stamp(c, CX, 1150, "FBI ARREST", RED, 90, -6, pa, sc=lerp(2, 1, eo(pa)))
        c.restore(); c.restore()
    if out > 0:
        for i in range(8):
            p = eo(prog(t, b1 + i * 0.08, 0.3))
            robber(c, 150 + (i % 4) * 260, 560 + (i // 4) * 280, 0.75, p * out)
        text(c, "LIFE IN PRISON", CX, 450, ANTON, 90, RED, out)
        pr = prog(t, wt("arrest", "$58,000") - 0.2, 0.3)
        if pr > 0:
            c.drawRect(skia.Rect(0, 300, W, 1230), P(C(BG, 0.7 * eo(pr))))
            text(c, "RECOVERED:", CX, 760, BEBAS, 80, MUTED, eo(pr), spacing=6)
            pop_text(c, "~$58,000", CX, 920, ANTON, 170, GOLD2, pr, glow=24, glow_rgb=GOLD)
            text(c, "OF $2.7 MILLION", CX, 1030, BEBAS, 76, CREAM, eo(pr), spacing=4)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "NEXT EPISODE", CX, 450, BEBAS, 70, MUTED, a, spacing=10)
    # airplane silhouette
    c.save(); c.translate(lerp(-200, CX, eio(prog(t, 0, 2.0))), 680); c.rotate(-8)
    pl = skia.Path(); pl.moveTo(-240, 0); pl.lineTo(200, -10); pl.cubicTo(250, -10, 260, 10, 200, 14); pl.lineTo(-240, 14); pl.close()
    c.drawPath(pl, P(C(CREAM, a)))
    w = skia.Path(); w.moveTo(-20, 0); w.lineTo(-120, 120); w.lineTo(-60, 120); w.lineTo(60, 4); w.close(); c.drawPath(w, P(C(CREAM, a)))
    tl = skia.Path(); tl.moveTo(-220, 0); tl.lineTo(-260, -80); tl.lineTo(-210, -80); tl.lineTo(-170, 0); tl.close(); c.drawPath(tl, P(C(CREAM, a)))
    c.restore()
    text(c, "THE REAL HEIST BEHIND", CX, 880, BEBAS, 76, CREAM, eo(prog(t, wt("cta", "real") - 0.2, 0.3)), spacing=4)
    pop_text(c, "GOODFELLAS", CX, 1030, ANTON, 150, GOLD2, prog(t, wt("cta", "Goodfellas.") - 0.15, 0.25), glow=26, glow_rgb=GOLD)
    follow_pill(c, wt("cta", "Follow") - 0.1, t, 1170)

E.DRAW = dict(hook=sc_hook, place=sc_place, plan=sc_plan, tries=sc_tries, night=sc_night, vault=sc_vault, loot=sc_loot,
              clues=sc_clues, pact=sc_pact, greed=sc_greed, arrest=sc_arrest, cta=sc_cta)
E.RED_SCENES = {"greed", "arrest"}
IMPACTS = [("hook", "almost", -0.2, 0.3), ("night", "seven", -0.3, 0.25), ("loot", "half", -0.1, 0.3), ("greed", "talked.", -0.15, 0.35),
           ("arrest", "arrested", -0.15, 0.4), ("arrest", "$58,000", -0.2, 0.3), ("cta", "Goodfellas.", -0.15, 0.3)]
CLINKS = [("loot", "$1.2", 0.0)]

if __name__ == "__main__":
    E.main()
