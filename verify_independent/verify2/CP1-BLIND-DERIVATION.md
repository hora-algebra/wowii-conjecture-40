# CP-1 blind re-derivation (VERIFY-2, priority 1)

**Sealed before opening `LEMMA-A-CARRIER-POSET.md`.**
Target file SHA-256 at time of sealing (unopened):
`978fbbf43bc0d98711e741541bc828eb0acf99ade76e7a389c029ee8e57338db`

## Sources read before writing this

1. `README.md` (problem statement only).
2. `proofs/PROOFS.md` — §A (model/notation), §B, §C5 (generalized Hall,
   F1, canonical exposing set), §C5b, §C6 (tight-set lattice), §C7, §D
   (Lemma A: T_F normalization, Lemma A-I, Tight-Set Saturation,
   Exposing-Set Internal Saturation, **Common Tight Carrier**,
   **Punctured Tightness**, single-blocker, Mhat_h, O-64 caveat).
3. `PREREG-CARRIER-POSET.md` — the CP statement itself.

**Disclosure of partial leakage.** `PREREG-CARRIER-POSET.md` lines 27-29
contain a two-sentence proof sketch of the containment step: "`B_s` is
tight by punctured tightness and contains `t`; canonical minimality gives
`A_t subseteq B_s`, and `B_s` is a proper subset of `A_s`." I had read
this before deriving. It is a sketch of what I call Step 1 below. It
mentions no case split and gives no argument for distinctness,
acyclicity, or the `P\U` characterization. Those I derived unaided.

**Not read:** `LEMMA-A-CARRIER-POSET.md`, `work/b17e/carrier_poset.py`,
`ATTEMPT_REPORT.md` (b17e revision), `GAUNTLET.md` (b17e revision).

## Statement being derived

Setting: a Lemma-A° instance (bipartite `G`, `S` a minimum FVS, `H=G-S` a
forest, fixed edge `e`, capacities `c=2` except `c=1` on `e`'s two
endpoints) whose forced incidence core contains a cycle `F`, with cycle
sides `P subseteq S`, `Q subseteq H`. For `s in P`, `A_s` is the unique
minimum Hall-tight set containing `s` (Common Tight Carrier),
`B_s = A_s\{s}`, and `U = union_{s in P} B_s`.

> **CP.** For distinct `s,t in P`, if `t in B_s` then `A_t subsetneq A_s`.
> Consequently the digraph `D` on `P` with arc `s->t` iff `t in B_s` is
> acyclic, the carriers `{A_s : s in P}` are pairwise distinct, and
> `P\U = {t in P : A_t is inclusion-maximal among {A_s : s in P}}`.
> In particular `P\U != empty`.

## Facts imported (all PROVED in PROOFS.md, none of them mine)

- **(L1) Tight-set lattice (C6).** If `X`,`Y` are Hall-tight then `X&Y`
  and `XuY` are Hall-tight.
- **(L2) Exposure (F1, C5).** A tight `X` *exposes* the incidence
  `a=(s,h)` iff `s in X` and `deg_X(h) <= c(h)`.
- **(L3) Canonical exposing set (C5).** For a forced `a`, the canonical
  exposing set is the *inclusion-minimal* tight set exposing `a`; it is
  contained in every tight set exposing `a`.
- **(L4) Common Tight Carrier (§D).** For `s in P` with its two forced
  `F`-edges `f^-=(s,q^-)`, `f^+=(s,q^+)`: the canonical exposing sets
  coincide, `=: A_s`; and **for every tight `Y` with `s in Y`,
  `A_s subseteq Y`**. So `A_s` is the unique minimum tight set containing
  `s`.
- **(L5) Punctured Tightness (§D).** For `s in P`, `B_s = A_s\{s}` is
  Hall-tight.

Note `P != empty` and every `s in P` carries exactly two forced `F`-edges
with **distinct** `H`-ends (`F` is a cycle of the bipartite incidence
graph, so it has length `>= 4` and `|P|=|Q|=m >= 2`). Hence (L4) and (L5)
are available at every `s in P`. This is the only place cycle-hood is
used.

---

## Step 1 — the containment lemma

**Claim.** For distinct `s,t in P` with `t in B_s`: `A_t subsetneq A_s`.

*Proof.* `B_s` is Hall-tight by (L5). By hypothesis `t in B_s`. Since
`t in P`, (L4) applies at `t`: every tight set containing `t` contains
`A_t`. Taking `Y = B_s` gives

        A_t subseteq B_s.

Also `s in A_s` and `s notin B_s = A_s\{s}`, so `B_s subsetneq A_s`.
Chaining, `A_t subseteq B_s subsetneq A_s`, hence `A_t subsetneq A_s`. []

I found **no case split here.** The argument is uniform in the capacity
profile (all-capacity-2 vs. one capacity-1 pair): neither (L4) nor (L5)
distinguishes them, and Step 1 uses nothing else. It is also uniform in
whether `t`'s carrier meets `Q`, whether `s` and `t` are adjacent on `F`,
and whether `S` is independent.

