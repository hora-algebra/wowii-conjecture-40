"""Post-holdout discovery mining of the n=10 data (order 2-6).
NOT a holdout: the primary C_R1 statement already passed its sealed n=10 test
(O-15). This pass dissects the mechanism.

Reuses the SAME frozen, dual-verified engine as eval_L1_holdout (feasible,
comps, ncyc, nbrs) so per-edge labels reconcile exactly with O-15
(R1=2,021,855 R2=761 R3=48,324). Adds:
  - R2 refinement: R2a (one-move plateau, same P) / R2b (one-move uphill only) /
    R2x (feasible completion exists but NOT reachable in one elementary move).
  - per-cycle cyclic word over {R1,R2a,R2b,R2x,R3,E} (E = the fixed edge e).
  - split of every cycle by whether it contains the fixed H-edge e=(x,y).
  - per-cycle booleans: all-R2, has-R2b, every-R2-adjacent-to-R1, max R2 run,
    max R3 run, mixed R2/R3, R1-free (expect 0), has-R1-path-exchange (S2).
  - one R1 witness per cycle component, re-validated by an INDEPENDENT E2
    validator written fresh below (feasibility, single simple alternating
    path/cycle, deg-2 on S, capacities, e fixed, P strictly smaller) — the
    cheap per-component dual-cert.
Outputs under wowii61-runs/: mine-n10-{progress,r2,cycles,summary}.txt
"""
import sys, subprocess
from collections import defaultdict, Counter
from itertools import combinations, product
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
from eval_L1_holdout import feasible, comps, ncyc, nbrs

R = "."
PROG = f"{R}/mine-n10-progress.txt"
R2F  = f"{R}/mine-n10-r2.txt"
CYC  = f"{R}/mine-n10-cycles.txt"
SUMM = f"{R}/mine-n10-summary.txt"

# ---------- INDEPENDENT E2 validator (does NOT use nbrs) ----------
def indep_feasible(n, adj, Sset, x, y, J):
    degS = defaultdict(int); degH = defaultdict(int)
    for (u, v) in J:
        if u not in Sset or v in Sset:      return False   # edge must be S->H
        if not (adj[u] >> v & 1):           return False   # real graph edge
        degS[u] += 1; degH[v] += 1
    for s in Sset:
        if degS[s] != 2:                    return False
    cap = {h: 2 for h in range(n) if h not in Sset}; cap[x] = 1; cap[y] = 1
    for h, d in degH.items():
        if d > cap.get(h, 0):               return False
    return True

def indep_ncyc(J, x, y):
    g = defaultdict(list)
    for (u, v) in list(J) + [(x, y)]:
        g[u].append(v); g[v].append(u)
    seen = set(); c = 0
    for s0 in list(g):
        if s0 in seen: continue
        comp = []; st = [s0]
        while st:
            u = st.pop()
            if u in seen: continue
            seen.add(u); comp.append(u); st += g[u]
        E = sum(len(g[u]) for u in comp) // 2
        if E == len(comp): c += 1
    return c

def e2_validate(n, adj, Sset, x, y, J, Jp):
    """Independently certify that Jp is a valid one-elementary-move R1 neighbor
    of J that releases at least one edge and strictly reduces P. Returns
    (ok, reason)."""
    if not indep_feasible(n, adj, Sset, x, y, Jp):      return False, "Jp-infeasible"
    D = set(J) ^ set(Jp)
    if not D:                                            return False, "empty-move"
    status = {z: ('J' if z in set(J) else 'P') for z in D}
    inc = defaultdict(list); av = defaultdict(set)
    for z in D:
        s, h = z; inc[s].append(z); inc[h].append(z); av[s].add(h); av[h].add(s)
    if any(len(v) > 2 for v in inc.values()):            return False, "deg>2"
    start = next(iter(inc)); seen = {start}; st = [start]
    while st:
        u = st.pop()
        for w in av[u]:
            if w not in seen: seen.add(w); st.append(w)
    if len(seen) != len(inc):                            return False, "disconnected"
    for vtx, es in inc.items():
        if len(es) == 2 and status[es[0]] == status[es[1]]:
            return False, "no-alternation"                # same status at deg-2 vertex
    d1 = [vtx for vtx, es in inc.items() if len(es) == 1]
    if len(d1) not in (0, 2):                             return False, "bad-endpoints"
    if any(vtx in Sset for vtx in d1):                   return False, "S-endpoint"
    if indep_ncyc(Jp, x, y) >= indep_ncyc(J, x, y):      return False, "P-not-smaller"
    return True, "ok"

