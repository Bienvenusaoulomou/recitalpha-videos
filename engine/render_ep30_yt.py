import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep30")
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

PH = dict(ds=load_photo("schultz_01.jpg"), wp=load_photo("schultz_poster.jpg"))
CR_S = "NYPD BOOKING PHOTO, 1930s · PUBLIC DOMAIN"
CR_W = "WANTED POSTER, 1934 · U.S. GOVERNMENT · PUBLIC DOMAIN"

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    mountains(c, 1.0, y=1240, t=t)
    safe(c, CX, 760, 0.9 * lerp(1.0, 1.06, t / max(1, D)), 1.0, open_=0.0)
    text(c, "A GANGSTER'S SAFE", CX, 390, ANTON, 112, CREAM, 1.0)
    pn = prog(t, b1 - 0.05, 0.22)
    if pn > 0: stamp(c, CX, 1080, "NEVER FOUND", RED, 130, -6, pn, sc=lerp(2.2, 1, eo(pn)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3))
    photo_card(c, PH["ds"], CX, 780, 520, 600, t / D, a, 1.0, 1.12, focus=(0.5, 0.4), rot=-1.5, credit=CR_S)
    pop_text(c, "DUTCH SCHULTZ", CX, 390, ANTON, 120, CREAM, prog(t, 0.0, 0.25))
    pill(c, "BOOTLEGGER · RACKETEER", 1190, eo(prog(t, W_("who", "bootlegger,") - 0.2, 0.3)), GOLD2, 58, 760)

def sc_trial(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("trial", 1)
    photo_card(c, PH["wp"], CX, 780, 640, 640, t / D, a, 1.0, 1.15, focus=(0.5, 0.15), credit=CR_W, dim=0.25)
    pop_text(c, "1935 · TAX EVASION", CX, 390, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pf = prog(t, W_("trial", "free.") - 0.3, 0.22)
    if pf > 0: stamp(c, CX, 1180, "WALKED FREE", GOLD2, 130, -6, pf, sc=lerp(2.2, 1, eo(pf)))

def sc_safe(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("safe", 1)
    pop_text(c, "THE LEGEND SAYS...", CX, 390, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    op = eo(prog(t, W_("safe", "filled") - 0.3, 0.6))
    safe(c, CX, 780, 0.9, a, open_=op)
    if op > 0.3:
        bills(c, CX - 120, 820, op, n=4, rot=-6); bills(c, CX + 110, 860, op, n=4, rot=8)
        ticket(c, CX, 690, 0.55, op, rot=-4, head="BOND", title="$1,000", sub="BEARER")
    k = eo(prog(t, W_("safe", "$7") - 0.3, 0.9))
    if k > 0: counter(c, 7000000 * k, CX, 1180, 150, GOLD2, k, prefix="~$", glow=24)

def sc_hide(c, t, D):
    a = eo(prog(t, 0, 0.3))
    mountains(c, a, y=1240, t=t)
    pop_text(c, "THE CATSKILL MOUNTAINS", CX, 400, ANTON, 96, CREAM, prog(t, W_("hide", "Catskill") - 0.2, 0.25))
    pp = eo(prog(t, W_("hide", "Phoenicia.") - 0.4, 0.35))
    pin(c, CX + 120, 820, 1.3 * lerp(0.6, 1, back(pp)), pp, RED, "PHOENICIA?")
    for i in range(2): person(c, 260 + i * 110, 1080, 42, CREAM, a)

def sc_secret(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("secret", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        safe(c, CX, 760, 0.9, a * (1 - out))
        pop_text(c, "?", CX, 790, ANTON, 260, GOLD2, prog(t, 0.2, 0.3) * (1 - out), glow=24, glow_rgb=GOLD)
        pop_text(c, "HE NEVER TOLD", CX, 400, ANTON, 112, CREAM, prog(t, 0.0, 0.25) * (1 - out))
    if out > 0:
        mountains(c, out, y=1240, t=t)
        for i in range(6):
            x = 140 + i * 160; y = 980 + 40 * math.sin(i * 1.7)
            person(c, x, y, 36, GOLD2 if i % 2 else CREAM, eo(prog(t, b1 + i * 0.1, 0.3)))
        pop_text(c, "~90 YEARS OF SEARCHING", CX, 420, ANTON, 96, GOLD2, prog(t, W_("secret", "90") - 0.3, 0.25), glow=18, glow_rgb=GOLD)

def sc_nothing(c, t, D):
    a = eo(prog(t, 0, 0.3))
    mountains(c, a, y=1240, t=t)
    pn = prog(t, 0.0, 0.22)
    if pn > 0: stamp(c, CX, 700, "NOTHING.", RED, 190, -6, pn, sc=lerp(2.2, 1, eo(pn)))
    pop_text(c, "NOT ONE DOLLAR", CX, 920, ANTON, 104, CREAM, prog(t, W_("nothing", "one") - 0.2, 0.25))

def sc_loopend(c, t, D):
    mountains(c, 1.0, y=1240, t=t)
    safe(c, CX, 760, 0.9, 1.0)
    pop_text(c, "WHICH MEANS...", CX, 390, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, who=sc_who, trial=sc_trial, safe=sc_safe, hide=sc_hide, secret=sc_secret, nothing=sc_nothing,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"rehook"}
_IMP = [("hook", "found", -0.2, 0.4), ("trial", "free.", -0.3, 0.35), ("safe", "$7", -0.2, 0.35),
        ("hide", "Phoenicia.", -0.4, 0.3), ("rehook", "killed.", -0.2, 0.4), ("secret", "never", -0.1, 0.3),
        ("nothing", "Nothing.", -0.1, 0.45), ("loopend", "Which", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("safe", "$7", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
