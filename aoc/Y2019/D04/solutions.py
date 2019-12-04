from ...classes import Solution
from typing import Tuple, List


def parse_input(data: List[str]) -> Tuple[int]:
    return tuple(int(i) for i in data[0].strip().split('-'))


def is_valid_solution(n: str, p2=False) -> bool:
    digits = tuple(int(c) for c in n)
    last_index = len(n) - 1
    sequence_length = 1
    has_sequence = False
    has_pair = False
    prev = 0
    for i, d in enumerate(digits):
        if d < prev:
            return False
        elif i > 0 and d == prev:
            has_sequence = True
            sequence_length += 1
            if i == last_index and sequence_length == 2:
                has_pair = True
        else:
            if sequence_length == 2:
                has_pair = True
            sequence_length = 1
        prev = d
    if p2 and not has_pair:
        return False
    if has_sequence:
        return True
    return False


def count_solutions(minval, maxval, p2=False):
    solutions = 0
    for n in range(minval, maxval + 1):
        if is_valid_solution(str(n), p2=p2):
            solutions += 1
    return solutions


def phase1(data):
    return count_solutions(*data)


def phase2(data):
    return count_solutions(*data, p2=True)


solution = Solution(2019, 4, phase1=phase1, phase2=phase2, input_parser=parse_input)
