# PHASE0_RECORD — WOWII Conjecture 40 close-out ledger (append-only)

*Redacted export of the project's internal append-only ledger. Mathematical content, entry identifiers, counts, and hashes are unchanged; internal process narration has been removed.*

RESULT_RECORD.md /
RESULT_RECORD-II.md are the closed prior archive. This ledger covers the two final
computational runs. STANDING: nothing committed without explicit authorization; preregistration
discipline (checker frozen + hashed BEFORE launch); timeouts/aborts -> UNKNOWN; failures
preserved with certificates and independently re-verified before reporting.

## Checker (FROZEN before launch)
- Source: phase0.c sha256 = 9f5cc32223f5c3d9990255fc61dbdf7e43d507ef5b5ba6f58cb29100cf36619e
- Built: `cc -O3 -o phase0 phase0.c` (binary sha256 440461b3e288fd51841324b594c53a16e4b5888394f0fb3473ef82e12be358dd
 — compiler-dependent; the SOURCE hash is the frozen artifact).
- Exact invariants for n<=11: f (max induced forest, subset scan + union-find), b (max
 induced bipartite, subset scan + 2-coloring), p (min path cover = n - max spanning linear
 forest, ham+dp bitmask). Second independent engines available for cross-check:
 inv40_a.py (networkx + brute Hamiltonian) sha256 e7989532..., inv40_b.py (B&B) 198ebb7e...

## RUN 1 — DIRECT-SWEEP-40 (FROZEN STATEMENT)
For every connected graph on 10 vertices: p(G) + b(G) + 1 <= 2 f(G).
Universe: ALL connected graphs on n=10 via `geng -c -q 10` (expected 11,716,571; rerun from
scratch, old partials distrusted). Failure = any G with p+b+1 > 2f -> save g6 + witnesses,
recompute with a second independent engine, then flag. Second-engine policy: on a
~10,000-graph deterministic sample (every 1171st), every low-slack graph (slack <= 1), and
every violation.

## RUN 2 — SV-CHECK (FROZEN STATEMENT)
For every connected NONBIPARTITE graph G: there exists a vertex t with o(G-t)=o(G)-1 and
p(G) <= p(G-t), where o=n-b. Universe: ALL connected nonbipartite graphs 3<=n<=9
(`geng -c -q n`, filter nonbipartite). Empty eligible set for a nonbipartite graph => engine
bug (HALT), not a failure. Failure = every eligible t has p(G-t)=p(G)-1. p can drop by at
most 1 under vertex deletion (asserted; p_drop_bugs counter).

## GOLD TESTS (all PASS, run with the frozen checker, BEFORE launch) — 2026-08-01
RUN1 invariants (f,b,p): K_10 (2,2,1); K_5,5 (6,10,1); K_1,9 (10,10,8); K_1,2/3/4 stars;
K_3,3 (4,6,1); K_2,2,2 (3,4,1); K_2,2,3 (4,5,1); K_1,1,1,3 (4,4,1); C_10 (9,10,1) — ALL PASS.
Regression: 995 connected graphs n=2..7 -> 995 enumerated, 0 violations.
RUN2 SV: K_5 (o=3,Elig=5,pass); C_5 (o=1,Elig=5); C_7 (o=1,Elig=7); K_1,1,1,3 (o=2,Elig=3);
K_1,2,4 (o=1,Elig=1,strict p increase); triangle+pendant (o=1,Elig=3) — ALL PASS.

## BENCHMARK (before projecting; single-threaded) — 2026-08-01
- RUN1: 50,000 connected n=10 graphs (f+b+p) in 5.72s => 8,740 graphs/sec.
- RUN2: connected nonbipartite n<=8 (11,859 graphs) in 0.4s; n=9 sample 19,427 nonbipartite
 graphs in 1.7s => ~11,000 graphs/sec.

## PROJECTIONS
- RUN1 full n=10 (11,716,571): ~1,340 s ~= 22 minutes.
- RUN2 full n<=9 (connected nonbipartite; total connected n<=9 ~= 273,565, most nonbipartite):
 ~1-3 minutes.
- STRETCH RUN1 n=11 (1,006,700,565 connected graphs; ~2-3x slower/graph): ~4 DAYS
 single-threaded. DEFAULT NO-GO; to be decided.
- STRETCH RUN2 n=10 nonbipartite (~11.7M x OCT loop; ~5,500 g/s est): ~35-60 minutes; to be decided.

## RUN STATUS
Preregistration complete (frozen checker hashed + gold + regression + benchmark, all BEFORE
launch). Main runs (RUN1 n=10, RUN2 n<=9) authorized deliverables. Stretch runs NOT started
(pending). Files STAGED, NOT committed (await explicit authorization).

