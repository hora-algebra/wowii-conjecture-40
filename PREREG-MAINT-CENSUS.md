# Preregistration: maintenance census runs (operator-authorized, LOCAL ONLY)

Branch `maint/2026-08-census`, 2026-08-05. Results stay on this local branch;
nothing from this phase is pushed. Frozen BEFORE any n=10 condition data or
any n>=11 excess data was computed.

Engine: `work/census/maint_census.c`, SHA-256

    fd32245aa87c4eaebee24b454b00c0e9c18685f05a3862d4b733ef1dc3e83e15

(recorded in `work/census/MAINT-CENSUS-SHA256.txt`), a C port of the frozen
Python checkers `l6scan.py` (`2e568740…`) and `e1scan.py` (`11dc5f28…`) from
branch `attempt/2026-08-04-claude-fable-5-0eb8`, definitions ported 1:1.

## Pre-freeze validation (recorded, all exact)

- Gold (cond): DC{, K3, the seven L3 residuals, the three SV witnesses —
  no failures, K3 the only tight; CX11 in both labelings (`J??FF?^FuE?`,
  `JFw???^Fuo?`) and CX(4) (`L?~o?????^`}r?`) each fail S1 and S2 with the
  certified profiles (unique OCT, thresholds 1, slacks 3/3/4), S3 clean.
- cond on ALL connected graphs `3<=n<=8`: `connected=12111 nonbip=11859
  s1=0 s2=0 s3=0 tight=217` — identical to the recorded l6scan.py output.
- cond on ALL connected graphs `n=9`: `connected=261080 nonbip=260350
  s1=0 s2=0 s3=0 tight=2494`, tight set **identical** to the published
  `verification/v2-lift-census/lift-a-tight-n9.g6`. Runtime 6.7 s.
- excess on ALL connected bipartite `2<=n<=10`: `graphs=5015` with
  histogram `0:1 1:60 2:574 3:912 4:1545 5:1208 6:552 7:146 8:16 9:1` and
  the single witness `I??FF?^Fo a=5 b=5 p=2 g=1 excess=0` — identical to
  the recorded e1scan.py output.

## Run 1 (frozen): n = 10 L5/L6-condition census

- Universe: ALL connected graphs on 10 vertices (`geng -c -q 10 R/8`,
  R = 0..7), nonbipartite subset evaluated.
- Anchors (run FAILS on mismatch): shard `connected` sums to 11,716,571;
  `nonbip` sums to 11,712,539; S3 = 0 everywhere (exact LIFT-A is known
  clean at n=10 from the v1/v2 full census); the union of tight lists has
  exactly 52,303 members and equals, as a set, the published
  `verification/v2-lift-census/lift-a-tight-n10.g6`
  (SHA-256 `9fe71fb1c6675b06f59901060898304509b5179358be9967188cd88a25566a69`).
- DATA (the open question, settles CX11 minimality): S1 = number of graphs
  with NO minimum OCT satisfying `p <= 2c_e + Delta + 2r - 1`; S2 = same
  for `p <= Delta + 2g - 1`. Every S1/S2 witness graph6 is preserved with
  its full per-OCT profile and afterwards re-verified by the frozen Python
  `l6scan.py` itself (profile() must agree).
- Interpretation, frozen now: S1 = 0 means the minimal order of L5-condition
  failure is exactly 11, witnessed by CX11; S1 > 0 means it is 10 and the
  witnesses supersede CX11 as minimal.

## Run 2 (frozen): excess-0 component enumeration, n = 11 and n = 12

- Universe: ALL connected bipartite graphs on 11 then 12 vertices
  (`geng -c -b -q n`, n=12 sharded R/8).
- Anchors (run FAILS on mismatch): totals 25,598 (n=11) and 212,780 (n=12)
  — A005142.
- DATA: every graph with `excess(C) = |a-b| + 2 g(C) - p(C) <= 0`,
  preserved with `(a, b, p, g, excess)`; plus the full excess histogram.
  This is the population any future lifting threshold must be preregistered
  against (ATTACK.md v3, Step 3 target 3).
- INV-DOM (`g >= 1 + r`) is asserted per component in both modes; any
  violation aborts.
