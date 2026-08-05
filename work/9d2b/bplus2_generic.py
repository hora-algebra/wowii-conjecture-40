#!/usr/bin/env python3
"""Generic bounded-path B-PLUS-2 replay and multi-cycle shard scanner.

Usage:
  bplus2_generic.py replay11
  bplus2_generic.py replay12
  bplus2_generic.py scan N shard nshards
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
from a1_verify import indep_feasible

SOURCE = "5cb5bb9a29718562d4d25a6902fd693f0a4677f4"


def bounded_paths(nn, adj, Sset, x, y, J, a, s, limit):
    """Enumerate every simple residual augmenting vertex-path up to limit."""
    M = set(core.norm(J))
    M.discard(a)
    cap = {h: 2 for h in range(nn) if h not in Sset}
    cap[x] = 1
    cap[y] = 1
    deg = defaultdict(int)
    for u, v in M:
        deg[u] += 1
        deg[v] += 1
    out = []
    used = {s}

    def rec(u, path):
        depth = len(path) - 1
        if depth >= limit:
            return
        if u in Sset:
            for h in range(nn):
                ed = (min(u, h), max(u, h))
                if h in Sset or not (adj[u] >> h & 1):
                    continue
                if ed in M or ed == a or h in used:
                    continue
                used.add(h)
                hp = path + [h]
                if deg[h] < cap[h]:
                    out.append(hp)
                rec(h, hp)
                used.remove(h)
        else:
            for z in range(nn):
                ed = (min(u, z), max(u, z))
                if z not in Sset or ed not in M or z in used:
                    continue
                used.add(z)
                rec(z, path + [z])
                used.remove(z)

    rec(s, [s])
    return out


def analyse_cycle(nn, adj, Sset, x, y, J, cc):
    J = core.norm(J)
    Ccc = frozenset(cc)
    Jcyc = core.cyc_sets_edges(J, x, y)
    order, _ = core.walk_cycle(set(cc), J, x, y)
    edata = []
    for ed in [e for kind, e in order if kind == "J"]:
        an = (min(ed), max(ed))
        s = ed[0] if ed[0] in Sset else ed[1]
        dg = core.residual_dag(nn, adj, Sset, x, y, J, an, s)
        if dg is not None:
            edata.append((an, s, dg))
    if not edata:
        return {"avoidable": False, "bplus2": False}
    d0 = min(dg[0] for _, _, dg in edata)
    best = None
    paths_tested = 0
    feasible_failures = 0
    best_path = None
    for an, s, _ in edata:
        for path in bounded_paths(nn, adj, Sset, x, y, J, an, s, d0 + 2):
            paths_tested += 1
            Jp = core.toggle(J, an, path)
            if not indep_feasible(nn, adj, Sset, x, y, Jp):
                feasible_failures += 1
                continue
            if core.is_ces(Jp, Ccc, Jcyc, x, y):
                length = len(path) - 1
                if best is None or length < best:
                    best = length
                    best_path = {"released": list(an), "path": path}
    return {"avoidable": True, "d0": d0, "dces_bounded": best,
            "bplus2": best is not None and best <= d0 + 2,
            "paths_tested": paths_tested,
            "infeasible_candidates": feasible_failures,
            "best_path": best_path}


def load_json(refpath):
    p = subprocess.run(["git", "show", f"{SOURCE}:{refpath}"], check=True,
                       capture_output=True, text=True)
    return json.loads(p.stdout)


def records11():
    src = load_json("work/sd/sd-n11-AGGREGATE.json")
    return src["witnesses"]["A1-BAD-SELECTION"]


def records12():
    out = []
    rows = []
    for shard in range(32):
        src = load_json(f"work/sd/sd-v2-n12-{shard}of32.txt")
        profile = int(src.get("a1bad_profile", {}).get("2|1", 0))
        saved = [r for r in src.get("witnesses", {}).get(
            "A1-BAD-SELECTION", []) if r.get("a1_good") == 1]
        rows.append({"shard": shard, "profile": profile, "saved": len(saved)})
        out.extend(saved)
    return out, rows


def validate_record(rec):
    nn, adj = core.inv_b.parse_g6(rec["g6"])
    Sset = set(rec["S"])
    x, y = rec["e"]
    J = core.norm([tuple(e) for e in rec["J"]])
    feasible_set = {core.norm(F) for F in core.feasible(
        nn, adj, sorted(Sset), x, y)}
    cycles = {frozenset(cc) for cc, iscy in core.comps(J, (x, y)) if iscy}
    expected = {frozenset(cc) for cc in rec["cycles"]}
    valid = (core.EB.tau(nn, adj) == len(Sset)
             and frozenset(Sset) in {frozenset(S) for S in
                                      core.min_fvs_all(nn, adj, len(Sset))}
             and J in feasible_set and cycles == expected)
    return valid, nn, adj, Sset, x, y, J


def replay(mode):
    if mode == "replay11":
        records, source_rows = records11(), None
    else:
        records, source_rows = records12()
    rows = []
    for rec in records:
        valid, nn, adj, Sset, x, y, J = validate_record(rec)
        for bad in rec["bad"]:
            result = analyse_cycle(nn, adj, Sset, x, y, J, bad[0]) if valid else {}
            rows.append({"valid": valid, "record": rec, "analysis": result})
    result = {
        "mode": mode, "source_commit": SOURCE,
        "records": len(records), "cycles_graded": len(rows),
        "invalid": sum(not r["valid"] for r in rows),
        "bplus2_failures": sum(not r["analysis"].get("bplus2", False)
                               for r in rows),
        "rows": rows,
    }
    d0hist = defaultdict(int)
    dhist = defaultdict(int)
    for row in rows:
        d0hist[str(row["analysis"].get("d0"))] += 1
        dhist[str(row["analysis"].get("dces_bounded"))] += 1
    result["d0_histogram"] = dict(d0hist)
    result["dces_histogram"] = dict(dhist)
    if source_rows is not None:
        result["source_rows"] = source_rows
    out = HERE / "results" / f"bplus2-{mode}.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"},
                     sort_keys=True))


def scan(n, shard, nshards):
    t0 = time.time()
    ctr = defaultdict(int)
    failures = []
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
                for J in core.feasible(nn, adj, list(S), x, y):
                    cycs = [cc for cc, iscy in core.comps(J, (x, y)) if iscy]
                    if len(cycs) < 2:
                        continue
                    ctr["multi_cyclic_selections"] += 1
                    Jcyc = core.cyc_sets_edges(core.norm(J), x, y)
                    for cc in cycs:
                        ctr["cycle_components"] += 1
                        Ccc = frozenset(cc)
                        order, _ = core.walk_cycle(cc, J, x, y)
                        edata = []
                        for ed in [e for kind, e in order if kind == "J"]:
                            an = (min(ed), max(ed))
                            s = ed[0] if ed[0] in Sset else ed[1]
                            dg = core.residual_dag(
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
                            paths = core.enum_shortest_paths(fw, s, td, d)
                            if len(paths) >= core.PATHCAP:
                                ctr["path_cap_hits"] += 1
                            for path in paths:
                                if core.is_ces(core.toggle(J, an, path),
                                               Ccc, Jcyc, x, y):
                                    a1 = True
                        if a1:
                            continue
                        ctr["a1_failures"] += 1
                        analysis = analyse_cycle(nn, adj, Sset, x, y, J, cc)
                        if analysis["infeasible_candidates"]:
                            ctr["infeasible_candidates"] += analysis[
                                "infeasible_candidates"]
                        if analysis["bplus2"]:
                            ctr["bplus2_successes"] += 1
                        else:
                            ctr["bplus2_failures"] += 1
                            if len(failures) < 80:
                                failures.append(core.witness(
                                    g6, Sset, x, y, J, cc, d0,
                                    {"analysis": analysis}))
    proc.wait()
    result = {"mode": "scan", "n": n, "shard": shard,
              "nshards": nshards, "counters": dict(ctr),
              "failures": failures,
              "wall_seconds": round(time.time() - t0, 3)}
    out = HERE / "results" / f"bplus2-scan-n{n}-{shard}of{nshards}.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "failures"},
                     sort_keys=True))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("mode required")
    if sys.argv[1] in {"replay11", "replay12"}:
        replay(sys.argv[1])
    elif sys.argv[1] == "scan" and len(sys.argv) == 5:
        scan(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        raise SystemExit("invalid arguments")


if __name__ == "__main__":
    main()
