#!/usr/bin/env python3
"""Frozen checker for the component-imbalance refinement of LIFT-A.

The mathematical statements tested here are recorded in LIFT-A-RESIDUAL.md.
The script has two jobs:

1. test the refined bipartite forest bound on every bipartite graph through a
   requested order; and
2. measure, without fitting a statement to the output, how much of the prior
   L2-residual class is covered by the new L3 condition.

Usage: python3 work/lift_residual.py [nmax]
Default nmax is 8.  nauty's `geng` must be on PATH.
"""

from __future__ import annotations

import subprocess
import sys


CONNECTED_COUNTS = {3: 2, 4: 6, 5: 21, 6: 112, 7: 853, 8: 11117}
BIPARTITE_COUNTS = {2: 2, 3: 3, 4: 7, 5: 13, 6: 35, 7: 88, 8: 303}


def popcount(value: int) -> int:
    """Python 3.9-compatible population count."""
    return bin(value).count("1")


def parse_g6(text: str):
    text = text.strip()
    if not text or text.startswith(">>"):
        raise ValueError(f"unsupported graph6 line: {text!r}")
    n = ord(text[0]) - 63
    if not 0 <= n < 63:
        raise ValueError("checker supports only one-byte graph6 orders")
    need = n * (n - 1) // 2
    bits = []
    for ch in text[1:]:
        value = ord(ch) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
        if len(bits) >= need:
            break
    if len(bits) < need:
        raise ValueError(f"truncated graph6 line: {text!r}")
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return n, adj


def graph6_lines(n: int, bipartite: bool):
    args = ["geng", "-q"]
    if bipartite:
        args.append("-b")
    else:
        args.append("-c")
    args.append(str(n))
    proc = subprocess.run(args, check=True, capture_output=True, text=True)
    return [line for line in proc.stdout.splitlines() if line and not line.startswith(">>")]


def is_bipartite(adj, universe: int) -> bool:
    color = [-1] * len(adj)
    unseen = universe
    while unseen:
        root_bit = unseen & -unseen
        root = root_bit.bit_length() - 1
        color[root] = 0
        stack = [root]
        unseen ^= root_bit
        while stack:
            u = stack.pop()
            nbrs = adj[u] & universe
            while nbrs:
                bit = nbrs & -nbrs
                nbrs ^= bit
                v = bit.bit_length() - 1
                if color[v] < 0:
                    color[v] = color[u] ^ 1
                    unseen &= ~bit
                    stack.append(v)
                elif color[v] == color[u]:
                    return False
    return True


def is_forest(adj, universe: int) -> bool:
    parent = list(range(len(adj)))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    vertices = universe
    while vertices:
        vbit = vertices & -vertices
        vertices ^= vbit
        v = vbit.bit_length() - 1
        lower = adj[v] & universe & (vbit - 1)
        while lower:
            ubit = lower & -lower
            lower ^= ubit
            u = ubit.bit_length() - 1
            a, b = find(u), find(v)
            if a == b:
                return False
            parent[a] = b
    return True


def max_induced_size(adj, universe: int, predicate) -> int:
    by_size = sorted(
        range(universe + 1),
        key=popcount,
        reverse=True,
    )
    for subset in by_size:
        if subset & ~universe:
            continue
        if predicate(adj, subset):
            return popcount(subset)
    raise AssertionError("empty set must satisfy both predicates")


def path_cover(adj, universe: int) -> int:
    """Exact minimum path cover by subset DP; isolated vertices are paths."""
    size = 1 << len(adj)
    endpoints = [0] * size
    path = [False] * size
    for mask in range(1, size):
        if mask & ~universe:
            continue
        if mask & (mask - 1) == 0:
            endpoints[mask] = mask
            path[mask] = True
            continue
        vertices = mask
        ends = 0
        while vertices:
            vbit = vertices & -vertices
            vertices ^= vbit
            v = vbit.bit_length() - 1
            if endpoints[mask ^ vbit] & adj[v]:
                ends |= vbit
        endpoints[mask] = ends
        path[mask] = bool(ends)

    inf = len(adj) + 1
    dp = [inf] * size
    dp[0] = 0
    for mask in range(1, size):
        if mask & ~universe:
            continue
        anchor = mask & -mask
        sub = mask
        best = inf
        while sub:
            if sub & anchor and path[sub]:
                best = min(best, dp[mask ^ sub] + 1)
            sub = (sub - 1) & mask
        dp[mask] = best
    return dp[universe]