# ---------- cyclic-order walk of a cycle component ----------
LAB = {'R1': '1', 'R2a': 'a', 'R2b': 'b', 'R2x': 'x', 'R3': '3', 'E': 'e'}

def walk_cycle(cc, J, x, y):
    """Return ordered list of edges around the single cycle spanning cc. Each
    entry is ('E', (x,y)) for the fixed edge or ('J', (s,h)) for a selected
    incidence edge."""
    ccset = set(cc)
    g = defaultdict(list)   # vertex -> list of (neighbor, edge-record)
    for (u, v) in J:
        if u in ccset and v in ccset:
            rec = ('J', (u, v)); g[u].append((v, rec)); g[v].append((u, rec))
    has_e = (x in ccset and y in ccset)
    if has_e:
        rec = ('E', (x, y)); g[x].append((y, rec)); g[y].append((x, rec))
    start = x if has_e else next(iter(ccset))
    order = []; prev = None; cur = start; used = set()
    while True:
        nxt = None
        for (w, rec) in g[cur]:
            if id(rec) in used: continue
            if w == prev and len([1 for (ww, rr) in g[cur] if ww == prev]) == 1:
                continue
            nxt = (w, rec); break
        if nxt is None:
            break
        w, rec = nxt; used.add(id(rec)); order.append(rec); prev = cur; cur = w
        if cur == start:
            break
    return order, has_e

def canon_word(chars):
    """Rotation+reflection-invariant canonical string of a cyclic label list."""
    s = ''.join(chars); n = len(s)
    if n == 0: return ''
    rots = [s[i:] + s[:i] for i in range(n)]
    r = s[::-1]; rots += [r[i:] + r[:i] for i in range(n)]
    return min(rots)

# ---------- per-edge label (reconciles with eval_L1_holdout) ----------
def label_edge(ed, J, fs, nb, P):
    if not any(ed not in Jp for Jp in fs):        return 'R3'    # no feasible completion
    rel = [Jp for Jp in nb if ed not in Jp]        # one-move neighbors dropping ed
    if rel and any(P[Jp] < P[J] for Jp in rel):   return 'R1'
    if not rel:                                    return 'R2x'
    m = min(P[Jp] for Jp in rel)
    return 'R2a' if m == P[J] else 'R2b'

def best_r1_neighbor(ed, J, nb, P):
    rel = [Jp for Jp in nb if ed not in Jp and P[Jp] < P[J]]
    if not rel: return None
    return min(rel, key=lambda Jp: P[Jp])

