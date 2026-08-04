#!/usr/bin/env python3
"""Exact verification of the L5/L6-condition counterexample CX11.

CX11 = the E1 witness I??FF?^Fo (two K_{3,2} blocks glued along a C4)
plus an apex t adjacent to {0, 1, 6, 7} — two vertices of each color class,
none in the right block {3,4,5,8,9}. Everything below is asserted by exact
computation; a second pass re-derives p and the OCT set by definition-level
brute force (no shared path-DP) as an internal cross-engine check.

Why this attachment: t needs neighbours in BOTH classes for an odd cycle
(same-class attachments stay bipartite — the first attempted apex {0,1,2}
failed exactly there and is preserved in git history as the recorded
mistake); two per class make {t} the UNIQUE minimum OCT (deleting any one
C-vertex leaves t a neighbour in each class, joined by a path in the
2-connected C, hence an odd cycle); and avoiding the right block preserves
the slot-counting proof that CX11 is not traceable.

Facts asserted:
  W1  I??FF?^Fo has edge set {0,1,2}x{6,7} u {3,4,5}x{8,9} u {6,7}x{8,9},
      classes A={0,1,2,8,9}, B={3,4,5,6,7} (5+5), p=2, tau=2,
      every same-side pair (both classes) has codegree >= 2 (hence r=0, g=1),
      FE=6, excess = 0 (the unique E1 failure at n<=10).
  W2  CX11 (n=11) is connected, nonbipartite, o=1, and {10} (the apex) is
      its UNIQUE minimum OCT.
  W3  p(CX11)=2, ell(CX11)=9.
  W4  For the unique OCT: B = I??FF?^Fo with c_e=1, i=0, M=5, Delta=0, r=0,
      g=1, tau(B)=2. Thresholds: L2 = 2c_e-1 = 1; L3 = 2c_e+Delta-1 = 1;
      L5 = 2c_e+Delta+2r-1 = 1; L6 = Delta+2g-1 = 1. All < p = 2:
      NO minimum OCT of CX11 satisfies any of the L2/L3/L5/L6 conditions.
      L4 inapplicable: the unique remainder is not a forest (tau=2).
  W5  Exact LIFT-A holds at CX11: ell = 9 >= 2 tau(B) + o + 1 = 6 (slack 3).
  W6  Conjecture 40 holds at CX11 (sanity): 2f >= p + b + 1.
"""
import sys, os
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l6scan import (parse_graph6, from_edges, is_forest_subset, tau_of,
                    bipartition_of, components, bip_stats, path_cover,
                    min_octs, profile)

C_G6 = "I??FF?^Fo"


def build_c():
    n, adj = parse_graph6(C_G6)
    E = {(i, j) for i in range(n) for j in range(i + 1, n) if adj[i] >> j & 1}
    want = set()
    for a in (0, 1, 2):
        for b in (6, 7):
            want.add((a, b))
    for a in (3, 4, 5):
        for b in (8, 9):
            want.add((a, b))
    for a in (6, 7):
        for b in (8, 9):
            want.add((a, b))
    assert E == want, (E ^ want)
    return n, adj


def check_w1():
    n, adj = build_c()
    full = (1 << n) - 1
    ok, color = bipartition_of(n, adj, full)
    assert ok
    A = sorted(v for v in range(n) if color[v] == color[0])
    B = sorted(v for v in range(n) if color[v] != color[0])
    assert {len(A), len(B)} == {5}
    assert set(A) == {0, 1, 2, 8, 9} or set(B) == {0, 1, 2, 8, 9}
    # codegrees >= 2 on both sides
    for side in (A, B):
        for u, v in combinations(side, 2):
            assert bin(adj[u] & adj[v]).count("1") >= 2, (u, v)
    assert path_cover(n, adj) == 2
    assert tau_of(n, adj) == 2
    c_e, i, M, Delta, r, g = bip_stats(n, adj, full)
    assert (c_e, i, M, Delta, r, g) == (1, 0, 5, 0, 0, 1)
    excess = abs(len(A) - len(B)) + 2 * g - 2
    assert excess == 0
    print("W1 OK: I??FF?^Fo = glued K_{3,2}s, 5+5, dense both sides, "
          "p=2, tau=2, g=1, excess=0")


def build_cx11():
    n, adj = build_c()
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if adj[i] >> j & 1]
    E += [(0, 10), (1, 10), (6, 10), (7, 10)]
    return from_edges(11, E)


def to_graph6(n, adj):
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append((adj[i] >> j) & 1)
    while len(bits) % 6:
        bits.append(0)
    out = chr(n + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]:
            v = (v << 1) | b
        out += chr(v + 63)
    return out


