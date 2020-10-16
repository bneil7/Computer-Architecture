"""CPU functionality."""

import sys

# set instructions in binary
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
SUB = 0b10100001
# SPRINT
CMP = 0b10100111  # Compare the values in two registers.
JMP = 0b01010100  # Jump to the address stored in the given register.
JEQ = 0b01010101
# If `equal` flag is set (true), jump to the address stored in the given register.
JNE = 0b01010110
# If `E` flag is clear (false, 0), jump to the address stored in the given
# register.


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0  # PROGRAM COUNTER
        # self.ir = 0  # INSTRUCTION REGISTER
        # self.mar = 0  # MEMORY ADDRESS REGISTER
        self.FL = 0b00000000  # FLAG

    def ram_write(self, address, value):
        """
        Writes the value to the address passed in.
        Gets the address through the pc register
        """
        self.ram[address] = value

    def ram_read(self, address):
        """ 
        Accept the address to read and returns the value stored there.
        Get the address through the pc register.
        """
        return self.ram[address]

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()  # strip deletes empty line/space when printing

                    if line == "" or line[0] == "#":
                        continue  # pushes program through if line is empty

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)  # BASE 2, BECAUSE BINARY
                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU (arithmetic logic unit) operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "CMP":
            self.FL = 0b00000000
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001  # E(qual)
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010  # G(reater than)
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100  # L(ess than)
            else:
                print("ALU CMP OP NOT FOUND")
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        SP = 7
        halted = False

        # while running, get instruction from program counter address memory
        while not halted:
            instruction = self.ram_read(self.pc)

            # get next 2 bytes of data as placeholders for instruction to use
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # check for different instruction cases
            if instruction == HLT:  # Halt instruction, exits emulator
                halted = True
                self.pc = 0  # set steps counter back to zero
            elif instruction == LDI:  # set value of the register to an integer
                # operand_a is the register number
                # operand_b is the value to set the register to
                # self.trace()
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == PRN:  # prints numeric value stored in given register
                # operand_a is the register number
                # self.trace()
                print(self.reg[operand_a])
                self.pc += 2
            elif instruction == MUL:  # Multiplies reg_a * reg_b
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif instruction == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif instruction == SUB:
                self.alu("SUB", operand_a, operand_b)
                self.pc += 3
            elif instruction == PUSH:
                '''
                1. Decrement the `SP`.
                2. Copy the value in the given register to the address pointed to by
                `SP`. 
                '''
                # self.trace()
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.pc += 2
            elif instruction == POP:
                '''
                1. Copy the value from the address pointed to by `SP` to the given register.
                2. Increment `SP`.
                '''
                # self.trace()
                self.reg[operand_a] = self.ram[SP]
                SP += 1
                self.pc += 2
            elif instruction == CALL:
                # print("-- CALL --")
                value = self.pc + 2
                SP -= 1
                self.ram_write(SP, value)
                self.pc = self.reg[operand_a]
            elif instruction == RET:
                '''
                Pop the value from the top of the stack and store it in the `PC`.
                '''
                # print("-- RET --")
                self.pc = self.ram[SP]
                SP += 1
                # do not increment pc in RET
            ### SPRINT CHALLENGE ###
            elif instruction == CMP:
                self.alu("CMP", operand_a, operand_b)
            elif instruction == JMP:
                # Set the `PC` to the address stored in the given register.
                self.pc = self.reg[operand_a]
            elif instruction == JEQ:
                if self.FL == 0b00000001:
                    self.pc = self.reg[operand_a]
            elif instruction == JNE:
                if self.FL != 0b00000001:
                    self.pc = self.reg[operand_a]
            else:
                print(
                    f"Instruction '{instruction:08b}' not found at address {self.pc}")
                # ^ prints out in binary to 8 places
                sys.exit(1)
