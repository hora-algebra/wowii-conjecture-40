# ATTEMPT REPORT

**Branch** `attempt/2026-08-03-claude-opus-5-5047`
**Model / harness** Claude Opus 5 (1M context), Claude Code CLI, macOS 8-core
(6P+2E), Python 3.9.6, clang -O2, `nauty` `geng` from Homebrew.
**Date** 2026-08-03. Clone at `main` = `0617d7a`, tags v1.0/v1.1.
**Outcome in one line** — no counterexample and no proof of Lemma A, Lemma B or
SV; verified movement on four fronts: the paper's weakest computational claim
(Lemma A at n = 11) is now reproducible and dual-engine, Lemma A is verified
exhaustively at n = 12 and n = 13, F2 (the statement the bipartite case actually
needs) is verified directly for the first time through n = 13, and the lifting
inequality (ATTACK.md target 4, previously untouched) is preregistered,
exhaustively scanned, and **proved for a structured class covering 94% of the
small universe**. One new lemma on the banked carrier-family angle is proved.

---

## Step 0 — freshness check (network available)

| source | checked | finding |
|---|---|---|
| (a) issues / PRs on `cozuya/wowii-conjecture-40` | `gh issue list --state all --json`, `gh pr list --state all --json` | `[]` and `[]` — none, ever |
| (b) MathOverflow 513887 | fetched with `curl` and parsed (WebFetch is blocked for mathoverflow.net in this harness) | title *"Can the forced edges of an exact-demand capacitated selection in a bipartite incidence model form a cycle, given hereditary FVS tightness?"*, asked **2026-08-03 19:18:25Z (today)**, `answerCount = 0`, 0 comments |
| (c) WOWII open list | `curl http://cms.uhd.edu/faculty/delavinae/research/wowII/open.html` | Conjecture 40 still carries the status letter **O** (open). The only dated annotation is DeLaViña's 2004-03-06 remark that `f(G) >= b(G)/2 + 1`, settling the path-cover-number-1 case. No status change. |
| (d) arXiv / web | arXiv API queries `all:"Graffiti.pc"`, `all:"decycling number" AND all:"odd cycle transversal"`, `all:"forest number" AND all:"path cover number"`, `abs:"conjecture 40" AND abs:"graph"`; two web searches | Nothing on Conjecture 40 or on Lemmas A/B/SV. One recent hit: *"The 2-Domination Number and the Upper Median Degree: A Proof of Graffiti.pc Conjecture 387"* (arXiv, 2026-07-28) — different conjecture, unrelated. A `formal-conjectures` PR disproving **WOWII 103** — different conjecture. |

Nothing has been resolved by others; the run's job is unchanged.

## Step 0.5 — prior attempts

`git fetch origin 'refs/heads/attempt/*:refs/remotes/origin/attempt/*'` brought
nothing; `git ls-remote --heads origin` lists exactly `refs/heads/main` and
`refs/heads/release/v1.1`. `attempts/LESSONS.md` ends with "(No entries yet.)".
**I am the first post-v1.1 attempt.** There are no `[FALSIFIED]` or `[DEAD END]`
entries to refute; the binding prior knowledge is ATTACK.md Step 2 plus the
ledgers, which I read in full (`ledgers/RESULT_RECORD.md` O-1 … O-84,
`ledgers/PHASE0_RECORD.md`, `proofs/PROOFS.md`, both challenge sheets).

## Step 1 — gauntlet

**Completed.** `GAUNTLET.md` on this branch covers (i) the Theorem 3.13
reduction chain with the exact role of every ingredient and a table of what is
load-bearing where, (ii) the abstract even-cycle system with the computation
`rho(X) = 2|X|` for *every* `X` and `tau(G[H u S]) = 1 < m`, (iii) all three
witnesses with the mechanism of the forcing and the exact localization each
kills, (iv) the `T_F` normalization with proof and a precise statement of what
it does and does not license.

Two by-products of writing it:

* Every witness value was re-derived with independently written code
  (`work/wcheck.py`: fresh feasibility, forced core, `rho`, all Hall-tight
  sets, carriers, punctures, and `tau(G[H u X])` for **every** `X ⊆ S`). All
  recorded values reproduced.
