"""Independent recomputation of the three Lemma-A warning witnesses (gauntlet step 1(iii)).

Written from the model spec in paper section 3 / PROOFS.md section D ONLY.
It shares no code with tools/ (no import of inv_b, experiment_b, eval_frozen, ...).
For each witness JSON it recomputes, from the raw vertex/edge lists:

  * H is a forest;
  * tau(G) and whether S is a minimum FVS of G;
  * every feasible selection (demand 2 per s, cap c(h)=2 except 1 on e's endpoints);
  * the forced core = intersection of all feasible selections, and its cycles;
  * tau(G[H u X]) for EVERY X subseteq S, hence the hereditary-tightness profile
    and the inclusion-minimal violating sets;
  * where those violations sit relative to P (the forced cycle's S-side) and to
    B_s (the punctured carrier), which is what each witness refutes.

Positive control : the abstract even-cycle system (Hall-feasible, forced core is a
                   cycle, hereditary tightness violated) must reproduce those three facts.
Negative control : a hereditarily tight instance built from a genuine minimum FVS
                   must have an ACYCLIC forced core (Lemma A holds there).
"""
import json, sys, itertools, os
from collections import defaultdict


# ---------------------------------------------------------------- graph basics
def has_cycle(verts, edges):
    """union-find over the induced subgraph on `verts`."""
    idx = {v: i for i, v in enumerate(verts)}
    par = list(range(len(verts)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for (u, v) in edges:
        if u not in idx or v not in idx:
            continue
        ru, rv = find(idx[u]), find(idx[v])
        if ru == rv:
            return True
        par[ru] = rv
    return False


def induced_edges(edges, verts):
    vs = set(verts)
    return [(u, v) for (u, v) in edges if u in vs and v in vs]


def tau(verts, edges):
    """minimum feedback vertex set size, brute force over subsets (small graphs)."""
    verts = list(verts)
    for k in range(len(verts) + 1):
        for D in itertools.combinations(verts, k):
            rest = [v for v in verts if v not in D]
            if not has_cycle(rest, induced_edges(edges, rest)):
                return k, set(D)
    raise AssertionError


# --------------------------------------------------------- the selection model
def feasible_selections(S, inc, cap):
    """inc: dict s -> list of H-neighbours. Every s picks 2 distinct; loads <= cap."""
    S = list(S)
    out = []
    choice = [list(itertools.combinations(sorted(inc[s]), 2)) for s in S]

    def rec(i, load, acc):
        if i == len(S):
            out.append(dict(acc))
            return
        for pair in choice[i]:
            if any(load[h] + 1 > cap.get(h, 2) for h in pair):
                continue
            for h in pair:
                load[h] += 1
            acc[S[i]] = pair
            rec(i + 1, load, acc)
            del acc[S[i]]
            for h in pair:
                load[h] -= 1

    rec(0, defaultdict(int), {})
    return out


def sel_edges(sel):
    return {(s, h) for s, pair in sel.items() for h in pair}


def cycles_of(sel):
    """cyclic components of the incidence graph of a selection (max degree 2)."""
    adj = defaultdict(set)
    for (s, h) in sel_edges(sel):
        adj[s].add(h)
        adj[h].add(s)
    seen, cyc = set(), []
    for v in list(adj):
        if v in seen:
            continue
        comp, stack, ne = set(), [v], 0
        while stack:
            w = stack.pop()
            if w in comp:
                continue
            comp.add(w)
            stack.extend(adj[w])
        for w in comp:
            ne += len(adj[w])
        ne //= 2
        seen |= comp
        if ne >= len(comp):          # component has a cycle (here: is a cycle)
            cyc.append(frozenset(comp))
    return cyc


# ------------------------------------------------------------------ the report
def analyse(name, S, H, inc_edges, h_edges, e, refutes, P=None, Bs=None):
    inc = defaultdict(list)
    for (s, h) in inc_edges:
        inc[s].append(h)
    allv = list(S) + list(H)
    alledges = [tuple(x) for x in inc_edges] + [tuple(x) for x in h_edges]
    cap = {h: 2 for h in H}
    cap[e[0]] = 1
    cap[e[1]] = 1

    print(f"\n=== {name} ===")
    print(f"refutes: {refutes}")
    hf = not has_cycle(H, induced_edges(alledges, H))
    print(f"  H is a forest                      : {hf}")
    tG, D = tau(allv, alledges)
    print(f"  tau(G) = {tG}, |S| = {len(S)}  ->  S is a minimum FVS: {tG == len(S)}"
          f"   (a minimum FVS found: {sorted(map(str, D))})")

    feas = feasible_selections(S, inc, cap)
    print(f"  feasible selections                : {len(feas)}")
    if not feas:
        return
    core = set.intersection(*[sel_edges(f) for f in feas])
    core_cyc = cycles_of({s: tuple(h for (t, h) in core if t == s) for s in S
                          if len([h for (t, h) in core if t == s]) == 2})
    print(f"  forced-core edges                  : {sorted(map(str, core))}")
    print(f"  forced-core CYCLES                 : {[sorted(map(str, c)) for c in core_cyc]}")

    # hereditary tightness for every X subseteq S
    viol = []
    for k in range(1, len(S) + 1):
        for X in itertools.combinations(sorted(S, key=str), k):
            vs = list(H) + list(X)
            t, _ = tau(vs, induced_edges(alledges, vs))
            if t < len(X):
                viol.append((set(X), t))
    minimal = [ (X, t) for (X, t) in viol
                if not any(Y < X for (Y, _) in viol) ]
    print(f"  hereditary tightness holds for all X subseteq S: {not viol}")
    for (X, t) in minimal:
        loc = []
        if P is not None:
            loc.append("subset of P" if X <= set(P) else
                       ("disjoint from P" if not (X & set(P)) else "meets P"))
        if Bs is not None:
            loc.append("subset of B_s" if X <= set(Bs) else
                       ("disjoint from B_s" if not (X & set(Bs)) else "meets B_s"))
        print(f"    inclusion-minimal violation X={sorted(map(str,X))} "
              f"tau(G[H u X])={t} < |X|={len(X)}   [{', '.join(loc)}]")
    if P is not None:
        vs = list(H) + list(P)
        t, Dp = tau(vs, induced_edges(alledges, vs))
        print(f"  tau(G[H u P]) = {t}  vs |P| = {len(P)}"
              f"  -> P {'IS' if t < len(P) else 'is NOT'} a violating set"
              f"   (FVS {sorted(map(str,Dp))})")
    if Bs is not None:
        vs = list(H) + list(Bs)
        t, Db = tau(vs, induced_edges(alledges, vs))
        print(f"  tau(G[H u B_s]) = {t} vs |B_s| = {len(Bs)}"
              f"  -> B_s {'IS' if t < len(Bs) else 'is NOT'} a violating set")
        degs = {u: len(inc[u]) for u in Bs}
        print(f"  incidence degrees on B_s           : {[(str(u), d) for u, d in degs.items()]}")


# ---------------------------------------------------------------- the controls
def control_even_cycle(m=3):
    """abstract even-cycle system: s_i ~ h_i, h_{i+1}; demand 2; cap 2; H edgeless."""
    S = [f"s{i}" for i in range(m)]
    H = [f"h{i}" for i in range(m)]
    inc_edges = [(f"s{i}", f"h{i}") for i in range(m)] + \
                [(f"s{i}", f"h{(i+1) % m}") for i in range(m)]
    # the abstract system has NO distinguished edge: every capacity stays 2, so
    # point the (x,y) clamp at a vertex that is not in H.
    analyse(f"POSITIVE CONTROL even-cycle system m={m}", S, H, inc_edges, [],
            ("__none__", "__none__"),
            "Hall feasibility alone: forced core IS a cycle, hereditary tightness FAILS")


def control_clean():
    """a hereditarily tight instance: G = two triangles?  no - bipartite.
    Take G = C_4 with a pendant path; S = {one C_4 vertex} is a minimum FVS."""
    # C6 with chords is easier: use K_{2,3} plus a pendant edge.
    # S = {s} (one side of K_{2,3}) is NOT enough for tau>=2, so build two blocks.
    S = ["s", "t"]
    H = ["h1", "h2", "h3", "h4", "p", "q"]
    inc_edges = [("s", "h1"), ("s", "h2"), ("s", "h3"),
                 ("t", "h2"), ("t", "h3"), ("t", "h4")]
    h_edges = [("h1", "p"), ("p", "h2"), ("h3", "q"), ("q", "h4")]
    analyse("NEGATIVE CONTROL hereditarily tight instance", S, H, inc_edges, h_edges,
            ("h1", "p"),
            "expected: S a minimum FVS, hereditary tightness HOLDS, forced core ACYCLIC")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    wdir = os.path.join(here, "..", "..", "tools", "witnesses")
    spec = {
        "O-56": dict(P=[0, 1], Bs=None),
        "O-63": dict(P=["s", "t"], Bs=["u", "a", "b"]),
        "O-64": dict(P=["s", "t"], Bs=["u"]),
    }
    for wid, extra in spec.items():
        d = json.load(open(os.path.join(wdir, wid + ".json")))
        v = d["vertices"]
        S = v["S"]
        H = v["H"]
        analyse(wid, S, H, d["incidence_edges_S_H"], d["H_forest_edges"],
                tuple(d["distinguished_edge"]), d["refutes"], **extra)
    control_even_cycle(3)
    control_even_cycle(4)
    control_clean()
