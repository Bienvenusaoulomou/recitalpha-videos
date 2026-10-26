import os, sys, math
os.environ.setdefault("REC_ROOT", "/home/claude/ep09")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999

PH = dict(street=load_photo("antwerp_01.jpg"), rough=load_photo("antwerp_02.jpg"))
CR_ST = "PHOTO: THORSTEN1997 · PUBLIC DOMAIN"
CR_RO = "PHOTO: USGS · PUBLIC DOMAIN"

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, b1 - 0.25, 0.25))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        safe(c, CX, 820, 1.25, 1.0, open_=eio(prog(t, 0.6, 1.6)))
        diamonds_field(c, t, 1.0 * eo(prog(t, 1.2, 0.5)), n=10, y0=600, y1=1100, s=0.22)
        text(c, "DIAMOND VAULT", CX, 440, ANTON, 130, CREAM, 1.0)
        rows = [("RADAR", W_("hook", "radar,")), ("HEAT SENSORS", W_("hook", "heat")), ("MAGNETS", W_("hook", "magnets."))]
        for i, (lb, t0) in enumerate(rows):
            chip(c, lb, CX - 300 + i * 300, 1150, eo(prog(t, t0 - 0.15, 0.2)), RED)
        c.restore(); c.restore()
    if out > 0:
        sandwich(c, CX, 790, 1.4 * lerp(1.4, 1.0, eo(out)), out, rot=-4)
        pop_text(c, "CAUGHT BY", CX, 470, ANTON, 120, CREAM, prog(t, b1 - 0.1, 0.25))
        pop_text(c, "A SANDWICH", CX, 1080, ANTON, 140, GOLD2, prog(t, W_("hook", "sandwich.") - 0.2, 0.25), glow=24, glow_rgb=GOLD)

