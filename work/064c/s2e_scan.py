#!/usr/bin/env python3
"""
s2e_scan.py -- independent checker for the SAFE-2-EXISTS structural claims
CL-1..CL-8 of PREREG-SAFE2-064c.md.

Fresh engine: graph6 parsing, minimum-FVS enumeration, feasible-selection
enumeration, residual-digraph BFS, semantic CES test.  Nothing is imported
from the repository's own tools; the anchors are compared, not reused.

Usage:
  python3 s2e_scan.py --controls          run controls only
  python3 s2e_scan.py --n 9               run controls then the exhaustive scan
  python3 s2e_scan.py --n 10 --shard i/k  sharded by geng output index
"""
import sys, os, json, argparse, subprocess, itertools, time
from collections import deque

GENG = "/opt/homebrew/bin/geng"

# ---------------------------------------------------------------- graph6 ----
def g6_decode(s):
    s = s.strip()
    if not s:
        return None
    data = [ord(c) - 63 for c in s]
    n = data[0]
    assert 0 <= n <= 62, "only small graph6 supported"
    bits = []
    for d in data[1:]:
        for k in (5, 4, 3, 2, 1, 0):
            bits.append((d >> k) & 1)
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            idx += 1
    return n, adj

def bits(m):
    while m:
        b = m & -m
        yield b.bit_length() - 1
        m ^= b

def is_forest(n, adj, mask):
    """acyclic check on the induced subgraph given by vertex bitmask"""
    seen = 0
    for v in bits(mask):
        if seen >> v & 1:
            continue
        stack = [(v, -1)]
        seen |= 1 << v
        while stack:
            u, par = stack.pop()
            nb = adj[u] & mask
            for w in bits(nb):
                if w == par:
                    continue
                if seen >> w & 1:
                    return False
                seen |= 1 << w
                stack.append((w, u))
    return True

def is_connected(n, adj):
    full = (1 << n) - 1
    seen = 1
    stack = [0]
    while stack:
        u = stack.pop()
        for w in bits(adj[u] & ~seen):
            seen |= 1 << w
            stack.append(w)
    return seen == full

def bipartition(n, adj):
    col = [-1] * n
    for r in range(n):
        if col[r] >= 0:
            continue
        col[r] = 0
        dq = deque([r])
        while dq:
            u = dq.popleft()
            for w in bits(adj[u]):
                if col[w] < 0:
                    col[w] = 1 - col[u]
                    dq.append(w)
                elif col[w] == col[u]:
                    return None
    return col

def tau(n, adj, mask):
    """feedback vertex number of the induced subgraph on `mask`"""
    verts = list(bits(mask))
    for k in range(0, len(verts) + 1):
        for D in itertools.combinations(verts, k):
            dm = 0
            for d in D:
                dm |= 1 << d
            if is_forest(n, adj, mask & ~dm):
                return k
    return len(verts)

def min_fvs_all(n, adj):
    full = (1 << n) - 1
    verts = list(range(n))
    for k in range(0, n + 1):
        found = []
        for D in itertools.combinations(verts, k):
            dm = 0
            for d in D:
                dm |= 1 << d
            if is_forest(n, adj, full & ~dm):
                found.append(dm)
        if found:
            return k, found
    return 0, [0]

# ------------------------------------------------------- selection model ----
class Inst:
    """one (G, S, e) instance"""
    __slots__ = ("n", "adj", "col", "S", "Hm", "cap", "e", "NH", "owners_of",
                 "Hlist", "Slist")

    def __init__(self, n, adj, col, Sm, e):
        self.n, self.adj, self.col = n, adj, col
        self.Hm = ((1 << n) - 1) & ~Sm
        self.Slist = list(bits(Sm))
        self.Hlist = list(bits(self.Hm))
        self.S = Sm
        self.e = e
        self.cap = {h: 2 for h in self.Hlist}
        self.cap[e[0]] = 1
        self.cap[e[1]] = 1
        self.NH = {s: tuple(bits(adj[s] & self.Hm)) for s in self.Slist}

