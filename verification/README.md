# Verification artifacts

Exhaustive check of Conjecture 40 (`p(G) + b(G) + 1 <= 2 f(G)`) for all connected
graphs on `2 <= n <= 11` vertices, plus the Single-Vertex property for connected
nonbipartite graphs `n <= 10`. Zero violations at every order.

## Contents

- `phase0.c` — primary exact checker (`f`, `b`, `p` for `n <= 11`).
  - `gold` / `gold2`: gold tests. `reg`: regression over small connected graphs.
  - `run1 <shard-id> <sample-every>`: reads graph6 from stdin, checks the bound,
    writes per-shard accounting. Output directory is `$PHASE0_OUT` (default: the
    current directory).
  - Example: `geng -c -q 8 | ./phase0 run1 n8 1000`
- `phase0_verify2.py` — independent second engine (pure-Python bitmask), coded
  separately from `phase0.c`. `python3 phase0_verify2.py FILE ...` (graph6 per
  line) re-checks the bound and reports any violation.
- `accounting/` — per-shard counts. `n=11` was sharded into 192 residue classes
  (`phase0-n11-count-0.txt` … `-191.txt`) whose `count=` fields sum to exactly
  1,006,700,565; `phase0-n11-count-n8.txt`, `-n9.txt` are the `n=8,9` layers.
- `second-engine/` — second-engine re-verification results (`n11verify-*.txt`):
  32 chunks covering all `n=11` low-slack + sample, plus `VERn8`/`VERn9`.
- `witnesses/` — compressed low-slack witness sets (graph6 + slack) for
  `n = 8, 9, 10, 11`, and the `n = 10, 11` random samples.
- `SHA256SUMS.txt` — hashes of every file in this directory.

## Reproducing

```
cc -O3 -o phase0 phase0.c
geng -c -q 10 | ./phase0 run1 0 100000     # n=10 (nauty geng)
```
`geng` is from nauty (McKay & Piperno). Counts must match the known number of
connected graphs at each order (`n=8`: 11,117; `n=9`: 261,080; `n=10`:
11,716,571; `n=11`: 1,006,700,565).

## Checker hash provenance (important)

The results were produced by a **frozen** build of `phase0.c` whose source has
sha256 `bc7f614d90f421aa5a60d2791644c619230cb78216a943811327739d7225a464`.
The copy published here differs from that frozen source in **exactly two string
literals**: the hard-coded output directory was replaced by `$PHASE0_OUT`
(default current directory) to remove absolute paths and make the file portable.
This change touches only where output files are written, **not** the invariant
computation (`f`, `b`, `p`), and the gold tests pass identically. The published
`phase0.c` therefore has a different hash (see `SHA256SUMS.txt`); the frozen
`bc7f614d…` value is the one recorded in the ledgers as the artifact that
generated the results.
