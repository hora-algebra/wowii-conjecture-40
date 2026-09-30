# Comprehension and scope — 2026-09-30

This record is retrospective to an already-written candidate proof. It is not
a claim that the original exploration followed the repository's prospective
gauntlet or preregistration protocol. No new theorem is assumed here.

## Reduction

Write tau=n-f, o=n-b, ell=n-p. Multiplying the conjecture's integer inequality
by two gives ell+o >= 2 tau+1. In a bipartite graph o=0. For tau=0 a connected
nontrivial graph has an edge, giving ell>=1. Otherwise take a minimum FVS S.
For X contained in S, tau(G[H union X])=|X|: any smaller deletion, together
with S minus X, would contradict minimality of S. H must have an edge,
since otherwise adjoining a single s gives a star and violates that equality.

For e=xy in H, capacities are 1 at x,y and 2 elsewhere. The source-to-S arcs
have capacity 2, incidence arcs capacity 1, and H-to-sink arcs capacity c(h).
The minimum cut with source-side S-set X has capacity
2(|S|-|X|)+sum_h min(c(h),d_X(h)). Thus Hall inequalities give a selection.
The forest extension estimate and hereditary minimum-FVS equality establish
those inequalities on each original bipartition side; the ranks add across
the sides. Lemma A implies every selected cycle has an avoidable edge. A
valid cycle-erasing descent statement would then strictly decrease the number
of selected cycles until none remain. Lemma A alone supplies no such descent.
Adding e to an acyclic selection cannot create a cycle: an incidence-only
x-y path has even length, whereas x and y are in opposite original classes.
The resulting spanning forest has maximum degree 2 and 2|S|+1 edges, proving
the bipartite bound. General coefficient-one lifting remains separate.

## Hall without hereditary tightness

On an alternating cycle with m>=2 S-vertices, each S-vertex has precisely
two neighbours and all H-capacities are 2. Every feasible selection must
contain every edge; Hall has equality for every S-subset, but the forced core
is cyclic. The graph has tau=1<m. A disjoint K2 may carry the distinguished
edge without changing this example. Hence a proof must use minimum-FVS
geometry, not only rank submodularity or tight-set closure.

## Published negative controls

The unchanged upstream oracle was run by review/replay_witnesses.py.
O-56 has 1 selection, 8 forced edges and tau=2<4=|S|. The auxiliary pair
{2,3}, disjoint from the cycle's S-side, has tau=1; deleting their shared
neighbour 6 breaks its cycles. Thus locating the violation on P is invalid.
O-63 has 6 selections and 4 forced edges. Its three auxiliary vertices each
see h,w,z and collectively saturate them. This forces the cycle vertices
onto q1,q2. The full auxiliary triple has tau=2<3, whereas its pairs have
tau=2. Their incidence degrees are 3, and the common hub structure defeats
the claimed private-cycle localization. The triple is minimal within the
punctured carrier, not necessarily among all subsets of S.
O-64 has 1 selection and 6 forced edges. Vertex u saturates the capacity-1
h, forcing s away from h. The punctured carrier {u} has tau=1, but the cycle
pair {s,t} has tau=1<2. This defeats punctured-carrier localization.
These examples fail the theorem's premise; they test that the checker can
detect cyclic forced cores and that no false localization is silently used.

## Normalization

For a hypothetical forced cycle with S-side P, let A_s be the intersection
of all Hall-tight sets containing s. Tight sets are closed under intersection
and union by rank submodularity and Hall's lower bound. Each A_s exposes
both forced incidences at s, since taking a subset cannot increase the
degree at their H-endpoints. Let T be their union. Restrict G to H union T.
Deleting T leaves H, and hereditary minimality implies tau=|T|. Incidence
ranks of subsets of T are unchanged, so Hall feasibility and tightness of
each A_s persist. Its exposing condition persists as well, hence the cycle
is still forced by Hall after deleting each of its incidences. This last
argument is necessary: forcedness does not persist under arbitrary demand
restriction. Normalization permits S=T, but does not locate a violation
inside P, one carrier, or one punctured carrier. Connectedness may be lost.

## Review window

The initial packaging/reproduction window is one hour, renewable if needed.
The pre-existing proof and exploratory results are labelled retrospective.
Subsequent new scans will record their exact checker hash and universe before
execution. No environmental blindness or human review is claimed.
