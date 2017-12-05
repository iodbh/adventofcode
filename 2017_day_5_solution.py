from utils import get_input


def parse_input(input):
    return [int(x) for x in input]


def solution_5_1(input):
    pos = 0
    counter = 0
    while True:
        try:
            njumps = input[pos]
        except IndexError:
            return counter
        counter += 1
        input[pos] += 1
        pos += njumps


def solution_5_2(input):
    pos = 0
    counter = 0
    while True:
        try:
            njumps = input[pos]
        except IndexError:
            return counter
        counter += 1
        if input[pos] >= 3:
            input[pos] -= 1
        else:
            input[pos] += 1
        pos += njumps


if __name__ == '__main__':
    print(solution_5_1(parse_input(get_input(2017, 5))))
    print(solution_5_2(parse_input(get_input(2017, 5))))