# Preregistration — SAFE-2-EXISTS structural attack (branch 064c)

Frozen BEFORE the checker is run on mathematical data. The checker
`work/064c/s2e_scan.py` is hashed into `work/064c/SHA256.txt` in the same commit
as this file, before any target run.

## 0. Provenance of inputs (what I treat as given, and at what grade)

Binding, supplied by the operator and corroborated by the checked-in records
named below:

- `SAFE-2-EXISTS ⟹ F2` is settled; I am proving the hypothesis, not the
  implication. (Recorded proof: `PREREG-SAFE-EXISTS.md` §3 on
  `attempt/2026-08-05-codex-gpt-5-9d2b`.)
- Universal all-cycle `B-PLUS-2` is exhaustively clean through n=12
  (composite census, 9d2b ATTEMPT_REPORT Result 1).
- `B-TERMINAL-SLIDE` and unrestricted `SUCCESSOR-ONE` are FALSIFIED at n=12
  (9d2b Result 2, witness `K??FFbw}Fw^_`). Not rebuilt on here.
- `SD-2STEP-DESCENT` survives n=12; `HARD-SUCCESSOR-ONE` is the recorded
  conjectural lead, scope = states with no A1-good cycle.
- The Lemma-A machinery (carriers `A_s`/`B_s`, carrier poset CP, NC, NCM/CE,
  A-I⁺) is available; `verify4-package/VERIFY4_REPORT.md` grades the
  derivations of NC, NCM/CE and A-I⁺ as CERTIFIED.

Everything below that I derive is labelled independently of the above.

## 1. Setting and notation (fixed here, used by the checker)

Model of paper Definition 3.2: `G` connected bipartite with classes `L,R`;
`S` a minimum FVS; `H = G−S` a forest; `e = xy ∈ E(H)`; `c(x)=c(y)=1`,
`c(h)=2` otherwise. A feasible selection `J` gives each `s ∈ S` exactly two
incidences, each `h ∈ H` at most `c(h)`.

- `sat(h)` : `deg_J(h) = c(h)`. `slack(h)` : `deg_J(h) < c(h)`.
- A selected cycle `C` is a cyclic component of `J`; `P(C)=V(C)∩S`,
  `Q(C)=V(C)∩H`.
- Residual digraph `D_J`: arcs `s→h` for `(s,h) ∉ J`, `h→s'` for `(s',h) ∈ J`.
  Releasing an avoidable `a=(s_0,h_0)` of `C`, a residual augmenting path is a
  simple `D_J`-path from `s_0` to an `h` with `deg_{J−a}(h) < c(h)`; its length
  is its number of incidence edges (odd).
- `d0(C)` = min such length over avoidable incidences of `C`.
  `C` is **A1-good** if some length-`d0(C)` step is CES for `C`, else **A1-bad**.
- `J` is a **hard state** if it is cyclic and has no A1-good selected cycle.
- `c(J)` = number of selected cycles.

## 2. Claims graded (each stated exactly; predicted verdict in brackets)

**CL-1 (LENGTH-ONE-CES).** [predict 0 failures — I claim a proof]
For every feasible `J`, every selected cycle `C`, every avoidable incidence
`a=(s,h)` of `C` and every residual augmenting path of length 1 from `s` in
`N−a`, the resulting toggle is CES for `C`.

**CL-2 (A1-GOOD ⟺ SLACK-ADJACENCY).** [predict 0 failures — I claim a proof]
For every feasible `J` and selected cycle `C`:
`d0(C)=1` ⟺ some `s ∈ P(C)` has a `G`-neighbour `h ∈ H` with `slack(h)`.
Consequently every cycle with a slack-adjacent `S`-vertex is A1-good, and every
A1-bad cycle has `d0 ≥ 3`.

