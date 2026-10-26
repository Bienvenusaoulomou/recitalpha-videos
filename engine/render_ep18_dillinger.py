import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep18")
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

PH = dict(port=load_photo("dillinger_01.jpg"), poster=load_photo("dillinger_05.jpg"), idc=load_photo("dillinger_02.jpg"),
          mug=load_photo("dillinger_03.jpg"), jail=load_photo("jail_01.jpg"))
CR_FBI = "FBI · PUBLIC DOMAIN"
CR_J = "CROWN POINT JAIL · PHOTO: NYTTEND · PUBLIC DOMAIN"

def car(c, x, y, s, a, rgb=(30, 30, 34)):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.addRoundRect(skia.Rect(-220, -90, 220, 0), 20, 20); c.drawPath(body, P(C(rgb, a)))
    cab = skia.Path(); cab.moveTo(-120, -90); cab.lineTo(-80, -170); cab.lineTo(90, -170); cab.lineTo(130, -90); cab.close(); c.drawPath(cab, P(C(rgb, a)))
    c.drawRect(skia.Rect(-70, -155, 0, -100), P(C((90, 100, 110), a))); c.drawRect(skia.Rect(15, -155, 85, -100), P(C((90, 100, 110), a)))
    for wx in (-130, 130):
        c.drawCircle(wx, 0, 44, P(C((15, 15, 15), a))); c.drawCircle(wx, 0, 20, P(C((150, 150, 150), a)))
    c.drawCircle(215, -50, 12, P(C(GOLD2, a)))
    c.restore()

def road(c, a, t, y=1000):
    c.drawRect(skia.Rect(0, y - 50, W, y + 50), P(C((50, 46, 42), a)))
    for k in range(8):
        x = ((k * 180 - t * 520) % (W + 180)) - 90
        c.drawRect(skia.Rect(x, y - 5, x + 90, y + 5), P(C(GOLD2, a)))

