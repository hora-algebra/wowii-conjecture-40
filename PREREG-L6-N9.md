# Preregistration: L6 forest-extension bonus + prospective n=9 universality scan

Branch `attempt/2026-08-04-claude-fable-5-0eb8`, 2026-08-04. Frozen BEFORE
any n=9 computation of the quantities below. Checker:
`work/fable-0eb8/l6scan.py`, SHA-256

    2e5687400be26728bdea7d7ea167c64811bd1f0e1056caccf96c65f6b693dcd5

(recorded in `work/fable-0eb8/L6SCAN-SHA256.txt`), committed together with
this file before the first `bip9` or `scan9` invocation.

## New lemma frozen here (proof in ATTEMPT_REPORT.md §L6)

For an edge-containing bipartite component `C` with classes `A_C, B_C`:

    FE(C) = max { |W| + |Y| : (W,Z) an ordered pair of the two classes,
                  Y ⊆ Z, C[W u Y] acyclic }
    g(C)  = FE(C) - max(|A_C|,|B_C|)   >= 1,
    g(B)  = sum over edge-components of g(C).

**L6-Forest.** `tau(B) <= M(B) - g(B)` for every finite bipartite `B`.
*Proof.* FE is realized by an induced forest containing one full class; the
union over components plus all isolated vertices is an induced forest of
order `sum_C FE(C) + i(B) = |B| - M(B) + g(B)`; complement. (Also directly:
`tau(C) = |C| - f(C) <= |C| - FE(C) = min_C - g(C)`, and `tau` is additive
over components.) **Status: MATHEMATICALLY PROVED** (trivial once FE is
defined; the content is that `g` is computable structure).

**L6 (lift).** If some minimum OCT `T` of connected nonbipartite `G` has
`p(G) <= Delta(B) + 2 g(B) - 1` (with `B = G - T`), then LIFT-A holds at `G`
with that `T`. *Proof.* `2 tau(B) + o + 1 <= 2M - 2g + o + 1
= n - Delta - 2g + 1 <= n - p = ell`. **Status: MATHEMATICALLY PROVED.**

Relations, proved and asserted per-instance by the checker (INV-DOM):
`g(C) >= 1 + r(C)` (a sparse pair in a smallest class is a 2-element
acyclic `Y`; a single vertex is a 1-element one), hence the L6 threshold
dominates the L5 threshold `2c_e + Delta + 2r - 1` for the same `T`.
A set `Y` qualifies iff the neighbourhood family `{N(y) ∩ W : y in Y}` is
Berge-acyclic (its incidence bipartite graph is a forest), so `g(C)` is the
maximum Berge-acyclic subfamily of the small-side neighbourhood hypergraph —
this is the natural closure of the codex sparse-pair bonus.

## Pre-freeze validation (already run, recorded)

- `gold`: DC{, K3, C5, C7, bowtie, the seven L3 residuals (known `o,p`,
  L3-uncovered, L5-covered), the three SV witnesses at n=11 (`o=1, p=3`,
  unique minimum OCT, exact slack 4). ALL PASS. Data point recorded: on all
  three SV witnesses the L5 margin is 0 and the L6 margin is 4.
- `regress` (n<=8, the codex/audit universe): bipartite 451, T1 failures 0
  (tight 450, minus-1 control fires 450); connected nonbipartite 11,859,
  S1 failures 0, S2 failures 0, S3 failures 0; the false exact+1 control
  fails on exactly 217 graphs = the known count of LIFT-A-tight graphs at
  `3<=n<=8` (matches the v2 paper's cross-tabulation column). ALL PASS.

## Frozen prospective universes and statements

1. `bip9`: all bipartite graphs on 9 vertices (`geng -b -q 9`; anchor count
   1,119 per OEIS A033995).
   - **T1**: `tau(B) <= M(B) - g(B)` — 0 failures required (it is a proved
     theorem; a failure means a checker bug and fails the run).
   - **CTRL-T1-MINUS-1**: `tau <= M - g - 1` must fail on >= 1 graph.
2. `scan9 R 8` for R = 0..7: all connected graphs on 9 vertices
   (`geng -c -q 9 R/8`), restricted to nonbipartite. Anchors: connected
   shard counts must sum to 261,080; nonbipartite to 260,350.
   - **S1 (open question, the point of the run)**: count of graphs with NO
     minimum OCT satisfying the L5 condition
     `p <= 2c_e + Delta + 2r - 1`. Never computed at n=9 by anyone;
     the codex attempt found 0 such graphs at n<=8.
   - **S2**: count of graphs with NO minimum OCT satisfying the L6
     condition `p <= Delta + 2g - 1`. (S2 <= S1 pointwise by INV-DOM.)
   - **S3 (consistency)**: exact LIFT-A (`exists` minimum OCT with
     `ell >= 2 tau(B) + o + 1`) — 0 failures required (known true at n=9
     from the v1/v2 full census; any failure = checker bug, run fails).
   - **TIGHT**: the set of graphs with best exact slack 0 must have
     exactly 2,494 members and equal, as a set, the published
     `verification/v2-lift-census/lift-a-tight-n9.g6`
     (SHA-256 `6078480935bf84787a02b5ee580eb13e039583419929013916379f97c3cd5abc`);
     compared after sorting both lists.
   - **INV-DOM** asserted on every (graph, minimum OCT).

## Frozen decision rules

- Census anchor mismatch, T1 failure, S3 failure, INV-DOM failure, or a
  silent control -> the run FAILS; diagnose, document, re-freeze if code
  changes (codex bit_count precedent: compatibility-only repairs must be
  recorded with old and new hashes).
- S1 = S2 = 0: the L5 and L6 conditions survive n=9; report as
  COMPUTATIONALLY VERIFIED (universe n<=9) universality evidence; the
  general question stays OPEN. Follow-up (not frozen): structured probes at
  n>=10.
- S1 > 0, S2 = 0: the codex sparse-pair bonus is insufficient at n=9 but
  the Berge-acyclic closure L6 still covers; witnesses become the exact
  target shapes for generalizing the proof. Report witnesses.
- S2 > 0: both conditions fail existentially at n=9; the witnesses are the
  first known graphs beyond every full-side forest-extension bound; against
  S3=0 they still satisfy exact LIFT-A, so the gap
  `f(C) - FE(C)` per component is load-bearing there. Report witnesses and
  their per-OCT profiles.
- Witness structure analysis performed after seeing the data is labeled
  IN-SAMPLE.

## Runtime expectation (measured basis, not a promise)

Measured 15.7 s for the full n<=8 regression (~12k connected + 451
bipartite graphs). n=9 is ~261k connected graphs with ~4x per-graph cost;
expected order 30-90 min single-core, sharded 8 ways.
