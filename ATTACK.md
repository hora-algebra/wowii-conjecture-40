# Attack protocol for the open remainder of WOWII Conjecture 40 (v6)

This repository is a sealed research artifact (main branch, tags
v1.0/v1.1/v2.0) plus this protocol. If you are an AI agent: follow this file
exactly. Do not modify main, with one exception: appending to
`attempts/LESSONS.md` via pull request per Step 5. Everything you do happens
on your own attempt branch.

There is no v6 predecessor you are missing. Versions v1.1–v5 existed; v6 is
this file. If an instruction you were given cites an ATTACK.md version higher
than the newest one actually present on `main`, follow the newest one that
exists, say so in your report, and treat the instruction as a delta on top of
it — do not reconstruct a protocol from a version number.

## Status of the main statements (see paper.pdf v2 for exact statements)

1. **LEMMA A° (paper §4.1)**: in the incidence model, under hereditary FVS
   tightness, the forced core contains no cycle. **OPEN.**
   `LEMMA-A-CLEAN-END.md` itself says Lemma A remains open, and no controller
   framing may raise the source's status.
   - **CERTIFIED — the machinery only:** NC (clean-end chordlessness), NCM/CE,
     and A-I⁺. VERIFY-4's verdict word is `CERTIFIED` and its own next sentence
     is the scope: "This verdict covers the mathematical derivations of NC,
     NCM/CE, and A-I⁺." Certifying the machinery is not certifying Lemma A°.
   - **REVIEWED-SOUND, NOT BLIND-REPRODUCED — the refutation-hardened endgame
     document:** VERIFY-5 reviews `LEMMA-A-CLEAN-END.md`; its stated scope is,
     "This verdict applies to the proved target steps NC, CE, and A-I+; it is
     not a verdict that Lemma A° itself has been proved." Direct refutation
     attempts found zero failures for NC(i), NC(ii), the NC consequence,
     CE/NCM, and A-I⁺, with live controls. This is a soundness review of those
     steps, not a proof or blind reproduction of Lemma A°
     (`verify/2026-08-05-verify5`, `VERIFY5_REPORT.md`).
   - **OPEN OBLIGATION — the carrier-to-blocker bridge.**
     `SEALED-DERIVATION.md` states the bridge verbatim:

     > **Carrier-to-blocker bridge (CB).** If the normalized forced core contains
     > `F`, then some nonempty `R subseteq T_F` satisfies
     > `lambda_H(R) <= |R|-1`.

     The same file characterizes the obstruction verbatim:

     > The carrier results constrain the incidence/capacity layer.  The number
     > `lambda_H(R)`, however, depends on how those incidences attach through the
     > components and paths of the forest `H`, and (for general `R subseteq T_F`) on
     > edges internal to `R`.  Contracting components of `H-D` turns the missing
     > step into the augmented-quotient geometry described in `proofs/PROOFS.md`:
     > a deficient blocker must be found even when the quotient is cyclic and even
     > when its useful vertex set is mixed across `P` and several punctures.

     No packaged result proves CB in general. That is the remaining Lemma A°
     obligation.
   - Computational status unchanged: verified exhaustively n ≤ 14
     (2,391,365,507 instances at n = 14 alone, zero cyclic cores; dual-engine,
     hashes in paper §6).

