/* fcore.c — Lemma A oracle: is the forced incidence core acyclic?
 *
 * INDEPENDENT SECOND ENGINE for tools/forced_core.py.  forced_core.py decides
 * forcedness by enumerating EVERY feasible selection and intersecting them.
 * This program decides forcedness by the flow characterisation (paper Thm 3.10):
 * a selected incidence a is forced iff, after deleting a, the deficient vertex
 * admits no residual augmentation.  Algorithmically distinct; it shares no code.
 *
 * Output format deliberately mirrors tools/forced_core.py so the two can be
 * compared field by field:
 *   instances, cyclic cores, empty cores, non-forest cores, max forced-core
 *   path length, path-length histogram, component-size histogram.
 *
 * Model (paper Definition 3.1): G bipartite, S a MINIMUM feedback vertex set,
 * H = G - S (a forest), e = (x,y) a fixed edge of H.  Each s in S has demand 2;
 * c(h) = 2 except c(x) = c(y) = 1.  An instance is a triple (G, S, e); the scan
 * ranges over every minimum FVS and every H-edge, exactly as forced_core.py.
 *
 * Usage:  fcore gold | fcore run        (graph6 on stdin; use geng -bc -q N)
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

/* ---------- incidence-selection model ---------- */

static int K;                 /* |S| */
static int Sv[MAXN];          /* S vertices */
static u32 nbH[MAXN];         /* nbH[i] = H-neighbours of Sv[i], as a vertex mask */
static int cap[MAXN];         /* capacity per H vertex (indexed by vertex id) */
static u32 sel[MAXN];         /* sel[i] = chosen H-neighbours of Sv[i] */
static int load_[MAXN];       /* load per H vertex */
static u32 banned_s, banned_h;/* the single forbidden incidence, if any */

static u32 visH;

/* Kuhn-style augmentation for the b-matching: give Sv[i] one more incidence. */
static int try_aug(int i){
    u32 cand = nbH[i] & ~sel[i];
    while(cand){
        int h=__builtin_ctz(cand); cand&=cand-1;
        if(visH>>h&1) continue;
        if(banned_h==(u32)(1u<<h) && banned_s==(u32)(1u<<i)) continue;
        visH |= 1u<<h;
        if(load_[h] < cap[h]){ sel[i]|=1u<<h; load_[h]++; return 1; }
        for(int j=0;j<K;j++) if(j!=i && (sel[j]>>h&1)){
            sel[j] &= ~(1u<<h); load_[h]--;
            if(try_aug(j)){ sel[i]|=1u<<h; load_[h]++; return 1; }
            sel[j] |= 1u<<h; load_[h]++;
        }
    }
    return 0;
}

/* Build a feasible selection from scratch; return 1 on success. */
static int build_feasible(void){
    for(int i=0;i<K;i++) sel[i]=0;
    for(int v=0;v<N;v++) load_[v]=0;
    for(int i=0;i<K;i++) for(int r=0;r<2;r++){
        visH=0;
        if(!try_aug(i)) return 0;
    }
    return 1;
}

/* ---------- forced-core statistics (same fields as forced_core.py) ---------- */

static int fu_par[2*MAXN];
static int fu_find(int v){ while(fu_par[v]!=v){ fu_par[v]=fu_par[fu_par[v]]; v=fu_par[v]; } return v; }

/* ---------- positive control ----------------------------------------------
 * "0 cyclic cores" is only meaningful if the engine CAN report one.  The three
 * frozen warning witnesses (tools/witnesses/O-5{6,3,4}.json) each have a cyclic
 * forced core; they are not reachable from geng because their S is not a
 * minimum FVS, so they are supplied here explicitly.  The engine must report
 * cycle rank 1 and the recorded forced-core size on each.
 * Each control gives: K, the S-vertex list, the H-vertex mask, the incidence
 * lists, and the fixed edge.  Vertex ids are 0..N-1 as in the JSON (O-63/O-64
 * relabelled in the order their JSON lists them).                            */
