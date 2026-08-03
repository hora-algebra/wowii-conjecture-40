# GAUNTLET — comprehension record

Branch `attempt/2026-08-03-claude-opus-5-5047`. Written per ATTACK.md Step 1,
before any new mathematics. Everything below is in my own words with the
derivations written out. Where I checked something against the oracle I say so
and give the command; where I only reasoned, I say that too.

Notation follows the paper: `G` bipartite with classes `L, R`; `S` a minimum
FVS; `H = G - S` (a forest, because deleting an FVS destroys all cycles);
`e = (x,y)` a fixed edge of `H`; each `s in S` has demand 2; each `h in H` has
capacity `c(h) = 2` except `c(x) = c(y) = 1`. A *feasible selection* `J` gives
each `s` two distinct `S`–`H` incidences respecting capacities. `tau = n - f`,
`o = n - b`, `ell = n - p`.
`rho(X) = sum_{h in H} min(c(h), deg_X(h))`, `delta(X) = rho(X) - 2|X|`.

---

## (i) The reduction chain of Theorem 3.13 — how A + B give the bipartite case

Target: `ell(G) >= 2 tau(G) + 1` for every connected nontrivial bipartite `G`.
(By Theorem 2.1 this is exactly Conjecture 40 restricted to bipartite `G`,
because `o = 0` there.)

**Step 0 — the case `tau = 0`.** Then `G` is a nontrivial connected forest, so
it has an edge `uv`. Take `{uv}` together with every other vertex as a trivial
one-vertex path: that is a spanning linear forest with `1 = 2*0 + 1` edges. Done
without any of the machinery.

So assume `tau >= 1` and fix a minimum FVS `S`, `|S| = tau >= 1`.

**Step 1 — `E(H)` is nonempty, so a distinguished edge exists.**
Suppose `E(H) = empty`. Pick any `s in S` and put `X = {s}`. In `G[H u {s}]`
the only edges are the incidences at `s` (there are no `H`–`H` edges by
assumption, and no other `S`-vertex is present), so `G[H u {s}]` is a star plus
isolated vertices — a forest. Hence `tau(G[H u {s}]) = 0`. But hereditary FVS
tightness (Lemma 3.3) gives `tau(G[H u {s}]) = |{s}| = 1`. Contradiction.
So `E(H) != empty`; fix `e = (x,y) in E(H)`.

*Role of hereditary tightness here:* it is the only thing that rules out
`E(H) = empty`. Note it uses minimality of `S`, not just that `S` is an FVS.

**Step 2 — a feasible selection exists for this `e`.**
This is Corollary 3.8, and it is where the two nontrivial auxiliary results
enter:

  * Lemma 3.4 (generalized Hall): a feasible selection exists iff
    `rho(X) >= 2|X|` for every `X subseteq S`. Proof is a min-cut computation:
    for a source–sink cut `(A,B)` with `X = S ∩ A`, the forward capacity is
    `2(|S|-|X|)` from the unsaturated source arcs, plus, for each `h`, the
    cheaper of `c(h)` (put `h` in `A`, pay its sink arc) and `deg_X(h)` (put `h`
    in `B`, pay the `X`-incidence arcs). So the cheapest cut with a given `X`
    is `2|S| + delta(X)`, the global min cut is `2|S| + min_X delta(X)`, and
    max-flow = `2|S|` iff `min_X delta(X) >= 0`.
  * Lemma 3.7 (rooted forest extension): for `X` independent inside one
    bipartition class, `tau(G[H u X]) <= floor(rho_e(X)/2)`.
  * Hereditary tightness again: `tau(G[H u X]) = |X|`.

  Combining: split an arbitrary `X subseteq S` as `X_L u X_R`. Every `h in H∩L`
  has neighbours only in `X_R` and vice versa, so the two summands of `rho_e`
  have disjoint supports and `rho_e(X) = rho_e(X_L) + rho_e(X_R)`. If
  `rho_e(X) < 2|X|` then one side, say `X_L`, has `rho_e(X_L) < 2|X_L|`, and
  Lemma 3.7 gives `tau(G[H u X_L]) <= floor(rho_e(X_L)/2) < |X_L|`,
  contradicting hereditary tightness. Hence `rho_e(X) >= 2|X|` for all `X` and
  every `e`, and Lemma 3.4 supplies a feasible selection.

  *Quantifier note (PROOFS.md B3′).* Theorem 3.13 needs an acyclic feasible
  selection for **some** `e`. Corollary 3.8 gives initial feasibility for
  **every** `e` — strictly stronger than needed, and not to be confused with
  the target quantifier.

