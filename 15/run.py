#!/usr/bin/env python3

from sys import stdin
from re import match
from collections import defaultdict
from functools import reduce


def my_hash(s: str) -> int:
    return reduce(lambda h, c: ((h + ord(c)) * 17) % 256, s, 0)


def my_hashmap(boxes, instruction):
    assert (m := match(r"([a-z]+)([=-])(\d+)?", instruction))
    label, op, length_raw = m.groups()

    if op == "-":
        for box in boxes.values():
            if label in box:
                box.pop(label)
                break

    else:
        dst = my_hash(label)
        boxes[dst][label] = int(length_raw)

    return boxes


def score(boxes):
    return sum((i + 1) * (j + 1) * v
               for i, box in boxes.items()
               for j, v in enumerate(box.values()))


instructions = stdin.read().strip().split(",")
print(sum(my_hash(ins) for ins in instructions))
print(score(reduce(my_hashmap, instructions, defaultdict(dict))))
