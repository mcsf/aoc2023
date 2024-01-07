#!/bin/sh

buf="$(cat)"
echo "$buf" | awk -f part1.awk | python3
echo "$buf" | python3 part2.py
