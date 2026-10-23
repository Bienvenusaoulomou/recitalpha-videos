import os, sys, math, random
os.environ["REC_ROOT"] = "/home/claude/ep02"
sys.path.insert(0, "/home/claude/ep02")
import numpy as np, skia
from PIL import Image, ImageOps
import engine as E
from engine import (C, P, F, text, text_w, rule, stamp, coin, person, shadowed, layer_alpha, prog, eo, eio, back, lerp, clamp,
                    wt, beat, CX, W, H, ANTON, BEBAS, PLAY, POPB, GOLD, GOLD2, CREAM, RED, MUTED, INK, DARK, BG)

ROOT = "/home/claude/ep02"

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

PH = dict(
    fbi=load_photo("lustig_fbi_1931.jpg", crop=(0, 0, 460, 300)),
    eiffel=load_photo("eiffel_1925.jpg"),
    hotel=load_photo("hotel_crillon.jpg"),
    clip=load_photo("lustig_1935.jpg"),
    bill=load_photo("fake_10_dollar.jpg"),
    alca=load_photo("alcatraz_1930s.jpg"),
    cert=load_photo("death_certificate.png", crop=(0, 700, 1000, 1000)),
)
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

# ---------- scenes ----------
def sc_hook(c, t, D):
    a = eo(prog(t, 0.0, 0.5))
    text(c, "PARIS · 1925", CX, 430, BEBAS, 96, GOLD, a, spacing=6)
    tower(c, CX, 1110, lerp(0.78, 0.84, eio(prog(t, 0, D))), a)
    ts = wt("hook", "sold") - 0.05
    tag(c, CX + 150, 860, "FOR SALE", eo(prog(t, 0.4, 0.4)) * (1 - prog(t, ts, 0.15)), rot=-6)
    ps = prog(t, ts, 0.2)
    if ps > 0: stamp(c, CX, 820, "SOLD", RED, 150, -12, ps, sc=lerp(2.2, 1.0, eo(ps)))
    pa = eo(prog(t, wt("hook", "ashamed") - 0.1, 0.35))
    if pa > 0:
        c.drawRoundRect(skia.Rect(90, 1120, 990, 1210), 45, 45, P(C(INK, 0.85 * pa)))
        text(c, "THE BUYER NEVER CALLED THE POLICE", CX, 1185, BEBAS, 62, CREAM, pa, spacing=2)

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.5))
    photo_card(c, PH["fbi"], CX, 640, 860, 561, t / D, a, 1.0, 1.10, focus=(0.35, 0.4), rot=-1.5,
               credit="PHOTO: U.S. BUREAU OF INVESTIGATION, 1931")
    pn = eo(prog(t, 0.4, 0.6))
    text(c, "VICTOR LUSTIG", CX, 1035, PLAY, 100, CREAM, pn, spacing=lerp(24, 4, pn))
    chips = [("PERFECT SUITS", wt("who", "suits,"), GOLD2), ("SEVERAL LANGUAGES", wt("who", "languages,"), GOLD2), ("DOZENS OF ARRESTS", wt("who", "arrests."), RED)]
    for i, (lbl, t0, rgb) in enumerate(chips):
        p = eo(prog(t, t0 - 0.35, 0.25))
        q = 1 - eo(prog(t, chips[i + 1][1] - 0.4, 0.2)) if i + 1 < len(chips) else 1
        if p * q > 0: text(c, lbl, CX, 1135 + (1 - p) * 30, BEBAS, 76, rgb, p * q, spacing=5)

