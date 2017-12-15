from ...classes import Solution

DIVIDER = 2147483647
FACTORS = {'A': 16807, 'B': 48271}
CRITERIA = {'A': 4, 'B': 8}


def generate(previous, factor):
    return (previous * factor) % DIVIDER

def picky_generator(start_value, factor, criteria):
    value = start_value
    while True:
        value = generate(value, factor)
        if value % criteria == 0:
            yield value


def last_16_bits(value):
    return f'{value:016b}'[-16:]


def parse_input(data):
    out = {}
    for line in data:
        l = line.split()
        generator = l[1]
        start_value = int(l[-1])
        out[generator] = start_value
    return out


def phase1(data):
    current_values = data
    count = 0
    for i in range(40000000):
        for generator in ('A', 'B'):
            current_values[generator] = generate(current_values[generator], FACTORS[generator])
        if last_16_bits(current_values['A']) == last_16_bits(current_values['B']):
            count += 1
    return count


def phase2(data):
    count = 0
    current_values = data
    generators = {}
    for g in ('A', 'B'):
        generators[g] = picky_generator(current_values[g], FACTORS[g], CRITERIA[g])
    for i in range(5000000):
        for generator in ('A', 'B'):
            current_values[generator] = next(generators[generator])
        if last_16_bits(current_values['A']) == last_16_bits(current_values['B']):
            count += 1
    return count


solution = Solution(2017, 15, phase1=phase1, phase2=phase2, input_parser=parse_input)
