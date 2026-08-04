#!/bin/zsh
cd /Users/christineozols/conj40-attempts/work
for r in 0 1 2 3; do
  ( mkdir -p n10/s$r && cd n10/s$r && geng -c -q 10 $r/4 | ../../lift run > out.txt 2>&1 ; echo "shard $r rc=$?" ) &
done
wait
echo "ALL SHARDS DONE"
cat n10/s*/out.txt