* **Documentation discrepancy.** `proofs/PROOFS.md` §D says "O-56 and O-63 are
  already normalized (`S = T_F`); O-64 lies OUTSIDE the hereditary-tightness
  class (its `S` is not a minimum FVS), so the normalization does not apply to
  it." Measured: `tau(G[H u S])` vs `|S|` is 2 vs 4 (O-56), 3 vs 5 (O-63), 2 vs
  3 (O-64) — **all three** are outside the class (necessarily, since a
  hereditarily tight instance with a forced cycle is what Lemma A° forbids), and
  **all three** satisfy `S = T_F` (O-64: `A_s = {s,u}`, `A_t = {t}`). The
  sentence's implicature is wrong; no mathematical claim depends on it.

## Step 4 — oracle contact and gold tests

`shasum -a 256 -c tools/SHA256SUMS.txt` → **17/17 OK** before any use.
Gold reproductions against `tools/README.md`:

| gold | expected | got |
|---|---|---|
| `a1_verify.py 7` | `A1 = 143/143`, 0 failures | identical |
| `b_hslide.py 9` | 24,195 cycles, gap `{0: 24195}`, 0 failures | identical |
| `b_hslide.py 10` | 448,577 cycles, gap `{0: 448577}`, 0 failures | identical |
| `forced_core.py 10` | ledger O-44: max path 8, hist `{1:127,2:55734,3:10,4:3170,6:150,8:8}` | identical |

Every new checker I wrote carries a **positive control** — an instance where it
must report failure — so that a clean run is evidence rather than an artefact.

---

## Results

### R1. Lemma A at n = 11 is now a reproducible, hash-verified run

Paper §4.1, footnote: *"An n=11 run over 994,607 instances reported zero cyclic
cores and maximum forced-path length 8; that run is recorded in a preserved
intermediate report, incompletely ledgered, and not independently reproducible
from a completion artifact. We therefore do not claim exhaustive n=11
verification of Lemma A."* `proofs/PROOFS.md` §D and
`proofs/LEMMA-A-CHALLENGE.md` carry the same caveat.

Re-ran the shipped, hash-verified checker:

```
cd tools && python3 forced_core.py 11
```
```
instances = 994607
CYCLIC forced core (= all-R3 cycle exists = Lemma A FAILS) = 0
instances with empty forced core = 514372
non-forest forced cores = 0
max forced-core path length (edges) over acyclic cores = 8
forced-core path-length histogram = {1: 740, 2: 457749, 3: 52, 4: 20732, 6: 930, 8: 32}
forced-core component-size histogram = {0: 514372, 2: 1529, 3: 549874, 4: 52, 5: 20826, 7: 930, 9: 32}
```
414 s wall. Instance count and max path length match the footnote exactly, and
the run is reproducible from `tools/` at the published hashes
(`forced_core.py` `ba8b0ba5…`, plus `inv_b.py`, `experiment_b.py`,
`eval_frozen.py`, `eval_L1_holdout.py`, all `OK` against `SHA256SUMS.txt`).

**Status: COMPUTATIONALLY VERIFIED.** Universe: all 25,598 connected bipartite
graphs on 11 vertices, every minimum FVS, every edge of `H` — 994,607 instances.

### R2. An independent second engine, and Lemma A at n = 12 and n = 13

`work/fcore.c` (sha256 `598bb06f…`) decides forcedness by the **flow**
characterization (paper Theorem 3.10: release the incidence and ask for a
residual augmentation) rather than by intersecting every feasible selection.
Algorithmically distinct; no shared code.

*Cross-validation.* Field-for-field identical to `forced_core.py` at
n = 8, 9, 10, 11 on every reported quantity — instances, empty cores, cyclic
cores, non-forest cores, max forced-path length, and both histograms.
Two independent engines now certify Lemma A over the whole `n <= 11` universe.

*Positive control.* On the three warning witnesses (not reachable from `geng`,
so supplied explicitly) the engine reports cycle rank 1 and forced-core sizes
8 / 4 / 6 — matching `work/wcheck.py`. So it can and does detect a cyclic core.

*New frontier.*

| n | connected bipartite graphs | instances `(G,S,e)` | cyclic forced cores | max forced path | runtime |
|---|---|---|---|---|---|
| 11 | 25,598 | 994,607 | **0** | 8 | 0.4 s |
| 12 | 212,780 | 10,970,519 | **0** | 10 | 6.6 s |
| 13 | 2,241,730 | 141,887,501 | **0** | 10 | 115 s |
| 14 | see §"Jobs" below | | | | |