**CL-3 (BAD-STEP STRUCTURE at length 3).** [predict 0 failures — I claim a proof]
Let `C` be A1-bad with `d0(C)=3` and let `J → J0` be a bad minimizing step,
released `a=(s,h)`, path `s,h1,s1,h2`. Then
(a) `h1 ∉ Q(C)`;
(b) the component `K` of `h1` in `J` is a path component, and `s1 ∉ P(C)`;
(c) `J0` has exactly one selected cycle `Z` that is not a selected cycle of `J`;
(d) `V(Z) ∩ V(C) = ∅`;
(e) `c(J0) = c(J)`;
(f) `deg_{J0}(h) = c(h)−1`, i.e. the released `H`-endpoint is slack in `J0`.

**CL-4 (CYCLE HAS AN OUTSIDE NEIGHBOUR).** [predict 0 failures — I claim a proof]
For every feasible `J` and selected cycle `C`: `N_H(P(C)) ⊋ Q(C)`.

**CL-5 (ONE-SIDED FOREST-HALL BOUND).** [predict 0 failures — I claim a proof]
For every `X ⊆ S` inside one bipartition class and every `Y ⊆ H` with
`|N_G(s) ∩ Y| ≤ 1` for all `s ∈ X`: `|Y| ≤ |H| − |X|`.

**CL-6 (HARD-SUCCESSOR-SLACK, existential).** [conjectural: the target]
For every hard state `J` there is a minimizing step `J → J0` with
`c(J0) ≤ c(J)` such that some `S`-vertex lying on a selected cycle of `J0` has
a `slack(J0)` `G`-neighbour. (By CL-1/CL-2 this is exactly
HARD-SUCCESSOR-ONE with the CES obligation discharged.)

**CL-7 (HARD-SUCCESSOR-SLACK, universal).** [conjectural, strictly stronger]
The same conclusion for EVERY minimizing step out of a hard state.

**CL-8 (SLACK-FREE CLOSURE IS TIGHT).** [predict 0 failures — I claim a proof]
Let `C` be a selected cycle and `A*` the `D_J`-closure of `P(C)`
(`A_0=P(C)`; `Y_i = ⋃_{s∈A_i} (N_H(s) \ J(s))`; `A_{i+1} = A_i ∪ owners(Y_i)`).
If no `h ∈ Y* ` is slack then (i) `A*` is `ρ`-tight; (ii)
`W := N_H(A*) \ Y* ≠ ∅`; (iii) every incidence between `A*` and `W` is forced.

## 3. Universe, controls, decision rules

Universe U(n): every graph of `geng -bc -q n` (connected bipartite), every
minimum FVS `S` with `|S| ≥ 1`, every `e ∈ E(H)`, every feasible selection.

Controls, all required to pass BEFORE any target verdict is read:
1. `geng -bc -q n` counts for n=6..9 reproduced.
2. Feasibility: every `(G,S,e)` admits at least one feasible selection
   (paper Corollary 3.9). A single failure aborts the run.
3. Hereditary tightness: `τ(G[H∪X]) = |X|` re-derived for random `X ⊆ S`
   (independent of the FVS routine used to pick `S`).
4. Positive control for CES detection: a hand-built selection whose toggle
   creates a new cycle must be reported non-CES.
5. Anchor: n=9 cycle-component count and A1-failure count compared with the
   9d2b record (730 graphs / 24,195 cycle components / 0 A1 failures).
   A mismatch is reported, not silently reconciled.

Decision rules:
- Any CL-1..CL-5, CL-8 failure REFUTES my proof; the certificate is preserved
  and the claim is relabelled FALSIFIED in the report. No proof is written up
  before its scan is clean.
- CL-6/CL-7 failures are recorded as counterexamples with full certificates
  (graph6, `S`, `e`, `J`, `C`, path). A CL-7 failure with CL-6 clean is a
  meaningful separation, not a refutation of the target.
- Zero failures earns `COMPUTATIONALLY VERIFIED (exhaustive U(n))`, never
  `MATHEMATICALLY PROVED`. Proofs are graded separately and only for the
  statements where a written derivation exists in this branch's report.
- Incomplete runs at wrap-up: `ABORTED-NO-VERDICT`, shards retained.
