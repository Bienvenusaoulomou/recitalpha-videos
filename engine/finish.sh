#!/bin/bash
# usage: finish.sh ep13 EP13_Slug  -> mux, sample strip, push, url check
E=$1; N=$2
/home/claude/tools/mux.sh $E $N
V=/home/claude/recitalpha-videos/videos/Recitalpha_$N
D=/tmp/claude-0/fin_$E; mkdir -p $D; i=0
TT=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $V.mp4); TY=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${V}_yt.mp4)
for f in 0.01 0.15 0.35 0.55 0.75 0.95; do s=$(python3 -c "print(max(0.3,$TT*$f))"); ffmpeg -loglevel error -y -ss $s -i $V.mp4 -frames:v 1 -vf scale=216:384 $D/g_$i.png; i=$((i+1)); done
for f in 0.02 0.5 0.97; do s=$(python3 -c "print(max(0.3,$TY*$f))"); ffmpeg -loglevel error -y -ss $s -i ${V}_yt.mp4 -frames:v 1 -vf scale=216:384 $D/g_$i.png; i=$((i+1)); done
python3 -c "
from PIL import Image
S=Image.new('RGB',(216*9,384))
for i in range(9): S.paste(Image.open('$D/g_%d.png'%i).convert('RGB'),(i*216,0))
S.save('$D/strip.jpg')"
cd /home/claude/recitalpha-videos && git add videos/Recitalpha_${N}* && git commit -qm "$E $N (TikTok + YouTube loop cuts)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016oEeKTCBmNaew3HRkY6ocV" && git pull -q --rebase && git push -q 2>&1 | grep -vi warning | tail -2
for f in Recitalpha_$N.mp4 Recitalpha_${N}_yt.mp4; do echo "$f $(curl -s -o /dev/null -w '%{http_code}' -r 0-100 https://raw.githubusercontent.com/Bienvenusaoulomou/recitalpha-videos/main/videos/$f)"; done
