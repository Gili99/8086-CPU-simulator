import sys
from lex import TokenType
from opcode import RegType, OperandType

class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter
        
        self.curToken = None
        self._nextToken()

    def _nextToken(self):
        self.curToken = self.lexer.getNextToken() 

    def _checkToken(self, token):
        return self.curToken.kind == token
    
    def _match(self, token):
        if not self._checkToken(token):
            self._abort("Unexpected token. got: " + str(self.curToken.kind) + ", instead of: " + str(token))
        self._nextToken()

    def _matchCommand(self):
        return TokenType.isCommand(self.curToken)

    def _abort(self, message):
        sys.exit("Error in parsing. " + message)

    # program ::= {statement nl}
    def program(self):
        print("PROGRAM")
        while not self._checkToken(TokenType.EOF):
            self.statement()
            if not self._checkToken(TokenType.EOF):
                self.nl()

    # nl ::= NEWLINE
    def nl(self):
        self._match(TokenType.NEWLINE)
        while self._checkToken(TokenType.NEWLINE):
            self._nextToken()

        # end the currently generated opcode    
        self.emitter.endOpcode()
    
    # statement ::= COMMAND singleOperand | COMMAND doubleOperands
    def statement(self):
        print("STATEMENT")
        self._matchCommand()

        # Add the command to the opcode
        self.emitter.addOpcodePart(self.curToken.text)
        
        # Check if command requires single or double operands
        if TokenType.isSingleOperand(self.curToken):
            self._nextToken()
            self.singleOperand()
        else:
            self._nextToken()
            self.doubleOperands()
    
    # singleOpernad ::= REG8BIT | REG16BIT
    def singleOperand(self):
        print("SINGLE_OPERAND")

        if self._checkToken(TokenType.REG8BIT):
            # emit opcode
            self.emitter.addOpcodePart(RegType.REG8BIT.value)
            self.emitter.addOpcodePart(OperandType.REGISTER.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
        elif self._checkToken(TokenType.REG16BIT):
            # emit opcode
            self.emitter.addOpcodePart(RegType.REG16BIT.value)
            self.emitter.addOpcodePart(OperandType.REGISTER.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
        else:
            self._abort("Expected register. got: " + str(self.curToken.kind))
    
    # doubleOperands ::= REG8BIT, source8 | REG16BIT, source16
    def doubleOperands(self):
        print("OPERANDS")

        # The destination is an 8 bit register
        if self._checkToken(TokenType.REG8BIT):
            # emit opcode
            self.emitter.addOpcodePart(RegType.REG8BIT.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
            self._nextToken()
            self.source8()
        
        # The destination is a 16 bit register
        elif self._checkToken(TokenType.REG16BIT):
            # emit opcode
            self.emitter.addOpcodePart(RegType.REG16BIT.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
            self._match(TokenType.COMMA)
            self.source16()
        else:
            self._abort("Unexpected token at operands: " + str(self.curToken.kind))

    # source8 ::= 8REG | numberSource
    def source8(self):
        print("SOURCE8")

        if self._checkToken(TokenType.REG8BIT):
            self.emitter.addOpcodePart(OperandType.REGISTER.value)
            self.emitter.addOpcodePart(self.curToken.text)
            self._nextToken()

        # Check if it is a 16-bit instead of an 8-bit register
        elif self._checkToken(TokenType.REG16BIT):
            self._abort("Expected 8-bit register. got: " + str(self.curToken.text))
        else:
            self.numberSource()

    # source16 ::= 16REG | numberSource
    def source16(self):
        print("SOURCE16")

        if self._checkToken(TokenType.REG16BIT):
            self.emitter.addOpcodePart(OperandType.REGISTER.value)
            self.emitter.addOpcodePart(self.curToken.text)
            self._nextToken()

        # Check if it is an 8-bit instead of a 16-bit register
        elif self._checkToken(TokenType.REG8BIT):
            self._abort("Expected 16-bit register. got: " + str(self.curToken.text))
        else:
            self.numberSource()
    
    # numberSource ::= number | [number]
    def numberSource(self):
        print("NUMBER_SOURCE")

        if self._checkToken(TokenType.LEFT_BRACE):
            # emit opcode
            self.emitter.addOpcodePart(OperandType.MEMORY_ADDRESS.value)

            self._nextToken()
            self.number()
            self._match(TokenType.RIGHT_BRACE)
        else:
            self.number()
    
    # number ::= HEX_NUMBER | BIN_NUMBER | DEC_NUMBER
    def number(self):
        print("NUMBER")

        if self._checkToken(TokenType.HEX_NUMBER):
            # emit opcode
            self.emitter.addOpcodePart(OperandType.HEX_NUMBER.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
        elif self._checkToken(TokenType.BIN_NUMBER):
            # emit opcode
            self.emitter.addOpcodePart(OperandType.BIN_NUMBER.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
        elif self._checkToken(TokenType.DEC_NUMBER):
            # emit opcode
            self.emitter.addOpcodePart(OperandType.DEC_NUMBER.value)
            self.emitter.addOpcodePart(self.curToken.text)

            self._nextToken()
        else:
            self._abort("Expected number, got: " + str(self.curToken.kind))
        
