#!/usr/bin/env python3

from heapq import heappush, heappop
from operator import add, mul

L = {(x, y): int(c)
     for y, line in enumerate(open(0))
     for x, c in enumerate(line.strip())}

end = (max(x for x, _ in L),
       max(y for _, y in L))

move_deltas = {0: (1, 0), 1: (0, -1), 2: (-1, 0), 3: (0, 1)}
move_ranges = [list(range(1, 4)), list(range(4, 11))]


def moves(x, y, r, move_range):
    rotations = (r + 1) % 4, (r + 3) % 4    # Turn left and right
    for r in rotations:
        for n in move_range:
            if result := move_cost(x, y, r, n):
                cost = result
                dst = vadd((x, y), vmul(move_deltas[r], (n, n)))
                node = (*dst, r)
                yield cost, node


def find_lowest_cost(move_range):
    start = ((0, 0, 0), (0, 0, 3))  # Consider x, y and initial rotation
    Q = [(0, p) for p in start]     # Search queue
    C = {p: 0 for p in start}       # Cost map

    while Q:
        cost, node = heappop(Q)

        if node[:2] == end:
            return cost

        if cost > C[node]:
            continue

        for edge_cost, edge in moves(*node, move_range):
            edge_cost += cost
            if edge not in C or edge_cost < C[edge]:
                C[edge] = edge_cost
                heappush(Q, (edge_cost, edge))


def move_cost(x, y, r, n):
    cost = 0
    for i in range(1, n + 1):
        x, y = tuple(map(add, (x, y), move_deltas[r]))
        if not (x, y) in L:
            return
        cost += L[x, y]
    return cost


def vadd(v1, v2):
    return tuple(map(add, v1, v2))


def vmul(v1, v2):
    return tuple(map(mul, v1, v2))


print(find_lowest_cost(move_ranges[0]))
print(find_lowest_cost(move_ranges[1]))
