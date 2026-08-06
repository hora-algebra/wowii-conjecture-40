#!/usr/bin/env python3
"""
s2e_scan11.py -- fast exhaustive pass for CL-1..CL-3, CL-6, CL-7 at n=11.

Design.  CL-2 (proved, and exhaustively verified at n<=10 by s2e_scan.py)
says a selected cycle is A1-good as soon as one of its S-vertices has a slack
G-neighbour.  This pass uses that as a FILTER only: every cycle that fails the
filter (no slack-adjacent S-vertex) is handed to the same full residual
machinery used at n<=10, which recomputes d0, enumerates every minimizing
path, toggles it and decides CES semantically.  If CL-2 were false the n=11
A1-failure count would disagree with the recorded anchor (six), so the filter
is self-testing against the anchor.

Independent verification of CL-1 at n=11 is done on a deterministic sample
(every SAMPLE-th slack-adjacent cycle gets the full treatment as well).
"""
import sys, json, time, subprocess, argparse
import s2e_scan as B

SAMPLE = 997

def cycles_fast(Slist, sel, NHset):
    """selected cycles of a selection; returns list of (Pset, Qset, edgeset)"""
    adj = {}
    for s, (a, b) in zip(Slist, sel):
        adj.setdefault(s, []).append(a)
        adj.setdefault(s, []) if False else None
        adj[s].append(b) if False else None
    # build properly
    adj = {}
    for s, (a, b) in zip(Slist, sel):
        adj[s] = [a, b]
        adj.setdefault(a, []).append(s)
        adj.setdefault(b, []).append(s)
    seen = set()
    out = []
    for v in adj:
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        vs = []
        ne = 0
        while stack:
            u = stack.pop()
            vs.append(u)
            ne += len(adj[u])
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        ne //= 2
        if ne == len(vs):
            P = [u for u in vs if u in NHset]
            Q = [u for u in vs if u not in NHset]
            es = set()
            for s in P:
                for h in adj[s]:
                    es.add((s, h))
            out.append((P, Q, frozenset(es)))
    return out

def run(n, shard, out, tlimit=None, verify_all=False, rng=None, ckpt=200):
    t0 = time.time()
    st = B.Stats()
    st.sampled_cl1 = 0
    lines = subprocess.run([B.GENG, "-bc", "-q", str(n)], capture_output=True,
                           text=True).stdout.split()
    seen_cycles = 0
    hard_records = []
    a1_records = []
    done_upto = (rng[0] - 1) if rng else -1
    for idx, g6 in enumerate(lines):
        if rng and not (rng[0] <= idx < rng[1]):
            continue
        if shard and idx % shard[1] != shard[0]:
            continue
        if rng and idx % ckpt == 0 and idx > rng[0]:
            checkpoint(st, n, shard, rng, done_upto, out, t0,
                       a1_records, hard_records)
        if tlimit and time.time() - t0 > tlimit:
            st.aborted_at = idx
            break
        gn, adj = B.g6_decode(g6)
        done_upto = idx
        col = B.bipartition(gn, adj)
        if col is None:
            continue
        k, fvss = B.min_fvs_all(gn, adj)
        if k < 1:
            continue
        st.graphs += 1
        for Sm in fvss:
            Hm = ((1 << gn) - 1) & ~Sm
            for i in B.bits(Hm):
                for j in B.bits(adj[i] & Hm):
                    if i >= j:
                        continue
                    inst = B.Inst(gn, adj, col, Sm, (i, j))
                    NHset = inst.NH
                    cap = inst.cap
                    Slist = inst.Slist
                    sels = B.feasible_selections(inst)
                    if not sels:
                        st.fail.setdefault("CL0-feasibility", []).append(
                            dict(g6=g6, S=Slist, e=(i, j)))
                        continue
                    st.instances += 1
                    st.selections += len(sels)
                    for sel in sels:
                        degH = {}
                        for (a, b) in sel:
                            degH[a] = degH.get(a, 0) + 1
                            degH[b] = degH.get(b, 0) + 1
                        cyc = cycles_fast(Slist, sel, NHset)
                        if not cyc:
                            continue
                        st.cycle_components += len(cyc)
                        cand = []
                        for (P, Q, es) in cyc:
                            slack_adj = False
                            for s in P:
                                for h in NHset[s]:
                                    if degH.get(h, 0) < cap[h]:
                                        slack_adj = True
                                        break
                                if slack_adj:
                                    break
                            if not slack_adj:
                                cand.append((P, Q, es))
                            else:
                                seen_cycles += 1
                                if verify_all or seen_cycles % SAMPLE == 0:
                                    st.sampled_cl1 += 1
                                    full_cycle_check(inst, g6, st, sel,
                                                     (P, Q, es), cyc)
                        if not cand:
                            continue
                        # full analysis on the A1-bad candidates
                        E, dH, inc = B.sel_state(inst, sel)
                        old = set(c[2] for c in cyc)
                        badcycles = []
                        for (P, Q, es) in cand:
                            res = full_cycle_check(inst, g6, st, sel,
                                                   (P, Q, es), cyc)
                            if res is not None and res[0] is False:
                                badcycles.append((P, Q, es, res[1]))
                        if badcycles:
                            st.a1_fail += len(badcycles)
                            a1_records.append(dict(g6=g6, S=Slist, e=(i, j),
                                                   sel=[list(p) for p in sel],
                                                   ncyc=len(cyc),
                                                   nbad=len(badcycles)))
                        # hard state: every selected cycle is A1-bad
                        if len(badcycles) == len(cyc):
                            st.hard_states += 1
                            hard_records.append(
                                cl67(inst, g6, st, sel, cyc, badcycles))
    s = st.summary()
    s["n"] = n
    s["range"] = rng
    s["done_upto"] = done_upto
    s["complete"] = (rng is None) or (done_upto >= rng[1] - 1)
    s["shard"] = shard
    s["aborted_at"] = getattr(st, "aborted_at", None)
    s["sampled_cl1"] = st.sampled_cl1
    s["seconds"] = round(time.time() - t0, 3)
    print(json.dumps(s, indent=1))
    if out:
        with open(out, "w") as f:
            json.dump({"summary": s,
                       "a1_records": a1_records[:200],
                       "hard_records": hard_records[:200],
                       "failures": {k: v[:20] for k, v in st.fail.items()
                                    if isinstance(v, list) and v}},
                      f, indent=1, default=str)
    return st

