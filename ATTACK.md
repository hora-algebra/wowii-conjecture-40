# Attack protocol for the open remainder of WOWII Conjecture 40 (v4)

This repository is a sealed research artifact (main branch, tags
v1.0/v1.1/v2.0) plus this protocol. If you are an AI agent: follow this file
exactly. Do not modify main, with one exception: appending to
`attempts/LESSONS.md` via pull request per Step 5. Everything you do happens
on your own attempt branch.

## Status of the main statements (see paper.pdf v2 for exact statements)
1. LEMMA A° (paper §4.1): in the incidence model, under hereditary FVS
   tightness, the forced core contains no cycle. OPEN. Verified exhaustively
   n ≤ 14 (2,391,365,507 instances at n = 14 alone, zero cyclic cores;
   dual-engine, hashes in paper §6).
2. SAFE-EXISTS: the remaining existential safe-toggle/descent statement needed
   to obtain F2 without a universal local toggle claim. OPEN. SD-SHORT is
   FALSIFIED (n=11, six witnesses; 1,184 at n=12); SD-2STEP-DESCENT and
   SD-PLUS-2 are computational evidence, not proofs. The completed n=12
   scan is recorded on attempt/2026-08-05-claude-opus-5-4d7a.
3. F2 (the statement Theorem 3.13 actually needs: some fixed edge admits an
   acyclic feasible selection): verified directly through n = 13 in the
   stronger F2-ALL form, zero failures. OPEN in general.
4. SV (paper §5): FALSIFIED, minimum order 11. Certified witnesses and the
   unique-singleton-OCT mechanism are in SV-FALSIFIED.md on main. Do not
   attack or revive it; Theorem 5.5 rests on a false hypothesis. LIFT-P is
   FALSIFIED by the same witnesses.
5. The lifting inequality LIFT-A (for some minimum OCT T,
   ℓ(G) ≥ 2τ(G−T) + |T| + 1) and its universal form LIFT-A-ALL: OPEN, with
   zero failures over every connected graph n ≤ 10 plus the preregistered
   n = 11 classes. This is the SURVIVING route to the general case given the
   bipartite case. Proved sufficient coverage: L1/L2 (branch
   attempt/2026-08-03-claude-opus-5-5047), L3/L4/L5
   (attempt/2026-08-04-codex-a7c3), L6/L7
   (attempt/2026-08-04-claude-fable-5-0eb8). OBSTRUCTION: the CX(m) family
   (L5-CONDITION-FALSIFIED.md on the fable branch; first member
   CX11 = `J??FF?^FuE?`, n = 11, unique minimum OCT) defeats every
   minimum-OCT threshold computable from per-component class sizes and
   full-side forest-extension invariants — no such threshold can be
   universal. Any new sufficient condition must read deeper structure:
   partial-side forests / hub deletions in 2-connected dense blocks, or the
   apex's stitching into the path cover.
Proving Lemma A and SAFE-EXISTS closes the bipartite case. Proving LIFT-A (or
LIFT-A-ALL) plus the bipartite case closes the conjecture. Falsifying any open
statement above, with a verified witness, is equally a success outcome.

## Step 0 — freshness check (every run, before anything else)
Check, in order: (a) open issues and pull requests on this repository;
(b) the MathOverflow question
https://mathoverflow.net/questions/513887/ for new answers or comments;
(c) the maintained WOWII page
http://cms.uhd.edu/faculty/delavinae/research/wowII/open.html for a status
change on Conjecture 40; (d) a web/arXiv search for new work on the
conjecture or the lemmas. If anything has been resolved by others, your
run's job changes to: obtain their argument, verify it against this
repository's oracle and data, and report. Record what you checked in your
report even if nothing changed. If you have no network access, say so in
the report and proceed.

## Step 0.5 — learn from prior attempts
Fetch and read the accumulated knowledge before any new work:

```
git fetch origin 'refs/heads/attempt/*:refs/remotes/origin/attempt/*'
```

`attempts/LESSONS.md` on main is now POPULATED and BINDING. Read it, and
`ATTEMPT_REPORT.md` on every `origin/attempt/*` branch. Treat [FALSIFIED]
and [DEAD END] entries as binding — re-attacking one requires first
refuting, in writing in your report, the recorded reason it died. Treat
[CONJECTURAL LEAD] entries as candidate starting points alongside Step 3.

## Step 1 — comprehension gauntlet (mandatory before any new mathematics)
Write GAUNTLET.md on your branch containing, in your own words with full
derivations: (i) the reduction chain of paper Theorem 3.13 (why A + B imply
the bipartite case, including the exact role of each); (ii) why the abstract
even-cycle system shows Hall feasibility alone cannot yield Lemma A —
hereditary tightness is essential; (iii) for each witness in
tools/witnesses/, which proof strategy it kills and the exact mechanism:
O-56 and O-63 versus the degree-2/private-cycle localizations, O-64 versus
B_s-localization; (iv) the statement and proof of the T_F normalization
(paper Lemma 4.7) and what it licenses. If you cannot complete the gauntlet
correctly, STOP and report that; do not proceed to new work.

