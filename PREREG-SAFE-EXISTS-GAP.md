# Preregistration amendment: optimized n=12 universal-gap closure

Frozen before `work/9d2b/safe_exists_gap_scan.py` is run for mathematical data.
This amendment changes the execution schedule, not any statement.

## Exact reason the restricted scan is complete for the open gap

The already-completed 4d7a n=12 aggregate has the full A1-bad profile

`(number of cycles, number of A1-good cycles) = (1,0): 1,184; (2,1): 196`,

with no other profile cell, zero `SD-PLUS-2` failures, zero Lemma-A violations,
and zero path-cap hits.  Inspection of its frozen checker shows:

1. Every A1-good cycle is automatically B-PLUS-2-good.
2. On a one-cycle A1-bad selection, its selection-level `SD-PLUS-2` test must
   test that sole cycle.  Thus the 1,184 `(1,0)` cycles are already individually
   certified.
3. Only the A1-bad cycle in each `(2,1)` selection could be skipped after the
   other cycle made the selection-level existential flag true.

Therefore the entire ungraded universal B-PLUS-2 scope consists exactly of the
196 A1-bad cycles in multi-cycle selections.  The optimized checker enumerates
the whole n=12 graph/minimum-FVS/fixed-edge/feasible-selection universe, discards
only selections with fewer than two selected cycles before residual analysis,
and grades every cycle in every retained selection.  It does not rely on the
capped saved-witness list.

The expected anchors, fixed from 4d7a before this scan, are 212,780 connected
bipartite graphs, 5,912,277 retained multi-cycle selections, 11,824,554 retained
cycle components, 196 A1-failing cycles, and profile `(2,1):196`.

## Decision rule

- Reproduce the n=11 multi-cycle anchor first: 130,811 retained selections,
  261,622 retained cycles, and zero A1 failures.
- On n=12, all shards, all anchors, zero path caps, and zero terminal-slide
  failures closes the missing universal scope.  Combined with the fixed 4d7a
  one-cycle certificates, label B-TERMINAL-SLIDE and hence B-PLUS-2
  **COMPUTATIONALLY VERIFIED (exhaustive n=12 universe, composite census)**.
- A terminal-slide failure falsifies B-TERMINAL-SLIDE after independent witness
  confirmation, but leaves B-PLUS-2 unresolved pending generic bounded-path
  enumeration.
- SUCCESSOR-ONE and SAFE-2 results from this checker have only the restricted
  196-case multi-cycle scope.  They may supplement, but do not replace, the
  previously completed 1,380-cycle SD-2STEP-DESCENT census.
- Incompletion at wrap-up is `ABORTED-NO-VERDICT`; completed shards remain
  resumable.

