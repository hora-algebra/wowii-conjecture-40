# ATTEMPT REPORT

**Branch** `attempt/2026-08-04-claude-fable-5-0eb8`
**Model / harness** Claude Fable 5, Claude Code CLI, macOS (8-core), Python
3.9.6, nauty `geng` (Homebrew).
**Date** 2026-08-04.
**Base** GitHub `main` = `b9eb809` ("Merge release/v2", tag v2.0 line) — note
this is the post-v2 main, which already contains the 5047 attempt's results
(SV falsified, Lemma A to n=14, LIFT census) and the v2 paper. This file
replaces, on this branch only, the 5047 report that v2 main carries at the
same path; that document is unchanged on `main`.

**Outcome in one line** — the codex-a7c3 advance (L3/L4/L5) is **independently
CONFIRMED** (proofs re-derived, every count reproduced by a fresh engine and
by re-running its frozen checkers); its open universality question is
**settled negatively**: the L5 condition — and this branch's strictly
stronger L6 condition — holds for every connected nonbipartite graph with
`n <= 9` (new, preregistered, prospective census) but is **FALSIFIED at
n = 11** by a certified witness `CX11 = J??FF?^FuE?` with a unique minimum
OCT, member of an infinite family; along the way the new component-excess
conjecture E1 is **FALSIFIED at n = 10** with a unique witness that is
exactly the building block of CX11. Exact LIFT-A survives everything here.

## Step 0 — freshness check (network partially available)

