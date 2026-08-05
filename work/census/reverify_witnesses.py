#!/usr/bin/env python3
"""Re-verify every S1FAIL/S2FAIL witness from the C census with the frozen
Python checker l6scan.py (attempt/2026-08-04-claude-fable-5-0eb8,
sha256 2e568740...). For each witness graph6: recompute the full profile and
assert the same verdict (no minimum OCT satisfies the L5 / L6 condition).
"""
import sys, glob, os

sys.path.insert(0, "/Users/christineozols/conj40v2/attempt-fable-0eb8/work/fable-0eb8")
from l6scan import parse_graph6, profile

def main(pattern):
    n_s1 = n_s2 = 0
    seen = {}
    for path in sorted(glob.glob(pattern)):
        for line in open(path):
            if not (line.startswith("S1FAIL") or line.startswith("S2FAIL")):
                continue
            tag, g6 = line.split()[0], line.split()[1]
            if g6 not in seen:
                n, adj = parse_graph6(g6)
                seen[g6] = profile(n, adj)
            pr = seen[g6]
            if tag == "S1FAIL":
                n_s1 += 1
                assert pr["best"]["l5"] < 0, (g6, pr["best"])
            else:
                n_s2 += 1
                assert pr["best"]["l6"] < 0, (g6, pr["best"])
            print(f"REVERIFIED {tag} {g6}: p={pr['p']} o={pr['o']} "
                  f"octs={len(pr['octs'])} L5margin={pr['best']['l5']} "
                  f"L6margin={pr['best']['l6']} slack={pr['best']['slack']}")
    print(f"TOTAL reverified: S1={n_s1} S2={n_s2}; all agree with l6scan.py")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "n10/out-*.txt")
