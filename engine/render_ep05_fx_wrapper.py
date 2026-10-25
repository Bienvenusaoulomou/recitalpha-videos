import os, sys
os.environ.setdefault("REC_ROOT", "/home/claude/ep05")
sys.path.insert(0, os.environ["REC_ROOT"])
import importlib
R = importlib.import_module("render_ep05_lufthansa")
from props import *
import script as S
E = R.E
E.FX = True
BR = "/home/claude/broll"

def sc_rehook(c, t, D):
    l1, l2, l3 = S.REHOOK
    b1 = beat("rehook", 1)
    pop_text(c, l1, CX, 640, BEBAS, 110, CREAM, prog(t, 0.0, 0.22), s0=1.4)
    pop_text(c, l2, CX, 800, ANTON, 150, GOLD2, prog(t, 0.25, 0.25), glow=26, glow_rgb=GOLD)
    pb = prog(t, b1 - 0.1, 0.25)
    if pb > 0:
        sz = 84
        while text_w(l3, F(ANTON, sz)) > 880 and sz > 40: sz -= 2
        pop_text(c, l3, CX, 1000, ANTON, sz, RED if "DEADLY" in l3 else CREAM, pb, glow=18, s0=1.15)

def sc_loopend(c, t, D):
    l1, l2, l3 = S.LOOPEND
    b1 = beat("loopend", 1)
    pop_text(c, l1, CX, 640, BEBAS, 96, CREAM, prog(t, 0.0, 0.22), s0=1.3)
    pop_text(c, l2, CX, 790, ANTON, 120, GOLD2, prog(t, 0.35, 0.25), glow=22, glow_rgb=GOLD)
    pb = prog(t, b1 - 0.1, 0.25)
    if pb > 0:
        sz = 80
        while text_w(l3, F(ANTON, sz)) > 880 and sz > 40: sz -= 2
        pop_text(c, l3, CX, 980, ANTON, sz, CREAM, pb, s0=1.15)

E.DRAW["rehook"] = sc_rehook
E.DRAW["loopend"] = sc_loopend
ids = {s["id"] for s in E.SCENES}
first_word = lambda sid: [x for x in S.SCENES if x[0] == sid][0][1][0].split()[0]
IMPACTS = [x for x in R.IMPACTS if x[0] in ids] + [("rehook", first_word("rehook"), -0.1, 0.3)]
CLINKS = [x for x in getattr(R, "CLINKS", []) if x[0] in ids]
ROOT = R.ROOT
E.set_hits(IMPACTS)
E.BROLL["cash"] = E.load_broll(f"{BR}/vault_cleveland_small.mp4", start=36, dur=7, alpha=0.8, credit="ARCHIVE FOOTAGE · PUBLIC DOMAIN")
E.BROLL["loot"] = E.load_broll(f"{BR}/vault_cleveland_small.mp4", start=18, dur=9, alpha=0.75, credit="ARCHIVE FOOTAGE · PUBLIC DOMAIN")
if __name__ == "__main__": E.main()
