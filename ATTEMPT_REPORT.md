# ATTEMPT REPORT — SAFE-EXISTS / universal B-PLUS-2

## Run identity and outcome

- Model/harness: OpenAI Codex, GPT-5, local shell harness.
- Date: 2026-08-05, America/Chicago.
- Branch: `attempt/2026-08-05-codex-gpt-5-9d2b`.
- Fresh base: public `main` commit
  `64eb3dacd3e332b9464faece8bd42f72e16bf6dc` (`ATTACK.md` v4).
- Constraint: local commits only. Nothing was pushed; no PR, tag, release, or
  public post was made.
- Soft budget: 180 minutes, restarted at `2026-08-05T11:39:54-05:00`, soft
  deadline `14:39:54-05:00`, with the v4 15-minute wrap rule.
- Primary target: SAFE-EXISTS, with the four user-designated binding inputs.
  No secondary target was opened.

The main finite result is **COMPUTATIONALLY VERIFIED (exhaustive n=12
universe, composite census)**: universal all-cycle B-PLUS-2 has zero failures
over all 228,810,295 selected cycle components at n=12. This closes the precise
quantifier gap left by 4d7a; it is finite evidence, not a proof.

The main structural result is a separation. **B-TERMINAL-SLIDE is FALSIFIED at
n=12**, and both unrestricted SUCCESSOR-ONE statements introduced here are
**FALSIFIED at n=12**. Nevertheless, the weakest descent-sufficient
SAFE-2-EXISTS core remains **CONJECTURAL** and retains the inherited exhaustive
n=12 computational support. A new hard-state-only successor statement survives
1,140 retained n=12 states and is the recommended proof target.

## Protocol restart, freshness, and branch discipline

The initial pre-resume interpretation that local v3 plus the activation message
could act as a narrow v4 delta is **WITHDRAWN**. After the user supplied the
resolved provenance, I ran the requested public-remote commands first, fetched
public `main`, read its actual v4 and `attempts/LESSONS.md`, and restarted Step 0
and the time budget. No mathematics or preregistration was performed under the
withdrawn interpretation.

The isolated clone is
`<local-clone>`.
The unique suffix `9d2b` was generated before branch creation. Main was never
checked out for editing. The first two branch commits record the clean restart:

- `5a458c3` — fresh v4 comprehension gauntlet;
- `06119dc` — initial SAFE-EXISTS preregistration and frozen checker.

## Step 0 — freshness findings

Checked in the v4 order:

1. GitHub issues and pull requests: no open issue or PR; public `main` was
   `64eb3da`.
2. MathOverflow question 513887: zero answers, zero comments, not closed.
3. Maintained WOWII page: Conjecture 40 still had status `O`.
4. Web/arXiv searches: no resolving work on Conjecture 40, Lemma A, or
   SAFE-EXISTS was found. The Formal Conjectures entry remains a statement, not
   a proof.

Therefore the primary target did not change.

## Step 0.5 — binding lessons and provenance audit

I read public `attempts/LESSONS.md` through the maintenance-reconciliation entry
and every complete public attempt report: `5047`, `a7c3`, `0eb8`, `4d7a`, and
`b17e`. The reconciliation lesson requiring post-push existence proofs was
treated as binding.

The four binding SAFE inputs resolve as follows.

- **FALSIFIED:** SD-SHORT and SD-COUNT-SHORT have six n=11 failures and 1,184
  n=12 failures. A greedy one-step schedule and scheduling only by cycle choice
  are dead.
- **COMPUTATIONALLY VERIFIED (exhaustive n<=11):** VERIFY-2 independently
  reproduces the six A1 failures, all 20 successful one-lookahead paths, and
  zero universal B-PLUS-2 failures.
- **COMPUTATIONALLY VERIFIED (exhaustive n=12, source 4d7a):** SD-2STEP-DESCENT
  has zero failures on 1,380 A1-failing cycles, and SD-PLUS-2 has zero failures.
- **OPEN AT START OF THIS RUN:** the universal all-cycle B-PLUS-2 n=12 grade.
  The 4d7a selection-level scan could skip the 196 A1-bad cycles co-occurring
  with an A1-good cycle.

There was a provenance mismatch in the user shorthand, handled without assigning
cause: VERIFY-2 explicitly labels n=12 `NOT CHECKED`; the prospective exhaustive
n=12 survival is recorded by 4d7a. Both were used at their checked-in scopes.

## Step 1 — comprehension gauntlet

`GAUNTLET.md` was completed in fresh prose and committed before new mathematics.
It contains:

