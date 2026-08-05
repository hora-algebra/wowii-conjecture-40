"""FROZEN checker for the SD (scheduled-descent) statements of PREREG-SD.md.

Per feasible selection J with at least one selected cycle it grades, on the SAME
per-cycle predicate the frozen tools/b_hslide.py uses (`A1(C)` = some residual
augmenting path of length d0(C) is CES for C):

  A1-ALL          (control, the FALSIFIED statement) : A1(C) for EVERY cycle C of J
  SD-SHORT        : A1(C) for SOME cycle C of J
  SD-COUNT-SHORT  : some shortest toggle at some cycle strictly lowers |cyc(J)|
  SD-PLUS-2       : some cycle of J admits a CES path of length <= d0(C)+2

and records, for every J that contains at least one A1-failing cycle, the pair
(|cyc(J)|, #A1-good cycles of J) plus the full certificate.

Engine: imports the frozen a1_verify / eval_L1_holdout / mine_n10 / eval_frozen
modules, so the per-cycle predicate is bit-identical to b_hslide's.

usage:  python3 sd_scan.py N [shard nshards] [--ces=always|never]
"""
import sys, subprocess, json
from collections import defaultdict
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
from eval_L1_holdout import feasible, comps
from mine_n10 import walk_cycle
from a1_verify import (norm, cyc_sets_edges, residual_dag, enum_shortest_paths,
                       toggle, PATHCAP)

CES_MODE = "real"          # overridden by --ces=


def is_ces(Jp, Ccc, Jcyc, x, y):
    """semantic CES: C destroyed, and no cycle present that was not already there."""
    if CES_MODE == "always":
        return True
    if CES_MODE == "never":
        return False
    Jpc = cyc_sets_edges(Jp, x, y)
    return Ccc not in Jpc and Jpc <= Jcyc


