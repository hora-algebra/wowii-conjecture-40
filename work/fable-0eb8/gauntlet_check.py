#!/usr/bin/env python3
"""Independent gauntlet verification for attempt/2026-08-04-claude-fable-5-0eb8.

Written from the paper's definitions (v2 paper.tex) without consulting any
prior attempt's checker code. Recomputes, for each warning witness
(O-56, O-63, O-64) and for the abstract even-cycle system:

  - all feasible selections of the incidence model (demand 2 per s,
    capacity c(h)=2 except c=1 on the endpoints of the distinguished edge);
  - the forced core (intersection of all feasible selections);
  - rho(X) and Hall feasibility / tightness for every X subset of S;
  - tau(G[H u X]) (exact minimum FVS of the induced subgraph) for every X;
  - inclusion-minimal tight exposing sets (canonical carriers A_s);
  - the specific mechanism claims each witness is recorded to support.

Everything is asserted; any mismatch raises.
"""
import itertools, json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "..", "..", "tools", "witnesses")


def norm(v):
    return str(v)


class Instance:
    def __init__(self, S, H, inc, forest, e1):
        # S, H: lists of vertex names (strings). inc: list of (s,h) incidences.
        # forest: list of (h,h') H-edges. e1: pair of H-vertices with capacity 1.
        self.S = [norm(x) for x in S]
        self.H = [norm(x) for x in H]
        self.inc = [(norm(a), norm(b)) for a, b in inc]
        self.forest = [(norm(a), norm(b)) for a, b in forest]
        self.e1 = frozenset(norm(x) for x in e1) if e1 else frozenset()
        self.cap = {h: (1 if h in self.e1 else 2) for h in self.H}
        self.nbr = {s: [h for (a, h) in self.inc if a == s] for s in self.S}

    # ---- feasible selections ----
    def feasible_selections(self):
        """All maps s -> 2-subset of N(s) with every h-load <= cap."""
        out = []
        choices = []
        for s in self.S:
            opts = list(itertools.combinations(sorted(self.nbr[s]), 2))
            choices.append(opts)
        for combo in itertools.product(*choices):
            load = {}
            ok = True
            for pair in combo:
                for h in pair:
                    load[h] = load.get(h, 0) + 1
                    if load[h] > self.cap[h]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                out.append({s: set(p) for s, p in zip(self.S, combo)})
        return out

    def forced_core(self, sels):
        """Intersection of all feasible selections, as a set of (s,h) edges."""
        core = None
        for J in sels:
            edges = {(s, h) for s in self.S for h in J[s]}
            core = edges if core is None else (core & edges)
        return core or set()

    # ---- Hall / tightness ----
    def rho(self, X):
        Xs = set(X)
        tot = 0
        for h in self.H:
            d = sum(1 for s in Xs if h in self.nbr[s])
            tot += min(self.cap[h], d)
        return tot

    def tight_sets(self):
        return [set(X) for r in range(len(self.S) + 1)
                for X in itertools.combinations(self.S, r)
                if self.rho(X) == 2 * len(X)]

    def hall_ok(self):
        return all(self.rho(X) >= 2 * len(X)
                   for r in range(len(self.S) + 1)
                   for X in itertools.combinations(self.S, r))

    def exposes(self, X, s, h):
        Xs = set(X)
        if s not in Xs:
            return False
        d = sum(1 for t in Xs if h in self.nbr[t])
        return d <= self.cap[h]

    def carrier(self, s, forced_edges):
        """Inclusion-minimal tight set containing s exposing every forced
        incidence at s (paper Lemma 4.3 says it is unique)."""
        mine = [(a, h) for (a, h) in forced_edges if a == s]
        best = None
        for X in self.tight_sets():
            if s in X and all(self.exposes(X, s, h) for (_, h) in mine):
                if best is None or len(X) < len(best):
                    best = X
        # verify uniqueness at minimum size
        cnt = sum(1 for X in self.tight_sets()
                  if s in X and all(self.exposes(X, s, h) for (_, h) in mine)
                  and len(X) == len(best))
        assert cnt == 1, f"carrier not unique for {s}"
        return best

    # ---- the induced graph G[H u X] and exact FVS ----
    def graph_edges(self, X):
        Xs = set(X)
        E = [tuple(e) for e in self.forest]
        E += [(s, h) for (s, h) in self.inc if s in Xs]
        V = set(self.H) | Xs
        return V, E

    @staticmethod
    def is_forest(V, E):
        parent = {v: v for v in V}

        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for a, b in E:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
        return True

    def tau_induced(self, X):
        """Exact FVS number of G[H u X] by subset enumeration."""
        V, E = self.graph_edges(X)
        Vl = sorted(V)
        for k in range(len(Vl) + 1):
            for D in itertools.combinations(Vl, k):
                Ds = set(D)
                E2 = [(a, b) for (a, b) in E if a not in Ds and b not in Ds]
                V2 = V - Ds
                if self.is_forest(V2, E2):
                    return k
        raise RuntimeError


