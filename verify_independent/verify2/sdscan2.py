#!/usr/bin/env python3
"""VERIFY-2 independent SD census driver.

usage: sdscan2.py N [shard nshards] [--bplus2-all] [--ces=always|never]

Grades, per the frozen statements:
  A1-ALL failures        cycles C with no CES minimising step        (positive gap)
  SD-SHORT               some cycle of J satisfies A1(C)
  SD-COUNT-SHORT         some minimising toggle strictly lowers |cyc(J)|
  SD-PLUS-2   (exists-cycle)  some cycle has dCES <= d0+2
  B-PLUS-2    (forall-cycle)  EVERY cycle has dCES <= d0+2   [--bplus2-all]
  SD-2STEP               every minimising step at an A1-failing C lands on J0
                         admitting a CES minimising step
  SD-2STEP-DESCENT       some minimising step lands on J0 with
                         |cyc(J0)| <= |cyc(J)| admitting a CES minimising step
  ONE-CYCLE              histogram of |cyc(J)|
  lemmaA_violations      selected cycles all of whose incidences are forced
"""
import sys, os, json, subprocess, time
from collections import Counter
from sdverify2 import (g6_decode, min_fvs_all, Inst, cycle_components,
                       cycle_count_unionfind, bfs_residual, enum_paths,
                       toggle, is_ces, INF)

CAP = [0]
CES_MODE = "real"


def ces_pred(inst, oldset, newsel, C):
    ok, ncy = is_ces(inst, oldset, newsel, C)
    if CES_MODE == "always":
        return True, ncy
    if CES_MODE == "never":
        return False, ncy
    return ok, ncy


def bounded_paths(inst, selset, load, a, Lmax):
    """all simple augmenting paths of length <= Lmax in the residual of N-a."""
    i0, h0 = a
    sel = selset - {a}
    L = list(load)
    L[h0] -= 1
    out = []
    usedS = {i0}
    usedH = set()

    def rec(node, depth, sofar):
        if depth >= Lmax:
            return
        for h in inst.inc[node]:
            ed = (node, h)
            if ed in sel or ed == a or h in usedH:
                continue
            usedH.add(h)
            ns = sofar + [ed]
            if L[h] < inst.cap[h]:
                out.append(list(ns))
            # continue through h on a selected edge
            for i in inst.users[h]:
                if (i, h) in sel and i not in usedS:
                    usedS.add(i)
                    rec(i, depth + 2, ns + [(i, h)])
                    usedS.discard(i)
            usedH.discard(h)

    rec(i0, 0, [])
    return out


