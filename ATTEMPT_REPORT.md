# ATTEMPT REPORT — SAFE-2-EXISTS attack 7851

## Run identity and protocol boundary

- Model/harness: OpenAI Codex, GPT-5, local shell harness.
- Date: 2026-08-05, America/Chicago.
- Branch: `attempt/2026-08-05-codex-gpt-5-7851`.
- Base: fetched mirror `origin/main` at
  `64eb3dacd3e332b9464faece8bd42f72e16bf6dc`.
- Constraint: local commits only; nothing will be pushed and no PR, tag,
  release, or public post will be made.
- Soft budget: four hours anchored at branch creation,
  `2026-08-05T22:21:48-05:00`, with the final fifteen minutes reserved for
  report completion and a local commit.
- Sole target: **SAFE-2-EXISTS**, the hypothesis of the certified implication
  `SAFE-2-EXISTS => F2`.
- Selected angle: direct hard-state proof through `HARD-SUCCESSOR-ONE`, using
  the certified Lemma-A carrier/poset/NC/A-I+ stack where it supplies relevant
  structural restrictions.  This was selected because it attacks the exact
  state-level obligation, has zero failures on every graded hard state through
  n=12, and avoids the falsified unrestricted successor and terminal-slide
  claims.

The fetched mirror contains `ATTACK.md` v4 rather than the instructed v6, and
its `main` still labels Lemma A-degree open.  No fetched ref contains v6.
This mismatch is recorded, not silently erased.  The run uses the unchanged
v4 procedural requirements together with the operator's explicit v6 deltas as
binding: Lemma A-degree is CERTIFIED; SAFE-2-EXISTS is the sole target;
SAFE-2-EXISTS implies F2; universal B-PLUS-2 is clean through n=12;
B-TERMINAL-SLIDE and unrestricted SUCCESSOR-ONE are falsified at n=12;
SD-2STEP-DESCENT survives n=12; HARD-SUCCESSOR-ONE is the conjectural lead;
and any proof produced here is labeled CLAIMED pending blind certification.

## Step 0 — freshness

Completed in protocol order on 2026-08-05:

1. GitHub reports zero open issues and zero open pull requests; public `main`
   is the same `64eb3da` exposed by the local mirror.
2. StackExchange API question 513887 reports zero answers and zero comments,
   with no activity after creation.
3. The maintained WOWII page fetched over HTTP and still labels entry 40 `O`;
   its only attached result is the 2004 path-cover-one observation.  The server
   reports `Last-Modified: Mon, 03 Aug 2026 18:00:38 GMT`.
4. Targeted web and arXiv searches found the Formal Conjectures statement and
   related induced-forest/path-cover work, but no proof, counterexample, or
   status change for Conjecture 40 or SAFE-2-EXISTS.

**Finding:** no external result changes the target.

## Step 0.5 — binding prior work

The required attempt-ref fetch completed.  Read in full before new mathematics:

- `attempts/LESSONS.md` on `origin/main` (through the maintenance
  post-push-existence lesson);
- every fetched `ATTEMPT_REPORT.md`: 5047, a7c3, 0eb8, b17e, 4d7a, 0520,
  and 9d2b;
- the available local VERIFY-4 package report and sealed NC derivation.

Binding SAFE facts carried forward:

- **FALSIFIED:** SD-SHORT / SD-COUNT-SHORT, B-TERMINAL-SLIDE, unrestricted
  SUCCESSOR-ONE-ALL and SUCCESSOR-ONE-DESCENT.
- **COMPUTATIONALLY VERIFIED:** universal all-cycle B-PLUS-2 through n=12;
  SD-2STEP-DESCENT through n=12; HARD-SUCCESSOR-ONE on all six n=11 hard
  states and the complete retained n=12 population described below.
- **CONJECTURAL:** HARD-SUCCESSOR-ONE in general.
- **MATHEMATICALLY PROVED, conditional:** SAFE-2-EXISTS implies F2 by integer
  descent.
- **POST-HOC ONLY:** in the 170 retained `(2,1)` records, a length-five repair
  uses the other A1-good cycle.

The 9d2b report graded 1,140 retained n=12 hard records and the operator's
binding statement preserves exactly that scope.  The source profile total is
1,184, leaving 44 certificates omitted by the retention caps.  Completing
those 44 without inspecting them first became the finite experiment below.

No falsified or dead-end statement will be revived.

## Step 1 — comprehension gauntlet

**COMPLETED.** `GAUNTLET.md` freshly derives the full reduction, the Hall-tight
abstract cycle showing hereditary tightness is essential, the exact
O-56/O-63/O-64 mechanisms, and the T_F normalization including re-forcing by
F1 rather than false monotonicity.

