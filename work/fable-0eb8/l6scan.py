#!/usr/bin/env python3
"""Frozen checker for the L6 forest-extension bonus and the prospective n=9
universality scan of the L5/L6 lifting conditions.

Branch attempt/2026-08-04-claude-fable-5-0eb8. Statements, universes,
controls, and decision rules are frozen in PREREG-L6-N9.md at the repo root.

Definitions (B bipartite; components of B; C ranges over edge-containing
components with color classes A_C, B_C):

  c_e(B)   = number of edge-containing components
  i(B)     = number of isolated vertices
  M(B)     = sum_C min(|A_C|,|B_C|)
  Delta(B) = i(B) + sum_C ||A_C|-|B_C||     ( = |B| - 2M(B) )
  r(C)     = 1 if some class of C of size <= the other class's size contains
             two vertices with at most one common neighbour in C, else 0
  r(B)     = sum_C r(C)
  FE(C)    = max over ordered class pairs (W,Z) in {(A_C,B_C),(B_C,A_C)} and
             Y subset of Z with C[W u Y] acyclic, of |W| + |Y|
  g(C)     = FE(C) - max(|A_C|,|B_C|)      (g >= 1: Y one vertex is a star)
  g(B)     = sum_C g(C)

Statements tested (G connected nonbipartite; T ranges over ALL minimum OCTs
of G; B = G - T; p = p(G); ell = n - p; o = |T|):

  S1 (L5 condition universality): some minimum OCT T has
       p <= 2 c_e(B) + Delta(B) + 2 r(B) - 1
  S2 (L6 condition universality): some minimum OCT T has
       p <= Delta(B) + 2 g(B) - 1
  S3 (exact LIFT-A): some minimum OCT T has ell >= 2 tau(B) + o + 1
  T1 (L6-Forest): tau(B) <= M(B) - g(B) for every bipartite B
  CTRL-T1-MINUS-1: tau(B) <= M(B) - g(B) - 1 must FAIL somewhere
  CTRL-EXACT-PLUS-1: ell >= 2 tau(B) + o + 2 (best T) must FAIL somewhere
  INV-DOM: per (G,T), L6 threshold >= L5 threshold  (since g >= 1 + r)

Modes:
  gold          known-value controls (DC{, K3, C5, C7, bowtie, 7 L3
                residuals, 3 SV witnesses at n=11)
  regress       full n<=8 sweep; must reproduce the audited counts
  bip9          T1 + control on all 1,119 bipartite graphs at n=9
  scan9 R M     prospective scan of connected n=9 shard R/M
"""
import subprocess, sys, os
from itertools import combinations

GENG = "/opt/homebrew/bin/geng"


def parse_graph6(line):
    line = line.strip()
    data = [ord(c) - 63 for c in line]
    n = data[0]
    bits = []
    for v in data[1:]:
        for i in range(5, -1, -1):
            bits.append((v >> i) & 1)
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return n, adj


def from_edges(n, E):
    adj = [0] * n
    for a, b in E:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return n, adj


def is_forest_subset(adj, mask):
    verts = [v for v in range(len(adj)) if mask >> v & 1]
    parent = {v: v for v in verts}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for i in verts:
        ai = adj[i]
        for j in verts:
            if j > i and (ai >> j & 1):
                ri, rj = find(i), find(j)
                if ri == rj:
                    return False
                parent[ri] = rj
    return True


def tau_of(n, adj, mask=None):
    if mask is None:
        mask = (1 << n) - 1
    verts = [v for v in range(n) if mask >> v & 1]
    m = len(verts)
    for f in range(m, -1, -1):
        for keep in combinations(verts, f):
            km = 0
            for v in keep:
                km |= 1 << v
            if is_forest_subset(adj, km):
                return m - f
    return m


def bipartition_of(n, adj, mask):
    color = {}
    for start in range(n):
        if not (mask >> start & 1) or start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in range(n):
                if (mask >> v & 1) and (adj[u] >> v & 1):
                    if v not in color:
                        color[v] = 1 - color[u]
                        stack.append(v)
                    elif color[v] == color[u]:
                        return False, None
    return True, color


def components(n, adj, mask):
    seen = 0
    out = []
    for start in range(n):
        if not (mask >> start & 1) or (seen >> start & 1):
            continue
        comp = 1 << start
        stack = [start]
        while stack:
            u = stack.pop()
            for v in range(n):
                if (mask >> v & 1) and (adj[u] >> v & 1) and not (comp >> v & 1):
                    comp |= 1 << v
                    stack.append(v)
        seen |= comp
        out.append(comp)
    return out


