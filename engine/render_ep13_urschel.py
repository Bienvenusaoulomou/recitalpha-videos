import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep13")
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

PH = dict(escort=load_photo("kelly_01.gif"), court=load_photo("kelly_02.gif"), mug=load_photo("machine_gun_kelly_02.jpg"),
          alca=load_photo("alcatraz_1930s.jpg"), drake=load_photo("drake_02.jpg"))
CR = "PHOTO: 1933 · PUBLIC DOMAIN"
CR_DOJ = "PHOTO: U.S. DEPT. OF JUSTICE · PUBLIC DOMAIN"

def blindfold(c, a, y=700, t=0):
    if a <= 0: return
    # silhouette head + band
    c.drawCircle(CX, y, 210, P(C((70, 60, 50), a)))
    body = skia.Path(); body.moveTo(CX - 330, y + 560); body.quadTo(CX, y + 140, CX + 330, y + 560); body.close()
    c.drawPath(body, P(C((70, 60, 50), a)))
    band = skia.Path(); band.addRoundRect(skia.Rect(CX - 230, y - 60, CX + 230, y + 30), 30, 30)
    c.drawPath(band, P(C((20, 18, 16), a)))
    tail = skia.Path(); tail.moveTo(CX + 220, y - 20); tail.quadTo(CX + 320, y + 10 + 20 * math.sin(t * 3), CX + 360, y + 90); tail.lineTo(CX + 330, y + 100)
    tail.quadTo(CX + 290, y + 30, CX + 215, y + 20); tail.close(); c.drawPath(tail, P(C((20, 18, 16), a)))

def sound_waves(c, x, y, a, t, n=4, rgb=GOLD2, left=False):
    for k in range(n):
        f = (t * 0.9 + k / n) % 1
        r = 40 + 220 * f
        st = 150 if left else -30
        c.drawArc(skia.Rect(x - r, y - r, x + r, y + r), st, 60, False, P(C(rgb, a * (1 - f)), stroke=7))

def fingerprint(c, x, y, s, a, rgb=CREAM, p=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(int(9 * p) + 1):
        r = 20 + k * 16
        c.drawArc(skia.Rect(-r * 0.8, -r, r * 0.8, r), 200 + k * 7, 300 - k * 10, False, P(C(rgb, a * 0.85), stroke=6))
    c.restore()

def farmhouse(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-220, -200, 220, 0), P(C((110, 78, 54), a)))
    r = skia.Path(); r.moveTo(-260, -200); r.lineTo(0, -340); r.lineTo(260, -200); r.close(); c.drawPath(r, P(C((70, 50, 36), a)))
    for wx in (-130, 130): c.drawRect(skia.Rect(wx - 40, -150, wx + 40, -80), P(C(GOLD2, a * 0.7)))
    c.drawRect(skia.Rect(-40, -120, 40, 0), P(C((40, 30, 22), a)))
    c.restore()

