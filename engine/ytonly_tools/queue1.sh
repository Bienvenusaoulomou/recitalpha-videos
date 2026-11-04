#!/bin/bash
# queue1.sh ep23 ep24 ... : renders YT-only episodes, 2 at a time
for e in "$@"; do
  while [ $(pgrep -fc "tools/chain1.sh") -ge 2 ]; do sleep 15; done
  rm -f /home/claude/$e/chain.status
  nohup /home/claude/tools/chain1.sh $e render_$e > /dev/null 2>&1 &
  sleep 3
done
wait
while [ $(pgrep -fc "tools/chain1.sh") -ge 1 ]; do sleep 15; done
for e in "$@"; do echo "$e $(cat /home/claude/$e/chain.status 2>/dev/null)"; done
