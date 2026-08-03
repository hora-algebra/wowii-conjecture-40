# Lemma A: two results from the banked carrier-family angle

Branch `attempt/2026-08-03-claude-opus-5-5047`, 2026-08-03.
ATTACK.md Step 3 target 1 ("the `T_F`-normalized carrier attack ... combine the
carrier lattice, punctured tightness, and the augmented forest quotient on
normalized instances. This angle was banked, never spent.").

Two things are recorded here. §1 is a new lemma, **MATHEMATICALLY PROVED** and
computationally checked. §2 is a methodological observation that makes a
targeted falsification search for Lemma A° possible for the first time, plus the
result of running it. §3 records what I could not do, so the next attempt does
not re-walk it.

Notation as in the paper. `G` bipartite (connectedness never used below), `S` a
vertex set with `H = G - S` a forest, `e = (x,y)` a fixed edge of `H`,
`c(h) = 2` except `c(x) = c(y) = 1`, demand 2 at every `s in S`.
`rho(X) = sum_h min(c(h), deg_X(h))`, `delta(X) = rho(X) - 2|X|`; *tight* means
`delta(X) = 0` (Hall tightness, **not** FVS tightness). `A_s` is the canonical
carrier of `s` (Lemma 4.4: the unique inclusion-minimal tight set containing
`s`), `B_s = A_s \ {s}`.

---

## 1. Carrier–cycle separation

Suppose the forced core contains a cycle. Because every `s in S` has selected
degree exactly 2 and every `h in H` has load at most `c(h) <= 2`, the forced
core has maximum degree 2; so a forced cycle is a cyclic component

    F :  s_1 - q_1 - s_2 - q_2 - ... - s_m - q_m - s_1      (m >= 2)

alternating between `P = {s_1,...,s_m}` and `Q = {q_1,...,q_m}`, with `s_i`
incident on `F` to `q_{i-1}` and `q_i` (indices mod `m`). Each `q_i` carries two
forced incidences, so `c(q_i) = 2`. Write

    U = union of B_s over s in P ,      T = P u U ( = T_F ).

> **Lemma CS (carrier–cycle separation).** Assume the system is feasible and the
> forced core contains the cycle `F` above. Then
>
> **(a)** for every `s in P \ U`, both forced ends `q` of `s` satisfy
> `deg_U(q) <= c(q) - 1 = 1`;
>
> **(b)** if `s_i` and `s_{i+1}` are consecutive on `F` and both lie in
> `P \ U`, then their shared end has `deg_U(q_i) = 0`;
>
> **(c)** consequently, if `P ∩ U = empty` then `deg_U(q) = 0` for **every**
> `q in Q`: no vertex of any puncture is adjacent to any vertex of the forced
> cycle's `H`-side. Under the `T_F` normalization (`S = T_F = P u U`,
> Lemma 4.7) this reads `N_S(q) ⊆ P` for every `q in Q`.
>
> **(d)** (by-product) `U u R` is tight for **every** `R ⊆ P \ U`.

Only the Hall layer is used: feasibility, submodularity of `delta`, the
tight-set lattice (Lemma 3.6), the canonical carrier (Lemma 4.4) and punctured
tightness (Lemma 4.5). Hereditary FVS tightness is **not** needed, so the lemma
holds on the three warning witnesses too (checked, §1.3).

### 1.1 Proof

*Step 1 — `U` and `T` are tight.* Each `A_s` is tight by definition and each
`B_s` is tight by punctured tightness (Lemma 4.5). The tight sets are closed
under union (Lemma 3.6, from submodularity and `delta >= 0`). `U` is the union
of the `B_s` and `T` is the union of the `A_s`, so both are tight:
`rho(U) = 2|U|`, `rho(T) = 2|T|`.

*Step 2 — the marginal of a single `s in P \ U`.* For any `Y ⊇ U` with
`s ∉ Y`,

    rho(Y u {s}) - rho(Y) = #{ h in N_H(s) : deg_Y(h) < c(h) } .

