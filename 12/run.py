#!/usr/bin/env python3

from sys import stdin
from functools import cache

records = []
for line in stdin:
    row, shape = line.strip().split(' ')
    records.append((row, tuple(map(int, shape.split(',')))))


@cache
def count_possibs(row: str, shape: tuple[int, ...]) -> int:
    if not row:
        return int(not shape)

    if not shape:
        return int("#" not in row)

    c, rest = row[0], row[1:]

    if c == ".":
        return count_possibs(rest, shape)

    if c == "#":
        n = shape[0]
        if len(row) < n or "." in row[:n] or (len(row) > n and row[n] == "#"):
            return 0
        return count_possibs(row[n + 1:], shape[1:])

    return count_possibs("#" + rest, shape) + count_possibs("." + rest, shape)


def expand(row: str, shape: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join([row] * 5), shape * 5


print(sum(count_possibs(*r) for r in records))
print(sum(count_possibs(*expand(*r)) for r in records))
