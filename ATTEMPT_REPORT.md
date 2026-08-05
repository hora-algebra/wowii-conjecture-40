# ATTEMPT REPORT

**Branch:** `attempt/2026-08-05-codex-gpt-5-b17e`
**Model / harness:** OpenAI Codex, GPT-5; macOS arm64; Python 3.9.6;
Homebrew nauty `geng`
**Date:** 2026-08-05
**Base:** post-maintenance `main-local` at `85d1483`
**Soft time budget declared at start:** 2 hours
**Publication status:** LOCAL ONLY; no push, PR, public post, credential use,
or release action

**Outcome in one line:** **MATHEMATICALLY PROVED** a carrier-containment poset
lemma that guarantees `P\U` is nonempty on every forced-core cycle, and
**FALSIFIED** the stronger adjacent-maxima route with a preregistered exhaustive
scan and independently checked certificate. Lemma A and Conjecture 40 remain
OPEN.

## Setup and branch discipline

The starting checkout in the prompt was a verification branch, not the right
attack base. The older repository at
`/Users/christineozols/research/wowii-conjecture-40` did not contain the fresh
maintenance census branch. I therefore cloned locally from
`/Users/christineozols/conj40v2/conj40-verify`, which exposed the complete local
ref set: post-maintenance `main-local`, all three attempt branches,
`lessons/consolidated`, and `maint/2026-08-census`.

Fresh clone:

```
/Users/christineozols/conj40v2/conj40-attack-codex-20260805-b17e
```

The required fetch

```
git fetch origin '+refs/heads/*:refs/remotes/origin/*'
```

completed. I detached at `origin/main-local`, read ATTACK.md v3 in full, then
created the unique attempt branch
`attempt/2026-08-05-codex-gpt-5-b17e`. Main and every pre-existing branch were
left unchanged.

## Step 0 — freshness check

**Status: COMPUTATIONALLY VERIFIED as a live read-only check on 2026-08-05.**

| source | method | finding |
|---|---|---|
| GitHub issues / PRs | unauthenticated GitHub REST API | `[]` / `[]`: no open issue or PR |
| MathOverflow 513887 | direct page fetch | answer count 0; comment count 0; no post modification after creation |
| maintained WOWII page | direct HTTP fetch and inspection of entry 40 | status remains `O`; only the 2004 path-cover-one annotation is present |
| web / arXiv | exact DuckDuckGo searches and arXiv API query for the conjecture names | no new proof, counterexample, or lemma result; results were the project repository and formal-conjectures statement; arXiv total 0 |

Nothing found externally changed the run's objective.

## Step 0.5 — binding prior evidence

**Status: READ AND ACCEPTED AS BINDING EVIDENCE.** I fetched and read
`attempts/LESSONS.md` and all three complete attempt reports:

- `attempt/2026-08-03-claude-opus-5-5047` (648 lines);
- `attempt/2026-08-04-codex-a7c3` (282 lines);
- `attempt/2026-08-04-claude-fable-5-0eb8` (238 lines).

I did not re-walk any `[FALSIFIED]` or `[DEAD END]` item. In particular I did
not revive shortest-path-only Lemma B, P/`B_s`/`T_F` localization, SV,
LIFT-P, the L5/L6 universality claims, the class-size/full-side threshold
family, or the Lemma-CS-to-P-local bridge.

### Fresh maintenance censuses

**Status: COMPUTATIONALLY VERIFIED, BINDING INPUT.** I read
`PREREG-MAINT-CENSUS.md`, `MAINT-CENSUS-REPORT.md`, every order-10 shard
summary, and every order-11/12 excess witness on
`origin/maint/2026-08-census` before choosing a target.

- The order-10 universe was all 11,716,571 connected graphs, of which
  11,712,539 were nonbipartite. Exact LIFT-A had 0 failures and its 52,303
  tight graphs matched the published set.
- The older L5 condition has 7 failures at order 10, all with `p=3,o=1`,
  L5 margin `-1`, L6 margin `+3`, and exact LIFT-A slack 3. These supersede
  CX11 only as minimal L5-condition witnesses.
- L6 covers every connected nonbipartite graph through order 10. CX11 is the
  exact minimum L6-condition failure at order 11.
- The complete excess-`<=0` population is 2 graphs at order 11 and 16 at
  order 12. The order-12 layer contains the first negative excess values,
  `-1` and `-2`.

These results reinforced the hard obstruction against new full-side lifting
thresholds. No threshold claim was proposed in this run.

## Step 1 — comprehension gauntlet

**Status: MATHEMATICALLY PROVED / COMPLETED.** `GAUNTLET.md` is a fresh
268-line derivation of:

1. the complete Theorem 3.13 reduction, with Lemma A used only to provide
   Lemma B's avoidable-incidence premise and Lemma B used only for descent;
