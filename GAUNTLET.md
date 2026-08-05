# Comprehension gauntlet — attempt/2026-08-05-claude-opus-5-4d7a

ATTACK.md v3 Step 1. Written before any new mathematics on this branch. Own
words, own derivations; every computational statement below was recomputed on
this branch by `work/sd/wit_verify.py`, which shares no code with `tools/`
(it re-implements the model from the spec in paper §3 / PROOFS.md §D).

Notation used throughout. `G` connected, nontrivial, bipartite with classes
`L, R`. `tau(G)` = minimum feedback vertex set (decycling number), `f = n - tau`.
`o(G)` = minimum odd cycle transversal, `b = n - o`. `p(G)` = minimum number of
vertex-disjoint paths covering `V`, `ell = n - p` = number of edges in a maximum
spanning linear forest. `S` a minimum FVS, `H = G - S`, `e = xy` a fixed edge of
`H`. `G[H u X]` is the subgraph induced on `H u X`.

---

## (i) The reduction chain of Theorem 3.13, and the exact role of A and B

**Where the whole thing is going.** Conjecture 40 says
`f >= ceil((p + b + 1)/2)`. Substituting `f = n - tau`, `b = n - o`,
`p = n - ell` and clearing the ceiling gives the equivalent *deficiency form*
`ell + o >= 2*tau + 1`. For bipartite `G` we have `o = 0`, so the bipartite
target is exactly

> **(BT)** `ell(G) >= 2*tau(G) + 1`.

So the bipartite case asks for a spanning linear forest with at least `2 tau + 1`
edges. The whole apparatus exists to *build* one such forest explicitly.

**Step 1: why an incidence-selection model at all.** `tau = |S|`, and `H = G - S`
is a forest (deleting an FVS kills every cycle). A linear forest is a graph of
maximum degree `<= 2` with no cycle. The cheapest way to reach `2|S| + 1` edges
is to let every `s in S` contribute exactly two edges (`2|S|` edges) and add one
more edge from inside `H`. That is precisely the model: each `s in S` has
**demand 2** (it must select two distinct `S`–`H` incidences); each `h in H` has
**capacity** `c(h) = 2`, except that the two endpoints `x, y` of the fixed
`H`-edge `e` get `c(x) = c(y) = 1` so that `e` itself can be added without
pushing them to degree 3. A **feasible selection** `J` is any such assignment. A
**selected cycle** is a cyclic component of the bipartite incidence graph `J`.

**Step 2: an acyclic feasible selection is the theorem.** Suppose `J` is feasible
and `J u {e}` is acyclic. Every vertex has degree `<= 2` in `J u {e}`: an `s` has
degree exactly 2 by demand; an `h != x, y` has degree `<= c(h) = 2`; and `x`
(resp. `y`) has `<= 1` from `J` plus 1 from `e`. Acyclic + max degree 2 = a
disjoint union of paths = a linear forest. It spans `S u H = V(G)` (isolated
vertices are allowed as trivial paths) and has `2|S| + 1` edges. Hence
`ell >= 2|S| + 1 = 2 tau + 1`, which is (BT). Call the existence of such a `J`
for *some* fixed edge `e` the statement **F2**.

Note the quantifier: F2 needs **one** `e`, not every `e`. (The rooted forest
extension corollary happens to prove initial *feasibility* for every `e`, which is
stronger than needed and must not be confused with F2.)

**Step 3: the three things that make F2 non-vacuous.**

- *A fixed edge exists.* If `E(H)` were empty, take `X = {s}` for any `s in S`.
  Then `G[H u {s}]` has edges only at `s`, so it is a star forest and
  `tau(G[H u {s}]) = 0`. But hereditary FVS tightness (below) forces
  `tau(G[H u {s}]) = |{s}| = 1`. Contradiction, so `E(H) != empty`.
- *A feasible selection exists at all.* By the generalized Hall criterion
  (max-flow/min-cut on the obvious network), feasibility holds iff
  `rho(X) := sum_h min(c(h), deg_X(h)) >= 2|X|` for every `X subseteq S`. The
  rooted forest extension lemma gives `tau(G[H u X]) <= floor(rho_e(X)/2)`; if
  `rho_e(X) < 2|X|` for some `X` this yields `tau(G[H u X]) < |X|`, contradicting
  hereditary tightness. So a feasible selection exists — for every `e`.
