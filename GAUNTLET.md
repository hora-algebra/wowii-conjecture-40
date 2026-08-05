# Comprehension gauntlet — fresh attempt b17e

**Branch:** `attempt/2026-08-05-codex-gpt-5-b17e`
**Status:** MATHEMATICALLY PROVED for the derivations below; the witness
profiles are separately labeled COMPUTATIONALLY VERIFIED.
**Sources read:** `paper/paper.tex` §§3–4 and §7, `proofs/PROOFS.md` §§B,D,
`proofs/LEMMA-A-CHALLENGE.md`, the three JSON certificates in
`tools/witnesses/`, and every binding prior-attempt report.

The symbol `tau` below means feedback-vertex number. The fixed bipartite graph
has a minimum FVS `S`, the induced forest `H=G-S`, and a distinguished edge
`e=xy` of `H`. Each `s in S` demands two distinct incidences into `H`; every
`h in H` has capacity two except `x,y`, which have capacity one. A feasible
selection is the resulting integral demand-saturating b-matching. Its selected
cycles use only `S-H` incidences.

## 1. Theorem 3.13 reduction: the exact jobs of Lemmas A and B

**Status: MATHEMATICALLY PROVED.**

The bipartite target is `ell(G) >= 2 tau(G)+1`, where `ell(G)` is the maximum
number of edges in a spanning linear forest.

1. If `tau(G)=0`, then connected nontrivial `G` is a forest with an edge. That
   edge and all remaining vertices as trivial paths give `ell(G)>=1`, exactly
   the required bound.

2. Assume `tau(G)>=1` and choose a minimum FVS `S`. Minimality gives hereditary
   tightness

       tau(G[H union X]) = |X| for every X subseteq S.                 (HT)

   The upper bound is immediate because deleting `X` leaves the forest `H`.
   For the lower bound, an FVS `D` of `G[H union X]` with `|D|<|X|` would make
   `(S\X) union D` an FVS of `G` smaller than `S`.

3. There is an edge of `H`. Otherwise, for any `s in S`, the graph
   `G[H union {s}]` would have edges only at `s`, hence would be a star forest
   with feedback number zero, contradicting (HT), which gives one.

4. Fix any `e in E(H)`. The proved rooted-forest bound converts (HT) into the
   generalized Hall inequalities

       rho(X) = sum_h min(c(h), deg_X(h)) >= 2|X|  for all X subseteq S.

   The max-flow/min-cut criterion therefore supplies an initial feasible
   selection. This feasibility is proved for every fixed `e`, although the
   final theorem needs only one.

5. **Lemma A's one job** is to show that the forced core is acyclic. Take any
   selected cycle `C`. If all its incidences were forced, `C` would itself be a
   cycle in the forced core. Therefore `C` contains at least one avoidable
   incidence, which is precisely the hypothesis under which Lemma B is stated.
   Lemma A does not construct a move and does not itself decrease cycles.

6. **Lemma B's one job** is to supply a CES toggle for a selected cycle that
   has an avoidable incidence. A CES toggle destroys the designated cycle and
   creates no selected cycle that was not already present. Hence it strictly
   decreases the nonnegative integer “number of selected cycles.” Repetition
   terminates at an acyclic feasible selection `J`. Lemma B is the descent
   step; Lemma A only licenses its application at every nonterminal state.

7. The fixed-edge parity lemma says `J union {e}` is acyclic iff `J` is. A
   cycle using `e=xy` would leave, after removing `e`, an `x-y` path consisting
   of alternating `H-S` incidence edges. Such a path has even length, whereas
   `x` and `y` are adjacent and therefore in opposite bipartition classes, so
   every `x-y` path in bipartite `G` has odd length. Also, `e` cannot belong to
   a selected-incidence cycle.

8. In `J union {e}`, every `s` has degree exactly two; every ordinary `H`
   vertex has degree at most two; and `x,y` have selected load at most one, so
   adding `e` still leaves degree at most two. An acyclic maximum-degree-two
   graph is a disjoint union of paths. It spans `S union H=V(G)` and contains
   the `2|S|` selected incidences plus `e`, so

       ell(G) >= 2|S|+1 = 2 tau(G)+1.

Thus Lemma A plus Lemma B is a sufficient mechanism for the bipartite theorem.
The statement actually needed is the weaker existential target F2: for some
fixed `e in E(H)`, an acyclic feasible selection exists. Initial feasibility
for every `e` and the previously checked F2-ALL form are stronger auxiliary
facts, not a change to Theorem 3.13's quantifier.

## 2. Why Hall feasibility cannot prove Lemma A

**Status: MATHEMATICALLY PROVED.**

