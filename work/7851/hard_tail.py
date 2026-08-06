#!/usr/bin/env python3
"""Replay retained hard states and grade the exact cap-boundary tails."""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import experiment_b as EB
import inv_b
from a1_verify import (PATHCAP, cyc_sets_edges, enum_shortest_paths, norm,
                       residual_dag, toggle)
from eval_L1_holdout import comps, feasible
from eval_frozen import min_fvs_all
from mine_n10 import walk_cycle


SOURCE = "5cb5bb9a29718562d4d25a6902fd693f0a4677f4"
TEMPLATE = "work/sd/sd-v2-n12-{}of32.txt"
START = {
    4: (208036, "K?ABBAWeF_?}"),
    11: (187883, "K??FFBw}Fw^_"),
    13: (210349, "K?ABCqWXCsKl"),
    14: (193230, "K??Ffbo}Fw^_"),
    16: (207024, "K?AE@bGMF_?~"),
    25: (209529, "K?AB?r_F?{[H"),
}
EXPECTED_PROFILE = 1184
EXPECTED_RETAINED = 1140
EXPECTED_MISSING = 44
CES_MODE = "real"


def source_json(shard):
    ref = f"{SOURCE}:{TEMPLATE.format(shard)}"
    proc = subprocess.run(["git", "show", ref], check=True,
                          capture_output=True, text=True)
    return json.loads(proc.stdout)


def edge_list(edges):
    return sorted([min(u, v), max(u, v)] for u, v in edges)


def state_payload(g6, Sset, x, y, J, cycles):
    return {
        "g6": g6,
        "S": sorted(Sset),
        "e": [min(x, y), max(x, y)],
        "J": edge_list(J),
        "cycles": sorted(sorted(cc) for cc in cycles),
    }


