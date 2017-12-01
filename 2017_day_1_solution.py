from utils import get_input

def solution1(input):
    input = [int(x) for x in input.strip()]
    last = len(input)-1
    output = 0
    for idx, val in enumerate(input):
        if idx < last:
            next_idx = idx + 1
        else:
            next_idx = 0
        if val == input[next_idx]:
            output += val
        if next_idx == 0:
            return output

if __name__ == '__main__':
    print(solution1(get_input(2017,1)))
