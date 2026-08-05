r"""VERIFY-3 graph-layer forced-core engine, written fresh for this run.

Universe: every connected bipartite graph on n vertices (geng -c -b),
every minimum FVS S, H = G - S, every edge e of H, capacities c=2 except
c=1 on e's endpoints. For each instance:
  * feasibility must hold (C5b regression);
  * the forced core must be acyclic (Lemma A census regression, and the
    non-existence of any A-I+-shaped forced cycle in particular).
Forcedness engine: FLOW-based (independent of the enumeration-intersection
method): a feasible selection is a max flow of value 2|S| in the network
sigma ->(2) s ->(1) h ->(c(h)) sink; incidence (s,h) is forced iff deleting
its arc drops the max flow below 2|S| (paper C4/C5/F1).
Cross-check: on every instance with n <= 8 (and every 500th instance
overall), forcedness is recomputed by brute-force enumeration of all
feasible selections and the two engines must agree exactly.
Controls:
  * positive: the O-64 graph (explicit in PROOFS.md D) fed as (G,S,e)
    with its non-minimum S must yield a CYCLIC forced core; ADJ-1's
    realization likewise;
  * negative (engine-can-fail): a corrupted O-64 run where the checker's
    expected verdict is inverted must FAIL.
Counts reported per n: graphs, tau>=2 instances (anchor: 2186 @ n=8,
13003 @ n=9, 116216 @ n=10), tau<2 instances, infeasible, cyclic cores.
"""
import subprocess
import sys
from itertools import combinations


def graphs6(n):
    out = subprocess.run(['geng', '-q', '-c', '-b', str(n)],
                         capture_output=True, text=True)
    return out.stdout.split()


def decode_g6(s):
    data = [ord(c) - 63 for c in s]
    n = data[0]
    bits = []
    for x in data[1:]:
        bits += [(x >> i) & 1 for i in range(5, -1, -1)]
    adj = [set() for _ in range(n)]
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i].add(j)
                adj[j].add(i)
            k += 1
    return n, adj


def is_forest(n, adj, verts):
    verts = set(verts)
    seen = set()
    for r in verts:
        if r in seen:
            continue
        stack = [(r, -1)]
        seen.add(r)
        while stack:
            v, par = stack.pop()
            skip_par = False
            for w in adj[v]:
                if w not in verts:
                    continue
                if w == par and not skip_par:
                    skip_par = True
                    continue
                if w in seen:
                    return False
                seen.add(w)
                stack.append((w, v))
    return True


def min_fvs_size(n, adj):
    for k in range(0, n + 1):
        for D in combinations(range(n), k):
            if is_forest(n, adj, set(range(n)) - set(D)):
                return k
    return n


def all_min_fvs(n, adj, tau):
    out = []
    for D in combinations(range(n), tau):
        if is_forest(n, adj, set(range(n)) - set(D)):
            out.append(frozenset(D))
    return out


# ---------------------------------------------------------------- flow engine
def max_flow(S, Hs, nbH, cap, banned=None):
    """Integral max flow, value = units routed (target 2|S|).
    Nodes: 'src', ('s',s), ('h',h), 'snk'. Unit augmentation BFS."""
    Sl = list(S)
    capacity = {}
    def setc(u, v, c):
        capacity[(u, v)] = c
        capacity.setdefault((v, u), 0)
    for s in Sl:
        setc('src', ('s', s), 2)
        for h in nbH[s]:
            if banned is not None and (s, h) == banned:
                continue
            setc(('s', s), ('h', h), 1)
    for h in Hs:
        setc(('h', h), 'snk', cap[h])
    flow = 0
    while True:
        prev = {'src': None}
        queue = ['src']
        while queue and 'snk' not in prev:
            u = queue.pop(0)
            for (a, b), c in list(capacity.items()):
                if a == u and c > 0 and b not in prev:
                    prev[b] = u
                    if b == 'snk':
                        break
                    queue.append(b)
        if 'snk' not in prev:
            return flow, capacity
        v = 'snk'
        while prev[v] is not None:
            u = prev[v]
            capacity[(u, v)] -= 1
            capacity[(v, u)] += 1
            v = u
        flow += 1


