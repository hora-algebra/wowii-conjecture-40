# Comprehension gauntlet — attempt/2026-08-05-claude-opus-5-064c

Written from `paper/paper.tex` (v2), `proofs/PROOFS.md`, `LEMMA-A-CARRIER.md`
and `tools/witnesses/` on `main` at `9b01be1`. Own words, own derivations.
Ordering note for the record: Step 0 and Step 0.5 were completed first; this
gauntlet was written after the first structural observations of the run were
made but before any of them was written up as a claim or graded by the oracle.

---

## (i) The reduction chain of Theorem 3.13, and the exact role of each lemma

**Target.** For connected nontrivial bipartite `G`, `ℓ(G) ≥ 2·τ(G) + 1`, where
`ℓ` is the maximum number of edges of a spanning linear forest and `τ` the
feedback vertex number. (`τ = 0` is disposed of first: a nontrivial forest has
an edge, and one edge plus isolated vertices is a spanning linear forest with
`1 = 2·0+1` edges.)

**The model.** Fix a minimum FVS `S`, so `H := G − S` is a forest. Fix an edge
`e = xy ∈ E(H)`. Give every `s ∈ S` demand exactly 2 and every `h ∈ H`
capacity `c(h) = 2`, except `c(x) = c(y) = 1`. A *feasible selection* `J`
picks two distinct `S`–`H` incidences at each `s` respecting the capacities.

**Why the model computes the target.** Suppose `J` is feasible and acyclic.
Every `s` has `deg_J(s) = 2`; every `h` has `deg_J(h) ≤ c(h) ≤ 2`; and `x,y`
have `deg_J ≤ 1`, so `J ∪ {e}` still has maximum degree 2. `J ∪ {e}` is acyclic
(Lemma 3.11, below), so it is a disjoint union of paths — a linear forest. It
spans `S ∪ H = V`, and it has `2|S| + 1` edges. Hence `ℓ ≥ 2|S| + 1 = 2τ + 1`.
So the whole bipartite case reduces to **F2**: *for some fixed edge `e`, an
acyclic feasible selection exists.*

**Why `J ∪ {e}` is acyclic when `J` is (fixed-edge parity, Lemma 3.11).** A
cycle of `J ∪ {e}` through `e` would give, after deleting `e`, an `x`–`y` path
made of `S`–`H` incidences. Such a path alternates `H, S, H, …`, so it has even
length. But `x` and `y` are adjacent in a bipartite graph, hence in opposite
classes, so every `x`–`y` path has odd length. Contradiction. So the only
possible cycles of `J ∪ {e}` are cycles of `J`.

**Existence of a feasible selection at all (Corollary 3.9).** Feasibility is a
flow question: source `→ s` of capacity 2, `s → h` of capacity 1 per incidence,
`h →` sink of capacity `c(h)`. By max-flow/min-cut, a feasible selection exists
iff `ρ(X) := Σ_h min(c(h), deg_X(h)) ≥ 2|X|` for every `X ⊆ S` (Lemma 3.5).
This is verified from hereditary FVS tightness: split `X` by bipartition class
(each half independent), apply the rooted forest bound
`τ(G[H ∪ X]) ≤ ⌊ρ_e(X)/2⌋` (Lemma 3.8) to the deficient half, and contradict
`τ(G[H ∪ X]) = |X|`. Note where the fixed edge enters: the bound is proved for
the *punctured* capacity vector, so feasibility holds for **every** choice of
`e`, not just a convenient one.

**Hereditary FVS tightness (Lemma 3.3), the hypothesis that carries everything.**
For every `X ⊆ S`, `τ(G[H ∪ X]) = |X|`. `≤` is trivial (`X` is an FVS of
`G[H∪X]`). For `≥`: if `D` were an FVS of `G[H∪X]` with `|D| < |X|`, then
`(S \ X) ∪ D` is an FVS of `G` of size `|S| − |X| + |D| < |S|`, contradicting
minimality of `S`. Two things worth keeping in mind: the statement is
equivalent to `S` being a *minimum* FVS (not merely inclusion-minimal), and it
is a statement about *all* `2^{|S|}` subsets, which is why it is strictly
stronger than the Hall feasibility it implies.

**Descent (Lemma 3.12).** A toggle `J → J'` is *cycle-erasing* (CES) for a
selected cycle `C` when `C` is not a cycle of `J'` and every cycle of `J'` was
already a cycle of `J`. This is semantic: compare the two cycle sets. A CES
toggle strictly lowers the number of selected cycles, a nonnegative integer, so
iterated CES toggles terminate at an acyclic feasible selection.

**The two lemmas and their separate jobs.**

- **Lemma A** (forced core acyclic): the set of incidences lying in *every*
  feasible selection contains no cycle. Its only job in the reduction is to
  guarantee that every selected cycle contains at least one *avoidable*
  (non-forced) incidence. Without it, a selected cycle could be rigid and the
  descent would have nothing to move.
