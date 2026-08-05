"""Independent re-verification of the six SD-SHORT / A1 failures at n=11
(PREREG-SD.md §4.4), plus the in-sample one-step-lookahead probe SD-LOOK2.

Independence: this file does NOT use a1_verify's residual BFS, DAG, or path
enumeration. It enumerates every feasible selection directly and works in the
SYMMETRIC-DIFFERENCE metric

    m(J, J') = |J symdiff J'|

which is tied to the frozen engine's residual-path length by the proved
residual-augmentation theorem (PROOFS.md C4): a toggle releasing an avoidable
incidence a along a residual augmenting path Q of length d yields
J' = J symdiff ({a} u E(Q)) with a not in E(Q), hence m(J, J') = d + 1. So the
frozen d0(C) and the quantity below must satisfy  m_min = d0 + 1.

Checks per witness:
  1. H = G - S is a forest, and tau(G) = |S|  (S is a minimum FVS);
  2. hereditary FVS tightness tau(G[H u X]) = |X| for EVERY X subseteq S;
  3. J is feasible and its selected cycles are exactly the recorded ones;
  4. m_min over feasible J' omitting an incidence of C, and whether ANY such
     minimiser is CES for C          -> independent A1 / SD-SHORT verdict;
  5. the smallest m at which a CES J' appears -> independent B-PLUS-2 gap;
  6. SD-LOOK2 (IN SAMPLE at n=11): from a minimising non-CES J', does J' itself
     admit a minimising CES toggle for one of ITS cycles?
"""
import sys, json, itertools
from collections import defaultdict
sys.path.insert(0, '.')
import inv_b            # graph6 parsing only


# ------------------------------------------------------------ graph utilities
def has_cycle(verts, edges):
    idx = {v: i for i, v in enumerate(verts)}
    par = list(range(len(verts)))

    def find(a):
        while par[a] != a:
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


def edges_of(adj, n):
    return [(u, v) for u in range(n) for v in range(u + 1, n) if adj[u] >> v & 1]


def induced(edges, verts):
    vs = set(verts)
    return [(u, v) for (u, v) in edges if u in vs and v in vs]


def tau(verts, edges):
    verts = list(verts)
    for k in range(len(verts) + 1):
        for D in itertools.combinations(verts, k):
            rest = [v for v in verts if v not in D]
            if not has_cycle(rest, induced(edges, rest)):
                return k
    raise AssertionError


# ----------------------------------------------------------- selection model
def all_feasible(n, adj, S, Hv, x, y):
    cap = {h: 2 for h in Hv}
    cap[x] = 1
    cap[y] = 1
    Sl = sorted(S)
    opts = []
    for s in Sl:
        nb = [h for h in Hv if adj[s] >> h & 1]
        o = list(itertools.combinations(nb, 2))
        if not o:
            return []
        opts.append(o)
    out = []
    load = defaultdict(int)
    acc = []

    def rec(i):
        if i == len(Sl):
            # normalise each incidence to (min, max): the recorded witnesses
            # store edges vertex-sorted, not (s, h)-ordered.
            out.append(frozenset((min(u, v), max(u, v)) for (u, v) in acc))
            return
        for (h1, h2) in opts[i]:
            if load[h1] >= cap[h1] or load[h2] >= cap[h2]:
                continue
            load[h1] += 1
            load[h2] += 1
            acc.append((Sl[i], h1))
            acc.append((Sl[i], h2))
            rec(i + 1)
            acc.pop()
            acc.pop()
            load[h1] -= 1
            load[h2] -= 1
    rec(0)
    return out


def cycles_of(J, x, y):
    """cyclic components of J u {e}; max degree 2 so each component is a path or a cycle."""
    g = defaultdict(list)
    for (u, v) in list(J) + [(x, y)]:
        g[u].append(v)
        g[v].append(u)
    seen, res = set(), set()
    for s0 in list(g):
        if s0 in seen:
            continue
        comp, st = [], [s0]
        while st:
            u = st.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.append(u)
            st += g[u]
        if sum(len(g[u]) for u in comp) // 2 == len(comp):
            res.add(frozenset(comp))
    return res


