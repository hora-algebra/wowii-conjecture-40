# ATTEMPT REPORT

**Branch** `attempt/2026-08-05-claude-opus-5-0520`
**Model / harness** Claude Opus 5 (1M context), Claude Code CLI, macOS arm64
(Darwin 24.6.0), Python 3.9.6.
**Date** 2026-08-05.
**Protocol followed** ATTACK.md **v4**, read from `public/main`.
**Base** `public/main` = `64eb3da` ("Merge pull request #5 from
cozuya/lessons/tooling-post-push-proof").
**Soft time budget declared at start** 4 hours wall-clock (unanchored estimate —
no measured rate for this harness on this project). Actual: ≈2h15m to report.
**Publication status** LOCAL ONLY. Per the operator's binding instruction nothing
was pushed, no PR or lessons branch was opened, no public action attempted. As a
mechanical safeguard the push URLs of both `origin` and `public` were set to
`DISABLED-NO-PUSH-PER-OPERATOR` in this clone.

**Outcome in one line** — **MATHEMATICALLY PROVED** a new Hall-layer lemma **NC**
(clean-end chordlessness) that turns b17e's "two residual capacity holes at an
inclusion-maximal carrier" into a *neighbourhood* statement, **PROVED** a
consequent extension **A-I⁺** of Lemma A-I, verified both prospectively on
14,699 cyclic-forced-core systems with zero failures and all negative controls
firing, and found a **TOOLING** discrepancy: two published census rows on `main`
do not reproduce from the frozen checker at its own recorded hash. **Lemma A and
Conjecture 40 remain OPEN.**

---

## Provenance incident, and the stance I withdrew

This run began from a working checkout whose `ATTACK.md` was **v1.1**, with every
local branch and the local mirror `/Users/christineozols/conj40-mirror.git` at
**v3** or older. I could not locate the v4 protocol the operator had named, and
reported that. The operator then supplied the resolution: v4 exists on
`public/main`, landed after a reconciliation audit. I added the `public` remote,
fetched, and confirmed it directly:

```
public/main = 64eb3da   ATTACK.md line 1 = "... WOWII Conjecture 40 (v4)"
origin/main is a strict ancestor, 3 commits behind (77661ae, 446badb, 9b01be1)
```

**I withdrew the v3-based stance in writing** (`work/0520/RUNLOG.md`) and
restarted Step 0 from v4. The corresponding upstream lesson —
"maintenance completion claims require post-push existence proofs" — is present
in the base of this branch at `attempts/LESSONS.md` line 81 and was read as
binding. Everything below is under v4.

## Step 0 — freshness check (live, 2026-08-05)

| source | method | finding |
|---|---|---|
| GitHub issues | `gh issue list --state all` | none |
| GitHub PRs | `gh pr list --state all` | 5, **all MERGED**, none open |
| MathOverflow 513887 | StackExchange API v2.3 | `answer_count=0`, `is_answered=false`, `last_activity_date = creation_date = 2026-08-03T19:18:25Z` — **no answer, comment or edit since posting** |
| WOWII open list | plain-HTTP fetch of `cms.dt.uh.edu/…/wowII/open.html` (the `cms.uhd.edu` host in ATTACK.md refuses HTTPS; `cms.dt.uh.edu` is live) | still listed as **`O 40.`**, statement unchanged, only the Mar 6 2004 annotation. **No status change.** |
| web / arXiv | 2 web searches; 3 arXiv API queries | nothing on Conjecture 40 or Lemmas A/B. Recent Graffiti.pc activity is on other conjectures (141/142/143, 387, 2) and on DeLaViña–Waller (2605.24855). |

**Nothing resolved by others; run objective unchanged.**

## Step 0.5 — binding prior evidence

Read in full: `attempts/LESSONS.md` on `public/main` (81 lines, all six entries
including the reconciliation entry), b17e's `ATTEMPT_REPORT.md` (247 lines) and
`LEMMA-A-CARRIER-POSET.md`, `LEMMA-A-CARRIER.md` (5047), `proofs/PROOFS.md`
§§A–D, and the b17e artefacts `PREREG-CARRIER-POSET.md`, `carrier_poset.py`,
`ADJ-WITNESS.json`. No `[FALSIFIED]` or `[DEAD END]` entry was re-walked: I did
not revive shortest-path-only Lemma B, `P`/`B_s`/`T_F` universal localization,
SV, LIFT-P, the L5/L6 universality claims, the class-size threshold family, the
Lemma-CS-to-`P`-local bridge, or ADJ.

**Oracle check before any new mathematics:** `shasum -a 256 -c SHA256SUMS.txt`
run from `tools/` — **17/17 OK**.

## Step 1 — comprehension gauntlet

**COMPLETED** (`GAUNTLET.md`, rewritten from scratch on this branch). All four
required parts derived in my own words: the Theorem 3.13 reduction chain with
Lemma A's role isolated (it exists *only* to supply Lemma B's avoidable-incidence
premise); the abstract even-cycle system; the three witnesses; and the `T_F`
normalization with its non-monotone re-forcing step done via F1.

