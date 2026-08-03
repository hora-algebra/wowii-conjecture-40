/* lift.c — checker for the lifting inequality (ATTACK.md target 4).
 *
 * Frozen per PREREG-LIFT.md.  Invariant primitives (decode_g6, is_forest,
 * is_bip, the ham/dpc path-cover DP) are taken from the project's frozen engine
 * verification/phase0.c so that f, b, p agree with the oracle by construction.
 *
 * Modes:
 *   gold            run the built-in gold suite, print PASS/FAIL
 *   run             read graph6 lines from stdin, test the frozen statements
 *   bench <k>       throughput measurement on the first k lines
 *
 * Statements tested per connected nonbipartite G (see PREREG-LIFT.md):
 *   LIFT-A      exists min OCT T : ell(G) >= 2*tau(G-T) + |T| + 1
 *   LIFT-A-ALL  the same for every min OCT T
 *   LIFT-P      exists min OCT T : p(G) <= p(G-T)
 *   LIFT-P-ALL  the same for every min OCT T
 *   SV          exists vertex t : o(G-t) = o(G)-1 and p(G) <= p(G-t)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned int u32;
static int N;
static u32 adj[16];

static int decode_g6(const char *s){
    int idx=0;
    N = s[idx++]-63;
    if(N<1||N>12) return 0;
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
    int parent[16];
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
static int is_bip(u32 S){
    int color[16]; for(int i=0;i<N;i++) color[i]=-1;
    int stack[16];
    for(int st=0;st<N;st++) if((S>>st&1) && color[st]<0){
        int sp=0; stack[sp++]=st; color[st]=0;
        while(sp){ int u=stack[--sp]; u32 nb=adj[u]&S;
            while(nb){ int v=__builtin_ctz(nb); nb&=nb-1;
                if(color[v]<0){ color[v]=color[u]^1; stack[sp++]=v; }
                else if(color[v]==color[u]) return 0;
            }
        }
    }
    return 1;
}

/* max induced forest / bipartite within the induced subgraph on `univ` */
static int max_forest_in(u32 univ){
    int best=0;
    for(u32 S=univ;; S=(S-1)&univ){
        int pc=__builtin_popcount(S);
        if(pc>best && is_forest(S)) best=pc;
        if(S==0) break;
    }
    return best;
}
static int max_bip_in(u32 univ){
    int best=0;
    for(u32 S=univ;; S=(S-1)&univ){
        int pc=__builtin_popcount(S);
        if(pc>best && is_bip(S)) best=pc;
        if(S==0) break;
    }
    return best;
}

/* min path cover of the induced subgraph on `univ`, over the full index range.
 * Identical algorithm to phase0.c compute_p, restricted to a vertex subset. */
static char hamv[1<<12][12];
static char pathset[1<<12];
static short dpc[1<<12];
static int path_cover_in(u32 univ){
    u32 M=1u<<N;
    /* Masks are enumerated ASCENDING and non-subsets of univ skipped, so that
     * every state is computed after all its proper subsets (the ham DP needs
     * ham[mask \ v], the cover DP needs dpc[mask ^ sub]). */
    for(u32 mask=0; mask<M; mask++){
        if(mask & ~univ) continue;
        if(__builtin_popcount(mask)==1){
            int v=__builtin_ctz(mask);
            hamv[mask][v]=1; pathset[mask]=1;
            continue;
        }
        char any=0;
        for(int v=0;v<N;v++){
            if(!(mask>>v&1)){ hamv[mask][v]=0; continue; }
            u32 prev=mask^(1u<<v);
            u32 cand=adj[v]&prev;
            char ok=0;
            while(cand){ int u=__builtin_ctz(cand); cand&=cand-1;
                         if(hamv[prev][u]){ok=1;break;} }
            hamv[mask][v]=ok; if(ok) any=1;
        }
        pathset[mask]=any;
    }
    dpc[0]=0;
    for(u32 mask=1; mask<M; mask++){
        if(mask & ~univ) continue;
        int best=999;
        for(u32 sub=mask; sub; sub=(sub-1)&mask){
            if(pathset[sub]){ int c=dpc[mask^sub]+1; if(c<best) best=c; }
        }
        dpc[mask]=(short)best;
    }
    return dpc[univ];
}

/* ---------------- the lifting tests ---------------- */

typedef struct {
    int n, o, ell, p;
    int nOCT;                 /* number of minimum OCTs */
    int liftA, liftA_all;     /* 1 = holds */
    int liftP, liftP_all;
    int bestA;                /* max_T [ ell - 2 tau(G-T) - |T| - 1 ] */
    int sv;                   /* 1 = holds, -1 = no eligible vertex (bug) */
    int consistency_fail;
    u32 firstBadT;            /* a min OCT failing LIFT-A (if any) */
} Res;

