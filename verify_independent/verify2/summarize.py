#!/usr/bin/env python3
"""merge shard JSONs and print the graded table"""
import sys, json
from collections import Counter

files = sys.argv[1:]
ctr = Counter()
hist = Counter()
cap = 0
wit = {}
ns = set()
shards = []
for f in files:
    d = json.load(open(f))
    ns.add(d["n"])
    shards.append(d["shard"])
    for k, v in d["counters"].items():
        ctr[k] += v
    for k, v in d["ncyc_histogram"].items():
        hist[int(k)] += v
    cap += d["path_cap_hits"]
    for k, v in d["witnesses"].items():
        wit.setdefault(k, [])
        wit[k].extend(v)

print("n            =", sorted(ns))
print("shards       =", len(shards), "->", sorted(shards)[:5], "...")
for k in ["graphs", "cyclic_selections", "cycle_components",
          "a1_failures", "sd_short_failures", "sd_count_short_failures",
          "sd_plus2_failures", "bplus2_all_failures",
          "sd_2step_probed", "sd_2step_failures",
          "sd_2step_descent_failures", "lemmaA_violations"]:
    print("%-28s %d" % (k, ctr.get(k, 0)))
print("%-28s %d" % ("path_cap_hits", cap))
print("ncyc histogram              ", dict(sorted(hist.items())))
for k, v in wit.items():
    if v:
        print("--- witnesses[%s] (%d shown)" % (k, len(v)))
        seen = set()
        for w in v:
            key = (w.get("g6"), tuple(w.get("S", [])), tuple(w.get("e", [])))
            if key in seen:
                continue
            seen.add(key)
            print("   ", json.dumps(w))
