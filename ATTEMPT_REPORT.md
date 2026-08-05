# ATTEMPT REPORT — attempt/2026-08-05-claude-opus-5-4d7a

**Model / harness:** Claude Opus 5 (1M context) via Claude Code CLI, effort xhigh.
**Date:** 2026-08-05, starting 01:14 CDT.
**Repository state at branch point:** local `main-local` @ `85d1483`
(ATTACK.md v3 merged). Cloned from the local repository
`/Users/christineozols/conj40v2/conj40-verify` (the canonical local copy holding
`maint/2026-08-census`, `lessons/consolidated` and ATTACK.md v3; the copy at
`~/research/wowii-conjecture-40` is stale and lacks all three).
**Declared soft time budget (ATTACK.md v3 Step 5 stopping rule):** 4.5 hours from
01:14 CDT, wrap-up at 05:45 CDT; at wrap-up only jobs projected to finish within
15 minutes are carried to completion, everything else is marked
ABORTED-NO-VERDICT with resumable state on disk.
**Nothing was pushed.** All commits are local to this branch.

---

## Step 0 — freshness check

| check | result |
|---|---|
| open issues on `cozuya/wowii-conjecture-40` | none |
| pull requests | 2, both MERGED, both internal (`lessons/5047`, `lessons/consolidated`); nothing external |
| MathOverflow 513887 | **NOT PERFORMED** — `WebFetch` refuses `mathoverflow.net` in this harness ("unable to fetch") |
| WOWII open-problems page | **NOT PERFORMED** — `cms.uhd.edu` and the current `cms.dt.uh.edu` mirror are HTTP-only; the fetch tool upgrades to HTTPS and gets `ECONNREFUSED` |
| web / arXiv search | performed; nothing on Conjecture 40 specifically. Nearest 2026 items are unrelated Graffiti.pc work (proofs of Conjectures 141/142/143, `arXiv:2608.01396`) and a DeLaViña–Waller conjecture paper (`arXiv:2605.24855`). No indication Conjecture 40 or any of the open lemmas has been resolved by others |

**Status:** no evidence of external resolution. Two of the four mandated checks
could not be performed with the tools available and are recorded as NOT
PERFORMED, not as "nothing changed".

## Step 0.5 — prior attempts

Read `attempts/LESSONS.md` (all four entries: 5047, VERIFY-1, codex-a7c3,
fable-5-0eb8) and `ATTEMPT_REPORT.md` on `main-local`, plus the two binding
inputs for this run:

- `maint/2026-08-census` @ `c5ccf32` — the n=10 L5/L6-condition census (L5
  fails at n=10 with 7 witnesses; L6 clean at n<=10, so **CX11 is exactly minimal
  for L6**) and the excess<=0 enumeration at n=11,12 (2 and 16 graphs, first
  negative excess values). Read in full **before** choosing a target.
- The proved CX(m) obstruction: no sufficient LIFT-A threshold computable from
  per-component class sizes, isolate/edge-component counts and full-side
  forest-extension invariants can be universal.

Nothing on this branch proposes, freezes, or relies on any such threshold.

## Step 1 — comprehension gauntlet

**Completed.** `GAUNTLET.md` on this branch covers (i) the reduction chain of
Theorem 3.13 with the exact role of each of A and B, (ii) why the abstract
even-cycle system shows Hall feasibility alone cannot yield Lemma A, (iii) each
of O-56 / O-63 / O-64 and the precise localization it kills, (iv) the `T_F`
normalization with proof and licence. Every computational statement in it was
recomputed by `work/sd/wit_verify.py`, which shares no code with `tools/`.

