import json, sys, subprocess, glob, os
from PIL import Image
ep, mod = sys.argv[1], sys.argv[2]
extra = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else []
tl = json.load(open(f"{ep}/timeline.json"))
fr = [0] + extra
for s in tl["scenes"]:
    d = s["end"] - s["start"]
    fr += [int((s["start"] + d * 0.35) * 30), int((s["start"] + d * 0.85) * 30)]
for f in glob.glob(f"{ep}/prev_*.png"): os.remove(f)
r = subprocess.run(["python3", mod, "--frames=" + ",".join(map(str, fr))], cwd=ep, capture_output=True, text=True)
print(r.stdout[-2000:], r.stderr[-3000:])
ims = [Image.open(f"{ep}/prev_{f:05d}.png").convert("RGB").resize((270, 480)) for f in fr]
cols = 9
S = Image.new("RGB", (cols * 270, ((len(ims) + cols - 1) // cols) * 480))
for i, im in enumerate(ims): S.paste(im, ((i % cols) * 270, (i // cols) * 480))
S.save(f"{ep}/contact.jpg", quality=80); print(fr)
