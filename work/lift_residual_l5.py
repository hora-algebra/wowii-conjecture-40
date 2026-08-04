#!/usr/bin/env python3
"""Regression checker for the L5 pair-sparse forest/lifting refinement."""

from __future__ import annotations

import hashlib
from itertools import combinations
from pathlib import Path

import lift_residual as base


EXPECTED_BASE_SHA = "78b7a981b113b627b77fcefff483d3d39b288145748ab0fcad30aadbcc507bb6"


def pair_bonus(adj, universe: int) -> int:
    """Number of edge components earning the one-vertex L5 bonus."""
    unseen = universe
    bonus = 0
    while unseen:
        root_bit = unseen & -unseen
        root = root_bit.bit_length() - 1
        unseen ^= root_bit
        queue = [root]
        color = {root: 0}
        sides = [[], []]
        has_edge = False
        while queue:
            u = queue.pop()
            sides[color[u]].append(u)
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
                    raise AssertionError("pair_bonus called on nonbipartite graph")
        if not has_edge:
            continue
        if len(sides[0]) < len(sides[1]):
            candidates = [sides[0]]
        elif len(sides[1]) < len(sides[0]):
            candidates = [sides[1]]
        else:
            candidates = sides
        earned = any(
            base.popcount(adj[u] & adj[v] & universe) <= 1
            for side in candidates
            for u, v in combinations(side, 2)
        )
        bonus += int(earned)
    return bonus


def main():
    base_path = Path(__file__).with_name("lift_residual.py")
    actual = hashlib.sha256(base_path.read_bytes()).hexdigest()
    if actual != EXPECTED_BASE_SHA:
        raise SystemExit(f"base checker hash mismatch: {actual}")

    bip_total = bip_bad = bip_tight = false_control = 0
    for n in range(2, 9):
        lines = base.graph6_lines(n, bipartite=True)
        if len(lines) != base.BIPARTITE_COUNTS[n]:
            raise SystemExit(f"bipartite census mismatch at n={n}")
        for g6 in lines:
            nn, adj = base.parse_g6(g6)
            full = (1 << nn) - 1
            tau = base.exact_tau(adj, full)
            ce, _iso, smaller, _delta, _parts = base.component_profile(adj, full)
            r = pair_bonus(adj, full)
            bound = smaller - ce - r
            bip_total += 1
            if tau > bound:
                bip_bad += 1
                print("L5-FOREST-FAIL", g6, nn, tau, bound, ce, smaller, r)
            if tau == bound:
                bip_tight += 1
            if tau > bound - 1:
                false_control += 1

    if false_control == 0:
        raise SystemExit("false L5 strengthening control did not fire")
    print(
        "L5-FOREST-BOUND",
        {"bipartite": bip_total, "fail": bip_bad, "tight": bip_tight,
         "false_control": false_control},
    )

    totals = {
        "connected": 0,
        "nonbipartite": 0,
        "l2": 0,
        "l3": 0,
        "l5": 0,
        "new_over_l3": 0,
        "post_l5": 0,
        "l5_lift_fail": 0,
    }
    new_examples = []
    residual_examples = []

    for n in range(3, 9):
        lines = base.graph6_lines(n, bipartite=False)
        if len(lines) != base.CONNECTED_COUNTS[n]:
            raise SystemExit(f"connected census mismatch at n={n}")
        totals["connected"] += len(lines)
        for g6 in lines:
            nn, adj = base.parse_g6(g6)
            full = (1 << nn) - 1
            if base.is_bipartite(adj, full):
                continue
            totals["nonbipartite"] += 1
            p = base.path_cover(adj, full)
            ell = nn - p
            o, octs = base.minimum_oct_masks(adj, full)
            l2 = l3 = l5 = lift = False
            best5 = -1
            best_record = None
            for tmask in octs:
                bmask = full ^ tmask
                ce, iso, smaller, delta, parts = base.component_profile(adj, bmask)
                r = pair_bonus(adj, bmask)
                tau_b = base.exact_tau(adj, bmask)
                threshold2 = 2 * ce - 1
                threshold3 = 2 * ce + delta - 1
                threshold5 = threshold3 + 2 * r
                slack = ell - (2 * tau_b + o + 1)
                l2 |= p <= threshold2
                l3 |= p <= threshold3
                l5 |= p <= threshold5
                lift |= slack >= 0
                if threshold5 > best5:
                    best5 = threshold5
                    best_record = (tmask, ce, iso, smaller, delta, r, parts, tau_b, slack)
            totals["l2"] += int(l2)
            totals["l3"] += int(l3)
            totals["l5"] += int(l5)
            totals["new_over_l3"] += int(l5 and not l3)
            totals["post_l5"] += int(not l5)
            if l5 and not lift:
                totals["l5_lift_fail"] += 1
                print("L5-IMPLICATION-FAIL", g6, nn, o, p, ell, best5, best_record)
            if l5 and not l3 and len(new_examples) < 20:
                new_examples.append((g6, nn, o, p, ell, best5, best_record))
            if not l5 and len(residual_examples) < 20:
                residual_examples.append((g6, nn, o, p, ell, best5, best_record))

    if totals["nonbipartite"] != 11859:
        raise SystemExit(f"nonbipartite census mismatch: {totals['nonbipartite']}")
    print("L5-COVERAGE", totals)
    print("L5-NEW-EXAMPLES", new_examples)
    print("POST-L5-EXAMPLES", residual_examples)

    if bip_bad or totals["l5_lift_fail"]:
        raise SystemExit("L5 regression failed")


if __name__ == "__main__":
    main()
