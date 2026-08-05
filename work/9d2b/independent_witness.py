#!/usr/bin/env python3
"""Independent VERIFY-2 recheck of the first n=12 mechanism witness."""
import hashlib
import json
import subprocess
import types
from collections import defaultdict
from pathlib import Path

VERIFY_COMMIT = "6a94cb9b8b137249d6a19f25589112c09fdca9ee"
VERIFY_PATH = "verify_independent/verify2/sdverify2.py"
G6 = "K??FFbw}Fw^_"
S_VERTICES = [6, 7, 8, 9, 10]
EDGE = (4, 11)
J_VERTICES = [(0, 6), (0, 7), (1, 6), (1, 7), (2, 8),
              (2, 9), (3, 8), (3, 9), (4, 10), (5, 10)]
C_VERTICES = {0, 1, 6, 7}


def load_verify_engine():
    p = subprocess.run(["git", "show", f"{VERIFY_COMMIT}:{VERIFY_PATH}"],
                       check=True, capture_output=True)
    mod = types.ModuleType("sdverify2_fixed")
    exec(compile(p.stdout, f"{VERIFY_COMMIT}:{VERIFY_PATH}", "exec"), mod.__dict__)
    return mod, hashlib.sha256(p.stdout).hexdigest()


def bounded_paths(v, inst, selset, load, a, limit):
    i0, h0 = a
    sel = selset - {a}
    residual_load = list(load)
    residual_load[h0] -= 1
    out = []
    used_s = {i0}
    used_h = set()

    def rec(i, depth, sofar):
        if depth >= limit:
            return
        for h in inst.inc[i]:
            ed = (i, h)
            if ed in sel or ed == a or h in used_h:
                continue
            used_h.add(h)
            path = sofar + [ed]
            if residual_load[h] < inst.cap[h]:
                out.append(path)
            for j in inst.users[h]:
                if (j, h) in sel and j not in used_s:
                    used_s.add(j)
                    rec(j, depth + 2, path + [(j, h)])
                    used_s.remove(j)
            used_h.remove(h)

    rec(i0, 0, [])
    return out


def successor_profile(v, inst, forced, selset):
    cycles = v.cycle_components(inst, selset)
    old = set(cycles)
    load = inst.loads(selset)
    selection_d0 = v.INF
    min_ces = False
    for cycle in cycles:
        info = []
        for a in [e for e in cycle if e not in forced]:
            d, ds, dh, tg = v.bfs_residual(inst, selset, load, a)
            if d < v.INF:
                info.append((a, d, ds, dh, tg))
        if not info:
            continue
        d0 = min(row[1] for row in info)
        selection_d0 = min(selection_d0, d0)
        for a, d, ds, dh, tg in info:
            if d != d0:
                continue
            for path in v.enum_paths(inst, selset, a, ds, dh, tg, [0]):
                ok, _ = v.is_ces(inst, old, v.toggle(selset, a, path), cycle)
                min_ces = min_ces or ok
    return selection_d0, min_ces


def main():
    v, engine_hash = load_verify_engine()
    nn, adj = v.g6_decode(G6)
    smask = sum(1 << s for s in S_VERTICES)
    tau, fvss = v.min_fvs_all(adj, nn)
    inst = v.Inst(adj, nn, smask, EDGE)
    sidx = {vertex: i for i, vertex in enumerate(inst.S)}
    hidx = {vertex: i for i, vertex in enumerate(inst.H)}

    def incidence(edge):
        u, w = edge
        s, h = (u, w) if u in sidx else (w, u)
        return sidx[s], hidx[h]

    selset = frozenset(incidence(e) for e in J_VERTICES)
    target = frozenset(incidence(e) for e in J_VERTICES
                       if e[0] in C_VERTICES and e[1] in C_VERTICES)
    all_sels = {inst.sel_of(choice) for choice in inst.selections()}
    cycles = v.cycle_components(inst, selset)
    forced = inst.forced_set()
    load = inst.loads(selset)
    old = set(cycles)

    info = []
    for a in [e for e in target if e not in forced]:
        d, ds, dh, tg = v.bfs_residual(inst, selset, load, a)
        if d < v.INF:
            info.append((a, d, ds, dh, tg))
    d0 = min(row[1] for row in info)
    steps = []
    shortest_ces = 0
    terminal_repairs = 0
    successor_rows = []
    for a, d, ds, dh, tg in info:
        if d != d0:
            continue
        for path in v.enum_paths(inst, selset, a, ds, dh, tg, [0]):
            steps.append((a, path))
            J0 = v.toggle(selset, a, path)
            ok, _ = v.is_ces(inst, old, J0, target)
            shortest_ces += int(ok)
            sd0, minces = successor_profile(v, inst, forced, J0)
            successor_rows.append({"d0": sd0, "min_ces": minces,
                                   "ncyc": len(v.cycle_components(inst, J0))})

            terminal = path[-1][1]
            used_s = {a[0]} | {edge[0] for edge in path}
            used_h = {edge[1] for edge in path}
            load0 = inst.loads(J0)
            for i in inst.users[terminal]:
                if (i, terminal) not in J0 or i in used_s:
                    continue
                for hp in inst.inc[i]:
                    if hp in used_h or (i, hp) in J0 or load0[hp] >= inst.cap[hp]:
                        continue
                    Jp = v.toggle(selset, a, path + [(i, terminal), (i, hp)])
                    slide_ok, _ = v.is_ces(inst, old, Jp, target)
                    terminal_repairs += int(slide_ok)

    best = v.INF
    bounded_count = 0
    for a in [e for e in target if e not in forced]:
        for path in bounded_paths(v, inst, selset, load, a, d0 + 2):
            bounded_count += 1
            ok, _ = v.is_ces(inst, old, v.toggle(selset, a, path), target)
            if ok:
                best = min(best, len(path))

    result = {
        "verify_commit": VERIFY_COMMIT,
        "verify_engine_sha256": engine_hash,
        "graph_n": nn,
        "tau": tau,
        "S_is_minimum_fvs": smask in fvss,
        "selection_feasible": selset in all_sels,
        "cycle_count": len(cycles),
        "target_present": target in cycles,
        "d0": d0,
        "minimizing_steps": len(steps),
        "shortest_ces": shortest_ces,
        "terminal_slide_repairs": terminal_repairs,
        "generic_paths_tested": bounded_count,
        "generic_first_ces": None if best == v.INF else best,
        "successors": successor_rows,
        "all_successor_d0_three": all(r["d0"] == 3 for r in successor_rows),
        "all_successor_min_ces": all(r["min_ces"] for r in successor_rows),
    }
    out = Path(__file__).resolve().parent / "results" / "independent-witness.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
