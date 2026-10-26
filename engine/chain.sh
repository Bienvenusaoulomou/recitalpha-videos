#!/bin/bash
# usage: chain.sh epNN module
EP=$1; M=$2
for D in /home/claude/$EP /home/claude/$EP/yt; do
  cd $D && REC_ROOT=$D python3 /home/claude/tools/dryrun.py $M > dry.log 2>&1 || { echo "DRYFAIL $D" >> /home/claude/$EP/chain.status; exit 1; }
done
for D in /home/claude/$EP /home/claude/$EP/yt; do
  cd $D && REC_ROOT=$D python3 $M.py > render.log 2>&1 && REC_ROOT=$D python3 mix_ep.py $M > mix.log 2>&1 || { echo "RENDERFAIL $D" >> /home/claude/$EP/chain.status; exit 1; }
  echo "DONE $D" >> /home/claude/$EP/chain.status
done
