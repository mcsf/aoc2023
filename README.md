Advent of Code 2023 🎄
======================

→ https://adventofcode.com/2023


Directory structure
-------------------

```
├ test.sh    — Test runner for entire repository
│
├ 01         - Day 1
│ ├ input    - Individual input puzzle (not included)
│ ├ sample   - Sample puzzle from the problem statement
│ ├ expected - Expected output for puzzle solvers
│ ├ run.py   - Puzzle solver (any executable file matching `^run.`)
│ └ run.hs   - There can be more than one solver per day
│
├ 02
│ ├ input
…
```

Testing
-------

```
# Run all tests
./test.sh

# Run for a given day
./test.sh 04
```
