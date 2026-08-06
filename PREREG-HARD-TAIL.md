# Preregistration — hard-state cap tails and off-path escape

Frozen before the checker is run.  The 1,140 retained n=12 hard-state records
are exposed discovery data.  The 44 records omitted by the source certificate
caps have not been inspected and form the prospective slice for the mechanism
claim below.

## Provenance and inherited totals

Source commit:
`5cb5bb9a29718562d4d25a6902fd693f0a4677f4`.
Its complete n=12 profile records 1,184 states of type `(1,0)` (one selected
cycle, no A1-good cycle).  The first 50 A1-bad certificates per shard retain
1,140 of them and omit 44 in shards 4, 11, 13, 14, 16, and 25.

The final retained-certificate boundaries, included conservatively in each
tail, are:

| shard | zero-based graph index | graph6 | omitted hard records |
|---:|---:|---|---:|
| 4 | 208036 | `K?ABBAWeF_?}` | 10 |
| 11 | 187883 | `K??FFBw}Fw^_` | 8 |
| 13 | 210349 | `K?ABCqWXCsKl` | 4 |
| 14 | 193230 | `K??Ffbo}Fw^_` | 4 |
| 16 | 207024 | `K?AE@bGMF_?~` | 12 |
| 25 | 209529 | `K?AB?r_F?{[H` | 6 |

The checker must verify each boundary string, enumerate every graph in these
six shard tails, and union state identities with all retained records.  A
complete grade requires exactly 1,184 unique hard states and exactly 44 states
new beyond the retained set.

## Claims graded

**HARD-SUCCESSOR-ONE.**  If a cyclic feasible selection `J` has no A1-good
selected cycle, some A1-bad minimizing first step `J -> J0` satisfies
`c(J0)<=c(J)`, and `J0` has a CES minimizing step of length one.

This remains the inherited conjectural lead.  The tail test only extends its
finite grade; no finite result promotes it to a theorem.

**OFF-PATH-ESCAPE (OPE).**  On a hard state in this n=12 slice:

1. `J` has exactly one selected cycle `C`, `C` is a 4-cycle, and `d0(C,J)=3`;
2. every A1-bad minimizing path `Q` destroys `C` and produces exactly one
   selected cycle `Z`, also a 4-cycle;
3. exactly one selected incidence of `Z` is newly added by `Q`, and exactly
   one `S`-vertex `v` of `Z` is not a vertex of `Q`;
4. releasing one of the two `Z`-incidences at this off-path vertex `v` and
   adding one incidence from `v` along a residual path of length one is CES
   for `Z`.

OPE is stronger than HARD-SUCCESSOR-ONE on this slice because it supplies a
length-one CES successor after every bad minimizing first step.  It was formed
after exploratory inspection of the 1,140 retained records; results on those
records are post-hoc regression only.  Its test on the 44 tail-only records is
prospective.

## Carrier-stack obstruction graded descriptively

For each hard state, record how many selected-cycle incidences lie in the
global forced core.  This is descriptive, not a theorem.  A state with zero
such incidences cannot support a proof that begins by applying carrier/NC/A-I+
directly to an edge or cycle in the forced core.  No conclusion about other,
indirect uses of hereditary tightness is licensed.

## Controls and decision rules

1. Verify `tools/SHA256SUMS.txt` from `tools/` before use.
2. Freeze this file and `work/7851/hard_tail.py`, record its SHA-256, and commit
   before execution.
3. Retained regression under real CES must reproduce: 1,140 unique valid hard
   states, 3,924 bad minimizing first steps, zero HARD-SUCCESSOR-ONE failures,
   and zero OPE failures.
4. `--ces=always` on retained records must yield zero hard states.
5. `--ces=never` on retained records must produce hard states and must fire the
   HSO/OPE failure channels; this is a mutation control, not mathematical data.
6. A boundary mismatch, a nonzero path-cap count, a replay/identity mismatch,
   fewer or more than 44 tail-only states, a union size other than 1,184, or an
   incomplete `geng` stream makes the target **ABORTED-NO-VERDICT**.
7. A preserved HSO or OPE failure must be independently rechecked before a
   `FALSIFIED` label.  Zero failures earns only **COMPUTATIONALLY VERIFIED** on
   the explicit n=12 universe.