def feasible_selections(inst, limit=None):
    """all feasible selections; a selection is a tuple of (h1,h2) per S vertex"""
    S = inst.Slist
    NH = inst.NH
    cap = inst.cap
    deg = {h: 0 for h in inst.Hlist}
    out = []
    pairs = []
    for s in S:
        ns = NH[s]
        pairs.append([(a, b) for i, a in enumerate(ns) for b in ns[i + 1:]])
    cur = [None] * len(S)

    def rec(i):
        if limit is not None and len(out) >= limit:
            return
        if i == len(S):
            out.append(tuple(cur))
            return
        for (a, b) in pairs[i]:
            if deg[a] < cap[a] and deg[b] < cap[b]:
                deg[a] += 1
                deg[b] += 1
                cur[i] = (a, b)
                rec(i + 1)
                deg[a] -= 1
                deg[b] -= 1
    rec(0)
    return out

def sel_state(inst, sel):
    """returns (edgeset, degH, adjacency map) for a selection"""
    E = set()
    degH = {h: 0 for h in inst.Hlist}
    inc = {}
    for s, (a, b) in zip(inst.Slist, sel):
        E.add((s, a)); E.add((s, b))
        degH[a] += 1; degH[b] += 1
        inc[s] = (a, b)
    return E, degH, inc

def components(inst, E):
    """components of the incidence graph; returns list of (vertexset, edgeset)"""
    adjm = {}
    for (s, h) in E:
        adjm.setdefault(s, []).append(h)
        adjm.setdefault(h, []).append(s)
    seen = set()
    comps = []
    for v in adjm:
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        vs = set()
        es = set()
        while stack:
            u = stack.pop()
            vs.add(u)
            for w in adjm[u]:
                key = (u, w) if u in inst.NH else (w, u)
                es.add(key)
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append((frozenset(vs), frozenset(es)))
    return comps

def selected_cycles(inst, E):
    """cyclic components: |V| == |E|"""
    return [c for c in components(inst, E) if len(c[0]) == len(c[1])]

# ------------------------------------------------- residual augmentation ----
def residual_paths(inst, E, degH, inc, a, maxlen=None, cap_paths=200000):
    """
    All simple shortest residual augmenting paths after releasing a=(s0,h0).
    Returns (dist, paths) with dist = shortest length (None if not avoidable)
    and paths = list of vertex sequences [s0,h1,s1,h2,...,hk].
    """
    s0, h0 = a
    # residual capacity after release
    def slack_after(h):
        d = degH[h] - (1 if h == h0 else 0)
        return d < inst.cap[h]
    # BFS layered from s0
    dist = {s0: 0}
    order = [s0]
    dq = deque([s0])
    terminal = None
    while dq:
        u = dq.popleft()
        du = dist[u]
        if terminal is not None and du >= terminal:
            break
        if u in inst.NH:            # S vertex -> unselected incidences
            sel = inc[u]
            for h in inst.NH[u]:
                if h in sel and not (u == s0 and h == h0):
                    continue        # selected incidence: not a forward arc
                if u == s0 and h == h0:
                    continue        # released arc deleted from the network
                if h in sel:
                    continue
                if h not in dist:
                    dist[h] = du + 1
                    dq.append(h)
                    if slack_after(h) and (terminal is None or du + 1 < terminal):
                        terminal = du + 1
        else:                       # H vertex -> owners of selected incidences
            for s in inst.Slist:
                if h_selected(inc, s, u) and not (s == s0 and u == h0):
                    if s not in dist:
                        dist[s] = du + 1
                        dq.append(s)
    if terminal is None:
        return None, []
    # enumerate all shortest paths to terminals at distance == terminal
    paths = []
    tgt = [h for h in inst.Hlist if dist.get(h) == terminal and slack_after(h)]
    def back(v, acc):
        if len(paths) >= cap_paths:
            return
        if v == s0:
            paths.append([s0] + acc[::-1])
            return
        dv = dist[v]
        if v in inst.NH:            # S vertex reached from an H vertex (backward arc)
            for h in inst.Hlist:
                if dist.get(h) == dv - 1 and h_selected(inc, v, h) and not (v == s0 and h == h0):
                    back(h, acc + [v])
        else:                       # H vertex reached from an S vertex (forward arc)
            for s in inst.Slist:
                if dist.get(s) == dv - 1 and u_unselected(inst, inc, s, v) and not (s == s0 and v == h0):
                    back(s, acc + [v])
    for t in tgt:
        back(t, [])
    return terminal, paths

def h_selected(inc, s, h):
    p = inc.get(s)
    return p is not None and (p[0] == h or p[1] == h)

