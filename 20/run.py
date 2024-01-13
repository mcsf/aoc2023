#!/usr/bin/env python3

from re import findall
from collections import Counter
from math import prod, lcm
from itertools import count

modules = {}
for line in open(0):
    if m := findall(r"[%&]|\w+", line):
        kind = "" if m[0].islower() else m.pop(0)
        key, *dsts = m
        modules[key] = (kind, dsts)


# Initialize memory of conjunction modules
def initstate():
    states = {}
    conjs = {key for key, (kind, _) in modules.items() if kind == "&"}
    for key, (_, dsts) in modules.items():
        for dst in dsts:
            if dst in conjs:
                states.setdefault(dst, {})
                states[dst][key] = False
    return states


def flow(states, pulsein, key, src):
    if module := modules.get(key):
        kind, dsts = module

        if not kind:
            return pulsein

        elif kind == "%":
            if not pulsein:
                state = not states.get(key, False)
                states[key] = state
                return state

        elif kind == "&":
            states[key][src] = pulsein
            return not all(states[key].values())


# For part 2
rx_precursor = next(k for k in modules if "rx" in modules[k][1])
n_precursor_srcs = len({k for k in modules if rx_precursor in modules[k][1]})


def pushn():
    states = initstate()    # Module memories
    total = Counter()       # High/low pulse counts
    cycles = {}             # Time until precursor receives source's pulse

    for i in count(0):

        # Part 1
        if i == 1000:
            print(prod(total.values()))

        queue = [(False, "broadcaster", "")]    # Nodes of (pulse, dst, src)
        total[False] += 1
        while queue:
            pulsein, key, src = queue.pop(0)
            pulseout = flow(states, pulsein, key, src)
            if pulseout is not None:

                # Part 2
                if key == rx_precursor and pulsein:
                    if src not in cycles:
                        cycles[src] = i + 1
                    if len(cycles) == n_precursor_srcs:
                        print(lcm(*cycles.values()))
                        return

                for dst in modules[key][1]:
                    queue.append((pulseout, dst, key))
                    total[pulseout] += 1


pushn()
