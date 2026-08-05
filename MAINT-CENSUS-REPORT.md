# Maintenance census report — maint/2026-08-census (LOCAL ONLY)

2026-08-05. Preregistration: PREREG-MAINT-CENSUS.md (engine
`work/census/maint_census.c`, SHA-256 `fd32245a…`, frozen and committed
before either run; validation record therein). All anchors passed; all
decision rules evaluated. Nothing from this branch is pushed.

## Run 1 — n = 10 L5/L6-condition census (COMPUTATIONALLY VERIFIED)

Universe: ALL 11,716,571 connected graphs on 10 vertices (8 `geng` shards;
shard sums exact), 11,712,539 nonbipartite. Wall time ≈ 6 min on 8 cores.

| check | result |
|---|---|
| connected / nonbipartite anchors | 11,716,571 / 11,712,539 — exact |
| S3 (exact LIFT-A) failures | **0** (consistency anchor, as required) |
| LIFT-A-tight graphs | **52,303**, set-identical to the published `verification/v2-lift-census/lift-a-tight-n10.g6` |
| **S1 (L5 condition) failures** | **7** |
| **S2 (L6 condition) failures** | **0** |
| L6-covers-but-L5-does-not | 7 (exactly the S1 witnesses) |

**The seven L5-condition failures at n = 10** (each re-verified by the
frozen Python `l6scan.py`, sha256 `2e568740…` — L5 margin −1, L6 margin +3,
exact slack 3 on every one):

```
I??CFFaFW  p=3 o=1  (2 min OCTs)   I??FFBaFw  p=3 o=1  (2 min OCTs)
I??CFFafW  p=3 o=1                 I??FF?^wo  p=3 o=1
I??EFFaFW  p=3 o=1                 I??FF?^ww  p=3 o=1
I??EFFaFw  p=3 o=1
```

Every failing minimum-OCT remainder has the profile
`tau=1, c_e=1, Delta=1, r=0, g=3` — threshold L5 = 2 < 3 = p, threshold
L6 = 6. Mechanism: the sparse pairs sit in the LARGER color class, which
the codex `r` (defined on smaller-or-tied classes only) cannot see, while
`g` (FE, maximized over both orientations) collects three of them.

**Consequences (per the frozen interpretation clause):**
- The minimal order of L5-condition failure is **10**, not 11; the seven
  graphs above supersede CX11 as minimal L5 witnesses.
- The L6 condition holds for EVERY connected nonbipartite graph with
  `n <= 10` (this run) and fails at `n = 11` (CX11, certified on the fable
  branch). **CX11 is exactly minimal for the L6 condition.**
- Exact LIFT-A remains clean through n = 10 with the tight set reproduced.

## Run 2 — excess-0 component enumeration, n = 11 and n = 12
(COMPUTATIONALLY VERIFIED)

Universe: ALL connected bipartite graphs; anchors exact
(25,598 at n = 11; 212,780 at n = 12 over 4 shards).

**n = 11 (2 graphs with excess <= 0, both = 0; first unbalanced members):**

```
J???FB_FW~?  a=5 b=6 p=3 g=1 excess=0
J???FB_Fw~?  a=5 b=6 p=3 g=1 excess=0
```

**n = 12 (16 graphs with excess <= 0: fourteen 0, one −1, one −2 — the
first NEGATIVE excess values known):**

```
K???Fbo{?^`}  6+6 p=2 g=1 e=0      K????B_w?xb}  5+7 p=4 g=1 e=0
K???E?xMULwu  6+6 p=2 g=1 e=0      K????B_w?|bm  5+7 p=4 g=1 e=0
K??CABo{?^`}  6+6 p=2 g=1 e=0      K????B_w?|b}  5+7 p=4 g=1 e=0
K???FB_FW~B{  6+6 p=2 g=1 e=0      K????B_w?~b}  5+7 p=4 g=1 e=0
K????B_FG|[J  6+6 p=4 g=2 e=0      K????BoBv_@{  6+6 p=4 g=2 e=0
K????B_Fg|[J  6+6 p=4 g=2 e=0      K????BoBv_@|  6+6 p=4 g=2 e=0
K???CBo{?^`}  6+6 p=3 g=1 e=-1     K????BoBo^]A  6+6 p=4 g=2 e=0
K????Bo{?^`}  6+6 p=4 g=1 e=-2     K????BoBo^]B  6+6 p=4 g=2 e=0
```

All 18 witnesses re-verified by the frozen Python `e1scan.py`
(sha256 `11dc5f28…`); full histograms in `work/census/exc/`. This is the
preregistration population mandated by ATTACK.md v3 Step 3 target 3: any
future lifting threshold must be tested against these graphs (and the
excess-0 members at the target order) before prose. The negative-excess
pair shows the L7 deficit can strictly grow with n — full-side bounds fall
behind `p` by arbitrary-looking amounts, reinforcing the CX(m) obstruction.

## Artifacts

- `work/census/maint_census.c` + `MAINT-CENSUS-SHA256.txt` (frozen engine)
- `work/census/n10/out-R.txt`, `n10/tight-R.g6` (8 shards),
  `tight-n10-sorted.g6` (52,303, matches published)
- `work/census/exc/n11.txt`, `exc/n12-R.txt` (4 shards)
- `work/census/reverify_witnesses.py` (Python re-verification driver)
- gold inputs `gold_cond.g6`, `cx_golds.g6`
