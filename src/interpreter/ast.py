from .token import Token
from uuid import uuid4
from .symbol import FunctionSymbol
from abc import ABC
import ast

class AST(metaclass=ABC):
    """
    The base class for all nodes in the Abstract Syntax Tree (AST).
    """
    def __str__(self) -> str:
        return "<" + self.__class__.__name__ + ">"
    
    def __repr__(self) -> str:
        return self.__str__()
  

class Program(AST):
    """
    Represents the entire program in the AST. Contains a list of statements.

    Attributes:
        statements (list[AST]): A list of AST nodes representing the statements in the program.
    """
    def __init__(self, statements: list[AST]) -> None:
        self.statements = statements

class Integer(AST):
    """
    Represents a constant integer value in the AST.

    Attributes:
        token (Token): The token associated with the integer literal.
        value (int): The integer value of the token.
    """
    def __init__(self, token: Token):
        self.token = token
        self.value: int = token.value

class Boolean(AST):
    """
    Represents a constant boolean value in the AST.

    Attributes:
        token (Token): The token associated with the boolean literal.
        value (bool): The boolean value of the token.
    """
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

class BinOp(AST):
    """
    Represents a binary operation in the AST.

    Attributes:
        left (AST): The left operand of the binary operation.
        op (Token): The operator token of the binary operation.
        right (AST): The right operand of the binary operation.

    Usage:
        bin_op_node = BinOp(left=expr1, op=plus_token, right=expr2)
    """
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right
    
    def __str__(self) -> str:
        return f"{super().__str__()}(left={self.left}, op={self.op}, right={self.right})"

class UnaryOp(AST):
    """
    Represents a unary operation in the AST.

    Attributes:
        op (Token): The operator token of the unary operation.
        expr (AST): The operand of the unary operation.

    Usage:
        unary_op_node = UnaryOp(op=minus_token, expr=expr)
    """
    def __init__(self, op: Token, expr: Token):
        self.token = self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"{super().__str__()}(op={self.op}, value={self.expr})"
    
class NotOp(AST):
    """
    Represents a logical NOT operation in the AST

    Attributes:
        expr (AST): The operand of the NOT operation.

    Usage:
        not_op_node = NotOp(expr=expr_node)
    """
    def __init__(self,expr: AST) -> None:
        self.expr = expr

    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.expr})"

class Param(AST):
    """
    Represents a function parameter in the AST.

    Attributes:
        token (Token): The token representing the parameter.
        name (str): The name of the parameter.

    Usage:
        param_node = Param(token=param_token)
    """
    def __init__(self, token: Token) -> None:
        self.token = token
        self.name = token.value
    
    def __str__(self) -> str:
        return f"{super().__str__()}(name={self.name})"
    
class FunctionDecl(AST):
    """
    Represents a function declaration in the AST.

    Attributes:
        func_name (str): The name of the function.
        params (list[Param]): A list of parameter nodes representing the function's parameters.
        expr_node (AST): The body expression of the function.

    Usage:
        func_decl_node = FunctionDecl(name='foo', params=[param1, param2], expr_node=body_expr)
    """
    def __init__(self, name:str, params: list[Param], expr_node: AST):
        self.func_name = name
        self.params = params
        self.expr_node = expr_node

    def __str__(self) -> str:
        param_str = [str(param) for param in self.params]
        return f"{super().__str__()}(name={self.func_name}, params=[{",".join(param_str)}], expr={self.expr_node})"
    
class FunctionCall(AST):
    """
    Represents a function call in the AST.

    Attributes:
        token (Token): The token representing the function being called.
        func_name (str): The name of the function being called.
        actual_params (list[AST]): A list of parameter nodes representing the actual arguments passed to the function.
        func_symbol (FunctionSymbol): The symbol representing the function in the symbol table.

    Usage:
        func_call_node = FunctionCall(token=call_token, actual_params=[arg1, arg2])
    """
    def __init__(self, token: Token, actual_params: list[Param] ) -> None:
        self.token = token
        self.func_name: str = token.value
        self.actual_params = actual_params
        self.func_symbol: FunctionSymbol = None
    
    def __str__(self) -> str:
        param_str = [str(param) for param in self.actual_params]
        return f"{super().__str__()}(name={self.func_name}, params=[{",".join(param_str)}])"
    
class Lambda(AST):
    """
    Represents a lambda expression in the AST.

    Attributes:
        lambda_name (str): The unique name of the lambda expression, generated using a UUID.
        param (Param): The parameter of the lambda expression.
        expr_node (AST): The body expression of the lambda.

    Usage:
        lambda_node = Lambda(param=param, expr_node=body_expr)
    """
    def __init__(self,param:Param, expr_node: AST) -> None:
        self.lambda_name:str = f"lambda_{str(uuid4())[:8]}"
        self.param = param
        self.expr_node = expr_node

    def __str__(self):
        return f"{super().__str__()}(name={self.lambda_name}, param={self.param}, expr={self.expr_node})"
    
class NoOp(AST):
    """
    Represents a no operation node in the AST.

    Usage:
        noop_node = NoOp()
    """
    pass

    def __str__(self) -> str:
        return f"{super().__str__()}()"
    