static int eval(Res *r){
    u32 full=(1u<<N)-1;
    int b=max_bip_in(full);
    int o=N-b;
    int pG=path_cover_in(full);
    r->n=N; r->o=o; r->p=pG; r->ell=N-pG;
    r->nOCT=0; r->liftA=0; r->liftA_all=1; r->liftP=0; r->liftP_all=1;
    r->bestA=-999; r->consistency_fail=0; r->firstBadT=0;
    if(o==0) return 0;                      /* bipartite: outside the universe */

    for(u32 T=0;T<=full;T++){
        if(__builtin_popcount(T)!=o) continue;
        u32 rest=full^T;
        if(!is_bip(rest)) continue;         /* not an OCT */
        r->nOCT++;
        int tauB=(N-o)-max_forest_in(rest);
        int a = r->ell - (2*tauB + o + 1);
        if(a>r->bestA) r->bestA=a;
        if(a>=0) r->liftA=1;
        else { r->liftA_all=0; if(!r->firstBadT) r->firstBadT=T; }
        int pB=path_cover_in(rest);
        if(pG<=pB) r->liftP=1; else r->liftP_all=0;
        /* internal consistency: ell(G) = ell(G-T) + |T| + (p(G-T) - p(G)) */
        int ellB=(N-o)-pB;
        if(r->ell != ellB + o + (pB - pG)) r->consistency_fail=1;
    }
    /* SV */
    {
        u32 saved[16]; int fn=N;
        for(int i=0;i<fn;i++) saved[i]=adj[i];
        int elig=0, pass=0;
        for(int t=0;t<fn;t++){
            int map[16], m=0;
            for(int i=0;i<fn;i++) if(i!=t) map[i]=m++;
            N=fn-1; for(int i=0;i<N;i++) adj[i]=0;
            for(int i=0;i<fn;i++) if(i!=t){
                u32 nb=saved[i];
                while(nb){ int j=__builtin_ctz(nb); nb&=nb-1;
                    if(j!=t && i<j){ adj[map[i]]|=(1u<<map[j]); adj[map[j]]|=(1u<<map[i]); } }
            }
            u32 fl=(1u<<N)-1;
            int oGt=N-max_bip_in(fl);
            if(oGt==o-1){ elig++; if(path_cover_in(fl)>=pG) pass=1; }
            N=fn; for(int i=0;i<fn;i++) adj[i]=saved[i];
        }
        r->sv = (elig==0)?-1:pass;
    }
    return 1;
}

/* ---------------- gold ---------------- */
static void clearG(int n){ N=n; for(int i=0;i<n;i++) adj[i]=0; }
static void addE(int i,int j){ adj[i]|=(1u<<j); adj[j]|=(1u<<i); }
static void cycle(int n){ clearG(n); for(int i=0;i<n;i++) addE(i,(i+1)%n); }
static void complete_multipartite(int np,int*sz){
    int n=0; for(int k=0;k<np;k++) n+=sz[k];
    clearG(n);
    int base[16], off=0;
    for(int k=0;k<np;k++){ base[k]=off; off+=sz[k]; }
    for(int a=0;a<np;a++) for(int c=a+1;c<np;c++)
        for(int i=0;i<sz[a];i++) for(int j=0;j<sz[c];j++) addE(base[a]+i,base[c]+j);
}

