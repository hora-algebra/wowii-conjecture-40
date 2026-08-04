# ATTEMPT REPORT

**Branch:** `attempt/2026-08-04-codex-a7c3`  
**Model / harness:** OpenAI Codex, GPT-5, macOS, Python 3.9.6, nauty `geng`  
**Date:** 2026-08-04  
**Base:** `0617d7a` (`origin/main`, tag `v1.1`)  
**Commit/publish status:** no commits, pushes, PRs, public posts, or release
changes, per the operator's direct instruction.

## Outcome

**MATHEMATICALLY PROVED:** three new structured-class results for the surviving
LIFT-A route.

1. **L3-Forest:** for bipartite `B`, if `M(B)` is the sum of the smaller
   bipartition-class sizes over its edge-containing components and `c_e(B)` is
   their number, then

       tau(B) <= M(B)-c_e(B).

2. **L3:** for a minimum OCT `T`, with `B=G-T` and
   `Delta(B)=|B|-2M(B)`, the condition

       p(G) <= 2c_e(B)+Delta(B)-1

   implies `ell(G)>=2tau(B)+|T|+1`.
3. **L5-Forest/L5:** if `r(B)` counts edge-components in which two vertices in
   a smaller color class have at most one common neighbour, then

       tau(B) <= M(B)-c_e(B)-r(B),

   and the stronger sufficient lifting condition is

       p(G) <= 2c_e(B)+Delta(B)+2r(B)-1.

**COMPUTATIONALLY VERIFIED (regression universe):** L3-Forest and L5-Forest
have zero failures on all 451 bipartite graphs through `n=8`.  L2 covered
11,170 of the 11,859 connected nonbipartite graphs through `n=8`; L3 covers
11,852, adding 682; L5 covers all 11,859, adding the last seven.  No graph
covered by L3 or L5 failed the exact LIFT-A inequality.  This is not a proof
that the L5 condition holds for every graph; LIFT-A and LIFT-A-ALL remain open
in general.

The complete proofs, frozen protocols, hashes, outputs, and scope limitations
are in `LIFT-A-RESIDUAL.md`.

## Step 0 — freshness check

Network access was available.

| source | method | finding |
|---|---|---|
| GitHub issues/PRs | GitHub REST API for `cozuya/wowii-conjecture-40`; local `origin` is a filesystem mirror and cannot identify a GitHub host to `gh` | One open PR, #1, `Lessons: attempt/2026-08-03-claude-opus-5-5047`; no separate open issue.  The PR only propagates prior lessons and does not resolve a mathematical target. |
| MathOverflow 513887 | Stack Exchange API, question plus answer/comment endpoints | 0 answers and 0 comments; no activity after creation. |
| maintained WOWII page | direct HTTP fetch and inspection of Conjecture 40 entry | Status remains `O` (open); no change from the 2004 annotation. |
| arXiv / web | exact arXiv API queries for `Written on the Wall II` + `Conjecture 40`, and `largest induced forest` + `path cover`; exact web searches | Both arXiv queries returned 0 results.  No proof, counterexample, or new work on Conjecture 40 or the open lemmas was found.  The live formal-conjectures documentation still states the conjecture. |

**ABORTED-NO-VERDICT:** GitHub CLI could not query the configured `origin`
directly because it is a local filesystem mirror, not a hosted
URL.  The public repository identity was recovered from MathOverflow and the
GitHub API check completed successfully, so this limitation did not leave the
freshness check incomplete.

Nothing found in Step 0 changed the run's target.

## Step 0.5 — prior attempts and superseding v2 state

The required fetch

    git fetch origin 'refs/heads/attempt/*:refs/remotes/origin/attempt/*'

completed.  The fetched prior attempt is
`origin/attempt/2026-08-03-claude-opus-5-5047` at `47d0c64`.  I read its full
648-line `ATTEMPT_REPORT.md`, the `attempts/LESSONS.md` on main, and the proposed
lessons on `origin/lessons/5047`.  I also read `paper/paper.pdf` directly in
full (all 14 pages), `VERIFY_REPORT.md`, `LEMMA-A-CARRIER.md`, `SV-FALSIFIED.md`, both lifting
preregistrations, `proofs/PROOFS.md`, and the relevant challenge documents.

The initial working directory was the independent verification worktree on
`verify/2026-08-f522`.  A separate fresh attempt worktree already existed on
the exact branch `attempt/2026-08-04-codex-a7c3`.  All writes were made there;
the verification worktree and main branch were not modified.

Binding v2 facts honored in this run:

- **FALSIFIED:** SV, minimally at `n=11`; not attacked or re-verified.
- **FALSIFIED:** LIFT-P; not revived.
- **CONJECTURAL:** LIFT-A and LIFT-A-ALL survive but remain open in general.
- **MATHEMATICALLY PROVED:** prior L1/L2 and Lemma CS.
- **COMPUTATIONALLY VERIFIED:** Lemma A through `n=14` and F2-ALL through
  `n=13`, with VERIFY-1's scope corrections; neither is promoted to a proof.

