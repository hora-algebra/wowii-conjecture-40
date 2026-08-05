#!/usr/bin/env python3
"""VERIFY-2 independent SD engine.

Written from the STATEMENTS only:
  proofs/PROOFS.md  (sec A model/CES, sec E d0/A1/B-PLUS-2)
  PREREG-SD.md sec 0/2, PREREG-SD2.md sec 2   (SD-SHORT, SD-2STEP[-DESCENT])
No code from work/sd/*.py, tools/*.py or verification/*.py was read before this
file was complete.

Model (PROOFS.md sec A):
  G connected bipartite; S a MINIMUM feedback vertex set with |S| >= 2;
  H = G - S (a forest); a distinguished edge e = (x,y) in E(H).
  Each s in S has demand 2; each h in H has capacity c(h) = 2, except
  c(x) = c(y) = 1.  A feasible selection J gives every s exactly two distinct
  H-incidences, respecting capacities.
  A SELECTED CYCLE is a cyclic component of the incidence graph J.

  CES (canonical): J -> J' is cycle-erasing for a designated selected cycle C
  iff (i) C is not a selected cycle of J', and (ii) every selected cycle of J'
  was already a selected cycle of J.

  Residual digraph of N-a for released incidence a=(s,h): a is ABSENT from the
  network; arcs s'->h' on unselected incidences, h'->s' on selected ones.  An
  augmenting path runs from the deficient s to any H-vertex t with
  load(t) < c(t); its length is its number of incidence edges (always odd).
  a is AVOIDABLE iff some feasible selection omits a, equivalently iff such an
  augmenting path exists (max-flow / min-cut).
  d0(C) = min over avoidable a on C of the shortest augmenting-path length.
  A MINIMISING STEP at C is a toggle along a path of length exactly d0(C).
  A1(C): some minimising step at C is CES for C.
"""
import sys, os, json, itertools
from collections import deque

PATH_CAP = 50000
INF = 10 ** 9


# ---------------------------------------------------------------- graph6
def g6_decode(s):
    b = s.strip().encode()
    if not b:
        return 0, []
    if b[0] == 126:
        raise ValueError("n >= 63 unsupported")
    n = b[0] - 63
    bits = []
    for ch in b[1:]:
        v = ch - 63
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    adj = [0] * n
    p = 0
    for j in range(1, n):
        for i in range(j):
            if p < len(bits) and bits[p]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            p += 1
    return n, adj


def popcount(x):
    return bin(x).count("1")


# ---------------------------------------------------------------- forest / FVS
def is_forest(adj, mask, n):
    seen = 0
    for r in range(n):
        b = 1 << r
        if not (mask & b) or (seen & b):
            continue
        comp = b
        seen |= b
        stack = [r]
        vcount = 0
        edeg = 0
        while stack:
            v = stack.pop()
            vcount += 1
            nb = adj[v] & mask
            edeg += popcount(nb)
            m = nb & ~comp
            while m:
                lb = m & -m
                comp |= lb
                seen |= lb
                stack.append(lb.bit_length() - 1)
                m ^= lb
        if edeg // 2 != vcount - 1:
            return False
    return True


def min_fvs_all(adj, n):
    full = (1 << n) - 1
    for k in range(n + 1):
        out = []
        for combo in itertools.combinations(range(n), k):
            S = 0
            for v in combo:
                S |= 1 << v
            if is_forest(adj, full & ~S, n):
                out.append(S)
        if out:
            return k, out
    return n, [full]


# ---------------------------------------------------------------- instance
class Inst:
    def __init__(self, adj, n, Smask, e):
        self.S = [v for v in range(n) if (Smask >> v) & 1]
        self.H = [v for v in range(n) if not ((Smask >> v) & 1)]
        hidx = {h: i for i, h in enumerate(self.H)}
        self.nS = len(self.S)
        self.nH = len(self.H)
        self.cap = [2] * self.nH
        self.cap[hidx[e[0]]] = 1
        self.cap[hidx[e[1]]] = 1
        self.inc = [sorted(hidx[h] for h in self.H if (adj[s] >> h) & 1)
                    for s in self.S]
        self.pairs = [list(itertools.combinations(self.inc[i], 2))
                      for i in range(self.nS)]
        self.incset = frozenset((i, h) for i in range(self.nS)
                                for h in self.inc[i])
        # users[h] = S-indices incident to h
        self.users = [[] for _ in range(self.nH)]
        for i in range(self.nS):
            for h in self.inc[i]:
                self.users[h].append(i)
        self.ok = all(len(p) > 0 for p in self.pairs)

    # ---- enumerate feasible selections
    def selections(self, limit=None):
        k = self.nS
        load = [0] * self.nH
        choice = [0] * k
        out = []
        cap = self.cap
        pairs = self.pairs

        def rec(i):
            if i == k:
                out.append(tuple(choice))
                return limit is not None and len(out) >= limit
            for pi, (a, b) in enumerate(pairs[i]):
                if load[a] < cap[a] and load[b] < cap[b]:
                    load[a] += 1
                    load[b] += 1
                    choice[i] = pi
                    if rec(i + 1):
                        load[a] -= 1
                        load[b] -= 1
                        return True
                    load[a] -= 1
                    load[b] -= 1
            return False

        rec(0)
        return out

    def selections_avoiding(self, i0, h0):
        """is there a feasible selection in which S-vertex i0 does not use h0?"""
        k = self.nS
        load = [0] * self.nH
        cap = self.cap
        pairs = self.pairs

        def rec(i):
            if i == k:
                return True
            for pi, (a, b) in enumerate(pairs[i]):
                if i == i0 and (a == h0 or b == h0):
                    continue
                if load[a] < cap[a] and load[b] < cap[b]:
                    load[a] += 1
                    load[b] += 1
                    if rec(i + 1):
                        load[a] -= 1
                        load[b] -= 1
                        return True
                    load[a] -= 1
                    load[b] -= 1
            return False

        return rec(0)

    def forced_set(self):
        return frozenset((i, h) for i in range(self.nS) for h in self.inc[i]
                         if not self.selections_avoiding(i, h))

    def sel_of(self, choice):
        s = set()
        for i in range(self.nS):
            a, b = self.pairs[i][choice[i]]
            s.add((i, a))
            s.add((i, b))
        return frozenset(s)

    def loads(self, selset):
        L = [0] * self.nH
        for (_, h) in selset:
            L[h] += 1
        return L