2. the abstract even-cycle calculation `rho(X)=2|X|` and
   `tau(G[H union S])=1<|S|`, showing Hall feasibility alone cannot imply
   Lemma A;
3. the forcing and killed strategies of O-56, O-63, and O-64; and
4. the `T_F` normalization, including re-forcing by F1 rather than a false
   monotonicity assumption.

Before use, `shasum -a 256 -c tools/SHA256SUMS.txt` passed 17/17. Independent
`work/wcheck.py` reproduction of O-56/O-63/O-64 found feasible-selection counts
`1/6/1`, forced-core cycle rank one on all three, and the complete carrier and
hereditary-tightness profiles.

**TOOLING SCOPE CORRECTION.** O-63's JSON calls the full puncture `B_s` the
“first inclusion-minimal violation.” The independent complete subset scan
finds other global size-two violations, such as `{a,s}`. The recorded statement
is correct only within `B_s`: every proper subset of that puncture is tight and
`B_s` itself has `tau=2<3`. This does not affect any strategy it falsifies.

## Exactly one primary target

I chose **Lemma A via the `T_F`-normalized carrier machinery** (ATTACK.md Step
3 target 1). This was the controller's highest-priority unspent mechanism;
only Lemma CS had been harvested from it. The general-to-bipartite route had
absorbed the prior attempts and its full-side threshold family is now
CX-obstructed. No Lemma B or LIFT work was mixed into this attempt.

## New claim CP — carrier-containment poset

**Status: MATHEMATICALLY PROVED, not Lean-formalized.** Full statement and
proof: `LEMMA-A-CARRIER-POSET.md`.

Let a forced-core cycle have `S`-side `P`. For each `s in P`, let `A_s` be its
canonical minimum Hall-tight carrier, `B_s=A_s\{s}`, and
`U=union_(s in P)B_s`.

> If distinct `s,t in P` satisfy `t in B_s`, then
> `A_t proper-subset A_s`. Hence the carrier-containment digraph is acyclic,
> all cycle carriers are distinct, and `P\U` is exactly the set of vertices
> whose carriers are inclusion-maximal. In particular `P\U` is nonempty.

Proof: punctured tightness makes `B_s` tight. Since it contains `t`, canonical
minimality gives `A_t subseteq B_s`, while `B_s=A_s\{s}` is a proper subset of
`A_s`. Arcs therefore strictly descend by inclusion. The characterization of
`P\U` follows in both directions, and a finite carrier family has a maximal
member.

**New consequence — MATHEMATICALLY PROVED.** Lemma CS(a) says that every
`s in P\U` has `deg_U(q)<=1` at both forced ends. CP proves such an `s` always
exists. Thus every forced-core cycle has at least one cycle vertex whose two
forced ends each retain a unit of capacity outside the union of punctures,
without assuming the known-false condition `P intersect U=empty`.

## Preregistration and prospective scan

`PREREG-CARRIER-POSET.md` froze CP, the stronger conjectural lead ADJ, the
universe, anchors, controls, and decision rules before the target execution.
Checker and dependency were committed first at:

```
7fe9f98569bb4bebb980b69dbb734993b82f4d5c499ad1efa3dab90a2f4d7222  work/b17e/carrier_poset.py
d11b0bca3a4ac437b4811ce588e660fe2e382ccd725e017fbadd2919e195696a  work/carrier.py
```

Positive controls O-56/O-63/O-64 passed CP and reproduced their carrier
profiles. The known-false PDIS negative control fired. The target was exactly
`carrier.gen_exhaustive(3,5)`:

```
TARGET systems=115774 cyclic=798 pdis=18 CP_fail=0 ADJ_fail=18
```

**Status: COMPUTATIONALLY VERIFIED.** Universe: 115,774 abstract systems,
798 feasible systems with a cyclic forced core; CP failures 0. All three
published anchors matched exactly. Runtime: 4.21 s wall. Raw output is
`work/b17e/carrier-poset-scan.txt`.

## ADJ falsification

**Status: FALSIFIED.** ADJ proposed that two inclusion-maximal cycle carriers
must be consecutive, which would trigger Lemma CS(b) and give some
`q in Q` with `deg_U(q)=0`. It failed on all 18 overlap systems. Per the
preregistered decision, no in-sample repair was attempted.

The first certificate has

```
S=P={s0,s1,s2}; H-incidence vertices={0,1,2}; all capacities 2
N(s0)={0,1}; N(s1)={0,2}; N(s2)={0,1,2}
A_s0={s0}; A_s1={s1}; A_s2=S
U={s0,s1}; P\U={s2}
```

The unique feasible selection is `s0->{0,1}`, `s1->{0,2}`,
`s2->{1,2}`, whose forced core is the 6-cycle
`s0-0-s1-2-s2-1-s0`. Only `A_s2` is maximal, so no adjacent maximal pair
exists. Adding an incidence-free `K2` supplies the fixed capacity-one edge in
the disconnected paper model.