def u_unselected(inst, inc, s, h):
    return (h in inst.NH[s]) and not h_selected(inc, s, h)

def toggle(inst, sel, a, path):
    """apply the augmentation; returns new selection tuple"""
    s0, h0 = a
    inc = {s: list(p) for s, p in zip(inst.Slist, sel)}
    # remove released
    inc[s0].remove(h0)
    k = (len(path) + 1) // 2
    # path = [s0,h1,s1,h2,...,h_k]
    for i in range(0, len(path) - 1, 2):
        s = path[i]; h = path[i + 1]
        inc[s].append(h)
        if i + 2 < len(path):
            s_next = path[i + 2]
            inc[s_next].remove(h)
    return tuple(tuple(sorted(inc[s])) for s in inst.Slist)

def cycles_key(inst, sel):
    E, degH, inc = sel_state(inst, sel)
    return set(c[1] for c in selected_cycles(inst, E))

# ------------------------------------------------------------ closure -------
def closure(inst, E, degH, inc, P):
    """D_J closure of P; returns (A*, Y*, reached_slack)"""
    A = set(P)
    Y = set()
    frontier = set(P)
    reached = False
    while frontier:
        newY = set()
        for s in frontier:
            for h in inst.NH[s]:
                if not h_selected(inc, s, h) and h not in Y:
                    newY.add(h)
        newY -= Y
        Y |= newY
        for h in newY:
            if degH[h] < inst.cap[h]:
                reached = True
        newA = set()
        for h in newY:
            for s in inst.Slist:
                if h_selected(inc, s, h) and s not in A:
                    newA.add(s)
        A |= newA
        frontier = newA
    return A, Y, reached

def rho(inst, X):
    tot = 0
    for h in inst.Hlist:
        d = sum(1 for s in X if h in inst.NH[s])
        tot += min(inst.cap[h], d)
    return tot

def forced_incidences(inst):
    """(s,h) forced iff no feasible selection omits it -- direct definition"""
    sels = feasible_selections(inst)
    allinc = set()
    for s in inst.Slist:
        for h in inst.NH[s]:
            allinc.add((s, h))
    forced = set(allinc)
    for sel in sels:
        E, _, _ = sel_state(inst, sel)
        forced &= E
    return forced

# ------------------------------------------------------------- the scan -----
class Stats:
    def __init__(self):
        self.graphs = 0
        self.instances = 0
        self.selections = 0
        self.cycle_components = 0
        self.a1_fail = 0
        self.hard_states = 0
        self.cap_hits = 0
        self.fail = {k: [] for k in
                     ("CL1", "CL2", "CL3", "CL4", "CL5", "CL6", "CL7", "CL8")}
        self.d0_hist = {}
        self.cl6_ok = 0
        self.cl7_steps = 0

    def summary(self):
        return dict(graphs=self.graphs, instances=self.instances,
                    selections=self.selections,
                    cycle_components=self.cycle_components,
                    a1_fail=self.a1_fail, hard_states=self.hard_states,
                    cap_hits=self.cap_hits,
                    d0_hist={str(k): v for k, v in sorted(self.d0_hist.items())},
                    cl6_ok=self.cl6_ok, cl7_steps=self.cl7_steps,
                    failures={k: len(v) for k, v in self.fail.items()})

