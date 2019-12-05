from ...classes import Solution
from ..classes import IntCode


def phase1(data):
    computer = IntCode(data, debug=True)
    state, screen_output = computer.run_program()
    return screen_output[-1]


def phase2(data):
    return None


solution = Solution(2019, 5, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
