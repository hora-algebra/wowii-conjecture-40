#!/usr/bin/env python3
"""Replay retained (2,1) certificates from fixed 4d7a n=12 shard objects."""
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import safe_exists_scan as core

SOURCE = "5cb5bb9a29718562d4d25a6902fd693f0a4677f4"
TEMPLATE = "work/sd/sd-v2-n12-{}of32.txt"


def load_source(shard):
    ref = f"{SOURCE}:{TEMPLATE.format(shard)}"
    p = subprocess.run(["git", "show", ref], check=True,
                       capture_output=True, text=True)
    return json.loads(p.stdout)


def replay_one(rec):
    nn, adj = core.inv_b.parse_g6(rec["g6"])
    Sset = set(rec["S"])
    x, y = rec["e"]
    J = core.norm([tuple(e) for e in rec["J"]])
    checks = {
        "n12": nn == 12,
        "tau": core.EB.tau(nn, adj) == len(Sset),
        "minimum_fvs_member": frozenset(Sset) in {
            frozenset(S) for S in core.min_fvs_all(nn, adj, len(Sset))},
        "fixed_edge": x not in Sset and y not in Sset and bool(adj[x] >> y & 1),
        "feasible": J in {
            core.norm(F) for F in core.feasible(nn, adj, sorted(Sset), x, y)},
    }
    actual_cycles = {frozenset(cc) for cc, iscy in core.comps(J, (x, y)) if iscy}
    recorded_cycles = {frozenset(cc) for cc in rec["cycles"]}
    checks["cycles"] = actual_cycles == recorded_cycles and len(actual_cycles) == 2
    checks["one_bad_record"] = len(rec["bad"]) == 1 and rec["a1_good"] == 1
    if not all(checks.values()):
        return {"validation": checks, "record": rec}

    cc, recorded_d0, reason = rec["bad"][0]
    Ccc = frozenset(cc)
    checks["bad_cycle_present"] = Ccc in actual_cycles
    checks["bad_reason"] = reason == "no-shortest-CES"
    order, _ = core.walk_cycle(set(cc), J, x, y)
    edata = []
    for ed in [e for kind, e in order if kind == "J"]:
        an = (min(ed), max(ed))
        s = ed[0] if ed[0] in Sset else ed[1]
        h = ed[1] if ed[0] in Sset else ed[0]
        dg = core.residual_dag(nn, adj, Sset, x, y, J, an, s)
        if dg is not None:
            edata.append((an, s, h, dg))
    checks["avoidable"] = bool(edata)
    if not edata:
        return {"validation": checks, "record": rec}
    d0 = min(dg[0] for _, _, _, dg in edata)
    checks["d0"] = d0 == recorded_d0
    Jcyc = core.cyc_sets_edges(J, x, y)
    bad_short = []
    cap = False
    shortest_ces = False
    for an, s, h, (d, fw, td) in edata:
        if d != d0:
            continue
        paths = core.enum_shortest_paths(fw, s, td, d)
        cap = cap or len(paths) >= core.PATHCAP
        for path in paths:
            if core.is_ces(core.toggle(J, an, path), Ccc, Jcyc, x, y):
                shortest_ces = True
            else:
                bad_short.append((an, s, h, path))
    checks["a1_failure"] = not shortest_ces
    checks["no_path_cap"] = not cap

    terminal_ok = False
    hslide_ok = False
    all_succ_min = True
    all_succ_one = True
    some_min_descent = False
    some_one_descent = False
    successors = []
    nc = len(Jcyc)
    for an, s, h, path in bad_short:
        J0 = core.toggle(J, an, path)
        nc0 = len(core.cyc_sets_edges(J0, x, y))
        min_ok, one_ok, succ_d0, succ_cap = core.successor_profile(
            nn, adj, Sset, x, y, J0)
        cap = cap or succ_cap
        all_succ_min = all_succ_min and min_ok
        all_succ_one = all_succ_one and one_ok and succ_d0 == 1
        some_min_descent = some_min_descent or (min_ok and nc0 <= nc)
        some_one_descent = some_one_descent or (
            one_ok and succ_d0 == 1 and nc0 <= nc)
        successors.append({"path": path, "ncyc0": nc0,
                           "d0min0": succ_d0, "min_ces0": min_ok,
                           "one_ces0": one_ok})
        for slid, tp in core.slides_from(nn, adj, Sset, x, y, J, an, path):
            if core.is_ces(core.toggle(J, an, slid), Ccc, Jcyc, x, y):
                terminal_ok = True
                hslide_ok = hslide_ok or tp == h
    checks["no_path_cap"] = not cap
    return {
        "validation": checks,
        "terminal_ok": terminal_ok,
        "hslide_ok": hslide_ok,
        "all_succ_min": all_succ_min,
        "all_succ_one": all_succ_one,
        "some_min_descent": some_min_descent,
        "some_one_descent": some_one_descent,
        "bad_first_steps": len(bad_short),
        "successors": successors,
        "record": rec,
    }


def main():
    t0 = time.time()
    source_rows = []
    records = []
    for shard in range(32):
        src = load_source(shard)
        profile = int(src.get("a1bad_profile", {}).get("2|1", 0))
        saved = [r for r in src.get("witnesses", {}).get(
            "A1-BAD-SELECTION", []) if r.get("a1_good") == 1]
        source_rows.append({"shard": shard, "profile_2_1": profile,
                            "saved_2_1": len(saved),
                            "missing": profile - len(saved)})
        records.extend(saved)

    replayed = [replay_one(rec) for rec in records]
    invalid = [r for r in replayed if not all(r["validation"].values())]
    failures = {
        "terminal_slide": [r for r in replayed if not r.get("terminal_ok", False)],
        "h_slide": [r for r in replayed if not r.get("hslide_ok", False)],
        "sd_2step_all": [r for r in replayed if not r.get("all_succ_min", False)],
        "safe_2_exists_local": [r for r in replayed
                                if not r.get("some_min_descent", False)],
        "successor_one_all": [r for r in replayed
                              if not r.get("all_succ_one", False)],
        "successor_one_descent": [r for r in replayed
                                  if not r.get("some_one_descent", False)],
    }
    result = {
        "source_commit": SOURCE,
        "source_rows": source_rows,
        "source_profile_2_1": sum(r["profile_2_1"] for r in source_rows),
        "saved_records": len(records),
        "missing_records": sum(r["missing"] for r in source_rows),
        "missing_by_shard": {str(r["shard"]): r["missing"]
                             for r in source_rows if r["missing"]},
        "invalid_replays": len(invalid),
        "bad_first_steps": sum(r.get("bad_first_steps", 0) for r in replayed),
        "failure_counts": {k: len(v) for k, v in failures.items()},
        "failures": {k: v[:40] for k, v in failures.items() if v},
        "wall_seconds": round(time.time() - t0, 3),
    }
    out = HERE / "results" / "safe-witness-replay.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"output": str(out), **result}, sort_keys=True))


if __name__ == "__main__":
    main()