2. **SAFE-2-EXISTS — the open core.** This is where the bipartite case now
   actually stands or falls, and it is the least-defended statement in the
   project. **OPEN.** What is settled around it:
   - **PROVED — SAFE-2-EXISTS ⟹ F2.** Either one CES minimizing step
     decreases the selected-cycle count, or a nonincreasing minimizing first
     step followed by a CES minimizing step decreases it within two moves;
     the count is a nonnegative integer, so iteration terminates
     (attempt/2026-08-05-codex-gpt-5-9d2b; re-derived and CONFIRMED with no
     gap by VERIFY-3 §2.4). The descent consumes only a strict decrease of
     the cycle count, not CES, so SAFE-2-DEC already suffices
     (attempt/2026-08-05-claude-opus-5-064c).
   - **PROVED — HARD-SUCCESSOR-ONE ⟹ SAFE-2-EXISTS.** An A1-good cycle gives
     SAFE's direct CES case; a hard state is exactly the domain where HSO
     supplies the nonincreasing first step and the CES second step
     (attempt/2026-08-05-codex-gpt-5-7851). This proves the reduction only.
     HSO itself is unproved.
   - **PROVED — the hard-state characterization.** `d₀(C) = 1` iff some
     `S`-vertex of the selected cycle `C` has a slack `G`-neighbour. Hence
     every A1-bad cycle has `d₀ ≥ 3`, and in a hard state every `H`-neighbour
     of every cycle `S`-vertex is saturated. A1-goodness is a one-line local
     predicate, so the hard population is isolable with no residual search.
     Relatedly, slack is exactly path-endedness: the incidence graph always
     has exactly `|H|−|S|` path components regardless of cycle count, total
     slack is `2(|H|−|S|−1)`, and `|Sat(J)| ≤ |S|+1` — so in a hard state a
     cycle's `S`-side neighbourhood is squeezed into at most `|S|+1` vertices
     while needing at least `|P(C)|+1` of them (064c).
   - **PROVED — A-I transfer.** Paper Lemma 4.2 (A-I) transfers verbatim from
     forced-core cycles to *selected* cycles, `N_H(P(C)) ⊋ Q(C)`, because its
     proof uses only that the cycle's `S`-side lies in one bipartition class
     and has no `H`-neighbour off the cycle. The certified Lemma-A stack is
     therefore usable on the Lemma-B side (064c).
   - **PROVED — no free lunch.** If `μ = min_J c(J) ≥ 1` then every `c = μ`
     selection is hard, and SAFE-2-EXISTS, SAFE-2-DEC, HARD-ESCAPE and
     HARD-SUCCESSOR-ONE all fail there. Every statement in this family is at
     least as strong as F2 and false exactly when F2 is false, so **no proof
     of any of them can avoid consuming hereditary FVS tightness** — the
     abstract even-cycle system has `μ = 1`. Ask of every candidate you
     write: *where does this use hereditary tightness?* If there is no
     answer, the argument is wrong (064c).
   - **DEAD END — the certified-stack opening.** A proof cannot begin
     universally by applying the certified carrier/poset/NC/A-I⁺ stack to a
     forced selected-cycle incidence: **860 of the 1,184 n=12 hard states
     have zero such incidences** (7851). This does not forbid indirect use of
     hereditary tightness or of forced structure elsewhere; it forbids that
     opening move.
   - **BINDING — the cross-vendor n=12 census.** The complete exhaustive n=12
     universe (all 212,780 connected bipartite graphs; 212,229 with `τ≥1`;
     11,223,582 instances; 1,468,422,722 feasible selections; 228,810,295
     selected cycle components; 1,380 A1-failing cycles splitting 1,184/196;
     1,184 hard states) has now been produced or reproduced by four runs
     across two vendors — 4d7a and 064c (Claude Opus 5), 9d2b and 7851
     (OpenAI Codex GPT-5) — with VERIFY-2 and VERIFY-3 auditing. The 44
     cap-omitted hard-state records that the 9d2b replay left ungraded were
     closed twice independently (VERIFY-3 §2.5 and 7851), 0 failures. Treat
     these figures as the fixed source of record: reproduce them as anchors
     before any new n=12 work, and do not re-run the census as new evidence.
     It remains finite evidence and is not a proof of anything.
   - FALSIFIED nearby, do not re-walk: SD-SHORT and SD-COUNT-SHORT (n=11, six
     witnesses; 1,184 at n=12); ONE-CYCLE (n=10); B-TERMINAL-SLIDE (n=12,
     `K??FFbw}Fw^_`, `S={6,7,8,9,10}`, `e=(4,11)`); unrestricted
     SUCCESSOR-ONE-ALL and SUCCESSOR-ONE-DESCENT (n=12, same witness). Every
     one of those falsifications lives in `(2,1)` states, which SAFE-2-EXISTS
     never needed — they refute obligations that were never load-bearing.
     Only hard states carry content.

3. **F2** (the statement Theorem 3.13 actually needs: some fixed edge admits
   an acyclic feasible selection): verified directly through n = 13 in the
   stronger F2-ALL form, zero failures. OPEN in general.

4. **SV (paper §5)**: FALSIFIED, minimum order 11. Certified witnesses and the
   unique-singleton-OCT mechanism are in SV-FALSIFIED.md on main. Do not
   attack or revive it; Theorem 5.5 rests on a false hypothesis. LIFT-P is
   FALSIFIED by the same witnesses.

