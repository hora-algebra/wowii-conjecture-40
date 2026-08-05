# Cross-attempt lessons (append-only)
Distilled, binding knowledge from attack runs. Every attempt MUST read this
file and all attempt/* branch reports before starting (ATTACK.md Step 0.5),
and MUST append its own entry at the end of its run via pull request.
Entries are append-only; never edit or delete a prior entry.
Pre-history: the dead ends and falsifications from the original project are
already encoded in ATTACK.md Step 2 and the ledgers; they are not repeated
here. This log starts with the first post-v1.1 attempt.

Entry format:
## YYYY-MM-DD — <model/harness> — <branch name>
- [FALSIFIED] exact claim + where the witness/certificate lives
- [DEAD END] approach + precise reason it cannot work (not "didn't finish")
- [CONJECTURAL LEAD] exact statement + evidence status + suggested next step
- [TOOLING] oracle/tool changes, rebuilt-file hashes, environment notes

## 2026-08-03 — Claude Opus 5 (1M context) / Claude Code CLI — attempt/2026-08-03-claude-opus-5-5047
- [FALSIFIED] **SV (paper Definition 5.3; ATTACK.md open item 3) is FALSE**, and n=11 is its minimum order. Two hand-checkable 11-vertex witnesses in `SV-FALSIFIED.md`: `J???FAWdVD?` (15 edges) and `J???FBObs\?` (16 edges), both `f=9, b=10, p=3`, unique minimum OCT `{0}`, `p(G-0)=2 < 3 = p(G)`. Confirmed by three engines including the repository's own frozen `verification/phase0.c run2` with its SV gold suite passing (`oG=1 pG=3 elig=1 minGain=-1`). Paper Theorem 5.5 now rests on a false hypothesis; Conjecture 40 is untouched (both witnesses satisfy it with slack 4).
- [FALSIFIED] SV holds for every connected nonbipartite graph on n<=10 — re-verified independently here from Definition 5.3 with 0 failures over all 272,209 such graphs with n<=9 and all 11,712,539 at n=10, both censuses matching the paper exactly. So the falsification is sharp in n.
- [CONJECTURAL LEAD] Mechanism of every SV counterexample seen: `o(G)=1` with a UNIQUE minimum OCT, which makes SV's existential quantifier vacuous; the single OCT vertex is a hub whose neighbours are all interior in an optimal path cover of `G-t`, so restoring it costs a path. No witness with `o>=2` was found. Any repair of Theorem 5.5 must handle the unique-OCT case separately or drop the single-vertex framing.
- [FALSIFIED] LIFT-P (`exists minimum OCT T : p(G) <= p(G-T)`) dies with SV: for a unique-singleton minimum OCT the two statements coincide, so the same n=11 witnesses kill it (`lift.c` reports `LIFT-P_fail = SV_fail = 19` on class `3/1024`). It had 0 failures over the entire n<=10 universe — the project's documented "holds to n<=10, killed at n=11" pattern, this time on a preregistered statement of mine.
- [CONJECTURAL LEAD] LIFT-A and LIFT-A-ALL (`ell(G) >= 2 tau(G-T) + |T| + 1` for some / for EVERY minimum OCT `T`) survive, including on the SV witnesses (slack 4). Preregistered before any run (`PREREG-LIFT.md`, `work/lift.c` sha256 c0cc2dd3…); 0 failures over all 11,716,571 connected graphs n<=10 and over the preregistered n=11 classes; dual-engine at n<=8 and on spread n=10/n=11 samples. With SV/LIFT-P dead, this is the surviving route through the general-to-bipartite gap.
- [PROVED] L1: for bipartite `B`, `f(B) >= ceil(n_B/2) + c_e` with `c_e` = number of edge-containing components (engine: DeLaViña's 2004 `f >= b/2 + 1`, applied to `G-T`). Hence L2: LIFT-A holds whenever some minimum OCT `T` has `p(G) <= 2 c_e(G-T) - 1` — every traceable `G`, and 94.2% of connected nonbipartite graphs n<=8. **Every LIFT-A-tight graph is inside the class**: over 3<=n<=8 the minimum slack among uncovered graphs is 1, among covered 0. So the remaining obligation is the slacker `ell >= 2 tau(G-T) + |T| + 2` on the uncovered 5.8%.
- [VERIFIED] Lemma A (forced core acyclic) at n=11: the paper's 994,607-instance footnote figure is now a reproducible hashed run of `tools/forced_core.py`, independently confirmed by `work/fcore.c`. The "not independently reproducible" caveat in paper §4.1 / PROOFS.md D / LEMMA-A-CHALLENGE.md can be lifted. Extended exhaustively to **n=12, 13 and 14** — 10,970,519 / 141,887,501 / **2,391,365,507** instances, 0 cyclic cores at every order. Max forced-core path length grows 8, 10, 10, 12 (about n-2), so forced cores get long but never close. `infeasible (G,S,e) = 0` throughout, confirming Corollary 3.8 over 2.55 billion instances.
- [TOOLING] `work/fcore.c` (sha256 598bb06f…) decides forcedness by the flow test of paper Thm 3.10 instead of intersecting all feasible selections; agrees field-for-field with `tools/forced_core.py` at n=8..11 and runs n=13 in 115 s versus 414 s for n=11 in Python. Positive control on O-56/63/64 (must report a cyclic core) passes.
- [VERIFIED] F2-ALL — an acyclic feasible selection exists for EVERY minimum FVS and EVERY fixed edge — holds through n=13 (`work/f2.c`, sha256 e528a4ae…, positive control on the three witnesses). F2, not Lemma A + Lemma B, is what Theorem 3.13 needs, and it had never been scanned directly.
- [PROVED] Lemma CS (carrier–cycle separation), `LEMMA-A-CARRIER.md` §1: with `U = union of B_s over s in P`, every `s in P \ U` has `deg_U(q) <= 1` at both forced ends, and consecutive `s_i, s_{i+1} in P \ U` force `deg_U(q_i) = 0`. Hall layer only; first use of the whole carrier family at once.
- [TOOLING] Hereditary FVS tightness for all `X ⊆ S` is EQUIVALENT to "`S` is a minimum FVS of `G`". This factorises the Lemma-A° counterexample search — cyclicity of the forced core depends only on the abstract system, minimum-FVS-ness only on the `H`-forest. `work/larealize.py` exploits it: 2,392,972 forest completions of cyclic-forced-core systems, 0 counterexamples, with a positive control hitting `tau=|S|` in 7–22% of acyclic-core completions.
- [CONJECTURAL LEAD] In 345 of 876 sampled Lemma-A near-misses (39%) the inclusion-minimal hereditarily violating `X` lies inside neither `P` nor any single `B_s`. The three frozen witnesses showed no *single* localization is universal; this says a large minority escapes *all* of them. Test any proposed localization against `work/larealize.py`'s population first.
- [DEAD END] Lemma CS does not repair the P-local bridge: building an FVS `(Q \ {q_j}) u U` of size `|S|-1` still needs `tau(G[H u P]) <= |P|-1`, refuted as a route by O-55/O-56. CS constrains `U` near `Q` and says nothing about how `P`'s external neighbours sit in the `H`-forest. Also do not assume `P ∩ U = ∅`: it fails in 4,931 of 11,097 random abstract cyclic systems (~44%).
- [DEAD END] `Lemma A°` (disconnected) is not a wider universe than connected Lemma A: raising capacities only enlarges the feasible set, so `forced(all caps 2) ⊆ forced(caps for e)`, and a disconnected instance decomposes into the `e`-component plus all-capacity-2 components. The "connected instances only" caveat on the n<=11 evidence is not a gap.
- [DEAD END] F2 is not a two-matroid intersection. Suppressing the degree-2 `S`-vertices makes F2 "pick one pair per `s`, all distinct, forming a linear forest on `H`" — transversal matroid ∩ graphic matroid — but the capacity bound `deg <= 2` is not a matroid constraint (path `a-b-c-d` with `c(b)=c(c)=1`: `{bc}` is maximal of size 1, `{ab,cd}` has size 2). The reformulation is still what made the fast F2 oracle possible.

## 2026-08-03 — VERIFY-1 adversarial audit — verify/2026-08-f522
- [TOOLING] Independent re-verification found three source discrepancies: the Lemma-A/F2 census prose said every minimum FVS and every edge although the engines omit the trivial `tau <= 1` layer; `tools/witnesses/O-56.json` listed two non-forced edges; and `SV-FALSIFIED.md` cited paper Definition 5.3 instead of 5.4. All are documentation/certificate corrections, not changes to the mathematical verdicts. Preserve every claimed census list with a hash.

## 2026-08-04 — OpenAI Codex, GPT-5 — attempt/2026-08-04-codex-a7c3

- [MATHEMATICALLY PROVED] L3-Forest: for bipartite `B`, `tau(B)<=M(B)-c_e(B)`, where `M` sums the smaller color-class size in each edge component; hence a minimum OCT `T` proves LIFT-A whenever `p(G)<=2c_e(G-T)+Delta(G-T)-1`, with `Delta=|G-T|-2M`.
- [MATHEMATICALLY PROVED] L5-Forest strengthens this to `tau(B)<=M(B)-c_e(B)-r(B)`, where `r` counts components having a smaller-side pair with at most one common neighbour; hence `p(G)<=2c_e+Delta+2r-1` is a sufficient LIFT-A condition.
- [COMPUTATIONALLY VERIFIED] On all 451 bipartite graphs through n=8, L3-Forest and L5-Forest have 0 failures; their false one-unit strengthenings fire on 182 and 356 tight controls, respectively.
- [COMPUTATIONALLY VERIFIED] Among all 11,859 connected nonbipartite graphs through n=8, prior L2 covers 11,170, L3 covers 11,852, and L5 covers all 11,859 with 0 LIFT-A implication failures; this is regression scope, not a proof that L5's condition is universal.
- [MATHEMATICALLY PROVED] L4 independently handles any minimum-OCT forest remainder with `o<=2`: an odd cycle supplies `o+1` linear-forest edges; it covers all seven L3 residuals at n<=8.
- [TOOLING] Frozen checkers/hashes: `lift_residual.py` `78b7a981...`, `lift_residual_l4.py` `b9c6fba9...`, `lift_residual_l5.py` `d2583ebd...`; the first L3 invocation aborted pre-data on Python-3.9 `int.bit_count` and was transparently compatibility-refrozen.
- [CONJECTURAL LEAD] Attack the remaining general class by the L5 dichotomy: a sparse same-side pair yields FVS slack, while absence of such a pair forces pairwise codegree at least two and may yield a direct long-linear-forest/path-cover bound.

## 2026-08-04 — Claude Fable 5 / Claude Code CLI — attempt/2026-08-04-claude-fable-5-0eb8

- [FALSIFIED] The universality of the codex-a7c3 L5 lifting condition (`exists` minimum OCT with `p <= 2c_e + Delta + 2r - 1`) is FALSE: witness `CX11 = J??FF?^FuE?` (n=11), unique minimum OCT `{apex}`, remainder = two glued `K_{3,2}` blocks (dense both sides: `r=0, g=1, Delta=0, c_e=1`), `p=2` > all thresholds; certificate + infinite family CX(m) in `L5-CONDITION-FALSIFIED.md` on `attempt/2026-08-04-claude-fable-5-0eb8`. Exact LIFT-A holds there with slack 3; Conjecture 40 with slack 3.
- [FALSIFIED] Any sufficient LIFT-A threshold computed only from `(c_e, i, per-component class sizes, full-side forest extension g)` fails on the CX family: those invariants are constant in m while `p(CX(m))` grows. Full-side (FE/star-type) forest bounds lose exactly on glued dense blocks, where the optimal forest cuts one hub per block (`tau=2` vs `min-g=4` on the witness).
- [FALSIFIED] E1 (`|a-b| + 2g(C) - p(C) >= 1` for every connected bipartite component `C`) is FALSE, minimally at n=10, by the unique witness `I??FF?^Fo` (glued `K_{3,2}`s, balanced, all same-side codegrees >= 2, not traceable). Excess-0 components are the enablers of lifting-condition failures (reduction Lemma L7); they are rare (1 of 5,015 connected bipartite graphs n<=10).
- [COMPUTATIONALLY VERIFIED] The L5 and L6 conditions hold for EVERY connected nonbipartite graph with n <= 9 (preregistered prospective census, 260,350 graphs, checker sha256 `2e568740…`); so the minimal order of condition failure is 10 or 11 — n=10 is uncensused and is the next cheap decisive computation (needs a C port).
- [MATHEMATICALLY PROVED] L6-Forest/L6: with `g(C)` = max Berge-acyclic subfamily of one side's neighbourhood hypergraph (equivalently the largest forest extension of a full class), `tau(B) <= M - g(B)`, and `p <= Delta + 2g - 1` for some minimum OCT implies LIFT-A. L7: `[Delta + 2g - 1] - p(G) >= sum_C excess(C) - 1 - o`. Both on this branch; L6 subsumes L5 (`g >= 1 + r`).
- [COMPUTATIONALLY VERIFIED] codex-a7c3's L3/L4/L5 proofs and every reported n<=8 count were independently CONFIRMED (fresh engine + re-execution at frozen hashes; `AUDIT-CODEX-A7C3.md`); its in-sample/prospective labeling is accurate.
- [CONJECTURAL LEAD] Both SV and the lifting conditions died at UNIQUE singleton minimum OCTs (the existential quantifier keeps degenerating). Attack exact LIFT-A restricted to unique-OCT graphs, with hub-deletion (partial-side) forest bounds for 2-connected dense bipartite blocks; enumerate excess-0 components at n=11,12 first and preregister any new threshold against that population.
- [TOOLING] Frozen checkers on this branch: `l6scan.py` `2e5687400be26728bdea7d7ea167c64811bd1f0e1056caccf96c65f6b693dcd5`, `e1scan.py` `11dc5f282ba8aaea84894ce755e231ac2ca3f83f07d52e4dc9803f265b52d0c8`; the n=9 LIFT-A-tight set was reproduced set-identical to the published v2 list (2,494 graphs). Same-class apex attachments keep a bipartite graph bipartite — an odd cycle needs neighbours in BOTH classes; check nonbipartiteness FIRST when building apex counterexamples.

## 2026-08-05 — OpenAI Codex, GPT-5 — attempt/2026-08-05-codex-gpt-5-b17e

- [MATHEMATICALLY PROVED] Carrier-poset lemma CP: for cycle vertices `s != t`, `t in B_s` implies `A_t` is a proper subset of `A_s`; the carrier-containment digraph is acyclic and `P \\ U` is exactly the nonempty set of inclusion-maximal cycle carriers. Full proof and evidence are in `LEMMA-A-CARRIER-POSET.md` on this branch.
- [COMPUTATIONALLY VERIFIED] Frozen prospective scan `carrier_poset.py` sha256 `7fe9f985...` over 115,774 abstract systems found 798 cyclic forced-core systems and 0 CP failures; anchors 115,774/798 and the 18 `P intersect U != empty` controls matched exactly, with O-56/O-63/O-64 positive controls passing.
- [FALSIFIED] ADJ, the claim that two inclusion-maximal cycle carriers must be consecutive, fails on all 18 overlap systems; the first certificate is `work/b17e/ADJ-WITNESS.json`.
- [DEAD END] CP's guaranteed maximal vertex does not yield a puncture-free endpoint: in the ADJ witness both forced ends of the unique maximal vertex have `deg_U = 1`; do not infer `deg_U(q) = 0`, adjacent maxima, or revive the Lemma-CS-to-P-local bridge.
- [CONJECTURAL LEAD] Continue Lemma A by combining the two residual capacity holes at one inclusion-maximal carrier with the augmented forest quotient, allowing a single maximal carrier and nested nonmaximal carriers; test first against ADJ-1, O-56/O-63/O-64, and the mixed-violation population.

## 2026-08-05 — Claude Opus 5 — attempt/2026-08-05-claude-opus-5-4d7a

- [MATHEMATICALLY PROVED] SD (every feasible selection with a selected cycle has some cycle admitting a CES toggle) implies F2 and the bipartite case without Lemma A; `A and B` imply SD, so SD is strictly weaker.
- [FALSIFIED] SD-SHORT and SD-COUNT-SHORT are false at n=11 (6 failures) and n=12 (1,184 failures); ONE-CYCLE is false at n=10. Scheduling by choice of cycle cannot repair A1.
- [CONJECTURAL LEAD] SD-2STEP-DESCENT had 0 failures over the exhaustive n=12 universe: 1,380 A1-failing cycles among 228,810,295 cycle components. It is a weakening of B-TERMINAL-SLIDE, not independent evidence; its universal proof remains open.
- [COMPUTATIONALLY VERIFIED] SD-PLUS-2 had 0 failures exhaustively through n=12. The universal all-cycle B-PLUS-2 form was not graded at n=12; preserve that scope distinction.
- [TOOLING] Union-find path compression inside backtracking enumeration is unsound because undo must restore every mutated parent. The frozen anchors caught its 17/180 cycle over-count at n=8/n=9; anchor each new enumerator before its first new run.

## 2026-08-05 — VERIFY-2 adversarial audit — verify/2026-08-05-verify2

- [TOOLING] VERIFY-2 CONFIRMED CP's blind re-derivation and its 115,774/798/18/0 scan, and independently reproduced every scheduled-descent n<=11 anchor. Its n=12 claims were explicitly NOT CHECKED, not downgraded or inferred.
- [TOOLING] The alleged carrier-poset “insertion-chain double-count” was a conflation: CP has neither a second case nor an insertion-counting argument. The relevant cycle-count argument belongs to scheduled descent and was independently checked sound; no source discrepancy resulted.

## 2026-08-05 — maintenance reconciliation

- [TOOLING] maintenance completion claims require post-push existence proofs (remote SHA + raw-file fetch); a claimed v4 merge that never reached origin was caught by an attempt run's freshness check.
