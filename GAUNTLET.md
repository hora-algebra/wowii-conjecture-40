# GAUNTLET — SAFE-2-EXISTS attack 7851

Branch `attempt/2026-08-05-codex-gpt-5-7851`, written before any new
mathematics or target scan.  This is a fresh derivation from `paper/paper.tex`,
`proofs/PROOFS.md`, and the three shipped witness certificates.

Notation: `G` is bipartite; `S` is a minimum feedback vertex set; `H=G-S` is
a forest; `e=xy` is a fixed edge of `H`.  Each `s in S` has demand two.  The
capacity of each `h in H` is two except `c(x)=c(y)=1`.  A feasible selection
chooses two `S-H` incidences at every `s` without exceeding the capacities.
An incidence is forced if every feasible selection uses it.  A CES toggle for
a designated selected cycle deletes that cycle and creates no selected cycle
that was not already present.

## 1. The reduction: the exact work done by A, B, F2, and SAFE-2

For a bipartite graph the deficiency form of Conjecture 40 is

    ell(G) >= 2 tau(G) + 1,

where `ell=n-p` is the maximum number of edges in a spanning linear forest and
`tau=n-f` is the minimum FVS size.

If `tau=0`, connectedness and nontriviality give an edge.  That edge together
with isolated one-vertex paths is a spanning linear forest with one edge, so
the target is immediate.  Assume `tau>=1` and take a minimum FVS `S`, of size
`tau`; then `H=G-S` is a forest.

There must be an edge in `H`.  Otherwise, for any `s in S`, the graph induced
by `H union {s}` is a star plus isolated vertices, hence has FVS number zero.
Hereditary FVS tightness gives instead
`tau(G[H union {s}])=1`, a contradiction.  Thus an edge `e=xy` can be fixed.

Initial feasibility for this fixed edge is unconditional once `S` is minimum.
For `X subseteq S`, define

    rho(X) = sum_{h in H} min(c(h), deg_X(h)).

The generalized Hall criterion says a feasible selection exists exactly when
`rho(X)>=2|X|` for every `X`.  Its min-cut calculation is: for a cut whose
source side contains exactly `X` from `S`, the source arcs to `S-X` cost
`2(|S|-|X|)`; each `h` can be put on the cheaper side for a cost
`min(c(h),deg_X(h))`.  The least cut with this `X` therefore has capacity
`2|S| + rho(X)-2|X|`.  A flow of value `2|S|` exists iff all these deficits are
nonnegative.

To prove those inequalities, split `X` between the two bipartition classes.
The two parts contribute to disjoint sets of `H`-vertices.  If their total
`rho` were less than `2|X|`, one part `Y` would have `rho(Y)<2|Y|`.  The rooted
forest-extension lemma would then give

    tau(G[H union Y]) <= floor(rho(Y)/2) < |Y|,

contradicting hereditary tightness.  Hence a feasible selection exists for
every fixed edge, a stronger quantifier than F2 needs.

Now fix any feasible selection `J` having a selected cycle `C`.

- Lemma A says the forced core is acyclic.  If every incidence of `C` were
  forced, `C` itself would lie in that core.  Therefore `C` has an avoidable
  incidence.  This is the only role of Lemma A in the reduction.
- Lemma B says a selected cycle with an avoidable incidence admits a CES
  toggle.  This is the only role of Lemma B.
- Each CES toggle strictly decreases the nonnegative integer counting selected
  cycles.  Repetition terminates at an acyclic feasible selection.

Let that terminal selection again be called `J`.  Adding the fixed edge `e`
does not create a cycle.  A cycle using `e=xy` would leave, after deleting
`e`, an even-length alternating `H-S-H` path from `x` to `y`; but `x` and `y`
are in opposite bipartition classes, so every path between them has odd
length.  Thus `J union {e}` is acyclic.

It also has maximum degree at most two.  Every `s` has degree two; ordinary
`H`-vertices respect capacity two; and `x,y` have selection degree at most one,
leaving room for `e`.  Therefore `J union {e}` is a spanning linear forest.  It
has `2|S|+1=2tau(G)+1` edges, proving the bipartite inequality.

The logical compression is F2: for some fixed `e`, an acyclic feasible
selection exists.  A+B imply F2 via CES descent, but they are not the statement
F2 itself.

The live target is weaker still.  Write `c(J)` for the selected-cycle count and
call a minimizing toggle CES when it erases its designated cycle without
creating a new one.  SAFE-2-EXISTS says that every cyclic `J` has either

1. a CES minimizing step; or
2. an A1-bad minimizing step `J -> J0` with `c(J0)<=c(J)`, after which `J0`
   has a CES minimizing step.

In the first case the cycle count falls in one step.  In the second it does not
increase on the first step and falls on the second.  Repeating blocks of at
most two steps terminates for the same integer-descent reason, directly giving
F2.  The certified implication `SAFE-2-EXISTS => F2` therefore proves only the
conditional reduction; the present attack must establish the SAFE hypothesis.

## 2. Why Hall feasibility cannot prove Lemma A

Take `m>=2`, vertices `S={s_0,...,s_{m-1}}` and
`Q={q_0,...,q_{m-1}} subset H`, with incidence edges

    s_i q_{i-1}, s_i q_i                 (indices modulo m)

and capacity two at every `q_i`.  Add an incidence-disjoint fixed `H`-edge if
the fixed-edge model is desired.  Each `s_i` has exactly two available
incidences, so the feasible selection is unique and consists of the whole
alternating even cycle.  Every incidence is forced; the forced core is cyclic.

