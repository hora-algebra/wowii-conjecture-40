# Provenance and source inventory

## New packet versus original evidence

This handoff was assembled in ChatGPT on 2026-09-27 at the operator's request to make the HOC preparation durable for a future OTR SCOUT. It is a source-repository packet, not output of an activated OTR campaign. There is no prior formal OTR invocation UUID for this conversation, and none should be invented during admission.

The two original evidence sets remain distinct under their original directory names. All file bytes inside them are unchanged. The readable `THEOREM-A.md` outside the archive has one disclosed editorial change; the original is retained inside. `BASELINE-AND-ERRATA.md` consolidates the review exchange and explicitly supersedes mistaken historical wording. It is a later reconciliation, not an independently generated theorem proof.

Original uploaded ZIP identities:

| Origin | Original ZIP SHA-256 |
|---|---|
| Claude evidence v2, `hoc-review-evidence-v2.zip` | `2e0182d627c510c4163a188aa3be98bd6988dd0d23107b61e97a7c13b5a50ab4` |
| ChatGPT independent audit, `hoc-independent-audit.zip` | `80255988f3a3f4d5ea42953098a3000b06b42277f6362d1f854265fffaf770a9` |
| Earlier Claude v1, for lineage only | `14eb53e676e57c4a8019955b9c0567883875b0a9de42c345ce51522edc57d988` |

The new tar archive preserves the ZIPs' extracted files, not the original ZIP container bytes. Its SHA-256 is `6253fc7c035978b39834344c19eeb76726180dc13062b9f393a6ea9c5bea0689`, 52,012 bytes; concatenate the seven parts in numeric order. Its 52 regular files contain 551,080 decoded bytes. Both current source manifests (44+6 entries) were verified during packaging. The extractor repeats those checks without executing research code.

Critical original file hashes:

- Claude `engine/hoc.c`: `16cecf8cd5cf9d40b899350dfbd609049b79fea82f39e5ac020db416fb492984`.
- ChatGPT `verify_certificates.py`: `dee86d22e44f2f952b3eb51e07358e2d223c41fb1af8c26e6dbc6b03e4e7e31d`.
- Original v2 `THEOREM-A.md`: `7d3367da0c2cf6d2adfb969e1991fa0317a68f0d7a64cdef6bcdc30c2aa8e1e6`.

## Actual archived material

`hoc-review-evidence/` contains `RUN.md`, the original theorem, current and historical manifests, `engine/hoc.c`, `engine/analyze.py`, all supplied `results/` files (n=11/12 certificates, n=12 census/slack-pair JSON and n=13 HOC summaries), and the complete supplied `referee/` directory with Python/C++ implementations, variants and logs. This is every file supplied in v2, not a selection of favorable outputs.

`hoc-independent-audit/` contains `INDEPENDENT-AUDIT.md`, `verify_certificates.py`, `independent-replay.json`, `replay-n12.json`, the three-graph n=11 and 317-graph n=12 graph6 lists, and its checksum manifest.

The original RUN.md statement that nothing was pushed described its creation time. These exact files are now published as historical source material. Similarly, source verification statements are attributed reports of prior runs, not claims that every run was repeated while packaging.

## Review lineage and limits

1. The initial Issue #10 proposed HOC using the August finite census and planned an n=13 holdout.
2. Claude's adversarial review derived Theorem A, wrote a fresh C engine, ran n<=13 checks and obtained a separate non-blind Claude referee derivation with independent Python/C++ implementations. The n=14 shard was used only for the disclosed sizing quantities.
3. ChatGPT read that work, re-derived the proof along the same lemma structure and wrote a separate Python certificate verifier. This is cross-vendor concurrence but non-blind, not independent discovery or protocol certification. It replayed 2,216 retained rows, not the complete all-graph census, and reran Claude's C engine on the supplied 317 n=12 graphs.
4. The operator supplied the independent audit back to Claude. Claude reported exact checksum/input identity, verifier/code inspection, matching replays and mutation checks, and supplied the C1-C8 corrections plus the standalone v2 proof.
5. ChatGPT accepted that baseline with the amendments recorded in `BASELINE-AND-ERRATA.md`. No additional n=14 target search or launcher implementation was part of reconciliation or publication.

The complete mathematical proof and executable evidence are retained. Conversational recommendations and the C1-C8 disposition are consolidated in the baseline rather than requiring a future model to read the whole relay transcript. No consensus vote changes the status to PROVED. OTR must record historical-answer exposure when using these materials.

## Pinned August primary sources

Repository: `cozuya/wowii-conjecture-40`. Paths below are relative to the indicated immutable commit. Resolve them using `https://github.com/cozuya/wowii-conjecture-40/blob/<commit>/<path>` or an equivalent exact-byte retrieval.

| Source | Immutable commit | Relevant paths |
|---|---|---|
| 064c | `4ca6378dc72d08ad9ca1af4ccef7145704de79cf` | `PROOFS-SAFE2-064c.md`, `PREREG-SAFE2-064c.md`, `ATTEMPT_REPORT.md`, `work/064c/s2e_scan11.py`, `work/064c/s2e_scan.py` |
| 4d7a | `5cb5bb9a29718562d4d25a6902fd693f0a4677f4` | `ATTEMPT_REPORT.md`, `PREREG-SD2.md`, `work/sd/sd_scan2.py` |
| 7851 | `3bfce15c8979157eb16103b8bcd1ab1761b88cd6` | `ATTEMPT_REPORT.md`, `PREREG-HARD-TAIL.md`, `work/7851/hard_tail.py` |
| VERIFY-3 | `57b297b01f07a783a685485fe286a98492f152f6` | verification record for the 44-record retention tail; locate the exact report in this snapshot when needed |
| Pre-handoff main | `290d1b28fd70038824fbba736e1bf47dd83aed01` | `attempts/LESSONS.md`, project definitions/paper and retained O-63 witness provenance |

Primary definition source: [064c §0 and structural results](https://github.com/cozuya/wowii-conjecture-40/blob/4ca6378dc72d08ad9ca1af4ccef7145704de79cf/PROOFS-SAFE2-064c.md). Apply this packet's errata; its misleading headings are not additional theorems.

Historical dossier: [Issue #10](https://github.com/cozuya/wowii-conjecture-40/issues/10). It is superseded as a startup instruction by the new Scout issue and this packet. Do not use its n=13 plan or old resource estimate.

## OTR mechanics: source review, not timeless promises

The timeout audit discussed OTR checkout `81f7a8b`, v3.0-rc1, especially `scripts/role-launch.mts` and its environment/tool/argv policy. It checked Claude-based formal actions, not the Codex route. Recheck against the destination campaign's pinned framework/toolchain before GO.

At handoff creation, the following current framework documents were also consulted:

- `scout/README.md` (blob `8ae2c8b5ea057d1ba9650f9ad9237d5bec6f495e`): explicit captured human input, fresh SCOUT reality check, critic/response/recommendation and human GO.
- `docs/carry-evidence-admission.md` (blob `25bbd28d84757d57a77d963cf38d21b971532693`): explicit pre-GO admission, source attestation, immutable recipient/exposure grants and real frozen delivery; no informal post-GO import.
- `sources/README.md` (blob `202bf772b1e69732016b2142d1f4270ec9156adf`): primary source access, append-only source history and legal evidence transport.

A source-repository commit is not proof certification, an already admitted carry package or authority to change sealed framework behavior. Use actual destination rules, report any schema mismatch honestly, and obtain required operator transactions before the one-way GO boundary.
