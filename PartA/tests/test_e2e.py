
import pytest
from src.interpreter.lexer import Lexer
from src.interpreter.parser import Parser
from src.interpreter.semantic_analyzer import SemanticAnalyzer
from src.interpreter.interpreter import Interpreter
from src.interpreter.ast import AST
from src.interpreter.errors import InterpreterError

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

def test_lambda_expression():
    text = """
    Defun {'name': 'foo', 'arguments': (n)}
    n(2,2)

    foo((Lambd x,y. x+y))
    foo((Lambd x,y. x*y))
    foo((Lambd x,y. x==y))
    foo((Lambd x,y. (Lambd z. z + 1 + (Lambd r. r * r)(x))(y)))
    """

    results = [4,4,True,7]
    counter = 0
    interpreter = Interpreter()
    tree = get_ast(text)

    for result in interpreter.interpret(tree):
        assert results[counter] == result
        counter +=1

def test_function_call_no_lambda():
    text = """
    Defun {'name': 'foo', 'arguments': (n)}
    n(2,2)

    foo(5)
    """
    interpreter = Interpreter()
    with pytest.raises(InterpreterError):
        next(interpreter.interpret(get_ast(text)))