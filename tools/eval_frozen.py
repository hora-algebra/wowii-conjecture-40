"""Frozen-hypothesis holdout test for the bipartite core of WOWII 40.
FROZEN STRONG HYPOTHESIS (see FROZEN_HYPOTHESIS.md): for every 2-connected
bipartite G with k=tau(G)>0, EVERY critical vertex v (tau(G-v)=k-1) satisfies
ell2(G,v) >= 2k+1.  margin(G)=ell(G)-(2k+1);  cost(v)=ell(G)-ell2(G,v);
excess(v)=cost(v)-margin;  success <=> excess(v)<=0.
Keeps the BB-vs-DP dual check as an integrity assertion. Classifies each
hypothesis violation B/C/D and records it."""
import signal
import subprocess
import sys
from itertools import combinations

sys.path.insert(0, ".")
import inv_b
import inv40_b
import experiment_b as EB
from experiment_b_dual import ell2_dp, critical

RUNS = "."
OUT = f"{RUNS}/frozen-holdout.txt"
VIO = f"{RUNS}/frozen-violations.txt"
PER_GRAPH_TIMEOUT = 90  # seconds; on exceed -> UNKNOWN, never a failure


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


signal.signal(signal.SIGALRM, _alarm)


def min_fvs_all(n, adj, k):
    res = []
    for S in combinations(range(n), k):
        Sset = set(S)
        keep = [u for u in range(n) if u not in Sset]
        idx = {u: i for i, u in enumerate(keep)}
        aa = [0] * len(keep)
        for u in keep:
            m = adj[u]
            while m:
                w = (m & -m).bit_length() - 1
                m &= m - 1
                if w > u and w not in Sset:
                    aa[idx[u]] |= 1 << idx[w]
                    aa[idx[w]] |= 1 << idx[u]
        if inv_b.forest_b(len(keep), aa) == len(keep):
            res.append(Sset)
    return res


def run(startn, endn, label):
    viol = tot = unknown = 0
    hist = {}
    for n in range(startn, endn + 1):
        gs = subprocess.run(["geng", "-b", "-C", "-q", str(n)],
                            capture_output=True, text=True).stdout.split()
        gi = nviol = ntot = nunk = 0
        for g6 in gs:
            gi += 1
            if gi % 200 == 0:
                with open(OUT, "a") as fo:
                    fo.write(f"[{label}] n={n} {gi}/{len(gs)} tot={tot} "
                             f"viol={viol} unknown={unknown}\n")
            nn, adj = inv_b.parse_g6(g6)
            k = EB.tau(nn, adj)
            if k == 0:
                continue
            ntot += 1
            tot += 1
            try:
                signal.alarm(PER_GRAPH_TIMEOUT)
                ellG = nn - inv40_b.pathcover_b(nn, adj)
                margin = ellG - (2 * k + 1)
                C = critical(nn, adj, k)
                dp = ell2_dp(nn, adj)
                succ = []
                all_ok = True
                for v in C:
                    bb = EB.ell2(nn, adj, v)
                    assert bb == dp[v], f"DUAL MISMATCH {g6} v={v} bb={bb} dp={dp[v]}"
                    excess = (ellG - dp[v]) - margin
                    hist[excess] = hist.get(excess, 0) + 1
                    if dp[v] >= 2 * k + 1:
                        succ.append(v)
                    else:
                        all_ok = False
                signal.alarm(0)
            except _Timeout:
                signal.alarm(0)
                unknown += 1
                nunk += 1
                with open(VIO, "a") as vf:
                    vf.write(f"[{label}] {g6} n={nn} k={k} class=E UNKNOWN "
                             f"(exceeded {PER_GRAPH_TIMEOUT}s)\n")
                continue
            if not all_ok:
                viol += 1
                nviol += 1
                fvss = min_fvs_all(nn, adj, k)
                every_fvs = all(any(v in S for v in succ) for S in fvss)
                cls = "B" if (succ and every_fvs) else ("C" if succ else "D")
                with open(VIO, "a") as vf:
                    vf.write(f"[{label}] {g6} n={nn} k={k} margin={margin} "
                             f"C={C} succeed={succ} class={cls} "
                             f"ell2={[dp[v] for v in C]}\n")
                if cls == "D":  # existential failure: STOP and preserve witness
                    with open(OUT, "a") as fo:
                        fo.write(f"[{label}] *** EXISTENTIAL FAILURE (class D) at "
                                 f"{g6} n={nn} k={k} — HALTING, witness preserved ***\n")
                    print(f"*** EXISTENTIAL FAILURE class D: {g6} n={nn} k={k} — STOPPED")
                    sys.exit(2)
        with open(OUT, "a") as fo:
            fo.write(f"[{label}] n={n} DONE graphs={ntot} violations={nviol} "
                     f"unknown={nunk}\n")
    with open(OUT, "a") as fo:
        fo.write(f"[{label}] {startn}-{endn} DONE tot={tot} violations={viol} "
                 f"unknown={unknown} excess_hist={dict(sorted(hist.items()))}\n")
    print(f"[{label}] {startn}-{endn}: total={tot} FROZEN-HYPOTHESIS "
          f"violations={viol} unknown={unknown}")
    print(f"  excess histogram (<=0 means success): {dict(sorted(hist.items()))}")


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    lbl = sys.argv[3] if len(sys.argv) > 3 else "run"
    run(a, b, lbl)