def fe_of_component(n, adj, comp, A, B):
    """FE(C): max |W| + |Y|, W a full class, Y in the other, C[W u Y] forest."""
    best = 0
    for W, Z in ((A, B), (B, A)):
        wm = 0
        for v in W:
            wm |= 1 << v
        # descending |Y| with early exit
        found = False
        for k in range(len(Z), -1, -1):
            for Y in combinations(Z, k):
                ym = wm
                for v in Y:
                    ym |= 1 << v
                if is_forest_subset(adj, ym):
                    best = max(best, len(W) + k)
                    found = True
                    break
            if found:
                break
    return best


def bip_stats(n, adj, mask):
    """(c_e, i, M, Delta, r, g) of the bipartite graph induced on mask."""
    ok, color = bipartition_of(n, adj, mask)
    assert ok
    c_e = i = M = imb = r = g = 0
    for comp in components(n, adj, mask):
        verts = [v for v in range(n) if comp >> v & 1]
        has_edge = any(adj[u] >> v & 1 for u in verts for v in verts if v > u)
        if not has_edge:
            i += len(verts)
            continue
        c_e += 1
        A = [v for v in verts if color[v] == 0]
        B = [v for v in verts if color[v] == 1]
        a, b = len(A), len(B)
        M += min(a, b)
        imb += abs(a - b)
        rc = 0
        small = []
        if a <= b:
            small.append(A)
        if b <= a:
            small.append(B)
        for cls in small:
            for u, v in combinations(cls, 2):
                if bin(adj[u] & adj[v] & comp).count("1") <= 1:
                    rc = 1
        r += rc
        fe = fe_of_component(n, adj, comp, A, B)
        gc = fe - max(a, b)
        assert gc >= 1 + rc, ("g >= 1 + r violated", gc, rc)
        g += gc
    return c_e, i, M, imb + i, r, g


def path_cover(n, adj):
    full = (1 << n) - 1
    ham = [0] * (full + 1)
    for v in range(n):
        ham[1 << v] = 1 << v
    order = sorted(range(1, full + 1), key=lambda m: bin(m).count("1"))
    for mask in order:
        if bin(mask).count("1") < 2:
            continue
        ends = 0
        for v in range(n):
            if not (mask >> v & 1):
                continue
            if ham[mask ^ (1 << v)] & adj[v]:
                ends |= 1 << v
        ham[mask] = ends
    INF = 99
    dp = [INF] * (full + 1)
    dp[0] = 0
    for mask in order:
        low = mask & (-mask)
        sub = mask
        while sub:
            if (sub & low) and ham[sub]:
                cand = dp[mask ^ sub] + 1
                if cand < dp[mask]:
                    dp[mask] = cand
            sub = (sub - 1) & mask
    return dp[full]


def min_octs(n, adj):
    full = (1 << n) - 1
    for k in range(n + 1):
        found = []
        for T in combinations(range(n), k):
            tm = 0
            for v in T:
                tm |= 1 << v
            ok, _ = bipartition_of(n, adj, full ^ tm)
            if ok:
                found.append(tm)
        if found:
            return k, found
    raise RuntimeError


def profile(n, adj):
    """Full per-graph record for a connected nonbipartite graph."""
    full = (1 << n) - 1
    p = path_cover(n, adj)
    ell = n - p
    o, octs = min_octs(n, adj)
    best = dict(l5=-10**9, l6=-10**9, slack=-10**9)
    per_oct = []
    for T in octs:
        bm = full ^ T
        tau_b = tau_of(n, adj, bm)
        c_e, i, M, Delta, r, g = bip_stats(n, adj, bm)
        thr5 = 2 * c_e + Delta + 2 * r - 1
        thr6 = Delta + 2 * g - 1
        assert thr6 >= thr5, ("INV-DOM violated", thr5, thr6)
        slack = ell - (2 * tau_b + o + 1)
        best["l5"] = max(best["l5"], thr5 - p)
        best["l6"] = max(best["l6"], thr6 - p)
        best["slack"] = max(best["slack"], slack)
        per_oct.append((T, tau_b, c_e, Delta, r, g, thr5, thr6, slack))
    return dict(n=n, p=p, ell=ell, o=o, octs=octs, best=best, per_oct=per_oct)


def check_bip_graph(n, adj):
    """(T1 ok, T1 tight, minus-1 control fires) for one bipartite graph."""
    full = (1 << n) - 1
    tau = tau_of(n, adj)
    c_e, i, M, Delta, r, g = bip_stats(n, adj, full)
    ok = tau <= M - g
    tight = tau == M - g
    ctrl = not (tau <= M - g - 1)
    return ok, tight, ctrl


