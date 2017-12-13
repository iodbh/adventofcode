from ...classes import Solution


def parse_input(data):
    return [int(x) for x in data[0].split()]


def redistribute(memory):
    lenght = len(memory)
    nblocks = max(memory)
    idx = memory.index(nblocks)
    memory[idx] = 0
    while nblocks > 0:
        idx = (idx + 1) % lenght
        memory[idx] += 1
        nblocks -= 1
    return tuple(memory)


def get_solution_data(data):
    known_states = set()
    length = len(data)
    while True:
        nstates = len(known_states)
        known_states.add(redistribute(data))
        if len(known_states) == nstates:
            return nstates + 1, data


def phase1(data):
    return get_solution_data(data)[0]


def phase2(data):
    count = 0
    new_state = get_solution_data(data)[1]
    expected_state = tuple(new_state)
    while True:
        count += 1
        state = redistribute(data)
        if state == expected_state:
            return count


solution = Solution(2017, 6, phase1=phase1, phase2=phase2, input_parser=parse_input)