# ---------------------------------------------------------------- cycles
def cycle_components(inst, selset):
    """max degree <= 2, so components are paths or cycles; a component is a
    cycle iff #edges == #vertices."""
    adjS = [[] for _ in range(inst.nS)]
    adjH = [[] for _ in range(inst.nH)]
    for (i, h) in selset:
        adjS[i].append(h)
        adjH[h].append(i)
    seenS = [False] * inst.nS
    seenH = [False] * inst.nH
    cyc = []
    for start in range(inst.nS):
        if seenS[start]:
            continue
        seenS[start] = True
        nv = 0
        edges = set()
        dq = deque([(0, start)])
        while dq:
            side, v = dq.popleft()
            nv += 1
            if side == 0:
                for h in adjS[v]:
                    edges.add((v, h))
                    if not seenH[h]:
                        seenH[h] = True
                        dq.append((1, h))
            else:
                for i in adjH[v]:
                    edges.add((i, v))
                    if not seenS[i]:
                        seenS[i] = True
                        dq.append((0, i))
        if len(edges) == nv:
            cyc.append(frozenset(edges))
    return cyc


def cycle_count_unionfind(inst, selset):
    """independent count: contract each S-vertex (degree exactly 2) into one
    edge of a multigraph M on H; count insertions that close a cycle."""
    par = list(range(inst.nH))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    byS = {}
    for (i, h) in selset:
        byS.setdefault(i, []).append(h)
    c = 0
    for hs in byS.values():
        a, b = find(hs[0]), find(hs[1])
        if a == b:
            c += 1
        else:
            par[a] = b
    return c


# ---------------------------------------------------------------- residual
def bfs_residual(inst, selset, load, a, maxlen=None):
    """returns (dist, dS, dH, targets) for the residual of N-a."""
    i0, h0 = a
    sel = selset - {a}
    L = list(load)
    L[h0] -= 1
    dS = [INF] * inst.nS
    dH = [INF] * inst.nH
    dS[i0] = 0
    frontier = [(0, i0)]
    d = 0
    while frontier:
        if maxlen is not None and d >= maxlen:
            return INF, dS, dH, []
        nxt = []
        for side, v in frontier:
            if side == 0:
                for h in inst.inc[v]:
                    if (v, h) in sel or (v, h) == a:
                        continue
                    if dH[h] > d + 1:
                        dH[h] = d + 1
                        nxt.append((1, h))
            else:
                for i in inst.users[v]:
                    if (i, v) in sel and dS[i] > d + 1:
                        dS[i] = d + 1
                        nxt.append((0, i))
        d += 1
        if not nxt:
            return INF, dS, dH, []
        hits = [h for (side, h) in nxt if side == 1 and L[h] < inst.cap[h]]
        if hits:
            return d, dS, dH, hits
        frontier = nxt
    return INF, dS, dH, []


def enum_paths(inst, selset, a, dS, dH, targets, cap_counter):
    """all shortest augmenting paths, as ordered lists of incidence edges
    (odd length; even index = added/unselected, odd index = removed/selected)."""
    sel = selset - {a}
    paths = []
    stack = [(1, t, ()) for t in targets]
    while stack:
        side, node, sofar = stack.pop()
        if len(paths) >= PATH_CAP:
            cap_counter[0] += 1
            break
        if side == 1:                                  # arrived at H via unsel
            for i in inst.users[node]:
                ed = (i, node)
                if ed in sel or ed == a:
                    continue
                if dS[i] != dH[node] - 1:
                    continue
                ns = ((ed,) + sofar)
                if i == a[0] and dS[i] == 0:
                    paths.append(list(ns))
                else:
                    stack.append((0, i, ns))
        else:                                          # arrived at S via sel
            for h in inst.inc[node]:
                ed = (node, h)
                if ed not in sel:
                    continue
                if dH[h] != dS[node] - 1:
                    continue
                stack.append((1, h, (ed,) + sofar))
    return paths


def toggle(selset, a, path):
    new = set(selset)
    new.discard(a)
    for k, ed in enumerate(path):
        if k % 2 == 0:
            new.add(ed)
        else:
            new.discard(ed)
    return frozenset(new)


def is_ces(inst, oldcycset, newsel, C):
    ncy = cycle_components(inst, newsel)
    if C in ncy:
        return False, ncy
    for z in ncy:
        if z not in oldcycset:
            return False, ncy
    return True, ncy
