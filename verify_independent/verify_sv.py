#!/usr/bin/env python3
"""Independent Definition 5.4 SV checker.

This file was written from paper/paper.pdf sections 2 and 5 before inspecting
any repository implementation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Graph:
    n: int
    adj: tuple[int, ...]

    @property
    def edges(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            (u, v)
            for u in range(self.n)
            for v in range(u + 1, self.n)
            if (self.adj[u] >> v) & 1
        )


def decode_graph6(text: str) -> Graph:
    text = text.strip()
    if text.startswith(">>graph6<<"):
        text = text[10:]
    if not text or text[0] == "~":
        raise ValueError("checker supports only one-byte graph6 orders 0..62")
    n = ord(text[0]) - 63
    need = n * (n - 1) // 2
    bits: list[int] = []
    for ch in text[1:]:
        value = ord(ch) - 63
        if not 0 <= value < 64:
            raise ValueError(f"invalid graph6 character {ch!r}")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < need:
        raise ValueError("truncated graph6 string")
    adj = [0] * n
    index = 0
    for v in range(1, n):
        for u in range(v):
            if bits[index]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            index += 1
    return Graph(n, tuple(adj))


def delete_vertex(graph: Graph, removed: int) -> Graph:
    keep = [v for v in range(graph.n) if v != removed]
    index = {old: new for new, old in enumerate(keep)}
    adj = [0] * (graph.n - 1)
    for old_u in keep:
        u = index[old_u]
        for old_v in keep:
            if old_u < old_v and ((graph.adj[old_u] >> old_v) & 1):
                v = index[old_v]
                adj[u] |= 1 << v
                adj[v] |= 1 << u
    return Graph(graph.n - 1, tuple(adj))


def is_forest(graph: Graph, mask: int) -> bool:
    parent = list(range(graph.n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u in range(graph.n):
        if not ((mask >> u) & 1):
            continue
        neighbours = graph.adj[u] & mask & ~((1 << (u + 1)) - 1)
        while neighbours:
            bit = neighbours & -neighbours
            v = bit.bit_length() - 1
            neighbours ^= bit
            ru, rv = find(u), find(v)
            if ru == rv:
                return False
            parent[ru] = rv
    return True


def is_bipartite(graph: Graph, mask: int) -> bool:
    unseen = mask
    colour1 = 0
    while unseen:
        start_bit = unseen & -unseen
        unseen ^= start_bit
        frontier = start_bit
        colour = 0
        while frontier:
            next_frontier = 0
            vertices = frontier
            if colour:
                colour1 |= frontier
            while vertices:
                bit = vertices & -vertices
                u = bit.bit_length() - 1
                vertices ^= bit
                neighbours = graph.adj[u] & mask
                if colour and (neighbours & colour1):
                    return False
                if not colour and (neighbours & (mask ^ colour1 ^ unseen)):
                    return False
                next_frontier |= neighbours & unseen
            unseen &= ~next_frontier
            frontier = next_frontier
            colour ^= 1
    return True


def max_induced_order(graph: Graph, predicate) -> int:
    for size in range(graph.n, -1, -1):
        for mask in range(1 << graph.n):
            if bin(mask).count("1") == size and predicate(graph, mask):
                return size
    raise AssertionError("empty graph must satisfy both predicates")


def path_cover_number(graph: Graph) -> int:
    limit = 1 << graph.n
    endpoints = [0] * limit
    hamiltonian = [False] * limit
    hamiltonian[0] = True
    for mask in range(1, limit):
        if mask & (mask - 1) == 0:
            endpoints[mask] = mask
        else:
            vertices = mask
            possible = 0
            while vertices:
                bit = vertices & -vertices
                v = bit.bit_length() - 1
                vertices ^= bit
                if endpoints[mask ^ bit] & graph.adj[v]:
                    possible |= bit
            endpoints[mask] = possible
        hamiltonian[mask] = endpoints[mask] != 0

    covers = [graph.n + 1] * limit
    covers[0] = 0
    for mask in range(1, limit):
        first = mask & -mask
        subset = mask
        while subset:
            if (subset & first) and hamiltonian[subset]:
                candidate = 1 + covers[mask ^ subset]
                if candidate < covers[mask]:
                    covers[mask] = candidate
            subset = (subset - 1) & mask
    return covers[-1]


PRINTED_EDGES = {
    "J???FAWdVD?": {
        (0, 7), (0, 8), (0, 9), (0, 10), (1, 7), (1, 10), (2, 7),
        (2, 10), (3, 8), (3, 9), (4, 8), (5, 9), (6, 10), (7, 9),
        (8, 10),
    },
    r"J???FBObs\?": {
        (0, 7), (0, 8), (0, 9), (0, 10), (1, 7), (1, 8), (2, 7),
        (3, 8), (4, 9), (4, 10), (5, 9), (5, 10), (6, 9), (6, 10),
        (7, 9), (8, 10),
    },
    "J???FAWdUD_": {
        (0, 7), (0, 8), (0, 9), (0, 10), (1, 7), (1, 10), (2, 7),
        (3, 8), (3, 9), (4, 8), (5, 9), (6, 10), (7, 9), (8, 10),
        (9, 10),
    },
}


def check(text: str) -> None:
    graph = decode_graph6(text)
    expected_edges = PRINTED_EDGES.get(text)
    if expected_edges is not None:
        assert set(graph.edges) == expected_edges, (
            f"decoded edge mismatch for {text}: {graph.edges!r}"
        )
    f_value = max_induced_order(graph, is_forest)
    b_value = max_induced_order(graph, is_bipartite)
    p_value = path_cover_number(graph)
    o_value = graph.n - b_value
    eligible: list[tuple[int, int]] = []
    for vertex in range(graph.n):
        smaller = delete_vertex(graph, vertex)
        smaller_b = max_induced_order(smaller, is_bipartite)
        smaller_o = smaller.n - smaller_b
        if smaller_o == o_value - 1:
            eligible.append((vertex, path_cover_number(smaller)))
    print(
        f"{text} edges_asserted={expected_edges is not None} "
        f"f={f_value} b={b_value} p={p_value} o={o_value} "
        f"eligible={eligible}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", nargs="*", default=list(PRINTED_EDGES))
    args = parser.parse_args()
    for text in args.graph6:
        check(text)


if __name__ == "__main__":
    main()
