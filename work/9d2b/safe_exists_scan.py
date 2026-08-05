#!/usr/bin/env python3
"""Frozen SAFE-EXISTS/B-PLUS-2 continuation checker.

Usage: safe_exists_scan.py N [shard nshards] [--ces=real|always|never]

The bulk enumeration and A1 predicate use the frozen public-main engine.  New
grading is confined to A1-failing cycles: all minimizing successors are checked
for a CES minimizing step of length one, descent-compatible existence is
checked, and the frozen two-edge terminal-slide certificate is checked for each
cycle (universal, not selection-level).
"""
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))

import experiment_b as EB
import inv_b
from a1_verify import (PATHCAP, cyc_sets_edges, enum_shortest_paths, norm,
                       residual_dag, toggle)
from eval_L1_holdout import comps, feasible
from eval_frozen import min_fvs_all
from mine_n10 import walk_cycle

CES_MODE = "real"


def is_ces(Jp, Ccc, Jcyc, x, y):
    if CES_MODE == "always":
        return True
    if CES_MODE == "never":
        return False
    Jpc = cyc_sets_edges(Jp, x, y)
    return Ccc not in Jpc and Jpc <= Jcyc


def slides_from(nn, adj, Sset, x, y, J, a, Q0):
    """Frozen b_hslide.py two-edge terminal-slide construction."""
    t = Q0[-1]
    M0 = set(toggle(J, a, Q0))
    cap = {h: 2 for h in range(nn) if h not in Sset}
    cap[x] = 1
    cap[y] = 1
    deg = defaultdict(int)
    for u, v in M0:
        deg[u] += 1
        deg[v] += 1
    out = []
    for u in range(nn):
        if u not in Sset or not (adj[t] >> u & 1) or u in Q0:
            continue
        if (min(t, u), max(t, u)) not in M0:
            continue
        for tp in range(nn):
            if tp in Sset or tp in Q0 or tp == u:
                continue
            if not (adj[u] >> tp & 1):
                continue
            if (min(u, tp), max(u, tp)) in M0 or deg[tp] >= cap[tp]:
                continue
            out.append((Q0 + [u, tp], tp))
    return out


def successor_profile(nn, adj, Sset, x, y, J0):
    """Return (has_min_CES, has_length1_min_CES, selection_min_d0, capped)."""
    J0 = norm(J0)
    J0cyc = cyc_sets_edges(J0, x, y)
    if not J0cyc:
        return False, False, None, False
    has_min_ces = False
    has_one_ces = False
    selection_min = None
    capped = False
    for cc, iscy in comps(J0, (x, y)):
        if not iscy:
            continue
        Ccc = frozenset(cc)
        order, _ = walk_cycle(cc, J0, x, y)
        edata = []
        for ed in [e for kind, e in order if kind == "J"]:
            an = (min(ed), max(ed))
            s = ed[0] if ed[0] in Sset else ed[1]
            dg = residual_dag(nn, adj, Sset, x, y, J0, an, s)
            if dg is not None:
                edata.append((an, s, dg))
        if not edata:
            continue
        d0 = min(dg[0] for _, _, dg in edata)
        selection_min = d0 if selection_min is None else min(selection_min, d0)
        for an, s, (d, fw, td) in edata:
            if d != d0:
                continue
            paths = enum_shortest_paths(fw, s, td, d)
            if len(paths) >= PATHCAP:
                capped = True
            for path in paths:
                if is_ces(toggle(J0, an, path), Ccc, J0cyc, x, y):
                    has_min_ces = True
                    if d0 == 1:
                        has_one_ces = True
    return has_min_ces, has_one_ces, selection_min, capped


