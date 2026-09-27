# HOC baseline and errata — handoff v1, 2026-09-27

This is the reconciled planning baseline, not a certificate. It supersedes the original Issue #10 where they differ. Original bundle files are preserved unchanged, including historical statements corrected here. `PROVENANCE.md` identifies their exact origins and source snapshots.

## 1. Fixed research target and outcomes

**HARD-ONE-CYCLE (HOC): every hard state has exactly one selected cycle.** The intended campaign concerns connected finite simple bipartite graphs, minimum feedback vertex sets and the fixed-edge capacity model below. A proof with weaker hypotheses is welcome; it does not silently broaden the campaign's refutation universe.

The target is not Conjecture 40, HSO, SAFE-2 or F2. A reviewed HOC proof or a certified HOC counterexample completes the objective, even if found quickly. Budget-scoped exhaustion must preserve investigated routes, failures, remaining obligations and why no justified next move fits that budget. Merely reaching a runtime/token limit is not mathematical exhaustion. Finite zero-failure coverage is a separately scoped result, not a universal proof or automatic terminal success.

HOC can simplify hard-state structure, but does not itself settle successor/descent. The existing relocation theorem already handles arbitrary cycle counts. Conversely, HOC implies mu<=1, where mu is the minimum cycle count over feasible selections: a minimizer with >=2 cycles cannot have a CES minimizing step and would be a multi-cycle hard state. Thus HOC is not just an innocuous local observation.

## 2. Definitions that must survive transport

Use pinned 064c `PROOFS-SAFE2-064c.md` §0, with the explicit conventions and errata below.

- G is finite, simple and bipartite, with original parts L and R. S is a minimum feedback vertex set; H=G-S is a forest. For every X contained in S, hereditary FVS tightness gives tau(G[H union X])=|X|.
- e=xy is a distinguished edge of H. Capacities kappa(x)=kappa(y)=1; all other H vertices have capacity 2.
- A feasible selection J assigns each s in S exactly two distinct H-neighbors and obeys the capacities. The incidence graph has only those selected S-H edges. H's own edges, including e, are NOT edges of this incidence graph. Include isolated H vertices as trivial path components.
- Its connected components are paths and cycles. c(J) counts cyclic components; P(C)=V(C) intersect S and Q(C)=V(C) intersect H. T(J) is the set of S vertices on path components.
- Saturated means deg_J(h)=kappa(h); slack means strict inequality. A cycle is slack-free when every H-neighbor in G of every s in P(C) is saturated.
- A selected incidence is avoidable if some feasible selection omits it. Release a=(s0,h0). A residual augmenting path is a simple alternating sequence s0,h1,s1,...,h_k: forward incidences are not in the ORIGINAL J, backward incidences are in J, the released arc is deleted from the residual network, and h_k is slack in J-a. Length is 2k-1. Its alternating toggle, together with deletion of a, returns a full feasible selection J0.
- d0(C) is the minimum residual path length over ALL avoidable incidences of C. A minimizing step has that cycle-wide length. Finding a shortest path for one release is not necessarily a minimizing step for C.
- CES for C means C is destroyed and every selected cycle of J0 is an original selected cycle of J. Compare cycle identity/edge sets, not only c(J0)<c(J). A count-decreasing move that creates a different cycle need not be CES.
- C is A1-good iff some minimizing step for C is CES; otherwise A1-bad. A cycle with no avoidable incidence is A1-bad by the project's convention. Do not silently assume d0 is finite in that case.
- A hard state is cyclic and has every selected cycle A1-bad. HOC is equivalent to c(J)>=2 implying at least one A1-good cycle.

**The forced-core Lemma A remains OPEN.** Neither the target nor the new theorem assumes it. A proposed proof must handle the no-avoidable-incidence convention rather than excluding it by fiat.

Length-one residual steps are CES. The exact local equivalence is **d0(C)=1 iff a cycle-side S vertex has a slack H-neighbor**. It follows that A1-bad implies slack-free. The converse is false: slack-free cycles can be A1-good via longer minimizing CES steps. There is no inherited universal bound of three on the length of an A1-good cycle's minimizing CES step.