- **Lemma B** (cycle-erasing descent): every selected cycle that contains an
  avoidable incidence admits a CES toggle. Its job is to make the descent step
  exist once Lemma A has supplied the raw material.

So the chain is: hereditary tightness ⟹ feasibility (unconditional) ⟹ [Lemma A]
every selected cycle has an avoidable incidence ⟹ [Lemma B] a CES toggle exists
⟹ descent terminates ⟹ acyclic feasible selection ⟹ `J ∪ {e}` is a spanning
linear forest with `2τ+1` edges ⟹ bipartite Conjecture 40. Everything except
A and B is proved unconditionally in §3.

**Residual augmentation (Theorem 3.13's engine, paper Thm 3.10).** Deleting the
arc of a selected incidence `a=(s,h)` from the network leaves the flow `J − a`
with a single deficient source arc at `s`. So `a` is avoidable iff a simple
residual augmenting path from `s` exists; "avoidable" and "one-move avoidable"
coincide. Concretely a residual path is
`s, h₁, s₁, h₂, …, h_k` with `(s,h₁) ∉ J`, `(s_i,h_i) ∈ J`, `(s_i,h_{i+1}) ∉ J`,
and `deg_{J−a}(h_k) < c(h_k)`; its length is `2k−1`, always odd. Toggling
replaces `(s_i,h_i)` by `(s_i,h_{i+1})` along the path and adds `(s,h₁)`.

---

## (ii) Why Hall feasibility alone cannot give Lemma A

Take the abstract even-cycle system: `S = {s₁,…,s_m}`, `H = {h₁,…,h_m}`, each
`s_i` adjacent exactly to `h_i` and `h_{i+1}` (indices mod `m`), all demands 2,
all capacities 2. Then `ρ(X) = Σ_h min(2, deg_X(h))`. For `X = S`,
`ρ(S) = 2m = 2|S|`: Hall's condition holds with equality, so the system is
feasible. But each `s_i` has exactly two available incidences, so the *unique*
feasible selection is all `2m` incidences, and that selection is the whole
`2m`-cycle. Its forced core is therefore a cycle.

This is not a counterexample to Lemma A, because the instance violates
hereditary tightness: `G[H ∪ S]` is a `2m`-cycle, whose feedback vertex number
is 1, while `|S| = m`. Take `m ≥ 2` and the violation is strict.

The moral is sharp and it is what makes Lemma A hard: the *Hall layer* — the
tight-set lattice, the carrier machinery, punctured tightness, the F1
forced-iff-exposed characterization — is all available in the abstract system
too, and the abstract system has a cyclic forced core. So no argument that uses
only tight sets, carriers and capacities can prove Lemma A. Some step must
consume the *forest* structure of `H` together with `τ(G[H∪X]) = |X|` for a
subset `X` that the argument constructs. Every proved foothold in §4 that does
close a subcase (A-I, the single-blocker lemma) does exactly that: it exhibits
an explicit `X` and an explicit FVS of `G[H ∪ X]` of size `< |X|`.

---

## (iii) The three warning witnesses and what each one kills

The witnesses live in `tools/witnesses/`. None is a counterexample to Lemma A°:
in each, hereditary tightness *fails* somewhere, so a cyclic forced core is
permitted. Their job is to refute proposed rules about **where** the violation
must sit.

Setup for reading them: for `s` on a forced cycle, `A_s` is the unique
inclusion-minimal tight set exposing both forced incidences at `s` (Lemma 4.4),
`B_s = A_s \ {s}` is tight (punctured tightness, Lemma 4.5), the two forced ends
`q^-,q^+` of `s` are the only `H`-neighbours `v` of `s` with
`deg_{A_s}(v) ≤ c(v)`, and every other `H`-neighbour `h` of `s` has
`deg_{A_s}(h) ≥ c(h)+1`.

- **O-56** (capacity 2, acyclic quotient). `A_s = {0,2,3}`, `B_s = {2,3}` tight,
  forced ends `{4,5}`, external neighbour `6` with `deg_{A_s}(6) = 3`, and the
  incidences `2 ~ {6,7}`, `3 ~ {6,8}`. Here the hereditary violation does sit
  inside `B_s` and is blocked by the *single* external `H`-vertex `6`. This is
  exactly the single-blocker configuration of Lemma 4.8: if every `u ∈ U_h =
  N(h) ∩ B_s` had at most one `H`-neighbour besides `h`, then `{h}` alone would
  be an FVS of `G[H ∪ U_h]`, giving `τ ≤ 1 < 2 ≤ |U_h|` and a contradiction.
  What O-56 kills: it does not kill the subcase — it *inhabits* it, showing the
  subcase is nonempty; what it kills is the hope that exhibiting the
  single-blocker configuration is by itself progress toward the general case,
  since the configuration occurs without the general obstruction being present.
  Its real force is together with O-63.
- **O-63** (capacity 2, cyclic quotient). Every vertex of `U_h` has incidence
  degree 3; the hereditary violation is the *whole* `B_s = {u,a,b}`; the
  blocking set is `{h,w}`, of size 2. This refutes two natural localizations
  at once: (1) "every `B_s`-vertex has incidence degree 2" — false here; and
  (2) "incidence degree `≥ 3` forces a private cycle in the forest quotient" —
  also false here, the quotient is cyclic but not for that reason. In
  particular, degree-2 and private-cycle localizations of the violation are
  dead: a single external blocker is not enough and high degree does not
  manufacture the cycle you want.
- **O-64** (capacity 1). `S = {s,t,u}`; `H` is the tree `q₁ − r − q₂` plus
  `q₁ − y`, `y − h`, `y − w`; fixed edge `e = (h,y)`, so `c(h) = c(y) = 1`;
  adjacencies `s ~ q₁,q₂,h`, `t ~ q₁,q₂`, `u ~ h,w`. The unique feasible
  selection is `s,t → {q₁,q₂}` and `u → {h,w}`: `u` consumes the capacity-1
  vertex `h`, which pushes `s` off `h`, and `s − q₁ − t − q₂ − s` is a forced
  cycle. What it kills: `B_s`-localization. Here `B_s = {u}` is Hall-tight but
  `τ(G[H ∪ B_s]) = 1 = |B_s|` — it carries **no** hereditary violation at all.
  The first violation is on the cycle's own `S`-side, `P = {s,t}`, where
  `τ(G[H∪P]) = 1 < 2`. It also separates the capacity-1 and capacity-2 branches:
  the mechanism that creates the forced cycle here is the punctured capacity of
  the fixed edge, which cannot occur in the all-capacity-2 setting.

Taken together: neither `P`, nor any `B_s`, nor `T_F` is a universal home for
the hereditary violation. Any proof must build its violating set from the whole
carrier family plus the external-neighbour structure.

---

## (iv) The `T_F` normalization (Lemma 4.9), with proof, and what it licenses

**Statement.** Suppose a Lemma-A° instance has a forced-core cycle `F` with
`S`-side `P`. Put `T_F = ⋃_{s∈P} A_s`, and restrict to `G' = G[H ∪ T_F]` with
`S' = T_F`, the same `H`, the same fixed edge and capacities. Then
`G' − S' = H`; `S'` is a minimum FVS of `G'`; hereditary tightness holds for
every `X ⊆ T_F`; the restricted system is feasible; every `A_s` remains tight
and still exposes both forced incidences at `s`; and every edge of `F` is still
forced in `G'`.

**Proof.** (1) For `X ⊆ T_F`, the graphs `G'[H∪X]` and `G[H∪X]` are literally
the same induced subgraph of `G`, so `τ(G'[H∪X]) = τ(G[H∪X]) = |X|` by
hereditary tightness in `G`. (2) Taking `X = T_F` gives `τ(G') = |T_F|`, and
`T_F` is an FVS of `G'` since `G' − T_F = H` is a forest; hence it is a minimum
FVS. (3) `ρ` depends only on the capacities and the `X`-to-`H` incidences, all
unchanged, so `ρ(X) ≥ 2|X|` survives restriction and Lemma 3.5 gives
feasibility. (4) The one delicate point: forcedness is **not** monotone under
restriction — deleting the demands of `S`-vertices outside `T_F` can create new
feasible selections and un-force incidences. So `F` is re-forced from scratch
via F1: for `s ∈ P`, its carrier `A_s ⊆ T_F` is still tight (same `ρ` value)
and still exposes both incidences at `s` (same degrees, same capacities), so no
feasible selection of `G'` omits them. Connectedness can be destroyed by the
restriction — which is precisely why Lemma A° is stated without a connectedness
hypothesis. ∎

**What it licenses.** A minimal counterexample to Lemma A° may be assumed to
satisfy `S = T_F = ⋃_{s∈P} A_s = P ∪ U` where `U = ⋃_{s∈P} B_s`. Under that
normalization statements about `N_S(q)` become statements about `N_{P∪U}(q)`,
which is what makes the NC/NCM conclusions usable in the form
`deg_S(q) = 2`. What it does **not** license: it does not preserve
connectedness, it does not preserve forcedness of anything outside `F`, and it
does not let one assume `P ∩ U = ∅` (that fails in ~44% of sampled cyclic
abstract systems, per the 5047 lessons entry).

---

## Outcome

Gauntlet **COMPLETED**. Manifest check on the inherited tools:
`cd tools && shasum -a 256 -c SHA256SUMS.txt` → 17/17 OK (recorded in
`work/064c/logs/manifest.txt`).
