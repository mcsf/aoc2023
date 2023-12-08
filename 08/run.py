#!/usr/bin/python3

from sys import stdin
from re import findall
from math import lcm


def parse():
    instructions, rest = stdin.read().strip().split('\n\n')
    network = {}
    for line in rest.split('\n'):
        node, *edges = findall(r'\w+', line)
        network[node] = edges
    return instructions, network


def count_steps_one(node='AAA'):
    step_count = 0
    idx = 0
    while not node.endswith('Z'):
        direction = 0 if instructions[idx] == 'L' else 1
        node = network[node][direction]
        idx = (idx + 1) % len(instructions)
        step_count += 1
    return step_count


def count_steps_all():
    nodes = (n for n in network if n.endswith('A'))
    counts = map(count_steps_one, nodes)
    return lcm(*counts)


instructions, network = parse()
print(count_steps_one())
print(count_steps_all())
