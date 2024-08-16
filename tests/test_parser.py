import pytest
from src.interpreter.parser import Parser
from src.interpreter.lexer import Lexer
from src.interpreter.ast import NotOp, Program, FunctionDecl, Lambda, BinOp, Integer, Boolean, FunctionCall,UnaryOp,Param,NestedLambda
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
    assert len(function_decleration_node.formal_parameters) == 1

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

        assert len(function_decleration_node.formal_parameters) == len(expected_params)
        for index,expected_param_name in enumerate(expected_params):
            assert function_decleration_node.formal_parameters[index].name == expected_param_name

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
        "Defun {'arguments': (n) 'name': 'factorial' } (n == 0) or (n * factorial(n - 1))",
        "Defun {'arguments': (n) 'name': 'factorial' }"
    ]

    for text in texts:
        with pytest.raises(ParserError):
            get_ast(text)

def test_binary_correct_operations():
    tests =[
        ("True && False", Boolean, True, Boolean, False, TokenType.AND),
        ("True || False", Boolean, True, Boolean, False, TokenType.OR),
        ("5 == 10"      , Integer, 5, Integer, 10, TokenType.EQUAL),
        ("5 != 10"      , Integer, 5, Integer, 10, TokenType.NOT_EQUAL),
        ("5 >= 10"      , Integer, 5, Integer, 10, TokenType.GREATER_THAN_EQ),
        ("5 > 10"       , Integer, 5, Integer, 10, TokenType.GREATER_THAN),
        ("5 <= 10"      , Integer, 5, Integer, 10, TokenType.LESS_THAN_EQ),
        ("5 < 10"       , Integer, 5, Integer, 10, TokenType.LESS_THAN),
        ("5 + 10"       , Integer, 5, Integer, 10, TokenType.PLUS),
        ("5-5"          , Integer, 5, Integer, 5, TokenType.MINUS),
        ("5*5"          , Integer, 5, Integer, 5, TokenType.MUL),
        ("5/5"          , Integer, 5, Integer, 5, TokenType.DIV),
        ("5%5"          , Integer, 5, Integer, 5, TokenType.MODULO),
        ("(1 + 2)"      , Integer, 1, Integer, 2, TokenType.PLUS),
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
        "5 <> 3",
        "5 || && 3",
        "5 + == 3",
        "(5 + 3",
        "(5 + +)",
    ]

    for text in texts:
        with pytest.raises(ParserError):
            get_ast(text)

def test_binary_operation_precedence():
    text = "5 + 3 * 2 - 8 / 4"
    ast = get_ast(text)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0],BinOp)
    binop1: BinOp = ast.statements[0]

    assert isinstance(binop1.left,Integer)
    assert binop1.left.value == 5
    assert binop1.op.type == TokenType.PLUS
    assert isinstance(binop1.right,BinOp)

    binop2: BinOp = binop1.right
    assert isinstance(binop2.left,BinOp)
    assert binop2.op.type == TokenType.MINUS

    binop3: BinOp = binop2.left
    assert isinstance(binop3.left,Integer)
    assert binop3.left.value == 3
    assert isinstance(binop3.right,Integer)
    assert binop3.right.value == 2
    assert binop3.op.type == TokenType.MUL
                      
    binop4: BinOp = binop2.right
    assert isinstance(binop4.left,Integer)
    assert binop4.left.value == 8
    assert isinstance(binop4.right,Integer)
    assert binop4.right.value == 4
    assert binop4.op.type == TokenType.DIV

def test_binary_opearation_precedence_paren():
    text = "((5 + 3) * 2) - 4"
    ast = get_ast(text)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0],BinOp)
    binop1: BinOp = ast.statements[0]

    assert isinstance(binop1.left, BinOp)
    assert isinstance(binop1.right, Integer)
    assert binop1.right.value == 4
    assert binop1.op.type == TokenType.MINUS

    binop2 = binop1.left
    assert isinstance(binop2.left, BinOp)
    assert isinstance(binop2.right, Integer)
    assert binop2.right.value == 2
    assert binop2.op.type == TokenType.MUL

    binop3 = binop2.left
    assert isinstance(binop3.left, Integer)
    assert binop3.left.value == 5
    assert isinstance(binop3.right, Integer)
    assert binop3.right.value == 3
    assert binop3.op.type == TokenType.PLUS

