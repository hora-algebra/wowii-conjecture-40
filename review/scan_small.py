"""Prospective replay of candidate proof assertions; not a universal proof."""
import json
import subprocess
import sys
import time
from pathlib import Path
import lemma_checks as checks

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'tools'))
from inv_b import parse_g6

start = time.monotonic()
by_order = {}
for n in range(2, 11):
    result = subprocess.run(['geng', '-bc', '-q', str(n)], check=True,
                            capture_output=True, text=True)
    graphs = result.stdout.split()
    assert graphs, 'Generator returned an empty universe'
    for g6 in graphs:
        nn, adj = parse_g6(g6)
        assert nn == n
        colors = {0: 0}
        queue = [0]
        for v in queue:
            for w in checks.vertices(adj[v]):
                if w not in colors:
                    colors[w] = 1 - colors[v]
                    queue.append(w)
                assert colors[w] != colors[v]
        assert len(colors) == n
        left = sum(1 << v for v in colors if colors[v] == 0)
        checks.check(adj, left)
    by_order[n] = len(graphs)
    print(json.dumps({'finished_order': n, 'graphs': len(graphs),
                      'counts': checks.counts}), flush=True)
print(json.dumps({'status': 'PASS', 'by_order': by_order,
                  'counts': checks.counts, 'seconds': time.monotonic()-start}))
