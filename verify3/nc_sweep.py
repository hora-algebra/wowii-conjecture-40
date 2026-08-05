r"""VERIFY-3 extended sweep: full forced-structure universe |S|+|H| <= 10.

Universe convention = work/carrier.py's exhaustive generator, extended to
every (k=|S|, p=|H|) with k>=2, p>=3, k+p<=10: S-neighbourhoods of size
2..4, every H-vertex covered, capacities all 2 or one c=1 pair {a,b}.

Optimization (validated against the published (3,5) anchors before use):
feasible selections are enumerated ONCE per incidence structure under
all-capacity-2, then each c1 pair filters that list (a selection feasible
under caps<=2 with a c1 pair is exactly an all-2 selection whose load at
both c1 vertices is <=1). Predicates are imported from nc_verify3.
"""
import sys
from itertools import combinations, product
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, 'verify3')
from nc_verify3 import feasible, forced_core, core_cycles, check_system


def hall_feasible(S, combo, cap):
    """Generalized Hall criterion (C5): rho(X) >= 2|X| for all X."""
    from itertools import chain
    k = len(combo)
    for mask in range(1, 1 << k):
        X = [combo[i] for i in range(k) if mask >> i & 1]
        nx = bin(mask).count('1')
        deg = {}
        for nb in X:
            for h in nb:
                deg[h] = deg.get(h, 0) + 1
        rho = sum(min(cap[h], d) for h, d in deg.items())
        if rho < 2 * nx:
            return False
    return True


def block(args):
    from itertools import combinations_with_replacement
    k, p, lo, hi = args[:4]
    cwr = len(args) > 4 and args[4]
    H = list(range(p))
    opts = [frozenset(c) for r in (2, 3, 4) for c in combinations(H, r) if r <= p]
    S = [f"s{i}" for i in range(k)]
    cap2 = {h: 2 for h in H}
    c1pairs = [(a, b) for a in H for b in H if a < b]
    counters = Counter()
    certs = []
    nsys = 0
    idx = -1
    gen = (combinations_with_replacement(opts, k) if cwr
           else product(opts, repeat=k))
    for combo in gen:
        idx += 1
        if idx < lo or idx >= hi:
            continue
        if len(frozenset().union(*combo)) < p:
            continue
        nbH = dict(zip(S, combo))
        if not hall_feasible(S, combo, cap2):
            for c1 in [()] + c1pairs:
                nsys += 1              # counted; infeasible => no cyclic core
            continue
        sels2 = feasible(S, nbH, cap2)
        for c1 in [()] + c1pairs:
            nsys += 1
            if c1:
                a, b = c1
                cap = {h: (1 if h in c1 else 2) for h in H}
                sels = [J for J in sels2
                        if sum(1 for (s, h) in J if h == a) <= 1
                        and sum(1 for (s, h) in J if h == b) <= 1]
            else:
                cap = cap2
                sels = sels2
            if not sels:
                continue
            fc = forced_core(sels)
            if not core_cycles(fc):
                continue
            # full predicate run (recomputes internally; rare path)
            check_system(S, H, nbH, cap, counters, certs,
                         f"({k},{p})#{idx}c1={c1}")
    return (k, p, nsys, counters, certs)


def main(pairs):
    from math import comb
    jobs = []
    NCHUNK = 64
    for spec in pairs:
        k, p = spec[0], spec[1]
        cwr = spec[-1] == 'cwr'
        nums = [x for x in spec[2:] if x != 'cwr']
        opts_n = sum(1 for r in (2, 3, 4) for _ in combinations(range(p), r))
        total = comb(opts_n + k - 1, k) if cwr else opts_n ** k
        lo0, hi0 = (nums[0], nums[1]) if len(nums) == 2 else (0, total)
        step = max(1, (hi0 - lo0) // NCHUNK + 1)
        for lo in range(lo0, hi0, step):
            jobs.append((k, p, lo, min(lo + step, hi0), cwr))
    jobs.sort(key=lambda j: -(j[3] - j[2]))
    grand = Counter()
    per = {}
    ncert = 0
    with Pool() as pool:
        for (k, p, nsys, counters, certs) in pool.imap_unordered(block, jobs):
            key = (k, p)
            if key not in per:
                per[key] = [0, Counter()]
            per[key][0] += nsys
            per[key][1] += counters
            grand += counters
            grand['systems'] += nsys
            for c in certs:
                ncert += 1
                print("FAIL-CERT", c, flush=True)
    for (k, p) in sorted(per):
        n, c = per[(k, p)]
        print(f"  ({k},{p}) systems={n} cyclic={c['cyclic']} "
              f"NC={c['NC_fail']} NCM={c['NCM_fail']} CPR={c['CPR_fail']} "
              f"PT={c['PT_fail']} AIPhyp={c['aiplus_hyp']} AIP={c['AIP_fail']} "
              f"ctrl={c['NC-ALL']}/{c['CHORD-ALL']}/{c['PDIS']}")
    print(f"[SWEEP k+p<=10] systems={grand['systems']} cyclic={grand['cyclic']} "
          f"NC_fail={grand['NC_fail']} NCM_fail={grand['NCM_fail']} "
          f"CPR_fail={grand['CPR_fail']} PT_fail={grand['PT_fail']} "
          f"AIP_hyp={grand['aiplus_hyp']} AIP_fail={grand['AIP_fail']}")
    print(f"    controls: NC-ALL={grand['NC-ALL']} "
          f"CHORD-ALL={grand['CHORD-ALL']} PDIS={grand['PDIS']}")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'anchor':
        # validation: (2..3, 3..5) must reproduce 115774/798/18
        pairs = [(k, p) for k in (2, 3) for p in (3, 4, 5)]
        grand = Counter()
        for (k, p) in pairs:
            opts_n = sum(1 for r in (2, 3, 4) for _ in combinations(range(p), r))
            (_, _, nsys, counters, certs) = block((k, p, 0, opts_n ** k))
            grand += counters
            grand['systems'] += nsys
            for c in certs:
                print("FAIL-CERT", c)
        print(f"[ANCHOR] systems={grand['systems']} cyclic={grand['cyclic']} "
              f"NC={grand['NC_fail']} NCM={grand['NCM_fail']} "
              f"CPR={grand['CPR_fail']} PT={grand['PT_fail']} "
              f"AIPhyp={grand['aiplus_hyp']} "
              f"ctrl={grand['NC-ALL']}/{grand['CHORD-ALL']}/{grand['PDIS']}")
    else:
        # args: pairs as k,p[,lo,hi][,cwr] tokens, e.g.  3,7 4,6,cwr
        pairs = [tuple(int(x) if x.isdigit() else x for x in a.split(','))
                 for a in sys.argv[1:]]
        if not pairs:
            pairs = [(k, p) for k in range(2, 8) for p in range(3, 9)
                     if k + p <= 10]
        main(pairs)
