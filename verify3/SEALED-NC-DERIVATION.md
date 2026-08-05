# VERIFY-3 sealed derivation — NC (clean-end chordlessness)

Written and committed BEFORE opening `LEMMA-A-CLEAN-END.md` (target,
branch `attempt/2026-08-05-claude-opus-5-0520`, head `6def500`).
Verifier: Claude Fable 5, 2026-08-05.

## 0. Contamination log (two events, disclosed before use)

The protocol allowed reading ONLY: the claimed statement from the target
branch's ATTEMPT_REPORT status line; the certified prior stack (paper §4,
PROOFS.md, LEMMA-A-CARRIER.md, LEMMA-A-CARRIER-POSET.md, T_F normalization);
and PREREG-NC.md's frozen statement.

* **Event 1.** Extracting the claimed statement, I displayed
  `ATTEMPT_REPORT.md` lines 112–126. The statement blockquote ends at
  line 121; lines 123–126 are the report's compressed proof sketch
  ("Proof in two lines each: a chord from `s_k ∉ cyc(q)` makes `q` a
  non-forced-end neighbour of `s_k`, so punctured tightness forces
  `deg_{A_{s_k}}(q) ≥ 3`, hence `deg_{B_{s_k}}(q) ≥ 2` with
  `B_{s_k} ⊆ U` — contradicting cleanliness; and an auxiliary
  `w ∈ U \ P` at `q` would make both cycle vertices of `q` lie in
  `P \ U`," — cut off mid-sentence by my window). I read them.
* **Event 2.** I read ALL of `PREREG-NC.md` at freeze commit `2510e2b`,
  which contains not only the frozen statement (§2 blockquotes) but the
  full recorded proof of NC(i), NC(ii), and NCM. "PREREG-NC.md's frozen
  statement" plausibly meant §2's statement alone; I resolve the
  ambiguity against myself and log this as a breach.
* Also unavoidably visible: the branch's `git log` subject line
  ("NC clean-end chordlessness: proof, prospective verification (14,699
  cyclic systems, 0 failures), A-I+ corollary, CAP2-BS exploratory
  record, and the carrier.py census discrepancy") and the
  ATTEMPT_REPORT's section-heading list (claim titles + grades only).

**Consequence.** This derivation is NOT blind: the author's proof route
for NC was seen before it was written. What this document still
certifies independently: (1) every inference below was re-derived and
checked by me against the certified prior stack, with each step's exact
dependency named; (2) gap-hunting was done adversarially (edge cases
m=2, multiplicity of forced edges at s, the exact-drop-by-one step);
(3) the machine confirmation (fresh checkers, written from statements
only) is fully independent of the target's code, which I have not read.
`LEMMA-A-CLEAN-END.md` itself remains unread at commit time; the
step-by-step diff in the next phase is against THIS text.

## 1. The claim (verbatim, from the two allowed sources)

From ATTEMPT_REPORT status line/heading:
"### NC (clean-end chordlessness) — MATHEMATICALLY PROVED,
COMPUTATIONALLY VERIFIED", with statement blockquote:

> Call `q ∈ Q` **clean** if `deg_U(q) ≤ 1`. If `q` is clean then
> `N_S(q) ∩ P = cyc(q)` and `N_S(q) ∩ (U \ P) = ∅`; hence
> `deg_U(q) = |cyc(q) ∩ U|`, and on a `T_F`-normalized instance `N_S(q) = cyc(q)`,
> i.e. `deg_S(q) = 2`.

From PREREG-NC.md §2 (frozen statement):

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

The two statements agree (the report's "clean" is the prereg's
`deg_U(q) ≤ 1` hypothesis).

## 2. Setting and standing hypotheses

Abstract incidence system: finite `S` (demand 2 each), finite `H`,
bipartite incidence graph `S`–`H`, capacities `c(h) ∈ {1,2}`. Feasible
selection `J`: each `s` gets exactly 2 distinct incidences, each `h` at
most `c(h)`. **Standing hypothesis: the system is feasible** (some `J`
exists). Forced incidence: one lying in every feasible `J`. Forced
core: the graph of all forced incidences. `ρ(X) = Σ_h min(c(h),
deg_X(h))`, `δ = ρ − 2|X|`, tight means `δ(X)=0` (Hall tightness).

`F = s_1−q_1−s_2−⋯−s_m−q_m−s_1` (`m ≥ 2`) a cycle of the forced core;
`P = {s_i}`, `Q = {q_i}`, `cyc(q_i) = {s_i, s_{i+1}}` (indices mod m),
`A_s` the canonical carrier, `B_s = A_s \ {s}`, `U = ⋃_{s∈P} B_s`.
All vertices of F are distinct (F is a cycle of a max-degree-2 graph:
PROOFS.md §D / LEMMA-A-CARRIER.md §1).

Certified inputs used (each PROVED in the prior stack):

* **[PT]** Punctured tightness (paper Lemma 4.5 = lem:punct; PROOFS.md
  §D): `B_s` tight; the only `H`-neighbours `v` of `s` with
  `deg_{A_s}(v) ≤ c(v)` are the two forced ends `q^−, q^+`; every other
  `H`-neighbour `h` of `s` has `deg_{A_s}(h) ≥ c(h)+1`.
* **[CS(a)]** (paper lem:CS(a); LEMMA-A-CARRIER.md §1): for
  `s ∈ P\U`, both forced ends `q` of `s` have `deg_U(q) ≤ c(q)−1 = 1`.
* **[CS(b)]** (paper lem:CS(b)): if consecutive `s_i, s_{i+1}` both lie
  in `P\U`, then `deg_U(q_i) = 0`.
* **[CP]** Carrier-poset lemma (LEMMA-A-CARRIER-POSET.md, b17e):
  `t ∈ B_s ⟹ A_t ⊊ A_s`; `P\U` = the inclusion-maximal cycle
  carriers; `P\U ≠ ∅`.
* **[CC]** Common tight carrier (paper lem:carrier): `A_s` is the
  unique minimum tight set containing `s`; exists for every `s ∈ P`.

Boundary respected: ADJ is FALSIFIED (b17e) — nothing below assumes two
adjacent maximal carriers, a `deg_U(q)=0` endpoint, or `P ∩ U = ∅`.

## 3. Preliminary facts (derived, with dependencies)

**P0 (two forced edges at each `s ∈ P`, and they are the F-edges).**
Each `s ∈ P` carries the two forced F-incidences `(s,q^−), (s,q^+)`
(distinct since F is a cycle with all vertices distinct). It carries no
third forced incidence: `s` has demand exactly 2, so a feasible `J`
(which exists) selects exactly 2 incidences at `s` and contains every
forced incidence — three forced incidences at `s` would be
unsatisfiable. Hence [PT]'s "two forced ends" at `s ∈ P` are exactly
`q^− = q_{i−1}`, `q^+ = q_i` for `s = s_i`. *(Deps: feasibility,
definition of forced.)*

**P1 (`c(q) = 2` for every `q ∈ Q`).** `q_i` carries the two forced
incidences `(s_i, q_i), (s_{i+1}, q_i)`, both selected in every
feasible `J`; so `load_J(q_i) ≥ 2`, hence `c(q_i) ≥ 2`; capacities are
at most 2, so `c(q_i) = 2`. *(Deps: feasibility, capacity model.)*

**P2 (forced-end indexing).** For `q = q_i ∈ Q` and `s_k ∈ P`: `q_i`
is a forced end of `s_k` iff `i ∈ {k−1, k}` (mod m) iff
`k ∈ {i, i+1}` (mod m) iff `s_k ∈ cyc(q_i)`. *(Deps: P0, definition of
`cyc`.)*

**P3 (`cyc(q) ⊆ N_S(q) ∩ P`).** Forced incidences are incidence edges,
so `s_i, s_{i+1}` are `S`-neighbours of `q_i` and lie in `P`; they are
distinct (`m ≥ 2`, F's vertices distinct). *(Deps: setup.)*

## 4. Derivation of NC

Fix `q ∈ Q` with `deg_U(q) ≤ 1`, where `deg_U(q) = |N_S(q) ∩ U|`.

**(i) `N_S(q) ∩ P = cyc(q)`.**
`⊇` is P3. For `⊆`, suppose `s_k ∈ P`, `s_k ∼ q`, `s_k ∉ cyc(q)`.
By P2, `q` is an `H`-neighbour of `s_k` that is NOT one of `s_k`'s two
forced ends. By [PT] applied at `s_k` (carrier `A_{s_k}`, which exists
by [CC]):
`deg_{A_{s_k}}(q) ≥ c(q) + 1 = 3`, using P1 for `c(q) = 2`.
Since `s_k ∈ A_{s_k}` and `s_k ∼ q`, deleting the single vertex `s_k`
lowers the degree at `q` by exactly one:
`deg_{B_{s_k}}(q) = deg_{A_{s_k}}(q) − 1 ≥ 2`.
`s_k ∈ P` gives `B_{s_k} ⊆ U`, so `deg_U(q) ≥ deg_{B_{s_k}}(q) ≥ 2` —
contradicting `deg_U(q) ≤ 1`. ∎ *(Deps: P1, P2, [PT], [CC].)*

**(ii) `N_S(q) ∩ (U \ P) = ∅`.**
Suppose `w ∈ U \ P` with `w ∼ q`. Then `w ∈ N_S(q) ∩ U`, so
`deg_U(q) ≥ 1`; with the hypothesis, `deg_U(q) = 1` and
`N_S(q) ∩ U = {w}`. The two vertices of `cyc(q)` are `S`-neighbours of
`q` (P3); if either lay in `U` it would be in `N_S(q) ∩ U = {w}`,
impossible since `w ∉ P` while `cyc(q) ⊆ P`. So both vertices of
`cyc(q)` lie in `P \ U`. They are consecutive on `F` with shared end
`q`, so [CS(b)] gives `deg_U(q) = 0` — contradicting `deg_U(q) = 1`. ∎
*(Deps: P3, [CS(b)]. Note the m = 2 case: both pairs
`(s_1,s_2)` and `(s_2,s_1)` are consecutive, covering `q_1` and `q_2`;
[CS(b)]'s proof in LEMMA-A-CARRIER.md handles this explicitly.)*

**Consequences.** `N_S(q) ∩ U = (N_S(q) ∩ U ∩ P) ∪ (N_S(q) ∩ (U\P))
= (cyc(q) ∩ U) ∪ ∅` by (i),(ii); hence `deg_U(q) = |cyc(q) ∩ U|`.
On a `T_F`-normalized instance `S = P ∪ U` (T_F normalization lemma,
paper lem:TF), `N_S(q) = (N_S(q) ∩ P) ∪ (N_S(q) ∩ (U\P)) = cyc(q)`,
so `deg_S(q) = |cyc(q)| = 2`. ∎

## 5. Derivation of NCM

`P \ U ≠ ∅` is [CP]. For `s ∈ P \ U`, [CS(a)] gives `deg_U(q) ≤ 1` at
both forced ends `q` of `s`; NC then applies at each such `q`, so
`N_S(q) ∩ (P ∪ U) = (N_S(q) ∩ P) ∪ (N_S(q) ∩ (U \ P)) = cyc(q)`,
of size 2. ∎ *(Deps: [CP], [CS(a)], NC.)*

## 6. Adversarial notes (gaps hunted, none found)

1. *Exact-drop-by-one in (i):* needs `s_k ∈ A_{s_k}` (definitional) and
   `s_k ∼ q` (hypothesis); degrees count set membership, no
   multiplicity issue.
2. *`c(q)=2` (P1):* requires feasibility; without a feasible `J`,
   "forced" is vacuous (every incidence forced) and the claim collapses
   — feasibility must be, and is, a standing hypothesis of the whole
   carrier framework.
3. *Third forced edge at `s_k` (P0):* excluded by demand 2 +
   feasibility; without P0, [PT]'s "two forced ends" could mismatch the
   F-ends.
4. *`m = 2`:* `cyc(q)` still has two distinct elements; [CS(b)]
   applies; no degenerate identification of `q^−, q^+`.
5. *NC does not need hereditary FVS tightness* — pure Hall layer;
   consistent with its preregistered scope ("not graded as progress on
   Lemma A beyond what §4 claims"). NC cannot close Lemma A by itself
   (GAUNTLET §(ii) boundary, respected).

## 7. Verdict of the sealed phase

**Derivation SUCCEEDS.** NC(i), NC(ii), the consequences, and NCM all
follow from the certified stack: [PT] + [CS(a)] + [CS(b)] + [CP] +
[CC] + feasibility, with the elementary bridges P0–P3 supplied above.
Independence caveat: see §0 — the proof route was contaminated; the
step-checking, gap-hunt, and all machine work are mine.

Machine-confirmation plan (next phase, fresh code only):
enumerate abstract systems, find forced cores by feasibility
enumeration, compute carriers by direct tight-set minimization, test
NC/NCM raw (predicate on every clean q), on: the certified anchor
universe `(|S|≤3, |H|≤5)` expecting 115,774 systems / 798 cyclic / 18
`P∩U≠∅`; an n≤10 forced-structure universe; the ADJ boundary witness;
O-56 / O-63 / O-64. Negative controls that must fire: NC-ALL ("every
q ∈ Q is clean" — false on ADJ-1), CHORD-ALL ("N_S(q) ∩ P = cyc(q) for
every q ∈ Q" — false on ADJ-1), PDIS ("P ∩ U = ∅" — false on 18
anchor systems). Positive control: the three witnesses must pass NC.
