# Preregistration: generic B-PLUS-2 recheck after terminal-slide failure

The repaired, frozen certificate replay returned valid reconstructions for all
170 retained `(2,1)` n=12 cases, with 170 terminal-slide failures.  Under the
predeclared decision rule this does not falsify B-PLUS-2; it triggers a generic
bounded-path recheck.  This file and the new checker are frozen before that
recheck is run.

## Exact checker obligation

For each target A1-failing cycle C, compute its global d0 over all avoidable
selected incidences.  For every avoidable incidence a, enumerate every simple
alternating residual augmenting path after releasing a whose length is at most
d0+2.  Test CES semantically by selected-cycle-set comparison.  The target is
B-PLUS-2-good iff at least one such path is CES.  Terminal-slide geometry is not
assumed.

The residual DFS independently enumerates paths rather than calling the frozen
shortest-path DAG enumerator.  It checks feasibility of each toggled candidate
before accepting it.

## Frozen schedule and anchors

1. Gold replay the six n=11 A1 failures from fixed 4d7a commit
   `5cb5bb9a29718562d4d25a6902fd693f0a4677f4`; expect six B-PLUS-2 successes
   with first CES length five (d0=3).
2. Replay all 170 retained n=12 `(2,1)` certificates.
3. Exhaustively scan multi-cycle n=12 shards 11 and 14 of 32 with the same
   generic predicate.  Expected A1 failures: 38 and 46 respectively.  Their
   union with replay covers all 196 cases exactly as preregistered in
   `PREREG-SAFE-EXISTS-HYBRID.md`.

Zero generic failures, complete anchors, valid feasibility checks and zero caps
earns B-PLUS-2 **COMPUTATIONALLY VERIFIED (exhaustive n=12 universe, composite
census)** when combined with the fixed 4d7a single-cycle coverage.  Any generic
failure must be independently checked before `FALSIFIED`.  Incomplete jobs are
`ABORTED-NO-VERDICT`.