def slides_from(nn, adj, Sset, x, y, J, a, Q0):
    """two-edge terminal slides Q+ = Q0 + [u,t'] on the same released edge a.
    Identical construction to tools/b_hslide.py::slides_from."""
    t = Q0[-1]
    M0 = set(toggle(J, a, Q0))
    cap = {hh: 2 for hh in range(nn) if hh not in Sset}
    cap[x] = 1
    cap[y] = 1
    deg = defaultdict(int)
    for (u2, v2) in M0:
        deg[u2] += 1
        deg[v2] += 1
    res = []
    for u in range(nn):
        if u in Sset and (adj[t] >> u & 1) and u not in Q0:
            e_tu = (min(t, u), max(t, u))
            if e_tu not in M0:
                continue
            for tp in range(nn):
                if tp in Sset or tp in Q0 or tp == u:
                    continue
                if not (adj[u] >> tp & 1):
                    continue
                if (min(u, tp), max(u, tp)) in M0:
                    continue
                if deg[tp] >= cap[tp]:
                    continue
                res.append(Q0 + [u, tp])
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    global CES_MODE
    for a in sys.argv[1:]:
        if a.startswith("--ces="):
            CES_MODE = a.split("=", 1)[1]
    NN = args[0] if args else '9'
    shard = int(args[1]) if len(args) > 1 else 0
    nsh = int(args[2]) if len(args) > 2 else 1
    tag = f"n{NN}-{shard}of{nsh}" + ("" if CES_MODE == "real" else f"-ces{CES_MODE}")
    OUT, PROG = f"sd-{tag}.txt", f"sd-{tag}-prog.txt"
    open(PROG, "w").close()

    gs = subprocess.run(['geng', '-bc', '-q', NN],
                        capture_output=True, text=True).stdout.split()
    ngraphs = len(gs)

    n_cyc = 0                 # cycle components seen (anchor)
    n_selJ = 0                # feasible selections with >=1 cycle
    f_a1all = 0               # per-CYCLE A1 failures  (anchor: 6 at n=11)
    f_sdshort = 0             # per-SELECTION SD-SHORT failures
    f_sdcount = 0
    f_sdplus2 = 0
    n_lemA = 0                # cycles with no avoidable incidence (Lemma A violation)
    n_capped = 0              # cycles where path enumeration hit PATHCAP with no CES
    profile = defaultdict(int)   # (|cyc(J)|, #A1-good) for J containing an A1-bad cycle
    ncyc_hist = defaultdict(int)
    witnesses = defaultdict(list)

    for gi, g6 in enumerate(gs):
        if gi % nsh != shard:
            continue
        if gi % 500 < nsh:
            open(PROG, "a").write(
                f"g {gi}/{ngraphs} cyc={n_cyc} selJ={n_selJ} A1allfail={f_a1all} "
                f"SDSHORTfail={f_sdshort} SDCOUNTfail={f_sdcount} SDP2fail={f_sdplus2} "
                f"lemA={n_lemA} capped={n_capped}\n")
        nn, adj = inv_b.parse_g6(g6)
        k = EB.tau(nn, adj)
        if k < 2:
            continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S)
            Hv = [v for v in range(nn) if v not in Sset]
            for (x, y) in [(u, w) for u in Hv for w in Hv
                           if u < w and adj[u] >> w & 1]:
                feas = feasible(nn, adj, list(S), x, y)
                if not feas:
                    continue
                for J in feas:
                    cycs = [cc for (cc, iscy) in comps(J, (x, y)) if iscy]
                    if not cycs:
                        continue
                    n_selJ += 1
                    ncyc_hist[len(cycs)] += 1
                    Jcyc = cyc_sets_edges(norm(J), x, y)
                    nc = len(Jcyc)
                    a1_good = 0
                    any_count_drop = False
                    any_plus2 = False
                    bad_cycles = []
                    for cc in cycs:
                        n_cyc += 1
                        Ccc = frozenset(cc)
                        order, _ = walk_cycle(cc, J, x, y)
                        cyc_edges = [ed for (kk, ed) in order if kk == 'J']
                        edata = []
                        for ed in cyc_edges:
                            an = (min(ed), max(ed))
                            s = ed[0] if ed[0] in Sset else ed[1]
                            h = ed[1] if ed[0] in Sset else ed[0]
                            dg = residual_dag(nn, adj, Sset, x, y, J, an, s)
                            if dg is not None:
                                edata.append((an, s, h, dg))
                        if not edata:
                            n_lemA += 1
                            f_a1all += 1
                            bad_cycles.append((sorted(cc), None, "no-avoidable"))
                            continue
                        d0 = min(dg[0] for (_, _, _, dg) in edata)
                        A0 = [t for t in edata if t[3][0] == d0]
                        ces_short = False
                        capped = False
                        bad_short = []
                        for (an, s, h, (d, fw, td)) in A0:
                            paths = enum_shortest_paths(fw, s, td, d)
                            if len(paths) >= PATHCAP:
                                capped = True
                            for p in paths:
                                Jp = toggle(J, an, p)
                                if is_ces(Jp, Ccc, Jcyc, x, y):
                                    ces_short = True
                                else:
                                    bad_short.append((an, s, h, p))
                                    if len(cyc_sets_edges(Jp, x, y)) < nc:
                                        any_count_drop = True
                            if ces_short:
                                break
                        if ces_short:
                            a1_good += 1
                            any_count_drop = True     # CES implies strict decrease
                            any_plus2 = True
                            continue
                        f_a1all += 1
                        if capped:
                            n_capped += 1
                        bad_cycles.append((sorted(cc), d0, "no-shortest-CES"))
                        # SD-PLUS-2 for this cycle: 2-edge terminal slides
                        for (an, s, h, Q0) in bad_short:
                            for Qp in slides_from(nn, adj, Sset, x, y, J, an, Q0):
                                Jp = toggle(J, an, Qp)
                                if is_ces(Jp, Ccc, Jcyc, x, y):
                                    any_plus2 = True
                                if len(cyc_sets_edges(Jp, x, y)) < nc:
                                    pass          # not counted: slide is length d0+2
                            if any_plus2:
                                break
                    if a1_good == 0:
                        f_sdshort += 1
                        if len(witnesses['SD-SHORT']) < 50:
                            witnesses['SD-SHORT'].append(
                                dict(g6=g6, S=sorted(Sset), e=[x, y],
                                     J=sorted(sorted(z) for z in J),
                                     ncyc=len(cycs),
                                     cycles=[sorted(c) for c in cycs]))
                    if not any_count_drop:
                        f_sdcount += 1
                        if len(witnesses['SD-COUNT-SHORT']) < 50:
                            witnesses['SD-COUNT-SHORT'].append(
                                dict(g6=g6, S=sorted(Sset), e=[x, y],
                                     J=sorted(sorted(z) for z in J), ncyc=len(cycs)))
                    if not any_plus2:
                        f_sdplus2 += 1
                        if len(witnesses['SD-PLUS-2']) < 50:
                            witnesses['SD-PLUS-2'].append(
                                dict(g6=g6, S=sorted(Sset), e=[x, y],
                                     J=sorted(sorted(z) for z in J), ncyc=len(cycs)))
                    if bad_cycles:
                        profile[(len(cycs), a1_good)] += 1
                        if len(witnesses['A1-BAD-SELECTION']) < 50:
                            witnesses['A1-BAD-SELECTION'].append(
                                dict(g6=g6, S=sorted(Sset), e=[x, y],
                                     J=sorted(sorted(z) for z in J),
                                     ncyc=len(cycs), a1_good=a1_good,
                                     bad=bad_cycles,
                                     cycles=[sorted(c) for c in cycs]))

    res = dict(n=NN, shard=shard, nshards=nsh, ces_mode=CES_MODE,
               graphs=ngraphs, cycle_components=n_cyc, cyclic_selections=n_selJ,
               A1_ALL_failures=f_a1all, SD_SHORT_failures=f_sdshort,
               SD_COUNT_SHORT_failures=f_sdcount, SD_PLUS_2_failures=f_sdplus2,
               lemmaA_violations=n_lemA, path_cap_hits=n_capped,
               ncyc_histogram={str(k2): v for k2, v in sorted(ncyc_hist.items())},
               a1bad_profile={f"{a}|{b}": v for (a, b), v in sorted(profile.items())},
               witnesses={k2: v for k2, v in witnesses.items()})
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"sd_scan n={NN} shard {shard}/{nsh} ces={CES_MODE} DONE "
          f"cyc={n_cyc} selJ={n_selJ} A1allfail={f_a1all} SDSHORTfail={f_sdshort} "
          f"SDCOUNTfail={f_sdcount} SDP2fail={f_sdplus2} lemA={n_lemA} capped={n_capped}")


if __name__ == "__main__":
    main()
