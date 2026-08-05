# VERIFY-2 — adversarial verification report

Branch `verify/2026-08-05-verify2`. Run date 2026-08-05. Everything local; no
network use, no push, no external disclosure. The prior VERIFY-1 report is
preserved unchanged as `VERIFY_REPORT-VERIFY1.md`.

**Targets.** The two newest attempt branches:

| run | branch | head | subject |
|---|---|---|---|
| carrier-poset | `attempt/2026-08-05-codex-gpt-5-b17e` | `6ca752b` | Lemma A carrier-containment poset (CP); ADJ falsification |
| scheduled-descent | `attempt/2026-08-05-claude-opus-5-4d7a` | `ff8eadd` | SD / SD-SHORT / SD-2STEP census to n = 12 |

Both branches exist **only** in their working folders
(`conj40-attack-codex-20260805-b17e`, `conj40-attack-opus5-20260805-4d7a`).
The local mirror `/Users/christineozols/conj40-mirror.git` does **not** carry
either — its newest attempt ref is dated 2026-08-04. They were fetched
directly from the two working repos into a fresh clone. Common merge-base:
`85d1483` ("Merge maint/2026-08-attackv3: ATTACK.md v3").

**Method.** Fresh checkers written from the *statements* before any of the
target run's code was read. Engine provenance and hashes in §6.

---

## 1. Priority 1 — BLIND re-derivation of CP

### 1.1 What was sealed, and when

My proof was written and committed as `e44c2c2`
(`verify_independent/verify2/CP1-BLIND-DERIVATION.md`) **before**
`LEMMA-A-CARRIER-POSET.md` was opened. The target file's SHA-256 at sealing
time is recorded inside the sealed document
(`978fbbf43bc0d98711e741541bc828eb0acf99ade76e7a389c029ee8e57338db`) and is
unchanged.

Read before deriving: `README.md`; `proofs/PROOFS.md` §A, §B, §C5, §C5b, §C6,
§C7, §D; `PREREG-CARRIER-POSET.md`.
Not read before deriving: `LEMMA-A-CARRIER-POSET.md`,
`work/b17e/carrier_poset.py`, and the b17e revisions of `ATTEMPT_REPORT.md`
and `GAUNTLET.md`.

**Disclosed partial leakage.** `PREREG-CARRIER-POSET.md` lines 27–29 already
contain a two-sentence sketch of the containment step ("`B_s` is tight by
punctured tightness and contains `t`; canonical minimality gives
`A_t ⊆ B_s`, and `B_s` is a proper subset of `A_s`"). I had read it. It
sketches only what I call Step 1; it asserts no case split and gives no
argument for distinctness, acyclicity, or the `P\U` characterisation. Those
four steps are unaided.

### 1.2 Result: derived in full, and there is no second case

I derived the whole lemma — containment, pairwise distinctness, acyclicity of
the containment digraph, `P\U = {inclusion-maximal carriers}` (both
inclusions), and nonemptiness — in five short steps, **with no case split
anywhere**. The diff against the published proof is essentially nil: it
follows the same five steps in the same order, and my Steps 1, 2, 4a, 4b, 5
correspond one-to-one to its five paragraphs.

The only structural difference: my Step 5 uses a cardinality argument (take
`s` maximising `|A_s|`) where the published proof says "a finite nonempty
family of sets has an inclusion-maximal member". Same fact; mine is more
explicit. I also flagged in the sealed document a tempting *wrong* route to
Step 5 — via "a finite acyclic digraph has a sink", which would conflate
out-degree 0 with `s ∉ U`. The published proof does not take that route
either.

The load-bearing step is the **universal** clause of Common Tight Carrier
("for any tight `Y` containing `s`, `A_s ⊆ Y`"). PROOFS.md §D states and
proves it outright — `A_s ∩ Y` is tight by the lattice (C6) and inherits
exposure from `A_s` by monotonicity of `deg` — so Step 1 is legitimate. Had
that clause been available only for `Y` that additionally expose a forced
`F`-edge, Step 1 would break and a second case would genuinely be needed.
It is not so restricted.

### 1.3 The mandate's premise does not hold

> *"The controller could not reconstruct the second case (insertion-chain
> double-count) on first pass; your independent derivation or your independent
> failure to derive it is the single most important output of this run."*

**There is no second case in CP, and no insertion-chain double-count in its
proof.** Evidence:

