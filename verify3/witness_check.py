r"""VERIFY-3 P2: witness confirmation + controls for the Lemma-B engine.

1. [CTRL-N11] The six 4d7a n=11 A1-BAD-SELECTION witnesses (data records):
   each must grade as: target cycle A1-bad with d0=3, first generic CES at
   5 (B-PLUS-2 gap 2), and at least one repairing terminal slide (
   B-TERMINAL-SLIDE holds at n=11), with c(J0)<=c(J) two-step descent.
2. [WITNESS] The codex n=12 independent witness K??FFbw}Fw^_:
   claims: tau=5, S min FVS, J feasible, 2 cycles, other cycle A1-good,
   target {0,1,6,7}: d0=3, 12 minimizing steps all bad, 0 terminal
   slides, first generic CES 5; all 12 successors: ncyc=1, d0=3, CES
   minimizing step exists (SD-2STEP survives; SUCCESSOR-ONE falsified).
3. [MUT] mutation: inverting the destroys-C condition in the CES test on
   the witness target must turn bad steps into 'CES' (harness liveness).
"""
import json
import subprocess
import sys

sys.path.insert(0, 'verify3')
from graph_fcore_verify3 import decode_g6, min_fvs_size, is_forest
from lemmab_verify3 import (grade_state, instance_selections, sel_cycles,
                            analyze_cycle, toggle, residual_paths)


def n11_controls():
    out = subprocess.run(['git', 'show', '5cb5bb9:work/sd/sd-n11-AGGREGATE.json'],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    wits = d['witnesses']['A1-BAD-SELECTION']
    print(f"[CTRL-N11] {len(wits)} witnesses from 4d7a n=11 aggregate")
    allok = True
    for w in wits:
        r = grade_state(w['g6'], w['S'], tuple(w['e']), w['J'])
        bad = r['bad']
        ok = (r['feasible'] and len(bad) >= 1)
        for b in bad:
            ok &= (b['d0'] == 3 and b['first_ces'] == 5 and b['tslides'] > 0
                   and all(s['min_ces'] and s['nondecr'] for s in b['succ']))
        print(f"  g6={w['g6']} ncyc={r['ncyc']} a1good={r['a1_good_count']} "
              f"bad={[(b['d0'], b['first_ces'], b['tslides'], b['hslides']) for b in bad]} ok={ok}")
        allok &= ok
    print(f"[CTRL-N11] {'ALL PASS' if allok else '*** FAIL ***'}")
    return allok


def witness():
    rec = {
        'g6': 'K??FFbw}Fw^_',
        'S': [6, 7, 8, 9, 10],
        'e': (4, 11),
        'J': [[6, 0], [6, 1], [7, 0], [7, 1], [8, 2], [8, 3], [9, 2], [9, 3],
              [10, 4], [10, 5]],
    }
    n, adj = decode_g6(rec['g6'])
    tau = min_fvs_size(n, adj)
    S = set(rec['S'])
    isfvs = is_forest(n, adj, set(range(n)) - S)
    print(f"[WITNESS] n={n} tau={tau} (claim 5) S_is_FVS={isfvs} "
          f"S_is_min={isfvs and tau == len(S)}")
    r = grade_state(rec['g6'], rec['S'], rec['e'], rec['J'])
    print(f"  feasible={r['feasible']} nsels={r['nsels']} ncyc={r['ncyc']} "
          f"a1_good_count={r['a1_good_count']}")
    for (C, rr, good) in r['cycles']:
        cv = sorted({x for e2 in C for x in e2})
        print(f"  cycle {cv}: d0={rr['d0']} minimizing={len(rr['steps'])} "
              f"ces_min={sum(1 for (_,_,_,c) in rr['steps'] if c)} "
              f"first_ces={rr['first_ces']} a1good={good}")
    ok = (tau == 5 and isfvs and r['feasible'] and r['ncyc'] == 2
          and r['a1_good_count'] == 1)
    for b in r['bad']:
        print(f"  target(bad): d0={b['d0']} badsteps={b['nbadsteps']} "
              f"tslides={b['tslides']} hslides={b['hslides']} "
              f"first_ces={b['first_ces']}")
        succ_ok = all(s['ncyc'] == 1 and s['d0'] == 3 and s['min_ces']
                      and s['nondecr'] for s in b['succ'])
        print(f"  successors: {[(s['ncyc'], s['d0'], s['min_ces']) for s in b['succ']]}")
        print(f"  succ_ok(all ncyc=1,d0=3,CES-min)={succ_ok} "
              f"SUCCESSOR-ONE falsified={all(s['d0'] != 1 for s in b['succ'])}")
        ok &= (b['d0'] == 3 and b['nbadsteps'] == 12 and b['tslides'] == 0
               and b['first_ces'] == 5 and succ_ok)
    print(f"[WITNESS] {'CONFIRMED' if ok else '*** MISMATCH ***'}")
    return ok


def mutation():
    rec_g6 = 'K??FFbw}Fw^_'
    S = [6, 7, 8, 9, 10]
    e = (4, 11)
    J = frozenset([(6, 0), (6, 1), (7, 0), (7, 1), (8, 2), (8, 3), (9, 2),
                   (9, 3), (10, 4), (10, 5)])
    n, adj = decode_g6(rec_g6)
    Sf = frozenset(S)
    rest = sorted(set(range(n)) - Sf)
    nbH = {s: frozenset(w for w in adj[s] if w not in Sf) for s in S}
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in rest}
    cap = {h: 2 for h in rest}
    cap[e[0]] = cap[e[1]] = 1
    Jn = frozenset((s, h) for (s, h) in J)
    _, sels = instance_selections(Sf, nbH, cap)
    cycles = sel_cycles(Jn)
    C = [c for c in cycles if 6 in {s for (s, h) in c}][0]
    r = analyze_cycle(Jn, C, sels, nbH, nbS, cap)
    # mutated CES: drop the no-new-cycle condition entirely
    mut_ces = 0
    for (a, p, J0, ces) in r['steps']:
        newc = set(sel_cycles(J0))
        if C not in newc:                  # mutation: ignore created cycles
            mut_ces += 1
    print(f"[MUT] steps={len(r['steps'])} honest_ces="
          f"{sum(1 for (_,_,_,c) in r['steps'] if c)} "
          f"mutated_ces(no-new-cycle check removed)={mut_ces} "
          f"(must be >0 to prove the created-cycle check is load-bearing)")
    return mut_ces > 0


if __name__ == '__main__':
    ok = n11_controls()
    ok &= witness()
    ok &= mutation()
    print(f"[P2 WITNESS PHASE] {'ALL CONFIRMED' if ok else '*** PROBLEM ***'}")
