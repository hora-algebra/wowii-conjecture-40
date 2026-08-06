# ATTEMPT REPORT — SAFE-2-EXISTS (branch attempt/2026-08-05-claude-opus-5-064c)

## Run identity

- Model/harness: Claude Opus 5 (1M context), Claude Code CLI, local shell.
- Date: 2026-08-05, America/Chicago. Start 22:20 CDT.
- Branch: `attempt/2026-08-05-claude-opus-5-064c` (suffix generated from
  `/dev/urandom` before branch creation), cut from mirror `origin/main`
  = `9b01be1`, whose tree equals public `main` `64eb3da`.
- Clone: `~/conj40v2/conj40-attack-s2e-claude` from `~/conj40-mirror.git`,
  all branches fetched.
- Declared soft time budget: **180 minutes** (soft deadline 01:20 CDT), with the
  v4 rule that at wrap-up only jobs projected to finish within 15 minutes are
  carried to completion.
- Constraint honoured: local commits only. Nothing pushed; no PR, tag, release
  or public post. Read-only network use only (freshness checks).
- Primary target: SAFE-2-EXISTS, sole and mandatory. No secondary target opened.

## Protocol provenance — one discrepancy, stated and not resolved by me

The activation instruction says to follow **ATTACK.md v6**. No `ATTACK.md` v5 or
v6 exists in the mirror, on any of its 24 branches, anywhere on this machine, or
on the public repository: the newest is **v4**, and public `main`
(`64eb3da`, 2026-08-05T16:35:01Z) carries v4. Likewise `attempts/LESSONS.md` on
`main` ends at the maintenance-reconciliation entry — it contains **no verify4
entry and no 9d2b entry**. I therefore followed v4, which is the freshest
protocol that exists, and treated the operator's activation message as the
binding delta on top of it. The substantive content the message attributes to v6
is corroborated by checked-in records I read directly:

- `~/conj40v2/conj40-attack-safe-exists-20260805-9d2b/ATTEMPT_REPORT.md`
  (universal B-PLUS-2 clean through n=12; B-TERMINAL-SLIDE and unrestricted
  SUCCESSOR-ONE FALSIFIED at n=12; SD-2STEP-DESCENT surviving;
  HARD-SUCCESSOR-ONE as the conjectural lead; the 170 `(2,1)` mechanism records).
- `~/conj40v2/verify4-package/VERIFY4_REPORT.md`, verdict **CERTIFIED**, whose
  scope is stated in its own first line as *"the mathematical derivations of NC,
  NCM/CE, and A-I⁺"* — machinery for Lemma A, not a written closure of Lemma A°
  itself. I used it at that scope: Lemma A is assumed available where I say so,
  and every result below that does not name it is independent of it.

Nothing else in the activation message was down-graded or re-interpreted.

## Step 0 — freshness (all four items, network available)

