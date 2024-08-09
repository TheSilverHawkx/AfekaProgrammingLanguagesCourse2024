
import pytest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.analyzer import SemanticAnalyzer
from interpreter.interpreter import Interpreter

def run_code(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)
    
    interpreter = Interpreter()
    result = interpreter.visit(tree)
    
    return result

def test_factorial_function():
    text = "Defun {'name': 'factorial', 'arguments': (n,)} (n == 0) or (n * factorial(n - 1)); factorial(5);"
    result = run_code(text)
    assert result == 120  # 5! = 120

def test_lambda_expression():
    text = "(Lambd x.(Lambd y. (x + y)))(3)(4)"
    result = run_code(text)
    assert result == 7

def test_conditional_and_arithmetic():
    text = "let x = (3 + 4) * (2 - 1); if (x > 0) { x = x * 2; } x;"
    result = run_code(text)
    assert result == 14

def test_complex_expression():
    text = "Defun {'name': 'compute', 'arguments': (a, b, c)} (a * b) + c; compute(2, 3, 4);"
    result = run_code(text)
    assert result == 10

def test_runtime_error():
    text = "Defun {'name': 'error', 'arguments': (x,)} x / 0; error(10);"
    with pytest.raises(ZeroDivisionError):
        run_code(text)
