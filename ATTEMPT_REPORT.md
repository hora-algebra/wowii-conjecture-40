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

The 9d2b report graded 1,140 retained n=12 hard records and left 44 cap-omitted.
The operator's current binding statement promotes the retained population to
complete; that later provenance is not present on a fetched ref and will not be
misdescribed here as independently re-run evidence.

No falsified or dead-end statement will be revived.

## Step 1 — comprehension gauntlet

**COMPLETED.** `GAUNTLET.md` freshly derives the full reduction, the Hall-tight
abstract cycle showing hereditary tightness is essential, the exact
O-56/O-63/O-64 mechanisms, and the T_F normalization including re-forcing by
F1 rather than false monotonicity.

## Targets, claims, evidence, dead ends, and recommendation

To be completed at wrap-up.

## LESSONS FOR FUTURE ATTEMPTS

To be replaced at wrap-up by 5-15 self-contained statement-level lines in the
binding lessons format.
