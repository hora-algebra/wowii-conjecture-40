# Comprehension gauntlet — attempt/2026-08-04-claude-fable-5-0eb8

Model: Claude Fable 5 (Claude Code CLI). Date: 2026-08-04.
Base: v2 main `b9eb809` ("Merge release/v2"). This file replaces, on this
branch only, the previous attempt's gauntlet that v2 main carries at the same
path; that document remains intact on `main` and on its own branch.

Paper references use the v2 numbering, verified directly against
`paper/paper.tex`: Theorem 3.13 = `thm:F2` (reduction), Lemma 4.7 = `lem:TF`
($T_F$ normalization), Definition 5.4 = SV, Lemmas 5.7/5.8 = L1/L2.

Every numerical fact quoted below about the witnesses and the abstract
even-cycle system was recomputed from the paper's definitions by my own code,
`work/fable-0eb8/gauntlet_check.py`, written without consulting any prior
attempt's checker. It enumerates feasible selections directly, intersects them
for the forced core, computes rho and all tight sets, computes exact FVS
numbers of the induced subgraphs `G[H u X]` for every `X ⊆ S`, and derives the
canonical carriers. All assertions pass ("ALL GAUNTLET CHECKS PASS").

## (i) The reduction chain of Theorem 3.13

**Target.** For connected nontrivial bipartite `G`: `ell(G) >= 2 tau(G) + 1`,
where `tau = n - f` (decycling number) and `ell = n - p` (max edges of a
spanning linear forest). This is the bipartite case of Conjecture 40 because
the deficiency substitution `f = n - tau, b = n - o, p = n - ell` turns
`2f >= p + b + 1` into `ell + o >= 2 tau + 1` (Theorem 2.1; the ceiling can be
dropped since `2f` is even and `t >= ceil(m/2) iff 2t >= m` for integers), and
bipartite means `o = 0`.

**The model.** If `tau = 0`, `G` is a forest with an edge and `ell >= 1`
trivially; so let `S` be a minimum FVS, `|S| = tau >= 1`, and `H = G - S` the
resulting forest. Fix an edge `e = (x,y)` of `H` (existence: below). The
selection model gives every `s in S` demand 2, every `h in H` capacity 2,
except the endpoints of `e` get capacity 1. A feasible selection `J` picks 2
distinct `S`-`H` incidences at each `s`, respecting capacities. A selected
cycle is a cyclic component of the incidence graph `J`.

**Why an acyclic feasible selection suffices** (the counting step inside the
proof of 3.13). Suppose `J` is feasible and `J u {e}` is acyclic. Every vertex
of `J u {e}` has degree <= 2: `s`-vertices have degree exactly 2 (demand);
`h`-vertices have degree <= c(h) <= 2, and the two capacity-1 endpoints of `e`
have at most 1 selected incidence plus the edge `e` itself. An acyclic graph
with maximum degree 2 is a disjoint union of paths — a linear forest. It spans
`S u H = V(G)` (uncovered vertices ride along as trivial paths) and has
exactly `2|S| + 1` edges: two per `s`, plus `e`. Hence `ell(G) >= 2 tau + 1`.

**The chain that delivers an acyclic feasible selection:**

1. **Lemma 3.3 (hereditary FVS tightness).** `tau(G[H u X]) = |X|` for every
   `X ⊆ S`. Upper bound: `X` itself is an FVS of `G[H u X]` (deleting it
   leaves the forest `H`). Lower bound: an FVS `D` of `G[H u X]` with
   `|D| < |X|` would make `(S \ X) u D` an FVS of `G` smaller than `S`.
   This is the only place minimality of `S` enters the machine, and it is the
   hypothesis separating real instances from abstract Hall systems (see (ii)).

2. **Lemma 3.4 (generalized Hall).** A feasible selection exists iff
   `rho(X) := sum_h min(c(h), deg_X(h)) >= 2|X|` for all `X ⊆ S`. Proof is
   max-flow/min-cut on the network sigma -> S -> H -> sink: the cheapest cut
   whose S-side intersection is `X` costs `2(|S|-|X|) + rho(X)`, since each
   `h` is placed on the cheaper of its two sides, contributing
   `min(c(h), deg_X(h))`.

