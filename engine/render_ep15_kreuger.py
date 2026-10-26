import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep15")
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

PH = dict(time=load_color("kreuger_time.jpg"), port=load_photo("kreuger_01.jpg", maxw=900), office=load_photo("kreuger_02.jpg"),
          share=load_color("kreuger_05.jpg"), news=load_photo("kreuger_news.jpg"), plane=load_photo("kreuger_03.jpg"))
CR = "PHOTO: PUBLIC DOMAIN"
CR_T = "TIME MAGAZINE, 1929 · PUBLIC DOMAIN"

def pie(c, x, y, r, frac, a, rgb=GOLD2):
    c.drawCircle(x, y, r, P(C((80, 72, 60), a)))
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, 360 * frac, False); p.close()
    c.drawPath(p, P(C(rgb, a)))
    c.drawCircle(x, y, r, P(C(GOLD, a), stroke=5))

def chart(c, x0, y0, w, h, k, a, crash_at=0.55):
    pts = []
    n = 40
    for i in range(int(n * k) + 1):
        f = i / n
        v = 0.3 + f / crash_at * 0.5 + 0.03 * math.sin(i * 1.7) if f < crash_at else 0.8 - (f - crash_at) / (1 - crash_at) * 0.7
        pts.append((x0 + f * w, y0 + h - v * h))
    if len(pts) > 1:
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        c.drawPath(p, P(C(RED if k > crash_at else GOLD2, a), stroke=10))
    c.drawLine(x0, y0 + h, x0 + w, y0 + h, P(C(MUTED, a), stroke=3))

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["time"], CX, 760, 560, 738, t / b1, 1.0 - out, 1.0, 1.06, rot=-2, credit=CR_T)
        text(c, "HE LENT MONEY", CX, 330, ANTON, 104, CREAM, 1.0 - out)
        text(c, "TO ENTIRE COUNTRIES", CX, 1210, ANTON, 96, GOLD2, 1 - out, glow=20, glow_rgb=GOLD)
    if out > 0:
        matchbox(c, CX - 170, 820, 1.05, out, rot=-6)
        match(c, CX + 250, 960, 1.5, out, t, lit=eo(prog(t, W_("hook", "matches.") - 0.2, 0.3)), rot=12)
        pop_text(c, "MATCHES.", CX, 400, ANTON, 140, GOLD2, prog(t, W_("hook", "matches.") - 0.1, 0.22), glow=22, glow_rgb=GOLD)
        pl = prog(t, W_("hook", "lies.") - 0.15, 0.22)
        if pl > 0: stamp(c, CX, 1160, "AND LIES", RED, 130, -5, pl, sc=lerp(2, 1, eo(pl)))

