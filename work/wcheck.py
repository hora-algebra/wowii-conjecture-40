"""Independent re-verification of the three warning witnesses in tools/witnesses/.

Written from the model spec in paper section 3 / PROOFS.md A, sharing no code with
tools/*.py.  Recomputes, for each witness JSON: bipartiteness, H-forest-ness,
the full set of feasible selections, the forced core, its cycles, rho/delta and
the Hall-tight sets, the canonical carriers A_s and punctures B_s, and
tau(G[H u X]) for every X subseteq S (hereditary tightness profile).

Usage:  python3 wcheck.py <witness.json> [...]
"""
import json
import sys
from itertools import combinations, product


# ---------- elementary graph utilities (independent implementation) ----------

def components(vertices, edges):
    """Connected components of the graph (vertices, edges) as a list of sets."""
    adj = {v: set() for v in vertices}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    seen, out = set(), []
    for v in vertices:
        if v in seen:
            continue
        stack, comp = [v], set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(w for w in adj[u] if w not in comp)
        seen |= comp
        out.append(comp)
    return out


def is_forest(vertices, edges):
    """A graph is a forest iff |E| = |V| - #components."""
    es = {frozenset(e) for e in edges if e[0] in vertices and e[1] in vertices}
    return len(es) == len(vertices) - len(components(vertices, edges))


def two_colour(vertices, edges):
    """Return a proper 2-colouring dict, or None if the graph has an odd cycle."""
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    col = {}
    for r in vertices:
        if r in col:
            continue
        col[r] = 0
        stack = [r]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in col:
                    col[w] = 1 - col[u]
                    stack.append(w)
                elif col[w] == col[u]:
                    return None
    return col


def fvs_min(vertices, edges):
    """Minimum feedback vertex set size, by increasing-size brute force."""
    vs = list(vertices)
    for k in range(len(vs) + 1):
        for D in combinations(vs, k):
            keep = [v for v in vs if v not in set(D)]
            if is_forest(set(keep), edges):
                return k, set(D)
    raise AssertionError("unreachable")


# ---------- the incidence-selection model ----------

class Instance:
    def __init__(self, wit):
        self.S = list(wit["vertices"]["S"])
        self.H = list(wit["vertices"]["H"])
        self.inc = [tuple(p) for p in wit["incidence_edges_S_H"]]
        self.hedges = [tuple(p) for p in wit["H_forest_edges"]]
        self.e = tuple(wit["distinguished_edge"])
        c1 = set(wit["capacities"].get("c1_vertices", list(self.e)))
        self.cap = {h: (1 if h in c1 else 2) for h in self.H}
        self.nbrH = {s: sorted([h for (t, h) in self.inc if t == s], key=str)
                     for s in self.S}
        self.nbrS = {h: sorted([s for (s, g) in self.inc if g == h], key=str)
                     for h in self.H}
        self.V = self.S + self.H
        self.E = self.inc + self.hedges

    def induced_edges(self, X):
        """Edges of G induced on H u X (X subseteq S)."""
        keep = set(self.H) | set(X)
        return [(u, v) for (u, v) in self.E if u in keep and v in keep]

    def tau(self, X):
        """tau(G[H u X])."""
        keep = set(self.H) | set(X)
        return fvs_min(keep, self.induced_edges(X))[0]

    def feasible(self):
        """All feasible selections, as frozensets of incidences."""
        per = []
        for s in self.S:
            per.append(list(combinations(self.nbrH[s], 2)))
            if not per[-1]:
                return []
        out = []
        for choice in product(*per):
            load = {}
            sel = []
            for s, (a, b) in zip(self.S, choice):
                sel += [(s, a), (s, b)]
                load[a] = load.get(a, 0) + 1
                load[b] = load.get(b, 0) + 1
            if all(load.get(h, 0) <= self.cap[h] for h in self.H):
                out.append(frozenset(sel))
        return out

    def rho(self, X):
        return sum(min(self.cap[h], sum(1 for s in self.nbrS[h] if s in X))
                   for h in self.H)

    def delta(self, X):
        return self.rho(X) - 2 * len(X)

    def degX(self, h, X):
        return sum(1 for s in self.nbrS[h] if s in X)


