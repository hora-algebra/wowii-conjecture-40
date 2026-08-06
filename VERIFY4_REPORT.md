# VERIFY4 REPORT

## Verdict

CERTIFIED

This verdict covers the mathematical derivations of NC, NCM/CE, and A-I⁺.
`SEALED-DERIVATION.md` and `LEMMA-A-CLEAN-END.md` agree on every shared
conclusion.  Their only materially different proof step is NC(ii), for which
they give two compatible and independently valid arguments.

## Audited inputs

| artifact | SHA-256 |
|---|---|
| `STATEMENT.md` | `c81880d63d2e702f102e122aaad7e9c26fe3f703da8d35aba324bcf0f33416f0` |
| `SEALED-DERIVATION.md` | `002c2dc87f9de51000d46bab000d506447d54c95495ef8ace374beff84d0e1dd` |
| `LEMMA-A-CLEAN-END.md` | `231205c7ae7c7287d12f3afc7b92f8872e6cdd8d7333bfb956e8f103ff4d7f5f` |
| `tools/verify_nc.py` | `b2ee1d2fcd910de44cf8c83c4257916efa8cecdba25ff74f229f71c0fbb0b110` |
| `tools/verify_phase2.py` | `14e1d2d2b03b33e73a3e3023e8b84044ca18139162a45b046a9140d5f80cc7d6` |

The phase-1 sealed commit is
`f2765aa4f9780955f4d995b0581aed19108b09b7`.  Before phase-2 target checks,
`shasum -a 256 -c tools/SHA256SUMS.txt` returned `OK` for all 17 shipped
entries.

## Step-by-step comparison

### 1. Cycle-end capacity and saturation

- Sealed derivation: the two forced cycle incidences at `q` occur in every
  feasible selection; capacities are at most two; therefore `c(q)=2` and those
  incidences saturate `q`.
- CLEAN-END: states the same fact in its notation block.

These are identical premises.  The finite oracle checked capacity two and load
two at all 10,360 enumerated cycle ends (`M1`).

### 2. NC(i): exclusion of a nonconsecutive cycle vertex

Both texts use the same chain.  If a cycle vertex `r∉cyc(q)` is adjacent to
`q`, then `q` is not a forced end of `r`.  Punctured tightness gives

    deg_{A_r}(q) ≥ c(q)+1 = 3.

Removing the adjacent vertex `r` gives `deg_{B_r}(q)≥2`; since `B_r⊆U`, this
contradicts `deg_U(q)≤1`.  The reverse inclusion
`cyc(q)⊆N_S(q)∩P` is definitional.

The checker confirmed the carrier/puncture predicates 10,360 times (`M2`) and
the exact implication “extra `P`-neighbour forces `deg_U≥2`” 450 times (`M4`).

### 3. NC(ii): two different valid routes

The sealed route is:

> `load_{B_s}^J(q) = min(2,1) = 1.`

If an auxiliary `u∈U\P` touches a clean `q`, choose a puncture `B_s` containing
`u`.  Then `deg_{B_s}(q)=1`.  Tight-set saturation forces the unique
`B_s`-to-`q` incidence into every feasible selection, making a third selected
incidence at the already saturated capacity-two vertex `q`.  This is a
contradiction.

The CLEAN-END route is:

> `They are consecutive on F with shared end q, so Lemma CS(b) gives deg_U(q) = 0 — contradicting deg_U(q) ≥ 1.`

If the auxiliary `w` is the unique `U`-neighbour of clean `q`, neither cycle
endpoint can lie in `U`; otherwise it would be a second, distinct
`U`-neighbour.  Both endpoints therefore lie in `P\U`, so CS(b) applies and
forces `deg_U(q)=0`, contradicting the presence of `w`.

The sealed saturation premise passed 148,552 `(tight set, selection,
H-vertex)` checks (`M3`).  The CLEAN-END CS(b) predicate passed at all 9,010
cycle ends whose two cycle vertices lie in `P\U`.  Both routes conclude the
same NC(ii), which passed at every one of 9,910 clean ends.

### 4. Degree identity and normalized conclusion

Both texts decompose `U` into its `P` and `U\P` parts.  NC(i) and NC(ii) give

    N_S(q)∩U = cyc(q)∩U,

hence `deg_U(q)=|cyc(q)∩U|`.  If `S=P∪U`, the same two parts exhaust `S`, so
`N_S(q)=cyc(q)` and `deg_S(q)=2`.

