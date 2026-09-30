"""All labelled simple graphs through order 6, independent X and forest H."""
import itertools,json,time
from lemma_checks import forest,vertices,subsets
counts=dict(graphs=0,partitions=0,even_shared=0,odd_equal=0,expansion=0)
t0=time.monotonic()
for n in range(7):
 es=list(itertools.combinations(range(n),2));full=(1<<n)-1
 for bits in range(1<<len(es)):
  a=[0]*n
  for i,(v,w) in enumerate(es):
   if bits>>i&1:a[v]|=1<<w;a[w]|=1<<v
  ff=[forest(a,m) for m in range(1<<n)]
  tau=n-max(m.bit_count() for m in range(1<<n) if ff[m])
  counts['graphs']+=1
  for X in range(1<<n):
   H=full^X
   if not ff[H] or any(a[x]&X for x in vertices(X)):continue
   counts['partitions']+=1
   U=sum(1<<h for h in vertices(H) if (a[h]&X).bit_count()>=2)
   L=sum(1<<h for h in vertices(H) if (a[h]&X).bit_count()==1)
   d={x:(a[x]&L).bit_count() for x in vertices(X)}
   B=sum(1<<x for x in d if d[x]>=2);rho=2*U.bit_count()+L.bit_count()
   assert forest(a,full&~(U|B)) and tau<=rho//2
   if U and rho%2==0:
    counts['even_shared']+=1
    assert tau<=rho//2-1
   if not(U and tau==X.bit_count() and rho==2*tau+1):continue
   counts['odd_equal']+=1
   ts=[x for x in d if d[x]==1];assert len(ts)==1 and all(v<=2 for v in d.values())
   t=ts[0];Z=sum(1<<x for x in d if d[x]==0)
   assert a[t]&U==U and Z.bit_count()==U.bit_count()-1
   for W in subsets(Z):
    if not W:continue
    N=0
    for w in vertices(W):N|=a[w]&U
    assert N.bit_count()>=W.bit_count()+1
    counts['expansion']+=1
print(json.dumps(dict(status='PASS',counts=counts,seconds=time.monotonic()-t0)))
