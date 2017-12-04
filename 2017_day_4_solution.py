from utils import get_input


def parse_input(input):
    return [l.split() for l in input]


def solution_4_1(input):
    valid_count = len(input)
    for line in input:
        while len(line):
            word = line.pop()
            if word in line:
                valid_count -= 1
                break
    return valid_count


def solution_4_2(input):
    valid_count = len(input)
    for line in input:
        split_line = [sorted(list(w)) for w in line]
        while len(split_line):
            word = split_line.pop()
            if word in split_line:
                valid_count -= 1
                break
    return valid_count


if __name__ == '__main__':
    print(solution_4_1(parse_input(get_input(2017, 4))))
    print(solution_4_2(parse_input(get_input(2017, 4))))