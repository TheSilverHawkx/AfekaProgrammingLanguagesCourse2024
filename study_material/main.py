from interpreter.lexer import Lexer
from interpreter.interpreter import Interpreter
from interpreter.parser import Parser
from os.path import exists,isfile
from interpreter.analyzer import SemanticAnalyzer
from interpreter.errors import LexerError,ParserError,SemanticError
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='SPI - Simple Pascal Interpreter'
    )
    parser.add_argument('inputfile', help='Pascal source file')
    parser.add_argument(
        '--scope',
        help='Print scope information',
        action='store_true',
    )
    parser.add_argument(
        '--stack',
        help='Print call stack',
        action='store_true',
    )
    args = parser.parse_args()

    if not exists(args.inputfile) or not isfile(args.inputfile):
        print(f"Path '{args.inputfile}' doesn't exist or is not a file")
        exit(-1)

    content = open(args.inputfile,'r').read()

    lexer = Lexer(content)
    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except (LexerError, ParserError) as e:
        print(e.message)
        exit(1)

    semantic_analyzer = SemanticAnalyzer(args.scope)
    try:
        semantic_analyzer.visit(tree)
    except SemanticError as e:
        print(e.message)
        exit(1)

    interpreter = Interpreter(tree,args.stack)
    interpreter.interpret()

if __name__ == '__main__':
    main()
