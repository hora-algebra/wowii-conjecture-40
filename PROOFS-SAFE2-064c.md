# Structural results for SAFE-2-EXISTS — branch 064c

Self-contained. Every hypothesis is stated. Status labels follow ATTACK.md
Step 2. Nothing here is labelled PROVED without a complete derivation in this
file; nothing is labelled COMPUTATIONALLY VERIFIED without a named universe and
a hashed checker in `work/064c/`.

---

## 0. Setting

`G` is a finite simple bipartite graph with bipartition classes `L, R`; `S` is a
minimum feedback vertex set; `H = G − S` is a forest; `e = xy` is a fixed edge of
`H`. Capacities: `c(x) = c(y) = 1` and `c(h) = 2` for every other `h ∈ H`.

A **feasible selection** `J` assigns to each `s ∈ S` exactly two distinct
`S`–`H` incidences at `s`, so that each `h ∈ H` receives at most `c(h)` of them.
Write `J(s)` for the two `H`-vertices selected at `s`, `deg_J(h)` for the number
of selected incidences at `h`, and `N_H(v)` for the `G`-neighbourhood in `H`.

- `h` is **saturated** if `deg_J(h) = c(h)`, and **slack** if `deg_J(h) < c(h)`.
- The incidence graph of `J` has all `S`-degrees equal to 2 and all `H`-degrees
  at most 2, so each component is a path or a cycle. A **selected cycle** is a
  cyclic component. `c(J)` denotes the number of selected cycles. For a selected
  cycle `C` put `P(C) = V(C) ∩ S` and `Q(C) = V(C) ∩ H`.
- **Hereditary FVS tightness** (paper Lemma 3.3, unconditional):
  `τ(G[H ∪ X]) = |X|` for every `X ⊆ S`, where `τ` is the feedback vertex
  number.
- An incidence is **forced** if it lies in every feasible selection; **avoidable**
  otherwise. **F1** (paper Lemma 3.6): `(s,h)` is forced iff some `ρ`-tight
  `X ⊆ S` *exposes* it, i.e. `s ∈ X` and `deg_X(h) ≤ c(h)`; here
  `ρ(X) = Σ_h min(c(h), deg_X(h))` and `X` is tight when `ρ(X) = 2|X|`.
- **Residual augmenting path** (paper Theorem 3.10): after releasing an
  incidence `a = (s₀,h₀) ∈ J`, a residual augmenting path is a simple sequence
  `s₀, h₁, s₁, h₂, …, s_{k−1}, h_k` with `(s_{i−1}, h_i) ∉ J` for all `i`,
  `(s_i, h_i) ∈ J` for `1 ≤ i ≤ k−1`, `(s₀,h₀)` deleted from the network, and
  `deg_{J−a}(h_k) < c(h_k)`. Its **length** is `2k−1`. Toggling it gives the
  feasible selection
  `J₀ = J − a + (s₀,h₁) − (s₁,h₁) + (s₁,h₂) − ⋯ + (s_{k−1},h_k)`.
  `a` is avoidable iff such a path exists.
- `d₀(C)` is the minimum length of a residual augmenting path over the avoidable
  incidences of `C`. A **minimizing step** for `C` is a toggle along a path of
  length `d₀(C)`. A toggle `J → J₀` is **CES** for `C` when `C` is not a selected
  cycle of `J₀` and every selected cycle of `J₀` is a selected cycle of `J`.
  `C` is **A1-good** if some minimizing step for `C` is CES, else **A1-bad**.
  `J` is a **hard state** if it is cyclic and every selected cycle is A1-bad.

**Fact 0.** Every `h ∈ Q(C)` satisfies `c(h) = 2` and `deg_J(h) = 2`; in
particular every `H`-vertex of a selected cycle is saturated, `x` and `y` lie on
no selected cycle, and every slack `H`-vertex lies on no selected cycle. Also
`P(C)` lies in a single bipartition class and `Q(C)` in the other.

*Proof.* All vertices of a cyclic component have degree 2 in `J`, and
`deg_J(h) ≤ c(h) ≤ 2` forces `c(h) = 2 = deg_J(h)`. `C` alternates `S`- and
`H`-vertices along `G`-edges, and `G` is bipartite, so consecutive vertices of
`C` lie in opposite classes; the `S`-positions therefore all lie in one class. ∎

---

## 1. Length-one steps are automatically cycle-erasing

**Theorem 1 (LENGTH-ONE-CES). MATHEMATICALLY PROVED.**
Let `J` be feasible, `C` a selected cycle, `a = (s,h)` an incidence of `C`, and
suppose a residual augmenting path of length 1 from `s` exists after releasing
`a` — that is, there is `h' ∈ N_H(s)` with `(s,h') ∉ J` and
`deg_{J−a}(h') < c(h')`. Then `J' = J − a + (s,h')` is feasible and CES for `C`;
moreover the selected cycles of `J'` are exactly those of `J` other than `C`.

