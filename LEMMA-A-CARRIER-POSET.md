# Lemma A: carrier-containment poset

Branch `attempt/2026-08-05-codex-gpt-5-b17e`, 2026-08-05. Primary target:
ATTACK.md Step 3 target 1, Lemma A on `T_F`-normalized instances.
Preregistration: `PREREG-CARRIER-POSET.md`.

## Result

**CP — MATHEMATICALLY PROVED (not Lean-formalized) and COMPUTATIONALLY
VERIFIED** on the preregistered universe of 798 cyclic forced-core systems.

Let `F` be a forced-core cycle with `S`-side `P`. For each `s in P`, let
`A_s` be the canonical carrier, the unique minimum Hall-tight set containing
`s`; put `B_s=A_s\{s}` and `U=union_(s in P) B_s`.

> **Carrier-poset lemma (CP).** For distinct `s,t in P`, if `t in B_s`, then
> `A_t` is a proper subset of `A_s`. Thus the digraph on `P` with an arc
> `s -> t` when `t in B_s` is acyclic, the cycle carriers are pairwise
> distinct, and
>
>     P\U = {t in P : A_t is inclusion-maximal among {A_s:s in P}}.
>
> In particular `P\U` is nonempty.

### Proof

Punctured tightness says `B_s` is Hall-tight. If `t in B_s`, then `B_s` is a
tight set containing the cycle vertex `t`. By the defining minimality of
`A_t`,

    A_t subseteq B_s = A_s\{s} proper-subset A_s.

Every arc therefore strictly decreases carrier inclusion, so a directed cycle
is impossible.

If two distinct cycle vertices had the same carrier, then `t in A_t=A_s`
would put `t in B_s`, and the preceding strict inclusion would give
`A_t proper-subset A_s`, a contradiction. Hence the carriers are distinct.

If `t in P intersect U`, some `s` has `t in B_s`, so `A_t proper-subset A_s`
and `A_t` is not maximal. Conversely, if `A_t proper-subset A_s`, then
`t in A_t subseteq A_s`; since `s != t`, this puts `t in B_s subseteq U`.
Thus `t notin U` iff `A_t` is inclusion-maximal. A finite nonempty family of
sets has an inclusion-maximal member, proving `P\U` is nonempty. ∎

### New consequence for Lemma CS

**MATHEMATICALLY PROVED.** Lemma CS(a) was conditional on choosing
`s in P\U`: both forced ends `q` of such an `s` obey `deg_U(q)<=1`. CP proves
that at least one such `s` always exists. Therefore every forced-core cycle
has a cycle vertex whose two forced ends each retain at least one unit of
capacity outside `U`. This conclusion is unconditional at the Hall layer; it
does not require the known-false assumption `P intersect U = empty`.

Oracle contact for the consequence is the conjunction of the prior
`carrier.py` CS(a) scan (zero CS failures on the same 798-system exhaustive
universe, with false controls firing) and the new prospective CP scan below.

## Prospective verification

Frozen hashes, committed before target execution:

```
7fe9f98569bb4bebb980b69dbb734993b82f4d5c499ad1efa3dab90a2f4d7222  work/b17e/carrier_poset.py
d11b0bca3a4ac437b4811ce588e660fe2e382ccd725e017fbadd2919e195696a  work/carrier.py
```

Positive controls O-56/O-63/O-64 each produced one forced cycle, passed every
CP predicate, and reproduced `P intersect U = empty`. The negative companion
PDIS fired on a system with `P intersect U != empty`.

Target universe: all 115,774 abstract systems from
`carrier.gen_exhaustive(3,5)`; 798 had a cyclic forced core. Published anchors
reproduced exactly, including all 18 systems with `P intersect U != empty`.

```
TARGET systems=115774 cyclic=798 pdis=18 CP_fail=0 ADJ_fail=18
```

Runtime was 4.21 s wall. Raw output is in
`work/b17e/carrier-poset-scan.txt`.

## ADJ is falsified

**FALSIFIED.** The preregistered stronger lead

> two vertices of `P\U` are consecutive around every forced cycle

fails on all 18 overlap systems in this universe. The first certificate is:

```
S = P = {s0,s1,s2}, H-incidence vertices = {0,1,2}, all capacities 2
N(s0) = {0,1}
N(s1) = {0,2}
N(s2) = {0,1,2}
A_s0 = {s0}, A_s1 = {s1}, A_s2 = {s0,s1,s2}
U = {s0,s1}, P\U = {s2}
```

The feasible selection is unique: `s0->{0,1}`, `s1->{0,2}`, and saturation
of `0` forces `s2->{1,2}`. Its forced core is the 6-cycle

    s0-0-s1-2-s2-1-s0.

There is only one maximal carrier, `A_s2`, so no two maximal-carrier vertices
can be consecutive. To realize the all-capacities-two abstract system in the
paper's disconnected fixed-edge model, add a separate edge `xy` with no
incidences. The machine-readable certificate is
`work/b17e/ADJ-WITNESS.json`.

Independent verification with `work/wcheck.py` (no code shared with the new
checker) found: bipartite true; `H` a forest; one feasible selection; six
forced incidences; forced-core cycle rank one; Hall-tight sets
`empty,{s0},{s1},{s0,s1},S`; and the carriers displayed above. An acyclic
unique-selection negative control returned forced-core cycle rank zero.

The witness is **not** a counterexample to Lemma A: it has
`tau(G[H union S])=1<3`, so hereditary FVS tightness fails. It falsifies only
the Hall-layer ADJ shortcut. In particular CP guarantees two capacity holes at
the two forced ends of at least one maximal vertex, but one cannot infer an
endpoint with `deg_U(q)=0`; in this witness the unique maximal vertex has both
ends at `U`-degree one.

## Scope and next use

CP converts the overlap `P intersect U != empty` from an arbitrary membership
pattern into a strict finite hierarchy of carriers and guarantees a maximal
cycle carrier outside every puncture. It is genuine movement beyond Lemma CS,
but it does not close Lemma A. The next carrier attack should use the two
capacity holes at a maximal vertex together with the augmented forest quotient;
it must allow a single maximal carrier and must not require two adjacent
maxima or a completely puncture-free cycle endpoint.
