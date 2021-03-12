
class Emitter:
    def __init__(self):
        self._parts = []
    
    def addOpcodePart(self, part):
        self._parts.append(str(part))
        self._parts.append(' ')

    def endOpcode(self):
        self._parts.append('\n')
    
    def getProgramScript(self):
        res = ""
        for part in self._parts:
            res += part
        return res