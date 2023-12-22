#!/usr/bin/env python3

from sys import stdin
from collections import Counter

patterns = []
for block in stdin.read().strip().split('\n\n'):
    patterns.append(block.split('\n'))


def get_pivot(lines):
    # A search space that will be narrowed down through set intersection
    pivots = set(range(1, len(lines[0])))

    for line in lines:
        pivots &= set(p for p in pivots if is_pivot(line, p))
        if not pivots:
            return

    assert len(pivots) == 1
    return min(pivots)


def is_pivot(line, pivot):
    return all(a == b for a, b in zip(line[pivot:], reversed(line[:pivot])))


def cols(pattern):
    return list(zip(*pattern))


def summarize_with(patterns, get_pivot):
    result = 0
    for i, pattern in enumerate(patterns):
        if pivot := get_pivot(pattern):
            result += pivot
        elif pivot := get_pivot(cols(pattern)):
            result += 100 * pivot
        assert pivot
    return result


def is_almost_pivot(line, pivot):
    return differ_by_one(line[pivot:], reversed(line[:pivot]))


def differ_by_one(xs, ys):
    has_error = 0
    for x, y in zip(xs, ys):
        if x != y:
            if has_error:
                return False
            else:
                has_error = True
    return has_error


def get_pivots_off_by_one(lines):
    pivots = Counter()
    almost_pivots = Counter()

    for line in lines:
        for pivot in range(1, len(lines[0])):
            if is_pivot(line, pivot):
                pivots[pivot] += 1
            if is_almost_pivot(line, pivot):
                almost_pivots[pivot] += 1

    # A "pivot off by one" is a point which is a pivot for all but one lines
    # (`len(lines) - 1`) and which is an "almost pivot" for exactly one other
    # line.
    intersection = (
            {p for p, count in almost_pivots.items() if count == 1} &
            {p for p, count in pivots.items() if count == len(lines) - 1})

    if intersection:
        assert len(intersection) == 1
        return min(intersection)


print(summarize_with(patterns, get_pivot))
print(summarize_with(patterns, get_pivots_off_by_one))
