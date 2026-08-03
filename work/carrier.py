"""Carrier-layer scanner for ABSTRACT incidence-selection systems.

Motivation.  Every instance reachable from `geng` satisfies hereditary FVS
tightness and therefore (as far as anything has ever been checked) has an
acyclic forced core, so real graphs give NO data at all on the structure of a
forced cycle.  The three frozen witnesses are the only forced-cycle instances
in the repository.  This scanner drops the graph realisation and enumerates
ABSTRACT systems

    S (demands 2)  --  incidences  --  H (capacities c(h) in {1,2})

which is exactly the layer on which the Hall criterion, the tight-set lattice,
F1, the canonical carriers A_s and the punctures B_s are defined (paper
Lemmas 3.4-3.6, 4.4, 4.5).  Every system with a cyclic forced core is kept and
the carrier-layer claims below are tested on it.

CLAIMS TESTED (all are supposed to be THEOREMS of the Hall layer; a failure
means my proof is wrong, not that the claim is interesting):

  PT   punctured tightness: for each s on a forced cycle, A_s is the unique
       minimum tight set containing s, B_s = A_s \\ {s} is tight, exactly the
       two forced ends q of s have deg_{A_s}(q) <= c(q), and every other
       H-neighbour h of s has deg_{A_s}(h) >= c(h)+1.
  CS1  carrier-cycle separation (a): with U = union of the B_s over the cycle's
       S-side P, every s in P \\ U has deg_U(q) <= c(q)-1 at both of its forced
       ends q.
  CS2  carrier-cycle separation (b): if s_i and s_{i+1} are consecutive on the
       cycle and both lie in P \\ U, then deg_U(q_i) = 0 at their shared end.
  CS3  corollary (c): if P and U are disjoint, no vertex of U is adjacent to
       any cycle H-vertex.

Usage:
    python3 carrier.py exhaustive [maxK] [maxP]
    python3 carrier.py random <trials> [seed]
"""
import random
import sys
from itertools import combinations, product


def tight_sets(S, nbH, nbS, cap):
    """All Hall-tight X subseteq S, plus min delta (feasibility check)."""
    out, mind = [], 99
    for k in range(len(S) + 1):
        for X in combinations(S, k):
            X = frozenset(X)
            rho = sum(min(cap[h], len(nbS[h] & X)) for h in cap)
            d = rho - 2 * len(X)
            if d < mind:
                mind = d
            if d == 0:
                out.append(X)
    return out, mind


def feasible_selections(S, nbH, cap):
    per = []
    for s in S:
        opts = list(combinations(sorted(nbH[s]), 2))
        if not opts:
            return []
        per.append(opts)
    out = []
    for ch in product(*per):
        load = {}
        for (a, b) in ch:
            load[a] = load.get(a, 0) + 1
            load[b] = load.get(b, 0) + 1
        if all(load[h] <= cap[h] for h in load):
            out.append(ch)
    return out


def forced_and_cycles(S, sels):
    """Forced incidences, and the cycle components of the forced core."""
    if not sels:
        return None, None
    forced = None
    for ch in sels:
        cur = frozenset((s, h) for s, (a, b) in zip(S, ch) for h in (a, b))
        forced = cur if forced is None else (forced & cur)
    adj = {}
    for (s, h) in forced:
        adj.setdefault(('S', s), []).append(('H', h))
        adj.setdefault(('H', h), []).append(('S', s))
    seen, cycles = set(), []
    for v in list(adj):
        if v in seen:
            continue
        comp, stack = [], [v]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.append(u)
            stack += adj[u]
        nedge = sum(len(adj[u]) for u in comp) // 2
        if nedge == len(comp):          # max degree 2 => cyclic component
            cycles.append(comp)
        elif nedge > len(comp):
            cycles.append(comp)         # cannot happen (max degree 2)
    return forced, cycles


def walk_cycle(comp, forced):
    """Return the cyclic order [s_1, q_1, s_2, q_2, ...] of a forced cycle."""
    adj = {}
    cs = {v for v in comp}
    for (s, h) in forced:
        if ('S', s) in cs and ('H', h) in cs:
            adj.setdefault(('S', s), []).append(('H', h))
            adj.setdefault(('H', h), []).append(('S', s))
    start = comp[0]
    order, prev, cur = [start], None, start
    while True:
        nxt = [w for w in adj[cur] if w != prev]
        nxt = nxt[0] if len(nxt) == 1 else (nxt[0] if nxt[0] != prev else nxt[1])
        if nxt == start:
            break
        order.append(nxt)
        prev, cur = cur, nxt
    return order


