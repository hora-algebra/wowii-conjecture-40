/* f2.c — direct oracle for F2 (paper Section 3.4 / PROOFS.md B3').
 *
 * F2 is what the bipartite case actually needs: for some fixed edge e of H
 * there is an ACYCLIC feasible selection.  Lemma A + Lemma B + the descent is
 * one route to F2, not an equivalent of it, and F2 itself has never been
 * scanned directly in this project.  This program tests the STRONGER
 * universally-quantified form
 *
 *   F2-ALL : for every minimum FVS S with tau >= 2 and every fixed edge e of
 *            H = G - S, an acyclic feasible selection exists,
 *
 * which is exactly what Lemma A + Lemma B would deliver, and reports the
 * existential form F2-SOME (some e works) separately.
 * The tau <= 1 layer is omitted as trivial: an incidence cycle requires two
 * S-vertices, and at tau <= 1 every feasible selection is acyclic.
 *
 * Method.  In a feasible selection every s has selected degree exactly 2, so
 * suppressing s (replacing the path h - s - h' by the edge {h,h'}) is a
 * homeomorphism onto a multigraph M on the vertex set H with one edge per s and
 * deg_M(h) = load(h) <= c(h).  Selected cycles of J are exactly cycles of M.
 * So an acyclic feasible selection is a choice of one pair sigma(s) of distinct
 * H-neighbours per s whose |S| edges form a LINEAR FOREST on H respecting the
 * capacities.  We search for one by backtracking with incremental union-find and
 * load counters, most-constrained s first.
 *
 * Usage:  f2 run < graph6      (use geng -bc -q N)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned int u32;
#define MAXN 16

static int N;
static u32 adj[MAXN];

static int decode_g6(const char *s){
    int idx=0;
    N = s[idx++]-63;
    if(N<1||N>MAXN) return 0;
    for(int i=0;i<N;i++) adj[i]=0;
    int cur=0, have=0;
    for(int j=1;j<N;j++) for(int i=0;i<j;i++){
        if(have==0){ cur=s[idx++]-63; have=6; }
        int b=(cur>>(have-1))&1; have--;
        if(b){ adj[i]|=(1u<<j); adj[j]|=(1u<<i); }
    }
    return 1;
}
static int is_forest(u32 S){
    int parent[MAXN];
    for(int i=0;i<N;i++) parent[i]=i;
    for(int j=0;j<N;j++) if(S>>j&1){
        u32 nb = adj[j] & S & ((1u<<j)-1);
        while(nb){
            int i=__builtin_ctz(nb); nb&=nb-1;
            int a=i; while(parent[a]!=a) a=parent[a];
            int c=j; while(parent[c]!=c) c=parent[c];
            if(a==c) return 0;
            parent[a]=c;
        }
    }
    return 1;
}

/* ---- backtracking search for a linear forest transversal ---- */

static int K;
static int optA[MAXN][64], optB[MAXN][64], nopt[MAXN];   /* candidate pairs */
static int ordr[MAXN];
static int capv[MAXN], loadv[MAXN];
static int uf[MAXN];
static int ufa[MAXN], ufb[MAXN], uftop;   /* undo log: ufa[t] was pointed to ufb[t] */

static int find_(int v){ while(uf[v]!=v) v=uf[v]; return v; }

static int solve(int depth){
    if(depth==K) return 1;
    int i=ordr[depth];
    for(int t=0;t<nopt[i];t++){
        int a=optA[i][t], b=optB[i][t];
        if(loadv[a]>=capv[a] || loadv[b]>=capv[b]) continue;
        int ra=find_(a), rb=find_(b);
        if(ra==rb) continue;                 /* would close a cycle */
        uf[ra]=rb; ufa[uftop]=ra; ufb[uftop]=rb; uftop++;
        loadv[a]++; loadv[b]++;
        if(solve(depth+1)) return 1;
        loadv[a]--; loadv[b]--;
        uftop--; uf[ufa[uftop]]=ufa[uftop];
    }
    return 0;
}

/* positive control: the three frozen witnesses have a forced cycle, so EVERY
 * feasible selection contains a cycle and the search MUST report failure.
 * Without this, "0 F2 failures" could be a solver that always says yes. */
