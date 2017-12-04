from utils import get_input


def parse_input(input):
    return [l.split() for l in input]


def solution_4_1(input):
    valid_count = len(input)
    print(valid_count)
    for line in input:
        while len(line):
            word = line.pop()
            if word in line:
                valid_count -= 1
                print('invalid')
                break
    print(valid_count)
    return valid_count


if __name__ == '__main__':
    print(solution_4_1(parse_input(get_input(2017, 4))))