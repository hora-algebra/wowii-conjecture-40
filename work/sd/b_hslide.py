"""FROZEN n=12 holdout checker for B-PLUS-2, B-TERMINAL-SLIDE, B-H-SLIDE.
Per selected cycle C:
  d0 = min residual augmenting-path length over avoidable edges.
  If some shortest pair is CES -> gap 0, all three statements hold.
  Else (gap>0): search 2-edge terminal slides Q+ = Q0 + [u, t'] on the same
  released edge (Q0 a shortest bad path; (t,u) selected, (u,t') unselected, simple,
  feasible) and record:
    B-PLUS-2      : a CES path of length <= d0+2 exists (dCES<=d0+2).
    B-TERMINAL-SLIDE: some such slide (t' any residual terminal) is CES.
    B-H-SLIDE     : some such slide with t' = freed endpoint h is CES.
    no-CES flag   : no CES path found up to length d0+2 (would also fail B-ANY at
                    this bound; the cycle is preserved as a witness, NOT silently
                    passed).
Failures preserved per statement. Fresh residual-DAG engine (a1_verify)."""
import sys, subprocess
from collections import defaultdict
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
from eval_L1_holdout import feasible, comps, ncyc
from mine_n10 import walk_cycle
from a1_verify import norm, cyc_sets_edges, residual_dag, enum_shortest_paths, toggle

OUT = "b-hslide.txt"
PROG = "b-hslide-prog.txt"

def slides_from(nn, adj, Sset, x, y, J, a, Q0):
    """all Q+ = Q0 + [u, t'] : (t,u) selected in J-a-toggled-by-Q0, (u,t') unselected,
    simple, t' residual-capacity H terminal. Returns list of (Q+, u, t')."""
    s, h = (a[0], a[1]) if a[0] in Sset else (a[1], a[0])
    t = Q0[-1]
    M0 = set(toggle(J, a, Q0))          # J0 = state after toggling Q0
    cap = {hh: 2 for hh in range(nn) if hh not in Sset}; cap[x] = 1; cap[y] = 1
    deg = defaultdict(int)
    for (u2, v2) in M0: deg[u2] += 1; deg[v2] += 1
    res = []
    for u in range(nn):
        if u in Sset and (adj[t] >> u & 1) and u not in Q0:
            e_tu = (min(t, u), max(t, u))
            if e_tu not in M0: continue           # (t,u) must be selected in J0
            for tp in range(nn):
                if tp in Sset or tp in Q0 or tp == u: continue
                if not (adj[u] >> tp & 1): continue
                e_utp = (min(u, tp), max(u, tp))
                if e_utp in M0: continue           # (u,t') must be unselected
                if deg[tp] >= cap[tp]: continue    # t' residual capacity (before add)
                res.append((Q0 + [u, tp], u, tp))
    return res

def is_ces(Jp, Ccc, Jcyc, x, y):
    Jpc = cyc_sets_edges(Jp, x, y)
    return Ccc not in Jpc and Jpc <= Jcyc

