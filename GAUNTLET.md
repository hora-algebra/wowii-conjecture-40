# GAUNTLET — ATTACK-2 comprehension record

Branch `attempt/2026-08-04-codex-a7c3`, 2026-08-04.  This is the Step 1
record required by `ATTACK.md`.  The mathematical derivations below have status
**MATHEMATICALLY PROVED**; the numerical descriptions of O-56/O-63/O-64 have
status **COMPUTATIONALLY VERIFIED** by the hash-checked frozen certificates and
the independent `work/wcheck.py` engine from the preceding attempt.

Write `tau=n-f`, `o=n-b`, and `ell=n-p`.  In the bipartite incidence model,
`S` is a minimum FVS, `H=G-S` is a forest, `e=xy` is a fixed edge of `H`, every
`s in S` has demand two, and every `h in H` has capacity two except
`c(x)=c(y)=1`.  A feasible selection is the corresponding integral demand-two
`b`-matching.  For `X subseteq S`, put

    rho(X) = sum_h min(c(h), deg_X(h)),   delta(X)=rho(X)-2|X|.

The minimum-FVS hypothesis gives hereditary tightness
`tau(G[H union X])=|X|` for every `X subseteq S`: `X` itself is an FVS of the
induced graph, while an FVS `D` smaller than `X` would make
`(S-X) union D` an FVS of `G` smaller than `S`.

## 1. Theorem 3.13: exactly how Lemmas A and B imply the bipartite case

The deficiency form of Conjecture 40 is

    ell(G)+o(G) >= 2 tau(G)+1.

Indeed, `2f >= p+b+1`; substituting `f=n-tau`, `b=n-o`, and `p=n-ell`
and cancelling `2n` gives the displayed inequality.  On a bipartite graph
`o=0`, so the target is `ell>=2tau+1`.

If `tau=0`, connectedness and nontriviality give an edge; that edge and all
other vertices as trivial paths form a spanning linear forest with one edge.
Now assume `tau>=1` and choose a minimum FVS `S`.

1. `E(H)` is nonempty.  If it were empty, then for any `s in S` the graph
   `G[H union {s}]` would be a star plus isolated vertices and would have FVS
   number zero, contradicting hereditary tightness, which gives one.  Thus a
   distinguished edge `e=xy` can be fixed.
2. A feasible selection exists for this fixed edge.  The generalized Hall
   calculation says feasibility is equivalent to `rho(X)>=2|X|` for every
   `X subseteq S`: a cut whose source-side `S`-set is `X` has minimum capacity
   `2(|S|-|X|)+rho(X)=2|S|+delta(X)`.  Split `X` by the two bipartition
   classes.  The two parts contribute to disjoint `H`-supports.  If one part
   had `rho(X_i)<2|X_i|`, the rooted-forest extension lemma would give
   `tau(G[H union X_i])<=floor(rho(X_i)/2)<|X_i|`, contradicting hereditary
   tightness.  Hence Hall holds.  This proves initial feasibility for every
   `e`, though the final theorem needs only some `e`.
3. Lemma A is used at one precise point.  If a selected cycle consisted only
   of forced incidences, it would be a cycle in the forced core.  Lemma A says
   the forced core is acyclic, so every selected cycle has at least one
   avoidable incidence.
4. Lemma B applies to that avoidable incidence and supplies a CES toggle:
   the designated selected cycle disappears and no previously absent selected
   cycle appears.  Therefore the selected-cycle count strictly decreases.
   Repeating terminates because that count is a nonnegative integer, leaving
   an acyclic feasible selection `J`.
5. Adding `e` preserves acyclicity.  A cycle through `e` would leave, after
   deleting `e`, an even-length `x`--`y` path alternating through `H,S,H,...`.
   But adjacent vertices `x,y` lie in opposite bipartition classes, so every
   `x`--`y` path in `G` has odd length.
