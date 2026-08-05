"""nccontrols0520 — gold test for nc0520, run BEFORE the target scan.

POSITIVE controls (must PASS NC/NCM/CPR):
  O-56, O-63, O-64 (tools/witnesses/), and ADJ-1 (work/0520/ADJ-WITNESS-vendored.json,
  sha256 2a0d62e0..., vendored from public/attempt/2026-08-05-codex-gpt-5-b17e
  at 9cd62bb9f36c6cd61d9d62d7fed77db38463c9b1).

NEGATIVE controls (ADJ-1 must FIRE both, else the harness cannot detect the
known boundary):
  NC-ALL     — ADJ-1 has q=0 with deg_U(0)=2
  CHORD-ALL  — ADJ-1 has q=0 whose S-neighbourhood contains the non-cycle
               vertex s2

Also prints, for each control, the per-q table that NC constrains.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine0520 as E
import nc0520

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


def load_json(path):
    with open(path) as f:
        j = json.load(f)
    S = [str(v) for v in j['vertices']['S']]
    H = [str(v) for v in j['vertices']['H']]
    nb = {s: set() for s in S}
    for (a, b) in j['incidence_edges_S_H']:
        nb[str(a)].add(str(b))
    nbH = {s: frozenset(v) for s, v in nb.items()}
    c1 = set(str(v) for v in j['capacities'].get('c1_vertices', []))
    cap = {h: (1 if h in c1 else 2) for h in H}
    return S, H, nbH, cap


CASES = [('O-56', os.path.join(ROOT, 'tools', 'witnesses', 'O-56.json')),
         ('O-63', os.path.join(ROOT, 'tools', 'witnesses', 'O-63.json')),
         ('O-64', os.path.join(ROOT, 'tools', 'witnesses', 'O-64.json')),
         ('ADJ-1', os.path.join(HERE, 'ADJ-WITNESS-vendored.json'))]

for name, path in CASES:
    S, H, nbH, cap = load_json(path)
    before_fail = len(nc0520.FAILS)
    before_ctl = dict(nc0520.CONTROL)
    status = nc0520.check_system(S, H, nbH, cap, tag=name)
    newfails = nc0520.FAILS[before_fail:]
    fired = {k: nc0520.CONTROL[k] - before_ctl.get(k, 0)
             for k in nc0520.CONTROL if nc0520.CONTROL[k] - before_ctl.get(k, 0)}
    print(f"===== {name}: cyclic_forced_core={status is not None} "
          f"NC/NCM/CPR={'PASS' if status == 'ok' else status} "
          f"controls_fired={fired}")
    for f in newfails:
        print("     FAIL", f[0], f[5])

    res = E.analyse(S, H, nbH, cap)
    if res is None:
        continue
    for order in res['cycles']:
        P, Q, A, B, U, ends = E.cycle_data(res, order)
        Pset, Uset = set(P), set(U)
        L = len(order)
        cyc = {}
        for i, v in enumerate(order):
            if v[0] == 'H':
                cyc[v[1]] = {order[(i - 1) % L][1], order[(i + 1) % L][1]}
        print(f"     P={sorted(P)} U={sorted(U)} P\\U={sorted(Pset-Uset)}")
        for q in Q:
            degU = len(res['nbS'][q] & U)
            extraP = sorted((res['nbS'][q] & Pset) - cyc[q])
            extraU = sorted((res['nbS'][q] & Uset) - Pset)
            print(f"       q={q}: deg_U={degU} cyc={sorted(cyc[q])} "
                  f"N_S(q)={sorted(res['nbS'][q])} extraP={extraP} "
                  f"extraU={extraU}")
