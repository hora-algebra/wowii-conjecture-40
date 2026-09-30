"""Replay published negative controls using the unchanged upstream oracle."""
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from eval_L1_holdout import feasible
from forced_core import norm, cyclomatic
import experiment_b as EB

results = []
for path in sorted((ROOT / 'tools/witnesses').glob('*.json')):
    data = json.loads(path.read_text())
    names = data['vertices']['S'] + data['vertices']['H']
    idx = {v: i for i, v in enumerate(names)}
    n = len(names)
    adj = [0] * n
    for a, b in data['incidence_edges_S_H'] + data['H_forest_edges']:
        a, b = idx[a], idx[b]
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    S = [idx[v] for v in data['vertices']['S']]
    x, y = map(idx.__getitem__, data['distinguished_edge'])
    selections = feasible(n, adj, S, x, y)
    assert len(selections) == data['feasible_selections']['count']
    core = set.intersection(*(set(norm(J)) for J in selections))
    assert cyclomatic(core) > 0
    tau = EB.tau(n, adj)
    assert tau < len(S), 'Negative control unexpectedly satisfies minimum-FVS premise'
    hs = data['hereditary_tightness']
    violation = hs.get('first_inclusion_minimal_violation', hs.get('first_violation'))
    subset = violation['set']
    kept = [idx[v] for v in data['vertices']['H'] + subset]
    small = [sum(1 << j for j, w in enumerate(kept) if adj[v] >> w & 1) for v in kept]
    actual = EB.tau(len(kept), small)
    assert actual == violation['tau'] < len(subset)
    results.append(dict(witness=data['id'], selections=len(selections),
        forced_edges=len(core), forced_cycle_rank=cyclomatic(core),
        tau=tau, supplied_S_size=len(S), violation=subset, violation_tau=actual))
print(json.dumps({'status': 'PASS', 'negative_controls_fired': len(results),
    'results': results}, indent=2))
