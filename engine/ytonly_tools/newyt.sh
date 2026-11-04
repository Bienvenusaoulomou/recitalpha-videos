#!/bin/bash
# YouTube-only episode: newyt.sh ep22 twain   (copies photos from staged archive/new/<topic>)
E=/home/claude/$1; R=/home/claude/recitalpha-videos/engine
mkdir -p $E/img
for f in engine.py props.py kit.py kit2.py gen_audio.py mix_ep.py; do cp $R/$f $E/; done
ln -sfn /home/claude/rec/fonts $E/fonts; ln -sfn /home/claude/rec/models $E/models
[ -n "$2" ] && cp /mnt/user-data/uploads/Recitalpha/archive/new/$2/*.jpg $E/img/ 2>/dev/null
echo ok $E
