#!/bin/bash
# usage: newep.sh ep09
E=/home/claude/$1; R=/home/claude/recitalpha-videos/engine
mkdir -p $E/img $E/yt
for f in engine.py props.py kit.py gen_audio.py mix_ep.py; do cp $R/$f $E/; cp $R/$f $E/yt/; done
for D in $E $E/yt; do ln -sfn /home/claude/rec/fonts $D/fonts; ln -sfn /home/claude/rec/models $D/models; done
ln -sfn $E/img $E/yt/img
echo ok $E
