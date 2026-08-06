# SEALED DERIVATION — VERIFY-4, phase 1

## Result

**Complete proof.** The NC primary claim and the NCM corollary in
`STATEMENT.md` follow from the certified carrier stack.  The proof does not
assume the false condition `P ∩ U = ∅`.  Hereditary FVS tightness and the
`T_F` normalization are not needed for the local NC implication; normalization
is used only to specialize its conclusion to all of `S`.

## Certified inputs used

All notation is that of `STATEMENT.md` and the included stack.

1. A feasible selection exists.  An incidence is forced when it occurs in every
   feasible selection (`paper/paper.tex`, Selection model and F1).
2. If `X` is Hall-tight, then for every feasible selection `J` and every
   `h ∈ H`,

       load_X^J(h) = min(c(h), deg_X(h)).                 (SAT)

   This is Tight-set saturation (`paper/paper.tex`, Lemma `sat`).
3. For every `s ∈ P`, its canonical carrier `A_s` is tight.  With
   `B_s=A_s\{s}`, punctured tightness says that `B_s` is tight, the only
   neighbours `v` of `s` satisfying `deg_{A_s}(v) ≤ c(v)` are the two forced
   ends of `s`, and every other neighbour `h` satisfies

       deg_{A_s}(h) ≥ c(h)+1.                             (PT)

4. Carrier--cycle separation CS(a) says that if `s ∈ P\U`, each forced end
   `q` of `s` has `deg_U(q) ≤ 1` (`paper/paper.tex`, Lemma `CS`).
5. The carrier-poset lemma CP says

       P\U = {s ∈ P : A_s is inclusion-maximal among the cycle carriers},

   and in particular `P\U ≠ ∅` (`LEMMA-A-CARRIER-POSET.md`).
6. On a `T_F`-normalized instance, `S=T_F=P∪U` (`paper/paper.tex`, Lemma
   `TF`).

## Proof of NC

Fix `q ∈ Q` with `deg_U(q) ≤ 1`.

The two incidences joining `q` to the two vertices of `cyc(q)` lie on the
forced-core cycle, so both occur in every feasible selection.  A feasible
selection has load at most `c(q)` at `q`, while every capacity is either one or
two.  Hence

    c(q)=2,                                                (1)

and the two forced cycle incidences saturate `q` in every feasible selection.

### NC(i): no additional cycle vertex

Suppose, for a contradiction, that some

    r ∈ (N_S(q) ∩ P) \ cyc(q)

exists.  The vertex `q` is not one of the two forced ends of `r`.  Since `r` is
adjacent to `q`, punctured tightness (PT), applied to `A_r`, gives

    deg_{A_r}(q) ≥ c(q)+1 = 3.                             (2)

The set `B_r=A_r\{r}` removes exactly the neighbour `r` from the degree at
`q`, so

    deg_{B_r}(q) = deg_{A_r}(q)-1 ≥ 2.                    (3)

But `B_r ⊆ U`, and therefore `deg_U(q) ≥ 2`, contradicting the hypothesis.
Thus `N_S(q)∩P ⊆ cyc(q)`.  The reverse inclusion holds by the definition of the
cycle `F`, so

    N_S(q) ∩ P = cyc(q).                                  (4)

### NC(ii): no auxiliary vertex of `U`

Suppose, again for a contradiction, that some

    u ∈ N_S(q) ∩ (U\P)

exists.  By the definition `U=⋃_{s∈P}B_s`, choose `s ∈ P` with `u ∈ B_s`.
Because `B_s ⊆ U` and `u` is a `q`-neighbour,

    1 ≤ deg_{B_s}(q) ≤ deg_U(q) ≤ 1;

hence `deg_{B_s}(q)=1`.  The puncture `B_s` is tight, so (SAT), (1), and any
feasible selection `J` give

    load_{B_s}^J(q) = min(2,1) = 1.                       (5)

The unique `B_s`-to-`q` incidence is therefore selected in `J`; it is the
incidence `u q`.  Since `u∉P`, this incidence is distinct from the two forced
cycle incidences at `q`.  Thus `J` would load at least three incidences onto the
capacity-two vertex `q`, contradicting feasibility.  Consequently

    N_S(q) ∩ (U\P) = ∅.                                  (6)

Equations (4) and (6) are exactly NC(i) and NC(ii).

### Consequences in NC

Decompose the neighbours of `q` in `U` according to whether they lie in `P`:

    N_S(q) ∩ U
      = (N_S(q) ∩ P ∩ U) ∪ (N_S(q) ∩ (U\P))
      = cyc(q) ∩ U.

