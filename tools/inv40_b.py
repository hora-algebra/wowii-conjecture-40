"""Engine B for WOWII Conjecture 40: bipartite size via odd-cycle branching,
path cover number via max-linear-forest branch and bound.
Conventions match the repo's Lean:
  b(G)  = max |S| with induced subgraph on S bipartite (no odd cycles).
  p(G)  = min number of disjoint path-blocks covering all vertices, where a
          block is valid iff the graph restricted to it has a Hamiltonian
          path (Lean: block = support of an IsPath walk).
          Equivalently p = n - L, L = max edges of a spanning linear forest.
"""
import sys

sys.path.insert(0, ".")
import inv_b


def _shortest_odd_cycle(n, adj, removed):
    """Vertex set of some odd cycle in G - removed, else None. BFS 2-coloring."""
    color = {}
    for src in range(n):
        if removed >> src & 1 or src in color:
            continue
        color[src] = 0
        par = {src: -1}
        frontier = [src]
        while frontier:
            nxt = []
            for u in frontier:
                m = adj[u] & ~removed
                while m:
                    v = (m & -m).bit_length() - 1
                    m &= m - 1
                    if v not in color:
                        color[v] = color[u] ^ 1
                        par[v] = u
                        nxt.append(v)
                    elif color[v] == color[u]:
                        # odd closed walk: union of ancestor chains contains an odd cycle
                        cyc = set()
                        a, bnode = u, v
                        while a != -1:
                            cyc.add(a)
                            a = par[a]
                        while bnode != -1:
                            cyc.add(bnode)
                            bnode = par[bnode]
                        return cyc
            frontier = nxt
    return None


def bip_at_least(n, adj, k, removed=0):
    """True iff an induced bipartite subgraph of size >= k exists."""
    if n - bin(removed).count("1") < k:
        return False
    cyc = _shortest_odd_cycle(n, adj, removed)
    if cyc is None:
        return True
    if bin(removed).count("1") >= n - k:
        return False
    for v in cyc:
        if bip_at_least(n, adj, k, removed | (1 << v)):
            return True
    return False


def bipartite_b(n, adj):
    for k in range(n, 0, -1):
        if bip_at_least(n, adj, k):
            return k
    return 0


def _max_linear_forest(n, adj):
    """Max edge count of a subgraph that is a disjoint union of paths
    (all degrees <= 2, acyclic). Branch and bound over the edge list."""
    edges = []
    for u in range(n):
        m = adj[u]
        while m:
            v = (m & -m).bit_length() - 1
            m &= m - 1
            if v > u:
                edges.append((u, v))
    best = [0]
    deg = [0] * n
    parent = list(range(n))

    def find(x, par):
        while par[x] != x:
            x = par[x]
        return x

    def bb(i, count, par):
        if count + (len(edges) - i) <= best[0]:
            return
        if i == len(edges):
            if count > best[0]:
                best[0] = count
            return
        u, v = edges[i]
        # include edge if both endpoints have degree < 2 and no cycle forms
        if deg[u] < 2 and deg[v] < 2:
            ru, rv = find(u, par), find(v, par)
            if ru != rv:
                par2 = list(par)
                par2[ru] = rv
                deg[u] += 1
                deg[v] += 1
                bb(i + 1, count + 1, par2)
                deg[u] -= 1
                deg[v] -= 1
        bb(i + 1, count, par)

    bb(0, 0, parent)
    return best[0]


def pathcover_b(n, adj):
    return n - _max_linear_forest(n, adj)


def quad(g6):
    """(n, f, b, p) using the certified forest engine plus this module."""
    n, adj = inv_b.parse_g6(g6)
    f = inv_b.forest_b(n, adj)
    b = bipartite_b(n, adj)
    p = pathcover_b(n, adj)
    return n, f, b, p


def slack(g6):
    """f - ceil((p + b + 1)/2); negative = counterexample to Conjecture 40."""
    n, f, b, p = quad(g6)
    return f - (-(-(p + b + 1) // 2))
