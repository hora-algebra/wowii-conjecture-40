"""nc0520 — prospective checker for the NC lemma (clean-end chordlessness).

FROZEN before the target run; see PREREG-NC.md for the preregistration, the
universe, the controls and the decision rules.  Uses engine0520 (independently
written, anchored at systems=115774 cyclic=798 pdis=18).

Notation.  Forced-core cycle F with S-side P and H-side Q, in cyclic order.
A_s = canonical (inclusion-minimum Hall-tight) set containing s; B_s = A_s\\{s};
U = union of B_s over s in P.  For q in Q write cyc(q) = the two cycle vertices
of q.

CLAIMS TESTED
  NC   (primary, believed TRUE, proof in LEMMA-A-CLEAN-END.md):
       for every q in Q with deg_U(q) <= 1,
         (N_S(q) & P) == cyc(q)          [no chord from another cycle vertex]
         (N_S(q) & (U \\ P)) == empty     [no auxiliary of U touches q]
  NCM  (corollary, believed TRUE): P\\U is nonempty, and for every s in P\\U both
       forced ends q of s satisfy deg_U(q) <= 1 and NC's conclusion; hence
       |N_S(q) & (P u U)| == 2 at those ends.
  CPR  (regression re-verification of b17e's CP): for distinct s,t in P,
       t in B_s implies A_t proper-subset A_s; and P\\U is exactly the set of
       inclusion-maximal carriers.

NEGATIVE CONTROLS (known FALSE; each MUST fire, else the harness is dead code)
  NC-ALL     every q in Q has deg_U(q) <= 1
  CHORD-ALL  every q in Q has (N_S(q) & P) == cyc(q)
  PDIS       P & U == empty                      [anchor: 18 in the exhaustive universe]
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine0520 as E

FAILS = []
CONTROL = Counter()


def check_system(S, H, nbH, cap, tag=""):
    """Returns None if not a cyclic-forced-core system, else 'ok' / 'fail'."""
    res = E.analyse(S, H, nbH, cap)
    if res is None:
        return None
    nbS = res['nbS']
    status = 'ok'
    for order in res['cycles']:
        P, Q, A, B, U, ends = E.cycle_data(res, order)
        Pset, Uset = set(P), set(U)

        # ---------------- CPR: regression re-verification of CP -------------
        for s in P:
            for t in P:
                if s != t and t in B[s]:
                    if not (A[t] < A[s]):
                        FAILS.append(('CPR-not-proper', tag, S, dict(nbH),
                                      dict(cap), f"s={s} t={t}"))
                        status = 'fail'
        maximal = {t for t in P
                   if not any(A[t] < A[r] for r in P if r != t)}
        if maximal != (Pset - Uset):
            FAILS.append(('CPR-maximal-mismatch', tag, S, dict(nbH), dict(cap),
                          f"maximal={sorted(maximal)} P\\U={sorted(Pset-Uset)}"))
            status = 'fail'
        if not (Pset - Uset):
            FAILS.append(('CPR-PminusU-empty', tag, S, dict(nbH), dict(cap), ""))
            status = 'fail'

        # ---------------- NC -------------------------------------------------
        L = len(order)
        cyc = {}
        for i, v in enumerate(order):
            if v[0] == 'H':
                cyc[v[1]] = {order[(i - 1) % L][1], order[(i + 1) % L][1]}
        for q in Q:
            degU = len(nbS[q] & U)
            if degU <= 1:
                extraP = (nbS[q] & Pset) - cyc[q]
                extraU = (nbS[q] & Uset) - Pset
                if extraP:
                    FAILS.append(('NC-chord', tag, S, dict(nbH), dict(cap),
                                  f"q={q} degU={degU} extraP={sorted(extraP)}"))
                    status = 'fail'
                if extraU:
                    FAILS.append(('NC-aux', tag, S, dict(nbH), dict(cap),
                                  f"q={q} degU={degU} extraU={sorted(extraU)}"))
                    status = 'fail'

        # ---------------- NCM ------------------------------------------------
        for s in (Pset - Uset):
            for q in ends[s]:
                degU = len(nbS[q] & U)
                if degU > 1:
                    FAILS.append(('NCM-CSa', tag, S, dict(nbH), dict(cap),
                                  f"s={s} q={q} degU={degU}"))
                    status = 'fail'
                if len(nbS[q] & (Pset | Uset)) != 2:
                    FAILS.append(('NCM-degS', tag, S, dict(nbH), dict(cap),
                                  f"s={s} q={q} "
                                  f"NS={sorted(nbS[q] & (Pset|Uset))}"))
                    status = 'fail'

        # ---------------- NEGATIVE CONTROLS ----------------------------------
        if any(len(nbS[q] & U) > 1 for q in Q):
            CONTROL['NC-ALL'] += 1
        if any((nbS[q] & Pset) - cyc[q] for q in Q):
            CONTROL['CHORD-ALL'] += 1
        if Pset & Uset:
            CONTROL['PDIS'] += 1
    return status


def run(systems, label):
    nsys = ncyc = 0
    for (S, H, nbH, cap) in systems:
        nsys += 1
        if check_system(S, H, nbH, cap) is not None:
            ncyc += 1
    print(f"[{label}] systems={nsys} cyclic={ncyc} claim_failures={len(FAILS)}")
    print(f"    negative controls (each MUST be > 0): {dict(CONTROL)}")
    for f in FAILS[:5]:
        print("   FAIL", f)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "exhaustive"
    if mode == "exhaustive":
        mk = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        mp = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        run(E.gen_exhaustive(mk, mp), f"exhaustive k<={mk} p<={mp}")
    elif mode == "random":
        import random
        t = int(sys.argv[2])
        sd = int(sys.argv[3])

        def gen():
            rng = random.Random(sd)
            for _ in range(t):
                p = rng.randint(3, 6)
                k = rng.randint(2, 5)
                H = list(range(p))
                S = [f"s{i}" for i in range(k)]
                nbH = {}
                for s in S:
                    d = rng.randint(2, min(p, 4))
                    nbH[s] = frozenset(rng.sample(H, d))
                c1 = rng.sample(H, 2) if (p >= 2 and rng.random() < 0.5) else []
                cap = {h: (1 if h in c1 else 2) for h in H}
                yield (S, H, nbH, cap)
        run(gen(), f"random {t} seed {sd}")