*Proof.* `(s,h') ∉ J` while `a = (s,h) ∈ J`, so `h' ≠ h`; releasing `a` changes
no degree except at `h`, hence `deg_J(h') = deg_{J−a}(h') < c(h')`: `h'` is
**slack in `J`**.

*Feasibility.* `s` keeps selected degree 2; `h` drops to `deg_J(h) − 1`; `h'`
rises to `deg_J(h') + 1 ≤ c(h')`. All other degrees are unchanged.

*Cycles.* By Fact 0, `h'` slack implies `h' ∉ V(C)`. In `J − a` the component of
`s` is the path `P_C := C − a`, whose vertex set is exactly `V(C)`; every other
component of `J − a` is a component of `J` other than `C`. Since `h' ∉ V(C)`,
`h'` lies in a component `D ≠ P_C` of `J − a`. Adding the single edge `(s,h')`
joins two distinct components, so it creates no cycle, and `P_C ∪ D + (s,h')` is
acyclic. Therefore the cyclic components of `J'` are precisely the cyclic
components of `J − a`, i.e. the selected cycles of `J` other than `C`. ∎

**Corollary 1.1.** If `d₀(C) = 1` then `C` is A1-good, and a length-one
minimizing step lowers `c(J)` by exactly one.

---

## 2. A1-goodness is slack-adjacency

**Theorem 2 (A1-GOOD ⟺ SLACK-ADJACENCY). MATHEMATICALLY PROVED.**
For every feasible `J` and every selected cycle `C`:

  `d₀(C) = 1` ⟺ some `s ∈ P(C)` has a slack `G`-neighbour in `H`.

Consequently, if some `s ∈ P(C)` has a slack neighbour then `C` is A1-good; and
if `C` is A1-bad then `d₀(C) ≥ 3` and **every** `H`-neighbour of **every**
vertex of `P(C)` is saturated.

*Proof.* (⟸) Let `s ∈ P(C)` have a slack neighbour `h'`. By Fact 0,
`h' ∉ V(C)`; both selected incidences at `s` lie on `C`, so `(s,h') ∉ J`.
Release either incidence `a` of `s` (both lie on `C`). In `J − a` we still have
`deg(h') ≤ deg_J(h') < c(h')`, so `s → h' → sink` is a residual augmenting path
of length 1. Hence `a` is avoidable and `d₀(C) = 1`.

(⟹) A length-one path after releasing `a = (s,h)` ends at some `h'` with
`(s,h') ∉ J` and `deg_{J−a}(h') < c(h')`. Since `a ∈ J` and `(s,h') ∉ J` we get
`h' ≠ h`, so `deg_J(h') = deg_{J−a}(h') < c(h')`: `h'` is slack, and
`s ∈ P(C)`. ∎

**Remark 2.1.** Theorem 2 makes A1-goodness a *local, one-line* predicate on the
state: no residual search is needed. It is the reason the hard-state population
can be isolated cheaply (used by `work/064c/s2e_scan11.py`).

---

## 3. Importing A-I: every selected cycle has an outside neighbour

**Theorem 3 (A-I for selected cycles). MATHEMATICALLY PROVED.**
For every feasible `J` and every selected cycle `C`: `N_H(P(C)) ⊋ Q(C)`.

*Proof.* Write `P = P(C)`, `Q = Q(C)`, `m = |P| = |Q| ≥ 2`. Suppose
`N_H(P) ⊆ Q`. By Fact 0, `P` lies in one bipartition class, so `P` is
independent in `G` and `G[H ∪ P]` has no `P`–`P` edge. Fix `q₀ ∈ Q` and put
`D = Q \ {q₀}`, `|D| = m−1`. In `G[H ∪ P] − D`:

* the `H`-part is `H − D`, an induced subgraph of the forest `H`, hence a forest;
* each `s ∈ P` has `N_H(s) ⊆ Q`, so at most the single neighbour `q₀` survives;
* `P` is independent.

A forest together with additional pairwise non-adjacent vertices of degree at
most one is again a forest. So `D` is a feedback vertex set of `G[H ∪ P]` of
size `m − 1 < m = |P|`, contradicting `τ(G[H ∪ P]) = |P|`. ∎

**Provenance.** This is paper Lemma 4.2 (A-I) with "forced-core cycle" replaced
by "selected cycle": the proof of A-I uses only that the cycle's `S`-side lies in
one bipartition class and that its `S`-vertices have no `H`-neighbour off the
cycle. Both hold verbatim for a selected cycle. This is the first transfer of
the certified Lemma-A stack onto the Lemma-B side.

