
import pytest
from interpreter.parser import Parser
from interpreter.lexer import Lexer
from interpreter.ast import Program, FunctionDecl, Lambda, BinOp, Integer, Boolean, FunctionCall
from interpreter.errors import ParserError

def test_parse_function_declaration():
    text = "Defun {'name': 'factorial', 'arguments': (n,)} (n == 0) or (n * factorial(n - 1))"
    lexer = Lexer(text)
    parser = Parser(lexer)
    
    ast = parser.parse()
    
    assert isinstance(ast, Program)
    assert isinstance(ast.block, FunctionDecl)
    assert ast.block.name == 'factorial'
    assert len(ast.block.params) == 1
    assert isinstance(ast.block.body, BinOp)

def test_parse_lambda_expression():
    text = "(Lambd x.(Lambd y. (x + y)))"
    lexer = Lexer(text)
    parser = Parser(lexer)
    
    ast = parser.parse()
    
    assert isinstance(ast, Program)
    assert isinstance(ast.block, Lambda)
    assert ast.block.param == 'x'
    assert isinstance(ast.block.body, Lambda)
    assert ast.block.body.param == 'y'
    assert isinstance(ast.block.body.body, BinOp)

def test_parse_function_call():
    text = "factorial(5)"
    lexer = Lexer(text)
    parser = Parser(lexer)
    
    ast = parser.parse()
    
    assert isinstance(ast, Program)
    assert isinstance(ast.block, FunctionCall)
    assert ast.block.name == 'factorial'
    assert len(ast.block.args) == 1
    assert isinstance(ast.block.args[0], Integer)

def test_parse_syntax_error():
    text = "Defun {'name': 'factorial', 'arguments': (n,) (n == 0)"
    lexer = Lexer(text)
    parser = Parser(lexer)
    
    with pytest.raises(ParserError):
        parser.parse()
