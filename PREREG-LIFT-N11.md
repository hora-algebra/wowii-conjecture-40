# FROZEN preregistration — n = 11 structured holdout for the lifting statements

Frozen 2026-08-03 on branch `attempt/2026-08-03-claude-opus-5-5047`, **before**
the run. This is a second, prospective test of the statements already frozen in
`PREREG-LIFT.md`, at an order that preregistration explicitly excluded
("`n = 11` is **not** attempted"). Nothing in `PREREG-LIFT.md` is edited; the
statements, the checker and its hash are carried over unchanged.

## Statements (unchanged, carried over verbatim from PREREG-LIFT.md)

**LIFT-A**, **LIFT-A-ALL**, **LIFT-P**, **LIFT-P-ALL**, **SV**, exactly as
frozen there. No statement has been altered since it was committed in `5e93527`,
which was before any sweep output existed.

The statement of interest is **LIFT-A-ALL** — `ell(G) >= 2 tau(G-T) + |T| + 1`
for *every* minimum OCT `T`. It survived the whole of `3 <= n <= 10`
(11,716,571 connected graphs) with zero failures, which is exactly the profile
this project's documented death pattern warns about: "plausible pattern, holds
n ≤ 10, frozen, killed at n = 11 by a sealed holdout" (ATTACK.md Step 2). So
n = 11 is the right place to try to kill it.

## Checker (unchanged, already hashed)

`work/lift.c`,
sha256 `c0cc2dd315144a0c9c64c875234e193fd8f700e01949ea6668964220a4d01c5e`
(recorded in `work/LIFT-SHA256.txt`, committed in `5e93527`). Not modified since.
Gold suite re-run before this holdout; it must print `GOLD ALL PASS`.

## Universe (frozen)

Exhaustive over the `nauty geng` residue classes

    geng -c -q 11 1/1024 ,  geng -c -q 11 2/1024 ,  geng -c -q 11 3/1024

— three of the 1024 classes of the 1,006,700,565 connected graphs on 11
vertices, so roughly 2.95 million graphs. This is a **structured holdout, not
exhaustive verification at n = 11**, and must be reported as such.

Class `0/1024` is deliberately **excluded**: a 6,000-graph prefix of the
sub-class `0/4096` was used to measure throughput before this document was
written, so those graphs are not fresh. (The measurement could not have tuned
anything — the statements were frozen days-of-work earlier and are unchanged —
but the exclusion removes the question.)

Rationale for the size: measured throughput at n = 11 is about 900 graphs/s per
process on the sparse end of the enumeration; three classes on three cores is
roughly half an hour, which is what the session has.

## Decision rules (frozen)

* A LIFT-A failure halts the run and is reported as **FALSIFIED**, with the
  graph6 string, `ell`, `o`, every minimum OCT and its `tau(G-T)` preserved in
  the shard's `lift-witness.txt`.
* LIFT-A-ALL / LIFT-P / LIFT-P-ALL / SV failures are counted, first witness
  preserved, and reported; they do not halt the run. A LIFT-A-ALL failure would
  be a genuine result (it would downgrade LIFT-A-ALL from a lead to a falsified
  statement) and must be reported as prominently as a LIFT-A failure would be.
* An SV failure at n = 11 is a **new** data point (the paper verifies SV only to
  n = 10) and must be reported as such, not treated as an engine bug.
* Reported per shard and in total: graphs, nonbipartite graphs, all five failure
  counts, the best-`T` slack histogram, and the maximum number of minimum OCTs.
* Partial completion is reported as a prefix of the named residue classes, with
  the graph count reached, and never described as exhaustive.