**Corollary 3.1. MATHEMATICALLY PROVED.** If `C` is A1-bad, then some
`s ∈ P(C)` has a **saturated** `G`-neighbour `h₁ ∉ Q(C)`.
*Proof.* Theorem 3 gives a neighbour off `Q(C)`; Theorem 2 makes every
neighbour of `P(C)` saturated. ∎

---

## 4. Structure of a bad minimizing step of length three

Throughout this section `C` is A1-bad with `d₀(C) = 3`, and `J → J₀` is a
minimizing step that is **not** CES: released `a = (s,h)` with `(s,h)` an
incidence of `C`, path `s, h₁, s₁, h₂`, and

  `J₀ = J − (s,h) + (s,h₁) − (s₁,h₁) + (s₁,h₂)`.

Because the path has length 3 and not 1, `h₁` is not slack in `J − a`; since the
released arc lowers only `h`, this forces `h₁ ≠ h` and `h₁` saturated in `J`.
The terminal `h₂` satisfies `deg_{J−a}(h₂) < c(h₂)`, i.e. either `h₂ ≠ h` and
`h₂` is slack in `J`, or `h₂ = h`.

**Theorem 4 (bad-step structure, terminal off the released end).
MATHEMATICALLY PROVED.** If `h₂ ≠ h` then:

(a) `h₁ ∉ V(C)` and `s₁ ∉ P(C)`;
(b) the component `K` of `h₁` in `J` is a **path** component;
(c) `J₀` has exactly one selected cycle `Z` that is not a selected cycle of `J`;
(d) `V(Z) ⊆ V(K)`, so `V(Z) ∩ V(C) = ∅`;
(e) `c(J₀) = c(J)`;
(f) `deg_{J₀}(h) = 1 < 2 = c(h)`: the released `H`-end becomes slack.

*Proof.* (a) `h₂ ≠ h` makes `h₂` slack in `J`, and `(s₁,h₂) ∉ J` with
`h₂ ∈ N_H(s₁)`; by Theorem 2, `s₁ ∉ P(C)`. If `h₁ ∈ V(C)` then `h₁ ∈ Q(C)` and
by Fact 0 both selected incidences at `h₁` come from `P(C)`, so `s₁ ∈ P(C)` —
contradiction. Hence `h₁ ∉ V(C)`.

(b) Suppose `K` is a cycle. In `J − a` the component of `s` is the path `P_C`
on `V(C)`; `K` is untouched. Adding `(s,h₁)` merges `P_C` and `K` into one
component containing the cycle `K`. Removing `(s₁,h₁)` — an edge of `K` — leaves
that component connected with maximum degree 2 and no cycle, i.e. a path.
Finally `h₂` is slack, so by Fact 0 `h₂ ∉ V(C) ∪ V(K)`, so adding `(s₁,h₂)`
joins two distinct components and creates no cycle. The selected cycles of `J₀`
would then be those of `J` minus `{C, K}` — a CES step, contradicting badness.
So `K` is a path.

(c),(d) With `K` a path, the graph `J − a + (s,h₁)` is a forest of paths except
that `h₁` may have degree 3; removing `(s₁,h₁)`, an edge of the tree
`P_C ∪ K + (s,h₁)`, splits that tree into exactly two components: `K₁ ∋ s₁` and
the component containing `h₁` and `P_C`. No cycle exists at this point, and `C`
is destroyed (the incidence `(s,h)` is not restored, since `h₁ ≠ h` and
`s₁ ≠ s`). The step is not CES, so the final addition `(s₁,h₂)` must create a
cycle; that happens iff `h₂` lies in the component `K₁` of `s₁`, and then the
unique new cycle is `Z = (the K₁-path from s₁ to h₂) + (s₁,h₂) ⊆ K₁ ⊆ K`.
Since `V(K) ∩ V(C) = ∅`, (d) follows.

(e) `C` is destroyed, `Z` is created, all other components are untouched.

(f) `h ∈ Q(C)` has `c(h) = 2` and `deg_J(h) = 2` by Fact 0, and `J₀` removes one
incidence at `h` and adds none (`h₂ ≠ h`, `h₁ ≠ h`). ∎

**Theorem 4′ (terminal at the released end). MATHEMATICALLY PROVED.**
If `h₂ = h` then exactly one of the following holds:

(i) `h₁ ∉ V(C)` and the component `K` of `h₁` in `J` is a **cycle**; then
    `c(J₀) = c(J) − 1`;
(ii) `h₁ ∈ Q(C)`; then `s₁ ∈ P(C)`, the new cycles of `J₀` lie inside `V(C)`,
    and `c(J₀) ∈ {c(J), c(J)+1}`.

