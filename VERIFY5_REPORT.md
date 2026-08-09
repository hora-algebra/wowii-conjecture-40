# VERIFY-5 phase 2 report

## Verdict

**REVIEWED-SOUND, NOT BLIND-REPRODUCED**

Scope sentence, quoting `STATEMENT.md`: this report reviews the claim, “Let
$G$ be a finite simple bipartite graph, \emph{not necessarily connected},
$S$ a minimum FVS, $H=G-S$, and $e$ a fixed edge of $H$ with capacities as in
Definition~\ref{def:selection}. Prove that the forced incidence core is
acyclic.”

This verdict applies to the proved target steps NC, CE, and A-I+; it is not a
verdict that Lemma A° itself has been proved.  `LEMMA-A-CLEAN-END.md` explicitly
leaves Lemma A° open, at the same external-neighbour/forest-geometry
obstruction recorded in `SEALED-DERIVATION.md`.

## 1. Sealed comparison boundary

The compared files and their package-local SHA-256 values were:

```text
f42415645f6990c43c66f21c673da7875e1a9244baf3d5114ee38ab08049330e  SEALED-DERIVATION.md
231205c7ae7c7287d12f3afc7b92f8872e6cdd8d7333bfb956e8f103ff4d7f5f  LEMMA-A-CLEAN-END.md
```

Phase 1 did not independently derive NC, CE, or A-I+.  It was expressly
allowed to cite their statement blocks from `GIVEN-RESULTS.md`, and used them
as given inputs in `SEALED-DERIVATION.md` lines 23-47 and 105-138.  Therefore
agreement between phase 1 and the target on those results is not blind
reproduction.

Phase 1's independently added blocker equivalence and heavy/guarded-sparse
dichotomy are compatible with the target.  The target does not claim to cross
phase 1's carrier-to-blocker bridge (CB), and its lines 238-261 identify the
same surviving issue: the geometry of `Ext(P)` in the forest `H`.

## 2. Verbatim list of steps not blind-reproduced in phase 1

These are the complete target result statements that phase 1 imported rather
than independently derived.  They are quoted verbatim from
`LEMMA-A-CLEAN-END.md`.

### U1 — NC

> **NC (clean-end chordlessness) — MATHEMATICALLY PROVED.** Let `q ∈ Q` be
> clean. Then
>
>   (i)  `N_S(q) ∩ P = cyc(q)`, and
>   (ii) `N_S(q) ∩ (U \ P) = ∅`.
>
> Hence `deg_U(q) = |cyc(q) ∩ U|`, and on a `T_F`-normalized instance
> (`S = T_F = P ∪ U`, Lemma 4.7) simply `N_S(q) = cyc(q)`, i.e. `deg_S(q) = 2`.

### U2 — CE

> **Corollary CE (clean ends of a maximal carrier) — MATHEMATICALLY PROVED.**
> Every forced-core cycle has a cycle vertex `s` — any one whose carrier is
> inclusion-maximal, which exists by CP — such that **both** forced ends `q` of
> `s` satisfy `N_S(q) ∩ (P ∪ U) = cyc(q)`. On a `T_F`-normalized instance both
> ends have `deg_S(q) = 2` exactly.

### U3 — A-I⁺

> **A-I⁺ — MATHEMATICALLY PROVED.** Suppose there is a **clean** `q_0 ∈ Q` with
>
>   (1) `Ext(s) = ∅` for both `s ∈ cyc(q_0)`, and
>   (2) `|Ext(s)| ≤ 1` for every other `s ∈ P`.
>
> Then `τ(G[H ∪ P]) ≤ m − 1 < m = |P|`, contradicting hereditary FVS tightness.
> Hence no forced-core cycle of a Lemma-A° instance has this shape.

No other proved target step advances beyond phase 1.  CAP2-BS is quoted and
assessed separately in Section 6 because the target itself labels it
conjectural and does not use it in a derivation.

## 3. Step-by-step adversarial proof review

### 3.1 NC(i): exclusion of a chord at a clean end

**What phase 1 could not independently derive.**  U1(i) asserts that a clean
cycle-side `H` vertex has no incidence to a nonconsecutive vertex of `P`.

**Target chain.**  For a putative chord `s_k-q_i`, with
`s_k notin cyc(q_i)`, `q_i` is not one of the two forced ends of `s_k`.
Punctured tightness therefore gives

