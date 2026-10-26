#!/bin/bash
# regenerate yt audio only: trimyt.sh ep12
cd /home/claude/$1/yt && REC_ROOT=$PWD python3 gen_audio.py af_heart 1.05 | tail -1 && python3 - <<'PY'
import json, soundfile as sf
tl=json.load(open('timeline.json')); last=tl['scenes'][-1]['sentences'][-1]['end']
T=round(last+0.35,3); tl['total']=T; tl['scenes'][-1]['end']=T; json.dump(tl,open('timeline.json','w'),indent=1)
v,sr=sf.read('voice.wav'); sf.write('voice.wav',v[:int(T*sr)],sr); print('YT TOTAL',T)
PY
