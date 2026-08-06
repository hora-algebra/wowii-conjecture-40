"""Independent finite oracle for STATEMENT.md (NC/NCM).

The target census is an explicit labeled abstract-carrier universe based on
LEMMA-A-CARRIER.md and LEMMA-A-CARRIER-POSET.md: 2 <= |S| <= 3,
2 <= |H| <= 5, every S-vertex has at least two H-neighbours, and capacities
are either all two or have exactly two capacity-one vertices.  Only feasible
systems enter the count.  Incidence-isolated H-vertices and disconnected
incidence graphs are retained.  The historical ``carrier.py`` generator is not
shipped in this package, so this deliberately does not claim to reproduce its
115,774-system universe.

Controls run before the target.  The checker uses only the finite selection
model: feasible selections are enumerated directly, forced incidences are
their intersection, and rho-tight sets/carriers are computed from definitions.
"""

from itertools import combinations, product
import json
from pathlib import Path


def bitcount(x):
    return bin(x).count("1")


def edge_bit(p, h, h_count):
    return 1 << (p * h_count + h)


def choices_for(mask):
    hs = [h for h in range(mask.bit_length()) if mask >> h & 1]
    return [sum(1 << h for h in pair) for pair in combinations(hs, 2)]


def selection_edges(choice_masks, h_count):
    edges = 0
    for p, hs in enumerate(choice_masks):
        for h in range(h_count):
            if hs >> h & 1:
                edges |= edge_bit(p, h, h_count)
    return edges


def feasible_selections(neigh, caps):
    """Return every feasible selection as a bit mask on S x H."""
    h_count = len(caps)
    per = [choices_for(mask) for mask in neigh]
    if any(not row for row in per):
        return []
    out = []
    loads = [0] * h_count
    picked = [0] * len(neigh)

    def rec(p):
        if p == len(neigh):
            out.append(selection_edges(picked, h_count))
            return
        for hs in per[p]:
            touched = []
            ok = True
            for h in range(h_count):
                if hs >> h & 1:
                    loads[h] += 1
                    touched.append(h)
                    if loads[h] > caps[h]:
                        ok = False
            if ok:
                picked[p] = hs
                rec(p + 1)
            for h in touched:
                loads[h] -= 1

    rec(0)
    return out


def forced_edges_early(neigh, caps):
    """Find forced edges; stop once their running intersection is acyclic.

    A further intersection cannot acquire a cycle, so an early acyclic result
    is exact for the predicate needed by the target census.
    """
    p_count, h_count = len(neigh), len(caps)
    per = [choices_for(mask) for mask in neigh]
    if any(not row for row in per):
        return None, None
    loads = [0] * h_count
    picked = [0] * p_count
    forced = None
    selections = []
    stopped_acyclic = False

    def rec(p):
        nonlocal forced, stopped_acyclic
        if stopped_acyclic:
            return
        if p == p_count:
            j = selection_edges(picked, h_count)
            selections.append(j)
            forced = j if forced is None else forced & j
            if not has_cycle(forced, p_count, h_count):
                stopped_acyclic = True
            return
        for hs in per[p]:
            if stopped_acyclic:
                break
            touched = []
            ok = True
            for h in range(h_count):
                if hs >> h & 1:
                    loads[h] += 1
                    touched.append(h)
                    if loads[h] > caps[h]:
                        ok = False
            if ok:
                picked[p] = hs
                rec(p + 1)
            for h in touched:
                loads[h] -= 1

    rec(0)
    if forced is None:
        return None, None
    if stopped_acyclic:
        return forced, None
    return forced, selections


def has_cycle(edges, p_count, h_count):
    parent = list(range(p_count + h_count))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p in range(p_count):
        for h in range(h_count):
            if edges & edge_bit(p, h, h_count):
                a, b = find(p), find(p_count + h)
                if a == b:
                    return True
                parent[a] = b
    return False


def cycle_components(edges, p_count, h_count):
    adj = {v: set() for v in range(p_count + h_count)}
    for p in range(p_count):
        for h in range(h_count):
            if edges & edge_bit(p, h, h_count):
                u, v = p, p_count + h
                adj[u].add(v)
                adj[v].add(u)
    seen = set()
    cycles = []
    for start in range(p_count + h_count):
        if start in seen or not adj[start]:
            continue
        stack = [start]
        comp = set()
        while stack:
            v = stack.pop()
            if v in comp:
                continue
            comp.add(v)
            stack.extend(adj[v] - comp)
        seen |= comp
        edge_count = sum(len(adj[v]) for v in comp) // 2
        if edge_count == len(comp):
            assert all(len(adj[v]) == 2 for v in comp)
            p_set = {v for v in comp if v < p_count}
            q_set = {v - p_count for v in comp if v >= p_count}
            cyc = {
                q: {p for p in p_set if p_count + q in adj[p]}
                for q in q_set
            }
            assert all(len(cyc[q]) == 2 for q in q_set)
            cycles.append((p_set, q_set, cyc))
    return cycles


