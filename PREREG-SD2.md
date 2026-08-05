# FROZEN preregistration — SD-2STEP and the n = 12 prospective holdout

Branch `attempt/2026-08-05-claude-opus-5-4d7a`. Frozen 2026-08-05 after the
n <= 11 SD census (PREREG-SD.md, results in `work/sd/sd-n11-AGGREGATE.json`) and
**before** any n = 12 run of the v2 checker.

## 0. Provenance — read this before grading anything below

SD-2STEP was formulated **after** inspecting the six n = 11 A1 failures. It is
therefore **IN SAMPLE at n = 11** and its n <= 11 verification carries no
prospective weight: the only non-trivial n <= 11 instances are the 20 shortest
bad paths that suggested it. This is exactly the position B-PLUS-2 and
B-TERMINAL-SLIDE occupy, and exactly the configuration that has killed three
prior statements in this project at the next order up. **n = 12 is its first
prospective test and the only one that counts.**

## 1. What the n <= 11 census established (PREREG-SD.md, already frozen and run)

- `A1-ALL` failures at n = 11 = **6**, cycle components = **8,202,633** — both
  published anchors reproduced exactly.
- **SD-SHORT is FALSIFIED**, minimal order 11, 6 failures.
- **SD-COUNT-SHORT is FALSIFIED**, minimal order 11, 6 failures.
- **SD-PLUS-2**: 0 failures, n <= 11.
- **ONE-CYCLE is FALSIFIED**, minimal order **10** (5,269 two-cycle selections at
  n = 10; 130,811 at n = 11; the maximum ever observed is 2).
- Mechanism: all six A1-failing cycles sit in selections with `|cyc(J)| = 1`, so
  there was no second cycle to schedule. Cycle-choice scheduling is not vacuous
  in general (130,811 two-cycle selections at n = 11) but **is** vacuous exactly
  where A1 fails.

So the remaining scheduling freedom is over **moves**, not cycles.

## 2. FROZEN STATEMENTS

Setting as in PREREG-SD.md §0. A **minimising step** from a feasible selection
`K` is a residual toggle releasing an avoidable incidence on a selected cycle
`C` of `K` along a residual path of length exactly `d0(C)`.

- **SD-2STEP (mechanism form).** For every feasible `J` and every selected cycle
  `C` of `J` failing `A1(C)`: **every** minimising step of `J` at `C` lands on a
  selection `J0` that itself admits a CES minimising step (for some selected
  cycle of `J0`).
- **SD-2STEP-DESCENT (descent form — this is the one that would close the
  bipartite case).** For every feasible `J` and every selected cycle `C` of `J`
  failing `A1(C)`: **some** minimising step of `J` at `C` lands on a `J0` with
  `|cyc(J0)| <= |cyc(J)|` that admits a CES minimising step. The composite of the
  two minimising steps then reaches `|cyc(J0)| - 1 <= |cyc(J)| - 1` cycles.

**Why the descent form suffices.** If `A1(C)` holds for some cycle of `J`, one
minimising step already lowers `|cyc(J)|` (CES implies a strict decrease). If no
cycle of `J` satisfies `A1`, SD-2STEP-DESCENT supplies two minimising steps whose
composite lowers `|cyc(J)|`. Either way `|cyc(J)|` strictly decreases every one
or two steps, so the descent terminates at an acyclic feasible selection; by
fixed-edge parity and the degree count that is F2, hence the bipartite case
`ell >= 2 tau + 1`. **Lemma A is not used** (an all-forced cycle simply has no
avoidable incidence and is counted as an A1 failure with no minimising step, which
would FALSIFY SD-2STEP — so the checker's `lemmaA_violations` counter must stay 0
for the grading to be meaningful, and it is reported separately).

This is a genuinely different repair from B-PLUS-2/B-TERMINAL-SLIDE: those keep a
**single** toggle and lengthen it to `d0 + 2`; SD-2STEP keeps every toggle at
**minimum** length and spends a second step. Neither implies the other.

## 3. Checker

`work/sd/sd_scan2.py`, sha256 in `work/sd/SD2-SHA256.txt`, frozen and committed
before the n = 12 launch. It is `sd_scan.py` plus the `shortest_ces_exists`
probe; the probe fires only on A1-failing cycles, so every counter carried over
from v1 must reproduce v1's numbers exactly.

**Gold test (must pass before the n = 12 launch, or the run is void).** v2 at
n = 9 and n = 11 must reproduce, field for field, v1's numbers:
cycle components 24,195 (n=9) and **8,202,633** (n=11); `A1-ALL failures` 0 and
**6**; `SD-SHORT failures` 0 and 6; `SD-PLUS-2 failures` 0 and 0;
`lemmaA_violations` 0; `path_cap_hits` 0. In addition
`SD-2STEP probed` must equal 6 at n = 11 (one probe per A1 failure).

**Negative controls** are inherited from PREREG-SD.md §3 and were run and passed
on v1 (`--ces=always` → 0 failures everywhere; `--ces=never` → A1-ALL failures =
24,195 = every cycle component at n = 9, SD-SHORT failures = 24,195 = every
cyclic selection). Note the acknowledged gap: the `--ces=never` control does not
exercise the `SD-COUNT-SHORT` path, which is measured by direct cycle counting
rather than by the CES predicate.

## 4. The n = 12 holdout

Universe: all 212,780 connected bipartite graphs on 12 vertices
(`geng -bc -q 12`), every minimum FVS with `|S| >= 2`, every `e in E(H)`, every
feasible selection with a selected cycle. Sharded by graph index into **32**
shards, run 8 at a time, so that partial completion is a well-defined
deterministic subset of the universe rather than an unlabelled prefix.

**Decision rules, fixed now.**

1. A shard's output counts only if the shard ran to completion. At wrap-up, the
   verdict is reported over the **completed shards only**, named explicitly by
   index, with the covered fraction stated. Incomplete shards are
   ABORTED-NO-VERDICT.
2. `SD-2STEP-DESCENT failures >= 1` on any completed shard → **FALSIFIED**, with
   the full certificate preserved and independently re-verified by the
   symmetric-difference engine `work/sd/sd_reverify.py` before being reported.
3. `SD-2STEP-DESCENT failures = 0` over the completed shards → **prospectively
   supported at n = 12 on that subset**. This is NOT a verification of the
   statement in general and will not be reported as one.
4. The n = 12 figures for `A1-ALL failures`, `SD-PLUS-2 failures`,
   `lemmaA_violations` and the `ncyc` histogram are recorded as prospective
   results for those statements too — in particular this is the first n = 12
   data on `A1`, on the `<= d0+2` bound, and on Lemma A in this model since the
   n = 12 holdout of 2026-07-31 was aborted without a verdict.
5. No statement in §2 is edited after any n = 12 output is seen. Progress
   counters are operational only.

## 5. What each outcome means (fixed now)

- **SD-2STEP-DESCENT survives n = 12.** Then the scheduled-descent shape of
  ATTACK.md v3 target (b) is alive in its *move-ordering* form: the descent can
  be run entirely on shortest steps with one step of lookahead, and the `d0 + 2`
  slide is not needed. That is a cleaner proof obligation than B-TERMINAL-SLIDE
  (no path-lengthening, no terminal-slide geometry), and it is the statement the
  next attempt should try to prove.
- **SD-2STEP-DESCENT dies at n = 12.** Then shortest steps are genuinely
  insufficient no matter how they are scheduled, and the `d0 + 2` metric bound
  B-PLUS-2 is doing irreducible work. Target (b) collapses into the existing
  B-PLUS-2 programme and should not be pursued as a separate angle.