Independent recomputation reproduced: all three witnesses' forced cycles; O-56
`tau(G[H u P]) = 2 = |P|` (P clean) with minimal violation `{2,3}` disjoint from
`P`; O-63 minimal violation inside `B_s` = the full `B_s = {u,a,b}` with all
three of incidence-degree 3; O-64 `tau(G[H u B_s]) = 1 = |B_s|` (`B_s` clean)
with the violation on `P = {s,t}`. Also confirmed independently that in all
three, `tau(G) < |S|` — they lie outside the hereditary-tightness class, which is
why they refute localizations and not Lemma A. Positive control: the abstract
even-cycle system at `m = 3, 4` is Hall-feasible, has a forced-core cycle, and
violates hereditary tightness at every singleton. Negative control: a
hereditarily tight instance has an acyclic forced core.

Frozen-oracle gold tests all reproduce the recorded values: every file in
`tools/` matches `tools/SHA256SUMS.txt`; `a1_verify.py 7` → `A1 = 143/143,
failures = 0`; `b_hslide.py 9` → 24,195 cycles, gap `{0: 24195}`;
`b_hslide.py 10` → 448,577 cycles, gap `{0: 448577}`.

The inherited `GAUNTLET.md` and `ATTEMPT_REPORT.md` from `main-local` are
preserved unmodified at `work/GAUNTLET-inherited-from-main.md` and
`work/ATTEMPT_REPORT-inherited-from-main.md`.

---

## Target chosen, and why

**Primary target: ATTACK.md v3 Step 3 target 2 / controller option (b) — Lemma B
via scheduled, ordered cycle-erasure.** Exactly one target was attacked.

Justification:

1. It is the only one of the three with **zero prior attempts**. Target (a) has
   had one partial harvest (Lemma CS) and a recorded dead end; target (c) sits
   directly under a proved obstruction (CX(m)) that forbids the natural
   statements, and its enabling census was only just completed.
2. It admits a **decisive oracle**. The frozen `b_hslide.py` already computes,
   per selected cycle, the exact predicate a scheduling statement needs; the
   whole n <= 11 universe is 25,598 graphs and runs in minutes. Target (a) is
   proof-shaped and its oracle contact is weak — the failure mode ATTACK.md
   warns about ("a prose proof with no oracle contact counts as NOTHING").
3. It is the only target where a **weakening of the published reduction** is
   available. The paper's Descent Lemma is stated with the hypothesis "*some*
   CES toggle exists", while Theorem 3.13 supplies the far stronger "*every*
   cycle of *every* selection is erasable" via `A and B`. That quantifier gap is
   free real estate and is precisely what "scheduling" means here.

---

## Claims, with status labels and evidence

### 1. SD-REDUCTION — [MATHEMATICALLY PROVED] (trivial; an unpackaging, not new mathematics)

Define **SD**: for every `(G, S, e)` in the model and every feasible selection
`J` with a selected cycle, *there exists* a selected cycle `C` of `J` and a CES
toggle for `C`. Then **SD implies F2, hence the bipartite case, using neither
Lemma A nor Lemma B.**

*Proof.* Initial feasibility for every `e` is unconditional. SD is verbatim the
hypothesis of the Descent Lemma. A CES toggle strictly lowers the nonnegative
integer `|cyc(J)|`, so iteration terminates at an acyclic feasible selection;
fixed-edge parity makes `J u {e}` acyclic; the degree count gives a spanning
linear forest with `2|S| + 1` edges. ∎

`A and B` imply SD, so SD is strictly weaker than the pair currently under
attack, and **Lemma A is not needed under SD** (an all-forced cycle is simply one
that SD does not have to pick). Preregistered in `PREREG-SD.md` §1. This is the
statement that makes everything below worth testing.

### 2. SD-SHORT — [FALSIFIED], minimal order 11

**Statement (frozen in `PREREG-SD.md` §2 before any run and before any n=11
witness was inspected):** for every feasible `J` with a selected cycle, *some*
selected cycle `C` of `J` satisfies `A1(C)` — some residual augmenting path of
length `d0(C)` is CES for `C`. This is the falsified A1 with its universal
quantifier over cycles replaced by an existential one, and by §1 it would close
the bipartite case.

**Result: 6 failures at n = 11**, 0 at n <= 10. Certificates in
`work/sd/sd-n11-AGGREGATE.json`; the three graphs are

