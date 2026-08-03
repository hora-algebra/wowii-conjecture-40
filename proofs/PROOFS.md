# WOWII Graph Conjecture 40 — bipartite core: proof document

Revised 2026-07-30 after review. Honest grading throughout: PROVED lemmas are
written out; machine-verified lemmas that now have written proofs are graded PROVED
with the machine check as regression evidence; the two genuinely OPEN cores and the
provisional reductions are stated precisely.

---
## A. Main theorem and notation
Conjecture 40 (Lean, connected nontrivial G): f(G) >= ceil((pathCover(G)+b(G)+1)/2),
f = largestInducedForestSize, b = largestInducedBipartiteSubgraphSize,
pathCover = min vertex-disjoint simple paths covering V.
Write tau = n-f (min feedback vertex set), o = n-b (min odd-cycle transversal),
ell = n-pathCover (max edges of a spanning linear forest).

For a set S of vertices, G[H u X] denotes the subgraph induced on H u X where
H = G - S. Given a min FVS S, H is a forest (see B). The incidence-selection model:
each s in S has demand 2; each h in H has capacity c(h)=2, except the two endpoints
x,y of a fixed edge e=(x,y) of H have c(x)=c(y)=1. A feasible selection J assigns to
each s two H-incidences respecting capacities. A selected cycle is a cyclic
component of the incidence graph J (equivalently of J u {e}, by Lemma 0).

