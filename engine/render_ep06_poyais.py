import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep06")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *

PH = dict(mac=load_photo("macgregor.jpg", crop=(0, 0, 500, 560)),
          note=load_photo("note.jpg"),
          port=load_photo("port.png"))
CR_MAC = "S.W. REYNOLDS AFTER S.J. ROCHARD · PUBLIC DOMAIN"
CR_NOTE = "REAL POYAIS NOTE · SMITHSONIAN NMAH · PUBLIC DOMAIN"
CR_PORT = "FROM THE 1822 POYAIS GUIDEBOOK · PUBLIC DOMAIN"
GREEN = (60, 86, 52)

def land(c, x, y, s, a, rgb=GREEN):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-300, -40); p.cubicTo(-220, -170, 40, -190, 170, -110); p.cubicTo(320, -30, 240, 110, 70, 140)
    p.cubicTo(-90, 160, -330, 110, -300, -40); p.close()
    c.drawPath(p, P(C(rgb, a))); c.drawPath(p, P(C(GOLD, a), stroke=5))
    c.restore()

def ship(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y + 6 * math.sin(t * 2)); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-160, 0); hull.lineTo(160, 0); hull.lineTo(120, 60); hull.lineTo(-120, 60); hull.close()
    c.drawPath(hull, P(C((70, 50, 34), a)))
    for mx in (-60, 50):
        c.drawLine(mx, 0, mx, -220, P(C(CREAM, a), stroke=6))
        sl = skia.Path(); sl.moveTo(mx - 60, -200); sl.quadTo(mx + 10, -150, mx - 60, -40); sl.lineTo(mx + 60, -40); sl.quadTo(mx + 80, -150, mx + 60, -200); sl.close()
        c.drawPath(sl, P(C(CREAM, a * 0.92)))
    c.restore()

def waves(c, y, a, t):
    for k in range(4):
        p = skia.Path(); yy = y + k * 34
        p.moveTo(0, yy)
        for x in range(0, W + 40, 40): p.lineTo(x, yy + 8 * math.sin(x / 60 + t * 2 + k))
        c.drawPath(p, P(C((90, 120, 140), a * (0.5 - k * 0.1)), stroke=4))

