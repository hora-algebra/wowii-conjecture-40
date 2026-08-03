"""Independent second engine for Conjecture 40 (pure-Python bitmask).

Verifies the bound  p(G) + b(G) + 1 <= 2 f(G)  on graph6 input, where
  f = max induced forest (union-find subset scan),
  b = max induced bipartite subgraph (2-colouring subset scan),
  p = min path cover = n - max spanning linear forest (ham + dp bitmask).
Coded independently of the C checker phase0.c; used to re-verify every low-slack
graph. Self-contained: a graph6 parser is inlined (no external dependency, no
absolute paths).

Usage:
  python3 phase0_verify2.py FILE [FILE ...]   # each line: a graph6 string
  cat witnesses.txt | python3 phase0_verify2.py -   # read from stdin
Exit status 0 and "bound-violations=0" means all checked graphs satisfy the bound.
"""
import sys, time

def parse_g6(s):
    """graph6 -> (n, adj[]) with adj[v] a bitmask of neighbours (n <= 62)."""
    s = s.strip().split()[0]
    data = [ord(c) - 63 for c in s]
    n = data[0]
    bits = []
    for byte in data[1:]:
        for k in range(5, -1, -1):
            bits.append((byte >> k) & 1)
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            idx += 1
    return n, adj

def f_forest(n, adj):
    best = 0
    for S in range(1 << n):
        pc = bin(S).count('1')
        if pc <= best: continue
        par = list(range(n)); ok = 1
        m = S
        while m and ok:
            j = (m & -m).bit_length() - 1; m &= m - 1
            nb = adj[j] & S & ((1 << j) - 1)
            while nb:
                i = (nb & -nb).bit_length() - 1; nb &= nb - 1
                a = i
                while par[a] != a: a = par[a]
                c = j
                while par[c] != c: c = par[c]
                if a == c: ok = 0; break
                par[a] = c
        if ok: best = pc
    return best

def b_bip(n, adj):
    best = 0
    for S in range(1 << n):
        pc = bin(S).count('1')
        if pc <= best: continue
        col = [-1] * n; ok = 1
        for st in range(n):
            if (S >> st & 1) and col[st] < 0:
                stack = [st]; col[st] = 0
                while stack and ok:
                    u = stack.pop(); nb = adj[u] & S
                    while nb:
                        v = (nb & -nb).bit_length() - 1; nb &= nb - 1
                        if col[v] < 0: col[v] = col[u] ^ 1; stack.append(v)
                        elif col[v] == col[u]: ok = 0; break
                if not ok: break
        if ok: best = pc
    return best

def p_cover(n, adj):
    M = 1 << n
    ham = [0] * M
    for v in range(n): ham[1 << v] = 1 << v
    pathset = [0] * M
    for v in range(n): pathset[1 << v] = 1
    for mask in range(1, M):
        if bin(mask).count('1') < 2: continue
        last = 0
        m = mask
        while m:
            v = (m & -m).bit_length() - 1; m &= m - 1
            prev = mask ^ (1 << v)
            if adj[v] & ham[prev] & prev: last |= (1 << v)
        ham[mask] = last
        if last: pathset[mask] = 1
    INF = 99; dp = [INF] * M; dp[0] = 0
    for mask in range(1, M):
        best = INF; sub = mask
        while sub:
            if pathset[sub]:
                c = dp[mask ^ sub] + 1
                if c < best: best = c
            sub = (sub - 1) & mask
        dp[mask] = best
    return dp[M - 1]

def main(argv):
    files = argv[1:] or ['-']
    t0 = time.time(); total = 0; bviol = 0; bad = []
    for fn in files:
        fh = sys.stdin if fn == '-' else open(fn)
        for line in fh:
            g6 = line.strip()
            if not g6: continue
            n, adj = parse_g6(g6)
            f = f_forest(n, adj); b = b_bip(n, adj); p = p_cover(n, adj)
            total += 1
            if p + b + 1 > 2 * f:
                bviol += 1; bad.append((g6, f, b, p))
        if fn != '-': fh.close()
    print(f"verify2: {total} graphs in {time.time()-t0:.0f}s; bound-violations={bviol}")
    for g in bad[:20]:
        print("  BVIOL", g)
    return 1 if bviol else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