*Proof.* Suppose first `h₁ ∉ V(C)`, with component `K`. If `K` is a path, then
as in Theorem 4(c) removing `(s₁,h₁)` splits `P_C ∪ K + (s,h₁)` into `K₁ ∋ s₁`
and the part containing `h₁` and all of `P_C` — in particular containing `h`.
Then adding `(s₁,h)` joins two distinct components, creating no cycle, so the
step is CES, contradicting badness. So `K` is a cycle; then, as in Theorem 4(b),
after `+(s,h₁) −(s₁,h₁)` the merged component is a single path containing both
`s₁` and `h`, and `+(s₁,h)` closes exactly one cycle there. Both `C` and `K` are
destroyed and one cycle is created: `c(J₀) = c(J) − 1`.

Now suppose `h₁ ∈ V(C)`, so `h₁ ∈ Q(C)` and (Fact 0) `s₁ ∈ P(C)` is one of the
two `C`-neighbours of `h₁`. Write `P_C = C − (s,h)` as the path from `h` to `s`,
and let `α, β` be the `P_C`-neighbours of `h₁` on the `h`-side and the `s`-side
respectively. Adding `(s,h₁)` creates the cycle `Z₁` consisting of the `P_C`-arc
from `h₁` to `s` together with `(s,h₁)`, with the path `h … α h₁` attached at
`h₁`. If `s₁ = β`, then `Z₁` is destroyed and the component is a path containing
both `h` and `β`, so `+(β,h)` creates exactly one cycle, inside `V(C)`, and
`c(J₀) = c(J)`. If `s₁ = α`, then `Z₁` survives, the path `h … α` splits off,
and `+(α,h)` closes a second cycle inside that path; both new cycles lie inside
`V(C)` and `c(J₀) = c(J) + 1`. ∎

**Remark 4.1 (why this matters).** Theorem 4 says a bad length-three step
*relocates* the cycle: the new cycle `Z` is vertex-disjoint from `C` and lives
inside a former path component, while the released `H`-end `h` — a vertex of the
old cycle — becomes the new slack vertex. So the step does not shrink anything;
it exchanges "a cycle here, slack there" for "slack here, a cycle there". This
is exactly why one-step statements (SD-SHORT, B-TERMINAL-SLIDE, unrestricted
SUCCESSOR-ONE) keep dying, and it explains the recorded n=12 profile in which
every bad minimizing reroute creates exactly one replacement cycle.

---

## 5. The descent needs only a strict decrease

**Proposition 5. MATHEMATICALLY PROVED** (this is the paper's own remark under
Definition 3.4, made explicit).
For F2 it suffices that from every cyclic feasible selection some finite
sequence of toggles reaches a feasible selection with strictly fewer selected
cycles. Hence the following statement, weaker than SAFE-2-EXISTS (it is implied
by it), already implies F2:

> **SAFE-2-DEC.** For every cyclic feasible `J`, either some minimizing step
> strictly lowers `c`, or some minimizing step `J → J₀` has `c(J₀) ≤ c(J)` and
> some minimizing step from `J₀` strictly lowers `c`.

*Proof.* `c` is a nonnegative integer; a strictly decreasing sequence
terminates, and a terminal selection has no selected cycle, which with
Lemma 3.11 (fixed-edge parity) gives the spanning linear forest with `2τ+1`
edges. SAFE-2-EXISTS implies SAFE-2-DEC because a CES step lowers `c` by at
least one. ∎

**Remark 5.1.** Theorem 4′(i) supplies a family of *non-CES* steps that are
nevertheless count-decreasing. Any proof effort aimed at SAFE-2-EXISTS that gets
stuck on the CES clause should check SAFE-2-DEC first: it is what F2 consumes.

**Corollary 5.2. MATHEMATICALLY PROVED.** If an A1-bad cycle `C` has a
minimizing step whose terminal is the released end and whose first hop leaves
`C` (Theorem 4′(i)), then that single step strictly lowers the cycle count, so
SAFE-2-DEC is discharged at that state in one move. Such a step exists only when
the first hop lands on *another selected cycle*; in the graded population it
accounts for 184 of 720 bad minimizing steps (see `work/064c` results).

**Remark 5.3 (the `(2,1)` population is already free).** A state that has an
A1-good cycle is settled in one length-one CES step by Theorems 1 and 2 — no
lookahead, no terminal slide, no successor geometry. The recorded n=12
falsifications of B-TERMINAL-SLIDE and of unrestricted SUCCESSOR-ONE all live in
`(2,1)` states, i.e. states that *have* an A1-good cycle. So those
counterexamples refute obligations that neither SAFE-2-EXISTS nor SAFE-2-DEC
ever needed. The only states that carry real content are the hard ones.

---

## 6. The slack-free closure of a selected cycle is tight