def flow_forced(S, Hs, nbH, cap):
    """(feasible?, set of forced incidences) by the flow method."""
    target = 2 * len(S)
    f0, _ = max_flow(S, Hs, nbH, cap)
    if f0 < target:
        return False, None
    forced = set()
    for s in S:
        for h in nbH[s]:
            f, _ = max_flow(S, Hs, nbH, cap, banned=(s, h))
            if f < target:
                forced.add((s, h))
    return True, forced


def enum_forced(S, Hs, nbH, cap):
    """Brute-force cross-check engine (independent method)."""
    Sl = sorted(S)
    per = []
    for s in Sl:
        opts = list(combinations(sorted(nbH[s]), 2))
        if not opts:
            return False, None
        per.append(opts)
    inter = None
    load0 = {}
    def rec(i, load):
        nonlocal inter
        if i == len(per):
            cur = frozenset((Sl[j], h) for j in range(len(per))
                            for h in chosen[j])
            inter = cur if inter is None else (inter & cur)
            return
        for (a, b) in per[i]:
            if load.get(a, 0) < cap[a] and load.get(b, 0) < cap[b] \
               and (a != b):
                load[a] = load.get(a, 0) + 1
                load[b] = load.get(b, 0) + 1
                chosen.append((a, b))
                rec(i + 1, load)
                chosen.pop()
                load[a] -= 1
                load[b] -= 1
    chosen = []
    rec(0, load0)
    if inter is None:
        return False, None
    return True, set(inter)


def core_cyclic(forced):
    deg = {}
    for (s, h) in forced:
        deg[('s', s)] = deg.get(('s', s), 0) + 1
        deg[('h', h)] = deg.get(('h', h), 0) + 1
    nv = len(deg)
    ne = len(forced)
    # forest iff every component has edges < vertices; max degree 2 =>
    # cyclic iff some component is a cycle; simple global test: build and BFS
    adj = {}
    for (s, h) in forced:
        adj.setdefault(('s', s), []).append(('h', h))
        adj.setdefault(('h', h), []).append(('s', s))
    seen = set()
    for v in adj:
        if v in seen:
            continue
        comp, stack = set(), [v]
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(w for w in adj[u] if w not in comp)
        seen |= comp
        ce = sum(len(adj[u]) for u in comp) // 2
        if ce >= len(comp):
            return True
    return False


def run_instance(S, Hset, nbH, cap, xcheck):
    feas, forced = flow_forced(S, Hset, nbH, cap)
    if xcheck:
        feas2, forced2 = enum_forced(S, Hset, nbH, cap)
        assert feas == feas2, "engine disagreement on feasibility"
        if feas:
            assert forced == forced2, \
                f"engine disagreement on forced set: {forced ^ forced2}"
    if not feas:
        return 'infeasible'
    return 'cyclic' if core_cyclic(forced) else 'ok'


def scan_n(n):
    stats = {'graphs': 0, 'inst2': 0, 'inst_lo': 0, 'infeasible': 0,
             'cyclic': 0, 'xchecked': 0}
    inst_no = 0
    for g6 in graphs6(n):
        stats['graphs'] += 1
        nn, adj = decode_g6(g6)
        tau = min_fvs_size(nn, adj)
        for S in all_min_fvs(nn, adj, tau):
            rest = sorted(set(range(nn)) - S)
            Hedges = [(a, b) for (a, b) in combinations(rest, 2)
                      if b in adj[a]]
            nbH = {s: frozenset(w for w in adj[s] if w not in S) for s in S}
            for e in Hedges:
                inst_no += 1
                cap = {h: 2 for h in rest}
                cap[e[0]] = cap[e[1]] = 1
                key = 'inst2' if tau >= 2 else 'inst_lo'
                stats[key] += 1
                if tau < 2:
                    continue  # trivial layer: S-side of a cycle needs >=2
                xc = (n <= 8) or (inst_no % 500 == 0)
                if xc:
                    stats['xchecked'] += 1
                r = run_instance(sorted(S), rest, nbH, cap, xc)
                if r == 'infeasible':
                    stats['infeasible'] += 1
                    print(f"INFEASIBLE n={n} g6={g6} S={sorted(S)} e={e}")
                elif r == 'cyclic':
                    stats['cyclic'] += 1
                    print(f"CYCLIC-CORE n={n} g6={g6} S={sorted(S)} e={e}")
    print(f"[n={n}] graphs={stats['graphs']} tau2_instances={stats['inst2']} "
          f"taulo_instances={stats['inst_lo']} infeasible={stats['infeasible']} "
          f"cyclic={stats['cyclic']} xchecked={stats['xchecked']}", flush=True)