def sc_paper(c, t, D):
    a = eo(prog(t, 0, 0.5))
    tr = wt("paper", "repairs") - 0.6
    idea = eo(prog(t, beat("paper", 1) - 0.15, 0.35))
    photo_card(c, PH["eiffel"], CX - 90, 720, 520, 750, t / D, a, 1.05, 1.2, focus=(0.5, 0.6), rot=-3,
               credit="EIFFEL TOWER, 1925 · PUBLIC DOMAIN", dim=0.5 * idea)
    pp = eo(prog(t, tr, 0.5))
    if pp > 0:
        shadowed(c, lambda: paper_doc(c, lerp(1200, 690, pp), 860, 0.62, 7, 1.0,
                                      "LE QUOTIDIEN", "PARIS · 1925", "TOO COSTLY TO REPAIR?", 6))
    if idea > 0:
        c.drawRect(skia.Rect(0, 300, W, 1230), P(C(BG, 0.6 * idea)))
        text(c, "LUSTIG HAD", CX, 690, BEBAS, 96, CREAM, idea, spacing=8)
        text(c, "AN IDEA.", CX, 870, ANTON, 200, GOLD2, idea, glow=28, glow_rgb=GOLD)

def sc_fake(c, t, D):
    a = eo(prog(t, 0, 0.4))
    c.save(); c.translate(CX, 740); c.rotate(-2)
    c.drawRect(skia.Rect(-300, -400, 300, 400), P(C((234, 225, 202), a)))
    text(c, "RÉPUBLIQUE FRANÇAISE", 0, -320, BEBAS, 40, (110, 95, 70), a, spacing=6)
    text(c, "MINISTÈRE DES POSTES", 0, -262, PLAY, 44, INK, a)
    text(c, "ET TÉLÉGRAPHES", 0, -214, PLAY, 44, INK, a)
    rule(c, -250, 250, -186, INK, a, 3)
    for ln in range(9):
        ww = 480 if ln % 3 != 2 else 300
        c.drawRect(skia.Rect(-240, -140 + ln * 38, -240 + ww * eo(prog(t, 0.2 + ln * 0.06, 0.3)), -128 + ln * 38), P(C((160, 148, 125), a)))
    sg = eo(prog(t, wt("fake", "papers,") - 0.2, 0.8))
    if sg > 0:
        sp = skia.Path(); n = int(40 * sg)
        for i in range(n + 1):
            u = i / 40; xx = -200 + u * 300; yy = 300 + 22 * math.sin(u * 19) * (1 - u * 0.5) - 30 * u
            (sp.moveTo if i == 0 else sp.lineTo)(xx, yy)
        c.drawPath(sp, P(C((30, 40, 90), a), stroke=4))
    ps = prog(t, wt("fake", "papers,") + 0.4, 0.2)
    if ps > 0:
        c.save(); c.translate(170, 270); c.scale(lerp(1.8, 1, eo(ps)), lerp(1.8, 1, eo(ps)))
        c.drawCircle(0, 0, 70, P(C(RED, 0.85 * ps), stroke=7)); c.drawCircle(0, 0, 54, P(C(RED, 0.6 * ps), stroke=3))
        text(c, "RF", 0, 18, PLAY, 50, RED, 0.85 * ps)
        c.restore()
    c.restore()
    pf = prog(t, wt("fake", "posed") - 0.1, 0.22)
    if pf > 0: stamp(c, CX, 760, "FAKE", RED, 170, -18, pf, sc=lerp(2.0, 1.0, eo(pf)))
    pl = eo(prog(t, wt("fake", "official") - 0.1, 0.35))
    if pl > 0:
        c.drawRoundRect(skia.Rect(120, 1110, 960, 1200), 45, 45, P(C(INK, 0.85 * pl)))
        text(c, "\"TOP GOVERNMENT OFFICIAL\"", CX, 1175, BEBAS, 64, GOLD2, pl, spacing=2)

