#!/usr/bin/env python3
"""Frozen checker for conjecture E1 (component excess).

Branch attempt/2026-08-04-claude-fable-5-0eb8. Frozen per PREREG-E1.md.

E1: every connected bipartite graph C with at least one edge and classes of
sizes a, b satisfies

    excess(C) := |a - b| + 2 g(C) - p(C) >= 1,

with g(C) = FE(C) - max(a,b) as in PREREG-L6-N9.md (FE = the largest induced
forest using one FULL color class plus a subset of the other).

Motivation (Lemma L7, proved in ATTEMPT_REPORT.md): for any minimum OCT T of
a connected nonbipartite G with B = G - T,

    [Delta(B) + 2 g(B) - 1] - p(G) >= sum_C excess(C) - 1 - o(G),

so E1 implies the L6 lifting condition for every G having a minimum OCT with
c_e(B) >= o(G) + 1. E1 is equivalent to ell(C) >= 2(min(a,b) - g(C)) + 1 —
the bipartite Conjecture-40 inequality with tau replaced by its L6-Forest
upper bound; it is strictly stronger than the conjecture exactly on graphs
where tau < min - g.

Universe: all connected bipartite graphs 2 <= n <= 10 (geng -c -b -q).
Anchor counts (OEIS A005142 tail): 1, 1, 3, 5, 17, 44, 182, 730, 4032.

Controls:
  gold hand-derived values: K2 excess 1; C4 excess 1; C6 excess 3;
    P4 excess 3; K_{1,3} excess 2; K_{2,3} excess 2; K_{3,3} excess 1.
  CTRL-E1-PLUS-1: excess(C) >= 2 must FAIL somewhere (K2 already).
Decision rules: census mismatch or gold failure -> run FAILS.
E1 failures are DATA: record every witness graph6 with (a,b,p,g,excess).
"""
import subprocess, sys
from itertools import combinations

GENG = "/opt/homebrew/bin/geng"


def parse_graph6(line):
    line = line.strip()
    data = [ord(c) - 63 for c in line]
    n = data[0]
    bits = []
    for v in data[1:]:
        for i in range(5, -1, -1):
            bits.append((v >> i) & 1)
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return n, adj


def from_edges(n, E):
    adj = [0] * n
    for a, b in E:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return n, adj


def is_forest_subset(adj, mask):
    verts = [v for v in range(len(adj)) if mask >> v & 1]
    parent = {v: v for v in verts}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for i in verts:
        ai = adj[i]
        for j in verts:
            if j > i and (ai >> j & 1):
                ri, rj = find(i), find(j)
                if ri == rj:
                    return False
                parent[ri] = rj
    return True


def two_color(n, adj):
    color = {}
    for start in range(n):
        if start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in range(n):
                if adj[u] >> v & 1:
                    if v not in color:
                        color[v] = 1 - color[u]
                        stack.append(v)
                    elif color[v] == color[u]:
                        return None
    return color


def fe(n, adj, A, B):
    best = 0
    for W, Z in ((A, B), (B, A)):
        wm = 0
        for v in W:
            wm |= 1 << v
        done = False
        for k in range(len(Z), -1, -1):
            for Y in combinations(Z, k):
                ym = wm
                for v in Y:
                    ym |= 1 << v
                if is_forest_subset(adj, ym):
                    best = max(best, len(W) + k)
                    done = True
                    break
            if done:
                break
    return best


def path_cover(n, adj):
    full = (1 << n) - 1
    ham = [0] * (full + 1)
    for v in range(n):
        ham[1 << v] = 1 << v
    order = sorted(range(1, full + 1), key=lambda m: bin(m).count("1"))
    for mask in order:
        if bin(mask).count("1") < 2:
            continue
        ends = 0
        for v in range(n):
            if not (mask >> v & 1):
                continue
            if ham[mask ^ (1 << v)] & adj[v]:
                ends |= 1 << v
        ham[mask] = ends
    INF = 99
    dp = [INF] * (full + 1)
    dp[0] = 0
    for mask in order:
        low = mask & (-mask)
        sub = mask
        while sub:
            if (sub & low) and ham[sub]:
                cand = dp[mask ^ sub] + 1
                if cand < dp[mask]:
                    dp[mask] = cand
            sub = (sub - 1) & mask
    return dp[full]


def excess_of(n, adj):
    color = two_color(n, adj)
    assert color is not None
    A = [v for v in range(n) if color[v] == 0]
    B = [v for v in range(n) if color[v] == 1]
    g = fe(n, adj, A, B) - max(len(A), len(B))
    p = path_cover(n, adj)
    return abs(len(A) - len(B)) + 2 * g - p, len(A), len(B), p, g


def gold():
    fails = []

    def expect(name, n, adj, want):
        e = excess_of(n, adj)[0]
        ok = e == want
        print(f"  {name}: excess={e} want={want} {'PASS' if ok else 'FAIL'}")
        if not ok:
            fails.append(name)

    expect("K2", *from_edges(2, [(0, 1)]), 1)
    expect("C4", *from_edges(4, [(0, 1), (1, 2), (2, 3), (3, 0)]), 1)
    expect("C6", *from_edges(6, [(i, (i + 1) % 6) for i in range(6)]), 3)
    expect("P4", *from_edges(4, [(0, 1), (1, 2), (2, 3)]), 3)
    expect("K13", *from_edges(4, [(0, 1), (0, 2), (0, 3)]), 2)
    expect("K23", *from_edges(5,
           [(a, b) for a in (0, 1) for b in (2, 3, 4)]), 2)
    expect("K33", *from_edges(6,
           [(a, b) for a in (0, 1, 2) for b in (3, 4, 5)]), 1)
    print("E1 GOLD:", "ALL PASS" if not fails else f"FAILURES {fails}")
    return not fails


def census():
    want = {2: 1, 3: 1, 4: 3, 5: 5, 6: 17, 7: 44, 8: 182, 9: 730, 10: 4032}
    tot = viol = ctrl = 0
    min_excess = 10**9
    hist = {}
    for n in range(2, 11):
        cnt = 0
        out = subprocess.run([GENG, "-c", "-b", "-q", str(n)],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            nn, adj = parse_graph6(line)
            cnt += 1
            tot += 1
            e, a, b, p, g = excess_of(nn, adj)
            hist[e] = hist.get(e, 0) + 1
            min_excess = min(min_excess, e)
            if e < 1:
                viol += 1
                print(f"E1-WITNESS {line.strip()} a={a} b={b} p={p} g={g} "
                      f"excess={e}")
            if e < 2:
                ctrl += 1
        assert cnt == want[n], (n, cnt)
    print(f"E1 census n<=10: {tot} connected bipartite graphs, "
          f"failures={viol}, min excess={min_excess}")
    print(f"excess histogram: {dict(sorted(hist.items()))}")
    print(f"CTRL-E1-PLUS-1 fires on {ctrl} graphs (must be > 0)")
    assert ctrl > 0
    return viol


if __name__ == "__main__":
    if sys.argv[1] == "gold":
        sys.exit(0 if gold() else 1)
    elif sys.argv[1] == "census":
        census()
