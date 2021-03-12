import sys
from lex import *
from parse import Parser
from emit import Emitter

def main():
    with open(sys.argv[1], 'r') as inputFile:
        program = inputFile.read()

    lexer = Lexer(program)
    emitter = Emitter()
    parser = Parser(lexer, emitter)
    parser.program()

    print("Generated script:")
    print(emitter.getProgramScript())
    """
    token = lexer.getNextToken()
    while token.kind is not TokenType.EOF:
        print(token.kind)
        token = lexer.getNextToken()
    """

if __name__ == "__main__":
    main()