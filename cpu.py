from registers import FlagsRegister

class CPU8086:
    def __init__(self):
        self.flags = FlagsRegister()
        self.mpRegs = [0 for i in range(8)] # Multi-purpose registers

    def runProgram(self, commands):
        pass

    def printState(self):
        pass

    def mov(self, operands):
        dest = 