`infeasible (G,S,e) skipped = 0` at every order — an empirical confirmation of
Corollary 3.8 (a feasible selection exists for every distinguished edge) over
155M instances.

**Status: COMPUTATIONALLY VERIFIED**, universe as tabulated. Previous published
frontier: exhaustive n ≤ 10 plus the unreproducible n = 11 report.

### R3. F2 verified directly, for the first time, through n = 13

Theorem 3.13 needs only

> **F2.** for some `e in E(H)` there is an acyclic feasible selection,

and Lemma A + Lemma B + descent is a *route* to F2, not an equivalent of it. F2
itself is not scanned anywhere in the repository. `work/f2.c` (sha256
`e528a4ae…`) tests the stronger universal form **F2-ALL** (every minimum FVS,
every fixed edge) directly, by searching for the acyclic selection.

The search uses a reformulation derived in `GAUNTLET.md`: since every `s` has
selected degree exactly 2, suppressing the `s` vertices carries a feasible
selection to a multigraph on `H` with one edge per `s` and `deg(h) <= c(h)`, and
selected cycles become cycles of that multigraph. So an acyclic feasible
selection is exactly a **linear forest on `H` with `|S|` edges admitting a
system of distinct representatives into `S`**; the program backtracks over that
with incremental union-find, most-constrained `s` first.

| n | instances | F2-ALL failures | F2-SOME failures | runtime |
|---|---|---|---|---|
| 8 | 2,186 | 0 | 0 | <0.01 s |
| 9 | 13,003 | 0 | 0 | 0.01 s |
| 10 | 116,216 | 0 | 0 | 0.03 s |
| 11 | 994,607 | 0 | 0 | 0.28 s |
| 12 | 10,970,519 | 0 | 0 | 4.3 s |
| 13 | 141,887,501 | **0** | **0** | 85 s |

Instance counts agree exactly with `fcore` at every order (independent
enumeration). Positive control: on O-56, O-63, O-64 the search correctly finds
**no** acyclic feasible selection.

**Status: COMPUTATIONALLY VERIFIED.** At `n <= 10` this was already implied by
Lemma A + A1/U1; at `n = 11` it was implied only modulo the unreproducible
Lemma-A run; at `n = 12, 13` it is new, and everywhere it is now *direct*
rather than inferred through the descent.

### R4. A new proved lemma on the banked carrier-family angle

ATTACK.md Step 3 target 1 records the `T_F`-normalized carrier attack as
"banked, never spent". `LEMMA-A-CARRIER.md` §1 spends part of it.

> **Lemma CS (carrier–cycle separation).** Let the forced core contain a cycle
> `F = s_1 q_1 … s_m q_m` with `S`-side `P` and `H`-side `Q`, and put
> `U = ⋃_{s in P} B_s` where `B_s = A_s \ {s}` is the punctured carrier. Then
> (a) every `s in P \ U` has `deg_U(q) <= c(q) - 1 = 1` at both of its forced
> ends; (b) if `s_i, s_{i+1}` are consecutive on `F` and both lie in `P \ U`
> then `deg_U(q_i) = 0`; (c) hence if `P ∩ U = ∅` then no vertex of any
> puncture is adjacent to any vertex of `Q`; (d) `U u R` is tight for every
> `R ⊆ P \ U`.

Proof (in `LEMMA-A-CARRIER.md` §1.1) is four short steps: `U` and `T_F = P u U`
are tight by the lattice; the marginal of adding one `s in P \ U` to `U` is at
most 2 because punctured tightness saturates every non-forced-end neighbour
inside `B_s ⊆ U`; the telescoping sum `rho(T_F) - rho(U) = 2|P \ U|` then forces
every marginal to be exactly 2; and applying that to two consecutive cycle
vertices pins the shared end at `deg_U = 0`.

This is the first statement that uses the whole family `{A_s : s in P}` at once
rather than one carrier at a time. Only the Hall layer is used — feasibility,
submodularity, the tight-set lattice, the canonical carrier, punctured tightness
— so hereditary FVS tightness is not needed and the lemma holds on the three
witnesses too.

