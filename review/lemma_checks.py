"""Independent finite checks. Never a substitute for the universal proof."""
import itertools,json,random,time
from pathlib import Path

def vertices(mask):
    while mask:
        bit=mask&-mask
        yield bit.bit_length()-1
        mask-=bit

def subsets(mask):
    x=mask
    while True:
        yield x
        if not x: break
        x=(x-1)&mask

def forest(a,mask):
    p=list(range(len(a)))
    def root(v):
        while p[v]!=v:v=p[v]
        return v
    for v in vertices(mask):
        for w in vertices(a[v]&mask&((1<<v)-1)):
            x,y=root(v),root(w)
            if x==y:return False
            p[x]=y
    return True

counts=dict(graphs=0,minimum_fvs_edge_instances=0,tight_sets=0,shared_tight_sets=0,
            strict_neighbourhood_checks=0,carrier_checks=0,direct_selection_checks=0)

def check(a,left):
    n=len(a);full=(1<<n)-1
    forests=[H for H in range(1<<n) if forest(a,H)]
    k=max(map(int.bit_count,forests))
    for H in forests:
        if H.bit_count()!=k:continue
        S=full^H
        for v in vertices(H):
            for w in vertices(a[v]&H&((1<<v)-1)):
                counts['minimum_fvs_edge_instances']+=1
                caps={h:1 if h in (v,w) else 2 for h in vertices(H)}
                def rank(X):return sum(min(caps[h],(a[h]&X).bit_count()) for h in caps)
                tight=[]
                forced=[0]*n
                for X in subsets(S):
                    rr=rank(X)
                    assert rr>=2*X.bit_count(),('hall',a,H,v,w,X)
                    if rr!=2*X.bit_count():continue
                    tight.append(X)
                    for h in caps:
                        if (a[h]&X).bit_count()<=caps[h]:
                            for s in vertices(a[h]&X):forced[s]|=1<<h;forced[h]|=1<<s
                assert forest(forced,full),('forced cycle',a,H,v,w)
                # Independently enumerate selections on a sample of small instances.
                if S.bit_count()<=3 and counts['direct_selection_checks']<1000:
                    choices=[list(itertools.combinations(vertices(a[s]&H),2)) for s in vertices(S)]
                    common=None;number=0
                    for sel in itertools.product(*choices):
                        loads={h:0 for h in caps};edges=set()
                        for s,hs in zip(vertices(S),sel):
                            for h in hs:loads[h]+=1;edges.add((s,h))
                        if any(loads[h]>caps[h] for h in caps):continue
                        number+=1;common=edges if common is None else common&edges
                    assert number
                    expected={(s,h) for s in vertices(S) for h in vertices(forced[s])}
                    assert common==expected
                    counts['direct_selection_checks']+=1
                for X in tight:
                    if not X or (X&left and X&(full^left)):continue
                    counts['tight_sets']+=1
                    U=sum(1<<h for h in caps if (a[h]&X).bit_count()>=2)
                    if U.bit_count()<2:continue
                    counts['shared_tight_sets']+=1
                    L=sum(1<<h for h in caps if (a[h]&X).bit_count()==1)
                    B=sum(1<<s for s in vertices(X) if (a[s]&L).bit_count()==2)
                    T=sum(1<<s for s in vertices(X) if (a[s]&L).bit_count()==1)
                    Z=X&~(B|T)
                    assert T.bit_count()==1 and Z.bit_count()==U.bit_count()-1
                    t=next(vertices(T));assert a[t]&U==U
                    for W in subsets(Z):
                        if not W:continue
                        N=0
                        for s in vertices(W):N|=a[s]&U
                        assert N.bit_count()>=W.bit_count()+1
                        counts['strict_neighbourhood_checks']+=1
                    for A in tight:
                        if A&~X:continue
                        reduced=A&~B
                        assert rank(reduced)==2*reduced.bit_count()
                        if reduced&T:assert reduced==Z|T
                        counts['carrier_checks']+=1
    counts['graphs']+=1