Every computational assertion was recomputed by `work/0520/engine0520.py`, an
independent re-implementation (forcedness decided by **re-solving feasibility
with the incidence forbidden**; `A_s` computed as the **intersection of all tight
sets containing `s`**) sharing no predicate code with `carrier.py`,
`carrier_poset.py` or `wcheck.py`. Anchored before use:
`ANCHOR systems=115774 cyclic=798 pdis=18` — exact match.

One original contribution in the gauntlet: **the `ρ`-blindness sharpening.** The
C5b bound `τ(G[H ∪ X]) ≤ ⌊ρ_e(X)/2⌋` collapses to exactly `τ ≤ |X|` on Hall-tight
sets, so **no hereditary violation can ever be certified by `ρ`-counting alone**.
This explains structurally why the `P`-local bridge cannot be obtained by
counting (`δ(P) ≥ 0` forbids it) and why every surviving foothold is geometric.

**Two metadata scope defects found** (neither affects a verdict): O-63's
"first inclusion-minimal violation" is minimal only *within* `B_s` — my complete
subset scan finds six strictly smaller global violations `{a,s},{a,t},{b,s},
{b,t},{s,u},{t,u}`, independently confirming b17e's `[TOOLING]` lesson; and
O-56's `refutes` field names the single-external-blocker subcase, which O-56 in
fact *satisfies* (it is PROVED in PROOFS.md).

## Target attacked

**Exactly one: ATTACK.md v4 Step 3 target 1** — Lemma A via the carrier-poset
endgame, resumed at the precise shape b17e left open ("combine the two residual
capacity holes at one inclusion-maximal carrier with the augmented forest
quotient, allowing a single maximal carrier and nested nonmaximal carriers"). No
Lemma B / SAFE-EXISTS or LIFT work was mixed in.

## Claims

### NC (clean-end chordlessness) — MATHEMATICALLY PROVED, COMPUTATIONALLY VERIFIED

Full statement, proof and scope: `LEMMA-A-CLEAN-END.md`. Preregistered with the
proof written out *before* any scan, frozen at commit `2510e2b`
(`PREREG-NC.md`).

> Call `q ∈ Q` **clean** if `deg_U(q) ≤ 1`. If `q` is clean then
> `N_S(q) ∩ P = cyc(q)` and `N_S(q) ∩ (U \ P) = ∅`; hence
> `deg_U(q) = |cyc(q) ∩ U|`, and on a `T_F`-normalized instance `N_S(q) = cyc(q)`,
> i.e. `deg_S(q) = 2`.

Proof in two lines each: a chord from `s_k ∉ cyc(q)` makes `q` a non-forced-end
neighbour of `s_k`, so punctured tightness forces `deg_{A_{s_k}}(q) ≥ 3`, hence
`deg_{B_{s_k}}(q) ≥ 2` with `B_{s_k} ⊆ U` — contradicting cleanliness; and an
auxiliary `w ∈ U \ P` at `q` would make both cycle vertices of `q` lie in `P \ U`,
so CS(b) gives `deg_U(q) = 0`, contradiction.

**Why it is not already known.** CS(c) gave `N_S(q) ⊆ P` only under the
known-false `P ∩ U = ∅`. NC's hypothesis is *always available somewhere* (CP
gives `P \ U ≠ ∅`; CS(a) makes both ends of any maximal-carrier vertex clean),
and its conclusion is strictly stronger — it forbids **chords from other cycle
vertices**, a phenomenon `ledgers/RESULT_RECORD.md` entry O-60 explicitly records
as possible in general. NC localizes them: chords live only at dirty `q`.

**Corollary CE — MATHEMATICALLY PROVED.** Every forced-core cycle has a cycle
vertex (any inclusion-maximal carrier, by CP) both of whose forced ends see no
`T_F`-vertex other than their own two cycle vertices. This is the concrete
content of b17e's "two capacity holes".

**Verification.** Checkers frozen and hashed before the run:

