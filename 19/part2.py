from typing import NamedTuple
from math import prod
from re import findall, match


class Rule(NamedTuple):
    var: str
    op: str
    val: int
    dst: str


class Flow(NamedTuple):
    rules: list[Rule]
    default: str


class Ranges(NamedTuple):
    x: range = range(1, 4001)
    m: range = range(1, 4001)
    a: range = range(1, 4001)
    s: range = range(1, 4001)

    def _set(self, k, v) -> "Ranges":
        """Like `_replace`, but with dynamic keys."""
        d = self._asdict()
        d[k] = v
        return Ranges(*d.values())


def parse_flow(line: str) -> tuple[str, Flow]:
    head, *rules, default = findall(r"[^{},]+", line)
    return head, Flow(list(map(parse_rule, rules)), default)


def parse_rule(s: str) -> Rule:
    assert (m := match(r"([xmas])([<>])(\d+):(\w+)", s))
    var, op, val, dst = m.groups()
    return Rule(var, op, int(val), dst)


LINES = open(0).read().split("\n\n")[0].split("\n")
FLOWS = dict(map(parse_flow, LINES))


def possibs(ranges: Ranges, flow: str):
    if flow == "A":
        return prod(len(r) for r in ranges)

    if flow == "R":
        return 0

    total = 0
    for rule in FLOWS[flow].rules:
        rule_constraints, ranges = partition(ranges, rule)
        total += possibs(rule_constraints, rule.dst)

    total += possibs(ranges, FLOWS[flow].default)
    return total


def partition(ranges: Ranges, rule: Rule) -> tuple[Ranges, Ranges]:
    r: range = ranges._asdict()[rule.var]
    val = rule.val if rule.op == "<" else rule.val + 1
    rs1 = ranges._set(rule.var, range(r.start, val))
    rs2 = ranges._set(rule.var, range(val, r.stop))
    return (rs1, rs2) if rule.op == "<" else (rs2, rs1)


print(possibs(Ranges(), "in"))