## RUN 2 RESULT — 2026-08-01 (checker sha256 9f5cc322...)
Universe enumerated: connected nonbipartite graphs 3<=n<=9 = 272,209 graphs.
RESULT: violations=0; p_drop_bugs=0; empty-Elig HALTs=0; runtime 32.6s.
=> SV holds for EVERY connected nonbipartite graph n<=9. No failures => no certificates /
independent recomputation required (second-engine policy triggers only on a hit). PASS.

## STRETCH RUN 2 n=10 SV — LAUNCHED 2026-08-01 (authorized)
Same FROZEN SV statement + frozen checker (phase0.c 9f5cc322...), universe extended to ALL
connected nonbipartite graphs on n=10 (from geng -c -q 10, ~11.7M connected, nonbipartite
subset). Running concurrently with RUN1 (n=10 direct sweep); ~35-60 min est (longer under
concurrent CPU load). Result -> phase0-run2-n10-result.txt; any violation -> phase0-run2-VIOL.txt
(overwrites the empty n<=9 file — n<=9 had 0 violations, nothing lost). PENDING.

## RUN 1 RESULT — 2026-08-01 (checker sha256 9f5cc322...)
Universe enumerated: 11,716,571 connected graphs on n=10 -> EXACTLY matches expected count
(no halt). RESULT: violations=0; min_slack=0; low-slack (slack<=1)=115,154 (slack 0: 4,960
tight/equality; slack 1: 110,194); sample=10,005; runtime 1,574.9s (~26 min).
=> Conjecture 40 (p+b+1 <= 2f) VERIFIED for ALL connected graphs on 10 vertices. PASS.
SECOND-ENGINE VERIFICATION (independent of phase0.c): (a) inv40_b (B&B, genuinely different
algorithm) cross-checked the first ~20,000 low-slack graphs, 0 bound-violations, before it
STALLED on a pathological dense graph (B&B blowup) — killed, documented, NOT left hanging.
(b) phase0_verify2.py (independently-coded pure-Python bitmask: forest union-find scan,
bipartite 2-coloring scan, path-cover ham+dp) re-verified ALL 115,154 low-slack + 10,005
sample = 125,159 graphs, 0 bound-violations, ALL PASS (1,119s). Violations=0 so no
per-graph certificates required.

## STRETCH RUN 2 n=10 SV RESULT — 2026-08-01 (authorized)
Universe enumerated: 11,712,539 connected NONBIPARTITE graphs on n=10 (~4,032 bipartite
skipped; consistent with 11,716,571 total connected). RESULT: violations=0; p_drop_bugs=0;
empty-Elig HALTs=0; runtime 5,087.7s (~85 min, slowed by concurrent RUN1). => SV holds for
EVERY connected nonbipartite graph on n=10. PASS.

## n=11 GO/NO-GO ASSESSMENT (measured, not started) — 2026-08-01
Measured per-graph cost ratio n=11 / n=10 = 2.75x (n=10 9,731/s vs n=11 3,542/s under equal
load). Single-thread n=11 ~= 3,540/s => 1,006,700,565 / 3,540 ~= 79-85 h (~3.4 days).
Sharded on M1 Pro (6 P-cores + 2 E-cores; E ~0.4x a P): aggregate ~24,000/s => ~11.6 h
ideal all-8, ~13 h on 6 P-cores; REALISTIC with thermal throttling ~15-18 h wall.
Verification follow-up: low-slack density at n=10 = 0.98% => ~9.9M low-slack at n=11;
independent verify at ~160/s (n=11) => ~17 h solo, ~3 h sharded 6-way (or relax policy to
SAMPLE the low-slack). Requires: sample-interval re-tune + checker RE-FREEZE (new hash,
re-gold) before launch; ~100MB disk; machine dedicated+awake ~a day. STATUS: NOT started;
default was NO-GO; under consideration: an overnight multicore run, decision pending.

## PHASE 0 SUMMARY (all runs, 2026-08-01)
- Checker phase0.c FROZEN sha256 9f5cc322...; gold (invariants + SV) + 995-regression ALL
 PASS before launch.
- RUN1 direct-sweep n=10: 11,716,571 graphs, 0 violations, second-engine ALL PASS. PASS.
- RUN2 SV n<=9: 272,209 graphs, 0 violations. PASS.
- n=10 SV stretch: 11,712,539 graphs, 0 violations. PASS.
- Conjecture 40 exhaustively verified for all connected graphs n<=10; SV verified for all
 connected nonbipartite graphs n<=10. n=11 assessed (~15-18h overnight), not launched.
- Nothing committed (staged, pending authorization). O68 archive intact.

## RUN 1 n=11 EXTENSION — RE-FREEZE + LAUNCH (2026-08-01; authorized)
Same FROZEN statement (p+b+1 <= 2f for every connected graph); NO statement change. Harness
re-tuned for sharding + accounting only (sample interval 100000; per-shard count/lowslack/
sample/VIOL files; global HALT flag; per-shard start/finish timestamps; violation -> witness
sets gF/gB + HALT + exit 42). RE-FROZEN checker:
 phase0.c sha256 = bc7f614d90f421aa5a60d2791644c619230cb78216a943811327739d7225a464
 binary  sha256 = 4086aa5c95effb8beaec0f0a6590d973e57f655e9fccf9da4ad6d75c0c473757