def state_id(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def is_ces(Jp, Ccc, Jcyc, x, y):
    if CES_MODE == "always":
        return True
    if CES_MODE == "never":
        return False
    Jpc = cyc_sets_edges(Jp, x, y)
    return Ccc not in Jpc and Jpc <= Jcyc


def cycle_data(nn, adj, Sset, x, y, J, cc):
    order, _ = walk_cycle(cc, J, x, y)
    rows = []
    for ed in [edge for kind, edge in order if kind == "J"]:
        an = (min(ed), max(ed))
        s = ed[0] if ed[0] in Sset else ed[1]
        h = ed[1] if ed[0] in Sset else ed[0]
        dag = residual_dag(nn, adj, Sset, x, y, J, an, s)
        if dag is not None:
            rows.append((an, s, h, dag))
    return rows


def direct_ces_at(nn, adj, Sset, x, y, J0, Z, v, J0cyc):
    moves = []
    order, _ = walk_cycle(set(Z), J0, x, y)
    for ed in [edge for kind, edge in order if kind == "J" and v in edge]:
        an = (min(ed), max(ed))
        dag = residual_dag(nn, adj, Sset, x, y, J0, an, v)
        if dag is None or dag[0] != 1:
            continue
        paths = enum_shortest_paths(dag[1], v, dag[2], 1)
        for path in paths:
            if is_ces(toggle(J0, an, path), Z, J0cyc, x, y):
                moves.append({"release": list(an), "path": path})
    return moves


def any_length_one_ces(nn, adj, Sset, x, y, J0):
    J0cyc = cyc_sets_edges(J0, x, y)
    moves = []
    for cc, iscy in comps(J0, (x, y)):
        if not iscy:
            continue
        Z = frozenset(cc)
        order, _ = walk_cycle(cc, J0, x, y)
        for ed in [edge for kind, edge in order if kind == "J"]:
            an = (min(ed), max(ed))
            s = ed[0] if ed[0] in Sset else ed[1]
            dag = residual_dag(nn, adj, Sset, x, y, J0, an, s)
            if dag is None or dag[0] != 1:
                continue
            paths = enum_shortest_paths(dag[1], s, dag[2], 1)
            for path in paths:
                if is_ces(toggle(J0, an, path), Z, J0cyc, x, y):
                    moves.append({"cycle": sorted(Z), "release": list(an),
                                  "path": path})
    return moves


def analyse_state(g6, nn, adj, Sset, x, y, J, forced):
    J = norm(J)
    cycles = [frozenset(cc) for cc, iscy in comps(J, (x, y)) if iscy]
    Jcyc = cyc_sets_edges(J, x, y)
    payload = state_payload(g6, Sset, x, y, J, cycles)
    result = {
        "id": state_id(payload), "payload": payload,
        "cycle_count": len(cycles), "a1_good": 0, "a1_bad": 0,
        "bad_first_steps": 0, "path_caps": 0,
        "lemmaA_violations": 0, "hso": False, "ope": True,
        "forced_cycle_edges": sum(
            edge in forced for edge in J
            if any(edge[0] in cc and edge[1] in cc for cc in cycles)),
        "ope_reasons": Counter(), "step_samples": [],
    }
    hard_steps = []
    cycle_rows = []
    for Ccc in cycles:
        rows = cycle_data(nn, adj, Sset, x, y, J, set(Ccc))
        if not rows:
            result["lemmaA_violations"] += 1
            continue
        d0 = min(row[3][0] for row in rows)
        shortest_ces = False
        bad = []
        for an, s, h, (d, fw, td) in rows:
            if d != d0:
                continue
            paths = enum_shortest_paths(fw, s, td, d)
            if len(paths) >= PATHCAP:
                result["path_caps"] += 1
            for path in paths:
                J0 = toggle(J, an, path)
                if is_ces(J0, Ccc, Jcyc, x, y):
                    shortest_ces = True
                else:
                    bad.append((Ccc, d0, an, s, h, path, J0))
        if shortest_ces:
            result["a1_good"] += 1
        else:
            result["a1_bad"] += 1
            hard_steps.extend(bad)
        cycle_rows.append((Ccc, d0))

    if result["a1_good"] or not result["a1_bad"]:
        result["ope"] = False
        return result

    if len(cycles) != 1:
        result["ope"] = False
        result["ope_reasons"]["initial_cycle_count"] += 1
    if any(len(Ccc) != 4 for Ccc, _ in cycle_rows):
        result["ope"] = False
        result["ope_reasons"]["initial_not_four_cycle"] += 1
    if any(d0 != 3 for _, d0 in cycle_rows):
        result["ope"] = False
        result["ope_reasons"]["initial_d0_not_three"] += 1

    nc = len(Jcyc)
    for Ccc, d0, an, s, h, path, J0 in hard_steps:
        result["bad_first_steps"] += 1
        J0 = norm(J0)
        J0cyc = cyc_sets_edges(J0, x, y)
        nc0 = len(J0cyc)
        direct = any_length_one_ces(nn, adj, Sset, x, y, J0)
        if direct and nc0 <= nc:
            result["hso"] = True

        step_ok = True
        reasons = []
        if Ccc in J0cyc:
            step_ok = False
            reasons.append("old_cycle_survives")
        if len(J0cyc) != 1:
            step_ok = False
            reasons.append("successor_cycle_count")
            Z = None
        else:
            Z = next(iter(J0cyc))
            if len(Z) != 4:
                step_ok = False
                reasons.append("successor_not_four_cycle")
        if Z is not None:
            added = set(J0) - set(J)
            z_added = [edge for edge in added
                       if edge[0] in Z and edge[1] in Z]
            if len(z_added) != 1:
                step_ok = False
                reasons.append("new_cycle_added_edge_count")
            off_path = [v for v in Z if v in Sset and v not in path]
            if len(off_path) != 1:
                step_ok = False
                reasons.append("off_path_S_count")
                escape = []
            else:
                escape = direct_ces_at(
                    nn, adj, Sset, x, y, J0, Z, off_path[0], J0cyc)
                if not escape:
                    step_ok = False
                    reasons.append("off_path_no_direct_CES")
        else:
            off_path = []
            escape = []
        if not step_ok:
            result["ope"] = False
            for reason in reasons:
                result["ope_reasons"][reason] += 1
            if len(result["step_samples"]) < 4:
                result["step_samples"].append({
                    "cycle": sorted(Ccc), "d0": d0,
                    "release": list(an), "path": path,
                    "successor_cycles": sorted(sorted(cc) for cc in J0cyc),
                    "reasons": reasons, "direct_moves": direct,
                    "off_path_moves": escape,
                })
    result["ope_reasons"] = dict(result["ope_reasons"])
    return result


def retained_inputs():
    profile = 0
    rows = []
    for shard in range(32):
        data = source_json(shard)
        profile += int(data.get("a1bad_profile", {}).get("1|0", 0))
        rows.extend(rec for rec in data.get("witnesses", {}).get(
            "A1-BAD-SELECTION", [])
                    if rec.get("ncyc") == 1 and rec.get("a1_good") == 0)
    return profile, rows


def replay_retained(rows):
    out = {}
    invalid = []
    for rec in rows:
        nn, adj = inv_b.parse_g6(rec["g6"])
        Sset = set(rec["S"])
        x, y = rec["e"]
        J = norm(tuple(edge) for edge in rec["J"])
        sels = [norm(sel) for sel in feasible(nn, adj, sorted(Sset), x, y)]
        forced = set(sels[0]) if sels else set()
        for sel in sels[1:]:
            forced.intersection_update(sel)
        analysis = analyse_state(rec["g6"], nn, adj, Sset, x, y, J, forced)
        actual = analysis["payload"]
        expected = state_payload(
            rec["g6"], Sset, x, y, J,
            [frozenset(cc) for cc in rec.get("cycles", [])])
        checks = {
            "n12": nn == 12,
            "minimum_fvs": EB.tau(nn, adj) == len(Sset),
            "S_member": frozenset(Sset) in {
                frozenset(S) for S in min_fvs_all(nn, adj, len(Sset))},
            "feasible": J in sels,
            "payload": actual == expected,
        }
        if not all(checks.values()):
            invalid.append({"checks": checks, "expected": expected,
                            "actual": actual})
        out[analysis["id"]] = analysis
    return out, invalid


def summarize(rows):
    return {
        "states": len(rows),
        "hard_states": sum(not row["a1_good"] and row["a1_bad"] > 0
                           for row in rows.values()),
        "bad_first_steps": sum(row["bad_first_steps"] for row in rows.values()),
        "hso_failures": sum(not row["hso"] for row in rows.values()
                            if not row["a1_good"] and row["a1_bad"] > 0),
        "ope_failures": sum(not row["ope"] for row in rows.values()
                            if not row["a1_good"] and row["a1_bad"] > 0),
        "path_caps": sum(row["path_caps"] for row in rows.values()),
        "lemmaA_violations": sum(row["lemmaA_violations"] for row in rows.values()),
        "forced_cycle_edges": dict(sorted(Counter(
            row["forced_cycle_edges"] for row in rows.values()).items())),
    }


def scan_tails():
    rows = {}
    ctr = Counter()
    failures = []
    boundary = {}
    min_start = min(index for index, _ in START.values())
    proc = subprocess.Popen(["geng", "-bc", "-q", "12"],
                            stdout=subprocess.PIPE, text=True)
    for gi, raw in enumerate(proc.stdout):
        g6 = raw.strip()
        if not g6:
            continue
        ctr["geng_graphs_seen"] += 1
        if gi < min_start:
            continue
        shard = gi % 32
        if shard not in START or gi < START[shard][0]:
            continue
        if shard not in boundary:
            boundary[shard] = g6
        ctr["graphs_in_tails"] += 1
        nn, adj = inv_b.parse_g6(g6)
        k = EB.tau(nn, adj)
        if k < 2:
            continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S)
            Hv = [v for v in range(nn) if v not in Sset]
            Hedges = [(u, v) for i, u in enumerate(Hv) for v in Hv[i + 1:]
                      if adj[u] >> v & 1]
            for x, y in Hedges:
                sels = [norm(sel) for sel in feasible(
                    nn, adj, sorted(Sset), x, y)]
                if not sels:
                    continue
                forced = set(sels[0])
                for sel in sels[1:]:
                    forced.intersection_update(sel)
                for J in sels:
                    cycles = [cc for cc, iscy in comps(J, (x, y)) if iscy]
                    if not cycles:
                        continue
                    ctr["cyclic_selections"] += 1
                    analysis = analyse_state(g6, nn, adj, Sset, x, y, J, forced)
                    ctr["path_caps"] += analysis["path_caps"]
                    ctr["lemmaA_violations"] += analysis["lemmaA_violations"]
                    if analysis["a1_good"] or not analysis["a1_bad"]:
                        continue
                    ctr["hard_states"] += 1
                    rows[analysis["id"]] = analysis
                    if (not analysis["hso"] or not analysis["ope"]) and len(failures) < 40:
                        failures.append(analysis)
    proc.wait()
    return rows, dict(ctr), boundary, failures, proc.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("retained", "tails"), required=True)
    parser.add_argument("--ces", choices=("real", "always", "never"),
                        default="real")
    args = parser.parse_args()
    global CES_MODE
    CES_MODE = args.ces
    started = time.time()

    profile, retained_records = retained_inputs()
    retained, invalid = replay_retained(retained_records)
    result = {
        "mode": args.mode, "ces_mode": CES_MODE, "source_commit": SOURCE,
        "profile_1_0": profile, "retained_records": len(retained_records),
        "retained_unique": len(retained), "retained_invalid": len(invalid),
        "retained_summary": summarize(retained),
        "retained_invalid_samples": invalid[:10],
    }

    if args.mode == "tails":
        tails, counters, boundary, failures, returncode = scan_tails()
        combined = dict(retained)
        combined.update(tails)
        new_ids = sorted(set(tails) - set(retained))
        boundary_checks = {
            str(shard): boundary.get(shard) == expected
            for shard, (_, expected) in START.items()
        }
        result.update({
            "tail_counters": counters,
            "tail_unique": len(tails),
            "tail_only_unique": len(new_ids),
            "combined_unique": len(combined),
            "combined_summary": summarize(combined),
            "boundary_observed": {str(k): v for k, v in sorted(boundary.items())},
            "boundary_checks": boundary_checks,
            "geng_returncode": returncode,
            "failure_samples": failures,
            "target_gate": {
                "profile": profile == EXPECTED_PROFILE,
                "retained": len(retained) == EXPECTED_RETAINED,
                "missing": len(new_ids) == EXPECTED_MISSING,
                "combined": len(combined) == EXPECTED_PROFILE,
                "boundaries": all(boundary_checks.values()),
                "no_invalid": not invalid,
                "no_caps": counters.get("path_caps", 0) == 0,
                "no_lemmaA_violation": counters.get("lemmaA_violations", 0) == 0,
                "geng_complete": (counters.get("geng_graphs_seen", 0) == 212780
                                  and returncode == 0),
                "hso": summarize(combined)["hso_failures"] == 0,
                "ope": summarize(combined)["ope_failures"] == 0,
            },
        })
    result["wall_seconds"] = round(time.time() - started, 3)
    outdir = Path(__file__).resolve().parent / "results"
    outdir.mkdir(exist_ok=True)
    outfile = outdir / f"hard-{args.mode}-{CES_MODE}.json"
    outfile.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    concise = {key: value for key, value in result.items()
               if key not in {"failure_samples", "retained_invalid_samples"}}
    print(json.dumps({"output": str(outfile), **concise}, sort_keys=True))


if __name__ == "__main__":
    main()