static int gold_one(const char*nm,int eo,int eell,int eslack,int enOCT){
    Res r; eval(&r);
    int ok = (r.o==eo) && (r.ell==eell) && (r.bestA==eslack)
             && (enOCT<0 || r.nOCT==enOCT) && r.liftA==1 && r.consistency_fail==0;
    printf("  %-14s n=%2d o=%d(exp %d) ell=%d(exp %d) bestA=%d(exp %d) "
           "nOCT=%d(exp %d) liftA=%d liftP=%d  %s\n",
           nm,r.n,r.o,eo,r.ell,eell,r.bestA,eslack,r.nOCT,enOCT,
           r.liftA,r.liftP, ok?"PASS":"FAIL");
    return ok;
}
static int gold_fbp(const char*nm,int ef,int eb,int ep){
    u32 fl=(1u<<N)-1;
    int f=max_forest_in(fl), b=max_bip_in(fl), p=path_cover_in(fl);
    int ok=(f==ef&&b==eb&&p==ep);
    printf("  %-14s n=%2d f=%d(exp %d) b=%d(exp %d) p=%d(exp %d)  %s\n",
           nm,N,f,ef,b,eb,p,ep, ok?"PASS":"FAIL");
    return ok;
}
static int run_gold(void){
    int all=1,s[16];
    for(int i=0;i<3;i++) s[i]=1; complete_multipartite(3,s); all&=gold_one("K_3",1,2,0,3);
    for(int i=0;i<4;i++) s[i]=1; complete_multipartite(4,s); all&=gold_one("K_4",2,3,0,6);
    for(int i=0;i<5;i++) s[i]=1; complete_multipartite(5,s); all&=gold_one("K_5",3,4,0,10);
    cycle(5); all&=gold_one("C_5",1,4,2,5);
    cycle(7); all&=gold_one("C_7",1,6,4,7);
    /* bowtie: triangles 0-1-2 and 2-3-4 sharing vertex 2 */
    clearG(5); addE(0,1);addE(1,2);addE(0,2);addE(2,3);addE(3,4);addE(2,4);
    all&=gold_one("bowtie",1,4,2,1);
    /* phase0 cross-checks on (f,b,p) */
    s[0]=2;s[1]=2;s[2]=2; complete_multipartite(3,s); all&=gold_fbp("K_2,2,2",3,4,1);
    s[0]=1;s[1]=1;s[2]=1;s[3]=3; complete_multipartite(4,s); all&=gold_fbp("K_1,1,1,3",4,4,1);
    for(int i=0;i<10;i++) s[i]=1; complete_multipartite(10,s); all&=gold_fbp("K_10",2,2,1);
    s[0]=5;s[1]=5; complete_multipartite(2,s); all&=gold_fbp("K_5,5",6,10,1);
    s[0]=1;s[1]=9; complete_multipartite(2,s); all&=gold_fbp("K_1,9",10,10,8);
    cycle(10); all&=gold_fbp("C_10",9,10,1);
    printf("GOLD %s\n", all?"ALL PASS":"FAILURES PRESENT");
    return all?0:1;
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: lift gold|run|bench k\n"); return 2; }
    if(!strcmp(argv[1],"gold")) return run_gold();

    long k = (!strcmp(argv[1],"bench") && argc>2) ? atol(argv[2]) : -1;
    int bench = !strcmp(argv[1],"bench");

    char line[512];
    long tot=0, nonbip=0;
    long fA=0,fAall=0,fP=0,fPall=0,fSV=0,cons=0,svbug=0;
    int maxOCT=0;
    long slackhist[64]; for(int i=0;i<64;i++) slackhist[i]=0;
    long slackbig=0;
    FILE *wf=fopen("lift-witness.txt","w");
    clock_t t0=clock();
    while(fgets(line,sizeof line,stdin)){
        line[strcspn(line,"\n")]=0;
        if(!line[0]) continue;
        if(!decode_g6(line)){ fprintf(stderr,"HALT decode fail: %s\n",line); return 3; }
        tot++;
        Res r;
        if(!eval(&r)) continue;   /* bipartite */
        nonbip++;
        if(r.nOCT>maxOCT) maxOCT=r.nOCT;
        if(r.consistency_fail){ cons++;
            fprintf(wf,"CONSISTENCY %s\n",line); }
        if(!r.liftA){
            fA++;
            fprintf(wf,"LIFT-A-FAIL %s n=%d o=%d ell=%d p=%d nOCT=%d bestA=%d\n",
                    line,r.n,r.o,r.ell,r.p,r.nOCT,r.bestA);
            fflush(wf);
            printf("*** LIFT-A FALSIFIED at %s (n=%d o=%d ell=%d bestA=%d) — HALTING\n",
                   line,r.n,r.o,r.ell,r.bestA);
            fclose(wf);
            return 42;
        }
        if(!r.liftA_all){ if(fAall==0) fprintf(wf,"LIFT-A-ALL-FAIL(first) %s n=%d o=%d ell=%d T=%u\n",
                                               line,r.n,r.o,r.ell,r.firstBadT);
                          fAall++; }
        if(!r.liftP){ if(fP==0) fprintf(wf,"LIFT-P-FAIL(first) %s n=%d o=%d p=%d nOCT=%d\n",
                                        line,r.n,r.o,r.p,r.nOCT);
                      fP++; }
        if(!r.liftP_all){ if(fPall==0) fprintf(wf,"LIFT-P-ALL-FAIL(first) %s n=%d o=%d p=%d\n",
                                               line,r.n,r.o,r.p);
                          fPall++; }
        if(r.sv==-1){ svbug++; fprintf(wf,"SV-EMPTY-ELIG %s\n",line); }
        else if(r.sv==0){ if(fSV==0) fprintf(wf,"SV-FAIL(first) %s n=%d o=%d p=%d\n",line,r.n,r.o,r.p);
                          fSV++; }
        if(r.bestA>=0 && r.bestA<64) slackhist[r.bestA]++; else slackbig++;
        if(bench && tot>=k) break;
    }
    double dt=(double)(clock()-t0)/CLOCKS_PER_SEC;
    fclose(wf);
    printf("DONE graphs=%ld nonbipartite=%ld  LIFT-A_fail=%ld LIFT-A-ALL_fail=%ld "
           "LIFT-P_fail=%ld LIFT-P-ALL_fail=%ld SV_fail=%ld SV_emptyelig=%ld "
           "consistency_fail=%ld maxminOCTs=%d time=%.2fs (%.0f g/s)\n",
           tot,nonbip,fA,fAall,fP,fPall,fSV,svbug,cons,maxOCT,dt,tot/(dt>0?dt:1));
    printf("bestA slack histogram:");
    for(int i=0;i<64;i++) if(slackhist[i]) printf(" %d:%ld",i,slackhist[i]);
    if(slackbig) printf(" >=64:%ld",slackbig);
    printf("\n");
    return 0;
}
