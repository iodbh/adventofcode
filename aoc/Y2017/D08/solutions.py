from ...classes import Solution
from collections import namedtuple

Instruction = namedtuple("Instruction", "register operation value left operator right")


class CPU:
    def __init__(self):
        self.registers = {}

    def _dereference_register(self, register):
        if register not in self.registers:
            self.registers[register] = 0
        return self.registers[register]

    def test(self, left, operator, right):
        left_value = self._dereference_register(left)
        return eval('{} {} {}'.format(left_value, operator, right))

    def register_operation(self, register, operation, value):
        current_value = self._dereference_register(register)
        if operation == 'inc':
            new_value = current_value + value
        elif operation == 'dec':
            new_value = current_value - value
        self.registers[register] = new_value

        return new_value

    def execute(self, instruction):
        if self.test(instruction.left, instruction.operator, instruction.right):
            self.register_operation(instruction.register, instruction.operation, instruction.value)


def parse_input(data):
    output = []
    for line in data:
        elements = [i.strip() for i in line.split() if "if" not in i]
        elements[2] = int(elements[2])
        elements[-1] = int(elements[-1])
        output.append(Instruction(*elements))
    return output


def phase1(data):
    cpu = CPU()
    for instruction in data:
        cpu.execute(instruction)
    return max(cpu.registers.values())


def phase2(data):
    output = 0
    cpu = CPU()
    for instruction in data:
        cpu.execute(instruction)
        max_value = max(cpu.registers.values())
        if max_value > output:
            output = max_value
    return output


solution = Solution(2017, 8, phase1=phase1, phase2=phase2, input_parser=parse_input)
