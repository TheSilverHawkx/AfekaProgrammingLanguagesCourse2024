from .token import TokenType,Token
from uuid import uuid4
from .symbol import FunctionSymbol

class AST:
    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __repr__(self) -> str:
        return self.__str__()
  

class Program(AST):
    def __init__(self, statements: list[AST]) -> None:
        self.statements = statements

    def __str__(self) -> str:
        statements_str = [str(stmt) for stmt in self.statements]
        return super().__str__() + f"[\n{",\n".join(statements_str)}\n]"

class Integer(AST):
    """ Constant Integer AST Node"""
    def __init__(self, token: Token):
        self.token = token
        self.value: int = token.value

    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.value})"

class Boolean(AST):
    """ Constant Boolean AST Node"""
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value
    
    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.value})"

class BinOp(AST):
    """ Binary Operation AST Node"""
    def __init__(self, left: Token, op: Token, right: Token):
        self.left = left
        self.token = self.op = op
        self.right = right
    
    def __str__(self) -> str:
        return f"{super().__str__()}(left={self.left}, op={self.op}, right={self.right})"

class UnaryOp(AST):
    """ Unary Operation AST Node"""
    def __init__(self, op: Token, expr: Token):
        self.token = self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"{super().__str__()}(op={self.op}, value={self.expr})"
    
class NotOp(AST):
    """ Not Operation AST Node"""
    def __init__(self,expr: AST) -> None:
        self.expr = expr

    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.expr})"

class Param(AST):
    """ Function Parameter AST Node"""
    def __init__(self, token: Token) -> None:
        self.token = token
        self.name = token.value
    
    def __str__(self) -> str:
        return f"{super().__str__()}(name={self.name})"
    
class FunctionDecl(AST):
    """ Function Declaration AST Node"""
    def __init__(self, name:str, params: list[Param], expr_node):
        self.func_name = name
        self.params = params
        self.expr_node = expr_node

    def __str__(self) -> str:
        param_str = [str(param) for param in self.params]
        return f"{super().__str__()}(name={self.func_name}, params=[{",".join(param_str)}], expr={self.expr_node})"
    
class FunctionCall(AST):
    def __init__(self, token: Token, actual_params: list[Param] ) -> None:
        self.token = token
        self.func_name: str = token.value
        self.actual_params = actual_params
        self.func_symbol: FunctionSymbol = None
    
    def __str__(self) -> str:
        param_str = [str(param) for param in self.actual_params]
        return f"{super().__str__()}(name={self.func_name}, params=[{",".join(param_str)}])"
    
class Lambda(AST):
    """ Lambda Decleration AST Node"""
    def __init__(self,param:Param, expr_node: AST) -> None:
        self.lambda_name:str = f"lambda_{str(uuid4())[:8]}"
        self.param = param
        self.expr_node = expr_node

    def __str__(self):
        return f"{super().__str__()}(name={self.lambda_name}, param={self.param}, expr={self.expr_node})"
    
class NoOp(AST):
    """ Empty Operation AST Node"""
    pass

    def __str__(self) -> str:
        return f"{super().__str__()}()"
    