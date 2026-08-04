#!/usr/bin/env python3
"""Regression checker for L4 and combined L3+L4 coverage through n=8."""

from __future__ import annotations

import hashlib
from pathlib import Path

import lift_residual as base


EXPECTED_BASE_SHA = "78b7a981b113b627b77fcefff483d3d39b288145748ab0fcad30aadbcc507bb6"


def main():
    base_path = Path(__file__).with_name("lift_residual.py")
    actual = hashlib.sha256(base_path.read_bytes()).hexdigest()
    if actual != EXPECTED_BASE_SHA:
        raise SystemExit(f"base checker hash mismatch: {actual}")

    totals = {
        "connected": 0,
        "nonbipartite": 0,
        "l3": 0,
        "post_l3": 0,
        "l4": 0,
        "l4_on_post_l3": 0,
        "combined": 0,
        "l4_lift_fail": 0,
        "false_plus_one_control": 0,
    }
    post_l3 = []

    for n in range(3, 9):
        lines = base.graph6_lines(n, bipartite=False)
        expected = base.CONNECTED_COUNTS[n]
        if len(lines) != expected:
            raise SystemExit(f"connected census mismatch n={n}: {len(lines)} != {expected}")
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
            l3 = False
            l4 = False
            lift = False
            l4_records = []

            for tmask in octs:
                bmask = full ^ tmask
                ce, iso, smaller, delta, parts = base.component_profile(adj, bmask)
                tau_b = base.exact_tau(adj, bmask)
                l3_here = p <= 2 * ce + delta - 1
                l4_here = o <= 2 and tau_b == 0
                slack = ell - (2 * tau_b + o + 1)
                l3 |= l3_here
                l4 |= l4_here
                lift |= slack >= 0
                if l4_here:
                    l4_records.append((tmask, ce, iso, smaller, delta, parts, tau_b, slack))

            totals["l3"] += int(l3)
            totals["post_l3"] += int(not l3)
            totals["l4"] += int(l4)
            totals["l4_on_post_l3"] += int(l4 and not l3)
            totals["combined"] += int(l3 or l4)
            if l4 and not lift:
                totals["l4_lift_fail"] += 1
                print("L4-IMPLICATION-FAIL", g6, nn, o, p, ell, l4_records)
            if l4 and ell < o + 2:
                totals["false_plus_one_control"] += 1
            if not l3:
                post_l3.append((g6, nn, o, p, ell, l4, l4_records))

    if totals["nonbipartite"] != 11859:
        raise SystemExit(f"nonbipartite census mismatch: {totals['nonbipartite']}")
    if totals["false_plus_one_control"] == 0:
        raise SystemExit("false strengthening control did not fire")

    print("L4-COVERAGE", totals)
    print("POST-L3-DETAIL", post_l3)

    if totals["l4_lift_fail"]:
        raise SystemExit("L4 implication failure detected")


if __name__ == "__main__":
    main()
