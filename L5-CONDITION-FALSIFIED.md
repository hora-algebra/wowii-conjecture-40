# The L5 (and L6) lifting conditions are not universal — FALSIFIED at n = 11

Branch `attempt/2026-08-04-claude-fable-5-0eb8`, 2026-08-04.

## What is falsified — and what is not

The codex-a7c3 attempt proved (and this branch re-verified, see
`AUDIT-CODEX-A7C3.md`) the sufficient lifting condition

    L5:  some minimum OCT T of G has  p(G) <= 2 c_e(B) + Delta(B) + 2 r(B) - 1
         (B = G - T)  =>  LIFT-A holds at G,

and left open, as its highest-information question, whether the condition's
hypothesis holds for EVERY connected nonbipartite graph ("[CONJECTURAL
LEAD] ... may yield a direct bound"; explicitly "not a proof that the L5
condition is universal"). This branch added the strictly stronger frozen
condition L6 (`p <= Delta + 2 g - 1`, PREREG-L6-N9.md) and asks the same
question of it.

**Both universality statements are FALSE.** There is an 11-vertex graph —
and an infinite family — with a UNIQUE minimum OCT whose remainder defeats
every threshold proved so far (L2, L3, L5, L6), with L4 inapplicable.

**Not falsified:** LIFT-A itself (the witness satisfies it with slack 3),
Conjecture 40 (slack 3), and the L2–L6 lemmas as implications (they are
proved theorems; it is their *hypothesis coverage* that stops here).

## The witness CX11

graph6 `J??FF?^FuE?` (11 vertices, 20 edges):

```
V = {0..10};  classes of B = G - 10:  A = {0,1,2,8,9},  B* = {3,4,5,6,7}
E = {0,1,2} x {6,7}          (left block  K_{3,2})
    u {3,4,5} x {8,9}        (right block K_{3,2})
    u {6,7} x {8,9}          (glue C4)
    u 10 ~ {0, 1, 6, 7}      (apex t := 10)
```

`G - t` is the graph `I??FF?^Fo`: two K_{3,2} blocks glued along a C4 —
balanced 5+5, connected, and **dense on both sides**: every same-side pair
has codegree >= 2 (leaf pairs share both hubs; leaf/opposite-hub pairs share
the two near hubs; hub pairs share >= 2). Hence `r(B) = 0` and `g(B) = 1`.

**Hand-checkable facts** (each also machine-certified, below):

1. *`{t}` is the unique minimum OCT.* `G - t` is bipartite, and `G`
   contains the triangle `t-0-6-t`, so `o = 1`. For any other vertex `v`,
   the remainder `G - v` still contains an odd cycle: `t` keeps a
   neighbour in each class (it has two in each), `G - t - v = C - v` is
   connected (`C` is 2-connected), so `t`'s two cross-class neighbours are
   joined by an odd-length path, closing an odd cycle through `t`.
2. *`p(G) = 2`.* Not traceable: each right leaf `x in {3,4,5}` has
   `N(x) = {8,9}` exactly, and every edge leaving `R = {3,4,5,8,9}` uses a
   slot at `{8,9}`. A Hamilton path gives `8` and `9` at most four path
   edges in total, of which the three right leaves consume
   `6 - (endpoints among {3,4,5}) >= 4`; so no slot remains for a crossing
   edge, `R` is severed from the rest of the path — contradiction. Two
   paths do cover: `2-6-0-t-7-1` and `3-8-4-9-5`.
3. *Every proved threshold fails at the unique OCT.* `B = G - t` is one
   edge-component (`c_e = 1`, `i = 0`), balanced (`Delta = 0`), dense
   (`r = 0`, `g = 1`). Thresholds: L2 `= 2c_e - 1 = 1`; L3
   `= 2c_e + Delta - 1 = 1`; L5 `= 2c_e + Delta + 2r - 1 = 1`; L6
   `= Delta + 2g - 1 = 1`. All `< p = 2`. L4 needs a forest remainder;
   `tau(B) = 2` (two disjoint C4s; and removing `{6,8}` leaves a double
   star). So NO minimum OCT of CX11 satisfies any proved sufficient
   condition.
4. *Exact LIFT-A holds:* `ell = 9 >= 2 tau(B) + o + 1 = 6` (slack 3).
   Conjecture 40 holds: `f = 8, b = 10, p = 2`, `2f - (p+b+1) = 3`.

## The infinite family CX(m)

