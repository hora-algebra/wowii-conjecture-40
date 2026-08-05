"""ncdesc0520 — POST-HOC DESCRIPTIVE STATISTICS. Not a preregistered claim.

Written AFTER the frozen NC scan, purely to report how often the hypotheses of
NC and of the corollary A-I+ are actually met, so that neither is reported as a
vacuous statement.  Nothing here is graded; no decision rule depends on it.

Reported over the exhaustive universe gen_exhaustive(3,5), cyclic systems only:

  clean_q        number of q in Q with deg_U(q) <= 1        (NC's hypothesis)
  dirty_q        number of q in Q with deg_U(q) >= 2
  chords_at_dirty  chords (s in P adjacent to q, s not in cyc(q)) at dirty q
  AIplus_hyp     systems admitting a clean q0 whose two cycle vertices have no
                 H-neighbour outside Q, with every other s in P having at most
                 one H-neighbour outside Q
  AIplus_ok      of those, how many satisfy the conclusion of the counting step
                 (every s in P has degree <= 1 in G[H u P] - (Q\\{q0}))
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine0520 as E

stat = Counter()
first_aiplus = []

for (S, H, nbH, cap) in E.gen_exhaustive(3, 5):
    res = E.analyse(S, H, nbH, cap)
    if res is None:
        continue
    stat['cyclic_systems'] += 1
    nbS = res['nbS']
    for order in res['cycles']:
        P, Q, A, B, U, ends = E.cycle_data(res, order)
        Pset, Uset, Qset = set(P), set(U), set(Q)
        L = len(order)
        cyc = {}
        for i, v in enumerate(order):
            if v[0] == 'H':
                cyc[v[1]] = {order[(i - 1) % L][1], order[(i + 1) % L][1]}
        clean = [q for q in Q if len(nbS[q] & U) <= 1]
        dirty = [q for q in Q if len(nbS[q] & U) >= 2]
        stat['clean_q'] += len(clean)
        stat['dirty_q'] += len(dirty)
        for q in dirty:
            stat['chords_at_dirty'] += len((nbS[q] & Pset) - cyc[q])
        ext = {s: (set(nbH[s]) - Qset) for s in P}
        hit = False
        for q0 in clean:
            if all(not ext[s] for s in cyc[q0]) and \
               all(len(ext[s]) <= 1 for s in P if s not in cyc[q0]):
                hit = True
                D = Qset - {q0}
                degs = {s: len(set(nbH[s]) - D) for s in P}
                if all(d <= 1 for d in degs.values()):
                    stat['AIplus_ok'] += 1
                else:
                    stat['AIplus_BROKEN'] += 1
                    if len(first_aiplus) < 3:
                        first_aiplus.append((S, {s: sorted(nbH[s]) for s in S},
                                             dict(cap), q0, degs))
                break
        if hit:
            stat['AIplus_hyp'] += 1

print("POST-HOC DESCRIPTIVE (exhaustive 3 5, cyclic systems only)")
for k in ('cyclic_systems', 'clean_q', 'dirty_q', 'chords_at_dirty',
          'AIplus_hyp', 'AIplus_ok', 'AIplus_BROKEN'):
    print(f"  {k} = {stat[k]}")
for f in first_aiplus:
    print("  AIplus_BROKEN example:", f)
