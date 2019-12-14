from ...classes import Solution
from ..classes import IntCode


def phase1(data):
    computer = IntCode(debug=False, silent=True)
    mem, out = computer.run_program(data, inputs=[1])
    return out[0]


def phase2(data):
    computer = IntCode(debug=False, silent=True)
    mem, out = computer.run_program(data, inputs=[2])
    return out[0]


solution = Solution(2019, 9, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