Therefore

    deg_U(q) = |cyc(q) ∩ U|.

If the instance is `T_F`-normalized, then `S=P∪U`.  Equations (4) and (6)
therefore account for every `S`-neighbour of `q` and give

    N_S(q)=cyc(q),

so `deg_S(q)=|cyc(q)|=2`.

## Proof of NCM

By CP, `P\U` is nonempty.  Fix `s ∈ P\U`.  CS(a) applies to each of the two
forced ends `q` of `s` and gives `deg_U(q)≤1`.  NC, already proved, applies at
each end.  Hence

    N_S(q) ∩ (P∪U)
      = (N_S(q)∩P) ∪ (N_S(q)∩(U\P))
      = cyc(q),

whose size is two.  This proves every assertion of NCM. ∎

## Machine verification

### Integrity and controls

Before target testing, the command

    cd tools && shasum -a 256 -c SHA256SUMS.txt

reported `OK` for all 17 shipped entries.

The added independent checker is `tools/verify_nc.py`, SHA-256

    b2ee1d2fcd910de44cf8c83c4257916efa8cecdba25ff74f229f71c0fbb0b110

It directly enumerates feasible selections, intersects them to obtain forced
incidences, and computes `rho`, tight sets, canonical carriers, and punctures
from the package definitions.  Its controls execute before its target loop:

- a unique-selection acyclic system must have no forced-core cycle;
- the ADJ witness in `LEMMA-A-CARRIER-POSET.md` must reproduce its documented
  carriers, must falsify `P∩U=∅`, and must falsify NC(i) when the
  `deg_U(q)≤1` hypothesis is deleted (the offending end has `deg_U=2`);
- O-56, O-63, and O-64 must reproduce respectively 1, 6, and 1 feasible
  selections, a forced cycle, and their documented canonical carriers.

All controls passed before the target result was emitted.

### Target universe and obligations

The command

    cd tools && python3 verify_nc.py

then exhaustively checked a labeled abstract universe with `2≤|S|≤3`,
`2≤|H|≤5`, at least two neighbours per `S`-vertex, and either all capacities
two or exactly two capacity-one vertices.  Incidence-isolated `H`-vertices and
disconnected incidence graphs were retained.  Only feasible systems entered
the count.

Final output:

    CONTROLS PASS: acyclic detector; ADJ threshold/PDIS controls fired; O-56/O-63/O-64 counts, cycles, carriers reproduced
    TARGET PASS: systems=168618 cyclic_systems=4880 cycles=4880 pdis_false=450 M1_cycle_capacity_and_load=10360 M2_carrier_puncture=10360 M3_tight_saturation=148552 M4_extra_P_forces_U_degree_two=450 M5_M6_NC_and_consequences=9910 M7_CP_CS_NCM=18920

The checked obligations were:

| code | finite predicate checked | checks |
|---|---|---:|
| M1 | cycle ends have capacity two and load two in every feasible selection | 10,360 |
| M2 | canonical carriers and all punctured-tightness predicates used above | 10,360 |
| M3 | tight-set saturation for every enumerated tight set, feasible selection, and `H`-vertex | 148,552 |
| M4 | every additional `P`-neighbour at a cycle end forces `deg_U≥2` | 450 |
| M5/M6 | NC(i), NC(ii), the `deg_U` identity, and the normalized-neighbour conclusion at every eligible end | 9,910 |
| M7 | CP, CS(a), nonempty `P\U`, and NCM at all maximal-carrier ends | 18,920 |

This is regression evidence, not a substitute for the proof above.

### Reproducibility limitations and run repairs

The historical `work/carrier.py`, `work/b17e/carrier_poset.py`, and their raw
outputs are referenced by the included documents but are not shipped in this
package.  Therefore the historical `115,774 / 798 / 18` scan is **NOT CHECKED**
here.  The new checker states its own broader labeled universe explicitly and
does not claim that its different counts reproduce that missing generator.

The first invocation of the new checker failed before any control completed:
the available Python raised `AttributeError` for `int.bit_count()`.  Replacing
that call with the compatible `bin(x).count("1")` repaired the harness.  A
subsequent run passed the controls and all mathematical assertions but exposed
a count mismatch with an initial, unjustified historical-anchor assertion.
That mismatch was kept separate from the target predicates: the exact cause of
the historical generator difference is unresolved because its source is absent.
The checker was corrected to describe and freeze only its explicit universe,
after which the final run above exited successfully.
