# Lemma A — FROZEN human challenge sheet (2026-07-30)

Active proof effort on Lemma A is STOPPED here (project decision). General Lemma A remains
OPEN. No further synthetic construction or localization proof-mining. This sheet is the
precise open problem plus the proved footholds and the warnings that kill false shortcuts.

## The statement (equivalent form)
Fixed S = min FVS, H = G-S a forest, incidence b-matching: each s in S demands 2; c(h)=2
except c(x)=c(y)=1 on the fixed edge e=(x,y). A "forced edge" (R3) is in every feasible
selection; the "forced core" is the graph of forced edges.
LEMMA A: if S is a minimum FVS (equivalently tau(G[H u X])=|X| for every X subseteq S),
the forced core is ACYCLIC. OPEN in general.
EVIDENCE (provenance-labelled, same as PROOFS.md D): n=11 instances 994,607; cyclic forced
cores 0; maximum forced-path length 8. COMPUTATIONALLY VERIFIED according to preserved
a preserved intermediate report; completion is INCOMPLETELY LEDGERED and NOT independently reproducible
from a preserved completion log/checker artifact. NOT a hashed reproducible run.

## Prerequisite statements to read first (exact, in PROOFS.md)
- C5 (Generalized Hall + F1): a feasible selection exists iff rho(X) >= 2|X| for all
 X subseteq S, where rho(X)=sum_h min(c(h),deg_X(h)); F1: a forced (R3) edge a=(s,q) iff
 some Hall-tight X (delta(X)=0) EXPOSES it (s in X and deg_X(q) <= c(q)); the canonical
 exposing set is the inclusion-minimal such X (source side of a max flow in N-a).
- C6 (Tight-set lattice): the Hall-tight sets (delta(X)=rho(X)-2|X|=0) are closed under
 intersection and union (delta is submodular and >= 0).
- These are the exact C5/C6/F1 facts the carrier-family argument below relies on for Hall
 tightness, its lattice, and exposing sets. Read them in PROOFS.md before this sheet.
(The proposed T_F normalization is NOT promoted here — it remains under independent
adversarial review.)

## The sharp challenge (carrier-family form)
Assume a forced-core cycle F exists while tau(G[H u X])=|X| for every X subseteq S. F is
an S-H incidence cycle; P = its S-side. For each s in P let A_s be its unique minimum
Hall-tight carrier (proved to exist, below) and B_s = A_s\{s}. Using {A_s : s in P}, P,
capacity-1 vs capacity-2 external neighbours, the augmented forest quotient Mhat_h, and
feasible-selection exchanges, derive EITHER
 (1) some X subseteq P union (union_s A_s) with tau(G[H u X]) < |X|; OR
 (2) a feasible selection omitting a forced-cycle edge.
This is a proof PROGRAM, not a proved dichotomy. Do NOT assert the violator is always P,
always B_s, or always T_F. "P union (union_s A_s)" is NOT a tight-set lattice: P need not
be Hall-tight, so union/intersection with P need not preserve tightness.

## Disconnected form + normalization (PROVED)
- LEMMA A° (disconnected): G bipartite, NOT necessarily connected; S a min FVS, H=G-S,
 fixed edge e. Then the forced core is acyclic. Implies the connected version F2 needs;
 all footholds below hold without connectedness; the n<=11 evidence was connected only.
- T_F NORMALIZATION LEMMA (PROVED, accepted in review; full proof in PROOFS.md D): for a
 forced-core cycle F with S-side P, set T_F = union_{s in P} A_s (canonical carriers).
 Restricting to G'=G[H u T_F], S'=T_F keeps H, e, capacities; then S' is a min FVS of G',
 hereditary tightness holds on every X subseteq T_F, and every F-edge remains forced (its
 forcedness RE-DERIVED via F1 from the same tight carrier A_s — NOT assumed monotone under
 restriction; restriction may add feasible selections and may disconnect G, hence A°).
 => a minimal counterexample may be assumed S = T_F. (O-56, O-63 already normalized; O-64
 is outside the hereditary-tightness class, so unaffected.)

## Proved footholds (all in PROOFS.md D, verified computationally)
- LEMMA A-I: if N_H(P) subseteq Q (cycle's S-side has all H-neighbours on the cycle),
 hereditary tightness is contradicted. So a violation needs an EXTERNAL H-neighbour.
- TIGHT-SET SATURATION: for Hall-tight X, load_X^J(h)=min(c(h),deg_X(h)) every feasible J.
- EXPOSING-SET INTERNAL SATURATION: an external H-neighbour h of s has deg_X(h)>=c(h)+1
 for any tight X containing s; h saturated inside X\{s}.
- COMMON TIGHT CARRIER: the two forced edges at s share one canonical exposing set A_s,
 the UNIQUE MINIMUM Hall-tight set containing s.
- PUNCTURED TIGHTNESS: B_s=A_s\{s} is Hall-tight; exactly the two forced ends q^-,q^+ have
 deg_{A_s}<=c; every other H-neighbour of s is oversubscribed (deg_{A_s}>=c+1).
- SINGLE-BLOCKER SUBCASE: external h with c(h)=2 and every u in U_h=N(h)∩B_s having <=1
 H-neighbour besides h => {h} blocks G[H u U_h] => tau<=1<|U_h|. (U_h independent.)
- AUGMENTED FOREST QUOTIENT: G[H u Y]-h is a forest IFF Mhat_h(Y) acyclic, where Mhat_h(Y)
 contracts each component of H-h, keeps Y-to-component incidences (parallels) AND all
 edges of G[Y]. (Plain M_h without G[Y] edges is valid only for independent Y.)

## Three certified WARNING witnesses (kill false localizations)
- O-56 (cap-2, quotient ACYCLIC): violation in B_s={2,3}, blocker {6} size 1.
- O-63 (cap-2, quotient CYCLIC): U_h all incidence-degree 3; violation is the FULL B_s
 ={u,a,b}, blocker {h,w} size 2. => "every B_s vertex degree 2" and "degree>=3 =>
 private cycle" are FALSE; the blocker can exceed the single external vertex.
- O-64 (cap-1): B_s={u} is Hall-tight but tau(G[H u B_s])=|B_s| (CLEAN, no violation, no
 exchange); the violation is on P={s,t}. => B_s-localization is FALSE; neither P nor B_s
 is a universal localizer; capacity-1 and capacity-2 are separate branches.
(Full certificates: RESULT_RECORD O-56, O-63, O-64. Independent-code verified.)

## Recorded but PARKED (no further round now)
Capacity-2-only conjecture tau(G[H u B_s]) <= |B_s|-1: neither proved nor refuted. O-64
(capacity-1) does not touch it. Not to be mined further at present.

## Do NOT
- use "hereditary tightness => forced core acyclic" as a foothold (that implication IS
 Lemma A); only "S min FVS <=> tau(G[H u X])=|X| for all X subseteq S" is available.
- restart synthetic forced-cycle construction; three bracketing witnesses suffice.
