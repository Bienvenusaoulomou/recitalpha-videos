"""More shared props (EP09+): sandwich, spray can, sensors, trash bag, trees, DNA, deposit boxes, radar, road sign,
oil tank, printing press, banknote, telegraph/radio tower, phone, plane, map pin, match, gun silhouette (wooden), bridge, mint coins..."""
import math, random
import skia
from props import *
from kit import *

def _sh(c, r, a, blur=16):
    sh = P(C((0, 0, 0), 0.55 * a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    c.drawRoundRect(r, 20, 20, sh)

def sandwich(c, x, y, s, a, bite=True, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    _sh(c, skia.Rect(-250, -60, 250, 130), a)
    bread = (214, 170, 104); crust = (150, 104, 52)
    def slab(y0, h):
        p = skia.Path(); p.addRoundRect(skia.Rect(-240, y0, 240, y0 + h), 40, 40)
        if bite:
            b = skia.Path(); b.addCircle(240, y0 + h / 2 - 10, 85); b.addCircle(170, y0 - 10, 60)
            p = skia.Op(p, b, skia.PathOp.kDifference_PathOp) or p
        c.drawPath(p, P(C(bread, a))); c.drawPath(p, P(C(crust, a), stroke=8))
    slab(40, 70)
    # salami slices + lettuce
    let = skia.Path(); let.moveTo(-250, 40)
    for k in range(13): let.lineTo(-250 + k * 40, 40 - (18 if k % 2 else 4))
    let.lineTo(250, 40); let.close(); c.drawPath(let, P(C((110, 150, 60), a)))
    for k in range(5):
        cx = -190 + k * 90
        if bite and cx > 120: continue
        c.drawCircle(cx, 30, 44, P(C((170, 50, 50), a))); c.drawCircle(cx, 30, 44, P(C((110, 30, 30), a), stroke=4))
        for d in range(4): c.drawCircle(cx - 16 + (d % 2) * 28, 18 + (d // 2) * 22, 5, P(C((236, 200, 190), a)))
    slab(-70, 90)
    for k in range(6): c.drawOval(skia.Rect(-170 + k * 55, -50, -160 + k * 55, -40), P(C((240, 226, 190), a)))
    c.restore()

def spraycan(c, x, y, s, a, spray=0.0, t=0, ang=-35):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    _sh(c, skia.Rect(-70, -150, 70, 210), a)
    c.drawRoundRect(skia.Rect(-70, -140, 70, 210), 30, 30, P(C((190, 60, 120), a)))
    c.drawRect(skia.Rect(-70, -40, 70, 60), P(C(CREAM, a)))
    text(c, "HAIR", 0, 0, ANTON, 44, INK, a); text(c, "SPRAY", 0, 46, BEBAS, 36, INK, a, spacing=3)
    c.drawRoundRect(skia.Rect(-40, -190, 40, -140), 10, 10, P(C((200, 200, 205), a)))
    c.drawRect(skia.Rect(-14, -215, 14, -190), P(C((230, 230, 235), a)))
    if spray > 0:
        rng = random.Random(7)
        for k in range(70):
            d = rng.uniform(20, 420) * spray; sp = rng.uniform(-0.35, 0.35) * (d / 420 + 0.2)
            px, py = d * math.sin(sp), -215 - d * math.cos(sp)
            c.drawCircle(px, py, rng.uniform(3, 9), P(C((235, 235, 240), a * 0.5 * (1 - d / 460))))
    c.restore()

def sensor(c, x, y, r, a, blind=0.0, t=0, label=None):
    if a <= 0: return
    c.drawCircle(x, y, r + 14, P(C((40, 38, 36), a)))
    on = (1 - blind)
    pul = 0.6 + 0.4 * math.sin(t * 8)
    g = P(C(RED, a * on * 0.5 * pul)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r))
    c.drawCircle(x, y, r * 1.6, g)
    c.drawCircle(x, y, r, P(C(tuple(int(lerp(v, 120, blind)) for v in RED), a)))
    c.drawCircle(x - r * 0.3, y - r * 0.3, r * 0.25, P(C((255, 255, 255), a * 0.5)))
    if blind > 0:
        c.drawCircle(x, y, r * 1.05, P(C((235, 235, 240), a * 0.55 * blind)))
        for sgn in (-1, 1):
            c.drawLine(x - r, y - sgn * r, x + r, y + sgn * r, P(C(CREAM, a * blind), stroke=9))
    if label: text(c, label, x, y + r + 62, BEBAS, 44, CREAM, a, spacing=4)

def trashbag(c, x, y, s, a, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    _sh(c, skia.Rect(-200, -100, 200, 220), a)
    p = skia.Path(); p.moveTo(-40, -170); p.quadTo(-230, -60, -190, 120); p.quadTo(-150, 220, 0, 220)
    p.quadTo(150, 220, 190, 120); p.quadTo(230, -60, 40, -170); p.close()
    c.drawPath(p, P(C((34, 34, 36), a))); c.drawPath(p, P(C((90, 90, 96), a), stroke=4))
    c.drawLine(-60, -30, -100, 120, P(C((80, 80, 86), a), stroke=4)); c.drawLine(50, -40, 80, 140, P(C((80, 80, 86), a), stroke=4))
    k = skia.Path(); k.moveTo(-40, -170); k.lineTo(-70, -230); k.lineTo(0, -190); k.lineTo(70, -230); k.lineTo(40, -170); k.close()
    c.drawPath(k, P(C((50, 50, 54), a)))
    c.restore()

def tree(c, x, y, s, a, rgb=(40, 62, 40)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-14, -60, 14, 0), P(C((70, 50, 34), a)))
    for k, (w, yy) in enumerate([(120, -60), (95, -150), (70, -230)]):
        p = skia.Path(); p.moveTo(-w, yy); p.lineTo(0, yy - 150); p.lineTo(w, yy); p.close()
        c.drawPath(p, P(C(tuple(v + k * 8 for v in rgb), a)))
    c.restore()

def forest(c, a, y=1180, n=9, seed=3):
    rng = random.Random(seed)
    for k in range(n):
        tree(c, 60 + k * 120 + rng.uniform(-20, 20), y + rng.uniform(-20, 30), rng.uniform(0.9, 1.4), a)

def dna(c, x, y, h, a, t, rgb1=GOLD2, rgb2=CREAM, w=150):
    if a <= 0: return
    n = 22
    for k in range(n):
        yy = y - h / 2 + k * h / (n - 1)
        ph = t * 2.5 + k * 0.45
        x1, x2 = x + w * math.sin(ph), x - w * math.sin(ph)
        z = math.cos(ph)
        c.drawLine(x1, yy, x2, yy, P(C(MUTED, a * 0.6), stroke=4))
        c.drawCircle(x1, yy, 14 + 4 * z, P(C(rgb1, a * (0.7 + 0.3 * z))))
        c.drawCircle(x2, yy, 14 - 4 * z, P(C(rgb2, a * (0.7 - 0.3 * z))))

def box_grid(c, x, y, cols, rows, a, n_open, t=0, bw=118, bh=78):
    if a <= 0: return
    x0 = x - cols * bw / 2; y0 = y - rows * bh / 2
    c.drawRect(skia.Rect(x0 - 16, y0 - 16, x0 + cols * bw + 16, y0 + rows * bh + 16), P(C((60, 56, 50), a)))
    i = 0
    order = sorted(range(cols * rows), key=lambda k: random.Random(k * 31).random())
    opened = set(order[:int(n_open)])
    for r in range(rows):
        for q in range(cols):
            k = r * cols + q
            rr = skia.Rect(x0 + q * bw + 5, y0 + r * bh + 5, x0 + (q + 1) * bw - 5, y0 + (r + 1) * bh - 5)
            if k in opened:
                c.drawRect(rr, P(C((14, 12, 10), a)))
                c.drawRect(rr, P(C(RED, a * 0.8), stroke=3))
            else:
                c.drawRect(rr, P(C((150, 140, 120), a)))
                c.drawRect(rr, P(C((200, 186, 150), a), stroke=2))
                c.drawCircle(rr.centerX(), rr.centerY(), 9, P(C((90, 84, 72), a)))

def radar(c, x, y, r, a, t, rgb=(120, 220, 140)):
    if a <= 0: return
    for k in range(1, 4): c.drawCircle(x, y, r * k / 3, P(C(rgb, a * 0.5), stroke=3))
    c.drawLine(x - r, y, x + r, y, P(C(rgb, a * 0.3), stroke=2)); c.drawLine(x, y - r, x, y + r, P(C(rgb, a * 0.3), stroke=2))
    ang = t * 2.4
    for k in range(18):
        aa = ang - k * 0.05
        c.drawLine(x, y, x + r * math.cos(aa), y + r * math.sin(aa), P(C(rgb, a * 0.6 * (1 - k / 18)), stroke=5))

def road_sign(c, x, y, s, a, label="E19", sub="ANTWERP · BRUSSELS", rgb=(30, 110, 60)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-12, 0, 12, 260), P(C((120, 120, 120), a)))
    c.drawRoundRect(skia.Rect(-260, -150, 260, 20), 18, 18, P(C(rgb, a)))
    c.drawRoundRect(skia.Rect(-250, -140, 250, 10), 14, 14, P(C(CREAM, a), stroke=4))
    text(c, label, 0, -50, ANTON, 90, CREAM, a)
    text(c, sub, 0, -5, BEBAS, 36, CREAM, a, spacing=3)
    c.restore()

def diamonds_field(c, t, a, n=18, seed=5, y0=380, y1=1240, fall=True, s=0.32):
    if a <= 0: return
    rng = random.Random(seed)
    for k in range(n):
        x = rng.uniform(80, W - 80); sp = rng.uniform(120, 260); ph = rng.uniform(0, 10)
        yy = y0 + ((t * sp + ph * 100) % (y1 - y0)) if fall else rng.uniform(y0, y1)
        diamond(c, x, yy, s * rng.uniform(0.6, 1.2), a * 0.9, t + ph)

def pin(c, x, y, s, a, rgb=RED, label=None):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 0); p.quadTo(-70, -90, -60, -130); p.arcTo(skia.Rect(-60, -190, 60, -70), 180, 180, False)
    p.quadTo(70, -90, 0, 0); p.close()
    c.drawPath(p, P(C(rgb, a))); c.drawCircle(0, -130, 24, P(C(CREAM, a)))
    if label: text(c, label, 0, 60, BEBAS, 48, CREAM, a, spacing=4)
    c.restore()

def banknote(c, x, y, s, a, rot=0, value="500", sub="ESCUDOS", rgb=(150, 170, 140), portrait=True):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    _sh(c, skia.Rect(-330, -150, 330, 170), a)
    c.drawRoundRect(skia.Rect(-340, -160, 340, 160), 14, 14, P(C(rgb, a)))
    c.drawRoundRect(skia.Rect(-322, -142, 322, 142), 10, 10, P(C(tuple(max(0, v - 50) for v in rgb), a), stroke=4))
    if portrait:
        c.drawOval(skia.Rect(-120, -110, 120, 110), P(C(tuple(min(255, v + 40) for v in rgb), a)))
        c.drawCircle(0, -20, 46, P(C(tuple(max(0, v - 60) for v in rgb), a)))
        b = skia.Path(); b.moveTo(-80, 100); b.quadTo(0, 10, 80, 100); b.close(); c.drawPath(b, P(C(tuple(max(0, v - 60) for v in rgb), a)))
    text(c, value, -230, -60, ANTON, 80, INK, a); text(c, value, 230, 110, ANTON, 80, INK, a)
    text(c, sub, 230, -80, BEBAS, 40, INK, a, spacing=3)
    c.restore()

def oil_tank(c, x, y, s, a, level=0.8, water=0.0, t=0, label="SOYBEAN OIL", xray=0.0):
    """storage tank; xray>0 shows the inside: a thin oil layer floating on water"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Rect(-200, -330, 200, 0)
    c.drawRect(body, P(C((150, 150, 146), a)))
    c.drawOval(skia.Rect(-200, -360, 200, -300), P(C((180, 180, 176), a)))
    c.drawOval(skia.Rect(-200, -30, 200, 30), P(C((120, 120, 116), a)))
    if xray > 0:
        c.save(); c.clipRect(body)
        lv = -330 * level
        c.drawRect(skia.Rect(-200, lv, 200, 0), P(C((70, 120, 170), a * xray)))           # water
        oil_h = 330 * (1 - water) * level if water < 1 else 0
        c.drawRect(skia.Rect(-200, lv, 200, lv + max(14, oil_h)), P(C((222, 176, 60), a * xray)))  # oil on top
        for k in range(6):
            yy = lv + 30 + k * 45
            c.drawLine(-200, yy + 6 * math.sin(t * 2 + k), 200, yy + 6 * math.sin(t * 2 + k + 1), P(C((140, 180, 220), a * xray * 0.4), stroke=3))
        c.restore()
    for k in range(4): c.drawLine(-200, -80 * k - 40, 200, -80 * k - 40, P(C((110, 110, 106), a), stroke=3))
    c.drawRect(body, P(C((90, 90, 86), a), stroke=4))
    if label and xray < 0.5: text(c, label, 0, -150, ANTON, 46, INK, a * (1 - xray * 2))
    c.restore()

def press(c, x, y, s, a, t=0, rgb=(64, 58, 50)):
    """printing press with paper sheets coming out"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-260, -220, 260, 60), P(C(rgb, a)))
    c.drawRect(skia.Rect(-260, -220, 260, 60), P(C(GOLD, a * 0.7), stroke=4))
    for k, cx in enumerate((-130, 130)):
        c.save(); c.translate(cx, -80); c.rotate(t * 200 * (1 if k else -1))
        c.drawCircle(0, 0, 90, P(C((110, 100, 86), a))); c.drawCircle(0, 0, 90, P(C(GOLD, a), stroke=5))
        for q in range(6):
            ang = q * math.pi / 3; c.drawLine(0, 0, 80 * math.cos(ang), 80 * math.sin(ang), P(C(GOLD, a), stroke=5))
        c.restore()
    c.drawRect(skia.Rect(-300, 60, 300, 90), P(C((40, 36, 30), a)))
    c.restore()

def tower_radio(c, x, y, s, a, t=0, waves=True):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-90, 0); p.lineTo(0, -420); p.lineTo(90, 0)
    c.drawPath(p, P(C(CREAM, a), stroke=8))
    for k in range(6):
        yy = -k * 70; w = 90 * (1 - k / 6)
        c.drawLine(-w, yy, w, yy - 70, P(C(CREAM, a * 0.7), stroke=4)); c.drawLine(w, yy, -w, yy - 70, P(C(CREAM, a * 0.7), stroke=4))
    c.drawCircle(0, -430, 16, P(C(RED, a)))
    if waves:
        for k in range(3):
            f = (t * 0.8 + k / 3) % 1
            c.drawArc(skia.Rect(-60 - 260 * f, -490 - 260 * f, 60 + 260 * f, -370 + 260 * f), -150, 120, False, P(C(GOLD2, a * (1 - f)), stroke=6))
    c.restore()

def phone(c, x, y, s, a, rot=0, t=0, ring=0.0):
    """1990s brick mobile phone"""
    if a <= 0: return
    c.save(); c.translate(x, y + ring * 6 * math.sin(t * 60)); c.rotate(rot); c.scale(s, s)
    _sh(c, skia.Rect(-90, -240, 90, 240), a)
    c.drawRoundRect(skia.Rect(-90, -240, 90, 240), 30, 30, P(C((40, 40, 44), a)))
    c.drawRect(skia.Rect(-30, -330, -10, -240), P(C((40, 40, 44), a)))
    c.drawRoundRect(skia.Rect(-65, -190, 65, -70), 10, 10, P(C((120, 160, 110), a)))
    for r in range(4):
        for q in range(3): c.drawRoundRect(skia.Rect(-60 + q * 45, -30 + r * 52, -25 + q * 45, 4 + r * 52), 8, 8, P(C((90, 90, 96), a)))
    c.restore()

def plane(c, x, y, s, a, rot=0, rgb=CREAM):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-200, -24, 200, 24), 24, 24, P(C(rgb, a)))
    w = skia.Path(); w.moveTo(-40, 0); w.lineTo(40, -170); w.lineTo(80, -170); w.lineTo(60, 0); w.close(); c.drawPath(w, P(C(rgb, a)))
    w2 = skia.Path(); w2.moveTo(-40, 0); w2.lineTo(40, 170); w2.lineTo(80, 170); w2.lineTo(60, 0); w2.close(); c.drawPath(w2, P(C(rgb, a)))
    tl = skia.Path(); tl.moveTo(-200, 0); tl.lineTo(-180, -80); tl.lineTo(-150, -80); tl.lineTo(-140, 0); tl.close(); c.drawPath(tl, P(C(rgb, a)))
    c.drawCircle(200, 0, 12, P(C(GOLD2, a)))
    c.restore()