```
ac1836d99ca5ad711feea9c717ab6b326cbfcc9f50be983bb069380b938a81a0  work/0520/engine0520.py
64ebfa3f789411bb1fdaf893e3eb54ad190409c9858a92467d1670e4d2fa4f93  work/0520/nc0520.py
b21f5b8d5b14c23f0853ad83535d601766b8a202996c620d2f64208f8d2e32de  work/0520/nccontrols0520.py
2a0d62e00e867306951730223c2063bc3950fa0f7d4da18169cfb14d536728f1  work/0520/ADJ-WITNESS-vendored.json
```

Gold test first: O-56, O-63, O-64, ADJ-1 all carry a cyclic forced core and all
**PASS** NC/NCM/CPR; ADJ-1 fires all three negative controls. ADJ-1 is the sharp
separator, exactly as preregistered — its `q = 0` is dirty (`deg_U = 2`) and
carries the chord `s2`, while the two ends of the unique maximal carrier `s2` are
clean with `N_S(q) = cyc(q)` exactly.

Target scans (`work/0520/nc-scan-0520.txt`):

| universe | systems | cyclic | NC/NCM/CPR failures | negative controls | runtime |
|---|---|---|---|---|---|
| `exhaustive 3 5` | 115,774 | 798 | **0** | 18 / 18 / 18 | 43.3 s |
| `random 20000 seed 1` | 20,000 | 656 | **0** | 332 / 332 / 332 | 10.4 s |
| `random 400000 seed 777` | 400,000 | 13,245 | **0** | 6,727 / 6,695 / 6,727 | 200.4 s |

**Total 14,699 systems with a cyclic forced core, 0 failures**, every negative
control firing in every population. Post-hoc descriptive: of 1,620 cycle
`H`-vertices in the exhaustive universe, 1,602 are clean and 18 dirty, and **all
18 chords in the universe sit at dirty `q`** — the exact complement NC predicts.

### A-I⁺ (extension of Lemma A-I) — MATHEMATICALLY PROVED

> If there is a **clean** `q_0 ∈ Q` with `Ext(s) = ∅` for both `s ∈ cyc(q_0)` and
> `|Ext(s)| ≤ 1` for every other `s ∈ P` (`Ext(s) = N_H(s) \ Q`), then
> `τ(G[H ∪ P]) ≤ m − 1`, contradicting hereditary FVS tightness.

`D = Q \ {q_0}` has size `m−1`; NC(i) at the clean `q_0` is what guarantees no
`s ∉ cyc(q_0)` is adjacent to `q_0`, so every `s ∈ P` has degree ≤ 1 in
`G[H ∪ P] − D` and the graph is a forest. Lemma A-I is the special case
`Ext ≡ ∅`; A-I⁺'s hypothesis is strictly weaker. Non-vacuous: 528 of the 798
exhaustive cyclic systems satisfy it, and the counting step verifies in all 528
(`work/0520/ncdesc0520.py`). ADJ-1 satisfies it with `q_0 = 1` and A-I⁺ correctly
certifies its hereditary-tightness failure.

### CAP2-BS — CONJECTURAL; scan graded ABORTED-NO-VERDICT

The parked capacity-2 inequality `τ(G[H ∪ B_s]) ≤ |B_s| − 1` when every non-end
`H`-neighbour of `s` has capacity 2. **I ran sizing runs before writing any
preregistration**, which breaks this project's discipline, so it is reported as
exploratory and is **not** graded as verified; the parked status in PROOFS.md §D
is unchanged. Witness gold test is clean and discriminating: O-56 (`1 = 1`,
tight), O-63 (`2 = 2`, tight) and ADJ-1 (`0 ≤ 1`) hold under the guard, while
O-64 is correctly excluded by the guard and **fails** the unguarded form. Scan
over `gen_exhaustive(3,5)` + 2 Steiner: 3,132 completions, 0 failures — but only
18 of 450 `(system, s)` pairs pass the guard and the `NOGUARD` control never
fires *inside* the universe (O-64 has `|H| = 6`, outside it). A scan whose
negative control is inert in its own universe is not evidence. The completion
enumerator was validated against `larealize.py`'s anchor (732 completions over
438 cyclic systems at 0 Steiner — reproduced exactly).

### TOOLING — a published census that does not reproduce

Both **random** rows of the table in `LEMMA-A-CARRIER.md` §1.3 (on `main`) fail
to reproduce from `work/carrier.py` at its own preregistered hash
`d11b0bca3a4ac437b4811ce588e660fe2e382ccd725e017fbadd2919e195696a`:

