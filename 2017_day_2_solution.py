from utils import get_input
from itertools import permutations


def parse_input(input):
    out = []
    for line in input:
        out.append(list(int(x) for x in line.split()))
    return out


def solution_2_1(input):
    checksum = 0
    for line in input:
        checksum += (max(line)-min(line))
    return checksum


def solution_2_2(input):
    checksum = 0
    for line in input:
        for a, b in permutations(line, 2):
            if a % b == 0:
                checksum += (a//b)
                break
    return checksum


if __name__ == '__main__':
    print(solution_2_1(parse_input(get_input(2017, 2))))
    print(solution_2_2(parse_input(get_input(2017, 2))))