"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # stores the instructions from a program for processing
        self.ram = [0] * 256
        # represents internal registers or working memory
        # we can store values in registers for ease of access
        # or use them as signals
        self.reg = [0] * 8
        # program counter register, stores reference to the mem
        # address of the current instruction
        self.pc = 0

    def ram_read(self, MAR):
        """Accepts a memory address and returns the value stored there"""
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        """Accepts a value to write and the address to write it to"""
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Need proper file name passed")
            sys.exit(1)

        filename = sys.argv[1]

        with open(filename) as f:
            for line in f:
                if line == '':
                    continue
                # ignore comments
                comment_split = line.split('#')

                if comment_split[0] == '' or comment_split[0] == '\n':
                    continue
                else:
                    num = comment_split[0].strip()

                    self.ram[address] = int(num, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

        running = True

        while running is True:
            # receive instructions to be executed
            ir = self.ram[self.pc]

            # HLT
            if ir == 1:
                running = False
                self.pc += 1

            # LDI
            elif ir == 130:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                self.pc += 3

            # PRN
            elif ir == 71:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2

            # MUL
            elif ir == 162:

                self.reg[self.ram[self.pc + 1]
                         ] *= self.reg[self.ram[self.pc + 2]]

                self.pc += 3

            else:
                sys.exit(1)
