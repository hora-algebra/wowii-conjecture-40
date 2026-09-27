# HARD-ONE-CYCLE: durable OTR SCOUT handoff

Prepared 2026-09-27 from the Issue #10 discussion, Claude's evidence v2, ChatGPT's independent audit and the subsequent reconciliation.

**Ready as input to a fresh pre-GO SCOUT. Not a GO authorization, a launched campaign, or a certified mathematical result.** This packet supersedes the original dossier's n=13 holdout plan and optimistic evidence interpretation. It does not modify the historical source branches or the OTR framework.

## Start here

Give the fresh OTR pre-GO Controller the Scout issue URL and the immutable packet commit linked there. The Controller should read `SCOUT-SEED.md`, then `BASELINE-AND-ERRATA.md`, `THEOREM-A.md` and `PROVENANCE.md`. The issue and seed contain the startup instructions; the operator does not need to pass a separate Markdown attachment or reconstruct the chat.

The fixed target is HOC: every hard state has exactly one selected cycle, in the connected bipartite/minimum-FVS incidence model. This is not a campaign to settle Conjecture 40 or choose another subproblem.

Theorem A supplies a proof that hard states have at least two S-vertices on path components. Its status is **claimed, with complete proof and non-blind concurring reviews; formal campaign verification remains owed**. Its corollaries explain the small-order data through n=13. The unresolved multi-cycle region starts at n=14.

## Readable files and full evidence

| File | Purpose |
|---|---|
| `SCOUT-SEED.md` | Actual fixed-target pre-GO instructions, inherited input, resource constraints and startup gates |
| `BASELINE-AND-ERRATA.md` | Exact definitions, current mathematical baseline, corrected evidence interpretation and known source errors |
| `THEOREM-A.md` | Complete standalone proof; one disclosed editorial correction to the v2 original |
| `PROVENANCE.md` | Pinned August sources, archive/source hashes, review lineage, claim scope and sizing exposure |
| `extract_evidence.py` | Standard-library-only verifier/extractor; executes no research code |
| `evidence/inherited.tar.xz.part01` through `part07` | Exact archived contents of both evidence bundles, split for transport |

The seven parts concatenate in numeric order to a 52,012-byte xz-compressed tar, SHA-256:

`6253fc7c035978b39834344c19eeb76726180dc13062b9f393a6ea9c5bea0689`

It contains **52 unchanged source files, 551,080 decoded bytes**: all 45 files from Claude's v2 bundle and all seven files from ChatGPT's independent audit. The current source manifests contain 44 and six checksums respectively; the two manifests do not checksum themselves.

After obtaining this pinned repository snapshot, extract to a new directory **outside campaign worktrees**:

```sh
python3 research/hoc-scout-2026-09-27/extract_evidence.py --output /absolute/new/hoc-inherited
```

The extractor verifies the complete archive and all 50 source checksum entries before publishing the output directory. It refuses an existing output directory. It does not compile or execute the research engines. Python with standard-library lzma support is required; the research replays have their own dependencies documented in the original bundles.

The extracted roots are `hoc-review-evidence/` (C engine, analysis script, all supplied results/certificates, referee implementations and logs, RUN.md and original theorem) and `hoc-independent-audit/` (independent Python verifier, replay JSON, graph lists and audit report).

## Admission and readiness

Storage in this source repository is not admission to a future campaign. Before GO, use the destination OTR version's supported source/evidence intake and explicit human transactions where required, retaining exact bytes, hashes, source lineage, role visibility and non-blind exposure. A URL, a checksum or model agreement alone grants neither admission nor proof status.

The current launch route, actual laptop calibration, exact campaign budget and handling of the disclosed n=14 sizing shard must be settled before GO. They do not prevent SCOUT from starting. No n=14 target search was run while assembling this handoff, and no OTR launcher change was made.
