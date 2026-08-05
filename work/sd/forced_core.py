"""Lemma A via the forced-core reformulation. A selected incidence edge is FORCED iff it
belongs to EVERY feasible incidence selection (deg 2 on S, capacities on H). By
the residual-augmentation lemma, forced <=> R3. So:
  Lemma A  <=>  FORCED-CORE FOREST: the graph of all forced edges is acyclic.
This is instance-level (per (G,S,e)), independent of any chosen state J.
Build the forced core per instance and check: acyclic (= Lemma A); forest; max
path length; component structure. Also A0: R3(in a state) == forced (spot-check).
"""
import sys, subprocess
from collections import defaultdict
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
from eval_L1_holdout import feasible

OUT = "forced-core.txt"
PROG = "forced-core-prog.txt"

def norm(J): return frozenset((min(a, b), max(a, b)) for a, b in J)

def cyclomatic(edges):
    deg = defaultdict(int); nodes = set()
    for (u, v) in edges: deg[u] += 1; deg[v] += 1; nodes |= {u, v}
    par = {v: v for v in nodes}
    def f(v):
        while par[v] != v: par[v] = par[par[v]]; v = par[v]
        return v
    c = 0
    for (u, v) in edges:
        ra, rb = f(u), f(v)
        if ra == rb: c += 1
        else: par[ra] = rb
    return c

def components_and_maxpath(edges):
    g = defaultdict(list)
    for (u, v) in edges: g[u].append(v); g[v].append(u)
    seen = set(); comps = []
    for v in list(g):
        if v in seen: continue
        st = [v]; cc = []
        while st:
            u = st.pop()
            if u in seen: continue
            seen.add(u); cc.append(u); st += g[u]
        comps.append(cc)
    # longest path (tree diameter) via double-BFS per component (valid if forest)
    def bfs_far(src):
        dist = {src: 0}; dq = [src]; far = src
        while dq:
            u = dq.pop(0)
            for w in g[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1; dq.append(w)
                    if dist[w] > dist[far]: far = w
        return far, dist[far]
    maxpath = 0
    for cc in comps:
        a, _ = bfs_far(cc[0]); _, d = bfs_far(a); maxpath = max(maxpath, d)
    return comps, maxpath

if __name__ == "__main__":
    open(OUT, "w").close(); open(PROG, "w").close()
    NN = sys.argv[1] if len(sys.argv) > 1 else '10'
    gs = subprocess.run(['geng', '-bc', '-q', NN], capture_output=True, text=True).stdout.split()
    n_inst = 0; cyclic_core = 0; noforced = 0
    maxpath_over = 0; nonforest = 0
    path_hist = defaultdict(int); comp_size_hist = defaultdict(int)
    fails = []
    gi = 0
    for g6 in gs:
        gi += 1
        if gi % 500 == 0:
            open(PROG, "a").write(f"g {gi}/{len(gs)} inst={n_inst} cyclic_core={cyclic_core} "
                                  f"nonforest={nonforest} maxpath={maxpath_over}\n")
        nn, adj = inv_b.parse_g6(g6); k = EB.tau(nn, adj)
        if k < 2: continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S); Hv = [v for v in range(nn) if v not in Sset]
            for (x, y) in [(u, w) for u in Hv for w in Hv if u < w and adj[u] >> w & 1]:
                feas = feasible(nn, adj, list(S), x, y)
                if not feas: continue
                n_inst += 1
                inter = None
                for J in feas:
                    nj = norm(J)
                    inter = nj if inter is None else (inter & nj)
                forced = list(inter)
                if not forced:
                    noforced += 1; comp_size_hist[0] += 1; continue
                cyc = cyclomatic(forced)
                if cyc > 0:
                    cyclic_core += 1
                    if len(fails) < 20: fails.append((g6, sorted(S), (x, y), sorted(map(tuple, forced))))
                comps, maxpath = components_and_maxpath(forced)
                if cyc == 0:
                    maxpath_over = max(maxpath_over, maxpath); path_hist[maxpath] += 1
                    for cc in comps: comp_size_hist[len(cc)] += 1
                else:
                    nonforest += 1
    with open(OUT, "a") as f:
        f.write(f"=== FORCED-CORE (Lemma A) n={NN} ===\n")
        f.write(f"instances = {n_inst}\n")
        f.write(f"CYCLIC forced core (= all-R3 cycle exists = Lemma A FAILS) = {cyclic_core}\n")
        f.write(f"instances with empty forced core = {noforced}\n")
        f.write(f"non-forest forced cores = {nonforest}\n")
        f.write(f"max forced-core path length (edges) over acyclic cores = {maxpath_over}\n")
        f.write(f"forced-core path-length histogram = {dict(sorted(path_hist.items()))}\n")
        f.write(f"forced-core component-size histogram = {dict(sorted(comp_size_hist.items()))}\n")
        if fails: f.write("CYCLIC-CORE witnesses (Lemma A failures):\n" + "\n".join(f"  {e}" for e in fails) + "\n")
    print(f"forced_core n={NN} DONE inst={n_inst} cyclic_core={cyclic_core} nonforest={nonforest} "
          f"maxpath={maxpath_over} noforced={noforced}")
