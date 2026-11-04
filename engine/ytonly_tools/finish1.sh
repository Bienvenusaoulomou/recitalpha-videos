#!/bin/bash
# finish1.sh ep22 EP22_Slug -> mux YT cut, strip, push, url check
E=/home/claude/$1; N=$2; V=/home/claude/recitalpha-videos/videos/Recitalpha_${N}_yt.mp4
ffmpeg -loglevel error -y -i $E/video_only.mp4 -i $E/mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $V
TY=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $V); echo "$V $(du -m $V | cut -f1)MB ${TY}s"
D=/tmp/claude-0/fin_$1; mkdir -p $D; i=0
for f in 0.01 0.12 0.25 0.38 0.5 0.62 0.75 0.88 0.98; do s=$(python3 -c "print(max(0.3,$TY*$f))"); ffmpeg -loglevel error -y -ss $s -i $V -frames:v 1 -vf scale=216:384 $D/g_$i.png; i=$((i+1)); done
python3 -c "
from PIL import Image
S=Image.new('RGB',(216*9,384))
for i in range(9): S.paste(Image.open('$D/g_%d.png'%i).convert('RGB'),(i*216,0))
S.save('$D/strip.jpg')"
cd /home/claude/recitalpha-videos && git add -A engine videos/Recitalpha_${N}_yt.mp4 && git commit -qm "$1 $N (YouTube loop cut)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016oEeKTCBmNaew3HRkY6ocV" && git pull -q --rebase && git push -q 2>&1 | grep -vi warning | tail -2
echo "Recitalpha_${N}_yt.mp4 $(curl -s -o /dev/null -w '%{http_code}' -r 0-100 https://raw.githubusercontent.com/Bienvenusaoulomou/recitalpha-videos/main/videos/Recitalpha_${N}_yt.mp4)"