1. the complete Theorem 3.13/F2 reduction and the separate roles of Lemmas A
   and B;
2. the abstract even-cycle demonstration that Hall feasibility alone cannot
   yield Lemma A;
3. exact O-56/O-63/O-64 mechanisms and the proof strategies each kills;
4. the T_F normalization and its proof, including why re-forcing uses F1 rather
   than monotonicity.

Outcome: **COMPLETED**. The inherited manifest also passed 17/17 entries with
`cd tools && shasum -a 256 -c SHA256SUMS.txt`.

## Exact SAFE core

`PREREG-SAFE-EXISTS.md` defines:

**SAFE-2-EXISTS.** For every cyclic feasible selection J, either J admits a CES
minimizing step, or some A1-bad minimizing step J -> J0 has
`c(J0) <= c(J)` and J0 admits a CES minimizing step.

**MATHEMATICALLY PROVED, conditional on SAFE-2-EXISTS:** this statement is
descent-sufficient. The first alternative strictly decreases the nonnegative
integer c. In the second, the first step does not increase c and the CES second
step strictly decreases it. Repeating blocks of at most two steps reaches an
acyclic feasible selection, hence F2. This is a state-level existential claim;
it does not require every bad cycle or every minimizing move to work.

The universal statement remains **CONJECTURAL**. Its inherited finite grade is
**COMPUTATIONALLY VERIFIED (exhaustive n<=12)** through the stronger 4d7a
SD-2STEP-DESCENT census. This run did not promote that finite evidence to a
general proof.

## Gold tests and controls

The primary checker `safe_exists_scan.py` was frozen at sha256
`880e2822cc7e5a155d103f3d9f6df73c23aa6e5d7ef69aff305e5cc6eeb250b8`
before mathematical execution.

- `--ces=always`, n=8: 2,584/2,584 cycles A1-good.
- `--ces=never`, n=8: 2,584/2,584 cycles A1-bad and every failure channel
  fired. This is a mutation control only.
- Real n=9: 730 graphs, 24,195 cycle components, zero A1 failures.
- Real n=11, eight shards: 25,598 graphs; 8,202,633 cycle components;
  8,071,822 cyclic selections; six A1 failures; 20 bad minimizing paths; zero
  terminal-slide, successor-one, SD-2STEP, SAFE-2 local, Lemma-A, or path-cap
  failures. Maximum shard wall time was 1,568.821 s under shared CPU contention.
- The optimized multi-cycle gold test independently reproduced 130,811 n=11
  multi-cycle selections, 261,622 cycle components, and zero A1 failures.

These are **COMPUTATIONALLY VERIFIED** controls on the stated finite universes.

## Result 1 — universal B-PLUS-2 through n=12

**Status: COMPUTATIONALLY VERIFIED (all connected bipartite graphs at n=12,
every minimum FVS, every fixed H-edge, every feasible selection, all
228,810,295 selected cycle components).**

The conclusion is a composite exhaustive census, not a sample:

1. Fixed 4d7a commit `5cb5bb9a29718562d4d25a6902fd693f0a4677f4`
   exhaustively records 1,380 A1-bad cycles with profile `(1,0):1,184` and
   `(2,1):196`, zero SD-PLUS-2 failures, zero Lemma-A violations, and zero caps.
   On a one-cycle state, selection-level SD-PLUS-2 necessarily grades that sole
   cycle; hence all 1,184 `(1,0)` cycles are individually covered. Every
   A1-good cycle is trivially B-PLUS-2-good.
2. The fixed source retains full certificates for 170/196 `(2,1)` cycles.
   Generic replay validated all 170 and enumerated 3,376 simple residual paths:
   every cycle had `d0=3`, first CES length `dCES=5`, zero failures, and zero
   infeasible candidates.
3. Certificate caps omitted 14 shard-11 and 12 shard-14 cycles. Exact tail scans
   started from the entire graph containing each 50th retained certificate.
   Both boundary graph6 strings matched. Shard 11 graded 26 tail A1 failures,
   all good (624 bounded paths, 1,121.922 s); shard 14 graded 44, all good
   (1,008 bounded paths, 497.037 s). There were zero invalid candidates, caps,
   or B-PLUS-2 failures.
4. The replay/tail union is exact: shard-11 overlap is 12 and shard-14 overlap
   is 32, so `170 + 26 + 44 - 12 - 32 = 196` distinct gap cycles.

