#!/usr/bin/env python3
"""Independent audit of the codex-a7c3 L3/L4/L5 claims.

Written from the definitions in LIFT-A-RESIDUAL.md and paper v2 BEFORE
reading any line of the codex checkers' code. Everything is recomputed
from scratch:

  tau(B)  : n - max order of an induced forest (subset scan, union-find)
  p(G)    : minimum path cover (Hamiltonian-path-on-submask DP + submask DP)
  min OCTs: all subsets T of minimum size with G-T bipartite
  per-component class sizes, c_e, i, M, Delta, r

Claims audited (codex-a7c3, LIFT-A-RESIDUAL.md / ATTEMPT_REPORT.md):
  A1. L3-Forest tau(B) <= M - c_e on all bipartite graphs 2<=n<=8:
      451 graphs (2,3,7,13,35,88,303 per order), 0 failures, 182 tight;
      false control tau <= M - c_e - 1 fires on exactly the tight cases.
  A2. L5-Forest tau(B) <= M - c_e - r: 0 failures, 356 tight; false
      one-unit strengthening fires on the tight cases.
  A3. Connected nonbipartite 3<=n<=8: counts 2,6,21,112,853,11117 connected
      per order (nonbipartite total 11,859); exact LIFT-A (exists min OCT T:
      ell >= 2 tau(G-T) + |T| + 1) 0 failures.
  A4. Coverage: L2 (p <= 2c_e - 1) covers 11,170; L3 (p <= 2c_e + Delta - 1)
      covers 11,852 (682 not covered by L2); L3 residual = 7 named graphs;
      L5 (p <= 2c_e + Delta + 2r - 1) covers all 11,859.
  A5. Implication failures: a graph covered by L3 (resp. L5) via minimum OCT
      T must satisfy the exact LIFT-A inequality with that same T: 0 failures.
  A6. L4: o <= 2 and some min OCT leaving a forest -> ell >= o + 1;
      applies to 4,606 graphs incl. all 7 L3 residuals; false control
      ell >= o + 2 fails at least twice (K_3 among them).
  A7. Strictness control DC{: o=1, p=2, fails L2, passes L3 (and exact).
"""
import subprocess, sys
from itertools import combinations

GENG = "/opt/homebrew/bin/geng"


# ---------- graph6 ----------
def parse_graph6(line):
    line = line.strip()
    data = [ord(c) - 63 for c in line]
    n = data[0]
    assert 0 <= n <= 62
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


# ---------- primitives ----------
def edges_of(n, adj):
    return [(i, j) for i in range(n) for j in range(i + 1, n)
            if adj[i] >> j & 1]


def is_forest_subset(adj, mask):
    """No cycle inside the induced subgraph on mask (union-find)."""
    verts = [v for v in range(adj.__len__()) if mask >> v & 1]
    parent = {v: v for v in verts}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for i in verts:
        for j in verts:
            if j <= i:
                continue
            if adj[i] >> j & 1:
                ri, rj = find(i), find(j)
                if ri == rj:
                    return False
                parent[ri] = rj
    return True


def tau_of(n, adj, mask=None):
    """Decycling number of the induced subgraph on mask (default: all)."""
    if mask is None:
        mask = (1 << n) - 1
    verts = [v for v in range(n) if mask >> v & 1]
    m = len(verts)
    # max induced forest order f, scanning subset sizes from m down
    for f in range(m, -1, -1):
        for keep in combinations(verts, f):
            km = 0
            for v in keep:
                km |= 1 << v
            if is_forest_subset(adj, km):
                return m - f
    return m


def bipartition_of(n, adj, mask):
    """2-coloring of induced subgraph on mask; None if odd cycle.
    Returns (colorable, color dict)."""
    color = {}
    for start in range(n):
        if not (mask >> start & 1) or start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in range(n):
                if (mask >> v & 1) and (adj[u] >> v & 1):
                    if v not in color:
                        color[v] = 1 - color[u]
                        stack.append(v)
                    elif color[v] == color[u]:
                        return False, None
    return True, color


def components(n, adj, mask):
    seen = 0
    out = []
    for start in range(n):
        if not (mask >> start & 1) or (seen >> start & 1):
            continue
        comp = 0
        stack = [start]
        comp |= 1 << start
        while stack:
            u = stack.pop()
            for v in range(n):
                if (mask >> v & 1) and (adj[u] >> v & 1) and not (comp >> v & 1):
                    comp |= 1 << v
                    stack.append(v)
        seen |= comp
        out.append(comp)
    return out