def witness(g6, Sset, x, y, J, cc, d0, extra=None):
    out = {"g6": g6, "S": sorted(Sset), "e": [x, y],
           "J": sorted(sorted(e) for e in J), "cycle": sorted(cc), "d0": d0}
    if extra:
        out.update(extra)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit("usage: safe_exists_scan.py N [shard nshards] [--ces=...]")
    n = int(args[0])
    shard = int(args[1]) if len(args) > 1 else 0
    nshards = int(args[2]) if len(args) > 2 else 1
    global CES_MODE
    for arg in sys.argv[1:]:
        if arg.startswith("--ces="):
            CES_MODE = arg.split("=", 1)[1]
    if CES_MODE not in {"real", "always", "never"}:
        raise SystemExit("invalid CES mode")

    t0 = time.time()
    counters = defaultdict(int)
    profile = defaultdict(int)
    failures = defaultdict(list)
    graph_total = None
    proc = subprocess.Popen(["geng", "-bc", "-q", str(n)],
                            stdout=subprocess.PIPE, text=True)
    for gi, raw in enumerate(proc.stdout):
        g6 = raw.strip()
        if not g6:
            continue
        counters["geng_graphs_seen"] += 1
        if gi % nshards != shard:
            continue
        counters["graphs_in_shard"] += 1
        nn, adj = inv_b.parse_g6(g6)
        k = EB.tau(nn, adj)
        if k < 2:
            continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S)
            Hv = [v for v in range(nn) if v not in Sset]
            Hedges = [(u, v) for ii, u in enumerate(Hv) for v in Hv[ii + 1:]
                      if adj[u] >> v & 1]
            for x, y in Hedges:
                sels = feasible(nn, adj, list(S), x, y)
                if not sels:
                    continue
                for J in sels:
                    cycs = [cc for cc, iscy in comps(J, (x, y)) if iscy]
                    if not cycs:
                        continue
                    counters["cyclic_selections"] += 1
                    Jcyc = cyc_sets_edges(norm(J), x, y)
                    nc = len(Jcyc)
                    a1_good = 0
                    a1_bad = 0
                    for cc in cycs:
                        counters["cycle_components"] += 1
                        Ccc = frozenset(cc)
                        order, _ = walk_cycle(cc, J, x, y)
                        edata = []
                        for ed in [e for kind, e in order if kind == "J"]:
                            an = (min(ed), max(ed))
                            s = ed[0] if ed[0] in Sset else ed[1]
                            h = ed[1] if ed[0] in Sset else ed[0]
                            dg = residual_dag(nn, adj, Sset, x, y, J, an, s)
                            if dg is not None:
                                edata.append((an, s, h, dg))
                        if not edata:
                            counters["lemmaA_violations"] += 1
                            if len(failures["lemmaA"]) < 40:
                                failures["lemmaA"].append(
                                    witness(g6, Sset, x, y, J, cc, None))
                            continue
                        d0 = min(dg[0] for _, _, _, dg in edata)
                        A0 = [row for row in edata if row[3][0] == d0]
                        ces_short = False
                        bad_short = []
                        for an, s, h, (d, fw, td) in A0:
                            paths = enum_shortest_paths(fw, s, td, d)
                            if len(paths) >= PATHCAP:
                                counters["path_cap_hits"] += 1
                            for path in paths:
                                if is_ces(toggle(J, an, path), Ccc, Jcyc, x, y):
                                    ces_short = True
                                else:
                                    bad_short.append((an, s, h, path))
                        if ces_short:
                            a1_good += 1
                            continue

                        a1_bad += 1
                        counters["a1_failures"] += 1
                        counters["bad_first_steps"] += len(bad_short)
                        terminal_ok = False
                        hslide_ok = False
                        all_succ_one = True
                        all_succ_min = True
                        some_one_descent = False
                        some_min_descent = False
                        succ_rows = []
                        for an, s, h, path in bad_short:
                            J0 = toggle(J, an, path)
                            nc0 = len(cyc_sets_edges(J0, x, y))
                            min_ok, one_ok, succ_d0, cap = successor_profile(
                                nn, adj, Sset, x, y, J0)
                            if cap:
                                counters["path_cap_hits"] += 1
                            all_succ_min = all_succ_min and min_ok
                            all_succ_one = all_succ_one and one_ok and succ_d0 == 1
                            if min_ok and nc0 <= nc:
                                some_min_descent = True
                            if one_ok and succ_d0 == 1 and nc0 <= nc:
                                some_one_descent = True
                            succ_rows.append({"path": path, "ncyc0": nc0,
                                              "d0min0": succ_d0,
                                              "min_ces0": min_ok,
                                              "one_ces0": one_ok})
                            for slid, tp in slides_from(
                                    nn, adj, Sset, x, y, J, an, path):
                                if is_ces(toggle(J, an, slid), Ccc, Jcyc, x, y):
                                    terminal_ok = True
                                    if tp == h:
                                        hslide_ok = True

                        if not terminal_ok:
                            counters["terminal_slide_failures"] += 1
                        else:
                            counters["bplus2_certified_bad_cycles"] += 1
                        if not hslide_ok:
                            counters["h_slide_failures"] += 1
                        if not all_succ_min:
                            counters["sd_2step_all_failures"] += 1
                        if not some_min_descent:
                            counters["safe_2_exists_local_failures"] += 1
                        if not all_succ_one:
                            counters["successor_one_all_failures"] += 1
                        if not some_one_descent:
                            counters["successor_one_descent_failures"] += 1
                        for key, failed in (
                            ("terminal_slide", not terminal_ok),
                            ("sd_2step_all", not all_succ_min),
                            ("safe_2_exists_local", not some_min_descent),
                            ("successor_one_all", not all_succ_one),
                            ("successor_one_descent", not some_one_descent),
                        ):
                            if failed and len(failures[key]) < 40:
                                failures[key].append(witness(
                                    g6, Sset, x, y, J, cc, d0,
                                    {"ncyc": nc, "successors": succ_rows}))
                    if a1_bad:
                        profile[(len(cycs), a1_good)] += 1
                    if a1_good == 0 and a1_bad:
                        counters["sd_short_failures"] += 1
    proc.wait()
    graph_total = counters["geng_graphs_seen"]
    result = {
        "n": n, "shard": shard, "nshards": nshards,
        "ces_mode": CES_MODE, "geng_graphs_total": graph_total,
        "counters": dict(counters),
        "a1bad_profile": {f"{a}|{b}": v for (a, b), v in sorted(profile.items())},
        "failures": dict(failures),
        "wall_seconds": round(time.time() - t0, 3),
    }
    outdir = Path(__file__).resolve().parent / "results"
    outdir.mkdir(exist_ok=True)
    tag = f"n{n}-{shard}of{nshards}-{CES_MODE}"
    outpath = outdir / f"safe-{tag}.json"
    outpath.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"output": str(outpath), **result}, sort_keys=True))


if __name__ == "__main__":
    main()
