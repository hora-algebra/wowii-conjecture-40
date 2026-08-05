#!/usr/bin/env python3
"""Replay every retained n=12 (1,0) hard-state certificate."""
import json
from pathlib import Path

import safe_witness_replay as replay


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
        rows.append(replay.replay_one(rec))
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