static int ctl(const char*name,int n,int k,const int*Sl,const u32*inc,int ex,int ey){
    N=n; K=k;
    for(int v=0;v<N;v++){ capv[v]=2; loadv[v]=0; uf[v]=v; }
    capv[ex]=1; capv[ey]=1; uftop=0;
    for(int i=0;i<k;i++){
        nopt[i]=0;
        for(int a=0;a<N;a++) if(inc[i]>>a&1)
            for(int b=a+1;b<N;b++) if(inc[i]>>b&1){
                optA[i][nopt[i]]=a; optB[i][nopt[i]]=b; nopt[i]++; }
        ordr[i]=i;
    }
    int r=solve(0);
    printf("  %-8s acyclic feasible selection found = %d (expected 0)  %s\n",
           name,r,r==0?"PASS":"FAIL");
    return r==0;
}
static int run_pos(void){
    int all=1;
    { int S[4]={0,1,2,3};
      u32 inc[4]={ (1u<<4)|(1u<<5)|(1u<<6), (1u<<4)|(1u<<5)|(1u<<6),
                   (1u<<6)|(1u<<7),         (1u<<6)|(1u<<8) };
      all&=ctl("O-56",14,4,S,inc,10,11); }
    { int S[5]={0,1,2,3,4};
      u32 hwz=(1u<<7)|(1u<<8)|(1u<<9);
      u32 inc[5]={ (1u<<5)|(1u<<6)|(1u<<7), (1u<<5)|(1u<<6), hwz, hwz, hwz };
      all&=ctl("O-63",13,5,S,inc,11,12); }
    { int S[3]={0,1,2};
      u32 inc[3]={ (1u<<3)|(1u<<4)|(1u<<7), (1u<<3)|(1u<<4), (1u<<7)|(1u<<8) };
      all&=ctl("O-64",9,3,S,inc,7,6); }
    printf("POSITIVE CONTROL %s\n", all?"ALL PASS":"FAILURES PRESENT");
    return all?0:1;
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: f2 run < graph6 | f2 pos\n"); return 2; }
    if(!strcmp(argv[1],"pos")) return run_pos();
    if(strcmp(argv[1],"run")){ fprintf(stderr,"usage: f2 run < graph6 | f2 pos\n"); return 2; }
    char line[512];
    long ngraphs=0, n_inst=0, fail_inst=0, n_pairs=0, fail_someE=0, n_SF=0;
    FILE *wf=fopen("f2-witness.txt","w");
    clock_t t0=clock();

    while(fgets(line,sizeof line,stdin)){
        line[strcspn(line,"\n")]=0;
        if(!line[0]) continue;
        if(!decode_g6(line)){ fprintf(stderr,"HALT decode %s\n",line); return 3; }
        ngraphs++;
        u32 full=(1u<<N)-1;
        int bestF=0;
        for(u32 X=0;X<=full;X++){
            int pc=__builtin_popcount(X);
            if(pc<=bestF) continue;
            if(is_forest(X)) bestF=pc;
        }
        int tau=N-bestF;
        if(tau<2) continue;

        for(u32 Sm=0;Sm<=full;Sm++){
            if(__builtin_popcount(Sm)!=tau) continue;
            if(!is_forest(full^Sm)) continue;
            n_SF++;
            int Sv[MAXN]; K=0;
            for(int v=0;v<N;v++) if(Sm>>v&1) Sv[K++]=v;
            u32 Hm=full^Sm;
            int anyE=0, okE=0;

            for(int x=0;x<N;x++){ if(!(Hm>>x&1)) continue;
              u32 nb=adj[x]&Hm&~((1u<<x)-1);
              while(nb){
                int y=__builtin_ctz(nb); nb&=nb-1;
                anyE=1; n_inst++;
                for(int v=0;v<N;v++){ capv[v]=2; loadv[v]=0; uf[v]=v; }
                capv[x]=1; capv[y]=1;
                uftop=0;
                int bad=0;
                for(int i=0;i<K;i++){
                    nopt[i]=0;
                    u32 nh=adj[Sv[i]]&Hm;
                    for(int a=0;a<N;a++) if(nh>>a&1)
                        for(int b=a+1;b<N;b++) if(nh>>b&1){
                            if(nopt[i]<64){ optA[i][nopt[i]]=a; optB[i][nopt[i]]=b; nopt[i]++; }
                        }
                    if(nopt[i]==0) bad=1;
                }
                if(bad){ fail_inst++; fprintf(wf,"NO-OPTIONS %s S=%u e=(%d,%d)\n",line,Sm,x,y); continue; }
                /* most-constrained first */
                for(int i=0;i<K;i++) ordr[i]=i;
                for(int i=1;i<K;i++){ int t=ordr[i],j=i-1;
                    while(j>=0 && nopt[ordr[j]]>nopt[t]){ ordr[j+1]=ordr[j]; j--; }
                    ordr[j+1]=t; }
                if(solve(0)) okE++;
                else{
                    fail_inst++;
                    fprintf(wf,"F2-ALL-FAIL %s S=%u e=(%d,%d)\n",line,Sm,x,y);
                    fflush(wf);
                }
              }
            }
            if(anyE && okE==0){ fail_someE++;
                fprintf(wf,"F2-SOME-FAIL %s S=%u\n",line,Sm); fflush(wf); }
            n_pairs += anyE;
        }
    }
    double dt=(double)(clock()-t0)/CLOCKS_PER_SEC;
    fclose(wf);
    printf("=== F2 DIRECT SCAN ===\n");
    printf("graphs = %ld\n", ngraphs);
    printf("(G,S) pairs with tau>=2 = %ld\n", n_SF);
    printf("instances (G,S,e) = %ld\n", n_inst);
    printf("F2-ALL failures (instances with NO acyclic feasible selection) = %ld\n", fail_inst);
    printf("F2-SOME failures ((G,S) with no working e at all) = %ld\n", fail_someE);
    printf("runtime_sec = %.2f\n", dt);
    return 0;
}
