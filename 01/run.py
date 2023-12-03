#!/usr/bin/env python3

from re import findall
from sys import stdin


def value_pt1(s):
    digits = [c for c in s if c.isnumeric()]
    return int(digits[0] + digits[-1]) if digits else 0


NS = ['one', 'two', 'three', 'four', 'five',
      'six', 'seven', 'eight', 'nine']

# Use lookahead (?=) to catch overlapping words (e.g. oneight)
RE = '(?=(' + '|'.join([str(n) for n in range(10)] + NS) + '))'


def value_pt2(s):
    matches = findall(RE, s)
    digits = [d if d.isnumeric() else str(NS.index(d)+1) for d in matches]
    return int(digits[0] + digits[-1])


lines = [line.strip() for line in stdin]
print(sum(value_pt1(line) for line in lines))
print(sum(value_pt2(line) for line in lines))
