import math
from abc import abstractclassmethod, ABC

class FlagsRegister:
    def __init__(self):
        self.carry = False
        self.auxiliary = False
        self.parity = False
        self.zero = False
        self.sign = False
        self.overflow = False

class MPRegister(ABC):
    def __init__(self, limitInBits):
        self._limitInBits = limitInBits
    
    def limit(self):
        return self._limitInBits
  
    @abstractclassmethod
    def get_value_bits(self):
        pass

    @abstractclassmethod
    def set_value_bits(self, bits):
        pass

class MP8BitRegister(MPRegister):
    def __init__(self):
        super().__init__(8)
        self._bits = [0 for i in range(8)]

    def get_value_bits(self):
        return self._bits
    
    def set_value_bits(self, bits):
        self._bits = bits

class MP16BitRegister(MPRegister):
    def __init__(self):
        super().__init__(16)
        self._lower = MP8BitRegister()
        self._upper = MP8BitRegister()

    def __getitem__(self, identifier):
        if identifier == 'l':
            return self._lower
        elif identifier == 'h':
            return self._upper
        elif identifier == 'x':
            return self
        else:
            raise Exception("Unknown identifier in register")
    
    def get_value_bits(self):
        bits = self._upper.get_value_bits().copy()
        bits.extend(self._lower.get_value_bits())
        return bits
    
    def set_value_bits(self, bits):
        self._upper.set_value_bits(bits[0:8])
        self._lower.set_value_bits(bits[8:16])