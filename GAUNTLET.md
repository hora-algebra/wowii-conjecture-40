# Comprehension gauntlet — attempt/2026-08-05-claude-opus-5-0520

ATTACK.md **v4** Step 1. Written from `proofs/PROOFS.md`, `LEMMA-A-CARRIER.md`,
`LEMMA-A-CARRIER-POSET.md` and `tools/witnesses/*.json`, in my own words.
Every computational statement below was recomputed by `work/0520/engine0520.py`
and `work/0520/wit0520.py`, which share no predicate code with `work/carrier.py`,
`work/carrier_poset.py` or `work/wcheck.py`. Engine anchor (before any use):

```
ANCHOR systems=115774 cyclic=798 pdis=18      # matches carrier.py and b17e exactly
```

## Notation

`G` bipartite. `S ⊆ V(G)` with `H = G − S` a forest. `e = (x,y)` a fixed edge of
`H`; capacities `c(h) = 2` for all `h ∈ H` except `c(x) = c(y) = 1`. Each `s ∈ S`
has **demand 2**: a *feasible selection* `J` picks, for every `s`, two distinct
`H`-neighbours, subject to `load_J(h) ≤ c(h)`.

Two different "tight"s, never to be conflated:

* **Hall tightness.** `ρ(X) = Σ_{h∈H} min(c(h), deg_X(h))`, `δ(X) = ρ(X) − 2|X|`.
  Feasibility ⟺ `δ(X) ≥ 0` for all `X ⊆ S` (C5). `X` is *tight* when `δ(X) = 0`.
* **Hereditary FVS tightness.** `τ(G[H ∪ X]) = |X|` for every `X ⊆ S` (C2).
  Equivalent to "`S` is a minimum FVS of `G`" (5047 §2.1: `⇐` is C2; `⇒` is
  `X = S` plus the fact that `H` is a forest).

`A_s` = the unique inclusion-minimum Hall-tight set containing `s` (canonical
carrier); `B_s = A_s \ {s}`. For a forced-core cycle with `S`-side `P`,
`U = ⋃_{s∈P} B_s` and `T_F = P ∪ U = ⋃_{s∈P} A_s`.

---

## (i) The reduction chain of Theorem 3.13 — why A + B give the bipartite case

**Step 1 — algebraic normal form (B1).** With `τ = n − f`, `o = n − b`,
`ℓ = n − pathCover`, Conjecture 40 (`f ≥ ⌈(p+b+1)/2⌉`) is equivalent to
`ℓ + o ≥ 2τ + 1`. For bipartite `G`, `o = 0`, so the bipartite target is exactly

    ℓ(G) ≥ 2·τ(G) + 1.

**Step 2 — the model.** If `τ = 0` then `G` is a nontrivial forest, has an edge,
and that single edge is already a spanning linear forest: `ℓ ≥ 1 = 2τ+1`. So
assume `τ ≥ 1` and fix a **minimum** FVS `S ≠ ∅`; `H = G − S` is a forest (B2).
`E(H) ≠ ∅`: otherwise, for any `s ∈ S`, `G[H ∪ {s}]` is a star forest, so
`τ(G[H ∪ {s}]) = 0`, contradicting hereditary tightness `τ(G[H ∪ {s}]) = 1`.
Fix `e ∈ E(H)` and give `e`'s endpoints capacity 1, everything else capacity 2.

**Step 3 — why an acyclic selection is exactly what is wanted.** A feasible
selection `J` gives every `s ∈ S` degree exactly 2 and every `h ∈ H` degree
`≤ c(h)`. If `J ∪ {e}` is acyclic then it is a forest in which every vertex has
degree `≤ 2` — a **linear forest** — spanning `V(G)`, with
`2|S| + 1` edges. Hence `ℓ ≥ 2|S| + 1 = 2τ + 1`. That is **F2**:

