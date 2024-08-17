import argparse
from pathlib import Path
from os.path import exists,isfile
import interpreter as intrprt

def prompt(semantic_analyzer: intrprt.SemanticAnalyzer, interpreter: intrprt.Interpreter):
    root = intrprt.Program([])

    while True:
        try:
            user_input = ''
            while True:
                line = input('>>> ' if not user_input else '... ')

                if line.strip().lower()  == 'exit':
                    raise KeyboardInterrupt
                
                if line.lower().startswith('defun') or line.strip().endswith(('{','(')):
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

            root.statements = ast.statements
            semantic_analyzer.visit(root)

            for output in interpreter.interpret(root):
                print(output)

        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f"Error: {e}")

def parse(semantic_analyzer: intrprt.SemanticAnalyzer, interpreter: intrprt.Interpreter):
    if not exists(args.input_file) or not isfile(args.input_file):
        print(f"Path '{args.input_file}' doesn't exist or is not a file")
        exit(-1)

    if args.input_file.suffix != '.lambda':
        print(f"Error: File '{args.input_file}' is not a lambda file. Aborting...")
        exit(-1)

    content = open(args.input_file,'r').read()

    try:
        lexer = intrprt.Lexer(content)
        parser = intrprt.Parser(lexer)
        tree = parser.parse()
        semantic_analyzer.visit(tree)

        for output in interpreter.interpret(tree):
            print(output)
    except (intrprt.LexerError,intrprt.SemanticError, intrprt.ParserError,intrprt.InterpreterError) as e:
        print(e.message)
        exit(1)
    except Exception as e:
        print(e)
        exit(1)

def configure_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Functional Language Parser'
    )

    parser.add_argument(
        '--show-scope',
        help='Print scope information every time the scope changes',
        action='store_true',
        dest='log_scope'
    )
    parser.add_argument(
        '--show-stack',
        help='Print call stack every time the stack changes',
        action='store_true',
        dest='log_stack'
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

    semantic_analyzer = intrprt.SemanticAnalyzer(args.log_scope)
    interpreter = intrprt.Interpreter(args.log_stack)
    args.func(semantic_analyzer,interpreter)