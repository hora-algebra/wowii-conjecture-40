# GIVEN RESULTS — certified machinery, citable without re-derivation

Package metadata (not part of any claim): each block below is reproduced
**verbatim** from the file and line range named immediately above it. These are
**statements only**. No proof, derivation, proof sketch, or route for NC, NCM,
CE, or A-I⁺ appears anywhere in this package, and the documents that carry
those derivations are not included. Each result is certified (§E) and may be
used as a given, without re-derivation, in a proof of `STATEMENT.md`.

---

## A. Notation used by the blocks in §C and §D

Reproduced verbatim from `LEMMA-A-CLEAN-END.md` lines 18–23, at blob
`35479e4327455d29a6ef705c22a04c4430366b37`, as frozen at commit `6def500`.
Nothing else from that file is included in this package except the two
statement blocks in §C and §D.

Forced-core cycle `F : s_1 − q_1 − s_2 − ⋯ − s_m − q_m − s_1` (`m ≥ 2`),
`P = {s_i}` its `S`-side, `Q = {q_i}` its `H`-side, `cyc(q_i) = {s_i, s_{i+1}}`.
Each `q ∈ Q` carries two forced incidences, so `c(q) = 2` and `q` is saturated
in every feasible selection. `A_s` is the canonical carrier, `B_s = A_s \ {s}`,
`U = ⋃_{s∈P} B_s`, `T_F = P ∪ U`. Write `Ext(s) = N_H(s) \ Q`.
Call `q ∈ Q` **clean** if `deg_U(q) ≤ 1` and **dirty** otherwise.

---

## B. NC and NCM

Reproduced verbatim from `PREREG-NC.md` lines 40–57, at blob
`96f9e511958e1d838e2fd5e42159349ab5a86f80`, as frozen at commit `2510e2b`
(frozen before the scan that tested it). Nothing else from that file is
included in this package.

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

---

## C. Corollary CE

Reproduced verbatim from `LEMMA-A-CLEAN-END.md` lines 81–85 (provenance as in
§A). CE and NCM are the same result under two names.

> **Corollary CE (clean ends of a maximal carrier) — MATHEMATICALLY PROVED.**
> Every forced-core cycle has a cycle vertex `s` — any one whose carrier is
> inclusion-maximal, which exists by CP — such that **both** forced ends `q` of
> `s` satisfy `N_S(q) ∩ (P ∪ U) = cyc(q)`. On a `T_F`-normalized instance both
> ends have `deg_S(q) = 2` exactly.

---

## D. A-I⁺

Reproduced verbatim from `LEMMA-A-CLEAN-END.md` lines 98–104 (provenance as in
§A).

> **A-I⁺ — MATHEMATICALLY PROVED.** Suppose there is a **clean** `q_0 ∈ Q` with
>
>   (1) `Ext(s) = ∅` for both `s ∈ cyc(q_0)`, and
>   (2) `|Ext(s)| ≤ 1` for every other `s ∈ P`.
>
> Then `τ(G[H ∪ P]) ≤ m − 1 < m = |P|`, contradicting hereditary FVS tightness.
> Hence no forced-core cycle of a Lemma-A° instance has this shape.

---

## E. Certification, and its true scope

One line per result, then the scope that applies to all of them.

* **NC** — CERTIFIED twice, independently: VERIFY-3 (branch
  `verify/2026-08-05-verify3`) and VERIFY-4 (branch
  `verify/2026-08-05-verify4`). Each verifier wrote and committed its own
  derivation under seal *before* opening the source document, then ran a
  controls-first finite oracle; both reported zero failures.
* **NCM / CE** — CERTIFIED by the same two runs; both record that the two
  names carry the same content.
* **A-I⁺** — CERTIFIED by the same two runs. VERIFY-4's phase-2 checker also
  enumerated the deletion-degree obligation and an independent
  forest-extension control, with a negative control that fires.

**True scope of those certifications.**

1. They certify *correctness relative to the certified prior stack* — paper §4,
   `proofs/PROOFS.md`, Lemma CS, CP, and the `T_F` normalization. Those inputs
   were re-read and spot-checked, not re-derived from scratch in those runs.
