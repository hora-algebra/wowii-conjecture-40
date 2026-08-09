# Lemma A: clean-end chordlessness (NC) and an extension of Lemma A-I

Branch `attempt/2026-08-05-claude-opus-5-0520`, 2026-08-05.
ATTACK.md **v4** Step 3 target 1 — the carrier-poset endgame, continued from
`LEMMA-A-CARRIER-POSET.md` (b17e) exactly at the shape it left open.
Preregistration: `PREREG-NC.md` (frozen at commit `2510e2b`, before any scan).

Inherited as a certified stack and used without re-derivation: the carrier
lattice (C6), the canonical carrier `A_s` (Common Tight Carrier), punctured
tightness (Lemma 4.5), the `T_F` normalization (Lemma 4.7), Lemma CS (5047) and
the carrier-poset lemma CP (b17e). **ADJ is FALSIFIED and is treated as a
binding boundary throughout**: nothing below assumes two adjacent
inclusion-maximal carriers, a puncture-free endpoint `deg_U(q) = 0`, or
`P ∩ U = ∅`.

## Notation

Forced-core cycle `F : s_1 − q_1 − s_2 − ⋯ − s_m − q_m − s_1` (`m ≥ 2`),
`P = {s_i}` its `S`-side, `Q = {q_i}` its `H`-side, `cyc(q_i) = {s_i, s_{i+1}}`.
Each `q ∈ Q` carries two forced incidences, so `c(q) = 2` and `q` is saturated
in every feasible selection. `A_s` is the canonical carrier, `B_s = A_s \ {s}`,
`U = ⋃_{s∈P} B_s`, `T_F = P ∪ U`. Write `Ext(s) = N_H(s) \ Q`.
Call `q ∈ Q` **clean** if `deg_U(q) ≤ 1` and **dirty** otherwise.

---

## 1. The lemma

> **NC (clean-end chordlessness) — MATHEMATICALLY PROVED.** Let `q ∈ Q` be
> clean. Then
>
>   (i)  `N_S(q) ∩ P = cyc(q)`, and
>   (ii) `N_S(q) ∩ (U \ P) = ∅`.
>
> Hence `deg_U(q) = |cyc(q) ∩ U|`, and on a `T_F`-normalized instance
> (`S = T_F = P ∪ U`, Lemma 4.7) simply `N_S(q) = cyc(q)`, i.e. `deg_S(q) = 2`.

### Proof

**(i).** Suppose `s_k ∈ P`, `s_k ∼ q = q_i`, and `s_k ∉ cyc(q)`. The two forced
ends of `s_k` are `q_{k−1}` and `q_k`; `q_i` is one of them only when
`k ∈ {i, i+1}`, i.e. only when `s_k ∈ cyc(q)`. So `q` is an `H`-neighbour of
`s_k` which is **not** a forced end of `s_k`. Punctured tightness therefore
applies in its "other neighbour" clause and gives

    deg_{A_{s_k}}(q) ≥ c(q) + 1 = 3 .

Since `s_k ∈ A_{s_k}` and `s_k ∼ q`, deleting the single vertex `s_k` lowers the
degree at `q` by exactly one, so `deg_{B_{s_k}}(q) ≥ 2`. But `s_k ∈ P`, so
`B_{s_k} ⊆ U` by the definition of `U`. Hence `deg_U(q) ≥ 2`, contradicting
cleanliness. ∎

**(ii).** Suppose `w ∈ U \ P` with `w ∼ q`. Then `w ∈ N_S(q) ∩ U`, so
`deg_U(q) ≥ 1`; cleanliness forces `N_S(q) ∩ U = {w}` exactly. As `w ∉ P`,
neither vertex of `cyc(q)` lies in `U`, i.e. both lie in `P \ U`. They are
consecutive on `F` with shared end `q`, so **Lemma CS(b)** gives
`deg_U(q) = 0` — contradicting `deg_U(q) ≥ 1`. ∎

Only the Hall layer is used: punctured tightness, the definition of `U`, and
CS(b). Hereditary FVS tightness is **not** needed, which is why NC also holds on
the three frozen witnesses and on ADJ-1 (all four verified below).

