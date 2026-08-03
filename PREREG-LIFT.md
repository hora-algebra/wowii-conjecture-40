# FROZEN preregistration — the lifting inequality (ATTACK.md target 4)

Frozen 2026-08-03 on branch `attempt/2026-08-03-claude-opus-5-5047`, **before**
any output of the checker was inspected. Statements, universe, checker source
and its sha256 are fixed here; the run follows.

## Why this target

ATTACK.md item 4 of the open list: "The lifting inequality: for some minimum
OCT `T`, `ell(G) >= 2 tau(G-T) + |T| + 1`. OPEN, sufficient for the general case
given the bipartite case." Step 3 target 4: "prove it for some structured class,
or hunt counterexamples to it (a counterexample redirects the gap work — report
it as a result, it does not touch the conjecture)."

Nothing in `ledgers/` or `proofs/` records any computation on this statement.
The general -> bipartite step is the one reduction gap that is *not* covered by
Lemma A / Lemma B, and the only thing proved there is the coefficient-2 bound
(Theorem 5.2). So this is unmined ground.

## Setting and notation

`G` a finite simple graph, `n = |V|`. `f, b, p` as in the paper;
`tau = n - f`, `o = n - b`, `ell = n - p`. A *minimum OCT* is a vertex set `T`
with `|T| = o(G)` and `G - T` bipartite. All parameters are additive over
connected components; `p` counts isolated vertices as trivial paths. `tau(G-T)`
is the decycling number of the (bipartite) graph `G - T`.

## FROZEN STATEMENTS

**LIFT-A** (the exact ATTACK.md form). For every connected nonbipartite `G` on
`n >= 3` vertices there exists a minimum OCT `T` with

    ell(G) >= 2 * tau(G - T) + |T| + 1.

**LIFT-A-ALL** (universal variant, recorded to measure how existential LIFT-A
really is). The same inequality for **every** minimum OCT `T`.

**LIFT-P** (path-cover form). For every connected nonbipartite `G` on `n >= 3`
vertices there exists a minimum OCT `T` with

    p(G) <= p(G - T) ,   equivalently   ell(G) >= ell(G - T) + |T|.

**LIFT-P-ALL**. The same for every minimum OCT `T`.

