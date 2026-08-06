# Graffiti.pc Conjecture 40: a deficiency form, a bipartite reduction, and verification to n = 11

This repository accompanies the note *"The Graffiti.pc conjecture
`f(G) >= ceil((p(G)+b(G)+1)/2)`: an equivalent deficiency form, a reduction of
the bipartite case to two finite lemmas, and exhaustive verification to n = 11"*
([paper/paper.pdf](paper/paper.pdf)).

For a connected graph `G` on `n` vertices, let `f(G)` be the maximum order of an
induced forest, `b(G)` the maximum order of an induced bipartite subgraph, and
`p(G)` the minimum number of vertex-disjoint paths covering `V(G)`. **WOWII
Conjecture 40** (DeLaviña's *Written on the Wall II* / Graffiti.pc list) states

```
f(G) >= ceil( (p(G) + b(G) + 1) / 2 ).
```

## What is proved

- **Equivalent deficiency form.** With `tau = n - f` (decycling number),
  `o = n - b` (odd-cycle transversal number), and `ell = n - p` (edges in a
  maximum spanning linear forest), the conjecture is equivalent to
  `ell + o >= 2*tau + 1`. For bipartite `G` this is `ell >= 2*tau + 1`.
- **Reduction of the bipartite case** to two explicitly stated lemmas (Lemma A on
  forced cores, Lemma B on cycle-erasing descent). All the surrounding structure
  is proved: a generalized Hall criterion, a rooted forest extension bound, a
  residual-augmentation flow theorem, and a descent argument.
- **Conditional general bound.** Conditional on the bipartite case,
  `ell + 2*o >= 2*tau + 1` (coefficient two).
- **Historical single-vertex reduction.** SV would have implied the full
  conjecture with the bipartite case, but SV is now falsified.

## Results since v2.0

- **SV is FALSIFIED at minimal order 11.** Certified minimal witnesses show
  that the paper's single-vertex route cannot prove the conjecture; the
  conjecture itself is untouched by those witnesses.
- **Lemma A is COMPUTATIONALLY VERIFIED through n = 14** (including
  2,391,365,507 instances at n = 14, with zero cyclic forced cores), and
  **F2-ALL is COMPUTATIONALLY VERIFIED through n = 13**. Neither finite
  verification is a general proof.
- **Lifting inequality progress and obstruction.** Structured sufficient
  LIFT-A classes L1--L7 are proved and their stated finite scans are clean,
  but the CX(m) family obstructs every threshold based only on component class
  sizes and full-side forest-extension invariants. Coefficient-one lifting
  remains open.
- **Lemma A endgame: machinery certified, lemma not.** The clean-end
  machinery (NC, NCM/CE, A-I⁺) is written up, independently re-derived, and
  CERTIFIED by two adversarial audits. Lemma A itself is **not** certified —
  no environmentally-blind audit of the full statement has been performed —
  and it remains open. See ATTACK.md item 1 for the exact scope of each
  verdict.
- **SAFE-2-EXISTS is the open core of the bipartite case.** Proved around it:
  SAFE-2-EXISTS ⟹ F2, HARD-SUCCESSOR-ONE ⟹ SAFE-2-EXISTS, the hard-state
  characterization, the transfer of Lemma A-I to selected cycles, and a
  no-free-lunch theorem showing every statement in the family must consume
  hereditary FVS tightness. The complete exhaustive n = 12 census (1,184 hard
  states) has been reproduced across two independent model vendors. None of
  it is a general proof.

## What is open

*AI or human and want to attack the open lemmas? Start at [ATTACK.md](ATTACK.md).*

- **Lemma A**, at the carrier-poset endgame — claimed, machinery certified,
  full statement neither proved nor blindly certified.
- **SAFE-2-EXISTS**, the remaining existential safe-toggle/descent statement
  for the bipartite reduction, now localized to the hard states.
- The general-to-bipartite step at **coefficient one** (`ell + o >= 2*tau + 1`).

## What is verified computationally

- Conjecture 40 holds for **all connected graphs on `2 <= n <= 11` vertices**
  (1,006,700,565 graphs at `n = 11`), with **zero violations**, under a
  preregistered, hash-frozen, dual-engine protocol (an exact C checker plus an
  independently coded second engine on every low-slack graph).
- SV holds through `n <= 10` and is **falsified at minimal order `n = 11`**.
- Lemma A and F2 are additionally summarized in “Results since v2.0”; the
  underlying branch reports preserve checker hashes, witnesses, and scope.

## Where each claim lives

| Claim | Location |
|---|---|
| Statement, proofs, conditional results | [paper/paper.tex](paper/paper.tex), [paper/paper.pdf](paper/paper.pdf) |
| Every theorem/number → its source | [paper/claims-to-sources.md](paper/claims-to-sources.md) |
| Full proof document (bipartite core) | [proofs/PROOFS.md](proofs/PROOFS.md) |
| Lemma A challenge sheet; Lemma B refinements | [proofs/LEMMA-A-CHALLENGE.md](proofs/LEMMA-A-CHALLENGE.md), [proofs/FROZEN-BPLUS2.md](proofs/FROZEN-BPLUS2.md) |
| Append-only computational ledgers | [ledgers/PHASE0_RECORD.md](ledgers/PHASE0_RECORD.md), [ledgers/RESULT_RECORD.md](ledgers/RESULT_RECORD.md) |
| Checkers, witness sets, per-shard counts, hashes | [verification/](verification/) (see [verification/README.md](verification/README.md)) |

## Reproducing the verification

```
cd verification
cc -O3 -o phase0 phase0.c
geng -c -q 10 | ./phase0 run1 0 100000     # nauty geng; n=10 (~11.7M graphs)
```

Enumeration uses `geng` from nauty (McKay & Piperno). Shard counts must sum to
the known number of connected graphs at each order. Every low-slack graph is
re-checked by the independent engine `phase0_verify2.py`. See
[verification/README.md](verification/README.md) for the checker-hash provenance.

## Data availability and citation

Release tag `v1.0` is archived at
**https://doi.org/10.5281/zenodo.21778700**. Source:
https://github.com/cozuya/wowii-conjecture-40. The `v2.0` data/release bundle is
pending Zenodo versioning.

## License

Code (the contents of `verification/`) is released under the **MIT License**
(see [LICENSE](LICENSE)). The paper and mathematical write-ups (`paper/`,
`proofs/`, `ledgers/`) are released under **CC BY 4.0**.

## Acknowledgment

The mathematics and computations were developed with AI assistance (Claude
models); all results were independently cross-checked computationally.