5. **The general lifting gap — unchanged.** The lifting inequality LIFT-A (for
   some minimum OCT T, ℓ(G) ≥ 2τ(G−T) + |T| + 1) and its universal form
   LIFT-A-ALL: OPEN, with zero failures over every connected graph n ≤ 10
   plus the preregistered n = 11 classes. This is the SURVIVING route to the
   general case given the bipartite case. Proved sufficient coverage: L1/L2
   (branch attempt/2026-08-03-claude-opus-5-5047), L3/L4/L5
   (attempt/2026-08-04-codex-a7c3), L6/L7
   (attempt/2026-08-04-claude-fable-5-0eb8). OBSTRUCTION: the CX(m) family
   (L5-CONDITION-FALSIFIED.md on the fable branch; first member
   CX11 = `J??FF?^FuE?`, n = 11, unique minimum OCT) defeats every
   minimum-OCT threshold computable from per-component class sizes and
   full-side forest-extension invariants — no such threshold can be
   universal. Any new sufficient condition must read deeper structure:
   partial-side forests / hub deletions in 2-connected dense blocks, or the
   apex's stitching into the path cover. No run since v4 has attacked this;
   it is unmoved, not deprioritized.

Proving Lemma A° and SAFE-2-EXISTS closes the bipartite case. Proving LIFT-A
(or LIFT-A-ALL) plus the bipartite case closes the conjecture. Falsifying any
open statement above, with a verified witness, is equally a success outcome.

## Step 0 — freshness check (every run, before anything else)
Check, in order: (a) open issues and pull requests on this repository;
(b) the MathOverflow question
https://mathoverflow.net/questions/513887/ for new answers or comments;
(c) the maintained WOWII page
http://cms.uhd.edu/faculty/delavinae/research/wowII/open.html for a status
change on Conjecture 40 — note that `cms.uhd.edu` refuses TLS and the live
mirror is `cms.dt.uh.edu`, and that `WebFetch`-style tools that force HTTPS
cannot reach either it or mathoverflow.net, while `curl` reaches both;
(d) a web/arXiv search for new work on the conjecture or the lemmas. If
anything has been resolved by others, your run's job changes to: obtain their
argument, verify it against this repository's oracle and data, and report.
Record what you checked in your report even if nothing changed. If you have
no network access, say so in the report and proceed.

Your freshness check is also a live audit of the maintainer. If the protocol
version, the LESSONS.md contents, or a branch you were told exists does not
match what you actually find, **report the mismatch in your report** and
proceed against what exists. That dissent is evidence and has already caught
one incident; it is never insubordination.

## Step 0.5 — learn from prior attempts
Fetch and read the accumulated knowledge before any new work:

```
git fetch origin 'refs/heads/attempt/*:refs/remotes/origin/attempt/*'
git fetch origin 'refs/heads/verify/*:refs/remotes/origin/verify/*'
```

`attempts/LESSONS.md` on main is POPULATED and BINDING. Read it, and
`ATTEMPT_REPORT.md` on every `origin/attempt/*` branch. The `verify/*`
branches carry the adversarial audits (VERIFY-1 `verify/2026-08-f522`,
VERIFY-2 `verify/2026-08-05-verify2`, VERIFY-3 `verify/2026-08-05-verify3`,
VERIFY-4 `verify/2026-08-05-verify4`); read the audit of any result you plan
to build on, not just the result. Treat [FALSIFIED] and [DEAD END] entries as
binding — re-attacking one requires first refuting, in writing in your
report, the recorded reason it died. Treat [CONJECTURAL LEAD] entries as
candidate starting points alongside Step 3.

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
- **Scope travels with the verdict.** Never restate someone else's
  verification verdict without quoting the scope sentence that verifier
  attached to it, in the same breath as the verdict word. And the status of a
  statement may only be raised by a verification whose stated scope names
  that statement — certifying its lemmas, its machinery, or its consequences
  does not raise it. Both rules exist because a CERTIFIED verdict scoped to
  "the mathematical derivations of NC, NCM/CE, and A-I⁺" was relayed upstream
  as certification of Lemma A° itself.
- Every new sub-claim must be stated exactly and then TESTED before use:
  against the witnesses, against exhaustive small-n data via tools/, or by a
  fresh preregistered scan (freeze + hash the checker first, gold-test it,
  then run). A prose proof with no oracle contact counts as NOTHING. This
  project's documented death pattern is: plausible pattern, holds n ≤ 10,
  frozen, killed at n = 11 by a sealed holdout. It has now fired three
  times (Lemma B shortest-path form; SV/LIFT-P; the L5/L6 lifting
  conditions). Assume your first three ideas are that pattern.
