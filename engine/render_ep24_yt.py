import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep24")
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

PH = dict(work=load_photo("hvm_02.jpg"), ver=load_photo("vermeer_01.jpg"))
IMG_VER = skia.Image.open(f"{E.ROOT}/img/vermeer_01.jpg")
CR_W = "VAN MEEGEREN AT WORK, 1945 · KOOS RAUCAMP / ANEFO · CC0"
CR_V = "REAL VERMEER: GIRL WITH A PEARL EARRING, c.1665 · PUBLIC DOMAIN"

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        frame(c, CX, 760, 460, 560, 1 - out, None, rot=-2, label="\"VERMEER\"", fake=prog(t, W_("hook", "fake,") - 0.2, 0.4))
        pop_text(c, "\"I PAINTED IT\"", CX, 400, ANTON, 120, CREAM, prog(t, 0.0, 0.22) * (1 - out), s0=1.3)
        pl = prog(t, W_("hook", "life.") - 0.3, 0.22)
        if pl > 0: stamp(c, CX, 1150, "TO SAVE HIS LIFE", RED, 100, -5, pl * (1 - out), sc=lerp(2.2, 1, eo(pl)))
    if out > 0:
        pop_text(c, "ITS OWNER:", CX, 560, BEBAS, 100, CREAM, out, s0=1.2)
        pg = prog(t, W_("hook", "Göring.") - 0.25, 0.22)
        if pg > 0: stamp(c, CX, 800, "HERMANN GÖRING", RED, 120, -4, pg, sc=lerp(2.2, 1, eo(pg)))

def sc_forger(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("forger", 1)
    photo_card(c, PH["work"], CX, 780, 760, 640, t / D, a, 1.0, 1.12, focus=(0.5, 0.45), credit=CR_W)
    pop_text(c, "HAN VAN MEEGEREN", CX, 390, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pill(c, "SPECIALTY: \"NEW\" VERMEERS", 1205, eo(prog(t, b1 - 0.1, 0.3)), GOLD2, 60, 840)

def sc_fooled(c, t, D):
    a = eo(prog(t, 0, 0.3))
    frame(c, CX, 760, 400, 500, a, IMG_VER, rot=2)
    text(c, CR_V, W - 60, 1110, BEBAS, 30, MUTED, a * 0.9, align="r", spacing=2)
    pop_text(c, "\"A LOST MASTERPIECE!\"", CX, 400, ANTON, 104, GOLD2, prog(t, W_("fooled", "lost") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    pf = prog(t, W_("fooled", "fortunes.") - 0.3, 0.3)
    if pf > 0:
        bills(c, 200, 1160, pf, n=5, rot=-10); bills(c, 880, 1160, pf, n=5, rot=10)
        pill(c, "BUYERS PAID FORTUNES", 1200, eo(pf), CREAM, 60, 640)

def sc_goering(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("goering", 1)
    frame(c, CX, 740, 380, 460, a, None, rot=-2, label="\"VERMEER\"")
    pop_text(c, "GÖRING'S COLLECTION", CX, 400, ANTON, 104, RED, prog(t, W_("goering", "Göring's") - 0.2, 0.25), glow=16)
    if t > b1 - 0.3:
        for i in range(6):
            p = eo(prog(t, b1 + i * 0.18, 0.35))
            frame(c, 140 + i * 160, 1075, 100, 120, p * 0.9, None, rot=(i % 2) * 6 - 3)
        pill(c, "PAID WITH OTHER PAINTINGS", 1240, eo(prog(t, W_("goering", "paintings.") - 0.4, 0.3)), GOLD2, 54, 820)

def sc_arrest(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("arrest", 1)
    calendar(c, CX, 560, 0.7, a, "1945", "ARRESTED")
    pop_text(c, "\"SOLD A NATIONAL TREASURE\"", CX, 840, ANTON, 84, CREAM, prog(t, W_("arrest", "national") - 0.2, 0.25))
    pop_text(c, "TO THE NAZIS", CX, 950, ANTON, 96, RED, prog(t, W_("arrest", "Nazis.") - 0.2, 0.25))
    pd = prog(t, W_("arrest", "death.") - 0.3, 0.22)
    if pd > 0: stamp(c, CX, 1150, "PENALTY: DEATH", RED, 92, -6, pd, sc=lerp(2.2, 1, eo(pd)))

def sc_proof(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("proof", 1)
    out = eo(prog(t, b1 - 0.3, 0.3))
    if out < 1:
        frame(c, CX, 780, 420, 520, a * (1 - out), None, rot=-2, label="\"VERMEER\"", fake=prog(t, W_("proof", "not") - 0.2, 0.5))
        pop_text(c, "\"I PAINTED IT.\"", CX, 400, ANTON, 120, GOLD2, prog(t, W_("proof", "painted") - 0.3, 0.25), glow=18, glow_rgb=GOLD)
    if out > 0:
        photo_card(c, PH["work"], CX, 760, 760, 620, (t - b1) / max(1, D - b1), out, 1.0, 1.1, focus=(0.5, 0.45), credit=CR_W)
        for i in range(6): person(c, 150 + i * 156, 1170, 40, CREAM if i % 2 else MUTED, out)
        pop_text(c, "IN FRONT OF WITNESSES", CX, 400, ANTON, 96, CREAM, prog(t, W_("proof", "witnesses.") - 0.4, 0.25))

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("verdict", 1)
    pf = prog(t, W_("verdict", "forgery.") - 0.4, 0.22)
    if pf > 0: stamp(c, CX, 640, "1 YEAR · FORGERY", GOLD2, 120, -5, pf, sc=lerp(2.2, 1, eo(pf)))
    pop_text(c, "THE VERDICT", CX, 420, ANTON, 104, CREAM, prog(t, 0.05, 0.25))
    calendar(c, CX, 960, 0.7, eo(prog(t, b1 - 0.1, 0.3)), "1947", "END OF THE STORY")

def sc_loopend(c, t, D):
    frame(c, CX, 760, 460, 560, 1.0, None, rot=-2, label="\"VERMEER\"")
    pop_text(c, "THAT'S WHY...", CX, 400, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, forger=sc_forger, fooled=sc_fooled, goering=sc_goering, arrest=sc_arrest, proof=sc_proof,
              verdict=sc_verdict, loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"arrest"}
_IMP = [("hook", "Göring.", -0.25, 0.45), ("forger", "Vermeers.", -0.3, 0.3), ("goering", "Göring's", -0.2, 0.35),
        ("rehook", "him.", -0.2, 0.3), ("arrest", "death.", -0.3, 0.45), ("proof", "witnesses.", -0.4, 0.3),
        ("verdict", "forgery.", -0.4, 0.35), ("loopend", "That's", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
