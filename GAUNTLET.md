# Comprehension gauntlet — attempt 9d2b

**Branch:** `attempt/2026-08-05-codex-gpt-5-9d2b`

**Protocol:** public `main` ATTACK.md v4 at `64eb3dacd3e332b9464faece8bd42f72e16bf6dc`

**Status:** MATHEMATICALLY PROVED / COMPLETED in this attempt's own words.

This document is written before any new SAFE-EXISTS mathematics. The public
paper, `proofs/PROOFS.md`, the three checked-in warning certificates, all five
public attempt reports, and public `attempts/LESSONS.md` were read first.

## 0. Model and notation used below

Let `G` be a connected nontrivial bipartite graph, `S` a minimum feedback
vertex set, and `H=G-S`; thus `H` is an induced forest and `|S|=tau(G)`. Fix an
edge `e=xy` of `H`. In the incidence-selection network every `s in S` has exact
demand 2; every `h in H` has capacity 2 except `x,y`, which have capacity 1. A
feasible selection `J` chooses two distinct `S-H` incidences at every `s` and
respects all `H` capacities. A selected cycle is a cyclic component of `J`.

For `X subseteq S`, put

`rho(X)=sum_{h in H} min(c(h),deg_X(h))` and
`delta(X)=rho(X)-2|X|`.

The generalized Hall criterion says feasibility is equivalent to
`delta(X)>=0` for every `X`. An incidence is forced exactly when a Hall-tight
set `X` (`delta(X)=0`) exposes it. The forced core is the graph consisting of
all forced incidences.

A toggle is CES for an old selected cycle `C` when it destroys `C` and every
selected cycle after the toggle was already selected before it. Thus a CES
toggle creates no new selected cycle and strictly decreases the number of
selected cycles. The weaker fact “strictly fewer cycles” would already support
termination, but CES is the semantic move supplied by the paper's mechanism.

## 1. Theorem 3.13 reduction: exact role of A and B

**Status: MATHEMATICALLY PROVED.** The chain is as follows.

### 1.1 Hereditary FVS tightness

For every `X subseteq S`,

`tau(G[H union X])=|X|`.

The upper bound is immediate because deleting `X` leaves the forest `H`. If a
set `D` with `|D|<|X|` were an FVS of `G[H union X]`, then
`(S\X) union D` would be an FVS of `G` of size
`|S|-|X|+|D|<|S|`, contradicting minimality of `S`. This is the structural
input that later separates real graph instances from arbitrary Hall-feasible
incidence systems.

### 1.2 A fixed edge of H exists

The case `tau(G)=0` is handled separately by the paper. Suppose `tau(G)>=1`.
If `E(H)` were empty, then for any `s in S`, the graph
`G[H union {s}]` would be a star forest: `H` has no edges and all remaining
edges meet `s`. Its FVS number would be 0, contradicting hereditary tightness,
which gives 1. Hence `E(H)` is nonempty and an edge `e=xy` can be fixed.

### 1.3 Initial feasibility does not use A or B

The rooted-forest-extension lemma bounds
`tau(G[H union X]) <= floor(rho_e(X)/2)` for an independent one-side set `X`.
Split an arbitrary `X subseteq S` across the two bipartition classes. Their
capacity supports in `H` are disjoint, so `rho_e` is additive across the split.
If `rho_e(X)<2|X|`, one side would have `rho_e(X_i)<2|X_i|`; the rooted bound
would give `tau(G[H union X_i])<|X_i|`, contradicting hereditary tightness.
Thus `rho_e(X)>=2|X|` for every `X`, and generalized Hall supplies a feasible
selection for every fixed `e`.

### 1.4 Lemma A supplies only an avoidable incidence

Lemma A says the forced core is acyclic. Take any selected cycle `C` in a
feasible `J`. If every incidence of `C` were forced, those same incidences
would form a cycle in the forced core. Therefore `C` contains at least one
avoidable incidence. This is the exact use of A: it establishes the premise of
B for each selected cycle. A does not itself produce a toggle or perform
descent.

### 1.5 Residual augmentation turns avoidability into one move

