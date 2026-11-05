"""Récitalpha 2D character rig (skia). Flat vector, ink outline, posable limbs,
blink, lip-sync (mouth 0..1), brows, wink, walk cycle. Feet at (x, y)."""
import math, skia

INK = (24, 20, 16)
def C(rgb, a=1.0): return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a).toColor()
def P(rgb, a=1.0, stroke=0, cap=True):
    p = skia.Paint(AntiAlias=True, Color=C(rgb, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        if cap: p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p
OL = 6  # outline width

def fill_ol(c, draw, rgb, a=1.0):
    """draw(paint) twice: ink outline then fill."""
    draw(P(INK, a, stroke=OL * 2)); draw(P(rgb, a))

def limb(c, x, y, ang1, l1, ang2, l2, w, rgb, a=1.0, end=None, end_r=0, end_rgb=None):
    """angles in degrees, 0 = straight down, positive = forward (+x). Returns end point."""
    r1 = math.radians(ang1); ex, ey = x + l1 * math.sin(r1), y + l1 * math.cos(r1)
    r2 = math.radians(ang1 + ang2); hx, hy = ex + l2 * math.sin(r2), ey + l2 * math.cos(r2)
    pth = skia.Path(); pth.moveTo(x, y); pth.lineTo(ex, ey); pth.lineTo(hx, hy)
    o = P(INK, a, stroke=w + OL * 2); c.drawPath(pth, o)
    if end == "hand": c.drawCircle(hx, hy, end_r + OL, P(INK, a))
    if end == "shoe": c.drawOval(skia.Rect(hx - end_r * 0.6 - OL, hy - end_r * 0.55 - OL, hx + end_r * 1.5 + OL, hy + end_r * 0.45 + OL), P(INK, a))
    c.drawPath(pth, P(rgb, a, stroke=w))
    if end == "hand": c.drawCircle(hx, hy, end_r, P(end_rgb, a))
    if end == "shoe": c.drawOval(skia.Rect(hx - end_r * 0.6, hy - end_r * 0.55, hx + end_r * 1.5, hy + end_r * 0.45), P(end_rgb, a))
    return hx, hy

class Char:
    def __init__(self, kind, pal):
        self.kind, self.pal = kind, pal

    def draw(self, c, x, y, s=1.0, face=1, a=1.0, walk=None, mouth=0.0, blink=0.0, wink=0.0,
             brow=0.0, tilt=0.0, look=(1, 0), arm_f=(10, -20), arm_b=(-8, -15), bob=0.0, hat_lift=0.0):
        pal = self.pal; lady = self.kind == "lady"; hood = self.kind == "hood"; office = self.kind == "office"
        c.save(); c.translate(x, y); c.scale(s * face, s)
        # ground shadow
        c.drawOval(skia.Rect(-120, -14, 120, 14), P(INK, a * 0.35))
        # walk cycle
        if walk is not None:
            ph = walk * 2 * math.pi; sw = 28 * math.sin(ph); knee = max(0, 30 * math.sin(ph + 1.3))
            knee2 = max(0, 30 * math.sin(ph + math.pi + 1.3)); bob += 8 * abs(math.cos(ph))
        else: sw, knee, knee2 = 0, 0, 0
        leg_len = 125 if not lady else 120
        hip = -2 * leg_len - 10 - bob
        legc = pal["legs"]
        limb(c, 12, hip, -sw, leg_len, knee2, leg_len, 34 if not lady else 22, legc, a, "shoe", 24, pal["shoe"])
        torso_top = hip - (190 if not lady else 175)
        # back arm
        limb(c, -30, torso_top + 28, arm_b[0] - sw * 0.6, 95, arm_b[1], 90, 30, pal["sleeve"], a, "hand", 19, pal["skin"])
        limb(c, -12, hip, sw, leg_len, knee, leg_len, 34 if not lady else 22, legc, a, "shoe", 24, pal["shoe"])
        # torso
        t = skia.Path()
        if lady:
            t.moveTo(-58, torso_top + 6); t.cubicTo(-70, torso_top + 70, -62, hip - 70, -45, hip - 40)
            t.lineTo(-100, hip + 75); t.quadTo(0, hip + 95, 100, hip + 75); t.lineTo(45, hip - 40)
            t.cubicTo(62, hip - 70, 70, torso_top + 70, 58, torso_top + 6); t.quadTo(0, torso_top - 10, -58, torso_top + 6)
        else:
            t.moveTo(-72, torso_top + 10); t.cubicTo(-84, torso_top + 90, -80, hip - 30, -70, hip + 18)
            t.quadTo(0, hip + 34, 70, hip + 18); t.cubicTo(80, hip - 30, 84, torso_top + 90, 72, torso_top + 10)
            t.quadTo(0, torso_top - 12, -72, torso_top + 10)
        t.close()
        c.drawPath(t, P(INK, a, stroke=OL * 2)); c.drawPath(t, P(pal["body"], a))
        c.save(); c.clipPath(t, doAntiAlias=True)
        if lady:   # waist band + fringe lines (flapper)
            c.drawRect(skia.Rect(-80, hip - 48, 80, hip - 30), P(pal["accent"], a))
            for i in range(-90, 100, 22):
                c.drawLine(i, hip + 10, i - 4, hip + 95, P(INK, a * 0.25, stroke=3))
        elif hood:  # hoodie: pocket + drawstrings + zip
            c.drawRoundRect(skia.Rect(-50, hip - 70, 50, hip - 10), 14, 14, P(INK, a * 0.25))
            for sx in (-1, 1): c.drawLine(sx * 16, torso_top + 6, sx * 20, torso_top + 70, P((230, 230, 230), a, stroke=4))
            c.drawLine(0, torso_top + 10, 0, hip + 20, P(INK, a * 0.3, stroke=3))
        else:      # pinstripes, shirt, tie, lapels
            if not office:
                for i in range(-90, 100, 20): c.drawLine(i, torso_top - 20, i, hip + 40, P(INK, a * 0.18, stroke=2))
            sh = skia.Path(); sh.moveTo(-34, torso_top - 4); sh.lineTo(0, torso_top + 95); sh.lineTo(34, torso_top - 4); sh.close()
            c.drawPath(sh, P((236, 228, 210), a))
            tie = skia.Path(); tie.moveTo(-9, torso_top + 6); tie.lineTo(9, torso_top + 6); tie.lineTo(14, torso_top + 80)
            tie.lineTo(0, torso_top + 96); tie.lineTo(-14, torso_top + 80); tie.close(); c.drawPath(tie, P(pal["accent"], a))
            for sx in (-1, 1):
                lp = skia.Path(); lp.moveTo(sx * 36, torso_top - 4); lp.lineTo(sx * 4, torso_top + 104); lp.lineTo(sx * 50, torso_top + 40); lp.close()
                c.drawPath(lp, P(INK, a * 0.25))
            c.drawCircle(40, torso_top + 52, 5, P((236, 228, 210), a))  # pocket square
        c.restore()
        # head
        hx, hy = 6, torso_top - 78
        c.save(); c.translate(hx, hy + 70); c.rotate(tilt); c.translate(0, -70)
        neck = skia.Rect(-17, 30, 17, 82); c.drawRect(neck, P(INK, a)); c.drawRect(skia.Rect(-12, 30, 12, 82), P(pal["skin"], a))
        if hood:
            hd_ = skia.Rect(-92, -104, 96, 84)
            c.drawOval(skia.Rect(hd_.left() - OL, hd_.top() - OL, hd_.right() + OL, hd_.bottom() + OL), P(INK, a)); c.drawOval(hd_, P(pal["body"], a))
            c.drawOval(skia.Rect(-56, -62, 74, 60), P((14, 14, 18), a))
            for ex in (6, 46):
                g = P(pal["accent"], a * 0.8); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)); c.drawCircle(ex + 4 * look[0], -6, 10, g)
                c.drawCircle(ex + 4 * look[0], -6 - 9 * blink * 0, 6 * (1 - blink) + 1, P(pal["accent"], a))
        else:
            if lady:   # bob hair back
                c.drawOval(skia.Rect(-82 - OL, -70 - OL, 78 + OL, 62 + OL), P(INK, a)); c.drawOval(skia.Rect(-82, -70, 78, 62), P(pal["hair"], a))
            c.drawCircle(-52, 8, 16 + OL, P(INK, a)); c.drawCircle(-52, 8, 16, P(pal["skin"], a))  # ear
            hd = skia.Rect(-66, -72, 70, 66)
            c.drawOval(skia.Rect(hd.left() - OL, hd.top() - OL, hd.right() + OL, hd.bottom() + OL), P(INK, a)); c.drawOval(hd, P(pal["skin"], a))
            c.drawCircle(42, 22, 13, P((230, 120, 100), a * 0.35))  # cheek
            # eyes (3/4 view: shifted forward)
            lx, ly = look
            for ex, sz, w_ in ((14, 1.0, wink), (50, 0.85, 0)):
                cl = max(blink, w_)
                hgt = 19 * sz * (1 - cl)
                if hgt > 2.5:
                    c.drawOval(skia.Rect(ex - 12 * sz, -8 - hgt, ex + 12 * sz, -8 + hgt), P((250, 247, 240), a))
                    c.drawOval(skia.Rect(ex - 12 * sz, -8 - hgt, ex + 12 * sz, -8 + hgt), P(INK, a, stroke=3.5))
                    c.save(); c.clipRect(skia.Rect(ex - 12 * sz, -8 - hgt, ex + 12 * sz, -8 + hgt))
                    c.drawCircle(ex + 4 * lx, -8 + 4 * ly, 8 * sz, P(INK, a)); c.drawCircle(ex + 4 * lx + 2.5, -11 + 4 * ly, 2.6, P((255, 255, 255), a))
                    c.restore()
                else:
                    arc = skia.Path(); arc.moveTo(ex - 12 * sz, -6); arc.quadTo(ex, 2 if w_ > 0.5 else -2, ex + 12 * sz, -6)
                    c.drawPath(arc, P(INK, a, stroke=4.5))
                by = -36 - brow * 12 + (3 if (w_ > 0.5 and ex == 14) else 0)
                c.drawLine(ex - 13 * sz, by + 2 - brow * 3, ex + 12 * sz, by - 2 + (-2 if lady else 2), P(pal["hair"] if not lady else INK, a, stroke=6 if not lady else 4))
            # nose
            nz = skia.Path(); nz.moveTo(62, -6); nz.quadTo(80, 14, 60, 20); c.drawPath(nz, P(INK, a, stroke=4))
            # mouth
            mo = max(0.0, min(1.0, mouth)); mx, my = 38, 40
            if mo > 0.08:
                mr = skia.Rect(mx - 15 - 3 * mo, my - 4, mx + 15 + 3 * mo, my - 2 + 26 * mo)
                c.drawOval(mr, P((70, 22, 22), a)); c.save(); c.clipRect(skia.Rect(mr.left(), my + 8 * mo, mr.right(), mr.bottom()))
                c.drawOval(skia.Rect(mx - 9, my + 6 * mo, mx + 9, my + 24 * mo), P((210, 90, 90), a)); c.restore()
                c.drawOval(mr, P(INK, a, stroke=3.5))
            else:
                sm = skia.Path(); sm.moveTo(mx - 16, my - 2); sm.quadTo(mx, my + 10, mx + 18, my - 6); c.drawPath(sm, P(INK, a, stroke=4.5))
            if lady:   # lips tint + cloche hat
                c.drawCircle(mx, my + 1, 3, P(pal["accent"], a * 0.0))
                cl = skia.Path(); cl.moveTo(-90, -14); cl.cubicTo(-92, -100, 90, -112, 86, -20); cl.quadTo(40, -42, -10, -40); cl.quadTo(-60, -40, -90, -14); cl.close()
                c.drawPath(cl, P(INK, a, stroke=OL * 2)); c.drawPath(cl, P(pal["hat"], a))
                c.drawPath(cl, P(INK, a * 0.0))
                c.save(); c.clipPath(cl, doAntiAlias=True); c.drawRect(skia.Rect(-100, -54, 100, -38), P(pal["accent"], a)); c.restore()
                c.drawCircle(-46, -50, 12, P(INK, a)); c.drawCircle(-46, -50, 8, P(pal["accent2"], a))
            elif office:  # short hair + glasses
                hr = skia.Path(); hr.moveTo(-66, -20); hr.cubicTo(-70, -90, 60, -100, 70, -30); hr.cubicTo(30, -60, -20, -56, -66, -20); hr.close()
                c.drawPath(hr, P(pal["hair"], a)); c.drawPath(hr, P(INK, a, stroke=3))
                for ex in (14, 50): c.drawCircle(ex, -8, 21, P(INK, a, stroke=4))
                c.drawLine(35, -8, 29, -8, P(INK, a, stroke=4))
            else:      # mustache + fedora
                ms = skia.Path(); ms.moveTo(mx - 24, my - 10); ms.quadTo(mx, my - 22, mx + 26, my - 12); ms.quadTo(mx + 10, my - 4, mx, my - 10); ms.quadTo(mx - 10, my - 4, mx - 24, my - 10); ms.close()
                c.drawPath(ms, P(pal["hair"], a)); c.drawPath(ms, P(INK, a, stroke=2.5))
                c.save(); c.translate(0, -hat_lift); c.rotate(-hat_lift * 0.15)
                br = skia.Rect(-100, -66, 112, -40)
                crown = skia.Path(); crown.moveTo(-66, -54); crown.cubicTo(-70, -120, -30, -136, 6, -122); crown.cubicTo(40, -136, 76, -122, 72, -54); crown.close()
                for shp in ("crown", "brim"):
                    if shp == "crown": c.drawPath(crown, P(INK, a, stroke=OL * 2)); c.drawPath(crown, P(pal["hat"], a))
                    else: c.drawOval(skia.Rect(br.left() - OL, br.top() - OL, br.right() + OL, br.bottom() + OL), P(INK, a)); c.drawOval(br, P(pal["hat"], a))
                c.save(); c.clipPath(crown, doAntiAlias=True); c.drawRect(skia.Rect(-80, -76, 80, -56), P(pal["accent2"], a)); c.restore()
                dent = skia.Path(); dent.moveTo(-20, -126); dent.quadTo(6, -110, 30, -126); c.drawPath(dent, P(INK, a * 0.6, stroke=4))
                c.restore()
        c.restore()
        # front arm (returns hand pos in local coords)
        hand = limb(c, 34, torso_top + 30, arm_f[0] + sw * 0.6, 95, arm_f[1], 90, 30, pal["sleeve"], a, "hand", 20, pal["skin"])
        c.restore()
        return hand, (hx, hy)

