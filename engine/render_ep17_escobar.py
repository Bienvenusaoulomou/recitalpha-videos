import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep17")
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

PH = dict(mug=load_photo("escobar_03.jpg"), mug2=load_photo("escobar_02.jpg"))
CR = "PHOTO: COLOMBIAN NATIONAL POLICE, 1976 · PUBLIC DOMAIN"

def timer(c, x, y, secs, a, size=150, limit=120):
    m, s = int(secs) // 60, int(secs) % 60
    rgb = RED if secs > limit else GOLD2
    c.drawRoundRect(skia.Rect(x - 260, y - size * 0.95, x + 260, y + size * 0.25), 24, 24, P(C((20, 18, 16), a * 0.9)))
    c.drawRoundRect(skia.Rect(x - 260, y - size * 0.95, x + 260, y + size * 0.25), 24, 24, P(C(rgb, a), stroke=5))
    text(c, "%02d:%02d" % (m, s), x, y, ANTON, size, rgb, a, glow=18 if secs > limit else 0, glow_rgb=RED)

def city_grid(c, a, t, focus=0.0, fx=CX + 120, fy=820):
    for i in range(7):
        for j in range(6):
            x = 130 + i * 140; y = 470 + j * 140
            c.drawRect(skia.Rect(x, y, x + 110, y + 110), P(C((70, 64, 56), a * (1 - 0.7 * focus * (1 - math.exp(-((x + 55 - fx) ** 2 + (y + 55 - fy) ** 2) / 20000))))))
    r = lerp(520, 70, eio(focus))
    c.drawCircle(fx, fy, r, P(C(RED, a), stroke=6))
    g = P(C(RED, a * 0.15)); c.drawCircle(fx, fy, r, g)

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["mug"], CX, 760, 620, 620, t / b1, 1 - out, 1.0, 1.1, focus=(0.5, 0.4), rot=-1.5, credit=CR)
        text(c, "MOST WANTED", CX, 370, ANTON, 130, CREAM, 1 - out)
        counter(c, 16, CX, 1220, 110, GOLD2, 1 - out, prefix="HID ", suffix=" MONTHS", glow=18)
    if out > 0:
        phone(c, CX - 230, 800, 1.1, out, rot=-8, t=t, ring=0.6)
        secs = lerp(95, 167, clamp((t - b1) / max(0.5, D - b1 - 0.3)))
        timer(c, CX + 170, 820, secs, out, 130)
        pop_text(c, "ONE CALL", CX, 420, ANTON, 140, CREAM, prog(t, b1 - 0.05, 0.22))
        pl = prog(t, W_("hook", "long.") - 0.2, 0.22)
        if pl > 0: stamp(c, CX, 1150, "TOO LONG", RED, 140, -5, pl, sc=lerp(2.2, 1, eo(pl)))