def test_factor_consts():
    tests = [
        ('8'    , Integer,8),
        ('True' , Boolean,True),
        ('False', Boolean,False),
        ('(8)'  , Integer,8)
    ]

    for test,node_type,expected_value in tests:
        ast = get_ast(test)

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0],node_type)
        assert ast.statements[0].value == expected_value

def test_factor_function_call_const_params():
    tests = [
        ('foo(3)'   ,'foo',[Integer],[3]),
        ('foo()'    ,'foo',[],[]),
        ('bar(3,5)' ,'bar',[Integer,Integer],[3,5]),
        ('bar(3,True)' ,'bar',[Integer,Boolean],[3,True]),
    ]
    
    for test, func_name, params_types, param_values in tests:
        ast = get_ast(test)

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0],FunctionCall)
        assert ast.statements[0].func_name == func_name
        assert len(ast.statements[0].actual_params) == len(params_types)

        for index,ap in enumerate(ast.statements[0].actual_params):
            assert isinstance(ap,params_types[index] )
            assert ap.value == param_values[index]

def test_factor_function_call_expr():
    func_name = 'baz'
    text = f'{func_name}(3 || True)'
    ast = get_ast(text)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0],FunctionCall)
    func_call = ast.statements[0]

    assert func_call.func_name == func_name
    assert len(func_call.actual_params) == 1

    param = func_call.actual_params[0]

    assert isinstance(param, BinOp)
    assert isinstance(param.left,Integer)
    assert param.left.value == 3
    assert isinstance(param.right,Boolean)
    assert param.right.value == True
    assert param.op.type == TokenType.OR

def test_factor_function_call_lambd():
    func_name = 'foo'
    text = f'{func_name}((Lambd x,y. x+y))'
    ast = get_ast(text)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0],FunctionCall)
    func_call = ast.statements[0]

    assert func_call.func_name == func_name
    assert len(func_call.actual_params) == 1

    lambda_decl = func_call.actual_params[0]

    assert isinstance(lambda_decl, Lambda)
    assert len(lambda_decl.formal_params) == 2
    assert isinstance(lambda_decl.expr_node,BinOp)
    bin_op = lambda_decl.expr_node
    assert isinstance(bin_op.left,Param)
    assert bin_op.op.type == TokenType.PLUS
    assert isinstance(bin_op.right,Param)

def test_factor_function_call_nested_lambd():
    func_name = 'foo'
    text = f'{func_name}((Lambd x,y. (Lambd z. z+ 5 + x)(y) + 1))'
    ast = get_ast(text)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0],FunctionCall)
    func_call = ast.statements[0]

    assert func_call.func_name == func_name
    assert len(func_call.actual_params) == 1

    lambda_decl = func_call.actual_params[0]

    assert isinstance(lambda_decl, Lambda)
    assert len(lambda_decl.formal_params) == 2
    assert isinstance(lambda_decl.expr_node,BinOp)
    bin_op = lambda_decl.expr_node
    assert isinstance(bin_op.left,NestedLambda)

    nested_lambda = bin_op.left

    assert len(nested_lambda.lambda_node.formal_params) == 1
    assert len(nested_lambda.actual_params) == 1

    assert bin_op.op.type == TokenType.PLUS
    assert isinstance(bin_op.right,Integer)

def test_factor_unary_operation():
    tests = [
        ('-3'    , TokenType.MINUS  ,Integer),
        ('+3'    , TokenType.PLUS   ,Integer),
        ('-True' , TokenType.MINUS  ,Boolean),
        ('-(1+1)', TokenType.MINUS  , BinOp)
    ]

    for test,op_type,expr_node_type in tests:
        ast = get_ast(test)

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0],UnaryOp)
        assert ast.statements[0].op.type == op_type
        assert isinstance(ast.statements[0].expr,expr_node_type )

def test_not_operation():
    tests = [
        ('!True' , Boolean),
        ('!(True && True)', BinOp),
    ]

    for test,expr_node_type in tests:
        ast = get_ast(test)

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0],NotOp)
        assert isinstance(ast.statements[0].expr,expr_node_type )