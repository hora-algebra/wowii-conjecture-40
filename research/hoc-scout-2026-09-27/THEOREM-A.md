# Theorem A (anchor count): standalone statement and proof

**Status.** Claimed, with the complete proof below. It has had two non-blind reviews: a line-by-line referee pass by a separate Claude agent, which found it holds (its two wording fixes are incorporated here), and a cross-vendor re-derivation in ChatGPT's independent audit. It has also been replayed by machine (see the verification record). It has **not** been certified under the project's environmentally blind protocol.

## Setting

- `G` is a finite simple bipartite graph with classes `L`, `R`. Connectedness is not used.
- `S ⊆ V(G)` is such that `H = G − S` is a forest, and **hereditary FVS tightness** holds: `τ(G[H ∪ X]) = |X|` for every `X ⊆ S`. This holds for every minimum FVS (paper Lemma 3.3), and taking `X = S` it includes minimality.
- `e = xy ∈ E(H)` is the distinguished edge. Capacities are `κ(x) = κ(y) = 1` and `κ(h) = 2` otherwise.
- A **feasible selection** `J` gives each `s ∈ S` two distinct `H`-neighbours, and each `h ∈ H` receives at most `κ(h)` of them.
  - The incidence graph of `J` contains only the selected `S–H` edges. Its components are paths (an isolated `H`-vertex is a trivial path) and cycles. The **selected cycles** are the cyclic components.
  - `P(C) = V(C) ∩ S` and `Q(C) = V(C) ∩ H`.
  - `h` is **saturated** if `deg_J(h) = κ(h)`, and **slack** otherwise.
  - `T(J)` is the set of `S`-vertices on path components.
- Residual augmenting path, `d0`, minimizing step, CES, A1-good/A1-bad and hard state are exactly as in `PROOFS-SAFE2-064c.md` §0. In particular, the released arc is deleted from the network, `d0` is taken over avoidable incidences, and a cycle with no avoidable incidence is A1-bad.
- A selected cycle `C` is **slack-free** if no `G`-neighbour in `H` of any vertex of `P(C)` is slack.

## Inherited facts used

- **F0** (064c Fact 0). `P(C)` lies in one class and `Q(C)` in the other. Every vertex of `Q(C)` is saturated, and `x`, `y` lie on no selected cycle.
- **F1.** Every A1-bad cycle is slack-free, and so is a cycle with no avoidable incidence.
  - Suppose `s ∈ P(C)` has a slack neighbour `h'`.
  - Releasing either incidence of `s` then gives the residual path `s → h'` of length 1, so the incidence is avoidable.
  - A length-1 step is CES (064c Theorem 1), so `C` is A1-good.
  - Conversely, if `C` is slack-free, no length-1 residual path leaves `C`, so `d0(C) ≥ 3`. This is 064c Theorem 2; only `d0 = 1 ⟺` slack-adjacency is used, never "A1-good ⟺ slack-adjacent".
- **F2** (064c Prop. 12(i)). The number of path components is `p = |H| − |S|`.

## Fact P (parity)

Any two `H`-vertices of one `J`-component are joined by an `H–S–…–H` walk of even length, so they lie in the same class.

Since `x` and `y` are adjacent, they lie in different classes and therefore in different components. Both components are paths by F0. Hence `p ≥ 2`, and by F2, **`|H| ≥ |S| + 2`**. This holds for every instance with a feasible selection, so it is an invariant, not a filter.

## Lemma 1 (class-wise accounting; no tightness)

For the ordered class pair `(L, R)`:

`|Sat(J) ∩ R| = |S ∩ L| − r_R + δ_R ≤ |S ∩ L|`.

Here `r_R` counts the path components that contain an `S`-vertex and whose `H`-vertices lie in `R`. `δ_R = 1` exactly when the member of `{x, y}` lying in `R` has `J`-degree 1.

*Proof.* Each `S`-vertex lies in one component, and the `S`-vertices of the components whose `H`-vertices lie in `R` are exactly `S ∩ L`. Now count saturated `R`-vertices by component:

- **Cycles** with `H`-side in `R` contribute `|Q(C)| = |P(C)|` saturated vertices.
- **Nontrivial paths** with `H`-vertices in `R` and `m ≥ 1` `S`-vertices have `m + 1` `H`-vertices:
  - Their `m − 1` interior vertices have degree 2. They are not `x` or `y`, which have capacity 1, so they are saturated.
  - Their two ends have degree 1, so an end is saturated exactly when its capacity is 1, that is, when it is `x` or `y`.
- **Isolated `H`-vertices** are slack.

At most one of `x`, `y` lies in `R`, and summing gives the identity. If `δ_R = 1`, that degree-1 vertex is an end of such a path, so `r_R ≥ 1 ≥ δ_R`. ∎

Summing both ordered pairs gives `|Sat(J)| = |S| − r(J) + j(J) ≤ |S|`, where `j(J)` is the number of vertices of `{x, y}` of `J`-degree 1. This sharpens 064c Prop. 12(iii).

