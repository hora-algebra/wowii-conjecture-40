#!/usr/bin/env python3
"""Exact generic B-PLUS-2 tails after fixed 4d7a certificate caps."""
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import bplus2_generic as generic

START = {
    11: (187883, "K??FFBw}Fw^_", 14),
    14: (193230, "K??Ffbo}Fw^_", 12),
}


def main():
    if len(sys.argv) != 2 or int(sys.argv[1]) not in START:
        raise SystemExit("usage: bplus2_tail.py 11|14")
    shard = int(sys.argv[1])
    start_index, start_g6, expected_missing = START[shard]
    n = 12
    nshards = 32
    t0 = time.time()
    ctr = defaultdict(int)
    failures = []
    first_processed = None

    proc = subprocess.Popen(["geng", "-bc", "-q", "12"],
                            stdout=subprocess.PIPE, text=True)
    for gi, raw in enumerate(proc.stdout):
        g6 = raw.strip()
        if not g6:
            continue
        ctr["geng_graphs_seen"] += 1
        if gi < start_index or gi % nshards != shard:
            continue
        if first_processed is None:
            first_processed = g6
        ctr["graphs_in_tail"] += 1
        nn, adj = generic.core.inv_b.parse_g6(g6)
        k = generic.core.EB.tau(nn, adj)
        if k < 2:
            continue
        for S in generic.core.min_fvs_all(nn, adj, k):
            Sset = set(S)
            Hv = [v for v in range(nn) if v not in Sset]
            Hedges = [(u, v) for ii, u in enumerate(Hv) for v in Hv[ii + 1:]
                      if adj[u] >> v & 1]
            for x, y in Hedges:
                for J in generic.core.feasible(nn, adj, list(S), x, y):
                    cycs = [cc for cc, iscy in generic.core.comps(J, (x, y))
                            if iscy]
                    if len(cycs) < 2:
                        continue
                    ctr["multi_cyclic_selections"] += 1
                    Jcyc = generic.core.cyc_sets_edges(
                        generic.core.norm(J), x, y)
                    for cc in cycs:
                        ctr["cycle_components"] += 1
                        Ccc = frozenset(cc)
                        order, _ = generic.core.walk_cycle(cc, J, x, y)
                        edata = []
                        for ed in [e for kind, e in order if kind == "J"]:
                            an = (min(ed), max(ed))
                            s = ed[0] if ed[0] in Sset else ed[1]
                            dg = generic.core.residual_dag(
                                nn, adj, Sset, x, y, J, an, s)
                            if dg is not None:
                                edata.append((an, s, dg))
                        if not edata:
                            ctr["lemmaA_violations"] += 1
                            continue
                        d0 = min(dg[0] for _, _, dg in edata)
                        a1 = False
                        for an, s, (d, fw, td) in edata:
                            if d != d0:
                                continue
                            paths = generic.core.enum_shortest_paths(fw, s, td, d)
                            if len(paths) >= generic.core.PATHCAP:
                                ctr["path_cap_hits"] += 1
                            for path in paths:
                                if generic.core.is_ces(
                                        generic.core.toggle(J, an, path),
                                        Ccc, Jcyc, x, y):
                                    a1 = True
                        if a1:
                            continue
                        ctr["a1_failures"] += 1
                        analysis = generic.analyse_cycle(
                            nn, adj, Sset, x, y, J, cc)
                        ctr["bounded_paths_tested"] += analysis["paths_tested"]
                        ctr["infeasible_candidates"] += analysis[
                            "infeasible_candidates"]
                        if analysis["bplus2"]:
                            ctr["bplus2_successes"] += 1
                        else:
                            ctr["bplus2_failures"] += 1
                            if len(failures) < 80:
                                failures.append(generic.core.witness(
                                    g6, Sset, x, y, J, cc, d0,
                                    {"analysis": analysis}))
    proc.wait()
    result = {
        "n": n, "shard": shard, "nshards": nshards,
        "start_index": start_index, "expected_start_g6": start_g6,
        "first_processed_g6": first_processed,
        "boundary_match": first_processed == start_g6,
        "expected_missing_at_least": expected_missing,
        "counters": dict(ctr), "failures": failures,
        "wall_seconds": round(time.time() - t0, 3),
    }
    out = Path(__file__).resolve().parent / "results" / f"bplus2-tail-{shard}.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "failures"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
