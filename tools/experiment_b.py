"""Experiment B: exact test of the tau-induction extension property for the
bipartite core of WOWII 40, per the incidence-model spec.

For 2-connected bipartite G with k=tau(G)>0:
  C(G) = { v : tau(G-v) = k-1 }   (critical vertices)
  ell2(G,v) = max edges of a spanning linear forest F of G with deg_F(v)=2
Property HOLDS for G iff  max_{v in C(G)} ell2(G,v) >= 2k+1.
Categories: A = holds, C = exact failure (all critical v give ell2 <= 2k),
D = unknown (timeout). Every C-failure is preserved."""
import subprocess
import sys

sys.path.insert(0, ".")
import inv_b


def induced(n, adj, drop):
    keep = [u for u in range(n) if u != drop]
    idx = {u: i for i, u in enumerate(keep)}
    a2 = [0] * len(keep)
    for u in keep:
        m = adj[u]
        while m:
            w = (m & -m).bit_length() - 1
            m &= m - 1
            if w > u and w != drop:
                a2[idx[u]] |= 1 << idx[w]
                a2[idx[w]] |= 1 << idx[u]
    return len(keep), a2


def tau(n, adj):
    return n - inv_b.forest_b(n, adj)


def _max_lf(n, adj, deg0, par0, exclude_v):
    """Max additional linear-forest edges over edges not incident to exclude_v,
    starting from degrees deg0 and union-find par0."""
    edges = []
    for u in range(n):
        if u == exclude_v:
            continue
        m = adj[u]
        while m:
            w = (m & -m).bit_length() - 1
            m &= m - 1
            if w > u and w != exclude_v:
                edges.append((u, w))
    best = [0]

    def find(x, par):
        while par[x] != x:
            x = par[x]
        return x

    def bb(i, count, deg, par):
        if count + (len(edges) - i) <= best[0]:
            return
        if i == len(edges):
            best[0] = max(best[0], count)
            return
        u, w = edges[i]
        if deg[u] < 2 and deg[w] < 2:
            ru, rw = find(u, par), find(w, par)
            if ru != rw:
                p2 = list(par)
                p2[ru] = rw
                deg[u] += 1
                deg[w] += 1
                bb(i + 1, count + 1, deg, p2)
                deg[u] -= 1
                deg[w] -= 1
        bb(i + 1, count, deg, par)

    bb(0, 0, list(deg0), list(par0))
    return best[0]


def ell(n, adj):
    return _max_lf(n, adj, [0] * n, list(range(n)), -1)


def ell2(n, adj, v):
    """Max spanning-linear-forest edges with deg(v)=2, over neighbor pairs."""
    neigh = [u for u in range(n) if (adj[v] >> u) & 1]
    best = -1
    for i in range(len(neigh)):
        for j in range(i + 1, len(neigh)):
            x, y = neigh[i], neigh[j]
            deg = [0] * n
            deg[v] = 2
            deg[x] = 1
            deg[y] = 1
            par = list(range(n))

            def find(a):
                while par[a] != a:
                    a = par[a]
                return a
            par[find(x)] = find(v)
            par[find(y)] = find(v)
            add = _max_lf(n, adj, deg, par, v)
            best = max(best, 2 + add)
    return best


def test_graph(n, adj):
    k = tau(n, adj)
    if k == 0:
        return ("BASE", k, None)
    C = []
    for v in range(n):
        m, a2 = induced(n, adj, v)
        if tau(m, a2) == k - 1:
            C.append(v)
    best_e2 = -1
    per_v = {}
    for v in C:
        e2 = ell2(n, adj, v)
        per_v[v] = e2
        best_e2 = max(best_e2, e2)
    holds = best_e2 >= 2 * k + 1
    return ("A" if holds else "C", k, dict(C=C, per_v=per_v, best_e2=best_e2,
            need=2 * k + 1, ell=ell(n, adj)))


def gold():
    # C4 = K(2,2): tau=1, need 3, ell2 should be 3 (Hamiltonian path, v internal)
    c4 = [0] * 4
    for u, w in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        c4[u] |= 1 << w
        c4[w] |= 1 << u
    cat, k, info = test_graph(4, c4)
    assert k == 1 and info["best_e2"] == 3 and cat == "A", ("C4", cat, k, info)
    for v in range(4):
        assert ell2(4, c4, v) == 3
        assert ell2(4, c4, v) <= ell(4, c4)
    # K(3,3): tau=2, need 5, ell=5
    k33 = [0] * 6
    for u in range(3):
        for w in range(3, 6):
            k33[u] |= 1 << w
            k33[w] |= 1 << u
    cat, k, info = test_graph(6, k33)
    assert k == 2 and cat == "A" and info["best_e2"] >= 5, ("K33", cat, k, info)
    print("GOLD PASS: C4 (ell2=3, A), K33 (tau=2, A, best_e2=%d), ell2<=ell OK"
          % info["best_e2"])


if __name__ == "__main__":
    gold()
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    total = failures = base = unknown = 0
    fails = []
    for n in range(4, maxn + 1):
        out = subprocess.run(["geng", "-b", "-C", "-q", str(n)],
                             capture_output=True, text=True).stdout.split()
        ncat = {"A": 0, "C": 0, "BASE": 0}
        for g6 in out:
            nn, adj = inv_b.parse_g6(g6)
            cat, k, info = test_graph(nn, adj)
            ncat[cat] = ncat.get(cat, 0) + 1
            total += 1
            if cat == "C":
                failures += 1
                fails.append((g6, k, info))
        print(f"n={n}: {len(out)} 2-conn bipartite | holds(A)={ncat['A']} "
              f"base(k=0)={ncat['BASE']} FAILURES(C)={ncat['C']}")
    print(f"\nTOTAL: {total} graphs, exact failures={failures}")
    for g6, k, info in fails[:10]:
        print(f"  FAIL {g6} k={k} need={info['need']} best_ell2={info['best_e2']} "
              f"C={info['C']} per_v={info['per_v']}")
