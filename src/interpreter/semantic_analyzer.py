from .interpreter import NodeVisitor
from .symbol import BuiltinTypeSymbol, ScopedSymbolTable, ParamSymbol, CallableSymbol
from .errors import SemanticError, ErrorCode
from .token import Token
from .ast import (
    Program,
    FunctionCall,
    FunctionDecl,
    Lambda,
    BinOp,
    NotOp,
    UnaryOp,
    NoOp,
    Param,
    Integer,
    Boolean,
    NestedLambda
)

class SemanticAnalyzer(NodeVisitor):
    """
    SemanticAnalyzer class

    Responsible for performing semantic analysis on an abstract syntax tree (AST)
    during the interpretation process. It traverses the AST,
    checking for semantic errors such as undeclared variables, and incorrect function usage.
    It also manages the scoping of variables and functions.
    """
    def __init__(self) -> None:
        self.current_scope: ScopedSymbolTable = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=None
        )

        self.current_scope._init_builtins()

    def error(self, error_code: ErrorCode, token: Token) -> None:
        """
        Raises a SemanticError with the given error code and token information.

        Args:
            error_code (ErrorCode): The specific error code representing the type of semantic error.
            token (Token): The token at which the semantic error occurred.

        Raises:
            SemanticError: An exception indicating a semantic error with detailed information.
        """
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f"{error_code.value} -> {token}"
        )
    
    def visit_Program(self,node: Program) -> None:
        """
        Handle a program AST node. Creates and manages the global scope.

        Args:
            node (Program): The program node representing the entire program.
        """
        
        for node in node.statements:
            self.visit(node)

    def visit_NoOp(self,node:NoOp) -> None:
        """
        Handle a no operation AST node.
        No action is performed here.
        
        Args:
            node (NoOp): The NoOp node to be visited.
        """
        pass

    def visit_BinOp(self,node: BinOp) -> None:
        """
        Handles a binary operation AST node.

        Traversing left and right operands.

        Args:
            node (BinOp): The binary operation node to be visited.
        """            
        self.visit(node.left)
        self.visit(node.right)

    def visit_FunctionDecl(self, node: FunctionDecl) -> None:
        """
        Handle a function declaration AST node.
        Processing its name, parameters, body, and creating a scope for the function.
        Taversing its expression node

        Args:
            node (FunctionDecl): The function declaration node to be visited.
        """
        func_name = node.func_name

        if self.current_scope.lookup(func_name) is not None:
            self.error(
                error_code=ErrorCode.DUPLICATE_SYMBOL,
                token=node
            )

        func_symbol = CallableSymbol(name=func_name)

        self.current_scope.insert(func_symbol)
        func_scope = ScopedSymbolTable(
            scope_name=func_name,
            scope_level= self.current_scope.scope_level +1,
            enclosing_scope= self.current_scope
        )

        self.current_scope = func_scope 

        for param in node.formal_parameters:
            param_symbol = ParamSymbol(param.name,BuiltinTypeSymbol)

            self.current_scope.insert(param_symbol)
            func_symbol.formal_params.append(param_symbol)

        self.visit(node.expr_node)

        self.current_scope = self.current_scope.enclosing_scope
        func_symbol.expr_ast = node.expr_node
        node.symbol = func_symbol

    def visit_FunctionCall(self, node: FunctionCall) -> None:
        """
        Visits a function call AST node.
        Traverses its parameters and attaches the function symbol to the AST node.

        Args:
            node (FunctionCall): The function call node to be visited.
        """
        function_symbol: CallableSymbol | ParamSymbol | None = self.current_scope.lookup(node.func_name)

        if function_symbol is None:
            self.error(
                error_code=ErrorCode.SYMBOL_NOT_FOUND,
                token=node.token
            )

        if isinstance(function_symbol,CallableSymbol):
            if len(function_symbol.formal_params) != len(node.actual_params):
                self.error(
                    error_code=ErrorCode.UNEQUAL_PARAM_COUNT,
                    token=node.token
                )

            node.symbol = function_symbol

        for index,param in enumerate(node.actual_params):
            self.visit(param)

            if isinstance(param, Lambda):
                param.symbol = self.current_scope.lookup(param.lambda_name)
                param.lambda_name = function_symbol.formal_params[index].name

    def visit_Lambda(self, node: Lambda) -> None:
        """
        Handles a lambda expression AST node.
        Processes its parameter and traverses its expression.

        Args:
            node (Lambda): The lambda expression node to be visited.
        """
        lambda_name = node.lambda_name

        param_symbols = [ParamSymbol(param.name, BuiltinTypeSymbol) for param in node.formal_params]
        lambda_symbol = CallableSymbol(name=lambda_name, formal_params=node.formal_params)

        self.current_scope.insert(lambda_symbol)
        lambda_scope = ScopedSymbolTable(
            scope_name=lambda_name,
            scope_level= self.current_scope.scope_level +1,
            enclosing_scope= self.current_scope
        )

        self.current_scope = lambda_scope 

        for symbol in param_symbols:
            self.current_scope.insert(symbol)

        self.visit(node.expr_node)

        self.current_scope = self.current_scope.enclosing_scope
        lambda_symbol.expr_ast = node.expr_node
        node.symbol = lambda_symbol

    def visit_NestedLambda(self, node: NestedLambda):
        self.visit(node.lambda_node)

        map(lambda x: self.visit(x),node.actual_params)


    def visit_NotOp(self, node: NotOp) -> None:
        """
        Handles a logical NOT operation AST node.
        No action is performed here to allow a truthy-falsy behavior

        Args:
            node (NotOp): The logical NOT operation node to be visited.
        """
        pass

    def visit_UnaryOp(self, node: UnaryOp) -> None:
        """
        Visits a unary operation AST node.
        No action is performed here.

        Args:
            node (UnaryOp): The unary operation node to be visited.
        """
        pass

    def visit_Param(self, node: Param) -> None:
        """
        Handles a actual parameter AST node.
        
        Verifies the parameter was already declared

        Args:
            node (Param): The parameter node to be visited.
        """
        param_symbol = self.current_scope.lookup(node.name)

        if param_symbol is None:
            self.error(
                error_code=ErrorCode.SYMBOL_NOT_FOUND,
                token=node.token
            )

    def visit_Integer(self, node: Integer) -> None:
        """
        Handles an integer literal AST node.
        Integer literals are leaf nodes representing constant values.
        No action is performed here.

        Args:
            node (Integer): The integer literal node to be visited.
        """
        pass

    def visit_Boolean(self, node: Boolean) -> None:
        """
        Visits a boolean literal AST node.
        Boolean literals are leaf nodes representing constant values.
        No action is performed here.

        Args:
            node (Boolean): The boolean literal node to be visited.
        """
        pass