| source | method | finding |
|---|---|---|
| (a) issues / PRs | web fetch of the GitHub lists | 0 issues ever; exactly one open PR, #1 "Lessons: attempt/2026-08-03-claude-opus-5-5047" (the lessons PR; no mathematical content beyond the 5047 report). |
| (a') repository state | `git fetch` of GitHub main + all attempt branches | **main has advanced to v2** (`b9eb809`), merging the 5047 results and a v2 paper/PDF; `attempts/LESSONS.md` on main still has no entries (PR #1 unmerged). ATTACK.md §"What is open" and Step 3 are stale relative to v2 (SV listed OPEN there is FALSIFIED in v2); I follow the v2 state of knowledge. |
| (b) MathOverflow 513887 | direct fetch and API fetch both blocked by the harness | UNREACHABLE for me today. The codex-a7c3 report (2026-08-04, network available) records 0 answers / 0 comments. |
| (c) WOWII page | fetch declined/blocked (two adjusted routes attempted) | UNREACHABLE for me today. codex-a7c3 (same day) records status letter **O** (open), unchanged. |
| (d) web/arXiv | two web searches | Nothing new on Conjecture 40 or the lemmas; hits are other WOWII conjectures (103, 141–143, 284, 91) and unrelated. |

Nothing found that changes the run's job.

## Step 0.5 — prior attempts

Read in full: `attempts/LESSONS.md` (empty), the 5047 `ATTEMPT_REPORT.md`
(as amended on v2 main), `VERIFY_REPORT.md` (VERIFY-1), `SV-FALSIFIED.md`,
both lifting preregistrations, and the codex-a7c3 branch (audited at
`5c4a4ec`, since sanitized in place to `9349b7c` with no change to any
checker, hash record, count, or statement; based exactly on v1.1
`0617d7a`): its `ATTEMPT_REPORT.md`, `LIFT-A-RESIDUAL.md`,
checkers and hash records. Binding facts honored: SV and LIFT-P are
FALSIFIED (n=11) and were not touched; the frozen dead ends of ATTACK.md
Step 2 were not re-walked; LIFT-A / LIFT-A-ALL remain the surviving route.

## Step 1 — gauntlet

**COMPLETED** — `GAUNTLET.md` on this branch: (i) the Theorem 3.13 chain
with the exact role of every ingredient; (ii) the abstract even-cycle
computation `rho(X) = 2|X|`, its unique maximally-cyclic forced selection,
and the failure of hereditary tightness at `X = S`; (iii) all three warning
witnesses with mechanisms and the exact localization each kills; (iv) the
`T_F` normalization proof and its license/non-license. Everything
recomputed by fresh code (`work/fable-0eb8/gauntlet_check.py`, no code
shared with `tools/`): selection counts 1/6/1, the corrected 8-edge O-56
forced core, carriers, violating sets `{2,3}` / `{u,a,b}` / `{s,t}`,
`tau(G[HuS]) = 2/3/2`, even-cycle systems m=2..5. `tools/SHA256SUMS.txt`
17/17 OK before use.

## Independent audit of codex-a7c3 (AUDIT-CODEX-A7C3.md)

- Hashes of all three codex checkers match their recorded freezes.
- All five proofs (L3-Forest, L3, L4, L5-Forest, L5) re-derived from
  scratch; **no gaps**; verdict MATHEMATICALLY PROVED (not Lean-formalized).
- Every reported count reproduced twice: by my fresh engine
  (`work/fable-0eb8/audit_l3l5.py`, 14.9 s) and by re-executing the codex
  checkers at their frozen hashes — 451/0/182, 356 tight, 11,859 graphs,
  L2/L3/L5 coverage 11,170 / 11,852 / 11,859, increments 682 / 7, the exact
  seven residual graph6 strings, L4 4,606 with false control firing twice,
  descriptive universal-L3 count 11,783, `DC{` strictness control.
- Scope labeling (prospective L3 vs regression L4/L5) verified accurate.
- **CONFIRMED overall; the only open item was condition-(6) universality —
  attacked below.**

## New results

### R1. L6 / L7 — closing the sparse-pair bonus into its natural maximum

Frozen in `PREREG-L6-N9.md` before any new run. For an edge-containing
bipartite component `C` with classes `A_C, B_C`:
`FE(C) = max{|W| + |Y|}` over a full class `W` plus `Y` in the other class
with `C[W u Y]` acyclic; `g(C) = FE(C) - max(|A_C|, |B_C|) >= 1`. A set `Y`
qualifies iff the neighbourhood family `{N(y) ∩ W}` is Berge-acyclic, so
`g` is the maximum Berge-acyclic subfamily — the closure of the codex
sparse-pair idea (`g >= 1 + r`).

- **L6-Forest** (`tau(B) <= M(B) - g(B)`) and **L6** (some minimum OCT with
  `p <= Delta + 2g - 1` implies LIFT-A with that OCT):
  **MATHEMATICALLY PROVED** (short; PREREG-L6-N9.md).
- **L7** (reduction): for any minimum OCT, `[Delta + 2g - 1] - p(G) >=
  sum_C excess(C) - 1 - o`, where `excess(C) = |a-b| + 2g(C) - p(C)`;
  via `p(G) <= p(B) + o` and additivity. **MATHEMATICALLY PROVED.**
  Consequence: components of positive excess pay for the OCT; components
  with `excess = 0` are the only enablers of a condition failure
  (given enough of them relative to `o` and `c_e`).

### R2. Prospective n = 9 census of the open universality question

Frozen: `PREREG-L6-N9.md` + checker `l6scan.py` (SHA-256 `2e568740…`),
committed before the run; gold suite (DC{, K3, C5, C7, bowtie, the seven L3
residuals, the three SV witnesses) and the full n<=8 regression passed
pre-freeze; n=9 untouched at freeze time.

**Result: COMPUTATIONALLY VERIFIED (universe: all 261,080 connected graphs
on 9 vertices, 260,350 nonbipartite; eight `geng` shards; anchors exact).**

- S1 = 0: every connected nonbipartite graph with `n <= 9` has a minimum
  OCT satisfying the codex L5 condition. (New frontier; was n <= 8.)
- S2 = 0: same for the L6 condition; L6-beyond-L5 count 0 at n = 9.
- S3 = 0: exact LIFT-A clean (consistency); the 2,494 LIFT-A-tight graphs
  found are **set-identical to the published v2 list**
  (`lift-a-tight-n9.g6`, SHA-256 `60784809…`) — a strong external anchor.
- Bipartite layer: T1 (L6-Forest) 0 failures on all 1,119 bipartite graphs
  at n = 9 (tight on 1,114 — the bound is near-exact at small orders);
  negative controls fired throughout (450+1,114 minus-1 fires; exact+1
  fails on exactly the 217 known tight graphs at n <= 8).

### R3. E1 (component excess >= 1) — FALSIFIED at n = 10

Frozen: `PREREG-E1.md` + `e1scan.py` (SHA-256 `11dc5f28…`), gold
hand-derived values, committed before the census. Universe: all 5,015
connected bipartite graphs `2 <= n <= 10` (anchors exact).

**Result: E1 is FALSE, minimally at n = 10, by exactly one graph:**
`I??FF?^Fo` — two `K_{3,2}` blocks glued along a C4; balanced 5+5, dense on
both sides (all same-side codegrees >= 2, so `r = 0`, `g = 1`), `p = 2`
(not traceable), `excess = 0`. Excess histogram over the universe:
`{0:1, 1:60, 2:574, 3:912, 4:1545, 5:1208, 6:552, 7:146, 8:16, 9:1}`;
control fired on 61 graphs. This is the exact "dense complementary case"
of the codex dichotomy, realized: full-side forest bounds lose 2 here
(`tau = 2` vs `min - g = 4`), because the optimal forest cuts one hub in
EACH block instead of keeping a full side.

### R4. The L5 and L6 conditions are not universal — FALSIFIED at n = 11

`L5-CONDITION-FALSIFIED.md` carries the certificate. **CX11 =
`J??FF?^FuE?`**: the E1 witness plus an apex `t ~ {0,1,6,7}` (two
neighbours in each class, none in the right block).

- `{t}` is the **unique minimum OCT** (hand proof via 2-connectivity of the
  E1 witness; machine check: exactly one vertex whose removal is
  bipartite).
- `p = 2` (hand proof: slot counting at the right hubs; machine: DP and an
  independent brute-force second engine).
- The unique remainder has `c_e = 1, i = 0, Delta = 0, r = 0, g = 1`:
  thresholds L2 = L3 = L5 = L6 = 1 < 2 = p, and L4 is inapplicable
  (`tau(B) = 2`). **No proved sufficient condition covers CX11.**
- Exact LIFT-A holds (`ell = 9 >= 6`, slack 3); Conjecture 40 holds
  (slack 3).
- **Infinite family** CX(m) (`n = 2m + 5`): same proofs verbatim;
  machine-verified at m = 3, 4 (p = 2, 3 — the failure margin grows).
- Engines: `verify_cx.py` (exact + definition-level second pass), frozen
  `l6scan.py` profile, and the repository's own frozen
  `phase0_verify2.py` (`verification/SHA256SUMS.txt` 237/237 OK):
  `J??FF?^FuE? f=8 b=10 p=2`. All agree.
- Status: universality of L5/L6 conditions **FALSIFIED**; the CX
  construction itself **MATHEMATICALLY PROVED** for all m >= 3 and
  **COMPUTATIONALLY VERIFIED** at m = 3, 4. Provenance: the witness came
  from the frozen E1 census; the apex design is **IN-SAMPLE** (built
  after seeing the witness), then certified exactly — the certificate does
  not depend on how it was found.
- **Minimality: OPEN between 10 and 11.** `n <= 9` is excluded by R2's
  prospective census; n = 10 has never been censused for the condition.

## Dead ends and incidents

- **Parity blunder, caught by the oracle:** my first apex attachment
  (`t ~ {0,1,2}`, three same-class vertices) leaves the graph BIPARTITE —
  same-class attachments close only even cycles. `verify_cx.py`'s
  nonbipartiteness assertion caught it before anything was recorded as a
  result; the corrected attachment needs two neighbours in EACH class.
  Recorded in the verifier's docstring as a warning to future constructors.
- The conditional o=1 reduction sketch ("E1 + isolated vertex or c_e >= 2
  implies coverage") died with E1 itself; its unconditional core survives
  as L7 and as the design principle that found the witness. No other
  branch was abandoned.
- Background-process hygiene: detached shard jobs were terminated by
  session cleanup; rerun as supervised background jobs. No data loss (the
  frozen checker is restart-safe per shard).
- The MathOverflow and WOWII freshness checks were unreachable from this
  harness (recorded above): ABORTED-NO-VERDICT for those two sub-checks,
  mitigated by the codex same-day record.

## Jobs still running at report time

None. Both preregistered runs (n=9 scan, ~6 min wall on 8 shards; E1
census, ~7 min) completed and are committed.

## Propagation status (ATTACK.md Step 5) — NOT EXECUTED

Committed only to `attempt/2026-08-04-claude-fable-5-0eb8` in the local
clone. No push, no PR, no public post — per the operator's standing
instruction, publication waits for explicit authorization. The commands
that WOULD publish, reported and not executed:

    git push github attempt/2026-08-04-claude-fable-5-0eb8
    git checkout -b lessons/0eb8 b9eb809
    # append the LESSONS section below to attempts/LESSONS.md, commit
    git push github lessons/0eb8
    gh pr create --repo cozuya/wowii-conjecture-40 \
      --base main --head lessons/0eb8 \
      --title "Lessons: attempt/2026-08-04-claude-fable-5-0eb8"

## Recommended next angle

1. **Census the L5/L6 condition at n = 10** (the 11.7M-graph layer) to
   settle minimality of CX11. The Python checker needs a C port for this;
   validate it against `l6scan.py` on n <= 9 and the CX family first.
2. **Attack exact LIFT-A on unique-OCT graphs directly.** Both SV and the
   L5 condition died at singleton unique OCTs; CX11's exact slack is 3,
   and its tau comes from hub cuts in 2-connected dense blocks. A
   hub-deletion forest bound for 2-connected dense bipartite components
   (`tau(C) <= (number of blocks)`-type statements) would beat FE exactly
   where it loses. The E1 histogram says excess-0 components are rare
   (1 in 5,015 through n = 10) — enumerate excess-0 components at n = 11,
   12 (bipartite-only, cheap) BEFORE conjecturing any repaired threshold,
   then preregister against that population.
3. **Do not re-freeze any full-side (FE-style) bound as a universality
   candidate.** CX(m) kills the whole family of thresholds computable from
   `(c_e, i, class sizes, g)` alone: within the CX family those data are
   constant while `p` grows with m — so ANY function of them fails; a
   universal condition must read deeper structure than per-component class
   sizes and full-side forest extensions.
4. The 5047 recommendation of pushing LIFT-A-ALL to full n = 11 stands;
   CX11 satisfies it with room, and it remains the surviving route.

## LESSONS FOR FUTURE ATTEMPTS

- [FALSIFIED] The universality of the codex-a7c3 L5 lifting condition (`exists` minimum OCT with `p <= 2c_e + Delta + 2r - 1`) is FALSE: witness `CX11 = J??FF?^FuE?` (n=11), unique minimum OCT `{apex}`, remainder = two glued `K_{3,2}` blocks (dense both sides: `r=0, g=1, Delta=0, c_e=1`), `p=2` > all thresholds; certificate + infinite family CX(m) in `L5-CONDITION-FALSIFIED.md` on `attempt/2026-08-04-claude-fable-5-0eb8`. Exact LIFT-A holds there with slack 3; Conjecture 40 with slack 3.
- [FALSIFIED] Any sufficient LIFT-A threshold computed only from `(c_e, i, per-component class sizes, full-side forest extension g)` fails on the CX family: those invariants are constant in m while `p(CX(m))` grows. Full-side (FE/star-type) forest bounds lose exactly on glued dense blocks, where the optimal forest cuts one hub per block (`tau=2` vs `min-g=4` on the witness).
- [FALSIFIED] E1 (`|a-b| + 2g(C) - p(C) >= 1` for every connected bipartite component `C`) is FALSE, minimally at n=10, by the unique witness `I??FF?^Fo` (glued `K_{3,2}`s, balanced, all same-side codegrees >= 2, not traceable). Excess-0 components are the enablers of lifting-condition failures (reduction Lemma L7); they are rare (1 of 5,015 connected bipartite graphs n<=10).
- [COMPUTATIONALLY VERIFIED] The L5 and L6 conditions hold for EVERY connected nonbipartite graph with n <= 9 (preregistered prospective census, 260,350 graphs, checker sha256 `2e568740…`); so the minimal order of condition failure is 10 or 11 — n=10 is uncensused and is the next cheap decisive computation (needs a C port).
- [MATHEMATICALLY PROVED] L6-Forest/L6: with `g(C)` = max Berge-acyclic subfamily of one side's neighbourhood hypergraph (equivalently the largest forest extension of a full class), `tau(B) <= M - g(B)`, and `p <= Delta + 2g - 1` for some minimum OCT implies LIFT-A. L7: `[Delta + 2g - 1] - p(G) >= sum_C excess(C) - 1 - o`. Both on this branch; L6 subsumes L5 (`g >= 1 + r`).
- [COMPUTATIONALLY VERIFIED] codex-a7c3's L3/L4/L5 proofs and every reported n<=8 count were independently CONFIRMED (fresh engine + re-execution at frozen hashes; `AUDIT-CODEX-A7C3.md`); its in-sample/prospective labeling is accurate.
- [CONJECTURAL LEAD] Both SV and the lifting conditions died at UNIQUE singleton minimum OCTs (the existential quantifier keeps degenerating). Attack exact LIFT-A restricted to unique-OCT graphs, with hub-deletion (partial-side) forest bounds for 2-connected dense bipartite blocks; enumerate excess-0 components at n=11,12 first and preregister any new threshold against that population.
- [TOOLING] Frozen checkers on this branch: `l6scan.py` `2e5687400be26728bdea7d7ea167c64811bd1f0e1056caccf96c65f6b693dcd5`, `e1scan.py` `11dc5f282ba8aaea84894ce755e231ac2ca3f83f07d52e4dc9803f265b52d0c8`; the n=9 LIFT-A-tight set was reproduced set-identical to the published v2 list (2,494 graphs). Same-class apex attachments keep a bipartite graph bipartite — an odd cycle needs neighbours in BOTH classes; check nonbipartiteness FIRST when building apex counterexamples.