## Target attacked and exact reduction

The selected proof route was:

> **HARD-SUCCESSOR-ONE (HSO).**  If a cyclic feasible selection `J` has no
> A1-good selected cycle, some A1-bad minimizing first step `J -> J0`
> satisfies `c(J0)<=c(J)`, and `J0` has a CES minimizing step of length one.

**MATHEMATICALLY PROVED (reduction only): HSO implies SAFE-2-EXISTS.**  If
`J` has an A1-good selected cycle, its defining minimizing toggle is already
the direct CES alternative in SAFE-2.  Otherwise HSO supplies the
nonincreasing A1-bad first step and the length-one CES second step, which is
the other SAFE-2 alternative.  This reduction does not prove HSO.

The angle was chosen over a fresh n=13 slice because HSO is the exact
hard-state obligation, had the strongest inherited finite evidence, and was
the place where the newly certified Lemma-A machinery might conceivably give
a structural theorem.  It also avoids both falsified successor statements:
HSO applies only when there is no A1-good cycle and is existential in the
choice of the first step.

## Carrier-stack proof attempt and obstruction

The intended bridge was to put the certified acyclic forced core and its
carrier/poset/NC/A-I+ structure on the selected cycle, then force the
successful successor exchange from the resulting capacity holes.  The finite
hard-state data show why that bridge cannot be the opening move.

**COMPUTATIONALLY VERIFIED (complete n=12 hard-state certificate profile):**
860 of the 1,184 hard states have zero selected-cycle incidences in the global
forced core; the other 324 have two.  Thus a proof that starts by choosing a
forced incidence of the selected cycle and applying its carrier structure has
no input on 860 states.  This is a dead end for that *direct* bridge only.  It
does not refute Lemma A, the certified carrier results, or an indirect use of
hereditary tightness elsewhere in the state.

Inspection of the 1,140 retained records suggested a different local shape:
after every bad minimizing length-three step, the new 4-cycle has one
`S`-vertex outside the path, and that vertex has a length-one CES escape.  The
exact claim was frozen as OFF-PATH-ESCAPE (OPE) in
`PREREG-HARD-TAIL.md`.  The retained records were marked discovery data; only
the 44 source-cap omissions were prospective for OPE.

## Frozen cap-tail experiment

Frozen inputs:

- checker `work/7851/hard_tail.py`, SHA-256
  `74155bcf20e8993ddb0090d033384f1da667a319a98a52a5bb14db57453710d8`;
- preregistration `PREREG-HARD-TAIL.md`, SHA-256
  `a098b40af65159abcce66be97e9a00df845b7eaa7687b10145e7ecc9e7ff5c38`;
- source commit
  `5cb5bb9a29718562d4d25a6902fd693f0a4677f4`;
- pre-execution commit
  `df55fa41c27414ed40111d0a1e894b322d41e9c1`.

All 17 entries in `tools/SHA256SUMS.txt` passed before and after execution.
The retained real-CES regression and mutation controls were run first:

| run | hard states | bad first steps | HSO failures | OPE failures | wall s |
|---|---:|---:|---:|---:|---:|
| real | 1,140 | 3,924 | 0 | 0 | 15.331 |
| `CES=always` | 0 | 0 | 0 | 0 | 14.503 |
| `CES=never` | 1,140 | 3,924 | 1,140 | 1,140 | 15.250 |

The frozen target command was
`python3 work/7851/hard_tail.py --mode tails --ces real`.  It completed in
2,255.174 seconds with exit code zero.  It consumed all 212,780 graphs from
`geng -bc -q 12`, checked the six frozen graph-index/graph6 boundaries, and
analysed 1,897 graphs in the exact tails, including 4,155,208 cyclic
selections.  There were zero path caps and zero Lemma-A violations.

Every preregistered target gate passed:

| grade | result |
|---|---:|
| source profile `(one cycle, zero A1-good)` | 1,184 |
| retained records / unique valid states | 1,140 / 1,140 |
| unique hard states found in tails | 58 |
| new tail-only hard states | 44 |
| combined unique hard states | 1,184 |
| combined bad minimizing first steps | 4,088 |
| HSO failures | 0 |
| OPE failures | 0 |
| invalid replays / path caps / Lemma-A violations | 0 / 0 / 0 |

**COMPUTATIONALLY VERIFIED (finite scope): HARD-SUCCESSOR-ONE has zero
failures on all 1,184 hard states in the exhaustive n=12 source profile and
all 4,088 of their bad minimizing first steps.**  This completes the 44
certificates omitted by the source retention caps; it does not prove HSO for
larger graphs.