**SV** (paper Definition 5.3, re-verified here as a cross-check against the
paper's `n <= 10` claim). For every connected nonbipartite `G` there is a vertex
`t` with `o(G - t) = o(G) - 1` and `p(G) <= p(G - t)`.

**Recorded implications** (proved here, not tested):
* `LIFT-P` at `G` together with the bipartite case for `G - T` implies `LIFT-A`
  at `G` with the same `T`. Indeed `ell(G) >= ell(G-T) + |T|` and, applying the
  bipartite case componentwise to the bipartite graph `B = G - T`,
  `ell(B) >= 2 tau(B) + c_e >= 2 tau(B) + 1` where `c_e >= 1` is the number of
  components of `B` containing an edge (Lemma 5.1 of the paper gives `c_e >= 1`).
* `LIFT-A` for all connected nonbipartite `G`, together with the bipartite case,
  implies Conjecture 40 in full: with `T` as in LIFT-A,
  `tau(G-T) >= tau(G) - |T|`, so
  `ell(G) >= 2 tau(G) - 2|T| + |T| + 1 = 2 tau(G) - o + 1`, i.e.
  `ell + o >= 2 tau + 1`.
* `SV` is neither implied by nor implies `LIFT-P` a priori (`SV` moves one
  vertex; `LIFT-P` removes a whole minimum OCT at once). Both are recorded.

## Universe (frozen)

* Exhaustive: every connected graph on `3 <= n <= 9` (`nauty geng -c -q n`),
  restricted to the nonbipartite ones. Expected connected-graph counts
  `2:1, 3:2, 4:6, 5:21, 6:112, 7:853, 8:11117, 9:261080` — the run must
  reproduce these totals or it is void.
* Exhaustive at `n = 10` (11,716,571 connected graphs) **if** the measured
  throughput at `n = 9` projects to under 6 hours single-process; otherwise a
  preregistered fallback: exhaustive over the first `k` graphs of `geng -c -q 10`
  in geng order with `k` fixed by the throughput measurement and reported as a
  prefix, not as exhaustive.
* `n = 11` is **not** attempted.

## Decision rules (frozen)

* Any graph failing LIFT-A is a **counterexample**: the run halts, the graph6
  string plus `ell`, `o`, all minimum OCTs and their `tau(G-T)` are written to a
  witness file, and the result is reported as FALSIFIED.
* Failures of LIFT-A-ALL / LIFT-P-ALL are **not** failures of the target
  statements; they are recorded as counts and the first witness is preserved.
* Any SV failure at `n <= 10` would contradict the paper's recorded verification
  and is treated as an engine bug until resolved; halt and preserve.
* Reported per `n`: number of connected graphs, number of nonbipartite ones,
  LIFT-A failures, LIFT-A-ALL failures, LIFT-P failures, LIFT-P-ALL failures,
  SV failures, the histogram of the best LIFT-A slack
  `max_T [ ell(G) - 2 tau(G-T) - |T| - 1 ]`, and the maximum number of minimum
  OCTs seen.
* No statement above may be edited after the first run output is read. If a
  statement turns out to be uninteresting, that is reported, not fixed.

## Checker

`work/lift.c`, compiled `cc -O2 -o lift lift.c`. It reuses the exact invariant
primitives of the project's frozen engine `verification/phase0.c`
(`decode_g6`, `is_forest`, `is_bip`, the `ham`/`dpc` path-cover DP) so that
`f`, `b`, `p` agree with the oracle by construction, and adds the OCT
enumeration and the lifting tests.

Gold suite that must pass before any sweep (`./lift gold`):

| graph | expected |
|---|---|
| `K_3` | `o=1`, unique min OCT, `tau(G-T)=0`, `ell=2`, LIFT-A slack 0 |
| `K_4` | `o=2`, `tau(G-T)=0`, `ell=3`, slack 0 |
| `K_5` | `o=3`, `tau(G-T)=0`, `ell=4`, slack 0 |
| `C_5` | `o=1`, `tau(G-T)=0`, `ell=4`, slack 2 |
| `C_7` | `o=1`, `ell=6`, slack 4 |
| `K_{2,2,2}` | `f=3, b=4, p=1` (matches phase0 gold), `o=2` |
| `K_{1,1,1,3}` | `f=4, b=4, p=1` (matches phase0 gold), `o=2` |
| bowtie | `o=1`, unique min OCT = the cut vertex, `ell=4`, slack 2 |

plus a cross-engine assertion on every swept graph: `f`, `b`, `p` recomputed by
the same routines as `phase0.c`, and the identity
`ell(G) = ell(G-T) + |T| + (p(G-T) - p(G))` checked for every enumerated `T`
(an internal consistency invariant, not a mathematical claim).

sha256 of the frozen checker is recorded in `work/LIFT-SHA256.txt`, written
before the first sweep.


---

## Post-run addendum (2026-08-03, after the sweep completed)

Recorded here, below the frozen section, so the preregistration above is not
edited. Results: LIFT-A, LIFT-A-ALL, LIFT-P and SV had **zero** failures over
every connected graph with `3 <= n <= 10` (11,716,571 graphs at n = 10; shard
counts sum exactly to the known total; 11,712,539 of them nonbipartite, matching
the paper's SV census). LIFT-P-ALL is **FALSIFIED**: 3 / 16 / 150 / 2,130
failures at n = 7 / 8 / 9 / 10, first witness recorded in
`work/lift-witness-n9.txt`. Best-`T` slack histogram at n = 10:
`{0: 52303, 1: 333485, 2: 1311405, 3: 3227682, 4: 3852977, 5: 2614879, 6: 317201, 7: 2607}`.
Maximum number of minimum OCTs on one graph: 105. `work/liftcheck2.py`, an
independently written engine, reproduces every field including the slack
histograms at n = 6, 7, 8.
