# Run notes — attempt 9d2b

## Protocol and budget

- Attempt branch: `attempt/2026-08-05-codex-gpt-5-9d2b`.
- Base: public `main` at `64eb3dacd3e332b9464faece8bd42f72e16bf6dc`.
- Operative protocol: checked-in `ATTACK.md` v4 from that base.
- Soft budget restarted at `2026-08-05T11:39:54-05:00`: 180 minutes, soft
  deadline `2026-08-05T14:39:54-05:00`, with the v4 15-minute wrap rule.
- Publication constraint: local commits only; no push, PR, tag, release, or
  public post.

## Withdrawn setup interpretation

- **WITHDRAWN:** the pre-resume working interpretation “public/local main has
  v3, so use v3 plus the activation message as a narrow v4 delta.” Public v4
  was fetched before this branch was created, and every protocol step was
  restarted from the actual v4. No mathematical work or preregistration was
  performed under the withdrawn interpretation.

## Step 0 snapshot

- GitHub: no open issues or pull requests; public `main` resolved to `64eb3da`.
- MathOverflow question 513887: zero answers, zero comments, not closed.
- Maintained WOWII page: entry 40 still has status `O`.
- Web/arXiv search: no resolving work on Conjecture 40, Lemma A, or
  SAFE-EXISTS found; the formal-conjectures statement remains a statement, not
  a proof.

## Step 0.5 snapshot

- Public `attempts/LESSONS.md` was read through the maintenance-reconciliation
  entry requiring post-push existence proofs.
- Complete public reports read: `5047`, `a7c3`, `0eb8`, `4d7a`, and `b17e`.
- Binding SAFE-EXISTS facts carried forward: SD-SHORT and SD-COUNT-SHORT are
  FALSIFIED; scheduling solely by cycle choice is a DEAD END; SD-PLUS-2 and
  SD-2STEP-DESCENT are computational evidence with their reported scopes; the
  n=12 universal B-PLUS-2 grade and the precise existential SAFE-EXISTS proof
  obligation remain to be audited before a new claim is chosen.
- Provenance correction: VERIFY-2 independently confirms the n<=11
  scheduled-descent anchors but labels n=12 `NOT CHECKED`; the prospective
  exhaustive n=12 survival is recorded by 4d7a.

## Primary continuation

- Preregistered SAFE-2-EXISTS, the post-hoc SUCCESSOR-ONE mechanism audit, and
  the universal per-cycle B-TERMINAL-SLIDE/B-PLUS-2 continuation in
  `PREREG-SAFE-EXISTS.md`.
- The universal B-PLUS-2 verdict will be inferred only from explicit
  terminal-slide certificates for every A1-bad cycle. A terminal-slide failure
  leaves B-PLUS-2 unresolved until a generic bounded-path recheck.

## Execution outcome

- Full n=11 gold test reproduced 25,598 graphs, 8,202,633 cycle components,
  six A1 failures and 20 bad minimizing paths; all new predicates passed and
  there were no caps.
- The repaired n=12 replay validated all 170 retained `(2,1)` records. All 170
  fail terminal-slide; 142 fail unrestricted successor-one; all 170 pass
  SD-2STEP-DESCENT. The first witness was confirmed with VERIFY-2's independent
  engine.
- Generic bounded-path replay found `d0=3`, `dCES=5` for all 170. Exact tail
  scans from the two certificate-cap boundary graphs covered 26 and 44 A1-bad
  cycles, all B-PLUS-2-good. Replay/tail union covers all 196 universal-gap
  cycles after accounting for 12 and 32 overlaps.
- HARD-SUCCESSOR-ONE passed on all 1,140 retained `(1,0)` hard states and all
  3,924 minimizing first paths; 44 capped-away source records remain ungraded
  for this post-hoc strengthening.
- Two initially launched full multi-cycle n=12 shard jobs and their two generic
  replacements were stopped without output when shared-CPU timing made them
  redundant. They are `ABORTED-NO-VERDICT`; exact cap-tail scans replaced them.
- Two pre-data validator failures are retained as `*-v1-invalid.json` and
  excluded from every verdict. Repairs changed only edge-orientation/profile
  validation and were re-hashed and committed before rerun.