Let `h in N_H(s)` be **not** one of the two forced ends of `s`. Punctured
tightness gives `deg_{A_s}(h) >= c(h) + 1`, hence
`deg_{B_s}(h) >= c(h)` (removing the single vertex `s` drops the degree by at
most one), and `B_s ⊆ U ⊆ Y`, so `deg_Y(h) >= c(h)`: such an `h` contributes
nothing. Only the two forced ends `q^-, q^+` of `s` can contribute, so

    rho(Y u {s}) - rho(Y) <= 2,

with equality iff `deg_Y(q^-) < c(q^-)` and `deg_Y(q^+) < c(q^+)`.  (†)

*Step 3 — every marginal is exactly 2; this is (a) and (d).*
Write `P \ U = {p_1, ..., p_r}` in any order and put
`U_j = U u {p_1,...,p_j}`, so `U_0 = U` and `U_r = T`. Telescoping,

    sum_{j=1..r} ( rho(U_j) - rho(U_{j-1}) ) = rho(T) - rho(U)
                                             = 2|T| - 2|U| = 2r,

because `T = P u U` gives `|T| - |U| = |P \ U| = r`. Each summand is at most
`rho(U u {p_j}) - rho(U)` by submodularity of `rho`, and that is at most 2 by
(†). A sum of `r` terms each `<= 2` equalling `2r` forces every term to be
exactly 2 — and forces `rho(U_j) = 2|U_j|` for every `j`, which is (d) once one
notes the ordering was arbitrary, so any `R ⊆ P \ U` can be taken first.
Since the ordering is arbitrary, in particular `rho(U u {p}) - rho(U) = 2` for
every `p in P \ U`, and (†) with `Y = U` gives (a).

*Step 4 — (b).* Let `s_i, s_{i+1} in P \ U` share the end `q_i`. Take the order
`p_1 = s_i`, `p_2 = s_{i+1}`. By Step 3 the second increment is exactly 2:

    rho(U u {s_i, s_{i+1}}) - rho(U u {s_i}) = 2 .

By (†) with `Y = U u {s_i}` the only contributors are the two forced ends
`q_i, q_{i+1}` of `s_{i+1}`, each contributing at most 1, so each contributes
exactly 1. Write `d = deg_U(q_i)`. Then `deg_{U u {s_i}}(q_i) = d + 1` and

    contribution at q_i = min(2, d+2) - min(2, d+1) = 1
      <=>  min(2, d+1) = 1  <=>  d + 1 <= 1  <=>  d = 0 .

*Step 5 — (c).* If `P ∩ U = empty` then `P \ U = P`, so every consecutive pair
`s_i, s_{i+1}` qualifies for (b) and every `q_i` gets `deg_U(q_i) = 0`. (For
`m = 2` the two consecutive pairs are `(s_1,s_2)` and `(s_2,s_1)`, covering both
`q_1` and `q_2`.) Under `S = T_F = P u U`, `deg_U(q) = 0` means every
`S`-neighbour of `q` lies in `P`. ∎

### 1.2 What it says, and how it fits the open problem

The `A_s` and `B_s` were previously used one carrier at a time (Lemmas 4.4–4.6
and the `U_h`/blocker analysis). Lemma CS is the first statement that uses the
whole **family** `{A_s : s in P}` at once, which is precisely the angle ATTACK.md
records as banked. Its content is a *separation*: the auxiliary machinery `U`
that does the forcing never touches the vertices `Q` it forces the cycle onto.
Combined with

* Lemma A-I (some `s in P` must have an `H`-neighbour outside `Q`, else
  hereditary tightness fails), and
* punctured tightness (every such external neighbour `h` has
  `deg_{B_s}(h) >= c(h)`, so `h` **is** touched by `U`),

the normalized picture is: `H`-vertices split into the cycle's own `Q`, on which
only `P` acts, and the external neighbourhood of `P`, each of whose vertices is
saturated from inside `U`. The two parts of `S` interact only away from `Q`.

### 1.3 Verification

`work/carrier.py` enumerates **abstract** systems `(S, H, incidences,
capacities)` — the layer on which everything above is defined — keeps those with
a cyclic forced core, and tests punctured tightness, CS(a), CS(b), CS(c). It
carries two negative controls (statements known to be false, which must fail,
so that "0 failures" is not an artefact of dead code): `CTRL-DEG2` = "every
`B_s`-vertex has incidence-degree 2" (refuted by O-63), and `CTRL-PDIS` =
`P ∩ U = empty`.

