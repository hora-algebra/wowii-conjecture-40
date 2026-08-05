# Preregistration amendment: certificate replay plus two-shard completion

Frozen before any n=12 command in this attempt.  The two-core allocation makes
the 32-shard schedule in `PREREG-SAFE-EXISTS-GAP.md` exceed the declared budget.
This amendment replaces it with an exact, auditable cover of the same 196-case
gap; no mathematical predicate is changed.

Source commit is fixed as 4d7a commit
`5cb5bb9a29718562d4d25a6902fd693f0a4677f4`.  Its 32 committed shard JSON files
record 196 `(2,1)` selections.  Before this preregistration, a mechanical count
showed that their capped full-certificate lists retain 170 of those 196:
all are retained except 14 in shard 11 and 12 in shard 14.  The retained count
equals the profile count separately in every other shard.  Shard 11 retains
24/38 and shard 14 retains 34/46.

The frozen hybrid schedule is:

1. Replay all 170 retained multi-cycle certificates from the fixed git object,
   rechecking graph decoding, minimum-FVS membership, feasibility, the recorded
   A1 failure, every minimizing first step, terminal slides, and successor
   predicates.
2. Exhaustively run the already-frozen gap checker on n=12 shards 11 and 14 of
   32.  These scans grade all 38+46=84 multi-cycle A1 failures in those shards,
   including the 58 retained certificates and the 26 omitted by the caps.

Thus the union has size `170 + 84 - 58 = 196`, with the overlap explicit rather
than silently double-counted.  The fixed aggregate proves there is no other
universal gap.  A clean universal conclusion additionally requires all source
profile/count assertions, replay validations, shard anchors, and path-cap
checks to pass.

Decision rules are unchanged from `PREREG-SAFE-EXISTS-GAP.md`.  A
terminal-slide failure is not a B-PLUS-2 failure.  Any source inconsistency,
failed replay validation, incomplete shard, or unexpected anchor produces
`ABORTED-NO-VERDICT` for the composite universal conclusion.

