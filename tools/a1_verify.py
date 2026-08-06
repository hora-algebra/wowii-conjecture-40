"""Independent step 1: freeze + verify A1.
A1: for every selected cycle C, let d = min residual augmenting-path length over
all avoidable edges of C; among the shortest (length-d) edge/path pairs, at least
one is CES (toggle destroys C, creates no new cycle).

This is a FRESH implementation via an alternating residual BFS / shortest-path
DAG + explicit shortest-path enumeration + fresh toggle + fresh cycle counting.
It does NOT use the nbrs one-move engine that selector_exp used, so agreement
between the two is a genuine dual-check of A1. Also independently verifies each
cycle's CES shortest witness end to end.
"""
import sys, subprocess
from collections import defaultdict, deque
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
from eval_L1_holdout import feasible, comps, ncyc
from mine_n10 import walk_cycle

OUT = "a1-verify.txt"
PROG = "a1-verify-prog.txt"
PATHCAP = 4000

def norm(J): return frozenset((min(a, b), max(a, b)) for a, b in J)

def cyc_sets_edges(edges, x, y):
    g = defaultdict(list)
    for (u, v) in list(edges) + [(x, y)]: g[u].append(v); g[v].append(u)
    seen = set(); res = set()
    for s0 in list(g):
        if s0 in seen: continue
        comp = []; st = [s0]
        while st:
            u = st.pop()
            if u in seen: continue
            seen.add(u); comp.append(u); st += g[u]
        if sum(len(g[u]) for u in comp) // 2 == len(comp): res.add(frozenset(comp))
    return res

def residual_dag(nn, adj, Sset, x, y, J, a, s):
    """Alternating residual BFS after deleting a. Returns (d, forward, term_d)
    or None if no augmenting path (a is R3). Fresh, independent of nbrs."""
    M = set(norm(J)); M.discard(a)
    cap = {h: 2 for h in range(nn) if h not in Sset}; cap[x] = 1; cap[y] = 1
    degM = defaultdict(int)
    for (u, v) in M: degM[u] += 1; degM[v] += 1
    dist = {s: 0}; dq = deque([s]); forward = defaultdict(list); terminals = {}
    while dq:
        u = dq.popleft(); du = dist[u]
        if u in Sset:                       # S: outgoing UNMATCHED edges to H
            for w in range(nn):
                if w in Sset or not (adj[u] >> w & 1): continue
                e = (min(u, w), max(u, w))
                if e in M or e == a: continue
                if w not in dist: dist[w] = du + 1; dq.append(w)
                if dist[w] == du + 1: forward[u].append(w)
        else:                               # H: terminal if residual capacity
            if degM[u] < cap[u]: terminals[u] = du
            for z in range(nn):             # continue via MATCHED edges to S
                if z not in Sset or not (adj[z] >> u & 1): continue
                e = (min(z, u), max(z, u))
                if e not in M or e == a: continue
                if z not in dist: dist[z] = du + 1; dq.append(z)
                if dist[z] == du + 1: forward[u].append(z)
    if not terminals: return None
    d = min(terminals.values())
    term_d = {t for t, dd in terminals.items() if dd == d}
    return d, forward, term_d

def enum_shortest_paths(forward, s, term_d, d, cap=PATHCAP):
    paths = []
    def dfs(u, path):
        if len(paths) >= cap: return
        if len(path) - 1 == d:
            if u in term_d: paths.append(list(path))
            return
        for w in forward.get(u, ()):
            if w in path: continue
            path.append(w); dfs(w, path); path.pop()
    dfs(s, [s])
    return paths

def toggle(J, a, path):
    M = set(norm(J)); M.discard(a)
    pe = set((min(path[i], path[i+1]), max(path[i], path[i+1])) for i in range(len(path)-1))
    return frozenset(M ^ pe)

def indep_feasible(nn, adj, Sset, x, y, J):
    dS = defaultdict(int); dH = defaultdict(int)
    for (u, v) in J:
        aa, bb = (u, v) if u in Sset else (v, u)
        if aa not in Sset or bb in Sset or not (adj[aa] >> bb & 1): return False
        dS[aa] += 1; dH[bb] += 1
    if any(dS[t] != 2 for t in Sset): return False
    cap = {h: 2 for h in range(nn) if h not in Sset}; cap[x] = 1; cap[y] = 1
    return all(dH[h] <= cap.get(h, 0) for h in dH)

