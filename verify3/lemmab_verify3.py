r"""VERIFY-3 fresh Lemma-B-layer engine (P2, codex SAFE-EXISTS branch).

Written from STATEMENTS only: proofs/FROZEN-BPLUS2.md (CES, d0, length
convention, terminal slide), PROOFS.md C4/E (residual paths), and the codex
branch's PREREG-SAFE-EXISTS.md claim statements. No code was read from
work/9d2b/*.py, work/sd/sd_scan*.py (except its two sharding lines:
geng -bc -q index % nshards), b_hslide.py, or any prior checker.

Model: connected bipartite G, min FVS S, H=G-S forest, fixed H-edge e,
caps c=2 except c=1 on e's endpoints; feasible selection J (2 incidences
per s in S, loads <= caps). Selected cycle = cyclic component of J.
Residual digraph for released selected incidence a=(s,h): arcs S->H on
unselected incidences EXCEPT a (deleted), arcs H->S on selected
incidences of J-a. A residual augmenting path: starts at s, alternates
add/remove arcs, vertex-simple, ends after an add arc at an H-terminal t
with load_{J-a}(t) < c(t). Length = number of arcs (odd).
Toggle: J0 = J - a - removed + added (feasible by construction).
CES for target C: C is not a cycle of J0 AND every cycle of J0 is a
cycle of J (cycle identity = its edge set).
A1-good cycle C: some released avoidable a of C admits a minimizing
(length d0(C)) path whose toggle is CES. d0(C) = min path length over
avoidable released a of C. Avoidable = omitted by some feasible
selection of the instance.
Terminal slide (FROZEN-BPLUS2): bad minimizing Q0 ending at t; pick
(t,u) with (u,t) in J0, then (u,t') unselected in J0, t' != a-partners,
Q+ simple (u fresh, t' fresh or the freed h), toggle feasible
(load check at t'), J+ = J0 - (u,t) + (u,t'); slide repairs if J+ is
CES for C. h-slide: the t' = freed h special case.
"""
import subprocess
import sys
from itertools import combinations

sys.path.insert(0, 'verify3')
from graph_fcore_verify3 import decode_g6, is_forest, min_fvs_size, all_min_fvs


def instance_selections(S, nbH, cap):
    Sl = sorted(S)
    per = []
    for s in Sl:
        opts = list(combinations(sorted(nbH[s]), 2))
        if not opts:
            return Sl, []
        per.append(opts)
    sols = []
    def rec(i, load, acc):
        if i == len(per):
            sols.append(frozenset(acc))
            return
        for (a, b) in per[i]:
            if load.get(a, 0) < cap[a] and load.get(b, 0) < cap[b]:
                load[a] = load.get(a, 0) + 1
                load[b] = load.get(b, 0) + 1
                acc.append((Sl[i], a)); acc.append((Sl[i], b))
                rec(i + 1, load, acc)
                acc.pop(); acc.pop()
                load[a] -= 1; load[b] -= 1
    rec(0, {}, [])
    return Sl, sols


def sel_cycles(J):
    """Cycle components of a selection, as frozensets of (s,h) edges."""
    adj = {}
    for (s, h) in J:
        adj.setdefault(('S', s), []).append(('H', h))
        adj.setdefault(('H', h), []).append(('S', s))
    seen, out = set(), []
    for v in adj:
        if v in seen:
            continue
        comp, stack = set(), [v]
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(w for w in adj[u] if w not in comp)
        seen |= comp
        ne = sum(len(adj[u]) for u in comp) // 2
        if ne == len(comp):
            out.append(frozenset((s, h) for (s, h) in J
                                 if ('S', s) in comp and ('H', h) in comp))
    return out


def residual_paths(J, a, nbH, nbS, cap, maxlen):
    """All vertex-simple residual augmenting paths for released a=(s,h),
    grouped by length. Returns dict length -> list of paths; each path is
    (added_tuple, removed_tuple) of incidence edges in order."""
    s0, h0 = a
    Jm = J - {a}
    load = {}
    for (s, h) in Jm:
        load[h] = load.get(h, 0) + 1
    out = {}

    def dfs(cur, visited, added, removed, length):
        if length >= maxlen:
            return
        # cur is an S-vertex; take an add arc
        for h in sorted(nbH[cur]):
            if (cur, h) == a or (cur, h) in Jm or ('H', h) in visited:
                continue
            # terminal?
            if load.get(h, 0) < cap[h]:
                out.setdefault(length + 1, []).append(
                    (tuple(added + [(cur, h)]), tuple(removed)))
            # continue through h via a remove arc
            if length + 2 < maxlen + 1:
                for s2 in sorted(nbS[h]):
                    if (s2, h) in Jm and ('S', s2) not in visited:
                        dfs(s2,
                            visited | {('H', h), ('S', s2)},
                            added + [(cur, h)],
                            removed + [(s2, h)],
                            length + 2)

    dfs(s0, {('S', s0)}, [], [], 0)
    return out


def toggle(J, a, path):
    added, removed = path
    return (J - {a} - set(removed)) | set(added)


