#!/bin/bash
# usage: queue.sh "ep15 render_ep15" "ep16 render_ep16" ...  (runs when < 3 chains active)
for job in "$@"; do
  while [ $(pgrep -fc "^/bin/bash (/home/claude/)?tools/chain.sh") -ge 3 ]; do sleep 20; done
  nohup /home/claude/tools/chain.sh $job >/dev/null 2>&1 &
  sleep 5
done
