#!/usr/bin/env python3

from sys import stdin
from re import findall
from math import prod


def parse():
    def ints(s):
        return list(map(int, findall(r'\d+', s)))

    def concat(ns):
        return int(''.join(str(n) for n in ns))

    ts = ints(next(stdin))
    ds = ints(next(stdin))
    quick_races = list(zip(ts, ds))
    long_race = (concat(ts), concat(ds))

    return quick_races, long_race


def try_race(t_max, d_min, t_accel):
    speed = t_accel
    t_moving = t_max - t_accel
    return speed * t_moving


def win_count(race):
    t_max, d_min = race
    count = 0
    for t_accel in range(t_max):
        if try_race(t_max, d_min, t_accel) > d_min:
            count += 1
    return count


quick_races, long_race = parse()
print(prod(map(win_count, quick_races)))
print(win_count(long_race))  # Naive, but only takes 4s on M1 Pro
