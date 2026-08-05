# Preregistration: carrier-containment poset and adjacent maxima

Branch `attempt/2026-08-05-codex-gpt-5-b17e`, 2026-08-05. This file is
written before running the new checker on its target universe.

## Primary target and status before the run

The sole primary target is ATTACK.md Step 3 target 1: Lemma A on
`T_F`-normalized instances via canonical carriers, punctures, and the
augmented forest quotient. No LIFT threshold is proposed or tested.

Let a feasible abstract incidence system have a forced-core cycle `F`, with
cycle sides `P subseteq S` and `Q subseteq H`. For `s in P`, let `A_s` be the
unique minimum Hall-tight set containing `s`, put `B_s=A_s\{s}`, and put
`U=union_(s in P) B_s`.

### CP (carrier-poset lemma)

For distinct `s,t in P`, if `t in B_s`, then `A_t` is a proper subset of
`A_s`. Consequently the digraph on `P` with arc `s -> t` iff `t in B_s` is
acyclic, the carriers `{A_s:s in P}` are pairwise distinct, and

    P\U = {t in P : A_t is inclusion-maximal among the cycle carriers}.

In particular `P\U` is nonempty. Status before scan: proposed
MATHEMATICALLY PROVED sublemma, not Lean-formalized. Proof to be written up
only after oracle contact: `B_s` is tight by punctured tightness and contains
`t`; canonical minimality gives `A_t subseteq B_s`, and
`B_s` is a proper subset of `A_s`.

### ADJ (adjacent-maxima lead)

The cycle contains two consecutive vertices from `P\U`. Equivalently, two
inclusion-maximal cycle carriers occur consecutively around `F`. If true,
Lemma CS(b) yields a shared `q in Q` with `deg_U(q)=0` without assuming the
known-false global condition `P intersect U = empty`.

Status before scan: CONJECTURAL. It will not be used as a premise unless it
survives the scan; a single exact failure falsifies it.

## Frozen target universe

The prospective exhaustive universe is exactly
`carrier.gen_exhaustive(maxK=3,maxP=5)` from the checked-in
`work/carrier.py`: abstract systems with `2<=|S|<=3`, `3<=|H|<=5`, every
`S`-vertex having 2, 3, or 4 `H`-neighbours (bounded by `|H|`), every `H`
vertex incident, and either all capacities two or one capacity-one pair.
Only feasible systems with a cyclic forced core enter the CP/ADJ verdict.

Published anchors from the prior carrier run must reproduce exactly:

- 115,774 abstract systems scanned;
- 798 systems with a cyclic forced core;
- 18 cyclic systems with `P intersect U != empty` (the known-false PDIS
  companion fires).

Frozen after the control-only pass and before the target scan:

    7fe9f98569bb4bebb980b69dbb734993b82f4d5c499ad1efa3dab90a2f4d7222  work/b17e/carrier_poset.py
    d11b0bca3a4ac437b4811ce588e660fe2e382ccd725e017fbadd2919e195696a  work/carrier.py

The control-only invocation detected one forced cycle and passed CP on each of
O-56/O-63/O-64. The negative PDIS control fired on a three-vertex cyclic
system with `P\U={s2}`. No target counts or CP/ADJ verdicts were produced by
that mode.

## Controls required before target execution

Positive controls: O-56, O-63, and O-64 must each be parsed as a feasible
system with a cyclic forced core; CP must hold; and their recorded
`P intersect U = empty` profile must reproduce. This exercises cycle finding,
tight-set enumeration, carriers, punctures, and the CP predicates.

Negative control: the checker must locate a system in the already published
exhaustive universe with `P intersect U != empty`, thereby firing the false
companion PDIS. This prevents a vacuous implementation that always computes
`U` disjoint from `P`. The target run must reproduce the published count 18.

## Frozen decisions

- Any CP failure: do not claim the proof; preserve the first certificate and
  label CP FALSIFIED or ABORTED-NO-VERDICT according to independent checking.
- CP has zero failures with all anchors/controls passing: label CP
  MATHEMATICALLY PROVED only if the written proof remains valid, and separately
  COMPUTATIONALLY VERIFIED on the stated universe.
- Any ADJ failure: preserve and independently re-check the first certificate;
  label ADJ FALSIFIED. Do not attempt to rescue it by adding an in-sample
  condition during this run.
- ADJ has zero failures with all anchors/controls passing: label only
  COMPUTATIONALLY VERIFIED on this universe and CONJECTURAL in general.
- Any anchor or control mismatch: the entire target scan is
  ABORTED-NO-VERDICT.