def cycles_of(edges):
    """Cycle rank of the incidence graph given by `edges` (union-find)."""
    par = {}

    def find(v):
        par.setdefault(v, v)
        while par[v] != v:
            par[v] = par[par[v]]
            v = par[v]
        return v

    rank = 0
    for (u, v) in edges:
        a, b = find(u), find(v)
        if a == b:
            rank += 1
        else:
            par[a] = b
    return rank


def report(path):
    wit = json.load(open(path))
    I = Instance(wit)
    print("=" * 72)
    print(f"{wit['id']}  ({path})")
    print("=" * 72)

    col = two_colour(I.V, I.E)
    print(f"  bipartite                      : {col is not None}")
    print(f"  H induced forest               : {is_forest(set(I.H), I.hedges)}")
    print(f"  G connected                    : {len(components(I.V, I.E)) == 1}")

    feas = I.feasible()
    print(f"  #feasible selections           : {len(feas)}"
          f"   (json says {wit['feasible_selections']['count']})")
    assert feas, "no feasible selection"

    forced = set(feas[0])
    for J in feas[1:]:
        forced &= J
    forced = {(s, h) for (s, h) in forced}
    fr = cycles_of(sorted(forced, key=str))
    print(f"  |forced core|                  : {len(forced)}")
    print(f"  forced-core cycle rank         : {fr}   (0 = Lemma A holds here)")

    if "forced_cycle" in wit:
        fc = [tuple(x) for x in wit["forced_cycle"]["edges"]]
        allf = all((s, h) in forced for (s, h) in fc)
        print(f"  claimed forced cycle all forced: {allf}   {fc}")

    # Hall structure
    tight = [X for k in range(len(I.S) + 1) for X in map(set, combinations(I.S, k))
             if I.delta(X) == 0]
    mind = min(I.delta(set(X)) for k in range(len(I.S) + 1)
               for X in combinations(I.S, k))
    print(f"  min delta over all X           : {mind}  (>=0 == Hall feasible)")
    print(f"  Hall-tight sets                : "
          f"{sorted((sorted(map(str, X)) for X in tight), key=len)}")

    # canonical carriers for the forced-cycle S-side
    P = wit.get("vertices", {}).get("P_cycle_S_side") \
        or wit.get("vertices", {}).get("forced_cycle_S_side") \
        or wit.get("forced_cycle", {}).get("vertices", [])
    P = [p for p in P if p in I.S]
    for s in P:
        cand = [X for X in tight if s in X]
        A = min(cand, key=len)
        assert all(A <= Y for Y in cand), f"A_{s} not the unique minimum tight set"
        B = A - {s}
        print(f"  A_{s} = {sorted(map(str,A))}  B_{s} = {sorted(map(str,B))}"
              f"  B tight = {I.delta(B) == 0}"
              f"  tau(G[H u B_{s}]) = {I.tau(B)} vs |B_{s}| = {len(B)}")

    # hereditary tightness profile: all X with tau < |X|, inclusion-minimal first
    viol = []
    for k in range(len(I.S) + 1):
        for X in combinations(I.S, k):
            X = set(X)
            t = I.tau(X)
            if t < len(X):
                viol.append((len(X), sorted(map(str, X)), t))
    viol.sort()
    print(f"  hereditary-tightness violations: {len(viol)}")
    for (k, X, t) in viol[:6]:
        print(f"      X={X}  tau={t} < |X|={k}")
    print(f"  tau(G[H u S]) = {I.tau(set(I.S))}   |S| = {len(I.S)}"
          f"   => S is a minimum FVS of G: {I.tau(set(I.S)) == len(I.S)}")
    print()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
