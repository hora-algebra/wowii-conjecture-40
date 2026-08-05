# Preregistration — NC (clean-end chordlessness), attempt/…-claude-opus-5-0520

Frozen **before** the target scan. ATTACK.md v4 Step 2 ("freeze + hash the
checker first, gold-test it, then run") and Step 3 target 1 (Lemma A via the
carrier-poset endgame).

## 0. Frozen artefacts and hashes

```
ac1836d99ca5ad711feea9c717ab6b326cbfcc9f50be983bb069380b938a81a0  work/0520/engine0520.py
64ebfa3f789411bb1fdaf893e3eb54ad190409c9858a92467d1670e4d2fa4f93  work/0520/nc0520.py
b21f5b8d5b14c23f0853ad83535d601766b8a202996c620d2f64208f8d2e32de  work/0520/nccontrols0520.py
2a0d62e00e867306951730223c2063bc3950fa0f7d4da18169cfb14d536728f1  work/0520/ADJ-WITNESS-vendored.json
```

`ADJ-WITNESS-vendored.json` is copied verbatim from
`public/attempt/2026-08-05-codex-gpt-5-b17e` at commit
`9cd62bb9f36c6cd61d9d62d7fed77db38463c9b1`, path `work/b17e/ADJ-WITNESS.json`.
`engine0520.py` was anchored before this preregistration at
`ANCHOR systems=115774 cyclic=798 pdis=18`, matching `work/carrier.py` and
b17e's `carrier_poset.py` exactly.

## 1. Inherited, treated as binding

* **CP** (b17e, MATHEMATICALLY PROVED): for distinct `s,t ∈ P`, `t ∈ B_s`
  implies `A_t ⊊ A_s`; the carrier-containment digraph is acyclic; `P \ U` is
  exactly the set of inclusion-maximal cycle carriers and is **nonempty**.
* **CS(a)** (5047, PROVED): every `s ∈ P \ U` has `deg_U(q) ≤ 1` at both forced
  ends `q`.
* **CS(b)** (5047, PROVED): if `s_i, s_{i+1}` are consecutive on `F` and both
  lie in `P \ U`, then `deg_U(q_i) = 0`.
* **Punctured tightness** (paper Lemma 4.5): `B_s` is Hall-tight, the only
  `H`-neighbours `v` of `s` with `deg_{A_s}(v) ≤ c(v)` are the two forced ends
  `q^-, q^+`, and every **other** `H`-neighbour `h` of `s` satisfies
  `deg_{A_s}(h) ≥ c(h) + 1`.
* **ADJ is FALSIFIED** (b17e): binding boundary. I do **not** assume two
  adjacent inclusion-maximal carriers, nor a puncture-free endpoint
  (`deg_U(q) = 0`), nor `P ∩ U = ∅`.

## 2. The claims, stated exactly

Throughout: `F` a forced-core cycle
`s_1 − q_1 − s_2 − ⋯ − s_m − q_m − s_1` (`m ≥ 2`), `P = {s_i}`, `Q = {q_i}`,
`cyc(q_i) = {s_i, s_{i+1}}`, `U = ⋃_{s∈P} B_s`, `N_S(q)` the set of
`S`-neighbours of `q`.

> **NC (primary).** For every `q ∈ Q` with `deg_U(q) ≤ 1`:
>
>   (i)  `N_S(q) ∩ P = cyc(q)`  — no other cycle vertex is adjacent to `q`;
>   (ii) `N_S(q) ∩ (U \ P) = ∅` — no auxiliary vertex of `U` is adjacent to `q`.
>
> Consequently `deg_U(q) = |cyc(q) ∩ U|`, and on a `T_F`-normalized instance
> (`S = P ∪ U`) simply `N_S(q) = cyc(q)`, i.e. `deg_S(q) = 2`.

> **NCM (corollary).** `P \ U ≠ ∅`, and for every `s ∈ P \ U` both forced ends
> `q` of `s` satisfy `deg_U(q) ≤ 1` and hence NC's conclusion; so
> `|N_S(q) ∩ (P ∪ U)| = 2` at those ends.

**Proof, recorded before the scan.**