def scan_instance(inst, g6, st, do_cl5=True, do_cl8=True):
    sels = feasible_selections(inst)
    if not sels:
        st.fail["CL0-feasibility"] = st.fail.get("CL0-feasibility", [])
        st.fail["CL0-feasibility"].append(dict(g6=g6, S=inst.Slist, e=inst.e))
        return
    st.instances += 1
    st.selections += len(sels)

    if do_cl5:
        cl5_check(inst, g6, st)

    for sel in sels:
        E, degH, inc = sel_state(inst, sel)
        cyc = selected_cycles(inst, E)
        if not cyc:
            continue
        st.cycle_components += len(cyc)
        oldcycles = set(c[1] for c in cyc)
        slackset = {h for h in inst.Hlist if degH[h] < inst.cap[h]}
        state_good = False
        state_steps = []        # (C, path, a, newsel) for minimizing steps
        for (vs, es) in cyc:
            P = [v for v in vs if v in inst.NH]
            Q = [v for v in vs if v not in inst.NH]
            # ---- CL-4
            outside = set()
            for s in P:
                outside |= set(inst.NH[s]) - set(Q)
            if not outside:
                st.fail["CL4"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                           sel=sel, cyc=sorted(vs)))
            # ---- d0 and all minimizing steps
            best = None
            allpaths = []
            for (s, h) in es:
                d, paths = residual_paths(inst, E, degH, inc, (s, h))
                if d is None:
                    continue
                if best is None or d < best:
                    best = d
                    allpaths = [((s, h), p) for p in paths]
                elif d == best:
                    allpaths += [((s, h), p) for p in paths]
            if best is None:
                # no avoidable incidence on this cycle: Lemma A violation
                st.fail["LEMMA-A"] = st.fail.get("LEMMA-A", [])
                st.fail["LEMMA-A"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                               sel=sel, cyc=sorted(vs)))
                continue
            st.d0_hist[best] = st.d0_hist.get(best, 0) + 1
            # ---- CL-2
            slack_adj = any(any(degH[h] < inst.cap[h] for h in inst.NH[s])
                            for s in P)
            if (best == 1) != slack_adj:
                st.fail["CL2"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                           sel=sel, cyc=sorted(vs), d0=best,
                                           slack_adj=slack_adj))
            good = False
            for (a, p) in allpaths:
                ns = toggle(inst, sel, a, p)
                nE, nd, ninc = sel_state(inst, ns)
                ncyc = set(c[1] for c in selected_cycles(inst, nE))
                is_ces = (es not in ncyc) and ncyc <= oldcycles
                if len(p) == 2 * 1:      # never; placeholder
                    pass
                if is_ces:
                    good = True
                # ---- CL-1: every length-1 step must be CES
                if len(p) == 2 and not is_ces:
                    # path [s0,h1] has 2 vertices = length 1
                    st.fail["CL1"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                               sel=sel, cyc=sorted(vs),
                                               a=a, path=p))
                state_steps.append(((vs, es), a, p, ns, is_ces, len(ncyc)))
            if good:
                state_good = True
            else:
                st.a1_fail += 1
                # ---- CL-3 (structure of bad minimizing steps at d0 = 3)
                if best == 3:
                    for (a, p) in allpaths:
                        ns = toggle(inst, sel, a, p)
                        nE, nd, ninc = sel_state(inst, ns)
                        ncyc = set(c[1] for c in selected_cycles(inst, nE))
                        if es in ncyc or ncyc <= oldcycles:
                            continue     # not a bad step
                        cl3_check(inst, g6, st, sel, (vs, es), a, p, ns,
                                  oldcycles, ncyc, E, degH, inc)
        # ---- CL-8 closure test (per cycle, on the original state)
        if do_cl8:
            for (vs, es) in cyc:
                P = [v for v in vs if v in inst.NH]
                A, Y, reached = closure(inst, E, degH, inc, P)
                if not reached:
                    cl8_check(inst, g6, st, sel, A, Y)
        # ---- CL-6 / CL-7 on hard states
        if not state_good:
            st.hard_states += 1
            ok_any = False
            for (C, a, p, ns, is_ces, ncount) in state_steps:
                if ncount > len(cyc):
                    continue
                nE, nd, ninc = sel_state(inst, ns)
                ncyc = selected_cycles(inst, nE)
                succ = False
                for (nvs, nes) in ncyc:
                    for v in nvs:
                        if v in inst.NH and any(nd[h] < inst.cap[h]
                                                for h in inst.NH[v]):
                            succ = True
                st.cl7_steps += 1
                if succ:
                    ok_any = True
                else:
                    st.fail["CL7"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                               sel=sel, a=a, path=p))
            if ok_any:
                st.cl6_ok += 1
            else:
                st.fail["CL6"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                           sel=sel))