GOLD (re-run on exact re-frozen build, BEFORE launch): RUN1 invariants ALL PASS; SV gold2
ALL PASS; 995-graph n<=7 regression 0 violations. Compute byte-identical in behaviour.
SHARDING: geng -c -q 11 r/192 for r=0..191 (proper partition of all 1,006,700,565 connected
n=11 graphs); 8 concurrent processes (M1 Pro 6P+2E) via xargs -P 8; per-shard resume (skip
shards whose count file shows status=DONE); HALT flag aborts all shards on any violation.
ACCOUNTING: shard counts MUST sum to exactly 1,006,700,565 or the run is INCOMPLETE.
VERIFICATION TAIL (FULL, not sampled): second independent engine (phase0_verify2.py
bitmask, robust) on ALL low-slack (slack<=1) concatenated from shards + a 10,000 random
sample. SV NOT run at n=11 (not authorized). Status: LAUNCHING.

## RUN 1 n=11 PRIMARY RESULT — 2026-08-02 (re-frozen checker bc7f614d...)
COMPLETE. 192/192 shards status=DONE, no missing shard ids. SHARD-COUNT SUM =
1,006,700,565 = EXACT expected count (accounting OK). violations=0; HALT=none;
min_slack=0 (equality cases). low-slack (slack<=1) streamed = 3,853,461; sample = 9,968;
wall time 18.11 h (8 processes, M1 Pro 6P+2E, geng res/192 sharding).
=> Conjecture 40 (p+b+1 <= 2f) VERIFIED for ALL 1,006,700,565 connected graphs on 11
vertices, 0 violations, exact enumeration. PASS (primary engine).
VERIFICATION TAIL — COMPLETE 2026-08-02. Independent second engine (phase0_verify2.py bitmask,
separately coded from phase0.c: f union-find scan, b 2-coloring scan, p ham+dp) re-checked ALL
3,853,461 low-slack + 9,968 sample = 3,863,429 graphs (FULL, not sampled). Sharded 32
chunks x 8 lanes; per-chunk rate ~57 g/s/core; 0 bound-violations, 0 BVIOL certificates.
=> Second-engine confirms the primary result on every low-slack (slack<=1) graph. PASS.

## RUN 1 n=11 FINAL — PASS (2026-08-02)
Conjecture 40 (p+b+1 <= 2f) VERIFIED for ALL 1,006,700,565 connected graphs on 11 vertices.
Primary engine (phase0.c bc7f614d..., re-golded before launch): 192/192 shards DONE, shard-count
sum = 1,006,700,565 EXACT, 0 violations, 18.11 h. Second independent engine: all 3,863,429
low-slack+sample re-verified, 0 violations. No committed artifacts beyond this ledger (review
req 7). Exhaustive verification now stands at n<=11 for Conjecture 40; SV at n<=10.

## SIDE TASK — n=11 equality (slack-0) count (2026-08-02, authorized, filter existing files only)
Post-processed the streamed low-slack shard files (phase0-n11-lowslack-[0-9]*.txt; field 2 = slack).
NO new sweep. slack distribution over the 3,853,461 low-slack graphs: slack-0 (equality,
2f = p+b+1) = 96,949; slack-1 = 3,756,512. (Compare n=10: equality = 4,960.) For paper.tex §6.

## RUN 1 n=8, n=9 — DIRECT-SWEEP-40 under the re-frozen protocol (2026-08-02; review R4)
Fills the n=8,9 layers under the SAME frozen checker as n=11 (phase0.c bc7f614d..., re-golded
clean before use) so that the "n<=11" claim is uniform under the dual-engine protocol (previously
these layers rested on the older pre-dual-engine archive).
- n=8: geng -c -q 8 -> 11,117 connected graphs = EXACT expected count; violations=0; min_slack=0;
 low-slack (slack<=1)=657. Second engine (phase0_verify_chunk.py bitmask) on all low-slack+sample
 (668 graphs): 0 bound-violations. PASS.
- n=9: geng -c -q 9 -> 261,080 connected graphs = EXACT expected count; violations=0; min_slack=0;
 low-slack (slack<=1)=6,098. Second engine on all low-slack+sample (6,359 graphs): 0
 bound-violations. PASS.
Per-n connected-graph counts now all verified under the frozen protocol: n=2..7 = 995 (regression),
n=8 = 11,117, n=9 = 261,080, n=10 = 11,716,571, n=11 = 1,006,700,565. => Conjecture 40 verified for
ALL connected graphs 2<=n<=11, dual-engine on every low-slack graph, 0 violations throughout.