def sc_king(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("king", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["port"], CX, 760, 560, 700, t / b1, a * (1 - out), 1.0, 1.12, focus=(0.5, 0.3), rot=-1.5, credit=CR)
        pop_text(c, "IVAR KREUGER", CX, 340, ANTON, 120, CREAM, prog(t, 0.05, 0.25))
        pop_text(c, "THE MATCH KING", CX, 1200, ANTON, 100, GOLD2, prog(t, W_("king", "Match") - 0.1, 0.25) * (1 - out), glow=20, glow_rgb=GOLD)
    if out > 0:
        k = eo(prog(t, W_("king", "40%") - 0.3, 0.9))
        pie(c, CX, 780, 300, 0.4 * k, out)
        counter(c, 40 * k, CX, 820, 140, INK, out, prefix="", suffix="%")
        pop_text(c, "OF THE WORLD'S MATCHES", CX, 1210, ANTON, 84, CREAM, prog(t, W_("king", "world's") - 0.2, 0.25))
        text(c, "BY 1929", CX, 390, ANTON, 110, GOLD2, out)

def sc_deal(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("deal", 1)
    building(c, CX, 1000, 0.75, a, "GOVERNMENT", cols=6)
    pop_text(c, "BROKE AFTER WWI", CX, 380, ANTON, 104, CREAM, prog(t, W_("deal", "broke") - 0.15, 0.25))
    for i in range(4):
        d = clamp((t - W_("deal", "lend") + 0.2) * 1.3 - i * 0.2)
        if d > 0: bills(c, lerp(-100, CX - 150 + i * 100, eo(d)), 560 + i * 30, a * (1 - eo(prog(t, b1 - 0.3, 0.3)) * 0.6), 2, rot=(i - 2) * 6)
    pm = eo(prog(t, b1 - 0.1, 0.35))
    if pm > 0:
        matchbox(c, CX, 680, 0.9 * lerp(1.5, 1, back(pm)), pm, rot=4, label="MONOPOLY")
        pn = prog(t, W_("deal", "monopoly") - 0.1, 0.22)
        if pn > 0: stamp(c, CX, 1180, "MATCH MONOPOLY", GOLD2, 100, -4, pn, sc=lerp(2, 1, eo(pn)))

def sc_loans(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("loans", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        pop_text(c, "GERMANY ALONE", CX, 420, ANTON, 120, CREAM, prog(t, 0.05, 0.25) * (1 - out))
        k = eo(prog(t, W_("loans", "$125") - 0.2, 1.0))
        counter(c, 125e6 * k, CX, 800, 150, GOLD2, a * (1 - out), glow=24)
    if out > 0:
        for i in range(12):
            x = 160 + (i % 6) * 152; y = 560 + (i // 6) * 170
            building(c, x, y + 80, 0.18, out * clamp((t - b1) * 4 - i * 0.2), None, cols=4)
        k = eo(prog(t, b1 + 0.2, 1.2))
        c.drawRect(skia.Rect(0, 900, W, 1120), P(C(BG, 0.7 * out)))
        counter(c, 350e6 * k, CX, 1060, 140, GOLD2, out, suffix="+", glow=24)
        pop_text(c, "LENT TO GOVERNMENTS", CX, 1200, ANTON, 76, CREAM, prog(t, W_("loans", "lent") - 0.15, 0.25))

def sc_dividends(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("dividends", 1)
    photo_card(c, PH["share"], CX, 790, 520, 693, t / D, a, 1.0, 1.08, rot=2, credit="KREUGER & TOLL SHARE, 1927 · PUBLIC DOMAIN", dim=0.45 * eo(prog(t, b1 - 0.2, 0.3)))
    pd = prog(t, W_("dividends", "20%") - 0.2, 0.25)
    pop_text(c, "20%+ DIVIDENDS", CX, 380, ANTON, 120, GOLD2, pd, glow=22, glow_rgb=GOLD)
    pn = prog(t, b1 - 0.05, 0.25)
    if pn > 0:
        c.drawRect(skia.Rect(0, 1040, W, 1250), P(C(BG, 0.8 * eo(pn))))
        stamp(c, CX, 1150, "PAID WITH NEW MONEY", RED, 92, -4, pn, sc=lerp(2, 1, eo(pn)))

def sc_bonds(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("bonds", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    ticket(c, CX, 720, 1.05, a, rot=-3, head="REGNO D'ITALIA", title="GOVERNMENT BOND", sub="TREASURY · ROMA")
    if out < 1:
        pf = prog(t, W_("bonds", "forged") - 0.15, 0.22)
        if pf > 0: stamp(c, CX, 720, "FORGED", RED, 160, -10, pf * (1 - out), sc=lerp(2.2, 1, eo(pf)))
        k = eo(prog(t, W_("bonds", "$140") - 0.3, 1.0))
        counter(c, 140e6 * k, CX, 1140, 130, GOLD2, eo(prog(t, W_("bonds", "worth") - 0.3, 0.3)) * (1 - out), glow=20)
    if out > 0:
        c.drawRect(skia.Rect(0, 950, W, 1250), P(C(BG, 0.8 * out)))
        signature(c, CX, 1110, prog(t, b1, 0.8), out, "Ministro dele Finanze", 64)
        pc = eo(prog(t, W_("bonds", "misspelled") - 0.2, 0.3))
        c.drawOval(skia.Rect(CX - 120, 1040, CX + 30, 1130), P(C(RED, pc), stroke=7))
        pop_text(c, "MISSPELLED NAMES", CX, 380, ANTON, 110, RED, prog(t, W_("bonds", "misspelled") - 0.1, 0.25), glow=16, glow_rgb=RED)

def sc_crash(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("crash", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        chart(c, 140, 520, 800, 560, clamp(t / max(0.5, b1 - 0.3)), a * (1 - out))
        pop_text(c, "THE GREAT DEPRESSION", CX, 420, ANTON, 100, CREAM, prog(t, W_("crash", "Great") - 0.15, 0.25) * (1 - out))
    if out > 0:
        photo_card(c, PH["news"], CX, 810, 480, 640, (t - b1) / (D - b1), out, 1.0, 1.1, focus=(0.5, 0.3), credit=CR, dim=0.35)
        pop_text(c, "PARIS · MARCH 1932", CX, 340, ANTON, 104, CREAM, prog(t, b1 - 0.05, 0.25))
        pill(c, "FOUND DEAD IN HIS APARTMENT", 1200, eo(prog(t, W_("crash", "dead") - 0.2, 0.3)), CREAM, 56, 860)

def sc_audit(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("audit", 1)
    paper_doc(c, CX, 820, 0.9, -2, a, "KREUGER & TOLL", "AUDIT · 1932", "THE BOOKS")
    pop_text(c, "THE ACCOUNTANTS", CX, 380, ANTON, 110, CREAM, prog(t, 0.05, 0.25))
    pk = prog(t, b1 - 0.05, 0.25)
    if pk > 0:
        c.drawRect(skia.Rect(0, 560, W, 900), P(C(BG, 0.75 * eo(pk))))
        k = eo(prog(t, W_("audit", "$250") - 0.3, 1.0))
        counter(c, 250e6 * k, CX, 790, 150, RED, eo(pk), suffix="+", glow=20)
        pop_text(c, "INFLATED EARNINGS", CX, 1150, ANTON, 104, GOLD2, prog(t, W_("audit", "inflated") - 0.15, 0.25), glow=18, glow_rgb=GOLD)

def sc_legacy(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("legacy", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        coin(c, CX - 220, 760, 140, a * (1 - out), "$1", 90)
        text(c, "=", CX, 800, ANTON, 140, CREAM, a * (1 - out))
        coin(c, CX + 220, 760, 90 * eo(prog(t, W_("legacy", "30") - 0.3, 0.4)) + 1, a * (1 - out), "$0.30", 44)
        pop_text(c, "INVESTORS GOT BACK", CX, 420, ANTON, 104, CREAM, prog(t, 0.05, 0.25) * (1 - out))
    if out > 0:
        building(c, CX, 1100, 0.9, out, "NEW LAWS", cols=7)
        pop_text(c, "TO PROTECT INVESTORS", CX, 420, ANTON, 100, GOLD2, prog(t, W_("legacy", "protect") - 0.15, 0.25), glow=18, glow_rgb=GOLD)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    building(c, CX, 1000, 0.75, a, "LADIES ONLY", cols=5)
    pw = prog(t, W_("cta", "women,") - 0.2, 0.25)
    pop_text(c, "A BANK FOR WOMEN", CX, 540, ANTON, 104, CREAM, pw)
    pp = prog(t, W_("cta", "month.") - 0.3, 0.22)
    if pp > 0: stamp(c, CX, 1110, "8% PER MONTH", GOLD2, 110, -4, pp, sc=lerp(2, 1, eo(pp)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    photo_card(c, PH["time"], CX, 760, 560, 738, t / D, 1.0, 1.0, 1.06, rot=-2, credit=CR_T, dim=0.3)
    pn = prog(t, W_("loopend", "nothing.") - 0.2, 0.22)
    if pn > 0: stamp(c, CX, 760, "BUILT ON NOTHING", RED, 100, -8, pn, sc=lerp(2.2, 1, eo(pn)))
    pop_text(c, "AN EMPIRE OF MATCHES", CX, 380, ANTON, 90, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "BECAUSE...", CX, 1210, ANTON, 110, GOLD2, prog(t, beat("loopend", 1) - 0.1, 0.25), glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, king=sc_king, deal=sc_deal, loans=sc_loans, dividends=sc_dividends, bonds=sc_bonds,
              crash=sc_crash, audit=sc_audit, legacy=sc_legacy, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"bonds", "crash"}
_IMP = [("hook", "lies.", -0.15, 0.4), ("king", "40%", -0.3, 0.3), ("deal", "monopoly", -0.1, 0.35),
        ("loans", "$125", -0.2, 0.3), ("rehook", "problem.", -0.2, 0.3), ("dividends", "Often", -0.05, 0.35),
        ("bonds", "forged", -0.15, 0.4), ("bonds", "misspelled", -0.2, 0.3), ("crash", "March", -0.1, 0.3),
        ("audit", "$250", -0.3, 0.4), ("legacy", "30", -0.3, 0.3), ("cta", "month.", -0.3, 0.3),
        ("loopend", "nothing.", -0.2, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("loans", "$125", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
