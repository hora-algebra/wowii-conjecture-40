# LIFT-A residual attack: component imbalance and isolated components

Branch `attempt/2026-08-04-codex-a7c3`, 2026-08-04.

This attacks the first ATTACK-2 priority: prove LIFT-A on part of the residual
class not covered by the preceding attempt's L2 theorem.  Nothing here revives
SV or LIFT-P; both are **FALSIFIED** at `n=11` and are not used.

## 1. A sharper constructive forest bound

Let `B` be any finite bipartite graph.  For every edge-containing connected
component `C`, let `(a_C,b_C)` be its two bipartition-class sizes, in either
order.  Define

    c_e(B) = number of edge-containing components,
    i(B)   = number of isolated vertices,
    M(B)   = sum_C min(a_C,b_C),
    Delta(B) = i(B) + sum_C |a_C-b_C|.

The sums indexed by `C` run only over edge-containing components.  Notice

    |B| - 2 M(B) = Delta(B).                                      (1)

> **L3-Forest.** For every finite bipartite graph `B`,
>
>     f(B) >= |B| - M(B) + c_e(B),
>     equivalently tau(B) <= M(B) - c_e(B).                       (2)

**Status: MATHEMATICALLY PROVED; not Lean-formalized.**

**Proof.** In an edge-containing component `C`, take every vertex in the larger
bipartition class and one vertex from the smaller class.  The induced graph is
a star centered at the added vertex, together with isolated vertices from the
larger class that are not adjacent to it, hence is a forest of order
`max(a_C,b_C)+1`.  In an isolated component take its vertex.  The union over
components is an induced forest of order

    i(B) + sum_C (max(a_C,b_C)+1)
      = |B| - sum_C min(a_C,b_C) + c_e(B)
      = |B| - M(B) + c_e(B).

Taking complements gives (2).  No connectedness assumption is used.  QED.

The previous bound L1 was `tau(B)<=floor(|B|/2)-c_e(B)`.  L3-Forest retains
information that L1 discarded: isolated components and imbalance between the
two color classes of each nontrivial component.

## 2. The new lifting class

Let `G` be connected and nonbipartite, and let `T` be a minimum odd-cycle
transversal.  Put `B=G-T`, so `|T|=o(G)` and `B` is bipartite.

> **L3 (component-imbalance lift).** If some minimum OCT `T` satisfies
>
>     p(G) <= 2 c_e(B) + Delta(B) - 1,                            (3)
>
> then LIFT-A holds at `G` with this same `T`:
>
>     ell(G) >= 2 tau(B) + |T| + 1.                              (4)

**Status: MATHEMATICALLY PROVED; not Lean-formalized.**

**Proof.** Write `n=|G|`, `n_B=|B|`, and `o=|T|`, so `n_B=n-o`.  By
L3-Forest and (1),

    2 tau(B)+o+1
      <= 2M(B)-2c_e(B)+o+1
       = n_B-Delta(B)-2c_e(B)+o+1
       = n-Delta(B)-2c_e(B)+1.

Condition (3) gives

    ell(G)=n-p(G) >= n-Delta(B)-2c_e(B)+1,

which proves (4).  QED.

Since `Delta(B)>=0`, L3 contains the prior class
`p(G)<=2c_e(B)-1` (L2).  It is strictly larger.  For graph6 `DC{`, with edges
`03,04,14,24,34`, the triangle `0-3-4-0` gives `o=1`.  Its two leaves `1,2`
force any Hamilton path to have endpoints `1,2`, which would use the segment
`1-4-2` and strand `0,3`; hence `p>=2`, while
`1-4-0-3` plus singleton `2` gives `p=2`.  Taking `T={4}` leaves the edge `03`
and two isolated vertices, so `c_e=1`, `Delta=2`.  L2 requires `p<=1` and does
not apply; L3 permits `p<=3` and does apply.

## 3. Frozen computational test

**Status before execution: FROZEN.**  The following test and decision rules
were written before the checker was first run.  The operator prohibited
commits during the run, so the freeze is local and hash-based rather than
commit-backed.

Checker: `work/lift_residual.py`.

The initial frozen SHA-256 was
`6e555454160f6112bd5a51040b03fa266e8f861745e2183392ffac42d94730b5`.
Its first invocation stopped before enumerating a graph because the local
Python 3.9 runtime lacks `int.bit_count`.  No mathematical output existed.
The compatibility-only repair replaced those calls with
`bin(value).count("1")`; the statement, universe, controls, and decision rules
were unchanged.  The re-frozen SHA-256 is

    78b7a981b113b627b77fcefff483d3d39b288145748ab0fcad30aadbcc507bb6