**COMPUTATIONALLY VERIFIED (finite scope): OFF-PATH-ESCAPE has zero failures
on the same 1,184 states and 4,088 steps.**  Its 1,140-state component is
post-hoc regression.  The 44 tail-only states, contributing the 164 steps not
in the retained summary, are the preregistered prospective slice.  OPE remains
CONJECTURAL universally.

The target result is
`work/7851/results/hard-tails-real.json`, SHA-256
`b036acbee18484aa59438f75839ce933f0e894dca6fb41c0dd00d430bdc3bcb0`.
The three control-result hashes and this target hash are frozen in
`work/7851/RESULT-SHA256.txt`; both failure-sample arrays in the target JSON
are empty.

## Final status, dead end, and recommendation

**CONJECTURAL:** SAFE-2-EXISTS remains open.  No proof was produced, so there
is no CLAIMED proof to send through environmentally blind certification and
no theorem status changes.  The certified implication `SAFE-2-EXISTS => F2`
was not re-proved or used as a substitute for its hypothesis.

**DEAD END:** direct import of the Lemma-A carrier stack onto an already
forced selected-cycle edge cannot cover the hard states: 860/1,184 have no
such edge.  The mismatch is absence of an input foothold, not a failure of the
certified stack and not evidence about causality.

**Recommended next attack:** freeze a structured n=13 hard-state slice before
inspection, stratified by number of selected cycles and forced selected-cycle
incidences, and grade HSO and OPE separately.  Oversample the zero-incidence
stratum and any multi-cycle hard states.  If OPE survives prospectively, aim
for its residual-network proof: after a bad length-three toggle, prove that
the unique off-path `S`-vertex of the successor 4-cycle has an unsaturated
adjacent capacity slot giving the length-one CES.  This reads the successor's
exchange geometry rather than requiring the original cycle to lie in the
forced core.

No network write, push, PR, tag, release, or public post was made.

## LESSONS FOR FUTURE ATTEMPTS

## 2026-08-05 — OpenAI Codex, GPT-5 / local shell harness — attempt/2026-08-05-codex-gpt-5-7851
- [MATHEMATICALLY PROVED] HARD-SUCCESSOR-ONE implies SAFE-2-EXISTS: an A1-good cycle gives SAFE's direct CES case, while a hard state is exactly the domain where HSO gives SAFE's nonincreasing first step and CES second step; this proves only the reduction, not HSO.
- [COMPUTATIONALLY VERIFIED] The exhaustive n=12 source profile contains 1,184 hard states and 4,088 bad minimizing first steps; the 44 certificates omitted by retention caps were completed prospectively, with zero HSO failures, zero replay errors, zero path caps, and zero Lemma-A violations (`work/7851/results/hard-tails-real.json`, SHA-256 `b036acbee18484aa59438f75839ce933f0e894dca6fb41c0dd00d430bdc3bcb0`).
- [COMPUTATIONALLY VERIFIED] OFF-PATH-ESCAPE has zero failures on those 1,184 states: every bad length-three first step replaces the unique 4-cycle by one 4-cycle whose unique off-path `S`-vertex has a length-one CES; 1,140 states are post-hoc regression and only the 44 tail-only states are prospective evidence.
- [DEAD END] A proof cannot begin universally by applying the certified carrier/poset/NC/A-I+ stack to a forced selected-cycle incidence: 860/1,184 n=12 hard states have zero such incidences; this does not rule out indirect use of hereditary tightness or forced structure elsewhere.
- [TOOLING] The cap-tail checker (`work/7851/hard_tail.py`, SHA-256 `74155bcf20e8993ddb0090d033384f1da667a319a98a52a5bb14db57453710d8`) checks six exact graph-index/graph6 boundaries, unions state identities with retained certificates, and requires 212,780 `geng` records; all target gates passed in 2,255.174 seconds.
- [TOOLING] CES mutation controls are live: `CES=always` removes all 1,140 retained hard states, while `CES=never` produces 1,140 HSO and 1,140 OPE failures; hashes for all four result files are in `work/7851/RESULT-SHA256.txt`.
- [CONJECTURAL] SAFE-2-EXISTS, HARD-SUCCESSOR-ONE, and OFF-PATH-ESCAPE remain unproved universally; the next high-information test is a preregistered n=13 hard-state slice stratified by cycle count and forced selected-cycle incidences, oversampling the zero-incidence and multi-cycle strata.
