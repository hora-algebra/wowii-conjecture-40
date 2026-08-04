# Independent blind-result ledger

This ledger records independent results before repository implementation code
is opened. Times are UTC.

| Time | Claim | Independent result | Checker SHA-256 |
|---|---|---|---|
| 2026-08-03T22:42:34Z | SV witness `J???FAWdVD?` | decoded edges equal printed edges; `f=9 b=10 p=3 o=1 eligible=[(0,2)]` | `a13d99eb76c09467a95bb76450a2e6540a02b10cfcd6b0af4ca6bd89450a9c85` |
| 2026-08-03T22:42:34Z | SV witness `J???FBObs\?` | decoded edges equal printed edges; `f=9 b=10 p=3 o=1 eligible=[(0,2)]` | `a13d99eb76c09467a95bb76450a2e6540a02b10cfcd6b0af4ca6bd89450a9c85` |
| 2026-08-03T22:42:34Z | SV witness `J???FAWdUD_` | decoded edges equal printed edges; `f=9 b=10 p=3 o=1 eligible=[(0,2)]` | `a13d99eb76c09467a95bb76450a2e6540a02b10cfcd6b0af4ca6bd89450a9c85` |

## Post-blind repository-engine cross-checks

| Claim | Result |
|---|---|
| `verification/SHA256SUMS.txt` | 237 OK, 0 bad; `phase0.c` SHA-256 `17db663be9cd4d1e9adb1524b2717fb90c379fc53ba56066a5d3bcf275c8dac6` |
| Frozen `phase0` gold controls | `GOLD ALL PASS`; `GOLD2 (SV) ALL PASS` |
| Frozen `phase0 run2`, three witnesses | 3 graphs, 3 violations, 0 bug flags; each has `oG=1 pG=3 elig=1 minGain=-1` |
| Frozen `phase0 run2`, `geng -cq 11 3/1024` | 363,207 connected nonbipartite graphs, 19 violations, 0 bug flags; violation-file SHA-256 `a8a523f9ea445052ec0c7ac75fc90685d435685a6a6275203e5d3dcab0cbee1e` |

## Independent SV minimality sweep

Independent C source SHA-256: `db587fa016101e3620a26644ef3daa2d91d8003793008052c578e478c086cf5b`.

| Order | Connected graphs | Connected bipartite | Connected nonbipartite | SV failures |
|---:|---:|---:|---:|---:|
| 3 | 2 | 1 | 1 | 0 |
| 4 | 6 | 3 | 3 | 0 |
| 5 | 21 | 5 | 16 | 0 |
| 6 | 112 | 17 | 95 | 0 |
| 7 | 853 | 44 | 809 | 0 |
| 8 | 11,117 | 182 | 10,935 | 0 |
| 9 | 261,080 | 730 | 260,350 | 0 |
| 3--9 total | 273,191 | 982 | 272,209 | 0 |
| 10 | 11,716,571 | 4,032 | 11,712,539 | 0 |

## Independent connected-bipartite enumeration anchors

| Order | `geng -c -b` count | Expected | Result |
|---:|---:|---:|---|
| 11 | 25,598 | 25,598 | match |
| 12 | 212,780 | 212,780 | match |
| 13 | 2,241,730 | 2,241,730 | match |
| 14 | 31,193,324 | 31,193,324 | match |

## Independent Lemma A forced-core run

Enumeration-intersection source SHA-256 before repository-code inspection:
`0e07ecaf9499bebde0e8933110251a0fb2a7a47e31c0ba83f54bcbb2fb1537a9`.

| Check | Independent result | Branch expectation | Result |
|---|---|---|---|
| Positive control O-56 | 1 feasible selection; cyclic core | cyclic core | match |
| Positive control O-63 | 6 feasible selections; cyclic core | cyclic core | match |
| Positive control O-64 | 1 feasible selection; cyclic core | cyclic core | match |
| Protocol check at n=8 | 182 graphs; 786 minimum FVSs; 3,770 `(G,S,e)` instances; 0 cyclic; 0 infeasible | 2,186 instances; 0 cyclic | instance-count mismatch pending diagnosis |

Post-blind diagnosis: the branch census excludes `tau < 2`, whose forced core
cannot contain a cycle.  With that stated convention, the independent n=8
count is 2,186 and matches.  Final source SHA-256 after adding only this census
filter and reducing progress verbosity:
`25ce6906a24452d2959314f1ef3c3425259fe3bd76f64207c02cbe97404dd5ed`.

| Order | Connected bipartite graphs | Minimum FVSs (`tau >= 2`) | `(G,S,e)` instances | Cyclic cores | Infeasible |
|---:|---:|---:|---:|---:|---:|
| 11 | 25,598 | 152,508 | 994,607 | 0 | 0 |
| 12 | 212,780 | 1,542,523 | 10,970,519 | 0 | 0 |
| 13 | 2,241,730 | 18,504,983 | 141,887,501 | 0 | 0 |
| 14 | 31,193,324 | 293,111,483 | 2,391,365,507 | 0 | 0 |

## Independent F2 / F2-ALL run

Direct acyclic-selection search source SHA-256 before opening `work/f2.c`:
`fd55562bb3dbbe6531f8da8171ea2a1d9c820f0d1a047719d67cb2d5c63c4171`.
All three warning-instance positive controls report no acyclic feasible
selection.

| Order | Instances | F2-ALL failures | F2-SOME failures |
|---:|---:|---:|---:|
| 8 | 2,186 | 0 | 0 |
| 9 | 13,003 | 0 | 0 |
| 10 | 116,216 | 0 | 0 |
| 11 | 994,607 | 0 | 0 |
| 12 | 10,970,519 | 0 | 0 |
| 13 | 141,887,501 | 0 | 0 |

## Independent LIFT-A / LIFT-A-ALL run

Definition-based source SHA-256 after adding a result-inspection mode:
`af5e7cbf5b886357fba68f1ecca01ef22caf925c8b0fe6f75f2295495bdc95cd`.

| Order / universe | Connected graphs | Nonbipartite | LIFT-A failures | LIFT-A-ALL failures | Best-slack 0 |
|---|---:|---:|---:|---:|---:|
| 3 full | 2 | 1 | 0 | 0 | 1 |
| 4 full | 6 | 3 | 0 | 0 | 1 |
| 5 full | 21 | 16 | 0 | 0 | 3 |
| 6 full | 112 | 95 | 0 | 0 | 6 |
| 7 full | 853 | 809 | 0 | 0 | 23 |
| 8 full | 11,117 | 10,935 | 0 | 0 | 183 |
| 9 full | 261,080 | 260,350 | 0 | 0 | 2,494 |
| 10, graph numbers divisible by 1,000 | 11,716 | 11,713 | 0 | 0 | 42 |

The branch does not contain the 52,303 LIFT-A-tight n=10 graph6 list, so the
specified fallback was used.  The fresh n=9 tight list has 2,494 records and
SHA-256 `6078480935bf84787a02b5ee580eb13e039583419929013916379f97c3cd5abc`.
Each of the three SV witnesses has `ell=8`, one minimum OCT, and both best and
worst LIFT-A slack 4.
