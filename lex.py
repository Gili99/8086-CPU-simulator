from enum import Enum
import sys

class Token:
    def __init__(self, kind, text):
        self.kind = kind
        self.text = text

class TokenType(Enum):
    # Commands
    MOV = 0,
    ADD = 1,

    # MP-Registers
    REG8BIT = 100,
    REG16BIT = 101

    # MISC
    NEWLINE = 1000,
    EOF = 1001,
    COMMA = 1002

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
            if text == kind.name:
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
        
        # Done with the current token, advance to the next character
        self._nextChar()     
        return token