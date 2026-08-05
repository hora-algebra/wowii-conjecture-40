# VERIFY-3 — adversarial verification report

Branch `verify/2026-08-05-verify3`, base `origin/main` (64eb3da). Run date
2026-08-05. Everything local; no push, no PR, no external disclosure. The
VERIFY-1 report is preserved unchanged as `VERIFY_REPORT-VERIFY1.md`.

**Targets.**

| priority | branch | head | subject |
|---|---|---|---|
| 1 (core-lemma certification) | `attempt/2026-08-05-claude-opus-5-0520` | `6def500` | `LEMMA-A-CLEAN-END.md`: NC (clean-end chordlessness), NCM/CE, A-I⁺ |
| 2 (standard pass) | `attempt/2026-08-05-codex-gpt-5-9d2b` | `99ec07e` | SAFE-EXISTS / universal B-PLUS-2; B-TERMINAL-SLIDE falsification at n=12 |

**Method.** Priority 1 under the contamination protocol: sealed independent
derivation written and committed (`52d4458`,
`verify3/SEALED-NC-DERIVATION.md`) before `LEMMA-A-CLEAN-END.md` was opened;
then step-by-step diff, grep-verification of attributed text, and machine
confirmation with fresh checkers. Priority 2 as a standard pass with fresh
checkers written from statements before reading any target checker code.
None of `work/0520/*.py`, `work/9d2b/*.py`, `work/sd/sd_scan*.py` (beyond
its two sharding lines), or `b_hslide.py` was read at any point.

---

## 0. Protocol deviations and contamination disclosure (Priority 1)

Reported first because the contamination rules were absolute and I breached
them twice, before the sealed derivation was written. Both events are logged
with exact boundaries in `verify3/SEALED-NC-DERIVATION.md` §0, committed
before the target was opened.

1. **ATTEMPT_REPORT overshoot.** Extracting the claimed statement, my
   4-line-too-wide window (lines 112–126) exposed the report's compressed
   proof sketch of NC(i)/(ii) ("Proof in two lines each: …").
2. **PREREG-NC.md read in full.** The task authorized "PREREG-NC.md's frozen
   statement"; the frozen file contains the full recorded proof below the
   statement, and I read the whole file. I resolve the statement/document
   ambiguity against myself and log it as a breach.
3. Unavoidably visible: the branch's `git log` subject line (topic-level) and
   the ATTEMPT_REPORT heading list (claim titles and grades only).

**Consequence.** The Priority-1 derivation is **verification-grade, not
blind**: the author's proof route was seen before my derivation was written.
What remains independent: every inference was re-derived and checked against
the certified prior stack with named dependencies and an adversarial gap-hunt
(sealed §6); all machine confirmation used fresh checkers written without
reading the target's code; the step-by-step diff of step (c) is unaffected.
The Priority-2 "blind re-derivation" of SAFE-2-EXISTS ⟹ F2 carries an
analogous caveat: the codex report and prereg state the claim and its short
proof in the same sections, so the derivation below is a checked
re-derivation, not a blind one.

---

## 1. Priority 1 — LEMMA-A-CLEAN-END.md (opus 0520)

### 1.1 Verdict

**CERTIFIED.**

Scope of the certification: the NC statement (both the ATTEMPT_REPORT
blockquote and the PREREG-NC.md §2 frozen statement, which agree), its
consequences (`deg_U(q) = |cyc(q) ∩ U|`; `N_S(q) = cyc(q)`, `deg_S(q) = 2`
on `T_F`-normalized instances), Corollary CE (= prereg NCM), and A-I⁺.
The claims are correctly graded by their author: Hall-layer only, no claim
of closing Lemma A, CAP2-BS left CONJECTURAL / scan ABORTED-NO-VERDICT.

### 1.2 Sealed derivation vs the document (step-by-step diff)

My sealed derivation (committed `52d4458`, before opening the target)
derives NC(i), NC(ii), the consequences, and NCM from exactly the certified
inputs the document also uses; the diff is step-for-step:

| document step | sealed counterpart | agreement |
|---|---|---|
| Notation ¶: "Each `q ∈ Q` carries two forced incidences, so `c(q) = 2`" | P1 (with the feasibility dependency made explicit) | same |
| (i) index argument "`q_i` is one of them only when `k ∈ {i, i+1}`" | P2 | same |
| (i) punctured-tightness "other neighbour" clause, `deg_{A_{s_k}}(q) ≥ 3` | §4(i) via [PT], with the two-forced-edges premise P0 made explicit | same |
| (i) "deleting the single vertex `s_k` lowers the degree at `q` by exactly one" | §4(i) exact-drop step | same |
| (ii) `N_S(q) ∩ U = {w}`, both `cyc(q)` vertices in `P \ U`, CS(b) | §4(ii) | same |
| CE via CP (`P\U ≠ ∅`) + CS(a) | §5 NCM | same |

