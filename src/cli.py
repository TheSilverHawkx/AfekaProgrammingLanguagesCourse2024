import argparse
from pathlib import Path
from os.path import exists,isfile
import interpreter as intrprt

def prompt():
    interpreter = intrprt.Interpreter()
    semantic_analyzer = intrprt.SemanticAnalyzer()
    root = intrprt.Program([])

    while True:
        try:
            user_input = ''
            while True:
                line = input('>>> ' if not user_input else '... ')

                if line.strip().lower()  == 'exit':
                    raise KeyboardInterrupt
                
                if 'defun ' in line.lower() or line.strip().endswith(('{','(')):
                    user_input += line + '\n'
                    continue

                if line.strip() == '':
                    user_input = ''
                    continue

                elif  not line.strip().endswith(('{','(')):
                    user_input += line
                    break


            lexer = intrprt.Lexer(user_input)
            parser = intrprt.Parser(lexer)
            ast = parser.parse()

            # root.statements.extend(ast.statements)
            root.statements = ast.statements
            semantic_analyzer.visit(root)
            interpreter.interpret(root)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")

def parse():
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

        interpreter = intrprt.Interpreter(tree) #args.stack
        interpreter.interpret()
    except (intrprt.LexerError, intrprt.ParserError) as e:
        print(e.message)
        exit(1)

def configure_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Functional Language Parser'
    )

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

    subparsers = parser.add_subparsers(required=True, dest="mode")

    parser_parse = subparsers.add_parser('parse', description="parse a source file and print the output to screen")
    parser_parse.add_argument(
        '-f',
        '--input-file',
        help='Source file path',
        type=Path,
        required=True
    )
    parser_parse.set_defaults(func=parse)

    parser_prompt = subparsers.add_parser('prompt')    
    parser_prompt.set_defaults(func=prompt)
    
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = configure_parameters()
    args.func()