**Step 3 — Lemma A converts "forced core acyclic" into "every selected cycle
has an avoidable incidence".**
Call an incidence *forced* if it lies in every feasible selection, *avoidable*
otherwise. Let `J` be a feasible selection and `C` a selected cycle of `J`
(a cyclic component of the incidence graph `J`). If every incidence of `C` were
forced, then `C` would be a cycle inside the forced core — contradicting
Lemma A. So `C` contains an avoidable incidence.

*Exact role of Lemma A:* it is used **only** to discharge the hypothesis of
Lemma B. It is not used anywhere else in the chain. If Lemma B were stated
unconditionally ("every selected cycle admits a CES toggle"), Lemma A would be
redundant. Conversely Lemma A alone gives nothing about descent.

**Step 4 — Lemma B supplies the descent step.** By Lemma B the cycle `C`
admits a CES toggle: a passage to a feasible `J'` in which `C` is no longer a
selected cycle and every selected cycle of `J'` was already one of `J`.

**Step 5 — descent terminates (Lemma 3.12).** A CES toggle removes one selected
cycle and creates none, so the number of selected cycles strictly decreases. It
is a nonnegative integer, so after finitely many toggles we reach a feasible
selection `J` with **no** selected cycle, i.e. `J` is acyclic as a graph.

  *Slack in the hypothesis.* Definition 3.2 flags this explicitly: strict
  decrease of the cycle count alone would already suffice for termination. The
  semantic "creates no new cycle" form is what the mechanism produces, not what
  the descent needs. So the true composite requirement is weaker than
  Lemma A + Lemma B; it is `F2` (see the closing remark).

**Step 6 — add the fixed edge back (Lemma 3.9, fixed-edge parity).**
`J u {e}` is acyclic iff `J` is. Reason: a cycle of `J u {e}` through `e` would,
on deleting `e`, leave an `x`–`y` path made of `S`–`H` incidences only. Such a
path alternates `H, S, H, S, ...`, hence has even length. But `x, y` are
adjacent in the bipartite graph `G`, so they lie in opposite classes, and every
`x`–`y` path in `G` has odd length. Contradiction. (Consequence: `e` is never
on a selected cycle, so the cycle bookkeeping can ignore it entirely.)

**Step 7 — the degree count turns acyclicity into a linear forest.**
In `J u {e}`: every `s in S` has degree exactly 2 (demand 2); every `h in H` has
degree at most `c(h) <= 2`; and `x, y` have `c = 1`, so after adding `e` their
degree is at most 2. An acyclic graph of maximum degree 2 is a disjoint union of
paths, i.e. a linear forest. Its vertex set is `S u H = V(G)`, so it spans, and
it has `2|S|` incidence edges plus `e`, i.e. `2|S| + 1` edges. Hence

    ell(G) >= 2|S| + 1 = 2 tau(G) + 1.

**Where each hypothesis is load-bearing.**

| ingredient | used for |
|---|---|
| `S` an FVS | `H` is a forest |
| `S` **minimum** | hereditary tightness (Lemma 3.3), hence Steps 1 and 2 |
| bipartiteness | Step 2 (`rho` splits by class; Lemma 3.7 needs `X` in one class) and Step 6 (parity) |
| Lemma 3.7 + 3.4 | Step 2, feasibility |
| **Lemma A** | Step 3 only: gives Lemma B its hypothesis |
| **Lemma B** | Step 4: the descent step |
| capacities `c(x)=c(y)=1` | Step 7 only: leaves room for `e` at `x, y` |

