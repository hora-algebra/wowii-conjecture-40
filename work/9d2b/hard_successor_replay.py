#!/usr/bin/env python3
"""Replay every retained n=12 (1,0) hard-state certificate."""
import json
from pathlib import Path

import safe_witness_replay as replay
import safe_exists_scan as core


def replay_hard_one(rec):
    nn, adj = core.inv_b.parse_g6(rec["g6"])
    Sset = set(rec["S"])
    x, y = rec["e"]
    J = core.norm([tuple(e) for e in rec["J"]])
    actual_cycles = {frozenset(cc) for cc, iscy in core.comps(J, (x, y)) if iscy}
    recorded_cycles = {frozenset(cc) for cc in rec["cycles"]}
    checks = {
        "n12": nn == 12,
        "tau": core.EB.tau(nn, adj) == len(Sset),
        "minimum_fvs_member": frozenset(Sset) in {
            frozenset(S) for S in core.min_fvs_all(nn, adj, len(Sset))},
        "fixed_edge": x not in Sset and y not in Sset and bool(adj[x] >> y & 1),
        "feasible": J in {core.norm(F) for F in core.feasible(
            nn, adj, sorted(Sset), x, y)},
        "cycles": actual_cycles == recorded_cycles and len(actual_cycles) == 1,
        "one_bad_record": len(rec["bad"]) == 1 and rec["a1_good"] == 0,
    }
    if not all(checks.values()):
        return {"validation": checks, "record": rec}

    cc, recorded_d0, reason = rec["bad"][0]
    Ccc = frozenset(cc)
    order, _ = core.walk_cycle(set(cc), J, x, y)
    edata = []
    for ed in [e for kind, e in order if kind == "J"]:
        an = (min(ed), max(ed))
        s = ed[0] if ed[0] in Sset else ed[1]
        h = ed[1] if ed[0] in Sset else ed[0]
        dg = core.residual_dag(nn, adj, Sset, x, y, J, an, s)
        if dg is not None:
            edata.append((an, s, h, dg))
    checks["bad_cycle_present"] = Ccc in actual_cycles
    checks["bad_reason"] = reason == "no-shortest-CES"
    checks["avoidable"] = bool(edata)
    if not edata:
        return {"validation": checks, "record": rec}
    d0 = min(dg[0] for _, _, _, dg in edata)
    checks["d0"] = d0 == recorded_d0
    Jcyc = core.cyc_sets_edges(J, x, y)
    bad_short = []
    shortest_ces = False
    cap = False
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
    all_succ_min = True
    all_succ_one = True
    some_min_descent = False
    some_one_descent = False
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
        for slid, _ in core.slides_from(nn, adj, Sset, x, y, J, an, path):
            terminal_ok = terminal_ok or core.is_ces(
                core.toggle(J, an, slid), Ccc, Jcyc, x, y)
    checks["no_path_cap"] = not cap
    return {"validation": checks, "terminal_ok": terminal_ok,
            "all_succ_min": all_succ_min, "all_succ_one": all_succ_one,
            "some_min_descent": some_min_descent,
            "some_one_descent": some_one_descent,
            "bad_first_steps": len(bad_short), "record": rec}


def main():
    records = []
    rows = []
    profile_total = 0
    saved_by_shard = []
    for shard in range(32):
        src = replay.load_source(shard)
        profile = int(src.get("a1bad_profile", {}).get("1|0", 0))
        saved = [r for r in src.get("witnesses", {}).get(
            "A1-BAD-SELECTION", [])
                 if r.get("ncyc") == 1 and r.get("a1_good") == 0]
        profile_total += profile
        records.extend(saved)
        saved_by_shard.append({"shard": shard, "profile": profile,
                               "saved": len(saved),
                               "missing": profile - len(saved)})
    for rec in records:
        rows.append(replay_hard_one(rec))
    invalid = sum(not all(row["validation"].values()) for row in rows)
    counts = {
        "terminal_slide_failures": sum(not row.get("terminal_ok", False)
                                       for row in rows),
        "sd_2step_all_failures": sum(not row.get("all_succ_min", False)
                                     for row in rows),
        "safe_2_exists_local_failures": sum(
            not row.get("some_min_descent", False) for row in rows),
        "successor_one_all_failures": sum(
            not row.get("all_succ_one", False) for row in rows),
        "hard_successor_one_failures": sum(
            not row.get("some_one_descent", False) for row in rows),
    }
    result = {
        "source_commit": replay.SOURCE,
        "profile_1_0": profile_total,
        "saved_records": len(records),
        "missing_records": profile_total - len(records),
        "missing_by_shard": {str(r["shard"]): r["missing"]
                             for r in saved_by_shard if r["missing"]},
        "invalid_replays": invalid,
        "bad_first_steps": sum(row.get("bad_first_steps", 0) for row in rows),
        "failure_counts": counts,
        "failures": [row for row in rows
                     if not row.get("some_one_descent", False)][:40],
    }
    out = Path(__file__).resolve().parent / "results" / "hard-successor-replay.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "failures"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
