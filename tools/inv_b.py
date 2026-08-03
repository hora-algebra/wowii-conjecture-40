"""Implementation B — standalone bitmask engine (sweep workhorse).
Own graph6 parser, iterative Havel-Hakimi residue, BFS diameter,
induced-forest size via feedback-vertex-set branching.
Conventions mirror the repo's Lean definitions exactly (see RESULT_RECORD S-3).
"""
import sys
from math import ceil


def parse_g6(line):
    """graph6 -> (n, adj) where adj is a list of neighbor-bitmasks. n < 63 assumed."""
    s = line.strip()
    data = [ord(c) - 63 for c in s]
    n = data[0]
    bits = []
    for v in data[1:]:
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            idx += 1
    return n, adj


def residue_b(degs):
    """Iterative Havel-Hakimi. Head 0 (sorted desc) => residue = whole list length."""
    s = sorted(degs, reverse=True)
    while s:
        d = s[0]
        if d == 0:
            return len(s)
        rest = s[1:]
        for i in range(d):
            rest[i] -= 1
        s = sorted(rest, reverse=True)
    return 0


def diam_b(n, adj):
    """Max BFS eccentricity. Caller guarantees connected."""
    best = 0
    for src in range(n):
        dist = [-1] * n
        dist[src] = 0
        frontier = [src]
        d = 0
        while frontier:
            d += 1
            nxt = []
            for u in frontier:
                m = adj[u]
                while m:
                    v = (m & -m).bit_length() - 1
                    m &= m - 1
                    if dist[v] < 0:
                        dist[v] = d
                        nxt.append(v)
            frontier = nxt
        ecc = max(dist)
        if ecc > best:
            best = ecc
    return best


def _find_cycle(n, adj, removed):
    """Return vertices of some cycle in G - removed, or None. Iterative DFS."""
    color = [0] * n  # 0 unvisited, 1 active, 2 done
    parent = [-1] * n
    for start in range(n):
        if removed >> start & 1 or color[start]:
            continue
        stack = [(start, -1, adj[start] & ~removed)]
        color[start] = 1
        while stack:
            u, pu, rem = stack[-1]
            if rem == 0:
                color[u] = 2
                stack.pop()
                continue
            v = (rem & -rem).bit_length() - 1
            stack[-1] = (u, pu, rem & (rem - 1))
            if v == pu:
                continue
            if color[v] == 1:
                # back edge u->v : cycle = chain u..v via parents
                cyc = [u]
                w = u
                while w != v:
                    w = parent[w]
                    cyc.append(w)
                return cyc
            if color[v] == 0:
                color[v] = 1
                parent[v] = u
                stack.append((v, u, adj[v] & ~removed))
    return None


def forest_b(n, adj):
    """Largest induced forest = n - min feedback vertex set, by cycle-branching."""
    best = [n]

    def solve(removed, k):
        if k >= best[0]:
            return
        cyc = _find_cycle(n, adj, removed)
        if cyc is None:
            best[0] = k
            return
        for v in cyc:
            solve(removed | (1 << v), k + 1)

    solve(0, 0)
    return n - best[0]


def triple(line):
    n, adj = parse_g6(line)
    degs = [bin(a).count("1") for a in adj]
    r = residue_b(degs)
    dm = diam_b(n, adj)
    f = forest_b(n, adj)
    return n, r, dm, f


def slack(line):
    """f - residue - ceil(diam/3); negative = COUNTEREXAMPLE."""
    n, r, dm, f = triple(line)
    return f - r - ceil(dm / 3)


if __name__ == "__main__":
    for ln in sys.stdin:
        ln = ln.strip()
        if ln:
            n, r, dm, f = triple(ln)
            print(ln, n, r, dm, f, f - r - ceil(dm / 3))
