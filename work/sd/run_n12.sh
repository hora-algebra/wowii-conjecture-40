#!/bin/bash
cd "$(dirname "$0")"
seq 0 31 | xargs -P 8 -I{} python3 sd_scan2.py 12 {} 32
echo "ALL 32 SHARDS DONE" >> n12-driver.log
