#!/bin/bash
# chain1.sh ep22 render_ep22 : dryrun + render + mix (single YT cut)
D=/home/claude/$1; M=$2; cd $D
REC_ROOT=$D python3 /home/claude/tools/dryrun.py $M > dry.log 2>&1 || { echo "DRYFAIL" > chain.status; exit 1; }
REC_ROOT=$D python3 $M.py > render.log 2>&1 && REC_ROOT=$D python3 mix_ep.py $M > mix.log 2>&1 || { echo "RENDERFAIL" > chain.status; exit 1; }
echo DONE > chain.status
