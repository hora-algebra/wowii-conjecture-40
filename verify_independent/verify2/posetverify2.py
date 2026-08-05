#!/usr/bin/env python3
"""VERIFY-2 independent carrier-poset checker.

Written from the STATEMENTS only (PREREG-CARRIER-POSET.md universe
description; PROOFS.md sec C5/C5b/C6 and sec D for tightness, carriers,
punctures).  work/carrier.py and work/b17e/carrier_poset.py were NOT read
before this file was complete.

Abstract incidence system: S = {0..k-1}, H = {0..p-1}, N(s) subset H,
capacities c(h) in {1,2}.  Feasible selection: every s takes two DISTINCT
H-neighbours, every h loaded at most c(h).

  rho(X)   = sum_h min(c(h), deg_X(h)),  delta(X) = rho(X) - 2|X|
  X TIGHT  iff delta(X) = 0            (Hall/rho-tightness)
  forced incidence (s,h): used by EVERY feasible selection
  forced core: graph of forced incidences.  Max degree 2 on both sides
    (an s has only two slots; if j incidences at h were all forced then
    c(h) >= j), so its components are paths or cycles.
  A_s  = the unique minimum tight set containing s   (uniqueness is CHECKED,
         not assumed)
  B_s  = A_s \\ {s};  U = union over s in P of B_s

  CP  : for distinct s,t in P with t in B_s, A_t proper-subset A_s; the
        digraph s->t (t in B_s) is acyclic; carriers pairwise distinct;
        P\\U = inclusion-maximal carriers; P\\U nonempty.
  ADJ : some q in Q has BOTH its two F-neighbours in P\\U.
  PDIS: P intersect U nonempty (the known-false companion).
"""
import sys, json, itertools
from collections import deque


# ---------------------------------------------------------------- system
class Sys:
    def __init__(self, nb, cap):
        self.nb = [tuple(sorted(x)) for x in nb]     # nb[s] = H-neighbours
        self.cap = list(cap)
        self.k = len(nb)
        self.p = len(cap)
        self.pairs = [list(itertools.combinations(self.nb[s], 2))
                      for s in range(self.k)]

    # ---- feasibility / selections
    def selections(self, limit=None):
        load = [0] * self.p
        cur = [0] * self.k
        out = []

        def rec(i):
            if i == self.k:
                out.append(tuple(cur))
                return limit is not None and len(out) >= limit
            for pi, (a, b) in enumerate(self.pairs[i]):
                if load[a] < self.cap[a] and load[b] < self.cap[b]:
                    load[a] += 1
                    load[b] += 1
                    cur[i] = pi
                    if rec(i + 1):
                        load[a] -= 1
                        load[b] -= 1
                        return True
                    load[a] -= 1
                    load[b] -= 1
            return False

        rec(0)
        return out

    def feasible(self):
        return len(self.selections(limit=1)) > 0

    # ---- tightness (independent of any selection)
    def rho(self, Xmask):
        t = 0
        for h in range(self.p):
            d = 0
            for s in range(self.k):
                if (Xmask >> s) & 1 and h in self.nb[s]:
                    d += 1
            t += min(self.cap[h], d)
        return t

    def tight_sets(self):
        return [X for X in range(1 << self.k)
                if self.rho(X) == 2 * bin(X).count("1")]

    def hall_ok(self):
        return all(self.rho(X) >= 2 * bin(X).count("1")
                   for X in range(1 << self.k))

    # ---- carriers
    def carriers(self):
        """A[s] as a bitmask; also returns whether the MINIMUM tight set
        containing s is unique for every s (checked, not assumed)."""
        tights = self.tight_sets()
        A = [None] * self.k
        unique = True
        for s in range(self.k):
            cont = [X for X in tights if (X >> s) & 1]
            if not cont:
                A[s] = None
                unique = False
                continue
            # inclusion-minimal members
            minimal = [X for X in cont
                       if not any(Y != X and (Y & X) == Y for Y in cont)]
            if len(minimal) != 1:
                unique = False
                A[s] = minimal[0] if minimal else None
            else:
                A[s] = minimal[0]
        return A, unique

    # ---- forced core
    def forced_edges(self):
        sels = self.selections()
        if not sels:
            return None

        allinc = set((s, h) for s in range(self.k) for h in self.nb[s])
        # forced = in EVERY selection
        forced = set(allinc)
        for ch in sels:
            cur = set()
            for s in range(self.k):
                a, b = self.pairs[s][ch[s]]
                cur.add((s, a))
                cur.add((s, b))
            forced &= cur
        return forced

    def forced_cycles(self, forced):
        """components of the forced core that are cycles (#edges == #vertices)"""
        adjS = [[] for _ in range(self.k)]
        adjH = [[] for _ in range(self.p)]
        for (s, h) in forced:
            adjS[s].append(h)
            adjH[h].append(s)
        seenS = [False] * self.k
        seenH = [False] * self.p
        out = []
        for st in range(self.k):
            if seenS[st] or not adjS[st]:
                continue
            seenS[st] = True
            nv = 0
            edges = set()
            Pv, Qv = set(), set()
            dq = deque([(0, st)])
            while dq:
                side, v = dq.popleft()
                nv += 1
                if side == 0:
                    Pv.add(v)
                    for h in adjS[v]:
                        edges.add((v, h))
                        if not seenH[h]:
                            seenH[h] = True
                            dq.append((1, h))
                else:
                    Qv.add(v)
                    for s in adjH[v]:
                        edges.add((s, v))
                        if not seenS[s]:
                            seenS[s] = True
                            dq.append((0, s))
            if len(edges) == nv:
                out.append((frozenset(edges), frozenset(Pv), frozenset(Qv)))
        return out


