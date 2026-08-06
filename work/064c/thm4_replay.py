#!/usr/bin/env python3
"""
thm4_replay.py -- replay the preserved A1-bad records and grade the FULL
Theorem 4 / Theorem 4' trichotomy of PROOFS-SAFE2-064c.md with the correct
scoping (Theorem 4 applies only when the terminal is not the released end).

Input: any number of scan result JSON files with an `a1_records` list
(g6, S, e, sel).  Each record is re-derived from its certificate; nothing is
taken on trust from the producing run.
"""
import sys, json, glob
import s2e_scan as B


def grade(g6, Slist, e, selraw):
    gn, adj = B.g6_decode(g6)
    col = B.bipartition(gn, adj)
    Sm = 0
    for s in Slist:
        Sm |= 1 << s
    inst = B.Inst(gn, adj, col, Sm, tuple(e))
    sel = tuple(tuple(p) for p in selraw)
    # certificate validation
    if list(inst.Slist) != list(Slist):
        return {"invalid": "S mismatch"}
    for s, p in zip(inst.Slist, sel):
        if len(p) != 2 or p[0] == p[1] or any(h not in inst.NH[s] for h in p):
            return {"invalid": "pair not an incidence pair at %d" % s}
    E, degH, inc = B.sel_state(inst, sel)
    for h in inst.Hlist:
        if degH[h] > inst.cap[h]:
            return {"invalid": "capacity violated at %d" % h}
    out = {"g6": g6, "S": Slist, "e": list(e), "cases": {}, "thm4_fail": [],
           "thm4p_fail": [], "cycles": 0, "a1bad": 0, "bad_steps": 0}
    cyc = B.selected_cycles(inst, E)
    old = set(c[1] for c in cyc)
    out["cycles"] = len(cyc)
    for (vs, es) in cyc:
        best, allp = None, []
        for (s, h) in es:
            d, ps = B.residual_paths(inst, E, degH, inc, (s, h))
            if d is None:
                continue
            if best is None or d < best:
                best, allp = d, [((s, h), p) for p in ps]
            elif d == best:
                allp += [((s, h), p) for p in ps]
        if best is None:
            out["thm4_fail"].append({"lemmaA": sorted(vs)})
            continue
        steps = []
        good = False
        for (a, p) in allp:
            ns = B.toggle(inst, sel, a, p)
            nE, nd, ninc = B.sel_state(inst, ns)
            nc = set(c[1] for c in B.selected_cycles(inst, nE))
            ces = (es not in nc) and nc <= old
            if ces:
                good = True
            steps.append((a, p, ns, ces, nc, nd))
        if good or best != 3:
            continue
        out["a1bad"] += 1
        for (a, p, ns, ces, nc, nd) in steps:
            if ces:
                continue
            out["bad_steps"] += 1
            s0, h0 = a
            h1, s1, h2 = p[1], p[2], p[3]
            comps = B.components(inst, E)
            Kcyc = any(h1 in cv and len(cv) == len(ce) for (cv, ce) in comps)
            new = nc - old
            if h2 != h0:
                case = "I"
                why = []
                if h1 in vs:
                    why.append("4a:h1_on_C")
                if s1 in vs:
                    why.append("4a:s1_on_C")
                if Kcyc:
                    why.append("4b:K_is_cycle")
                if len(new) != 1:
                    why.append("4c:new=%d" % len(new))
                else:
                    Zv = set()
                    for (u, v) in list(new)[0]:
                        Zv |= {u, v}
                    if Zv & vs:
                        why.append("4d:Z_meets_C")
                if len(nc) != len(old):
                    why.append("4e:count")
                if nd[h0] != inst.cap[h0] - 1:
                    why.append("4f:h_not_slack")
                if why:
                    out["thm4_fail"].append({"a": a, "p": p, "why": why})
            else:
                # Theorem 4': either (i) h1 off C, K a cycle, count drops by 1
                #             or     (ii) h1 in Q(C), new cycles inside V(C)
                if h1 not in vs:
                    case = "II(i)"
                    why = []
                    if not Kcyc:
                        why.append("4pi:K_not_cycle")
                    if len(nc) != len(old) - 1:
                        why.append("4pi:count=%d->%d" % (len(old), len(nc)))
                    if why:
                        out["thm4p_fail"].append({"a": a, "p": p, "why": why})
                else:
                    case = "II(ii)"
                    why = []
                    if s1 not in vs:
                        why.append("4pii:s1_off_C")
                    for Z in new:
                        Zv = set()
                        for (u, v) in Z:
                            Zv |= {u, v}
                        if not Zv <= vs:
                            why.append("4pii:new_cycle_outside_C")
                    if len(nc) not in (len(old), len(old) + 1):
                        why.append("4pii:count=%d->%d" % (len(old), len(nc)))
                    if why:
                        out["thm4p_fail"].append({"a": a, "p": p, "why": why})
            out["cases"][case] = out["cases"].get(case, 0) + 1
    return out


if __name__ == "__main__":
    files = []
    for pat in sys.argv[1:]:
        files += glob.glob(pat)
    agg = {"records": 0, "invalid": 0, "cases": {}, "bad_steps": 0,
           "a1bad": 0, "thm4_fail": [], "thm4p_fail": []}
    seen = set()
    for f in files:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for r in d.get("a1_records", []):
            key = (r["g6"], tuple(r["S"]), tuple(r["e"]),
                   tuple(tuple(p) for p in r["sel"]))
            if key in seen:
                continue
            seen.add(key)
            agg["records"] += 1
            g = grade(r["g6"], r["S"], r["e"], r["sel"])
            if "invalid" in g:
                agg["invalid"] += 1
                continue
            for k, v in g["cases"].items():
                agg["cases"][k] = agg["cases"].get(k, 0) + v
            agg["bad_steps"] += g["bad_steps"]
            agg["a1bad"] += g["a1bad"]
            agg["thm4_fail"] += [dict(g6=g["g6"], **x) for x in g["thm4_fail"]]
            agg["thm4p_fail"] += [dict(g6=g["g6"], **x)
                                  for x in g["thm4p_fail"]]
    agg["thm4_fail_n"] = len(agg["thm4_fail"])
    agg["thm4p_fail_n"] = len(agg["thm4p_fail"])
    agg["thm4_fail"] = agg["thm4_fail"][:10]
    agg["thm4p_fail"] = agg["thm4p_fail"][:10]
    print(json.dumps(agg, indent=1, default=str))
