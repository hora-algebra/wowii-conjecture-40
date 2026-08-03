/* Independent Definition 5.4 SV sweep engine.
 * Written from paper/paper.pdf Sections 2 and 5 before inspecting any
 * repository SV sweep implementation.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bits_t;

static int n;
static bits_t adj[16];
static bits_t path_end[1u << 15];
static unsigned char path_cover[1u << 15];

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
            int edge = (value >> (--remaining)) & 1;
            if (edge) {
                adj[u] |= 1u << v;
                adj[v] |= 1u << u;
            }
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
                } else if (colour[v] == colour[u]) {
                    return 0;
                }
            }
        }
    }
    return 1;
}

static bits_t minimum_oct_eligible(bits_t full, int *oct_size) {
    for (int k = 1; k <= n; ++k) {
        bits_t eligible = 0;
        for (bits_t deleted = 1; deleted <= full; ++deleted) {
            if (__builtin_popcount(deleted) != k) continue;
            if (is_bipartite(full ^ deleted)) eligible |= deleted;
        }
        if (eligible) {
            *oct_size = k;
            return eligible;
        }
    }
    abort();
}

static void compute_path_covers(bits_t full) {
    path_end[0] = 0;
    path_cover[0] = 0;
    for (bits_t mask = 1; mask <= full; ++mask) {
        if (!(mask & (mask - 1))) {
            path_end[mask] = mask;
        } else {
            bits_t endpoints = 0;
            bits_t vertices = mask;
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
        bits_t chosen = optional;
        for (;;) {
            bits_t part = chosen | first;
            if (path_end[part]) {
                unsigned char candidate = (unsigned char)(1 + path_cover[mask ^ part]);
                if (candidate < best) {
                    best = candidate;
                    if (best == 2) break;
                }
            }
            if (!chosen) break;
            chosen = (chosen - 1) & optional;
        }
        path_cover[mask] = best;
    }
}

int main(void) {
    char line[256];
    unsigned long long input_count = 0, bipartite_count = 0;
    unsigned long long nonbipartite_count = 0, violation_count = 0;
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!line[0]) continue;
        ++input_count;
        if (!decode_graph6(line)) {
            fprintf(stderr, "decode failure at input %llu\n", input_count);
            return 2;
        }
        bits_t full = (1u << n) - 1;
        if (is_bipartite(full)) {
            ++bipartite_count;
            continue;
        }
        ++nonbipartite_count;

        int oct_size = -1;
        bits_t eligible = minimum_oct_eligible(full, &oct_size);
        compute_path_covers(full);
        int p_graph = path_cover[full];
        int sv_holds = 0;
        bits_t candidates = eligible;
        while (candidates) {
            bits_t bit = candidates & (0u - candidates);
            candidates ^= bit;
            if (p_graph <= path_cover[full ^ bit]) {
                sv_holds = 1;
                break;
            }
        }
        if (!sv_holds) {
            ++violation_count;
            printf("SV_FAIL %s o=%d p=%d eligible=", line, oct_size, p_graph);
            candidates = eligible;
            int first_output = 1;
            while (candidates) {
                bits_t bit = candidates & (0u - candidates);
                int v = __builtin_ctz(bit);
                candidates ^= bit;
                printf("%s%d:%d", first_output ? "" : ",", v,
                       path_cover[full ^ bit]);
                first_output = 0;
            }
            putchar('\n');
        }
    }
    fprintf(stderr,
            "SV_SUMMARY input=%llu bipartite=%llu nonbipartite=%llu violations=%llu\n",
            input_count, bipartite_count, nonbipartite_count, violation_count);
    return violation_count ? 1 : 0;
}