3. **Lemma 3.7 + Corollary 3.8 (feasibility for every fixed edge).** The
   rooted-forest-extension bound (3.7) says: for `X` independent and inside
   one bipartition class, `tau(G[H u X]) <= floor(rho_e(X)/2)`. Its proof
   deletes an `H`-vertex with `deg_X >= 2` (away from the root `r`, the
   `e`-endpoint on the side opposite `X`) — costing exactly 2 units of
   `rho_e` and 1 of FVS — and closes the base case by hand around `r`.
   Corollary 3.8 splits arbitrary `X` as `X_L u X_R`; the supports of the two
   `rho_e` summands are disjoint (each `H`-vertex has neighbours in only one
   class), so `rho_e(X) = rho_e(X_L) + rho_e(X_R)`, and a Hall violation on
   either side would contradict hereditary tightness through 3.7. So the
   model is feasible — for every choice of `e`. Tightness also supplies the
   fixed edge: `E(H) = ∅` would make `G[H u {s}]` a star forest with
   `tau = 0 != 1`.

4. **Lemma A (forced core acyclic) — open.** An incidence is forced when it
   lies in every feasible selection; the forced core is the graph of forced
   incidences. Its exact role in 3.13: it guarantees that every selected
   cycle `C` of any feasible selection contains at least one avoidable
   (non-forced) incidence — if all of `C`'s incidences were forced, `C`
   would be a cycle inside the forced core. Lemma A supplies exactly the
   premise of Lemma B, nothing else.