### Why this is new, and why it needed CP

Lemma CS(c) already gave `N_S(q) ⊆ P` for every `q ∈ Q` — but **only** under the
hypothesis `P ∩ U = ∅`, which 5047 measured failing in ≈44% of random cyclic
systems and which ATTACK.md records as not to be assumed. NC improves this on
both sides:

* **Hypothesis.** `deg_U(q) ≤ 1` is *always available somewhere*: CP guarantees
  `P \ U ≠ ∅`, and CS(a) makes both forced ends of any `s ∈ P \ U` clean. So NC
  never needs the known-false global condition.
* **Conclusion.** It is strictly stronger than `N_S(q) ⊆ P`: it additionally
  forbids **chords from other cycle vertices**. The project ledger records that
  phenomenon as genuinely possible in general —
  `ledgers/RESULT_RECORD.md`, entry O-60: "Lemma A-I uses `N_G(P) ⊆ Q` (NOT the
  false equivalence 'each `s` has only its 2 `F`-neighbours' — `s` may have
  unselected chords to other `Q`-vertices)". NC says exactly where such chords
  can and cannot live: **only at dirty `q`**.

> **Corollary CE (clean ends of a maximal carrier) — MATHEMATICALLY PROVED.**
> Every forced-core cycle has a cycle vertex `s` — any one whose carrier is
> inclusion-maximal, which exists by CP — such that **both** forced ends `q` of
> `s` satisfy `N_S(q) ∩ (P ∪ U) = cyc(q)`. On a `T_F`-normalized instance both
> ends have `deg_S(q) = 2` exactly.

This is the concrete content of b17e's "two residual capacity holes at one
inclusion-maximal carrier": the holes are not merely spare capacity, they are
**total absence of any other `T_F`-vertex** at those two `H`-vertices.

---

## 2. Consequence: an extension of Lemma A-I

Lemma A-I (PROVED, paper §4.1) kills the case `N_H(P) ⊆ Q`, i.e. `Ext(s) = ∅`
for *every* `s ∈ P`. NC weakens that hypothesis.

> **A-I⁺ — MATHEMATICALLY PROVED.** Suppose there is a **clean** `q_0 ∈ Q` with
>
>   (1) `Ext(s) = ∅` for both `s ∈ cyc(q_0)`, and
>   (2) `|Ext(s)| ≤ 1` for every other `s ∈ P`.
>
> Then `τ(G[H ∪ P]) ≤ m − 1 < m = |P|`, contradicting hereditary FVS tightness.
> Hence no forced-core cycle of a Lemma-A° instance has this shape.

**Proof.** Put `D = Q \ {q_0}`, so `|D| = m − 1`. `H − D` is a forest (induced
subgraph of the forest `H`). `P` lies in a single bipartition class — `F`
alternates between `P` and `Q ⊆ H` — so `G[H ∪ P]` has no edge inside `P`, and
every edge at a vertex of `P` goes to `H`. For `s ∈ P` its surviving neighbours
in `G[H ∪ P] − D` are `(N_H(s) ∩ {q_0}) ∪ Ext(s)`:

* if `s ∈ cyc(q_0)`: `Ext(s) = ∅` by (1), so the degree is exactly 1;
* if `s ∉ cyc(q_0)`: **by NC(i) applied at the clean `q_0`**, `s` is not adjacent
  to `q_0`, so the degree is `|Ext(s)| ≤ 1` by (2).

Every `s ∈ P` therefore has degree ≤ 1 and lies on no cycle, while `H − D` is a
forest. So `G[H ∪ P] − D` is a forest and `D` is an FVS of `G[H ∪ P]` of size
`m − 1`. ∎

Step (2)'s use of NC is essential and is exactly what A-I could not do: without
NC, a vertex `s ∉ cyc(q_0)` could carry an unselected chord to `q_0`, reaching
degree `|Ext(s)| + 1 = 2` and permitting a cycle.