**Status: MATHEMATICALLY PROVED, not Lean-formalized.** Checked by
`work/carrier.py` on abstract systems with a cyclic forced core: 798 (exhaustive
`|S| <= 3, |H| <= 5`), 547 and 11,097 (random) — **0 failures**, with two
negative controls firing (`CTRL-DEG2`, the O-63-refuted degree hypothesis:
2,643 fires; `CTRL-PDIS`: `P ∩ U != ∅` in 4,931 of 11,097 cases).

That last number is itself a scope warning worth recording: `P ∩ U != ∅` about
**44%** of the time, so the clean corollary (c) is not generically available.

### R5. A factorised falsification search for Lemma A°

`LEMMA-A-CARRIER.md` §2. The enabling observation is one line:

> hereditary FVS tightness for every `X ⊆ S` **is equivalent to** "`S` is a
> minimum FVS of `G`" (`<=` is Lemma 3.3; `=>` is `X = S`).

Consequently a Lemma-A° counterexample is a bipartite `G` (connectedness not
required) with a *minimum* FVS `S` and a cyclic forced core — and the two halves
depend on **disjoint data**: cyclicity of the forced core depends only on the
abstract system `(S, H-vertices, incidences, capacities)`, while
minimum-FVS-ness depends, for fixed incidences, only on the `H`-forest edges.
So the search factorises into two independent enumerations. Every previous
search in the repository (O-52…O-56, O-68…O-82) varied both at once on a single
hand-built skeleton, which is why it could only produce one instance at a time.

`work/larealize.py` runs it: stage 1 enumerates abstract systems with a cyclic
forced core; stage 2 enumerates, for each, every proper 2-colouring and every
bipartite-legal `H`-forest completion (including up to three incidence-free
extra `H`-vertices), and computes `tau(G)`.

| run | cyclic systems | forest completions | with `tau(G) = |S|` |
|---|---|---|---|
| `exhaustive 3 4`, 0 / 1 / 2 / 3 Steiner | 438 | 732 / 6,768 / 77,976 / 1,070,160 | **0 / 0 / 0 / 0** |
| `exhaustive 3 5`, 2 Steiner | 798 | 590,796 | **0** |
| `random 20000 seed 555`, 1 Steiner (`|S| <= 5`, `|H| <= 6`) | 682 | 732,016 | **0** |

Counting the three non-nested universes, **2,392,972 forest completions of
systems with a cyclic forced core, zero counterexamples**. Five random systems
hit the declared 50,000-completions-per-system cap; that is reported rather than
silently dropped.

**Positive control** (essential): the same completion loop on *acyclic*-core
systems reaches `tau(G) = |S|` in 3,968 of 55,846 completions (7.1%) in the
exhaustive run and 50,944 of 233,924 (21.8%) in the random run, so the loop
demonstrably can produce genuine minimum-FVS instances.

**Status: COMPUTATIONALLY VERIFIED** (universe: abstract systems with `|S| <= 3`,
`|H| <= 5`, up to 3 incidence-free extra `H`-vertices, plus a random `|S| <= 5`,
`|H| <= 6` layer; all bipartite-legal forest completions). Not a proof, and the
universe is small — but it is the
first search of the counterexample space that is exhaustive in *both*
coordinates and is calibrated.

*Localization data.* Each miss yields the inclusion-minimal violating `X ⊆ S`,
which is exactly what the open target asks about and of which the repository had
three hand-built points. Over a spread sample of 876 completions: `X ⊆ P` in
504, `X` inside some `B_s` in 27, and **`X` "mixed" — inside neither `P` nor any
single `B_s` — in 345 (39%)**. The witnesses showed no *single* one of `P`,
`B_s`, `T_F` is universal; this says a large fraction of cases escape *all* of
the proposed localizations at once.

### R6. The lifting inequality (ATTACK.md target 4) — preregistered scan and a proved class

Nothing in `ledgers/` or `proofs/` records any computation on target 4. I
preregistered it before writing any checker: `PREREG-LIFT.md` fixes the
statements, the universe, the decision rules and the gold suite;
`work/LIFT-SHA256.txt` records `lift.c` = `c0cc2dd315144a0c9c64c875234e193fd8f700e01949ea6668964220a4d01c5e`;
both were committed (`5e93527`) **before** the first sweep. The checker reuses
the exact invariant primitives of the frozen `verification/phase0.c`, and its
gold suite reproduces phase0's `(f,b,p)` golds (`K_10`, `K_{5,5}`, `K_{1,9}`,
`C_10`, `K_{2,2,2}`, `K_{1,1,1,3}`) plus eight lifting-specific golds.