def sc_vault(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("vault", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["street"], CX, 760, 900, 680, t / b1, a * (1 - out), 1.0, 1.15, credit=CR_ST)
        pop_text(c, "ANTWERP, 2003", CX, 360, ANTON, 104, CREAM, prog(t, 0.05, 0.25))
        pc = eo(prog(t, W_("vault", "diamond") - 0.2, 0.3))
        pill(c, "DIAMOND CAPITAL OF THE WORLD", 1200, pc * (1 - out), GOLD2, 56, 900)
    if out > 0:
        # depth gauge
        text(c, "2 FLOORS UNDERGROUND", CX, 400, ANTON, 92, CREAM, out)
        for k in range(3):
            y = 520 + k * 150
            c.drawRect(skia.Rect(140, y, 940, y + 120), P(C((60, 54, 46) if k < 2 else (30, 26, 22), out)))
            text(c, ["STREET", "-1", "-2  VAULT"][k], CX, y + 82, ANTON, 64, GOLD2 if k == 2 else MUTED, out)
        rows = [("HEAT SENSORS", W_("vault", "layer") - 0.1, CREAM), ("DOPPLER RADAR", W_("vault", "after") - 0.1, CREAM),
                ("MAGNETIC ALARM", W_("vault", "of", 1) - 0.1, CREAM), ("SEISMIC SENSOR", W_("vault", "security.") - 0.1, RED)]
        seq_rows(c, t, rows, 1130, 92)


def sc_insider(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("insider", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        building(c, CX, 1200, 0.85, a, "DIAMOND CENTER", cols=6)
        id_card(c, CX, 600, 0.95, -3, eo(prog(t, W_("insider", "Leonardo") - 0.3, 0.35)), "LEONARDO NOTARBARTOLO", "DIAMOND DEALER", tag_="OFFICE TENANT")
        pp = prog(t, W_("insider", "posing") - 0.15, 0.25)
        if pp > 0: stamp(c, CX + 220, 760, "FAKE?", RED, 90, 10, pp, sc=lerp(2, 1, eo(pp)))
        c.restore(); c.restore()
    if out > 0:
        box_grid(c, CX, 760, 7, 6, out, 0)
        k = eo(prog(t, W_("insider", "own") - 0.2, 0.4))
        x0 = CX - 3.5 * 118; y0 = 760 - 3 * 78
        rr = skia.Rect(x0 + 4 * 118 + 5, y0 + 2 * 78 + 5, x0 + 5 * 118 - 5, y0 + 3 * 78 - 5)
        g = P(C(GOLD2, 0.5 * k)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); c.drawRect(rr, g)
        c.drawRect(rr, P(C(GOLD2, k)))
        text(c, "HIS OWN BOX", CX, 400, ANTON, 120, CREAM, out)
        pop_text(c, "INSIDE THE VAULT", CX, 1150, ANTON, 100, GOLD2, prog(t, W_("insider", "inside") - 0.15, 0.25), glow=18, glow_rgb=GOLD)

def sc_tricks(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("tricks", 1)
    ps = eo(prog(t, W_("tricks", "hairspray.") - 0.6, 0.6))
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        sensor(c, CX + 180, 620, 90, a, blind=ps, t=t, label="HEAT SENSOR")
        spraycan(c, CX - 230, 980, 1.2, a, spray=ps, t=t, ang=40)
        if ps > 0.9: stamp(c, CX + 180, 620, "BLINDED", GOLD2, 80, -8, prog(t, W_("tricks", "hairspray.") + 0.05, 0.2))
        c.restore(); c.restore()
    if out > 0:
        # light sensor + tape, magnet + plate
        tp = eo(prog(t, W_("tricks", "Tape") - 0.1, 0.35))
        sensor(c, 300, 620, 70, out, blind=0, t=t, label="LIGHT")
        if tp > 0:
            c.save(); c.translate(300, 620); c.rotate(-20)
            c.drawRect(skia.Rect(-120 * tp, -36, 120 * tp, 36), P(C((210, 190, 130), out * 0.95))); c.restore()
        mp = eo(prog(t, W_("tricks", "plate") - 0.2, 0.4))
        # magnet U
        c.save(); c.translate(780, 640)
        u = skia.Path(); u.addArc(skia.Rect(-90, -40, 90, 140), 0, 180)
        c.drawPath(u, P(C(RED, out), stroke=46))
        c.drawRect(skia.Rect(-113, -60, -67, 50), P(C(RED, out))); c.drawRect(skia.Rect(67, -60, 113, 50), P(C(RED, out)))
        c.drawRect(skia.Rect(-113, -100, -67, -60), P(C(CREAM, out))); c.drawRect(skia.Rect(67, -100, 113, -60), P(C(CREAM, out)))
        c.drawRect(skia.Rect(-150, -140 - 200 * (1 - mp), 150, -110 - 200 * (1 - mp)), P(C((190, 196, 205), out * mp)))
        c.restore()
        text(c, "MAGNETIC ALARM", 780, 860, BEBAS, 44, CREAM, out, spacing=4)
        rows = [("TAPE", W_("tricks", "Tape") - 0.1, CREAM), ("A METAL PLATE", W_("tricks", "plate") - 0.2, GOLD2),
                ("ALARM FOOLED", W_("tricks", "alarm.") - 0.2, RED)]
        seq_rows(c, t, rows, 1130, 100)

def sc_boxes(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("boxes", 1)
    text(c, "VALENTINE'S WEEKEND", CX, 400, ANTON, 96, CREAM, a)
    # heart
    hp = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if hp > 0:
        c.save(); c.translate(CX, 760); s = 1 + 0.06 * math.sin(t * 7); c.scale(s, s)
        h = skia.Path(); h.moveTo(0, 160); h.cubicTo(-260, -20, -150, -220, 0, -90); h.cubicTo(150, -220, 260, -20, 0, 160)
        c.drawPath(h, P(C(RED, a * hp))); c.restore()
        text(c, "FEB 15-16, 2003", CX, 1080, BEBAS, 70, GOLD2, a * hp, spacing=6)
    if hp < 1:
        k = clamp((t - b1) / max(0.5, D - b1 - 0.4))
        box_grid(c, CX, 760, 8, 7, 1 - hp, int(k * 56 * 0.66))
        counter(c, int(k * 100), CX, 1180, 130, GOLD2, 1 - hp, prefix="", suffix="+ BOXES", glow=16)

def sc_loot(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("loot", 1)
    diamonds_field(c, t, a, n=16, s=0.28)
    k = eo(prog(t, W_("loot", "More") - 0.2, 1.4))
    c.drawRect(skia.Rect(0, 520, W, 760), P(C(BG, 0.65 * a)))
    counter(c, 100000000 * k, CX, 690, 150, GOLD2, a, suffix="+", glow=26)
    pe = eo(prog(t, W_("loot", "estimates.") - 0.3, 0.3))
    text(c, "BY SOME ESTIMATES", CX, 790, BEBAS, 60, CREAM, pe, spacing=6)
    rows = [("DIAMONDS", W_("loot", "Diamonds,") - 0.1, CREAM), ("GOLD", W_("loot", "gold") - 0.1, GOLD2), ("JEWELS", W_("loot", "jewels.") - 0.1, CREAM)]
    seq_rows(c, t, rows, 420, 100)
    pf = prog(t, b1 - 0.1, 0.3)
    if pf > 0:
        c.drawRect(skia.Rect(0, 980, W, 1250), P(C(BG, 0.75 * eo(pf))))
        for i in range(7): diamond(c, 160 + i * 125, 1200, 0.25, eo(pf), t + i)
        pop_text(c, "LEFT ON THE FLOOR", CX, 1080, ANTON, 96, CREAM, pf)

def sc_trash(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("trash", 1)
    p1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if p1 > 0:
        pop_text(c, "ONE MISTAKE", CX, 760, ANTON, 150, RED, prog(t, 0.1, 0.25) * p1, glow=24, glow_rgb=RED)
    if p1 < 1:
        q = 1 - p1
        forest(c, q, y=1220)
        road_sign(c, CX + 270, 620, 0.8, q, "E19", "ANTWERP · BRUSSELS")
        dp = eo(prog(t, W_("trash", "dumped") - 0.1, 0.7))
        trashbag(c, lerp(CX - 500, CX - 150, dp), lerp(500, 1000, dp), 0.95, q, rot=lerp(-60, 8, dp))
        pop_text(c, "A FOREST BY THE HIGHWAY", CX, 400, ANTON, 80, CREAM, prog(t, W_("trash", "forest") - 0.2, 0.25))

def sc_sandwich(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("sandwich", 1)
    out = eo(prog(t, b1 - 0.3, 0.35))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        forest(c, a, y=1220, seed=8)
        trashbag(c, CX, 950, 1.05, a, rot=6)
        person(c, CX - 300, 900, 70, CREAM, a)
        pill(c, "THE LANDOWNER FOUND IT", 420, eo(prog(t, W_("sandwich", "landowner") - 0.2, 0.3)), CREAM, 60, 860)
        pp = prog(t, W_("sandwich", "police.") - 0.2, 0.25)
        if pp > 0: stamp(c, CX + 220, 650, "POLICE", RED, 90, 8, pp, sc=lerp(2, 1, eo(pp)))
        c.restore(); c.restore()
    if out > 0:
        sandwich(c, CX, 760, 1.5 * lerp(0.6, 1.0, back(out)), out, rot=-5)
        pop_text(c, "HALF-EATEN", CX, 430, ANTON, 120, CREAM, prog(t, W_("sandwich", "half-eaten") - 0.1, 0.25))
        pop_text(c, "SALAMI SANDWICH", CX, 1100, ANTON, 110, GOLD2, prog(t, W_("sandwich", "salami") - 0.1, 0.25), glow=20, glow_rgb=GOLD)

def sc_dna(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("dna", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        dna(c, CX, 760, 620, a * (1 - out), t)
        pop_text(c, "DNA MATCH", CX, 420, ANTON, 130, GOLD2, prog(t, 0.05, 0.25) * (1 - out), glow=20, glow_rgb=GOLD)
        id_card(c, CX, 1130, 0.5, 2, eo(prog(t, W_("dna", "Notarbartolo.") - 0.3, 0.3)) * (1 - out), "NOTARBARTOLO", "IDENTIFIED", tag_="SUSPECT")
    if out > 0:
        bars(c, out, y0=330, y1=1240)
        pt = prog(t, W_("dna", "10") - 0.15, 0.25)
        if pt > 0: stamp(c, CX, 760, "10 YEARS", RED, 150, -6, pt, sc=lerp(2.2, 1, eo(pt)), sub="IN PRISON")

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("twist", 1)
    fade = 1 - eo(prog(t, b1, 1.2))
    for i in range(9):
        diamond(c, 170 + (i % 3) * 370, 560 + (i // 3) * 220, 0.4, a * max(0.12, fade), t + i)
    pop_text(c, "THE DIAMONDS?", CX, 420, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    pn = prog(t, b1 - 0.1, 0.25)
    if pn > 0:
        c.drawRect(skia.Rect(0, 1020, W, 1240), P(C(BG, 0.7 * eo(pn))))
        stamp(c, CX, 1130, "NEVER FOUND", RED, 130, -4, pn, sc=lerp(2, 1, eo(pn)))

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    # a field of planted diamonds
    c.drawRect(skia.Rect(80, 640, W - 80, 1000), P(C((86, 70, 50), a)))
    k = clamp((t - W_("cta", "field") + 0.3) / 1.2)
    for i in range(12):
        x = 140 + (i % 6) * 160; y = 720 + (i // 6) * 160
        diamond(c, x, y - 40 * eo(clamp(k * 12 - i)), 0.18, a * clamp(k * 12 - i), t + i)
    pt = prog(t, W_("cta", "bankers") - 0.2, 0.25)
    pop_text(c, "AMERICA'S RICHEST BANKERS", CX, 540, ANTON, 76, CREAM, pt)
    pp = prog(t, W_("cta", "planted") - 0.2, 0.25)
    if pp > 0: stamp(c, CX, 1110, "PLANTED BY HAND?", GOLD2, 96, -4, pp, sc=lerp(2, 1, eo(pp)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1220)

def sc_loopend(c, t, D):
    for i in range(9):
        diamond(c, 170 + (i % 3) * 370, 560 + (i // 3) * 220, 0.4, 0.25, t + i)
    pn = prog(t, 0.0, 0.22)
    stamp(c, CX, 560, "NEVER FOUND", RED, 130, -4, pn, sc=lerp(2, 1, eo(pn)))
    pa = prog(t, beat("loopend", 1) - 0.1, 0.25)
    sandwich(c, CX, 900, 0.9, eo(pa), rot=-4)
    pop_text(c, "ALL BECAUSE...", CX, 1180, ANTON, 96, GOLD2, pa, glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, vault=sc_vault, insider=sc_insider, tricks=sc_tricks, boxes=sc_boxes, loot=sc_loot,
              trash=sc_trash, sandwich=sc_sandwich, dna=sc_dna, twist=sc_twist, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"trash", "dna", "twist"}
_IMP = [("hook", "sandwich.", -0.2, 0.4), ("vault", "security.", -0.1, 0.3), ("insider", "own", -0.2, 0.3),
        ("rehook", "hairspray.", -0.1, 0.35), ("tricks", "hairspray.", 0.05, 0.3), ("tricks", "alarm.", -0.2, 0.3),
        ("loot", "More", -0.2, 0.3), ("trash", "Then", -0.05, 0.3), ("sandwich", "police.", -0.2, 0.3),
        ("sandwich", "salami", -0.1, 0.35), ("dna", "10", -0.15, 0.4), ("twist", "never", -0.1, 0.4),
        ("cta", "planted", -0.2, 0.3), ("loopend", "Most", -0.05, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("loot", "Diamonds,", 0.0), ("boxes", "broke", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
BR = "/home/claude/recitalpha-videos/archive/broll"
PDV = "ARCHIVE FOOTAGE · PUBLIC DOMAIN"
if "boxes" in SID: E.BROLL["boxes"] = E.load_broll(f"{BR}/vault_cleveland_small.mp4", start=38, dur=7, alpha=0.45, credit=PDV)
if "rehook" in SID: E.BROLL["rehook"] = E.load_broll(f"{BR}/vault_cleveland_small.mp4", start=20, dur=5, alpha=0.5, credit=PDV)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
