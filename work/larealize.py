"""Targeted falsification search for Lemma A-degree (paper Problem 4.1).

KEY SIMPLIFICATION used throughout.  Hereditary FVS tightness for every
X subseteq S is EQUIVALENT to "S is a minimum FVS of G":
  (<=) is paper Lemma 3.3;
  (=>) take X = S, giving tau(G) = |S|, and S is an FVS since G - S = H.
So a Lemma-A-degree counterexample is exactly:

    a bipartite G (connectedness NOT required), a MINIMUM FVS S with
    H = G - S, a fixed H-edge e, and a cyclic forced core.

Whether the forced core is cyclic depends ONLY on the abstract system
(S, H, incidences, capacities) -- the H-forest edges are irrelevant to
feasibility and forcedness.  Whether S is a minimum FVS depends ONLY on the
H-forest (given the incidences).  The two halves are therefore independent, and
the search factorises:

  stage 1  enumerate abstract systems with a CYCLIC forced core (carrier.py);
  stage 2  for each, enumerate every bipartite-consistent H-forest completion
           and ask whether tau(G) = |S|.

A single hit at stage 2 FALSIFIES Lemma A-degree.  Every miss yields the
inclusion-minimal X subseteq S with tau(G[H u X]) < |X| -- which is exactly the
localization data the open problem asks for, and of which the repository has
only three hand-built points (O-56, O-63, O-64).

Capacity handling.  If the system designates a capacity-1 pair {x,y}, the
completion must contain the H-edge xy (that is what makes c(x)=c(y)=1).  If all
capacities are 2, the fixed edge is supplied by a separate K_2 component --
legitimate because Problem 4.1 does not assume connectedness, and the K_2
endpoints carry no incidences, so they contribute nothing to tau.

Usage:  python3 larealize.py exhaustive [maxK] [maxP] [steiner]
        python3 larealize.py random <trials> [seed] [steiner]
"""
import sys
from collections import Counter
from itertools import combinations, product

sys.path.insert(0, ".")
import carrier as C

CAP = 50000   # max forest completions examined per abstract system (reported)


# ---------------- graph utilities ----------------

def is_forest_edges(nv, edges):
    par = list(range(nv))

    def f(v):
        while par[v] != v:
            par[v] = par[par[v]]
            v = par[v]
        return v

    for (u, v) in edges:
        a, b = f(u), f(v)
        if a == b:
            return False
        par[a] = b
    return True


def tau_of(vertices, edges):
    """Minimum feedback vertex set size, brute force by increasing size."""
    vs = sorted(vertices, key=str)
    idx = {v: i for i, v in enumerate(vs)}
    E = [(idx[u], idx[v]) for (u, v) in edges if u in idx and v in idx]
    n = len(vs)
    for k in range(n + 1):
        for D in combinations(range(n), k):
            dm = set(D)
            if is_forest_edges(n, [(u, v) for (u, v) in E
                                   if u not in dm and v not in dm]):
                return k, {vs[i] for i in D}
    return n, set()


def colourings(S, H, nbH):
    """All proper 2-colourings of the incidence graph, as dicts v -> 0/1."""
    adj = {v: set() for v in list(S) + list(H)}
    for s in S:
        for h in nbH[s]:
            adj[s].add(h)
            adj[h].add(s)
    comps = []
    seen = set()
    for v in list(S) + list(H):
        if v in seen:
            continue
        col = {v: 0}
        stack = [v]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in col:
                    col[w] = 1 - col[u]
                    stack.append(w)
                elif col[w] == col[u]:
                    return []          # incidence graph not bipartite (impossible)
        seen |= set(col)
        comps.append(col)
    out = []
    for flips in product([0, 1], repeat=len(comps)):
        c = {}
        for fl, col in zip(flips, comps):
            for v, x in col.items():
                c[v] = x ^ fl
        out.append(c)
    return out


def forests_over(allowed, must_contain):
    """Every acyclic edge subset of `allowed` containing `must_contain`."""
    verts = sorted({v for e in allowed for v in e}, key=str)
    idx = {v: i for i, v in enumerate(verts)}
    base = [(idx[u], idx[v]) for (u, v) in must_contain]
    rest = [e for e in allowed if e not in must_contain]
    if not is_forest_edges(len(verts), base):
        return
    for r in range(len(rest) + 1):
        for sub in combinations(rest, r):
            E = base + [(idx[u], idx[v]) for (u, v) in sub]
            if is_forest_edges(len(verts), E):
                yield list(must_contain) + list(sub)


# ---------------- the search ----------------

def locate(S, H, nbH, hedges, P, Bs_union, A):
    """Inclusion-minimal X subseteq S with tau(G[H u X]) < |X|, plus its role."""
    best = None
    for k in range(1, len(S) + 1):
        for X in combinations(S, k):
            Xs = set(X)
            verts = set(H) | Xs
            E = [(s, h) for s in Xs for h in nbH[s]] + list(hedges)
            t, _ = tau_of(verts, E)
            if t < len(Xs):
                best = (Xs, t)
                break
        if best:
            break
    if best is None:
        return None, "NONE"
    Xs = best[0]
    Ps = set(P)
    role = []
    if Xs <= Ps:
        role.append("subset-of-P")
    if Xs <= set(Bs_union):
        role.append("subset-of-U")
    for s in P:
        if Xs <= (A[s] - {s}):
            role.append(f"subset-of-B_{s}")
            break
    if not role:
        role.append("mixed")
    return best, "/".join(role)