No gap survived the adversarial hunt (sealed §6): the two implicit premises
the document leans on — no third forced incidence at a cycle vertex, and
`c(q) = 2` requiring feasibility — are both discharged by demand-2 +
feasibility (my P0/P1) and are present in the certified stack (max-degree-2
forced core, LEMMA-A-CARRIER.md §1). Every label the document attributes to
the prior stack was grep-verified verbatim: the O-60 ledger quote
(`ledgers/RESULT_RECORD.md:331`, ASCII/Unicode differences only), GAUNTLET
§(ii), ATTACK.md Step 3's ADJ boundary, the `LEMMA-A-CARRIER.md` §1.3 tables
and §2.3 `larealize` anchor (438 cyclic / 732 completions), and the
PREREG-NC.md §0 hashes.

### 1.3 A-I⁺ (new content, not in the sealed claim)

Verified after unsealing. The deletion argument is sound: with
`D = Q \ {q_0}` (`|D| = m−1`), P lies in one bipartition class, so surviving
`P`-degrees in `G[H ∪ P] − D` are `|Ext(s)|` plus adjacency to `q_0`;
NC(i) at the clean `q_0` removes the chord option for `s ∉ cyc(q_0)`;
hypotheses (1)/(2) then bound every degree by 1, `H − D` is a forest, so
`τ(G[H ∪ P]) ≤ m−1 < m`, contradicting hereditary tightness (C2). The
essential-use claim for NC is correct: without NC(i) a chord `s ∼ q_0` gives
degree 2 and the argument fails. Machine confirmation below (counting step
checked raw on every hypothesis-satisfying cyclic system; 0 failures).

### 1.4 Machine confirmation (fresh checkers; all code in `verify3/`)

Engines written for this run without reading any target code:
`nc_verify3.py` (abstract layer: NC/NCM/CPR/PT/A-I⁺ + negative controls),
`nc_sweep.py` (extended universe), `graph_fcore_verify3.py` (graph layer,
flow-based forcedness cross-checked against enumeration-intersection),
`localization_check.py` (§5/§6 witness claims).

Gold tests and controls:

* O-56 / O-63 / O-64 / ADJ-1: feasible-selection counts 1 / 6 / 1 / 1
  (matching VERIFY-1 and the JSONs; O-56's corrected 8-edge forced core
  reproduced); all four carry cyclic forced cores and pass NC/NCM/CPR/PT;
  ADJ-1 fires all three negative controls and satisfies the A-I⁺ hypothesis
  at `q_0 = 1` with degrees `s0 ↦ 1, s1 ↦ 0, s2 ↦ 1` — exactly as the
  document illustrates.
* Mutation controls (harness liveness): NC(i) without the clean guard fires
  on ADJ-1 at `q = 0`; an injected aux chord `3∼4` on O-56 fires NC(ii); an
  injected `Ext(s0) = {x}` on ADJ-1 fires the A-I⁺ counting check. All fired.
* Graph-layer controls: the O-64 and ADJ-1 graph realizations (S not a
  minimum FVS) yield cyclic forced cores; an acyclic C4 control stays clean.

Certified-anchor universes (exact reproduction):

```
exhaustive(|S|<=3,|H|<=5): 115,774 systems, 798 cyclic, 0 failures,
                           controls NC-ALL 18 / CHORD-ALL 18 / PDIS 18,
                           A-I+ hypothesis satisfied by 528  (doc: 528/798)
random 20000 seed 1:       656 cyclic, 0 failures, controls 332/332/332
random 400000 seed 777:    13,245 cyclic, 0 failures, controls 6727/6695/6727
descriptive claim:         1,602 clean + 18 dirty q over the 798;
                           all 18 chords at dirty q, none at clean  (doc: same)
```

Extended abstract universe (new to this run; carrier.py conventions, every
`(|S|, |H|)` with `|S| ≥ 2`, `|H| ≥ 3`, `|S|+|H| ≤ 10`; the two heaviest
blocks (4,6) and (5,5) deduped by S-relabeling, which every predicate is
invariant under):

