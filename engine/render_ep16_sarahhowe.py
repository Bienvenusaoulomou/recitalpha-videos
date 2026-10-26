import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep16")
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

PH = dict(globe=load_photo("howe_01.jpg"))
CR_G = "THE BOSTON WEEKLY GLOBE, 1880 · PUBLIC DOMAIN"

def crystal_ball(c, x, y, r, a, t=0):
    if a <= 0: return
    g = P(C((150, 120, 255), a * 0.35)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.5))
    c.drawCircle(x, y, r * 1.2, g)
    sh = skia.Paint(); sh.setShader(skia.GradientShader.MakeRadial(skia.Point(x - r * 0.3, y - r * 0.3), r * 1.3,
                    [C((220, 210, 255), a), C((90, 60, 160), a), C((30, 20, 60), a)], [0.0, 0.55, 1.0]))
    c.drawCircle(x, y, r, sh)
    for k in range(3):
        ang = t * 1.5 + k * 2.1
        c.drawCircle(x + r * 0.45 * math.cos(ang), y + r * 0.3 * math.sin(ang), r * 0.12, P(C((255, 240, 200), a * 0.6)))
    base = skia.Path(); base.moveTo(x - r * 0.7, y + r * 1.25); base.lineTo(x - r * 0.45, y + r * 0.85); base.lineTo(x + r * 0.45, y + r * 0.85); base.lineTo(x + r * 0.7, y + r * 1.25); base.close()
    c.drawPath(base, P(C((120, 84, 40), a))); c.drawPath(base, P(C(GOLD, a), stroke=4))

