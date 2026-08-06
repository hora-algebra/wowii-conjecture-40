#!/usr/bin/env python3
"""
witness_check.py -- instantiate the branch's lemmas on the three frozen
witnesses tools/witnesses/O-{56,63,64}.json, as ATTACK.md Step 4(a) requires.

The witnesses are instances in which hereditary FVS tightness FAILS somewhere
(that is what lets their forced core be cyclic).  So they are a genuine
adversarial test for the results that DO use hereditary tightness — those must
be allowed to fail here, and the failure must be traceable to the violated
hypothesis, not to the argument.  The results that do NOT use tightness must
hold.

Checked per witness, on every feasible selection and every selected cycle:
  T1  every length-one residual step is CES                (no tightness used)
  T2  d0(C)=1 iff some S-vertex of C has a slack neighbour (no tightness used)
  P12 path-component count / total slack / |Sat| <= |S|+1  (no tightness used)
  T3  N_H(P(C)) strictly contains Q(C)                     (USES tightness)
  T6  slack-free closure is rho-tight, W nonempty, forced  (USES tightness)
and the hereditary-tightness status of the instance itself is reported.
"""
import json, itertools, sys
import s2e_scan as B


def load(path):
    d = json.load(open(path))
    S = list(d['vertices']['S'])
    H = list(d['vertices']['H'])
    idx = {v: i for i, v in enumerate(S + H)}   # names may be strings
    S = [idx[v] for v in S]
    H = [idx[v] for v in H]
    n = len(idx)
    adj = [0] * n
    for (a, b) in d['incidence_edges_S_H'] + d['H_forest_edges']:
        a, b = idx[a], idx[b]
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    e = tuple(idx[v] for v in d['distinguished_edge'])
    col = B.bipartition(n, adj)
    if col is None:
        raise SystemExit('witness %s is not bipartite as read' % d['id'])
    return d, n, adj, col, S, H, e


def check(path):
    d, n, adj, col, S, H, e = load(path)
    Sm = 0
    for s in S:
        Sm |= 1 << s
    out = {'id': d['id'], 'fixed_edge': list(e) if e else None}
    # hereditary tightness status of the instance
    Hm = ((1 << n) - 1) & ~Sm
    viol = []
    for r in range(0, len(S) + 1):
        for X in itertools.combinations(S, r):
            xm = 0
            for x in X:
                xm |= 1 << x
            if B.tau(n, adj, Hm | xm) != len(X):
                viol.append(list(X))
    out['hereditary_tightness_violations'] = len(viol)
    out['first_violating_sets'] = viol[:3]
    inst = B.Inst(n, adj, col, Sm, e)
    sels = B.feasible_selections(inst)
    out['feasible_selections'] = len(sels)
    res = dict(cycles=0, T1_fail=0, T2_fail=0, P12_fail=0, T3_fail=0,
               T6_fired=0, T6_fail=0)
    for sel in sels:
        E, degH, inc = B.sel_state(inst, sel)
        comps = B.components(inst, E)
        cyc = [c for c in comps if len(c[0]) == len(c[1])]
        old = set(c[1] for c in cyc)
        # P12
        covered = set()
        for (vs, es) in comps:
            covered |= set(vs)
        iso = [h for h in inst.Hlist if h not in covered]
        npaths = len(comps) - len(cyc) + len(iso)
        p = len(inst.Hlist) - len(inst.Slist)
        slack = sum(inst.cap[h] - degH[h] for h in inst.Hlist)
        nsat = sum(1 for h in inst.Hlist if degH[h] == inst.cap[h])
        if npaths != p or slack != 2 * p - 2 or nsat > len(inst.Slist) + 1:
            res['P12_fail'] += 1
        for (vs, es) in cyc:
            res['cycles'] += 1
            P = [v for v in vs if v in inst.NH]
            Q = set(v for v in vs if v not in inst.NH)
            # T3
            outside = set()
            for s in P:
                outside |= set(inst.NH[s]) - Q
            if not outside:
                res['T3_fail'] += 1
            # T2 / T1
            best = None
            paths = []
            for (s, h) in es:
                dd, ps = B.residual_paths(inst, E, degH, inc, (s, h))
                if dd is None:
                    continue
                if best is None or dd < best:
                    best, paths = dd, [((s, h), q) for q in ps]
                elif dd == best:
                    paths += [((s, h), q) for q in ps]
            slack_adj = any(degH[h] < inst.cap[h] for s in P
                            for h in inst.NH[s])
            if best is not None and ((best == 1) != slack_adj):
                res['T2_fail'] += 1
            for (a, q) in paths:
                if len(q) != 2:
                    continue
                ns = B.toggle(inst, sel, a, q)
                nE, nd, ninc = B.sel_state(inst, ns)
                nc = set(c[1] for c in B.selected_cycles(inst, nE))
                if not (es not in nc and nc <= old):
                    res['T1_fail'] += 1
            # T6
            A, Y, reached = B.closure(inst, E, degH, inc, P)
            if not reached:
                res['T6_fired'] += 1
                NA = set()
                for s in A:
                    NA |= set(inst.NH[s])
                W = NA - Y
                bad = (B.rho(inst, A) != 2 * len(A)) or (not W) or \
                      (len(NA) < len(A) + 1)
                if bad:
                    res['T6_fail'] += 1
    out.update(res)
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(check(p), indent=1))
