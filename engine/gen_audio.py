import json, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
import os; ROOT=os.environ.get("REC_ROOT","/home/claude/rec"); sys.path.insert(0, ROOT)
from script import SCENES

VOICE = sys.argv[1] if len(sys.argv) > 1 else "af_heart"
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
SR = 24000
k = Kokoro("/home/claude/rec/models/kokoro-v1.0.onnx", "/home/claude/rec/models/voices-v1.0.bin")

LEAD, GAP_SENT, GAP_SCENE = 0.35, 0.22, 0.45
chunks, timeline, t = [], [], LEAD
chunks.append(np.zeros(int(LEAD * SR), dtype=np.float32))
for si, (sid, sents) in enumerate(SCENES):
    scene = {"id": sid, "start": t, "sentences": []}
    for j, s in enumerate(sents):
        audio, sr = k.create(s, voice=VOICE, speed=SPEED, lang="en-us")
        assert sr == SR
        audio = audio.astype(np.float32)
        # trim leading/trailing near-silence
        idx = np.where(np.abs(audio) > 0.01)[0]
        if len(idx):
            audio = audio[max(0, idx[0] - 240): idx[-1] + 1200]
        d = len(audio) / SR
        scene["sentences"].append({"text": s, "start": t, "end": t + d})
        chunks.append(audio)
        t += d
        gap = GAP_SENT if j < len(sents) - 1 else GAP_SCENE
        chunks.append(np.zeros(int(gap * SR), dtype=np.float32))
        t += gap
    scene["end"] = t
    timeline.append(scene)
    print(f"{sid:10s} {scene['start']:6.2f} -> {scene['end']:6.2f}")

tail = 1.6  # hold on end card
chunks.append(np.zeros(int(tail * SR), dtype=np.float32))
t += tail
timeline[-1]["end"] = t
voice = np.concatenate(chunks)
sf.write(ROOT+"/voice.wav", voice, SR)
json.dump({"total": t, "scenes": timeline}, open(ROOT+"/timeline.json", "w"), indent=1)
print("TOTAL", round(t, 2))
