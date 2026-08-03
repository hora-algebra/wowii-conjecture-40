/* PHASE0 primary engine — WOWII Conjecture 40 close-out.
 * Exact f(G)=max induced forest, b(G)=max induced bipartite, p(G)=min path cover
 * (n - max spanning linear forest edges) for n<=11.
 * Modes:
 *   gold                    : run built-in gold tests, print PASS/FAIL.
 *   run1                    : read graph6 lines (n=10) from stdin; check
 *                             p+b+1 <= 2f; report counts, min slack, violations,
 *                             low-slack (slack<=1) g6 -> lowslack file, and a
 *                             deterministic sample -> sample file.
 *   run2                    : read graph6 (connected nonbipartite, 3<=n<=9) from
 *                             stdin; SV check.
 *   bench <k>               : run1-style on first k lines, print throughput.
 * Invariants computed exactly; no heuristics.
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
    if(N<1||N>11) return 0;
    for(int i=0;i<N;i++) adj[i]=0;
    int cur=0, have=0;
    for(int j=1;j<N;j++) for(int i=0;i<j;i++){
        if(have==0){ cur=s[idx++]-63; have=6; }
        int b=(cur>>(have-1))&1; have--;
        if(b){ adj[i]|=(1u<<j); adj[j]|=(1u<<i); }
    }
    return 1;
}

/* forest test on induced subgraph S via union-find */
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
static u32 gF, gB; /* witnessing subsets (for violation reports) */
static int compute_f(void){
    int best=0, M=1<<N; u32 bs=0;
    for(u32 S=0;S<(u32)M;S++){
        int pc=__builtin_popcount(S);
        if(pc<=best) continue;
        if(is_forest(S)){ best=pc; bs=S; }
    }
    gF=bs; return best;
}
static int compute_b(void){
    int best=0, M=1<<N; u32 bs=0;
    for(u32 S=0;S<(u32)M;S++){
        int pc=__builtin_popcount(S);
        if(pc<=best) continue;
        if(is_bip(S)){ best=pc; bs=S; }
    }
    gB=bs; return best;
}
/* min path cover = n - max spanning linear forest edges, via ham+dp */
static char ham[1<<11][11];
static char pathset[1<<11];
static int dpc[1<<11];
static int compute_p(void){
    int M=1<<N, full=M-1;
    for(int mask=0;mask<M;mask++){ pathset[mask]=0; for(int v=0;v<N;v++) ham[mask][v]=0; }
    for(int v=0;v<N;v++){ ham[1<<v][v]=1; pathset[1<<v]=1; }
    for(int mask=1;mask<M;mask++){
        if(__builtin_popcount(mask)<2) continue;
        char any=0;
        for(int v=0;v<N;v++) if(mask>>v&1){
            u32 prev=mask^(1u<<v);
            u32 cand=adj[v]&prev;
            char ok=0;
            while(cand){ int u=__builtin_ctz(cand); cand&=cand-1; if(ham[prev][u]){ok=1;break;} }
            ham[mask][v]=ok; if(ok) any=1;
        }
        pathset[mask]=any;
    }
    for(int mask=0;mask<M;mask++) dpc[mask]=99;
    dpc[0]=0;
    for(int mask=1;mask<M;mask++){
        int best=99;
        for(int sub=mask; sub; sub=(sub-1)&mask){
            if(pathset[sub]){ int c=dpc[mask^sub]+1; if(c<best) best=c; }
        }
        dpc[mask]=best;
    }
    return dpc[full];
}
static int oct(void){ return N - compute_b(); } /* min odd-cycle transversal */

/* ---- gold graph constructors ---- */
static void clearG(int n){ N=n; for(int i=0;i<n;i++) adj[i]=0; }
static void addE(int i,int j){ adj[i]|=(1u<<j); adj[j]|=(1u<<i); }
static void complete_multipartite(int nparts,int *sizes){
    int n=0; for(int k=0;k<nparts;k++) n+=sizes[k];
    clearG(n);
    int base[16], off=0;
    for(int k=0;k<nparts;k++){ base[k]=off; off+=sizes[k]; }
    for(int a=0;a<nparts;a++) for(int b=a+1;b<nparts;b++)
        for(int i=0;i<sizes[a];i++) for(int j=0;j<sizes[b];j++)
            addE(base[a]+i, base[b]+j);
}
static void cycle(int n){ clearG(n); for(int i=0;i<n;i++) addE(i,(i+1)%n); }

