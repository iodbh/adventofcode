from ...classes import Solution
from string import ascii_lowercase


class SoundProcessor:

    def __init__(self):
        self.registers = {c: 0 for c in ascii_lowercase}
        self.next_instruction = 0
        self.last_played = None

        self.instructions_map = {
            "set": self.set,
            "add": self.add,
            "mul": self.mul,
            "mod": self.mod,
            "rcv": self.rcv,
            "jgz": self.jgz,
            "snd": self.snd,
        }

    def run(self, instructions):
        self.next_instruction = 0
        while self.next_instruction < len(instructions):
            yield self.run_instruction(instructions[self.next_instruction])

    def run_instruction(self, instruction):
        instruction, *arguments = instruction.split()
        retval = self.instructions_map[instruction](*arguments)
        if instruction != "jgz":
            self.next_instruction += 1
        return instruction, arguments, retval

    def der(self, value):
        if value in ascii_lowercase:
            return self.registers[value]
        return int(value)

    def add(self, register, value):
        self.registers[register] = self.registers[register] + self.der(value)

    def mul(self, register, value):
        self.registers[register] = self.registers[register] * self.der(value)

    def mod(self, register, value):
        self.registers[register] = self.registers[register] % self.der(value)

    def rcv(self, value):
        value = self.der(value)
        if value != 0:
            return self.last_played

    def jgz(self, value, offset):
        if self.der(value) != 0:
            self.next_instruction += int(offset)
            print(f'setting next instruction to: {self.next_instruction}')
        else:
            self.next_instruction += 1

    def snd(self, value):
        self.last_played = self.der(value)

    def set(self, register, value):
        self.registers[register] = self.der(value)


def phase1(data):
    sp = SoundProcessor()
    for instruction, arguments, retval in sp.run(data):
        print(f'{instruction} {arguments} : {retval} : {sp.registers["a"]} : next: {sp.next_instruction}')
        if instruction == "rcv" and retval is not None:
            return retval


solution = Solution(2017, 18, phase1=phase1)