5. **Lemma B (CES toggles exist) — open.** A toggle `J -> J'` is CES for a
   designated selected cycle `C` when `C` is no longer a selected cycle of
   `J'` and every selected cycle of `J'` was already one of `J` (Definition
   3.2: semantic, compare cycle sets; strictly stronger than "fewer
   cycles"). Lemma B: every selected cycle containing an avoidable incidence
   admits a CES toggle. Proved infrastructure it leans on: Theorem 3.10
   (residual augmentation — after deleting the one unit of flow routed
   through a selected incidence `a`, avoidability of `a` is equivalent to a
   single residual augmenting path in `N - a`), hence "avoidable" =
   "one-move avoidable" (Corollary 3.11).

6. **Lemma 3.12 (descent).** Each CES toggle strictly decreases the number
   of selected cycles (destroys `C`, creates none), a nonnegative integer,
   so iteration terminates in an acyclic feasible selection. Termination
   needs only strict decrease; the no-new-cycle strength is what the toggle
   mechanism actually produces.

7. **Lemma 3.9 (fixed-edge parity).** `J` acyclic implies `J u {e}` acyclic:
   a cycle through `e = (x,y)` minus `e` would be an `x`-`y` path
   alternating `H,S,H,...`, of even length; but `x,y` are adjacent in
   bipartite `G`, so every `x`-`y` path has odd length. Bipartiteness is
   spent here a second time (the first is the class split in 3.8).

Roles, exactly: A gives B its premise; B gives the descent its step; the
descent gives an acyclic `J`; parity lets `e` join it; counting converts it
to `ell >= 2 tau + 1`; tightness (via 3.7/3.8) makes the model feasible at
all and forces `E(H) != ∅`. A and B are the only unproved links.

## (ii) Why Hall feasibility alone cannot give Lemma A

The abstract even-cycle system on `m >= 2` spokes: `S = {s_0..s_{m-1}}`,
`H = {h_0..h_{m-1}}`, `s_i` incident to exactly `h_i` and `h_{i+1 mod m}`,
demand 2, all capacities 2 (no capacity-1 pair needed).

**Computation of rho, from the definition.** For any `X ⊆ S`:
`sum_h deg_X(h) = sum_{s in X} deg(s) = 2|X|`, and every `h` has total degree
2 in the system, so `deg_X(h) <= 2 = c(h)` and the min truncation never
bites: `rho(X) = 2|X|` exactly. The Hall criterion holds with **every** `X`
tight — feasibility is as non-strict as it can be.

**The unique feasible selection is the whole cycle.** Total demand `2m`
equals total capacity `2m`, so every capacity is saturated; each `s_i` has
only two incident `H`-vertices, so it must select both. The forced core is
therefore the entire alternating cycle `s_0 h_1 s_1 h_2 ... h_0 s_0` —
maximally cyclic. (Checker: unique selection, forced core = `C_{2m}`,
`m = 2..5`.)

**Where hereditary tightness fails.** Realized as a graph, `G[H u S]` is the
cycle `C_{2m}`, and `tau(C_{2m}) = 1 < m = |S|` for `m >= 2`. So `S` is
nowhere near a minimum FVS and Lemma 3.3's conclusion already fails at
`X = S`. Conclusion: "Hall-feasible => forced core acyclic" is FALSE as
stated; Lemma A can only be the implication

    hereditary FVS tightness for all X ⊆ S  =>  forced core acyclic,

so any proof must actually spend the tightness hypothesis on subsets, not
just feasibility. A proposed proof of Lemma A that never uses
`tau(G[H u X]) = |X|` for some nontrivial `X` is refuted by this system
before it starts.

## (iii) The three warning witnesses: what each kills, and how

None of the three is a Lemma-A° counterexample. In each, hereditary tightness
FAILS somewhere (my checker locates the exact inclusion-minimal violating
set), so the forced cycle is permitted; each witness refutes a proposed rule
for *where* the violation must sit. All values below recomputed
independently by `gauntlet_check.py`.

**O-56 (capacity-2 case, acyclic quotient) — kills P-localization and
calibrates the single-blocker subcase.** `S = {0,1,2,3}`, forced 4-cycle on
`P = {0,1}` through `H`-vertices `{4,5}`; auxiliaries `{2,3}` both adjacent
to the shared external vertex `6` (plus private vertices `7`, `8`).
Mechanism of the forcing: `{2,3}` must be split across `6`'s capacity
(their private pairs `(2:7), (3:8)` leave one slot each on `6`), so
`deg(6)`'s capacity 2 is saturated by `{2,3}`; `0` and `1` are pushed off
`6` onto `{4,5}`, whose four incidences become the forced cycle. Unique
feasible selection; forced core has exactly **8** edges (my enumeration
agrees with the corrected JSON; VERIFY-1's note 2 — the old ten-edge list
wrongly included `(0,6),(1,6)` — is confirmed resolved in v2). The
inclusion-minimal hereditary violation is `X = {2,3}`:
`tau(G[H u {2,3}]) = 1 < 2`, with single-vertex FVS witness `{6}` — the
violation is **disjoint from `P`**, killing "the violation must lie on the
cycle's own S-side" (P-localization; `P = {0,1}` itself is clean, `tau = 2`).
Since the blocker is the single external vertex `6`, O-56 also shows the
single-blocker subcase (Lemma 4.6) is nonempty — it is an instance that
subcase handles; what it kills is any strategy that *only* proves the
P-local case.

**O-63 (capacity-2 case, cyclic quotient) — kills the degree-2 and
private-cycle localizations.** `S = {s,t,u,a,b}`; forced 4-cycle on
`P = {s,t}` through `{q1,q2}` (`t` is rigid: its only neighbours are
`q1,q2`). The trio `{u,a,b}` — each of incidence-degree exactly **3**, to
`{h,w,z}` — has demand 6 against capacity 6, so it saturates `h,w,z` and
pushes `s` off `h`. Carrier `A_s = {s,u,a,b}` (recomputed: the unique
minimum tight set containing `s`), puncture `B_s = {u,a,b}`, tight
(`rho = 6`). The inclusion-minimal hereditary violation is the **entire**
`B_s`: `tau(G[H u {u,a,b}]) = 2 < 3`, while every pair inside it is clean
(`tau = 2` each), and the minimum FVS witnesses are `{h,w}` or `{h,z}` —
**blockers of size 2**. This kills two rules at once: (1) "every vertex of
`B_s` has incidence-degree 2" (all three have degree 3); (2)
"incidence-degree >= 3 forces a private cycle avoiding `h`" (no single
external vertex blocks; the violation needs a pair, and the augmented
quotient `M_h` is cyclic here — `u,a,b` all have both non-`h` neighbours
`w,z` in one `H - h` component). Any argument that deletes one external
vertex and expects the puncture to fall apart dies here.

**O-64 (capacity-1 case) — kills B_s-localization.** `S = {s,t,u}`; `H` is
the tree `q1-r-q2`, `q1-y`, `y-h`, `y-w`; fixed edge `e = (h,y)` with
`c(h) = c(y) = 1`. Unique feasible selection: `s,t -> {q1,q2}`,
`u -> {h,w}`. Mechanism: `u` saturates the **capacity-1** vertex `h`,
pushing `s` off `h`; `s,t` then grind on `{q1,q2}` and the 4-cycle
`s-q1-t-q2-s` is forced. Carrier `A_s = {s,u}`, so `B_s = {u}` — and here
is the kill: `B_s` is Hall-tight (`rho({u}) = 2`, since `c(h) = 1` and `u`'s
two usable units are `h` and `w`... precisely `min(1,1) + min(2,1) = 2`)
yet hereditarily **clean**: `tau(G[H u {u}]) = 1 = |B_s|`. The first
violation sits on the cycle's own S-side `P = {s,t}`:
`tau(G[H u {s,t}]) = 1 < 2` (FVS witness `{q1}`). So "the violation lives
inside the puncture `B_s`" is false — the mirror image of O-56, where `P`
was clean. Together O-56 and O-64 prove no single one of `P`, `B_s` is a
universal localizer, and O-64 shows the capacity-1 branch is genuinely
separate: the saturating set can be one `S`-vertex through a capacity-1
`H`-vertex, so density arguments about punctures have nothing to grip.

Cross-check on all three (recomputed): `tau(G[H u S]) = 2, 3, 2` against
`|S| = 4, 5, 3` — all three sit outside the hereditarily tight class, as
they must (a hereditarily tight instance with a forced cycle is exactly
what Lemma A° forbids).

## (iv) The T_F normalization (Lemma 4.7): statement, proof, license

**Statement.** Let a Lemma-A° instance (bipartite `G`, minimum FVS `S`,
forest `H = G - S`, fixed edge `e`, standard capacities) have a forced-core
cycle `F` with S-side `P`. Let `A_s` be the canonical carrier of `s in P`
(the unique minimum tight set containing `s`, exposing both forced
incidences at `s` — Lemma 4.3), and put `T_F = union of A_s over s in P`.
Restrict to `G' = G[H u T_F]` with `S' = T_F`, same `H`, same `e`, same
capacities. Then: `G' - S' = H`; `S'` is a minimum FVS of `G'`; hereditary
tightness holds for all `X ⊆ T_F`; the restricted system is feasible; each
`A_s` is still tight and still exposes the forced edges at `s`; hence every
edge of `F` is still forced in `G'`. Consequence: a minimal counterexample
to Lemma A° may be assumed to satisfy `S = T_F`.

**Proof, in my own words.**
(1) For `X ⊆ T_F`, the graphs `G'[H u X]` and `G[H u X]` are the *same
graph* — both are induced subgraphs of `G` on `H u X`. So hereditary
tightness on subsets of `T_F` transfers verbatim from Lemma 3.3 on `G`.
(2) With `X = T_F`: `tau(G') = |T_F|`, and `T_F` is itself an FVS of `G'`
(removing it leaves the forest `H`), so `S' = T_F` is a *minimum* FVS of
`G'`. This re-establishes the one global hypothesis of the model.
(3) `rho` is computed from `X`, the capacities, and the `X`-to-`H` edges
only — all unchanged by restriction. So `rho(X) >= 2|X|` for `X ⊆ T_F` is
inherited and Lemma 3.4 gives feasibility of the restricted system.
(4) The delicate point: forcedness is NOT monotone under restriction —
deleting the S-vertices outside `T_F` removes their demands, which can
create new feasible selections in which a previously forced incidence is
avoided. So each `F`-edge must be *re-forced* from scratch: its certificate
is the carrier `A_s ⊆ T_F`, still tight (same `rho` value) and still
exposing the incidence (same degrees, same capacities), so by
forced-iff-exposed (Lemma 3.5/F1, applied in `G'`), no feasible selection
of `G'` omits it. Hence `F` survives as a forced-core cycle of `G'`.

**What it licenses.** In hunting a minimal counterexample to Lemma A° one
may assume every `S`-vertex lies in some cycle carrier:
`S = T_F = P u (union of punctures B_s)`. It does NOT license:
(a) connectedness — the restriction can disconnect `G'`, which is exactly
why Lemma A° is stated without a connectedness hypothesis (and that costs
nothing: an all-capacity-2 component not containing `e` has its forcedness
implied by the fixed-edge case — the 5047 dead-end ledger note);
(b) forcedness of incidences *outside* `F` — only the `F`-edges are
re-certified;
(c) any localization of the hereditary violation inside `T_F` — O-56
(violation = punctures `{2,3}`), O-63 (violation = full `B_s`), and O-64
(violation = `P`) jointly show the violating set moves around inside `T_F`
from instance to instance.

## Verification record

- `tools/SHA256SUMS.txt`: **17/17 OK** from the `tools/` directory of my
  worktree (v2 main `b9eb809`) before any oracle use.
- `work/fable-0eb8/gauntlet_check.py` (my code, this branch): O-56, O-63,
  O-64 all reproduced — feasible-selection counts 1 / 6 / 1, forced-core
  membership of each recorded forced 4-cycle, O-56 forced core exactly the
  corrected 8 edges, carriers `A_0 = {0,2,3}`, `A_1 = {1,2,3}` (O-56),
  `A_s = {s,u,a,b}` (O-63), violation sets `{2,3}` / `{u,a,b}` / `{s,t}`
  with tau 1 / 2 / 1 and blockers `{6}` / `{h,w}`,`{h,z}` / `{q1}`;
  `tau(G[H u S]) = 2 / 3 / 2` vs `|S| = 4 / 5 / 3`; abstract even-cycle
  systems `m = 2..5`: `rho(X) = 2|X|` for every `X`, unique feasible
  selection, forced core `C_{2m}`, `tau(G[H u S]) = 1`.
