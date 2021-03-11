import sys
from lex import *

def main():
    with open(sys.argv[1], 'r') as inputFile:
        program = inputFile.read()
        
    lexer = Lexer(program)
    token = lexer.getNextToken()
    while token.kind is not TokenType.EOF:
        print(token.kind)
        token = lexer.getNextToken()

if __name__ == "__main__":
    main()