"""Independent re-derivation of the three frozen witnesses, for GAUNTLET.md.

Reads tools/witnesses/*.json as raw DATA (vertices, incidences, forest edges,
capacities) and recomputes everything else from the definitions with
engine0520: feasible selections, forced core, forced cycles, Hall-tight sets,
canonical carriers A_s, punctures B_s, U, and tau(G[H u X]) for every
X subseteq S.  No derived field of the JSON is trusted.
"""
import json
import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine0520 as E

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..'))


def load(name):
    with open(os.path.join(ROOT, 'tools', 'witnesses', name + '.json')) as f:
        j = json.load(f)
    S = [str(v) for v in j['vertices']['S']]
    H = [str(v) for v in j['vertices']['H']]
    nbH = {s: set() for s in S}
    for (a, b) in j['incidence_edges_S_H']:
        nbH[str(a)].add(str(b))
    nbH = {s: frozenset(v) for s, v in nbH.items()}
    Hedges = [(str(a), str(b)) for (a, b) in j['H_forest_edges']]
    c1 = set(str(v) for v in j['capacities'].get('c1_vertices', []))
    cap = {h: (1 if h in c1 else 2) for h in H}
    return j, S, H, nbH, Hedges, cap


def report(name):
    j, S, H, nbH, Hedges, cap = load(name)
    print(f"===== {name} =====")
    print(f"  S={S}  H={H}  c1={[h for h in H if cap[h]==1]}")

    # --- H is a forest?
    adjH = {h: set() for h in H}
    for (a, b) in Hedges:
        adjH[a].add(b)
        adjH[b].add(a)
    print(f"  H is a forest: {not E.has_cycle(adjH)}")

    sels = E.feasible_selections(S, nbH, cap)
    print(f"  feasible selections: {len(sels)}")
    forced = E.forced_incidences(S, nbH, cap)
    print(f"  forced incidences ({len(forced)}): {sorted(forced)}")
    cycles = E.forced_core_cycles(forced)
    print(f"  forced-core cyclic components: {len(cycles)}")
    for order in cycles:
        print(f"    cycle: {' - '.join(v[1] for v in order)}")

    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    tights, mind = E.tight_sets(S, nbS, cap)
    print(f"  min delta over subsets = {mind} (>=0 means Hall-feasible)")
    print(f"  Hall-tight sets: {sorted(tuple(sorted(t)) for t in tights)}")

    for order in cycles:
        res = dict(tights=tights)
        P = [v[1] for v in order if v[0] == 'S']
        Q = [v[1] for v in order if v[0] == 'H']
        A = {s: E.canonical_carrier(s, tights) for s in P}
        B = {s: A[s] - {s} for s in P}
        U = frozenset().union(*B.values()) if P else frozenset()
        print(f"  P={sorted(P)}  Q={sorted(Q)}")
        for s in P:
            print(f"    A_{s}={sorted(A[s])}  B_{s}={sorted(B[s])}")
        print(f"    U={sorted(U)}   P&U={sorted(set(P)&set(U))}   "
              f"P\\U={sorted(set(P)-set(U))}")
        for q in Q:
            print(f"    deg_U({q})={len(nbS[q] & U)}  c={cap[q]}")

    # --- hereditary FVS tightness, every subset
    viol = []
    for k in range(1, len(S) + 1):
        for X in combinations(sorted(S), k):
            t = E.tau_induced(Hedges, H, nbH, set(X))
            if t < len(X):
                viol.append((tuple(X), t))
    print(f"  hereditary tightness violations tau(G[H u X])<|X| : {len(viol)}")
    minimal = []
    for (X, t) in viol:
        if not any(set(Y) < set(X) for (Y, _) in viol):
            minimal.append((X, t))
    print(f"    inclusion-MINIMAL violating sets: "
          f"{[(X, f'tau={t}<{len(X)}') for (X, t) in minimal]}")
    tS = E.tau_induced(Hedges, H, nbH, set(S))
    print(f"  tau(G[H u S])={tS}, |S|={len(S)}  -> S is a minimum FVS: "
          f"{tS == len(S)}")


if __name__ == "__main__":
    for name in (sys.argv[1:] or ['O-56', 'O-63', 'O-64']):
        report(name)
        print()