def palm(c, x, y, s, a, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    tr = skia.Path(); tr.moveTo(-10, 0); tr.quadTo(10, -150, 30, -300); tr.lineTo(46, -300); tr.quadTo(26, -150, 14, 0); tr.close()
    c.drawPath(tr, P(C((60, 44, 30), a)))
    for k in range(6):
        ang = math.radians(-160 + k * 28 + 4 * math.sin(t * 1.5 + k))
        lf = skia.Path(); lf.moveTo(38, -300)
        ex, ey = 38 + 150 * math.cos(ang), -300 + 150 * math.sin(ang) + 60
        lf.quadTo(38 + 90 * math.cos(ang), -300 + 90 * math.sin(ang) - 30, ex, ey)
        c.drawPath(lf, P(C((50, 90, 50), a), stroke=16))
    c.restore()

def bond(c, x, y, s, rot, a):
    paper_doc(c, x, y, s, rot, a, "GOVERNMENT OF POYAIS", "LONDON · 1822", "BOND", lines=6)

# ---------------- scenes ----------------
def sc_hook(c, t, D):
    text(c, "A COUNTRY", CX, 450, ANTON, 120, CREAM, 1.0)
    text(c, "THAT NEVER EXISTED", CX, 570, ANTON, 104, GOLD2, 1.0, glow=20, glow_rgb=GOLD)
    land(c, CX, 820, 1.0, 1.0)
    text(c, "POYAIS", CX, 840, PLAY, 80, CREAM, 1.0)
    for i in range(10):
        p = eo(prog(t, 0.3 + i * 0.12, 0.4))
        person(c, 140 + i * 89, 1190, 28, CREAM, p)
    b1 = beat("hook", 1)
    for i, (lbl, w0) in enumerate([("FAKE MAPS", "maps,"), ("FAKE MONEY", "money,"), ("FAKE DEEDS", "deeds")]):
        p = prog(t, wt("hook", w0) - 0.15, 0.22)
        if p > 0: stamp(c, (270, 810, CX)[i], (990, 990, 1090)[i], lbl, RED, 60, (-10, 8, -4)[i], p, sc=lerp(2, 1, eo(p)))

def sc_man(c, t, D):
    a = eo(prog(t, 0, 0.4))
    photo_card(c, PH["mac"], CX, 750, 560, 600, t / D, a, 1.0, 1.12, focus=(0.5, 0.3), rot=-1.5, credit=CR_MAC)
    text(c, "GREGOR MACGREGOR", CX, 400, PLAY, 70, CREAM, eo(prog(t, wt("man", "Gregor") - 0.3, 0.3)))
    pc = eo(prog(t, wt("man", "London") - 0.3, 0.3))
    pill(c, "LONDON · 1821", 1160, pc * (1 - eo(prog(t, wt("man", "Cazique") - 0.5, 0.2))), CREAM, 62, 560)
    pz = prog(t, wt("man", "Cazique") - 0.2, 0.25)
    pop_text(c, "\"CAZIQUE OF POYAIS\"", CX, 1170, ANTON, 84, GOLD2, pz, glow=18, glow_rgb=GOLD)

def sc_claim(c, t, D):
    a = eo(prog(t, 0, 0.4))
    # coastline of Central America (stylized)
    p = skia.Path(); p.moveTo(120, 520); p.cubicTo(300, 600, 420, 640, 560, 660); p.cubicTo(720, 680, 860, 640, 980, 700)
    p.lineTo(980, 1100); p.lineTo(120, 1100); p.close()
    c.drawPath(p, P(C((52, 64, 44), a))); c.drawPath(p, P(C(GOLD, a * 0.7), stroke=4))
    text(c, "CENTRAL AMERICA", CX, 470, BEBAS, 80, CREAM, a, spacing=6)
    b1 = beat("claim", 1)
    pg = eo(prog(t, b1 - 0.3, 0.6))
    if pg > 0:
        r = skia.Rect(560, 690, 940, 960)
        c.drawRoundRect(r, 20, 20, P(C(GOLD2, 0.35 * pg))); c.drawRoundRect(r, 20, 20, P(C(GOLD2, pg), stroke=6))
        k = eio(prog(t, wt("claim", "12,500") - 0.2, 1.0))
        text(c, "{:,} SQ MI".format(int(12500 * k)), 750, 850, ANTON, 64, CREAM, pg)
    pb = prog(t, wt("claim", "Belgium.") - 0.2, 0.25)
    pop_text(c, "BIGGER THAN BELGIUM", CX, 1170, ANTON, 90, GOLD2, pb, glow=18, glow_rgb=GOLD)

def sc_guide(c, t, D):
    a = eo(prog(t, 0, 0.4))
    out = eo(prog(t, wt("guide", "St.") - 0.6, 0.3))
    if out < 1:
        paper_doc(c, CX, 760, 0.85, -3, a * (1 - out), "SKETCH OF THE", "MOSQUITO SHORE · 1822", "POYAIS", lines=7)
        text(c, "THE GUIDEBOOK", CX, 420, ANTON, 96, CREAM, a * (1 - out))
        pill(c, "RICH SOIL", 1150, eo(prog(t, wt("guide", "Rich") - 0.2, 0.3)) * (1 - out), GOLD2, 64, 480)
    if out > 0:
        photo_card(c, PH["port"], CX, 720, 900, 560, (t - wt("guide", "St.")) / 4, out, 1.0, 1.1, credit=CR_PORT)
        text(c, "CAPITAL: \"ST. JOSEPH\"", CX, 400, ANTON, 84, GOLD2, out)
        pill(c, "A BUSY PORT...?", 1150, eo(prog(t, wt("guide", "busy") - 0.2, 0.3)), CREAM, 64, 600)

def sc_bonds(c, t, D):
    a = eo(prog(t, 0, 0.4))
    for i in range(4):
        p = eo(prog(t, 0.1 + i * 0.25, 0.4))
        bond(c, CX - 120 + i * 80, 780 - i * 20, 0.62, -12 + i * 8, p * a)
    text(c, "LONDON INVESTORS", CX, 420, ANTON, 92, CREAM, a)
    b1 = beat("bonds", 1)
    k = eio(prog(t, b1 - 0.1, 1.1))
    if k > 0:
        c.drawRect(skia.Rect(0, 980, W, 1230), P(C(BG, 0.6 * clamp(k * 3))))
        shadowed(c, lambda: text(c, "£{:,.0f}".format(200000 * k), CX, 1130, ANTON, 150, GOLD2 if k >= 1 else CREAM, clamp(k * 3),
                                 glow=24 if k >= 1 else 0, glow_rgb=GOLD))

def sc_money(c, t, D):
    a = eo(prog(t, 0, 0.4))
    photo_card(c, PH["note"], CX, 700, 900, 454, t / D, a, 1.0, 1.08, rot=1.2, credit=CR_NOTE)
    seq_rows(c, t, [("REAL BRITISH MONEY", wt("money", "real") - 0.1, CREAM), ("FOR POYAIS DOLLARS", wt("money", "Poyais") - 0.2, GOLD2)], 430, 88)
    pw = prog(t, wt("money", "dollars.") + 0.3, 0.25)
    if pw > 0: stamp(c, CX, 1080, "WORTHLESS", RED, 100, -6, pw, sc=lerp(2, 1, eo(pw)))

def sc_sail(c, t, D):
    a = eo(prog(t, 0, 0.4))
    waves(c, 900, a, t)
    ship(c, lerp(-250, 380, eo(prog(t, 0.2, 2.5))), 880, 0.9, a, t)
    ship(c, lerp(-250, 760, eo(prog(t, wt("sail", "1823,") - 0.4, 2.5))), 900, 0.75, a, t + 1)
    text(c, "1822", 260, 470, ANTON, 110, GOLD2, eo(prog(t, wt("sail", "1822") - 0.3, 0.3)))
    text(c, "1823", 820, 470, ANTON, 110, GOLD2, eo(prog(t, wt("sail", "1823,") - 0.3, 0.3)))
    pp = prog(t, wt("sail", "250") - 0.2, 0.25)
    pop_text(c, "~250 SETTLERS", CX, 1170, ANTON, 100, CREAM, pp)

def sc_arrival(c, t, D):
    a = eo(prog(t, 0, 0.4))
    for i in range(7):
        palm(c, 80 + i * 160, 1120 + (i % 2) * 30, 0.9 + 0.2 * (i % 3), a, t + i)
    c.drawRect(skia.Rect(46, 1080, W - 46, 1225), P(C((40, 50, 34), a * 0.8)))
    rows = [("NO CAPITAL", wt("arrival", "capital.") - 0.2, CREAM), ("NO ROADS", wt("arrival", "roads.") - 0.2, CREAM),
            ("NO PORT", wt("arrival", "port.") - 0.2, CREAM), ("JUST JUNGLE & SWAMP", wt("arrival", "jungle") - 0.3, GOLD2)]
    seq_rows(c, t, rows, 560, 110)

def sc_disease(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "FEVER", CX, 450, ANTON, 130, RED, a, glow=20, glow_rgb=RED)
    b1 = beat("disease", 1)
    k = clamp((t - b1 + 0.2) / 1.6)
    for i in range(25):
        x = 170 + (i % 5) * 185; y = 600 + (i // 5) * 110
        dead = i < int(k * 18)
        person(c, x, y, 34, MUTED if dead else CREAM, a * (0.25 if dead else 1))
    pp = prog(t, wt("disease", "180") - 0.2, 0.25)
    if pp > 0:
        c.drawRect(skia.Rect(0, 1060, W, 1230), P(C(BG, 0.7 * eo(pp))))
        pop_text(c, "180+ DIED", CX, 1170, ANTON, 120, CREAM, pp)

def sc_rescue(c, t, D):
    a = eo(prog(t, 0, 0.4))
    land(c, CX, 760, 1.1, a)
    pin = eo(prog(t, wt("rescue", "Belize.") - 0.3, 0.3))
    c.drawCircle(CX + 60, 720, 22, P(C(RED, pin))); c.drawCircle(CX + 60, 720, 40, P(C(RED, pin * 0.6), stroke=6))
    text(c, "BRITISH HONDURAS", CX, 450, ANTON, 90, CREAM, a)
    text(c, "TODAY: BELIZE", CX, 540, BEBAS, 70, MUTED, pin, spacing=6)
    b1 = beat("rescue", 1)
    pf = prog(t, wt("rescue", "50") - 0.2, 0.25)
    if pf > 0:
        c.drawRect(skia.Rect(0, 980, W, 1230), P(C(BG, 0.6 * eo(pf))))
        pop_text(c, "FEWER THAN 50", CX, 1090, ANTON, 120, GOLD2, pf, glow=20, glow_rgb=GOLD)
        text(c, "MADE IT HOME", CX, 1180, BEBAS, 72, CREAM, eo(pf), spacing=6)

def sc_france(c, t, D):
    a = eo(prog(t, 0, 0.4))
    b1 = beat("france", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    photo_card(c, PH["mac"], CX, 720, 520, 600, t / D, a, 1.05, 1.15, focus=(0.5, 0.3), credit=CR_MAC, dim=0.25 * out)
    text(c, "AND MACGREGOR?", CX, 380, ANTON, 90, CREAM, a * (1 - out))
    pf = eo(prog(t, wt("france", "France.") - 0.3, 0.3)) * (1 - out)
    pill(c, "SAME SCAM · FRANCE", 1160, pf * (1 - eo(prog(t, wt("france", "acquitted.") - 0.4, 0.2))), CREAM, 62, 680)
    pq = prog(t, wt("france", "acquitted.") - 0.15, 0.22)
    if pq > 0 and out < 1:
        c.save(); layer_alpha(c, 1 - out); stamp(c, CX, 1130, "ACQUITTED", GOLD2, 110, -6, pq, sc=lerp(2, 1, eo(pq))); c.restore(); c.restore()
    if out > 0:
        text(c, "DIED IN VENEZUELA · 1845", CX, 380, ANTON, 76, CREAM, out)
        pill(c, "WITH A WAR HERO'S PENSION", 1160, eo(prog(t, wt("france", "pension") - 0.2, 0.3)), GOLD2, 62, 880)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "NEXT EPISODE", CX, 450, BEBAS, 70, MUTED, a, spacing=10)
    # woman silhouette with a bank behind
    c.save(); layer_alpha(c, a)
    c.drawRect(skia.Rect(240, 560, 840, 900), P(C((58, 48, 38))))
    for k in range(5): c.drawRect(skia.Rect(280 + k * 120, 620, 320 + k * 120, 880), P(C((90, 76, 56))))
    tri = skia.Path(); tri.moveTo(210, 560); tri.lineTo(CX, 470); tri.lineTo(870, 560); tri.close(); c.drawPath(tri, P(C((70, 58, 44))))
    text(c, "BANK", CX, 545, ANTON, 50, GOLD2, 1)
    c.restore(); c.restore()
    c.drawCircle(CX, 700, 64, P(C(CREAM, a)))
    dress = skia.Path(); dress.moveTo(CX - 55, 765); dress.lineTo(CX + 55, 765); dress.lineTo(CX + 140, 920); dress.lineTo(CX - 140, 920); dress.close()
    c.drawPath(dress, P(C(CREAM, a)))
    text(c, "CARNEGIE'S", CX, 1010, ANTON, 84, CREAM, eo(prog(t, wt("cta", "Carnegie's") - 0.3, 0.3)))
    pop_text(c, "SECRET DAUGHTER?", CX, 1100, ANTON, 84, GOLD2, prog(t, wt("cta", "daughter.") - 0.15, 0.25), glow=20, glow_rgb=GOLD)
    pf = prog(t, wt("cta", "Follow") - 0.1, 0.4)
    if pf > 0:
        follow_pill(c, wt("cta", "Follow") - 0.1, t, 1190)

E.DRAW = dict(hook=sc_hook, man=sc_man, claim=sc_claim, guide=sc_guide, bonds=sc_bonds, money=sc_money, sail=sc_sail,
              arrival=sc_arrival, disease=sc_disease, rescue=sc_rescue, france=sc_france, cta=sc_cta)
E.RED_SCENES = {"disease"}
IMPACTS = [("hook", "deeds", -0.15, 0.35), ("claim", "Belgium.", -0.2, 0.3), ("money", "dollars.", 0.3, 0.3),
           ("arrival", "jungle", -0.3, 0.3), ("disease", "180", -0.2, 0.35), ("france", "acquitted.", -0.15, 0.35),
           ("cta", "daughter.", -0.15, 0.3)]
CLINKS = [("bonds", "£200,000.", 0.0)]
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