```
labeled blocks:  21,584,075 systems, 169,047 cyclic forced cores, 0 failures
(4,6) deduped:    2,948,880 systems,  52,055 cyclic,               0 failures
(5,5) deduped:    1,147,190 systems,  10,892 cyclic,               0 failures
total:           ~25.7M systems, ~232k cyclic; NC, NCM/CE, CP-regression,
                 punctured-tightness regression, A-I+ counting step: 0 failures;
                 all three negative controls fire in every population that
                 contains dirty q
```

Graph layer, full census n ≤ 10 (`geng -bc`, every minimum FVS, every
H-edge; flow-forcedness engine, cross-checked instance-by-instance against
an independent enumeration engine at n ≤ 8 and every 500th instance above):

```
n<=7: anchors match; n=8: 2,186 tau>=2 instances (+1,584 tau<2 = VERIFY-1's
literal 3,770); n=9: 13,003; n=10: 4,032 graphs, 116,216 instances.
0 infeasible (C5b regression), 0 cyclic forced cores anywhere -- in
particular no A-I+-shaped forced cycle exists on any hereditarily tight
instance with n <= 10.
```

### 1.5 The TOOLING discrepancy (document §4) — CONFIRMED

Three engines agree against the published figures. Frozen `work/carrier.py`
at its preregistered hash `d11b0bca…` rerun now: `random 20000 1` gives 656
cyclic / PDIS 332 / DEG2 157, and my independent engine gives 656 / 332 on
the identical population — against the published `LEMMA-A-CARRIER.md` §1.3
row of 547 / 251 / 142. Likewise 13,245 / 6,727 vs the published 11,097 /
4,931 at seed 777. The exhaustive row (115,774 / 798 / 18) reproduces
exactly in all engines. The document's diagnosis (stale documentation
figures, not engine drift; anchors and verdicts unaffected) is correct, and
its corrected overlap rates (50.6% / 50.8%) match mine.

### 1.6 Localization refutations and CAP2-BS gold rows (document §5–§6) — CONFIRMED

Machine-checked on the realized witness graphs (`localization_check.py`):
O-63's maximal carrier `A_t = {t}` has `τ(G[H ∪ A_t]) = 1` (no violation
there); O-64's two maximal carriers `A_t = {t}` (τ=1) and `A_s = {s,u}`
(τ=2) both carry no violation — "the violation lives in some maximal
carrier" is refuted as stated. CAP2-BS gold rows reproduce exactly:
O-56 `B_s={2,3}`, guard yes, τ=1 (tight); O-63 `B_s={u,a,b}`, guard yes,
τ=2 (tight); ADJ-1 `B_s2={s0,s1}`, guard yes, τ=0; O-64 `B_s={u}`, guard
no (capacity-1 neighbour), τ=1 — the unguarded form fails exactly there.
The author's own grading of the CAP2-BS scan as ABORTED-NO-VERDICT (inert
in-universe negative control) is accurate and is the correct reading of the
evidence.

### 1.7 Prospective-verification integrity

The freeze commit `2510e2b` precedes the results commit `6def500`; the four
`work/0520` artifacts hash to exactly the values recorded in the frozen
PREREG-NC.md (`ac1836d9… / 64ebfa3f… / b21f5b8d… / 2a0d62e0…`); the vendored
ADJ witness is byte-identical to b17e's original at the cited commit
`9cd62bb`. The preregistered decision rules were followed; the negative
controls fired in every population as required.

---

## 2. Priority 2 — codex SAFE-EXISTS branch (9d2b)

Engines: `lemmab_verify3.py` (residual paths, CES, terminal slides,
successor grading — written from `proofs/FROZEN-BPLUS2.md`, PROOFS.md C4/E,
and `PREREG-SAFE-EXISTS.md` statements), `witness_check.py`,
`tail_scan.py`. Controls first, then results.

### 2.1 Controls

* Full-universe n=9 anchor: my engine over all 730 connected bipartite
  graphs, every minimum FVS, every H-edge, every feasible selection:
  24,195 selected cycle components, 0 A1 failures — exactly the codex gold
  figures.
* The six 4d7a n=11 A1-BAD-SELECTION witnesses (three graphs × two
  selections): my engine grades every one A1-bad with `d0 = 3`, first
  generic CES at 5, repairing terminal slides present (all to the freed
  `h`), successors CES-repairable and non-increasing — B-TERMINAL-SLIDE
  and B-H-SLIDE hold at n=11, exactly as frozen.
* Mutation: removing the created-cycle half of the CES comparison flips all
  12 bad minimizing steps of the n=12 witness to "CES" — the check is
  load-bearing.
* In-witness discrimination: the same instance carries one A1-good cycle
  (CES at `d0 = 3` found) and one A1-bad cycle (no CES at 3) — positive and
  negative behaviour in a single record.