def rho(x_mask, neigh, caps):
    return sum(
        min(caps[h], sum(1 for p in range(len(neigh))
                         if x_mask >> p & 1 and neigh[p] >> h & 1))
        for h in range(len(caps))
    )


def degree_x(x_mask, h, neigh):
    return sum(1 for p in range(len(neigh))
               if x_mask >> p & 1 and neigh[p] >> h & 1)


def tight_sets(neigh, caps):
    return [x for x in range(1 << len(neigh))
            if rho(x, neigh, caps) == 2 * bitcount(x)]


def carriers(neigh, caps, p_set):
    tight = tight_sets(neigh, caps)
    ans = {}
    for p in p_set:
        containing = [x for x in tight if x >> p & 1]
        assert containing
        a = (1 << len(neigh)) - 1
        for x in containing:
            a &= x
        assert a in tight
        ans[p] = a
    return tight, ans


def selected_load(j, x_mask, h, p_count, h_count):
    return sum(1 for p in range(p_count)
               if x_mask >> p & 1 and j & edge_bit(p, h, h_count))


def check_cycle(neigh, caps, selections, forced, cycle, counters):
    p_count, h_count = len(neigh), len(caps)
    p_set, q_set, cyc = cycle
    p_mask = sum(1 << p for p in p_set)
    tight, a = carriers(neigh, caps, p_set)
    b = {p: a[p] & ~(1 << p) for p in p_set}
    u_mask = 0
    for value in b.values():
        u_mask |= value

    # M1: cycle ends have capacity two and are saturated by their two forced edges.
    for q in q_set:
        assert caps[q] == 2
        for j in selections:
            assert selected_load(j, p_mask, q, p_count, h_count) == 2
    counters["M1_cycle_capacity_and_load"] += len(q_set)

    # M2: canonical-carrier and punctured-tightness predicates.
    for p in p_set:
        ends = {q for q in q_set if p in cyc[q]}
        assert len(ends) == 2
        assert b[p] in tight
        exposed = {h for h in range(h_count)
                   if neigh[p] >> h & 1 and degree_x(a[p], h, neigh) <= caps[h]}
        assert exposed == ends
        for h in range(h_count):
            if neigh[p] >> h & 1 and h not in ends:
                assert degree_x(a[p], h, neigh) >= caps[h] + 1
        counters["M2_carrier_puncture"] += 1

    # M3: tight-set saturation, checked for every tight X, feasible J, and h.
    for x in tight:
        for j in selections:
            for h in range(h_count):
                assert selected_load(j, x, h, p_count, h_count) == min(
                    caps[h], degree_x(x, h, neigh)
                )
                counters["M3_tight_saturation"] += 1

    # M4: the exact punctured-tightness implication used for NC(i).
    for q in q_set:
        for p in p_set - cyc[q]:
            if neigh[p] >> q & 1:
                assert degree_x(b[p], q, neigh) >= 2
                assert degree_x(u_mask, q, neigh) >= 2
                counters["M4_extra_P_forces_U_degree_two"] += 1

    # M5/M6: NC and both stated consequences at every eligible q.
    eligible = 0
    for q in q_set:
        deg_u = degree_x(u_mask, q, neigh)
        if deg_u > 1:
            continue
        eligible += 1
        n_p = {p for p in p_set if neigh[p] >> q & 1}
        n_aux = {p for p in range(p_count)
                 if u_mask >> p & 1 and not (p_mask >> p & 1)
                 and neigh[p] >> q & 1}
        assert n_p == cyc[q]
        assert not n_aux
        assert deg_u == len(cyc[q] & {p for p in range(p_count) if u_mask >> p & 1})
        n_normalized = {p for p in range(p_count)
                        if ((p_mask | u_mask) >> p & 1) and neigh[p] >> q & 1}
        assert n_normalized == cyc[q]
        counters["M5_M6_NC_and_consequences"] += 1
    assert eligible > 0

    # M7: CP, CS(a), and NCM.
    for s in p_set:
        for t in p_set - {s}:
            if b[s] >> t & 1:
                assert a[t] & ~a[s] == 0
                assert a[t] != a[s]
    maximal = {t for t in p_set
               if not any(t != s and a[t] & ~a[s] == 0 and a[t] != a[s]
                          for s in p_set)}
    outside = {p for p in p_set if not (u_mask >> p & 1)}
    assert outside == maximal
    assert outside
    for p in outside:
        ends = {q for q in q_set if p in cyc[q]}
        for q in ends:
            assert degree_x(u_mask, q, neigh) <= 1
            n_normalized = {s for s in range(p_count)
                            if ((p_mask | u_mask) >> s & 1) and neigh[s] >> q & 1}
            assert n_normalized == cyc[q]
            assert len(n_normalized) == 2
            counters["M7_CP_CS_NCM"] += 1

    counters["cycles"] += 1
    if p_mask & u_mask:
        counters["pdis_false"] += 1


