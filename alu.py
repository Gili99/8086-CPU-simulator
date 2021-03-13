#####################################################################
# ALU - a class used for basic arithmetic operations on binary arrays
#####################################################################
class ALU:

    @staticmethod
    def addTwoBinaryArrays(arr1, arr2):
        print("arr1: " + str(arr1))
        print("arr2: " + str(arr2))
        assert len(arr1) == len(arr2)

        resArr = [0 for i in range(len(arr1))]
        arr1Rev = arr1[::-1]
        arr2Rev = arr2[::-1]
        carry = 0
        for i in range(len(arr1Rev)):
            result = arr1Rev[i] + arr2Rev[i] + carry
            if result > 1:
                result = result - 2
                carry = 1
            else:
                carry = 0
            resArr[i] = result

        print("res:  " + str(resArr[::-1]))

        # check if there is carry remaining
        if carry == 1:
            pass # handle the carry flag

        return (resArr[::-1], False) 