def analyse_selection(inst, forced, selset, want_bplus2_all):
    """returns a dict of per-selection results."""
    cyc = cycle_components(inst, selset)
    ncy = len(cyc)
    res = {"ncyc": ncy}
    if ncy == 0:
        return res
    assert cycle_count_unionfind(inst, selset) == ncy, "cycle-count mismatch"
    oldset = set(cyc)
    load = inst.loads(selset)

    per_cycle = []
    lemmaA = 0
    for C in cyc:
        avoid = [a for a in C if a not in forced]
        if not avoid:
            lemmaA += 1
            per_cycle.append({"C": C, "d0": INF, "a1": False,
                              "steps": [], "dces": INF})
            continue
        d0 = INF
        info = []
        for a in avoid:
            d, dS, dH, tg = bfs_residual(inst, selset, load, a)
            assert d < INF, "avoidable edge with no augmenting path"
            info.append((a, d, dS, dH, tg))
            d0 = min(d0, d)
        steps = []
        for (a, d, dS, dH, tg) in info:
            if d != d0:
                continue
            for p in enum_paths(inst, selset, a, dS, dH, tg, CAP):
                steps.append((a, p))
        a1 = False
        mincount_drop = False
        for (a, p) in steps:
            nsel = toggle(selset, a, p)
            ok, ncy2 = ces_pred(inst, oldset, nsel, C)
            if ok:
                a1 = True
            if len(ncy2) < ncy:
                mincount_drop = True
        per_cycle.append({"C": C, "d0": d0, "a1": a1, "steps": steps,
                          "dces": d0 if a1 else None,
                          "drop": mincount_drop})
    res["lemmaA"] = lemmaA
    res["percycle"] = per_cycle
    res["sd_short"] = any(pc["a1"] for pc in per_cycle)
    res["sd_count_short"] = any(pc.get("drop") for pc in per_cycle)

    # ---- d0+2 probing on A1-failing cycles (this is where SD-PLUS-2 and the
    # universal B-PLUS-2 differ, and where 4d7a left the universal form ungraded)
    fails = [pc for pc in per_cycle if not pc["a1"] and pc["d0"] < INF]
    if fails and (not res["sd_short"] or want_bplus2_all):
        for pc in fails:
            C = pc["C"]
            best = INF
            for a in [x for x in C if x not in forced]:
                for p in bounded_paths(inst, selset, load, a, pc["d0"] + 2):
                    if len(p) > pc["d0"] + 2:
                        continue
                    nsel = toggle(selset, a, p)
                    ok, _ = ces_pred(inst, oldset, nsel, C)
                    if ok:
                        best = min(best, len(p))
            pc["dces"] = best
    res["sd_plus2"] = (res["sd_short"]
                       or any(pc.get("dces") not in (None, INF)
                              and pc["dces"] <= pc["d0"] + 2 for pc in fails))
    if want_bplus2_all:
        res["bplus2_all"] = all(
            pc["a1"] or (pc["d0"] < INF and pc.get("dces") not in (None, INF)
                         and pc["dces"] <= pc["d0"] + 2)
            for pc in per_cycle)
    return res


def probe_2step(inst, forced, selset, per_cycle, C_entry, ncy):
    """returns (all_ok, some_ok_descent) for one A1-failing cycle."""
    all_ok = True
    some_ok = False
    for (a, p) in C_entry["steps"]:
        J0 = toggle(selset, a, p)
        cy0 = cycle_components(inst, J0)
        ok0 = admits_ces_min_step(inst, forced, J0, cy0)
        if not ok0:
            all_ok = False
        if ok0 and len(cy0) <= ncy:
            some_ok = True
    return all_ok, some_ok


def admits_ces_min_step(inst, forced, J0, cy0):
    if not cy0:
        return False
    oldset = set(cy0)
    load = inst.loads(J0)
    for C in cy0:
        avoid = [a for a in C if a not in forced]
        if not avoid:
            continue
        d0 = INF
        info = []
        for a in avoid:
            d, dS, dH, tg = bfs_residual(inst, J0, load, a)
            if d < INF:
                info.append((a, d, dS, dH, tg))
                d0 = min(d0, d)
        if d0 == INF:
            continue
        for (a, d, dS, dH, tg) in info:
            if d != d0:
                continue
            for p in enum_paths(inst, J0, a, dS, dH, tg, CAP):
                nsel = toggle(J0, a, p)
                ok, _ = ces_pred(inst, oldset, nsel, C)
                if ok:
                    return True
    return False