```text
deg_{A_{s_k}}(q_i) >= c(q_i)+1 = 3.
```

The equality `c(q_i)=2` is justified: two forced cycle incidences load `q_i`,
so a capacity-one vertex cannot occur on `Q`.  Since the chord endpoint
`s_k` belongs to `A_{s_k}`, puncturing removes exactly that one neighbour and
gives `deg_{B_{s_k}}(q_i)>=2`.  As `B_{s_k} subseteq U`, this implies
`deg_U(q_i)>=2`, contrary to cleanliness.

**Adversarial checks.**

- The modular indexing remains correct at `m=2`: each cycle vertex has two
  distinct forced ends, and a nonconsecutive `P` vertex does not exist, so the
  assertion is vacuous rather than malformed.
- The proof does not assume `P intersect U` is empty.
- It uses the “other neighbour” clause of punctured tightness only after
  proving that the chord is not a forced end.
- Simplicity of `G` makes puncturing lower the degree by exactly one.

**Judgment.**  The written justification closes U1(i); it does not assume it.

### 3.2 NC(ii): exclusion of an auxiliary `U`-neighbour

**What phase 1 could not independently derive.**  U1(ii) asserts that a clean
`q` is adjacent to no vertex in `U` outside `P`.

**Target chain.**  If `w in U\P` is adjacent to `q`, cleanliness and the one
known neighbour `w` imply `N_S(q) intersect U={w}`.  Since `w` is not in `P`,
neither of the two vertices in `cyc(q)` can belong to `U`; otherwise `q` would
have at least two distinct `U`-neighbours.  Thus both cycle endpoints belong
to `P\U`.  They are consecutive and share `q`, so CS(b) gives
`deg_U(q)=0`, contradicting the edge `w-q`.

**Adversarial checks.**

- Membership of `w` in several punctures would not matter: `deg_U` counts
  vertices, and `w` is still one neighbour.
- The inference that both cycle endpoints lie outside `U` uses
  `w notin P`, so `w` is distinct from them.
- CS(b), not its known-false converse, is invoked with both of its hypotheses
  established.
- The argument remains valid for the two parallel cycle positions at `m=2`.

**Judgment.**  The written justification closes U1(ii); it does not assume it.

### 3.3 The “hence” clause of NC

U1(i) says all `P`-neighbours are exactly `cyc(q)`, and U1(ii) removes every
neighbour in `U\P`.  Hence the neighbours belonging to `U` are exactly
`cyc(q) intersect U`, proving the degree identity.  Under normalization every
`S` vertex lies in `P union U`, so no further `S`-neighbour is possible.

**Judgment.**  This is a set decomposition, with no hidden monotonicity or
normalization assumption.

### 3.4 CE

**What phase 1 could not independently derive.**  U2 turns CP's residual
capacity holes into exact neighbourhood statements at both ends of a single
maximal-carrier vertex.

**Target chain.**  CP identifies inclusion-maximal cycle carriers with
vertices of `P\U` and guarantees that at least one exists.  CS(a) makes both
forced ends of every such vertex clean.  NC applied separately at the two
ends gives `N_S(q) intersect (P union U)=cyc(q)`.  Normalization replaces
`P union U` by `S`.

**Adversarial checks.**  This chain neither asks for two adjacent maximal
carriers nor upgrades cleanliness to `deg_U(q)=0`.  It is therefore unaffected
by ADJ-1.

**Judgment.**  The written justification closes U2 from CP, CS(a), and NC.

### 3.5 A-I+: construction of the FVS

**What phase 1 could not independently derive.**  U3 asserts that deleting
`D=Q\{q_0}` is sufficient under the clean-end and external-degree hypotheses.

**Target chain.**  The target establishes each needed point:

1. `|D|=m-1`, and `H-D` is a forest because `H` is a forest.
2. All vertices of `P` lie in one global bipartition class, so there are no
   edges inside `P`.
3. After deleting `D`, the surviving neighbours of `s in P` are exactly
   `(N_H(s) intersect {q_0}) union Ext(s)`.
4. Each endpoint in `cyc(q_0)` has exactly the one neighbour `q_0`, because
   its external neighbourhood is empty.
