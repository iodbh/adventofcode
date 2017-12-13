from ...classes import Solution
from itertools import permutations

def parse_input(data):
    out = []
    for line in data:
        out.append(list(int(x) for x in line.split()))
    return out


def phase1(data):
    checksum = 0
    for line in data:
        checksum += (max(line)-min(line))
    return checksum


def phase2(data):
    checksum = 0
    for line in data:
        for a, b in permutations(line, 2):
            if a % b == 0:
                checksum += (a//b)
                break
    return checksum


solution = Solution(2017, 2, phase1=phase1, phase2=phase2, input_parser=parse_input)