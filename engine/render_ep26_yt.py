import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep26")
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

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        building(c, CX, 1180, 0.8, 1 - out, "BANK", cols=6)
        counter(c, 10000000, CX, 560, 150 * lerp(1.15, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1 - out, prefix="$", glow=22)
        pg = prog(t, W_("hook", "gun.") - 0.3, 0.22)
        if pg > 0:
            pistol(c, CX, 760, 1.0, pg * (1 - out), rot=-10)
            stamp(c, CX, 760, "NO GUN", RED, 130, -8, pg * (1 - out), sc=lerp(2.2, 1, eo(pg)))
    if out > 0:
        desk_phone(c, CX, 800, 1.2 * lerp(0.7, 1, back(out)), out, rot=-6, t=t, ring=1.0)
        pop_text(c, "ONE PHONE CALL", CX, 1150, ANTON, 120, GOLD2, prog(t, W_("hook", "phone") - 0.2, 0.25), glow=20, glow_rgb=GOLD)

def sc_consultant(c, t, D):
    a = eo(prog(t, 0, 0.3))
    pop_text(c, "1978 · LOS ANGELES", CX, 400, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    id_card(c, CX, 720, 1.0, -3, eo(prog(t, W_("consultant", "Stanley") - 0.3, 0.35)), "STANLEY RIFKIN", "COMPUTER CONSULTANT", tag_="CONTRACTOR")
    building(c, CX, 1220, 0.55, eo(prog(t, W_("consultant", "Security") - 0.2, 0.35)), "SECURITY PACIFIC BANK", cols=7)

def sc_code(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("code", 1)
    pop_text(c, "THE WIRE TRANSFER ROOM", CX, 400, ANTON, 90, CREAM, prog(t, 0.0, 0.25))
    code_panel(c, CX, 720, a, code="• • • • •" if t < W_("code", "code,") - 0.2 else "SECRET", reveal=1.0, label="TODAY'S TRANSFER CODE")
    pw = prog(t, W_("code", "written") - 0.2, 0.22)
    if pw > 0: stamp(c, CX + 160, 860, "WRITTEN DOWN", RED, 70, 6, pw, sc=lerp(2, 1, eo(pw)))
    pe = eo(prog(t, b1 - 0.2, 0.35))
    if pe > 0:
        lightbulb_eye(c, CX, 1080, 70, pe, t)
        pop_text(c, "MEMORIZED", CX, 1240, ANTON, 90, GOLD2, prog(t, b1, 0.25), glow=16, glow_rgb=GOLD)

def sc_call(c, t, D):
    a = eo(prog(t, 0, 0.3))
    desk_phone(c, 280, 800, 0.8, a, rot=-8, t=t, ring=0.0)
    building(c, 790, 1000, 0.5, a, "BANK", cols=4)
    wires(c, 380, 760, 700, 820, clamp(t / 1.0), a, t)
    pop_text(c, "\"HI, I'M FROM THE BANK\"", CX, 400, ANTON, 92, CREAM, prog(t, W_("call", "pretending") - 0.2, 0.25))
    pc = prog(t, W_("call", "code.") - 0.4, 0.22)
    if pc > 0: stamp(c, CX, 1180, "+ THE CODE", GOLD2, 110, -5, pc, sc=lerp(2.2, 1, eo(pc)))

def sc_wire(c, t, D):
    a = eo(prog(t, 0, 0.3))
    building(c, 230, 1050, 0.45, a, "L.A.", cols=3)
    building(c, 850, 1050, 0.45, a, "ZURICH", cols=3)
    wires(c, 330, 850, 750, 850, 1.0, a, t * 1.6)
    k = eo(prog(t, 0.1, max(0.6, D - 0.6)))
    counter(c, 10200000 * k, CX, 600, 140, GOLD2, a, prefix="$", glow=22)
    pop_text(c, "→ SWITZERLAND", CX, 1220, ANTON, 104, CREAM, prog(t, W_("wire", "Switzerland.") - 0.3, 0.25))

def sc_diamonds(c, t, D):
    a = eo(prog(t, 0, 0.3))
    diamonds_field(c, t, a, n=22, seed=8)
    diamond(c, CX, 760, 1.6, a, t)
    k = eo(prog(t, W_("diamonds", "43,200") - 0.3, 0.9))
    counter(c, 43200 * k, CX, 450, 130, CREAM, a, prefix="", suffix=" CARATS", glow=16)
    pop_text(c, "SOVIET DIAMONDS", CX, 1060, ANTON, 96, GOLD2, prog(t, W_("diamonds", "Soviet") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    pill(c, "FOR $8.1 MILLION", 1200, eo(prog(t, W_("diamonds", "$8.1") - 0.2, 0.3)), CREAM, 64, 600)

def sc_caught(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("caught", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        desk_phone(c, CX, 780, 1.3, a * (1 - out), rot=6, t=t, ring=1.0)
        pop_text(c, "SOMEONE HE TRUSTED", CX, 400, ANTON, 100, CREAM, prog(t, W_("caught", "someone") - 0.2, 0.25) * (1 - out))
        pf = prog(t, W_("caught", "FBI.") - 0.3, 0.22)
        if pf > 0: stamp(c, CX, 1100, "TIPPED OFF THE FBI", RED, 96, -5, pf * (1 - out), sc=lerp(2.2, 1, eo(pf)))
    if out > 0:
        bars(c, out, y0=330, y1=1240)
        calendar(c, CX, 700, 0.8, out, "NOV 5", "1978")
        pa = prog(t, W_("caught", "arrested") - 0.2, 0.22)
        if pa > 0: stamp(c, CX, 1060, "ARRESTED", RED, 150, -6, pa, sc=lerp(2.2, 1, eo(pa)))

def sc_loopend(c, t, D):
    desk_phone(c, CX, 800, 1.2, 1.0, rot=-6, t=t, ring=0.6)
    pop_text(c, "AND THAT'S HOW...", CX, 400, ANTON, 112, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, consultant=sc_consultant, code=sc_code, call=sc_call, wire=sc_wire, diamonds=sc_diamonds,
              caught=sc_caught, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"caught"}
_IMP = [("hook", "gun.", -0.3, 0.4), ("code", "memorized", -0.2, 0.3), ("call", "code.", -0.4, 0.35),
        ("wire", "Switzerland.", -0.3, 0.3), ("rehook", "diamonds.", -0.2, 0.35), ("diamonds", "Soviet", -0.2, 0.3),
        ("caught", "FBI.", -0.3, 0.4), ("caught", "arrested", -0.2, 0.4), ("loopend", "And", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("wire", "$10.2", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
