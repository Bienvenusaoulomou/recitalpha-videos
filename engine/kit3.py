"""kit3 — props for EP22-EP30 (globe, mountains, dog, stone giant, frame, check, wires, casino sign)."""
import math, random, skia
from engine import *

def _sh(c, r, a, blur=16):
    p = P(C((0, 0, 0), 0.55 * a)); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur)); c.drawRRect(r, p)

def globe(c, x, y, r, a, t=0, rgb=GOLD2):
    c.drawCircle(x, y, r, P(C((22, 30, 44), a)))
    c.save(); p = skia.Path(); p.addCircle(x, y, r); c.clipPath(p, doAntiAlias=True)
    for k in range(7):  # meridians
        ph = (t * 0.35 + k / 7) % 1.0; w = r * math.cos(ph * math.pi)
        if abs(w) > 2: c.drawOval(skia.Rect(x - abs(w), y - r, x + abs(w), y + r), P(C(rgb, a * 0.35), stroke=3))
    for k in range(-2, 3):
        yy = y + k * r * 0.38; hw = math.sqrt(max(0, r * r - (yy - y) ** 2))
        c.drawLine(x - hw, yy, x + hw, yy, P(C(rgb, a * 0.3), stroke=3))
    rng = random.Random(4)  # land blobs drifting
    for i in range(6):
        bx = x + ((rng.uniform(-1.4, 1.4) + t * 0.35) % 2.8 - 1.4) * r; by = y + rng.uniform(-0.6, 0.6) * r
        c.drawOval(skia.Rect(bx - r * 0.28, by - r * 0.16, bx + r * 0.28, by + r * 0.16), P(C(rgb, a * 0.45)))
    c.restore()
    c.drawCircle(x, y, r, P(C(rgb, a), stroke=5))

def route(c, pts, k, a, rgb=RED):
    """dashed travel route through pts, revealed to fraction k"""
    if k <= 0: return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    meas = skia.PathMeasure(p, False); L = meas.getLength(); d = skia.Path(); meas.getSegment(0, L * k, d, True)
    pp = P(C(rgb, a), stroke=7); pp.setPathEffect(skia.DashPathEffect.Make([22, 14], 0)); c.drawPath(d, pp)
    for q in pts:
        c.drawCircle(q[0], q[1], 10, P(C(rgb, a)))