- Report premise-firing counts next to every "0 failures". A check that never
  fires reads exactly like a check that passes, and a scan universe that
  cannot fire its own negative control is not evidence. If a run caps
  retained records per shard, print the cap and the omitted count and
  reconcile `found = retained-overlap + missing` before calling it
  exhaustive.
- Do not modify frozen statements, ledgers, or anything on main.
  Append-only ledger discipline applies to your own branch records.
- Known dead ends (do not re-walk; ledgers and LESSONS.md have the
  forensics): shortest-path-only Lemma B (A1/U1, falsified); B_s/P/T_F
  universal localizations for Lemma A (witness-refuted); `A_s`-localization
  of the hereditary violation, refuted even existentially by O-64; the O68
  motif branch (permanently frozen); SV and LIFT-P (falsified at n=11);
  class-size / full-side forest-extension lifting thresholds (CX(m)-refuted);
  opening a SAFE-2-EXISTS proof on a forced selected-cycle incidence
  (860/1,184 at n=12).

## Step 3 — targets, in suggested order
1. **SAFE-2-EXISTS, at the hard states.** This is the open core and the
   highest-value target. At a hard state SAFE-2-EXISTS is *equivalent* to
   "some minimizing step that does not increase the cycle count leaves the
   hard set", and the weaker HARD-ESCAPE (leave the hard set in finitely many
   such steps) already gives F2. So the target is a statement about one
   finite digraph on hard states whose out-arcs are described by the
   relocation theorem on the 064c branch. Two cheap decisive experiments are
   named and unrun: (a) the identified universal-successor failure mechanism
   — at a hard state, a minimizing step whose terminal is the released end
   and whose first hop lands back on the cycle leaves the slack set unmoved
   and confines every new cycle inside the old one, so the successor has no
   length-one step at all; it has never occurred in the graded population,
   and searching for that local pattern settles the universal form; (b) every
   hard state seen so far — all 6 at n=11 and every preserved n=12 record —
   has exactly ONE selected cycle; proving or refuting that collapses the
   hard-state digraph. Do not try to prove the successor claim by showing the
   relocated cycle sees the freed vertex `h`: over 1,148 hard-state
   certificates the witnessing slack vertex is `h` alone in 392 steps, an
   already-slack vertex in 1,700, both in 1,848, neither in 0 — any argument
   must produce *some* slack neighbour, not a designated one. A preregistered
   n=13 hard-state slice, stratified by cycle count and forced selected-cycle
   incidences and oversampling the zero-incidence and multi-cycle strata, is
   the recommended new scan.
2. **A blind full-lemma audit of Lemma A°.** The machinery is certified and
   the full statement is not, by anyone, ever. If you can run a genuinely
   environmentally-blind audit — nothing in your working tree beyond a sealed
   package, no attempt report, no prior derivation — that closes the largest
   open verification debt in the repository. Package what you seal and commit
   the seal before you open anything.
3. **Lemma A° via the carrier-poset endgame**, if you are attacking rather
   than auditing: CP's inclusion-maximal carrier, its two capacity holes (now
   known via CE to be a *neighbourhood* statement, not spare capacity),
   punctured tightness, and the augmented forest quotient. ADJ is false, so
   do not assume adjacent maxima or a puncture-free endpoint, and do not
   assume `P ∩ U = ∅`. The obstruction has moved into `Ext(P)` — how the
   cycle vertices' external `H`-neighbours sit in the forest. CAP2-BS is the
   one carrier localization still genuinely open; any run at it needs a
   universe reaching `|H| ≥ 6` so the NOGUARD control can fire natively.
4. **Exact LIFT-A on unique-minimum-OCT graphs**, via partial-side/hub-deletion
   forest bounds for 2-connected dense bipartite blocks — the CX(m)
   obstruction lives exactly there, and both SV and the lifting conditions
   died at unique singleton OCTs. Enumerate excess-0 components
   (PREREG-E1.md sense) at n = 11, 12 FIRST, and preregister any proposed
   threshold against that population before writing a line of prose about it.
   Nobody has touched this since v4.
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
- **Landing is not claiming.** Anything you report as pushed, opened, or
  merged must carry its own existence proof, obtained after the fact and from
  the remote: the remote SHA from `git ls-remote`, an HTTP-200 raw-file fetch
  of a file on the pushed branch, and the PR number with its merge state.
  Without those, write that the work is staged locally and unlanded. Two
  consecutive maintenance batches were once accepted as complete when nothing
  in either had reached the world; the report is not the deliverable, the
  remote state is.
