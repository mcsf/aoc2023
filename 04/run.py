#!/usr/bin/env python3

from re import sub
from sys import stdin


def parse_card(line) -> tuple[set, list]:
    line = line.split(': ')[1]
    line = sub('  +', ' ', line)
    lhs, rhs = (s.strip() for s in line.split(' | '))
    win = set(map(lambda s: int(s.strip()), lhs.split(' ')))
    hav = list(map(lambda s: int(s.strip()), rhs.split(' ')))
    return win, hav


def count_points(cards):
    return sum(int(pow(2, sum(1 for n in hav if n in win) - 1))
               for win, hav in cards)


def earn_scratchcards(cards):
    counts = dict((i, 1) for i in range(len(cards)))
    for i, (win, hav) in enumerate(cards):
        count = sum(1 for n in hav if n in win)
        for j in range(i + 1, i + 1 + count):
            counts[j] += counts[i]
    return sum(counts.values())


cards = list(map(parse_card, stdin))
print(count_points(cards))
print(earn_scratchcards(cards))
