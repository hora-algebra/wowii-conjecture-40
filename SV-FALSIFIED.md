# SV is FALSIFIED at n = 11

Branch `attempt/2026-08-03-claude-opus-5-5047`, 2026-08-03.
ATTACK.md open item 3: *"SV (paper §5): every connected nonbipartite `G` has a
vertex `t` in some minimum OCT with `p(G) <= p(G-t)`. OPEN. Verified `n <= 10`."*
ATTACK.md Step 3 target 3: *"SV: prove it, or extend verification to n = 11."*
ATTACK.md: *"Falsifying any of them, with a verified witness, is equally a
success outcome."*

**SV is false.** The smallest counterexamples have 11 vertices; two explicit ones
are certified below. This does **not** touch Conjecture 40 — the paper is
explicit that "SV is a sufficient route, not a necessary one: a failure of SV
would not refute Conjecture 40" (§5, after Theorem 5.5) — and indeed both
witnesses satisfy Conjecture 40 with slack 4. What it does is **close the SV
route to the general case**: paper Theorem 5.5 (SV + bipartite case ⇒ full
conjecture) is now known to rest on a false hypothesis.

## The statement

**SV** (paper Definition 5.3). For every connected nonbipartite finite simple
graph `G` there is a vertex `t` lying in some minimum odd-cycle transversal of
`G` with `p(G) <= p(G-t)`, equivalently `ell(G) >= ell(G-t) + 1`.
A vertex `t` lies in some minimum OCT iff `o(G-t) = o(G) - 1`; call such a `t`
*eligible*. So SV fails at `G` exactly when every eligible `t` has
`p(G-t) < p(G)`.

## Witness 1 — 11 vertices, 15 edges (fewest edges found)

graph6 `J???FAWdVD?`

```
V = {0,...,10}
E = 0-7, 0-8, 0-9, 0-10,
    1-7, 1-10, 2-7, 2-10, 3-8, 3-9,
    4-8, 5-9, 6-10,
    7-9, 8-10
```

Measured (three independent engines, see below):

| quantity | value |
|---|---|
| `n` | 11 |
| `f` (max induced forest) | 9 |
| `b` (max induced bipartite) | 10 |
| `p` (path cover number) | **3** |
| `tau = n - f`, `o = n - b`, `ell = n - p` | 2, 1, 8 |
| Conjecture 40 slack `2f - (p + b + 1)` | 4 — the conjecture holds comfortably |
| eligible vertices `{t : o(G-t) = o(G)-1}` | **`{0}`**, exactly one |
| `p(G - 0)` | **2** |
| **SV** | `p(G) = 3 > 2 = p(G-0)` — **FAILS** |

Why the eligible set is a singleton, by hand: `0-7-9-0` and `0-8-10-0` are
triangles (the edges `7-9` and `8-10` are present), and they meet only in `0`.
Deleting any single vertex other than `0` leaves one of the two triangles
intact, so no other vertex is an odd-cycle transversal on its own; and `G - 0`
is bipartite (checked). Hence `o(G) = 1` and the unique minimum OCT is `{0}`.
SV therefore has no freedom at all here — its existential quantifier ranges over
one vertex, and that vertex fails.

Why `p(G) = 3` while `p(G - 0) = 2`: vertices `4, 5, 6` are pendants (on `8`,
`9`, `10` respectively). Three degree-1 vertices need three distinct path
endpoints, and a linear forest with `k` nontrivial paths has `2k` endpoints, so
`p >= 2` already. Adding `0` back — a degree-4 vertex all of whose neighbours
`7, 8, 9, 10` are needed as interior vertices of the two-path cover of `G - 0` —
costs one more path. The full values are machine-checked.

## Witness 2 — 11 vertices, 16 edges (the first one found)

graph6 `J???FBObs\?`

```
V = {0,...,10}
E = 0-7, 0-8, 0-9, 0-10,
    1-7, 1-8, 2-7, 3-8,
    4-9, 4-10, 5-9, 5-10, 6-9, 6-10,
    7-9, 8-10
```

Same profile: `f = 9`, `b = 10`, `p = 3`, `tau = 2`, `o = 1`, `ell = 8`,
Conjecture-40 slack 4; the same two triangles `0-7-9-0`, `0-8-10-0`; eligible
set `{0}`; `p(G - 0) = 2`. Here `{4,5,6} × {9,10}` is a `K_{3,2}`, which is what
pins the path cover.

## Verification

**Four** engines, all agreeing, on every witness — including *both* engines of
the paper's own dual-engine protocol, each verified against the repository's
published hashes first (`shasum -a 256 -c verification/SHA256SUMS.txt` →
**237/237 OK**, covering `phase0.c` = `17db663b…` and `phase0_verify2.py` =
`69bae704…`).

