"""B4 split checker (FROZEN before running; see FROZEN-B4.md v2).
Over every positive-gap selected cycle C and EVERY globally-shortest bad path Q0
(length d0, toggle not CES), with J0=toggle(J,a,Q0), released a=(s,h), terminal
t=Q0[-1], final added edge (u,t) with u=Q0[-2]:
  S-B4a : old selected cycles of J destroyed other than C = none.
  S-B4b : J0 has exactly one NEW cyclic component Z (not in J).
  S-B4c : Z contains the final added edge (u,t) (both ends in Z).
  termdeg: deg_{J0}(t).
  CASE-C : h is a vertex of Q0 (endpoint-return geometry; predicted h==t).
           For Case-C paths, also record whether the toggle is CES.
Tests the STRONG "all shortest bad paths" form (implies the lex-optimal form).
First failures preserved. Fresh residual-DAG engine (a1_verify). n on argv (default 10).
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
    npos=0; checked=0; fa=fb=fc=0; caseC=0; caseC_notces=0; fails=[]; degset=set()
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
                        bad=[]; anyces=False
                        for an,(s,(d,fwd,term_d)) in per.items():
                            if d!=d0: continue
                            h=an[1] if an[0]==s else an[0]
                            for Q0 in enum_shortest_paths(fwd,s,term_d,d):
                                J0=toggle(Jn,an,Q0); J0c=cyc_sets_edges(J0,x,y)
                                ces=(Ccc not in J0c and J0c<=Jcyc)
                                if ces: anyces=True
                                else: bad.append((an,s,h,Q0,J0,J0c))
                        if anyces: continue
                        npos+=1
                        for (an,s,h,Q0,J0,J0c) in bad:
                            checked+=1
                            new=[z for z in J0c if z not in Jcyc]
                            olddes=[z for z in Jcyc if z not in J0c]
                            t=Q0[-1]; u=Q0[-2]; fe=(min(u,t),max(u,t))
                            degt=sum(1 for e in J0 if t in e); degset.add(degt)
                            oka=(olddes==[Ccc]); okb=(len(new)==1)
                            okc=okb and (fe[0] in new[0] and fe[1] in new[0])
                            if not oka: fa+=1
                            if not okb: fb+=1
                            if okb and not okc: fc+=1
                            if h in Q0:
                                caseC+=1
                                # CES already false here (this is a bad path)
                                caseC_notces+=1
                                if h!=t and len(fails)<10:
                                    fails.append(('CASE-C h!=t',g6,sorted(Sset),(x,y),sorted(cc),Q0,h,t))
                            if not (oka and okb and okc) and len(fails)<10:
                                fails.append((g6,sorted(Sset),(x,y),sorted(cc),Q0,'olddes',[sorted(z) for z in olddes],'new',[sorted(z) for z in new],'fe',fe,'degt',degt))
    print(f"n={NN}: pos-gap={npos} bad-checked={checked} termdeg_seen={sorted(degset)} "
          f"failS4a={fa} failS4b={fb} failS4c={fc} caseC_paths={caseC} caseC_notCES={caseC_notces}")
    for f in fails: print("  FAIL/NOTE:",f)
    return fa+fb+fc

if __name__=="__main__":
    run(int(sys.argv[1]) if len(sys.argv)>1 else 10)
