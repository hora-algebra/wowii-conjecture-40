# STATEMENT — the claim to be certified

Package metadata (not part of the claim): the block below is reproduced
**verbatim** from `PREREG-NC.md` lines 40–57, at blob
`96f9e511958e1d838e2fd5e42159349ab5a86f80`, as frozen at commit `2510e2b`.
Nothing else from that file is included in this package. No proof, argument,
or derivation of the statement appears anywhere in this package.

---

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

## Imported definitions

**None required.** Every defined term and symbol occurring in the statement
above resolves inside a document already included in this package. The
closure was computed mechanically; the resolution table is reproduced here
for the verifier's convenience, with file and line provenance.

| term / symbol | resolved in | line |
|---|---|---|
| selection model: `S`, `H`, capacities `c`, incidences | `paper/paper.tex` — `\begin{definition}[Selection model]\label{def:selection}` | 250 |
| `deg_X(h)` (degree into a subset) | `paper/paper.tex` — "where `$\deg_X(h)$` is the number of neighbours of `$h$` in `$X$`" | 304 |
| `ρ(X)`, `δ(X)`, ρ-tight set | `paper/paper.tex` | 301–302, 329 |
| forced incidence / **forced core** | `paper/paper.tex` — "the \emph{forced core} is the graph of all forced incidences" | 325 |
| tight-set lattice | `paper/paper.tex` — `\begin{lemma}[Tight-set lattice]\label{lem:C6}` | 342 |
| **`A_s`** (canonical carrier) | `paper/paper.tex` — `\begin{lemma}[Common tight carrier]\label{lem:carrier}` | 599 |
| `A_s` (prose definition) | `LEMMA-A-CARRIER-POSET.md` — "`A_s` be the canonical carrier, the unique minimum Hall-tight set containing" | 13 |
| **`B_s`** | `LEMMA-A-CARRIER.md` — "`s`), `B_s = A_s \ {s}`." | 20 |
| punctured tightness | `paper/paper.tex` — `\begin{lemma}[Punctured tightness]\label{lem:punct}` | 616 |
| **forced ends** `q^-, q^+` of `s` | `LEMMA-A-CARRIER.md` | 76 |
| carrier–cycle separation (CS) | `paper/paper.tex` — `\begin{lemma}[Carrier--cycle separation (CS)]\label{lem:CS}` | 634 |
| **`T_F` normalization** | `paper/paper.tex` — `\begin{lemma}[$T_F$ normalization]\label{lem:TF}` | 703 |
| hereditary FVS tightness | `paper/paper.tex` — `\begin{lemma}[Hereditary FVS tightness]\label{lem:C2}` | 282 |
| `F`, `P`, `Q`, `cyc(q_i)`, `U`, `N_S(q)` | defined in the statement block above | — |
