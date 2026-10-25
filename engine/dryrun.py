import sys, importlib, skia
import os; sys.path.insert(0, os.getcwd())
mod = sys.argv[1]; sys.argv = [sys.argv[0]]
R = importlib.import_module(mod); E = R.E
surf = skia.Surface(E.W, E.H); c = surf.getCanvas()
import math
n = int(math.ceil(E.TOTAL * E.FPS))
for fi in range(0, n, 3): E.frame(c, fi)
print("DRYRUN OK", n)
