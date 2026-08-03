# Attack protocol for the open remainder of WOWII Conjecture 40

This repository is a sealed research artifact (main branch, tags v1.0/v1.1)
plus this protocol. If you are an AI agent: follow this file exactly. Do not
modify main, with one exception: appending to `attempts/LESSONS.md` via pull
request per Step 5. Everything you do happens on your own attempt branch.

## What is open (see paper.pdf for exact statements)
1. LEMMA A° (paper §4.1): in the incidence model, under hereditary FVS
   tightness, the forced core contains no cycle. OPEN. Verified exhaustively
   n ≤ 10.
2. LEMMA B (paper §4.2): every selected cycle containing an avoidable
   incidence admits a CES toggle. OPEN. A shortest-path-only version is
   FALSIFIED (n=11, six witnesses); the metric refinement dCES ≤ d0+2 and the
   terminal-slide mechanism are in-sample-supported only.
3. SV (paper §5): every connected nonbipartite G has a vertex t in some
   minimum OCT with p(G) ≤ p(G−t). OPEN. Verified n ≤ 10.
4. The lifting inequality: for some minimum OCT T,
   ℓ(G) ≥ 2τ(G−T) + |T| + 1. OPEN, sufficient for the general case given
   the bipartite case.
Proving A and B closes the bipartite case. Proving SV (or the lifting
inequality) plus the bipartite case closes the conjecture. Falsifying any of
them, with a verified witness, is equally a success outcome.

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

Read `attempts/LESSONS.md` on main, and `ATTEMPT_REPORT.md` on every
`origin/attempt/*` branch. Treat [FALSIFIED] and [DEAD END] entries as
binding — re-attacking one requires first refuting, in writing in your
report, the recorded reason it died. Treat [CONJECTURAL LEAD] entries as
candidate starting points alongside Step 3. If there are no attempt branches
and `attempts/LESSONS.md` is empty, you are the first attempt; proceed.

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
  frozen, killed at n = 11 by a sealed holdout. Assume your first three
  ideas are that pattern.
- Do not modify frozen statements, ledgers, or anything on main.
  Append-only ledger discipline applies to your own branch records.
- Known dead ends (do not re-walk; ledgers have the forensics): shortest-
  path-only Lemma B (A1/U1, falsified); B_s/P/T_F universal localizations
  for Lemma A (witness-refuted); the O68 motif branch (permanently frozen).

## Step 3 — targets, in suggested order
1. Lemma A via the T_F-normalized carrier attack: by paper Lemma 4.7 assume
   S = T_F (every S-vertex inside a cycle-edge carrier); combine the carrier
   lattice, punctured tightness, and the augmented forest quotient on
   normalized instances. This angle was banked, never spent.
2. Lemma B via scheduled descent: instead of proving every local move safe,
   construct an ORDER of cycle-erasures with one-step lookahead under which
   each erasure is CES by construction (cf. the cycle-merge scheduling of
   Lavrov–Vandenbussche, EJC 31(3) #P3.1, adapted to exact demand and the
   capacity-1 pair). Also banked, never spent.
3. SV: prove it, or extend verification to n = 11 (preregistered).
4. The lifting inequality: prove it for some structured class, or hunt
   counterexamples to it (a counterexample redirects the gap work — report
   it as a result, it does not touch the conjecture).
5. Resume the frozen n=12 B-PLUS-2 structured holdout exactly per
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
