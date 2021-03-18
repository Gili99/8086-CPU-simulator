from registers import FlagsRegister, MP16BitRegister
from opcode_enums import OperandType, RegType
from alu import ALU
from memory import Memory
import math
from enum import Enum

class PrintMode(Enum):
    DECIMAL = 0
    BINARY = 1
    HEX = 2

class CPU8086:
    def __init__(self):
        # Operations and their methods
        # Format: 'command name' : (handling function, parameters to function)
        self.ops = { \
            'mov': (self.arithTwoOperandOperation, self.mov), \
            'add': (self.arithTwoOperandOperation, self.add), \
            }

        # set up the flags
        self.flags = FlagsRegister()
        self.mpRegs = {"a": MP16BitRegister(), \
            "b": MP16BitRegister(), \
            "c": MP16BitRegister(), \
            "d": MP16BitRegister()}
        
        # set up the memory
        self.memory = Memory(10)

    def runProgram(self, commands):
        for command in commands:
            commandParts = command.split(' ')
            commandFunc, params = self.resolveCommandFunc(commandParts[0])
            if params is not None:
                commandFunc(commandParts, params)

    def resolveCommandFunc(self, commandName):
        return self.ops[commandName]

    def resolveMPRegister(self, regText):
        mp16bitRegister = self.mpRegs[regText[0]]
        return mp16bitRegister[regText[1]]

    def resolveDestinationRegister(self, commandParts):
        return self.resolveMPRegister(commandParts[2])

    def resolveDestination(self, commandParts):
        destType = commandParts[1]
        if int(destType) == RegType.MEMORY.value:
            return (self.memory, int(commandParts[2], 16)) # destination addresses alaways in hex form 
        else:
            return (self.resolveDestinationRegister(commandParts), None)

    def resolveOperandValue(self, sourceType, source, destType):
        sourceType = int(sourceType)

        # The source is a register
        if sourceType == OperandType.REGISTER.value:
            return self.resolveMPRegister(source).get_value_bits()
        
        # the source is a hex number
        elif sourceType == OperandType.HEX_NUMBER.value:
            value = int(source, 16)

        # the source is a binary number
        elif sourceType == OperandType.BIN_NUMBER.value:
            value = int(source, 2)

        # the source is placed inside a memory address
        elif sourceType == OperandType.MEMORY_ADDRESS.value:
            value = int(ALU.binArrToDec(self.memory[int(source, 16)])) # memory address is always in HEX

        # Determine the size of the destination register
        sizeOfReg = 16
        if int(destType) == RegType.REG8BIT.value or int(destType) == RegType.MEMORY.value:
            sizeOfReg = 8

        # convert the value to binary array
        binVal = bin(value)
        binArr = [0 for i in range(sizeOfReg - len(binVal) + 2)]
        for i in range(2, len(binVal)):
            binArr.append(int(binVal[i]))
        return binArr

    def getRegisterValue(self, register, printMode):
        if printMode == PrintMode.DECIMAL:
            result = ALU.binArrToDec(register.get_value_bits())
        return result

    def printState(self):
        # print the registers
        axVal = self.getRegisterValue(self.mpRegs['a'], PrintMode.DECIMAL)
        bxVal = self.getRegisterValue(self.mpRegs['b'], PrintMode.DECIMAL)
        cxVal = self.getRegisterValue(self.mpRegs['c'], PrintMode.DECIMAL)
        dxVal = self.getRegisterValue(self.mpRegs['d'], PrintMode.DECIMAL)

        print("ax: %d, bx: %d, cx: %d, dx: %d" % (axVal, bxVal, cxVal, dxVal))

        # print the memory
        memString = ''
        for i in range(len(self.memory)):
            memString += str(i) + ": " + str(int(ALU.binArrToDec(self.memory[i]))) + ", "
        
        print(memString)

    ############################################################################
    # Arithmetic two operands operations
    ############################################################################

    # A genaral function for performing two operands operations
    # The operation is a pointer to a function that carries out a specific operation
    def arithTwoOperandOperation(self, commandParts, operation):
        # get relevant parts for the operation
        #print(commandParts)
        destType = commandParts[1]
        dest, location = self.resolveDestination(commandParts)
        typeOfSource = commandParts[3]

        # check if source is a memory address
        if len(commandParts) > 6:
            source = commandParts[5] # 4 is type of number. currently only hex when using memory
        else:
            source = commandParts[4]
        binArr = self.resolveOperandValue(typeOfSource, source, destType)

        # perform the operation
        operation(destType, dest, location, typeOfSource, source, binArr)

        # check for flag changes
        self.printState()

    # mov operation - mov value from register/number into destination register
    def mov(self, destType, dest, location, typeOfSource, source, binArr):
        # destination is a memory
        if int(destType) == RegType.MEMORY.value:
            dest[location] = binArr
        else: # destination is a register
            dest.set_value_bits(binArr)

    # add operation - add the tource value into the destination register
    def add(self, destType, dest, location, typeOfSource, source, binArr):
        destBits = dest.get_value_bits()
        resultArr, isCarry = ALU.addTwoBinaryArrays(destBits, binArr)
        dest.set_value_bits(resultArr)
