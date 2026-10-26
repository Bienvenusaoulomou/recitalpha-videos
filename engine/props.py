"""Shared Récitalpha props: photo cards, tower, tags, documents, bills. Import AFTER setting os.environ["REC_ROOT"]."""
import os, math, random
import numpy as np, skia
from PIL import Image, ImageOps
import engine as E
from engine import (C, P, F, text, text_w, rule, stamp, coin, person, shadowed, layer_alpha, prog, eo, eio, back, lerp, clamp,
                    wt, beat, CX, W, H, ANTON, BEBAS, PLAY, POPB, GOLD, GOLD2, CREAM, RED, MUTED, INK, DARK, BG)
ROOT = os.environ["REC_ROOT"]

# ---------- photos ----------
def load_photo(name, crop=None, maxw=1300):
    im = Image.open(f"{ROOT}/img/{name}").convert("RGB")
    if crop: im = im.crop(crop)
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
    sep = ImageOps.colorize(g, black=(16, 12, 8), mid=(128, 106, 76), white=(244, 231, 200))
    a = np.array(sep)
    arr = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.kRGBA_8888_ColorType)

SAMP = skia.SamplingOptions(skia.FilterMode.kLinear)

def photo_card(c, img, cx, cy, w, h, k, a, z0=1.0, z1=1.12, focus=(0.5, 0.5), rot=0, credit=None, dim=0.0):
    if a <= 0.003: return
    c.save(); c.translate(cx, cy); c.rotate(rot)
    layer_alpha(c, a)
    sh = P(C((0, 0, 0), 0.65)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
    c.drawRect(skia.Rect(-w / 2 - 12, -h / 2, w / 2 + 12, h / 2 + 34), sh)
    c.drawRect(skia.Rect(-w / 2 - 14, -h / 2 - 14, w / 2 + 14, h / 2 + 14), P(C((236, 226, 204))))
    c.save(); c.clipRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2))
    iw, ih = img.width(), img.height()
    s = max(w / iw, h / ih) * lerp(z0, z1, eio(clamp(k)))
    dw, dh = iw * s, ih * s
    x0 = clamp(-focus[0] * dw, w / 2 - dw, -w / 2); y0 = clamp(-focus[1] * dh, h / 2 - dh, -h / 2)
    c.drawImageRect(img, skia.Rect(x0, y0, x0 + dw, y0 + dh), SAMP)
    vg = skia.Paint(); vg.setShader(skia.GradientShader.MakeRadial(skia.Point(0, 0), max(w, h) * 0.75,
                                                                      [C((0, 0, 0), 0), C((0, 0, 0), 0.45)], [0.55, 1.0]))
    c.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), vg)
    if dim > 0: c.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), P(C(BG, dim)))
    c.restore()
    if credit: text(c, credit, w / 2 + 6, h / 2 + 52, BEBAS, 30, MUTED, 0.9, align="r", spacing=2)
    c.restore(); c.restore()

# ---------- props ----------
def tower(c, x, y, s, a, rust=0.0, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    edge = P(C(GOLD, a), stroke=6); thin = P(C(GOLD, a * 0.55), stroke=2.5)
    L = skia.Path(); L.moveTo(-230, 0); L.cubicTo(-150, -120, -60, -380, -14, -700); L.lineTo(14, -700); L.cubicTo(60, -380, 150, -120, 230, 0)
    fill = skia.Path(L); fill.close(); c.drawPath(fill, P(C(INK, a * 0.9)))
    c.drawPath(L, edge)
    arch = skia.Path(); arch.moveTo(-150, 0); arch.cubicTo(-120, -110, 120, -110, 150, 0); c.drawPath(arch, edge)
    for yy, hw in ((-180, 128), (-400, 50), (-640, 18)):
        c.drawRect(skia.Rect(-hw - 22, yy - 16, hw + 22, yy), P(C(GOLD, a)))
    for i in range(14):  # lattice
        y0 = -i * 48; y1 = y0 - 48
        def half(yv):
            u = -yv / 700
            return lerp(230, 14, 1 - (1 - u) ** 2.2)
        c.drawLine(-half(y0), y0, half(y1), y1, thin); c.drawLine(half(y0), y0, -half(y1), y1, thin)
    c.drawLine(0, -700, 0, -790, P(C(GOLD, a), stroke=6))
    if rust > 0:
        for i in range(26):
            R = random.Random(i + 11); yy = -R.uniform(20, 640); u = -yy / 700
            hw = lerp(230, 14, 1 - (1 - u) ** 2.2) * R.uniform(-0.9, 0.9)
            c.drawCircle(hw, yy, R.uniform(6, 16), P(C((150, 70, 30), rust * a * 0.8)))
    c.restore()

def tag(c, x, y, label, a, rot=-6, rgb=RED):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot + 3 * math.sin(E.TOTAL))
    f = F(ANTON, 62); w = f.measureText(label) + 60
    c.drawLine(-w / 2 + 30, -40, 0, -110, P(C(CREAM, a), stroke=3)); c.drawLine(w / 2 - 30, -40, 0, -110, P(C(CREAM, a), stroke=3))
    c.drawRoundRect(skia.Rect(-w / 2, -40, w / 2, 50), 10, 10, P(C(rgb, a)))
    text(c, label, 0, 30, ANTON, 62, CREAM, a)
    c.restore()

def paper_doc(c, x, y, s, rot, a, head, sub, title, lines=8):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-300, -380, 300, 380), P(C((234, 225, 202), a)))
    text(c, head, 0, -300, PLAY, 34, INK, a)
    text(c, sub, 0, -258, BEBAS, 30, (110, 95, 70), a, spacing=4)
    rule(c, -250, 250, -232, INK, a, 3)
    text(c, title, 0, -170, ANTON, 50, INK, a)
    for ln in range(lines):
        ww = 480 if ln % 3 != 2 else 320
        c.drawRect(skia.Rect(-240, -100 + ln * 40, -240 + ww, -88 + ln * 40), P(C((160, 148, 125), a)))
    c.restore()