## 3. Theorem A and the new starting point

The complete proof is in `THEOREM-A.md`. Its source v2 original remains unchanged in the archive. The readable copy replaces only the introductory "Equivalently" with "More specifically, we prove" and records that edit: the proof establishes a constructive assertion stronger than the headline theorem.

**Status: claimed, with complete proof; two non-blind concurring reviews, one cross-vendor, plus machine replays. Not certified under the project's environmentally blind protocol.** The new campaign must perform its own appropriate verification and record exposure honestly. Certification is not implied by uploading files, matching hashes or model concurrence.

Core facts and proof mechanism:

1. In each incidence component all H vertices lie in one original bipartition class. The capacity-1 endpoints x and y are in different original classes and cannot lie on selected cycles, so they occupy distinct path components. With p=|H|-|S|, p>=2. **|H|>=|S|+2 is an invariant of every feasible instance**, not a special pruning test.
2. Class-wise accounting gives |Sat intersect R|=|S intersect L|-r_R+delta_R<=|S intersect L|, with r_R the number of nontrivial paths whose H-side is R and delta_R the degree-1 capacity-1 end indicator in R. Summing yields **|Sat|=|S|-r+j<=|S|**. Total slack remains 2p-2.
3. For each q in Sat intersect R, tightness on the whole class S intersect L forces some s there to have two neighbors in (Slack intersect R) union {q}. Otherwise deleting (Sat intersect R) minus {q} is a too-small FVS. This is the slack-pair lemma.
4. The nonempty union of same-oriented slack-free cycle S-sides needs a saturated neighbor outside their combined cycle H-sides; it lies on a nontrivial path. This is the class-anchor lemma.
5. If T is empty, no anchor exists. If T={t}, the only possible anchor is a capacity-1 end of the path x-t-w. The slack-pair lemma forces an explicit residual length-three CES move through its owner t, contradicting hardness. Therefore **every hard state has |T|>=2**.

Connectedness is unused in Theorem A; its proof works for finite simple bipartite G with H a forest, hereditary tightness and the capacity convention. This is a stronger inherited statement, not a reason to discard the intended connected-graph campaign boundary.

Corollaries, subject to verification of that proof:

- A hard state with k>=1 cycles has |S|>=2k+2 and n>=4k+6.
- HOC holds through n<=13. The old n=13 prospective target test has a theorem-determined answer.
- At n=14, a counterexample must have |S|=6, |H|=8, exactly two selected 4-cycles, |T|=2 and exactly two path components, those containing x and y separately.
- Three cycles in a hard state require n>=18. A two-cycle counterexample with a cycle longer than four requires n>=16.
- HOC implies mu<=1 for every instance with feasible selections.

The proposed n=14 exclusion of opposite orientation, star geometry of H and interior-anchor restrictions are **UNVERIFIED SKETCHES**. They are retained in the source theorem's appendix only. They are not hypotheses, conclusions or sound filters for the new campaign.

## 4. Binding errata overlay for inherited sources

Use section labels and pinned commits in `PROVENANCE.md`, not unqualified current line numbers.

| Source location | Correction |
|---|---|
| 064c Theorem 2 title, Remark 2.1; ATTEMPT_REPORT result 2; CL-2 title; main LESSONS lines 142 at the pinned snapshot | d0=1 iff slack adjacency. NOT A1-good iff slack adjacency. A full A1 classifier still needs residual analysis on slack-free cycles. |
| 064c Theorem 10 SECOND equivalence; ATTEMPT_REPORT item 9 | CL-6=>SAFE-2-EXISTS is established; the converse is unproven, not refuted. A CL-6 failure does not refute SAFE-2-EXISTS. The first hard-set escape equivalence survives this objection. |
| 064c Remark 5.3; §7 sentence saying Theorem 2 settles every non-hard state in one length-one step; ATTEMPT_REPORT item 12; main LESSONS line 145 at the pinned snapshot | Replace "length-one CES step" with **"minimizing CES step"**. Do NOT replace it universally with "length 1 or 3". Three is proved for Theorem A's particular construction and observed in named finite records. |
| 064c Prop. 12(iii) | Sharpen the loose |Sat|<=|S|+1 to |Sat|=|S|-r+j<=|S| using class-wise accounting. |
| 4d7a cycle-count commentary | Arbitrary k-cycle selections need n>=4k+2: two cycles cannot occur at n=9; three cannot occur at n=13. Hard states obey the stronger n>=4k+6 bound. |
| Initial Issue #10 | Replace the n=13 holdout, old runtime extrapolation, overstated empirical motivation, loose counting intuition and provenance claims with this packet. |

