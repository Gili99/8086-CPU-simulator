from registers import FlagsRegister, MP16BitRegister
from opcode_enums import OperandType, RegType
from alu import ALU
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

    def resolveSourceValue(self, sourceType, source, regType):
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
            pass

        # Determine the size of the destination register
        sizeOfReg = 16
        if int(regType) == RegType.REG8BIT.value:
            sizeOfReg = 8

        # convert the value to binary array
        binVal = bin(value)

        binArr = [0 for i in range(sizeOfReg - len(binVal) + 2)]
        for i in range(2, len(binVal)):
            binArr.append(int(binVal[i]))
        return binArr

    def getRegisterValue(self, register, printMode):
        if printMode == PrintMode.DECIMAL:
            bitsRev = register.get_value_bits()[::-1]
            result = 0
            for i, bit in enumerate(bitsRev):
                result += math.pow(2, i) * int(bit)
        return result

    def printState(self):
        pass

    ############################################################################
    # Arithmetic two operands operations
    ############################################################################

    # A genaral function for performing two operands operations
    # The operation is a pointer to a function that carries out a specific operation
    def arithTwoOperandOperation(self, commandParts, operation):
        # get relevant parts for the operation
        #print(commandParts)
        regType = commandParts[1]
        destReg = self.resolveDestinationRegister(commandParts)
        typeOfSource = commandParts[3]
        source = commandParts[4]
        binArr = self.resolveSourceValue(typeOfSource, source, regType)

        # perform the operation
        operation(regType, destReg, typeOfSource, source, binArr)

        # check for flag changes
        print(commandParts[2] + " : " + str(self.getRegisterValue((destReg), PrintMode.DECIMAL)))

    # mov operation - mov value from register/number into destination register
    def mov(self, regType, destReg, typeOfSource, source, binArr):
        destReg.set_value_bits(binArr)

    # add operation - add the tource value into the destination register
    def add(self, regType, destReg, typeOfSource, source, binArr):
        destBits = destReg.get_value_bits()
        resultArr, isCarry = ALU.addTwoBinaryArrays(destBits, binArr)
        destReg.set_value_bits(resultArr)