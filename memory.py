
#################################################################
# MemoryException - An exception that occured in memory
#################################################################
class MemoryException(Exception):
    pass

#################################################################
# Memory - A class used to represent a RAM memory device that
# supports IO operations
#################################################################
class Memory:
    def __init__(self, sizeInBytes):
        self._ram = [1 for i in range(sizeInBytes)]

    def _getValueOfMultipleCells(self, cells):
        binStr = ''
        for cell in cells:
            binStr += str(format(cell, '08b'))
        return int(binStr, 2)

    # Checks if the given index is a legal index in memory
    def _isWithinRange(self, index):
        return index >= 0 and index < len(self._ram)

    def __getitem__(self, index):
        isSlice = isinstance(index, slice)

        # Check that index is legal
        if isSlice:
            isLegalIndex = self._isWithinRange(index.start) and self._isWithinRange(index.stop)
        else:
            isLegalIndex = self._isWithinRange(index)

        if not isLegalIndex:
            raise MemoryException("Trying to access illegal memory location")
        
        # Retrieve the appropriate value
        value = self._ram[index]
        if isSlice:
            value = self._getValueOfMultipleCells(value)
        return value

if __name__ == "__main__":
    m = Memory(4096)
    print(m[0:2])