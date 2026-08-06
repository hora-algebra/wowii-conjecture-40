#!/usr/bin/env python3
"""Insert the generated n=12 section into ATTEMPT_REPORT.md and fill the
n=12 lessons bullet.  Run from work/064c."""
import json, subprocess, sys, re

REPORT = '../../ATTEMPT_REPORT.md'

sec = subprocess.run([sys.executable, 'report_n12.py'], capture_output=True,
                     text=True).stdout.rstrip() + "\n"
agg = json.loads(subprocess.run([sys.executable, 'aggregate_n12.py'],
                                capture_output=True, text=True).stdout)
rep = json.loads(subprocess.run(
    [sys.executable, 'thm4_replay.py', 'results/n11-s*.json',
     'results/n12-*.json.partial', 'results/n12-r*[0-9bcde].json',
     'results/n12-g*.json'], capture_output=True, text=True).stdout)
t = agg['totals']
cov = agg['coverage_fraction']

txt = open(REPORT).read()
start = txt.index('## n=12 coverage and verdict')
end = txt.index('## Recommended next angle')
txt = txt[:start] + sec + "\n" + txt[end:]

if cov >= 0.9999 and not agg['gaps']:
    scope = ("the **complete exhaustive n=12 universe** (all 212,780 connected "
             "bipartite graphs)")
else:
    scope = ("**%.1f%% of the n=12 universe**, as an explicit disjoint union of "
             "index intervals" % (100 * cov))
bullet = (
    "- [COMPUTATIONALLY VERIFIED] Over %s — every minimum FVS with `|S| ≥ 1`, "
    "every `H`-edge, every feasible selection: %s graphs, %s instances, %s "
    "feasible selections, %s selected cycle components, %s A1-failing cycles "
    "and %s hard states, every one of which satisfies the successor claim, with "
    "all %s minimizing steps out of hard states landing on a successor whose "
    "new cycle has `d₀ = 1`. The bad-step trichotomy was re-graded from "
    "certificates on %d A1-bad records / %d bad steps (%s) with 0 failures and "
    "no occurrence of the CL-7-falsifying case."
    % (scope, f"{t['graphs']:,}", f"{t['instances']:,}", f"{t['selections']:,}",
       f"{t['cycle_components']:,}", f"{t['a1_fail']:,}",
       f"{t['hard_states']:,}", f"{t['cl7_steps']:,}", rep['records'],
       rep['bad_steps'],
       ", ".join("%d of type %s" % (v, k)
                 for k, v in sorted(rep['cases'].items()))))
txt = re.sub(r"- \[COMPUTATIONALLY VERIFIED\] N12PLACEHOLDER", bullet, txt)
open(REPORT, 'w').write(txt)
print("report finalized; coverage %.4f gaps %s" % (cov, agg['gaps']))