def bip_stats(n, adj, mask):
    """(c_e, i, M, Delta, r) of the bipartite graph induced on mask."""
    ok, color = bipartition_of(n, adj, mask)
    assert ok
    c_e = i = M = imb = r = 0
    for comp in components(n, adj, mask):
        verts = [v for v in range(n) if comp >> v & 1]
        has_edge = any(adj[u] >> v & 1 for u in verts for v in verts if v > u)
        if not has_edge:
            i += len(verts)
            continue
        c_e += 1
        A = [v for v in verts if color[v] == 0]
        B = [v for v in verts if color[v] == 1]
        a, b = len(A), len(B)
        M += min(a, b)
        imb += abs(a - b)
        # r(C): some smaller class (either on tie) has a pair with codeg <= 1
        small_classes = []
        if a <= b:
            small_classes.append(A)
        if b <= a:
            small_classes.append(B)
        rc = 0
        for cls in small_classes:
            for u, v in combinations(cls, 2):
                codeg = bin(adj[u] & adj[v] & comp).count("1")
                if codeg <= 1:
                    rc = 1
        r += rc
    return c_e, i, M, imb + i, r


def path_cover(n, adj):
    """Minimum path cover number of the whole graph (trivial paths allowed)."""
    full = (1 << n) - 1
    # ham[mask] = bitmask of vertices at which a Hamiltonian path of the
    # induced subgraph on mask can end (mask must be covered by ONE path)
    ham = [0] * (full + 1)
    for v in range(n):
        ham[1 << v] = 1 << v
    order = sorted(range(1, full + 1), key=lambda m: bin(m).count("1"))
    for mask in order:
        if bin(mask).count("1") < 2:
            continue
        ends = 0
        sub = mask
        v = 0
        for v in range(n):
            if not (mask >> v & 1):
                continue
            prev = mask ^ (1 << v)
            if ham[prev] & adj[v]:
                ends |= 1 << v
        ham[mask] = ends
    # dp over set cover by path-covered submasks
    INF = 99
    dp = [INF] * (full + 1)
    dp[0] = 0
    for mask in order:
        # iterate submasks of mask that contain lowest set bit (canonical)
        low = mask & (-mask)
        sub = mask
        while sub:
            if (sub & low) and ham[sub]:
                cand = dp[mask ^ sub] + 1
                if cand < dp[mask]:
                    dp[mask] = cand
            sub = (sub - 1) & mask
    return dp[full]


def min_octs(n, adj):
    """All minimum odd-cycle transversals (as masks). o = |each|."""
    full = (1 << n) - 1
    for k in range(n + 1):
        found = []
        for T in combinations(range(n), k):
            tm = 0
            for v in T:
                tm |= 1 << v
            ok, _ = bipartition_of(n, adj, full ^ tm)
            if ok:
                found.append(tm)
        if found:
            return k, found
    raise RuntimeError


