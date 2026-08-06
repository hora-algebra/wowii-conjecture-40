"""Phase-2 cross-check for SEALED-DERIVATION.md and LEMMA-A-CLEAN-END.md.

Controls run before targets.  The sealed verifier is not modified: this script
imports its finite-model primitives, reruns its controls and full target, and
then independently checks the alternative CS(b) proof of NC(ii) and the A-I+
deletion-degree step on the same explicit labeled universe.
"""

from itertools import combinations, product
from pathlib import Path

import verify_nc as V


def graph_acyclic(n, edges):
    parent = list(range(n))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True


def cycle_data(neigh, caps, forced, cycle):
    p_set, q_set, cyc = cycle
    _, carriers = V.carriers(neigh, caps, p_set)
    punctures = {p: carriers[p] & ~(1 << p) for p in p_set}
    u_mask = 0
    for b in punctures.values():
        u_mask |= b
    p_mask = sum(1 << p for p in p_set)
    return p_set, q_set, cyc, carriers, punctures, u_mask, p_mask


def ext_sets(neigh, p_set, q_set):
    return {
        p: {h for h in range(max(mask.bit_length() for mask in neigh))
            if neigh[p] >> h & 1 and h not in q_set}
        for p in p_set
    }


def ai_plus_degrees(neigh, p_set, q_set, cyc, q0):
    ext = ext_sets(neigh, p_set, q_set)
    clean_shape = (
        all(not ext[p] for p in cyc[q0])
        and all(len(ext[p]) <= 1 for p in p_set - cyc[q0])
    )
    if not clean_shape:
        return None, ext
    surviving = {
        p: len(ext[p]) + (1 if neigh[p] >> q0 & 1 else 0)
        for p in p_set
    }
    return surviving, ext


def phase2_controls():
    # Forest-extension detector: the degree-one guard is discriminating.
    assert graph_acyclic(4, [(0, 1), (1, 2), (2, 3)])
    assert not graph_acyclic(3, [(0, 1), (1, 2), (2, 0)])
    assert not graph_acyclic(4, [(0, 1), (1, 2), (3, 0), (3, 2)])

    # ADJ-1 from LEMMA-A-CARRIER-POSET.md.  q=1 is the clean A-I+ control.
    neigh = (0b011, 0b101, 0b111)
    caps = (2, 2, 2)
    selections = V.feasible_selections(neigh, caps)
    assert len(selections) == 1
    cycles = V.cycle_components(selections[0], 3, 3)
    assert len(cycles) == 1
    p_set, q_set, cyc, _, _, u_mask, _ = cycle_data(
        neigh, caps, selections[0], cycles[0]
    )
    assert V.degree_x(u_mask, 1, neigh) == 1
    surviving, ext = ai_plus_degrees(neigh, p_set, q_set, cyc, 1)
    assert all(not ext[p] for p in p_set)
    assert surviving == {0: 1, 1: 0, 2: 1}
    assert all(d <= 1 for d in surviving.values())
    # q=0 is the dirty chord control and must be excluded by the clean guard.
    assert V.degree_x(u_mask, 0, neigh) == 2
    assert {p for p in p_set if neigh[p] >> 0 & 1} - cyc[0] == {2}

    # The three shipped witnesses must fail A-I+'s first Ext condition.
    expected_external = {
        "O-56.json": {0: {6}, 1: {6}},
        "O-63.json": {"s": {"h"}, "t": set()},
        "O-64.json": {"s": {"h"}, "t": set()},
    }
    base = Path(__file__).resolve().parent / "witnesses"
    for name, expected in expected_external.items():
        _, s_names, h_names, wn, wc = V.from_json(base / name)
        fs = V.feasible_selections(wn, wc)
        forced = fs[0]
        for j in fs[1:]:
            forced &= j
        cycles = V.cycle_components(forced, len(wn), len(wc))
        assert len(cycles) == 1
        p_set, q_set, _ = cycles[0]
        ext = ext_sets(wn, p_set, q_set)
        named = {
            s_names[p]: {h_names[h] for h in ext[p]}
            for p in p_set
        }
        assert named == expected
        assert all(any(ext[p] for p in cyc_q)
                   for _, _, cyc_map in cycles for cyc_q in cyc_map.values())
    print("PHASE2 CONTROLS PASS: ADJ clean A-I+ degrees 1/0/1; dirty chord "
          "excluded; O-56/O-63/O-64 Ext guards fail; forest negative fires")


