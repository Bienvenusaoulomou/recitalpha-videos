import os, sys, math
os.environ.setdefault("REC_ROOT", "/home/claude/ep07")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999

# ---------------- scenes ----------------
def sc_hook(c, t, D):
    text(c, "SHE FOOLED BANKERS", CX, 450, ANTON, 104, CREAM, 1.0)
    text(c, "OUT OF MILLIONS", CX, 570, ANTON, 120, GOLD2, 1.0, glow=22, glow_rgb=GOLD)
    for i in range(7):  # bills stack growing
        p = eo(prog(t, -0.35 + i * 0.1, 0.3)) if i > 2 else 1.0
        bills(c, CX - 300 + i * 100, 760 - (i % 2) * 20, p, n=3, rot=(i - 3) * 4)
    b1 = beat("hook", 1)
    pq = prog(t, b1 - 0.1, 0.3)
    if pq > 0:
        c.drawRoundRect(skia.Rect(150, 880, W - 150, 1150), 16, 16, P(C((236, 226, 204), eo(pq))))
        text(c, "ONE SIGNATURE", CX, 940, BEBAS, 48, (110, 95, 70), eo(pq), spacing=6)
        signature(c, CX, 1060, prog(t, W_("hook", "fake") - 0.2, 0.9), eo(pq))
    ps = prog(t, W_("hook", "signature.") - 0.05, 0.22)
    if ps > 0: stamp(c, CX + 230, 1120, "FAKE", RED, 90, -12, ps, sc=lerp(2, 1, eo(ps)))

def sc_mansion(c, t, D):
    a = eo(prog(t, 0, 0.3))
    mansion(c, CX, 1000, 1.05, a, t)
    text(c, "NEW YORK", CX, 400, BEBAS, 70, MUTED, a, spacing=10)
    pc = eo(prog(t, W_("mansion", "Andrew") - 0.2, 0.3))
    text(c, "ANDREW CARNEGIE", CX, 500, ANTON, 96, GOLD2, pc, glow=16, glow_rgb=GOLD)
    pr = prog(t, W_("mansion", "richest") - 0.2, 0.3)
    pill(c, "ONE OF THE RICHEST MEN ALIVE", 1150, eo(pr) * (1 - eo(prog(t, beat("mansion", 1) - 0.3, 0.2))), CREAM, 58, 900)
    pl = eo(prog(t, beat("mansion", 1) - 0.1, 0.6))
    if pl > 0:
        carriage(c, lerp(-200, 260, pl), 1120, 0.95, 1.0, t)
        pill(c, "A LAWYER WAITS OUTSIDE", 1210, prog(t, W_("mansion", "lawyer") - 0.1, 0.3), GOLD2, 58, 720)