def sc_escape(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("escape", 1)
    # prison on a hill
    hill = skia.Path(); hill.moveTo(0, 1240); hill.quadTo(CX, 760, W, 1240); hill.close(); c.drawPath(hill, P(C((50, 70, 46), a)))
    building(c, CX, 1000, 0.6, a, "LA CATEDRAL", cols=5)
    pop_text(c, "JULY 1992", CX, 380, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    pw = prog(t, W_("escape", "walked") - 0.15, 0.22)
    if pw > 0: stamp(c, CX, 560, "HE WALKED OUT", RED, 110, -5, pw, sc=lerp(2, 1, eo(pw)))
    pill(c, "A LUXURY PRISON HE NEGOTIATED", 1200, eo(prog(t, b1 - 0.1, 0.3)), GOLD2, 54, 900)

def sc_hunt(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("hunt", 1)
    pop_text(c, "THE SEARCH BLOC", CX, 400, ANTON, 120, GOLD2, prog(t, 0.05, 0.25), glow=18, glow_rgb=GOLD)
    for i in range(5): person(c, 220 + i * 160, 760, 60, (90, 100, 90), a * clamp((t - 0.3) * 3 - i * 0.3))
    pu = eo(prog(t, b1 - 0.1, 0.3))
    radar(c, CX, 1030, 190, pu, t)
    pill(c, "U.S. TRACKING TECHNOLOGY", 1250 - 20, pu, CREAM, 52, 760)

def sc_rule(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("rule", 1)
    phone(c, CX - 240, 800, 1.0, a, rot=-6, t=t)
    secs = lerp(0, 115, clamp((t - b1) / max(0.5, D - b1 - 0.6))) if t > b1 else 0
    timer(c, CX + 170, 760, secs, a * eo(prog(t, b1 - 0.2, 0.3)), 120)
    pop_text(c, "CALLS CAN BE TRACED", CX, 400, ANTON, 100, CREAM, prog(t, W_("rule", "traced.") - 0.3, 0.25))
    pm = prog(t, W_("rule", "moved.") - 0.2, 0.22)
    if pm > 0: stamp(c, CX, 1140, "THEN MOVE", RED, 120, -5, pm, sc=lerp(2, 1, eo(pm)))
    pu = prog(t, W_("rule", "Under") - 0.15, 0.25)
    pop_text(c, "UNDER 2 MINUTES", CX + 170, 900, BEBAS, 60, GOLD2, pu)

def sc_hunter(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("hunter", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        id_card(c, CX, 760, 1.0, -3, a * (1 - out), "LT. HUGO MARTINEZ", "SIGNALS OFFICER", tag_="SEARCH BLOC")
        pill(c, "THE COMMANDER'S SON", 1170, eo(prog(t, W_("hunter", "son") - 0.2, 0.3)) * (1 - out), GOLD2, 60, 720)
    if out > 0:
        radar(c, CX, 780, 330, out, t * 1.4)
        for k in range(3):
            f = (t * 0.7 + k / 3) % 1
            c.drawCircle(CX, 780, 60 + 300 * f, P(C(GOLD2, out * (1 - f) * 0.7), stroke=4))
        pop_text(c, "RADIO DIRECTION FINDING", CX, 400, ANTON, 84, CREAM, prog(t, W_("hunter", "radio") - 0.15, 0.25))
        pop_text(c, "WAITING FOR THAT VOICE", CX, 1200, ANTON, 84, GOLD2, prog(t, W_("hunter", "waiting") - 0.15, 0.25), glow=16, glow_rgb=GOLD)

def sc_call(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("call", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        calendar(c, CX, 760, 1.1, a * (1 - out), "DEC 1", "1993")
        pop_text(c, "HE TURNED 44", CX, 1150, ANTON, 120, GOLD2, prog(t, W_("call", "44.") - 0.2, 0.25) * (1 - out), glow=18, glow_rgb=GOLD)
    if out > 0:
        phone(c, CX - 240, 800, 1.1, out, rot=-6, t=t, ring=0.4)
        secs = lerp(60, 170, clamp((t - b1) / max(0.5, D - b1 - 0.3)))
        timer(c, CX + 170, 780, secs, out, 130)
        pop_text(c, "HE CALLED HIS FAMILY", CX, 400, ANTON, 96, CREAM, prog(t, b1 + 0.1, 0.25))
        pl = prog(t, W_("call", "longer") - 0.2, 0.22)
        if pl > 0: stamp(c, CX, 1150, "LONGER THAN USUAL", RED, 92, -4, pl, sc=lerp(2, 1, eo(pl)))

def sc_locate(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("locate", 1)
    f = clamp(t / max(0.5, D - 0.5))
    city_grid(c, a, t, focus=eio(f))
    pop_text(c, "LOS OLIVOS, MEDELLIN", CX, 380, ANTON, 92, CREAM, prog(t, W_("locate", "Los") - 0.2, 0.25))
    rows = [("ONE BLOCK", W_("locate", "block.") - 0.2, GOLD2), ("ONE HOUSE", W_("locate", "house.") - 0.2, RED)]
    seq_rows(c, t, rows, 1250 - 40, 100)
    ph = eo(prog(t, W_("locate", "house.") - 0.3, 0.3))
    pin(c, CX + 120, 800, 0.8, ph, RED)

def sc_end(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("end", 1)
    for i in range(5):
        farm_x = 150 + i * 195
        c.drawRect(skia.Rect(farm_x - 80, 860, farm_x + 80, 1060), P(C((90, 80, 70) if i != 2 else (130, 100, 70), a)))
        r = skia.Path(); r.moveTo(farm_x - 95, 860); r.lineTo(farm_x, 780); r.lineTo(farm_x + 95, 860); r.close(); c.drawPath(r, P(C((60, 50, 44), a)))
    g = P(C(RED, 0.25 * a * (0.5 + 0.5 * math.sin(t * 12)))); c.drawRect(skia.Rect(0, 330, W, 1240), g)
    pop_text(c, "SURROUNDED", CX, 420, ANTON, 130, CREAM, prog(t, 0.05, 0.25))
    pd = prog(t, W_("end", "over.") - 0.2, 0.22)
    if pd > 0: stamp(c, CX, 1150, "MANHUNT OVER", RED, 110, -5, pd, sc=lerp(2, 1, eo(pd)), sub="DEC. 2, 1993")

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("twist", 1)
    photo_card(c, PH["mug2"], CX, 740, 600, 620, t / D, a, 1.0, 1.1, focus=(0.5, 0.35), credit=CR, dim=0.4 * eo(prog(t, b1 - 0.2, 0.3)))
    pop_text(c, "ONE OF THE RICHEST", CX, 360, ANTON, 104, CREAM, prog(t, 0.05, 0.25))
    pb = prog(t, b1 - 0.05, 0.25)
    if pb > 0:
        phone(c, CX, 760, 1.0 * lerp(1.5, 1, back(eo(pb))), eo(pb), rot=-6, t=t, ring=0.5)
        pop_text(c, "BROUGHT DOWN BY A PHONE CALL", CX, 1180, ANTON, 76, GOLD2, pb, glow=16, glow_rgb=GOLD)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    bars(c, a * 0.8, y0=600, y1=1100)
    pw = prog(t, W_("cta", "wood.") - 0.4, 0.3)
    pistol(c, CX, 850, 1.3 * lerp(1.4, 1, back(eo(pw))), eo(pw), rot=-8)
    pop_text(c, "AMERICA'S MOST FAMOUS BANK ROBBER", CX, 520, ANTON, 64, CREAM, prog(t, W_("cta", "famous") - 0.2, 0.25))
    if pw > 0: stamp(c, CX, 1110, "A GUN MADE OF WOOD", RED, 92, -4, pw, sc=lerp(2, 1, eo(pw)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    phone(c, CX - 230, 800, 1.1, 1.0, rot=-8, t=t, ring=0.6)
    timer(c, CX + 170, 820, 167, 1.0, 130)
    pop_text(c, "BROUGHT DOWN BY A PHONE CALL", CX, 400, ANTON, 76, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "BECAUSE...", CX, 1170, ANTON, 120, GOLD2, prog(t, W_("loopend", "Because") - 0.1, 0.25), glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, escape=sc_escape, hunt=sc_hunt, rule=sc_rule, hunter=sc_hunter, call=sc_call, locate=sc_locate,
              end=sc_end, twist=sc_twist, cta=sc_cta, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"end", "locate"}
_IMP = [("hook", "long.", -0.2, 0.4), ("escape", "walked", -0.15, 0.35), ("hunt", "United", -0.1, 0.3),
        ("rule", "moved.", -0.2, 0.35), ("rehook", "listening.", -0.2, 0.3), ("hunter", "voice.", -0.2, 0.3),
        ("call", "longer", -0.2, 0.4), ("locate", "house.", -0.2, 0.4), ("end", "over.", -0.2, 0.4),
        ("twist", "Brought", -0.05, 0.35), ("cta", "wood.", -0.3, 0.3), ("loopend", "Brought", -0.05, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = []
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
