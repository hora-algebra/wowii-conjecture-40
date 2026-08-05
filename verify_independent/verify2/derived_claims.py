#!/usr/bin/env python3
"""VERIFY-2 checks on the derived / consequence claims of both branches."""
import itertools
from posetverify2 import Sys, gen_exhaustive, check_cp_adj, mask_list
from sdverify2 import g6_decode, is_forest

print("=" * 70)
print("CLAIM (b17e): the ADJ witness is NOT a Lemma-A counterexample -")
print("  it has tau(G[H u S]) = 1 < 3, so hereditary FVS tightness fails.")
# realise the witness as a graph: S={s0,s1,s2} -> vertices 0,1,2
#   H incidence vertices {0,1,2} -> vertices 3,4,5 ; plus x,y -> 6,7
n = 8
E = [(0, 3), (0, 4),           # s0 ~ 0,1
     (1, 3), (1, 5),           # s1 ~ 0,2
     (2, 3), (2, 4), (2, 5),   # s2 ~ 0,1,2
     (6, 7)]                   # the distinguished H-edge x-y
adj = [0] * n
for u, v in E:
    adj[u] |= 1 << v
    adj[v] |= 1 << u
full = (1 << n) - 1


def tau_of(vmask):
    verts = [v for v in range(n) if (vmask >> v) & 1]
    for k in range(len(verts) + 1):
        for combo in itertools.combinations(verts, k):
            D = 0
            for v in combo:
                D |= 1 << v
            if is_forest(adj, vmask & ~D, n):
                return k
    return len(verts)


print("  tau(G[H u S]) = tau(G) =", tau_of(full), " |S| = 3")
print("  => hereditary FVS tightness FAILS:", tau_of(full) != 3)
Smask = 0b111
print("  H = G - S is a forest:", is_forest(adj, full & ~Smask, n))

print()
print("=" * 70)
print("CLAIM (b17e): 'CP guarantees two capacity holes at a maximal vertex' -")
print("  for s in P\\U, both forced ends q obey deg_U(q) <= 1,")
print("  equivalently each retains >=1 unit of capacity outside U.")
tot = viol_le1 = viol_cap = 0
for sysm in gen_exhaustive():
    r = check_cp_adj(sysm)
    if r is None:
        continue
    forced = sysm.forced_edges()
    for (E2, P, Q) in sysm.forced_cycles(forced):
        A, _ = sysm.carriers()
        U = 0
        for s in P:
            U |= A[s] & ~(1 << s)
        PminusU = [s for s in P if not ((U >> s) & 1)]
        for s in PminusU:
            ends = [h for (ss, h) in E2 if ss == s]
            for q in ends:
                degU = sum(1 for t in range(sysm.k)
                           if ((U >> t) & 1) and q in sysm.nb[t])
                tot += 1
                if degU > 1:
                    viol_le1 += 1
                if degU > sysm.cap[q] - 1:
                    viol_cap += 1
print("  forced ends of P\\U vertices checked : %d" % tot)
print("  violations of deg_U(q) <= 1          : %d" % viol_le1)
print("  violations of deg_U(q) <= c(q) - 1   : %d" % viol_cap)

print()
print("=" * 70)
print("CLAIM (4d7a): 3 selected cycles impossible below n=13; 2 need n>=9.")
print("  each selected cycle uses >=2 S- and >=2 H-vertices;")
print("  feasibility: 2|S| <= sum_h c(h) = 2|H| - 2, so |H| >= |S| + 1.")
for k in (2, 3):
    Smin = 2 * k
    Hmin = Smin + 1
    print("  %d disjoint cycles: |S| >= %d, hence |H| >= %d, so n >= %d"
          % (k, Smin, Hmin, Smin + Hmin))