# ------------------------------------------------------------------ gold
def gold():
    fails = []

    def expect(name, cond):
        print(f"  {name}: {'PASS' if cond else 'FAIL'}")
        if not cond:
            fails.append(name)

    # DC{ : o=1, p=2; L2 fails, L3 passes; exact holds
    n, adj = parse_graph6("DC{")
    pr = profile(n, adj)
    expect("DC{ o=1 p=2", pr["o"] == 1 and pr["p"] == 2)
    l2 = any(pr_o[2] * 2 - 1 >= pr["p"] for pr_o in pr["per_oct"])
    l3 = any(2 * pr_o[2] + pr_o[3] - 1 >= pr["p"] for pr_o in pr["per_oct"])
    expect("DC{ fails L2, passes L3", (not l2) and l3)
    expect("DC{ exact LIFT-A", pr["best"]["slack"] >= 0)
    expect("DC{ covered by L5 and L6",
           pr["best"]["l5"] >= 0 and pr["best"]["l6"] >= 0)

    # K3: o=1 p=1 ell=2, slack 0 (tight); false exact+1 must fail here
    n, adj = from_edges(3, [(0, 1), (1, 2), (0, 2)])
    pr = profile(n, adj)
    expect("K3 o=1 p=1 slack=0", pr["o"] == 1 and pr["p"] == 1
           and pr["best"]["slack"] == 0)
    expect("K3 covered by L5/L6", pr["best"]["l5"] >= 0 and pr["best"]["l6"] >= 0)

    # C5 and C7: o=1, p=1, slack 2 and 4
    for m, want_slack in ((5, 2), (7, 4)):
        n, adj = from_edges(m, [(i, (i + 1) % m) for i in range(m)])
        pr = profile(n, adj)
        expect(f"C{m} o=1 p=1 slack={want_slack}",
               pr["o"] == 1 and pr["p"] == 1
               and pr["best"]["slack"] == want_slack)

    # bowtie: unique min OCT (center), o=1, p=1
    n, adj = from_edges(5, [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4)])
    pr = profile(n, adj)
    expect("bowtie o=1 p=1 unique OCT {0}",
           pr["o"] == 1 and pr["p"] == 1 and pr["octs"] == [1])
    expect("bowtie covered by L2 (c_e=2)",
           any(pr_o[2] == 2 for pr_o in pr["per_oct"]))

    # the seven L3 residuals: known (o,p); L5 must cover, L3 must not
    resid = {"F?o}W": (1, 2), "FCQV_": (1, 2), "G?BEH{": (1, 3),
             "G?`CVo": (1, 3), "G?o}][": (2, 2), "GCQQVo": (2, 2),
             "GCQSng": (2, 2)}
    for g6, (o_w, p_w) in resid.items():
        n, adj = parse_graph6(g6)
        pr = profile(n, adj)
        l3 = any(2 * po[2] + po[3] - 1 >= pr["p"] for po in pr["per_oct"])
        expect(f"{g6} o={o_w} p={p_w} L3-uncovered L5-covered L6-covered",
               pr["o"] == o_w and pr["p"] == p_w and (not l3)
               and pr["best"]["l5"] >= 0 and pr["best"]["l6"] >= 0)

    # SV witnesses at n=11: o=1, p=3, unique min OCT, exact slack 4
    for g6 in ("J???FAWdVD?", "J???FBObs\\?", "J???FAWdUD_"):
        n, adj = parse_graph6(g6)
        pr = profile(n, adj)
        expect(f"{g6} o=1 p=3 unique-OCT slack=4",
               pr["o"] == 1 and pr["p"] == 3 and len(pr["octs"]) == 1
               and pr["best"]["slack"] == 4)
        print(f"    (data) {g6}: L5 margin {pr['best']['l5']},"
              f" L6 margin {pr['best']['l6']}")

    print("GOLD:", "ALL PASS" if not fails else f"FAILURES {fails}")
    return not fails