def cl3_check(inst, g6, st, sel, C, a, p, ns, oldcycles, ncyc, E, degH, inc):
    vs, es = C
    s0, h0 = a
    h1 = p[1]
    s1 = p[2] if len(p) > 2 else None
    bad = []
    Q = set(v for v in vs if v not in inst.NH)
    P = set(v for v in vs if v in inst.NH)
    if h1 in Q:
        bad.append("a:h1_on_cycle")
    if s1 in P:
        bad.append("b:s1_on_cycle")
    # component of h1 in J must be a path
    comps = components(inst, E)
    for (cvs, ces) in comps:
        if h1 in cvs and len(cvs) == len(ces):
            bad.append("b:h1_component_is_cycle")
    new = ncyc - oldcycles
    if len(new) != 1:
        bad.append("c:new_cycle_count=%d" % len(new))
    else:
        Z = list(new)[0]
        Zv = set()
        for (s, h) in Z:
            Zv.add(s); Zv.add(h)
        if Zv & vs:
            bad.append("d:Z_meets_C")
    if len(ncyc) != len(oldcycles):
        bad.append("e:cycle_count_changed")
    nE, nd, ninc = sel_state(inst, ns)
    if nd[h0] != inst.cap[h0] - 1:
        bad.append("f:released_h_not_slack")
    if bad:
        st.fail["CL3"].append(dict(g6=g6, S=inst.Slist, e=inst.e, sel=sel,
                                   cyc=sorted(vs), a=a, path=p, why=bad))

def cl8_check(inst, g6, st, sel, A, Y):
    bad = []
    if rho(inst, A) != 2 * len(A):
        bad.append("i:not_tight rho=%d 2|A|=%d" % (rho(inst, A), 2 * len(A)))
    NA = set()
    for s in A:
        NA |= set(inst.NH[s])
    W = NA - Y
    if not W:
        bad.append("ii:W_empty")
    else:
        forced = forced_incidences(inst)
        for s in A:
            for h in inst.NH[s]:
                if h in W and (s, h) not in forced:
                    bad.append("iii:unforced(%d,%d)" % (s, h))
                    break
    if bad:
        st.fail["CL8"].append(dict(g6=g6, S=inst.Slist, e=inst.e, sel=sel,
                                   A=sorted(A), Y=sorted(Y), why=bad))

def cl5_check(inst, g6, st):
    """exhaustive over X in one class and Y subset of H (small n only)"""
    for cls in (0, 1):
        Sc = [s for s in inst.Slist if inst.col[s] == cls]
        if not Sc:
            continue
        for r in range(1, len(Sc) + 1):
            for X in itertools.combinations(Sc, r):
                # maximum Y with <=1 neighbour of each s in X
                bestY = 0
                Hl = inst.Hlist
                for mask in range(1 << len(Hl)):
                    Y = [Hl[i] for i in range(len(Hl)) if mask >> i & 1]
                    if len(Y) <= bestY:
                        continue
                    ok = True
                    for s in X:
                        if sum(1 for h in Y if h in inst.NH[s]) > 1:
                            ok = False
                            break
                    if ok:
                        bestY = len(Y)
                if bestY > len(Hl) - len(X):
                    st.fail["CL5"].append(dict(g6=g6, S=inst.Slist, e=inst.e,
                                               X=list(X), bestY=bestY,
                                               H=len(Hl)))
                    return