def from_json(path):
    data = json.loads(path.read_text())
    s_names = data["vertices"]["S"]
    h_names = data["vertices"]["H"]
    si = {name: i for i, name in enumerate(s_names)}
    hi = {name: i for i, name in enumerate(h_names)}
    neigh = [0] * len(s_names)
    for s, h in data["incidence_edges_S_H"]:
        neigh[si[s]] |= 1 << hi[h]
    c1 = set(data["capacities"]["c1_vertices"])
    caps = tuple(1 if h in c1 else 2 for h in h_names)
    return data, s_names, h_names, neigh, caps


def controls():
    # Acyclic forced-core control: unique selection, but its forced graph is a path.
    neigh = (0b011, 0b110)
    caps = (2, 2, 2)
    fs = feasible_selections(neigh, caps)
    assert len(fs) == 1 and not has_cycle(fs[0], 2, 3)

    # ADJ-WITNESS from LEMMA-A-CARRIER-POSET.md.  It must falsify both
    # P-disjointness and NC(i) with the degree threshold removed.
    neigh = (0b011, 0b101, 0b111)
    caps = (2, 2, 2)
    fs = feasible_selections(neigh, caps)
    assert len(fs) == 1
    forced = fs[0]
    cycles = cycle_components(forced, 3, 3)
    assert len(cycles) == 1
    p_set, q_set, cyc = cycles[0]
    tight, a = carriers(neigh, caps, p_set)
    assert set(tight) == {0b000, 0b001, 0b010, 0b011, 0b111}
    assert a == {0: 0b001, 1: 0b010, 2: 0b111}
    u = (a[0] & ~0b001) | (a[1] & ~0b010) | (a[2] & ~0b100)
    assert u == 0b011 and u & 0b111
    bad_without_threshold = [q for q in q_set
                             if {p for p in p_set if neigh[p] >> q & 1} != cyc[q]]
    assert bad_without_threshold == [0]
    assert degree_x(u, 0, neigh) == 2

    # The three shipped warning witnesses are independent package controls for
    # feasible-selection counts, forced cycles, and documented carriers.
    base = Path(__file__).resolve().parent / "witnesses"
    expected = {
        "O-56.json": (1, {0: {0, 2, 3}, 1: {1, 2, 3}}),
        "O-63.json": (6, {0: {"s", "u", "a", "b"}}),
        "O-64.json": (1, {0: {"s", "u"}}),
    }
    for name, (count, documented) in expected.items():
        data, s_names, h_names, neigh, caps = from_json(base / name)
        fs = feasible_selections(neigh, caps)
        assert len(fs) == count
        forced = fs[0]
        for j in fs[1:]:
            forced &= j
        cycles = cycle_components(forced, len(neigh), len(caps))
        assert cycles
        p_set = cycles[0][0]
        _, a = carriers(neigh, caps, p_set)
        for p, aset in documented.items():
            assert {s_names[i] for i in range(len(s_names)) if a[p] >> i & 1} == aset
    print("CONTROLS PASS: acyclic detector; ADJ threshold/PDIS controls fired; "
          "O-56/O-63/O-64 counts, cycles, carriers reproduced")


def capacity_patterns(h_count):
    yield (2,) * h_count
    for a, b in combinations(range(h_count), 2):
        yield tuple(1 if h in (a, b) else 2 for h in range(h_count))


def target():
    counters = {
        "systems": 0,
        "cyclic_systems": 0,
        "cycles": 0,
        "pdis_false": 0,
        "M1_cycle_capacity_and_load": 0,
        "M2_carrier_puncture": 0,
        "M3_tight_saturation": 0,
        "M4_extra_P_forces_U_degree_two": 0,
        "M5_M6_NC_and_consequences": 0,
        "M7_CP_CS_NCM": 0,
    }
    for p_count in range(2, 4):
        for h_count in range(2, 6):
            possible_neigh = [mask for mask in range(1 << h_count)
                              if bitcount(mask) >= 2]
            for caps in capacity_patterns(h_count):
                for neigh in product(possible_neigh, repeat=p_count):
                    forced, selections = forced_edges_early(neigh, caps)
                    if forced is None:
                        continue
                    counters["systems"] += 1
                    if selections is None:
                        continue
                    cycles = cycle_components(forced, p_count, h_count)
                    assert cycles
                    counters["cyclic_systems"] += 1
                    for cycle in cycles:
                        check_cycle(neigh, caps, selections, forced, cycle, counters)
    assert counters["systems"] == 168_618, counters
    assert counters["cyclic_systems"] == 4_880, counters
    assert counters["pdis_false"] == 450, counters
    print("TARGET PASS: " + " ".join(f"{k}={v}" for k, v in counters.items()))


if __name__ == "__main__":
    controls()
    target()
