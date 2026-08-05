"""ONE-CYCLE scanner (PREREG-SD.md §6): does any feasible selection have >= 2 selected cycles?

Lean by design: it needs only the feasible selections and their selected-cycle
counts, not residual paths or CES, so it reaches orders the full sd_scan cannot.

Speed note (and why the count is exact). J u {e} has maximum degree 2 (demand 2
at each s; cap <= 2 at each h; the two fixed-edge endpoints have cap 1 and take
e as their second edge). A max-degree-2 graph is a disjoint union of paths and
cycles, so no component holds two cycles and "number of cyclic components" is
well defined. Suppressing every s (degree exactly 2) turns J into a multigraph M
on H with one edge {h1,h2} per s; incidence cycles of J correspond exactly to
cycles of M (a 4-cycle of J becomes a parallel pair in M). So the number of
selected cycles equals the number of edge insertions of M that close a cycle,
which union-find counts incrementally during the enumeration.

Enumeration uses incremental capacity pruning rather than a full product, so it
is much faster than eval_L1_holdout.feasible on dense instances; the anchor
counts below are what verify the two agree.

usage: python3 onecycle_scan.py N [shard nshards]
"""
import sys, subprocess, json
from itertools import combinations
from collections import defaultdict
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all


def scan_instance(nn, adj, S, Hv, x, y, hist, witness_sink, g6):
    """enumerate every feasible selection; tally its selected-cycle count."""
    cap = {h: 2 for h in Hv}
    cap[x] = 1
    cap[y] = 1
    Sl = list(S)
    pairs = []
    for s in Sl:
        nb = [h for h in Hv if adj[s] >> h & 1]
        p = [pr for pr in combinations(nb, 2)]
        if not p:
            return
        pairs.append(p)
    load = defaultdict(int)
    par = {h: h for h in Hv}

    def find(a):
        # NO path compression: the enumeration backtracks, and the only sound
        # O(1) undo is restoring the single parent entry a union wrote. With
        # compression, find() mutates other entries too and the undo is wrong
        # (this cost 17 spurious cycles at n=8 before the anchor caught it).
        while par[a] != a:
            a = par[a]
        return a

    chosen = []

    def rec(i, ncyc):
        if i == len(Sl):
            hist[ncyc] += 1
            if ncyc >= 2 and len(witness_sink) < 20:
                witness_sink.append(dict(g6=g6, S=sorted(Sl), e=[x, y],
                                         ncyc=ncyc, pairs=list(chosen)))
            return
        for (h1, h2) in pairs[i]:
            if load[h1] >= cap[h1] or load[h2] >= cap[h2]:
                continue
            load[h1] += 1
            load[h2] += 1
            r1, r2 = find(h1), find(h2)
            if r1 == r2:
                closed = True
            else:
                closed = False
                par[r1] = r2
            chosen.append((h1, h2))
            rec(i + 1, ncyc + (1 if closed else 0))
            chosen.pop()
            if not closed:
                par[r1] = r1
            load[h1] -= 1
            load[h2] -= 1

    rec(0, 0)


def main():
    NN = sys.argv[1] if len(sys.argv) > 1 else '9'
    shard = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    nsh = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    tag = f"n{NN}-{shard}of{nsh}"
    OUT, PROG = f"oc-{tag}.txt", f"oc-{tag}-prog.txt"
    open(PROG, "w").close()
    gs = subprocess.run(['geng', '-bc', '-q', NN],
                        capture_output=True, text=True).stdout.split()
    hist = defaultdict(int)
    wit = []
    for gi, g6 in enumerate(gs):
        if gi % nsh != shard:
            continue
        if gi % 500 < nsh:
            tot = sum(v for k, v in hist.items() if k >= 1)
            cyc = sum(k * v for k, v in hist.items())
            open(PROG, "a").write(f"g {gi}/{len(gs)} cyclicJ={tot} cycles={cyc} "
                                  f"maxcyc={max(hist) if hist else 0} ge2={len(wit)}\n")
        nn, adj = inv_b.parse_g6(g6)
        k = EB.tau(nn, adj)
        if k < 2:
            continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S)
            Hv = [v for v in range(nn) if v not in Sset]
            for (x, y) in [(u, w) for u in Hv for w in Hv
                           if u < w and adj[u] >> w & 1]:
                scan_instance(nn, adj, Sset, Hv, x, y, hist, wit, g6)
    res = dict(n=NN, shard=shard, nshards=nsh, graphs=len(gs),
               feasible_selections=sum(hist.values()),
               cyclic_selections=sum(v for k, v in hist.items() if k >= 1),
               cycle_components=sum(k * v for k, v in hist.items()),
               max_cycles=max(hist) if hist else 0,
               ncyc_histogram={str(k): v for k, v in sorted(hist.items())},
               ONE_CYCLE_violations=sum(v for k, v in hist.items() if k >= 2),
               witnesses=wit)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"onecycle n={NN} shard {shard}/{nsh} DONE feas={res['feasible_selections']} "
          f"cyclicJ={res['cyclic_selections']} cycles={res['cycle_components']} "
          f"maxcyc={res['max_cycles']} ONE_CYCLE_violations={res['ONE_CYCLE_violations']}")


if __name__ == "__main__":
    main()
