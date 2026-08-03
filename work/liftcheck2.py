"""Independent second engine for the frozen lifting statements (PREREG-LIFT.md).

Pure Python, written from the statements rather than from lift.c; shares no code
with it (it reuses only the graph6 parser and the brute-force invariant helpers
in liftclass.py, which were themselves written independently of lift.c).
Prints the same aggregate line as `lift run` so the two can be diffed.

Usage: python3 liftcheck2.py <n>        (reads geng -c -q n itself)
"""
import subprocess
import sys
from itertools import combinations

sys.path.insert(0, ".")
from liftclass import (parse_g6, is_bip, max_bip, max_forest, path_cover)


def run(n):
    gs = subprocess.run(["geng", "-c", "-q", str(n)],
                        capture_output=True, text=True).stdout.split()
    tot = nonbip = 0
    fA = fAall = fP = fPall = fSV = 0
    maxOCT = 0
    slack = {}
    for g6 in gs:
        nn, adj = parse_g6(g6)
        full = (1 << nn) - 1
        tot += 1
        b = max_bip(nn, adj, full)
        o = nn - b
        if o == 0:
            continue
        nonbip += 1
        pG = path_cover(nn, adj, full)
        ell = nn - pG
        okA = okP = False
        allA = allP = True
        best = None
        nOCT = 0
        for T in combinations(range(nn), o):
            Tm = 0
            for t in T:
                Tm |= 1 << t
            rest = full ^ Tm
            if not is_bip(nn, adj, rest):
                continue
            nOCT += 1
            tauB = (nn - o) - max_forest(nn, adj, rest)
            a = ell - (2 * tauB + o + 1)
            best = a if best is None else max(best, a)
            if a >= 0:
                okA = True
            else:
                allA = False
            pB = path_cover(nn, adj, rest)
            if pG <= pB:
                okP = True
            else:
                allP = False
        maxOCT = max(maxOCT, nOCT)
        if not okA:
            fA += 1
        if not allA:
            fAall += 1
        if not okP:
            fP += 1
        if not allP:
            fPall += 1
        # SV
        sv = False
        elig = 0
        for t in range(nn):
            rest = full ^ (1 << t)
            ot = (nn - 1) - max_bip(nn, adj, rest)
            if ot == o - 1:
                elig += 1
                if path_cover(nn, adj, rest) >= pG:
                    sv = True
        if elig and not sv:
            fSV += 1
        slack[best] = slack.get(best, 0) + 1
    print(f"ENGINE-2 n={n} graphs={tot} nonbipartite={nonbip} "
          f"LIFT-A_fail={fA} LIFT-A-ALL_fail={fAall} LIFT-P_fail={fP} "
          f"LIFT-P-ALL_fail={fPall} SV_fail={fSV} maxminOCTs={maxOCT}")
    print(f"    bestA slack histogram: {dict(sorted(slack.items()))}")


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
