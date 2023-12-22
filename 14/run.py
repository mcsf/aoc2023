#!/usr/bin/env python3

from sys import stdin
from functools import cache

lines = tuple(stdin.read().strip().split('\n'))


@cache
def shift(line: str) -> str:
    """
    Shift a line of rocks to the left:

        shift("..O.#.O") == "O...#O."
    """

    # No round rocks, so nothing to shift around
    if "O" not in line:
        return line

    # Rock already at the start, so continue with the rest of the line
    if not (rock := line.index("O")):
        return "O" + shift(line[1:])

    # Find obstacle closest to the rock, moving to the left
    obst = None
    for i in range(rock - 1, -1, -1):
        if line[i] != ".":
            obst = i
            break

    # No obstacle found: rock can shift to the start
    if obst is None:
        return "O" + shift(line[1:rock] + "." + line[rock+1:])

    # Obstacle already holding rock, so jump to whatever follows the rock
    if obst == rock - 1:
        return line[:rock+1] + shift(line[rock+1:])

    # Shift rock towards obstacle
    return (line[:obst+1] + "O" +
            shift(line[obst+2:rock] + "." + line[rock+1:]))


@cache
def line_load(line: str) -> int:
    """
    Calculate the load of round rocks on a line, weighted from right to left.
    """
    return sum(i for (i, c) in enumerate(reversed(line), start=1) if c == "O")


@cache
def transpose(grid):
    """
    Transpose a grid of characters, thus turning a sequence of rows into a
    sequence of columns, and vice-versa.
    """
    return tuple(''.join(line) for line in zip(*grid))


def north_load(grid: tuple[str, ...]) -> int:
    """
    Calculate the total North-based load of round rocks on a grid. Assumes the
    grid is configured as a sequence of rows, not columns.
    """
    return sum(line_load(col) for col in transpose(grid))


def tilt_fourways(grid):
    """
    Run a cycle of four tilts (N, W, S, E).
    """

    def tilt(line, is_reversed):
        return shift(line) if not is_reversed else shift(line[::-1])[::-1]

    for t in ("N", "W", "S", "E"):
        is_reversed = t in ("S", "E")
        grid = tuple(tilt(line, is_reversed) for line in transpose(grid))

    return grid


def tilt_n(grid, n):
    """
    Run `n` cycles of four tilts.
    """
    curr = grid
    history = {curr: 0}

    has_jumped = False
    i = 1
    while i <= n:
        curr = tilt_fourways(curr)

        if not has_jumped and curr in history:
            loop_length = i - history[curr]
            i = (n // loop_length) * loop_length + (i % loop_length)
            has_jumped = True

        history[curr] = i
        i += 1

    return curr


print(sum(line_load(shift(col)) for col in transpose(lines)))
print(north_load(tilt_n(lines, 1000000000)))