2. VERIFY-4 recomputed every derivation-dependent predicate on an explicit
   package-local labeled universe of 168,618 systems, 4,880 of them with a
   cyclic forced core, with all controls firing and zero failures. The
   historical `115,774 / 798 / 18` scan artifacts were not shipped to that
   verifier and were therefore **not** re-run by it; VERIFY-3 did reproduce the
   certified-anchor universes exactly.
3. NC, NCM, and CE are Hall-layer statements: they use `ρ`-tightness and the
   carrier machinery, not hereditary FVS tightness. A-I⁺ does use hereditary
   FVS tightness, and rules out one shape of forced-core cycle.
4. Neither certification claims that `STATEMENT.md` is closed, and neither
   grades these results as progress on it beyond what paper §4 already records.

---

## F. Imported definitions

**None required.** Every defined term and symbol occurring in §A–§D resolves
inside a document already included in this package. The closure was computed
mechanically; the resolution table is reproduced here for the prover's
convenience, with file and line provenance.

| term / symbol | resolved in | line |
|---|---|---|
| selection model: `S`, `H`, capacities `c`, incidences, feasible selection | `paper/paper.tex` — `\begin{definition}[Selection model]\label{def:selection}` | 250–257 |
| `deg_X(h)`, `ρ(X)`, `δ(X)` | `paper/paper.tex` | 301–304 |
| `ρ`-tight set (`δ(X)=0`), exposing | `paper/paper.tex` — `\begin{lemma}[Forced $\iff$ tight-set exposed, F1]\label{lem:F1}` | 327–331 |
| forced incidence / **forced core** | `paper/paper.tex` — "the \emph{forced core} is the graph of all forced incidences" | 324–325 |
| tight-set lattice | `paper/paper.tex` — `\begin{lemma}[Tight-set lattice]\label{lem:C6}` | 342 |
| tight-set saturation, `load^J_X(h)` | `paper/paper.tex` — `\begin{lemma}[Tight-set saturation]\label{lem:sat}` | 585 |
| **`A_s`** (canonical carrier) | `paper/paper.tex` — `\begin{lemma}[Common tight carrier]\label{lem:carrier}` | 599 |
| `A_s` (prose definition) | `LEMMA-A-CARRIER-POSET.md` — "`A_s` be the canonical carrier, the unique minimum Hall-tight set containing" | 13 |
| **`B_s`**, punctured tightness | `paper/paper.tex` — `\begin{lemma}[Punctured tightness]\label{lem:punct}` | 616–619 |
| `B_s` (prose definition) | `LEMMA-A-CARRIER.md` — "`s`), `B_s = A_s \ {s}`." | 20 |
| **forced ends** `q^-, q^+` of `s` | `LEMMA-A-CARRIER.md` | 76 |
| carrier–cycle separation (CS), incl. CS(a), CS(b) | `paper/paper.tex` — `\begin{lemma}[Carrier--cycle separation (CS)]\label{lem:CS}` | 634 |
| Lemma CS, full statement (a)–(d) | `LEMMA-A-CARRIER.md` — "**Lemma CS (carrier–cycle separation).**" | 38–52 |
| **CP**, inclusion-maximal carrier, `P\U` nonempty | `LEMMA-A-CARRIER-POSET.md` — "**Carrier-poset lemma (CP).**" | 16–23 |
| **`T_F` normalization** | `paper/paper.tex` — `\begin{lemma}[$T_F$ normalization]\label{lem:TF}` | 703 |
| hereditary FVS tightness | `paper/paper.tex` — `\begin{lemma}[Hereditary FVS tightness]\label{lem:C2}` | 282 |
| `τ` (`=\FVS`, decycling number / minimum FVS size) | `paper/paper.tex` — macro at line 22; prose at 137–138 | 22, 137–138 |
| `F`, `P`, `Q`, `cyc(q_i)`, `U`, `T_F`, `Ext(s)`, **clean** / **dirty**, `A_s`, `B_s`, `c(q)=2` | defined in the notation block of §A above | — |
| `N_S(q)`, `m` | defined in the block of §B above | — |