CES (canonical definition, used throughout). A move (toggle from selection J to J') is
CES ("cycle-erasing") for a DESIGNATED selected cycle C when it (i) destroys C (C is not a
selected cycle of J'), AND (ii) creates no selected cycle absent from J (every selected
cycle of J' was already a selected cycle of J). This is the SEMANTIC definition (compare
the fresh cycle sets before/after). It IMPLIES a strict decrease in selected-cycle count
(C is removed and nothing new appears). Note: CES is NOT defined merely as "strictly fewer
selected cycles" — although strict decrease alone would already suffice for the descent's
termination (C8).

---
## B. Reductions and exact remaining reduction gaps
(B1) ALGEBRAIC EQUIVALENCE (PROVED; verified 995/995 connected graphs n<=7):
Conjecture 40 <=> ell + o >= 2*tau + 1. For bipartite G, o = 0, so the target is
ell >= 2*tau + 1.
NOTE (keep distinct — margin definition). Define the linear margin
  mu(G) := ell(G) + o(G) - (2*tau(G) + 1).
Then: the conjecture is mu(G) >= 0; LINEAR TIGHTNESS means mu(G) = 0. The ORIGINAL theorem
is a CEILING inequality f >= ceil((pathCover+b+1)/2); because of the ceiling's parity,
EQUALITY in the original ceiling statement can correspond to EITHER mu = 0 OR mu = 1. So
"ceiling-equality" and "linear tightness (mu=0)" are distinct notions and must NOT be
conflated.

(B2) H IS A FOREST because S is an FVS (deleting an FVS leaves a forest). Minimality
of S is NOT needed for this; it is needed for hereditary tightness (C2).

(B3) F2 => BIPARTITE TARGET — PROVED (conditional only on proving F2 itself).
 Case tau=0: G is a connected nontrivial forest, so it has an edge; that edge plus
 all other vertices as isolated vertices is a spanning linear forest, giving
 ell >= 1 = 2*tau+1.
 Case tau>=1: let S be a min FVS (nonempty). E(H) is NONEMPTY: suppose E(H)=empty;
 take X={s} for any s in S. Since H has no edges, G[H u {s}] has edges only at s, a
 star forest, so tau(G[H u {s}]) = 0. But hereditary FVS tightness (C2) gives
 tau(G[H u {s}]) = |{s}| = 1 — contradiction. Hence E(H) != empty, so a fixed edge
 e in H exists. F2 then produces a spanning linear forest with degree 2 at every s
 in S, containing e, no other H-edge, no S-S edge — exactly 2|S|+1 edges — so
 ell >= 2|S|+1 = 2*tau+1. []
 Therefore F2 implies the full bipartite target; the distinguished-edge existence
 issue is CLOSED.

(B3') F2 — STANDALONE STATEMENT (complete quantifiers). For a connected nontrivial
bipartite G with tau>=1, min FVS S, H=G-S a forest: THERE EXISTS a distinguished edge
e in E(H) and an ACYCLIC feasible incidence selection J_e (each s in S incident to exactly
2 selected incidences; capacities c=2 except c=1 on e's two endpoints; J_e u {e} acyclic)
whose spanning linear forest has 2|S|+1 edges. QUANTIFIER DISCIPLINE:
 - the final bipartite theorem (B3) needs EXISTENCE for ONE distinguished e in E(H)
  (some e suffices; it is NOT required for every e);
 - C5b proves INITIAL feasibility (a feasible selection exists) for EVERY distinguished e
  (universal), which is strictly stronger than needed and is not the target quantifier;
 - the currently intended Lemma-A + Lemma-B (cycle-erasing descent) route seeks an ACYCLIC
  feasible selection for the FIXED e (one e), the existence quantifier F2 actually needs.
Do NOT silently upgrade F2's required "exists e" to "for all e"; the universal C5b result
is a stronger auxiliary, not the theorem.

(B4) REMAINING REDUCTION GAP (single, stated separately):
 GENERAL -> BIPARTITE (via the odd-cycle-transversal parameter o): the desired
 coefficient-1 general theorem ell + o >= 2tau + 1 is genuinely PROVISIONAL and unproved.

(B5) GENERAL -> BIPARTITE, WEAKENED FORM — MATHEMATICALLY PROVED CONDITIONAL ON THE
BIPARTITE THEOREM (this is NOT the desired coefficient-1 general theorem; it has a 2o term).
STATEMENT: assuming the bipartite theorem (ell(B) >= 2tau(B)+1 for every connected
nontrivial bipartite B) holds for all connected nontrivial bipartite graphs, then for every
connected nontrivial graph G,
  ell(G) + 2*o(G) >= 2*tau(G) + 1.
PROOF. Choose a minimum odd-cycle transversal T, |T| = o(G); B := G - T is (a maximum
induced) bipartite subgraph.
 (i) ell(G) >= ell(B) (a spanning linear forest of B extends to one of G by adding the
   T-vertices as isolated vertices).
 (ii) tau(B) >= tau(G) - o (deleting the o vertices of T lowers the min FVS by at most o).
 (iii) Apply the bipartite theorem COMPONENTWISE to B: summing ell(B_i) >= 2tau(B_i)+1
    over the components B_i of B that contain an edge (edgeless components have
    ell=0=2tau) gives ell(B) >= 2tau(B) + c_e, where c_e = number of components of B
    containing an edge.
 (iv) c_e >= 1: B (a MAXIMUM induced bipartite subgraph) is NOT edgeless. Suppose it were;
    then b(G) = alpha(G) (independence number). Take a maximum independent set I; since
    G is connected and nontrivial there is a vertex v outside I with a neighbour in I,
    and I u {v} induces a star, which is bipartite, of size |I|+1 > b(G) — contradicting
    maximality of b(G). So B has an edge and c_e >= 1.
 Combining: ell(G) >= ell(B) >= 2tau(B) + c_e >= 2(tau(G)-o) + c_e = 2tau(G) - 2o + c_e,
 hence ell(G) + 2o >= 2tau(G) + c_e >= 2tau(G) + 1. []
 This is weaker than the target (coefficient 2 on o, not 1). Reattachment / lifting /
 single-vertex-induction routes toward the coefficient-1 theorem are NOT yet project
 targets (unsupported).

---
## C. Fully proved lemmas

### C1. Algebraic equivalence — PROVED (see B1).

### C2. Hereditary FVS tightness — PROVED
Claim: for every X subseteq S, tau(G[H u X]) = |X|.
Proof: X is an FVS of G[H u X] (deleting X leaves H, a forest), so
tau(G[H u X]) <= |X|. Conversely suppose D is an FVS of G[H u X] with |D| < |X|.
Then (S \ X) u D is an FVS of G: deleting it leaves a subgraph of G[H u X] - D,
which is a forest. Its size is |S| - |X| + |D| < |S|, contradicting minimality of S.
Hence tau(G[H u X]) = |X|. []
This is the load-bearing input for Lemma A.

### C3. Fixed-edge parity (Lemma 0) — PROVED
The fixed edge e=(x,y) lies on no selected cycle. If J u {e} had a cycle through e,
deleting e leaves an x-to-y path of S-H incidence edges, which alternates H,S,H,...
and so has EVEN length; but x,y are adjacent in bipartite G, hence in opposite
parts, so every x-y path has ODD length. Contradiction. Thus selected cycles lie in
J, and J u {e} is acyclic iff J is. []

### C4. Residual augmentation (Lemma 1) — PROVED (repaired flow proof; regression-checked ~2.19M releases)
Setup: J a feasible selection, a=(s,h) a selected incidence. Work in the flow network N of
C5 (source sigma; arcs sigma->s of capacity 2; incidence arcs s->h of capacity 1; arcs
h->sink of capacity c(h)). DELETE the arc a from N entirely; call the result N-a. J is a
value-2|S| integral flow in N. LITERAL DEFINITION of J-a: from J, delete ONE COMPLETE
UNIT-FLOW PATH sigma -> s -> h -> sink (the unit routed through the incidence arc a). Its
effect, arc by arc:
 - flow on sigma->s decreases from 2 to 1;
 - the incidence arc a=(s->h) is absent from N-a (carried 1 unit in J; carries none);
 - flow on h->sink decreases by 1;
 - EVERY OTHER arc flow is unchanged.
FLOW CONSERVATION check: at s, inflow (sigma->s) drops by 1 and outflow (s->h via a) drops
by 1, so net balance is preserved (s now has inflow 1 = outflow 1, its remaining selected
incidence); at h, inflow (s->h via a) drops by 1 and outflow (h->sink) drops by 1, so
balance is preserved. All other vertices are untouched. Hence J-a is a VALID integral flow
of value 2|S|-1 in N-a, in which sigma->s is the ONLY unsaturated source arc.
CLAIM: a feasible selection omitting a exists iff N-a admits a value-2|S| flow iff there is
a simple residual sigma-to-sink augmenting path in N-a from the deficient s.
Proof: a feasible selection omitting a IS a value-2|S| flow in N-a (it saturates every
sigma->s and never uses a). Conversely, by the ordinary augmenting-path theorem applied to
the flow J-a of value 2|S|-1, N-a admits a larger (value-2|S|) flow iff there is a simple
residual sigma-to-sink path; augmenting along it saturates sigma->s and yields an integral
value-2|S| flow = a feasible selection. Its incidence portion (strip the source/sink arcs)
is exactly the required alternating augmenting path from s to an H-vertex of residual
capacity. The released arc a is ABSENT from N-a, so it cannot be re-added by any residual
path. []
CONCLUSION: avoidable iff one-move avoidable (a is globally avoidable iff a single residual
augmentation in N-a omits it).
Corollary: R2x — the class "globally avoidable but admitting no one-move residual
augmentation" — is IMPOSSIBLE (empty). (The earlier symmetric-difference argument is
superseded by this flow proof; the ~2.19M-release check is regression evidence, not the
proof.)

### C5. Generalized Hall criterion and F1 — PROVED
Flow network N: a source sigma with arcs sigma->s of capacity 2 for each s in S;
each incidence edge as an arc s->h of capacity 1; arcs h->sink of capacity c(h) for
each h in H. An integral s-flow saturating every sigma->s arc corresponds exactly to
a feasible selection (each s sends 2 units, split over 2 distinct incidences by the
unit arc capacities; each h receives <= c(h)). Max feasible flow value <= 2|S|, with
equality iff a feasible selection exists.
For X subseteq S, rho(X) = sum_{h in H} min(c(h), deg_X(h)), delta(X)=rho(X)-2|X|.

GENERALIZED HALL — min-cut normalization (full detail): consider any sigma-sink cut
(A, B) with sigma in A, sink in B, and set X = S intersect A. The cut capacity is
the sum of forward arcs A->B:
 - source arcs sigma->s for s in S intersect B: 2 each, total 2(|S|-|X|);
 - incidence arcs s->h with s in A, h in B: only s in X can contribute (an s not in
  A carries no flow to a cut on its incidences); each such arc costs 1;
 - sink arcs h->sink with h in A: c(h) each.
For each h, its total contribution is minimized by placing h on the cheaper side:
 cost(h) = min( c(h) [put h in A, pay the sink arc], deg_X(h) [put h in B, pay the
 X-incidence arcs] ) = min(c(h), deg_X(h)).
Hence the minimum cut compatible with a given X has capacity
 2(|S|-|X|) + sum_h min(c(h), deg_X(h)) = 2|S| - 2|X| + rho(X) = 2|S| + delta(X),
and the global min cut is 2|S| + min_{X subseteq S} delta(X). By max-flow/min-cut,
max flow = min(2|S|, 2|S| + min_X delta(X)) = 2|S| iff min_X delta(X) >= 0, i.e. iff
rho(X) >= 2|X| for every X subseteq S. So a feasible selection exists iff the
generalized Hall inequality holds. []

### C5b. Rooted Forest Extension + feasibility prerequisite closed (NOT F2 itself)
ROOTED FOREST EXTENSION LEMMA. Let G be bipartite, H an induced forest, X an independent
set contained in one bipartition class. Fix an edge e=ab of H; give a,b capacity 1 and
every other H-vertex capacity 2. Write rho_e(X) = sum_{h in H} min(c_e(h), deg_X(h)). Then
  tau(G[H union X]) <= floor(rho_e(X)/2).
PROOF. Let r be the endpoint of e in the bipartition class OPPOSITE X; the other endpoint
lies in X's class, so has no X-neighbour. Thus r is the only e-endpoint that can have
X-neighbours (deg_X(r)>=0 allowed). Induct on k = #{h in H-{r} : deg_X(h) >= 2}.
 STEP (k>0): pick h in H-{r} with deg_X(h)>=2. h is neither endpoint of e (not r by
 choice; not the other endpoint, which has deg_X=0), so c_e(h)=2. Let K=G[H u X], K'=K-h.
 H-h is still a forest with e in it, so the lemma applies to K'; deleting h removes exactly
 min(2,deg_X(h))=2 from rho_e, so rho_e^{K'}(X)=rho_e^K(X)-2. If D is an FVS of K' then
 D u {h} is an FVS of K, so tau(K) <= 1+tau(K') <= 1+floor((rho_e^K(X)-2)/2)
 = floor(rho_e^K(X)/2). 
 BASE (k=0): every h in H-{r} has <=1 X-neighbour.
  CASE 1 (deg_X(r)<=1): every h (incl r) has <=1 X-neighbour, so each rho term equals
  deg_X(h) and rho_e(X)= total #(X-H incidences). Let D={x in X : deg_H(x)>=2}; each
  contributes >=2 incidences so 2|D| <= rho_e(X), |D| <= floor(rho_e(X)/2). In K-D every
  surviving X-vertex has degree <=1, and adding leaves/isolated vertices to the forest H
  keeps it a forest, so K-D is a forest. Thus tau(K) <= |D| <= floor(rho_e(X)/2).
  CASE 2 (deg_X(r)>=2): let m = #(X-to-(H-{r}) incidences); every non-root H-vertex has
  <=1 X-neighbour (contributes 1) and r contributes 1 (c_e(r)=1), so rho_e(X)=m+1. Let
  Q={x in X : deg_{H-{r}}(x)>=2}, q=|Q|; then 2q <= m.
   SUBCASE 2A (m >= 2q+1): D = Q u {r}. After deleting r, every surviving x outside Q has
   <=1 remaining H-neighbour, so K-D has all X-degrees <=1 and (H-r a forest) is a
   forest. |D|=q+1 <= floor((m+1)/2)=floor(rho_e(X)/2).
   SUBCASE 2B (m = 2q): then every x in Q has exactly two non-root incidences and every
   x in X-Q has zero, so D=Q makes every surviving X-vertex isolated or adjacent only to
   r (degree <=1); K-D is a forest. |D|=q=floor((2q+1)/2)=floor((m+1)/2)=floor(rho_e(X)/2). []
CONSEQUENCE (feasibility for every distinguished edge). Bipartition G = L u R; X_L=X∩L,
X_R=X∩R, both independent. Every h in H∩L is adjacent only to X_R and every h in H∩R only
to X_L, so the Hall-rank supports are disjoint and rho_e(X)=rho_e(X_L)+rho_e(X_R). If
rho_e(X) < 2|X|, some side (say X_L) has rho_e(X_L) < 2|X_L|; the lemma gives
tau(G[H u X_L]) <= floor(rho_e(X_L)/2) < |X_L|, contradicting hereditary FVS tightness
tau(G[H u X_L])=|X_L|. Hence rho_e(X) >= 2|X| for every X subseteq S and every fixed e in
E(H); by the generalized Hall criterion (C5) an INITIAL FEASIBLE SELECTION EXISTS FOR
EVERY DISTINGUISHED EDGE e. []
STATUS: MATHEMATICALLY PROVED, NOT LEAN-FORMALIZED. The fixed-edge feasibility prerequisite
of F2 is CLOSED, with the universal fixed-e quantifier valid. F2 itself remains OPEN
(acyclicity still requires Lemma A + Lemma B via descent). Computational checks are
REGRESSION EVIDENCE only: the bound tau <= floor(rho_e(X)/2) held on 3767 random (forest H,
independent X, fixed e) cases (0 violations, and the proof's explicit FVS construction
reproduced under the bipartite hypothesis, 0/5774); rho_e(X) >= 2|X| held for every
(X subseteq S, e in E(H)) over class-3 n<=8 (9,669 pairs) and n<=9 (54,935 pairs), 0
violations.

F1 (forced <=> tight-set-exposed): fix a max flow of value 2|S| (a feasible J). For
a=(s,h), deleting the arc a lowers rho(X) by exactly one iff s in X and
deg_X(h) <= c(h) (removing one X-incidence at h decreases min(c(h),deg_X(h)) iff h is
not over-subscribed by X). If a is forced, then deleting a admits no feasible flow,
so by the Hall criterion some X has rho_{N-a}(X) < 2|X|; since rho(X) >= 2|X| held, X
was tight (delta(X)=0) and deleting a dropped rho(X) by one, so s in X and
deg_X(h) <= c(h): X exposes a. Conversely, if a tight X exposes a, then in N-a the
set X has rho_{N-a}(X) = 2|X|-1 < 2|X|, so no feasible selection omits a: a is
forced. []
CANONICAL EXPOSING SET (matches the normalization above): for a forced a, run a max
flow in N-a (value 2|S|-1) and let A be the source side of the residual graph
(vertices reachable from sigma along arcs with residual capacity). Then
X_a = S intersect A is a tight set exposing a, and it is the inclusion-minimal such
set because the residual-reachable side is the unique minimal min-cut source side.
(Machine-verified n<=9, 0/104k failures, as regression.)

### C6. Tight-set lattice — PROVED
delta(X) = rho(X) - 2|X| is submodular (X -> min(c(h), deg_X(h)) is submodular per
h) and >= 0. If X, Y tight then 0 <= delta(X&Y) + delta(XuY) <= delta(X) + delta(Y)
= 0, so X&Y and XuY are tight. []

### C7. Quotient acyclicity (Lemma 2) — PROVED
For a residual toggle releasing a, let J0=J-a, O=removed selected edges, N=added
edges, R=J0-O; Jp = R u N. Quotient multigraph K: one node per component of R, one
edge per member of N.
Claim: K acyclic => the toggle creates no selected cycle absent from R.
Proof: let Z be a cycle of Jp that is not a cycle of R; then Z uses at least one
N-edge. Contract each component of R to a point: the R-subpaths of Z collapse, its
N-edges survive, so the image of Z is a nonempty closed trail in K. Every nonempty
closed trail in a multigraph contains a cycle (a loop if an N-edge has both ends in
one R-component; a 2-cycle from parallel N-edges; otherwise a longer cycle). Hence K
is cyclic. Contrapositive: K acyclic => no such Z. [] (Only this direction holds;
the converse is false. Machine check: 0 violations n<=10, as regression.)

### C8. Descent (Lemma 5) — PROVED
A CES toggle destroys the target cycle and creates none, so it strictly lowers the
number of selected cycle components; that count is a nonnegative integer, so
repeated CES toggles terminate in an acyclic feasible selection = the F2 spanning
linear forest. []

---
## D. Lemma A (no all-R3 cycle = forced core is a forest) — OPEN core
[FROZEN 2026-07-30: active proof effort STOPPED here (project decision); effort moved to
Lemma B. Human challenge sheet = LEMMA-A-CHALLENGE.md. Proved footholds below remain
valid; general Lemma A OPEN; the capacity-2-only tau(G[H u B_s])<=|B_s|-1 is parked,
neither proved nor refuted.]
EXACT STATEMENT: no selected cycle consists entirely of R3 (forced) edges;
equivalently the FORCED CORE (graph of all forced incidence edges) is acyclic.
EVIDENCE (provenance-labelled): n=11 instances 994,607; cyclic forced cores 0; maximum
forced-path length 8. COMPUTATIONALLY VERIFIED according to a preserved intermediate report;
the completion is INCOMPLETELY LEDGERED and is NOT independently reproducible from a
preserved completion log or checker artifact. This is NOT a hashed reproducible run.
(The proposed T_F normalization is NOT added here — it remains under independent
adversarial review.)
NECESSITY OF HEREDITARY TIGHTNESS: Hall feasibility + submodularity ALONE do not
suffice — the abstract even-cycle system (S_i ~ H_i,H_{i+1}, demand 2, cap 2) is
Hall-feasible yet its forced core is a cycle; there tau(G[H u S]) = 1 < |S|, i.e. it
VIOLATES hereditary tightness. So Lemma A is exactly:
  hereditary FVS tightness (C2) for all X subseteq S => forced core acyclic.
This implication is UNPROVED IN GENERAL. One substantial subcase is PROVED:

LEMMA A° (disconnected version). Let G be a finite simple bipartite graph, NOT necessarily
connected. Let S be a minimum FVS, H=G-S, e a fixed edge of H with the usual capacities
(c=2 except c=1 on e's endpoints). Then the forced incidence core is acyclic. Notes:
Lemma A° IMPLIES the connected version needed by F2 (a connected instance is a Lemma-A°
instance); all proved Lemma-A footholds (A-I, Tight-Set Saturation, Common Tight Carrier,
Punctured Tightness, single-blocker, Mhat_h) remain valid WITHOUT connectedness (none uses
it); the existing exhaustive n<=11 evidence covered CONNECTED instances only.

T_F NORMALIZATION LEMMA — PROVED (accepted in review). Suppose a Lemma-A° instance has a
forced-core cycle F with S-side P. For each s in P let A_s be its canonical minimum
Hall-tight carrier (C5b/Common Tight Carrier); set T_F = union_{s in P} A_s. Restrict to
  G' = G[H union T_F], S' = T_F, same H, distinguished edge e and capacities.
Then: (a) G'-S' = H; (b) S' is a minimum FVS of G'; (c) hereditary FVS tightness holds for
every X subseteq T_F; (d) the restricted incidence system is feasible; (e) every A_s
remains Hall-tight and exposes both forced F-edges at s; (f) every edge of F remains FORCED
in the restricted instance; (g) hence the forced core of the restricted instance still
contains F. THEREFORE a minimal counterexample to Lemma A° may be assumed to satisfy
S = T_F. 
PROOF NOTES (essential): restriction MAY create new feasible selections (removing S-vertices
outside T_F relaxes some capacities), so forcedness is NOT assumed monotone under
restriction; instead forcedness of each F-edge is RE-ESTABLISHED in G' from the SAME tight
exposing carrier A_s via F1 (A_s subseteq T_F stays Hall-tight and exposing in the
restricted flow network, so F1 gives forcedness afresh). Connectedness MAY be lost under
restriction — which is exactly why Lemma A° is stated without it. Canonicity of A_s is not
required for bare validity, but is retained because it yields the SMALLEST normalized set
T_F and is used by the downstream carrier lemmas. STATUS of the frozen witnesses: O-56 and
O-63 are already normalized (S = T_F); O-64 lies OUTSIDE the hereditary-tightness class
(its S is not a minimum FVS), so the normalization does not apply to it. []

LEMMA A-I (closed-H-neighbourhood subcase) — PROVED.
Suppose the forced core has a cycle F with S-side P and H-side Q (|P|=|Q|=m, each h in
Q has c(h)=2 and is saturated by its two F-vertices). If N_H(P) subseteq Q (every
H-neighbour of every cycle S-vertex lies on Q), then hereditary FVS tightness is
contradicted; hence no such F exists.
Proof: in G[H u P] pick any q0 in Q, set D = Q\{q0}, |D| = m-1. Any cycle of
G[H u P] - D lies in H-D (impossible: induced subgraph of the forest H) or contains
some s in P. But P is one bipartition class (F is an S-H incidence cycle), so within
G[H u P] a vertex s in P has neighbours only among its H-neighbours: edges inside P are
impossible, and edges from P to S\P are absent from G[H u P]. With N_H(s) subseteq Q,
after deleting Q\{q0} each s in P has degree <= 1 and lies on no cycle. So D is an FVS
of size |P|-1, giving tau(G[H u P]) <= |P|-1 < |P|, contradicting tau(G[H u P]) = |P|.
[] (Checked m=2..5; uses only F and N_H(P) subseteq Q, not why F's edges are forced.
Strengthened from the earlier N_G(P) subseteq Q form — S-neighbours never enter
G[H u P], so only H-neighbours need be on Q.)

Two supporting lemmas, both PROVED, verified on O-56 (0 violations):
 TIGHT-SET SATURATION. For a tight X (rho(X)=2|X|), every feasible J and every h in H,
  load_X^J(h) = min(c(h), deg_X(h))  (load_X^J(h) = #selected X-h incidences).
  Proof: load_X^J(h) <= min(c(h),deg_X(h)) termwise; sum_h load_X^J(h) = 2|X| =
  rho(X) = sum_h min(c(h),deg_X(h)); equal sums of termwise-dominated quantities force
  equality in every term. []
 EXPOSING-SET INTERNAL SATURATION. Let s in P, h an H-neighbour of s outside Q, and X
  any tight set containing s (e.g. a canonical exposing set of a forced F-edge at s).
  Then (s,h) is selected in no feasible J (s's demand 2 is exhausted by its two forced
  F-edges), and deg_X(h) >= c(h)+1: otherwise tight-set saturation gives
  load_X^J(h) = deg_X(h), forcing every X-h incidence — including (s,h) — to be
  selected, contradiction. Hence X already contains >= c(h) S-neighbours of h besides
  s, and h is saturated in every J by users inside X\{s}. The saturation is witnessed
  INSIDE the exposing set; no user need be sought outside it. []

REMAINING OPEN CASE — a SINGLE case: N_H(P) not subseteq Q, i.e. some cycle vertex s
has an H-neighbour h outside Q. (There is NO separate "S-S" complement of Lemma A-I:
edges inside P are impossible by bipartiteness and P->(S\P) edges are absent from
G[H u P]. S-S edges become relevant only later, for hereditary blockers on larger
auxiliary sets Y subseteq T_F that include auxiliary S-vertices.)
Two more PROVED lemmas, verified on O-56, that pin down A_s. "Tight" below is
Hall/rho-tightness (rho(X)=2|X|), the exposing-set notion; distinct from FVS/hereditary
tightness tau(X)=|X|. Note delta(X)=rho(X)-2|X| >= 0 for all X (feasibility).
 COMMON TIGHT CARRIER. Let f^-=(s,q^-), f^+=(s,q^+) be the two forced F-edges at s,
  with canonical inclusion-minimal tight exposing sets X^-, X^+. Then X^- ∩ X^+ is
  tight (lattice), contains s, and still exposes BOTH f^- and f^+ (its degree at each
  q is <= that of the exposer), so by inclusion-minimality X^- ∩ X^+ = X^- = X^+ =: A_s.
  Moreover for any tight Y containing s, A_s ∩ Y is tight, contains s, exposes a forced
  edge at s, so A_s ∩ Y = A_s, i.e. A_s subseteq Y. Hence A_s is the UNIQUE MINIMUM
  tight set containing s (the "tight carrier" — now the term "atom" is justified). []
 PUNCTURED TIGHTNESS. Let B_s = A_s\{s}. Removing s lowers min(c(v),deg_{A_s}(v)) by 1
  exactly at the H-neighbours v of s with deg_{A_s}(v) <= c(v); let k be their number.
  A_s exposes both f^-,f^+, so their distinct H-ends q^-,q^+ are both such vertices,
  giving k>=2; and rho(B_s)=rho(A_s)-k=2|A_s|-k so delta(B_s)=2-k, while delta>=0
  forces k<=2. Hence k=2 and delta(B_s)=0: B_s IS TIGHT, the only H-neighbours of s
  with deg_{A_s}(v)<=c(v) are exactly q^-,q^+, and every OTHER H-neighbour h of s has
  deg_{A_s}(h) >= c(h)+1 (this recovers and strengthens Exposing-Set Internal
  Saturation). [] (Verified O-56: A_0={0,2,3}, B_0={2,3} tight, k=2 at {4,5}, external
  h=6 has deg_{A_0}(6)=3>=3.)
UPDATED LOCAL STRUCTURE. For an external H-neighbour h of s: h is oversubscribed in A_s
(deg_{A_s}(h) >= c(h)+1, so deg_{B_s}(h) >= c(h)); B_s=A_s\{s} is tight; ONLY this
oversubscribed h is guaranteed saturated by B_s (Tight-Set Saturation gives load_B(v) =
min(c(v),deg_B(v)); a v with deg_B(v) < c(v) is NOT saturated — see the capacity-one
witness O-64, where w has deg_B(w)=1 < c(w)=2). Support U_h = N_G(h) ∩ B_s, |U_h| >=
c(h). On O-56 the violation happens to sit in B_s; but B_s is NOT a universal localizer
(O-64 below).

SINGLE-BLOCKER SUBCASE — PROVED, verified. Let h be an external
H-neighbour of s (c(h)=2, so |U_h|>=2 by internal saturation), U_h=N_G(h) ∩ B_s. If
every u in U_h has at most one H-neighbour OTHER than h, then G[H u U_h]-h is a forest:
all of U_h share the neighbour h so lie in one bipartition class (no edges inside U_h);
after deleting h each u has degree <=1, so lies on no cycle, and H-h is a forest. Hence
D={h}, |D|=1 <= |U_h|-1, giving tau(G[H u U_h]) <= 1 < |U_h| — contradiction. []
(The earlier "two disjoint paths in H-h" phrasing is replaced by this degree-<=1
argument; O-56 is this subcase, 2~{6,7}, 3~{6,8}.)

EXACT FOREST-GEOMETRY QUOTIENT (the condition Hall tightness does not see). For an
INDEPENDENT Y subseteq B_s (no S-S edges inside Y) define the bipartite multigraph
M_h(Y): one side = Y, other side = the connected components of H-h; for each incidence
u-v with u in Y, v in component C, add an edge u-C (parallel edges kept). Then
G[H u Y]-h is a forest IFF M_h(Y) is acyclic (contract each component of the forest H-h;
cycles correspond; parallel edges u-C lift to the private cycle through u and the unique
C-path between its two attachments). The single-blocker subcase is exactly "M_h(U_h)
acyclic" — VALID because U_h is independent (all share neighbour h => one bipartition
class). CAVEAT: B_s in general may contain S-S edges (S need not be independent),
which appear in G[H u Y] but NOT in M_h(Y); for general Y use the AUGMENTED quotient
Mhat_h(Y) = M_h(Y) plus all edges of G[Y]; then G[H u Y]-h is a forest IFF Mhat_h(Y) is
acyclic. Note: incidence-degree >=3 does NOT by itself force a private cycle — only when
two of u's non-h neighbours lie in the SAME component of H-h.

CAPACITY-ONE COUNTEREXAMPLE TO B_s-LOCALIZATION (O-64, verified) — B_s is NOT a universal
localizer, so the earlier "Punctured-Carrier Lemma" (violation always inside B_s) is
FALSE. Witness: S={s,t,u}, H-tree q1-r-q2, q1-y, y-h, y-w; e=h-y (c(h)=c(y)=1); s~q1,q2,h,
t~q1,q2, u~h,w. Unique feasible selection s,t->{q1,q2}, u->{h,w}: u saturates the
capacity-1 vertex h, so s is pushed off h and s-q1-t-q2-s is a forced cycle (NO feasible
exchange exists). Carrier A_s={s,u}, B_s={u}, B_s Hall-tight; BUT tau(G[H u B_s])=1=|B_s|
(the cycle u-h-y-w-u needs its own vertex) — B_s carries NO hereditary violation, and no
Y subseteq B_s helps. The first violation is on the cycle's OWN S-side P={s,t}:
tau(G[H u P])=1<2 (delete q1). So neither P nor B_s is a universal localization set (O-56/
O-63: violation in B_s; O-64: violation on P, B_s clean, no exchange).

FINAL HUMAN PROOF TARGET (carrier-family form; NOT proved; would close Lemma A). Assume a
forced-core cycle F exists while hereditary FVS tightness holds for every X subseteq S.
Using the FAMILY of common carriers {A_s : s in P} (each the unique minimum tight set at
s), their punctures B_s, capacity-1 and capacity-2 external neighbours, and the H-forest
quotient geometry (Mhat_h), derive one of:
 (1) a hereditary-violating subset X contained in P union (union_s A_s) — obtained from
   the carrier family and P, NOT necessarily inside B_s or P alone. (NOT a "lattice":
   the proved closure is for Hall-tight sets like the A_s, B_s; P need not be Hall-
   tight, and union/intersection with P need not preserve tightness.) OR
 (2) a feasible incidence exchange avoiding a forced-cycle edge.
Do NOT assert the violating set is always P, always B_s, or always T_F until one such
localization is proved. PROVED PIECES available as footholds: Common Tight Carrier,
Punctured Tightness, single-blocker/acyclic-quotient subcase, the Mhat_h characterization.
WITHDRAWN as unsupported/false: (a) the "propagation" branch (a surviving cycle "exposes
a further external saturated H-neighbour"); (b) "every B_s vertex has incidence-degree 2"
(FALSE, O-63); (c) "degree>=3 => private cycle" (only when the quotient is cyclic); (d)
B_s-localization / the B_s-only Punctured-Carrier Lemma (FALSE, O-64); (e) the sharper
tau(G[H u B_s])=|B_s|-1 conjecture (FALSE, O-64: tau(B_s)=|B_s|). The capacity-2-only
inequality tau(G[H u B_s]) <= |B_s|-1 is neither proved nor refuted; capacity-1 and
capacity-2 external neighbours are SEPARATE structural branches. Do NOT use "hereditary
tightness => forced core acyclic" as a foothold — that implication IS Lemma A (open);
only "S min FVS <=> tau(G[H u X])=|X| for all X subseteq S" is available.

---
## E. Lemma B (cycle erasure) — OPEN core
FALSIFIED SHORTEST THEOREM: A1 ("some globally-shortest residual pair erases C") and
U1 held exhaustively n<=10 (448,577 cycles) but the SEALED n=11 holdout FALSIFIED
both (6 failures each; frozen pre-launch, dual-verified independently).
THE SIX n=11 WITNESSES (all k=4, 4-vertex cycles): the relevant shortest bad paths
DESTROY C and create ONE crossing cycle; a cycle-erasing reroute exists only at
length d0+2. (The earlier "rotation" interpretation was retracted; these are
crossing, not rotation.)
CORRECTED FROZEN STATEMENTS (verified exhaustively n<=11; the exhaustive n=12 run was
ABORTED before completion by decision => aborted prospective holdout, NO verdict; the
frozen statements + checker hashes remain reusable for a future holdout):
 (Abbreviations: d0(C) = the minimum residual augmenting-path length over the avoidable
 edges of C; dCES(C) = the minimum length of a residual path whose toggle is CES for C.)
 B-PLUS-2: dCES(C) <= d0(C) + 2.
 B-TERMINAL-SLIDE / B-H-SLIDE: for every selected cycle C, with d0 the min residual
 augmenting-path length over avoidable edges, there exist an avoidable edge a=(s,h)
 and a residual path Q0 of length d0 such that EITHER toggling Q0 is CES, OR Q0 ends
 at an H-terminal t and extends by t-u-h on the same released edge to a simple
 feasible residual path Q+ whose state exchange, from J0 = toggle(Q0), is
   J+ = J0 - (t,u) + (u,h),
 with J+ CES. Keep B-PLUS-2, B-TERMINAL-SLIDE, B-H-SLIDE logically separate.
B1 — FORMAL TERMINAL-SLIDE CRITERION (PROVED conditional lemma; corrected in review;
separates the UNDERSTOOD slide from the OPEN existence theorem B2).
Setup: a=(s,h) an avoidable (released) edge; Q0 a simple residual augmenting path from the
release ending at H-terminal t; J0 = toggle(Q0), feasible. Let (u,t) be the FINAL added
edge of Q0 (u the last S-vertex, t the H-terminal).
HYPOTHESES (explicit form):
 (H1) C is not a cycle of J0 (Q0 destroys C);
 (H2) J0 has EXACTLY ONE cycle Z that was NOT already present in J (old cycles of J other
    than C may persist — J0 need not be globally acyclic);
 (H3) the final added edge (u,t) of Q0 lies on Z;
 (H4) (u,h) is an incidence edge of G, unselected in J0, with (u,h) != a (equivalently
    u != s), AND deg_{J0-(u,t)}(h) < c(h) [explicit residual capacity — necessary,
    since Q0 may have re-consumed the unit freed by releasing a];
 (H5) u and h lie in different components of J0 - (u,t).
CLAIM: J+ = J0 - (u,t) + (u,h) is feasible, still omits a, destroys Z, and creates NO new
cycle (it need not be globally acyclic); hence J+ is cycle-erasing (CES) for C.
PROOF.
Feasibility (termwise):
 - t is an H-vertex; it loses the incidence (u,t), so its load drops by 1 (<= c(t)). No
  demand at t. OK.
 - u is an S-vertex of demand 2; loses (u,t), gains (u,h): selected degree stays 2. OK.
 - h gains (u,h); by (H4) deg_{J0-(u,t)}(h) < c(h), so load_{J+}(h) <= c(h). OK.
 - all other vertices keep their J0 incidences. Hence J+ is feasible. And (u,h) != a so a
  stays unselected; J+ still omits a (an avoider).
No new cycle:
 - By (H2) Z is the ONLY cycle newly created by Q0; by (H3) (u,t) in Z; deleting (u,t)
  breaks Z. Every cycle of J0-(u,t) was therefore already a cycle of J (deleting (u,t)
  cannot create a cycle). 
 - Adding (u,h) with u,h in DIFFERENT components of J0-(u,t) (H5) joins two components,
  creating no cycle. So every cycle of J+ was already a cycle of J; combined with (H1),
  J+ destroys C and introduces no new selected cycle. J+ is CES for C (canonical
  definition, notation A). [] (J+ may still contain OLD cycles of J; CES requires
  destroying C and creating no fresh cycle — it does NOT require global acyclicity — and
  this implies a strict selected-cycle-count decrease.)
(In-sample audit, six n=11 witnesses, all 20 bad shortest paths: final added edge (u,t)
on Z, (u,h) unselected with the residual-capacity condition, u,h in different components
of J0-(u,t), freed endpoint = h; exactly one old cycle (C) destroyed each time.)

B2 — THE ACTUAL OPEN EXISTENCE PROBLEM (NOT "a K_{3,2} exists").
For every positive-gap selected cycle C there is a globally shortest residual augmenting
path Q0 (for some released cycle edge) such that EITHER Q0 is CES, OR its terminal
configuration satisfies hypotheses (H1)-(H5) of B1. The six n=11 witnesses realise this
via a local K_{3,2} (4-cycle S-vertices p,q plus an off-cycle S-vertex u adjacent to both
cycle H-vertices, supplying u), but that is ONE empirical mechanism, not the theorem.
EMPIRICAL K_{3,2} NORMAL FORM (PROVISIONAL): observed in all six positive-gap n=11 cases;
UNTESTED beyond n=11 (n=12 aborted, no verdict). Do NOT treat as proved or seek a
universal K_{3,2} first (B5). The open obligation is the existence of a shortest Q0 whose
terminal meets (H1)-(H5) — to be approached via residual shortestness (B4), capacity
saturation, and hereditary tightness, not by assuming the K_{3,2}.

B3 — IN-SAMPLE NORMALIZATION OF THE SIX n=11 SHORTEST BAD PATHS (EMPIRICAL; NOT promoted;
these six are the A1-failure exceptions from which S-B4 was formulated, so this is IN-
SAMPLE exhaustive description, NOT prospective validation). 3 distinct n=11 graphs x 2
selections; all k=4, 4-cycle C, d0=3. Over ALL 20 shortest bad paths Q0, fresh analysis:
 - Q0 destroys C: 20/20.
 - exactly ONE old cycle is destroyed (namely C): 20/20 (old-destroyed count = 1 always).
 - J0 has EXACTLY ONE new cyclic component Z: 20/20.
 - the FINAL ADDED EDGE (u,t) of Q0 lies on Z (both ends in Z) — the strong form B1 needs,
  not merely "t on Z": 20/20.
 - deg_{J0}(t) = 2: 20/20 (terminal-degree obstruction absent here).
 - of the two terminal selected edges at t, exactly one u has u ~ h (freed endpoint), the
  B1 slide vertex, with u,h in different components of J0-(u,t): 20/20.
So B1's (H1)-(H5) hold via that u and the d0+2 slide reaches CES in every witness. EMPIRICAL
n=11 regularities, NOT proved; they are the B4 targets below.

B4 — FOOTHOLDS + SPLIT PROOF TARGETS (shortestness consequences).
FOOTHOLD 1 (PROVED, verified): J u {e} has MAX DEGREE 2 (S-vertices demand 2 => deg 2;
H-vertex deg <= c(h) <= 2; e=(x,y) with c(x)=c(y)=1 keeps x,y <= 2), hence a disjoint union
of simple paths and cycles. Releasing avoidable a on C opens C into a path; toggling a
shortest Q0 preserves max-degree-2. For max-degree-2 graphs, cycle rank = number of cycle
components, and |E(J0)|=|E(J)|, |V| equal, so cycles(J0)-cycles(J)=comps(J0)-comps(J).
FOOTHOLD 2 (PROVED, corrected in review): Q0 is a residual path in D_a := the residual
digraph of N-a (C4), from which the released incidence arc a is ABSENT; therefore a is not
an edge of Q0 BY DEFINITION (not by assumption). Hence J Δ J0 = {a} u E(Q0) with the two
sets edge-disjoint. TWO cases:
 CASE P (h not a vertex of Q0): {a} u Q0 is a simple alternating PATH from h to t.
 CASE C (h on Q0): h has residual capacity immediately after releasing a, so a shortest
  augmenting path cannot pass through h internally (the prefix ending at h would be a
  SHORTER augmenting path); hence h = t and {a} u Q0 is a simple alternating CYCLE.
 So "single simple path" is NOT universal — only Case P. The endpoint-return case t=h is
 separate (see B4-RETURN). CYCLE-RANK CAVEAT: with d = #old cycles destroyed and n = #new
 cycles, n - d = comps(J0)-comps(J). The formula n = comps(J0)-comps(J)+1 assumes d=1
 (only C destroyed) — NOT proved. Also, even in Case P a single alternating path may
 enter/leave/re-enter retained components and alter SEVERAL cycle components; rank
 accounting ALONE does not give "exactly one new cycle". Shortestness/lex-optimality must
 enter (via the ordered retained-component trace, B4 sub-program).
SPLIT PROOF TARGETS (all NOT proved; frozen; in-sample 20/20 at n=11; n<=10 VACUOUS — 0
positive-gap cycles, consistent with A1/U1 exhaustive n<=10):
 S-B4a — a lex-optimal shortest bad path destroys NO old selected cycle other than C.
 S-B4b — such a path creates EXACTLY ONE new selected cycle Z.
 S-B4c — Z contains the FINAL added edge (u,t) of Q0 (the exact property B1 needs; strictly
     stronger than "t on Z", since t may carry two selected incidences).
 (subtarget) deg_{J0}(t)=2 can be arranged — NOT automatic when t is previously unused or a
     capacity-1 endpoint; if deg_{J0}(t)=1 no new cycle contains t or (u,t).
 B4-RETURN (freeze separately) — if a shortest path for released a=(s,h) ends at h (Case C),
     then either its toggle is CES or another equally-short path has terminal != h with
     no worse lex cycle profile.
The real work: prove that lex-optimality collapses the ordered retained-component trace to
ONE terminal closing interval — a genuine combinatorial argument, NOT the Euler-rank
identity. If S-B4a/b/c are proved, B1 + B4 reduce Lemma B to B5 (the single adjacency u~h).

B4 DIRECTED TRACE + THE CORRECT SHORTCUT OBJECT (corrected in review).
WITHDRAWN: the undirected "splice P_i" shortcut. An R-component path P_i is made of
RETAINED SELECTED edges, which in the residual digraph D_a (= residual digraph of J-a:
S->H on unselected incidences, H->S on selected) all orient H->S; at an internal S-vertex
of P_i both selected edges point into S, so P_i is NOT a directed residual path. Undirected
same-R-component closure therefore does NOT supply a residual shortcut.
VERIFIED CLASS-1 OBSTRUCTION (O-67, preserved): an arbitrary feasible max-degree-2 state
(S={s0,s2,s4,r}; s0~ha,hb,h1; s2~h1,g,h3; s4~h3,hc,t; r~g,h3; caps 1 except c(g)=c(h3)=2;
release a=s0-ha) has a UNIQUE shortest augmenting path s0-h1-s2-h3-s4-t whose toggle creates
a NONTERMINAL new cycle s2-g-r-h3, and no directed chord improves it. So shortestness +
max-degree-2 + same-R-component ALONE cannot establish S-B4; the hereditary-FVS structure
is essential.
DIRECTED TRACE (computed on all six n=11 witnesses): each new cycle Z is ONE-ADDED-EDGE and
TERMINAL — E(Z) ∩ E(Q0) = exactly the final added edge (u,t); Z's other edges are retained
selected (oriented H->S). BFS distances in D_a increase 0,1,2,3 along Q0. The witnesses
occupy only the {one-added-edge, terminal} class; multi-added-edge and nonterminal classes
are unrepresented at n=11.
THE CORRECT SHORTCUT OBJECT = a DIRECTED RESIDUAL CHORD in D_a (D_a is throughout the
residual digraph of N-a, C4: S->H on unselected incidences, H->S on selected; the released
incidence a is ABSENT, never an unselected forward arc): a directed path W from v_i
to v_j on Q0 with internal vertices off Q0 and |W| < j-i (strict improvement), or |W| = j-i
with strictly fewer new cycles / fewer path-edges on new cycles (lex improvement). Verify
any proposed chord with BFS distance labels in D_a (undirected forest connectivity is NOT
residual reachability). FROZEN shortcut lemmas (NOT proved; FROZEN-B4 v3):
 DIRECTED-CHORD-B: a lex-optimal shortest bad path creating a NONTERMINAL new cycle
  determines a directed residual chord improving Q0. (FALSE in class 1 — O-67; open for
  class 3 = hereditarily tight.)
 DIRECTED-CHORD-A: such a path destroying an old cycle D != C determines a directed
  residual chord improving Q0. (Logically independent of B; keep separate.)
Test order: (1) arbitrary feasible states, (2) graph-realizable, (3) hereditarily
tight; preserve the first failure in each class. S-B4a/b/c remain separate open targets; the
missing implication is "forbidden cycle pattern + residual orientation + shortestness +
hereditary structure => directed improving chord", NOT the Euler-rank identity.

---
## F. Computational methodology and hashes
Engines: nauty geng (connected bipartite, geng -bc -q N); a fresh residual-DAG
shortest-path engine (a1_verify.py) cross-checked against an independent
one-move/nbrs engine and against feasible-state symmetric differences; the quotient
certificate; the forced-core / tight-set / FVS computations. Dual-verification and
sealed pre-registered holdouts throughout (FROZEN-A1-U1.md, FROZEN-BPLUS2.md, with
sha256 code hashes). VERIFICATION SCOPES (per object, distinct):
 - Direct Conjecture-40 sweep (algebraic equivalence B1 target): COMPLETE for n<=9; n=10
  STOPPED at about 59%, NO final verdict.
 - Lemma-B cycle universe (A1/U1, B-PLUS-2/terminal-slide): EXHAUSTIVE through n<=11. The
  ~8.2M figure is the n=11 Lemma-B CYCLE-COMPONENT count (NOT a cumulative total through
  n<=11).
 - n=12 (Lemma-B holdout): ABORTED before completion (~49% of graphs processed then
  stopped by decision), NO verdict; frozen statements and checker hashes remain reusable.
 - Lemma-A forced-core (n=11): intermediate-report provenance only (per section D — preserved
  a preserved intermediate report; incompletely ledgered; not independently reproducible; NOT a
  hashed run).
PROTOCOL NOTE (matching the ledger): during the aborted n=12 run the running failure
counter(s) were viewed, contrary to the operational-only monitoring discipline; all
statements and code were frozen and sha256-hashed BEFORE launch, no tuning followed, and
the deviation is recorded (RESULT_RECORD O-45/O-58).

---
## G. Open proof challenges
1. Lemma A: hereditary FVS tightness => forced-core acyclic (the blocker/exchange
  dichotomy, or another argument).
2. Lemma B: existence of the terminal-slide vertex u for every positive-gap cycle;
  and the metric bound B-PLUS-2 in general.
3. General -> bipartite reduction: the coefficient-1 general theorem ell + o >= 2tau + 1
  (via the odd-cycle-transversal parameter). NOTE: the WEAKER coefficient-2 form
  ell + 2o >= 2tau + 1 is proved conditionally on the bipartite theorem (B5); the
  coefficient-1 theorem remains open.
(Former item 4 REMOVED: the min-cut normalization of the generalized Hall proof C5 is
already expanded in full detail in C5; it is no longer an open/exposition item.)

Reduction status: F2 => bipartite target is PROVED (B3); the whole result reduces to
proving F2 (= Lemma A + Lemma B via the cycle-erasing descent) for the bipartite
case, plus the provisional general -> bipartite reduction (coefficient-1 open; coefficient-2
form B5 proved conditionally).
