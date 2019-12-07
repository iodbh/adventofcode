from ...classes import Solution
from ..classes import IntCode
from copy import copy
from itertools import permutations


def phase1(data):

    amplifier_program = data
    commputers = [IntCode(memory=copy(amplifier_program), silent=True) for _ in range(5)]
    max_output = 0
    for combination in permutations(range(5), 5):
        inp = 0
        for idx, phase_setting in enumerate(combination):
            computer = commputers[idx]
            computer.reset()
            _, out = computer.run_program(inputs=[phase_setting, inp])
            inp = out[0]
        if inp > max_output:
            max_output = inp
    return max_output


def run_feedback_loop(computers):
    input_output = [0]
    running = True
    while running:
        for name, computer in zip(("A", "B", "C", "D", "E"), computers):
            mem, input_output = computer.run_program(inputs=input_output)
            if not computer.waiting:
                if name == "E":
                    return input_output[-1]


def phase2(data):
    amplifier_program = data
    max_output = 0
    computers = [IntCode(memory=copy(amplifier_program), silent=True, input_wait=True) for _ in range(5)]
    for combination in permutations(range(5, 10), 5):
        for idx, computer in enumerate(computers):
            computer.reset()
            # send phase settings
            computer.run_program(inputs=[combination[idx]])
        loop_output = run_feedback_loop(computers)
        if loop_output > max_output:
            max_output = loop_output
    return max_output


solution = Solution(2019, 7, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
