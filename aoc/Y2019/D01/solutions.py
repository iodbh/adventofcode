from ...classes import Solution
from math import floor


def parse_input(data):
    return [int(item) for item in data]


def get_fuel_for_mass(mass: int):
    return floor(mass/3) - 2


def get_total_fuel_for_module(module_mass):
    fuel_mass = get_fuel_for_mass(module_mass)
    additional = get_fuel_for_mass(fuel_mass)
    while additional > 0:
        fuel_mass += additional
        additional = get_fuel_for_mass(additional)
    return fuel_mass


def phase1(data):
    return sum(map(get_fuel_for_mass, data))


def phase2(data):
    return sum(map(get_total_fuel_for_module, data))


solution = Solution(2019, 1, phase1=phase1, phase2=phase2, input_parser=parse_input)
