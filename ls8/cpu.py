"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
      """Construct a new CPU."""
      self.running = True
      self.RAM = [0] * 256
      self.Reg = [0] * 8
      self.IR = {
        1: 'HLT',
        130: 'LDI',
        71: 'PRN'
      }
      self.PC = 0
      # self.SP = 
      # self.IE = 
      # self.FL = 

    def ram_read(self, address):
      return self.RAM[address]

    def ram_write(self, address, write):
      self.RAM[address] = write

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.Reg[reg_a] += self.Reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.FL,
            #self.IE,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.Reg[i], end='')

        print()

    def LDI(self, reg_a, reg_b):
      index = self.ram_read(reg_a)
      value = self.ram_read(reg_b)
      self.Reg[index] = value
      self.PC += 3

    def HLT(self):
      self.running = False

    def PRN(self, reg_a):
      index = self.ram_read(reg_a)
      print(f'{self.Reg[index]}')
      self.PC += 2

    def run(self):
      """Run the CPU."""
      while self.running:
        command = self.ram_read(self.PC)
        if command in self.IR:
          instruction = self.IR[command]
        if instruction == 'LDI':
          self.LDI(self.PC + 1, self.PC + 2)
        elif instruction == 'HLT':
          self.HLT()
        elif instruction == 'PRN':
          self.PRN(self.PC + 1)
        else:
          print(f'This {instruction} doe not exist.')
          sys.exit(1)