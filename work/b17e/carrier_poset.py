#!/usr/bin/env python3
"""Frozen checker for PREREG-CARRIER-POSET.md.

Modes:
  controls  parse O-56/O-63/O-64 and locate a known-false PDIS system
  scan      exhaustive carrier.gen_exhaustive(3,5) target universe

No target scan is performed in controls mode.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "work"))
import carrier as C


def structure(S, H, nbH, cap):
    """Return CP/ADJ data for every forced-core cycle in one feasible system."""
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in H}
    sels = C.feasible_selections(S, nbH, cap)
    if not sels:
        return []
    forced, cycles = C.forced_and_cycles(S, sels)
    if not cycles:
        return []
    tights, mind = C.tight_sets(S, nbH, nbS, cap)
    if mind < 0:
        raise AssertionError("feasible enumerator disagrees with Hall deficit")

    out = []
    for comp in cycles:
        order = C.walk_cycle(comp, forced)
        P = [v[1] for v in order if v[0] == "S"]
        A = {}
        for s in P:
            candidates = [X for X in tights if s in X]
            carrier = min(candidates, key=lambda X: (len(X), tuple(sorted(map(str, X)))))
            if not all(carrier <= X for X in candidates):
                raise AssertionError(f"canonical carrier failure at {s}")
            A[s] = carrier

        B = {s: A[s] - {s} for s in P}
        U = frozenset().union(*(B[s] for s in P))
        arcs = {(s, t) for s in P for t in P if s != t and t in B[s]}

        cp_failures = []
        for s, t in sorted(arcs, key=lambda z: tuple(map(str, z))):
            if not A[t] < A[s]:
                cp_failures.append(("strict-descent", s, t))

        # Independent directed-cycle check rather than inferring it from sizes.
        state = {s: 0 for s in P}

        def visit(s):
            state[s] = 1
            for a, t in arcs:
                if a != s:
                    continue
                if state[t] == 1:
                    return True
                if state[t] == 0 and visit(t):
                    return True
            state[s] = 2
            return False

        has_directed_cycle = any(state[s] == 0 and visit(s) for s in P)
        if has_directed_cycle:
            cp_failures.append(("directed-cycle",))

        maximal = {
            t for t in P
            if not any(A[t] < A[s] for s in P if s != t)
        }
        outside = set(P) - set(U)
        if outside != maximal:
            cp_failures.append(("maximal-characterization", sorted(map(str, outside)),
                                sorted(map(str, maximal))))
        if not outside:
            cp_failures.append(("outside-empty",))
        if len({frozenset(A[s]) for s in P}) != len(P):
            cp_failures.append(("carriers-not-distinct",))

        adjacent = any(
            P[i] in outside and P[(i + 1) % len(P)] in outside
            for i in range(len(P))
        )
        out.append({
            "P": P,
            "A": A,
            "U": U,
            "outside": outside,
            "arcs": arcs,
            "cp_failures": cp_failures,
            "adjacent": adjacent,
            "forced": forced,
        })
    return out


def from_witness(name):
    data = json.loads((ROOT / "tools" / "witnesses" / name).read_text())
    S = list(data["vertices"]["S"])
    H = list(data["vertices"]["H"])
    nbH = {s: set() for s in S}
    for s, h in data["incidence_edges_S_H"]:
        nbH[s].add(h)
    c1 = set(data["capacities"].get("c1_vertices", data["distinguished_edge"]))
    cap = {h: (1 if h in c1 else 2) for h in H}
    return S, H, nbH, cap


def certificate(S, H, nbH, cap, rec):
    return {
        "S": list(S),
        "H": list(H),
        "nbH": {str(s): sorted(nbH[s], key=str) for s in S},
        "cap": {str(h): cap[h] for h in H},
        "P": list(rec["P"]),
        "A": {str(s): sorted(rec["A"][s], key=str) for s in rec["P"]},
        "U": sorted(rec["U"], key=str),
        "P_minus_U": sorted(rec["outside"], key=str),
        "arcs": sorted([list(a) for a in rec["arcs"]], key=str),
    }


def controls():
    for name in ("O-56.json", "O-63.json", "O-64.json"):
        args = from_witness(name)
        records = structure(*args)
        assert records, f"{name}: forced cycle not detected"
        assert all(not r["cp_failures"] for r in records), name
        assert all(not (set(r["P"]) & set(r["U"])) for r in records), name
        print(f"POSITIVE_CONTROL {name}: cycles={len(records)} CP=PASS PDIS=PASS")

    # PDIS is a published false companion. Locate one control without invoking
    # the target scan/reporting logic or evaluating ADJ as a verdict.
    for S, H, nbH, cap in C.gen_exhaustive(3, 5):
        records = structure(S, H, nbH, cap)
        for rec in records:
            if set(rec["P"]) & set(rec["U"]):
                print("NEGATIVE_CONTROL PDIS_FIRED " +
                      json.dumps(certificate(S, H, nbH, cap, rec), sort_keys=True))
                return
    raise AssertionError("negative PDIS control did not fire")


def scan():
    systems = cyclic = pdis = cp_fails = adj_fails = 0
    first_cp = first_adj = None
    for S, H, nbH, cap in C.gen_exhaustive(3, 5):
        systems += 1
        records = structure(S, H, nbH, cap)
        if not records:
            continue
        cyclic += 1
        # The published universe has at most one forced-cycle component per
        # retained system; fail closed if the accounting assumption changes.
        if len(records) != 1:
            raise AssertionError("multiple forced cycles in one target system")
        rec = records[0]
        if set(rec["P"]) & set(rec["U"]):
            pdis += 1
        if rec["cp_failures"]:
            cp_fails += 1
            if first_cp is None:
                first_cp = certificate(S, H, nbH, cap, rec)
                first_cp["failures"] = rec["cp_failures"]
        if not rec["adjacent"]:
            adj_fails += 1
            if first_adj is None:
                first_adj = certificate(S, H, nbH, cap, rec)

    print(f"TARGET systems={systems} cyclic={cyclic} pdis={pdis} "
          f"CP_fail={cp_fails} ADJ_fail={adj_fails}")
    if first_cp is not None:
        print("FIRST_CP_FAIL " + json.dumps(first_cp, sort_keys=True))
    if first_adj is not None:
        print("FIRST_ADJ_FAIL " + json.dumps(first_adj, sort_keys=True))

    assert systems == 115774, systems
    assert cyclic == 798, cyclic
    assert pdis == 18, pdis


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "controls"
    if mode == "controls":
        controls()
    elif mode == "scan":
        scan()
    else:
        raise SystemExit("usage: carrier_poset.py [controls|scan]")