## Step 1 — comprehension gauntlet

**MATHEMATICALLY PROVED / COMPLETED:** `GAUNTLET.md` gives the four mandatory
derivations in this attempt's own words:

1. the exact Theorem 3.13 chain and the separate role of every hypothesis,
   including why A only supplies B's avoidable-edge premise;
2. the abstract even-cycle computation `rho(X)=2|X|` for every `X`, its unique
   cyclic feasible selection, and the failure `tau=1<|S|`;
3. the mechanisms and killed strategies for O-56, O-63, and O-64; and
4. the complete `T_F` normalization proof, including why forcedness must be
   re-derived through F1 after restriction.

**COMPUTATIONALLY VERIFIED:** before using the oracle,
`tools/SHA256SUMS.txt` passed 17/17 from its declared `tools/` working
directory.  The prior independent `wcheck.py` reproduced all three warning
witnesses.  This also incorporates VERIFY-1's correction: O-56 has eight actual
forced edges, while the JSON metadata's ten-edge `forced_core_edges` list is
wrong; the four-edge forced cycle remains valid.

## Step 3 target attacked

Priority 1: prove LIFT-A or LIFT-A-ALL on the residual class not covered by L2.
No census frontier was extended and no false v2 target was revisited.

### Claim R1 — component-sensitive forest bound

For each edge-containing bipartite component `C`, taking all vertices of its
larger color class and one vertex of its smaller class induces a star plus
isolates.  Summing this construction over components and taking all isolated
vertices proves

    f(B) >= |B|-M(B)+c_e(B),
    tau(B) <= M(B)-c_e(B).

Here

    Delta(B)=i(B)+sum_C |a_C-b_C|=|B|-2M(B).

Substitution into the lifting inequality proves L3 exactly as stated in the
Outcome.

**Status: MATHEMATICALLY PROVED, not Lean-formalized.**

### Claim R2 — L3 strictly extends L2

Graph6 `DC{` has edges `03,04,14,24,34`, `o=1`, and `p=2`.  It is not
Hamilton-traceable because leaves `1,2` would have to be the two endpoints and
would force the segment `1-4-2`, stranding `0,3`; the cover
`1-4-0-3` plus singleton `2` shows `p=2`.  With OCT `{4}`, `B` is edge `03`
plus two isolates, so `c_e=1`, `Delta=2`.  L2's threshold is one and fails;
L3's is three and succeeds.

**Status: MATHEMATICALLY PROVED and COMPUTATIONALLY VERIFIED by the frozen
strictness control.**

### Claim R3 — pair-sparse strengthening

If two vertices `u,v` in a smaller color class of a bipartite component have
at most one common neighbour, then all vertices of the opposite class together
with `u,v` induce a forest: any cycle would have to be a 4-cycle through two
common neighbours.  This gains one vertex beyond R1 in every independently
qualifying component and proves

    tau(B) <= M(B)-c_e(B)-r(B).

The lifting algebra then gives L5.

**Status: MATHEMATICALLY PROVED, not Lean-formalized.**

### Claim R4 — a separate small-OCT forest remainder

If `o<=2` and some minimum OCT leaves a forest, then the required bound is
`ell>=o+1`.  An odd cycle supplies two path edges when `o=1`.  When `o=2`, the
maximum bipartite remainder has an edge, so `n>=4`; a shortest odd cycle, plus
an entering path if it is a triangle, supplies a three-edge path.

**Status: MATHEMATICALLY PROVED, not Lean-formalized.**  L4 is an independent
route for the seven initially observed L3 residuals; L5 later subsumed those
seven at the verified frontier.

## Computational evidence and controls

### Frozen L3 run

Current checker:

    work/lift_residual.py
    sha256 78b7a981b113b627b77fcefff483d3d39b288145748ab0fcad30aadbcc507bb6

The initial source hash was
`6e555454160f6112bd5a51040b03fa266e8f861745e2183392ffac42d94730b5`.
Its first invocation stopped before enumerating one graph because Python 3.9
lacks `int.bit_count`.  Replacing those calls by
`bin(value).count("1")` was a compatibility-only repair; the theorem,
universe, controls, and decisions remained frozen.  The new hash was recorded
before the successful run.

Frozen-universe result:

| check | universe | result |
|---|---:|---:|
| L3-Forest | all bipartite graphs, `2<=n<=8` | 451 graphs, 0 failures, 182 tight |
| false `tau<=M-c_e-1` control | same | fired on 182 cases |
| exact LIFT-A | connected nonbipartite, `3<=n<=8` | 11,859 graphs, 0 failures |
| L2 coverage | same | 11,170 |
| L3 coverage | same | 11,852 |
| new L3-over-L2 | same | 682 |
| L3 residual | same | 7 |
| L3-covered implication failures | same | 0 |

