import sys
from lex import *
from parse import Parser
from emit import Emitter
from cpu import CPU8086

def main():
    with open(sys.argv[1], 'r') as inputFile:
        program = inputFile.read()

    lexer = Lexer(program)
    emitter = Emitter()
    parser = Parser(lexer, emitter)
    parser.program()
    program = emitter.getProgramScript()
    print(program)

    cpu = CPU8086()
    cpu.runProgram(program.split('\n'))


    """
    token = lexer.getNextToken()
    while token.kind is not TokenType.EOF:
        print(token.kind)
        token = lexer.getNextToken()
    """

if __name__ == "__main__":
    main()