def car(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.addRoundRect(skia.Rect(-220, -90, 220, 0), 20, 20); c.drawPath(body, P(C((30, 30, 34), a)))
    cab = skia.Path(); cab.moveTo(-120, -90); cab.lineTo(-80, -170); cab.lineTo(90, -170); cab.lineTo(130, -90); cab.close(); c.drawPath(cab, P(C((30, 30, 34), a)))
    c.drawRect(skia.Rect(-70, -155, 0, -100), P(C((90, 100, 110), a))); c.drawRect(skia.Rect(15, -155, 85, -100), P(C((90, 100, 110), a)))
    for wx in (-130, 130):
        c.drawCircle(wx, 0, 44, P(C((15, 15, 15), a))); c.drawCircle(wx, 0, 20, P(C((150, 150, 150), a)))
    c.drawCircle(215, -50, 12, P(C(GOLD2, a)))
    c.restore()

def cards_table(c, x, y, a, t=0):
    c.drawOval(skia.Rect(x - 300, y - 90, x + 300, y + 90), P(C((40, 80, 50), a)))
    c.drawOval(skia.Rect(x - 300, y - 90, x + 300, y + 90), P(C((90, 60, 40), a), stroke=14))
    for i in range(5):
        c.save(); c.translate(x - 120 + i * 60, y - 10 + (i % 2) * 20); c.rotate(-20 + i * 10)
        c.drawRoundRect(skia.Rect(-30, -44, 30, 44), 6, 6, P(C(CREAM, a))); text(c, ["A", "K", "Q", "J", "10"][i], 0, 14, ANTON, 38, RED if i in (1, 2) else INK, a)
        c.restore()

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, W_("hook", "Machine") - 0.4, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        blindfold(c, 1.0, 720, t)
        text(c, "BLINDFOLDED", CX, 400, ANTON, 140, CREAM, 1.0)
        pd = prog(t, W_("hook", "week.") - 0.25, 0.25)
        if pd > 0: stamp(c, CX, 1160, "OVER A WEEK", RED, 110, -5, pd * (1 - eo(prog(t, b1 - 0.2, 0.2))), sc=lerp(2, 1, eo(pd)))
        if t > b1 - 0.1:
            sound_waves(c, CX - 260, 720, 1.0, t, left=True); sound_waves(c, CX + 260, 720, 1.0, t)
            pop_text(c, "HE MEMORIZED EVERY SOUND", CX, 1160, ANTON, 76, GOLD2, prog(t, b1 - 0.1, 0.25), glow=16, glow_rgb=GOLD)
        c.restore(); c.restore()
    if out > 0:
        photo_card(c, PH["escort"], CX, 760, 820, 640, (t - b1) / (D - b1), out, 1.0, 1.12, credit=CR)
        pm = prog(t, W_("hook", "Kelly.") - 0.2, 0.22)
        if pm > 0: stamp(c, CX, 1170, "MACHINE GUN KELLY", RED, 96, -4, pm, sc=lerp(2, 1, eo(pm)))
        pop_text(c, "BROUGHT DOWN", CX, 370, ANTON, 104, CREAM, prog(t, W_("hook", "brought") - 0.1, 0.25))

def sc_taken(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "OKLAHOMA CITY · 1933", CX, 380, ANTON, 92, CREAM, prog(t, 0.05, 0.25))
    cards_table(c, CX, 880, a, t)
    pa = eo(prog(t, W_("taken", "armed") - 0.2, 0.3))
    for i, x in enumerate((CX - 380, CX + 380)):
        person(c, x, 720, 120, (96, 88, 80), pa); c.drawCircle(x, 650, 130, P(C(RED, pa * 0.6), stroke=6))
    pu = eo(prog(t, W_("taken", "Charles") - 0.3, 0.3))
    pill(c, "OILMAN CHARLES URSCHEL", 1130, pu, GOLD2, 60, 820)
    pg = prog(t, W_("taken", "card") - 0.2, 0.25)
    pop_text(c, "MID CARD GAME", CX, 560, BEBAS, 64, MUTED, pg)

def sc_ransom(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("ransom", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    photo_card(c, PH["mug"], CX, 700, 900, 610, t / D, a, 1.0, 1.1, credit=CR_DOJ, dim=0.55 * out)
    pop_text(c, "KELLY & BATES", CX, 340, ANTON, 120, CREAM, prog(t, 0.1, 0.25))
    if out > 0:
        k = eo(prog(t, W_("ransom", "$200,000.") - 0.2, 1.0))
        counter(c, 200000 * k, CX, 760, 170, GOLD2, out, glow=26)
        pill(c, "THE RANSOM", 1130, out, CREAM, 64, 460)

def sc_drive(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("drive", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        # road scrolling
        c.drawRect(skia.Rect(0, 940, W, 1040), P(C((50, 46, 42), a)))
        for k in range(8):
            x = ((k * 180 - t * 520) % (W + 180)) - 90
            c.drawRect(skia.Rect(x, 985, x + 90, 995), P(C(GOLD2, a)))
        car(c, CX, 940, 1.2, a, t)
        pop_text(c, "OKLAHOMA → TEXAS".replace("→", "TO"), CX, 420, ANTON, 104, CREAM, prog(t, 0.1, 0.25))
        pill(c, "HOURS ON THE ROAD", 1160, eo(prog(t, W_("drive", "hours") - 0.2, 0.3)), GOLD2, 60, 640)
        c.restore(); c.restore()
    if out > 0:
        blindfold(c, out, 720, t)
        pc = prog(t, W_("drive", "Chained") - 0.15, 0.22)
        if pc > 0: stamp(c, CX, 1140, "CHAINED", RED, 130, -6, pc, sc=lerp(2, 1, eo(pc)))
        pop_text(c, "UNABLE TO SEE", CX, 380, ANTON, 110, CREAM, prog(t, W_("drive", "Unable") - 0.1, 0.25))

def sc_plane(c, t, D):
    a = eo(prog(t, 0, 0.3))
    farmhouse(c, CX, 1130, 1.1, a)
    f = clamp(t / max(1.0, D))
    plane(c, lerp(-250, W + 250, (f * 1.6) % 1), 560, 0.75, a)
    sound_waves(c, CX, 700, a * 0.7, t)
    clock(c, CX + 330, 820, 110, eo(prog(t, W_("plane", "same") - 0.3, 0.3)), 9.75 + 0.02 * t)
    pop_text(c, "SAME TIME EVERY DAY", CX, 380, ANTON, 96, GOLD2, prog(t, W_("plane", "same") - 0.15, 0.25), glow=18, glow_rgb=GOLD)
    text(c, "A PLANE OVERHEAD", CX - 150, 860, BEBAS, 56, CREAM, eo(prog(t, W_("plane", "plane") - 0.2, 0.3)), spacing=6)

def sc_prints(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("prints", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        n = int(clamp((t - W_("prints", "counted") + 0.2) / 1.2) * 8)
        for i in range(n):
            x = 200 + i * 95; y = 900 + (25 if i % 2 else -25)
            c.drawOval(skia.Rect(x - 26, y - 44, x + 26, y + 44), P(C(CREAM, a * 0.8)))
        counter(c, n, CX, 700, 150, GOLD2, a, prefix="", suffix=" STEPS", glow=18)
        sound_waves(c, CX - 300, 480, a, t, left=True); sound_waves(c, CX + 300, 480, a, t)
        pop_text(c, "EVERY VOICE", CX, 480, ANTON, 90, CREAM, prog(t, W_("prints", "voice,") - 0.2, 0.25))
        c.restore(); c.restore()
    if out > 0:
        for i, (x, y, s) in enumerate(((300, 620, 1.3), (760, 560, 1.0), (560, 900, 1.5), (850, 1000, 1.1), (250, 1050, 0.9))):
            fingerprint(c, x, y, s, out * eo(prog(t, b1 + 0.2 + i * 0.25, 0.3)), CREAM, p=eo(prog(t, b1 + 0.2 + i * 0.25, 0.6)))
        pop_text(c, "FINGERPRINTS", CX, 400, ANTON, 120, GOLD2, prog(t, W_("prints", "fingerprints") - 0.15, 0.25), glow=18, glow_rgb=GOLD)
        pill(c, "ON EVERYTHING HE COULD REACH", 1190, eo(prog(t, W_("prints", "everything") - 0.2, 0.3)), CREAM, 56, 880)

def sc_paid(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("paid", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        for i in range(6): bills(c, 220 + (i % 3) * 320, 620 + (i // 3) * 170, a * (1 - out), 3, rot=(i - 3) * 5)
        counter(c, 200000, CX, 1000, 140, GOLD2, a * (1 - out), glow=20)
        pf = prog(t, W_("paid", "free.") - 0.2, 0.22)
        if pf > 0: stamp(c, CX, 1160, "SET FREE", GOLD2, 110, -5, pf * (1 - out), sc=lerp(2, 1, eo(pf)))
    if out > 0:
        ticket(c, CX, 760, 1.0, out, rot=-3, head="CASE FILE", title="URSCHEL KIDNAPPING", sub="FEDERAL AGENTS")
        pop_text(c, "HE TOLD THE FBI", CX, 400, ANTON, 110, CREAM, prog(t, b1 - 0.05, 0.25))
        pop_text(c, "EVERYTHING", CX, 1140, ANTON, 120, GOLD2, prog(t, W_("paid", "everything.") - 0.2, 0.25), glow=20, glow_rgb=GOLD)

def sc_raid(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("raid", 1)
    farmhouse(c, CX, 1080, 1.0, a)
    pin(c, CX + 330, 930, 0.9, eo(prog(t, W_("raid", "Paradise,") - 0.3, 0.3)), RED)
    pop_text(c, "PARADISE, TEXAS", CX, 400, ANTON, 120, CREAM, prog(t, W_("raid", "Paradise,") - 0.1, 0.25))
    pr = prog(t, W_("raid", "raided") - 0.15, 0.22)
    if pr > 0:
        g = P(C(RED, 0.25 * (0.5 + 0.5 * math.sin(t * 14)))); c.drawRect(skia.Rect(0, 330, W, 1240), g)
        stamp(c, CX, 600, "RAID · AUGUST 1933", RED, 90, -4, pr, sc=lerp(2, 1, eo(pr)))
    pm = eo(prog(t, W_("raid", "ransom") - 0.3, 0.3))
    for i in range(3): bills(c, CX - 220 + i * 220, 1180, pm, 2, rot=(i - 1) * 8)
    pill(c, "PART OF THE RANSOM FOUND", 1230, pm, GOLD2, 52, 760)

def sc_caught(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("caught", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["court"], CX, 790, 620, 800, t / b1, a * (1 - out), 1.0, 1.12, focus=(0.5, 0.35), credit=CR)
        pop_text(c, "CAUGHT · SEPT. 1933", CX, 330, ANTON, 96, CREAM, prog(t, 0.05, 0.25))
    if out > 0:
        photo_card(c, PH["alca"], CX, 720, 940, 620, (t - b1) / (D - b1), out, 1.0, 1.12, credit="PHOTO: ALCATRAZ · PUBLIC DOMAIN", dim=0.3)
        pl = prog(t, b1 - 0.05, 0.22)
        if pl > 0: stamp(c, CX, 720, "LIFE", RED, 190, -6, pl, sc=lerp(2.2, 1, eo(pl)))
        pop_text(c, "17 YEARS ON ALCATRAZ", CX, 1150, ANTON, 92, GOLD2, prog(t, W_("caught", "17") - 0.15, 0.25), glow=16, glow_rgb=GOLD)

def sc_myth(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("myth", 1)
    # speech bubble
    pb = eo(prog(t, W_("myth", "Don't") - 0.2, 0.3))
    c.save(); c.translate(CX, 700); s = lerp(0.6, 1, back(pb)); c.scale(s, s)
    bub = skia.Path(); bub.addRoundRect(skia.Rect(-420, -170, 420, 170), 80, 80)
    tl = skia.Path(); tl.moveTo(-160, 160); tl.lineTo(-260, 300); tl.lineTo(-60, 165); tl.close()
    c.drawPath(bub, P(C(CREAM, pb))); c.drawPath(tl, P(C(CREAM, pb)))
    text(c, "\"DON'T SHOOT,", 0, -10, ANTON, 104, INK, pb); text(c, "G-MEN!\"", 0, 110, ANTON, 110, RED, pb)
    c.restore()
    pop_text(c, "THE LEGEND", CX, 400, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    pm = prog(t, W_("myth", "myth.") - 0.2, 0.22)
    if pm > 0: c.drawRect(skia.Rect(0, 450, W, 960), P(C(BG, 0.75 * eo(pm))))
    if pm > 0: stamp(c, CX, 700, "PROBABLY A MYTH", RED, 110, -8, pm, sc=lerp(2.2, 1, eo(pm)))
    pn = eo(prog(t, W_("myth", "nickname") - 0.2, 0.3))
    pill(c, "BUT THE NICKNAME STUCK", 1160, pn, GOLD2, 62, 800)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    photo_card(c, PH["drake"], CX, 810, 460, 560, t / D, a, 1.0, 1.1, focus=(0.5, 0.3), rot=2, credit="PAINTING: M. GHEERAERTS · PUBLIC DOMAIN")
    pt = prog(t, W_("cta", "thousands") - 0.2, 0.25)
    pop_text(c, "SIR FRANCIS DRAKE'S FORTUNE", CX, 480, ANTON, 70, GOLD2, pt, glow=16, glow_rgb=GOLD)
    pe = prog(t, W_("cta", "exist.") - 0.3, 0.22)
    if pe > 0: stamp(c, CX, 1090, "IT DIDN'T EXIST", RED, 100, -5, pe, sc=lerp(2, 1, eo(pe)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    blindfold(c, 1.0, 720, t)
    sound_waves(c, CX - 260, 720, 1.0, t, left=True); sound_waves(c, CX + 260, 720, 1.0, t)
    pop_text(c, "ALL BECAUSE...", CX, 1170, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, taken=sc_taken, ransom=sc_ransom, drive=sc_drive, plane=sc_plane, prints=sc_prints, paid=sc_paid,
              raid=sc_raid, caught=sc_caught, myth=sc_myth, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"raid", "drive"}
_IMP = [("hook", "Kelly.", -0.2, 0.4), ("taken", "armed", -0.2, 0.3), ("ransom", "$200,000.", -0.2, 0.35),
        ("drive", "Chained", -0.15, 0.35), ("rehook", "clues.", -0.1, 0.3), ("prints", "fingerprints", -0.15, 0.3),
        ("paid", "free.", -0.2, 0.3), ("raid", "raided", -0.15, 0.4), ("caught", "Life", -0.05, 0.4),
        ("myth", "myth.", -0.2, 0.35), ("cta", "exist.", -0.3, 0.3), ("loopend", "All", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = []
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
