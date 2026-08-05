/* maint_census.c — C port of the l6scan.py condition test + e1scan.py excess
 * test, for the maint/2026-08-census runs.
 *
 * Definitions ported 1:1 from the frozen Python checkers
 * (l6scan.py sha256 2e568740..., e1scan.py sha256 11dc5f28...):
 *   c_e, i, M, Delta, r  per bipartite remainder as in PREREG-L6-N9.md
 *   g(C) = FE(C) - max class size, FE = largest induced forest containing
 *          one full color class (both orientations tried)
 *   S1 fail: NO minimum OCT with p <= 2c_e + Delta + 2r - 1
 *   S2 fail: NO minimum OCT with p <= Delta + 2g - 1
 *   S3 fail: NO minimum OCT with ell >= 2 tau(B) + o + 1
 *   tight  : best exact slack over minimum OCTs == 0
 *   excess(C) = |a-b| + 2 g(C) - p(C)   (connected bipartite C)
 *
 * Modes:
 *   ./maint_census cond    < graph6-lines   (connected graphs; skips bipartite)
 *   ./maint_census excess  < graph6-lines   (connected bipartite graphs)
 *
 * Output (cond): tally line "COND connected=%llu nonbip=%llu s1=%llu s2=%llu
 *   s3=%llu l6not5=%llu tight=%llu"; per-failure lines "S1FAIL/S2FAIL/S3FAIL
 *   <g6> p=%d o=%d [per-OCT tuples]"; tight graph6 lines to fd 3 if open.
 * Output (excess): histogram + "E0WIT <g6> a=%d b=%d p=%d g=%d excess=%d"
 *   for every excess <= 0 witness; tally "EXC graphs=%llu min_excess=%d".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 16

static int n;                 /* current graph order */
static int adj[MAXN];         /* adjacency bitmasks */

static int parse_g6(const char *s) {
    int len = (int)strlen(s);
    if (len < 1) return 0;
    n = s[0] - 63;
    if (n < 1 || n > 15) return 0;
    memset(adj, 0, sizeof adj);
    int need = n * (n - 1) / 2, bit = 0;
    for (int c = 1; bit < need; c++) {
        if (c >= len) return 0;
        int v = s[c] - 63;
        for (int k = 5; k >= 0 && bit < need; k--, bit++) {
            if (v >> k & 1) {
                /* colex order: bit index -> pair (i,j), j = column */
                int b = bit, j = 1;
                while (b >= j) { b -= j; j++; }
                adj[b] |= 1 << j;
                adj[j] |= 1 << b;
            }
        }
    }
    return 1;
}

/* 2-coloring of induced subgraph on mask; returns 1 if bipartite and sets
 * *col1 = vertices colored 1 (subset of mask). Also usable as bipartite test. */
static int two_color(int mask, int *col1) {
    int seen = 0, c1 = 0;
    while (1) {
        int rest = mask & ~seen;
        if (!rest) break;
        int start = __builtin_ctz(rest);
        int frontier = 1 << start, color = 0;
        seen |= frontier;
        while (frontier) {
            int nxt = 0;
            for (int f = frontier; f; f &= f - 1) {
                int v = __builtin_ctz(f);
                nxt |= adj[v] & mask;
            }
            /* conflict: a vertex in the current color layer adjacent to same layer */
            for (int f = frontier; f; f &= f - 1) {
                int v = __builtin_ctz(f);
                if (adj[v] & frontier) return 0;
            }
            if (color == 1) c1 |= frontier;
            nxt &= ~seen;
            seen |= nxt;
            frontier = nxt;
            color ^= 1;
        }
    }
    if (col1) *col1 = c1;
    return 1;
}

/* connected components of induced subgraph on mask: comps[] gets masks */
static int components(int mask, int comps[MAXN]) {
    int seen = 0, k = 0;
    while (1) {
        int rest = mask & ~seen;
        if (!rest) break;
        int frontier = 1 << __builtin_ctz(rest), comp = frontier;
        while (frontier) {
            int nxt = 0;
            for (int f = frontier; f; f &= f - 1)
                nxt |= adj[__builtin_ctz(f)] & mask;
            nxt &= ~comp;
            comp |= nxt;
            frontier = nxt;
        }
        comps[k++] = comp;
        seen |= comp;
    }
    return k;
}