Frozen statements: **LIFT-A** (∃ minimum OCT `T`: `ell(G) >= 2 tau(G-T) + |T| + 1`),
**LIFT-A-ALL** (same for every minimum `T`), **LIFT-P** (∃ `T`: `p(G) <= p(G-T)`),
**LIFT-P-ALL**, and **SV** as a cross-check.

| n | connected graphs | nonbipartite | LIFT-A fail | LIFT-A-ALL fail | LIFT-P fail | LIFT-P-ALL fail | SV fail |
|---|---|---|---|---|---|---|---|
| 3–6 | 141 | 115 | 0 | 0 | 0 | 0 | 0 |
| 7 | 853 | 809 | 0 | 0 | 0 | 3 | 0 |
| 8 | 11,117 | 10,935 | 0 | 0 | 0 | 16 | 0 |
| 9 | 261,080 | 260,350 | 0 | 0 | 0 | 150 | 0 |
| **10** | **11,716,571** | **11,712,539** | **0** | **0** | **0** | 2,130 | **0** |

Every statement above was frozen in `PREREG-LIFT.md` and the checker hashed and
committed **before the first sweep**, so the whole range `3 <= n <= 10` is a
prospective test, not a fit.

Two accounting checks the preregistration required, both passing: the n = 10
shard counts (four `geng` residue classes) sum to exactly **11,716,571**, the
known number of connected graphs on 10 vertices; and the nonbipartite count is
exactly **11,712,539**, which is the same number the paper reports for its SV
verification at n = 10 — an independent reproduction of that census. The SV
column likewise reproduces the paper's SV result for every `n <= 10` with a
checker written from the definition rather than from `phase0.c`'s `run2`.

n = 10 wall time 1,334–1,526 s per shard at ~2,000 graphs/s, four shards.
Best-`T` slack histogram over all 11,712,539 nonbipartite graphs:
`{0: 52,303, 1: 333,485, 2: 1,311,405, 3: 3,227,682, 4: 3,852,977, 5: 2,614,879, 6: 317,201, 7: 2,607}`.
Minimum slack is 0, i.e. the inequality is attained.

*Dual engine.* `work/liftcheck2.py` is an independently written pure-Python
implementation of the five frozen statements. It agrees with `lift.c`
field-for-field — including the complete slack histograms — at n = 6, 7, 8.

Two things the scan says beyond "no counterexample":

* **LIFT-A-ALL** holds — the inequality is true for *every* minimum OCT, not
  just some, throughout the scanned range. That is a stronger statement than the
  target and worth freezing for a future holdout.
* **LIFT-P-ALL is FALSIFIED** from n = 7 (first witness `H???FA^`, n=9 entry in
  `work/lift-witness-n9.txt`): the path-cover form genuinely needs its
  existential quantifier over minimum OCTs.
* the best-`T` slack `max_T [ell - 2 tau(G-T) - |T| - 1]` is 0 for 2,494 graphs
  at n = 9 and 52,303 at n = 10, so the inequality is tight on a substantial
  family — it is a sharp statement, not a slack one.

**A structured class, proved.** ATTACK.md target 4 also asks for a proof on a
structured class.

> **L1.** For bipartite `B` on `n_B` vertices with `c_e` edge-containing
> components, `f(B) >= ceil(n_B/2) + c_e`, i.e. `tau(B) <= floor(n_B/2) - c_e`.
> *Proof.* In each component take the larger bipartition class (independent, so
> a forest, of size `>= ceil(n_i/2)`); if that component has an edge, add one
> vertex of the other class — the induced subgraph is a star plus isolated
> vertices, still a forest. Union over components. ∎
>
> **L2.** If some minimum OCT `T` of a connected nonbipartite `G` satisfies
> `p(G) <= 2 c_e(G-T) - 1`, then LIFT-A holds at `G` with that `T`.
> *Proof.* `2 tau(G-T) + |T| + 1 <= 2 floor(n_B/2) - 2c_e + o + 1 <= n + 1 - 2c_e
> <= n - p(G) = ell(G)`. ∎
>
> **Corollary.** LIFT-A holds for every **traceable** connected nonbipartite `G`
> (`p = 1`, and `c_e >= 1` by paper Lemma 5.1). Since LIFT-A implies
> `ell + o >= 2 tau + 1` unconditionally, this re-proves Conjecture 40 for
> traceable graphs.