def sc_drop(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("drop", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        person(c, CX - 160, 820, 70, CREAM, a)
        person(c, CX + 160, 830, 62, MUTED, eo(prog(t, W_("drop", "housekeeper.") - 0.4, 0.3)))
        text(c, "INSIDE...", CX, 450, ANTON, 110, CREAM, a)
        pill(c, "SHE ONLY TALKS TO THE HOUSEKEEPER", 1120, eo(prog(t, W_("drop", "chatted") - 0.2, 0.3)), GOLD2, 54, 980)
        c.restore(); c.restore()
    if out > 0:
        pf = eo(prog(t, W_("drop", "dropped") - 0.1, 0.8))
        y = lerp(560, 760, pf); rot = lerp(-25, -4, pf) + 3 * math.sin(t * 3) * (1 - pf)
        paper_doc(c, CX, y, 0.9, rot, out, "PROMISSORY NOTE", "NEW YORK", "", lines=4)
        k = eio(prog(t, W_("drop", "$2,000,000,") - 0.2, 1.0))
        if k > 0:
            c.save(); c.translate(CX, y); c.rotate(rot)
            counter(c, 2000000 * k, 0, -130, 92, INK, out)
            signature(c, 30, 230, prog(t, W_("drop", "signed") - 0.1, 0.9), out, size=56)
            c.restore()
        pa = prog(t, W_("drop", "Carnegie.") + 0.1, 0.25)
        if pa > 0: pop_text(c, "SIGNED: ANDREW CARNEGIE?", CX, 1210, ANTON, 70, GOLD2, pa, glow=14, glow_rgb=GOLD)

def sc_secret(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pw = prog(t, W_("secret", "Carnegie's") - 0.2, 0.3)
    pop_text(c, "\"I'M CARNEGIE'S", CX, 470, ANTON, 104, CREAM, pw)
    pop_text(c, "SECRET DAUGHTER\"", CX, 590, ANTON, 104, GOLD2, prog(t, W_("secret", "secret") - 0.1, 0.3), glow=22, glow_rgb=GOLD)
    if pw <= 0:
        text(c, "THEN SHE WHISPERED...", CX, 520, BEBAS, 80, MUTED, a, spacing=6)
    k1 = eio(prog(t, W_("secret", "$7") - 0.2, 0.9))
    if k1 > 0:
        counter(c, 7000000 * k1, CX, 830, 110, CREAM, clamp(k1 * 3))
        text(c, "MORE IN \"NOTES\"", CX, 900, BEBAS, 54, MUTED, clamp(k1 * 3), spacing=6)
    k2 = eio(prog(t, W_("secret", "$400") - 0.2, 1.2))
    if k2 > 0:
        c.drawRect(skia.Rect(0, 980, W, 1240), P(C(BG, 0.6 * clamp(k2 * 3))))
        counter(c, 400000000 * k2, CX, 1120, 130, GOLD2 if k2 >= 1 else CREAM, clamp(k2 * 3), glow=22 if k2 >= 1 else 0)
        text(c, "WHEN HE DIES (SHE CLAIMED)", CX, 1200, BEBAS, 50, CREAM, clamp(k2 * 3), spacing=4)

def sc_banks(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "OHIO BANKERS", CX, 420, ANTON, 110, CREAM, a)
    for i in range(3):
        p = eo(prog(t, 0.15 + i * 0.25, 0.35))
        building(c, 230 + i * 310, 900, 0.45, p, "BANK")
    for i in range(10):
        p = prog(t, 0.8 + i * 0.18, 0.9)
        if 0 < p < 1:
            x0 = 230 + (i % 3) * 310; x = lerp(x0, CX, eio(p)); y = lerp(820, 1080, eio(p)) - 120 * math.sin(math.pi * p)
            bills(c, x, y, 1 - p * 0.3, 1, rot=i * 20)
    person(c, CX, 1110, 50, GOLD2, eo(prog(t, 0.6, 0.3)))
    pq = prog(t, beat("banks", 1) - 0.1, 0.3)
    if pq > 0:
        c.drawRect(skia.Rect(0, 1000, W, 1240), P(C(BG, 0.65 * eo(pq))))
        pop_text(c, "WHO WOULD SAY NO?", CX, 1150, ANTON, 104, GOLD2, pq, glow=18, glow_rgb=GOLD)

def sc_loans(c, t, D):
    a = eo(prog(t, 0, 0.3))
    yrs = int(lerp(1897, 1904, eio(prog(t, 0.2, D - 1.0))))
    calendar(c, CX, 600, 1.0, a, str(yrs), "YEAR")
    k = eio(prog(t, W_("loans", "piled") - 0.3, 2.2))
    counter(c, 2000000 * k, CX, 980, 150, GOLD2 if k >= 1 else CREAM, a, glow=24 if k >= 1 else 0)
    text(c, "IN LOANS", CX, 1080, BEBAS, 70, CREAM, a, spacing=8)
    for i in range(int(k * 12)):
        bills(c, 140 + (i % 6) * 160, 1180 - (i // 6) * 26, 0.9, 1, rot=(i * 37) % 20 - 10)

def sc_newton(c, t, D):
    a = eo(prog(t, 0, 0.3))
    calendar(c, CX, 560, 0.9, a, "1904", "YEAR")
    pb = eo(prog(t, W_("newton", "Massachusetts") - 0.2, 0.3))
    pill(c, "A MASSACHUSETTS BANKER", 800, pb, CREAM, 58, 820)
    k = eio(prog(t, W_("newton", "$190,000.") - 0.2, 1.0))
    if k > 0: counter(c, 190000 * k, CX, 960, 140, CREAM, clamp(k * 3))
    pl = prog(t, W_("newton", "loan,") - 0.1, 0.25)
    if pl > 0 and k <= 0: pop_text(c, "LOAN CALLED IN", CX, 960, ANTON, 100, GOLD2, pl)
    pc = prog(t, beat("newton", 1) - 0.05, 0.22)
    if pc > 0: stamp(c, CX, 1150, "CAN'T PAY", RED, 110, -6, pc, sc=lerp(2, 1, eo(pc)))

def sc_oberlin(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "OBERLIN, OHIO", CX, 420, ANTON, 104, CREAM, a)
    building(c, CX, 960, 0.95, a, "CITIZENS' BANK")
    pr = prog(t, W_("oberlin", "run") - 0.3, 1.6)
    for i in range(14):
        p = clamp(pr * 1.4 - i * 0.03)
        if p > 0:
            x = lerp(-60 if i % 2 else W + 60, CX - 200 + (i % 7) * 66, eo(p))
            person(c, x, 1120 + (i // 7) * 60, 26, CREAM, 1.0)
    pc = prog(t, W_("oberlin", "close.") - 0.1, 0.22)
    if pc > 0: stamp(c, CX, 760, "CLOSED", RED, 140, -8, pc, sc=lerp(2.2, 1, eo(pc)))

def sc_carnegie(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("carnegie", 1)
    text(c, "SOMEONE ASKED", CX, 450, BEBAS, 84, MUTED, a, spacing=6)
    text(c, "ANDREW CARNEGIE", CX, 570, ANTON, 110, GOLD2, a, glow=18, glow_rgb=GOLD)
    q = eo(prog(t, 0.3, 0.4))
    text(c, "?", CX, 860, ANTON, 260, CREAM, q * (1 - eo(prog(t, b1 - 0.2, 0.2))))
    pn = prog(t, W_("carnegie", "never") - 0.15, 0.25)
    if pn > 0:
        pop_text(c, "\"NEVER HEARD", CX, 860, ANTON, 120, CREAM, pn)
        pop_text(c, "OF HER.\"", CX, 990, ANTON, 120, RED, prog(t, W_("carnegie", "her.") - 0.1, 0.25), glow=18, glow_rgb=RED)

def sc_arrest(c, t, D):
    a = eo(prog(t, 0, 0.3))
    b1 = beat("arrest", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        c.save(); layer_alpha(c, 1 - out)
        text(c, "CAUGHT IN NEW YORK", CX, 430, ANTON, 96, CREAM, a)
        pb = eo(prog(t, W_("arrest", "belt") - 0.3, 0.4))
        c.drawRoundRect(skia.Rect(140, 700, W - 140, 860), 30, 30, P(C((92, 70, 46), pb)))
        c.drawRoundRect(skia.Rect(140, 700, W - 140, 860), 30, 30, P(C(GOLD, pb), stroke=6))
        for i in range(6): bills(c, 240 + i * 120, 780, pb, 2, rot=(i - 3) * 4)
        text(c, "MONEY BELT", CX, 660, BEBAS, 64, GOLD2, pb, spacing=8)
        k = eio(prog(t, W_("arrest", "$100,000.") - 0.2, 0.9))
        if k > 0: counter(c, 100000 * k, CX, 1060, 150, GOLD2, clamp(k * 3), suffix="+", glow=18 if k >= 1 else 0)
        c.restore(); c.restore()
    if out > 0:
        bars(c, eo(prog(t, b1 - 0.1, 0.6)))
        pt = prog(t, W_("arrest", "10") - 0.15, 0.22)
        if pt > 0: stamp(c, CX, 720, "10+ YEARS", RED, 130, -6, pt, sc=lerp(2, 1, eo(pt)))
        pp = eo(prog(t, W_("arrest", "prison", 0) - 0.2, 0.3))
        pill(c, "DIED IN PRISON · 1907", 1050, pp, CREAM, 66, 760)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.3))
    text(c, "NEXT EPISODE", CX, 420, BEBAS, 70, MUTED, a, spacing=10)
    sea(c, 920, a, t)
    warship(c, CX, 880, 1.0, a, t)
    pn = prog(t, W_("cta", "medical") - 0.2, 0.25)
    pop_text(c, "NO MEDICAL DEGREE", CX, 560, ANTON, 96, CREAM, pn)
    pw = prog(t, W_("cta", "war.") - 0.1, 0.25)
    pop_text(c, "SURGERY IN A WAR", CX, 1090, ANTON, 96, GOLD2, pw, glow=18, glow_rgb=GOLD)
    if "Follow" in [x["w"] for x in E.WORDS if x["scene"] == "cta"]:
        follow_pill(c, W_("cta", "Follow") - 0.1, t, 1200)

def sc_loopend(c, t, D):
    l1, l2, _ = S.LOOPEND
    bars(c, eo(prog(t, 0.0, 0.5)))
    pop_text(c, l1, CX, 700, ANTON, 104, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, l2, CX, 900, ANTON, 150, GOLD2, prog(t, beat("loopend", 1) - 0.1, 0.25), glow=22, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, mansion=sc_mansion, drop=sc_drop, secret=sc_secret, banks=sc_banks, loans=sc_loans,
              newton=sc_newton, oberlin=sc_oberlin, carnegie=sc_carnegie, arrest=sc_arrest, cta=sc_cta, loopend=sc_loopend,
              rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"newton", "oberlin", "arrest"}
_IMP = [("hook", "signature.", -0.05, 0.35), ("drop", "dropped", -0.1, 0.3), ("secret", "$400", -0.2, 0.3),
        ("rehook", "But", -0.1, 0.3), ("newton", "couldn't", -0.05, 0.35), ("oberlin", "close.", -0.1, 0.35),
        ("carnegie", "never", -0.15, 0.35), ("arrest", "10", -0.15, 0.35), ("cta", "war.", -0.1, 0.3),
        ("loopend", "And", -0.1, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [x for x in [("loans", "$2", 1.6), ("drop", "$2,000,000,", 0.6)] if x[0] in SID]
E.set_hits(IMPACTS)
BR = "/home/claude/recitalpha-videos/archive/broll"
VAULT = "ARCHIVE FOOTAGE · PUBLIC DOMAIN"
if "banks" in SID: E.BROLL["banks"] = E.load_broll(f"{BR}/vault_cleveland_small.mp4", start=36, dur=6, alpha=0.75, credit=VAULT)
if "loans" in SID: E.BROLL["loans"] = E.load_broll(f"{BR}/vault_cleveland_small.mp4", start=18, dur=6, alpha=0.7, credit=VAULT)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
