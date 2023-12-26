#!/usr/bin/env python3

class Polygon:
    def __init__(self):
        self.curr = 0+0j
        self.prev = 0+0j
        self.area = 0

    def add(self, d, n):
        # https://en.wikipedia.org/wiki/Shoelace_formula
        self.curr += n * deltas[d]
        self.area += int(
                self.prev.real * self.curr.imag
                - self.curr.real * self.prev.imag
                + n)
        self.prev = self.curr

    def realarea(self):
        return self.area // 2 + 1


directions = "RDLU"
deltas = [1, 1j, -1, -1j]
p1, p2 = Polygon(), Polygon()

for line in open(0):
    pieces = line.strip().split()
    p1.add(d=directions.index(pieces[0]), n=int(pieces[1]))
    p2.add(d=int(pieces[2][-2:-1]), n=int(pieces[2][2:-2], 16))

print(p1.realarea())
print(p2.realarea())