def check(S, H, nbH, cap, report):
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = feasible_selections(S, nbH, cap)
    if not sels:
        return None
    forced, cycles = forced_and_cycles(S, sels)
    if not cycles:
        return None
    tights, mind = tight_sets(S, nbH, nbS, cap)
    tset = set(tights)

    def degX(h, X):
        return len(nbS[h] & frozenset(X))

    for comp in cycles:
        order = walk_cycle(comp, forced)
        P = [v[1] for v in order if v[0] == 'S']
        Q = [v[1] for v in order if v[0] == 'H']
        # canonical carriers
        A = {}
        for s in P:
            cand = [X for X in tights if s in X]
            Am = min(cand, key=len)
            if not all(Am <= Y for Y in cand):
                report('PT-unique-min-tight', S, H, nbH, cap, f"s={s}")
                return 'fail'
            A[s] = Am
        # PT
        for s in P:
            i = order.index(('S', s))
            ends = {order[(i - 1) % len(order)][1], order[(i + 1) % len(order)][1]}
            B = A[s] - {s}
            if frozenset(B) not in tset:
                report('PT-B-tight', S, H, nbH, cap, f"s={s}")
                return 'fail'
            for h in nbH[s]:
                if h in ends:
                    if degX(h, A[s]) > cap[h]:
                        report('PT-end-not-exposed', S, H, nbH, cap, f"s={s} h={h}")
                        return 'fail'
                else:
                    if degX(h, A[s]) < cap[h] + 1:
                        report('PT-external-not-oversubscribed', S, H, nbH, cap,
                               f"s={s} h={h}")
                        return 'fail'
        U = frozenset().union(*[A[s] - {s} for s in P]) if P else frozenset()
        if U and frozenset(U) not in tset:
            report('U-not-tight', S, H, nbH, cap, "")
            return 'fail'
        Pp = [s for s in P if s not in U]
        # CS1
        for s in Pp:
            i = order.index(('S', s))
            for j in (-1, 1):
                q = order[(i + j) % len(order)][1]
                if degX(q, U) > cap[q] - 1:
                    report('CS1', S, H, nbH, cap, f"s={s} q={q} degU={degX(q,U)}")
                    return 'fail'
        # CS2
        L = len(order)
        for i in range(0, L, 2):
            si = order[i][1] if order[i][0] == 'S' else None
            if si is None:
                continue
            q = order[(i + 1) % L][1]
            sj = order[(i + 2) % L][1]
            if si in Pp and sj in Pp and degX(q, U) != 0:
                report('CS2', S, H, nbH, cap, f"si={si} q={q} sj={sj}")
                return 'fail'
        # CS3
        if not (set(P) & set(U)):
            for q in Q:
                if degX(q, U) != 0:
                    report('CS3', S, H, nbH, cap, f"q={q}")
                    return 'fail'
        # ---- NEGATIVE CONTROLS -------------------------------------------
        # These are known-FALSE statements (O-63 refutes CTRL-DEG2; CTRL-PDIS
        # is the P-disjointness that must not be assumed).  They exist so that
        # "0 failures" above is evidence and not an artefact of dead code: the
        # same machinery must report failures for these.
        for s in P:
            for u in A[s] - {s}:
                if len(nbH[u]) != 2:
                    CONTROL['CTRL-DEG2'] += 1
                    break
        if set(P) & set(U):
            CONTROL['CTRL-PDIS'] += 1
    return 'ok'


FAILS = []
from collections import Counter
CONTROL = Counter()


def report(kind, S, H, nbH, cap, extra):
    FAILS.append((kind, list(S), list(H),
                  {s: sorted(nbH[s]) for s in S}, dict(cap), extra))


def run(systems, label):
    nsys = ncyc = 0
    for (S, H, nbH, cap) in systems:
        nsys += 1
        r = check(S, H, nbH, cap, report)
        if r is not None:
            ncyc += 1
    print(f"[{label}] systems scanned = {nsys}; "
          f"systems with a CYCLIC forced core = {ncyc}; "
          f"claim failures = {len(FAILS)}")
    print(f"    negative controls (must be > 0 to show the harness can fail): {dict(CONTROL)}")
    for f in FAILS[:5]:
        print("   FAIL", f)


def gen_exhaustive(maxK, maxP):
    for p in range(3, maxP + 1):
        H = list(range(p))
        opts = [frozenset(c) for r in (2, 3, 4) for c in combinations(H, r) if r <= p]
        for k in range(2, maxK + 1):
            S = [f"s{i}" for i in range(k)]
            for combo in product(opts, repeat=k):
                nbH = dict(zip(S, combo))
                if len(frozenset().union(*combo)) < p:
                    continue                      # H-vertex with no incidence
                for c1 in [()] + [(a, b) for a in H for b in H if a < b]:
                    cap = {h: (1 if h in c1 else 2) for h in H}
                    yield (S, H, nbH, cap)


def gen_random(trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        p = rng.randint(3, 8)
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


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "random"
    if mode == "exhaustive":
        mk = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        mp = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        run(gen_exhaustive(mk, mp), f"exhaustive k<={mk} p<={mp}")
    else:
        t = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
        sd = int(sys.argv[3]) if len(sys.argv) > 3 else 12345
        run(gen_random(t, sd), f"random {t} seed {sd}")