def mountains(c, a, y=1180, t=0, rgb=(52, 60, 56), mist=True):
    for layer, (h, col, seed) in enumerate([(420, (40, 46, 44), 2), (300, rgb, 5), (190, (68, 74, 66), 9)]):
        rng = random.Random(seed); p = skia.Path(); p.moveTo(0, y); x = 0
        while x < W + 120:
            p.lineTo(x, y - rng.uniform(0.45, 1.0) * h); x += rng.uniform(110, 220)
        p.lineTo(W, y); p.close(); c.drawPath(p, P(C(col, a)))
        rng2 = random.Random(seed + 40)
        for i in range(16):  # pines
            px = rng2.uniform(0, W); py = y - rng2.uniform(0, 0.35) * h; s = rng2.uniform(26, 46)
            tri = skia.Path(); tri.moveTo(px, py - s * 1.6); tri.lineTo(px - s * 0.5, py); tri.lineTo(px + s * 0.5, py); tri.close()
            c.drawPath(tri, P(C((28, 40, 32), a * 0.9)))
    if mist:
        for i in range(3):
            mx = (t * 30 + i * 400) % (W + 600) - 300
            g = P(C(CREAM, a * 0.07)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
            c.drawOval(skia.Rect(mx, y - 260 + i * 60, mx + 520, y - 180 + i * 60), g)

def frame(c, x, y, w, h, a, img=None, rot=0, label=None, fake=0.0):
    """gilded painting frame; img = skia.Image or None"""
    c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 36, -h / 2 - 36, w / 2 + 36, h / 2 + 36), 6, 6); _sh(c, r, a, 24)
    c.drawRect(skia.Rect(-w / 2 - 36, -h / 2 - 36, w / 2 + 36, h / 2 + 36), P(C((150, 112, 50), a)))
    c.drawRect(skia.Rect(-w / 2 - 36, -h / 2 - 36, w / 2 + 36, h / 2 + 36), P(C(GOLD2, a), stroke=6))
    c.drawRect(skia.Rect(-w / 2 - 12, -h / 2 - 12, w / 2 + 12, h / 2 + 12), P(C((96, 70, 30), a), stroke=10))
    if img is not None:
        sw, sh = img.width(), img.height(); sc = max(w / sw, h / sh); cw, ch = w / sc, h / sc
        src = skia.Rect((sw - cw) / 2, (sh - ch) / 2, (sw + cw) / 2, (sh - ch) / 2 + ch)
        pa = skia.Paint(AntiAlias=True); pa.setAlphaf(a)
        c.drawImageRect(img, src, skia.Rect(-w / 2, -h / 2, w / 2, h / 2), skia.SamplingOptions(skia.FilterMode.kLinear), pa)
    else:  # stylised "old master" portrait (no real painting)
        g = skia.Paint(AntiAlias=True); g.setShader(skia.GradientShader.MakeRadial(skia.Point(-w * 0.1, -h * 0.15), max(w, h) * 0.8,
                    [C((92, 74, 48), a), C((30, 24, 16), a)], None)); c.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), g)
        c.save(); c.clipRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2))
        sh_ = skia.Path(); sh_.moveTo(-w * 0.42, h / 2); sh_.cubicTo(-w * 0.4, h * 0.12, w * 0.4, h * 0.12, w * 0.42, h / 2); sh_.close()
        c.drawPath(sh_, P(C((60, 70, 96), a)))
        c.drawOval(skia.Rect(-w * 0.17, -h * 0.2, w * 0.17, h * 0.14), P(C((214, 180, 140), a * 0.95)))
        c.drawOval(skia.Rect(-w * 0.22, -h * 0.3, w * 0.2, -h * 0.06), P(C((44, 74, 120), a)))
        c.drawCircle(w * 0.1, h * 0.02, w * 0.018, P(C((240, 236, 220), a)))
        for i in range(14):
            y_ = -h / 2 + i * h / 13; c.drawLine(-w / 2, y_, w / 2, y_ + 8, P(C((0, 0, 0), a * 0.12), stroke=1.5))
        c.restore()
    if fake > 0:  # crack lines
        rng = random.Random(7)
        for i in range(9):
            x0, y0 = rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2); p = skia.Path(); p.moveTo(x0, y0)
            for k in range(4): x0 += rng.uniform(-60, 60); y0 += rng.uniform(-60, 60); p.lineTo(x0, y0)
            c.drawPath(p, P(C((20, 16, 12), a * fake * 0.8), stroke=3))
    if label:
        c.drawRect(skia.Rect(-150, h / 2 + 50, 150, h / 2 + 100), P(C((190, 150, 70), a)))
        text(c, label, 0, h / 2 + 87, BEBAS, 40, INK, a, spacing=4)
    c.restore()

def check(c, x, y, s, a, rot=0, payee="H. R. HUGHES", amount="$100,000", bank="McGRAW-HILL", stamp_=None):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-400, -170, 400, 170), 14, 14); _sh(c, r, a)
    c.drawRRect(r, P(C((214, 228, 206), a))); c.drawRRect(r, P(C((90, 120, 90), a), stroke=4))
    for i in range(-380, 400, 26): c.drawLine(i, -170, i + 60, 170, P(C((150, 180, 150), a * 0.25), stroke=2))
    text(c, bank, -380, -110, BEBAS, 46, (40, 70, 50), a, align="l", spacing=4)
    text(c, "PAY TO THE ORDER OF", -380, -30, BEBAS, 30, (60, 80, 60), a, align="l", spacing=3)
    text(c, payee, -380, 30, PLAY, 58, INK, a, align="l")
    c.drawLine(-380, 46, 120, 46, P(C(INK, a * 0.6), stroke=2))
    c.drawRect(skia.Rect(160, -10, 380, 60), P(C((240, 246, 236), a))); c.drawRect(skia.Rect(160, -10, 380, 60), P(C(INK, a * 0.5), stroke=2))
    text(c, amount, 270, 42, ANTON, 48, INK, a)
    text(c, "⑆ 021000 ⑆ 7734 ⑈", -380, 140, POPB, 26, (60, 80, 60), a * 0.8, align="l")
    c.restore()

