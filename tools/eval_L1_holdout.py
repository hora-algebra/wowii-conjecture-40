"""Sealed n=10 holdout for the L1 / R2=0 / every-cycle-has-R1 findings.
Uses the corrected, dual-verified elementary-move engine (E1-corrected,
verified equal to the independent E2 on all cyclic states n<=9).
Preregistered classifications; frozen before opening (see FROZEN_L1.md)."""
import sys, subprocess
from itertools import combinations, product
sys.path.insert(0, '.')
import inv_b, experiment_b as EB
from eval_frozen import min_fvs_all
OUT = "L1-holdout.txt"

def feasible(n,adj,S,x,y):
    Hv=[v for v in range(n) if v not in set(S)]; cap={h:2 for h in Hv}; cap[x]=1; cap[y]=1
    per=[]
    for s in S:
        nb=[h for h in Hv if adj[s]>>h&1]; per.append(list(combinations(nb,2)))
        if not per[-1]: return []
    out=[]
    for ch in product(*per):
        d={}; e=[]
        for si,s in enumerate(S):
            a,b=ch[si]; e+=[(s,a),(s,b)]; d[a]=d.get(a,0)+1; d[b]=d.get(b,0)+1
        if all(d.get(h,0)<=cap[h] for h in Hv): out.append(frozenset(e))
    return out
def comps(J,e):
    g={}
    for (u,v) in list(J)+[e]: g.setdefault(u,[]).append(v); g.setdefault(v,[]).append(u)
    seen=set(); res=[]
    for s0 in list(g):
        if s0 in seen: continue
        cc=[]; st=[s0]
        while st:
            u=st.pop()
            if u in seen: continue
            seen.add(u); cc.append(u); st+=[w for w in g[u] if w not in seen]
        res.append((set(cc), sum(len(g[u]) for u in cc)//2==len(cc)))
    return res
def ncyc(J,e): return sum(1 for c,cy in comps(J,e) if cy)
def nbrs(feas,J,Sset):
    Jset=set(J); res=set()
    for Jp in feas:
        if Jp==J: continue
        D=Jset^set(Jp)
        if not D: continue
        stt={z:('J' if z in Jset else 'P') for z in D}; inc={}; av={}
        for z in D:
            s,h=z; inc.setdefault(s,[]).append(z); inc.setdefault(h,[]).append(z); av.setdefault(s,set()).add(h); av.setdefault(h,set()).add(s)
        if any(len(v)>2 for v in inc.values()): continue
        s0=next(iter(inc)); sn=set(); st=[s0]
        while st:
            u=st.pop()
            if u in sn: continue
            sn.add(u); st+=[w for w in av[u] if w not in sn]
        if len(sn)!=len(inc): continue
        if any(len(es)==2 and stt[es[0]]==stt[es[1]] for es in inc.values()): continue
        d1=[v for v in inc if len(inc[v])==1]
        if len(d1) not in (0,2): continue
        if len(d1)==2 and any(v in Sset for v in d1): continue
        res.add(Jp)
    return res

if __name__=="__main__":
    L1fail=R1=R2=R3=allR3=cyc=comps_c=0; gi=0
    gs=subprocess.run(['geng','-bc','-q','10'],capture_output=True,text=True).stdout.split()
    for g6 in gs:
        gi+=1
        if gi%200==0:
            open(OUT,"a").write(f"progress {gi}/{len(gs)} cyc={cyc} L1fail={L1fail} R2={R2} allR3={allR3}\n")
        nn,adj=inv_b.parse_g6(g6); k=EB.tau(nn,adj)
        if k<2: continue
        for S in min_fvs_all(nn,adj,k):
            Sset=set(S); Hv=[v for v in range(nn) if v not in Sset]
            for (x,y) in [(u,w) for u in Hv for w in Hv if u<w and adj[u]>>w&1]:
                feas=feasible(nn,adj,list(S),x,y)
                if not feas: continue
                fs=set(feas); P={J:ncyc(J,(x,y)) for J in feas}
                for J in feas:
                    if P[J]==0: continue
                    cyc+=1
                    nb=nbrs(fs,J,Sset)
                    if not any(P[Jp]<P[J] for Jp in nb): L1fail+=1
                    for (cc,iscy) in comps(J,(x,y)):
                        if not iscy: continue
                        comps_c+=1
                        ce=[ed for ed in J if ed[0] in cc and ed[1] in cc]
                        hasR1=False
                        for ed in ce:
                            av=[Jp for Jp in fs if ed not in Jp]
                            if not av: R3+=1; continue
                            if any((Jp in nb) and (ed in (J^Jp)) and P[Jp]<P[J] for Jp in nb): R1+=1; hasR1=True
                            else: R2+=1
                        if not hasR1: allR3+=1
    open(OUT,"a").write(f"DONE n=10 HOLDOUT: cyclic_states={cyc} L1-state-FAILURES={L1fail} "
                        f"R1={R1} R2={R2} R3={R3} cycle_components={comps_c} all-R3-components={allR3}\n")