### 2.2 B-TERMINAL-SLIDE n=12 witness — CONFIRMED

`K??FFbw}Fw^_`, `S = {6,7,8,9,10}`, `e = (4,11)`, J as recorded; target
cycle `{0,1,6,7}`. Independently: n=12 connected bipartite; `τ = 5` and S
is a minimum FVS; J feasible (one of 249 feasible selections); exactly two
selected cycles; the other cycle `{2,3,8,9}` is A1-good. Target: `d0 = 3`;
**12 minimizing steps, none CES; 0 valid terminal slides (0 h-slides);
first generic CES at length 5** (B-PLUS-2 gap 2 holds here). One detail of
the report is off by omission only: it cites the selection as recorded in
`independent-witness.json`, but that file holds only the summary; the full
`(g6, S, e, J, C)` record is in `safe-witness-replay.json`.

### 2.3 Successor-one falsifications — CONFIRMED

On the same witness all 12 bad minimizing successors have exactly one
selected cycle, successor `d0 = 3` (never 1), and every successor admits a
CES minimizing step. So SUCCESSOR-ONE-ALL and SUCCESSOR-ONE-DESCENT are
false at n=12 while SD-2STEP-DESCENT survives — the report's separation is
exactly right, including its refusal to promote the mismatch to a cause.

### 2.4 SAFE-2-EXISTS ⟹ F2 re-derivation — CONFIRMED (no gap)

Re-derived and checked (blindness caveat in §0): if J is acyclic, C3 makes
`J ∪ {e}` acyclic, giving the 2|S|+1-edge spanning linear forest (B3), i.e.
F2. If J is cyclic, alternative 1 (a CES minimizing step) strictly lowers
the selected-cycle count c (destroys the designated cycle, creates none);
alternative 2 first moves to J0 with `c(J0) ≤ c(J)` (feasibility preserved
— every toggle along a residual augmenting path lands on a feasible
selection, C4), then a CES minimizing step lowers c strictly. Each ≤2-step
block strictly decreases a nonnegative integer, so iteration reaches an
acyclic feasible selection; C5b supplies the initial selection. The claim's
conditional grading (descent-sufficient; the universal statement stays
CONJECTURAL) is correct.

### 2.5 The 44 cap-omitted hard-state records — GRADED (this run's new work)

The 4d7a shard files cap retained witnesses at 50 per shard; six shards
overflowed, omitting 44 `(1,0)` records (shards 4/11/13/14/16/25:
10/8/4/4/12/6) and 26 `(2,1)` records (shards 11/14: 14/12). My per-shard
reconciliation of the cap arithmetic matches both codex replay manifests
exactly. I rescanned each affected shard from the graph containing its 50th
retained witness (inclusive) through the shard end with the fresh engine —
every minimum FVS, every H-edge, every cyclic feasible selection — and
reconciled found = retained-overlap + missing per shard.

Results (`verify3/tail-shard-*.json`, reconciliation by `tail_scan.py
reconcile`):

| shard | tail graphs | found | overlap w/ retained | new | new (1,0) | new (2,1) |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 149 | 16 | 6 | 10 | 10 | 0 |
| 11 | 779 | 34 | 12 | 22 | 8 | 14 |
| 13 | 76 | 6 | 2 | 4 | 4 | 0 |
| 14 | 611 | 48 | 32 | 16 | 4 | 12 |
| 16 | 180 | 14 | 2 | 12 | 12 | 0 |
| 25 | 102 | 10 | 4 | 6 | 6 | 0 |

Every per-shard `new` count equals the missing count exactly; the shard-11
and shard-14 overlaps (12 and 32) equal the codex report's figures; the 26
and 44 tail `(2,1)` records of shards 11/14 equal its tail-scan counts. No
record of any other profile appeared.

**Grades of the 44 cap-omitted `(1,0)` records (and the 42 overlapping
retained records re-checked en passant): zero failures everywhere.** Every
`(1,0)` record has `d0 = 3`, a repairing terminal slide, all successors with
a length-one CES minimizing step, HARD-SUCCESSOR-ONE satisfied, and
SD-2STEP satisfied. Every `(2,1)` tail record has `d0 = 3`, no terminal
slide, and SD-2STEP satisfied (the A1-good alternative present). A direct
B-PLUS-2 computation on all 128 tail records gives gap exactly 2
(`dCES = 5 = d0 + 2`) on every one, zero violations.