This current value is recorded in `work/LIFT-RESIDUAL-SHA256.txt`.

### Frozen universe

1. L3-Forest: every unlabeled bipartite graph on `2<=n<=8`, including
   disconnected graphs (`geng -b -q n`).  Required per-order counts are
   `2,3,7,13,35,88,303`, totaling 451.
2. L3 coverage: every connected graph on `3<=n<=8`, restricted to the
   nonbipartite graphs.  Required connected counts are
   `2,6,21,112,853,11117`; required nonbipartite total is 11,859.
3. Every minimum OCT is enumerated.  `p(G)`, `tau(G-T)`, component color-class
   sizes, L2 coverage, L3 coverage, and exact LIFT-A slack are computed from
   definitions.

### Frozen outputs and decision rules

The run reports:

- failures and tight cases of (2) on the bipartite universe;
- L2-covered, L3-covered, newly covered, and post-L3 residual counts;
- the universal-over-minimum-OCT L3 count as descriptive data only;
- representative newly covered and still-residual graph6 records; and
- the profile `(p-best_L3_threshold, Delta, c_e)` of the remaining residual.

Any violation of L3-Forest, any L3-covered graph failing LIFT-A, or any census
mismatch makes the run fail.  The negative control is the deliberately false
one-unit strengthening `tau(B)<=M(B)-c_e(B)-1`, which must fail.  The strictness
control is `DC{`, which must fail L2 and pass L3 with `p=2`.

## 4. Post-run result

**Status: COMPUTATIONALLY VERIFIED** on the frozen universe.  The current
checker hash passed before execution.  Results:

- L3-Forest: 451/451 bipartite graphs checked, 0 failures, 182 tight.  The
  false one-unit strengthening failed on all 182 tight cases, so the negative
  control fired.
- LIFT-A remained clean on all 11,859 connected nonbipartite graphs through
  `n=8` (0 exact failures).
- L2 covered 11,170 graphs.  L3 covered 11,852, including **682 graphs not
  covered by L2**.  No L3-covered graph failed LIFT-A.
- L3 held for every minimum OCT on 11,783 graphs (descriptive universal count).
- Only 7 graphs remained outside L3.  Five had residual profile
  `(p-best_threshold,Delta,c_e)=(1,0,1)` and two had `(1,1,1)`.

