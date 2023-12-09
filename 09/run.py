#!/usr/bin/env python3

from sys import stdin


def predict(seq):
    start = end = 0
    derivatives = list(derive(seq))
    while derivatives:
        curr = derivatives.pop()
        start = curr[0] - start
        end = curr[-1] + end
    return start, end


def derive(seq):
    while any(seq):
        yield seq
        seq = [b - a for a, b in zip(seq, seq[1:])]


sequences = [[int(n) for n in line.strip().split(' ')] for line in stdin]
predictions = list(map(predict, sequences))
print(sum(end for start, end in predictions))
print(sum(start for start, end in predictions))
