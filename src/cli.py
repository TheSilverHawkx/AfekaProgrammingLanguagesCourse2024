import argparse
from pathlib import Path
from os.path import exists,isfile
import interpreter as intrprt

def configure_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Functional Language Parser'
    )
    subparser = parser.add_subparsers()

    parse_code_parser = subparser.add_parser("parse")
    interactive_parser = subparser.add_parser("prompt")


    parse_code_parser.add_argument(
        '-f',
        '--input-file',
        help='Source file path',
        type=Path
    )
    parse_code_parser.add_argument(
        '--scope',
        help='Print scope information',
        action='store_true',
    )
    parse_code_parser.add_argument(
        '--stack',
        help='Print call stack',
        action='store_true',
    )
    args = parser.parse_args()

    return args

def main(args: argparse.Namespace):
    if not exists(args.input_file) or not isfile(args.input_file):
        print(f"Path '{args.input_file}' doesn't exist or is not a file")
        exit(-1)

    content = open(args.input_file,'r').read()

    lexer = intrprt.Lexer(content)
    try:
        parser = intrprt.Parser(lexer)
        tree = parser.parse()
        
        semantic_analyzer = intrprt.SemanticAnalyzer() #args.scope
        try:
            semantic_analyzer.visit(tree)
        except intrprt.SemanticError as e:
            print(e.message)
            exit(1)

        print(tree)
        interpreter = intrprt.Interpreter(tree) #args.stack
        interpreter.interpret()
    except (intrprt.LexerError, intrprt.ParserError) as e:
        print(e.message)
        exit(1)




if __name__ == "__main__":
    args = configure_parameters()
    main(args)