6. `J union {e}` has maximum degree two: demand gives degree two at each
   `s`; capacities give degree at most two at each ordinary `h`; and the two
   capacity-one endpoints retain room for `e`.  An acyclic graph of maximum
   degree two is a disjoint union of paths.  It spans `V(G)` and has
   `2|S|+1=2tau(G)+1` edges, proving the bipartite target.

Thus Lemma A only establishes the avoidable-edge premise of Lemma B; Lemma B
only supplies the decreasing move.  The Hall/rooted-forest results initialize
the process, parity permits adding `e`, and the degree count converts the final
selection into a linear forest.  The composite requirement is the weaker F2
statement: for some `e in E(H)`, an acyclic feasible selection exists.  A+B is
a sufficient route to F2, not a logically equivalent restatement of F2.

## 2. Why Hall feasibility cannot prove Lemma A

For `m>=2`, take `S={s_1,...,s_m}` and abstract `H`-vertices
`{h_1,...,h_m}`, with indices cyclic and

    N(s_i)={h_i,h_{i+1}},  demand(s_i)=2,  c(h_j)=2.

For every `X subseteq S`, no `h_j` has more than two neighbours in `X`, so

    rho(X)=sum_j deg_X(h_j)=sum_{s in X} deg_H(s)=2|X|.

Every subset is Hall-tight.  Each `s_i` nevertheless has exactly two available
incidences and must select both, so the feasible selection is unique and its
forced core is the entire alternating `2m`-cycle.  Hall feasibility,
submodularity, the tight-set lattice, and forced-edge exposure all coexist with
a cyclic forced core.

Realize the abstract system with no `H`--`H` edges.  The resulting graph is the
same `2m`-cycle and has FVS number one.  At `X=S`, therefore,

    tau(G[H union S])=1<m=|S|.

The missing hypothesis is exactly hereditary FVS tightness.  The all-capacity-
two example fits Lemma A° bookkeeping by adjoining a disjoint `K_2` and
taking its edge as `e`; the capacity-one endpoints then have no incidences.
Consequently any proof of Lemma A must use the forest geometry to find a set
whose FVS number drops, or use that geometry to construct an exchange.  The
Hall data alone cannot distinguish the forbidden abstract cycle from a legal
minimum-FVS instance.

## 3. What the warning witnesses rule out

None of O-56, O-63, or O-64 is a Lemma-A counterexample.  The independent
checker gives `tau(G)=2<4`, `3<5`, and `2<3`, respectively, for their displayed
sets `S`, while each forced core has cycle rank one.  They are controls showing
where hereditary tightness may fail when the minimum-FVS premise is removed.

### O-56: the violation need not be on the cycle side `P`

Here `P={0,1}`; auxiliary vertices `2,3` are rigid on `{6,7}` and `{6,8}`.
They saturate the capacity-two vertex `6`, forcing `0,1` away from `6` and onto
`{4,5}`.  Hence `0-4-1-5-0` is forced.  Direct enumeration finds one feasible
selection and an eight-edge forced core (VERIFY-1 correctly identifies the
ten-edge list in the JSON metadata as erroneous; the certified cycle itself is
unchanged).

Every subset of `P` is FVS-tight, but `X={2,3}` has FVS `{6}`, so
`tau(G[H union X])=1<2`.  Thus a forced cycle does not force a hereditary
violation inside `P`; the P-local/CVB bridge is false.  Positively, it realizes
the proved single-blocker case: for the carrier `A_0={0,2,3}`, puncture
`B_0={2,3}`, and external vertex `h=6`, deleting `h` leaves each puncture
vertex with at most one remaining `H`-neighbour.

### O-63: the capacity-two branch is not a degree-two/private-cycle normal form

The auxiliary set `{u,a,b}` has total demand six and only the three capacity-two
outlets `{h,w,z}`.  It saturates all of them.  Vertex `s` is pushed off `h`
onto `{q1,q2}`, while `t` is rigid there, forcing
`s-q1-t-q2-s`.  There are six feasible selections and precisely those four
cycle edges are forced.

