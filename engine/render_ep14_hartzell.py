import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep14")
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

PH = dict(drake=load_photo("drake_02.jpg"), engr=load_photo("drake_01.jpg", maxw=1100), crowd=load_photo("great_depression_01.jpg"))
CR_P = "PAINTING: M. GHEERAERTS · PUBLIC DOMAIN"
CR_E = "ENGRAVING: J. HONDIUS, 1583 · PUBLIC DOMAIN"
CR_C = "PHOTO: U.S. GOV, 1929 · PUBLIC DOMAIN"

def envelope(c, x, y, s, a, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-120, -75, 120, 75), P(C((236, 226, 204), a)))
    p = skia.Path(); p.moveTo(-120, -75); p.lineTo(0, 15); p.lineTo(120, -75); c.drawPath(p, P(C((160, 140, 110), a), stroke=4))
    text(c, "$", 70, 55, ANTON, 50, (60, 120, 70), a)
    c.restore()

def people_grid(c, n, a, y0=560, cols=10, rows=6):
    for i in range(min(n, cols * rows)):
        x = 150 + (i % cols) * 87; y = y0 + (i // cols) * 100
        person(c, x, y, 26, CREAM if i % 7 else GOLD2, a)

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    photo_card(c, PH["drake"], CX, 780, 540, 640, t / D, 1.0, 1.0, 1.12, focus=(0.5, 0.3), rot=-1.5, credit=CR_P)
    text(c, "SIR FRANCIS DRAKE'S", CX, 390, ANTON, 92, CREAM, 1.0)
    text(c, "FORTUNE", CX, 1200, ANTON, 130, GOLD2, 1.0, glow=24, glow_rgb=GOLD)
    pn = prog(t, b1 - 0.05, 0.22)
    if pn > 0: stamp(c, CX, 780, "NEVER EXISTED", RED, 120, -8, pn, sc=lerp(2.2, 1, eo(pn)))

def sc_claim(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("claim", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    photo_card(c, PH["engr"], CX, 760, 620, 790, t / D, a, 1.0, 1.1, focus=(0.5, 0.35), rot=1.5, credit=CR_E, dim=0.6 * out)
    if out < 1:
        pc = eo(prog(t, W_("claim", "300") - 0.3, 0.3))
        calendar(c, CX, 760, 0.9, pc * (1 - out), "300", "YEARS")
        pop_text(c, "UNCLAIMED ESTATE", CX, 330, ANTON, 104, CREAM, prog(t, 0.05, 0.25) * (1 - out))
    if out > 0:
        k = eo(prog(t, b1 + 0.3, 1.4))
        counter(c, 100e9 * k, CX, 800, 130, GOLD2, out, glow=26)
        pop_text(c, "WITH INTEREST...", CX, 330, ANTON, 104, CREAM, prog(t, b1 - 0.05, 0.25))
        text(c, "(SUPPOSEDLY)", CX, 900, BEBAS, 56, MUTED, out, spacing=6)

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    id_card(c, CX, 640, 1.0, -3, a, "OSCAR HARTZELL", "THE SELLER", tag_="THE DRAKE ESTATE")
    pc = eo(prog(t, W_("who", "con") - 0.3, 0.3))
    for i, x in enumerate((CX - 250, CX + 250)):
        person(c, x, 1010, 70, (110, 100, 90), pc)
    text(c, "2 CON ARTISTS STARTED IT", CX, 1200, ANTON, 70, RED, pc)
    pop_text(c, "HE TOOK OVER", CX, 360, ANTON, 110, GOLD2, prog(t, W_("who", "took") - 0.15, 0.25), glow=18, glow_rgb=GOLD)

def sc_promise(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("promise", 1)
    coin(c, 300, 760, 110, a, "$1", 80)
    text(c, "YOU GIVE", 300, 540, BEBAS, 60, CREAM, a, spacing=6)
    pb = eo(prog(t, b1 - 0.1, 0.4))
    for i in range(10): bills(c, 760, 900 - i * 34, pb * clamp(pb * 10 - i), 2, rot=(i % 3 - 1) * 4)
    text(c, "YOU GET BACK", 760, 540, BEBAS, 60, CREAM, pb, spacing=6)
    pp = prog(t, W_("promise", "$500") - 0.15, 0.25)
    pop_text(c, "$500", 760, 1100, ANTON, 150, GOLD2, pp, glow=24, glow_rgb=GOLD)
    pop_text(c, "FIGHT FOR THE ESTATE", CX, 380, ANTON, 92, CREAM, prog(t, W_("promise", "fight") - 0.15, 0.25))
    text(c, "(REPORTEDLY)", CX, 1220, BEBAS, 46, MUTED, pb, spacing=6)

def sc_london(c, t, D):
    a = eo(prog(t, 0, 0.3))
    mansion(c, CX, 1100, 1.0, a, t)
    pop_text(c, "LONDON", CX, 380, ANTON, 140, CREAM, prog(t, W_("london", "London,") - 0.15, 0.25))
    pl = prog(t, W_("london", "luxury") - 0.2, 0.25)
    pill(c, "LIVING IN LUXURY ON THEIR MONEY", 1180, eo(pl), GOLD2, 56, 920)
    for i in range(5): bills(c, 200 + i * 170, lerp(450, 640, ((t * 0.5 + i * 0.37) % 1)), a * eo(pl) * 0.9, 1, rot=t * 40 + i * 30)

def sc_numbers(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("numbers", 1)
    k = clamp(t / max(0.5, b1 - 0.2))
    people_grid(c, int(k * 60), a * (1 - 0.6 * eo(prog(t, b1 - 0.2, 0.3))))
    counter(c, 70000 * eo(k), CX, 420, 150, CREAM, a, prefix="", suffix="+ PEOPLE", glow=0)
    pm = prog(t, b1 - 0.05, 0.25)
    if pm > 0:
        c.drawRect(skia.Rect(0, 780, W, 1000), P(C(BG, 0.75 * eo(pm))))
        counter(c, 2000000 * eo(prog(t, b1, 0.9)), CX, 940, 150, GOLD2, eo(pm), suffix="+", glow=24)

def sc_depression(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["crowd"], CX, 740, 900, 640, t / D, a, 1.0, 1.15, credit=CR_C, dim=0.25)
    pop_text(c, "THE GREAT DEPRESSION", CX, 340, ANTON, 100, CREAM, prog(t, W_("depression", "Great") - 0.15, 0.25))
    pe = prog(t, W_("depression", "kept") - 0.3, 0.3)
    rng = random.Random(4)
    for i in range(8):
        d = clamp((t - W_("depression", "kept") + 0.3) * 1.2 - i * 0.12)
        if d > 0: envelope(c, lerp(rng.uniform(100, 980), CX, eo(d)), lerp(1300, 760, eo(d)), 0.7, (1 - eo(clamp(d * 1.3 - 0.3))) + 0.0, rot=rng.uniform(-25, 25))
    pill(c, "THEY KEPT SENDING CASH", 1180, eo(pe), GOLD2, 60, 760)

def sc_deport(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("deport", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        pd = prog(t, W_("deport", "deported") - 0.15, 0.22)
        if pd > 0: stamp(c, CX, 560, "DEPORTED · 1933", RED, 100, -5, pd, sc=lerp(2, 1, eo(pd)))
        building(c, CX, 1150, 0.8, eo(prog(t, W_("deport", "Sioux") - 0.3, 0.3)), "COURT", cols=6)
        pop_text(c, "SIOUX CITY, IOWA", CX, 380, ANTON, 104, CREAM, prog(t, W_("deport", "Sioux") - 0.15, 0.25))
        c.restore(); c.restore()
    if out > 0:
        pp = eo(prog(t, b1, 0.3)) * (1 - eo(prog(t, W_("deport", "Hartzell", 1) - 0.3, 0.3)))
        paper_doc(c, CX, 760, 0.95, -2, out * pp, "EXPERT TESTIMONY", "UNIVERSITY PROFESSOR", "DRAKE HAD NO HEIRS")
        pb = eo(prog(t, W_("deport", "Hartzell", 1) - 0.3, 0.4))
        if pb > 0:
            bars(c, pb, y0=330, y1=1240)
            pt = prog(t, W_("deport", "10") - 0.15, 0.25)
            if pt > 0: stamp(c, CX, 760, "10 YEARS", RED, 150, -6, pt, sc=lerp(2.2, 1, eo(pt)))

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("twist", 1)
    rng = random.Random(9)
    for i in range(10):
        d = clamp((t - W_("twist", "money") + 0.3) * 1.5 - i * 0.1)
        if d > 0: envelope(c, rng.uniform(150, 930), lerp(1300, rng.uniform(560, 1000), eo(d)), 0.6, a, rot=rng.uniform(-30, 30))
    pop_text(c, "THEY PAID FOR HIS DEFENSE", CX, 400, ANTON, 84, CREAM, prog(t, W_("twist", "defense.") - 0.4, 0.25))
    pb = prog(t, b1 - 0.05, 0.25)
    if pb > 0:
        c.drawRect(skia.Rect(0, 1040, W, 1250), P(C(BG, 0.75 * eo(pb))))
        stamp(c, CX, 1140, "BELIEVED FOR LIFE", GOLD2, 100, -4, pb, sc=lerp(2, 1, eo(pb)))

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    matchbox(c, CX - 160, 900, 1.0, a, rot=-6)
    match(c, CX + 260, 1020, 1.4, a, t, lit=eo(prog(t, W_("cta", "Match") - 0.2, 0.3)), rot=12)
    pop_text(c, "THE MATCH KING", CX, 560, ANTON, 120, GOLD2, prog(t, W_("cta", "Match") - 0.1, 0.25), glow=22, glow_rgb=GOLD)
    pc = prog(t, W_("cta", "countries.") - 0.3, 0.25)
    pop_text(c, "LENT MONEY TO COUNTRIES", CX, 680, ANTON, 70, CREAM, pc)
    pr = prog(t, W_("cta", "really") - 0.2, 0.25)
    if pr > 0: stamp(c, CX, 1110, "WHAT WAS IT REALLY?", RED, 84, -4, pr, sc=lerp(2, 1, eo(pr)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    photo_card(c, PH["drake"], CX, 760, 560, 700, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.3), rot=-1.5, credit=CR_P, dim=0.3)
    counter(c, 100e9, CX, 420, 120, GOLD2, prog(t, 0.0, 0.22), glow=20)
    pn = prog(t, W_("loopend", "never") - 0.1, 0.22)
    if pn > 0: stamp(c, CX, 760, "NEVER EXISTED", RED, 120, -8, pn, sc=lerp(2.2, 1, eo(pn)))
    pop_text(c, "AND STILL...", CX, 1200, ANTON, 110, GOLD2, prog(t, beat("loopend", 1) - 0.1, 0.25), glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, claim=sc_claim, who=sc_who, promise=sc_promise, london=sc_london, numbers=sc_numbers,
              depression=sc_depression, deport=sc_deport, twist=sc_twist, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"deport"}
_IMP = [("hook", "fortune", -0.1, 0.4), ("claim", "With", -0.1, 0.3), ("who", "took", -0.15, 0.3),
        ("promise", "$500", -0.15, 0.35), ("rehook", "paying.", -0.2, 0.35), ("london", "luxury", -0.2, 0.3),
        ("numbers", "At", -0.05, 0.35), ("depression", "kept", -0.3, 0.3), ("deport", "deported", -0.15, 0.35),
        ("deport", "10", -0.15, 0.4), ("twist", "Some", -0.05, 0.35), ("cta", "Match", -0.1, 0.3),
        ("loopend", "never", -0.1, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("promise", "$500", 0.0), ("numbers", "At", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