def woman(c, x, y, r, rgb, a):
    if a <= 0: return
    c.drawCircle(x, y - r * 1.1, r * 0.6, P(C(rgb, a)))
    d = skia.Path(); d.moveTo(x - r * 0.35, y - r * 0.5); d.lineTo(x + r * 0.35, y - r * 0.5); d.lineTo(x + r * 0.9, y + r * 1.1); d.lineTo(x - r * 0.9, y + r * 1.1); d.close()
    c.drawPath(d, P(C(rgb, a)))

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        crystal_ball(c, CX, 760, 230, 1 - out, t)
        text(c, "A FORTUNE TELLER", CX, 380, ANTON, 110, CREAM, 1 - out)
        text(c, "OPENED A BANK FOR WOMEN", CX, 1200, ANTON, 78, GOLD2, 1 - out, glow=16, glow_rgb=GOLD)
    if out > 0:
        k = eo(prog(t, b1, 0.6))
        text(c, "%d%%" % max(1, round(8 * k)), CX, 860, ANTON, 380, GOLD2, out, glow=36, glow_rgb=GOLD)
        text(c, "INTEREST", CX, 400, ANTON, 120, CREAM, out)
        pm = prog(t, W_("hook", "month.") - 0.2, 0.22)
        if pm > 0: stamp(c, CX, 1110, "PER MONTH", RED, 130, -5, pm, sc=lerp(2.2, 1, eo(pm)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("who", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    pop_text(c, "BOSTON, 1879", CX, 380, ANTON, 110, CREAM, prog(t, 0.05, 0.25))
    if out < 1:
        id_card(c, CX, 760, 1.0, -3, a * (1 - out), "SARAH HOWE", "FORTUNE TELLER", tag_="THE BANKER")
    if out > 0:
        building(c, CX, 1130, 0.9, out, "LADIES' DEPOSIT", cols=6)
        pop_text(c, "THE LADIES' DEPOSIT COMPANY", CX, 560, ANTON, 76, GOLD2, prog(t, b1 - 0.05, 0.25), glow=16, glow_rgb=GOLD)

def sc_rules(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("rules", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    text(c, "THE RULES", CX, 380, ANTON, 120, CREAM, a)
    if out < 1:
        woman(c, CX, 820, 120, CREAM, a * (1 - out))
        rows = [("SINGLE WOMEN ONLY", W_("rules", "single") - 0.1, GOLD2), ("NOT RICH", W_("rules", "rich.") - 0.2, RED)]
        seq_rows(c, t, rows, 1150, 96)
    if out > 0:
        k = eo(prog(t, b1, 0.8))
        y = 820
        c.drawRect(skia.Rect(160, y - 14, 920, y + 14), P(C((80, 72, 60), out)))
        c.drawRect(skia.Rect(160, y - 14, lerp(160, 920, k), y + 14), P(C(GOLD2, out)))
        counter(c, 200, 200, y - 70, 100, CREAM, out, suffix="")
        counter(c, 1000 * k, 880, y - 70, 100, GOLD2, out * eo(prog(t, W_("rules", "$1,000.") - 0.3, 0.3)))
        pop_text(c, "MIN", 200, y + 90, BEBAS, 56, MUTED, prog(t, b1, 0.25)); pop_text(c, "MAX", 880, y + 90, BEBAS, 56, MUTED, prog(t, W_("rules", "$1,000.") - 0.3, 0.25))

def sc_math(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("math", 1)
    coin(c, CX, 520, 120, a, "$1,000", 50)
    n = int(clamp((t - W_("math", "$80") + 0.3) / 1.8) * 12)
    for i in range(12):
        x = 140 + i * 72
        h = 30 + 18 * i if i < n else 0
        if h: c.drawRect(skia.Rect(x, 1060 - h, x + 52, 1060), P(C(GOLD2, a)))
    counter(c, 80 * n, CX, 790, 120, GOLD2, a * eo(prog(t, W_("math", "$80") - 0.3, 0.3)), prefix="+$", suffix="", glow=16)
    text(c, "EVERY MONTH", CX, 1130, BEBAS, 60, CREAM, a, spacing=8)
    pd = prog(t, b1 - 0.05, 0.25)
    if pd > 0:
        c.drawRect(skia.Rect(0, 620, W, 1180), P(C(BG, 0.75 * eo(pd))))
        stamp(c, CX, 900, "~96% A YEAR", RED, 130, -6, pd, sc=lerp(2.2, 1, eo(pd)))

def sc_ponzi(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("ponzi", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        for i in range(3): woman(c, 220, 640 + i * 200, 50, MUTED, a)
        for i in range(3): woman(c, 860, 640 + i * 200, 50, GOLD2, a)
        text(c, "OLD", 220, 1260, BEBAS, 60, MUTED, a, spacing=6); text(c, "NEW", 860, 1260, BEBAS, 60, GOLD2, a, spacing=6)
        f = (t * 0.8) % 1
        for i in range(3):
            bills(c, lerp(760, 320, eio(f)), 640 + i * 200, a, 1)
        pn = prog(t, W_("ponzi", "no") - 0.1, 0.22)
        if pn > 0: stamp(c, CX, 420, "NO INVESTMENTS", RED, 92, -4, pn, sc=lerp(2, 1, eo(pn)))
        c.restore(); c.restore()
    if out > 0:
        calendar(c, CX - 230, 760, 0.8, out, "1879", "HOWE")
        calendar(c, CX + 230, 760, 0.8, eo(prog(t, W_("ponzi", "Ponzi.") - 0.4, 0.3)), "1920", "PONZI")
        pop_text(c, "40 YEARS BEFORE PONZI", CX, 1150, ANTON, 92, GOLD2, prog(t, b1, 0.25), glow=18, glow_rgb=GOLD)

def sc_growth(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("growth", 1)
    pop_text(c, "NO ADS", CX, 400, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
    pop_text(c, "JUST WORD OF MOUTH", CX, 520, BEBAS, 70, GOLD2, prog(t, W_("growth", "word") - 0.15, 0.25))
    k = clamp((t - b1) / max(0.6, D - b1 - 0.5))
    for i in range(int(k * 40)):
        woman(c, 150 + (i % 10) * 87, 700 + (i // 10) * 120, 26, GOLD2 if i % 5 == 0 else CREAM, a)
    counter(c, 1200 * eo(k), CX, 1230, 110, GOLD2, a * eo(prog(t, b1, 0.3)), prefix="~", suffix=" WOMEN", glow=16)

def sc_expose(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("expose", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        news(c, CX, 760, 1.2 * lerp(0.7, 1, back(a)), -3, a * (1 - out), "BOSTON", "\"A MYSTERIOUS BANK\"", "SEPTEMBER 1880")
        pop_text(c, "THE DAILY ADVERTISER", CX, 360, ANTON, 96, CREAM, prog(t, W_("expose", "Boston") - 0.1, 0.25) * (1 - out))
        ps = prog(t, W_("expose", "swindle.") - 0.2, 0.22)
        if ps > 0: stamp(c, CX, 1140, "SWINDLE", RED, 140, -6, ps * (1 - out), sc=lerp(2.2, 1, eo(ps)))
    if out > 0:
        photo_card(c, PH["globe"], CX, 830, 480, 720, (t - b1) / (D - b1), out, 1.0, 1.12, focus=(0.5, 0.25), credit=CR_G)
        rows = [("PANIC", W_("expose", "Panic.") - 0.1, RED), ("A RUN ON THE BANK", W_("expose", "run") - 0.2, CREAM), ("OVER", W_("expose", "over.") - 0.2, GOLD2)]
        seq_rows(c, t, rows, 390, 96)

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3))
    bars(c, a, y0=330, y1=1240)
    pt = prog(t, W_("verdict", "3") - 0.15, 0.25)
    if pt > 0: stamp(c, CX, 760, "3 YEARS", RED, 170, -6, pt, sc=lerp(2.2, 1, eo(pt)), sub="IN PRISON")

def sc_again(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("again", 1)
    building(c, CX, 1050, 0.85, a, "WOMAN'S BANK", cols=6)
    pop_text(c, "SHE DID IT AGAIN", CX, 390, ANTON, 120, GOLD2, prog(t, W_("again", "opened") - 0.15, 0.25), glow=18, glow_rgb=GOLD)
    pp = prog(t, W_("again", "7%") - 0.2, 0.25)
    pop_text(c, "7% A MONTH", CX, 560, ANTON, 104, CREAM, pp)
    pv = prog(t, W_("again", "disappeared") - 0.15, 0.22)
    if pv > 0:
        c.drawRect(skia.Rect(0, 330, W, 1240), P(C(BG, 0.5 * eo(pv))))
        stamp(c, CX, 860, "VANISHED", RED, 160, -8, pv, sc=lerp(2.2, 1, eo(pv)), sub="WITH THE MONEY")

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    pw = prog(t, W_("cta", "wanted") - 0.2, 0.25)
    pop_text(c, "THE MOST WANTED MAN", CX, 540, ANTON, 96, CREAM, pw)
    phone(c, CX - 220, 900, 1.0, a, rot=-8, t=t, ring=prog(t, W_("cta", "phone") - 0.3, 0.2))
    tower_radio(c, CX + 230, 1100, 1.0, a, t)
    pl = prog(t, W_("cta", "long.") - 0.3, 0.22)
    if pl > 0: stamp(c, CX, 1120, "ONE CALL TOO LONG", RED, 92, -4, pl, sc=lerp(2, 1, eo(pl)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    crystal_ball(c, CX, 760, 230, 1.0, t)
    pop_text(c, "AND IT ALL STARTED", CX, 400, ANTON, 104, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "WHEN...", CX, 1200, ANTON, 120, GOLD2, prog(t, W_("loopend", "when") - 0.1, 0.25), glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, who=sc_who, rules=sc_rules, math=sc_math, ponzi=sc_ponzi, growth=sc_growth, expose=sc_expose,
              verdict=sc_verdict, again=sc_again, cta=sc_cta, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"expose", "verdict"}
_IMP = [("hook", "month.", -0.2, 0.4), ("who", "Ladies'", -0.1, 0.3), ("rules", "rich.", -0.2, 0.3),
        ("math", "Almost", -0.05, 0.35), ("rehook", "next", -0.1, 0.3), ("ponzi", "no", -0.1, 0.35),
        ("growth", "About", -0.05, 0.3), ("expose", "swindle.", -0.2, 0.4), ("expose", "Panic.", -0.1, 0.3),
        ("verdict", "3", -0.15, 0.4), ("again", "disappeared", -0.15, 0.4), ("cta", "long.", -0.3, 0.3),
        ("loopend", "And", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("math", "$80", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
