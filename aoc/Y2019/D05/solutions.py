from ...classes import Solution
from ..classes import IntCode


def phase1(data):
    computer = IntCode(data, silent=True)
    state, screen_output = computer.run_program(inputs=[1])
    return screen_output[-1]


def phase2(data):
    computer = IntCode(data, silent=True)
    state, screen_output = computer.run_program(inputs=[5])
    return screen_output[0]


solution = Solution(2019, 5, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