def component_profile(adj, universe: int):
    """Return (edge components, isolates, M, Delta, sorted part profiles).

    M is the sum of the smaller bipartition-class sizes over edge-containing
    components.  Delta = isolates + sum |a-b| = |B|-2M.
    """
    unseen = universe
    edge_components = 0
    isolates = 0
    smaller_sum = 0
    delta = 0
    profiles = []

    while unseen:
        root_bit = unseen & -unseen
        root = root_bit.bit_length() - 1
        unseen ^= root_bit
        queue = [root]
        color = {root: 0}
        counts = [0, 0]
        has_edge = False
        while queue:
            u = queue.pop()
            counts[color[u]] += 1
            nbrs = adj[u] & universe
            if nbrs:
                has_edge = True
            while nbrs:
                bit = nbrs & -nbrs
                nbrs ^= bit
                v = bit.bit_length() - 1
                if v not in color:
                    color[v] = color[u] ^ 1
                    unseen &= ~bit
                    queue.append(v)
                elif color[v] == color[u]:
                    raise AssertionError("component_profile called on nonbipartite graph")
        if has_edge:
            a, b = sorted(counts)
            edge_components += 1
            smaller_sum += a
            delta += b - a
            profiles.append((a, b))
        else:
            isolates += 1
            delta += 1

    assert delta == popcount(universe) - 2 * smaller_sum
    return edge_components, isolates, smaller_sum, delta, tuple(sorted(profiles))


def exact_tau(adj, universe: int) -> int:
    return popcount(universe) - max_induced_size(adj, universe, is_forest)


def minimum_oct_masks(adj, full: int):
    b = max_induced_size(adj, full, is_bipartite)
    order = popcount(full) - b
    masks = []
    sub = full
    while True:
        if popcount(sub) == order and is_bipartite(adj, full ^ sub):
            masks.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & full
    return order, masks