# ---------------------------------------------------------------- CP / ADJ
def check_cp_adj(sysm):
    """returns a verdict dict for one system, or None if it is not a feasible
    system with a cyclic forced core."""
    if not sysm.feasible():
        return None
    forced = sysm.forced_edges()
    cycles = sysm.forced_cycles(forced)
    if not cycles:
        return None
    A, uniq = sysm.carriers()
    res = {"cyclic": True, "carrier_unique": uniq,
           "cp_fail": 0, "adj_fail": 0, "pdis": 0, "detail": []}
    for (E, P, Q) in cycles:
        B = {s: (A[s] & ~(1 << s)) for s in P if A[s] is not None}
        U = 0
        for s in P:
            U |= B[s]
        Pmask = 0
        for s in P:
            Pmask |= 1 << s
        pdis = (Pmask & U) != 0
        # ---- CP part 1: containment
        cpfail = []
        for s in P:
            for t in P:
                if s == t:
                    continue
                if (B[s] >> t) & 1:
                    proper = (A[t] & ~A[s]) == 0 and A[t] != A[s]
                    if not proper:
                        cpfail.append(("containment", s, t))
        # ---- CP part 2: carriers pairwise distinct
        for s, t in itertools.combinations(sorted(P), 2):
            if A[s] == A[t]:
                cpfail.append(("distinct", s, t))
        # ---- CP part 3: digraph acyclic
        arcs = [(s, t) for s in P for t in P
                if s != t and ((B[s] >> t) & 1)]
        if has_cycle(sorted(P), arcs):
            cpfail.append(("acyclic",))
        # ---- CP part 4: P\U == inclusion-maximal carriers
        PminusU = set(s for s in P if not ((U >> s) & 1))
        maxi = set()
        for s in P:
            if not any(t != s and (A[s] & ~A[t]) == 0 and A[s] != A[t]
                       for t in P):
                maxi.add(s)
        if PminusU != maxi:
            cpfail.append(("PminusU", sorted(PminusU), sorted(maxi)))
        # ---- CP part 5: nonempty
        if not PminusU:
            cpfail.append(("nonempty",))
        # ---- ADJ: some q in Q has both F-neighbours in P\U
        adj_ok = False
        for q in Q:
            ends = [s for s in P if (s, q) in E]
            if len(ends) == 2 and ends[0] in PminusU and ends[1] in PminusU:
                adj_ok = True
        if cpfail:
            res["cp_fail"] += 1
        if not adj_ok:
            res["adj_fail"] += 1
        if pdis:
            res["pdis"] += 1
        res["detail"].append({
            "P": sorted(P), "Q": sorted(Q),
            "A": {str(s): mask_list(A[s]) for s in sorted(P)},
            "U": mask_list(U), "P_minus_U": sorted(PminusU),
            "arcs": arcs, "cp_fail": cpfail, "adj_ok": adj_ok,
            "pdis": pdis})
    return res