CONMAN = Char("man", dict(skin=(232, 186, 150), body=(58, 66, 84), sleeve=(52, 60, 78), legs=(46, 52, 68), shoe=(70, 44, 30),
                          hat=(92, 76, 58), hair=(54, 38, 28), accent=(196, 54, 44), accent2=(30, 26, 22)))
LADY = Char("lady", dict(skin=(244, 206, 176), body=(40, 120, 118), sleeve=(244, 206, 176), legs=(236, 196, 166), shoe=(150, 40, 50),
                         hat=(40, 96, 94), hair=(40, 28, 22), accent=(214, 168, 75), accent2=(196, 54, 44)))


HACKER = Char("hood", dict(skin=(200, 170, 140), body=(34, 38, 46), sleeve=(30, 34, 42), legs=(26, 28, 34), shoe=(20, 20, 22),
                           hat=(0, 0, 0), hair=(20, 20, 20), accent=(90, 255, 160), accent2=(0, 0, 0)))
RECRUITER = Char("office", dict(skin=(214, 172, 136), body=(70, 74, 82), sleeve=(66, 70, 78), legs=(50, 54, 62), shoe=(30, 24, 20),
                                hat=(0, 0, 0), hair=(40, 30, 24), accent=(40, 90, 160), accent2=(0, 0, 0)))
EMPLOYEE = Char("office", dict(skin=(236, 196, 160), body=(150, 160, 176), sleeve=(150, 160, 176), legs=(60, 66, 80), shoe=(40, 30, 24),
                               hat=(0, 0, 0), hair=(150, 100, 50), accent=(196, 54, 44), accent2=(0, 0, 0)))