**Closing remark (what is really needed).** Unwinding Steps 3–5, all the
bipartite theorem needs is

> **F2.** For some `e in E(H)` there is an acyclic feasible selection.

Lemma A + Lemma B + descent is one route to `F2`; it is a *sufficient*
mechanism, not an equivalent reformulation.

**A reformulation of F2 I will use later** (elementary, derived here; I have not
seen it stated in the repo). In a feasible selection every `s` has degree
exactly 2, so suppressing each `s` — replacing the path `h - s - h'` by the edge
`{h, h'}` — is a homeomorphism of the incidence graph onto a multigraph `M` on
the vertex set `H`. Suppressing degree-2 vertices preserves cycles, so:

* selected cycles of `J` correspond exactly to cycles of `M` (a selected
  4-cycle `s - h - s' - h' - s` becomes a pair of parallel edges);
* `deg_M(h)` is exactly the load of `h`, so the capacity constraint says
  `deg_M(h) <= c(h) <= 2`.

Hence **F2 is equivalent to: choose, for each `s in S`, an unordered pair
`sigma(s)` of distinct `H`-neighbours of `s`, so that the `|S|` chosen pairs are
pairwise distinct and form a *linear forest* on the vertex set `H`, with `x` and
`y` of degree at most 1.** Adding `e = xy` to that linear forest is then legal
and acyclic by Step 6, and subdividing each chosen pair by its `s` recovers the
spanning linear forest of `G` with `2|S| + 1` edges.

Two immediate consequences of the reformulation, both used below:

* *(cycle-count identity)* Let `d_1` be the number of `H`-vertices of load 1
  and `C` the number of connected components of the graph formed by the selected
  incidences (equivalently of `M`). Then the number of selected cycles is
  `C - d_1/2`. (From `d_1 + 2 d_2 = 2|S|` and cycle rank
  `= |E| - |V| + C`.) So acyclicity is exactly "`|S| + 1` or more distinct
  `H`-vertices get used, in the right pattern".
* *(matroid shape)* "Distinct pairs, one per `s`" is independence in a
  transversal matroid on the candidate `H`-edges; "forest" is the graphic
  matroid on `H`. Their intersection is tractable — but the extra degree bound
  `deg <= 2` is **not** a matroid constraint (standard counterexample: on the
  path `a-b-c-d` with `c(b) = c(c) = 1`, `{bc}` is maximal of size 1 while
  `{ab, cd}` has size 2), which is exactly why F2 is not a two-matroid
  intersection and why the descent is needed.

---

## (ii) Why Hall feasibility alone cannot give Lemma A: the abstract even cycle

**The system.** Fix `m >= 2`. Let `S = {s_1, ..., s_m}` and
`H = {h_1, ..., h_m}` (indices mod `m`), with `s_i` adjacent to `h_i` and
`h_{i+1}` and nothing else. Demands 2, all capacities 2 (this is the
all-capacity-2 model; see the remark at the end of this section for why it is a
legitimate special case).

**It is Hall feasible, and in fact every set is tight.** Each `h_j` has exactly
two `S`-neighbours, `s_{j-1}` and `s_j`, so `deg_X(h_j) <= 2` for every
`X subseteq S` and therefore `min(2, deg_X(h_j)) = deg_X(h_j)`. Summing,

    rho(X) = sum_j deg_X(h_j) = sum_{s in X} deg_H(s) = 2|X|.

So `delta(X) = 0` for **every** `X subseteq S`: Hall's condition holds with
equality everywhere, and the tight-set lattice (Lemma 3.6) is the full Boolean
lattice. Nothing about submodularity or the flow structure is violated.

**Its forced core is a cycle.** Each `s_i` has exactly two `H`-neighbours and
demand 2, so it must select both. The unique feasible selection is therefore all
`2m` incidences, and the forced core is the whole `2m`-cycle
`s_1 h_2 s_2 h_3 ... s_m h_1 s_1`.