def marquee(c, x, y, a, t):
    if a <= 0: return
    c.drawRect(skia.Rect(x - 380, y - 120, x + 380, y + 120), P(C((60, 30, 30), a)))
    for k in range(24):
        bx = x - 360 + k * 31.3
        on = (int(t * 8) + k) % 3 != 0
        c.drawCircle(bx, y - 105, 8, P(C(GOLD2 if on else (90, 70, 40), a))); c.drawCircle(bx, y + 105, 8, P(C(GOLD2 if on else (90, 70, 40), a)))
    text(c, "BIOGRAPH", x, y + 40, ANTON, 120, CREAM, a, glow=16, glow_rgb=GOLD)

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        bars(c, 1 - out, y0=330, y1=1240)
        pistol(c, CX + 20, 740, 1.5, 1 - out, rot=-8 + 3 * math.sin(t * 3))
        text(c, "A GUN MADE OF", CX, 420, ANTON, 110, CREAM, 1 - out)
        text(c, "WOOD", CX, 1180, ANTON, 170, GOLD2, 1 - out, glow=26, glow_rgb=GOLD)
    if out > 0:
        road(c, out, t)
        car(c, CX, 990, 1.4, out)
        pop_text(c, "THE SHERIFF'S", CX, 420, ANTON, 120, CREAM, prog(t, W_("hook", "sheriff's") - 0.15, 0.25))
        pc = prog(t, W_("hook", "car.") - 0.15, 0.22)
        if pc > 0: stamp(c, CX, 600, "OWN CAR", RED, 140, -5, pc, sc=lerp(2.2, 1, eo(pc)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("who", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["port"], CX, 760, 560, 700, t / b1, a * (1 - out), 1.0, 1.12, focus=(0.5, 0.35), rot=-1.5, credit=CR_FBI)
        pop_text(c, "JOHN DILLINGER", CX, 350, ANTON, 120, CREAM, prog(t, W_("who", "John") - 0.1, 0.25))
        pill(c, "AMERICA'S MOST FAMOUS BANK ROBBER", 1200, eo(prog(t, W_("who", "famous") - 0.2, 0.3)) * (1 - out), GOLD2, 52, 940)
    if out > 0:
        photo_card(c, PH["poster"], CX - 180, 800, 480, 620, 0, out, 1.0, 1.0, rot=-6, credit=None)
        photo_card(c, PH["idc"], CX + 190, 860, 480, 620, 0, eo(prog(t, b1 + 0.3, 0.3)), 1.0, 1.0, rot=5, credit=CR_FBI)
        pop_text(c, "WANTED EVERYWHERE", CX, 370, ANTON, 110, RED, prog(t, b1, 0.25), glow=16, glow_rgb=RED)

def sc_jail(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("jail", 1)
    photo_card(c, PH["jail"], CX, 740, 900, 675, t / D, a, 1.0, 1.15, credit=CR_J)
    pop_text(c, "CROWN POINT, INDIANA", CX, 350, ANTON, 96, CREAM, prog(t, W_("jail", "Crown") - 0.15, 0.25))
    pill(c, "THE SHERIFF WAS CONFIDENT", 1200, eo(prog(t, b1 - 0.1, 0.3)), GOLD2, 58, 820)

def sc_gun(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("gun", 1)
    polish = eo(prog(t, b1, 0.8))
    rgb = tuple(int(lerp(v, w, polish)) for v, w in zip((170, 120, 70), (40, 34, 30)))
    pistol(c, CX + 20, 740, 1.5, a, rot=-6, rgb=rgb)
    rows = [("A PIECE OF WOOD", W_("gun", "piece") - 0.1, CREAM), ("A RAZOR HANDLE BARREL", W_("gun", "razor") - 0.1, GOLD2),
            ("SHOE POLISH", W_("gun", "shoe") - 0.15, RED)]
    seq_rows(c, t, rows, 1180, 90)
    pop_text(c, "A FAKE PISTOL", CX, 400, ANTON, 130, CREAM, prog(t, 0.05, 0.25))

def sc_guards(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("guards", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        pistol(c, CX - 180, 760, 1.2, a * (1 - out), rot=-4, rgb=(40, 34, 30))
        person(c, CX + 260, 760, 110, CREAM, a * (1 - out))
        pop_text(c, "OPEN THE CELL", CX, 420, ANTON, 120, GOLD2, prog(t, W_("guards", "open") - 0.15, 0.25) * (1 - out), glow=18, glow_rgb=GOLD)
    if out > 0:
        k = clamp((t - b1) / max(0.6, D - b1 - 0.4))
        n = int(k * 24)
        for i in range(n):
            person(c, 170 + (i % 8) * 105, 620 + (i // 8) * 170, 40, CREAM, out)
        bars(c, out * 0.85, y0=520, y1=1110)
        counter(c, n, CX, 450, 130, GOLD2, out, prefix="", suffix="+ LOCKED UP", glow=18)
        pill(c, "MORE THAN 2 DOZEN PEOPLE", 1200, eo(prog(t, W_("guards", "dozen") - 0.2, 0.3)), CREAM, 58, 820)

def sc_car(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("car", 1)
    road(c, a, t, 1020)
    car(c, CX - 80, 1010, 1.3, a)
    pop_text(c, "THE SHERIFF'S FORD V-8", CX, 400, ANTON, 96, CREAM, prog(t, W_("car", "sheriff's") - 0.15, 0.25))
    ps = eo(prog(t, b1, 0.5))
    road_sign(c, lerp(W + 300, CX + 300, ps), 680, 0.8, ps, "ILLINOIS", "STATE LINE", rgb=(40, 70, 130))

def sc_feds(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("feds", 1)
    pf = prog(t, W_("feds", "federal") - 0.15, 0.22)
    if pf > 0: stamp(c, CX, 650, "FEDERAL CASE", RED, 130, -5, pf, sc=lerp(2.2, 1, eo(pf)))
    pb = prog(t, b1 - 0.05, 0.25)
    if pb > 0:
        c.save(); c.translate(CX, 980); s = lerp(1.5, 1, back(eo(pb))); c.scale(s, s)
        star = skia.Path()
        for k in range(10):
            r = 170 if k % 2 == 0 else 80
            ang = -math.pi / 2 + k * math.pi / 5
            (star.moveTo if k == 0 else star.lineTo)(r * math.cos(ang), r * math.sin(ang))
        star.close(); c.drawPath(star, P(C(GOLD2, eo(pb)))); c.drawPath(star, P(C(GOLD, eo(pb)), stroke=6))
        text(c, "FBI", 0, 30, ANTON, 80, INK, eo(pb))
        c.restore()
    pop_text(c, "THE FBI WAS AFTER HIM", CX, 400, ANTON, 96, CREAM, prog(t, b1, 0.25))

def sc_end(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("end", 1)
    marquee(c, CX, 720, a, t)
    pop_text(c, "CHICAGO · JULY 1934", CX, 400, ANTON, 100, CREAM, prog(t, 0.05, 0.25))
    pill(c, "FEDERAL AGENTS WERE WAITING", 1000, eo(prog(t, W_("end", "agents") - 0.2, 0.3)), GOLD2, 58, 880)
    pe = prog(t, b1 - 0.05, 0.22)
    if pe > 0: stamp(c, CX, 1170, "THE END", RED, 140, -5, pe, sc=lerp(2.2, 1, eo(pe)))

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("twist", 1)
    pistol(c, CX, 780, 1.6, a, rot=-6, rgb=(60, 46, 34))
    pop_text(c, "\"I CARVED IT MYSELF\"", CX, 420, ANTON, 100, CREAM, prog(t, W_("twist", "carved") - 0.2, 0.25))
    pw = prog(t, W_("twist", "woodworker.") - 0.3, 0.22)
    if pw > 0:
        c.drawRect(skia.Rect(0, 1040, W, 1250), P(C(BG, 0.8 * eo(pw))))
        stamp(c, CX, 1140, "OR A WOODWORKER?", RED, 96, -4, pw, sc=lerp(2, 1, eo(pw)))

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    bridge(c, CX, 1000, 0.95, a)
    pt = prog(t, W_("cta", "sold") - 0.15, 0.25)
    pop_text(c, "HE SOLD THE BROOKLYN BRIDGE", CX, 520, ANTON, 72, CREAM, pt)
    tag(c, CX + 220, 700, "FOR SALE", eo(prog(t, W_("cta", "Bridge.") - 0.2, 0.3)), rot=8)
    pa = prog(t, W_("cta", "again") - 0.2, 0.22)
    if pa > 0: stamp(c, CX, 1110, "AGAIN AND AGAIN", GOLD2, 96, -4, pa, sc=lerp(2, 1, eo(pa)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    bars(c, 1.0, y0=330, y1=1240)
    pistol(c, CX + 20, 740, 1.5, 1.0, rot=-8 + 3 * math.sin(t * 3))
    pop_text(c, "ALL BECAUSE...", CX, 1180, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, who=sc_who, jail=sc_jail, gun=sc_gun, guards=sc_guards, car=sc_car, feds=sc_feds,
              end=sc_end, twist=sc_twist, cta=sc_cta, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"feds", "end"}
_IMP = [("hook", "car.", -0.15, 0.4), ("who", "Wanted", -0.05, 0.3), ("jail", "sheriff", -0.1, 0.3),
        ("rehook", "surprise.", -0.2, 0.35), ("gun", "shoe", -0.15, 0.3), ("guards", "Then", -0.05, 0.3),
        ("car", "state", -0.1, 0.3), ("feds", "federal", -0.15, 0.4), ("end", "It", -0.05, 0.4),
        ("twist", "woodworker.", -0.3, 0.3), ("cta", "again", -0.2, 0.3), ("loopend", "All", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = []
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
