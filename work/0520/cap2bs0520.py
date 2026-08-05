"""cap2bs0520 — prospective checker for CAP2-BS, the parked capacity-2
punctured-carrier inequality.  See PREREG-CAP2BS.md.

CLAIM (CAP2-BS).  Let a Lemma-A-degree instance have a forced-core cycle F with
S-side P, let s in P have B_s != empty, and suppose EVERY H-neighbour h of s
outside its two forced ends satisfies c(h) = 2.  Then

        tau(G[H u B_s]) <= |B_s| - 1.

proofs/PROOFS.md section D records the general (capacity-mixed) form as FALSE
(O-64) and this capacity-2-only form as "neither proved nor refuted".

NEGATIVE CONTROL (known FALSE; MUST fire, else the harness is dead code)
  NOGUARD   the same inequality with the c(h)=2 hypothesis DROPPED.
            O-64 refutes it: there B_s={u} is Hall-tight with tau = 1 = |B_s|.

Structure: stage 1 takes the abstract cyclic systems from the frozen
carrier.py generator; stage 2 enumerates every bipartite-legal H-forest
completion with `steiner` extra incidence-free H-vertices, exactly as
work/larealize.py does (its colourings/forests_over/tau_of are reused, and the
capacity-1 pair is realised as a required H-edge; an all-capacity-2 system gets
its fixed edge from a separate incidence-free K_2).  The claim is tested on
EVERY completion, not only on minimum-FVS ones: CAP2-BS does not assume
hereditary tightness.
"""
import os
import sys
from collections import Counter
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import carrier as C
import larealize as LA
import engine0520 as E

STAT = Counter()
FAILS = []
CAPCOMP = 20000       # max completions examined per (system, s); reported


def carriers_for_cycle(S, H, nbH, cap, order):
    nbS = {h: frozenset(x for x in S if h in nbH[x]) for h in H}
    tights, _ = E.tight_sets(S, nbS, cap)
    P = [v[1] for v in order if v[0] == 'S']
    A = {s: E.canonical_carrier(s, tights) for s in P}
    L = len(order)
    ends = {}
    for i, v in enumerate(order):
        if v[0] == 'S':
            ends[v[1]] = {order[(i - 1) % L][1], order[(i + 1) % L][1]}
    return P, A, ends


def completions(S, H, nbH, cap, steiner):
    """Every bipartite-legal H-forest completion; yields (Hc, hedges)."""
    c1 = sorted([h for h in H if cap[h] == 1])
    Hc = list(H) + [f"z{i}" for i in range(steiner)]
    for col in LA.colourings(S, H, nbH):
        for extra in range(2 ** steiner):
            colf = dict(col)
            for i in range(steiner):
                colf[f"z{i}"] = (extra >> i) & 1
            allowed = [(u, v) for u, v in combinations(Hc, 2)
                       if colf[u] != colf[v]]
            if len(c1) == 2:
                must = [(c1[0], c1[1])]
                if colf[c1[0]] == colf[c1[1]]:
                    continue
            else:
                must = []
            for hed in LA.forests_over(allowed, must):
                yield Hc, hed
            if steiner == 0 and len(c1) != 2:
                break


def run(maxK, maxP, steiner, limit_systems=None):
    nsys = 0
    for (S, H, nbH, cap) in C.gen_exhaustive(maxK, maxP):
        sels = C.feasible_selections(S, nbH, cap)
        if not sels:
            continue
        forced, cycles = C.forced_and_cycles(S, sels)
        if not cycles:
            continue
        nsys += 1
        STAT['cyclic_systems'] += 1
        if limit_systems and nsys > limit_systems:
            break
        for comp in cycles:
            order = C.walk_cycle(comp, forced)
            order = [(v[0], v[1]) for v in order]
            P, A, ends = carriers_for_cycle(S, H, nbH, cap, order)
            for s in P:
                B = A[s] - {s}
                if not B:
                    continue
                others = [h for h in nbH[s] if h not in ends[s]]
                guard = all(cap[h] == 2 for h in others)
                STAT['s_with_Bs'] += 1
                if guard:
                    STAT['s_guarded'] += 1
                seen = 0
                for Hc, hed in completions(S, H, nbH, cap, steiner):
                    seen += 1
                    if seen > CAPCOMP:
                        STAT['capped'] += 1
                        break
                    verts = set(Hc) | set(B)
                    edges = [(x, h) for x in B for h in nbH[x]] + list(hed)
                    t, _ = LA.tau_of(verts, edges)
                    STAT['completions_tested'] += 1
                    if t > len(B) - 1:
                        if guard:
                            STAT['CAP2BS_FAIL'] += 1
                            if len(FAILS) < 5:
                                FAILS.append(('CAP2-BS', S,
                                              {x: sorted(nbH[x]) for x in S},
                                              dict(cap), s, sorted(B), t, hed))
                        else:
                            STAT['NOGUARD_fired'] += 1
    print(f"[cap2bs exhaustive {maxK} {maxP} steiner={steiner}] " +
          " ".join(f"{k}={v}" for k, v in sorted(STAT.items())))
    for f in FAILS:
        print("   FAIL", f)


if __name__ == "__main__":
    mk = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    mp = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    st = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    lim = int(sys.argv[4]) if len(sys.argv) > 4 else None
    run(mk, mp, st, lim)
