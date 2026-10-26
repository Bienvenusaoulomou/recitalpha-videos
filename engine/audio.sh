#!/bin/bash
# usage: audio.sh ep09  -> voice for both cuts, yt tail trimmed to 0.35 s
E=/home/claude/$1
for D in $E $E/yt; do (cd $D && REC_ROOT=$D python3 gen_audio.py af_heart 1.05 | tail -1) & done; wait
cd $E/yt && python3 - <<'PY'
import json, soundfile as sf
tl=json.load(open('timeline.json')); last=tl['scenes'][-1]['sentences'][-1]['end']
T=round(last+0.35,3); tl['total']=T; tl['scenes'][-1]['end']=T; json.dump(tl,open('timeline.json','w'),indent=1)
v,sr=sf.read('voice.wav'); sf.write('voice.wav',v[:int(T*sr)],sr); print('YT TOTAL',T)
PY
