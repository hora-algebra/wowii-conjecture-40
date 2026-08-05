r"""VERIFY-3 P2: tail rescan of the six capped 4d7a n=12 shards.

Grades the 44 cap-omitted (1,0) hard-state records (and the 26 omitted
(2,1) records) with the fresh engine of lemmab_verify3.py. For each
affected shard, scans every graph of the shard from the boundary graph
(the one containing the shard's 50th = last retained witness, inclusive)
to the shard end: every minimum FVS with tau>=2, every H-edge e, every
cyclic feasible selection, every A1-bad selected cycle.

Per A1-bad state record the grades:
  profile (ncyc | a1_good_count)
  TSLIDE   some bad minimizing path of the bad cycle admits a repairing
           terminal slide (B-TERMINAL-SLIDE mechanism)
  S1ALL    every bad minimizing step's successor J0 has a length-one CES
           minimizing step (SUCCESSOR-ONE-ALL restricted to this state)
  HARD1    (hard states only) some bad minimizing step has
           c(J0) <= c(J) and J0 admits a length-one CES step
  SD2STEP  some bad minimizing step has c(J0) <= c(J) and J0 admits a
           CES minimizing step (any length)
Reconciliation: found records per shard must equal missing + overlap,
where overlap = retained records lying in the scanned range.
"""
import json
import subprocess
import sys
from itertools import combinations
from multiprocessing import Pool

sys.path.insert(0, 'verify3')
from graph_fcore_verify3 import decode_g6, is_forest, min_fvs_size, all_min_fvs
from lemmab_verify3 import (instance_selections, sel_cycles, residual_paths,
                            toggle, is_ces, terminal_slides)

SCRATCH = ('/private/tmp/claude-501/-Users-christineozols-conj40v2-conj40-verify3/'
           '5ee4e383-4869-47ec-ae7d-a1fd6f2998bc/scratchpad')
SHARDS = {4: 10, 11: 8, 13: 4, 14: 4, 16: 12, 25: 6}


def quick_cycle(J, C, sels, nbH, nbS, cap):
    """(d0, minimizing steps [(a,p,J0,ces)]) with iterative deepening."""
    avoid = [a for a in sorted(C) if any(a not in J2 for J2 in sels)]
    if not avoid:
        return None, None
    for L in (1, 3, 5, 7):
        steps = []
        for a in avoid:
            paths = residual_paths(J, a, nbH, nbS, cap, L)
            for p in paths.get(L, []):
                J0 = toggle(J, a, p)
                steps.append((a, p, J0, is_ces(J, J0, C)))
        if steps:
            return L, steps
    return None, None


def one_ces_exists(J0, sels, nbH, nbS, cap):
    """Does J0 admit a length-one CES minimizing step?"""
    for Z in sel_cycles(J0):
        avoid = [a for a in sorted(Z) if any(a not in J2 for J2 in sels)]
        for a in avoid:
            paths = residual_paths(J0, a, nbH, nbS, cap, 1)
            for p in paths.get(1, []):
                if is_ces(J0, toggle(J0, a, p), Z):
                    return True
    return False


def any_ces_exists(J0, sels, nbH, nbS, cap):
    for Z in sel_cycles(J0):
        d0, steps = quick_cycle(J0, Z, sels, nbH, nbS, cap)
        if steps and any(c for (_, _, _, c) in steps):
            return True
    return False


