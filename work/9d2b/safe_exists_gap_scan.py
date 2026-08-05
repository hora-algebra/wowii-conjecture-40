#!/usr/bin/env python3
"""Frozen multi-cycle gap-closure scan for universal n=12 B-PLUS-2.

Usage: safe_exists_gap_scan.py N [shard nshards]

The logical scope reduction is preregistered in PREREG-SAFE-EXISTS-GAP.md.
"""
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import safe_exists_scan as core


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: safe_exists_gap_scan.py N [shard nshards]")
    n = int(sys.argv[1])
    shard = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    nshards = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    t0 = time.time()
    ctr = defaultdict(int)
    profile = defaultdict(int)
    failures = defaultdict(list)

    proc = subprocess.Popen(["geng", "-bc", "-q", str(n)],
                            stdout=subprocess.PIPE, text=True)
    for gi, raw in enumerate(proc.stdout):
        g6 = raw.strip()
        if not g6:
            continue
        ctr["geng_graphs_seen"] += 1
        if gi % nshards != shard:
            continue
        ctr["graphs_in_shard"] += 1
        nn, adj = core.inv_b.parse_g6(g6)
        k = core.EB.tau(nn, adj)
        if k < 2:
            continue
        for S in core.min_fvs_all(nn, adj, k):
            Sset = set(S)
            Hv = [v for v in range(nn) if v not in Sset]
            Hedges = [(u, v) for ii, u in enumerate(Hv) for v in Hv[ii + 1:]
                      if adj[u] >> v & 1]
            for x, y in Hedges:
                sels = core.feasible(nn, adj, list(S), x, y)
                if not sels:
                    continue
                for J in sels:
                    cycs = [cc for cc, iscy in core.comps(J, (x, y)) if iscy]
                    if len(cycs) < 2:
                        continue
                    ctr["multi_cyclic_selections"] += 1
                    Jcyc = core.cyc_sets_edges(core.norm(J), x, y)
                    nc = len(Jcyc)
                    a1_good = 0
                    a1_bad = 0
                    for cc in cycs:
                        ctr["cycle_components"] += 1
                        Ccc = frozenset(cc)
                        order, _ = core.walk_cycle(cc, J, x, y)
                        edata = []
                        for ed in [e for kind, e in order if kind == "J"]:
                            an = (min(ed), max(ed))
                            s = ed[0] if ed[0] in Sset else ed[1]
                            h = ed[1] if ed[0] in Sset else ed[0]
                            dg = core.residual_dag(
                                nn, adj, Sset, x, y, J, an, s)
                            if dg is not None:
                                edata.append((an, s, h, dg))
                        if not edata:
                            ctr["lemmaA_violations"] += 1
                            if len(failures["lemmaA"]) < 40:
                                failures["lemmaA"].append(core.witness(
                                    g6, Sset, x, y, J, cc, None))
                            continue
                        d0 = min(dg[0] for _, _, _, dg in edata)
                        ces_short = False
                        bad_short = []
                        for an, s, h, (d, fw, td) in edata:
                            if d != d0:
                                continue
                            paths = core.enum_shortest_paths(fw, s, td, d)
                            if len(paths) >= core.PATHCAP:
                                ctr["path_cap_hits"] += 1
                            for path in paths:
                                if core.is_ces(
                                        core.toggle(J, an, path), Ccc, Jcyc, x, y):
                                    ces_short = True
                                else:
                                    bad_short.append((an, s, h, path))
                        if ces_short:
                            a1_good += 1
                            continue

                        a1_bad += 1
                        ctr["a1_failures"] += 1
                        ctr["bad_first_steps"] += len(bad_short)
                        terminal_ok = False
                        hslide_ok = False
                        all_succ_one = True
                        all_succ_min = True
                        some_one_descent = False
                        some_min_descent = False
                        succ_rows = []
                        for an, s, h, path in bad_short:
                            J0 = core.toggle(J, an, path)
                            nc0 = len(core.cyc_sets_edges(J0, x, y))
                            min_ok, one_ok, succ_d0, cap = core.successor_profile(
                                nn, adj, Sset, x, y, J0)
                            if cap:
                                ctr["path_cap_hits"] += 1
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
                            for slid, tp in core.slides_from(
                                    nn, adj, Sset, x, y, J, an, path):
                                if core.is_ces(
                                        core.toggle(J, an, slid), Ccc, Jcyc, x, y):
                                    terminal_ok = True
                                    if tp == h:
                                        hslide_ok = True
                        if terminal_ok:
                            ctr["bplus2_certified_bad_cycles"] += 1
                        else:
                            ctr["terminal_slide_failures"] += 1
                        if not hslide_ok:
                            ctr["h_slide_failures"] += 1
                        if not all_succ_min:
                            ctr["sd_2step_all_failures"] += 1
                        if not some_min_descent:
                            ctr["safe_2_exists_local_failures"] += 1
                        if not all_succ_one:
                            ctr["successor_one_all_failures"] += 1
                        if not some_one_descent:
                            ctr["successor_one_descent_failures"] += 1
                        for key, failed in (
                            ("terminal_slide", not terminal_ok),
                            ("sd_2step_all", not all_succ_min),
                            ("safe_2_exists_local", not some_min_descent),
                            ("successor_one_all", not all_succ_one),
                            ("successor_one_descent", not some_one_descent),
                        ):
                            if failed and len(failures[key]) < 40:
                                failures[key].append(core.witness(
                                    g6, Sset, x, y, J, cc, d0,
                                    {"ncyc": nc, "successors": succ_rows}))
                    if a1_bad:
                        profile[(len(cycs), a1_good)] += 1
    proc.wait()
    result = {
        "n": n, "shard": shard, "nshards": nshards,
        "geng_graphs_total": ctr["geng_graphs_seen"],
        "counters": dict(ctr),
        "a1bad_profile": {f"{a}|{b}": v
                          for (a, b), v in sorted(profile.items())},
        "failures": dict(failures),
        "wall_seconds": round(time.time() - t0, 3),
    }
    outdir = HERE / "results"
    outdir.mkdir(exist_ok=True)
    outpath = outdir / f"gap-n{n}-{shard}of{nshards}.json"
    outpath.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"output": str(outpath), **result}, sort_keys=True))


if __name__ == "__main__":
    main()