def check_w2_w6():
    n, adj = build_cx11()
    full = (1 << n) - 1
    # connected, nonbipartite
    assert len(components(n, adj, full)) == 1
    ok, _ = bipartition_of(n, adj, full)
    assert not ok
    o, octs = min_octs(n, adj)
    assert o == 1 and octs == [1 << 10], (o, octs)
    print("W2 OK: CX11 connected nonbipartite, unique minimum OCT = {apex}")

    p = path_cover(n, adj)
    assert p == 2
    ell = n - p
    assert ell == 9
    print("W3 OK: p(CX11)=2, ell=9")

    bm = full ^ (1 << 10)
    tau_b = tau_of(n, adj, bm)
    c_e, i, M, Delta, r, g = bip_stats(n, adj, bm)
    assert (tau_b, c_e, i, M, Delta, r, g) == (2, 1, 0, 5, 0, 0, 1)
    thr = {"L2": 2 * c_e - 1, "L3": 2 * c_e + Delta - 1,
           "L5": 2 * c_e + Delta + 2 * r - 1, "L6": Delta + 2 * g - 1}
    assert thr == {"L2": 1, "L3": 1, "L5": 1, "L6": 1}
    assert all(t < p for t in thr.values())
    assert tau_b != 0          # L4 hypothesis (forest remainder) unavailable
    print(f"W4 OK: unique-OCT thresholds {thr} all < p=2; "
          "L4 inapplicable (tau(B)=2)")

    assert ell >= 2 * tau_b + o + 1
    print(f"W5 OK: exact LIFT-A holds, slack {ell - (2 * tau_b + o + 1)}")

    # Conjecture 40 sanity: f = n - tau(G), b = n - o, 2f >= p + b + 1
    tau_g = tau_of(n, adj)
    f = n - tau_g
    b = n - o
    assert 2 * f >= p + b + 1, (f, b, p)
    print(f"W6 OK: Conjecture 40 holds at CX11 "
          f"(f={f}, b={b}, p={p}, slack {2*f - (p+b+1)})")

    # cross-check with the frozen scanner's own aggregation
    pr = profile(n, adj)
    assert pr["o"] == 1 and pr["p"] == 2 and len(pr["octs"]) == 1
    assert pr["best"]["l5"] == -1 and pr["best"]["l6"] == -1
    assert pr["best"]["slack"] == 3
    print("CROSS OK: l6scan.profile agrees (L5 margin -1, L6 margin -1, "
          "slack 3)")

    g6 = to_graph6(n, adj)
    rt = parse_graph6(g6)
    assert rt[1] == adj
    print(f"CX11 graph6: {g6}")


# ---- second engine: definition-level brute force, no shared DP ----
def brute_traceable(n, adj):
    """Is there a Hamilton path? DFS over permutations with pruning."""
    seen = set()

    def dfs(v, mask):
        if mask == (1 << n) - 1:
            return True
        key = (v, mask)
        if key in seen:
            return False
        seen.add(key)
        for u in range(n):
            if (adj[v] >> u & 1) and not (mask >> u & 1):
                if dfs(u, mask | 1 << u):
                    return True
        return False

    return any(dfs(s, 1 << s) for s in range(n))


def brute_two_cover(n, adj):
    """Can V be covered by two vertex-disjoint paths (either may be trivial)?"""
    full = (1 << n) - 1
    # try all splits: mask covered by one path each
    ham_cache = {}

    def ham(mask):
        if mask in ham_cache:
            return ham_cache[mask]
        verts = [v for v in range(n) if mask >> v & 1]
        if len(verts) == 1:
            ham_cache[mask] = True
            return True
        seen = set()

        def dfs(v, m):
            if m == mask:
                return True
            if (v, m) in seen:
                return False
            seen.add((v, m))
            for u in verts:
                if (adj[v] >> u & 1) and not (m >> u & 1):
                    if dfs(u, m | 1 << u):
                        return True
            return False
        r = any(dfs(s, 1 << s) for s in verts)
        ham_cache[mask] = r
        return r

    sub = full
    while sub:
        if ham(sub) and (sub == full or ham(full ^ sub)):
            return True
        sub = (sub - 1) & full
    return False


def second_engine():
    n, adj = build_cx11()
    assert not brute_traceable(n, adj)
    assert brute_two_cover(n, adj)
    print("ENGINE2 OK: CX11 not traceable; two paths suffice (p=2)")
    # OCT uniqueness by definition: exactly one v with G-v bipartite
    elig = []
    for v in range(n):
        ok, _ = bipartition_of(n, adj, ((1 << n) - 1) ^ (1 << v))
        if ok:
            elig.append(v)
    assert elig == [10]
    print("ENGINE2 OK: apex is the only vertex whose removal is bipartite")


if __name__ == "__main__":
    check_w1()
    check_w2_w6()
    second_engine()
    print("ALL CX11 CHECKS PASS")