For a feasible `J` define the residual closure of a set `A₀ ⊆ S`:

  `Y_i = ⋃_{s ∈ A_i} ( N_H(s) \ J(s) )`,  `A_{i+1} = A_i ∪ { s' : ∃ h ∈ Y_i, (s',h) ∈ J }`,

and let `A*`, `Y*` be the (finite) limits. These are exactly the vertices
reachable in the residual digraph of `J` from `A₀`.

**Theorem 6. MATHEMATICALLY PROVED.**
Let `C` be a selected cycle, `A₀ = P(C)`, and suppose **no** `h ∈ Y*` is slack.
Put `W = N_H(A*) \ Y*`. Then:

(i) `A*` lies in one bipartition class and `N_H(A*)` in the other; in particular
    at most one of `x, y` lies in `N_H(A*)`;
(ii) every selected incidence with `H`-end in `Y*` has its `S`-end in `A*`;
(iii) `A*` is `ρ`-tight: `ρ(A*) = 2|A*|`;
(iv) `|N_H(A*)| ≥ |A*| + 1`;
(v) `W ≠ ∅`, and **every** incidence between `A*` and `W` is forced.

*Proof.* (i) `A₀ = P(C)` lies in one class by Fact 0; `H`-neighbours of that
class lie in the other; owners of those `H`-vertices lie back in the first.
Induction. `x` and `y` are adjacent, hence in different classes, so `N_H(A*)`
contains at most one of them.

(ii) If `(s',h) ∈ J` with `h ∈ Y*` then `s'` is added to `A*` at the next step of
the closure, by construction.

(iii) Partition `N_H(A*) = Y* ⊔ W`. For `h ∉ N_H(A*)`, `deg_{A*}(h) = 0`.
For `h ∈ Y*`: `h` is saturated by hypothesis and all its selected incidences
come from `A*` by (ii), so `deg_{A*}(h) ≥ deg_J(h) = c(h)` and
`min(c(h), deg_{A*}(h)) = c(h)`. For `h ∈ W`: by definition of `W`, every
`A*`-neighbour of `h` *selects* `h`, so `deg_{A*}(h) ≤ deg_J(h) ≤ c(h)` and
`min(c(h), deg_{A*}(h)) = deg_{A*}(h)`. Now count selected incidences with
`S`-end in `A*`: there are `2|A*|` of them and each has its `H`-end in
`N_H(A*)`. Writing `E_W` for the number of them with `H`-end in `W`,

  `Σ_{h∈Y*} c(h) = Σ_{h∈Y*} deg_J(h) = 2|A*| − E_W`   (using (ii)),
  `Σ_{h∈W} deg_{A*}(h) = #(A*–W adjacencies) = E_W`   (definition of `W`).

Hence `ρ(A*) = (2|A*| − E_W) + E_W = 2|A*|`. Feasibility gives `ρ ≥ 2|A*|`, so
`A*` is tight.

(iv) Put `D = N_H(A*) \ {z₀}` for any `z₀ ∈ N_H(A*)`. In `G[H ∪ A*] − D` the
`H`-part is a subforest of `H`, `A*` is independent by (i), and each `s ∈ A*` has
`N_H(s) ⊆ N_H(A*)`, hence at most the one surviving neighbour `z₀`. So `D` is a
feedback vertex set and `|A*| = τ(G[H ∪ A*]) ≤ |N_H(A*)| − 1`.

(v) If `W = ∅` then `E_W = 0` and `Σ_{h∈Y*} c(h) = 2|A*|`; but by (i) at most one
vertex of `Y*` has capacity 1, so `Σ_{h∈Y*} c(h) ≥ 2|Y*| − 1 ≥ 2(|A*|+1) − 1`
by (iv), giving `2|A*| ≥ 2|A*| + 1`, absurd. For forcedness: `A*` is tight by
(iii) and every `h ∈ W` has `deg_{A*}(h) ≤ c(h)`, so `A*` exposes each incidence
`(s,h)` with `s ∈ A*`, `h ∈ W ∩ N_H(s)`; F1 makes it forced. ∎

**Corollary 6.1 (dichotomy at a selected cycle). MATHEMATICALLY PROVED,
conditional on Lemma A.** For every feasible `J` and selected cycle `C`, either

* the residual closure of `P(C)` reaches a slack `H`-vertex — so `C` has an
  avoidable incidence witnessed by a residual path ending at genuine slack — or
* some `q ∈ Q(C)` lies in `Y*`, i.e. some closure vertex is adjacent to a cycle
  vertex of `C` without selecting it.

*Proof.* Suppose neither. By Theorem 6, `W ≠ ∅` and all `A*`–`W` incidences are
forced. Every `q ∈ Q(C)` lies in `N_H(A*)` (its `C`-owners are in `P(C) ⊆ A*`)
and, by assumption, not in `Y*`; so `Q(C) ⊆ W` and every incidence of `C` is
forced. Then the forced core contains the cycle `C`, contradicting Lemma A. ∎

