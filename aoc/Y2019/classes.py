class IntCode:
    """
    An IntCode Computer
    """
    OPCODES = {
        1: {"name": "ADD", "params": ("val1", "val2", "dst")},
        2: {"name": "MUL", "params": ("val1", "val2", "dst")},
        3: {"name": "INP", "params": ("dst")},
        4: {"name": "OUT", "params": ("src")},
        99: {"name": "EXT", "params": tuple()},
    }

    PAR_POSITION = 0
    PAR_IMMEDIATE = 1

    def __init__(self, memory=None, debug=False):
        if memory is not None:
            self.memory = memory[:]
        else:
            self.memory = []

        self.initial_memory = self.memory[:]

        self.ip = 0  # Instruction Pointer

        if debug:
            self.log = print
        else:
            self.log = lambda x: None

    def run_program(self, memory=None, ip=0):
        self.log("[PRG] RUNNING PROGRAM")
        self.log("[MEM] MEMORY STATE:")
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
        return self.memory

    def execute_next_instruction(self):
        opcode, parameters = self.parse_instruction(self.ip)
        op = self.OPCODES[opcode]
        try:
            op_name = f"op_{op['name']}"
        except KeyError:
            raise ValueError(f"Invalid opcode: {opcode}")
        self.log(f"[RUN] | {op['name']} | {' '.join(p+':'+str(v) for p, v in zip(op['params'], parameters))}")
        getattr(self, op_name)(*parameters)
        if opcode != 99:
            self.ip += len(op["params"]) + 1

    def parse_instruction(self, address):
        instruction = str(self.memory[address])
        if len(instruction) <= 2:
            opcode = int(instruction)
            parameters_modes = []
        else:
            opcode = int(instruction[-2:])
            parameters_modes = reversed([int(c) for c in instruction[:-2]])
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
        msg = f"     [GET] param[{parval}]"
        if mode == self.PAR_POSITION:
            value = self.memory[parval]
            msg += f"->pos->mem[{parval}]"
        elif mode == self.PAR_IMMEDIATE:
            value = parval
            msg += f"->dir->{parval}<"
        else:
            raise ValueError(f"Parameter mode should be either 0 or 1, got {mode}")
        msg += f"->{value}"
        self.log(msg)
        return value

    def op_ADD(self, val1, val2, dst):
        self.log(f"     [ADD] mem[{dst}]={val1+val2}({val1}+{val2})")
        self.memset(dst, val1 + val2)

    def op_MUL(self, val1, val2, dst):
        self.log(f"     [MUL] mem[{dst}]={val1 * val2}({val1}*{val2})")
        self.memset(dst, val1 * val2)

    def op_INP(self, dst):
        try:
            val = int(input(" > "))
        except ValueError:
            print("Invalid input.")
            self.op_INP(dst)
            return
        self.memset(dst, val)

    def op_EXT(self):
        self.ip = None

    def op_OUT(self, src):
        print(src)

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

