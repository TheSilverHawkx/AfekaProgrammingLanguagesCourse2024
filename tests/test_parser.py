
import pytest
from src.interpreter.parser import Parser
from src.interpreter.lexer import Lexer
from src.interpreter.ast import Program, FunctionDecl, Lambda, BinOp, Integer, Boolean, FunctionCall
from src.interpreter.errors import ParserError
from src.interpreter.token import TokenType

def get_ast(text):
    return Parser(Lexer(text)).parse()


def test_empty_program():
    text = ''
    ast = get_ast(text)

    assert isinstance(ast,Program)
    assert len(ast.statements) == 0

def test_single_statement():
    text = '5'
    ast = get_ast(text)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], Integer)
    assert ast.statements[0].value == 5

def test_multi_statement():
    tests = [
        ('5'    , Integer, 5),
        ('10'   , Integer, 10),
        ('True' , Boolean, True),
    ]

    text = "\n".join([x[0] for x in tests])
    ast = get_ast(text)

    assert len(ast.statements) == 3

    for index,test in enumerate(tests):
        assert isinstance(ast.statements[index], test[1])
        
        if (hasattr(ast.statements[index],'value')):
            assert ast.statements[index].value == test[2]

def test_function_declartion_args_no_comma():
    text = "Defun {'arguments': (n), 'name': 'factorial' } (n == 0) or (n * factorial(n - 1))"
    ast = get_ast(text)
    
    assert isinstance(ast, Program)
    assert isinstance(ast.statements[0],FunctionDecl)

    # Verify Defun {'name': 'factorial', 'arguments': (n,)}
    function_decleration_node: FunctionDecl = ast.statements[0]
    assert function_decleration_node.func_name == 'factorial'
    assert len(function_decleration_node.params) == 1

    # Verify (n==0) or (n * factorial(n -1))
    assert isinstance(function_decleration_node.expr_node,BinOp)
    left1 = function_decleration_node.expr_node.left
    right1 = function_decleration_node.expr_node.right

    # Verify (n == 0)
    assert isinstance(left1,BinOp)
    
    # Verify (n * factorial(n -1))
    assert isinstance(right1, BinOp)

    #  Verify factorial(n - 1)
    assert isinstance(right1.right, FunctionCall)
    assert len(right1.right.actual_params) == 1
    assert isinstance(right1.right.actual_params[0], BinOp)

def test_function_declaration_correct_structure():
    texts = [
        ("Defun {'arguments': (n), 'name': 'factorial' } (n == 0) or (n * factorial(n - 1))",['n']),
        ("Defun {'arguments': (n,), 'name': 'factorial' } (n == 0) or (n * factorial(n - 1))",['n']),
        ("Defun {'name': 'factorial', 'arguments': (n,)} (n == 0) or (n * factorial(n - 1))",['n']),
        ("Defun {'name': 'factorial', 'arguments': (x,y)} (n == 0) or (n * factorial(n - 1))",['x','y']),
        ("Defun {'name': 'factorial', 'arguments': ()} (n == 0) or (n * factorial(n - 1))",[]),
    ]

    for text,expected_params in texts:
        ast = get_ast(text)
    
        assert isinstance(ast, Program)
        assert isinstance(ast.statements[0],FunctionDecl)

        # Verify function configuration (name, arguments)
        function_decleration_node: FunctionDecl = ast.statements[0]
        assert function_decleration_node.func_name == 'factorial'

        assert len(function_decleration_node.params) == len(expected_params)
        for index,expected_param_name in enumerate(expected_params):
            assert function_decleration_node.params[index].name == expected_param_name

        # Verify (n==0) or (n * factorial(n -1))
        assert isinstance(function_decleration_node.expr_node,BinOp)
        left1 = function_decleration_node.expr_node.left
        right1 = function_decleration_node.expr_node.right

        # Verify (n == 0)
        assert isinstance(left1,BinOp)
        
        # Verify (n * factorial(n -1))
        assert isinstance(right1, BinOp)

        #  Verify factorial(n - 1)
        assert isinstance(right1.right, FunctionCall)
        assert len(right1.right.actual_params) == 1
        assert isinstance(right1.right.actual_params[0], BinOp)

