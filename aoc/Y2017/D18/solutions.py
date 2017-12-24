from ...classes import Solution
from string import ascii_lowercase

MAX_WAIT = 1000


class DeadLockException(Exception):
    ...


class SoundProcessor:

    def __init__(self, pid, mode):
        assert mode in ("sound", "ipc")
        self.mode = mode
        self.registers = {c: 0 for c in ascii_lowercase}
        self.registers["p"] = pid
        self.next_instruction = 0
        self.last_played = None
        self.queue = []
        self.wait_count = 0

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
            if self.wait_count > MAX_WAIT:
                raise DeadLockException
            yield self.run_instruction(instructions[self.next_instruction])

    def run_instruction(self, instruction):
        instruction, *arguments = instruction.split()
        retval = self.instructions_map[instruction](*arguments)
        if instruction not in ("jgz", "rcv"):
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
        # phase2
        if self.mode == "ipc":
            if len(self.queue) != 0:
                self.next_instruction += 1
            else:
                self.wait_count += 1
        # phase 1
        elif self.mode == "sound":
            self.next_instruction += 1
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
    sp = SoundProcessor(0, "ipc")
    for instruction, arguments, retval in sp.run(data):
        print(f'{instruction} {arguments} : {retval} : {sp.registers["a"]} : next: {sp.next_instruction}')
        if instruction == "rcv" and retval is not None:
            return retval


def phase2(data):
    tmgr = {pid: {"program": SoundProcessor(pid), "stopped": False, "snd_count": 0}for pid in (0, 1)}
    # run the initial send/receive here
    processes = {pid: tmgr[pid]["program"].run(data) for pid in tmgr}
    while True:
        for pid in tmgr:
            try:
                instruction, arguments, retval = processes[pid]
                if instruction == "snd":
                    tmgr[pid]["snd_count"] += 1
                    tmgr[(pid+1) % 2]["program"].queue.insert("value", 0) #TODO: push the value
            except DeadLockException:
                tmgr[pid]["stopped"] = True
        if all([i]["stopped"] for i in tmgr.values()):
            return tmgr[0]["snd_count"]


solution = Solution(2017, 18, phase1=phase1, phase2=phase2)
