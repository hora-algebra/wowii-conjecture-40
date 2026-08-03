# tools/ — lemma-level verification oracle

Frozen and supporting checkers for the **open** lemmas (A, B) and the incidence
model of paper §3. The conjecture-level checkers live in `../verification/`;
these operate one level down, on the incidence-selection model and the
forced-core / cycle-erasure machinery.

## Running

All checkers are pure Python 3 (standard library) **except** `inv40_a.py`, which
needs `networkx`. Enumeration shells out to `geng` from nauty (must be on
`PATH`). Run from **inside this directory** (Python puts the script's directory
on the import path, which is how the modules find each other):

```
cd tools
python3 forced_core.py 10        # Lemma A forced-core scan, connected bipartite n=10
```

Each checker enumerates connected bipartite graphs with `geng -bc -q N` and
writes a result file to the current directory.

## Checkers (what each verifies)

| tool | checks | input | output | frozen statement / ledger |
|---|---|---|---|---|
| `a1_verify.py` | the **shortest-path-only** Lemma B forms A1/U1 (now FALSIFIED at n=11) | `python3 a1_verify.py [N=10]` (geng `-bc -q N`) | `a1-verify.txt` | FROZEN-BPLUS2.md (A1/U1); ledger O-40 |
| `b_hslide.py` | **B-PLUS-2** (`dCES ≤ d0+2`) and the **terminal-slide** mechanism per selected cycle | `python3 b_hslide.py [N=12]` | `b-hslide.txt` | FROZEN-BPLUS2.md (B-PLUS-2 / B-TERMINAL-SLIDE) |
| `forced_core.py` | **Lemma A°**: the forced incidence core is acyclic | `python3 forced_core.py [N=10]` | `forced-core.txt` | paper §4.1; ledger O-44, O-47 |
| `eval_L1_holdout.py` | L1 Lemma-B holdout helpers (feasibility, components, cycle count) | `python3 eval_L1_holdout.py` (n=10) | `L1-holdout.txt` | FROZEN-BPLUS2.md |
| `b4_check.py` | B4 directed-residual-chord / shortcut targets on shortest bad paths | `python3 b4_check.py [N=10]` | stdout | PROOFS.md §E (B4, S-B4a/b/c) |
| `b4_split.py` | B4 split-target geometry (Case-P / Case-C, endpoint-return) | `python3 b4_split.py [N=10]` | stdout | PROOFS.md §E (B4 split) |
| `inv40_a.py` | invariants `(n,f,b,p)` — Engine A (networkx + brute Hamiltonian) | `import inv40_a; inv40_a.quad_from_g6(g6)` | return tuple | conjecture-40 invariants (cross-check) |
| `inv40_b.py` | invariants `(n,f,b,p)` — Engine B (odd-cycle branching + B&B linear forest) | `import inv40_b; inv40_b.quad(g6)` | return tuple | conjecture-40 invariants (cross-check) |

Supporting modules (imported by the checkers; not run directly):
`inv_b.py` (graph6 parser + bitmask invariants), `experiment_b.py` and
`experiment_b_dual.py` (incidence-model / dual-`ℓ₂` helpers), `eval_frozen.py`
(`min_fvs_all`, minimum feedback-vertex-set enumeration), `mine_n10.py`
(n=10 discovery helpers incl. `walk_cycle`).

## Witnesses (`witnesses/`)

Machine-readable certificates (adjacency lists + feasible-selection / tight-set
data) for the three warning instances of paper §4.1. Each JSON names, in its
`refutes` field, the localization strategy it kills:

- `O-56.json` — refutes **P-localization** (the violation is disjoint from the
  cycle's S-side P); single-external-blocker / acyclic-quotient subcase.
- `O-63.json` — refutes the **degree-2** and **degree≥3 ⇒ private-cycle**
  localizations; violation is the full punctured carrier, size-2 blocker, cyclic
  quotient.
- `O-64.json` — refutes **B_s-localization** (B_s is Hall-tight but carries no
  hereditary violation; the violation is on P); capacity-1 branch.

## Hash provenance (read before trusting a build)

`SHA256SUMS.txt` lists the sha256 of every file **as shipped here**. Four tools
were **frozen** during the project and their frozen-source hashes are published
in `../proofs/FROZEN-BPLUS2.md` and `../ledgers/RESULT_RECORD.md`. The
provenance of each was verified against those published hashes **before**
sanitization; the copies here differ from the frozen source only in hard-coded
absolute output paths (replaced by relative paths / the current directory) and,
for two files, a neutralized docstring — **never** in the checker logic (gold
values reproduce identically). Both hashes:

| tool | frozen-source sha256 (published, provenance-verified) | shipped-copy sha256 |
|---|---|---|
| `a1_verify.py` | `12d9d843a385c25a0c161f4db2cdbb26196587ae35ff8251b697efd6b0b6bbf9` | `c91bf3ec1e13e5a23e5fef9508c2c185b9cccd77480114e2b1cd7e2cff1837ce` |
| `b_hslide.py` | `54e13cace032de32f73e85e1bdf50614aa083fb9e3543eb74eb389f233aaca10` | `06ab7034531f6893bc4a1d5cdb7e0f5a2a228ff160cf4f1a07c993d1ae8f15de` |
| `inv40_a.py` | `e7989532bf001fcaf1be6bafc310330bb3549d2bfb53deef7721862acba21a81` | `88430606e554d3a70bd4fe9bab2a30379a66c31a50d42c94c57980bfcead52af` |
| `inv40_b.py` | `198ebb7e5c0d969d21e792c210ca49f08fd96cf8ea34f290a0933b1865f5bbbf` | `34a0b11c97f653590702209f7eeee85eb014be9ceb7f73c9ba4165bb66703c46` |

The frozen-source hash is the artifact that generated the recorded results; a
future run that re-freezes should hash its own build and record both.

## Preservation note

All verification checkers referenced by the frozen statements are present. The
project's exploratory search scripts (annealing / motif search) are **not**
included here — they are not verification oracles and their results were
superseded by exhaustive enumeration. If you find a ledger reference to a checker
that is not in this directory, treat it as **not preserved; reimplement against
the model spec in paper §3 / PROOFS.md** before relying on it.