if __name__ == "__main__":
    for f in (PROG, R2F, CYC, SUMM):
        open(f, "w").close()
    open(R2F, "a").write("# R2 zoo (all releases labeled R2a/R2b/R2x). "
                         "cols: g6 | S | e=(x,y) | Jbitmask-edges | label | "
                         "cycle-word | contains-e\n")
    open(CYC, "a").write("# interesting cycles (all-R2 / has-R2b / mixed R2R3 / "
                         "R1-free) + word histograms at end\n")

    # counters
    tot_R1 = tot_R2a = tot_R2b = tot_R2x = tot_R3 = 0
    n_cyc_states = n_components = 0
    wit_ok = wit_fail = 0
    wit_is_path = wit_is_cycle = 0     # witness move shape (S2 evidence)
    fail_examples = []
    # per-cycle booleans
    c_allR2 = c_hasR2b = c_mixedR2R3 = c_R1free = c_everyR2adjR1 = 0
    c_has_e = c_no_e = 0
    c_hasR1_path = 0                   # S2: a cycle has an R1 whose move is a path
    maxrun_R2 = maxrun_R3 = 0
    word_hist_e = Counter(); word_hist_noe = Counter()
    smallest_R2 = None                 # (n_edges_state, detail)
    smallest_mixed = None

    NN = sys.argv[1] if len(sys.argv) > 1 else '10'
    gs = subprocess.run(['geng', '-bc', '-q', NN], capture_output=True, text=True).stdout.split()
    gi = 0
    for g6 in gs:
        gi += 1
        if gi % 100 == 0:
            open(PROG, "a").write(
                f"g {gi}/{len(gs)} cyc_states={n_cyc_states} comps={n_components} "
                f"R2a={tot_R2a} R2b={tot_R2b} R2x={tot_R2x} R3={tot_R3} "
                f"witOK={wit_ok} witFAIL={wit_fail}\n")
        nn, adj = inv_b.parse_g6(g6); k = EB.tau(nn, adj)
        if k < 2: continue
        for S in min_fvs_all(nn, adj, k):
            Sset = set(S); Hv = [v for v in range(nn) if v not in Sset]
            for (x, y) in [(u, w) for u in Hv for w in Hv if u < w and adj[u] >> w & 1]:
                feas = feasible(nn, adj, list(S), x, y)
                if not feas: continue
                fs = set(feas); P = {J: ncyc(J, (x, y)) for J in feas}
                for J in feas:
                    if P[J] == 0: continue
                    n_cyc_states += 1
                    nb = nbrs(fs, J, Sset)
                    for (cc, iscy) in comps(J, (x, y)):
                        if not iscy: continue
                        n_components += 1
                        order, has_e = walk_cycle(cc, J, (x, y)[0], (x, y)[1])
                        # label each edge of the cycle in cyclic order
                        labels = []
                        for (kind, edg) in order:
                            if kind == 'E':
                                labels.append('E'); continue
                            lab = label_edge(edg, J, fs, nb, P)
                            labels.append(lab)
                            if   lab == 'R1':  tot_R1  += 1
                            elif lab == 'R2a': tot_R2a += 1
                            elif lab == 'R2b': tot_R2b += 1
                            elif lab == 'R2x': tot_R2x += 1
                            elif lab == 'R3':  tot_R3  += 1
                        chars = [LAB[l] for l in labels]
                        word = canon_word(chars)
                        (word_hist_e if has_e else word_hist_noe)[word] += 1
                        if has_e: c_has_e += 1
                        else:     c_no_e += 1
                        # per-cycle booleans over J-edges (ignore 'E')
                        jl = [l for l in labels if l != 'E']
                        has1  = any(l == 'R1' for l in jl)
                        has3  = any(l == 'R3' for l in jl)
                        has2  = any(l in ('R2a', 'R2b', 'R2x') for l in jl)
                        has2b = any(l == 'R2b' for l in jl)
                        if not has1: c_R1free += 1
                        if has2 and not has1: c_allR2 += 1
                        if has2 and has3: c_mixedR2R3 += 1
                        if has2b: c_hasR2b += 1
                        # cyclic-adjacency: every R2 edge adjacent to an R1 edge
                        m = len(labels)
                        if has2:
                            alladj = True
                            for i, l in enumerate(labels):
                                if l in ('R2a', 'R2b', 'R2x'):
                                    lft = labels[(i - 1) % m]; rgt = labels[(i + 1) % m]
                                    if lft != 'R1' and rgt != 'R1':
                                        alladj = False; break
                            if alladj: c_everyR2adjR1 += 1
                        # max consecutive R2 / R3 runs (cyclic)
                        def maxrun(pred):
                            if not any(pred(l) for l in labels): return 0
                            if all(pred(l) for l in labels): return len(labels)
                            best = cur = 0
                            for l in labels + labels:  # cyclic
                                cur = cur + 1 if pred(l) else 0
                                best = max(best, cur)
                            return min(best, len(labels))
                        maxrun_R2 = max(maxrun_R2, maxrun(lambda l: l in ('R2a','R2b','R2x')))
                        maxrun_R3 = max(maxrun_R3, maxrun(lambda l: l == 'R3'))

                        # ---- one R1 witness for this component, independently validated ----
                        wit_edge = None
                        for (kind, edg), lab in zip(order, labels):
                            if kind == 'J' and lab == 'R1':
                                wit_edge = edg; break
                        if wit_edge is not None:
                            Jp = best_r1_neighbor(wit_edge, J, nb, P)
                            if Jp is None:
                                wit_fail += 1
                                if len(fail_examples) < 20:
                                    fail_examples.append((g6, "no-best-nbr", str(sorted(J))))
                            else:
                                ok, why = e2_validate(nn, adj, Sset, x, y, J, Jp)
                                if ok:
                                    wit_ok += 1
                                    D = set(J) ^ set(Jp)
                                    d1 = sum(1 for vtx in set(v for z in D for v in z)
                                             if sum(1 for z in D if vtx in z) == 1)
                                    if d1 == 2: wit_is_path += 1
                                    else:       wit_is_cycle += 1
                                    if d1 == 2 and has1:
                                        c_hasR1_path += 1
                                else:
                                    wit_fail += 1
                                    if len(fail_examples) < 20:
                                        fail_examples.append((g6, why, str(sorted(J))))

                        # ---- dump R2 releases and interesting cycles ----
                        if has2:
                            estr = str(sorted((sorted(x) for x in J)))[:200]
                            for (kind, edg), lab in zip(order, labels):
                                if kind == 'J' and lab in ('R2a', 'R2b', 'R2x'):
                                    open(R2F, "a").write(
                                        f"{g6} | S={sorted(Sset)} | e={(x,y)} | "
                                        f"edge={edg} | {lab} | word={word} | e_in_cycle={has_e}\n")
                            nedges = len(J)
                            if smallest_R2 is None or nedges < smallest_R2[0]:
                                smallest_R2 = (nedges, f"{g6} S={sorted(Sset)} e={(x,y)} word={word}")
                        if has2 and not has1:
                            open(CYC, "a").write(f"ALL-R2 cycle: {g6} S={sorted(Sset)} "
                                                 f"e={(x,y)} word={word}\n")
                        if has2b:
                            open(CYC, "a").write(f"R2b cycle: {g6} S={sorted(Sset)} "
                                                 f"e={(x,y)} word={word}\n")
                        if has2 and has3:
                            if smallest_mixed is None or len(J) < smallest_mixed[0]:
                                smallest_mixed = (len(J), f"{g6} S={sorted(Sset)} e={(x,y)} word={word}")
                        if not has1:
                            open(CYC, "a").write(f"*** R1-FREE cycle (violates C_R1): "
                                                 f"{g6} S={sorted(Sset)} e={(x,y)} word={word}\n")

    # ---- summary ----
    with open(SUMM, "a") as f:
        f.write("=== mine_n10 DISCOVERY SUMMARY (n=10) ===\n")
        f.write(f"cyclic_states={n_cyc_states} cycle_components={n_components}\n")
        f.write(f"per-edge labels: R1={tot_R1} R2a={tot_R2a} R2b={tot_R2b} "
                f"R2x={tot_R2x} R3={tot_R3}\n")
        f.write(f"  R2 total (R2a+R2b+R2x)={tot_R2a+tot_R2b+tot_R2x} "
                f"(O-15 expected 761); R3={tot_R3} (expected 48324); "
                f"R1={tot_R1} (expected 2021855)\n")
        f.write(f"cycles containing e: {c_has_e}; not containing e: {c_no_e}\n")
        f.write(f"per-cycle booleans: R1-free={c_R1free} (expect 0)  "
                f"all-R2={c_allR2}  has-R2b={c_hasR2b}  mixed-R2/R3={c_mixedR2R3}  "
                f"every-R2-adjacent-to-R1={c_everyR2adjR1}\n")
        f.write(f"max consecutive R2 run={maxrun_R2}  max consecutive R3 run={maxrun_R3}\n")
        f.write(f"witness dual-cert: OK={wit_ok} FAIL={wit_fail}  "
                f"(move shape: path={wit_is_path} cycle={wit_is_cycle}); "
                f"cycles with an R1 PATH-exchange (S2)={c_hasR1_path}\n")
        f.write(f"smallest R2 state: {smallest_R2}\n")
        f.write(f"smallest mixed R2/R3 cycle: {smallest_mixed}\n")
        if fail_examples:
            f.write("WITNESS FAILURES (first 20):\n")
            for e in fail_examples:
                f.write(f"  {e}\n")
        f.write("--- cycle-word histogram (contains e), top 40 ---\n")
        for w, c in word_hist_e.most_common(40):
            f.write(f"  {w}: {c}\n")
        f.write("--- cycle-word histogram (no e), top 40 ---\n")
        for w, c in word_hist_noe.most_common(40):
            f.write(f"  {w}: {c}\n")
    print("mine_n10 DONE")
