"""engine0520 — independent re-implementation of the incidence-selection layer.

Written from the definitions in proofs/PROOFS.md (sections A, C5, C5b, C6, D)
for attempt/2026-08-05-claude-opus-5-0520.  It shares NO predicate code with
work/carrier.py, work/carrier_poset.py (b17e) or work/wcheck.py.  Deliberate
implementation differences, so that agreement is evidence:

  * feasible selections      : explicit backtracking with live capacity loads
                               (carrier.py filters a full itertools.product).
  * forcedness of (s,h)      : re-solve feasibility with (s,h) FORBIDDEN
                               (the definition + C4); carrier.py intersects all
                               feasible selections.
  * canonical carrier A_s    : INTERSECTION of every Hall-tight set containing s
                               (legitimate by the C6 lattice), then verified
                               tight; carrier.py takes the minimum by size and
                               then checks minimality.
  * minimum FVS tau(.)       : increasing-size brute force with an explicit
                               cycle test.

The universe generator gen_exhaustive is re-derived from the documented
contract of carrier.py (|S| = k in 2..maxK, |H| = p in 3..maxP, each s carries
2..4 incidences, every H-vertex carries at least one incidence, capacities all
2 or exactly two chosen vertices at capacity 1) and is anchored against the
published counts before use.
"""
import sys
from itertools import combinations, product


# ---------------------------------------------------------------- Hall layer

def rho(X, nbS, cap):
    """rho(X) = sum_h min(c(h), deg_X(h))."""
    X = frozenset(X)
    return sum(min(cap[h], len(nbS[h] & X)) for h in cap)


def delta(X, nbS, cap):
    return rho(X, nbS, cap) - 2 * len(frozenset(X))


def all_subsets(S):
    S = list(S)
    for k in range(len(S) + 1):
        for X in combinations(S, k):
            yield frozenset(X)


def tight_sets(S, nbS, cap):
    """(list of Hall-tight subsets, min delta over all subsets)."""
    out, mind = [], None
    for X in all_subsets(S):
        d = delta(X, nbS, cap)
        if mind is None or d < mind:
            mind = d
        if d == 0:
            out.append(X)
    return out, mind


def feasible_selections(S, nbH, cap, forbid=frozenset(), limit=None):
    """Every feasible selection, as a dict s -> (h1,h2).  Backtracking."""
    S = list(S)
    load = {h: 0 for h in cap}
    choice, out = {}, []

    def rec(i):
        if limit is not None and len(out) >= limit:
            return
        if i == len(S):
            out.append(dict(choice))
            return
        s = S[i]
        opts = sorted(nbH[s])
        for ai in range(len(opts)):
            a = opts[ai]
            if (s, a) in forbid or load[a] >= cap[a]:
                continue
            load[a] += 1
            for bi in range(ai + 1, len(opts)):
                b = opts[bi]
                if (s, b) in forbid or load[b] >= cap[b]:
                    continue
                load[b] += 1
                choice[s] = (a, b)
                rec(i + 1)
                load[b] -= 1
                if limit is not None and len(out) >= limit:
                    break
            load[a] -= 1
            if limit is not None and len(out) >= limit:
                return
    rec(0)
    return out


def is_feasible(S, nbH, cap, forbid=frozenset()):
    return bool(feasible_selections(S, nbH, cap, forbid=forbid, limit=1))


def forced_incidences(S, nbH, cap):
    """(s,h) is forced iff NO feasible selection omits it.  Definition + C4."""
    forced = set()
    for s in S:
        for h in nbH[s]:
            if not is_feasible(S, nbH, cap, forbid=frozenset({(s, h)})):
                forced.add((s, h))
    return frozenset(forced)


def forced_core_cycles(forced):
    """Cyclic components of the forced core, each returned in cyclic order
    [('S',s1),('H',q1),('S',s2),...].  Max degree is 2 in the forced core
    (demand 2 at every s, capacity <= 2 at every h), so a component is cyclic
    iff #edges == #vertices."""
    adj = {}
    for (s, h) in forced:
        adj.setdefault(('S', s), set()).add(('H', h))
        adj.setdefault(('H', h), set()).add(('S', s))
    seen, cycles = set(), []
    for v in sorted(adj, key=repr):
        if v in seen:
            continue
        comp, stack = [], [v]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.append(u)
            stack.extend(adj[u])
        nedge = sum(len(adj[u]) for u in comp) // 2
        if nedge != len(comp):
            continue
        # walk the cycle
        start = comp[0]
        order, prev, cur = [start], None, start
        while True:
            nxt = [w for w in adj[cur] if w != prev]
            nxt = nxt[0] if len(nxt) == 1 else [w for w in nxt if w != prev][0]
            if nxt == start:
                break
            order.append(nxt)
            prev, cur = cur, nxt
        cycles.append(order)
    return cycles