**Remark 6.2 (what Theorem 6 does not do).** Theorem 6 is *not* a proof of
Lemma A. Its argument closes only when `W = ∅`; in general `W ≠ ∅` and the
`A*`–`W` incidences form a forced sub-structure that the counting cannot bound,
because the `H`-forest can reconnect two spared `W`-vertices. Sparing two
`W`-vertices is exactly what would be needed to push `|D|` below `|A*|`. This is
the same obstruction that O-56/O-63/O-64 record for the localization attempts,
reached from a different direction; it is stated here so that the next attempt
does not re-walk it hoping the closure counting alone suffices.

---

## 7. The target, restated

**Theorem 7 (reformulation of HARD-SUCCESSOR-ONE). MATHEMATICALLY PROVED.**
Let `J` be a hard state and `J → J₀` any toggle. Then

  "`J₀` admits a CES minimizing step of length one"
   ⟺ "some `S`-vertex lying on a selected cycle of `J₀` has a slack
      `G`-neighbour in `J₀`".

*Proof.* Apply Theorem 2 to `J₀` (right side ⟺ some selected cycle `Z` of `J₀`
has `d₀(Z) = 1`), then Theorem 1 to `J₀` (a length-one minimizing step is
automatically CES). ∎

So the recorded conjectural lead becomes a statement with no residual search and
no CES obligation in it:

> **CL-6 (target, CONJECTURAL).** For every hard state `J` there is a minimizing
> step `J → J₀` with `c(J₀) ≤ c(J)` such that some `S`-vertex on a selected
> cycle of `J₀` has a slack `G`-neighbour in `J₀`.
>
> **CL-7 (universal form, CONJECTURAL).** The same for *every* minimizing step
> out of a hard state.

By Proposition 5 and Corollary 1.1, CL-6 implies SAFE-2-DEC restricted to hard
states, and together with Theorem 2 (which settles every non-hard state in one
length-one step) it implies SAFE-2-DEC outright, hence F2.

**Theorem 8 (the successor is at residual distance at most three).
MATHEMATICALLY PROVED.** In the situation of Theorem 4 (hard state `J`, A1-bad
`C` with `d₀(C)=3`, bad minimizing step `J → J₀` with released `a=(s,h)`, path
`s,h₁,s₁,h₂`, new cycle `Z`), the new cycle satisfies `d₀(Z) ≤ 3` in `J₀`.

*Proof.* `s₁ ∈ P(Z)`, and its two `J₀`-incidences are `(s₁,w₁)` and `(s₁,h₂)`,
both on `Z` (`w₁` is the second `J`-selected neighbour of `s₁`). Release either
of them, say `a′`. Then

  `s₁ → h₁ → s → h`

is a residual augmenting path in `J₀ − a′`: `(s₁,h₁) ∉ J₀` (it was removed) and
`h₁ ∈ N_H(s₁)`; `h₁` is still saturated in `J₀ − a′` (it lost `s₁` and gained
`s`, and `a′` does not touch it), so it is not a terminal and its selected
incidence `(s,h₁) ∈ J₀` continues the path; `(s,h) ∉ J₀` and `h ∈ N_H(s)`; and
`deg_{J₀}(h) = 1 < 2 = c(h)` by Theorem 4(f), so `h` is a valid terminal. The
four vertices are distinct because `h ∈ Q(C)`, `s ∈ P(C)`, `h₁ ∉ V(C)` and
`s₁ ∉ P(C)`. Hence `d₀(Z) ≤ 3`. ∎

**Corollary 8.1. MATHEMATICALLY PROVED.** In that situation `d₀(Z) ∈ {1,3}`, and
`d₀(Z) = 1` exactly when some `S`-vertex of `Z` has a slack `J₀`-neighbour
(Theorem 2), in which case the second step is CES by Theorem 1 and SAFE-2-EXISTS
holds at `J`.

**Remark 8.2 (the two undo paths are never CES).** Toggling the path of
Theorem 8 after releasing `(s₁,h₂)` returns exactly `J`, and after releasing
`(s₁,w₁)` it returns `J` with the single pair `J(s₁) = {h₁,w₁}` replaced by
`{h₁,h₂}`; in both cases `C` reappears, and `C` is not a selected cycle of `J₀`,
so neither toggle is CES for `Z`. So the length-3 branch of Corollary 8.1 cannot
be discharged by the canonical return path: SAFE-2-EXISTS at a hard state needs
either `d₀(Z)=1`, or a *different* length-3 minimizing step at `J₀` that is CES.