def sc_meeting(c, t, D):
    a = eo(prog(t, 0, 0.5))
    ts = wt("meeting", "Top") - 0.1
    sec = prog(t, ts, 0.22)
    photo_card(c, PH["hotel"], CX, 620, 880, 600, t / D, a, 1.0, 1.15, focus=(0.5, 0.45), rot=1.2,
               credit="HÔTEL DE CRILLON, PARIS · LIBRARY OF CONGRESS", dim=0.55 * clamp(sec * 2))
    t6 = wt("meeting", "six") - 0.1
    for i in range(6):
        p = eo(prog(t, t6 + i * 0.09, 0.3))
        person(c, 240 + i * 120, 1060 - (1 - p) * 30, 34, CREAM, p)
    text(c, "6 SCRAP METAL DEALERS", CX, 1175, BEBAS, 70, GOLD2, eo(prog(t, t6 + 0.5, 0.3)), spacing=3)
    if sec > 0:
        stamp(c, CX, 600, "TOP SECRET", RED, 120, -8, sec, sc=lerp(2.2, 1.0, eo(sec)))
    psc = eo(prog(t, wt("meeting", "scrap.", 1) - 0.3, 0.3))
    if psc > 0:
        text(c, "THE TOWER... FOR SCRAP", CX, 800, ANTON, 84, GOLD2, psc, glow=16, glow_rgb=GOLD)

