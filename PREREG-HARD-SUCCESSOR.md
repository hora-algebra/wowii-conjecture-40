# Preregistration: restrict successor-one to the actual hard states

The n=12 multi-cycle audit falsified the over-strong SUCCESSOR-ONE statements,
but every such counterexample has profile `(2,1)`: its state already has an
A1-good cycle, so SAFE-2-EXISTS uses its first alternative and never needs a
successor of the bad cycle.  This motivates the following strictly narrower
post-hoc claim.

**HARD-SUCCESSOR-ONE.**  If a cyclic feasible selection J has no A1-good
selected cycle, then some minimizing first step J -> J0 from some selected cycle
satisfies c(J0)<=c(J), and J0 has a CES minimizing step of length one.

This claim is descent-sufficient: a state with an A1-good cycle immediately
decreases c; a state without one uses the stated two-step block, which strictly
decreases c.  It is weaker than SUCCESSOR-ONE-DESCENT because it imposes a
successor condition only where the direct alternative is unavailable.

This is not prospective: it is formulated after the `(1,0)/(2,1)` split was
known.  The frozen test replays every retained `(1,0)` n=12 certificate from
4d7a commit `5cb5bb9a29718562d4d25a6902fd693f0a4677f4`.  The full profile has
1,184 such states; certificate caps retain 1,140.  The result is evidence only
on those 1,140 records, not an exhaustive n=12 grade.  Existing exhaustive n=11
evidence covers all six hard states there.

Any failure is independently checked before `FALSIFIED`.  Zero failures earns
only `CONJECTURAL (1,140 retained n=12 hard-state certificates plus exhaustive
n<=11 evidence)`.

