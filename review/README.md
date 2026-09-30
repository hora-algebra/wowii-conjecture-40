# Reproducing the checks

Run from the repository root with Python 3.10+ and nauty 2.8.9 geng on PATH:

```sh
(cd tools && shasum -a 256 -c SHA256SUMS.txt)
shasum -a 256 -c review/SHA256SUMS-review.txt
shasum -a 256 -c review/SHA256SUMS-general.txt
python3 review/replay_witnesses.py
python3 review/scan_small.py
python3 review/check_general.py
(cd tools && python3 a1_verify.py 7)
(cd tools && python3 forced_core.py 8)
```

Expected summaries are witness-results.json, small-results.jsonl and
general-results.json. Each finite universe and premise-firing count is included.
The direct intersection cross-check is limited to 1000 small-demand instances.
The scans are supplementary checks, not proofs, and share a forest predicate.
The witness replay instead calls the unchanged upstream selection oracle.
The general scan enumerates all labelled graphs through order six, not only
bipartite graphs; it tests the auxiliary forest-plus-independent-set lemmas.
No random sample is described as exhaustive.

Code in this review directory was generated with OpenAI Codex. No paid external
verification service was used. Proof files describe their own CC BY 4.0 scope.
The new Python files are provided under the MIT License in ../LICENSE; retain
its notice when redistributing the upstream code with them.
