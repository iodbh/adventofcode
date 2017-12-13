from ...classes import Solution


def parse_input(data):
    return [l.split() for l in data]


def phase1(data):
    valid_count = len(data)
    for line in data:
        while len(line):
            word = line.pop()
            if word in line:
                valid_count -= 1
                break
    return valid_count


def phase2(data):
    valid_count = len(data)
    for line in data:
        split_line = [sorted(list(w)) for w in line]
        while len(split_line):
            word = split_line.pop()
            if word in split_line:
                valid_count -= 1
                break
    return valid_count


solution = Solution(2017, 4, phase1=phase1, phase2=phase2, input_parser=parse_input)