**Non-vacuity and a positive control.** Over the exhaustive universe, 528 of the
798 cyclic systems satisfy A-I⁺'s hypothesis (post-hoc count,
`work/0520/ncdesc0520.py`), and in all 528 the counting step is verified.
ADJ-1 itself satisfies the hypothesis with `q_0 = 1`: `D = {0,2}`, degrees
`s0 ↦ 1`, `s1 ↦ 0`, `s2 ↦ 1`, so `τ(G[H ∪ P]) ≤ 2 < 3` — and ADJ-1 indeed fails
hereditary tightness (`τ(G[H ∪ S]) = 1 < 3`), so A-I⁺ correctly certifies it.

**What A-I⁺ does not do.** It does not escape O-56. In O-56 both cycle vertices
have `Ext = {6} ≠ ∅`, so hypothesis (1) fails; likewise in O-63 (`Ext(s) = {h}`)
and O-64 (`Ext(s) = {h}`). A-I⁺ is a strictly weaker hypothesis than A-I, not a
route around the recorded `P`-local dead end.

---

## 3. Prospective verification

Checkers frozen and hashed **before** the target run (`PREREG-NC.md` §0,
committed at `2510e2b`):

```
ac1836d99ca5ad711feea9c717ab6b326cbfcc9f50be983bb069380b938a81a0  work/0520/engine0520.py
64ebfa3f789411bb1fdaf893e3eb54ad190409c9858a92467d1670e4d2fa4f93  work/0520/nc0520.py
b21f5b8d5b14c23f0853ad83535d601766b8a202996c620d2f64208f8d2e32de  work/0520/nccontrols0520.py
2a0d62e00e867306951730223c2063bc3950fa0f7d4da18169cfb14d536728f1  work/0520/ADJ-WITNESS-vendored.json
```

