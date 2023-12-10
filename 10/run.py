#!/usr/bin/env python3

from sys import stdin
from itertools import product


def parse():
    pipes = {}
    joints = set()

    for y, line in enumerate(stdin):
        y *= 2
        for x, c in enumerate(line.strip()):
            x *= 2
            if c == '.':
                continue
            elif c == 'S':
                start = x, y
                pipes[x, y] = []
            elif c == '|':
                pipes[x, y] = [(x, y - 2), (x, y + 2)]
                joints |= {(x, y - 1), (x, y + 1)}
            elif c == '-':
                pipes[x, y] = [(x - 2, y), (x + 2, y)]
                joints |= {(x - 1, y), (x + 1, y)}
            elif c == 'L':
                pipes[x, y] = [(x, y - 2), (x + 2, y)]
                joints |= {(x, y - 1), (x + 1, y)}
            elif c == 'J':
                pipes[x, y] = [(x, y - 2), (x - 2, y)]
                joints |= {(x, y - 1), (x - 1, y)}
            elif c == '7':
                pipes[x, y] = [(x - 2, y), (x, y + 2)]
                joints |= {(x - 1, y), (x, y + 1)}
            elif c == 'F':
                pipes[x, y] = [(x + 2, y), (x, y + 2)]
                joints |= {(x + 1, y), (x, y + 1)}

    size = x + 1, y + 1

    for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
        adj = start[0] + dx, start[1] + dy
        if adj in pipes and start in pipes[adj]:
            pipes[start].append(adj)

    return pipes, start, size, joints


def get_loop_path(pipes, curr):
    path = []
    visited = set()
    while curr not in visited:
        path.append(curr)
        visited.add(curr)
        for adj in pipes[curr]:
            if adj in pipes and curr in pipes[adj] and adj not in visited:
                curr = adj
    return path


def count_inner_tiles(path, joints, size):
    watertight = set(path) | joints
    flooded = flood(size, watertight)

    count = 0
    for y in range(size[1]):
        for x in range(size[0]):
            node = x, y
            if node not in flooded and node not in watertight:
                if x % 2 == 0 and y % 2 == 0:  # Sleight of hand
                    count += 1

    return count


def flood(size, watertight):
    queue = list(get_map_edges(size))
    flooded = set()

    while queue:
        curr = queue.pop()
        if curr not in watertight and curr not in flooded:
            flooded.add(curr)
            for adj in get_8_adjacent(size, *curr):
                queue.append(adj)

    return flooded


def get_map_edges(size):
    x_max, y_max = size[0] - 1, size[1] - 1
    for y in range(y_max + 1):
        yield (0, y)
        yield (x_max, y)

    for x in range(x_max + 1):
        yield (x, 0)
        yield (x, y_max)


def get_8_adjacent(size, x, y):
    for dx, dy in product([-1, 0, 1], repeat=2):
        xx, yy = x + dx, y + dy
        if (xx, yy) != (x, y) \
                and xx >= 0 and xx < size[0] \
                and yy >= 0 and yy < size[1]:
            yield xx, yy


def main():
    pipes, start, size, joints = parse()
    path = get_loop_path(pipes, start)
    print(len(path) // 2)
    print(count_inner_tiles(path, joints, size))


main()