The generic checker was frozen at sha256
`b3831f85d5be5c27cddca1c2e4b2e18629c1dd80a0c652c9c3141114ce2715a9`;
the exact tail checker at
`75c1468217d6fb9f1fafb9c9a007d63c2064731f20abc3dbfecbdafbe10b31ae`.
The generic engine reproduced the six n=11 positive-gap controls exactly:
`d0=3`, `dCES=5`, zero failures.

This result closes the recorded cheapest high-value continuation. It does not
prove B-PLUS-2 universally.

## Result 2 — terminal-slide and unrestricted successor-one fail

**B-TERMINAL-SLIDE: FALSIFIED, minimum known order n=12.** It holds throughout
the exhaustive n<=11 data, but every one of the 170 retained `(2,1)` n=12
certificates has no terminal-slide repair. One independently checked witness is:

- graph6 `K??FFbw}Fw^_`;
- `S={6,7,8,9,10}`, fixed edge `e=(4,11)`;
- target selected cycle `{0,1,6,7}` in the selection recorded in
  `work/9d2b/results/independent-witness.json`.

VERIFY-2's independent engine at public commit
`6a94cb9b8b137249d6a19f25589112c09fdca9ee` (engine sha256
`ac11fc10b95e14fb8d6f6d06d2210b6809e0dea1e0b7a28d60081d21b96248a6`)
confirms: `tau=5`, S is a minimum FVS, selection feasible, two selected cycles,
target `d0=3`, 12 minimizing paths, zero minimizing CES paths, zero terminal
slides, and generic first CES length five.

**SUCCESSOR-ONE-ALL and SUCCESSOR-ONE-DESCENT: FALSIFIED at n=12.** On the same
independent witness, all 12 minimizing successors have one selected cycle,
minimum residual distance three, and a CES minimizing step. Thus two-step
descent works, but no length-one second step exists. In the 170-record primary
replay, 142 fail both unrestricted successor-one forms while all 170 pass
SD-2STEP-DESCENT.

This separates mismatches from causes. The data establish that terminal-slide
and length-one successor geometry are too strong in multi-cycle `(2,1)` states;
they do not establish a general causal explanation for why SAFE-2 survives.

## Result 3 — hard-state successor refinement

**HARD-SUCCESSOR-ONE: CONJECTURAL (exhaustive n<=11 hard states plus 1,140
retained n=12 hard-state certificates).**

The claim is restricted to states with no A1-good cycle: some minimizing first
step has `c(J0)<=c(J)` and J0 has a CES minimizing step of length one. Together
with the direct A1-good alternative it is **MATHEMATICALLY PROVED** to imply
SAFE-2-EXISTS by the same integer-descent argument.

The frozen replay graded all 1,140 retained `(1,0)` n=12 certificates and all
3,924 bad minimizing paths: zero terminal-slide, unrestricted successor-one,
HARD-SUCCESSOR-ONE, SD-2STEP, SAFE-2 local, or path-cap failures. The fixed full
profile contains 1,184 hard states, so 44 cap-omitted records remain ungraded for
this post-hoc strengthening (shards 4, 11, 13, 14, 16, and 25). The checker
sha256 is
`8ac92f96345b18f90c72a88ad90d0812a205b1ebd55aff6096593c02ccf68897`.

This is not prospective evidence: the statement was formulated after the
`(1,0)/(2,1)` split was known. Its value is proof-target selection. The
unrestricted successor-one counterexamples are irrelevant to the weakest SAFE
state obligation because every one already has an A1-good cycle.

## Post-hoc mechanism observation

**CONJECTURAL, post-hoc observation on the 170 retained `(2,1)` records:** the
checker-selected shortest generic length-five repair always uses the other
A1-good cycle. In 142 records it removes one selected incidence of that cycle;
in 28 it removes two. This explains the data-level distinction between generic
B-PLUS-2 and terminal extension, but it is neither preregistered universal
evidence nor a proof.

## Tooling, repairs, and aborted jobs

All current checker hashes are in `work/9d2b/SHA256.txt`; all verdict-bearing
result hashes are in `work/9d2b/RESULT-SHA256.txt`. Both manifests pass.

Two validator defects were caught before their outputs were used:

- replay v1 compared normalized undirected certificate edges with `(S,H)`
  generator edges without normalizing both sides; 118 false invalidations;
- hard-state replay v1 reused a `(2,1)` validator on `(1,0)` records; 1,140
  false invalidations.

Both v1 outputs are retained with `-v1-invalid` names and excluded from all
verdicts. The repairs changed only validation, were documented, re-hashed and
committed before rerun, and then produced zero invalidations.

