# RUNLOG — attempt/2026-08-05-claude-opus-5-0520 (append-only)

Model/harness: Claude Opus 5 (1M context) / Claude Code CLI, macOS arm64 (Darwin 24.6.0), Python 3.9.6.
Date: 2026-08-05.
Base: `public/main` at `64eb3da` ("Merge pull request #5 from cozuya/lessons/tooling-post-push-proof"),
which carries **ATTACK.md v4** and the populated, binding `attempts/LESSONS.md`.
Protocol followed: ATTACK.md **v4** (read from `public/main`, 164 lines).

**Soft time budget declared at start of run: 4 hours of wall-clock agent time,
starting 2026-08-05.** Unanchored estimate (no measured rate for this harness in
this project yet); treat as a soft stop, not a schedule.

**Publication status: LOCAL ONLY.** Operator instruction: commit locally, push
nothing. Push URLs for both `origin` and `public` have been set to
`DISABLED-NO-PUSH-PER-OPERATOR` in this clone as a mechanical safeguard.

## Provenance correction (recorded per operator instruction)

An earlier stance in this run treated the local `origin` copies of ATTACK.md as
current. That stance is **WITHDRAWN**. The local mirror
`<local-mirror>` and every local working checkout carry
ATTACK.md **v3** or older; the operative protocol is **v4** on `public/main`.
`origin/main` is a strict ancestor of `public/main` (3 commits behind:
`77661ae`, `446badb`, `9b01be1`). The corresponding upstream lesson is recorded
at `attempts/LESSONS.md` line 79-81 ("maintenance completion claims require
post-push existence proofs"), and it is present in the base of this branch.

## Step 0 — freshness check (2026-08-05, live network)

| source | method | finding |
|---|---|---|
| GitHub issues | `gh issue list --repo cozuya/wowii-conjecture-40 --state all` | none (empty list) |
| GitHub PRs | `gh pr list --repo cozuya/wowii-conjecture-40 --state all` | 5 PRs, **all MERGED**, none open; #5 `lessons/tooling-post-push-proof` merged 2026-08-05T16:34:58Z is the tip of `public/main` |
| MathOverflow 513887 | StackExchange API v2.3 (`api.stackexchange.com`) | title "Can the forced edges of an exact-demand capacitated selection in a bipartite incidence model form a cycle, given hereditary FVS tightness?"; `answer_count=0`, `is_answered=false`, `score=0`, `view_count=17`, `creation_date=2026-08-03T19:18:25Z`, `last_activity_date=2026-08-03T19:18:25Z` — i.e. **no answer, no comment, no edit since posting** |
| WOWII open list | plain-HTTP fetch of `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/open.html` (the `cms.uhd.edu` host in ATTACK.md refuses HTTPS; `cms.dt.uh.edu` is the live host) | entry still listed as **`O 40.`** on the OPEN list: "If G is a simple connected graph on more than one vertex, then f(G) >= CEIL[(p(G)+b(G)+1)/2]", dated Mar 05, 2004, carrying only the Mar 6 2004 DeLaViña path-cover-one annotation. **No status change.** |
| web / arXiv | WebSearch ×2; arXiv API ×3 (`"forest number"+"path cover"`, `"Graffiti.pc"`, `"bipartite number"+"forest number"`) | no new work on Conjecture 40 or on Lemmas A/B. Recent Graffiti.pc activity exists but on other conjectures (141/142/143 arXiv 2608.01396, 387, 2) and on the DeLaViña–Waller conjecture (2605.24855) — none touch Conjecture 40. |

**Verdict: nothing resolved by others. Run objective unchanged.**

## Step 4 oracle check (done before any new mathematics)

`shasum -a 256 -c tools/SHA256SUMS.txt` run from `tools/`: **17/17 OK**
(a1_verify.py, b_hslide.py, b4_check.py, b4_split.py, eval_frozen.py,
eval_L1_holdout.py, experiment_b_dual.py, experiment_b.py, forced_core.py,
inv_b.py, inv40_a.py, inv40_b.py, mine_n10.py, README.md, witnesses/O-56.json,
witnesses/O-63.json, witnesses/O-64.json).

## Step 1 — gauntlet: COMPLETED (GAUNTLET.md rewritten on this branch)

Engine anchored before use: `ANCHOR systems=115774 cyclic=798 pdis=18` (exact
match to `carrier.py` and b17e). Witnesses re-derived independently: feasible
selection counts 1 / 6 / 1, forced cycles, carrier tables, violation structure.
Two metadata scope defects recorded (O-63 minimality scope; O-56 `refutes` field).

## Step 3 target 1 — results (append-only)

* PREREG-NC.md frozen at commit `2510e2b` BEFORE any scan, with the NC proof
  written out in it.
* Gold test: O-56 / O-63 / O-64 / ADJ-1 all PASS; ADJ-1 fires all three negative
  controls (NC-ALL, CHORD-ALL, PDIS).
* Targets: exhaustive 3 5 → 798 cyclic, 0 failures, controls 18/18/18, 43.3 s;
  random 20000 seed 1 → 656 cyclic, 0 failures, controls 332/332/332, 10.4 s;
  random 400000 seed 777 → 13,245 cyclic, 0 failures, controls 6727/6695/6727,
  200.4 s. Total 14,699 cyclic systems, 0 failures.
* Post-run hash check of all four frozen artefacts: unchanged.
* NC, CE, A-I+ graded MATHEMATICALLY PROVED + COMPUTATIONALLY VERIFIED.
* CAP2-BS: exploratory only (sizing runs preceded preregistration); scan graded
  ABORTED-NO-VERDICT because its negative control cannot fire inside the
  universe. CAP2-BS itself stays CONJECTURAL; PROOFS.md's parked status unchanged.

## TOOLING discrepancy (reported, not absorbed)

`LEMMA-A-CARRIER.md` §1.3 random rows do not reproduce from `work/carrier.py`
at its preregistered hash `d11b0bca...`. Rerun: `random 20000 1` → 656 / PDIS
332 / DEG2 157 (published 547 / 251 / 142); `random 400000 777` → 13,245 / 6,727
/ 3,271 (published 11,097 / 4,931 / 2,643). `engine0520` agrees with the frozen
tool system-by-system (symmetric difference 0 on the 20,000-system population).
The `exhaustive 3 5` row reproduces exactly, so CP's evidence is unaffected.

## Wrap-up

No jobs left running. Nothing pushed; push URLs disabled in this clone.