def load(name):
    with open(os.path.join(WIT, name)) as f:
        return json.load(f)


def check_o56():
    j = load("O-56.json")
    v = j["vertices"]
    inst = Instance(v["S"], v["H"], j["incidence_edges_S_H"],
                    j["H_forest_edges"], j["distinguished_edge"])
    sels = inst.feasible_selections()
    assert len(sels) == 1, len(sels)
    uniq = {norm(k): set(norm(x) for x in vv)
            for k, vv in j["feasible_selections"]["unique"].items()}
    assert sels[0] == uniq
    core = inst.forced_core(sels)
    want = {(norm(a), norm(b)) for a, b in j["forced_core_edges"]}
    assert core == want, (core, want)          # 8 edges (VERIFY-1 corrected)
    assert len(core) == 8
    # forced 4-cycle 0-4-1-5
    cyc = {(norm(a), norm(b)) for a, b in j["forced_cycle"]["edges"]}
    assert cyc <= core
    # Hall feasibility holds globally
    assert inst.hall_ok()
    # hereditary tightness: singletons fine, first violation X={2,3}, tau=1
    for s in inst.S:
        assert inst.tau_induced({s}) == 1
    assert inst.tau_induced({"2", "3"}) == 1          # < 2: the violation
    assert inst.tau_induced({"0", "1"}) == 2          # P itself is clean
    assert inst.tau_induced(set(inst.S)) == 2         # tau(G[HuS]) = 2 < 4=|S|
    # carriers: A_0 = {0,2,3}, A_1 = {1,2,3}
    assert inst.carrier("0", core) == {"0", "2", "3"}
    assert inst.carrier("1", core) == {"1", "2", "3"}
    # single-blocker mechanism: FVS witness {6} kills G[H u {2,3}]
    V, E = inst.graph_edges({"2", "3"})
    E2 = [(a, b) for (a, b) in E if a != "6" and b != "6"]
    assert Instance.is_forest(V - {"6"}, E2)
    print("O-56 OK: unique selection, 8 forced edges, forced 4-cycle,"
          " violation {2,3} (tau 1) disjoint from P={0,1}, blocker {6},"
          " tau(G[HuS])=2<4, A_0={0,2,3}")