A direct finite witness to the length-one error is that **158 of the 196 n=12 (2,1) selections have both cycles slack-free**, so none has any length-one cycle step. All 1,894 good-cycle witnesses in the retained both-slack-free n=12 records are length three. Do not extend that observed length to arbitrary instances.

The unmodified audit report contains old "negative control" wording for O-63, "discovery use" wording for the n=14 sizing sample, and an inadequately qualified deterministic-wait recommendation. The corrected dispositions below supersede those phrases.

## 5. Evidence and provenance boundaries

The supplied runs are regression and mechanism evidence. There are no supplied HOC target results in the unresolved n>=14 region. Their absence through n=13 is explained by Theorem A, subject to its verification. That does not make the old data useless; it changes what they can support.

Key n=12 anchors:

| Quantity | Count |
|---|---:|
| All connected bipartite graphs | 212,780 |
| Graphs with tau>=1 in the C full-census table | 212,229 |
| Fixed instances in that table | 11,223,582 |
| Feasible selections | 1,468,422,722 |
| Selected cycle components | 228,810,295 |
| Two-cycle selections | 5,912,277 |
| Slack-free cycles | 1,422,156 |
| A1-bad cycle occurrences | 1,380 |
| Hard selections, profile (1,0) | 1,184 |
| Selections with profile (2,1) | 196 |
| Selections with profile (2,0) | 0 |
| Both-slack-free two-cycle selections | 1,026 = 158 (2,1) + 868 (2,2) |

At n=11 there are six hard tuples on three graphs. At n=12 the 1,184 hard tuples span 280 graphs. The 1,026 both-slack-free two-cycle selections have (|S|,|H|)=(5,7), |T|=1. At n=13 the reported 28,821 such selections have (5,8), |T|=1, again no counterexample.

Do not conflate these provenances:

- 1,468,422,722 is the 064c all-feasible count reproduced by Claude's C census. The older 4d7a scheduled-descent census reported 222,898,018 cyclic selections and used |S|>=2.
- The profile table counts selections, not bad-cycle occurrences; the relevant numbers coincide only because each recorded row has one bad cycle.
- 064c `report_n12.py` copied the 1,184/196 split from 4d7a. Its own hard and bad counts alone did not independently determine the whole profile.
- 7851 and VERIFY-3 closed the missing 44 retained records. All 1,184 were subsequently graded for HSO/OPE/CL-6/CL-7. The census had already identified them. OPE's one-cycle condition supplied an additional population check.
- HOC was selected using n<=12 data; those are in-sample observations. n=13 was later run as a check of the new theorem, not a preserved holdout.
- Reported full absence results come from full enumerations: August engines plus Claude/referee rechecks at n<=12; Claude's engine at n=13. They are not independently established by ChatGPT's certificate replay.
- ChatGPT's independent Python verifier replayed 2,216 supplied certificate rows on 320 distinct graphs (3 at n=11, 317 at n=12), 31,276 minimizing paths and 6,188 constructive steps, with zero failures. It did not import Claude's code; NetworkX served graph6 decoding/bipartiteness. This checks retained positive records, not the omitted graph universe.
- ChatGPT's C rerun on the 317 certificate graphs reproduced the relevant bad/hard/profile counts for that subset. Claude reports re-running the independent verifier with matching JSON apart from timing, successful assertion-triggering mutations, and byte-identical C replay JSON on those graphs. Preserve this as a reported audit of the artifacts, not a new blind trial.

## 6. Computation and controls

Use the supplied C engine as a reference implementation, not an unquestionable oracle. Regress it and retain an independently coded verifier for any discovery. Exact minimum-FVS, feasibility, cycle identity and exhaustive minimizing-step checks are required for a genuine counterexample. Resource/path caps, incomplete shards and errors must be visible and cannot be counted as zero failures.

