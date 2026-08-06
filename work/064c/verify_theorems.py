#!/usr/bin/env python3
"""
verify_theorems.py -- targeted oracle checks for Theorems 4, 4', 6, 8 of
PROOFS-SAFE2-064c.md, plus premise-frequency reporting (so that a "0 failures"
line is never mistaken for a vacuous check).

  --closure n   : how often the Theorem-6 premise (slack-free closure of a
                  selected cycle) actually holds, and whether its conclusions
                  hold when it does.
  --hard n      : replay every hard state at order n; for each bad minimizing
                  step check Theorem 4 (a)-(f), Theorem 8 (d0(Z) <= 3) and
                  report the d0(Z) distribution.
"""
import sys, json, argparse, subprocess
import s2e_scan as B


def closure_stats(n):
    lines = subprocess.run([B.GENG, "-bc", "-q", str(n)], capture_output=True,
                           text=True).stdout.split()
    fired = 0
    cycles = 0
    fails = []
    Wsizes = {}
    for g6 in lines:
        gn, adj = B.g6_decode(g6)
        col = B.bipartition(gn, adj)
        if col is None:
            continue
        k, fvss = B.min_fvs_all(gn, adj)
        if k < 1:
            continue
        for Sm in fvss:
            Hm = ((1 << gn) - 1) & ~Sm
            for i in B.bits(Hm):
                for j in B.bits(adj[i] & Hm):
                    if i >= j:
                        continue
                    inst = B.Inst(gn, adj, col, Sm, (i, j))
                    for sel in B.feasible_selections(inst):
                        E, degH, inc = B.sel_state(inst, sel)
                        for (vs, es) in B.selected_cycles(inst, E):
                            cycles += 1
                            P = [v for v in vs if v in inst.NH]
                            A, Y, reached = B.closure(inst, E, degH, inc, P)
                            if reached:
                                continue
                            fired += 1
                            NA = set()
                            for s in A:
                                NA |= set(inst.NH[s])
                            W = NA - Y
                            Wsizes[len(W)] = Wsizes.get(len(W), 0) + 1
                            bad = []
                            if B.rho(inst, A) != 2 * len(A):
                                bad.append("not_tight")
                            if len(NA) < len(A) + 1:
                                bad.append("NA_too_small")
                            if not W:
                                bad.append("W_empty")
                            else:
                                forced = B.forced_incidences(inst)
                                for s in A:
                                    for h in inst.NH[s]:
                                        if h in W and (s, h) not in forced:
                                            bad.append("unforced")
                                            break
                            Q = set(v for v in vs if v not in inst.NH)
                            if not (Q & Y):
                                bad.append("no_Q_in_Y(Cor6.1)")
                            if bad:
                                fails.append(dict(g6=g6, S=inst.Slist,
                                                  e=inst.e, sel=sel,
                                                  cyc=sorted(vs), why=bad))
    print(json.dumps(dict(n=n, cycles=cycles, premise_fired=fired,
                          W_size_hist=Wsizes, failures=len(fails),
                          first_failures=fails[:5]), indent=1, default=str))