**Where it fails.** Realize the system as a graph with `H` independent
(no `H`–`H` edges). Then `G[H u S]` *is* the `2m`-cycle, whose minimum FVS has
size 1. So

    tau(G[H u S]) = 1 < m = |S|   for every m >= 2,

i.e. hereditary FVS tightness fails at `X = S`, and equivalently `S` is not a
minimum FVS of `G` (a single vertex is). The system is not a legal Lemma-A
instance.

**Conclusion.** `rho >= 2|.|` (Hall), submodularity of `delta`, the tight-set
lattice, and the F1 characterization "forced ⟺ tight-set exposed" are all
present in this system, and they permit a cyclic forced core. Therefore
Lemma A cannot be a consequence of the flow/Hall layer alone. Lemma A is
**exactly** the implication

    tau(G[H u X]) = |X| for every X subseteq S   ==>   forced core acyclic,

and the hypothesis on the left is the only extra input available. This also
tells you what a proof must look like: it must convert a forced cycle into an
`X subseteq S` and an FVS of `G[H u X]` of size `< |X|` (or into a feasible
exchange), i.e. it must touch the forest geometry of `H`, which `rho` cannot
see. (`rho` depends only on the incidence degrees and capacities; the abstract
even cycle and a hereditarily tight instance can have identical `rho` data and
different `H`-forests.)

*Remark on the all-capacity-2 model.* The abstract system has no
capacity-1 pair. That is legitimate: Lemma A° is stated for possibly
disconnected `G`, and in `G' = G ⊔ K_2` with `e` the `K_2` edge, the two
capacity-1 vertices are the `K_2` endpoints, which carry no incidences, so the
`G`-part of the system runs at all capacities 2. I checked the converse
direction too, so that no one mistakes this for an untested gap: raising
capacities only *enlarges* the feasible set, so
`forced(all caps 2) subseteq forced(caps for e)` for every `e in E(H)`; hence
acyclicity of the forced core for one `e` already implies it for all caps 2, and
Lemma A° carries no content beyond the connected fixed-edge statement.

---

## (iii) The three warning witnesses: what each kills, and by what mechanism

I re-derived all three from their JSON certificates with freshly written code
(`work/wcheck.py`, no shared code with `tools/`): bipartiteness, `H` a forest,
the complete feasible-selection set by brute force, the forced core as the
intersection of all feasible selections, its cycle rank by union–find, `rho` and
all Hall-tight sets, the canonical carriers `A_s` (verified to be the unique
minimum tight set containing `s`), the punctures `B_s`, and
`tau(G[H u X])` for **every** `X subseteq S`. Every recorded value reproduced.

Command:
`cd work && python3 wcheck.py ../tools/witnesses/O-56.json ../tools/witnesses/O-63.json ../tools/witnesses/O-64.json`

First, the fact that makes all three legal: **none of them is a counterexample
to Lemma A°**, because in each one hereditary tightness fails. Measured:

| witness | `tau(G[H u S])` | `|S|` | forced-core cycle rank |
|---|---|---|---|
| O-56 | 2 | 4 | 1 |
| O-63 | 3 | 5 | 1 |
| O-64 | 2 | 3 | 1 |

So in each case `S` is *not* a minimum FVS of `G`, the Lemma-A hypothesis is
absent, and the forced cycle is permitted. Each witness is used only to refute a
proposed rule for *where* the hereditary violation must sit.

### O-56 — kills P-localization; the acyclic-quotient / single-blocker normal form

`S = {0,1,2,3}` with `P = {0,1}` and auxiliaries `{2,3}`;
`H = {4,...,13}`; incidences `0,1 ~ 4,5,6`, `2 ~ 6,7`, `3 ~ 6,8`;
`H`-forest `9-4, 9-5, 4-10, 10-11, 6-12, 12-7, 6-13, 13-8`; `e = (10,11)`
(a pendant path, so `x = 10, y = 11` carry no incidences).