def bills(c, x, y, a, n=1, rot=0):
    for i in range(n):
        c.save(); c.translate(x + i * 6, y - i * 8); c.rotate(rot + i * 3)
        c.drawRoundRect(skia.Rect(-70, -34, 70, 34), 6, 6, P(C((120, 150, 100), a)))
        c.drawRoundRect(skia.Rect(-62, -26, 62, 26), 4, 4, P(C((70, 100, 60), a), stroke=3))
        c.drawCircle(0, 0, 16, P(C((70, 100, 60), a), stroke=3))
        c.restore()


def follow_pill(c, t0, t, y=1165):
    pf = prog(t, t0, 0.4)
    if pf > 0:
        s = back(pf); c.save(); c.translate(CX, y); c.scale(s, s)
        c.drawRoundRect(skia.Rect(-300, -56, 300, 56), 56, 56, P(C(GOLD2, 1)))
        text(c, "FOLLOW  @recitalpha6", 0, 17, POPB, 48, INK, 1)
        c.restore()

def pop_text(c, s_, x, y, tf, size, rgb, p, glow=0, glow_rgb=None, s0=1.6):
    if p <= 0: return
    s = lerp(s0, 1.0, eo(p))
    c.save(); c.translate(x, y); c.scale(s, s); text(c, s_, 0, 0, tf, size, rgb, clamp(p * 2), glow=glow, glow_rgb=glow_rgb); c.restore()

def pill(c, label, y, p, rgb=CREAM, size=62, w=840):
    if p <= 0: return
    c.drawRoundRect(skia.Rect(CX - w / 2, y - 62, CX + w / 2, y + 28), 45, 45, P(C(INK, 0.85 * p)))
    text(c, label, CX, y, BEBAS, size, rgb, p, spacing=2)

def seq_rows(c, t, rows, y, size=84, tf=None):
    """rows: [(label, t0, rgb)] shown one at a time at y"""
    tf = tf or ANTON
    for i, (lbl, t0, rgb) in enumerate(rows):
        p = eo(prog(t, t0 - 0.2, 0.3))
        q = 1 - eo(prog(t, rows[i + 1][1] - 0.35, 0.2)) if i + 1 < len(rows) else 1
        if p * q > 0:
            s = lerp(1.3, 1.0, p)
            c.save(); c.translate(CX, y); c.scale(s, s); text(c, lbl, 0, 0, tf, size, rgb, p * q); c.restore()

def safe(c, x, y, s, a, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-200, -220, 200, 220), 18, 18, P(C((48, 44, 38), a)))
    c.drawRoundRect(skia.Rect(-200, -220, 200, 220), 18, 18, P(C(GOLD, a), stroke=6))
    c.save(); c.translate(-170, 0); c.scale(lerp(1, 0.15, eio(open_)), 1)
    c.drawRoundRect(skia.Rect(0, -190, 340, 190), 12, 12, P(C((70, 64, 54), a)))
    c.drawRoundRect(skia.Rect(0, -190, 340, 190), 12, 12, P(C(GOLD, a), stroke=4))
    c.drawCircle(170, 0, 62, P(C(GOLD, a), stroke=8))
    for k in range(8):
        ang = k * math.pi / 4
        c.drawLine(170 + 30 * math.cos(ang), 30 * math.sin(ang), 170 + 62 * math.cos(ang), 62 * math.sin(ang), P(C(GOLD, a), stroke=5))
    c.restore()
    if open_ > 0.3:
        for i in range(6):
            bills(c, -80 + (i % 3) * 70, -90 + (i // 3) * 90, a * clamp((open_ - 0.3) * 3), 2, rot=(i - 3) * 5)
    c.restore()

def calendar(c, x, y, s, a, label, sub=""):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-150, -160, 150, 160), 16, 16, P(C((236, 226, 204), a)))
    c.drawRoundRect(skia.Rect(-150, -160, 150, -80), 16, 16, P(C(RED, a)))
    c.drawRect(skia.Rect(-150, -100, 150, -80), P(C(RED, a)))
    text(c, sub, 0, -105, BEBAS, 46, CREAM, a, spacing=4)
    text(c, label, 0, 90, ANTON, 150, INK, a)
    c.restore()

def make_rehook(scene_id, line1, line2, line3, danger=False):
    """Generic re-hook scene (put it at ~0:25-0:30). Usage: E.DRAW["rehook"] = make_rehook("rehook", "BUT THE", "CRAZIEST PART?", "PEOPLE ACTUALLY MOVED THERE.")"""
    def sc(c, t, D):
        b1 = beat(scene_id, 1) if len(E.SCN[scene_id]["sentences"]) > 1 else D * 0.5
        pop_text(c, line1, CX, 640, BEBAS, 110, CREAM, prog(t, 0.0, 0.22), s0=1.4)
        s2 = 150
        while text_w(line2, F(ANTON, s2)) > 960 and s2 > 60: s2 -= 4
        pop_text(c, line2, CX, 800, ANTON, s2, GOLD2, prog(t, 0.25, 0.25), glow=26, glow_rgb=GOLD)
        pb = prog(t, b1 - 0.1, 0.25)
        if pb > 0:
            sz = 84
            while text_w(line3, F(ANTON, sz)) > 880 and sz > 40: sz -= 2
            pop_text(c, line3, CX, 1000, ANTON, sz, RED if danger else CREAM, pb, glow=18, s0=1.15)
    return sc