def main():
    n = int(sys.argv[1])
    shard, nsh = 0, 1
    want_bplus2_all = "--bplus2-all" in sys.argv
    global CES_MODE
    for arg in sys.argv:
        if arg.startswith("--ces="):
            CES_MODE = arg.split("=")[1]
    rest = [a for a in sys.argv[2:] if not a.startswith("--")]
    if len(rest) >= 2:
        shard, nsh = int(rest[0]), int(rest[1])

    t0 = time.time()
    ctr = Counter()
    hist = Counter()
    witnesses = {"a1": [], "sd_short": [], "sd_2step": [],
                 "sd_2step_descent": [], "one_cycle_2plus": [],
                 "bplus2_all": [], "lemmaA": []}
    CAPW = 40

    proc = subprocess.Popen(["geng", "-bc", "-q", str(n)],
                            stdout=subprocess.PIPE, text=True)
    gi = -1
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        gi += 1
        if gi % nsh != shard:
            continue
        ctr["graphs"] += 1
        nn, adj = g6_decode(line)
        tau, fvss = min_fvs_all(adj, nn)
        if tau < 2:
            continue
        for Smask in fvss:
            Hv = [v for v in range(nn) if not ((Smask >> v) & 1)]
            Hedges = [(u, v) for ii, u in enumerate(Hv) for v in Hv[ii + 1:]
                      if (adj[u] >> v) & 1]
            for e in Hedges:
                inst = Inst(adj, nn, Smask, e)
                if not inst.ok:
                    continue
                sels = inst.selections()
                if not sels:
                    continue
                forced = inst.forced_set()
                for ch in sels:
                    selset = inst.sel_of(ch)
                    r = analyse_selection(inst, forced, selset,
                                          want_bplus2_all)
                    hist[r["ncyc"]] += 1
                    if r["ncyc"] == 0:
                        continue
                    ctr["cyclic_selections"] += 1
                    ctr["cycle_components"] += r["ncyc"]
                    ctr["lemmaA_violations"] += r["lemmaA"]
                    if r["ncyc"] >= 2 and len(witnesses["one_cycle_2plus"]) < CAPW:
                        witnesses["one_cycle_2plus"].append(
                            {"g6": line, "S": [int(x) for x in inst.S],
                             "e": [int(e[0]), int(e[1])], "ncyc": r["ncyc"]})
                    for pc in r["percycle"]:
                        if not pc["a1"] and pc["d0"] < INF:
                            ctr["a1_failures"] += 1
                            if len(witnesses["a1"]) < CAPW:
                                witnesses["a1"].append(
                                    {"g6": line,
                                     "S": [int(x) for x in inst.S],
                                     "e": [int(e[0]), int(e[1])],
                                     "d0": pc["d0"], "ncyc": r["ncyc"],
                                     "clen": len(pc["C"]),
                                     "dces": (None if pc.get("dces") in (None, INF)
                                              else pc["dces"])})
                    if not r["sd_short"]:
                        ctr["sd_short_failures"] += 1
                        if len(witnesses["sd_short"]) < CAPW:
                            witnesses["sd_short"].append(
                                {"g6": line, "S": [int(x) for x in inst.S],
                                 "e": [int(e[0]), int(e[1])],
                                 "ncyc": r["ncyc"]})
                    if not r["sd_count_short"]:
                        ctr["sd_count_short_failures"] += 1
                    if not r["sd_plus2"]:
                        ctr["sd_plus2_failures"] += 1
                    if want_bplus2_all and not r.get("bplus2_all", True):
                        ctr["bplus2_all_failures"] += 1
                        if len(witnesses["bplus2_all"]) < CAPW:
                            witnesses["bplus2_all"].append(
                                {"g6": line, "S": [int(x) for x in inst.S],
                                 "e": [int(e[0]), int(e[1])]})
                    # ---- SD-2STEP probes, only on A1-failing cycles
                    for pc in r["percycle"]:
                        if pc["a1"] or pc["d0"] == INF:
                            continue
                        ctr["sd_2step_probed"] += 1
                        allok, someok = probe_2step(inst, forced, selset,
                                                    r["percycle"], pc,
                                                    r["ncyc"])
                        if not allok:
                            ctr["sd_2step_failures"] += 1
                            if len(witnesses["sd_2step"]) < CAPW:
                                witnesses["sd_2step"].append(
                                    {"g6": line,
                                     "S": [int(x) for x in inst.S],
                                     "e": [int(e[0]), int(e[1])]})
                        if not someok:
                            ctr["sd_2step_descent_failures"] += 1
                            if len(witnesses["sd_2step_descent"]) < CAPW:
                                witnesses["sd_2step_descent"].append(
                                    {"g6": line,
                                     "S": [int(x) for x in inst.S],
                                     "e": [int(e[0]), int(e[1])]})
    proc.wait()
    out = {"n": n, "shard": shard, "nshards": nsh,
           "ces_mode": CES_MODE,
           "bplus2_all_graded": want_bplus2_all,
           "counters": dict(ctr),
           "ncyc_histogram": {str(k): v for k, v in sorted(hist.items())},
           "path_cap_hits": CAP[0],
           "wall_s": round(time.time() - t0, 2),
           "witnesses": witnesses}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