def is_ces(J, J0, C):
    old = set(sel_cycles(J))
    new = set(sel_cycles(J0))
    return (C not in new) and new.issubset(old)


def analyze_cycle(J, C, sels, nbH, nbS, cap, capdepth=7):
    """d0, minimizing steps [(a, path, J0, ces)], first generic CES length."""
    avoid = [a for a in sorted(C) if any(a not in J2 for J2 in sels)]
    if not avoid:
        return None                       # no avoidable edge (Lemma A viol.)
    # find d0
    best = None
    per_a = {}
    for a in avoid:
        paths = residual_paths(J, a, nbH, nbS, cap, capdepth)
        per_a[a] = paths
        for L in paths:
            if best is None or L < best:
                best = L
    if best is None:
        return None
    steps = []
    for a in avoid:
        for p in per_a[a].get(best, []):
            J0 = toggle(J, a, p)
            steps.append((a, p, J0, is_ces(J, J0, C)))
    # generic first CES length
    first_ces = None
    for L in sorted(set(k for paths in per_a.values() for k in paths)):
        for a in avoid:
            for p in per_a[a].get(L, []):
                if is_ces(J, toggle(J, a, p), C):
                    first_ces = L
                    break
            if first_ces:
                break
        if first_ces:
            break
    return {'d0': best, 'steps': steps, 'first_ces': first_ces,
            'avoid': avoid, 'per_a': per_a}


def terminal_slides(J, C, a, path, nbH, nbS, cap):
    """All valid terminal slides of the bad minimizing path; returns list of
    (u, t2, J+, ces_flag)."""
    J0 = toggle(J, a, path)
    added, removed = path
    t = added[-1][1]
    pathverts = {('S', s) for (s, h) in added} | {('H', h) for (s, h) in added}
    out = []
    load0 = {}
    for (s, h) in J0:
        load0[h] = load0.get(h, 0) + 1
    for u in sorted(nbS[t]):
        if (u, t) not in J0:
            continue
        if ('S', u) in pathverts:          # Q+ simple: u fresh
            continue
        for t2 in sorted(nbH[u]):
            if (u, t2) in J0 or t2 == t:
                continue
            if ('H', t2) in pathverts and t2 != a[1]:
                continue                   # t' fresh or the freed h
            if load0.get(t2, 0) >= cap[t2]:
                continue                   # residual capacity at t'
            Jp = (J0 - {(u, t)}) | {(u, t2)}
            out.append((u, t2, Jp, is_ces(J, Jp, C)))
    return out


def grade_state(g6, S, e, J, capdepth=7, want_full=True):
    """Full grade of one (G,S,e,J) state. Returns dict."""
    n, adj = decode_g6(g6)
    S = frozenset(S)
    rest = sorted(set(range(n)) - S)
    nbH = {s: frozenset(w for w in adj[s] if w not in S) for s in S}
    nbS = {h: frozenset(s for s in S if h in nbH[s]) for h in rest}
    cap = {h: 2 for h in rest}
    cap[e[0]] = cap[e[1]] = 1
    Sl, sels = instance_selections(S, nbH, cap)
    J = frozenset((a, b) if a in S else (b, a) for (a, b) in J)
    res = {'feasible': J in set(sels), 'nsels': len(sels)}
    cycles = sel_cycles(J)
    res['ncyc'] = len(cycles)
    per_cycle = []
    for C in cycles:
        r = analyze_cycle(J, C, sels, nbH, nbS, cap, capdepth)
        a1good = any(ces for (_, _, _, ces) in r['steps']) if r else None
        per_cycle.append((C, r, a1good))
    res['a1_good_count'] = sum(1 for (_, _, g) in per_cycle if g)
    res['cycles'] = per_cycle
    if not want_full:
        return res
    # successor + slide analysis of every A1-bad cycle
    bad_info = []
    for (C, r, a1good) in per_cycle:
        if r is None or a1good:
            continue
        entry = {'d0': r['d0'], 'first_ces': r['first_ces'],
                 'nbadsteps': len(r['steps']),
                 'tslides': 0, 'hslides': 0, 'succ': []}
        for (a, p, J0, ces) in r['steps']:
            assert not ces
            sl = terminal_slides(J, C, a, p, nbH, nbS, cap)
            entry['tslides'] += sum(1 for (_, _, _, c2) in sl if c2)
            entry['hslides'] += sum(1 for (u, t2, _, c2) in sl
                                    if c2 and t2 == a[1])
            # successor state J0
            c0 = sel_cycles(J0)
            sd0 = None
            succ_ces = False
            for Z in c0:
                rz = analyze_cycle(J0, Z, sels, nbH, nbS, cap, capdepth)
                if rz is None:
                    continue
                if sd0 is None or rz['d0'] < sd0:
                    sd0 = rz['d0']
                if any(cz for (_, _, _, cz) in rz['steps']):
                    succ_ces = True
            entry['succ'].append({'ncyc': len(c0), 'd0': sd0,
                                  'min_ces': succ_ces,
                                  'nondecr': len(c0) <= len(cycles)})
        bad_info.append(entry)
    res['bad'] = bad_info
    return res
