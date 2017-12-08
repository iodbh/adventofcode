from utils import get_input
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

def parse_input(input):
    for line in input:
        elements = [i.strip() for i in line.split() if "if" not in i]
        elements[2] = int(elements[2])
        elements[-1] = int(elements[-1])
        yield Instruction(*elements)


def solution_8_1(input):
    cpu = CPU()
    for instruction in input:
        print(instruction)
        cpu.execute(instruction)
    return max(cpu.registers.values())


def solution_8_2(input):
    ...


if __name__ == '__main__':

    test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".split('\n')

    print(solution_8_1(parse_input(get_input(2017, 8))))
    #print(solution_8_2(parse_input(get_input(2017, 8))))