from utils import get_input


def parse_input(input):
    return [int(x) for x in input[0].split()]


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


def solution_6_1(input):
    known_states = set()
    length = len(input)
    while True:
        nstates = len(known_states)
        known_states.add(redistribute(input))
        if len(known_states) == nstates:
            return nstates+1, input


def solution_6_2(input):
    count = 0
    new_state = solution_6_1(input)[1]
    expected_state = tuple(new_state)
    while True:
        count += 1
        state = redistribute(input)
        if state == expected_state:
            return count


if __name__ == '__main__':
    print(solution_6_1(parse_input(get_input(2017, 6)))[0])
    print(solution_6_2(parse_input(get_input(2017, 6))))