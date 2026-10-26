import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep19")
sys.path.insert(0, os.environ["REC_ROOT"])
import numpy as np, skia
from PIL import Image
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

def load_color(name):
    im = Image.open(f"{E.ROOT}/img/{name}").convert("RGB")
    a = np.array(im); a = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(a), colorType=skia.kRGBA_8888_ColorType)

PH = dict(ci=load_color("george_parker_04.jpg"), jackson=load_photo("george_parker_01.jpg"), parker=load_photo("parker_01.jpg"),
          fire=load_color("bridge_02.jpg"), brainerd=load_photo("bridge_01.jpg"))
CR_CI = "CURRIER & IVES, 1883 · PUBLIC DOMAIN"
CR_J = "PHOTO: W. H. JACKSON, c.1900 · LOC · PUBLIC DOMAIN"
CR = "PUBLIC DOMAIN"

def tollbooth(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-80, -200, 80, 0), P(C((150, 60, 50), a)))
    r = skia.Path(); r.moveTo(-100, -200); r.lineTo(0, -270); r.lineTo(100, -200); r.close(); c.drawPath(r, P(C((90, 40, 34), a)))
    c.drawRect(skia.Rect(-50, -160, 50, -90), P(C(GOLD2, a * 0.8)))
    text(c, "TOLL", 0, -20, ANTON, 50, CREAM, a)
    c.drawRect(skia.Rect(80, -80, 320, -64), P(C((230, 230, 230), a)))
    for k in range(4): c.drawRect(skia.Rect(110 + k * 60, -80, 140 + k * 60, -64), P(C(RED, a)))
    c.restore()

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    photo_card(c, PH["ci"], CX, 790, 900, 660, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.4), rot=-1.5, credit=CR_CI, dim=0.25 * eo(prog(t, b1 - 0.2, 0.3)))
    text(c, "HE SOLD THE", CX, 390, ANTON, 120, CREAM, 1.0)
    text(c, "BROOKLYN BRIDGE", CX, 1210, ANTON, 120, GOLD2, 1.0, glow=22, glow_rgb=GOLD)
    pw = prog(t, W_("hook", "twice") - 0.15, 0.22)
    if pw > 0:
        stamp(c, CX, 790, "TWICE A WEEK", RED, 130, -7, pw, sc=lerp(2.2, 1, eo(pw)), sub="REPORTEDLY")

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("who", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["parker"], CX, 760, 520, 620, t / b1, a * (1 - out), 1.0, 1.12, focus=(0.5, 0.4), rot=-1.5, credit=CR)
        pop_text(c, "GEORGE C. PARKER", CX, 360, ANTON, 110, CREAM, prog(t, W_("who", "George") - 0.15, 0.25))
        pill(c, "NEW YORK", 1170, a * (1 - out), GOLD2, 60, 400)
    if out > 0:
        for i in range(12):
            x = 170 + (i % 6) * 150; y = 720 + (i // 6) * 220
            person(c, x, y, 50, CREAM if i % 4 else GOLD2, out * clamp((t - b1) * 3 - i * 0.12))
            c.drawRect(skia.Rect(x + 30, y + 40, x + 70, y + 80), P(C((120, 84, 50), out * clamp((t - b1) * 3 - i * 0.12))))
        pop_text(c, "NEW IMMIGRANTS", CX, 420, ANTON, 120, GOLD2, prog(t, W_("who", "immigrants.") - 0.3, 0.25), glow=18, glow_rgb=GOLD)
        text(c, "HIS FAVORITE TARGETS", CX, 1250 - 40, BEBAS, 60, CREAM, out, spacing=6)

def sc_pitch(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("pitch", 1)
    bridge(c, CX, 1000, 0.95, a)
    tollbooth(c, CX - 300, 1000, 0.8, eo(prog(t, W_("pitch", "toll") - 0.3, 0.3)))
    pop_text(c, "CHARGE A TOLL", CX, 400, ANTON, 120, CREAM, prog(t, W_("pitch", "toll") - 0.15, 0.25))
    k = clamp((t - b1) / max(0.5, D - b1 - 0.3))
    counter(c, 100000 * eo(k), CX, 600, 110, GOLD2, eo(prog(t, b1 - 0.1, 0.3)), suffix="...", glow=18)
    pe = prog(t, W_("pitch", "forever.") - 0.3, 0.22)
    if pe > 0: stamp(c, CX, 1180, "EASY MONEY FOREVER", GOLD2, 90, -4, pe, sc=lerp(2, 1, eo(pe)))

def sc_papers(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("papers", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        paper_doc(c, CX, 780, 1.0, -2, a * (1 - out), "DEED OF OWNERSHIP", "CITY OF NEW YORK", "BROOKLYN BRIDGE")
        signature(c, CX + 100, 1030, prog(t, 0.6, 0.8), a * (1 - out), "G. C. Parker", 60)
        pf = prog(t, W_("papers", "forged") - 0.15, 0.22)
        if pf > 0: stamp(c, CX, 780, "FORGED", RED, 150, -10, pf * (1 - out), sc=lerp(2.2, 1, eo(pf)))
    if out > 0:
        building(c, CX, 1120, 0.85, out, "PARKER & CO.", cols=6)
        pop_text(c, "REAL OFFICES", CX, 420, ANTON, 120, GOLD2, prog(t, W_("papers", "real") - 0.15, 0.25), glow=18, glow_rgb=GOLD)
        pill(c, "TO LOOK LEGIT", 560, eo(prog(t, W_("papers", "legit.") - 0.3, 0.3)), CREAM, 60, 480)

def sc_tolls(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("tolls", 1)
    photo_card(c, PH["jackson"], CX, 720, 940, 660, t / D, a, 1.0, 1.12, credit=CR_J, dim=0.25)
    tollbooth(c, CX - 160, 1000, 0.9, eo(prog(t, W_("tolls", "toll") - 0.3, 0.3)))
    pop_text(c, "THEY SET UP TOLL BOOTHS", CX, 340, ANTON, 92, CREAM, prog(t, W_("tolls", "toll") - 0.15, 0.25))
    pp = prog(t, W_("tolls", "police") - 0.15, 0.22)
    if pp > 0:
        g = P(C(RED, 0.2 * (0.5 + 0.5 * math.sin(t * 14)))); c.drawRect(skia.Rect(0, 330, W, 1240), g)
        stamp(c, CX, 1170, "POLICE: THROWN OFF", RED, 92, -5, pp, sc=lerp(2, 1, eo(pp)))

def sc_more(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("more", 1)
    pop_text(c, "NOT JUST BRIDGES", CX, 400, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    items = [("GRANT'S TOMB", W_("more", "Grant's"), -4), ("STATUE OF LIBERTY", W_("more", "Statue"), 3), ("MADISON SQUARE GARDEN", W_("more", "Madison"), -2)]
    for i, (lb, t0, rot) in enumerate(items):
        d = eo(prog(t, t0 - 0.2, 0.3))
        ticket(c, CX + (i - 1) * 30, 640 + i * 200, 0.7, d, rot=rot, head="DEED OF SALE", title=lb, sub="SOLD BY G. C. PARKER")
        if d > 0.8: stamp(c, CX + 250, 700 + i * 200, "SOLD", RED, 70, 10, prog(t, t0 + 0.2, 0.2))

def sc_caught(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("caught", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        for i in range(3):
            d = eo(prog(t, 0.4 + i * 0.4, 0.3))
            stamp(c, CX, 560 + i * 220, "CONVICTED #%d" % (i + 1), RED, 96, -5 + i * 4, d * (1 - out), sc=lerp(2, 1, d))
    if out > 0:
        bars(c, out, y0=330, y1=1240)
        pop_text(c, "1928", CX, 470, ANTON, 150, CREAM, prog(t, W_("caught", "1928,") - 0.2, 0.25))
        pl = prog(t, W_("caught", "life") - 0.15, 0.22)
        if pl > 0: stamp(c, CX, 820, "LIFE", RED, 200, -6, pl, sc=lerp(2.2, 1, eo(pl)), sub="SING SING")

def sc_prison(c, t, D):
    a = eo(prog(t, 0, 0.3))
    calendar(c, CX, 700, 1.0, a, "1937", "SING SING")
    pn = prog(t, W_("prison", "never") - 0.15, 0.25)
    pop_text(c, "HE NEVER OWNED", CX, 1050, ANTON, 104, CREAM, pn)
    pop_text(c, "A THING HE SOLD", CX, 1170, ANTON, 104, GOLD2, prog(t, W_("prison", "thing") - 0.15, 0.25), glow=18, glow_rgb=GOLD)

def sc_phrase(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("phrase", 1)
    photo_card(c, PH["brainerd"], CX, 760, 940, 574, t / D, a, 1.0, 1.1, credit="PHOTO: G. B. BRAINERD · PUBLIC DOMAIN", dim=0.55 * eo(prog(t, b1 - 0.2, 0.3)))
    pop_text(c, "HIS LEGACY", CX, 380, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    p1 = prog(t, b1 - 0.05, 0.25)
    pop_text(c, "\"IF YOU BELIEVE THAT,", CX, 700, ANTON, 92, CREAM, p1)
    pop_text(c, "I HAVE A BRIDGE", CX, 820, ANTON, 104, GOLD2, prog(t, W_("phrase", "bridge") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    pop_text(c, "TO SELL YOU.\"", CX, 940, ANTON, 104, GOLD2, prog(t, W_("phrase", "sell") - 0.15, 0.25), glow=18, glow_rgb=GOLD)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    building(c, CX, 1060, 0.7, a, "U.S. MINT", cols=6)
    pm = prog(t, W_("cta", "Mint") - 0.15, 0.25)
    pop_text(c, "ROBBING THE U.S. MINT", CX, 540, ANTON, 90, CREAM, pm)
    k = eo(prog(t, W_("cta", "$200,000") - 0.2, 0.8))
    counter(c, 200000 * k, CX, 660, 110, GOLD2, eo(prog(t, W_("cta", "$200,000") - 0.3, 0.3)), glow=18)
    ps = prog(t, W_("cta", "90") - 0.15, 0.22)
    if ps > 0: stamp(c, CX, 1110, "IN 90 SECONDS", RED, 100, -4, ps, sc=lerp(2, 1, eo(ps)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    photo_card(c, PH["ci"], CX, 740, 860, 620, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.4), rot=-1.5, credit=None, dim=0.5)
    pop_text(c, "\"I HAVE A BRIDGE", CX, 700, ANTON, 104, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=18, glow_rgb=GOLD)
    pop_text(c, "TO SELL YOU.\"", CX, 820, ANTON, 104, GOLD2, prog(t, W_("loopend", "sell") - 0.15, 0.25), glow=18, glow_rgb=GOLD)
    pop_text(c, "BECAUSE...", CX, 1210, ANTON, 110, CREAM, prog(t, W_("loopend", "Because") - 0.1, 0.25))

E.DRAW = dict(hook=sc_hook, who=sc_who, pitch=sc_pitch, papers=sc_papers, tolls=sc_tolls, more=sc_more, caught=sc_caught,
              prison=sc_prison, phrase=sc_phrase, cta=sc_cta, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"caught", "tolls"}
_IMP = [("hook", "twice", -0.15, 0.4), ("who", "immigrants.", -0.3, 0.3), ("pitch", "forever.", -0.3, 0.3),
        ("papers", "forged", -0.15, 0.35), ("rehook", "tolls.", -0.2, 0.3), ("tolls", "police", -0.15, 0.4),
        ("more", "Statue", -0.2, 0.3), ("caught", "life", -0.15, 0.4), ("prison", "never", -0.15, 0.3),
        ("phrase", "bridge", -0.2, 0.35), ("cta", "90", -0.15, 0.3), ("loopend", "If", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("pitch", "toll", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
