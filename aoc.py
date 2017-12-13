import aoc
from sys import argv
import pkgutil
import re


def discover_solutions():

    solutions = {}

    YEAR_PKG_REGEX = r'^(?:.*\.)*Y([0-9][0-9][0-9][0-9])$'
    DAY_PKG_REGEX = r'^(?:.*\.)*D([0-9][0-9])$'

    prefix = aoc.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(aoc.__path__, prefix):
        match = re.search(YEAR_PKG_REGEX, modname)
        if ispkg and match:
            year = match.groups()[0]
            solutions[year] = {}
            year_module = importer.find_module(modname).load_module(modname)
            for importer, inmodname, ispkg in pkgutil.iter_modules(year_module.__path__, modname + '.'):
                match = re.search(DAY_PKG_REGEX, inmodname)
                if ispkg and match:
                    day = match.groups()[0]
                    day_module = importer.find_module(inmodname).load_module(inmodname)
                    solutions[year][day] = day_module.solution
    return solutions


if __name__ == '__main__':
    if len(argv) <3 :
        exit(f'Usage : {argv[0]} [YEAR] [DAY|all]')
    solutions = discover_solutions()
    available_years = solutions.keys()
    year = argv[1]
    if year not in available_years:
        exit(f'YEAR must be one of [{", ".join(available_years)}]')
    available_days = list(solutions[year].keys())
    available_days.insert(0, "all")
    day = argv[2]
    if day not in available_days:
        exit(f'DAY must be one of [{", ".join(available_days)}]')
    if day == 'all':
        for solution in solutions[year].values():
            print(solution)
    else:
        print(solutions[year][day])
