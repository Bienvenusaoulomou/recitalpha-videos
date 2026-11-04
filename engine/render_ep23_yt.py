import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep23")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
from kit3 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999
def B(sid, i):
    try: return beat(sid, i)
    except Exception: return 999

PH = dict(h1=load_photo("hughes_01.jpg"), h2=load_photo("hughes_02.jpg"))
CR_1 = "HOWARD HUGHES, 1938 · ACME NEWSPICTURES · PUBLIC DOMAIN"
CR_2 = "HUGHES AT THE PRESS CLUB, 1938 · HARRIS & EWING / LOC · PUBLIC DOMAIN"

def bookcover(c, x, y, s, a, rot=0, fake=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-230, -330, 230, 330), 10, 10)
    sh = P(C((0, 0, 0), 0.55 * a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20)); c.drawRRect(r, sh)
    c.drawRRect(r, P(C((120, 30, 28), a))); c.drawRect(skia.Rect(-230, -330, -195, 330), P(C((80, 20, 18), a)))
    text(c, "THE", 15, -170, BEBAS, 60, GOLD2, a, spacing=6)
    text(c, "AUTOBIOGRAPHY", 15, -100, ANTON, 54, CREAM, a)
    text(c, "OF", 15, -40, BEBAS, 54, GOLD2, a, spacing=6)
    text(c, "HOWARD", 15, 50, ANTON, 92, CREAM, a)
    text(c, "HUGHES", 15, 150, ANTON, 92, CREAM, a)
    c.drawLine(-140, 210, 170, 210, P(C(GOLD2, a), stroke=4))
    c.restore()
    if fake > 0: stamp(c, x, y + 40 * s, "FAKE", RED, 170, -10, fake, sc=lerp(2.2, 1, eo(fake)))

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    bookcover(c, CX, 760, lerp(1.0, 1.05, t / max(1, D)), 1.0, -3)
    k = eo(prog(t, W_("hook", "$765,000.") - 0.4, 0.9))
    if k > 0: counter(c, 765000 * k, CX, 1200, 130, GOLD2, k, prefix="$", glow=22)
    pop_text(c, "SOLD FOR", CX, 400, BEBAS, 100, CREAM, prog(t, W_("hook", "sold") - 0.1, 0.25))
    pn = prog(t, b1 - 0.05, 0.22)
    if pn > 0: stamp(c, CX, 700, "THEY NEVER MET", RED, 110, -6, pn, sc=lerp(2.2, 1, eo(pn)))

def sc_hughes(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["h1"], CX, 800, 540, 720, t / D, a, 1.0, 1.12, focus=(0.5, 0.3), rot=1.5, credit=CR_1)
    pop_text(c, "HOWARD HUGHES", CX, 390, ANTON, 112, CREAM, prog(t, 0.0, 0.25))
    pill(c, "BILLIONAIRE · ALMOST NEVER SEEN", 1240, eo(prog(t, W_("hughes", "billionaire") - 0.2, 0.3)), GOLD2, 50, 860)

def sc_forge(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("forge", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        paper_doc(c, CX - 120, 780, 1.0, -6, a * (1 - out), "PERSONAL", "", "DEAR CLIFF,", lines=7)
        signature(c, CX - 40, 1010, prog(t, W_("forge", "handwriting,") - 0.6, 0.9), a * (1 - out), "Howard R. Hughes", 66)
        pop_text(c, "FORGED LETTERS", CX, 400, ANTON, 120, RED, prog(t, W_("forge", "forged") - 0.15, 0.25), glow=16)
    if out > 0:
        building(c, CX, 1180, 0.8, out, "McGRAW-HILL", cols=6)
        pop_text(c, "\"SECRET INTERVIEWS\"", CX, 400, ANTON, 104, GOLD2, prog(t, W_("forge", "secret") - 0.2, 0.25), glow=18, glow_rgb=GOLD)

def sc_checks(c, t, D):
    a = eo(prog(t, 0, 0.3))
    for i in range(3):
        p = eo(prog(t, 0.15 * i + 0.2, 0.35))
        check(c, CX + (i - 1) * 30, 600 + i * 170, 1.05, p, rot=(-4, 3, -2)[i], payee="H. R. HUGHES", amount="$ $ $", bank="McGRAW-HILL")
    pop_text(c, "McGRAW-HILL PAID", CX, 400, ANTON, 112, GOLD2, prog(t, 0.0, 0.25), glow=18, glow_rgb=GOLD)
    pill(c, "PAY TO: \"H. R. HUGHES\"", 1210, eo(prog(t, W_("checks", "H.") - 0.2, 0.3)), CREAM, 60, 700)

def sc_call(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["h2"], CX, 700, 760, 520, t / D, a, 1.0, 1.1, focus=(0.4, 0.4), credit=CR_2, dim=0.25)
    desk_phone(c, CX + 250, 1130, 0.65, a, rot=-8, t=t, ring=1.0 if t < W_("call", "reporters") else 0.0)
    pop_text(c, "JANUARY 7, 1972", CX, 390, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pn = prog(t, W_("call", "never") - 0.2, 0.22)
    if pn > 0: stamp(c, CX - 150, 1150, "\"NEVER MET HIM\"", RED, 100, -6, pn, sc=lerp(2.2, 1, eo(pn)))

def sc_bank(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("bank", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        building(c, CX, 1150, 0.75, a * (1 - out), "SWISS BANK", cols=5)
        pop_text(c, "WHO DEPOSITED THEM?", CX, 400, ANTON, 104, CREAM, prog(t, 0.05, 0.25) * (1 - out))
    if out > 0:
        id_card(c, CX, 740, 1.0, -3, out, "HELGA R. HUGHES", "ACCOUNT HOLDER", tag_="ALIAS")
        pw = prog(t, W_("bank", "wife,") - 0.3, 0.22)
        if pw > 0: stamp(c, CX, 1080, "IRVING'S WIFE", RED, 120, -5, pw, sc=lerp(2.2, 1, eo(pw)))

def sc_prison(c, t, D):
    a = eo(prog(t, 0, 0.3))
    bars(c, a, y0=330, y1=1240)
    pm = prog(t, W_("prison", "17") - 0.3, 0.22)
    if pm > 0: stamp(c, CX, 760, "17 MONTHS", RED, 170, -6, pm, sc=lerp(2.2, 1, eo(pm)))
    pop_text(c, "FEDERAL PRISON", CX, 1000, ANTON, 104, CREAM, prog(t, W_("prison", "federal") - 0.2, 0.25))

def sc_loopend(c, t, D):
    bookcover(c, CX, 760, 1.0, 1.0, -3)
    pop_text(c, "THAT'S HOW...", CX, 400, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, hughes=sc_hughes, forge=sc_forge, checks=sc_checks, call=sc_call, bank=sc_bank, prison=sc_prison,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"prison"}
_IMP = [("hook", "never", -0.1, 0.4), ("forge", "forged", -0.15, 0.3), ("checks", "paid.", -0.2, 0.3),
        ("rehook", "phone", -0.2, 0.3), ("call", "never", -0.2, 0.4), ("bank", "wife,", -0.3, 0.4),
        ("prison", "17", -0.3, 0.4), ("loopend", "That's", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$765,000.", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
