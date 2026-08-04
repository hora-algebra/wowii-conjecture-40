# Blind proof derivations

Recorded before opening `LEMMA-A-CARRIER.md` section 1.1 or the corresponding
proofs in `ATTEMPT_REPORT.md`.

## L1

Let the edge-containing components of bipartite `B` have bipartitions
`(L_i,R_i)`.  In each such component, take the larger bipartition class and
one vertex of the smaller class.  The induced subgraph is a star plus isolated
vertices, hence a forest, and has at least `ceil(n_i/2)+1` vertices.  Take every
isolated vertex of `B` as well.  The disjoint union remains an induced forest.
The sum of the componentwise ceilings is at least the ceiling of the total, so

`f(B) >= ceil(|B|/2) + c_e(B)`.

## L2

Let `T` be a minimum OCT, put `B=G-T`, and write `c_e=c_e(B)`.  If
`p(G) <= 2c_e-1`, then

`ell(G)=|B|+|T|-p(G) >= |B|+|T|-2c_e+1`.

By L1,

`tau(B)=|B|-f(B) <= floor(|B|/2)-c_e`,

so `2tau(B) <= |B|-2c_e`.  Substitution gives

`ell(G) >= 2tau(G-T)+|T|+1`,

which is LIFT-A for this minimum OCT.

## Lemma CS

Let `F=s_1q_1...s_mq_m` be a forced-core cycle, `P` and `Q` its two sides,
`B_s=A_s-{s}`, and `U=union_{s in P} B_s`.  Each `B_s` is tight and tight sets
are closed under union, hence `U` is tight.  Tight-set saturation says that in
every feasible selection the selected load from `U` at every `h` is
`min(c(h),deg_U(h))`.

Every cycle vertex `s in P` has its two cycle incidences forced.  Its demand is
two, so those are exactly its selected incidences in every feasible selection.
The cycle's `H`-vertices have capacity two (a capacity-one endpoint cannot lie
on a selected cycle).  If `s in P-U`, one unit of capacity at either forced end
is consumed outside `U`.  Saturation therefore gives
`deg_U(q)<=c(q)-1=1`, proving (a).  If both cycle neighbors of `q_i` lie in
`P-U`, both capacity units are consumed outside `U`, so saturation gives
`deg_U(q_i)=0`, proving (b).  If `P intersect U` is empty, (b) applies at every
`q_i`, proving (c).

For (d), fix `R subseteq P-U`.  At every non-cycle neighbor `h` of
`s in P-U`, punctured-carrier oversubscription gives
`deg_{B_s}(h)>=c(h)`, hence already `deg_U(h)>=c(h)`; adding `s` cannot increase
the `rho` term there.  At a cycle vertex `q`, if one member of `R` is incident,
(a) leaves exactly the needed unit of unsaturated capacity; if both are
incident, (b) leaves both units.  Thus adding `R` to `U` increases `rho` by
exactly the two forced cycle incidences per member of `R`:

`rho(U union R)=rho(U)+2|R|=2|U|+2|R|=2|U union R|`.

Therefore `U union R` is tight.

## Post-blind comparison

- L1: same componentwise construction.  The independent derivation explicitly
  states the isolated-component and ceiling-summation steps; the branch proof's
  "union over components" covers them.  No gap.
- L2: the inequalities are algebraically identical; the branch compresses them
  into one chain.  No gap.
- Lemma CS: the branch proves (a) and (d) by making both `U` and `P union U`
  tight and telescoping submodular marginals, then obtains (b).  The independent
  derivation instead uses tight-set saturation for (a)/(b) and carrier
  oversubscription for (d).  Both routes justify every marginal and the
  capacity-two use at cycle vertices.  No gap.
