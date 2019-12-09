class IntCode:
    """
    An IntCode Computer
    """
    # Note: any parameter called "dst" will not be dereferenced when parsing
    # parameters ("Parameters that an instruction writes to will never be in
    # immediate mode.")
    OPCODES = {
        1: {"name": "ADD", "params": ("val1", "val2", "dst")},
        2: {"name": "MUL", "params": ("val1", "val2", "dst")},
        3: {"name": "INP", "params": ("dst",)},
        4: {"name": "OUT", "params": ("src",)},
        5: {"name": "JIT", "params": ("cond", "to")},
        6: {"name": "JIF", "params": ("cond", "to")},
        7: {"name": "ILT", "params": ("val1", "val2", "dst")},
        8: {"name": "IEQ", "params": ("val1", "val2", "dst")},
        9: {"name": "IRB", "params": ("val",)},
        99: {"name": "EXT", "params": tuple()},
    }

    PAR_POSITION = 0
    PAR_IMMEDIATE = 1
    PAR_RELATIVE = 2

    def __init__(self, memory=None, debug=False, silent=False, input_wait=False):
        """
        if silent is set, OUT instructions won't actually print anything
        """
        # memory state
        if memory is not None:
            self.memory = memory[:]
        else:
            self.memory = []

        self.initial_memory = self.memory[:]
        self.relative_base = 0

        self.ip = 0  # Instruction Pointer

        # execution pausing
        self.input_wait = input_wait
        self.waiting = False

        # automation stuff
        self.inputs = []
        self.screen_output = []  # stores output messages
        self.silent = silent

        # debug
        if debug:
            self.log = print
        else:
            self.log = lambda *x, **y: None

    def run_program(self, memory=None, ip=0, inputs=None):
        self.log("[PRG] RUNNING PROGRAM")
        # set i/o buffers
        self.screen_output = []
        if inputs is not None:
            self.inputs = inputs[:]
            self.log(f"[PRG] using input buffer: {self.inputs}")
        else:
            self.inputs = []

        # set memory
        if memory is not None:
            self.memory = memory
            self.initial_memory = memory[:]
        self.log(f"[MEM] {self.memory}")

        # handle suspension
        if not self.waiting:
            # only set the instruction pointer if we're not in suspended mode
            self.ip = ip
        else:
            self.log("[SLEEP] Resuming execution.")
        self.waiting = False

        mem_size = len(self.memory)
        while self.ip is not None:  # run until EXT instruction
            self.log(f"[IP ] {self.ip}")
            if self.ip >= mem_size:
                # terminate if there are no more instructions
                break
            if self.waiting:
                # return if we are waiting for input
                self.log(f"[SLEEP] suspending execution")
                break
            self.execute_next_instruction()
        return self.memory, self.screen_output

    def execute_next_instruction(self):
        opcode, parameters = self.parse_instruction(self.ip)
        op = self.OPCODES[opcode]
        try:
            op_name = f"op_{op['name']}"
        except KeyError:
            raise ValueError(f"Invalid opcode: {opcode}")
        self.log(f"[RUN] | {op['name']} | {' '.join(p+':'+str(v) for p, v in zip(op['params'], parameters))}")
        # suspend execution if we're waiting on input
        if op["name"] == "INP" and self.input_wait and len(self.inputs) == 0:
            self.waiting = True
            return
        getattr(self, op_name)(*parameters)
        if opcode not in (5, 6, 99):  # instructions that set the next instruction
            self.ip += len(op["params"]) + 1

    def parse_instruction(self, address):
        instruction = str(self.memory[address])
        if len(instruction) <= 2:
            opcode = int(instruction)
            parameters_modes = []
        else:
            opcode = int(instruction[-2:])
            parameters_modes = [int(c) for c in instruction[-3::-1]]
        self.log(f"[PARSE] {self.OPCODES[opcode]['name']} : {instruction} at {address}")
        parameters = []
        for idx, param in enumerate(self.OPCODES[opcode]["params"]):
            try:
                mode = parameters_modes[idx]
            except IndexError:
                mode = self.PAR_POSITION
            parameter_address = address + idx + 1
            parval = self.memory[parameter_address]
            if param == "dst":  # destination parameters shouldn't be dereferenced
                value = parval
                if mode == self.PAR_RELATIVE:
                    value += self.relative_base
            else:
                value = self.get_parameter_value(parval, mode)

            # debug output
            msg = f'       [parameter] mem[{parameter_address}] "{param}" = {parval}'
            if mode == self.PAR_POSITION:
                msg += f" -> {value}"
            self.log(msg)

            parameters.append(value)

        return opcode, parameters

    @property
    def memlen(self):
        if not hasattr(self, "_memlen"):
            self._memlen = len(self.memory)
        return self._memlen

    def mem_allocate(self, address: int):
        """
        Extends memory if the current list is too small to reach the given
        address.
        """
        if address >= self.memlen:
            self.log(f"     [MEM] Extend --> {address}", end="")
            self.memory += [0 for _ in range(address + 1 - self.memlen)]
            self._memlen = len(self.memory)
            self.log(f" | newlen: {self._memlen}")

    def memset(self, address: int, value: int):
        self.mem_allocate(address)
        self.memory[address] = value

    def memget(self, address: int):
        self.mem_allocate(address)
        return self.memory[address]

    def get_parameter_value(self, parval: int, mode: int):
        self.log(f"     [GET] param[{parval}]@{mode}", end="")
        if mode == self.PAR_POSITION:
            value = self.memget(parval)
            self.log(f"->pos->mem[{parval}]", end="")
        elif mode == self.PAR_IMMEDIATE:
            value = parval
            self.log(f"->dir->{parval}", end="")
        elif mode == self.PAR_RELATIVE:
            return self.memget(parval+self.relative_base)
        else:
            raise ValueError(f"Parameter mode should be either 0, 2 or 3;  got {mode}")
        self.log(f"->{value}")
        return value

    def op_ADD(self, val1, val2, dst):
        """
        ADDition
        """
        self.log(f"     [ADD] mem[{dst}]={val1+val2}({val1}+{val2})")
        self.memset(dst, val1 + val2)

    def op_MUL(self, val1, val2, dst):
        """
        MULtiplication
        """
        self.log(f"     [MUL] mem[{dst}]={val1 * val2}({val1}*{val2})")
        self.memset(dst, val1 * val2)

    def op_INP(self, dst):
        """
        INPut
        """
        self.log("     [INP] (from:", end="")
        valid = False
        if len(self.inputs):
            self.log("buffer)", end="")
            val = self.inputs.pop(0)
        else:
            while not valid:
                try:
                    val = int(input(" > "))
                    self.log("keyboard)", end="")
                    valid = True
                except ValueError:
                    print("Invalid input.")
        self.log(f" mem[{dst}]={val}")
        self.memset(dst, val)

    def op_OUT(self, src):
        """
        OUTput
        """
        self.screen_output.append(src)
        if not self.silent:
            print(src)

    def op_JIT(self, cond, to):
        """
        Jump If True
        """
        if cond != 0:
            self.ip = to
        else:
            self.ip += 3

    def op_JIF(self, cond, to):
        """
        Jump If False
        """
        if cond == 0:
            self.ip = to
        else:
            self.ip += 3

    def op_ILT(self, val1, val2, dst):
        """
        Is Less Than
        """
        if val1 < val2:
            self.memset(dst, 1)
        else:
            self.memset(dst, 0)

    def op_IEQ(self, val1, val2, dst):
        """
        Is EQual
        """
        if val1 == val2:
            self.memset(dst, 1)
        else:
            self.memset(dst, 0)

    def op_EXT(self):
        """
        EXiT
        """
        self.ip = None

    def op_IRB(self, val):
        """
        Increment Relative Base
        """
        self.relative_base += val

    def reset(self):
        self.memory = self.initial_memory[:]
        self._memlen = len(self.memory)
        self.ip = 0
        self.inputs = []
        self.screen_output = []
        self.waiting = False
        self.relative_base = 0

    @classmethod
    def read_code(cls, data):
        """
        Utility to be used as the "parse_input" function.
        """
        output = []
        for line in data:
            output.extend(int(val) for val in line.strip().split(","))
        return output