def forest_extension_target():
    """Exhaust the pure final step of A-I+: leaves added to a forest stay acyclic."""
    checks = forests = 0
    for h_count in range(1, 6):
        possible_h_edges = list(combinations(range(h_count), 2))
        for edge_mask in range(1 << len(possible_h_edges)):
            h_edges = [edge for i, edge in enumerate(possible_h_edges)
                       if edge_mask >> i & 1]
            if not graph_acyclic(h_count, h_edges):
                continue
            forests += 1
            for p_count in range(4):
                # -1 means isolated; otherwise the P-vertex has one H-neighbour.
                for attachment in product(range(-1, h_count), repeat=p_count):
                    edges = list(h_edges)
                    for p, h in enumerate(attachment):
                        if h >= 0:
                            edges.append((h_count + p, h))
                    assert graph_acyclic(h_count + p_count, edges)
                    checks += 1
    print(f"FOREST EXTENSION PASS: forests={forests} leaf_attachment_checks={checks}")


def phase2_target():
    counts = {
        "systems": 0,
        "cyclic_systems": 0,
        "cycles": 0,
        "clean_q": 0,
        "dirty_q": 0,
        "chords": 0,
        "clean_end_nc": 0,
        "cs_b": 0,
        "ai_plus_pairs": 0,
        "ai_plus_systems": 0,
        "ai_plus_extension_only_pairs": 0,
        "ai_plus_degree_checks": 0,
    }
    for p_count in range(2, 4):
        for h_count in range(2, 6):
            possible_neigh = [mask for mask in range(1 << h_count)
                              if V.bitcount(mask) >= 2]
            for caps in V.capacity_patterns(h_count):
                for neigh in product(possible_neigh, repeat=p_count):
                    forced, selections = V.forced_edges_early(neigh, caps)
                    if forced is None:
                        continue
                    counts["systems"] += 1
                    if selections is None:
                        continue
                    counts["cyclic_systems"] += 1
                    system_has_ai_plus = False
                    cycles = V.cycle_components(forced, p_count, h_count)
                    for cycle in cycles:
                        counts["cycles"] += 1
                        p_set, q_set, cyc, _, _, u_mask, p_mask = cycle_data(
                            neigh, caps, forced, cycle
                        )
                        outside = {p for p in p_set if not (u_mask >> p & 1)}

                        # CLEAN-END proof (ii): CS(b) for both outside endpoints.
                        for q in q_set:
                            if cyc[q] <= outside:
                                assert V.degree_x(u_mask, q, neigh) == 0
                                counts["cs_b"] += 1

                        ext = ext_sets(neigh, p_set, q_set)
                        for q in q_set:
                            deg_u = V.degree_x(u_mask, q, neigh)
                            n_p = {p for p in p_set if neigh[p] >> q & 1}
                            chords = n_p - cyc[q]
                            counts["chords"] += len(chords)
                            if deg_u <= 1:
                                counts["clean_q"] += 1
                                # NC(i), NC(ii), and normalized consequence.
                                assert n_p == cyc[q]
                                aux = {p for p in range(p_count)
                                       if u_mask >> p & 1
                                       and not (p_mask >> p & 1)
                                       and neigh[p] >> q & 1}
                                assert not aux
                                n_tf = {p for p in range(p_count)
                                        if (p_mask | u_mask) >> p & 1
                                        and neigh[p] >> q & 1}
                                assert n_tf == cyc[q]
                                counts["clean_end_nc"] += 1

                                # A-I+: the checked conclusion is the only
                                # incidence-dependent step.  With H a forest,
                                # adjoining independent P-vertices of degree <=1
                                # preserves acyclicity.
                                surviving, ext_q = ai_plus_degrees(
                                    neigh, p_set, q_set, cyc, q
                                )
                                if surviving is not None:
                                    counts["ai_plus_pairs"] += 1
                                    system_has_ai_plus = True
                                    assert all(d <= 1 for d in surviving.values())
                                    counts["ai_plus_degree_checks"] += len(surviving)
                                    if any(ext_q[p] for p in p_set - cyc[q]):
                                        counts["ai_plus_extension_only_pairs"] += 1
                            else:
                                counts["dirty_q"] += 1
                                # All chords must lie outside NC's guard.
                                if chords:
                                    assert deg_u >= 2
                    if system_has_ai_plus:
                        counts["ai_plus_systems"] += 1

    assert counts["systems"] == 168_618, counts
    assert counts["cyclic_systems"] == 4_880, counts
    assert counts["cycles"] == 4_880, counts
    assert counts["clean_q"] + counts["dirty_q"] == 10_360, counts
    assert counts["clean_end_nc"] == counts["clean_q"], counts
    assert counts["ai_plus_pairs"] > 0, counts
    print("PHASE2 TARGET PASS: " + " ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    V.controls()
    phase2_controls()
    V.target()
    phase2_target()
    forest_extension_target()