## Step 2 — carriers are pairwise distinct

**Claim.** For distinct `s,t in P`, `A_s != A_t`.

*Proof.* Suppose `A_s = A_t`. Then `t in A_t = A_s`, and `t != s`, so
`t in A_s\{s} = B_s`. Step 1 then gives `A_t subsetneq A_s = A_t`,
impossible. []

## Step 3 — acyclicity of the containment digraph

**Claim.** `D` (arcs `s->t` iff `t in B_s`) is acyclic.

*Proof.* An arc `s->t` forces `t != s` (as `s notin B_s`), so `D` is
loopless, and by Step 1 every arc satisfies `A_t subsetneq A_s`. Along a
directed cycle `s_1 -> s_2 -> ... -> s_k -> s_1` we would get
`A_{s_1} subsetneq A_{s_2} subsetneq ... subsetneq A_{s_1}` (reading the
strict containments in the direction they point), i.e.
`A_{s_1} subsetneq A_{s_1}`. Contradiction. []

Equivalently: `s -> t` implies `|A_t| < |A_s|`, and a strictly decreasing
integer sequence cannot close up.

## Step 4 — the `P\U` characterization

Write `Max = {t in P : A_t is inclusion-maximal in {A_s : s in P}}`.

**(4a) `P\U subseteq Max`.** Contrapositive: let `t in P` with `A_t` not
maximal. Then there is `s in P` with `A_t subsetneq A_s`. Since
`A_t != A_s` we have `s != t`, and `t in A_t subseteq A_s`, so
`t in A_s\{s} = B_s subseteq U`. Hence `t notin P\U`. []

**(4b) `Max subseteq P\U`.** Contrapositive: let `t in P & U`. Then
`t in B_s` for some `s in P`, and `t != s` because `s notin B_s`. Step 1
gives `A_t subsetneq A_s` with `s in P`, so `A_t` is not maximal among the
cycle carriers, i.e. `t notin Max`. []

Together `P\U = Max`.

## Step 5 — nonemptiness

`P != empty` (it is the `S`-side of a cycle, `|P| >= 2`), so
`{A_s : s in P}` is a finite nonempty family of sets. Choose `s in P` with
`|A_s|` maximum. If `A_s subsetneq A_r` for some `r in P` then
`|A_s| < |A_r|`, contradicting the choice. So `A_s` is inclusion-maximal,
`s in Max = P\U`, and `P\U != empty`. []

(Alternative, independent of Step 4: `D` is a finite acyclic digraph by
Step 3, hence has a source-free... more precisely a vertex of out-degree
`0`; but out-degree `0` means `B_s & P = empty`, which is *not* the same
as `s notin U`. The cardinality argument above is the correct one and is
what I use. This is worth flagging because "acyclic digraph has a sink"
would give the wrong conclusion here — see the note below.)

### Note on a tempting wrong route to Step 5

`s notin U` means `s` lies in **no** `B_r` for `r in P`, i.e. `s` has
**in-degree 0** in `D`. A finite acyclic digraph does have a vertex of
in-degree `0`, so this route also closes — but only because `D`'s arc set
is exactly "`t in B_s` with `t in P`", so in-degree `0` in `D` is
equivalent to `s notin U & P`... and `U` may contain vertices of `S\P`,
which is harmless since we only ask about `s in P`. Both routes agree.
The cardinality argument in Step 5 avoids the bookkeeping entirely.

---

## Summary of my blind result

- Step 1 (the containment lemma, "CP-1") derived in three lines from
  Punctured Tightness + Common Tight Carrier minimality, with **no case
  split**.
- Steps 2-5 (distinctness, acyclicity, `P\U = Max`, nonemptiness) derived
  from Step 1 by elementary set/order reasoning, again with no case
  split. The only genuine two-case structure I found anywhere is the two
  **inclusions** of the set equality in Step 4, which is bookkeeping, not
  mathematics.
- **I did not find, and do not believe I needed, any "insertion-chain
  double-count" argument.** If the published proof contains a second case
  requiring one, then either (i) the published CP-1 is a strictly stronger
  statement than the one preregistered, or (ii) the published second case
  is redundant given (L4)+(L5). The diff will decide which.

Open risk I am aware of before diffing: my Step 1 leans entirely on (L4)'s
universal clause "*for every* tight `Y` containing `s`, `A_s subseteq Y`".
If that clause were only available for `Y` that additionally *expose a
forced `F`-edge at* `t`, Step 1 would break and a second case would be
needed. I checked PROOFS.md §D: the Common Tight Carrier lemma states and
proves the universal clause outright ("Moreover for any tight `Y`
containing `s` ... `A_s subseteq Y`"), because `A_s & Y` inherits exposure
from `A_s` by monotonicity of `deg`. So the universal clause is genuinely
available and Step 1 stands.
