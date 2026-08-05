# Replay checker repair

The first execution of `safe_witness_replay.py`, frozen at sha256
`78eceaa7e1411016868973f129f2ad0bc835e17f190fd0495b511791560bdcc7`,
returned 118 invalid validations before grading those records.  The mismatch was
localized to the `feasible` control: committed certificates normalize each
undirected edge as `(min,max)`, while `feasible()` represents an incidence as
`(S,H)`.  The raw frozensets therefore differ whenever an S label exceeds its H
label, although they encode the same selection.

The v2 repair normalizes every generated feasible selection before membership
comparison.  No mathematical predicate, source record, enumeration scope, or
decision rule changed.  The invalid v1 output is retained as
`work/9d2b/results/safe-witness-replay-v1-invalid.json` and is excluded from all
verdicts.  The repaired checker is re-hashed and committed before rerun.