1. **Repository issues/PRs.** The clone's only remote is the local mirror, so I
   queried the public repository named in the MathOverflow post,
   `github.com/cozuya/wowii-conjecture-40`: 5 issues and 5 pull requests, **all
   closed/merged**; **0 open**. `main` head `64eb3dacd3e332b9464faece8bd42f72e16bf6dc`
   at 2026-08-05T16:35:01Z (merge of PR #5), tree-identical to the mirror `main`
   I branched from.
2. **MathOverflow 513887** ("Can the forced edges of an exact-demand capacitated
   selection in a bipartite incidence model form a cycle, given hereditary FVS
   tightness?"): asked 2 days ago, 17 views, **`answerCount = 0`**, not closed,
   no answer text present.
3. **Maintained WOWII page.** `cms.uhd.edu` refuses TLS; the live mirror
   `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/open.html` fetched
   over plain HTTP (200, 334,470 bytes). Conjecture 40 is present on the **open**
   list with status letter **`O`**, statement
   `f(G) ≥ CEIL[(p(G)+b(G)+1)/2]`; it does **not** appear on `resolvedT.htm`.
4. **Web/arXiv.** Searches for 2026 work on WOWII/Graffiti.pc Conjecture 40,
   Lemma A and SAFE-EXISTS returned only unrelated resolutions (Graffiti.pc 2,
   141–143, WOWII 103). Nothing resolves Conjecture 40 or either lemma.

The primary target did not change.

*Tooling note for the next run:* `WebFetch` force-upgrades HTTP to HTTPS and
cannot reach the WOWII host or mathoverflow.net; `curl` reaches both.

## Step 0.5 — binding prior knowledge

Read in full: `attempts/LESSONS.md` on `main` (all entries), and the attempt
reports for `5047`, `a7c3`, `0eb8`, `4d7a`, `b17e` and `9d2b`, plus
`PREREG-SAFE-EXISTS.md`, `proofs/FROZEN-BPLUS2.md`, `LEMMA-A-CARRIER.md`,
`verify4-package/{STATEMENT,VERIFY4_REPORT}.md` and paper §3–§4.

Treated as binding and **not** rebuilt on: SD-SHORT / SD-COUNT-SHORT
(FALSIFIED), B-TERMINAL-SLIDE (FALSIFIED at n=12), unrestricted SUCCESSOR-ONE
(FALSIFIED at n=12), shortest-path-only Lemma B, SV/LIFT-P, the
class-size/full-side lifting thresholds, and the `B_s`/`P`/`T_F` universal
localizations for Lemma A. Nothing I claim below re-attacks any of them.

## Step 1 — gauntlet

`GAUNTLET.md` written on this branch: the Theorem 3.13 reduction chain with each
lemma's exact role; the abstract even-cycle system and why Hall feasibility
alone cannot yield Lemma A; O-56 / O-63 / O-64 with the exact mechanism each
one kills; and the `T_F` normalization with proof and its limits.
Outcome: **COMPLETED**. Inherited manifest `tools/SHA256SUMS.txt`: **17/17 OK**
(`work/064c/logs/manifest.txt`).

## Angle chosen, and why

Angle (a) of the activation message: attack SAFE-2-EXISTS on hard states,
importing the certified Lemma-A machinery. Justification: both cores run on
hereditary FVS tightness, and the entire certified stack (A-I, carriers, the
`ρ`-tight lattice, F1) had only ever been pointed at the forced core. The first
thing I checked was whether the Lemma-A subcase arguments survive verbatim when
"forced-core cycle" is replaced by "selected cycle" — they do (Theorem 3 below),
and that transfer is what generates the rest. I did not open angle (b) or (c).

## Results

All statements, proofs and the exact open obligation are in
`PROOFS-SAFE2-064c.md` on this branch; preregistration in
`PREREG-SAFE2-064c.md`; checkers and outputs in `work/064c/`.

### Verification instrument (independent)

`work/064c/s2e_scan.py` (sha256 `ab362300…`) is a fresh engine — own graph6
reader, own minimum-FVS enumeration, own feasible-selection enumeration, own
residual-digraph BFS with full shortest-path enumeration, semantic CES test by
selected-cycle-set comparison. It imports nothing from `tools/`. Its anchors
against the record, reproduced independently:

| anchor | recorded | this engine |
|---|---|---|
| connected bipartite graphs, n=9 (`geng -bc`) | 730 | 730 |
| cycle components, n=8 | 2,584 | 2,584 |
| cycle components, n=9 | 24,195 | 24,195 |
| A1 failures, n=9 | 0 | 0 |
| cycle components, n=11 | 8,202,633 | **8,202,633** |
| A1 failures, n=11 | 6 | **6** |

`work/064c/s2e_scan11.py` (sha256 `ab97a2eb…`) is the fast pass for n ≥ 11; it
uses Theorem 2 only as a *filter* and hands every unfiltered cycle to the same
full machinery, so the n=11 anchor above is itself a test of the filter.

### PROVED (with derivations in `PROOFS-SAFE2-064c.md`)

1. **Theorem 1 (LENGTH-ONE-CES).** Every residual augmenting step of length one
   out of a selected cycle is CES, and removes exactly that cycle. *Mechanism:*
   the terminal of a length-one path is slack, every `H`-vertex of a selected
   cycle is saturated, so the terminal lies outside the cycle and the toggle
   joins two distinct components. The CES obligation on length-one steps is
   therefore vacuous — it never has to be checked or proved again.
2. **Theorem 2 (A1-GOOD ⟺ SLACK-ADJACENCY).** `d₀(C) = 1` iff some `S`-vertex
   of `C` has a slack `G`-neighbour. Hence a cycle with a slack-adjacent
   `S`-vertex is A1-good, every A1-bad cycle has `d₀ ≥ 3`, and in a hard state
   *every* `H`-neighbour of *every* cycle `S`-vertex is saturated. A1-goodness
   becomes a one-line local predicate with no residual search.
3. **Theorem 3 (A-I transferred).** For every feasible selection and every
   selected cycle `C`, `N_H(P(C)) ⊋ Q(C)`. The proof of paper Lemma 4.2 (A-I)
   applies verbatim to selected cycles: it uses only that `P(C)` lies in one
   bipartition class and has no `H`-neighbour off the cycle. This is the first
   transfer of the certified Lemma-A stack onto the Lemma-B side.
4. **Theorem 4 (bad-step structure).** For an A1-bad `C` with `d₀(C)=3` and a
   non-CES minimizing step whose terminal is not the released end: the first hop
   leaves the cycle, the component it enters is a path, exactly one new cycle
   `Z` is created, `Z` is vertex-disjoint from `C`, the cycle count is unchanged,
   and the released `H`-end of `C` becomes the new slack vertex. Theorem 4′
   settles the remaining terminal-at-the-released-end case: it either strictly
   *decreases* the cycle count or has its first hop on the cycle.
5. **Proposition 5.** The descent consumes only a strict decrease of the cycle
   count, not CES; so **SAFE-2-DEC** (defined in the proofs file), strictly
   weaker than SAFE-2-EXISTS, already implies F2. Theorem 4′(i) exhibits non-CES
   steps that are count-decreasing, so the gap between the two is real.
6. **Theorem 6 (slack-free closure).** If the residual closure `A*` of a
   selected cycle's `S`-side reaches no slack `H`-vertex, then `A*` is
   `ρ`-tight, `|N_H(A*)| ≥ |A*|+1`, the set `W = N_H(A*) \ Y*` is nonempty, and
   **every** `A*`–`W` incidence is forced. The proof needs the bipartite parity
   fact that `x` and `y` — the only capacity-1 vertices — lie in different
   classes while `N_H(A*)` lies in one, so at most one of them can be reached.
   **Corollary 6.1** (assuming Lemma A): at every selected cycle, either the
   closure reaches genuine slack, or some closure vertex is adjacent to a cycle
   vertex without selecting it.
7. **Theorem 7 (target restated).** HARD-SUCCESSOR-ONE is *equivalent* to:
   after the step, some `S`-vertex on a selected cycle of the successor has a
   slack neighbour. Both the "length one" and the "CES" clauses of the recorded
   lead are discharged by Theorems 1 and 2.
8. **Theorem 8 + Corollary 8.1.** After a bad minimizing step of Theorem 4 the
   new cycle satisfies `d₀(Z) ≤ 3` in the successor, via the explicit path
   `s₁ → h₁ → s → h`; hence `d₀(Z) ∈ {1,3}`. **Remark 8.2:** both toggles along
   that explicit path re-create `C`, so neither is CES — the canonical return
   path cannot discharge the length-3 branch.
9. **Theorem 10 (exact equivalence).** At a hard state, SAFE-2-EXISTS ⟺ CL-6 ⟺
   *some non-increasing minimizing step leaves the hard set*. So the target is a
   statement about one finite digraph on hard states: no hard state may have all
   its non-increasing minimizing out-arcs land inside the hard set.
   **Corollary 10.1:** the weaker HARD-ESCAPE (leave the hard set in finitely
   many non-increasing steps) already gives F2.
10. **Proposition 9 (conditional falsification of the universal form).** If a
    hard state admits a minimizing step of type II(ii) — terminal at the
    released end with the first hop landing back on the cycle — then the
    successor has no length-one step at all and CL-7 fails. The slack set does
    not move at such a step. This converts "is the universal successor form
    true?" into a finite local pattern search, specified in Remark 9.1.
11. **Proposition 11 (no free lunch).** If `μ = min_J c(J) ≥ 1` then every
    `c = μ` selection is hard and CL-6, HARD-ESCAPE, SAFE-2-DEC and
    SAFE-2-EXISTS all fail there. Hence every statement in this family is at
    least as strong as F2 and false exactly when F2 is false; no proof of any of
    them can avoid consuming hereditary FVS tightness. This is the structural
    reason SD-SHORT, B-TERMINAL-SLIDE and SUCCESSOR-ONE all died, and it is the
    test a new candidate should pass before it is scanned: *where does it use
    hereditary tightness?*
12. **Corollary 5.2 / Remark 5.3.** A type-II(i) step (terminal at the released
    end, first hop onto *another* selected cycle) strictly lowers the cycle
    count, so SAFE-2-DEC is discharged there in one move. And the whole `(2,1)`
    population — where B-TERMINAL-SLIDE and unrestricted SUCCESSOR-ONE were
    falsified at n=12 — has an A1-good cycle by definition, so Theorems 1–2
    settle it in a single length-one CES step: those recorded counterexamples
    refute obligations that SAFE-2-EXISTS never needed.

### COMPUTATIONALLY VERIFIED

- **CL-1..CL-5, CL-8 (the six proved claims, as graded predicates):
  exhaustive n ≤ 10** — every connected bipartite graph, every minimum FVS with
  `|S| ≥ 1`, every `H`-edge, every feasible selection: n=8 (159 graphs / 3,609
  instances / 25,114 selections / 2,584 cycle components), n=9 (683 / 17,797 /
  237,671 / 24,195), n=10 (3,926 / 134,851 / 3,515,290 / 448,577). **0 failures**
  on every claim. CL-5 (the one-sided forest–Hall bound) was graded
  exhaustively over all one-class `X ⊆ S` and all `Y ⊆ H` at n ≤ 9.
- **CL-1, CL-2, CL-3, CL-6, CL-7: exhaustive n = 11** — 25,363 graphs with
  `τ ≥ 1`, 1,061,745 instances, 59,954,062 feasible selections, **8,202,633
  cycle components**, **6 A1-failing cycles**, **6 hard states**, 20 minimizing
  steps out of hard states. **0 failures.** In particular CL-7 (the *universal*
  successor form) holds at n=11: every one of the 20 steps yields a successor
  with a slack-adjacent cycle `S`-vertex, i.e. `d₀(Z)=1`.
- **Theorem 6 is not vacuous:** at n=9 its premise (slack-free closure of a
  selected cycle) fires on 32 of the 24,195 cycle components, always with
  `|W| = 1`, and all four conclusions plus Corollary 6.1 hold every time.
- **n = 12:** a checkpointed, restart-safe exhaustive pass over contiguous
  `geng -bc -q 12` index intervals was launched at 22:53 CDT. Coverage and
  verdict are recorded in the "n=12 status" section below.

### CONJECTURAL (the target itself)

**CL-6 / HARD-SUCCESSOR-ONE, in the reduced form of Theorem 7.** Not proved.
The reduction is now sharp: by Theorems 4 and 8 the whole question at a hard
state is whether the relocated cycle `Z` — which lives inside a former *path*
component — has an `S`-vertex adjacent to the newly freed slack vertex `h`,
which lives on the former *cycle*. Theorem 3 gives an `S`-vertex of `Z` with a
neighbour off `Q(Z)`, but not a slack one. Closing that needs a
hereditary-tightness argument that sees the old cycle and the old path component
simultaneously; nothing in the certified stack does that yet.

## Dead ends hit, with reasons

- **The closure-counting route to Lemma A does not close.** Theorem 6 proves
  `A*` tight and forces the `A*`–`W` incidences, and the counting closes
  completely when `W = ∅` — but `W ≠ ∅` is exactly what the same counting then
  proves. Pushing `|D|` below `|A*|` requires sparing two `W`-vertices, and the
  `H`-forest can reconnect two spared vertices. This is the O-56/O-63/O-64
  obstruction reached from a new direction. Recorded so the next attempt does
  not re-walk it.
- **The canonical return path is not a repair.** Remark 8.2: the length-3 path
  that Theorem 8 constructs at the successor always re-creates the destroyed
  cycle, so it is never CES. Any proof of the length-3 branch must produce a
  *different* minimizing step.
- **Theorem 4 does not extend verbatim to terminals at the released end.** My
  first form of the bad-step structure claimed `h₁ ∉ V(C)` unconditionally; the
  case `h₂ = h` refutes that shape of the argument, and Theorem 4′ is what
  survives. The `h₂ = h` case did not occur among A1-bad cycles at n ≤ 11, so
  the finite data would not have caught the over-claim — the case analysis did.

## Tooling defects caught before use

- The n≥11 fast pass first graded CL-3 on *every* non-CES minimizing path,
  including paths belonging to cycles that are A1-**good**; CL-3 is stated only
  for A1-bad cycles. This produced 58,468 spurious "failures" at n=11. The
  defect was found by inspection of the failure records before any verdict was
  read, the scoping was repaired, the checker was re-hashed and the run redone.
  The v1 outputs are retained as `results/n11-s*-v1-cl3misscoped.json` and are
  excluded from every verdict.
- The abort path wrote an `int` into the failure dictionary and crashed the
  summary; fixed before the long runs.

## n=12 status

See "n=12 coverage" at the end of this report (written at wrap-up).

## Recommended next angle

1. **Prove the length-3 branch of Corollary 8.1**, i.e. that at the successor
   `J₀` some minimizing step other than the two return toggles is CES. By
   Remark 8.2 the target is now a single, fully specified configuration: old
   cycle `C`, old path component `K ⊇ Z`, the freed vertex `h ∈ Q(C)`, and the
   bridge `h₁` with `(s,h₁) ∈ J₀`, `(s₁,h₁) ∈ J`. Everything is explicit; what
   is missing is one application of hereditary tightness to a set that meets
   both `P(C)` and `P(Z)`. The natural candidate is `X = P(C) ∪ P(Z)`, which is
   independent and lies in one bipartition class (proof in
   `PROOFS-SAFE2-064c.md` §7) — the FVS to build against it is the open step.
2. **Retarget SAFE-2-DEC instead of SAFE-2-EXISTS** (Proposition 5). It is what
   F2 consumes, it is strictly weaker, and Theorem 4′(i) already supplies
   count-decreasing non-CES steps that SAFE-2-EXISTS cannot use.
3. Do **not** re-verify the CES status of length-one steps, and do not
   formulate any new statement whose content is "some length-one step is CES":
   Theorem 1 makes that a tautology.

## LESSONS FOR FUTURE ATTEMPTS

- [MATHEMATICALLY PROVED] Every residual augmenting step of length one out of a selected cycle is automatically CES: the terminal of a length-one path is slack, every `H`-vertex of a selected cycle is saturated, so the terminal lies off the cycle and the toggle merges two distinct components; the CES clause of any "length-one" statement (including HARD-SUCCESSOR-ONE) is vacuous.
- [MATHEMATICALLY PROVED] `d₀(C) = 1` iff some `S`-vertex of the selected cycle `C` has a slack `G`-neighbour; hence every A1-bad cycle has `d₀ ≥ 3` and, in a hard state, every `H`-neighbour of every cycle `S`-vertex is saturated. A1-goodness is a local predicate — no residual search is needed to isolate the hard population.
- [MATHEMATICALLY PROVED] Paper Lemma 4.2 (A-I) transfers verbatim from forced-core cycles to *selected* cycles: `N_H(P(C)) ⊋ Q(C)` for every selected cycle, because the proof uses only that `P(C)` lies in one bipartition class and has no `H`-neighbour off the cycle. The certified Lemma-A stack is usable on the Lemma-B side.
- [MATHEMATICALLY PROVED] A non-CES minimizing step of length 3 out of an A1-bad cycle whose terminal is not the released end *relocates* the cycle: the new cycle is vertex-disjoint from the old one and lies inside a former path component, the cycle count is unchanged, and the released `H`-end becomes the new slack vertex. This is why one-step mechanisms (SD-SHORT, B-TERMINAL-SLIDE, unrestricted SUCCESSOR-ONE) keep dying.
- [MATHEMATICALLY PROVED] After such a step the relocated cycle `Z` satisfies `d₀(Z) ≤ 3` in the successor, via the explicit path `s₁ → h₁ → s → h`; so `d₀(Z) ∈ {1,3}`. Both toggles along that explicit path re-create the destroyed cycle, so neither is CES: the length-3 branch cannot be discharged by the canonical return path.
- [MATHEMATICALLY PROVED] The descent needs only a strict decrease of the selected-cycle count, not CES; SAFE-2-DEC (a nonincreasing minimizing step followed by a count-decreasing minimizing step) already implies F2 and is strictly weaker than SAFE-2-EXISTS — Theorem 4′(i) exhibits non-CES steps that decrease the count.
- [MATHEMATICALLY PROVED] If the residual closure `A*` of a selected cycle's `S`-side reaches no slack `H`-vertex, then `A*` is `ρ`-tight, `|N_H(A*)| ≥ |A*|+1`, `W = N_H(A*) \ Y*` is nonempty and every `A*`–`W` incidence is forced. The proof uses that `x` and `y` lie in different bipartition classes while `N_H(A*)` lies in one, so at most one capacity-1 vertex is reachable.
- [DEAD END] That closure counting cannot prove Lemma A: it closes only when `W = ∅`, and the same counting proves `W ≠ ∅`. Dropping `|D|` below `|A*|` needs two spared `W`-vertices, and the `H`-forest can reconnect them — the O-56/O-63/O-64 obstruction from a new direction.
- [COMPUTATIONALLY VERIFIED] Independent re-derivation of the recorded anchors with a fresh engine: 2,584 cycle components at n=8, 730 graphs / 24,195 cycle components / 0 A1 failures at n=9, and 8,202,633 cycle components / exactly 6 A1 failures / 6 hard states at n=11 (25,363 graphs with `τ≥1`, 1,061,745 instances, 59,954,062 feasible selections).
- [COMPUTATIONALLY VERIFIED] All six n=11 hard states have exactly one selected cycle, and all 20 minimizing steps out of them land on a successor whose new cycle has a slack-adjacent `S`-vertex (`d₀(Z)=1`), so the *universal* successor form holds at n=11, not just the existential one.
- [TOOLING] Theorem 6's premise is not vacuous: at n=9 it fires on 32 of 24,195 cycle components, always with `|W| = 1`. Report premise-firing counts alongside "0 failures", or a vacuous check reads as a passing one.
- [TOOLING] Scope a claim's checker to the claim's own quantifier: grading the bad-step structure on non-CES paths of A1-*good* cycles produced 58,468 spurious failures at n=11 before the scoping was repaired (v1 outputs retained, excluded from all verdicts).
- [TOOLING] `WebFetch` force-upgrades HTTP to HTTPS and cannot reach the maintained WOWII page (`cms.uhd.edu` refuses TLS; the live mirror is `cms.dt.uh.edu`) or mathoverflow.net; `curl` reaches both. Conjecture 40 is still marked `O` on the open list.
