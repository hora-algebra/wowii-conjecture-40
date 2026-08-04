# paper.tex — claims-to-sources table (for review)

Every theorem, lemma, and number in `paper.tex` mapped to its source: a section of
`PROOFS.md` (as corrected by the review audits), another repo document, or a
ledger entry (`PHASE0_RECORD.md` / `RESULT_RECORD.md`). Source discipline: math
content is from `PROOFS.md` in its corrected form; every computational number
cites a ledger entry and, where relevant, a checker hash.

## Theorems and lemmas

| paper.tex item | Statement | Source |
|---|---|---|
| Conjecture 1.1 (WOWII #40) | `f >= ceil((p+b+1)/2)` | PROOFS.md §A; GENERAL-TO-BIPARTITE.md prior-art |
| Thm 2.1 (Equivalence) | conjecture ⇔ `ell+o >= 2tau+1` | PROOFS.md B1/C1 (PROVED); verified 995/995 n≤7 (PHASE0_RECORD B1/GOLD) |
| §2 margin `mu = ell+o-(2tau+1)`; ceiling-equality ⇔ mu∈{0,1} | margin definition, do not conflate with ceiling | PROOFS.md B1 margin NOTE |
| Prop 2.4 (Equality families) — TWO margin formulas: `p = max(1, 2n_r - n)`; if p=1 `mu = n_r - n_{r-1}`, if p>1 `mu = (n-n_r) - n_{r-1} + 1` | linear-tight iff traceable + equal top two parts; every K_{a,b} (a<b) and every star K_{1,m} (m>=2) has mu=1 | **Derived in this paper** from PROOFS.md B1 margin def (R1 correction: the single-formula version was wrong for stars/understated K_{a,b}). Both formulas agree at boundary 2n_r=n+1; cross-checked against golds K_10(2,2,1), K_5,5(6,10,1), K_1,9(10,10,8), C_10(9,10,1) (PHASE0_RECORD GOLD TESTS) |
| Def 3.1 (Selection model) | demand-2 / capacity model, fixed edge e | PROOFS.md §A |
| Def 3.2 (CES move) | semantic cycle-erasing definition | PROOFS.md §A (CES canonical); FROZEN-BPLUS2.md |
| Lem 3.3 (Hereditary FVS tightness) | `tau(G[H∪X])=|X|` | PROOFS.md C2 (PROVED) |
| Lem 3.4 (Generalized Hall) | feasible ⇔ `rho(X)>=2|X|` ∀X | PROOFS.md C5 (PROVED; full min-cut) |
| Lem 3.5 (Forced ⇔ tight-exposed, F1) | forced iff tight X exposes | PROOFS.md C5/F1 (PROVED) |
| Lem 3.6 (Tight-set lattice) | tight sets closed under ∩,∪ | PROOFS.md C6 (PROVED) |
| Lem 3.7 (Rooted forest extension) | `tau(G[H∪X]) <= floor(rho_e(X)/2)` | PROOFS.md C5b (PROVED; full induction) |
| Cor 3.8 (Feasibility ∀e) | `rho_e(X)>=2|X|`; feasible for every e | PROOFS.md C5b CONSEQUENCE |
| Lem 3.9 (Fixed-edge parity, Lemma 0) | e on no selected cycle | PROOFS.md C3 (PROVED) |
| Thm 3.10 (Residual augmentation) | avoidable ⇔ one-move avoidable; **flow proof over N−a** | PROOFS.md C4 (PROVED; repaired flow proof — NOT the old symmetric-difference sketch) |
| Cor 3.11 (no R2x) | globally-avoidable-but-not-one-move is empty | PROOFS.md C4 corollary |
| Lem 3.12 (Descent) | CES toggles terminate → acyclic selection | PROOFS.md C8 (PROVED) |
| Thm 3.13 (Reduction of bipartite case) | Lemma A + Lemma B ⇒ bipartite conjecture; `J∪{e}` spanning linear forest with `2|S|+1` edges; E(H)≠∅ for tau≥1 | PROOFS.md B3 + B3′ (F2 standalone) + F2/§G |
| §4 Lemma A necessity (hereditary tightness, not Hall alone) | abstract even-cycle counterexample | PROOFS.md D; RESULT_RECORD O-45 CORRECTION 1, O-47 |
| Open Problem 4.1 (Lemma A°) | forced core acyclic, **stated without connectedness** | PROOFS.md D (LEMMA A°) |
| Lem 4.2 (A-I closed-neighbourhood subcase) | `N_H(P)⊆Q` ⇒ contradiction | PROOFS.md D (Lemma A-I, PROVED) |
| Lem 4.3 (Tight-set saturation) | `load=min(c,deg_X)` | PROOFS.md D (PROVED) |
| Lem 4.4 (Common tight carrier) | unique min tight set `A_s` | PROOFS.md D (PROVED) |
| Lem 4.5 (Punctured tightness) | `B_s=A_s\{s}` tight; k=2 | PROOFS.md D (PROVED) |
| Lem 4.6 (Carrier-cycle separation, CS) | conclusions (a)--(d) for the whole carrier family | `LEMMA-A-CARRIER.md` §1.1 (proved); `verify_independent/BLIND_PROOFS.md` (independent derivation and comparison) |
| Lem 4.7 (Single-blocker subcase) | independent `U_h` ⇒ contradiction | PROOFS.md D (PROVED) |
| Lem 4.8 (`T_F` normalization) | WLOG `S=T_F`; forcedness re-derived via F1 | PROOFS.md D (T_F NORMALIZATION, PROVED, accepted in review) |
| Witnesses O-56 / O-63 / O-64 | kill B_s-/P-/degree localizations; O-64 explicit graph | PROOFS.md D; LEMMA-A-CHALLENGE.md §witnesses; RESULT_RECORD O-56/O-63/O-64 |
| Open Problem 4.9 (Lemma B) | CES toggle always exists | PROOFS.md E; FROZEN-BPLUS2.md |
| Prop 4.10 (Terminal-slide criterion, B1) | (H1)-(H5) ⇒ `J+` CES | PROOFS.md E (B1, PROVED conditional lemma) |
| Lem 5.1 (monotonicities) | `ell(G)>=ell(G-T)`, `tau(G-T)>=tau(G)-|T|` | PROOFS.md B5 (i),(ii) |
| Lem 5.2 (edge lemma) | `b >= alpha+1` | PROOFS.md B5 (iv) |
| Thm 5.3 (conditional coeff-2) | `ell+2o >= 2tau+1` given bipartite theorem | PROOFS.md B5 (PROVED conditional); GENERAL-TO-BIPARTITE.md |
| Def 5.4 (SV) | single-vertex property | GENERAL-TO-BIPARTITE.md |
| Thm 5.5 (Single-vertex reduction) | SV + bipartite ⇒ full conjecture (induction) | GENERAL-TO-BIPARTITE.md (PROVED as an implication) |
| Def 5.6 (LIFT-A / LIFT-A-ALL / LIFT-P / LIFT-P-ALL) | minimum-OCT lifting statements | `PREREG-LIFT.md` (frozen before sweep); `ATTEMPT_REPORT.md` R6 |
| LIFT-A implies the full conjecture given the bipartite case | `ell(G) >= 2tau(G-T)+|T|+1` and vertex-deletion monotonicity | `PREREG-LIFT.md` recorded implications; `ATTEMPT_REPORT.md` R6 |
| Lem 5.7 (L1) | bipartite `f(B) >= ceil(n_B/2)+c_e(B)` | `ATTEMPT_REPORT.md` R6 (proved); `verify_independent/BLIND_PROOFS.md` (independent derivation, no gap) |
| Lem 5.8 (L2) | `p(G) <= 2c_e(G-T)-1` implies LIFT-A | `ATTEMPT_REPORT.md` R6 (proved); `verify_independent/BLIND_PROOFS.md` (independent derivation, no gap) |
| Traceable corollary | L2 applies when `p(G)=1` | `ATTEMPT_REPORT.md` R6; paper Lemma 5.2 supplies `c_e>=1` |

## Numbers (all with ledger source; checker hashes noted)

| Number in paper | Value | Source |
|---|---|---|
| Equivalence regression | 995 connected graphs n≤7 (=1,2,6,21,112,853), agree | PHASE0_RECORD B1 / GOLD TESTS |
| n=8 universe | 11,117 connected graphs, 0 violations, min slack 0, low-slack 657; 2nd engine 668, 0 viol | PHASE0_RECORD RUN 1 n=8,n=9 (hash `bc7f614d`) — R4 run |
| n=9 universe | 261,080 connected graphs, 0 violations, min slack 0, low-slack 6,098; 2nd engine 6,359, 0 viol | PHASE0_RECORD RUN 1 n=8,n=9 (hash `bc7f614d`) — R4 run |
| n=10 universe | 11,716,571 connected graphs, 0 violations, min slack 0 | PHASE0_RECORD RUN 1 RESULT (hash `9f5cc322`) |
| n=10 low-slack / equality / sample | 115,154 / 4,960 / 10,005; 2nd engine 125,159, 0 viol | PHASE0_RECORD RUN 1 RESULT |
| n=11 universe | 1,006,700,565 connected graphs; 192 shards sum exact; 0 violations, min slack 0 | PHASE0_RECORD n=11 PRIMARY + FINAL (hash `bc7f614d`) |
| n=11 low-slack / equality / slack-1 | 3,853,461 / 96,949 / 3,756,512 | PHASE0_RECORD n=11 PRIMARY + SIDE TASK |
| n=11 second-engine total / sample / wall | 3,863,429 re-verified 0 viol; sample 9,968; 18.1 h | PHASE0_RECORD n=11 VERIFICATION TAIL / FINAL |
| SV n≤9 | 272,209 connected nonbipartite, 0 violations | PHASE0_RECORD RUN 2 RESULT |
| SV n=10 | 11,712,539 connected nonbipartite, 0 violations | PHASE0_RECORD STRETCH RUN 2 n=10 RESULT |
| Lemma A exhaustive n≤10 | forced core acyclic, 0 cyclic (n=7..10) | RESULT_RECORD O-44 (forced_core.py) |
| SV witness 1 | graph6 `J???FAWdVD?`; `f=9,b=10,p=3,o=1`, eligible `{0}`, `p(G-0)=2`, slack 4 | attempt `SV-FALSIFIED.md`; `ATTEMPT_REPORT.md` R7; VERIFY-1 `VERIFY_REPORT.md` rows 2, 5, 31 |
| SV minimality and residue check | 272,209 nonbipartite through n=9 and 11,712,539 at n=10, 0 failures; class `3/1024` at n=11 has 363,207 nonbipartite and 19 failures | attempt `ATTEMPT_REPORT.md` R6/R7; VERIFY-1 `VERIFY_REPORT.md` rows 6--8 |
| LIFT full n≤9 | 273,191 connected / 272,209 nonbipartite; 0 LIFT-A and LIFT-A-ALL failures | attempt `ATTEMPT_REPORT.md` R6; VERIFY-1 `VERIFY_REPORT.md` row 26 |
| LIFT n=10 full census | 11,716,571 connected / 11,712,539 nonbipartite; 0 LIFT-A and LIFT-A-ALL failures; 52,303 tight | attempt `ATTEMPT_REPORT.md` R6; release closure `verification/v2-lift-census/README.md`; VERIFY-1 engine SHA `af5e7cbf...` |
| LIFT n=11 preregistered holdout | classes 1,2,3/1024: 2,051,196 connected / 2,045,943 nonbipartite; 0 A/ALL, 19 SV and LIFT-P failures, 5,093 tight | attempt `PREREG-LIFT-N11.md`; `ATTEMPT_REPORT.md` R6/R7 and jobs table |
| LIFT tightness cross-tab n≤8 | covered `217/666/2773/3978/3255/281`; uncovered `0/43/249/199/198/0` | attempt `ATTEMPT_REPORT.md` R6; proofs independently audited in `verify_independent/BLIND_PROOFS.md` |
| LIFT tight lists | n=9: 2,494, SHA `6078480935...`; n=10: 52,303, SHA `9fe71fb1c...` | VERIFY-1 `VERIFY_REPORT.md` row 27; release closure `verification/v2-lift-census/SHA256SUMS.txt` |
| Connected-bipartite anchors n=11..14 | 25,598 / 212,780 / 2,241,730 / 31,193,324 | independent `geng -c -b`; VERIFY-1 `VERIFY_REPORT.md` rows 9--12; OEIS A005142 |
| Lemma A n=11..14 | 994,607 / 10,970,519 / 141,887,501 / 2,391,365,507 scoped instances; 0 cyclic cores (aggregate 2,545,218,134) | attempt `ATTEMPT_REPORT.md` R1/R2, `work/fcore.c` SHA `598bb06f...`; VERIFY-1 `VERIFY_REPORT.md` rows 13--18, `verify_independent/forced_core.c` SHA `25ce6906...` |
| F2 n=8..13 | 2,186 / 13,003 / 116,216 / 994,607 / 10,970,519 / 141,887,501 scoped instances (aggregate 153,984,032); 0 F2-ALL and F2-SOME failures | attempt `ATTEMPT_REPORT.md` R3, `work/f2.c` SHA `e528a4ae...`; VERIFY-1 `VERIFY_REPORT.md` rows 20--24, `verify_independent/f2.c` SHA `fd55562b...` |
| Census scope | every minimum FVS with tau≥2, every H-edge; tau≤1 omitted as trivial | VERIFY-1 `VERIFY_REPORT.md` discrepancy note 1; corrected v2 prose |
| Checker hashes printed in §6 | phase0 `17db663b...`; attempt lift/fcore/f2 `c0cc2dd3...` / `598bb06f...` / `e528a4ae...`; VERIFY lift/fcore/f2 `af5e7cbf...` / `25ce6906...` / `fd55562b...` | `verification/SHA256SUMS.txt`; attempt `work/*-SHA256.txt`; hashes of committed VERIFY-1 sources |
| Lemma B falsification / gap dist | shortest-only false at n=11 (6 witnesses); gap {0: 8,202,627 ; 2: 6} | PROOFS.md E; FROZEN-BPLUS2.md |

## Provenance flags (honesty)

- **Lavrov-Vandenbussche identity** `delta_2(S) + Lambda-def(S) = supp(S) - |S|` (§7):
 supplied by the reviewer in the PHASE 1 instruction for the related-work
 framing. It is **NOT** present in or derived from the repo proof documents;
 stated in the paper (with a footnote) as the bridge to [LV2024], not claimed as
 a verified result of this project.
- **Lemma A census scope**: v2 states the implemented nontrivial universe
 exactly: every minimum FVS with `tau>=2`, every `H`-edge. The omitted
 `tau<=1` layer is structurally incapable of an incidence cycle.
- **B-PLUS-2 / terminal-slide**: presented as in-sample-supported refinements of
 an OPEN lemma (two sentences), not as theorems. O-68 branch content, A1/U1
 forensics (one sentence), internal protocol/role narration, and frozen-motif
 statistics are excluded per instruction.
- **Excluded computational scopes** (not cited as support in the paper): the
 direct Conjecture-40 sweep at the OLD partial n=10 (~59%, no verdict) — the
 paper uses only the COMPLETE re-run (RUN 1 RESULT); the aborted n=12 Lemma-B
 holdout (no verdict).
- **Reference URLs (confirmed)**: the WOWII open-problems URL `[2]`
 (`http://cms.uhd.edu/faculty/delavinae/research/wowII/open.html`) and the
 formal-conjectures file path in `[3]`
 (`FormalConjectures/WrittenOnTheWallII/GraphConjecture40.lean`) are confirmed;
 the nauty citation (McKay–Piperno, J. Symbolic Comput. 60 (2014) 94–112,
 doi:10.1016/j.jsc.2013.09.003) is standard. Data availability: repository
 `https://github.com/cozuya/wowii-conjecture-40` (release `v2.0`), archived at
 doi:10.5281/zenodo.21778700.

## Review revision round (R1–R13) — resolution

| Item | Fix applied |
|---|---|
| R1 | Prop 2.4 reproved with two margin formulas (`p=max(1,2n_r-n)`; p=1 → `n_r-n_{r-1}`, p>1 → `(n-n_r)-n_{r-1}+1`); stars/K_{a,b} corrected; golds kept |
| R2 | Lemma 4.7 (T_F) — replaced sketch with full 4-step proof (i)-(iv); "Proof." not "Proof sketch."; connectedness remark kept |
| R3 | Lemma B restated "…containing an avoidable incidence"; Thm 3.13 proof chain via Lemma A → avoidable incidence → Lemma B → descent; deleted "not vacuously obstructed" |
| R4 | Ran frozen checker (bc7f614d) over n=8 (11,117) and n=9 (261,080), exact counts, 2nd engine on all low-slack, 0 viol; §6 bullet rewritten as 2≤n≤10 with per-n counts; ledger appended |
| R5 | cycle total 8,202,627 → **8,202,633** (8,202,627 gap-0 + 6 gap-2) |
| R6 | §7: [LV] conjecture (not characterize) covering one side X by ≤ Λ-def(G) paths, proved for forests/max-deg-3/regular high-girth; identity stated for all-capacity-2 with supp(S), Λ(S) defined inline; intro phrase changed |
| R7 | Def 5.4 SV quantifier fixed ("Say SV holds if for every … G there is a vertex t …") |
| R8 | Lemma 4.2 — added the alternation clause placing P in one bipartition class |
| R9 | Lemma 4.4 — "canonical" deleted; inclusion-minimal exposers exist by finiteness |
| R10 | Lemma 4.6 — replaced dangling phrase with derivation `deg_{A_s}(h) ≥ 3, s∈N(h) ⇒ |U_h| ≥ 2` |
| R11 | Witness block — added sentence: none is a hereditarily-tight instance carrying a forced cycle / counterexample to A°; O-56 & O-63 adjacency re-verified char-by-char vs RESULT_RECORD certificates (match) |
| R12 | Lemma 3.6 — added why `min(c,deg_X)` submodular (concave nondecreasing ∘ modular) |
| R13 | [2] WOWII URL + dates; [3] repo URL + file path; added [4] nauty (McKay–Piperno) cited in §6 |
