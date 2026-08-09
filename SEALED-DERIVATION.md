# VERIFY-5 phase 1 — sealed derivation of Lemma A°

## Verdict

**DOCUMENTED FAILURE.** I did not obtain a complete proof of Lemma A°, and I
did not find a counterexample.  The derivation below reduces the remaining
step to an exact carrier-to-forest-blocker assertion and characterizes the two
structural branches in which that assertion is still missing.  The packaged
controls show that the blocker cannot always be localized to the cycle side
`P` or to one punctured carrier `B_s`.

All evidentiary file reads and all generated outputs in this run were confined
to the package.  No network access was used.

## 1. Setup and certified inputs

Assume for contradiction that the forced core contains a cycle

```text
F = s_1-q_1-s_2-q_2-...-s_m-q_m-s_1,   m >= 2,
```

with notation `P`, `Q`, `A_s`, `B_s`, `U`, `T_F`, `Ext(s)`, and “clean” as in
`GIVEN-RESULTS.md`.  I use the following packaged results as certified inputs:

1. hereditary FVS tightness (`paper/paper.tex`, Lemma C2);
2. the Hall criterion, F1, the tight-set lattice, the common carrier,
   punctured tightness, CS, CP, and the `T_F` normalization;
3. NC/NCM/CE and A-I+ from `GIVEN-RESULTS.md`.

By `T_F` normalization, restricting to `G[H union T_F]` preserves a forced
copy of `F`, minimum-FVS status, and hereditary tightness.  Thus it is enough
to work in the normalized instance

```text
S = T_F = P union U.
```

By CP there is an inclusion-maximal cycle carrier.  By NCM/CE, every cycle
vertex having such a carrier has two clean forced ends, and at each such end

```text
N_S(q) = cyc(q),   so deg_S(q) = 2.
```

In particular every putative counterexample has at least two clean vertices
of `Q` (the two distinct ends of one maximal-carrier vertex).

## 2. An exact reformulation of hereditary FVS tightness

For `R subseteq S`, define the **H-blocker number**

```text
lambda_H(R) = min {|D| : D subseteq V(H) and G[H union R] - D is a forest},
```

with value infinity if no such `D` exists.

### Blocker equivalence

The following two statements are equivalent:

```text
(HT)  tau(G[H union X]) = |X| for every X subseteq S;

(BL)  lambda_H(R) >= |R| for every nonempty R subseteq S.
```

Proof.  Since deleting `X` leaves the forest `H`, one always has
`tau(G[H union X]) <= |X|`.

If (BL) fails, some `D subseteq H` of size less than `|R|` makes
`G[H union R]-D` a forest.  Then `D` is an FVS smaller than `R`, so (HT) fails
at `X=R`.

Conversely, suppose (HT) fails at `X`, and let `D` be an FVS of
`G[H union X]` with `|D|<|X|`.  Put

```text
D_H = D intersect H,       D_S = D intersect X,       R = X \ D_S.
```

Then

```text
G[H union R] - D_H = G[H union X] - D
```

is a forest, while

```text
|D_H| = |D|-|D_S| < |X|-|D_S| = |R|.
```

Thus (BL) fails.  This also shows `R` is nonempty.  This proves the
equivalence.  ∎

Consequently, after normalization a proof of Lemma A° would be complete if
one could prove the following bridge:

> **Carrier-to-blocker bridge (CB).** If the normalized forced core contains
> `F`, then some nonempty `R subseteq T_F` satisfies
> `lambda_H(R) <= |R|-1`.

A-I+ proves CB with `R=P` in its stated shape.  The single-blocker subcase in
`paper/paper.tex` proves CB with `R=U_h` when its degree condition holds.  No
packaged result proves CB in general.

## 3. What A-I+ leaves: an exhaustive structural dichotomy

Let

```text
Z = {s in P : Ext(s) is nonempty}.
```

Every putative counterexample lies in at least one of the following branches:

```text
(H)  some s in P has |Ext(s)| >= 2;                         [heavy]

(G)  every s in P has |Ext(s)| <= 1, and
     Z intersects cyc(q) for every clean q in Q.            [guarded sparse]
```

Proof.  If (H) fails, all external degrees are at most one.  If (G) also
fails, there is a clean `q_0` whose two cycle endpoints have no external
neighbour.  Then A-I+ applies: its condition (1) holds at `q_0`, and its
condition (2) holds because (H) failed.  A-I+ gives
`tau(G[H union P]) <= m-1`, contradicting hereditary tightness.  ∎

CE supplies clean ends but does not force either endpoint of a clean edge to
have empty external neighbourhood.  Equivalently, in the sparse branch the
externally active vertices `Z` form a vertex cover of the cycle edges indexed
by clean vertices of `Q`.

This is the strongest conclusion I could derive from CE plus A-I+ without
introducing an unsupported forest-geometry assertion.

## 4. The obstruction to completing CB

The carrier results constrain the incidence/capacity layer.  The number
`lambda_H(R)`, however, depends on how those incidences attach through the
components and paths of the forest `H`, and (for general `R subseteq T_F`) on
edges internal to `R`.  Contracting components of `H-D` turns the missing
step into the augmented-quotient geometry described in `proofs/PROOFS.md`:
a deficient blocker must be found even when the quotient is cyclic and even
when its useful vertex set is mixed across `P` and several punctures.

The package controls rule out the three direct closures I tested:

1. **Always take `R=P`: false as a route.**  On O-56,
   `lambda_H(P)=|P|=2`, while the auxiliary pair `{2,3}` has blocker number
   one.