| run | systems | with cyclic forced core | CS/PT failures | controls fired |
|---|---|---|---|---|
| `carrier.py exhaustive 3 5` | 115,774 | 798 | **0** | `CTRL-PDIS` 18 |
| `carrier.py random 20000 1` | 20,000 | 547 | **0** | `CTRL-DEG2` 142, `CTRL-PDIS` 251 |
| `carrier.py random 400000 777` | 400,000 | 11,097 | **0** | `CTRL-DEG2` 2,643, `CTRL-PDIS` 4,931 |

Also checked directly on the three frozen witnesses (`work/wcheck.py` computes
the same carriers): O-56 `U = {2,3}`, `Q = {4,5}`, `deg_U(4) = deg_U(5) = 0`;
O-63 `U = {u,a,b}`, `deg_U(q1) = deg_U(q2) = 0`; O-64 `U = {u}`,
`deg_U(q1) = deg_U(q2) = 0`. All consistent with (c), and all three happen to
have `P ∩ U = empty`.

**Important scope note.** `CTRL-PDIS` fired on 4,931 of the 11,097 random cyclic
systems, i.e. `P ∩ U != empty` about 44% of the time. So the clean form (c) is
**not** generically available; only (a) and (b) are unconditional. Do not build
an argument that assumes `P ∩ U = empty`.

---

## 2. A factorised falsification search for Lemma A°

### 2.1 The observation

> Hereditary FVS tightness for every `X ⊆ S` is **equivalent** to "`S` is a
> minimum FVS of `G`".

`(<=)` is Lemma 3.3. `(=>)` is immediate: take `X = S` to get `tau(G) = |S|`,
and `S` is an FVS because `G - S = H` is a forest. Both directions are one line;
the point is what it buys.

A counterexample to Lemma A° is therefore exactly a bipartite `G`
(connectedness not required) with a **minimum** FVS `S`, a fixed `H`-edge `e`,
and a cyclic forced core. Now note which data each half depends on:

* whether the forced core is cyclic depends **only** on the abstract system
  `(S, H-vertices, incidences, capacities)`. Feasibility and forcedness are
  pure `b`-matching questions; the `H`-forest edges never enter.
* whether `S` is a minimum FVS depends, for fixed incidences, **only** on the
  `H`-forest edges.

So the search **factorises**: enumerate abstract systems with a cyclic forced
core, then, for each, enumerate every bipartite-consistent `H`-forest completion
and ask whether `tau(G) = |S|`. Every previous search in the repository
(O-52…O-56, O-68…O-82) varied incidences and forest together on one hand-built
skeleton, which is why it could only ever produce single instances.

Two further reductions make the completions cheap:

* connectedness is not required (Problem 4.1 is stated without it), so no
  connectivity constraint is imposed on the completion;
* if the abstract system has all capacities 2, the fixed edge can be supplied by
  a **separate `K_2` component** whose endpoints carry no incidences. They then
  have `c = 1` legitimately and contribute nothing to `tau`. (Conversely, for a
  fixed graph, raising capacities only enlarges the feasible set, so
  `forced(all caps 2) ⊆ forced(caps for e)` for every `e`; the all-caps-2 case
  is therefore implied by the fixed-edge case and is not an untested gap.)

### 2.2 The search and its calibration

`work/larealize.py`. Stage 1 uses `carrier.py`'s generators; stage 2 enumerates
every proper 2-colouring of the incidence graph, every bipartite-legal edge set
on the `H`-vertices plus up to `k` extra incidence-free ("Steiner") `H`-vertices
that is a forest and contains the required `c = 1` edge, and computes `tau(G)`
by brute-force minimum FVS.

**Positive control.** "No completion of a cyclic system reaches `tau = |S|`"
would be worthless if the completion loop never reached `tau = |S|` at all. So
the same loop is run on systems with an **acyclic** forced core, where minimum-FVS
completions must exist. It does reach them: in the `k <= 3, p <= 4`,
2-Steiner run, 3,968 of 55,846 control completions (7.1%) had `tau(G) = |S|`.