# --------------------------------------------------------------- regress
def regress():
    per_order_bip = {2: 2, 3: 3, 4: 7, 5: 13, 6: 35, 7: 88, 8: 303}
    tot = t1f = t1t = ctrl = 0
    for n in range(2, 9):
        cnt = 0
        out = subprocess.run([GENG, "-b", "-q", str(n)],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            nn, adj = parse_graph6(line)
            cnt += 1
            tot += 1
            ok, tight, c = check_bip_graph(nn, adj)
            t1f += 0 if ok else 1
            t1t += 1 if tight else 0
            ctrl += 1 if c else 0
        assert cnt == per_order_bip[n], (n, cnt)
    print(f"regress bipartite n<=8: {tot} graphs, T1 failures={t1f}, "
          f"tight={t1t}, minus-1 control fires={ctrl}")
    assert tot == 451 and t1f == 0 and ctrl > 0

    conn_want = {3: 2, 4: 6, 5: 21, 6: 112, 7: 853, 8: 11117}
    nonbip = s1f = s2f = s3f = l6not5 = 0
    exact_plus1_fails = 0
    for n in range(3, 9):
        cnt = 0
        out = subprocess.run([GENG, "-c", "-q", str(n)],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            nn, adj = parse_graph6(line)
            cnt += 1
            full = (1 << nn) - 1
            ok, _ = bipartition_of(nn, adj, full)
            if ok:
                continue
            nonbip += 1
            pr = profile(nn, adj)
            if pr["best"]["l5"] < 0:
                s1f += 1
            if pr["best"]["l6"] < 0:
                s2f += 1
            if pr["best"]["slack"] < 0:
                s3f += 1
            if pr["best"]["l6"] >= 0 > pr["best"]["l5"]:
                l6not5 += 1
            if pr["best"]["slack"] < 1:
                exact_plus1_fails += 1
        assert cnt == conn_want[n], (n, cnt)
    print(f"regress connected nonbipartite n<=8: {nonbip}; "
          f"S1 failures={s1f} S2 failures={s2f} S3 failures={s3f}; "
          f"exact+1 control fails on {exact_plus1_fails}")
    assert nonbip == 11859 and s1f == 0 and s2f == 0 and s3f == 0
    assert exact_plus1_fails > 0
    print("REGRESS: ALL PASS (L5 coverage 11,859/11,859 reproduced; "
          "L6 also total)")
    return True


# ------------------------------------------------------------------ bip9
def bip9():
    tot = t1f = t1t = ctrl = 0
    out = subprocess.run([GENG, "-b", "-q", "9"],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        nn, adj = parse_graph6(line)
        tot += 1
        ok, tight, c = check_bip_graph(nn, adj)
        t1f += 0 if ok else 1
        t1t += 1 if tight else 0
        ctrl += 1 if c else 0
    print(f"bip9: {tot} graphs, T1 failures={t1f}, tight={t1t}, "
          f"minus-1 control fires={ctrl}")
    assert tot == 1119, tot
    return t1f == 0 and ctrl > 0


# ----------------------------------------------------------------- scan9
def scan9(res, mod, outdir):
    os.makedirs(outdir, exist_ok=True)
    tag = f"{res}m{mod}"
    conn = nonbip = s1f = s2f = s3f = l6not5 = tight = 0
    s1_wit, s2_wit = [], []
    tight_list = []
    proc = subprocess.Popen([GENG, "-c", "-q", "9", f"{res}/{mod}"],
                            stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        nn, adj = parse_graph6(line)
        conn += 1
        full = (1 << nn) - 1
        ok, _ = bipartition_of(nn, adj, full)
        if ok:
            continue
        nonbip += 1
        pr = profile(nn, adj)
        if pr["best"]["l5"] < 0:
            s1f += 1
            s1_wit.append((line.strip(), pr["p"], pr["o"],
                           [po[1:] for po in pr["per_oct"]]))
        if pr["best"]["l6"] < 0:
            s2f += 1
            s2_wit.append((line.strip(), pr["p"], pr["o"],
                           [po[1:] for po in pr["per_oct"]]))
        if pr["best"]["slack"] < 0:
            s3f += 1
        if pr["best"]["l6"] >= 0 > pr["best"]["l5"]:
            l6not5 += 1
        if pr["best"]["slack"] == 0:
            tight += 1
            tight_list.append(line.strip())
    proc.wait()
    assert proc.returncode == 0
    with open(os.path.join(outdir, f"tight-{tag}.g6"), "w") as f:
        for g6 in tight_list:
            f.write(g6 + "\n")
    with open(os.path.join(outdir, f"summary-{tag}.txt"), "w") as f:
        f.write(f"shard {res}/{mod}: connected={conn} nonbip={nonbip} "
                f"S1fail={s1f} S2fail={s2f} S3fail={s3f} "
                f"L6-not-L5={l6not5} tight={tight}\n")
        for g6, p, o, po in s1_wit:
            f.write(f"S1-WIT {g6} p={p} o={o} per-oct={po}\n")
        for g6, p, o, po in s2_wit:
            f.write(f"S2-WIT {g6} p={p} o={o} per-oct={po}\n")
    print(f"shard {res}/{mod}: connected={conn} nonbip={nonbip} "
          f"S1fail={s1f} S2fail={s2f} S3fail={s3f} "
          f"L6-not-L5={l6not5} tight={tight}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "gold":
        sys.exit(0 if gold() else 1)
    elif mode == "regress":
        sys.exit(0 if regress() else 1)
    elif mode == "bip9":
        sys.exit(0 if bip9() else 1)
    elif mode == "scan9":
        scan9(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("unknown mode")