The carrier puncture is `B_s={u,a,b}`.  Every one of its vertices has incidence
degree three, refuting the proposed universal degree-two localization.  After
deleting `h`, the other neighbours `w,z` lie in the same component of `H-h`;
the quotient has parallel edges and is cyclic.  Thus high incidence degree does
not create a private cycle in the manner required by the one-blocker proof.
Within `B_s`, every proper pair is FVS-tight but the whole puncture has
`tau=2<3`, with a two-vertex blocker such as `{h,w}`.  The blocker therefore
need not be the single external vertex.

### O-64: a carrier puncture need not contain any violation

The fixed edge is `hy`, so `c(h)=1`.  Auxiliary vertex `u` is rigid on
`{h,w}` and alone saturates `h`; this pushes `s` onto `{q1,q2}`, where `t` is
already rigid, forcing `s-q1-t-q2-s`.  The feasible selection is unique.

Here `A_s={s,u}` and `B_s={u}` are Hall-tight, but
`tau(G[H union B_s])=1=|B_s|`: the puncture is hereditarily clean.  The first
displayed failure is instead `P={s,t}`, where deleting `q1` gives
`tau(G[H union P])=1<2`.  Hence violation-in-`B_s` is false, and capacity-one
and capacity-two external neighbours cannot be merged into one argument.

Together O-56 and O-64 show that neither `P` nor one puncture is a universal
localizer; O-63 shows that the capacity-two puncture analysis cannot assume the
O-56 degree pattern or a one-vertex blocker.

## 4. The `T_F` normalization and its exact license

Suppose, toward a contradiction to Lemma A°, that the forced core contains a
cycle `F`.  Let `P` be its `S`-side.  For each `s in P`, forced-edge exposure and
the tight-set lattice give the canonical carrier `A_s`: the unique
inclusion-minimal Hall-tight set containing `s`, exposing both forced edges at
`s`.  Define

    T_F = union_{s in P} A_s,
    G' = G[H union T_F],   S'=T_F.

Then the following all hold.

1. `G'-S'=H`, still a forest.
2. For every `X subseteq T_F`, the graphs `G'[H union X]` and
   `G[H union X]` are literally identical.  Hereditary tightness in the
   original instance therefore gives `tau(G'[H union X])=|X|`.
3. Taking `X=T_F` proves `tau(G')=|T_F|`; since deleting `T_F` leaves `H`,
   `T_F` is a minimum FVS of `G'`.
4. The rank function `rho` depends only on the `X`--`H` incidences and the
   capacities, none of which changes.  Hall inequalities restrict to all
   subsets of `T_F`, so the reduced instance remains feasible.
5. Forcedness is not assumed monotone under deleting demand vertices.  Instead,
   for every edge of `F` at `s`, the same `A_s subseteq T_F` remains tight with
   the same degrees and still exposes that edge.  The forced-edge criterion
   therefore re-proves that edge forced in the reduced instance.  Thus `F`
   survives.

Connectedness can be lost, which is why the open statement is Lemma A°
for possibly disconnected graphs.  The normalization licenses the assumption
`S=T_F` in a minimal counterexample and nothing stronger: it does not imply
`P` is tight, `P` is disjoint from the puncture union, the violation lies in a
particular carrier, or the warning witnesses satisfy the minimum-FVS premise.

## Gauntlet outcome

**MATHEMATICALLY PROVED:** the four required derivations are complete.
**COMPUTATIONALLY VERIFIED:** `tools/SHA256SUMS.txt` passes 17/17 from its
declared working directory; `wcheck.py` reproduces feasibility, forced-cycle
rank, carriers, punctures, and every hereditary profile for O-56/O-63/O-64.
The run may proceed to ATTACK.md Step 3.