**Theorem 10 (exact equivalence: SAFE-2-EXISTS is a one-step escape from the
hard set). MATHEMATICALLY PROVED.** Call a cyclic feasible selection *hard* if
none of its selected cycles is A1-good. Then, for a hard state `J`:

  `J` satisfies SAFE-2-EXISTS
  ⟺ some minimizing step `J → J₀` has `c(J₀) ≤ c(J)` and `J₀` is **not** hard
  ⟺ CL-6 holds at `J`.

*Proof.* SAFE-2-EXISTS at a hard `J` asks for a minimizing step `J → J₀` with
`c(J₀) ≤ c(J)` such that `J₀` has a CES minimizing step; "`J₀` has a CES
minimizing step" is by definition "some selected cycle of `J₀` is A1-good",
i.e. "`J₀` is not hard". The second equivalence is Theorem 2 applied to `J₀`
(a cycle is A1-good iff one of its `S`-vertices has a slack neighbour) together
with Theorem 1 (a length-one step is automatically CES). ∎

**Corollary 10.1. MATHEMATICALLY PROVED.** F2 follows from the weaker statement
(weaker because CL-6 implies it)

> **HARD-ESCAPE.** From every hard state there is a finite sequence of
> minimizing steps, none increasing `c`, reaching a state that is not hard.

*Proof.* A non-hard cyclic state has an A1-good cycle, hence a CES minimizing
step, which lowers `c` by at least one; iterate and apply Proposition 5. ∎

**Proposition 11 (no free lunch). MATHEMATICALLY PROVED.**
Let `μ = min{ c(J) : J feasible }` for a fixed instance. If `μ ≥ 1` then every
feasible selection attaining `μ` is a hard state, and CL-6, HARD-ESCAPE,
SAFE-2-DEC and SAFE-2-EXISTS all fail at it.

*Proof.* Let `c(J) = μ ≥ 1`. A CES step lowers `c`, so no selected cycle of `J`
is A1-good: `J` is hard. Any step with `c(J₀) ≤ c(J)` has `c(J₀) = μ` and is
therefore again hard, so no non-increasing sequence leaves the hard set and no
second step can lower `c`. ∎

**Remark 11.1.** So every statement in this family — SAFE-2-EXISTS, SAFE-2-DEC,
HARD-ESCAPE, CL-6, and the earlier SD-SHORT / B-TERMINAL-SLIDE /
SUCCESSOR-ONE family — is *at least as strong as F2* and is false exactly when
F2 is false. No proof of any of them can avoid consuming hereditary FVS
tightness: a purely local argument about toggles would prove `μ = 0` for
instances where it is false (the abstract even-cycle system of the gauntlet has
`μ = 1`). This is the structural reason the one-step mechanisms kept dying at
`n = 11` and `n = 12`, and it is the criterion any new candidate should be held
to before it is scanned: *where does it use hereditary tightness?*

**Remark 10.2.** So the whole remaining content of SAFE-2-EXISTS is a statement
about a single finite digraph: put an arc `J → J₀` for every minimizing step out
of a hard state that does not increase `c`. SAFE-2-EXISTS says no hard state has
*all* of its out-arcs landing inside the hard set; HARD-ESCAPE says the hard set
contains no *closed* subset reachable from a hard state. Proposition 9 below
gives the only mechanism found so far that can pin an out-arc inside the hard
set, and Theorem 4 says every other out-arc relocates the cycle into a former
path component while freeing a cycle vertex — which is precisely why the hard
set looks hard to stay inside.

**Proposition 9 (a conditional falsification of the universal form).
MATHEMATICALLY PROVED.** Let `J` be a hard state and suppose some minimizing
step out of `J` is of type II(ii) of Theorem 4′ — terminal at the released end
`h₂ = h`, first hop `h₁ ∈ Q(C)`. Then the successor `J₀` has **no** length-one
step at all, so **CL-7 fails at `J`**.

*Proof.* In a type-II(ii) step the toggle is
`J₀ = J − (s,h) + (s,h₁) − (s₁,h₁) + (s₁,h)`. Degrees: `h` loses one and gains
one; `h₁` loses one and gains one; nothing else changes. Hence
`slack(J₀) = slack(J)`. By Theorem 4′(ii) every new cycle of `J₀` lies inside
`V(C)`, so its `S`-vertices lie in `P(C)`; and every old cycle of `J₀` is a
cycle of `J`. Because `J` is hard, Theorem 2 says no `S`-vertex on any cycle of
`J` — in particular none in `P(C)` — has a slack `J`-neighbour, and the slack
set has not moved. So no `S`-vertex on a cycle of `J₀` has a slack
`J₀`-neighbour: by Theorem 2 applied to `J₀`, no cycle of `J₀` has `d₀ = 1`. ∎