1. **`verification/phase0.c` mode `run2` — the project's own frozen engine**, the
   one used for the paper's SV verification. Compiled from the repository copy
   unmodified; its SV gold suite (`phase0 gold2`: `K_5`, `C_5`, `C_7`,
   `K_{1,1,1,3}`, `K_{1,2,4}`, triangle+pendant) prints `GOLD2 (SV) ALL PASS`
   and its invariant gold suite (`phase0 gold`) prints `GOLD ALL PASS` first.
   Output on each witness:
   ```
   J???FAWdVD? oG=1 pG=3 elig=1 minGain=-1
   J???FBObs\? oG=1 pG=3 elig=1 minGain=-1
   ```
   (`minGain = -1` is `min_t [p(G-t) - p(G)]` over eligible `t`; SV needs
   `>= 0`.)
2. **`work/lift.c`** (sha256 `c0cc2dd3…`, frozen and committed in `5e93527`
   before any sweep, gold suite `GOLD ALL PASS`) — found them, reports
   `SV_fail`.
3. **`verification/phase0_verify2.py` — the project's frozen *second* engine**,
   the independently coded pure-Python bitmask implementation used to re-check
   every low-slack graph in the paper. Driving its own `f_forest`, `b_bip` and
   `p_cover` primitives directly from Definition 5.3:
   ```
   'J???FAWdVD?'  f=9 b=10 p=3  o=1  eligible(t,p(G-t))=[(0, 2)]  SV=FAILS
   'J???FAWdUD_'  f=9 b=10 p=3  o=1  eligible(t,p(G-t))=[(0, 2)]  SV=FAILS
   'J???FBObs\?'  f=9 b=10 p=3  o=1  eligible(t,p(G-t))=[(0, 2)]  SV=FAILS
   ```
   So the falsification is certified by the same pair of engines, at the same
   hashes, that certified the paper's positive results.
4. **`work/liftcheck2.py`**, an independently written pure-Python engine —
   reports `SV_fail=1` on each, and prints the full per-vertex table
   `o(G-t), p(G-t)` for every `t`, from which the failure can be read directly.

## Minimality in `n`

SV holds for **every** connected nonbipartite graph on at most 10 vertices. That
is the paper's result, and this run reproduced it independently with an engine
written from Definition 5.3: 0 SV failures over all 272,209 connected
nonbipartite graphs with `3 <= n <= 9` and all 11,712,539 on `n = 10` — both
census counts matching the paper's exactly. So **11 is the minimum order of an
SV counterexample.**

## How common

Not rare. In the first 20,000 graphs of the single `geng` residue class
`3/1024` at `n = 11`, the frozen `phase0 run2` engine found **10** violations,
all with the same signature `o = 1`, `p = 3`, one eligible vertex,
`minGain = -1`. A census over the three preregistered residue classes
(`1/1024`, `2/1024`, `3/1024`; see `PREREG-LIFT-N11.md`) is reported in
`ATTEMPT_REPORT.md`.

## The family is uniform

All 19 witnesses found in residue class `3/1024` have the **identical**
signature:

    o = 1 ,  p = 3 ,  exactly one eligible vertex ,  p(G - t) = 2

with Conjecture-40 slack 4 (14 of them) or 2 (5 of them), and 15 to 19 edges.
Two attain 15 edges: `J???FAWdVD?` (Witness 1 above) and

    J???FAWdUD_ :  0-7, 0-8, 0-9, 0-10, 1-7, 1-10, 2-7, 3-8, 3-9,
                   4-8, 5-9, 6-10, 7-9, 8-10, 9-10

which `phase0 run2` also certifies (`oG=1 pG=3 elig=1 minGain=-1`), with
`G - 0` bipartite, `p(G) = 3`, `p(G-0) = 2`, and no other single vertex an
odd-cycle transversal.

## The mechanism, stated as a rule

Every witness found has `o(G) = 1` **with a unique minimum OCT**. When the
minimum OCT is unique, SV's existential quantifier is vacuous — there is exactly
one candidate `t` — so SV degenerates into the unconditional claim
`p(G) <= p(G - t)` for that one vertex. And an OCT vertex can perfectly well be
a vertex whose removal *helps* the path cover: here `0` is a high-degree hub
whose neighbours are all needed internally, so putting it back costs a path.

That suggests the repairable version, if one wants to keep this route:

> **SV′ (not tested here).** For every connected nonbipartite `G` there is a
> vertex `t` with `o(G-t) = o(G) - 1` and `ell(G) >= ell(G-t) + 1`, **or** `G`
> has a unique minimum OCT `{v}` and `ell(G) >= ell(G-v) + 1 - k` for a
> compensating `k` absorbed elsewhere in the induction.

I have not formulated, let alone tested, a working repair; the honest statement
is that SV as written is false and Theorem 5.5 needs a different hypothesis.
Note that the lifting inequality (ATTACK.md item 4), which is the other route
through the same gap, **survives**: LIFT-A and even the universal LIFT-A-ALL had
zero failures over every connected graph with `n <= 10` and over the
preregistered `n = 11` classes, including on these very witnesses (slack 4).

## Files

* `work/sv11/` — census output of `phase0 run2` over the preregistered classes,
  including `phase0-run2-VIOL.txt` with every witness found.
* `work/n11/s3/lift-witness.txt` — the first witness as recorded by `lift.c`
  during the preregistered holdout.
