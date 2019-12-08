import pkg_resources
from os.path import isfile
from os import linesep
from .exceptions import AOCException, AOCNoInputException
from copy import deepcopy
from typing import Callable, Any, Union, List


class Solution:

    def __init__(
            self,
            year: str,
            day: int,
            phase1: Callable[[Any], Union[str, int, float]] = None,
            phase2: Callable[[Any], Union[str, int, float]] = None,
            input_parser: Callable[[List[str]], Any] = None,
            test: bool = False
    ):

        self.year = year
        self.day = day

        self.test = test
        self.input_path = pkg_resources.resource_filename('aoc', f'Y{year}/inputs/{day:02}{"_test" if self.test else ""}')
        if not isfile(self.input_path):
            raise AOCNoInputException(f'Missing input file for year {year} day {day}')

        self.phase1 = phase1
        self.phase2 = phase2
        self.input_parser = input_parser

    @property
    def result(self):
        if not hasattr(self, '_result'):
            self._result = {"01": None, "02": None}
            input_data = self.parse_input(self._read_input())
            for phase in ("01", "02"):
                try:
                    self._result[phase] = self._solve(phase, deepcopy(input_data))
                except NotImplementedError:
                    self._result[phase] = "Not solved yet !"
        return self._result

    def __repr__(self):
        return f'[ {self.year} - {self.day:02} {"(Test)" if self.test else ""} ]' \
               f'{linesep}    [+] Phase 01: {self.result["01"]}' \
               f'{linesep}    [+] Phase 02: {self.result["02"]}'

    def _solve(self, phase, data):
        if phase == '01':
            return self.phase_1(data)
        elif phase == '02':
            return self.phase_2(data)
        else:
            raise AOCException('Phase must be either "01" or "02"')

    def _read_input(self):
        with open(self.input_path, 'r') as f:
            return f.readlines()

    def parse_input(self, data):
        if self.input_parser is not None:
            return self.input_parser(data)
        return data

    def phase_1(self, data):
        if self.phase1 is not None:
            return self.phase1(data)
        raise NotImplementedError("No solution provided for phase 1")

    def phase_2(self, data):
        if self.phase2 is not None:
            return self.phase2(data)
        raise NotImplementedError("No solution provided for phase 1")