def canonical_carrier(s, tights):
    """A_s = intersection of every Hall-tight set containing s.

    By the C6 lattice the tight sets are closed under intersection, so this
    intersection is itself tight and is THE unique inclusion-minimum tight set
    containing s.  Returns None if no tight set contains s."""
    cand = [X for X in tights if s in X]
    if not cand:
        return None
    A = cand[0]
    for X in cand[1:]:
        A = A & X
    return A


# ------------------------------------------------------- realised-graph layer

def induced_graph(H_edges, H_vertices, nbH, X):
    """Adjacency of G[H u X]: the H-forest plus incidences of X (S-S edges are
    not part of the abstract model and are passed in H_edges if present)."""
    adj = {v: set() for v in H_vertices}
    for x in X:
        adj[x] = set()
    for (u, v) in H_edges:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    for x in X:
        for h in nbH[x]:
            if h in adj:
                adj[x].add(h)
                adj[h].add(x)
    return adj


def has_cycle(adj):
    seen = set()
    for root in adj:
        if root in seen:
            continue
        stack = [(root, None)]
        seen.add(root)
        parent = {root: None}
        while stack:
            u, p = stack.pop()
            for w in adj[u]:
                if w == p:
                    continue
                if w in seen:
                    return True
                seen.add(w)
                parent[w] = u
                stack.append((w, u))
    return False


def tau(adj):
    """Minimum feedback vertex set size, brute force by increasing size."""
    verts = sorted(adj, key=repr)
    if not has_cycle(adj):
        return 0
    for k in range(1, len(verts) + 1):
        for D in combinations(verts, k):
            Ds = set(D)
            sub = {v: (adj[v] - Ds) for v in verts if v not in Ds}
            if not has_cycle(sub):
                return k
    return len(verts)


def tau_induced(H_edges, H_vertices, nbH, X):
    return tau(induced_graph(H_edges, H_vertices, nbH, X))


# ------------------------------------------------------------ universe

def gen_exhaustive(maxK, maxP):
    """Re-derivation of carrier.py's documented universe contract."""
    for p in range(3, maxP + 1):
        H = list(range(p))
        opts = [frozenset(c) for r in (2, 3, 4) if r <= p
                for c in combinations(H, r)]
        for k in range(2, maxK + 1):
            S = [f"s{i}" for i in range(k)]
            for combo in product(opts, repeat=k):
                if len(frozenset().union(*combo)) < p:
                    continue
                nbH = dict(zip(S, combo))
                for c1 in [()] + [(a, b) for a in H for b in H if a < b]:
                    cap = {h: (1 if h in c1 else 2) for h in H}
                    yield (S, H, nbH, cap)


def analyse(S, H, nbH, cap):
    """Full carrier analysis of one abstract system, or None if it is
    infeasible or its forced core is acyclic."""
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    if not is_feasible(S, nbH, cap):
        return None
    forced = forced_incidences(S, nbH, cap)
    cycles = forced_core_cycles(forced)
    if not cycles:
        return None
    tights, _ = tight_sets(S, nbS, cap)
    return dict(S=S, H=H, nbH=nbH, cap=cap, nbS=nbS, forced=forced,
                cycles=cycles, tights=tights)


def cycle_data(res, order):
    """P, Q, carriers, punctures, U for one forced cycle, in cyclic order."""
    P = [v[1] for v in order if v[0] == 'S']
    Q = [v[1] for v in order if v[0] == 'H']
    A = {s: canonical_carrier(s, res['tights']) for s in P}
    B = {s: (A[s] - {s}) for s in P}
    U = frozenset().union(*B.values()) if P else frozenset()
    ends = {}
    L = len(order)
    for i, v in enumerate(order):
        if v[0] == 'S':
            ends[v[1]] = (order[(i - 1) % L][1], order[(i + 1) % L][1])
    return P, Q, A, B, U, ends


if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "anchor":
        mk = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        mp = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        nsys = ncyc = npdis = 0
        for (S, H, nbH, cap) in gen_exhaustive(mk, mp):
            nsys += 1
            res = analyse(S, H, nbH, cap)
            if res is None:
                continue
            ncyc += 1
            hit = False
            for order in res['cycles']:
                P, Q, A, B, U, ends = cycle_data(res, order)
                if set(P) & set(U):
                    hit = True
            if hit:
                npdis += 1
        print(f"ANCHOR systems={nsys} cyclic={ncyc} pdis={npdis}")