Four n=12 jobs are **ABORTED-NO-VERDICT**: two full multi-cycle mechanism shards
and two full generic replacements. They were stopped without output when
shared-machine contention made them redundant. The exact certificate replay
plus cap-boundary tails replaced them and completed the primary grade within
budget. No other process on the shared machine was modified.

## Dead ends and scope boundaries

- **DEAD END / binding:** greedy shortest-step scheduling and scheduling only by
  choice of cycle; the six n=11 and 1,184 n=12 SD-SHORT failures remain binding.
- **FALSIFIED:** B-TERMINAL-SLIDE cannot be the universal proof of B-PLUS-2.
- **FALSIFIED:** unrestricted successor distance one cannot prove
  SD-2STEP-DESCENT; multi-cycle states force distance three in the verified
  witness.
- **NOT CLAIMED:** finite enumeration proves SAFE-EXISTS, Lemma B, F2, or the
  conjecture in general.
- **NOT CLAIMED:** VERIFY-2 independently checked the full n=12 census. It did
  not; only the fixed witness was independently checked here.

## Recommended next angle

Attack HARD-SUCCESSOR-ONE only on states with no A1-good cycle. This is closer
to the weakest descent-sufficient obligation than either universal B-PLUS-2 or
per-bad-cycle SD-2STEP. In all retained n=12 hard states, J has one selected
cycle, every bad minimizing reroute creates one replacement cycle, and every
successor admits a length-one CES step. A proof should show that the crossing
cycle created in this no-good/single-cycle regime necessarily exposes such a
length-one exchange. It must not quantify over bad cycles in `(2,1)` states:
those are the new counterexamples, and the original state should simply use its
other A1-good cycle.

The cheapest finite cleanup, if desired before proof work, is to grade the 44
cap-omitted hard-state records in the six identified shards. It would complete
HARD-SUCCESSOR-ONE at n=12, but would still be finite evidence.

## LESSONS FOR FUTURE ATTEMPTS

- [COMPUTATIONALLY VERIFIED] Universal all-cycle B-PLUS-2 has zero failures through n=12: the 4d7a census covers every A1-good cycle and all 1,184 one-cycle A1-bad states, while this attempt generically graded the complete 196-cycle `(2,1)` gap by 170 fixed-certificate replays plus exact cap-boundary tails; the retained 170 all have `d0=3` and first CES length 5, and every tail-only record has a CES path within `d0+2`.
- [FALSIFIED] B-TERMINAL-SLIDE is false at n=12 despite holding through n=11: `K??FFbw}Fw^_`, `S={6,7,8,9,10}`, `e=(4,11)` has a feasible two-cycle selection whose target cycle has 12 bad minimizers, no terminal slide, and first generic CES at length 5; VERIFY-2 independently confirms the certificate.
- [FALSIFIED] Unrestricted SUCCESSOR-ONE-ALL and SUCCESSOR-ONE-DESCENT are false at n=12 on the same witness: every minimizing successor has `d0=3`, although every successor does admit a CES minimizing step, so SD-2STEP-DESCENT survives.
- [CONJECTURAL LEAD] HARD-SUCCESSOR-ONE restricts length-one successor geometry to states with no A1-good cycle and is descent-sufficient; it has zero failures on all six n=11 hard states and 1,140 retained n=12 `(1,0)` states covering 3,924 minimizing paths, with 44 cap-omitted records still ungraded.
- [MATHEMATICALLY PROVED] SAFE-2-EXISTS is sufficient for F2: either one CES minimizing step decreases the cycle count, or a nonincreasing minimizing first step followed by a CES minimizing step decreases it within two moves; iteration terminates because the cycle count is a nonnegative integer.
- [DEAD END] Do not prove terminal-slide or length-one successor geometry for every A1-bad cycle: multi-cycle `(2,1)` states falsify both stronger mechanisms but already satisfy the direct A1-good alternative, so those obligations are irrelevant to the weakest SAFE state claim.
- [CONJECTURAL LEAD] In all 170 retained `(2,1)` gap records, the checker-selected generic length-five B-PLUS-2 repair uses the other A1-good cycle (one removed incidence in 142 records, two in 28); treat this as post-hoc mechanism data, not a proof.
- [TOOLING] VERIFY-2 independently confirms scheduled-descent only through n<=11 and marks n=12 NOT CHECKED; the prospective exhaustive n=12 evidence comes from 4d7a, while this attempt used VERIFY-2 only for a fixed n=12 witness recheck.
- [TOOLING] Normalize undirected certificate edges before comparing them with `(S,H)` incidence selections, and bind replay validators to the intended profile; the preserved invalid v1 runs show that representation and profile checks can otherwise create false failures before mathematics is reached.
