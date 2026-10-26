import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep10")
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

PH = dict(king=load_photo("hoax_01.jpg"), ralston=load_photo("hoax_02.jpg"), tiffany=load_photo("hoax_03.jpg"),
          land=load_photo("hoax_05_c.jpg"), land2=load_photo("hoax_06_c.jpg"))
CR = "PHOTO: PUBLIC DOMAIN"
CR_OS = "PHOTO: T. H. O'SULLIVAN, 1872 · PUBLIC DOMAIN"
RUBY = (200, 40, 60)

def ruby(c, x, y, s, a, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(8 * math.sin(t))
    top = skia.Path(); top.moveTo(-120, -40); top.lineTo(-70, -100); top.lineTo(70, -100); top.lineTo(120, -40); top.close()
    bot = skia.Path(); bot.moveTo(-120, -40); bot.lineTo(120, -40); bot.lineTo(0, 120); bot.close()
    c.drawPath(top, P(C((230, 80, 100), a))); c.drawPath(bot, P(C(RUBY, a)))
    for pth in (top, bot): c.drawPath(pth, P(C((255, 200, 210), a), stroke=4))
    c.restore()

def ground(c, a, y0=620, y1=1060, holes=0, t=0, k=0.0):
    c.drawRect(skia.Rect(60, y0, W - 60, y1), P(C((92, 72, 50), a)))
    rng = random.Random(4)
    for i in range(40):
        c.drawCircle(rng.uniform(80, W - 80), rng.uniform(y0 + 10, y1 - 10), rng.uniform(3, 8), P(C((120, 98, 70), a)))
    for i in range(holes):
        x = 170 + (i % 5) * 185; y = y0 + 90 + (i // 5) * 150
        c.drawOval(skia.Rect(x - 50, y - 18, x + 50, y + 18), P(C((40, 30, 20), a)))
        dk = clamp(k * holes - i)
        if dk > 0:
            (ruby if i % 3 == 1 else diamond)(c, x, lerp(y - 260, y - 8, eo(dk)), 0.2, a * dk, t + i)

def pouch(c, x, y, s, a, pour=0.0, t=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-60, -150); p.quadTo(-220, -40, -170, 110); p.quadTo(0, 200, 170, 110); p.quadTo(220, -40, 60, -150); p.close()
    c.drawPath(p, P(C((120, 80, 46), a))); c.drawPath(p, P(C((70, 44, 24), a), stroke=6))
    c.drawLine(-80, -140, 80, -140, P(C(GOLD, a), stroke=10))
    c.restore()
    if pour > 0:
        rng = random.Random(2)
        for i in range(14):
            d = clamp(pour * 1.6 - i / 14)
            if d <= 0: continue
            gx = x + rng.uniform(-160, 160) * s; gy = lerp(y - 40 * s, y + 340 * s + rng.uniform(-40, 40), eo(d))
            (ruby if i % 4 == 2 else diamond)(c, gx, gy, 0.16, a * d, t + i)

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    text(c, "A FIELD OF", CX, 420, ANTON, 120, CREAM, 1.0)
    text(c, "DIAMONDS", CX, 560, ANTON, 150, GOLD2, 1.0, glow=26, glow_rgb=GOLD)
    k = clamp((t - b1 + 0.2) / 1.6)
    ground(c, 1.0, 640, 1080, holes=10, t=t, k=k if t > b1 - 0.2 else 0)
    if t < b1 - 0.2:
        for i in range(10):
            x = 170 + (i % 5) * 185; y = 730 + (i // 5) * 150
            diamond(c, x, y - 8, 0.2, 1.0, t + i)
    pb = prog(t, W_("hook", "bankers") - 0.15, 0.25)
    pill(c, "SOLD TO AMERICA'S RICHEST BANKERS", 1160, eo(pb) * (1 - eo(prog(t, b1 - 0.3, 0.2))), CREAM, 54, 940)
    pp = prog(t, W_("hook", "planted") - 0.15, 0.25)
    if pp > 0: stamp(c, CX, 1170, "PLANTED BY HAND", RED, 96, -4, pp, sc=lerp(2, 1, eo(pp)))

def sc_bag(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pa = eo(prog(t, W_("bag", "Philip") - 0.3, 0.3))
    id_card(c, CX - 230, 560, 0.6, -5, pa, "PHILIP ARNOLD", "PROSPECTOR", tag_="KENTUCKY")
    id_card(c, CX + 230, 600, 0.6, 4, eo(prog(t, W_("bag", "John") - 0.3, 0.3)), "JOHN SLACK", "PROSPECTOR", tag_="KENTUCKY")
    pf = eo(prog(t, W_("bag", "Francisco") - 0.3, 0.3))
    pill(c, "SAN FRANCISCO", 380, pf, GOLD2, 60, 600)
    pb = eo(prog(t, W_("bag", "bag") - 0.3, 0.3))
    pouch(c, CX, 930, 0.95, pb, pour=prog(t, W_("bag", "uncut") - 0.2, 1.2), t=t)
    pop_text(c, "UNCUT DIAMONDS", CX, 1200, ANTON, 96, CREAM, prog(t, W_("bag", "uncut") - 0.1, 0.25))

def sc_banker(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("banker", 1)
    photo_card(c, PH["ralston"], CX, 720, 560, 660, t / D, a, 1.0, 1.12, focus=(0.5, 0.35), rot=-1.5, credit=CR)
    pop_text(c, "WILLIAM RALSTON", CX, 360, ANTON, 104, CREAM, prog(t, W_("banker", "William") - 0.1, 0.25))
    pill(c, "FOUNDER, BANK OF CALIFORNIA", 1160, eo(prog(t, W_("banker", "founder") - 0.2, 0.3)) * (1 - eo(prog(t, b1 - 0.3, 0.2))), GOLD2, 56, 900)
    pw = prog(t, b1 - 0.05, 0.22)
    if pw > 0: stamp(c, CX, 1140, "HE WANTED IN", RED, 100, -5, pw, sc=lerp(2, 1, eo(pw)))

def sc_tiffany(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("tiffany", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    photo_card(c, PH["tiffany"], CX, 720, 560, 660, t / D, a, 1.0, 1.12, focus=(0.5, 0.3), rot=1.5, credit=CR, dim=0.55 * out)
    pop_text(c, "CHARLES LEWIS TIFFANY", CX, 360, ANTON, 90, CREAM, prog(t, W_("tiffany", "Charles") - 0.1, 0.25))
    if out > 0:
        k = eo(prog(t, W_("tiffany", "about") - 0.1, 1.0))
        c.drawRect(skia.Rect(0, 560, W, 860), P(C(BG, 0.6 * out)))
        counter(c, 150000 * k, CX, 760, 170, GOLD2, out, glow=26)
        pt = eo(prog(t, W_("tiffany", "tenth") - 0.3, 0.3))
        pill(c, "FOR JUST 1/10 OF THE STONES", 1160, pt, CREAM, 58, 900)

def sc_london(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("london", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        text(c, "LONDON", CX, 430, ANTON, 150, CREAM, a)
        pouch(c, CX, 800, 0.8, a, t=t)
        tag(c, CX + 210, 690, "CHEAP", eo(prog(t, W_("london", "cheap,") - 0.15, 0.25)), rot=10)
        k = eo(prog(t, W_("london", "about") - 0.1, 0.8))
        counter(c, 20000 * k, CX, 1150, 130, GOLD2, eo(prog(t, W_("london", "about") - 0.2, 0.2)), glow=18)
        c.restore(); c.restore()
    if out > 0:
        photo_card(c, PH["land"], CX, 740, 940, 660, (t - b1) / (D - b1), out, 1.0, 1.15, credit=CR_OS)
        rng = random.Random(9)
        for i in range(14):
            d = clamp((t - W_("london", "scattered") + 0.2) * 1.4 - i / 14)
            if d > 0:
                (ruby if i % 3 == 1 else diamond)(c, rng.uniform(150, 930), lerp(380, rng.uniform(700, 1020), eo(d)), 0.15, out * d, t + i)
        pop_text(c, "SCATTERED ON A REMOTE MESA", CX, 360, ANTON, 78, CREAM, prog(t, W_("london", "scattered") - 0.1, 0.25))

def sc_inspect(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("inspect", 1)
    photo_card(c, PH["land2"], CX, 720, 940, 640, t / D, a, 1.05, 1.18, credit=CR_OS, dim=0.35 * eo(prog(t, b1 - 0.2, 0.3)))
    pop_text(c, "JUNE 1872", CX, 360, ANTON, 110, CREAM, prog(t, 0.05, 0.25))
    pill(c, "A MINING EXPERT IS SENT", 1160, eo(prog(t, W_("inspect", "mining") - 0.2, 0.3)) * (1 - eo(prog(t, b1 - 0.3, 0.2))), GOLD2, 58, 820)
    if t > b1 - 0.2:
        rng = random.Random(3)
        for i in range(16):
            d = clamp((t - b1) * 3 - i / 4)
            if d > 0:
                gx, gy = rng.uniform(160, 920), rng.uniform(520, 960)
                (ruby if i % 2 else diamond)(c, gx, gy, 0.17 * back(clamp(d)), a, t + i)
        pop_text(c, "DIAMONDS & RUBIES", CX, 1150, ANTON, 104, GOLD2, prog(t, W_("inspect", "diamonds") - 0.1, 0.25), glow=20, glow_rgb=GOLD)

def sc_payout(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("payout", 1)
    for i in range(8):
        bills(c, 200 + (i % 4) * 230, 540 + (i // 4) * 130, a * clamp((t - 0.2) * 2 - i * 0.15), 3, rot=(i - 4) * 4)
    k = eo(prog(t, W_("payout", "more") - 0.1, 1.2))
    c.drawRect(skia.Rect(0, 760, W, 1000), P(C(BG, 0.65 * a)))
    counter(c, 600000 * k, CX, 930, 160, GOLD2, a, suffix="+", glow=26)
    pt = prog(t, b1 - 0.1, 0.25)
    if pt > 0: stamp(c, CX, 1150, "$10 MILLION+ TODAY", RED, 84, -4, pt, sc=lerp(2, 1, eo(pt)))
    text(c, "THE PAYOUT", CX, 400, ANTON, 110, CREAM, a)

def sc_king(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("king", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["king"], CX, 720, 560, 660, t / b1, a * (1 - out), 1.0, 1.12, focus=(0.5, 0.35), rot=-1.5, credit="PHOTO: USGS · PUBLIC DOMAIN")
        pop_text(c, "CLARENCE KING", CX, 360, ANTON, 110, CREAM, prog(t, W_("king", "Clarence") - 0.1, 0.25))
        pill(c, "GOVERNMENT GEOLOGIST", 1160, eo(prog(t, W_("king", "geologist,") - 0.2, 0.3)) * (1 - out), GOLD2, 58, 760)
    if out > 0:
        ps = eo(prog(t, b1, 0.4))
        pill(c, "ONLY NEAR THE SURFACE", 400, ps * (1 - eo(prog(t, W_("king", "about") - 0.3, 0.2))), CREAM, 60, 820)
        kk = clamp((t - W_("king", "about") + 0.1) / 1.0)
        for i in range(12):
            ruby(c, 170 + (i % 6) * 148, 560 + (i // 6) * 170, 0.32, out * clamp(kk * 12 - i), t + i)
        pd = eo(prog(t, W_("king", "diamond.") - 0.3, 0.3))
        diamond(c, CX, 1000, 0.6 * lerp(1.6, 1, pd), pd, t)
        text(c, "12 RUBIES", 260, 1240, ANTON, 70, (230, 90, 110), out * clamp(kk * 12 - 11))
        text(c, "1 DIAMOND", 820, 1240, ANTON, 70, (200, 230, 245), pd)

def sc_exposed(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("exposed", 1)
    pop_text(c, "NOVEMBER 1872", CX, 400, ANTON, 104, CREAM, prog(t, 0.05, 0.25))
    ground(c, a * (1 - eo(prog(t, b1 - 0.3, 0.3))), 560, 1000, holes=10, t=t, k=1.0)
    ps = prog(t, W_("exposed", "salted.") - 0.2, 0.22)
    if ps > 0: stamp(c, CX, 780, "SALTED", RED, 170, -8, ps * (1 - eo(prog(t, b1 - 0.3, 0.3))), sc=lerp(2.2, 1, eo(ps)))
    pn = eo(prog(t, b1 - 0.3, 0.35))
    news(c, CX, 790, 1.25 * lerp(0.7, 1, back(pn)), -3, pn, "EXTRA!", "THE GREAT DIAMOND HOAX", "THE FIELD WAS SALTED")

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    press(c, CX, 760, 0.95, a, t)
    for i in range(5):
        d = clamp((t - W_("cta", "print") + 0.3) * 1.5 - i * 0.3)
        if d > 0: banknote(c, CX + (i - 2) * 90, lerp(820, 930 + i * 10, eo(d)), 0.45, a * d, rot=(i - 2) * 6, value="500", sub="ESCUDOS")
    pp = prog(t, W_("cta", "millions.") - 0.2, 0.25)
    pop_text(c, "REAL MONEY", CX, 540, ANTON, 110, GOLD2, pp, glow=20, glow_rgb=GOLD)
    pf = prog(t, W_("cta", "fake") - 0.15, 0.25)
    if pf > 0: stamp(c, CX, 1100, "FAKE CONTRACTS", RED, 96, -4, pf, sc=lerp(2, 1, eo(pf)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1230)

def sc_loopend(c, t, D):
    ground(c, 1.0, 620, 1060, holes=10, t=t, k=1.0)
    pop_text(c, "WORTH ALMOST", CX, 420, ANTON, 120, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "NOTHING", CX, 560, ANTON, 150, RED, prog(t, W_("loopend", "nothing.") - 0.2, 0.25), glow=20, glow_rgb=RED)
    pop_text(c, "THAT'S HOW...", CX, 1170, ANTON, 104, GOLD2, prog(t, beat("loopend", 1) - 0.1, 0.25), glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, bag=sc_bag, banker=sc_banker, tiffany=sc_tiffany, london=sc_london, inspect=sc_inspect,
              payout=sc_payout, king=sc_king, exposed=sc_exposed, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"exposed"}
_IMP = [("hook", "planted", -0.15, 0.4), ("bag", "uncut", -0.1, 0.3), ("banker", "He", -0.05, 0.35),
        ("tiffany", "about", -0.1, 0.3), ("rehook", "London.", -0.1, 0.35), ("london", "about", -0.2, 0.3),
        ("inspect", "diamonds", -0.1, 0.3), ("payout", "More", -0.1, 0.35), ("king", "diamond.", -0.3, 0.3),
        ("exposed", "salted.", -0.2, 0.45), ("cta", "fake", -0.15, 0.3), ("loopend", "nothing.", -0.2, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("hook", "planted", 0.0), ("bag", "uncut", 0.0), ("inspect", "diamonds", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
