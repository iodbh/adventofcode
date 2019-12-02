from ...classes import Solution


def parse_input(data):
    output = []
    for line in data:
        output.extend(int(num) for num in line.split(","))
    return output


def run_intcode(memory):
    instruction_pointer = 0
    opcode = memory[instruction_pointer]
    while opcode != 99 and instruction_pointer <= len(memory) -1:
        parameter1_address = memory[instruction_pointer + 1]
        parameter1 = memory[parameter1_address]
        parameter2_address = memory[instruction_pointer + 2]
        parameter2 = memory[parameter2_address]
        dst_address = memory[instruction_pointer + 3]
        next_instruction_address = instruction_pointer + 4
        if opcode == 1:
            memory[dst_address] = parameter1 + parameter2
        elif opcode == 2:
            memory[dst_address] = parameter1 * parameter2
        instruction_pointer = next_instruction_address
        opcode = memory[instruction_pointer]
    return memory


def bruteforce_inputs(initial_memory, target):
    for noun in range(0, 100):
        for verb in range(0, 100):
            memory = initial_memory[:]
            memory[1] = noun
            memory[2] = verb
            output = run_intcode(memory)[0]
            if output == target:
                return noun, verb


def phase1(data):
    data[1] = 12
    data[2] = 2
    state = run_intcode(data[:])
    return state[0]


def phase2(data):
    noun, verb = bruteforce_inputs(data, 19690720)
    return 100 * noun + verb


solution = Solution(2019, 2, phase1=phase1, phase2=phase2, input_parser=parse_input)
