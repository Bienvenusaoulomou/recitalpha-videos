#!/bin/bash
# usage: mux.sh ep09 EP09_Antwerp_Diamond_Heist
E=/home/claude/$1; V=/home/claude/recitalpha-videos/videos
ffmpeg -loglevel error -y -i $E/video_only.mp4 -i $E/mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $V/Recitalpha_$2.mp4
ffmpeg -loglevel error -y -i $E/yt/video_only.mp4 -i $E/yt/mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $V/Recitalpha_$2_yt.mp4
for f in $V/Recitalpha_$2.mp4 $V/Recitalpha_$2_yt.mp4; do echo "$f $(du -m $f | cut -f1)MB $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)s"; done
