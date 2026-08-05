#!/usr/bin/env python3
"""Is A_s well-posed?  Separate the two possible failures, and separate
cycle vertices (where Common Tight Carrier applies) from off-cycle ones.

Common Tight Carrier (PROOFS.md sec D) asserts A_s exists and is the unique
minimum tight set containing s, for s ON a forced cycle.  For off-cycle s
nothing is claimed.  The tight-set lattice (C6) makes the minimum UNIQUE
whenever any tight set contains s; so the only possible failure is
NON-EXISTENCE (no tight set contains s at all)."""
from posetverify2 import gen_exhaustive, check_cp_adj, mask_list

no_tight_any = 0        # some s in S has no tight set containing it
no_tight_onP = 0        # some s in P has no tight set containing it
multi_min_any = 0       # some s in S has >1 inclusion-minimal tight superset
multi_min_onP = 0
cyclic = 0
examples = []

for sysm in gen_exhaustive():
    if not sysm.feasible():
        continue
    forced = sysm.forced_edges()
    cycles = sysm.forced_cycles(forced)
    if not cycles:
        continue
    cyclic += 1
    Pall = set()
    for (_, P, _) in cycles:
        Pall |= set(P)
    tights = sysm.tight_sets()
    bad_exist, bad_multi = [], []
    for s in range(sysm.k):
        cont = [X for X in tights if (X >> s) & 1]
        if not cont:
            bad_exist.append(s)
            continue
        minimal = [X for X in cont
                   if not any(Y != X and (Y & X) == Y for Y in cont)]
        if len(minimal) != 1:
            bad_multi.append(s)
    if bad_exist:
        no_tight_any += 1
        if set(bad_exist) & Pall:
            no_tight_onP += 1
            if len(examples) < 3:
                examples.append(("no-tight-on-P",
                                 [list(x) for x in sysm.nb], sysm.cap,
                                 bad_exist, sorted(Pall)))
        elif len(examples) < 3:
            examples.append(("no-tight-off-P",
                             [list(x) for x in sysm.nb], sysm.cap,
                             bad_exist, sorted(Pall)))
    if bad_multi:
        multi_min_any += 1
        if set(bad_multi) & Pall:
            multi_min_onP += 1

print("cyclic systems                          %d" % cyclic)
print("  with some s in S lacking a tight set  %d" % no_tight_any)
print("    ... where such an s lies ON a cycle %d" % no_tight_onP)
print("  with some s having >1 minimal tight   %d" % multi_min_any)
print("    ... where such an s lies ON a cycle %d" % multi_min_onP)
print()
for e in examples:
    print(" ", e)