/* forest test on induced subgraph: edges == vertices - components */
static int forest_ok(int mask) {
    int edges = 0;
    for (int f = mask; f; f &= f - 1) {
        int v = __builtin_ctz(f);
        edges += __builtin_popcount(adj[v] & mask & ~((2 << v) - 1));
    }
    if (edges >= __builtin_popcount(mask)) return 0;   /* quick reject */
    int comps[MAXN];
    int k = components(mask, comps);
    return edges == __builtin_popcount(mask) - k;
}

/* max induced forest order within mask */
static int max_forest(int mask) {
    int best = 0;
    int s = mask;
    while (1) {
        int pc = __builtin_popcount(s);
        if (pc > best && forest_ok(s)) best = pc;
        if (s == 0) break;
        s = (s - 1) & mask;
    }
    return best;
}

/* FE of one component with classes A,B (masks): max |W|+|Y| over both
 * orientations, Y subset of Z, W u Y forest */
static int fe_comp(int A, int B) {
    int best = 0;
    for (int side = 0; side < 2; side++) {
        int W = side ? B : A, Z = side ? A : B;
        int wpc = __builtin_popcount(W);
        int s = Z;
        while (1) {
            int cand = wpc + __builtin_popcount(s);
            if (cand > best && forest_ok(W | s)) best = cand;
            if (s == 0) break;
            s = (s - 1) & Z;
        }
    }
    return best;
}

/* minimum path cover of the whole graph */
static unsigned char dp_cover[1 << 15];
static unsigned short ham_ends[1 << 15];

static int path_cover_all(void) {
    int full = (1 << n) - 1;
    for (int mask = 1; mask <= full; mask++) {
        int pc = __builtin_popcount(mask);
        if (pc == 1) { ham_ends[mask] = mask; continue; }
        int ends = 0;
        for (int f = mask; f; f &= f - 1) {
            int v = __builtin_ctz(f);
            if (ham_ends[mask ^ (1 << v)] & adj[v]) ends |= 1 << v;
        }
        ham_ends[mask] = (unsigned short)ends;
    }
    dp_cover[0] = 0;
    for (int mask = 1; mask <= full; mask++) {
        int low = mask & (-mask);
        int best = 99;
        for (int sub = mask; sub; sub = (sub - 1) & mask) {
            if ((sub & low) && ham_ends[sub]) {
                int c = dp_cover[mask ^ sub] + 1;
                if (c < best) best = c;
            }
        }
        dp_cover[mask] = (unsigned char)best;
    }
    return dp_cover[full];
}

/* all minimum OCTs: returns o, fills octs[] (masks), cnt */
static int min_octs(int octs[], int *cnt) {
    int full = (1 << n) - 1;
    for (int k = 0; k <= n; k++) {
        int c = 0;
        for (int T = 0; T <= full; T++) {
            if (__builtin_popcount(T) != k) continue;
            if (two_color(full ^ T, NULL)) octs[c++] = T;
        }
        if (c) { *cnt = c; return k; }
    }
    return -1;
}

/* per-remainder stats; returns via pointers */
static void bip_stats(int bm, int *c_e, int *iso, int *M, int *Delta,
                      int *r, int *g) {
    int col1 = 0;
    two_color(bm, &col1);
    int comps[MAXN];
    int k = components(bm, comps);
    *c_e = *iso = *M = *r = *g = 0;
    int imb = 0;
    for (int t = 0; t < k; t++) {
        int comp = comps[t];
        int has_edge = 0;
        for (int f = comp; f; f &= f - 1)
            if (adj[__builtin_ctz(f)] & comp) { has_edge = 1; break; }
        if (!has_edge) { *iso += __builtin_popcount(comp); continue; }
        (*c_e)++;
        int A = comp & ~col1, B = comp & col1;
        int a = __builtin_popcount(A), b = __builtin_popcount(B);
        *M += a < b ? a : b;
        imb += a > b ? a - b : b - a;
        /* r(C): some smaller-or-tied class has a pair with codeg <= 1 */
        int rc = 0;
        for (int side = 0; side < 2 && !rc; side++) {
            int cls = side ? B : A, other = side ? A : B;
            if (__builtin_popcount(cls) > __builtin_popcount(other)) continue;
            for (int f = cls; f && !rc; f &= f - 1) {
                int u = __builtin_ctz(f);
                for (int h = f & (f - 1); h; h &= h - 1) {
                    int v = __builtin_ctz(h);
                    if (__builtin_popcount(adj[u] & adj[v] & comp) <= 1) {
                        rc = 1; break;
                    }
                }
            }
        }
        *r += rc;
        int fe = fe_comp(A, B);
        int gc = fe - (a > b ? a : b);
        if (gc < 1 + rc) {
            fprintf(stderr, "INV-DOM VIOLATION gc=%d rc=%d\n", gc, rc);
            exit(2);
        }
        *g += gc;
    }
    *Delta = imb + *iso;
}

