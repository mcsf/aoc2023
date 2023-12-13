from sys import stdin
from itertools import groupby, combinations
from math import comb

records = []
for line in stdin:
    springs, code = line.strip().split(' ')
    springs = list(springs)  # type: ignore
    code = list(map(int, code.split(',')))  # type: ignore
    records.append((springs, code))


def satisfies(springs, code):
    return code == [len(list(g)) for k, g in groupby(springs) if k == '#']


def count_assignments(record):
    _, code = record
    return sum(1 for springs in generate_assignments(record)
               if satisfies(springs, code))


def generate_assignments(record):
    springs, code = record

    # Number of '#' left to assign
    n = sum(code) - sum(1 for x in springs if x == '#')

    # Slots into which to assign them
    slots = [i for i, c in enumerate(springs) if c == '?']

    print(''.join(springs), code, 'with', comb(len(slots), n), 'combinations')

    for slot_assignments in combinations(slots, n):
        yield assign(springs, slot_assignments)


def assign(springs, slot_assignments):
    result = []
    for i in range(len(springs)):
        spring = springs[i]
        if i in slot_assignments:
            spring = '#'
        elif springs[i] == '?':
            spring = '.'
        result.append(spring)
    return result


def unfold(record):
    springs, code = record
    new_springs = springs.copy()
    for i in range(4):
        new_springs += ['?'] + springs
    return new_springs, 5 * code


# print(records[0])
# print(unfold(records[0]))
print(sum(count_assignments(r) for r in records), flush=True)
print(sum(count_assignments(unfold(r)) for r in records), flush=True)