The seven residual graph6 records were

    F?o}W  FCQV_  G?BEH{  G?`CVo  G?o}][  GCQQVo  GCQSng.

For every one, the exact record shows a minimum OCT `T` for which `G-T` is a
forest (`tau(G-T)=0`), and `o(G)` is one or two.  This observation motivates
the next proved residual lemma; it is not folded back into L3.

## 5. Closing the observed residual by a separate structural lemma

> **L4 (small-OCT forest remainder).** Let `G` be connected and nonbipartite.
> If `o(G)<=2` and some minimum OCT `T` leaves a forest `G-T`, then LIFT-A
> holds with that `T`.

**Status: MATHEMATICALLY PROVED; not Lean-formalized.**

**Proof.** Since `G-T` is a forest, `tau(G-T)=0`, so the lifting inequality is
`ell(G)>=o(G)+1`.

If `o=1`, an odd cycle in `G`, with one cycle edge omitted, is a path with at
least two edges.  Adding all vertices outside that path as isolated vertices
gives a spanning linear forest with at least `2=o+1` edges.

If `o=2`, the maximum induced bipartite graph `G-T` has an edge (paper Lemma
5.2), hence `|G|>=4`.  Every connected nonbipartite graph on at least four
vertices contains a three-edge path: take a shortest odd cycle; if it has
length at least five, use three consecutive edges, while if it is a triangle,
connectedness and the extra vertex provide a path entering the triangle, which
can be followed by two consecutive triangle edges.  That path plus isolated
vertices is a spanning linear forest with at least `3=o+1` edges.  QED.

L4 was formulated after the seven L3-residual records were inspected, so its
`n<=8` computation is explicitly a regression test, not a prospective holdout.
The proof is independent of the census.

### Frozen L4 regression

The regression re-enumerates all connected graphs through `n=8`, recomputes
every minimum OCT and exact lifting slack, and reports how many of the seven
post-L3 residuals L4 covers.  The deliberately false strengthening
`ell(G)>=o(G)+2` on the same L4 class must fail (already `K_3` is a hand-checkable
control).  It depends on the frozen L3 checker at SHA-256
`78b7a981b113b627b77fcefff483d3d39b288145748ab0fcad30aadbcc507bb6`.

Checker `work/lift_residual_l4.py` has SHA-256
`b9c6fba9a9a4ff70fd8a37b3aeb6f91b2499d68b51498996335479a0b413ac1f`, also
recorded in `work/LIFT-RESIDUAL-L4-SHA256.txt`.  Result not yet executed at
freeze time.

**L4 regression result: COMPUTATIONALLY VERIFIED.**  Among all 11,859
connected nonbipartite graphs through `n=8`, L4 applies to 4,606.  It applies
to all 7 post-L3 residual graphs, so L3 or L4 covers all 11,859; no L4-covered
graph failed LIFT-A.  The false `ell>=o+2` strengthening failed twice, so its
control fired.  This is in-sample regression evidence for the proved lemma.

## 6. A stronger pair-sparse refinement

The seven residual bipartite graphs suggest retaining one more elementary
piece of component structure.  For an edge-containing bipartite component `C`,
let `r(C)=1` when one of its smaller bipartition classes (either class when the
sizes tie) contains two vertices with at most one common neighbour; otherwise
let `r(C)=0`.  Put

    r(B) = sum_C r(C).

> **L5-Forest.** For every finite bipartite graph `B`,
>
>     f(B) >= |B|-M(B)+c_e(B)+r(B),
>     equivalently tau(B) <= M(B)-c_e(B)-r(B).                  (5)

**Status: MATHEMATICALLY PROVED; not Lean-formalized.**

**Proof.** Use the L3-Forest construction componentwise.  In a component with
`r(C)=1`, take all vertices of the larger class and the certified pair `u,v`
from the smaller class instead of only one smaller-class vertex.  A cycle in
this induced bipartite graph would have to alternate between `u` and `v`; with
only these two vertices on their side it would be a 4-cycle through two common
neighbours.  The pair has at most one common neighbour, so no cycle exists.
This gains one vertex independently in every such component.  Summing proves
(5).  QED.

> **L5 (pair-sparse lift).** If some minimum OCT `T`, with `B=G-T`, satisfies
>
>     p(G) <= 2c_e(B)+Delta(B)+2r(B)-1,                         (6)
>
> then LIFT-A holds with `T`.

**Status: MATHEMATICALLY PROVED; not Lean-formalized.**

**Proof.** Substitute (5) and `2M(B)=|B|-Delta(B)` into the L3 algebra:

    2tau(B)+|T|+1 <= n-Delta(B)-2c_e(B)-2r(B)+1.

Condition (6) makes `ell(G)=n-p(G)` at least this large.  QED.

Every bipartite forest component whose smaller side has at least two vertices
has `r(C)=1`: two same-side vertices cannot share two neighbours without
forming a 4-cycle.  Thus L5 captures the structural source of the extra slack
seen in the seven post-L3 records, while applying beyond forest remainders.

### Frozen L5 regression

L5 was formulated after the `n<=8` L3/L4 output, so this is again explicitly a
regression, not a prospective holdout.  The checker independently recomputes
`r(B)`, verifies (5) on all 451 bipartite graphs through `n=8`, and measures L5
coverage on all 11,859 connected nonbipartite graphs.  A false one-unit
strengthening of (5) must fail.  Any (5) failure or L5-covered LIFT-A failure
halts the run.  It depends on the frozen L3 checker hash stated above.

Checker `work/lift_residual_l5.py` has SHA-256
`d2583ebdb17793be93c8af3bb71072912630ba9b05b79e8f396d3ab94784b1bd`, also
recorded in `work/LIFT-RESIDUAL-L5-SHA256.txt`.  Result not yet executed at
freeze time.

**L5 regression result: COMPUTATIONALLY VERIFIED.**  On all 451 bipartite
graphs through `n=8`, L5-Forest had 0 failures and 356 tight cases; the false
one-unit strengthening failed on all 356 tight cases.  On all 11,859 connected
nonbipartite graphs through `n=8`, L5 covered 11,859, adding exactly the seven
L3 residuals and leaving zero; no L5-covered graph failed LIFT-A.  The seven
newly covered records have `r(B)=1` and exact LIFT-A slack 3.  This is
regression evidence for the proved structured-class theorem, not evidence that
condition (6) holds in general.
