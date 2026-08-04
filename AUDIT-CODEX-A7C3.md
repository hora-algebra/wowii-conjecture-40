# Independent audit of attempt/2026-08-04-codex-a7c3 (commit 9349b7c)

Auditor: attempt/2026-08-04-claude-fable-5-0eb8 (Claude Fable 5), 2026-08-04.
Audited artifact: branch `attempt/2026-08-04-codex-a7c3`, whose sole commit
("Add LIFT-A residual attack and checkers") sits directly on v1.1
(`0617d7a`, matching the report's stated base). The audit ran against the
branch's pre-sanitization commit `5c4a4ec00f5b72f6e887a61ea8cc43adf326e7a9`;
the branch was subsequently sanitized in place to
`9349b7cb809d0d21e5355808ae32b0081e8a13fa`, amending only neutralized
path/narration lines in `ATTEMPT_REPORT.md` and `LIFT-A-RESIDUAL.md` — every
audited checker, hash record, count, and mathematical statement is
bit-identical between the two commits. Files audited: `ATTEMPT_REPORT.md`,
`LIFT-A-RESIDUAL.md`, `work/lift_residual.py`, `work/lift_residual_l4.py`,
`work/lift_residual_l5.py`, and the three SHA-256 records.

Method: (1) hash verification; (2) my own re-derivation of every proof,
recorded below, done before reading the checker sources; (3) an independent
engine (`work/fable-0eb8/audit_l3l5.py`, written from the definitions in the
paper and LIFT-A-RESIDUAL.md, sharing no code with the codex checkers or with
`tools/`), reproducing every reported count; (4) re-execution of the codex
checkers at their frozen hashes.

## 1. Hash and provenance verification

| item | verdict |
|---|---|
| `lift_residual.py` = `78b7a981…` per `work/LIFT-RESIDUAL-SHA256.txt` | CONFIRMED |
| `lift_residual_l4.py` = `b9c6fba9…` per `work/LIFT-RESIDUAL-L4-SHA256.txt` | CONFIRMED |
| `lift_residual_l5.py` = `d2583ebd…` per `work/LIFT-RESIDUAL-L5-SHA256.txt` | CONFIRMED |
| branch base = `0617d7a` (tag v1.1) as reported | CONFIRMED |
| pre-repair hash `6e555454…` (the `int.bit_count` version) | NOT VERIFIABLE — that source is not in the tree; only the narrative records it. Minor: the repair story is coherent and the repaired source contains `bin(...).count("1")` where a bit-count is needed. |

## 2. Mathematical audit of the five proofs

My own re-derivations; each verdict is about the codex proof as written in
`LIFT-A-RESIDUAL.md`.

**L3-Forest** (`tau(B) <= M(B) - c_e(B)` for every finite bipartite `B`).
Re-derived: in an edge-containing component `C` with classes of sizes
`a_C >= b_C`, the larger class plus one vertex `v` of the smaller class
induces: larger class independent, edges only `v`-to-`N(v)` — a star plus
isolated vertices, a forest on `a_C + 1` vertices. Isolated components add
themselves. Total induced forest order `|B| - M + c_e`; complement gives the
bound. The identity `|B| - 2M = Delta` is class-size arithmetic per
component. No connectedness used; `M >= c_e` keeps the bound sane.
**Verdict: MATHEMATICALLY PROVED — CONFIRMED.**

**L3** (if some minimum OCT `T` has `p(G) <= 2c_e + Delta - 1` then
`ell(G) >= 2tau(B) + |T| + 1` with that `T`). Re-derived:
`2tau + o + 1 <= 2(M - c_e) + o + 1 = (n_B - Delta) - 2c_e + o + 1
= n - Delta - 2c_e + 1 <= n - p(G) = ell(G)`, the last step being exactly
condition (3). **Verdict: MATHEMATICALLY PROVED — CONFIRMED.** The
containment of L2 (`Delta >= 0`) is immediate.

**L5-Forest** (`tau(B) <= M(B) - c_e(B) - r(B)`). Re-derived: in a
component with a certified pair `u,v` (same smaller-or-tied class, codegree
<= 1), take the full opposite class plus `u,v`. Any cycle in this induced
bipartite graph must alternate sides; the small side has exactly two
vertices, and a simple cycle visits each at most once, so any cycle is a
4-cycle `u-x-v-y-u` through two distinct common neighbours `x,y` of the
pair — impossible with codegree <= 1. Forest order `max_C + 2`; the +1
bonus per qualifying component is additive because components are disjoint.
**Verdict: MATHEMATICALLY PROVED — CONFIRMED.** (Note the definition
subtlety, faithfully implemented in both engines: on a class-size tie,
either class may act as "smaller".)

**L5** (condition `p(G) <= 2c_e + Delta + 2r - 1` suffices). Same algebra
as L3 with `M - c_e - r`. **Verdict: MATHEMATICALLY PROVED — CONFIRMED.**

**L4** (`o <= 2`, some minimum OCT leaves a forest => `ell >= o + 1`, which
is LIFT-A there since `tau(G-T) = 0`). Re-derived: `o = 1`: an odd cycle
has length >= 3; dropping one edge leaves a path with >= 2 edges; pad with
trivial paths. `o = 2`: `b(G) = n - 2` and the maximum induced bipartite
subgraph has an edge (paper Lemma 5.2, `b >= alpha + 1`, needing `G`
connected nontrivial), so `n >= 4`. A shortest odd cycle of length >= 5
contains a 3-edge path; a triangle plus connectivity and a fourth vertex
gives `w-x-y-z` (entering edge + two triangle edges), 3 edges either way.
**Verdict: MATHEMATICALLY PROVED — CONFIRMED.**

No gap found in any of the five proofs. None is Lean-formalized.

## 3. Computational reproduction

### 3a. Independent engine (mine)

`work/fable-0eb8/audit_l3l5.py`: graph6 parser, union-find forest test,
subset-scan `tau`, Hamiltonian-path-DP + submask-DP path cover, BFS
2-coloring, exhaustive minimum-OCT enumeration — all written fresh. Output
(runtime 14.9 s):

- Bipartite `2<=n<=8`: 451 graphs, per-order counts `2,3,7,13,35,88,303`.
  L3-Forest failures 0, tight 182, false one-unit control fires 182.
  L5-Forest failures 0, tight 356, false control fires 356. **Matches.**
- Connected `3<=n<=8`: per-order counts `2,6,21,112,853,11117`;
  nonbipartite 11,859. Exact LIFT-A failures 0. Coverage L2 = 11,170,
  L3 = 11,852 (682 beyond L2), L5 = 11,859 (7 beyond L3, residual 0).
  L3 residual = exactly `F?o}W FCQV_ G?BEH{ G?`CVo G?o}][ GCQQVo GCQSng`.
  Same-`T` implication failures: L3 = 0, L5 = 0. L4 applies to 4,606,
  0 failures, covers all 7 residuals, false `ell >= o+2` control fails on
  exactly 2 graphs. Descriptive universal-OCT L3 count 11,783. **All match.**
- `DC{` strictness control: `p = 2`, `o = 1`, three minimum OCTs; fails L2,
  passes L3, exact LIFT-A holds. **Matches** (including the codex claim
  that `DC{` is not traceable — my DP returns `p = 2` — and my hand check
  of the leaves-force-`1-4-2` argument).

### 3b. Re-execution of the codex checkers

At the verified hashes, on this machine (`geng` on PATH):

- `lift_residual.py 8`: `L3-FOREST-BOUND: 451 / 0 / 182; fires=182`,
  `LIFT-COVERAGE {connected: 12111, nonbipartite: 11859, lift_fail: 0,
  l2: 11170, l3: 11852, new: 682, residual: 7, l3_implies_lift_fail: 0,
  l3_all: 11783}`, `STRICT-CONTROL DC{ PASS`, residual profiles
  `{(1,0,1): 5, (1,1,1): 2}` — identical to the recorded outputs.
- `lift_residual_l4.py`: `l4: 4606, l4_on_post_l3: 7, combined: 11859,
  l4_lift_fail: 0, false_plus_one_control: 2` — identical.
- `lift_residual_l5.py`: `L5-FOREST {451, 0, 356, 356}`, `L5-COVERAGE
  {l5: 11859, new_over_l3: 7, post_l5: 0, l5_lift_fail: 0}`,
  `POST-L5-EXAMPLES []` — identical.

## 4. Scope and labeling audit

- The report's distinction — L3 run frozen prospectively; L4 and L5
  formulated after seeing the seven residuals and their `n<=8` runs labeled
  regression, not holdout — is accurate and properly carried through both
  documents. **CONFIRMED as honest labeling.**
- The report's closing caveat — zero residual at `n<=8` is NOT evidence
  that L5's condition (6) is universal — is correct and remains the open
  question. **The universality of condition (6) is OPEN; nothing in the
  codex artifact claims otherwise.**
- The codex Step-0 findings (one open PR #1, MO 513887 with 0 answers,
  WOWII status letter O) are consistent with what I could verify today
  (0 issues, PR #1 open; MO and the WOWII page were unreachable from my
  harness — recorded in my own report).

## 5. Overall verdicts on the audited advance

| claim | status after audit |
|---|---|
| L3-Forest, L3, L4, L5-Forest, L5 | MATHEMATICALLY PROVED — independently re-derived, no gaps; not Lean-formalized |
| `n<=8` regression numbers (451/0/182; 356; 11,859; 11,170/11,852/11,859; 682/7/0; 4,606; controls 182/356/2) | COMPUTATIONALLY VERIFIED (universe: all bipartite graphs `2<=n<=8`; all connected nonbipartite `3<=n<=8`) — reproduced by an independent engine AND by re-running the frozen checkers |
| "L5 condition (6) holds for every connected nonbipartite graph" | CONJECTURAL — open; the `n<=8` sweep is regression-scope only |
| pre-repair checker hash `6e555454…` | ABORTED-NO-VERDICT provenance detail, not independently verifiable, no mathematical weight |