## Lemma 2 (slack-pair lemma; uses tightness)

For every `q ∈ Sat(J) ∩ R`, some `s ∈ S ∩ L` is `G`-adjacent to at least two vertices of `(Slack(J) ∩ R) ∪ {q}`.

*Proof.*

1. Let `D = (Sat(J) ∩ R) \ {q}`. By Lemma 1, `|D| ≤ |S ∩ L| − 1`.
2. In `F = G[H ∪ (S ∩ L)] − D`:
   - `H − D` is a forest;
   - `S ∩ L` is independent;
   - every `s ∈ S ∩ L` has its `H`-neighbours in `R`, so its neighbours in `F` lie in `(H ∩ R) \ D = (Slack ∩ R) ∪ {q}`.
3. If each `s ∈ S ∩ L` had at most one such neighbour, `F` would be a forest with pendant or isolated vertices added, hence a forest. Then `τ(G[H ∪ (S ∩ L)]) ≤ |D| < |S ∩ L|`, contradicting tightness.

If `S ∩ L = ∅`, Lemma 1 gives `Sat(J) ∩ R = ∅` and the statement is vacuous. ∎

## Lemma 3 (class anchor; uses tightness)

Suppose **at least one** selected cycle of `J` has its `S`-side in `L`, and every such cycle is slack-free. Let `X_L` be the union of their `S`-sides.

Then `X_L` has a saturated `G`-neighbour outside the union of their `H`-sides. Every such neighbour lies on a path component that contains an `S`-vertex: it is either a path-interior vertex, or `x` or `y` with `J`-degree 1.

*Proof.*

1. `X_L` is nonempty and independent. Pick `z0 ∈ N_H(X_L)` and delete `N_H(X_L) \ {z0}`. What remains of `G[H ∪ X_L]` is a forest, so `τ(G[H ∪ X_L]) ≤ |N_H(X_L)| − 1`. Tightness then gives `|N_H(X_L)| ≥ |X_L| + 1`.
2. The `H`-sides of these cycles have `|X_L|` vertices in total. So some neighbour `z` of `X_L` lies outside them.
3. `z` lies in `R` and is saturated, because the cycles are slack-free.
4. The saturated `R`-vertices lying on cycles are exactly the `H`-sides of the `L`-sided cycles, because `R`-sided cycles have their `H`-sides in `L`. So `z` lies on a path component.
5. Being saturated, `z` has degree at least 1, so its component contains an `S`-vertex. `z` is then either interior (degree 2) or an end of capacity 1. ∎

## Theorem A

**Every hard state `J` satisfies `|T(J)| ≥ 2`.**

More specifically, we prove: if every selected cycle of a cyclic feasible `J` is slack-free and `|T(J)| ≤ 1`, then some selected cycle has a CES minimizing step of length 3. Hard states satisfy the slack-free premise by F1.

*Proof.* Let `J` be cyclic, with all selected cycles slack-free, and suppose `|T| ≤ 1`.

**(a) `T = ∅`.** Every path component is an isolated, slack `H`-vertex. Lemma 3, applied to a class containing some cycle's `S`-side, needs a saturated vertex on a path component that contains an `S`-vertex, and there is none. So `T ≠ ∅`.

**(b) `T = {t}`.** Name the classes so that `t ∈ L`.

- Neither selected neighbour of `t` can have a second owner, since that owner would be another path `S`-vertex. So `t`'s component is exactly a path `a – t – b` with `a, b ∈ R`, and every other path component is an isolated slack vertex.
- Hence the only possible saturated path vertex is an end of this path that equals `x` or `y`. By Fact P, at most one of `x`, `y` is on it.
- If some cycle had its `S`-side in `R`, Lemma 3 (with the roles of `L` and `R` exchanged) would need a saturated path vertex in `L`, and none exists. So every cycle has its `S`-side in `L`.
- Lemma 3 then yields a saturated end of `t`'s path of capacity 1 that is adjacent to a cycle `S`-vertex. Call it `x` (both `x` and `y` have capacity 1, so this is only naming).
- Call the other end `w`. By Fact P, `w ∉ {x, y}`, so `κ(w) = 2 > 1 = deg_J(w)`, and `w` is slack.
- Choose a cycle `C*` and `s ∈ P(C*)` with `s ~ x`, and let `q ∈ J(s)`. Then `q ∈ Q(C*) ⊆ Sat ∩ R`.

Now `S ∩ L = (∪ P(C)) ∪ {t}`. Apply Lemma 2 to `q`. Cycle `S`-vertices see no slack vertex, so they see at most `q`; the witness must therefore be `t`. Since `t` already sees `w`, either:

- (i) `t ~ q`, or
- (ii) `t ~ u` for some slack `u ∈ R` with `u ∉ {x, w}` (`u ≠ x` because `x` is saturated).

**Case (i).** Release `a = (s, q)` and use the path `s → x → t → q`.