static int goldcase(const char*name,int ef,int eb,int ep){
    int f=compute_f(), b=compute_b(), p=compute_p();
    int ok = (f==ef && b==eb && p==ep);
    printf("  %-14s n=%2d  f=%d(exp %d) b=%d(exp %d) p=%d(exp %d)  %s\n",
           name,N,f,ef,b,eb,p,ep,ok?"PASS":"FAIL");
    return ok;
}
static int run_gold(void){
    int all=1, s[16];
    /* K_10 = complete graph = 10 parts of size 1 */
    for(int i=0;i<10;i++) s[i]=1; complete_multipartite(10,s); all&=goldcase("K_10",2,2,1);
    /* K_5,5 */ s[0]=5;s[1]=5; complete_multipartite(2,s); all&=goldcase("K_5,5",6,10,1);
    /* K_1,9 star */ s[0]=1;s[1]=9; complete_multipartite(2,s); all&=goldcase("K_1,9",10,10,8);
    /* stars K_1,m: p=m-1,b=f=m+1 */
    for(int m=2;m<=4;m++){ s[0]=1;s[1]=m; complete_multipartite(2,s);
        char nm[16]; snprintf(nm,16,"K_1,%d",m); all&=goldcase(nm,m+1,m+1,m-1); }
    /* K_3,3 */ s[0]=3;s[1]=3; complete_multipartite(2,s); all&=goldcase("K_3,3",4,6,1);
    /* K_2,2,2 octahedron */ s[0]=2;s[1]=2;s[2]=2; complete_multipartite(3,s); all&=goldcase("K_2,2,2",3,4,1);
    /* K_2,2,3 */ s[0]=2;s[1]=2;s[2]=3; complete_multipartite(3,s); all&=goldcase("K_2,2,3",4,5,1);
    /* K_1,1,1,3 */ s[0]=1;s[1]=1;s[2]=1;s[3]=3; complete_multipartite(4,s); all&=goldcase("K_1,1,1,3",4,4,1);
    /* C_10 */ cycle(10); all&=goldcase("C_10",9,10,1);
    printf("GOLD %s\n", all?"ALL PASS":"FAILURES PRESENT");
    return all?0:1;
}

/* SV evaluation on current global graph (assumed connected nonbipartite).
 * Returns: 1 PASS, 0 FAIL, -1 empty-Elig (engine bug). Fills out-params. */
