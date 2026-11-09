"""kit4 — props for EP32-EP34 (Dec 2026 new format): euro note, shield, snowflake, exchange box, laptop, crypto coin,
video-call screen with deepfake glitch, jewelled glove, court gavel/scales, oil derrick."""
import math, random, skia
from engine import *

GREEN = (90, 255, 160)
BLUE = (60, 120, 200)

def _sh(c, r, a, blur=16):
    p = P(C((0, 0, 0), 0.55 * a)); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur)); c.drawRRect(r, p)

def laptop(c, x, y, s, a, t=0, label=None, glow=1.0, rgb=GREEN):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-170, -230, 170, 0), 14, 14, P(C((40, 42, 48), a)))
    c.drawRect(skia.Rect(-152, -212, 152, -18), P(C((8, 14, 12), a)))
    rng = random.Random(3)
    for i in range(9):
        w = rng.uniform(60, 260); off = (t * 40 + i * 21) % 190
        c.drawRect(skia.Rect(-140, -200 + off, -140 + w, -194 + off), P(C(rgb, a * 0.6 * glow)))
    if label: text(c, label, 0, -100, ANTON, 44, rgb, a * glow)
    c.drawRoundRect(skia.Rect(-210, 0, 210, 26), 10, 10, P(C((70, 72, 80), a)))
    c.restore()

def crypto_coin(c, x, y, r, a, t=0, sym="B"):
    sq = abs(math.cos(t * 3 + x * 0.01))
    c.save(); c.translate(x, y); c.scale(max(0.15, sq), 1)
    c.drawCircle(0, 0, r, P(C(GOLD2, a))); c.drawCircle(0, 0, r * 0.8, P(C(GOLD, a), stroke=r * 0.12))
    text(c, sym, 0, r * 0.36, ANTON, r * 1.05, INK, a)
    c.restore()

def euro_note(c, x, y, s, a, rot=0, value="500", rgb=(150, 120, 190)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-150, -75, 150, 75), 10, 10); _sh(c, r, a, 10)
    c.drawRRect(r, P(C(rgb, a)))
    c.drawRect(skia.Rect(-150, -75, -70, 75), P(C(tuple(min(255, v + 40) for v in rgb), a)))
    for k in range(4): c.drawLine(-40 + k * 30, -60, -10 + k * 30, 60, P(C(INK, a * 0.15), stroke=4))
    text(c, "€" + value, 70, 28, ANTON, 70, CREAM, a)
    c.drawRRect(r, P(C(INK, a * 0.6), stroke=3))
    c.restore()

def shield(c, x, y, s, a, label="SAFE", rgb=(60, 170, 110), check=True):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, -170); p.cubicTo(70, -130, 120, -130, 150, -130); p.cubicTo(150, 20, 110, 120, 0, 180)
    p.cubicTo(-110, 120, -150, 20, -150, -130); p.cubicTo(-120, -130, -70, -130, 0, -170); p.close()
    c.drawPath(p, P(C(rgb, a))); c.drawPath(p, P(C(CREAM, a), stroke=8))
    if check:
        k = skia.Path(); k.moveTo(-60, 0); k.lineTo(-15, 50); k.lineTo(70, -50)
        pk = P(C(CREAM, a), stroke=22); pk.setStrokeCap(skia.Paint.kRound_Cap); c.drawPath(k, pk)
    if label: text(c, label, 0, 250, ANTON, 64, CREAM, a)
    c.restore()

