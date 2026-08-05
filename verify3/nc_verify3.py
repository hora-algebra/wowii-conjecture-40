r"""VERIFY-3 fresh checker for NC / NCM(CE) / CP-regression / A-I+ (counting step).

Written from the STATEMENTS in verify3/SEALED-NC-DERIVATION.md and
LEMMA-A-CLEAN-END.md only. No predicate code was read from work/0520/,
work/carrier.py's check(), b17e's carrier_poset.py, or work/wcheck.py.
The two GENERATORS replicate work/carrier.py's universe definitions
verbatim (universe identity is required to reproduce published anchors);
every predicate below is fresh.

Predicates tested on every system with a cyclic forced core:
  HALL  internal consistency: feasible selections exist iff min delta >= 0
  PT    punctured tightness (regression of certified stack)
  CPR   carrier-poset regression: t in B_s => A_t proper subset of A_s;
        P\U == inclusion-maximal carriers; P\U nonempty
  NC    for every clean q (deg_U(q) <= 1):
          (i) N_S(q) & P == cyc(q); (ii) N_S(q) & (U\P) == empty;
          consequence deg_U(q) == |cyc(q) & U|
  NCM   for every s in P\U both forced ends clean and
        N_S(q) & (P|U) == cyc(q), size exactly 2
  AIP   A-I+ hypothesis (exists clean q0, Ext==empty on cyc(q0),
        |Ext|<=1 elsewhere on P); when it holds, the counting step:
        every s in cyc(q0) has surviving degree exactly 1 (only q0) and
        every other s in P has surviving degree |Ext(s)| <= 1, checked
        against raw adjacency (NOT via NC -- raw).
Negative controls (known-false; must fire somewhere or harness is dead):
  NC-ALL     every q in Q is clean            (false on ADJ-1)
  CHORD-ALL  every q in Q has N_S(q)&P==cyc(q) (false on ADJ-1)
  PDIS       P & U == empty                    (false on 18 anchor systems)
Controls are counted once per SYSTEM (any cyclic component may trigger).
"""
import json
import random
import sys
from itertools import combinations, product


# ---------------------------------------------------------------- generators
# Universe definitions replicated from certified work/carrier.py (5047).
def gen_exhaustive(maxK, maxP):
    for p in range(3, maxP + 1):
        H = list(range(p))
        opts = [frozenset(c) for r in (2, 3, 4) for c in combinations(H, r) if r <= p]
        for k in range(2, maxK + 1):
            S = [f"s{i}" for i in range(k)]
            for combo in product(opts, repeat=k):
                nbH = dict(zip(S, combo))
                if len(frozenset().union(*combo)) < p:
                    continue
                for c1 in [()] + [(a, b) for a in H for b in H if a < b]:
                    cap = {h: (1 if h in c1 else 2) for h in H}
                    yield (S, H, nbH, cap)


