#!/usr/bin/env python3
"""Verify the CX family at m = 3 and m = 4.

CX(m), n = 2m + 5: left leaves l1..lm ~ hubs h1,h2; right leaves r1..rm ~
hubs h3,h4; glue edges {h1,h2} x {h3,h4}; apex t ~ {l1, l2, h1, h2}.
CX(3) is CX11 = J??FF?^FuE?.

Asserted for each m: connected, nonbipartite, o = 1, unique minimum OCT
{t}; B = G - t is balanced (m+2 / m+2), one edge-component, r = 0, g = 1
(all same-side codegrees >= 2), so every threshold L2/L3/L5/L6 equals 1;
p(G) >= 2 (computed exactly), hence NO minimum OCT satisfies any of the
conditions; exact LIFT-A holds.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l6scan import (from_edges, bipartition_of, components, bip_stats,
                    path_cover, min_octs, tau_of)


def build(m):
    # vertices: 0..m-1 left leaves, m..m+1 left hubs, m+2..2m+1 right leaves,
    # 2m+2..2m+3 right hubs, 2m+4 apex
    h1, h2 = m, m + 1
    r0 = m + 2
    h3, h4 = 2 * m + 2, 2 * m + 3
    t = 2 * m + 4
    E = []
    for l in range(m):
        E += [(l, h1), (l, h2)]
    for r in range(r0, r0 + m):
        E += [(r, h3), (r, h4)]
    E += [(h1, h3), (h1, h4), (h2, h3), (h2, h4)]
    E += [(0, t), (1, t), (h1, t), (h2, t)]
    return from_edges(2 * m + 5, E), t


def check(m):
    (n, adj), t = build(m)
    full = (1 << n) - 1
    assert len(components(n, adj, full)) == 1
    ok, _ = bipartition_of(n, adj, full)
    assert not ok
    o, octs = min_octs(n, adj)
    assert o == 1 and octs == [1 << t], "unique minimum OCT {t}"
    p = path_cover(n, adj)
    ell = n - p
    bm = full ^ (1 << t)
    tau_b = tau_of(n, adj, bm)
    c_e, i, M, Delta, r, g = bip_stats(n, adj, bm)
    assert (c_e, i, Delta, r, g) == (1, 0, 0, 0, 1), (c_e, i, Delta, r, g)
    thr = 2 * c_e + Delta + 2 * r - 1          # = L2=L3=L5 threshold
    thr6 = Delta + 2 * g - 1
    assert thr == 1 and thr6 == 1
    assert p >= 2, p                            # condition fails for the only OCT
    assert ell >= 2 * tau_b + o + 1             # exact LIFT-A still holds
    print(f"CX(m={m}) n={n}: unique OCT, p={p}, tau(B)={tau_b}, "
          f"thresholds L2..L6 = 1 < p -> ALL CONDITIONS FAIL; "
          f"exact LIFT-A slack {ell - (2*tau_b + o + 1)}")


if __name__ == "__main__":
    for m in (3, 4):
        check(m)
    print("CX FAMILY CHECKS PASS (m=3,4)")