static int control(const char*name,int n,int k,const int*Sl,const u32*inc,
                   int ex,int ey,int exp_forced,int exp_cyc){
    N=n; K=k;
    for(int i=0;i<k;i++){ Sv[i]=Sl[i]; nbH[i]=inc[i]; }
    for(int v=0;v<N;v++) cap[v]=2;
    cap[ex]=1; cap[ey]=1;
    banned_s=banned_h=0;
    if(!build_feasible()){ printf("  %-8s FAIL (no feasible selection)\n",name); return 0; }
    u32 base[MAXN]; int baseload[MAXN];
    for(int i=0;i<k;i++) base[i]=sel[i];
    for(int v=0;v<N;v++) baseload[v]=load_[v];
    int fe_i[2*MAXN], fe_h[2*MAXN], nfe=0;
    for(int i=0;i<k;i++){
        u32 m=base[i];
        while(m){
            int h=__builtin_ctz(m); m&=m-1;
            for(int q=0;q<k;q++) sel[q]=base[q];
            for(int v=0;v<N;v++) load_[v]=baseload[v];
            sel[i]&=~(1u<<h); load_[h]--;
            banned_s=1u<<i; banned_h=1u<<h; visH=0;
            int avoidable=try_aug(i);
            banned_s=banned_h=0;
            if(!avoidable){ fe_i[nfe]=i; fe_h[nfe]=h; nfe++; }
        }
    }
    int NV=k+N;
    for(int t=0;t<NV;t++) fu_par[t]=t;
    int cyc=0;
    for(int t=0;t<nfe;t++){
        int a=fu_find(fe_i[t]), b=fu_find(k+fe_h[t]);
        if(a==b) cyc++; else fu_par[a]=b;
    }
    int ok = (nfe==exp_forced) && (cyc==exp_cyc);
    printf("  %-8s |forced|=%d(exp %d) cycle_rank=%d(exp %d)  %s\n",
           name,nfe,exp_forced,cyc,exp_cyc, ok?"PASS":"FAIL");
    return ok;
}
static int run_pos(void){
    int all=1;
    /* O-56: S={0,1,2,3}; H={4..13}; 0,1~4,5,6 ; 2~6,7 ; 3~6,8 ; e=(10,11).
     * Forced core = all 8 incidences, containing the 4-cycle 0-4-1-5.        */
    { int S[4]={0,1,2,3};
      u32 inc[4]={ (1u<<4)|(1u<<5)|(1u<<6), (1u<<4)|(1u<<5)|(1u<<6),
                   (1u<<6)|(1u<<7),         (1u<<6)|(1u<<8) };
      all&=control("O-56",14,4,S,inc,10,11,8,1); }
    /* O-63: S={s,t,u,a,b}=0..4 ; H: q1=5,q2=6,h=7,w=8,z=9,r=10,x=11,y=12.
     * s~q1,q2,h ; t~q1,q2 ; u,a,b~h,w,z ; e=(x,y)=(11,12).                   */
    { int S[5]={0,1,2,3,4};
      u32 hwz=(1u<<7)|(1u<<8)|(1u<<9);
      u32 inc[5]={ (1u<<5)|(1u<<6)|(1u<<7), (1u<<5)|(1u<<6), hwz, hwz, hwz };
      all&=control("O-63",13,5,S,inc,11,12,4,1); }
    /* O-64: S={s,t,u}=0..2 ; H: q1=3,q2=4,r=5,y=6,h=7,w=8.
     * s~q1,q2,h ; t~q1,q2 ; u~h,w ; e=(h,y)=(7,6).                           */
    { int S[3]={0,1,2};
      u32 inc[3]={ (1u<<3)|(1u<<4)|(1u<<7), (1u<<3)|(1u<<4), (1u<<7)|(1u<<8) };
      all&=control("O-64",9,3,S,inc,7,6,6,1); }
    printf("POSITIVE CONTROL %s\n", all?"ALL PASS":"FAILURES PRESENT");
    return all?0:1;
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: fcore run < graph6 | fcore pos\n"); return 2; }
    if(!strcmp(argv[1],"pos")) return run_pos();
    if(strcmp(argv[1],"run")){ fprintf(stderr,"unknown mode\n"); return 2; }

    char line[512];
    long n_inst=0, cyclic_core=0, noforced=0, nonforest=0, infeasible=0;
    long ngraphs=0;
    int maxpath_over=0;
    long path_hist[64]; for(int i=0;i<64;i++) path_hist[i]=0;
    long comp_hist[64]; for(int i=0;i<64;i++) comp_hist[i]=0;
    FILE *wf=fopen("fcore-witness.txt","w");
    clock_t t0=clock();

    while(fgets(line,sizeof line,stdin)){
        line[strcspn(line,"\n")]=0;
        if(!line[0]) continue;
        if(!decode_g6(line)){ fprintf(stderr,"HALT decode fail %s\n",line); return 3; }
        ngraphs++;
        u32 full=(1u<<N)-1;

        /* tau = N - max induced forest; collect every minimum FVS in one scan */
        int bestF=0;
        for(u32 X=0;X<=full;X++){
            int pc=__builtin_popcount(X);
            if(pc<=bestF) continue;
            if(is_forest(X)) bestF=pc;
        }
        int tau=N-bestF;
        if(tau<2) continue;                     /* matches forced_core.py */

        for(u32 Sm=0;Sm<=full;Sm++){
            if(__builtin_popcount(Sm)!=tau) continue;
            if(!is_forest(full^Sm)) continue;   /* Sm is a minimum FVS */

            K=0;
            for(int v=0;v<N;v++) if(Sm>>v&1) Sv[K++]=v;
            u32 Hm=full^Sm;

            for(int x=0;x<N;x++){ if(!(Hm>>x&1)) continue;
              u32 nb=adj[x]&Hm&~((1u<<x)-1)&~(1u<<x);
              while(nb){
                int y=__builtin_ctz(nb); nb&=nb-1;     /* H-edge (x,y), x<y */

                for(int v=0;v<N;v++) cap[v]=2;
                cap[x]=1; cap[y]=1;
                int ok=1;
                for(int i=0;i<K;i++){
                    nbH[i]=adj[Sv[i]]&Hm;
                    if(__builtin_popcount(nbH[i])<2) ok=0;
                }
                banned_s=banned_h=0;
                if(!ok || !build_feasible()){ infeasible++; continue; }
                n_inst++;

                /* forced core: keep a copy of one feasible selection */
                u32 base[MAXN]; int baseload[MAXN];
                for(int i=0;i<K;i++) base[i]=sel[i];
                for(int v=0;v<N;v++) baseload[v]=load_[v];

                /* forced edges, stored as (i, h) pairs */
                int fe_i[2*MAXN], fe_h[2*MAXN], nfe=0;
                for(int i=0;i<K;i++){
                    u32 m=base[i];
                    while(m){
                        int h=__builtin_ctz(m); m&=m-1;
                        /* delete (Sv[i],h) and try to re-augment in N - a */
                        for(int q=0;q<K;q++) sel[q]=base[q];
                        for(int v=0;v<N;v++) load_[v]=baseload[v];
                        sel[i]&=~(1u<<h); load_[h]--;
                        banned_s=1u<<i; banned_h=1u<<h;
                        visH=0;
                        int avoidable=try_aug(i);
                        banned_s=banned_h=0;
                        if(!avoidable){ fe_i[nfe]=i; fe_h[nfe]=h; nfe++; }
                    }
                }
                for(int i=0;i<K;i++) sel[i]=base[i];
                for(int v=0;v<N;v++) load_[v]=baseload[v];

                if(nfe==0){ noforced++; comp_hist[0]++; continue; }

                /* cycle rank of the forced core (union-find over S-idx / H-vtx) */
                /* node ids: 0..K-1 for S vertices, K..K+N-1 for H vertices */
                int NV=K+N;
                for(int t=0;t<NV;t++) fu_par[t]=t;
                int cyc=0;
                for(int t=0;t<nfe;t++){
                    int a=fu_find(fe_i[t]), b=fu_find(K+fe_h[t]);
                    if(a==b) cyc++; else fu_par[a]=b;
                }
                if(cyc>0){
                    cyclic_core++; nonforest++;
                    fprintf(wf,"CYCLIC-FORCED-CORE %s S=%u e=(%d,%d) cyc=%d edges=",
                            line,Sm,x,y,cyc);
                    for(int t=0;t<nfe;t++) fprintf(wf," (%d,%d)",Sv[fe_i[t]],fe_h[t]);
                    fprintf(wf,"\n"); fflush(wf);
                    continue;
                }

                /* component sizes and tree diameter (forest case) */
                {
                    static int deg[2*MAXN]; static int nbr[2*MAXN][2*MAXN];
                    for(int t=0;t<NV;t++) deg[t]=0;
                    for(int t=0;t<nfe;t++){
                        int a=fe_i[t], b=K+fe_h[t];
                        nbr[a][deg[a]++]=b; nbr[b][deg[b]++]=a;
                    }
                    static char seen[2*MAXN];
                    for(int t=0;t<NV;t++) seen[t]=0;
                    int maxpath=0;
                    for(int t=0;t<NV;t++){
                        if(deg[t]==0||seen[t]) continue;
                        /* collect component */
                        int stack[2*MAXN], sp=0, comp[2*MAXN], nc=0;
                        stack[sp++]=t; seen[t]=1;
                        while(sp){ int u=stack[--sp]; comp[nc++]=u;
                            for(int q=0;q<deg[u];q++){ int w=nbr[u][q];
                                if(!seen[w]){ seen[w]=1; stack[sp++]=w; } } }
                        comp_hist[nc<64?nc:63]++;
                        /* double BFS for the diameter */
                        int dist[2*MAXN];
                        int far=comp[0];
                        for(int pass=0;pass<2;pass++){
                            for(int q=0;q<nc;q++) dist[comp[q]]=-1;
                            int qq[2*MAXN], head=0, tail=0;
                            dist[far]=0; qq[tail++]=far;
                            while(head<tail){ int u=qq[head++];
                                for(int q=0;q<deg[u];q++){ int w=nbr[u][q];
                                    if(dist[w]<0){ dist[w]=dist[u]+1; qq[tail++]=w;
                                        if(dist[w]>dist[far]) far=w; } } }
                            if(pass==1 && dist[far]>maxpath) maxpath=dist[far];
                        }
                    }
                    if(maxpath>maxpath_over) maxpath_over=maxpath;
                    path_hist[maxpath<64?maxpath:63]++;
                }
              }
            }
        }
    }
    double dt=(double)(clock()-t0)/CLOCKS_PER_SEC;
    fclose(wf);
    printf("=== FORCED-CORE (Lemma A, flow engine) ===\n");
    printf("graphs = %ld\n", ngraphs);
    printf("instances = %ld\n", n_inst);
    printf("CYCLIC forced core (= Lemma A FAILS) = %ld\n", cyclic_core);
    printf("instances with empty forced core = %ld\n", noforced);
    printf("non-forest forced cores = %ld\n", nonforest);
    printf("infeasible (G,S,e) skipped = %ld\n", infeasible);
    printf("max forced-core path length (edges) over acyclic cores = %d\n", maxpath_over);
    printf("forced-core path-length histogram = {");
    { int first=1; for(int i=0;i<64;i++) if(path_hist[i]){ printf("%s%d: %ld",first?"":", ",i,path_hist[i]); first=0; } }
    printf("}\n");
    printf("forced-core component-size histogram = {");
    { int first=1; for(int i=0;i<64;i++) if(comp_hist[i]){ printf("%s%d: %ld",first?"":", ",i,comp_hist[i]); first=0; } }
    printf("}\n");
    printf("runtime_sec = %.2f\n", dt);
    return 0;
}
