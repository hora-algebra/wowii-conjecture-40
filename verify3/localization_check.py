r"""VERIFY-3: machine-check of LEMMA-A-CLEAN-END.md section 5's two
localization-refutation claims and section 6's CAP2-BS gold table.

Claims checked (quoting the target):
  (L1) "in O-63 the maximal carrier A_t = {t} has tau(G[H u A_t]) = 1 > 0"
       -- i.e. some cycle vertex t has carrier {t} (maximal), and the
       violation does NOT live there.
  (L2) "in O-64 neither maximal carrier works (A_s = {s,u} has two
       vertex-disjoint cycles, tau = 2 > 1)"
  (C1) CAP2-BS gold rows: O-56 (s in {0,1}, B_s={2,3}, guard yes,
       tau(G[H u B_s]) = 1 = |B_s|-1), O-63 (B_s={u,a,b}, guard yes,
       tau = 2 = |B_s|-1), ADJ-1 (B_s2={s0,s1}, guard yes, tau=0 <= 1),
       O-64 (B_s={u}, guard NO (cap-1 neighbour), tau = 1 > 0 = |B_s|-1:
       unguarded form FAILS).
All tau computed by brute-force minimum FVS on the realized graphs.
"""
import json
import sys
from itertools import combinations

sys.path.insert(0, 'verify3')
from nc_verify3 import (feasible, forced_core, core_cycles, all_tight,
                        load_witness)


def realize(w):
    """Vertices + undirected edge set of the witness graph."""
    V = [str(x) for x in w['vertices']['S']] + [str(x) for x in w['vertices']['H']]
    E = set()
    for (a, b) in w['incidence_edges_S_H'] + w.get('H_forest_edges', []):
        E.add(frozenset((str(a), str(b))))
    return V, E


def tau_induced(V, E, keep):
    keep = set(keep)
    edges = [tuple(e) for e in E if set(e) <= keep]
    verts = sorted(keep)

    def forest(rm):
        rm = set(rm)
        adj = {}
        for (a, b) in edges:
            if a in rm or b in rm:
                continue
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        seen = set()
        for r in adj:
            if r in seen:
                continue
            stack = [(r, None)]
            seen.add(r)
            while stack:
                v, par = stack.pop()
                skippar = False
                for u in adj.get(v, []):
                    if u == par and not skippar:
                        skippar = True
                        continue
                    if u in seen:
                        return False
                    seen.add(u)
                    stack.append((u, v))
        return True

    for k in range(len(verts) + 1):
        for rm in combinations(verts, k):
            if forest(rm):
                return k
    return len(verts)


def carriers(path):
    w, S, H, nbH, cap = load_witness(path)
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = feasible(S, nbH, cap)
    order = core_cycles(forced_core(sels))[0]
    P = [v[1] for v in order if v[0] == 'S']
    Q = [v[1] for v in order if v[0] == 'H']
    L = len(order)
    ends = {x: {order[(i - 1) % L][1], order[(i + 1) % L][1]}
            for i, (t, x) in enumerate(order) if t == 'S'}
    tights, _ = all_tight(S, nbS, cap, H)
    A = {s: frozenset.intersection(*[X for X in tights if s in X]) for s in P}
    return w, S, H, nbH, cap, P, Q, ends, A


def main():
    ok = True

    # ---- L1: O-63
    w, S, H, nbH, cap, P, Q, ends, A = carriers('tools/witnesses/O-63.json')
    V, E = realize(w)
    Hset = [str(x) for x in w['vertices']['H']]
    maxima = [t for t in P if not any(A[t] < A[s] for s in P if s != t)]
    l1 = False
    for t in maxima:
        if A[t] == frozenset({t}):
            tv = tau_induced(V, E, set(Hset) | set(A[t]))
            print(f"[L1 O-63] maximal carrier A_{t}={sorted(A[t])} "
                  f"tau(G[H u A_t])={tv} (target claims 1 > 0)")
            l1 = (tv == 1)
    ok &= l1

    # ---- L2: O-64
    w, S, H, nbH, cap, P, Q, ends, A = carriers('tools/witnesses/O-64.json')
    V, E = realize(w)
    Hset = [str(x) for x in w['vertices']['H']]
    maxima = [t for t in P if not any(A[t] < A[s] for s in P if s != t)]
    l2 = True
    for t in maxima:
        tv = tau_induced(V, E, set(Hset) | set(A[t]))
        viol = tv < len(A[t])
        print(f"[L2 O-64] maximal carrier A_{t}={sorted(A[t])} "
              f"tau={tv} vs |A|={len(A[t])} violation={viol} "
              f"(target: no maximal carrier violates)")
        if viol:
            l2 = False
        if A[t] == frozenset({t, 'u'}) and tv != 2:
            l2 = False
    ok &= l2

    # ---- C1: CAP2-BS gold rows
    rows = [
        ('tools/witnesses/O-56.json', '0', {'2', '3'}, True, 1),
        ('tools/witnesses/O-63.json', 's', {'u', 'a', 'b'}, True, 2),
        ('verify3/ADJ-WITNESS.json', 's2', {'s0', 's1'}, True, 0),
        ('tools/witnesses/O-64.json', 's', {'u'}, False, 1),
    ]
    for (path, sname, Bexp, guard_exp, tau_exp) in rows:
        w, S, H, nbH, cap, P, Q, ends, A = carriers(path)
        V, E = realize(w)
        Hset = [str(x) for x in w['vertices']['H']]
        B = A[sname] - {sname}
        nonend = [h for h in nbH[sname] if h not in ends[sname]]
        guard = all(cap[h] == 2 for h in nonend)
        tv = tau_induced(V, E, set(Hset) | B)
        bound_holds = tv <= len(B) - 1
        row_ok = (B == frozenset(Bexp) and guard == guard_exp and tv == tau_exp)
        print(f"[C1 {w['id']}] s={sname} B_s={sorted(B)} (exp {sorted(Bexp)}) "
              f"nonend={sorted(nonend)} caps={[cap[h] for h in sorted(nonend)]} "
              f"guard={guard} (exp {guard_exp}) tau={tv} (exp {tau_exp}) "
              f"CAP2-BS holds={bound_holds} row_ok={row_ok}")
        ok &= row_ok
        if w['id'] == 'O-64':
            ok &= not bound_holds     # unguarded form must FAIL here

    print(f"[LOCALIZATION+CAP2BS] {'ALL CONFIRMED' if ok else '*** MISMATCH ***'}")


if __name__ == '__main__':
    main()
