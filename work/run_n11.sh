#!/bin/zsh
cd /Users/christineozols/conj40-attempts/work
for r in 1 2 3; do
  ( mkdir -p n11/s$r && cd n11/s$r && geng -c -q 11 $r/1024 | ../../lift run > out.txt 2>&1 ; echo "shard $r rc=$?" ) &
done
wait
echo "N11 SHARDS DONE"
cat n11/s*/out.txt