2. **Always take one puncture `R=B_s`: false.**  On O-64 the relevant
   puncture is `{u}` and has blocker number one, equal to its size; the
   deficient set is `P={s,t}`.
3. **Obtain adjacent maximal carriers and invoke CS(b): false at the Hall
   layer.**  The carrier-poset counterexample is reproduced in
   `LEMMA-A-CARRIER-POSET.md`, and the package-local finite scan below fires
   this negative control again.

These witnesses are not counterexamples to Lemma A°: each fails hereditary
tightness.  They show only that the proposed fixed localizations do not supply
CB.  They do not prove that CB is independent of the certified inputs.

The remaining obligations are therefore precise:

- in branch (H), convert a high-external-degree cycle vertex and its carrier
  hierarchy into a deficient blocker despite a possibly cyclic augmented
  forest quotient; or
- in branch (G), use the external-neighbour vertex cover of the clean cycle
  edges, together with CP's strict carrier hierarchy, to construct a mixed
  `R` and fewer than `|R|` blockers in `H`.

I found no valid construction for either obligation.  Stopping at this point
is necessary: asserting CB would simply restate the unproved content in
blocker language.

## 5. Controls-first machine verification

All generated test output was package-local.  The transient
`tools/forced-core*.txt` files were removed after their hashes and summaries
were recorded, so the committed phase-1 product does not alter the packaged
oracles.

### 5.1 Package integrity

The SHA-256 table in `MANIFEST.md` was parsed and recomputed before relying on
the artifacts:

```text
MANIFEST HASH CHECK: listed=25 failures=0
```

The frozen Lemma-A oracle `tools/forced_core.py` had the expected shipped hash

```text
ba8b0ba56f96e4d2095dd5254093852b361185652e40402be5b5114434154547
```

### 5.2 Negative and positive controls, run before target scans

An inline standard-library checker, run with the package as its working
directory, independently enumerated feasible selections, intersected them to
obtain the forced core, enumerated Hall-tight sets and canonical carriers,
computed exact FVS numbers, and computed `lambda_H` by enumerating subsets of
`H`.  It first produced:

```text
CONTROL pure-cycle: PASS feasible=1 forced_cycle_rank=1 beta(P)=1 A-I+-shape=yes
CONTROL acyclic-path: PASS feasible=1 forced_cycle_rank=0
O-56: PASS feasible=1 forced_rank=1 |P|=2 beta(P)=2 clean=2 sparse=True guarded=True
O-63: PASS feasible=6 forced_rank=1 |P|=2 beta(P)=2 clean=2 sparse=True guarded=True
O-64: PASS feasible=1 forced_rank=1 |P|=2 beta(P)=1 clean=2 sparse=True guarded=True
CONTROL false P-localization (O-56): FIRED
CONTROL false B_s-localization (O-64): FIRED
CONTROLS-FIRST SUITE: PASS
```

The blocker equivalence of Section 2 was checked for every `X subseteq S` on
the pure-cycle control and on O-56/O-63/O-64: 60 subset cases in total, with
zero disagreements between the two sides of the equivalence.  This is a
regression check, not the proof of the equivalence.

### 5.3 Hall-layer target scan for the new dichotomy

After the controls, I exhaustively enumerated all `2^16` incidence masks on a
labeled universe with four demand vertices, four capacity-two vertices, and
demand two.  There were 7,151 feasible systems, 2,934 with a cyclic forced
core, and 3,492 cyclic forced components.  For each component the checker
recomputed tight sets, canonical carriers, `U`, clean ends, external
neighbourhoods, and the branch classification.

```text
ABSTRACT TARGET S=4,H=4,all c=2: systems=7151 cyclic_systems=2934 forced_cycles=3492
CP_fail=0 CE_fail=0 residual_partition_fail=0
branches heavy=252 guarded_sparse=288 AIplus_shape=2952
controls P_intersect_U=2304 ADJ_false=1440
```

Here `AIplus_shape` means the heavy branch fails and some clean edge has two
externally inactive endpoints.  A-I+ rules out that class only when hereditary
tightness is present.  The other two counts are precisely branches (H) and
(G).  The scan is Hall-layer regression evidence only; no forest completion
or minimum-FVS premise was imposed.

### 5.4 Frozen Lemma-A oracle target scan

Finally, from inside `tools/`, I ran the preserved oracle exactly as documented:

```text
PYTHONHASHSEED=0 python3 forced_core.py 8
PYTHONHASHSEED=0 python3 forced_core.py 10
```

The `n=8` run found 2,186 instances and zero cyclic forced cores.  The `n=10`
run reproduced the package's stated instance count:

```text
forced_core n=10 DONE inst=116216 cyclic_core=0 nonforest=0 maxpath=8 noforced=57017
```

The SHA-256 of the complete `n=10` result file was

```text
63f5c271b4ab32975a998f1446500457128ac7dd5d5e0251ad5e3aa1f4f66724
```

This finite enumeration supports Lemma A° on that oracle universe but cannot
close either branch (H) or (G) in general.

## 6. Phase-1 conclusion

The derivation is complete through normalization, clean-end reduction, the
exact blocker equivalence, and the heavy/guarded-sparse dichotomy.  It fails at
CB: no certified result in the package converts the remaining carrier data
and augmented forest geometry into a deficient H-blocker, and the packaged
controls falsify the simplest fixed-localization substitutes.  Therefore this
file is a documented phase-1 failure, not a proof of Lemma A° and not a
counterexample.