```
J??FErWxDw?   S={0,2,3,4}    e=(5,10)    2 selections
J?B@eQo]Fo?   S={6,7,8,10}   e=(0,5)     2 selections
J?B@eOtq`i_   S={0,1,6,10}   e=(4,9)     2 selections
```

**Mechanism (the actual finding).** The recorded profile is
`(|cyc(J)|, #A1-good cycles) = (1, 0)` for all six: *every* A1-failing cycle sits
in a selection that has **exactly one** selected cycle. There was never a second
cycle to schedule. So SD-SHORT does not fail because scheduling is weak — it
fails because at the six witnesses there is nothing to schedule.

### 3. SD-COUNT-SHORT — [FALSIFIED], minimal order 11

Same universe, 6 failures, same witnesses: at those selections no minimum-length
toggle of any cycle strictly lowers `|cyc(J)|` either. (Consistent with the
recorded fact that each bad shortest path destroys exactly one old cycle and
creates exactly one new one.)

### 4. ONE-CYCLE — [FALSIFIED], minimal order **10**

**Statement:** every feasible selection has at most one selected cycle. Formulated
from the n <= 6..9 regression output (where it holds with histogram `{1: all}`)
and labelled IN SAMPLE at n <= 9 in `PREREG-SD.md` §6 **before** n = 10 and n = 11
were run.

**Result: false at n = 10** — 5,269 feasible selections with two selected cycles
(out of 443,308 cyclic selections); at n = 11, 130,811 out of 8,071,822. The
maximum ever observed is **2**; no selection with three selected cycles exists at
any order `n <= 11`.

This is the project's documented death pattern firing on my own statement one
order after the sample, which is the cheapest possible way for it to fire. It
also matters for claim 2: multi-cycle selections are *not* rare in general, so
cycle-choice scheduling is not structurally vacuous — it is vacuous exactly, and
only, where A1 fails at n <= 11.

**Do not over-read the cap of 2.** Three selected cycles need at least six
`S`-vertices, and feasibility forces `2|S| <= 2|H| - 2`, i.e. `|H| >= |S| + 1`;
so three selected cycles are impossible for pure counting reasons below
**n = 13**. The observed maximum of 2 through n = 12 is therefore an arithmetic
artefact, not evidence, and n = 13 is its first real test. By the same count two
cycles require `n >= 9`, so n = 9 *was* a genuine test that ONE-CYCLE passed and
minimal order 10 is a real fact.

### 5. SD-PLUS-2 — [COMPUTATIONALLY VERIFIED], universe: all connected bipartite `n <= 11`

The `exists`-cycle weakening of B-PLUS-2 (some cycle of `J` admits a CES residual
path of length `<= d0 + 2`): **0 failures** over 8,202,633 cycle components at
n = 11 and everything below. Weaker than B-PLUS-2, and by claim 1 it suffices for
the bipartite case on the universe where it holds. It inherits B-PLUS-2's
evidential status and adds no independent support.

### 6. Anchors reproduced — [COMPUTATIONALLY VERIFIED]

| anchor | published | this run |
|---|---|---|
| connected bipartite graphs, n = 9 / 10 / 11 / 12 | 730 / 4,032 / 25,598 / 212,780 | identical |
| cycle components n = 9 | 24,195 | 24,195 |
| cycle components n = 10 | 448,577 | 448,577 |
| cycle components n = 11 | 8,202,633 | **8,202,633** (8 shards, exact sum) |
| A1 failures (positive-gap cycles) at n = 11 | 6 | **6** |
| B-PLUS-2 / gap > 2 failures at n <= 11 | 0 | 0 |
| Lemma A violations (all-forced cycles) at n <= 11 | 0 | 0 |
| path-enumeration cap hits | 0 | 0 |

Reproducing `A1 failures = 6` under the `for all` aggregation, from the same code
path that produces the SD verdict under `there exists`, is the positive control
for the whole census.

### 7. SD-2STEP / SD-2STEP-DESCENT — [CONJECTURAL], in-sample at n = 11; n = 12 prospective

Formulated **after** seeing the six failures, so its n <= 11 support is
in-sample and carries no prospective weight (`PREREG-SD2.md` §0 says so
explicitly). Stated as: **A1 failures are never consecutive along minimising
steps.** Precisely — if a selected cycle `C` of `J` fails `A1`, then a
minimum-length toggle of `C` lands on a selection `J0` that itself admits a
CES minimum-length toggle; the descent form additionally requires
`|cyc(J0)| <= |cyc(J)|`, which makes the composite of two minimising steps a
genuine strict decrease and hence closes the bipartite case by claim 1.

**In-sample evidence (n = 11, exhaustive over the whole universe, but the only
non-trivial instances are the six discovery witnesses):** 6/6 A1-failing cycles
pass both forms; independently, over all **20** shortest bad paths — matching the
20 recorded in PROOFS.md §B3 — **20/20** are followed by a minimising CES step.

**Honest deflation — SD-2STEP-DESCENT is a WEAKENING of B-TERMINAL-SLIDE, not a
new mechanism.** [MATHEMATICALLY PROVED, conditional] *B-TERMINAL-SLIDE together
with hypotheses (H1)–(H3) of Proposition B1 implies SD-2STEP-DESCENT.* Proof: the
slide is `Q+ = Q0 + [u, t']`, and by pure algebra
`toggle(J, a, Q+) = J0 Δ {(t,u), (u,t')} = J0 - (t,u) + (u,t')` where
`J0 = toggle(J, a, Q0)`. Viewed from `J0` that is a residual augmentation
releasing `(t,u)` along a path of length **1**, and 1 is the minimum possible
residual path length, so it is a *minimising step of `J0`*; `(t,u)` lies on `J0`'s
new cycle `Z` by (H3). Under (H2) (only `C` destroyed, exactly one new cycle),
`cyc(J0) = (cyc(J) \ {C}) u {Z}`, so `|cyc(J0)| = |cyc(J)|` and `Q+` being CES for
`C` makes the second step CES for `Z` relative to `J0`. ∎

[COMPUTATIONALLY VERIFIED] At all **20** n = 11 bad shortest paths,
`d0(J0) = 1` and `|cyc(J0)| = |cyc(J)| = 1`, confirming the implication concretely.

So SD-2STEP-DESCENT's n <= 11 support is **not independent** of B-TERMINAL-SLIDE's.
Its value is entirely in being *weaker*: it can survive at n = 12 where
B-TERMINAL-SLIDE dies (the converse implication does not hold — SD-2STEP-DESCENT
permits the second step to release any incidence of any cycle of `J0`, not only
the slide edge, and imposes no (H4)/(H5) geometry). It states the whole descent
in minimum-length steps and replaces the (H1)–(H5) package with the single
slogan "A1 does not fail twice in a row".

### 8. n = 12 prospective holdout — COMPLETED EXHAUSTIVELY

Preregistered in `PREREG-SD2.md`, frozen with checker hash `9caa7805…` before
launch. **All 32 shards ran to completion**, i.e. all 212,780 connected bipartite
graphs on 12 vertices, every minimum FVS with `|S| >= 2`, every `e in E(H)`, every
feasible selection with a selected cycle. Wall time about 2 h 25 min on 8 cores.
This also **completes the n = 12 Lemma-B holdout that was aborted at ~49% on
2026-07-31 with no verdict** — though see the scope caveat below, which is why it
does not close out the frozen B-PLUS-2 statement in its universal form.

| quantity | n = 11 | **n = 12** |
|---|---|---|
| connected bipartite graphs | 25,598 | 212,780 |
| cycle components | 8,202,633 | **228,810,295** |
| cyclic feasible selections | 8,071,822 | 222,898,018 |
| selections with 2 selected cycles | 130,811 | 5,912,277 |
| **A1 failures** (positive-gap cycles) | 6 | **1,380** |
| **SD-SHORT failures** | 6 | **1,184** |
| SD-COUNT-SHORT failures | 6 | 1,184 |
| **SD-PLUS-2 failures** | 0 | **0** |
| **SD-2STEP failures / probed** | 0 / 6 | **0 / 1,380** |
| **SD-2STEP-DESCENT failures** | 0 | **0** |
| Lemma-A violations (all-forced cycles) | 0 | **0** |
| path-enumeration cap hits | 0 | 0 |

**SD-SHORT: FALSIFIED again at n = 12, but no longer for the n = 11 reason.**
The profile is now `(1,0): 1,184` and `(2,1): 196` — at n = 12, 196 of the 1,380
A1-failing cycles *do* sit in a two-cycle selection whose other cycle is A1-good,
so cycle-choice scheduling rescues 14.2% of them. It is not enough: 1,184
selections still have no A1-good cycle at all. So the n = 11 finding ("scheduling
by cycle is vacuous") was an artefact of the small sample; the correct statement
is that cycle-choice scheduling *helps but does not suffice*.

**SD-2STEP-DESCENT survived its first prospective test, at scale.** 1,380
independent non-trivial instances, 230x the six that suggested it, zero failures.
It is the only statement in this report that both (a) closes the bipartite case
by claim 1 and (b) has prospective, out-of-sample support.

**Uniformity worth recording:** every A1-failing cycle in the preserved records
(1,310 of the 1,380, the per-shard witness caps) is a 4-cycle with `d0 = 3` — the
same fingerprint as all six at n = 11. Not one A1 failure at any order has
`d0 != 3`.

**Independent re-verification (PREREG-SD2.md §4.2).** Eight evenly-spaced (every
146th) recorded n = 12 SD-SHORT failures were re-derived by
`work/sd/sd_reverify.py` — fresh code, no residual BFS/DAG/path machinery, working
in the symmetric-difference metric. All eight confirm: `H` a forest,
`tau(G) = |S| = 4` so `S` **is** a minimum FVS, hereditary FVS tightness for every
`X ⊆ S`, exactly one selected 4-cycle, `m_min = 4` hence `d0 = 3`, **zero** CES
minimisers, first CES at `m = 6` hence gap exactly 2, and **26/26** minimising
first steps followed by a minimising CES second step.

**Scope caveat — what this run does NOT settle.** The counter graded is
SD-PLUS-2, the `exists`-cycle form. The frozen **B-PLUS-2 in its universal
(`for all`-cycle) form is NOT graded at n = 12 by this run**: the checker stops
searching `<= d0 + 2` repairs for a selection once any one of its cycles is
covered, so up to 196 A1-failing cycles — exactly those co-occurring with an
A1-good cycle — had their `<= d0 + 2` repair left unchecked. Grading the universal
form needs a re-run of the same cost (~2.5 h), which did not fit this run's
budget. It is the cheapest high-value job for the next attempt.

---

## Dead ends hit, and why

- **[DEAD END] Scheduling by choice of cycle.** ATTACK.md v3 target 2 read
  literally — "construct an ORDER of cycle-erasures" — cannot repair A1. At every
  n <= 11 instance where A1 fails, the containing selection has exactly one
  selected cycle, so the order has length 1 and there is no choice to make. The
  remaining scheduling freedom is over **moves**, not cycles. This is not a
  statement that multi-cycle selections are rare (130,811 exist at n = 11); it is
  that they never coincide with an A1 failure through n = 11.
- **[DEAD END] ONE-CYCLE as a structural simplification.** The hope that the
  descent potential is two-valued (so that one CES toggle always suffices) is
  false from n = 10 on.
- **Not attempted, deliberately:** any new LIFT-A threshold. The CX(m)
  obstruction is binding and the excess-0 population at n = 11,12 exists precisely
  to test such proposals; formulating one was outside this run's single target.

## Tooling notes

- New checkers on this branch, all with committed sha256:
  `work/sd/sd_scan.py` (`227cf118…`), `work/sd/sd_scan2.py` (`9caa7805…`, = v1
  plus the SD-2STEP probe), `work/sd/onecycle_scan.py`,
  `work/sd/wit_verify.py` (`99cdfd46…`), `work/sd/sd_reverify.py`. Hashes in
  `work/sd/SD-SHA256.txt` and `work/sd/SD2-SHA256.txt`, frozen and committed
  before the runs they grade.
- `sd_scan*.py` import the frozen engine (`a1_verify`, `eval_L1_holdout`,
  `mine_n10`, `eval_frozen`, `inv_b`, `experiment_b`), so the per-cycle A1
  predicate is bit-identical to `b_hslide.py`'s; v2 reproduces v1 field-for-field
  at n = 9 and n = 11 as its gold test.
- **Negative controls fire.** With `--ces=always`, 0 failures everywhere; with
  `--ces=never` at n = 9, A1-ALL failures = 24,195 = every cycle component and
  SD-SHORT failures = 24,195 = every cyclic selection. Acknowledged gap: the
  `--ces=never` mutant does not exercise the SD-COUNT-SHORT path, which is
  measured by direct cycle counting rather than through the CES predicate.
- **Counter control.** Before trusting "every selection has one cycle", the
  frozen `comps`/`ncyc` were checked on hand-built selections and correctly
  returned 2, 1 and 0 cyclic components.
- **A bug the anchors caught.** The first lean ONE-CYCLE scanner used union-find
  *with path compression* inside a backtracking enumeration, where the only sound
  O(1) undo is restoring the single parent entry a union wrote. It over-reported
  by 17 cycles at n = 8 and 180 at n = 9; the published anchors (2,584 / 24,195)
  caught it immediately. Fixed by dropping compression. Recorded because it is a
  generic hazard for any backtracking enumerator in this project.
- **Independent re-verification of every failure** (`work/sd/sd_reverify.py`):
  fresh code, no residual-BFS/DAG/path machinery, working in the
  symmetric-difference metric `m(J,J') = |J Δ J'|` (tied to residual-path length
  by the proved residual-augmentation theorem: `m = d + 1`). It re-derives for all
  six witnesses: `H` a forest; `tau(G) = |S| = 4` so `S` **is** a minimum FVS;
  hereditary FVS tightness holds for every `X ⊆ S`; exactly one selected cycle, a
  4-cycle; `m_min = 4` hence `d0 = 3`; **0** CES minimisers; first CES at `m = 6`
  hence gap **2**. Every number matches the frozen engine.
- Environment: macOS, 8 cores, Python 3.9, `geng` from nauty on PATH. `ps` does
  not show background workers in this sandbox; progress files were used instead.

---

## Recommended next angle

1. **Prove SD-2STEP-DESCENT** ("A1 never fails twice in a row along minimising
   steps"). It survived n = 12 exhaustively on 1,380 out-of-sample instances, it
   closes the bipartite case on its own (claim 1, no Lemma A), and it is a proved
   weakening of B-TERMINAL-SLIDE — so it is strictly the easiest live target in
   the Lemma-B programme. The natural proof route is the B4 sub-programme
   (lex-optimal shortest paths, directed residual chords in `D_a`) applied not to
   `J` but to the *successor* `J0`: `J0`'s new cycle `Z` is one-added-edge and
   terminal, and empirically `d0(J0) = 1` every time, which is a far more
   constrained object than a general selected cycle. Proving "`d0(J0) = 1`
   whenever `C` fails A1" would essentially finish it.
1b. **Cheapest high-value computation:** re-grade n = 12 for B-PLUS-2 in its
   universal form (~2.5 h on 8 cores with `work/sd/sd_scan2.py` modified to search
   `<= d0 + 2` repairs per cycle rather than per selection). That would finally
   close out the holdout aborted on 2026-07-31.
2. **Re-target the "scheduling" idea from cycles to moves.** Any future statement
   of the scheduled-descent shape must quantify over an order of *toggles*; an
   order of *cycle-erasures* is provably empty where it is needed (n <= 11).
3. **Keep SD, not `A and B`, as the headline obligation.** Every statement in this
   report closes the bipartite case without Lemma A. If a future attempt proves
   any of SD-PLUS-2, SD-2STEP-DESCENT, or plain SD, Lemma A can be dropped from
   the reduction entirely — which would also retire the whole
   `P` / `B_s` / `T_F` localization programme that O-56, O-63 and O-64 have been
   killing one strategy at a time.
4. **Do not** propose a LIFT-A threshold from class sizes, isolate/edge-component
   counts, or full-side forest-extension invariants (CX(m) obstruction), and test
   any new threshold against `maint/2026-08-census`'s excess-0 population first.

---

## LESSONS FOR FUTURE ATTEMPTS

## 2026-08-05 — Claude Opus 5 (1M context) / Claude Code CLI — attempt/2026-08-05-claude-opus-5-4d7a
- [MATHEMATICALLY PROVED] Theorem 3.13's hypotheses can be weakened from `A and B` to the single statement **SD** ("every feasible selection with a selected cycle has SOME cycle admitting a CES toggle"). SD is verbatim the Descent Lemma's hypothesis, so SD implies F2 and the bipartite case with **no Lemma A at all**; `A and B` imply SD, so SD is strictly weaker. Anything that proves SD retires the entire `P`/`B_s`/`T_F` localization programme that O-56/O-63/O-64 have been killing one strategy at a time. (`PREREG-SD.md` §1.)
- [FALSIFIED] **SD-SHORT** (the `exists`-cycle weakening of A1: some cycle of `J` is erased by a residual path of length `d0`) is FALSE, minimal order **11**, 6 failures, on the same three graphs that killed A1: ``J??FErWxDw?`` `S={0,2,3,4}` `e=(5,10)`; ``J?B@eQo]Fo?`` `S={6,7,8,10}` `e=(0,5)`; ``J?B@eOtq`i_`` `S={0,1,6,10}` `e=(4,9)`, two selections each. Preregistered before any run and before any n=11 witness was inspected. Still false at n=12 with **1,184** failures. Certificates: `work/sd/sd-n11-AGGREGATE.json`, `sd-n12-AGGREGATE.json`.
- [FALSIFIED] **SD-COUNT-SHORT** (some minimum-length toggle strictly lowers the selected-cycle count) is FALSE at n=11 (6) and n=12 (1,184), same selections.
- [CONJECTURAL LEAD — the main result of this run] **SD-2STEP-DESCENT: "A1 failures are never consecutive along minimising steps."** If a selected cycle of `J` fails A1, some minimum-length toggle lands on a `J0` with `|cyc(J0)| <= |cyc(J)|` that itself admits a CES minimum-length toggle; the composite strictly lowers `|cyc(J)|`, so by SD this closes the bipartite case **without Lemma A**. **0 failures over the 1,380 A1-failing cycles in the EXHAUSTIVE n=12 universe** (228,810,295 cycle components) — its first prospective test, 230x its in-sample support. Frozen with checker hash in `PREREG-SD2.md` before launch.
- [MATHEMATICALLY PROVED] SD-2STEP-DESCENT is a strict **weakening** of B-TERMINAL-SLIDE, not a new mechanism: `toggle(J,a,Q0+[u,t']) = J0 - (t,u) + (u,t')`, which seen from `J0` is a residual augmentation of length **1** — the minimum possible — releasing an incidence of `J0`'s new cycle; with B1's (H1)+(H2), `|cyc(J0)| = |cyc(J)|`. So its evidence is not independent of B-TERMINAL-SLIDE's, and its entire value is being weaker. Confirmed concretely: `d0(J0) = 1` at all 20 n=11 bad shortest paths and at 26/26 in the independently re-verified n=12 sample.
- [CONJECTURAL LEAD] Every A1-failing cycle ever found — 6 at n=11, 1,310 preserved of 1,380 at n=12 — is a **4-cycle with `d0 = 3`**, and its successor always has `d0(J0) = 1`. Proving "`C` fails A1 `=>` `d0(J0) = 1`" would essentially finish SD-2STEP-DESCENT. No A1 failure at any order has `d0 != 3`.
- [DEAD END, corrected] Scheduling by **choice of cycle** cannot repair A1. At n<=11 it is outright vacuous (all 6 A1-failing cycles sit in selections with exactly ONE selected cycle, profile `(1,0)` 6/6). At n=12 it is no longer vacuous — 196 of 1,380 A1-failing cycles sit in a 2-cycle selection whose other cycle is A1-good — but it rescues only 14.2% and 1,184 selections still have no A1-good cycle. ATTACK.md v3 target 2 must therefore order **toggles**, not cycles. (The n=11-only reading, "cycle scheduling is vacuous", is a small-sample artefact; do not repeat it.)
- [FALSIFIED] **ONE-CYCLE** ("no feasible selection has two selected cycles") holds for every connected bipartite graph with n<=9 and is FALSE at **n=10** (5,269 two-cycle selections of 443,308 cyclic ones; 130,811 at n=11; 5,912,277 at n=12). Formulated in-sample at n<=9 and killed one order later. NOTE: the observed maximum of **2** is a counting artefact, not evidence — three selected cycles need `|S|>=6` and feasibility forces `|H|>=|S|+1`, so three are impossible below **n=13**, which is the first real test.
- [COMPUTATIONALLY VERIFIED] **SD-PLUS-2** (some cycle of `J` admits a CES residual path of length `<= d0+2`): **0 failures exhaustively through n=12**. Weaker than B-PLUS-2 and sufficient for the bipartite case by SD. CAVEAT: this run does **not** grade B-PLUS-2 in its universal (`for all`-cycle) form at n=12 — the checker stops searching once one cycle of a selection is covered, leaving up to 196 A1-failing cycles unchecked. Re-grading that is ~2.5 h on 8 cores and is the cheapest way to finally close the holdout aborted on 2026-07-31.
- [COMPUTATIONALLY VERIFIED] The aborted n=12 Lemma-B holdout is now **run to completion** in the SD form: all 212,780 connected bipartite graphs, every minimum FVS, every fixed edge, every feasible selection — **228,810,295 cycle components**, 0 Lemma-A violations (no all-forced cycle), 0 path-cap hits. n=11 anchors reproduced exactly first (8,202,633 cycle components; A1 failures = 6).
- [TOOLING] Union-find **with path compression inside a backtracking enumeration is wrong** — the only sound O(1) undo is restoring the single parent entry the union wrote, and compression mutates others. It over-counted cycles by 17 at n=8 and 180 at n=9 before the published anchors (2,584 / 24,195) caught it. Anchor every new enumerator against a published count before its first new run.
- [TOOLING] New checkers on this branch, hashes committed before the runs they grade: `work/sd/sd_scan.py` `227cf118…`, `work/sd/sd_scan2.py` `9caa7805…` (v1 + the SD-2STEP probe; reproduces v1 field-for-field at n=9 and n=11 as its gold test), `work/sd/wit_verify.py` `99cdfd46…` (witness recomputation sharing no code with `tools/`), `work/sd/sd_reverify.py` (independent symmetric-difference engine, `m(J,J') = d+1`), `work/sd/onecycle_scan.py`. Negative controls fire: `--ces=never` at n=9 gives A1 failures = 24,195 = every cycle component and SD-SHORT failures = 24,195 = every cyclic selection; `--ces=always` gives 0 everywhere. Gap: the `--ces=never` mutant does not exercise the SD-COUNT-SHORT path.
- [TOOLING] Cost is no longer a reason to leave a holdout aborted. Sharded by graph index in plain Python on 8 cores, the whole Lemma-B cycle universe takes ~5 min at n=11 and ~2 h 25 min at n=12 (228.8M cycle components). Growth is ~18x per order to n=11 and 27.9x from n=11 to n=12.
