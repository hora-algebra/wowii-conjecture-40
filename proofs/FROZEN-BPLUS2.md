# FROZEN preregistration — B-PLUS-2 and B-TERMINAL-SLIDE (before n=12 holdout)

Frozen 2026-07-30, after the sealed n=11 holdout FALSIFIED the shortest-only
statements A1/U1 (O-40) and the corrected gap analysis + terminal-slide audit
(O-41, O-42). These replace A1/U1 as the Branch-B statements. n=11 is now
DISCOVERY data for them; n=12 is the fresh sealed holdout.

## Setting
As in FROZEN-A1-U1.md (connected bipartite G, min FVS S, H=G−S forest, fixed
H-edge e, capacitated incidence selection J, selected cycle C, avoidable edge,
residual augmenting path). CES is SEMANTIC: the toggle destroys C and creates no selected
cycle absent from the previous selection (decided by fresh selected-cycle-set comparison);
acyclicity of the quotient multigraph is only an OPTIONAL SUFFICIENT certificate of CES,
NOT the definition. Length = number of edges in the residual
augmenting path (DAG-path convention).
d0(C) = min residual augmenting-path length over avoidable edges of C.
dCES(C) = min length of a CES residual augmenting path over all avoidable edges.

## FROZEN STATEMENT B-PLUS-2 (metric)
For every selected cycle C: dCES(C) <= d0(C) + 2.
(Equivalently: a cycle-erasing residual path exists of length at most d0+2.)

## FROZEN STATEMENT B-TERMINAL-SLIDE (mechanism, existential)
For every selected cycle C there exist a released avoidable edge a=(s,h) and a
globally shortest residual augmenting path Q0 for a such that EITHER
 (1) Q0 is CES; OR
 (2) Q0 admits one valid TWO-EDGE TERMINAL SLIDE on the same released edge a:
   Q+ = (Q0, u, t') with
     - (t,u) the next residual edge of the alternating type (t=Q0's terminal),
     - (u,t') the following residual edge of the opposite type,
     - Q+ simple, t' a residual-capacity H terminal,
     - toggling Q+ feasible,
   and Q+ is CES.
   In state terms the slide is the exchange J+ = J0 − (t,u) + (u,t')
   (S1 (t,u)∈J0, S2 (u,t')∉J0, S7 verified 10/10 on the n=11 witnesses).

## Also observed (n=11 witnesses, NOT frozen as universal — quantifier-audit)
- t' = the freed endpoint h of a in all 10 repairing slides (F3 on the 6 cycles).
- The obstruction is a CROSSING cycle (Q0 destroys C, makes one new cycle
 elsewhere); the slide edge (t,u) is on that crossing cycle and its removal
 reconnects two different components (S5), erasing with no new cycle.
- B-EVEN (gap even) follows from bipartite parity; not a separate conjecture.

## Verification status at freeze
- Exhaustive n<=11: B-ANY (dCES finite) holds; gap distribution exactly
 {0: 8,202,627 ; 2: 6} at n=11; so B-PLUS-2 holds n<=11. The 6 positive-gap
 cycles (k=4, 4-cycles) are all repaired by a terminal slide to h; S1/S2/S5/S7/S8/
 F1 = 10/10, dual-verified with fresh code independent of the discovery engine.
- The shortest-only A1/U1 are FALSE at n=11 (O-40); B-PLUS-2/B-TERMINAL-SLIDE
 survive those exact counterexamples.

## Frozen verifier code (sha256)
- The n=12 checker was written and frozen; its hash is in the "Frozen n=12 checker" section
 below (b_hslide.py 54e13cac...). (The earlier "TBD before launch" placeholder is
 superseded by that completed checker section.)
Shared engine: a1_verify.py (residual DAG), eval_L1_holdout.py, mine_n10.py,
eval_frozen.py, inv_b.py, experiment_b.py.

## Holdout protocol
Open a sealed n=12 run (exhaustive if feasible; else a PREREGISTERED structured
subset: a deterministic sample + a targeted exhaustive k=4 / 4-cycle family +
separate random and adversarial generators + fixed timeout rules; reported as a
structured holdout, not exhaustive verification). For every cycle compute d0,
whether a shortest pair is CES, and (only if not) whether a terminal slide of
length d0+2 is CES; record dCES and gap. Timeouts -> UNKNOWN. Any B-PLUS-2 or
B-TERMINAL-SLIDE failure preserved with full witness. Do NOT inspect partial
output to revise the statements.

## Still OPEN
- Lemma A: every selected cycle has an avoidable edge (no all-R3 cycle). Separate
 R3-cut / hereditary-FVS branch, unaffected by the n=11 failures.
- A PROOF (not verification) of B-PLUS-2 / B-TERMINAL-SLIDE: the local obligation
 is to show a shortest bad path always exposes an edge (t,u) of its crossing
 cycle followed by an admissible (u,t') to SOME residual-capacity terminal t'
 reconnecting distinct components. (The empirical n=11 witnesses all had t' = the
 freed endpoint h — see "Also observed" above — but the general proof obligation
 is stated for a residual-capacity terminal t', not specifically h.)

## Frozen n=12 checker (added 2026-07-30)
- b_hslide.py 54e13cace032de32f73e85e1bdf50614aa083fb9e3543eb74eb389f233aaca10
- a1_verify.py 12d9d843a385c25a0c161f4db2cdbb26196587ae35ff8251b697efd6b0b6bbf9
Regression PASSED: n<=10 all gap-0 (0 failures); the 6 n=11 positive-gap cycles all satisfy B-PLUS-2, B-TERMINAL-SLIDE, B-H-SLIDE (gap=2, slide to freed h). Corrupted-witness sanity: a non-CES slide is correctly rejected by the fresh cycle check.

## n=12 holdout status (added 2026-07-31)
The sealed n=12 run was ABORTED before completion (~49% of graphs processed, then stopped
by decision): NO VERDICT. The frozen statements above and the checker hash (b_hslide.py
54e13cac...) remain reusable for a future holdout (full, targeted-k=4 subset, or n=13). No
frozen theorem quantifier or checker hash was altered by this documentation patch.
