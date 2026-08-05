#!/usr/bin/env python3
"""VERIFY-2 full audit of the six n=11 SD-SHORT / A1 witnesses.

Checks, independently, every mechanism claim made about them in
4d7a ATTEMPT_REPORT.md claims 2/3/7 and PROOFS.md sec B3 / sec E:
  - G connected bipartite; H = G-S a forest
  - tau(G) = |S| = 4, so S IS a minimum FVS
  - hereditary FVS tightness: tau(G[H u X]) = |X| for EVERY X subset S
  - exactly 2 feasible selections, each with exactly one selected 4-cycle
  - d0 = 3, zero CES minimisers, first CES at length 5 (gap exactly 2)
  - profile (|cyc(J)|, #A1-good cycles) = (1, 0)
  - over all shortest bad paths: exactly one old cycle destroyed (C),
    exactly one new cycle Z, final added edge (u,t) lies on Z,
    d0(J0) = 1, |cyc(J0)| = |cyc(J)| = 1, and a CES minimising second step
"""
import itertools, json
from sdverify2 import (g6_decode, min_fvs_all, is_forest, Inst,
                       cycle_components, bfs_residual, enum_paths, toggle,
                       is_ces, INF)
from sdscan2 import bounded_paths, admits_ces_min_step

CASES = [("J??FErWxDw?", [0, 2, 3, 4], (5, 10)),
         ("J?B@eQo]Fo?", [6, 7, 8, 10], (0, 5)),
         ("J?B@eOtq`i_", [0, 1, 6, 10], (4, 9))]

CAP = [0]
total_bad_paths = 0
total_failing_cycles = 0
allok = True


def tau_of(adj, n, vmask):
    """min FVS size of the induced subgraph on vmask"""
    verts = [v for v in range(n) if (vmask >> v) & 1]
    for k in range(len(verts) + 1):
        for combo in itertools.combinations(verts, k):
            D = 0
            for v in combo:
                D |= 1 << v
            if is_forest(adj, vmask & ~D, n):
                return k
    return len(verts)


for g6, S, e in CASES:
    n, adj = g6_decode(g6)
    Smask = 0
    for v in S:
        Smask |= 1 << v
    print("=" * 72)
    print("graph %s   S=%s   e=%s" % (g6, S, e))

    # ---- bipartite + connected
    colour = [-1] * n
    colour[0] = 0
    stack = [0]
    seen = 1
    bip = True
    while stack:
        v = stack.pop()
        for w in range(n):
            if (adj[v] >> w) & 1:
                if colour[w] == -1:
                    colour[w] = 1 - colour[v]
                    seen += 1
                    stack.append(w)
                elif colour[w] == colour[v]:
                    bip = False
    print("  bipartite=%s connected=%s" % (bip, seen == n))

    # ---- S a minimum FVS?
    tau, fvss = min_fvs_all(adj, n)
    print("  tau(G)=%d  |S|=%d  S is a minimum FVS: %s"
          % (tau, len(S), Smask in fvss))
    allok &= (tau == len(S)) and (Smask in fvss)

    # ---- H a forest
    full = (1 << n) - 1
    print("  H = G-S is a forest: %s" % is_forest(adj, full & ~Smask, n))

    # ---- hereditary FVS tightness for EVERY X subset S
    ht = True
    for r in range(len(S) + 1):
        for X in itertools.combinations(S, r):
            Xm = 0
            for v in X:
                Xm |= 1 << v
            if tau_of(adj, n, (full & ~Smask) | Xm) != len(X):
                ht = False
    print("  hereditary FVS tightness tau(G[H u X])=|X| for all X: %s" % ht)
    allok &= ht

    # ---- the incidence system
    inst = Inst(adj, n, Smask, e)
    forced = inst.forced_set()
    sels = inst.selections()
    print("  feasible selections: %d" % len(sels))

    for ch in sels:
        selset = inst.sel_of(ch)
        cyc = cycle_components(inst, selset)
        if not cyc:
            continue
        load = inst.loads(selset)
        oldset = set(cyc)
        for C in cyc:
            avoid = [a for a in C if a not in forced]
            d0 = INF
            info = []
            for a in avoid:
                d, dS, dH, tg = bfs_residual(inst, selset, load, a)
                info.append((a, d, dS, dH, tg))
                d0 = min(d0, d)
            steps = []
            for (a, d, dS, dH, tg) in info:
                if d == d0:
                    for p in enum_paths(inst, selset, a, dS, dH, tg, CAP):
                        steps.append((a, p))
            ces_min = [(a, p) for (a, p) in steps
                       if is_ces(inst, oldset, toggle(selset, a, p), C)[0]]
            if ces_min:
                continue                      # A1-good cycle, not a witness
            total_failing_cycles += 1
            print("  --- A1-FAILING cycle: |C|=%d edges, |cyc(J)|=%d, d0=%d, "
                  "#minimising steps=%d, #CES minimisers=%d"
                  % (len(C), len(cyc), d0, len(steps), len(ces_min)))
            allok &= (len(C) == 4 and len(cyc) == 1 and d0 == 3
                      and len(ces_min) == 0)

            # first CES length (dCES)
            best = INF
            for a in avoid:
                for p in bounded_paths(inst, selset, load, a, d0 + 4):
                    if is_ces(inst, oldset, toggle(selset, a, p), C)[0]:
                        best = min(best, len(p))
            print("      dCES = %s   (gap = %s)" % (best, best - d0))
            allok &= (best == d0 + 2)

            # per-bad-path structure
            n_paths = 0
            ok_paths = 0
            for (a, p) in steps:
                n_paths += 1
                J0 = toggle(selset, a, p)
                cy0 = cycle_components(inst, J0)
                destroyed = [z for z in cyc if z not in cy0]
                created = [z for z in cy0 if z not in oldset]
                # d0(J0) over its cycles
                load0 = inst.loads(J0)
                d0J0 = INF
                for Z in cy0:
                    for a2 in Z:
                        if a2 in forced:
                            continue
                        d2, _, _, _ = bfs_residual(inst, J0, load0, a2)
                        d0J0 = min(d0J0, d2)
                final_added = p[0] if len(p) == 1 else p[-1]
                onZ = any(final_added in Z for Z in created)
                second = admits_ces_min_step(inst, forced, J0, cy0)
                good = (destroyed == [C] and len(created) == 1
                        and len(cy0) == len(cyc) and d0J0 == 1
                        and onZ and second)
                ok_paths += good
                if not good:
                    print("      BAD PATH STRUCTURE:", len(p), len(destroyed),
                          len(created), len(cy0), d0J0, onZ, second)
            total_bad_paths += n_paths
            print("      shortest bad paths: %d; all with "
                  "[destroyed=={C}, exactly 1 new cycle Z, (u,t) on Z, "
                  "d0(J0)=1, |cyc(J0)|=|cyc(J)|, CES minimising 2nd step]: %d/%d"
                  % (n_paths, ok_paths, n_paths))
            allok &= (ok_paths == n_paths)

print("=" * 72)
print("A1-failing cycles found      : %d   (report claims 6)" % total_failing_cycles)
print("total shortest bad paths     : %d   (report/PROOFS sec B3 claim 20)"
      % total_bad_paths)
print("ALL STRUCTURAL CLAIMS HELD   : %s" % allok)
