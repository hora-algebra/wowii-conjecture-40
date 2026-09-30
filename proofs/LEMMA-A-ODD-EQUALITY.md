# A proposed proof of Lemma A° by odd equality structure

**Status: MATHEMATICALLY PROVED (author-side proof claim, submitted for review),
not LEAN-FORMALIZED or independently certified.** No change to the repository's
accepted status is requested. This does not prove F2 or WOWII Conjecture 40.

This note was developed and written using OpenAI Codex, with AI proof reviews
and executable finite checks. No human review or environmentally blind
certification is claimed. The proof below is the evidence; AI concurrence and
finite computation are not substitutes for it.

## Statement and attribution

Let G be a finite simple bipartite graph, S any minimum-cardinality feedback
vertex set, H=G-S, and xy any edge of H. Put c(x)=c(y)=1 and c(h)=2 otherwise.
A selection takes exactly two S-H edges at each s in S and at most c(h) at
h in H. Such selections exist, and their common edges form a forest.
Connectedness and an extremal choice among minimum FVSs are not required.

The question, hereditary minimality, capacitated Hall criterion, tight-set
lattice and canonical carriers come from Chris Ozols / cozuya,
[proof collection](https://github.com/cozuya/wowii-conjecture-40/blob/290d1b28fd70038824fbba736e1bf47dd83aed01/proofs/PROOFS.md)
and [carrier notes](https://github.com/cozuya/wowii-conjecture-40/blob/290d1b28fd70038824fbba736e1bf47dd83aed01/LEMMA-A-CARRIER.md).
See also [MathOverflow 513887](https://mathoverflow.net/questions/513887).
The neighbourhood deletion argument in (4) already appears in
[attempt 064c, Theorem 6(iv)](https://github.com/cozuya/wowii-conjecture-40/blob/4ca6378dc72d08ad9ca1af4ccef7145704de79cf/PROOFS-SAFE2-064c.md).
The basic deletion bound is closely related to C5b in the proof collection.
Neither is claimed as new here. The contribution proposed for review is the
odd equality structure combined with minimal carriers.
Those mathematical write-ups are CC BY 4.0. This note restates the needed
framework and supplies an odd-equality argument; it does not claim global
priority or endorsement by the source author. This note is offered under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) to the extent of
applicable rights. The Japanese companion contains two further corollaries.

## 1. A deletion bound and its equality case

For every X contained in S,

$$\tau(G[H\cup X])=|X|. \tag{1}$$

Indeed a smaller deletion, combined with S minus X, would contradict minimum
cardinality of S.

More generally let K consist of a forest H and an independent set X. Define
U={h: d_X(h)>=2}, L={h: d_X(h)=1}, u=|U|, l=|L| and
rho0=2u+l. For a in X put d(a)=|N(a) intersect L| and B={a:d(a)>=2}, b=|B|.
Deleting U union B leaves every remaining X-vertex of degree at most one,
so the remaining graph is a forest. Consequently

$$\tau(K)\le u+b\le\lfloor\rho_0/2\rfloor. \tag{2}$$

If U is nonempty and rho0 is even, this improves to

$$\tau(K)\le\rho_0/2-1. \tag{3}$$

If 2b<l, parity proves this. If 2b=l, all vertices outside B have d=0.
Keep one vertex v of U and delete B and U minus v. Each surviving X-vertex
then has degree at most one, proving (3).

Suppose now tau(K)=|X| and rho0=2|X|+1, with U nonempty. Equation (2) forces
|X|=u+b and l=2b+1. The sum of the d(a)'s is l. Either one B-vertex has d=3,
all other B-vertices have d=2 and all outside B have d=0; or all B-vertices
have d=2 and exactly one vertex t outside B has d=1, all others having d=0.
The first case is contradicted by the same deletion retaining one U-vertex.
Thus write X as B, {t}, Z, with d on these parts respectively 2,1,0.
Then |Z|=u-1. Let z be t's unique L-neighbour. For each v in U, delete B
and U minus v. Only t can have degree two among surviving X-vertices, and
its possible neighbours are z,v. The deletion has size |X|-1, so a cycle
must remain. Hence t is adjacent to every vertex of U.

For every nonempty W contained in Z,

$$|N_U(W)|\ge |W|+1. \tag{4}$$

The neighbourhood is nonempty, since otherwise isolated W could be retained
while deleting fewer than |X| vertices of X. Choose v in that neighbourhood
and delete B, t, Z minus W, and N_U(W) minus v. The survivors in W have degree
at most one, so this is a feedback vertex set. Its size is
b+u-1-|W|+|N_U(W)|. Comparison with tau(K)=b+u proves (4).

## 2. Hall and canonical carriers

For A contained in S put rho(A)=sum_h min(c(h),d_A(h)). Integer max-flow
with capacities 2 from source to S, 1 on incidences, and c(h) from H to sink
shows that selections exist exactly when rho(A)>=2|A| for every A.

To prove this inequality, first take A in one original bipartition class.
If U is empty, (1) on singletons gives each a at least two H-neighbours and
rho(A)=rho0(A)>=2|A|. Otherwise (1)--(3) give rho0(A)>=2|A|+1. Only one
endpoint of xy can neighbour A, so reducing its capacity loses at most one.
For arbitrary A the ranks add across its two original bipartition classes.

Call A tight when rho(A)=2|A|. An edge sh is forced exactly when some tight
A contains s and d_A(h)<=c(h): removing sh decreases rho(A) by one exactly
under that degree condition, and destroys feasibility exactly when Hall is
violated. The submodularity of rho and Hall's lower bound show that tight
sets are closed under unions and intersections. For a vertex s incident to
a forced edge, let A_s be the intersection of all tight sets containing s.
It is tight, minimal, and exposes every forced edge at s, because passing to
a subset cannot increase d_A(h). Splitting ranks across the original
bipartition shows that A_s lies wholly in s's class.

In every selection, tightness of A also forces the number of edges from A
at each h to be exactly min(c(h),d_A(h)): the upper bounds sum to the exact
total demand 2|A|.

## 3. Excluding a forced cycle

Suppose a forced cycle has S-side P and H-side Q. All P lie in one original
bipartition class and every q has capacity two. Set X=union of A_s over s
in P. This is a tight independent set. Define U,L relative to X. Since each
q has two neighbours in P, Q is contained in U and u>=2. Let r be the endpoint
of xy opposite X's class. Tightness gives rho0(X)=2|X| or 2|X|+1. Equation
(3) excludes the former. Thus r belongs to U and the odd equality case
applies: X=B disjoint union {t} disjoint union Z, |Z|=u-1, and t sees all U.

Tight saturation forces every X-L edge into every selection. Vertices of B
use both edges on L, and t uses one edge on L. None can lie on the proposed
cycle, whose two incidences at each P-vertex lead into U. Hence P is a subset
of Z.

Fix s in P. For D=A_s intersect B, removing D from A_s removes at least
2|D| rank contribution, from its distinct private L-neighbours. Hall forces
rho(A_s minus D)=2|A_s minus D|. Since this set still contains s, carrier
minimality forces D empty. Thus A_s is contained in Z union {t}.

If t belongs to A_s, put W=A_s minus {t}. It is nonempty since it contains s.
As t sees all U and its unique L-neighbour, whereas Z sees only U, exactly

$$\rho(A_s)=u+1+|N_U(W)|-\mathbf{1}_{r\in N_U(W)}.$$

Tightness and (4) yield 2|W|+2>=u+|W|+1, so |W|>=u-1=|Z| and W=Z.
At either cycle neighbour q of s, A_s then contains both P-neighbours of q
and t, three distinct vertices. This contradicts the exposing condition
d_{A_s}(q)<=c(q)=2. Therefore t belongs to no A_s for s in P, contrary to
t belonging to their union X. There is no forced cycle.

The last step uses the union of carriers, not localization of a hereditary
violation within P or within one punctured carrier. In particular it does
not invoke the localization claims refuted by O-56, O-63 and O-64.
