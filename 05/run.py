#!/usr/bin/env python3

from sys import stdin
from re import findall
from collections import namedtuple
from collections.abc import Iterator

Range = namedtuple('Range', ['start', 'end'])
Mapping = namedtuple('Mapping', ['dst', 'src', 'len'])


def parse():
    def ints(s: str) -> list[int]:
        return list(map(int, findall(r'\d+', s)))

    head, *body = stdin.read().strip().split('\n\n')
    seeds = ints(head)
    cmaps = [[Mapping(*ints(line)) for line in block.split('\n')[1:]]
             for block in body]

    return seeds, cmaps


def part1():
    print(min(map(convert_to_location, seeds)))


def part2():
    seed_ranges = list(as_ranges(seeds))
    location_ranges = convert_to_location_ranges(seed_ranges)
    print(min(rg.start for rg in location_ranges))


def convert_to_location(seed: int) -> int:
    val = seed
    for mappings in cmaps:
        for m in mappings:
            if m.src <= val <= m.src + m.len - 1:
                val += m.dst - m.src
                break
    return val


def as_ranges(lst) -> Iterator[Range]:
    for i in range(0, len(lst), 2):
        start, length = lst[i:i+2]
        end = start + length - 1
        yield Range(start, end)


# Given a list of seed ranges, successively convert the list of ranges
# corresponding to one source (e.g. seed) to the next (e.g. soil), all the way
# to the final range of locations, according to each source's mappings.
def convert_to_location_ranges(seed_ranges: list[Range]) -> list[Range]:
    source_ranges = seed_ranges
    for mappings in cmaps:
        next_ranges = []
        for rg in source_ranges:
            converted_rgs = convert_range(rg, mappings)
            next_ranges += converted_rgs
        source_ranges = next_ranges
    return source_ranges


def convert_range(rg: Range, mappings: list[Mapping]) -> list[Range]:
    # Resulting ranges
    next_ranges = []  # type: list[Range]

    # Track which ranges within `rg` are matched by mappings, so that later on
    # we can find any gaps and plug them.
    matched_source_ranges = set()  # type: set[Range]

    for m in mappings:
        m_end = m.src + m.len - 1

        # If a mapping overlaps the source range, compute the corresponding
        # destination range
        if rg.start <= m_end and rg.end >= m.src:
            new_start = max(rg.start, m.src)
            new_end = min(rg.end, m_end)
            diff = m.dst - m.src
            next_ranges.append(Range(new_start + diff, new_end + diff))
            matched_source_ranges.add(Range(new_start, new_end))

    if not next_ranges:
        return [rg]

    # If there are gaps in the source's mappings, make sure to plug them.
    # Whenever a gap is found, the destination range is equal to the source
    # range.
    if gaps := find_gaps(rg, list(sorted(matched_source_ranges))):
        next_ranges += gaps
        next_ranges.sort()

    return next_ranges


# Find gaps, i.e. parts of the range defined in `limits` that are not covered
# by any of the ranges in `ranges`. Assumes that `ranges` is sorted and that
# ranges in `ranges` don't overlap
def find_gaps(limits: Range, ranges: list[Range]) -> list[Range]:
    result = []  # type: list[Range]

    # Case: gap at the beginning
    if limits.start < ranges[0].start:
        result.append(Range(limits.start, ranges[0].start - 1))

    # Case: gap in between ranges
    for prev, curr in zip(ranges, ranges[1:]):
        if curr.start - prev.end > 1:
            result.append(Range(prev.end + 1, curr.start - 1))

    # Case: gap at the end
    if ranges[-1].end < limits.end:
        result.append(Range(ranges[-1].end + 1, limits.end))

    return result


seeds, cmaps = parse()
part1()
part2()
