from ...classes import Solution


def phase1(data):
    data = [int(x) for x in data[0].strip()]
    output = 0
    for idx, val in enumerate(data):
        next_idx = (idx + 1)%len(data)
        if val == data[next_idx]:
                output += val
    return output


def phase2(data):
    data = [int(x) for x in data[0].strip()]
    output = 0
    nsteps = int(len(data) / 2)
    for idx, val in enumerate(data):
        next_idx = (idx+nsteps)%len(data)
        if val == data[next_idx]:
            output += val
    return output


solution = Solution(2017, 1, phase1=phase1, phase2=phase2)

