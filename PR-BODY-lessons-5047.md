# Prepared PR description — `Lessons: attempt/2026-08-03-claude-opus-5-5047`

Not opened. Held for the operator; this file is the intended body if and when
the `lessons/5047` branch is pushed and a pull request is raised against `main`.

---

Appends one entry to `attempts/LESSONS.md` per ATTACK.md Step 5, from attempt
branch `attempt/2026-08-03-claude-opus-5-5047` (2026-08-03, Claude Opus 5
(1M context) / Claude Code CLI).

## Headline

**SV (paper Definition 5.3; ATTACK.md open item 3) is FALSIFIED.** The minimum
order of a counterexample is 11. Two hand-checkable witnesses are certified in
`SV-FALSIFIED.md` on the attempt branch — `J???FAWdVD?` (15 edges) and
`J???FBObs\?` (16 edges) — each with `f=9, b=10, p=3`, a **unique** minimum
odd-cycle transversal `{0}`, and `p(G-0) = 2 < 3 = p(G)`.

Verified by four engines, including **both** engines of the paper's own
dual-engine protocol at their published hashes
(`shasum -a 256 -c verification/SHA256SUMS.txt` → 237/237 OK):

```
$ ./phase0 run2 < witnesses.g6
J???FAWdVD? oG=1 pG=3 elig=1 minGain=-1
J???FBObs\? oG=1 pG=3 elig=1 minGain=-1
```

`n = 11` is minimal: SV was re-verified independently from Definition 5.3 with
0 failures over all 272,209 connected nonbipartite graphs with `n <= 9` and all
11,712,539 at `n = 10`, both census counts matching the paper exactly.

**Conjecture 40 is not affected** — the paper states that a failure of SV would
not refute it, and both witnesses satisfy it with slack 4. What this closes is
the route: Theorem 5.5 (SV + bipartite case ⇒ full conjecture) now rests on a
false hypothesis, and §5 needs an erratum. The other route through the same gap,
the lifting inequality, survives on these very witnesses.

## Also in the entry

* Lemma A verified exhaustively at **n = 12, 13 and 14** (10,970,519 /
  141,887,501 / 2,391,365,507 instances, zero cyclic forced cores); the paper's
  `n = 11` footnote is now a reproducible hashed run and is dual-engined.
* F2 — the statement Theorem 3.13 actually needs — scanned directly for the
  first time, clean through `n = 13`.
* LIFT-A and LIFT-A-ALL preregistered and clean over all 11,716,571 connected
  graphs `n <= 10` plus a preregistered `n = 11` holdout; LIFT-P falsified by the
  same SV witnesses.
* One new proved lemma (carrier–cycle separation) and three recorded dead ends.

## One deviation, ruled on by the operator

This commit also **deletes the line `(No entries yet.)`** from
`attempts/LESSONS.md`. ATTACK.md Step 5 says that file may be changed "only by
appending", so the deletion is flagged explicitly rather than slipped in.

**Operator ruling (2026-08-03): permitted** — `(No entries yet.)` is a
placeholder, not an entry, and the file's own rule scopes append-only to entries
("never edit or delete a prior entry"). Leaving it in place above a real entry
would make the file self-contradictory. No prior entry is touched; the change is
one placeholder line removed plus the new entry appended.

## Provenance

* Attempt branch: `attempt/2026-08-03-claude-opus-5-5047`, 26 commits, base
  `main` = `0617d7a`.
* Full report: `ATTEMPT_REPORT.md`; certificate: `SV-FALSIFIED.md`;
  comprehension record: `GAUNTLET.md`; preregistrations: `PREREG-LIFT.md`,
  `PREREG-LIFT-N11.md` (both committed before their runs).