For `m>=3`, let `S={s_0,...,s_(m-1)}` and
`Q={q_0,...,q_(m-1)}`, with indices modulo `m`, and give `s_i` exactly the two
neighbours `q_i,q_(i+1)`. Give every `q_i` capacity two. To put this into the
disconnected Lemma A° model, add a disjoint `H`-edge `xy`; its endpoints
have capacity one and no `S`-incidences. The induced graph on `H=Q union {x,y}`
is a forest.

For every `X subseteq S`, each `q_i` has `deg_X(q_i)<=2`, so truncation at
capacity two does nothing. Double-counting incidences gives

    rho(X) = sum_i deg_X(q_i) = sum_(s in X) deg_Q(s) = 2|X|.

Every Hall inequality is therefore met with equality. Nevertheless every
`s_i` has only two available incidences and demand two, so the unique feasible
selection uses all `2m` incidence edges. Its forced core is the alternating
cycle

    s_0-q_1-s_1-q_2-...-s_(m-1)-q_0-s_0.

The missing hypothesis is hereditary FVS tightness. At `X=S`, the incidence
graph is one cycle (plus the disjoint edge `xy`), so deleting one vertex breaks
all cycles:

    tau(G[H union S]) = 1 < m = |S|.

Thus generalized Hall feasibility, F1, submodularity, and the tight-set lattice
can coexist with a cyclic forced core. Any proof of Lemma A must use the forest
geometry encoded by (HT), not only the flow layer.

## 3. Warning witnesses and the strategies they kill

**Status: COMPUTATIONALLY VERIFIED.** I ran

    python3 work/wcheck.py tools/witnesses/O-56.json \
      tools/witnesses/O-63.json tools/witnesses/O-64.json

The checker independently enumerates all feasible selections, intersects them
to get the forced core, enumerates all Hall-tight sets and canonical carriers,
and brute-forces `tau(G[H union X])` for every `X subseteq S`. It reproduced
selection counts `1,6,1`, forced-core cycle rank one in each witness, and
`tau(G[H union S])=2,3,2` versus `|S|=4,5,3`. Hence none is a Lemma A
counterexample: every one deliberately lacks the minimum-FVS/hereditary-
tightness hypothesis. They only falsify local proof strategies.

### O-56: P-localization and the degree-two/single-blocker seed

**Status: COMPUTATIONALLY VERIFIED.** Here `P={0,1}` and `Q={4,5}`. Vertices
`2` and `3` are rigid: they select `{6,7}` and `{6,8}`, saturating the
capacity-two vertex `6`. The cycle vertices `0,1`, each adjacent to `4,5,6`,
are therefore forced onto `4,5`; the unique selection contains the forced
4-cycle `0-4-1-5-0`.

The canonical carrier at `0` is `A_0={0,2,3}` and its puncture is
`B_0={2,3}`. The set `B_0` is Hall-tight, but deleting vertex `6` makes
`G[H union B_0]` a forest, so `tau=1<2`. In contrast, the cycle side `P` is
hereditarily tight. The contradiction is therefore disjoint from `P`; O-56
falsifies the proposed universal localization of the hereditary violation to
`P` or `G[H union P]`.

It is also the positive model for the proved single-blocker subcase. With
external neighbour `h=6`, every vertex of `U_h=N(h) intersect B_0={2,3}` has
only one non-`h` neighbour. The quotient after removing `h` is acyclic and the
one-vertex blocker `{6}` witnesses the strict FVS inequality. What is not
licensed is promoting this degree-two geometry to every carrier puncture.

### O-63: the degree-two normal form and private-cycle charging

**Status: COMPUTATIONALLY VERIFIED.** Vertices `u,a,b` each see exactly
`h,w,z`; their combined demand equals the total capacity six of those three
vertices, so they saturate all of them. Vertex `s` cannot use its third
neighbour `h` and is forced onto `q1,q2`; `t` is rigid on `q1,q2`. This forces
the cycle `s-q1-t-q2-s`. There are six feasible selections because the six
incidences from `u,a,b` may be distributed among `h,w,z` subject to load two.

The canonical data are

    A_s={s,u,a,b},  B_s=U_h={u,a,b}.

All three puncture vertices have incidence degree three, immediately
falsifying “every puncture vertex has degree two.” Removing `h` does not make
the augmented forest quotient acyclic: `w` and `z` lie in the same component
of `H-h`, so every auxiliary attaches twice to that component. Each resulting
`h`-avoiding cycle uses the same `H` path between `w` and `z`; the cycles are
not separately chargeable “private” cycles. Consequently the whole puncture
needs only a size-two blocker, for example `{h,w}`, and
`tau(G[H union B_s])=2<3`, while every proper subset of `B_s` is tight.

