/* Independent Lemma A forced-core checker.
 *
 * Method chosen before repository-code inspection: enumerate feasible
 * selections by backtracking and intersect their selected incidences.  Once
 * the running intersection is acyclic, enumeration may stop because further
 * intersections only delete incidences and cannot create a cycle.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bits_t;

static int n;
static bits_t adj[16];
static bits_t s_mask, h_mask;
static int fixed_x, fixed_y;
static int s_order[16], s_count;
static unsigned char capacity[16], load[16];
static bits_t current_selection[16], forced_selection[16];
static unsigned long long feasible_count;
static int have_first_selection, stopped_acyclic;

static int decode_graph6(const char *line) {
    int pos = 0;
    n = (unsigned char)line[pos++] - 63;
    if (n < 1 || n > 15) return 0;
    for (int v = 0; v < n; ++v) adj[v] = 0;
    int value = 0, remaining = 0;
    for (int v = 1; v < n; ++v) {
        for (int u = 0; u < v; ++u) {
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
    }
    return 1;
}

static int find_root(int parent[16], int v) {
    while (parent[v] != v) {
        parent[v] = parent[parent[v]];
        v = parent[v];
    }
    return v;
}

static int induced_is_forest(bits_t mask) {
    int parent[16];
    for (int v = 0; v < n; ++v) parent[v] = v;
    bits_t vertices = mask;
    while (vertices) {
        bits_t u_bit = vertices & (0u - vertices);
        int u = __builtin_ctz(u_bit);
        vertices ^= u_bit;
        bits_t neighbours = adj[u] & mask & ~((1u << (u + 1)) - 1u);
        while (neighbours) {
            bits_t v_bit = neighbours & (0u - neighbours);
            int v = __builtin_ctz(v_bit);
            neighbours ^= v_bit;
            int ru = find_root(parent, u), rv = find_root(parent, v);
            if (ru == rv) return 0;
            parent[ru] = rv;
        }
    }
    return 1;
}

static int forced_has_cycle(void) {
    int parent[16];
    for (int v = 0; v < n; ++v) parent[v] = v;
    bits_t ss = s_mask;
    while (ss) {
        bits_t s_bit = ss & (0u - ss);
        int s = __builtin_ctz(s_bit);
        ss ^= s_bit;
        bits_t neighbours = forced_selection[s];
        while (neighbours) {
            bits_t h_bit = neighbours & (0u - neighbours);
            int h = __builtin_ctz(h_bit);
            neighbours ^= h_bit;
            int rs = find_root(parent, s), rh = find_root(parent, h);
            if (rs == rh) return 1;
            parent[rs] = rh;
        }
    }
    return 0;
}

static void record_feasible_selection(void) {
    ++feasible_count;
    bits_t ss = s_mask;
    while (ss) {
        bits_t bit = ss & (0u - ss);
        int s = __builtin_ctz(bit);
        ss ^= bit;
        if (!have_first_selection) forced_selection[s] = current_selection[s];
        else forced_selection[s] &= current_selection[s];
    }
    have_first_selection = 1;
    if (!forced_has_cycle()) stopped_acyclic = 1;
}

static void enumerate_selections(int position) {
    if (stopped_acyclic) return;
    if (position == s_count) {
        record_feasible_selection();
        return;
    }
    int s = s_order[position];
    bits_t firsts = adj[s] & h_mask;
    while (firsts) {
        bits_t h1_bit = firsts & (0u - firsts);
        int h1 = __builtin_ctz(h1_bit);
        firsts ^= h1_bit;
        if (load[h1] >= capacity[h1]) continue;
        bits_t seconds = firsts;
        while (seconds) {
            bits_t h2_bit = seconds & (0u - seconds);
            int h2 = __builtin_ctz(h2_bit);
            seconds ^= h2_bit;
            if (load[h2] >= capacity[h2]) continue;
            ++load[h1];
            ++load[h2];
            current_selection[s] = h1_bit | h2_bit;
            enumerate_selections(position + 1);
            --load[h1];
            --load[h2];
            if (stopped_acyclic) return;
        }
    }
}

static void sort_s_by_incidence_degree(void) {
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
        while (j > 0 && __builtin_popcount(adj[s_order[j - 1]] & h_mask) > degree) {
            s_order[j] = s_order[j - 1];
            --j;
        }
        s_order[j] = value;
    }
}

static int check_instance(unsigned long long *selections_seen) {
    memset(load, 0, sizeof load);
    memset(current_selection, 0, sizeof current_selection);
    memset(forced_selection, 0, sizeof forced_selection);
    for (int h = 0; h < n; ++h) capacity[h] = 2;
    capacity[fixed_x] = capacity[fixed_y] = 1;
    feasible_count = 0;
    have_first_selection = 0;
    stopped_acyclic = 0;
    sort_s_by_incidence_degree();
    enumerate_selections(0);
    *selections_seen = feasible_count;
    return have_first_selection ? forced_has_cycle() : -1;
}

static void clear_graph(int order) {
    n = order;
    for (int v = 0; v < n; ++v) adj[v] = 0;
}

static void add_edge(int u, int v) {
    adj[u] |= 1u << v;
    adj[v] |= 1u << u;
}

static int run_control(const char *name, int order, bits_t controls_s,
                       int x, int y, const int edges[][2], int edge_count,
                       unsigned long long expected_feasible) {
    clear_graph(order);
    for (int i = 0; i < edge_count; ++i) add_edge(edges[i][0], edges[i][1]);
    s_mask = controls_s;
    h_mask = ((1u << n) - 1u) ^ s_mask;
    fixed_x = x;
    fixed_y = y;
    unsigned long long seen = 0;
    int cyclic = check_instance(&seen);
    int pass = cyclic == 1 && seen == expected_feasible;
    printf("CONTROL %s feasible=%llu cyclic=%d expected_feasible=%llu %s\n",
           name, seen, cyclic, expected_feasible, pass ? "PASS" : "FAIL");
    return pass;
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
    all &= run_control("O-56", 14, 0x000fu, 10, 11, o56,
                       (int)(sizeof o56 / sizeof o56[0]), 1);
    all &= run_control("O-63", 13, 0x001fu, 6, 12, o63,
                       (int)(sizeof o63 / sizeof o63[0]), 6);
    all &= run_control("O-64", 9, 0x0007u, 7, 6, o64,
                       (int)(sizeof o64 / sizeof o64[0]), 1);
    return all ? 0 : 1;
}

static int run_sweep(void) {
    char line[256];
    unsigned long long graph_count = 0, min_fvs_count = 0;
    unsigned long long instance_count = 0, infeasible_count = 0, cyclic_count = 0;
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!line[0]) continue;
        ++graph_count;
        if (!decode_graph6(line)) {
            fprintf(stderr, "decode failure at graph %llu\n", graph_count);
            return 2;
        }
        bits_t full = (1u << n) - 1u;
        int minimum = -1;
        for (int deleted_size = 0; deleted_size <= n && minimum < 0; ++deleted_size) {
            for (bits_t deleted = 0; deleted <= full; ++deleted) {
                if (__builtin_popcount(deleted) == deleted_size &&
                    induced_is_forest(full ^ deleted)) {
                    minimum = deleted_size;
                    break;
                }
            }
        }
        /* With fewer than two S-vertices the bipartite forced core cannot
         * contain a cycle.  The branch's published instance counts omit these
         * logically trivial layers, so use the same census convention. */
        if (minimum < 2) continue;
        for (bits_t deleted = 0; deleted <= full; ++deleted) {
            if (__builtin_popcount(deleted) != minimum) continue;
            bits_t kept = full ^ deleted;
            if (!induced_is_forest(kept)) continue;
            ++min_fvs_count;
            s_mask = deleted;
            h_mask = kept;
            bits_t hh = h_mask;
            while (hh) {
                bits_t u_bit = hh & (0u - hh);
                int u = __builtin_ctz(u_bit);
                hh ^= u_bit;
                bits_t neighbours = adj[u] & h_mask & ~((1u << (u + 1)) - 1u);
                while (neighbours) {
                    bits_t v_bit = neighbours & (0u - neighbours);
                    int v = __builtin_ctz(v_bit);
                    neighbours ^= v_bit;
                    fixed_x = u;
                    fixed_y = v;
                    unsigned long long seen = 0;
                    int cyclic = check_instance(&seen);
                    ++instance_count;
                    if (cyclic < 0) ++infeasible_count;
                    else if (cyclic) {
                        ++cyclic_count;
                        printf("CYCLIC %s S=%x e=%d-%d feasible=%llu\n",
                               line, deleted, u, v, seen);
                    }
                }
            }
        }
        if (graph_count % 1000000u == 0) {
            fprintf(stderr,
                    "FCORE_PROGRESS graphs=%llu instances=%llu cyclic=%llu infeasible=%llu\n",
                    graph_count, instance_count, cyclic_count, infeasible_count);
        }
    }
    fprintf(stderr,
            "FCORE_SUMMARY graphs=%llu min_fvs=%llu instances=%llu cyclic=%llu infeasible=%llu\n",
            graph_count, min_fvs_count, instance_count, cyclic_count, infeasible_count);
    return (cyclic_count || infeasible_count) ? 1 : 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: forced_core controls|sweep\n");
        return 2;
    }
    if (!strcmp(argv[1], "controls")) return run_controls();
    if (!strcmp(argv[1], "sweep")) return run_sweep();
    fprintf(stderr, "unknown mode\n");
    return 2;
}
