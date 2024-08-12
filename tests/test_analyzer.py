import pytest
from src.interpreter.analyzer import SemanticAnalyzer
from src.interpreter.errors import SemanticError
from src.interpreter.symbol import ScopedSymbolTable, BuiltinTypeSymbol,FunctionSymbol,LambdaSymbol,ParamSymbol
import src.interpreter.ast as _ast
from src.interpreter.token import Token,TokenType


def test_built_in_types():
    builtin_types = ['INTEGER','BOOLEAN']

    global_scope = ScopedSymbolTable(
        scope_name='test',
        scope_level=1,
        enclosing_scope=None
    )

    global_scope._init_builtins()

    for _type in builtin_types:
        assert global_scope.lookup(_type) != None

def test_function_declaration_added_to_scope():
    func_name = 'test'
    func_params = [_ast.Param(Token(type="ID", value='x')),_ast.Param(Token(type="ID", value='y'))]
    func_decl = _ast.FunctionDecl(
        name= func_name,
        params=func_params,
        expr_node=_ast.NoOp()
    )

    analyzer = SemanticAnalyzer()
    analyzer.current_scope = ScopedSymbolTable(
        scope_level=1,
        enclosing_scope=None,
        scope_name='Root'
    )
    analyzer.visit(func_decl)

    function_symbol = analyzer.current_scope.lookup(func_name)

    assert function_symbol is not None
    assert isinstance(function_symbol,FunctionSymbol)
    assert function_symbol.name == func_name
    assert len(function_symbol.formal_params) == len(func_params)

    for index, param in enumerate(func_params):
        assert function_symbol.formal_params[index].name == param.name

def test_duplicate_function_declaration():
    func_name = 'test'
    func_params = _ast.Param(Token(type=TokenType.ID, value='x'))
    func_decls =[
        _ast.FunctionDecl(
            name= func_name,
            params=func_params,
            expr_node=_ast.NoOp()
        ),
        _ast.FunctionDecl(
            name= func_name,
            params=func_params,
            expr_node=_ast.NoOp()
        )
    ] 

    program = _ast.Program(func_decls)

    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.visit(program)

def test_function_call_resolution():
    program =_ast.Program([
        _ast.FunctionDecl(
            name= 'test',
            params=[_ast.Param(Token(TokenType.ID,'x'))],
            expr_node=_ast.NoOp()
        ),
        _ast.FunctionCall(
            token=Token(type=TokenType.ID,value='test'),
            actual_params=[_ast.Integer(Token(type=TokenType.INTEGER_CONST,value=5))]
        )
    ])

    analyzer = SemanticAnalyzer()
    analyzer.visit(program)
    
    assert True

def test_function_call_not_declared():
    program =_ast.Program([
        _ast.FunctionCall(
            token=Token(type=TokenType.ID,value='test'),
            actual_params=[_ast.Integer(Token(type=TokenType.INTEGER_CONST,value=5))]
        )
    ])

    analyzer = SemanticAnalyzer()

    with pytest.raises(SemanticError):
        analyzer.visit(program)

def test_function_call_unequal_param_count():
    program =_ast.Program([
        _ast.FunctionDecl(
            name= 'test',
            params=[_ast.Param(Token(TokenType.ID,'x'))],
            expr_node=_ast.NoOp()
        ),
        _ast.FunctionCall(
            token=Token(type=TokenType.ID,value='test'),
            actual_params=[]
        )
    ])

    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.visit(program)
    
    assert True

def test_function_call_undeclared_variable():
    func_decl = _ast.FunctionDecl(
        name='foo',
        params=[
            _ast.Param(
                Token(
                    type=TokenType.ID,
                    value='x'
                )
            )
        ],
        expr_node= _ast.BinOp(
            left=_ast.Param(
                Token(
                    type=TokenType.ID,
                    value='y'
                )
            ),
            right=_ast.Integer(
                Token(
                    type=TokenType.INTEGER_CONST,
                    value=10
                )
            ),
            op=TokenType.PLUS
        )
    )
    
    analyzer = SemanticAnalyzer()
    analyzer.current_scope = ScopedSymbolTable(
        scope_name='test',
        scope_level=1,
        enclosing_scope=None
    )
    
    with pytest.raises(SemanticError):
        analyzer.visit(func_decl)

def test_lambda_declaration():
    lambd = _ast.Lambda(
        param=_ast.Param(token=Token(type=TokenType.ID,value='x')),
        expr_node=_ast.NoOp()
    )

    analyzer = SemanticAnalyzer()
    analyzer.current_scope = ScopedSymbolTable(
        scope_name='Root',
        enclosing_scope=None,
        scope_level=1
    )
    analyzer.visit(lambd)

    lambd_symbol: LambdaSymbol = analyzer.current_scope.lookup(lambd.lambda_name)
       
    assert lambd_symbol is not None
    assert lambd_symbol.name == lambd.lambda_name
    assert lambd_symbol.param.name == lambd.param.name

def test_lambda_call():
    pass

def test_lambda_not_declared():
    pass

def test_param_in_table_lookup():
    table = ScopedSymbolTable(
        scope_name='test',
        enclosing_scope=None,
        scope_level=1
    )
    param = ParamSymbol('x')
    table.insert(param)

    param_symbol = table.lookup(param.name)

    assert param_symbol is not None

def test_param_in_table_lookup_recursive():
    table1 = ScopedSymbolTable(
        scope_name='foo',
        enclosing_scope=None,
        scope_level=1
    )

    table2 = ScopedSymbolTable(
        scope_name='bar',
        enclosing_scope=table1,
        scope_level=2
    )

    param = ParamSymbol('x')
    table1.insert(param)

    param_symbol = table2.lookup(param.name)

    assert param_symbol is not None

def test_param_in_table_lookup_no_recursive():
    table1 = ScopedSymbolTable(
        scope_name='foo',
        enclosing_scope=None,
        scope_level=1
    )

    table2 = ScopedSymbolTable(
        scope_name='bar',
        enclosing_scope=table1,
        scope_level=2
    )

    param = ParamSymbol('x')
    table1.insert(param)

    
    param_symbol = table2.lookup(param.name,current_scope_only=True)

    assert param_symbol is None
    
def test_param_not_int_table_lookup():
    table = ScopedSymbolTable(
        scope_name='foo',
        enclosing_scope=None,
        scope_level=1
    )    
    param_symbol = table.lookup('x',current_scope_only=True)

    assert param_symbol is None

def test_param_overriden_lookup():
    table1 = ScopedSymbolTable(
        scope_name='foo',
        enclosing_scope=None,
        scope_level=1
    )

    table2 = ScopedSymbolTable(
        scope_name='bar',
        enclosing_scope=table1,
        scope_level=2
    )

    param_name = 'x'
    param1 = ParamSymbol(param_name, type=BuiltinTypeSymbol('INTEGER'))
    param2 = ParamSymbol(param_name, type=BuiltinTypeSymbol('BOOLEAN'))
    table1.insert(param1)
    table2.insert(param2)

    param_symbol = table2.lookup(param_name)

    assert param_symbol.name == param_name
    assert isinstance(param_symbol.type,BuiltinTypeSymbol)
    assert param_symbol.type.name == 'BOOLEAN'