def scan_graph(args):
    gi, g6 = args
    n, adj = decode_g6(g6)
    tau = min_fvs_size(n, adj)
    recs = []
    if tau < 2:
        return recs
    for S in all_min_fvs(n, adj, tau):
        rest = sorted(set(range(n)) - S)
        nbH = {s: frozenset(w for w in adj[s] if w not in S) for s in S}
        nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in rest}
        Hedges = [(a, b) for (a, b) in combinations(rest, 2) if b in adj[a]]
        for e in Hedges:
            cap = {h: 2 for h in rest}
            cap[e[0]] = cap[e[1]] = 1
            Sl, sels = instance_selections(S, nbH, cap)
            for J in sels:
                cycles = sel_cycles(J)
                if not cycles:
                    continue
                info = []
                for C in cycles:
                    d0, steps = quick_cycle(J, C, sels, nbH, nbS, cap)
                    if steps is None:
                        info.append((C, None, None, None))
                        continue
                    good = any(c for (_, _, _, c) in steps)
                    info.append((C, d0, steps, good))
                ngood = sum(1 for (_, _, _, g) in info if g)
                nbad = sum(1 for (_, _, _, g) in info if g is False)
                if nbad == 0:
                    continue
                # A1-bad selection record
                for (C, d0, steps, good) in info:
                    if good is not False:
                        continue
                    badsteps = [(a, p, J0) for (a, p, J0, c) in steps if not c]
                    tsl = False
                    s1all = True
                    hard1 = False
                    sd2 = False
                    for (a, p, J0) in badsteps:
                        if not tsl:
                            sl = terminal_slides(J, C, a, p, nbH, nbS, cap)
                            tsl = any(c2 for (_, _, _, c2) in sl)
                        one = one_ces_exists(J0, sels, nbH, nbS, cap)
                        s1all &= one
                        nondecr = len(sel_cycles(J0)) <= len(cycles)
                        if nondecr and one:
                            hard1 = True
                        if nondecr and not sd2:
                            sd2 = any_ces_exists(J0, sels, nbH, nbS, cap)
                    recs.append({
                        'gi': gi, 'g6': g6, 'S': sorted(S), 'e': list(e),
                        'J': sorted(map(list, J)),
                        'cycle': sorted({x for ed in C for x in ed}),
                        'ncyc': len(cycles), 'a1_good': ngood, 'd0': d0,
                        'nbad': len(badsteps), 'TSLIDE': tsl,
                        'S1ALL': s1all, 'HARD1': hard1, 'SD2STEP': sd2,
                    })
    return recs


def main():
    g6s = open(f'{SCRATCH}/n12.g6').read().split()
    idx = {g: i for i, g in enumerate(g6s)}
    summary = {}
    for sh in sorted(SHARDS):
        out = subprocess.run(['git', 'show',
                              f'5cb5bb9:work/sd/sd-v2-n12-{sh}of32.txt'],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
        retained = d['witnesses']['A1-BAD-SELECTION']
        bi = idx[retained[-1]['g6']]
        tail = [(i, g6s[i]) for i in range(bi, len(g6s)) if i % 32 == sh]
        with Pool() as pool:
            found = [r for rs in pool.imap_unordered(scan_graph, tail)
                     for r in rs]
        # overlap: retained records whose graph lies in the scanned range
        overlap = [w for w in retained if idx[w['g6']] >= bi]
        prof10 = [r for r in found if r['ncyc'] == 1 and r['a1_good'] == 0]
        prof21 = [r for r in found if r['ncyc'] == 2 and r['a1_good'] == 1]
        other = [r for r in found if r not in prof10 and r not in prof21]
        newr = len(found) - len(overlap)
        summary[sh] = (len(found), len(overlap), newr)
        print(f"[shard {sh}] tail_graphs={len(tail)} found={len(found)} "
              f"overlap_retained={len(overlap)} new={newr} "
              f"(expect missing={SHARDS[sh]}+{'(2,1)miss' if sh in (11,14) else '0'}) "
              f"profiles: (1,0)={len(prof10)} (2,1)={len(prof21)} "
              f"other={len(other)}", flush=True)
        grades = {}
        for r in found:
            key = (r['ncyc'], r['a1_good'])
            g = grades.setdefault(key, {'n': 0, 'TSLIDE': 0, 'S1ALL': 0,
                                        'HARD1': 0, 'SD2STEP': 0, 'd0s': set()})
            g['n'] += 1
            g['d0s'].add(r['d0'])
            for k in ('TSLIDE', 'S1ALL', 'HARD1', 'SD2STEP'):
                g[k] += bool(r[k])
        for key, g in sorted(grades.items()):
            print(f"    profile {key}: n={g['n']} d0s={sorted(g['d0s'])} "
                  f"TSLIDE={g['TSLIDE']}/{g['n']} S1ALL={g['S1ALL']}/{g['n']} "
                  f"HARD1={g['HARD1']}/{g['n']} SD2STEP={g['SD2STEP']}/{g['n']}",
                  flush=True)
        with open(f'verify3/tail-shard-{sh}.json', 'w') as fp:
            json.dump(found, fp, indent=1)
    print("[TAIL SUMMARY]", summary)


if __name__ == '__main__':
    main()
