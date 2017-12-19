from ...classes import Solution
from collections import deque


def parse_input(data):
    return int(data[0].strip())


def get_state_after(steps_per_cycle, ncycles):
    buffer = [0]
    position = 0
    for i in range(ncycles):
        position = (steps_per_cycle + position) % len(buffer)
        if position == len(buffer):
            buffer.append(position + 1)
        else:
            buffer.insert(position + 1, i + 1)
        position += 1
    return buffer, position


def phase1(data):
    buffer, position = get_state_after(data, 2017)
    return buffer[position+1]


def phase2(data):
    # This one is from Reddit, as my own solution was way too slow to bruteforce.
    spinlock = deque([0])

    for i in range(1, 50000001):
        spinlock.rotate(-data)
        spinlock.append(i)

    return spinlock[spinlock.index(0) + 1]


solution = Solution(2017, 17, phase1=phase1, phase2=phase2, input_parser=parse_input)