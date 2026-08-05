r"""VERIFY-3 P2: n=9 full-universe anchor for the fresh Lemma-B engine.
Expected (codex gold + VERIFY-2 lineage): 730 connected bipartite graphs,
24,195 selected cycle components over all instances/selections, 0 A1
failures (every selected cycle admits a CES minimizing step)."""
import subprocess
import sys
from itertools import combinations
from multiprocessing import Pool

sys.path.insert(0, 'verify3')
from graph_fcore_verify3 import decode_g6, min_fvs_size, all_min_fvs
from lemmab_verify3 import instance_selections, sel_cycles
from tail_scan import quick_cycle


def scan(g6):
    n, adj = decode_g6(g6)
    tau = min_fvs_size(n, adj)
    ncomp = nbad = ncycsel = 0
    if tau < 2:
        return (0, 0, 0)
    for S in all_min_fvs(n, adj, tau):
        rest = sorted(set(range(n)) - S)
        nbH = {s: frozenset(w for w in adj[s] if w not in S) for s in S}
        nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in rest}
        for (a, b) in combinations(rest, 2):
            if b not in adj[a]:
                continue
            cap = {h: 2 for h in rest}
            cap[a] = cap[b] = 1
            Sl, sels = instance_selections(S, nbH, cap)
            for J in sels:
                cycles = sel_cycles(J)
                if not cycles:
                    continue
                ncycsel += 1
                for C in cycles:
                    ncomp += 1
                    d0, steps = quick_cycle(J, C, sels, nbH, nbS, cap)
                    if steps is None or not any(c for (_, _, _, c) in steps):
                        nbad += 1
    return (ncomp, nbad, ncycsel)


if __name__ == '__main__':
    g6s = subprocess.run(['geng', '-bc', '-q', '9'],
                         capture_output=True, text=True).stdout.split()
    with Pool() as pool:
        res = list(pool.imap_unordered(scan, g6s))
    print(f"[n=9 anchor] graphs={len(g6s)} "
          f"cycle_components={sum(r[0] for r in res)} "
          f"cyclic_selections={sum(r[2] for r in res)} "
          f"A1_failures={sum(r[1] for r in res)}")