- It is a residual augmenting path:
  - `(s, x) ∉ J`, because `s` selects only vertices of `Q(C*)`;
  - `x ≠ q` has `deg_{J−a}(x) = 1 = κ(x)`, so `x` is not a terminal;
  - `(t, x) ∈ J`, and it is not the released arc;
  - `(t, q) ∉ J`, because `t` selects `x` and `w`;
  - `deg_{J−a}(q) = 1 < 2`, so `q` is a terminal.
- The toggle is `J0 = J − (s,q) + (s,x) − (t,x) + (t,q)`. Its component containing `s` and `t` is the single path `x – s – … – q – t – w`, and every other component is unchanged.
- So `C*` is destroyed and no new cycle appears: the step is CES.

**Case (ii).** Release `a = (s, h)` for either `h ∈ J(s)` and use the path `s → x → t → u`.

- This is valid as above. `u` is a terminal because it is slack in `J` and `u ≠ h`.
- `u` is an isolated vertex of `J`, because the only nontrivial path is `x – t – w`.
- In `J0 = J − (s,h) + (s,x) − (t,x) + (t,u)`, the opened cycle becomes the path `x – s – … – h`, and `t`'s component becomes the path `w – t – u`.
- No cycle contains `s` or `t`, so the step is CES.

In both cases the path has length 3. `C*` is slack-free, so `d0(C*) ≥ 3` by F1, and therefore `d0(C*) = 3` and the step is minimizing. So `C*` is A1-good.

Consequently a hard state, in which every cycle is A1-bad, cannot have `|T| ≤ 1`. ∎

Lemma A (the forced core is acyclic, which is OPEN) is not used anywhere. The proof exhibits the avoidable incidence it needs.

## Corollaries

1. **Size bound.** A hard state with `k ≥ 1` selected cycles has `|S| ≥ 2k + 2` and `n ≥ 4k + 6`.
   - Each cycle has at least 2 `S`-vertices, the cycles are disjoint, and `T` is disjoint from them; this gives the bound on `|S|`.
   - `|H| ≥ |S| + 2` by Fact P, which gives the bound on `n`.
2. **HOC holds for `n ≤ 13`.**
3. **The only possible shape at `n = 14`.** A counterexample to HOC at `n = 14` has:
   - `|S| = 6` and `|H| = 8`;
   - exactly two selected cycles, both 4-cycles;
   - `|T| = 2`;
   - exactly two path components, namely the component of `x` and the component of `y` (by Fact P and `p = 2`).
4. **Larger shapes.** A hard state with three cycles needs `n ≥ 18`. A two-cycle counterexample containing a cycle longer than 4 needs `n ≥ 16`.
5. **HOC ⇒ μ ≤ 1** for every instance, where `μ = min c(J)` over feasible `J` (feasible selections exist by paper Corollary 3.9).
   - If `μ ≥ 2`, a selection `J` attaining `μ` has no CES minimizing step, since such a step would leave fewer than `μ` cycles.
   - So `J` is a hard state with at least 2 cycles.

## Not established here

The review's n=14 sketch is **not established**. It claimed:

- opposite orientation is excluded;
- same orientation survives only with the path `x–t1–v–t2–w`, `y` isolated, `S` inside one class and `H` a star at `y`;
- `v` is never an anchor.

## Verification record

- **Referee.** A separate Claude agent, non-blind, rebuilt the argument line by line and found that it holds. Its two wording fixes (Lemma 3 needs at least one `L`-sided cycle; in case (ii), `u ∉ {x, w}`) are applied above.
- **Referee's engines.** Two independent implementations, in Python and C++:
  - checked Lemmas 1–3 and `|T| ≥ 2` on every hard state through n=12, with 0 failures;
  - replayed the construction on every slack-free state with `|T| ≤ 1` through n=12 (95,193 states at n=12, about 1.18M constructed steps), with 0 failures;
  - found 0 failures on disconnected bipartite graphs up to n=10.
- **Lemma 2 at n=12.** 0 violations over all 1,468,422,722 feasible selections, checked with `engine/hoc.c -P`.
  - Negative control: with a non-minimum FVS of size `τ + 1`, it fails 80 / 1,344 / 11,149 times at n=7/8/9.
  - The tightness-free Lemma 1 has 0 violations throughout.
- **ChatGPT's independent audit.**
  - It re-derived the proof.
  - Its separate verifier (`verify_certificates.py`, sha256 `dee86d22…`) replayed all 2,216 supplied n=11/12 certificate rows, including 6,188 executions of the construction, with 0 failures.
  - Re-running that verifier on `results/` reproduces its recorded output exactly, and its gates fire under mutation.

## Handoff editorial note

This readable copy changes only the introductory word "Equivalently" to "More specifically, we prove" relative to the v2 original. The constructive assertion is stronger than the headline theorem, and is proved directly. The unchanged v2 original remains in the inherited archive (SHA-256 `7d3367da0c2cf6d2adfb969e1991fa0317a68f0d7a64cdef6bcdc30c2aa8e1e6`). This edit does not confer protocol certification. Consult `BASELINE-AND-ERRATA.md` for the exact residual definitions, source errata and limits of the reported verification record.
