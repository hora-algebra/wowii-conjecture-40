# Preregistration: SAFE-EXISTS successor audit and universal B-PLUS-2 continuation

Frozen before the checker is run for mathematical data.  The checker and this
file will be committed, and the checker hash recorded in `work/9d2b/SHA256.txt`,
before the gold tests and the n=12 run.

## 0. Provenance and discovery status

The binding starting data are not independent of one another.

- `SD-SHORT` and `SD-COUNT-SHORT` are **FALSIFIED**: six failures at n=11 and
  1,184 failures at n=12.  Thus a greedy one-step rule, even after choosing the
  cycle, is not a live target.
- The independent VERIFY-2 engine exhaustively reproduces at n<=11 the six A1
  failures, the 20/20 successful one-lookahead paths, and zero universal
  `B-PLUS-2` failures.  It explicitly marks the n=12 claims `NOT CHECKED`.
- The 4d7a engine prospectively and exhaustively reports zero
  `SD-2STEP-DESCENT` and `SD-PLUS-2` failures among 1,380 A1-failing n=12 cycle
  instances.  That is the source of the prospective n=12 evidence.
- The observations that all checked bad successors have distance one and that
  terminal slides repair the n=11 failures were formulated after inspecting
  discovery data.  Any result for the new successor-distance claims below is
  therefore a **post-hoc mechanism audit**, not a fresh prospective test.

The phrase "n=12 prospective survival on the verify branch" is retained only
as a user-supplied pointer to binding input.  The checked-in provenance is the
more precise split above; no causality or fault is assigned for the mismatch.

## 1. Setting

Use the incidence-selection definitions of `proofs/FROZEN-BPLUS2.md`.  For a
feasible selection J and a selected cycle C, release an avoidable selected
incidence a of C and let d0(C,J) be the minimum residual augmenting-path length.
A toggle is CES when it destroys C and creates no selected cycle absent from J.
Write c(J) for the number of selected cycle components.

An **A1-bad first step** is a toggle J -> J0 along a residual path of length
d0(C,J) that is not CES for C.  All minimizing paths for all minimizing released
incidences are quantified over; hitting the frozen path cap invalidates a clean
universal verdict.

## 2. Exact claims graded

**SAFE-2-EXISTS.**  For every feasible cyclic J, either J has a CES minimizing
step, or there are an A1-failing selected cycle C and an A1-bad first step
J -> J0 such that c(J0) <= c(J) and J0 has a CES minimizing step.

**SUCCESSOR-ONE-ALL.**  For every A1-bad first step J -> J0, the minimum
residual distance over the selected cycles of J0 is one and J0 has a CES
minimizing step of length one.

**SUCCESSOR-ONE-DESCENT.**  For every A1-failing selected cycle C, some A1-bad
first step J -> J0 has c(J0) <= c(J) and J0 has a CES minimizing step of length
one.

**B-TERMINAL-SLIDE.**  The frozen statement in
`proofs/FROZEN-BPLUS2.md`: every selected cycle either has a CES minimizing step
or one of its bad minimizing paths has a CES two-edge terminal slide.

**B-PLUS-2.**  Every selected cycle has dCES <= d0+2.  A successful terminal
slide is an explicit B-PLUS-2 certificate.  Therefore zero B-TERMINAL-SLIDE
failures verifies B-PLUS-2 on the same finite universe.  A terminal-slide
failure alone does **not** falsify B-PLUS-2; it leaves that cycle unresolved and
requires a generic bounded-path recheck.

## 3. Why SAFE-2-EXISTS is descent-sufficient

This implication is **MATHEMATICALLY PROVED**, conditional on the exact claim.
At a cyclic state, take the first alternative when available; a CES step reduces
c by at least one.  Otherwise take the stated first step to J0.  It does not
increase c, and the stated CES second step reduces c(J0) by at least one.  Hence
every block of at most two steps strictly decreases the nonnegative integer c.
Iteration terminates at an acyclic feasible selection.  This is the weakest
claim graded here that is used as a sufficient core; neither
SUCCESSOR-ONE-ALL nor universal B-PLUS-2 is needed for the implication.

The checker grades the cycle-local `SD-2STEP-DESCENT` condition.  Together with
the already-graded alternative that some cycle is A1-good, zero local failures
is exactly the computational test of SAFE-2-EXISTS.

## 4. Universe and schedule

1. Verify the inherited tool manifest with `shasum -a 256 -c SHA256SUMS.txt`.
2. Freeze and hash `work/9d2b/safe_exists_scan.py`.
3. Gold-test n=9, then exhaustive n=11 in shards.  Required anchors at n=11:
   25,598 connected bipartite graphs, 8,202,633 cycle components, six A1
   failures, zero Lemma-A violations, and zero path-cap hits.  The six failures
   must pass the known one-lookahead and universal B-PLUS-2 checks.
4. Run the real checker exhaustively at n=12, sharded deterministically by the
   index of `geng -bc -q 12` output.  Expected enumeration anchor: 212,780
   connected bipartite graphs.  Aggregate only completed shard JSON files.

The primary n=12 run is a re-grade of a previously exposed universe, not a
sealed holdout.  Its value is scope completion and mechanism discrimination.

## 5. Controls and decision rules

- `--ces=always` must eliminate A1 failures on a small universe.
- `--ces=never` must make every cycle component A1-failing on a small universe;
  it is only a mutation control, not mathematical data.
- A preserved failure is independently re-run from its full graph6/S/e/J/C
  certificate before any `FALSIFIED` label.
- Zero failures with all shards complete and no cap hits earns
  `COMPUTATIONALLY VERIFIED (exhaustive n=12 universe)`, never
  `MATHEMATICALLY PROVED`.
- Any incomplete census at wrap-up is `ABORTED-NO-VERDICT`, with completed
  shards and hashes retained.  Existing results are not silently combined to
  fill a missing shard.
- Failure of SUCCESSOR-ONE-ALL does not refute SAFE-2-EXISTS.  Failure of
  B-TERMINAL-SLIDE does not refute B-PLUS-2.  Failure of a greedy choice does
  not refute an existential choice.

