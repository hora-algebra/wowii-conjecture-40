#!/bin/zsh
cd "$(dirname "$0")"
PHASE0_BIN="${PHASE0_BIN:-$PWD/../verification/phase0}"
for r in 1 2 3; do
  ( mkdir -p sv11/s$r && cd sv11/s$r && PHASE0_OUT=. geng -c -q 11 $r/1024 | "$PHASE0_BIN" run2 > out.txt 2>&1 ; echo "sv shard $r rc=$?" ) &
done
wait
echo "SV11 DONE"
cat sv11/s*/out.txt
wc -l sv11/s*/phase0-run2-VIOL.txt