def mask_list(m):
    if m is None:
        return None
    return [i for i in range(m.bit_length()) if (m >> i) & 1]


def has_cycle(nodes, arcs):
    g = {v: [] for v in nodes}
    for a, b in arcs:
        g[a].append(b)
    color = {v: 0 for v in nodes}

    def dfs(v):
        color[v] = 1
        for w in g[v]:
            if color[w] == 1:
                return True
            if color[w] == 0 and dfs(w):
                return True
        color[v] = 2
        return False

    return any(color[v] == 0 and dfs(v) for v in nodes)


# ---------------------------------------------------------------- universe
def gen_exhaustive(maxK=3, maxP=5):
    """PREREG-CARRIER-POSET frozen universe:
    2<=|S|<=maxK, 3<=|H|<=maxP, every S-vertex has 2,3 or 4 H-neighbours
    (capped by |H|), every H-vertex incident, and either all capacities two
    or exactly one capacity-one pair."""
    for k in range(2, maxK + 1):
        for p in range(3, maxP + 1):
            cand = []
            for d in (2, 3, 4):
                if d <= p:
                    cand.extend(itertools.combinations(range(p), d))
            for nb in itertools.product(cand, repeat=k):
                cover = set()
                for x in nb:
                    cover |= set(x)
                if len(cover) != p:
                    continue
                yield Sys(nb, [2] * p)
                for (x, y) in itertools.combinations(range(p), 2):
                    cap = [2] * p
                    cap[x] = 1
                    cap[y] = 1
                    yield Sys(nb, cap)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if mode == "count":
        n = sum(1 for _ in gen_exhaustive())
        print("systems =", n)
        return
    systems = cyclic = pdis = cp_fail = adj_fail = 0
    nonuniq = 0
    first_adj = None
    first_cp = None
    for sysm in gen_exhaustive():
        systems += 1
        r = check_cp_adj(sysm)
        if r is None:
            continue
        cyclic += 1
        if not r["carrier_unique"]:
            nonuniq += 1
        cp_fail += 1 if r["cp_fail"] else 0
        adj_fail += 1 if r["adj_fail"] else 0
        pdis += 1 if r["pdis"] else 0
        if r["adj_fail"] and first_adj is None:
            first_adj = {"nb": [list(x) for x in sysm.nb], "cap": sysm.cap,
                         "detail": r["detail"]}
        if r["cp_fail"] and first_cp is None:
            first_cp = {"nb": [list(x) for x in sysm.nb], "cap": sysm.cap,
                        "detail": r["detail"]}
    print("TARGET systems=%d cyclic=%d pdis=%d CP_fail=%d ADJ_fail=%d "
          "carrier_nonunique=%d" %
          (systems, cyclic, pdis, cp_fail, adj_fail, nonuniq))
    if first_adj:
        print("FIRST_ADJ_FAIL", json.dumps(first_adj, sort_keys=True))
    if first_cp:
        print("FIRST_CP_FAIL", json.dumps(first_cp, sort_keys=True))


if __name__ == "__main__":
    main()