*Provenance, stated plainly:* for a connected `B` the engine of L1 is
DeLaViña's 2004 remark `f >= b/2 + 1` recorded on the WOWII page, which already
settles Conjecture 40 for `p = 1`. What is new is applying it to `G - T` rather
than to `G`, the `c_e` refinement, and the consequence for the *lifting* form —
which is strictly stronger than the conjecture on that class.

**Status: MATHEMATICALLY PROVED.** L1 checked exhaustively on all 7,049
bipartite graphs with `n <= 10` (0 violations, 169 tight). Coverage of L2
measured on all connected nonbipartite graphs with `3 <= n <= 8`: **11,170 /
11,859 = 94.2%** satisfy `p(G) <= 2 max_T c_e(G-T) - 1`, so the proved class is
not a curiosity.

**And the uncovered part is not the extremal part.** Cross-tabulating L2
coverage against the best-`T` slack over all connected nonbipartite graphs with
`3 <= n <= 8`:

| best-`T` slack | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| L2-covered | 217 | 666 | 2,773 | 3,978 | 3,255 | 281 |
| L2-uncovered | **0** | 43 | 249 | 199 | 198 | 0 |

**Every graph at which LIFT-A is tight lies inside the proved class**; every
uncovered graph has slack at least 1. So the proof obligation that remains has a
unit of slack to spend, which is a materially easier target than the general
statement. Smallest uncovered instance: `DC{` (n = 5, `o = 1`, `p = 2`,
`max_T c_e = 1`, slack 1).

### R7. The aborted n = 12 Lemma-B holdout (ATTACK.md target 5)

Resumed exactly per `proofs/FROZEN-BPLUS2.md` with the shipped frozen checker
`tools/b_hslide.py` (`OK` against `SHA256SUMS.txt`; frozen-source hash
`54e13cac…` published in FROZEN-BPLUS2.md). Holdout discipline observed more
strictly than the original run, whose recorded deviation (O-45) was reading the
failure counters mid-run: **I did not read `b-hslide-prog.txt` at any point**;
liveness was monitored only via `ps`. Outcome in "Jobs" below.

---

## Jobs still running at report time

Three sweeps were still running when this report was written. Their status is
recorded here rather than guessed; anything not stated as finished did not
finish.

* `fcore run` at n = 14 — **PENDING**
* `b_hslide.py 12` (the frozen n = 12 Lemma-B holdout) — **PENDING**

---

## Dead ends hit, and why

* **Turning Lemma CS into a Lemma-A contradiction.** The natural next move is to
  build an FVS of `G` of size `|S| - 1` as `(Q \ {q_j}) u U`. That needs
  `Q \ {q_j}` to be an FVS of `G[H u P]`, i.e. `tau(G[H u P]) <= |P| - 1` — the
  P-local bridge, refuted as a route by O-55/O-56. Lemma CS constrains `U` near
  `Q` but says nothing about how `P`'s *external* neighbours sit in the
  `H`-forest, which is exactly what the blocker needs. Checked on O-56: both
  choices of `j` leave `0` and `1` sharing the external neighbour `6`, so the
  quotient stays cyclic.
* **Assuming `P ∩ U = ∅`** (which would give the clean corollary CS(c)). It
  fails in ~44% of random abstract cyclic systems.
* **A two-matroid framing of F2.** The suppression reformulation makes F2
  "choose one pair `sigma(s) ⊆ N_H(s)` per `s`, all distinct, forming a linear
  forest on `H`". "Distinct, one per `s`" is a transversal matroid and "forest"
  is the graphic matroid, but the degree bound `deg <= c(h) <= 2` is **not** a
  matroid constraint — on the path `a-b-c-d` with `c(b) = c(c) = 1`, `{bc}` is
  maximal of size 1 while `{ab, cd}` has size 2. So Edmonds' matroid-intersection
  theorem does not apply and the reformulation does not by itself give F2.
  Recorded because the reformulation is clean, is what made the fast F2 oracle
  possible, and the obstruction to using it further is definite.