| run | published | frozen `carrier.py`, rerun | `engine0520` |
|---|---|---|---|
| `exhaustive 3 5` | 115,774 / 798 / PDIS 18 | **same** | **same** |
| `random 20000 1` | **547** cyclic / PDIS **251** / DEG2 **142** | **656** / **332** / **157** | **656** / **332** |
| `random 400000 777` | **11,097** / PDIS **4,931** / DEG2 **2,643** | **13,245** / **6,727** / **3,271** | **13,245** / **6,727** |

The two engines were compared **system by system** on the 20,000-system
population: identical set of 656, symmetric difference 0. So this is a **stale
documentation figure, not engine drift**. The exhaustive row — the only one b17e
and VERIFY-2 relied on — reproduces exactly, so CP's evidence and the
`115,774 / 798 / 18` anchors are untouched, as are the "0 failures" verdicts. The
"≈44%" figure quoted for `P ∩ U ≠ ∅` should read ≈50.6% (332/656) and ≈50.8%
(6,727/13,245) on rerun.

## Dead ends hit, and why

* **"The hereditary violation lives in a maximal carrier `A_s`" — FALSIFIED
  before use, not preregistered.** I checked it against the witnesses first:
  O-63's maximal `A_t = {t}` has `τ = 1 > 0`, and in **O-64 neither** maximal
  carrier works (`A_s = {s,u}` contains two vertex-disjoint cycles, `τ = 2 > 1`;
  `A_t = {t}`, `τ = 1 > 0`). So even the *existential* form is refuted. This is
  the third localization family to die the same way; there is still no universal
  localizer.
* **`NC-ALL` ("every `q` is clean") and `CHORD-ALL` ("no chords anywhere") are
  FALSE** — ADJ-1 refutes both at `q = 0`. They were carried as negative controls
  precisely so that "0 failures" could not be dead code.
* **NC does not repair the `P`-local bridge.** It constrains `N_S(q)` for `q ∈ Q`
  and says nothing about `Ext(s) = N_H(s) \ Q`, which is exactly the gap
  `LEMMA-A-CARRIER.md` §3 identifies. O-55/O-56 remain binding.
* **The ADJ boundary was honoured throughout**: no argument assumes adjacent
  maxima, a puncture-free endpoint `deg_U(q) = 0`, or `P ∩ U = ∅`.

## Recommended next angle

The surviving shape is sharp: at a guaranteed inclusion-maximal carrier the two
forced ends are now known to be *completely free of other `T_F` vertices*, so the
entire obstruction has moved into `Ext(P)` — how the cycle vertices' external
`H`-neighbours sit in the forest. Attack that geometry directly, with **CAP2-BS
as the concrete target**, but: (a) preregister before any sizing run; (b) use a
universe reaching `|H| ≥ 6` so that O-63- and O-64-shaped configurations lie
*inside* it and the `NOGUARD` control can fire natively — the `gen_exhaustive(3,5)`
abstract universe is demonstrably too small (only 18 of 450 pairs pass the
capacity-2 guard); (c) keep capacity-1 and capacity-2 external neighbours as
separate branches, since that distinction is exactly what separates O-64 from
O-56/O-63. The checker, its anchored completion enumerator and the witness
controls are checkpointed on this branch and resume as they stand.

## Jobs and local propagation

No jobs left running. Gauntlet, preregistration, frozen checkers, raw scan
outputs, proofs, controls and this report are committed **only** to the attempt
branch. Nothing was pushed; no lessons branch or PR was created. The operator
must relay or merge the lessons below.

