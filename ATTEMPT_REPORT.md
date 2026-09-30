# Lemma A° odd-equality proof proposal — 2026-09-30

Branch: attempt/2026-09-30-codex-6e29. Harness: OpenAI Codex.
This is an AI-generated research submission for review, not a claim of human
refereeing, environmental blindness or complete Lean formalization.

## Target and verdict scope

MATHEMATICALLY PROVED is used here for the author-side claim in
proofs/LEMMA-A-ODD-EQUALITY.md: every minimum FVS of a finite simple bipartite
graph, with any remaining forest edge reserved by endpoint capacities one,
has an acyclic forced incidence core. The argument is self-contained.
The repository's accepted status must not be raised merely by merging this
report or the lessons. F2, SAFE-2-EXISTS and WOWII40 remain unresolved here.

## Freshness and prior work

Base main: 290d1b28fd70038824fbba736e1bf47dd83aed01. ATTACK.md is v5;
PR #9 proposing v6 is open. Its status correction is respected: prior
certification of NC/CE/A-I+ is not certification of all of Lemma A.
MathOverflow 513887 was fetched directly on 2026-09-30 and had answerCount=0.
The WOWII maintained mirror timed out; its live status was not verified.
Web searches for the named conjecture/lemma found the existing project and
question, not an additional proof; this is not an exhaustive novelty search.
All nine available attempt reports and main's LESSONS were read in a separate
citation review. Verify branches contain inherited attempt reports: these
were not miscounted as independent full-lemma audits. This proof does not
rely on the disputed endgame or borrow its certification.

Existing work is credited in both proof notes. In particular the strict
neighbourhood bound is already in 064c Theorem 6(iv); the proposed new
contribution combines odd equality structure with minimal carriers.

## Protocol deviations and comprehension

The candidate was developed before this repository-specific packaging run.
Its gauntlet and some exploratory computations were retrospective; we do not
claim that they were preregistered. review/COMPREHENSION.md records the full
reduction, the Hall-only counterexample, the three warning instances, and
normalization. New packaging scans were frozen in commits before execution,
with checker hashes in review/. This is a transparent submission of an
existing candidate, not a claim of perfect historical protocol compliance.
The initial packaging window was one hour. No incomplete computational job
is used as evidence and no job remains running for these scans.

## Verification

COMPUTATIONALLY VERIFIED, with exact scope:

- Upstream tool/witness hashes: 17/17 matched before use.
- O-56/63/64: all three negative controls have a cyclic forced core, with
  1/6/1 selections and 8/4/6 forced edges. Each fails minimum-FVS tightness.
- Upstream a1_verify 7: 143/143, failures=0, witness failures=0, capped=0.
- Upstream forced_core 8: 2186 instances, cyclic cores=0, max path length=6.
- All 5015 connected bipartite graphs of orders 2–10: 158576 minimum-FVS/edge
  instances, 94691 tight sets, 4650 shared tight sets, 5996 strict-neighbour
  checks, 14083 carrier checks. Direct selection intersection checked on
  1000 instances only. No failed assertion; scan exit code 0.
- All 33868 labelled simple graphs of orders 0–6: 293990 independent-X/forest-H
  partitions; 88436 strict-even premises, 5820 odd-equality premises and
  2580 nonempty expansion premises. No failed assertion; scan exit code 0.

Reproduction: review/README.md. Exact outputs and checker hashes are retained.
These results are finite error searches. They are not full formal proofs.
AI mathematical reviews of the Japanese proof and English version found no
specific logical gap. They were not environmentally blind; agreement is not
independent certification. No status is inferred from earlier agents' labels.

## Next step

Review the deletion equality case and the final carrier-union contradiction.
If accepted mathematically, formalize the full graph statement. Do not infer
an acyclic feasible selection from an acyclic intersection of all selections.

## LESSONS FOR FUTURE ATTEMPTS

- [MATHEMATICALLY PROVED — proof proposal, not upstream certification] A self-contained author-side proof of full Lemma A° is supplied in [the proof note](https://github.com/hora-algebra/wowii-conjecture-40/blob/859676ec0f68ea0fe0673c8a70b4abed49e93f5a/proofs/LEMMA-A-ODD-EQUALITY.md); it uses odd equality structure and canonical-carrier minimality. No accepted-status change is requested by this entry.
- [MATHEMATICALLY PROVED — proof proposal] For a forest H plus independent X with tau(H union X)=|X| and sum_h min(2,d_X(h))=2|X|+1, if U={h:d_X(h)>=2} is nonempty, the private-neighbour degrees on X are 2 on B, 1 at a unique t, and 0 on Z, with |Z|=|U|-1 and U contained in N(t).
- [TOOLING] The strict neighbourhood inequality used in the proof is already present in attempt 064c Theorem 6(iv), and the base deletion argument is related to C5b; those ingredients are not claimed as new.
- [COMPUTATIONALLY VERIFIED] Prospective checks: 5015 connected bipartite graphs of orders 2–10, 158576 minimum-FVS/edge instances; all 33868 labelled simple graphs of orders 0–6 for the auxiliary deletion lemmas, 293990 eligible partitions. Exact premise counts, hashes and reproduction instructions are in review/ on the attempt branch; no assertion failed.
- [COMPUTATIONALLY VERIFIED] The unchanged upstream oracle reproduces all three O-56/O-63/O-64 negative controls, a1_verify 7 gives 143/143 without caps, and forced_core 8 gives 2186 instances with no cyclic core and maximum path length 6.
- [TOOLING] This is AI-generated work, with non-blind AI review and no human refereeing or full Lean formalization claimed. Original exploratory work and comprehension were retrospective; only the new recorded scans were prospectively frozen. F2 and Conjecture 40 are not proved by this submission.