## Step 2 — rules of engagement
- Status vocabulary is mandatory for every claim: MATHEMATICALLY PROVED /
  LEAN-FORMALIZED / COMPUTATIONALLY VERIFIED (with universe) / CONJECTURAL /
  FALSIFIED / FROZEN / ABORTED-NO-VERDICT. Nothing ships without a label.
- Every new sub-claim must be stated exactly and then TESTED before use:
  against the witnesses, against exhaustive small-n data via tools/, or by a
  fresh preregistered scan (freeze + hash the checker first, gold-test it,
  then run). A prose proof with no oracle contact counts as NOTHING. This
  project's documented death pattern is: plausible pattern, holds n ≤ 10,
  frozen, killed at n = 11 by a sealed holdout. It has now fired three
  times (Lemma B shortest-path form; SV/LIFT-P; the L5/L6 lifting
  conditions). Assume your first three ideas are that pattern.
- Do not modify frozen statements, ledgers, or anything on main.
  Append-only ledger discipline applies to your own branch records.
- Known dead ends (do not re-walk; ledgers and LESSONS.md have the
  forensics): shortest-path-only Lemma B (A1/U1, falsified); B_s/P/T_F
  universal localizations for Lemma A (witness-refuted); the O68 motif
  branch (permanently frozen); SV and LIFT-P (falsified at n=11);
  class-size / full-side forest-extension lifting thresholds
  (CX(m)-refuted).

## Step 3 — targets, in suggested order
1. Lemma A via the carrier-poset endgame: use CP's inclusion-maximal carrier,
   its two capacity holes, punctured tightness, and the augmented forest
   quotient. ADJ is false, so do not assume adjacent maxima or a
   puncture-free endpoint.
2. SAFE-EXISTS via scheduled descent: attack the existential safe-toggle
   statement, not SD-SHORT or scheduling by choice of cycle. Treat the
   completed n=12 SD-2STEP/SD-PLUS-2 results as evidence with their stated
   scope, not as a proof.
3. Exact LIFT-A on unique-minimum-OCT graphs, via partial-side/hub-deletion
   forest bounds for 2-connected dense bipartite blocks — the CX(m)
   obstruction lives exactly there, and both SV and the lifting conditions
   died at unique singleton OCTs. Enumerate excess-0 components
   (PREREG-E1.md sense) at n = 11, 12 FIRST, and preregister any proposed
   threshold against that population before writing a line of prose about
   it.
4. Resume the frozen n=12 B-PLUS-2 structured holdout exactly per
   proofs/FROZEN-BPLUS2.md with the hashed checkers in tools/.
Any verified movement on any target is a successful run.

## Step 4 — verification oracle
tools/ contains the frozen checkers with hashes (verify against
tools/SHA256SUMS.txt before trusting a binary you built). Any claimed proof
of Lemma A or B must, before being written up: (a) have each of its lemmas
instantiated and machine-checked on the witnesses and on sampled n ≤ 10
instances; (b) survive your own adversarial pass hunting for exactly the
overfit pattern above; (c) be written self-contained with every hypothesis
stated. If you can Lean-formalize any new lemma against
google-deepmind/formal-conjectures definitions, that is the gold standard.

## Step 5 — branch and report protocol
- Branch: `attempt/YYYY-MM-DD-<model-name>-<4 random hex chars>`. The
  4-hex-character uniqueness suffix is mandatory — concurrent attempts exist.
  Never commit to main. Never force-push. Commit freely on your branch.
- Stopping rule: declare a soft time budget at the start of the run and
  record it in your report. Prefer COMPLETING one preregistered run over
  launching the next. At wrap-up, finish only jobs projected to end within
  15 minutes; mark everything else ABORTED-NO-VERDICT with checkpointed,
  resumable state on disk. An aborted run honestly labeled is not a
  failure; an unlabeled one is.
- End EVERY run — success, failure, or timeout — by writing
  ATTEMPT_REPORT.md at your branch root:
    model/harness and date; step-0 and step-0.5 findings; gauntlet outcome;
    targets attacked; every claim made, with status label and its
    verification evidence (hashes, universes, runtimes); dead ends hit and
    why; recommended next angle for the following attempt.
  ATTEMPT_REPORT.md MUST end with a final section titled
  "## LESSONS FOR FUTURE ATTEMPTS" written in exactly the entry format of
  attempts/LESSONS.md — self-contained statement-level bullets, no narrative,
  5–15 lines.
  "No verified progress" written cleanly is a GOOD report and the expected
  modal outcome. A report claiming a proof that never touched the oracle is
  a failed run regardless of how convincing the proof reads.
- End-of-run propagation: push your attempt branch if you have credentials.
  Then propagate your lessons: create branch `lessons/<your-branch-suffix>`
  off main, append your LESSONS section verbatim to attempts/LESSONS.md, and
  open a pull request titled "Lessons: <branch>". attempts/LESSONS.md is the
  ONLY file on main an attempt may ever propose changing, and only via PR,
  and only by appending. If you lack push/PR credentials, print the lessons
  block at the top of your final output and state that the operator must
  merge it.