* **`Lemma A°` (disconnected) is not a wider universe than connected Lemma A.**
  Raising capacities only enlarges the feasible set, so
  `forced(all caps 2) ⊆ forced(caps for e)` for every `e in E(H)`; a disconnected
  instance decomposes into the component carrying `e` plus all-capacity-2
  components, each of which is implied by the connected fixed-edge result. So
  the "connected only" caveat on the existing `n <= 11` evidence is not a gap.
  (I chased this as a possible untested hole before checking; it is not one.)
* **SV at n = 11 is out of reach here.** SV needs `o(G-t)` and `p(G-t)` for
  every eligible `t`, i.e. roughly an order of magnitude more work per graph than
  the 18.1-hour n = 11 conjecture sweep. Not attempted; measured throughput at
  n = 10 was 2,780 graphs/s single-process including SV, which projects to about
  100 CPU-hours at n = 11.

---

## Recommended next angle

1. **Freeze LIFT-A-ALL and run an n = 10/11 sealed holdout.** It survived
   `n <= 9` exhaustively and is strictly stronger than the target statement;
   `work/lift.c` is already written, hashed and gold-tested. This is the
   cheapest well-posed prospective test available in the project right now, and
   target 4 is the only reduction gap that Lemmas A and B do not touch.
2. **Attack the residual 5.8%, using the slack.** L2 proves LIFT-A whenever
   `p(G) <= 2 c_e(G-T) - 1`. Everything hard about the general-to-bipartite step
   lives in the complement — connected nonbipartite `G` with large path-cover
   number whose minimum OCTs leave few edge-containing components. The
   cross-tabulation above says that complement contains **no tight instance**:
   every uncovered graph has slack `>= 1`. So the remaining obligation is
   `ell(G) >= 2 tau(G-T) + |T| + 2` on a family where the extremal cases have
   already been removed — a strictly easier-looking target than LIFT-A itself.
   Characterize that family first; it is small and `work/lift.c` can list it.
3. **Push `work/larealize.py` to `|S| = 4, 5`.** The factorisation makes the
   Lemma-A° counterexample space searchable for the first time. `|S| <= 3` is
   clean; the interesting regime (`P ∩ U != ∅`, longer forced cycles) starts at
   `|S| >= 4`. Either a counterexample appears — which would be the run's
   biggest possible outcome — or the localization histogram grows into real
   evidence about *where* the violation lives.
4. **Do not re-derive the localization from `P` or `B_s`.** 39% of the violating
   sets found by the search are inside neither. Any proposed localization should
   be run against `work/larealize.py`'s population before a line of prose is
   written about it.
5. **`work/fcore.c` and `work/f2.c` make the Lemma-A / F2 universe cheap** (n=13
   in 2 minutes, versus 7 minutes for n=11 in Python). n = 14 and n = 15 are
   within reach of one machine; the analogous C rewrite of `b_hslide.py` is the
   obvious way to finish the n = 12 Lemma-B holdout, but it must be validated
   against the frozen Python checker on the six n = 11 witnesses first.

---

## LESSONS FOR FUTURE ATTEMPTS