## LESSONS FOR FUTURE ATTEMPTS
- [MATHEMATICALLY PROVED] Lemma NC (clean-end chordlessness): if a forced-core cycle H-vertex `q` is *clean* (`deg_U(q) <= 1`) then `N_S(q) & P = cyc(q)` and no auxiliary of `U` touches `q`; so `deg_U(q) = |cyc(q) & U|`, and on a `T_F`-normalized instance `deg_S(q) = 2`. Proof and evidence in `LEMMA-A-CLEAN-END.md` on `attempt/2026-08-05-claude-opus-5-0520`. It strictly strengthens the CS(c) consequence `N_S(q) ⊆ P` and, unlike CS(c), never needs the known-false `P ∩ U = ∅`.
- [MATHEMATICALLY PROVED] Corollary CE: by CP + CS(a), every forced-core cycle has a cycle vertex whose two forced ends see NO `T_F`-vertex besides their own two cycle vertices. This is what b17e's "two residual capacity holes" actually are — a neighbourhood statement, not just spare capacity.
- [MATHEMATICALLY PROVED] A-I⁺ extends Lemma A-I: a clean `q_0` whose two cycle vertices have no `H`-neighbour off `Q`, with every other cycle vertex having at most one, already forces `τ(G[H ∪ P]) ≤ |P|-1`. NC is what makes the deletion `D = Q\{q_0}` legal by excluding chords into `q_0`. Non-vacuous on 528 of 798 exhaustive cyclic systems.
- [COMPUTATIONALLY VERIFIED] NC/CE/A-I⁺ prospective scan, checkers frozen and hashed before the run (`nc0520.py` sha256 `64ebfa3f...`, `engine0520.py` sha256 `ac1836d9...`): 14,699 systems with a cyclic forced core across `exhaustive 3 5` (798), `random 20000 seed 1` (656) and `random 400000 seed 777` (13,245); **0 failures**, with negative controls NC-ALL / CHORD-ALL / PDIS firing in every population. All 18 chords in the exhaustive universe sit at the 18 dirty `q`.
- [FALSIFIED] "Some inclusion-maximal carrier `A_s` contains the hereditary violation" is FALSE even in existential form: in O-64 neither maximal carrier works (`A_s={s,u}` has two vertex-disjoint cycles, `τ=2=|A_s|`; `A_t={t}`, `τ=1=|A_t|`). Do not propose `A_s`-localization; test any localization against O-64 first.
- [FALSIFIED] `NC-ALL` ("every `q ∈ Q` is clean") and `CHORD-ALL` ("no cycle vertex has a chord to a non-adjacent `q`") are both FALSE; ADJ-1 refutes both at `q=0`, where `deg_U(0)=2` and `s2` is a chord. Chords exist only at dirty `q` — that is exactly NC.
- [DEAD END] NC does not repair the `P`-local bridge and must not be used for it: it constrains `N_S(q)` for `q ∈ Q` and says nothing about `Ext(s) = N_H(s)\Q`, which is the actual obstruction. O-55/O-56 remain binding.
- [CONJECTURAL LEAD] CAP2-BS — `τ(G[H ∪ B_s]) ≤ |B_s|-1` whenever every non-forced-end `H`-neighbour of `s` has capacity 2 — is the one carrier localization still genuinely open (`proofs/PROOFS.md` §D parks it). It holds tightly on O-56 (`1=1`), O-63 (`2=2`) and on ADJ-1, and O-64 is excluded by the capacity guard rather than refuting it. NOT graded here: sizing runs preceded preregistration.
- [TOOLING] A scan universe must be able to fire its own negative control. `gen_exhaustive(3,5)` cannot test CAP2-BS: only 18 of 450 `(system,s)` pairs pass the capacity-2 guard and the refuting shape O-64 has `|H|=6`, outside the universe. Any CAP2-BS run needs `|H| >= 6`.
- [TOOLING] Two published census rows do not reproduce from the frozen checker at its own recorded hash. `work/carrier.py` (sha256 `d11b0bca...`) rerun now gives `random 20000 1` → 656 cyclic / PDIS 332 / DEG2 157 and `random 400000 777` → 13,245 / 6,727 / 3,271, whereas `LEMMA-A-CARRIER.md` §1.3 publishes 547/251/142 and 11,097/4,931/2,643. An independent engine agrees with the frozen tool system-by-system (symmetric difference 0 over the 20,000-system population), so this is stale documentation, not engine drift. The `exhaustive 3 5` row (115,774/798/18) reproduces exactly, so CP's evidence is unaffected; the quoted "≈44%" for `P ∩ U ≠ ∅` should read ≈50.7%.
- [TOOLING] O-56's `refutes` field names the single-external-blocker subcase as something it refutes; O-56 in fact *satisfies* that PROVED subcase (`U_6={2,3}`, each with one non-`6` neighbour, acyclic quotient). Wording defect only, in the same file VERIFY-1 already corrected once.
- [TOOLING] Independently reconfirmed b17e's O-63 scope correction: `{u,a,b}` is inclusion-minimal only *within* `B_s`; a complete subset scan finds six strictly smaller global violations `{a,s},{a,t},{b,s},{b,t},{s,u},{t,u}`, each with `τ=1<2`.
- [TOOLING] Structural obstruction worth carrying: the C5b bound `τ(G[H ∪ X]) ≤ ⌊ρ_e(X)/2⌋` collapses to exactly `τ ≤ |X|` on Hall-tight `X`, so no hereditary violation can EVER be certified by `ρ`-counting alone. Any Lemma A proof must use `H`-forest geometry (`M̂_h`); this is why `δ(P) ≥ 0` forbids reaching the `P`-local bridge by counting.