def sc_victim(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pick = eo(prog(t, wt("victim", "Poisson,") - 0.3, 0.4))
    for i in range(6):
        x = 190 + i * 140
        chosen = i == 2
        rgb = GOLD2 if (chosen and pick > 0.5) else CREAM
        al = a * (1 - 0.7 * pick) if not chosen else a
        sc = 1 + 0.35 * pick if chosen else 1
        c.save(); c.translate(x, 720); c.scale(sc, sc); person(c, 0, 0, 44, rgb, al); c.restore()
    pn = eo(prog(t, wt("victim", "André") - 0.2, 0.4))
    text(c, "ANDRÉ POISSON", CX, 900, PLAY, 86, CREAM, pn, spacing=lerp(20, 4, pn))
    text(c, "SCRAP DEALER", CX, 965, BEBAS, 52, MUTED, pn, spacing=6)
    tp = wt("victim", "paid") - 0.1
    if t > tp:
        tt = t - tp
        for i in range(10):
            R = random.Random(i + 70); ph = clamp((tt - i * 0.12) / 0.9)
            if 0 < ph < 1:
                x = lerp(470, 980, eio(ph)); y = 760 - 180 * math.sin(math.pi * ph) + R.uniform(-30, 30)
                bills(c, x, y, math.sin(math.pi * ph), 1, rot=R.uniform(-30, 30))
        text(c, "LUSTIG", 905, 560, BEBAS, 56, GOLD, eo(prog(t, tp, 0.3)), spacing=4)
    pb = eo(prog(t, wt("victim", "bribe") - 0.1, 0.3))
    if pb > 0:
        s = lerp(1.6, 1.0, pb)
        c.save(); c.translate(CX, 1150); c.scale(s, s); text(c, "+ A BRIBE", 0, 0, ANTON, 120, RED, pb); c.restore()

def sc_escape(c, t, D):
    a = eo(prog(t, 0, 0.4))
    tn = wt("escape", "Nothing.") - 0.2
    m = 1 - eo(prog(t, tn, 0.35))
    ax, ay, bx, by, kx, ky = 260, 900, 820, 760, 540, 520
    if m > 0:
        c.drawCircle(ax, ay, 18, P(C(GOLD2, a * m))); text(c, "PARIS", ax, ay + 80, BEBAS, 70, CREAM, a * m, spacing=4)
        pr = eio(prog(t, 0.4, 2.0)); n = 36
        for i in range(int(n * pr)):
            u = i / n
            x = (1 - u) ** 2 * ax + 2 * (1 - u) * u * kx + u * u * bx; y = (1 - u) ** 2 * ay + 2 * (1 - u) * u * ky + u * u * by
            c.drawCircle(x, y, 5, P(C(GOLD, 0.85 * m)))
        u = pr; x = (1 - u) ** 2 * ax + 2 * (1 - u) * u * kx + u * u * bx; y = (1 - u) ** 2 * ay + 2 * (1 - u) * u * ky + u * u * by
        bills(c, x, y - 30, m * a, 3, rot=-8)
        pb = eo(prog(t, 2.2, 0.3))
        c.drawCircle(bx, by, 18 * pb, P(C(RED, m))); text(c, "AUSTRIA", bx, by + 80, BEBAS, 70, CREAM, pb * m, spacing=4)
        pw = eo(prog(t, wt("escape", "watched") - 0.2, 0.4))
        text(c, "THEN HE WAITED...", CX, 1150, BEBAS, 76, MUTED, pw * m, spacing=6)
    pn = eo(prog(t, tn, 0.35))
    if pn > 0:
        for i in range(3):
            c.save(); c.translate(CX + (i - 1) * 60, 700 + i * 20); c.rotate((i - 1) * 8)
            c.drawRect(skia.Rect(-220, -150, 220, 150), P(C((228, 219, 196), pn)))
            for ln in range(6): c.drawRect(skia.Rect(-190, -110 + ln * 40, 190 - (ln % 2) * 90, -98 + ln * 40), P(C((165, 152, 128), pn)))
            c.restore()
        text(c, "NOTHING.", CX, 1050, ANTON, 190, CREAM, pn, glow=18)
        text(c, "NOT A WORD IN THE PAPERS", CX, 1150, BEBAS, 62, MUTED, eo(prog(t, wt("escape", "word.") - 0.3, 0.3)), spacing=3)

def sc_again(c, t, D):
    a = eo(prog(t, 0, 0.4))
    tp = wt("again", "police.") - 0.3
    out = eo(prog(t, tp, 0.4))
    if out < 1:
        tower(c, CX, 1110, 0.8, a * (1 - out))
        tag(c, CX + 140, 870, "FOR SALE · AGAIN", eo(prog(t, wt("again", "again.") - 0.3, 0.3)) * (1 - out), rot=-5)
        text(c, "BACK IN PARIS", CX, 430, BEBAS, 90, GOLD, a * (1 - out), spacing=6)
    if out > 0:
        pulse = 0.5 + 0.5 * math.sin(t * 14)
        c.drawCircle(CX, 560, 90, P(C(RED, out * (0.35 + 0.5 * pulse))))
        c.drawRoundRect(skia.Rect(CX - 60, 520, CX + 60, 600), 20, 20, P(C(RED, out)))
        text(c, "POLICE!", CX, 790, ANTON, 170, RED, out, glow=24)
        ps = eo(prog(t, wt("again", "America.") - 0.6, 0.4))
        if ps > 0:
            E.waves(c, t, 1030, ps)
            E.ship(c, lerp(200, 760, eio(prog(t, wt("again", "America.") - 0.6, 2.0))), 985, t, ps)
            text(c, "OFF TO AMERICA", CX, 1200, BEBAS, 76, GOLD2, ps, spacing=6)

def sc_capone(c, t, D):
    a = eo(prog(t, 0, 0.5))
    if t > wt("capone", "rewarded"):
        tt = t - wt("capone", "rewarded")
        for i in range(16):
            R = random.Random(i + 900)
            x = CX + R.uniform(-380, 380); y = 330 + ((tt * R.uniform(250, 500) + R.uniform(0, 300)) % 560)
            bills(c, x, y, clamp(tt * 2) * 0.8, 1, rot=R.uniform(-40, 40) + tt * 60)

    E.man(c, CX, 690, a, 0.72)
    text(c, "AL CAPONE", CX, 960, ANTON, 120, GOLD2, eo(prog(t, wt("capone", "Capone.") - 0.3, 0.4)), glow=18, glow_rgb=GOLD)
    rows = [("BORROWED $50,000", wt("capone", "borrowed"), CREAM),
            ("RETURNED EVERY CENT", wt("capone", "returned"), CREAM),
            ("+ A REWARD FROM CAPONE", wt("capone", "rewarded"), GOLD2)]
    for i, (lbl, t0, rgb) in enumerate(rows):
        p = eo(prog(t, t0 - 0.2, 0.3))
        q = 1 - eo(prog(t, rows[i + 1][1] - 0.35, 0.2)) if i + 1 < len(rows) else 1
        if p * q > 0:
            s = lerp(1.3, 1.0, p)
            c.save(); c.translate(CX, 1110); c.scale(s, s); text(c, lbl, 0, 0, ANTON, 84, rgb, p * q); c.restore()
def sc_fall(c, t, D):
    b1 = beat("fall", 1)
    out = eo(prog(t, b1 - 0.3, 0.4))
    a = eo(prog(t, 0, 0.5)) * (1 - out)
    photo_card(c, PH["clip"], CX, 640, 600, 612, t / D, a, 1.0, 1.12, focus=(0.5, 0.35), rot=-2,
               credit="EVENING PUBLIC LEDGER, 1935")
    pb = eo(prog(t, wt("fall", "fake") - 0.25, 0.4)) * (1 - out)
    if pb > 0:
        photo_card(c, PH["bill"], lerp(1300, CX + 40, pb), 1010, 560, 250, 0.5, pb, 1.0, 1.0, rot=6,
                   credit="ONE OF LUSTIG'S FAKE $10 BILLS")
        text(c, "~$50,000 IN FAKE BILLS", CX, 1205, ANTON, 72, GOLD2, eo(prog(t, wt("fall", "locker.") - 0.4, 0.3)) * (1 - out))
    if out > 0:
        # jail wall & bedsheet rope
        c.drawRect(skia.Rect(300, 330, 780, 1060), P(C((40, 36, 30), out)))
        for r in range(12):
            for k in range(4):
                bx = 300 + k * 120 + (60 if r % 2 else 0); by = 330 + r * 61
                c.drawRect(skia.Rect(bx, by, bx + 118, by + 59), P(C((60, 54, 44), out * 0.8), stroke=2))
        c.drawRect(skia.Rect(470, 380, 610, 520), P(C(INK, out)))
        for k in range(4): c.drawLine(490 + k * 35, 380, 490 + k * 35, 520, P(C(MUTED, out), stroke=5))
        rp = eio(prog(t, wt("fall", "escaped") - 0.1, 1.2)); yb = lerp(520, 1050, rp)
        path = skia.Path(); path.moveTo(540, 520)
        for i in range(1, 30):
            yy = lerp(520, yb, i / 29); path.lineTo(540 + 8 * math.sin(i * 0.9 + t * 3), yy)
        c.drawPath(path, P(C(CREAM, out), stroke=9))
        for i in range(1, 6):
            yy = lerp(520, yb, i / 6); c.drawCircle(540 + 8 * math.sin(i * 4.5 + t * 3), yy, 13, P(C(CREAM, out)))
        person(c, 560, lerp(560, 1000, eio(prog(t, wt("fall", "escaped") + 0.4, 1.6))), 26, GOLD2, out)
        text(c, "ESCAPED WITH BEDSHEETS", CX, 1150, BEBAS, 76, CREAM, out * eo(prog(t, wt("fall", "bedsheets,") - 0.4, 0.3)), spacing=4)
        pc = prog(t, wt("fall", "caught") - 0.1, 0.22)
        if pc > 0:
            c.drawRect(skia.Rect(0, 300, W, 1230), P(C(BG, 0.5 * pc)))
            stamp(c, CX, 760, "CAUGHT", RED, 150, -9, pc, sc=lerp(2.2, 1.0, eo(pc)), sub="PITTSBURGH · 1935")

def sc_ending(c, t, D):
    b1 = beat("ending", 1)
    out = eo(prog(t, b1 - 0.3, 0.4))
    a = eo(prog(t, 0, 0.5)) * (1 - out)
    photo_card(c, PH["alca"], CX, 620, 900, 533, t / D, a, 1.0, 1.15, focus=(0.42, 0.45), rot=-1,
               credit="ALCATRAZ, 1930s · U.S. NAVY")
    text(c, "20 YEARS · ALCATRAZ", CX, 1030, ANTON, 96, CREAM, a * eo(prog(t, wt("ending", "20") - 0.2, 0.3)))
    text(c, "DIED IN FEDERAL CUSTODY · 1947", CX, 1120, BEBAS, 62, MUTED, a * eo(prog(t, wt("ending", "1947.") - 0.4, 0.3)), spacing=3)
    if out > 0:
        k = prog(t, b1, D - b1)
        cw, ch = 960, 288
        photo_card(c, PH["cert"], CX, 640, cw, ch, 0, out, 1.0, 1.0, credit="LUSTIG'S DEATH CERTIFICATE, 1947")
        ph = eo(prog(t, wt("ending", "Apprentice") - 0.2, 0.4))
        if ph > 0:
            s = cw / 1000
            x0, x1, y0, y1 = -cw / 2 + 120 * s, -cw / 2 + 880 * s, -ch / 2 + 100 * s, -ch / 2 + 185 * s
            c.save(); c.translate(CX, 640)
            c.drawRoundRect(skia.Rect(x0, y0, x0 + (x1 - x0) * ph, y1), 8, 8, P(C(GOLD2, 1.0), stroke=6))
            c.restore()
        p1 = eo(prog(t, wt("ending", "Apprentice") - 0.1, 0.35))
        text(c, "APPRENTICE SALESMAN", CX, 960, ANTON, 92, CREAM, p1)
        p2 = prog(t, wt("ending", "counterfeiter.") - 0.1, 0.25)
        if p2 > 0:
            s = lerp(1.6, 1.0, eo(p2))
            c.save(); c.translate(CX, 1090); c.scale(s, s); text(c, "& COUNTERFEITER", 0, 0, ANTON, 104, RED, p2, glow=18); c.restore()

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "NEXT EPISODE", CX, 450, BEBAS, 70, MUTED, a, spacing=10)
    E.man(c, CX, 690, a * 0.9, 0.55)
    text(c, "THE MOST FEARED GANGSTER IN AMERICA", CX, 900, BEBAS, 58, CREAM, eo(prog(t, wt("cta", "feared") - 0.2, 0.3)), spacing=2)
    pj = prog(t, wt("cta", "jailed") - 0.1, 0.25)
    if pj > 0:
        s = lerp(1.7, 1.0, eo(pj))
        c.save(); c.translate(CX, 1040); c.scale(s, s)
        text(c, "JAILED FOR TAXES?", 0, 0, ANTON, 128, GOLD2, clamp(pj * 2), glow=26, glow_rgb=GOLD)
        c.restore()
    pf = prog(t, wt("cta", "Follow") - 0.1, 0.4)
    if pf > 0:
        s = back(pf); c.save(); c.translate(CX, 1165); c.scale(s, s)
        c.drawRoundRect(skia.Rect(-300, -56, 300, 56), 56, 56, P(C(GOLD2, 1)))
        text(c, "FOLLOW  @recitalpha6", 0, 17, POPB, 48, INK, 1)
        c.restore()

E.DRAW = dict(hook=sc_hook, who=sc_who, paper=sc_paper, fake=sc_fake, meeting=sc_meeting, victim=sc_victim, escape=sc_escape,
              again=sc_again, capone=sc_capone, fall=sc_fall, ending=sc_ending, cta=sc_cta)
E.RED_SCENES = {"again", "fall"}

IMPACTS = [("hook", "sold", -0.05, 0.35), ("fake", "posed", -0.1, 0.3), ("meeting", "Top", -0.1, 0.3), ("victim", "bribe", -0.1, 0.25),
           ("escape", "Nothing.", -0.2, 0.25), ("again", "police.", -0.3, 0.3), ("fall", "caught", -0.1, 0.4),
           ("ending", "counterfeiter.", -0.1, 0.35), ("cta", "jailed", -0.1, 0.3)]
CLINKS = [("capone", "rewarded", 0.0)]

if __name__ == "__main__":
    E.main()