def dog(c, x, y, s, a, t=0, rgb=(244, 240, 232), bow=RED):
    """small fluffy white dog (Maltese-like), sitting, facing right"""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-120, 80, 120, 110), P(C((0, 0, 0), a * 0.35)))
    wag = math.sin(t * 9) * 12
    fur = P(C(rgb, a)); ol = P(C(INK, a), stroke=10)
    blobs = [(-60, 20, 70), (0, 30, 80), (55, 25, 60), (-95, -10 + wag * 0.3, 38), (40, -50, 62), (95, -55, 52)]
    for bx, by, r in blobs: c.drawCircle(bx, by, r + 5, P(C(INK, a)))
    for bx, by, r in blobs: c.drawCircle(bx, by, r, fur)
    for i in range(10):  # fur strokes
        ang = i * 0.6; c.drawLine(-30 + 70 * math.cos(ang) * 0.6, 40 + 30 * math.sin(ang), -30 + 70 * math.cos(ang) * 0.6 + 10, 70 + 30 * math.sin(ang), P(C((210, 204, 194), a), stroke=4))
    c.drawCircle(78, -66, 9, P(C(INK, a))); c.drawCircle(81, -69, 3, P(C((255, 255, 255), a)))
    c.drawCircle(140, -40, 12, P(C(INK, a)))  # nose
    c.drawOval(skia.Rect(10, -60, 50, 10), P(C((226, 220, 210), a)))  # ear
    # bow
    bp = skia.Path(); bp.moveTo(40, -110); bp.lineTo(10, -130); bp.lineTo(10, -90); bp.close(); bp.moveTo(40, -110); bp.lineTo(70, -130); bp.lineTo(70, -90); bp.close()
    c.drawPath(bp, P(C(bow, a))); c.drawCircle(40, -110, 8, P(C(bow, a)))
    c.restore()

def stone_giant(c, x, y, s, a, rgb=(196, 186, 168), crack=0.0):
    """reclining stone giant (top view-ish), centred at x,y"""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-430, 40, 430, 110), P(C((0, 0, 0), a * 0.4)))
    st = P(C(rgb, a)); sh = P(C((150, 140, 124), a))
    body = skia.Path(); body.moveTo(-300, -40); body.cubicTo(-200, -90, 150, -80, 260, -40); body.cubicTo(300, -20, 300, 40, 260, 60)
    body.cubicTo(150, 80, -200, 80, -300, 50); body.close()
    c.drawPath(body, st); c.drawPath(body, P(C(INK, a), stroke=6))
    c.drawCircle(-360, 0, 70, st); c.drawCircle(-360, 0, 70, P(C(INK, a), stroke=6))  # head
    for lx in (-1, 1):  # legs
        lg = skia.Path(); lg.moveTo(240, lx * 26); lg.lineTo(430, lx * 34); c.drawPath(lg, P(C(rgb, a), stroke=56));
    c.drawLine(-200, -60, 60, -56, P(C((150, 140, 124), a), stroke=40))  # arm
    c.drawLine(-200, 60, 60, 56, P(C((150, 140, 124), a), stroke=40))
    for i in range(8): c.drawLine(-260 + i * 60, -30, -250 + i * 60, 30, P(C((160, 150, 132), a * 0.6), stroke=3))
    if crack > 0:
        p = skia.Path(); p.moveTo(-420, -30); p.lineTo(-300, 10); p.lineTo(-200, -20); p.lineTo(-60, 30); p.lineTo(80, -10); p.lineTo(220, 20)
        meas = skia.PathMeasure(p, False); d = skia.Path(); meas.getSegment(0, meas.getLength() * crack, d, True)
        c.drawPath(d, P(C(RED, a), stroke=8))
    c.restore()

def casino_sign(c, x, y, s, a, t=0, label="FLAMINGO", lights=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-380, -120, 380, 120), 30, 30); _sh(c, r, a, 28)
    c.drawRRect(r, P(C((30, 18, 26), a))); c.drawRRect(r, P(C((236, 110, 150), a), stroke=8))
    n = 30
    for i in range(n):
        ang = i / n
        px = -360 + 720 * ang if i < n else 0
        on = lights > 0 and (int(t * 8) + i) % 3 != 0
        for py in (-100, 100):
            c.drawCircle(px, py, 8, P(C(GOLD2 if on else (90, 70, 50), a * (lights if on else 1))))
    g = P(C((255, 120, 170), a * 0.8 * lights)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
    f = F(ANTON, 130); w_ = text_w(label, f)
    c.drawString(label, -w_ / 2, 45, f, g)
    text(c, label, 0, 45, ANTON, 130, (255, 190, 210) if lights > 0.3 else (140, 110, 120), a)
    c.restore()

def wires(c, x0, y0, x1, y1, k, a, t=0, rgb=GOLD2, n=5):
    """pulses travelling along a cable from (x0,y0) to (x1,y1)"""
    c.drawLine(x0, y0, x1, y1, P(C(MUTED, a * 0.6), stroke=6))
    for i in range(n):
        f = ((t * 0.9 + i / n) % 1.0) * k
        px, py = lerp(x0, x1, f), lerp(y0, y1, f)
        g = P(C(rgb, a)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)); c.drawCircle(px, py, 16, g)
        c.drawCircle(px, py, 8, P(C(rgb, a)))