Nevertheless every Hall inequality is tight.  For `X subseteq S`, each
`q_i` has `X`-degree at most two, so truncating at capacity two changes nothing:

    rho(X) = sum_i deg_X(q_i) = 2|X|.

Thus Hall feasibility, tight-set submodularity, and even universal Hall
tightness all coexist with a cyclic forced core.

What fails is the graph-theoretic certificate inherited from a *minimum* FVS.
For a singleton `{s_i}`, the graph induced by `H union {s_i}` is a path/star
and has FVS number zero, not one.  Also the full incidence cycle has FVS number
one, which is less than `|S|` when `m>=2`.  Hence hereditary FVS tightness is
essential; it is information not encoded in `rho`.

## 3. The three warning witnesses and the exact shortcuts they kill

None of O-56, O-63, or O-64 satisfies hereditary FVS tightness.  Their forced
cycles are therefore permitted.  They are counterexamples to proposed proof
localizations, not to Lemma A.

### O-56: the acyclic-quotient, single-blocker branch is real

Here `P={0,1}` is the forced cycle side and auxiliaries are `{2,3}`.  Vertices
2 and 3 must respectively select `{6,7}` and `{6,8}`.  They saturate the
capacity-two vertex 6, forcing 0 and 1 away from 6 and onto `{4,5}`.  The
four incidences through 4 and 5 form the forced cycle.

For cycle vertex 0 the canonical carrier is `A_0={0,2,3}` and its tight
puncture is `B_0={2,3}`.  Removing the single external vertex 6 makes both 2
and 3 leaves of the remaining `H`-forest, so
`tau(G[H union {2,3}])<=1<2`.  The hereditary violation lies in the auxiliary
puncture and is disjoint from `P`; meanwhile
`tau(G[H union P])=|P|`.  Thus a proof cannot insist that the violation is on
the cycle side.  O-56 also confirms, rather than refutes, the proved
degree-at-most-one/single-blocker subcase: its forest quotient is acyclic.

### O-63: degree and private-cycle shortcuts fail

The three auxiliaries `u,a,b` have total demand six and their available
vertices `h,w,z` have total capacity six, so they saturate all three.  This
pushes `s` off `h`; together with rigid `t`, the incidences through `q1,q2`
form the forced 4-cycle.

The carrier is `A_s={s,u,a,b}` and `B_s={u,a,b}`.  Every vertex of `B_s` has
incidence degree three, so the proposed rule that punctures consist of
degree-two vertices is false.  The first violation within the puncture is the
whole three-set and needs a two-vertex blocker such as `{h,w}`; no singleton
external blocker suffices.  Moreover high incidence degree alone does not
force the desired private cycle: whether two attachments close a cycle depends
on their components in `H-h`, i.e. on the (augmented) forest quotient.  Here
that quotient is cyclic, demonstrating the genuine branch the degree-only
argument fails to resolve.

### O-64: puncture localization fails in the capacity-one branch

The fixed edge is `hy`, so `c(h)=1`.  Vertex `u` must select `{h,w}` and
saturates `h`; consequently `s` cannot select `sh` and, with `t`, is forced
onto `q1,q2`.  This creates the forced cycle
`s-q1-t-q2-s` in the unique feasible selection.

Here `A_s={s,u}` and `B_s={u}` is Hall-tight, but

    tau(G[H union B_s]) = 1 = |B_s|.

The puncture contains no hereditary violation and admits no exchange.  The
violation instead lies on `P={s,t}`, since deleting `q1` shows
`tau(G[H union P])=1<2`.  Therefore neither `P` nor `B_s` is a universal
localizer, and the capacity-one and capacity-two external-neighbour branches
cannot be conflated.

## 4. The T_F normalization and what it licenses

Assume, for contradiction, a Lemma-A-degree instance with a forced-core cycle
`F`; let `P` be its `S`-side.  For each `s in P`, let `A_s` be its canonical
minimum Hall-tight carrier and put

    T_F = union_{s in P} A_s.

Restrict to `G'=G[H union T_F]` and set `S'=T_F`, keeping `H`, `e`, capacities,
and all remaining incidences.

For every `X subseteq T_F`, the induced graph `G'[H union X]` is literally the
same as `G[H union X]`.  Original hereditary tightness therefore gives
`tau(G'[H union X])=|X|`.  In particular, at `X=T_F`, the set `T_F` is a
minimum FVS of `G'` (it is an FVS because deleting it leaves the forest `H`).

The Hall function on subsets of `T_F` is unchanged: it depends only on `H`,
the capacities, and the incidences from the chosen subset.  Hence all original
Hall inequalities restrict to `T_F`, so the restricted system remains
feasible.

Forcedness must not be asserted monotone under restriction.  Removing demands
outside `T_F` can create new feasible selections.  Instead, re-force every
cycle incidence at `s` using F1: `A_s` remains a tight subset of `T_F`, its
degrees and capacities are unchanged, and it still exposes that incidence.
Thus every edge of `F` remains forced and the cycle survives in the restricted
instance.

Consequently a minimal counterexample to Lemma A-degree may be normalized to
`S=T_F`; disconnectedness caused by restriction is why the degree form is
needed.  The normalization licenses use of the complete carrier family without
outside `S`-vertices and preserves hereditary tightness and the forced cycle.
It does not prove that a hereditary violation lies in `P`, one `B_s`, or any
other proposed local set; it does not make forcedness monotone; and it does not
turn Hall tightness into hereditary FVS tightness.

## Outcome

**COMPLETED.**  The reduction, Hall countermodel, witness mechanisms, and
normalization have been derived with their quantifiers and failure boundaries
kept separate.  New SAFE-2-EXISTS work may now begin.
