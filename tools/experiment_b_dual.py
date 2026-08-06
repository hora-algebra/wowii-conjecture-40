"""Independent (dual-engine) ell2 checker via path-subset DP + Ham-path
backtracking, per the dual-invariant spec. Cross-validates against the edge-B&B
ell2 in experiment_b.py, then mines the D=0 discovery set (property A: does
EVERY critical vertex succeed, or only some?)."""
import subprocess
import sys
from functools import lru_cache

sys.path.insert(0, ".")
import inv_b
import inv40_b
import experiment_b as EB


def ell2_dp(n, adj):
    """Return dict v -> ell2(G,v) for all v, via subset-path DP. Independent
    of the edge-B&B: uses (a) a reach DP for single-path coverability and
    (b) Ham-path backtracking for the v-internal predicate."""
    full = (1 << n) - 1
    # reach[mask][u]: simple path covering exactly mask ending at u
    reach = [0] * (1 << n)   # bitmask of possible endpoints
    for u in range(n):
        reach[1 << u] = 1 << u
    for mask in range(1, 1 << n):
        if mask & (mask - 1) == 0:
            continue
        ends = 0
        sub = mask
        while sub:
            u = (sub & -sub).bit_length() - 1
            sub &= sub - 1
            prev = mask ^ (1 << u)
            if reach[prev] & adj[u]:   # some endpoint of prev adjacent to u
                ends |= 1 << u
        reach[mask] = ends
    canpath = [reach[m] != 0 for m in range(1 << n)]

    def v_internal(mask, v):
        # Ham path of G[mask] with v not an endpoint?
        verts = [u for u in range(n) if mask >> u & 1]
        if len(verts) < 3 or not (mask >> v & 1):
            return False
        found = [False]

        def dfs(u, visited, first):
            if found[0]:
                return
            if visited == mask:
                if first != v and u != v:
                    found[0] = True
                return
            m = adj[u] & mask & ~visited
            while m:
                w = (m & -m).bit_length() - 1
                m &= m - 1
                dfs(w, visited | (1 << w), first)
                if found[0]:
                    return
        for s in verts:
            dfs(s, 1 << s, s)
            if found[0]:
                break
        return found[0]

    def p_internal(v):
        INF = 99
        dp = [[INF, INF] for _ in range(1 << n)]
        dp[0][0] = 0
        for mask in range(1 << n):
            if dp[mask][0] == INF and dp[mask][1] == INF:
                continue
            rem = full ^ mask
            u = (rem & -rem).bit_length() - 1
            # enumerate subsets T of rem that contain u
            t = rem
            subs = []
            while t:
                if t & (1 << u):
                    subs.append(t)
                t = (t - 1) & rem
            for T in subs:
                if not canpath[T]:
                    continue
                for flag in (0, 1):
                    if dp[mask][flag] == INF:
                        continue
                    nm = mask | T
                    if dp[mask][flag] + 1 < dp[nm][flag]:
                        dp[nm][flag] = dp[mask][flag] + 1
                    if flag == 0 and (T >> v & 1) and v_internal(T, v):
                        if dp[mask][0] + 1 < dp[nm][1]:
                            dp[nm][1] = dp[mask][0] + 1
        return dp[full][1]

    out = {}
    for v in range(n):
        pi = p_internal(v)
        out[v] = (n - pi) if pi < 99 else -1
    return out


def critical(n, adj, k):
    C = []
    for v in range(n):
        m, a2 = EB.induced(n, adj, v)
        if EB.tau(m, a2) == k - 1:
            C.append(v)
    return C


if __name__ == "__main__":
    startn = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    maxn = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    OUT = "dual-overnight.txt"
    mism = 0
    checked = 0
    d0_total = 0
    d0_all_crit_succeed = 0
    d0_only_some = 0
    for n in range(startn, maxn + 1):
        d0_this = subprocess.run(["geng", "-b", "-C", "-q", str(n)],
                                 capture_output=True, text=True).stdout.split()
        gi = 0
        for g6 in d0_this:
            gi += 1
            if gi % 200 == 0:
                with open(OUT, "a") as fo:
                    fo.write(f"n={n} progress {gi}/{len(d0_this)} checks={checked} "
                             f"mismatches={mism} d0={d0_total} onlysome={d0_only_some}\n")
            nn, adj = inv_b.parse_g6(g6)
            k = EB.tau(nn, adj)
            if k == 0:
                continue
            f = inv_b.forest_b(nn, adj)
            b = inv40_b.bipartite_b(nn, adj)
            p = inv40_b.pathcover_b(nn, adj)
            D = 2 * (nn - f) + 1 - (nn - p) - (nn - b)
            C = critical(nn, adj, k)
            # dual-check ell2 for all critical v (bb vs dp)
            dp = ell2_dp(nn, adj)
            for v in C:
                bb = EB.ell2(nn, adj, v)
                if bb != dp[v]:
                    print(f"!!! MISMATCH n={nn} {g6} v={v} bb={bb} dp={dp[v]}")
                    mism += 1
                checked += 1
            # mine D=0
            if D == 0:
                d0_total += 1
                succ = [v for v in C if dp[v] >= 2 * k + 1]
                if len(succ) == len(C):
                    d0_all_crit_succeed += 1
                else:
                    d0_only_some += 1
                    print(f"  D0 not-all-critical-succeed: {g6} k={k} "
                          f"C={C} succeed={succ} ell2={[dp[v] for v in C]}")
        with open(OUT, "a") as fo:
            fo.write(f"n={n} DONE | checks={checked} mismatches={mism} "
                     f"d0={d0_total} every-crit-succeeds={d0_all_crit_succeed} "
                     f"only-some={d0_only_some}\n")
        print(f"n={n} done | dual-checks so far={checked} mismatches={mism}")
    print(f"\nDUAL-ENGINE: {checked} (graph,critical-v) ell2 values cross-checked "
          f"BB vs DP, mismatches={mism}")
    print(f"D=0 discovery set: {d0_total} graphs | every-critical-v-succeeds="
          f"{d0_all_crit_succeed} | only-some-succeed={d0_only_some}")
