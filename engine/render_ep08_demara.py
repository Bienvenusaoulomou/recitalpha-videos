import os, sys, math
os.environ.setdefault("REC_ROOT", "/home/claude/ep08")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999

def ident(c, n, a):
    """identity counter chip, top of the scene"""
    chip(c, "FAKE IDENTITY #%d" % n, CX, 1225, a, GOLD2)

def monk(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    robe = skia.Path(); robe.moveTo(-60, -150); robe.quadTo(0, -230, 60, -150); robe.lineTo(150, 200); robe.lineTo(-150, 200); robe.close()
    c.drawPath(robe, P(C((92, 70, 46), a)))
    c.drawCircle(0, -150, 52, P(C((60, 46, 32), a)))
    c.drawCircle(0, -140, 34, P(C(CREAM, a * 0.25)))
    c.drawLine(-40, 40, 40, 40, P(C(GOLD, a), stroke=8))
    c.restore()

def stretcher(c, x, y, a):
    if a <= 0: return
    c.drawRoundRect(skia.Rect(x - 70, y - 14, x + 70, y + 14), 8, 8, P(C(CREAM, a)))
    c.drawCircle(x - 52, y - 26, 16, P(C(CREAM, a)))
    c.drawRect(skia.Rect(x - 6, y - 30, x + 6, y + 2), P(C(RED, a)))
    c.drawRect(skia.Rect(x - 16, y - 20, x + 16, y - 8), P(C(RED, a)))

# ---------------- scenes ----------------
def sc_hook(c, t, D):
    sea(c, 930, 1.0, t)
    warship(c, CX, 900, 1.0, 1.0, t)
    text(c, "SURGERY", CX, 450, ANTON, 140, CREAM, 1.0)
    text(c, "ON A WARSHIP", CX, 580, ANTON, 120, GOLD2, 1.0, glow=22, glow_rgb=GOLD)
    pw = prog(t, W_("hook", "war.") - 0.1, 0.25)
    pop_text(c, "IN A WAR", CX, 1060, ANTON, 96, RED, pw, glow=16, glow_rgb=RED)
    pd = prog(t, W_("hook", "degree.") - 0.15, 0.22)
    if pd > 0: stamp(c, CX, 1170, "NO MEDICAL DEGREE", RED, 76, -5, pd, sc=lerp(2, 1, eo(pd)))

def sc_monk(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "FERDINAND WALDO DEMARA", CX, 420, ANTON, 76, CREAM, a)
    monk(c, CX, 820, 1.2, eo(prog(t, W_("monk", "monk.") - 0.6, 0.4)))
    calendar(c, 230, 700, 0.6, eo(prog(t, W_("monk", "16") - 0.3, 0.3)), "16", "AGE")
    pr = eo(prog(t, W_("monk", "ran") - 0.2, 0.3))
    pill(c, "RAN AWAY TO BECOME A MONK", 1120, pr * (1 - eo(prog(t, beat("monk", 1) - 0.3, 0.2))), CREAM, 58, 860)
    ps = prog(t, beat("monk", 1) - 0.05, 0.25)
    pop_text(c, "JUST THE START", CX, 1120, ANTON, 100, GOLD2, ps, glow=18, glow_rgb=GOLD)

def sc_careers(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pf = eo(prog(t, W_("careers", "suicide,") - 0.6, 0.3))
    out = eo(prog(t, W_("careers", "Doctor") - 0.4, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        text(c, "HE FAKED HIS", CX, 520, ANTON, 110, CREAM, a)
        text(c, "OWN SUICIDE", CX, 650, ANTON, 120, RED, pf, glow=16, glow_rgb=RED)
        c.restore(); c.restore()
    if out > 0:
        id_card(c, CX, 720, 1.1, -3, out, "DR. ROBERT LINTON FRENCH", "PSYCHOLOGIST")
        pp = prog(t, W_("careers", "psychology") - 0.2, 0.3)
        pill(c, "TEACHES PSYCHOLOGY AT A COLLEGE", 1100, eo(pp), GOLD2, 56, 940)
        ident(c, 1, out)

def sc_founder(c, t, D):
    a = eo(prog(t, 0, 0.3))
    id_card(c, CX, 620, 0.95, 2.5, a, "BROTHER JOHN PAYNE", "RELIGIOUS ORDER", tag_="NEW NAME")
    pc = eo(prog(t, W_("founder", "college") - 0.4, 0.4))
    building(c, CX, 1130, 0.55, pc, "COLLEGE")
    pm = prog(t, W_("founder", "Maine.") - 0.15, 0.25)
    if pm > 0: stamp(c, CX + 260, 1000, "MAINE", GOLD2, 80, 8, pm, sc=lerp(2, 1, eo(pm)))
    ident(c, 2, a)

def sc_navy(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "KOREAN WAR", CX, 420, ANTON, 110, CREAM, a)
    pi = eo(prog(t, W_("navy", "Joseph") - 0.3, 0.4))
    id_card(c, CX, 760, 1.0, -2, pi, "SURGEON JOSEPH CYR", "ROYAL CANADIAN NAVY", tag_="BORROWED NAME")
    if pi < 1: sea(c, 900, a * (1 - pi), t); warship(c, CX, 880, 0.9, a * (1 - pi), t)
    ps = prog(t, W_("navy", "surgeon.") - 0.15, 0.25)
    pop_text(c, "SHIP'S SURGEON", CX, 1140, ANTON, 110, GOLD2, ps, glow=20, glow_rgb=GOLD)
    ident(c, 3, pi * (1 - eo(ps)))

def sc_wounded(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("wounded", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        k = clamp((t - W_("wounded", "16") + 0.3) / 1.2)
        for i in range(16):
            stretcher(c, 200 + (i % 4) * 230, 560 + (i // 4) * 110, a if i < int(k * 16) + 1 and k > 0 else a * 0.15)
        pk = prog(t, W_("wounded", "16") - 0.2, 0.25)
        if pk > 0: pop_text(c, "~16 WOUNDED", CX, 1110, ANTON, 120, RED, pk, glow=16, glow_rgb=RED)
        c.restore(); c.restore()
    if out > 0:
        book(c, CX, 760, 1.05, out, t)
        text(c, "THE TEXTBOOK", CX, 440, ANTON, 104, CREAM, out)
        rows = [("READ FAST...", W_("wounded", "read") - 0.1, CREAM), ("THEN OPERATE", W_("wounded", "operated.") - 0.2, GOLD2)]
        seq_rows(c, t, rows, 1130, 100)

def sc_bullet(c, t, D):
    a = eo(prog(t, 0, 0.3))
    # torso outline
    tor = skia.Path(); tor.moveTo(CX - 210, 1080); tor.quadTo(CX - 250, 620, CX - 120, 560); tor.lineTo(CX + 120, 560)
    tor.quadTo(CX + 250, 620, CX + 210, 1080); tor.close()
    c.drawPath(tor, P(C((80, 66, 50), a))); c.drawPath(tor, P(C(GOLD, a), stroke=5))
    c.drawCircle(CX, 480, 70, P(C((80, 66, 50), a))); c.drawCircle(CX, 480, 70, P(C(GOLD, a), stroke=5))
    pe = eo(prog(t, W_("bullet", "removed") - 0.1, 1.0))
    bx, by = lerp(CX + 60, CX + 280, pe), lerp(760, 560, pe)
    c.save(); c.translate(bx, by); c.rotate(-30)
    c.drawRoundRect(skia.Rect(-24, -50, 24, 50), 24, 24, P(C(GOLD2, a))); c.restore()
    if pe > 0: c.drawLine(CX + 60, 760, bx, by, P(C(CREAM, 0.4 * a * (1 - pe)), stroke=3))
    pp = eo(prog(t, W_("bullet", "chest.") - 0.2, 0.3))
    pill(c, "A BULLET FROM A MAN'S CHEST", 1160, pp * (1 - eo(prog(t, beat("bullet", 1) - 0.3, 0.2))), CREAM, 58, 900)
    ps = prog(t, W_("bullet", "survived.") - 0.15, 0.25)
    if ps > 0:
        c.drawRect(skia.Rect(0, 1020, W, 1240), P(C(BG, 0.7 * eo(ps))))
        pop_text(c, "EVERY PATIENT SURVIVED", CX, 1140, ANTON, 92, GOLD2, ps, glow=18, glow_rgb=GOLD)
        text(c, "(REPORTEDLY)", CX, 1215, BEBAS, 48, MUTED, eo(ps), spacing=6)

def sc_exposed(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("exposed", 1)
    news(c, CX, 720, 1.2, -3, a, "EXTRA!", "HERO SHIP DOCTOR", "SURGEON SAVES WOUNDED MEN")
    pr = prog(t, b1 - 0.1, 0.3)
    if pr > 0:
        c.drawRect(skia.Rect(0, 1000, W, 1240), P(C(BG, 0.7 * eo(pr))))
        pop_text(c, "THE REAL DR. CYR", CX, 1110, ANTON, 100, CREAM, pr)
        pop_text(c, "FOUND OUT", CX, 1215, ANTON, 80, RED, prog(t, W_("exposed", "found") - 0.1, 0.25))
    pi = prog(t, W_("exposed", "out.") - 0.05, 0.22)
    if pi > 0: stamp(c, CX, 720, "IMPOSTOR", RED, 140, -10, pi, sc=lerp(2.2, 1, eo(pi)))

def sc_after(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("after", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        text(c, "SENT HOME", CX, 440, ANTON, 120, CREAM, a)
        pn = prog(t, W_("after", "No") - 0.15, 0.25)
        if pn > 0: stamp(c, CX, 800, "NO CHARGES", GOLD2, 130, -6, pn, sc=lerp(2, 1, eo(pn)))
        c.restore(); c.restore()
    if out > 0:
        text(c, "TEXAS PRISON", CX, 440, ANTON, 120, CREAM, out)
        id_card(c, CX, 760, 0.85, 2, out, "PRISON STAFF", "HUNTSVILLE, TEXAS", tag_="NEW JOB")
        pm = prog(t, W_("after", "magazine.") - 0.4, 0.4)
        if pm > 0:
            bars(c, eo(pm), y0=330, y1=1240)
            pop_text(c, "EXPOSED AGAIN", CX, 1150, ANTON, 110, RED, pm, glow=16, glow_rgb=RED)
        ident(c, 4, out * (1 - eo(pm)))

def sc_film(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "HOLLYWOOD", CX, 430, ANTON, 120, GOLD2, a, glow=20, glow_rgb=GOLD)
    for i in range(2):
        cx = CX - 180 + i * 360
        c.save(); c.translate(cx, 760); c.rotate(t * 60 * (1 if i else -1))
        c.drawCircle(0, 0, 150, P(C((60, 56, 50), a))); c.drawCircle(0, 0, 150, P(C(GOLD, a), stroke=6))
        for k in range(5):
            ang = k * 2 * math.pi / 5
            c.drawCircle(80 * math.cos(ang), 80 * math.sin(ang), 34, P(C(BG, a)))
        c.restore()
    c.drawRect(skia.Rect(140, 930, W - 140, 1000), P(C((40, 36, 30), a)))
    for k in range(12): c.drawRect(skia.Rect(160 + k * 66, 948, 196 + k * 66, 982), P(C(CREAM, a * 0.6)))
    pt = prog(t, W_("film", "movie,") - 0.2, 0.25)
    pop_text(c, "\"THE GREAT IMPOSTOR\"", CX, 1110, ANTON, 92, CREAM, pt)
    pc = eo(prog(t, W_("film", "Tony") - 0.2, 0.3))
    pill(c, "STARRING TONY CURTIS · 1961", 1210, pc, GOLD2, 56, 860)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 420, BEBAS, 70, MUTED, a, spacing=10)
    safe(c, CX, 760, 0.9, a, open_=eio(prog(t, W_("cta", "beat") , 1.0)))
    diamond(c, CX + 250, 620, 0.7, eo(prog(t, W_("cta", "diamond") - 0.2, 0.3)), t)
    rows = [("RADAR", W_("cta", "radar,") - 0.1, CREAM), ("HEAT SENSORS", W_("cta", "heat") - 0.1, CREAM),
            ("MAGNETS", W_("cta", "magnets,") - 0.1, CREAM), ("CAUGHT BY A SANDWICH?", W_("cta", "sandwich.") - 0.2, GOLD2)]
    seq_rows(c, t, rows, 1080, 96)
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1200)

def sc_loopend(c, t, D):
    sea(c, 930, 1.0, t)
    warship(c, lerp(CX, CX + 700, eio(prog(t, 0.3, D))), 900, 0.9, 1.0, t)
    pop_text(c, "NO CHARGES.", CX, 520, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)
    pop_text(c, "HE WALKED AWAY.", CX, 650, ANTON, 104, CREAM, prog(t, W_("loopend", "walked") - 0.1, 0.25))
    pop_text(c, "AND THE WORLD LEARNED...", CX, 1150, ANTON, 84, CREAM, prog(t, beat("loopend", 1) - 0.1, 0.25))

E.DRAW = dict(hook=sc_hook, monk=sc_monk, careers=sc_careers, founder=sc_founder, navy=sc_navy, wounded=sc_wounded,
              bullet=sc_bullet, exposed=sc_exposed, after=sc_after, film=sc_film, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"wounded", "exposed"}
_IMP = [("hook", "degree.", -0.15, 0.35), ("careers", "suicide,", -0.2, 0.3), ("founder", "Maine.", -0.15, 0.3),
        ("rehook", "But", -0.1, 0.3), ("wounded", "16", -0.2, 0.3), ("bullet", "survived.", -0.15, 0.3),
        ("exposed", "out.", -0.05, 0.4), ("after", "No", -0.15, 0.35), ("after", "magazine.", -0.4, 0.3),
        ("cta", "sandwich.", -0.2, 0.3), ("loopend", "No", -0.1, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = []
E.set_hits(IMPACTS)
BR = "/home/claude/recitalpha-videos/archive/broll"
CC0 = "FOOTAGE: WIKIMEDIA COMMONS · CC0"
if "navy" in SID: E.BROLL["navy"] = E.load_broll(f"{BR}/ocean06_small.mp4", start=0, dur=6, alpha=0.75, credit=CC0)
if "rehook" in SID: E.BROLL["rehook"] = E.load_broll(f"{BR}/ocean09_small.mp4", start=0, dur=4, alpha=0.6, credit=CC0)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
