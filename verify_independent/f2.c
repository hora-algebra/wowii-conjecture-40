/* Independent direct F2 / F2-ALL checker.
 * Written from the paper's incidence-selection definition before inspecting
 * work/f2.c.  It searches for one feasible selection whose incidence graph is
 * acyclic, pruning a branch immediately when a selected cycle appears.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bits_t;

static int n;
static bits_t adj[16], s_mask, h_mask;
static int fixed_x, fixed_y, s_order[16], s_count;
static unsigned char capacity[16], load[16];
static int found_acyclic;

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

static int induced_is_forest(bits_t mask) {
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

static void sort_s(void) {
    s_count = 0;
    bits_t ss = s_mask;
    while (ss) {
        bits_t bit = ss & (0u - ss);
        ss ^= bit;
        s_order[s_count++] = __builtin_ctz(bit);
    }
    for (int i = 1; i < s_count; ++i) {
        int value = s_order[i];
        int degree = __builtin_popcount(adj[value] & h_mask);
        int j = i;
        while (j && __builtin_popcount(adj[s_order[j - 1]] & h_mask) > degree) {
            s_order[j] = s_order[j - 1];
            --j;
        }
        s_order[j] = value;
    }
}

static void search_acyclic(int position, const int incoming_parent[16]) {
    if (found_acyclic) return;
    if (position == s_count) {
        found_acyclic = 1;
        return;
    }
    int s = s_order[position];
    bits_t firsts = adj[s] & h_mask;
    while (firsts) {
        bits_t h1b = firsts & (0u - firsts);
        int h1 = __builtin_ctz(h1b);
        firsts ^= h1b;
        if (load[h1] >= capacity[h1]) continue;
        bits_t seconds = firsts;
        while (seconds) {
            bits_t h2b = seconds & (0u - seconds);
            int h2 = __builtin_ctz(h2b);
            seconds ^= h2b;
            if (load[h2] >= capacity[h2]) continue;
            int parent[16];
            memcpy(parent, incoming_parent, sizeof parent);
            int r1 = root(parent, h1), r2 = root(parent, h2);
            if (r1 == r2) continue;
            parent[r1] = r2;
            ++load[h1];
            ++load[h2];
            search_acyclic(position + 1, parent);
            --load[h1];
            --load[h2];
            if (found_acyclic) return;
        }
    }
}

static int instance_has_acyclic_selection(void) {
    for (int h = 0; h < n; ++h) {
        capacity[h] = 2;
        load[h] = 0;
    }
    capacity[fixed_x] = capacity[fixed_y] = 1;
    sort_s();
    int parent[16];
    for (int h = 0; h < n; ++h) parent[h] = h;
    found_acyclic = 0;
    search_acyclic(0, parent);
    return found_acyclic;
}

static void clear_graph(int order) {
    n = order;
    for (int v = 0; v < n; ++v) adj[v] = 0;
}

static void add_edge(int u, int v) {
    adj[u] |= 1u << v;
    adj[v] |= 1u << u;
}

static int control(const char *name, int order, bits_t controls_s, int x, int y,
                   const int edges[][2], int edge_count) {
    clear_graph(order);
    for (int i = 0; i < edge_count; ++i) add_edge(edges[i][0], edges[i][1]);
    s_mask = controls_s;
    h_mask = ((1u << n) - 1u) ^ s_mask;
    fixed_x = x;
    fixed_y = y;
    int acyclic = instance_has_acyclic_selection();
    printf("CONTROL %s acyclic_feasible=%d %s\n", name, acyclic,
           acyclic ? "FAIL" : "PASS");
    return !acyclic;
}

static int run_controls(void) {
    static const int o56[][2] = {
        {0,4},{0,5},{0,6},{1,4},{1,5},{1,6},{2,6},{2,7},{3,6},{3,8},
        {9,4},{9,5},{4,10},{10,11},{6,12},{12,7},{6,13},{13,8}
    };
    static const int o63[][2] = {
        {0,7},{0,8},{0,9},{1,7},{1,8},{2,9},{2,10},{2,11},
        {3,9},{3,10},{3,11},{4,9},{4,10},{4,11},
        {5,7},{5,8},{5,9},{5,10},{5,11},{7,6},{6,12}
    };
    static const int o64[][2] = {
        {0,3},{0,5},{0,7},{1,3},{1,5},{2,7},{2,8},
        {3,4},{4,5},{3,6},{6,7},{6,8}
    };
    int all = 1;
    all &= control("O-56", 14, 0x000fu, 10, 11, o56,
                   (int)(sizeof o56 / sizeof o56[0]));
    all &= control("O-63", 13, 0x001fu, 6, 12, o63,
                   (int)(sizeof o63 / sizeof o63[0]));
    all &= control("O-64", 9, 0x0007u, 7, 6, o64,
                   (int)(sizeof o64 / sizeof o64[0]));
    return all ? 0 : 1;
}

static int run_sweep(void) {
    char line[256];
    unsigned long long graphs = 0, min_fvs = 0, instances = 0;
    unsigned long long all_failures = 0, some_failures = 0;
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!line[0]) continue;
        ++graphs;
        if (!decode_graph6(line)) return 2;
        bits_t full = (1u << n) - 1u;
        int minimum = -1;
        for (int k = 0; k <= n && minimum < 0; ++k) {
            for (bits_t deleted = 0; deleted <= full; ++deleted) {
                if (__builtin_popcount(deleted) == k &&
                    induced_is_forest(full ^ deleted)) {
                    minimum = k;
                    break;
                }
            }
        }
        if (minimum < 2) continue;
        for (bits_t deleted = 0; deleted <= full; ++deleted) {
            if (__builtin_popcount(deleted) != minimum) continue;
            bits_t kept = full ^ deleted;
            if (!induced_is_forest(kept)) continue;
            ++min_fvs;
            s_mask = deleted;
            h_mask = kept;
            int some_for_fvs = 0;
            bits_t hh = h_mask;
            while (hh) {
                bits_t ub = hh & (0u - hh);
                int u = __builtin_ctz(ub);
                hh ^= ub;
                bits_t neighbours = adj[u] & h_mask & ~((1u << (u + 1)) - 1u);
                while (neighbours) {
                    bits_t vb = neighbours & (0u - neighbours);
                    int v = __builtin_ctz(vb);
                    neighbours ^= vb;
                    fixed_x = u;
                    fixed_y = v;
                    ++instances;
                    if (instance_has_acyclic_selection()) some_for_fvs = 1;
                    else {
                        ++all_failures;
                        printf("F2_ALL_FAIL %s S=%x e=%d-%d\n", line, deleted, u, v);
                    }
                }
            }
            if (!some_for_fvs) {
                ++some_failures;
                printf("F2_SOME_FAIL %s S=%x\n", line, deleted);
            }
        }
        if (graphs % 1000000u == 0)
            fprintf(stderr, "F2_PROGRESS graphs=%llu instances=%llu all_fail=%llu some_fail=%llu\n",
                    graphs, instances, all_failures, some_failures);
    }
    fprintf(stderr,
            "F2_SUMMARY graphs=%llu min_fvs=%llu instances=%llu all_failures=%llu some_failures=%llu\n",
            graphs, min_fvs, instances, all_failures, some_failures);
    return (all_failures || some_failures) ? 1 : 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "controls")) return run_controls();
    if (!strcmp(argv[1], "sweep")) return run_sweep();
    return 2;
}
