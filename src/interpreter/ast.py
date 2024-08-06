from .token import TokenType,Token
from uuid import uuid4

class AST:
    def __str__(self) -> str:
        return self.__class__.__name__
  

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
        self.value = token.value

    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.value})"
    
    __repr__ = __str__

class Boolean(AST):
    """ Constant Boolean AST Node"""
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value
    
    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.value})"
    
    __repr__ = __str__

class BinOp(AST):
    """ Binary Operation AST Node"""
    def __init__(self, left: Token, op: Token, right: Token):
        self.left = left
        self.token = self.op = op
        self.right = right
    
    def __str__(self) -> str:
        return f"{super().__str__()}(left={self.left}, op={self.op}, right={self.right})"
    
    __repr__ = __str__

class UnaryOp(AST):
    """ Unary Operation AST Node"""
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"{super().__str__()}(op={self.op}, value={self.expr})"
    
    __repr__ = __str__

class NotOp(AST):
    """ Not Operation AST Node"""
    def __init__(self,expr: AST) -> None:
        self.expr = expr

    def __str__(self) -> str:
        return f"{super().__str__()}(value={self.expr})"
    
    __repr__ = __str__

class Param(AST):
    """ Function Parameter AST Node"""
    def __init__(self, token: Token) -> None:
        self.token = token
        self.name = token.value
    
    def __str__(self) -> str:
        return f"{super().__str__()}(name={self.name})"
    
    __repr__ = __str__

class FunctionDecl(AST):
    """ Function Declaration AST Node"""
    def __init__(self, name:str, params: list[Param], expr_node):
        self.func_name = name
        self.params = params
        self.expr_node = expr_node

    def __str__(self) -> str:
        param_str = [str(param) for param in self.params]
        return f"{super().__str__()}(name={self.func_name}, params=[{",".join(param_str)}], expr={self.expr_node})"
    
    __repr__ = __str__
    
class FunctionCall(AST):
    def __init__(self, token: Token, actual_params ) -> None:
        self.token = token
        self.func_name = token.value
        self.actual_params = actual_params
        self.func_symbol = None
    
    def __str__(self) -> str:
        param_str = [str(param) for param in self.actual_params]
        return f"{super().__str__()}(name={self.func_name}, params=[{",".join(param_str)}])"
    
    __repr__ = __str__

class Lambda(AST):
    """ Lambda Decleration AST Node"""
    def __init__(self,param:Param, expr_node: AST) -> None:
        self.lambda_name:str = f"lambda_{str(uuid4())[:8]}"
        self.param = param
        self.expr_node = expr_node

    def __str__(self):
        return f"{super().__str__()}(name={self.lambda_name}, param={self.param}, expr={self.expr_node})"
    
    __repr__ = __str__
    

class NoOp(AST):
    """ Empty Operation AST Node"""
    pass

    def __str__(self) -> str:
        return f"{super().__str__()}()"
    
    __repr__ = __str__