- [TOOLING] `work/fcore.c` (sha256 598bb06f…) decides forced-core acyclicity by the flow test of paper Thm 3.10 instead of intersecting all feasible selections; it agrees field-for-field with `tools/forced_core.py` at n=8,9,10,11 and runs n=13 in 115 s versus 414 s for n=11 in Python. Dual-engine Lemma A now exists.
- [VERIFIED] Lemma A (forced core acyclic) holds on all 994,607 instances at n=11 — the paper's footnote figure, now reproducible from the hashed `tools/forced_core.py`, and independently confirmed by `work/fcore.c`. The "not independently reproducible" caveat in paper §4.1 / PROOFS.md D / LEMMA-A-CHALLENGE.md can be lifted.
- [VERIFIED] Lemma A holds exhaustively at n=12 (10,970,519 instances) and n=13 (141,887,501 instances); max forced-core path length rises to 10. `infeasible (G,S,e) = 0` throughout, confirming Corollary 3.8 over 155M instances.
- [VERIFIED] F2-ALL — an acyclic feasible selection exists for EVERY minimum FVS and EVERY fixed edge — holds through n=13 (`work/f2.c`, sha256 e528a4ae…, positive control on O-56/63/64). F2, not Lemma A + Lemma B, is what Theorem 3.13 needs; it had never been scanned directly.
- [CONJECTURAL LEAD] LIFT-A-ALL: `ell(G) >= 2 tau(G-T) + |T| + 1` for EVERY minimum OCT `T`, not merely some. Exhaustive, 0 failures, all connected nonbipartite graphs n<=9. Stronger than ATTACK.md target 4; `work/lift.c` (sha256 c0cc2dd3…) is frozen and gold-tested — freeze it and run an n=10/11 holdout.
- [FALSIFIED] LIFT-P-ALL (`p(G) <= p(G-T)` for every minimum OCT `T`) fails from n=7: 3 failures at n=7, 16 at n=8, 150 at n=9; first witness in `work/lift-witness-n9.txt`. The existential quantifier over minimum OCTs in LIFT-P is load-bearing.
- [PROVED] L1: for bipartite `B`, `f(B) >= ceil(n_B/2) + c_e` where `c_e` counts edge-containing components. Hence L2: LIFT-A holds whenever some minimum OCT `T` has `p(G) <= 2 c_e(G-T) - 1`, which covers every traceable `G` and 94.2% of all connected nonbipartite graphs with n<=8. The hard part of the general-to-bipartite step lives in the other 5.8%.
- [PROVED] Lemma CS (carrier–cycle separation), `LEMMA-A-CARRIER.md` §1: with `U = ⋃_{s in P} B_s`, every `s in P \ U` has `deg_U(q) <= 1` at both forced ends, and consecutive `s_i, s_{i+1} in P \ U` force `deg_U(q_i) = 0`. Hall layer only; first use of the whole carrier family at once.
- [DEAD END] Lemma CS does not repair the P-local bridge. Building an FVS `(Q \ {q_j}) u U` of size `|S|-1` still requires `tau(G[H u P]) <= |P|-1`, refuted as a route by O-55/O-56; CS constrains `U` near `Q` and says nothing about how `P`'s external neighbours sit in the `H`-forest.
- [DEAD END] Do not assume `P ∩ U = ∅`. It fails in 4,931 of 11,097 random abstract systems with a cyclic forced core (~44%).
- [DEAD END] `Lemma A°` (disconnected) is not a wider universe: raising capacities only enlarges the feasible set, so `forced(all caps 2) ⊆ forced(caps for e)`, and a disconnected instance decomposes into the `e`-component plus all-capacity-2 components. The "connected instances only" caveat on the n<=11 evidence is not a gap.
- [DEAD END] F2 is not a two-matroid intersection. Suppressing the degree-2 `S`-vertices makes F2 "pick one pair per `s`, all distinct, forming a linear forest on `H`" — transversal matroid ∩ graphic matroid — but the capacity bound `deg <= 2` is not a matroid constraint (path `a-b-c-d`, `c(b)=c(c)=1`: `{bc}` maximal of size 1, `{ab,cd}` of size 2).
- [TOOLING] Hereditary FVS tightness for all `X ⊆ S` is EQUIVALENT to "`S` is a minimum FVS of `G`". This factorises the Lemma-A° counterexample search: cyclicity of the forced core depends only on the abstract system, minimum-FVS-ness only on the `H`-forest. `work/larealize.py` exploits it; 2,392,972 forest completions of cyclic-core systems gave 0 counterexamples, with a positive control hitting `tau = |S|` in 7.1% of acyclic-core completions.
- [CONJECTURAL LEAD] In 345 of 876 sampled Lemma-A near-misses (39%) the inclusion-minimal hereditarily violating `X` lies inside neither `P` nor any single `B_s`. Test any proposed localization against `work/larealize.py`'s population before writing prose about it.
- [TOOLING] `proofs/PROOFS.md` §D implies O-56 and O-63 are inside the hereditary-tightness class. Measured `tau(G[H u S])` vs `|S|`: 2 vs 4, 3 vs 5, 2 vs 3 — all three witnesses are outside it, and all three satisfy `S = T_F`. Documentation only; no claim depends on it.
