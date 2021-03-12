from enum import Enum
import sys

class Token:
    def __init__(self, kind, text):
        self.kind = kind
        self.text = text

class TokenType(Enum):
    # Single operand Commands
    INC = 0
    DEC = 1

    # Double operand commands
    MOV = 50
    ADD = 51
    SUB = 52
    MUL = 53
    DIV = 54

    # MP-Registers
    REG8BIT = 100
    REG16BIT = 101

    # operands
    HEX_NUMBER = 200
    BIN_NUMBER = 201
    DEC_NUMBER = 202
    LABEL = 203

    # MISC
    NEWLINE = 1000
    EOF = 1001
    COMMA = 1002
    LEFT_BRACE = 1003
    RIGHT_BRACE = 1004

    @staticmethod
    def isCommand(token):
        if token.kind.value <= 100:
            return True
        return False

    @staticmethod
    def isSingleOperand(commandToken):
        if commandToken.kind.value < 50:
            return True
        return False

###########################################################################
# The lexer class is responsible for breaking the input strings into tokens
###########################################################################
class Lexer:
    def __init__(self, source):
        self.source = source
        self.curPos = -1
        self.curChar = ''
        self._nextChar()

    # Advances the lexer to the nexr char in the sequence
    def _nextChar(self):
        self.curPos += 1
        if (self.curPos >= len(self.source)):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]
    
    # Returns the next char in the sequence without advancing it
    def _peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]
    
    # Aborts the lexing process and exits the program
    def _abort(self, message):
        sys.exit("Error in lexer: " + message)

    # Skips whitespaces
    def _skipSpaces(self):
        while self.curChar == ' ':
            self._nextChar()

    # Checks if the given text matches a known keyword. if so it returns the ENUM keyword, if not returns None
    def _checkIfKeyword(self, text):
        text = text.upper()
        for kind in TokenType:
            if text == kind.name and kind.value <= 100:
                return kind
        return None

    # Checks if the given text is a register
    def _checkIfRegister(self, text):
        text = text.upper()
        if text in ['AL', 'AH', 'BL', 'BH', 'CL', 'CH', 'DL', 'DH']:
            return TokenType.REG8BIT
        
        if text in ['AX', 'BX', 'CX', 'DX']:
            return TokenType.REG16BIT
        
        return None

    # Each call returns the next token in the sequence
    def getNextToken(self):
        self._skipSpaces()
        token = None

        # Handle special chars
        if self.curChar == '\n':
            token = Token(TokenType.NEWLINE, self.curChar)
        elif self.curChar == '\0':
            token = Token(TokenType.EOF, self.curChar)
        elif self.curChar == ',':
            token = Token(TokenType.COMMA, self.curChar)
        elif self.curChar == '[':
            token = Token(TokenType.LEFT_BRACE, self.curChar)
        elif self.curChar == ']':
            token = Token(TokenType.RIGHT_BRACE, self.curChar)
        
        # handle alphanumeric instances
        elif self.curChar.isalpha():
            startPos = self.curPos

            while self._peek().isalpha():
                self._nextChar()
            
            text = self.source[startPos: self.curPos + 1]
            kind = self._checkIfKeyword(text)
            
            # kind is a keyword
            if kind is not None:
                token = Token(kind, text)
            else:
                kind = self._checkIfRegister(text) 

                # kind is a register
                if kind is not None:
                    token = Token(kind, text)
                else:
                    pass # Later add support for label identifiers

        # handle numbers
        elif self.curChar.isdigit():
            startPos = self.curPos
            
            while self._peek().isdigit():
                self._nextChar()
            
            if self._peek() == '\n':
                token = Token(TokenType.DEC_NUMBER, self.source[startPos: self.curPos + 1])
            elif self._peek() == 'h':
                token = Token(TokenType.HEX_NUMBER, self.source[startPos: self.curPos + 1])
                self._nextChar()
            elif self._peek() == 'b':
                token = Token(TokenType.BIN_NUMBER, self.source[startPos: self.curPos + 1])
                self._nextChar()
            else:
                self._abort("Unexpected character at the end of number: (" + self.source[startPos: self.curPos + 1] + ")")
        
        else:
            self._abort("Unknown character: " + self.curChar)

        # Done with the current token, advance to the next character
        self._nextChar()     
        return token