**Remark 9.1 (a preregistered search target).** Proposition 9 turns "is the
universal successor form true?" into a finite, local pattern search: a hard
state whose cycle `C` has a chord `s → q` (`s ∈ P(C)`, `q ∈ Q(C)`, `(s,q) ∉ J`)
such that the `s`-side `C`-neighbour of `q` is `G`-adjacent to the released end
`h`, with `d₀(C) = 3`. No such step has been seen in the graded population
(720 bad minimizing steps over 176 A1-bad records: 536 of type I, 184 of type
II(i), **0** of type II(ii)). The first type-II(ii) minimizing step at a hard
state falsifies CL-7 outright and is the cheapest decisive experiment left on
this branch of the problem. It does **not** by itself falsify CL-6 or
HARD-SUCCESSOR-ONE, which are existential over steps.

**Proposition 12 (slack is exactly path-endedness). MATHEMATICALLY PROVED.**
For every feasible `J`, writing `p = |H| − |S|`:

(i) the incidence graph has exactly `|H| − |S| + c(J)` components, of which
    exactly `p` are paths (isolated `H`-vertices counted as trivial paths) —
    so the number of path components does **not** depend on `c(J)`;
(ii) the total slack `Σ_h (c(h) − deg_J(h))` equals `2p − 2`;
(iii) at least `p − 1` `H`-vertices are slack, hence `|Sat(J)| ≤ |S| + 1`.

*Proof.* (i) The incidence graph has `|S| + |H|` vertices and `2|S|` edges and
every component is a path or a cycle, so the number of components is
`(|S|+|H|) − 2|S| + c(J)`. (ii)
`Σ_h c(h) − Σ_h deg_J(h) = (2|H| − 2) − 2|S| = 2p − 2`. (iii) each `H`-vertex
carries at most `2` units of slack, so at least `p−1` of them are slack, and
`|Sat(J)| ≤ |H| − (p−1) = |S| + 1`. ∎

**Corollary 12.1.** In a hard state, `N_H(P(C)) ⊆ Sat(J)` for every selected
cycle `C` (Theorem 2), so the whole neighbourhood of every cycle's `S`-side lies
inside a set of at most `|S| + 1` vertices, while `|N_H(P(C))| ≥ |P(C)| + 1`
(Theorem 6(iv)). Hard states are therefore *tight* configurations in a literal
counting sense — the cycle's `S`-side must find all of its neighbours among the
few saturated vertices.

**Measured fact 9.2 (which slack vertex witnesses the successor).** Over every
preserved hard-state certificate at n=11 and n=12 (1,146 records, 3,932 bad
minimizing steps, `work/064c/witness_slack.py`), the slack vertex of `J₀` that
gives the relocated cycle its length-one step is: the freed end `h` only, in
384 steps; a vertex that was *already* slack in `J`, only, in 1,700 steps; both,
in 1,848; neither, in **0**. So a proof shaped as "the relocated cycle sees the
freed vertex `h`" cannot work — it is refuted on 1,700 of 3,932 steps — and
neither can a proof that ignores `h`. Any argument must produce *some* slack
neighbour, not a designated one.

**Where the remaining difficulty sits, exactly.** Let `J` be hard, `C` a
selected cycle, and take the bad step of Theorem 4. Then the slack set moves by
exactly one unit: `slack(J₀) = (slack(J) \ {h₂}) ∪ {h}`, and the new cycle `Z`
sits inside the old path component `K`, disjoint from `C`, whereas the new slack
vertex `h` sits on the old cycle `C`. CL-6 therefore asks for an adjacency
between `P(Z)` and `slack(J₀) = (slack(J) \ {h₂}) ∪ {h}` — and by Measured fact
9.2 the argument may not privilege either part of that set: `h` alone suffices
in 384 of 3,932 graded steps, a pre-existing slack vertex alone in 1,700.

What is available: `Z` is exactly the component `K₁` of `K` closed up by the new
incidence (`h₂` had degree one in `J`, so it was an *end* of the path `K`, and
`Z = K₁ + (s₁,h₂)`); `P(Z)` is independent and lies in one bipartition class;
`|N_H(P(Z))| ≥ |P(Z)| + 1` (Theorem 6(iv)); the slack vertices of `J₀` are
exactly the ends of its `|H| − |S|` path components, up to the two units
absorbed by `x` and `y` (Proposition 12). What is missing is an argument that
forces one of those path ends to be `G`-adjacent to `P(Z)`. Every counting
identity above is satisfied with room to spare in both directions, so the step
must come from hereditary tightness applied to a set that meets both `P(C)` and
`P(Z)` — the natural candidate being `X = P(C) ∪ P(Z)`, which is independent and
one-sided, with the feedback vertex set to build against it still unknown. That
is the precise open obligation left by this run.
