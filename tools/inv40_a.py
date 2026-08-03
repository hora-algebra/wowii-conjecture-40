"""Engine A for Conjecture 40 — independent implementations (networkx +
brute force). Bipartite: descending subset scan with nx.is_bipartite.
Path cover: enumerate vertex-set partitions; a block is valid iff the graph
restricted to it (edges of G inside the block) has a Hamiltonian path —
the direct reading of the Lean IsPathCover. Exact; small n only."""
from itertools import combinations, permutations

import networkx as nx


def bipartite_a(G):
    nodes = list(G.nodes())
    n = len(nodes)
    for size in range(n, 0, -1):
        for sub in combinations(nodes, size):
            H = G.subgraph(sub)
            if H.number_of_edges() == 0 or nx.is_bipartite(H):
                return size
    return 0


def _block_traceable(G, block):
    """Does G restricted to `block` admit a Hamiltonian path? Brute force."""
    bl = list(block)
    if len(bl) == 1:
        return True
    for perm in permutations(bl):
        if all(G.has_edge(perm[i], perm[i + 1]) for i in range(len(perm) - 1)):
            return True
    return False


def _partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in _partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [part[i] + [first]] + part[i + 1:]
        yield part + [[first]]


def pathcover_a(G):
    nodes = list(G.nodes())
    best = len(nodes)
    for part in _partitions(nodes):
        if len(part) >= best:
            continue
        if all(_block_traceable(G, b) for b in part):
            best = len(part)
    return best


def quad_from_g6(line):
    G = nx.from_graph6_bytes(line.strip().encode())
    import sys
    sys.path.insert(0, ".")
    import inv_a
    return len(G), inv_a.forest_a(G), bipartite_a(G), pathcover_a(G)