if __name__ == "__main__":
    open(OUT, "w").close(); open(PROG, "w").close()
    NN = sys.argv[1] if len(sys.argv) > 1 else '10'
    gs = subprocess.run(['geng', '-bc', '-q', NN], capture_output=True, text=True).stdout.split()
    n_cyc = 0; a1_ok = 0; a1_fail = 0; wit_fail = 0; capped = 0
    fails = []
    gi = 0
    for g6 in gs:
        gi += 1
        if gi % 100 == 0:
            open(PROG, "a").write(f"g {gi}/{len(gs)} cyc={n_cyc} A1ok={a1_ok} A1fail={a1_fail} "
                                  f"witfail={wit_fail} capped={capped}\n")
        nn, adj = inv_b.parse_g6(g6); k = EB.tau(nn, adj)
        if k < 2: continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S); Hv = [v for v in range(nn) if v not in Sset]
            for (x, y) in [(u, w) for u in Hv for w in Hv if u < w and adj[u] >> w & 1]:
                feas = feasible(nn, adj, list(S), x, y)
                if not feas: continue
                P = {J: ncyc(J, (x, y)) for J in feas}
                for J in feas:
                    if P[J] == 0: continue
                    Jcyc = cyc_sets_edges(norm(J), x, y)
                    for (cc, iscy) in comps(J, (x, y)):
                        if not iscy: continue
                        n_cyc += 1
                        Ccc = frozenset(cc)
                        order, has_e = walk_cycle(cc, J, x, y)
                        cyc_edges = [ed for (kk, ed) in order if kk == 'J']
                        # d_a per avoidable edge (fresh residual BFS)
                        per = {}
                        for ed in cyc_edges:
                            an = (min(ed), max(ed)); s = ed[0] if ed[0] in Sset else ed[1]
                            dag = residual_dag(nn, adj, Sset, x, y, J, an, s)
                            if dag is None: continue            # R3 edge
                            per[an] = (s, dag)
                        if not per:
                            a1_fail += 1                        # would violate Lemma A too
                            if len(fails) < 20: fails.append((g6, sorted(Sset), (x, y), sorted(cc), "no-avoidable"))
                            continue
                        d_min = min(dag[0] for (s, dag) in per.values())
                        # among edges attaining d_min, is any shortest path CES?
                        found = False; this_capped = False; wit = None
                        for an, (s, (d, forward, term_d)) in per.items():
                            if d != d_min: continue
                            paths = enum_shortest_paths(forward, s, term_d, d)
                            if len(paths) >= PATHCAP: this_capped = True
                            for path in paths:
                                Jp = toggle(J, an, path)
                                Jpc = cyc_sets_edges(Jp, x, y)
                                if Ccc not in Jpc and Jpc <= Jcyc:     # CES
                                    found = True; wit = (an, s, path, Jp, d); break
                            if found: break
                        if found:
                            a1_ok += 1
                            # independent full verify of the witness
                            an, s, path, Jp, d = wit
                            t = path[-1]
                            ok = (indep_feasible(nn, adj, Sset, x, y, Jp)
                                  and an not in Jp
                                  and t not in Sset and path[0] == s
                                  and len(set(path)) == len(path)
                                  and Ccc not in cyc_sets_edges(Jp, x, y)
                                  and cyc_sets_edges(Jp, x, y) <= Jcyc)
                            if not ok: wit_fail += 1
                        else:
                            if this_capped: capped += 1
                            else:
                                a1_fail += 1
                                if len(fails) < 20:
                                    fails.append((g6, sorted(Sset), (x, y), sorted(cc),
                                                  sorted(sorted(z) for z in J), d_min))
    with open(OUT, "a") as f:
        f.write(f"=== A1 INDEPENDENT VERIFY (n={NN}) ===\n")
        f.write(f"cycle_components = {n_cyc}\n")
        f.write(f"A1 holds (some globally-shortest residual path is CES) = {a1_ok}/{n_cyc}\n")
        f.write(f"A1 failures = {a1_fail}\n")
        f.write(f"witness independent full-verify failures = {wit_fail}\n")
        f.write(f"cycles hitting path-enum cap ({PATHCAP}) with no CES found = {capped}\n")
        if fails: f.write("failures:\n" + "\n".join(f"  {e}" for e in fails) + "\n")
    print(f"a1_verify n={NN} DONE A1={a1_ok}/{n_cyc} fail={a1_fail} witfail={wit_fail} capped={capped}")