def full_cycle_check(inst, g6, st, sel, C, cyc):
    """returns (is_A1_good, minimizing_steps) and grades CL-1, CL-2, CL-3"""
    P, Q, es = C
    E, degH, inc = B.sel_state(inst, sel)
    old = set(c[2] for c in cyc)
    vs = set(P) | set(Q)
    best = None
    allpaths = []
    for (s, h) in es:
        d, paths = B.residual_paths(inst, E, degH, inc, (s, h))
        if d is None:
            continue
        if best is None or d < best:
            best, allpaths = d, [((s, h), p) for p in paths]
        elif d == best:
            allpaths += [((s, h), p) for p in paths]
    if best is None:
        st.fail.setdefault("LEMMA-A", []).append(
            dict(g6=g6, S=inst.Slist, e=inst.e, sel=sel, cyc=sorted(vs)))
        return None
    st.d0_hist[best] = st.d0_hist.get(best, 0) + 1
    slack_adj = any(degH[h] < inst.cap[h] for s in P for h in inst.NH[s])
    if (best == 1) != slack_adj:
        st.fail["CL2"].append(dict(g6=g6, S=inst.Slist, e=inst.e, sel=sel,
                                   cyc=sorted(vs), d0=best,
                                   slack_adj=slack_adj))
    good = False
    steps = []
    for (a, p) in allpaths:
        ns = B.toggle(inst, sel, a, p)
        nE, nd, ninc = B.sel_state(inst, ns)
        ncyc = set(c[1] for c in B.selected_cycles(inst, nE))
        is_ces = (es not in ncyc) and ncyc <= old
        if len(p) == 2 and not is_ces:
            st.fail["CL1"].append(dict(g6=g6, S=inst.Slist, e=inst.e, sel=sel,
                                       cyc=sorted(vs), a=a, path=p))
        if is_ces:
            good = True
        steps.append((a, p, ns, is_ces, len(ncyc)))
    # CL-3 is stated for A1-BAD cycles only: grade it after `good` is settled.
    if not good and best == 3:
        for (a, p, ns, is_ces, ncount) in steps:
            if is_ces:
                continue
            nE, nd, ninc = B.sel_state(inst, ns)
            ncyc = set(c[1] for c in B.selected_cycles(inst, nE))
            B.cl3_check(inst, g6, st, sel, (frozenset(vs), es), a, p, ns,
                        old, ncyc, E, degH, inc)
    return (good, steps)

def cl67(inst, g6, st, sel, cyc, badcycles):
    """CL-6 / CL-7 on a hard state"""
    rec = dict(g6=g6, S=inst.Slist, e=inst.e, sel=[list(p) for p in sel],
               ncyc=len(cyc), steps=0, ok=0)
    ok_any = False
    for (P, Q, es, steps) in badcycles:
        for (a, p, ns, is_ces, ncount) in steps:
            if ncount > len(cyc):
                continue
            nE, nd, ninc = B.sel_state(inst, ns)
            succ = False
            for (nvs, nes) in B.selected_cycles(inst, nE):
                for v in nvs:
                    if v in inst.NH and any(nd[h] < inst.cap[h]
                                            for h in inst.NH[v]):
                        succ = True
            st.cl7_steps += 1
            rec["steps"] += 1
            if succ:
                ok_any = True
                rec["ok"] += 1
            else:
                st.fail["CL7"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                           sel=[list(x) for x in sel],
                                           a=a, path=p))
    if ok_any:
        st.cl6_ok += 1
    else:
        st.fail["CL6"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                   sel=[list(x) for x in sel]))
    return rec

def checkpoint(st, n, shard, rng, done_upto, out, t0, a1_records,
               hard_records):
    s = st.summary()
    s.update(n=n, shard=shard, range=rng, done_upto=done_upto,
             complete=False, seconds=round(time.time() - t0, 3))
    if out:
        with open(out + ".partial", "w") as f:
            json.dump({"summary": s, "a1_records": a1_records[:200],
                       "hard_records": hard_records[:400],
                       "failures": {k: v[:20] for k, v in st.fail.items()
                                    if isinstance(v, list) and v}},
                      f, indent=1, default=str)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=11)
    ap.add_argument("--shard")
    ap.add_argument("--out")
    ap.add_argument("--tlimit", type=float)
    ap.add_argument("--verify-all", action="store_true")
    ap.add_argument("--range")
    A = ap.parse_args()
    sh = None
    if A.shard:
        i, k = A.shard.split("/")
        sh = (int(i), int(k))
    rg = None
    if A.range:
        a, b = A.range.split(":")
        rg = (int(a), int(b))
    run(A.n, sh, A.out, tlimit=A.tlimit, verify_all=A.verify_all, rng=rg)