def snowflake(c, x, y, r, a, rot=0, rgb=(170, 220, 255)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    pp = P(C(rgb, a), stroke=max(3, r * 0.09)); pp.setStrokeCap(skia.Paint.kRound_Cap)
    for k in range(6):
        ang = k * math.pi / 3; dx, dy = math.cos(ang), math.sin(ang)
        c.drawLine(0, 0, r * dx, r * dy, pp)
        for f in (0.5, 0.75):
            bx, by = r * f * dx, r * f * dy
            for sgn in (-1, 1):
                a2 = ang + sgn * 0.7
                c.drawLine(bx, by, bx + r * 0.25 * math.cos(a2), by + r * 0.25 * math.sin(a2), pp)
    c.restore()

def ice_block(c, x, y, w, h, a):
    if a <= 0: return
    r = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 22, 22)
    c.drawRRect(r, P(C((150, 200, 240), a * 0.35))); c.drawRRect(r, P(C((200, 235, 255), a * 0.9), stroke=6))
    c.drawLine(x - w * 0.35, y - h * 0.3, x - w * 0.1, y - h * 0.42, P(C((240, 250, 255), a * 0.8), stroke=8))

def box(c, x, y, w, h, a, label, rgb=(44, 50, 62), lab_rgb=CREAM, size=44):
    if a <= 0: return
    r = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 18, 18); _sh(c, r, a)
    c.drawRRect(r, P(C(rgb, a))); c.drawRRect(r, P(C(GOLD, a * 0.8), stroke=4))
    sz = size
    while text_w(label, F(BEBAS, sz)) > w - 30 and sz > 20: sz -= 2
    text(c, label, x, y + sz * 0.35, BEBAS, sz, lab_rgb, a, spacing=2)

def arrow(c, x0, y0, x1, y1, k, a, rgb=GOLD2, w=10):
    if k <= 0: return
    xe, ye = lerp(x0, x1, k), lerp(y0, y1, k)
    pp = P(C(rgb, a), stroke=w); pp.setStrokeCap(skia.Paint.kRound_Cap); c.drawLine(x0, y0, xe, ye, pp)
    ang = math.atan2(ye - y0, xe - x0)
    hd = skia.Path(); hd.moveTo(xe + 26 * math.cos(ang), ye + 26 * math.sin(ang))
    hd.lineTo(xe + 22 * math.cos(ang + 2.4), ye + 22 * math.sin(ang + 2.4)); hd.lineTo(xe + 22 * math.cos(ang - 2.4), ye + 22 * math.sin(ang - 2.4)); hd.close()
    c.drawPath(hd, P(C(rgb, a)))

def screen(c, x, y, w, h, a, label=None):
    """monitor frame, returns inner rect"""
    r = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 20, 20); _sh(c, r, a, 22)
    c.drawRRect(r, P(C((34, 36, 42), a)))
    inner = skia.Rect(x - w / 2 + 18, y - h / 2 + 18, x + w / 2 - 18, y + h / 2 - 18)
    c.drawRect(inner, P(C((14, 18, 26), a)))
    c.drawRect(skia.Rect(x - 30, y + h / 2, x + 30, y + h / 2 + 50), P(C((34, 36, 42), a)))
    c.drawRoundRect(skia.Rect(x - 120, y + h / 2 + 44, x + 120, y + h / 2 + 62), 8, 8, P(C((50, 52, 58), a)))
    if label: text(c, label, x, y - h / 2 + 52, BEBAS, 36, CREAM, a * 0.8, spacing=3)
    return inner

def tile(c, rect, a, draw_char, name, glitch=0.0, t=0, fake=False, rgb=(26, 32, 44)):
    """one video-call tile: draw_char(c, cx, feet_y, scale) inside rect; glitch 0..1 adds RGB-split + scanlines"""
    c.save(); c.clipRect(rect)
    c.drawRect(rect, P(C(rgb, a)))
    cx, cy = rect.centerX(), rect.centerY(); s = rect.height() / 300.0
    if glitch > 0:
        rng = random.Random(int(t * 12))
        for k in range(3):
            dx = rng.uniform(-14, 14) * glitch
            c.save(); c.translate(dx, 0); draw_char(c, cx, rect.bottom() + 330 * s, s, 0.35 * glitch); c.restore()
    draw_char(c, cx, rect.bottom() + 330 * s, s, 1.0)
    if glitch > 0:
        rng = random.Random(int(t * 20) + 7)
        for k in range(int(6 * glitch) + 1):
            yy = rng.uniform(rect.top(), rect.bottom()); hh = rng.uniform(4, 18)
            c.drawRect(skia.Rect(rect.left(), yy, rect.right(), yy + hh), P(C((90, 255, 160) if k % 2 else (255, 60, 80), a * 0.35 * glitch)))
    c.restore()
    c.drawRect(rect, P(C(GOLD if not fake else RED, a * 0.9), stroke=4))
    c.drawRoundRect(skia.Rect(rect.left() + 10, rect.bottom() - 46, rect.left() + 20 + text_w(name, F(BEBAS, 32)), rect.bottom() - 10), 8, 8, P(C(INK, a * 0.8)))
    text(c, name, rect.left() + 15, rect.bottom() - 18, BEBAS, 32, CREAM if not fake else RED, a, align="l")