def check_o63():
    j = load("O-63.json")
    v = j["vertices"]
    inst = Instance(v["S"], v["H"], j["incidence_edges_S_H"],
                    j["H_forest_edges"], j["distinguished_edge"])
    sels = inst.feasible_selections()
    assert len(sels) == 6, len(sels)
    core = inst.forced_core(sels)
    cyc = {(norm(a), norm(b)) for a, b in j["forced_cycle"]["edges"]}
    assert cyc <= core
    assert inst.hall_ok()
    # carrier of s and its puncture
    A_s = inst.carrier("s", core)
    assert A_s == {"s", "u", "a", "b"}
    assert inst.rho({"u", "a", "b"}) == 6            # B_s tight
    # every U_h vertex has incidence-degree 3
    for x in ("u", "a", "b"):
        assert len(inst.nbr[x]) == 3
    # hereditary violation is the FULL B_s (tau 2 < 3), pairs are clean
    for pair in itertools.combinations(["u", "a", "b"], 2):
        assert inst.tau_induced(set(pair)) == 2
    assert inst.tau_induced({"u", "a", "b"}) == 2
    # blocker {h,w} of size 2 works
    V, E = inst.graph_edges({"u", "a", "b"})
    for blocker in ({"h", "w"}, {"h", "z"}):
        E2 = [(x, y) for (x, y) in E if x not in blocker and y not in blocker]
        assert Instance.is_forest(V - blocker, E2)
    # ...but no SINGLE vertex is: tau=2 means no size-1 FVS
    assert inst.tau_induced(set(inst.S)) == 3        # 3 < 5 = |S|
    print("O-63 OK: 6 selections, forced 4-cycle, A_s={s,u,a,b},"
          " B_s={u,a,b} tight with all incidence-degree 3,"
          " violation = full B_s (tau 2), blocker size 2, tau(G[HuS])=3<5")


def check_o64():
    j = load("O-64.json")
    v = j["vertices"]
    inst = Instance(v["S"], v["H"], j["incidence_edges_S_H"],
                    j["H_forest_edges"], j["distinguished_edge"])
    sels = inst.feasible_selections()
    assert len(sels) == 1
    uniq = {norm(k): set(norm(x) for x in vv)
            for k, vv in j["feasible_selections"]["unique"].items()}
    assert sels[0] == uniq
    core = inst.forced_core(sels)
    cyc = {(norm(a), norm(b)) for a, b in j["forced_cycle"]["edges"]}
    assert cyc <= core
    assert inst.hall_ok()
    # B_s = {u} is Hall-tight yet hereditarily CLEAN: tau(G[Hu{u}])=1=|B_s|
    assert inst.rho({"u"}) == 2
    assert inst.tau_induced({"u"}) == 1
    # first violation on P = {s,t}: tau=1 < 2, FVS witness {q1}
    assert inst.tau_induced({"s", "t"}) == 1
    V, E = inst.graph_edges({"s", "t"})
    E2 = [(x, y) for (x, y) in E if x != "q1" and y != "q1"]
    assert Instance.is_forest(V - {"q1"}, E2)
    assert inst.tau_induced(set(inst.S)) == 2        # 2 < 3 = |S|
    print("O-64 OK: unique selection (u saturates capacity-1 h), forced"
          " 4-cycle, B_s={u} tight but clean, violation on P={s,t},"
          " tau(G[HuS])=2<3")


def check_even_cycle(m):
    """Abstract even-cycle system: S_i ~ {H_i, H_(i+1 mod m)}, all caps 2."""
    S = [f"s{i}" for i in range(m)]
    H = [f"h{i}" for i in range(m)]
    inc = [(f"s{i}", f"h{i}") for i in range(m)] + \
          [(f"s{i}", f"h{(i + 1) % m}") for i in range(m)]
    inst = Instance(S, H, inc, [], None)   # no forest edges, no capacity-1 pair
    # rho(X) = 2|X| for EVERY X: Hall-feasible with every set tight
    for r in range(m + 1):
        for X in itertools.combinations(S, r):
            assert inst.rho(X) == 2 * len(X)
    sels = inst.feasible_selections()
    assert len(sels) == 1                     # unique: everything selected
    core = inst.forced_core(sels)
    assert len(core) == 2 * m                 # the whole 2m-cycle is forced
    # G[H u S] is the cycle C_2m: FVS number 1 < m for m >= 2
    assert inst.tau_induced(set(S)) == 1
    print(f"even-cycle m={m} OK: rho(X)=2|X| all X, unique selection,"
          f" forced core = C_{2*m}, tau(G[HuS])=1<{m}")


if __name__ == "__main__":
    check_o56()
    check_o63()
    check_o64()
    for m in (2, 3, 4, 5):
        check_even_cycle(m)
    print("ALL GAUNTLET CHECKS PASS")
