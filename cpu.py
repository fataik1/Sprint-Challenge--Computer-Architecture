"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.branchtable = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100000: self.ADD,
            0b10100001: self.SUB,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10101000: self.AND,
            0b01100101: self.INC,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b00000001: self.HLT 
        }
        self.sp = 7
        self.reg[self.sp] = 0xF4

        self.EQ = 7
        self.GT = 6
        self.LT = 5
        self.flags = [0] * 8

    # print(sys.argv[0])
    # sys.exit(0)

    def LDI(self): # handles the LDI instruction
        reg_index = self.ram_read(self.pc + 1)
        reg_value = self.ram_read(self.pc + 2)
        self.reg[reg_index] = reg_value
    
    def PRN(self): # handles the PRN instruction
        reg_index = self.ram_read(self.pc + 1)
        print(self.reg[reg_index])

    def ADD(self): #handles the ADD instructions
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('ADD', reg_a, reg_b) 

    def SUB(self):   #handles the SUB instructions
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('SUB', reg_a, reg_b)

    def MUL(self): # handles the MUL instruction
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('MUL', reg_a, reg_b)

    def DIV(self):  # handles the DIV instruction
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('DIV', reg_a, reg_b)
        
    def AND(self):  # handles the AND instruction
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('AND', reg_a, reg_b)
        
    def INC(self):  # handles the INC instruction
        reg_a = self.ram_read(self.pc + 1)
        self.alu("INC", reg_a=reg_a, reg_b=None)
    
    def PUSH(self):  # handles the PUSH instuction
        # decrement stack pointer
        self.reg[self.sp] -= 1
        # get register value
        reg_index = self.ram_read(self.pc + 1)
        value = self.reg[reg_index]
        # Store in memory
        address_to_push_to = self.reg[self.sp]
        self.ram[address_to_push_to] = value

    def POP(self):
        address_to_pop_from = self.reg[self.sp]
        value = self.ram[address_to_pop_from]

        # store in the given register
        reg_index = self.ram_read(self.pc + 1)
        self.reg[reg_index] = value

        # increment SP
        self.reg[self.sp] += 1

        # self.pc += 2
    
    def CALL(self):
        #gets the address of the next instruction
        return_address = self.pc + 2
        # push on the stack
        self.reg[self.sp] -= 1
        address_to_push_to = self.reg[self.sp]
        self.ram[address_to_push_to] = return_address
        # set the pc to te subroutine address
        reg_index = self.ram_read(self.pc + 1)
        subroutine_address = self.reg[reg_index]
        self.pc = subroutine_address

    def RET(self):
        # get return address from top of the stack
        address_to_pop_from = self.reg[self.sp]
        return_address = self.ram[address_to_pop_from]
        self.reg[self.sp] += 1
        #set pc to return address
        self.pc = return_address

    def CMP(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('CMP', reg_a, reg_b)

    def JMP(self):
        reg_index = self.ram_read(self.pc + 1)
        address_to_jump_to = self.reg[reg_index]
        self.pc = address_to_jump_to

    def JEQ(self):
        reg_index = self.ram_read(self.pc + 1)
        address_to_jump_to = self.reg[reg_index]
        if self.flags[self.EQ] == 1:
            self.pc = address_to_jump_to
        else:
            self.pc += 2
    
    def JNE(self):
        reg_index = self.ram_read(self.pc + 1)
        address_to_jump_to = self.reg[reg_index]
        if self.flags[self.EQ] == 0:
            self.pc = address_to_jump_to
        else:
            self.pc += 2
        
    def HLT(self):  # hanldes the HLT instruction
        self.running = False
        #self.pc += 1

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value
        

    def load(self):
        """Load a program into memory."""

        address = 0

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
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("Usage: python ls8\ls8.py filename")
            sys.exit(1)

        try:
            arg1 = sys.argv[1]
            with open(arg1) as f:
                for line in f:
                    try:
                        line = line.split("#", 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find the file {arg1}")
            sys.exit(1)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b] 
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "AND":
            bitwise_AND = (self.reg[reg_a] & self.reg[reg_b])
            self.reg[reg_a] = bitwise_AND
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flags[self.EQ] = 1
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flags[self.GT] = 1
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags[self.LT] = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.ram[self.pc]

            if ir not in self.branchtable:
                print(f"Not known {ir} at location{self.pc}")
                sys.exit(1)
            
            ir_code = self.branchtable[ir]
            ir_code()

            mask = 0b00010000
            does_ir_set_pc = (ir & mask) >> 4

            if does_ir_set_pc == 1:
                continue
            else:
                # ir_code = self.branchtable[ir]
                # ir_code()

                mask = 0b11000000
                num_params = (ir & mask) >> 6
                self.pc+= (num_params + 1)

cpu = CPU()

cpu.load()
cpu.run()