static int sv_eval(int verbose,int*poG,int*ppG,int*pelig,int*pminGain,int*pbug){
    u32 full[16]; int fn=N; for(int i=0;i<fn;i++) full[i]=adj[i];
    int oG=oct(); int pG=compute_p();
    int elig=0,pass=0,minGain=99,bug=0,eligmask=0;
    for(int t=0;t<fn;t++){
        int map[16],m=0; for(int i=0;i<fn;i++) if(i!=t) map[i]=m++;
        N=fn-1; for(int i=0;i<N;i++) adj[i]=0;
        for(int i=0;i<fn;i++) if(i!=t){ u32 nb=full[i];
            while(nb){ int j=__builtin_ctz(nb); nb&=nb-1; if(j!=t && i<j) addE(map[i],map[j]); } }
        int oGt=oct();
        if(oGt==oG-1){ elig++; eligmask|=(1<<t); int pGt=compute_p();
            int gain=pGt-pG; if(gain<-1) bug++; if(gain>=0) pass=1; if(gain<minGain) minGain=gain;
            if(verbose) printf("    t=%d eligible: o(G-t)=%d p(G-t)=%d gain=%d\n",t,oGt,pGt,gain);
        }
        N=fn; for(int i=0;i<fn;i++) adj[i]=full[i];
    }
    if(poG)*poG=oG; if(ppG)*ppG=pG; if(pelig)*pelig=elig; if(pminGain)*pminGain=minGain; if(pbug)*pbug=bug;
    if(verbose) printf("    o(G)=%d p(G)=%d Elig=%d(mask %d) -> %s\n",oG,pG,elig,eligmask,pass?"PASS":"FAIL");
    return (elig==0)?-1:pass;
}
static int sv_gold(const char*name,int exp_o,int exp_elig){
    int oG,pG,elig,mg,bug; int r=sv_eval(0,&oG,&pG,&elig,&mg,&bug);
    int ok = (r==1) && (oG==exp_o) && (elig==exp_elig) && bug==0;
    printf("  %-22s o=%d(exp %d) Elig=%d(exp %d) pass=%d bug=%d  %s\n",
           name,oG,exp_o,elig,exp_elig,r==1,bug,ok?"PASS":"FAIL");
    return ok;
}
static int run_gold2(void){
    int all=1,s[16];
    for(int i=0;i<5;i++) s[i]=1; complete_multipartite(5,s); all&=sv_gold("K_5",3,5); /* o(K_5)=n-2=3 */
    cycle(5); all&=sv_gold("C_5",1,5);
    cycle(7); all&=sv_gold("C_7",1,7);
    s[0]=1;s[1]=1;s[2]=1;s[3]=3; complete_multipartite(4,s); all&=sv_gold("K_1,1,1,3",2,3);
    s[0]=1;s[1]=2;s[2]=4; complete_multipartite(3,s); all&=sv_gold("K_1,2,4",1,1);
    /* triangle {0,1,2} + pendant path 2-3-4 */
    clearG(5); addE(0,1);addE(1,2);addE(0,2); addE(2,3);addE(3,4); all&=sv_gold("tri+pendant",1,3);
    printf("GOLD2 (SV) %s\n", all?"ALL PASS":"FAILURES PRESENT");
    return all?0:1;
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: phase0 gold|run1|run2|bench k\n"); return 2; }
    if(!strcmp(argv[1],"gold")) return run_gold();
    if(!strcmp(argv[1],"gold2")) return run_gold2();
    if(!strcmp(argv[1],"reg")){ /* regression: any-n connected graphs, check bound */
        char line[256]; long cnt=0, viol=0;
        while(fgets(line,sizeof line,stdin)){
            line[strcspn(line,"\n")]=0; if(!line[0]) continue;
            if(!decode_g6(line)){ fprintf(stderr,"decode fail\n"); return 3; }
            int f=compute_f(), b=compute_b(), p=compute_p();
            if(2*f-(p+b+1)<0){ viol++; fprintf(stderr,"VIOL %s f=%d b=%d p=%d\n",line,f,b,p); }
            cnt++;
        }
        printf("REG: graphs=%ld violations=%ld\n",cnt,viol);
        return 0;
    }
    if(!strcmp(argv[1],"bench")){
        long k = argc>2?atol(argv[2]):100000;
        char line[256]; long cnt=0; clock_t t0=clock();
        while(cnt<k && fgets(line,sizeof line,stdin)){
            line[strcspn(line,"\n")]=0; if(!line[0]) continue;
            if(!decode_g6(line)){ fprintf(stderr,"decode fail\n"); return 3; }
            (void)compute_f(); (void)compute_b(); (void)compute_p(); cnt++;
        }
        double dt=(double)(clock()-t0)/CLOCKS_PER_SEC;
        printf("bench: %ld graphs (n=%d) in %.2fs -> %.0f graphs/sec\n",cnt,N,dt,cnt/dt);
        return 0;
    }
    if(!strcmp(argv[1],"run1")){
        /* run1 <shard-id> <sample-every> : sharded sweep, any n, per-shard accounting */
        const char* shard = argc>2?argv[2]:"0";
        long SAMPLE_EVERY = argc>3?atol(argv[3]):100000;
        const char* R=getenv("PHASE0_OUT"); if(!R) R=".";  /* output dir; default cwd */
        char pL[320],pS[320],pV[320],pC[320],pH[320];
        snprintf(pL,320,"%s/phase0-n11-lowslack-%s.txt",R,shard);
        snprintf(pS,320,"%s/phase0-n11-sample-%s.txt",R,shard);
        snprintf(pV,320,"%s/phase0-n11-VIOL-%s.txt",R,shard);
        snprintf(pC,320,"%s/phase0-n11-count-%s.txt",R,shard);
        snprintf(pH,320,"%s/phase0-n11-HALT",R);
        FILE *lf=fopen(pL,"w"), *sf=fopen(pS,"w"), *vf=fopen(pV,"w");
        char line[256]; long cnt=0, viol=0, lowc=0; int minslack=999;
        long start=(long)time(0);
        while(fgets(line,sizeof line,stdin)){
            line[strcspn(line,"\n")]=0; if(!line[0]) continue;
            if(!decode_g6(line)){ fprintf(stderr,"HALT: decode fail shard %s at %ld\n",shard,cnt); return 3; }
            int f=compute_f(), b=compute_b(), p=compute_p();
            int slack = 2*f - (p+b+1);
            cnt++;
            if(slack<minslack) minslack=slack;
            if(slack<0){
                viol++;
                fprintf(vf,"%s f=%d b=%d p=%d slack=%d forestset=%u bipset=%u\n",line,f,b,p,slack,gF,gB);
                fflush(vf);
                FILE*hf=fopen(pH,"w"); if(hf){ fprintf(hf,"VIOLATION shard=%s %s f=%d b=%d p=%d\n",shard,line,f,b,p); fclose(hf); }
                FILE*c=fopen(pC,"w"); fprintf(c,"shard=%s count=%ld violations=%ld min_slack=%d lowslack=%ld status=VIOLATION_HALT start=%ld finish=%ld\n",shard,cnt,viol,minslack,lowc,start,(long)time(0)); fclose(c);
                fclose(lf);fclose(sf);fclose(vf);
                return 42;
            }
            if(slack<=1){ lowc++; fprintf(lf,"%s %d\n",line,slack); }
            if(cnt%SAMPLE_EVERY==0) fprintf(sf,"%s\n",line);
            if(cnt%1000000==0){ FILE*h=fopen(pH,"r"); if(h){ fclose(h);
                FILE*c=fopen(pC,"w"); fprintf(c,"shard=%s count=%ld violations=%ld min_slack=%d lowslack=%ld status=HALTED start=%ld finish=%ld\n",shard,cnt,viol,minslack,lowc,start,(long)time(0)); fclose(c);
                fclose(lf);fclose(sf);fclose(vf); return 43; } }
        }
        fclose(lf);fclose(sf);fclose(vf);
        FILE*c=fopen(pC,"w"); fprintf(c,"shard=%s count=%ld violations=%ld min_slack=%d lowslack=%ld status=DONE start=%ld finish=%ld\n",shard,cnt,viol,minslack,lowc,start,(long)time(0)); fclose(c);
        printf("shard %s DONE: count=%ld viol=%ld minslack=%d lowslack=%ld\n",shard,cnt,viol,minslack,lowc);
        return 0;
    }
    if(!strcmp(argv[1],"run2")){
        const char* R2=getenv("PHASE0_OUT"); if(!R2) R2=".";
        char pV2[320]; snprintf(pV2,320,"%s/phase0-run2-VIOL.txt",R2);
        FILE *vf=fopen(pV2,"w");
        char line[256]; long cnt=0, viol=0, bugct=0;
        clock_t t0=clock();
        while(fgets(line,sizeof line,stdin)){
            line[strcspn(line,"\n")]=0; if(!line[0]) continue;
            if(!decode_g6(line)){ fprintf(stderr,"HALT: decode fail\n"); return 3; }
            /* connected assumed (geng -c); require nonbipartite */
            if(compute_b()==N) continue; /* bipartite -> skip (not in SV universe) */
            int oG,pG,elig,minGain,bug;
            int r = sv_eval(0,&oG,&pG,&elig,&minGain,&bug);
            bugct += bug;
            cnt++;
            if(r==-1){ fprintf(stderr,"HALT(bug): empty Elig for nonbipartite %s\n",line); return 5; }
            if(r==0){ viol++; fprintf(vf,"%s oG=%d pG=%d elig=%d minGain=%d\n",line,oG,pG,elig,minGain); fflush(vf); }
            if(cnt%50000==0) fprintf(stderr,"[run2] %ld graphs viol=%ld\n",cnt,viol);
        }
        double dt=(double)(clock()-t0)/CLOCKS_PER_SEC;
        fclose(vf);
        printf("RUN2 DONE: graphs=%ld violations=%ld p_drop_bugs=%ld runtime_sec=%.1f\n",cnt,viol,bugct,dt);
        return 0;
    }
    fprintf(stderr,"unknown mode\n"); return 2;
}