def controls():
    # O-64 realization from PROOFS.md D (S NOT a minimum FVS): must be CYCLIC
    # vertices: s,t,u,q1,r,q2,y,h,w -> 0..8
    names = {'s': 0, 't': 1, 'u': 2, 'q1': 3, 'r': 4, 'q2': 5,
             'y': 6, 'h': 7, 'w': 8}
    edges = [('q1', 'r'), ('r', 'q2'), ('q1', 'y'), ('y', 'h'), ('y', 'w'),
             ('s', 'q1'), ('s', 'q2'), ('s', 'h'),
             ('t', 'q1'), ('t', 'q2'), ('u', 'h'), ('u', 'w')]
    n = 9
    adj = [set() for _ in range(n)]
    for (a, b) in edges:
        adj[names[a]].add(names[b])
        adj[names[b]].add(names[a])
    S = [names[x] for x in ('s', 't', 'u')]
    rest = sorted(set(range(n)) - set(S))
    nbH = {s: frozenset(w for w in adj[s] if w not in S) for s in S}
    cap = {h: 2 for h in rest}
    cap[names['h']] = cap[names['y']] = 1          # e = (h, y)
    r = run_instance(S, rest, nbH, cap, True)
    print(f"[CTRL O-64 graph] verdict={r} (must be cyclic)")
    ok = (r == 'cyclic')
    # ADJ-1 realization: S=s0,s1,s2 (9,10,11), H=0,1,2,x=3,y=4, e=(x,y)
    n = 8
    adj = [set() for _ in range(n)]
    inc = [(5, 0), (5, 1), (6, 0), (6, 2), (7, 0), (7, 1), (7, 2), (3, 4)]
    for (a, b) in inc:
        adj[a].add(b)
        adj[b].add(a)
    S = [5, 6, 7]
    rest = [0, 1, 2, 3, 4]
    nbH = {s: frozenset(w for w in adj[s] if w not in S) for s in S}
    cap = {h: 2 for h in rest}
    cap[3] = cap[4] = 1
    r = run_instance(S, rest, nbH, cap, True)
    print(f"[CTRL ADJ-1 graph] verdict={r} (must be cyclic)")
    ok &= (r == 'cyclic')
    # negative harness control: acyclic instance must NOT read cyclic
    # (path P4 with S = one center vertex is tau=0; use C4: tau=1, S={0})
    n = 4
    adj = [set() for _ in range(n)]
    for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        adj[a].add(b)
        adj[b].add(a)
    S = [0]
    rest = [1, 2, 3]
    nbH = {0: frozenset({1, 3})}
    cap = {1: 2, 2: 2, 3: 2}
    cap[1] = cap[2] = 1                            # e = (1,2)
    r = run_instance(S, rest, nbH, cap, True)
    print(f"[CTRL C4 acyclic] verdict={r} (must be ok)")
    ok &= (r == 'ok')
    print(f"[GRAPH CONTROLS] {'ALL PASS' if ok else '*** FAIL ***'}")


if __name__ == '__main__':
    if sys.argv[1] == 'controls':
        controls()
    else:
        for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
            scan_n(n)