def check_named_strict_extension():
    n, adj = parse_g6("DC{")
    full = (1 << n) - 1
    p = path_cover(adj, full)
    o, octs = minimum_oct_masks(adj, full)
    l2 = -1
    l3 = -1
    records = []
    for tmask in octs:
        bmask = full ^ tmask
        ce, iso, smaller, delta, parts = component_profile(adj, bmask)
        l2 = max(l2, 2 * ce - 1)
        l3 = max(l3, 2 * ce + delta - 1)
        records.append((tmask, ce, iso, smaller, delta, parts))
    assert o == 1 and p == 2
    assert p > l2 and p <= l3
    print(
        "STRICT-CONTROL DC{ PASS: o=1 p=2, best_L2_threshold="
        f"{l2}, best_L3_threshold={l3}, OCT_records={records}"
    )


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    if not 2 <= nmax <= 8:
        raise SystemExit("frozen checker supports 2 <= nmax <= 8")

    check_named_strict_extension()

    bip_total = bip_bad = bip_tight = stronger_control_fires = 0
    for n in range(2, nmax + 1):
        lines = graph6_lines(n, bipartite=True)
        expected = BIPARTITE_COUNTS[n]
        if len(lines) != expected:
            raise SystemExit(f"bipartite census mismatch n={n}: {len(lines)} != {expected}")
        for g6 in lines:
            nn, adj = parse_g6(g6)
            full = (1 << nn) - 1
            tau = exact_tau(adj, full)
            ce, _iso, smaller, _delta, _parts = component_profile(adj, full)
            bound = smaller - ce
            bip_total += 1
            if tau > bound:
                bip_bad += 1
                print("L3-FOREST-BOUND-FAIL", g6, nn, tau, bound)
            if tau == bound:
                bip_tight += 1
            if tau > bound - 1:
                stronger_control_fires += 1

    if stronger_control_fires == 0:
        raise SystemExit("negative control failed to fire")
    print(
        "L3-FOREST-BOUND: "
        f"bipartite_graphs={bip_total} failures={bip_bad} tight={bip_tight}; "
        f"CTRL-BOUND-MINUS-1 fires={stronger_control_fires}"
    )

    totals = {
        "connected": 0,
        "nonbipartite": 0,
        "lift_fail": 0,
        "l2": 0,
        "l3": 0,
        "new": 0,
        "residual": 0,
        "l3_implies_lift_fail": 0,
        "l3_all": 0,
    }
    new_examples = []
    residual_examples = []
    residual_profiles = {}

    for n in range(3, nmax + 1):
        lines = graph6_lines(n, bipartite=False)
        expected = CONNECTED_COUNTS[n]
        if len(lines) != expected:
            raise SystemExit(f"connected census mismatch n={n}: {len(lines)} != {expected}")
        totals["connected"] += len(lines)
        for g6 in lines:
            nn, adj = parse_g6(g6)
            full = (1 << nn) - 1
            if is_bipartite(adj, full):
                continue
            totals["nonbipartite"] += 1
            p = path_cover(adj, full)
            ell = nn - p
            o, octs = minimum_oct_masks(adj, full)
            l2_ok = False
            l3_ok = False
            l3_all = True
            lift_ok = False
            best_l2 = -1
            best_l3 = -1
            best_slack = -99
            best_record = None

            for tmask in octs:
                bmask = full ^ tmask
                ce, iso, smaller, delta, parts = component_profile(adj, bmask)
                tau_b = exact_tau(adj, bmask)
                if tau_b > smaller - ce:
                    raise SystemExit(f"embedded forest bound failure at {g6}")
                threshold2 = 2 * ce - 1
                threshold3 = 2 * ce + delta - 1
                slack = ell - (2 * tau_b + o + 1)
                best_l2 = max(best_l2, threshold2)
                if threshold3 > best_l3:
                    best_l3 = threshold3
                    best_record = (ce, iso, smaller, delta, parts, tau_b)
                best_slack = max(best_slack, slack)
                l2_ok |= p <= threshold2
                l3_ok |= p <= threshold3
                l3_all &= p <= threshold3
                lift_ok |= slack >= 0

            if not lift_ok:
                totals["lift_fail"] += 1
            if l2_ok:
                totals["l2"] += 1
            if l3_ok:
                totals["l3"] += 1
            if l3_all:
                totals["l3_all"] += 1
            if l3_ok and not l2_ok:
                totals["new"] += 1
                if len(new_examples) < 12:
                    new_examples.append((g6, nn, o, p, ell, best_l2, best_l3, best_slack, best_record))
            if not l3_ok:
                totals["residual"] += 1
                key = (p - best_l3, best_record[3], best_record[0])
                residual_profiles[key] = residual_profiles.get(key, 0) + 1
                if len(residual_examples) < 20:
                    residual_examples.append((g6, nn, o, p, ell, best_l2, best_l3, best_slack, best_record))
            if l3_ok and not lift_ok:
                totals["l3_implies_lift_fail"] += 1
                print("L3-IMPLICATION-FAIL", g6)

    expected_nonbip = sum({3: 1, 4: 3, 5: 16, 6: 95, 7: 809, 8: 10935}[n]
                              for n in range(3, nmax + 1))
    if totals["nonbipartite"] != expected_nonbip:
        raise SystemExit(
            f"nonbipartite census mismatch: {totals['nonbipartite']} != {expected_nonbip}"
        )

    print("LIFT-COVERAGE", totals)
    print("NEW-L3-EXAMPLES", new_examples)
    print("POST-L3-RESIDUAL-EXAMPLES", residual_examples)
    print("POST-L3-RESIDUAL-PROFILES", sorted(residual_profiles.items()))

    if bip_bad or totals["lift_fail"] or totals["l3_implies_lift_fail"]:
        raise SystemExit("one or more required checks failed")


if __name__ == "__main__":
    main()