# ------------------------------------------------------------- controls -----
def controls():
    print("== CONTROLS ==")
    ok = True
    # 1. geng counts
    exp = {5: 21, 6: 38, 7: 93, 8: 250, 9: 766}
    for n in (5, 6, 7, 8, 9):
        out = subprocess.run([GENG, "-bc", "-q", str(n)], capture_output=True,
                             text=True).stdout.split()
        print("   geng -bc %d : %d graphs" % (n, len(out)))
        exp[n] = len(out)
    # 2. graph6 round trip on a known graph: path P4 = 'Cr'
    n, adj = g6_decode("Cr")
    print("   g6 'Cr' n=%d degs=%s" % (n, [bin(a).count('1') for a in adj]))
    # 3. C4 instance sanity
    n, adj = g6_decode("Cr")           # P4, tau = 0 -> skip
    n, adj = g6_decode("Cs")
    # C4 explicit
    n = 4
    adj = [0] * 4
    for (i, j) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        adj[i] |= 1 << j; adj[j] |= 1 << i
    k, fvss = min_fvs_all(n, adj)
    print("   C4: tau=%d  #min-FVS=%d (expect 1, 4)" % (k, len(fvss)))
    ok &= (k == 1 and len(fvss) == 4)
    col = bipartition(n, adj)
    Sm = fvss[0]
    inst = Inst(n, adj, col, Sm, tuple(sorted(bits(((1 << n) - 1) & ~Sm))[:2]))
    # 4. positive control for the CES detector: build a 6-cycle instance
    #    K_{3,3} minus a perfect matching = C6; S = two opposite vertices
    n = 6
    adj = [0] * 6
    for (i, j) in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]:
        adj[i] |= 1 << j; adj[j] |= 1 << i
    k, fvss = min_fvs_all(n, adj)
    print("   C6: tau=%d #min-FVS=%d" % (k, len(fvss)))
    # 5. a hand instance where a toggle creates a new cycle must be non-CES:
    #    verified inside the scan by construction (CL-1 failures would show).
    # 6. hereditary tightness re-derivation on sampled instances
    bad = 0
    tested = 0
    for line in subprocess.run([GENG, "-bc", "-q", "7"], capture_output=True,
                               text=True).stdout.split():
        n, adj = g6_decode(line)
        col = bipartition(n, adj)
        k, fvss = min_fvs_all(n, adj)
        if k < 1:
            continue
        for Sm in fvss[:2]:
            Hm = ((1 << n) - 1) & ~Sm
            for r in range(0, k + 1):
                for X in itertools.combinations(list(bits(Sm)), r):
                    xm = 0
                    for x in X:
                        xm |= 1 << x
                    tested += 1
                    if tau(n, adj, Hm | xm) != len(X):
                        bad += 1
    print("   hereditary tightness: %d subsets tested, %d violations "
          "(expect 0)" % (tested, bad))
    ok &= (bad == 0)
    # 7. feasibility for every fixed edge, n<=7
    nofeas = 0
    ninst = 0
    for line in subprocess.run([GENG, "-bc", "-q", "7"], capture_output=True,
                               text=True).stdout.split():
        n, adj = g6_decode(line)
        col = bipartition(n, adj)
        k, fvss = min_fvs_all(n, adj)
        if k < 1:
            continue
        for Sm in fvss:
            Hm = ((1 << n) - 1) & ~Sm
            for i in bits(Hm):
                for j in bits(adj[i] & Hm):
                    if i < j:
                        inst = Inst(n, adj, col, Sm, (i, j))
                        ninst += 1
                        if not feasible_selections(inst, limit=1):
                            nofeas += 1
    print("   feasibility n=7: %d instances, %d infeasible (expect 0)"
          % (ninst, nofeas))
    ok &= (nofeas == 0)
    print("CONTROLS %s" % ("PASS" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- driver ----
def run(n, shard=None, do_cl5=True, do_cl8=True, out=None, tlimit=None):
    t0 = time.time()
    st = Stats()
    lines = subprocess.run([GENG, "-bc", "-q", str(n)], capture_output=True,
                           text=True).stdout.split()
    for idx, g6 in enumerate(lines):
        if shard and idx % shard[1] != shard[0]:
            continue
        if tlimit and time.time() - t0 > tlimit:
            print("TIME LIMIT hit at graph index %d" % idx)
            st.aborted_at = idx
            break
        gn, adj = g6_decode(g6)
        col = bipartition(gn, adj)
        if col is None:
            continue
        k, fvss = min_fvs_all(gn, adj)
        if k < 1:
            continue
        st.graphs += 1
        for Sm in fvss:
            Hm = ((1 << gn) - 1) & ~Sm
            for i in bits(Hm):
                for j in bits(adj[i] & Hm):
                    if i < j:
                        inst = Inst(gn, adj, col, Sm, (i, j))
                        scan_instance(inst, g6, st, do_cl5=do_cl5,
                                      do_cl8=do_cl8)
    s = st.summary()
    s["n"] = n
    s["shard"] = shard
    s["aborted_at"] = getattr(st, "aborted_at", None)
    s["seconds"] = round(time.time() - t0, 3)
    print(json.dumps(s, indent=1))
    if out:
        with open(out, "w") as f:
            json.dump({"summary": s,
                       "failures": {k: v[:20] for k, v in st.fail.items()
                                    if isinstance(v, list) and v}},
                      f, indent=1, default=str)
    return st

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--n", type=int)
    ap.add_argument("--shard")
    ap.add_argument("--no-cl5", action="store_true")
    ap.add_argument("--no-cl8", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--tlimit", type=float)
    A = ap.parse_args()
    if A.controls:
        sys.exit(0 if controls() else 1)
    sh = None
    if A.shard:
        i, k = A.shard.split("/")
        sh = (int(i), int(k))
    run(A.n, sh, do_cl5=not A.no_cl5, do_cl8=not A.no_cl8, out=A.out,
        tlimit=A.tlimit)