**Consequence.** HARD-SUCCESSOR-ONE now has zero failures on the complete
n=12 hard-state profile — all 1,184 `(1,0)` states (1,140 codex-retained +
44 graded here) — closing the finite cleanup the codex report recommended.
It remains post-hoc finite evidence (CONJECTURAL), exactly as preregistered
in `PREREG-HARD-SUCCESSOR.md`; nothing here promotes it.

### 2.6 Sample replay of the (2,1)-gap certificates — CONFIRMED

All 40 saved `(2,1)` failure records in `safe-witness-replay.json` were
replayed with the fresh engine: 40/40 full field-level agreement — state
valid and feasible, `ncyc = 2` with one A1-good cycle, target `d0 = 3`,
zero terminal slides, first generic CES at 5 (B-PLUS-2 gap 2), bad-step
counts equal, successor profiles (including the all-successors-distance-one
subset) equal. Zero disagreements.

### 2.7 Priority-2 grading summary

| claim | codex grade | VERIFY-3 result |
|---|---|---|
| B-TERMINAL-SLIDE falsified at n=12 (witness) | FALSIFIED | **CONFIRMED** (independent full re-grade of the witness) |
| SUCCESSOR-ONE-ALL / -DESCENT falsified at n=12 | FALSIFIED | **CONFIRMED** (same witness, all 12 successors at distance 3) |
| SAFE-2-EXISTS ⟹ F2 | MATHEMATICALLY PROVED (conditional) | **CONFIRMED**, no gap |
| (2,1) gap records: d0=3, first CES 5, slides fail, SD-2STEP holds | replay 170/170 | **CONFIRMED on the 40 retained failure records** (40/40 agreement) |
| HARD-SUCCESSOR-ONE on retained n=12 (1,0) records | 0 failures on 1,140; 44 ungraded | **44 omitted records graded here: 0 failures — complete at 1,184/1,184** (still CONJECTURAL: post-hoc, finite) |
| universal B-PLUS-2 composite n=12 census | COMPUTATIONALLY VERIFIED | **Partially re-verified**: witness + 40-record sample + tails re-graded here; the 4d7a full-census component was not re-run (out of scope, as in the codex run itself) |

---

## 3. Engine provenance (this run)

All fresh code lives in `verify3/` on this branch. sha256:

```
4b1128858c5159002b9460534d77a6105c8d3c6ac25d228840fe0e256bf3522f  graph_fcore_verify3.py
24f0779d8daa0baf2fb8c6d0d3c917375e70fe652ac097d387ab9c89430e4e29  lemmab_verify3.py
97844a7bac958d6b16456f0073705d22ced4471c9c39a1ef27e230a0899759c9  localization_check.py
f2929e499a2897abf4c31a7dca488be97c29c7979cc69300b4115cf483164d1e  n9_anchor.py
b3f8f3698798ab2cc75c84d05f62a9e024c99515ea4bce727c139f221b6e7fd6  nc_sweep.py
8e6875fc263e82d6ffb4e531f4bcc09f474c0331890125eb1970dba174eeb27c  nc_verify3.py
52d1223a01c0f50eb118de1d9b1da93895a46abb074fc9a699d7ecb7becc3a8d  tail_scan.py
b1c4091161b6f9c23688e7acd4a3bb3e753e15250b3af0d7fd6eca4a5dad43cd  witness_check.py
ea9f38c8f0ac053294a4c4c24491444acd33e92e9b3753162d603dcdeb43f188  SEALED-NC-DERIVATION.md
```

Caveat on the sealed hash: `SEALED-NC-DERIVATION.md` was committed sealed at
`52d4458`; `nc_sweep.py` and `tail_scan.py` were edited after their first
commit for restartability and speed (per-pair slicing, early-exit
classification, slice reconcile); the predicate code is unchanged and the
per-shard results were re-derived consistently across engine variants (full
scans and slices agree record-for-record where they overlap).

Written from statements only; the target branches' checker code was never
opened. Universe conventions were taken from certified prior tooling
(`work/carrier.py` generators; `sd_scan2.py`'s two sharding lines
`geng -bc -q 12`, `gi % 32 == shard`).

## 4. What this run does NOT establish

* No promotion of any finite census to a proof. Lemma A, Lemma B,
  SAFE-2-EXISTS, and Conjecture 40 remain OPEN.
* The 4d7a n=12 full census (228,810,295 cycle components) was not re-run;
  its role here is the same fixed-source role the codex run gave it.
* The Priority-1 certification is of correctness relative to the certified
  prior stack (paper §4, PROOFS.md, Lemma CS, CP, T_F); those inputs were
  re-read and their proofs spot-checked but not themselves re-derived from
  scratch in this run (CP and CS carry VERIFY-2's independent
  certification).