5. NC(i) excludes a chord from every other `s in P` to `q_0`; hypothesis (2)
   leaves such an `s` with degree at most one.
6. Adding independent vertices of degree at most one to a forest cannot
   create a cycle.  Thus `D` is an FVS of size `m-1`.

**Adversarial checks.**

- Edges from `P` to `S\P` are absent from the induced graph
  `G[H union P]`; no independence of all of `S` is assumed.
- Chords to the deleted vertices of `Q\{q_0}` are harmless.
- NC(i) is used only at the clean vertex `q_0`.
- Sharing an `H`-neighbour does not create a cycle when every added `P`
  vertex itself has degree at most one.

**Judgment.**  The written justification closes U3.  Its use of NC(i) is
essential and explicit, not circular.

## 4. Controls-first machine instantiation

All evidentiary reads and generated outputs were confined to the package.  The
new target and attempt-report files are not listed in the original manifest,
so I recorded their hashes rather than treating manifest coverage as
provenance for them.

### 4.1 Controls, executed before target scans

An independent inline standard-library checker enumerated feasible selections,
intersected them to obtain forced incidences, recomputed all Hall-tight sets
and canonical carriers, and tested NC, CE, and the A-I+ surviving-degree
obligation.  It produced:

```text
O-56: PASS feasible=1 clean=2 dirty=0 chords=0 maxima=['0', '1'] AIplus_q=0
O-63: PASS feasible=6 clean=2 dirty=0 chords=0 maxima=['s', 't'] AIplus_q=0
O-64: PASS feasible=1 clean=2 dirty=0 chords=0 maxima=['s', 't'] AIplus_q=0
ADJ-1: PASS feasible=1 clean=2 dirty=1 chords=1 maxima=['s2'] AIplus_q=2
NEGATIVE CONTROLS NC-ALL/CHORD-ALL/PDIS/ADJ: FIRED
PURE-m2: PASS feasible=1 clean=2 dirty=0 chords=0 maxima=['s0', 's1'] AIplus_q=2
POSITIVE CONTROL A-I+ m=2: FIRED
NEGATIVE CONTROL cyclic-core detector (forced path): FIRED
PHASE2 CONTROLS-FIRST: PASS
```

ADJ-1 was reconstructed from the certificate in
`LEMMA-A-CARRIER-POSET.md`, not from an absent target checker.  Its dirty
vertex has a genuine chord, so the checker demonstrably rejects the false
strengthenings “every `q` is clean” and “no chord exists anywhere.”  The pure
four-cycle exercises the `m=2` A-I+ branch.  The forced-path control ensures
that unique selection was not conflated with a cyclic forced core.

### 4.2 Targeted refutation search: capacity-two Hall universe

I exhaustively enumerated all `2^16` labeled incidence masks with four demand
vertices, four capacity-two vertices, and demand two.  For every feasible
system I enumerated every feasible selection, formed the forced core, extracted
every cyclic component, recomputed carriers from the intersection of all tight
sets containing each cycle vertex, and tested every clean `q`.

```text
systems=65536
feasible systems=7151
systems with cyclic forced core=2934
forced cyclic components=3492
clean q tested=7992
dirty q observed=3744
A-I+ qualifying (cycle,q) instances=6912

FAILURES:
NC(i)=0  NC(ii)=0  NC-hence=0  normalized-neighbourhood=0
NCM=0    CE=0      A-I+-surviving-degree=0  CP-regression=0

NEGATIVE CONTROLS WITHIN UNIVERSE:
P intersect U=2304  CHORD-ALL=2304  NC-ALL=2304  ADJ=1440
```

This is a direct attempted refutation of every asserted implication in U1-U3,
not evidence for Lemma A°: the universe is Hall-layer only and does not impose
a forest completion or minimum-FVS status.

### 4.3 Targeted refutation search: capacity-one branch

To exercise genuine capacity-one vertices, I separately enumerated all 24,576
pairs consisting of a labeled `S=3,H=4` incidence mask and a choice of two
capacity-one `H` vertices.  This universe had 3,030 feasible systems, 342 with
a cyclic forced core, and 342 forced cyclic components.

```text
clean q tested=684
dirty q observed=0
A-I+ qualifying (cycle,q) instances=144
NC(i)=0  NC(ii)=0  CE=0  A-I+-surviving-degree=0
```

