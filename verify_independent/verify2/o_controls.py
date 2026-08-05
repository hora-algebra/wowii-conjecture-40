#!/usr/bin/env python3
"""VERIFY-2: the three published Lemma-A positive controls O-56/O-63/O-64,
loaded from tools/witnesses/*.json and run through the independent poset
engine.  PREREG-CARRIER-POSET.md requires each to parse as a feasible system
with a cyclic forced core, to pass CP, and to reproduce P intersect U = empty."""
import json, sys, os
from posetverify2 import Sys, check_cp_adj, mask_list

WDIR = sys.argv[1] if len(sys.argv) > 1 else "tools/witnesses"

EXPECT = {"O-56": {"nsel": 1, "Pu_empty": True},
          "O-63": {"nsel": 6, "Pu_empty": True},
          "O-64": {"nsel": 1, "Pu_empty": True}}

allok = True
for wid in ("O-56", "O-63", "O-64"):
    d = json.load(open(os.path.join(WDIR, wid + ".json")))
    Snames = [str(x) for x in d["vertices"]["S"]]
    inc = [(str(a), str(b)) for a, b in d["incidence_edges_S_H"]]
    # only H-vertices that actually carry an incidence matter to the system
    Hnames = sorted({b for _, b in inc})
    sidx = {s: i for i, s in enumerate(Snames)}
    hidx = {h: i for i, h in enumerate(Hnames)}
    caps = d.get("capacities", {})
    c1 = set(str(x) for x in caps.get("c1_vertices", []))
    cap = [1 if h in c1 else 2 for h in Hnames]
    nb = [[] for _ in Snames]
    for a, b in inc:
        nb[sidx[a]].append(hidx[b])
    sysm = Sys([tuple(sorted(x)) for x in nb], cap)

    sels = sysm.selections()
    r = check_cp_adj(sysm)
    print("=== %s" % wid)
    print("   S=%s  H(incident)=%s  cap=%s" % (Snames, Hnames, cap))
    print("   feasible selections: %d   (published %d)"
          % (len(sels), EXPECT[wid]["nsel"]))
    ok = len(sels) == EXPECT[wid]["nsel"]
    if r is None:
        print("   *** NO CYCLIC FORCED CORE (control FAILED)")
        allok = False
        continue
    A, uniq = sysm.carriers()
    for dt in r["detail"]:
        Pn = [Snames[s] for s in dt["P"]]
        print("   forced cycle: P=%s Q=%s" % (Pn, [Hnames[q] for q in dt["Q"]]))
        print("   carriers: %s" % {Snames[int(s)]: [Snames[i] for i in v]
                                   for s, v in dt["A"].items()})
        print("   U=%s  P\\U=%s  P&U empty=%s  CP holds=%s  ADJ holds=%s"
              % ([Snames[i] for i in dt["U"]],
                 [Snames[i] for i in dt["P_minus_U"]],
                 not dt["pdis"], not dt["cp_fail"], dt["adj_ok"]))
        ok &= (not dt["cp_fail"]) and ((not dt["pdis"]) ==
                                       EXPECT[wid]["Pu_empty"])
    print("   CONTROL %s" % ("PASS" if ok else "FAIL"))
    allok &= ok

print()
print("ALL THREE POSITIVE CONTROLS PASS:", allok)