*Mechanism of the forcing.* Vertices 2 and 3 each have exactly two
`H`-neighbours, so they are rigid: `2 -> {6,7}`, `3 -> {6,8}`. Together they put
load 2 on the capacity-2 vertex 6, saturating it. So 0 and 1 cannot use 6 and
are pushed onto `{4,5}` — the unique feasible selection, whose forced core
contains the 4-cycle `0-4-1-5-0`. (Verified: 1 feasible selection, all 4 cycle
edges forced.)

*What it kills.* Measured hereditary profile: `tau({0}) = tau({1}) = 1`,
`tau({0,1}) = 2`. So **`P` and every subset of `P` is hereditarily tight**, and
the inclusion-minimal violation is `X = {2,3}` with `tau = 1 < 2` (FVS `{6}`),
which is **disjoint from `P`**. Therefore the route "a forced cycle with
`S`-side `P` forces a small FVS inside `G[H u P]`" (the CVB / P-local bridge) is
false: you cannot localize the contradiction to `P`.

*Its positive content.* It is the single-blocker subcase of Lemma 4.6:
the external `H`-neighbour of `0` is `h = 6` with `c(h) = 2`, the carrier is
`A_0 = {0,2,3}` (verified minimum tight containing 0), the puncture
`B_0 = {2,3}` is tight, and `U_h = N(6) ∩ B_0 = {2,3}`. Each of 2 and 3 has
exactly one `H`-neighbour besides 6 (namely 7 and 8), so deleting 6 leaves every
`U_h`-vertex of degree `<= 1` and `H - 6` a forest; `{6}` is an FVS of
`G[H u U_h]` of size `1 < 2 = |U_h|`. The forest quotient `M_6(U_h)` is
**acyclic**. This is exactly the shape of the proved subcase — it shows the
subcase is nonempty, and it is also the instance from which the (false)
degree-2 normal form below was generalized.

### O-63 — kills the degree-2 normal form and "degree >= 3 ⇒ private cycle"

`S = {s,t,u,a,b}`; `H = {r,x,q1,q2,h,w,z,y}`; `H`-tree
`r-q1, r-q2, r-h, r-w, r-z, q1-x, x-y`; `e = (x,y)`; incidences
`s ~ q1,q2,h`; `t ~ q1,q2`; `u,a,b ~ h,w,z`.

*Mechanism of the forcing.* `u,a,b` have total demand 6 and their only outlets
are `h,w,z` with total capacity 6, so `{u,a,b}` saturates all three. Hence `s`
cannot use `h` and is pushed onto `{q1,q2}`; `t` is rigid on `{q1,q2}`. The
4-cycle `s-q1-t-q2-s` is forced. (Verified: 6 feasible selections, all 4 cycle
edges in the intersection.)

*Carrier data (verified).* `A_s = {s,u,a,b}` (`rho = 8 = 2|A_s|`, and it is
contained in every tight set containing `s`), `B_s = {u,a,b}` tight,
`U_h = N(h) ∩ B_s = {u,a,b}`, and **every** vertex of `U_h` has incidence-degree
3 (`h, w, z`).

*What it kills.*
1. "Every vertex of `B_s` has incidence-degree 2" — **false** here; all three
   have degree 3. So the O-56 normal form is not universal, and the proof of the
   single-blocker subcase (which needs `<= 1` non-`h` neighbour per `U_h`
   vertex) does not apply.
2. "A `U_h`-vertex of incidence-degree `>= 3` has a private cycle avoiding `h`"
   — **false in general**, and this witness shows why the correct statement is
   a *quotient* condition. `H - h` is a single component (`r` links
   `q1, q2, w, z`, and `q1-x-y` hangs off it), so each of `u, a, b` has both of
   its non-`h` neighbours (`w` and `z`) in the *same* component: the quotient
   multigraph `M_h(U_h)` has parallel edges and is **cyclic**. Deleting `h`
   alone does **not** leave a forest. The correct criterion is
   `G[H u Y] - h` is a forest **iff** the (augmented) quotient
   `Mhat_h(Y)` is acyclic; incidence-degree `>= 3` matters only when two of the
   vertex's non-`h` neighbours share a component of `H - h`.
