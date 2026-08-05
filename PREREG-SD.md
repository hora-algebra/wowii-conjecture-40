# FROZEN preregistration — SCHEDULED DESCENT (SD) statements

Branch `attempt/2026-08-05-claude-opus-5-4d7a`. Frozen 2026-08-05 **before** any
SD scan was executed and **before** any n=11 witness data was inspected. The
statements below were derived only from the published quantifier of the Descent
Lemma (paper Lemma 3.12 / PROOFS.md C8) and from the *public* fact that the
shortest-path-only form A1 is FALSIFIED at n=11 with exactly 6 positive-gap
cycles. No n=11 witness graph, selection, or cycle was examined before freezing.

---

## 0. Setting (identical to FROZEN-A1-U1.md and `tools/b_hslide.py`)

`G` connected bipartite, `tau(G) = |S| >= 2`, `S` a minimum FVS, `H = G - S` a
forest, `e = (x,y)` a fixed edge of `H`; each `s in S` has demand 2; `c(h) = 2`
except `c(x) = c(y) = 1`. `J` ranges over **all** feasible selections. `cyc(J)` is
the set of selected cycles (cyclic components of the incidence graph). An
incidence `a` on a cycle is **avoidable** iff the residual BFS after deleting `a`
reaches a residual-capacity `H`-terminal. For a selected cycle `C`:

- `d0(C)` = minimum residual augmenting-path length over the avoidable incidences
  of `C`;
- a toggle is **CES for `C`** iff `C` is destroyed and every cycle of the new
  selection was already a cycle of `J` (the semantic definition);
- **`A1(C)`** := some residual augmenting path of length exactly `d0(C)`, over the
  avoidable incidences of `C` attaining `d0(C)`, is CES for `C`.

`A1(C)` is exactly the per-cycle predicate `shortest_ces` computed by the frozen
`tools/b_hslide.py` and by `tools/a1_verify.py`.

## 1. The motivating observation (status: MATHEMATICALLY PROVED, trivial)

**Claim SD-REDUCTION.** Let

> **SD** — for every `(G, S, e)` in the setting above and every feasible `J` with
> `cyc(J) != empty`, **there exists** a selected cycle `C in cyc(J)` and a CES
> toggle for `C`.

Then SD implies F2, hence the bipartite case `ell >= 2 tau + 1`, **without Lemma
A and without Lemma B**.

*Proof.* Initial feasibility for every `e` is unconditional (rooted forest
extension + generalized Hall). The Descent Lemma is stated with exactly the
hypothesis "from every feasible selection with a selected cycle, some CES toggle
exists"; SD is that hypothesis verbatim. A CES toggle strictly lowers
`|cyc(J)|`, a nonnegative integer, so iteration terminates at a feasible `J` with
`cyc(J) = empty`; fixed-edge parity makes `J u {e}` acyclic; the degree count
gives a spanning linear forest with `2|S| + 1` edges. ∎

`A and B` imply SD (A makes every cycle eligible, B erases every eligible cycle),
so SD is a **strictly weaker** hypothesis than the pair currently being attacked:
it replaces "*every* cycle of *every* selection is erasable" by "*some* cycle of
every selection is erasable". Lemma A is not needed at all under SD.

This is an unpackaging of the published Descent Lemma, not new mathematics; it is
recorded because it is what makes the statements below worth testing.

## 2. FROZEN STATEMENTS

Quantified over: every connected bipartite `G` on `n` vertices, every minimum FVS
`S` with `|S| >= 2`, every `e in E(H)`, every feasible selection `J` with
`cyc(J) != empty`.

- **SD-SHORT** — there exists `C in cyc(J)` with `A1(C)` true.
- **SD-COUNT-SHORT** — there exist `C in cyc(J)`, an avoidable incidence `a` on
  `C` attaining `d0(C)`, and a residual path of length `d0(C)` for `a`, whose
  toggle `J'` satisfies `|cyc(J')| < |cyc(J)|`.
- **SD-PLUS-2** — there exists `C in cyc(J)` admitting a CES residual path of
  length `<= d0(C) + 2`.

Implications (so a single run grades all three):
`A1-ALL` (the falsified statement: `A1(C)` for **every** `C`) ⟹ SD-SHORT ⟹
SD-COUNT-SHORT, and SD-SHORT ⟹ SD-PLUS-2. Each of SD-SHORT, SD-COUNT-SHORT,
SD-PLUS-2 implies SD (hence F2, hence the bipartite case) on the universe where
it is verified.

**Also recorded, not frozen as a conjecture** (descriptive, for the report): for
every `J` containing at least one `A1`-failing cycle, the value `|cyc(J)|` and how
many of its cycles are `A1`-good. This is the mechanism datum that decides whether
scheduling can buy anything at all at the shortest-path level.

## 3. Checker, controls, and anchors

Checker: `work/sd/sd_scan.py`, sha256 recorded in `work/sd/SD-SHA256.txt`,
frozen and committed **before** the n=11 run. It imports the frozen engine
(`inv_b`, `experiment_b`, `eval_frozen`, `eval_L1_holdout`, `mine_n10`,
`a1_verify`) so that its per-cycle `A1` predicate is bit-identical to
`tools/b_hslide.py`'s.

**Positive control / anchor (must reproduce, or the run is void).**

| order | cycle components | A1-ALL failures (= positive-gap cycles) |
|---|---|---|
| n = 9 | 24,195 | 0 |
| n = 10 | 448,577 | 0 |
| n = 11 | 8,202,633 | **6** |