static void mode_cond(void) {
    char line[128];
    unsigned long long conn = 0, nonbip = 0, s1 = 0, s2 = 0, s3 = 0,
                       l6not5 = 0, tight = 0;
    FILE *tf = fdopen(3, "w");   /* tight list, if fd 3 provided */
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!parse_g6(line)) continue;
        conn++;
        int full = (1 << n) - 1;
        if (two_color(full, NULL)) continue;
        nonbip++;
        int p = path_cover_all(), ell = n - p;
        int octs[1 << 12], cnt = 0;
        int o = min_octs(octs, &cnt);
        int ok5 = 0, ok6 = 0, best_slack = -1000;
        char prof[4096]; prof[0] = 0;
        for (int t = 0; t < cnt; t++) {
            int bm = full ^ octs[t];
            int c_e, iso, M, Delta, r, g;
            bip_stats(bm, &c_e, &iso, &M, &Delta, &r, &g);
            int tau = __builtin_popcount(bm) - max_forest(bm);
            int thr5 = 2 * c_e + Delta + 2 * r - 1;
            int thr6 = Delta + 2 * g - 1;
            int slack = ell - (2 * tau + o + 1);
            if (p <= thr5) ok5 = 1;
            if (p <= thr6) ok6 = 1;
            if (slack > best_slack) best_slack = slack;
            char one[128];
            snprintf(one, sizeof one, " (T=%d tau=%d c_e=%d D=%d r=%d g=%d"
                     " thr5=%d thr6=%d sl=%d)", octs[t], tau, c_e, Delta,
                     r, g, thr5, thr6, slack);
            if (strlen(prof) + strlen(one) + 1 < sizeof prof)
                strcat(prof, one);
        }
        if (!ok5) { s1++; printf("S1FAIL %s p=%d o=%d%s\n", line, p, o, prof); }
        if (!ok6) { s2++; printf("S2FAIL %s p=%d o=%d%s\n", line, p, o, prof); }
        if (best_slack < 0) { s3++; printf("S3FAIL %s p=%d o=%d%s\n",
                                           line, p, o, prof); }
        if (ok6 && !ok5) l6not5++;
        if (best_slack == 0) { tight++; if (tf) fprintf(tf, "%s\n", line); }
    }
    if (tf) fclose(tf);
    printf("COND connected=%llu nonbip=%llu s1=%llu s2=%llu s3=%llu "
           "l6not5=%llu tight=%llu\n", conn, nonbip, s1, s2, s3, l6not5,
           tight);
}

static void mode_excess(void) {
    char line[128];
    unsigned long long tot = 0;
    long long hist[64]; memset(hist, 0, sizeof hist);
    int min_e = 1 << 20;
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!parse_g6(line)) continue;
        int full = (1 << n) - 1, col1 = 0;
        if (!two_color(full, &col1)) { fprintf(stderr, "nonbip input\n");
                                       exit(2); }
        tot++;
        int A = full & ~col1, B = col1;
        int a = __builtin_popcount(A), b = __builtin_popcount(B);
        int g = fe_comp(A, B) - (a > b ? a : b);
        int p = path_cover_all();
        int e = (a > b ? a - b : b - a) + 2 * g - p;
        if (e + 32 >= 0 && e + 32 < 64) hist[e + 32]++;
        if (e < min_e) min_e = e;
        if (e <= 0)
            printf("E0WIT %s a=%d b=%d p=%d g=%d excess=%d\n",
                   line, a, b, p, g, e);
    }
    printf("EXC graphs=%llu min_excess=%d hist:", tot, min_e);
    for (int e = -32; e < 32; e++)
        if (hist[e + 32]) printf(" %d:%lld", e, hist[e + 32]);
    printf("\n");
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "mode?\n"); return 1; }
    if (!strcmp(argv[1], "cond")) mode_cond();
    else if (!strcmp(argv[1], "excess")) mode_excess();
    else { fprintf(stderr, "unknown mode\n"); return 1; }
    return 0;
}