**Production pruning:** tau(G)>=6 at the instance level. Assert |H|>=|S|+2 as an invariant. Per selection, only >=2 cycles, all slack-free and |T|>=2 require HOC search. The theorem-dependent filters require accepted proof support; a filtered sweep provides no independent test of cases excluded by that theorem.

**Controls:** n=11/12 anchors (including the 1,026 both-slack-free selections), construction replay, CES-always/CES-never mutants, tau+1 FVS negative control for the slack-pair lemma, and O-63 positive HOC-detector control. Exercise controls without inappropriate production pruning.

O-63, with its given S, has tau(G)=3<|S|=5. Each of six selections has a forced 4-cycle with no avoidable incidence, and a genuinely A1-bad 6-cycle with d0=3 and six minimizing steps, none CES. The classifier must report six (2,0) states under the no-step convention. These are **positive detector controls**, NOT target counterexamples, because minimum-FVS tightness fails. Applying tau>=6 or |T|>=2 before this control would incorrectly skip the test.

## 7. n=14 exposure, resources and execution

The exact sizing partition was nauty 2.8.8 `geng -bc -q 14 0/400`, containing 159,611 graphs, approximately 0.51% of the 31,193,324-graph universe. Shards are not assumed equally sized.

Claude's follow-up states only instance counts (5,909,851 for |S|>=4; 10,084 for |S|>=6), feasible-selection counts (14,815,011,763 and 35,372,045 respectively) and CPU time were computed on it. **No cycle, slack, A1 or HOC output was computed.** The accurate label is target-blind sizing exposure, not prior target-discovery data. Disclose the exposure and record the operator's prospective policy; inclusion in full finite coverage is distinct from claiming untouched input.

Historical C timings: n=12 full census about 20.5 wall seconds on two cores / 36 CPU-seconds; n=13 HOC sweep about six wall minutes on two cores. Filtered n=14 about 23 CPU-minutes is an upper-leaning sizing extrapolation, not a completed run, guaranteed bound or laptop benchmark. The slice method overestimated completed n=13 workloads in Claude's calibration. The original 68-hour Python extrapolation is not a planning basis.

Recommended opening investigation is n=14 in the actual campaign, after checker/spec freeze and controls. Higher n remains an in-scope tactic only with justified information gain and resources, not an automatic obligation. No new n=14 research was done in packaging this handoff.

The previous execution audit at OTR checkout 81f7a8b found that formal Claude child environments drop the BASH timeout variables, settings sources are disabled, and Monitor is not allowed. The default foreground Bash maximum was ten minutes. Lack of a model-action wall-clock cap is not evidence of unlimited tool waiting; background tasks are not a qualified durable compute mechanism. Codex's equivalent behavior was not checked. **Current-check and qualify the actual launch route before GO.**

Freeze checker/spec in an earlier canonical action and execute in a later legal action, publishing results through normal ownership. Do not introduce an informal post-GO operator import. For longer waits, the operator must choose a qualified route, a bounded pre-GO timeout-setting change, or explicitly accepted chunking; no launcher change has been made by this handoff. Local multi-day CPU tolerance does not authorize repeated expensive inference or cloud spending.

## 8. Reconciliation dispositions and pending decisions

The substantive mathematical baseline and C1-C8 corrections from Claude's audit response were accepted, with these explicit amendments: no universal "length 1 or 3" replacement; change Theorem A's "Equivalently" to a stronger-assertion introduction; distinguish connected target scope from weaker theorem hypotheses; bypass production filters for invalid-hypothesis controls; preserve theorem dependency of pruning; and qualify the actual harness wait route rather than inferring it from action duration.

The prior broad review round is complete. Remaining pre-GO work is operational and protocol-bound: honest source/admission delivery, exact destination campaign/profile and numeric budget, real laptop calibration, prospective shard policy, and any selected launch timeout qualification/change. The suggested n=14 reservation and shard treatment remain recommendations until captured as actual operator choices. Creating this packet authorizes none of those silently and does not authorize GO.