def glove(c, x, y, s, a, t=0, rot=0):
    """white sparkly glove (generic, stylised)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-90, 200); p.lineTo(-95, 20); p.cubicTo(-150, -10, -170, -60, -140, -80); p.cubicTo(-120, -90, -95, -50, -80, -30)
    for i, (fx, fh) in enumerate([(-70, 190), (-20, 230), (30, 215), (75, 170)]):
        p.lineTo(fx, -fh + 30); p.cubicTo(fx, -fh, fx + 40, -fh, fx + 40, -fh + 30); p.lineTo(fx + 40, -40) if i < 3 else p.lineTo(fx + 38, 20)
    p.lineTo(95, 200); p.close()
    c.drawPath(p, P(C((240, 240, 246), a))); c.drawPath(p, P(C(INK, a), stroke=7))
    c.drawRect(skia.Rect(-95, 160, 95, 210), P(C((220, 220, 230), a)))
    rng = random.Random(9)
    for i in range(34):
        px, py = rng.uniform(-80, 100), rng.uniform(-180, 190)
        if not p.contains(px, py): continue
        tw = 0.5 + 0.5 * math.sin(t * 6 + i)
        c.drawCircle(px, py, 6 + 4 * tw, P(C((200, 210, 255), a * (0.5 + 0.5 * tw))))
    c.restore()

def scales(c, x, y, s, a, tilt=0.0, rgb=GOLD2):
    """scales of justice"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    pp = P(C(rgb, a), stroke=10); pp.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawLine(0, -220, 0, 160, pp); c.drawRect(skia.Rect(-90, 150, 90, 175), P(C(rgb, a)))
    c.drawCircle(0, -230, 16, P(C(rgb, a)))
    ang = math.radians(tilt * 14); dx, dy = 170 * math.cos(ang), 170 * math.sin(ang)
    c.drawLine(-dx, -200 - dy, dx, -200 + dy, pp)
    for sx, sy in ((-dx, -200 - dy), (dx, -200 + dy)):
        p2 = P(C(rgb, a), stroke=4); c.drawLine(sx, sy, sx - 60, sy + 120, p2); c.drawLine(sx, sy, sx + 60, sy + 120, p2)
        c.drawArc(skia.Rect(sx - 70, sy + 80, sx + 70, sy + 160), 0, 180, False, P(C(rgb, a)))
    c.restore()

def derrick(c, x, y, s, a, t=0, rgb=(60, 56, 50)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    pp = P(C(rgb, a), stroke=10)
    c.drawLine(-110, 0, 0, -420, pp); c.drawLine(110, 0, 0, -420, pp)
    for k in range(1, 5):
        yy = -k * 84; hw = 110 * (1 - k * 84 / 420)
        c.drawLine(-hw, yy, hw, yy, P(C(rgb, a), stroke=6))
    ph = math.sin(t * 2.4) * 12
    c.save(); c.translate(260, -170); c.rotate(ph)
    c.drawRect(skia.Rect(-170, -18, 120, 18), P(C(rgb, a))); c.drawRoundRect(skia.Rect(-210, -60, -150, 70), 20, 20, P(C(rgb, a)))
    c.restore()
    c.drawRect(skia.Rect(240, -170, 280, 0), P(C(rgb, a)))
    c.restore()