For a selected incidence `a=(s,h)`, remove the unit flow through `a` and delete
the incidence arc. The resulting flow has value `2|S|-1`, with the source arc
to `s` the unique deficient source arc. A feasible selection omitting `a`
exists exactly when the residual network has an augmenting path from that
deficiency to residual `H` capacity. Augmenting along one simple residual path
restores value `2|S|` and still omits `a`. Hence “globally avoidable” and
“avoidable by one residual augmentation” coincide.

### 1.6 Lemma B supplies the descent move

Lemma B says every selected cycle containing an avoidable incidence admits a
CES toggle. A supplied an avoidable incidence on every selected cycle; B now
turns that premise into a move. This is the exact use of B: it produces a
cycle-erasing toggle. B does not establish initial feasibility and does not
show that a selected cycle has an avoidable edge.

### 1.7 Descent terminates

Starting with the feasible `J`, if a selected cycle remains, A and B provide a
CES toggle. Each such toggle strictly decreases the nonnegative integer
`#cyc(J)`, so iteration terminates at an acyclic feasible selection `J*`.

This identifies the weaker live core in v4. The reduction actually needs only
SAFE-EXISTS/SD: from every cyclic feasible state, some safe toggle sequence or
some cycle with a suitable toggle yields strict descent. It does not need a
universal local-toggle statement for every selected cycle. A+B is one route to
that existential conclusion, not the conclusion's logical minimum.

### 1.8 Convert the terminal selection into the desired linear forest

Fixed-edge parity says `e` lies on no selected cycle and `J* union {e}` is
acyclic exactly when `J*` is. The reason is bipartite parity: a cycle through
`e=xy` would leave, after deleting `e`, an even-length incidence path between
the opposite-class vertices `x,y`, whereas every bipartite `x-y` path has odd
length.

The graph `J* union {e}` has maximum degree at most 2. Every `s` has degree 2;
ordinary `H` vertices have selected degree at most 2; and `x,y` have selected
degree at most 1, so adding `e` keeps their degree at most 2. An acyclic graph
of maximum degree 2 is a disjoint union of paths. It spans `V(G)` and has
exactly `2|S|+1` edges: two selected incidences for each `s`, plus `e`.
Therefore the largest spanning linear forest has at least
`2|S|+1=2 tau(G)+1` edges, which is the bipartite target used by Conjecture 40.

The load-bearing map is therefore:

`minimum FVS -> hereditary tightness -> feasibility ->`
`A: an avoidable edge -> B: a CES move -> descent -> acyclic selection ->`
`fixed-edge parity and degree count -> linear forest bound`.

## 2. Why Hall feasibility alone cannot imply Lemma A

**Status: MATHEMATICALLY PROVED.** Fix `m>=2`. Let
`S={s_0,...,s_{m-1}}` and `H={h_0,...,h_{m-1}}`, all `H` capacities 2, and
give `s_i` exactly the two neighbours `h_i,h_{i+1}` (indices modulo `m`).

For any `X subseteq S`, every `h` has `deg_X(h)<=2`, so truncation at capacity
2 does nothing:

`rho(X)=sum_h deg_X(h)=sum_{s in X} deg_H(s)=2|X|`.

Thus every Hall inequality holds with equality. A feasible selection exists.
In fact it is unique, because each `s_i` has exactly two available incidences
and demand 2. Consequently all incidences are forced, and the forced core is
the entire alternating cycle

`s_0-h_1-s_1-h_2-...-s_{m-1}-h_0-s_0`.

Hall feasibility, submodularity, tight-set closure, and even universal
Hall-tightness therefore coexist with a cyclic forced core.

What fails is the graph-theoretic hypothesis. With no `H-H` edges, the graph
`G[H union S]` is that even cycle, so one vertex kills its only cycle:
`tau(G[H union S])=1<|S|=m`. Hereditary FVS tightness fails (already at the
full set, and in small versions on smaller nonempty sets as well). Thus a proof
of Lemma A must use hereditary FVS tightness or an equivalent consequence; the
Hall layer alone cannot prove it.

