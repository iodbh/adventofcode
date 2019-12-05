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
        99: {"name": "EXT", "params": tuple()},
    }

    PAR_POSITION = 0
    PAR_IMMEDIATE = 1

    def __init__(self, memory=None, debug=False, silent=False):
        """
        if silent is set, OUT instructions won't actually print anything
        """
        if memory is not None:
            self.memory = memory[:]
        else:
            self.memory = []

        self.initial_memory = self.memory[:]

        self.ip = 0  # Instruction Pointer


        # automation stuff
        self.inputs = []
        self.screen_output = []  # stores output messages
        self.silent = silent

        if debug:
            self.log = print
        else:
            self.log = lambda *x, **y: None

    def run_program(self, memory=None, ip=0, inputs=None):
        self.log("[PRG] RUNNING PROGRAM")
        self.log("[MEM] MEMORY STATE:")

        if inputs is not None:
            self.inputs = inputs[:]

        self.log(self.memory)
        if memory is not None:
            self.memory = memory
            self.initial_memory = memory[:]
        self.ip = ip
        mem_size = len(self.memory)
        while self.ip is not None:  # run until EXT instruction
            self.log(f"[IP ] {self.ip}")
            if self.ip >= mem_size:
                # terminate if there are no more instructions
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
            else:
                value = self.get_parameter_value(parval, mode)

            # debug output
            msg = f'       [parameter] mem[{parameter_address}] "{param}" = {parval}'
            if mode == self.PAR_POSITION:
                msg += f" -> {value}"
            self.log(msg)

            parameters.append(value)

        return opcode, parameters

    def memset(self, address, value):
        self.memory[address] = value

    def get_parameter_value(self, parval, mode):
        self.log(f"     [GET] param[{parval}]@{mode}", end="")
        if mode == self.PAR_POSITION:
            value = self.memory[parval]
            self.log(f"->pos->mem[{parval}]", end="")
        elif mode == self.PAR_IMMEDIATE:
            value = parval
            self.log(f"->dir->{parval}<", end="")
        else:
            raise ValueError(f"Parameter mode should be either 0 or 1, got {mode}")
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
        valid = False
        if len(self.inputs):
            val = self.inputs.pop()
        else:
            while not valid:
                try:
                    val = int(input(" > "))
                    valid = True
                except ValueError:
                    print("Invalid input.")
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

    def reset(self):
        self.memory = self.initial_memory[:]
        self.ip = 0

    @classmethod
    def read_code(cls, data):
        """
        Utility to be used as the "parse_input" function.
        """
        output = []
        for line in data:
            output.extend(int(val) for val in line.strip().split(","))
        return output

