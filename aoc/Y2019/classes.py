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
            self.memory = memory
        else:
            self.memory = []

        self.initial_memory = self.memory[:]

        self.ip = 0  # Instruction Pointer

        if self.debug:
            self.log = print
        else:
            self.log = lambda x: None

    def run_program(self, memory=None, ip=0):
        if memory is not None:
            self.memory = memory
            self.initial_memory = memory[:]
        self.ip = ip
        mem_size = len(self.memory)
        while self.ip is not None:  # run until EXT instruction
            if self.ip >= mem_size:
                # terminate if there are no more instructions
                break
            self.execute_next_instruction()
        return memory

    def execute_next_instruction(self):
        opcode, parameters = self.parse_instruction(self.ip)
        op = self.OPCODES[opcode]
        try:
            op_name = f"op_{op['name']}"
        except KeyError:
            raise ValueError(f"Invalid opcode: {opcode}")
        self.log(f"[RUN] | {self.OPCODES[opcode]} | {' '.join(p+':'+v for p, v in zip(op['params'], parameters))}")
        getattr(self, op_name)(*parameters)
        self.ip += len(op["params"])

    def parse_instruction(self, address):
        instruction = self.memory[self.ip]
        if len(instruction) <= 2:
            opcode = int(instruction)
            parameters_modes = []
        else:
            opcode = int(instruction[-2:])
            parameters_modes = reversed([int(c) for c in instruction[:-2]])
        self.log(f"[PARSE] {self.OPCODES[opcode]['name']} at {address}")
        parameters = []
        for idx, param in enumerate(self.OPCODES[opcode]):
            try:
                mode = parameters_modes[idx]
            except IndexError:
                mode = self.PAR_POSITION
            parval = self.memory[address + idx + 1]
            value = self.get_parameter_value(parval, mode)

            # debug output
            msg = f'     [parameter] "{param}" = {parval}'
            if mode == self.PAR_POSITION:
                msg += f" -> {value}"
            self.log(msg)

            parameters.append(value)

        return opcode, parameters

    def memset(self, address, value):
        self.memory[address] = value

    def get_parameter_value(self, parval, mode):
        if mode == self.PAR_POSITION:
            return self.memory[parval]
        elif mode == self.PAR_IMMEDIATE:
            return parval
        raise ValueError(f"Parameter mode should be either 0 or 1, got {mode}")

    def op_ADD(self, val1, val2, val3):
        self.memset(val3, val1 + val2)

    def op_MUL(self, val1, val2, val3):
        self.memset(val3, val1 * val2)

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

    @classmethod
    def read_code(cls, data):
        """
        Utility to be used as the "parse_input" function.
        """
        output = []
        for line in data:
            output.extend(val for val in line.strip().split(","))
        return output

