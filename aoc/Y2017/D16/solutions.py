from ...classes import Solution


PROGRAMS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']


def spin(datalist, n):
    for idx, value in enumerate(datalist[:]):
        datalist[(idx+n)%len(datalist)] = value


def exchange(datalist, index_a, index_b):
    datalist[index_a], datalist[index_b] = datalist[index_b], datalist[index_a]


def partner(datalist, a, b):
    exchange(datalist, datalist.index(a), datalist.index(b))


def step(programs, step):
    if step.startswith('s'):
        size = int(step[1:])
        spin(programs, size)
    elif step.startswith('x'):
        idx_a, idx_b = (int(i) for i in step[1:].split('/'))
        exchange(programs, idx_a, idx_b)
    elif step.startswith('p'):
        a, b = step[1:].split('/')
        partner(programs, a, b)


def dance(programs, steps, nsteps):
    for n in range(1,nsteps+1):
        for idx, inst in enumerate(steps):
            step(programs, inst)
            if programs == PROGRAMS:
                remaining_steps = (nsteps % n) + (len(steps) - (idx+1))
                return dance(programs, steps, remaining_steps)
    return ''.join(programs)


def parse_input(data):
    text = data[0].strip()
    return text.split(',')


def phase1(data):
    programs = PROGRAMS[:]
    for inst in data:
        step(programs, inst)
    return ''.join(programs)


def phase_2(data):
    programs = PROGRAMS[:]
    nsteps = 1000000000
    return dance(programs, data, nsteps)


solution = Solution(2017, 16, phase1=phase1, phase2=phase_2, input_parser=parse_input)
