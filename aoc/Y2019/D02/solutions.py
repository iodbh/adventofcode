from ...classes import Solution
from ..classes import IntCode


def bruteforce_inputs(initial_memory, target):
    computer = IntCode(memory=initial_memory, debug=False)

    for noun in range(0, 100):
        for verb in range(0, 100):
            computer.reset()
            computer.memset(1, noun)
            computer.memset(2, verb)
            output = computer.run_program()[0]
            if output == target:
                return noun, verb


def phase1(data):
    data[1] = 12
    data[2] = 2
    computer = IntCode(data)
    state = computer.run_program()
    return state[0]


def phase2(data):
    print(2)
    print(data)
    noun, verb = bruteforce_inputs(data, 19690720)
    return 100 * noun + verb


solution = Solution(2019, 2, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
