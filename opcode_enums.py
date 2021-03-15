from enum import Enum

class RegType(Enum):
    REG8BIT = 0
    REG16BIT = 1
    MEMORY = 2

class OperandType(Enum):
    REGISTER = 0
    DEC_NUMBER = 1
    HEX_NUMBER = 2
    BIN_NUMBER = 3
    MEMORY_ADDRESS = 4