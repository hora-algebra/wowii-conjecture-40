# MANIFEST — VERIFY-5 work package v5-0

Inventory of every file in this package, with its SHA-256. Nothing else is
included; there are no hidden files, and no version-control history beyond the
single commit that creates this tree.

## Package documents

| file | role |
|---|---|
| `STATEMENT.md` | the claim to be proved (Lemma A°), verbatim from paper §4, plus its definitional closure |
| `GIVEN-RESULTS.md` | NC, NCM, CE, A-I⁺ — verbatim statement blocks, certified, citable without re-derivation |
| `MANIFEST.md` | this file |
| `paper/paper.tex`, `paper/paper.pdf` | the paper, sealed `main` artifact, unmodified |
| `proofs/PROOFS.md` | the proof ledger for the surrounding results, sealed `main` artifact, unmodified |
| `LEMMA-A-CARRIER.md` | Lemma CS and the carrier machinery (branch 5047), unmodified |
| `LEMMA-A-CARRIER-POSET.md` | Lemma CP and the ADJ falsification (branch b17e), unmodified |
| `tools/` | the lemma-level verification oracle, sealed `main` artifacts; `tools/README.md` documents its own provenance |

## SHA-256 of every file

A file cannot list its own hash, so `MANIFEST.md` is excluded from the table
below; its hash is fixed by the git commit that seals this tree.

```
18f74b28d22f650cfe6bcea637e3a23f827e9d17edf2a5c1ab8d3f0f63ca5dd1  ./GIVEN-RESULTS.md
978fbbf43bc0d98711e741541bc828eb0acf99ade76e7a389c029ee8e57338db  ./LEMMA-A-CARRIER-POSET.md
4c06189879d866fb84188e95c63178ee43d0dba413f460518add83dbf016c7bd  ./LEMMA-A-CARRIER.md
afb83283db753295cde85ede7e5d2d0af153c7dfb3916b244b205e4be6bd84a8  ./paper/paper.pdf
7647dd7980dc08382466db56b21184c7024ced46460f78cf1bb670aeb0002edf  ./paper/paper.tex
5d0966dc82629b2f108cb18b4891287315ab97053f6b5a756a26f565a002687f  ./proofs/PROOFS.md
5d0051f22f2f45fe0952e713cc7a82de8dea391c846734829073b1e3a1c0e31e  ./STATEMENT.md
c91bf3ec1e13e5a23e5fef9508c2c185b9cccd77480114e2b1cd7e2cff1837ce  ./tools/a1_verify.py
06ab7034531f6893bc4a1d5cdb7e0f5a2a228ff160cf4f1a07c993d1ae8f15de  ./tools/b_hslide.py
f7962c74a64c060b7999474c91100bac77f18321291c352ebfa4ee7c4ab6309a  ./tools/b4_check.py
a1b44e0ef38b9ff0c3f75e9e43ec79ad8d0f05b91c35fba5a32835441d861c79  ./tools/b4_split.py
725afea2994efbb2f526f54ec8bbe3cc8bafb9c8ee4de3b795b7aa94886caf1f  ./tools/eval_frozen.py
ae3eda2639d46b1bb9189d1b7cdcf8564616149199f79759437db04beae07572  ./tools/eval_L1_holdout.py
e14d8a33612b99cd2d14a065e44a7baaf40397d5bb964fb8ea537c291b0e7ace  ./tools/experiment_b_dual.py
02cc6b4c54c16bf33e31bbd1d31bdb175ec5afbc0775b117e873e7097d22183b  ./tools/experiment_b.py
ba8b0ba56f96e4d2095dd5254093852b361185652e40402be5b5114434154547  ./tools/forced_core.py
0dc451402b7e5df7b5cd61e04481e856a86dfd91e4949db20201b47222ba6fe4  ./tools/inv_b.py
88430606e554d3a70bd4fe9bab2a30379a66c31a50d42c94c57980bfcead52af  ./tools/inv40_a.py
34a0b11c97f653590702209f7eeee85eb014be9ceb7f73c9ba4165bb66703c46  ./tools/inv40_b.py
bec35956aa7bd868ddf961d4fa6a7774a19ac9cbffe4185050fd89708d790308  ./tools/mine_n10.py
4dbd88fb43a254f04bdc8b5b9f74556680ebdce7893de910531967ae18c3ac5e  ./tools/README.md
6b8ed7f599d09c9f380879917c9a82757f870754e34c1b499b7750212a4431a6  ./tools/SHA256SUMS.txt
f918572a239b8e89c1ff9d5999b31f21474aaa36ebdc70fe34791213ddae127b  ./tools/witnesses/O-56.json
04a39f0f38adda999a95961e9ade3b7b95c2c5c466ffa36ea76f235e85525ec0  ./tools/witnesses/O-63.json
1ffe975de36b16b12b7cc10f85a46b62e26c363a661d19ade10debf7a3dcef29  ./tools/witnesses/O-64.json
```