def hard_replay(n):
    lines = subprocess.run([B.GENG, "-bc", "-q", str(n)], capture_output=True,
                           text=True).stdout.split()
    out = dict(n=n, hard_states=0, bad_steps=0, thm4_fail=[], thm8_fail=[],
               d0Z_hist={}, case_hist={}, cl6_ok=0)
    for g6 in lines:
        gn, adj = B.g6_decode(g6)
        col = B.bipartition(gn, adj)
        if col is None:
            continue
        k, fvss = B.min_fvs_all(gn, adj)
        if k < 1:
            continue
        for Sm in fvss:
            Hm = ((1 << gn) - 1) & ~Sm
            for i in B.bits(Hm):
                for j in B.bits(adj[i] & Hm):
                    if i >= j:
                        continue
                    inst = B.Inst(gn, adj, col, Sm, (i, j))
                    for sel in B.feasible_selections(inst):
                        E, degH, inc = B.sel_state(inst, sel)
                        cyc = B.selected_cycles(inst, E)
                        if not cyc:
                            continue
                        old = set(c[1] for c in cyc)
                        # hard?  every cycle A1-bad
                        allbad = True
                        percyc = []
                        for (vs, es) in cyc:
                            # Theorem 2 (proved): a cycle with a slack-adjacent
                            # S-vertex is A1-good, so the state is not hard.
                            if any(degH[hh] < inst.cap[hh]
                                   for v in vs if v in inst.NH
                                   for hh in inst.NH[v]):
                                allbad = False
                                break
                            best, allp = None, []
                            for (s, h) in es:
                                d, ps = B.residual_paths(inst, E, degH, inc,
                                                         (s, h))
                                if d is None:
                                    continue
                                if best is None or d < best:
                                    best, allp = d, [((s, h), p) for p in ps]
                                elif d == best:
                                    allp += [((s, h), p) for p in ps]
                            if best is None:
                                allbad = False
                                break
                            good = False
                            steps = []
                            for (a, p) in allp:
                                ns = B.toggle(inst, sel, a, p)
                                nE, nd, ninc = B.sel_state(inst, ns)
                                nc = set(c[1] for c in
                                         B.selected_cycles(inst, nE))
                                ces = (es not in nc) and nc <= old
                                if ces:
                                    good = True
                                steps.append((a, p, ns, ces, nc))
                            if good:
                                allbad = False
                                break
                            percyc.append(((vs, es), best, steps))
                        if not allbad or not percyc:
                            continue
                        out["hard_states"] += 1
                        ok_any = False
                        for ((vs, es), best, steps) in percyc:
                            for (a, p, ns, ces, nc) in steps:
                                if ces:
                                    continue
                                out["bad_steps"] += 1
                                s0, h0 = a
                                h1 = p[1]
                                s1 = p[2] if len(p) > 2 else None
                                h2 = p[3] if len(p) > 3 else None
                                case = ("I" if (h2 is not None and h2 != h0)
                                        else "II")
                                out["case_hist"][case] = \
                                    out["case_hist"].get(case, 0) + 1
                                if case == "I":
                                    why = []
                                    if h1 in vs:
                                        why.append("a")
                                    if s1 in vs:
                                        why.append("a2")
                                    if len(nc - old) != 1:
                                        why.append("c")
                                    else:
                                        Z = list(nc - old)[0]
                                        Zv = set()
                                        for (u, v) in Z:
                                            Zv |= {u, v}
                                        if Zv & vs:
                                            why.append("d")
                                    if len(nc) != len(old):
                                        why.append("e")
                                    nE, nd, ninc = B.sel_state(inst, ns)
                                    if nd[h0] != inst.cap[h0] - 1:
                                        why.append("f")
                                    if why:
                                        out["thm4_fail"].append(
                                            dict(g6=g6, why=why, a=a, p=p))
                                # Theorem 8: d0 of every new cycle <= 3
                                nE, nd, ninc = B.sel_state(inst, ns)
                                for Z in (nc - old):
                                    zbest = None
                                    for (u, v) in Z:
                                        d, _ = B.residual_paths(inst, nE, nd,
                                                                ninc, (u, v))
                                        if d is not None and (zbest is None
                                                              or d < zbest):
                                            zbest = d
                                    out["d0Z_hist"][str(zbest)] = \
                                        out["d0Z_hist"].get(str(zbest), 0) + 1
                                    if zbest is None or zbest > 3:
                                        out["thm8_fail"].append(
                                            dict(g6=g6, a=a, p=p, d0Z=zbest))
                                    if zbest == 1:
                                        ok_any = True
                        if ok_any:
                            out["cl6_ok"] += 1
    out["thm4_fail"] = out["thm4_fail"][:5]
    out["thm8_fail"] = out["thm8_fail"][:5]
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--closure", type=int)
    ap.add_argument("--hard", type=int)
    A = ap.parse_args()
    if A.closure:
        closure_stats(A.closure)
    if A.hard:
        hard_replay(A.hard)
