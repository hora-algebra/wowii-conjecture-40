# Preregistration: conjecture E1 (component excess), census n <= 10

Branch `attempt/2026-08-04-claude-fable-5-0eb8`, 2026-08-04. Frozen BEFORE
any computation of `excess` on any graph other than the seven hand-derived
gold graphs below. Checker: `work/fable-0eb8/e1scan.py`, SHA-256

    11dc5f282ba8aaea84894ce755e231ac2ca3f83f07d52e4dc9803f265b52d0c8

(recorded in `work/fable-0eb8/E1SCAN-SHA256.txt`), committed together with
this file before the census run.

## Statement

**E1 (CONJECTURAL).** Every connected bipartite graph `C` with at least one
edge and color-class sizes `a, b` satisfies

    excess(C) := |a - b| + 2 g(C) - p(C) >= 1,

where `g(C) = FE(C) - max(a,b)` is the full-side forest-extension bonus of
PREREG-L6-N9.md. Equivalently `ell(C) >= 2 (min(a,b) - g(C)) + 1`: the
bipartite Conjecture-40 inequality with `tau(C)` replaced by its L6-Forest
upper bound `min(a,b) - g(C)`. E1 is implied by the bipartite case of
Conjecture 40 on every graph where that upper bound is attained
(`tau = min - g`; measured true on 1,564 of the 1,570 bipartite graphs
`n <= 9`), and is a strictly stronger claim on the rest.

## Why E1 matters (Lemma L7, proved unconditionally; write-up in
ATTEMPT_REPORT.md)

For any minimum OCT `T` of connected nonbipartite `G`, `B = G - T`,
`o = |T|`: since `p(G) <= p(B) + o` and `p(B) = sum_C p(C) + i(B)`,

    [Delta(B) + 2 g(B) - 1] - p(G)
      >= sum_{edge components C} excess(C) - 1 - o.

Hence if E1 holds, the L6 lifting condition (and so LIFT-A) holds at every
`G` possessing a minimum OCT with `c_e(G-T) >= o(G) + 1`. The open
universality question then reduces to graphs whose every minimum OCT leaves
at most `o` edge-containing components (for `o = 1`: exactly one).

## Frozen universe, anchors, controls, decision rules

- Universe: all connected bipartite graphs `2 <= n <= 10`
  (`geng -c -b -q n`); anchor counts 1, 1, 3, 5, 17, 44, 182, 730, 4032
  (A005142).
- Gold (hand-derived, run pre-freeze, ALL PASS): K2 excess 1; C4 excess 1;
  C6 excess 3; P4 excess 3; K_{1,3} excess 2; K_{2,3} excess 2;
  K_{3,3} excess 1.
- CTRL-E1-PLUS-1: the strengthening `excess >= 2` must fail on >= 1 graph
  (K2 and C4 are hand-checked failures of it).
- Census mismatch or gold failure -> run FAILS. E1 failures are DATA:
  every witness recorded with `(graph6, a, b, p, g, excess)`; they refute
  E1 and localize exactly where the L6 route needs more than the full-side
  bound. The excess histogram is reported descriptively either way.
