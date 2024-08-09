
import pytest
from interpreter.analyzer import SemanticAnalyzer
from interpreter.parser import Parser
from interpreter.lexer import Lexer
from interpreter.errors import SemanticError

def test_variable_scope():
    text = "Defun {'name': 'test', 'arguments': (x,)} (x + 10); { let x = 20; }"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)

    # No errors should be raised for correct scoping
    assert True

def test_undeclared_variable():
    text = "Defun {'name': 'test', 'arguments': (x,)} (y + 10);"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    
    analyzer = SemanticAnalyzer()
    
    with pytest.raises(SemanticError):
        analyzer.visit(tree)

def test_function_declaration_and_call():
    text = "Defun {'name': 'add', 'arguments': (a, b)} (a + b); let result = add(10, 20); result;"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)
    
    # Ensure the function declaration and call are correctly analyzed
    assert True

def test_function_call_with_incorrect_arguments():
    text = "Defun {'name': 'add', 'arguments': (a, b)} (a + b); let result = add(10); result;"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    
    analyzer = SemanticAnalyzer()
    
    with pytest.raises(SemanticError):
        analyzer.visit(tree)