*(i)* Let `s_k ∈ P` with `s_k ∼ q` and `s_k ∉ cyc(q)`, `q = q_i`. The two forced
ends of `s_k` are `q_{k−1}` and `q_k`; `q = q_i` equals one of them only if
`k ∈ {i, i+1}`, i.e. only if `s_k ∈ cyc(q)`. So `q` is an `H`-neighbour of `s_k`
that is **not** a forced end of `s_k`. Punctured tightness therefore gives
`deg_{A_{s_k}}(q) ≥ c(q) + 1 = 3` (every `q ∈ Q` has `c(q) = 2`, being saturated
by its two forced cycle incidences). Since `s_k ∈ A_{s_k}` and `s_k ∼ q`,
removing `s_k` drops the degree at `q` by exactly one, so
`deg_{B_{s_k}}(q) ≥ 2`. But `B_{s_k} ⊆ U` because `s_k ∈ P`. Hence
`deg_U(q) ≥ 2`, contradicting `deg_U(q) ≤ 1`. ∎

*(ii)* Let `w ∈ U \ P` with `w ∼ q`. Then `w ∈ N_S(q) ∩ U`, so `deg_U(q) ≥ 1`;
with `deg_U(q) ≤ 1` this forces `N_S(q) ∩ U = {w}`. As `w ∉ P`, neither vertex
of `cyc(q)` lies in `U`, i.e. both lie in `P \ U`. They are consecutive on `F`
with shared end `q`, so CS(b) gives `deg_U(q) = 0` — contradicting
`deg_U(q) ≥ 1`. ∎

*NCM* is immediate: `P \ U ≠ ∅` is CP; CS(a) supplies the hypothesis of NC at
both ends of any `s ∈ P \ U`; and then `N_S(q) ∩ (P ∪ U) = cyc(q)` has size 2
because `cyc(q)` consists of two distinct cycle vertices (`m ≥ 2`). ∎

**What NC is not.** It says nothing about `H`-neighbours of `P` outside `Q`, so
it does **not** repair the `P`-local bridge (`τ(G[H ∪ P]) ≤ m−1`), which is a
recorded DEAD END refuted by O-55/O-56, and I do not use it that way.

## 3. Universe, controls, decision rules — fixed now

**Positive controls (gold test, run first).** O-56, O-63, O-64 and ADJ-1 must
each be recognised as carrying a cyclic forced core and must **pass** NC, NCM
and the CPR regression.

**Negative controls.** Each must FIRE at least once, or the harness is dead
code and the run is graded ABORTED-NO-VERDICT for that population:

| control | statement (known FALSE) | expected witness |
|---|---|---|
| `NC-ALL` | every `q ∈ Q` has `deg_U(q) ≤ 1` | ADJ-1, `q = 0`, `deg_U(0) = 2` |
| `CHORD-ALL` | every `q ∈ Q` has `N_S(q) ∩ P = cyc(q)` | ADJ-1, `q = 0`, `s2 ∉ cyc(0)` |
| `PDIS` | `P ∩ U = ∅` | 18 systems in the exhaustive universe |

**Target universes, in this order.**

1. `exhaustive 3 5` — all 115,774 abstract systems of
   `gen_exhaustive(|S| ≤ 3, |H| ≤ 5)`; expected 798 with a cyclic forced core
   and `PDIS` firing 18 times (published anchors).
2. `random 20000 1` — expected ≈547 cyclic (published anchor).
3. `random 400000 777` — expected ≈11,097 cyclic (published anchor).

**Decision rules.**

* Any NC or NCM failure ⟹ **NC is FALSIFIED**, my proof above is wrong; I
  report the first certificate verbatim, withdraw the lemma, and make no
  in-sample repair.
* Any CPR failure ⟹ a discrepancy against b17e's CP; reported as a
  discrepancy, not silently absorbed.
* Any published anchor (115,774 / 798 / 18 / 547 / 11,097) not reproduced ⟹
  the run is graded a TOOLING discrepancy and the mathematical grading is
  withheld.
* Zero NC failures across all three populations ⟹ NC is graded
  **MATHEMATICALLY PROVED** (on the proof above) **and COMPUTATIONALLY
  VERIFIED** with the universe stated explicitly. It is **not** graded as
  progress on Lemma A beyond what §4 claims.

## 4. What a success would and would not mean — fixed now

NC would strengthen the recorded consequence of CS(c) in two ways: it replaces
the known-false global hypothesis `P ∩ U = ∅` by the always-available
`deg_U(q) ≤ 1` (CS(a) + CP), and it strengthens the conclusion from
`N_S(q) ⊆ P` to `N_S(q) = cyc(q)`, which additionally forbids **chords from
other cycle vertices** — a phenomenon the project ledger
(`ledgers/RESULT_RECORD.md`, entry O-60) explicitly records as possible in
general ("`s` may have unselected chords to other `Q`-vertices").

It would **not** close Lemma A, and I preregister that I will not claim it does.
Lemma A needs a hereditary-FVS violation; NC lives entirely on the Hall layer,
and GAUNTLET.md §(ii) records why no Hall-layer statement can suffice alone.