## 3. Warning witnesses and the strategies they delimit

**Status: COMPUTATIONALLY VERIFIED in the binding public certificates and
attempt reports.** The mechanisms below are also directly checkable from the
listed capacities and unique/saturated selections. None is a counterexample to
Lemma A: each deliberately violates hereditary FVS tightness. They constrain
where a Lemma-A contradiction may be sought.

For a forced-cycle vertex `s`, let `A_s` be the canonical minimum Hall-tight
set exposing both forced cycle incidences, and let `B_s=A_s\{s}`. Punctured
tightness proves `B_s` is Hall-tight. The false shortcuts tried to turn that
Hall fact into a fixed location for a hereditary-FVS violation.

### 3.1 O-56: the acyclic-quotient/single-blocker normal form, and failure of P-localization

The cycle side is `P={0,1}`. The auxiliaries are `2,3`. Incidences are
`0,1 ~ {4,5,6}`, `2 ~ {6,7}`, and `3 ~ {6,8}`; the distinguished capacity-one
edge has no S-incidences. Vertices 2 and 3 each have exactly two neighbours and
demand 2, so they must take both. Their incidences saturate `c(6)=2`, forcing
0 and 1 off 6 and onto `{4,5}`. The unique selection has the forced cycle
`0-4-1-5-0`.

Here `A_0={0,2,3}` and `B_0={2,3}`. Deleting the external vertex 6 makes
`G[H union B_0]` a forest, so
`tau(G[H union {2,3}])=1<2`; the hereditary violation is the auxiliary pair.
By contrast, `tau(G[H union P])=2=|P|`: the cycle side is clean. Thus O-56
falsifies the claim that the contradiction must live on `P`.

O-56 also realizes the proved degree-two/single-blocker subcase. Each member of
`U_6={2,3}` has at most one H-neighbour besides 6, so deleting 6 leaves them as
leaves on the forest `H-6`. This is evidence that the subcase is nonempty, not
evidence that every punctured carrier has this degree pattern.

### 3.2 O-63: the reachable high-degree/cyclic-quotient branch

The cycle side is `{s,t}`. The three auxiliaries `u,a,b` each have neighbourhood
`{h,w,z}`; their total demand 6 equals the total capacity of those three
H-vertices. Hence they saturate all of `{h,w,z}`, pushing `s` off `h`; `s` and
`t` are then forced onto `{q1,q2}`, giving the forced cycle
`s-q1-t-q2-s`. There are six feasible assignments among the auxiliaries but
the four cycle incidences are forced.

Here `A_s={s,u,a,b}`, `B_s=U_h={u,a,b}`, and every vertex of `B_s` has
incidence-degree 3. Therefore “every punctured-carrier vertex has degree 2” is
FALSIFIED. The full `B_s` is the hereditary violation:
`tau(G[H union B_s])=2<3`, with blocker `{h,w}` or `{h,z}`; every proper subset
of `B_s` is tight in the within-puncture sense. Thus a single external blocker
need not suffice.

The forest-geometry distinction is essential. Contracting the components of
`H-h` gives the quotient `M_h(B_s)`. In O-63, `H-h` remains connected and each
of `u,a,b` has two non-h neighbours in that same component, producing parallel
quotient edges and hence a cyclic quotient. This demonstrates that the
high-degree/cyclic-quotient branch is genuinely reachable. Incidence degree by
itself is not the correct criterion: a degree-3 vertex has a private cycle
avoiding `h` only when two of its non-h attachments lie in the same component
of `H-h`. O-63 lies on that cyclic side; it is the quotient, not the numeral
“3”, that explains the cycle.

Together O-56 and O-63 bracket the capacity-2 geometry: the quotient may be
acyclic with a one-vertex blocker, or cyclic with a larger blocker. A proof may
not assume the O-56 degree-two normal form.

### 3.3 O-64: failure of B_s-localization and the capacity-one branch