3. Consequently the *blocker can exceed a single external vertex*: measured, the
   inclusion-minimal hereditary violation is the **full** `B_s = {u,a,b}` with
   `tau = 2 < 3` and blocker `{h,w}` (or `{h,z}`) of size 2. Every pair inside
   `{u,a,b}` is tight (`tau = 2`); the violation appears only at size 3.

So O-56 and O-63 together bracket the capacity-2 branch: the violation *can* sit
inside `B_s`, but neither the degree hypothesis nor the blocker size of the
O-56 normal form survives.

### O-64 — kills `B_s`-localization; capacity-1 is a separate branch

`S = {s,t,u}`; `H = {q1,q2,r,y,h,w}`; `H`-tree `q1-r, r-q2, q1-y, y-h, y-w`;
`e = (h,y)` so `c(h) = c(y) = 1`; incidences `s ~ q1,q2,h`; `t ~ q1,q2`;
`u ~ h,w`.

*Mechanism of the forcing.* `u` has exactly two `H`-neighbours, so it is rigid:
`u -> {h,w}`. That puts load 1 on `h`, whose capacity is **1** (it is an
endpoint of the fixed edge). So `h` is saturated by a single user, `s` is pushed
off `h` onto `{q1,q2}`, `t` is rigid there, and `s-q1-t-q2-s` is forced.
(Verified: exactly 1 feasible selection.)

*What it kills.* Measured: `A_s = {s,u}`, `B_s = {u}`, `B_s` is Hall-tight, and

    tau(G[H u B_s]) = 1 = |B_s| ,

because `u` closes its own cycle `u-h-y-w-u` in `G[H u {u}]`, which needs one
vertex of its own. So `B_s` carries **no** hereditary violation, no subset of
`B_s` does, and (verified: the feasible selection is unique) there is **no**
feasible exchange avoiding a forced cycle edge. The first hereditary violation
is on the cycle's own `S`-side: `tau(G[H u P]) = 1 < 2` for `P = {s,t}`
(delete `q1`).

Hence:
* the "Punctured-Carrier Lemma" (violation always inside `B_s`) is **false**;
* the sharper `tau(G[H u B_s]) = |B_s| - 1` and even
  `tau(G[H u B_s]) <= |B_s| - 1` are **false** in the capacity-1 branch;
* combined with O-56 (violation in `B_s`, `P` clean) and O-64 (violation on `P`,
  `B_s` clean), **neither `P` nor `B_s` is a universal localizer**;
* the saturation bookkeeping must be stated carefully: tight-set saturation only
  gives `load_B(v) = min(c(v), deg_B(v))`, so a `v` with `deg_B(v) < c(v)` need
  not be saturated. Here `w` is adjacent to `B_s` with `deg_{B_s}(w) = 1 < 2 =
  c(w)`, and is indeed not saturated. Only the *oversubscribed* external `h`
  (`deg_{A_s}(h) >= c(h)+1`) is guaranteed saturated.

### Summary of the localization landscape

| witness | capacity branch | quotient `M_h(B_s)` | inclusion-minimal violation | blocker |
|---|---|---|---|---|
| O-56 | 2 | acyclic | `{2,3} ⊆ B_s`, disjoint from `P` | `{6}`, size 1 |
| O-63 | 2 | cyclic | the full `B_s = {u,a,b}` | `{h,w}`, size 2 |
| O-64 | 1 | — | `P = {s,t}`; `B_s` clean | `{q1}` |

Any proposed Lemma-A argument must survive all three rows. In particular the
open target may not assume the violating set is `P`, is `B_s`, or is `T_F`
itself; only "some subset of `P u ⋃_s A_s`" is licensed.

