"""B4 bounded falsification checker (FROZEN before running; see FROZEN-B4.md).
Statement S-B4 (single-terminal-cycle structure of shortest bad paths):
For every selected cycle C whose gap is positive (NO globally-shortest residual
augmenting path over avoidable edges of C is CES), and for EVERY globally-shortest
bad path Q0 (length d0, toggle NOT CES):
  let J0 = toggle(J,a,Q0), t = Q0[-1]. Then
    (i)  J0 has EXACTLY ONE new cyclic component Z (a cycle set not present in J);
    (ii) t in Z;
    (iii) some selected edge (t,u) of J0 has both endpoints in Z.
Reports the FIRST failing (graph, S, e, C, Q0) per clause; does not tune around it.
Fresh residual-DAG engine (a1_verify). Bounded: n given on argv, default 10.
"""
import sys, subprocess
from collections import defaultdict
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
from eval_L1_holdout import feasible, comps, ncyc
from mine_n10 import walk_cycle
from a1_verify import norm, cyc_sets_edges, residual_dag, enum_shortest_paths, toggle

def run(NN):
    gs = subprocess.run(['geng','-bc','-q',str(NN)], capture_output=True, text=True).stdout.split()
    n_pos=0; checked=0; failI=failII=failIII=0; fails=[]
    for g6 in gs:
        nn, adj = inv_b.parse_g6(g6); k = EB.tau(nn, adj)
        if k < 2: continue
        for S in min_fvs_all(nn, adj, k):
            Sset=set(S); Hv=[v for v in range(nn) if v not in Sset]
            for (x,y) in [(u,w) for u in Hv for w in Hv if u<w and adj[u]>>w&1]:
                feas = feasible(nn, adj, list(S), x, y)
                if not feas: continue
                for J in feas:
                    if ncyc(J,(x,y))==0: continue
                    Jn=norm(J); Jcyc=cyc_sets_edges(Jn,x,y)
                    for (cc,iscy) in comps(J,(x,y)):
                        if not iscy: continue
                        Ccc=frozenset(cc)
                        order,_=walk_cycle(cc,J,x,y)
                        cyc_edges=[ed for (kk,ed) in order if kk=='J']
                        per={}
                        for ed in cyc_edges:
                            an=(min(ed),max(ed)); s=ed[0] if ed[0] in Sset else ed[1]
                            dag=residual_dag(nn,adj,Sset,x,y,J,an,s)
                            if dag is None: continue
                            per[an]=(s,dag)
                        if not per: continue
                        d0=min(dag[0] for (s,dag) in per.values())
                        # collect all shortest paths; is ANY CES? (gap==0 => skip)
                        badpaths=[]; anyces=False
                        for an,(s,(d,fwd,term_d)) in per.items():
                            if d!=d0: continue
                            for Q0 in enum_shortest_paths(fwd,s,term_d,d):
                                J0=toggle(Jn,an,Q0); J0c=cyc_sets_edges(J0,x,y)
                                if Ccc not in J0c and J0c<=Jcyc: anyces=True
                                else: badpaths.append((an,s,Q0,J0,J0c))
                        if anyces: continue           # gap 0, not our target
                        n_pos+=1
                        for (an,s,Q0,J0,J0c) in badpaths:
                            checked+=1
                            newc=[z for z in J0c if z not in Jcyc]
                            t=Q0[-1]
                            okI = (len(newc)==1)
                            okII = okI and (t in newc[0])
                            tue=[(min(t,u),max(t,u)) for u in Sset if (min(t,u),max(t,u)) in J0]
                            okIII = okII and any(e[0] in newc[0] and e[1] in newc[0] for e in tue)
                            if not okI: failI+=1
                            if okI and not okII: failII+=1
                            if okII and not okIII: failIII+=1
                            if not (okI and okII and okIII) and len(fails)<10:
                                fails.append((g6,sorted(Sset),(x,y),sorted(cc),Q0,len(newc),
                                              [sorted(z) for z in newc]))
    print(f"n={NN}: positive-gap cycles={n_pos} bad-paths-checked={checked} "
          f"failI(one-Z)={failI} failII(t-in-Z)={failII} failIII(term-edge-in-Z)={failIII}")
    for f in fails: print("  FAIL:",f)
    return failI+failII+failIII

if __name__=="__main__":
    NN = int(sys.argv[1]) if len(sys.argv)>1 else 10
    run(NN)
