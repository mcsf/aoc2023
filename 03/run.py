#!/usr/bin/env python3

from sys import stdin
from re import finditer
from itertools import count
from math import prod

ids = count()  # Generator of unique IDs for numbers
nums = dict()  # Map of (x, y) -> (number, ID)
syms = dict()  # Map of (x, y) -> symbol

for y, line in enumerate(stdin):
    line = line.strip()

    # Scan for numbers and map them in `nums`
    for match in finditer(r'\d+', line):
        num = int(match.group())
        nid = next(ids)
        for x in range(*match.span()):
            nums[(x, y)] = (num, nid)

    # Scan for symbols and map them in `syms`
    for match in finditer(r'[^\d.]', line):
        x, _ = match.span()
        sym = match.group()
        syms[(x, y)] = sym


adj_nums = set()  # Part 1
ratio_sum = 0     # Part 2

for (x, y), sym in syms.items():
    gear = set()
    for dx, dy in [(-1, -1), (-1, +0), (-1, +1),
                   (+0, -1),           (+0, +1),
                   (+1, -1), (+1, +0), (+1, +1)]:
        if found := nums.get((x + dx, y + dy)):
            adj_nums.add(found)
            gear.add(found)
    if sym == '*' and len(gear) == 2:
        ratio_sum += prod(num for (num, _) in gear)

print(sum(num for (num, nid) in adj_nums))
print(ratio_sum)
