from .interpreter import NodeVisitor
from .symbol import ScopedSymbolTable, ParamSymbol, FunctionSymbol, LambdaSymbol
from .errors import SemanticError, ErrorCode
from .token import Token
from .ast import Program,FunctionCall,FunctionDecl,Lambda,BinOp,NotOp,UnaryOp,NoOp,Param,Integer,Boolean

class SemanticAnalyzer(NodeVisitor):
    def __init__(self) -> None:
        self.current_scope: ScopedSymbolTable = None

    def error(self, error_code: ErrorCode, token: Token) -> None:
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f"{error_code.value} -> {token}"
        )
    
    def visit_Program(self,node: Program) -> None:
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope
        )

        global_scope._init_builtins()

        self.current_scope = global_scope

        # Visit Subtree
        for node in node.statements:
            self.visit(node)
        
        self.current_scope = self.current_scope.enclosing_scope

    def visit_NoOp(self,node:NoOp) -> None:
        pass

    def visit_BinOp(self,node: BinOp) -> None:
        self.visit(node.left)
        self.visit(node.right)

    def visit_FunctionDecl(self, node: FunctionDecl) -> None:
        func_name = node.func_name
        func_symbol = FunctionSymbol(name=func_name)

        self.current_scope.insert(func_symbol)
        func_scope = ScopedSymbolTable(
            scope_name=func_name,
            scope_level= self.current_scope.scope_level +1,
            enclosing_scope= self.current_scope
        )

        self.current_scope = func_scope 

        for param in node.params:
            param_symbol = ParamSymbol(param.name)

            self.current_scope.insert(param_symbol)
            func_symbol.formal_params.append(param_symbol)

        self.visit(node.expr_node)

        self.current_scope = self.current_scope.enclosing_scope
        func_symbol.expr_ast = node.expr_node

    def visit_FunctionCall(self, node: FunctionCall) -> None:
        for param in node.actual_params:
            self.visit(param)

        node.func_symbol = self.current_scope.lookup(node.func_name)

    def visit_Lambda(self, node: Lambda) -> None:
        lambda_name = node.lambda_name
        lambda_symbol = LambdaSymbol(name=lambda_name)

        self.current_scope.insert(lambda_symbol)
        lambda_scope = ScopedSymbolTable(
            scope_name=lambda_name,
            scope_level= self.current_scope.scope_level +1,
            enclosing_scope= self.current_scope
        )

        self.current_scope = lambda_scope 

        param_symbol = ParamSymbol(node.param.name)
        self.current_scope.insert(param_symbol)
        lambda_symbol.param = param_symbol

        self.visit(node.expr_node)

        self.current_scope = self.current_scope.enclosing_scope
        lambda_symbol.expr_ast = node.expr_node
        
    def visit_NotOp(self, node: NotOp) -> None:
        # TODO: maybe add a check that the encapsulated node is boolean?
        pass

    def visit_UnaryOp(self, node: UnaryOp) -> None:
        # TODO: maybe add a check that the encapsulated node is integer?
        pass

    def visit_Param(self, node: Param) -> None:
        pass

    def visit_Integer(self, node: Integer) -> None:
        pass

    def visit_Boolean(self, node: Boolean) -> None:
        pass