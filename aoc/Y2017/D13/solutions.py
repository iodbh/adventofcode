"""
This solution is from https://www.reddit.com/r/adventofcode/comments/7jgyrt/2017_day_13_solutions/
"""

from ...classes import Solution
import itertools


def parse_input(data):
    return {int(pos): int(height) for pos, height in (line.split(': ') for line in data)}


def scanner(height, time):
    offset = time % ((height - 1) * 2)

    return 2 * (height - 1) - offset if offset > height - 1 else offset


def phase1(data):
    return sum(pos * data[pos] for pos in data if scanner(data[pos], pos) == 0)


def phase2(data):
    return next(wait for wait in itertools.count() if not any(scanner(data[pos], wait + pos) == 0 for pos in data))


solution = Solution(2017, 13, phase1=phase1, phase2=phase2, input_parser=parse_input)