def analyse(S, H, nbH, cap, steiner, stats, witnesses):
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = C.feasible_selections(S, nbH, cap)
    if not sels:
        return
    forced, cycles = C.forced_and_cycles(S, sels)
    if not cycles:
        # POSITIVE CONTROL: acyclic-core systems must sometimes realise with
        # tau(G) = |S|, otherwise "no counterexample" would be an artefact of
        # the completion loop never producing a minimum-FVS instance at all.
        if stats["ctrl_systems"] < 300:
            stats["ctrl_systems"] += 1
            Hc = list(H) + [f"z{i}" for i in range(steiner)]
            c1c = sorted([h for h in H if cap[h] == 1])
            for col in colourings(S, H, nbH):
                for zc in product([0, 1], repeat=steiner):
                    cc = dict(col)
                    for i, x in enumerate(zc):
                        cc[f"z{i}"] = x
                    allowed = [(u, v) for u, v in combinations(Hc, 2)
                               if cc[u] != cc[v]]
                    must = []
                    if len(c1c) == 2:
                        if cc[c1c[0]] == cc[c1c[1]]:
                            continue
                        must = [tuple(c1c)]
                    for hedges in forests_over(allowed, must):
                        stats["ctrl_completions"] += 1
                        E = [(s, h) for s in S for h in nbH[s]] + list(hedges)
                        t, _ = tau_of(set(Hc) | set(S), E)
                        if t == len(S):
                            stats["ctrl_minFVS_hits"] += 1
        return
    stats["cyclic_systems"] += 1

    tights, _ = C.tight_sets(S, nbH, nbS, cap)
    comp = cycles[0]
    order = C.walk_cycle(comp, forced)
    P = [v[1] for v in order if v[0] == 'S']
    A = {}
    for s in P:
        cand = [X for X in tights if s in X]
        A[s] = min(cand, key=len)
    U = set().union(*[set(A[s]) - {s} for s in P]) if P else set()

    c1 = sorted([h for h in H if cap[h] == 1])
    Hx = list(H) + [f"z{i}" for i in range(steiner)]
    percap = [0]

    for col in colourings(S, H, nbH):
        # Steiner vertices are free to take either colour
        for zc in product([0, 1], repeat=steiner):
            cc = dict(col)
            for i, x in enumerate(zc):
                cc[f"z{i}"] = x
            allowed = [(u, v) for u, v in combinations(Hx, 2) if cc[u] != cc[v]]
            must = []
            if len(c1) == 2:
                if cc[c1[0]] == cc[c1[1]]:
                    continue                   # e cannot be an edge: skip
                must = [tuple(c1)]
            for hedges in forests_over(allowed, must):
                if percap[0] >= CAP:
                    stats["systems_hitting_completion_cap"] += 1
                    return
                percap[0] += 1
                stats["completions"] += 1
                verts = set(Hx) | set(S)
                E = [(s, h) for s in S for h in nbH[s]] + list(hedges)
                t, _ = tau_of(verts, E)
                if t == len(S):
                    stats["COUNTEREXAMPLES"] += 1
                    witnesses.append(("LEMMA-A-COUNTEREXAMPLE", list(S), Hx,
                                      {s: sorted(nbH[s]) for s in S},
                                      dict(cap), hedges, list(P)))
                    return
                stats[f"tau_deficit_{len(S)-t}"] += 1
                stats["seen"] += 1
                if stats["seen"] % 89 == 0 and stats["located"] < 3000:
                    stats["located"] += 1
                    b, role = locate(S, Hx, nbH, hedges, P, U, A)
                    if b:
                        stats["role:" + role] += 1
                        stats["viol_size:%d" % len(b[0])] += 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "exhaustive"
    stats = Counter()
    witnesses = []
    if mode == "exhaustive":
        mk = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        mp = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        st = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        gen = C.gen_exhaustive(mk, mp)
        label = f"exhaustive k<={mk} p<={mp} steiner={st}"
    else:
        t = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
        sd = int(sys.argv[3]) if len(sys.argv) > 3 else 4242
        st = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        gen = C.gen_random(t, sd)
        label = f"random {t} seed {sd} steiner={st}"
    n = 0
    for (S, H, nbH, cap) in gen:
        n += 1
        analyse(S, H, nbH, cap, st, stats, witnesses)
    print(f"[{label}] abstract systems = {n}")
    for k in sorted(stats):
        print(f"    {k} = {stats[k]}")
    if witnesses:
        print("*** LEMMA A-degree COUNTEREXAMPLE(S) FOUND ***")
        for w in witnesses[:3]:
            print("   ", w)
    else:
        print("    no counterexample: every forest completion of every cyclic "
              "system had tau(G) < |S|")


if __name__ == "__main__":
    main()
