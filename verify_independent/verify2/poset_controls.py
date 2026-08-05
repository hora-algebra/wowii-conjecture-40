#!/usr/bin/env python3
"""VERIFY-2 controls for the independent poset checker.
Run BEFORE the target scan (PREREG-CARRIER-POSET.md control discipline)."""
import json
from posetverify2 import Sys, check_cp_adj, mask_list


def show(name, sysm, expect_cyclic=True):
    r = check_cp_adj(sysm)
    print("=== %s" % name)
    print("   nb=%s cap=%s feasible=%s selections=%d"
          % ([list(x) for x in sysm.nb], sysm.cap, sysm.feasible(),
             len(sysm.selections())))
    print("   tight sets =", [mask_list(X) for X in sysm.tight_sets()])
    f = sysm.forced_edges()
    print("   forced incidences =", sorted(f) if f else f)
    if r is None:
        print("   VERDICT: no cyclic forced core  (expected cyclic=%s)"
              % expect_cyclic)
        return r
    A, uniq = sysm.carriers()
    print("   carriers A =", {s: mask_list(A[s]) for s in range(sysm.k)},
          "unique=%s" % uniq)
    for d in r["detail"]:
        print("   cycle P=%s Q=%s  U=%s  P\\U=%s  pdis=%s  adj_ok=%s  cp_fail=%s"
              % (d["P"], d["Q"], d["U"], d["P_minus_U"], d["pdis"],
                 d["adj_ok"], d["cp_fail"]))
    return r


# --------------------------------------------------- ADJ-1 published witness
# S={s0,s1,s2}; H incidence vertices {0,1,2} all capacity 2.
# (x,y carry the distinguished edge but no incidences, so they are inert here.)
adj1 = Sys([(0, 1), (0, 2), (0, 1, 2)], [2, 2, 2])
r1 = show("ADJ-1 (published ADJ counterexample)", adj1)

# --------------------------------------------------- negative control: acyclic
# ACYCLIC-CONTROL.json: a~{0,1}, b~{2,3}; unique selection, no forced cycle.
acy = Sys([(0, 1), (2, 3)], [2, 2, 2, 2])
r2 = show("ACYCLIC-CONTROL (must have no forced cycle)", acy, False)

# --------------------------------------------------- positive: even-cycle system
# PROOFS.md sec D: the abstract even-cycle system S_i ~ H_i,H_{i+1}, demand 2,
# cap 2 is Hall-feasible yet its forced core IS a cycle.  m=3.
even3 = Sys([(0, 1), (1, 2), (2, 0)], [2, 2, 2])
r3 = show("EVEN-CYCLE m=3 (forced core must be a cycle)", even3)

even4 = Sys([(0, 1), (1, 2), (2, 3), (3, 0)], [2, 2, 2, 2])
r4 = show("EVEN-CYCLE m=4 (forced core must be a cycle)", even4)

# --------------------------------------------------- synthetic PDIS control
# must exhibit P intersect U != empty (the known-false companion firing)
print()
print("=== synthetic search for a PDIS system inside the frozen universe")
from posetverify2 import gen_exhaustive
found = 0
for sysm in gen_exhaustive():
    r = check_cp_adj(sysm)
    if r and r["pdis"]:
        print("   PDIS fires: nb=%s cap=%s" % ([list(x) for x in sysm.nb],
                                               sysm.cap))
        for d in r["detail"]:
            print("     P=%s U=%s P\\U=%s adj_ok=%s cp_fail=%s"
                  % (d["P"], d["U"], d["P_minus_U"], d["adj_ok"],
                     d["cp_fail"]))
        found += 1
        if found >= 2:
            break
print("   (PDIS control fired: %s)" % (found > 0))