def gen_random(trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        p = rng.randint(3, 6)
        k = rng.randint(2, 5)
        H = list(range(p))
        S = [f"s{i}" for i in range(k)]
        nbH = {}
        for s in S:
            d = rng.randint(2, min(p, 4))
            nbH[s] = frozenset(rng.sample(H, d))
        c1 = rng.sample(H, 2) if (p >= 2 and rng.random() < 0.5) else []
        cap = {h: (1 if h in c1 else 2) for h in H}
        yield (S, H, nbH, cap)


# ---------------------------------------------------------------- fresh engine
def feasible(S, nbH, cap):
    """All feasible selections, as tuples of frozenset({(s,h),...})."""
    per = []
    for s in S:
        pairs = list(combinations(sorted(nbH[s], key=str), 2))
        if not pairs:
            return []
        per.append([(s, a, b) for (a, b) in pairs])
    sols = []
    def rec(i, load, acc):
        if i == len(per):
            sols.append(frozenset(acc))
            return
        for (s, a, b) in per[i]:
            la, lb = load.get(a, 0) + 1, load.get(b, 0) + 1
            if la <= cap[a] and lb <= cap[b]:
                load[a], load[b] = la, lb
                acc.append((s, a)); acc.append((s, b))
                rec(i + 1, load, acc)
                acc.pop(); acc.pop()
                load[a] -= 1; load[b] -= 1
                if load[a] == 0: del load[a]
                if load[b] == 0: del load[b]
    rec(0, {}, [])
    return sols


def forced_core(sels):
    f = None
    for J in sels:
        f = J if f is None else (f & J)
    return f or frozenset()


def core_cycles(forced):
    """Cyclic components of the forced core as ordered lists
    [s1,q1,s2,q2,...]; the core has max degree 2."""
    adj = {}
    for (s, h) in forced:
        adj.setdefault(('S', s), set()).add(('H', h))
        adj.setdefault(('H', h), set()).add(('S', s))
    seen, out = set(), []
    for v0 in adj:
        if v0 in seen:
            continue
        comp, stack = set(), [v0]
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(adj[u] - comp)
        seen |= comp
        ne = sum(len(adj[u]) for u in comp) // 2
        if ne < len(comp):
            continue                      # tree component
        # walk the cycle
        start = min(comp, key=str)
        order, prev, cur = [start], None, start
        while True:
            nxts = [w for w in adj[cur] if w != prev]
            nxt = nxts[0]
            if nxt == start:
                break
            order.append(nxt)
            prev, cur = cur, nxt
        if order[0][0] == 'H':            # rotate so an S-vertex leads
            order = order[1:] + order[:1]
        out.append(order)
    return out


def all_tight(S, nbS, cap, Hs):
    """(list of tight frozensets, min delta over all X)."""
    tights, mind = [], None
    for k in range(len(S) + 1):
        for X in combinations(S, k):
            Xf = frozenset(X)
            rho = sum(min(cap[h], len(nbS[h] & Xf)) for h in Hs)
            d = rho - 2 * k
            if mind is None or d < mind:
                mind = d
            if d == 0:
                tights.append(Xf)
    return tights, mind


class Fail(Exception):
    pass


def check_system(S, H, nbH, cap, counters, certs, tag):
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = feasible(S, nbH, cap)
    tights, mind = all_tight(S, nbS, cap, H)
    if (len(sels) > 0) != (mind >= 0):
        raise Fail(f"HALL inconsistency {tag}: sels={len(sels)} mind={mind}")
    if not sels:
        return False
    forced = forced_core(sels)
    cycles = core_cycles(forced)
    if not cycles:
        return False
    counters['cyclic'] += 1

    def fail(name, msg):
        counters[name + '_fail'] += 1
        if len(certs) < 8:
            certs.append((name, tag, {s: sorted(nbH[s], key=str) for s in S},
                          {h: cap[h] for h in H}, msg))

    fired = set()
    for order in cycles:
        P = [v[1] for v in order if v[0] == 'S']
        Q = [v[1] for v in order if v[0] == 'H']
        m = len(P)
        cyc = {}
        L = len(order)
        for i, (t, x) in enumerate(order):
            if t == 'H':
                cyc[x] = {order[(i - 1) % L][1], order[(i + 1) % L][1]}
        ends = {}
        for i, (t, x) in enumerate(order):
            if t == 'S':
                ends[x] = {order[(i - 1) % L][1], order[(i + 1) % L][1]}
        # carriers: A_s = intersection of all tight sets containing s
        A = {}
        for s in P:
            cont = [X for X in tights if s in X]
            if not cont:
                fail('PT', f"no tight set contains s={s}")
                continue
            As = frozenset.intersection(*cont)
            if As not in set(tights):
                fail('PT', f"A_{s} (intersection) not tight -> no unique min")
                continue
            A[s] = As
        if len(A) < len(P):
            continue
        # PT regression
        for s in P:
            B = A[s] - {s}
            if B not in set(tights) and len(B) >= 0:
                rhoB = sum(min(cap[h], len(nbS[h] & B)) for h in H)
                if rhoB != 2 * len(B):
                    fail('PT', f"B_{s} not tight")
            for h in nbH[s]:
                dA = len(nbS[h] & A[s])
                if h in ends[s]:
                    if dA > cap[h]:
                        fail('PT', f"end {h} of {s}: deg_A={dA}>cap")
                else:
                    if dA < cap[h] + 1:
                        fail('PT', f"non-end {h} of {s}: deg_A={dA}<cap+1")
        U = frozenset().union(*[A[s] - {s} for s in P])
        PU = set(P) & U
        # CPR
        for s in P:
            for t in P:
                if s != t and t in A[s] - {s}:
                    if not (A[t] < A[s]):
                        fail('CPR', f"t={t} in B_{s} but A_t not proper subset A_s")
        maxima = {t for t in P
                  if not any(A[t] < A[s2] for s2 in P if s2 != t)}
        if {t for t in P if t not in U} != maxima:
            fail('CPR', f"P\\U != maximal carriers")
        if all(t in U for t in P):
            fail('CPR', "P\\U empty")
        # NC
        def degU(h):
            return len(nbS[h] & U)
        for q in Q:
            if degU(q) <= 1:                      # clean
                if nbS[q] & set(P) != cyc[q]:
                    fail('NC', f"(i) q={q}: N_P={sorted(nbS[q]&set(P),key=str)}"
                               f" != cyc={sorted(cyc[q],key=str)}")
                if nbS[q] & (U - set(P)):
                    fail('NC', f"(ii) q={q}: aux nbrs "
                               f"{sorted(nbS[q]&(U-set(P)),key=str)}")
                if degU(q) != len(cyc[q] & U):
                    fail('NC', f"(cons) q={q}: degU={degU(q)}"
                               f" != |cyc&U|={len(cyc[q]&U)}")
        # NCM / CE
        PmU = [s for s in P if s not in U]
        if not PmU:
            fail('NCM', "P\\U empty (CE existence)")
        for s in PmU:
            for q in ends[s]:
                if degU(q) > 1:
                    fail('NCM', f"end {q} of maximal {s} not clean: degU={degU(q)}")
                elif nbS[q] & (set(P) | U) != cyc[q] or len(cyc[q]) != 2:
                    fail('NCM', f"end {q} of {s}: N_(P|U)="
                               f"{sorted(nbS[q]&(set(P)|U),key=str)}")
        # A-I+ (hypothesis + counting step, raw adjacency)
        Ext = {s: nbH[s] - set(Q) for s in P}
        hyp_q = [q for q in Q if degU(q) <= 1
                 and all(len(Ext[s]) == 0 for s in cyc[q])
                 and all(len(Ext[s]) <= 1 for s in P if s not in cyc[q])]
        if hyp_q:
            counters['aiplus_hyp'] += 1
            q0 = hyp_q[0]
            for s in P:
                surv = (Ext[s] | ({q0} if q0 in nbH[s] else set()))
                if s in cyc[q0]:
                    if surv != {q0}:
                        fail('AIP', f"s={s} in cyc(q0={q0}): surviving nbrs {sorted(surv,key=str)}")
                else:
                    if len(surv) > 1:
                        fail('AIP', f"s={s} deg {len(surv)}>1 after deleting Q-{{q0}}")
        # negative controls
        if any(degU(q) > 1 for q in Q):
            fired.add('NC-ALL')
        if any(nbS[q] & set(P) != cyc[q] for q in Q):
            fired.add('CHORD-ALL')
        if PU:
            fired.add('PDIS')
    for c in fired:
        counters[c] += 1
    return True


def run(systems, label):
    from collections import Counter
    counters = Counter()
    certs = []
    n = 0
    for (S, H, nbH, cap) in systems:
        n += 1
        check_system(S, H, nbH, cap, counters, certs, f"{label}#{n}")
    print(f"[{label}] systems={n} cyclic={counters['cyclic']} "
          f"NC_fail={counters['NC_fail']} NCM_fail={counters['NCM_fail']} "
          f"CPR_fail={counters['CPR_fail']} PT_fail={counters['PT_fail']} "
          f"AIP_hyp={counters['aiplus_hyp']} AIP_fail={counters['AIP_fail']}")
    print(f"    controls fired (systems): NC-ALL={counters['NC-ALL']} "
          f"CHORD-ALL={counters['CHORD-ALL']} PDIS={counters['PDIS']}")
    for c in certs:
        print("  FAIL-CERT", c)
    return counters


# ---------------------------------------------------------------- witnesses
def load_witness(path):
    with open(path) as fp:
        w = json.load(fp)
    S = [str(x) for x in w['vertices']['S']]
    H = [str(x) for x in w['vertices']['H']]
    nbH = {s: frozenset() for s in S}
    for (a, b) in w['incidence_edges_S_H']:
        a, b = str(a), str(b)
        if a in nbH:
            nbH[a] = nbH[a] | {b}
        else:
            nbH[b] = nbH[b] | {a}
    c1 = {str(x) for x in w['capacities'].get('c1_vertices', [])}
    cap = {h: (1 if h in c1 else 2) for h in H}
    return w, S, H, nbH, cap


def witness_mode(paths):
    from collections import Counter
    for path in paths:
        w, S, H, nbH, cap = load_witness(path)
        counters = Counter()
        certs = []
        sels = feasible(S, nbH, cap)
        fc = forced_core(sels)
        cyc = core_cycles(fc)
        ok = check_system(S, H, nbH, cap, counters, certs, w['id'])
        exp = w.get('feasible_selections', {}).get('count')
        fc_exp = w.get('forced_core_edges')
        fc_match = ''
        if fc_exp is not None:
            fc_have = frozenset((str(a), str(b)) for (a, b) in fc_exp)
            fc_match = f" forced_core_matches_json={fc_have == fc}"
        print(f"[{w['id']}] feasible={len(sels)} (json {exp}) "
              f"cyclic_core={bool(cyc)} checked={ok} "
              f"NC_fail={counters['NC_fail']} NCM_fail={counters['NCM_fail']} "
              f"CPR_fail={counters['CPR_fail']} PT_fail={counters['PT_fail']} "
              f"AIP_hyp={counters['aiplus_hyp']} AIP_fail={counters['AIP_fail']}"
              f"{fc_match}")
        print(f"    controls: NC-ALL={counters['NC-ALL']} "
              f"CHORD-ALL={counters['CHORD-ALL']} PDIS={counters['PDIS']}")
        for c in certs:
            print("  FAIL-CERT", c)


# ------------------------------------------------------- mutation controls
def mutation_controls(adj_path, o56_path):
    """Prove THIS harness can fail: feed it corrupted/unguarded inputs."""
    from collections import Counter
    ok = True

    # MUT-1: NC predicate applied to ALL q of ADJ-1 (clean guard removed)
    w, S, H, nbH, cap = load_witness(adj_path)
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = feasible(S, nbH, cap)
    order = core_cycles(forced_core(sels))[0]
    P = [v[1] for v in order if v[0] == 'S']
    Q = [v[1] for v in order if v[0] == 'H']
    L = len(order)
    cyc = {x: {order[(i-1) % L][1], order[(i+1) % L][1]}
           for i, (t, x) in enumerate(order) if t == 'H'}
    tights, _ = all_tight(S, nbS, cap, H)
    A = {s: frozenset.intersection(*[X for X in tights if s in X]) for s in P}
    U = frozenset().union(*[A[s] - {s} for s in P])
    bad = [q for q in Q if nbS[q] & set(P) != cyc[q]]
    print(f"[MUT-1] NC(i) without clean guard on ADJ-1: "
          f"violations at q={bad} (must be nonempty)")
    ok &= bool(bad)

    # MUT-2: predicate-level injection. Compute carriers/U on GENUINE O-56,
    # then corrupt the adjacency of clean q=4 with aux vertex 3 and re-run
    # the NC(ii) predicate exactly as written in check_system.
    w, S, H, nbH, cap = load_witness(o56_path)
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = feasible(S, nbH, cap)
    order = core_cycles(forced_core(sels))[0]
    P = [v[1] for v in order if v[0] == 'S']
    L = len(order)
    cyc = {x: {order[(i-1) % L][1], order[(i+1) % L][1]}
           for i, (t, x) in enumerate(order) if t == 'H'}
    tights, _ = all_tight(S, nbS, cap, H)
    A = {s: frozenset.intersection(*[X for X in tights if s in X]) for s in P}
    U = frozenset().union(*[A[s] - {s} for s in P])
    nbS_bad = dict(nbS); nbS_bad['4'] = nbS['4'] | {'3'}
    q = '4'
    clean = len(nbS_bad[q] & U) <= 1
    nc2_viol = bool(nbS_bad[q] & (U - set(P)))
    print(f"[MUT-2] O-56, injected aux chord 3~4: q=4 clean={clean}, "
          f"NC(ii) violation detected={nc2_viol} (both must be True)")
    ok &= clean and nc2_viol

    # MUT-3: predicate-level injection. Genuine ADJ-1 cycle; inject
    # Ext(s0)={x}; the A-I+ counting step at q0=1 (s0 in cyc(q0)) must fail.
    w, S, H, nbH, cap = load_witness(adj_path)
    sels = feasible(S, nbH, cap)
    order = core_cycles(forced_core(sels))[0]
    P = [v[1] for v in order if v[0] == 'S']
    Q = [v[1] for v in order if v[0] == 'H']
    nbH_bad = dict(nbH); nbH_bad['s0'] = nbH['s0'] | {'x'}
    Ext = {s: nbH_bad[s] - set(Q) for s in P}
    q0 = '1'
    s = 's0'                                # s0 ~ q0=1 and s0 in cyc(q0)
    surv = (Ext[s] | ({q0} if q0 in nbH_bad[s] else set()))
    fired = surv != {q0}
    print(f"[MUT-3] ADJ-1, injected Ext(s0)={{x}}: counting step at q0=1 "
          f"gives surviving nbrs {sorted(surv)} != {{q0}}: detected={fired} "
          f"(must be True)")
    ok &= fired
    print(f"[MUTATION CONTROLS] {'ALL FIRED' if ok else '*** DEAD CODE ***'}")


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exhaustive':
        run(gen_exhaustive(int(sys.argv[2]), int(sys.argv[3])),
            f"exhaustive k<={sys.argv[2]} p<={sys.argv[3]}")
    elif mode == 'random':
        run(gen_random(int(sys.argv[2]), int(sys.argv[3])),
            f"random {sys.argv[2]} seed {sys.argv[3]}")
    elif mode == 'witness':
        witness_mode(sys.argv[2:])
    elif mode == 'mutation':
        mutation_controls(sys.argv[2], sys.argv[3])
