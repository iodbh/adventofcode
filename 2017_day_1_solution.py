from utils import get_input

def solution_1_1(input):
    input = [int(x) for x in input[0].strip()]
    output = 0
    for idx, val in enumerate(input):
        next_idx = (idx + 1)%len(input)
        if val == input[next_idx]:
                output += val
    return output


def solution_1_2(input):
    input = [int(x) for x in input[0].strip()]
    output = 0
    nsteps = int(len(input)/2)
    for idx, val in enumerate(input):
        next_idx = (idx+nsteps)%len(input)
        if val == input[next_idx]:
            output += val
    return output


if __name__ == '__main__':
    print(solution_1_1(get_input(2017, 1)))
    print(solution_1_2(get_input(2017, 1)))