*One documentation discrepancy I found while checking.* PROOFS.md §D, in the
`T_F`-normalization paragraph, says "O-56 and O-63 are already normalized
(`S = T_F`); O-64 lies OUTSIDE the hereditary-tightness class (its `S` is not a
minimum FVS), so the normalization does not apply to it." The measured values
say that **all three** lie outside the hereditary-tightness class
(`tau(G[H u S]) < |S|` in each — see the table above; necessarily so, since a
hereditarily tight instance with a forced cycle is exactly what Lemma A° forbids),
and that **all three** satisfy `S = T_F` (O-64: `A_s = {s,u}`, `A_t = {t}`,
union `= {s,t,u} = S`). So the sentence's implicature that O-56/O-63 are inside
the class is wrong; the `S = T_F` observation is purely set-theoretic and holds
in all three. No mathematical claim depends on this.

---

## (iv) The `T_F` normalization (Lemma 4.7): statement, proof, and what it licenses

**Setup.** Suppose a Lemma-A° instance `(G, S, H, e)` has a forced-core cycle
`F` with `S`-side `P`. For each `s in P` let `A_s` be its canonical carrier: the
unique inclusion-minimal Hall-tight set containing `s` (Lemma 4.4 — the two
forced incidences at `s` have inclusion-minimal tight exposers `X^-`, `X^+`;
`X^- ∩ X^+` is tight by the lattice, contains `s`, and still exposes both
because its degrees are coordinatewise no larger, so minimality forces
`X^- = X^+ = A_s`; and for any tight `Y ∋ s`, `A_s ∩ Y` is tight, contains `s`
and exposes a forced incidence at `s`, so `A_s ⊆ Y`). Put

    T_F = ⋃_{s in P} A_s ,   G' = G[H u T_F],   S' = T_F ,

keeping the same `H`, the same distinguished edge `e`, and the same capacities.

**Statement.** Then: (a) `G' - S' = H`; (b) `S'` is a minimum FVS of `G'`;
(c) hereditary tightness holds for every `X ⊆ T_F` in `G'`; (d) the restricted
system is feasible; (e) every `A_s` is still Hall-tight in `G'` and still
exposes both forced incidences at `s`; (f) every edge of `F` is still forced in
`G'`. Consequently a minimal counterexample to Lemma A° may be assumed to
satisfy `S = T_F`.

**Proof.**

(a) `G'` is induced on `H u T_F` and `T_F ⊆ S`, so removing `S' = T_F` leaves
exactly `H`, which is a forest.

(c) For `X ⊆ T_F`, `G'[H u X]` and `G[H u X]` are literally the same graph:
both are the subgraph of `G` induced on `H u X`. So
`tau(G'[H u X]) = tau(G[H u X]) = |X|`, verbatim from Lemma 3.3 applied to `G`.

(b) Take `X = T_F` in (c): `tau(G') = tau(G'[H u T_F]) = |T_F|`. And `T_F` is an
FVS of `G'` (deleting it leaves `H`). So it is a minimum FVS.

(d) `rho` is a function of the data `(X, H, capacities, X-to-H edges)` only, all
of which are unchanged in `G'`. So the Hall inequality `rho(X) >= 2|X|`, which
holds for all `X ⊆ S`, restricts to all `X ⊆ T_F`; Lemma 3.4 gives feasibility.
(Alternatively: (c) plus Corollary 3.8 applied to `G'` directly.)

(e) Tightness of `A_s` (`rho(A_s) = 2|A_s|`) and the exposure condition
(`s in A_s`, `deg_{A_s}(q) <= c(q)`) are statements about the same unchanged
data, so they persist.

(f) **This is the step that needs care, and it is the reason the lemma is not
trivial.** Forcedness is *not* monotone under restriction: deleting the demand
of `S`-vertices outside `T_F` frees capacity and can create new feasible
selections, so an incidence forced in `G` need not be forced in `G'`. Instead
forcedness is re-derived from scratch: by F1 (Lemma 3.5), an incidence is forced
iff some tight set exposes it; by (e) the set `A_s ⊆ T_F` is still tight in `G'`
and still exposes the two `F`-incidences at `s`; so F1, applied inside `G'`,
gives their forcedness afresh. Hence `F` is still in the forced core of `G'`.
∎

