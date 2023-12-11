#!/usr/bin/env python3

from sys import stdin
from itertools import combinations, starmap


def main():
    space = parse(stdin)
    print(score(expand(space)))
    print(score(expand(space, 1000000)))


def parse(f):
    space = set()
    for y, line in enumerate(f):
        for x, c in enumerate(line.strip()):
            if c == '#':
                space.add((x, y))
    return space


def score(space):
    return sum(starmap(distance, combinations(space, r=2)))


def expand(space, rate=2):
    x_min, y_min, x_max, y_max = dimensions(space)

    cols = [x for x in range(x_min, x_max + 1)
            if all((x, y) not in space for y in range(y_min, y_max + 1))]

    rows = [y for y in range(y_min, y_max + 1)
            if all((x, y) not in space for x in range(x_min, x_max + 1))]

    return {(x + sum(rate - 1 for xx in cols if xx < x),
             y + sum(rate - 1 for yy in rows if yy < y))
            for x, y in space}


def distance(a, b):
    return sum(abs(x1 - x2) for x1, x2 in zip(a, b))


def dimensions(space):
    xs = [x for x, y in space]
    ys = [y for x, y in space]
    return (min(xs), min(ys), max(xs), max(ys))


main()
