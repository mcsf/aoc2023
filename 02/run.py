#!/usr/bin/env python3

from sys import stdin
from math import prod
from re import search


def parse_game(line):
    head, body = line.strip().split(': ')
    game_id = int(search(r'\d+', head)[0])
    sets = [dict((color, int(n))
                 for (n, color) in (draw.split(' ') for draw in s.split(', ')))
            for s in body.split('; ')]
    return (game_id, sets)


def exceeds_constraints(s):
    constraints = [('red', 12), ('green', 13), ('blue', 14)]
    return any(s.get(color, 0) > val for (color, val) in constraints)


def power(sets):
    return prod(max(s.get(c, 0) for s in sets)
                for c in ['red', 'green', 'blue'])


games = [parse_game(line) for line in stdin]

print(sum(game_id
          for game_id, sets in games
          if not any(exceeds_constraints(s) for s in sets)))

print(sum(power(sets) for _, sets in games))