Left leaves `l_1..l_m ~ {h1,h2}`, right leaves `r_1..r_m ~ {h3,h4}`, glue
`{h1,h2} x {h3,h4}`, apex `t ~ {l_1, l_2, h1, h2}`; `n = 2m + 5`, CX(3) =
CX11. For every `m >= 3` the same arguments give: unique minimum OCT
`{t}`; `B` balanced one-component dense (`r = 0`, `g = 1`, `Delta = 0`,
`c_e = 1`), all thresholds `= 1`; the slot argument at `{8,9}` (unchanged,
since `t` avoids the right block) forces `p >= 2`. So every member defeats
L2/L3/L5/L6, and the failure margin grows: `p(CX(4)) = 3`.
**Status: MATHEMATICALLY PROVED (hand proofs above);**
**COMPUTATIONALLY VERIFIED at m = 3 (n = 11) and m = 4 (n = 13).**

## Machine certificates (three engines)

1. `work/fable-0eb8/verify_cx.py` — asserts every fact W1–W6 by exact
   computation (subset-scan tau, DP path cover, exhaustive minimum-OCT
   enumeration), then re-derives non-traceability, the 2-path cover, and
   OCT uniqueness by definition-level brute force sharing no DP with the
   first pass. ALL PASS.
2. `work/fable-0eb8/l6scan.py` (frozen, SHA-256 `2e568740…`,
   PREREG-L6-N9.md) — its `profile()` reports L5 margin −1, L6 margin −1,
   exact slack 3 on CX11. Agrees.
3. The repository's own frozen second engine
   `verification/phase0_verify2.py` (SHA-256 suite: 237/237 OK):
   `J??FF?^FuE?  f=8 b=10 p=2` and `I??FF?^Fo  f=8 b=10 p=2`. Agrees.

`work/fable-0eb8/cx_family.py` verifies CX(3) and CX(4).

## Provenance, stated plainly

- The route to the witness was the **preregistered, frozen** E1 census
  (PREREG-E1.md, checker SHA-256 `11dc5f28…`): E1 (`excess(C) :=
  |a-b| + 2g(C) - p(C) >= 1` for every connected bipartite `C` with an
  edge) is **FALSIFIED at n = 10 by exactly one graph** among all 5,015
  connected bipartite graphs with `n <= 10` — `I??FF?^Fo`, `excess = 0`
  (histogram: `{0:1, 1:60, 2:574, 3:912, 4:1545, 5:1208, 6:552, 7:146,
  8:16, 9:1}`). By the reduction Lemma L7 (ATTEMPT_REPORT.md), an
  excess-0 component is exactly the enabler a lifting-condition
  counterexample needs.
- The apex attachment was designed BY HAND from that witness
  (**IN-SAMPLE construction**), then certified exactly. The first
  attempted attachment (`t ~ {0,1,2}`, same class) was WRONG — it leaves
  the graph bipartite — and was caught by the verifier; the corrected
  attachment `{0,1,6,7}` is the certified one.
- **Minimal order of failure: 10 or 11, OPEN.** The preregistered
  prospective n = 9 census (PREREG-L6-N9.md; runs recorded in
  `work/fable-0eb8/scan9-out/`) shows S1 = S2 = 0: every connected
  nonbipartite graph with `n <= 9` satisfies the L5 condition (hence L6).
  n = 10 has not been censused for the condition (only for exact LIFT-A,
  which is clean there).

## Consequences for the LIFT-A program

- CX11 is the first known graph outside EVERY proved LIFT-A coverage
  class. Exact LIFT-A holds on it with room; what fails is the
  full-side forest bound: `tau(B) = 2` while `min - g = 4`. The FE route
  (take one whole color class per component) is structurally lossy on
  glued dense blocks — the optimal forest here keeps 3 of 5 vertices from
  ONE side and 5 of 5 from the other by cutting one hub per block
  (`B - {6,8}` is a double star).
- Any universal sufficient condition must therefore either (a) bound
  `tau(B)` by forests taking PARTIAL sides in two or more blocks (e.g.
  hub-deletion bounds in 2-connected dense pieces), or (b) exploit `p(G)`
  upper bounds that see the apex's stitching, or (c) abandon the
  threshold-form and attack `ell >= 2 tau(B) + o + 1` directly on
  unique-OCT graphs. The unique-OCT mechanism here is the same one that
  killed SV at n = 11 — that quantifier keeps dying at singleton OCTs.