> **F2.** There exist a fixed edge `e ∈ E(H)` and a feasible selection `J_e`
> with `J_e ∪ {e}` acyclic.

Quantifier discipline (B3'): F2 needs **one** `e`, not all `e`.

**Step 4 — a feasible selection exists at all (C5b).** The Rooted Forest
Extension Lemma gives `τ(G[H ∪ X]) ≤ ⌊ρ_e(X)/2⌋` for `X` independent inside one
bipartition class. Split `X ⊆ S` as `X_L ∪ X_R`; the two Hall supports are
disjoint, so `ρ_e(X) = ρ_e(X_L) + ρ_e(X_R)`. If `ρ_e(X) < 2|X|` then some side
has `ρ_e(X_L) < 2|X_L|`, whence `τ(G[H ∪ X_L]) ≤ ⌊ρ_e(X_L)/2⌋ < |X_L|`,
contradicting hereditary tightness. So Hall holds for every `X` and every `e`,
and C5 produces a feasible selection **for every** `e`.

**Step 5 — the descent, and the exact role of each lemma.**

* **Lemma 0 (C3).** `e` lies on no selected cycle: deleting `e` from a cycle
  through it would leave an `x`–`y` path alternating `H,S,H,…`, of even length,
  but `x,y` are adjacent in a bipartite graph, so every `x`–`y` path is odd.
  Hence `J ∪ {e}` is acyclic ⟺ `J` is acyclic; the descent may ignore `e`.
* **Lemma A** — *forced core acyclic*. An incidence is **forced** (R3) if it
  lies in every feasible selection, **avoidable** otherwise. Lemma A says the
  forced core contains no cycle. **Its only job in the chain is this:** any
  selected cycle `C` of `J` therefore cannot consist entirely of forced
  incidences, so `C` contains at least one *avoidable* incidence. That is
  precisely the hypothesis Lemma B demands. Lemma A is used nowhere else.
* **Lemma B** — *every selected cycle containing an avoidable incidence admits
  a CES toggle*. CES is semantic: the move destroys `C` and creates no selected
  cycle that was not already present. Lemma B's only job is to supply one
  descent step.
* **Lemma 1 / C4.** "Avoidable" is equivalent to "one-move avoidable": deleting
  the arc `a` from the flow network `N` leaves a flow of value `2|S|−1`, and by
  the augmenting-path theorem a value-`2|S|` flow exists in `N − a` iff a simple
  residual augmenting path does. So the search for a toggle is local; the class
  "globally avoidable but not one-move avoidable" is empty.
* **Lemma 5 / C8 (descent).** A CES toggle strictly decreases the number of
  selected cyclic components, a nonnegative integer; so iterating terminates at
  an acyclic feasible selection, i.e. F2.

**Chain.** `A` (every selected cycle has an avoidable incidence) `+ B` (such a
cycle can be erased) `+ C8` (the count descends) `⇒ F2 ⇒ ℓ ≥ 2τ+1` (Step 3)
`⇒` the bipartite case of Conjecture 40 (Step 1).

**Status note carried from ATTACK.md v4 and branch `…-4d7a`.** `A + B` is *a*
route, not the only one: **SD** ("every feasible selection possessing a selected
cycle has *some* cycle admitting a CES toggle") already implies F2 through C8
with **no** use of Lemma A, and `A ∧ B ⇒ SD`, so SD is strictly weaker. That is
why v4 lists SAFE-EXISTS, not Lemma B, as open item 2. Lemma A remains
independently interesting and is this run's target.

---

## (ii) Why Hall feasibility alone cannot yield Lemma A

**The abstract even-cycle system.** Take `S = {s_0,…,s_{m−1}}`,
`H = {h_0,…,h_{m−1}}`, incidences `s_i ~ h_i, h_{i+1}` (indices mod `m`), all
capacities 2, demand 2.

*Feasible and rigid.* Each `s_i` has exactly two incidences, so every feasible
selection must take both: the selection is unique and **every** incidence is
forced. Each `h_j` is used by `s_{j−1}` and `s_j`, i.e. load `2 = c(h_j)`.

*Hall holds — with room to spare.* For any `X ⊆ S`, `Σ_h deg_X(h) = 2|X|` and
`deg_X(h) ≤ 2 = c(h)` for every `h`, so every term of `ρ` is `min(c,deg)=deg`
and `ρ(X) = 2|X|`. Thus `δ(X) = 0` for **every** subset: the system is feasible
and *every* set is Hall-tight.

*Yet the forced core is a cycle.* The incidence graph is the `2m`-cycle
`s_0 h_1 s_1 h_2 … s_{m−1} h_0 s_0`, entirely forced.

*What fails is hereditary FVS tightness.* Realise `H` as an edgeless forest
(supply the fixed edge `e` by a separate incidence-free `K_2`, legitimate since
Problem 4.1 is stated without connectedness). Then `G[H ∪ S]` **is** that
`2m`-cycle, so `τ(G[H ∪ S]) = 1`, while `|S| = m`. For `m ≥ 2`,
`τ(G[H ∪ S]) = 1 < m`: `S` is not a minimum FVS.

Recomputed with `engine0520` for `m = 2,3,4,5`:

```
m=2: forced=4/4 cyclic_components=1 (len 4) min_delta=0 every_subset_tight=True tau=1 |S|=2
m=3: forced=6/6 cyclic_components=1 (len 6) min_delta=0 every_subset_tight=True tau=1 |S|=3
m=4: forced=8/8 cyclic_components=1 (len 8) min_delta=0 every_subset_tight=True tau=1 |S|=4
m=5: forced=10/10 cyclic_components=1 (len 10) min_delta=0 every_subset_tight=True tau=1 |S|=5
```

**Conclusion.** Feasibility, submodularity, the tight-set lattice, F1 and the
carriers are *all* properties of the Hall layer, and the even-cycle system
satisfies every one of them while carrying a cyclic forced core. So no argument
living purely on that layer can prove Lemma A. Lemma A is exactly the
implication

    hereditary FVS tightness for every X ⊆ S   ⇒   forced core acyclic,

and the hypothesis is *essential*, not decorative.

**A sharper form of the same obstruction (my own, elementary, MATHEMATICALLY
PROVED).** It is not merely that `ρ` is *insufficient*; `ρ`-counting can never
even produce the contradiction. Let `X ⊆ S` be independent inside one
bipartition class, so C5b applies: `τ(G[H ∪ X]) ≤ ⌊ρ_e(X)/2⌋`. If `X` is
Hall-tight then `ρ_e(X) = 2|X|` and the bound reads `τ(G[H ∪ X]) ≤ |X|` —
exactly what hereditary tightness asserts, so no contradiction. If `X` is not
tight the bound is weaker still (`ρ_e(X) ≥ 2|X|+1`). Hence **no hereditary
violation can ever be certified by the `ρ` value of a set alone**; a violation
must be exhibited by an explicit small FVS, i.e. by the *forest geometry* of
`H` — which is precisely what the augmented quotient `M̂_h` encodes and what `ρ`
is blind to. This is why the surviving footholds (single-blocker subcase,
`M̂_h`-acyclicity) are all geometric, and it is the reason the `P`-local bridge
`τ(G[H ∪ P]) ≤ m−1` cannot be obtained by counting: `δ(P) ≥ 0` forbids it.

---

## (iii) The three frozen witnesses: what each kills, and how

All facts below were **recomputed** from the raw JSON data (vertices,
incidences, forest edges, capacities) by `work/0520/wit0520.py`; no derived
field of the JSON was trusted. All three satisfy `τ(G[H ∪ S]) < |S|`, i.e.
**none of them is a hereditary-tightness instance** — they refute *proof
strategies*, never Lemma A itself.

### O-56 — kills `P`-localization; is the single-blocker subcase

`S = {0,1,2,3}`, `P = {0,1}`, auxiliaries `{2,3}`; `H` a forest on `4..13`;
`c(10) = c(11) = 1`.

*Mechanism of the forced cycle.* `2 ~ {6,7}` and `3 ~ {6,8}`; vertex `7` is the
only other neighbour of `2` and `8` the only other neighbour of `3`, so both
auxiliaries must use `6`. That fills `c(6) = 2`. Now `0` and `1` are incident to
`{4,5,6}` but `6` is full, so each must take **both** `4` and `5`, and
`load(4) = load(5) = 2` exactly. The selection is unique; recomputed:
**1 feasible selection, 8 forced incidences**, forced core containing the
4-cycle `0−4−1−5−0`.

*What it refutes.* The inclusion-minimal hereditary violation is `X = {2,3}`
with `τ(G[H ∪ {2,3}]) = 1 < 2` (delete `6`) — and `{2,3} ∩ P = ∅`. So the
claim "the violation lies on the cycle's own `S`-side `P`" is **false**.
Recomputed: minimal violating sets `{2,3}` (`τ=1<2`), `{0,1,2}`, `{0,1,3}`.

*Carriers.* `A_0 = {0,2,3}`, `A_1 = {1,2,3}`, `B_0 = B_1 = {2,3} = U`,
`P ∩ U = ∅`, `deg_U(4) = deg_U(5) = 0`. So O-56 sits in the clean CS(c) regime.

*Its positive role.* It is an instance of the **proved** single-blocker subcase:
`h = 6` is an external `H`-neighbour of `0`, `U_6 = N(6) ∩ B_0 = {2,3}`, and
each of `2,3` has exactly one `H`-neighbour besides `6`; so `M̂_6(U_6)` is
acyclic, `G[H ∪ U_6] − 6` is a forest, and `τ ≤ 1 < 2 = |U_6|`. (The `refutes`
field of `O-56.json` also names "the acyclic-quotient / single-external-blocker
subcase (blocker size 1)". Read literally that is wrong — the subcase is PROVED
in PROOFS.md and O-56 *satisfies* it. I record it as a **wording defect in the
witness metadata**, consistent with VERIFY-1's finding that this file needed
correction; nothing mathematical turns on it.)

### O-63 — kills the degree-2 and "degree ≥ 3 ⇒ private cycle" localizations

`S = {s,t,u,a,b}`, `P = {s,t}`, `H = {r,x,q1,q2,h,w,z,y}`, `c(x)=c(y)=1`.

*Mechanism.* `u,a,b` are each incident to exactly `{h,w,z}`; their total demand
is 6 and `c(h)+c(w)+c(z) = 6`, so `h,w,z` are saturated by `{u,a,b}` in every
feasible selection. Hence `s` can never use `h`, and `s`, like `t`, is confined
to `{q1,q2}`: the 4-cycle `s−q1−t−q2−s` is forced. Recomputed: **6 feasible
selections**, 4 forced incidences, exactly that cycle.

*What it refutes.* `A_s = {s,u,a,b}`, `B_s = {u,a,b}`, and every vertex of `B_s`
has incidence-degree **3**, not 2 — killing "every `B_s`-vertex has
incidence-degree 2". And although `u,a,b` all have degree ≥ 3, none has a
*private* cycle avoiding `h`: both non-`h` neighbours `w,z` lie in the **same**
component of `H − h` (the star at `r`), so the quotient `M̂_h(B_s)` has parallel
edges and is cyclic. The violation needs the **whole** `B_s` and a **size-2**
blocker: `τ(G[H ∪ {u,a,b}]) = 2 < 3`, blocker `{h,w}` or `{h,z}`. So
"incidence-degree ≥ 3 ⇒ private cycle" is **false**; only `M̂_h`-cyclicity
decides.

*Scope correction, independently reproduced.* `O-63.json` calls `{u,a,b}` the
"first inclusion-minimal violation". My complete subset scan finds **six**
strictly smaller global violations — `{a,s}, {a,t}, {b,s}, {b,t}, {s,u}, {t,u}`,
each with `τ = 1 < 2`. The JSON statement is correct only *within* `B_s`
(where every proper subset is tight). This independently confirms the b17e
`[TOOLING]` lesson; the strategies O-63 kills are unaffected.

*Carriers.* `A_t = {t}`, `B_t = ∅`, so `A_s` and `A_t` are **incomparable** —
both inclusion-maximal, `P \ U = {s,t}`, `U = {u,a,b}`, `deg_U(q1)=deg_U(q2)=0`.

### O-64 — kills `B_s`-localization (capacity-1 branch)

`S = {s,t,u}`, `P = {s,t}`, `H`-tree `q1−r−q2`, `q1−y`, `y−h`, `y−w`;
`e = (h,y)`, so `c(h) = c(y) = 1`.

*Mechanism.* `u ~ {h,w}` only, so `u` must take both; `u` therefore saturates
the **capacity-1** vertex `h`. That pushes `s` off `h`, leaving `s` (and `t`)
confined to `{q1,q2}`: the forced 4-cycle `s−q1−t−q2−s`. Recomputed: **1
feasible selection**, 6 forced incidences, that cycle. Note there is *no*
feasible exchange at all here.

*What it refutes.* `A_s = {s,u}`, `B_s = {u}`, and `B_s` is Hall-tight — but
`τ(G[H ∪ B_s]) = 1 = |B_s|`: the puncture carries **no** hereditary violation
(the cycle `u−h−y−w−u` needs its own vertex). No `Y ⊆ B_s` helps. The violation
is instead on `P` itself: `τ(G[H ∪ {s,t}]) = 1 < 2` (delete `q1`). Recomputed:
the unique inclusion-minimal violating set is `{s,t} = P`.
So **`B_s`-localization is false**, the sharper `τ(G[H ∪ B_s]) ≤ |B_s| − 1` is
false, and capacity-1 versus capacity-2 external neighbours are genuinely
separate branches.

**Joint content.** O-56 puts the violation strictly off `P`; O-64 puts it
strictly on `P` with `B_s` clean. So neither `P` nor `B_s` — nor, since
`T_F = S` in all three, `T_F` — is a universal localizer. 5047's `larealize.py`
population strengthens this: in 39% of sampled near-misses the inclusion-minimal
violating set lies inside *neither* `P` nor *any* single `B_s`.

---

## (iv) The `T_F` normalization (paper Lemma 4.7): statement, proof, licence

**Statement.** Let a Lemma-A° instance (`G` bipartite, not necessarily
connected; `S` a **minimum** FVS; `H = G − S` a forest; fixed edge `e ∈ E(H)`
with the usual capacities) have a forced-core cycle `F` with `S`-side `P`. Put
`T_F = ⋃_{s∈P} A_s` and restrict to

    G' = G[H ∪ T_F],   S' = T_F,   same H, same e, same capacities.

Then (a) `G' − S' = H`; (b) `S'` is a minimum FVS of `G'`; (c) hereditary FVS
tightness holds for every `X ⊆ T_F`; (d) the restricted system is feasible;
(e) every `A_s` is still Hall-tight in `G'` and still exposes both forced
`F`-edges at `s`; (f) every edge of `F` is still **forced** in `G'`; (g) hence
the forced core of `G'` still contains `F`. **Therefore a minimal counterexample
to Lemma A° may be assumed to satisfy `S = T_F`.**

**Proof.**

(a) Deleting `S \ T_F` from `G` and then `T_F` leaves `H` unchanged, since
`H = G − S` and no `H`-vertex is removed.

(b) and (c). `H` is a forest, so `T_F` is an FVS of `G'` and
`τ(G') ≤ |T_F|`. For the reverse, note that hereditary tightness in `G`
(available because `S` is a minimum FVS, C2) gives `τ(G[H ∪ X]) = |X|` for
**every** `X ⊆ S`, in particular for every `X ⊆ T_F`; and `G'[H ∪ X] = G[H ∪ X]`
because `X ⊆ T_F` and the induced subgraph does not see the deleted vertices.
So `τ(G'[H ∪ X]) = |X|` for every `X ⊆ T_F` — which is (c), and with `X = T_F`
also (b).

(d) `X ⊆ T_F ⊆ S` implies `δ_{G'}(X) = δ_G(X) ≥ 0` (the deleted `S`-vertices
never appear in `ρ(X)`, which depends only on `X`'s own incidences and on the
capacities). By C5, `G'` is feasible.

(e) `A_s ⊆ T_F` by construction, and `ρ`, `δ` are computed from `A_s`'s own
incidences, so `A_s` is still tight in `G'`; likewise `deg_{A_s}(q) ≤ c(q)` at
each of the two forced ends `q` is unchanged, so `A_s` still *exposes* both.

(f) **This is the step that must not be done by monotonicity.** Restriction can
*create* new feasible selections — removing `S`-vertices outside `T_F` frees
capacity — so forcedness is **not** monotone under restriction and may not be
inherited. Instead, forcedness is re-established from scratch: by F1 (C5), an
incidence `a = (s,q)` is forced **iff** some Hall-tight set exposes it. By (e),
`A_s` is tight in `G'` and exposes both forced `F`-edges at `s`. Applying F1 in
the *restricted* network gives forcedness of each `F`-edge afresh in `G'`.

(g) Immediate from (f): every edge of `F` is forced in `G'`, so `F` lies in the
forced core of `G'`.

Connectedness may be destroyed by the restriction — which is exactly why the
statement is set in the **disconnected** Lemma A°. That is legitimate: A° implies
the connected version needed by F2 (a connected instance is an A° instance), and
raising all capacities to 2 only enlarges the feasible set, so
`forced(all caps 2) ⊆ forced(caps for e)` and the all-caps-2 abstract systems are
covered rather than being an untested gap.

**What the normalization licenses.**

1. **`S = P ∪ U`.** Every `S`-vertex is either on the cycle or inside some
   puncture. There are no "irrelevant" auxiliaries: every auxiliary is part of
   the forcing machinery. This is what makes the carrier family the *whole*
   object of study rather than one carrier at a time.
2. **The smallest such set.** Canonicity of `A_s` is not needed for validity but
   gives the inclusion-minimum normalized set, which is what the downstream
   carrier lemmas (CS, CP) consume.
3. **A bounded search space.** The abstract layer `(S, H-vertices, incidences,
   capacities)` decides feasibility, forcedness and the carriers, while the
   `H`-forest edges decide minimum-FVS-ness. Since hereditary tightness for all
   `X ⊆ S` ⟺ `S` is a minimum FVS, the counterexample hunt **factorises**, which
   is what `larealize.py` exploits.

**What it does not license.** `T_F` is *not* a universal localizer of the
hereditary violation: all three frozen witnesses satisfy `S = T_F`
set-theoretically and none of them puts the violation in a common place. And
because all three fail hereditary tightness, **the normalization lemma does not
even apply to them** — they constrain strategies, not the normalized class.

---

## Gauntlet outcome

**COMPLETED.** All four parts derived; every computational assertion recomputed
by an independently written engine that reproduces the published anchors
(`115774 / 798 / 18`) and the three witnesses' feasible-selection counts
(`1 / 6 / 1`), forced-core cycles, carrier tables and violation structure. Two
metadata scope defects were found and are reported above (O-63's
"inclusion-minimal" phrasing — independently confirming b17e's lesson — and
O-56's `refutes` field naming a subcase it in fact satisfies). Neither affects
any mathematical verdict. Proceeding to Step 3 target 1.
