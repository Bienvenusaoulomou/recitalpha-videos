import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep11")
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

PH = dict(reis=load_photo("alves_01.png"), note=load_color("alves_02.png"), crowd=load_photo("alves_03.png"))
CR_N = "BANCO DE PORTUGAL · PUBLIC DOMAIN"
CR = "PHOTO: PUBLIC DOMAIN"

def sc_hook(c, t, D):
    b1 = beat("hook", 1)
    photo_card(c, PH["note"], CX, 730, 900, 528, t / D, 1.0, 1.0, 1.1, rot=-2, credit=CR_N)
    text(c, "200,000", CX, 400, ANTON, 170, GOLD2, 1.0, glow=26, glow_rgb=GOLD)
    text(c, "BANKNOTES", CX, 1110, ANTON, 120, CREAM, 1.0)
    pr = prog(t, b1 - 0.1, 0.22)
    if pr > 0: stamp(c, CX, 730, "REAL ONES", RED, 150, -8, pr, sc=lerp(2.2, 1, eo(pr)))

def sc_contract(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("contract", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["reis"], CX, 740, 560, 680, t / b1, a * (1 - out), 1.0, 1.12, focus=(0.5, 0.3), rot=-1.5, credit=CR)
        pop_text(c, "ALVES DOS REIS", CX, 360, ANTON, 110, CREAM, prog(t, W_("contract", "Artur") - 0.1, 0.25))
        pill(c, "LISBON, 1925", 1170, a * (1 - out), GOLD2, 60, 520)
    if out > 0:
        paper_doc(c, CX, 800, 0.95, -2, out, "BANCO DE PORTUGAL", "CONFIDENTIAL", "LOAN FOR ANGOLA")
        signature(c, CX + 120, 1010, prog(t, W_("contract", "signatures.") - 0.5, 0.8), out, "the Governor", 56)
        rows = [("FAKE SIGNATURES", W_("contract", "signatures.") - 0.2, RED), ("FAKE AUTHORIZATION", W_("contract", "authorization.") - 0.3, RED)]
        seq_rows(c, t, rows, 1170, 92)
        pop_text(c, "A SECRET LOAN", CX, 340, ANTON, 110, GOLD2, prog(t, W_("contract", "secret") - 0.1, 0.25), glow=18, glow_rgb=GOLD)

def sc_printer(c, t, D):
    a = eo(prog(t, 0, 0.3))
    press(c, CX, 800, 1.1, a, t)
    pop_text(c, "WATERLOW & SONS", CX, 400, ANTON, 110, CREAM, prog(t, W_("printer", "Waterlow") - 0.1, 0.25))
    text(c, "LONDON", CX, 500, BEBAS, 64, MUTED, eo(prog(t, W_("printer", "London,") - 0.2, 0.3)), spacing=10)
    pp = eo(prog(t, W_("printer", "printed") - 0.3, 0.3))
    pill(c, "PRINTED PORTUGAL'S REAL MONEY", 1170, pp, GOLD2, 58, 920)

def sc_notes(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("notes", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    n = int(clamp(t / 2.0) * 12)
    for i in range(n):
        banknote(c, CX + ((i * 37) % 120 - 60), 830 - i * 14, 0.8, a * (1 - out * 0.7), rot=(i * 13) % 14 - 7, value="500", sub="ESCUDOS", rgb=(196, 150, 150))
    if out < 1:
        k = eo(prog(t, 0, 1.4))
        counter(c, 200000 * k, CX, 420, 150, GOLD2, a * (1 - out), prefix="", suffix=" NOTES", glow=20)
        pm = prog(t, W_("notes", "100") - 0.15, 0.25)
        pop_text(c, "100,000,000 ESCUDOS", CX, 1170, ANTON, 92, CREAM, pm * (1 - out))
    if out > 0:
        c.drawRect(skia.Rect(0, 380, W, 1240), P(C(BG, 0.55 * out)))
        # 1% of the economy: 100 squares, one gold
        for i in range(100):
            x = 240 + (i % 10) * 66; y = 520 + (i // 10) * 66
            hi = (i == 99)
            c.drawRect(skia.Rect(x, y, x + 56, y + 56), P(C(GOLD2 if hi else (90, 82, 70), out * (1 if hi else 0.8))))
        g = P(C(GOLD2, 0.6 * out * (0.6 + 0.4 * math.sin(t * 6)))); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
        c.drawRect(skia.Rect(240 + 9 * 66, 520 + 9 * 66, 240 + 9 * 66 + 56, 520 + 9 * 66 + 56), g)
        pop_text(c, "~1% OF THE ECONOMY", CX, 420, ANTON, 104, GOLD2, prog(t, b1 - 0.05, 0.25), glow=20, glow_rgb=GOLD)
        text(c, "OF PORTUGAL", CX, 1260, BEBAS, 60, CREAM, out, spacing=8)

def sc_bank(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("bank", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        building(c, CX, 1130, 0.95, a, "HIS OWN BANK", cols=6)
        text(c, "BANK OF ANGOLA", CX, 420, ANTON, 104, CREAM, a)
        text(c, "& METROPOLE", CX, 530, ANTON, 90, GOLD2, a)
        c.restore(); c.restore()
    if out > 0:
        for i in range(5):
            d = eo(prog(t, b1 + 0.2 + i * 0.35, 0.3))
            ticket(c, CX + (i - 2) * 28, 780 - i * 26, 0.85, d * out, rot=(i - 2) * 3, head="SHARE", title="BANK OF PORTUGAL", sub="ONE SHARE")
        pop_text(c, "BUYING THE BANK", CX, 400, ANTON, 110, GOLD2, prog(t, W_("bank", "buying") - 0.15, 0.25), glow=18, glow_rgb=GOLD)
        pop_text(c, "OF PORTUGAL ITSELF", CX, 1150, ANTON, 92, CREAM, prog(t, W_("bank", "itself.") - 0.3, 0.25))
        text(c, "(REPORTEDLY)", CX, 1235, BEBAS, 46, MUTED, out, spacing=6)

def sc_caught(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("caught", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        photo_card(c, PH["crowd"], CX, 740, 940, 625, t / b1, a * (1 - out), 1.0, 1.15, credit="PHOTO: LISBON, DEC. 1925 · PUBLIC DOMAIN")
        pop_text(c, "DECEMBER 1925", CX, 370, ANTON, 110, CREAM, prog(t, 0.05, 0.25))
        pill(c, "CROWDS RUSH TO SWAP THEIR NOTES", 1170, eo(prog(t, W_("caught", "fell") - 0.2, 0.3)) * (1 - out), GOLD2, 54, 920)
    if out > 0:
        for i, (yy, rot) in enumerate(((620, -3), (980, 3))):
            d = eo(prog(t, b1 + i * 0.3, 0.3))
            c.save(); c.translate(CX, yy); c.rotate(rot); c.translate(-CX, -yy)
            photo_card(c, PH["note"], CX, yy, 700, 410, 0, d * out, 1.0, 1.0)
            c.restore()
        pf = eo(prog(t, W_("caught", "same") - 0.2, 0.3))
        for yy in (620, 980):
            c.drawRoundRect(skia.Rect(CX + 30, yy - 90, CX + 230, yy - 30), 10, 10, P(C(RED, pf), stroke=6))
        ps = prog(t, W_("caught", "serial") - 0.1, 0.25)
        if ps > 0: stamp(c, CX, 800, "SAME SERIAL NUMBER", RED, 84, -6, ps, sc=lerp(2, 1, eo(ps)))

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("verdict", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        bars(c, a * (1 - out), y0=330, y1=1240)
        pt = prog(t, W_("verdict", "20") - 0.15, 0.25)
        if pt > 0: stamp(c, CX, 760, "20 YEARS", RED, 160, -6, pt * (1 - out), sc=lerp(2.2, 1, eo(pt)), sub="IN PRISON")
    if out > 0:
        press(c, CX, 650, 0.7, out, t * 0.2)
        text(c, "THE PRINTER PAYS", CX, 400, ANTON, 104, CREAM, out)
        k = eo(prog(t, W_("verdict", "more") - 0.2, 1.2))
        counter(c, 610000 * k, CX, 1000, 150, GOLD2, out, prefix="£", suffix="+", glow=24)
        text(c, "TO THE BANK OF PORTUGAL", CX, 1110, BEBAS, 56, CREAM, eo(prog(t, W_("verdict", "Bank") - 0.2, 0.3)), spacing=6)

def sc_coup(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("coup", 1)
    pop_text(c, "A CRISIS OF TRUST", CX, 400, ANTON, 110, CREAM, prog(t, 0.05, 0.25))
    pc = prog(t, W_("coup", "coup") - 0.2, 0.25)
    if pc > 0: stamp(c, CX, 620, "MILITARY COUP · 1926", RED, 92, -4, pc * (1 - eo(prog(t, b1 - 0.2, 0.3)) * 0.6), sc=lerp(2, 1, eo(pc)))
    # timeline bar 1926 -> 1974
    k = eo(prog(t, b1, max(0.5, D - b1 - 0.6)))
    y = 960
    c.drawRect(skia.Rect(140, y - 10, 940, y + 10), P(C((80, 72, 60), a)))
    c.drawRect(skia.Rect(140, y - 10, lerp(140, 940, k), y + 10), P(C(RED, a)))
    text(c, "1926", 160, y + 80, ANTON, 60, CREAM, a, align="l")
    text(c, "1974", 920, y + 80, ANTON, 60, CREAM, eo(clamp(k * 3 - 2)), align="r")
    pop_text(c, "DICTATORSHIP · ~50 YEARS", CX, 1150, ANTON, 84, GOLD2, prog(t, W_("coup", "dictatorship") - 0.15, 0.25), glow=16, glow_rgb=GOLD)
    text(c, "MANY HISTORIANS LINK THE TWO", CX, 820, BEBAS, 48, MUTED, eo(prog(t, W_("coup", "historians") - 0.2, 0.3)), spacing=5)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    xr = eo(prog(t, W_("cta", "water.") - 0.6, 0.6))
    for i, x in enumerate((CX - 280, CX, CX + 280)):
        oil_tank(c, x, 1000, 0.62, a, level=0.9, water=0.95, t=t + i, label="SALAD OIL", xray=xr)
    k = eo(prog(t, W_("cta", "borrowed") - 0.1, 1.2))
    counter(c, 100000000 * k, CX, 560, 110, GOLD2, eo(prog(t, W_("cta", "borrowed") - 0.2, 0.3)), suffix="+", glow=18)
    pw = prog(t, W_("cta", "water.") - 0.1, 0.25)
    if pw > 0: stamp(c, CX, 1130, "FULL OF WATER", RED, 96, -4, pw, sc=lerp(2, 1, eo(pw)))
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1235)

def sc_loopend(c, t, D):
    paper_doc(c, CX, 760, 1.0, -2, 1.0, "BANCO DE PORTUGAL", "CONFIDENTIAL", "LOAN FOR ANGOLA")
    pf = prog(t, W_("loopend", "forged") - 0.1, 0.22)
    if pf > 0: stamp(c, CX, 760, "FORGED", RED, 150, -10, pf, sc=lerp(2.2, 1, eo(pf)))
    pop_text(c, "20 YEARS IN PRISON", CX, 400, ANTON, 100, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, "BECAUSE...", CX, 1170, ANTON, 110, GOLD2, prog(t, beat("loopend", 1) - 0.1, 0.25), glow=18, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, contract=sc_contract, printer=sc_printer, notes=sc_notes, bank=sc_bank, caught=sc_caught,
              verdict=sc_verdict, coup=sc_coup, cta=sc_cta, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"caught", "verdict"}
_IMP = [("hook", "Real", -0.1, 0.4), ("contract", "signatures.", -0.2, 0.3), ("printer", "Waterlow", -0.1, 0.3),
        ("rehook", "yes.", -0.1, 0.35), ("notes", "Almost", -0.05, 0.3), ("bank", "buying", -0.15, 0.3),
        ("caught", "serial", -0.1, 0.4), ("verdict", "20", -0.15, 0.4), ("verdict", "more", -0.2, 0.3),
        ("coup", "coup", -0.2, 0.35), ("cta", "water.", -0.1, 0.35), ("loopend", "forged", -0.1, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("notes", "200,000", 0.0)] if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
