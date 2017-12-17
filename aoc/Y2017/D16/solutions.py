from ...classes import Solution


def spin(datalist, n):
    for idx, value in enumerate(datalist[:]):
        datalist[(idx+n)%len(datalist)] = value


def exchange(datalist, index_a, index_b):
    datalist[index_a], datalist[index_b] = datalist[index_b], datalist[index_a]


def partner(datalist, a, b):
    exchange(datalist, datalist.index(a), datalist.index(b))


def parse_input(data):
    text = data[0].strip()
    return text.split(',')


def phase1(data):
    programs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    for step in data:
        if step.startswith('s'):
            size = int(step[1:])
            spin(programs, size)
        elif step.startswith('x'):
            idx_a, idx_b = (int(i) for i in step[1:].split('/'))
            exchange(programs, idx_a, idx_b)
        elif step.startswith('p'):
            a, b = step[1:].split('/')
            partner(programs, a, b)
    return ''.join(programs)


solution = Solution(2017, 16, phase1=phase1, input_parser=parse_input)
