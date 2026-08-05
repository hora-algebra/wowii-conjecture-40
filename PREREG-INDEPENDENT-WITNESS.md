# Preregistration: independent n=12 mechanism witness check

The primary engine has produced a valid n=12 `(2,1)` certificate with these
provisional properties: its A1-bad cycle has no terminal slide; generic
B-PLUS-2 succeeds at length five; all minimizing successors satisfy SD-2STEP,
but their minimum distance is three rather than one.  Before assigning a
`FALSIFIED` label to either stronger mechanism statement, recheck this fixed
certificate with VERIFY-2's independent incidence-index engine from public
commit `6a94cb9b8b137249d6a19f25589112c09fdca9ee`.

Fixed certificate: graph6 `K??FFbw}Fw^_`, S=`[6,7,8,9,10]`, e=`[4,11]`,
J and target cycle exactly as embedded in the checker.  Required validations:
minimum FVS, feasibility, two selected cycles, target A1 failure with d0=3,
all minimizing paths enumerated without a cap, no terminal slide, generic first
CES at length five, successor minimum distance three on every minimizing path,
and a CES minimizing second step on every successor.

Any mismatch leaves the corresponding falsification unconfirmed.  The checker
loads the independent engine directly from the fixed git object and records its
sha256; it does not import the primary frozen engine.

