
import pytest
from src.interpreter.lexer import Lexer
from src.interpreter.parser import Parser
from src.interpreter.analyzer import SemanticAnalyzer
from src.interpreter.interpreter import Interpreter
from src.interpreter.ast import AST

def get_ast(text:str)-> AST:
    tree =  Parser(Lexer(text)).parse()
    SemanticAnalyzer().visit(tree)
    return tree

def test_simple_addition():
    text = "5 + 3"
    ast = get_ast(text)

    interpreter = Interpreter()
    result = next(interpreter.interpret(ast))
    assert result == 8

def test_combined_operations():
    text = "3 % 5 + 2 * 8 - 3 / 3"

    ast = get_ast(text)

    interpreter = Interpreter()
    result = next(interpreter.interpret(ast))
    assert result == 18

def test_unary_opeartions():
    tests = [
        ('-5', -5),
        ('-5 + 10', 5),
        ('+5 + 10', 15)
    ]
    interpreter = Interpreter()

    for text, expected_output in tests:
        result = next(interpreter.interpret(get_ast(text)))
        assert result == expected_output

def test_logical_operations():
    tests = [
        ('!True',False),
        ('True || False',True),
        ('False || True',True),
        ('True && False',False),
        ('True && True',True),
    ]
    interpreter = Interpreter()

    for text, expected_output in tests:
        result = next(interpreter.interpret(get_ast(text)))
        assert result == expected_output

def test_function_declaration_call():
    text = """
    Defun {'name': 'add', 'arguments': (x, y)}
    x + y
    add(3, 7)
    """

    interpreter = Interpreter()

    result = next(interpreter.interpret(get_ast(text)))
    assert result == 10

# def test_lambda_expression():
#     text = "(Lambd x.(Lambd y. (x + y)))(3)(4)"
#     interpreter = Interpreter()

#     result = next(interpreter.interpret(get_ast(text)))
#     assert result == 7