Here `S={s,t,u}` and the fixed edge is `e=hy`, so `c(h)=c(y)=1`. Incidences are
`s~{q1,q2,h}`, `t~{q1,q2}`, and `u~{h,w}`. Since `u` has demand 2 and exactly
two neighbours, it uses both and saturates the capacity-one vertex `h`. This
pushes `s` off `h`; `s,t` are forced onto `{q1,q2}`, and the unique selection
contains the forced cycle `s-q1-t-q2-s`.

The carrier is `A_s={s,u}` and its puncture is `B_s={u}`. Although `B_s` is
Hall-tight, it is hereditary-FVS clean:
`tau(G[H union B_s])=1=|B_s|`. No subset of `B_s` supplies a contradiction and
there is no feasible exchange avoiding a cycle incidence. Instead the first
violation is the cycle side `P={s,t}`, with
`tau(G[H union P])=1<2`.

Thus B_s-localization and the sharper assertion
`tau(G[H union B_s])<=|B_s|-1` are FALSIFIED. O-56 and O-64 are mirror warnings:
in O-56, `P` is clean and the auxiliaries violate; in O-64, `B_s` is clean and
`P` violates. Neither `P` nor any single `B_s` is a universal localizer, and
capacity-one external neighbours cannot be silently treated as the capacity-2
branch.

## 4. The T_F normalization (paper Lemma 4.7)

**Status: MATHEMATICALLY PROVED.** Work in the disconnected formulation
Lemma A°, since restriction may destroy connectedness. Suppose a forced
core cycle `F` has S-side `P`. For each `s in P`, let `A_s` be its canonical
minimum Hall-tight carrier, and set

`T_F = union_{s in P} A_s`.

Restrict to `G'=G[H union T_F]` with `S'=T_F`, retaining the same `H`, fixed edge
`e`, and capacities. Then:

1. `G'-S'=H` is a forest.
2. `S'` is a minimum FVS of `G'` and hereditary FVS tightness holds for every
   `X subseteq T_F`.
3. The restricted selection system is feasible.
4. Every `A_s` stays Hall-tight and exposes the same two cycle incidences.
5. Every edge of `F` is forced again in the restricted system, so `F` remains
   a forced-core cycle.

For (1), only S-vertices outside `T_F` were deleted. For (2), if
`X subseteq T_F`, then `G'[H union X]` and `G[H union X]` are literally the
same induced graph. Original hereditary tightness therefore gives
`tau(G'[H union X])=|X|`. Taking `X=T_F` makes `T_F` a minimum FVS of `G'`.
For (3), the original Hall inequalities simply restrict to subsets of `T_F`,
so generalized Hall gives a feasible selection.

The delicate point is (4)-(5). Forcedness is not monotone under deleting demand
vertices: removing `S\T_F` can free H-capacity and create new feasible
selections. Therefore forcedness may not merely be inherited. Instead it is
re-established through the F1 characterization. Each `A_s` is contained in
`T_F`; `rho(A_s)` and the exposing degree at the two cycle endpoints depend
only on incidences from `A_s`, the same H-vertices, and the same capacities.
Thus `A_s` remains tight and still exposes both incidences. F1 makes those
incidences forced afresh in the restricted instance. Doing this for every
`s in P` preserves all edges of `F`.

Consequently any counterexample can be normalized to one with `S=T_F`: every
S-vertex lies in some canonical carrier of a forced-cycle vertex. This license
removes carrier-irrelevant S-vertices and permits an argument to use the full
carrier family.

It does not license any of the following: that the hereditary violation is
`P`, one `B_s`, or `T_F`; that forcedness is monotone under restriction; that
connectedness is preserved; or that one may use the three warning instances as
Lemma-A counterexamples. The warning instances happen set-theoretically to
satisfy `S=T_F`, but each fails the minimum-FVS/hereditary-tightness hypothesis.

## 5. Gauntlet verdict

**Status: MATHEMATICALLY PROVED / COMPLETED.** All four v4 requirements are
derived above. The reduction distinguishes the roles of A and B; the abstract
cycle shows Hall feasibility is insufficient; the warning witnesses are used
only at their exact falsification scopes; and the normalization re-proves
forcedness via tight exposing carriers rather than assuming monotonicity.

The attempt may proceed to SAFE-EXISTS.
