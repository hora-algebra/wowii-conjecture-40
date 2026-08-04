/* Independent LIFT-A / LIFT-A-ALL checker.
 * Written from PREREG-LIFT.md's frozen statements before inspecting work/lift.c.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bits_t;

static int n;
static bits_t adj[16];
static bits_t path_end[1u << 15];
static unsigned char path_cover[1u << 15];
static unsigned char forest_order[1u << 15];

static int decode_graph6(const char *line) {
    int pos = 0;
    n = (unsigned char)line[pos++] - 63;
    if (n < 1 || n > 15) return 0;
    for (int v = 0; v < n; ++v) adj[v] = 0;
    int value = 0, remaining = 0;
    for (int v = 1; v < n; ++v) for (int u = 0; u < v; ++u) {
        if (!remaining) {
            unsigned char ch = (unsigned char)line[pos++];
            if (ch < 63 || ch > 126) return 0;
            value = ch - 63;
            remaining = 6;
        }
        if ((value >> (--remaining)) & 1) {
            adj[u] |= 1u << v;
            adj[v] |= 1u << u;
        }
    }
    return 1;
}

static int root(int parent[16], int v) {
    while (parent[v] != v) v = parent[v];
    return v;
}

static int is_forest(bits_t mask) {
    int parent[16];
    for (int v = 0; v < n; ++v) parent[v] = v;
    bits_t vertices = mask;
    while (vertices) {
        bits_t ub = vertices & (0u - vertices);
        int u = __builtin_ctz(ub);
        vertices ^= ub;
        bits_t neighbours = adj[u] & mask & ~((1u << (u + 1)) - 1u);
        while (neighbours) {
            bits_t vb = neighbours & (0u - neighbours);
            int v = __builtin_ctz(vb);
            neighbours ^= vb;
            int ru = root(parent, u), rv = root(parent, v);
            if (ru == rv) return 0;
            parent[ru] = rv;
        }
    }
    return 1;
}

static int is_bipartite(bits_t mask) {
    signed char colour[16];
    int queue[16];
    for (int v = 0; v < n; ++v) colour[v] = -1;
    for (int start = 0; start < n; ++start) {
        if (!(mask & (1u << start)) || colour[start] >= 0) continue;
        int head = 0, tail = 0;
        colour[start] = 0;
        queue[tail++] = start;
        while (head < tail) {
            int u = queue[head++];
            bits_t neighbours = adj[u] & mask;
            while (neighbours) {
                bits_t bit = neighbours & (0u - neighbours);
                int v = __builtin_ctz(bit);
                neighbours ^= bit;
                if (colour[v] < 0) {
                    colour[v] = (signed char)(1 - colour[u]);
                    queue[tail++] = v;
                } else if (colour[v] == colour[u]) return 0;
            }
        }
    }
    return 1;
}

static void compute_path_covers(bits_t full) {
    path_end[0] = 0;
    path_cover[0] = 0;
    for (bits_t mask = 1; mask <= full; ++mask) {
        if (!(mask & (mask - 1))) path_end[mask] = mask;
        else {
            bits_t endpoints = 0, vertices = mask;
            while (vertices) {
                bits_t bit = vertices & (0u - vertices);
                int v = __builtin_ctz(bit);
                vertices ^= bit;
                if (path_end[mask ^ bit] & adj[v]) endpoints |= bit;
            }
            path_end[mask] = endpoints;
        }
        if (path_end[mask]) {
            path_cover[mask] = 1;
            continue;
        }
        unsigned char best = (unsigned char)n;
        bits_t first = mask & (0u - mask);
        bits_t optional = mask ^ first;
        for (bits_t chosen = optional;; chosen = (chosen - 1) & optional) {
            bits_t part = chosen | first;
            if (path_end[part]) {
                unsigned char candidate = (unsigned char)(1 + path_cover[mask ^ part]);
                if (candidate < best) {
                    best = candidate;
                    if (best == 2) break;
                }
            }
            if (!chosen) break;
        }
        path_cover[mask] = best;
    }
}

static void compute_forest_orders(bits_t full) {
    forest_order[0] = 0;
    for (bits_t mask = 1; mask <= full; ++mask) {
        if (is_forest(mask)) {
            forest_order[mask] = (unsigned char)__builtin_popcount(mask);
            continue;
        }
        unsigned char best = 0;
        bits_t vertices = mask;
        while (vertices) {
            bits_t bit = vertices & (0u - vertices);
            vertices ^= bit;
            if (forest_order[mask ^ bit] > best) best = forest_order[mask ^ bit];
        }
        forest_order[mask] = best;
    }
}

static int compute_lift(int *oct_size, int *best_slack, int *worst_slack,
                        int *minimum_oct_count, int *ell) {
    bits_t full = (1u << n) - 1u;
    if (is_bipartite(full)) return 0;
    compute_path_covers(full);
    compute_forest_orders(full);
    *ell = n - path_cover[full];
    *oct_size = -1;
    *best_slack = -100;
    *worst_slack = 100;
    *minimum_oct_count = 0;
    for (int k = 1; k <= n && *oct_size < 0; ++k) {
        for (bits_t deleted = 1; deleted <= full; ++deleted) {
            if (__builtin_popcount(deleted) != k) continue;
            bits_t remainder = full ^ deleted;
            if (!is_bipartite(remainder)) continue;
            *oct_size = k;
            ++*minimum_oct_count;
            int tau_remainder = __builtin_popcount(remainder) - forest_order[remainder];
            int slack = *ell - 2 * tau_remainder - k - 1;
            if (slack > *best_slack) *best_slack = slack;
            if (slack < *worst_slack) *worst_slack = slack;
        }
    }
    return 1;
}

static void clear_graph(int order) {
    n = order;
    for (int v = 0; v < n; ++v) adj[v] = 0;
}

static void add_edge(int u, int v) {
    adj[u] |= 1u << v;
    adj[v] |= 1u << u;
}

static int gold_one(const char *name, int expected_slack) {
    int o, best, worst, count, ell;
    int nonbip = compute_lift(&o, &best, &worst, &count, &ell);
    int pass = nonbip && best == expected_slack && worst == expected_slack;
    printf("GOLD %s ell=%d o=%d minOCTs=%d best=%d worst=%d expected=%d %s\n",
           name, ell, o, count, best, worst, expected_slack, pass ? "PASS" : "FAIL");
    return pass;
}

static int run_gold(void) {
    int all = 1;
    clear_graph(3); for (int u=0;u<3;u++) for(int v=u+1;v<3;v++) add_edge(u,v);
    all &= gold_one("K3", 0);
    clear_graph(4); for (int u=0;u<4;u++) for(int v=u+1;v<4;v++) add_edge(u,v);
    all &= gold_one("K4", 0);
    clear_graph(5); for (int u=0;u<5;u++) for(int v=u+1;v<5;v++) add_edge(u,v);
    all &= gold_one("K5", 0);
    clear_graph(5); for (int u=0;u<5;u++) add_edge(u,(u+1)%5);
    all &= gold_one("C5", 2);
    clear_graph(7); for (int u=0;u<7;u++) add_edge(u,(u+1)%7);
    all &= gold_one("C7", 4);
    return all ? 0 : 1;
}

static int run_sweep(void) {
    char line[256];
    unsigned long long graphs = 0, nonbipartite = 0, lift_a_fail = 0;
    unsigned long long lift_a_all_fail = 0, tight = 0, histogram[32] = {0};
    int maximum_minimum_octs = 0;
    FILE *tight_out = NULL;
    const char *tight_path = getenv("LIFT_TIGHT_OUT");
    if (tight_path) tight_out = fopen(tight_path, "w");
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!line[0]) continue;
        ++graphs;
        if (!decode_graph6(line)) return 2;
        int o, best, worst, min_oct_count, ell;
        if (!compute_lift(&o, &best, &worst, &min_oct_count, &ell)) continue;
        ++nonbipartite;
        if (min_oct_count > maximum_minimum_octs) maximum_minimum_octs = min_oct_count;
        if (best < 0) {
            ++lift_a_fail;
            printf("LIFT_A_FAIL %s ell=%d o=%d best=%d\n", line, ell, o, best);
        }
        if (worst < 0) {
            ++lift_a_all_fail;
            printf("LIFT_A_ALL_FAIL %s ell=%d o=%d worst=%d\n", line, ell, o, worst);
        }
        if (best == 0) {
            ++tight;
            if (tight_out) fprintf(tight_out, "%s\n", line);
        }
        if (best >= 0 && best < 32) ++histogram[best];
    }
    if (tight_out) fclose(tight_out);
    fprintf(stderr,
            "LIFT_SUMMARY graphs=%llu nonbipartite=%llu lift_a_fail=%llu lift_a_all_fail=%llu tight=%llu max_min_octs=%d histogram=",
            graphs, nonbipartite, lift_a_fail, lift_a_all_fail, tight,
            maximum_minimum_octs);
    int first = 1;
    for (int i = 0; i < 32; ++i) if (histogram[i]) {
        fprintf(stderr, "%s%d:%llu", first ? "" : ",", i, histogram[i]);
        first = 0;
    }
    fputc('\n', stderr);
    return (lift_a_fail || lift_a_all_fail) ? 1 : 0;
}

static int run_inspect(void) {
    char line[256];
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!line[0]) continue;
        if (!decode_graph6(line)) return 2;
        int o, best, worst, min_oct_count, ell;
        if (!compute_lift(&o, &best, &worst, &min_oct_count, &ell)) {
            printf("LIFT_INSPECT %s bipartite=1\n", line);
            continue;
        }
        printf("LIFT_INSPECT %s ell=%d o=%d minOCTs=%d best=%d worst=%d\n",
               line, ell, o, min_oct_count, best, worst);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "gold")) return run_gold();
    if (!strcmp(argv[1], "sweep")) return run_sweep();
    if (!strcmp(argv[1], "inspect")) return run_inspect();
    return 2;
}
