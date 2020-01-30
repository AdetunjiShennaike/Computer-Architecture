"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
      """Construct a new CPU."""
      self.running = True
      self.RAM = [0] * 256
      self.Reg = [0] * 8
      # self.IM #R5 Interrupt Marker
      self.IS = 248 #R6 Interrupt Status(Interrupts held betwen I0-I7[0xF8-0xFF])
      self.SP = 244 #R7 Stack Pointer(Starts at 0xF4 if stack is empty)

      # Internal Registers
      self.PC = 0 #Unmarked Program Counter
      self.IR = { #Instruction Register
        0: 'NOP', #No Operation
        1: 'HLT', #Halt
        17: 'RET', #Return
        19: 'IRET', #Interupt Return
        69: 'PUSH',
        70: 'POP',
        71: 'PRN', #Print
        72: 'PRA', #Print Alpha
        80: 'CALL', #Call a subroutine(function)
        82: 'INT', #Interupt
        84: 'JMP', #Jump
        85: 'JEQ', #Jump to Equal if set
        86: 'JNE', #Jump to Address stored if Equal not set
        87: 'JGT', #Jump to Greater-Than if set
        88: 'JLT', #Jump to Less-Than if set
        89: 'JLE', #Jump to Less-Than or Equal if set
        90: 'JGE', #Jump to Greater-Than or Equal if set
        101: 'INC', #Increment
        102: 'DEC', #Decrement
        105: 'NOT', #Bitwise NOT
        130: 'LDI', #Set value of Reg_a to input
        131: 'LD', #Load Reg_a with value at Reg_b
        132: 'ST', #Store value in Reg_b in Reg_a
        160: 'ADD',
        161: 'SUB',
        162: 'MUL',
        163: 'DIV',
        164: 'MOD', #Modulous
        167: 'CMP', #Compare
        168: 'AND', #Bitwise AND
        170: 'OR', #Bitwise OR
        171: 'XOR', #Bitwise Exclusive OR
        172: 'SHL', #Shift Left
        173: 'SHR', #Shift Right
      }
      # self.MAR #Memory Address Register
      # self.MDR #Memory Data Register
      # self.IE = 
      self.FL = { #Flags
        'E': 0, #Equals
        'G': 0, #Greater
        'L': 0, #Less
      }

    def ram_read(self, address):
      return self.RAM[address]

    def ram_write(self, address, write):
      self.RAM[address] = int(f'0b{write}', 2)

    def load(self, file):
        """Load a program into memory."""

        address = 0

        f = open(file, 'r')
        for line in f.readlines():
          split = line.split('#')
          instruction = split[0].strip()
          if instruction == '':
            continue
          self.ram_write(address, instruction)
          address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.RAM[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b = 0):
        """ALU operations."""

        if op == "ADD":
            self.Reg[reg_a] += self.Reg[reg_b]
        elif op == "SUB": 
            self.Reg[reg_a] -= self.Reg[reg_b]
        elif op == "AND":
            result = self.Reg[reg_a] & self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "NOT":
            result = ~self.Reg[reg_a]
            self.Reg[reg_a] = result
        elif op == "OR":
            result = self.Reg[reg_a] | self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "XOR":
            result = self.Reg[reg_a] ^ self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "DEC":
            self.Reg[reg_a] -= 1
        elif op == "INC":
            self.Reg[reg_a] += 1
        elif op == "SHL":
            result = self.Reg[reg_a] << self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "SHR":
            result = self.Reg[reg_a] >> self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "CMP":
            if self.Reg[reg_a] > self.Reg[reg_b]:
              self.FL['L'] = 0
              self.FL['G'] = 1
              self.FL['E'] = 0
            if self.Reg[reg_a] < self.Reg[reg_b]:
              self.FL['L'] = 1
              self.FL['G'] = 0
              self.FL['E'] = 0
            else:
              self.FL['L'] = 0
              self.FL['G'] = 0
              self.FL['E'] = 1
        elif op == "MUL":
            result = self.Reg[reg_a] * self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "DIV":
            if self.Reg[reg_b] == 0:
              print(f'Cannot use the value 0')
              self.HLT()
            result = self.Reg[reg_a] // self.Reg[reg_b]
            self.Reg[reg_a] = result
        elif op == "MOD":
            if self.Reg[reg_b] == 0:
              print(f'Cannot use the value 0')
              self.HLT()
            result = self.Reg[reg_a] % self.Reg[reg_b]
            self.Reg[reg_a] = result
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            self.FL,
            #self.IE,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.Reg[i], end='')

        print()

    def LDI(self, reg_a, reg_b):
      # index = self.ram_read(reg_a)
      # value = self.ram_read(reg_b)
      self.Reg[reg_a] = reg_b

    def HLT(self):
      self.running = False

    def PRN(self, reg_a):
      # index = self.ram_read(reg_a)
      print(f'{self.Reg[reg_a]}')

    def CALL(self, func):
      pass

    def INT(self, reg_a):
      pass
    
    def IRET(self, func):
      pass

    def JEQ(self, func):
      pass

    def JGE(self, func):
      pass

    def JGT(self, func):
      pass

    def POP(self):
      pass

    def PRA(self):
      pass

    def PUSH(self):
      pass

    def RET(self):
      pass

    def ST(self):
      pass



    def run(self):
      """
      Run the CPU.
      
      When the LS-8 is booted, the following steps occur:

        R0-R6 are cleared to 0.
        R7 is set to 0xF4.
        PC and FL registers are cleared to 0.
        RAM is cleared to 0.
      
      Subsequently, the program can be loaded into RAM starting at address 0x00.
      """

      self.Reg[7] = self.SP

      while self.running:
        command = self.ram_read(self.PC)
        if command in self.IR:
          instruction = self.IR[command]
        if instruction == 'LDI':
          self.LDI(self.ram_read(self.PC + 1), self.ram_read(self.PC + 2))
          self.PC += 3
        elif instruction == 'HLT':
          self.HLT()
        elif instruction == 'PRN':
          self.PRN(self.ram_read(self.PC + 1))
          self.PC += 2
        elif instruction == 'MUL':
          self.alu('MUL',self.ram_read(self.PC + 1), self.ram_read(self.PC + 2))
          self.PC += 3
        else:
          print(f'This {instruction} does not exist.')
          sys.exit(1)