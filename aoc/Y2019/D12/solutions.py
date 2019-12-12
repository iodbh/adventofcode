from ...classes import Solution
from operator import add
from itertools import combinations
from typing import Tuple
from copy import deepcopy
from math import gcd


class Body:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]

    def apply_velocity(self):
        self.position = list(map(add, self.position, self.velocity))

    @property
    def potential_energy(self):
        return sum(abs(value) for value in self.position)

    @property
    def kinectic_energy(self):
        return sum(abs(value) for value in self.velocity)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinectic_energy

    def __repr__(self):
        return f"pos=<x={self.position[0]}, y={self.position[1]}, z={self.position[2]}>, vel=<x={self.velocity[0]}, y={self.velocity[1]}, z={self.velocity[2]}>"


def parse_input(data):
    out = []
    for line in data:
        line = line.strip("<>\n")
        x, y, z = (int(d[1]) for d in (c.split("=") for c in line.split(",")))
        out.append((x, y, z))
    return out


def simulate(bodies: Tuple[Body]):
    step = 1
    while True:
        for b1, b2 in combinations(bodies, 2):
            apply_gravity(b1, b2)
        for body in bodies:
            body.apply_velocity()
        yield step
        step += 1


def apply_gravity(b1, b2):
    for axis, (axpos1, axpos2) in enumerate(zip(b1.position, b2.position)):
        if axpos1 > axpos2:
            b1.velocity[axis] -= 1
            b2.velocity[axis] += 1
        elif axpos1 < axpos2:
            b1.velocity[axis] += 1
            b2.velocity[axis] -= 1


def phase1(data):
    bodies = tuple(Body(*pos) for pos in data)
    for step in simulate(bodies):
        if step == 1000:
            return sum(b.total_energy for b in bodies)


def phase2(data):
    bodies = tuple(Body(*pos) for pos in data)
    initial_bodies = deepcopy(bodies)
    dimsteps = []
    for dimension in range(3):
        initstep = [None, None, None]
        for step in simulate(bodies):
            if all(b.position[dimension] == orig.position[dimension] and b.velocity[dimension] == 0 for b, orig in zip(bodies, initial_bodies)):
                if initstep[dimension] is None:
                    initstep[dimension] = step
                else:
                    dimsteps.append(step-initstep[dimension])
                    break

    # get the lowest common mutiple for the 3 steps numbers
    gcd2 = gcd(dimsteps[1], dimsteps[2])
    lcm2 = dimsteps[1] * dimsteps[2] // gcd2
    lcm3 = dimsteps[0] * lcm2 // gcd(dimsteps[0], lcm2)

    return lcm3


solution = Solution(2019, 12, phase1=phase1, phase2=phase2, input_parser=parse_input)
