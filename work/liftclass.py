"""Check the two ingredients of the PROVED structured class for LIFT-A.

LEMMA L1 (proved).  For a bipartite graph B on n_B vertices with c_e
edge-containing components,  f(B) >= ceil(n_B/2) + c_e,  equivalently
tau(B) <= floor(n_B/2) - c_e.
    Proof: in each component take the larger bipartition class (independent,
    size >= ceil(n_i/2)); if the component has an edge, add one vertex of the
    other class -- the induced subgraph is a star plus isolated vertices, a
    forest.  Union over components.

THEOREM L2 (proved from L1).  If some minimum OCT T of a connected nonbipartite
G satisfies p(G) <= 2*c_e(G-T) - 1, then LIFT-A holds at G with that T:
    2*tau(G-T) + |T| + 1 <= 2*floor(n_B/2) - 2c_e + o + 1 <= n + 1 - 2c_e
                         <= n - p = ell(G).
    In particular every traceable (p = 1) connected nonbipartite G is covered,
    since c_e >= 1 always (paper Lemma 5.1).
    Provenance: the engine of L1 for a connected B is DeLavina's 2004 remark
    f >= b/2 + 1 on the WOWII page; what is new here is applying it to G - T and
    to the lifting form, and the c_e refinement.

This script verifies L1 exhaustively on bipartite graphs (geng -b, all
connectivities) and measures how much of the nonbipartite universe L2 covers.

Usage: python3 liftclass.py <nmax>
"""
import subprocess
import sys
from itertools import combinations


def parse_g6(s):
    n = ord(s[0]) - 63
    bits, idx = [], 1
    need = n * (n - 1) // 2
    while len(bits) < need:
        v = ord(s[idx]) - 63
        idx += 1
        bits += [(v >> k) & 1 for k in range(5, -1, -1)]
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return n, adj


def is_forest(n, adj, S):
    par = list(range(n))

    def f(v):
        while par[v] != v:
            par[v] = par[par[v]]
            v = par[v]
        return v
    for j in range(n):
        if not (S >> j & 1):
            continue
        m = adj[j] & S & ((1 << j) - 1)
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            a, b = f(i), f(j)
            if a == b:
                return False
            par[a] = b
    return True


def is_bip(n, adj, S):
    col = {}
    for r in range(n):
        if not (S >> r & 1) or r in col:
            continue
        col[r] = 0
        st = [r]
        while st:
            u = st.pop()
            m = adj[u] & S
            while m:
                v = (m & -m).bit_length() - 1
                m &= m - 1
                if v not in col:
                    col[v] = col[u] ^ 1
                    st.append(v)
                elif col[v] == col[u]:
                    return False
    return True


def max_forest(n, adj, univ):
    best = 0
    S = univ
    while True:
        pc = bin(S).count("1")
        if pc > best and is_forest(n, adj, S):
            best = pc
        if S == 0:
            break
        S = (S - 1) & univ
    return best


def max_bip(n, adj, univ):
    best = 0
    S = univ
    while True:
        pc = bin(S).count("1")
        if pc > best and is_bip(n, adj, S):
            best = pc
        if S == 0:
            break
        S = (S - 1) & univ
    return best


def comps_with_edge(n, adj, univ):
    seen, ce = 0, 0
    for r in range(n):
        if not (univ >> r & 1) or (seen >> r & 1):
            continue
        st, comp = [r], 0
        seen |= 1 << r
        while st:
            u = st.pop()
            comp |= 1 << u
            m = adj[u] & univ & ~seen
            while m:
                v = (m & -m).bit_length() - 1
                m &= m - 1
                seen |= 1 << v
                st.append(v)
        has_edge = any((adj[v] & comp) for v in range(n) if comp >> v & 1)
        if has_edge:
            ce += 1
    return ce


def path_cover(n, adj, univ):
    """min path cover of the induced subgraph on univ (exponential DP)."""
    hamv = [0] * (1 << n)          # bitmask of valid path endpoints
    pathset = [False] * (1 << n)
    for mask in range(1 << n):
        if mask & ~univ:
            continue
        if bin(mask).count("1") == 1:
            hamv[mask] = mask
            pathset[mask] = True
            continue
        h = 0
        m2 = mask
        while m2:
            v = (m2 & -m2).bit_length() - 1
            m2 &= m2 - 1
            if hamv[mask ^ (1 << v)] & adj[v]:
                h |= 1 << v
        hamv[mask] = h
        pathset[mask] = h != 0
    dp = [99] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        if mask & ~univ:
            continue
        best = 99
        sub = mask
        while sub:
            if pathset[sub] and dp[mask ^ sub] + 1 < best:
                best = dp[mask ^ sub] + 1
            sub = (sub - 1) & mask
        dp[mask] = best
    return dp[univ]


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    # --- L1 on all bipartite graphs ---
    bad = tot = tight = 0
    for n in range(2, nmax + 1):
        gs = subprocess.run(["geng", "-b", "-q", str(n)],
                            capture_output=True, text=True).stdout.split()
        for g6 in gs:
            nn, adj = parse_g6(g6)
            full = (1 << nn) - 1
            f = max_forest(nn, adj, full)
            ce = comps_with_edge(nn, adj, full)
            bound = -(-nn // 2) + ce
            tot += 1
            if f < bound:
                bad += 1
                print("L1 VIOLATION", g6, "f=", f, "bound=", bound)
            elif f == bound:
                tight += 1
    print(f"L1 (f(B) >= ceil(n/2) + c_e) on all bipartite graphs n<={nmax}: "
          f"{tot} graphs, {bad} violations, {tight} tight")

    # --- L2 coverage on connected nonbipartite graphs ---
    cov = tot2 = 0
    hist = {}
    for n in range(3, nmax + 1):
        gs = subprocess.run(["geng", "-c", "-q", str(n)],
                            capture_output=True, text=True).stdout.split()
        for g6 in gs:
            nn, adj = parse_g6(g6)
            full = (1 << nn) - 1
            b = max_bip(nn, adj, full)
            o = nn - b
            if o == 0:
                continue
            tot2 += 1
            p = path_cover(nn, adj, full)
            best = 0
            for T in combinations(range(nn), o):
                Tm = 0
                for t in T:
                    Tm |= 1 << t
                rest = full ^ Tm
                if not is_bip(nn, adj, rest):
                    continue
                ce = comps_with_edge(nn, adj, rest)
                if ce > best:
                    best = ce
            ok = p <= 2 * best - 1
            hist[(p, best)] = hist.get((p, best), 0) + 1
            if ok:
                cov += 1
    print(f"L2 coverage on connected nonbipartite graphs 3<=n<={nmax}: "
          f"{cov}/{tot2} = {100.0*cov/max(tot2,1):.1f}% satisfy "
          f"p <= 2*max_T c_e(G-T) - 1")


if __name__ == "__main__":
    main()