def test_function_declaration_incorrect_structure():
    texts = [
        "Defun {'arguments': (n,)} (n == 0) or (n * factorial(n - 1))",
        "Defun {'name': 'factorial'} (n == 0) or (n * factorial(n - 1))",
        "Defun {'name': 'factorial', 'arguments': (n,)} Defun {'name': 'foo', 'arguments': ()} (1 +2)"
        "Defun {'name': '', 'arguments': (n)} (n == 0) or (n * factorial(n - 1))",
    ]

    for text in texts:
        with pytest.raises(ParserError):
            get_ast(text)

def test_binary_correct_operations():
    tests =[
        ("True && False", Boolean,True,Boolean,False, TokenType.AND),
        ("True || False", Boolean,True,Boolean,False, TokenType.OR),
        ("5 == 10"      , Integer,5,Integer,10, TokenType.EQUAL),
        ("5 != 10"      , Integer,5,Integer,10, TokenType.NOT_EQUAL),
        ("5 >= 10"      , Integer,5,Integer,10, TokenType.GREATER_THAN_EQ),
        ("5 > 10"       , Integer,5,Integer,10, TokenType.GREATER_THAN),
        ("5 <= 10"      , Integer,5,Integer,10, TokenType.LESS_THAN_EQ),
        ("5 < 10"       , Integer,5,Integer,10, TokenType.LESS_THAN),
        ("5 + 10"       , Integer,5,Integer,10, TokenType.PLUS),
        ("5-5"          , Integer,5,Integer,5, TokenType.MINUS),
        ("5*5"          , Integer,5,Integer,5, TokenType.MUL),
        ("5/5"          , Integer,5,Integer,5, TokenType.DIV),
        ("5%5"          , Integer,5,Integer,5, TokenType.MODULO),
    ]

    for text,left_node_type,left_value,right_node_type,right_value,op_token_type in tests:
        ast = get_ast(text)

        assert isinstance(ast.statements[0],BinOp)
        assert isinstance(ast.statements[0].left,left_node_type)
        assert ast.statements[0].left.value == left_value
        assert isinstance(ast.statements[0].right,right_node_type)
        assert ast.statements[0].right.value == right_value
        assert ast.statements[0].op.type == op_token_type

def test_binary_incorrect_operations():
    texts = [
        "5 == 10 == 2",
        "5 != 10 != 2",
        "5 >= 10 >= 5",
        "5 > 10 > 5",
        "5 <= 10 <= 1",
        "5 < 10 < 5",
    ]

    for text in texts:
        with pytest.raises(ParserError):
            get_ast(text)

def test_lambda_expression():
    text = "(Lambd x.(Lambd y. (x + y)))"
    ast = get_ast(text)
    
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], Lambda)

    # Verify (Lambd x. (Lambd y. (x + y)))
    lambda1 = ast.statements[0]
    assert lambda1.param.name == 'x'

    # Verify (Lambd y. (x + y))
    assert isinstance(lambda1.expr_node,Lambda)

    lambda2 = lambda1.expr_node
    assert lambda2.param.name == 'y'

    # Verify x + y
    assert isinstance(lambda2.expr_node,BinOp)


def test_function_call():
    text = "factorial(5)"
    lexer = Lexer(text)
    parser = Parser(lexer)
    
    ast = parser.parse()
    
    assert isinstance(ast, Program)
    assert isinstance(ast.statements[0], FunctionCall)

    function_call_node: FunctionCall = ast.statements[0]
    assert function_call_node.func_name == 'factorial'
    assert len(function_call_node.actual_params) == 1
    assert isinstance(function_call_node.actual_params[0], Integer)

def test_syntax_error():
    text = "Defun {'name': 'factorial', 'arguments': (n,) (n == 0)"
    lexer = Lexer(text)
    parser = Parser(lexer)
    
    with pytest.raises(ParserError):
        parser.parse()