The n=11 row is the published figure from `proofs/FROZEN-BPLUS2.md` and
`tools/README.md`. Reproducing `A1-ALL failures = 6` at n=11 is simultaneously
the checker's positive control and the negative control for the new statement:
the same code path that yields `6` under `for all` yields the SD verdict under
`there exists`.

**Negative controls (must fire).** Run with two deliberately broken predicates on
n = 9:
- `is_ces` forced to always-True → SD-SHORT failures must be 0 and A1-ALL
  failures must be 0 (checker cannot report a failure it should not);
- `is_ces` forced to always-False → SD-SHORT failures must equal the number of
  cyclic feasible selections, and A1-ALL failures must equal the number of cycle
  components (24,195). A checker that does not fire here is not measuring
  anything.

**Universe anchor.** connected bipartite graph counts from `geng -bc -q n` must
be 730 (n=9), 4,032 (n=10), 25,598 (n=11).

## 4. Decision rules (fixed now)

1. Run n = 4..10 first as regression. **Any** SD-SHORT or A1-ALL failure at
   n <= 10 voids the run (A1 is known to hold exhaustively through n = 10).
2. Then run n = 11 exhaustively, sharded by graph index over 8 shards; shard
   cycle-component counts must sum to 8,202,633.
3. Verdicts:
   - SD-SHORT with 0 failures over n <= 11 → **COMPUTATIONALLY VERIFIED
     (n <= 11)**; it is then the weakest statement in this project known to
     close the bipartite case, and survives the exact order that killed A1. The
     next holdout is n = 12 (the aborted B-PLUS-2 universe).
   - SD-SHORT with >= 1 failure at n = 11 → **FALSIFIED**, minimal order 11,
     with every failing `(g6, S, e, J, cycles)` preserved verbatim. Then
     SD-COUNT-SHORT and SD-PLUS-2 are graded on the same run.
4. No statement in §2 will be edited after any output is seen. Partial-progress
   counters are operational only; failure counts will not be used to retune a
   statement. Any failure is preserved with the full certificate and
   re-verified by the independent `work/sd/wit_verify.py`-style recomputation
   before being reported.
5. Anything unfinished at wrap-up is reported ABORTED-NO-VERDICT with its
   shard-level checkpoint state on disk.

## 5. What each outcome would mean (fixed now, so it cannot be rationalised later)

- **SD-SHORT survives n = 11.** The A1 falsification is an artefact of the
  universal quantifier over cycles, not of shortest paths. The correct Lemma-B
  target becomes a *scheduling* statement, and Lemma A becomes unnecessary. This
  would be the first reduction of the bipartite case to a single statement.
- **SD-SHORT dies at n = 11.** Scheduling by cycle choice buys nothing at the
  shortest-path level: the six A1-failing cycles sit in selections with no
  A1-good cycle to fall back on. The scheduled-descent route must then use
  longer paths (SD-PLUS-2) or lookahead over several moves, and the `d0 + 2`
  slide is doing essential work rather than cosmetic repair. This is a real
  constraint on target (b) and is reported as such.

---

## 6. ADDENDUM — ONE-CYCLE (added 2026-08-05, after the n <= 9 regression, before n = 10 and n = 11)

**Provenance, stated exactly.** The regression runs mandated by §4.1 (n = 6, 7,
8, 9) returned `cycle_components == cyclic_selections` at every order, with
selected-cycle-count histogram `{1: all}`. That is: **no feasible selection at
n <= 9 has two selected cycles.** This was not anticipated when §2 was frozen.
The statement below is therefore formulated **IN SAMPLE with respect to
n <= 9**; n = 10 and n = 11 are prospective for it, and are run without any
further inspection of n <= 9 detail.

**ONE-CYCLE.** For every connected bipartite `G`, every minimum FVS `S` with
`|S| >= 2`, every fixed edge `e in E(H)`, and every feasible selection `J`, the
incidence graph `J u {e}` has **at most one** cyclic component.

**Counter control (run before freezing this addendum, passed).** On hand-built
selections the frozen `eval_L1_holdout.comps` / `ncyc` return 2, 1 and 0 cyclic
components respectively for a two-cycle, a one-cycle and an acyclic selection. So
"always 1" is a property of the universe, not an artefact of the counter.

**Consequences if ONE-CYCLE holds on a universe.** On that universe:

- (C1) SD-SHORT is **equivalent** to A1-ALL, SD is **equivalent** to Lemma B
  restricted to that universe, and *scheduling by choice of cycle is vacuous* —
  there is never more than one cycle to choose between. Target (b) of ATTACK.md
  v3 must then order something other than cycles.
- (C2) The descent has length `<= 1`: one CES toggle from any cyclic feasible
  selection already lands on an acyclic one.
- (C3) The descent potential `|cyc(J)|` takes only the values 0 and 1, so F2 is
  exactly "some feasible selection has `|cyc(J)| = 0`", and every intermediate
  "fewer cycles" bookkeeping in the project's Lemma-B analysis is bookkeeping
  about a two-valued quantity.

**Decision rule.** ONE-CYCLE is graded on the same runs as §2 via the
`ncyc_histogram` field. Any selection with `>= 2` cycles at n = 10 or n = 11
FALSIFIES it and is preserved verbatim. If it survives n <= 11 it is reported as
COMPUTATIONALLY VERIFIED (n <= 11), CONJECTURAL in general — explicitly NOT
proved, and explicitly at risk of the project's documented "holds to n <= 10,
dies at n = 11 or 12" pattern; n = 12 is its first untouched holdout.