`engine0520.py` is an independent re-implementation (no predicate code shared
with `work/carrier.py`, b17e's `carrier_poset.py`, or `work/wcheck.py`): forced
incidences are decided by **re-solving feasibility with the incidence
forbidden**, and `A_s` is computed as the **intersection of all tight sets
containing `s`**. It was anchored before use at
`ANCHOR systems=115774 cyclic=798 pdis=18`.

### Gold test (positive and negative controls, run before the target)

| control | cyclic core | NC / NCM / CPR | negative controls fired |
|---|---|---|---|
| O-56 | yes | **PASS** | — |
| O-63 | yes | **PASS** | — |
| O-64 | yes | **PASS** | — |
| ADJ-1 | yes | **PASS** | `NC-ALL`, `CHORD-ALL`, `PDIS` all fire |

ADJ-1 is the sharp separator, exactly as preregistered: its `q = 0` has
`deg_U(0) = 2` and `N_S(0) = {s0,s1,s2} ⊋ cyc(0) = {s0,s1}` — so it is **dirty**
and carries a chord — while the two ends of the unique maximal carrier `s2`,
namely `q = 1` and `q = 2`, are clean with `N_S(q) = cyc(q)` exactly. The
witness that killed ADJ is therefore also the witness that shows NC's hypothesis
is exactly the right one.

### Target scans

```
[exhaustive k<=3 p<=5]  systems=115774 cyclic=798   claim_failures=0
                        controls {NC-ALL: 18, CHORD-ALL: 18, PDIS: 18}      43.3 s
[random 20000 seed 1]   systems=20000  cyclic=656   claim_failures=0
                        controls {NC-ALL: 332, CHORD-ALL: 332, PDIS: 332}   10.4 s
[random 400000 seed 777] systems=400000 cyclic=13245 claim_failures=0
                        controls {NC-ALL: 6727, CHORD-ALL: 6695, PDIS: 6727} 200.4 s
```

**Total: 14,699 systems with a cyclic forced core, 0 NC failures, 0 NCM
failures, 0 CP-regression failures**, with all three negative controls firing in
every population. Raw output: `work/0520/nc-scan-0520.txt`.

Descriptive (post-hoc, not preregistered, `work/0520/nc-desc-0520.txt`): over the
798 exhaustive cyclic systems there are 1,602 clean and 18 dirty `q`, and
**all 18 chords in the universe sit at dirty `q`** — the exact complement NC
predicts.

**Status: MATHEMATICALLY PROVED (not Lean-formalized) and COMPUTATIONALLY
VERIFIED** on the universe above.

---

## 4. TOOLING discrepancy found (does not affect any verdict)

The two **random** rows of the census table in `LEMMA-A-CARRIER.md` §1.3 (on
`main`) do not reproduce from the frozen checker at its own recorded hash.
Running `work/carrier.py`, `sha256 d11b0bca3a4ac437b4811ce588e660fe2e382ccd725e017fbadd2919e195696a`
(the hash preregistered by b17e in `PREREG-CARRIER-POSET.md`):

| run | published in `LEMMA-A-CARRIER.md` §1.3 | frozen `carrier.py`, rerun now | `engine0520` |
|---|---|---|---|
| `exhaustive 3 5` | 115,774 / 798 cyclic / PDIS 18 | **same** | **same** |
| `random 20000 1` | 20,000 / **547** cyclic / PDIS **251**, DEG2 **142** | 20,000 / **656** / PDIS **332**, DEG2 **157** | 20,000 / **656** / PDIS **332** |
| `random 400000 777` | 400,000 / **11,097** cyclic / PDIS **4,931**, DEG2 **2,643** | 400,000 / **13,245** / PDIS **6,727**, DEG2 **3,271** | 400,000 / **13,245** / PDIS **6,727** |

The two engines were compared **system by system** on the 20,000-system
population: both flag the identical set of 656 systems, symmetric difference 0.
So this is a **stale documentation figure, not engine drift**. The exhaustive
row — the only one b17e and VERIFY-2 relied on — reproduces exactly, so CP's
evidence and the `115,774 / 798 / 18` anchors are unaffected. The "0 failures"
verdicts in that table are also unaffected: both engines report 0 on the same
populations. What changes is only the recorded size of the random populations
(and hence the 44% figure quoted for `P ∩ U ≠ ∅`, which is 332/656 = 50.6% at
seed 1 and 6,727/13,245 = 50.8% at seed 777 on rerun).

---

## 5. Scope, and what remains open

**Lemma A and Conjecture 40 remain OPEN.** NC is a Hall-layer statement, and
`GAUNTLET.md` §(ii) records why no Hall-layer statement can suffice on its own:
the abstract even-cycle system satisfies every Hall-layer property while
carrying a cyclic forced core, and — sharper — the C5b bound
`τ(G[H ∪ X]) ≤ ⌊ρ_e(X)/2⌋` collapses to exactly `τ ≤ |X|` on tight sets, so a
hereditary violation can never be certified by `ρ`-counting alone.

What NC does deliver into the endgame: at a guaranteed-existing inclusion-
maximal carrier, the two forced ends are **completely free of other `T_F`
vertices**. That converts b17e's "two capacity holes" from a counting statement
into a neighbourhood statement, and it is what makes A-I⁺'s deletion argument
legal at `q_0`.

What it does **not** deliver, stated explicitly so the next attempt does not
re-walk it:

* It says nothing about `Ext(s) = N_H(s) \ Q` — how the cycle vertices' external
  neighbours sit in the `H`-forest. That is precisely the gap
  `LEMMA-A-CARRIER.md` §3 identifies for Lemma CS, and NC does not close it. The
  `P`-local bridge remains refuted as a route by O-55/O-56.
* Localizing the hereditary violation to `A_s` for a maximal `s` is **false**:
  in O-63 the maximal carrier `A_t = {t}` has `τ(G[H ∪ A_t]) = 1 > 0`, and in
  O-64 *neither* maximal carrier works (`A_s = {s,u}` has two vertex-disjoint
  cycles, `τ = 2 > 1`). So "the violation lives in some maximal carrier" is
  refuted; I checked this before proposing it and did not preregister it.
* The strengthenings `NC-ALL` ("every `q` is clean") and `CHORD-ALL` ("no chords
  anywhere") are **FALSE** — ADJ-1 refutes both at `q = 0`. Do not assume them.

**Recommended next step.** The surviving shape is: a clean `q_0` exists with
`N_S(q_0) = cyc(q_0)`; the obstruction is entirely in `Ext`. The next subclaim
should therefore be about the **`H`-forest geometry of `Ext(P)`** at a maximal
carrier — concretely, the parked capacity-2 inequality
`τ(G[H ∪ B_s]) ≤ |B_s| − 1` for external neighbours `h` with `c(h) = 2`, which
`proofs/PROOFS.md` §D records as *neither proved nor refuted* and which O-64
does **not** refute (its `h` is capacity-1). That is the one localization in the
area still genuinely open, and it should be attacked with a preregistered
realization scan (`larealize.py`-style forest completions), not with prose.
§6 records how far I got with it in this run, and why it is **not** graded.

---

## 6. CAP2-BS — exploratory only, NOT preregistered, NOT graded

I began the follow-on attack in the same run. State it exactly:

> **CAP2-BS (CONJECTURAL).** Let a forced-core cycle have `S`-side `P`, let
> `s ∈ P` have `B_s ≠ ∅`, and suppose **every** `H`-neighbour of `s` outside its
> two forced ends has capacity 2. Then `τ(G[H ∪ B_s]) ≤ |B_s| − 1`.

**Honest procedural status.** I ran sizing runs on the target universe **before**
writing any preregistration, in order to find out whether the universe was large
enough. That breaks this project's preregistration discipline, so CAP2-BS is
reported as **exploratory** and is **not** graded as COMPUTATIONALLY VERIFIED,
regardless of the outcome below. It does **not** upgrade the parked status
recorded in `proofs/PROOFS.md` §D.

**Gold test on the four witnesses** (`work/0520/cap2bs-controls-0520.txt`) — this
part is clean and does discriminate:

| witness | `s` | `B_s` | non-end nbrs / caps | guard | `τ` vs `|B_s|−1` | verdict |
|---|---|---|---|---|---|---|
| O-56 | 0, 1 | `{2,3}` | `{6}` / `[2]` | yes | `1 = 1` | holds, **tight** |
| O-63 | s | `{u,a,b}` | `{h}` / `[2]` | yes | `2 = 2` | holds, **tight** |
| ADJ-1 | s2 | `{s0,s1}` | `{0}` / `[2]` | yes | `0 ≤ 1` | holds |
| O-64 | s | `{u}` | `{h}` / `[1]` | **no** | `1 > 0` | guard correctly excludes it; the unguarded form **FAILS** |

So the capacity-2 guard is exactly what separates O-64 from the other three, and
the harness demonstrably detects a failure when one exists.

**Scan.** `work/0520/cap2bs0520.py` over `gen_exhaustive(3,5)` with 2 Steiner
vertices: 798 cyclic systems, 450 `(system, s)` pairs with `B_s ≠ ∅`, of which
only **18** pass the capacity-2 guard; 3,132 forest completions tested;
**0 CAP2-BS failures**. The completion enumerator was validated against
`larealize.py`'s published anchor (732 completions over the 438 cyclic systems of
`gen_exhaustive(3,4)` at 0 Steiner — reproduced exactly).

**Why this scan is weak, stated plainly.** The `NOGUARD` negative control never
fires anywhere *inside* the scanned universe — it fires only on the O-64 control,
which has `|H| = 6` and therefore lies **outside** `gen_exhaustive(3,5)`. A scan
whose negative control is inert within its own universe is not evidence. Combined
with only 18 guarded pairs, the correct grading is **ABORTED-NO-VERDICT** for the
scan and **CONJECTURAL** for CAP2-BS.

**For the next attempt.** CAP2-BS is worth a proper preregistered run, but it
needs a universe reaching `|H| ≥ 6` (so that O-64-shaped and O-63-shaped
configurations are *inside* it and the negative control can fire natively), and
it must be preregistered before any sizing. The checker, its completion
enumerator (anchored at 732) and the witness controls are checkpointed on this
branch and are resumable as they stand.