if __name__ == "__main__":
    open(OUT, "w").close(); open(PROG, "w").close()
    NN = sys.argv[1] if len(sys.argv) > 1 else '12'
    gs = subprocess.run(['geng', '-bc', '-q', NN], capture_output=True, text=True).stdout.split()
    n_cyc = 0; nonvac = 0; gappos = 0
    f_bplus2 = f_tslide = f_hslide = f_noces = 0
    gap_hist = defaultdict(int); maxgap = 0
    fails = defaultdict(list)
    gi = 0
    for g6 in gs:
        gi += 1
        if gi % 500 == 0:
            open(PROG, "a").write(f"g {gi}/{len(gs)} cyc={n_cyc} gappos={gappos} "
                                  f"fB2={f_bplus2} fTS={f_tslide} fHS={f_hslide} fNO={f_noces} maxgap={maxgap}\n")
        nn, adj = inv_b.parse_g6(g6); k = EB.tau(nn, adj)
        if k < 2: continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S); Hv = [v for v in range(nn) if v not in Sset]
            for (x, y) in [(u, w) for u in Hv for w in Hv if u < w and adj[u] >> w & 1]:
                feas = feasible(nn, adj, list(S), x, y)
                if not feas: continue
                Pd = {J: ncyc(J, (x, y)) for J in feas}
                for J in feas:
                    if Pd[J] == 0: continue
                    Jcyc = cyc_sets_edges(norm(J), x, y)
                    for (cc, iscy) in comps(J, (x, y)):
                        if not iscy: continue
                        n_cyc += 1; Ccc = frozenset(cc)
                        order, _ = walk_cycle(cc, J, x, y)
                        cyc_edges = [ed for (kk, ed) in order if kk == 'J']
                        edata = []
                        for ed in cyc_edges:
                            an = (min(ed), max(ed)); s = ed[0] if ed[0] in Sset else ed[1]
                            h = ed[1] if ed[0] in Sset else ed[0]
                            dg = residual_dag(nn, adj, Sset, x, y, J, an, s)
                            if dg is not None: edata.append((an, s, h, dg))
                        if not edata: continue
                        d0 = min(dg[0] for (_, _, _, dg) in edata)
                        A0 = [(an, s, h, dg) for (an, s, h, dg) in edata if dg[0] == d0]
                        # gap 0 ?
                        shortest_ces = False; bad_short = []   # (an,s,h,Q0)
                        for (an, s, h, (d, fw, td)) in A0:
                            for p in enum_shortest_paths(fw, s, td, d):
                                if is_ces(toggle(J, an, p), Ccc, Jcyc, x, y): shortest_ces = True
                                else: bad_short.append((an, s, h, p))
                        if shortest_ces:
                            gap_hist[0] += 1
                            continue
                        # gap > 0: this is nonvacuous (A1 would fail here)
                        nonvac += 1; gappos += 1
                        bplus2 = tslide = hslide = False; found_ces_len = None
                        for (an, s, h, Q0) in bad_short:
                            for (Qp, u, tp) in slides_from(nn, adj, Sset, x, y, J, an, Q0):
                                if is_ces(toggle(J, an, Qp), Ccc, Jcyc, x, y):
                                    L = len(Qp) - 1
                                    bplus2 = bplus2 or (L <= d0 + 2); tslide = True
                                    if tp == h: hslide = True
                                    if found_ces_len is None or L < found_ces_len: found_ces_len = L
                        # record
                        if found_ces_len is None:
                            f_noces += 1
                            if len(fails['noCES']) < 20: fails['noCES'].append((g6, sorted(S), (x, y), sorted(cc), d0))
                        else:
                            gap = found_ces_len - d0; gap_hist[gap] += 1; maxgap = max(maxgap, gap)
                            if gap > 2:
                                f_bplus2 += 1
                                if len(fails['BPLUS2']) < 20: fails['BPLUS2'].append((g6, sorted(S), (x, y), sorted(cc), d0, found_ces_len))
                        if not tslide:
                            f_tslide += 1
                            if len(fails['TSLIDE']) < 20: fails['TSLIDE'].append((g6, sorted(S), (x, y), sorted(cc), d0))
                        if not hslide:
                            f_hslide += 1
                            if len(fails['HSLIDE']) < 20: fails['HSLIDE'].append((g6, sorted(S), (x, y), sorted(cc), d0))
    with open(OUT, "a") as f:
        f.write(f"=== B-PLUS-2 / B-TERMINAL-SLIDE / B-H-SLIDE HOLDOUT (n={NN}) ===\n")
        f.write(f"cycle_components = {n_cyc}; positive-gap (A1-failing) = {gappos}\n")
        f.write(f"no-CES-at-<=d0+2 failures = {f_noces}\n")
        f.write(f"B-PLUS-2 failures (gap>2) = {f_bplus2}\n")
        f.write(f"B-TERMINAL-SLIDE failures = {f_tslide}\n")
        f.write(f"B-H-SLIDE failures = {f_hslide}\n")
        f.write(f"gap histogram = {dict(sorted(gap_hist.items()))}; max gap = {maxgap}\n")
        for kk, ex in fails.items():
            if ex: f.write(f"-- {kk} witnesses:\n" + "\n".join(f"   {e}" for e in ex) + "\n")
    print(f"b_hslide n={NN} DONE cyc={n_cyc} gappos={gappos} noCES={f_noces} "
          f"B2fail={f_bplus2} TSfail={f_tslide} HSfail={f_hslide} maxgap={maxgap}")
