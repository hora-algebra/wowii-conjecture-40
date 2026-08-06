#!/usr/bin/env python3
"""
aggregate_n12.py -- union the n=12 interval results into one honest coverage
statement.  Each worker covers a contiguous `geng -bc -q 12` index interval
[a, done_upto]; the union is reported with any gap listed explicitly.  Overlaps
would be a defect, so they are detected and reported rather than summed.
"""
import json, glob, sys

TOTAL = 212780

def main():
    iv = []
    for f in sorted(glob.glob('results/n12-*.json')) + \
             sorted(glob.glob('results/n12-*.json.partial')):
        if 'DO-NOT' in f or 'SUPERSEDED' in f:
            continue
        try:
            s = json.load(open(f))['summary']
        except Exception:
            continue
        if s.get('range') is None:
            continue
        a = s['range'][0]
        b = s['done_upto']
        if b < a:
            continue
        iv.append((a, b, f, s))
    # prefer the completed file over its own .partial
    best = {}
    for (a, b, f, s) in iv:
        key = a
        if key not in best or b > best[key][1]:
            best[key] = (a, b, f, s)
    rows = sorted(best.values())
    agg = dict(graphs=0, instances=0, selections=0, cycle_components=0,
               a1_fail=0, hard_states=0, cl6_ok=0, cl7_steps=0, sampled_cl1=0)
    d0 = {}
    fails = {}
    covered = 0
    overlaps = []
    gaps = []
    prev_end = -1
    for (a, b, f, s) in rows:
        if a <= prev_end:
            overlaps.append((f, a, prev_end))
        elif a > prev_end + 1:
            gaps.append((prev_end + 1, a - 1))
        prev_end = max(prev_end, b)
        covered += b - a + 1
        for k in agg:
            agg[k] += s.get(k, 0)
        for k, v in s['d0_hist'].items():
            d0[k] = d0.get(k, 0) + v
        for k, v in s['failures'].items():
            fails[k] = fails.get(k, 0) + v
    if prev_end < TOTAL - 1:
        gaps.append((prev_end + 1, TOTAL - 1))
    out = dict(universe="geng -bc -q 12 (%d graphs)" % TOTAL,
               intervals=[(a, b, f.split('/')[-1]) for (a, b, f, s) in rows],
               covered_indices=covered,
               coverage_fraction=round(covered / TOTAL, 4),
               gaps=gaps, overlaps=overlaps,
               totals=agg, d0_hist=d0, failures=fails)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