This is the exact correction to the naive private-cycle route: high incidence
degree alone does not give disjoint or independently chargeable cycles. The
component-level augmented quotient, including parallel attachments and any
edges inside the tested `S`-set, is the correct object.

Scope note: the JSON's “first inclusion-minimal violation” is correct *within
`B_s`*. It is not the first violation in the full subset lattice: the
independent checker also finds global size-two violations such as `{a,s}`.
That documentation mismatch does not alter the degree/private-cycle
falsifications or the puncture calculation.

### O-64: B_s-localization and the capacity-one branch

**Status: COMPUTATIONALLY VERIFIED.** The distinguished edge is `e=hy`, so
`c(h)=1`. Vertex `u` is rigid on `{h,w}` and alone saturates `h`; this forces
`s` off `h` and onto `q1,q2`, while `t` is rigid there. The unique feasible
selection contains the forced cycle `s-q1-t-q2-s`.

Now `A_s={s,u}` and `B_s={u}` are Hall-tight, but

    tau(G[H union B_s]) = 1 = |B_s|.

Indeed `u-h-y-w-u` is a cycle requiring one deletion. Thus the puncture is
hereditarily clean and the unique selection offers no exchange. The violation
instead occurs on `P={s,t}`, where deleting `q1` gives
`tau(G[H union P])=1<2`. This falsifies universal `B_s`-localization and shows
that the capacity-one and capacity-two external-neighbour branches cannot be
identified. Together O-56 and O-64 also show that neither `P` nor `B_s` is a
universal localizer.

## 4. T_F normalization: statement, derivation, and license

**Status: MATHEMATICALLY PROVED.** ATTACK.md calls this paper Lemma 4.7; after
the carrier–cycle separation insertion, the current v2 paper numbers it Lemma
4.8. The statement is the same.

Assume a Lemma A° instance has a forced-core cycle `F` with `S`-side
`P`. For each `s in P`, let `A_s` be the canonical carrier: the unique minimum
Hall-tight set containing `s`, which exposes both forced incidences of `F` at
`s`. Define

    T_F = union_(s in P) A_s,
    G'  = G[H union T_F],
    S'  = T_F,

with the same `H`, distinguished edge, and capacities.

The conclusions follow in four steps.

1. For every `X subseteq T_F`, the graphs `G'[H union X]` and
   `G[H union X]` are literally the same induced graph. Original hereditary
   tightness therefore gives `tau(G'[H union X])=|X|`.

2. Taking `X=T_F` gives `tau(G')=|T_F|`. Deleting `T_F` leaves `H`, a forest,
   so `T_F` is an FVS and the equality makes it a minimum FVS of `G'`.

3. For `X subseteq T_F`, `rho(X)` depends only on the `X-H` incidences and the
   capacities, all unchanged by restriction. The original Hall inequalities
   restrict to all subsets of `T_F`, so the restricted incidence model is
   feasible.

4. Forcedness is not assumed monotone under deleting demand vertices from
   `S\T_F`; such a deletion may create new feasible selections. Instead each
   cycle incidence is forced again from F1. Its carrier `A_s` lies inside
   `T_F`, has the same `rho` value and the same degrees at its exposed endpoint,
   so it remains tight and exposing in the restricted system. F1 then forces
   that incidence afresh. Every edge of `F` remains in the forced core of
   `G'`.

Therefore every counterexample restricts to another counterexample with
`S'=T_F`. A minimal counterexample may be studied under the normalization

    S = T_F = union_(s in P) A_s.

What this licenses is exact: every remaining `S`-vertex lies in at least one
carrier belonging to a forced-cycle vertex, so irrelevant demand vertices may
be removed and the entire carrier family covers `S`. Canonical carriers give
the smallest such normalized set and preserve the downstream puncture and
lattice statements.

It does **not** license any of the following: that `P` is Hall-tight; that
`P`, one puncture, or `T_F` contains a proper hereditary violation; that
forcedness survives restriction by monotonicity; or that the restricted graph
remains connected. The last point is why the normalization is stated for
Lemma A° without connectedness. After normalization, saying only that a
violation lies in `T_F` says no more than that it lies somewhere in `S`.

## Gauntlet outcome

**Status: MATHEMATICALLY PROVED / COMPLETED.** The reduction, Hall-only
counterexample, witness mechanisms, and normalization have been derived with
their quantifiers and limitations intact. The warning certificates contacted
the oracle and the shipped tool hashes passed `17/17`. I may proceed to one
new primary target under ATTACK.md Step 3.
