# Hard-state replay repair

The first `hard_successor_replay.py` execution, sha256
`a7e19befa97dac0ec026f044a6835f1700844233a531d4b180f937519c150f64`,
reused the multi-cycle replay validator.  That validator deliberately required
two cycles and `a1_good=1`, so it rejected all 1,140 `(1,0)` records before
mathematical grading.  Its output is retained as
`hard-successor-replay-v1-invalid.json` and excluded from verdicts.

The repaired checker uses the same residual and CES engine but validates the
preregistered hard-state profile: exactly one recorded/actual cycle,
`a1_good=0`, and one recorded A1-bad cycle.  No claim or decision rule changed;
the repaired hash is committed before rerun.