No negative control fired internally in this small capacity-one universe, so
its zero counts are reported only as supplementary instantiation.  The
controls in Section 4.1, including capacity-one witness O-64, had already run.

### 4.4 Preserved graph-oracle scan

After the controls and target searches, I reran the packaged graph oracle:

```text
PYTHONHASHSEED=0 python3 forced_core.py 10
```

It reproduced:

```text
instances = 116216
CYCLIC forced core (= all-R3 cycle exists = Lemma A FAILS) = 0
non-forest forced cores = 0
max forced-core path length (edges) = 8
```

The result-file SHA-256 was
`63f5c271b4ab32975a998f1446500457128ac7dd5d5e0251ad5e3aa1f4f66724`.
The generated output files were then removed.  Because this oracle found no
cyclic forced core on its minimum-FVS universe, it supports the statement at
that finite order but tests U1-U3 only vacuously; Sections 4.1-4.3 provide the
nonvacuous step-level tests.

## 5. Exact refutation verdict per proved target step

| Step | Targeted refutation attempted | Machine result | Does prose close it? |
|---|---|---:|---|
| NC(i) | clean chord at `q`, including overlap and dirty-chord controls | 0 failures | yes |
| NC(ii) | auxiliary `U\P` neighbour at a clean `q` | 0 failures | yes |
| NC consequence | wrong `deg_U` identity or extra normalized neighbour | 0 failures | yes |
| CE/NCM | maximal-carrier end not clean or not chordless | 0 failures | yes |
| A-I+ | qualifying clean end with a surviving `P`-degree above one | 0 failures | yes |

The machine results are finite regression evidence.  The soundness judgment
comes from the written implications reviewed in Section 3.

## 6. CAP2-BS and other target material outside the proved derivation

The target states, verbatim:

> **CAP2-BS (CONJECTURAL).** Let a forced-core cycle have `S`-side `P`, let
> `s ∈ P` have `B_s ≠ ∅`, and suppose **every** `H`-neighbour of `s` outside its
> two forced ends has capacity 2. Then `τ(G[H ∪ B_s]) ≤ |B_s| − 1`.

This is not a proved step in the target.  Its written discussion explicitly
says the scan is not graded, its in-universe negative control is inert, and
the conclusion remains conjectural.  I therefore did not use CAP2-BS in the
soundness judgment.

I did independently reproduce its four witness controls:

```text
O-56  s=0   B=['2','3']       guard=True   tau=1  bound=1
O-63  s=s   B=['a','b','u']   guard=True   tau=2  bound=2
ADJ-1 s=s2  B=['s0','s1']     guard=True   tau=0  bound=1
O-64  s=s   B=['u']           guard=False  tau=1  bound=0
```

Thus the guarded controls do not refute CAP2-BS and the unguarded form fails
on O-64, exactly as the target says.  This does not establish CAP2-BS.

The target's historical `work/0520` checkers and raw outputs are absent from
this package, so the following numerical evidence claims were not reproduced
on their exact stated universes:

> Over the exhaustive universe, 528 of the 798 cyclic systems satisfy A-I+'s
> hypothesis.

> **Total: 14,699 systems with a cyclic forced core, 0 NC failures, 0 NCM
> failures, 0 CP-regression failures**, with all three negative controls firing
> in every population.

> Over the 798 exhaustive cyclic systems there are 1,602 clean and 18 dirty
> `q`, and **all 18 chords in the universe sit at dirty `q`**.

> 798 cyclic systems, 450 `(system, s)` pairs with `B_s != empty`, of which only
> **18** pass the capacity-2 guard; 3,132 forest completions tested; **0 CAP2-BS
> failures**.

Those are evidence claims, not missing logical steps in the written proofs.
The alternative package-local searches in Section 4 instantiate the proof
predicates but do not reproduce the absent historical runs.

## 7. Final comparison

The target covers exactly the ground phase 1 did not independently reach by
supplying written proofs of NC and A-I+, with CE as their CP/CS consequence.
Each proof step survives direct logical review and targeted finite refutation
search.  The target then stops before the carrier-to-blocker bridge, explicitly
acknowledging that its results do not control `Ext(P)` in the forest.  That is
the same obstruction, not a disagreement between the two derivations.
