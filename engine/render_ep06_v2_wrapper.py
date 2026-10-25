import os, sys
os.environ["REC_ROOT"] = "/home/claude/ep06"
sys.path.insert(0, "/home/claude/ep06")
import importlib
R = importlib.import_module("render_ep06_poyais")
from props import *
import script as S
E = R.E

def sc_rehook(c, t, D):
    l1, l2, l3 = S.REHOOK
    b1 = beat("rehook", 1)
    pa = prog(t, 0.0, 0.22)
    pop_text(c, l1, CX, 640, BEBAS, 110, CREAM, pa, s0=1.4)
    pop_text(c, l2, CX, 800, ANTON, 150, GOLD2, prog(t, 0.25, 0.25), glow=26, glow_rgb=GOLD)
    pb = prog(t, b1 - 0.1, 0.25)
    if pb > 0:
        pop_text(c, l3, CX, 1000, ANTON, 84, RED if "DEADLY" in l3 else CREAM, pb, glow=18, s0=1.5)

E.DRAW["rehook"] = sc_rehook
ids = {s["id"] for s in E.SCENES}
IMPACTS = [x for x in R.IMPACTS if x[0] in ids] + [("rehook", S.SCENES[[s[0] for s in S.SCENES].index("rehook")][1][0].split()[0], -0.1, 0.3)]
CLINKS = [x for x in getattr(R, "CLINKS", []) if x[0] in ids]
ROOT = R.ROOT

if __name__ == "__main__":
    E.main()