### 2.3 Result

| run | cyclic systems | forest completions of them | with `tau(G) = |S|` (= Lemma A° counterexample) |
|---|---|---|---|
| `exhaustive 3 4`, 0 Steiner | 438 | 732 | **0** |
| `exhaustive 3 4`, 1 Steiner | 438 | 6,768 | **0** |
| `exhaustive 3 4`, 2 Steiner | 438 | 77,976 | **0** |
| `exhaustive 3 4`, 3 Steiner | 438 | 1,070,160 | **0** |

In every completion the deficit `|S| - tau(G)` was 1 or 2 — never 0.

**Status: COMPUTATIONALLY VERIFIED** (universe: abstract systems with
`|S| <= 3`, `|H| <= 4` and up to three incidence-free extra `H`-vertices; all
bipartite-legal forest completions; positive control passing). This is *not* a
proof and the universe is small — but it is the first search of the
counterexample space that is exhaustive in both coordinates, and it is
calibrated.

### 2.4 Localization data (the actual open question)

The open target asks *where* the hereditary violation sits (the repository has
exactly three data points: O-56 inside `B_s`, O-63 the whole `B_s`, O-64 on
`P`). The search produces one such data point per completion. Over a spread
sample of 876 completions from the `k <= 3, p <= 4`, 2-Steiner run, the
inclusion-minimal violating `X ⊆ S`:

| location of the inclusion-minimal violating `X` | count |
|---|---|
| `X ⊆ P` | 504 |
| `X ⊆ P` and `X ⊆ B_s` for some `s` (small overlaps) | 27 |
| mixed (neither inside `P` nor inside any `B_s`) | 345 |
| size 1 / size 2 | 583 / 293 |

The headline is the last row of the middle block: **39% of the violating sets
are "mixed"** — contained neither in `P` nor in any single puncture. That is a
stronger negative than the three witnesses gave (they only showed no *single*
one of `P`, `B_s`, `T_F` is universal); it says a large fraction of cases are
not covered by *any* of the localizations that have been proposed, and any
future localization claim should be tested against this population first.

---

## 3. What I could not do (do not re-walk)

* **Turning Lemma CS into a contradiction.** The natural move after (c) is to
  build an FVS of `G` of size `|S| - 1` as `(Q \ {q_j}) u U`, of size
  `(m-1) + |U|`. That requires `Q \ {q_j}` to be an FVS of `G[H u P]`, i.e.
  `tau(G[H u P]) <= m - 1` — which is the P-local bridge, already refuted as a
  *route* by O-55/O-56. Lemma CS does not repair it: in O-56 the quotient of `P`
  over the components of `H - (Q \ {q_j})` is cyclic for both choices of `j`
  (checked: `0` and `1` still share the external neighbour `6`), so no `j`
  works. Lemma CS constrains `U` near `Q`; it says nothing about how `P`'s
  external neighbours sit in the `H`-forest, which is what the blocker needs.
* **Assuming `P ∩ U = empty`.** It fails in ~44% of abstract cyclic systems
  (§1.3), so (c) is not available in general.
* **A three-matroid framing of `F2`.** Suppressing each `s` (which has selected
  degree exactly 2) turns a feasible selection into a multigraph on `H` with
  one edge per `s` and `deg(h) <= c(h)`; selected cycles become cycles of that
  multigraph. So `F2` is exactly "pick one edge `sigma(s) ⊆ N_H(s)` per `s`,
  all distinct, forming a **linear forest** on `H` with `x, y` of degree
  `<= 1`". "Distinct, one per `s`" is a transversal matroid and "forest" is the
  graphic matroid, but the degree bound is not a matroid constraint
  (on the path `a-b-c-d` with `c(b) = c(c) = 1`, `{bc}` is maximal of size 1
  while `{ab, cd}` has size 2), so this is not a two-matroid intersection and
  Edmonds' theorem does not apply. Recorded because the reformulation is clean
  and worth having, and because the obstruction to using it is definite.
