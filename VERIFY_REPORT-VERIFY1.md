# VERIFY-1

| # | Claim | Verdict | Independent result |
|---:|---|---|---|
| 1 | Frozen `verification/phase0.c` integrity and controls | CONFIRMED | `SHA256SUMS.txt`: 237 OK, 0 bad; source SHA-256 `17db663be9cd4d1e9adb1524b2717fb90c379fc53ba56066a5d3bcf275c8dac6`; `GOLD ALL PASS`; `GOLD2 (SV) ALL PASS`. |
| 2 | SV witness `J???FAWdVD?` | CONFIRMED | Decoded edges equal the printed 15-edge list; `f=9 b=10 p=3 o=1`; eligible set `{0}`; `p(G-0)=2`. |
| 3 | SV witness `J???FBObs\?` | CONFIRMED | Decoded edges equal the printed 16-edge list; `f=9 b=10 p=3 o=1`; eligible set `{0}`; `p(G-0)=2`. |
| 4 | SV witness `J???FAWdUD_` | CONFIRMED | Decoded edges equal the printed 15-edge list; `f=9 b=10 p=3 o=1`; eligible set `{0}`; `p(G-0)=2`. |
| 5 | Frozen `phase0 run2` on the three SV witnesses | CONFIRMED | 3 graphs, 3 violations, 0 bug flags; each has `oG=1 pG=3 elig=1 minGain=-1`. |
| 6 | Frozen `phase0 run2` on `geng -c 11 3/1024` | CONFIRMED | 363,207 connected nonbipartite graphs, 19 violations, 0 bug flags. |
| 7 | SV minimality through `n=9` | CONFIRMED | 272,209 connected nonbipartite graphs, 0 SV failures. |
| 8 | SV minimality at `n=10` | CONFIRMED | 11,716,571 connected graphs; 4,032 bipartite; 11,712,539 nonbipartite; 0 SV failures. |
| 9 | Connected-bipartite anchor at `n=11` | CONFIRMED | Independent `geng -c -b`: 25,598. |
| 10 | Connected-bipartite anchor at `n=12` | CONFIRMED | Independent `geng -c -b`: 212,780. |
| 11 | Connected-bipartite anchor at `n=13` | CONFIRMED | Independent `geng -c -b`: 2,241,730. |
| 12 | Connected-bipartite anchor at `n=14` | CONFIRMED | Independent `geng -c -b`: 31,193,324. |
| 13 | Lemma A positive controls O-56 / O-63 / O-64 | CONFIRMED | Independent enumeration-intersection engine: feasible-selection counts `1 / 6 / 1`; cyclic forced core on all three. |
| 14 | Lemma A at `n=11` | CONFIRMED | 25,598 graphs; 994,607 nontrivial `(G,S,e)` instances; 0 cyclic forced cores; 0 infeasible. |
| 15 | Lemma A at `n=12` | CONFIRMED | 212,780 graphs; 10,970,519 instances; 0 cyclic forced cores; 0 infeasible. |
| 16 | Lemma A at `n=13` | CONFIRMED | 2,241,730 graphs; 141,887,501 instances; 0 cyclic forced cores; 0 infeasible. |
| 17 | Lemma A at `n=14` | CONFIRMED | Four full residue shards sum to 31,193,324 graphs and 2,391,365,507 instances; 0 cyclic forced cores; 0 infeasible. |
| 18 | Lemma A census described as every minimum FVS and every `H`-edge | DISCREPANCY | The reported counts exclude `tau<2`; at `n=8` the reported census is 2,186, while literal enumeration of every minimum FVS and every `H`-edge is 3,770. See note 1. |
| 19 | Lemma A maximum forced-path lengths `8 / 10 / 10 / 12` at `n=11..14` | NOT CHECKED | The independent engine was scoped to the mandated cyclic-core verdict and safely stopped once a running selection intersection became acyclic. |
| 20 | `work/f2.c` frozen source identity | CONFIRMED | SHA-256 `e528a4ae58ece0489c50a11e6f4a3ff229e3a24383ec856d3a0877994549b458`, matching `work/F2-SHA256.txt`. |
| 21 | F2 positive controls O-56 / O-63 / O-64 | CONFIRMED | Independent direct search finds no acyclic feasible selection on any control. |
| 22 | F2-ALL and F2-SOME through `n=12` | CONFIRMED | Instance totals at `n=8..12`: `2,186 / 13,003 / 116,216 / 994,607 / 10,970,519`; 0 F2-ALL failures and 0 F2-SOME failures at every order. |
| 23 | F2-ALL and F2-SOME at `n=13` | CONFIRMED | Four full residue shards sum to 2,241,730 graphs and 141,887,501 instances; 0 F2-ALL failures; 0 F2-SOME failures. |
| 24 | F2 computational census described as every minimum FVS and every fixed edge | DISCREPANCY | `work/f2.c` also skips `tau<2`; its `n=8` reported instance count is 2,186 rather than the literal 3,770. See note 1. |
| 25 | `work/lift.c` frozen source identity | CONFIRMED | SHA-256 `c0cc2dd315144a0c9c64c875234e193fd8f700e01949ea6668964220a4d01c5e`, matching `work/LIFT-SHA256.txt`. |
| 26 | LIFT-A and LIFT-A-ALL through `n=9` | CONFIRMED | Full `n=3..9`: 273,191 connected graphs, 272,209 nonbipartite, 0 LIFT-A failures, 0 LIFT-A-ALL failures. |
| 27 | LIFT-A-tight census at `n=9` | CONFIRMED | 2,494 best-slack-zero graphs; saved graph6 list has 2,494 records and SHA-256 `6078480935bf84787a02b5ee580eb13e039583419929013916379f97c3cd5abc`. |
| 28 | Every-1000th connected graph sample at `n=10` | CONFIRMED | 11,716 sampled connected graphs, 11,713 nonbipartite; 0 LIFT-A failures; 0 LIFT-A-ALL failures; 42 best-slack-zero. |
| 29 | All 52,303 claimed LIFT-A-tight graphs at `n=10` | NOT CHECKED | Their graph6 list is not on the branch; the required fallback full tight census through `n=9` was completed instead. |
| 30 | Full-universe LIFT-A / LIFT-A-ALL claim at `n=10` | NOT CHECKED | VERIFY-1 prescribed an every-1000th sample at `n=10`, not a new full census, when the 52,303-record list was absent. |
| 31 | LIFT-A / LIFT-A-ALL on the three SV witnesses | CONFIRMED | Each has `ell=8`, one minimum OCT, and best and worst LIFT-A slack 4. |
| 32 | L1 proof | CONFIRMED | Blind componentwise bipartition derivation matches the branch proof; isolated components and ceiling aggregation are valid; no gap. |
| 33 | L2 proof | CONFIRMED | Blind derivation gives `ell(G)>=|B|+|T|-2c_e+1>=2tau(B)+|T|+1`; algebra matches the branch proof; no gap. |
| 34 | Lemma CS proof | CONFIRMED | Blind tight-set-saturation derivation proves (a)--(d); branch submodular-telescoping derivation is independently valid; no gap. |
| 35 | O-56 JSON `forced_core_edges` | DISCREPANCY | JSON prints 10 forced edges; independent intersection and `work/wcheck.py` give 8. See note 2. |
| 36 | SV paper-definition citation in `SV-FALSIFIED.md` | DISCREPANCY | The file calls SV “paper Definition 5.3”; `paper/paper.pdf` labels SV Definition 5.4. See note 3. |

## Discrepancy notes

1. `tools/forced_core.py`, `work/fcore.c`, and `work/f2.c` skip `tau<2`, but the surrounding prose says “every minimum FVS, every edge.” The published instance counts are exact for the `tau>=2` nontrivial census. The omitted layer cannot contain a forced-core cycle because its `S`-side has fewer than two vertices.
2. `tools/witnesses/O-56.json` lists `(0,6)` and `(1,6)` as forced, but its own unique feasible selection omits both; the actual forced core is `{(0,4),(0,5),(1,4),(1,5),(2,6),(2,7),(3,6),(3,8)}` and still has cycle rank 1.
3. The numbering discrepancy is bibliographic only; the SV predicate printed in `SV-FALSIFIED.md` matches Definition 5.4's substance.