**Status: COMPUTATIONALLY VERIFIED by an independent engine.** The
machine-readable `work/b17e/ADJ-WITNESS.json`, checked with `work/wcheck.py`
(no shared code), is bipartite with `H` a forest, has one feasible selection,
six forced edges, cycle rank one, and the carrier table above. A separate
acyclic unique-selection negative control returned cycle rank zero.

The certificate is not a Lemma A counterexample:
`tau(G[H union S])=1<3`, so hereditary FVS tightness fails. It falsifies only
the Hall-layer adjacent-maxima shortcut. It also shows CP's two capacity holes
need not include any endpoint with `deg_U(q)=0`.

## Dead ends and incidents

- **FALSIFIED:** ADJ / adjacent maximal carriers. The exact reason is a valid
  forced 6-cycle can have one maximal carrier containing both other cycle
  vertices; `P\U` is then a singleton. This route is closed without an
  independently justified new hypothesis.
- **DEAD END honored, not re-walked:** CP does not revive the Lemma-CS-to-
  P-local bridge. It provides local capacity holes, not an FVS of
  `G[H union P]`; O-56 remains binding.
- **ABORTED-NO-VERDICT (tooling only):** one read-only artifact loop used
  zsh's special lowercase variable `path`, temporarily shadowing `PATH`; its
  `git show` commands did not execute and produced no data. The loop was rerun
  with a neutral variable and completed. No mathematical result depends on it.

## Recommended next angle

Continue the same primary target from CP's exact surviving shape: choose an
inclusion-maximal cycle carrier `A_s`. Both forced ends of `s` have
`U`-degree at most one, but there may be only one maximal carrier and neither
end need have `U`-degree zero. The next subclaim should therefore combine these
two residual capacity holes with the augmented forest quotient of `B_s` at an
external neighbour, allowing nested nonmaximal carriers. It must be tested
against `ADJ-WITNESS.json`, O-56/O-63/O-64, and the prior mixed-violation
population before use. Do not require adjacent maxima or reintroduce a
universal `P`, `B_s`, or `T_F` localization.

## Jobs and local propagation

No jobs remain running. The gauntlet, preregistration, frozen checker, raw
output, proof, witness, controls, and this report are committed only to the
attempt branch. Per the operator's binding instruction, nothing was pushed,
no PR or lessons branch was opened, and no public action was attempted. The
operator must relay or merge the lessons below after controller audit.

## LESSONS FOR FUTURE ATTEMPTS
- [MATHEMATICALLY PROVED] Carrier-poset lemma CP: for cycle vertices `s!=t`, `t in B_s` implies `A_t proper-subset A_s`; the carrier-containment digraph is acyclic and `P\U` is exactly the nonempty set of inclusion-maximal cycle carriers. Full proof and evidence are in `LEMMA-A-CARRIER-POSET.md` on `attempt/2026-08-05-codex-gpt-5-b17e`.
- [MATHEMATICALLY PROVED] Combining CP with Lemma CS(a), every forced-core cycle has at least one cycle vertex outside `U` whose two forced ends each satisfy `deg_U(q)<=1`; this removes the need to assume the known-false global condition `P intersect U=empty`.
- [COMPUTATIONALLY VERIFIED] Frozen prospective scan `carrier_poset.py` sha256 `7fe9f985...` over 115,774 abstract systems found 798 cyclic forced-core systems and 0 CP failures; anchors 115,774/798 and the 18 `P intersect U!=empty` controls matched exactly, with O-56/O-63/O-64 positive controls passing.
- [FALSIFIED] ADJ, the claim that two inclusion-maximal cycle carriers must be consecutive, fails on all 18 overlap systems; first certificate `work/b17e/ADJ-WITNESS.json` has `A_s2=S`, `A_s0={s0}`, `A_s1={s1}`, hence `P\U={s2}` on a uniquely forced 6-cycle. Independent `wcheck.py` confirms it.
- [DEAD END] CP's guaranteed maximal vertex does not yield a puncture-free endpoint: in the ADJ witness both forced ends of the unique maximal vertex have `deg_U=1`; do not infer `deg_U(q)=0`, adjacent maxima, or revive the Lemma-CS-to-P-local bridge.
- [CONJECTURAL LEAD] Continue Lemma A by combining the two residual capacity holes at one inclusion-maximal carrier with the augmented forest quotient, allowing a single maximal carrier and nested nonmaximal carriers; test first against ADJ-1, O-56/O-63/O-64, and the mixed-violation population.
- [TOOLING] O-63's JSON phrase “first inclusion-minimal violation” is correct only within `B_s`; a complete subset scan finds global size-two violations such as `{a,s}` while every proper subset of `B_s={u,a,b}` remains tight, so the witness's degree/private-cycle falsifications are unchanged.