The checker confirmed these identities at all 9,910 clean ends.

### 5. NCM versus CE

The names differ, but the content agrees.  CP makes `P\U` the nonempty set of
maximal-carrier cycle vertices.  CS(a) makes both forced ends of every such
vertex clean.  Applying NC gives

    N_S(q)∩(P∪U)=cyc(q)

at both ends, and normalization turns this into `deg_S(q)=2`.  The combined
CP/CS(a)/NCM obligations passed 18,920 endpoint checks (`M7`).  Neither text
uses `P∩U=∅`, adjacent maximal carriers, or a globally zero `U`-degree
assumption.

### 6. A-I⁺, present only in CLEAN-END

Let `D=Q\{q_0}`.  The proof has four steps:

1. `|D|=m−1`, and `H−D` is a forest.
2. For `s∈cyc(q_0)`, hypothesis (1) leaves exactly the neighbour `q_0`, so the
   surviving degree is one.
3. For `s∉cyc(q_0)`, NC(i) excludes adjacency to `q_0`; hypothesis (2) leaves at
   most one external neighbour.
4. `P` is independent, so adjoining its degree-at-most-one vertices to the
   forest `H−D` cannot create a cycle.  Thus `D` is an FVS of size `m−1<m`,
   contradicting hereditary FVS tightness.

The phase-2 checker found 5,590 eligible `(cycle,q_0)` pairs in 2,720 cyclic
systems and checked all 12,530 resulting `P`-vertex degrees.  It then
independently enumerated all 339 labeled forests on at most five `H`-vertices
and 81,987 ways to adjoin at most three independent vertices with degree at
most one; every extension stayed acyclic.  A negative control in which the
adjoined vertex had two neighbours on one forest path produced a cycle, so the
test discriminates the degree-one condition.

## Controls-first machine record

Command:

    cd tools && python3 verify_phase2.py

Output:

    CONTROLS PASS: acyclic detector; ADJ threshold/PDIS controls fired; O-56/O-63/O-64 counts, cycles, carriers reproduced
    PHASE2 CONTROLS PASS: ADJ clean A-I+ degrees 1/0/1; dirty chord excluded; O-56/O-63/O-64 Ext guards fail; forest negative fires
    TARGET PASS: systems=168618 cyclic_systems=4880 cycles=4880 pdis_false=450 M1_cycle_capacity_and_load=10360 M2_carrier_puncture=10360 M3_tight_saturation=148552 M4_extra_P_forces_U_degree_two=450 M5_M6_NC_and_consequences=9910 M7_CP_CS_NCM=18920
    PHASE2 TARGET PASS: systems=168618 cyclic_systems=4880 cycles=4880 clean_q=9910 dirty_q=450 chords=450 clean_end_nc=9910 cs_b=9010 ai_plus_pairs=5590 ai_plus_systems=2720 ai_plus_extension_only_pairs=0 ai_plus_degree_checks=12530
    FOREST EXTENSION PASS: forests=339 leaf_attachment_checks=81987

The ADJ control remains sharp: its dirty `q=0` carries the extra chord, while
its clean `q=1` reproduces the A-I⁺ surviving degrees `1,0,1`.  O-56, O-63, and
O-64 reproduce their documented feasible-selection counts and carriers, pass
NC, and fail A-I⁺ hypothesis (1) through the documented external neighbour.

## Evidence boundary

The `work/0520` checkers and raw outputs cited by `LEMMA-A-CLEAN-END.md` are not
included in this package.  Consequently this audit does not independently
re-run its exact historical `115,774 / 798`, random-run, `528 / 798`, or
CAP2-BS census figures.  Instead, all derivation-dependent predicates were
recomputed with the package-local, controls-first oracle on the explicitly
defined 168,618-system labeled universe above.  The missing historical
artifacts limit reproduction of those numerical provenance claims; they do not
create a mathematical step failure in NC, NCM/CE, or A-I⁺.

One harness calibration expectation initially assumed this bounded universe
would contain an A-I⁺ case with a nonempty permitted `Ext` on the third cycle
vertex.  The observed count was zero.  That expectation is not a premise or
claim in either proof, so it was removed; the zero is retained in the final
output as `ai_plus_extension_only_pairs=0` rather than reinterpreted.
