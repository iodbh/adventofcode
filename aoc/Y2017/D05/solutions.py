from ...classes import Solution


def parse_input(data):
    return [int(x) for x in data]


def phase1(data):
    pos = 0
    counter = 0
    while True:
        try:
            njumps = data[pos]
        except IndexError:
            return counter
        counter += 1
        data[pos] += 1
        pos += njumps


def phase2(data):
    pos = 0
    counter = 0
    while True:
        try:
            njumps = data[pos]
        except IndexError:
            return counter
        counter += 1
        if data[pos] >= 3:
            data[pos] -= 1
        else:
            data[pos] += 1
        pos += njumps


solution = Solution(2017, 5, phase1=phase1, phase2=phase2, input_parser=parse_input)
