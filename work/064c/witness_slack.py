#!/usr/bin/env python3
"""
witness_slack.py -- for every preserved hard-state certificate, replay each bad
minimizing step and record WHICH slack vertex of the successor witnesses
CL-6/CL-7: the freed cycle end `h` itself, or some other slack vertex.

This distinguishes two possible mechanisms behind the empirical `d0(Z)=1`:
  (A) an S-vertex of the relocated cycle Z is adjacent to the freed vertex h;
  (B) it is adjacent to some slack vertex that was already slack in J.
"""
import json, glob, sys
import s2e_scan as B

def main(pats):
    seen = set()
    stat = dict(records=0, steps=0, onlyA=0, onlyB=0, both=0, none=0,
                invalid=0)
    for pat in pats:
        for f in glob.glob(pat):
            if 'DO-NOT' in f or 'SUPERSEDED' in f:
                continue
            try:
                d = json.load(open(f))
            except Exception:
                continue
            for r in d.get('hard_records', []):
                key = (r['g6'], tuple(r['S']), tuple(r['e']),
                       tuple(tuple(p) for p in r['sel']))
                if key in seen:
                    continue
                seen.add(key)
                stat['records'] += 1
                grade(r, stat)
    print(json.dumps(stat, indent=1))

def grade(r, stat):
    gn, adj = B.g6_decode(r['g6'])
    col = B.bipartition(gn, adj)
    Sm = 0
    for s in r['S']:
        Sm |= 1 << s
    inst = B.Inst(gn, adj, col, Sm, tuple(r['e']))
    sel = tuple(tuple(p) for p in r['sel'])
    E, degH, inc = B.sel_state(inst, sel)
    cyc = B.selected_cycles(inst, E)
    old = set(c[1] for c in cyc)
    for (vs, es) in cyc:
        best, allp = None, []
        for (s, h) in es:
            dd, ps = B.residual_paths(inst, E, degH, inc, (s, h))
            if dd is None:
                continue
            if best is None or dd < best:
                best, allp = dd, [((s, h), p) for p in ps]
            elif dd == best:
                allp += [((s, h), p) for p in ps]
        if best is None:
            stat['invalid'] += 1
            continue
        for (a, p) in allp:
            ns = B.toggle(inst, sel, a, p)
            nE, nd, ninc = B.sel_state(inst, ns)
            ncy = B.selected_cycles(inst, nE)
            nset = set(c[1] for c in ncy)
            if es not in nset and nset <= old:
                continue                      # CES step: not a bad step
            stat['steps'] += 1
            h0 = a[1]
            A = Bo = False
            for (nvs, nes) in ncy:
                for v in nvs:
                    if v not in inst.NH:
                        continue
                    for hh in inst.NH[v]:
                        if nd[hh] < inst.cap[hh]:
                            if hh == h0:
                                A = True
                            else:
                                Bo = True
            if A and Bo:
                stat['both'] += 1
            elif A:
                stat['onlyA'] += 1
            elif Bo:
                stat['onlyB'] += 1
            else:
                stat['none'] += 1

if __name__ == "__main__":
    main(sys.argv[1:])