- The published CP proof (`LEMMA-A-CARRIER-POSET.md` lines 25–44) is 18 lines
  and contains no case analysis of any kind.
- The strings `CP-1`, `CP-2`, `CP1`, `CP2`, `double-count`, `double count`
  **do not occur anywhere in either attempt branch**. CP is a single undivided
  lemma; the b17e scan emits one counter, `CP_fail`.
- The string `insertion` occurs exactly twice across both branches. Once in
  b17e `GAUNTLET.md` line 208, in the unrelated sense of a paper-numbering
  change ("after the carrier–cycle separation insertion, the current v2 paper
  numbers it Lemma 4.8"). Once in **4d7a**, `work/sd/onecycle_scan.py` lines
  10–14, describing the *cycle-counting* argument:

  > "Suppressing every `s` (degree exactly 2) turns `J` into a multigraph `M`
  > on `H` with one edge `{h1,h2}` per `s`; incidence cycles of `J` correspond
  > exactly to cycles of `M` (a 4-cycle of `J` becomes a parallel pair in
  > `M`). So the number of selected cycles equals the number of edge
  > insertions of `M` that close a cycle, which union-find counts
  > incrementally during the enumeration."

So "insertion-chain double-count" names a real object — but it lives in the
**scheduled-descent** run's cycle counter, not in the carrier-poset run's CP
proof. The two appear to have been conflated.

Because a double-count there would corrupt every `ncyc` figure in the 4d7a
census, I verified that argument directly instead. It is sound and
machine-confirmed on millions of instances: §3.4.

### 1.4 Grading

**CP — CONFIRMED.** Independently re-derived; the published proof is correct
as written, and complete.

---

## 2. Priority 3 — independent poset builder

`verify_independent/verify2/posetverify2.py`, written from the universe
description in `PREREG-CARRIER-POSET.md` and the tightness/carrier definitions
in PROOFS.md §C5/§C5b/§C6/§D. `work/carrier.py` and
`work/b17e/carrier_poset.py` were not read before it was complete.

### 2.1 Controls first, as the preregistration requires

Published positive controls, loaded from `tools/witnesses/*.json`
(`o_controls.py`):

| control | published selections | mine | cyclic forced core | CP | `P ∩ U = ∅` |
|---|---|---|---|---|---|
| O-56 | 1 | **1** | yes | holds | reproduced |
| O-63 | 6 | **6** | yes | holds | reproduced |
| O-64 | 1 | **1** | yes | holds | reproduced |

These also reproduce the specific carrier values PROOFS.md §D records:
O-56 `A_0 = {0,2,3}`; O-64 `A_s = {s,u}`, `B_s = {u}`.

Further controls (`poset_controls.py`):

| control | expected | observed |
|---|---|---|
| ADJ-1 (published witness) | feasible, cyclic forced core, CP holds, ADJ fails | reproduced exactly |
| `ACYCLIC-CONTROL.json` | forced-core cycle rank **zero** | no cyclic forced core |
| even-cycle system m=3 (PROOFS.md §D) | forced core **is** a cycle | cycle found, CP holds |
| even-cycle system m=4 | forced core **is** a cycle | cycle found, CP holds |
| PDIS negative companion | must fire | fires |

The ADJ-1 reproduction is exact, field for field:

```
tight sets  = {}, {s0}, {s1}, {s0,s1}, {s0,s1,s2}
carriers    = A_s0 {s0} | A_s1 {s1} | A_s2 {s0,s1,s2}
forced core = 6-cycle s0-0-s1-2-s2-1-s0   (all 6 incidences forced)
U = {s0,s1}   P\U = {s2}   pdis = True   CP holds   ADJ fails
```

### 2.2 Target scan

```
mine       TARGET systems=115774 cyclic=798 pdis=18 CP_fail=0 ADJ_fail=18
published  TARGET systems=115774 cyclic=798 pdis=18 CP_fail=0 ADJ_fail=18
```

Every published anchor reproduced exactly from an independently written
generator and checker. The `FIRST_ADJ_FAIL` certificate is identical too —
same system `N(s0)={0,1}`, `N(s1)={0,2}`, `N(s2)={0,1,2}`, all capacities two,
same carriers, same `U`, same `P\U={s2}`, same arcs `[(s2,s0),(s2,s1)]`.
Runtime 3.6 s (published 4.21 s).

### 2.3 One flag raised and resolved

My builder initially reported `carrier_nonunique = 360`: 360 of the 798 cyclic
systems contain some `s ∈ S` with no well-defined minimum tight carrier. This
is **not** a discrepancy (`carrier_wellposed.py`):

```
cyclic systems                          798
  with some s in S lacking a tight set  360
    ... where such an s lies ON a cycle   0     <-- the number that matters
  with some s having >1 minimal tight     0
    ... where such an s lies ON a cycle   0
```

Two facts: (i) the failure is always *non-existence*, never *non-uniqueness* —
exactly as the tight-set lattice (C6) predicts, since if any tight set
contains `s` then the minimum one is unique; (ii) it never touches a cycle
vertex. Common Tight Carrier only claims `A_s` for `s ∈ P`, and there `A_s` is
well-posed in all 798 systems. CP is never evaluated on an undefined carrier.

### 2.4 The derived consequence for Lemma CS

b17e claims CP upgrades Lemma CS(a) to unconditional: some `s ∈ P\U` always
exists, and its two forced ends each retain capacity outside `U`. Checked over
the whole universe (`derived_claims.py`):

```
forced ends of P\U vertices checked : 3168
violations of deg_U(q) <= 1         : 0
violations of deg_U(q) <= c(q) - 1  : 0
```

**CONFIRMED** on this universe. This is a Hall-layer statement only; it does
not bear on Lemma A, and b17e says so.

### 2.5 Scope note on "n ≤ 10"

The mandate asks for CP machine checks "at n ≤ 10". CP's preregistered
universe is not indexed by graph order — it is 115,774 *abstract* incidence
systems with `2 ≤ |S| ≤ 3`, `3 ≤ |H| ≤ 5`. The reason is structural: at every
graph order verified so far the forced core is acyclic (Lemma A holds), so CP
is **vacuous** on graph-realised instances and can only be exercised
abstractly. My SD census independently re-confirms `lemmaA_violations = 0` for
all connected bipartite graphs `n ≤ 11` (§3.2) — that is the corresponding
"n ≤ 10" statement, and it is precisely why the abstract universe is the right
test bed.

---

## 3. Priority 2 — fresh SD engines

`verify_independent/verify2/sdverify2.py` + `sdscan2.py`, written from
PROOFS.md §A/§E, `PREREG-SD.md` §0/§2 and `PREREG-SD2.md` §2, before reading
`work/sd/*.py`.

### 3.1 Negative controls (PREREG-SD.md §3), at n = 9

| control | expected | observed |
|---|---|---|
| `--ces=always` | 0 failures everywhere | 0 everywhere |
| `--ces=never` | A1-ALL failures = 24,195 = every cycle component; SD-SHORT failures = 24,195 | **24,195 / 24,195** |

`--ces=never` leaves `SD-COUNT-SHORT failures = 0`. My engine reproduces this
**acknowledged control gap** exactly: SD-COUNT-SHORT is measured by direct
cycle counting, not through the CES predicate, so a CES override cannot
exercise it. PREREG-SD2.md §3 already records this limitation; it is real and
correctly disclosed.

### 3.2 Exhaustive census, n ≤ 11 — full, not a subset

All connected bipartite graphs (`geng -bc -q n`), every minimum FVS with
`|S| ≥ 2`, every `e ∈ E(H)`, every feasible selection.

| quantity | n=9 | n=10 | n=11 | published n=11 |
|---|---|---|---|---|
| connected bipartite graphs | 730 | 4,032 | 25,598 | 25,598 ✔ |
| cyclic feasible selections | 24,195 | 443,308 | 8,071,822 | 8,071,822 ✔ |
| cycle components | 24,195 | 448,577 | **8,202,633** | 8,202,633 ✔ |
| selections with 2 cycles | 0 | **5,269** | **130,811** | 5,269 / 130,811 ✔ |
| A1-ALL failures | 0 | 0 | **6** | 6 ✔ |
| SD-SHORT failures | 0 | 0 | 6 | 6 ✔ |
| SD-COUNT-SHORT failures | 0 | 0 | 6 | 6 ✔ |
| SD-PLUS-2 failures | 0 | 0 | 0 | 0 ✔ |
| **B-PLUS-2 universal failures** | **0** | **0** | **0** | *ungraded — see §3.5* |
| SD-2STEP probed / failures | 0/0 | 0/0 | **6 / 0** | 6 / 0 ✔ |
| SD-2STEP-DESCENT failures | 0 | 0 | **0** | 0 ✔ |
| Lemma-A violations | 0 | 0 | **0** | 0 ✔ |
| path-enumeration cap hits | 0 | 0 | 0 | 0 ✔ |

n = 11 ran **full** in 183 s wall over 8 shards. Every published anchor
reproduced. The three witness graphs are identical, with identical `S` and `e`:

```
J??FErWxDw?   S={0,2,3,4}    e=(5,10)
J?B@eQo]Fo?   S={6,7,8,10}   e=(0,5)
J?B@eOtq`i_   S={0,1,6,10}   e=(4,9)
```

**ONE-CYCLE — CONFIRMED FALSIFIED at minimal order 10** (0 two-cycle
selections at n = 9, 5,269 at n = 10). The supporting counting argument also
checks out: a selected cycle needs ≥ 2 `S`- and ≥ 2 `H`-vertices, and
feasibility gives `2|S| ≤ 2|H| − 2`, hence `|H| ≥ |S| + 1`. Two cycles need
`n ≥ 9` — so n = 9 *was* a genuine test and minimal order 10 is a real fact —
and three need `n ≥ 13`, so the observed cap of 2 through n = 12 is indeed an
arithmetic artefact rather than evidence.

### 3.3 Full audit of the six witnesses

`witness_audit.py` re-derives every mechanism claim from scratch:

- 3 graphs × 2 selections = **6** A1-failing cycles ✔
- **20** shortest bad paths in total ✔ (matches PROOFS.md §B3's 20)
- every failing cycle: 4-cycle, `|cyc(J)| = 1`, `d0 = 3`, **zero** CES
  minimisers — the profile `(1,0)` ✔
- `dCES = 5` in every case, so the gap is **exactly 2** ✔
- `G` bipartite and connected; `H = G−S` a forest; `tau(G) = |S| = 4`, so `S`
  **is** a minimum FVS; hereditary FVS tightness `tau(G[H ∪ X]) = |X|` for
  **every** `X ⊆ S` ✔
- **20/20** shortest bad paths satisfy the full B1 structure: exactly one old
  cycle destroyed (namely `C`), exactly one new cycle `Z`, final added edge
  `(u,t)` lies on `Z`, `d0(J0) = 1`, `|cyc(J0)| = |cyc(J)| = 1`, and a CES
  minimising second step exists ✔

This independently reproduces 4d7a claim 7, PROOFS.md §B3, and the "20/20
followed by a minimising CES step" figure.

### 3.4 The insertion-counting argument (the "double-count" concern)

`sdscan2.py` computes `|cyc(J)|` structurally (components of the incidence
graph with `#edges == #vertices`) and **cross-checks every cyclic selection**
against an independent union-find count over the contracted multigraph `M` —
the very argument quoted in §1.3. The assertion ran on 8,071,822 cyclic
selections at n = 11, 443,308 at n = 10, and every cyclic selection below,
with **zero mismatches**.

The argument is sound, and the reason is worth recording: in this model every
`s ∈ S` has selected degree exactly 2 and every `h ∈ H` has selected degree
`≤ c(h) ≤ 2`, so `J` and `M` both have maximum degree ≤ 2. A max-degree-2
graph is a disjoint union of paths and cycles, so each component holds at most
one cycle and each cycle-closing insertion creates exactly one. Self-loops
cannot arise because an `s` selects two *distinct* `H`-neighbours; the 4-cycle
case appears as a parallel pair and is counted once. **No double-count.**
(Acyclic selections short-circuit before the assertion, but there the count is
0 on both sides trivially.)

### 3.5 A gap in 4d7a's grading, closed at n ≤ 11

4d7a grades `SD-PLUS-2`, the **∃-cycle** form, and explicitly records that the
universal **∀-cycle** `B-PLUS-2` was left ungraded at n = 12, because their
checker stops probing a selection once one of its cycles is covered. They call
re-running it "the cheapest high-value job for the next attempt".

I graded the universal form directly at n ≤ 11 by probing **every** A1-failing
cycle out to `d0 + 2` — which is exactly what the universal form reduces to,
since A1-good cycles have `dCES = d0`:

```
bplus2_all_failures    n<=9: 0     n=10: 0     n=11: 0
```

**B-PLUS-2 in its universal form — CONFIRMED, 0 failures, n ≤ 11**, from an
independent engine. This corroborates PROOFS.md §E's "verified exhaustively
n ≤ 11". The n = 12 universal grading remains open (§4).

---

## 4. What is NOT checked

| item | status | why |
|---|---|---|
| 4d7a claim 8 — the n = 12 holdout (228,810,295 cycle components; 1,380 A1 failures; 1,184 SD-SHORT; 0 SD-2STEP-DESCENT) | **NOT CHECKED** | Outside the mandate, which asked for n ≤ 10 full and n = 11. Cost measured, not guessed: a 1/1024 shard of n = 12 does not finish in 120 s, so the full run with my engine exceeds **34 core-hours ≈ 4.3 h on 8 cores** — past the mandate's ~4 h guard. Four background launches were additionally reaped by the sandbox. **ABORTED-NO-VERDICT**; no partial output is reported. |
| B-PLUS-2 universal form at n = 12 | **NOT CHECKED** | Same cost; graded at n ≤ 11 instead (§3.5). |
| 4d7a `sd_reverify.py` 8-sample n = 12 re-verification | **NOT CHECKED** | Depends on the n = 12 records above. |
| b17e Step 0 freshness check (GitHub / MathOverflow / arXiv state) | **NOT CHECKED** | Live external state on a different date; this run made no network access. |
| b17e `GAUNTLET.md` 268-line derivation | **NOT CHECKED** in full | Only §4 (T_F normalization) was read, in support of Priority 1. |
| maintenance censuses (order-10 11,716,571 connected graphs; LIFT-A; L5/L6; excess population) | **NOT CHECKED** | On `maint/2026-08-census`, not on either target branch. |
| Lean formalisation | **NOT CHECKED** | None claimed; both runs label their proofs "not Lean-formalized". |

n = 12 is the single material gap. It is the only place where either run's
headline prospective claim rests on numbers I did not reproduce.

---

## 5. Claim-by-claim grading

### 5.1 b17e — carrier-poset run

| # | claim | grade | evidence |
|---|---|---|---|
| 1 | CP is mathematically proved | **CONFIRMED** | blind re-derivation, §1; sealed at `e44c2c2` |
| 2 | CP computationally verified: 115,774 systems, 798 cyclic, 18 PDIS, `CP_fail=0` | **CONFIRMED** | independent generator + checker, exact match, §2.2 |
| 3 | ADJ is FALSIFIED, 18 failures | **CONFIRMED** | `ADJ_fail=18`, identical first certificate, §2.2 |
| 4 | the ADJ witness is not a Lemma-A counterexample (`tau(G[H∪S]) = 1 < 3`) | **CONFIRMED** | `tau = 1`, hereditary tightness fails, §2.4 |
| 5 | CS(a) consequence: some `s ∈ P\U` always exists, with two capacity holes | **CONFIRMED** on the universe | 3,168 forced ends, 0 violations, §2.4 |
| 6 | positive controls O-56 / O-63 / O-64; negative PDIS control | **CONFIRMED** | selection counts 1 / 6 / 1, cyclic core on all three, CP holds, `P ∩ U = ∅` reproduced; PDIS fires. §2.1 |
| 7 | CP does not close Lemma A | **CONFIRMED** (agreement) | Lemma A remains open; CP is a Hall-layer result, and the ADJ witness violates hereditary tightness |

### 5.2 4d7a — scheduled-descent run

| # | claim | grade | evidence |
|---|---|---|---|
| 1 | SD-REDUCTION: SD ⟹ F2 ⟹ bipartite case, using neither Lemma A nor B | **CONFIRMED** (by reading) | a correct unpackaging of C5b + C8 + Lemma 0 + B3. The caveat that SD tacitly forbids a selection all of whose cycles are all-forced is stated by the run itself (PREREG-SD2 §2) and guarded by `lemmaA_violations = 0`, which I independently reproduce |
| 2 | SD-SHORT FALSIFIED, minimal order 11, 6 failures | **CONFIRMED** | §3.2–3.3; same 3 graphs, same `S`, same `e` |
| 3 | SD-COUNT-SHORT FALSIFIED, 6 failures | **CONFIRMED** | §3.2 |
| 4 | ONE-CYCLE FALSIFIED at minimal order **10**; 5,269 / 130,811; max ever 2 | **CONFIRMED** | §3.2 |
| 5 | the cap of 2 is a counting artefact below n = 13 | **CONFIRMED** | §3.2 |
| 6 | SD-PLUS-2: 0 failures, n ≤ 11 | **CONFIRMED** | §3.2 |
| 7 | anchors: 730 / 4,032 / 25,598 graphs; 24,195 / 448,577 / 8,202,633 cycle components; A1 failures 6; cap hits 0; Lemma-A violations 0 | **CONFIRMED**, every figure | §3.2 |
| 8 | SD-2STEP / SD-2STEP-DESCENT hold at n ≤ 11 (6/6, 20/20), in sample | **CONFIRMED**, and the in-sample caveat is correctly stated | §3.2–3.3 |
| 9 | witness structure (4-cycles, `d0 = 3`, gap exactly 2, B1 (H1)–(H5)) | **CONFIRMED**, 20/20 | §3.3 |
| 10 | B-TERMINAL-SLIDE + (H1)–(H3) ⟹ SD-2STEP-DESCENT; `d0(J0) = 1` at all 20 | **CONFIRMED** | §3.3; the identity `toggle(J,a,Q+) = J0 − (t,u) + (u,t')` is one line, and "length 1 is minimal" is right |
| 11 | the n = 12 holdout figures | **NOT CHECKED** | §4 |
| 12 | scope caveat: universal B-PLUS-2 ungraded at n = 12 | **CONFIRMED as a real gap**, and closed at n ≤ 11 | §3.5 |

### 5.3 Discrepancies

**None.** No published number, witness, certificate, or verdict on either
branch failed to reproduce. The two items that required investigation — the
360 ill-posed carriers (§2.3) and the "insertion-chain double-count" (§1.3,
§3.4) — both resolved in the runs' favour.

The only correction is to the **mandate's own premise**: CP has no second case
and no double-count. The insertion-counting argument that the phrase points at
belongs to the other branch, and it is sound.

Both runs' honesty labelling held up under checking. In particular 4d7a's
in-sample/prospective distinction, its `--ces=never` control-gap disclosure,
and its scope caveat on universal B-PLUS-2 are all accurate — the last one
being a real gap that its author flagged rather than hid.

---

## 6. Engines, with hashes

All under `verify_independent/verify2/`. Each was written from the statements
before the corresponding target code was read.

```
ac11fc10b95e14fb8d6f6d06d2210b6809e0dea1e0b7a28d60081d21b96248a6  sdverify2.py
46f2586d4f27dbf9f88de43c6f0870b73cbe6e4159bb9823d9ecc0fd18c921fd  sdscan2.py
24b87201de4fb96c31ddae1252b1bca091f64934e28a2cb049536e46172428a8  posetverify2.py
e536f92312cca7fe200faa8f2521c52d6c4603a601e9850a9d3d742cedd6fa8f  poset_controls.py
4c770ec463887fd744e67a04ae1e58c1a2df85230eae0dd5bb26dee8f9007770  witness_audit.py
fa53af3420cc6b24e3e4d9ffa7d8e50300c87dd794a2a7b42fa17fcc35a33528  carrier_wellposed.py
98fafb19fdbfdf7157aa641d8ee8cce6de831918477f79e19e2ba6506d2dc536  derived_claims.py
```

(`o_controls.py` and `summarize.py` are loaders/formatters, not deciders.)

Enumeration uses `geng` from nauty (`/opt/homebrew/bin/geng`), the generator
the project itself uses. Python 3.9.6, 8 cores. Raw outputs in
`verify_independent/verify2/out/`.

## 7. Reproducing

```
cd verify_independent/verify2
python3 o_controls.py ../../tools/witnesses   # published positive controls
python3 poset_controls.py                     # ADJ-1, acyclic, even-cycle, PDIS
python3 posetverify2.py scan                  # 115774 / 798 / 18 / 0 / 18
python3 carrier_wellposed.py                  # 0 ill-posed carriers on P
python3 derived_claims.py                     # CS(a) + counting arguments
python3 sdscan2.py 9  --ces=always            # negative control
python3 sdscan2.py 9  --ces=never             # negative control
python3 sdscan2.py 10 --bplus2-all            # full n=10
seq 0 7 | xargs -P 8 -I{} sh -c \
  'python3 sdscan2.py 11 {} 8 --bplus2-all > out/n11-{}of8.json'
python3 summarize.py out/n11-*of8.json        # full n=11
python3 witness_audit.py                      # the six witnesses, 20/20
```