def code_panel(c, x, y, a, code="7 3 4 1 9", reveal=1.0, label="TODAY'S CODE"):
    r = skia.RRect.MakeRectXY(skia.Rect(x - 330, y - 110, x + 330, y + 110), 16, 16); _sh(c, r, a)
    c.drawRRect(r, P(C((236, 226, 196), a))); c.drawRRect(r, P(C(INK, a), stroke=4))
    text(c, label, x, y - 50, BEBAS, 46, (90, 70, 50), a, spacing=6)
    shown = code[:int(len(code) * reveal + 0.999)] if reveal < 1 else code
    text(c, shown, x, y + 60, ANTON, 96, RED, a, spacing=8)

def lightbulb_eye(c, x, y, r, a, t=0):
    """'memorizing' eye with scanning glint"""
    c.drawOval(skia.Rect(x - r * 1.6, y - r * 0.9, x + r * 1.6, y + r * 0.9), P(C(CREAM, a)))
    c.drawOval(skia.Rect(x - r * 1.6, y - r * 0.9, x + r * 1.6, y + r * 0.9), P(C(INK, a), stroke=8))
    c.drawCircle(x + r * 0.3 * math.sin(t * 2), y, r * 0.6, P(C((60, 90, 120), a)))
    c.drawCircle(x + r * 0.3 * math.sin(t * 2), y, r * 0.3, P(C(INK, a)))
    c.drawCircle(x + r * 0.3 * math.sin(t * 2) + r * 0.15, y - r * 0.15, r * 0.1, P(C((255, 255, 255), a)))

def desk_phone(c, x, y, s, a, rot=0, t=0, ring=0.0, rgb=(36, 34, 32)):
    """1970s rotary desk phone with handset (centre of base at x,y)"""
    if a <= 0: return
    c.save(); c.translate(x + ring * 5 * math.sin(t * 55), y); c.rotate(rot + ring * 3 * math.sin(t * 40)); c.scale(s, s)
    sh = P(C((0, 0, 0), 0.5 * a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawOval(skia.Rect(-210, 90, 210, 140), sh)
    base = skia.Path(); base.moveTo(-200, 120); base.lineTo(-150, -40); base.lineTo(150, -40); base.lineTo(200, 120); base.close()
    c.drawPath(base, P(C(rgb, a))); c.drawPath(base, P(C(GOLD, a * 0.6), stroke=4))
    c.drawCircle(0, 50, 72, P(C((230, 220, 196), a))); c.drawCircle(0, 50, 72, P(C(GOLD, a * 0.6), stroke=4))
    for i in range(10):
        ang = math.radians(-60 + i * 28); c.drawCircle(52 * math.cos(ang), 50 + 52 * math.sin(ang), 11, P(C(rgb, a)))
    c.drawCircle(0, 50, 22, P(C(RED, a)))
    lift = ring * 18 * abs(math.sin(t * 20))
    hs = skia.Path(); hs.moveTo(-190, -60 - lift); hs.cubicTo(-120, -130 - lift, 120, -130 - lift, 190, -60 - lift)
    c.drawPath(hs, P(C(rgb, a), stroke=44))
    for sx in (-1, 1): c.drawOval(skia.Rect(sx * 190 - 50, -100 - lift, sx * 190 + 50, -40 - lift), P(C(rgb, a)))
    if ring > 0:
        for k in range(3):
            rr = 230 + k * 40 + (t * 120) % 40
            for sx in (-1, 1):
                arc = skia.Path(); arc.addArc(skia.Rect(-rr, -40 - rr, rr, -40 + rr), -90 + sx * 40 - 18, 36)
                c.drawPath(arc, P(C(GOLD2, a * ring * (0.8 - k * 0.22)), stroke=6))
    c.restore()