**Two things the lemma costs.**
* Connectedness may be lost: `G[H u T_F]` need not be connected. This is exactly
  why the open problem is stated as Lemma A° (no connectedness hypothesis) —
  the normalization is only usable if the disconnected form is the target. And
  A° implies the connected Lemma A used in Theorem 3.13, since a connected
  instance is a special case.
* Canonicity of `A_s` is not needed for bare validity (any tight exposing set
  would do in (e)/(f)), but the minimal choice gives the smallest `T_F`, and the
  downstream carrier lemmas (punctured tightness, `U_h` structure) are stated
  for the canonical `A_s`.

**What it licenses, precisely.** In a minimal counterexample one may assume

    S = T_F = ⋃_{s in P} A_s ,

i.e. **every `S`-vertex lies inside the carrier of some cycle vertex**. There is
no "outer" part of `S` that merely creates congestion from a distance: every
`S`-vertex is certified to participate in the tight set responsible for some
forced cycle edge. In that normalized instance `S` itself is a union of tight
sets, hence tight by the lattice (Lemma 3.6), so `rho(S) = 2|S|` and
`delta ≡ 0` on a lattice containing `S`, every `A_s`, and every `B_s`.

**What it does *not* license.** It does not say the hereditary violation lies in
`T_F` in any *proper* sense — after normalization `T_F = S`, so "the violation
lies in `T_F`" is just "the violation lies in `S`", which is the whole of
Lemma A. The normalization removes irrelevant `S`-vertices; it does not locate
the violation. (This is consistent with the witnesses: all three already satisfy
`S = T_F`, and their violations sit in three different places.)

**Punctured tightness, for the record** (Lemma 4.5, used in (iii)): with
`B_s = A_s \ {s}`, removing `s` lowers `min(c(v), deg_{A_s}(v))` by 1 exactly at
those `H`-neighbours `v` of `s` with `deg_{A_s}(v) <= c(v)`; let `k` be their
number. The two forced ends `q^-, q^+` qualify, so `k >= 2`; and
`rho(B_s) = rho(A_s) - k = 2|A_s| - k` gives `delta(B_s) = 2 - k >= 0`, so
`k <= 2`. Hence `k = 2`, `B_s` is tight, the only non-oversubscribed
`H`-neighbours of `s` are `q^-` and `q^+`, and every other `H`-neighbour `h`
satisfies `deg_{A_s}(h) >= c(h) + 1` (so `deg_{B_s}(h) >= c(h)`).

---

## Oracle contact made while writing this

All commands run from a clean clone at commit `0617d7a`, `tools/` hashes
verified against `tools/SHA256SUMS.txt` (17/17 OK) before use.

| check | command | result |
|---|---|---|
| gold: A1 at n=7 | `python3 a1_verify.py 7` | `A1 = 143/143, fail = 0` — matches tools/README |
| gold: B-PLUS-2 at n=9 | `python3 b_hslide.py 9` | `cyc = 24195`, gap hist `{0: 24195}`, 0 failures — matches |
| gold: B-PLUS-2 at n=10 | `python3 b_hslide.py 10` | `cyc = 448577`, gap hist `{0: 448577}`, 0 failures — matches |
| Lemma A at n=8 | `python3 forced_core.py 8` | inst 2186, cyclic cores 0, maxpath 6 |
| Lemma A at n=9 | `python3 forced_core.py 9` | inst 13003, cyclic cores 0, maxpath 6 |
| Lemma A at n=10 | `python3 forced_core.py 10` | inst 116216, cyclic cores 0, maxpath 8 — matches ledger O-44 |
| three witnesses | `python3 work/wcheck.py …` | every recorded value reproduced with independent code |

Gauntlet outcome: **completed**.