# ---------- audits ----------
def audit_bipartite():
    per_order_want = {2: 2, 3: 3, 4: 7, 5: 13, 6: 35, 7: 88, 8: 303}
    total = fails5 = fails3 = tight3 = tight5 = ctrl3 = ctrl5 = 0
    for n in range(2, 9):
        cnt = 0
        out = subprocess.run([GENG, "-b", "-q", str(n)],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            nn, adj = parse_graph6(line)
            cnt += 1
            total += 1
            full = (1 << nn) - 1
            tau = tau_of(nn, adj)
            c_e, i, M, Delta, r = bip_stats(nn, adj, full)
            assert nn - 2 * M == Delta, "identity (1) fails"
            if not tau <= M - c_e:
                fails3 += 1
            if tau == M - c_e:
                tight3 += 1
            if not tau <= M - c_e - 1:
                ctrl3 += 1          # false control fires
            if not tau <= M - c_e - r:
                fails5 += 1
            if tau == M - c_e - r:
                tight5 += 1
            if not tau <= M - c_e - r - 1:
                ctrl5 += 1
        assert cnt == per_order_want[n], (n, cnt)
    print(f"bipartite universe: {total} graphs "
          f"(per-order counts match {sorted(per_order_want.values())})")
    print(f"  L3-Forest: failures={fails3} tight={tight3} "
          f"false-control-fires={ctrl3}")
    print(f"  L5-Forest: failures={fails5} tight={tight5} "
          f"false-control-fires={ctrl5}")
    assert fails3 == 0 and tight3 == 182 and ctrl3 == 182
    assert fails5 == 0 and tight5 == 356 and ctrl5 == 356
    print("  A1, A2 CONFIRMED")


def audit_nonbipartite():
    conn_want = {3: 2, 4: 6, 5: 21, 6: 112, 7: 853, 8: 11117}
    nonbip = 0
    lifta_fail = 0
    cov = {"L2": 0, "L3": 0, "L5": 0}
    l3_new_over_l2 = 0
    l3_residual = []
    l5_new_over_l3 = 0
    impl_fail = {"L3": 0, "L5": 0}
    l4_applies = 0
    l4_fail = 0
    l4_false_ctrl_fails = 0
    l4_covers_residual = 0
    l3_universal = 0
    for n in range(3, 9):
        cnt = 0
        out = subprocess.run([GENG, "-c", "-q", str(n)],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            nn, adj = parse_graph6(line)
            cnt += 1
            full = (1 << nn) - 1
            ok, _ = bipartition_of(nn, adj, full)
            if ok:
                continue
            nonbip += 1
            p = path_cover(nn, adj)
            ell = nn - p
            o, octs = min_octs(nn, adj)
            got = {"L2": False, "L3": False, "L5": False}
            exact = False
            forest_rem = False
            allL3 = True
            for T in octs:
                tm = full ^ T
                tau_b = tau_of(nn, adj, tm)
                c_e, i, M, Delta, r = bip_stats(nn, adj, tm)
                exact_here = ell >= 2 * tau_b + o + 1
                if exact_here:
                    exact = True
                if tau_b == 0:
                    forest_rem = True
                if p <= 2 * c_e - 1:
                    got["L2"] = True
                if p <= 2 * c_e + Delta - 1:
                    got["L3"] = True
                    if not exact_here:
                        impl_fail["L3"] += 1
                else:
                    allL3 = False
                if p <= 2 * c_e + Delta + 2 * r - 1:
                    got["L5"] = True
                    if not exact_here:
                        impl_fail["L5"] += 1
            if not exact:
                lifta_fail += 1
            for k in cov:
                if got[k]:
                    cov[k] += 1
            if got["L3"] and not got["L2"]:
                l3_new_over_l2 += 1
            if got["L5"] and not got["L3"]:
                l5_new_over_l3 += 1
            if allL3:
                l3_universal += 1
            if not got["L3"]:
                l3_residual.append(line.strip())
            # L4
            if o <= 2 and forest_rem:
                l4_applies += 1
                if not ell >= o + 1:
                    l4_fail += 1
                if not ell >= o + 2:
                    l4_false_ctrl_fails += 1
                if not got["L3"]:
                    l4_covers_residual += 1
        assert cnt == conn_want[n], (n, cnt)
    print(f"connected nonbipartite 3<=n<=8: {nonbip} graphs "
          f"(connected counts match)")
    print(f"  exact LIFT-A failures: {lifta_fail}")
    print(f"  coverage: L2={cov['L2']} L3={cov['L3']} "
          f"(new over L2: {l3_new_over_l2}) L5={cov['L5']} "
          f"(new over L3: {l5_new_over_l3})")
    print(f"  L3 residual ({len(l3_residual)}): {sorted(l3_residual)}")
    print(f"  implication failures: L3={impl_fail['L3']} L5={impl_fail['L5']}")
    print(f"  L4 applies: {l4_applies}, failures={l4_fail}, "
          f"false ell>=o+2 control fails on {l4_false_ctrl_fails} graphs, "
          f"covers {l4_covers_residual} of the L3 residuals")
    print(f"  descriptive: L3 holds for EVERY min OCT on {l3_universal}")
    assert nonbip == 11859
    assert lifta_fail == 0
    assert cov == {"L2": 11170, "L3": 11852, "L5": 11859}
    assert l3_new_over_l2 == 682 and l5_new_over_l3 == 7
    assert sorted(l3_residual) == sorted(
        ["F?o}W", "FCQV_", "G?BEH{", "G?`CVo", "G?o}][", "GCQQVo", "GCQSng"])
    assert impl_fail == {"L3": 0, "L5": 0}
    assert l4_applies == 4606 and l4_fail == 0
    assert l4_false_ctrl_fails >= 2 and l4_covers_residual == 7
    print("  A3, A4, A5, A6 CONFIRMED")


def audit_dcbrace():
    n, adj = parse_graph6("DC{")
    E = edges_of(n, adj)
    assert E == [(0, 3), (0, 4), (1, 4), (2, 4), (3, 4)], E
    p = path_cover(n, adj)
    o, octs = min_octs(n, adj)
    assert p == 2 and o == 1
    ell = n - p
    full = (1 << n) - 1
    ok2 = ok3 = exact = False
    for T in octs:
        tm = full ^ T
        tau_b = tau_of(n, adj, tm)
        c_e, i, M, Delta, r = bip_stats(n, adj, tm)
        if p <= 2 * c_e - 1:
            ok2 = True
        if p <= 2 * c_e + Delta - 1:
            ok3 = True
        if ell >= 2 * tau_b + o + 1:
            exact = True
    assert not ok2 and ok3 and exact
    print(f"DC{{: p=2, o=1, min OCTs={octs} -> fails L2, passes L3, "
          f"exact LIFT-A holds.  A7 CONFIRMED")


if __name__ == "__main__":
    audit_dcbrace()
    audit_bipartite()
    audit_nonbipartite()
    print("ALL AUDIT CHECKS PASS")