def clock(c, x, y, r, a, t_h=9.75, label=None):
    if a <= 0: return
    c.drawCircle(x, y, r, P(C(CREAM, a))); c.drawCircle(x, y, r, P(C(GOLD, a), stroke=8))
    for k in range(12):
        ang = k * math.pi / 6
        c.drawLine(x + r * 0.82 * math.sin(ang), y - r * 0.82 * math.cos(ang), x + r * 0.95 * math.sin(ang), y - r * 0.95 * math.cos(ang), P(C(INK, a), stroke=5))
    mh = (t_h % 12) / 12 * 2 * math.pi; mm = (t_h % 1) * 2 * math.pi
    c.drawLine(x, y, x + r * 0.5 * math.sin(mh), y - r * 0.5 * math.cos(mh), P(C(INK, a), stroke=10))
    c.drawLine(x, y, x + r * 0.78 * math.sin(mm), y - r * 0.78 * math.cos(mm), P(C(INK, a), stroke=6))
    c.drawCircle(x, y, 10, P(C(RED, a)))
    if label: text(c, label, x, y + r + 70, BEBAS, 54, CREAM, a, spacing=4)

def matchbox(c, x, y, s, a, rot=0, label="SAFETY MATCHES"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    _sh(c, skia.Rect(-220, -140, 220, 140), a)
    c.drawRoundRect(skia.Rect(-220, -140, 220, 140), 10, 10, P(C((200, 60, 40), a)))
    c.drawRect(skia.Rect(-220, -140, 220, -110), P(C((60, 40, 30), a)))
    c.drawRect(skia.Rect(-220, 110, 220, 140), P(C((60, 40, 30), a)))
    c.drawCircle(0, -10, 60, P(C(CREAM, a))); text(c, "K", 0, 15, ANTON, 70, (200, 60, 40), a)
    text(c, label, 0, 90, BEBAS, 40, CREAM, a, spacing=4)
    c.restore()

def match(c, x, y, s, a, t=0, lit=1.0, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-10, -10, 10, 300), P(C((222, 190, 140), a)))
    c.drawOval(skia.Rect(-20, -50, 20, 0), P(C((170, 40, 30), a)))
    if lit > 0:
        fl = 1 + 0.12 * math.sin(t * 23) + 0.08 * math.sin(t * 37)
        g = P(C((255, 170, 60), a * 0.5 * lit)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
        c.drawCircle(0, -70, 90 * fl, g)
        fp = skia.Path(); fp.moveTo(-28, -40); fp.quadTo(-34, -110 * fl, 0, -150 * fl); fp.quadTo(34, -110 * fl, 28, -40); fp.close()
        c.drawPath(fp, P(C((255, 190, 70), a * lit)))
        ip = skia.Path(); ip.moveTo(-12, -40); ip.quadTo(-14, -80, 0, -100 * fl); ip.quadTo(14, -80, 12, -40); ip.close()
        c.drawPath(ip, P(C((255, 245, 200), a * lit)))
    c.restore()

def pistol(c, x, y, s, a, rot=0, rgb=(150, 104, 60), grain=True):
    """simple pistol silhouette; brown + grain = carved wood"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(-220, -60); p.lineTo(200, -60); p.lineTo(200, 0); p.lineTo(-40, 0)
    p.lineTo(-40, 20); p.lineTo(-80, 20); p.lineTo(-60, 190); p.lineTo(-170, 190); p.lineTo(-200, 10); p.lineTo(-220, 0); p.close()
    c.drawPath(p, P(C(rgb, a)))
    if grain:
        for k in range(7): c.drawLine(-210, -50 + k * 8, 190, -48 + k * 8 + 3 * math.sin(k), P(C(tuple(max(0, v - 40) for v in rgb), a * 0.6), stroke=2))
        for k in range(5): c.drawLine(-170 + k * 4, 30 + k * 30, -80 + k * 3, 30 + k * 30, P(C(tuple(max(0, v - 40) for v in rgb), a * 0.6), stroke=2))
    c.drawPath(p, P(C(tuple(max(0, v - 60) for v in rgb), a), stroke=4))
    tg = skia.Path(); tg.addCircle(-60, 40, 26); c.drawPath(tg, P(C(tuple(max(0, v - 60) for v in rgb), a), stroke=5))
    c.restore()

def bridge(c, x, y, s, a, rgb=(150, 136, 110)):
    """Brooklyn-Bridge-like silhouette (two gothic towers + cables)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-520, -40, 520, 0), P(C(rgb, a)))
    for tx in (-260, 260):
        c.drawRect(skia.Rect(tx - 60, -460, tx + 60, 0), P(C(rgb, a)))
        for ax in (tx - 30, tx + 30):
            ar = skia.Path(); ar.moveTo(ax - 18, -180); ar.lineTo(ax - 18, -330); ar.quadTo(ax, -370, ax + 18, -330); ar.lineTo(ax + 18, -180); ar.close()
            c.drawPath(ar, P(C(BG, a)))
    for sgn in (-1, 1):
        cab = skia.Path(); cab.moveTo(-260, -450); cab.quadTo(0, -60, 260, -450); c.drawPath(cab, P(C(rgb, a), stroke=6))
    for tx, d in ((-260, -1), (260, 1)):
        cab = skia.Path(); cab.moveTo(tx, -450); cab.quadTo(tx + d * 160, -150, tx + d * 270, -40); c.drawPath(cab, P(C(rgb, a), stroke=6))
    for k in range(-9, 10):
        xx = k * 26
        yy = -450 + (1 - (xx / 260) ** 2) * 390 * 0.5 + 0  # approx cable curve
        c.drawLine(xx, -40, xx, min(-40, -450 + 390 * (1 - (xx / 260) ** 2) * 0.5 + 195), P(C(rgb, a * 0.6), stroke=2))
    c.restore()

def ticket(c, x, y, s, a, rot=0, head="CERTIFICATE", title="", sub="", rgb=(232, 222, 196)):
    """certificate / bond / receipt"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    _sh(c, skia.Rect(-360, -220, 360, 240), a)
    c.drawRect(skia.Rect(-370, -230, 370, 230), P(C(rgb, a)))
    c.drawRect(skia.Rect(-345, -205, 345, 205), P(C(GOLD, a), stroke=5))
    c.drawRect(skia.Rect(-330, -190, 330, 190), P(C(GOLD, a * 0.6), stroke=2))
    text(c, head, 0, -120, PLAY, 58, INK, a)
    sz = 72
    while text_w(title, F(ANTON, sz)) > 620 and sz > 30: sz -= 2
    text(c, title, 0, 0, ANTON, sz, INK, a)
    text(c, sub, 0, 70, BEBAS, 42, (100, 86, 60), a, spacing=4)
    c.drawCircle(250, 140, 46, P(C(RED, a * 0.8)))
    c.restore()
