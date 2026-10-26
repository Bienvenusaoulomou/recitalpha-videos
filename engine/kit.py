"""Extra props for EP07/EP08 (buildings, ID cards, warship, prison bars, newspaper, book...)."""
import math
import skia
from props import *

STONE, STONE2 = (70, 60, 48), (98, 84, 64)
NAVY = (58, 70, 82)

def building(c, x, y, s, a, label="BANK", cols=5, rgb=STONE):
    """classical building, base center at (x, y)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-300, -340, 300, 0), P(C(rgb, a)))
    for k in range(cols):
        cx = -240 + k * (480 / (cols - 1))
        c.drawRect(skia.Rect(cx - 20, -300, cx + 20, -20), P(C(STONE2, a)))
    tri = skia.Path(); tri.moveTo(-330, -340); tri.lineTo(0, -450); tri.lineTo(330, -340); tri.close()
    c.drawPath(tri, P(C(STONE2, a))); c.drawPath(tri, P(C(GOLD, a * 0.8), stroke=4))
    c.drawRect(skia.Rect(-330, -20, 330, 0), P(C(STONE2, a)))
    if label: text(c, label, 0, -360, ANTON, 52, GOLD2, a)
    c.restore()

def mansion(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-400, -420, 400, 0), P(C(STONE, a)))
    c.drawRect(skia.Rect(-120, -560, 120, -420), P(C(STONE, a)))
    roof = skia.Path(); roof.moveTo(-430, -420); roof.lineTo(-300, -500); roof.lineTo(300, -500); roof.lineTo(430, -420); roof.close()
    c.drawPath(roof, P(C((54, 46, 38), a)))
    for r in range(3):
        for k in range(6):
            if r == 2 and k in (2, 3): continue
            wx, wy = -330 + k * 132, -380 + r * 125
            lit = 0.5 + 0.5 * math.sin(t * 2 + k + r)
            c.drawRect(skia.Rect(wx - 30, wy, wx + 30, wy + 80), P(C(GOLD2, a * (0.35 + 0.4 * lit))))
    c.drawRect(skia.Rect(-60, -130, 60, 0), P(C((40, 32, 24), a)))
    c.drawRect(skia.Rect(-60, -130, 60, 0), P(C(GOLD, a), stroke=4))
    c.restore()

def carriage(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-130, -190, 130, -40), 26, 26, P(C((44, 36, 28), a)))
    c.drawRoundRect(skia.Rect(-130, -190, 130, -40), 26, 26, P(C(GOLD, a), stroke=5))
    c.drawRect(skia.Rect(-70, -165, 10, -95), P(C(GOLD2, a * 0.5)))
    c.drawCircle(-30, -132, 20, P(C(CREAM, a)))  # lawyer waiting
    for wx in (-90, 90):
        c.drawCircle(wx, -20, 46, P(C(GOLD, a), stroke=7))
        for k in range(6):
            ang = k * math.pi / 3 + t * 0.4
            c.drawLine(wx, -20, wx + 44 * math.cos(ang), -20 + 44 * math.sin(ang), P(C(GOLD, a), stroke=3))
    c.restore()

def id_card(c, x, y, s, rot, a, name, sub, tag_=None, rgb=(236, 226, 204)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    sh = P(C((0, 0, 0), 0.6 * a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawRoundRect(skia.Rect(-370, -200, 370, 230), 26, 26, sh)
    c.drawRoundRect(skia.Rect(-380, -220, 380, 220), 26, 26, P(C(rgb, a)))
    c.drawRoundRect(skia.Rect(-380, -220, 380, -140), 26, 26, P(C(INK, a)))
    c.drawRect(skia.Rect(-380, -160, 380, -140), P(C(INK, a)))
    text(c, tag_ or "IDENTIFICATION", 0, -165, BEBAS, 48, GOLD2, a, spacing=6)
    c.drawRect(skia.Rect(-340, -110, -130, 150), P(C((180, 168, 140), a)))
    c.drawCircle(-235, -20, 52, P(C((110, 98, 78), a)))
    body = skia.Path(); body.moveTo(-320, 150); body.quadTo(-235, 30, -150, 150); body.close(); c.drawPath(body, P(C((110, 98, 78), a)))
    text(c, "?", -235, 0, ANTON, 70, CREAM, a)
    sz = 56
    while text_w(name, F(ANTON, sz)) > 460 and sz > 26: sz -= 2
    text(c, name, 110, -40, ANTON, sz, INK, a)
    text(c, sub, 110, 30, BEBAS, 40, (110, 95, 70), a, spacing=3)
    for ln in range(3):
        c.drawRect(skia.Rect(-100, 70 + ln * 30, 320 - ln * 60, 80 + ln * 30), P(C((160, 148, 125), a)))
    c.restore()

def warship(c, x, y, s, a, t=0, rgb=NAVY):
    if a <= 0: return
    c.save(); c.translate(x, y + 5 * math.sin(t * 1.6)); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-420, -40); hull.lineTo(400, -40); hull.lineTo(460, -90); hull.lineTo(330, 60); hull.lineTo(-360, 60); hull.close()
    c.drawPath(hull, P(C(rgb, a)))
    c.drawRect(skia.Rect(-160, -150, 120, -40), P(C(rgb, a)))
    c.drawRect(skia.Rect(-90, -240, 40, -150), P(C(rgb, a)))
    c.drawRect(skia.Rect(140, -110, 220, -40), P(C(rgb, a)))
    c.drawLine(180, -80, 330, -110, P(C(rgb, a), stroke=12))
    c.drawRect(skia.Rect(-300, -100, -230, -40), P(C(rgb, a)))
    c.drawLine(-25, -240, -25, -330, P(C(rgb, a), stroke=6))
    for k in range(5): c.drawCircle(-120 + k * 50, -95, 9, P(C(GOLD2, a * 0.8)))
    c.drawPath(hull, P(C(GOLD, a * 0.6), stroke=3))
    c.restore()

def sea(c, y, a, t):
    for k in range(5):
        p = skia.Path(); yy = y + k * 30
        p.moveTo(0, yy)
        for xx in range(0, W + 40, 40): p.lineTo(xx, yy + 9 * math.sin(xx / 70 + t * 2.2 + k))
        c.drawPath(p, P(C((110, 140, 160), a * (0.55 - k * 0.09)), stroke=4))

def bars(c, a, x0=60, x1=W - 60, y0=330, y1=1230, n=8):
    if a <= 0: return
    for k in range(n):
        xx = x0 + k * (x1 - x0) / (n - 1)
        c.drawRect(skia.Rect(xx - 14, y0, xx + 14, lerp(y0, y1, a)), P(C((60, 58, 56), 0.95)))
        c.drawRect(skia.Rect(xx - 14, y0, xx - 6, lerp(y0, y1, a)), P(C((120, 116, 110), 0.95)))
    c.drawRect(skia.Rect(x0 - 20, y0 + 120, x1 + 20, y0 + 150), P(C((60, 58, 56), a)))

def counter(c, v, x, y, size, rgb, a, prefix="$", suffix="", glow=0):
    s = "{}{:,.0f}{}".format(prefix, v, suffix)
    sz = size
    while text_w(s, F(ANTON, sz)) > 940 and sz > 40: sz -= 4
    text(c, s, x, y, ANTON, sz, rgb, a, glow=glow, glow_rgb=GOLD)

def news(c, x, y, s, ang, a, head="EXTRA!", title="", sub=""):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.drawRect(skia.Rect(-330, -240, 330, 240), P(C((232, 224, 204), a)))
    text(c, head, 0, -160, PLAY, 80, INK, a)
    rule(c, -300, 300, -138, INK, a, 4); rule(c, -300, 300, -128, INK, a, 1.5)
    sz = 60
    while text_w(title, F(ANTON, sz)) > 600 and sz > 30: sz -= 2
    text(c, title, 0, -62, ANTON, sz, INK, a)
    text(c, sub, 0, -14, BEBAS, 36, (90, 80, 60), a, spacing=3)
    for col in range(3):
        x0 = -300 + col * 205
        for ln in range(8):
            ww = 180 if ln % 4 != 3 else 110
            c.drawRect(skia.Rect(x0, 20 + ln * 25, x0 + ww, 30 + ln * 25), P(C((150, 140, 120), a)))
    c.restore()

def book(c, x, y, s, a, t=0, title="SURGERY"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-320, -200, 320, 210), P(C((90, 30, 26), a)))
    c.drawRect(skia.Rect(-300, -190, 0, 190), P(C((236, 226, 204), a)))
    c.drawRect(skia.Rect(0, -190, 300, 190), P(C((226, 216, 194), a)))
    text(c, title, -150, -130, ANTON, 44, INK, a)
    for ln in range(8):
        c.drawRect(skia.Rect(-270, -90 + ln * 32, -40, -82 + ln * 32), P(C((150, 140, 120), a)))
        c.drawRect(skia.Rect(30, -150 + ln * 38, 270, -142 + ln * 38), P(C((150, 140, 120), a)))
    # flipping page
    f = (t * 1.6) % 1.0
    c.save(); c.scale(math.cos(f * math.pi), 1)
    c.drawRect(skia.Rect(0, -190, 300, 190), P(C((244, 236, 216), a * 0.9)))
    c.restore()
    c.restore()

def signature(c, x, y, p, a, label="Andrew Carnegie", size=64):
    """handwritten-style signature revealed left->right by p"""
    if a <= 0 or p <= 0: return
    f = F(PLAY, size); w = text_w(label, f)
    c.save(); c.clipRect(skia.Rect(x - w / 2 - 10, y - size, x - w / 2 + (w + 20) * clamp(p), y + 30))
    c.save(); c.translate(x, y); c.skew(-0.25, 0)
    text(c, label, 0, 0, PLAY, size, (40, 50, 110), a)
    c.restore(); c.restore()
    rule(c, x - w / 2 - 20, x + w / 2 + 20, y + 18, INK, a, 2)

def chip(c, label, x, y, a, rgb=GOLD2):
    if a <= 0: return
    f = F(BEBAS, 44); w = text_w(label, f, 3) + 50
    c.drawRoundRect(skia.Rect(x - w / 2, y - 40, x + w / 2, y + 14), 26, 26, P(C(INK, 0.85 * a)))
    c.drawRoundRect(skia.Rect(x - w / 2, y - 40, x + w / 2, y + 14), 26, 26, P(C(rgb, a), stroke=3))
    text(c, label, x, y, BEBAS, 44, rgb, a, spacing=3)

def diamond(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(6 * math.sin(t))
    top = skia.Path(); top.moveTo(-120, -40); top.lineTo(-70, -100); top.lineTo(70, -100); top.lineTo(120, -40); top.close()
    bot = skia.Path(); bot.moveTo(-120, -40); bot.lineTo(120, -40); bot.lineTo(0, 120); bot.close()
    c.drawPath(top, P(C((200, 230, 245), a))); c.drawPath(bot, P(C((150, 200, 230), a)))
    for pth in (top, bot): c.drawPath(pth, P(C((255, 255, 255), a), stroke=4))
    c.drawLine(-70, -100, 0, 120, P(C((255, 255, 255), a * 0.6), stroke=2)); c.drawLine(70, -100, 0, 120, P(C((255, 255, 255), a * 0.6), stroke=2))
    c.restore()