- *`J u {e}` is acyclic iff `J` is.* (Fixed-edge parity.) If `J u {e}` had a
  cycle through `e`, deleting `e` would leave an `x`–`y` path made of `S`–`H`
  incidences, which alternates `H, S, H, S, ...` and therefore has **even**
  length. But `x` and `y` are adjacent in a bipartite graph, so they lie in
  opposite classes and every `x`–`y` path has **odd** length. Contradiction. So
  `e` sits on no selected cycle and acyclicity of `J` suffices.

**Step 4: the descent, and where A and B enter.** Start from any feasible `J`. If
it has a selected cycle, we want to move to another feasible selection with
strictly fewer selected cycles. The move used is a *residual toggle*: pick a
selected incidence `a = (s,h)` that is **avoidable** (some feasible selection
omits it), delete it, and re-route along a residual augmenting path in the flow
network with `a` removed. By the residual-augmentation theorem, `a` is avoidable
**iff** a single such augmentation exists (there is no "avoidable but not
one-move avoidable" class). A toggle is **CES** for a designated selected cycle
`C` when (i) `C` is destroyed and (ii) *no* selected cycle appears that was not
already there. CES implies the selected-cycle count strictly drops, and a
strictly decreasing sequence of nonnegative integers terminates — that is the
Descent Lemma.

The two open lemmas supply exactly the two things the descent needs:

- **Lemma A** (forced core acyclic) is what guarantees *every* selected cycle has
  an avoidable incidence at all. A **forced** incidence is one that belongs to
  every feasible selection; the **forced core** is the graph of all forced
  incidences. If some selected cycle `C` had all its incidences forced, `C`
  would be a cycle of the forced core. Lemma A says that never happens. Its role
  is therefore purely to make Lemma B's hypothesis non-vacuous: **A supplies the
  input B needs, it does not itself move anything.**
- **Lemma B** (cycle-erasing descent) says every selected cycle *that contains an
  avoidable incidence* admits a CES toggle. Its role is to actually perform the
  descent step.

Chain: hereditary tightness ⟹ (Hall) feasibility for every `e`; A ⟹ every
selected cycle is Lemma-B-eligible; B ⟹ a CES toggle exists; Descent ⟹
terminate at an acyclic feasible `J`; parity ⟹ `J u {e}` acyclic; degree count ⟹
a spanning linear forest with `2|S| + 1` edges ⟹ (BT).

**A consequence I will use (and which the proof of Theorem 3.13 quietly
overshoots).** The Descent Lemma is already stated with the hypothesis "*from
every feasible selection with a selected cycle, **some** CES toggle exists*".
`A and B` together give the much stronger "*every* selected cycle of *every*
feasible selection admits a CES toggle". The gap between those two quantifiers
is the whole of Lemma A plus most of Lemma B, and nothing downstream uses it.
This is the opening my primary target exploits (see `PREREG-SD.md`).

---

## (ii) Why the abstract even-cycle system shows Hall feasibility cannot yield Lemma A

Lemma A is an implication with *two* hypotheses available: (a) the instance is
Hall-feasible, and (b) hereditary FVS tightness, `tau(G[H u X]) = |X|` for every
`X subseteq S`. The question is whether (a) alone is enough. It is not, and the
abstract even-cycle system is the reason.

**The system.** Take `m >= 2`. Vertices `s_0, ..., s_{m-1}` on the `S` side and
`h_0, ..., h_{m-1}` on the `H` side, with `s_i` adjacent to `h_i` and `h_{i+1}`
(indices mod `m`). Every `s_i` has demand 2, every `h_j` has capacity 2, and `H`
is edgeless (so trivially a forest).

**It is Hall-feasible.** Each `s_i` has exactly two neighbours, so it must select
both; each `h_j` then receives exactly two selected incidences, `deg = 2 = c`.
So there is exactly one feasible selection, and Hall's condition holds
(`rho(X) >= 2|X|` for every `X`).

**Its forced core is a cycle.** Since the selection is unique, every incidence is
forced. The incidence graph is a single `2m`-cycle. So the forced core is a
cycle: Lemma A's conclusion is **false** for this system.

**Recomputed on this branch** (`work/sd/wit_verify.py`, positive control):
`m = 3` → 1 feasible selection, forced-core cycle `{s0,s1,s2,h0,h1,h2}`;
`m = 4` → 1 feasible selection, forced-core cycle on all 8 vertices.

**What must therefore fail is hereditary tightness — and it does.** In this
system `H` is edgeless, so `G[H u {s_i}]` is a star (two edges at `s_i`) and
`tau(G[H u {s_i}]) = 0 < 1 = |{s_i}|`. Recomputed: every singleton `{s_i}` is an
inclusion-minimal hereditary violation with `tau = 0`. Equivalently, the whole
graph here is a `2m`-cycle whose minimum FVS has size 1, so `S` (of size
`m >= 2`) is not a minimum FVS at all.

**The lesson, stated exactly.** Hall feasibility, and everything derivable from
it — the tight-set lattice, submodularity of `delta(X) = rho(X) - 2|X|`, carriers,
punctures, the F1 characterization of forcedness — are *all* satisfied by a system
whose forced core is a cycle. Therefore **no argument that uses only Hall/flow
data can prove Lemma A.** Any proof must at some point consume hypothesis (b),
hereditary FVS tightness, which is a statement about *feedback vertex sets in the
induced subgraphs of `G`* and is invisible to the flow network. Concretely: the
flow network sees only the bipartite incidence structure between `S` and `H`; it
does not see the edges of the forest `H`, and it is exactly the geometry of `H`
(which `H`-vertices lie in a common component, and how) that hereditary tightness
constrains. That is why the augmented forest quotient `Mhat_h` — the object that
does see `H`'s components — is the natural carrier of the missing information.

---

## (iii) The three witnesses: which strategy each kills, and how

All three live in `tools/witnesses/`. Each is an instance with a **forced-core
cycle**, so each is a situation Lemma A says cannot occur; each is legal only
because it **violates hereditary tightness** — I confirmed independently that in
all three `tau(G) < |S|`, i.e. `S` is not a minimum FVS. That is what stops them
from being counterexamples to Lemma A itself. What they *are* is counterexamples
to proposed **localizations**: statements of the form "if a forced cycle exists,
the hereditary violation must live in <specific set>". Every such proposal has
died on one of these three.

Fix the vocabulary. `F` = the forced-core cycle, `P` = its `S`-side, `Q` = its
`H`-side. For `s in P`, `A_s` = the unique minimum Hall-tight set containing `s`
(the *carrier*), and `B_s = A_s \ {s}` (the *puncture*), which is itself
Hall-tight.

### O-56 — kills **P-localization**

`S = {0,1,2,3}`, `H = {4,...,13}`; incidences `0~4,5,6`; `1~4,5,6`; `2~6,7`;
`3~6,8`; `H`-forest `9-4, 9-5, 4-10, 10-11, 6-12, 12-7, 6-13, 13-8`; fixed edge
`e = (10,11)`.

*Mechanism.* Vertices `2` and `3` each have exactly two `H`-neighbours, so both
are rigid: `2` takes `{6,7}` and `3` takes `{6,8}`. Between them they put load 2
on `6`, saturating `c(6) = 2`. So `0` and `1` are **pushed off** `6` and each must
take `{4,5}`. The selection is unique, everything is forced, and `0-4-1-5-0` is a
forced 4-cycle. Recomputed: 1 feasible selection, forced core
`{(0,4),(0,5),(1,4),(1,5),(2,6),(2,7),(3,6),(3,8)}`, forced-core cycle
`{0,1,4,5}`.

*What it kills.* The natural first proposal is: "the hereditary violation lies on
the cycle's own `S`-side `P`", i.e. `tau(G[H u P]) < |P|`. Recomputed here:
`tau(G[H u P]) = 2 = |P|` with FVS `{4,5}` — **`P` is clean**. The
inclusion-minimal violation is `X = {2,3}` with `tau(G[H u X]) = 1 < 2`
(delete `6`: the two cycles `2-6-12-7-2` and `3-6-13-8-3` share exactly `6`).
`{2,3}` is **disjoint from `P`**. So the violation can sit entirely off the
cycle, in the auxiliary vertices that did the pushing. O-56 also occupies the
single-external-blocker / acyclic-quotient subcase (blocker size 1), which is why
that subcase had to be proved separately rather than assumed to localize.

### O-63 — kills the **degree-2** and **degree≥3 ⟹ private cycle** localizations

`S = {s,t,u,a,b}`, `H = {r,x,q1,q2,h,w,z,y}`; `s~q1,q2,h`; `t~q1,q2`;
`u,a,b ~ h,w,z`; `H`-forest `r-q1, r-q2, r-h, r-w, r-z, q1-x, x-y`; `e = (x,y)`.

*Mechanism.* `u, a, b` have total demand 6 and their only neighbours are
`{h,w,z}` with total capacity 6, so they saturate `{h,w,z}` exactly. `s` is
therefore pushed off `h` and is rigid on `{q1,q2}`; `t` is rigid there anyway. The
forced 4-cycle is `s-q1-t-q2-s`. Recomputed: 6 feasible selections, forced core
exactly those four incidences, forced cycle `{s,t,q1,q2}`.

*What it kills.* Here `A_s = {s,u,a,b}` and `B_s = {u,a,b}`, both Hall-tight.
Two proposals died:

1. "*Every vertex of `B_s` has incidence-degree 2*" — recomputed: `u, a, b` all
   have incidence-degree **3**. False.
2. "*A `U_h`-vertex of incidence-degree `>= 3` has a private cycle avoiding `h`*"
   — false. Degree 3 only forces a cycle when two of the vertex's non-`h`
   neighbours land in the **same** component of `H - h`; the correct criterion is
   cyclicity of the augmented quotient `Mhat_h`, not the degree.

Also: the inclusion-minimal violation **inside `B_s`** is the *whole* of
`B_s = {u,a,b}` (recomputed `tau(G[H u {u,a,b}]) = 2 < 3`), with a size-2
blocker — not a single external vertex. So "the violation is a single blocker"
also dies here. (My scan additionally reports 2-element violations such as
`{s,u}` that reach outside `B_s`; the minimal violation *within* `B_s` is the
full set, as recorded.)

### O-64 — kills **`B_s`-localization** (and separates the capacity-1 branch)

`S = {s,t,u}`, `H = {q1,r,q2,y,h,w}`; `s~q1,q2,h`; `t~q1,q2`; `u~h,w`;
`H`-forest `q1-r, r-q2, q1-y, y-h, y-w`; fixed edge `e = (h,y)`, so
`c(h) = c(y) = 1`.

*Mechanism.* This is the **capacity-1** branch. `u` has only two neighbours
`{h,w}` so it is rigid and takes both; that single unit **saturates** `h`, whose
capacity is 1 because `h` is an endpoint of the fixed edge. `s` is pushed off `h`
and is rigid on `{q1,q2}`, as is `t`. Unique feasible selection; forced 4-cycle
`s-q1-t-q2-s`. Recomputed: 1 feasible selection, forced cycle `{s,t,q1,q2}`.

*What it kills.* After O-56 killed `P`-localization, the natural retreat was
`B_s`-localization: "the violation lives in the puncture `B_s`". Here
`A_s = {s,u}` and `B_s = {u}`. `B_s` is Hall-tight, but recomputed
`tau(G[H u B_s]) = 1 = |B_s|` — **`B_s` is clean**, and since `|B_s| = 1` no
subset of it can help either. The unique inclusion-minimal violation is
`X = P = {s,t}` with `tau(G[H u P]) = 1 < 2` (delete `q1`). So O-64 is the exact
mirror of O-56: there the violation was off `P` and inside the auxiliaries; here
it is on `P` and `B_s` is clean.

**Joint conclusion (this is the real content).** O-56 and O-64 together prove
that **no single one of `P`, `B_s` is a universal localizer**, in either
direction — the violating set is sometimes disjoint from `P` and sometimes equal
to it. O-63 additionally kills the two degree-based shortcuts for finding it. What
survives is only the weak disjunctive target: derive *either* a hereditary
violation somewhere in `P u (union_s A_s)` *or* a feasible exchange off the cycle.
That is why the carrier **family** (all `A_s` at once) rather than any single
carrier is the object the current attack uses. Two further recorded facts sharpen
the warning: O-64 shows capacity-1 and capacity-2 external neighbours are
genuinely separate branches, and it refutes the sharper conjecture
`tau(G[H u B_s]) = |B_s| - 1`.

---

## (iv) The `T_F` normalization (paper Lemma 4.7): statement, proof, and licence

**Statement.** Work in Lemma A° — the disconnected version: `G` bipartite (not
necessarily connected), `S` a minimum FVS, `H = G - S` a forest, `e in E(H)` with
the usual capacities. Suppose the instance has a forced-core cycle `F` with
`S`-side `P`. For each `s in P` let `A_s` be its canonical minimum Hall-tight
carrier, and set `T_F = union_{s in P} A_s`. Restrict to

  `G' = G[H u T_F]`,  `S' = T_F`,  same `H`, same `e`, same capacities.

Then (a) `G' - S' = H`; (b) `S'` is a minimum FVS of `G'`; (c) hereditary FVS
tightness holds for every `X subseteq T_F`; (d) the restricted system is feasible;
(e) every `A_s` is still Hall-tight and still exposes both forced `F`-edges at
`s`; (f) every edge of `F` is still **forced** in `G'`; (g) hence the forced core
of `G'` still contains `F`. Consequently a minimal counterexample to Lemma A° may
be assumed to satisfy `S = T_F`.

**Proof, and the one step that is easy to get wrong.**

(a) is immediate: deleting the `S`-vertices outside `T_F` does not touch `H`.

(b) and (c): for `X subseteq T_F subseteq S`, the graph `G'[H u X]` *is*
`G[H u X]` — the induced subgraph does not care that other `S`-vertices were
deleted, because `X` and `H` are the same vertices with the same induced edges.
So `tau(G'[H u X]) = tau(G[H u X]) = |X|` by hereditary tightness in `G`. Taking
`X = T_F` gives `tau(G') = |T_F| = |S'|`, so `S'` is a minimum FVS of `G'`, and
the same computation for every `X` gives hereditary tightness in `G'`. (This is
the point where "hereditary" earns its name: the hypothesis is preserved under
restriction *for free*, because it is a statement about induced subgraphs.)

(d) follows from (c) via the rooted-forest-extension route, exactly as for the
unrestricted instance.

(e)–(f) are the delicate part. **Forcedness is not monotone under restriction.**
Deleting `S`-vertices outside `T_F` *frees capacity* at `H`-vertices, so the
restricted instance can have strictly more feasible selections, and an incidence
that was forced in `G` could a priori become avoidable in `G'`. The proof
therefore does not attempt to inherit forcedness; it **re-derives** it. By the F1
characterization, an incidence is forced iff some Hall-tight set *exposes* it.
For `s in P`, the carrier `A_s` is contained in `T_F` by construction, so it
survives the restriction as a vertex set; and its tightness is computed from
`rho(A_s) = sum_h min(c(h), deg_{A_s}(h))`, which depends only on `A_s`'s own
incidences — vertices outside `T_F` never enter that sum. So `A_s` is still
tight in `G'`, still contains `s`, and still exposes both forced `F`-edges at `s`;
F1 then hands back forcedness **afresh** in `G'`. That gives (f), and (g) follows
since `F`'s edges are all of this kind.

**Two side conditions worth keeping visible.** First, **connectedness may be
lost** under the restriction — which is exactly why the lemma is stated for
Lemma A°, the disconnected version, and why Lemma A° being equivalent to the
connected form matters. (It is: raising all capacities to 2 only enlarges the
feasible set, so `forced(all caps 2) subseteq forced(caps for e)`, and a
disconnected instance splits into the `e`-component plus all-capacity-2
components.) Second, canonicity of `A_s` is not needed for validity — any tight
exposing sets would do — but it yields the *smallest* `T_F`, which is what the
downstream carrier lemmas want.

**What the normalization licenses, precisely.** It licenses the WLOG
`S = T_F` — "every `S`-vertex lies in the carrier of some cycle vertex" — when
hunting a minimal counterexample to Lemma A°. Concretely this buys:

- every `s in S` is in some Hall-tight `A_{s'}`, so the whole `S` side is covered
  by the tight-set lattice and no "inert" `S`-vertices remain to be argued about;
- the auxiliary vertices that do the *pushing* (the `{2,3}` of O-56, the
  `{u,a,b}` of O-63) are guaranteed present in the normalized instance, so a
  proof may use them; and
- searching for a hereditary violation may be confined to subsets of
  `T_F = S`, matching the "final human proof target" phrasing.

**What it does not license.** It does **not** say the violating set is `T_F`, nor
that it is `P`, nor that it is any `B_s`. O-56 (violation disjoint from `P`) and
O-64 (`B_s` clean, violation on `P`) forbid all three as universal claims. It
also does not apply to the three frozen witnesses at all — each has `S` not a
minimum FVS, so they sit outside the hypothesis class (they happen, set-
theoretically, to satisfy `S = T_F` anyway).

---

## Gauntlet outcome

Completed. Independent recomputation of all three witnesses reproduces the
recorded mechanism, the forced cycle, and the exact localization each one kills;
the abstract even-cycle system reproduces "Hall-feasible + forced-core cycle +
hereditary tightness violated" at `m = 3, 4`; a hereditarily tight negative
control has an acyclic (in fact empty) forced core. Frozen-oracle gold tests
also reproduce: `a1_verify.py 7` → `A1 = 143/143, failures = 0`;
`b_hslide.py 9` → 24,195 cycles, gap histogram `{0: 24195}`, 0 failures;
`b_hslide.py 10` → 448,577 cycles, gap histogram `{0: 448577}`, 0 failures.
All match `tools/README.md`'s recorded gold values, and every file in `tools/`
matches `tools/SHA256SUMS.txt`.

The gauntlet's inherited predecessor from `main-local` is preserved unmodified at
`work/GAUNTLET-inherited-from-main.md`.