The seven L3 residuals were `F?o}W`, `FCQV_`, `G?BEH{`, ``G?`CVo``,
`G?o}][`, `GCQQVo`, and `GCQSng`.

### L4 regression

    work/lift_residual_l4.py
    sha256 b9c6fba9a9a4ff70fd8a37b3aeb6f91b2499d68b51498996335479a0b413ac1f

**COMPUTATIONALLY VERIFIED, in-sample regression:** L4 applies to 4,606 of
11,859 graphs and all seven L3 residuals; no implication failure.  The false
strengthening `ell>=o+2` fired twice.

### L5 regression

    work/lift_residual_l5.py
    sha256 d2583ebdb17793be93c8af3bb71072912630ba9b05b79e8f396d3ab94784b1bd

| check | universe | result |
|---|---:|---:|
| L5-Forest | all bipartite graphs, `2<=n<=8` | 451 graphs, 0 failures, 356 tight |
| false one-unit strengthening | same | fired on 356 cases |
| L5 coverage | connected nonbipartite, `3<=n<=8` | 11,859 / 11,859 |
| new L5-over-L3 | same | 7 |
| post-L5 residual | same | 0 |
| L5-covered implication failures | same | 0 |

**Scope:** L3/L4/L5 were proved before use; the L3 run was frozen prospectively.
L4 and L5 were formulated after inspecting the L3 residual and their `n<=8`
runs are openly labeled regression rather than holdout evidence.  The proofs,
not the regression counts, support the general structured-class claims.

## Dead ends and incidents

- **ABORTED-NO-VERDICT (tooling only):** the initial L3 checker did not run on
  Python 3.9 because of `int.bit_count`.  It produced no mathematical data;
  the compatibility-only re-freeze is recorded above.
- No mathematical branch ended in a certified dead end.  L3 alone left seven
  graphs, but their structure yielded L4 and then the stronger L5 refinement.
- **UNKNOWN / OPEN:** whether every connected nonbipartite graph has a minimum
  OCT satisfying L5 condition (6).  The zero residual at `n<=8` is not a proof
  and is not presented as one.

## Recommended next attack

The L5 proof exposes a clean dichotomy for each bipartite remainder component.
If a smaller-side pair has codegree at most one, the induced-forest bound gains
a vertex.  If no such pair exists, every two vertices of the smaller side have
at least two common neighbours, an unusually dense codegree condition.

The next highest-information proof attack is therefore:

1. generalize `r(C)` to a multi-vertex bonus: bound the largest same-side set
   `Y` for which all vertices of the opposite class together with `Y` induce a
   forest; and
2. on the complementary pairwise-codegree-at-least-two components, use the
   dense overlap to construct a longer linear forest directly and lower
   `p(G)`.

This is a structural sparse-pair/dense-codegree split aimed at proving the L5
condition, not another routine census.  A prospective `n=9` or structured
`n=11` scan of L5 should be used only to locate the first uncovered shape and
test the resulting exact sublemma.

## Local handoff and propagation

No commit was made, honoring the operator's explicit instruction.  No push,
PR, or public post was attempted.  The proposed lesson entry below therefore
has not been propagated to `attempts/LESSONS.md`; the operator can preserve or
merge it after reviewing the uncommitted diff.

## LESSONS FOR FUTURE ATTEMPTS

- [MATHEMATICALLY PROVED] L3-Forest: for bipartite `B`, `tau(B)<=M(B)-c_e(B)`, where `M` sums the smaller color-class size in each edge component; hence a minimum OCT `T` proves LIFT-A whenever `p(G)<=2c_e(G-T)+Delta(G-T)-1`, with `Delta=|G-T|-2M`.
- [MATHEMATICALLY PROVED] L5-Forest strengthens this to `tau(B)<=M(B)-c_e(B)-r(B)`, where `r` counts components having a smaller-side pair with at most one common neighbour; hence `p(G)<=2c_e+Delta+2r-1` is a sufficient LIFT-A condition.
- [COMPUTATIONALLY VERIFIED] On all 451 bipartite graphs through n=8, L3-Forest and L5-Forest have 0 failures; their false one-unit strengthenings fire on 182 and 356 tight controls, respectively.
- [COMPUTATIONALLY VERIFIED] Among all 11,859 connected nonbipartite graphs through n=8, prior L2 covers 11,170, L3 covers 11,852, and L5 covers all 11,859 with 0 LIFT-A implication failures; this is regression scope, not a proof that L5's condition is universal.
- [MATHEMATICALLY PROVED] L4 independently handles any minimum-OCT forest remainder with `o<=2`: an odd cycle supplies `o+1` linear-forest edges; it covers all seven L3 residuals at n<=8.
- [TOOLING] Frozen checkers/hashes: `lift_residual.py` `78b7a981...`, `lift_residual_l4.py` `b9c6fba9...`, `lift_residual_l5.py` `d2583ebd...`; the first L3 invocation aborted pre-data on Python-3.9 `int.bit_count` and was transparently compatibility-refrozen.
- [CONJECTURAL LEAD] Attack the remaining general class by the L5 dichotomy: a sparse same-side pair yields FVS slack, while absence of such a pair forces pairwise codegree at least two and may yield a direct long-linear-forest/path-cover bound.
