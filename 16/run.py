#!/usr/bin/env python3

from sys import stdin
from collections import namedtuple

Beam = namedtuple("Beam", ["pos", "rot"])

grid = {(x, y): c
        for y, line in enumerate(stdin)
        for x, c in enumerate(line.strip())
        if c != "."}

dims = (max(x for x, _ in grid),
        max(y for _, y in grid))


def contained(b: Beam) -> bool:
    x, y = b.pos
    return 0 <= x <= dims[0] and \
        0 <= y <= dims[1]


def trace(b: Beam) -> list[Beam]:
    if not contained(b):
        return []

    if b.pos not in grid:
        return [fwd(b)]

    c = grid[b.pos]

    if c in ("/", "\\"):
        return [fwd(rot(b, c))]

    if c in ("|", "-"):
        beams = split(b, c)
        return beams

    raise Exception


def fwd(b: Beam) -> Beam:
    x, y = b.pos
    if b.rot == 0:  # Right
        return Beam((x + 1, y), b.rot)
    elif b.rot == 1:  # Up
        return Beam((x, y - 1), b.rot)
    elif b.rot == 2:  # Left
        return Beam((x - 1, y), b.rot)
    else:  # Down
        return Beam((x, y + 1), b.rot)


def rot(b: Beam, c: str) -> Beam:
    states = {"/": {0: 1, 1: 0, 2: 3, 3: 2},
              "\\": {0: 3, 1: 2, 2: 1, 3: 0}}
    return Beam(b.pos, states[c][b.rot])


def split(b: Beam, c: str) -> list[Beam]:
    if b.rot in (0, 2) and c == "|":
        return [fwd(Beam(b.pos, 1)), fwd(Beam(b.pos, 3))]

    if b.rot in (1, 3) and c == "-":
        return [fwd(Beam(b.pos, 0)), fwd(Beam(b.pos, 2))]

    return [fwd(b)]


def count_energized_tiles(start: Beam) -> int:
    curr = [start]
    visited_vectors = set()
    visited_nodes = set()

    while curr:
        prev = curr
        curr = []
        for b in prev:
            if not contained(b) or b in visited_vectors:
                continue
            visited_vectors.add(b)
            visited_nodes.add(b.pos)
            curr += trace(b)

    return len(visited_nodes)


def find_best_beam() -> int:
    candidates = set()
    xmax, ymax = dims

    for x in range(xmax):
        candidates.add(Beam((x, 0), 3))
        candidates.add(Beam((x, xmax - 1), 1))

    for y in range(ymax):
        candidates.add(Beam((0, y), 0))
        candidates.add(Beam((ymax - 1, y), 2))

    return max(map(count_energized_tiles, candidates))


print(count_energized_tiles(Beam((0, 0), 0)))
print(find_best_beam())