def report(w):
    g6, S, (x, y) = w['g6'], set(w['S']), w['e']
    n, adj = inv_b.parse_g6(g6)
    E = edges_of(adj, n)
    Hv = [v for v in range(n) if v not in S]
    J = frozenset((min(z), max(z)) for z in w['J'])
    print(f"\n--- {g6}  S={sorted(S)}  e=({x},{y}) ---")
    print(f"  H is a forest                : {not has_cycle(Hv, induced(E, Hv))}")
    tG = tau(range(n), E)
    print(f"  tau(G) = {tG}, |S| = {len(S)} -> S minimum FVS : {tG == len(S)}")
    ht = all(tau(list(Hv) + list(X), induced(E, list(Hv) + list(X))) == len(X)
             for k in range(1, len(S) + 1) for X in itertools.combinations(sorted(S), k))
    print(f"  hereditary FVS tightness     : {ht}")

    feas = all_feasible(n, adj, S, Hv, x, y)
    print(f"  feasible selections          : {len(feas)}")
    assert J in feas, "recorded J is not feasible under the independent enumerator"
    Jcyc = cycles_of(J, x, y)
    print(f"  selected cycles of J         : {[sorted(c) for c in Jcyc]}  (count {len(Jcyc)})")
    assert len(Jcyc) == 1
    C = next(iter(Jcyc))
    Cinc = [(u, v) for (u, v) in J if u in C and v in C]

    # m_min over feasible J' omitting some incidence of C
    cand = [Jp for Jp in feas if any(a not in Jp for a in Cinc)]
    mmin = min(len(J ^ Jp) for Jp in cand)
    minis = [Jp for Jp in cand if len(J ^ Jp) == mmin]
    ces = [Jp for Jp in minis if C not in cycles_of(Jp, x, y)
           and cycles_of(Jp, x, y) <= Jcyc]
    print(f"  m_min = {mmin}  (= d0+1, so independent d0 = {mmin-1});"
          f" minimisers = {len(minis)}; CES among them = {len(ces)}"
          f"   -> A1/SD-SHORT {'HOLDS' if ces else 'FAILS'}")

    allces = [Jp for Jp in feas if C not in cycles_of(Jp, x, y)
              and cycles_of(Jp, x, y) <= Jcyc and Jp != J]
    mces = min(len(J ^ Jp) for Jp in allces) if allces else None
    print(f"  smallest m with a CES J'     : {mces}  -> independent gap "
          f"= {mces - mmin if mces else None} (frozen engine reports gap 2)")

    # SD-LOOK2, IN SAMPLE at n=11: after a minimising non-CES step, is the next
    # minimising step CES for one of the new selection's cycles?
    ok, tot = 0, 0
    for Jp in minis:
        Jpc = cycles_of(Jp, x, y)
        if not Jpc:
            ok += 1
            tot += 1
            continue
        tot += 1
        good = False
        for C2 in Jpc:
            C2inc = [(u, v) for (u, v) in Jp if u in C2 and v in C2]
            c2 = [K for K in feas if any(a not in K for a in C2inc)]
            if not c2:
                continue
            m2 = min(len(Jp ^ K) for K in c2)
            if any(C2 not in cycles_of(K, x, y) and cycles_of(K, x, y) <= Jpc
                   for K in c2 if len(Jp ^ K) == m2):
                good = True
        ok += 1 if good else 0
    print(f"  SD-LOOK2 (in sample): {ok}/{tot} minimising first steps are followed"
          f" by a minimising CES second step")
    return dict(g6=g6, mmin=mmin, d0=mmin - 1, ces_at_mmin=len(ces),
                m_first_ces=mces, gap=(mces - mmin) if mces else None,
                look2=f"{ok}/{tot}", ncyc=len(Jcyc), hered=ht, minfvs=(tG == len(S)))


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else 'sd-n11-AGGREGATE.json'
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    agg = json.load(open(src))
    ws = agg['witnesses']['SD-SHORT']
    # deterministic evenly-spaced sample, so the choice cannot be cherry-picked
    step = max(1, len(ws) // lim)
    sample = ws[::step][:lim]
    print(f"# re-verifying {len(sample)} of {len(ws)} recorded SD-SHORT failures"
          f" from {src} (every {step}th)")
    out = [report(w) for w in sample]
    json.dump(out, open(src.replace('AGGREGATE', 'REVERIFY'), 'w'), indent=1)
    print("\nsummary:", json.dumps(out, indent=1))
